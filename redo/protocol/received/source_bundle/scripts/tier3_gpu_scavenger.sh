#!/bin/bash
#
# scripts/tier3_gpu_scavenger.sh — Block C Tier 3 elastic H100 pool grower.
#
# Every 30 minutes:
#   1. Query `qhost -F gpu_arch,gpu_card` for hopper_h100 hosts with a free
#      gpu_card slot.
#   2. Count H100 workers currently held by this user in the primary
#      Tier 3 tmux pool ($POOL_NAME).
#   3. If holdings < 30 (contract §6 cap), grab up to
#      `min(new_available, 30 - holdings)` additional qrsh workers,
#      each in a fresh tmux window `w<N>`.
#
# Runs in its own tmux session `tier3_scavenger`. Never voluntarily
# releases workers — h_rt=24:00:00 leases held until scheduler evicts.
#
# All grabbed workers pull from the same shared queue as the initial
# 25 launched by dispatch_tier3.sh — no separate retry pool (coordinator
# revision 2026-09-04).
#
# Idempotent: safe to run multiple times; grows only when there's slack
# between current holdings and the 30 cap.

set -o pipefail

POOL_NAME="${POOL_NAME:-block_c_tier3_2026_09_04}"
BLOCK_C_TIER3_POOL="${BLOCK_C_TIER3_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_b_worker.sh"
H_RT="${H_RT:-24:00:00}"
CHAI_MSA="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"
H100_CAP="${H100_CAP:-30}"
POLL_SEC="${POLL_SEC:-1800}"

LOG="$BLOCK_C_TIER3_POOL/logs/scavenger.log"
mkdir -p "$(dirname "$LOG")"

log() { echo "[$(date -u +%FT%TZ) scavenger] $*" | tee -a "$LOG"; }

log "starting; H100 cap=$H100_CAP, poll every ${POLL_SEC}s, target pool=$POOL_NAME"

# The tmux window index counter must be preserved across cycles — start
# from the max existing window index + 1 for this session.
_max_win() {
    tmux list-windows -t "$POOL_NAME" -F '#I' 2>/dev/null | sort -n | tail -1
}

QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G -v BLOCK_B_POOL,CHAI_MSA_DIRECTORY,BACKBONE_POOL_TIER"
ENV_EXPORT_H100="export BLOCK_B_POOL='$BLOCK_C_TIER3_POOL' && export CHAI_MSA_DIRECTORY='$CHAI_MSA' && export BACKBONE_POOL_TIER='h100_any'"

while true; do
    if ! tmux has-session -t "$POOL_NAME" 2>/dev/null; then
        log "primary session $POOL_NAME gone — exiting"
        exit 0
    fi

    # Count H100 workers held (state==r AND queue matches gpu_arch=hopper_h100)
    # A per-tmux-window count is a good proxy — every qrsh started by
    # dispatch_tier3.sh or by a prior scavenger cycle lives in one window
    # of $POOL_NAME.
    held=$(tmux list-windows -t "$POOL_NAME" 2>/dev/null | wc -l)
    held=${held:-0}

    # Query cluster for hopper_h100 hosts and count total advertised slots.
    # Each qhost -F entry represents one gpu_card advertisement; free slots
    # need qstat cross-check but for elastic grow behavior we can rely on
    # SGE's own scheduling to accept-or-reject the qrsh.
    avail=$(qhost -F gpu_arch,gpu_card 2>/dev/null | grep -c hopper_h100)
    avail=${avail:-0}

    target=$((H100_CAP - held))
    if [ "$target" -le 0 ]; then
        log "at cap: held=$held ≥ cap=$H100_CAP; sleeping"
    elif [ "$avail" -le 0 ]; then
        log "no H100 slots advertised; held=$held/$H100_CAP; sleeping"
    else
        grab=$target
        [ "$avail" -lt "$grab" ] && grab=$avail
        log "cycle: held=$held avail=$avail grab=$grab (cap=$H100_CAP)"

        base=$(_max_win)
        base=${base:-0}
        for i in $(seq 1 "$grab"); do
            idx=$((base + i))
            name="w${idx}"
            tmux new-window -t "$POOL_NAME" -n "$name" 2>/dev/null || {
                log "tmux new-window failed for $name — abandoning cycle"
                break
            }
            tmux send-keys -t "$POOL_NAME:$name" \
                "$ENV_EXPORT_H100 && $QRSH_H100 bash $WORKER $name" Enter
            log "  spawned window $name (attempt to qrsh)"
        done
    fi

    sleep "$POLL_SEC"
done
