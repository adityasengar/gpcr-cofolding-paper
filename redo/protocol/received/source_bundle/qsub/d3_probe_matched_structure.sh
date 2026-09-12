#!/bin/bash
# qsub/d3_probe_matched_structure.sh — matched-structure MSA-depth probe.
#
# Fires ONE prediction for one (backbone, depth) cell of the D3 propagation
# test. Called 8 times (4 backbones × 2 depths) from the parent launcher.
#
# Required env (via qsub -v):
#   BACKBONE     — boltz|chai|of3|protenix
#   RECEPTOR_SEQ — protein sequence
#   MSA_A3M_PATH — .a3m file (for the "full" arm this is the fetched full msa;
#                              for "depth8" this is the subsampled version)
#   PROBE_OUT_DIR — where to write the CIF (e.g. /hpc/scratch/.../probe/<bb>/<depth>/)
#   PROBE_NAME    — a name for the prediction (informational)
#   PROBE_SEED    — matched seed across depths (default 42)
#
# Notes:
# - The CHAI backbone reads MSAs via CHAI_MSA_DIRECTORY (dir of .aligned.pqt).
#   For chai the caller sets CHAI_MSA_DIRECTORY=<dir with the depth-specific
#   .aligned.pqt> and leaves MSA_A3M_PATH empty. Boltz/OF3/Protenix read
#   MSA_A3M_PATH directly (per D3 plumbing at commit b3863bd).
#$ -N d3_probe_matched
#$ -cwd
#$ -o d3_probe_matched.$JOB_ID.log
#$ -j y
#$ -l h_rt=01:30:00
#$ -l m_mem_free=16G
#$ -l gpu_card=1
#$ -l gpu_arch=hopper_h100
#$ -pe smp 4
set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL
set -u

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS || true

: "${BACKBONE:?BACKBONE required}"
: "${RECEPTOR_SEQ:?RECEPTOR_SEQ required}"
: "${PROBE_OUT_DIR:?PROBE_OUT_DIR required}"
: "${PROBE_NAME:=d3_probe_aa2ar}"
: "${PROBE_SEED:=42}"

mkdir -p "$PROBE_OUT_DIR"
# Chai's launcher asserts $PRED_OUT_DIR is empty at start — keep _input
# out of the tree.
INPUT_DIR="$(dirname "$PROBE_OUT_DIR")/_input_$(basename "$PROBE_OUT_DIR")_${BACKBONE}"
mkdir -p "$INPUT_DIR"

REPO=/home/sengaad1/paper_af3

# Materialize input file via scorer.propose emitter, passing msa_a3m_path.
# For chai we don't pass an msa_a3m_path — chai's MSA path is via
# CHAI_MSA_DIRECTORY (already exported by the caller).
CHAI_MSA_ARG=""
case "$BACKBONE" in
    boltz)
        INPUT_EXT="yaml"
        ;;
    chai)
        INPUT_EXT="fasta"
        ;;
    of3)
        INPUT_EXT="json"
        ;;
    protenix)
        INPUT_EXT="json"
        ;;
    *) echo "unknown BACKBONE=$BACKBONE" >&2; exit 2;;
esac

PRED_INPUT="$INPUT_DIR/${PROBE_NAME}.${INPUT_EXT}"

# scorer.propose imports pre_check → structure → gemmi. Use the shared
# openfold3 venv (has gemmi) just for the input-materialisation step.
# The per-backbone launcher will activate its own venv afterwards.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate

# Build input using scorer.propose helpers directly. Note: chai does not
# consume msa_a3m_path in the input; MSA comes from CHAI_MSA_DIRECTORY.
python3 -c "
import sys
sys.path.insert(0, '$REPO')
from scorer.propose import (_boltz_yaml_monomer, _of3_json_monomer,
                            _protenix_json_monomer, _chai_ligand_fasta)
seq = '$RECEPTOR_SEQ'
name = '$PROBE_NAME'
seed = int('$PROBE_SEED')
bb = '$BACKBONE'
msa = '${MSA_A3M_PATH:-}' or None
if bb == 'boltz':
    out = _boltz_yaml_monomer(seq, msa_a3m_path=msa)
elif bb == 'of3':
    out = _of3_json_monomer(name, seq, seed=seed, msa_a3m_path=msa)
elif bb == 'protenix':
    out = _protenix_json_monomer(name, seq, msa_a3m_path=msa)
elif bb == 'chai':
    # chai FASTA is trivial: query header + sequence
    out = f'>protein|name={name}\n{seq}\n'
else:
    raise SystemExit(f'unknown backbone {bb}')
with open('$PRED_INPUT', 'w') as f:
    f.write(out)
print(f'wrote $PRED_INPUT ({len(out)} bytes)')
"

# Fire the per-backbone launcher. It reads MSA_A3M_PATH from env.
export PRED_INPUT
export PRED_OUT_DIR="$PROBE_OUT_DIR"
export PRED_SEED="$PROBE_SEED"
export PRED_SAMPLES=1
export PRED_SIDECAR="$PROBE_OUT_DIR/_rerun_plan.json"

echo "[d3-probe] BACKBONE=$BACKBONE"
echo "[d3-probe] MSA_A3M_PATH=${MSA_A3M_PATH:-<unset>}"
echo "[d3-probe] CHAI_MSA_DIRECTORY=${CHAI_MSA_DIRECTORY:-<unset>}"
echo "[d3-probe] PROBE_OUT_DIR=$PROBE_OUT_DIR"

bash "$REPO/qsub/rerun_${BACKBONE}.sh"
