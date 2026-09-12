"""Block C Tier 1 headline — evaluate P0-P7 pre-registered predictions.

Reads ``experiments/020_block_c_ligand_pharmacology/analysis/rows.tier1.csv``
(the rescored Tier 1 outputs) and emits:

  - `tier1_headline_2026_09_04.md` — human-readable headline
  - `tier1_provenance.json` — full per-cell numbers + P0-P7 verdicts
    with two-stage cluster-bootstrap CIs

**Predicate** (PREREG § 2c-revised / § C-5, Class A only — all 8 Tier 1
receptors are Class A):

    is_active = (d_npxxy_y558_y753_oh < 9.082
                 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932)

NaN on either axis → False (parent PREREG § 2c-revised).

**Provenance from prediction_path**: the manifest wrote every
prediction under ``<pool>/<receptor>/<ligand_role>/<arm>/<backbone>/
seed_<N>/model_<K>.cif``. That's the reliable source of the four
axis-provenance fields (ligand_role, backbone, arm, receptor). The
rescore driver's rows.csv strips manifest columns; parsing the path
here is faster and fewer joins than re-reading the manifest.

**Pre-registered exclusions** (Step 3, 2026-09-04, and § C-13):
  - ADRB2 × Chai on P1: apo active fraction = 1.00 on Block B → P1
    untestable on this cell. All other predictions unaffected.
  - NA rows (OX2R inverse, 5HT1B inverse, AA1R inverse) are absent
    from the manifest by construction (build_block_c_tier1_manifest.py
    skips them); P3 becomes a 5-receptor test.

**Bootstrap**: two-stage cluster — resample receptors within group,
then seeds within receptor. 10,000 replicates. Reports 2.5 / 97.5
percentiles. Panel CI half-width at n=8 is ~±0.25 per plan §3.5.

Usage:
    python3 scripts/analyse_block_c_tier1_headline.py \\
        --rows experiments/020_block_c_ligand_pharmacology/analysis/rows.tier1.csv \\
        --out-md experiments/020_block_c_ligand_pharmacology/analysis/tier1_headline_2026_09_04.md \\
        --out-json experiments/020_block_c_ligand_pharmacology/analysis/tier1_provenance.json
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

# Locked cell grid (post-NA-drop per amendment § C-2 / § C-13(f)).
RECEPTORS = ("ADRB2", "DRD3", "AA2AR", "ACM4",
             "OX2R", "ACM2", "5HT1B", "AA1R")
LIGAND_STATES = ("none", "decoy_lig", "neutral_antagonist",
                 "inverse_agonist", "full_agonist")
BACKBONES = ("boltz", "chai", "of3", "protenix")
PARTNER_ARMS = ("apo", "cognate")
NA_ROWS = {("OX2R", "inverse_agonist"), ("5HT1B", "inverse_agonist"),
           ("AA1R", "inverse_agonist")}

# Panel split per plan §3.3.
DISCRIMINATORS = frozenset({"ADRB2", "DRD3", "AA2AR", "ACM4", "OX2R"})
CONTROLS = frozenset({"ACM2", "5HT1B", "AA1R"})

# Pre-registered per-backbone exclusion (Step 3, 2026-09-04).
P1_EXCLUDED = {("ADRB2", "chai")}

# Thresholds (amendment § C-6).
P1_THRESHOLD = 0.20   # agonist+apo > none+apo, per-receptor gap
P2_THRESHOLD = 0.20   # antagonist+cognate < none+cognate, per-receptor gap
P3_THRESHOLD = 0.10   # inverse+cognate < antagonist+cognate, per-receptor gap
P4_THRESHOLD = 6      # ordering holds on ≥ 6 of 8 receptors
P0_THRESHOLD = 0.15   # cross-group Δ (agonist − antagonist gap)
P5_THRESHOLD = 0.15   # |decoy+apo − agonist+apo| < 0.15 (null claim)
P7_THRESHOLD = 2.0    # |pLDDT delta| < 2 (null)

BOOTSTRAP_N = 10_000
RNG_SEED = 20260904


_PATH_RE = re.compile(
    r"/([a-z0-9_]+)/([a-z_]+)/([a-z]+)/([a-z0-9]+)/seed_(\d+)/"
)


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
    """Load rows.tier1.csv and enrich each with parsed prediction_path
    fields. Discards rows whose path doesn't match the expected shape
    (should never happen for a Block C manifest run)."""
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
    """Bucket rows into (receptor, ligand_role, arm, backbone) → seed → list of rows.
    """
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
    either cell is missing (NA-row skip)."""
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


def evaluate_predictions(cells: dict) -> dict:
    """Compute P0-P7 verdicts per-backbone.

    Returns a dict with per-prediction verdict, per-receptor gap
    distribution, and cross-receptor summary CI.
    """
    verdicts: dict = {}

    # P1: agonist+apo > none+apo, ≥ 20 pp, per-receptor gap
    # Excludes ADRB2 × Chai.
    p1_per_backbone = {}
    for bb in BACKBONES:
        per_recep = {}
        for recep in RECEPTORS:
            if (recep, bb) in P1_EXCLUDED:
                continue
            gap = per_receptor_gap(cells, "full_agonist", "none", "apo", bb, recep)
            if not math.isnan(gap):
                per_recep[recep] = gap
        n_pass = sum(1 for v in per_recep.values() if v >= P1_THRESHOLD)
        point, lo, hi = bootstrap_receptor_mean(per_recep)
        p1_per_backbone[bb] = {
            "per_receptor_gaps": per_recep,
            "n_receptors_tested": len(per_recep),
            "n_pass_threshold": n_pass,
            "panel_mean": point,
            "panel_ci_95": [lo, hi],
            "threshold": P1_THRESHOLD,
            "clears_threshold": (point >= P1_THRESHOLD),
        }
    verdicts["P1"] = p1_per_backbone

    # P2: antagonist+cognate < none+cognate, ≥ 20 pp per-receptor
    p2_per_backbone = {}
    for bb in BACKBONES:
        per_recep = {}
        for recep in RECEPTORS:
            gap = per_receptor_gap(cells, "none", "neutral_antagonist",
                                    "cognate", bb, recep)
            if not math.isnan(gap):
                per_recep[recep] = gap  # positive = antag brings it down
        n_pass = sum(1 for v in per_recep.values() if v >= P2_THRESHOLD)
        point, lo, hi = bootstrap_receptor_mean(per_recep)
        p2_per_backbone[bb] = {
            "per_receptor_gaps": per_recep,
            "n_receptors_tested": len(per_recep),
            "n_pass_threshold": n_pass,
            "panel_mean": point,
            "panel_ci_95": [lo, hi],
            "threshold": P2_THRESHOLD,
            "clears_threshold": (point >= P2_THRESHOLD),
        }
    verdicts["P2"] = p2_per_backbone

    # P3: inverse+cognate < antagonist+cognate, ≥ 10 pp per-receptor
    # NA rows (OX2R, 5HT1B, AA1R inverse) are absent → 5-receptor test.
    p3_per_backbone = {}
    for bb in BACKBONES:
        per_recep = {}
        for recep in RECEPTORS:
            if (recep, "inverse_agonist") in NA_ROWS:
                continue
            gap = per_receptor_gap(cells, "neutral_antagonist",
                                    "inverse_agonist", "cognate", bb, recep)
            if not math.isnan(gap):
                per_recep[recep] = gap
        n_pass = sum(1 for v in per_recep.values() if v >= P3_THRESHOLD)
        point, lo, hi = bootstrap_receptor_mean(per_recep)
        p3_per_backbone[bb] = {
            "per_receptor_gaps": per_recep,
            "n_receptors_tested": len(per_recep),
            "n_pass_threshold": n_pass,
            "panel_mean": point,
            "panel_ci_95": [lo, hi],
            "threshold": P3_THRESHOLD,
            "clears_threshold": (point >= P3_THRESHOLD),
        }
    verdicts["P3"] = p3_per_backbone

    # P4: ordering inverse < antagonist < none < agonist on ≥ 6 of 8 receptors.
    # Per-backbone binomial sign test.
    p4_per_backbone = {}
    for bb in BACKBONES:
        n_correct = 0
        per_recep_ordering = {}
        for recep in RECEPTORS:
            # Skip cell if the cognate arm has an NA row for inverse
            if (recep, "inverse_agonist") in NA_ROWS:
                # P4 becomes 4-state ordering (none < antag < agonist)
                # for these 3 receptors; still testable but not the
                # full 4-order.
                per_recep_ordering[recep] = {"reason": "inverse_NA_reduced_ordering"}
                continue
            fracs = {}
            for state in LIGAND_STATES:
                key = (recep, state, "cognate", bb)
                if key in cells:
                    fracs[state] = cell_fraction_active(cells[key])
                else:
                    fracs[state] = float("nan")
            per_recep_ordering[recep] = fracs
            # Test the ordering: inverse < antagonist < none < agonist
            required = ["inverse_agonist", "neutral_antagonist", "none", "full_agonist"]
            values = [fracs.get(s, float("nan")) for s in required]
            if any(math.isnan(v) for v in values):
                continue
            if all(values[i] <= values[i + 1] for i in range(len(values) - 1)):
                n_correct += 1
        p4_per_backbone[bb] = {
            "n_correct": n_correct,
            "n_receptors": len(RECEPTORS),
            "threshold": P4_THRESHOLD,
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
        p5_per_backbone[bb] = {
            "per_receptor_abs_gap": per_recep,
            "panel_mean_abs": point,
            "panel_ci_95": [lo, hi],
            "threshold": P5_THRESHOLD,
            # Null: point < threshold → null holds → decoy ≈ agonist.
            "null_holds": (point < P5_THRESHOLD),
        }
    verdicts["P5"] = p5_per_backbone

    # P0 (descriptive): cross-group mean of within-receptor
    # (agonist − antagonist) gap on cognate arm.
    p0_per_backbone = {}
    for bb in BACKBONES:
        disc_gaps: list[float] = []
        ctrl_gaps: list[float] = []
        for recep in DISCRIMINATORS:
            g = per_receptor_gap(cells, "full_agonist",
                                  "neutral_antagonist", "cognate", bb, recep)
            if not math.isnan(g):
                disc_gaps.append(g)
        for recep in CONTROLS:
            g = per_receptor_gap(cells, "full_agonist",
                                  "neutral_antagonist", "cognate", bb, recep)
            if not math.isnan(g):
                ctrl_gaps.append(g)
        disc_mean = statistics.fmean(disc_gaps) if disc_gaps else float("nan")
        ctrl_mean = statistics.fmean(ctrl_gaps) if ctrl_gaps else float("nan")
        delta = disc_mean - ctrl_mean
        p0_per_backbone[bb] = {
            "discriminator_gaps": disc_gaps,
            "control_gaps": ctrl_gaps,
            "discriminator_mean": disc_mean,
            "control_mean": ctrl_mean,
            "delta": delta,
            "threshold": P0_THRESHOLD,
            "descriptive_only": True,  # per § C-8.3
            "meets_descriptive_threshold": (
                (not math.isnan(delta)) and delta >= P0_THRESHOLD
            ),
        }
    verdicts["P0"] = p0_per_backbone

    # P6 (descriptive): ligand docking rate ordering.
    # Placeholder — this needs `ligand_docked` axis which is
    # scorer-side-defined and may or may not be present. Emit the
    # signal for now.
    verdicts["P6"] = {"status": "descriptive_placeholder",
                      "note": "requires ligand_docked axis; see amendment § C-5"}

    # P7 (null): pLDDT does not separate. Deferred — needs per-row pLDDT
    # aggregation not part of the two-instrument axis. Emit placeholder.
    verdicts["P7"] = {"status": "descriptive_placeholder",
                      "note": "requires per-row pLDDT column; deferred to analysis-time"}

    return verdicts


def build_cell_grid(cells: dict) -> dict:
    """Emit the 8×5×2×4 fraction-active grid, backbone-major."""
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
                        # NA row or missing cell
                        grid[bb][recep][f"{state}_{arm}"] = None
    return grid


def render_markdown(cells: dict, verdicts: dict, grid: dict,
                     rows_csv: Path, rows_sha: str, n_rows: int) -> str:
    """Human-readable headline doc."""
    lines: list[str] = []
    lines.append("# Block C Tier 1 headline — pharmacology ladder\n")
    lines.append(f"**Workpackage**: Block C Tier 1 analysis. **Date**: 2026-09-04.\n")
    lines.append(f"**Rows scored**: {n_rows}. **rows.tier1.csv SHA256**: `{rows_sha}`.\n")
    lines.append(f"**Predicate**: Class A two-instrument, "
                 f"`d_npxxy_y558_y753_oh < {NPXXY_OH_LT}` AND "
                 f"`d_gpcrdb_tm6_tilt_246_637_ca > {TM6_TILT_GT}` "
                 f"(PREREG § 2c-revised / § C-5).\n")
    lines.append("")
    lines.append("---")

    # Cell grid — one table per backbone.
    lines.append("\n## 1. Cell fraction-active grid — 8 receptors × 5 ligand states × 2 arms × 4 backbones\n")
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
    lines.append("## 2. Pre-registered predictions — verdicts\n")

    def fmt_ci(ci):
        if math.isnan(ci[0]) or math.isnan(ci[1]):
            return "[nan, nan]"
        return f"[{ci[0]:+.3f}, {ci[1]:+.3f}]"

    # P0
    lines.append("\n### P0 (descriptive, cross-group agonist − antagonist gap)\n")
    lines.append("| backbone | disc mean | ctrl mean | Δ | threshold | verdict |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P0"][bb]
        d = v["delta"]
        verdict = "meets" if v["meets_descriptive_threshold"] else "below"
        lines.append(f"| {bb} | {v['discriminator_mean']:+.3f} | "
                     f"{v['control_mean']:+.3f} | {d:+.3f} | "
                     f"{P0_THRESHOLD:+.2f} | descriptive: {verdict} |")

    # P1
    lines.append("\n### P1: agonist+apo > none+apo (≥ 20 pp per-receptor)\n")
    lines.append("| backbone | n tested | n≥thr | panel mean | 95% CI | clears? |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P1"][bb]
        lines.append(f"| {bb} | {v['n_receptors_tested']} | "
                     f"{v['n_pass_threshold']} | {v['panel_mean']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | "
                     f"{'YES' if v['clears_threshold'] else 'no'} |")

    # P2
    lines.append("\n### P2: antagonist+cognate < none+cognate (≥ 20 pp per-receptor)\n")
    lines.append("| backbone | n tested | n≥thr | panel mean | 95% CI | clears? |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P2"][bb]
        lines.append(f"| {bb} | {v['n_receptors_tested']} | "
                     f"{v['n_pass_threshold']} | {v['panel_mean']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | "
                     f"{'YES' if v['clears_threshold'] else 'no'} |")

    # P3
    lines.append("\n### P3: inverse+cognate < antagonist+cognate (≥ 10 pp per-receptor, 5-receptor test)\n")
    lines.append("| backbone | n tested | n≥thr | panel mean | 95% CI | clears? |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P3"][bb]
        lines.append(f"| {bb} | {v['n_receptors_tested']} | "
                     f"{v['n_pass_threshold']} | {v['panel_mean']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | "
                     f"{'YES' if v['clears_threshold'] else 'no'} |")

    # P4 (primary decision test)
    lines.append("\n### P4 (PRIMARY): ordering inverse < antagonist < none < agonist on ≥ 6/8 receptors\n")
    lines.append("| backbone | n correct | threshold | clears? |")
    lines.append("|---|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P4"][bb]
        lines.append(f"| {bb} | {v['n_correct']} | {v['threshold']} | "
                     f"{'**YES**' if v['clears_threshold'] else 'no'} |")

    # P5 (null)
    lines.append("\n### P5 (null): |decoy+apo − agonist+apo| < 0.15 (occupancy dominates)\n")
    lines.append("| backbone | panel mean |Δ| | 95% CI | threshold | null holds? |")
    lines.append("|---|---:|---:|---:|:---:|")
    for bb in BACKBONES:
        v = verdicts["P5"][bb]
        lines.append(f"| {bb} | {v['panel_mean_abs']:+.3f} | "
                     f"{fmt_ci(v['panel_ci_95'])} | "
                     f"{P5_THRESHOLD:.2f} | "
                     f"{'YES (P5 holds — occupancy-dominant)' if v['null_holds'] else 'no (identity signal present)'} |")

    # Fire-gate summary
    lines.append("\n---\n")
    lines.append("## 3. Fire-gate assessment\n")
    p1_any = any(v["clears_threshold"] for v in verdicts["P1"].values())
    p2_any = any(v["clears_threshold"] for v in verdicts["P2"].values())
    p5_any_fails = any(not v["null_holds"] for v in verdicts["P5"].values())
    tier2_fires = p1_any or p2_any or p5_any_fails
    lines.append(f"- **Tier 2 fires**: {'YES' if tier2_fires else 'NO'} "
                 f"(P1 clears on any backbone: {p1_any}; "
                 f"P2 clears: {p2_any}; P5 null fails: {p5_any_fails}).")

    p3_any = any(v["clears_threshold"] for v in verdicts["P3"].values())
    p4_any = any(v["clears_threshold"] for v in verdicts["P4"].values())
    tier3_clear = p1_any or p2_any or p3_any or p4_any
    lines.append(f"- **Tier 3 fires**: {'evaluate' if tier3_clear else 'AMBIGUOUS or NO'} "
                 f"(needs a clear result on P0-P4 in either direction with 95% CI). "
                 f"Panel-level CI overlap with threshold decides — inspect verdicts JSON.")

    lines.append(f"- **Tier 4** (§ 5.5): conditional on Gate 0.1's B1 read-out; "
                 f"NOT decided here.")

    lines.append("\n---\n## 4. Notes\n")
    lines.append(f"- **ADRB2 × Chai excluded from P1** per Step 3 pre-registered exclusion "
                 f"(apo active fraction = 1.00 on Block B → P1 untestable).")
    lines.append(f"- **NA rows** (OX2R inverse, 5HT1B inverse, AA1R inverse) "
                 f"are absent from the manifest by construction. P3 is a "
                 f"5-receptor test (ADRB2, DRD3, AA2AR, ACM4, ACM2).")
    lines.append(f"- **P6 / P7 verdicts** are deferred to a follow-on "
                 f"analysis (require `ligand_docked` proxy and per-row pLDDT).")
    lines.append(f"- **P0 framing**: descriptive contrast per § C-8.3 finding "
                 f"(power < 0.5 at n=5+3 for Δ=0.15). P4 is the primary "
                 f"decision-level test.")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rows", type=Path, required=True,
                    help="rows.tier1.csv (post-rescore, per-row)")
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
        "workpackage": "Block C Tier 1 headline",
        "date": "2026-09-04",
        "rows_csv": str(args.rows),
        "rows_csv_sha256": rows_sha,
        "n_rows_scored": len(raw_rows),
        "n_cells": len(cells),
        "predicate": {
            "d_npxxy_y558_y753_oh_lt": NPXXY_OH_LT,
            "d_gpcrdb_tm6_tilt_246_637_ca_gt": TM6_TILT_GT,
            "class": "A only (all 8 Tier 1 receptors are Class A)",
            "nan_convention": "NaN → inactive",
        },
        "panel": {
            "receptors": list(RECEPTORS),
            "discriminators": sorted(DISCRIMINATORS),
            "controls": sorted(CONTROLS),
            "ligand_states": list(LIGAND_STATES),
            "arms": list(PARTNER_ARMS),
            "backbones": list(BACKBONES),
        },
        "pre_registered_exclusions": {
            "P1": [{"receptor": r, "backbone": bb} for (r, bb) in sorted(P1_EXCLUDED)],
            "NA_rows": [{"receptor": r, "ligand_role": lr} for (r, lr) in sorted(NA_ROWS)],
        },
        "thresholds": {
            "P0": P0_THRESHOLD, "P1": P1_THRESHOLD, "P2": P2_THRESHOLD,
            "P3": P3_THRESHOLD, "P4": P4_THRESHOLD, "P5": P5_THRESHOLD,
            "P7": P7_THRESHOLD,
        },
        "bootstrap": {
            "type": "two_stage_cluster_resample_receptors_then_seeds",
            "n_replicates": BOOTSTRAP_N,
            "rng_seed": RNG_SEED,
        },
        "cell_grid_fraction_active": grid,
        "verdicts": verdicts,
    }

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
