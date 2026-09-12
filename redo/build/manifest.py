#!/usr/bin/env python3
"""Write inputs/MANIFEST.tsv -- the hash record for every generated input.

Why this exists: inputs/ holds files that only code may write, and there is no
way to tell by looking at a .tsv whether someone opened it and fixed a value by
hand.  The manifest makes that detectable: gates/layout.py rehashes every file
and fails on any that has drifted from its recorded digest.

The `generator` column is derived by STATIC REFERENCE -- the build script whose
source mentions the filename -- not by observing a run.  Where that is ambiguous
the column says so rather than guessing, because a generator attribution is a
claim about which code is responsible for a number.

    python3 redo/build/manifest.py           # rewrite the manifest
    python3 redo/build/manifest.py --check    # exit 1 if it is stale
"""

import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, BUILD, GATES

MANIFEST = os.path.join(INPUTS, "MANIFEST.tsv")
HEADER = ["file", "sha256", "bytes", "generator"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def generators():
    """filename -> the build/gates scripts that WRITE it.

    A mention is not authorship: most of these scripts read half a dozen of
    these files and write one.  So we look only for writes, in the two forms
    the codebase actually uses --

        OUT = os.path.join(INPUTS, "x.csv")   ...   open(OUT, "w")
        open(os.path.join(INPUTS, "x.csv"), "w")

    Anything else stays unattributed.  A wrong generator is worse than a blank
    one: it says which code is answerable for a number, and that is a claim.
    """
    hits = {}
    for d in (BUILD, GATES):
        for s in sorted(os.listdir(d)):
            if not s.endswith(".py"):
                continue
            src = open(os.path.join(d, s), encoding="utf-8", errors="replace").read()
            # direct: open(os.path.join(INPUTS, "x"), "w")
            for name in re.findall(
                    r"open\(\s*os\.path\.join\(\s*\w+\s*,\s*['\"]([^'\"]+)['\"]\s*\)\s*,\s*['\"][wa]",
                    src):
                hits.setdefault(name, set()).add(s)
            # indirect: VAR = os.path.join(..., "x")  then  open(VAR, "w")
            for var, name in re.findall(
                    r"^\s*([A-Z_][A-Z0-9_]*)\s*=\s*os\.path\.join\(\s*\w+\s*,\s*['\"]([^'\"]+)['\"]\s*\)",
                    src, re.M):
                if re.search(rf"open\(\s*{var}\s*,\s*['\"][wa]", src):
                    hits.setdefault(name, set()).add(s)
    return hits


def rows():
    hits = generators()
    out = []
    for f in sorted(os.listdir(INPUTS)):
        p = os.path.join(INPUTS, f)
        if f == "MANIFEST.tsv" or not os.path.isfile(p) or f.startswith("."):
            continue
        who = sorted(hits.get(f, ()))
        gen = who[0] if len(who) == 1 else (",".join(who) if who else "unattributed")
        out.append([f, sha256(p), str(os.path.getsize(p)), gen])
    return out


def render(rs):
    return "\n".join(["\t".join(HEADER)] + ["\t".join(r) for r in rs]) + "\n"


def main(argv):
    text = render(rows())
    if "--check" in argv:
        have = open(MANIFEST, encoding="utf-8").read() if os.path.exists(MANIFEST) else ""
        if have != text:
            sys.stderr.write("MANIFEST.tsv is stale -- run: python3 redo/build/manifest.py\n")
            return 1
        return 0
    open(MANIFEST, "w", encoding="utf-8").write(text)
    n = text.count("\n") - 1
    amb = sum(1 for ln in text.splitlines()[1:] if "," in ln.split("\t")[-1])
    una = text.count("unattributed")
    sys.stdout.write(f"MANIFEST.tsv: {n} files  ({n - amb - una} attributed, "
                     f"{amb} ambiguous, {una} unattributed)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
