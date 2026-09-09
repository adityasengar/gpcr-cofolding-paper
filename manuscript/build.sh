#!/bin/bash
# Build the manuscript. Same command on both laptops.
#   ./manuscript/build.sh          compile
#   ./manuscript/build.sh clean    remove build artifacts
export PATH="/Library/TeX/texbin:$PATH"
cd "$(dirname "$0")" || exit 1

if [ "$1" = "clean" ]; then
  rm -f main.aux main.bbl main.blg main.log main.out main.toc main.fls main.fdb_latexmk main.synctex.gz
  rm -f si.aux si.bbl si.blg si.log si.out si.toc si.fls si.fdb_latexmk si.synctex.gz
  echo "cleaned"; exit 0
fi

command -v pdflatex >/dev/null || { echo "pdflatex not found — see tex/SETUP.md"; exit 1; }

if command -v latexmk >/dev/null; then
  if ! latexmk -pdf -silent -interaction=nonstopmode -halt-on-error main.tex >/tmp/_latexmk.log 2>&1; then
    echo "  BUILD FAILED — last 25 lines:"; tail -25 /tmp/_latexmk.log | sed 's/^/     /'; exit 1
  fi
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
# A missing panel is as loud as an undefined citation. figures/out/ is
# gitignored on purpose (regenerable), so a fresh clone must be told to run the
# panel scripts rather than shown a cryptic LaTeX error.
MISS=$(grep -oE "File \`[^']*' not found" main.log 2>/dev/null | sort -u)
[ -n "$MISS" ] && { echo "  !! missing graphic — run: python3 figures/block_a/panels/<name>.py"; \
  echo "$MISS" | sed 's/^/     /'; }
echo "  output   : manuscript/main.pdf ($(du -h main.pdf 2>/dev/null | cut -f1)), $(grep -oE "([0-9]+) pages" main.log | tail -1)"

# --- supplementary information -------------------------------------------
if [ -f si.tex ]; then
  if latexmk -pdf -silent -interaction=nonstopmode -halt-on-error si.tex >/tmp/_si.log 2>&1; then
    echo "  SI       : manuscript/si.pdf ($(du -h si.pdf 2>/dev/null | cut -f1)), $(grep -oE "([0-9]+) pages" si.log | tail -1)"
  else
    echo "  SI BUILD FAILED — last 20 lines:"; tail -20 /tmp/_si.log | sed 's/^/     /'
  fi
fi
