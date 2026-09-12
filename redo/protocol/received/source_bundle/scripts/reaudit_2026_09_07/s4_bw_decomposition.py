#!/usr/bin/env python3
"""S4 — per-feature contribution + minimal instrument.

Pre-registered against
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`.

Approach: since re-running scorer for per-BW-position CA distances requires HPC
CIF access, decompose signal at the FEATURE level (each of 8 F_iii features).
Each feature maps to canonical GPCR interpretation. Report per-feature LORO
AUROC and top-k reduced instrument (k=3, 5).

KILL-S4 (secondary): if top-k ≤ 10 doesn't match F_iii within 0.03 AUROC on
LORO apo × self-ref-excluded, keep F_iii as reference readout.
"""
from __future__ import annotations

import hashlib, json, sys
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

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s4_bw_decomposition.json"

CANONICAL_LABELS = {
    "_delta": "pocket-Cα (active - inactive) — aggregate pocket difference",
    "pocket_ca_rmsd": "pocket-Cα RMSD to routed reference — aggregate pocket",
    "pocket_sidechain_rmsd_active": "pocket sidechain RMSD to active reference",
    "pocket_sidechain_rmsd_inactive": "pocket sidechain RMSD to inactive reference",
    "w648_chi1": "W6.48 chi1 dihedral — toggle switch",
    "d_npxxy_y558_y753_oh": "NPxxY-OH distance (Y5.58 – Y7.53) — TM7 side chain",
    "d_gpcrdb_tm6_tilt_246_637_ca": "TM6 tilt (2.46 – 6.37 Cα) — canonical activation lever",
    "d_tm6_r350_r630_ca": "TM6 (3.50 – 6.30 Cα) — canonical activation distance",
}


def sha256_file(p):
    import hashlib
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def loro_auroc(sub: pd.DataFrame, features: list[str], model: str = "logreg") -> tuple[float, dict]:
    receptors = sorted(sub["receptor_slug"].str.upper().unique())
    all_s = []; all_y = []
    per_rec = {}
    for held in receptors:
        tr = sub[sub["receptor_slug"].str.upper() != held]
        te = sub[sub["receptor_slug"].str.upper() == held]
        Xtr = tr[features].to_numpy(dtype=float)
        ytr = tr["_label"].to_numpy(dtype=int)
        Xte = te[features].to_numpy(dtype=float)
        yte = te["_label"].to_numpy(dtype=int)
        m = np.isfinite(Xtr).all(axis=1)
        Xtr = Xtr[m]; ytr = ytr[m]
        m2 = np.isfinite(Xte).all(axis=1)
        Xte = Xte[m2]; yte = yte[m2]
        if len(np.unique(ytr)) < 2 or len(ytr) < 20 or len(Xte) == 0:
            continue
        if model == "logreg" and Xtr.shape[1] > 1:
            s = _fit_predict_logreg(Xtr, ytr, Xte)
        else:
            # threshold on single feature; sign auto-picked by training AUROC
            train_auc = _auroc(ytr, Xtr[:, 0])
            sign = 1 if train_auc >= 0.5 else -1
            s = sign * Xte[:, 0]
        all_s.append(s); all_y.append(yte)
        per_rec[held] = float(_auroc(yte, s))
    if not all_s:
        return float("nan"), {}
    return float(_auroc(np.concatenate(all_y), np.concatenate(all_s))), per_rec


def main():
    print("[S4] loading data...")
    df = load_and_prep()
    df = restrict_to_common_23(df)
    df = df[~df["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()
    df = df[df["arm"] == "apo"].copy()
    df["ligand_role"] = df["ligand_role"].astype(str)
    df = df[df["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    df["_label"] = (df["ligand_role"] == "full_agonist").astype(int)
    df["backbone"] = df["backbone"].astype(str).str.lower()

    # S4a: per-feature LORO AUROC.
    per_feature = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub_bb = df[df["backbone"] == bb].copy()
        per_feature[bb] = {}
        for feat in FEATURES_III:
            auc, _ = loro_auroc(sub_bb, [feat], model="threshold")
            per_feature[bb][feat] = auc
            print(f"  {bb:<10} {feat:<35} single-feat AUROC={auc:.3f}")

    # S4b: rank top-3 per backbone; label with canonical name.
    localization = {}
    for bb, feats in per_feature.items():
        ranked = sorted(feats.items(), key=lambda kv: -abs(kv[1] - 0.5))[:3]
        localization[bb] = [
            {"feature": f, "auroc": v, "canonical": CANONICAL_LABELS.get(f, f)}
            for f, v in ranked
        ]

    # S4c: reduced instrument at k=3, 5. Selection INSIDE training fold.
    reduced_instrument = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub_bb = df[df["backbone"] == bb].copy()
        # For each fold, rank features on training set, pick top-k, evaluate on held-out.
        for k in [3, 5]:
            # Fold-internal selection + evaluation
            receptors = sorted(sub_bb["receptor_slug"].str.upper().unique())
            all_s = []; all_y = []
            for held in receptors:
                tr = sub_bb[sub_bb["receptor_slug"].str.upper() != held]
                te = sub_bb[sub_bb["receptor_slug"].str.upper() == held]
                # Rank features on training set by absolute-deviation-from-0.5 AUROC
                feat_scores = {}
                for f in FEATURES_III:
                    Xtr_f = tr[f].to_numpy(dtype=float)
                    ytr = tr["_label"].to_numpy(dtype=int)
                    m = np.isfinite(Xtr_f)
                    if m.sum() < 20:
                        feat_scores[f] = 0.5
                        continue
                    feat_scores[f] = _auroc(ytr[m], Xtr_f[m])
                # Select top-k by |auroc - 0.5|
                top_k = sorted(feat_scores.items(), key=lambda kv: -abs(kv[1] - 0.5))[:k]
                top_feats = [f for f, _ in top_k]
                Xtr = tr[top_feats].to_numpy(dtype=float)
                ytr = tr["_label"].to_numpy(dtype=int)
                Xte = te[top_feats].to_numpy(dtype=float)
                yte = te["_label"].to_numpy(dtype=int)
                m = np.isfinite(Xtr).all(axis=1)
                Xtr = Xtr[m]; ytr = ytr[m]
                m2 = np.isfinite(Xte).all(axis=1)
                Xte = Xte[m2]; yte = yte[m2]
                if len(np.unique(ytr)) < 2 or len(Xte) == 0:
                    continue
                s = _fit_predict_logreg(Xtr, ytr, Xte)
                all_s.append(s); all_y.append(yte)
            if all_s:
                pooled = float(_auroc(np.concatenate(all_y), np.concatenate(all_s)))
            else:
                pooled = float("nan")
            reduced_instrument.setdefault(bb, {})[f"k_{k}"] = pooled
            print(f"  {bb:<10} k={k} reduced-instrument LORO AUROC={pooled:.3f}")

    # KILL-S4: compare to F_iii benchmarks. Read from s1 output.
    s1_out_path = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s1_loro_classifier.json"
    s1_out = json.loads(s1_out_path.read_text())
    f_iii = {}
    for v in s1_out["variants"]:
        if v.get("variant") == "C_no_selfref_apo" and v.get("feature_set") == "F_iii_pocket_plus_axes":
            f_iii[v["backbone"]] = v.get("pooled_auroc", float("nan"))

    kill_s4_fires = 0
    kill_s4_details = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        f3 = f_iii.get(bb, float("nan"))
        r_k3 = reduced_instrument.get(bb, {}).get("k_3", float("nan"))
        r_k5 = reduced_instrument.get(bb, {}).get("k_5", float("nan"))
        best_r = max(r_k3, r_k5) if not (np.isnan(r_k3) and np.isnan(r_k5)) else float("nan")
        gap = f3 - best_r if not (np.isnan(f3) or np.isnan(best_r)) else float("nan")
        kill_s4_details[bb] = {
            "f_iii_auroc": f3, "k3_auroc": r_k3, "k5_auroc": r_k5,
            "best_reduced": best_r, "gap_full_minus_reduced": gap,
        }
        if not np.isnan(gap) and gap > 0.03:
            kill_s4_fires += 1
    verdict = "KILL_S4_FIRED_REDUCED_UNDERPERFORMS" if kill_s4_fires >= 2 else "KILL_S4_DID_NOT_FIRE"

    report = {
        "task": "S4_per_feature_and_reduced",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "s4a_per_feature_loro_auroc": per_feature,
        "s4b_top3_per_backbone": localization,
        "s4c_reduced_instrument_loro_auroc": reduced_instrument,
        "kill_s4_details": kill_s4_details,
        "kill_s4_verdict": verdict,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"\nwrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 60)
    print("S4 verdict:", verdict)
    for bb, d in kill_s4_details.items():
        print(f"  {bb:<10} f_iii={d['f_iii_auroc']:.3f} k5={d['k5_auroc']:.3f} gap={d['gap_full_minus_reduced']:+.3f}")
    print()
    print("S4b top features per backbone:")
    for bb, feats in localization.items():
        print(f"  {bb}:")
        for f in feats:
            print(f"    {f['feature']:<35} AUROC={f['auroc']:.3f}  {f['canonical']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
