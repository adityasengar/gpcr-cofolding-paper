#!/bin/bash
#
# qsub/rerun_of3.sh — M2.3 fresh OpenFold-3-preview co-fold for one row.
#
# Env contract (identical to rerun_boltz.sh):
#   PRED_INPUT     absolute path to an OF3 query JSON
#   PRED_OUT_DIR   absolute path where OF3 output should land
#   PRED_SEED      integer seed (deterministic from fresh_seed_for)
#   PRED_SIDECAR   absolute path to the rerun-plan JSON
#
# Notes (structure-prediction skill, basel-hpc section):
#   - OF3 preview scores lower than final AF3/Boltz — kept in the panel
#     for architecture diversity, not primary accuracy claim.
#   - Weights fetched via HuggingFace token (site's NO_PROXY = *.amazonaws
#     blocks the S3 route; HF is the working alternative).
#   - OF3 uses `--random-seed` (single integer) so seed substitution is
#     clean.
#
# Not yet HPC-verified — smoke-test 5 rows before scaling per plan.

#$ -N pa3_of3_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rerun_of3.$JOB_ID.log
#$ -j y
#$ -l h_rt=05:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
    export SINGULARITYENV_CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
fi
unset OMP_NUM_THREADS
set -u

: "${PRED_INPUT:?PRED_INPUT is required (path to OF3 query JSON)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required}"
: "${PRED_SEED:?PRED_SEED is required}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required}"

[ -f "$PRED_INPUT" ] || { echo "FATAL: PRED_INPUT missing: $PRED_INPUT" >&2; exit 1; }

mkdir -p "$PRED_OUT_DIR" "$(dirname "$PRED_SIDECAR")"

OF3_VENV=${OF3_VENV:-/home/sengaad1/software/venvs/openfold3}
OF3_CKPT=${OF3_CKPT:-/home/sengaad1/software/openfold3/checkpoints/of3-p2-155k.pt}

if [ ! -d "$OF3_VENV" ]; then
    echo "FATAL: openfold3 venv not found at $OF3_VENV" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$OF3_VENV/bin/activate"

python3 --version
which run_openfold
[ -f "$OF3_CKPT" ] || { echo "FATAL: OF3 checkpoint missing at $OF3_CKPT" >&2; exit 1; }
nvidia-smi -L || true

echo "=== M2.3 rerun_of3 ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo ""
export LAUNCH_TS_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cp -f "$PRED_INPUT" "$PRED_OUT_DIR/_input_used.$(basename "$PRED_INPUT")"

set +e
# NOTE: OF3's `run_openfold predict` does NOT accept a `--random-seed`
# flag (verified 2026-08-27). The seed must be baked into the runner
# yaml's `experiment_settings.seeds:` list. Historically we relied on
# the query JSON's `seeds:` field — but that field only names the
# output subdirectory. The internal seed used for sampling is set by
# InferenceExperimentRunner.update_config_with_cli_args, which — if
# `--num-model-seeds` is passed — hardcodes `start_seed=42` and
# overwrites everything with `generate_seeds(42, N)`. That's the bug
# behind every OF3 prediction landing at internal seed 2,746,317,213
# (see refs/of3_seed_bug_mechanism.md, PREREG §9 erratum).
#
# Fix: build a per-query runner yaml with explicit
# `experiment_settings.seeds:` derived from PRED_SEED, and invoke
# WITHOUT `--num-model-seeds`. Then the offending branch is skipped
# and the launcher-derived seed wins.
N_SAMPLES="${PRED_SAMPLES:-1}"
N_SEEDS="${PRED_N_SEEDS:-1}"
echo "PRED_SAMPLES=$N_SAMPLES  N_SEEDS=$N_SEEDS"

SEEDS_YAML="$PRED_OUT_DIR/_runner_seeds.yml"
python3 - "$PRED_SEED" "$N_SEEDS" "$SEEDS_YAML" <<'PY'
import random, sys
from pathlib import Path
query_seed = int(sys.argv[1])
n_seeds = int(sys.argv[2])
out = Path(sys.argv[3])
random.seed(query_seed)
seeds = [random.randint(0, 2**32 - 1) for _ in range(n_seeds)]
out.write_text(
    "experiment_settings:\n"
    f"  seeds: {seeds}\n"
)
print(f"wrote {out} with seeds={seeds}")
PY

# Belt-and-braces regression guard (see qsub/openfold3_vendored_patch.diff
# and refs/of3_seed_bug_mechanism.md). The primary defence is the
# vendored raise ValueError at experiment_runner.py:611 — any launcher
# that inadvertently re-adds --num-model-seeds now hard-fails inside
# openfold3 rather than silently reactivating the seed collapse.
# The grep-guard below stays as a second layer in case the vendored
# patch is wiped by a `pip install --upgrade` and a future edit here
# reintroduces the buggy default.
if grep -q '2746317213\|\[42\]' "$SEEDS_YAML"; then
    echo "FATAL: runner_seeds.yml contains the buggy default seed. Refusing to launch." >&2
    cat "$SEEDS_YAML" >&2
    exit 1
fi

# ColabFold shim — enforces (connect=30, read=600) minimum timeout on
# api.colabfold.com and writes an HTTP-summary sidecar per prediction.
# Third appearance of the 6.02s-ReadTimeout bug in ColabFold clients
# (chai POST/ticket, OF3 GET/result/download, ...); the shim wraps
# requests.get/post generically so the next endpoint is covered too.
# Verified 2026-09-01: OF3's raw run at 748s (91 ReadTimeouts on ONE
# prediction, cache hit confirmed) → projected ~200s under the shim.
export COLABFOLD_SIDECAR="$PRED_OUT_DIR/_of3_colabfold_http_summary.json"

# Triton kernel launch limit — OF3's fused evoformer attention kernel
# (_triton_evo_attn at core/kernels/triton/evoformer.py:_attn_fwd) fails
# with "Triton Error [CUDA]: invalid argument" when
# --num-diffusion-samples exceeds ~25 on typical GPCR sequences (~350 aa
# + 150-row MSA). Ceiling bracket 2026-09-06 (Tier D1 CNR2 apo):
# n=25 → ok=True 25 CIFs; n=50 → ok=False 0 CIFs. Automatic chunking
# below preserves the pre-registered n_samples per (seed, row) while
# keeping each OF3 call below the ceiling.
# MSA source — pre-fetched .a3m in JSON (Tier D3 depth-tier mode) vs live
# ColabFold server (default; every other tier). When MSA_A3M_PATH is set,
# scorer/propose.py has already populated main_msa_file_paths + paired_msa_
# file_paths inside the query JSON, so the launcher must pass
# --use-msa-server false to avoid ColabFold overriding those paths.
export OF3_USE_MSA_SERVER="true"
if [ -n "${MSA_A3M_PATH:-}" ]; then
    export OF3_USE_MSA_SERVER="false"
    echo "MSA source  : pre-fetched (MSA_A3M_PATH=$MSA_A3M_PATH; --use-msa-server false)"
else
    echo "MSA source  : live ColabFold server (--use-msa-server true)"
fi

OF3_MAX_PER_CALL="${OF3_MAX_PER_CALL:-25}"
if [ "$N_SAMPLES" -le "$OF3_MAX_PER_CALL" ]; then
    # Fast path: single call, unchanged from pre-chunking behaviour.
    python3 /home/sengaad1/paper_af3/qsub/colabfold_shim.py of3 predict \
        --query-json "$PRED_INPUT" \
        --output-dir "$PRED_OUT_DIR" \
        --inference-ckpt-path "$OF3_CKPT" \
        --use-msa-server "$OF3_USE_MSA_SERVER" \
        --use-templates false \
        --num-diffusion-samples "$N_SAMPLES" \
        --runner-yaml "$SEEDS_YAML"
    EXIT=$?
else
    # Chunked path — Triton ceiling exceeded, split into subdirs.
    N_CHUNKS=$(( (N_SAMPLES + OF3_MAX_PER_CALL - 1) / OF3_MAX_PER_CALL ))
    echo "OF3 chunking: N_SAMPLES=$N_SAMPLES > OF3_MAX_PER_CALL=$OF3_MAX_PER_CALL → $N_CHUNKS chunks"
    EXIT=0
    REMAINING=$N_SAMPLES
    for CHUNK_IDX in $(seq 0 $((N_CHUNKS - 1))); do
        if [ "$REMAINING" -gt "$OF3_MAX_PER_CALL" ]; then
            SAMPLES_THIS=$OF3_MAX_PER_CALL
        else
            SAMPLES_THIS=$REMAINING
        fi
        CHUNK_DIR="$PRED_OUT_DIR/chunk_$CHUNK_IDX"
        mkdir -p "$CHUNK_DIR"
        # Deterministic sub-seed per chunk from PRED_SEED
        CHUNK_YAML="$CHUNK_DIR/_runner_seeds.yml"
        python3 - "$PRED_SEED" "$CHUNK_IDX" "$N_SEEDS" "$CHUNK_YAML" <<'PY'
import random, sys
from pathlib import Path
pred_seed = int(sys.argv[1])
chunk_idx = int(sys.argv[2])
n_seeds = int(sys.argv[3])
out = Path(sys.argv[4])
random.seed(pred_seed * 1_000_003 + chunk_idx)
seeds = [random.randint(0, 2**32 - 1) for _ in range(n_seeds)]
out.write_text("experiment_settings:\n  seeds: " + repr(seeds) + "\n")
print(f"chunk {chunk_idx}: wrote {out} with seeds={seeds}")
PY
        # Sentinel-bug guard per chunk
        if grep -q '2746317213\|\[42\]' "$CHUNK_YAML"; then
            echo "FATAL: chunk $CHUNK_IDX runner yaml contains sentinel bug seed. Refusing." >&2
            cat "$CHUNK_YAML" >&2
            exit 1
        fi
        echo ">>> chunk $CHUNK_IDX/$N_CHUNKS: $SAMPLES_THIS samples → $CHUNK_DIR"
        python3 /home/sengaad1/paper_af3/qsub/colabfold_shim.py of3 predict \
            --query-json "$PRED_INPUT" \
            --output-dir "$CHUNK_DIR" \
            --inference-ckpt-path "$OF3_CKPT" \
            --use-msa-server "$OF3_USE_MSA_SERVER" \
            --use-templates false \
            --num-diffusion-samples "$SAMPLES_THIS" \
            --runner-yaml "$CHUNK_YAML"
        CHUNK_EXIT=$?
        if [ $CHUNK_EXIT -ne 0 ]; then
            EXIT=$CHUNK_EXIT
        fi
        REMAINING=$((REMAINING - SAMPLES_THIS))
    done
fi
set -e

echo ""
echo "=== of3 exit=$EXIT ==="

STATUS_JSON="$PRED_OUT_DIR/_of3_status.json"
STATUS_WRITER="$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")/status_writer.py"
if [ ! -f "$STATUS_WRITER" ]; then
    STATUS_WRITER="/home/sengaad1/paper_af3/qsub/status_writer.py"
fi
# runtime_config resolves the runner-yaml seeds actually loaded plus
# flags a sentinel-bug-seed regression (audit trail #13 countermeasure).
export SEEDS_YAML_PATH="$SEEDS_YAML"
CONFIG_JSON=$(python3 -c "import json,os; print(json.dumps({
    'pred_input': os.environ.get('PRED_INPUT'),
    'pred_out_dir': os.environ.get('PRED_OUT_DIR'),
    'pred_sidecar': os.environ.get('PRED_SIDECAR'),
    'runner_yaml_path': os.environ.get('SEEDS_YAML_PATH'),
    'n_samples': int(os.environ.get('PRED_SAMPLES', '1')),
    'n_seeds': int(os.environ.get('PRED_N_SEEDS', '1')),
    'seed_passed': int(os.environ.get('PRED_SEED')),
    'num_model_seeds_flag_passed': False,
    'use_templates': False,
    'use_msa_server': os.environ.get('OF3_USE_MSA_SERVER', 'true').lower() == 'true',
    'msa_a3m_path': os.environ.get('MSA_A3M_PATH', ''),
    'of3_venv': os.environ.get('OF3_VENV'),
    'of3_ckpt': os.environ.get('OF3_CKPT'),
    'launch_ts_utc': os.environ.get('LAUNCH_TS_UTC'),
}))")
python3 "$STATUS_WRITER" \
    --backbone of3 \
    --exit-code "$EXIT" \
    --seed "$PRED_SEED" \
    --out-dir "$PRED_OUT_DIR" \
    --status-json "$STATUS_JSON" \
    --config-json "$CONFIG_JSON"

find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '_of3_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
