#!/bin/bash
# Run at the START of every session, on either machine, before doing anything else.
# Answers one question: what changed since THIS machine last worked on the paper.
cd "$(dirname "$0")" || exit 1
ME=$(cat .machine 2>/dev/null || hostname -s)

echo "=============================================================="
echo " machine: $ME     $(date '+%Y-%m-%d %H:%M')"
echo "=============================================================="

if [ -d .git ]; then
  echo
  if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    echo "--- pulling ---"
    git pull --ff-only 2>&1 | sed 's/^/  /'
  else
    echo "--- no remote configured yet; this machine is the only copy ---"
  fi
  LAST=$(git log --format='%H %s' -n 200 | grep -m1 "session-end($ME)" | cut -d' ' -f1)
  echo
  if [ -n "$LAST" ]; then
    N=$(git rev-list --count "$LAST"..HEAD)
    echo "--- $N commits since $ME last signed off ---"
    git log --format='  %ad %an: %s' --date=short "$LAST"..HEAD | head -30
  else
    echo "--- no previous sign-off from $ME; showing last 15 commits ---"
    git log --format='  %ad %an: %s' --date=short -15
  fi
  echo
  echo "--- files changed in that window ---"
  { [ -n "$LAST" ] && git diff --stat "$LAST"..HEAD || git diff --stat HEAD~5..HEAD; } \
    2>/dev/null | tail -20 | sed 's/^/  /'
else
  echo; echo "  (not a git repo yet — see CLAUDE.md 'Working across two machines')"
fi

echo
echo "--- handoff notes: last 2 entries of SESSIONS.md ---"
awk '/^## /{n++} n<=2' SESSIONS.md 2>/dev/null | head -40 | sed 's/^/  /'

echo
echo "--- corpus integrity ---"
[ -x lit/corpus_check.sh ] && lit/corpus_check.sh 2>&1 | sed 's/^/  /'

echo
echo "--- data freshness ---"
python3 analysis/fingerprint.py --check 2>&1 | sed 's/^/  /'

echo
echo "--- local-only assets (absent on a fresh clone) ---"
printf "  lit/pdfs/   %s\n" "$([ -d lit/pdfs ] && echo "$(ls lit/pdfs/*.pdf 2>/dev/null|wc -l|tr -d ' ') PDFs" || echo 'ABSENT — notes only, cannot open a PDF here')"
printf "  rows_enriched_v3_7.csv  %s\n" "$([ -f rows_enriched_v3_7.csv ] && echo present || echo 'ABSENT')"
echo
echo "--- bibliography drift (lit/refs.bib -> paper_tex/refs.bib) ---"
if [ -f paper_tex/refs.bib ]; then
  python3 analysis/sync_bib.py >/tmp/_bib.log 2>&1
  if [ -d paper_tex/.git ] && ! git -C paper_tex diff --quiet -- refs.bib 2>/dev/null; then
    echo "  !! paper_tex/refs.bib is STALE — regenerated, commit and push it to Overleaf"
  else
    echo "  in sync"
  fi
else
  echo "  paper_tex/ not cloned on this machine"
fi
echo
echo "Read CLAUDE.md next. Then wait."
