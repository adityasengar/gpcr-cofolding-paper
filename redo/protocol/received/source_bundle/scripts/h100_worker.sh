#!/bin/bash
# h100_worker.sh — one instance per qrsh session in the h100_pool.
#
# Loop:
#   1. Atomically pop one pending row from queue via queue_ops.py.
#   2. eval the env-var assignments (PRED_INPUT, PRED_OUT_DIR, PRED_SEED,
#      PRED_SAMPLES, PRED_SIDECAR, BACKBONE, CLAIM_SHA).
#   3. Invoke the existing qsub template body inline
#      (bash /home/sengaad1/paper_af3/qsub/rerun_${BACKBONE}.sh). The template's
#      `#$ …` directives are ignored when bash-invoked; only the body runs.
#   4. Mark the row done (exit 0) or failed (non-zero) via queue_ops.py mark.
#   5. Loop until pop returns exit code 1 (queue empty), then exit cleanly.
#
# Usage:  bash h100_worker.sh <worker_id>
# Runs inside a qrsh -l gpu_card=1,gpu_arch=hopper_h100,h_rt=86400 shell.

set -o pipefail

WORKER_ID="${1:-w?}"
REPO=/home/sengaad1/paper_af3
POOL=/hpc/scratch/sengaad1/paper_af3/h100_pool
LOG="$POOL/logs/worker.$WORKER_ID.log"

mkdir -p "$POOL/logs"

log() {
    echo "[$(date -u +%FT%TZ) $WORKER_ID] $*" | tee -a "$LOG"
}

log "starting on $(hostname); CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-<unset>}"

# Activate the openfold3 venv — has all deps queue_ops.py needs (csv, fcntl are stdlib).
# The individual backbone qsub templates do their own venv activation for boltz/of3/etc.
source "$REPO/.venv/bin/activate" 2>/dev/null \
    || source /home/sengaad1/software/venvs/openfold3/bin/activate

while true; do
    EVAL_ENV=$(python3 "$REPO/scripts/queue_ops.py" pop "$WORKER_ID" 2>>"$LOG")
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

    # Defensive: retry rows may have stale content (partial CIFs,
    # sidecars from earlier failed attempts) that trip chai's
    # "output_dir must be empty" assertion. Purge everything inside
    # PRED_OUT_DIR before invoking the template. The template restores
    # its own sidecar afterwards if needed.
    find "$PRED_OUT_DIR" -mindepth 1 -delete 2>/dev/null || true

    # OF3-specific: OF3 refuses to reuse `colabfold_msas/raw` from a prior
    # run in the same qrsh session's /scratch/tmp/. Purge it.
    if [ "$BACKBONE" = "of3" ]; then
        rm -rf /scratch/tmp/*/of3-of-sengaad1/colabfold_msas/raw 2>/dev/null || true
    fi

    # Invoke the qsub template body. The template writes its own
    # _${BACKBONE}_status.json on exit and prints its own log lines,
    # so we don't need to redirect further — just capture exit code.
    (
        bash "$REPO/qsub/rerun_${BACKBONE}.sh"
    )
    JOB_RC=$?

    if [ $JOB_RC -eq 0 ]; then
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" done \
            --reason "worker-$WORKER_ID ok" >>"$LOG" 2>&1
        log "done sha=$CLAIM_SHA rc=0"
    else
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" failed \
            --reason "worker-$WORKER_ID rc=$JOB_RC" >>"$LOG" 2>&1
        log "failed sha=$CLAIM_SHA rc=$JOB_RC"
    fi
done

log "worker terminating cleanly"
