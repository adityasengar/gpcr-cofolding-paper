#!/usr/bin/env python3
"""S6 — generalization: chemotype, cutoff, curation, per-row anti-memorization."""
from __future__ import annotations
import hashlib, json, math, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))
from s1_loro_classifier import (  # type: ignore
    load_and_prep, restrict_to_common_23, SELF_REF_RECEPTORS,
    FEATURES_III, _auroc, _fit_predict_logreg,
)

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s6_generalization.json"
LIGAND_SET_TIER3 = REPO / "refs/ligand_set_tier3.csv"
REF_SET_CSV = REPO / "refs/reference_set.csv"
CUTOFF_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3b_v1_training_cutoff_stratification_secondary.json"
BLOCK_A_ROWS = REPO / "experiments/018_block_a_switch_test/analysis/rows.pocket.csv"
GPCR_COUPLING = REPO / "refs/gpcr_coupling.csv"


def transfer_auroc(train_df, test_df, features):
    Xtr = train_df[features].to_numpy(dtype=float); ytr = train_df["_label"].to_numpy(dtype=int)
    Xte = test_df[features].to_numpy(dtype=float); yte = test_df["_label"].to_numpy(dtype=int)
    m = np.isfinite(Xtr).all(axis=1); Xtr = Xtr[m]; ytr = ytr[m]
    m2 = np.isfinite(Xte).all(axis=1); Xte = Xte[m2]; yte = yte[m2]
    if len(np.unique(ytr)) < 2 or len(Xte) == 0 or len(np.unique(yte)) < 2:
        return float("nan")
    return float(_auroc(yte, _fit_predict_logreg(Xtr, ytr, Xte)))


def main():
    print("[S6] loading rows + refs...")
    df = load_and_prep()
    df = restrict_to_common_23(df)
    df = df[df["arm"] == "apo"].copy()
    df["ligand_role"] = df["ligand_role"].astype(str)
    df = df[df["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    df["_label"] = (df["ligand_role"] == "full_agonist").astype(int)
    df["backbone"] = df["backbone"].astype(str).str.lower()

    try:
        lig_set = pd.read_csv(LIGAND_SET_TIER3, low_memory=False)
    except Exception:
        lig_set = pd.read_csv(LIGAND_SET_TIER3, on_bad_lines="skip", engine="python")
    ref_set = pd.read_csv(REF_SET_CSV, low_memory=False)

    # Per-receptor chemotype = full_agonist's ligand_type
    agon = lig_set[lig_set["ligand_role"] == "full_agonist"] if "ligand_role" in lig_set.columns else lig_set
    lt_col = "ligand_type" if "ligand_type" in agon.columns else None
    chemotype = {}
    if lt_col:
        for _, r in agon.iterrows():
            chemotype[str(r["receptor_slug"]).upper()] = str(r[lt_col]).lower()

    # S6a — chemotype fold-transfer.
    s6a = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        bb_df = df[df["backbone"] == bb].copy()
        sm_recs = [r for r in bb_df["receptor_slug"].str.upper().unique() if chemotype.get(r, "").startswith("small")]
        pep_recs = [r for r in bb_df["receptor_slug"].str.upper().unique() if chemotype.get(r, "").startswith("pep")]
        sm_df = bb_df[bb_df["receptor_slug"].str.upper().isin(sm_recs)]
        pep_df = bb_df[bb_df["receptor_slug"].str.upper().isin(pep_recs)]
        s6a[bb] = {
            "n_sm_recs": len(sm_recs), "n_pep_recs": len(pep_recs),
            "sm_to_pep_auroc": transfer_auroc(sm_df, pep_df, FEATURES_III),
            "pep_to_sm_auroc": transfer_auroc(pep_df, sm_df, FEATURES_III),
        }

    # S6b — cutoff transfer (best-effort: read v1 stratification for pre/post lists per bb)
    s6b = {}
    try:
        cutoff = json.loads(CUTOFF_JSON.read_text())
    except Exception:
        cutoff = None
    if cutoff and "per_backbone" in cutoff:
        for bb, d in cutoff.get("per_backbone", {}).items():
            pre = [r.upper() for r in d.get("pre_cutoff_receptors", [])]
            post = [r.upper() for r in d.get("post_cutoff_receptors", [])]
            bb_df = df[df["backbone"] == bb.lower()]
            pre_df = bb_df[bb_df["receptor_slug"].str.upper().isin(pre)]
            post_df = bb_df[bb_df["receptor_slug"].str.upper().isin(post)]
            s6b[bb] = {
                "n_pre_recs": len(pre), "n_post_recs": len(post),
                "n_pre_rows": int(len(pre_df)), "n_post_rows": int(len(post_df)),
                "pre_to_post_auroc": transfer_auroc(pre_df, post_df, FEATURES_III),
                "post_to_pre_auroc": transfer_auroc(post_df, pre_df, FEATURES_III),
            }
    else:
        s6b = {"note": "cutoff stratification JSON not found or has different structure"}

    # S6c — curation-availability bias
    # Compare 23 included vs 17 excluded (from Tier 3 40-panel)
    tier3_panel = pd.read_csv(REPO / "refs/tier3_panel.csv")
    all_40 = set(tier3_panel["receptor_slug"].str.upper())
    incl_23 = set(df["receptor_slug"].str.upper().unique())
    excl_17 = all_40 - incl_23

    # count active-reference PDBs per receptor as a proxy for "coverage"
    ref_active = ref_set[ref_set["role"] == "active"].copy()
    n_active_per_rec = ref_active.groupby(ref_active["receptor_slug"].str.upper()).size().to_dict()

    incl_counts = [n_active_per_rec.get(r, 0) for r in incl_23]
    excl_counts = [n_active_per_rec.get(r, 0) for r in excl_17]
    s6c = {
        "n_included_receptors": len(incl_23),
        "n_excluded_receptors": len(excl_17),
        "included_receptors": sorted(incl_23),
        "excluded_receptors": sorted(excl_17),
        "included_mean_active_refs": float(np.mean(incl_counts)) if incl_counts else float("nan"),
        "excluded_mean_active_refs": float(np.mean(excl_counts)) if excl_counts else float("nan"),
        "included_median_active_refs": float(np.median(incl_counts)) if incl_counts else float("nan"),
        "excluded_median_active_refs": float(np.median(excl_counts)) if excl_counts else float("nan"),
    }

    # S6d — per-row anti-memorization
    # Read bound_pdb from manifest (already joined into rows via load_and_prep? check)
    # We need ligand_bound_pdb per row. Load manifest.
    manifest = pd.read_csv(REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv", low_memory=False)
    mi = manifest.set_index("prediction_path")
    df["_bound_pdb"] = df["input_path"].map(mi["ligand_bound_pdb"].to_dict()).fillna("").astype(str).str.upper()

    # Get active-ref PDB per receptor from reference_set.csv
    active_ref_pdb = {}
    for _, r in ref_set.iterrows():
        if str(r.get("role", "")).lower() == "active":
            active_ref_pdb.setdefault(str(r["receptor_slug"]).upper(), str(r.get("pdb_id", "")).upper())

    df["_recallable"] = df.apply(
        lambda r: (r["_bound_pdb"] == active_ref_pdb.get(r["receptor_slug"].upper(), ""))
        if r["ligand_role"] == "full_agonist" else False,
        axis=1,
    )

    s6d = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        bb_df = df[df["backbone"] == bb].copy()
        # LORO with recallable stratifier: per receptor, are they recallable at all?
        # A receptor is "recallable" if its agonist_bound_pdb == active_ref_pdb.
        recallable_recs = set(
            bb_df[(bb_df["ligand_role"] == "full_agonist") & bb_df["_recallable"]]["receptor_slug"].str.upper()
        )
        r_df = bb_df[bb_df["receptor_slug"].str.upper().isin(recallable_recs)]
        m_df = bb_df[~bb_df["receptor_slug"].str.upper().isin(recallable_recs)]
        s6d[bb] = {
            "n_recallable_recs": len(recallable_recs),
            "n_must_generalise_recs": bb_df["receptor_slug"].str.upper().nunique() - len(recallable_recs),
            "recallable_within_stratum_auroc": transfer_auroc(r_df, r_df, FEATURES_III) if len(recallable_recs) > 3 else float("nan"),
            "must_gen_within_stratum_auroc": transfer_auroc(m_df, m_df, FEATURES_III) if bb_df["receptor_slug"].str.upper().nunique() - len(recallable_recs) > 3 else float("nan"),
            "recallable_to_must_gen_auroc": transfer_auroc(r_df, m_df, FEATURES_III) if r_df["receptor_slug"].str.upper().nunique() > 3 and m_df["receptor_slug"].str.upper().nunique() > 3 else float("nan"),
            "must_gen_to_recallable_auroc": transfer_auroc(m_df, r_df, FEATURES_III) if r_df["receptor_slug"].str.upper().nunique() > 3 and m_df["receptor_slug"].str.upper().nunique() > 3 else float("nan"),
        }

    report = {
        "task": "S6_generalization",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "s6a_chemotype_transfer": s6a,
        "s6b_cutoff_transfer": s6b,
        "s6c_curation_bias": s6c,
        "s6d_per_row_antimemorization": s6d,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"wrote {OUT.relative_to(REPO)}")

    print()
    print("=" * 70)
    print("S6a — chemotype fold-transfer AUROC")
    for bb, d in s6a.items():
        print(f"  {bb:<10} sm→pep={d['sm_to_pep_auroc']:.3f}  pep→sm={d['pep_to_sm_auroc']:.3f}  (n_sm={d['n_sm_recs']}, n_pep={d['n_pep_recs']})")
    print()
    print("S6b — cutoff transfer")
    if isinstance(s6b, dict) and "note" not in s6b:
        for bb, d in s6b.items():
            print(f"  {bb:<10} pre→post={d.get('pre_to_post_auroc', float('nan')):.3f}  post→pre={d.get('post_to_pre_auroc', float('nan')):.3f}  (n_pre={d.get('n_pre_recs', 0)}, n_post={d.get('n_post_recs', 0)})")
    else:
        print(f"  {s6b.get('note', 'skipped')}")
    print()
    print("S6c — curation bias")
    print(f"  Included (n={s6c['n_included_receptors']}): mean active refs = {s6c['included_mean_active_refs']:.2f}")
    print(f"  Excluded (n={s6c['n_excluded_receptors']}): mean active refs = {s6c['excluded_mean_active_refs']:.2f}")
    print()
    print("S6d — per-row anti-memorization AUROC")
    for bb, d in s6d.items():
        print(f"  {bb:<10} recallable(n={d['n_recallable_recs']})→must_gen: {d['recallable_to_must_gen_auroc']:.3f}  "
              f"must_gen(n={d['n_must_generalise_recs']})→recallable: {d['must_gen_to_recallable_auroc']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
