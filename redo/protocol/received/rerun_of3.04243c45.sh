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

# Refuse to launch if the yaml would still collapse to the buggy 42.
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
python3 /home/sengaad1/paper_af3/qsub/colabfold_shim.py of3 predict \
    --query-json "$PRED_INPUT" \
    --output-dir "$PRED_OUT_DIR" \
    --inference-ckpt-path "$OF3_CKPT" \
    --use-msa-server true \
    --use-templates false \
    --num-diffusion-samples "$N_SAMPLES" \
    --runner-yaml "$SEEDS_YAML"
EXIT=$?
set -e

echo ""
echo "=== of3 exit=$EXIT ==="

STATUS_JSON="$PRED_OUT_DIR/_of3_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, sys
from pathlib import Path
exit_code = int(sys.argv[1]); out_dir = Path(sys.argv[2])
seed = int(sys.argv[3]); status_path = Path(sys.argv[4])
produced = sorted(str(p) for p in out_dir.rglob("*.cif"))
status = {"backbone": "of3", "exit_code": exit_code, "seed": seed,
          "produced_files": produced, "n_produced": len(produced),
          "ok": exit_code == 0 and len(produced) > 0}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '_of3_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
