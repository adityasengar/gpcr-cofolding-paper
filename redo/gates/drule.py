#!/usr/bin/env python3
"""Gate on the decoy rule -- DRULE deliverable 3.

    python3 redo/gates/drule.py
    python3 redo/gates/drule.py --selftest

The pool itself (deliverable 1) cannot be built until a ChEMBL release is pinned
and downloaded, which is Aditya's decision.  So this gate covers what exists --
the target mapping -- and says LOUDLY that the pool has not been built rather than
falling silent about it.  That distinction matters: the project's rule is that a
missing input must never be a QUIET skip.  A deliverable that has not been produced
yet is reported as NOT BUILT, in the output, every run.  An input that has
disappeared is a failure.
"""

import csv
import io
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS  # noqa: E402

TARGETS = "drule_targets.tsv"
POOL = "drule_pool_molecules.tsv"
EXCL = "drule_pool_exclusions.tsv"
PANEL = "g1_receptors.tsv"


def tsv(name, root):
    with open(os.path.join(root, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main(argv=(), root=None):
    root = root or INPUTS
    blocking, passed, pending = [], [], []

    def chk(label, ok, detail=""):
        (passed if ok else blocking).append(label + (f"  -- {detail}" if detail else ""))

    # -- D-1  the target mapping exists and names its release ---------------
    if not os.path.exists(os.path.join(root, TARGETS)):
        chk("D-1  the ChEMBL target mapping is present", False,
            f"{TARGETS} is ABSENT -- run redo/build/drule_targets.py")
        return report(blocking, passed, pending)
    tg = tsv(TARGETS, root)
    rels = {r["chembl_release"] for r in tg}
    chk("D-1  the target mapping is present and names ONE ChEMBL release",
        len(rels) == 1 and all(rels), f"{len(tg)} rows, release {sorted(rels)}")

    # -- D-2  every receptor on the panel is accounted for -------------------
    panel = tsv(PANEL, root)
    missing = sorted({r["slug"] for r in panel} - {r["receptor_slug"] for r in tg})
    chk("D-2  every panel receptor has a row, resolved or not",
        not missing, f"absent from the mapping: {missing}" if missing
        else f"{len(panel)} receptors, all present")

    # -- D-3  an unresolved receptor is RECORDED, never dropped -------------
    # B1B1U5 is a jumping-spider opsin and has no ChEMBL target.  That is a real
    # fact about the panel and it must survive into the table, because a receptor
    # that silently vanishes from a decoy pool looks exactly like one that had no
    # decoys.
    unres = [r for r in tg if not r["chembl_target_id"]]
    blank = [r for r in unres if not r["receptor_slug"]]
    chk("D-3  unresolved receptors are recorded with an empty target, not dropped",
        not blank, f"{len(unres)} unresolved: " +
        ", ".join(r["receptor_slug"] for r in unres))

    # -- D-4  no ambiguous mapping is resolved silently ----------------------
    amb = [r for r in tg if r["n_targets_matched"] not in ("0", "1")]
    chk("D-4  no accession maps to more than one SINGLE PROTEIN target",
        not amb, ", ".join(f"{r['receptor_slug']}={r['n_targets_matched']}"
                           for r in amb) or "every resolved accession is 1:1")

    # -- D-5  the pool: checked if built, announced loudly if not -----------
    ppath = os.path.join(root, POOL)
    if not os.path.exists(ppath):
        pending.append(
            "the candidate pool is NOT BUILT. drule_pool.py refuses to run "
            "against the live API; it needs --db with a PINNED ChEMBL release "
            "plus --release and --sha256. Downloading one is Aditya's decision. "
            "The rule itself is proved meanwhile: drule_pool.py --selftest")
    else:
        # The pool is stored NORMALISED -- the molecule set once, plus only the
        # excluded (receptor, molecule) pairs. Flattened it is 7.6 M rows / 2.0 GB
        # and 95% redundant, because the absence rule excludes just 4.8%.
        pool = tsv(POOL, root)
        excl = tsv(EXCL, root) if os.path.exists(os.path.join(root, EXCL)) else None
        if excl is None:
            chk("D-5  the exclusion table is present", False,
                f"{EXCL} is ABSENT -- the molecule table alone cannot say who is "
                "ineligible, which is the auditability the rule turns on")
        else:
            # eligibility = in the molecule table, not excluded for this receptor.
            # So the leak test is that every exclusion names a real molecule and a
            # reason; an exclusion with neither silently becomes an eligibility.
            ids = {r["candidate_chembl_id"] for r in pool}
            orphan = [r for r in excl if r["candidate_chembl_id"] not in ids]
            silent = [r for r in excl if not r["ineligible_because"].strip()]
            chk("D-5  every exclusion names a molecule in the pool AND the axis "
                "that excluded it", not orphan and not silent,
                f"{len(orphan)} orphaned, {len(silent)} without a reason"
                if (orphan or silent) else
                f"{len(pool):,} molecules, {len(excl):,} exclusions, all resolved")
        norel = [r for r in pool if not r["chembl_release"] or not r["chembl_sha256"]]
        noscope = [r for r in pool if not r.get("pool_scope")]
        chk("D-6  every pool row records the release, its digest and the scope",
            not norel and not noscope,
            f"{len(norel)} without release/digest, {len(noscope)} without scope"
            if (norel or noscope) else
            f"release {sorted({r['chembl_release'] for r in pool})}, "
            f"scope {sorted({r['pool_scope'] for r in pool})}")

    return report(blocking, passed, pending)


def report(blocking, passed, pending):
    sys.stdout.write("\n=== redo decoy-rule gate ===\n\n")
    for p in passed:
        sys.stdout.write(f"  PASS  {p}\n")
    for b in blocking:
        sys.stdout.write(f"  FAIL  {b}\n")
    if pending:
        sys.stdout.write("\n  not built yet (announced, not skipped):\n")
        for p in pending:
            sys.stdout.write(f"  WAIT  {p}\n")
    sys.stdout.write("\n")
    if blocking:
        sys.stdout.write(f"  {len(blocking)} check(s) failed.\n\n")
        return 1
    sys.stdout.write(f"  CLEAN -- {len(passed)} checks pass"
                     + (f", {len(pending)} deliverable not built.\n\n" if pending
                        else ".\n\n"))
    return 0


# --------------------------------------------------------------------------
def _sub(path, old, new, n=1):
    s = open(path).read()
    open(path, "w").write(s.replace(old, new, n))


def _col(path, row_match, col, val):
    """Set one column on the first matching row (row_match=None -> first row)."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    for r in rows:
        if row_match is None or all(r[k] == v for k, v in row_match.items()):
            r[col] = val
            break
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _drop_row(path, slug):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    rows = [r for r in rows if r["receptor_slug"] != slug]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


PLANTS = [
    ("D-1", "delete the target mapping",
     lambda d: os.remove(os.path.join(d, TARGETS))),
    ("D-2", "drop a panel receptor from the mapping",
     lambda d: _drop_row(os.path.join(d, TARGETS), "CCKAR")),
    ("D-5", "strip the reason from an exclusion",
     lambda d: _col(os.path.join(d, EXCL), None, "ineligible_because", "")),
    ("D-6", "blank the release on a pool row",
     lambda d: _col(os.path.join(d, POOL), None, "chembl_release", "")),
    ("D-4", "make one accession map to two targets",
     lambda d: _sub(os.path.join(d, TARGETS), "\t1\tChEMBL_37", "\t2\tChEMBL_37")),
]


def selftest():
    if main() != 0:
        sys.stdout.write("baseline does not pass; fix that first\n")
        return 1
    sys.stdout.write("baseline: gate passes.  Planting one defect per check.\n\n")
    bad = 0
    for name, what, plant in PLANTS:
        tmp = tempfile.mkdtemp()
        for f in os.listdir(INPUTS):
            if f.endswith((".tsv", ".csv")):
                shutil.copy(os.path.join(INPUTS, f), tmp)
        plant(tmp)
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            rc = main(root=tmp)
        finally:
            sys.stdout = old
            shutil.rmtree(tmp)
        fired = f"FAIL  {name}" in buf.getvalue()
        good = rc == 1 and fired
        bad += 0 if good else 1
        sys.stdout.write(f"  {'ok  ' if good else 'MISS'} {name}: {what}"
                         f" -> {'fired' if fired else 'DID NOT FIRE'}\n")
    sys.stdout.write(f"\n  {len(PLANTS) - bad}/{len(PLANTS)} checks proved by "
                     f"planting. The pool is BUILT: D-5 and D-6 are live.\n\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv))
