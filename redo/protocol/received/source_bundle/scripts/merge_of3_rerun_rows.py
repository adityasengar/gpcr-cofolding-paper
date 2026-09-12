"""Merge the 2026-09-02 OF3 seed-fix rerun rows into the primary Block A
rows.csv, replacing the pre-fix (all-seeded-2746317213) OF3 rows.

Inputs:
  --original    experiments/018_block_a_switch_test/analysis/rows.csv
                (the primary Block A rows.csv — has boltz/chai/of3/protenix
                rows from the pre-fix campaign; OF3 rows here are the
                seed-buggy ones).
  --rerun       experiments/018_block_a_switch_test_of3_rerun_2026_09_02/
                analysis/rows.csv (freshly-scored OF3-only rows from the
                post-fix re-run).

Output:
  --out         experiments/018_block_a_switch_test/analysis/rows.merged.csv
                Original rows minus OF3 rows plus the rerun OF3 rows.

Rows are matched on input path shape — a rerun row's ``input_path`` shares
the same cell name (``018_block_a_switch_test_<receptor>_<arm>_of3``) as the
original. We drop every original row where the cell name matches an OF3
cell and stitch the rerun rows in their place.

Prints per-backbone × per-arm row counts before and after the merge as a
sanity check.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path


OF3_CELL_RE = re.compile(r"018_block_a_switch_test_[a-z0-9]+_(?:apo|cognate)_of3")


def _cell_name(path: str) -> str | None:
    for tok in path.split("/"):
        if OF3_CELL_RE.match(tok):
            return tok
    return None


def _backbone_from_path(p: str) -> str:
    pl = p.lower()
    if "/of3/" in pl or "_of3_" in pl:
        return "of3"
    if "/boltz/" in pl:
        return "boltz"
    if "/chai/" in pl:
        return "chai"
    if "/protenix/" in pl:
        return "protenix"
    return "?"


def _arm(p: str) -> str:
    pl = p.lower()
    if "_apo_" in pl:
        return "apo"
    if "_cognate_" in pl:
        return "cognate"
    return "?"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--original", required=True, type=Path,
                    help="primary Block A rows.csv")
    ap.add_argument("--rerun", required=True, type=Path,
                    help="OF3 rerun rows.csv")
    ap.add_argument("--out", required=True, type=Path,
                    help="output merged rows.csv")
    args = ap.parse_args(argv)

    with args.original.open() as f:
        original_rows = list(csv.DictReader(f))
    with args.rerun.open() as f:
        rerun_rows = list(csv.DictReader(f))

    print(f"original rows: {len(original_rows)}", file=sys.stderr)
    print(f"rerun rows:    {len(rerun_rows)}", file=sys.stderr)

    # Pre-merge counts
    before = Counter()
    for r in original_rows:
        p = r.get("input_path", "")
        before[(_backbone_from_path(p), _arm(r.get("input_path", "")))] += 1
    print("\npre-merge per (backbone × arm):", file=sys.stderr)
    for k in sorted(before):
        print(f"  {k[0]:10s} {k[1]:8s} {before[k]}", file=sys.stderr)

    # Drop OF3 rows from the original (they'll be replaced by rerun rows)
    kept_original = [r for r in original_rows
                     if _backbone_from_path(r.get("input_path", "")) != "of3"]
    print(f"\ndropped {len(original_rows) - len(kept_original)} OF3 rows from original",
          file=sys.stderr)

    # Align columns — the rerun rows have the same schema as original,
    # but they were scored against a possibly-different reference_set
    # (post §1(b) tilt merge). Use the original's column order; drop
    # any rerun-only columns; fill missing rerun columns with "".
    fieldnames = list(original_rows[0].keys()) if original_rows else list(rerun_rows[0].keys())
    aligned_rerun = []
    rerun_fields = set(rerun_rows[0].keys()) if rerun_rows else set()
    missing_in_rerun = [f for f in fieldnames if f not in rerun_fields]
    extra_in_rerun = [f for f in rerun_fields if f not in fieldnames]
    if missing_in_rerun:
        print(f"columns in original but not rerun: {missing_in_rerun}", file=sys.stderr)
    if extra_in_rerun:
        print(f"columns in rerun but not original (dropped): {extra_in_rerun}",
              file=sys.stderr)
    for r in rerun_rows:
        aligned_rerun.append({k: r.get(k, "") for k in fieldnames})

    merged = kept_original + aligned_rerun
    print(f"\nmerged rows: {len(merged)}", file=sys.stderr)

    # Post-merge counts
    after = Counter()
    for r in merged:
        p = r.get("input_path", "")
        after[(_backbone_from_path(p), _arm(p))] += 1
    print("post-merge per (backbone × arm):", file=sys.stderr)
    for k in sorted(after):
        print(f"  {k[0]:10s} {k[1]:8s} {after[k]}", file=sys.stderr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in merged:
            w.writerow(r)
    print(f"\nwrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
