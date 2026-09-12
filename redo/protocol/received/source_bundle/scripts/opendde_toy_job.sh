#!/bin/bash
#$ -N opendde_toy
#$ -cwd
#$ -o opendde_toy.$JOB_ID.log
#$ -j y
#$ -l h_rt=01:00:00
#$ -l m_mem_free=4G
#$ -l gpu_card=1
#$ -pe smp 4
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

# Where checkpoints and common assets live (set by the modulefile)
export OPENDDE_ROOT_DIR="${OPENDDE_ROOT_DIR:-/hpc/scratch/sengaad1/opendde}"
mkdir -p "$OPENDDE_ROOT_DIR"

WORKDIR=/hpc/scratch/sengaad1/opendde_toy
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Ubiquitin (76 AA, benchmark-grade well-folded reference)
cat > ubq.json <<'JSON'
[
  {
    "name": "ubiquitin",
    "modelSeeds": [101],
    "sequences": [
      {
        "proteinChain": {
          "sequence": "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG",
          "count": 1
        }
      }
    ]
  }
]
JSON

echo "=== opendde doctor ==="
opendde doctor 2>&1 | head -30 || true

echo "=== opendde pred (ubiquitin, MSA off, templates off) ==="
time opendde pred \
  -i ubq.json \
  -o ./out \
  -n opendde_v1 \
  --use_msa false \
  --use_template false \
  --use_rna_msa false \
  --sample 1 \
  --step 200 \
  --cycle 10

echo "=== outputs ==="
find ./out -maxdepth 5 -type f | head -30
echo "=== summary confidence (if present) ==="
find ./out -name '*summary*.json' -exec echo {} \; -exec head -c 4096 {} \;
echo "=== Done $(date) ==="
