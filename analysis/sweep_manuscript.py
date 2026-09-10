#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every number in the manuscript must have a declared source.

Block A shipped 23 discrepancy groups and Block B eight; in three separate
cases a number we quoted came from a claim sheet that its own data did not
reproduce. Reading the sections again would not have caught any of them. This
does something narrower and mechanical instead:

  1. extract every numeric token from the Results and Methods sections;
  2. look each up in analysis/NUMBER_REGISTRY.md;
  3. fail on any number that has no entry.

A number cannot enter the manuscript silently. Adding one means adding a
registry line saying where it came from, which is the step that gets skipped
when a sentence is written from a claim sheet at 2am.

The registry does NOT re-verify values -- verify_claims.py does that. This
answers a different question: "is there anything in the paper nobody has
accounted for?"

Usage:  python3 analysis/sweep_manuscript.py [--list-untraced]
"""
from __future__ import print_function
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ["manuscript/sections/results.tex", "manuscript/sections/methods.tex"]
REGISTRY = os.path.join(ROOT, "analysis", "NUMBER_REGISTRY.md")

# tokens that are never claims: LaTeX lengths, citation years, section numbers,
# and the small integers that appear as ordinary English ("one of four").
IGNORE_CONTEXT = re.compile(
    r'\\(?:cite[a-z]*|ref|label|includegraphics|textwidth|linewidth|hspace|vspace|'
    r'begin|end|section|subsection|input|citep|citet)\b')
PURE_YEAR = re.compile(r'^(19|20)\d\d$')


CITE = re.compile(r'\\cite[a-zA-Z]*\s*(\[[^\]]*\])?\s*(\[[^\]]*\])?\s*\{[^{}]*\}')
SHAISH = re.compile(r'\\texttt\{[^{}]*\}')


def strip_comments(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    # LaTeX thin-space thousands separators: 1{,}699 is one number, not two
    s = s.replace('{,}', ',')
    # citation page locators are audited by lit/validate/pageoffset.py, not here
    s = CITE.sub(' ', s)
    # \texttt{} holds SHAs, column names and file names, never claims
    s = SHAISH.sub(' ', s)
    return s


def tokens(path):
    """Yield (line_no, number, context) for every numeric token that could be a claim."""
    out = []
    for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
        line = strip_comments(line)
        if IGNORE_CONTEXT.search(line):
            # keep the line but drop the macro arguments, which carry years/keys
            line = IGNORE_CONTEXT.sub(" ", line)
            line = re.sub(r'\{[^{}]*\}', " ", line)
        for m in re.finditer(r'(?<![\w.\\])\d+(?:[.,]\d+)*', line):
            n = m.group(0)
            if PURE_YEAR.match(n):
                continue
            out.append((i, n, line.strip()))
    return out


UNTRACED_HEADING = "## NOT covered by any automated check"


def registry_numbers():
    """Return (covered, uncovered, n_entries).

    The registry has two halves and they mean opposite things. A number in the
    second half is REGISTERED but not CHECKED, and the sweep must keep saying so
    -- otherwise writing a number down would be enough to make it look verified,
    which is the failure this whole file exists to prevent.
    """
    if not os.path.exists(REGISTRY):
        return set(), set(), 0
    text = io.open(REGISTRY, encoding="utf-8").read()
    head, _, tail = text.partition(UNTRACED_HEADING)

    def nums_in(chunk):
        out = set()
        for l in chunk.splitlines():
            l = l.strip()
            if not l.startswith("|") or l.startswith("|---"):
                continue
            first = l.strip("|").split("|")[0].strip()
            for m in re.finditer(r'(?<![\w.])\d+(?:[.,]\d+)*', first):
                out.add(m.group(0))
        return out

    cov, unc = nums_in(head), nums_in(tail)
    return cov, unc - cov, len(cov) + len(unc)


def main():
    known, registered_uncovered, n_entries = registry_numbers()
    untraced, uncovered, total = [], [], 0
    for rel in SECTIONS:
        for line_no, n, ctx in tokens(os.path.join(ROOT, rel)):
            total += 1
            variants = {n, n.replace(",", ""), n.replace(",", "{,}")}
            if variants & known:
                continue
            if variants & registered_uncovered:
                uncovered.append((rel, line_no, n, ctx))
                continue
            untraced.append((rel, line_no, n, ctx))

    print("=" * 78)
    print("MANUSCRIPT NUMBER SWEEP -- %d numeric tokens, %d registry entries"
          % (total, n_entries))
    print("=" * 78)
    print("  covered by an automated check : %d" % (total - len(uncovered) - len(untraced)))
    print("  registered but NOT checked    : %d" % len(uncovered))
    print("  no registry entry at all      : %d" % len(untraced))
    if not untraced:
        print("\nEvery number has an entry. %d of them are still unchecked --"
              "\nsee the second half of analysis/NUMBER_REGISTRY.md." % len(uncovered))
        return 0
    print("\n%d numbers have NO registry entry:\n" % len(untraced))
    seen = set()
    for rel, line_no, n, ctx in untraced:
        key = (n, ctx[:60])
        if key in seen:
            continue
        seen.add(key)
        print("  %-34s:%-5d %-12s %s" % (os.path.basename(rel), line_no, n,
                                         ctx[:88]))
    print("\nAdd a line to analysis/NUMBER_REGISTRY.md for each, naming the file"
          "\nand filter it came from -- or remove it from the manuscript.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
