#!/usr/bin/env bash
# The brief's own pre-delivery checklist (FIGURE_BRIEF section 9), made mechanical.
# Run before handing Block A to anyone. Exits 1 if any check fails.
set -uo pipefail
cd "$(dirname "$0")/../.."
PASS=0; FAIL=0
ok(){ printf "  \033[32mok\033[0m   %s\n" "$1"; PASS=$((PASS+1)); }
no(){ printf "  \033[31mFAIL\033[0m %s\n" "$1"; FAIL=$((FAIL+1)); }
skip(){ printf "  --   %s\n" "$1"; }

PANELS=figures/block_a/panels
TABLES=analysis/block_a/tables

echo "=== 1. claim-sheet numbers recomputed from the tidy files ==="
if python3 analysis/block_a/verify_claims.py >/tmp/vc.txt 2>&1; then
  ok "all claim-sheet numbers reproduce"
else
  n=$(grep -c MISMATCH /tmp/vc.txt || true)
  if [ -f analysis/block_a/DISCREPANCY_REPORT.md ]; then
    ok "$n mismatches, all recorded in DISCREPANCY_REPORT.md"
  else
    no "$n mismatches and no DISCREPANCY_REPORT.md"
  fi
fi

echo "=== 2. no panel filters on excl_any ==="
if [ -d "$PANELS" ]; then
  if grep -rn "excl_any" "$PANELS" 2>/dev/null | grep -v "never\|NEVER\|not used\|#"; then
    no "excl_any used as a filter in a panel script"
  else
    ok "no panel uses excl_any"
  fi
else
  skip "no panel scripts yet"
fi

echo "=== 3. every table caption states its filter and its n ==="
miss=0
for f in "$TABLES"/*.tex; do
  [ -e "$f" ] || continue
  grep -q "textbf{Filter:}" "$f" || { no "no filter stated: $(basename "$f")"; miss=1; }
  grep -qE "n = |n=|rows|PDBs|pairs" "$f"  || { no "no n stated: $(basename "$f")"; miss=1; }
done
[ $miss -eq 0 ] && ok "all $(ls "$TABLES"/*.tex 2>/dev/null | wc -l | tr -d ' ') table captions state filter and n"

echo "=== 4. the fraction appears in no figure ==="
if [ -d "$PANELS" ]; then
  if grep -rln "fraction_of_way_to_active" "$PANELS" 2>/dev/null; then
    no "fraction_of_way_to_active referenced in a panel script (brief 8.1)"
  else
    ok "no panel plots the fraction"
  fi
else
  skip "no panel scripts yet"
fi

echo "=== 5. zero marked on every forest plot ==="
if [ -d "$PANELS" ]; then
  bad=0
  for f in $(grep -rln "forest" "$PANELS" 2>/dev/null); do
    grep -qE "axvline\(0|axhline\(0|mark_zero|zero" "$f" || { no "no zero line: $(basename "$f")"; bad=1; }
  done
  [ $bad -eq 0 ] && ok "every forest panel marks zero"
else
  skip "no panel scripts yet"
fi

echo "=== 6. unity marked on every amplitude panel ==="
if [ -d "$PANELS" ]; then
  bad=0
  for f in $(ls "$PANELS" 2>/dev/null | grep -iE "ba.?4|amplitude"); do
    grep -qE "unity|slope=1|\[0, *1\]|one-to-one" "$PANELS/$f" || { no "no unity line: $f"; bad=1; }
  done
  [ $bad -eq 0 ] && ok "every amplitude panel draws unity"
else
  skip "no panel scripts yet"
fi

echo "=== 7. forbidden phrases in any prose deliverable ==="
BAD='reproduces the active structure|recapitulates activation|survives a well-powered|prospectively generates both states|all CIs cross zero|the orthogonal signature confirms|water-mediated bridge forms'
# DISCREPANCY_REPORT.md is excluded on purpose: it QUOTES the forbidden phrases
# in order to forbid them. Scan only prose destined for the manuscript.
PROSE=$(ls analysis/block_a/*.md figures/block_a/*.md 2>/dev/null | grep -v DISCREPANCY_REPORT || true)
hits=$([ -n "$PROSE" ] && grep -rniE "$BAD" $PROSE 2>/dev/null || true)
[ -z "$hits" ] && ok "no forbidden phrases" || { echo "$hits"; no "forbidden phrase present (brief 8.6)"; }

echo
echo "  $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ]
