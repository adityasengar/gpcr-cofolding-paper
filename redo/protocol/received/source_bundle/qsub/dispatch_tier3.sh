#!/bin/bash
#
# qsub/dispatch_tier3.sh — Block C Tier 3 pool driver (40,800 predictions).
#
# Runs from a login node. Fires two tmux sessions:
#
#   1. $POOL_NAME               — the primary H100 workforce (N_H100 workers
#                                  at launch; scavenger grows toward 30 cap).
#   2. $POOL_NAME_A100          — supplemental A100 boltz-only workforce
#                                  (N_A100 workers, capped at 10). Non-boltz
#                                  rows released back to `pending` by the
#                                  worker's BACKBONE_POOL_TIER filter.
#
# The scavenger (scripts/tier3_gpu_scavenger.sh) runs in its own
# tmux session `tier3_scavenger` and grows the H100 pool up to 30 as
# capacity frees on the cluster.
#
# Env forwarding: qrsh does NOT forward exported vars automatically
# (qrsh-env-forwarding-gotcha-2026-09-02). Every required env var must
# appear on `qrsh -v` AND be exported before qrsh so tmux send-keys works.
#
# Env vars set for every worker:
#   BLOCK_B_POOL          — pool root (queue.csv + queue_state.csv here)
#   CHAI_MSA_DIRECTORY    — shared .aligned.pqt cache (belt-and-suspenders
#                           against the audit-#10 silent-single-seq class)
#   BACKBONE_POOL_TIER    — `h100_any` on H100 workers; `a100_boltz_only`
#                           on A100 workers (worker filters non-boltz rows
#                           back to pending)
#
# GPU pool caps (per contract §6, user-locked):
#   H100:  30 workers max  (all 4 backbones)
#   A100:  10 workers max  (boltz-2 only)
#
# Wall-clock estimate: ~33 h at 25-H100 pool; ~44 h with retries.
# h_rt=24:00:00 per worker; never released voluntarily.
#
# Idempotent-refuse: refuses to create either tmux session if it exists.
#
# Usage (basel-hpc login node):
#   bash qsub/dispatch_tier3.sh
#     (defaults: N_H100=25, N_A100=10, POOL_NAME=block_c_tier3_2026_09_04)

set -o pipefail

POOL_NAME="${POOL_NAME:-block_c_tier3_2026_09_04}"
POOL_NAME_A100="${POOL_NAME}_a100"
BLOCK_C_TIER3_POOL="${BLOCK_C_TIER3_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_b_worker.sh"
N_H100="${N_H100:-25}"
N_A100="${N_A100:-10}"
H_RT="${H_RT:-24:00:00}"
CHAI_MSA="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"

log() { echo "[$(date -u +%FT%TZ) tier3-launcher] $*"; }

# 1. Pool prereqs
for f in "$BLOCK_C_TIER3_POOL/queue.csv" "$BLOCK_C_TIER3_POOL/queue_state.csv"; do
    if [ ! -f "$f" ]; then
        log "ABORT: missing $f — run scripts/build_block_b_campaign_queue.py against tier3_manifest.csv first"
        exit 2
    fi
done
mkdir -p "$BLOCK_C_TIER3_POOL/logs"

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

# 3. Refuse if sessions already exist
for s in "$POOL_NAME" "$POOL_NAME_A100"; do
    if tmux has-session -t "$s" 2>/dev/null; then
        log "ABORT: tmux session '$s' already exists. Kill it with 'tmux kill-session -t $s' or use a different POOL_NAME."
        exit 4
    fi
done

log "creating H100 tmux session $POOL_NAME with $N_H100 workers"
log "creating A100 tmux session $POOL_NAME_A100 with $N_A100 boltz-only workers"
log "pool root: $BLOCK_C_TIER3_POOL"

# 4. H100 pool
QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G -v BLOCK_B_POOL,CHAI_MSA_DIRECTORY,BACKBONE_POOL_TIER"
ENV_EXPORT_H100="export BLOCK_B_POOL='$BLOCK_C_TIER3_POOL' && export CHAI_MSA_DIRECTORY='$CHAI_MSA' && export BACKBONE_POOL_TIER='h100_any'"

tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT_H100 && $QRSH_H100 bash $WORKER w0" Enter

for i in $(seq 1 $((N_H100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT_H100 && $QRSH_H100 bash $WORKER w$i" Enter
done

log "spawned $N_H100 H100 workers in tmux session $POOL_NAME"

# 5. A100 pool (boltz-only via BACKBONE_POOL_TIER filter in worker)
QRSH_A100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=ampere_a100,m_mem_free=32G -v BLOCK_B_POOL,CHAI_MSA_DIRECTORY,BACKBONE_POOL_TIER"
ENV_EXPORT_A100="export BLOCK_B_POOL='$BLOCK_C_TIER3_POOL' && export CHAI_MSA_DIRECTORY='$CHAI_MSA' && export BACKBONE_POOL_TIER='a100_boltz_only'"

tmux new-session -d -s "$POOL_NAME_A100" -n "a0"
tmux send-keys -t "$POOL_NAME_A100:a0" "$ENV_EXPORT_A100 && $QRSH_A100 bash $WORKER a0" Enter

for i in $(seq 1 $((N_A100 - 1))); do
    tmux new-window -t "$POOL_NAME_A100" -n "a$i"
    tmux send-keys -t "$POOL_NAME_A100:a$i" "$ENV_EXPORT_A100 && $QRSH_A100 bash $WORKER a$i" Enter
done

log "spawned $N_A100 A100 boltz-only workers in tmux session $POOL_NAME_A100"

log ""
log "attach H100 pool:  tmux attach -t $POOL_NAME"
log "attach A100 pool:  tmux attach -t $POOL_NAME_A100"
log "start scavenger:   POOL_NAME=$POOL_NAME BLOCK_C_TIER3_POOL=$BLOCK_C_TIER3_POOL bash scripts/tier3_gpu_scavenger.sh"
log "watch queue drain: watch \"awk -F, 'NR>1{print \\\$3}' $BLOCK_C_TIER3_POOL/queue_state.csv | sort | uniq -c\""
