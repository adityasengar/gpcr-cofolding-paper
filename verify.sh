#!/bin/bash
# Self-check. Run on EITHER laptop; it adapts to what that machine holds.
#   ./verify.sh
# Exit 0 = everything that should work here does.
cd "$(dirname "$0")" || exit 1
ME=$(cat .machine 2>/dev/null || hostname -s)
FAIL=0
ok(){ printf "  %-44s %s\n" "$1" "$2"; }
bad(){ printf "  %-44s %s\n" "$1" "$2"; FAIL=1; }

echo "=========== verify: $ME  $(date '+%Y-%m-%d %H:%M') ==========="

# --- git ---
git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  && ok "git repo" "OK" || bad "git repo" "NOT A REPO"
git ls-remote --exit-code origin >/dev/null 2>&1 \
  && ok "remote reachable" "OK" || bad "remote reachable" "FAIL (auth? network?)"
UP=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "?")
DN=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "?")
[ "$UP" = "0" ] && ok "up to date with remote" "OK" || bad "up to date with remote" "$UP commit(s) BEHIND — pull"
[ "$DN" = "0" ] && ok "nothing unpushed" "OK" || bad "nothing unpushed" "$DN commit(s) UNPUSHED — push"
UNC=$(git status --porcelain | wc -l | tr -d ' ')
[ "$UNC" = "0" ] && ok "working tree clean" "OK" || ok "working tree" "$UNC uncommitted (an agent may be mid-edit)"

# --- corpus ---
lit/corpus_check.sh >/dev/null 2>&1 && ok "corpus consistent" "OK" \
  || ok "corpus" "drift reported — run lit/corpus_check.sh"
ok "notes present" "$(ls lit/notes/*.md 2>/dev/null | wc -l | tr -d ' ')"
ok "PDFs present" "$(ls lit/pdfs/*.pdf 2>/dev/null | wc -l | tr -d ' ') (0 is correct off the author machine)"

# --- tex ---
if command -v /Library/TeX/texbin/pdflatex >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1; then
  tex/check_tex.sh 2>&1 | grep -q "all .* pinned packages present" \
    && ok "TeX matches the pin" "OK" || bad "TeX matches the pin" "DRIFT — run ./tex/check_tex.sh"
  OUT=$(./manuscript/build.sh 2>&1)
  B=$(echo "$OUT" | grep -oE 'bibitems : [0-9]+' | grep -oE '[0-9]+')
  U=$(echo "$OUT" | grep -oE 'undefined citations : [0-9]+' | grep -oE '[0-9]+')
  [ "${U:-1}" = "0" ] && ok "manuscript builds" "$B bibitems, 0 undefined" \
                      || bad "manuscript builds" "${U:-?} undefined citation(s)"
  ./manuscript/build.sh clean >/dev/null 2>&1
else
  bad "TeX" "pdflatex not found — see tex/SETUP.md"
fi

# --- data ---
python3 analysis/fingerprint.py --check >/dev/null 2>&1 \
  && ok "data fingerprint" "OK (or absent by design)" || bad "data fingerprint" "CHANGED — re-derive RESULTS.md"
python3 analysis/q.py ladder >/dev/null 2>&1 && ok "analysis queries run" "OK" || bad "analysis queries" "FAIL"

# --- bibliography ---
T=$(mktemp); cp manuscript/refs.bib "$T" 2>/dev/null
python3 analysis/sync_bib.py >/dev/null 2>&1
cmp -s "$T" manuscript/refs.bib && ok "manuscript/refs.bib in sync" "OK" \
  || bad "manuscript/refs.bib" "STALE — commit the regenerated file"
rm -f "$T"

echo
[ $FAIL -eq 0 ] && echo "  ALL CHECKS PASSED on $ME" || echo "  SOME CHECKS FAILED on $ME (see above)"
exit $FAIL
