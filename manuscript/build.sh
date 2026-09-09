#!/bin/bash
# Build the manuscript. Same command on both laptops.
#   ./manuscript/build.sh          compile
#   ./manuscript/build.sh clean    remove build artifacts
export PATH="/Library/TeX/texbin:$PATH"
cd "$(dirname "$0")" || exit 1

if [ "$1" = "clean" ]; then
  rm -f main.aux main.bbl main.blg main.log main.out main.toc main.fls main.fdb_latexmk main.synctex.gz
  echo "cleaned"; exit 0
fi

command -v pdflatex >/dev/null || { echo "pdflatex not found — see tex/SETUP.md"; exit 1; }

if command -v latexmk >/dev/null; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex || exit 1
else
  echo "(latexmk missing — falling back to the manual sequence; see tex/SETUP.md)"
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null || { echo "pass 1 failed"; exit 1; }
  bibtex main >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null || exit 1
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null || exit 1
fi

UNDEF=$(grep -c "Citation.*undefined" main.log 2>/dev/null | head -1 | tr -d "[:space:]"); UNDEF=${UNDEF:-0}
echo "  bibitems : $(grep -c bibitem main.bbl 2>/dev/null || echo 0)"
echo "  undefined citations : $UNDEF"
[ "$UNDEF" -gt 0 ] && { echo "  !! a cited key is not in refs.bib, or the paper is unread and therefore hidden"; \
  grep -o "Citation \`[^']*'" main.log | sort -u | sed 's/^/     /'; }
echo "  output   : manuscript/main.pdf ($(du -h main.pdf 2>/dev/null | cut -f1))"
