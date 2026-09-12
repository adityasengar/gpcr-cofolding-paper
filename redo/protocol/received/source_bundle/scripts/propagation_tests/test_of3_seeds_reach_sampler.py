#!/usr/bin/env python3
"""Propagation test 4 — OF3 seeds reach the sampler.

Motivation: audit trail #13. The vendored `if num_model_seeds:`
branch of experiment_runner.py:611 hardcoded `start_seed = 42` and
overwrote launcher-provided seeds with `generate_seeds(42, N)`,
producing internal seed 2746317213 for every prediction across 2,375
OF3 rows.

What it tests (two halves):

  A. Vendored patch is applied and hard-fails when
     `--num-model-seeds` is passed. Runs a Python probe on HPC:
     construct InferenceExperimentRunner.update_config_with_cli_args
     with num_model_seeds=5 and assert ValueError is raised with the
     paper_af3 sentinel string.

  B. No existing Block A OF3 output directory is named
     `seed_2746317213/`. Grep `/hpc/scratch/.../018_block_a.../of3/`.
     Any hit here means the seed collapse has recurred (or was never
     re-run).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO, emit_result, ssh_capture


PATCH_PROBE = r'''
source /home/sengaad1/software/venvs/openfold3/bin/activate >/dev/null 2>&1
python3 <<PY 2>&1
from openfold3.entry_points.experiment_runner import InferenceExperimentRunner
class F(InferenceExperimentRunner):
    def __init__(self): self.seeds = [1234]
try:
    F().update_config_with_cli_args(
        output_dir=None, num_diffusion_samples=None,
        num_model_seeds=5, use_msa_server=None, use_templates=None)
    print("PROBE_FAIL_NO_RAISE")
except ValueError as e:
    s = str(e)
    if "paper_af3 vendored patch" in s or "--num-model-seeds is deprecated" in s:
        print("PROBE_PASS")
    else:
        print(f"PROBE_UNEXPECTED_MESSAGE {s!r}")
except Exception as e:
    print(f"PROBE_UNEXPECTED {type(e).__name__} {e!r}")
PY
'''

SENTINEL_SEED_GLOB = (
    "ls -d /hpc/scratch/sengaad1/paper_af3/experiments/"
    "018_block_a_switch_test/*/*/of3/seed_2746317213 2>/dev/null | head -3"
)


def main() -> int:
    # A. Vendored patch fires on --num-model-seeds
    rc_a, out_a, err_a = ssh_capture(PATCH_PROBE, timeout=60)
    a_ok = "PROBE_PASS" in out_a
    if not a_ok:
        a_detail = f"probe stdout: {out_a.strip()[-300:]}, stderr: {err_a.strip()[-200:]}"
    else:
        a_detail = "vendored patch fires (ValueError with sentinel)"

    # B. No seed_2746317213/ subdirs in the Block A output tree
    rc_b, out_b, err_b = ssh_capture(SENTINEL_SEED_GLOB, timeout=20)
    sentinel_hits = [ln.strip() for ln in out_b.splitlines() if ln.strip()]
    b_ok = not sentinel_hits
    b_detail = (
        f"no seed_2746317213 dirs in Block A output tree"
        if b_ok else f"regression: found {len(sentinel_hits)} seed_2746317213/ subdirs"
    )

    passed = a_ok and b_ok
    return emit_result(
        "of3_seeds_reach_sampler", passed,
        f"vendored_patch_fires={a_ok}; no_sentinel_dirs={b_ok}",
        {"vendored_patch_probe": a_detail,
         "sentinel_dir_hits": sentinel_hits[:5],
         "sentinel_dir_check": b_detail},
    )


if __name__ == "__main__":
    raise SystemExit(main())
