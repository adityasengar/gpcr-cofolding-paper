#!/usr/bin/env python3
"""Propagation test 6 — scorer_git_sha end-to-end.

Motivation: audit trail #11 + the recurred audit finding #1 flagged in
Block A (2026-09-02): the HPC pip-installed venv strips `.git` metadata,
`_git_sha()` returns "no-git", and every provenance row records
`scorer_version = "0.1.0+no-git"`. A rows.csv with no scorer git sha
cannot be reproduced or reverified.

What it tests: rows.csv on-disk has a `scorer_git_sha` column populated
with a 40-char lowercase hex string on every row. Reuses the exact
check step7_dispatch_gate.check_scorer_git_sha performs.

Pass = every row's scorer_git_sha is a valid 40-hex string. Fail = any
row is "no-git" / empty / non-hex / dirty-suffixed.

This test does NOT re-score anything — it inspects existing provenance.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result

sys.path.insert(0, str(REPO / "scripts"))
from step7_dispatch_gate import check_scorer_git_sha, GateFailure

ROWS_CSV = REPO / "experiments/018_block_a_switch_test/analysis/rows.csv"


def main() -> int:
    if not ROWS_CSV.exists():
        return emit_result(
            "scorer_git_sha_endtoend", False,
            f"rows.csv missing at {ROWS_CSV}",
        )
    # Use scorer_git_sha embedded in rows.csv (04243c45...) as the
    # expected value — the test asserts uniformity and shape, not that
    # the sha matches current HEAD (which may have drifted since the
    # rescore was done).
    import csv as _csv
    embedded_sha = None
    with ROWS_CSV.open() as f:
        r = _csv.DictReader(f)
        for row in r:
            v = (row.get("scorer_git_sha") or "").strip()
            if v:
                embedded_sha = v
                break
    if not embedded_sha:
        return emit_result(
            "scorer_git_sha_endtoend", False,
            "rows.csv has no non-empty scorer_git_sha in the first row",
        )
    try:
        msg = check_scorer_git_sha(
            rows_csv_path=str(ROWS_CSV),
            expected_sha=embedded_sha,
        )
    except GateFailure as e:
        return emit_result(
            "scorer_git_sha_endtoend", False, str(e)[:400],
            {"embedded_sha": embedded_sha},
        )
    return emit_result(
        "scorer_git_sha_endtoend", True, msg,
        {"embedded_sha": embedded_sha, "check_output": msg[:200]},
    )


if __name__ == "__main__":
    raise SystemExit(main())
