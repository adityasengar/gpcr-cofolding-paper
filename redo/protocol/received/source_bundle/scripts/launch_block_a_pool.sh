#!/bin/bash
# launch_block_a_pool.sh — set up the 25-window tmux session with one
# qrsh worker per window (mix of H100 and A100).
#
# Runs from a login node. Creates tmux session $POOL_NAME with:
#   w0..w11  → H100 qrsh (12 windows)
#   w12..w24 → A100 qrsh (13 windows)
#
# Each qrsh runs block_a_worker.sh which loops popping from
# $BLOCK_A_POOL/queue_state.csv until empty.
#
# Idempotent-refuse: refuses to run if $POOL_NAME already exists.
#
# Usage:   bash launch_block_a_pool.sh
#          (verifies scorer-sync locally before spawning any worker)

set -o pipefail

POOL_NAME="${POOL_NAME:-block_a_pool_2026_09_01}"
BLOCK_A_POOL="${BLOCK_A_POOL:-/hpc/scratch/sengaad1/paper_af3/block_a_campaign_2026_09_01}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_a_worker.sh"

N_H100="${N_H100:-17}"      # take H100 first (17 free at 2026-09-01 T16:30Z)
N_A100="${N_A100:-8}"       # fill remainder to hit 25 total
H_RT="${H_RT:-48:00:00}"

log() { echo "[$(date -u +%FT%TZ) launcher] $*"; }

# 1. Pre-flight: queue.csv + state.csv must exist
for f in "$BLOCK_A_POOL/queue.csv" "$BLOCK_A_POOL/queue_state.csv"; do
    if [ ! -f "$f" ]; then
        log "ABORT: missing $f — run build_block_a_campaign_queue.py first"
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
log "pool root: $BLOCK_A_POOL"

# 4. Build the session
# m_mem_free=32G: OF3/protenix use 15-25GB residual + cgroup headroom;
# the site default cgroup cap is 4GB and killed 24 of 25 workers on the
# first launch (exit 129 / cgroups_enforced_memory_limit).
QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G"
QRSH_A100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=ampere_a100_sxm4,m_mem_free=32G"
ENV_EXPORT="export BLOCK_A_POOL='$BLOCK_A_POOL'"

# Window 0 = first H100
tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w0" Enter

# Remaining H100 windows
for i in $(seq 1 $((N_H100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w$i" Enter
done

# A100 windows
for i in $(seq $N_H100 $((N_H100 + N_A100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_A100 bash $WORKER w$i" Enter
done

log "spawned $((N_H100 + N_A100)) workers in tmux session $POOL_NAME"
log "attach with: tmux attach -t $POOL_NAME"
log "watch queue drain: watch \"awk -F, 'NR>1{print \\\$3}' $BLOCK_A_POOL/queue_state.csv | sort | uniq -c\""
