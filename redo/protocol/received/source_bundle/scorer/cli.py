"""argparse front-ends.

Two console scripts (declared in pyproject.toml [project.scripts]):

    gpcr-score       — single input
    gpcr-score-batch — manifest-driven batch, never aborts on raise
                       (amendment 3)

Neither front-end exposes any flag that silences an assertion. Assertions
raise → single-input exits non-zero; batch driver records the failing
column and continues.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from scorer.orchestrator import run_scorer, score_and_capture
from scorer.schema import CSV_COLUMNS, ScorerRow, StateClaim


VALID_STATES = tuple(s.value for s in StateClaim)


def _parser_single() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-score",
        description="Deterministic GPCR conformational-state scorer (single input).",
    )
    p.add_argument("--input", required=True, help="path to a PDB or CIF")
    p.add_argument("--receptor", default=None,
                   help="receptor slug (uppercase). Optional: resolver "
                        "extracts from path via word-boundary regex.")
    p.add_argument("--state-claim", required=True, choices=VALID_STATES,
                   help="conformational state claim for the input")
    p.add_argument("--out", required=True,
                   help="output directory (per-row artefacts go here)")
    p.add_argument("--ref-set", default="refs/reference_set.csv",
                   help="path to refs/reference_set.csv (default: repo-relative)")
    p.add_argument("--cache-dir", default="refs/cache",
                   help="GPCRdb/SIFTS cache root")
    p.add_argument("--input-species", default="human",
                   help="species of the input construct (feeds A5)")
    return p


def _parser_batch() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-score-batch",
        description="Batch scorer. Never aborts on raise (amendment 3).",
    )
    p.add_argument("--manifest", required=True,
                   help="CSV with columns: prediction_path, receptor_slug, "
                        "state_claim, input_species (optional)")
    p.add_argument("--out", required=True,
                   help="output directory (rows CSV + JSON sidecars)")
    p.add_argument("--ref-set", default="refs/reference_set.csv")
    p.add_argument("--cache-dir", default="refs/cache")
    return p


def _write_row(row: ScorerRow, out_dir: Path) -> None:
    """Write CSV row + JSON sidecar for a single input."""
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "rows.csv"
    is_new = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS))
        if is_new:
            w.writeheader()
        w.writerow(row.to_csv_row())
    # JSON sidecar named by input basename
    if row.input_path:
        sidecar = out_dir / (Path(row.input_path).name + ".scorer.json")
        sidecar.write_text(row.to_json_sidecar())


def main(argv: list[str] | None = None) -> int:
    args = _parser_single().parse_args(argv)
    out = Path(args.out).resolve()
    try:
        row = run_scorer(
            input_path=args.input,
            receptor_hint=args.receptor,
            input_state_claim=args.state_claim,
            output_dir=out,
            ref_set_csv_path=args.ref_set if Path(args.ref_set).exists() else None,
            cache_dir=args.cache_dir,
            input_species=args.input_species,
        )
        _write_row(row, out)
        return 0
    except Exception as e:
        # Reuse the batch capture path to persist a failure row
        row, err = score_and_capture(
            input_path=args.input,
            receptor_hint=args.receptor,
            input_state_claim=args.state_claim,
            output_dir=out,
            ref_set_csv_path=args.ref_set if Path(args.ref_set).exists() else None,
            cache_dir=args.cache_dir,
            input_species=args.input_species,
        )
        _write_row(row, out)
        print(f"FAILED [{type(err).__name__ if err else 'Unknown'}]: {err}",
              file=sys.stderr)
        return 2


def batch_main(argv: list[str] | None = None) -> int:
    args = _parser_batch().parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    manifest = Path(args.manifest)
    if not manifest.exists():
        print(f"manifest not found: {manifest}", file=sys.stderr)
        return 2

    census: dict[str, int] = {}
    total = 0
    with manifest.open() as f:
        reader = csv.DictReader(f)
        for row_in in reader:
            if not row_in or (row_in.get("prediction_path") or "").startswith("#"):
                continue
            total += 1
            input_path = row_in["prediction_path"]
            receptor = row_in.get("receptor_slug") or None
            state = row_in.get("state_claim") or StateClaim.Ga_COUPLED_ACTIVE.value
            species = row_in.get("input_species") or "human"
            row_out, err = score_and_capture(
                input_path=input_path,
                receptor_hint=receptor,
                input_state_claim=state,
                output_dir=out,
                ref_set_csv_path=args.ref_set if Path(args.ref_set).exists() else None,
                cache_dir=args.cache_dir,
                input_species=species,
            )
            _write_row(row_out, out)
            if err is not None:
                census[err.assertion_id] = census.get(err.assertion_id, 0) + 1

    # emit failure census as JSON for the paper figure
    (out / "failure_census.json").write_text(json.dumps({
        "total": total,
        "passed": total - sum(census.values()),
        "by_assertion": census,
    }, indent=2))
    print(f"scored {total} inputs; {sum(census.values())} failed; census: {census}",
          file=sys.stderr)

    # Finding #7 tripwire (docs/AUDIT_TRAIL.md#7): if any measurement
    # column in rows.csv is dominated by NaN, we are silently emitting a
    # pipeline where the axis was undefined for essentially every row.
    # That is the same class of bug as the reference-set silent-NaN
    # (delta_to_active was NaN on 91,950 rows for weeks without being
    # noticed). Raise on >95% NaN; warn on >50%. Ignore rows.csv absence
    # or empty batches — they are already loud in earlier logs.
    _check_batch_nan_tripwire(out)
    return 0


# ---------------------------------------------------------------------------
# Finding #7 batch-side tripwire
# ---------------------------------------------------------------------------


# Numeric axis / delta columns that a batch is expected to populate on the
# happy path. If ANY of these is >=95% NaN across a batch, that's the
# silent-drop pattern this tripwire catches. Kept as a data-driven list so
# adding a new axis in schema.py automatically extends coverage.
_BATCH_TRIPWIRE_NUMERIC_COLUMNS: tuple[str, ...] = (
    "d_tm6_r350_r630_ca",
    "d_npxxy_y558_y753_ca",
    "d_tm5_outward_r350_r558_ca",
    "d_y558_pack_min_heavy",
    "d_dry_sidechain_r350cz_e630oe1",
    "icl2_helical_frac",
    "plddt_mean",
    "receptor_d_active_ref",
    "receptor_d_inactive_ref",
    "receptor_midpoint",
    "delta_to_active",
    "delta_to_inactive",
)


def _nan_fraction(values: list[str]) -> tuple[int, int]:
    """Return (n_nan, n_total_non_empty) for a column of strings."""
    n_nan = 0
    n_total = 0
    for v in values:
        if v is None or v == "":
            # empty cells are neither present nor NaN — skip. A failure row
            # with early-abort assertion has empty axes, not "nan", and it
            # is already accounted for in the census above.
            continue
        n_total += 1
        s = str(v).strip().lower()
        if s in ("nan", "-nan", "+nan"):
            n_nan += 1
            continue
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        if f != f:  # NaN
            n_nan += 1
    return n_nan, n_total


def _check_batch_nan_tripwire(out: Path) -> None:
    rows_csv = out / "rows.csv"
    if not rows_csv.exists():
        return
    with rows_csv.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return
    by_col_nan: dict[str, tuple[int, int]] = {}
    for col in _BATCH_TRIPWIRE_NUMERIC_COLUMNS:
        if not rows or col not in rows[0]:
            continue
        values = [r.get(col, "") for r in rows]
        n_nan, n_total = _nan_fraction(values)
        by_col_nan[col] = (n_nan, n_total)

    raise_cols: list[str] = []
    warn_cols: list[str] = []
    for col, (n_nan, n_total) in by_col_nan.items():
        if n_total < 10:  # too small to judge — don't tripwire
            continue
        frac = n_nan / n_total
        if frac > 0.95:
            raise_cols.append(f"{col}={n_nan}/{n_total} ({frac:.1%})")
        elif frac > 0.50:
            warn_cols.append(f"{col}={n_nan}/{n_total} ({frac:.1%})")

    if warn_cols:
        print(
            f"WARN batch tripwire (finding #7): >50% NaN in {len(warn_cols)} "
            f"column(s): {'; '.join(warn_cols)}",
            file=sys.stderr,
        )
    if raise_cols:
        raise RuntimeError(
            f"batch tripwire (finding #7): >95% NaN in "
            f"{len(raise_cols)} numeric column(s) — the pipeline is silently "
            f"emitting undefined measurements. Columns:\n"
            + "\n".join(f"  {c}" for c in raise_cols)
            + "\nInvestigate the orchestrator / references path before "
            f"consuming {rows_csv}."
        )


if __name__ == "__main__":
    sys.exit(main())
