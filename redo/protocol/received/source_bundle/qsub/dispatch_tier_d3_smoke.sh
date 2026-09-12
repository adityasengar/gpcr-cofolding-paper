#!/bin/bash
#
# qsub/dispatch_tier_d3_full.sh — Tier D3 full pool driver.
#
# Runs from a login node. Creates a tmux session with N_H100 qrsh
# windows on default.q. Each worker reuses scripts/block_b_worker.sh
# unchanged, pointed at the D3 full pool via $BLOCK_B_POOL env.
#
# Grid: 12 (receptor, arm) cells × 4 backbones × 5 seeds × 10 samples =
# 2,400 predictions.
#
# Cell inventory (240 rows in queue, 20 dropped from ADRB2 active_nb
# because Nb80 sequence not yet curated → placeholder duplicates
# inactive_nb):
#   ADRB2:  apo, cognate_ga, inactive_nb              (3 arms × 4 bb × 5 s = 60 rows)
#   OPRK:   apo, cognate_ga, inactive_nb              (3 arms × 4 bb × 5 s = 60 rows)
#   ACM2:   apo, cognate_ga, active_nb                (3 arms × 4 bb × 5 s = 60 rows)
#   AGTR1:  apo, cognate_ga, active_nb                (3 arms × 4 bb × 5 s = 60 rows)
#   TOTAL:                                              240 rows
#
# Wall estimate: ~1 h on 12 H100. D1 full (14,000 preds, 19 H100) ran
# ~2 h; D3 is 2,400 preds so ~2/14 * 2h * 19/12 = ~0.5 h theoretical,
# reserve 2 h for overhead + slow-cell drift.
#
# Prerequisite: pool has queue.csv + queue_state.csv built from
# experiments/024_tier_d3_msa_depth/manifest/tier_d3_smoke_manifest.csv
# via scripts/build_block_b_campaign_queue.py.
#
# Usage (on basel-hpc login node):
#   bash qsub/dispatch_tier_d3_full.sh
#     (defaults: N_H100=12, POOL_NAME=tier_d3_smoke_2026_09_08)

set -o pipefail

POOL_NAME="${POOL_NAME:-tier_d3_smoke_2026_09_08}"
TIER_D3_POOL="${TIER_D3_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/024_tier_d3_msa_depth/smoke/pool}"
REPO=/home/sengaad1/paper_af3
WORKER="$REPO/scripts/block_b_worker.sh"
N_H100="${N_H100:-25}"
H_RT="${H_RT:-04:00:00}"
CHAI_MSA="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"

log() { echo "[$(date -u +%FT%TZ) tier-d3-full-launcher] $*"; }

# 1. Pool prereqs
for f in "$TIER_D3_POOL/queue.csv" "$TIER_D3_POOL/queue_state.csv"; do
    if [ ! -f "$f" ]; then
        log "ABORT: missing $f"
        log "  Build the queue first from the dispatch manifest:"
        log "    python3 $REPO/scripts/build_block_b_campaign_queue.py \\"
        log "      --manifest $REPO/experiments/024_tier_d3_msa_depth/manifest/tier_d3_smoke_manifest.csv \\"
        log "      --pool $TIER_D3_POOL"
        exit 2
    fi
done
mkdir -p "$TIER_D3_POOL/logs"

# 2. Scorer-sync pre-flight
python3 <<'PY'
import hashlib, json, pathlib, sys
repo = pathlib.Path("/home/sengaad1/paper_af3")
expected_path = repo / "refs/scorer_expected_shas.json"
if not expected_path.is_file():
    print("WARN: refs/scorer_expected_shas.json not present; skipping local sync check", file=sys.stderr)
    sys.exit(0)
expected = json.loads(expected_path.read_text())
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

# 3. Refuse if tmux session already exists
if tmux has-session -t "$POOL_NAME" 2>/dev/null; then
    log "ABORT: tmux session '$POOL_NAME' already exists. Kill it with 'tmux kill-session -t $POOL_NAME' or use a different POOL_NAME."
    exit 4
fi

log "creating tmux session $POOL_NAME with $N_H100 H100 workers"
log "pool root: $TIER_D3_POOL"

# 4. Build the session
QRSH_H100="qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G -v BLOCK_B_POOL,CHAI_MSA_DIRECTORY"
ENV_EXPORT="export BLOCK_B_POOL='$TIER_D3_POOL' && export CHAI_MSA_DIRECTORY='$CHAI_MSA'"

# Window 0
tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w0" Enter

for i in $(seq 1 $((N_H100 - 1))); do
    tmux new-window -t "$POOL_NAME" -n "w$i"
    tmux send-keys -t "$POOL_NAME:w$i" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w$i" Enter
done

log "spawned $N_H100 H100 workers in tmux session $POOL_NAME"
log "attach with: tmux attach -t $POOL_NAME"
log "watch queue drain: watch \"awk -F, 'NR>1{print \\\$3}' $TIER_D3_POOL/queue_state.csv | sort | uniq -c\""
log ""
log "Expected wall: ~1 h for 240 rows × 10 samples = 2,400 predictions on $N_H100 workers"
log "When drain completes, rescore with:"
log "    python3 $REPO/scripts/rescore_parallel.py --pool $TIER_D3_POOL --out $REPO/experiments/024_tier_d3_msa_depth/analysis/full"
