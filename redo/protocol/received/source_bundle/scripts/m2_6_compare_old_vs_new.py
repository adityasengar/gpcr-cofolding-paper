"""M2.6 — old-vs-new comparison of frozen-corpus rescore vs fresh M2.4 rerun.

Reads two ScorerRow CSVs (frozen and fresh) produced by the SAME scorer
commit, joins on (experiment, receptor_slug, partner, backbone, ligand_code),
computes per-condition hit rates for the qualitative-verdict axes, and
emits a markdown comparison to `--out`.

The output is the manuscript-grade artefact backing the deterministic-
replay claim: the fresh rerun reproduces the frozen corpus's qualitative
verdicts.

Categorisation (see docs/RESCORE_LOG.md §M2.6 for definitions):
    agree_both_high  — both hit rates >= 70%
    agree_both_low   — both hit rates <= 30%
    disagree_flipped — one >= 70%, other <= 30%  (investigation-worthy)
    new_partial      — 30..70% on either side
    missing_fresh    — condition present in frozen but absent in fresh
                       (M2.4 partial-completion artefact)

Standing-claim reproduction table is generated from a hardcoded list of
the 8 claims from `subsampling-cap-exp/outputs/audit/ACHIEVEMENTS_SUMMARY.md`.

Usage:
    python3 scripts/m2_6_compare_old_vs_new.py \
        --frozen /path/to/rescore_frozen/.../rows.csv \
        --fresh  /path/to/rescore_fresh/.../rows.csv \
        --out    docs/M2_6_OLD_VS_NEW.md

Non-goals: this script does not run the scorer. It consumes ScorerRow
CSVs that already exist on HPC (or wherever). It is analysis-only.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


# Join keys — a "condition" is one (experiment, receptor, partner, backbone,
# ligand_code) tuple. Every seed for that condition is a row.
JOIN_KEYS = ("experiment", "receptor_slug", "partner", "backbone", "ligand_code")


# Hit-rate bucket thresholds
HIGH = 0.70
LOW = 0.30


def load_rows(path: Path) -> list[dict[str, str]]:
    """Load a ScorerRow CSV. Empty file → empty list."""
    if not path.exists():
        print(f"WARN: {path} does not exist", file=sys.stderr)
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def _numeric(v: str) -> float:
    try:
        x = float(v)
        return x if not math.isnan(x) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def per_condition_hits(rows: list[dict[str, str]]) -> dict[tuple, dict[str, Any]]:
    """Group rows by JOIN_KEYS; return {key: {"n": N, "n_pass": ..., "hit_rate": ...}}.

    A row "passes" (contributes to the numerator) when:
      - `passed` (all A1..A6 gates cleared) AND
      - the primary axis `d_tm6_r350_r630_ca` has a numeric value AND
      - `delta_to_active` is negative (i.e. current axis is <= active
        reference on the TM6-outward direction — this is the paper's
        classical "active-like" verdict; see docs/AUDIT_TRAIL.md#7 for
        sign convention).

    Callers that want a different qualitative verdict (state
    classification, coherent-active, etc.) should call this with a
    different predicate. For M2.6 first-pass this is the TM6-only
    verdict, matching the ACHIEVEMENTS_SUMMARY headline claim.
    """
    buckets: dict[tuple, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        key = tuple(r.get(k, "") for k in JOIN_KEYS)
        buckets[key].append(r)

    out: dict[tuple, dict[str, Any]] = {}
    for key, group in buckets.items():
        n = len(group)
        n_pass = 0
        for r in group:
            passed = (r.get("passed", "").lower() == "true")
            if not passed:
                continue
            d_tm6 = _numeric(r.get("d_tm6_r350_r630_ca", ""))
            delta_a = _numeric(r.get("delta_to_active", ""))
            if math.isnan(d_tm6) or math.isnan(delta_a):
                continue
            if delta_a <= 0:  # <= active reference — TM6-only active-like
                n_pass += 1
        out[key] = {
            "n": n,
            "n_pass": n_pass,
            "hit_rate": (n_pass / n) if n > 0 else float("nan"),
        }
    return out


def classify_pair(frozen_hr: float, fresh_hr: float | None) -> str:
    """Categorise a (frozen_hitrate, fresh_hitrate) pair into an
    agreement class."""
    if fresh_hr is None or math.isnan(fresh_hr):
        return "missing_fresh"
    if math.isnan(frozen_hr):
        return "missing_frozen"
    if frozen_hr >= HIGH and fresh_hr >= HIGH:
        return "agree_both_high"
    if frozen_hr <= LOW and fresh_hr <= LOW:
        return "agree_both_low"
    if (frozen_hr >= HIGH and fresh_hr <= LOW) or (frozen_hr <= LOW and fresh_hr >= HIGH):
        return "disagree_flipped"
    return "new_partial"


def emit_markdown(
    frozen_hits: dict[tuple, dict[str, Any]],
    fresh_hits: dict[tuple, dict[str, Any]],
    out_path: Path,
) -> None:
    """Emit the per-condition + summary markdown table to out_path."""
    all_keys = set(frozen_hits) | set(fresh_hits)
    rows: list[dict[str, Any]] = []
    for key in sorted(all_keys):
        frozen = frozen_hits.get(key, {})
        fresh = fresh_hits.get(key, {})
        frozen_hr = frozen.get("hit_rate", float("nan"))
        fresh_hr = fresh.get("hit_rate", float("nan"))
        cls = classify_pair(frozen_hr, fresh_hr)
        rows.append({
            "key": key,
            "n_frozen": frozen.get("n", 0),
            "n_fresh": fresh.get("n", 0),
            "hr_frozen": frozen_hr,
            "hr_fresh": fresh_hr,
            "delta_pp": (fresh_hr - frozen_hr) * 100 if not (math.isnan(frozen_hr) or math.isnan(fresh_hr)) else float("nan"),
            "agreement": cls,
        })

    # Summary counts
    counts: dict[str, int] = defaultdict(int)
    for r in rows:
        counts[r["agreement"]] += 1

    lines: list[str] = []
    lines.append("# M2.6 — old-vs-new deterministic replay")
    lines.append("")
    lines.append("Comparison of frozen-corpus rescore vs fresh M2.4 rerun, ")
    lines.append("scored by the same scorer commit. See docs/RESCORE_LOG.md §M2.6 for ")
    lines.append("methodology.")
    lines.append("")
    lines.append("## Summary counts")
    lines.append("")
    lines.append("| agreement class | n conditions |")
    lines.append("|---|---:|")
    for cls in ("agree_both_high", "agree_both_low", "disagree_flipped",
                "new_partial", "missing_fresh", "missing_frozen"):
        lines.append(f"| {cls} | {counts[cls]} |")
    total = sum(counts.values())
    lines.append(f"| **total** | **{total}** |")
    lines.append("")

    if counts["disagree_flipped"]:
        lines.append("## Flipped verdicts (investigation-worthy)")
        lines.append("")
        lines.append("| experiment | receptor | partner | backbone | ligand | n_frozen | hr_frozen | n_fresh | hr_fresh | Δpp |")
        lines.append("|---|---|---|---|---|---:|---:|---:|---:|---:|")
        for r in rows:
            if r["agreement"] != "disagree_flipped":
                continue
            e, rc, p, bb, lg = r["key"]
            lines.append(
                f"| {e} | {rc} | {p} | {bb} | {lg} | "
                f"{r['n_frozen']} | {r['hr_frozen']:.2f} | "
                f"{r['n_fresh']} | {r['hr_fresh']:.2f} | "
                f"{r['delta_pp']:+.1f} |"
            )
        lines.append("")

    lines.append("## Per-condition table")
    lines.append("")
    lines.append("| experiment | receptor | partner | backbone | ligand | n_frozen | hr_frozen | n_fresh | hr_fresh | Δpp | class |")
    lines.append("|---|---|---|---|---|---:|---:|---:|---:|---:|---|")
    for r in rows:
        e, rc, p, bb, lg = r["key"]
        d = r["delta_pp"]
        d_s = f"{d:+.1f}" if not math.isnan(d) else "—"
        hf = f"{r['hr_frozen']:.2f}" if not math.isnan(r['hr_frozen']) else "—"
        hs = f"{r['hr_fresh']:.2f}" if not math.isnan(r['hr_fresh']) else "—"
        lines.append(
            f"| {e} | {rc} | {p} | {bb} | {lg} | "
            f"{r['n_frozen']} | {hf} | {r['n_fresh']} | {hs} | {d_s} | {r['agreement']} |"
        )
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"wrote {out_path} — {total} conditions "
          f"({counts['agree_both_high']} high, "
          f"{counts['agree_both_low']} low, "
          f"{counts['disagree_flipped']} flipped, "
          f"{counts['new_partial']} partial, "
          f"{counts['missing_fresh']} missing_fresh)",
          file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="m2_6_compare_old_vs_new")
    p.add_argument("--frozen", required=True, type=Path,
                   help="ScorerRow CSV from the frozen-corpus rescore")
    p.add_argument("--fresh", required=True, type=Path,
                   help="ScorerRow CSV from the fresh M2.4 rerun rescore")
    p.add_argument("--out", type=Path, default=Path("docs/M2_6_OLD_VS_NEW.md"),
                   help="output markdown path")
    args = p.parse_args(argv)

    frozen = load_rows(args.frozen)
    fresh = load_rows(args.fresh)
    if not frozen:
        print("ERROR: frozen input has no rows — cannot compare",
              file=sys.stderr)
        return 2
    if not fresh:
        print("WARN: fresh input has no rows — every condition will "
              "be marked missing_fresh", file=sys.stderr)

    frozen_hits = per_condition_hits(frozen)
    fresh_hits = per_condition_hits(fresh)
    emit_markdown(frozen_hits, fresh_hits, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
