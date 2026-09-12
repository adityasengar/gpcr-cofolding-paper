#!/bin/bash
#$ -N opendde_bench_msa
#$ -cwd
#$ -o opendde_bench_msa.$JOB_ID.log
#$ -j y
#$ -l h_rt=04:00:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -l gpu_arch=hopper_h100
#$ -pe smp 8
set -eo pipefail
source /etc/profile
module purge
module use ~/software/modules
module load proxy/GLOBAL OpenDDE/1.1.1
set -u

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS || true

export OPENDDE_ROOT_DIR="${OPENDDE_ROOT_DIR:-/hpc/scratch/sengaad1/opendde}"

WORKDIR=/hpc/scratch/sengaad1/opendde_bench_gpcr_msa
mkdir -p "$WORKDIR/out"
cd "$WORKDIR"

echo "=== opendde pred (6 jobs, MSA ON, sample=1) ==="
time opendde pred \
  -i input.json \
  -o ./out \
  -n opendde_v1 \
  --use_msa true \
  --use_template false \
  --use_rna_msa false \
  --sample 1 \
  --step 200 \
  --cycle 10 2>&1 | tail -60

echo "=== outputs ==="
find ./out -maxdepth 6 -name '*.cif' -o -name '*summary*.json' | sort
echo "=== Done $(date) ==="
