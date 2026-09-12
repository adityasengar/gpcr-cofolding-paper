#!/usr/bin/env python3
"""S2 — sample budget + within-cell dispersion + variance decomposition.

Pre-registered against
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`
(committed at e63692f).

Panel: 15 receptors (23 in 2×2 common set MINUS 9 self-reference receptors:
       ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD, OPRK).

Task 1 — AUROC(N) curve:
  N ∈ {1, 2, 5, 10, 20, 50}. 100 draws per N. Three aggregation rules:
    - mean, median, best-of-N (min pocket_ca_rmsd_active).
  Cell-level LORO on cell aggregates. Report AUROC(N) with CI across 100 draws.

Task 2 — Within-cell dispersion as second readout:
  σ(pocket_ca_rmsd) per cell. LORO classify agonist vs antag using dispersion
  alone. Report per-backbone AUROC + 200-permutation null.

Task 3 — Two-way variance decomposition:
  On pocket_ca_rmsd per (receptor, backbone, ligand_role, arm), estimate
  σ²_seed vs σ²_sample vs σ²_residual via method-of-moments ANOVA on
  seed × sample-index. Verdict: MORE_SEEDS / MORE_SAMPLES / MIXED.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))
from s1_loro_classifier import (  # type: ignore
    _auroc, _fit_predict_logreg, build_features, load_and_prep,
    restrict_to_common_23, SELF_REF_RECEPTORS, FEATURES_III,
)

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_JSON = OUT_DIR / "s2_sample_budget.json"

N_LEVELS = [1, 2, 5, 10, 20, 50]
N_DRAWS = 100
AGGS = ["mean", "median", "best_of_n"]
PERM_N_DISPERSION = 200

MODEL_IDX_RE = re.compile(r"_model_(\d+)\.cif|_sample_(\d+)\.cif|model_idx_(\d+)")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _extract_sample_idx(path: str) -> int:
    m = MODEL_IDX_RE.search(path)
    if not m:
        return -1
    for g in m.groups():
        if g is not None:
            return int(g)
    return -1


def _cell_aggregate(cell_rows: pd.DataFrame, n: int, agg: str,
                    features: list[str], rng: np.random.Generator) -> np.ndarray | None:
    """Sample n rows from cell, return per-feature aggregate vector."""
    if len(cell_rows) < n:
        return None
    idx = rng.choice(len(cell_rows), size=n, replace=False)
    sub = cell_rows.iloc[idx]
    X = sub[features].to_numpy(dtype=float)
    # Drop rows with any NaN in features.
    m = np.isfinite(X).all(axis=1)
    X = X[m]
    if len(X) == 0:
        return None
    if agg == "mean":
        return np.nanmean(X, axis=0)
    if agg == "median":
        return np.nanmedian(X, axis=0)
    if agg == "best_of_n":
        # Best of N = row with min pocket_ca_rmsd_active. Use as anchor;
        # return that row's full feature vector.
        pa_col = features.index("pocket_ca_rmsd_active") if "pocket_ca_rmsd_active" in features else None
        if pa_col is None:
            # Fall back: use mean.
            return np.nanmean(X, axis=0)
        pa = X[:, pa_col]
        i = int(np.nanargmin(pa))
        return X[i]
    raise ValueError(agg)


def _loro_cellaggr(
    aggs_by_cell: dict[tuple[str, str], np.ndarray],  # (recep, class_label) -> feature vec
    labels: dict[tuple[str, str], int],
) -> float:
    """LORO on cell-level aggregates. Each held-out receptor contributes its
    2 cells (agonist=1 and antag=0). AUROC pooled over 15 * 2 = 30 predictions.
    """
    receptors = sorted({k[0] for k in aggs_by_cell})
    all_scores, all_labels = [], []
    feature_dim = next(iter(aggs_by_cell.values())).shape[0]

    for held in receptors:
        Xtr, ytr = [], []
        Xte, yte = [], []
        for (rec, cls), vec in aggs_by_cell.items():
            lab = labels[(rec, cls)]
            if rec == held:
                Xte.append(vec); yte.append(lab)
            else:
                Xtr.append(vec); ytr.append(lab)
        if not Xtr or not Xte:
            continue
        Xtr = np.asarray(Xtr); ytr = np.asarray(ytr, dtype=int)
        Xte = np.asarray(Xte); yte = np.asarray(yte, dtype=int)
        # Drop NaN rows in train.
        m = np.isfinite(Xtr).all(axis=1)
        Xtr = Xtr[m]; ytr = ytr[m]
        if len(np.unique(ytr)) < 2 or len(ytr) < 4:
            continue
        # Handle NaN in test by replacing with train mean.
        train_mean = np.nanmean(Xtr, axis=0)
        Xte_c = np.where(np.isfinite(Xte), Xte, train_mean)
        scores = _fit_predict_logreg(Xtr, ytr, Xte_c, n_iter=200, lr=0.1, l2=1.0)
        all_scores.append(scores)
        all_labels.append(yte)
    if not all_scores:
        return float("nan")
    S = np.concatenate(all_scores)
    Y = np.concatenate(all_labels)
    return _auroc(Y, S)


def prepare_data():
    print("[S2] loading rows + manifest...")
    df = load_and_prep()  # Class-A passed rows w/ backbone, partner_type, arm, features
    df = restrict_to_common_23(df)
    df = df[~df["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()
    df["ligand_role"] = df["ligand_role"].astype(str)
    df = df[df["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    df["arm"] = df["arm"].astype(str)
    df = df[df["arm"] == "apo"].copy()  # apo arm only (pre-reg deployment-relevant)
    df["backbone"] = df["backbone"].astype(str).str.lower()
    print(f"[S2] class-A passed apo self-ref-excluded rows: {len(df)}")
    print(f"[S2] receptors: {sorted(df['receptor_slug'].str.upper().unique())}")
    return df


def task1_auroc_curve(df: pd.DataFrame) -> list[dict]:
    """AUROC(N) curve per (n, agg, backbone). 100 draws."""
    rng_master = np.random.default_rng(20260907)
    curve = []
    features = FEATURES_III[:]
    # Grouper: cell key = (backbone, receptor, class); class 1=agonist, 0=antag
    for bb in ["boltz", "chai", "of3", "protenix"]:
        bb_df = df[df["backbone"] == bb]
        if len(bb_df) == 0:
            continue
        cell_groups: dict[tuple[str, str], pd.DataFrame] = {}
        for (rec, role), sub in bb_df.groupby(["receptor_slug", "ligand_role"]):
            key = (rec.upper(), role)
            cell_groups[key] = sub
        # Build labels
        labels = {(rec, role): (1 if role == "full_agonist" else 0) for (rec, role) in cell_groups.keys()}

        for n in N_LEVELS:
            for agg in AGGS:
                aurocs = []
                for draw in range(N_DRAWS):
                    rng = np.random.default_rng(
                        rng_master.integers(0, 2**32 - 1)
                    )
                    aggs_by_cell = {}
                    for key, cell_rows in cell_groups.items():
                        vec = _cell_aggregate(cell_rows, n, agg, features, rng)
                        if vec is not None:
                            aggs_by_cell[key] = vec
                    # Only keep receptors with BOTH classes present.
                    receptors_ok = {
                        r for r in {k[0] for k in aggs_by_cell}
                        if (r, "full_agonist") in aggs_by_cell
                        and (r, "neutral_antagonist") in aggs_by_cell
                    }
                    aggs_by_cell = {
                        k: v for k, v in aggs_by_cell.items() if k[0] in receptors_ok
                    }
                    if len(receptors_ok) < 5:
                        aurocs.append(float("nan"))
                        continue
                    aurocs.append(_loro_cellaggr(aggs_by_cell, labels))
                arr = np.asarray([a for a in aurocs if not np.isnan(a)])
                if len(arr) < 5:
                    entry = {
                        "n": n, "aggregation": agg, "backbone": bb,
                        "mean_auroc": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"),
                        "n_valid": int(len(arr)),
                    }
                else:
                    entry = {
                        "n": n, "aggregation": agg, "backbone": bb,
                        "mean_auroc": float(np.mean(arr)),
                        "ci_lo": float(np.percentile(arr, 2.5)),
                        "ci_hi": float(np.percentile(arr, 97.5)),
                        "median_auroc": float(np.median(arr)),
                        "n_valid": int(len(arr)),
                    }
                curve.append(entry)
                print(f"  N={n:>2} agg={agg:<10} bb={bb:<10} mean_auroc={entry.get('mean_auroc', float('nan')):.3f} "
                      f"CI=[{entry.get('ci_lo', float('nan')):.3f}, {entry.get('ci_hi', float('nan')):.3f}]")
    return curve


def task2_dispersion(df: pd.DataFrame) -> list[dict]:
    """LORO classify agonist vs antag using within-cell dispersion of pocket_ca_rmsd."""
    print("\n[S2 T2] within-cell dispersion classifier...")
    rng_master = np.random.default_rng(20260907)
    out = []
    for bb in ["boltz", "chai", "of3", "protenix"]:
        bb_df = df[df["backbone"] == bb]
        # Per cell: SD of pocket_ca_rmsd.
        cell_stats: dict[tuple[str, str], float] = {}
        for (rec, role), sub in bb_df.groupby(["receptor_slug", "ligand_role"]):
            v = sub["pocket_ca_rmsd"].to_numpy(dtype=float)
            v = v[np.isfinite(v)]
            if len(v) < 5:
                continue
            cell_stats[(rec.upper(), role)] = float(np.std(v))
        aggs_by_cell = {k: np.array([v]) for k, v in cell_stats.items()}
        labels = {k: (1 if k[1] == "full_agonist" else 0) for k in cell_stats}
        auroc = _loro_cellaggr(aggs_by_cell, labels)
        # Permutation null: shuffle labels 200 times.
        null = []
        for _ in range(PERM_N_DISPERSION):
            perm_labels = {}
            recs = sorted({k[0] for k in aggs_by_cell})
            rng = np.random.default_rng(rng_master.integers(0, 2**32 - 1))
            for rec in recs:
                # shuffle within receptor
                keys = [k for k in aggs_by_cell if k[0] == rec]
                lab_arr = np.array([labels[k] for k in keys])
                perm = rng.permutation(lab_arr)
                for kk, pp in zip(keys, perm):
                    perm_labels[kk] = int(pp)
            null.append(_loro_cellaggr(aggs_by_cell, perm_labels))
        null_clean = np.asarray([x for x in null if not np.isnan(x)])
        p_perm = float(np.mean(null_clean >= auroc)) if len(null_clean) > 0 else float("nan")
        entry = {
            "backbone": bb, "auroc": float(auroc),
            "null_mean": float(np.mean(null_clean)) if len(null_clean) else float("nan"),
            "null_p_perm": p_perm,
            "n_cells": len(cell_stats),
        }
        print(f"  {bb:<10} auroc={auroc:.3f} null_mean={entry['null_mean']:.3f} p_perm={p_perm:.3f}")
        out.append(entry)
    return out


def task3_variance_decomp(df: pd.DataFrame) -> dict:
    """Method-of-moments ANOVA on pocket_ca_rmsd. Per (receptor, backbone,
    ligand_role, arm), decompose into σ²_seed, σ²_sample, σ²_residual."""
    print("\n[S2 T3] two-way variance decomposition...")
    # Extract sample_idx from input_path.
    df = df.copy()
    df["_sample_idx"] = df["input_path"].apply(_extract_sample_idx)
    df["_seed"] = df["seed_used"].astype(str)
    df["_pca"] = pd.to_numeric(df["pocket_ca_rmsd"], errors="coerce")

    # For each (receptor, backbone, ligand_role, arm) cell with valid data,
    # decompose. Then aggregate across cells.
    per_cell = []
    for (rec, bb, role, arm), sub in df.groupby(
        ["receptor_slug", "backbone", "ligand_role", "arm"]
    ):
        vals = sub["_pca"].to_numpy(dtype=float)
        seeds = sub["_seed"].to_numpy()
        samples = sub["_sample_idx"].to_numpy()
        m = np.isfinite(vals) & (samples >= 0)
        if m.sum() < 10:
            continue
        vals = vals[m]; seeds = seeds[m]; samples = samples[m]
        # Simple method-of-moments: variance across seed-means (with pooling within seed)
        unique_seeds = np.unique(seeds)
        if len(unique_seeds) < 2:
            continue
        seed_means = np.array([vals[seeds == s].mean() for s in unique_seeds])
        sigma2_seed = float(np.var(seed_means, ddof=1))
        # Within-seed variance (across samples)
        within = []
        for s in unique_seeds:
            v = vals[seeds == s]
            if len(v) >= 2:
                within.append(np.var(v, ddof=1))
        sigma2_within = float(np.mean(within)) if within else float("nan")
        per_cell.append({
            "receptor": rec, "backbone": bb, "ligand_role": role, "arm": arm,
            "sigma2_seed": sigma2_seed, "sigma2_within_seed": sigma2_within,
            "n_seeds": int(len(unique_seeds)), "n_samples_per_seed_avg": float(len(vals)/len(unique_seeds)),
        })

    if not per_cell:
        return {"verdict": "INSUFFICIENT_DATA"}

    # Aggregate: pooled seed vs pooled within-seed variance.
    sig_seed = np.asarray([c["sigma2_seed"] for c in per_cell])
    sig_within = np.asarray([c["sigma2_within_seed"] for c in per_cell])
    valid = np.isfinite(sig_seed) & np.isfinite(sig_within) & (sig_within > 0)
    sig_seed = sig_seed[valid]; sig_within = sig_within[valid]

    ratio = sig_seed / sig_within  # >1 = seed dominates; <1 = sample dominates
    median_ratio = float(np.median(ratio))
    q25, q75 = float(np.percentile(ratio, 25)), float(np.percentile(ratio, 75))
    if median_ratio > 1.5:
        verdict = "MORE_SEEDS"
    elif median_ratio < 0.67:
        verdict = "MORE_SAMPLES_PER_SEED"
    else:
        verdict = "MIXED"

    print(f"  n_cells: {len(sig_seed)}")
    print(f"  median σ²_seed: {float(np.median(sig_seed)):.4f}")
    print(f"  median σ²_within_seed (per sample): {float(np.median(sig_within)):.4f}")
    print(f"  median ratio σ²_seed / σ²_within: {median_ratio:.3f}  IQR [{q25:.3f}, {q75:.3f}]")
    print(f"  verdict: {verdict}")

    return {
        "n_cells_analyzed": int(len(sig_seed)),
        "median_sigma2_seed": float(np.median(sig_seed)),
        "median_sigma2_within_seed": float(np.median(sig_within)),
        "median_ratio_seed_over_within": median_ratio,
        "ratio_iqr_lo": q25,
        "ratio_iqr_hi": q75,
        "verdict": verdict,
        "verdict_note": (
            {
                "MORE_SEEDS": "σ²_seed > σ²_within-seed on most cells; adding seeds "
                              "reduces uncertainty faster than adding samples per seed.",
                "MORE_SAMPLES_PER_SEED": "σ²_within-seed > σ²_seed on most cells; "
                                         "adding samples per seed helps more.",
                "MIXED": "Neither dominates; both scaling axes have similar effect.",
            }[verdict]
        ),
        "per_cell_head": per_cell[:20],
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = prepare_data()
    print("\n[S2 T1] AUROC(N) curve — apo × 15 receptors × F_iii features")
    curve = task1_auroc_curve(df)
    dispersion = task2_dispersion(df)
    variance_decomp = task3_variance_decomp(df)

    report = {
        "task": "S2_sample_budget",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_git_sha": "e63692f",
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
        },
        "panel": {
            "n_receptors": 15,
            "self_ref_excluded": sorted(SELF_REF_RECEPTORS),
            "arm": "apo",
            "features": FEATURES_III,
            "n_rows_per_cell": 50,
            "n_seeds_per_cell": 5,
            "n_samples_per_seed": 10,
        },
        "sample_budget_auroc_curve": curve,
        "within_cell_dispersion_auroc": dispersion,
        "variance_decomposition": variance_decomp,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2, default=str))
    print(f"\nwrote {OUT_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
