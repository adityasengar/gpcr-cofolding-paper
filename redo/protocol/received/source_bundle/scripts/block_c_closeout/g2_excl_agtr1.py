#!/usr/bin/env python3
"""G2 sensitivity — exclude AGTR1 from the 15-receptor S1 set and rerun
the reference-separation vs per-receptor AUROC regression.

Reads:
  - `s1_loro_classifier.json` (per-receptor AUROC per backbone, F_iii C_no_selfref_apo)
  - `reference_separation_pocket_ca.csv` (Block B E4 output)

Writes:
  - `g2_excl_agtr1.json`
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
S1_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s1_loro_classifier.json"
REFSEP_CSV = REPO / "experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv"
OUT_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_excl_agtr1.json"

BACKBONES = ["boltz", "chai", "of3", "protenix"]
KILL_VARIANT = "C_no_selfref_apo"
KILL_FEATURE = "F_iii_pocket_plus_axes"
EXCLUDED = "AGTR1"
RNG_SEED = 20260910


def sha256_file(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def spearman_rho(x, y):
    def rankit(v):
        order = np.argsort(v, kind="mergesort")
        rnk = np.empty(len(v), dtype=float)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            rnk[order[i:j + 1]] = avg
            i = j + 1
        return rnk
    rx = rankit(np.asarray(x, dtype=float))
    ry = rankit(np.asarray(y, dtype=float))
    return float(np.corrcoef(rx, ry)[0, 1])


def ols_slope(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    mx = x.mean(); my = y.mean()
    cov = ((x - mx) * (y - my)).sum()
    varx = ((x - mx) ** 2).sum()
    slope = cov / varx if varx > 0 else float("nan")
    intercept = my - slope * mx
    yhat = intercept + slope * x
    ss_res = ((y - yhat) ** 2).sum()
    ss_tot = ((y - my) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return slope, intercept, r2


def bootstrap(x, y, n_iter=1000, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    n = len(x)
    slopes = np.empty(n_iter); rhos = np.empty(n_iter); r2s = np.empty(n_iter)
    for i in range(n_iter):
        idx = rng.integers(0, n, size=n)
        s, _, r2 = ols_slope(x[idx], y[idx])
        slopes[i] = s; r2s[i] = r2
        try:
            rhos[i] = spearman_rho(x[idx], y[idx])
        except Exception:
            rhos[i] = np.nan
    def ci(v):
        v = v[~np.isnan(v)]
        if len(v) == 0: return [float("nan"), float("nan")]
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {"slope_ci_95": ci(slopes), "rho_ci_95": ci(rhos), "r2_ci_95": ci(r2s),
            "slope_median": float(np.nanmedian(slopes)),
            "rho_median": float(np.nanmedian(rhos))}


def bimodality(v, near_perfect=0.85, inverted=0.30):
    v = np.asarray(v, dtype=float)
    v = v[~np.isnan(v)]
    n = len(v)
    if n == 0: return {"n": 0}
    return {"n": n,
            "n_perfect_ge_0_85": int((v >= near_perfect).sum()),
            "n_inverted_lt_0_30": int((v < inverted).sum()),
            "frac_bimodal": float(((v >= near_perfect).sum() + (v < inverted).sum()) / n)}


def main():
    s1 = json.loads(S1_JSON.read_text())
    per_bb_aur = {}
    for v in s1["variants"]:
        if v.get("variant") != KILL_VARIANT or v.get("feature_set") != KILL_FEATURE:
            continue
        per_bb_aur[v["backbone"]] = {k.upper(): float(x) for k, x in v["per_receptor_auroc"].items()}

    refsep = pd.read_csv(REFSEP_CSV)
    refsep["receptor"] = refsep["receptor"].str.upper()
    refsep_map = dict(zip(refsep["receptor"], refsep["pocket_ca_rmsd_A"]))

    s1_receptors = sorted(per_bb_aur[BACKBONES[0]].keys())
    s1_receptors_excl = [r for r in s1_receptors if r != EXCLUDED]
    assert EXCLUDED in s1_receptors, f"{EXCLUDED} not in S1 set"
    print(f"S1 set: {len(s1_receptors)} receptors")
    print(f"After excluding {EXCLUDED}: {len(s1_receptors_excl)} receptors")

    result = {
        "task": "G2_excl_agtr1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "s1_json": {"path": str(S1_JSON.relative_to(REPO)), "sha256": sha256_file(S1_JSON)},
            "refsep_csv": {"path": str(REFSEP_CSV.relative_to(REPO)), "sha256": sha256_file(REFSEP_CSV)},
        },
        "excluded": EXCLUDED,
        "reason": "AGTR1 recorded as suspect outlier per G2 finding; sensitivity per Section 3 of AGTR1 refassign dispatch",
        "s1_feature_set": KILL_FEATURE,
        "s1_variant": KILL_VARIANT,
        "n_receptors_full": len(s1_receptors),
        "n_receptors_excl": len(s1_receptors_excl),
        "receptors_excl": s1_receptors_excl,
        "per_backbone": {},
    }

    print(f"\n{'backbone':<10} {'slope_full':>12} {'slope_excl':>12} {'rho_full':>10} {'rho_excl':>10} {'r2_full':>10} {'r2_excl':>10}")
    print("-" * 76)
    for bb in BACKBONES:
        # Full 15-set (baseline)
        x_full = np.array([refsep_map[r] for r in s1_receptors if r in refsep_map])
        y_full = np.array([per_bb_aur[bb].get(r, np.nan) for r in s1_receptors if r in refsep_map])
        s_full, i_full, r2_full = ols_slope(x_full, y_full)
        rho_full = spearman_rho(x_full, y_full)
        bs_full = bootstrap(x_full, y_full, n_iter=1000, seed=RNG_SEED + hash(bb) % 10000)
        bim_full = bimodality(y_full)

        # Excluded (14-set)
        x_excl = np.array([refsep_map[r] for r in s1_receptors_excl if r in refsep_map])
        y_excl = np.array([per_bb_aur[bb].get(r, np.nan) for r in s1_receptors_excl if r in refsep_map])
        s_excl, i_excl, r2_excl = ols_slope(x_excl, y_excl)
        rho_excl = spearman_rho(x_excl, y_excl)
        bs_excl = bootstrap(x_excl, y_excl, n_iter=1000, seed=RNG_SEED + 1 + hash(bb) % 10000)
        bim_excl = bimodality(y_excl)

        result["per_backbone"][bb] = {
            "full_15": {
                "n": len(y_full),
                "slope_auroc_per_A": s_full,
                "intercept": i_full,
                "r_squared": r2_full,
                "spearman_rho": rho_full,
                "bootstrap": bs_full,
                "bimodality": bim_full,
            },
            "excl_agtr1_14": {
                "n": len(y_excl),
                "slope_auroc_per_A": s_excl,
                "intercept": i_excl,
                "r_squared": r2_excl,
                "spearman_rho": rho_excl,
                "bootstrap": bs_excl,
                "bimodality": bim_excl,
            },
            "delta": {
                "slope": s_excl - s_full,
                "r2": r2_excl - r2_full,
                "rho": rho_excl - rho_full,
            },
        }

        print(f"{bb:<10} {s_full:>12.3f} {s_excl:>12.3f} {rho_full:>10.3f} {rho_excl:>10.3f} {r2_full:>10.3f} {r2_excl:>10.3f}")

    # Pooled (all backbones stacked)
    x_full_pooled = []; y_full_pooled = []
    x_excl_pooled = []; y_excl_pooled = []
    for bb in BACKBONES:
        for r in s1_receptors:
            if r in refsep_map:
                x_full_pooled.append(refsep_map[r])
                y_full_pooled.append(per_bb_aur[bb].get(r, np.nan))
                if r != EXCLUDED:
                    x_excl_pooled.append(refsep_map[r])
                    y_excl_pooled.append(per_bb_aur[bb].get(r, np.nan))
    x_fp = np.array(x_full_pooled); y_fp = np.array(y_full_pooled)
    x_ep = np.array(x_excl_pooled); y_ep = np.array(y_excl_pooled)
    m_fp = ~np.isnan(y_fp); m_ep = ~np.isnan(y_ep)
    s_fp, i_fp, r2_fp = ols_slope(x_fp[m_fp], y_fp[m_fp])
    s_ep, i_ep, r2_ep = ols_slope(x_ep[m_ep], y_ep[m_ep])
    rho_fp = spearman_rho(x_fp[m_fp], y_fp[m_fp])
    rho_ep = spearman_rho(x_ep[m_ep], y_ep[m_ep])
    bs_fp = bootstrap(x_fp[m_fp], y_fp[m_fp], n_iter=1000, seed=RNG_SEED + 999)
    bs_ep = bootstrap(x_ep[m_ep], y_ep[m_ep], n_iter=1000, seed=RNG_SEED + 1000)

    result["pooled"] = {
        "full_15": {"n": int(m_fp.sum()), "slope": s_fp, "r2": r2_fp, "rho": rho_fp, "bootstrap": bs_fp},
        "excl_agtr1_14": {"n": int(m_ep.sum()), "slope": s_ep, "r2": r2_ep, "rho": rho_ep, "bootstrap": bs_ep},
        "delta": {"slope": s_ep - s_fp, "r2": r2_ep - r2_fp, "rho": rho_ep - rho_fp},
    }

    print("-" * 76)
    print(f"{'pooled':<10} {s_fp:>12.3f} {s_ep:>12.3f} {rho_fp:>10.3f} {rho_ep:>10.3f} {r2_fp:>10.3f} {r2_ep:>10.3f}")
    print()
    print("Slope-CI comparison (pooled):")
    print(f"  full_15:      slope CI = [{bs_fp['slope_ci_95'][0]:.3f}, {bs_fp['slope_ci_95'][1]:.3f}]")
    print(f"  excl_agtr1:   slope CI = [{bs_ep['slope_ci_95'][0]:.3f}, {bs_ep['slope_ci_95'][1]:.3f}]")
    print()
    print("Bimodality (n_inverted_lt_0.30) per backbone:")
    for bb in BACKBONES:
        f = result["per_backbone"][bb]["full_15"]["bimodality"]["n_inverted_lt_0_30"]
        e = result["per_backbone"][bb]["excl_agtr1_14"]["bimodality"]["n_inverted_lt_0_30"]
        print(f"  {bb:<10} full={f}, excl_agtr1={e}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, default=str))
    print(f"\nwrote {OUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
