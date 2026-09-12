#!/usr/bin/env python3
"""T9 — overclaimed framings.

  T9a P0 correlation power at n=35 (Fisher z-transform analytic power).
      Also rerun the correlation on rows.tier3.v2.csv (post-species-fix)
      to see if ρ shifts from the published 0.129 (which was computed on
      the pre-fix rows.tier3.csv).
  T9b Bound/free ratio robustness — four conventions + a replacement framing.
  T9c Anti-memorization "8 of 8" vs "6 of 8" flip enumeration.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT = OUT_DIR / "t9_overframing.json"

# Two-instrument literals (scripts/analyse_block_c_tier3_headline.py:58-59).
NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932
P5_THRESHOLD = 0.15  # scripts/analyse_block_c_tier1_headline.py

ROWS_TIER3_V2 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
ROWS_TIER3_V1 = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.csv"
ROWS_BLOCKB = REPO / "experiments/019_block_b_partner_selection/analysis/rows.csv"

V_JSONS = {
    "task6": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task6_p0_correlation.json",
    "task_F_v5": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_F_v5_clean_bound_stripped.json",
    "task_A_v3": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_A_v3_composition_check.json",
    "task_A_v2": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/task_A_v2_agonist_vs_decoy_apo_same_complex.json",
    "stage3b_v2": REPO / "experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3b_v2_same_complex_split.json",
}

_PATH_RE_TIER3 = re.compile(r"/([a-z0-9_]+)/([a-z_]+)/([a-z]+)/([a-z0-9]+)/seed_(\d+)/")
_PATH_RE_BLOCKB = re.compile(
    r"019_block_b_partner_selection_([a-z0-9]+)_([a-z_]+)_(boltz|chai|of3|protenix)"
)

BACKBONES = ("boltz", "chai", "of3", "protenix")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def is_active(row) -> bool:
    oh = _f(row.get("d_npxxy_y558_y753_oh"))
    tilt = _f(row.get("d_gpcrdb_tm6_tilt_246_637_ca"))
    if math.isnan(oh) or math.isnan(tilt):
        return False
    return (oh < NPXXY_OH_LT) and (tilt > TM6_TILT_GT)


def load_tier3(csv_path: Path) -> dict:
    tree = {}
    with csv_path.open() as f:
        for r in csv.DictReader(f):
            pp = r.get("input_path", "")
            m = _PATH_RE_TIER3.search(pp)
            if not m:
                continue
            rec = m.group(1).upper(); role = m.group(2); arm = m.group(3)
            bb = m.group(4); seed = int(m.group(5))
            r["is_active"] = is_active(r)
            tree.setdefault((rec, role, arm, bb), {}).setdefault(seed, []).append(r)
    return tree


def load_blockb(csv_path: Path) -> dict:
    tree = {}
    with csv_path.open() as f:
        for r in csv.DictReader(f):
            pp = r.get("input_path", "")
            m = _PATH_RE_BLOCKB.search(pp)
            if not m:
                continue
            rec = m.group(1).upper(); arm = m.group(2); bb = m.group(3)
            seed = r.get("seed_used", "") or ""
            r["is_active"] = is_active(r)
            tree.setdefault((rec, arm, bb), {}).setdefault(seed, []).append(r)
    return tree


def cell_frac(seeds_dict) -> float:
    n_a = n = 0
    for _s, rs in seeds_dict.items():
        for r in rs:
            n += 1
            if r["is_active"] is True:
                n_a += 1
    return (n_a / n) if n else float("nan")


def spearman(xs, ys) -> float:
    if len(xs) != len(ys) or not xs:
        return float("nan")
    def ranks(a):
        s = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a); i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and a[s[j + 1]] == a[s[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r
    rx = ranks(xs); ry = ranks(ys)
    n = len(xs)
    mx = sum(rx) / n; my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")


def compute_p0_rho(rows_path: Path) -> dict:
    """Replicate _task6_p0_correlation.py point statistic on the given rows csv."""
    print(f"  loading tier3 from {rows_path.name}...")
    tier3 = load_tier3(rows_path)
    print(f"  loading blockb from {ROWS_BLOCKB.name}...")
    blockb = load_blockb(ROWS_BLOCKB)

    # Per receptor: aggregate across backbones.
    tier3_recs = {k[0] for k in tier3.keys()}
    blockb_recs = {k[0] for k in blockb.keys()}
    common = sorted(tier3_recs & blockb_recs)

    x_family, y_lig_signed, y_lig_abs = [], [], []
    used = []
    for rec in common:
        bb_family, bb_lig = [], []
        for bb in BACKBONES:
            cog = blockb.get((rec, "cognate", bb), {})
            apo = blockb.get((rec, "apo", bb), {})
            if cog and apo:
                fc, fa = cell_frac(cog), cell_frac(apo)
                if not (math.isnan(fc) or math.isnan(fa)):
                    bb_family.append(fc - fa)
            ag = tier3.get((rec, "full_agonist", "apo", bb), {})
            dec = tier3.get((rec, "decoy_lig", "apo", bb), {})
            if ag and dec:
                fag, fdec = cell_frac(ag), cell_frac(dec)
                if not (math.isnan(fag) or math.isnan(fdec)):
                    bb_lig.append(fag - fdec)
        if bb_family and bb_lig:
            x_family.append(sum(bb_family) / len(bb_family))
            y_lig_signed.append(sum(bb_lig) / len(bb_lig))
            y_lig_abs.append(abs(sum(bb_lig) / len(bb_lig)))
            used.append(rec)
    rho_signed = spearman(x_family, y_lig_signed)
    rho_abs = spearman(x_family, y_lig_abs)
    return {
        "n_receptors_used": len(used),
        "receptors_used": used,
        "spearman_rho_signed_ligand": rho_signed,
        "spearman_rho_abs_ligand": rho_abs,
    }


def power_at_rho(rho_true: float, n: int, alpha: float = 0.05) -> float:
    """Two-sided Fisher z-transform power for Pearson correlation.
    For Spearman n is large enough that Pearson approximation is standard."""
    if n <= 3:
        return float("nan")
    z_r = math.atanh(rho_true)
    se = 1 / math.sqrt(n - 3)
    # Under H1: z ~ N(z_r, se); reject if |z| > z_{1-α/2} * se * sqrt(n-3)
    z_alpha = 1.959963984540054  # two-sided 95%
    # Rejection region on z-scale (test statistic z / se ~ N(0,1) under H0)
    crit_upper = z_alpha
    crit_lower = -z_alpha
    # Under H1 z / se ~ N(z_r * sqrt(n-3), 1)
    ncp = z_r * math.sqrt(n - 3)
    # Power = P(|Z| > 1.96) where Z ~ N(ncp, 1)
    def phi(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    p_upper = 1 - phi(crit_upper - ncp)
    p_lower = phi(crit_lower - ncp)
    return p_upper + p_lower


def t9a(report: dict) -> None:
    print("[T9a] P0 correlation on rows.tier3.v2 (post-fix)...")
    v2 = compute_p0_rho(ROWS_TIER3_V2)
    print(f"  v2 rho_abs   = {v2['spearman_rho_abs_ligand']:.4f}  (n={v2['n_receptors_used']})")

    published = json.loads(V_JSONS["task6"].read_text())
    published_rho = published["point_spearman_rho"]
    published_n = published["n_receptors_common_used"]
    published_ci = published["fisher_z_95ci_spearman"]

    p03 = power_at_rho(0.3, 35)
    p05 = power_at_rho(0.5, 35)
    p03_v2 = power_at_rho(0.3, v2["n_receptors_used"])
    p05_v2 = power_at_rho(0.5, v2["n_receptors_used"])

    recommendation = ""
    if p03 < 0.8:
        recommendation = (
            f"Power = {p03*100:.1f}% at ρ=0.3 (n={published_n}), below 80% threshold. "
            "Recommend the manuscript replace 'essentially independent tests' with "
            "'not resolved at this n'. The observed ρ=0.129 is compatible with any true "
            "ρ in the CI [-0.213, +0.443] — including moderate positive correlation."
        )
    else:
        recommendation = (
            f"Power {p03*100:.1f}% at ρ=0.3 (n={published_n}) meets 80% threshold. "
            "Current 'essentially independent tests' framing may hold."
        )

    report["t9a_p0_power_analysis"] = {
        "published": {
            "spearman_rho": published_rho,
            "n": published_n,
            "fisher_z_95ci_spearman": published_ci,
            "input_file": "rows.tier3.csv (pre-species-fix)",
        },
        "reaudit_on_v2": {
            "spearman_rho_abs_ligand": v2["spearman_rho_abs_ligand"],
            "spearman_rho_signed_ligand": v2["spearman_rho_signed_ligand"],
            "n": v2["n_receptors_used"],
            "receptors_used": v2["receptors_used"],
            "input_file": "rows.tier3.v2.csv (post-species-fix)",
            "delta_rho_vs_published": v2["spearman_rho_abs_ligand"] - published_rho,
        },
        "power_analysis": {
            "method": "Fisher z-transform, two-sided α=0.05, normal approximation",
            "power_at_rho_0.3_n35": p03,
            "power_at_rho_0.5_n35": p05,
            "power_at_rho_0.3_n_v2": p03_v2,
            "power_at_rho_0.5_n_v2": p05_v2,
        },
        "recommendation": recommendation,
    }
    print(f"  power at ρ=0.3, n=35: {p03*100:.1f}%")
    print(f"  power at ρ=0.5, n=35: {p05*100:.1f}%")


def geomean(xs):
    xs2 = [x for x in xs if x > 0]
    if not xs2:
        return float("nan")
    return math.exp(sum(math.log(x) for x in xs2) / len(xs2))


def t9b(report: dict) -> None:
    print("[T9b] Bound/free ratio robustness...")
    v5 = json.loads(V_JSONS["task_F_v5"].read_text())
    # per_receptor_apo_summary gives coh_active_fraction per receptor.
    per_rec = v5.get("per_receptor_apo_summary", {})
    stats = v5["stratum_stats"]
    bound = stats["v5_clean_bound_24"]["receptors"]
    free = stats["refined_v3_free_5"]["receptors"]

    def rec_frac(rec):
        entry = per_rec.get(rec, {})
        return entry.get("coh_active_fraction", float("nan")) if isinstance(entry, dict) else float("nan")

    bound_fracs = [rec_frac(r) for r in bound]
    free_fracs = [rec_frac(r) for r in free]

    bound_fracs_clean = [x for x in bound_fracs if not (x is None or (isinstance(x, float) and math.isnan(x)))]
    free_fracs_clean = [x for x in free_fracs if not (x is None or (isinstance(x, float) and math.isnan(x)))]

    bound_zero_or_near = sum(1 for x in bound_fracs_clean if x < 0.01)
    free_zero_or_near = sum(1 for x in free_fracs_clean if x < 0.01)

    ratios = {}
    # mean of means
    b_mean = sum(bound_fracs_clean) / len(bound_fracs_clean) if bound_fracs_clean else float("nan")
    f_mean = sum(free_fracs_clean) / len(free_fracs_clean) if free_fracs_clean else float("nan")
    ratios["mean_of_means"] = f_mean / b_mean if b_mean > 0 else float("inf")

    # median of medians
    def median(xs):
        s = sorted(xs); n = len(s)
        if not n:
            return float("nan")
        return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2
    b_med = median(bound_fracs_clean)
    f_med = median(free_fracs_clean)
    ratios["median_of_medians"] = f_med / b_med if b_med > 0 else float("inf")

    # geometric mean (skips zeros)
    b_geo = geomean(bound_fracs_clean)
    f_geo = geomean(free_fracs_clean)
    ratios["geometric_mean"] = f_geo / b_geo if b_geo > 0 else float("inf")

    # skip-zero-denominator: exclude bound receptors with < 0.01 from denominator
    bound_nonzero = [x for x in bound_fracs_clean if x >= 0.01]
    b_mean_nz = sum(bound_nonzero) / len(bound_nonzero) if bound_nonzero else float("nan")
    ratios["skip_zero_denominator_bound"] = f_mean / b_mean_nz if b_mean_nz > 0 else float("inf")

    # Cluster-bootstrap CI for the signed difference (free - bound).
    rng = np.random.default_rng(20260907)
    diffs = []
    b_arr = np.array(bound_fracs_clean); f_arr = np.array(free_fracs_clean)
    for _ in range(5000):
        b_boot = b_arr[rng.integers(0, len(b_arr), len(b_arr))]
        f_boot = f_arr[rng.integers(0, len(f_arr), len(f_arr))]
        diffs.append(f_boot.mean() - b_boot.mean())
    diffs = np.array(diffs)
    ci = tuple(np.percentile(diffs, [2.5, 97.5]))

    report["t9b_bound_free_ratio_robustness"] = {
        "bound_n": len(bound_fracs_clean),
        "free_n": len(free_fracs_clean),
        "bound_receptors_near_zero_lt_1pct": bound_zero_or_near,
        "free_receptors_near_zero_lt_1pct": free_zero_or_near,
        "bound_stratum_stats": {
            "mean": b_mean, "median": b_med, "geo_mean": b_geo,
            "mean_excl_near_zero": b_mean_nz, "n_near_zero_excluded": len(bound_fracs_clean) - len(bound_nonzero),
        },
        "free_stratum_stats": {
            "mean": f_mean, "median": f_med, "geo_mean": f_geo,
        },
        "ratios_free_over_bound_under_four_conventions": ratios,
        "signed_difference_free_minus_bound": {
            "point_estimate": float(f_mean - b_mean),
            "cluster_bootstrap_ci_95": [float(ci[0]), float(ci[1])],
            "note": "5000 bootstrap iterations, receptors resampled with replacement per stratum, "
                    "seed=20260907 (different from campaign seed=20260906 to avoid seed collision).",
        },
        "recommended_framing": (
            "Report two fractions plus a signed difference with CI, rather than a ratio. "
            f"Bound stratum n={len(bound_fracs_clean)}, mean {b_mean*100:.1f}%. "
            f"Free stratum n={len(free_fracs_clean)}, mean {f_mean*100:.1f}%. "
            f"Signed difference free − bound = +{(f_mean - b_mean)*100:.1f}% "
            f"(cluster-bootstrap 95% CI [{ci[0]*100:.1f}, {ci[1]*100:.1f}]). "
            "The ratio is arithmetically unstable when bound stratum has near-zero "
            f"denominators ({bound_zero_or_near} of {len(bound_fracs_clean)} receptors < 1%)."
        ),
    }
    print(f"  bound mean={b_mean:.3f} median={b_med:.3f}; free mean={f_mean:.3f} median={f_med:.3f}")
    print(f"  ratios: mean-of-means={ratios['mean_of_means']:.2f}x  "
          f"median-of-medians={ratios['median_of_medians']:.2f}x  "
          f"geometric={ratios['geometric_mean']:.2f}x  "
          f"skip-near-zero-den={ratios['skip_zero_denominator_bound']:.2f}x")
    print(f"  signed diff free-bound = +{(f_mean - b_mean)*100:.1f}% CI [{ci[0]*100:.1f}, {ci[1]*100:.1f}]")


def t9c(report: dict) -> None:
    print("[T9c] Anti-memorization 8/8 vs 6/8 flip enumeration...")
    v2 = json.loads(V_JSONS["task_A_v2"].read_text())
    v3 = json.loads(V_JSONS["task_A_v3"].read_text())

    # v2 test: 8 signed_ci_must_generalise (mustgen stratum CI clears zero)
    # v2 documents this as "n_signed_ci_must_generalise_over_8_tests": 8
    v2_result = v2["hypothesis_result"]

    # v3 test: (mustgen - recallable) point estimate direction — different comparison.
    # v3 reports "LARGER on MUST_GENERALISE for 6 of 8 tests (CA: 4/4; SC: 2/4)"
    hf = v3["honest_framing"]
    v3_ca = hf["summary_verdicts_per_backbone_ca_axis"]
    v3_sc = hf["summary_verdicts_per_backbone_sc_axis"]

    # Enumerate the 8 cells.
    cells = []
    for bb in ("boltz", "chai", "of3", "protenix"):
        for axis in ("ca", "sc"):
            axis_key = "pocket_ca_rmsd_active" if axis == "ca" else "pocket_sidechain_rmsd_active"
            v2_cell = v2.get("per_backbone", {}).get(bb, {}).get(axis_key, {})
            v3_cell = hf.get("magnitude_difference_bootstrap", {}).get(bb, {}).get(axis_key, {})
            same_ci_hit = v2_cell.get("same_minus_diff_of_deltas", {}).get("signed_nonzero", False)
            v2_mustgen_signed = v2_cell.get("diff_stratum_mean_delta_A", {}).get("signed_nonzero", False)
            v2_recall_signed = v2_cell.get("same_stratum_mean_delta_A", {}).get("signed_nonzero", False)
            v3_verdict = (v3_ca if axis == "ca" else v3_sc).get(bb, "unknown")
            cells.append({
                "backbone": bb,
                "axis": axis,
                "axis_key": axis_key,
                "v2_recallable_signed_nonzero": v2_recall_signed,
                "v2_mustgen_signed_nonzero": v2_mustgen_signed,
                "v2_recall_delta_est": v2_cell.get("same_stratum_mean_delta_A", {}).get("est"),
                "v2_mustgen_delta_est": v2_cell.get("diff_stratum_mean_delta_A", {}).get("est"),
                "v3_mustgen_minus_recallable_est": v3_cell.get("mustgen_minus_recallable_signed_delta_A", {}).get("est"),
                "v3_mustgen_minus_recallable_ci": [
                    v3_cell.get("mustgen_minus_recallable_signed_delta_A", {}).get("ci_lo"),
                    v3_cell.get("mustgen_minus_recallable_signed_delta_A", {}).get("ci_hi"),
                ],
                "v3_summary_verdict": v3_verdict,
                "v3_direction_favours_must_gen": (
                    v3_verdict.startswith("MUST_GEN_LARGER")
                ),
            })

    v3_must_gen_count = sum(1 for c in cells if c["v3_direction_favours_must_gen"])
    v3_recallable_count = sum(1 for c in cells if not c["v3_direction_favours_must_gen"])
    flipped = [c for c in cells if not c["v3_direction_favours_must_gen"]]

    report["t9c_antimemorization_flip_enumeration"] = {
        "v2_mustgen_signed_nonzero_count": v2_result.get("n_signed_ci_must_generalise_over_8_tests"),
        "v2_recallable_signed_nonzero_count": v2_result.get("n_signed_ci_recallable_over_8_tests"),
        "v2_meaning": (
            "v2's '8 of 8' counts (backbone × axis) cells where the MUST-GENERALISE "
            "stratum's own CI clears zero (i.e. anti-memorization signal is present in "
            "must-gen). Does not directly compare must-gen vs recallable magnitudes."
        ),
        "v3_must_gen_larger_count": v3_must_gen_count,
        "v3_recallable_larger_count": v3_recallable_count,
        "v3_meaning": (
            "v3's '6 of 8' counts (backbone × axis) cells where the POINT estimate of "
            "(must_gen − recallable) is negative (i.e. must-gen larger anti-mem effect). "
            "All 8 CIs straddle zero. Different comparison than v2."
        ),
        "cells_that_flipped_to_recallable_larger": flipped,
        "cells": cells,
        "reconciliation": (
            "v2 and v3 answer different questions. v2 asks 'is the anti-mem signal "
            "signed non-zero in the must-gen stratum?' — YES on 8/8 cells. v3 asks "
            "'is the anti-mem effect LARGER in must-gen than in recallable?' — 6/8 cells "
            "point in that direction, 2 flip to recallable-larger (both on SC axis: "
            + ", ".join(c["backbone"] for c in flipped) + "). All 8 v3 CIs straddle zero, "
            "so v3's direction claim is 'suggestive, not established at n=13/15'."
        ),
    }
    print(f"  v2 must_gen signed n/8: {v2_result.get('n_signed_ci_must_generalise_over_8_tests')}")
    print(f"  v3 direction favours must_gen: {v3_must_gen_count}/8; recallable: {v3_recallable_count}/8")
    for c in flipped:
        print(f"    FLIPPED: {c['backbone']} × {c['axis']} → {c['v3_summary_verdict']}")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "task": "T9_overframing",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "_provenance": {
            "inputs": {
                str(p.relative_to(REPO)): sha(p) for p in [
                    ROWS_TIER3_V1, ROWS_TIER3_V2, ROWS_BLOCKB, *V_JSONS.values(),
                ] if p.exists()
            },
            "script": {"path": str(Path(__file__).relative_to(REPO)), "sha256": sha(Path(__file__))},
            "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                       capture_output=True, text=True).stdout.strip(),
            "rng_seed": 20260907,
        },
    }
    t9a(report)
    t9b(report)
    t9c(report)

    report["recommendations"] = [
        report["t9a_p0_power_analysis"]["recommendation"],
        report["t9b_bound_free_ratio_robustness"]["recommended_framing"],
        report["t9c_antimemorization_flip_enumeration"]["reconciliation"],
    ]

    OUT.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[T9] wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
