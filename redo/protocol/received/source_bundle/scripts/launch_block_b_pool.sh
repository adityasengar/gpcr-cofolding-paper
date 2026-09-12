#!/bin/bash
# launch_block_b_pool.sh — set up the 20-window tmux session with one
# qrsh worker per window (10 H100 + 10 A100) for Block B Wide dispatch.
#
# Runs from a login node. Creates tmux session $POOL_NAME with:
#   w0..w9   → H100 qrsh (10 windows; w7-w9 reserved for big-Chai FSHR/LSHR)
#   w10..w19 → A100 qrsh (10 windows)
#
# Each qrsh runs block_b_worker.sh which loops popping from
# $BLOCK_B_POOL/queue_state.csv until empty.
#
# Big-Chai routing (audit #1: FSHR + LSHR >1000 aa, OOM on A100):
#   pre-emptive pin via queue_ops.py bulk_transition (pausing FSHR chai
#   and LSHR chai rows) is done BEFORE this launcher runs. After
#   workers attach, w7/w8/w9 get filter files (chai\nstrict) and the
#   FSHR/LSHR chai rows get unpaused so only those three workers can
#   claim them.
#
# Idempotent-refuse: refuses to run if $POOL_NAME already exists.
#
# Usage:   bash launch_block_b_pool.sh
#          (verifies scorer-sync locally before spawning any worker)
#
# Adapted from scripts/launch_block_a_pool.sh (Block A campaign,
# 2026-09-01) — same tmux+send-keys pattern that Block A proved works.

set -o pipefail

POOL_NAME="${POOL_NAME:-block_b_pool_2026_09_02}"
BLOCK_B_POOL="${BLOCK_B_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection/pool}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_b_worker.sh"

N_H100="${N_H100:-10}"      # 10 H100 workers (w0-w9; w7-w9 reserved for big-Chai)
N_A100="${N_A100:-10}"      # 10 A100 workers (w10-w19)
H_RT="${H_RT:-24:00:00}"    # 24 h per user 2026-09-02 green-light spec

log() { echo "[$(date -u +%FT%TZ) launcher] $*"; }

# 1. Pre-flight: queue.csv + state.csv must exist
for f in "$BLOCK_B_POOL/queue.csv" "$BLOCK_B_POOL/queue_state.csv"; do
    if [ ! -f "$f" ]; then
        log "ABORT: missing $f — run build_block_b_campaign_queue.py first"
        exit 2
    fi
done

# 2. Pre-flight: scorer-sync on the login node itself (workers do this
#    again on the compute node, but catching it here is cheaper).
python3 <<'PY'
import hashlib, json, pathlib, sys
repo = pathlib.Path("/home/sengaad1/paper_af3")
expected = json.loads((repo / "refs/scorer_expected_shas.json").read_text())
bad = []
for rel, exp_hex in expected.items():
    got = hashlib.sha256((repo / rel).read_bytes()).hexdigest()
    if got != exp_hex:
        bad.append(f"{rel}: expected {exp_hex[:12]} got {got[:12]}")
if bad:
    print("SCORER SYNC MISMATCH:", "; ".join(bad), file=sys.stderr)
    sys.exit(1)
print(f"scorer sync OK: {len(expected)}/{len(expected)} files match")
PY
if [ $? -ne 0 ]; then
    log "ABORT: scorer-sync check failed"
    exit 3
fi

# 3. Refuse if session already exists
if tmux has-session -t "$POOL_NAME" 2>/dev/null; then
    log "ABORT: tmux session '$POOL_NAME' already exists. Kill it with 'tmux kill-session -t $POOL_NAME' or use a different POOL_NAME."
    exit 4
fi

log "creating tmux session $POOL_NAME with $N_H100 H100 + $N_A100 A100 workers"
log "pool root: $BLOCK_B_POOL"

# 4. Build the session
# m_mem_free=32G: OF3/protenix use 15-25GB residual + cgroup headroom;
# the site default cgroup cap is 4GB and killed 24 of 25 workers on Block A's
# first launch (exit 129 / cgroups_enforced_memory_limit).
# UGE gotcha (verified 2026-09-02): qrsh does NOT forward exported env vars
# to the compute node by default (unlike qsub). Must explicitly `-v BLOCK_B_POOL`.
# Block A's launcher lacked this flag and worked only because the worker script's
# hardcoded fallback default happened to equal Block A's real pool path (silent
# no-op). Block B's fallback default was originally stale (relocated pool path),
# so the bug surfaced — patched here as the authoritative fix, plus a corrected
# fallback default in block_b_worker.sh as belt-and-suspenders.
QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G -v BLOCK_B_POOL"
QRSH_A100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=ampere_a100_sxm4,m_mem_free=32G -v BLOCK_B_POOL"
ENV_EXPORT="export BLOCK_B_POOL='$BLOCK_B_POOL'"

# Window 0 = first H100
tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w0" Enter

# Remaining H100 windows (w1..w9)
for i in $(seq 1 $((N_H100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w$i" Enter
done

# A100 windows (w10..w19)
for i in $(seq $N_H100 $((N_H100 + N_A100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_A100 bash $WORKER w$i" Enter
done

log "spawned $((N_H100 + N_A100)) workers in tmux session $POOL_NAME"
log "attach with: tmux attach -t $POOL_NAME"
log "watch queue drain: watch \"awk -F, 'NR>1{print \\\$3}' $BLOCK_B_POOL/queue_state.csv | sort | uniq -c\""
log ""
log "NEXT: after workers attach, pin big-Chai FSHR+LSHR to w7/w8/w9 via:"
log "  1. write \$BLOCK_B_POOL/filters/w7.txt (and w8, w9) with contents 'chai\\nstrict\\n'"
log "  2. queue_ops.py bulk_transition --from-state paused --to-state pending --receptor FSHR --backbone chai ..."
log "  3. same for LSHR"
