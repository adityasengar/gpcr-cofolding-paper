#!/usr/bin/env python3
"""Step 4 — redock vs cross-dock partitioned analysis on t7c_full corpus.

Compares to the previous t7b_pose_accuracy pipeline BUT:
  - Uses rescore_t7c_full/rows.csv (Bug #2 tripwire + Bug #3 MCS fix)
  - Splits on redock (input_bound_pdb == scorer_reference_pdb) vs cross-dock
  - Excludes decoy_lig (scorer docstring rule)
  - Reports ECDF per (backbone × arm × ligand_role × partition × receptor)
  - Does NOT pool across receptors
"""
from __future__ import annotations
import csv, statistics
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path("/Users/SENGAAD1/Documents/claude/paper_af3")
ROWS = REPO / "experiments/021_block_c_tier3_pharmacology/rescore_t7c_full/rows.csv"
MANIFEST = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
REF_SET = REPO / "refs/reference_set.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"


def build_ref_lookup():
    d = {}
    for r in csv.DictReader(REF_SET.open()):
        rec = r.get("receptor_slug","").upper().strip()
        role = r.get("role","").lower().strip()
        rs = r.get("role_specific","").strip()
        pdb = r.get("pdb_id","").upper().strip()
        if rec and role and pdb:
            d[(rec, role, rs)] = pdb
    return d


def resolve_ref_pdb(lookup, receptor, ligand_role):
    rec = receptor.upper()
    if ligand_role == "neutral_antagonist":
        return lookup.get((rec, "inactive", "inactive_neutral_antagonist")) or \
               lookup.get((rec, "inactive", ""))
    if ligand_role == "inverse_agonist":
        return lookup.get((rec, "inactive", "inactive_inverse_agonist")) or \
               lookup.get((rec, "inactive", ""))
    return lookup.get((rec, "active", ""))


def is_nan(s: str) -> bool:
    return s in ("", "nan", "NaN", "None")


def main():
    print(f"[step4] loading rescore_t7c_full/rows.csv...", flush=True)
    rows = list(csv.DictReader(ROWS.open()))
    print(f"        {len(rows)} rows", flush=True)

    m_idx = {r["prediction_path"]: r for r in csv.DictReader(MANIFEST.open())}
    ref_lookup = build_ref_lookup()

    # Attach backbone / arm / ligand_role / redock partition to every row
    for r in rows:
        m = m_idx.get(r.get("input_path",""))
        if not m:
            r["_bb"] = ""; r["_arm"] = ""; r["_role"] = ""; r["_redock"] = ""
            continue
        r["_bb"] = m["backbone"].lower()
        r["_arm"] = "apo" if m["partner_type"] == "apo" else "cognate"
        r["_role"] = m["ligand_role"]
        input_bound_pdb = m.get("ligand_bound_pdb","").upper().strip()
        recep = r.get("receptor_slug","").upper()
        scorer_ref = resolve_ref_pdb(ref_lookup, recep, r["_role"])
        r["_redock"] = "redock" if (input_bound_pdb and scorer_ref and input_bound_pdb == scorer_ref) else "cross_dock"

    # Filter: exclude decoy_lig + non-passing + non-numeric
    def usable(r):
        if r.get("passed","").lower() != "true":
            return False
        if r["_role"] == "decoy_lig":
            return False
        if r["_role"] not in ("full_agonist", "neutral_antagonist", "inverse_agonist"):
            return False
        try:
            v = float(r.get("ligand_rmsd_to_ref",""))
            return v == v
        except:
            return False

    filtered = [r for r in rows if usable(r)]
    print(f"        {len(filtered)} usable (real ligand, passed, numeric)", flush=True)

    # ECDF per (backbone × arm × role × partition × receptor)
    groups = defaultdict(list)
    for r in filtered:
        v = float(r["ligand_rmsd_to_ref"])
        groups[(r["_bb"], r["_arm"], r["_role"], r["_redock"], r.get("receptor_slug","").upper())].append(v)

    # Also per (bb × arm × role × partition) aggregated across receptors,
    # BUT only as a per-receptor ECDF summary — never pool the underlying
    # numbers.
    per_cell_per_recep_summary = []
    for key, vs in sorted(groups.items()):
        bb, arm, role, part, rec = key
        vs.sort()
        n = len(vs)
        pct_lt3 = 100 * sum(1 for v in vs if v < 3.0) / n
        med = statistics.median(vs)
        p25 = vs[n//4] if n >= 4 else vs[0]
        p75 = vs[3*n//4] if n >= 4 else vs[-1]
        per_cell_per_recep_summary.append({
            "backbone": bb, "arm": arm, "role": role, "partition": part,
            "receptor": rec, "n": n,
            "median_rmsd_A": round(med, 3),
            "p25_A": round(p25, 3),
            "p75_A": round(p75, 3),
            "pct_dock_lt_3A": round(pct_lt3, 1),
        })

    # Cell-level receptor distribution: how many receptors have >20% dock,
    # >50% dock, all-fail, all-dock — anti-pool report per (bb × arm × role × partition).
    cell_receptor_dist = []
    per_cell = defaultdict(list)
    for row in per_cell_per_recep_summary:
        key = (row["backbone"], row["arm"], row["role"], row["partition"])
        per_cell[key].append(row["pct_dock_lt_3A"])
    for key, pct_list in sorted(per_cell.items()):
        bb, arm, role, part = key
        pct_list.sort()
        n_recep = len(pct_list)
        cell_receptor_dist.append({
            "backbone": bb, "arm": arm, "role": role, "partition": part,
            "n_receptors": n_recep,
            "pct_dock_median_across_receptors": round(statistics.median(pct_list), 1) if n_recep else 0,
            "n_receptors_dock_gt_50pct": sum(1 for p in pct_list if p > 50),
            "n_receptors_dock_gt_20pct": sum(1 for p in pct_list if p > 20),
            "n_receptors_all_fail": sum(1 for p in pct_list if p == 0),
            "n_receptors_all_dock": sum(1 for p in pct_list if p == 100),
            "receptor_pct_list": ";".join(f"{p:.0f}" for p in pct_list),
        })

    # Write outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    per_recep_csv = OUT_DIR / "step4_ecdf_per_receptor.csv"
    with per_recep_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(per_cell_per_recep_summary[0].keys()))
        w.writeheader()
        for r in per_cell_per_recep_summary:
            w.writerow(r)

    cell_dist_csv = OUT_DIR / "step4_cell_receptor_distribution.csv"
    with cell_dist_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cell_receptor_dist[0].keys()))
        w.writeheader()
        for r in cell_receptor_dist:
            w.writerow(r)

    # Headline: for each (bb × arm × role × partition), report median-across-
    # receptors of pct_dock, along with the receptor distribution.
    print(f"\n=== Median-across-receptors dock rate + distribution ===")
    print(f"{'backbone':<9} {'arm':<8} {'role':<20} {'partition':<11} {'n_rcp':>5} {'med%':>5} {'>50%':>4} {'>20%':>4} {'all_fail':>8} {'all_dock':>8}")
    for r in cell_receptor_dist:
        print(f"{r['backbone']:<9} {r['arm']:<8} {r['role']:<20} {r['partition']:<11} {r['n_receptors']:>5} "
              f"{r['pct_dock_median_across_receptors']:>5.1f} "
              f"{r['n_receptors_dock_gt_50pct']:>4} {r['n_receptors_dock_gt_20pct']:>4} "
              f"{r['n_receptors_all_fail']:>8} {r['n_receptors_all_dock']:>8}")

    print(f"\nwrote {per_recep_csv.relative_to(REPO)}")
    print(f"wrote {cell_dist_csv.relative_to(REPO)}")

    # Also — one more diagnostic. Method distribution.
    method_dist = Counter(r.get("pocket_ligand_atom_map_method","") for r in filtered)
    print(f"\nMethod distribution on usable rows: {dict(method_dist.most_common())}")


if __name__ == "__main__":
    main()
