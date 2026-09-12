#!/usr/bin/env python3
"""Recompute SC-C-1 2x2 pocket-Ca-RMSD interaction under cluster-boot
over the paralog cluster map (Block A C-8 authoritative convention).

The receptor-boot CIs already exist in
`stage3_2x2_ligand_state_specificity.json` (per-backbone interaction.ci_lo/ci_hi).
This script recomputes the CI resampling paralog clusters instead of
individual receptors.

Method (matching stage3_post_audit_analysis.py exactly, with
resampling unit swapped):
 - For each backbone, restrict to Class-A passed rows.
 - For each of the 23 common receptors, collect per-receptor lists of
   pocket_ca_rmsd_{active,inactive} for {agonist, antag} rows.
 - Point estimate: interaction = (ag_active_pooled - antag_active_pooled)
   - (ag_inactive_pooled - antag_inactive_pooled), where each _pooled
   is the row-mean over ALL rows in the 23 receptors combined for that
   ligand-role × ref-role cell.
 - Bootstrap: draw len(clusters)=16 clusters with replacement; for each
   drawn cluster, use ALL receptors it contains (from the 23 common set);
   compute the four cell means and the interaction. Repeat 5000×,
   seed 1234 (matching original).
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
CLUSTERS_CSV = REPO / "experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv"
S1_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s1_loro_classifier.json"
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json"

N_ITER = 5000
RNG_SEED = 1234


def sha256_file(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _to_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def _mean(xs):
    xs = [x for x in xs if not math.isnan(x)]
    if not xs:
        return float("nan")
    return sum(xs) / len(xs)


def main():
    s1 = json.loads(S1_JSON.read_text())
    common_23 = [r.upper() for r in s1["common_receptors"]]

    # Load cluster map
    clu = pd.read_csv(CLUSTERS_CSV)
    clu["receptor"] = clu["receptor"].astype(str).str.upper()
    cluster_map = dict(zip(clu["receptor"], clu["cluster_id"]))

    # For the 23 common receptors, map to cluster
    rec_to_cluster = {r: cluster_map.get(r, f"single_{r}") for r in common_23}
    cluster_to_recs = defaultdict(list)
    for r, c in rec_to_cluster.items():
        cluster_to_recs[c].append(r)
    clusters = sorted(cluster_to_recs.keys())
    n_clusters = len(clusters)
    print(f"n_receptors_in_common: {len(common_23)}")
    print(f"n_clusters covering them: {n_clusters}")
    print(f"cluster_to_receptors:")
    for c in clusters:
        recs = cluster_to_recs[c]
        print(f"  {c} ({len(recs)}): {recs}")

    # Load rows
    print("\nloading rows.tier3.v2.csv…")
    df = pd.read_csv(ROWS_CSV, low_memory=False)
    df = df[df["passed"].astype(str).str.lower() == "true"].copy()
    df = df[df["receptor_class"].astype(str).str.upper() == "A"].copy()
    df["receptor_slug"] = df["receptor_slug"].astype(str).str.upper()
    df["backbone"] = df["input_path"].str.extract(r"/(boltz|chai|of3|protenix)/", expand=False)
    df["ligand_role"] = df["ligand_role"].astype(str)
    df["pocket_ca_rmsd_active"] = pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce")
    df["pocket_ca_rmsd_inactive"] = pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce")

    per_backbone = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df[df["backbone"] == bb]
        # Build per-receptor 4-cell lists (matching original script exactly)
        ag_a, ag_i, an_a, an_i = {}, {}, {}, {}
        for _, r in sub.iterrows():
            rec = r["receptor_slug"]
            if rec not in common_23:
                continue
            v_a = r["pocket_ca_rmsd_active"]; v_i = r["pocket_ca_rmsd_inactive"]
            if pd.isna(v_a) or pd.isna(v_i):
                continue
            role = r["ligand_role"]
            if role == "full_agonist":
                ag_a.setdefault(rec, []).append(v_a); ag_i.setdefault(rec, []).append(v_i)
            elif role in ("neutral_antagonist", "inverse_agonist"):
                an_a.setdefault(rec, []).append(v_a); an_i.setdefault(rec, []).append(v_i)
        # Point estimate: pool across all common receptors' rows (matching original)
        common_present = set(ag_a) & set(ag_i) & set(an_a) & set(an_i)
        common_list = sorted(common_present)
        def _pool(bins, recs):
            return _mean([v for c in recs for v in bins.get(c, [])])
        pt = ((_pool(ag_a, common_list) - _pool(an_a, common_list))
              - (_pool(ag_i, common_list) - _pool(an_i, common_list)))

        # Cluster-boot: draw n_clusters clusters with replacement, use all recs in each
        rng = random.Random(RNG_SEED)
        reps = []
        for _ in range(N_ITER):
            drawn = [rng.choice(clusters) for _ in range(n_clusters)]
            # Flatten to receptors (allowing duplicates via multi-cluster draws)
            sampled_recs = []
            for c in drawn:
                for rec in cluster_to_recs[c]:
                    if rec in common_present:
                        sampled_recs.append(rec)
            if not sampled_recs:
                continue
            v1 = _pool(ag_a, sampled_recs)
            v2 = _pool(ag_i, sampled_recs)
            v3 = _pool(an_a, sampled_recs)
            v4 = _pool(an_i, sampled_recs)
            if any(math.isnan(x) for x in (v1, v2, v3, v4)):
                continue
            interaction = (v1 - v3) - (v2 - v4)
            reps.append(interaction)
        reps_sorted = sorted(reps)
        if reps_sorted:
            lo = reps_sorted[max(0, int(len(reps_sorted) * 0.025) - 1)]
            hi = reps_sorted[min(len(reps_sorted) - 1, int(len(reps_sorted) * 0.975))]
        else:
            lo = float("nan"); hi = float("nan")

        # Also recompute receptor-boot for cross-check
        rng2 = random.Random(RNG_SEED)
        reps2 = []
        for _ in range(N_ITER):
            sample = [rng2.choice(common_list) for _ in range(len(common_list))]
            v1 = _pool(ag_a, sample)
            v2 = _pool(ag_i, sample)
            v3 = _pool(an_a, sample)
            v4 = _pool(an_i, sample)
            if any(math.isnan(x) for x in (v1, v2, v3, v4)):
                continue
            reps2.append((v1 - v3) - (v2 - v4))
        rb_sorted = sorted(reps2)
        rb_lo = rb_sorted[max(0, int(len(rb_sorted) * 0.025) - 1)] if rb_sorted else float("nan")
        rb_hi = rb_sorted[min(len(rb_sorted) - 1, int(len(rb_sorted) * 0.975))] if rb_sorted else float("nan")

        per_backbone[bb] = {
            "point_estimate": pt,
            "cluster_boot": {
                "ci_lo": lo,
                "ci_hi": hi,
                "n_iter": N_ITER,
                "n_iter_finite": len(reps),
                "n_clusters": n_clusters,
                "signed_nonzero": (lo > 0 and hi > 0) or (lo < 0 and hi < 0),
            },
            "receptor_boot_recomputed": {
                "ci_lo": rb_lo,
                "ci_hi": rb_hi,
                "n_iter_finite": len(reps2),
                "n_receptors": len(common_list),
            },
            "n_common_receptors": len(common_list),
        }
        print(f"\n{bb}: point={pt:+.4f}")
        print(f"  cluster-boot 95% CI: [{lo:+.4f}, {hi:+.4f}]  (n_clusters={n_clusters})")
        print(f"  receptor-boot 95% CI: [{rb_lo:+.4f}, {rb_hi:+.4f}]  (n_rec={len(common_list)})")
        print(f"  signed (cluster): {(lo>0 and hi>0) or (lo<0 and hi<0)}")

    result = {
        "task": "recompute_scc1_cluster_boot",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows_csv": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "clusters_csv": {"path": str(CLUSTERS_CSV.relative_to(REPO)), "sha256": sha256_file(CLUSTERS_CSV)},
        },
        "convention": "cluster-boot over paralog clusters (Block A C-8 authoritative); receptor-boot re-run for cross-check",
        "n_iter": N_ITER,
        "rng_seed": RNG_SEED,
        "n_receptors_in_common": len(common_23),
        "n_clusters": n_clusters,
        "cluster_to_receptors": {c: cluster_to_recs[c] for c in clusters},
        "per_backbone": per_backbone,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, default=str))
    print(f"\nwrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
