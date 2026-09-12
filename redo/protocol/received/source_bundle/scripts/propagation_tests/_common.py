"""Shared helpers for propagation tests.

Each test emits a machine-readable JSON row via ``emit_result`` to
``experiments/propagation_tests_2026_09_02/results.jsonl``. The driver
(scripts/run_propagation_tests.sh) aggregates and exit-codes accordingly.

Motivation: the three silent-config bugs this campaign chased (Chai MSA
env, OF3 start_seed=42, OF3 templates default-on, HPC scorer drift) all
looked green in status outputs while running against wrong config. These
tests assert that a distinctive value set at launch actually propagates
to the observable output of the run — the missing gate between "the
launcher said X" and "the compute node received X".
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RESULTS_PATH = REPO / "experiments/propagation_tests_2026_09_02/results.jsonl"


def emit_result(
    test_name: str,
    passed: bool,
    detail: str,
    evidence: dict | None = None,
) -> int:
    """Append a result row. Return the process exit code (0 on pass, 1 on fail)."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "test": test_name,
        "passed": bool(passed),
        "detail": detail,
        "evidence": evidence or {},
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"),
        "commit": _current_commit(),
    }
    with RESULTS_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    marker = "PASS" if passed else "FAIL"
    print(f"[{marker}] {test_name}: {detail}")
    return 0 if passed else 1


def _current_commit() -> str:
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return "unknown"


def ssh_capture(cmd: str, timeout: int = 30) -> tuple[int, str, str]:
    """Run a shell command on basel-hpc; return (rc, stdout, stderr)."""
    import subprocess
    r = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=10", "basel-hpc", cmd],
        capture_output=True, text=True, timeout=timeout,
    )
    return r.returncode, r.stdout, r.stderr
