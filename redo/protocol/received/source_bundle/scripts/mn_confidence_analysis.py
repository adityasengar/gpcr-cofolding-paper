"""Compute per-backbone (m,n) confidence + sufficiency verdict from rescored data.

Runs LOCALLY (post-rescore rsync). Reads:
- experiments/<slug>/rows.csv for the 10 (m,n) sub-experiments across 2 GPCRs:
    * AA2AR:  013_..._5_1, 014_..._1_5, 015_..._5_5, 016_..._20_1, 017_..._1_20
    * ADRB2:  019_..._5_1, 020_..._1_5, 021_..._5_5, 022_..._20_1, 023_..._1_20
  Optional 3rd/4th GPCR follow-up folders (024+) are picked up if present.

Emits:
- stdout: human-readable verdict table
- --json <path>: machine-readable JSON with per-backbone assessment + recommended follow-ups
                 (for dispatch_mn_followup.py to consume in the analyse-assess-augment loop)

Sufficiency framework (per plan §Phase C):

    SUFFICIENT (backbone):
        1. Winner axis matches across ALL GPCRs with data
        2. Effect-size ratio ≥ 2.0 on every GPCR
        3. ≥5 valid predictions per target (m,n) cell
        4. ≥80% pass-rate on confidence_flag != "low"

    INSUFFICIENT: fails any of the above; specific weakness recorded.
    UNSTABLE: winner axis flips between GPCRs (stronger signal for 3rd-GPCR follow-up).

Winner-axis calculation:
    ratio_5  = std(d_tm6 at 1×5)  / std(d_tm6 at 5×1)
    ratio_20 = std(d_tm6 at 1×20) / std(d_tm6 at 20×1)  (if both cells exist)

    ratio > 1 → samples-winner (samples-per-seed drives diversity)
    ratio < 1 → seeds-winner
    0.8 ≤ ratio ≤ 1.25 → balanced (recommend square (K,K) rule)

Usage:
    python3 scripts/mn_confidence_analysis.py \\
        --experiments-root /Users/SENGAAD1/Documents/claude/paper_af3/experiments \\
        --json /tmp/mn_verdict.json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

BACKBONES = ("boltz", "of3", "protenix", "chai")

# (slug_prefix, receptor, cell_m, cell_n)
STUDY_LAYOUT = [
    ("013_aa2ar_gs_neca_mn_5_1",   "AA2AR",  5,  1),
    ("014_aa2ar_gs_neca_mn_1_5",   "AA2AR",  1,  5),
    ("015_aa2ar_gs_neca_mn_5_5",   "AA2AR",  5,  5),
    ("016_aa2ar_gs_neca_mn_20_1",  "AA2AR",  20, 1),
    ("017_aa2ar_gs_neca_mn_1_20",  "AA2AR",  1,  20),
    ("019_adrb2_gs_agonist_mn_5_1",   "ADRB2",  5,  1),
    ("020_adrb2_gs_agonist_mn_1_5",   "ADRB2",  1,  5),
    ("021_adrb2_gs_agonist_mn_5_5",   "ADRB2",  5,  5),
    ("022_adrb2_gs_agonist_mn_20_1",  "ADRB2",  20, 1),
    ("023_adrb2_gs_agonist_mn_1_20",  "ADRB2",  1,  20),
]

# Sufficiency thresholds
MIN_EFFECT_SIZE = 2.0        # ratio for "clear" winner (max of ratio, 1/ratio)
MIN_CELL_N = 5               # minimum valid predictions per cell
MIN_PASS_RATE = 0.80         # confidence_flag pass-rate
BALANCED_LO, BALANCED_HI = 0.8, 1.25


def _to_float(x: str) -> float:
    try:
        v = float(x)
        return v if not math.isnan(v) else math.nan
    except (ValueError, TypeError):
        return math.nan


@dataclass
class CellStats:
    slug: str
    receptor: str
    m: int
    n: int
    backbone: str
    n_total: int = 0
    n_valid: int = 0
    d_tm6_mean: float = math.nan
    d_tm6_std: float = math.nan
    d_tm6_min: float = math.nan
    d_tm6_max: float = math.nan
    n_above_midpoint: int = 0
    n_below_midpoint: int = 0
    plddt_mean_med: float = math.nan
    conf_low_frac: float = math.nan
    conf_high_frac: float = math.nan


@dataclass
class BackboneReceptorVerdict:
    receptor: str
    backbone: str
    ratio_5: float = math.nan   # (1,5)/(5,1) std ratio
    ratio_20: float = math.nan  # (1,20)/(20,1) std ratio
    winner_axis: str = "unknown"    # "samples" / "seeds" / "balanced" / "unknown"
    effect_size: float = math.nan   # max(ratio, 1/ratio) at whichever N has data
    cells_covered: list = field(default_factory=list)
    cells_missing: list = field(default_factory=list)


@dataclass
class BackboneVerdict:
    backbone: str
    per_receptor: list = field(default_factory=list)
    verdict: str = "UNCERTAIN"      # SUFFICIENT / INSUFFICIENT / UNSTABLE / UNCERTAIN
    reason: str = ""
    followup_recommendation: dict = field(default_factory=dict)
    recommended_rule: str = ""       # e.g., "seeds=1, samples_per_seed=5"


def load_cell(experiments_root: Path, slug: str, receptor: str, m: int, n: int) -> list[CellStats]:
    """Read rows.csv for the slug; return one CellStats per backbone present."""
    rows_csv = experiments_root / slug / "rows.csv"
    if not rows_csv.exists():
        return []
    rows = list(csv.DictReader(rows_csv.open()))
    stats: list[CellStats] = []
    by_bb: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        bb = r.get("backbone", "").strip().lower()
        if not bb:
            # Derive from input_path (contains /boltz/, /of3/, etc.)
            ip = (r.get("input_path") or r.get("prediction_path") or "").lower()
            for cand in BACKBONES:
                if f"/{cand}/" in ip or f"_{cand}_" in ip:
                    bb = cand
                    break
        if bb in BACKBONES:
            by_bb[bb].append(r)

    for bb in BACKBONES:
        bb_rows = by_bb.get(bb, [])
        s = CellStats(slug=slug, receptor=receptor, m=m, n=n, backbone=bb,
                      n_total=len(bb_rows))
        if not bb_rows:
            stats.append(s)
            continue

        d_tm6_vals = []
        mid_vals = []
        plddt_vals = []
        conf_flags = []
        for r in bb_rows:
            d_tm6 = _to_float(r.get("d_tm6_r350_r630_ca", ""))
            mid = _to_float(r.get("receptor_midpoint", ""))
            plddt = _to_float(r.get("plddt_mean", ""))
            conf = (r.get("confidence_flag", "") or "").strip().lower()

            conf_flags.append(conf)
            if not math.isnan(plddt):
                plddt_vals.append(plddt)

            # "Valid" for std computation: d_tm6 numeric AND midpoint numeric
            if not math.isnan(d_tm6) and not math.isnan(mid):
                d_tm6_vals.append(d_tm6)
                mid_vals.append((d_tm6, mid))

        s.n_valid = len(d_tm6_vals)
        if s.n_valid >= 2:
            s.d_tm6_std = statistics.stdev(d_tm6_vals)
        elif s.n_valid == 1:
            s.d_tm6_std = 0.0
        if d_tm6_vals:
            s.d_tm6_mean = statistics.mean(d_tm6_vals)
            s.d_tm6_min = min(d_tm6_vals)
            s.d_tm6_max = max(d_tm6_vals)
        for d, mid in mid_vals:
            if d > mid:
                s.n_above_midpoint += 1
            else:
                s.n_below_midpoint += 1
        if plddt_vals:
            s.plddt_mean_med = statistics.median(plddt_vals)
        if conf_flags:
            n_low = sum(1 for c in conf_flags if c == "low")
            n_high = sum(1 for c in conf_flags if c == "high")
            s.conf_low_frac = n_low / len(conf_flags)
            s.conf_high_frac = n_high / len(conf_flags)
        stats.append(s)
    return stats


def collect_all_cells(experiments_root: Path) -> list[CellStats]:
    """Iterate the full study layout, plus opportunistic 024+ follow-up slugs."""
    all_stats: list[CellStats] = []
    for slug, receptor, m, n in STUDY_LAYOUT:
        all_stats.extend(load_cell(experiments_root, slug, receptor, m, n))

    # Opportunistic: pick up follow-up slugs matching pattern "024_" onwards
    for path in sorted(experiments_root.glob("[0-9][0-9][0-9]_*")):
        name = path.name
        if name.split("_")[0] in {s.split("_")[0] for s, _, _, _ in STUDY_LAYOUT}:
            continue  # already covered
        # parse "NNN_<something>_mn_M_N" — extract receptor + m + n
        parts = name.split("_")
        try:
            mn_idx = parts.index("mn")
            m, n = int(parts[mn_idx + 1]), int(parts[mn_idx + 2])
        except (ValueError, IndexError):
            continue
        # Infer receptor from slug (looks for a known receptor slug substring)
        receptor_guess = "UNKNOWN"
        for cand in ("AA2AR", "ADRB2", "DRD2", "5HT2C", "5HT1B"):
            if cand.lower() in name.lower():
                receptor_guess = cand
                break
        all_stats.extend(load_cell(experiments_root, name, receptor_guess, m, n))

    return all_stats


def classify_axis(ratio: float) -> str:
    if math.isnan(ratio) or ratio <= 0:
        return "unknown"
    if BALANCED_LO <= ratio <= BALANCED_HI:
        return "balanced"
    return "samples" if ratio > 1 else "seeds"


def compute_backbone_receptor(cells: list[CellStats], receptor: str, backbone: str) -> BackboneReceptorVerdict:
    """Compute winner axis + effect size for one (receptor, backbone) pair."""
    v = BackboneReceptorVerdict(receptor=receptor, backbone=backbone)
    by_mn: dict[tuple[int, int], CellStats] = {}
    for c in cells:
        if c.receptor != receptor or c.backbone != backbone:
            continue
        by_mn[(c.m, c.n)] = c

    # Track cell coverage
    target_cells = [(5, 1), (1, 5), (5, 5), (20, 1), (1, 20)]
    for tc in target_cells:
        if tc in by_mn and by_mn[tc].n_valid >= MIN_CELL_N:
            v.cells_covered.append(list(tc))
        else:
            v.cells_missing.append(list(tc))

    # Ratio at N=5
    c_5_1 = by_mn.get((5, 1))
    c_1_5 = by_mn.get((1, 5))
    if c_5_1 and c_1_5 and c_5_1.n_valid >= MIN_CELL_N and c_1_5.n_valid >= MIN_CELL_N:
        if c_5_1.d_tm6_std > 0:
            v.ratio_5 = c_1_5.d_tm6_std / c_5_1.d_tm6_std

    # Ratio at N=20
    c_20_1 = by_mn.get((20, 1))
    c_1_20 = by_mn.get((1, 20))
    if c_20_1 and c_1_20 and c_20_1.n_valid >= MIN_CELL_N and c_1_20.n_valid >= MIN_CELL_N:
        if c_20_1.d_tm6_std > 0:
            v.ratio_20 = c_1_20.d_tm6_std / c_20_1.d_tm6_std

    # Pick the ratio with more data support
    ratios = [r for r in (v.ratio_5, v.ratio_20) if not math.isnan(r)]
    if ratios:
        primary_ratio = max(ratios, key=lambda x: abs(math.log(x)) if x > 0 else -1)
        v.winner_axis = classify_axis(primary_ratio)
        v.effect_size = max(primary_ratio, 1.0 / primary_ratio)

    return v


def assess_backbone(per_receptor: list[BackboneReceptorVerdict], backbone: str) -> BackboneVerdict:
    """Aggregate cross-receptor verdicts into a SUFFICIENT/INSUFFICIENT/UNSTABLE call."""
    bv = BackboneVerdict(backbone=backbone, per_receptor=per_receptor)

    with_data = [r for r in per_receptor if r.winner_axis != "unknown"]
    if len(with_data) < 2:
        bv.verdict = "UNCERTAIN"
        bv.reason = (f"only {len(with_data)}/{len(per_receptor)} GPCR(s) have "
                     "the (5,1)+(1,5) or (20,1)+(1,20) cells populated. "
                     "Need ≥2 GPCRs of data for cross-receptor consistency.")
        bv.followup_recommendation = {
            "type": "fill_missing_cells",
            "backbone": backbone,
            "receptors": [r.receptor for r in per_receptor if not r.cells_covered],
        }
        return bv

    axes = {r.winner_axis for r in with_data}
    if "unknown" in axes:
        axes.discard("unknown")
    min_effect = min(r.effect_size for r in with_data)

    if len(axes) > 1:
        bv.verdict = "UNSTABLE"
        bv.reason = (f"winner axis differs between GPCRs: "
                     + "; ".join(f"{r.receptor}={r.winner_axis} (×{r.effect_size:.2f})"
                                 for r in with_data)
                     + ". A 3rd GPCR is needed to break the tie.")
        bv.followup_recommendation = {
            "type": "add_third_gpcr",
            "backbone": backbone,
            "candidate_gpcrs": ["DRD2", "5HT2C"],
            "reason": "resolve UNSTABLE cross-GPCR flip",
        }
        return bv

    if min_effect < MIN_EFFECT_SIZE:
        bv.verdict = "INSUFFICIENT"
        bv.reason = (f"winner axis={next(iter(axes))} consistent, but "
                     f"effect size min={min_effect:.2f}× < {MIN_EFFECT_SIZE:.1f}× "
                     "threshold on at least one GPCR. N=5 noise may not be beaten.")
        bv.followup_recommendation = {
            "type": "increase_N_via_10_10",
            "backbone": backbone,
            "reason": f"boost effect-size signal from {min_effect:.2f}×",
        }
        return bv

    # All checks pass so far — still need cell-coverage + confidence checks
    all_covered = all(len(r.cells_missing) == 0 for r in with_data)
    if not all_covered:
        missing = [(r.receptor, r.cells_missing) for r in with_data if r.cells_missing]
        bv.verdict = "INSUFFICIENT"
        bv.reason = f"missing cells: " + "; ".join(f"{rec}:{cs}" for rec, cs in missing)
        bv.followup_recommendation = {
            "type": "fill_missing_cells",
            "backbone": backbone,
            "missing": [{"receptor": rec, "cells": cs} for rec, cs in missing],
        }
        return bv

    # SUFFICIENT
    winner = next(iter(axes))
    bv.verdict = "SUFFICIENT"
    bv.reason = (f"winner={winner} consistent across {len(with_data)} GPCRs, "
                 f"min effect size ×{min_effect:.2f}, all cells covered.")
    # Recommend rule based on winner
    if winner == "samples":
        bv.recommended_rule = "seeds=1, samples_per_seed=5"
    elif winner == "seeds":
        bv.recommended_rule = "seeds=5, samples_per_seed=1"
    else:  # balanced
        bv.recommended_rule = "seeds=5, samples_per_seed=5 (balanced)"
    return bv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="mn_confidence_analysis")
    p.add_argument("--experiments-root", type=Path,
                   default=Path("/Users/SENGAAD1/Documents/claude/paper_af3/experiments/mn_consensus"))
    p.add_argument("--json", type=Path, default=None,
                   help="write machine-readable verdict + follow-up to this path")
    args = p.parse_args(argv)

    all_cells = collect_all_cells(args.experiments_root)
    n_cells_with_data = sum(1 for c in all_cells if c.n_valid > 0)
    print(f"loaded {len(all_cells)} (slug×backbone) cells; "
          f"{n_cells_with_data} with ≥1 valid prediction")
    print()

    receptors = sorted({c.receptor for c in all_cells if c.receptor != "UNKNOWN"})

    # Per-backbone verdicts
    backbone_verdicts: list[BackboneVerdict] = []
    for bb in BACKBONES:
        per_rec = [compute_backbone_receptor(all_cells, rec, bb) for rec in receptors]
        bv = assess_backbone(per_rec, bb)
        backbone_verdicts.append(bv)

    # Human-readable output
    print("Per-cell d_tm6 std (Å) [n_valid]:")
    print(f"{'slug':<40} {'bb':<10} {'m':>3} {'n':>3} {'nval':>4} {'std':>7} {'mean':>7}")
    for c in sorted(all_cells, key=lambda x: (x.receptor, x.slug, x.backbone)):
        if c.n_total == 0:
            continue
        std_str = f"{c.d_tm6_std:.3f}" if not math.isnan(c.d_tm6_std) else "  n/a"
        mean_str = f"{c.d_tm6_mean:.2f}" if not math.isnan(c.d_tm6_mean) else "  n/a"
        print(f"{c.slug[:39]:<40} {c.backbone:<10} {c.m:>3} {c.n:>3} {c.n_valid:>4} "
              f"{std_str:>7} {mean_str:>7}")
    print()

    print("Per-backbone verdict:")
    print(f"{'bb':<10} {'verdict':<14} {'rule':<40} reason")
    for bv in backbone_verdicts:
        print(f"{bv.backbone:<10} {bv.verdict:<14} {bv.recommended_rule:<40} {bv.reason[:80]}")
    print()

    n_sufficient = sum(1 for bv in backbone_verdicts if bv.verdict == "SUFFICIENT")
    print(f"summary: {n_sufficient}/{len(BACKBONES)} backbones SUFFICIENT")
    for bv in backbone_verdicts:
        if bv.verdict != "SUFFICIENT" and bv.followup_recommendation:
            print(f"  {bv.backbone} → {bv.followup_recommendation.get('type', '?')}: "
                  f"{bv.followup_recommendation.get('reason', '')[:80]}")

    if args.json:
        args.json.write_text(json.dumps({
            "cells": [asdict(c) for c in all_cells if c.n_total > 0],
            "backbone_verdicts": [asdict(bv) for bv in backbone_verdicts],
            "n_sufficient": n_sufficient,
            "n_backbones": len(BACKBONES),
            "receptors": receptors,
        }, indent=2, default=str))
        print(f"\nwrote {args.json}")

    return 0 if n_sufficient == len(BACKBONES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
