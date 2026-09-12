#!/bin/bash
# block_b_worker.sh — one instance per qrsh session in the block_b pool.
#
# Same loop as block_a_worker.sh but:
#   1. Scorer-sync pre-flight: verify HPC scorer/*.py SHA256s match
#      refs/scorer_expected_shas.json (audit trail #11 regression class).
#      Abort loud on mismatch — cannot let a worker score with a drifted
#      scorer package.
#   2. Uses queue_ops.py against the block_b Wide campaign pool
#      (not h100_pool, not block_a_campaign). Pool root is passed via
#      BLOCK_B_POOL env.
#
# Usage:  bash block_b_worker.sh <worker_id>
#         (run inside a qrsh session; BLOCK_B_POOL exported by caller.)

set -o pipefail

WORKER_ID="${1:-w?}"
REPO=/home/sengaad1/paper_af3
POOL="${BLOCK_B_POOL:-/hpc/scratch/sengaad1/paper_af3/experiments/019_block_b_partner_selection/pool}"
LOG="$POOL/logs/worker.$WORKER_ID.log"

mkdir -p "$POOL/logs"

log() {
    echo "[$(date -u +%FT%TZ) $WORKER_ID] $*" | tee -a "$LOG"
}

log "starting on $(hostname); pool=$POOL; CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-<unset>}"

# ---------------------------------------------------------------------
# Scorer-sync pre-flight (audit trail #11)
# ---------------------------------------------------------------------
EXPECTED="$REPO/refs/scorer_expected_shas.json"
if [ ! -f "$EXPECTED" ]; then
    log "ABORT: expected shas file missing at $EXPECTED"
    exit 3
fi

python3 <<'PY'
import hashlib, json, pathlib, sys
repo = pathlib.Path("/home/sengaad1/paper_af3")
expected = json.loads((repo / "refs/scorer_expected_shas.json").read_text())
mismatches = []
for rel, exp_hex in expected.items():
    p = repo / rel
    if not p.exists():
        mismatches.append(f"missing {rel}")
        continue
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got != exp_hex:
        mismatches.append(f"drift {rel}: expected {exp_hex[:12]} got {got[:12]}")
if mismatches:
    print("SCORER SYNC MISMATCH:", "; ".join(mismatches), file=sys.stderr)
    sys.exit(2)
print(f"scorer sync OK: {len(expected)}/{len(expected)} files match")
PY
if [ $? -ne 0 ]; then
    log "ABORT: scorer-sync pre-flight failed"
    exit 3
fi

log "scorer-sync pre-flight passed"

# Activate the openfold3 venv — has all deps queue_ops.py needs (csv, fcntl are stdlib).
source "$REPO/.venv/bin/activate" 2>/dev/null \
    || source /home/sengaad1/software/venvs/openfold3/bin/activate

# Chai MSA cache — cache mode is the only supported path (see audit trail #10).
export CHAI_MSA_DIRECTORY="${CHAI_MSA_DIRECTORY:-/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"

QUEUE_CSV="$POOL/queue.csv"
STATE_CSV="$POOL/queue_state.csv"

if [ ! -f "$QUEUE_CSV" ] || [ ! -f "$STATE_CSV" ]; then
    log "ABORT: queue.csv or queue_state.csv missing at $POOL"
    exit 4
fi

# ---------------------------------------------------------------------
# Main pop-run-mark loop
# ---------------------------------------------------------------------
while true; do
    EVAL_ENV=$(python3 "$REPO/scripts/queue_ops.py" pop "$WORKER_ID" \
        --state-csv "$STATE_CSV" --queue-csv "$QUEUE_CSV" 2>>"$LOG")
    RC=$?
    if [ $RC -eq 1 ]; then
        log "queue empty, exiting"
        break
    fi
    if [ $RC -ne 0 ]; then
        log "queue_ops.pop returned rc=$RC — aborting worker"
        exit $RC
    fi

    eval "$EVAL_ENV"
    log "claimed sha=$CLAIM_SHA backbone=$BACKBONE seed=$PRED_SEED samples=$PRED_SAMPLES"

    # BACKBONE_POOL_TIER filter — Block C Tier 3 (2026-09-04) adds a
    # supplemental A100 pool for boltz-only rows. A100 workers set
    # BACKBONE_POOL_TIER=a100_boltz_only; they release non-boltz rows back
    # to pending so an H100 worker can pick them up next. H100 workers set
    # BACKBONE_POOL_TIER=h100_any (or leave it unset) and accept any row.
    if [ "${BACKBONE_POOL_TIER:-h100_any}" = "a100_boltz_only" ] && [ "$BACKBONE" != "boltz" ]; then
        log "a100_boltz_only pool: releasing non-boltz row sha=$CLAIM_SHA backbone=$BACKBONE"
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" pending \
            --state-csv "$STATE_CSV" \
            --reason "a100_pool_backbone_reject worker=$WORKER_ID backbone=$BACKBONE" >>"$LOG" 2>&1
        continue
    fi

    mkdir -p "$PRED_OUT_DIR"

    # Defensive: purge stale content in the output dir (chai's
    # "output_dir must be empty" assertion, etc.).
    find "$PRED_OUT_DIR" -mindepth 1 -delete 2>/dev/null || true

    # OF3: nuke the colabfold_msas dir SCOPED TO THIS WORKER'S OWN scratch
    # before dispatch. OF3 0.4.4 flipped the purge semantics upstream:
    # openfold3/core/data/tools/colabfold_msa_server.py::preprocess_colabfold_msas
    # (line 1211) now raises FileExistsError if raw/ pre-exists. The prior
    # rule (2026-09-03) was "keep raw/ intact because os.mkdir(raw/main)
    # is non-recursive" — that inverted with 0.4.4, which now creates raw/
    # itself via makedirs and rejects a pre-existing raw/.
    #
    # Scoping is critical: `/scratch/tmp/*/of3-of-sengaad1/` matches EVERY
    # qrsh worker's scratch on this compute node, so a bare glob nukes
    # co-located workers' mid-flight downloads (Block C Tier 1 2026-09-04:
    # 21 OF3 failures — 11 with FileExistsError raw/ pre-existing, 10 with
    # FileNotFoundError raw/main/out.tar.gz — the second class being the
    # cross-worker collision on the shared glob).
    #
    # SGE sets TMPDIR=/scratch/tmp/$JOB_ID.$SGE_TASK_ID.$queue on
    # basel-hpc; use it directly. Fall back to a JOB_ID-scoped glob so
    # a bare-shell test still works. The final `2>/dev/null || true`
    # keeps the FIRST OF3 row on this worker from tripping on
    # "path doesn't exist yet" — expected for a fresh worker.
    if [ "$BACKBONE" = "of3" ]; then
        if [ -n "${TMPDIR:-}" ]; then
            rm -rf "${TMPDIR}/of3-of-sengaad1/colabfold_msas" 2>/dev/null || true
        elif [ -n "${JOB_ID:-}" ]; then
            rm -rf /scratch/tmp/${JOB_ID}.*/of3-of-sengaad1/colabfold_msas 2>/dev/null || true
        fi
    fi

    START_S=$(date +%s)
    # Capture backbone subprocess stdout+stderr to a per-row log file so
    # failures can be diagnosed post-hoc. Without this, tracebacks are
    # lost to tmux scrollback (Block B 2026-09-03 failure taxonomy
    # blocker; task #168).
    #
    # Log lands ONE LEVEL ABOVE $PRED_OUT_DIR (uniquely named by the
    # dir's basename) so chai-lab fold's `assert not any(output_dir.iterdir())`
    # doesn't fire — the pre-existing tee-into-PRED_OUT_DIR pattern broke
    # every chai row in Block C smoke 2026-09-04 (iterdir sees the log
    # file before chai gets a chance to write CIFs).
    ROW_LOG="$(dirname "$PRED_OUT_DIR")/rerun_${BACKBONE}.$(basename "$PRED_OUT_DIR").log"
    bash "$REPO/qsub/rerun_${BACKBONE}.sh" 2>&1 | tee "$ROW_LOG"
    JOB_RC=${PIPESTATUS[0]}
    WALL_S=$(( $(date +%s) - START_S ))

    # Check backbone's own ok flag — catches silent-fails where the launcher
    # returns rc=0 but the backbone internally caught a CUDA OOM / MSA API
    # timeout / other exception and produced zero output (audit trail #10
    # class; Block B 2026-09-03 silent-fail audit — 300 rows affected).
    STATUS_JSON="$PRED_OUT_DIR/_${BACKBONE}_status.json"
    STATUS_OK="False"
    STATUS_N=0
    if [ -f "$STATUS_JSON" ]; then
        STATUS_OK=$(python3 -c "
import json,sys
try:
    d = json.load(open(sys.argv[1]))
    print('True' if d.get('ok', False) else 'False')
except: print('False')" "$STATUS_JSON" 2>/dev/null || echo "False")
        STATUS_N=$(python3 -c "
import json,sys
try:
    d = json.load(open(sys.argv[1]))
    print(int(d.get('n_produced', 0)))
except: print(0)" "$STATUS_JSON" 2>/dev/null || echo "0")
    fi

    if [ $JOB_RC -eq 0 ] && [ "$STATUS_OK" = "True" ] && [ "$STATUS_N" -gt 0 ]; then
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" done \
            --state-csv "$STATE_CSV" \
            --reason "worker-$WORKER_ID ok n=$STATUS_N wall=${WALL_S}s" >>"$LOG" 2>&1
        log "done sha=$CLAIM_SHA rc=0 n=$STATUS_N wall=${WALL_S}s"
    else
        python3 "$REPO/scripts/queue_ops.py" mark "$CLAIM_SHA" failed \
            --state-csv "$STATE_CSV" \
            --reason "worker-$WORKER_ID rc=$JOB_RC ok=$STATUS_OK n=$STATUS_N wall=${WALL_S}s" >>"$LOG" 2>&1
        log "failed sha=$CLAIM_SHA rc=$JOB_RC ok=$STATUS_OK n=$STATUS_N wall=${WALL_S}s"
    fi
done

log "worker terminating cleanly"
