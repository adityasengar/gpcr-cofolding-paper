#!/usr/bin/env python3
"""Which works do our own held papers cite that the corpus does not hold?

Extracts every DOI from every held PDF (and every retrieved plain text), diffs
against refs.bib, and ranks what is missing by how many of our papers cite it.

    python3 validate/bibsweep.py            # report
    python3 validate/bibsweep.py --top 40   # longer list
    python3 validate/bibsweep.py --self-test

Why this exists. On 2026-09-14 a hand sweep of FIVE held PDFs' bibliographies
found nine works cited by our own corpus and absent from it, three of which were
load-bearing -- one was the paper the field cites for our own C8 claim. A hand
sweep of five is a judgement call; this is a mechanical check with a denominator,
which is the difference between "we looked" and "we know". A silent miss here
looks exactly like a clean result, so the script prints the denominator on every
run and refuses to report without passing its own self-test.
"""
import argparse, collections, os, re, subprocess, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
LIT  = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "bibsweep_text")
DOI_RE = re.compile(r'\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]*[A-Za-z0-9]')

def norm(doi):
    d = doi.lower().rstrip('.,;)')
    # strip trailing publisher junk that pdftotext glues on
    for tail in ('.pdf', '.full', '.abstract'):
        if d.endswith(tail): d = d[:-len(tail)]
    return d

def pdf_text(path):
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, os.path.basename(path) + ".txt")
    if os.path.exists(key) and os.path.getmtime(key) >= os.path.getmtime(path):
        return open(key, encoding="utf-8", errors="replace").read()
    try:
        t = subprocess.run(["pdftotext", "-layout", path, "-"],
                           capture_output=True, text=True, timeout=180).stdout
    except Exception:
        t = ""
    open(key, "w", encoding="utf-8").write(t)
    return t

def corpus_dois():
    s = open(os.path.join(LIT, "refs.bib"), encoding="utf-8").read()
    return {norm(d) for d in DOI_RE.findall(s)}

def sources():
    out = []
    pdir = os.path.join(LIT, "pdfs")
    if os.path.isdir(pdir):
        out += [os.path.join(pdir, f) for f in sorted(os.listdir(pdir)) if f.endswith(".pdf")]
    tdir = os.path.join(LIT, "source", "pending_text")
    if os.path.isdir(tdir):
        out += [os.path.join(tdir, f) for f in sorted(os.listdir(tdir)) if f.endswith(".txt")]
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    have = corpus_dois()
    srcs = sources()

    cited = collections.defaultdict(set)   # doi -> {citing citekeys}
    scanned, empty = 0, []
    for p in srcs:
        key = os.path.basename(p).rsplit(".", 1)[0]
        t = pdf_text(p) if p.endswith(".pdf") else open(p, encoding="utf-8", errors="replace").read()
        if len(t.strip()) < 500:
            empty.append(key); continue
        scanned += 1
        for d in DOI_RE.findall(t):
            d = norm(d)
            if d not in have:
                cited[d].add(key)

    # a DOI cited by only one paper is usually that paper's own self-citation or a
    # data DOI; rank by breadth, which is what "the field cites this" looks like
    ranked = sorted(cited.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    if a.self_test:
        probe = "10.9999/definitely-not-real-doi"
        assert probe not in have, "self-test probe collides with a real DOI"
        real = next(iter(have)) if have else None
        ok = real is not None and real in have
        print(f"self-test  can-find-absent: OK   can-find-present: {'OK' if ok else 'BROKEN'}")
        print(f"           refs.bib DOIs parsed: {len(have)}")
        return 0 if ok else 2

    print(f"sources scanned      : {scanned} of {len(srcs)} "
          f"({len(srcs)-scanned} unreadable/too short)")
    if empty:
        print(f"  unreadable         : {', '.join(empty[:8])}{' …' if len(empty)>8 else ''}")
    print(f"DOIs in refs.bib     : {len(have)}")
    print(f"distinct cited DOIs not in corpus : {len(cited)}")
    print(f"  cited by >=2 of our papers      : {sum(1 for _,v in cited.items() if len(v)>=2)}")
    print(f"  cited by >=3                    : {sum(1 for _,v in cited.items() if len(v)>=3)}")
    print()
    print(f"top {a.top} by number of our own papers citing them:")
    for d, who in ranked[:a.top]:
        w = ", ".join(sorted(who)[:4]) + (" …" if len(who) > 4 else "")
        print(f"  {len(who):>3}  {d:<44} {w}")

    if a.json:
        json.dump({d: sorted(v) for d, v in ranked}, open("/dev/stdout", "w"), indent=1)
    return 0

if __name__ == "__main__":
    sys.exit(main())
