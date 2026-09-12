#!/bin/bash
# verify_chai_msa_cache.sh — post-build correctness test for Chai's --msa-directory
#
# Run on basel-hpc after scripts/build_chai_msa_cache.py has produced
# /hpc/scratch/sengaad1/paper_af3/msa_cache/chai/*.aligned.pqt files.
#
# Usage:
#   verify_chai_msa_cache.sh [RECEPTOR_SLUG]
# Default: AA2AR (first cached during v2 build; safe default for mechanism check).
# Pass DRD2 (or another slug) once its .aligned.pqt lands in the cache.
#
# Test 1: wall-time signature (cache read vs API fetch vs single-seq)
# Test 2: hash-mismatch silent-fallback smoke test

# NB: `set -e` intentionally off — we want the verdict even if a test fails.
# `set -u` deferred until AFTER `source /etc/profile` (site's profile scripts
# reference DEBUGINFOD_URLS unbound, which trips -u).

RECEPTOR="${1:-AA2AR}"
MSA_DIR=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai
TEST_DIR=/hpc/scratch/sengaad1/paper_af3/chai_verify_${RECEPTOR}
mkdir -p "$TEST_DIR"

# Extract receptor sequence (multiline-safe via awk; concatenated)
SEQ_FILE=/home/sengaad1/paper_af3/refs/panel_receptor_sequences.fasta
SEQ=$(awk -v r="$RECEPTOR" 'BEGIN{p="^>" r "\\|"} $0~p {f=1;next} /^>/{f=0} f' "$SEQ_FILE" | tr -d '\n')
if [ -z "$SEQ" ]; then
    echo "FAIL: could not extract $RECEPTOR sequence from $SEQ_FILE"
    exit 1
fi
SHA=$(printf '%s' "$SEQ" | tr 'a-z' 'A-Z' | sha256sum | awk '{print $1}')
PQT="$MSA_DIR/${SHA}.aligned.pqt"

echo "=== Test setup ==="
echo "receptor: $RECEPTOR (length ${#SEQ})"
echo "expected .aligned.pqt: $PQT"
if [ ! -f "$PQT" ]; then
    echo "FAIL: expected .aligned.pqt does not exist. Build didn't cover $RECEPTOR."
    exit 2
fi
echo "size: $(stat -c '%s' $PQT) bytes"

# ------------------------------------------------------------------
# Test 1: wall-time signature — quick chai run with --msa-directory
# vs single-sequence
# ------------------------------------------------------------------

# Set up minimal chai input: single-chain. Chai expects `>ENTITY_TYPE|name=X`
INPUT_FASTA="$TEST_DIR/${RECEPTOR}_input.fasta"
cat > "$INPUT_FASTA" <<EOF
>protein|name=${RECEPTOR}
$SEQ
EOF

source /etc/profile
module load proxy/GLOBAL
source /home/sengaad1/software/venvs/chai1/bin/activate

echo ""
echo "=== Test 1a: Chai WITH --msa-directory (should be fast, no API fetch) ==="
mkdir -p "$TEST_DIR/out_with_cache"
START=$(date +%s)
timeout 300 chai-lab fold \
    "$INPUT_FASTA" \
    "$TEST_DIR/out_with_cache" \
    --num-trunk-recycles 1 \
    --num-diffn-timesteps 5 \
    --seed 1 \
    --msa-directory "$MSA_DIR" 2>&1 | tail -6
WITH_CACHE_SEC=$(($(date +%s) - START))
echo "with-cache wall time: ${WITH_CACHE_SEC}s"

echo ""
echo "=== Test 1b: Chai WITHOUT --msa-directory (single-sequence, baseline) ==="
mkdir -p "$TEST_DIR/out_singleseq"
START=$(date +%s)
timeout 300 chai-lab fold \
    "$INPUT_FASTA" \
    "$TEST_DIR/out_singleseq" \
    --num-trunk-recycles 1 \
    --num-diffn-timesteps 5 \
    --seed 1 2>&1 | tail -6
SINGLESEQ_SEC=$(($(date +%s) - START))
echo "single-seq wall time: ${SINGLESEQ_SEC}s"

# ------------------------------------------------------------------
# Test 2: hash-mismatch silent-fallback check
#
# Rename one .aligned.pqt so its hash doesn't match, run chai with
# --msa-directory, verify: (a) chai does NOT crash silently, (b) it
# falls back to single-seq behavior (this is the risk the gate exists
# to prevent).
# ------------------------------------------------------------------

echo ""
echo "=== Test 2: silent-fallback probe (rename one .aligned.pqt, verify chai behavior) ==="
MOVED_SRC="$MSA_DIR/${SHA}.aligned.pqt"
MOVED_DST="$MSA_DIR/DELIBERATELY_WRONG_HASH.aligned.pqt"
# Safety trap: if we die between mv-out and mv-back, restore on exit so we
# don't corrupt the shared cache. Idempotent (mv fails harmlessly if src gone).
trap '[ -f "$MOVED_DST" ] && mv "$MOVED_DST" "$MOVED_SRC" && echo "[trap] restored $MOVED_SRC"' EXIT
mv "$MOVED_SRC" "$MOVED_DST"

mkdir -p "$TEST_DIR/out_missing_pqt"
START=$(date +%s)
timeout 300 chai-lab fold \
    "$INPUT_FASTA" \
    "$TEST_DIR/out_missing_pqt" \
    --num-trunk-recycles 1 \
    --num-diffn-timesteps 5 \
    --seed 1 \
    --msa-directory "$MSA_DIR" 2>&1 | tail -8
MISSING_SEC=$(($(date +%s) - START))
echo "missing-pqt wall time: ${MISSING_SEC}s"

# Restore
mv "$MOVED_DST" "$MOVED_SRC"
echo "restored $MOVED_SRC"

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

echo ""
echo "=== Verdict ==="
echo "with-cache:        ${WITH_CACHE_SEC}s"
echo "single-seq:        ${SINGLESEQ_SEC}s"
echo "missing-pqt:       ${MISSING_SEC}s"
echo ""
echo "Interpretation:"
echo "- If with-cache ≈ single-seq: cache probably NOT being read (silent fallback risk)"
echo "- If with-cache >> single-seq: cache IS being read + featurized (expected)"
echo "- missing-pqt should behave like single-seq (verifies fallback pattern)"
