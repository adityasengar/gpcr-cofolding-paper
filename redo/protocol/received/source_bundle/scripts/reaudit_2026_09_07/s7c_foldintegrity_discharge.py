#!/usr/bin/env python3
"""S7c fold-integrity discharge.

The current SIGNAL_RECOVERY_REPORT flags that adding fold-integrity features
(`d_dry_sidechain_r350cz_e630oe1`, `d_npxxy_y558_y753_ca`) as regressors to
F_iii drops LORO AUROC by 0.13-0.22 on 3 of 4 backbones. Two interpretations:

  (a) Fold-quality confound: S1's signal is global structure quality, not
      pocket-conformation encoding of ligand identity.
  (b) L2 regularization artefact: adding correlated features (npxxy_ca vs
      npxxy_oh already in F_iii) pulls the L2 penalty away from optimal.

To distinguish: run the fold-integrity features ALONE as a classifier. If they
classify well by themselves, (a) is supported. If they don't, (a) is refuted.

Also tests broader "fold-only" feature set (all fold-integrity anchors, no
pocket-Cα/sidechain/w648 or ligand-state axes).
"""
from __future__ import annotations

import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))

from s1_loro_classifier import (  # type: ignore
    load_and_prep, restrict_to_common_23, SELF_REF_RECEPTORS, build_label,
    loro_evaluate, _auroc,
)

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s7c_foldintegrity_discharge.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


# Feature sets to test in isolation.
#
# FOLD_ONLY_MINIMAL is the exact pair cited in the current report's S7c warning.
# FOLD_ONLY_BROAD adds every fold-integrity anchor available in the row schema.
FEATURES_FOLD_MINIMAL = [
    "d_dry_sidechain_r350cz_e630oe1",
    "d_npxxy_y558_y753_ca",
]
FEATURES_FOLD_BROAD = FEATURES_FOLD_MINIMAL + [
    "d_tm6_r350_r630_ca",
    "d_gpcrdb_tm6_tilt_246_637_ca",
    "d_npxxy_y558_y753_oh",
]
# Pocket-only baseline (removes fold-integrity anchors from F_iii):
FEATURES_POCKET_ONLY = [
    "_delta",
    "pocket_ca_rmsd",
    "pocket_sidechain_rmsd_active",
    "pocket_sidechain_rmsd_inactive",
    "w648_chi1",
]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n-perm", type=int, default=100)
    p.add_argument("--out", default=str(OUT))
    args = p.parse_args()

    df_all = load_and_prep()
    df_common = restrict_to_common_23(df_all)
    # KILL-S1 row: apo × self-ref-excluded × 14 receptors.
    df_ka = df_common[
        (df_common["arm"] == "apo")
        & (~df_common["receptor_slug"].isin(SELF_REF_RECEPTORS))
    ].copy()

    backbones = ["boltz", "chai", "of3", "protenix"]
    variants = [
        ("A_fold_minimal_only", FEATURES_FOLD_MINIMAL),
        ("B_fold_broad_only", FEATURES_FOLD_BROAD),
        ("C_pocket_only_no_axes", FEATURES_POCKET_ONLY),
    ]

    results = []
    for var_name, feats in variants:
        for bb in backbones:
            sub = df_ka[df_ka["backbone"].str.lower() == bb].copy()
            pair = build_label(sub, "full_agonist", "neutral_antagonist")
            if len(pair) < 200 or pair["receptor_slug"].nunique() < 10:
                results.append({"variant": var_name, "backbone": bb,
                                "reason": "insufficient_data",
                                "n_rows": int(len(pair))})
                continue
            r = loro_evaluate(pair, feats, model="logreg", n_permutations=args.n_perm)
            r.update({"variant": var_name, "backbone": bb, "features": feats,
                      "n_rows": int(len(pair)),
                      "n_receptors": int(pair["receptor_slug"].nunique())})
            results.append(r)
            print(f"  {var_name:<28} {bb:<10} auroc={r['pooled_auroc']:.3f} "
                  f"null_mean={r['null_pooled_auroc_mean']:.3f} p_perm={r['permutation_p_value']:.3f}")

    # Discharge verdict.
    # If FOLD_MINIMAL_ONLY AUROCs are near chance (< 0.60), the confound
    # interpretation (a) is refuted — fold-integrity features alone do NOT
    # classify. If they classify well (>= 0.65), (a) is supported.
    fold_min = [r for r in results if r.get("variant") == "A_fold_minimal_only" and "pooled_auroc" in r]
    fold_min_aurocs = [r["pooled_auroc"] for r in fold_min]
    fold_min_mean = float(np.mean(fold_min_aurocs)) if fold_min_aurocs else float("nan")
    pocket_only = [r for r in results if r.get("variant") == "C_pocket_only_no_axes" and "pooled_auroc" in r]
    pocket_only_aurocs = [r["pooled_auroc"] for r in pocket_only]
    pocket_only_mean = float(np.mean(pocket_only_aurocs)) if pocket_only_aurocs else float("nan")

    verdict = {
        "fold_only_mean_auroc": fold_min_mean,
        "pocket_only_mean_auroc": pocket_only_mean,
    }
    if fold_min_mean < 0.60:
        verdict["confound_interpretation"] = "REFUTED_L2_REG_ARTEFACT"
        verdict["note"] = (
            "Fold-integrity features alone do not classify (mean AUROC < 0.60). "
            "The S7c drop is not a fold-quality confound; it is consistent with "
            "L2 regularization pulling coefficients away from optimum when "
            "correlated features are added. S1 signal survives."
        )
    elif fold_min_mean >= 0.65:
        verdict["confound_interpretation"] = "SUPPORTED_FOLD_QUALITY_CONFOUND"
        verdict["note"] = (
            "Fold-integrity features alone classify (mean AUROC >= 0.65). "
            "S1 signal is largely fold-quality, not pocket-conformation "
            "encoding of ligand identity. Rung 1 discrimination claim needs "
            "restatement — the signal is that the model's overall fold is "
            "different for the two ligand classes."
        )
    else:
        verdict["confound_interpretation"] = "MIXED"
        verdict["note"] = (
            f"Fold-only mean AUROC {fold_min_mean:.3f} is in the ambiguous "
            f"[0.60, 0.65] band. Fold quality carries some but not all of the "
            f"signal. Manuscript should acknowledge partial confound."
        )

    print()
    print("=" * 70)
    print("S7c fold-integrity discharge")
    print("=" * 70)
    print(f"  fold-minimal-only  mean AUROC: {fold_min_mean:.3f}")
    print(f"  pocket-only        mean AUROC: {pocket_only_mean:.3f}")
    print(f"  Verdict: {verdict['confound_interpretation']}")
    print(f"  {verdict['note']}")

    payload = {
        "task": "s7c_foldintegrity_discharge",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_git_sha": "e63692f",
        "n_permutations": args.n_perm,
        "results": results,
        "verdict": verdict,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, default=str))
    print(f"\nWrote {Path(args.out).relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
