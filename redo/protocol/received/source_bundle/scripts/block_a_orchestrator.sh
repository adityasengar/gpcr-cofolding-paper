#!/bin/bash
# block_a_orchestrator.sh — autonomous supervisor for the Block A campaign.
#
# Runs in an HPC tmux window. Loops:
#   1. Every 2 min, read queue_state.csv counts.
#   2. If pending+claimed == 0 → drain complete; exit into Phase 5.
#   3. If no qrsh workers alive but queue has pending → auto-relaunch pool.
#   4. If failure rate > 5% in a rolling window → stop and log.
#   5. Otherwise sleep.
#
# On drain complete:
#   - Reset any zombie 'claimed' rows to 'failed' (they never got mark).
#   - Run rescore over the whole slug via manifest mode.
#   - Compute primary result + per-class summaries.
#   - Render campaign_completion_report.md.
#   - Write DONE marker so a caller knows to commit + tag.
#
# Idempotent: safe to relaunch. Refuses if a prior orchestrator is running
# by checking /hpc/scratch/.../.orchestrator.pid.
#
# Usage (on basel-hpc):
#   tmux new-session -d -s block_a_orch 'bash scripts/block_a_orchestrator.sh'

set -o pipefail

POOL="${BLOCK_A_POOL:-/hpc/scratch/sengaad1/paper_af3/block_a_campaign_2026_09_01}"
REPO=/home/sengaad1/paper_af3
STATE="$POOL/queue_state.csv"
QUEUE="$POOL/queue.csv"
LOG_DIR="$POOL/logs"
LOG="$LOG_DIR/orchestrator.log"
PID_FILE="$POOL/.orchestrator.pid"
DONE_MARKER="$POOL/DRAIN_COMPLETE.marker"
FAIL_MARKER="$POOL/FAILURE_LIMIT_EXCEEDED.marker"
POLL_S=120
MAX_FAIL_RATE_PCT=5

log() { echo "[$(date -u +%FT%TZ) orch] $*" | tee -a "$LOG"; }

# ---------------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------------
mkdir -p "$LOG_DIR"

if [ -f "$PID_FILE" ]; then
    old=$(cat "$PID_FILE")
    if kill -0 "$old" 2>/dev/null; then
        log "ABORT: orchestrator pid $old already running"
        exit 2
    fi
fi
echo $$ > "$PID_FILE"

if [ -f "$DONE_MARKER" ]; then
    log "DRAIN_COMPLETE.marker already exists — nothing to do (last drain: $(cat $DONE_MARKER))"
    exit 0
fi

log "orchestrator starting pid=$$ pool=$POOL"

# ---------------------------------------------------------------------
# Poll loop
# ---------------------------------------------------------------------
LAST_DONE=0
NO_WORKER_STRIKES=0

while true; do
    if [ ! -f "$STATE" ]; then
        log "state.csv missing at $STATE; sleeping"
        sleep "$POLL_S"; continue
    fi

    read done pending claimed failed paused < <(awk -F, '
        NR>1 {c[$3]++}
        END {print c["done"]+0, c["pending"]+0, c["claimed"]+0, c["failed"]+0, c["paused"]+0}
    ' "$STATE")

    alive=$(qstat -u sengaad1 2>/dev/null | grep -c ' r ')

    log "state: done=$done pending=$pending claimed=$claimed failed=$failed paused=$paused | qrsh_alive=$alive"

    # --- Terminal condition: drain complete ---
    if [ $((pending + claimed + paused)) -eq 0 ]; then
        log "DRAIN COMPLETE: done=$done failed=$failed"
        break
    fi

    # --- Failure rate check (over the completed subset only) ---
    completed=$((done + failed))
    if [ $completed -gt 100 ]; then
        pct=$((failed * 100 / completed))
        if [ $pct -gt $MAX_FAIL_RATE_PCT ]; then
            log "FAIL RATE $pct% > $MAX_FAIL_RATE_PCT% — STOPPING pool"
            tmux kill-session -t block_a_pool_2026_09_01 2>/dev/null || true
            echo "$(date -u +%FT%TZ) failure_rate=$pct% failed=$failed completed=$completed" > "$FAIL_MARKER"
            exit 1
        fi
    fi

    # --- Tail-drain zombie-claim reset: workers that die AFTER popping
    # but BEFORE writing a status.json leave rows stuck at `claimed`
    # forever. Heuristic: if claimed_count > qrsh_alive_count, at least
    # (claimed - alive) rows have no live owner. Reset ALL stale claims
    # (not just the delta — we can't tell which are which, but the pool
    # will just re-pop them, and idempotent scoring means no harm even
    # if a live one gets reset alongside). ---
    if [ $claimed -gt $alive ] && [ $((pending + claimed)) -gt 0 ]; then
        log "orphan-claim reset: claimed=$claimed > alive=$alive; resetting claimed -> pending"
        python3 "$REPO/scripts/queue_ops.py" bulk_transition \
            --from-state claimed --to-state pending \
            --state-csv "$STATE" --queue-csv "$QUEUE" \
            --reason "orch orphan-claim reset (alive=$alive)" >> "$LOG" 2>&1 || true
        # Refresh counts for the kick gate below
        read done pending claimed failed paused < <(awk -F, '
            NR>1 {c[$3]++}
            END {print c["done"]+0, c["pending"]+0, c["claimed"]+0, c["failed"]+0, c["paused"]+0}
        ' "$STATE")
    fi

    # --- Per-window idle detection: any tmux pane sitting at a login
    # shell prompt while queue has pending or claimed work is a dead
    # worker whose qrsh dropped without a clean exit. Kick each idle
    # window back into a fresh qrsh + worker. Cheap: happens once every
    # POLL_S. Gate is (pending + claimed) — during tail-drain we may
    # have pending==0 but claimed>0 orphans; the reset above turns them
    # into pending, but we still need to relaunch workers. ---
    if [ $((pending + claimed)) -gt 0 ] && tmux has-session -t block_a_pool_2026_09_01 2>/dev/null; then
        for w in $(tmux list-windows -t block_a_pool_2026_09_01 -F '#W' 2>/dev/null); do
            last=$(tmux capture-pane -t block_a_pool_2026_09_01:$w -p 2>/dev/null | tail -1)
            if echo "$last" | grep -q 'paper_af3\]\$'; then
                idx=${w#w}
                if [ "$idx" -lt 17 ] 2>/dev/null; then
                    arch=hopper_h100
                else
                    arch=ampere_a100_sxm4
                fi
                log "per-window kick: $w idle at login shell; relaunching qrsh gpu_arch=$arch"
                tmux send-keys -t block_a_pool_2026_09_01:$w \
                    "export BLOCK_A_POOL='$POOL' && qrsh -q default.q -l h_rt=48:00:00,gpu_card=1,gpu_arch=$arch,m_mem_free=32G bash $REPO/scripts/block_a_worker.sh $w" Enter
            fi
        done
    fi

    # --- Auto-relaunch pool if workers dead but queue has work ---
    if [ $alive -eq 0 ] && [ $((pending + claimed)) -gt 0 ]; then
        NO_WORKER_STRIKES=$((NO_WORKER_STRIKES + 1))
        if [ $NO_WORKER_STRIKES -ge 2 ]; then
            log "auto-relaunching pool (no qrsh workers, queue has $pending pending)"
            # Reset any zombie claims to pending first
            python3 "$REPO/scripts/queue_ops.py" bulk_transition \
                --from-state claimed --to-state pending \
                --state-csv "$STATE" --queue-csv "$QUEUE" \
                --reason "orchestrator zombie-reset" >> "$LOG" 2>&1 || true
            tmux kill-session -t block_a_pool_2026_09_01 2>/dev/null || true
            sleep 5
            bash "$REPO/scripts/launch_block_a_pool.sh" >> "$LOG" 2>&1
            NO_WORKER_STRIKES=0
        fi
    else
        NO_WORKER_STRIKES=0
    fi

    sleep "$POLL_S"
done

# ---------------------------------------------------------------------
# Phase 5: rescore + reports
# ---------------------------------------------------------------------
log "Phase 5 starting: rescore + reports"
cd "$REPO"
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || true

# Zombie claims → failed (if any)
python3 scripts/queue_ops.py bulk_transition \
    --from-state claimed --to-state failed \
    --state-csv "$STATE" --queue-csv "$QUEUE" \
    --reason "orchestrator drain-finalise" >> "$LOG" 2>&1 || true

# Full rescore over the reorganised slug
rm -f experiments/018_block_a_switch_test/analysis/rows.csv.sha256
python3 scripts/rescore_experiment.py \
    --slug 018_block_a_switch_test \
    --manifest experiments/018_block_a_switch_test/runs/initial/manifest.csv \
    2>&1 | tee -a "$LOG"

# Primary result + per-class summaries
python3 scripts/compute_block_a_primary_result.py \
    --slug 018_block_a_switch_test 2>&1 | tee -a "$LOG"

# Campaign completion report
python3 scripts/render_campaign_completion_report.py \
    --slug 018_block_a_switch_test 2>&1 | tee -a "$LOG"

# DONE marker: consumer commits + tags
echo "$(date -u +%FT%TZ)" > "$DONE_MARKER"
log "Phase 5 complete. DRAIN_COMPLETE.marker written."
