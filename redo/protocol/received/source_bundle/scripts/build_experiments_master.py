"""Aggregate every per-experiment ``rows.csv`` into ``experiments/MASTER.csv``
and regenerate the ``experiments/README.md`` index.

The MASTER.csv is a derived view — never edited by hand, always
regenerated. Per-experiment ``rows.csv`` files are the source of truth;
this script just concatenates + sorts them.

Excludes ``_reference_*/`` folders from MASTER by design — the v3.7
reference corpus stays at ``artefacts/rows_enriched_v3_7.csv``, joined
manually by analysts who want to compare new work to the frozen
baseline. See silly-leaping-aho.md §"MASTER.csv scope".

Usage:

    scripts/build_experiments_master.py
    scripts/build_experiments_master.py --experiments-root path/to/experiments
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
EXPERIMENTS_ROOT = REPO / "experiments"


# =============================================================================
# Walk experiments/ for rows.csv files
# =============================================================================


_NNN_RE = __import__("re").compile(r"^(?:\d{3}_|_reference_)")


def experiment_slug_for(rows_csv: Path, experiments_root: Path) -> str:
    """Given a ``rows.csv`` path, return its owning experiment slug.

    Handles both shapes:
      - Canonical: ``experiments/NNN_slug/analysis/rows.csv`` — walk
        up to the first ancestor whose name matches ``NNN_`` (or
        ``_reference_``).
      - Grandfathered flat: ``experiments/NNN_slug/rows.csv`` — the
        parent directory *is* the slug.

    Falls back to ``rows_csv.parent.name`` for anything the walk
    misses (e.g. nested study folders like
    ``mn_consensus/013_../rows.csv``).
    """
    try:
        rel = rows_csv.resolve().relative_to(experiments_root.resolve())
    except ValueError:
        return rows_csv.parent.name
    for part in rel.parts:
        if _NNN_RE.match(part):
            return part
    return rows_csv.parent.name


def find_experiment_rows(experiments_root: Path) -> list[Path]:
    """Return every ``rows.csv`` under ``experiments_root``, walking
    into study subfolders (e.g. ``mn_consensus/013_.../rows.csv``) and
    the new ``NNN_slug/analysis/rows.csv`` shape.
    Excludes ``_reference_*/`` folders by design and the empty template
    folder ``000_template/``.

    Sorted deterministically.
    """
    if not experiments_root.exists():
        return []
    out: list[Path] = []
    for rows_csv in sorted(experiments_root.rglob("rows.csv")):
        # Skip anything under a _reference_* subtree or the template
        parts = rows_csv.parts
        if any(p.startswith("_reference_") for p in parts):
            continue
        if "000_template" in parts:
            continue
        out.append(rows_csv)
    return out


# =============================================================================
# Concatenate to MASTER.csv
# =============================================================================


def concatenate_rows(rows_csvs: list[Path],
                     experiments_root: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Load every rows.csv, prepend a synthetic ``experiment_slug`` column
    from the folder name if the row doesn't already carry one, and
    return ``(header_cols, sorted_rows)``.

    Sort key: (experiment_slug, receptor_slug, backbone, seed_used_int).
    """
    all_cols: list[str] = ["experiment_slug"]
    seen_cols: set[str] = {"experiment_slug"}
    rows: list[dict[str, str]] = []

    for rows_csv in rows_csvs:
        slug = experiment_slug_for(rows_csv, experiments_root)
        with rows_csv.open() as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                continue    # empty file — nothing to concat
            for col in reader.fieldnames:
                if col not in seen_cols:
                    seen_cols.add(col)
                    all_cols.append(col)
            for row in reader:
                if not row.get("experiment_slug"):
                    row["experiment_slug"] = slug
                rows.append(row)

    def _sort_key(r: dict[str, str]) -> tuple[str, str, str, int]:
        try:
            seed = int(r.get("seed_used", "0") or "0")
        except ValueError:
            seed = 0
        return (
            r.get("experiment_slug", ""),
            r.get("receptor_slug", ""),
            r.get("backbone", ""),
            seed,
        )

    rows.sort(key=_sort_key)
    return all_cols, rows


def write_master(cols: list[str], rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


# =============================================================================
# Index README.md
# =============================================================================


_README_HEADER = (
    "# Experiments\n"
    "\n"
    "Auto-generated index of the per-experiment folders under this directory.\n"
    "**Do not edit by hand** — this file is overwritten by\n"
    "`scripts/build_experiments_master.py`.\n"
    "\n"
    "For the pre-framework baseline, see "
    "[`../artefacts/rows_enriched_v3_7.csv`](../artefacts/rows_enriched_v3_7.csv)\n"
    "(17,568 rows, frozen, kept separate from MASTER by design — analysts join manually).\n"
    "\n"
)


def _experiment_row_summary(rows_csv: Path,
                            experiments_root: Path) -> dict[str, Any]:
    """Return summary stats about one experiment's rows.csv.

    Backbone is inferred from the scored ``input_path`` when a ``backbone``
    column isn't directly present (scorer.schema.ScorerRow doesn't emit
    one; the manifest does but per-experiment rows.csv comes from the
    scorer). Uses the same `detect_backbone` heuristic as the enricher.
    """
    import sys as _sys
    if str(REPO) not in _sys.path:
        _sys.path.insert(0, str(REPO))
    from scripts.enrich_partner_metadata import detect_backbone
    slug = experiment_slug_for(rows_csv, experiments_root)
    n_rows = 0
    receptors: Counter = Counter()
    backbones: Counter = Counter()
    ligands: Counter = Counter()
    with rows_csv.open() as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return {"slug": slug, "n_rows": 0, "receptors": "-",
                    "backbones": "-", "ligand_types": "-",
                    "last_updated": _dt.datetime.fromtimestamp(
                        rows_csv.stat().st_mtime, tz=_dt.timezone.utc
                    ).strftime("%Y-%m-%d")}
        for r in reader:
            n_rows += 1
            receptors[r.get("receptor_slug", "")] += 1
            bb = r.get("backbone", "")
            if not bb:
                bb = detect_backbone(r.get("input_path", ""))
            if bb and bb != "unknown":
                backbones[bb] += 1
            ligands[r.get("ligand_type", "") or "none"] += 1
    last_updated = _dt.datetime.fromtimestamp(
        rows_csv.stat().st_mtime, tz=_dt.timezone.utc
    ).strftime("%Y-%m-%d")
    return {
        "slug": slug,
        "n_rows": n_rows,
        "receptors": ",".join(sorted(receptors)) or "-",
        "backbones": ",".join(sorted(k for k in backbones if k)) or "-",
        "ligand_types": ",".join(sorted(ligands)) or "-",
        "last_updated": last_updated,
    }


def write_index(rows_csvs: list[Path], index_out: Path,
                experiments_root: Path) -> None:
    lines = [_README_HEADER, "\n"]
    if not rows_csvs:
        lines.append("_No experiments have been rescored yet._\n")
        lines.append("Run `scripts/spawn_experiment.py --slug ... --spec ...` to scaffold one.\n")
        index_out.write_text("".join(lines))
        return
    lines.append(
        "| slug | n_rows | receptors | backbones | ligand_types | last_updated |\n"
    )
    lines.append("|---|---:|---|---|---|---|\n")
    for rows_csv in rows_csvs:
        s = _experiment_row_summary(rows_csv, experiments_root)
        lines.append(
            f"| [{s['slug']}]({s['slug']}/) | {s['n_rows']} "
            f"| {s['receptors']} | {s['backbones']} "
            f"| {s['ligand_types']} | {s['last_updated']} |\n"
        )
    lines.append("\n")
    lines.append(
        f"_Generated {_dt.datetime.now(_dt.timezone.utc):%Y-%m-%d %H:%M UTC}._\n"
    )
    index_out.write_text("".join(lines))


# =============================================================================
# CLI
# =============================================================================


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-master",
        description="Aggregate per-experiment rows.csv into experiments/MASTER.csv "
                    "and regenerate the index README.",
    )
    p.add_argument("--experiments-root", type=Path, default=EXPERIMENTS_ROOT,
                   help=f"root directory (default: {EXPERIMENTS_ROOT})")
    p.add_argument("--out", type=Path, default=None,
                   help="output MASTER.csv path (default: <experiments-root>/MASTER.csv)")
    p.add_argument("--index-out", type=Path, default=None,
                   help="output index path (default: <experiments-root>/INDEX.md)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    experiments_root = args.experiments_root
    out = args.out or (experiments_root / "MASTER.csv")
    index_out = args.index_out or (experiments_root / "INDEX.md")

    rows_csvs = find_experiment_rows(experiments_root)
    cols, rows = concatenate_rows(rows_csvs, experiments_root)
    write_master(cols, rows, out)
    write_index(rows_csvs, index_out, experiments_root)

    print(f"aggregated {len(rows_csvs)} experiment(s), {len(rows)} row(s) → {out}")
    print(f"index → {index_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
