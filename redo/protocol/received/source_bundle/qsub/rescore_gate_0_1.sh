#!/bin/bash
#
# qsub/rescore_gate_0_1.sh — Block C Gate 0.1 retrospective rescore.
#
# Wraps scripts/rescore_parallel.py against the combined 42,812-row
# manifest (Block A + Block B + mn_consensus) so the new pocket-metric
# columns from A4's scorer extension land on every legacy holo row.
#
# CPU-only. No GPU compute, but `-l gpu_card=1` is still required on
# `default.q` per the site rule (jobs without gpu_card sit qw
# indefinitely — memory `paper_af3_gpu_pool_rules_2026_09_02.md`).
#
# Env-var contract:
#
#   MANIFEST   — path to Gate 0.1 manifest CSV (default: repo path)
#   OUT_DIR    — output dir for rows.csv + provenance JSON (required)
#   CACHE_DIR  — GPCRdb file-cache root (default: HPC scratch pre-warmed
#                per Block B precedent)
#   REF_SET    — path to refs/reference_set.csv (default: repo copy)
#
# Wall-time budget: ~90 min per Block B precedent (32k rows in ~60 min
# on 16 workers); grant 3 h.
#
#$ -N rescore_gate_0_1
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
MANIFEST=${MANIFEST:-$REPO/experiments/020_block_c_ligand_pharmacology/manifest/gate_0_1_rescore_manifest.csv}
: "${OUT_DIR:?OUT_DIR must be set (e.g. /hpc/scratch/sengaad1/paper_af3/gate_0_1_rescore_2026_09_03)}"

N_WORKERS=${N_WORKERS:-${NSLOTS:-16}}
REF_SET=${REF_SET:-$REPO/refs/reference_set.csv}
CACHE_DIR=${CACHE_DIR:-$REPO/refs/cache}

mkdir -p "$OUT_DIR"
cd "$REPO"

# Same venv discipline as qsub/rescore_parallel.sh.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found"; exit 1; }

python3 --version
python3 -c 'from scorer import _git_sha; print("scorer._git_sha=", _git_sha())'
echo "REPO=$REPO"
echo "MANIFEST=$MANIFEST"
echo "OUT_DIR=$OUT_DIR"
echo "N_WORKERS=$N_WORKERS"
echo "REF_SET=$REF_SET"
echo "CACHE_DIR=$CACHE_DIR"
echo "NSLOTS=${NSLOTS:-unset}"

wc -l "$MANIFEST"

python3 "$REPO/scripts/rescore_parallel.py" \
    --manifest "$MANIFEST" \
    --out "$OUT_DIR" \
    --n-workers "$N_WORKERS" \
    --ref-set "$REF_SET" \
    --cache-dir "$CACHE_DIR"

echo ""
echo "=== rescore_gate_0_1 complete ==="
ls -la "$OUT_DIR"
wc -l "$OUT_DIR/rows.csv"
