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
report() { # label, file_a, file_b
  local out; out=$(comm -23 "$2" "$3")
  if [ -n "$out" ]; then
    echo; echo "  !! $1 ($(echo "$out"|wc -l|tr -d ' ')):"
    echo "$out" | sed 's/^/       /'
    fail=1
  fi
}
report "PDF with no extraction"            "$t/pdf"   "$t/note"
report "note with no PDF"                  "$t/note"  "$t/pdf"
report "note missing from INDEX"           "$t/note"  "$t/index"
report "INDEX block with no note"          "$t/index" "$t/note"
report "note missing from refs.bib"        "$t/note"  "$t/bib"
report "refs.bib entry with NO paper behind it (unread — do not cite)" "$t/bib" "$t/note"
[ $fail -eq 0 ] && echo "  all four sets agree"
exit $fail
