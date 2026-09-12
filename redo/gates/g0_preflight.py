#!/usr/bin/env python3
"""Group 0 gate — is the instrument frozen, and is it safe to build on?

WHY THIS EXISTS.  `GROUP0_SYSTEMS.md` is frozen as of 2026-09-11.  Frozen means a
reader can act on its numbers without re-deriving them.  This script is what makes
that claim checkable: it re-reads every artefact the document quotes and either
confirms the frozen state or refuses.

Three verdicts, and the distinction is the point:

  PASS  a blocking check that holds.
  FAIL  a blocking check that does not.  Group 0 is NOT frozen; fix before use.
  WAIT  a declared dependency that is not satisfiable here yet.  Not a defect --
        it is work that has to happen elsewhere before that part of E0.1 runs.
        WAIT never fails the gate; it is the outstanding-dependency list.

SELF-TEST.  `--selftest` plants a defect for each blocking check in a scratch copy
of the tree and asserts that the check fires.  A checker that has never failed is
not a checker -- four of this project's checkers once reported nothing because
their reporting path never ran.  Every blocking check below has been proved by
planting.

USAGE
    python3 redo/gates/g0_preflight.py            # the gate
    python3 redo/gates/g0_preflight.py --selftest # prove each check fires
"""
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
ROOT = os.path.dirname(os.path.dirname(INPUTS))

# ---------------------------------------------------------------------------
# The frozen numbers.  These are the values GROUP0_SYSTEMS.md quotes.  If the
# inputs move, these checks fail and the document is stale -- which is exactly
# what "frozen" has to mean to be worth anything.
# ---------------------------------------------------------------------------
FROZEN = {
    "classA_scored": 1336,
    "classA_active": 965,
    "classA_inactive": 371,
    "classA_entries": 199,
    "calib_n": 726, "calib_active": 611, "calib_inactive": 115, "calib_entries": 155,
    "appl_n": 610, "appl_active": 354, "appl_inactive": 256, "appl_entries": 44,
    "f4_n": 433, "f4_active": 372, "f4_inactive": 61,
    "f4_receptors": 106, "f4_both_state": 17,
    "i1": 433, "i2": 289, "i3": 260, "i4": 193,
    "npxxy_entries_measurable": 157,
    "npxxy_5_58_tyr": 164,
    "npxxy_7_53_tyr": 189,
    "intermediates": 21, "intermediate_receptors": 6,
    "pinned_rows": 162, "pinned_npxxy_populated": 64, "pinned_offpanel": 69,
}

GPCRDB_INACTIVE_REF_MAX_A = 11.9   # class A, 2x46-6x37
TILT_CUT = 14.932
NPXXY_CUT = 9.08


def path(*p):
    return os.path.join(ROOT, *p)


def read_csv(p, delim=","):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def main(argv):
    if "--selftest" in argv:
        return selftest()

    blocking, pending, passed = [], [], []

    def chk(name, ok, detail=""):
        (passed if ok else blocking).append(f"{name}  {detail}".rstrip())

    def wait(name, detail):
        pending.append(f"   {name}  {detail}")

    # -- G0-1  the companions exist -----------------------------------------
    required = [
        "g0_calibration_structures.csv", "g0_anchor_conservation.csv",
        "g0_filter_ladder.csv", "g0_independence_ladder.csv",
        "g0_reference_axis_gap.csv", "g0_class_variants.csv",
        "g0_intermediates.csv", "g0_label_conflicts.csv",
        "g0_panel_exclusions.csv", "g0_activation_degree.csv",
        "g0_selftest.txt",
        # read by G0-13, which checks the Class A scope across BOTH populations.
        "g1_receptors.tsv",
    ]
    # The generators are code and live in build/; the artefacts they write are
    # generated and live in inputs/.  This check used to look for both in one
    # directory, which is why it could not survive the files being told apart.
    generators = ["g0_calibration_set.py", "g0_measure_axes.py",
                  "g0_anchor_conservation.py"]
    absent = ([f for f in required if not os.path.exists(os.path.join(INPUTS, f))]
              + [f for f in generators if not os.path.exists(os.path.join(BUILD, f))])
    chk("G0-1  every Group 0 companion is present", not absent,
        f"missing: {absent}" if absent
        else f"{len(required)} in inputs/, {len(generators)} in build/")
    if absent:
        report(blocking, pending, passed)
        return 1

    rows = read_csv(os.path.join(INPUTS, "g0_calibration_structures.csv"))
    cons = read_csv(os.path.join(INPUTS, "g0_anchor_conservation.csv"))
    ladder = read_csv(os.path.join(INPUTS, "g0_filter_ladder.csv"))
    indep = read_csv(os.path.join(INPUTS, "g0_independence_ladder.csv"))
    gap = read_csv(os.path.join(INPUTS, "g0_reference_axis_gap.csv"))

    scored = [r for r in rows if r["state"] in ("Active", "Inactive")]
    calib = [r for r in scored if r["on_panel48"] == "0"]
    appl = [r for r in scored if r["on_panel48"] == "1"]

    # -- G0-2  the population matches the catalogue's split ------------------
    ok = (len(scored) == FROZEN["classA_scored"]
          and len(calib) == FROZEN["calib_n"]
          and sum(1 for r in calib if r["state"] == "Active") == FROZEN["calib_active"]
          and sum(1 for r in calib if r["state"] == "Inactive") == FROZEN["calib_inactive"]
          and len(appl) == FROZEN["appl_n"])
    chk("G0-2  calibration/application split is the frozen 726/610", ok,
        f"{len(calib)}/{len(appl)}, catalogue says "
        f"{FROZEN['calib_n']}/{FROZEN['appl_n']}")

    # -- G0-3  the receptor-disjointness rule actually holds -----------------
    # The whole instrument rests on this: no calibration receptor may appear in
    # the application set under any species.
    cal_slugs = {r["receptor_slug"] for r in calib}
    app_slugs = {r["receptor_slug"] for r in appl}
    overlap = cal_slugs & app_slugs
    chk("G0-3  no receptor appears in both calibration and application", not overlap,
        f"overlap: {sorted(overlap)[:6]}" if overlap else
        f"{len(cal_slugs)} vs {len(app_slugs)} receptors, disjoint")

    # -- G0-4  the axis-definability gate ------------------------------------
    meas = sum(1 for r in cons if r["npxxy_measurable"] == "1")
    y558 = sum(1 for r in cons if r["aa_5_58"] == "Y")
    y753 = sum(1 for r in cons if r["aa_7_53"] == "Y")
    ok = (meas == FROZEN["npxxy_entries_measurable"]
          and y558 == FROZEN["npxxy_5_58_tyr"] and y753 == FROZEN["npxxy_7_53_tyr"])
    chk("G0-4  NPxxY axis definable on 157/199 entries", ok,
        f"5.58 Tyr {y558}, 7.53 Tyr {y753}, both {meas}")

    # -- G0-5  the frozen ladder ---------------------------------------------
    f4 = next((l for l in ladder if l["step"] == "F4"), None)
    ok = (f4 is not None
          and int(f4["n_remaining"]) == FROZEN["f4_n"]
          and int(f4["n_active"]) == FROZEN["f4_active"]
          and int(f4["n_inactive"]) == FROZEN["f4_inactive"]
          and int(f4["n_receptors"]) == FROZEN["f4_receptors"]
          and int(f4["n_receptors_both_states"]) == FROZEN["f4_both_state"])
    chk("G0-5  frozen ladder F4 = 433 (372A/61I, 106 receptors, 17 both-state)", ok,
        f"got {f4['n_remaining']} ({f4['n_active']}A/{f4['n_inactive']}I, "
        f"{f4['n_receptors']} receptors, {f4['n_receptors_both_states']} both-state)"
        if f4 else "F4 row absent")

    # -- G0-6  the retracted rule has not come back --------------------------
    # Q0c calibrated the active pole on GPCRdb activation degree, which GPCRdb
    # defines as "in complex with a signaling protein".  Reinstating it makes the
    # instrument circular.  This check exists so a future session cannot do it by
    # accident.
    src = open(os.path.join(BUILD, "g0_calibration_set.py")).read()
    reinstated = ("F0c" in src) or ("ACTIVE_DEGREE_REQUIRED" in src)
    steps = [l["step"] for l in ladder]
    chk("G0-6  retracted rule Q0c is not reinstated",
        not reinstated and "F0c" not in steps,
        "degree-100 gate is absent from the code and from the ladder"
        if not reinstated else "Q0c HAS RETURNED -- see GROUP0_SYSTEMS.md sec.5.1")

    # -- G0-7  the independence ladder ---------------------------------------
    got = {l["rule"].split()[0]: int(l["n"]) for l in indep}
    ok = all(got.get(k.upper()) == FROZEN[k] for k in ("i1", "i2", "i3", "i4"))
    chk("G0-7  independence ladder I1/I2/I3/I4 = 433/289/260/193", ok,
        f"got {[got.get(k.upper()) for k in ('i1', 'i2', 'i3', 'i4')]}")

    # -- G0-8  the blocker is still described accurately ---------------------
    offp = [g for g in gap if g["on_panel48"] == "0"]
    npx = sum(1 for g in gap if g["npxxy_oh_populated"] == "1")
    ok = (len(gap) == FROZEN["pinned_rows"] and npx == FROZEN["pinned_npxxy_populated"]
          and len(offp) == FROZEN["pinned_offpanel"]
          and sum(1 for g in offp if g["npxxy_oh_populated"] == "1") == 0)
    chk("G0-8  pinned reference set: 162 rows, 64 with NPxxY, 0 of 69 off-panel", ok,
        f"{len(gap)} rows, {npx} with NPxxY, {len(offp)} off-panel")

    # -- G0-9  the per-axis circularity statement still holds ----------------
    # GPCRdb selects inactive REFERENCE structures by d(2x46,6x37) <= 11.9 A on
    # our own tilt axis.  The defensible one-sided claim in sec.5.1 is that no
    # active reference falls at or below that line.  If that ever stops being
    # true the 2x2 in sec.5.1 needs rewriting.
    pinned = read_csv(path("data", "block_b", "09_references",
                           "reference_set.blockb_pinned.csv"))
    act = [float(r["d_gpcrdb_tm6_tilt_ref"]) for r in pinned
           if r["role"] == "active" and r["d_gpcrdb_tm6_tilt_ref"].strip()]
    below = [x for x in act if x <= GPCRDB_INACTIVE_REF_MAX_A]
    chk("G0-9  0 of 95 active references at or below GPCRdb's 11.9 A inactive line",
        len(act) == 95 and not below,
        f"{len(below)} of {len(act)} active refs at or below "
        f"{GPCRDB_INACTIVE_REF_MAX_A} A")

    # -- G0-10  the class F defect is still the defect we described ----------
    # GPCRdb measures class F tilt on 2x44-6x31.  Our rows use the class A pair
    # and the class A threshold.  This check asserts the defect is still present
    # and still unfixed, so that fixing it upstream is noticed rather than
    # silently diverging from sec.10.
    ba = path("data", "block_a", "01_rows", "block_a_rows.csv")
    fclass = [r for r in read_csv(ba) if r.get("gpcr_class") == "F"]
    same_pair = all(r["d_gpcrdb_tm6_tilt_246_637_ca"].strip() for r in fclass)
    same_cut = {r["threshold_tilt_used"] for r in fclass} == {str(TILT_CUT)}
    chk("G0-10  class F defect present as described (700 rows, class A pair+cut)",
        len(fclass) == 700 and same_pair and same_cut,
        f"{len(fclass)} class F rows on d_gpcrdb_tm6_tilt_246_637_ca "
        f"at threshold {sorted({r['threshold_tilt_used'] for r in fclass})}")

    # -- G0-11  the build step still reproduces the shipped values -----------
    st = os.path.join(INPUTS, "g0_selftest.txt")
    txt = open(st).read()
    # Count whole verdict tokens, not substrings: "MISMATCH" contains "MATCH",
    # and counting naively reported 16/2 for a file holding 14 MATCH and 2
    # MISMATCH.  Caught by this check failing on a correct tree, 2026-09-11.
    toks = [w for line in txt.splitlines() for w in line.split()]
    matches = sum(1 for w in toks if w == "MATCH")
    mismatches = sum(1 for w in toks if w == "MISMATCH")
    chk("G0-11  build-step self-test: 14 axis values MATCH, only 5G53 differs",
        matches == 14 and mismatches == 2 and "5G53" in txt,
        f"{matches} MATCH / {mismatches} MISMATCH in g0_selftest.txt")

    # -- outstanding dependencies -------------------------------------------
    wait("D2  panel expansion vs calibration reserve",
         "PI decision. 41 of 61 F4 inactives and every paired receptor sit in the "
         "32 expansion receptors; the panel cannot both absorb them and be "
         "calibrated off them. GROUP0_SYSTEMS.md sec.0.3, sec.6.3.")
    wait("D3  agonist-only admissibility",
         "PI decision, reopened. GPCRdb's activation degree cannot settle it -- "
         "it encodes partner presence. sec.5.1, sec.6.3.")
    wait("D4  balancing rule",
         "PI decision. paajanen anchors + unsupervised fit are adopted; the "
         "reweighting for the reported cut is still open. sec.6.1.")
    wait("D1  NPxxY OH vs Ca  (DEFERRED, does not block)",
         "Aditya 2026-09-11: resolve when the calibration is built. Consequence "
         "if kept as OH: 42 of 199 Class A receptors unevaluable. sec.0.1.")
    wait("Q4  fusion-in-window flag",
         "Needs the 503 RCSB metadata fetches plus the SIFTS-segment fusion "
         "derivation the build step already retrieves. sec.5.4.")
    wait("Q6  engineered-substitution cap",
         "Declared at <=1; not enforceable until verify_partner_chains.py is run "
         "over the calibration receptor chains. sec.5.5.")
    wait("measurement pass",
         "726 calibration + 610 application + 98 pinned reference rows. No GPU, "
         "~1-3 GB of cached mmCIF. sec.4.")
    wait("F3 sensitivity -- does the label-conflict filter bias the inactive pole?",
         "F3 removes 27 inactives (88->61), 31% of the scarce class, concentrated in "
         "five receptors (5HT2A loses 10). PRELIMINARY signal from the 30-row pilot, "
         "n=4: removed inactives sit at d_npxxy_oh 9.43 vs 11.51 for those retained, "
         "against a 9.08 threshold -- i.e. F3 may be discarding the cases nearest the "
         "boundary. Needs the measurement pass, then both thresholds recomputed with "
         "F3 on and off. The pass must ALSO measure the F3-REMOVED structures, or the "
         "filter's effect stays unauditable. DECISIONS.md F-12.")
    # The "class F atom pair" WAIT stood here until 2026-09-12: measure class F
    # tilt on 2x44-6x31 or drop the class F arm.  Aditya chose the scope --
    # DECISIONS.md D-2026-09-12-d, the redo is a Class A paper -- so the arm is
    # dropped and the dependency is answered rather than discharged.  What
    # replaces it is G0-13, which guards the scope instead of waiting on it.
    # -- G0-12  the regenerable mmCIF cache is excluded from git ------------
    # This was a wait() until 2026-09-11, which is a check that can never clear:
    # the work is the orchestrator's and the gate had no way to see it land.
    # A dependency nobody can discharge reads exactly like one nobody has.
    gi = os.path.join(ROOT, ".gitignore")
    rules = []
    if os.path.exists(gi):
        rules = [ln.strip() for ln in open(gi, encoding="utf-8")
                 if ln.strip() and not ln.lstrip().startswith("#")]
    want = "redo/cache/structures/"
    chk("G0-12  the 1-3 GB mmCIF cache is gitignored", want in rules,
        f"{want} present in .gitignore" if want in rules
        else f"{want} NOT in .gitignore -- the cache will be committed")

    # -- G0-13  the scope is Class A, and stays Class A ----------------------
    # D-2026-09-12-d closed E0.5 at "drop B and F and say the work is Class A",
    # on measured grounds: F-13 found a 9 A inter-backbone disagreement on class
    # B apo and no discriminating power at all on class F.  Both populations were
    # already Class A by construction, which is exactly why this needs a guard --
    # nothing would have complained if another class drifted back in.
    calib_classes = sorted({r["gpcr_class"] for r in rows})
    rec = read_csv(os.path.join(INPUTS, "g1_receptors.tsv"), delim="\t")
    panel_classes = sorted({r["gclass"] for r in rec})
    ok = calib_classes == ["Class A (Rhodopsin)"] and panel_classes == ["A"]
    chk("G0-13  the redo is Class A only, in both populations", ok,
        f"calibration {len(rows)} rows all Class A, panel {len(rec)} receptors all A"
        if ok else
        f"calibration classes {calib_classes}, panel classes {panel_classes}")

    return report(blocking, pending, passed)


def report(blocking, pending, passed):
    sys.stdout.write("\n=== Group 0 preflight ===\n\n")
    for p in passed:
        sys.stdout.write(f"  PASS  {p}\n")
    for b in blocking:
        sys.stdout.write(f"  FAIL  {b}\n")
    if pending:
        sys.stdout.write("\n  outstanding dependencies (not defects):\n")
        for p in pending:
            sys.stdout.write(f"  WAIT{p}\n")
    sys.stdout.write("\n")
    if blocking:
        sys.stdout.write(f"  NOT FROZEN -- {len(blocking)} blocking check(s) failed.\n\n")
        return 1
    sys.stdout.write(f"  FROZEN -- {len(passed)} blocking checks pass, "
                     f"{len(pending)} dependencies outstanding.\n\n")
    return 0


# ---------------------------------------------------------------------------
# Self-test: plant a defect per blocking check and assert it fires.
# ---------------------------------------------------------------------------

PLANTS = [
    ("G0-1", "delete a companion",
     lambda d: os.remove(os.path.join(d, "redo/inputs/g0_class_variants.csv"))),
    ("G0-2", "drop one calibration structure",
     lambda d: _drop_row(os.path.join(d, "redo/inputs/g0_calibration_structures.csv"),
                         lambda r: r["on_panel48"] == "0" and r["state"] == "Active")),
    ("G0-3", "move one calibration receptor onto the panel",
     lambda d: _set_first(os.path.join(d, "redo/inputs/g0_calibration_structures.csv"),
                          lambda r: r["on_panel48"] == "0", "on_panel48", "1")),
    ("G0-4", "turn a Tyr5.58 into an Ala",
     lambda d: _set_first(os.path.join(d, "redo/inputs/g0_anchor_conservation.csv"),
                          lambda r: r["aa_5_58"] == "Y", "aa_5_58", "A")),
    ("G0-5", "alter the frozen F4 count",
     lambda d: _set_first(os.path.join(d, "redo/inputs/g0_filter_ladder.csv"),
                          lambda r: r["step"] == "F4", "n_remaining", "999")),
    ("G0-6", "reinstate the retracted Q0c gate",
     lambda d: _append(os.path.join(d, "redo/build/g0_calibration_set.py"),
                       "\nACTIVE_DEGREE_REQUIRED = 100\n")),
    ("G0-7", "alter the frozen I2 count",
     lambda d: _set_first(os.path.join(d, "redo/inputs/g0_independence_ladder.csv"),
                          lambda r: r["rule"].startswith("I2"), "n", "999")),
    ("G0-8", "populate NPxxY on an off-panel pinned row",
     lambda d: _set_first(os.path.join(d, "redo/inputs/g0_reference_axis_gap.csv"),
                          lambda r: r["on_panel48"] == "0", "npxxy_oh_populated", "1")),
    ("G0-9", "push an active reference below GPCRdb's 11.9 A line",
     lambda d: _set_first(os.path.join(
         d, "data/block_b/09_references/reference_set.blockb_pinned.csv"),
         lambda r: r["role"] == "active" and r["d_gpcrdb_tm6_tilt_ref"].strip(),
         "d_gpcrdb_tm6_tilt_ref", "10.5")),
    ("G0-10", "change the class F threshold, as an upstream fix would",
     lambda d: _set_all(os.path.join(d, "data/block_a/01_rows/block_a_rows.csv"),
                        lambda r: r.get("gpcr_class") == "F",
                        "threshold_tilt_used", "13.0")),
    ("G0-11", "turn a self-test MATCH into a MISMATCH",
     lambda d: _sub(os.path.join(d, "redo/inputs/g0_selftest.txt"),
                    "MATCH", "MISMATCH", 1)),
    ("G0-13", "let a class B receptor drift back into the panel",
     lambda d: _sub(os.path.join(d, "redo/inputs/g1_receptors.tsv"),
                    "\tA\t", "\tB1\t", 1)),
]


def selftest():
    base = subprocess.run([sys.executable, os.path.abspath(__file__)],
                          capture_output=True, text=True, cwd=ROOT)
    if base.returncode != 0:
        sys.stdout.write("baseline gate does not pass; fix that before self-testing\n")
        sys.stdout.write(base.stdout)
        return 1
    sys.stdout.write("baseline: gate passes.  Planting one defect per blocking check.\n\n")
    bad = 0
    for name, what, plant in PLANTS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = os.path.join(tmp, "tree")
            _clone(ROOT, dst)
            try:
                plant(dst)
            except Exception as e:  # planting itself failed -- that is a miss
                sys.stdout.write(f"  MISS {name}: could not plant ({e})\n")
                bad += 1
                continue
            out = subprocess.run(
                [sys.executable, os.path.join(dst, "redo/gates/g0_preflight.py")],
                capture_output=True, text=True, cwd=dst).stdout
            fired = f"FAIL  {name}" in out
            sys.stdout.write(f"  {'ok  ' if fired else 'MISS'} {name}: {what}"
                             f" -> {'check fired' if fired else 'CHECK DID NOT FIRE'}\n")
            bad += 0 if fired else 1
    sys.stdout.write(f"\n  {len(PLANTS) - bad}/{len(PLANTS)} blocking checks proved "
                     f"by planting.\n\n")
    return 1 if bad else 0


# The gate reads redo/inputs/ and redo/build/ and RUNS from redo/gates/, so the
# scratch clone must recurse.  It did not: until 2026-09-12 this copied only the
# TOP-LEVEL files of each directory, which was correct while redo/ was flat and
# silently wrong from the moment the campaign moved to the guarded layout on
# 2026-09-11.  Every plant then failed to apply, every check reported MISS, and
# the harness still printed a tidy tally -- so "proved by planting" was asserted
# in three documents while 0 of 11 checks were actually being proved.
# Directories that are large and that no plant touches are skipped by name.
_CLONE_SKIP = {"cache", "protocol", "runs", "__pycache__", ".git"}


def _clone(src, dst):
    """Copy what the gate reads AND what it runs.  Recurses; skips the bulk."""
    for rel in ("redo", "data/block_b/09_references",
                "data/block_a/01_rows"):
        s, d = os.path.join(src, rel), os.path.join(dst, rel)
        shutil.copytree(s, d, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(*_CLONE_SKIP))
        # data/block_* is read-only in the real tree and copy2 preserves that,
        # which stopped the G0-9 plant from being written.  Make the SCRATCH
        # copy writable; the drop itself is never touched.
        for root, _, files in os.walk(d):
            for f in files:
                os.chmod(os.path.join(root, f), 0o644)


def _rows(p):
    with open(p) as fh:
        r = csv.DictReader(fh)
        return list(r), r.fieldnames


def _write(p, rows, cols):
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _set_first(p, pred, col, val):
    rows, cols = _rows(p)
    for r in rows:
        if pred(r):
            r[col] = val
            break
    else:
        raise ValueError("no row matched")
    _write(p, rows, cols)


def _set_all(p, pred, col, val):
    rows, cols = _rows(p)
    n = 0
    for r in rows:
        if pred(r):
            r[col] = val
            n += 1
    if not n:
        raise ValueError("no row matched")
    _write(p, rows, cols)


def _drop_row(p, pred):
    rows, cols = _rows(p)
    for i, r in enumerate(rows):
        if pred(r):
            rows.pop(i)
            break
    else:
        raise ValueError("no row matched")
    _write(p, rows, cols)


def _append(p, text):
    with open(p, "a") as fh:
        fh.write(text)


def _sub(p, old, new, n):
    s = open(p).read()
    if old not in s:
        raise ValueError("pattern absent")
    open(p, "w").write(s.replace(old, new, n))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
