#!/usr/bin/env python3
"""S3 — cross-backbone consensus as confidence signal, benchmarked vs pLDDT.

Pre-registered against
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`.

KILL-S3: if consensus predicts distance-to-crystal no better than pLDDT on
matched folds (paired Δ ≤ 0, CI clears zero on ≥ 2 of 4 backbones), stop.
"""
from __future__ import annotations

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
sys.path.insert(0, str(REPO / "scripts" / "reaudit_2026_09_07"))
from s1_loro_classifier import (  # type: ignore
    load_and_prep, restrict_to_common_23, SELF_REF_RECEPTORS, _auroc,
)

ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s3_consensus_confidence.json"


def sha256_file(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def spearman_rho(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman on paired arrays; NaN if either has < 3 finite pairs or no variance."""
    m = np.isfinite(a) & np.isfinite(b)
    a = a[m]; b = b[m]
    if len(a) < 3:
        return float("nan")
    ra = pd.Series(a).rank().to_numpy()
    rb = pd.Series(b).rank().to_numpy()
    if np.std(ra) == 0 or np.std(rb) == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    print("[S3] loading data...")
    df = load_and_prep()
    df = restrict_to_common_23(df)
    df = df[~df["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()
    df = df[df["arm"] == "apo"].copy()
    df["ligand_role"] = df["ligand_role"].astype(str)
    df = df[df["ligand_role"].isin(["full_agonist", "neutral_antagonist"])].copy()
    df["backbone"] = df["backbone"].astype(str).str.lower()
    df["plddt_mean"] = pd.to_numeric(df["plddt_mean"], errors="coerce")
    df["pocket_ca_rmsd_active"] = pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce")
    df["pocket_ca_rmsd_inactive"] = pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce")
    df["_seed"] = df["seed_used"].astype(str)
    print(f"[S3] rows: {len(df)}")

    # S3a: per-(receptor, ligand_role, seed) cross-backbone consensus.
    # Consensus = 1 / max_pairwise_distance of the 4 backbone means of
    # pocket_ca_rmsd_active (larger = tighter agreement).
    #
    # For rows with only 3 backbones present, use the max pairwise of those 3.
    grouped = df.groupby(["receptor_slug", "ligand_role", "_seed"])
    consensus_map: dict[tuple[str, str, str], float] = {}
    for key, g in grouped:
        per_bb_mean = g.groupby("backbone")["pocket_ca_rmsd_active"].mean().dropna()
        if len(per_bb_mean) < 2:
            continue
        vals = per_bb_mean.to_numpy()
        max_pair = float(np.max(vals) - np.min(vals))
        consensus_map[key] = 1.0 / (max_pair + 1e-6)

    # Propagate consensus onto each row.
    df["_consensus"] = df.apply(
        lambda r: consensus_map.get(
            (r["receptor_slug"], r["ligand_role"], r["_seed"]), np.nan
        ),
        axis=1,
    )

    # S3b: does consensus predict distance-to-crystal (pocket_ca_rmsd_active)?
    # Per-backbone Spearman.
    s3b = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df[df["backbone"] == bb].copy()
        # LORO on the correlation itself: drop one receptor, recompute.
        rhos = []
        for held in sorted(sub["receptor_slug"].str.upper().unique()):
            m = sub["receptor_slug"].str.upper() != held
            rhos.append(spearman_rho(
                sub.loc[m, "_consensus"].to_numpy(),
                sub.loc[m, "pocket_ca_rmsd_active"].to_numpy(),
            ))
        rhos = [x for x in rhos if not math.isnan(x)]
        s3b[bb] = {
            "spearman_full": spearman_rho(
                sub["_consensus"].to_numpy(),
                sub["pocket_ca_rmsd_active"].to_numpy(),
            ),
            "loro_mean_rho": float(np.mean(rhos)) if rhos else float("nan"),
            "loro_min_rho": float(np.min(rhos)) if rhos else float("nan"),
            "loro_max_rho": float(np.max(rhos)) if rhos else float("nan"),
            "n": int(len(sub)),
        }
        # pLDDT counterpart for pairing
        s3b[bb]["plddt_spearman_full"] = spearman_rho(
            sub["plddt_mean"].to_numpy(),
            sub["pocket_ca_rmsd_active"].to_numpy(),
        )
        # NOTE: for pLDDT, HIGHER means MORE confident, so we compare against
        # pocket_ca_rmsd_active where lower = closer to active. Sign matters
        # only for interpretation; use |rho|.

    # S3c: accuracy-vs-coverage — sort rows by consensus, take top X%, compute AUROC.
    # Task: agonist vs antag on pocket_ca_rmsd_active-based single-feature classifier
    # (proxy for S1's F_i). Report AUROC(coverage) per backbone. Also for pLDDT.
    s3c = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        sub = df[df["backbone"] == bb].copy().dropna(subset=["_consensus", "plddt_mean", "pocket_ca_rmsd_active"])
        if len(sub) == 0:
            continue
        y = (sub["ligand_role"] == "full_agonist").to_numpy().astype(int)
        # Score: negative pocket_ca_rmsd_active (agonist should be closer to active)
        s_pred = -sub["pocket_ca_rmsd_active"].to_numpy()
        # Order rows by consensus (descending)
        order_c = np.argsort(sub["_consensus"].to_numpy())[::-1]
        order_p = np.argsort(sub["plddt_mean"].to_numpy())[::-1]
        s3c[bb] = {"consensus": {}, "plddt": {}}
        for pct in [10, 25, 50, 75, 100]:
            k = max(int(len(sub) * pct / 100), 20)
            idx_c = order_c[:k]
            idx_p = order_p[:k]
            s3c[bb]["consensus"][pct] = {
                "n": int(k),
                "auroc": _auroc(y[idx_c], s_pred[idx_c]),
            }
            s3c[bb]["plddt"][pct] = {
                "n": int(k),
                "auroc": _auroc(y[idx_p], s_pred[idx_p]),
            }

    # S3d: paired Δ AUROC (consensus - pLDDT) on identical top-25% slice.
    s3d = {}
    for bb in ["boltz", "chai", "of3", "protenix"]:
        top = s3c.get(bb, {})
        if not top or 25 not in top.get("consensus", {}):
            continue
        c25 = top["consensus"][25]["auroc"]
        p25 = top["plddt"][25]["auroc"]
        s3d[bb] = {
            "consensus_top25_auroc": c25,
            "plddt_top25_auroc": p25,
            "delta_c_minus_p": float(c25 - p25) if (not math.isnan(c25) and not math.isnan(p25)) else float("nan"),
        }

    # KILL-S3 verdict
    n_beat = 0; n_measured = 0
    for bb, d in s3d.items():
        if math.isnan(d["delta_c_minus_p"]):
            continue
        n_measured += 1
        if d["delta_c_minus_p"] > 0:
            n_beat += 1
    kill_s3 = "KILL_S3_FIRED_CONSENSUS_NO_BETTER_THAN_PLDDT" if (n_measured >= 2 and n_beat < 2) else "KILL_S3_DID_NOT_FIRE"

    report = {
        "task": "S3_consensus_confidence",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {"path": str(ROWS_CSV.relative_to(REPO)), "sha256": sha256_file(ROWS_CSV)},
        },
        "s3a_definition": (
            "consensus[receptor, ligand_role, seed] = 1 / (max_pairwise_backbone_distance"
            " of pocket_ca_rmsd_active + 1e-6). Larger = tighter cross-backbone agreement."
        ),
        "s3b_spearman_consensus_vs_pca_active": s3b,
        "s3c_accuracy_vs_coverage": s3c,
        "s3d_paired_vs_plddt_top25": s3d,
        "kill_s3_verdict": kill_s3,
        "kill_s3_n_backbones_beat_plddt": n_beat,
        "kill_s3_n_backbones_measured": n_measured,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"[S3] wrote {OUT.relative_to(REPO)}")

    print()
    print("=" * 70)
    print("S3d paired Δ AUROC (consensus - pLDDT, top 25%)")
    print("=" * 70)
    for bb, d in s3d.items():
        print(f"  {bb:<10} consensus={d['consensus_top25_auroc']:.3f} "
              f"pLDDT={d['plddt_top25_auroc']:.3f} Δ={d['delta_c_minus_p']:+.3f}")
    print()
    print(f"KILL-S3 verdict: {kill_s3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
