#!/bin/bash
#
# qsub/rerun_protenix.sh — M2.3 fresh Protenix v2 co-fold for one row.
#
# Env contract (identical to rerun_boltz.sh):
#   PRED_INPUT     absolute path to a Protenix input JSON
#   PRED_OUT_DIR   absolute path where Protenix output should land
#   PRED_SEED      integer seed (deterministic from fresh_seed_for)
#   PRED_SIDECAR   absolute path to the rerun-plan JSON
#
# Notes (structure-prediction skill, basel-hpc section):
#   - `--msa_server_mode protenix` — NOT colabfold (naming mismatch).
#   - Needs CUDA/12.1.1 module + TORCH_CUDA_ARCH_LIST for A100 (8.0) or
#     H100 (9.0) — otherwise fast_layer_norm_cuda_v2 fails to compile.
#     Compiled `.so` caches under ~/.cache/torch_extensions/.
#   - Protenix takes an explicit `--seed` so seed substitution is clean.
#
# Not yet HPC-verified — smoke-test 5 rows before scaling per plan.

#$ -N pa3_ptx_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rerun_protenix.$JOB_ID.log
#$ -j y
#$ -l h_rt=05:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
module load CUDA/12.1.1                   # required for fast_layer_norm_cuda_v2

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
    export SINGULARITYENV_CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
fi
unset OMP_NUM_THREADS

# Detect GPU compute capability and set TORCH_CUDA_ARCH_LIST accordingly.
# A30 / A100 → 8.0, H100 → 9.0. Failure to set this breaks the JIT compile
# on first run.
CC=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "")
case "$CC" in
    9.0|9.*)  export TORCH_CUDA_ARCH_LIST="9.0" ;;
    8.0|8.*)  export TORCH_CUDA_ARCH_LIST="8.0" ;;
    *)        export TORCH_CUDA_ARCH_LIST="8.0;9.0" ;;
esac
echo "GPU compute cap: ${CC:-unknown}  ->  TORCH_CUDA_ARCH_LIST=$TORCH_CUDA_ARCH_LIST"

set -u

: "${PRED_INPUT:?PRED_INPUT is required (path to Protenix input JSON)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required}"
: "${PRED_SEED:?PRED_SEED is required}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required}"

[ -f "$PRED_INPUT" ] || { echo "FATAL: PRED_INPUT missing: $PRED_INPUT" >&2; exit 1; }

mkdir -p "$PRED_OUT_DIR" "$(dirname "$PRED_SIDECAR")"

PTX_VENV=${PTX_VENV:-/home/sengaad1/software/venvs/protenix}
if [ ! -d "$PTX_VENV" ]; then
    echo "FATAL: protenix venv not found at $PTX_VENV" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$PTX_VENV/bin/activate"

python3 --version
which protenix
nvidia-smi -L || true

echo "=== M2.3 rerun_protenix ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo "ARCH_LIST  : $TORCH_CUDA_ARCH_LIST"
echo ""

cp -f "$PRED_INPUT" "$PRED_OUT_DIR/_input_used.$(basename "$PRED_INPUT")"

set +e
# NOTE: Protenix uses `--seeds` (plural, comma-separated) not `--seed`
# (singular) — verified 2026-08-27 by the GPU benchmark agent. Previous
# `--seed "$PRED_SEED"` invocation caused `protenix pred` to exit
# immediately with an argparse error, which the M2.4 supervisor logged
# as a permanent failure. Change is single-arg-name substitution;
# semantics unchanged (we pass one seed at a time).
# Diversity-study samples-per-seed multiplier (default 1).
N_SAMPLES="${PRED_SAMPLES:-1}"
echo "PRED_SAMPLES=$N_SAMPLES"

protenix pred \
    -i "$PRED_INPUT" \
    -o "$PRED_OUT_DIR" \
    --use_default_params True \
    --msa_server_mode protenix \
    --sample "$N_SAMPLES" --cycle 3 --step 50 \
    --seeds "$PRED_SEED"
EXIT=$?
set -e

echo ""
echo "=== protenix exit=$EXIT ==="

STATUS_JSON="$PRED_OUT_DIR/_protenix_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, sys
from pathlib import Path
exit_code = int(sys.argv[1]); out_dir = Path(sys.argv[2])
seed = int(sys.argv[3]); status_path = Path(sys.argv[4])
produced = sorted(str(p) for p in out_dir.rglob("*.cif"))
status = {"backbone": "protenix", "exit_code": exit_code, "seed": seed,
          "produced_files": produced, "n_produced": len(produced),
          "ok": exit_code == 0 and len(produced) > 0}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '_protenix_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
