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

Every check here is proved by planting the defect it catches, and **every one of those
plants is RUNNABLE**:

    python3 redo/gates/layout.py --selftest        L2, six wrong file kinds
    python3 redo/gates/layout.py --selftest-all    L1 and L3-L7, one plant each

Both stage redo/ into a temporary directory and plant there, never in the real tree.
The staging asserts it reproduces redo/ before any plant runs, and `--selftest-all`
subtracts a BASELINE run: a check already failing on the unplanted tree cannot be
proved by planting it, because it would "fire" for a reason unrelated to the plant.

**Until 2026-09-12 this docstring claimed all seven were proved and only L2 had a
harness at all** -- `--selftest` was silently ignored by `main`, so the sentence read
as a guarantee with nothing behind it, and the L2 tally printed "7/7" beside a
seven-check guard. That is the defect this guard family exists to catch, sitting
inside the guard. Fixed in two steps the same day: the claim was narrowed to what was
true, then the missing plants were written.
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


def _kinds_for(redo):
    """KINDS, rooted anywhere.  The module-level KINDS is this applied to REDO."""
    d = lambda *p: os.path.join(redo, *p)                          # noqa: E731
    out = {}
    for key, val in KINDS.items():
        out[d(os.path.basename(key))] = val
    return out


def _paths_for(root):
    """Every path this guard reads, rooted anywhere.

    Added 2026-09-12 so `--selftest` can plant defects for L1 and L3-L7 into a
    TEMPORARY copy.  Before this, only L2 had a runnable harness while the module
    docstring claimed all seven were proved -- the exact defect this guard family
    exists to catch, sitting inside the guard.
    """
    redo = os.path.join(root, "redo")
    return dict(root=root, redo=redo,
                inputs=os.path.join(redo, "inputs"),
                runs=os.path.join(redo, "runs"),
                kinds=_kinds_for(redo))


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


def _stage(dst):
    """Reproduce redo/ under `dst` as symlinks, plus a root .gitignore.

    Symlinks, not copies, because redo/ carries ~90 MB and a self-test that is slow
    is a self-test nobody runs.  A plant that needs to MODIFY a file must call
    `_materialise` first -- writing through a symlink would edit the real tree, in a
    directory three sessions share.

    The assertion at the end is the part that matters.  Two harnesses in this repo
    staged with a hand-written extension list, silently dropped a file, and scored
    checks as fired for reasons unrelated to their plants.  A staging that does not
    prove it reproduces the original is the defect, not the list.
    """
    redo_dst = os.path.join(dst, "redo")
    for dirpath, dirnames, filenames in os.walk(REDO):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]
        rel = os.path.relpath(dirpath, REDO)
        out = os.path.join(redo_dst, rel) if rel != "." else redo_dst
        os.makedirs(out, exist_ok=True)
        for f in filenames:
            if f.startswith("."):
                continue
            os.symlink(os.path.join(dirpath, f), os.path.join(out, f))
    gi_src = os.path.join(ROOT, ".gitignore")
    if os.path.exists(gi_src):
        with open(os.path.join(dst, ".gitignore"), "w", encoding="utf-8") as fh:
            fh.write(open(gi_src, encoding="utf-8").read())
    # prove the staging reproduces the original, rather than assuming it
    def inventory(base):
        got = set()
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in ("__pycache__", ".git")]
            for f in fn:
                if not f.startswith("."):
                    got.add(os.path.relpath(os.path.join(dp, f), base))
        return got
    a, b = inventory(REDO), inventory(redo_dst)
    if a != b:
        raise AssertionError(f"staging does not reproduce redo/: "
                             f"missing {sorted(a - b)[:4]} extra {sorted(b - a)[:4]}")
    return redo_dst


def _materialise(path):
    """Turn a staged symlink into a real file, so a plant cannot reach the original."""
    real = os.path.realpath(path)
    os.unlink(path)
    with open(path, "wb") as fh:
        fh.write(open(real, "rb").read())


def _run_on(root):
    """Run the guard against a staged root, capturing which checks FAIL."""
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            main(["--root", root])
        except SystemExit:
            pass
    return {ln.split()[1] for ln in buf.getvalue().splitlines()
            if ln.strip().startswith("FAIL")}, buf.getvalue()


def selftest_all():
    """Plant a defect for L1 and L3-L7 and assert each one fires.

    L2 has its own harness (`selftest`), which plants six wrong file kinds.  This
    covers the other six checks, which until 2026-09-12 were asserted as proved by
    the module docstring with nothing runnable behind the claim.
    """
    import shutil
    import tempfile

    def plant_L1(redo):
        open(os.path.join(redo, "notes.txt"), "w").write("x")

    def plant_L3(redo):
        f = os.path.join(redo, "inputs", "ligand_tiers.tsv")
        _materialise(f)
        with open(f, "a", encoding="utf-8") as fh:
            fh.write("HAND_EDITED\n")

    def plant_L4(redo):
        os.unlink(os.path.join(redo, "inputs", "ligand_tiers.tsv"))

    def plant_L5(redo):
        d = os.path.join(redo, "runs", "0001_planted")
        os.makedirs(d)
        open(os.path.join(d, "rows.csv"), "w").write("x")   # manifest.json missing

    def plant_L6(redo):
        d = os.path.join(redo, "runs", "0002_planted")
        os.makedirs(d)
        for f in RUN_FILES:
            open(os.path.join(d, f), "w").write("x")
        json.dump({"input_sha256": ["deadbeef" * 8]},
                  open(os.path.join(d, "manifest.json"), "w"))

    def plant_L7(redo):
        gi = os.path.join(os.path.dirname(redo), ".gitignore")
        open(gi, "w", encoding="utf-8").write("redo/inputs/\n")   # over-broad, and
        #                                                           drops the wanted rule

    cases = [("L1", plant_L1), ("L3", plant_L3), ("L4", plant_L4),
             ("L5", plant_L5), ("L6", plant_L6), ("L7", plant_L7)]
    bad = 0
    baseline = set()
    sys.stdout.write("\n=== layout guard self-test: L1 and L3-L7, planted ===\n\n")
    # The BASELINE matters as much as the plants.  A check already failing on the
    # unplanted tree cannot be proved by planting it -- it would "fire" for a reason
    # that has nothing to do with the plant, which is exactly how a harness comes to
    # report a tidy tally over checks it never exercised.
    tmp = tempfile.mkdtemp(prefix="layout_clean_")
    try:
        baseline, _ = _run_on(_stage(tmp) and tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if baseline:
        sys.stdout.write(f"  NOTE  the tree is not clean right now: {sorted(baseline)} "
                         f"already fail unplanted, so those plants CANNOT be proved "
                         f"until it is.\n")
    else:
        sys.stdout.write("  ok    the staged copy passes unplanted\n")
    for name, plant in cases:
        tmp = tempfile.mkdtemp(prefix=f"layout_{name}_")
        try:
            redo = _stage(tmp)
            plant(redo)
            fired, _out = _run_on(tmp)
            # subtract the baseline: the plant must CAUSE the failure
            ok = name in (fired - baseline)
            extra = sorted(fired - baseline - {name})
            sys.stdout.write(f"  {'ok  ' if ok else 'MISS'}  planted {name:3s} -> "
                             f"{name} fires={ok}"
                             + (f"  (also {extra})" if extra else "") + "\n")
            bad += not ok
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    n = len(cases)
    sys.stdout.write(f"\n  L1,L3-L7: {n - bad}/{n} plants fire "
                     f"(L2 has its own harness: --selftest)\n\n")
    return 1 if bad else 0


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
    # "n/n" here counts PLANTS AGAINST L2, not the guard's seven checks.  Saying
    # "7/7" beside a seven-check guard is how a one-check self-test comes to read as
    # a whole-guard one -- the header-count failure class, in a test harness.
    sys.stdout.write(f"\n  L2: {n - bad}/{n} plants fire -- .gz is admitted and nothing "
                     f"else new "
                     f"is.\n\n")
    return 1 if bad else 0


def main(argv):
    root = ROOT
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    P = _paths_for(root)
    REDO_, INPUTS_, RUNS_, ROOT_ = P["redo"], P["inputs"], P["runs"], P["root"]
    fails, notes = [], []

    def chk(name, ok, detail=""):
        (notes if ok else fails).append((ok, name, detail))

    # -- L1  nothing unexpected at the top -----------------------------------
    have = {e for e in os.listdir(REDO_) if not e.startswith((".", "__"))}
    extra = sorted(have - TOP)
    chk("L1  redo/ holds only its eight declared entries", not extra,
        f"unexpected: {extra}" if extra else f"{len(have)} entries, all declared")

    # -- L2  each file is the kind its directory is for ----------------------
    wrong = check_kinds(P["kinds"], base=REDO_)
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

    mpath = os.path.join(INPUTS_, "MANIFEST.tsv")
    recorded = {}
    if os.path.exists(mpath):
        for ln in open(mpath, encoding="utf-8").read().splitlines()[1:]:
            if ln.strip():
                f, digest = ln.split("\t")[0], ln.split("\t")[1]
                recorded[f] = digest
    on_disk = {f for f in os.listdir(INPUTS_)
               if os.path.isfile(os.path.join(INPUTS_, f))
               and f != "MANIFEST.tsv" and not f.startswith(".")}

    drifted = sorted(f for f in (on_disk & set(recorded))
                     if sha256(os.path.join(INPUTS_, f)) != recorded[f])
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
    run_ids = sorted(e for e in os.listdir(RUNS_)
                     if os.path.isdir(os.path.join(RUNS_, e)) and not e.startswith("."))
    incomplete, unknown_inputs = [], []
    for r in run_ids:
        miss = [f for f in RUN_FILES if not os.path.exists(os.path.join(RUNS_, r, f))]
        if miss:
            incomplete.append(f"{r} missing {miss}")
            continue
        try:
            man = json.load(open(os.path.join(RUNS_, r, "manifest.json"), encoding="utf-8"))
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
    gi = os.path.join(ROOT_, ".gitignore")
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
    if "--selftest-all" in sys.argv:
        sys.exit(selftest_all())
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
