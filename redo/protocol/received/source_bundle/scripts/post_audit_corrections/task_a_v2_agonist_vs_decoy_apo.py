#!/usr/bin/env python3
"""Task A v2 — agonist-vs-decoy apo-arm contrast, stratified by
Task A v1's same-complex split.

For each Class-A receptor with at least one full_agonist/apo row AND
at least one decoy_lig/apo row:

  per-receptor scalar =
      mean(pocket_ca_rmsd_active | full_agonist & apo)
    − mean(pocket_ca_rmsd_active | decoy_lig    & apo)

Negative → the agonist input reproduces the active reference pocket
better than a property-matched decoy. This is a stronger per-receptor
control than the agonist/apo vs agonist/g_alpha contrast because both
partners now match on scaffold (both = apo receptor) — the only
difference between the two groups is ligand identity (real agonist vs
property-matched non-binder).

Stratify by:
  same_complex agonist stratum — bound_pdb ∈ active_ref_pdbs (recallable)
  must_generalise stratum       — bound_pdb ∉ active_ref_pdbs

Test per backbone:
  same_mean, diff_mean, delta = same − diff, 95% cluster-bootstrap CI
  (agonist-arm split; decoy_apo has no bound-pdb of its own).

User's pre-hypothesis: 8/8 signed CIs on must_generalise (n=13), effect
LARGER there than in the recallable stratum (n=15), and Chai's
non-significant cell will be in the RECALLABLE stratum.

Also computes on `pocket_sidechain_rmsd_active` as a secondary axis.
"""
from __future__ import annotations
import argparse, json, math, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import (
    REPO, to_float, load_rows, load_ref_set, load_ligand_bound_pdbs,
    cluster_bootstrap_two_group_diff, build_recon_meta, _mean,
)


def _active_pdbs(refs):
    return {x["pdb_id"].strip().upper() for x in refs.get("active", [])
            if x.get("pdb_id")}


def _bootstrap_mean_ci(values_by_receptor, n_iter=5000, seed=7):
    """Cluster-bootstrap over the *keys* of values_by_receptor —
    resample receptors with replacement, take the mean of per-receptor
    means, return (est, ci_lo, ci_hi, n_clusters, n_rows)."""
    import random
    keys = list(values_by_receptor.keys())
    if not keys:
        return {"est": float("nan"), "ci_lo": float("nan"),
                "ci_hi": float("nan"), "n_clusters": 0, "n_rows": 0,
                "signed_nonzero": False}
    rng = random.Random(seed)
    reps = []
    for _ in range(n_iter):
        sample_keys = [rng.choice(keys) for _ in range(len(keys))]
        per_r = [_mean(values_by_receptor[k]) for k in sample_keys]
        per_r = [x for x in per_r if not math.isnan(x)]
        if per_r:
            reps.append(sum(per_r) / len(per_r))
    reps.sort()
    per_r_pt = [_mean(values_by_receptor[k]) for k in keys]
    per_r_pt = [x for x in per_r_pt if not math.isnan(x)]
    pt = sum(per_r_pt) / len(per_r_pt) if per_r_pt else float("nan")
    lo = reps[max(0, int(len(reps)*0.025) - 1)] if reps else float("nan")
    hi = reps[min(len(reps)-1, int(len(reps)*0.975))] if reps else float("nan")
    signed = (not (math.isnan(lo) or math.isnan(hi))
              and ((lo > 0 and hi > 0) or (lo < 0 and hi < 0)))
    return {"est": pt, "ci_lo": lo, "ci_hi": hi,
            "n_clusters": len(keys),
            "n_rows": sum(len(v) for v in values_by_receptor.values()),
            "signed_nonzero": signed}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rows.tier3.v2.csv")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/rescore_manifest.tier3.v2.csv")
    ap.add_argument("--ref-set", type=Path,
                    default=REPO / "refs/reference_set.csv")
    ap.add_argument("--ligand-sets", nargs="+", type=Path,
                    default=[REPO / "refs/ligand_set.csv",
                             REPO / "refs/ligand_set_tier3.csv"])
    ap.add_argument("--out", type=Path,
                    default=REPO / "experiments/021_block_c_tier3_pharmacology"
                    "/analysis/verification/task_A_v2_agonist_vs_decoy_apo_same_complex.json")
    args = ap.parse_args()

    rows = load_rows(args.rows, manifest_csv=args.manifest)
    ref_set = load_ref_set(args.ref_set)
    lig_pdbs = load_ligand_bound_pdbs(args.ligand_sets)

    # Same-complex stratum on the AGONIST arm — matches Task A v1.
    strat = {}
    for rec, refs in ref_set.items():
        ag_pdb = lig_pdbs.get((rec, "full_agonist"), "")
        active_set = _active_pdbs(refs)
        if not ag_pdb or not active_set:
            strat[rec] = ("missing", ag_pdb, sorted(active_set))
            continue
        strat[rec] = (
            ("same" if ag_pdb in active_set else "different"),
            ag_pdb, sorted(active_set)
        )

    # per (backbone, axis, receptor, group=ag/dec) → list of values
    per_bb = defaultdict(lambda: {
        "ca": {"ag": defaultdict(list), "dec": defaultdict(list)},
        "sc": {"ag": defaultdict(list), "dec": defaultdict(list)},
    })
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        if (r.get("receptor_class") or "").upper() != "A":
            continue
        rec = (r.get("receptor_slug") or "").upper()
        bb = (r.get("backbone") or "").lower()
        if not bb:
            continue
        role = (r.get("ligand_role") or "").strip()
        pt = (r.get("partner_type") or "").lower()
        if pt != "apo":
            continue
        if role == "full_agonist":
            grp = "ag"
        elif role == "decoy_lig":
            grp = "dec"
        else:
            continue
        pca = to_float(r.get("pocket_ca_rmsd_active"))
        psc = to_float(r.get("pocket_sidechain_rmsd_active"))
        d = per_bb[bb]
        if not math.isnan(pca):
            d["ca"][grp][rec].append(pca)
        if not math.isnan(psc):
            d["sc"][grp][rec].append(psc)

    # Build per-receptor per-backbone contrast (agonist_apo − decoy_apo)
    # only for receptors that have BOTH groups populated.
    per_backbone_output = {}
    for bb in sorted(per_bb):
        d = per_bb[bb]
        bb_out = {}
        for axis, pretty in (("ca", "pocket_ca_rmsd_active"),
                             ("sc", "pocket_sidechain_rmsd_active")):
            ag = d[axis]["ag"]
            dec = d[axis]["dec"]
            common_recs = sorted(set(ag) & set(dec))
            # Split by agonist-arm stratum.
            same_delta = {}
            diff_delta = {}
            for rec in common_recs:
                stratum = strat.get(rec, ("missing",))[0]
                if stratum not in ("same", "different"):
                    continue
                delta = _mean(ag[rec]) - _mean(dec[rec])
                if math.isnan(delta):
                    continue
                if stratum == "same":
                    same_delta.setdefault(rec, []).append(delta)
                else:
                    diff_delta.setdefault(rec, []).append(delta)
            same_stat = _bootstrap_mean_ci(same_delta, seed=hash(("s", bb, axis)) % 65536)
            diff_stat = _bootstrap_mean_ci(diff_delta, seed=hash(("d", bb, axis)) % 65536)
            two_grp = cluster_bootstrap_two_group_diff(same_delta, diff_delta, seed=42)
            # Verdict per (backbone × axis)
            n_diff = diff_stat["n_clusters"]
            if n_diff < 5:
                verdict = "UNDERPOWERED_ON_MUST_GENERALISE"
            elif diff_stat["signed_nonzero"] and same_stat["signed_nonzero"]:
                # both signed non-zero — HOLD_ON_BOTH — check which is
                # stronger by point estimate.
                verdict = ("HOLD_ON_MUST_GENERALISE_STRONGLY"
                           if abs(diff_stat["est"]) > abs(same_stat["est"])
                           else "HOLD_ON_BOTH_STRATA_RECALLABLE_STRONGER")
            elif diff_stat["signed_nonzero"] and not same_stat["signed_nonzero"]:
                verdict = "HOLD_ON_MUST_GENERALISE_ONLY"
            elif same_stat["signed_nonzero"] and not diff_stat["signed_nonzero"]:
                verdict = "HOLD_ON_RECALLABLE_ONLY_ANTI_MEMORISATION"
            else:
                verdict = "NULL_ON_BOTH"
            bb_out[pretty] = {
                "same_stratum_mean_delta_A": same_stat,
                "diff_stratum_mean_delta_A": diff_stat,
                "same_minus_diff_of_deltas": two_grp,
                "verdict": verdict,
                "n_receptors_same": len(same_delta),
                "n_receptors_diff": len(diff_delta),
                "n_receptors_total_common_apo": len(common_recs),
                "signed_delta_expected_negative_for_agonist_specificity": True,
                "note": (
                    "Per-receptor scalar = "
                    "mean(pocket_*_active | full_agonist,apo) − "
                    "mean(pocket_*_active | decoy_lig,apo). Negative "
                    "= agonist input better matches active reference "
                    "pocket than decoy. Cluster-bootstrap 95% CI over "
                    "receptors (5000 iter). Same stratum = recallable "
                    "(agonist bound_pdb ∈ active refs); diff = "
                    "must-generalise."
                ),
            }
        per_backbone_output[bb] = bb_out

    # Chai non-significant cell — which stratum?
    chai_recallable_ca_signed = per_backbone_output.get(
        "chai", {}).get("pocket_ca_rmsd_active", {}).get(
            "same_stratum_mean_delta_A", {}).get("signed_nonzero", False)
    chai_mustgen_ca_signed = per_backbone_output.get(
        "chai", {}).get("pocket_ca_rmsd_active", {}).get(
            "diff_stratum_mean_delta_A", {}).get("signed_nonzero", False)
    chai_status_ca = ("mustgen_signed" if chai_mustgen_ca_signed else "mustgen_null")
    chai_status_ca += "_and_" + ("recallable_signed" if chai_recallable_ca_signed
                                  else "recallable_null")

    # Count "8/8 signed CIs on must-generalise" — 4 backbones × 2 axes = 8 tests
    n_signed_mustgen = 0
    n_signed_recall = 0
    for bb, bb_out in per_backbone_output.items():
        for axis, res in bb_out.items():
            if res["diff_stratum_mean_delta_A"]["signed_nonzero"]:
                n_signed_mustgen += 1
            if res["same_stratum_mean_delta_A"]["signed_nonzero"]:
                n_signed_recall += 1
    total_tests = sum(len(v) for v in per_backbone_output.values())

    payload = {
        "task": "A_v2_agonist_vs_decoy_apo_stratified_by_same_complex",
        "reconstruction": {
            "reconstruction_script": __file__,
            **build_recon_meta({
                "rows_csv": args.rows,
                "manifest_csv": args.manifest,
                "ref_set_csv": args.ref_set,
                **{f"ligand_set_{i}": p for i, p in enumerate(args.ligand_sets)},
            }),
        },
        "definition": (
            "Per receptor: delta = "
            "mean(pocket_*_active | full_agonist,apo) − "
            "mean(pocket_*_active | decoy_lig,apo). Negative = "
            "agonist rows closer to active reference pocket than decoy "
            "rows. Stratify by Task A v1 same-complex split on the "
            "AGONIST arm (bound_pdb ∈ active_refs → recallable/same; "
            "otherwise → must-generalise/different). Cluster-bootstrap "
            "over receptors (5000 iter). This is a per-arm marginal "
            "contrast — better-powered than the 2×2 interaction "
            "test which requires common receptors in the joint "
            "must-generalise cell (n=3 in v1)."
        ),
        "user_hypothesis": (
            "8/8 signed CIs on must_generalise (n≈13), the effect "
            "LARGER there than in recallable (n≈15), and Chai's only "
            "non-significant cell in the RECALLABLE stratum."
        ),
        "hypothesis_result": {
            f"n_signed_ci_must_generalise_over_{total_tests}_tests": n_signed_mustgen,
            f"n_signed_ci_recallable_over_{total_tests}_tests": n_signed_recall,
            "chai_ca_stratum_status": chai_status_ca,
            "chai_ca_recallable_signed": chai_recallable_ca_signed,
            "chai_ca_mustgen_signed": chai_mustgen_ca_signed,
        },
        "per_backbone": per_backbone_output,
        "stratum_split": {
            rec: {"stratum": s[0], "agonist_bound_pdb": s[1],
                  "active_refs": s[2]}
            for rec, s in sorted(strat.items())
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    raise SystemExit(main() or 0)
