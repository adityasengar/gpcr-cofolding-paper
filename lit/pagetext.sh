#!/bin/bash
# Emit a PDF's text with explicit page markers so extracted quotes carry real page numbers.
# usage: ./pagetext.sh <citekey> [first] [last]
cd "$(dirname "$0")"
f="pdfs/$1.pdf"; [ -f "$f" ] || { echo "no such paper: $1" >&2; exit 1; }
n=$(pdfinfo "$f" | awk '/^Pages/{print $2}')
a=${2:-1}; b=${3:-$n}
for p in $(seq "$a" "$b"); do
  echo "===== PAGE $p of $n ====="
  pdftotext -f "$p" -l "$p" -layout "$f" - 2>/dev/null
done
