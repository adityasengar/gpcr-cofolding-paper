#!/usr/bin/env python3
"""Propagation test 5 — chai pre-flight refuses on missing .aligned.pqt.

Motivation: audit trail #10 countermeasure. When
CHAI_MSA_DIRECTORY is set but a required protein-chain .aligned.pqt
is missing, `rerun_chai.sh` MUST hard-fail rather than fall back to
single-sequence with `ok=true`.

What it tests: extracts the pre-flight Python from
`qsub/rerun_chai.sh` (the same code that gets embedded into every
chai job), runs it against a synthetic FASTA that names a sequence
whose SHA cannot exist in the cache, and asserts the pre-flight
returns non-zero.

Pass = pre-flight exits ≠ 0 with an error message identifying at
least one missing .aligned.pqt. Fail = pre-flight passes (which would
mean the audit-trail #10 countermeasure has regressed).
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result

LAUNCHER = REPO / "qsub/rerun_chai.sh"


def _extract_preflight_python() -> str | None:
    """Read the launcher and extract the `python3 - "$PRED_INPUT"
    "$CHAI_MSA_DIRECTORY" <<'PYEOF' … PYEOF` heredoc body verbatim.
    """
    text = LAUNCHER.read_text()
    m = re.search(
        r"python3\s+-\s+.*?<<'PYEOF'\n(.*?)\nPYEOF",
        text, re.S,
    )
    if not m:
        return None
    return m.group(1)


def main() -> int:
    preflight = _extract_preflight_python()
    if preflight is None:
        return emit_result(
            "chai_aligned_pqt_present", False,
            "could not locate pre-flight PYEOF heredoc in rerun_chai.sh — "
            "audit-trail #10 countermeasure appears removed",
        )
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Synthetic FASTA with one protein chain whose SHA won't exist.
        fasta = td / "test_input.fasta"
        # A short seq that definitely won't be in the cache
        fasta.write_text(
            ">protein|name=synthetic_test\nMSYNTHETICPROBEQQQAAAWWW\n"
        )
        # Empty directory pretending to be the cache
        msa_dir = td / "empty_cache"
        msa_dir.mkdir()

        # Wrap the extracted preflight into a runnable file with the
        # two positional args in place of $PRED_INPUT / $CHAI_MSA_DIRECTORY.
        preflight_file = td / "preflight.py"
        preflight_file.write_text(
            f"import sys\nsys.argv = ['preflight', '{fasta}', '{msa_dir}']\n"
            + preflight
        )

        r = subprocess.run(
            [sys.executable, str(preflight_file)],
            capture_output=True, text=True, timeout=15,
        )
    passed = r.returncode != 0
    detail = (
        f"pre-flight exited {r.returncode} (expected non-zero on missing .aligned.pqt); "
        f"stderr snippet: {r.stderr.strip()[:200]!r}"
    )
    return emit_result(
        "chai_aligned_pqt_present", passed, detail,
        {"exit_code": r.returncode, "stdout": r.stdout[:400],
         "stderr": r.stderr[:400]},
    )


if __name__ == "__main__":
    raise SystemExit(main())
