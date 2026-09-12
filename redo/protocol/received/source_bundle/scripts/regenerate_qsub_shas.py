#!/usr/bin/env python3
"""Regenerate ``refs/qsub_expected_shas.json`` from the current tree.

The JSON pin is the local↔HPC qsub-sync gate (audit-1.2 countermeasure,
2026-09-04). Every file in ``scripts.step7_dispatch_gate.
QSUB_FILES_TRACKED`` MUST be represented in the JSON, and each entry's
SHA256 MUST match the current local file byte-for-byte. The gate
``check_qsub_files_hpc_matches_local`` computes SHAs on demand for
verification; this JSON exists so per-worker pre-flight scripts (which
lack ssh access to the coordinator) can pin an expected value without
another network round-trip.

**Run this AFTER any change to a file in ``QSUB_FILES_TRACKED``, and
BEFORE any dispatch that runs those launchers.**

Companion to ``scripts/regenerate_scorer_shas.py`` (audit-#11
countermeasure). Same shape, different tracked-file tuple.

Idempotent — running twice against the same tree produces the same
JSON. The tracked-file tuple lives in one place
(``scripts.step7_dispatch_gate.QSUB_FILES_TRACKED``); this script
imports it rather than duplicating.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.step7_dispatch_gate import QSUB_FILES_TRACKED  # noqa: E402

OUT_PATH = REPO / "refs" / "qsub_expected_shas.json"


def _sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    missing: list[str] = []
    entries: dict[str, str] = {}
    for rel in QSUB_FILES_TRACKED:
        p = REPO / rel
        if not p.exists():
            missing.append(rel)
            continue
        entries[rel] = _sha256_hex(p)

    if missing:
        print(
            f"ERROR: missing local files: {missing}",
            file=sys.stderr,
        )
        return 2

    # Sort keys for deterministic output diffs.
    OUT_PATH.write_text(
        json.dumps(entries, indent=2, sort_keys=True) + "\n"
    )
    print(f"wrote {OUT_PATH} — {len(entries)} tracked files:")
    for rel, h in sorted(entries.items()):
        print(f"  {rel}: {h[:12]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
