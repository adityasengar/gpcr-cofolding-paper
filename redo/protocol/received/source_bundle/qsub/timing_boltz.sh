#!/bin/bash
# qsub/timing_boltz.sh — one-off Block-A canonical-settings timing on H100.
# Canonical settings: --use_msa_server --recycling_steps 3 --diffusion_samples 5 --sampling_steps 200
# Hot MSA cache (ColabFold pre-warmed 2026-09-01).
#
# Submit: qsub -v TIMING_DIR=<dir> qsub/timing_boltz.sh
#
#$ -N ta_boltz
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01/logs/boltz.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=8G
#$ -l gpu_card=1
#$ -l gpu_arch=hopper_h100
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

TIMING_DIR=${TIMING_DIR:-/hpc/scratch/sengaad1/paper_af3/experiments/timing_h100_2026_09_01}
INPUT="$TIMING_DIR/inputs/boltz.yaml"
OUT_DIR="$TIMING_DIR/out_boltz"
TIME_FILE="$OUT_DIR/wall.time"
mkdir -p "$OUT_DIR"

BOLTZ_VENV=${BOLTZ_VENV:-/home/sengaad1/software/venvs/boltz}
BOLTZ_CACHE=${BOLTZ_CACHE:-/hpc/scratch/sengaad1/boltz_cache}
mkdir -p "$BOLTZ_CACHE"
source "$BOLTZ_VENV/bin/activate"

echo "=== timing_boltz ==="
echo "JOB_ID: ${JOB_ID:-<none>}"
echo "HOST  : $(hostname)"
echo "GPU   : ${CUDA_VISIBLE_DEVICES:-<none>}"
nvidia-smi -L || true
which boltz
python3 --version

START_EPOCH=$(date +%s)
echo "START_EPOCH=$START_EPOCH" > "$TIME_FILE"

set +e
/usr/bin/time -v -o "$TIME_FILE.gnu" \
boltz predict "$INPUT" \
    --out_dir "$OUT_DIR" \
    --use_msa_server \
    --cache "$BOLTZ_CACHE" \
    --devices 1 --accelerator gpu \
    --recycling_steps 3 --diffusion_samples 5 --sampling_steps 200 \
    --seed 42
EXIT=$?
set -e

END_EPOCH=$(date +%s)
WALL=$((END_EPOCH - START_EPOCH))
echo "END_EPOCH=$END_EPOCH" >> "$TIME_FILE"
echo "WALL_SEC=$WALL" >> "$TIME_FILE"
echo "EXIT=$EXIT" >> "$TIME_FILE"

echo ""
echo "=== boltz exit=$EXIT wall=${WALL}s ==="
cat "$TIME_FILE"

find "$OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '*.pdb' \) -printf '%p  %s bytes\n' 2>/dev/null | head -20

exit "$EXIT"
