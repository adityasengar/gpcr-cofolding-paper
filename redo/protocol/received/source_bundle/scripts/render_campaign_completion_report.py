"""Render experiments/018_block_a_switch_test/analysis/campaign_completion_report.md.

Aggregates:
  - per-backbone × per-arm pass rates from analysis/rows.csv,
  - OF3 retry distribution from every ``_of3_colabfold_http_summary.json``
    sidecar under scratch,
  - wall-time totals per backbone from ``_${bb}_status.json`` sidecars
    (or the worker log if the sidecar lacks a wall field),
  - sealed-subset row count (should be zero non-NaN delta_to_active).

Usage:
    python3 scripts/render_campaign_completion_report.py \
        --slug 018_block_a_switch_test \
        --scratch-root /hpc/scratch/sengaad1/paper_af3/experiments
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

SEALED_SLUGS = {"AA2AR", "ADRB2", "DRD2", "CCR5", "OPRK", "AGTR1", "GLP1R", "HRH1"}
# ^ Placeholder; refresh from refs/sealed_active_refs_2026_09_01.csv at run time.


def _f(x: str) -> float:
    try:
        return float(x)
    except (ValueError, TypeError):
        return math.nan


def _infer_arm(row: dict) -> str:
    sc = (row.get("state_claim") or "").strip()
    if sc == "apo":
        return "apo"
    if sc.startswith("Ga-coupled"):
        return "cognate"
    p = (row.get("input_path") or row.get("prediction_path") or "").lower()
    return "apo" if "_apo_" in p else ("cognate" if "_cognate_" in p else "?")


def _infer_backbone(row: dict) -> str:
    bb = (row.get("backbone") or "").strip().lower()
    if bb == "openfold3":
        return "of3"
    if bb in ("boltz", "chai", "of3", "protenix"):
        return bb
    p = (row.get("input_path") or row.get("prediction_path") or "").lower()
    # Both /of3/ and /openfold3/ conventions live in the wild — the
    # frozen v3.7 corpus uses /of3/; scorer/rerun_dispatch materialises
    # /of3/ subdirs; only the raw model source uses /openfold3/. Prior
    # to 2026-09-02, only the `/openfold3/` alternate was matched here,
    # so every OF3 row silently fell through to `unknown` and the
    # per-backbone pass-rate table showed identical counts for three
    # backbones with an "unknown" row underneath.
    for cand, out in [("boltz", "boltz"),
                      ("of3", "of3"),
                      ("openfold3", "of3"),
                      ("protenix", "protenix"),
                      ("chai", "chai")]:
        if f"/{cand}/" in p:
            return out
    return "unknown"


def load_sealed_slugs() -> set[str]:
    p = REPO / "refs" / "sealed_active_refs_2026_09_01.csv"
    if not p.exists():
        return SEALED_SLUGS
    slugs: set[str] = set()
    with p.open() as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    for row in csv.DictReader(lines):
        if (row.get("role") or "").strip() == "active":
            slugs.add((row.get("receptor_slug") or "").strip().upper())
    return slugs


def pass_rates(rows: list[dict]) -> dict:
    by = defaultdict(lambda: {"n": 0, "n_pass": 0})
    for r in rows:
        bb = _infer_backbone(r)
        arm = _infer_arm(r)
        key = (bb, arm)
        by[key]["n"] += 1
        if (r.get("passed") or "").strip().lower() == "true":
            by[key]["n_pass"] += 1
    return dict(by)


def of3_retry_distribution(scratch_root: Path, slug: str) -> dict:
    """Walk every _of3_colabfold_http_summary.json under scratch_root/slug/."""
    retries = []
    root = scratch_root / slug
    if not root.exists():
        return {"n": 0}
    for p in root.rglob("_of3_colabfold_http_summary.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        n = d.get("retries")
        if isinstance(n, int):
            retries.append(n)
    if not retries:
        return {"n": 0}
    return {
        "n": len(retries),
        "median": statistics.median(retries),
        "max": max(retries),
        "fraction_gt_zero": sum(1 for x in retries if x > 0) / len(retries),
    }


def wall_time_by_backbone(rows: list[dict]) -> dict:
    """Best-effort wall time totals per backbone from wall_s_used column
    if present, else from _status.json sidecars. Empty until scorer emits it."""
    walls: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        bb = _infer_backbone(r)
        w = _f(r.get("wall_s_used") or "")
        if not math.isnan(w):
            walls[bb].append(w)
    return {bb: {"n": len(vs), "sum_s": sum(vs), "median_s": statistics.median(vs) if vs else 0}
            for bb, vs in walls.items()}


def sealed_subset_check(rows: list[dict], sealed: set[str]) -> dict:
    n_sealed_rows = 0
    n_nonempty_delta = 0
    for r in rows:
        rec = (r.get("receptor_slug") or "").strip().upper()
        if rec not in sealed:
            continue
        n_sealed_rows += 1
        delta = (r.get("delta_to_active_d_tm6") or r.get("delta_to_active") or "").strip()
        if delta and delta not in ("nan", "NaN", "None"):
            n_nonempty_delta += 1
    return {"n_sealed_rows": n_sealed_rows,
            "n_nonempty_delta_to_active": n_nonempty_delta}


def render(rows_csv: Path, out_md: Path, scratch_root: Path, slug: str) -> None:
    with rows_csv.open() as f:
        rows = list(csv.DictReader(f))

    pr = pass_rates(rows)
    of3 = of3_retry_distribution(scratch_root, slug)
    walls = wall_time_by_backbone(rows)
    sealed = sealed_subset_check(rows, load_sealed_slugs())

    lines = [
        f"# Block A campaign completion report ({slug})",
        "",
        f"Generated from `analysis/rows.csv` ({len(rows)} rows scored).",
        "",
        "## Per-backbone × per-arm pass rates",
        "",
        "| backbone | arm | n | n_pass | pass_rate |",
        "|---|---|---:|---:|---:|",
    ]
    for (bb, arm), v in sorted(pr.items()):
        pct = f"{100 * v['n_pass'] / v['n']:.1f}%" if v['n'] else "-"
        lines.append(f"| {bb} | {arm} | {v['n']} | {v['n_pass']} | {pct} |")

    lines += [
        "",
        "## OF3 ColabFold-shim retry distribution",
        "",
    ]
    if of3["n"] == 0:
        lines.append("_no OF3 sidecar summaries under scratch_")
    else:
        lines += [
            f"- **n** (predictions with sidecar): {of3['n']}",
            f"- **median retries**: {of3['median']}",
            f"- **max retries**: {of3['max']}",
            f"- **fraction with retries > 0**: {of3['fraction_gt_zero']:.3f}",
        ]

    lines += [
        "",
        "## Wall time per backbone",
        "",
        "| backbone | n | median_s | sum_s |",
        "|---|---:|---:|---:|",
    ]
    for bb, w in sorted(walls.items()):
        lines.append(f"| {bb} | {w['n']} | {w['median_s']:.1f} | {w['sum_s']:.0f} |")
    if not walls:
        lines.append("_wall_s_used column not populated in rows.csv_")

    lines += [
        "",
        "## Sealed-subset gate check",
        "",
        f"- Sealed active receptors: {len(load_sealed_slugs())}",
        f"- rows.csv rows for sealed receptors: **{sealed['n_sealed_rows']}**",
        f"- of those, rows with non-NaN delta_to_active: **{sealed['n_nonempty_delta_to_active']}**",
        "",
        ("- **PASS** — no `delta_to_active` values landed for any sealed row."
         if sealed["n_nonempty_delta_to_active"] == 0 else
         "- **FAIL** — `delta_to_active` leaked into a sealed row. Investigate."),
        "",
    ]

    out_md.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default="018_block_a_switch_test")
    p.add_argument("--scratch-root", type=Path,
                   default=Path("/hpc/scratch/sengaad1/paper_af3/experiments"))
    p.add_argument("--experiments-root", type=Path,
                   default=REPO / "experiments")
    args = p.parse_args(argv)

    exp_dir = args.experiments_root / args.slug
    rows_csv = exp_dir / "analysis" / "rows.csv"
    if not rows_csv.exists():
        rows_csv = exp_dir / "rows.csv"
    out_md = exp_dir / "analysis" / "campaign_completion_report.md"
    render(rows_csv, out_md, args.scratch_root, args.slug)
    print(f"wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
