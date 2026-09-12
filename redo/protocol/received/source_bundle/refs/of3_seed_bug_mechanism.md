# OF3 seed bug — mechanism, verified

Investigation completed 2026-09-02 by orphaned sub-investigation from previous agent.

## Root cause

`/home/sengaad1/software/venvs/openfold3/lib/python3.13/site-packages/openfold3/entry_points/experiment_runner.py`, lines 608–612 in `InferenceExperimentRunner.update_config_with_cli_args`:

```python
if num_model_seeds:
    start_seed = 42
    self.seeds = generate_seeds(start_seed, num_model_seeds)
```

`start_seed` is a **hardcoded literal 42**. Every time the CLI is called with `--num-model-seeds N`, this line overwrites any seeds from the runner yaml with `generate_seeds(42, N)`.

`generate_seeds` (validator.py, near `InferenceExperimentSettings`, ~line 271):

```python
def generate_seeds(start_seed, num_seeds):
    random.seed(start_seed)
    return [random.randint(0, 2**32 - 1) for _ in range(num_seeds)]
```

## Verification

REPL: `random.seed(42); [random.randint(0, 2**32-1) for _ in range(5)]` →
```
[2746317213, 1181241943, 958682846, 3163119785, 1812140441]
```

First value `2746317213` exactly matches the fixed internal seed observed in all 2,375 OF3 rows in the Block A campaign (and in the frozen v3.7 corpus dating back to 2026-08-27). Deterministic — not import-chain entropy.

## Code path

1. Launcher calls `run_openfold.py predict --query-json … --num-model-seeds 5 [--runner-yaml …]`.
2. `predict` CLI has **no** `--seed` / `--seeds` flag. Query-JSON `seeds:` field is passed through only for output subdirectory naming via `inference_query_set.seeds` (run_openfold.py:662).
3. `InferenceExperimentConfig(**runner_args)` — if runner yaml is empty/missing, `InferenceExperimentSettings.seeds` defaults to `[42]`.
4. `InferenceExperimentRunner.__init__` sets `self.seeds = experiment_config.experiment_settings.seeds`, then calls `update_config_with_cli_args(num_model_seeds=5, …)` which **hardcodes** `start_seed=42` and overwrites `self.seeds` with `generate_seeds(42, 5)`.
5. `self.seeds` propagates to inference; per-seed subdirectories `seed_2746317213/`, `seed_1181241943/`, …  are written for every query, every dispatch.

## Patch — wrapper-level (Option A)

The wrapper cannot fix this by `random.seed(<launcher_seed>)` before invoking OF3 — line 611 hard-resets to 42 regardless of Python's global state.

**What works**: build a per-query runner yaml with an explicit `experiment_settings.seeds:` list derived from the dispatch seed, and invoke `run_openfold.py predict` **without** `--num-model-seeds`. Then the `if num_model_seeds:` branch is skipped, `self.seeds` stays at the yaml's list, and the launcher-derived seeds win.

Bash snippet for `qsub/rerun_of3.sh`:

```bash
NUM_SEEDS="${NUM_SEEDS:-5}"
SEEDS_YAML="${WORKDIR}/runner_seeds.yml"
python3 - > "${SEEDS_YAML}" <<PY
import random
random.seed(int("${QUERY_SEED}"))
seeds = [random.randint(0, 2**32 - 1) for _ in range(${NUM_SEEDS})]
print("experiment_settings:")
print(f"  seeds: {seeds}")
PY

# Do NOT pass --num-model-seeds; that triggers the hardcoded start_seed=42
# branch in experiment_runner.py:611.
python /home/sengaad1/software/venvs/openfold3/lib/python3.13/site-packages/openfold3/run_openfold.py predict \
    --query-json "${QUERY_JSON}" \
    --runner-yaml "${SEEDS_YAML}" \
    --output-dir "${OUTDIR}"
```

## Rationale for Option A over alternatives

- **Option A (wrapper)**: keeps openfold3 install untouched — venv is shared, no site-packages editing that would be wiped by `pip install --upgrade`.
- **Option B (monkey-patch validator.py:262)**: red herring — the offending line is actually experiment_runner.py:611.
- **Option C (edit site-packages directly)**: fragile per above.

## Post-patch verification

Per-dispatch: `random.seed(QUERY_SEED); [random.randint(0, 2**32-1) for _ in range(5)]` should equal the output-subdirectory names `seed_<n>/` for that job. If any seed subdir is named `seed_2746317213`, the fix did not land.

## Flag to double-check before landing

Verify the launcher isn't relying on `--num-model-seeds` being present for some other side effect (number of output subdirectories, etc.). Code review suggests `num_model_seeds` only exists to size the auto-generated seed list, so dropping it in favor of an explicit yaml `seeds:` is equivalent — but confirm on a single-cell smoke test before the 950-pred re-run.
