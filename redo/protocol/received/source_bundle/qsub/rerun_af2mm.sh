#!/bin/bash
#
# qsub/rerun_af2mm.sh — M2.3 fresh AlphaFold-2 multimer co-fold for one row.
#
# Env contract (identical to rerun_boltz.sh):
#   PRED_INPUT     absolute path to an AF2-multimer FASTA
#   PRED_OUT_DIR   absolute path where AF2 output should land
#   PRED_SEED      integer seed (deterministic from fresh_seed_for)
#   PRED_SIDECAR   absolute path to the rerun-plan JSON
#
# Notes (structure-prediction skill, basel-hpc section):
#   - AF2 2.3.2 is a system module (not a user venv): AlphaFold/2.3.2-foss-2023a-CUDA-12.1.1
#   - Databases at /db/camm/alphafoldDB/ — expensive to copy, share the
#     module's default paths.
#   - Long walltime — AF2 with full MSA + relaxation is slow (~1–2 h/target).
#   - `--random_seed` gives us deterministic seed substitution.
#   - AF2 multimer is used *only* for Wave 46 (architecture-independence
#     claim, 750 preds). All other backbones are covered by Boltz/OF3/
#     Protenix/Chai.
#
# Not yet HPC-verified — smoke-test 5 rows before scaling per plan.

#$ -N pa3_af2mm_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rerun_af2mm.$JOB_ID.log
#$ -j y
#$ -l h_rt=08:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -pe smp 8

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
module load AlphaFold/2.3.2-foss-2023a-CUDA-12.1.1

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS
set -u

: "${PRED_INPUT:?PRED_INPUT is required (path to AF2-mm FASTA)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required}"
: "${PRED_SEED:?PRED_SEED is required}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required}"

[ -f "$PRED_INPUT" ] || { echo "FATAL: PRED_INPUT missing: $PRED_INPUT" >&2; exit 1; }

mkdir -p "$PRED_OUT_DIR" "$(dirname "$PRED_SIDECAR")"

AF2_DBS=${AF2_DBS:-/db/camm/alphafoldDB}
which run_alphafold.sh 2>/dev/null || echo "warn: run_alphafold.sh not on PATH — module load ok?"
nvidia-smi -L || true

echo "=== M2.3 rerun_af2mm ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "AF2_DBS    : $AF2_DBS"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo ""

cp -f "$PRED_INPUT" "$PRED_OUT_DIR/_input_used.$(basename "$PRED_INPUT")"

# AF2 wants a per-target output subdir; use PRED_OUT_DIR directly and
# let AF2 create <basename>/ under it. This matches how the frozen w46
# jobs were structured.
set +e
run_alphafold.sh \
    -d "$AF2_DBS" \
    -o "$PRED_OUT_DIR" \
    -m multimer \
    -f "$PRED_INPUT" \
    -t 2022-01-01 \
    -c reduced_dbs \
    -e 3 \
    -r "$PRED_SEED"
EXIT=$?
set -e

echo ""
echo "=== af2mm exit=$EXIT ==="

STATUS_JSON="$PRED_OUT_DIR/_af2mm_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, sys
from pathlib import Path
exit_code = int(sys.argv[1]); out_dir = Path(sys.argv[2])
seed = int(sys.argv[3]); status_path = Path(sys.argv[4])
# AF2 emits ranked_N.pdb + unrelaxed_model_N_multimer_v3_pred_M.pdb
produced = sorted(str(p) for p in out_dir.rglob("*.pdb"))
status = {"backbone": "af2mm", "exit_code": exit_code, "seed": seed,
          "produced_files": produced, "n_produced": len(produced),
          "ok": exit_code == 0 and len(produced) > 0}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

find "$PRED_OUT_DIR" -maxdepth 6 \( -name 'ranked_*.pdb' -o -name '_af2mm_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
