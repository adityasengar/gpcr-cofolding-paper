#!/bin/bash
# Advisory guard for MULTIPLE SESSIONS ON ONE LAPTOP.
# These share one working tree, so git gives no isolation: if two sessions edit the
# same file the last write silently wins, and `git add -A` from one can commit
# another's half-finished work. There is no conflict and no warning.
LOCK=".session-lock"
WHO="${CLAUDE_SESSION_LABEL:-$(basename "$PWD")}@$(hostname -s)"
if [ -f "$LOCK" ]; then
  PREV=$(head -1 "$LOCK"); WHEN=$(sed -n 2p "$LOCK")
  AGE=$(( ($(date +%s) - ${WHEN:-0}) / 60 ))
  if [ "$PREV" != "$WHO" ] && [ "$AGE" -lt 240 ]; then
    echo "  !! another session claimed this tree ${AGE}m ago: $PREV"
    echo "     Only ONE session should WRITE at a time. If that one is still working,"
    echo "     read here and let it finish, or ask it to commit first."
  fi
fi
printf '%s\n%s\n' "$WHO" "$(date +%s)" > "$LOCK"
UNC=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNC" -gt 0 ]; then
  echo "  !! $UNC uncommitted change(s) already in this tree, possibly another session's"
  echo "     work in progress. DO NOT run 'git add -A' — stage explicit paths only:"
  echo "       git add <the files you actually changed> && git commit"
  echo "     This has already gone wrong once: commit 7e03642 swallowed another"
  echo "     session's 5 extractions and a 319-line intro draft."
fi
exit 0
