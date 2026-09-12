"""Merge Class B/F discovery outputs into the main Block A panel.

Runs AFTER agent a319017d completes and lands:
- refs/gpcr_coupling_class_bf.csv  (Class B/F receptors + cognate Gα)
- refs/reference_set_class_bf.csv  (paired active/inactive references)
- refs/anchors_per_class.csv       (per-class anchor pairs)

This script proposes a merge into the main panel files WITHOUT
destructive changes — writes proposed_gpcr_coupling.csv and
proposed_reference_set.csv side by side so a human reviews the merge
before it lands in refs/.

Usage:
    python3 scripts/merge_class_bf_into_panel.py --dry-run   # print merge summary
    python3 scripts/merge_class_bf_into_panel.py --emit      # write proposed_*.csv
    python3 scripts/merge_class_bf_into_panel.py --commit    # replace refs/ files (destructive)
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUPLING = REPO / "refs/gpcr_coupling.csv"
COUPLING_BF = REPO / "refs/gpcr_coupling_class_bf.csv"
REFSET = REPO / "refs/reference_set.csv"
REFSET_BF = REPO / "refs/reference_set_class_bf.csv"


def load_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open() as f:
        rdr = csv.DictReader(f)
        return list(rdr.fieldnames or []), list(rdr)


def merge_coupling(dry_run: bool) -> dict:
    """Merge Class B/F rows into gpcr_coupling.csv. New rows get a
    `panel_extension_source = "class_bf_step5"` column marker."""
    if not COUPLING_BF.exists():
        return {"error": f"missing {COUPLING_BF}"}

    a_cols, a_rows = load_rows(COUPLING)
    b_cols, b_rows = load_rows(COUPLING_BF)

    # Union of columns; preserve original order for the primary file
    merged_cols = list(a_cols)
    for c in b_cols:
        if c not in merged_cols:
            merged_cols.append(c)
    if "panel_extension_source" not in merged_cols:
        merged_cols.append("panel_extension_source")

    a_slugs = {r["receptor_slug"] for r in a_rows}

    duplicates = [r for r in b_rows if r["receptor_slug"] in a_slugs]
    new_rows = [r for r in b_rows if r["receptor_slug"] not in a_slugs]
    for r in new_rows:
        r.setdefault("panel_extension_source", "class_bf_step5")

    proposed = REPO / "refs/proposed_gpcr_coupling.csv"
    if not dry_run:
        with proposed.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=merged_cols, extrasaction="ignore")
            w.writeheader()
            for r in a_rows:
                r = dict(r)
                r.setdefault("panel_extension_source", "class_a_original")
                w.writerow(r)
            w.writerows(new_rows)
    return {
        "a_count": len(a_rows),
        "b_count": len(b_rows),
        "duplicates": [r["receptor_slug"] for r in duplicates],
        "new_receptors": [r["receptor_slug"] for r in new_rows],
        "proposed_path": str(proposed),
        "merged_col_count": len(merged_cols),
    }


def merge_refset(dry_run: bool) -> dict:
    """Merge Class B/F reference-set rows in."""
    if not REFSET_BF.exists():
        return {"error": f"missing {REFSET_BF}"}

    a_cols, a_rows = load_rows(REFSET)
    b_cols, b_rows = load_rows(REFSET_BF)

    merged_cols = list(a_cols)
    for c in b_cols:
        if c not in merged_cols:
            merged_cols.append(c)

    # De-dup on (receptor_slug, role, pdb_id)
    a_keys = {(r["receptor_slug"], r["role"], r["pdb_id"]) for r in a_rows}
    duplicates = [r for r in b_rows
                  if (r["receptor_slug"], r["role"], r["pdb_id"]) in a_keys]
    new_rows = [r for r in b_rows
                if (r["receptor_slug"], r["role"], r["pdb_id"]) not in a_keys]

    proposed = REPO / "refs/proposed_reference_set.csv"
    if not dry_run:
        with proposed.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=merged_cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(a_rows)
            w.writerows(new_rows)
    return {
        "a_count": len(a_rows),
        "b_count": len(b_rows),
        "duplicates": [(r["receptor_slug"], r["role"], r["pdb_id"]) for r in duplicates],
        "new_rows": len(new_rows),
        "proposed_path": str(proposed),
    }


def replace_originals() -> None:
    """Only called after human approves the merge. Replaces refs/
    files with the proposed_* versions. Keeps a .backup."""
    for name in ("gpcr_coupling.csv", "reference_set.csv"):
        orig = REPO / f"refs/{name}"
        proposed = REPO / f"refs/proposed_{name}"
        if not proposed.exists():
            print(f"skipping {name} — no proposed_ file")
            continue
        shutil.copy2(orig, orig.with_suffix(".csv.backup"))
        shutil.move(str(proposed), str(orig))
        print(f"replaced {orig} (backup at {orig}.backup)")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--emit", action="store_true")
    p.add_argument("--commit", action="store_true")
    args = p.parse_args()

    if not any([args.dry_run, args.emit, args.commit]):
        args.dry_run = True

    if args.commit:
        replace_originals()
        return 0

    print("=== merging gpcr_coupling ===")
    cop = merge_coupling(dry_run=args.dry_run)
    for k, v in cop.items():
        print(f"  {k}: {v}")
    print()
    print("=== merging reference_set ===")
    ref = merge_refset(dry_run=args.dry_run)
    for k, v in ref.items():
        print(f"  {k}: {v}")

    if args.emit:
        print()
        print("Wrote proposed_gpcr_coupling.csv + proposed_reference_set.csv.")
        print("Review the diffs; when satisfied, run with --commit to replace originals.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
