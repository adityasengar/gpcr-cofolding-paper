#!/bin/bash
# block_a_worker.sh — one instance per qrsh session in the block_a pool.
#
# Same loop as h100_worker.sh but:
#   1. Scorer-sync pre-flight: verify HPC scorer/*.py SHA256s match
#      refs/scorer_expected_shas.json (audit trail #11 regression class).
#      Abort loud on mismatch — cannot let a worker score with a drifted
#      scorer package.
#   2. Uses queue_ops.py against the block_a campaign pool
#      (not h100_pool). Pool root is passed via BLOCK_A_POOL env.
#
# Usage:  bash block_a_worker.sh <worker_id>
#         (run inside a qrsh session; BLOCK_A_POOL exported by caller.)

set -o pipefail

WORKER_ID="${1:-w?}"
REPO=/home/sengaad1/paper_af3
POOL="${BLOCK_A_POOL:-/hpc/scratch/sengaad1/paper_af3/block_a_campaign_2026_09_01}"
LOG="$POOL/logs/worker.$WORKER_ID.log"

mkdir -p "$POOL/logs"

log() {
    echo "[$(date -u +%FT%TZ) $WORKER_ID] $*" | tee -a "$LOG"
}

log "starting on $(hostname); pool=$POOL; CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-<unset>}"

# ---------------------------------------------------------------------
# Scorer-sync pre-flight (audit trail #11)
# ---------------------------------------------------------------------
EXPECTED="$REPO/refs/scorer_expected_shas.json"
if [ ! -f "$EXPECTED" ]; then
    log "ABORT: expected shas file missing at $EXPECTED"
    exit 3
fi

python3 <<'PY'
import hashlib, json, pathlib, sys
repo = pathlib.Path("/home/sengaad1/paper_af3")
expected = json.loads((repo / "refs/scorer_expected_shas.json").read_text())
mismatches = []
for rel, exp_hex in expected.items():
    p = repo / rel
    if not p.exists():
        mismatches.append(f"missing {rel}")
        continue
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got != exp_hex:
        mismatches.append(f"drift {rel}: expected {exp_hex[:12]} got {got[:12]}")
if mismatches:
    print("SCORER SYNC MISMATCH:", "; ".join(mismatches), file=sys.stderr)
    sys.exit(2)
print(f"scorer sync OK: {len(expected)}/{len(expected)} files match")
PY
if [ $? -ne 0 ]; then
    log "ABORT: scorer-sync pre-flight failed"
    exit 3
fi

log "scorer-sync pre-flight passed"

# Activate the openfold3 venv — has all deps queue_ops.py needs (csv, fcntl are stdlib).
source "$REPO/.venv/bin/activate" 2>/dev/null \
    || source /home/sengaad1/software/venvs/openfold3/bin/activate

# Chai MSA cache — cache mode is the only supported path (see audit trail #10).
export CHAI_MSA_DIRECTORY="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"

QUEUE_CSV="$POOL/queue.csv"
STATE_CSV="$POOL/queue_state.csv"

if [ ! -f "$QUEUE_CSV" ] || [ ! -f "$STATE_CSV" ]; then
    log "ABORT: queue.csv or queue_state.csv missing at $POOL"
    exit 4
fi

# ---------------------------------------------------------------------
# Main pop-run-mark loop
# ---------------------------------------------------------------------
while true; do
    EVAL_ENV=$(python3 "$REPO/scripts/queue_ops.py" pop "$WORKER_ID" \
        --state-csv "$STATE_CSV" --queue-csv "$QUEUE_CSV" 2>>"$LOG")
    RC=$?
    if [ $RC -eq 1 ]; then
        log "queue empty, exiting"
        break
    fi
    if [ $RC -ne 0 ]; then
        log "queue_ops.pop returned rc=$RC — aborting worker"
        exit $RC
    fi

    eval "$EVAL_ENV"
    log "claimed sha=$CLAIM_SHA backbone=$BACKBONE seed=$PRED_SEED samples=$PRED_SAMPLES"

    mkdir -p "$PRED_OUT_DIR"

    # Defensive: purge stale content in the output dir (chai's
    # "output_dir must be empty" assertion, etc.).
    find "$PRED_OUT_DIR" -mindepth 1 -delete 2>/dev/null || true

    # OF3: purge stale colabfold cache in this qrsh session's tmp.
    if [ "$BACKBONE" = "of3" ]; then
        rm -rf /scratch/tmp/*/of3-of-sengaad1/colabfold_msas/raw 2>/dev/null || true
    fi

    START_S=$(date +%s)
    (
        bash "$REPO/qsub/rerun_${BACKBONE}.sh"
    )
    JOB_RC=$?
    WALL_S=$(( $(date +%s) - START_S ))

    if [ $JOB_RC -eq 0 ]; then
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" done \
            --state-csv "$STATE_CSV" \
            --reason "worker-$WORKER_ID ok wall=${WALL_S}s" >>"$LOG" 2>&1
        log "done sha=$CLAIM_SHA rc=0 wall=${WALL_S}s"
    else
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" failed \
            --state-csv "$STATE_CSV" \
            --reason "worker-$WORKER_ID rc=$JOB_RC wall=${WALL_S}s" >>"$LOG" 2>&1
        log "failed sha=$CLAIM_SHA rc=$JOB_RC wall=${WALL_S}s"
    fi
done

log "worker terminating cleanly"
