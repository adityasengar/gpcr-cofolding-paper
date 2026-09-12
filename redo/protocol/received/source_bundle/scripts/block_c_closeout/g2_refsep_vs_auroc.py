#!/usr/bin/env python3
"""G2 — reference-separation vs per-receptor AUROC.

Regress per-receptor S1 LORO AUROC (from
`signal_recovery_2026_09_07/s1_loro_classifier.json`, variant
`C_no_selfref_apo` × F_iii × each backbone) against pocket-Cα RMSD
between each receptor's active and inactive references (from
`experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`,
Block B E4-adjacent O-3 output, SHA ed850577…).

Deliverables:
 - Regression per backbone: slope + CI + fraction of bimodality explained.
 - Applicability-domain threshold (if signal supported): the pocket-Cα-RMSD
   value above which method reliability crosses AUROC 0.7 (say).
 - AGTR1 counterexample test (well-separated on tilt 19.09 vs 11.23; does
   it fit pocket-Cα or break the account).
 - Fold-integrity-finite 10-receptor subset origin test (whether Check 2's
   subset draws from low-separation mode).

Outputs:
 - JSON at experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_refsep_vs_auroc.json
 - CSV table at same dir/g2_refsep_vs_auroc.csv
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
FI_JSON = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/check2_fi_finite_subset.json"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification"
OUT_JSON = OUT_DIR / "g2_refsep_vs_auroc.json"
OUT_CSV = OUT_DIR / "g2_refsep_vs_auroc.csv"

BACKBONES = ["boltz", "chai", "of3", "protenix"]
KILL_VARIANT = "C_no_selfref_apo"
KILL_FEATURE = "F_iii_pocket_plus_axes"

RNG_SEED = 20260910


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    """Spearman rank correlation, tie-average ranks."""
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


def ols_slope(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """OLS regression y = a + b*x. Return (slope, intercept, r_squared)."""
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


def bootstrap_slope(x: np.ndarray, y: np.ndarray, n_iter: int = 1000, seed: int = RNG_SEED) -> dict:
    """Receptor-bootstrap CI on OLS slope + Spearman rho."""
    rng = np.random.default_rng(seed)
    n = len(x)
    slopes = np.empty(n_iter); rhos = np.empty(n_iter); r2s = np.empty(n_iter)
    for i in range(n_iter):
        idx = rng.integers(0, n, size=n)
        xb, yb = x[idx], y[idx]
        s, _, r2 = ols_slope(xb, yb)
        slopes[i] = s; r2s[i] = r2
        try:
            rhos[i] = spearman_rho(xb, yb)
        except Exception:
            rhos[i] = np.nan
    def ci(v):
        v = v[~np.isnan(v)]
        if len(v) == 0:
            return [float("nan"), float("nan")]
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {
        "slope_ci_95": ci(slopes),
        "rho_ci_95": ci(rhos),
        "r_squared_ci_95": ci(r2s),
        "slope_bootstrap_median": float(np.nanmedian(slopes)),
        "rho_bootstrap_median": float(np.nanmedian(rhos)),
        "r_squared_bootstrap_median": float(np.nanmedian(r2s)),
    }


def bimodality_frac(auroc_vals: np.ndarray, near_perfect: float = 0.85, inverted: float = 0.30) -> dict:
    """Fraction near-perfect (≥ 0.85), fraction inverted (< 0.30), fraction middle."""
    v = np.asarray(auroc_vals, dtype=float)
    v = v[~np.isnan(v)]
    n = len(v)
    if n == 0:
        return {"n": 0}
    n_perfect = int((v >= near_perfect).sum())
    n_inverted = int((v < inverted).sum())
    n_middle = n - n_perfect - n_inverted
    return {
        "n": n, "n_perfect_ge_0_85": n_perfect,
        "n_inverted_lt_0_30": n_inverted, "n_middle": n_middle,
        "frac_bimodal": (n_perfect + n_inverted) / n,
    }


def main():
    # ------------------------------------------------------------
    # Load per-receptor AUROC from S1 JSON (variant C_no_selfref_apo × F_iii)
    # ------------------------------------------------------------
    s1 = json.loads(S1_JSON.read_text())
    per_backbone_auroc: dict[str, dict[str, float]] = {}
    for v in s1["variants"]:
        if v.get("variant") != KILL_VARIANT or v.get("feature_set") != KILL_FEATURE:
            continue
        bb = v["backbone"]
        per_backbone_auroc[bb] = {k.upper(): float(x) for k, x in v["per_receptor_auroc"].items()}
    assert set(per_backbone_auroc) == set(BACKBONES), f"missing backbone: {set(BACKBONES) - set(per_backbone_auroc)}"

    # ------------------------------------------------------------
    # Load pocket-Ca reference separation table
    # ------------------------------------------------------------
    refsep = pd.read_csv(REFSEP_CSV)
    refsep["receptor"] = refsep["receptor"].str.upper()
    refsep_map = dict(zip(refsep["receptor"], refsep["pocket_ca_rmsd_A"]))
    tilt_delta_map = dict(zip(refsep["receptor"], refsep["delta_ref_tilt_A"]))
    npxxy_delta_map = dict(zip(refsep["receptor"], refsep["delta_ref_npxxy_A"]))

    # S1 15-receptor set (per JSON variant 24-35 keys)
    s1_receptors = sorted(per_backbone_auroc[BACKBONES[0]].keys())
    assert len(s1_receptors) == 15, f"expected 15 receptors, got {len(s1_receptors)}"

    # ------------------------------------------------------------
    # Assemble long-format table: (receptor, backbone, auroc, pocket_ca_sep, tilt_sep, npxxy_sep)
    # ------------------------------------------------------------
    rows = []
    missing_refsep = []
    for rec in s1_receptors:
        if rec not in refsep_map:
            missing_refsep.append(rec)
            continue
        for bb in BACKBONES:
            rows.append({
                "receptor": rec,
                "backbone": bb,
                "auroc": per_backbone_auroc[bb].get(rec, float("nan")),
                "pocket_ca_sep": refsep_map[rec],
                "tilt_delta": tilt_delta_map[rec],
                "npxxy_delta": npxxy_delta_map[rec],
            })
    tbl = pd.DataFrame(rows)

    # ------------------------------------------------------------
    # Per-backbone regression: AUROC vs pocket_ca_sep
    # ------------------------------------------------------------
    regressions = {}
    for bb in BACKBONES:
        sub = tbl[tbl["backbone"] == bb].dropna(subset=["auroc", "pocket_ca_sep"])
        x = sub["pocket_ca_sep"].values
        y = sub["auroc"].values
        slope, intercept, r2 = ols_slope(x, y)
        rho = spearman_rho(x, y)
        boot = bootstrap_slope(x, y, n_iter=1000, seed=RNG_SEED + hash(bb) % 100000)
        bim = bimodality_frac(y)
        regressions[bb] = {
            "n_receptors": int(len(sub)),
            "slope_auroc_per_A": slope,
            "intercept": intercept,
            "r_squared": r2,
            "spearman_rho": rho,
            "bootstrap": boot,
            "bimodality": bim,
        }

    # ------------------------------------------------------------
    # Pooled regression (all 4 backbones stacked)
    # ------------------------------------------------------------
    sub = tbl.dropna(subset=["auroc", "pocket_ca_sep"])
    x = sub["pocket_ca_sep"].values
    y = sub["auroc"].values
    ps, pint, pr2 = ols_slope(x, y)
    p_rho = spearman_rho(x, y)
    pooled_boot = bootstrap_slope(x, y, n_iter=1000, seed=RNG_SEED)
    pooled_bim = bimodality_frac(y)

    # ------------------------------------------------------------
    # Applicability-domain threshold: what pocket_ca_sep threshold above which
    # median (or fraction ≥ 0.7) is achieved?
    # ------------------------------------------------------------
    # Sort receptors by pocket_ca_sep ascending; compute rolling reliability.
    thresholds = []
    for bb in BACKBONES:
        sub = tbl[tbl["backbone"] == bb].dropna(subset=["auroc", "pocket_ca_sep"]).sort_values("pocket_ca_sep")
        vals = sub["pocket_ca_sep"].values
        aurocs = sub["auroc"].values
        # For each candidate threshold τ (excluding min/max), compute median AUROC on those ≥ τ.
        # Find smallest τ where median AUROC(≥τ) ≥ 0.85 and no inversions (< 0.3) remain.
        best_tau = None; best_frac_reliable = None
        for i in range(len(vals)):
            tau = vals[i]
            aurocs_above = aurocs[i:]
            if len(aurocs_above) < 5:
                break
            med = float(np.median(aurocs_above))
            n_inv = int((aurocs_above < 0.30).sum())
            frac_reliable = float((aurocs_above >= 0.85).mean())
            if med >= 0.85 and n_inv == 0 and (best_tau is None):
                best_tau = tau
                best_frac_reliable = frac_reliable
        thresholds.append({
            "backbone": bb,
            "threshold_pocket_ca_A": best_tau,
            "frac_reliable_above": best_frac_reliable,
        })

    # ------------------------------------------------------------
    # AGTR1 counterexample: well-separated on tilt (19.09 - 11.23 = 7.86 Å per dispatch),
    # BUT what's its pocket_ca_sep and its AUROC?
    # ------------------------------------------------------------
    agtr1 = {}
    if "AGTR1" in refsep_map:
        agtr1_pocket_sep = float(refsep_map["AGTR1"])
        agtr1_tilt_delta = float(tilt_delta_map["AGTR1"])
        agtr1_npxxy_delta = float(npxxy_delta_map["AGTR1"])
        agtr1 = {
            "pocket_ca_sep_A": agtr1_pocket_sep,
            "delta_ref_tilt_A": agtr1_tilt_delta,
            "delta_ref_npxxy_A": agtr1_npxxy_delta,
            "per_backbone_auroc": {bb: per_backbone_auroc[bb].get("AGTR1") for bb in BACKBONES},
            "pocket_ca_rank_in_40": int(refsep[refsep["receptor"] == "AGTR1"]["pocket_ca_rank_of_40"].iloc[0]),
        }
        # Compare AGTR1's pocket_ca_sep to the S1 15-receptor set distribution
        s1_pockets = np.array([refsep_map[r] for r in s1_receptors if r in refsep_map])
        agtr1["pocket_ca_percentile_in_s1_15"] = float((s1_pockets < agtr1_pocket_sep).mean() * 100)
        agtr1["interpretation"] = (
            "AGTR1 well-separated on tilt (Δ_ref_tilt=%.2f Å) but pocket_ca_sep=%.2f Å "
            "(rank %d/40 in Block B panel, percentile %.0f%% in S1 15-set). "
            "Test: does AGTR1 fit the pocket_ca account (should invert if pocket_ca is small) "
            "or break it (if pocket_ca is large and AUROC still inverts)."
        ) % (agtr1_tilt_delta, agtr1_pocket_sep, agtr1["pocket_ca_rank_in_40"], agtr1["pocket_ca_percentile_in_s1_15"])

    # ------------------------------------------------------------
    # Fold-integrity 10-receptor subset test (Check 2)
    # ------------------------------------------------------------
    fi_result = {}
    if FI_JSON.exists():
        try:
            fi = json.loads(FI_JSON.read_text())
            fi_receptors = None
            for k in ("fi_finite_receptors", "receptors", "subset_receptors", "n_receptors", "receptor_list"):
                if k in fi:
                    val = fi[k]
                    if isinstance(val, list):
                        fi_receptors = [r.upper() for r in val]
                        break
            if fi_receptors:
                fi_pockets = [refsep_map[r] for r in fi_receptors if r in refsep_map]
                s1_pockets = np.array([refsep_map[r] for r in s1_receptors if r in refsep_map])
                fi_result = {
                    "fi_receptors": fi_receptors,
                    "n_receptors_in_refsep": len(fi_pockets),
                    "fi_pocket_ca_median": float(np.median(fi_pockets)) if fi_pockets else None,
                    "s1_pocket_ca_median": float(np.median(s1_pockets)),
                    "n_below_s1_median": int(sum(p < np.median(s1_pockets) for p in fi_pockets)),
                    "expected_random_below_median": len(fi_pockets) * 0.5,
                }
        except Exception as e:
            fi_result["error"] = str(e)

    # ------------------------------------------------------------
    # Report
    # ------------------------------------------------------------
    report = {
        "task": "G2_refsep_vs_auroc",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "s1_json": {"path": str(S1_JSON.relative_to(REPO)), "sha256": sha256_file(S1_JSON)},
            "refsep_csv": {"path": str(REFSEP_CSV.relative_to(REPO)), "sha256": sha256_file(REFSEP_CSV)},
        },
        "s1_variant_used": KILL_VARIANT,
        "s1_feature_set_used": KILL_FEATURE,
        "n_s1_receptors": len(s1_receptors),
        "s1_receptors": s1_receptors,
        "missing_from_refsep": missing_refsep,
        "per_backbone_regression": regressions,
        "pooled_regression": {
            "n_points": int(len(sub)),
            "slope_auroc_per_A": ps,
            "intercept": pint,
            "r_squared": pr2,
            "spearman_rho": p_rho,
            "bootstrap": pooled_boot,
            "bimodality": pooled_bim,
        },
        "applicability_thresholds": thresholds,
        "agtr1_counterexample": agtr1,
        "fold_integrity_check_2_test": fi_result,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, default=str))
    tbl.to_csv(OUT_CSV, index=False)

    # Print summary
    print("=" * 72)
    print("G2 — Reference separation vs per-receptor AUROC")
    print("=" * 72)
    print(f"\nS1 15-set: {s1_receptors}")
    if missing_refsep:
        print(f"  MISSING from refsep table: {missing_refsep}")
    print(f"\nPer-backbone regression (AUROC ~ pocket_ca_sep_A, n=15):")
    print(f"{'backbone':<10} {'slope':>8} {'slope_ci_95':>26} {'rho':>7} {'r2':>7} {'bimodal':>8}")
    for bb in BACKBONES:
        r = regressions[bb]
        ci = r["bootstrap"]["slope_ci_95"]
        bim = r["bimodality"]
        print(f"{bb:<10} {r['slope_auroc_per_A']:>8.3f}   [{ci[0]:>7.3f}, {ci[1]:>7.3f}]   {r['spearman_rho']:>6.3f}  {r['r_squared']:>6.3f}   {bim.get('frac_bimodal', float('nan')):>6.3f}")
    print(f"\nPooled: slope={ps:.3f} [{pooled_boot['slope_ci_95'][0]:.3f}, {pooled_boot['slope_ci_95'][1]:.3f}], rho={p_rho:.3f}, r2={pr2:.3f}")
    print(f"\nApplicability-domain thresholds (median AUROC ≥ 0.85 AND no inversions):")
    for t in thresholds:
        if t["threshold_pocket_ca_A"] is not None:
            print(f"  {t['backbone']:<10} τ = {t['threshold_pocket_ca_A']:.2f} Å  (frac reliable above = {t['frac_reliable_above']:.2f})")
        else:
            print(f"  {t['backbone']:<10} no clean threshold found")
    print(f"\nAGTR1 counterexample:")
    if agtr1:
        print(f"  pocket_ca_sep = {agtr1['pocket_ca_sep_A']:.2f} Å (rank {agtr1['pocket_ca_rank_in_40']}/40)")
        print(f"  Δ_ref_tilt    = {agtr1['delta_ref_tilt_A']:.2f} Å")
        print(f"  per-backbone AUROC: {agtr1['per_backbone_auroc']}")

    print(f"\nOutputs:")
    print(f"  {OUT_JSON.relative_to(REPO)}")
    print(f"  {OUT_CSV.relative_to(REPO)}")


if __name__ == "__main__":
    main()
