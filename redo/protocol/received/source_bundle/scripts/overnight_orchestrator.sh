#!/bin/bash
# overnight_orchestrator.sh — autonomous phase manager for h100_pool
#
# Runs in a tmux session `orchestrator` on basel-hpc.
# Every 90s: reads queue_state.csv + filters, applies transition rules.
#
# Phase machine:
#   1. FAST3      — filter=boltz,chai (drain fast tail; skip protenix which
#                    is MSA-hung; save OF3 for later)
#   2. PROTENIX   — after FAST3 drains, try protenix rows one-at-a-time
#                    (limit to 3 concurrent so MSA server isn't hammered).
#                    Skip protenix ADRB2 rows if they've been retried and
#                    are still hanging past 20 min.
#   3. OF3        — after PROTENIX drains (or times out), all workers OF3
#   4. DONE       — all pending+claimed = 0 → write DONE marker; exit
#
# Also handles:
# - Restart workers that have exited (strict filter mismatch)
# - Reset "claimed" rows stuck > 30 min (whichever backbone) back to pending
# - Emit heartbeat every 5 min to log file
#
# Requires:  tmux session h100_pool with 12 windows w0..w11 already running qrsh

set -eu
POOL=/hpc/scratch/sengaad1/paper_af3/h100_pool
REPO=/home/sengaad1/paper_af3
LOG=$POOL/orchestrator.log
STATE=$POOL/queue_state.csv
MARKER=$POOL/DONE.marker

TICK_SEC=90
STUCK_MIN=30          # any single claim held >30min → reset row + kill worker
PROTENIX_MAX=3        # cap protenix concurrent workers to avoid MSA overload
HEARTBEAT_TICKS=4     # log heartbeat every N ticks

mkdir -p "$POOL"
touch "$LOG"

# Detect Python 3 with venv
source $REPO/../software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/openfold3/bin/activate

phase() {
    # Report current phase from marker file (or "FAST3" if none set)
    if [ -f "$POOL/phase.marker" ]; then
        cat "$POOL/phase.marker"
    else
        echo "FAST3"
    fi
}

set_phase() {
    echo "$1" > "$POOL/phase.marker"
    log "PHASE_TRANSITION → $1"
}

log() {
    echo "[$(date -u +%FT%TZ) orch] $*" | tee -a "$LOG"
}

read_state() {
    # Emit backbone × state counts on stdout, one per line: "bb state count"
    awk -F, 'NR>1 {print $2, $3}' "$STATE" | sort | uniq -c | \
        awk '{print $2, $3, $1}'
}

count() {
    # count "backbone" "state" — returns 0 if missing
    awk -v bb="$1" -v st="$2" -F, 'NR>1 && $2==bb && $3==st {c++} END{print c+0}' "$STATE"
}

count_state() {
    # count_state "state" — total across all backbones
    awk -v st="$1" -F, 'NR>1 && $3==st {c++} END{print c+0}' "$STATE"
}

set_all_filters() {
    # set_all_filters "boltz,chai" [strict]
    local content="$1"
    local strict="${2:-}"
    for i in 0 1 2 3 4 5 6 7 8 9 10 11; do
        if [ -n "$strict" ]; then
            printf '%s\nstrict\n' "$content" > "$POOL/filters/w$i.txt"
        else
            printf '%s\n' "$content" > "$POOL/filters/w$i.txt"
        fi
    done
    log "filters set to '$content' strict=$strict"
}

set_filter_range() {
    # set_filter_range from to "content" [strict]
    local from="$1" to="$2" content="$3"
    local strict="${4:-}"
    for i in $(seq "$from" "$to"); do
        if [ -n "$strict" ]; then
            printf '%s\nstrict\n' "$content" > "$POOL/filters/w$i.txt"
        else
            printf '%s\n' "$content" > "$POOL/filters/w$i.txt"
        fi
    done
    log "filters w$from..w$to set to '$content' strict=$strict"
}

restart_workers() {
    # send "bash h100_worker.sh wN" to each pane. Idempotent-ish.
    for i in 0 1 2 3 4 5 6 7 8 9 10 11; do
        tmux send-keys -t h100_pool:w$i \
            "bash $REPO/scripts/h100_worker.sh w$i" Enter
    done
    log "sent worker restart to all 12 panes"
}

reset_stuck_claimed() {
    # Reset rows where claimed_at > STUCK_MIN minutes ago → pending.
    # EXCEPT protenix: known-slow MSA server (ADRB2 cold cache); killing
    # loses queue position and warm-cache benefit for peer jobs. Use a
    # much longer threshold for protenix (240 min = 4h) — if truly wedged,
    # something else is wrong.
    python3 - <<PY
import csv, datetime, subprocess
now = datetime.datetime.now(datetime.timezone.utc)
threshold_default = $STUCK_MIN * 60
threshold_protenix = 240 * 60   # 4h for protenix
rows = list(csv.DictReader(open('$STATE')))
resets = []
for r in rows:
    if r['state'] != 'claimed': continue
    if not r['claimed_at']: continue
    try:
        t = datetime.datetime.fromisoformat(r['claimed_at'].replace('Z','+00:00'))
    except: continue
    elapsed = (now - t).total_seconds()
    thr = threshold_protenix if r['backbone'] == 'protenix' else threshold_default
    if elapsed > thr:
        resets.append((r['prediction_sha'], r['worker'], r['backbone'], elapsed/60))
for sha, wrkr, bb, mins in resets:
    subprocess.run(['python3', '$REPO/scripts/queue_ops.py', 'mark', sha,
                    'pending', '--reason', f'stuck>{mins:.0f}min ({bb})'],
                   check=False)
    print(f'RESET {wrkr} {bb} sha={sha[:12]} elapsed={mins:.0f}m')
    # Also send Ctrl-C to that worker's tmux pane
    if wrkr.startswith('w'):
        subprocess.run(['tmux', 'send-keys', '-t', f'h100_pool:{wrkr}', 'C-c'],
                       check=False)
PY
}

heartbeat_tick=0
log "orchestrator starting up (pid=$$)"
# Preserve existing phase marker across restarts. Only set FAST3 if no
# marker exists yet — otherwise we'd cascade FAST3→PROTENIX and reset
# in-flight protenix claims, losing MSA queue positions.
if [ ! -f "$POOL/phase.marker" ]; then
    log "no existing phase marker; initializing to FAST3"
    set_phase "FAST3"
else
    log "resuming from phase.marker: $(cat $POOL/phase.marker)"
fi

while true; do
    heartbeat_tick=$((heartbeat_tick + 1))

    # Read counts
    pending_boltz=$(count boltz pending)
    pending_chai=$(count chai pending)
    pending_protenix=$(count protenix pending)
    pending_of3=$(count of3 pending)
    claimed_boltz=$(count boltz claimed)
    claimed_chai=$(count chai claimed)
    claimed_protenix=$(count protenix claimed)
    claimed_of3=$(count of3 claimed)
    total_pending=$(count_state pending)
    total_claimed=$(count_state claimed)
    total_done=$(count_state done)
    total_failed=$(count_state failed)

    fast_remaining=$((pending_boltz + pending_chai + claimed_boltz + claimed_chai))
    p=$(phase)

    # heartbeat every N ticks
    if [ $((heartbeat_tick % HEARTBEAT_TICKS)) -eq 0 ]; then
        log "phase=$p done=$total_done fail=$total_failed pending=$total_pending claimed=$total_claimed | \
boltz=(p$pending_boltz c$claimed_boltz) chai=(p$pending_chai c$claimed_chai) \
prtx=(p$pending_protenix c$claimed_protenix) of3=(p$pending_of3 c$claimed_of3)"
    fi

    # Reset stuck rows every tick
    reset_stuck_claimed >> "$LOG" 2>&1

    # Phase machine
    case "$p" in
        FAST3)
            # Transition when boltz+chai fully done
            if [ "$fast_remaining" -eq 0 ]; then
                log "FAST3 done (boltz+chai fully drained)"
                # Reset any stale claimed protenix rows to pending
                awk -F, 'NR>1 && $2=="protenix" && $3=="claimed"{print $1}' "$STATE" | \
                    while read sha; do
                        python3 "$REPO/scripts/queue_ops.py" mark "$sha" pending \
                            --reason "reset for PROTENIX phase" 2>&1 | tail -1
                    done
                # Move to PROTENIX phase
                set_phase "PROTENIX"
                # Only 3 workers do protenix (limit MSA load), rest do OF3
                set_filter_range 0 2 "protenix" "strict"
                set_filter_range 3 11 "of3" "strict"
                restart_workers
            else
                # Restart any idle workers (strict filter → some may have exited)
                # Send restart to all — no-op for still-running workers
                restart_workers
            fi
            ;;
        PROTENIX)
            # Transition when protenix fully done OR protenix has been in this phase >1h
            protenix_remaining=$((pending_protenix + claimed_protenix))
            of3_remaining=$((pending_of3 + claimed_of3))
            if [ "$protenix_remaining" -eq 0 ] && [ "$of3_remaining" -eq 0 ]; then
                set_phase "DONE"
            elif [ "$protenix_remaining" -eq 0 ]; then
                # Protenix done, move everyone to OF3
                log "PROTENIX drained, all workers → OF3"
                set_phase "OF3"
                set_all_filters "of3" "strict"
                restart_workers
            elif [ "$of3_remaining" -eq 0 ] && [ "$protenix_remaining" -gt 0 ]; then
                # OF3 finished before protenix. Move OF3-filter workers to
                # protenix too — MSA cache should be warmer now that some
                # protenix ADRB2 rows have completed.
                log "OF3 drained during PROTENIX phase; moving w3..w11 to protenix filter"
                set_filter_range 3 11 "protenix" "strict"
                restart_workers
            fi
            # Keep restarting workers each tick
            restart_workers
            ;;
        OF3)
            of3_remaining=$((pending_of3 + claimed_of3))
            if [ "$of3_remaining" -eq 0 ]; then
                # OF3 done. Try leftover protenix if any
                if [ $((pending_protenix + claimed_protenix)) -gt 0 ]; then
                    log "OF3 done; final protenix cleanup"
                    set_phase "PROTENIX_FINAL"
                    set_all_filters "protenix" "strict"
                    restart_workers
                else
                    set_phase "DONE"
                fi
            fi
            restart_workers
            ;;
        PROTENIX_FINAL)
            if [ $((pending_protenix + claimed_protenix)) -eq 0 ]; then
                set_phase "DONE"
            fi
            restart_workers
            ;;
        DONE)
            if [ "$total_pending" -eq 0 ] && [ "$total_claimed" -eq 0 ]; then
                log "ALL WORK DONE — writing marker and exiting"
                echo "done=$total_done failed=$total_failed at=$(date -u +%FT%TZ)" > "$MARKER"
                break
            fi
            # Something crept back in — retry
            log "DONE-phase but queue not empty (pending=$total_pending claimed=$total_claimed); resuming"
            set_phase "OF3"
            ;;
    esac

    sleep $TICK_SEC
done

log "orchestrator exiting cleanly"
