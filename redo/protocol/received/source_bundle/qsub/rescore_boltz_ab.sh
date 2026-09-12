#!/bin/bash
# qsub/rescore_boltz_ab.sh — score the 30 predictions from the Boltz
# --sampling_steps 50-vs-200 A/B (2026-09-01) with the frozen scorer.
#
# Submit:
#   qsub qsub/rescore_boltz_ab.sh
#
#$ -N rescore_boltz_ab
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/timing_boltz_50_vs_200_ab_2026_09_01/logs/rescore.$JOB_ID.log
#$ -j y
#$ -l h_rt=01:00:00
#$ -l m_mem_free=4G
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

REPO=${REPO:-/home/sengaad1/paper_af3}
AB_ROOT=/hpc/scratch/sengaad1/paper_af3/experiments/timing_boltz_50_vs_200_ab_2026_09_01
OUT_DIR=$AB_ROOT/scored
mkdir -p "$OUT_DIR"

cd "$REPO"
# openfold3 first (gemmi 0.7.5) for maximum compatibility, though Boltz-emitted
# CIF is fine with either.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate

python3 --version

python3 -c "from scorer.cli import batch_main; import sys; sys.exit(batch_main())" \
    --manifest "$AB_ROOT/scoring_manifest.csv" \
    --out "$OUT_DIR" \
    --ref-set refs/reference_set.csv \
    --cache-dir /hpc/scratch/sengaad1/paper_af3/refs/cache

echo ""
wc -l "$OUT_DIR/rows.csv"
cat "$OUT_DIR/failure_census.json"
