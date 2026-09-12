#!/usr/bin/env python3
"""Smoke-test the vendored OF3 patch is applied on-disk.

The paper_af3 vendored patch (audit #13) replaces the hardcoded
`start_seed = 42` branch in openfold3's
`entry_points/experiment_runner.py` with a `raise ValueError(...)`.
This script reads the on-disk file and asserts the patch is applied.

Run after any venv reinstall — a `pip install --upgrade` (or a fresh
venv build) restores the upstream file and reactivates the seed bug.

Usage
-----
    python3 scripts/verify_of3_vendored_patch.py [--venv /path/to/of3/venv]

Exit codes
----------
    0  patch present
    1  patch absent (upstream file restored)
    2  target file missing / unreadable
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SENTINEL = "paper_af3 vendored patch"
PRE_PATCH_MARKER = "start_seed = 42"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--venv",
        default=os.environ.get("OF3_VENV", "/home/sengaad1/software/venvs/openfold3"),
        help="OF3 venv path (default $OF3_VENV or /home/sengaad1/...)",
    )
    args = ap.parse_args(argv)

    target = (
        Path(args.venv)
        / "lib/python3.13/site-packages/openfold3/entry_points/experiment_runner.py"
    )
    if not target.exists():
        print(f"FAIL — target file missing: {target}", file=sys.stderr)
        return 2
    try:
        text = target.read_text()
    except OSError as e:
        print(f"FAIL — cannot read {target}: {e}", file=sys.stderr)
        return 2

    if SENTINEL in text:
        print(
            f"PASS — vendored patch applied at {target} "
            f"(sentinel found: {SENTINEL!r})"
        )
        return 0

    if PRE_PATCH_MARKER in text:
        print(
            f"FAIL — patch absent, upstream `{PRE_PATCH_MARKER}` still present "
            f"at {target}. Re-run qsub/apply_vendored_of3_patch.sh. "
            f"See refs/of3_seed_bug_mechanism.md and audit trail #13.",
            file=sys.stderr,
        )
        return 1

    print(
        f"FAIL — neither sentinel nor pre-patch marker present at {target}. "
        f"Upstream may have changed shape; inspect manually.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
