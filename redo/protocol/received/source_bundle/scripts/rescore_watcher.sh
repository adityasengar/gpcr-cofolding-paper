#!/bin/bash
# rescore_watcher.sh — waits for h100_pool DONE marker, then rescores all
# 10 experiments and writes RESCORE_DONE marker.
#
# Runs in a tmux session `rescore_watcher` on basel-hpc.
# Blocks on DONE.marker; when it appears, iterates through the 5 AA2AR
# phase1 slugs + 5 ADRB2 phase2 slugs, calling scripts/rescore_experiment.py
# with the right --scratch-root for each family.

set -eu
POOL=/hpc/scratch/sengaad1/paper_af3/h100_pool
REPO=/home/sengaad1/paper_af3
LOG=$POOL/rescore_watcher.log
DONE_MARKER=$POOL/DONE.marker
RESCORE_DONE=$POOL/RESCORE_DONE.marker

# AA2AR phase1 experiments (scratch under /hpc/scratch/.../experiments/)
AA2AR_SLUGS=(
    "013_aa2ar_gs_neca_mn_5_1"
    "014_aa2ar_gs_neca_mn_1_5"
    "015_aa2ar_gs_neca_mn_5_5"
    "016_aa2ar_gs_neca_mn_20_1"
    "017_aa2ar_gs_neca_mn_1_20"
)
AA2AR_SCRATCH=/hpc/scratch/sengaad1/paper_af3/experiments

# ADRB2 phase2 experiments (scratch under /hpc/scratch/.../h100_pool/experiments/)
ADRB2_SLUGS=(
    "019_adrb2_gs_agonist_mn_5_1"
    "020_adrb2_gs_agonist_mn_1_5"
    "021_adrb2_gs_agonist_mn_5_5"
    "022_adrb2_gs_agonist_mn_20_1"
    "023_adrb2_gs_agonist_mn_1_20"
)
ADRB2_SCRATCH=/hpc/scratch/sengaad1/paper_af3/h100_pool/experiments

log() {
    echo "[$(date -u +%FT%TZ) rw] $*" | tee -a "$LOG"
}

mkdir -p "$POOL"
: >>"$LOG"

log "rescore_watcher starting (pid=$$); waiting for $DONE_MARKER"

# Wait for DONE marker (poll every 60s, up to 12h wall)
DEADLINE=$(( $(date +%s) + 43200 ))
while [ ! -f "$DONE_MARKER" ]; do
    if [ $(date +%s) -gt $DEADLINE ]; then
        log "TIMEOUT: DONE marker never appeared (12h). Exiting."
        exit 1
    fi
    sleep 60
done

log "DONE marker seen; content: $(cat "$DONE_MARKER")"
log "Starting rescore of 10 experiments..."

source /home/sengaad1/software/venvs/openfold3/bin/activate

# AA2AR family
for slug in "${AA2AR_SLUGS[@]}"; do
    log "rescoring $slug (AA2AR scratch)"
    python3 "$REPO/scripts/rescore_experiment.py" \
        --slug "$slug" \
        --scratch-root "$AA2AR_SCRATCH" \
        --experiments-root "$REPO/experiments" 2>&1 | tail -10 | while read L; do log "  $slug: $L"; done \
        || log "  $slug: rescore failed with rc=$?"
done

# ADRB2 family (different scratch root)
for slug in "${ADRB2_SLUGS[@]}"; do
    log "rescoring $slug (ADRB2 scratch)"
    python3 "$REPO/scripts/rescore_experiment.py" \
        --slug "$slug" \
        --scratch-root "$ADRB2_SCRATCH" \
        --experiments-root "$REPO/experiments" 2>&1 | tail -10 | while read L; do log "  $slug: $L"; done \
        || log "  $slug: rescore failed with rc=$?"
done

# Write completion marker
echo "rescored=10 slugs at=$(date -u +%FT%TZ)" > "$RESCORE_DONE"
log "RESCORE_DONE marker written; ${#AA2AR_SLUGS[@]} AA2AR + ${#ADRB2_SLUGS[@]} ADRB2 rescored"

log "rescore_watcher done"
