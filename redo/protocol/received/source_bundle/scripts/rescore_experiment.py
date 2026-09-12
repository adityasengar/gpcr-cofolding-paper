"""Refresh a per-experiment ``rows.csv`` from the current state of scratch.

Walks the experiment's scratch tree
(``<scratch-root>/<slug>/``) for fold-model output files (``.cif`` +
``.pdb``), builds an on-the-fly rescore manifest, invokes the batch
scorer, and merges the resulting rows.csv into
``experiments/<slug>/rows.csv``.

The scorer's Layer-4 sidecar lift-in stamps ``pre_check_status`` and
Exp-Layer-1's ``seed_used`` / ``ligand_*`` on every row automatically
via ``_lift_provenance_from_sidecar``. This script additionally runs
the Exp-Layer-2 analysis-time enricher over the emitted rows.csv to
fill the four partner columns and any ligand fields the scorer's
sidecar-lift missed.

Idempotent: hashes the sorted list of ``(path, size, mtime)`` for the
scratch tree and stores the digest at ``rows.csv.sha256`` next to the
per-experiment CSV. Re-runs against unchanged scratch state are a
no-op ("no new predictions; skipping").

Usage:

    scripts/rescore_experiment.py --slug aa2ar_gs_bimodality_confirm

    scripts/rescore_experiment.py --slug X --dry-run       # list only
    scripts/rescore_experiment.py --slug X --fake-scorer    # write empty rows.csv
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parent.parent
EXPERIMENTS_ROOT = REPO / "experiments"
DEFAULT_SCRATCH_ROOT = Path("/hpc/scratch/sengaad1/paper_af3/experiments")
DEFAULT_REF_SET_CSV = REPO / "refs" / "reference_set.csv"


# ---------------------------------------------------------------------
# Rows path resolution (canonical NEW shape vs grandfathered flat shape)
# ---------------------------------------------------------------------

def resolve_rows_csv_path(exp_dir: Path) -> Path:
    """Return the canonical rows.csv path for this experiment.

    Canonical (new shape, per 000_template): ``<exp_dir>/analysis/rows.csv``.
    Grandfathered (pre-2026-09-01 experiments like
    ``013_mn_consensus_aa2ar_gs_neca_5_5``): ``<exp_dir>/rows.csv``.

    Rule: if ``<exp_dir>/analysis/`` exists, use the new path. Otherwise
    fall back to the flat legacy path. Keeps the reorg backward-compatible
    without touching grandfathered folders.
    """
    if (exp_dir / "analysis").is_dir():
        return exp_dir / "analysis" / "rows.csv"
    return exp_dir / "rows.csv"


def resolve_sha_marker_path(exp_dir: Path) -> Path:
    if (exp_dir / "analysis").is_dir():
        return exp_dir / "analysis" / "rows.csv.sha256"
    return exp_dir / "rows.csv.sha256"


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head_of(path: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "log", "-n", "1", "--pretty=%H", "--", str(path.resolve())],
            capture_output=True, text=True, check=True, cwd=str(REPO),
        )
        return r.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _write_rows_provenance(
    exp_dir: Path,
    rows_csv: Path,
    ref_set: Path,
    manifest_path: Path | None,
    tree_sha: str,
    n_predictions: int,
) -> Path:
    """Emit ``analysis/rows.provenance.json`` (or flat) alongside rows.csv.

    Records SHA256 of every scorer input this rescore depended on:
    - scorer/*.py (5 core files) — audit trail #11 countermeasure.
    - refs/thresholds_panel.csv — active-vs-inactive gates.
    - refs/reference_set.csv — per-receptor reference distances.
    - manifest.csv (if manifest-mode) — cell layout.
    """
    prov_path = rows_csv.parent / "rows.provenance.json"
    scorer_files = (
        "scorer/orchestrator.py",
        "scorer/schema.py",
        "scorer/structure.py",
        "scorer/cli.py",
        "scorer/assertions.py",
    )
    scorer_shas = {f: _sha256(REPO / f) for f in scorer_files}
    prov = {
        "scorer_shas": scorer_shas,
        "scorer_git_head": _git_head_of(REPO / "scorer"),
        "thresholds_panel_csv_sha256": _sha256(REPO / "refs" / "thresholds_panel.csv"),
        "reference_set_csv_sha256": _sha256(ref_set),
        "manifest_csv_sha256": _sha256(manifest_path) if manifest_path else None,
        "manifest_path": str(manifest_path.resolve()) if manifest_path else None,
        "rows_csv_sha256": _sha256(rows_csv),
        "scratch_tree_sha256": tree_sha,
        "n_predictions_scored": n_predictions,
        "rescored_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
    }
    prov_path.write_text(json.dumps(prov, indent=2) + "\n")
    return prov_path


# =============================================================================
# Scratch walk
# =============================================================================


_PREDICTION_EXTS = (".cif", ".pdb")

# Directories to skip — they hold model intermediates rather than fold outputs
_SKIP_DIRS = frozenset({
    "processed", "msa", "msas", "lightning_logs", "template_cache",
    "_input_rewrites", "checkpoints",
})


def iter_predictions(scratch_root: Path) -> Iterable[Path]:
    """Yield every ``.cif`` / ``.pdb`` under scratch_root, skipping known
    non-prediction directories.

    Ordered lexicographically for deterministic manifests.
    """
    if not scratch_root.exists():
        return
    for p in sorted(scratch_root.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in _PREDICTION_EXTS:
            continue
        # Skip files inside processed/ msa/ etc. — walk any depth
        if any(part in _SKIP_DIRS for part in p.parts):
            continue
        yield p


def hash_scratch_tree(paths: list[Path]) -> str:
    """SHA-256 of a stable "path + size + mtime" summary of the tree.

    Catches new files (path list grows), deleted files (list shrinks),
    and modified files (mtime + size change). Uses stat rather than
    content-hashing because prediction files can be 10–100 MB each and
    a content hash on the full tree would defeat the "safe to run 20
    times" idempotency goal.
    """
    h = hashlib.sha256()
    for p in paths:
        try:
            st = p.stat()
        except OSError:
            continue
        h.update(f"{p}|{st.st_size}|{int(st.st_mtime)}\n".encode("utf-8"))
    return h.hexdigest()


# =============================================================================
# Spec loading
# =============================================================================


def load_spec(exp_dir: Path) -> dict[str, Any]:
    spec_path = exp_dir / "spec.yaml"
    if not spec_path.exists():
        raise FileNotFoundError(
            f"no spec.yaml under {exp_dir}; run spawn_experiment first"
        )
    import yaml as _yaml
    return _yaml.safe_load(spec_path.read_text()) or {}


# =============================================================================
# Manifest mode — multi-cell experiments (Block A shape)
# =============================================================================
#
# Some experiments (Block A, `018_block_a_switch_test`) span many cells and
# don't have a single per-experiment ``spec.yaml`` — each cell has its own
# (receptor × arm × backbone) tuple. In that shape the manifest CSV
# (``experiments/<slug>/runs/<run>/manifest.csv``) IS the source of truth for
# what to rescore.
#
# In ``--manifest`` mode:
#   - Top-level ``spec.yaml`` lookup is skipped.
#   - For every prediction file found on scratch, the enclosing cell is
#     inferred from the path (the second path segment under scratch_root/slug
#     is the cell name, matching the manifest's ``experiment_slug`` column).
#   - Receptor / state_claim / species come from the cell's manifest rows —
#     all rows in a single cell share these values (one cell = one
#     receptor × one arm × one backbone).
#   - Top-level ligand FASTA regen is skipped (per-cell, not per-experiment).


def _index_manifest_by_cell(manifest_path: Path) -> dict[str, dict[str, str]]:
    """Map cell slug (=manifest ``experiment_slug`` column) → cell metadata.

    Each cell contributes one entry with the fields the scorer needs:
    ``receptor_slug``, ``state_claim``, ``input_species``, plus ``backbone``
    for diagnostics. Manifest rows within a cell share these fields by
    construction (one cell = one receptor × one arm × one backbone).
    """
    cells: dict[str, dict[str, str]] = {}
    with manifest_path.open() as f:
        for row in csv.DictReader(f):
            cell = (row.get("experiment_slug") or "").strip()
            if not cell:
                continue
            if cell in cells:
                continue
            receptor = (
                (row.get("receptor_resolved") or "").strip()
                or (row.get("receptor_from_path_substring") or "").strip()
            )
            cells[cell] = {
                "receptor_slug": receptor.upper(),
                "state_claim": (row.get("state_claim") or "").strip() or "Ga-coupled-active",
                "input_species": (row.get("species") or "").strip() or "human",
                "backbone": (row.get("backbone") or "").strip(),
            }
    return cells


def _infer_cell_from_path(pred_path: Path, scratch_slug_root: Path) -> str | None:
    """Return the cell slug for a prediction path under ``<scratch>/<slug>/``.

    Expected layout: ``<scratch>/<slug>/<cell>/<hash>/<backbone>/seed_.../*.cif``.
    The first path segment below ``scratch_slug_root`` is the cell.
    """
    try:
        rel = pred_path.resolve().relative_to(scratch_slug_root.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    return parts[0]


def _build_manifest_mode_rescore_rows(
    paths: list[Path],
    scratch_slug_root: Path,
    cells: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], list[Path]]:
    """Build rescore manifest rows in ``--manifest`` mode.

    Returns (rescore_rows, retained_paths). Any prediction file whose
    enclosing cell isn't in the manifest is dropped; the retained_paths
    parallel list is the subset actually queued for scoring.
    """
    rescore_rows: list[dict[str, str]] = []
    retained_paths: list[Path] = []
    unknown_cells: set[str] = set()
    for p in paths:
        cell = _infer_cell_from_path(p, scratch_slug_root)
        if cell is None or cell not in cells:
            if cell is not None:
                unknown_cells.add(cell)
            continue
        meta = cells[cell]
        rescore_rows.append({
            "prediction_path": str(p),
            "receptor_slug": meta["receptor_slug"],
            "state_claim": meta["state_claim"],
            "input_species": meta["input_species"],
        })
        retained_paths.append(p)
    if unknown_cells:
        print(
            f"[manifest-mode] warning: {len(unknown_cells)} cell(s) on scratch "
            f"not in manifest: {sorted(unknown_cells)[:5]}"
            f"{'...' if len(unknown_cells) > 5 else ''}",
            file=sys.stderr,
        )
    return rescore_rows, retained_paths


def _canonicalise_receptor_slug(spec: dict[str, Any]) -> str:
    """Same normalisation as gpcr-propose — receptor slug uppercase."""
    from scorer.propose import _canonicalise_receptor
    return _canonicalise_receptor(spec.get("receptor", ""))


# =============================================================================
# Manifest builder
# =============================================================================


_MANIFEST_COLUMNS = ("prediction_path", "receptor_slug", "state_claim", "input_species")


def build_rescore_manifest(paths: list[Path], spec: dict[str, Any]) -> list[dict[str, str]]:
    """One manifest row per prediction file. Every row has the same
    (receptor, state_claim, species) — those come from spec.yaml."""
    receptor = _canonicalise_receptor_slug(spec)
    state = spec.get("state_claim", "Ga-coupled-active")
    species = spec.get("species", "human")
    return [
        {
            "prediction_path": str(p),
            "receptor_slug": receptor,
            "state_claim": state,
            "input_species": species,
        }
        for p in paths
    ]


# =============================================================================
# Scorer invocation
# =============================================================================


def _write_manifest(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(_MANIFEST_COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _run_batch_scorer(manifest: Path, out_dir: Path, ref_set: Path,
                      cache_dir: Path | None = None) -> Path:
    """Invoke scorer.cli.batch_main and return the emitted rows.csv path."""
    from scorer.cli import batch_main
    argv = [
        "--manifest", str(manifest),
        "--out", str(out_dir),
        "--ref-set", str(ref_set),
    ]
    if cache_dir is not None:
        argv += ["--cache-dir", str(cache_dir)]
    rc = batch_main(argv)
    if rc != 0:
        raise RuntimeError(f"scorer.cli.batch_main exited {rc}")
    return out_dir / "rows.csv"


def _run_enricher(rows_csv: Path, predictions_csv: Path, out_csv: Path) -> dict[str, Any]:
    """Invoke the Exp-Layer 2 enricher inline.

    Falls back gracefully if predictions_csv doesn't exist (fresh
    proposal-only experiments have no EXPERIMENT_CATALOG row) — writes
    the input rows.csv verbatim to out_csv.
    """
    if not predictions_csv.exists():
        # Skip enrichment; rows already carry seed_used + ligand_* from
        # sidecar lift-in during scoring.
        shutil.copy(rows_csv, out_csv)
        return {"enricher_skipped": "no predictions.csv"}
    import sys as _sys
    if str(REPO) not in _sys.path:
        _sys.path.insert(0, str(REPO))
    from scripts.enrich_partner_metadata import enrich
    return enrich(rows_csv=rows_csv, predictions_csv=predictions_csv,
                  out_csv=out_csv)


# =============================================================================
# Ligand FASTA regen
# =============================================================================


def regenerate_ligand_fasta(exp_dir: Path, spec: dict[str, Any]) -> None:
    """Write ``experiments/<slug>/ligand_sequence.fasta`` from the spec's
    ligand block. Empty file if the spec has no peptide ligand.
    """
    fasta_path = exp_dir / "ligand_sequence.fasta"
    ligand = spec.get("ligand") or {}
    if not isinstance(ligand, dict):
        fasta_path.write_text("")
        return
    if ligand.get("type") != "peptide":
        fasta_path.write_text("")
        return
    seq = (ligand.get("sequence") or "").strip()
    if not seq:
        fasta_path.write_text("")
        return
    slug = exp_dir.name
    fasta_path.write_text(f">ligand_{slug}\n{seq}\n")


# =============================================================================
# Main rescore
# =============================================================================


def rescore(
    slug: str,
    experiments_root: Path = EXPERIMENTS_ROOT,
    scratch_root: Path = DEFAULT_SCRATCH_ROOT,
    ref_set: Path = DEFAULT_REF_SET_CSV,
    predictions_csv: Path | None = None,
    dry_run: bool = False,
    fake_scorer: bool = False,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Refresh the per-experiment rows.csv. Returns a summary dict.

    Two modes:

    - **spec.yaml mode (default)**: the experiment has one per-experiment
      ``spec.yaml`` (single receptor × arm × backbone). Receptor / state /
      species come from it, and one rescore-manifest row is emitted per
      prediction file found on scratch.
    - **manifest mode** (``manifest_path`` set): the experiment is
      multi-cell (Block A shape) — one manifest row per (backbone × receptor
      × arm × seed_index). Top-level ``spec.yaml`` is skipped; per-cell
      receptor / state / species are read from the manifest and applied to
      every prediction file whose enclosing cell matches a manifest row.
    """
    exp_dir = experiments_root / slug
    if not exp_dir.exists():
        raise FileNotFoundError(
            f"experiment folder {exp_dir} does not exist; run spawn_experiment first"
        )

    manifest_mode = manifest_path is not None
    spec: dict[str, Any] = {}
    if not manifest_mode:
        spec = load_spec(exp_dir)

    scratch_exp = scratch_root / slug
    paths = list(iter_predictions(scratch_exp))

    cells_by_slug: dict[str, dict[str, str]] = {}
    if manifest_mode:
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest not found: {manifest_path}")
        cells_by_slug = _index_manifest_by_cell(manifest_path)
        if not cells_by_slug:
            raise RuntimeError(
                f"manifest {manifest_path} yielded no cells (empty or wrong shape)"
            )

    tree_sha = hash_scratch_tree(paths)

    # Canonical (new shape, 000_template): analysis/rows.csv
    # Grandfathered (013_mn_consensus_..., etc.): rows.csv at top level.
    final_rows_csv = resolve_rows_csv_path(exp_dir)
    final_rows_csv.parent.mkdir(parents=True, exist_ok=True)
    sha_marker = resolve_sha_marker_path(exp_dir)
    prior_sha = sha_marker.read_text().strip() if sha_marker.exists() else ""

    if dry_run:
        print(f"[dry-run] would rescore {len(paths)} prediction(s) under {scratch_exp}")
        for p in paths[:10]:
            print(f"  {p}")
        if len(paths) > 10:
            print(f"  ... and {len(paths) - 10} more")
        return {"n_predictions": len(paths), "dry_run": True, "tree_sha": tree_sha}

    if paths and tree_sha == prior_sha:
        print(f"scratch tree unchanged (sha {tree_sha[:12]}); skipping rescore")
        return {"n_predictions": len(paths), "skipped": True, "tree_sha": tree_sha}

    if not paths:
        # No predictions on scratch yet — write an empty rows.csv marker
        # so downstream tools (MASTER builder) see the folder without
        # tripping on a missing file.
        if not final_rows_csv.exists():
            final_rows_csv.write_text("")   # empty file; MASTER walks over cleanly
        sha_marker.write_text(tree_sha)
        if not manifest_mode:
            regenerate_ligand_fasta(exp_dir, spec)
        return {"n_predictions": 0, "wrote_empty": True, "tree_sha": tree_sha,
                "rows_csv": str(final_rows_csv)}

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        manifest = tmp_dir / "manifest.csv"

        if manifest_mode:
            rescore_rows, retained_paths = _build_manifest_mode_rescore_rows(
                paths, scratch_exp, cells_by_slug
            )
        else:
            rescore_rows = build_rescore_manifest(paths, spec)
            retained_paths = paths

        if not rescore_rows:
            raise RuntimeError(
                "no prediction files matched a manifest cell; check "
                "scratch layout vs manifest 'experiment_slug' column"
            )
        _write_manifest(rescore_rows, manifest)

        if fake_scorer:
            # Test-only: emit a stub rows.csv with prediction_path per row
            # and no scoring. Skips network + gemmi + the whole scorer.
            stub_rows = final_rows_csv
            with stub_rows.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["prediction_path", "receptor_slug",
                                                  "state_claim", "input_species",
                                                  "passed"])
                w.writeheader()
                for row in rescore_rows:
                    row = dict(row)
                    row["passed"] = "True"
                    w.writerow(row)
            summary: dict[str, Any] = {"n_predictions": len(retained_paths),
                                       "fake_scorer": True,
                                       "tree_sha": tree_sha,
                                       "rows_csv": str(stub_rows)}
        else:
            out_dir = tmp_dir / "batch_out"
            scored_rows_csv = _run_batch_scorer(manifest, out_dir, ref_set)
            pred_csv = predictions_csv or (
                REPO / "docs" / "EXPERIMENT_CATALOG" / "data" / "predictions.csv"
            )
            enricher_summary = _run_enricher(
                rows_csv=scored_rows_csv,
                predictions_csv=pred_csv,
                out_csv=final_rows_csv,
            )
            # Emit rows.provenance.json alongside rows.csv — audit trail
            # #11 countermeasure at the analysis surface.
            prov_path = _write_rows_provenance(
                exp_dir=exp_dir,
                rows_csv=final_rows_csv,
                ref_set=ref_set,
                manifest_path=manifest_path if manifest_mode else None,
                tree_sha=tree_sha,
                n_predictions=len(retained_paths),
            )
            summary = {
                "n_predictions": len(retained_paths),
                "n_scratch_predictions": len(paths),
                "n_cells": len(cells_by_slug) if manifest_mode else 1,
                "manifest_mode": manifest_mode,
                "tree_sha": tree_sha,
                "rows_csv": str(final_rows_csv),
                "rows_provenance_json": str(prov_path),
                "enricher": enricher_summary,
            }

    sha_marker.write_text(tree_sha)
    if not manifest_mode:
        regenerate_ligand_fasta(exp_dir, spec)
    return summary


# =============================================================================
# CLI
# =============================================================================


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-rescore-experiment",
        description="Refresh a per-experiment rows.csv from the current scratch state.",
    )
    p.add_argument("--slug", required=True, help="the experiment slug")
    p.add_argument("--experiments-root", type=Path, default=EXPERIMENTS_ROOT,
                   help=f"root directory for experiments (default: {EXPERIMENTS_ROOT})")
    p.add_argument("--scratch-root", type=Path, default=DEFAULT_SCRATCH_ROOT,
                   help=f"HPC scratch root (default: {DEFAULT_SCRATCH_ROOT})")
    p.add_argument("--ref-set", type=Path, default=DEFAULT_REF_SET_CSV,
                   help=f"reference_set.csv path (default: {DEFAULT_REF_SET_CSV})")
    p.add_argument("--dry-run", action="store_true",
                   help="walk scratch and list; do not score")
    p.add_argument("--fake-scorer", action="store_true",
                   help="test-only: skip the real scorer and emit a stub rows.csv "
                        "with one row per prediction path")
    p.add_argument("--manifest", type=Path, default=None,
                   help="path to a per-experiment manifest CSV. When set, "
                        "top-level spec.yaml lookup is bypassed and per-cell "
                        "(receptor, state_claim, species) metadata is read "
                        "from the manifest. Used for multi-cell experiments "
                        "(Block A shape).")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        summary = rescore(
            slug=args.slug,
            experiments_root=args.experiments_root,
            scratch_root=args.scratch_root,
            ref_set=args.ref_set,
            dry_run=args.dry_run,
            fake_scorer=args.fake_scorer,
            manifest_path=args.manifest,
        )
    except (FileNotFoundError, RuntimeError) as e:
        print(f"gpcr-rescore-experiment: {e}", file=sys.stderr)
        return 2

    import json as _json
    print(_json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
