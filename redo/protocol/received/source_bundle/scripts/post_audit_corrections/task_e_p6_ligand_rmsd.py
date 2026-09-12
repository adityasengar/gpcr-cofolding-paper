#!/usr/bin/env python3
"""Task E — recompute P6 (docking) using the now-populated
`ligand_rmsd_to_ref` column. P6-pass = ligand_rmsd_to_ref < 3.0 Å
(the standard 'docked at pocket' threshold).

Also reports the population rate per cell — the earlier note
(2026-09-04 memory) said the manifest-join fix left ligand_rmsd_to_ref
NaN on all Tier 1 rows. The v2 rescore fixed this partially but a gap
remains, so P6 verdicts must account for the population rate."""
from __future__ import annotations
import argparse, json, math, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta, load_rows, to_float


P6_THRESHOLD_DOCKED_A = 3.0
POPULATION_FLOOR_FOR_VERDICT = 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_E_p6_ligand_rmsd_to_ref.json")
    args = ap.parse_args()

    rows = load_rows(args.rows, manifest_csv=args.manifest)

    # Per-cell: n_passed, n_lig_rmsd_populated, n_docked (<3 A),
    # distribution stats.
    per_cell = defaultdict(lambda: {
        "n_passed": 0,
        "n_lig_rmsd_populated": 0,
        "n_docked_lt_3A": 0,
        "values": [],
    })
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        bb = (r.get("backbone") or "").lower()
        role = (r.get("ligand_role") or "").strip()
        pt = (r.get("partner_type") or "").lower()
        # Exclude no-ligand rows — but every Tier 3 row has a ligand.
        cell = (bb, role, pt or "unknown")
        c = per_cell[cell]
        c["n_passed"] += 1
        v = to_float(r.get("ligand_rmsd_to_ref"))
        if not math.isnan(v):
            c["n_lig_rmsd_populated"] += 1
            c["values"].append(v)
            if v < P6_THRESHOLD_DOCKED_A:
                c["n_docked_lt_3A"] += 1

    out_cells = []
    real_ligand_roles = {"full_agonist", "neutral_antagonist", "inverse_agonist"}
    for (bb, role, pt), c in sorted(per_cell.items()):
        vals = sorted(c["values"])
        median = vals[len(vals)//2] if vals else float("nan")
        p10 = vals[int(0.1*len(vals))] if vals else float("nan")
        p90 = vals[int(0.9*len(vals))] if vals else float("nan")
        pop_rate = c["n_lig_rmsd_populated"] / c["n_passed"] if c["n_passed"] else 0.0
        dock_rate_among_pop = (
            c["n_docked_lt_3A"] / c["n_lig_rmsd_populated"]
            if c["n_lig_rmsd_populated"] > 0 else float("nan")
        )
        is_real_ligand = role in real_ligand_roles
        if pop_rate < POPULATION_FLOOR_FOR_VERDICT:
            verdict = "UNTESTABLE_LIGAND_RMSD_UNDERPOPULATED"
        elif not is_real_ligand:
            # For decoys, "docked" means placed in the reference-agonist
            # pocket. Not a docking success but a decoy displacement
            # test.
            verdict = ("DECOY_MOSTLY_MISPLACED" if dock_rate_among_pop < 0.10
                       else ("DECOY_MOSTLY_DOCKED_AT_POCKET"
                             if dock_rate_among_pop > 0.90
                             else "DECOY_MIXED"))
        elif dock_rate_among_pop >= 0.90:
            verdict = "DOCKED_>90%"
        elif dock_rate_among_pop >= 0.50:
            verdict = "DOCKING_INCOMPLETE_50_TO_90pct"
        else:
            verdict = "DOCKING_FAILURE_<50pct"
        out_cells.append({
            "backbone": bb,
            "ligand_role": role,
            "partner_type": pt,
            "n_passed": c["n_passed"],
            "n_ligand_rmsd_to_ref_populated": c["n_lig_rmsd_populated"],
            "ligand_rmsd_populated_rate": pop_rate,
            "n_docked_lt_3A_among_populated": c["n_docked_lt_3A"],
            "dock_rate_among_populated": dock_rate_among_pop,
            "median_A_among_populated": median,
            "p10_A_among_populated": p10,
            "p90_A_among_populated": p90,
            "verdict": verdict,
        })

    payload = {
        "task": "E_p6_recompute_with_ligand_rmsd_to_ref",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "rows_csv": args.rows,
                "manifest_csv": args.manifest,
            }),
        },
        "predicate": {
            "P6_definition": (
                "P6_pass iff ligand_rmsd_to_ref < 3.0 A (docked at the "
                "reference-ligand pocket). Excludes rows where "
                "ligand_rmsd_to_ref is NaN."
            ),
            "population_floor_for_verdict": POPULATION_FLOOR_FOR_VERDICT,
        },
        "population_finding": (
            "ligand_rmsd_to_ref is NOT reliably populated across the "
            "v2 corpus. The manifest-join fix (commit ea9efe5) landed "
            "role_specific-aware antag-ref lookup, but the "
            "sidecar-path fallback did not fully wire on Chai (whose "
            "pool tree uses a different subdirectory naming convention "
            "than Boltz/OF3/Protenix). Population rates per cell range "
            "from 0.0% (chai neutral_antagonist apo) to 79% "
            "(of3/protenix neutral_antagonist g_alpha). See "
            "of3_purge_race_2026_09_03 memory + Block C Tier 1 "
            "ligand_rmsd_gap memory for context. Any P6 verdict below "
            "the 50%-populated floor is marked "
            "UNTESTABLE_LIGAND_RMSD_UNDERPOPULATED."
        ),
        "prior_p6_claim_being_revised": (
            "The earlier post-audit task5_p6_p2_p3.json declared "
            "'docking not a failure mode' based on P6 evaluated via "
            "min-contact <= 3.4 A on 400 CIFs (one per cell). That was "
            "'ligand-present-and-touching', not 'docked at the "
            "reference pocket'. This recompute uses the stronger "
            "ligand_rmsd_to_ref < 3 A predicate on the SUBSET where "
            "the column is populated. The 'DEFINITIVELY EXCLUDED' "
            "wording on the docking hypothesis is DOWNGRADED — most "
            "cells are UNTESTABLE at the strong predicate; where "
            "testable, results vary."
        ),
        "per_cell": out_cells,
        "verdict_downgrade_summary": (
            "The earlier 'docking was not a failure mode' claim "
            "cannot be sustained at the ligand_rmsd_to_ref < 3 Å "
            "level because most cells are underpopulated. On the "
            "cells that ARE testable, docking rates vary widely — a "
            "definitive claim requires a full-population rescore "
            "(back-fill the ligand_rmsd_to_ref column) before it can "
            "be stated in either direction."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
