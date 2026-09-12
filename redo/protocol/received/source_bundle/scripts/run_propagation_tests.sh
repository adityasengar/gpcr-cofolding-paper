#!/bin/bash
#
# scripts/run_propagation_tests.sh — driver for the six §10 propagation
# tests. Each test asserts a distinctive config value actually reaches
# the compute layer (not just the launcher's assumption). Together they
# close the silent-config-bug class flagged in audit trail #9, #10, #11,
# #12, #13.
#
# Exit codes
#   0  all tests pass
#   1  one or more tests failed
#   2  test dispatch failed (couldn't even run a test)
#
# The results.jsonl file is appended to on each run — the aggregator
# reads only rows from THIS run (matched by timestamp cluster).
#

set -eo pipefail

REPO=$(cd "$(dirname "$0")/.." && pwd)
TESTS_DIR="$REPO/scripts/propagation_tests"
RESULTS_DIR="$REPO/experiments/propagation_tests_2026_09_02"
RESULTS="$RESULTS_DIR/results.jsonl"
mkdir -p "$RESULTS_DIR"

# Mark the boundary of this run in the JSONL so the driver can score
# only its own tests.
RUN_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"run_boundary\":true,\"run_started_ts_utc\":\"$RUN_TS\"}" >> "$RESULTS"

TESTS=(
    "test_seeds_produce_different_structures.py"
    "test_msa_depth_reaches_model.py"
    "test_no_templates_no_rcsb_call.py"
    "test_of3_seeds_reach_sampler.py"
    "test_chai_aligned_pqt_present.py"
    "test_scorer_git_sha_endtoend.py"
)

echo "=== §10 propagation tests — $RUN_TS ==="
FAILURES=()
for t in "${TESTS[@]}"; do
    echo ""
    echo "--- $t ---"
    if ! python3 "$TESTS_DIR/$t"; then
        FAILURES+=("$t")
    fi
done

echo ""
echo "=== summary ==="
echo "passed: $((${#TESTS[@]} - ${#FAILURES[@]})) / ${#TESTS[@]}"
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo "failed: ${FAILURES[*]}"
    echo ""
    echo "DISPATCH BLOCKED — resolve failing propagation tests before Block B dispatch."
    exit 1
fi
echo "all pass — dispatch prerequisite satisfied"
exit 0
