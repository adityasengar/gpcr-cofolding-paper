#!/usr/bin/env python3
"""Regenerate ``refs/scorer_expected_shas.json`` from the current tree.

The JSON pin is the local↔HPC scorer-sync gate (audit trail #11
countermeasure). Every file in ``scripts.step7_dispatch_gate.
SCORER_FILES_TRACKED`` MUST be represented in the JSON, and each entry's
SHA256 MUST match the current local file byte-for-byte. Per-worker
pre-flight scripts (``scripts/block_a_worker.sh``,
``scripts/block_b_worker.sh``) read this JSON on the compute node and
refuse to score if the HPC copy has drifted.

**Run this AFTER any change to a file in ``SCORER_FILES_TRACKED``, and
BEFORE any dispatch that runs the scorer.**

Rationale for existing separately from ``step7_dispatch_gate.py``:
the gate computes SHAs on demand for verification. This script writes
them for persistence, so pre-flight scripts don't need ssh access.

Idempotent — running twice against the same tree produces the same
JSON. The tracked-file tuple lives in one place
(``scripts.step7_dispatch_gate.SCORER_FILES_TRACKED``); this script
imports it rather than duplicating.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.step7_dispatch_gate import SCORER_FILES_TRACKED  # noqa: E402

OUT_PATH = REPO / "refs" / "scorer_expected_shas.json"


def _sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    missing: list[str] = []
    entries: dict[str, str] = {}
    for rel in SCORER_FILES_TRACKED:
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
