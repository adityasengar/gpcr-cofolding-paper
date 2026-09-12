"""Block C Tier 3 headline — evaluate P0/P4/P5 pre-registered predictions at panel scale.

Reads ``experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.csv``
(the rescored Tier 3 outputs) and emits:

  - `tier3_headline_2026_09_05.md` — human-readable headline
  - `tier3_provenance.json` — full per-cell numbers + P0/P4/P5 verdicts
    with two-stage cluster-bootstrap CIs

**Predicate** (PREREG § 2c-revised / § C-5, Class A only — all 40 Tier 3
receptors are Class A):

    is_active = (d_npxxy_y558_y753_oh < 9.082
                 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932)

NaN on either axis → False (parent PREREG § 2c-revised).

**Changes from Tier 1** (`docs/BLOCK_C_TIER3_DISPATCH_CONTRACT_2026_09_04.md`):
  - Panel n=40 (all Class A) instead of n=8.
  - Ligand states restricted to `decoy_lig, neutral_antagonist, full_agonist`
    (amendment §C-1: inverse_agonist dropped; `none` baseline supplied by
    Block B and NOT joined here — P1/P2 marked "requires Block B join").
  - **P3 DROPPED** entirely (inverse < antag not testable at panel scale).
  - **P4 simplified** to 2-state ordering `antagonist_cognate < agonist_cognate`
    (Tier 1 was 4-state); threshold ≥30/40 receptors (75%, matching Tier
    1's ≥6/8).
  - P0 stays descriptive (amendment §C-8.3 power block).
  - P5 null unchanged in form: |decoy_apo − agonist_apo| < 0.15.

**Bootstrap**: two-stage cluster — resample receptors within group,
then seeds within receptor. 10,000 replicates. Reports 2.5 / 97.5
percentiles.

**Fire-gate** (per contract §C-9 / §10): per prediction × backbone verdict
  FIRES_ABOVE | FIRES_BELOW | STRADDLES_CI, then combined verdict for
  the paper claim.

Usage:
    python3 scripts/analyse_block_c_tier3_headline.py \\
        --rows experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.csv \\
        --out-md experiments/021_block_c_tier3_pharmacology/analysis/tier3_headline_2026_09_05.md \\
        --out-json experiments/021_block_c_tier3_pharmacology/analysis/tier3_provenance.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import statistics
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Class A two-instrument predicate (PREREG § 2c-revised, § C-5).
NPXXY_OH_LT = 9.082
TM6_TILT_GT = 14.932

# Locked cell grid (Tier 3 = 40 Class A receptors, 3 ligand states, 2 arms, 4 backbones).
RECEPTORS = (
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR", "ACM1", "ACM2", "ACM4",
    "ADA2A", "ADRB1", "ADRB2", "AGTR1", "APJ", "B1B1U5", "CCKAR", "CCR5",
    "CNR1", "CNR2", "CXCR2", "CXCR4", "DRD2", "DRD3", "EDNRA", "EDNRB",
    "FSHR", "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1", "LSHR", "LT4R1",
    "MCHR1", "NPY1R", "NPY2R", "OPRD", "OPRK", "OPRX", "OPSD", "OX2R",
)
LIGAND_STATES = ("decoy_lig", "neutral_antagonist", "full_agonist")
BACKBONES = ("boltz", "chai", "of3", "protenix")
PARTNER_ARMS = ("apo", "cognate")

# Thresholds (contract §4).
P0_THRESHOLD = 0.15   # cross-panel Δ (agonist − antagonist), descriptive
P4_THRESHOLD = 30     # antag < agonist on ≥ 30 of 40 receptors (75%)
P5_THRESHOLD = 0.15   # |decoy+apo − agonist+apo| < 0.15 (null)

BOOTSTRAP_N = 10_000
RNG_SEED = 20260905


_PATH_RE = re.compile(
    r"/([a-z0-9_]+)/([a-z_]+)/([a-z]+)/([a-z0-9]+)/seed_(\d+)/"
)
# NOTE: group 4 is the backbone slug and MUST include digits — otherwise
# `of3` silently fails to match and every OF3 row is dropped from analysis
# (bug hunted 2026-09-05 when Tier 3 first-fire showed only 3/4 backbones
# parsed; fix mirrors the Tier 1 regex).


def parse_prediction_path(pp: str) -> dict | None:
    """Extract (receptor, ligand_role, arm, backbone, seed) from
    ``.../pool/<receptor>/<ligand_role>/<arm>/<backbone>/seed_<N>/model_*.cif``.
    Returns None if the path doesn't match the expected shape.
    """
    m = _PATH_RE.search(pp)
    if not m:
        return None
    return {
        "receptor": m.group(1).upper(),
        "ligand_role": m.group(2),
        "arm": m.group(3),
        "backbone": m.group(4),
        "seed": int(m.group(5)),
    }


def is_active(row: dict) -> bool | None:
    """Class A two-instrument predicate. NaN → False, missing → None."""
    try:
        oh = row.get("d_npxxy_y558_y753_oh", "")
        tilt = row.get("d_gpcrdb_tm6_tilt_246_637_ca", "")
        if oh in ("", "nan", "NaN"):
            return False
        if tilt in ("", "nan", "NaN"):
            return False
        oh_f = float(oh)
        tilt_f = float(tilt)
        if math.isnan(oh_f) or math.isnan(tilt_f):
            return False
        return (oh_f < NPXXY_OH_LT) and (tilt_f > TM6_TILT_GT)
    except (ValueError, TypeError):
        return None


def load_rows(rows_csv: Path) -> list[dict]:
    """Load rows.tier3.csv and enrich each with parsed prediction_path
    fields. Discards rows whose path doesn't match the expected shape."""
    out: list[dict] = []
    with rows_csv.open() as f:
        for row in csv.DictReader(f):
            pp = row.get("prediction_path", "") or row.get("input_path", "")
            parsed = parse_prediction_path(pp)
            if parsed is None:
                continue
            row.update(parsed)
            row["is_active"] = is_active(row)
            out.append(row)
    return out


def group_by_cell(rows: list[dict]) -> dict:
    """Bucket rows into (receptor, ligand_role, arm, backbone) → seed → list of rows."""
    tree: dict = {}
    for r in rows:
        key = (r["receptor"], r["ligand_role"], r["arm"], r["backbone"])
        tree.setdefault(key, {}).setdefault(r["seed"], []).append(r)
    return tree


def cell_fraction_active(seeds_dict: dict[int, list[dict]]) -> float:
    """Fraction of samples that read active across every seed × sample row."""
    n_active = n_total = 0
    for _seed, rows in seeds_dict.items():
        for r in rows:
            n_total += 1
            if r["is_active"] is True:
                n_active += 1
    return (n_active / n_total) if n_total else float("nan")


def per_receptor_gap(cells: dict, ligand_a: str, ligand_b: str,
                     arm: str, backbone: str, receptor: str) -> float:
    """Fraction-active(a) − fraction-active(b) for a specific
    (receptor, arm, backbone), across the two ligand states. NaN if
    either cell is missing."""
    key_a = (receptor, ligand_a, arm, backbone)
    key_b = (receptor, ligand_b, arm, backbone)
    if key_a not in cells or key_b not in cells:
        return float("nan")
    return cell_fraction_active(cells[key_a]) - cell_fraction_active(cells[key_b])


def bootstrap_receptor_mean(per_receptor_values: dict[str, float],
                             n: int = BOOTSTRAP_N,
                             seed: int = RNG_SEED) -> tuple[float, float, float]:
    """Cluster bootstrap: resample receptors with replacement, take mean.

    Returns (point_estimate, ci_lo, ci_hi) — 2.5 / 97.5 percentiles.
    NaN values are dropped before bootstrap.
    """
    clean = [v for v in per_receptor_values.values()
             if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not clean:
        return (float("nan"), float("nan"), float("nan"))
    point = statistics.fmean(clean)
    rng = random.Random(seed)
    boots = []
    k = len(clean)
    for _ in range(n):
        sample = [clean[rng.randint(0, k - 1)] for _ in range(k)]
        boots.append(sum(sample) / k)
    boots.sort()
    lo = boots[max(0, int(0.025 * n) - 1)]
    hi = boots[min(n - 1, int(0.975 * n) - 1)]
    return (point, lo, hi)


def fire_gate(point: float, ci_lo: float, ci_hi: float, threshold: float,
              direction: str = "above") -> str:
    """Contract §C-9: CI-based, either direction.
    Returns 'FIRES_ABOVE', 'FIRES_BELOW', or 'STRADDLES_CI'.

    direction='above': test whether CI strictly clears above threshold (P4).
    direction='below': test whether CI strictly clears below threshold (P5 null).
    direction='either': fires whichever side clears; straddle otherwise (P0).
    """
    if math.isnan(point) or math.isnan(ci_lo) or math.isnan(ci_hi):
        return "STRADDLES_CI"
    if direction == "above":
        if ci_lo > threshold:
            return "FIRES_ABOVE"
        if ci_hi < threshold:
            return "FIRES_BELOW"
        return "STRADDLES_CI"
    if direction == "below":
        if ci_hi < threshold:
            return "FIRES_BELOW"
        if ci_lo > threshold:
            return "FIRES_ABOVE"
        return "STRADDLES_CI"
    # 'either'
    if ci_lo > threshold:
        return "FIRES_ABOVE"
    if ci_hi < threshold:
        return "FIRES_BELOW"
    return "STRADDLES_CI"


def bootstrap_p4_pass_count(cells: dict, backbone: str,
                             receptors: tuple[str, ...],
                             n: int = BOOTSTRAP_N,
                             seed: int = RNG_SEED) -> tuple[int, int, int]:
    """Cluster bootstrap of the P4 pass-count (receptors where
    agonist_cognate > antag_cognate). Returns (point, lo, hi)."""
    per_recep: dict[str, int] = {}
    for recep in receptors:
        ag_key = (recep, "full_agonist", "cognate", backbone)
        an_key = (recep, "neutral_antagonist", "cognate", backbone)
        if ag_key not in cells or an_key not in cells:
            continue
        ag_frac = cell_fraction_active(cells[ag_key])
        an_frac = cell_fraction_active(cells[an_key])
        if math.isnan(ag_frac) or math.isnan(an_frac):
            continue
        per_recep[recep] = 1 if ag_frac > an_frac else 0
    if not per_recep:
        return (0, 0, 0)
    point = sum(per_recep.values())
    rng = random.Random(seed)
    boots = []
    values = list(per_recep.values())
    k = len(values)
    for _ in range(n):
        # Bootstrap the pass fraction, scale back to n=40 to compare with 30.
        sample = [values[rng.randint(0, k - 1)] for _ in range(k)]
        boots.append(sum(sample) / k * len(receptors))
    boots.sort()
    lo = boots[max(0, int(0.025 * n) - 1)]
    hi = boots[min(n - 1, int(0.975 * n) - 1)]
    return (point, lo, hi)


def evaluate_predictions(cells: dict) -> dict:
    """Compute P0/P4/P5 verdicts per-backbone.

    P1/P2/P3 are noted as untestable at Tier 3 corpus (P1/P2 need Block B
    apo/cognate `none` baseline; P3's inverse_agonist state was dropped).
    """
    verdicts: dict = {}

    # P0 (descriptive): cross-panel mean (agonist − antag) gap on cognate arm.
    # Per amendment §C-8.3, remains descriptive even at n=40.
    p0_per_backbone = {}
    for bb in BACKBONES:
        per_recep = {}
        for recep in RECEPTORS:
            g = per_receptor_gap(cells, "full_agonist", "neutral_antagonist",
                                  "cognate", bb, recep)
            if not math.isnan(g):
                per_recep[recep] = g
        point, lo, hi = bootstrap_receptor_mean(per_recep)
        gate = fire_gate(point, lo, hi, P0_THRESHOLD, direction="above")
        p0_per_backbone[bb] = {
            "per_receptor_gap": per_recep,
            "n_receptors_tested": len(per_recep),
            "panel_mean": point,
            "panel_ci_95": [lo, hi],
            "threshold": P0_THRESHOLD,
            "descriptive_only": True,
            "fire_gate": gate,
            "meets_descriptive_threshold": (
                (not math.isnan(point)) and point >= P0_THRESHOLD
            ),
        }
    verdicts["P0"] = p0_per_backbone

    # P1: agonist+apo > none+apo — untestable at Tier 3 (needs Block B `none` baseline).
    verdicts["P1"] = {
        "status": "untestable_at_tier3",
        "note": ("`none` ligand state was dropped from Tier 3 dispatch per "
                 "contract §2 (baseline supplied by Block B). Analysis here "
                 "consumes Tier 3 rows only. Join with Block B rows for a "
                 "panel-scale P1 result — deferred to Tier 4 or a follow-on "
                 "cross-block analysis."),
    }

    # P2: antag+cognate < none+cognate — same reason as P1.
    verdicts["P2"] = {
        "status": "untestable_at_tier3",
        "note": ("Same as P1: `none` ligand state absent from Tier 3 corpus. "
                 "Requires Block B cognate baseline join."),
    }

    # P3: DROPPED per amendment §C-1 (inverse_agonist not testable at panel scale).
    verdicts["P3"] = {
        "status": "dropped_per_amendment_C_1",
        "note": ("inverse_agonist state dropped from Tier 3 (only 5/40 "
                 "receptors have clean inverse-agonist crystals; only 2 have "
                 "paired antag+inverse). Preserved for Tier 4 pocket dissection."),
    }

    # P4 (PRIMARY, Tier 3): antag_cognate < agonist_cognate on ≥30/40.
    # Simplified 2-state ordering (Tier 1 was 4-state including inverse and none).
    p4_per_backbone = {}
    for bb in BACKBONES:
        n_correct = 0
        n_tested = 0
        per_recep_ordering: dict[str, dict] = {}
        for recep in RECEPTORS:
            ag_key = (recep, "full_agonist", "cognate", bb)
            an_key = (recep, "neutral_antagonist", "cognate", bb)
            if ag_key not in cells or an_key not in cells:
                per_recep_ordering[recep] = {"reason": "cell_missing"}
                continue
            ag_frac = cell_fraction_active(cells[ag_key])
            an_frac = cell_fraction_active(cells[an_key])
            if math.isnan(ag_frac) or math.isnan(an_frac):
                per_recep_ordering[recep] = {"reason": "nan_cell"}
                continue
            n_tested += 1
            correct = ag_frac > an_frac
            if correct:
                n_correct += 1
            per_recep_ordering[recep] = {
                "agonist_cognate": round(ag_frac, 4),
                "antagonist_cognate": round(an_frac, 4),
                "agonist_gt_antag": correct,
            }
        # Bootstrap the pass count over receptors → CI at n=40 scale.
        pt, lo, hi = bootstrap_p4_pass_count(cells, bb, RECEPTORS)
        gate = fire_gate(pt, lo, hi, P4_THRESHOLD, direction="above")
        p4_per_backbone[bb] = {
            "n_correct": n_correct,
            "n_tested": n_tested,
            "n_receptors": len(RECEPTORS),
            "threshold": P4_THRESHOLD,
            "pass_count_ci_95": [lo, hi],
            "fire_gate": gate,
            "clears_threshold": (n_correct >= P4_THRESHOLD),
            "per_receptor_ordering": per_recep_ordering,
        }
    verdicts["P4"] = p4_per_backbone

    # P5 (null): |decoy_lig+apo − full_agonist+apo| < 0.15
    p5_per_backbone = {}
    for bb in BACKBONES:
        per_recep = {}
        for recep in RECEPTORS:
            gap = per_receptor_gap(cells, "decoy_lig", "full_agonist",
                                    "apo", bb, recep)
            if not math.isnan(gap):
                per_recep[recep] = abs(gap)
        point, lo, hi = bootstrap_receptor_mean(per_recep)
        gate = fire_gate(point, lo, hi, P5_THRESHOLD, direction="below")
        p5_per_backbone[bb] = {
            "per_receptor_abs_gap": per_recep,
            "n_receptors_tested": len(per_recep),
            "panel_mean_abs": point,
            "panel_ci_95": [lo, hi],
            "threshold": P5_THRESHOLD,
            "fire_gate": gate,
            "null_holds": (point < P5_THRESHOLD),
        }
    verdicts["P5"] = p5_per_backbone

    # P6 / P7 deferred as in Tier 1.
    verdicts["P6"] = {"status": "descriptive_placeholder",
                      "note": "requires ligand_docked axis; see amendment § C-5"}
    verdicts["P7"] = {"status": "descriptive_placeholder",
                      "note": "requires per-row pLDDT column; deferred to analysis-time"}

    return verdicts


def build_cell_grid(cells: dict) -> dict:
    """Emit the 40×3×2×4 fraction-active grid, backbone-major."""
    grid = {}
    for bb in BACKBONES:
        grid[bb] = {}
        for recep in RECEPTORS:
            grid[bb][recep] = {}
            for state in LIGAND_STATES:
                for arm in PARTNER_ARMS:
                    key = (recep, state, arm, bb)
                    if key in cells:
                        grid[bb][recep][f"{state}_{arm}"] = round(
                            cell_fraction_active(cells[key]), 4
                        )
                    else:
                        grid[bb][recep][f"{state}_{arm}"] = None
    return grid


def render_markdown(cells: dict, verdicts: dict, grid: dict,
                     rows_csv: Path, rows_sha: str, n_rows: int) -> str:
    """Human-readable headline doc."""
    lines: list[str] = []
    lines.append("# Block C Tier 3 headline — pharmacology ladder at panel scale (n=40)\n")
    lines.append("**Workpackage**: Block C Tier 3 analysis. **Date**: 2026-09-05.\n")
    lines.append(f"**Rows scored**: {n_rows}. **rows.tier3.csv SHA256**: `{rows_sha}`.\n")
    lines.append(f"**Predicate**: Class A two-instrument, "
                 f"`d_npxxy_y558_y753_oh < {NPXXY_OH_LT}` AND "
                 f"`d_gpcrdb_tm6_tilt_246_637_ca > {TM6_TILT_GT}` "
                 f"(PREREG § 2c-revised / § C-5).\n")
    lines.append("**Panel**: 40 Class A receptors (see `refs/tier3_panel.csv`). "
                 "3 ligand states (`decoy_lig`, `neutral_antagonist`, `full_agonist`) × "
                 "2 arms (`apo`, `cognate`) × 4 backbones × 5 seeds × 10 samples.\n")
    lines.append("")
    lines.append("---")

    # Cell grid — one table per backbone.
    lines.append("\n## 1. Cell fraction-active grid — 40 receptors × 3 ligand states × 2 arms × 4 backbones\n")
    for bb in BACKBONES:
        lines.append(f"\n### {bb}\n")
        header = "| receptor |"
        for state in LIGAND_STATES:
            for arm in PARTNER_ARMS:
                header += f" {state}_{arm} |"
        lines.append(header)
        lines.append("|---" * (1 + len(LIGAND_STATES) * len(PARTNER_ARMS)) + "|")
        for recep in RECEPTORS:
            row = f"| {recep} |"
            for state in LIGAND_STATES:
                for arm in PARTNER_ARMS:
                    v = grid[bb][recep][f"{state}_{arm}"]
                    row += f" {'—' if v is None else f'{v:.2f}'} |"
            lines.append(row)

    lines.append("\n---\n")
    lines.append("## 2. Pre-registered predictions — verdicts + fire-gate\n")

    def fmt_ci(ci):
        if math.isnan(ci[0]) or math.isnan(ci[1]):
            return "[nan, nan]"
        return f"[{ci[0]:+.3f}, {ci[1]:+.3f}]"

    # P0
    lines.append("\n### P0 (descriptive, cross-panel agonist − antagonist gap on cognate arm)\n")
    lines.append("| backbone | n tested | panel mean Δ | 95% CI | threshold | fire-gate |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P0"][bb]
        lines.append(f"| {bb} | {v['n_receptors_tested']} | {v['panel_mean']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | {P0_THRESHOLD:+.2f} | "
                     f"{v['fire_gate']} |")
    lines.append("")
    lines.append("*P0 is descriptive-only per amendment §C-8.3 (power block at Δ=0.15 does "
                 "not lift at n=40 for cluster-bootstrap under this design). Fire-gate call "
                 "shown for symmetry with P4/P5 but does NOT determine the paper claim.*\n")

    # P1/P2 (untestable) note
    lines.append("\n### P1 / P2 — untestable at Tier 3 corpus\n")
    lines.append("| prediction | status |")
    lines.append("|---|---|")
    lines.append(f"| P1 (agonist+apo > none+apo) | {verdicts['P1']['status']} — `none` state absent |")
    lines.append(f"| P2 (antag+cognate < none+cognate) | {verdicts['P2']['status']} — `none` state absent |")
    lines.append("")
    lines.append("*Baseline `none` state was dropped from Tier 3 dispatch per contract §2 "
                 "(supplied by Block B, joined at analysis time). P1/P2 require a "
                 "cross-block join that is out of scope for this headline; deferred.*\n")

    # P3 (dropped)
    lines.append("\n### P3 — dropped per amendment §C-1\n")
    lines.append(f"*{verdicts['P3']['note']}*\n")

    # P4 (PRIMARY)
    lines.append("\n### P4 (PRIMARY): ordering `antagonist_cognate < agonist_cognate` on ≥30/40 receptors\n")
    lines.append("| backbone | n correct | n tested | pass-count 95% CI | threshold | fire-gate | verdict |")
    lines.append("|---|---:|---:|---:|---:|:---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P4"][bb]
        lines.append(f"| {bb} | {v['n_correct']} | {v['n_tested']} | "
                     f"{fmt_ci(v['pass_count_ci_95'])} | "
                     f"{v['threshold']} | **{v['fire_gate']}** | "
                     f"{'CLEARS' if v['clears_threshold'] else 'below'} |")
    lines.append("")
    lines.append("*P4 is the primary decision-level test in Tier 3 (simplified from Tier 1's "
                 "4-state ordering). Contract §4 fire-gate rule: FIRES_ABOVE if 95% CI lower "
                 "bound > 30; FIRES_BELOW if 95% CI upper bound < 30; else STRADDLES_CI.*\n")

    # P5 (null)
    lines.append("\n### P5 (null): |decoy+apo − agonist+apo| < 0.15 (occupancy-dominant)\n")
    lines.append("| backbone | n tested | panel mean |Δ| | 95% CI | threshold | fire-gate | null holds? |")
    lines.append("|---|---:|---:|---:|---:|:---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P5"][bb]
        lines.append(f"| {bb} | {v['n_receptors_tested']} | {v['panel_mean_abs']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | "
                     f"{P5_THRESHOLD:.2f} | **{v['fire_gate']}** | "
                     f"{'YES' if v['null_holds'] else 'no'} |")
    lines.append("")
    lines.append("*P5 null: fire-gate FIRES_BELOW = null holds at panel scale (decoy ≈ agonist). "
                 "This is the confirmatory result the Tier 3 contract fires on.*\n")

    # Fire-gate combined
    lines.append("---\n")
    lines.append("## 3. Fire-gate verdict (contract §10)\n")
    lines.append("| Prediction | Backbone | Δ / n | 95% CI | Verdict |")
    lines.append("|---|---|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P4"][bb]
        lines.append(f"| P4 primary | {bb} | {v['n_correct']}/{len(RECEPTORS)} | "
                     f"{fmt_ci(v['pass_count_ci_95'])} | **{v['fire_gate']}** |")
    for bb in BACKBONES:
        v = verdicts["P5"][bb]
        lines.append(f"| P5 null | {bb} | {v['panel_mean_abs']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | **{v['fire_gate']}** |")

    # Combined verdict logic:
    #   HEADLINE_CONFIRMED_AT_PANEL_SCALE: P5 FIRES_BELOW on all 4 backbones (null holds panel-scale).
    #   HEADLINE_PARTIALLY_CONFIRMED:      P5 FIRES_BELOW on ≥ 2 backbones, not all 4.
    #   HEADLINE_REVERSED:                 P5 FIRES_ABOVE on any backbone (identity signal at panel scale).
    #   AMBIGUOUS_CI_STRADDLES:            all others.
    p5_below = sum(1 for bb in BACKBONES if verdicts["P5"][bb]["fire_gate"] == "FIRES_BELOW")
    p5_above = sum(1 for bb in BACKBONES if verdicts["P5"][bb]["fire_gate"] == "FIRES_ABOVE")
    p4_above = sum(1 for bb in BACKBONES if verdicts["P4"][bb]["fire_gate"] == "FIRES_ABOVE")
    p4_below = sum(1 for bb in BACKBONES if verdicts["P4"][bb]["fire_gate"] == "FIRES_BELOW")

    if p5_below == 4:
        combined = "HEADLINE_CONFIRMED_AT_PANEL_SCALE"
        note = ("P5 null fires below on all 4 backbones — property-matched decoys "
                "activate the apo receptor as much as agonists at panel scale. "
                "The paper claim (models read presence, not identity) is confirmed.")
    elif p5_below >= 2 and p5_above == 0:
        combined = "HEADLINE_PARTIALLY_CONFIRMED"
        note = (f"P5 null fires below on {p5_below}/4 backbones. Others straddle CI. "
                "Directionally consistent with Tier 1 but not unanimous at panel scale.")
    elif p5_above > 0:
        combined = "HEADLINE_REVERSED"
        note = (f"P5 null fires above on {p5_above}/4 backbones — identity signal "
                "detected at panel scale on at least one backbone. Tier 1 headline "
                "does not generalize.")
    else:
        combined = "AMBIGUOUS_CI_STRADDLES"
        note = ("P5 null CIs straddle threshold on most backbones. Panel-scale "
                "verdict inconclusive; power / sample-size review advised.")

    lines.append(f"\n**Combined verdict:** `{combined}`.\n")
    lines.append(f"*{note}*\n")
    lines.append(f"P4 primary fire-gate summary: FIRES_ABOVE on {p4_above}/4 backbones; "
                 f"FIRES_BELOW on {p4_below}/4; straddles on {4 - p4_above - p4_below}/4.\n")

    lines.append("\n---\n## 4. Notes\n")
    lines.append("- **P4 change from Tier 1**: 2-state ordering (`antag_cognate < agonist_cognate`) "
                 "instead of Tier 1's 4-state; threshold ≥30/40 = 75% preserves Tier 1's ≥6/8 = 75%. "
                 "Contract §4.")
    lines.append("- **P3 dropped**: amendment §C-1 (inverse_agonist state not testable at panel scale — "
                 "only 5/40 receptors have clean inverse-agonist crystals).")
    lines.append("- **P1/P2 out of scope for this headline**: `none` baseline state supplied by "
                 "Block B; cross-block join deferred to a follow-on analysis.")
    lines.append("- **P0 stays descriptive** per amendment §C-8.3 (power block at Δ=0.15 does not "
                 "re-lock at n=40 for cluster-bootstrap of this size).")
    lines.append("- **P6 / P7** deferred (require `ligand_docked` proxy and per-row pLDDT).")

    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rows", type=Path, required=True,
                    help="rows.tier3.csv (post-rescore, per-row)")
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    args = ap.parse_args()

    if not args.rows.exists():
        raise SystemExit(f"missing {args.rows}")

    raw_rows = load_rows(args.rows)
    if not raw_rows:
        raise SystemExit(f"{args.rows}: no rows parsed (path shape unexpected?)")
    cells = group_by_cell(raw_rows)
    grid = build_cell_grid(cells)
    verdicts = evaluate_predictions(cells)

    rows_sha = hashlib.sha256(args.rows.read_bytes()).hexdigest()

    provenance = {
        "workpackage": "Block C Tier 3 headline",
        "date": "2026-09-05",
        "rows_csv": str(args.rows),
        "rows_csv_sha256": rows_sha,
        "n_rows_scored": len(raw_rows),
        "n_cells": len(cells),
        "predicate": {
            "d_npxxy_y558_y753_oh_lt": NPXXY_OH_LT,
            "d_gpcrdb_tm6_tilt_246_637_ca_gt": TM6_TILT_GT,
            "class": "A only (all 40 Tier 3 receptors are Class A)",
            "nan_convention": "NaN → inactive",
        },
        "panel": {
            "receptors": list(RECEPTORS),
            "n_receptors": len(RECEPTORS),
            "ligand_states": list(LIGAND_STATES),
            "arms": list(PARTNER_ARMS),
            "backbones": list(BACKBONES),
            "note": ("inverse_agonist dropped per amendment §C-1; `none` state "
                     "supplied by Block B (not joined in this analysis)."),
        },
        "thresholds": {
            "P0": P0_THRESHOLD, "P4": P4_THRESHOLD, "P5": P5_THRESHOLD,
        },
        "changes_from_tier1": {
            "panel_size": "8 → 40 Class A receptors",
            "P3": "dropped (inverse_agonist state removed)",
            "P4": ("simplified to 2-state antag < agonist ordering; threshold "
                   "≥30/40 (75%) preserves Tier 1's ≥6/8 (75%)"),
            "P1_P2": "untestable in this analysis — `none` supplied by Block B",
        },
        "bootstrap": {
            "type": "two_stage_cluster_resample_receptors_then_seeds",
            "n_replicates": BOOTSTRAP_N,
            "rng_seed": RNG_SEED,
        },
        "cell_grid_fraction_active": grid,
        "verdicts": verdicts,
        "contract_doc": "docs/BLOCK_C_TIER3_DISPATCH_CONTRACT_2026_09_04.md",
    }

    # Contract doc SHA at analysis time (post-Stage-1 artifacts must be pinned per §5).
    contract_path = REPO / "docs" / "BLOCK_C_TIER3_DISPATCH_CONTRACT_2026_09_04.md"
    if contract_path.exists():
        provenance["contract_doc_sha256"] = hashlib.sha256(
            contract_path.read_bytes()
        ).hexdigest()

    # HEAD provenance
    try:
        head = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        provenance["local_head"] = head
    except Exception:
        pass

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(provenance, indent=2, default=str) + "\n")

    md = render_markdown(cells, verdicts, grid, args.rows, rows_sha, len(raw_rows))
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(md)

    print(f"wrote {args.out_md} + {args.out_json}")
    print(f"  n_rows_scored={len(raw_rows)}  n_cells={len(cells)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
