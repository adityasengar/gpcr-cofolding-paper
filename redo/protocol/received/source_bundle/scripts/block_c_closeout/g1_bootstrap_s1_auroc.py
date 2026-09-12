#!/usr/bin/env python3
"""G1 — receptor-boot + cluster-boot CI on S1 KILL-S1-row AUROC.

Focused on the abstract number: F_iii × apo × self-ref-excluded (15
receptors) × 4 backbones.

Method:
 - Load rows.tier3.v2 + build features (same as s1_loro_classifier.py).
 - Restrict to 15-receptor S1 set × apo × {full_agonist, neutral_antagonist}
   × per-backbone.
 - For each of `n_iter` iterations, sample 15 receptors WITH replacement.
 - For each unique receptor in the sample, run LORO fold (train on the
   UNIQUE others in the sample; evaluate on the receptor).
 - Compute pooled AUROC on the sample (concat scores across drawn
   receptors, with a receptor's rows entering once per its multiplicity).
 - Repeat and report [2.5, 97.5] percentile CI on pooled AUROC.

Cluster-boot: same procedure but resample paralog CLUSTERS, then draw
all receptors in each drawn cluster. Cluster map from Block B's paralog
clusters (26 clusters over 40 Class A + Class B + Class F receptors).

Permutation null (already in s1_loro_classifier.json for reference).

Runtime note: 15 folds × ~4600 rows each with 300-iter GD × 4 backbones
× 300 iters = feasible in ~5-10 min.
"""
from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
CLUSTERS_CSV = REPO / "experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification"
OUT_JSON = OUT_DIR / "g1_bootstrap_s1_auroc.json"

BACKBONES = ["boltz", "chai", "of3", "protenix"]
S1_15 = ["5HT1B", "5HT5A", "AA1R", "AA2AR", "ACM2", "AGTR1", "CXCR2", "CXCR4",
         "EDNRB", "GRPR", "LPAR1", "LT4R1", "MCHR1", "NPY2R", "OPRX"]
FEATURES_III = [
    "_delta", "pocket_ca_rmsd", "pocket_sidechain_rmsd_active",
    "pocket_sidechain_rmsd_inactive", "w648_chi1",
    "d_npxxy_y558_y753_oh", "d_gpcrdb_tm6_tilt_246_637_ca", "d_tm6_r350_r630_ca",
]
N_ITER = 500
N_PERM = 200
RNG_SEED = 20260910


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _auroc(y, s):
    y = np.asarray(y).astype(bool); s = np.asarray(s, dtype=float)
    if len(np.unique(y)) < 2:
        return float("nan")
    n_pos = int(y.sum()); n_neg = int((~y).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(s, kind="mergesort")
    s_sorted = s[order]
    ranks_sorted = np.empty(len(s), dtype=float)
    i = 0
    while i < len(s_sorted):
        j = i
        while j + 1 < len(s_sorted) and s_sorted[j + 1] == s_sorted[i]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        ranks_sorted[i:j+1] = avg
        i = j + 1
    ranks = np.empty_like(ranks_sorted)
    ranks[order] = ranks_sorted
    r_pos = float(ranks[y].sum())
    U = r_pos - n_pos * (n_pos + 1) / 2.0
    return U / (n_pos * n_neg)


def _fit_predict_logreg(X_train, y_train, X_test, n_iter=300, lr=0.1, l2=1.0):
    mu = np.nanmean(X_train, axis=0)
    sd = np.nanstd(X_train, axis=0)
    sd = np.where(sd < 1e-8, 1.0, sd)
    def std(X):
        Xs = (X - mu) / sd
        return np.nan_to_num(Xs, nan=0.0, posinf=0.0, neginf=0.0)
    Xt = std(X_train); Xv = std(X_test)
    nf = Xt.shape[1]
    Xt = np.hstack([np.ones((Xt.shape[0], 1)), Xt])
    Xv = np.hstack([np.ones((Xv.shape[0], 1)), Xv])
    theta = np.zeros(nf + 1)
    y = y_train.astype(float); n = len(y)
    for _ in range(n_iter):
        z = Xt @ theta
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = (Xt.T @ (p - y)) / n
        grad[1:] += (l2 / n) * theta[1:]
        theta -= lr * grad
    return Xv @ theta


def build_features(rows: pd.DataFrame) -> pd.DataFrame:
    df = rows.copy()
    df["_delta"] = (pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce")
                    - pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce"))
    for c in FEATURES_III:
        if c in df.columns and c != "_delta":
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def load_and_prep():
    rows = pd.read_csv(ROWS_CSV, low_memory=False)
    manifest = pd.read_csv(MANIFEST_CSV, low_memory=False)
    m_idx = manifest.set_index("prediction_path")
    rows["backbone"] = rows["input_path"].map(m_idx["backbone"].to_dict()).fillna("")
    rows["partner_type"] = rows["input_path"].map(m_idx["partner_type"].to_dict()).fillna("")
    for col in ("ligand_role",):
        fb = rows.get(col, pd.Series([""] * len(rows)))
        rows[col] = rows["input_path"].map(m_idx[col].to_dict()).fillna(fb)
    rows["arm"] = rows["partner_type"].apply(lambda p: "apo" if str(p).lower() == "apo" else "cognate")
    df = build_features(rows)
    m = (df["receptor_class"].fillna("").astype(str).str.upper() == "A")
    m &= (df["passed"].astype(str).str.lower() == "true")
    df = df[m].copy()
    df["receptor_slug"] = df["receptor_slug"].astype(str).str.upper()
    return df


def prepare_subsets(df: pd.DataFrame) -> dict:
    """Return per-backbone dict of DataFrame subsets: 15 recs × apo × {agonist, antag}."""
    subs = {}
    for bb in BACKBONES:
        sub = df[(df["backbone"].str.lower() == bb) & (df["arm"] == "apo")].copy()
        sub = sub[sub["receptor_slug"].isin(S1_15)]
        sub = sub[sub["ligand_role"].isin(["full_agonist", "neutral_antagonist"])]
        sub["_label"] = (sub["ligand_role"] == "full_agonist").astype(int)
        subs[bb] = sub
    return subs


def loro_pooled_auroc(df_sub: pd.DataFrame, unique_receptors: list[str],
                     multiplicity: dict[str, int]) -> float:
    """LORO within the unique_receptors set; aggregate weighted by multiplicity."""
    obs_scores = []; obs_labels = []
    for held in unique_receptors:
        tr = df_sub[(df_sub["receptor_slug"].isin(unique_receptors)) & (df_sub["receptor_slug"] != held)]
        te = df_sub[df_sub["receptor_slug"] == held]
        if len(tr) == 0 or len(te) == 0:
            continue
        X_tr = tr[FEATURES_III].to_numpy(dtype=float)
        X_te = te[FEATURES_III].to_numpy(dtype=float)
        y_tr = tr["_label"].to_numpy(dtype=int)
        mask = np.isfinite(X_tr).all(axis=1)
        X_tr = X_tr[mask]; y_tr = y_tr[mask]
        if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
            continue
        s_te = _fit_predict_logreg(X_tr, y_tr, X_te)
        y_te = te["_label"].to_numpy(dtype=int)
        # Replicate scores/labels per multiplicity
        m = multiplicity.get(held, 1)
        for _ in range(m):
            obs_scores.append(s_te.copy())
            obs_labels.append(y_te.copy())
    if not obs_scores:
        return float("nan")
    s = np.concatenate(obs_scores); y = np.concatenate(obs_labels)
    return _auroc(y, s)


def load_clusters() -> dict[str, str]:
    """Load paralog clusters. Return receptor -> cluster_id."""
    if not CLUSTERS_CSV.exists():
        return {}
    df = pd.read_csv(CLUSTERS_CSV)
    # Expected columns: receptor + cluster (or similar)
    rec_col = next((c for c in df.columns if "receptor" in c.lower()), None)
    clu_col = next((c for c in df.columns if "cluster" in c.lower()), None)
    if not rec_col or not clu_col:
        return {}
    return dict(zip(df[rec_col].astype(str).str.upper(), df[clu_col].astype(str)))


def receptor_bootstrap_ci(df_sub: pd.DataFrame, n_iter: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    recs = sorted(df_sub["receptor_slug"].unique())
    n = len(recs)
    aurocs = np.empty(n_iter)
    t0 = time.time()
    for i in range(n_iter):
        # Draw n with replacement
        drawn = rng.choice(recs, size=n, replace=True)
        mult = defaultdict(int)
        for r in drawn:
            mult[r] += 1
        uniq = sorted(mult.keys())
        aurocs[i] = loro_pooled_auroc(df_sub, uniq, mult)
        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"    boot {i+1}/{n_iter}  elapsed {elapsed:.1f}s", flush=True)
    aurocs_clean = aurocs[~np.isnan(aurocs)]
    return {
        "n_iter": n_iter,
        "n_iter_finite": int(len(aurocs_clean)),
        "median": float(np.median(aurocs_clean)),
        "ci_95": [float(np.percentile(aurocs_clean, 2.5)), float(np.percentile(aurocs_clean, 97.5))],
        "std": float(np.std(aurocs_clean)),
    }


def cluster_bootstrap_ci(df_sub: pd.DataFrame, cluster_map: dict[str, str],
                        n_iter: int, seed: int) -> dict:
    """Bootstrap over clusters. For each iter, draw with replacement from the
    set of clusters present, then flatten drawn clusters to receptors."""
    rng = np.random.default_rng(seed)
    recs = sorted(df_sub["receptor_slug"].unique())
    # Assign each receptor to its cluster (fallback: singleton with receptor name)
    rec_cluster = {r: cluster_map.get(r, f"single_{r}") for r in recs}
    # Build cluster -> [receptors]
    cluster_recs = defaultdict(list)
    for r, c in rec_cluster.items():
        cluster_recs[c].append(r)
    clusters = sorted(cluster_recs.keys())
    n_cl = len(clusters)
    aurocs = np.empty(n_iter)
    t0 = time.time()
    for i in range(n_iter):
        drawn_clusters = rng.choice(clusters, size=n_cl, replace=True)
        mult = defaultdict(int)
        for c in drawn_clusters:
            for r in cluster_recs[c]:
                mult[r] += 1
        uniq = sorted(mult.keys())
        aurocs[i] = loro_pooled_auroc(df_sub, uniq, mult)
        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"    boot {i+1}/{n_iter}  elapsed {elapsed:.1f}s", flush=True)
    aurocs_clean = aurocs[~np.isnan(aurocs)]
    return {
        "n_iter": n_iter,
        "n_iter_finite": int(len(aurocs_clean)),
        "n_clusters": n_cl,
        "cluster_map_receptor_to_cluster": rec_cluster,
        "median": float(np.median(aurocs_clean)),
        "ci_95": [float(np.percentile(aurocs_clean, 2.5)), float(np.percentile(aurocs_clean, 97.5))],
        "std": float(np.std(aurocs_clean)),
    }


def permutation_null(df_sub: pd.DataFrame, n_iter: int, seed: int) -> dict:
    """Shuffle labels within receptor, run LORO on all 15, compute pooled AUROC."""
    rng = np.random.default_rng(seed)
    recs = sorted(df_sub["receptor_slug"].unique())
    aurocs = np.empty(n_iter)
    t0 = time.time()
    for i in range(n_iter):
        dp = df_sub.copy()
        for r in recs:
            m = dp["receptor_slug"] == r
            dp.loc[m, "_label"] = rng.permutation(dp.loc[m, "_label"].values)
        obs_s = []; obs_y = []
        for held in recs:
            tr = dp[dp["receptor_slug"] != held]
            te = dp[dp["receptor_slug"] == held]
            X_tr = tr[FEATURES_III].to_numpy(dtype=float)
            X_te = te[FEATURES_III].to_numpy(dtype=float)
            y_tr = tr["_label"].to_numpy(dtype=int)
            mask = np.isfinite(X_tr).all(axis=1)
            X_tr = X_tr[mask]; y_tr = y_tr[mask]
            if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
                continue
            s_te = _fit_predict_logreg(X_tr, y_tr, X_te)
            obs_s.append(s_te); obs_y.append(te["_label"].to_numpy(dtype=int))
        if obs_s:
            aurocs[i] = _auroc(np.concatenate(obs_y), np.concatenate(obs_s))
        else:
            aurocs[i] = float("nan")
        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            print(f"    perm {i+1}/{n_iter}  elapsed {elapsed:.1f}s", flush=True)
    a = aurocs[~np.isnan(aurocs)]
    return {
        "n_iter": n_iter,
        "n_iter_finite": int(len(a)),
        "mean": float(np.mean(a)),
        "ci_95": [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
        "std": float(np.std(a)),
    }


def observed_pooled_auroc(df_sub):
    recs = sorted(df_sub["receptor_slug"].unique())
    mult = {r: 1 for r in recs}
    return loro_pooled_auroc(df_sub, recs, mult)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[G1] loading rows + manifest...")
    df_all = load_and_prep()
    print(f"[G1] Class A passed rows: {len(df_all)}")
    subs = prepare_subsets(df_all)
    for bb, s in subs.items():
        print(f"  {bb}: {len(s)} rows, {s['receptor_slug'].nunique()} receptors, "
              f"labels {dict(s.groupby('_label').size())}")

    cluster_map = load_clusters()
    print(f"[G1] cluster map: {len(cluster_map)} receptors mapped")

    results = {"per_backbone": {}}
    for bb in BACKBONES:
        print(f"\n[G1] {bb}")
        sub = subs[bb]
        obs = observed_pooled_auroc(sub)
        print(f"  observed pooled AUROC = {obs:.4f}")
        print(f"  receptor-boot × {N_ITER}...")
        rboot = receptor_bootstrap_ci(sub, N_ITER, seed=RNG_SEED + hash(bb) % 100000)
        print(f"    median {rboot['median']:.4f}  CI [{rboot['ci_95'][0]:.4f}, {rboot['ci_95'][1]:.4f}]")
        print(f"  cluster-boot × {N_ITER}...")
        cboot = cluster_bootstrap_ci(sub, cluster_map, N_ITER, seed=RNG_SEED + 1 + hash(bb) % 100000)
        print(f"    median {cboot['median']:.4f}  CI [{cboot['ci_95'][0]:.4f}, {cboot['ci_95'][1]:.4f}]  (n_clusters={cboot['n_clusters']})")
        print(f"  permutation null × {N_PERM}...")
        pnull = permutation_null(sub, N_PERM, seed=RNG_SEED + 2 + hash(bb) % 100000)
        print(f"    mean {pnull['mean']:.4f}  CI [{pnull['ci_95'][0]:.4f}, {pnull['ci_95'][1]:.4f}]")

        # p_perm: fraction of null draws ≥ observed
        results["per_backbone"][bb] = {
            "n_rows": int(len(sub)),
            "n_receptors": int(sub["receptor_slug"].nunique()),
            "observed_pooled_auroc": obs,
            "receptor_boot": rboot,
            "cluster_boot": cboot,
            "permutation_null": pnull,
            "vs_null_ci_upper": pnull["ci_95"][1],
            "beats_null_upper": bool(obs > pnull["ci_95"][1]),
        }

    results.update({
        "task": "G1_bootstrap_s1_auroc",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows_csv": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest_csv": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
        },
        "s1_15_receptors": S1_15,
        "feature_set": "F_iii_pocket_plus_axes",
        "arm": "apo",
        "n_bootstrap_iter": N_ITER,
        "n_perm": N_PERM,
        "authoritative_convention": "cluster_boot (per Block A C-8); receptor_boot secondary",
    })

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n[G1] wrote {OUT_JSON.relative_to(REPO)}")

    print("\n" + "=" * 76)
    print("G1 SUMMARY — KILL-S1 row × F_iii × apo × 15 receptors, per backbone")
    print("=" * 76)
    print(f"{'backbone':<10} {'obs':>6} {'rboot_median':>13} {'rboot_ci95':>22} {'cboot_ci95':>22} {'null_upper':>10} {'beats':>6}")
    for bb in BACKBONES:
        r = results["per_backbone"][bb]
        rboot = r["receptor_boot"]; cboot = r["cluster_boot"]; pnull = r["permutation_null"]
        print(
            f"{bb:<10} {r['observed_pooled_auroc']:>6.3f} "
            f"{rboot['median']:>13.3f} "
            f"[{rboot['ci_95'][0]:.3f}, {rboot['ci_95'][1]:.3f}]   "
            f"[{cboot['ci_95'][0]:.3f}, {cboot['ci_95'][1]:.3f}]   "
            f"{pnull['ci_95'][1]:>10.3f} "
            f"{'YES' if r['beats_null_upper'] else 'NO':>6}"
        )


if __name__ == "__main__":
    main()
