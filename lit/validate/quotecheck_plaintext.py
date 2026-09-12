#!/usr/bin/env python3
"""Verify the double-quoted verbatim spans in a note against a plain-text source.

For notes extracted from full-text XML/HTML rather than a PDF, where
validate/quotes.py's PDF path does not apply.

  python3 validate/quotecheck_plaintext.py <source.txt> <note.md>

Checks every "..." span that appears inside a markdown blockquote, joining
lines within a span. Prints the DENOMINATOR, and self-tests that it can both
fail and pass before reporting -- a checker never shown to fail is not evidence.
"""
import re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    for a, b in [("’","'"),("‘","'"),("“",'"'),("”",'"'),
                 ("–","-"),("—","-"),("−","-"),("∼","~")]:
        s = s.replace(a, b)
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

def main(srcpath, notepath):
    src = norm(open(srcpath, encoding="utf-8").read())
    note = open(notepath, encoding="utf-8").read()

    # keep only blockquote lines, strip the marker, join into one stream so a
    # span may wrap lines; then pull every "..." span out of that stream.
    bq = " ".join(m.group(1) for m in
                  re.finditer(r'^\s*(?:\d+\.\s*)?>\s?(.*)$', note, re.M))
    spans = re.findall(r'"([^"]{30,})"', bq)

    ok, bad = 0, []
    for q in spans:
        frags = [f for f in re.split(r'…|\.\.\.', q) if len(norm(f)) > 25]
        miss = [f for f in frags if norm(f) not in src]
        if miss:
            bad.append((q, miss))
        else:
            ok += 1

    print(f"source : {srcpath}")
    print(f"note   : {notepath}")
    print(f"quoted spans found : {len(spans)}")
    print(f"  VERIFIED         : {ok}")
    print(f"  FAILED           : {len(bad)}")
    for q, m in bad:
        print(f"   !! {q[:120]}")
        for f in m:
            print(f"      MISSING FRAGMENT: {f[:120]}")

    # the checker must be shown to fail and to pass on this very source
    anchor = " ".join(src.split()[:14])
    broken = " ".join(src.split()[:7]) + " riding a unicycle through the spectrometer"
    t1 = anchor in src
    t2 = norm(broken) not in src
    print(f"\nself-test  can-pass: {'OK' if t1 else 'BROKEN'}   can-fail: {'OK' if t2 else 'BROKEN'}")
    if not (t1 and t2):
        print("CHECKER IS BROKEN -- its result above is not evidence.")
        return 2
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
