#!/bin/bash
#
# qsub/verify_drd2_msa_cache.sh — one-off cache-mode verify for Chai.
#
# Reproduces the DRD2+Gαi+dopamine pilot (5 seeds × 5 samples) using
# `--msa-directory` against the pre-built `.aligned.pqt` cache at
# /hpc/scratch/sengaad1/paper_af3/msa_cache/chai/  — instead of the
# pilot's `--use-msa-server` live ColabFold path.
#
# If the mean d_tm6 lands within pilot's 8.41 ± 3σ = [6.07, 10.75] Å,
# the Block A dispatch's cache-backed Chai path is validated. If it
# drifts (e.g. lands at ~18 Å like AA2AR/ADRB2 did), we have a silent-
# fallback or featurizer-shape bug to root-cause BEFORE Block A goes.
#
# Env contract (mirrors rerun_chai.sh):
#   PRED_INPUT     path to Chai FASTA (drd2 + alphai1 + dopamine)
#   PRED_OUT_DIR   scratch chai/seed_XXXX/ folder
#   PRED_SEED      integer seed (use pilot's 5)
#   PRED_SIDECAR   path to _rerun_plan.json (any placeholder; provenance
#                  lift walks it up during rescore)
#   PRED_SAMPLES   defaults to 5 (matches pilot)
#
# Fixed to --msa-directory=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai.
# No --use-msa-server, no chai_patched_wrapper.py monkey-patch (the
# patch's only purpose is proxy-timeout handling on the ColabFold path,
# which cache mode doesn't hit).

#$ -N pa3_chai_verify
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/verify_drd2_msa_cache.$JOB_ID.log
#$ -j y
#$ -l h_rt=01:30:00
#$ -l m_mem_free=8G
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

: "${PRED_INPUT:?PRED_INPUT is required (path to Chai FASTA)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required}"
: "${PRED_SEED:?PRED_SEED is required}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required}"

[ -f "$PRED_INPUT" ] || { echo "FATAL: PRED_INPUT missing: $PRED_INPUT" >&2; exit 1; }

MSA_DIR=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai
[ -d "$MSA_DIR" ] || { echo "FATAL: MSA cache dir missing: $MSA_DIR" >&2; exit 1; }

mkdir -p "$PRED_OUT_DIR" "$(dirname "$PRED_SIDECAR")"

CHAI_VENV=${CHAI_VENV:-/home/sengaad1/software/venvs/chai1}
if [ ! -d "$CHAI_VENV" ]; then
    echo "FATAL: chai venv not found at $CHAI_VENV" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$CHAI_VENV/bin/activate"

python3 --version
which chai-lab 2>/dev/null || echo "warn: chai-lab not on PATH"
nvidia-smi -L || true

echo "=== verify_drd2_msa_cache ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "MSA_DIR    : $MSA_DIR"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo ""

# chai-lab fold asserts `not any(output_dir.iterdir())`. Move the
# supervisor-written sidecar out of PRED_OUT_DIR for the fold, restore
# after so `_lift_provenance_from_sidecar` finds it during rescore.
META_DIR="$(dirname "$PRED_OUT_DIR")/_meta"
mkdir -p "$META_DIR"
cp -f "$PRED_INPUT" "$META_DIR/_input_used.$(basename "$PRED_INPUT")"

STASH_NAME="_rerun_plan.$(basename "$PRED_OUT_DIR").json"
STASHED_SIDECAR="$(dirname "$PRED_OUT_DIR")/$STASH_NAME"
if [ -f "$PRED_OUT_DIR/_rerun_plan.json" ]; then
    mv "$PRED_OUT_DIR/_rerun_plan.json" "$STASHED_SIDECAR"
fi

set +e
N_SAMPLES="${PRED_SAMPLES:-5}"
echo "PRED_SAMPLES=$N_SAMPLES"
echo "MSA         : --msa-directory $MSA_DIR  (cache mode; no ColabFold)"

chai-lab fold \
    "$PRED_INPUT" \
    "$PRED_OUT_DIR" \
    --msa-directory "$MSA_DIR" \
    --seed "$PRED_SEED" \
    --num-trunk-recycles 3 \
    --num-diffn-timesteps 50 \
    --num-diffn-samples "$N_SAMPLES"
EXIT=$?
set -e

echo ""
echo "=== chai exit=$EXIT ==="

if [ -f "$STASHED_SIDECAR" ]; then
    mkdir -p "$PRED_OUT_DIR"
    mv "$STASHED_SIDECAR" "$PRED_OUT_DIR/_rerun_plan.json"
fi

STATUS_JSON="$PRED_OUT_DIR/_chai_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, sys
from pathlib import Path
exit_code = int(sys.argv[1]); out_dir = Path(sys.argv[2])
seed = int(sys.argv[3]); status_path = Path(sys.argv[4])
produced = sorted(str(p) for p in list(out_dir.rglob("*.cif")) + list(out_dir.rglob("*.pdb")))
status = {"backbone": "chai", "exit_code": exit_code, "seed": seed,
          "produced_files": produced, "n_produced": len(produced),
          "ok": exit_code == 0 and len(produced) > 0}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '*.pdb' -o -name '_chai_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
