#!/bin/bash
# Push the current manuscript to Overleaf, for sharing only.
# Overleaf is an EXPORT TARGET, not a workspace: manuscript/ in this repo is canonical.
# Never edit in the Overleaf web editor and expect it to come back.
cd "$(dirname "$0")" || exit 1
[ -d overleaf/.git ] || { echo "overleaf/ not cloned here. See CLAUDE.md."; exit 1; }
python3 analysis/sync_bib.py >/dev/null || exit 1
cp manuscript/main.tex manuscript/refs.bib overleaf/
cd overleaf || exit 1
if git diff --quiet && git diff --cached --quiet; then
  echo "Overleaf already up to date."; exit 0
fi
git add -A && git commit -q -m "Sync from manuscript/ ($(date '+%Y-%m-%d %H:%M'))" && git push -q origin main \
  && echo "pushed to Overleaf. Share via Overleaf's read-only link."
