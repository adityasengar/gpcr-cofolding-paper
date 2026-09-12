#!/usr/bin/env python3
"""Check 1 — same-reference control on the S1 LORO classifier.

Question: does the classifier read pocket shape, or does it read
"which reference was used"?

Method: for each receptor, verify that the inactive-reference PDB
(and the active-reference PDB) is IDENTICAL between the agonist and
antagonist rows, at the SHA-256 level of the deposited PDB file. If
they diverge, the classifier's Δ = pocket_ca_rmsd_active −
pocket_ca_rmsd_inactive can trivially learn "which inactive did the
scorer pick" instead of "how far is this pocket from the inactive
structure".

Two outputs:
  1. Per-receptor SHA divergence table (active + inactive, agonist vs
     antag). Exposes the mechanism.
  2. Rerun S1 F_i / F_ii / F_iii on the SUBSET of receptors where both
     axes are role-agnostic (SHA-set-equal). Compare AUROC to the
     original S1 result. If the AUROC survives on this subset, the
     method claim is not a reference-identity artefact.

Result location:
    experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/
        check1_same_reference_control.json
        check1_same_reference_control.md
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts/reaudit_2026_09_07"))

# Reuse the exact classifier and LORO logic from S1.
from s1_loro_classifier import (  # noqa: E402
    build_features, build_label, restrict_to_common_23,
    loro_evaluate, sha256_file,
    FEATURES_I, FEATURES_II, FEATURES_III,
    ROWS_CSV, MANIFEST_CSV,
)

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_JSON = OUT_DIR / "check1_same_reference_control.json"
OUT_MD = OUT_DIR / "check1_same_reference_control.md"


def _load_rows_with_manifest() -> pd.DataFrame:
    rows = pd.read_csv(ROWS_CSV, low_memory=False)
    man = pd.read_csv(MANIFEST_CSV, low_memory=False)
    midx = man.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(midx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(midx["partner_type"].to_dict()).fillna("")
    rows["ligand_role"] = rows["input_path"].map(midx["ligand_role"].to_dict()).fillna(
        rows.get("ligand_role", pd.Series([""] * len(rows)))
    )
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )
    df = build_features(rows)
    m = (df["receptor_class"].fillna("").astype(str).str.upper() == "A")
    m &= (df["passed"].astype(str).str.lower() == "true")
    df = df[m].copy()
    df["receptor_slug"] = df["receptor_slug"].astype(str).str.upper()
    return df


def _sha_set_by_receptor_role(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """SHA sets per (receptor, ligand_role) — drop empty strings and nans."""
    def _clean(x):
        s = set()
        for v in x.dropna():
            sv = str(v).strip()
            if sv and sv.lower() != "nan":
                s.add(sv)
        return frozenset(s)
    return (df.groupby(["receptor_slug", "ligand_role"])[col]
              .apply(_clean).unstack(fill_value=frozenset()))


def _row_level_agreement(df: pd.DataFrame, col: str) -> dict:
    """For each receptor, count rows where the SHA is the modal SHA vs an
    off-modal one; report per-role coverage."""
    out = {}
    for rec, sub in df.groupby("receptor_slug"):
        vc = sub[col].dropna().astype(str).replace("nan", "").value_counts()
        vc = vc[vc.index != ""]
        if len(vc) == 0:
            out[rec] = {"n_distinct_shas": 0, "modal_sha": "", "n_rows_modal": 0,
                        "n_rows_offmodal": 0, "n_rows_missing": int(len(sub))}
            continue
        modal = vc.index[0]
        n_modal = int(vc.iloc[0])
        n_off = int(vc.iloc[1:].sum())
        n_miss = int(len(sub) - vc.sum())
        out[rec] = {"n_distinct_shas": int(len(vc)), "modal_sha": modal,
                    "n_rows_modal": n_modal, "n_rows_offmodal": n_off,
                    "n_rows_missing": n_miss}
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()

    print("[check1] loading rows + manifest...", flush=True)
    df_all = _load_rows_with_manifest()
    df_common = restrict_to_common_23(df_all)
    print(f"[check1] 2×2 common set: {df_common['receptor_slug'].nunique()} receptors, "
          f"{len(df_common)} rows", flush=True)

    pair = df_common[df_common["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    print(f"[check1] classifier pair rows: {len(pair)}", flush=True)

    # ------------------------------------------------------------------
    # Part A — SHA divergence census
    # ------------------------------------------------------------------
    inactive_by_role = _sha_set_by_receptor_role(pair, "pocket_ref_pdb_sha_inactive")
    active_by_role = _sha_set_by_receptor_role(pair, "pocket_ref_pdb_sha_active")

    census_rows = []
    role_agnostic_recs = []
    for rec in sorted(pair["receptor_slug"].unique()):
        ia_ag = inactive_by_role.loc[rec].get("full_agonist", frozenset()) if rec in inactive_by_role.index else frozenset()
        ia_an = inactive_by_role.loc[rec].get("neutral_antagonist", frozenset()) if rec in inactive_by_role.index else frozenset()
        ac_ag = active_by_role.loc[rec].get("full_agonist", frozenset()) if rec in active_by_role.index else frozenset()
        ac_an = active_by_role.loc[rec].get("neutral_antagonist", frozenset()) if rec in active_by_role.index else frozenset()
        inactive_same = (ia_ag == ia_an) and len(ia_ag) > 0
        active_same = (ac_ag == ac_an) and len(ac_ag) > 0
        both_same = inactive_same and active_same
        if both_same:
            role_agnostic_recs.append(rec)
        census_rows.append({
            "receptor": rec,
            "inactive_ag_shas": sorted(ia_ag), "inactive_an_shas": sorted(ia_an),
            "active_ag_shas": sorted(ac_ag), "active_an_shas": sorted(ac_an),
            "inactive_same_ref_across_roles": inactive_same,
            "active_same_ref_across_roles": active_same,
            "both_same": both_same,
        })

    # Row-level agreement — even within a role, could a receptor mix
    # multiple inactive SHAs (e.g., different seeds seeing different refs)?
    inactive_rowlvl = _row_level_agreement(pair, "pocket_ref_pdb_sha_inactive")
    active_rowlvl = _row_level_agreement(pair, "pocket_ref_pdb_sha_active")
    off_modal_receptors = [
        rec for rec, d in inactive_rowlvl.items()
        if d["n_rows_offmodal"] > 0 or active_rowlvl[rec]["n_rows_offmodal"] > 0
    ]

    print(f"[check1] receptors with inactive SHA divergence between roles: "
          f"{len(pair['receptor_slug'].unique()) - len(role_agnostic_recs)} / "
          f"{len(pair['receptor_slug'].unique())}", flush=True)
    print(f"[check1] receptors with mixed SHAs within a role (off-modal rows > 0): "
          f"{len(off_modal_receptors)}", flush=True)
    print(f"[check1] role-agnostic subset ({len(role_agnostic_recs)} rec): "
          f"{role_agnostic_recs}", flush=True)

    # ------------------------------------------------------------------
    # Part B — rerun S1 F_i / F_ii / F_iii on the role-agnostic subset,
    #          apo arm × both arms.
    # ------------------------------------------------------------------
    df_ra = df_common[df_common["receptor_slug"].isin(role_agnostic_recs)].copy()
    df_ra_pair = df_ra[df_ra["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    print(f"[check1] role-agnostic pair rows: {len(df_ra_pair)}", flush=True)

    backbones = ["boltz", "chai", "of3", "protenix"]
    feature_sets = {
        "F_i_delta": FEATURES_I,
        "F_ii_pocket_family": FEATURES_II,
        "F_iii_pocket_plus_axes": FEATURES_III,
    }
    arms = ["both", "apo"]

    def _run(subset: pd.DataFrame, backbone: str, arm: str,
             feature_set_name: str, feature_names: list[str]) -> dict:
        sub = subset[subset["backbone"].str.lower() == backbone].copy()
        if arm != "both":
            sub = sub[sub["arm"] == arm].copy()
        pair_bb = build_label(sub, "full_agonist", "neutral_antagonist")
        if len(pair_bb) < 200 or pair_bb["receptor_slug"].nunique() < 10:
            return {"backbone": backbone, "arm": arm,
                    "feature_set": feature_set_name,
                    "reason": "insufficient_data",
                    "n_rows": int(len(pair_bb)),
                    "n_receptors": int(pair_bb["receptor_slug"].nunique())}
        model = "threshold" if feature_set_name == "F_i_delta" else "logreg"
        r = loro_evaluate(pair_bb, feature_names, model=model, n_permutations=200)
        r.update({"backbone": backbone, "arm": arm,
                  "feature_set": feature_set_name,
                  "n_rows": int(len(pair_bb)),
                  "n_receptors": int(pair_bb["receptor_slug"].nunique()),
                  "model": model})
        return r

    variants = []
    for arm in arms:
        for bb in backbones:
            for fs_name, fs_cols in feature_sets.items():
                print(f"  {arm:<5} {bb:<9} {fs_name}...", flush=True)
                v = _run(df_ra, bb, arm, fs_name, fs_cols)
                v["arm_label"] = arm
                variants.append(v)

    # ------------------------------------------------------------------
    # Compare to the original S1 numbers so the reader sees the Δ
    # ------------------------------------------------------------------
    s1 = json.loads((OUT_DIR / "s1_loro_classifier.json").read_text())
    orig_variants = s1["variants"]
    def _key(v):
        return (v.get("variant", ""), v["backbone"], v["arm"], v["feature_set"])
    def _find_orig(bb, arm, fs):
        # Original variants: A_all23_botharms (arm='both'), B_all23_apo (arm='apo')
        want_variant = "B_all23_apo" if arm == "apo" else "A_all23_botharms"
        for ov in orig_variants:
            if (ov.get("variant") == want_variant and ov["backbone"] == bb and
                    ov["feature_set"] == fs):
                return ov
        return {}

    for v in variants:
        ov = _find_orig(v["backbone"], v["arm"], v["feature_set"])
        v["original_pooled_auroc"] = ov.get("pooled_auroc")
        v["delta_pooled_auroc"] = (
            v.get("pooled_auroc") - ov["pooled_auroc"]
            if ("pooled_auroc" in v and ov.get("pooled_auroc") is not None)
            else None
        )

    # ------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------
    report = {
        "task": "check1_same_reference_control",
        "generated_utc": ts,
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)),
                     "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)),
                         "sha256": sha256_file(MANIFEST_CSV)},
            "reference_s1": str((OUT_DIR / "s1_loro_classifier.json").relative_to(REPO)),
        },
        "n_common_receptors": int(df_common["receptor_slug"].nunique()),
        "n_role_agnostic_receptors": len(role_agnostic_recs),
        "role_agnostic_receptors": role_agnostic_recs,
        "diverging_receptors": [c["receptor"] for c in census_rows if not c["both_same"]],
        "receptors_with_mixed_shas_within_a_role": off_modal_receptors,
        "per_receptor_census": census_rows,
        "variants": variants,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[check1] wrote {OUT_JSON.relative_to(REPO)}")

    # Markdown summary
    md = ["# Check 1 — same-reference control on the S1 LORO classifier", ""]
    md.append(f"Generated: {ts}")
    md.append("")
    md.append("## Reference divergence census")
    md.append(f"- 2×2 common set: {df_common['receptor_slug'].nunique()} receptors")
    md.append(f"- Receptors with role-agnostic references on BOTH axes: "
              f"**{len(role_agnostic_recs)}**")
    md.append(f"- Receptors with divergent references (agonist vs antag): "
              f"{len(census_rows) - len(role_agnostic_recs)}")
    md.append(f"- Receptors with mixed SHAs within a single role: "
              f"{len(off_modal_receptors)} — "
              f"{off_modal_receptors if off_modal_receptors else '(none)'}")
    md.append("")
    if len(role_agnostic_recs) == df_common['receptor_slug'].nunique():
        md.append("> **Result**: on the 2×2 common set, every receptor uses a "
                  "single active-reference PDB and a single inactive-reference "
                  "PDB, identical between agonist and antagonist rows. The "
                  "*role_specific* tag differs (`generic_inactive_fallback` for "
                  "agonist rows vs `inactive_neutral_antagonist` for antag) but "
                  "both tags resolve to the same physical PDB on these 23 "
                  "receptors. The S1 classifier was **already** operating on "
                  "a role-agnostic reference frame — the reference-identity "
                  "confound is not present on this evaluation set.")
    else:
        md.append(f"> **Result**: only {len(role_agnostic_recs)} of "
                  f"{df_common['receptor_slug'].nunique()} common-set receptors "
                  "have role-agnostic references. Reruns below restrict to this "
                  "subset.")
    md.append("")

    md.append("## Rerun on the role-agnostic subset")
    md.append("")
    md.append("| arm | backbone | features | n_rec | n_rows | AUROC | orig AUROC | Δ AUROC |")
    md.append("|---|---|---|---|---|---|---|---|")
    for v in variants:
        if "pooled_auroc" not in v:
            md.append(f"| {v['arm']} | {v['backbone']} | {v['feature_set']} | "
                      f"{v.get('n_receptors','?')} | {v.get('n_rows','?')} | "
                      f"SKIP ({v.get('reason','')}) | | |")
            continue
        oa = v.get("original_pooled_auroc")
        da = v.get("delta_pooled_auroc")
        md.append(f"| {v['arm']} | {v['backbone']} | {v['feature_set']} | "
                  f"{v['n_receptors']} | {v['n_rows']} | {v['pooled_auroc']:.3f} | "
                  f"{oa:.3f} | {da:+.3f} |")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    if len(role_agnostic_recs) == df_common['receptor_slug'].nunique():
        md.append("The check reduces to a self-consistency test — same rows, "
                  "same features, same LORO folds. Any AUROC difference is "
                  "run-to-run RNG noise (numpy's `default_rng(20260907)` is "
                  "seeded consistently, so Δ should be tight around zero).")
    else:
        md.append("Compare Δ AUROC per (arm × backbone × feature-set). If the "
                  "role-agnostic AUROC drops below the pre-registered kill "
                  "threshold (0.65) on every backbone in the apo arm, the "
                  "method claim was reference-identity confounded.")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"[check1] wrote {OUT_MD.relative_to(REPO)}")

    # Print summary table
    print()
    print("=" * 100)
    print("CHECK 1 SUMMARY — role-agnostic rerun (apo × F_iii row)")
    print("=" * 100)
    for v in variants:
        if v["arm"] != "apo" or v["feature_set"] != "F_iii_pocket_plus_axes":
            continue
        if "pooled_auroc" not in v:
            print(f"  {v['backbone']:<10} SKIP")
            continue
        oa = v.get("original_pooled_auroc") or 0.0
        print(f"  {v['backbone']:<10} n_rec={v['n_receptors']:>2}  n={v['n_rows']:>5}  "
              f"AUROC={v['pooled_auroc']:.3f}  orig={oa:.3f}  Δ={v['delta_pooled_auroc']:+.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
