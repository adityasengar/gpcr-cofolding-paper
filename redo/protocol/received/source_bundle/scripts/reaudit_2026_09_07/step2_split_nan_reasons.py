#!/usr/bin/env python3
"""Step 2 — split NaN_empty into its 5 constituent exit reasons.

`t7b_pose_accuracy.py` collapsed every NaN into one "NaN_empty" bucket. But
the scorer's `ligand_rmsd_to_ref` has SIX distinct exit reasons that produce
NaN + method="":

  - apo_no_ligand              (state_claim == APO)
  - ligand_type_{apo,none,''}  (ligand_type is empty / none / apo)
  - no_alignment_transform     (ref_transform is None — usually Kabsch failed)
  - no_ref_ligand              (reference cache had zero ligand atoms) ← Bug-#2-relevant
  - no_pred_ligand             (prediction had zero HETATM ligand atoms)
  - empty_struct               (prediction CIF has no atoms at all)

Plus:
  - mcs_too_small              (MCS < 5 atoms — flagged with method="mcs_too_small")
  - rdkit_unavailable          (RDKit import failed at runtime)
  - parse_failure              (one side failed to build RDKit Mol)

All of these live in `pocket_notes` as prefix strings like `lig:apo_no_ligand`
or `lig:no_ref_ligand`. Parse them out per row without a rescore.

Outputs a per-(backbone × arm × ligand_role) census with all 9 reasons split.
"""
from __future__ import annotations
import csv, re
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path("/Users/SENGAAD1/Documents/claude/paper_af3")
ROWS_FIX = REPO / "experiments/021_block_c_tier3_pharmacology/rescore_t7b_fix/rows.csv"
ROWS_V2 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/nan_reason_census.csv"

# Reason patterns to extract from `pocket_notes`.
# Format: pocket_notes contains ";"-joined tokens; the ligand's exit reason
# is prefixed with "lig:".
LIG_REASON_RE = re.compile(r"lig:([a-z0-9_]+)")


def extract_reason(notes: str, method: str) -> str:
    if not notes:
        return method or "unknown"
    m = LIG_REASON_RE.search(notes)
    if m:
        return m.group(1)
    return method or "empty"


def is_nan(s: str) -> bool:
    return s in ("", "nan", "NaN", "None")


def main() -> int:
    manifest = {r["prediction_path"]: r for r in csv.DictReader(MANIFEST.open())}

    def parse_rows(path: Path, tag: str):
        rows = []
        for r in csv.DictReader(path.open()):
            ip = r.get("input_path", "")
            m = manifest.get(ip)
            if not m:
                continue
            bb = m["backbone"].lower()
            arm = "apo" if m["partner_type"] == "apo" else "cognate"
            role = m["ligand_role"]
            recep = r.get("receptor_slug", "").upper()
            method = r.get("pocket_ligand_atom_map_method", "")
            lrmsd = r.get("ligand_rmsd_to_ref", "")
            notes = r.get("pocket_notes", "")

            if is_nan(lrmsd):
                reason = extract_reason(notes, method)
                if not reason:
                    reason = "unknown_nan"
            else:
                # Numeric — bucket by method
                if method == "atom_name_element":
                    reason = "fast_path_ok"
                elif method == "mcs":
                    reason = "mcs_ok"
                elif method == "":
                    reason = "numeric_no_method"  # v2 pre-MCS rows
                else:
                    reason = f"other:{method}"
            rows.append({
                "corpus": tag,
                "backbone": bb, "arm": arm, "ligand_role": role,
                "receptor": recep, "reason": reason, "method": method,
                "input_path": ip,
            })
        return rows

    print("[step2] parsing rescore_t7b_fix (Boltz+Chai post-fix)...")
    fix_rows = parse_rows(ROWS_FIX, "t7b_fix")
    print(f"        {len(fix_rows)} rows")

    print("[step2] parsing rows.tier3.v2 (OF3+Protenix + pre-MCS Boltz+Chai)...")
    v2_rows = parse_rows(ROWS_V2, "v2")
    print(f"        {len(v2_rows)} rows")

    # Build the v3-merged view: use t7b_fix for Boltz+Chai, v2 for OF3+Protenix.
    v3 = []
    for r in fix_rows:
        v3.append(r)
    for r in v2_rows:
        if r["backbone"] in ("of3", "protenix"):
            v3.append(r)

    # Aggregate
    counts_by_cell = defaultdict(Counter)
    reason_totals = Counter()
    per_receptor = defaultdict(Counter)
    for r in v3:
        key = (r["backbone"], r["arm"], r["ligand_role"])
        counts_by_cell[key][r["reason"]] += 1
        reason_totals[r["reason"]] += 1
        per_receptor[r["receptor"]][r["reason"]] += 1

    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["backbone", "arm", "ligand_role", "reason", "n"])
        for (bb, arm, role), c in sorted(counts_by_cell.items()):
            for reason, n in sorted(c.items(), key=lambda x: -x[1]):
                w.writerow([bb, arm, role, reason, n])

    per_recep_out = OUT.parent / "nan_reason_census_by_receptor.csv"
    with per_recep_out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["receptor", "reason", "n"])
        for recep in sorted(per_receptor):
            for reason, n in sorted(per_receptor[recep].items(), key=lambda x: -x[1]):
                w.writerow([recep, reason, n])

    print()
    print(f"=== Reason totals (n={len(v3)} rows across v3 merged corpus) ===")
    for reason, n in reason_totals.most_common():
        pct = 100 * n / len(v3)
        print(f"  {reason:<30} {n:>6}  ({pct:5.1f}%)")

    print(f"\nwrote {OUT.relative_to(REPO)}")
    print(f"wrote {per_recep_out.relative_to(REPO)}")

    # Print per-backbone summary at the reason level
    print(f"\n=== Per (backbone × ligand_role) reason breakdown (compact) ===")
    print(f"{'backbone':<10} {'arm':<10} {'role':<22} {'fast':>6} {'mcs':>6} {'no_ref_lig':>10} {'no_pred_lig':>11} {'no_align':>9} {'mcs_small':>9} {'apo':>6} {'ligtype':>7} {'other':>6}")
    for (bb, arm, role), c in sorted(counts_by_cell.items()):
        fast = c.get("fast_path_ok", 0) + c.get("numeric_no_method", 0)
        mcs = c.get("mcs_ok", 0)
        no_ref = c.get("no_ref_ligand", 0)
        no_pred = c.get("no_pred_ligand", 0)
        no_align = c.get("no_alignment_transform", 0)
        mcs_small = c.get("mcs_too_small", 0)
        apo = c.get("apo_no_ligand", 0)
        ligtype = sum(v for k, v in c.items() if k.startswith("ligand_type"))
        other = sum(v for k, v in c.items()) - (fast + mcs + no_ref + no_pred + no_align + mcs_small + apo + ligtype)
        print(f"{bb:<10} {arm:<10} {role:<22} {fast:>6} {mcs:>6} {no_ref:>10} {no_pred:>11} {no_align:>9} {mcs_small:>9} {apo:>6} {ligtype:>7} {other:>6}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
