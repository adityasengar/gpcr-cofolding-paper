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
    """filename -> the build/gates scripts that WRITE it, by AST rather than regex.

    A mention is not authorship: most of these scripts read half a dozen of these
    files and write one.  Regex could see only two of the write forms this codebase
    uses and missed three more -- a lowercase local (`out = ...; open(out, "w")`),
    a constant reaching open() through a tuple loop (`for path, rows in ((A, x),
    (B, y)): open(path, "w")`), and `with open(...)`.  Walking the tree finds all of
    them and cannot be fooled by a filename appearing in a docstring.

    Still conservative on purpose: a name must be BOUND to an os.path.join(...,
    "literal") and then reach an open(..., "w"/"a"), directly or as a loop target
    whose iterable mentions it.  Anything else stays unattributed, because a wrong
    generator is worse than a blank one -- it says which code is answerable for a
    number, and that is a claim.
    """
    import ast

    def joined_literal(node):
        """os.path.join(ANY, "x.tsv") -> "x.tsv", else None."""
        if not isinstance(node, ast.Call):
            return None
        f = node.func
        if not (isinstance(f, ast.Attribute) and f.attr == "join"):
            return None
        last = node.args[-1] if node.args else None
        if isinstance(last, ast.Constant) and isinstance(last.value, str):
            return last.value
        return None

    hits = {}
    for d in (BUILD, GATES):
        for s in sorted(os.listdir(d)):
            if not s.endswith(".py"):
                continue
            try:
                tree = ast.parse(open(os.path.join(d, s), encoding="utf-8",
                                      errors="replace").read())
            except SyntaxError:
                continue

            # TEST SCAFFOLDING IS NOT AUTHORSHIP.  A gate's plant harness writes
            # into a STAGED copy of inputs/, which is statically indistinguishable
            # from writing the real file -- layout.py was briefly recorded as the
            # generator of ligand_tiers.tsv because its L3 plant appends to it.
            # Writes inside a selftest/plant/stage function are excluded.
            skip = set()
            for fn in ast.walk(tree):
                if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                        k in fn.name.lower() for k in ("selftest", "plant", "stage",
                                                       "materialise", "materialize")):
                    for sub in ast.walk(fn):
                        skip.add(id(sub))

            # 1. every `NAME = os.path.join(..., "f")`, WITH ITS LINE.
            # The line matters: g0_calibration_set.py rebinds `out` once per
            # output file, so a name->literal dict keeps only the last and loses
            # eight attributions. Each write is matched to the nearest binding
            # ABOVE it instead, which is what the rebinding idiom actually means.
            binds = []                       # (lineno, name, literal)
            for n in ast.walk(tree):
                if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                        and isinstance(n.targets[0], ast.Name):
                    lit = joined_literal(n.value)
                    if lit:
                        binds.append((n.lineno, n.targets[0].id, lit))

            def nearest(name, before):
                """The literal `name` held at line `before`, or None."""
                cands = [(ln, li) for ln, nm, li in binds if nm == name and ln < before]
                return max(cands)[1] if cands else None

            # 2. every name opened for writing, and every literal opened directly
            written_names, written_literals = [], set()   # (lineno, name)
            for n in ast.walk(tree):
                if id(n) in skip:
                    continue
                if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                        and n.func.id == "open"):
                    continue
                mode = n.args[1] if len(n.args) > 1 else None
                mode = mode.value if isinstance(mode, ast.Constant) else ""
                if not (isinstance(mode, str) and mode[:1] in ("w", "a")):
                    continue
                tgt = n.args[0] if n.args else None
                if isinstance(tgt, ast.Name):
                    written_names.append((n.lineno, tgt.id))
                lit = joined_literal(tgt)
                if lit:
                    written_literals.add(lit)

            for lit in written_literals:
                hits.setdefault(lit, set()).add(s)
            wnames = {nm for _ln, nm in written_names}
            for ln, nm in written_names:
                lit = nearest(nm, ln)
                if lit:
                    hits.setdefault(lit, set()).add(s)

            # 3. a bound name reaching open() as a LOOP TARGET:
            #        for path, rows in ((OUT_A, a), (OUT_B, b)): open(path, "w")
            for n in ast.walk(tree):
                if not isinstance(n, ast.For):
                    continue
                targets = ({n.target.id} if isinstance(n.target, ast.Name)
                           else {e.id for e in getattr(n.target, "elts", [])
                                 if isinstance(e, ast.Name)})
                if not (targets & wnames):
                    continue
                for sub in ast.walk(n.iter):
                    if isinstance(sub, ast.Name):
                        lit = nearest(sub.id, n.lineno)
                        if lit:
                            hits.setdefault(lit, set()).add(s)
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
