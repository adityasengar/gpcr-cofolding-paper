#!/bin/bash
# campaign_heartbeat.sh — log queue counts (per backbone × arm) every
# 15 min to logs/campaign_heartbeat.log. Runs on HPC login node.
#
# Usage:
#   BLOCK_A_POOL=... bash scripts/campaign_heartbeat.sh   (loop mode)
#   BLOCK_A_POOL=... bash scripts/campaign_heartbeat.sh once   (single tick)

set -o pipefail

POOL="${BLOCK_A_POOL:-/hpc/scratch/sengaad1/paper_af3/block_a_campaign_2026_09_01}"
STATE_CSV="$POOL/queue_state.csv"
QUEUE_CSV="$POOL/queue.csv"
LOG_DIR="${LOG_DIR:-$POOL/logs}"
LOG="$LOG_DIR/campaign_heartbeat.log"

mkdir -p "$LOG_DIR"

tick() {
    python3 <<PY | tee -a "$LOG"
import csv, datetime, pathlib
state = list(csv.DictReader(open("$STATE_CSV")))
queue = list(csv.DictReader(open("$QUEUE_CSV")))
q_by_sha = {r["prediction_sha"]: r for r in queue}
from collections import Counter
by_state = Counter(r["state"] for r in state)
by_bb_arm = Counter()
for r in state:
    q = q_by_sha.get(r["prediction_sha"], {})
    bb = q.get("backbone", "?")
    # Arm inferred from experiment_slug (..._cognate_ vs ..._apo_)
    slug = q.get("experiment_slug", "")
    arm = "cognate" if "_cognate_" in slug else ("apo" if "_apo_" in slug else "?")
    by_bb_arm[(bb, arm, r["state"])] += 1
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
print(f"[{now}] state totals: {dict(by_state)}")
for (bb, arm, st), n in sorted(by_bb_arm.items()):
    print(f"[{now}] {bb:<10} {arm:<8} {st:<10} {n}")
print(f"[{now}] ---")
PY
}

if [ "$1" = "once" ]; then
    tick
    exit 0
fi

# Loop mode: every 15 min
while true; do
    tick
    sleep 900
done
