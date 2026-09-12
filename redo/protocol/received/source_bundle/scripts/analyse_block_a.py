"""Analyse a Block A switch-test rows.csv → findings.md.

Inputs a rescored `experiments/018_block_a_switch_test/rows.csv` (or any
rows.csv with the same 73-column ScorerRow schema) and writes:

1. Per-backbone `N/40` success count (majority-vote and stringent bars).
2. Per-receptor across-backbone verdict.
3. Confidence miscalibration table (high-conf-wrong rate per backbone).
4. AA2AR-specific breakdown to check the anecdote at population scale.

Success predicate per (receptor, backbone) with K replicates per cell:

    partner_rows = rows where receptor=X, backbone=Y, partner_type=g_alpha
    apo_rows     = rows where receptor=X, backbone=Y, partner_type=apo

    active_hitrate(X,Y)   = fraction of partner_rows with d_tm6_r350_r630_ca >  receptor_midpoint
    inactive_hitrate(X,Y) = fraction of apo_rows     with d_tm6_r350_r630_ca <= receptor_midpoint

    success(X, Y)   = active_hitrate ≥ 0.5 AND inactive_hitrate ≥ 0.5
    strong(X, Y)    = active_hitrate ≥ 0.8 AND inactive_hitrate ≥ 0.8

Cells drop replicates with NaN d_tm6 / NaN midpoint / confidence_flag=low.
Cells with fewer than ceil(K/2) valid replicates → NaN, excluded from N/40.

Usage:

    scripts/analyse_block_a.py \\
        --rows experiments/018_block_a_switch_test/rows.csv \\
        --findings-out experiments/018_block_a_switch_test/findings.md
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


BACKBONES = ("boltz", "of3", "protenix", "chai")
HIGH_CONF = 70.0
LOW_CONF = 50.0


def _to_float(x: str) -> float:
    try:
        v = float(x)
        if math.isnan(v):
            return math.nan
        return v
    except (ValueError, TypeError):
        return math.nan


def load_rows(rows_csv: Path) -> list[dict]:
    with rows_csv.open() as f:
        return list(csv.DictReader(f))


def valid_replicate(r: dict) -> bool:
    """Drop rows with NaN d_tm6 / NaN midpoint / confidence_flag=low."""
    if r.get("confidence_flag", "").strip().lower() == "low":
        return False
    d_tm6 = _to_float(r.get("d_tm6_r350_r630_ca", ""))
    midpoint = _to_float(r.get("receptor_midpoint", ""))
    if math.isnan(d_tm6) or math.isnan(midpoint):
        return False
    return True


def compute_cell(rows: list[dict], partner_type: str) -> tuple[int, int, list[float]]:
    """Filter to (partner_type) rows, return (n_active_side, n_valid, d_tm6 values).

    'active side' means d_tm6 > midpoint (call it 'active_hitrate' numerator).
    """
    n_active = 0
    n_valid = 0
    d_tm6_vals: list[float] = []
    for r in rows:
        if r.get("partner_type", "") != partner_type:
            continue
        if not valid_replicate(r):
            continue
        n_valid += 1
        d_tm6 = _to_float(r["d_tm6_r350_r630_ca"])
        midpoint = _to_float(r["receptor_midpoint"])
        d_tm6_vals.append(d_tm6)
        if d_tm6 > midpoint:
            n_active += 1
    return n_active, n_valid, d_tm6_vals


def analyse(rows: list[dict], k_per_cell: int) -> dict:
    """Group by (receptor, backbone), compute per-cell verdicts."""
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        rec = r.get("receptor_slug", "").upper()
        bb = r.get("backbone", "")
        if not rec or not bb:
            continue
        grouped[(rec, bb)].append(r)

    per_cell: dict[tuple[str, str], dict] = {}
    for (rec, bb), cell_rows in grouped.items():
        n_partner_active, n_partner_valid, partner_d = compute_cell(cell_rows, "g_alpha")
        n_apo_active, n_apo_valid, apo_d = compute_cell(cell_rows, "apo")

        min_valid = max(1, math.ceil(k_per_cell / 2))
        if n_partner_valid < min_valid or n_apo_valid < min_valid:
            verdict = "NA"
            success = None
            strong = None
        else:
            active_hitrate = n_partner_active / n_partner_valid
            inactive_hitrate = 1.0 - (n_apo_active / n_apo_valid)
            success = (active_hitrate >= 0.5) and (inactive_hitrate >= 0.5)
            strong = (active_hitrate >= 0.8) and (inactive_hitrate >= 0.8)
            verdict = "strong" if strong else ("success" if success else "fail")

        # Confidence buckets — computed per replicate then rolled up
        n_hc_correct = n_hc_wrong = n_lc_correct = n_lc_wrong = 0
        for r in cell_rows:
            if not valid_replicate(r):
                continue
            plddt = _to_float(r.get("plddt_mean", ""))
            if math.isnan(plddt):
                continue
            d_tm6 = _to_float(r["d_tm6_r350_r630_ca"])
            midpoint = _to_float(r["receptor_midpoint"])
            partner = r.get("partner_type", "")
            expected_side_active = (partner == "g_alpha")
            actual_side_active = (d_tm6 > midpoint)
            is_correct = (expected_side_active == actual_side_active)
            if plddt >= HIGH_CONF:
                if is_correct:
                    n_hc_correct += 1
                else:
                    n_hc_wrong += 1
            elif plddt < LOW_CONF:
                if is_correct:
                    n_lc_correct += 1
                else:
                    n_lc_wrong += 1

        per_cell[(rec, bb)] = {
            "n_partner_active": n_partner_active,
            "n_partner_valid": n_partner_valid,
            "n_apo_active": n_apo_active,
            "n_apo_valid": n_apo_valid,
            "partner_d_mean": statistics.mean(partner_d) if partner_d else math.nan,
            "apo_d_mean": statistics.mean(apo_d) if apo_d else math.nan,
            "verdict": verdict,
            "success": success,
            "strong": strong,
            "n_hc_correct": n_hc_correct,
            "n_hc_wrong": n_hc_wrong,
            "n_lc_correct": n_lc_correct,
            "n_lc_wrong": n_lc_wrong,
        }
    return per_cell


def per_receptor_consensus(per_cell: dict) -> dict[str, dict]:
    """For each receptor, aggregate across the 4 backbones:
      - n_backbones_success (majority ≥0.5/≥0.5) — models that "get it right"
      - n_backbones_strong (≥0.8/≥0.8)
      - effect_size = median across bb of (partner_d_mean - apo_d_mean)
        Positive → switch works (partner draws d_tm6 outward, apo pulls inward).
        Zero or negative → switch fails.
      - consensus_verdict — "unanimous" all 4 success, "majority" ≥3 success,
        "split" 2/2, "minority" 1/4, "none" 0/4, or "insufficient" if any NA.

    Also returns per-receptor mean pLDDT proxy from plddt columns
    if the cell has them; not always populated by all backbones.
    """
    by_rec: dict[str, dict] = {}
    receptors = sorted({rec for (rec, _) in per_cell.keys()})
    for rec in receptors:
        cells = [per_cell[(rec, bb)] for bb in BACKBONES if (rec, bb) in per_cell]
        if not cells:
            continue
        n_success = sum(1 for c in cells if c.get("success") is True)
        n_strong = sum(1 for c in cells if c.get("strong") is True)
        n_na = sum(1 for c in cells if c.get("verdict") == "NA")
        effects = [
            c["partner_d_mean"] - c["apo_d_mean"]
            for c in cells
            if not math.isnan(c["partner_d_mean"]) and not math.isnan(c["apo_d_mean"])
        ]
        effect_size = statistics.median(effects) if effects else math.nan

        n_bb = len(cells)
        if n_na:
            verdict = "insufficient"
        elif n_success == n_bb:
            verdict = "unanimous"
        elif n_success >= max(3, n_bb - 1):
            verdict = "majority"
        elif n_success * 2 == n_bb:
            verdict = "split"
        elif n_success == 1:
            verdict = "minority"
        else:
            verdict = "none"

        by_rec[rec] = {
            "n_backbones_success": n_success,
            "n_backbones_strong": n_strong,
            "n_backbones_na": n_na,
            "effect_size_med": effect_size,
            "consensus": verdict,
        }
    return by_rec


def per_backbone_summary(per_cell: dict) -> list[dict]:
    """Aggregate per (X, Y) cells → per-backbone summary rows."""
    by_bb: dict[str, dict] = {bb: {
        "n_receptors": 0, "n_success": 0, "n_strong": 0, "n_na": 0,
        "n_hc_correct": 0, "n_hc_wrong": 0, "n_lc_correct": 0, "n_lc_wrong": 0,
    } for bb in BACKBONES}
    for (rec, bb), cell in per_cell.items():
        if bb not in by_bb:
            continue
        by_bb[bb]["n_receptors"] += 1
        if cell["verdict"] == "NA":
            by_bb[bb]["n_na"] += 1
        else:
            if cell["success"]:
                by_bb[bb]["n_success"] += 1
            if cell["strong"]:
                by_bb[bb]["n_strong"] += 1
        by_bb[bb]["n_hc_correct"] += cell["n_hc_correct"]
        by_bb[bb]["n_hc_wrong"] += cell["n_hc_wrong"]
        by_bb[bb]["n_lc_correct"] += cell["n_lc_correct"]
        by_bb[bb]["n_lc_wrong"] += cell["n_lc_wrong"]

    return [{"backbone": bb, **stats} for bb, stats in by_bb.items()]


def write_findings(per_cell: dict, summary: list[dict], out: Path,
                   n_receptors: int, k_per_cell: int,
                   consensus: dict[str, dict] | None = None) -> None:
    lines: list[str] = []
    lines.append("# Block A switch-test — findings")
    lines.append("")
    lines.append(f"**Predictions**: {n_receptors} receptors × 2 conditions × 4 backbones × K={k_per_cell} replicates per cell.")
    lines.append(f"**Success criterion**: `active_hitrate ≥ 0.5` (majority active when partnered with Gαs) AND `inactive_hitrate ≥ 0.5` (majority inactive when apo).")
    lines.append(f"**Strong bar**: both ≥ 0.8.")
    lines.append("")

    # 1. Per-backbone success table
    lines.append("## 1. Per-backbone success count")
    lines.append("")
    lines.append("| backbone | N receptors | N success (≥0.5/≥0.5) | N strong (≥0.8/≥0.8) | N NaN (dropped) |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in summary:
        lines.append(
            f"| {row['backbone']} | {row['n_receptors']} | "
            f"{row['n_success']}/{row['n_receptors'] - row['n_na']} | "
            f"{row['n_strong']}/{row['n_receptors'] - row['n_na']} | "
            f"{row['n_na']} |"
        )
    lines.append("")

    # 2. Per-receptor across-backbone verdict
    lines.append("## 2. Per-receptor across-backbone verdict")
    lines.append("")
    receptors = sorted({rec for (rec, _) in per_cell.keys()})
    lines.append("| receptor | boltz | of3 | protenix | chai | Δd_tm6 (Å, median) | consensus |")
    lines.append("|---|:-:|:-:|:-:|:-:|---:|:-:|")
    for rec in receptors:
        row_parts = [rec]
        for bb in BACKBONES:
            cell = per_cell.get((rec, bb))
            if cell is None:
                row_parts.append("—")
            else:
                v = cell["verdict"]
                sym = {"strong": "**✓✓**", "success": "✓", "fail": "✗", "NA": "?"}[v]
                row_parts.append(sym)
        cons = consensus.get(rec, {}) if consensus else {}
        eff = cons.get("effect_size_med", math.nan)
        eff_str = f"{eff:+.2f}" if not math.isnan(eff) else "—"
        row_parts.append(eff_str)
        row_parts.append(cons.get("consensus", "—"))
        lines.append("| " + " | ".join(row_parts) + " |")
    lines.append("")
    lines.append("Legend: `**✓✓**` = strong (≥0.8/≥0.8); `✓` = success (≥0.5/≥0.5); `✗` = fail; `?` = insufficient valid replicates. Δd_tm6 = median across backbones of `partner_d_mean - apo_d_mean`; positive → the switch pulls TM6 outward when partnered, inward when apo. Consensus: unanimous / majority / split / minority / none / insufficient.")
    lines.append("")

    # 2b. Cross-backbone consensus summary
    if consensus:
        c_counts: dict[str, int] = {"unanimous": 0, "majority": 0, "split": 0,
                                    "minority": 0, "none": 0, "insufficient": 0}
        for r in receptors:
            c_counts[consensus[r]["consensus"]] = c_counts.get(consensus[r]["consensus"], 0) + 1
        lines.append("### 2b. Cross-backbone consensus")
        lines.append("")
        lines.append("| consensus | N receptors |")
        lines.append("|---|---:|")
        for k in ("unanimous", "majority", "split", "minority", "none", "insufficient"):
            lines.append(f"| {k} | {c_counts.get(k, 0)} |")
        lines.append("")
        lines.append("Unanimous or majority means the switch works across most backbones for that receptor — a stronger evidence bar than a single backbone succeeding.")
        lines.append("")

    # 3. Confidence miscalibration table
    lines.append("## 3. Confidence miscalibration")
    lines.append("")
    lines.append(f"pLDDT high = ≥{HIGH_CONF}; low = <{LOW_CONF}. Rate = wrong / (correct + wrong) in that bucket.")
    lines.append("")
    lines.append("| backbone | high-conf correct | high-conf WRONG | high-conf wrong rate | low-conf correct | low-conf WRONG |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in summary:
        hcc, hcw = row["n_hc_correct"], row["n_hc_wrong"]
        rate = hcw / (hcc + hcw) if (hcc + hcw) else float("nan")
        rate_str = f"{100*rate:.1f}%" if not math.isnan(rate) else "—"
        lines.append(
            f"| {row['backbone']} | {hcc} | **{hcw}** | {rate_str} | "
            f"{row['n_lc_correct']} | {row['n_lc_wrong']} |"
        )
    lines.append("")
    lines.append("Interpretation: if `high-conf wrong rate` is materially > 0 for a backbone, the model is confidently wrong on some receptors — pLDDT is not a trustworthy filter for that backbone on this task.")
    lines.append("")

    # 4. AA2AR-specific breakdown
    lines.append("## 4. AA2AR — extending the anecdote")
    lines.append("")
    lines.append("Prior work: Boltz reports d_tm6 ≈ 9.6 Å with high pLDDT for AA2AR-Gs, but the real answer is ≈ 18.3 Å. Below, `partner_d_mean` and `apo_d_mean` per backbone for AA2AR:")
    lines.append("")
    lines.append("| backbone | partner d_tm6 mean | apo d_tm6 mean | verdict |")
    lines.append("|---|---:|---:|:-:|")
    for bb in BACKBONES:
        cell = per_cell.get(("AA2AR", bb))
        if cell is None:
            lines.append(f"| {bb} | — | — | — |")
            continue
        lines.append(
            f"| {bb} | {cell['partner_d_mean']:.2f} | {cell['apo_d_mean']:.2f} | {cell['verdict']} |"
        )
    lines.append("")
    lines.append("Reference midpoint for AA2AR: 13.13 Å (5G53 active 18.6 vs 5NM4 inactive 7.7).")
    lines.append("")

    # 5. Reproducibility
    lines.append("## 5. Reproducibility")
    lines.append("")
    lines.append("- Manifest: `experiments/018_block_a_switch_test/runs/initial/manifest.csv`")
    lines.append("- Rows: `experiments/018_block_a_switch_test/rows.csv`")
    lines.append("- HPC scratch: `/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/`")
    lines.append("- Analysis: `scripts/analyse_block_a.py`")
    lines.append("- Plan: `~/.claude/plans/silly-leaping-aho.md`")
    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="analyse_block_a")
    p.add_argument("--rows", type=Path, required=True, help="rows.csv path")
    p.add_argument("--findings-out", type=Path, required=True, help="findings.md path")
    p.add_argument("--k-per-cell", type=int, default=5,
                   help="predictions per (receptor, condition, backbone) cell (for min-valid gate)")
    args = p.parse_args(argv)

    rows = load_rows(args.rows)
    if not rows:
        print(f"empty rows.csv at {args.rows}", file=sys.stderr)
        return 1

    per_cell = analyse(rows, k_per_cell=args.k_per_cell)
    summary = per_backbone_summary(per_cell)
    consensus = per_receptor_consensus(per_cell)
    n_receptors = len({rec for (rec, _) in per_cell.keys()})

    print(f"Loaded {len(rows)} rows; {n_receptors} distinct receptors, {len(per_cell)} (rec, bb) cells.")
    print()
    print(f"{'backbone':<10} {'N_rec':>5} {'success':>8} {'strong':>8} {'NA':>5}  hc_wrong_rate")
    for row in summary:
        hcc, hcw = row["n_hc_correct"], row["n_hc_wrong"]
        rate = hcw / (hcc + hcw) if (hcc + hcw) else float("nan")
        rate_str = f"{100*rate:5.1f}%" if not math.isnan(rate) else "  n/a"
        print(f"{row['backbone']:<10} {row['n_receptors']:>5} {row['n_success']:>8} "
              f"{row['n_strong']:>8} {row['n_na']:>5}  {rate_str}")

    print()
    print("Cross-backbone consensus:")
    from collections import Counter
    verdict_counts = Counter(v["consensus"] for v in consensus.values())
    for k in ("unanimous", "majority", "split", "minority", "none", "insufficient"):
        print(f"  {k:<12} {verdict_counts.get(k, 0):>3}")

    write_findings(per_cell, summary, args.findings_out, n_receptors, args.k_per_cell,
                   consensus=consensus)
    print(f"\nWrote {args.findings_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
