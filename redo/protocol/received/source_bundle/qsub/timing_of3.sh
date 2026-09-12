#!/bin/bash
# qsub/timing_of3.sh — Block-A canonical-settings timing on H100.
# Canonical: --use-msa-server true --num-diffusion-samples 5 --num-model-seeds 1
# Hot ColabFold cache (pre-warmed 2026-09-01).
#
#$ -N ta_of3
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01/logs/of3.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -l gpu_arch=hopper_h100
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS
set -u

TIMING_DIR=${TIMING_DIR:-/hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01}
INPUT="$TIMING_DIR/inputs/of3.json"
OUT_DIR="$TIMING_DIR/out_of3"
TIME_FILE="$OUT_DIR/wall.time"
mkdir -p "$OUT_DIR"

OF3_VENV=${OF3_VENV:-/home/sengaad1/software/venvs/openfold3}
OF3_CKPT=${OF3_CKPT:-/home/sengaad1/software/openfold3/checkpoints/of3-p2-155k.pt}
source "$OF3_VENV/bin/activate"

echo "=== timing_of3 ==="
echo "JOB_ID: ${JOB_ID:-<none>}"
echo "HOST  : $(hostname)"
echo "GPU   : ${CUDA_VISIBLE_DEVICES:-<none>}"
nvidia-smi -L || true
which run_openfold
python3 --version

START_EPOCH=$(date +%s)
echo "START_EPOCH=$START_EPOCH" > "$TIME_FILE"

set +e
/usr/bin/time -v -o "$TIME_FILE.gnu" \
run_openfold predict \
    --query-json "$INPUT" \
    --output-dir "$OUT_DIR" \
    --inference-ckpt-path "$OF3_CKPT" \
    --use-msa-server true \
    --num-diffusion-samples 5 \
    --num-model-seeds 1
EXIT=$?
set -e

END_EPOCH=$(date +%s)
WALL=$((END_EPOCH - START_EPOCH))
echo "END_EPOCH=$END_EPOCH" >> "$TIME_FILE"
echo "WALL_SEC=$WALL" >> "$TIME_FILE"
echo "EXIT=$EXIT" >> "$TIME_FILE"

echo ""
echo "=== of3 exit=$EXIT wall=${WALL}s ==="
cat "$TIME_FILE"

find "$OUT_DIR" -maxdepth 6 -name '*.cif' -printf '%p  %s bytes\n' 2>/dev/null | head -20

exit "$EXIT"
