#!/usr/bin/env python3
"""S7 (ceiling + fold-integrity confound) + S8 (applicability domain).

Pre-registered against
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`.

S7 §7a (permutation nulls) already integrated in S1. This script covers:
  S7b — ceiling on 9 self-reference receptors alone
  S7c — fold-integrity confound (covariate control + fold-filter subset)

S8 — per-receptor AUROC distribution + predictor correlations + domain statement.
"""
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

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s7_s8_ceiling_domain.json"

FOLD_INTEGRITY_COLS = [
    "d_dry_sidechain_r350cz_e630oe1",
    "d_npxxy_y558_y753_ca",
]


def loro(sub: pd.DataFrame, features: list[str]) -> tuple[float, dict]:
    receptors = sorted(sub["receptor_slug"].str.upper().unique())
    all_s = []; all_y = []
    per_rec = {}
    for held in receptors:
        tr = sub[sub["receptor_slug"].str.upper() != held]
        te = sub[sub["receptor_slug"].str.upper() == held]
        Xtr = tr[features].to_numpy(dtype=float); ytr = tr["_label"].to_numpy(dtype=int)
        Xte = te[features].to_numpy(dtype=float); yte = te["_label"].to_numpy(dtype=int)
        m = np.isfinite(Xtr).all(axis=1); Xtr = Xtr[m]; ytr = ytr[m]
        m2 = np.isfinite(Xte).all(axis=1); Xte = Xte[m2]; yte = yte[m2]
        if len(np.unique(ytr)) < 2 or len(Xte) == 0:
            continue
        s = _fit_predict_logreg(Xtr, ytr, Xte)
        all_s.append(s); all_y.append(yte)
        per_rec[held] = float(_auroc(yte, s))
    if not all_s:
        return float("nan"), {}
    return float(_auroc(np.concatenate(all_y), np.concatenate(all_s))), per_rec


def spearman(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3: return float("nan")
    ra = pd.Series(a[m]).rank().to_numpy()
    rb = pd.Series(b[m]).rank().to_numpy()
    if np.std(ra) == 0 or np.std(rb) == 0: return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    print("[S7/S8] loading data...")
    df_full = load_and_prep()
    df_common = restrict_to_common_23(df_full)
    df_common = df_common[df_common["arm"] == "apo"].copy()
    df_common["ligand_role"] = df_common["ligand_role"].astype(str)
    df_common = df_common[df_common["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    df_common["_label"] = (df_common["ligand_role"] == "full_agonist").astype(int)
    df_common["backbone"] = df_common["backbone"].astype(str).str.lower()

    df_no_selfref = df_common[~df_common["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()
    df_selfref_only = df_common[df_common["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()

    # -----------------------------------------------------------
    # S7b — ceiling on 9 self-reference receptors
    # -----------------------------------------------------------
    s7b = {}
    print("[S7b] ceiling on 9 self-ref receptors, apo × F_iii")
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_selfref_only[df_selfref_only["backbone"] == bb].copy()
        pooled, per_rec = loro(sub, FEATURES_III)
        s7b[bb] = {"pooled_auroc": pooled, "n_receptors": int(sub["receptor_slug"].nunique()),
                   "per_receptor_auroc": per_rec}
        print(f"  {bb:<10} ceiling AUROC = {pooled:.3f}")

    # -----------------------------------------------------------
    # S7c(1) — covariate control: add fold-integrity anchors to F_iii
    # -----------------------------------------------------------
    print("[S7c(1)] adding fold-integrity covariates to F_iii, re-running LORO on 14 recs")
    s7c_cov = {}
    fold_cols_present = [c for c in FOLD_INTEGRITY_COLS if c in df_no_selfref.columns]
    features_with_cov = FEATURES_III + fold_cols_present
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_no_selfref[df_no_selfref["backbone"] == bb].copy()
        base, _ = loro(sub, FEATURES_III)
        cov_auc, _ = loro(sub, features_with_cov)
        s7c_cov[bb] = {"base_f_iii": base, "with_fold_covariates": cov_auc, "delta": cov_auc - base}
        print(f"  {bb:<10} base={base:.3f}  +cov={cov_auc:.3f}  Δ={cov_auc - base:+.3f}")

    # -----------------------------------------------------------
    # S7c(2) — fold-integrity filter: recompute on rows passing fold-integrity
    # thresholds. Approximate: DRY < 7 Å (rough threshold; check with axis analysis
    # if in doubt) AND non-NaN NPxxY.
    # -----------------------------------------------------------
    print("[S7c(2)] fold-integrity filter subset")
    s7c_filt = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_no_selfref[df_no_selfref["backbone"] == bb].copy()
        for c in fold_cols_present:
            sub[c] = pd.to_numeric(sub[c], errors="coerce")
        # Simple filter: all fold-integrity cols finite. (Threshold-based filtering
        # would need per-receptor thresholds; use finite-only as a coarse proxy.)
        m = np.ones(len(sub), dtype=bool)
        for c in fold_cols_present:
            m &= np.isfinite(sub[c].to_numpy(dtype=float))
        filt = sub[m].copy()
        auc, _ = loro(filt, FEATURES_III)
        s7c_filt[bb] = {"n_pass": int(len(filt)), "n_total": int(len(sub)),
                        "filtered_auroc": auc}
        print(f"  {bb:<10} n_pass={len(filt)}/{len(sub)}  filtered AUROC={auc:.3f}")

    # -----------------------------------------------------------
    # S8a — per-receptor AUROC distribution from S1 output
    # -----------------------------------------------------------
    s1_out = json.loads(
        (REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s1_loro_classifier.json").read_text()
    )
    s8a = {}
    for v in s1_out["variants"]:
        if v.get("variant") == "C_no_selfref_apo" and v.get("feature_set") == "F_iii_pocket_plus_axes":
            bb = v["backbone"]
            aurocs = list(v["per_receptor_auroc"].values())
            s8a[bb] = {
                "min": float(np.min(aurocs)),
                "q25": float(np.percentile(aurocs, 25)),
                "median": float(np.median(aurocs)),
                "q75": float(np.percentile(aurocs, 75)),
                "max": float(np.max(aurocs)),
                "n_inverted": sum(1 for a in aurocs if a < 0.3),
                "inverted_receptors": [r for r, a in v["per_receptor_auroc"].items() if a < 0.3],
                "n_perfect": sum(1 for a in aurocs if a >= 0.9),
                "perfect_receptors": [r for r, a in v["per_receptor_auroc"].items() if a >= 0.9],
                "per_receptor": v["per_receptor_auroc"],
            }

    # -----------------------------------------------------------
    # S8b — predictor correlations for per-receptor AUROC
    # -----------------------------------------------------------
    ref_set = pd.read_csv(REPO / "refs/reference_set.csv", low_memory=False)
    # deposition count per receptor from ref_set (n rows per receptor)
    n_refs_per_rec = ref_set.groupby(ref_set["receptor_slug"].str.upper()).size().to_dict()
    # Chemotype
    try:
        lig_set = pd.read_csv(REPO / "refs/ligand_set_tier3.csv", on_bad_lines="skip", engine="python")
        chemotype = {}
        for _, r in lig_set.iterrows():
            if str(r.get("ligand_role", "")) == "full_agonist":
                chemotype[str(r["receptor_slug"]).upper()] = str(r.get("ligand_type", "")).lower()
    except Exception:
        chemotype = {}
    # Coupling class
    try:
        coupling = pd.read_csv(REPO / "refs/gpcr_coupling.csv", low_memory=False)
        coupling_map = {}
        for _, r in coupling.iterrows():
            coupling_map[str(r["receptor_slug"]).upper()] = str(r.get("primary_coupling", ""))
    except Exception:
        coupling_map = {}

    s8b = {}
    for bb, d in s8a.items():
        per_rec = d["per_receptor"]
        recs = list(per_rec.keys())
        aurocs = np.array([per_rec[r] for r in recs])
        # deposition count
        dep = np.array([n_refs_per_rec.get(r, 0) for r in recs], dtype=float)
        # peptide vs sm
        is_pep = np.array([1.0 if chemotype.get(r, "").startswith("pep") else 0.0 for r in recs])
        # coupling categorical: numeric via distinct label indices
        cls = sorted(set(coupling_map.get(r, "") for r in recs))
        cls_idx = {c: i for i, c in enumerate(cls)}
        coup_num = np.array([cls_idx.get(coupling_map.get(r, ""), -1) for r in recs], dtype=float)

        s8b[bb] = {
            "spearman_auroc_vs_deposition_count": spearman(aurocs, dep),
            "spearman_auroc_vs_is_peptide": spearman(aurocs, is_pep),
            "spearman_auroc_vs_coupling_categorical": spearman(aurocs, coup_num),
        }

    # -----------------------------------------------------------
    # S8c — domain statement (aggregated across backbones)
    # -----------------------------------------------------------
    inverted_all = set()
    perfect_all = set()
    for bb, d in s8a.items():
        inverted_all.update(d["inverted_receptors"])
        perfect_all.update(d["perfect_receptors"])
    s8c = {
        "reliably_classified_receptors_any_backbone": sorted(perfect_all),
        "systematically_inverted_receptors_any_backbone": sorted(inverted_all),
        "domain_statement": (
            "The method reliably classifies (AUROC ≥ 0.9) on {p_n} receptors across "
            "backbones and systematically inverts (AUROC < 0.3) on {i_n} receptors "
            "(notably {i_r}). Best predictor of per-receptor performance: TBD from S8b."
        ).format(p_n=len(perfect_all), i_n=len(inverted_all), i_r=", ".join(sorted(inverted_all))),
    }

    report = {
        "task": "S7_S8_ceiling_domain",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "s7b_ceiling_self_reference_only": s7b,
        "s7c_covariate_control": s7c_cov,
        "s7c_fold_filter_subset": s7c_filt,
        "s8a_per_receptor_distribution": s8a,
        "s8b_predictor_correlations": s8b,
        "s8c_domain_statement": s8c,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"wrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 70)
    print("S7b ceiling AUROCs (9 self-ref recs, apo × F_iii):")
    for bb, d in s7b.items():
        print(f"  {bb:<10} {d['pooled_auroc']:.3f}")
    print()
    print("S7c covariate control (base F_iii vs +fold-integrity):")
    for bb, d in s7c_cov.items():
        print(f"  {bb:<10} base={d['base_f_iii']:.3f}  +cov={d['with_fold_covariates']:.3f}  Δ={d['delta']:+.3f}")
    print()
    print("S8a per-receptor AUROC distribution (F_iii apo × 15 recs):")
    for bb, d in s8a.items():
        print(f"  {bb:<10} min={d['min']:.3f} med={d['median']:.3f} max={d['max']:.3f} n_perfect={d['n_perfect']} n_inv={d['n_inverted']}")
    print()
    print("S8b predictor correlations (Spearman ρ):")
    for bb, d in s8b.items():
        print(f"  {bb:<10} dep_count={d['spearman_auroc_vs_deposition_count']:+.3f}  is_pep={d['spearman_auroc_vs_is_peptide']:+.3f}  coup={d['spearman_auroc_vs_coupling_categorical']:+.3f}")
    print()
    print("S8c domain:")
    print(f"  {s8c['domain_statement']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
