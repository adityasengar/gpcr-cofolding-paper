#!/bin/bash
#
# qsub/rescore_fold_integrity.sh — Block B Stage 0 Gate 1 fold-integrity
# rescore driver (2026-09-03).
#
# Runs scripts/rescore_fold_integrity.py against a rows.csv on scratch,
# emitting a 4-axis sidecar CSV (tm6_helicity_6_30_6_50, chain_breaks,
# ramachandran_outlier_frac, icl3_modelled_count). CPU-only compute
# (multiprocessing.Pool over CIF list). Same resource shape as
# qsub/rescore_parallel.sh: 16 CPU slots, 2 GB/slot, single node.
#
# `-l gpu_card=1` is the SITE rule on default.q (CPU-only jobs stay
# queued indefinitely otherwise per CLAUDE.md's engineering invariants
# + Block C plan §11). The requested GPU slot is unused.
#
# Env-var contract (pass via `qsub -v NAME=VALUE,...`):
#
#   ROWS       — path to rows.csv (required; typically block B's on scratch)
#   OUT        — path for the sidecar CSV output (required)
#   CACHE_DIR  — GPCRdb file-cache root (default: /home/sengaad1/paper_af3/refs/cache)
#   N_WORKERS  — worker count (default: NSLOTS = 16)
#
# The qrsh/qsub env-forwarding gotcha: qsub does NOT forward the caller's
# environment by default. Every variable this script consumes MUST be
# listed in the caller's `qsub -v` invocation or set at the top of this
# script.
#
#$ -N rescore_fold_integrity
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
: "${ROWS:?ROWS must be set (rows.csv on /hpc/scratch)}"
: "${OUT:?OUT must be set to the sidecar CSV path}"

N_WORKERS=${N_WORKERS:-${NSLOTS:-16}}
CACHE_DIR=${CACHE_DIR:-$REPO/refs/cache}

mkdir -p "$(dirname "$OUT")"

cd "$REPO"

# Reuse the openfold3 venv (gemmi 0.7.5 present). Fall back to boltz.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found"; exit 1; }

python3 --version
echo "REPO=$REPO"
echo "ROWS=$ROWS"
echo "OUT=$OUT"
echo "CACHE_DIR=$CACHE_DIR"
echo "N_WORKERS=$N_WORKERS"
echo "NSLOTS=${NSLOTS:-unset}"
echo "JOB_ID=${JOB_ID:-unset}"

python3 "$REPO/scripts/rescore_fold_integrity.py" \
    --rows "$ROWS" \
    --out "$OUT" \
    --cache-dir "$CACHE_DIR" \
    --n-workers "$N_WORKERS"

echo ""
echo "=== rescore_fold_integrity complete ==="
ls -la "$OUT"
wc -l "$OUT"
