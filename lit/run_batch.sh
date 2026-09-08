#!/bin/bash
# Extract a list of papers, one claude -p invocation per paper.
# One paper per process so a failure is isolated to that paper.
# usage: ./run_batch.sh <batch-name> <citekey> [citekey ...]

cd "$(dirname "$0")" || exit 1
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

BATCH="$1"; shift
mkdir -p logs
MASTER="logs/${BATCH}.log"

say() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$MASTER"; }

say "=== batch '$BATCH' starting: $# papers ==="
say "schema: $(grep -m1 '^\*\*Version' SCHEMA.md | tr -d '*')"

ok=0; skip=0; fail=0
for KEY in "$@"; do
  if [ -f "notes/$KEY.md" ]; then
    say "SKIP  $KEY (note already exists)"; skip=$((skip+1)); continue
  fi
  if [ ! -f "pdfs/$KEY.pdf" ]; then
    say "FAIL  $KEY (no PDF)"; fail=$((fail+1)); continue
  fi
  NP=$(pdfinfo "pdfs/$KEY.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
  say "START $KEY (${NP}p)"
  START=$(date +%s)

  PROMPT="You are extracting ONE paper into a structured note for a literature corpus. You are not writing prose and nothing you produce is a draft of anything.

WORKING DIRECTORY: $(pwd)
THE PAPER: citekey \`$KEY\`, at \`pdfs/$KEY.pdf\` ($NP pages).

HOW TO READ IT: run \`./pagetext.sh $KEY\`. This emits the full text with '===== PAGE n of N =====' markers so every quote carries a real page number. Read the WHOLE paper before writing anything. For a figure whose caption is genuinely insufficient to fill data_shape, render that page with 'pdftoppm -f <page> -l <page> -r 150 -png pdfs/$KEY.pdf /tmp/${KEY}_p<page>' and Read the PNG. Do this only where the caption truly does not carry the panel structure; each render costs real tokens.

FIRST: read SCHEMA.md. It is VERSION 3. Read the data_shape grammar section and the v2-to-v3 Changelog carefully. v3 fixed defects that five previous extractors hit, and the fixes only work if you follow them exactly. Note especially: slots are named by ROLE not screen position (vary/measure, not x/y); there is a series: slot for the colour dimension; there are five forms (PLOT, MATRIX, RENDER, TREE, SCHEMATIC); and the panel-splitting rule is split on mark or measure, never on facet alone.

THEN: write notes/$KEY.md with every field in SCHEMA.md, in schema order, under headings A through G, ending with a Tags section.

RULES THAT MATTER MORE THAN COMPLETENESS:
1. Read only this paper. Do not fill any field from memory of the literature or from what a similar paper did. If you are writing something you know rather than something you just read, stop and write NOT REPORTED.
2. NOT REPORTED is correct and expected. A note with every field populated is more suspicious than one with gaps.
3. oracle_leakage is the most important field. Work through all SEVEN routes in the schema separately, each with a verbatim quote and page, saying NONE FOUND per route where genuinely absent. Route 4 includes tuning a sweep RANGE on the evaluation set. Route 7 is design-level oracle use, which is weaker than pipeline leakage and must be labelled as such.
4. structural_priors_used is separate from oracle_leakage and is required. Design-time use of deposited structures is not a defect; record it there.
5. necessity_claims and novelty_claims are quoted VERBATIM with pages.
6. data_shape uses the v3 five-form grammar. Fill named slots in order.
7. hides only when a figure obscures its own result, including axis truncation. metric_saturation is numeric saturation only; do not record an axis break in both.
8. anti_memorization_design and _control are separate. NONE RUN is common and correct. controls_run is a separate table of what they actually ran.
9. states_generated and state_metric may be dual, joined by ' + '.
10. Leave comparable_to_ours EMPTY and why_it_matters EMPTY. Both belong to the user.
11. Tags ONLY from the fixed v3 vocabulary. If you need one that does not exist, do NOT invent it. Record under unresolved.
12. schema_version is v3. extracted_on is $(date +%Y-%m-%d). extractor is 'claude -p unattended batch $BATCH'.

Write the note. Then print a five-line summary: note size, fields filled vs NOT REPORTED, oracle_leakage verdict in one line, figure panel-group row count, and any tag you needed but could not use."

  if claude -p "$PROMPT" \
      --allowedTools "Bash Read Write Edit Glob Grep" \
      >> "logs/${BATCH}_${KEY}.log" 2>&1; then
    ELAPSED=$(( $(date +%s) - START ))
    if [ -f "notes/$KEY.md" ]; then
      say "OK    $KEY  ${ELAPSED}s  $(wc -c < "notes/$KEY.md" | tr -d ' ') chars"
      ok=$((ok+1))
    else
      say "FAIL  $KEY  ${ELAPSED}s  (ran but wrote no note)"; fail=$((fail+1))
    fi
  else
    say "FAIL  $KEY  (claude exited nonzero; see logs/${BATCH}_${KEY}.log)"; fail=$((fail+1))
  fi
done

say "=== batch '$BATCH' done: $ok ok, $skip skipped, $fail failed ==="
say "remaining un-extracted corpus-wide: $(./staleness.sh | wc -l | tr -d ' ')"
