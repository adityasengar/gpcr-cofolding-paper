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
N=$(python3 -c "import pandas,sys; print(len(pandas.read_csv('data/block_a/01_rows/block_a_rows.csv')))" 2>/dev/null)
[ "$N" = "9490" ] && ok "block A rows" "9,490" || bad "block A rows" "expected 9,490, got ${N:-none}"
./analysis/block_a/check_deliverables.sh >/dev/null 2>&1 \
  && ok "block A deliverables" "all checks pass" || bad "block A deliverables" "see check_deliverables.sh"

# --- redo campaign ---
python3 redo/gates/layout.py >/dev/null 2>&1 \
  && ok "redo layout" "7 checks clean" || bad "redo layout" "VIOLATED — run redo/gates/layout.py"
python3 redo/build/manifest.py --check >/dev/null 2>&1 \
  && ok "redo inputs manifest" "in sync" || bad "redo inputs manifest" "STALE — python3 redo/build/manifest.py"
python3 redo/gates/run_receipt.py >/dev/null 2>&1 \
  && ok "redo run receipts" "accepted (or no runs yet)" || bad "redo run receipts" "REFUSED — run redo/gates/run_receipt.py"
# The check COUNT is read from the gate's own tally, never asserted here. Both
# these lines carried hand-written counts and both had gone stale by 2026-09-12
# (ligands said 5 against 10, drule said 6 against 14) -- the same failure class
# as the three documents that said "33 experiments in 9 groups" against a body
# of 45 in 10. A count in a label is a claim nobody re-derives.
LIG=$(python3 redo/gates/ligands.py 2>/dev/null | grep -oE "CLEAN -- [0-9]+ checks pass" | grep -oE "[0-9]+")
python3 redo/gates/ligands.py >/dev/null 2>&1 \
  && ok "redo ligand table" "${LIG:-?} checks clean" || bad "redo ligand table" "FAILED — run redo/gates/ligands.py"
DRU=$(python3 redo/gates/drule.py 2>/dev/null | grep -oE "CLEAN -- [0-9]+ checks pass" | grep -oE "[0-9]+")
python3 redo/gates/drule.py >/dev/null 2>&1 \
  && ok "redo decoy rule" "${DRU:-?} checks clean; pool built, selection run" || bad "redo decoy rule" "FAILED — run redo/gates/drule.py"
G0=$(python3 redo/gates/g0_preflight.py 2>/dev/null | grep -E "FROZEN|NOT FROZEN" | tail -1 | sed 's/^ *//')
G1=$(python3 redo/gates/g1_preflight.py 2>/dev/null | grep -E "^[0-9]+ passed" | tail -1)
case "$G0" in "FROZEN"*) ok "redo group 0 gate" "$G0" ;; *) bad "redo group 0 gate" "${G0:-did not run}" ;; esac
case "$G1" in *"0 failed"*) ok "redo group 1 gate" "$G1" ;; *) bad "redo group 1 gate" "${G1:-did not run}" ;; esac
G2=$(python3 redo/gates/g2_preflight.py 2>/dev/null | grep -E "^[0-9]+ passed" | tail -1)
case "$G2" in *"0 failed"*) ok "redo group 2 gate" "$G2" ;; *) bad "redo group 2 gate" "${G2:-did not run}" ;; esac

# --- bibliography ---
T=$(mktemp); cp manuscript/refs.bib "$T" 2>/dev/null
python3 analysis/sync_bib.py >/dev/null 2>&1
cmp -s "$T" manuscript/refs.bib && ok "manuscript/refs.bib in sync" "OK" \
  || bad "manuscript/refs.bib" "STALE — commit the regenerated file"
rm -f "$T"

echo
[ $FAIL -eq 0 ] && echo "  ALL CHECKS PASSED on $ME" || echo "  SOME CHECKS FAILED on $ME (see above)"
exit $FAIL
