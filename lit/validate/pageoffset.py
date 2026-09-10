#!/usr/bin/env python3
"""Standing check: does a note's "p.N" mean the Nth PDF page or the printed folio N?

For any article whose printed pagination does not start at 1 these differ, and a
citation built from the wrong one sends a reader to a page that does not exist in
the published article. We hit this on georgiou2025heterogeneity, where notes carried
PDF pages and the article is printed at 3691-3728.

DISCOVERY: for PDF pages 2..7, find the offset k such that (pdf_page + k) appears on
the page for at least MIN_HITS of them.
VALIDATION, in priority order:
  1. refs.bib gives a page range  -> k is CONFIRMED iff k == first_page - 1.
  2. no page range in refs.bib    -> k is accepted only if it is large (> SMALL) AND
     the folio sits in a running header or footer. Small offsets on preprints are
     numeric coincidence, not pagination.
Run:  python3 validate/pageoffset.py
"""
import re, subprocess, pathlib

SAMPLE, MIN_HITS, SMALL = range(2, 8), 3, 20
BIB = pathlib.Path("refs.bib").read_text()

def first_printed_page(key):
    m = re.search(r'@\w+\{' + re.escape(key) + r',.*?\n\}', BIB, re.S)
    if not m: return None
    pg = re.search(r'pages\s*=\s*\{\s*(\d+)', m.group(0))
    return int(pg.group(1)) if pg else None

def analyse(pdf):
    try:
        n = int(subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
                .stdout.split("Pages:")[1].split()[0])
    except Exception:
        return 0, "unreadable"
    pages = [p for p in SAMPLE if p <= n]
    if len(pages) < MIN_HITS: return 0, "too short to sample"
    text = {}
    for p in pages:
        text[p] = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"],
                                 capture_output=True, text=True).stdout
    ints = {p: set(int(x) for x in re.findall(r'\b(\d{1,6})\b', t)) for p, t in text.items()}
    if all(not v for v in ints.values()): return 0, "no text layer (scanned)"

    want = first_printed_page(pdf.stem)
    if want is not None:
        k = want - 1
        hits = sum(1 for p in pages if (p + k) in ints[p])
        if k == 0: return 0, "bib says article starts at p.1"
        if hits >= MIN_HITS: return k, "CONFIRMED against refs.bib (starts p.%d)" % want
        return 0, "bib says starts p.%d but folio not found - check edition" % want

    cands = sorted({k for k in range(SMALL + 1, 30000)
                    if sum(1 for p in pages if (p + k) in ints[p]) >= MIN_HITS})
    for k in cands:
        ok = 0
        for p in pages:
            lines = [l.strip() for l in text[p].split("\n") if l.strip()]
            folio = str(p + k)
            for l in lines[:2] + lines[-2:]:
                low = l.lower()
                if "doi" in low or "http" in low or "arxiv" in low:
                    continue                      # DOIs contain year-like digit runs
                if re.search(r'(?<![\d.])' + folio + r'(?![\d.])', l):
                    ok += 1; break
        if ok >= MIN_HITS:
            return k, "confirmed by running header/footer (no page range in refs.bib)"
    return 0, "no printed folio detected"

rows = [(p.stem,) + analyse(p) for p in sorted(pathlib.Path("pdfs").glob("*.pdf"))]
flagged = [(k, o, s) for k, o, s in rows if o]
print("PAPERS WHERE PRINTED FOLIO != PDF PAGE  (printed = pdf + offset)\n")
for k, o, s in flagged:
    print("  %-30s +%-7d %s" % (k, o, s))
print("\n  %d of %d PDFs need conversion; the rest are 1-indexed or have no folio." %
      (len(flagged), len(rows)))
notes_only = [k for k, o, s in rows if not o and "scanned" in s]
if notes_only: print("  scanned, verify by hand: %s" % ", ".join(notes_only))
