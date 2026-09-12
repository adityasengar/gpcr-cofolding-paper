#!/bin/bash
# qsub/of3_seed_verification_dispatch.sh — dispatch the plan §2 OF3
# seed-fix verification cell.
#
# 3 receptors × cognate × 5 seeds × 5 samples = 75 CIFs total.
# One qsub per receptor; each runs OF3 with N_SEEDS=5, N_SAMPLES=5 so
# the runner yaml derives 5 distinct internal seeds from PRED_SEED and
# the sampler produces 5 output subdirectories per receptor.
#
# Acceptance (checked post-run):
#   1. No seed subdir is named `seed_2746317213` — proves the fix landed.
#   2. Median max element-wise across-seed diff (on d_tm6_r350_r630_ca)
#      > 0.3 Å across the 3 cells — proves the sampler is actually
#      seed-varying.
#
# Receptors: DRD2, ADRB2, HRH1 (all Class A cognate; normal
# cross-backbone spread; NOT AA2AR per plan §2's warning).

set -eo pipefail

REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH_BASE=/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_seedfix_verification
CAMPAIGN_SCRATCH=/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test

mkdir -p "$SCRATCH_BASE"

RECEPTORS=(DRD2 ADRB2 HRH1)
# Distinctive PRED_SEEDs derived from the dispatch timestamp. Each is
# passed to random.seed() inside qsub/rerun_of3.sh to produce 5
# internal seeds.
PRED_SEEDS=(2026090201 2026090202 2026090203)

for i in "${!RECEPTORS[@]}"; do
    rec="${RECEPTORS[$i]}"
    rec_lower=$(echo "$rec" | tr '[:upper:]' '[:lower:]')
    seed="${PRED_SEEDS[$i]}"

    # Reuse the query JSON from the campaign — any of the 5 cognate
    # dispatches works, they all use the same protein input.
    input_json=$(find "$CAMPAIGN_SCRATCH/018_block_a_switch_test_${rec_lower}_cognate_of3" \
        -name '_input_used.*.json' 2>/dev/null | head -1)
    if [ -z "$input_json" ]; then
        echo "FATAL: no input JSON found for $rec" >&2
        exit 1
    fi

    out_dir="$SCRATCH_BASE/${rec_lower}/of3"
    mkdir -p "$out_dir"
    sidecar="$out_dir/_rerun_plan.json"
    cp -f "$input_json" "$out_dir/_query_used.json"

    echo "=== $rec: seed=$seed input=$input_json out=$out_dir ==="

    # Prefer H100; fall back to A100. `-l gpu_type=h100` targets the
    # Hopper queue when available; otherwise scheduler grants A100.
    # Fall back to plain -l gpu_card=1 if gpu_type isn't honored.
    qsub \
        -N "of3_seedcheck_${rec_lower}" \
        -v PRED_INPUT="$input_json",PRED_OUT_DIR="$out_dir",PRED_SEED="$seed",PRED_SIDECAR="$sidecar",PRED_N_SEEDS=5,PRED_SAMPLES=5 \
        "$REPO/qsub/rerun_of3.sh"
done

echo ""
echo "Dispatch complete. Monitor at:"
echo "  $SCRATCH_BASE/*/of3/_of3_status.json"
echo "  /hpc/scratch/sengaad1/paper_af3/logs/rerun_of3.*.log"
