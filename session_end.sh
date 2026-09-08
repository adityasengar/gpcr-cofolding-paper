#!/bin/bash
# Run at the END of every session. Appends a handoff entry, commits, pushes.
# usage: ./session_end.sh "one-line summary of what this session did"
cd "$(dirname "$0")" || exit 1
ME=$(cat .machine 2>/dev/null || hostname -s)
SUMMARY="${1:?usage: ./session_end.sh \"what this session did\"}"
TMP=$(mktemp)
{
  echo "## $(date '+%Y-%m-%d %H:%M')  ·  $ME"
  echo
  echo "$SUMMARY"
  echo
  echo "- corpus: $(lit/corpus_check.sh 2>/dev/null | grep -cE '^  !!' || echo 0) drift categories"
  echo "- data:   $(python3 analysis/fingerprint.py --check 2>&1 | head -1)"
  echo "- TODO for next session: (edit me)"
  echo
  [ -f SESSIONS.md ] && cat SESSIONS.md
} > "$TMP"
mv "$TMP" SESSIONS.md
echo "SESSIONS.md updated. Review it, then:"
echo "  git add -A && git commit -m 'session-end($ME): $SUMMARY' && git push"
