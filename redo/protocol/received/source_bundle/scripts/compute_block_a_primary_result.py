"""Compute the Block A primary result — Δd_tm6(cognate − apo) per receptor.

Input: ``experiments/018_block_a_switch_test/analysis/rows.csv``.
Output:
  - ``analysis/primary_result_delta_d_tm6.csv`` — one row per
    (receptor, backbone) with the mean Δd_tm6 and n (rows contributing)
    for both arms.
  - ``analysis/per_class/class_A_primary.csv`` — 37 Class A receptors
    (excluding JSR1/B1B1U5, CNR1, OPRD; those go to secondary).
  - ``analysis/per_class/class_A_secondary.csv`` — JSR1, CNR1, OPRD.
  - ``analysis/per_class/class_B_secretin.csv`` — 4 Class B receptors.
  - ``analysis/per_class/class_F_case_studies.csv`` — 4 Class F receptors
    (per-receptor rows; no pooled Class F number).

Usage (local, after rescore populates analysis/rows.csv):
    python3 scripts/compute_block_a_primary_result.py \
        --slug 018_block_a_switch_test
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CLASS_A_PRIMARY = [
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR",
    "ACM1", "ACM2", "ACM4", "ADA2A", "ADRB1",
    "ADRB2", "AGTR1", "APJ", "CCKAR",
    "CCR5", "CNR2", "CXCR2", "CXCR4",
    "DRD2", "DRD3", "EDNRA", "EDNRB", "FSHR",
    "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1",
    "LSHR", "LT4R1", "MCHR1", "NPY1R", "NPY2R",
    "OPRK", "OPRX", "OPSD", "OX2R",
]

CLASS_A_SECONDARY = ["B1B1U5", "CNR1", "OPRD"]
CLASS_B = ["GLP1R", "GCGR", "PTH1R", "CRHR1"]
CLASS_F = ["SMO", "FZD4", "FZD6", "FZD7"]


def _f(x: str) -> float:
    if x in ("", "nan", "NaN", "None", None):
        return math.nan
    try:
        return float(x)
    except (ValueError, TypeError):
        return math.nan


def _read_rows(rows_csv: Path) -> list[dict[str, str]]:
    with rows_csv.open() as f:
        return list(csv.DictReader(f))


def _infer_arm(row: dict[str, str]) -> str:
    """Cognate vs apo: prefer state_claim, fall back to prediction_path."""
    sc = (row.get("state_claim") or "").strip()
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


def _infer_backbone(row: dict[str, str]) -> str:
    bb = (row.get("backbone") or "").strip()
    if bb:
        return bb
    p = (row.get("input_path") or row.get("prediction_path") or "").lower()
    for cand in ("boltz", "openfold3", "of3", "protenix", "chai"):
        if f"/{cand}/" in p or p.endswith(f"/{cand}"):
            return "of3" if cand == "openfold3" else cand
    return "unknown"


def group_by_receptor_backbone_arm(rows: list[dict[str, str]]) -> dict:
    d = defaultdict(lambda: defaultdict(list))
    for r in rows:
        rec = (r.get("receptor_slug") or "").upper().strip()
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        # Actual column emitted by scorer/schema.py (post-2026-08 anchor rename)
        d_tm6 = _f(r.get("d_tm6_r350_r630_ca") or r.get("d_tm6_outward_r350_r558_ca") or r.get("d_tm6_outward_ca") or "")
        if not (rec and bb in {"boltz", "of3", "protenix", "chai"} and arm in {"cognate", "apo"}):
            continue
        d[(rec, bb)][arm].append(d_tm6)
    return d


def compute_primary(rows_csv: Path, out_csv: Path) -> int:
    rows = _read_rows(rows_csv)
    grouped = group_by_receptor_backbone_arm(rows)
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["receptor_slug", "backbone",
                    "n_cognate", "mean_d_tm6_cognate", "std_d_tm6_cognate",
                    "n_apo", "mean_d_tm6_apo", "std_d_tm6_apo",
                    "delta_d_tm6"])
        for (rec, bb), by_arm in sorted(grouped.items()):
            cog = [x for x in by_arm.get("cognate", []) if not math.isnan(x)]
            apo = [x for x in by_arm.get("apo", []) if not math.isnan(x)]
            mc = statistics.mean(cog) if cog else math.nan
            sc = statistics.stdev(cog) if len(cog) > 1 else 0.0
            ma = statistics.mean(apo) if apo else math.nan
            sa = statistics.stdev(apo) if len(apo) > 1 else 0.0
            delta = mc - ma if (cog and apo) else math.nan
            w.writerow([rec, bb, len(cog), f"{mc:.3f}", f"{sc:.3f}",
                        len(apo), f"{ma:.3f}", f"{sa:.3f}",
                        f"{delta:.3f}" if not math.isnan(delta) else ""])
    return len(grouped)


def _write_class_slice(primary_csv: Path, slice_out: Path, receptors: list[str]) -> None:
    with primary_csv.open() as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r["receptor_slug"] in receptors]
    with slice_out.open("w", newline="") as f:
        if not rows:
            slice_out.write_text("")
            return
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default="018_block_a_switch_test")
    p.add_argument("--experiments-root", type=Path,
                   default=REPO / "experiments")
    args = p.parse_args(argv)

    exp_dir = args.experiments_root / args.slug
    rows_csv = exp_dir / "analysis" / "rows.csv"
    if not rows_csv.exists():
        # fall back to grandfathered flat path
        rows_csv = exp_dir / "rows.csv"
    if not rows_csv.exists():
        print(f"missing rows.csv under {exp_dir}", file=__import__("sys").stderr)
        return 2

    primary_csv = exp_dir / "analysis" / "primary_result_delta_d_tm6.csv"
    per_class = exp_dir / "analysis" / "per_class"
    per_class.mkdir(parents=True, exist_ok=True)

    n = compute_primary(rows_csv, primary_csv)
    print(f"wrote {primary_csv}  ({n} (receptor, backbone) groups)")

    for name, receptors in [
        ("class_A_primary.csv", CLASS_A_PRIMARY),
        ("class_A_secondary.csv", CLASS_A_SECONDARY),
        ("class_B_secretin.csv", CLASS_B),
        ("class_F_case_studies.csv", CLASS_F),
    ]:
        slice_out = per_class / name
        _write_class_slice(primary_csv, slice_out, receptors)
        print(f"wrote {slice_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
