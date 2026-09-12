#!/bin/bash
# qsub/timing_chai_cache.sh — Block-A canonical-settings timing on H100
# with the pre-built .aligned.pqt MSA cache.
# Canonical: --num-trunk-recycles 3 --num-diffn-timesteps 50 --num-diffn-samples 1
# (default 5 model_idx samples). CHAI_MSA_DIRECTORY set.
#
#$ -N ta_chai_c
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01/logs/chai_cache.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=8G
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
INPUT="$TIMING_DIR/inputs/chai.fasta"
OUT_DIR="$TIMING_DIR/out_chai_cache"
# chai-lab fold asserts output dir is empty; keep wall.time OUTSIDE it.
TIME_FILE="$TIMING_DIR/logs/chai_cache.wall.time"
rm -rf "$OUT_DIR"
mkdir -p "$TIMING_DIR/logs"

export CHAI_MSA_DIRECTORY=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai

CHAI_VENV=${CHAI_VENV:-/home/sengaad1/software/venvs/chai1}
source "$CHAI_VENV/bin/activate"

echo "=== timing_chai_cache ==="
echo "JOB_ID: ${JOB_ID:-<none>}"
echo "HOST  : $(hostname)"
echo "GPU   : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo "MSA   : $CHAI_MSA_DIRECTORY  ($(ls "$CHAI_MSA_DIRECTORY" 2>/dev/null | wc -l) files)"
nvidia-smi -L || true
which chai-lab
python3 --version

START_EPOCH=$(date +%s)
echo "START_EPOCH=$START_EPOCH" > "$TIME_FILE"

set +e
/usr/bin/time -v -o "$TIME_FILE.gnu" \
chai-lab fold \
    "$INPUT" \
    "$OUT_DIR" \
    --msa-directory "$CHAI_MSA_DIRECTORY" \
    --seed 42 \
    --num-trunk-recycles 3 \
    --num-diffn-timesteps 50 \
    --num-diffn-samples 1
EXIT=$?
set -e

END_EPOCH=$(date +%s)
WALL=$((END_EPOCH - START_EPOCH))
echo "END_EPOCH=$END_EPOCH" >> "$TIME_FILE"
echo "WALL_SEC=$WALL" >> "$TIME_FILE"
echo "EXIT=$EXIT" >> "$TIME_FILE"

echo ""
echo "=== chai_cache exit=$EXIT wall=${WALL}s ==="
cat "$TIME_FILE"

find "$OUT_DIR" -maxdepth 6 -name '*.cif' -printf '%p  %s bytes\n' 2>/dev/null | head -20

exit "$EXIT"
