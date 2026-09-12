#!/bin/bash
#
# qsub/rescore_block_a_2026_09_01.sh — rescore the 1900-prediction Block A
# GPCR co-folding campaign against the sealed-subset-removed reference_set.csv.
#
# Manifest-mode: per-cell (receptor × arm × backbone) metadata is read from
# experiments/018_block_a_switch_test/manifest/manifest.csv (SHA
# 360cf8c68c4cb6122834ca794ffffc13dd65067c044127b0e3d21f1381459194).
#
# Reference set: refs/reference_set.csv (sealed-subset removed, SHA
# 04d0897b15e6721e00cc5ea5477ed597aa84e6c1d0a5ff43a1c7d634d176f533).
#
# Scratch tree lives at
# /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/<cell>/.
# ~380 cells × ~5 samples/seed × ~5 seeds = ~9500 structures. v3_6 rescored
# 17,568 predictions in ~45 min, so h_rt=03:00:00 gives plenty of headroom.
#
#$ -N rescore_block_a
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/logs/rescore.$JOB_ID.log
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
SLUG=018_block_a_switch_test
LOG_DIR=$SCRATCH/experiments/$SLUG/logs
mkdir -p "$LOG_DIR"

cd "$REPO"

# openfold3 first: gemmi 0.7.5 parses all backbones' mmCIF (Boltz/Chai/OF3/Protenix).
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
ls -la "$REPO/experiments/$SLUG/analysis/"
wc -l "$REPO/experiments/$SLUG/analysis/rows.csv"
