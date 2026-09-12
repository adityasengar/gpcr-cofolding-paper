#!/bin/bash
#
# qsub/rescore_of3_rerun.sh — rescore the 2026-09-02 OF3 seed-fix
# re-run tree at
# /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_of3_rerun_2026_09_02/
#
# Same shape as qsub/rescore_block_a_2026_09_01.sh but points at the
# re-run slug so the original Block A rows.csv is untouched. Output
# lands at experiments/018_block_a_switch_test_of3_rerun_2026_09_02/
# analysis/rows.csv.
#
#$ -N rescore_of3_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_of3_rerun_2026_09_02/logs/rescore.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=4G
#$ -l gpu_card=1
#$ -pe smp 8

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS
set -u

REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH=/hpc/scratch/sengaad1/paper_af3
SLUG=018_block_a_switch_test_of3_rerun_2026_09_02
LOG_DIR=$SCRATCH/experiments/$SLUG/logs
mkdir -p "$LOG_DIR"

cd "$REPO"

source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found — install requirements and rerun"; exit 1; }

python3 --version
echo "REPO=$REPO"
echo "SLUG=$SLUG"

python3 "$REPO/scripts/rescore_experiment.py" \
    --slug "$SLUG" \
    --experiments-root "$REPO/experiments" \
    --scratch-root "$SCRATCH/experiments" \
    --manifest "$REPO/experiments/$SLUG/manifest/manifest.csv" \
    --ref-set "$REPO/refs/reference_set.csv"

echo ""
echo "=== rescore complete ==="
ls -la "$REPO/experiments/$SLUG/analysis/" 2>/dev/null
wc -l "$REPO/experiments/$SLUG/analysis/rows.csv" 2>/dev/null
