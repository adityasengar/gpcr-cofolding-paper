#!/usr/bin/env python3
"""Per-class threshold derivation — plan §16.

Class A tilt / NPxxY-OH thresholds were derived from the 32-receptor
Class A panel by midpoint(active_mean, inactive_mean). The current
predicate re-uses those thresholds for Class B and Class F, which is
saturation (Class B median tilt in apo = 22.05 A, well above 14.932 A;
Class F predicate is tilt-only so it is nearly always true).

This script derives Class B tilt / kink thresholds from the 4 Class B
reference pairs, and Class F tilt threshold from the 4 Class F reference
pairs, using the same midpoint rule. Reports self-classification
accuracy on the derivation set.

If self-classification accuracy is < 3/4 (Class B) or < 3/4 (Class F)
for a metric, the metric is reported descriptively rather than as a
usable threshold — n=4 is genuinely too small to derive a defensible
threshold and reporting saturated 4/4/4/4 numbers dressed as unanimous
is the anti-pattern §16 exists to prevent.

Usage:

    python3 scripts/derive_per_class_thresholds.py \\
        --reference-set refs/reference_set.csv \\
        --out-csv refs/thresholds_per_class.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


def _f(x: str | None) -> float:
    if x is None or x in ("", "nan", "NaN", "None"):
        return math.nan
    try:
        return float(x)
    except ValueError:
        return math.nan


# Class assignments (matches scorer/receptors.py RECEPTOR_CLASS)
CLASS_B_SLUGS = {"GLP1R", "GCGR", "PTH1R", "CRHR1"}
CLASS_F_SLUGS = {"SMO", "FZD4", "FZD6", "FZD7"}


def _midpoint(actives: list[float], inactives: list[float]) -> tuple[float, float, float, int, int]:
    """Return (threshold, mean_active, mean_inactive, n_active, n_inactive).

    threshold = mean(mean_active, mean_inactive). NaN in either
    aggregate returns NaN threshold.
    """
    a_ok = [x for x in actives if not math.isnan(x)]
    i_ok = [x for x in inactives if not math.isnan(x)]
    if not a_ok or not i_ok:
        return math.nan, math.nan, math.nan, len(a_ok), len(i_ok)
    mu_a = sum(a_ok) / len(a_ok)
    mu_i = sum(i_ok) / len(i_ok)
    thr = (mu_a + mu_i) / 2.0
    return thr, mu_a, mu_i, len(a_ok), len(i_ok)


def _self_classify_active_gt(actives: list[float], inactives: list[float],
                              thr: float) -> tuple[int, int]:
    """count(correct_active, correct_inactive) under `active > thr` rule."""
    a_ok = [x for x in actives if not math.isnan(x)]
    i_ok = [x for x in inactives if not math.isnan(x)]
    ca = sum(1 for x in a_ok if x > thr)
    ci = sum(1 for x in i_ok if x <= thr)
    return ca, ci


def _self_classify_active_lt(actives: list[float], inactives: list[float],
                              thr: float) -> tuple[int, int]:
    """count(correct_active, correct_inactive) under `active < thr` rule."""
    a_ok = [x for x in actives if not math.isnan(x)]
    i_ok = [x for x in inactives if not math.isnan(x)]
    ca = sum(1 for x in a_ok if x < thr)
    ci = sum(1 for x in i_ok if x >= thr)
    return ca, ci


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-set", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    args = ap.parse_args(argv)

    if not args.reference_set.exists():
        print(f"missing {args.reference_set}", file=sys.stderr)
        return 2

    # Load reference rows grouped per receptor per role
    per_receptor: dict[str, dict[str, list[dict[str, float]]]] = defaultdict(
        lambda: {"active": [], "inactive": []}
    )
    with args.reference_set.open() as f:
        for row in csv.DictReader(f):
            slug = (row.get("receptor_slug") or "").strip().upper()
            role = (row.get("role") or "").strip().lower()
            if not slug or role not in ("active", "inactive"):
                continue
            per_receptor[slug][role].append({
                "tilt": _f(row.get("d_gpcrdb_tm6_tilt_ref")),
                "kink": _f(row.get("angle_class_b_kink_ref")),
                "npxxy_oh": _f(row.get("d_npxxy_oh_ref")),
            })

    def _class_vals(slugs: set[str], role: str, field: str) -> list[float]:
        """Take the mean of PDBs per receptor per role, then return list
        of per-receptor means. Prevents a receptor with 2 PDBs from
        double-weighting the aggregate."""
        out = []
        for s in slugs:
            xs = [row[field] for row in per_receptor.get(s, {}).get(role, [])
                  if not math.isnan(row[field])]
            if xs:
                out.append(sum(xs) / len(xs))
        return out

    # ---- Class B: tilt + kink ---------------------------------------------
    B_tilt_a = _class_vals(CLASS_B_SLUGS, "active", "tilt")
    B_tilt_i = _class_vals(CLASS_B_SLUGS, "inactive", "tilt")
    B_tilt_thr, B_tilt_mu_a, B_tilt_mu_i, nBa, nBi = _midpoint(B_tilt_a, B_tilt_i)
    # tilt: expected active > threshold (higher tilt in active-like)
    B_tilt_ca, B_tilt_ci = _self_classify_active_gt(B_tilt_a, B_tilt_i, B_tilt_thr) \
        if not math.isnan(B_tilt_thr) else (0, 0)

    B_kink_a = _class_vals(CLASS_B_SLUGS, "active", "kink")
    B_kink_i = _class_vals(CLASS_B_SLUGS, "inactive", "kink")
    B_kink_thr, B_kink_mu_a, B_kink_mu_i, nBka, nBki = _midpoint(B_kink_a, B_kink_i)
    # kink angle: smaller angle in active (bent TM6). Use active < threshold.
    B_kink_ca, B_kink_ci = _self_classify_active_lt(B_kink_a, B_kink_i, B_kink_thr) \
        if not math.isnan(B_kink_thr) else (0, 0)

    # ---- Class F: tilt only ----------------------------------------------
    F_tilt_a = _class_vals(CLASS_F_SLUGS, "active", "tilt")
    F_tilt_i = _class_vals(CLASS_F_SLUGS, "inactive", "tilt")
    F_tilt_thr, F_tilt_mu_a, F_tilt_mu_i, nFa, nFi = _midpoint(F_tilt_a, F_tilt_i)
    F_tilt_ca, F_tilt_ci = _self_classify_active_gt(F_tilt_a, F_tilt_i, F_tilt_thr) \
        if not math.isnan(F_tilt_thr) else (0, 0)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "class", "metric", "rule", "threshold",
            "mean_active", "mean_inactive", "span",
            "n_active", "n_inactive",
            "correct_active", "correct_inactive", "self_acc",
            "usable",
        ])

        def _emit(cls: str, metric: str, rule: str, thr: float,
                  mu_a: float, mu_i: float, na: int, ni: int,
                  ca: int, ci: int):
            n = na + ni
            acc = (ca + ci) / n if n else math.nan
            # Plan §16: at n=4 per side the derivation set is fundamentally
            # too small to make a saturating self-acc meaningful. Only
            # mark usable=yes when the derivation set is large enough
            # (n>=5 per side) that a self-classification result carries
            # some information. Otherwise flag descriptive — the
            # caller must report the numbers as descriptive rather than
            # as a validated threshold to avoid the "4/4/4/4 unanimous"
            # anti-pattern.
            if na >= 5 and ni >= 5 and ca == na and ci == ni:
                usable = "yes"
            elif na < 5 or ni < 5:
                usable = "descriptive_n_lt_5_per_side"
            else:
                usable = "no_perfect_self_classification"
            w.writerow([
                cls, metric, rule,
                f"{thr:.4f}" if not math.isnan(thr) else "",
                f"{mu_a:.4f}" if not math.isnan(mu_a) else "",
                f"{mu_i:.4f}" if not math.isnan(mu_i) else "",
                f"{abs(mu_a - mu_i):.4f}"
                if not math.isnan(mu_a) and not math.isnan(mu_i) else "",
                na, ni, ca, ci,
                f"{acc:.3f}" if not math.isnan(acc) else "",
                usable,
            ])

        _emit("B", "d_gpcrdb_tm6_tilt", "active_gt", B_tilt_thr,
              B_tilt_mu_a, B_tilt_mu_i, nBa, nBi, B_tilt_ca, B_tilt_ci)
        _emit("B", "angle_class_b_kink", "active_lt", B_kink_thr,
              B_kink_mu_a, B_kink_mu_i, nBka, nBki, B_kink_ca, B_kink_ci)
        _emit("F", "d_gpcrdb_tm6_tilt", "active_gt", F_tilt_thr,
              F_tilt_mu_a, F_tilt_mu_i, nFa, nFi, F_tilt_ca, F_tilt_ci)

    print(f"wrote {args.out_csv}")
    print()
    print("Per-class thresholds (plan §16):")
    print(f"  Class B tilt   thr={B_tilt_thr:.3f} A   span={abs(B_tilt_mu_a - B_tilt_mu_i):.2f} A   self-acc={B_tilt_ca + B_tilt_ci}/{nBa + nBi}")
    print(f"  Class B kink   thr={B_kink_thr:.3f} deg span={abs(B_kink_mu_a - B_kink_mu_i):.2f} deg self-acc={B_kink_ca + B_kink_ci}/{nBka + nBki}")
    print(f"  Class F tilt   thr={F_tilt_thr:.3f} A   span={abs(F_tilt_mu_a - F_tilt_mu_i):.2f} A   self-acc={F_tilt_ca + F_tilt_ci}/{nFa + nFi}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
