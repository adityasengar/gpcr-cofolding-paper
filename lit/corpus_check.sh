#!/bin/bash
# Full corpus consistency check across all four sets: pdfs, notes, INDEX, refs.bib.
# Replaces staleness.sh, which only compared pdfs against notes and so could not see
# a bibliography entry with no paper behind it.
cd "$(dirname "$0")" || exit 1
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
find pdfs  -name '*.pdf' -exec basename {} .pdf \; 2>/dev/null | sort > "$t/pdf"
find notes -maxdepth 1 -name '*.md' -exec basename {} .md \; 2>/dev/null | sort > "$t/note"
grep -oE '^### [^ ]+' INDEX.md | cut -d' ' -f2 | sort > "$t/index"
grep -oE '^@[a-zA-Z]+[[:space:]]*\{[[:space:]]*[^,[:space:]]+' refs.bib \
  | sed 's/.*{[[:space:]]*//' | sort > "$t/bib"

printf "  %-10s %s\n" pdfs "$(wc -l <"$t/pdf"|tr -d ' ')" notes "$(wc -l <"$t/note"|tr -d ' ')" \
                       INDEX "$(wc -l <"$t/index"|tr -d ' ')" refs.bib "$(wc -l <"$t/bib"|tr -d ' ')"
fail=0
# hard=1 marks real drift (sets exit 1); hard=0 is an expected notice.
report() { # label, file_a, file_b, hard
  local out; out=$(comm -23 "$2" "$3")
  if [ -n "$out" ]; then
    echo; echo "  ${4:+!! }$1 ($(echo "$out"|wc -l|tr -d ' ')):"
    echo "$out" | sed 's/^/       /'
    [ -n "$4" ] && fail=1
  fi
}
# PDFs are excluded from the shared repo, so on a second machine every note looks
# orphaned. Reporting 66 phantom problems trains the reader to ignore this check.
if [ -s "$t/pdf" ]; then
  report "PDF with no extraction"          "$t/pdf"   "$t/note" hard
  # Expected, not drift: some publishers bot-wall the PDF, so the note was made from
  # PMC XML or publisher HTML and says so. Those cite as [citekey], not [citekey p.N].
  report "note with no PDF (read from HTML/XML; cite without a page)" "$t/note" "$t/pdf"
else
  echo "  (lit/pdfs/ not on this machine — PDF checks skipped, notes only)"
fi
report "note missing from INDEX"           "$t/note"  "$t/index" hard
report "INDEX block with no note"          "$t/index" "$t/note" hard
report "note missing from refs.bib"        "$t/note"  "$t/bib" hard
report "refs.bib entry with NO paper behind it (unread — do not cite)" "$t/bib" "$t/note" hard
[ $fail -eq 0 ] && echo "  all four sets agree"

# GAPS.md is generated, not hand-written. It was hand-built at 66 notes and reported a stale
# count for two days before anyone noticed, so staleness is now a check rather than a habit.
if [ -f build_gaps.py ]; then
  if python3 build_gaps.py --check 2>/dev/null; then
    echo "  GAPS.md                                    up to date"
  else
    echo "  !! GAPS.md is STALE — run: python3 lit/build_gaps.py"
    fail=1
  fi
fi

exit $fail
