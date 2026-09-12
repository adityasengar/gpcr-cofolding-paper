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
    #
    # .gz is allowed here from 2026-09-12, for the same reason and one more.
    # drule_rejections.tsv is 1.7 M rows / 86 MB as text and 7.2 MB gzipped, and
    # inputs/ is committed by design -- so the choice was "commit 86 MB
    # permanently" or "compress". A .gz is still a generated input, still
    # code-written, still hashed in MANIFEST.tsv; the extension says how the bytes
    # are packed, not who may write them, and L3 is what actually enforces the
    # latter. It must stay a NARROW admission: .gz only, and only because
    # drule_select.py writes it with mtime=0 and no embedded filename, so the same
    # rows give the same sha256 and the manifest digest still means something.
    # Compression that is not byte-stable would make L3 fire on every run.
    INPUTS:   ({".tsv", ".csv", ".fasta", ".txt", ".json", ".gz"}, set()),
    CACHE:    ({".json"}, {"structures"}),
    PROTOCOL: ({".md"}, {"received"}),
}

RUN_FILES = ("manifest.json", "rows.csv", "README.md")


def check_kinds(kinds, base=None):
    """L2's body, over any {directory: (allowed extensions, allowed subdirs)}.

    Extracted so `--selftest` can plant a misplaced file in a TEMPORARY directory
    rather than in redo/inputs/ itself.  Planting into the real tree to prove a guard
    is how you end up with a half-planted defect left behind when something raises,
    in a directory three sessions share.
    """
    wrong = []
    for d, (exts, subdirs) in kinds.items():
        if not os.path.isdir(d):
            continue
        for e in sorted(os.listdir(d)):
            if e.startswith((".", "__")):
                continue
            p = os.path.join(d, e)
            rel = os.path.relpath(p, base or REDO)
            if os.path.isdir(p):
                if e not in subdirs:
                    wrong.append(f"{rel} (unexpected directory)")
            elif os.path.splitext(e)[1] not in exts:
                wrong.append(f"{rel} (a {os.path.splitext(e)[1] or 'no-suffix'} file "
                             f"in a {'/'.join(sorted(exts))} directory)")
    return wrong


def selftest():
    """Prove L2 by planting, after the .gz admission of 2026-09-12.

    Widening an allow-list is exactly the moment to re-prove the guard: the change
    that lets one new kind through is the change that could let everything through,
    and a guard that has stopped refusing looks identical to one that has nothing to
    refuse.
    """
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    allowed, disallowed = [], []
    try:
        kinds = {tmp: (KINDS[INPUTS][0], set())}
        # baseline: the kinds inputs/ is for, including the new .gz
        for name in ("a.tsv", "b.csv", "c.json", "d.tsv.gz"):
            open(os.path.join(tmp, name), "w").close()
        base_wrong = check_kinds(kinds, tmp)
        allowed.append(("the admitted kinds pass, .gz included", not base_wrong,
                        base_wrong))
        # the plant: kinds that are still NOT inputs, one at a time
        for name in ("secret.sh", "notes.md", "scratch", "archive.zip",
                     "table.tsv.bz2"):
            p = os.path.join(tmp, name)
            open(p, "w").close()
            w = check_kinds(kinds, tmp)
            disallowed.append((name, bool(w)))
            os.remove(p)
        # and a directory, which inputs/ allows none of
        os.mkdir(os.path.join(tmp, "subdir"))
        dir_caught = bool(check_kinds(kinds, tmp))
        os.rmdir(os.path.join(tmp, "subdir"))
    finally:
        shutil.rmtree(tmp)

    bad = 0
    sys.stdout.write("\n=== layout guard self-test: L2, re-proved after the .gz "
                     "admission ===\n\n")
    for what, ok, detail in allowed:
        bad += 0 if ok else 1
        sys.stdout.write(f"  {'ok  ' if ok else 'MISS'} {what}"
                         f"{'' if ok else '  -- ' + str(detail)}\n")
    for name, fired in disallowed:
        bad += 0 if fired else 1
        verdict = ("L2 fires" if fired else
                   "L2 DID NOT FIRE -- the admission is too wide")
        sys.stdout.write(f"  {'ok  ' if fired else 'MISS'} planted {name:<14} -> "
                         f"{verdict}\n")
    bad += 0 if dir_caught else 1
    sys.stdout.write(f"  {'ok  ' if dir_caught else 'MISS'} planted a subdirectory  "
                     f"-> {'L2 fires' if dir_caught else 'L2 DID NOT FIRE'}\n")
    n = len(allowed) + len(disallowed) + 1
    sys.stdout.write(f"\n  {n - bad}/{n} -- .gz is admitted and nothing else new "
                     f"is.\n\n")
    return 1 if bad else 0


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
    wrong = check_kinds(KINDS)
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
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
