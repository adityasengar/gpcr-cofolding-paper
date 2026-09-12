#!/bin/bash
#
# qsub/refs_build.sh — run C12 (gpcr-refs build) + C13 (gpcr-refs thresholds)
# on basel-hpc.
#
# Reuses coordinate files from /hpc/scratch/sengaad1/subsampling/refs/gpcr_panel_pdbs/
# (fetched by the frozen pipeline). Anything missing is re-fetched from RCSB.
#
#$ -N gpcr_refs_build_thresholds
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/refs_build.$JOB_ID.log
#$ -j y
#$ -l h_rt=02:00:00
#$ -l m_mem_free=2G
#$ -l gpu_card=1               # mandatory on default.q per hpc-basel gotcha
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL       # needed for RCSB / GPCRdb outbound network

# CUDA_VISIBLE_DEVICES per hpc-basel gotcha (GPU cgroup isolation absent)
if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS

# Repo location
REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH=/hpc/scratch/sengaad1/paper_af3
FROZEN_PDBS=/hpc/scratch/sengaad1/subsampling/refs/gpcr_panel_pdbs

mkdir -p "$SCRATCH/refs/pdb" "$SCRATCH/logs" "$SCRATCH/refs/cache/gpcrdb" "$SCRATCH/refs/cache/rcsb"

cd "$REPO"

# Activate a venv — use the same env you already have python3.10+ / gemmi
source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    { echo "no venv found; install requirements and rerun"; exit 1; }

python3 --version

# ========== C12 step 1: dry run (MANDATORY per amendment S2) ==========

echo "=== C12 DRY RUN ==="
python3 -m scorer.refs_build build --dry-run \
    --input refs/reference_pdbs.csv \
    --reuse-from "$FROZEN_PDBS" \
    --pdb-cache "$SCRATCH/refs/pdb" \
    --cache-dir "$SCRATCH/refs/cache" \
    2>&1 | head -400

echo ""
echo "=== C12 LIVE RUN ==="

# ========== C12 step 2: live build ==========

python3 -m scorer.refs_build build \
    --input refs/reference_pdbs.csv \
    --out-csv refs/reference_set.csv \
    --out-provenance refs/provenance/ \
    --pdb-cache "$SCRATCH/refs/pdb" \
    --cache-dir "$SCRATCH/refs/cache" \
    --reuse-from "$FROZEN_PDBS"

echo ""
echo "=== C13 THRESHOLDS (M1 gate) ==="

# ========== C13: threshold regeneration ==========

python3 -m scorer.refs_build thresholds \
    --reference-set refs/reference_set.csv \
    --pdb-cache "$SCRATCH/refs/pdb" \
    --cache-dir "$SCRATCH/refs/cache" \
    --out refs/state_thresholds.csv \
    --report docs/THRESHOLD_DISTRIBUTION.md

echo ""
echo "=== M1 ARTEFACTS ==="
ls -la refs/reference_set.csv refs/pdbs.csv refs/state_thresholds.csv
wc -l refs/reference_set.csv refs/pdbs.csv refs/state_thresholds.csv
echo "---"
head -30 docs/THRESHOLD_DISTRIBUTION.md
echo ""
echo "STOP AT M1. Report the threshold distribution and wait for approval."
