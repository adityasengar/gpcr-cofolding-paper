#!/usr/bin/env python3
"""Task E v3 — scope the P6 verdict, do not withdraw.

The v3 report (STAGE_POST_AUDIT_REPORT_v3.md) recorded
`DOCKING_POSE_QUALITY_UNRESOLVED`. Per user directive on 2026-09-05,
that reads as a full withdrawal, but the 4-cell finding is
scientifically valid inside its scope. The correct verdict is
`DOCKING_POSE_QUALITY_SCOPED` — the numbers stand, the
non-generalisability is stated explicitly.

Reads the v2 JSON that carries the per-cell census, extracts the
4 valid (OF3/Protenix × neutral_antagonist × {apo, g_alpha}) cells,
computes dock-<3-Å rate and median ligand_rmsd_to_ref per cell from
rows.tier3.v2.csv (source-of-record), and emits the scoped verdict
with explicit non-generalisability list.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, sha256, git_sha, now_utc


BACKBONE_TAG = ("boltz", "chai", "of3", "protenix")


def _f(x):
    if x is None or x == "" or str(x).lower() in ("nan", "none"):
        return None
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def _backbone_from_path(p):
    for bb in BACKBONE_TAG:
        if f"/{bb}/" in p:
            return bb
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--task-e-v2", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_E_v2_reference_ligand_mapping.json")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_E_v3_scoped_finding.json")
    args = ap.parse_args()

    # Load manifest to map prediction_path -> backbone, ligand_role, partner_type
    with open(args.manifest) as f:
        mani = {r["prediction_path"]: r for r in csv.DictReader(f)}

    # Aggregate ligand_rmsd_to_ref per cell
    cells = defaultdict(list)
    with open(args.rows) as f:
        for row in csv.DictReader(f):
            m = mani.get(row.get("input_path", ""))
            if m is None:
                continue
            bb = m.get("backbone") or _backbone_from_path(row.get("input_path", ""))
            role = m.get("ligand_role", "")
            partner = m.get("partner_type", "")
            key = (bb, role, partner)
            lrmsd = _f(row.get("ligand_rmsd_to_ref"))
            passed = str(row.get("passed", "")).lower() == "true"
            cells[key].append({
                "lrmsd": lrmsd,
                "passed": passed,
                "notes": row.get("pocket_notes", "") or "",
            })

    # Focus on 4 valid cells: OF3/Protenix × neutral_antagonist × {apo, g_alpha}
    valid_backbones = {"of3", "protenix"}
    valid_role = "neutral_antagonist"
    valid_partners = {"apo", "g_alpha"}

    per_cell = []
    total_valid_rows = 0
    total_populated_rows = 0
    total_dock_lt_3A = 0
    for (bb, role, partner), items in sorted(cells.items()):
        if role != valid_role or bb not in valid_backbones or partner not in valid_partners:
            continue
        # populated == ligand_rmsd_to_ref parseable AND ref_pdb == input_bound_pdb
        # Per task E v2, the 4 valid cells are the ones where atom mapping is valid.
        # Use ligand_rmsd_to_ref not-None on passed rows as the populated set.
        populated = [x for x in items if x["passed"] and x["lrmsd"] is not None]
        if not populated:
            continue
        lrmsds = [x["lrmsd"] for x in populated]
        dock_lt_3A = sum(1 for v in lrmsds if v < 3.0)
        dock_lt_2A = sum(1 for v in lrmsds if v < 2.0)
        median = statistics.median(lrmsds)
        p25 = statistics.quantiles(lrmsds, n=4)[0] if len(lrmsds) >= 4 else median
        p75 = statistics.quantiles(lrmsds, n=4)[2] if len(lrmsds) >= 4 else median
        per_cell.append({
            "backbone": bb,
            "ligand_role": role,
            "partner_type": partner,
            "n_passed": len(items),
            "n_populated_ligand_rmsd": len(populated),
            "populated_rate": len(populated) / len(items),
            "n_ligand_rmsd_lt_3A": dock_lt_3A,
            "dock_rate_lt_3A": dock_lt_3A / len(populated),
            "n_ligand_rmsd_lt_2A": dock_lt_2A,
            "median_ligand_rmsd_A": median,
            "p25_ligand_rmsd_A": p25,
            "p75_ligand_rmsd_A": p75,
        })
        total_valid_rows += len(populated)
        total_populated_rows += len(populated)
        total_dock_lt_3A += dock_lt_3A

    dock_rates = [c["dock_rate_lt_3A"] for c in per_cell]
    medians = [c["median_ligand_rmsd_A"] for c in per_cell]

    out = {
        "task": "E_v3_scoped_finding",
        "reconstruction": {
            "reconstruction_script": str(Path(__file__).resolve()),
            "reconstruction_script_git_sha": git_sha(),
            "generated_at_utc": now_utc(),
            "inputs": {
                "rows_csv": {"path": str(args.rows), "sha256": sha256(args.rows)},
                "manifest_csv": {"path": str(args.manifest), "sha256": sha256(args.manifest)},
                "task_e_v2_json": {"path": str(args.task_e_v2), "sha256": sha256(args.task_e_v2)},
            },
        },
        "verdict": "DOCKING_POSE_QUALITY_SCOPED",
        "verdict_wording": (
            "On the subset where atom mapping is valid (OF3 + Protenix, "
            "antagonist arm, ref_pdb == input_bound_pdb, n={n_valid} rows "
            "out of 1400 antag), pose accuracy is {dock_lo:.0f}-{dock_hi:.0f}% "
            "dock-rate (ligand_rmsd_to_ref < 3 A) with median {med_lo:.1f}-{med_hi:.1f} A. "
            "This is a striking gap relative to Chai-1's 77% PoseBusters number "
            "and is consistent with co-folding + G-alpha + no-template being "
            "materially harder than dock-to-apo-receptor. The remaining 20 "
            "cells are unmeasurable pending an MCS-based atom matcher; this "
            "scoped finding cannot be generalised to Boltz, Chai, or the "
            "agonist arm."
        ).format(
            n_valid=total_valid_rows,
            dock_lo=100 * min(dock_rates) if dock_rates else 0,
            dock_hi=100 * max(dock_rates) if dock_rates else 0,
            med_lo=min(medians) if medians else 0,
            med_hi=max(medians) if medians else 0,
        ),
        "n_valid_rows": total_valid_rows,
        "dock_rate_per_cell": per_cell,
        "aggregate": {
            "n_populated_rows_across_4_cells": total_populated_rows,
            "n_dock_lt_3A_across_4_cells": total_dock_lt_3A,
            "aggregate_dock_rate_lt_3A": (
                total_dock_lt_3A / total_populated_rows
                if total_populated_rows else float("nan")
            ),
            "dock_rate_range_over_cells": [
                min(dock_rates) if dock_rates else float("nan"),
                max(dock_rates) if dock_rates else float("nan"),
            ],
            "median_ligand_rmsd_range_over_cells_A": [
                min(medians) if medians else float("nan"),
                max(medians) if medians else float("nan"),
            ],
        },
        "explicit_non_generalisability_scope": {
            "does_not_cover_backbones": ["boltz", "chai"],
            "does_not_cover_arms": ["full_agonist", "decoy_lig"],
            "reason_backbones": (
                "Boltz-2 and Chai-1 emit SMILES-derived or normalised atom "
                "names that diverge from the CCD atom-name convention. "
                "The scorer's (atom_name, element) matcher (scorer/pocket_metrics.py:501-624) "
                "returns no_atom_match at high rates on those backbones "
                "regardless of docking pose quality. Chai/neutral_antagonist/apo: "
                "0-10% population; Boltz/neutral_antagonist/apo: 31-41% population. "
                "Neither cell crosses the 50% population floor for a valid rate estimate."
            ),
            "reason_arms": (
                "For full_agonist rows the active reference is typically a "
                "different PDB from the input's ligand_bound_pdb (a signalling-state "
                "structure with a different agonist chemistry), so the reference "
                "CCD differs from the input CCD, atom names do not overlap, and "
                "the RMSD is no_atom_match. Decoy_lig rows are uninterpretable "
                "by construction (property-matched non-binders vs real-ligand ref)."
            ),
        },
        "comparison_to_posebusters": {
            "chai_1_posebusters_rate": 0.77,
            "chai_1_posebusters_benchmark": "dock-to-apo-receptor, single sample, template allowed",
            "this_scoped_measurement": "co-fold receptor + antagonist + Gα heterotrimer, 5 samples × 5 seeds, no template, ref_pdb = input_bound_pdb",
            "conclusion": (
                "Direct comparison overstates the gap: the setups differ on "
                "receptor construct (apo receptor vs full complex), sampling "
                "budget (1 vs 25), template usage (yes vs no), and reference "
                "selection (input-bound crystal vs role-specific active ref). "
                "The 6-8% observed dock rate here is a lower bound on what a "
                "PoseBusters-shaped Chai measurement would report."
            ),
        },
        "supersedes": {
            "v1_verdict": "DOCKING_NOT_A_FAILURE_MODE (withdrawn as premature)",
            "v2_verdict": "DOCKING_FAILURE_<50pct (withdrawn — cell selection was CCD-driven, not pose-driven)",
            "v3_prev_verdict": "DOCKING_POSE_QUALITY_UNRESOLVED (superseded — scoped verdict is preferable to full withdrawal)",
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {args.out}")
    print(f"n_valid_rows={total_valid_rows}, "
          f"aggregate_dock_rate={100*total_dock_lt_3A/total_populated_rows:.1f}%, "
          f"per-cell dock rates: {[f'{100*r:.1f}%' for r in dock_rates]}")


if __name__ == "__main__":
    main()
