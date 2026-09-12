#!/bin/bash
#
# qsub/supervisor_wrapper.sh — HPC-side auto-restart loop for the
# M2.4 supervisor.
#
# Runs the supervisor forever. If Python dies (OOM / uncaught exception /
# transient qstat blip that made it exit), restart after a short sleep.
# The loop only exits on:
#   - The MISSION_DONE_FLAG file (touch it to stop cleanly)
#   - SIGTERM / kill signal received via `kill $(pgrep -f supervisor_wrapper)`
#
# This is more resilient than session-based cron because the process lives
# on the HPC login node — it survives Claude Code session close.
#
# Usage:
#   nohup ~/paper_af3/qsub/supervisor_wrapper.sh &
#   disown -a
#
# Stop cleanly:
#   touch /hpc/scratch/sengaad1/paper_af3/MISSION_DONE_FLAG

set -eo pipefail

REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH=/hpc/scratch/sengaad1/paper_af3
LOGDIR=$SCRATCH/logs
MISSION_DONE_FLAG=$SCRATCH/MISSION_DONE_FLAG
WATCHDOG_LOG=$LOGDIR/supervisor_wrapper.log

mkdir -p "$LOGDIR"
: > "$WATCHDOG_LOG"   # truncate on start; use $WATCHDOG_LOG.<ts> archive
                       # per restart if we ever need history.

trap 'echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] wrapper caught SIGTERM, exiting" >> "$WATCHDOG_LOG"; exit 0' TERM

# One venv activation is enough — nohup keeps env sticky across restarts.
# shellcheck source=/dev/null
source /home/sengaad1/software/venvs/openfold3/bin/activate

restart_count=0
while true; do
    if [ -f "$MISSION_DONE_FLAG" ]; then
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] MISSION_DONE_FLAG present, exiting cleanly" >> "$WATCHDOG_LOG"
        exit 0
    fi

    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    log_this_run="$LOGDIR/supervisor_full.$(date -u +%s).log"

    echo "[$ts] starting supervisor (attempt #$((restart_count + 1))) — log=$log_this_run" >> "$WATCHDOG_LOG"

    # The supervisor exits 0 when all rows are done/failed (its own
    # run_forever "no more work" branch). Anything else = crash.
    set +e
    python3 -m scorer.supervisor \
        --manifest "$REPO/refs/rerun_manifest.csv" \
        --status   "$REPO/refs/rerun_status.csv" \
        --rerun-root "$SCRATCH/rerun" \
        --rewrite-cache "$SCRATCH/rerun/_input_rewrites" \
        --repo-root "$REPO" \
        --log-dir "$LOGDIR" \
        --backbone boltz --backbone of3 --backbone protenix --backbone chai --backbone af2mm \
        --max-concurrent 25 --max-submit-per-tick 8 \
        --h100-arch-selector 'gpu_arch=hopper_h100' \
        --h100-arch-value 'hopper_h100' \
        --poll-seconds 60 \
        > "$log_this_run" 2>&1
    exit_code=$?
    set -e

    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "[$ts] supervisor exited $exit_code — tail of $log_this_run:" >> "$WATCHDOG_LOG"
    tail -20 "$log_this_run" >> "$WATCHDOG_LOG" 2>/dev/null || true
    echo "---" >> "$WATCHDOG_LOG"

    if [ "$exit_code" -eq 0 ]; then
        # Clean exit — supervisor's own "no more work" branch. This is
        # the M2.4-complete case; leave the flag as a sentinel.
        echo "[$ts] supervisor reported no more work — mission done" >> "$WATCHDOG_LOG"
        touch "$MISSION_DONE_FLAG"
        exit 0
    fi

    restart_count=$((restart_count + 1))

    # Escalating backoff: 30s / 90s / 180s / 300s cap. Never exceed 5 min
    # between restarts — the supervisor is cheap to start and job
    # submissions can't wait longer than that or we lose GPU-h.
    case "$restart_count" in
        1)   sleep 30 ;;
        2)   sleep 90 ;;
        3)   sleep 180 ;;
        *)   sleep 300 ;;
    esac

    # Reset the restart_count if the previous run was long-lived so we
    # never permanently degrade the backoff to 5-min. "Long-lived" = the
    # log file grew larger than 100KB, which for the supervisor's own
    # per-tick JSON output means ≥ ~200 ticks ≈ 3+ hours of successful
    # operation.
    if [ -f "$log_this_run" ] && [ "$(stat -c '%s' "$log_this_run" 2>/dev/null || echo 0)" -gt 100000 ]; then
        restart_count=0
    fi
done
