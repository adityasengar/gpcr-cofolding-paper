#!/usr/bin/env python3
"""g2_preflight.py -- the dispatch-readiness gate for Group 2, the ligand arm.

Nothing in Group 2 is submitted until this exits 0.  Same contract as
`g1_preflight.py`: BLOCKING checks must pass; PENDING items are dependencies that
have not landed and are reported as NOT READY rather than as failures, because a
dependency in flight is not a defect.

Run:  python3 redo/gates/g2_preflight.py
Exit: 0 = every BLOCKING check passed and nothing is PENDING
      1 = a BLOCKING check failed
      2 = all BLOCKING checks passed but a PENDING dependency is outstanding

Prove the checks rather than trusting them:
  python3 redo/gates/g2_preflight.py --selftest
plants a defect for each blocking check in a scratch copy and asserts it fires.

The one rule this gate is built around: **a missing input FAILS, it does not
skip.**  Four checkers in this project have already reported nothing because their
reporting path never ran, and a silent check looks exactly like a passing one.
"""
import csv
import io
import os
import re
import shutil
import sys
import tempfile
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS                       # noqa: E402

SYSTEMS = "g2_systems.csv"
NEED = [SYSTEMS, "ligand_tiers.tsv", "ligand_set_redo.tsv", "g1_receptors.tsv",
        "g1_panel_freeze.tsv", "g1_partner_registry.tsv", "g1_cognate.tsv",
        # the decoy identity, from 2026-09-12.  Its absence is a FAILURE here, not
        # a pending dependency: g2_systems.csv's decoy cells are resolved against
        # it, so a gate that tolerated its absence would be checking those cells
        # against nothing.
        "drule_selected.tsv"]

# The tier a receptor's ligand_tier maps to, and the pool it may be reported in.
# T2 and T3 are NEVER pooled into T1 -- D-2026-09-12-f: at 2 and 7 clusters neither
# can carry the headline contrast, and saying so is the point of tiering them.
POOL_OF_TIER = {"T1_small_molecule": "T1_HEADLINE",
                "T2_peptide": "T2_REPORTED_APART",
                "T3_mixed": "T3_REPORTED_APART"}
# The decoy arm runs below CAMPAIGN.md sec.5.3's pre-registered >=12-cluster bar,
# by Aditya's decision of 2026-09-12, and every decoy row says so in ligand_flag.
# G-14 is what makes that unmissable rather than merely written down somewhere.
EXPLORATORY_FLAG = "EXPLORATORY_MISSED_PREREG_CLUSTER_BAR"


def tsv(name, root):
    with open(os.path.join(root, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def csvf(name, root):
    with open(os.path.join(root, name)) as fh:
        return list(csv.DictReader(fh))


def main(argv, root=None):
    root = root or INPUTS
    blocking, pending, passed = [], [], []

    def B(ok, label, detail=""):
        (passed if ok else blocking).append(
            label + (f" -- {detail}" if detail and not ok else ""))

    def W(label, detail):
        pending.append(f"{label} -- {detail}")

    # ------------------------------------------------------- G-1 files exist
    absent = [f for f in NEED if not os.path.exists(os.path.join(root, f))]
    B(not absent, "G-1  every input artefact exists", f"absent: {absent}")
    if absent:
        report(blocking, pending, passed)
        return 1

    rows = csvf(SYSTEMS, root)
    tiers = {r["receptor_slug"]: r for r in tsv("ligand_tiers.tsv", root)}
    frz = {r["receptor_slug"]: r for r in tsv("g1_panel_freeze.tsv", root)}
    reg = tsv("g1_partner_registry.tsv", root)
    lsr = tsv("ligand_set_redo.tsv", root)
    primary = {s for s, r in frz.items() if r["core_frozen"] == "yes"}

    if not rows:
        B(False, "G-1  every input artefact exists", f"{SYSTEMS} has no rows")
        report(blocking, pending, passed)
        return 1

    # ------------------------------------------- G-2 no tier is pooled with T1
    # Two ways this goes wrong and both are checked: a row declaring the wrong
    # pool for its receptor's tier, and an arm whose membership straddles tiers.
    wrong = sorted({(r["receptor_slug"], r["ligand_tier"], r["pool_group"])
                    for r in rows
                    if POOL_OF_TIER.get(r["ligand_tier"]) != r["pool_group"]})
    bytier = defaultdict(set)
    for r in rows:
        bytier[(r["item"], r["arm"])].add(r["ligand_tier"])
    mixed = sorted(k for k, v in bytier.items() if len(v) > 1)
    B(not wrong and not mixed,
      "G-2  no T2 or T3 row is pooled with T1",
      f"mis-pooled rows: {wrong[:4]}; tier-mixing arms: {mixed[:4]}")

    # --------------------------- G-3 every enacted pick reaches the enumeration
    enacted = {(r["receptor_slug"], r["ligand_role"]) for r in lsr
               if r["status"] == "enacted"}
    got = {(r["receptor_slug"], r["ligand_role_actual"]) for r in rows
           if r["ligand_identity_source"].startswith("REDO:")}
    missing = sorted(enacted - got)
    B(not missing,
      "G-3  every enacted ligand resolves to a row in the enumeration",
      f"enacted but never dispatched: {missing}")

    # ------------------------ G-4 an inverse agonist is never a neutral one
    # D-2026-09-12-f: `inverse_agonist` is recorded as its OWN role, never
    # relabelled.  Checked against the census's own typing, not against the
    # generator's verdict -- a check that reads back the column the generator
    # wrote is not a check.
    conflated = sorted({(r["receptor_slug"], r["ligand"], r["ligand_role_actual"])
                        for r in rows
                        if r["ligand"] == "antagonist"
                        and r["ligand_role_actual"] != (
                            "inverse_agonist"
                            if tiers[r["receptor_slug"]]["antagonist_role"]
                            == "inverse_agonist" else "neutral_antagonist")})
    also = sorted({(r["receptor_slug"], r["ligand_role_actual"]) for r in rows
                   if r["ligand"] == "inverse_agonist"
                   and r["ligand_role_actual"] != "inverse_agonist"})
    B(not conflated and not also,
      "G-4  no inverse agonist is recorded as a neutral antagonist",
      f"{conflated[:4]} {also[:4]}")

    # ---------------------------- G-5 a blocked receptor cannot be dispatched
    blocked_recs = {r["receptor_slug"] for r in lsr if r["status"] != "enacted"}
    leak = sorted({(r["receptor_slug"], r["dispatch_status"]) for r in rows
                   if r["receptor_slug"] in blocked_recs
                   and (r["dispatch_status"] == "READY"
                        or int(r["predictions_pooled"]) > 0
                        or int(r["predictions_percell"]) > 0)})
    B(not leak, "G-5  no blocked receptor carries a dispatchable row",
      f"blocked receptors {sorted(blocked_recs)} leaked: {leak}")

    # ----------------------------------------- G-6, G-12, G-13, G-14  the decoys
    # Rewritten 2026-09-12.  These four RE-DERIVE from inputs/drule_selected.tsv
    # rather than asserting a constant, so the selection and the dispatch table
    # cannot drift apart.  The check they replace asserted that EVERY decoy cell is
    # unresolved -- true while the pool was unbuilt and false the moment
    # drule_select.py ran, which is precisely why a gate must not hard-code the
    # state of its own dependency.
    dec = [r for r in rows if r["ligand"] == "decoy_lig"]
    sel = tsv("drule_selected.tsv", root)
    want_acc, want_ref = {}, {}
    for r in sel:
        if r["decoy_status"] == "accepted":
            want_acc.setdefault(r["receptor_slug"], []).append(
                (int(r["draw_rank"]), r["candidate_chembl_id"], r["inchikey"]))
        elif r["decoy_status"] == "decoy-unavailable":
            want_ref[r["receptor_slug"]] = r
    for v in want_acc.values():
        v.sort()

    # -- G-6  a resolved cell names EXACTLY the three accepted decoys -------
    bad = []
    for r in dec:
        s = r["receptor_slug"]
        if s not in want_acc:
            continue
        ids = r["ligand_name"].split("|")
        iks = r["ligand_inchikey"].split("|")
        exp_ids = [c for _k, c, _i in want_acc[s]]
        exp_iks = [i for _k, _c, i in want_acc[s]]
        why = []
        if ids != exp_ids:
            why.append(f"names {ids} not {exp_ids}")
        if iks != exp_iks:
            why.append("InChIKeys do not match the selection")
        if len(set(iks)) != len(iks) or not all(iks):
            why.append(f"{len(set(iks))} distinct InChIKeys for {len(iks)} decoys -- "
                       f"ligand_must_key_by=inchikey cannot address them")
        if len(ids) != int(r["n_shared_draws"]):
            why.append(f"{len(ids)} molecules across n_shared_draws="
                       f"{r['n_shared_draws']}; the draws ARE the molecules")
        if r["ligand_identity_status"] != "RESOLVED_DRULE_DECOY":
            why.append(f"status {r['ligand_identity_status']}")
        if r["dispatch_status"] != "READY" or int(r["predictions_pooled"]) == 0:
            why.append(f"{r['dispatch_status']} at "
                       f"{r['predictions_pooled']} pooled predictions")
        if why:
            bad.append(f"{s}/{r['chain_b_construct']}: " + "; ".join(why))
    B(bool(dec) and not bad,
      "G-6  a resolved decoy cell names exactly the three accepted decoys, with "
      "three distinct InChIKeys, and dispatches",
      f"{'the decoy arm is absent entirely' if not dec else bad[:3]}")

    # -- G-12  a refused receptor is blocked at zero, with ITS OWN reason ---
    bad = []
    for s, want in sorted(want_ref.items()):
        cells = [r for r in dec if r["receptor_slug"] == s]
        if not cells:
            bad.append(f"{s}: refused by the selection and ABSENT from the decoy "
                       f"arm -- a receptor that vanishes looks like one nobody "
                       f"considered")
            continue
        for r in cells:
            if (r["ligand_identity_status"] != "BLOCKED_DECOY_UNAVAILABLE"
                    or r["dispatch_status"] == "READY"
                    or int(r["predictions_pooled"]) or int(r["predictions_percell"])):
                bad.append(f"{s}: {r['dispatch_status']} / "
                           f"{r['ligand_identity_status']} at "
                           f"{r['predictions_pooled']} predictions")
            elif want["reason"] not in r["note"]:
                # verbatim, and per receptor.  B1B1U5 is refused because eligibility
                # is UNESTABLISHABLE (no ChEMBL target, therefore no exclusion rows);
                # the other four because too few eligible candidates passed.  Those
                # are different facts and a generic "no decoy" erases the difference.
                bad.append(f"{s}: its own recorded reason is not carried in the row")
    B(not bad, "G-12  a decoy-unavailable receptor is blocked at zero predictions "
               "and carries its OWN recorded reason, verbatim", f"{bad[:3]}")

    # -- G-13  the resolved set IS the accepted set, in BOTH directions ------
    # The property the old G-6 had and that must survive: it fires if a decoy
    # appears for a refused receptor, AND if a passing receptor's arm goes missing.
    got_res = {r["receptor_slug"] for r in dec
               if r["ligand_identity_status"] == "RESOLVED_DRULE_DECOY"}
    extra = sorted(got_res - set(want_acc))
    missing = sorted(set(want_acc) - got_res)
    B(not extra and not missing,
      "G-13  the receptors with a resolved decoy are exactly those the selection "
      "accepted, in both directions",
      f"resolved but NOT accepted: {extra}; accepted but NOT in the arm: {missing}")

    # -- G-14  the exploratory marker is on every decoy row ------------------
    # The arm runs below sec.5.3's pre-registered >=12-cluster bar.  If that is
    # recorded only in prose, a downstream reader can take it for a confirmatory
    # result without doing anything wrong, so it travels in the data on every row.
    noflag = sorted({(r["receptor_slug"], r["item"]) for r in dec
                     if EXPLORATORY_FLAG not in r["ligand_flag"]})
    nonote = sorted({(r["receptor_slug"], r["item"]) for r in dec
                     if "EXPLORATORY, NOT CONFIRMATORY" not in r["note"]})
    kc = len({r["receptor_cluster"] for r in dec
              if r["ligand_identity_status"] == "RESOLVED_DRULE_DECOY"})
    B(bool(dec) and not noflag and not nonote,
      "G-14  every decoy row carries the EXPLORATORY marker in ligand_flag and the "
      "deviation arithmetic in note",
      f"no flag: {noflag[:3]}; no note: {nonote[:3]}"
      if (noflag or nonote) else "the decoy arm is absent entirely")

    # ------------------------------ G-7 each receptor set is exactly its tier
    want = defaultdict(set)
    for s in primary:
        t = tiers[s]["ligand_tier"]
        if t in POOL_OF_TIER:
            want[t].add(s)
    curated_t1 = want["T1_small_molecule"] - blocked_recs
    have = defaultdict(set)
    for r in rows:
        have[r["receptor_set"]].add(r["receptor_slug"])
    errs = []
    for rset, expect in (("LIG_T1", curated_t1),
                         ("LIG_T1_BLOCKED", want["T1_small_molecule"] & blocked_recs),
                         ("LIG_T2", want["T2_peptide"]),
                         ("LIG_T3", want["T3_mixed"])):
        if have.get(rset, set()) != expect:
            errs.append(f"{rset}: missing {sorted(expect - have.get(rset, set()))}, "
                        f"extra {sorted(have.get(rset, set()) - expect)}")
    B(not errs, "G-7  every receptor set is exactly the tier table's membership",
      "; ".join(errs))

    # ------------------------- G-8 a READY row has every input resolved
    held = {r["construct"] for r in reg if r["held"] == "yes"} | {"R0_apo"}
    unres = sorted({(r["receptor_slug"], r["chain_b_construct"], r["ligand"],
                     r["ligand_identity_status"]) for r in rows
                    if r["dispatch_status"] == "READY"
                    and (r["chain_b_construct"] not in held
                         or r["chain_b_sha256"].startswith(("UNRESOLVED", "PENDING"))
                         or r["chain_b_len"] == "UNRESOLVED"
                         or r["ligand_identity_status"].startswith("UNRESOLVED"))})
    B(not unres, "G-8  no READY row carries an unresolved chain B or ligand",
      f"{unres[:4]}")

    # --------------------------------- G-9 the design is completely crossed
    # A 2x2 with a missing cell is not a 2x2.  Within each arm, every
    # (receptor, ligand level) must appear at every partner level the arm uses.
    partners = defaultdict(set)
    cells = defaultdict(set)
    for r in rows:
        k = (r["item"], r["arm"])
        partners[k].add(r["chain_b_construct"])
        cells[(k, r["receptor_slug"], r["ligand"])].add(r["chain_b_construct"])
    holes = sorted({(k[0], k[1], rec, lig,
                     tuple(sorted(partners[k] - p)))
                    for (k, rec, lig), p in cells.items() if partners[k] - p})
    B(not holes, "G-9  every arm is completely crossed over its partner axis",
      f"{len(holes)} incomplete cells, e.g. {holes[:3]}")

    # ------------------------- G-10 the prediction counts reproduce
    mism = []
    for r in rows:
        nbb = len(r["backbones"].split("|"))
        ready = r["dispatch_status"] == "READY"
        for grain, col, bcol in (("n_pooled", "predictions_pooled",
                                  "blocked_predictions_pooled"),
                                 ("n_percell", "predictions_percell",
                                  "blocked_predictions_percell")):
            exp = nbb * int(r[grain])
            if int(r[col]) != (exp if ready else 0) or \
                    int(r[bcol]) != (0 if ready else exp):
                mism.append((r["item"], r["receptor_slug"], r["ligand"], col,
                             r[col], exp))
    B(not mism, "G-10  every prediction count reproduces from backbones x n",
      f"{len(mism)} rows disagree, e.g. {mism[:3]}")

    # ------------------- G-11 the partner-MSA condition, same as g1's B7/B8
    msa = sorted({(r["chain_b_construct"], r["partner_msa"]) for r in rows
                  if (r["chain_b_construct"] == "R0_apo"
                      and r["partner_msa"] != "n/a")
                  or (r["chain_b_construct"] != "R0_apo"
                      and r["partner_msa"] != "off")})
    B(not msa, "G-11  every cognate row runs the partner MSA-free, every apo row n/a",
      f"{msa[:4]}")

    # ------------------------------------------------------------- PENDING
    if dec:
        # Every quantity here is DERIVED from the two files, never asserted.  This
        # line has already gone stale twice -- once saying the pool was not built
        # after it was, once saying no molecule was selected after selection ran --
        # and both times the words were right when written and wrong within a day.
        # So: count the states, and let the sentence follow the count.
        res = [r for r in dec if r["ligand_identity_status"] == "RESOLVED_DRULE_DECOY"]
        blk = [r for r in dec if r["ligand_identity_status"]
               == "BLOCKED_DECOY_UNAVAILABLE"]
        kc = len({r["receptor_cluster"] for r in res})
        kr = len({r["receptor_slug"] for r in res})
        mde, target = 1.218 / max(kc, 1) ** 0.5, 1.218 / 12 ** 0.5
        by_class = defaultdict(list)
        for s, w in sorted(want_ref.items()):
            by_class["eligibility unestablishable (no ChEMBL target)"
                     if int(w["n_eligible"] or 0) == 0
                     else "fewer than k candidates passed the eight axes"].append(s)
        W("the decoy arm is EXPLORATORY -- it runs below its own pre-registered bar",
          f"{len(res)} of {len(dec)} cells resolve, on {kr} receptors / {kc} "
          f"clusters; CAMPAIGN.md sec.5.3 pre-registers >=12 clusters. MDE "
          f"{mde:.3f} vs {target:.3f} at k=12 ({100 * (mde / target - 1):.1f}% less "
          f"sensitive), {sum(int(r['predictions_pooled']) for r in res)} pooled / "
          f"{sum(int(r['predictions_percell']) for r in res)} per-cell predictions. "
          f"Aditya's decision 2026-09-12: run it and pay the loss, strict rule kept. "
          f"{len(blk)} cells stay blocked, "
          + "; ".join(f"{', '.join(v)} -- {k}" for k, v in sorted(by_class.items()))
          + ". NOT a defect and NOT confirmatory: no claim may rest on this arm.")
    chain = sorted({(r["receptor_slug"], r["ligand_role_actual"]) for r in rows
                    if r["ligand_identity_status"] == "UNRESOLVED_CHAIN_NO_SEQUENCE"})
    if chain:
        W("chain-ligand sequences are not held",
          f"{chain} -- curated structurally in ligand_set_redo.tsv but the bytes "
          f"to supply as a polymer chain are nowhere in redo/inputs/")
    unc = sorted({(r["receptor_slug"], r["ligand_role_actual"]) for r in rows
                  if r["ligand_identity_status"] == "UNRESOLVED_UNCURATED"})
    if unc:
        W("uncurated ligands named by the census but never enacted", f"{unc}")
    relab = sorted({r["receptor_slug"] for r in rows
                    if "source_row_role_disagrees_with_gpcrdb" in r["ligand_flag"]})
    if relab:
        W("an inherited row's role disagrees with GPCRdb",
          f"{relab} -- taken under the census's role, flagged, not absorbed")
    mal = sorted({(r["receptor_slug"], r["ligand_role_actual"]) for r in rows
                  if "column_shift_in_source_row" in r["ligand_flag"]})
    if mal:
        W("an inherited row's provenance columns are shifted",
          f"{mal} -- chemistry unaffected, ccd_code holds prose (F-18)")
    items = sorted({r["item"] for r in rows})
    W("RUN_MATRIX 7.1 has no line item for the Group 2 arms",
      f"{items} -- the same documentation drift check B18 found for Group 1; "
      f"RUN_MATRIX costs G6a/b on CORE-L17 (17 clusters of a Block C-derived core), "
      f"and this enumeration runs on the frozen panel's T1 (16 receptors, 15 "
      f"clusters). The two panels are different objects with the same number on them")

    report(blocking, pending, passed)
    return 1 if blocking else (2 if pending else 0)


def report(blocking, pending, passed):
    for p in passed:
        sys.stdout.write(f"  PASS  {p}\n")
    for b in blocking:
        sys.stdout.write(f"  FAIL  {b}\n")
    for p in pending:
        sys.stdout.write(f"  WAIT  {p}\n")
    sys.stdout.write(f"\n{len(passed)} passed, {len(blocking)} failed, "
                     f"{len(pending)} pending\n")
    if blocking:
        sys.stdout.write("DO NOT DISPATCH.\n")
    elif pending:
        sys.stdout.write("Blocking checks pass; dependencies outstanding.\n")
    else:
        sys.stdout.write("READY.\n")


# ---------------------------------------------------------------- selftest
def _rewrite(path, fn):
    rows = list(csv.DictReader(open(path)))
    rows = [r for r in (fn(r) for r in rows) if r is not None]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _set(path, match, col, val, limit=None):
    n = [0]

    def f(r):
        if all(r[k] == v for k, v in match.items()) and (limit is None or n[0] < limit):
            n[0] += 1
            r[col] = val
        return r
    _rewrite(path, f)


def _drop(path, match, limit=None):
    n = [0]

    def f(r):
        if all(r[k] == v for k, v in match.items()) and (limit is None or n[0] < limit):
            n[0] += 1
            return None
        return r
    _rewrite(path, f)


def _dup_inchikey(path):
    """Collapse two of a decoy cell's three InChIKeys onto one.

    Not a blunt "make it READY": the cell still names three ChEMBL ids and still
    splits n across three draws, so every total in the table stays right while
    `ligand_must_key_by = inchikey` now addresses two molecules where three were
    drawn.  That is the failure a check on this field has to catch.
    """
    def f(r):
        if (r["ligand"] == "decoy_lig"
                and r["ligand_identity_status"] == "RESOLVED_DRULE_DECOY"
                and not f.done):
            iks = r["ligand_inchikey"].split("|")
            if len(iks) == 3:
                r["ligand_inchikey"] = "|".join([iks[0], iks[0], iks[2]])
                f.done = True
        return r
    f.done = False
    _rewrite(path, f)


CASES = {
    # a missing input must FAIL, never skip
    "G-1": ("ligand_tiers.tsv", lambda p: os.remove(p)),
    # report a T3 receptor inside the headline pool
    "G-2": (SYSTEMS, lambda p: _set(p, {"receptor_set": "LIG_T3"},
                                    "pool_group", "T1_HEADLINE")),
    # an enacted pick that never reaches a dispatch row
    "G-3": (SYSTEMS, lambda p: _set(p, {"receptor_slug": "S1PR1",
                                        "ligand": "antagonist"},
                                    "ligand_identity_source", "INHERITED:elsewhere")),
    # the carazolol error: an inverse agonist recorded as a neutral antagonist
    "G-4": (SYSTEMS, lambda p: _set(p, {"receptor_slug": "ADRB1",
                                        "ligand": "antagonist"},
                                    "ligand_role_actual", "neutral_antagonist")),
    # the refused receptor slips into dispatch
    "G-5": (SYSTEMS, lambda p: _set(p, {"receptor_slug": "PD2R2"},
                                    "dispatch_status", "READY")),
    # two of a receptor's three decoys collapse onto one InChIKey -- the subtler
    # form of the defect, because the cell still names three molecules and still
    # splits n three ways, and ligand_must_key_by=inchikey silently addresses two
    "G-6": (SYSTEMS, _dup_inchikey),
    # a receptor silently vanishes from its tier's arm
    "G-7": (SYSTEMS, lambda p: _drop(p, {"receptor_slug": "HRH3"})),
    # a READY row whose partner never resolved
    "G-8": (SYSTEMS, lambda p: _set(p, {"dispatch_status": "READY",
                                        "chain_b_construct": "R3_ct21"},
                                    "chain_b_sha256", "UNRESOLVED:no R3_ct21",
                                    limit=1)),
    # half of a 2x2: the apo cell of one (receptor, ligand) disappears
    "G-9": (SYSTEMS, lambda p: _drop(p, {"item": "G6a/G6b",
                                         "receptor_slug": "CNR2",
                                         "ligand": "full_agonist",
                                         "chain_b_construct": "R0_apo"})),
    # a budget that does not reproduce from its own factors
    "G-10": (SYSTEMS, lambda p: _set(p, {"item": "G6a/G6b"},
                                     "predictions_pooled", "999", limit=1)),
    # the F-5 confound: a cognate row running its partner MSA on
    "G-11": (SYSTEMS, lambda p: _set(p, {"chain_b_construct": "R3_ct21"},
                                     "partner_msa", "ON", limit=1)),
    # B1B1U5's categorically different refusal flattened into a generic one
    "G-12": (SYSTEMS, lambda p: _set(p, {"receptor_slug": "B1B1U5",
                                         "ligand": "decoy_lig"},
                                     "note", "pool not built")),
    # BOTH directions of the resolved-set identity, which is the property the old
    # G-6 had and that must survive its rewrite
    "G-13": [
        # (a) a REFUSED receptor acquires a resolved decoy
        (SYSTEMS, lambda p: _set(p, {"receptor_slug": "HRH3",
                                     "ligand": "decoy_lig"},
                                 "ligand_identity_status", "RESOLVED_DRULE_DECOY")),
        # (b) a PASSING receptor's decoy arm goes missing
        (SYSTEMS, lambda p: _drop(p, {"receptor_slug": "OPSD",
                                      "ligand": "decoy_lig"})),
    ],
    # the exploratory marker stripped from one row, so the arm could be read as
    # confirmatory by someone doing nothing wrong
    "G-14": (SYSTEMS, lambda p: _set(p, {"ligand": "decoy_lig"},
                                     "ligand_flag", "", limit=1)),
}


def selftest():
    """Plant one defect per blocking check and assert that check fires.

    A checker that has never failed is not known to work.  Each case copies the
    real artefacts into a scratch directory, corrupts exactly one thing, and
    asserts that the run fails AND that the named check is among the failures.

    A check whose identity has two directions gets two plants, as a list -- G-13
    must fire both when a refused receptor acquires a decoy and when a passing
    receptor's arm goes missing, and one plant can only ever show one of those.
    """
    ok, n = True, 0
    for name, plants in CASES.items():
        for i, (fn, corrupt) in enumerate(plants if isinstance(plants, list)
                                          else [plants]):
            n += 1
            tmp = tempfile.mkdtemp()
            # EVERY regular input, not a hand-written extension list: the day one
            # of these became a .gz, a filter like that silently removed it from
            # the planted copy and the gate then failed on the missing input
            # instead of on the plant.
            want = {f for f in os.listdir(INPUTS)
                    if os.path.isfile(os.path.join(INPUTS, f))
                    and not f.startswith(".")}
            for f in want:
                shutil.copy(os.path.join(INPUTS, f), tmp)
            assert set(os.listdir(tmp)) == want, "staging did not reproduce inputs/"
            before = open(os.path.join(tmp, fn), "rb").read()
            corrupt(os.path.join(tmp, fn))
            p = os.path.join(tmp, fn)
            after = open(p, "rb").read() if os.path.exists(p) else None
            buf, old = io.StringIO(), sys.stdout
            sys.stdout = buf
            try:
                rc = main(["g2_preflight.py"], root=tmp)
            finally:
                sys.stdout = old
                shutil.rmtree(tmp)
            out = buf.getvalue()
            applied = after != before
            fired = re.search(rf"FAIL  {re.escape(name)}\b", out) is not None
            good = rc == 1 and fired and applied
            ok &= good
            tag = f"{name}{chr(97 + i)}" if isinstance(plants, list) else name
            sys.stdout.write(
                f"  {'ok  ' if good else 'MISS'} {tag}: planted a defect in {fn} -> "
                f"rc={rc}, {name} fired={fired}"
                + ("" if applied else ", THE PLANT DID NOT APPLY") + "\n")
    sys.stdout.write(f"\n{n} plants over {len(CASES)} blocking checks proved\n" if ok
                     else "\nSOME CHECKS DID NOT FIRE -- they cannot be trusted\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv))
