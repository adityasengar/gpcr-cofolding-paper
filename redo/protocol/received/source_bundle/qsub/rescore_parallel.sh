#!/bin/bash
#
# qsub/rescore_parallel.sh — parallel rescore driver (prototype 2026-09-02).
#
# Runs scripts/rescore_parallel.py over a pre-exploded rescore manifest
# using a `multiprocessing.Pool` with N worker processes on a single node.
# CPU-only; no GPU request.
#
# Environment variables the caller can set:
#
#   MANIFEST   — path to rescore manifest CSV (required)
#   OUT_DIR    — output dir for rows.csv + provenance JSON (required)
#   N_WORKERS  — worker count (default: matches -pe smp slot, see below)
#   REF_SET    — path to refs/reference_set.csv (default: repo copy)
#   CACHE_DIR  — GPCRdb file-cache root (default: repo refs/cache).
#                Recommend pointing at a per-benchmark copy under scratch
#                so writes never contend with a concurrent rescore.
#
# SGE resource request: 16 CPU slots, 2 GB per slot = 32 GB total. The
# basel-hpc `chbscl-0-*` compute nodes are 16-core (32-thread) boxes and
# a `smp 32` request cannot be honoured on a single node — the 2026-09-02
# 32-slot bench job stayed in `qw` indefinitely. The 16-slot request
# lands on either a 16-core `chbscl-0-*` box or a 128-core `nrchbs-*`
# box within seconds. Adjust `m_mem_free` up if your manifest hits many
# large mmCIFs concurrently.
#
#$ -N rescore_parallel
#$ -cwd
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=2G
#$ -l gpu_card=1
#$ -pe smp 16

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
unset OMP_NUM_THREADS
set -u

REPO=${REPO:-/home/sengaad1/paper_af3}
: "${MANIFEST:?MANIFEST must be set to a rescore manifest CSV}"
: "${OUT_DIR:?OUT_DIR must be set to an output directory}"

# Default worker count follows the SGE slot grant. NSLOTS is set by SGE.
N_WORKERS=${N_WORKERS:-${NSLOTS:-16}}
REF_SET=${REF_SET:-$REPO/refs/reference_set.csv}
CACHE_DIR=${CACHE_DIR:-$REPO/refs/cache}

mkdir -p "$OUT_DIR"

cd "$REPO"

# Same venv as the sequential rescore (gemmi 0.7.5, scorer deps).
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found"; exit 1; }

python3 --version
echo "REPO=$REPO"
echo "MANIFEST=$MANIFEST"
echo "OUT_DIR=$OUT_DIR"
echo "N_WORKERS=$N_WORKERS"
echo "REF_SET=$REF_SET"
echo "CACHE_DIR=$CACHE_DIR"
echo "NSLOTS=${NSLOTS:-unset}"

python3 "$REPO/scripts/rescore_parallel.py" \
    --manifest "$MANIFEST" \
    --out "$OUT_DIR" \
    --n-workers "$N_WORKERS" \
    --ref-set "$REF_SET" \
    --cache-dir "$CACHE_DIR"

echo ""
echo "=== rescore_parallel complete ==="
ls -la "$OUT_DIR"
wc -l "$OUT_DIR/rows.csv"
