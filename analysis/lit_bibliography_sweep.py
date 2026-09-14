#!/usr/bin/env python3
"""Which works do our own held papers cite that the corpus does not contain?

WHY THIS IS A SCRIPT AND NOT A JUDGEMENT CALL.

On 2026-09-14 a lit survey agent found NINE works cited inside notes we hold and
absent from `refs.bib` -- by hand, from the bibliographies of FIVE PDFs. It also
got one wrong in the other direction, reporting a paper as missing that was
already extracted, with a 41 KB note and a PDF on disk.

Both failure directions matter and they are not symmetric. A false ABSENCE claim
costs credibility (`audit_asks.py` exists for the same reason on the data side).
A missed gap is worse and is invisible: "no prior work does X" is the highest-cost
answer this corpus can produce, because it is confident, well-formed, and flatters
the manuscript's novelty claim. `lit/CLAUDE.md` says exactly this.

Five PDFs of seventy-five is a sample with no denominator. This sweeps all of
them, so the answer carries one.

WHAT IT DOES. Extracts every DOI and arXiv id appearing in each held PDF, drops
the paper's own, and diffs against `lit/refs.bib`. Ranks what is missing by HOW
MANY DISTINCT HELD PAPERS CITE IT -- a work five of our papers cite is load-
bearing in this literature in a way one cited once is not, and that ranking is
the thing a human cannot do by reading five bibliographies.

WHAT IT DOES NOT DO. It does not decide what to extract; the lit session owns
`lit/**` and that judgement. It reports a ranked, checkable list and nothing else.
A DOI is also not a complete view -- older and conference works often carry none,
and the nine found by hand include several with no DOI at all (ICML 2026,
OpenReview). So this is a FLOOR on what is missing, never a ceiling, and it says
so in its own output.

Usage:  python3 analysis/lit_bibliography_sweep.py [--top N]
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFS = os.path.join(ROOT, "lit", "pdfs")
REFS = os.path.join(ROOT, "lit", "refs.bib")
CACHE = os.path.join(ROOT, "lit", ".bibsweep_cache")

# A DOI runs to whitespace or a delimiter; trailing sentence punctuation is not
# part of it. Getting this wrong inflates the "missing" list with near-duplicates
# of DOIs we DO hold, which is the false-absence failure this script exists to
# avoid producing itself.
DOI = re.compile(r"\b(10\.\d{4,9}/[^\s\"'<>,;()\[\]]+)", re.I)
ARXIV = re.compile(r"\barXiv[:\s]\s*(\d{4}\.\d{4,5})", re.I)
TRAIL = ".,;:)]}>'\"-"


def norm(d):
    d = d.strip().lower()
    while d and d[-1] in TRAIL:
        d = d[:-1]
    return d


def text_of(pdf):
    """pdftotext output, cached -- 75 PDFs is ~450 MB and this gets re-run."""
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, os.path.basename(pdf)[:-4] + ".txt")
    if os.path.exists(key) and os.path.getmtime(key) >= os.path.getmtime(pdf):
        return open(key, encoding="utf-8", errors="replace").read()
    try:
        out = subprocess.run(["pdftotext", "-q", pdf, "-"], capture_output=True,
                             timeout=120).stdout.decode("utf-8", "replace")
    except (subprocess.TimeoutExpired, OSError):
        out = ""
    open(key, "w", encoding="utf-8").write(out)
    return out


def main():
    top = 40
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])

    bib = open(REFS, encoding="utf-8", errors="replace").read()
    have = {norm(d) for d in DOI.findall(bib)}
    have_arx = {a.lower() for a in ARXIV.findall(bib)}
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))

    pdfs = sorted(f for f in os.listdir(PDFS) if f.endswith(".pdf"))
    cited = {}                      # doi -> set(citing citekeys)
    cited_arx = {}
    own = set()
    for f in pdfs:
        key = f[:-4]
        body = text_of(os.path.join(PDFS, f))
        if not body:
            print("  (no text extracted: %s)" % f)
            continue
        ds = {norm(d) for d in DOI.findall(body)}
        # The paper's own DOI is whichever of its DOIs refs.bib records for it.
        entry = re.search(r"@\w+\{%s,(.*?)\n@" % re.escape(key), bib + "\n@", re.S)
        mine = {norm(d) for d in DOI.findall(entry.group(1))} if entry else set()
        own |= mine
        for d in ds - mine:
            cited.setdefault(d, set()).add(key)
        for a in {x.lower() for x in ARXIV.findall(body)}:
            cited_arx.setdefault(a, set()).add(key)

    missing = {d: c for d, c in cited.items() if d not in have}
    missing_arx = {a: c for a, c in cited_arx.items()
                   if a not in have_arx and not any(a in d for d in have)}

    print("=" * 78)
    print("LIT BIBLIOGRAPHY SWEEP -- what our own papers cite that we do not hold")
    print("=" * 78)
    print("  held PDFs scanned                %d" % len(pdfs))
    print("  refs.bib entries                 %d  (%d carry a DOI)"
          % (len(keys), len(have)))
    print("  distinct DOIs cited by held PDFs %d" % len(cited))
    print("  ... of those, already in refs.bib %d" % (len(cited) - len(missing)))
    print("  ... NOT in refs.bib               %d" % len(missing))
    print("  distinct arXiv ids not in refs.bib %d" % len(missing_arx))
    print()
    print("  Ranked by how many DISTINCT held papers cite it. A work cited by")
    print("  several of our own sources is load-bearing in this literature.")
    print()
    rank = sorted(missing.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for d, c in rank[:top]:
        print("  %2d  %-52s" % (len(c), d[:52]))
        print("      cited by: %s" % ", ".join(sorted(c)[:6]))
    if len(rank) > top:
        print("  ... %d more with fewer citers (--top to see them)" % (len(rank) - top))

    print()
    print("  arXiv ids cited and not held, by citer count:")
    for a, c in sorted(missing_arx.items(), key=lambda kv: -len(kv[1]))[:12]:
        print("  %2d  arXiv:%-14s cited by: %s"
              % (len(c), a, ", ".join(sorted(c)[:5])))

    print()
    print("  FLOOR, NOT A CEILING. Conference and older works often carry no DOI")
    print("  and no arXiv id -- several of the nine found by hand on 2026-09-14")
    print("  (ICML 2026, OpenReview) would not appear here at all. A clean run")
    print("  means no DOI-bearing gap, never no gap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
