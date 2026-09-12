"""Verify the plan §2 OF3 seed-fix on the 3-receptor verification cell.

Reads every CIF under
``/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_seedfix_verification/{drd2,adrb2,hrh1}/of3/seed_<N>/``,
computes ``d_tm6_r350_r630_ca`` via the scorer, and reports:

  1. **No seed_2746317213 subdir** across the 3 cells — proves the seed
     patch landed in ``qsub/rerun_of3.sh``. Fail loud if seen.
  2. **Median max element-wise across-seed diff on d_tm6** > 0.3 Å.
     Within each cell, take each seed's sorted 5 sample values, compute
     the max element-wise difference across the 5 seed vectors, take
     the median over cells.

Also prints the per-seed sorted 5-value tuple for one cell (DRD2) so
the qualitative shape of the seed distribution is visible.

Usage
-----
    python3 scripts/verify_of3_seed_fix.py \\
        --verification-root /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_seedfix_verification

Runs on HPC (needs gemmi + scorer). Exits 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations

import argparse
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

BUGGY_SEED = "2746317213"
BUGGY_SEED_INT = 2746317213
D_TM6_ACCEPTANCE_A = 0.3


def _extract_d_tm6(cif_path: Path, entry_name: str, build_model, api,
                   _anchor_cache: dict[str, tuple[int | None, int | None]]) -> float:
    """Return d_tm6_r350_r630_ca for a single CIF, or NaN on failure.

    Skips the VerifiedModel construction (which requires A1-A6
    assertions) — we only need the CA-CA distance for two BW anchors,
    which is safe on unverified predictions here since the verification
    cell is diagnostic, not scoring.
    """
    try:
        model = build_model(str(cif_path), entry_name, api)
    except Exception as exc:
        print(f"WARN {cif_path.name}: {exc}", file=sys.stderr)
        return math.nan

    # BW anchor lookup — cached per-entry.
    if entry_name not in _anchor_cache:
        from scorer.anchors import resolve_anchors
        try:
            aset = resolve_anchors(api, entry_name)
            p350_anchor = aset.anchors.get("3.50")
            p630_anchor = aset.anchors.get("6.30")
            _anchor_cache[entry_name] = (
                p350_anchor.uniprot_pos if p350_anchor else None,
                p630_anchor.uniprot_pos if p630_anchor else None,
            )
        except Exception as exc:
            print(f"WARN anchor resolve failed for {entry_name}: {exc}",
                  file=sys.stderr)
            _anchor_cache[entry_name] = (None, None)

    p350, p630 = _anchor_cache[entry_name]
    if p350 is None or p630 is None:
        return math.nan

    r350 = model.residues.get(p350)
    r630 = model.residues.get(p630)
    if r350 is None or r630 is None:
        return math.nan
    ca350 = r350.find_atom("CA", "\0")
    ca630 = r630.find_atom("CA", "\0")
    if ca350 is None or ca630 is None:
        return math.nan
    return ca350.pos.dist(ca630.pos)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verification-root", required=True, type=Path)
    ap.add_argument("--receptors", nargs="+",
                    default=["drd2", "adrb2", "hrh1"],
                    help="lowercase receptor subdirectories")
    args = ap.parse_args(argv)

    from scorer.bw_numbering import Api
    from scorer.structure import build_uniprot_model
    from scorer.receptors import uniprot_slug

    repo_root = Path(__file__).resolve().parent.parent
    api = Api(repo_root / "refs" / "cache" / "gpcrdb")

    # Gate 1: no seed_2746317213 subdir anywhere.
    print("=== Gate 1: seed subdirectory scan ===")
    n_dirs = 0
    n_buggy = 0
    for rec in args.receptors:
        rec_dir = args.verification_root / rec / "of3"
        if not rec_dir.exists():
            print(f"WARN missing: {rec_dir}", file=sys.stderr)
            continue
        for seed_dir in rec_dir.rglob("seed_*"):
            if not seed_dir.is_dir():
                continue
            n_dirs += 1
            match = re.match(r"^seed_(\d+)$", seed_dir.name)
            if not match:
                continue
            seed_int = int(match.group(1))
            marker = " <-- BUGGY" if seed_int == BUGGY_SEED_INT else ""
            print(f"  {rec:8s} {seed_dir.relative_to(args.verification_root)}{marker}")
            if seed_int == BUGGY_SEED_INT:
                n_buggy += 1
    print(f"total seed subdirs: {n_dirs}, buggy (seed_{BUGGY_SEED}): {n_buggy}")
    if n_buggy > 0:
        print(f"FAIL: {n_buggy} seed subdir(s) still carry the buggy default seed.",
              file=sys.stderr)
        return 1

    # Gate 2: seed dispersion on d_tm6_r350_r630_ca.
    print("\n=== Gate 2: seed dispersion on d_tm6 ===")

    # Collect per (receptor, seed) -> sorted list of d_tm6 values.
    per_cell_seed_values: dict[str, dict[int, list[float]]] = defaultdict(dict)
    _anchor_cache: dict[str, tuple[int | None, int | None]] = {}

    for rec in args.receptors:
        entry_name = uniprot_slug(rec.upper())
        rec_dir = args.verification_root / rec / "of3"
        if not rec_dir.exists():
            continue
        # Walk seed subdirs, collect all CIFs per seed.
        for seed_dir in rec_dir.rglob("seed_*"):
            if not seed_dir.is_dir():
                continue
            match = re.match(r"^seed_(\d+)$", seed_dir.name)
            if not match:
                continue
            seed_int = int(match.group(1))
            values = []
            for cif in seed_dir.rglob("*.cif"):
                # Skip status sidecar / input files.
                if cif.name.startswith("_") or cif.name.endswith(".input.cif"):
                    continue
                v = _extract_d_tm6(cif, entry_name, build_uniprot_model, api,
                                   _anchor_cache)
                if not math.isnan(v):
                    values.append(v)
            if values:
                per_cell_seed_values[rec][seed_int] = sorted(values)

    if not per_cell_seed_values:
        print("FAIL: no d_tm6 values extracted.", file=sys.stderr)
        return 1

    # Print per-seed sorted 5-tuples for at least one cell.
    for rec in args.receptors:
        if rec not in per_cell_seed_values:
            continue
        print(f"\n--- {rec.upper()} per-seed sorted d_tm6 values ---")
        for seed in sorted(per_cell_seed_values[rec]):
            vals = per_cell_seed_values[rec][seed]
            print(f"  seed_{seed:12d}  " + "  ".join(f"{v:6.3f}" for v in vals))

    # Element-wise across-seed max diff, per receptor.
    max_diffs = []
    print("\n=== per-cell element-wise across-seed max diff ===")
    for rec in sorted(per_cell_seed_values):
        seeds = sorted(per_cell_seed_values[rec])
        if len(seeds) < 2:
            print(f"  {rec:8s} only {len(seeds)} seed(s), skipping")
            continue
        min_len = min(len(per_cell_seed_values[rec][s]) for s in seeds)
        if min_len == 0:
            continue
        # Compute per-element max - min across seeds.
        per_element_range = []
        for idx in range(min_len):
            elems = [per_cell_seed_values[rec][s][idx] for s in seeds]
            per_element_range.append(max(elems) - min(elems))
        max_diff = max(per_element_range)
        median_diff = statistics.median(per_element_range)
        max_diffs.append(max_diff)
        print(f"  {rec:8s} n_seeds={len(seeds)} n_samples/seed={min_len} "
              f"max_element_diff={max_diff:.3f} Å  median_element_diff={median_diff:.3f} Å")

    if not max_diffs:
        print("FAIL: no cells had >= 2 seeds.", file=sys.stderr)
        return 1

    median_max = statistics.median(max_diffs)
    print(f"\nmedian max element-wise across-seed diff across {len(max_diffs)} cells: "
          f"{median_max:.3f} Å")
    print(f"acceptance criterion: > {D_TM6_ACCEPTANCE_A} Å")

    if median_max > D_TM6_ACCEPTANCE_A:
        print(f"PASS: seed fix landed and sampler is seed-varying.")
        return 0
    else:
        print(f"FAIL: median max diff {median_max:.3f} Å <= {D_TM6_ACCEPTANCE_A} Å. "
              f"The sampler is still not seed-varying.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
