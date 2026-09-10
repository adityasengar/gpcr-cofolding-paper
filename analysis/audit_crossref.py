#!/usr/bin/env python3
"""Do the captions, the body and the figure ledger agree with each other?

WHY THIS AXIS. The number registry checks each number against the DATA. It does
not check numbers against EACH OTHER, so the same quantity can appear in
results.tex, in a caption in figures.tex, and in figures/FIGURES.md with three
different values and every one of them individually registered. A caption that
disagrees with the body is the cheapest thing for a referee to find and the
hardest thing to see while writing, because the two are never read side by side.

WHAT IT LOOKS FOR. Claims of the shape "N of M" -- a count against a
denominator. These carry most of this paper's factual weight (cells that fire,
receptors that move, references that deviate) and they have a property that
makes them mechanically checkable without knowing what they mean: for a given
N, the M should not vary between documents describing the same result.

The tool reports pairs, not verdicts. Two documents can legitimately say "108 of
159" and "111 of 160" about different arms of the same figure -- as this paper
does, because exclusions empty one cognate cell and no apo cell. So a
disagreement is a QUESTION, not a defect, and the output says which document to
read first rather than which number to change.

WHAT IT DELIBERATELY DOES NOT DO. It does not try to decide which value is
right. That needs the data, and the three verify_claims.py already do it.

Usage:  python3 analysis/audit_crossref.py
Exit 1 if any N appears with conflicting denominators.
"""
import io
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCS = [
    "manuscript/sections/results.tex",
    "manuscript/sections/methods.tex",
    "manuscript/sections/figures.tex",
    "manuscript/si.tex",
    "figures/FIGURES.md",
]

# "108 of 159", "111 of 160 apo cells", "4 of 11 positions"
OF = re.compile(r"(?<![\d.])(\d[\d,]*)\s+of\s+(?:the\s+)?(\d[\d,]*)(?![\d.])")

# strip LaTeX noise that would otherwise split a phrase
TEX = re.compile(r"\\(?:textbf|emph|texttt|textit)\{|\}|\$|\\,|\\;|~|\{|\}")


def num(s):
    return int(s.replace(",", ""))


def context(line, m, width=58):
    lo = max(0, m.start() - width // 2)
    return TEX.sub(" ", line[lo:m.end() + width]).strip()[:96]


def main():
    seen = defaultdict(list)          # numerator -> [(denominator, doc, line, ctx)]
    for rel in DOCS:
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            print("  (skipping %s -- not present)" % rel)
            continue
        for n, line in enumerate(io.open(full, encoding="utf-8"), 1):
            flat = TEX.sub(" ", line)
            for m in OF.finditer(flat):
                a, b = num(m.group(1)), num(m.group(2))
                if b < a or b < 3:
                    continue          # not a count-against-denominator
                if a < 2:
                    # 0 and 1 are degenerate keys: "0 of 9 strata" and "0 of 84
                    # swept points" are unrelated claims that collide on the
                    # numerator alone. Reporting them as a conflict was this
                    # tool's only finding on its first run, and it was noise.
                    continue
                seen[a].append((b, os.path.basename(rel), n, context(flat, m)))

    conflicts = {a: v for a, v in seen.items()
                 if len({d for d, _, _, _ in v}) > 1}

    print("=" * 78)
    print("CROSS-DOCUMENT AUDIT -- does the same claim carry the same denominator")
    print("=" * 78)
    print("\n%d distinct 'N of M' numerators across %d documents"
          % (len(seen), len(DOCS)))

    shared = {a: v for a, v in seen.items()
              if len({doc for _, doc, _, _ in v}) > 1}
    print("%d of them appear in more than one document" % len(shared))
    print("%d carry CONFLICTING denominators" % len(conflicts))

    for a in sorted(conflicts):
        print("\n  %d of ... appears with %s:"
              % (a, " and ".join(str(d) for d in sorted({d for d, _, _, _ in conflicts[a]}))))
        for b, doc, n, ctx in sorted(conflicts[a]):
            print("     %-4d  %-16s:%-4d  %s" % (b, doc, n, ctx))

    print("\n" + "=" * 78)
    if conflicts:
        print("Read each pair before changing anything. A conflict here is a "
              "QUESTION.\nThis paper legitimately carries 111 of 160 and 108 of "
              "159 for the two arms\nof one figure, because exclusions empty a "
              "cognate cell and no apo cell.")
    else:
        print("No numerator carries two different denominators across the "
              "documents.")
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
