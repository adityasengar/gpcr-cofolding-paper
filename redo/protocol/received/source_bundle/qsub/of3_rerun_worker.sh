#!/bin/bash
#
# qsub/of3_rerun_worker.sh — one qsub worker for the 2026-09-02 OF3
# re-run pool. Runs block_a_worker.sh's pop-run-mark loop against
# /hpc/scratch/sengaad1/paper_af3/of3_rerun_2026_09_02/queue.csv.
#
# Alternative to the tmux+qrsh pool launcher — same worker code, but
# each worker is a self-contained qsub batch job. Scale by submitting
# this script N times.
#
# Env passed via qsub -v:
#   WORKER_ID   e.g. w0, w1, ...
#   BLOCK_A_POOL  /hpc/scratch/sengaad1/paper_af3/of3_rerun_2026_09_02
#
#$ -N of3_rerun_wkr
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/of3_rerun_2026_09_02/logs/qsub.$JOB_ID.log
#$ -j y
#$ -l h_rt=24:00:00
#$ -l m_mem_free=32G
#$ -l gpu_card=1
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

: "${WORKER_ID:?WORKER_ID is required}"
: "${BLOCK_A_POOL:?BLOCK_A_POOL is required}"

export BLOCK_A_POOL
REPO=${REPO:-/home/sengaad1/paper_af3}

echo "=== of3 rerun worker $WORKER_ID ==="
echo "JOB_ID  : ${JOB_ID:-<no>}"
echo "HOST    : $(hostname)"
echo "GPU     : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo "POOL    : $BLOCK_A_POOL"
echo "DATE    : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

bash "$REPO/scripts/block_a_worker.sh" "$WORKER_ID"
