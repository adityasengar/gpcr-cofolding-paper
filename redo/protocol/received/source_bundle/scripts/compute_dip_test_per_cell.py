#!/usr/bin/env python3
"""Compute Hartigan dip test on d_tm6 per (receptor × arm × backbone) cell.

Emits three new columns joinable back to rows.csv or renderable as a
standalone per-cell table:

    dip_p         — Hartigan dip test p-value (two-sided)
    frac_active   — fraction of samples on the active side of the receptor
                     midpoint (0..1), NaN if midpoint or values are NaN
    std_d_tm6     — sample stdev of d_tm6_r350_r630_ca

Rationale (plan §19). The "12 bimodal cells" open item in the campaign
report was inflated by OF3 pre-fix (five-structures-replicated-five-times
read as five modes; post-fix uniform 4.3% across backbones). Real signal
is the 8 significant-dip cells surfaced in the plan — mostly apo (APJ,
OPSD, CNR1, CCR5 producing both states without a partner).

These columns are STANDING per-cell — every (receptor × arm × backbone)
cell in the primary result carries them from now on.

Usage:

    python3 scripts/compute_dip_test_per_cell.py \\
        --rows-csv experiments/018_block_a_switch_test/analysis/rows.csv \\
        --out-csv experiments/018_block_a_switch_test/analysis/dip_test_per_cell.csv \\
        [--dip-alpha 0.05]
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


BACKBONE_HINTS: tuple[tuple[str, str], ...] = (
    ("_boltz", "boltz"),
    ("_chai", "chai"),
    ("_of3", "of3"),
    ("_protenix", "protenix"),
    ("_af2mm", "af2mm"),
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


def _stdev(vals: list[float]) -> float:
    xs = [v for v in vals if not math.isnan(v)]
    if len(xs) < 2:
        return math.nan
    mu = sum(xs) / len(xs)
    var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def _dip_p(vals: list[float]) -> float:
    """Hartigan dip test p-value via `diptest` package. Returns NaN if
    the package is unavailable or the sample is degenerate."""
    xs = [v for v in vals if not math.isnan(v)]
    if len(xs) < 4:
        return math.nan
    try:
        import diptest
        import numpy as np
    except ImportError:
        return math.nan
    try:
        _, pv = diptest.diptest(np.asarray(xs, dtype=float))
        return float(pv)
    except Exception as exc:
        print(f"  dip failed: {exc}", file=sys.stderr)
        return math.nan


def _frac_active(d_tm6: list[float], midpoints: list[float],
                 actives: list[float]) -> float:
    """Fraction of samples on the active side of each row's midpoint.
    Class A / F (d_tm6-anchored): active-side means d_tm6 > midpoint
    when active_ref > inactive_ref (typical), or d_tm6 < midpoint when
    inverted. Class B rows will show NaN receptor_midpoint under the
    §15 tilt flip if `receptor_midpoint` was derived on the tilt axis
    while d_tm6 is passed here — the caller is expected to compute
    per-axis frac_active where relevant. For a per-cell number using
    d_tm6 (the primary axis for A / F, and reported-secondary for B),
    this returns NaN when either quantity is NaN.
    """
    n_on_active = 0
    n_used = 0
    for d, m, a in zip(d_tm6, midpoints, actives):
        if math.isnan(d) or math.isnan(m) or math.isnan(a):
            continue
        n_used += 1
        # active side = same side as receptor's active ref relative to midpoint
        if (a - m) * (d - m) > 0:
            n_on_active += 1
    if n_used == 0:
        return math.nan
    return n_on_active / n_used


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rows-csv", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--dip-alpha", type=float, default=0.05,
                    help="p-value cutoff for the significant-dip summary")
    args = ap.parse_args(argv)

    if not args.rows_csv.exists():
        print(f"missing {args.rows_csv}", file=sys.stderr)
        return 2

    # Bucket by (receptor_slug, arm, backbone)
    buckets: dict[tuple[str, str, str], dict[str, list[float]]] = defaultdict(
        lambda: {"d_tm6": [], "midpoint": [], "active_ref": []}
    )
    cell_class: dict[tuple[str, str, str], str] = {}

    with args.rows_csv.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = (row.get("receptor_slug") or "").strip().upper()
            arm = (row.get("input_state_claim") or "").strip()
            bb = _infer_backbone(row.get("input_path") or "")
            if not slug:
                continue
            key = (slug, arm, bb)
            buckets[key]["d_tm6"].append(_f(row.get("d_tm6_r350_r630_ca")))
            buckets[key]["midpoint"].append(_f(row.get("receptor_midpoint")))
            buckets[key]["active_ref"].append(_f(row.get("receptor_d_active_ref")))
            cell_class[key] = (row.get("receptor_class") or "").strip()

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    n_dip_sig = 0
    dip_sig_rows: list[tuple] = []
    with args.out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "receptor_slug", "receptor_class", "arm", "backbone",
            "n", "dip_p", "frac_active", "std_d_tm6", "mean_d_tm6",
        ])
        for key in sorted(buckets):
            slug, arm, bb = key
            b = buckets[key]
            vals = b["d_tm6"]
            xs = [v for v in vals if not math.isnan(v)]
            n = len(xs)
            dip = _dip_p(vals)
            fa = _frac_active(b["d_tm6"], b["midpoint"], b["active_ref"])
            sd = _stdev(vals)
            mu = (sum(xs) / n) if n else math.nan
            w.writerow([
                slug, cell_class.get(key, ""), arm, bb,
                n,
                f"{dip:.6f}" if not math.isnan(dip) else "",
                f"{fa:.4f}" if not math.isnan(fa) else "",
                f"{sd:.4f}" if not math.isnan(sd) else "",
                f"{mu:.4f}" if not math.isnan(mu) else "",
            ])
            if not math.isnan(dip) and dip < args.dip_alpha:
                n_dip_sig += 1
                dip_sig_rows.append((slug, arm, bb, dip, fa, sd, n))

    print(f"wrote {args.out_csv}")
    print(f"significant-dip cells (p<{args.dip_alpha}): {n_dip_sig}")
    for r in sorted(dip_sig_rows, key=lambda x: x[3]):
        slug, arm, bb, dip, fa, sd, n = r
        fa_s = f"{fa:.2f}" if not math.isnan(fa) else "NaN"
        sd_s = f"{sd:.2f}" if not math.isnan(sd) else "NaN"
        print(f"  {slug:10s} {arm:22s} {bb:10s} n={n:2d} "
              f"dip_p={dip:.4f}  frac_active={fa_s}  std={sd_s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
