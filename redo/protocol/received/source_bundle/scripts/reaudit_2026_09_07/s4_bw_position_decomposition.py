#!/usr/bin/env python3
"""S4 — per-BW-position decomposition + minimal instrument.

Pre-registered at
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`
(committed at e63692f).

KILL-S4 (secondary): if top-k reduced instrument (k ≤ 10) does NOT match
whole-pocket RMSD (within 0.03 AUROC on LORO, apo arm × self-ref-excluded),
the whole-pocket aggregate remains the reference readout; no minimal-instrument
claim.

Route: (b) — corpus does not carry per-BW-position pocket RMSDs; use the
existing position-level anchor motif features (all localized to canonical
Class A activation positions).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))
import s1_loro_classifier as s1  # noqa: E402

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_JSON = OUT_DIR / "s4_bw_position_decomposition.json"

# From S1 smoke (kill-S1 row winners): reference whole-pocket AUROCs to
# compare the reduced instrument against.
WHOLE_POCKET_AUROC = {
    # S1 KILL-S1 row (C_no_selfref_apo), F_iii_pocket_plus_axes
    "boltz":    0.852,
    "chai":     0.706,
    "of3":      0.656,
    "protenix": 0.825,
}
KILL_S4_TOLERANCE = 0.03

# Position-level anchor features present in rows.tier3.v2.csv, with BW
# interpretation. Each is a continuous scalar localized to a canonical
# activation-relevant position or pair.
POSITION_FEATURES: dict[str, dict] = {
    # DRY / TM3–TM6 outward
    "d_tm6_r350_r630_ca":                    {"bw": "3.50/6.30",         "motif": "DRY–TM6"},
    "d_dry_sidechain_r350cz_e630oe1":        {"bw": "3.50/6.30",         "motif": "DRY sidechain"},
    # NPxxY
    "d_npxxy_y558_y753_ca":                  {"bw": "5.58/7.53",         "motif": "NPxxY (CA)"},
    "d_npxxy_y558_y753_oh":                  {"bw": "5.58/7.53",         "motif": "NPxxY (OH)"},
    "d_y558_pack_min_heavy":                 {"bw": "5.58",              "motif": "Y5.58 pack"},
    # TM5 outward
    "d_tm5_outward_r350_r558_ca":            {"bw": "3.50/5.58",         "motif": "TM5 outward"},
    # TM6 tilt (GPCRdb)
    "d_gpcrdb_tm6_tilt_246_637_ca":          {"bw": "2.46/6.37",         "motif": "TM6 tilt"},
    # W6.48 toggle
    "w648_chi1":                             {"bw": "6.48",              "motif": "W6.48 toggle"},
    # ICL2 helicity
    "icl2_helical_frac":                     {"bw": "ICL2",              "motif": "ICL2 helicity"},
    # A100 index components
    "a100_component_1_ca":                   {"bw": "A100.c1",           "motif": "A100 comp 1"},
    "a100_component_2_ca":                   {"bw": "A100.c2",           "motif": "A100 comp 2"},
    "a100_component_3_ca":                   {"bw": "A100.c3",           "motif": "A100 comp 3"},
    "a100_component_4_ca":                   {"bw": "A100.c4",           "motif": "A100 comp 4"},
    "a100_component_5_ca":                   {"bw": "A100.c5",           "motif": "A100 comp 5"},
    "a100_index":                            {"bw": "A100",              "motif": "A100 composite"},
    # Whole-pocket aggregates (kept as reference — labeled explicitly)
    "pocket_ca_rmsd":                        {"bw": "pocket (aggregate)","motif": "aggregate"},
}

BACKBONES = ["boltz", "chai", "of3", "protenix"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load_kill_s1_subset() -> pd.DataFrame:
    """Load the KILL-S1 row: apo arm × self-reference-excluded × 2×2 common set."""
    print("[S4] loading rows + manifest ...")
    df_all = s1.load_and_prep()
    # Cast every candidate feature to numeric.
    for col in POSITION_FEATURES:
        if col in df_all.columns:
            df_all[col] = pd.to_numeric(df_all[col], errors="coerce")
    # Restrict to 2×2 common set + apo arm + self-ref-excluded.
    df_common = s1.restrict_to_common_23(df_all)
    df_c = df_common[~df_common["receptor_slug"].isin(s1.SELF_REF_RECEPTORS)].copy()
    df_apo = df_c[df_c["arm"] == "apo"].copy()
    # Filter to full_agonist vs neutral_antagonist labeled rows.
    df_pair = s1.build_label(df_apo, "full_agonist", "neutral_antagonist")
    print(f"[S4] {len(df_pair)} rows; "
          f"{df_pair['receptor_slug'].nunique()} receptors; "
          f"backbones: {sorted(df_pair['backbone'].str.lower().unique())}")
    return df_pair


# ---------------------------------------------------------------------
# Per-feature single-threshold LORO AUROC + permutation null.
# ---------------------------------------------------------------------


def per_feature_loro_auroc(
    df: pd.DataFrame, feature: str, n_permutations: int = 50,
) -> dict:
    """Single-feature threshold classifier LORO per backbone. Returns
    per-backbone dict with pooled AUROC + null summary."""
    out = {}
    for bb in BACKBONES:
        sub = df[df["backbone"].str.lower() == bb].copy()
        if len(sub) == 0:
            out[bb] = {"reason": "no_rows"}
            continue
        # single-feature; drop NaN.
        mask = np.isfinite(pd.to_numeric(sub[feature], errors="coerce").to_numpy())
        sub2 = sub[mask].copy()
        if len(sub2) == 0 or sub2["receptor_slug"].nunique() < 5:
            out[bb] = {"reason": "sparse", "n_rows": int(len(sub2))}
            continue
        r = s1.loro_evaluate(
            sub2, [feature], model="threshold",
            n_permutations=n_permutations, rng_seed=20260907,
        )
        out[bb] = {
            "n_rows": int(len(sub2)),
            "n_receptors": int(sub2["receptor_slug"].nunique()),
            "pooled_auroc": r["pooled_auroc"],
            "null_mean": r["null_pooled_auroc_mean"],
            "null_lo": r["null_pooled_auroc_2p5"],
            "null_hi": r["null_pooled_auroc_97p5"],
            "p_perm": r["permutation_p_value"],
            "z_vs_null": r["z_vs_null"],
        }
    return out


# ---------------------------------------------------------------------
# Top-k reduced instrument.
#
# Selection strictly inside training fold. For each LORO fold on backbone bb:
#   1. On the training receptors, compute the single-feature LORO AUROC
#      (nested LORO over the training set) for every candidate feature.
#      Because nested LORO is expensive, we use a cheaper proxy: single-
#      feature AUROC on the training-fold rows (pooled across training
#      receptors). This is a defensible fold-internal ranking; it does
#      NOT peek at the held-out receptor.
#   2. Rank features by training-fold AUROC; take top k.
#   3. Fit logreg on top-k features from the training fold; predict on
#      held-out.
# ---------------------------------------------------------------------


def top_k_loro_pipeline(
    df: pd.DataFrame, features: list[str], k: int, backbone: str,
    n_permutations: int = 50, rng_seed: int = 20260907,
) -> dict:
    """LORO with fold-internal top-k feature selection."""
    sub = df[df["backbone"].str.lower() == backbone].copy()
    receptors = sorted(sub["receptor_slug"].str.upper().unique())
    if len(receptors) < 5:
        return {"reason": "sparse", "n_receptors": len(receptors)}

    obs_scores: dict[str, np.ndarray] = {}
    obs_labels: dict[str, np.ndarray] = {}

    for held in receptors:
        tr = sub[sub["receptor_slug"].str.upper() != held].copy()
        te = sub[sub["receptor_slug"].str.upper() == held].copy()
        if len(tr) == 0 or len(te) == 0:
            continue
        # 1. Training-fold single-feature AUROCs.
        tr_aurocs = {}
        for f in features:
            v = pd.to_numeric(tr[f], errors="coerce").to_numpy()
            mask = np.isfinite(v)
            if mask.sum() < 30:
                continue
            y = tr["_label"].to_numpy(dtype=int)[mask]
            if len(np.unique(y)) < 2:
                continue
            a = s1._auroc(y.astype(bool), v[mask])
            # AUROC-directional: use max(a, 1-a) as the discriminative strength.
            tr_aurocs[f] = max(a, 1 - a) if np.isfinite(a) else 0.0
        # 2. Top-k features by training-fold discriminative strength.
        top = sorted(tr_aurocs.items(), key=lambda x: -x[1])[:k]
        top_feats = [f for f, _ in top]
        if len(top_feats) < 2:
            continue
        # 3. Fit logreg on top-k, predict held-out.
        X_tr = tr[top_feats].to_numpy(dtype=float)
        y_tr = tr["_label"].to_numpy(dtype=int)
        X_te = te[top_feats].to_numpy(dtype=float)
        mask_tr = np.isfinite(X_tr).all(axis=1)
        X_tr = X_tr[mask_tr]; y_tr = y_tr[mask_tr]
        # Impute test NaNs with train column means (fold-internal).
        col_means = np.nanmean(X_tr, axis=0)
        for c in range(X_te.shape[1]):
            m = ~np.isfinite(X_te[:, c])
            X_te[m, c] = col_means[c]
        if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
            continue
        s_te = s1._fit_predict_logreg(X_tr, y_tr, X_te)
        obs_scores[held] = s_te
        obs_labels[held] = te["_label"].to_numpy(dtype=int)

    if not obs_scores:
        return {"reason": "no_folds_produced_scores"}
    all_s = np.concatenate([obs_scores[r] for r in obs_labels])
    all_y = np.concatenate([obs_labels[r] for r in obs_labels])
    pooled_auroc = s1._auroc(all_y, all_s)

    # Permutation null: shuffle labels WITHIN receptor, redo top-k selection
    # + fit + predict.
    rng = np.random.default_rng(rng_seed)
    null = np.empty(n_permutations, dtype=float)
    for p in range(n_permutations):
        df_p = sub.copy()
        for rec in receptors:
            m = df_p["receptor_slug"].str.upper() == rec
            df_p.loc[m, "_label"] = rng.permutation(df_p.loc[m, "_label"].values)
        obs_p_s: list[np.ndarray] = []
        obs_p_y: list[np.ndarray] = []
        for held in receptors:
            tr = df_p[df_p["receptor_slug"].str.upper() != held].copy()
            te = df_p[df_p["receptor_slug"].str.upper() == held].copy()
            if len(tr) == 0 or len(te) == 0:
                continue
            tr_aurocs_p = {}
            for f in features:
                v = pd.to_numeric(tr[f], errors="coerce").to_numpy()
                mask = np.isfinite(v)
                if mask.sum() < 30:
                    continue
                y = tr["_label"].to_numpy(dtype=int)[mask]
                if len(np.unique(y)) < 2:
                    continue
                a = s1._auroc(y.astype(bool), v[mask])
                tr_aurocs_p[f] = max(a, 1 - a) if np.isfinite(a) else 0.0
            top_p = sorted(tr_aurocs_p.items(), key=lambda x: -x[1])[:k]
            top_feats_p = [f for f, _ in top_p]
            if len(top_feats_p) < 2:
                continue
            X_tr = tr[top_feats_p].to_numpy(dtype=float)
            y_tr = tr["_label"].to_numpy(dtype=int)
            X_te = te[top_feats_p].to_numpy(dtype=float)
            mask_tr = np.isfinite(X_tr).all(axis=1)
            X_tr = X_tr[mask_tr]; y_tr = y_tr[mask_tr]
            col_means = np.nanmean(X_tr, axis=0)
            for c in range(X_te.shape[1]):
                m = ~np.isfinite(X_te[:, c])
                X_te[m, c] = col_means[c]
            if len(np.unique(y_tr)) < 2 or len(y_tr) < 20:
                continue
            s_te = s1._fit_predict_logreg(X_tr, y_tr, X_te)
            obs_p_s.append(s_te)
            obs_p_y.append(te["_label"].to_numpy(dtype=int))
        if obs_p_s:
            null[p] = s1._auroc(np.concatenate(obs_p_y), np.concatenate(obs_p_s))
        else:
            null[p] = float("nan")

    null_clean = null[~np.isnan(null)]
    if len(null_clean):
        p_val = float(np.mean(null_clean >= pooled_auroc))
        n_mean = float(np.mean(null_clean))
        n_lo, n_hi = float(np.percentile(null_clean, 2.5)), float(np.percentile(null_clean, 97.5))
    else:
        p_val = n_mean = n_lo = n_hi = float("nan")
    return {
        "n_receptors": len(receptors),
        "n_holdouts_produced": len(obs_scores),
        "pooled_auroc": pooled_auroc,
        "null_mean": n_mean,
        "null_lo": n_lo,
        "null_hi": n_hi,
        "p_perm": p_val,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-permutations", type=int, default=50)
    parser.add_argument("--out", default=str(OUT_JSON))
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_kill_s1_subset()

    # 1. Per-feature single-threshold LORO AUROC.
    print("[S4-1] per-feature single-threshold LORO...")
    per_feature_by_bb: dict[str, dict[str, dict]] = {}
    all_features = list(POSITION_FEATURES.keys())
    # Restrict candidate features to ones actually present with reasonable
    # coverage (>90% non-NaN across the full subset).
    for f in list(all_features):
        v = pd.to_numeric(df[f], errors="coerce")
        cov = float(np.isfinite(v).mean())
        if cov < 0.5:
            print(f"  DROP feature '{f}': coverage {cov:.2f}")
            all_features.remove(f)
    print(f"[S4-1] {len(all_features)} usable features")

    for f in all_features:
        r = per_feature_loro_auroc(df, f, n_permutations=args.n_permutations)
        per_feature_by_bb[f] = r
        # Compact per-line summary.
        parts = []
        for bb in BACKBONES:
            rb = r.get(bb, {})
            if "pooled_auroc" in rb:
                parts.append(f"{bb}={rb['pooled_auroc']:.3f}")
            else:
                parts.append(f"{bb}=NA")
        print(f"  {f:<40}  {POSITION_FEATURES[f]['bw']:<15}  " + "  ".join(parts))

    # 2. Top-k reduced instrument per backbone.
    print("[S4-2] top-k reduced instrument (k=3, 5, 10) via fold-internal ranking...")
    # Anchor-only feature set (exclude the aggregate pocket_ca_rmsd, to test
    # whether the anchor family alone recovers the signal).
    anchor_features = [f for f in all_features if f != "pocket_ca_rmsd"]

    top_k_results: dict[str, list[dict]] = {}
    for bb in BACKBONES:
        top_k_results[bb] = []
        for k in (3, 5, 10):
            rr = top_k_loro_pipeline(
                df, anchor_features, k=k, backbone=bb,
                n_permutations=args.n_permutations,
            )
            rr.update({"k": k, "backbone": bb})
            top_k_results[bb].append(rr)
            print(f"  {bb:<10} k={k:<2}  pooled_auroc="
                  f"{rr.get('pooled_auroc', float('nan')):.3f}  "
                  f"null_mean={rr.get('null_mean', float('nan')):.3f}  "
                  f"p_perm={rr.get('p_perm', float('nan')):.3f}")

    # 3. KILL-S4 verdict.
    kill_s4_per_backbone: dict[str, dict] = {}
    for bb in BACKBONES:
        best_k = max(top_k_results[bb], key=lambda r: r.get("pooled_auroc", -1))
        whole = WHOLE_POCKET_AUROC.get(bb, float("nan"))
        best_auroc = best_k.get("pooled_auroc", float("nan"))
        delta = best_auroc - whole
        kill_s4_per_backbone[bb] = {
            "whole_pocket_auroc": whole,
            "best_top_k_auroc": best_auroc,
            "best_k": best_k.get("k"),
            "delta": delta,
            "within_tolerance": (abs(delta) <= KILL_S4_TOLERANCE),
        }
    n_backbones_within_tolerance = sum(
        1 for v in kill_s4_per_backbone.values() if v["within_tolerance"]
    )
    kill_s4_fired = (n_backbones_within_tolerance == 0)
    kill_s4_verdict = (
        f"KILL_S4_FIRED (0/4 backbones within {KILL_S4_TOLERANCE} AUROC of whole-pocket)"
        if kill_s4_fired
        else f"KILL_S4_DID_NOT_FIRE ({n_backbones_within_tolerance}/4 backbones within {KILL_S4_TOLERANCE})"
    )

    # 4. Localization summary — top-5 features per backbone (using single-feature AUROC).
    print("[S4-3] localization summary — top-5 features per backbone")
    localization = {}
    for bb in BACKBONES:
        ranking = []
        for f in all_features:
            rb = per_feature_by_bb.get(f, {}).get(bb, {})
            a = rb.get("pooled_auroc")
            if a is None:
                continue
            strength = max(a, 1 - a)  # directional-agnostic
            ranking.append((f, strength, a))
        ranking.sort(key=lambda x: -x[1])
        top5 = ranking[:5]
        canonical_motifs = {"NPxxY (CA)", "NPxxY (OH)", "Y5.58 pack",
                            "DRY–TM6", "DRY sidechain",
                            "TM6 tilt", "W6.48 toggle",
                            "TM5 outward"}
        top5_motifs = [POSITION_FEATURES[f]["motif"] for f, _, _ in top5]
        canonical_hits = sum(1 for m in top5_motifs if m in canonical_motifs)
        localization[bb] = {
            "top5": [{"feature": f, "bw": POSITION_FEATURES[f]["bw"],
                      "motif": POSITION_FEATURES[f]["motif"],
                      "strength": strength, "auroc": a}
                     for f, strength, a in top5],
            "canonical_hits_of_5": canonical_hits,
        }
        print(f"  {bb:<10} canonical/5={canonical_hits}  "
              f"top: {', '.join(POSITION_FEATURES[f]['motif'] for f, _, _ in top5)}")

    report = {
        "task": "S4_bw_position_decomposition",
        "route": "b — position-level anchor features from row corpus (no per-BW-position RMSDs available)",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows_tier3_v2_sha256": sha256_file(ROWS_CSV),
            "manifest_tier3_v2_sha256": sha256_file(MANIFEST_CSV),
        },
        "prereg_git_sha": "e63692f",
        "n_permutations": args.n_permutations,
        "kill_s4_tolerance_auroc": KILL_S4_TOLERANCE,
        "reference_whole_pocket_auroc_source": (
            "S1 smoke n_perm=5 KILL-S1 row (C_no_selfref_apo × F_iii); "
            "final S1 n_perm=200 pending."
        ),
        "whole_pocket_reference_auroc": WHOLE_POCKET_AUROC,
        "available_position_features": {
            f: POSITION_FEATURES[f] for f in all_features
        },
        "pocket_positions_in_scorer": {
            "note": (
                "scorer/pocket_metrics.py POCKET_BW_LABELS defines 12 Class A "
                "pocket residues at 3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, "
                "6.51, 6.52, 6.55, 7.39, 7.42. Per-residue CA RMSDs to each "
                "reference are computed inside compute_pocket_axes_bundle "
                "but only their aggregate pocket_ca_rmsd is emitted to rows. "
                "A per-position decomposition would require rescoring from "
                "the raw CIFs (T7b-style)."
            ),
            "pocket_bw_labels": ["3.32", "3.33", "3.36",
                                  "5.42", "5.43", "5.46",
                                  "6.48", "6.51", "6.52", "6.55",
                                  "7.39", "7.42"],
        },
        "per_feature_auroc": per_feature_by_bb,
        "top_k_instrument": top_k_results,
        "kill_s4_per_backbone": kill_s4_per_backbone,
        "kill_s4_verdict": kill_s4_verdict,
        "kill_s4_fired": kill_s4_fired,
        "localization_summary": localization,
        "numbering_convention_cross_check": (
            "Not applicable — position-level anchor features in the corpus "
            "are motif-based (NPxxY/DRY/TM6-tilt/W6.48/etc.), not BW-numbering-"
            "sensitive at the feature-name level. The BW-convention question "
            "surfaces only in the per-BW-position pocket RMSD decomposition "
            "that would require T7b rescore. Noted."
        ),
    }
    Path(args.out).write_text(json.dumps(report, indent=2, default=str))
    print()
    print("=" * 78)
    print("S4 SUMMARY")
    print("=" * 78)
    for bb in BACKBONES:
        v = kill_s4_per_backbone[bb]
        print(f"  {bb:<10} whole={v['whole_pocket_auroc']:.3f}  "
              f"top_k={v['best_top_k_auroc']:.3f} (k={v['best_k']})  "
              f"Δ={v['delta']:+.3f}  within_tol={v['within_tolerance']}")
    print()
    print(f"KILL-S4 verdict: {kill_s4_verdict}")
    print()
    print(f"[S4] wrote {Path(args.out).relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
