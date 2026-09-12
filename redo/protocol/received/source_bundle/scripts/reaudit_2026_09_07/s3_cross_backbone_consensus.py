#!/usr/bin/env python3
"""S3 — cross-backbone consensus as a confidence signal.

Pre-registered per
``experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md``
(committed at e63692f).

KILL-S3 (BINDING): if cross-backbone agreement predicts distance-to-crystal
NO BETTER than pLDDT on matched folds — paired Δ AUROC ≤ 0 with CI clearing
zero on ≥ 2 of 4 backbones — report the negative and stop the
confidence-signal claim line.

Steps:
  1. Per (receptor, ligand_state, arm, seed), compute pairwise-backbone
     distance on pocket_ca_rmsd_active/_inactive; consensus =
     1 / (1 + mean pairwise distance).
  2. Regress crystal-distance ~ consensus, LORO Spearman ρ per receptor.
  3. Accuracy-vs-coverage curve: at top X% most-consensual rows for S1
     classifier predictions, what's the pooled AUROC?
  4. Paired benchmark vs pLDDT: same curve using plddt_mean; per-backbone
     Δ AUROC.
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
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts/reaudit_2026_09_07"))

from s1_loro_classifier import (  # type: ignore  # noqa: E402
    _auroc, _fit_predict_logreg, FEATURES_III, FEATURES_II, FEATURES_I,
    SELF_REF_RECEPTORS, build_features, load_and_prep, restrict_to_common_23,
    build_label,
)

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_JSON = OUT_DIR / "s3_cross_backbone_consensus.json"


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


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]; y = y[m]
    if len(x) < 3:
        return float("nan")
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if np.std(rx) < 1e-12 or np.std(ry) < 1e-12:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def compute_consensus_per_row(df: pd.DataFrame) -> pd.Series:
    """For each row, compute cross-backbone consensus on the same
    (receptor, ligand_role, arm, seed, sample_idx) key.

    consensus = 1 / (1 + mean pairwise |Δ| over 6 pairs of the 4 backbones)
    on the 2-vector [pocket_ca_rmsd_active, pocket_ca_rmsd_inactive].

    Attaches the same consensus to every backbone's row in that cell
    (agreement is a cell-level property).
    """
    # Recover sample index from input_path if present. Path pattern:
    #   /pool/<receptor>/<role>/<arm>/<backbone>/seed_<N>/... /model_<K>.cif
    # sample_idx is the terminal `_<K>` in the file name; extract robustly.
    df = df.copy()
    df["_sample_idx"] = (
        df["input_path"].astype(str).str.extract(r"(?:_model|_sample|model_idx)[_.]?(\d+)")[0]
        .fillna("0").astype(int)
    )
    df["_seed_num"] = (
        df["input_path"].astype(str).str.extract(r"seed_(\d+)")[0]
        .fillna("0").astype(int)
    )
    df["_cell_key"] = (
        df["receptor_slug"].astype(str) + "|"
        + df["ligand_role"].astype(str) + "|"
        + df["arm"].astype(str) + "|"
        + df["_seed_num"].astype(str) + "|"
        + df["_sample_idx"].astype(str)
    )

    df["pocket_ca_rmsd_active_f"] = pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce")
    df["pocket_ca_rmsd_inactive_f"] = pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce")

    consensus_by_cell: dict[str, float] = {}
    grouped = df.groupby("_cell_key")
    for k, g in grouped:
        bbs = g["backbone"].astype(str).str.lower().values
        va = g["pocket_ca_rmsd_active_f"].values
        vi = g["pocket_ca_rmsd_inactive_f"].values
        # Aggregate to per-backbone means (if multiple rows per bb; usually 1).
        d: dict[str, tuple[float, float]] = {}
        for bb, a, i in zip(bbs, va, vi):
            if not (math.isfinite(a) and math.isfinite(i)):
                continue
            if bb not in d:
                d[bb] = (a, i)
        if len(d) < 2:
            consensus_by_cell[k] = float("nan")
            continue
        vecs = np.array(list(d.values()))
        # Pairwise |Δ|_L1 across the 2-vector.
        n = len(vecs)
        pw = []
        for i in range(n):
            for j in range(i + 1, n):
                pw.append(np.mean(np.abs(vecs[i] - vecs[j])))
        mean_pw = float(np.mean(pw))
        consensus_by_cell[k] = 1.0 / (1.0 + mean_pw)

    df["_consensus"] = df["_cell_key"].map(consensus_by_cell)
    return df["_consensus"]


def loro_predict_scores(
    df: pd.DataFrame, feature_names: list[str], label_col: str = "_label",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run LORO logistic regression on df, return (row_idx, scores, labels)
    aligned to df row order."""
    receptors = sorted(df["receptor_slug"].str.upper().unique())
    all_idx = []
    all_s = []
    all_y = []
    for held in receptors:
        te_mask = df["receptor_slug"].str.upper() == held
        tr_mask = ~te_mask
        tr = df[tr_mask]
        te = df[te_mask]
        if len(tr) == 0 or len(te) == 0:
            continue
        X_tr = tr[feature_names].to_numpy(dtype=float)
        X_te = te[feature_names].to_numpy(dtype=float)
        y_tr = tr[label_col].to_numpy(dtype=int)
        mask_tr = np.isfinite(X_tr).all(axis=1)
        X_tr = X_tr[mask_tr]; y_tr = y_tr[mask_tr]
        if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
            continue
        s_te = _fit_predict_logreg(X_tr, y_tr, X_te)
        all_idx.append(te.index.values)
        all_s.append(s_te)
        all_y.append(te[label_col].to_numpy(dtype=int))
    if not all_idx:
        return np.array([]), np.array([]), np.array([])
    return np.concatenate(all_idx), np.concatenate(all_s), np.concatenate(all_y)


def accuracy_at_coverage(scores, labels, confidence, coverage_pcts):
    """For each coverage percentage, keep top-X% most-confident predictions,
    return pooled AUROC on that subset."""
    order = np.argsort(-confidence)  # descending confidence
    out = {}
    n = len(scores)
    for pct in coverage_pcts:
        k = max(int(pct / 100.0 * n), 10)
        keep = order[:k]
        out[pct] = {
            "n_rows": int(k),
            "auroc": _auroc(labels[keep], scores[keep]),
            "coverage_pct": pct,
        }
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(OUT_JSON))
    parser.add_argument("--n-permutations", type=int, default=100)
    args = parser.parse_args()

    # -------------------------------------------------------------------
    # Load rows with backbone / ligand_role / arm joined in.
    # -------------------------------------------------------------------
    print("[S3] loading...", flush=True)
    df = load_and_prep()
    df["_pdb"] = df["input_path"].map(
        pd.read_csv(MANIFEST_CSV, low_memory=False)
        .set_index("prediction_path")["ligand_bound_pdb"].to_dict()
    )
    # pLDDT columns.
    df["plddt_mean"] = pd.to_numeric(df.get("plddt_mean", pd.Series(dtype=float)), errors="coerce")
    df["plddt_at_anchors"] = pd.to_numeric(df.get("plddt_at_anchors", pd.Series(dtype=float)), errors="coerce")
    df["min_plddt_at_anchor"] = pd.to_numeric(df.get("min_plddt_at_anchor", pd.Series(dtype=float)), errors="coerce")

    df_common = restrict_to_common_23(df)
    print(f"[S3] loaded {len(df)} class-A passed rows; common set n={df_common['receptor_slug'].nunique()}", flush=True)

    # -------------------------------------------------------------------
    # (1) Compute consensus per cell.
    # -------------------------------------------------------------------
    print("[S3] computing cross-backbone consensus...", flush=True)
    df_common["_consensus"] = compute_consensus_per_row(df_common)
    print(f"    consensus non-NaN: {df_common['_consensus'].notna().sum()} / {len(df_common)}", flush=True)

    # -------------------------------------------------------------------
    # (2) Consensus vs crystal-distance per receptor.
    #     "Crystal distance" here = pocket_ca_rmsd_active (distance to the
    #     receptor's active reference; this reference IS the crystal for
    #     receptors where ligand_bound_pdb equals the active reference PDB).
    #     Report per-receptor Spearman ρ pooled across (backbone, seed).
    # -------------------------------------------------------------------
    print("[S3] consensus vs crystal-distance per receptor...", flush=True)
    consensus_vs_crystal = {}
    for rec in sorted(df_common["receptor_slug"].unique()):
        sub = df_common[df_common["receptor_slug"] == rec]
        rho = spearman_rho(
            sub["_consensus"].values,
            pd.to_numeric(sub["pocket_ca_rmsd_active"], errors="coerce").values,
        )
        consensus_vs_crystal[rec] = {
            "spearman_rho": rho,
            "n_rows": int(len(sub)),
        }
    # Pooled Spearman on the full common set (single ρ across all rows).
    pooled_rho = spearman_rho(
        df_common["_consensus"].values,
        pd.to_numeric(df_common["pocket_ca_rmsd_active"], errors="coerce").values,
    )
    # Pooled with plddt for comparison.
    pooled_rho_plddt = spearman_rho(
        df_common["plddt_mean"].values,
        pd.to_numeric(df_common["pocket_ca_rmsd_active"], errors="coerce").values,
    )
    print(f"    pooled ρ(consensus, crystal-distance) = {pooled_rho:.3f}", flush=True)
    print(f"    pooled ρ(pLDDT, crystal-distance)     = {pooled_rho_plddt:.3f}", flush=True)

    # -------------------------------------------------------------------
    # (3) Accuracy-vs-coverage on S1 classifier per backbone.
    # -------------------------------------------------------------------
    print("[S3] accuracy-vs-coverage curves...", flush=True)
    # Use apo × self-ref-excluded × F_iii logistic regression (matches
    # S1's KILL row).
    df_kill = df_common[
        (df_common["arm"] == "apo")
        & (~df_common["receptor_slug"].isin(SELF_REF_RECEPTORS))
    ].copy()

    coverage_pcts = [25, 50, 75, 100]
    per_backbone_curves_consensus = {}
    per_backbone_curves_plddt = {}
    paired_deltas: list[dict] = []

    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_kill[df_kill["backbone"].str.lower() == bb].copy()
        pair = build_label(sub, "full_agonist", "neutral_antagonist")
        if len(pair) < 100 or pair["receptor_slug"].nunique() < 5:
            per_backbone_curves_consensus[bb] = {"reason": "insufficient_data"}
            per_backbone_curves_plddt[bb] = {"reason": "insufficient_data"}
            continue

        pair = pair.reset_index(drop=True)
        idx, s, y = loro_predict_scores(pair, FEATURES_III)
        if len(idx) == 0:
            per_backbone_curves_consensus[bb] = {"reason": "no_folds_valid"}
            per_backbone_curves_plddt[bb] = {"reason": "no_folds_valid"}
            continue

        # Confidence signals aligned to (idx).
        conf_consensus = pair.loc[idx, "_consensus"].values
        conf_plddt = pair.loc[idx, "plddt_mean"].values
        # NaN-safe: mask NaN confidences.
        m_c = np.isfinite(conf_consensus) & np.isfinite(s) & np.isfinite(y)
        m_p = np.isfinite(conf_plddt) & np.isfinite(s) & np.isfinite(y)

        per_backbone_curves_consensus[bb] = accuracy_at_coverage(
            s[m_c], y[m_c], conf_consensus[m_c], coverage_pcts,
        )
        per_backbone_curves_plddt[bb] = accuracy_at_coverage(
            s[m_p], y[m_p], conf_plddt[m_p], coverage_pcts,
        )
        # Paired Δ AUROC at 50% coverage — the middle of the curve.
        c_auroc_50 = per_backbone_curves_consensus[bb].get(50, {}).get("auroc", float("nan"))
        p_auroc_50 = per_backbone_curves_plddt[bb].get(50, {}).get("auroc", float("nan"))
        # Bootstrap CI on Δ.
        rng = np.random.default_rng(20260907)
        n_common = m_c & m_p
        s2, y2 = s[n_common], y[n_common]
        cc = conf_consensus[n_common]; cp = conf_plddt[n_common]
        n = int(np.sum(n_common))
        if n < 20:
            delta = float("nan"); ci_lo = float("nan"); ci_hi = float("nan")
        else:
            deltas = np.empty(500, dtype=float)
            for k in range(500):
                b = rng.integers(0, n, n)
                oc = np.argsort(-cc[b])[: max(int(0.5 * n), 10)]
                op = np.argsort(-cp[b])[: max(int(0.5 * n), 10)]
                a_c = _auroc(y2[b][oc], s2[b][oc])
                a_p = _auroc(y2[b][op], s2[b][op])
                deltas[k] = a_c - a_p
            deltas_clean = deltas[np.isfinite(deltas)]
            delta = float(np.mean(deltas_clean)) if len(deltas_clean) else float("nan")
            ci_lo = float(np.percentile(deltas_clean, 2.5)) if len(deltas_clean) else float("nan")
            ci_hi = float(np.percentile(deltas_clean, 97.5)) if len(deltas_clean) else float("nan")

        paired_deltas.append({
            "backbone": bb,
            "consensus_auroc_at_50pct": c_auroc_50,
            "plddt_auroc_at_50pct": p_auroc_50,
            "delta_at_50pct": (c_auroc_50 - p_auroc_50) if math.isfinite(c_auroc_50) and math.isfinite(p_auroc_50) else float("nan"),
            "delta_bootstrap_mean": delta,
            "delta_ci_lo": ci_lo,
            "delta_ci_hi": ci_hi,
        })
        print(
            f"    {bb:<10} consensus@50%={c_auroc_50:.3f}  pLDDT@50%={p_auroc_50:.3f}  "
            f"Δ={delta if math.isfinite(delta) else float('nan'):+.3f} "
            f"[{ci_lo if math.isfinite(ci_lo) else float('nan'):+.3f}, {ci_hi if math.isfinite(ci_hi) else float('nan'):+.3f}]",
            flush=True,
        )

    # -------------------------------------------------------------------
    # KILL-S3 verdict.
    # -------------------------------------------------------------------
    n_fired = sum(
        1 for d in paired_deltas
        if math.isfinite(d.get("delta_ci_lo", float("nan")))
        and math.isfinite(d.get("delta_ci_hi", float("nan")))
        and (
            d["delta_at_50pct"] <= 0
            or (d["delta_ci_lo"] <= 0 <= d["delta_ci_hi"])
        )
    )
    kill_s3_fired = n_fired >= 2
    kill_s3_verdict = (
        "KILL_S3_FIRED" if kill_s3_fired else "KILL_S3_DID_NOT_FIRE"
    )

    report = {
        "task": "S3_cross_backbone_consensus",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
            "manifest": {"path": str(MANIFEST_CSV.relative_to(REPO)), "sha256": sha256_file(MANIFEST_CSV)},
        },
        "prereg_git_sha": "e63692f",
        "n_common_receptors": int(df_common["receptor_slug"].nunique()),
        "consensus_vs_crystal_distance": {
            "per_receptor": consensus_vs_crystal,
            "pooled_rho_consensus": pooled_rho,
            "pooled_rho_plddt": pooled_rho_plddt,
        },
        "accuracy_vs_coverage_consensus": per_backbone_curves_consensus,
        "accuracy_vs_coverage_plddt": per_backbone_curves_plddt,
        "paired_delta_auroc": paired_deltas,
        "kill_s3_verdict": kill_s3_verdict,
        "kill_s3_fired": kill_s3_fired,
        "verdict_note": (
            f"n_backbones_where_delta_le0_or_ci_straddles_0 = {n_fired}/4. "
            "KILL-S3 fires if ≥ 2 of 4."
        ),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[S3] wrote {Path(args.out).relative_to(REPO)}")
    print()
    print("=" * 70)
    print("S3 verdict:", kill_s3_verdict)
    print(f"  pooled ρ(consensus, crystal-dist) = {pooled_rho:.3f}")
    print(f"  pooled ρ(pLDDT, crystal-dist)     = {pooled_rho_plddt:.3f}")
    print("  Paired Δ AUROC (consensus − pLDDT) at 50% coverage:")
    for d in paired_deltas:
        print(
            f"    {d['backbone']:<10} Δ={d['delta_at_50pct']:+.3f}  "
            f"boot Δ={d.get('delta_bootstrap_mean', float('nan')):+.3f} "
            f"[{d.get('delta_ci_lo', float('nan')):+.3f}, {d.get('delta_ci_hi', float('nan')):+.3f}]"
        )
    return 0 if not kill_s3_fired else 1


if __name__ == "__main__":
    raise SystemExit(main())
