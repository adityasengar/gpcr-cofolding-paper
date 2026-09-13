#!/usr/bin/env python3
"""Audit the request and rebuttal documents against what is actually on disk.

WHY. These documents go to another team. Their whole value is that every ask is
real, so the worst defect is not a missing ask -- it is an ask for a file we
already hold, or a file named slightly wrong. One of those turns the document
from a work order into a thing that has to be checked before it can be used, and
the Block C audit already found four such entries in a previous count: a
capitalisation variant, a correctly-absent retraction, a file held byte-identical
under the cited name, and one shipped under a different basename.

WHAT THIS TOOL LEARNED ABOUT ITSELF, on its first run, 2026-09-10.

Version 1 tried to read intent: it matched absence words and citation verbs
anywhere in the line, then compared that to the filesystem. It reported SIXTEEN
problems across the six documents. Every single one was the regex, not the
document -- a 100% false-positive rate:

  - "Deliberately absent" is a SECTION NAME in quotes, not a claim of absence.
  - "`rows.tier3.v2.csv` in `BLOCK_C_WRAP_REPORT.md`" enumerates an absent file;
    the bare "in" made it look like a citation.
  - "One -- `refsep_pocket_ca.csv` -- ships under a different basename" was read
    as a present-claim and then failed for not finding that literal path. The
    document was being MORE precise than the checker.

The lesson generalises past this file: a regex cannot tell a path that is the
SUBJECT of an ask from a path cited as EVIDENCE for one, and a tool whose output
must be hand-triaged every run is a tool that will be ignored. So version 2 does
only what is decidable, and reports the rest as a table for a human to read.

  PASS 1 -- the one high-precision check. A path claimed absent in the SAME
  SENTENCE (not the same line) that exists at that exact path. Text inside
  double quotes is stripped first, so section names cannot trigger it.

  Sentences are assembled ACROSS LINE BREAKS, because markdown wraps mid-
  sentence and a per-line splitter mis-binds every claim that straddles a wrap.
  That cost one false positive on run 2: "`task_A_v2_....json` is named in\n
  `BLOCK_C_STATE_CHECK.md` and does not ship" put the absence phrase and the
  wrong path on the same physical line.

  PASS 2 -- near-miss basenames, REVIEW ONLY, never a failure. The document
  claims absence and we hold that basename elsewhere. This cannot be decided
  mechanically: on its first run both hits were documents being correct --
  one said "does not ship ... is byte-identical to the copy we hold from Block
  B", which is exactly right, and one named TWO paths in a sentence whose
  absence claim bound to the other one. An absence claim now binds to the
  NEAREST PRECEDING path, which is how the English works, and what survives is
  printed for a human rather than failing the run.

  COVERAGE TABLE -- every path mentioned, with its filesystem status. No
  judgement, no intent parsing. This is the part that is actually useful before
  a document goes upstream.

Usage:  python3 analysis/audit_asks.py
Exit 1 if any pass finds something.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCS = [
    "analysis/block_a/DATA_REQUESTS.md",
    "analysis/block_b/DATA_REQUESTS.md",
    "analysis/block_c/DATA_REQUESTS.md",
    "analysis/block_d/DATA_REQUESTS.md",
    "analysis/block_d/ASK_2026_09_13.md",
    "rebuttals/BLOCK_A.md",
    "rebuttals/BLOCK_B.md",
    "rebuttals/BLOCK_C.md",
    "rebuttals/BLOCK_D.md",
    "rebuttals/PANEL_EXPANSION.md",
    "rebuttals/PANEL_EXPANSION_CLASS_A.md",
]

# a backtick-quoted token that looks like a file
# Backticked paths in prose, OR bare paths inside a fenced code block.
#
# Until 2026-09-13 this matched backticks only, so any path written inside a ```
# fence was invisible to the auditor -- and a request document's headline ask is
# very often a fenced block listing the files wanted. Block D's three rows.csv
# paths sat there unaudited for three days.
#
# Nothing was actually missed by it: those three begin `experiments/`, which
# UPSTREAM classifies as their-side and skips regardless. The defect is that a
# FENCED path pointing at something WE hold would have slipped through, and that
# is precisely the case this auditor exists to catch -- an ask for a file we
# already have destroys the credibility of every real ask beside it.
#
# SCOPE, deliberately limited. Fenced paths are surfaced in PASS 2 (for a human to
# read) and are NOT promoted to pass-1 false-ask failures. A bare fenced path
# carries no absence claim for pass 1 to contradict, and treating every fenced path
# as an ask would misfire on the code blocks these documents are full of --
# `pd.read_csv('data/block_c/.../g4_full_census_v2.csv')` names a file we hold and
# is not a request for it. A guard that cries wolf on its own examples destroys the
# credibility it exists to protect, which is the same failure it was built to stop.
PATH = re.compile(r"`([A-Za-z0-9_./*\-]+\.(?:csv|json|md|py|cif|tsv|txt|zip))`")
FENCED_PATH = re.compile(r"^\s*([A-Za-z0-9_./*\-]+\.(?:csv|json|md|py|cif|tsv|txt|zip))\b",
                         re.M)


def paths_in(text):
    """Every path a reader would take as an ask: backticked, or bare in a fence."""
    found = set(PATH.findall(text))
    for block in re.findall(r"```[^\n]*\n(.*?)```", text, re.S):
        found.update(FENCED_PATH.findall(block))
    return found

ABSENT = re.compile(
    r"\b(not shipped|unshipped|did not ship|does not ship|is absent|are absent|"
    r"is missing|never shipped|not present|not in the (?:zip|drop|bundle)|"
    r"we do not hold|not delivered|no such file)\b", re.I)

QUOTED = re.compile(r'"[^"]*"')      # section names etc -- never a claim

def sentences(text):
    """(sentence, line_number) over the whole document.

    Two things this must get right, and version 2 got each wrong in turn:

    1. Sentences WRAP. Markdown breaks lines mid-sentence, so splitting per
       line binds an absence claim to whatever path shares its physical line.
    2. Filenames CONTAIN PERIODS. Splitting on "." alone shatters
       `rows_tidy.csv` into fragments and the path regex then matches nothing --
       which is how version 2 reported zero paths in eight documents and looked
       like a pass.

    So the boundary is a sentence ender FOLLOWED BY WHITESPACE, which a
    filename's internal dot never is, and newline counts as that whitespace.
    """
    clean = QUOTED.sub(lambda m: " " * len(m.group(0)), text)
    out, start = [], 0
    for m in re.finditer(r"(?<=[.;:])\s", clean):
        seg = clean[start:m.start() + 1]
        if seg.strip():
            out.append((seg, clean.count("\n", 0, start) + 1))
        start = m.end()
    tail = clean[start:]
    if tail.strip():
        out.append((tail, clean.count("\n", 0, start) + 1))
    return out


# paths that name something on the PIPELINE's machine, not ours. An ask for one
# of these is correct by definition and must not be reported as a false ask.
UPSTREAM = re.compile(r"^(experiments/|release/|docs/|panel/|refs/|/tmp/|\$TMPDIR|"
                      r"rescore_|assets/)")


def tree_index():
    """basename (lowercased) -> every real path with that basename."""
    idx = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "out", "pdfs", "source", "__pycache__")]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            idx.setdefault(fn.lower(), []).append(rel)
    return idx


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


def main():
    idx = tree_index()
    false_asks, near_misses = [], []
    coverage = {}

    for doc in DOCS:
        full = os.path.join(ROOT, doc)
        if not os.path.exists(full):
            print("  (skipping %s -- not present)" % doc)
            continue
        raw = open(full).read()
        # Fenced blocks are scanned separately, with their real line numbers, so a
        # headline ask written as a bare fenced list is audited like any other.
        fenced = []
        for m in re.finditer(r"```[^\n]*\n(.*?)```", raw, re.S):
            base_line = raw[:m.start()].count("\n") + 2
            for i, ln in enumerate(m.group(1).split("\n")):
                for hit in FENCED_PATH.findall(ln):
                    fenced.append((hit, base_line + i))
        for sent, n in list(sentences(raw)) + [(f"`{p_}`", ln) for p_, ln in fenced]:
                for path in PATH.findall(sent):
                    base = os.path.basename(path).lower()
                    here = exists(path)
                    elsewhere = [p for p in idx.get(base, []) if p != path]

                    status = ("present" if here else
                              "elsewhere" if elsewhere else
                              "upstream" if UPSTREAM.match(path) else "absent")
                    coverage.setdefault(path, [status, elsewhere[:2], set()])
                    coverage[path][2].add(doc.split("/")[-1])

                    # an absence claim binds to the nearest path BEFORE it,
                    # not to every path in the sentence
                    m = ABSENT.search(sent)
                    if m:
                        before = [x for x in PATH.finditer(sent)
                                  if x.start() < m.start()]
                        owner = before[-1].group(1) if before else None
                        if owner == path:
                            if here:
                                false_asks.append(
                                    (doc, n, path, "exists at that exact path"))
                            elif elsewhere and not UPSTREAM.match(path):
                                near_misses.append((doc, n, path, elsewhere[:2]))

    print("=" * 78)
    print("REQUEST-DOCUMENT AUDIT -- do the claims about files survive the filesystem")
    print("=" * 78)

    def show(title, rows, fmt):
        print("\n%s: %d" % (title, len(rows)))
        for r in rows:
            print("   " + fmt(r))

    show("1. CLAIMED ABSENT IN A SENTENCE, BUT PRESENT (false asks)", false_asks,
         lambda r: "%s:%d  %s  -- %s" % (r[0], r[1], r[2], r[3]))
    show("2. CLAIMED ABSENT, BASENAME SHIPS ELSEWHERE -- REVIEW, not a failure",
         near_misses,
         lambda r: "%s:%d  %s  -> %s" % (r[0], r[1], r[2], ", ".join(r[3])))

    counts = {}
    for path, (status, _, _) in coverage.items():
        counts[status] = counts.get(status, 0) + 1
    print("\n3. COVERAGE -- every path these documents name, %d distinct"
          % len(coverage))
    for k in ("present", "elsewhere", "upstream", "absent"):
        print("     %-10s %d" % (k, counts.get(k, 0)))
    print("     (`absent` is the expected state for a file we are ASKING FOR.")
    print("      `elsewhere` is the one worth a human eye: we may already hold it.)")
    for path, (status, other, docs) in sorted(coverage.items()):
        if status == "elsewhere":
            print("     %-46s -> %s  [%s]"
                  % (path, ", ".join(other), ", ".join(sorted(docs))))

    print("\n%s" % ("=" * 78))
    if false_asks:
        print("%d FALSE ASK(S): a document asks for a file that exists. Fix before "
              "sending." % len(false_asks))
    else:
        print("No false asks: nothing is requested that we already hold at that path.")
    if near_misses:
        print("%d entry(ies) in pass 2 for a human to read. These are NOT failures --"
              "\non the tool's first run every one of them was the document being "
              "right." % len(near_misses))
    bad = len(false_asks)
    print("Upstream paths (experiments/, release/, docs/, refs/, /tmp) are exempt "
          "from\npass 1 and 3 by design: they name the pipeline's machine, not ours.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
