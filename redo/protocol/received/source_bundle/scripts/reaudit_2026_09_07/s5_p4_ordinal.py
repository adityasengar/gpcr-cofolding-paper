#!/usr/bin/env python3
"""S5 — recover P4 ordinal test on the continuous pocket axis.

Pre-reg P4: inverse_agonist < neutral_antagonist < none < full_agonist.
Tier 3 has {decoy_lig, neutral_antagonist, full_agonist}; Tier 1 has all 5.
Test on continuous Δ = pocket_ca_rmsd_active - pocket_ca_rmsd_inactive.

Per-receptor Kendall's τ + p-value. Fraction ≥ threshold.
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
)

OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s5_p4_ordinal.json"

# Expected pharmacology ordering on ΔactiveInactive: agonist most negative
# (pocket close to active), antag most positive (pocket close to inactive).
LIGAND_ORDER = {
    "full_agonist": 0,        # lowest Δ expected
    "none": 1,                 # apo, middle
    "decoy_lig": 1,           # decoy sits with apo (no chemistry)
    "neutral_antagonist": 2,  # highest Δ
    "inverse_agonist": 3,     # highest Δ (past antag)
}


def kendall_tau_p(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Kendall's τ_b + two-sided p-value via normal approximation."""
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]; y = y[m]
    n = len(x)
    if n < 4:
        return float("nan"), float("nan")
    concordant = 0; discordant = 0; tie_x = 0; tie_y = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[i] - x[j]; dy = y[i] - y[j]
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tie_x += 1
            elif dy == 0:
                tie_y += 1
            elif (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                concordant += 1
            else:
                discordant += 1
    total = concordant + discordant + tie_x + tie_y
    if total == 0:
        return float("nan"), float("nan")
    # tau_b
    denom = math.sqrt((concordant + discordant + tie_x) * (concordant + discordant + tie_y))
    if denom == 0:
        return float("nan"), float("nan")
    tau = (concordant - discordant) / denom
    # p-value via normal approx
    var = (2 * (2 * n + 5)) / (9 * n * (n - 1))
    z = tau / math.sqrt(var) if var > 0 else float("nan")
    from math import erf
    p_two = 2 * (1 - 0.5 * (1 + erf(abs(z) / math.sqrt(2))))
    return tau, p_two


def analyze_tier(df: pd.DataFrame, arm: str = "apo") -> dict:
    """Per-(receptor, backbone), compute Kendall's τ between ligand-role rank
    and Δ = pocket_ca_rmsd_active - pocket_ca_rmsd_inactive."""
    df = df.copy()
    df["_delta"] = pd.to_numeric(df["pocket_ca_rmsd_active"], errors="coerce") - pd.to_numeric(df["pocket_ca_rmsd_inactive"], errors="coerce")
    df["_ord"] = df["ligand_role"].map(LIGAND_ORDER)
    df = df.dropna(subset=["_ord"])
    df = df[df["arm"] == arm]

    out = {}
    for bb in sorted(df["backbone"].str.lower().unique()):
        sub_bb = df[df["backbone"].str.lower() == bb]
        per_rec = {}
        for rec in sorted(sub_bb["receptor_slug"].str.upper().unique()):
            sub = sub_bb[sub_bb["receptor_slug"].str.upper() == rec]
            tau, p = kendall_tau_p(sub["_ord"].to_numpy(dtype=float), sub["_delta"].to_numpy())
            per_rec[rec] = {"tau": tau, "p": p, "n_rows": int(len(sub))}
        out[bb] = per_rec
    return out


def summarize(per_backbone: dict, threshold_p: float = 0.05) -> dict:
    """Report per-backbone: fraction of receptors with τ > 0 AND p < threshold_p."""
    summary = {}
    for bb, per_rec in per_backbone.items():
        n_total = len(per_rec)
        n_positive_sig = sum(
            1 for d in per_rec.values()
            if not math.isnan(d["tau"]) and d["tau"] > 0 and d["p"] < threshold_p
        )
        n_positive = sum(1 for d in per_rec.values() if not math.isnan(d["tau"]) and d["tau"] > 0)
        summary[bb] = {
            "n_receptors": n_total,
            "n_tau_positive": n_positive,
            "n_tau_positive_and_p_lt_thresh": n_positive_sig,
            "fraction_positive": n_positive / n_total if n_total else float("nan"),
            "fraction_positive_significant": n_positive_sig / n_total if n_total else float("nan"),
        }
    return summary


def main():
    print("[S5] loading Tier 3...")
    df3 = load_and_prep()
    df3 = restrict_to_common_23(df3)
    df3_sr_ex = df3[~df3["receptor_slug"].str.upper().isin(SELF_REF_RECEPTORS)].copy()
    print(f"[S5] Tier 3 rows (23 common): {len(df3)} | self-ref-excluded (15): {len(df3_sr_ex)}")

    tier3_23 = analyze_tier(df3, arm="apo")
    tier3_15 = analyze_tier(df3_sr_ex, arm="apo")

    tier3_23_summary = summarize(tier3_23)
    tier3_15_summary = summarize(tier3_15)

    # Tier 1 — read rows.tier1.csv
    tier1_csv = REPO / "experiments/020_block_c_ligand_pharmacology/analysis/rows.tier1.csv"
    manifest_tier1 = REPO / "experiments/020_block_c_ligand_pharmacology/analysis/rescore_manifest.tier1.csv"
    print(f"[S5] loading Tier 1 from {tier1_csv.name}...")
    t1 = pd.read_csv(tier1_csv, low_memory=False)
    m1 = pd.read_csv(manifest_tier1, low_memory=False)
    mi = m1.set_index("prediction_path")
    t1["backbone"] = t1["input_path"].map(mi["backbone"].to_dict()).fillna("")
    t1["partner_type"] = t1["input_path"].map(mi["partner_type"].to_dict()).fillna("")
    t1["ligand_role"] = t1["input_path"].map(mi["ligand_role"].to_dict()).fillna(t1.get("ligand_role", pd.Series([""] * len(t1))))
    t1["arm"] = t1["partner_type"].apply(lambda p: "apo" if str(p).lower() == "apo" else "cognate")
    t1 = t1[(t1["receptor_class"].fillna("").astype(str).str.upper() == "A") & (t1["passed"].astype(str).str.lower() == "true")].copy()
    t1["receptor_slug"] = t1["receptor_slug"].astype(str).str.upper()

    if "pocket_ca_rmsd_active" not in t1.columns:
        # Tier 1 corpus predates the dual-reference companion columns.
        # Fall back to using pocket_ca_rmsd (against role-matched reference).
        print("[S5] Tier 1 lacks dual-ref columns; using pocket_ca_rmsd as proxy.")
        t1["pocket_ca_rmsd_active"] = pd.to_numeric(t1["pocket_ca_rmsd"], errors="coerce")
        t1["pocket_ca_rmsd_inactive"] = 0.0  # so _delta reduces to pocket_ca_rmsd
    tier1 = analyze_tier(t1, arm="apo")
    tier1_summary = summarize(tier1)

    report = {
        "task": "S5_p4_ordinal_continuous",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_git_sha": "e63692f",
        "note": (
            "Kendall's tau_b between ligand-role rank (agonist=0, apo/decoy=1, "
            "antag=2, inverse=3) and Δ = pocket_ca_rmsd_active - pocket_ca_rmsd_inactive. "
            "Positive tau = expected pharmacology direction."
        ),
        "tier3_apo_23_receptors": {
            "per_backbone": tier3_23,
            "summary": tier3_23_summary,
        },
        "tier3_apo_15_receptors_selfref_excluded": {
            "per_backbone": tier3_15,
            "summary": tier3_15_summary,
        },
        "tier1_apo": {
            "per_backbone": tier1,
            "summary": tier1_summary,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"wrote {OUT.relative_to(REPO)}")
    print()
    print("=" * 78)
    print("S5 — P4 ordinal recovery on the continuous axis")
    print("=" * 78)
    print(f"{'panel':<25} {'backbone':<10} {'fract_pos':>10} {'fract_sig':>10} {'n_rec':>6}")
    for name, summ in [
        ("Tier3 apo 23", tier3_23_summary),
        ("Tier3 apo 15 (no-selfref)", tier3_15_summary),
        ("Tier1 apo (5-class)", tier1_summary),
    ]:
        for bb, d in summ.items():
            print(f"{name:<25} {bb:<10} {d['fraction_positive']:>10.3f} "
                  f"{d['fraction_positive_significant']:>10.3f} {d['n_receptors']:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
