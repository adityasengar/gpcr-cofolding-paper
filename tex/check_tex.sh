#!/bin/bash
# Verify this machine's TeX matches the pinned environment.
# Package drift is the failure mode: a document that builds on one laptop and not
# the other, with no warning until it happens.
export PATH="/Library/TeX/texbin:$PATH"
cd "$(dirname "$0")/.." || exit 1
PIN=tex/tex-packages.txt
command -v tlmgr >/dev/null || { echo "  tlmgr not found — is BasicTeX installed?"; exit 1; }

echo "  distribution : $(tlmgr --version 2>/dev/null | grep -m1 'TeX Live' | sed 's/^ *//')"
for t in pdflatex bibtex latexmk; do
  printf "  %-13s %s\n" "$t" "$(command -v $t >/dev/null && echo present || echo 'MISSING')"
done

HERE=$(mktemp); tlmgr list --only-installed 2>/dev/null | sed 's/^i //;s/:.*//' | sort > "$HERE"
MISS=$(comm -23 <(grep -v '^#' "$PIN" | sort) "$HERE")
EXTRA=$(comm -13 <(grep -v '^#' "$PIN" | sort) "$HERE")
rm -f "$HERE"

if [ -n "$MISS" ]; then
  echo "  !! missing $(echo "$MISS" | wc -l | tr -d ' ') pinned packages:"
  echo "$MISS" | head -12 | sed 's/^/       /'
  echo "     install with:  sudo tlmgr install $(echo $MISS | tr '\n' ' ')"
else
  echo "  packages     all $(grep -vc '^#' "$PIN") pinned packages present"
fi
[ -n "$EXTRA" ] && { echo "  note: $(echo "$EXTRA" | wc -l | tr -d ' ') extra packages here not in the pin"; \
  echo "        if the manuscript needs one, re-pin so the other laptop gets it too"; }
exit 0
