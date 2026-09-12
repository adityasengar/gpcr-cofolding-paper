#!/bin/bash
# qsub/timing_protenix.sh — Block-A canonical-settings timing on H100.
# Canonical: --msa_server_mode protenix --sample 5 --cycle 3 --step 50
# Hot ColabFold cache (pre-warmed 2026-09-01).
#
#$ -N ta_ptx
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01/logs/protenix.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -l gpu_arch=hopper_h100
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
module load CUDA/12.1.1

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS

CC=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "")
case "$CC" in
    9.0|9.*)  export TORCH_CUDA_ARCH_LIST="9.0" ;;
    8.0|8.*)  export TORCH_CUDA_ARCH_LIST="8.0" ;;
    *)        export TORCH_CUDA_ARCH_LIST="8.0;9.0" ;;
esac

set -u
TIMING_DIR=${TIMING_DIR:-/hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01}
INPUT="$TIMING_DIR/inputs/protenix.json"
OUT_DIR="$TIMING_DIR/out_protenix"
TIME_FILE="$OUT_DIR/wall.time"
mkdir -p "$OUT_DIR"

PTX_VENV=${PTX_VENV:-/home/sengaad1/software/venvs/protenix}
source "$PTX_VENV/bin/activate"

echo "=== timing_protenix ==="
echo "JOB_ID: ${JOB_ID:-<none>}"
echo "HOST  : $(hostname)"
echo "GPU   : ${CUDA_VISIBLE_DEVICES:-<none>}  cc=$CC  arch=$TORCH_CUDA_ARCH_LIST"
nvidia-smi -L || true
which protenix
python3 --version

START_EPOCH=$(date +%s)
echo "START_EPOCH=$START_EPOCH" > "$TIME_FILE"

set +e
/usr/bin/time -v -o "$TIME_FILE.gnu" \
protenix pred \
    -i "$INPUT" \
    -o "$OUT_DIR" \
    --use_default_params True \
    --msa_server_mode protenix \
    --sample 5 --cycle 3 --step 50 \
    --seeds 42
EXIT=$?
set -e

END_EPOCH=$(date +%s)
WALL=$((END_EPOCH - START_EPOCH))
echo "END_EPOCH=$END_EPOCH" >> "$TIME_FILE"
echo "WALL_SEC=$WALL" >> "$TIME_FILE"
echo "EXIT=$EXIT" >> "$TIME_FILE"

echo ""
echo "=== protenix exit=$EXIT wall=${WALL}s ==="
cat "$TIME_FILE"

find "$OUT_DIR" -maxdepth 6 -name '*.cif' -printf '%p  %s bytes\n' 2>/dev/null | head -20

exit "$EXIT"
