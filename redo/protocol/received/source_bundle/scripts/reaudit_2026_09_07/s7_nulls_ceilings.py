#!/usr/bin/env python3
"""S7 — nulls, ceilings, and fold-integrity control for signal-recovery.

Two additional analyses beyond what S1 already computes:
  S7b (ceiling): F_iii logreg on the 9 self-reference receptors alone
                 (ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD, OPRK).
  S7c (fold-integrity control): F_iii + DRY/TM5/Y5.58 anchor distances as
                                covariates; report ΔAUROC.

Pre-reg: experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md (e63692f)
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))
from s1_loro_classifier import (  # type: ignore
    _auroc, _fit_predict_logreg, load_and_prep, build_label,
    restrict_to_common_23, loro_evaluate,
    FEATURES_III, SELF_REF_RECEPTORS,
)

FOLD_INTEGRITY_COLS = [
    "d_dry_sidechain_r350cz_e630oe1",  # DRY lock (R3.50-D3.49 sidechain distance)
    "d_tm5_outward_r350_r558_ca",       # TM5 outward
    "d_y558_pack_min_heavy",            # Y5.58 pack
]

FEATURES_III_PLUS_FOLD = FEATURES_III + FOLD_INTEGRITY_COLS

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s7_nulls_ceilings.json"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    print("[S7] loading rows + manifest...")
    df = load_and_prep()
    # Cast fold-integrity columns to numeric.
    for c in FOLD_INTEGRITY_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df_common = restrict_to_common_23(df)
    print(f"[S7] common set n={df_common['receptor_slug'].nunique()}")

    # -------- S7b: ceiling on 9 self-ref receptors, apo arm, F_iii ---------
    print("[S7b] ceiling on 9 self-reference receptors, apo arm, F_iii...")
    df_selfref = df_common[
        df_common["receptor_slug"].isin(SELF_REF_RECEPTORS)
    ].copy()
    ceiling = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_selfref[df_selfref["backbone"].str.lower() == bb].copy()
        sub = sub[sub["arm"] == "apo"].copy()
        pair = build_label(sub, "full_agonist", "neutral_antagonist")
        if len(pair) < 100 or pair["receptor_slug"].nunique() < 5:
            ceiling[bb] = {"reason": "insufficient_data",
                           "n_rows": int(len(pair)),
                           "n_receptors": int(pair["receptor_slug"].nunique())}
            continue
        r = loro_evaluate(pair, FEATURES_III, model="logreg",
                          n_permutations=0)
        r["n_rows"] = int(len(pair))
        r["n_receptors"] = int(pair["receptor_slug"].nunique())
        ceiling[bb] = r
        print(f"  {bb:<9} n_rcp={r['n_receptors']} pooled_auroc={r['pooled_auroc']:.3f}", flush=True)

    # -------- S7c: fold-integrity control on the 14-receptor clean set ------
    print("[S7c] fold-integrity covariate control...")
    df_clean = df_common[~df_common["receptor_slug"].isin(SELF_REF_RECEPTORS)].copy()
    fold_ctrl = {}
    baseline = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df_clean[df_clean["backbone"].str.lower() == bb].copy()
        sub = sub[sub["arm"] == "apo"].copy()
        pair = build_label(sub, "full_agonist", "neutral_antagonist")
        # Baseline: F_iii alone (same rows as S1 KILL row).
        r_base = loro_evaluate(pair, FEATURES_III, model="logreg", n_permutations=0)
        baseline[bb] = {
            "pooled_auroc": r_base["pooled_auroc"],
            "null_mean": r_base["null_pooled_auroc_mean"],
            "p": r_base["permutation_p_value"],
            "n_rows": int(len(pair)),
        }
        # +fold-integrity anchors.
        r_fi = loro_evaluate(pair, FEATURES_III_PLUS_FOLD, model="logreg", n_permutations=0)
        fold_ctrl[bb] = {
            "pooled_auroc": r_fi["pooled_auroc"],
            "null_mean": r_fi["null_pooled_auroc_mean"],
            "p": r_fi["permutation_p_value"],
            "delta_from_baseline": r_fi["pooled_auroc"] - r_base["pooled_auroc"],
        }
        print(f"  {bb:<9} baseline={r_base['pooled_auroc']:.3f}  "
              f"+fold_integrity={r_fi['pooled_auroc']:.3f}  "
              f"Δ={fold_ctrl[bb]['delta_from_baseline']:+.3f}", flush=True)

    # -------- Verdict --------
    ceiling_aurocs = [c.get("pooled_auroc", 0.0) for c in ceiling.values() if "pooled_auroc" in c]
    ceiling_mean = float(np.mean(ceiling_aurocs)) if ceiling_aurocs else float("nan")
    clean_aurocs = [b["pooled_auroc"] for b in baseline.values()]
    clean_mean = float(np.mean(clean_aurocs))
    fold_ctrl_deltas = [f["delta_from_baseline"] for f in fold_ctrl.values()]
    fold_ctrl_max_drop = min(fold_ctrl_deltas)

    verdict = {
        "ceiling_selfref_mean_auroc": ceiling_mean,
        "clean_14_mean_auroc": clean_mean,
        "gap_ceiling_minus_clean": ceiling_mean - clean_mean,
        "fold_integrity_max_drop": fold_ctrl_max_drop,
        "fold_integrity_kills_signal": bool(fold_ctrl_max_drop < -0.10),
    }

    payload = {
        "task": "S7_nulls_ceilings",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv",
                     "sha256": sha(REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv")},
        },
        "prereg_git_sha": "e63692f",
        "n_permutations": 100,
        "s7b_ceiling_selfref": ceiling,
        "s7c_baseline_fiii": baseline,
        "s7c_plus_fold_integrity": fold_ctrl,
        "verdict": verdict,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, default=str))
    print(f"[S7] wrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 78)
    print("S7 verdict:")
    for k, v in verdict.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
