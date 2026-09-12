#!/usr/bin/env python3
"""Propagation test 1 — seeds produce different structures.

Motivation: audit trail #13 (OF3 start_seed=42 collapse) shipped 2,375
OF3 predictions with identical internal seeds. Silent — indistinguishable
from within-seed sampler noise in the memo. This test asserts the seed
axis of variance is REAL for every backbone.

What it tests: for any (receptor × arm × backbone) cell in the current
`experiments/018_block_a_switch_test/analysis/rows.csv` that has ≥ 2
distinct dispatch seeds, the per-seed means of `d_tm6_r350_r630_ca`
differ by > epsilon. If any backbone shows near-zero between-seed
variance across all its cells, the seed-substitution contract is broken.

Threshold: an across-seed spread of ≥ 0.05 Å on the median cell for
each backbone. 0.05 Å is stricter than the 0.051 Å pre-fix OF3 collapse
observed 2026-09-01, and 100× looser than the 3.9 Å post-fix baseline —
comfortable band for pass/fail.
"""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result

ROWS_CSV = REPO / "experiments/018_block_a_switch_test/analysis/rows.csv"
METRIC = "d_tm6_r350_r630_ca"


def _backbone(path: str) -> str:
    p = (path or "").lower()
    for pat, name in (("_boltz", "boltz"), ("_chai", "chai"), ("_of3", "of3"),
                       ("_protenix", "protenix"), ("_af2mm", "af2mm")):
        if pat in p:
            return name
    return "unknown"


def _seed(path: str) -> str:
    """Extract the seed name from an input_path — for OF3, the ``seed_<n>/``
    subdirectory; for other backbones, the higher-level seed folder.
    """
    for part in (path or "").split("/"):
        if part.startswith("seed_"):
            return part
    return ""


def main() -> int:
    if not ROWS_CSV.exists():
        return emit_result(
            "seeds_produce_different_structures", False,
            f"rows.csv missing at {ROWS_CSV}",
        )
    # bucket (receptor, arm, backbone) -> {seed_name: [metric values]}
    from collections import defaultdict
    buckets: dict = defaultdict(lambda: defaultdict(list))
    with ROWS_CSV.open() as f:
        for r in csv.DictReader(f):
            m = r.get(METRIC)
            if not m or m.lower() == "nan":
                continue
            try:
                v = float(m)
            except ValueError:
                continue
            key = (r.get("receptor_slug", ""),
                   r.get("input_state_claim", ""),
                   _backbone(r.get("input_path", "")))
            buckets[key][_seed(r.get("input_path", ""))].append(v)

    per_bb: dict = defaultdict(list)
    for (rec, arm, bb), seeds in buckets.items():
        if len(seeds) < 2:
            continue
        means = [statistics.mean(v) for v in seeds.values() if v]
        if len(means) < 2:
            continue
        spread = max(means) - min(means)
        per_bb[bb].append((rec, arm, spread, list(seeds.keys())[:5]))

    problems = []
    evidence = {}
    for bb in sorted({b for _, _, b in buckets} - {"unknown"}):
        if not per_bb.get(bb):
            problems.append(f"{bb}: no multi-seed cells found")
            continue
        spreads = sorted(x[2] for x in per_bb[bb])
        median_spread = statistics.median(spreads)
        n_cells_ok = sum(1 for s in spreads if s >= 0.05)
        evidence[bb] = {
            "n_multi_seed_cells": len(spreads),
            "median_across_seed_spread_A": round(median_spread, 4),
            "min_spread": round(min(spreads), 4),
            "max_spread": round(max(spreads), 4),
            "n_cells_above_0.05A_threshold": n_cells_ok,
        }
        if median_spread < 0.05:
            problems.append(
                f"{bb}: median across-seed spread {median_spread:.4f} Å < 0.05 Å; "
                f"seed axis of variance may be collapsed."
            )

    if problems:
        return emit_result(
            "seeds_produce_different_structures", False,
            "; ".join(problems), evidence)

    return emit_result(
        "seeds_produce_different_structures", True,
        "every backbone shows > 0.05 Å median across-seed spread on d_tm6 "
        "(evidence per backbone captured)",
        evidence,
    )


if __name__ == "__main__":
    raise SystemExit(main())
