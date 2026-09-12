#!/usr/bin/env python3
"""S1 (centerpiece) — LORO ligand-class classifier on Block C tier 3.

Pre-registered against
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`
(committed at e63692f BEFORE this script computed any evaluation number).

Task: given the continuous pocket-geometry features of a single predicted
structure, classify the ligand as full_agonist vs neutral_antagonist.

Three feature sets:
  (i)   Δ = pocket_ca_rmsd_active − pocket_ca_rmsd_inactive
  (ii)  (i) + pocket_ca_rmsd, pocket_sidechain_rmsd_active,
             pocket_sidechain_rmsd_inactive, w648_chi1
  (iii) (ii) + d_npxxy_y558_y753_oh, d_gpcrdb_tm6_tilt_246_637_ca,
              d_tm6_r350_r630_ca  (as continuous values, not thresholded)

Models:
  Feature (i): single threshold, Youden's J selected on training fold.
  Features (ii), (iii): L2 logistic regression, standardized inside fold.

Cross-validation: LORO — 23 folds, one receptor held out.

Permutation null: 1000 permutations, ligand-class labels shuffled WITHIN
receptor before running the full LORO pipeline.

Runs:
  - all 23 receptors (both arms combined)
  - apo arm only, all 23 receptors
  - apo arm only, 14 receptors (9 self-reference-excluded)   <-- KILL-S1
  - 3-class {agonist, antag, decoy_lig} on all 23 (report confusion matrix)

KILL-S1 (pre-registered, binding):
  If LORO AUROC on apo arm × self-ref-excluded < 0.65 on ALL four backbones,
  report NO_PROSPECTIVE_CLASSIFIER and stop the method-extraction line.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_JSON = OUT_DIR / "s1_loro_classifier.json"

# From T1 addendum — 9 receptors that are 100 % self-reference on antag_inactive.
SELF_REF_RECEPTORS = frozenset({
    "ACM4", "ADRB2", "CCR5", "CNR1", "CNR2",
    "DRD3", "NPY1R", "OPRD", "OPRK",
})

# KILL-S1 threshold (pre-registered).
KILL_S1_AUROC = 0.65


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _to_float(x) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


# ============================================================
# Feature extraction
# ============================================================

FEATURES_I = ["_delta"]
FEATURES_II = FEATURES_I + [
    "pocket_ca_rmsd",
    "pocket_sidechain_rmsd_active",
    "pocket_sidechain_rmsd_inactive",
    "w648_chi1",
]
FEATURES_III = FEATURES_II + [
    "d_npxxy_y558_y753_oh",
    "d_gpcrdb_tm6_tilt_246_637_ca",
    "d_tm6_r350_r630_ca",
]


def build_features(rows: pd.DataFrame) -> pd.DataFrame:
    """Compute Δ and cast feature columns to numeric."""
    df = rows.copy()
    df["_delta"] = pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce") \
                   - pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce")
    numeric_cols = list(dict.fromkeys(FEATURES_III + [
        "pocket_ca_rmsd_active", "pocket_ca_rmsd_inactive",
    ]))
    for c in numeric_cols:
        if c in df.columns and c != "_delta":
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ============================================================
# Simple classifier fits (no sklearn — vanilla numpy so no version drift)
# ============================================================


def _youden_j_threshold(y_true: np.ndarray, scores: np.ndarray) -> float:
    """Threshold that maximizes Youden's J = TPR − FPR on the training data.

    y_true is the LARGE class (1 = agonist, 0 = antag).
    scores: higher score → predict positive.
    """
    if len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return 0.0
    sc = np.asarray(scores)
    yt = np.asarray(y_true)
    order = np.argsort(sc, kind="mergesort")[::-1]  # descending
    sc = sc[order]; yt = yt[order]
    P = int((yt == 1).sum()); N = int((yt == 0).sum())
    if P == 0 or N == 0:
        return 0.0
    tp = np.cumsum(yt == 1); fp = np.cumsum(yt == 0)
    tpr = tp / P; fpr = fp / N
    j = tpr - fpr
    best = int(np.argmax(j))
    return float(sc[best])


def _auroc(y_true: np.ndarray, scores: np.ndarray) -> float:
    """AUROC via Mann-Whitney U with tie-adjusted average ranks."""
    y = np.asarray(y_true).astype(bool)
    s = np.asarray(scores, dtype=float)
    if len(np.unique(y)) < 2:
        return float("nan")
    n_pos = int(y.sum())
    n_neg = int((~y).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    # Compute tie-adjusted average ranks over the full score vector.
    order = np.argsort(s, kind="mergesort")
    s_sorted = s[order]
    ranks_sorted = np.empty(len(s), dtype=float)
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # 1-based average rank
        ranks_sorted[i:j + 1] = avg
        i = j + 1
    ranks = np.empty_like(ranks_sorted)
    ranks[order] = ranks_sorted
    r_pos_sum = float(ranks[y].sum())
    U = r_pos_sum - n_pos * (n_pos + 1) / 2.0
    return U / (n_pos * n_neg)


def _average_precision(y_true: np.ndarray, scores: np.ndarray) -> float:
    """Average precision (area under PR curve). Vanilla implementation."""
    y = np.asarray(y_true).astype(bool)
    s = np.asarray(scores, dtype=float)
    if len(np.unique(y)) < 2:
        return float("nan")
    order = np.argsort(s, kind="mergesort")[::-1]
    y = y[order]
    tp = np.cumsum(y)
    fp = np.cumsum(~y)
    precision = tp / np.maximum(tp + fp, 1)
    recall = tp / max(1, int(y.sum()))
    # Step-function AP.
    ap = 0.0
    prev_r = 0.0
    for p, r in zip(precision, recall):
        ap += p * (r - prev_r)
        prev_r = r
    return float(ap)


def _fit_predict_logreg(
    X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray,
    n_iter: int = 300, lr: float = 0.1, l2: float = 1.0,
) -> np.ndarray:
    """Numpy L2-regularized logistic regression via gradient descent.

    Standardization is done inside this function using train-fold statistics.
    Returns predicted decision-function scores on X_test (higher → class 1).
    """
    # Standardize using train stats.
    mu = np.nanmean(X_train, axis=0)
    sd = np.nanstd(X_train, axis=0)
    sd = np.where(sd < 1e-8, 1.0, sd)

    def _standardize(X):
        Xs = (X - mu) / sd
        return np.nan_to_num(Xs, nan=0.0, posinf=0.0, neginf=0.0)

    Xt = _standardize(X_train)
    Xv = _standardize(X_test)
    n_features = Xt.shape[1]
    # Prepend intercept.
    Xt = np.hstack([np.ones((Xt.shape[0], 1)), Xt])
    Xv = np.hstack([np.ones((Xv.shape[0], 1)), Xv])
    theta = np.zeros(n_features + 1)
    y = y_train.astype(float)
    n = len(y)
    for _ in range(n_iter):
        z = Xt @ theta
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = (Xt.T @ (p - y)) / n
        grad[1:] += (l2 / n) * theta[1:]  # do not regularize intercept
        theta -= lr * grad
    scores = Xv @ theta
    return scores


# ============================================================
# LORO evaluation with permutation null (batched)
# ============================================================


def loro_evaluate(
    df: pd.DataFrame,
    feature_names: list[str],
    label_col: str = "_label",
    model: str = "logreg",  # "logreg" or "threshold"
    rng_seed: int = 20260907,
    n_permutations: int = 1000,
) -> dict:
    """Run LORO on df. Fit + predict per fold. Return per-receptor + pooled
    metrics + permutation-null distribution.

    df must carry: label_col in {0, 1}, receptor_slug, and every feature.
    """
    receptors = sorted(df["receptor_slug"].str.upper().unique())
    obs_scores: dict[str, np.ndarray] = {}
    obs_labels: dict[str, np.ndarray] = {}

    for held_out in receptors:
        tr = df[df["receptor_slug"].str.upper() != held_out]
        te = df[df["receptor_slug"].str.upper() == held_out]
        if len(tr) == 0 or len(te) == 0:
            continue
        X_tr = tr[feature_names].to_numpy(dtype=float)
        X_te = te[feature_names].to_numpy(dtype=float)
        y_tr = tr[label_col].to_numpy(dtype=int)
        # NaN-safe: drop rows in train where any feature is NaN.
        mask_tr = np.isfinite(X_tr).all(axis=1)
        X_tr = X_tr[mask_tr]; y_tr = y_tr[mask_tr]
        if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
            continue

        if model == "logreg":
            s_te = _fit_predict_logreg(X_tr, y_tr, X_te)
        else:  # threshold on single feature
            th = _youden_j_threshold(y_tr, X_tr[:, 0])
            s_te = X_te[:, 0] - th  # positive → predict class 1

        obs_scores[held_out] = s_te
        obs_labels[held_out] = te[label_col].to_numpy(dtype=int)

    per_receptor_auroc = {
        r: _auroc(obs_labels[r], obs_scores[r]) for r in obs_labels
    }
    per_receptor_ap = {
        r: _average_precision(obs_labels[r], obs_scores[r]) for r in obs_labels
    }

    # Pooled: concat all held-out predictions.
    all_s = np.concatenate([obs_scores[r] for r in obs_labels])
    all_y = np.concatenate([obs_labels[r] for r in obs_labels])
    pooled_auroc = _auroc(all_y, all_s)
    pooled_ap = _average_precision(all_y, all_s)

    # Permutation null: shuffle labels WITHIN receptor, rerun LORO.
    rng = np.random.default_rng(rng_seed)
    null_pooled_auroc = np.empty(n_permutations)
    for p in range(n_permutations):
        df_perm = df.copy()
        # Shuffle labels within each receptor separately.
        for rec in receptors:
            m = df_perm["receptor_slug"].str.upper() == rec
            df_perm.loc[m, label_col] = rng.permutation(df_perm.loc[m, label_col].values)
        null_scores = []; null_labels = []
        for held_out in receptors:
            tr = df_perm[df_perm["receptor_slug"].str.upper() != held_out]
            te = df_perm[df_perm["receptor_slug"].str.upper() == held_out]
            if len(tr) == 0 or len(te) == 0:
                continue
            X_tr = tr[feature_names].to_numpy(dtype=float)
            X_te = te[feature_names].to_numpy(dtype=float)
            y_tr = tr[label_col].to_numpy(dtype=int)
            mask_tr = np.isfinite(X_tr).all(axis=1)
            X_tr = X_tr[mask_tr]; y_tr = y_tr[mask_tr]
            if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
                continue
            if model == "logreg":
                s_te = _fit_predict_logreg(X_tr, y_tr, X_te)
            else:
                th = _youden_j_threshold(y_tr, X_tr[:, 0])
                s_te = X_te[:, 0] - th
            null_scores.append(s_te)
            null_labels.append(te[label_col].to_numpy(dtype=int))
        if not null_scores:
            null_pooled_auroc[p] = float("nan")
            continue
        null_pooled_auroc[p] = _auroc(
            np.concatenate(null_labels), np.concatenate(null_scores)
        )

    null_clean = null_pooled_auroc[~np.isnan(null_pooled_auroc)]
    if len(null_clean) == 0:
        p_value = float("nan"); z = float("nan"); null_mean = float("nan")
        null_lo = float("nan"); null_hi = float("nan")
    else:
        # Permutation p-value: fraction of null ≥ observed.
        p_value = float(np.mean(null_clean >= pooled_auroc))
        null_mean = float(np.mean(null_clean))
        null_lo = float(np.percentile(null_clean, 2.5))
        null_hi = float(np.percentile(null_clean, 97.5))
        null_sd = float(np.std(null_clean))
        z = (pooled_auroc - null_mean) / null_sd if null_sd > 0 else float("nan")

    return {
        "n_receptors_evaluated": len(obs_labels),
        "per_receptor_auroc": per_receptor_auroc,
        "per_receptor_ap": per_receptor_ap,
        "pooled_auroc": pooled_auroc,
        "pooled_ap": pooled_ap,
        "null_permutation_n": int(n_permutations),
        "null_pooled_auroc_mean": null_mean,
        "null_pooled_auroc_2p5": null_lo,
        "null_pooled_auroc_97p5": null_hi,
        "permutation_p_value": p_value,
        "z_vs_null": z,
    }


# ============================================================
# Main
# ============================================================


def load_and_prep() -> pd.DataFrame:
    print("[S1] loading rows + manifest...")
    rows = pd.read_csv(ROWS_CSV, low_memory=False)
    manifest = pd.read_csv(MANIFEST_CSV, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    for col in ("ligand_role",):
        fb = rows.get(col, pd.Series([""] * len(rows)))
        rows[col] = rows["input_path"].map(m_idx[col].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(
        lambda p: "apo" if str(p).lower() == "apo" else "cognate"
    )
    df = build_features(rows)
    # Filter: Class A only, passed=True.
    m = (df["receptor_class"].fillna("").astype(str).str.upper() == "A")
    m &= (df["passed"].astype(str).str.lower() == "true")
    df = df[m].copy()
    df["receptor_slug"] = df["receptor_slug"].astype(str).str.upper()
    return df


def build_label(df: pd.DataFrame, positive: str, negative: str) -> pd.DataFrame:
    sub = df[df["ligand_role"].isin([positive, negative])].copy()
    sub["_label"] = (sub["ligand_role"] == positive).astype(int)
    return sub


def restrict_to_common_23(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only receptors that have both agonist and antagonist rows with
    non-NaN pocket_ca_rmsd_active/_inactive on both — matches the 2×2 common
    set logic in stage3a_2x2."""
    per_rec_valid = defaultdict(lambda: {"ag": False, "an": False})
    for _, r in df.iterrows():
        rec = r["receptor_slug"]
        role = r["ligand_role"]
        if math.isnan(_to_float(r.get("pocket_ca_rmsd_active"))) or math.isnan(_to_float(r.get("pocket_ca_rmsd_inactive"))):
            continue
        if role == "full_agonist":
            per_rec_valid[rec]["ag"] = True
        elif role in ("neutral_antagonist", "inverse_agonist"):
            per_rec_valid[rec]["an"] = True
    keep = {rec for rec, d in per_rec_valid.items() if d["ag"] and d["an"]}
    return df[df["receptor_slug"].isin(keep)].copy()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT_JSON))
    parser.add_argument("--n-permutations", type=int, default=200)  # 200 default for speed; user can request 1000
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df_all = load_and_prep()
    print(f"[S1] Class-A passed rows: {len(df_all)}")

    # Restrict to the 2×2 common set for pooled analysis.
    df_common = restrict_to_common_23(df_all)
    common_receptors = sorted(df_common["receptor_slug"].unique())
    print(f"[S1] receptors in 2×2 common set: {len(common_receptors)}")
    print(f"      {common_receptors}")

    results = {}

    # ------------------------------------------------------------
    # Primary runs across (backbone × arm × feature-set × exclusion)
    # ------------------------------------------------------------
    backbones = ["boltz", "chai", "of3", "protenix"]
    feature_sets = {
        "F_i_delta": FEATURES_I,
        "F_ii_pocket_family": FEATURES_II,
        "F_iii_pocket_plus_axes": FEATURES_III,
    }
    arms = ["both", "apo"]

    def run_variant(
        variant_name: str, subset: pd.DataFrame, backbone: str,
        arm: str, feature_set_name: str, feature_names: list[str],
    ) -> dict:
        sub = subset[subset["backbone"].str.lower() == backbone].copy()
        if arm != "both":
            sub = sub[sub["arm"] == arm].copy()
        # Positive = full_agonist; Negative = neutral_antagonist.
        pair = build_label(sub, "full_agonist", "neutral_antagonist")
        if len(pair) < 200 or pair["receptor_slug"].nunique() < 10:
            return {
                "variant": variant_name, "backbone": backbone, "arm": arm,
                "feature_set": feature_set_name,
                "reason": "insufficient_data",
                "n_rows": int(len(pair)),
                "n_receptors": int(pair["receptor_slug"].nunique()),
            }
        model = "threshold" if feature_set_name == "F_i_delta" else "logreg"
        r = loro_evaluate(pair, feature_names, model=model,
                          n_permutations=args.n_permutations)
        r.update({
            "variant": variant_name, "backbone": backbone, "arm": arm,
            "feature_set": feature_set_name,
            "n_rows": int(len(pair)),
            "n_receptors": int(pair["receptor_slug"].nunique()),
            "model": model,
        })
        return r

    variants = []

    # Variant A: all 23 receptors, both arms.
    print("[S1 A] all-23, both arms")
    for bb in backbones:
        for fs_name, fs_cols in feature_sets.items():
            print(f"  {bb} {fs_name}...", flush=True)
            variants.append(run_variant("A_all23_botharms", df_common, bb, "both", fs_name, fs_cols))

    # Variant B: all 23 receptors, apo arm only.
    print("[S1 B] all-23, apo arm only")
    for bb in backbones:
        for fs_name, fs_cols in feature_sets.items():
            print(f"  {bb} {fs_name}...", flush=True)
            variants.append(run_variant("B_all23_apo", df_common, bb, "apo", fs_name, fs_cols))

    # Variant C (KILL-S1): 14 receptors, apo arm only, self-ref-excluded.
    print("[S1 C] self-ref-excluded (14 recs), apo arm  ← KILL-S1")
    df_common_no_selfref = df_common[
        ~df_common["receptor_slug"].isin(SELF_REF_RECEPTORS)
    ].copy()
    print(f"      receptors: {sorted(df_common_no_selfref['receptor_slug'].unique())}")
    for bb in backbones:
        for fs_name, fs_cols in feature_sets.items():
            print(f"  {bb} {fs_name}...", flush=True)
            variants.append(run_variant("C_no_selfref_apo", df_common_no_selfref, bb, "apo", fs_name, fs_cols))

    # ------------------------------------------------------------
    # KILL-S1 verdict.
    # ------------------------------------------------------------
    kill_s1_results = [v for v in variants if v.get("variant") == "C_no_selfref_apo"]
    per_backbone_best_auroc: dict[str, float] = {}
    for v in kill_s1_results:
        bb = v["backbone"]
        if "pooled_auroc" not in v:
            continue
        cur = per_backbone_best_auroc.get(bb, -1.0)
        if v["pooled_auroc"] > cur:
            per_backbone_best_auroc[bb] = v["pooled_auroc"]
    n_backbones_above = sum(
        1 for a in per_backbone_best_auroc.values() if a >= KILL_S1_AUROC
    )
    kill_s1_fired = (n_backbones_above == 0)
    kill_s1_verdict = (
        "KILL_S1_FIRED_NO_PROSPECTIVE_CLASSIFIER" if kill_s1_fired
        else f"KILL_S1_DID_NOT_FIRE ({n_backbones_above}/4 backbones ≥ 0.65)"
    )

    # ------------------------------------------------------------
    # Report.
    # ------------------------------------------------------------
    report = {
        "task": "S1_loro_classifier",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
        },
        "prereg_git_sha": "e63692f",
        "kill_s1_threshold": KILL_S1_AUROC,
        "n_permutations": args.n_permutations,
        "n_common_receptors": len(common_receptors),
        "common_receptors": common_receptors,
        "self_ref_receptors": sorted(SELF_REF_RECEPTORS),
        "variants": variants,
        "per_backbone_best_auroc_kill_s1_row": per_backbone_best_auroc,
        "kill_s1_verdict": kill_s1_verdict,
        "kill_s1_fired": kill_s1_fired,
    }

    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[S1] wrote {Path(args.out).relative_to(REPO)}")
    print()
    print("=" * 80)
    print("S1 SUMMARY — KILL-S1 row (apo × self-ref-excluded)")
    print("=" * 80)
    print(f"{'backbone':<10} {'feature_set':<20} {'n_rcp':>5} {'n_row':>6} "
          f"{'auroc':>7} {'null_mean':>9} {'p_perm':>8}")
    for v in kill_s1_results:
        if "pooled_auroc" not in v:
            print(f"  {v.get('backbone', '?'):<10} SKIP ({v.get('reason', 'unknown')})")
            continue
        print(
            f"{v['backbone']:<10} {v['feature_set']:<20} "
            f"{v['n_receptors']:>5} {v['n_rows']:>6} "
            f"{v['pooled_auroc']:>7.3f} {v['null_pooled_auroc_mean']:>9.3f} "
            f"{v['permutation_p_value']:>8.3f}"
        )
    print()
    print("Per-backbone BEST auroc on KILL-S1 row:")
    for bb, a in per_backbone_best_auroc.items():
        marker = "≥0.65" if a >= KILL_S1_AUROC else "<0.65"
        print(f"  {bb:<10} {a:.3f}  [{marker}]")
    print()
    print(f"KILL-S1 verdict: {kill_s1_verdict}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
