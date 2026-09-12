#!/usr/bin/env python3
"""The layout guard.

A documented folder structure decays; a checked one does not.  This is the
difference between a tidy directory and one that is still tidy in three months,
after several agents have worked in it.

It answers, mechanically, the question nobody can answer by looking at a flat
directory: **may I edit this file, and has anyone already?**

    L1  redo/ holds only the eight things it is allowed to hold
    L2  every file is the kind its directory is for
    L3  every generated input matches its recorded hash   <- hand-edit detector
    L4  the manifest has no row without a file
    L5  every run directory has the same three files
    L6  every run names input hashes we actually hold
    L7  the regenerable bulk is gitignored, and nothing else is

Each check was proved by planting the defect it is meant to catch.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import REDO, ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL

TOP = {"README.md", "paths.py", "spec", "build", "gates", "inputs", "cache",
       "runs", "protocol"}

KINDS = {
    SPEC:     ({".md"}, set()),
    BUILD:    ({".py"}, set()),
    GATES:    ({".py"}, set()),
    # .json is allowed here from 2026-09-12: an analysis that emits a result
    # table plus its provenance metadata is generating BOTH, and provenance is
    # naturally nested. The inputs/cache distinction is about who may write a
    # file, not about its extension -- and inputs/ carries MANIFEST.tsv to
    # prove it, which cache/ does not.
    INPUTS:   ({".tsv", ".csv", ".fasta", ".txt", ".json"}, set()),
    CACHE:    ({".json"}, {"structures"}),
    PROTOCOL: ({".md"}, {"received"}),
}

RUN_FILES = ("manifest.json", "rows.csv", "README.md")


def main(argv):
    fails, notes = [], []

    def chk(name, ok, detail=""):
        (notes if ok else fails).append((ok, name, detail))

    # -- L1  nothing unexpected at the top -----------------------------------
    have = {e for e in os.listdir(REDO) if not e.startswith((".", "__"))}
    extra = sorted(have - TOP)
    chk("L1  redo/ holds only its eight declared entries", not extra,
        f"unexpected: {extra}" if extra else f"{len(have)} entries, all declared")

    # -- L2  each file is the kind its directory is for ----------------------
    wrong = []
    for d, (exts, subdirs) in KINDS.items():
        if not os.path.isdir(d):
            continue
        for e in sorted(os.listdir(d)):
            if e.startswith((".", "__")):
                continue
            p = os.path.join(d, e)
            rel = os.path.relpath(p, REDO)
            if os.path.isdir(p):
                if e not in subdirs:
                    wrong.append(f"{rel} (unexpected directory)")
            elif os.path.splitext(e)[1] not in exts:
                wrong.append(f"{rel} (a {os.path.splitext(e)[1] or 'no-suffix'} file "
                             f"in a {'/'.join(sorted(exts))} directory)")
    chk("L2  every file is the kind its directory is for", not wrong,
        f"{len(wrong)} misplaced: {wrong[:4]}" if wrong else "6 directories clean")

    # -- L3 / L4  the manifest ------------------------------------------------
    import hashlib

    def sha256(path):
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for c in iter(lambda: fh.read(1 << 20), b""):
                h.update(c)
        return h.hexdigest()

    mpath = os.path.join(INPUTS, "MANIFEST.tsv")
    recorded = {}
    if os.path.exists(mpath):
        for ln in open(mpath, encoding="utf-8").read().splitlines()[1:]:
            if ln.strip():
                f, digest = ln.split("\t")[0], ln.split("\t")[1]
                recorded[f] = digest
    on_disk = {f for f in os.listdir(INPUTS)
               if os.path.isfile(os.path.join(INPUTS, f))
               and f != "MANIFEST.tsv" and not f.startswith(".")}

    drifted = sorted(f for f in (on_disk & set(recorded))
                     if sha256(os.path.join(INPUTS, f)) != recorded[f])
    unrecorded = sorted(on_disk - set(recorded))
    chk("L3  every generated input matches its recorded hash",
        not drifted and not unrecorded,
        (f"hand-edited or regenerated without restamping: {drifted}" if drifted else "")
        + (f" not in the manifest: {unrecorded}" if unrecorded else "")
        or f"{len(on_disk)} files, all match")

    orphan = sorted(set(recorded) - on_disk)
    chk("L4  the manifest has no row without a file", not orphan,
        f"recorded but absent: {orphan}" if orphan else f"{len(recorded)} rows all resolve")

    # -- L5 / L6  the runs ----------------------------------------------------
    run_ids = sorted(e for e in os.listdir(RUNS)
                     if os.path.isdir(os.path.join(RUNS, e)) and not e.startswith("."))
    incomplete, unknown_inputs = [], []
    for r in run_ids:
        miss = [f for f in RUN_FILES if not os.path.exists(os.path.join(RUNS, r, f))]
        if miss:
            incomplete.append(f"{r} missing {miss}")
            continue
        try:
            man = json.load(open(os.path.join(RUNS, r, "manifest.json"), encoding="utf-8"))
        except Exception as exc:                                  # noqa: BLE001
            incomplete.append(f"{r} manifest.json unreadable: {exc}")
            continue
        for h in man.get("input_sha256", []):
            if h not in set(recorded.values()):
                unknown_inputs.append(f"{r} -> {h[:12]}")
    chk("L5  every run directory has the same three files", not incomplete,
        "; ".join(incomplete) if incomplete
        else (f"{len(run_ids)} runs" if run_ids else "no runs yet"))
    chk("L6  every run names input hashes we hold", not unknown_inputs,
        "; ".join(unknown_inputs) if unknown_inputs
        else (f"{len(run_ids)} runs" if run_ids else "no runs yet"))

    # -- L7  gitignore --------------------------------------------------------
    gi = os.path.join(ROOT, ".gitignore")
    rules = []
    if os.path.exists(gi):
        rules = [ln.strip() for ln in open(gi, encoding="utf-8")
                 if ln.strip() and not ln.lstrip().startswith("#")]
    want = "redo/cache/structures/"
    over = sorted(r for r in rules
                  if r.startswith("redo/") and r != want)
    chk("L7  the regenerable bulk is gitignored, and nothing else is",
        want in rules and not over,
        (f"{want} is NOT gitignored -- 297 mmCIF files will be committed; "
         if want not in rules else "")
        + (f"over-broad redo rules: {over}" if over else "")
        or f"only {want}")

    # -- report ---------------------------------------------------------------
    sys.stdout.write("\n=== redo layout guard ===\n\n")
    for ok, name, detail in sorted(notes + fails, key=lambda t: t[1]):
        sys.stdout.write(f"  {'PASS' if ok else 'FAIL'}  {name}  {detail}\n".rstrip() + "\n")
    if fails:
        sys.stdout.write(f"\n  LAYOUT VIOLATED -- {len(fails)} check(s) failed.\n\n")
        return 1
    sys.stdout.write(f"\n  CLEAN -- {len(notes)} checks pass.\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
