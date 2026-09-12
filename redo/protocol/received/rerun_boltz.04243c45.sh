#!/bin/bash
#
# qsub/rerun_boltz.sh — M2.3 fresh Boltz-2 co-fold for one manifest row.
#
# Supervisor invokes via:
#   qsub -N pa3_boltz_<sha8> \
#        -v PRED_INPUT=<yaml>,PRED_OUT_DIR=<dir>,PRED_SEED=<int>,PRED_SIDECAR=<json> \
#        qsub/rerun_boltz.sh
#
# Env contract (all four are MANDATORY — script exits 1 if any is empty):
#   PRED_INPUT     absolute path to a Boltz-2 input.yaml
#   PRED_OUT_DIR   absolute path where Boltz output should land
#                  (supervisor creates parents; this script mkdir -p's leaves)
#   PRED_SEED      integer seed (deterministic, from fresh_seed_for)
#   PRED_SIDECAR   absolute path to the rerun-plan JSON the supervisor
#                  writes so this row can be traced back to its manifest
#                  origin at rescore time (M2.5)
#
# The venv layout follows the ``structure-prediction`` skill's basel-hpc
# section: /home/sengaad1/software/venvs/boltz/ has boltz + weights cache
# under $BOLTZ_CACHE (set below).
#
# Output survives even if the job dies mid-way: partial predictions are
# still useful to the supervisor's failure classifier.

#$ -N pa3_boltz_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rerun_boltz.$JOB_ID.log
#$ -j y
#$ -l h_rt=04:00:00
#$ -l m_mem_free=8G
#$ -l gpu_card=1                          # mandatory on default.q
#$ -pe smp 4

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL                  # colab MSA server + weights first-fetch

# CUDA_VISIBLE_DEVICES from SGE_HGR_gpu_card — GPU cgroup isolation is
# absent on basel-hpc, so relying on device 0 would race other jobs.
if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
    export SINGULARITYENV_CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
fi
unset OMP_NUM_THREADS
set -u

# ---- Env contract ---------------------------------------------------------

: "${PRED_INPUT:?PRED_INPUT is required (path to Boltz input.yaml)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required (destination dir)}"
: "${PRED_SEED:?PRED_SEED is required (integer seed)}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required (path to rerun plan JSON)}"

if [ ! -f "$PRED_INPUT" ]; then
    echo "FATAL: PRED_INPUT does not exist: $PRED_INPUT" >&2
    exit 1
fi

mkdir -p "$PRED_OUT_DIR"
mkdir -p "$(dirname "$PRED_SIDECAR")"

# ---- Venv + weights cache -------------------------------------------------

BOLTZ_VENV=${BOLTZ_VENV:-/home/sengaad1/software/venvs/boltz}
BOLTZ_CACHE=${BOLTZ_CACHE:-/hpc/scratch/sengaad1/boltz_cache}
mkdir -p "$BOLTZ_CACHE"

if [ ! -d "$BOLTZ_VENV" ]; then
    echo "FATAL: boltz venv not found at $BOLTZ_VENV" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$BOLTZ_VENV/bin/activate"

python3 --version
which boltz
nvidia-smi -L || true

# ---- Provenance -----------------------------------------------------------

# Write a compact per-job header so failed jobs are diagnosable purely
# from the .log without needing to open the sidecar JSON.
echo "=== M2.3 rerun_boltz ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "SIDECAR    : $PRED_SIDECAR"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo ""

# Copy the effective input alongside the output so the fresh run stays
# self-contained even if the source dir disappears.
cp -f "$PRED_INPUT" "$PRED_OUT_DIR/_input_used.$(basename "$PRED_INPUT")"

# ---- Run Boltz-2 ----------------------------------------------------------

# Flags match Boltz-2 upstream default (`sampling_steps=200`) — see
# PREREG §11a for the 50 vs 200 A/B on AA2AR (2026-09-01) that
# retained the tighter-tail 200-step config; wall time is identical
# (MSA-bound). recycling_steps=3, diffusion_samples=1 preserved.
# --seed is Boltz's own knob and takes precedence over any seed baked
# into the input YAML.

set +e
# `PRED_SAMPLES` is the diversity-study samples-per-seed multiplier.
# Default 1 preserves the historical single-sample-per-seed behaviour;
# analysts running the strategy-B (1 seed × N samples) branch of the
# diversity study set N via the propose YAML's `samples_per_seed:` field.
N_SAMPLES="${PRED_SAMPLES:-1}"
echo "PRED_SAMPLES=$N_SAMPLES"

boltz predict "$PRED_INPUT" \
    --out_dir "$PRED_OUT_DIR" \
    --use_msa_server \
    --cache "$BOLTZ_CACHE" \
    --devices 1 --accelerator gpu \
    --recycling_steps 3 --diffusion_samples "$N_SAMPLES" --sampling_steps 200 \
    --seed "$PRED_SEED"
EXIT=$?
set -e

echo ""
echo "=== boltz exit=$EXIT ==="

# ---- Post-run bookkeeping -------------------------------------------------

# Persist a machine-readable status marker so the supervisor's
# refs/rerun_status.csv poller can flip pending → done/failed without
# grepping the log.
STATUS_JSON="$PRED_OUT_DIR/_boltz_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, os, sys
from pathlib import Path

exit_code = int(sys.argv[1])
out_dir = Path(sys.argv[2])
seed = int(sys.argv[3])
status_path = Path(sys.argv[4])

# Discover produced cif/pdb files (Boltz emits under
# boltz_results_<name>/predictions/<name>/*.cif)
produced = []
for p in out_dir.rglob("*.cif"):
    produced.append(str(p))
for p in out_dir.rglob("*.pdb"):
    produced.append(str(p))

status = {
    "exit_code": exit_code,
    "seed": seed,
    "produced_files": sorted(produced),
    "n_produced": len(produced),
    "ok": exit_code == 0 and len(produced) > 0,
}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

# List what landed on disk so the supervisor's tail-check can find it
# via a single find(1) invocation later.
echo ""
echo "=== produced ==="
find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '*.pdb' -o -name '_boltz_status.json' \) -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
