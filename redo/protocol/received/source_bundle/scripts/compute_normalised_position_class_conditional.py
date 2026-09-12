#!/usr/bin/env python3
"""Normalised position on the class-conditional axis — plan §15 companion.

For each receptor, arm, and backbone, computes:

    pos = (current - inactive_ref) / (active_ref - inactive_ref)

where `current` is the class-appropriate current-axis value from rows.csv
(after the §15 class-conditional resolver landed), and `inactive_ref` /
`active_ref` are the class-appropriate refs (also §15-resolved).

Because §15 resolves everything through the scorer, this script does NOT
need to know per-class axis conventions itself — it reads receptor_
d_active_ref, receptor_d_inactive_ref, and (for Class A/F) d_tm6, or
(for Class B) d_gpcrdb_tm6_tilt_246_637_ca. The class dispatch is one
if-statement.

Emits `normalised_position_class_conditional.csv` — one row per
(receptor, arm, backbone) with mean + std normalised position, and a
header note about Class B axis flip.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


BACKBONE_HINTS = (("_boltz", "boltz"), ("_chai", "chai"),
                  ("_of3", "of3"), ("_protenix", "protenix"))


def _infer_backbone(path: str) -> str:
    p = path.lower()
    for pat, name in BACKBONE_HINTS:
        if pat in p:
            return name
    return "unknown"


def _f(x: str | None) -> float:
    if x is None or x in ("", "nan", "NaN", "None"):
        return math.nan
    try:
        return float(x)
    except ValueError:
        return math.nan


def _current(row: dict) -> float:
    cls = (row.get("receptor_class") or "").strip()
    if cls == "B":
        return _f(row.get("d_gpcrdb_tm6_tilt_246_637_ca"))
    # A / F on d_tm6
    return _f(row.get("d_tm6_r350_r630_ca"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows-csv", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    args = ap.parse_args()

    buckets: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)

    with args.rows_csv.open() as f:
        for row in csv.DictReader(f):
            slug = (row.get("receptor_slug") or "").strip().upper()
            cls = (row.get("receptor_class") or "").strip()
            arm_claim = (row.get("input_state_claim") or "").strip()
            if arm_claim.startswith("Ga-coupled"):
                arm = "cognate"
            elif arm_claim == "apo":
                arm = "apo"
            else:
                continue
            bb = _infer_backbone(row.get("input_path") or "")
            if bb == "unknown" or not slug or not cls:
                continue
            act = _f(row.get("receptor_d_active_ref"))
            ina = _f(row.get("receptor_d_inactive_ref"))
            cur = _current(row)
            if any(math.isnan(x) for x in (cur, act, ina)):
                continue
            denom = act - ina
            if abs(denom) < 1e-9:
                continue
            pos = (cur - ina) / denom
            buckets[(cls, slug, arm, bb)].append(pos)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# Normalised position on the class-conditional axis (plan §15)"])
        w.writerow(["# Class A: (d_tm6 - d_tm6_inactive_ref) / (d_tm6_active_ref - d_tm6_inactive_ref)"])
        w.writerow(["# Class B: (d_tilt - d_tilt_inactive_ref) / (d_tilt_active_ref - d_tilt_inactive_ref)"])
        w.writerow(["# Class F: (d_tm6 - d_tm6_inactive_ref) / (d_tm6_active_ref - d_tm6_inactive_ref) — reported-secondary"])
        w.writerow(["# COMPARABILITY NOTE: Class B pre-§15 numbers were on d_tm6-anchor (broken span). "
                    "Post-§15 uses tilt-anchor (10.4 A span). These are on different axes and not comparable."])
        w.writerow([])
        w.writerow(["receptor_class", "receptor_slug", "arm", "backbone",
                    "n", "mean_pos", "median_pos", "std_pos"])
        for key in sorted(buckets):
            cls, slug, arm, bb = key
            vals = buckets[key]
            if not vals:
                continue
            mean = statistics.fmean(vals)
            med = statistics.median(vals)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            w.writerow([cls, slug, arm, bb, len(vals),
                        f"{mean:.4f}", f"{med:.4f}", f"{sd:.4f}"])

    # Summary aggregates for the campaign report
    per_arm_bb_cls: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for (cls, slug, arm, bb), vals in buckets.items():
        if vals:
            per_arm_bb_cls[(cls, arm, bb)].append(statistics.fmean(vals))

    print(f"wrote {args.out_csv}")
    print()
    print("Median across-receptor normalised position (class × arm × backbone):")
    print("class arm      boltz    chai     of3      protenix")
    for cls in ("A", "B", "F"):
        for arm in ("apo", "cognate"):
            row = f"{cls}     {arm:8s} "
            for bb in ("boltz", "chai", "of3", "protenix"):
                xs = per_arm_bb_cls.get((cls, arm, bb), [])
                if xs:
                    row += f"{statistics.median(xs):>+.3f}(n={len(xs):2d}) "
                else:
                    row += "  -         "
            print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
