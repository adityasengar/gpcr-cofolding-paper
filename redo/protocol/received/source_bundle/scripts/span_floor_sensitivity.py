#!/usr/bin/env python3
"""Reference span-floor sensitivity curve for the Class A headline.

Plan §17: instead of pre-registering a 3 A floor (which invites the
"threshold chosen after seeing exclusions" objection), compute the
Class A headline (mean normalised-position on d_tm6, cognate arm) at
several floors — 0, 2, 3, 4 A — and emit the sensitivity curve. Pick a
floor with reason stated, or find the headline flat and note that the
choice doesn't matter.

Normalised position (Class A, per receptor):
    pos = (d_tm6 - inactive_ref) / (active_ref - inactive_ref)
    span = |active_ref - inactive_ref|

At floor f, receptors with span < f drop out of the median.

OPRD is a separate pre-registered disqualification (agonist-only
active reference, no Ga) and is dropped in a separate pass — its
justification is pre-registered biology, not span sensitivity. The
script reports both "with OPRD" and "without OPRD" curves so the
two justifications can be kept apart in the writeup.

Usage:

    python3 scripts/span_floor_sensitivity.py \\
        --rows-csv experiments/018_block_a_switch_test/analysis/rows.csv \\
        --out-csv experiments/018_block_a_switch_test/analysis/span_floor_sensitivity.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


BACKBONE_HINTS = (
    ("_boltz", "boltz"),
    ("_chai", "chai"),
    ("_of3", "of3"),
    ("_protenix", "protenix"),
)


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


def _class_A_cognate_median_pos(
    rows: list[dict],
    span_floor: float,
    include_oprd: bool,
) -> dict[str, dict]:
    """Per-backbone Class A cognate arm median normalised position at a
    span floor. Returns {backbone: {median_pos, n_receptors_kept,
    receptors_dropped_by_floor}}.
    """
    # Group per (receptor, backbone) — take mean of samples per group
    per_recep: dict[tuple[str, str], list[float]] = defaultdict(list)
    receptor_span: dict[str, float] = {}
    for r in rows:
        if (r.get("receptor_class") or "").strip() != "A":
            continue
        if (r.get("input_state_claim") or "").strip() != "Ga-coupled-active":
            continue
        slug = (r.get("receptor_slug") or "").strip().upper()
        if not slug:
            continue
        if not include_oprd and slug == "OPRD":
            continue
        d = _f(r.get("d_tm6_r350_r630_ca"))
        act = _f(r.get("receptor_d_active_ref"))
        ina = _f(r.get("receptor_d_inactive_ref"))
        if any(math.isnan(x) for x in (d, act, ina)):
            continue
        span = abs(act - ina)
        if span < span_floor:
            continue
        receptor_span[slug] = span
        # pos = (d - inactive) / (active - inactive); 0=inactive, 1=active
        denom = (act - ina)
        if abs(denom) < 1e-9:
            continue
        pos = (d - ina) / denom
        bb = _infer_backbone(r.get("input_path") or "")
        per_recep[(slug, bb)].append(pos)

    by_bb: dict[str, list[float]] = defaultdict(list)
    kept_by_bb: dict[str, set[str]] = defaultdict(set)
    for (slug, bb), vals in per_recep.items():
        by_bb[bb].append(sum(vals) / len(vals))
        kept_by_bb[bb].add(slug)
    out: dict[str, dict] = {}
    for bb, vals in by_bb.items():
        out[bb] = {
            "median": statistics.median(vals),
            "mean": statistics.fmean(vals),
            "n_receptors": len(kept_by_bb[bb]),
        }
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows-csv", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--floors", nargs="+", type=float, default=[0.0, 2.0, 3.0, 4.0])
    args = ap.parse_args(argv)

    with args.rows_csv.open() as f:
        rows = list(csv.DictReader(f))

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    all_backbones = ("boltz", "chai", "of3", "protenix")
    with args.out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["span_floor_a", "oprd", "backbone",
                    "median_pos", "mean_pos", "n_receptors"])
        for floor in args.floors:
            for include_oprd in (True, False):
                per_bb = _class_A_cognate_median_pos(rows, floor, include_oprd)
                for bb in all_backbones:
                    if bb in per_bb:
                        d = per_bb[bb]
                        w.writerow([
                            f"{floor:.1f}",
                            "in" if include_oprd else "out",
                            bb,
                            f"{d['median']:.4f}",
                            f"{d['mean']:.4f}",
                            d["n_receptors"],
                        ])
                    else:
                        w.writerow([f"{floor:.1f}", "in" if include_oprd else "out",
                                    bb, "", "", 0])

    # Print curve to stdout for the writeup
    print(f"wrote {args.out_csv}")
    print()
    print("Class A cognate median normalised position (d_tm6 axis) by span floor:")
    print("floor  oprd    boltz    chai    of3      protenix")
    for floor in args.floors:
        for include_oprd in (True, False):
            per_bb = _class_A_cognate_median_pos(rows, floor, include_oprd)
            cells = []
            for bb in all_backbones:
                if bb in per_bb:
                    d = per_bb[bb]
                    cells.append(f"{d['median']:.3f}(n={d['n_receptors']:2d})")
                else:
                    cells.append("     -   ")
            tag = "in " if include_oprd else "out"
            print(f"{floor:>3.1f}A   {tag}   " + "  ".join(cells))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
