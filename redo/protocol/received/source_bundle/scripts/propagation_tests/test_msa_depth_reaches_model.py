#!/usr/bin/env python3
"""Propagation test 2 — MSA depth reaches the model.

Motivation: audit trail #10 (Chai silent single-seq fallback). Chai's
`--msa-directory` mode should give predictions access to N-sequence
MSAs from the pre-built .aligned.pqt cache; the audit found that
`CHAI_MSA_DIRECTORY` was not propagating through `qsub -v` and Chai
was silently reading no MSAs. Status JSONs reported ok=true.

What it tests: the CHAI_MSA_DIRECTORY cache on HPC contains
.aligned.pqt files whose parquet payloads carry > 1 sequence per file
(i.e. real MSAs, not single-sequence stubs) AND the rerun_chai.sh
launcher wires `--msa-directory` behind the `CHAI_MSA_DIRECTORY` env.

Both halves must hold for MSA depth to reach the model:
  1. Cache holds real MSAs.
  2. Launcher references the cache directory.

Passes when: at least one .aligned.pqt has ≥ 5 sequences AND the
launcher grep confirms wiring.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result, ssh_capture

LAUNCHER = REPO / "qsub/rerun_chai.sh"
CHAI_CACHE_DIR = "/hpc/scratch/sengaad1/paper_af3/msa_cache/chai"


def _launcher_wires_cache() -> tuple[bool, str]:
    if not LAUNCHER.exists():
        return False, f"launcher missing at {LAUNCHER}"
    text = LAUNCHER.read_text()
    if "--msa-directory" not in text:
        return False, "launcher does not pass --msa-directory"
    if "CHAI_MSA_DIRECTORY" not in text:
        return False, "launcher does not read CHAI_MSA_DIRECTORY env var"
    return True, "launcher wires --msa-directory via CHAI_MSA_DIRECTORY"


def _cache_holds_real_msa() -> tuple[bool, dict]:
    """Ask HPC to sample one .aligned.pqt and count rows."""
    # First: any .aligned.pqt files at all?
    cmd = (
        f"ls -1 {CHAI_CACHE_DIR}/*.aligned.pqt 2>/dev/null | head -3"
    )
    rc, out, err = ssh_capture(cmd, timeout=15)
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not files:
        return False, {"error": f"no .aligned.pqt files at {CHAI_CACHE_DIR}",
                       "stderr": err[:200]}
    # For each sampled file, count rows via python (parquet is small).
    py_probe = (
        f"python3 -c \""
        f"import pyarrow.parquet as pq; "
        f"import sys; "
        f"totals = []; "
        f"[totals.append((f, pq.read_table(f).num_rows)) for f in {files!r}]; "
        f"print(totals)\""
    )
    rc, out, err = ssh_capture(py_probe, timeout=30)
    if rc != 0:
        # Retry with chai venv activated so pyarrow is available.
        py_probe = (
            f"source /home/sengaad1/software/venvs/chai1/bin/activate "
            f">/dev/null 2>&1; " + py_probe
        )
        rc, out, err = ssh_capture(py_probe, timeout=30)
    row_counts_raw = out.strip()
    # Parse row counts BEFORE truncating for evidence storage — the
    # parser needs the full tuple list. `out` may contain the HPC login
    # banner followed by the tuple list — extract just the list.
    parsed_rows: list[tuple[str, int]] = []
    for line in row_counts_raw.splitlines():
        s = line.strip()
        if s.startswith("[(") and s.endswith(")]"):
            try:
                parsed_rows = list(eval(s))
                break
            except Exception:
                pass
    ok = bool(parsed_rows)
    return ok, {"sampled_files": files, "row_counts_output": row_counts_raw[-800:],
                "parsed_row_counts": parsed_rows,
                "rc": rc, "stderr": err[:200]}


def main() -> int:
    launcher_ok, launcher_detail = _launcher_wires_cache()
    cache_ok, cache_evidence = _cache_holds_real_msa()

    max_rows = 0
    for _, n in cache_evidence.get("parsed_row_counts", []):
        if isinstance(n, int) and n > max_rows:
            max_rows = n
    depth_ok = max_rows >= 5

    passed = launcher_ok and cache_ok and depth_ok
    detail = (
        f"launcher_ok={launcher_ok} ({launcher_detail}); "
        f"cache_reachable={cache_ok}; max_msa_depth_sampled={max_rows}"
    )
    return emit_result(
        "msa_depth_reaches_model", passed, detail,
        {"launcher": launcher_detail, "cache": cache_evidence,
         "max_msa_depth_sampled": max_rows},
    )


if __name__ == "__main__":
    raise SystemExit(main())
