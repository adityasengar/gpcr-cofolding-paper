#!/usr/bin/env python3
"""Gate on the redo's curated ligand table.

inputs/ligand_set_redo.tsv enacts D-C's picks.  A ligand table is exactly the
artefact that rewards a gate: the frozen campaign measured its own curation-error
rate on memory-sourced SMILES at 40-46%, and the error that put carazolol in this
table as a neutral antagonist -- when GPCRdb calls it an inverse agonist -- was
made here on 2026-09-12 and caught by a check, not by reading.

    python3 redo/gates/ligands.py
    python3 redo/gates/ligands.py --selftest   # plant one defect per check

Every check is proved by planting the defect it catches.
"""

import csv
import io
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS  # noqa: E402

TABLE = "ligand_set_redo.tsv"
CANDIDATES = "ligand_curation_candidates.tsv"

# GPCRdb's own function vocabulary, per role we assign.
ROLE_FUNCTION = {"full_agonist": {"agonist"},
                 "neutral_antagonist": {"antagonist"}}


def tsv(name, root=None):
    with open(os.path.join(root or INPUTS, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main(argv, root=None):
    root = root or INPUTS
    blocking, passed = [], []

    def chk(label, ok, detail=""):
        (passed if ok else blocking).append(
            label + (f"  -- {detail}" if detail else ""))

    path = os.path.join(root, TABLE)
    if not os.path.exists(path):
        # A missing input FAILS.  A check that does nothing when its input is
        # absent is the defect it exists to catch.
        chk("L-1  the curated ligand table is present", False,
            f"{TABLE} is ABSENT -- run redo/build/ligand_set_redo.py")
        return report(blocking, passed)
    chk("L-1  the curated ligand table is present", True, f"{TABLE}")

    rows = tsv(TABLE, root)
    cands = tsv(CANDIDATES, root)
    enacted = [r for r in rows if r["status"] == "enacted"]
    blocked = [r for r in rows if r["status"] == "BLOCKED"]

    # -- L-2  every enacted pick traces to a candidate row -------------------
    miss = []
    for r in enacted:
        hits = [c for c in cands if c["receptor"] == r["receptor_slug"]
                and c["ligand_ccd"] == r["ligand_ccd"]
                and c["bound_pdb"] == r["bound_pdb"]]
        if len(hits) != 1:
            miss.append(f"{r['receptor_slug']}/{r['ligand_ccd']}@{r['bound_pdb']}"
                        f" -> {len(hits)} candidates")
    chk("L-2  every enacted pick traces to exactly one candidate row",
        not miss, "; ".join(miss) or f"{len(enacted)} picks all resolve")

    # -- L-3  the assigned role agrees with GPCRdb's function label ----------
    # This is the carazolol check.  An inverse agonist recorded as a neutral
    # antagonist silently reopens amendment C-1 without anyone deciding to.
    wrong = []
    for r in enacted:
        hits = [c for c in cands if c["receptor"] == r["receptor_slug"]
                and c["ligand_ccd"] == r["ligand_ccd"]
                and c["bound_pdb"] == r["bound_pdb"]]
        if not hits:
            continue
        fn = hits[0]["function_raw"].strip().lower()
        want = ROLE_FUNCTION.get(r["ligand_role"])
        if want is None or fn not in want:
            wrong.append(f"{r['receptor_slug']}/{r['ligand_ccd']}: role "
                         f"{r['ligand_role']} vs GPCRdb '{hits[0]['function_raw']}'")
    chk("L-3  no enacted role disagrees with GPCRdb's own function label",
        not wrong, "; ".join(wrong) or
        f"{len(enacted)} picks, every role matches its function_raw")

    # -- L-4  chemistry parses, and the pair is chemically distinct ----------
    # OPSD is blocked because agonist and antagonist are one molecule in two
    # isomers.  Any enacted receptor whose two roles share an InChIKey has the
    # same problem and must not be enacted.
    bad = []
    byrec = {}
    for r in enacted:
        if not r["canonical_smiles"]:
            bad.append(f"{r['receptor_slug']}/{r['ligand_ccd']}: SMILES did not parse")
        byrec.setdefault(r["receptor_slug"], []).append(r)
    for rec, rs in byrec.items():
        keys = [r["inchikey"] for r in rs if r["inchikey"]]
        if len(keys) != len(set(keys)):
            bad.append(f"{rec}: agonist and antagonist share an InChIKey — "
                       f"the OPSD problem")
    chk("L-4  every enacted SMILES parses and no receptor's pair is one molecule",
        not bad, "; ".join(bad) or
        f"{len(enacted)} structures parse, {len(byrec)} receptors chemically distinct")

    # -- L-5  every blocked receptor carries a stated reason -----------------
    silent = [r["receptor_slug"] for r in blocked if len(r["why"].strip()) < 40]
    chk("L-5  every blocked receptor says why, in the table itself",
        not silent, ", ".join(silent) or
        f"{len(blocked)} blocked: " + ", ".join(r["receptor_slug"] for r in blocked))

    return report(blocking, passed)


def report(blocking, passed):
    sys.stdout.write("\n=== redo ligand gate ===\n\n")
    for p in passed:
        sys.stdout.write(f"  PASS  {p}\n")
    for b in blocking:
        sys.stdout.write(f"  FAIL  {b}\n")
    sys.stdout.write("\n")
    if blocking:
        sys.stdout.write(f"  {len(blocking)} check(s) failed.\n\n")
        return 1
    sys.stdout.write(f"  CLEAN -- {len(passed)} checks pass.\n\n")
    return 0


# --------------------------------------------------------------------------
def _col(path, row_match, col, val):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    for r in rows:
        if all(r[k] == v for k, v in row_match.items()):
            r[col] = val
            break
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


PLANTS = [
    ("L-1", "delete the table", lambda d: os.remove(os.path.join(d, TABLE))),
    ("L-2", "point a pick at a CCD that is not a candidate",
     lambda d: _col(os.path.join(d, TABLE), {"ligand_ccd": "J8C"}, "ligand_ccd", "ZZZ")),
    ("L-3", "record an agonist as a neutral antagonist",
     lambda d: _col(os.path.join(d, TABLE), {"ligand_ccd": "HSM"},
                    "ligand_role", "neutral_antagonist")),
    ("L-4", "give one receptor the same molecule in both roles",
     lambda d: _col(os.path.join(d, TABLE), {"ligand_ccd": "ML5"}, "inchikey",
                    "KIHYPELVXPAIDH-HNSNBQBZSA-N")),
    ("L-5", "blank a blocked receptor's reason",
     lambda d: _col(os.path.join(d, TABLE), {"receptor_slug": "OPSD"}, "why", "")),
]


def selftest():
    if main(["ligands.py"]) != 0:
        sys.stdout.write("baseline does not pass; fix that before self-testing\n")
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
            rc = main(["ligands.py"], root=tmp)
        finally:
            sys.stdout = old
            shutil.rmtree(tmp)
        fired = f"FAIL  {name}" in buf.getvalue()
        good = rc == 1 and fired
        bad += 0 if good else 1
        sys.stdout.write(f"  {'ok  ' if good else 'MISS'} {name}: {what}"
                         f" -> {'fired' if fired else 'DID NOT FIRE'}\n")
    sys.stdout.write(f"\n  {len(PLANTS) - bad}/{len(PLANTS)} checks proved by "
                     f"planting.\n\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv))
