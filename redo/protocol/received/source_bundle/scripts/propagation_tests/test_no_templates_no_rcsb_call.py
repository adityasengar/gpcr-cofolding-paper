#!/usr/bin/env python3
"""Propagation test 3 — templates disabled, no rcsb call.

Motivation: audit trail #9. OF3 defaults `use_templates=True` at
inference, silently fetching from data.rcsb.org. The prospectivity
claim (de novo generation of a conformational state) is incompatible
with template retrieval — for any receptor whose Gs-bound structure is
in the PDB, "predicted active" reduces to "retrieved."

What it tests (belt-and-braces):
  1. All 4 launchers pass `--use-templates false` (OF3) or omit any
     template opt-in (Boltz/Chai/Protenix).
  2. `scorer/propose.py` emits no template field for any backbone.
  3. Grep of the launcher trees for `rcsb.org` shows no reference.

Strace/network sandbox not used (heavy on HPC and gated on kernel
policy); instead we assert on the CODE PATHS that would trigger any
outbound RCSB call. If the code paths are absent, the call cannot fire.
This mirrors step7_dispatch_gate::check_no_templates_any_backbone.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result

# Reuse the exact check step7 uses so this test lands only if it stays
# in sync with the gate.
sys.path.insert(0, str(REPO / "scripts"))
from step7_dispatch_gate import check_no_templates_any_backbone, GateFailure


def _grep_rcsb() -> tuple[bool, list[str]]:
    hits = []
    for path in list((REPO / "qsub").glob("*.sh")) + [REPO / "scorer/propose.py"]:
        if not path.exists():
            continue
        text = path.read_text()
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            # Skip comment lines
            if stripped.startswith("#"):
                continue
            if "rcsb.org" in stripped or "data.rcsb" in stripped:
                hits.append(f"{path.relative_to(REPO)}:{i}: {stripped[:80]}")
    return (not hits), hits


def main() -> int:
    # Part 1 — templates locked off across launchers + propose.py
    try:
        step7_msg = check_no_templates_any_backbone()
        step7_ok = True
    except GateFailure as e:
        step7_msg = str(e)
        step7_ok = False

    # Part 2 — no rcsb.org grep hits in non-comment lines
    rcsb_ok, rcsb_hits = _grep_rcsb()

    passed = step7_ok and rcsb_ok
    detail = (
        f"step7_templates_check={step7_ok}; rcsb_grep_clean={rcsb_ok}; "
        f"rcsb_hits={len(rcsb_hits)}"
    )
    return emit_result(
        "no_templates_no_rcsb_call", passed, detail,
        {"step7_message": step7_msg,
         "rcsb_grep_hits": rcsb_hits[:10]},
    )


if __name__ == "__main__":
    raise SystemExit(main())
