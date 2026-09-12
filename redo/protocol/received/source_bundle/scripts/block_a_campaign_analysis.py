"""Block A campaign analysis — coverage, primary Δd_tm6, two-instrument
state calls, OF3 retry histogram.

Input:  experiments/018_block_a_switch_test/analysis/rows.csv
Output (all under analysis/):
  - coverage.csv           rows per (arm × backbone × class) + pass rate + NaN counts
  - primary_result_delta_d_tm6.csv  per (receptor, backbone) + per-class × backbone medians
  - two_instrument_state_calls.csv  fraction of receptors called active per class × backbone
  - of3_retry_histogram.csv        counts by retry-count bucket

Primary predicate per PREREG §2:
    npxxy-OH:                d_npxxy_y558_y753_oh < 9.08
    GPCRdb TM6 tilt (CA):    d_gpcrdb_tm6_tilt_246_637_ca > 14.932
Both must hold on the cognate arm to call the receptor "active".
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CLASS_A_PRIMARY = {
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR",
    "ACM1", "ACM2", "ACM4", "ADA2A", "ADRB1",
    "ADRB2", "AGTR1", "APJ", "CCKAR",
    "CCR5", "CNR2", "CXCR2", "CXCR4",
    "DRD2", "DRD3", "EDNRA", "EDNRB", "FSHR",
    "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1",
    "LSHR", "LT4R1", "MCHR1", "NPY1R", "NPY2R",
    "OPRK", "OPRX", "OPSD", "OX2R",
}
CLASS_A_SECONDARY = {"B1B1U5", "CNR1", "OPRD"}
CLASS_B = {"GLP1R", "GCGR", "PTH1R", "CRHR1"}
CLASS_F = {"SMO", "FZD4", "FZD6", "FZD7"}

NPXXY_OH_THRESHOLD = 9.082
GPCRDB_TM6_TILT_THRESHOLD = 14.932
# Class B TM6 kink angle threshold. Panel-derived on tier-1 Class B
# receptors (PREREG §2c-revised): active < 159.95° (kink present), less
# is more active. Kobayashi et al. Nature 2023 anchors this metric.
CLASS_B_KINK_THRESHOLD_DEG = 159.95

# A1 range check bounds (plan §6): far-outward TM6 or NPxxY at >25 Å
# indicates a distorted prediction. NPxxY-OH 15 Å bound would flag 442
# ordinary inactive rows (95th percentile is 15.5 Å); use 25 Å for both
# axes.
A1_D_TM6_MAX_A = 25.0
A1_NPXXY_OH_MAX_A = 25.0

BACKBONES = ("boltz", "chai", "of3", "protenix")


def _f(x) -> float:
    if x in (None, "", "nan", "NaN", "None"):
        return math.nan
    try:
        v = float(x)
    except (TypeError, ValueError):
        return math.nan
    return v


def _infer_arm(row: dict) -> str:
    sc = (row.get("state_claim") or row.get("input_state_claim") or "").strip()
    if sc == "apo":
        return "apo"
    if sc.startswith("Ga-coupled"):
        return "cognate"
    p = (row.get("input_path") or row.get("prediction_path") or "").lower()
    if "_apo_" in p:
        return "apo"
    if "_cognate_" in p:
        return "cognate"
    return "?"


def _infer_backbone(row: dict) -> str:
    bb = (row.get("backbone") or "").strip().lower()
    if bb == "openfold3":
        return "of3"
    if bb in BACKBONES:
        return bb
    p = (row.get("input_path") or row.get("prediction_path") or "").lower()
    for cand, out in [("boltz", "boltz"), ("of3", "of3"), ("openfold3", "of3"),
                      ("protenix", "protenix"), ("chai", "chai")]:
        if f"/{cand}/" in p:
            return out
    return "unknown"


def _class_of(rec: str) -> str:
    r = rec.upper()
    if r in CLASS_A_PRIMARY or r in CLASS_A_SECONDARY:
        return "A"
    if r in CLASS_B:
        return "B"
    if r in CLASS_F:
        return "F"
    return "?"


def _median(xs):
    xs = [x for x in xs if not math.isnan(x)]
    return statistics.median(xs) if xs else math.nan


def _fmt(x, digits=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{digits}f}"


def read_rows(rows_csv: Path) -> list[dict]:
    with rows_csv.open() as f:
        return list(csv.DictReader(f))


# =====================================================================
# 1. Coverage
# =====================================================================

def coverage_table(rows: list[dict], out_csv: Path) -> None:
    by = defaultdict(lambda: {"n": 0, "n_pass": 0, "n_nan_d_tm6": 0,
                              "n_nan_npxxy": 0, "n_nan_gpcrdb_tilt": 0})
    for r in rows:
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        rec = (r.get("receptor_slug") or "").upper()
        cls = _class_of(rec)
        key = (arm, bb, cls)
        v = by[key]
        v["n"] += 1
        if (r.get("passed") or "").strip().lower() == "true":
            v["n_pass"] += 1
        if math.isnan(_f(r.get("d_tm6_r350_r630_ca"))):
            v["n_nan_d_tm6"] += 1
        if math.isnan(_f(r.get("d_npxxy_y558_y753_oh"))):
            v["n_nan_npxxy"] += 1
        if math.isnan(_f(r.get("d_gpcrdb_tm6_tilt_246_637_ca"))):
            v["n_nan_gpcrdb_tilt"] += 1
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["arm", "backbone", "class", "n", "n_pass", "pass_rate",
                    "n_nan_d_tm6", "n_nan_npxxy_oh", "n_nan_gpcrdb_tm6_tilt"])
        for (arm, bb, cls), v in sorted(by.items()):
            pr = v["n_pass"] / v["n"] if v["n"] else 0.0
            w.writerow([arm, bb, cls, v["n"], v["n_pass"], f"{pr:.3f}",
                        v["n_nan_d_tm6"], v["n_nan_npxxy"], v["n_nan_gpcrdb_tilt"]])


# =====================================================================
# 2. Primary result — Δd_tm6 median(cognate) − median(apo)
# =====================================================================

def primary_result(rows: list[dict], out_csv: Path) -> dict:
    # per (receptor, backbone) collect d_tm6 by arm
    by_receptor = defaultdict(lambda: defaultdict(list))
    receptor_class: dict[str, str] = {}
    for r in rows:
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        rec = (r.get("receptor_slug") or "").upper()
        if bb not in BACKBONES or arm not in ("cognate", "apo") or not rec:
            continue
        d = _f(r.get("d_tm6_r350_r630_ca"))
        by_receptor[(rec, bb)][arm].append(d)
        receptor_class[rec] = _class_of(rec)

    # per-receptor rows
    per_receptor_rows = []
    for (rec, bb), by_arm in sorted(by_receptor.items()):
        cog = [x for x in by_arm.get("cognate", []) if not math.isnan(x)]
        apo = [x for x in by_arm.get("apo", []) if not math.isnan(x)]
        m_cog = _median(cog)
        m_apo = _median(apo)
        delta = m_cog - m_apo if (cog and apo) else math.nan
        per_receptor_rows.append({
            "receptor_slug": rec,
            "receptor_class": receptor_class[rec],
            "backbone": bb,
            "n_cognate_valid": len(cog),
            "n_apo_valid": len(apo),
            "median_d_tm6_cognate": _fmt(m_cog),
            "median_d_tm6_apo": _fmt(m_apo),
            "delta_d_tm6": _fmt(delta),
        })

    # per (class × backbone) summary — median of per-receptor deltas
    by_cls_bb = defaultdict(list)
    for row in per_receptor_rows:
        d = row["delta_d_tm6"]
        if d == "":
            continue
        by_cls_bb[(row["receptor_class"], row["backbone"])].append(float(d))

    class_summary = []
    for (cls, bb) in sorted(by_cls_bb.keys()):
        deltas = by_cls_bb[(cls, bb)]
        n_active_dir = sum(1 for d in deltas if d > 0)  # cognate more outward than apo
        class_summary.append({
            "receptor_class": cls,
            "backbone": bb,
            "n_receptors_with_delta": len(deltas),
            "median_delta_d_tm6": _fmt(_median(deltas)),
            "mean_delta_d_tm6": _fmt(statistics.mean(deltas) if deltas else math.nan),
            "std_delta_d_tm6": _fmt(statistics.stdev(deltas) if len(deltas) > 1 else math.nan),
            "n_positive_delta": n_active_dir,
        })

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# Block A primary result — Δd_tm6 (median cognate − median apo)"])
        w.writerow(["# Axis: d_tm6_r350_r630_ca; predicate: median over 5 seeds × 5 samples"])
        w.writerow([])
        w.writerow(["## per_receptor_backbone"])
        w.writerow(["receptor_slug", "receptor_class", "backbone",
                    "n_cognate_valid", "n_apo_valid",
                    "median_d_tm6_cognate", "median_d_tm6_apo", "delta_d_tm6"])
        for r in per_receptor_rows:
            w.writerow([r[k] for k in ("receptor_slug", "receptor_class", "backbone",
                                       "n_cognate_valid", "n_apo_valid",
                                       "median_d_tm6_cognate", "median_d_tm6_apo",
                                       "delta_d_tm6")])
        w.writerow([])
        w.writerow(["## class_backbone_summary"])
        w.writerow(["receptor_class", "backbone", "n_receptors_with_delta",
                    "median_delta_d_tm6", "mean_delta_d_tm6", "std_delta_d_tm6",
                    "n_positive_delta"])
        for r in class_summary:
            w.writerow([r[k] for k in ("receptor_class", "backbone",
                                       "n_receptors_with_delta",
                                       "median_delta_d_tm6",
                                       "mean_delta_d_tm6",
                                       "std_delta_d_tm6",
                                       "n_positive_delta")])
    return {"per_receptor": per_receptor_rows, "class_summary": class_summary}


# =====================================================================
# 2b. Normalised-position table (d_tm6 axis)
#     Per-row normalised_pos = (d_tm6 − inactive_ref) / (active_ref − inactive_ref)
#     0 = inactive crystal, 1 = active crystal. Aggregate per (arm × backbone)
#     median across Class A. Also report fraction-between-references
#     (below inactive / between refs / above active).
# =====================================================================


def normalised_position_rmsd_table(rmsd_rows_csv: Path, out_csv: Path) -> dict:
    """Aggregate rmsd_pos per (arm × backbone) from a rescore_rmsd.py
    output CSV. Companion to normalised_position_table (d_tm6 axis) —
    if the two agree in direction and shape, the two-state result is
    confirmed on two independent axes (plan §5 Phase 4 gate).

    Reads the CSV produced by scripts/rescore_rmsd.py which appended
    rmsd_to_active_ref / rmsd_to_inactive_ref / rmsd_pos to the
    original rows.csv. Rows with empty rmsd_pos (skipped, no-ref-pair,
    load-failed) are dropped from the aggregation.
    """
    if not rmsd_rows_csv.exists():
        with out_csv.open("w", newline="") as f:
            csv.writer(f).writerow(["# input CSV missing — rescore_rmsd.py not yet run"])
        return {"skipped": True}

    per_row_pos: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in csv.DictReader(rmsd_rows_csv.open()):
        pos = _f(r.get("rmsd_pos"))
        if math.isnan(pos):
            continue
        rec = (r.get("receptor_slug") or "").upper()
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        cls = _class_of(rec)
        if cls not in ("A", "B", "F") or bb not in BACKBONES or arm not in ("apo", "cognate"):
            continue
        per_row_pos[(cls, arm, bb)].append(pos)

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# rmsd_pos aggregated — plan §5 Phase 4"])
        w.writerow(["# rmsd_pos = rmsd_to_inactive_ref / (rmsd_to_inactive_ref + rmsd_to_active_ref)"])
        w.writerow(["# 0 = at inactive crystal (rmsd_to_inactive small, rmsd_to_active large)"])
        w.writerow(["# 1 = at active crystal   (rmsd_to_active small, rmsd_to_inactive large)"])
        w.writerow(["# Same direction as normalised_position_d_tm6.csv (0 = inactive, 1 = active),"])
        w.writerow(["# but compressed toward 0.5 because backbone RMSD averages residues that do NOT"])
        w.writerow(["# move between the two states as well as those that do."])
        w.writerow(["# rmsd is a cross-class measure; independent of the anchor question."])
        w.writerow([])
        w.writerow(["## per_class_arm_backbone_summary"])
        w.writerow(["class", "arm", "backbone", "n_rows",
                    "median_rmsd_pos", "mean_rmsd_pos", "std_rmsd_pos"])
        for k in sorted(per_row_pos):
            vals = per_row_pos[k]
            w.writerow([
                k[0], k[1], k[2], len(vals),
                _fmt(statistics.median(vals)),
                _fmt(statistics.mean(vals)),
                _fmt(statistics.stdev(vals) if len(vals) > 1 else math.nan),
            ])
    return {
        "cells": {k: {"n": len(v),
                      "median": statistics.median(v),
                      "mean": statistics.mean(v)}
                  for k, v in per_row_pos.items()}
    }


def normalised_position_table(rows: list[dict], out_csv: Path) -> dict:
    """Compute normalised d_tm6 position per row and aggregate per
    (arm × backbone) across Class A. Two blocks land in ``out_csv``:

      1. Per (arm × backbone) median normalised position — the plan §5
         table (apo ≈ 0, cognate ≈ 0.94 on the delivered campaign).
      2. Per-cell fraction breakdown: below inactive (< 0), between
         (0 ≤ x ≤ 1), above active (> 1). The plan §5 headline was
         56/27/17 pooled across backbones on the cognate arm.
    """
    per_row_pos: dict[tuple[str, str], list[float]] = defaultdict(list)
    fractions: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"below_inactive": 0, "between": 0, "above_active": 0,
                 "n_valid": 0, "n_skipped": 0}
    )

    for r in rows:
        rec = (r.get("receptor_slug") or "").upper()
        cls = _class_of(rec)
        if cls != "A":
            continue
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        if bb not in BACKBONES or arm not in ("apo", "cognate"):
            continue
        d = _f(r.get("d_tm6_r350_r630_ca"))
        a_ref = _f(r.get("receptor_d_active_ref"))
        i_ref = _f(r.get("receptor_d_inactive_ref"))
        if any(math.isnan(x) for x in (d, a_ref, i_ref)):
            fractions[(arm, bb)]["n_skipped"] += 1
            continue
        span = a_ref - i_ref
        if abs(span) < 1e-6:
            fractions[(arm, bb)]["n_skipped"] += 1
            continue
        pos = (d - i_ref) / span
        per_row_pos[(arm, bb)].append(pos)
        fractions[(arm, bb)]["n_valid"] += 1
        if pos < 0:
            fractions[(arm, bb)]["below_inactive"] += 1
        elif pos > 1:
            fractions[(arm, bb)]["above_active"] += 1
        else:
            fractions[(arm, bb)]["between"] += 1

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# Class A normalised d_tm6 position — plan §5"])
        w.writerow(["# pos = (d_tm6 − receptor_d_inactive_ref) / (receptor_d_active_ref − receptor_d_inactive_ref)"])
        w.writerow(["# 0 = inactive crystal, 1 = active crystal"])
        w.writerow([])
        w.writerow(["## per_arm_backbone_median_and_iqr"])
        w.writerow(["arm", "backbone", "n_rows", "median_pos",
                    "mean_pos", "std_pos"])
        for (arm, bb) in sorted(per_row_pos.keys()):
            vals = per_row_pos[(arm, bb)]
            w.writerow([
                arm, bb, len(vals),
                _fmt(statistics.median(vals)),
                _fmt(statistics.mean(vals)),
                _fmt(statistics.stdev(vals) if len(vals) > 1 else math.nan),
            ])
        w.writerow([])
        w.writerow(["## per_arm_backbone_fraction_breakdown"])
        w.writerow(["arm", "backbone", "n_valid", "n_skipped",
                    "n_below_inactive", "n_between", "n_above_active",
                    "frac_below_inactive", "frac_between", "frac_above_active"])
        for (arm, bb) in sorted(fractions.keys()):
            v = fractions[(arm, bb)]
            n = v["n_valid"] or 1
            w.writerow([
                arm, bb, v["n_valid"], v["n_skipped"],
                v["below_inactive"], v["between"], v["above_active"],
                f"{v['below_inactive']/n:.3f}",
                f"{v['between']/n:.3f}",
                f"{v['above_active']/n:.3f}",
            ])

    return {
        "per_arm_backbone": {
            k: {"n": len(v),
                "median": statistics.median(v),
                "mean": statistics.mean(v)}
            for k, v in per_row_pos.items()
        },
        "fractions": dict(fractions),
    }


# =====================================================================
# 2c. A1 range check — plan §6
#     Flag rows where d_tm6 > 25 Å (22 ACM1/protenix/cognate rows in
#     Block A) or npxxy_oh > 25 Å (19 rows). Do NOT use 15 Å for
#     NPxxY-OH — that would flag 442 ordinary inactive rows.
# =====================================================================


def a1_range_check(rows: list[dict], out_csv: Path) -> dict:
    """Emit per-row A1 range flags + a per (receptor × arm × backbone)
    summary of how many rows exceeded the threshold.

    Two axes are checked:
      - d_tm6_r350_r630_ca > 25 Å
      - d_npxxy_y558_y753_oh > 25 Å
    """
    flagged_rows = []
    per_cell = defaultdict(lambda: {"n": 0, "n_flagged_d_tm6": 0,
                                    "n_flagged_npxxy_oh": 0, "n_any_flag": 0})
    for r in rows:
        rec = (r.get("receptor_slug") or "").upper()
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        d = _f(r.get("d_tm6_r350_r630_ca"))
        n_oh = _f(r.get("d_npxxy_y558_y753_oh"))
        flag_d = (not math.isnan(d)) and d > A1_D_TM6_MAX_A
        flag_n = (not math.isnan(n_oh)) and n_oh > A1_NPXXY_OH_MAX_A
        cell = (rec, arm, bb)
        per_cell[cell]["n"] += 1
        if flag_d:
            per_cell[cell]["n_flagged_d_tm6"] += 1
        if flag_n:
            per_cell[cell]["n_flagged_npxxy_oh"] += 1
        if flag_d or flag_n:
            per_cell[cell]["n_any_flag"] += 1
            flagged_rows.append({
                "receptor_slug": rec, "arm": arm, "backbone": bb,
                "d_tm6_r350_r630_ca": _fmt(d),
                "d_npxxy_y558_y753_oh": _fmt(n_oh),
                "input_path": r.get("input_path", ""),
                "flag_d_tm6": "true" if flag_d else "false",
                "flag_npxxy_oh": "true" if flag_n else "false",
            })

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([f"# A1 range check — plan §6"])
        w.writerow([f"# d_tm6 flag: d_tm6_r350_r630_ca > {A1_D_TM6_MAX_A} Å"])
        w.writerow([f"# NPxxY-OH flag: d_npxxy_y558_y753_oh > {A1_NPXXY_OH_MAX_A} Å"])
        w.writerow(["# 15 Å bound on NPxxY-OH was rejected — 95th "
                    "percentile is 15.5 Å, panel inactive-state mean is "
                    "12.88 Å."])
        w.writerow([])
        w.writerow(["## per_cell_summary"])
        w.writerow(["receptor_slug", "arm", "backbone", "n_rows",
                    "n_flagged_d_tm6", "n_flagged_npxxy_oh",
                    "n_any_flag"])
        for (rec, arm, bb), v in sorted(per_cell.items()):
            if v["n_any_flag"] == 0:
                continue
            w.writerow([rec, arm, bb, v["n"], v["n_flagged_d_tm6"],
                        v["n_flagged_npxxy_oh"], v["n_any_flag"]])
        w.writerow([])
        w.writerow(["## flagged_rows"])
        w.writerow(["receptor_slug", "arm", "backbone",
                    "d_tm6_r350_r630_ca", "d_npxxy_y558_y753_oh",
                    "flag_d_tm6", "flag_npxxy_oh", "input_path"])
        for r in flagged_rows:
            w.writerow([r[k] for k in ("receptor_slug", "arm", "backbone",
                                       "d_tm6_r350_r630_ca",
                                       "d_npxxy_y558_y753_oh",
                                       "flag_d_tm6", "flag_npxxy_oh",
                                       "input_path")])
    return {
        "n_flagged_total": len(flagged_rows),
        "n_flagged_d_tm6": sum(v["n_flagged_d_tm6"] for v in per_cell.values()),
        "n_flagged_npxxy_oh": sum(v["n_flagged_npxxy_oh"] for v in per_cell.values()),
    }


# =====================================================================
# 3. Two-instrument state calls (cognate rows only)
# =====================================================================

def two_instrument_state_calls(rows: list[dict], out_csv: Path) -> None:
    """Class-conditional active-call predicate (plan §4).

    - Class A: NPxxY-OH < 9.082 AND GPCRdb TM6 tilt > 14.932.
    - Class B: Class-B kink angle < 159.95° AND GPCRdb TM6 tilt > 14.932.
      (NPxxY doesn't exist in Class B1; the kink is Class B's real
      activation switch.)
    - Class F: GPCRdb TM6 tilt > 14.932 only. (NPxxY doesn't exist;
      the kink metric is Class-B-specific.)

    Rows are aggregated per (receptor, backbone) — median across the
    cognate arm's replicates — then evaluated against the class-conditional
    predicate.
    """
    by = defaultdict(lambda: {"npxxy": [], "tilt": [], "kink": [], "cls": ""})
    for r in rows:
        if _infer_arm(r) != "cognate":
            continue
        bb = _infer_backbone(r)
        rec = (r.get("receptor_slug") or "").upper()
        if bb not in BACKBONES or not rec:
            continue
        by[(rec, bb)]["npxxy"].append(_f(r.get("d_npxxy_y558_y753_oh")))
        by[(rec, bb)]["tilt"].append(_f(r.get("d_gpcrdb_tm6_tilt_246_637_ca")))
        by[(rec, bb)]["kink"].append(_f(r.get("angle_class_b_tm6_kink_639_650_654_deg")))
        by[(rec, bb)]["cls"] = _class_of(rec)

    # per (class, backbone) count active fraction
    per_cls_bb = defaultdict(lambda: {"n_receptors": 0, "n_active": 0,
                                      "n_missing_required": 0})
    per_receptor_rows = []
    for (rec, bb), v in sorted(by.items()):
        cls = v["cls"]
        m_n = _median(v["npxxy"])
        m_t = _median(v["tilt"])
        m_k = _median(v["kink"])

        # Class-conditional predicate. Returns (active, missing_reason) —
        # missing_reason is set when the required metrics for this class
        # aren't available and the call cannot be made.
        active = ""
        missing = ""
        if cls == "A":
            required_nan = math.isnan(m_n) or math.isnan(m_t)
            if required_nan:
                bits = []
                if math.isnan(m_n): bits.append("npxxy")
                if math.isnan(m_t): bits.append("tilt")
                missing = "nan_" + "_".join(bits)
                active = missing
            else:
                active = "yes" if (m_n < NPXXY_OH_THRESHOLD and m_t > GPCRDB_TM6_TILT_THRESHOLD) else "no"
        elif cls == "B":
            required_nan = math.isnan(m_k) or math.isnan(m_t)
            if required_nan:
                bits = []
                if math.isnan(m_k): bits.append("kink")
                if math.isnan(m_t): bits.append("tilt")
                missing = "nan_" + "_".join(bits)
                active = missing
            else:
                active = "yes" if (m_k < CLASS_B_KINK_THRESHOLD_DEG and m_t > GPCRDB_TM6_TILT_THRESHOLD) else "no"
        elif cls == "F":
            if math.isnan(m_t):
                missing = "nan_tilt"
                active = missing
            else:
                active = "yes" if m_t > GPCRDB_TM6_TILT_THRESHOLD else "no"
        else:
            active = f"cls_unhandled_{cls}"

        if missing:
            per_cls_bb[(cls, bb)]["n_missing_required"] += 1
        else:
            per_cls_bb[(cls, bb)]["n_receptors"] += 1
            if active == "yes":
                per_cls_bb[(cls, bb)]["n_active"] += 1
        per_receptor_rows.append({
            "receptor_slug": rec, "receptor_class": cls, "backbone": bb,
            "median_npxxy_oh": _fmt(m_n),
            "median_gpcrdb_tm6_tilt": _fmt(m_t),
            "median_class_b_kink": _fmt(m_k),
            "active_call": active,
        })

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([f"# Class-conditional two-instrument active-call predicate"])
        w.writerow([f"# Class A: npxxy_oh<{NPXXY_OH_THRESHOLD} AND gpcrdb_tm6_tilt>{GPCRDB_TM6_TILT_THRESHOLD}"])
        w.writerow([f"# Class B: class_b_kink<{CLASS_B_KINK_THRESHOLD_DEG} AND gpcrdb_tm6_tilt>{GPCRDB_TM6_TILT_THRESHOLD}"])
        w.writerow([f"# Class F: gpcrdb_tm6_tilt>{GPCRDB_TM6_TILT_THRESHOLD} only"])
        w.writerow(["# Cognate arm only; per-receptor call from median over 5 seeds × 5 samples."])
        w.writerow([])
        w.writerow(["## per_receptor_backbone"])
        w.writerow(["receptor_slug", "receptor_class", "backbone",
                    "median_npxxy_oh", "median_gpcrdb_tm6_tilt",
                    "median_class_b_kink", "active_call"])
        for r in per_receptor_rows:
            w.writerow([r[k] for k in ("receptor_slug", "receptor_class", "backbone",
                                       "median_npxxy_oh", "median_gpcrdb_tm6_tilt",
                                       "median_class_b_kink", "active_call")])
        w.writerow([])
        w.writerow(["## class_backbone_summary"])
        w.writerow(["receptor_class", "backbone", "n_receptors_scored",
                    "n_active", "fraction_active", "n_missing_required"])
        for (cls, bb), v in sorted(per_cls_bb.items()):
            frac = v["n_active"] / v["n_receptors"] if v["n_receptors"] else 0.0
            w.writerow([cls, bb, v["n_receptors"], v["n_active"], f"{frac:.3f}",
                        v["n_missing_required"]])


# =====================================================================
# 4. OF3 retry histogram
# =====================================================================

def of3_retry_histogram(scratch_root: Path, slug: str, out_csv: Path) -> dict:
    """Walk every _of3_colabfold_http_summary.json under
    <scratch_root>/<slug>/<cell>/ and bucket retry counts.
    """
    root = scratch_root / slug
    counts = Counter()
    n_seen = 0
    total_retries = 0
    if root.exists():
        for sidecar in root.rglob("*_of3_colabfold_http_summary.json"):
            try:
                data = json.loads(sidecar.read_text())
            except Exception:
                continue
            # Search common keys — OF3 shim writes 'colabfold_retries'
            r = data.get("colabfold_retries")
            if r is None:
                r = data.get("retries")
            if r is None:
                r = data.get("n_retries")
            if r is None:
                r = data.get("total_retries", 0)
            try:
                r = int(r)
            except (TypeError, ValueError):
                r = 0
            counts[r] += 1
            n_seen += 1
            total_retries += r
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["retry_count", "n_predictions"])
        for k in sorted(counts.keys()):
            w.writerow([k, counts[k]])
    return {"n_sidecars": n_seen, "total_retries": total_retries,
            "buckets": dict(counts)}


# =====================================================================
# main
# =====================================================================

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default="018_block_a_switch_test")
    p.add_argument("--experiments-root", type=Path, default=REPO / "experiments")
    p.add_argument("--scratch-root", type=Path,
                   default=Path("/hpc/scratch/sengaad1/paper_af3/experiments"))
    args = p.parse_args(argv)

    exp_dir = args.experiments_root / args.slug
    rows_csv = exp_dir / "analysis" / "rows.csv"
    if not rows_csv.exists():
        rows_csv = exp_dir / "rows.csv"
    if not rows_csv.exists():
        raise SystemExit(f"missing rows.csv under {exp_dir}")

    out_dir = exp_dir / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = read_rows(rows_csv)
    print(f"loaded {len(rows)} rows from {rows_csv}")

    coverage_table(rows, out_dir / "coverage.csv")
    print(f"wrote {out_dir / 'coverage.csv'}")

    primary_result(rows, out_dir / "primary_result_delta_d_tm6.csv")
    print(f"wrote {out_dir / 'primary_result_delta_d_tm6.csv'}")

    npos = normalised_position_table(
        rows, out_dir / "normalised_position_d_tm6.csv"
    )
    print(f"wrote {out_dir / 'normalised_position_d_tm6.csv'} — "
          f"{len(npos['per_arm_backbone'])} (arm×backbone) cells")

    # Phase 4 companion: rmsd_pos on the RMSD-rescored CSV. Skipped
    # gracefully if the RMSD rescore hasn't landed yet. Prefer the
    # combined file (all classes merged) over the class-A-only.
    for csv_name in ("rows.rmsd.csv", "rows.rmsd.class_A.csv"):
        rmsd_csv = out_dir / csv_name
        if rmsd_csv.exists():
            rmsd_npos = normalised_position_rmsd_table(
                rmsd_csv, out_dir / "normalised_position_rmsd.csv"
            )
            print(f"wrote {out_dir / 'normalised_position_rmsd.csv'} "
                  f"(source={csv_name})")
            break

    two_instrument_state_calls(rows, out_dir / "two_instrument_state_calls.csv")
    print(f"wrote {out_dir / 'two_instrument_state_calls.csv'}")

    a1_summary = a1_range_check(rows, out_dir / "a1_range_check.csv")
    print(f"wrote {out_dir / 'a1_range_check.csv'} — "
          f"n_flagged_total={a1_summary['n_flagged_total']}, "
          f"n_flagged_d_tm6={a1_summary['n_flagged_d_tm6']}, "
          f"n_flagged_npxxy_oh={a1_summary['n_flagged_npxxy_oh']}")

    of3_summary = of3_retry_histogram(
        args.scratch_root, args.slug, out_dir / "of3_retry_histogram.csv"
    )
    print(f"wrote {out_dir / 'of3_retry_histogram.csv'} — "
          f"{of3_summary['n_sidecars']} sidecars, {of3_summary['total_retries']} retries total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
