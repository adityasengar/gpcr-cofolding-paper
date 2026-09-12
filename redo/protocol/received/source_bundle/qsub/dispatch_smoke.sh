#!/bin/bash
#
# qsub/dispatch_smoke.sh — Block C 400-prediction smoke pool driver.
#
# Runs from a login node. Creates a tmux session with N_H100 qrsh
# windows on default.q (H100 only per coordinator authorisation for the
# Block C smoke — 25 H100 GPUs). Each worker reuses
# scripts/block_b_worker.sh unchanged, pointed at the smoke pool via
# $BLOCK_B_POOL env (worker's queue-loop code is pool-agnostic).
#
# Env forwarding: qrsh does NOT forward exported vars automatically
# (qrsh-env-forwarding-gotcha-2026-09-02). Every required env var
# must appear on the `qrsh -v` command line AND be exported before qrsh
# so the tmux-send-keys form works.
#
# Chai MSA cache pass-through mirrors block_b_worker.sh:
#   CHAI_MSA_DIRECTORY = /hpc/scratch/sengaad1/paper_af3/msa_cache/chai
# (also hardcoded in qsub/rerun_chai.sh as a fallback default —
# belt-and-suspenders per audit #10).
#
# Idempotent-refuse: refuses to run if tmux session already exists.
#
# Usage (on basel-hpc login node):
#   bash qsub/dispatch_smoke.sh
#     (defaults: N_H100=25, POOL_NAME=block_c_smoke_2026_09_04)

set -o pipefail

POOL_NAME="${POOL_NAME:-block_c_smoke_2026_09_04}"
BLOCK_C_SMOKE_POOL="${BLOCK_C_SMOKE_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/smoke/pool}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_b_worker.sh"
N_H100="${N_H100:-25}"
H_RT="${H_RT:-04:00:00}"
CHAI_MSA="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"

log() { echo "[$(date -u +%FT%TZ) smoke-launcher] $*"; }

# 1. Pool prereqs
for f in "$BLOCK_C_SMOKE_POOL/queue.csv" "$BLOCK_C_SMOKE_POOL/queue_state.csv"; do
    if [ ! -f "$f" ]; then
        log "ABORT: missing $f — run build_block_b_campaign_queue.py against smoke_manifest.csv first"
        exit 2
    fi
done
mkdir -p "$BLOCK_C_SMOKE_POOL/logs"

# 2. Scorer-sync pre-flight on the login node
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

log "creating tmux session $POOL_NAME with $N_H100 H100 workers"
log "pool root: $BLOCK_C_SMOKE_POOL"

# 4. Build the session
#    block_b_worker.sh reads BLOCK_B_POOL (its historical name), we point
#    it at the smoke pool.
QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G -v BLOCK_B_POOL,CHAI_MSA_DIRECTORY"
ENV_EXPORT="export BLOCK_B_POOL='$BLOCK_C_SMOKE_POOL' && export CHAI_MSA_DIRECTORY='$CHAI_MSA'"

# Window 0
tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w0" Enter

for i in $(seq 1 $((N_H100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w$i" Enter
done

log "spawned $N_H100 H100 workers in tmux session $POOL_NAME"
log "attach with: tmux attach -t $POOL_NAME"
log "watch queue drain: watch \"awk -F, 'NR>1{print \\\$3}' $BLOCK_C_SMOKE_POOL/queue_state.csv | sort | uniq -c\""
