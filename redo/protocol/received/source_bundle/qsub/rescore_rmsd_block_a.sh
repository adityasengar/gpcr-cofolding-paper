#!/bin/bash
#
# qsub/rescore_rmsd_block_a.sh — plan §1(a) primary deliverable.
#
# Computes CA-RMSD to active and inactive reference PDBs for every
# Block A prediction in analysis/rows.csv. CPU-only — no GPU. Estimate
# ~20 min for 8,000 Class A predictions on one qsub slot with warm
# caches.
#
# Output: experiments/018_block_a_switch_test/analysis/rows.rmsd.csv
# (input columns + rmsd_to_active_ref, rmsd_to_inactive_ref, rmsd_pos,
# rmsd_n_residues_used, rmsd_note).
#
# Env contract:
#   CLASS_FILTER   optional — "A" | "B" | "F" | "" (default: A first)
#   LIMIT          optional — process only the first N rows (0=all)
#
#$ -N rmsd_rescore
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/logs/rmsd_rescore.$JOB_ID.log
#$ -j y
#$ -l h_rt=02:00:00
#$ -l m_mem_free=8G
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
unset OMP_NUM_THREADS
set -u

REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH=/hpc/scratch/sengaad1/paper_af3
SLUG=018_block_a_switch_test
LOG_DIR=$SCRATCH/experiments/$SLUG/logs
mkdir -p "$LOG_DIR"

cd "$REPO"

# openfold3 venv carries gemmi + the scorer package as editable install.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found — install requirements and rerun"; exit 1; }

python3 --version
echo "REPO=$REPO"
echo "SLUG=$SLUG"
echo "CLASS_FILTER=${CLASS_FILTER:-}"
echo "LIMIT=${LIMIT:-0}"
echo "DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

ROWS_CSV="$REPO/experiments/$SLUG/analysis/rows.csv"
OUT_CSV="$REPO/experiments/$SLUG/analysis/rows.rmsd${CLASS_FILTER:+.class_$CLASS_FILTER}.csv"
REFS_CACHE="$REPO/refs/cache/pdb"

[ -f "$ROWS_CSV" ] || { echo "FATAL: rows.csv missing: $ROWS_CSV"; exit 1; }
[ -d "$REFS_CACHE" ] || { echo "FATAL: refs cache missing: $REFS_CACHE"; exit 1; }

echo "ROWS_CSV=$ROWS_CSV"
echo "OUT_CSV=$OUT_CSV"
echo "REFS_CACHE=$REFS_CACHE (n=$(ls "$REFS_CACHE" | wc -l))"
echo ""

python3 "$REPO/scripts/rescore_rmsd.py" \
    --rows-csv "$ROWS_CSV" \
    --reference-set "$REPO/refs/reference_set.csv" \
    --refs-cache "$REFS_CACHE" \
    --out-csv "$OUT_CSV" \
    ${CLASS_FILTER:+--class-filter "$CLASS_FILTER"} \
    ${LIMIT:+--limit "$LIMIT"}

echo ""
echo "=== rmsd rescore complete ==="
wc -l "$OUT_CSV"
