#!/bin/bash
# Run at the END of every session. Adds a handoff entry to SESSIONS.md.
# usage: ./session_end.sh "one-line summary of what this session did"
cd "$(dirname "$0")" || exit 1
ME=$(cat .machine 2>/dev/null || hostname -s)
SUMMARY="${1:?usage: ./session_end.sh \"what this session did\"}"

DRIFT=$(lit/corpus_check.sh 2>/dev/null | grep -cE '^[[:space:]]*!!' || echo 0)
DATA=$(python3 analysis/fingerprint.py --check 2>&1 | head -1 | sed 's/^[[:space:]]*//')

ENTRY=$(mktemp)
{
  echo "## $(date '+%Y-%m-%d %H:%M')  ·  $ME"
  echo
  echo "$SUMMARY"
  echo
  echo "- corpus drift categories: $DRIFT"
  echo "- data: $DATA"
  echo "- TODO for next session: (edit me before committing)"
  echo
} > "$ENTRY"

# Insert after the header block, immediately BEFORE the first existing entry —
# not at the very top, which would bury the file's own instructions.
OUT=$(mktemp)
if grep -q '^## ' SESSIONS.md 2>/dev/null; then
  awk -v f="$ENTRY" '
    !done && /^## / { while ((getline line < f) > 0) print line; done=1 }
    { print }' SESSIONS.md > "$OUT"
else
  cat SESSIONS.md "$ENTRY" > "$OUT" 2>/dev/null || cat "$ENTRY" > "$OUT"
fi
mv "$OUT" SESSIONS.md
rm -f "$ENTRY"

echo "SESSIONS.md updated. Edit the TODO line, then:"
echo "  git add -A && git commit -m 'session-end($ME): $SUMMARY' && git push"
