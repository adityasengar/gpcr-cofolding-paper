#!/usr/bin/env python3
"""Gate on the decoy rule -- DRULE deliverable 3.

    python3 redo/gates/drule.py
    python3 redo/gates/drule.py --selftest

The project's rule is that a missing input must never be a QUIET skip.  A
deliverable that has not been produced yet is reported as NOT BUILT, in the output,
every run.  An input that has disappeared is a failure.

D-1 .. D-6 cover the target mapping and the candidate pool (deliverables 0 and 1).
D-7 .. D-14 cover the selection (deliverable 2, `redo/build/drule_select.py`) and
are written against the three ways this particular rule can go quietly wrong:

  * a receptor whose eligibility cannot be established acquires decoys anyway
    because "no exclusion rows" reads as "nothing is excluded" (D-8, the B1B1U5
    trap -- it has no ChEMBL target, so the pool holds NO exclusion rows for it and
    a naive implementation hands it the LARGEST accepted set on the panel);
  * a number is frozen into a CSV cell and then drifts away from the ligand table
    that produced it -- §5.3 requires the report be REGENERATED, and MAP §2.4
    records the frozen campaign's ADRB2 decoy notes still naming a ligand replaced
    on 2026-09-04 with nothing noticing.  D-12 recomputes all eight axes and the
    Tanimoto maximum for every accepted decoy from SMILES and refuses a mismatch;
  * a candidate disappears between the pool and the two output tables, which would
    make the rejection record -- the thing that makes the rule auditable at all --
    incomplete without changing any total anybody reads (D-14).
"""

import csv
import hashlib
import io
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, BUILD  # noqa: E402

sys.path.insert(0, BUILD)
import drule_select as DS  # noqa: E402

# ---------------------------------------------------------------------------
# THE FREEZE.  D-2026-09-12-g (the rule's parameters) and -h (its outcome).
#
# What "locked" means in this directory: a constant that a gate asserts and that
# fails when it changes.  A FROZEN banner with nothing executable behind it is the
# defect, not the freeze -- layout.py carried a docstring claiming every check was
# proved by planting with no harness in the file until today, and g0_preflight's
# harness was dead for a day while three documents said otherwise.  So every number
# below is compared against a recomputation, and every one is proved by planting the
# change it exists to catch.
#
# The TWO SET-HASHES are the load-bearing entries.  Every count here survives a
# re-run that silently draws a different molecule for one receptor; the hashes do
# not.  They are sha256 over the "|"-joined SORTED values, so they are invariant to
# row order and to which receptor a molecule was drawn for -- which is the point:
# they pin the molecular identity of the arm and nothing else.
#
# MDE is NOT in here.  It is recomputed from the observed cluster count and then
# compared, so that changing the accepted set moves the assertion instead of
# leaving a stale 0.367 behind.
# ---------------------------------------------------------------------------
FROZEN = {
    # -- D-2026-09-12-g, the rule's enacted parameters
    "clogp_window": "absolute:1.0",
    "diversity_max": "0.3",
    "k_requested": "3",
    "chembl_release": "ChEMBL_37",
    "pool_scope": "within_panel",
    "draw_seed": "20260912",
    "chembl_sha256":
        "33c203740555f96067710cdfc1c3c55d890660e5908ec5cbf5817492c290d281",
    # -- D-2026-09-12-h, the outcome
    "n_accepted_receptors": 11,
    "accepted_receptors": ("5HT5A", "ACM4", "ADRB1", "CCKAR", "CNR2", "DRD3",
                           "GHSR", "LT4R1", "OPRD", "OPSD", "S1PR1"),
    "n_accepted_clusters": 11,
    "n_refused_receptors": 5,
    "refused_receptors": ("AA1R", "AA2AR", "B1B1U5", "HRH3", "LPAR1"),
    # frozen SEPARATELY from the refused set, because flattening B1B1U5's
    # refusal into the other four is the specific error this guards
    "refusal_classes": {
        "B1B1U5": "eligibility_unestablishable_no_chembl_target",
        "AA1R": "fewer_than_k_accepted",
        "AA2AR": "fewer_than_k_accepted",
        "HRH3": "fewer_than_k_accepted",
        "LPAR1": "fewer_than_k_accepted",
    },
    "n_accepted_molecules": 33,
    "chembl_id_set_sha256":
        "9d363f1f600796b5ef92b07c5457bb4e2a4f5acd0623c64fa89a6d318e84114b",
    "inchikey_set_sha256":
        "a694022dc0b56c96d199cf2eddb048ecadd963666778b0c7ab9bbfd3416c4fe1",
    # ADDED here, not handed down, because the two set-hashes above have a hole:
    # being over the SORTED values they are invariant to which receptor drew which
    # molecule, so PERMUTING the assignment -- the same 33 molecules against the
    # wrong references -- leaves both of them matching.  Measured, not assumed:
    # swapping one DRD3 decoy with one GHSR decoy keeps both digests and neither
    # molecule acquires an exclusion row, so D-9 stays quiet too.  This third
    # digest, over the sorted "slug:chembl_id" PAIRS, is what pins the assignment.
    "assignment_sha256":
        "e60eb91c8b6ea48c2f654d02dc1ac1031f6654a914cdb9114995aa4f55a04eff",
    # -- the dispatch consequence in g2_systems.csv
    #
    # CELL counts are frozen; PREDICTION totals deliberately are NOT.  The cell
    # counts are a property of the selection -- 11 receptors x 3 partner levels
    # READY, 5 x 3 BLOCKED -- and change only if the selection changes, which is
    # what this freeze is for.  The prediction totals are not: 132 of the 396
    # pooled predictions are `G6fd(option)` at R7_full, which sits behind an OPEN
    # pi_choice on the cognate rung, and n = 10/50 is a separate open decision on
    # the pooled claim.  Freezing them would make the freeze fire on decisions
    # Aditya is entitled to take -- friction dressed as safety.  g2_preflight's
    # G-10 already re-derives the totals from backbones x n, which is the right
    # place for them.  Recorded so this is legible as a choice, not an omission.
    "ready_cells": 33,
    "blocked_cells": 15,
    # the pre-registered bar the arm runs below, for the MDE comparison
    "prereg_k": 12,
    "mde_3dp": "0.367",
    "mde_loss_pct_1dp": "4.4",
}

FREEZE_NOTE = (
    "FROZEN by D-2026-09-12-g/h. Re-running redo/build/drule_select.py is NOT the "
    "fix -- it will reproduce this value, and if it does not, the inputs or the rule "
    "have moved underneath a locked decision. The fix is to change the DECISION "
    "first (redo/spec/DECISIONS.md), then FROZEN in redo/gates/drule.py, then "
    "regenerate. This gate is not broken when it says this.")

TARGETS = "drule_targets.tsv"
POOL = "drule_pool_molecules.tsv"
EXCL = "drule_pool_exclusions.tsv"
PANEL = "g1_receptors.tsv"
SEL = "drule_selected.tsv"
# gzipped from 2026-09-12 (86 MB -> 7.2 MB); read through drule_select.open_rejections
REJ = "drule_rejections.tsv.gz"
G2 = "g2_systems.csv"


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

    selection_checks(root, chk, blocking)
    return report(blocking, passed, pending)


# ==========================================================================
# deliverable 2 -- the selection, the rejections, and the traps
# ==========================================================================
def selection_checks(root, chk, blocking):
    spath = os.path.join(root, SEL)
    rpath = os.path.join(root, REJ)
    # A missing input FAILS.  Both files are generated by drule_select.py and
    # hashed in inputs/MANIFEST.tsv, so absence is a defect, not a "not built yet".
    for name, p in ((SEL, spath), (REJ, rpath)):
        if not os.path.exists(p):
            chk(f"D-7  {name} is present", False,
                f"{name} is ABSENT -- run redo/build/drule_select.py.  A check that "
                f"quietly does nothing when its input is missing is the defect it "
                f"exists to catch")
            return
    sel = tsv(SEL, root)
    tg = {r["receptor_slug"]: r for r in tsv(TARGETS, root)}

    # the scope is re-derived from g2_systems.csv, never taken from the output
    try:
        scope, _ = DS.load_scope(root)
    except SystemExit as e:
        chk("D-7  the decoy arm's scope is recoverable from g2_systems.csv", False,
            str(e))
        return

    # -- D-7  every receptor in scope is present, at k decoys or named as
    #         unavailable AT ZERO.  Never dropped, never "taken anyway".
    by = {}
    for r in sel:
        by.setdefault(r["receptor_slug"], []).append(r)
    missing = sorted(set(scope) - set(by))
    wrong = []
    for s in scope:
        rows = by.get(s, [])
        acc = [r for r in rows if r["decoy_status"] == "accepted"]
        una = [r for r in rows if r["decoy_status"] == "decoy-unavailable"]
        if acc and len(acc) != DS.K_DECOYS:
            wrong.append(f"{s}={len(acc)} accepted, k={DS.K_DECOYS}")
        if una and (len(una) != 1 or acc):
            wrong.append(f"{s}: {len(una)} unavailable rows beside {len(acc)} accepted")
        if una and una[0]["candidate_chembl_id"]:
            wrong.append(f"{s}: a decoy-unavailable row carries a molecule")
        if una and not una[0]["reason"].strip():
            wrong.append(f"{s}: decoy-unavailable with no stated ground")
        if not acc and not una:
            wrong.append(f"{s}: present with neither decoys nor a refusal")
    extra = sorted(set(by) - set(scope))
    chk("D-7  every receptor in the decoy arm carries exactly k decoys or a NAMED "
        "refusal at zero", not missing and not wrong and not extra,
        "; ".join(missing + wrong + extra) if (missing or wrong or extra) else
        f"{len(scope)} receptors, "
        f"{len([s for s in scope if any(r['decoy_status'] == 'accepted' for r in by[s])])}"
        f" with {DS.K_DECOYS} decoys, "
        f"{len([s for s in scope if by[s][0]['decoy_status'] == 'decoy-unavailable'])}"
        f" decoy-unavailable")

    # -- D-8  THE TRAP.  A receptor with no resolved ChEMBL target has no
    #         exclusion rows, so "not excluded" is not "eligible" -- eligibility is
    #         unestablishable and it must be REFUSED on that ground.
    unres = sorted(s for s in scope if not tg.get(s, {}).get("chembl_target_id"))
    leaked = [s for s in unres
              if any(r["decoy_status"] == "accepted" for r in by.get(s, []))]
    ungrounded = [s for s in unres
                  if not any("unestablishable" in r["reason"] for r in by.get(s, []))]
    chk("D-8  a receptor with NO resolved ChEMBL target acquires no decoy, and is "
        "refused on the ground that eligibility is unestablishable",
        not leaked and not ungrounded,
        f"accepted decoys at {leaked}; refusal not grounded for {ungrounded}"
        if (leaked or ungrounded) else
        f"{unres or 'none'} refused, eligibility unestablishable (no exclusion rows "
        f"exist for it, which is NOT the same as nothing being excluded)")

    acc_rows = [r for r in sel if r["decoy_status"] == "accepted"]

    # -- D-9  every accepted decoy really is eligible -----------------------
    ids = {r["candidate_chembl_id"] for r in tsv(POOL, root)}
    excl = {}
    with open(os.path.join(root, EXCL)) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            excl.setdefault(r["receptor_slug"], set()).add(r["candidate_chembl_id"])
    notin = [f"{r['receptor_slug']}/{r['candidate_chembl_id']}"
             for r in acc_rows if r["candidate_chembl_id"] not in ids]
    banned = [f"{r['receptor_slug']}/{r['candidate_chembl_id']}"
              for r in acc_rows
              if r["candidate_chembl_id"] in excl.get(r["receptor_slug"], ())]
    chk("D-9  every accepted decoy is in the pool AND carries no exclusion row for "
        "its own receptor", not notin and not banned,
        f"absent from the pool: {notin[:4]}; excluded yet accepted: {banned[:4]}"
        if (notin or banned) else f"{len(acc_rows)} accepted decoys, all eligible")

    # -- D-10  the seeded draw is recorded, and recomputes ------------------
    noseed = [r["receptor_slug"] for r in acc_rows
              if not r["draw_seed"].strip() or not r["receptor_seed"].strip()]
    wrongseed = [r["receptor_slug"] for r in acc_rows
                 if r["receptor_seed"].strip()
                 and r["receptor_seed"] != str(DS.receptor_seed(r["receptor_slug"]))]
    chk("D-10  every drawn decoy records the seed, and the seed recomputes from the "
        "receptor", not noseed and not wrongseed,
        f"no seed: {sorted(set(noseed))[:4]}; seed does not recompute: "
        f"{sorted(set(wrongseed))[:4]}" if (noseed or wrongseed) else
        f"draw_seed {sorted({r['draw_seed'] for r in acc_rows})}, "
        f"receptor seeds reproduce for all {len(acc_rows)} rows")

    # -- D-11 / D-14  the rejection record ----------------------------------
    # One streaming pass: vocabulary, the deterministic first axis, no overlap with
    # the accepted set, and the conservation law accepted + rejected == eligible.
    vocab = set(DS.AXES)
    badaxis = badfirst = 0
    per_rec = {}
    accepted_pairs = {(r["receptor_slug"], r["candidate_chembl_id"])
                      for r in acc_rows}
    overlap = 0
    with DS.open_rejections(rpath) as fh:
        head = fh.readline().rstrip("\n").split("\t")
        if head != ["receptor_slug", "candidate_chembl_id", "first_failed_axis",
                    "failed_axes", "n_failed_axes"]:
            chk("D-11  the rejection table has the declared columns", False,
                f"header is {head}")
            return
        for line in fh:
            slug, cid, first, axes_, n = line.rstrip("\n").split("\t")
            fa = axes_.split("|")
            if not fa or set(fa) - vocab or first not in vocab or str(len(fa)) != n:
                badaxis += 1
            elif first != min(fa, key=DS.AXES.index):
                badfirst += 1
            if (slug, cid) in accepted_pairs:
                overlap += 1
            per_rec[slug] = per_rec.get(slug, 0) + 1
    chk("D-11  every rejection names axes from the declared vocabulary, a "
        "deterministic first axis, and is not also accepted",
        not badaxis and not badfirst and not overlap,
        f"{badaxis} with an unknown/inconsistent axis, {badfirst} whose "
        f"first_failed_axis is not first in {DS.AXES}, {overlap} accepted AND rejected"
        if (badaxis or badfirst or overlap) else
        f"{sum(per_rec.values()):,} rejections over {len(per_rec)} receptors, "
        f"vocabulary {len(vocab)} axes, no overlap with the accepted set")

    # -- D-12  §5.3: the report is REGENERATED, never frozen into a CSV cell.
    # Recompute all eight axes and the Tanimoto maximum from SMILES and refuse any
    # accepted decoy that no longer passes, or whose stored value has drifted.
    cbad, abad = DS.validate_charge_rule(verbose=False)
    chk("D-13  the pH 7.4 protonation rule validates, and the six aminergic full "
        "agonists come out +1", not cbad and not abad,
        f"{len(cbad)} molecule(s) off: {[c[0] for c in cbad][:4]}; aminergic: {abad}"
        if (cbad or abad) else
        f"{len(DS.CHARGE_VALIDATION)} molecules at the expected charge, including "
        f"5HT5A ACM4 DRD3 OPRD ADRB1 HRH3 at +1")

    # -- D-15  amendments A and B are RECORDED, one setting for the whole run.
    # A row that does not say which window and which cap produced it cannot be
    # recomputed, and D-12 below would be checking against the module's current
    # defaults rather than against what was enacted -- which is the CSV-cell drift
    # MAP §2.4 describes, one level up.
    wins = {r.get("clogp_window", "") for r in sel}
    caps = {r.get("diversity_max", "") for r in sel}
    try:
        enacted_w = DS.parse_window(sorted(wins)[0]) if wins and all(wins) else None
        enacted_c = float(sorted(caps)[0]) if caps and all(caps) else None
    except Exception:                                            # noqa: BLE001
        enacted_w = enacted_c = None
    chk("D-15  every row records the enacted cLogP window and diversity cap, and the "
        "run used ONE of each",
        len(wins) == 1 and len(caps) == 1 and all(wins) and all(caps)
        and enacted_w is not None and enacted_c is not None,
        f"cLogP windows {sorted(wins)}, diversity caps {sorted(caps)}"
        if (len(wins) != 1 or len(caps) != 1 or not all(wins) or not all(caps)) else
        f"cLogP window {DS.wname(enacted_w)}, within-draw Tanimoto cap {enacted_c} "
        f"(§5.3 amendments A and B, 2026-09-12)")
    if enacted_w is None or enacted_c is None:
        return

    try:
        curated, census = DS.load_ligands(root)
        byc = {}
        for r in tg.values():
            byc.setdefault(r["cluster"], []).append(r["receptor_slug"])
        from rdkit import DataStructs
        drift = []
        for r in acc_rows:
            ref = DS.axes(r["ref_smiles"])
            a = DS.axes(r["smiles"])
            if ref is None or a is None:
                drift.append(f"{r['receptor_slug']}/{r['candidate_chembl_id']}: "
                             f"SMILES will not parse")
                continue
            fps = [x["_fp"] for x in
                   (DS.axes(t[2]) for t in DS.real_ligands(
                       byc.get(r["cluster"], [r["receptor_slug"]]), curated, census))
                   if x]
            mt = max(DataStructs.BulkTanimotoSimilarity(a["_fp"], fps)) if fps else 0.0
            # recomputed against the window the ROW records, not the module default
            f = DS.failed_axes(a, ref, DS.window(ref, enacted_w), mt)
            if f:
                drift.append(f"{r['receptor_slug']}/{r['candidate_chembl_id']}: "
                             f"recomputed, now fails {f}")
            elif abs(mt - float(r["max_tanimoto"])) > 1e-3:
                drift.append(f"{r['receptor_slug']}/{r['candidate_chembl_id']}: "
                             f"stored T={r['max_tanimoto']} recomputes to {mt:.4f}")
        chk("D-12  every accepted decoy still passes all eight axes and the Tanimoto "
            "screen on RECOMPUTATION from SMILES", not drift,
            "; ".join(drift[:3]) if drift else
            f"{len(acc_rows)} decoys recomputed against the CURRENT ligand tables at "
            f"{DS.wname(enacted_w)}, no drift (MAP §2.4: the frozen campaign's notes "
            f"drifted unnoticed)")

        # -- D-16  amendment B, enforced on the delivered draws.  §5.3 caps
        # similarity to the real ligands and says nothing about similarity AMONG the
        # k decoys; the first run drew OPSD two near-identical GPR52 ligands at
        # pairwise T = 0.641, which is one molecule wearing three hats.  Recomputed
        # from SMILES here, never read from the stored cell.
        too_close, worst = [], 0.0
        for slug, rows in by.items():
            picks = [r for r in rows if r["decoy_status"] == "accepted"]
            if not picks:
                continue          # decoy-unavailable: D-7 owns that shape, not this
            fps = {r["candidate_chembl_id"]: DS.axes(r["smiles"]) for r in picks}
            if any(v is None for v in fps.values()):
                continue
            ids = sorted(fps)
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    t = DataStructs.TanimotoSimilarity(fps[ids[i]]["_fp"],
                                                       fps[ids[j]]["_fp"])
                    worst = max(worst, t)
                    if t >= enacted_c:
                        too_close.append(f"{slug}: {ids[i]}/{ids[j]} T={t:.3f}")
            stored = {r.get("max_intra_draw_tanimoto", "") for r in picks}
            if len(stored) != 1 or not all(stored):
                too_close.append(f"{slug}: max_intra_draw_tanimoto not recorded "
                                 f"consistently on the draw")
        chk("D-16  the k decoys of a receptor are dissimilar to EACH OTHER, not only "
            "to the real ligands", not too_close,
            "; ".join(too_close[:3]) if too_close else
            f"every within-draw pair recomputes below the cap {enacted_c}; worst on "
            f"the panel is T = {worst:.3f}")
    except SystemExit as e:
        chk("D-12  every accepted decoy still passes on RECOMPUTATION", False, str(e))

    # -- D-14  nothing vanishes between the pool and the two tables ---------
    lost = []
    for s in scope:
        if not tg.get(s, {}).get("chembl_target_id"):
            continue                       # D-8's case: no eligible set to conserve
        rows = by.get(s, [])
        if not rows:
            continue          # D-7 owns "a receptor with no row at all"; do not
            #                   crash here and take the rest of the gate with us
        n_elig = int(rows[0]["n_eligible"] or 0)
        n_acc = int(rows[0]["n_accepted"] or 0)
        if n_elig != n_acc + per_rec.get(s, 0):
            lost.append(f"{s}: {n_elig:,} eligible != {n_acc:,} accepted + "
                        f"{per_rec.get(s, 0):,} rejected")
    chk("D-14  accepted + rejected == eligible, for every receptor: no candidate is "
        "silently dropped", not lost, "; ".join(lost[:4]) if lost else
        f"conserved over {len([s for s in scope if tg.get(s, {}).get('chembl_target_id')])}"
        f" receptors with a resolved target")

    freeze_checks(root, chk, sel, acc_rows, by, want_ref=want_ref_of(sel))


def want_ref_of(sel):
    """receptor -> its recorded refusal, with the class DERIVED from n_eligible.

    Same derivation g2_systems.py uses, and for the same reason: a refused receptor
    with ZERO eligible candidates was refused because eligibility could not be
    established at all, one with a nonzero eligible set because too few of them
    passed.  Reading the class out of the prose would make the freeze a check on a
    sentence.
    """
    out = {}
    for r in sel:
        if r["decoy_status"] == "decoy-unavailable":
            n = int(r["n_eligible"] or 0)
            out[r["receptor_slug"]] = dict(
                reason=r["reason"], n_eligible=n,
                cls=("eligibility_unestablishable_no_chembl_target" if n == 0
                     else "fewer_than_k_accepted"))
    return out


def set_sha256(values):
    """sha256 over the "|"-joined SORTED values.

    Sorted, so the digest is invariant to row order and to which receptor a molecule
    was drawn for -- it pins the arm's molecular identity and nothing else.  That is
    what makes it catch the one failure no count can: a re-run that swaps one decoy
    for another eligible candidate.
    """
    return hashlib.sha256("|".join(sorted(values)).encode()).hexdigest()


# ==========================================================================
# THE FREEZE -- D-17 .. D-24
# ==========================================================================
def freeze_checks(root, chk, sel, acc_rows, by, want_ref):
    def frz(label, ok, got, want, held=""):
        """Report a frozen constant.  `held` is what to say when it still holds."""
        chk(label, ok, held if ok else
            f"got {got}, D-2026-09-12 froze {want}.  {FREEZE_NOTE}")

    # -- D-17  the rule's enacted parameters --------------------------------
    params, bad = {}, []
    for col in ("clogp_window", "diversity_max", "k_requested", "chembl_release",
                "pool_scope", "draw_seed"):
        vals = sorted({r[col] for r in sel})
        params[col] = vals
        if vals != [FROZEN[col]]:
            bad.append(f"{col}={vals} not [{FROZEN[col]!r}]")
    frz("D-17  the rule's parameters are the frozen ones, on every row",
        not bad, "; ".join(bad),
        f"clogp_window={FROZEN['clogp_window']}, "
        f"diversity_max={FROZEN['diversity_max']}, k={FROZEN['k_requested']}, "
        f"{FROZEN['chembl_release']}/{FROZEN['pool_scope']}, "
        f"draw_seed={FROZEN['draw_seed']} (D-2026-09-12-g)",
        held=f"clogp_window {FROZEN['clogp_window']}, diversity_max "
             f"{FROZEN['diversity_max']}, k {FROZEN['k_requested']}, draw_seed "
             f"{FROZEN['draw_seed']}, {FROZEN['chembl_release']} / "
             f"{FROZEN['pool_scope']}")

    # -- D-18  the pool digest ----------------------------------------------
    # The release NAME is not the release.  DRULE_CHEMBL_SCOPE.md pins by version
    # AND download checksum, because an unpinned pull is paper_af3's ColabFold
    # problem in another costume; freezing only the name would leave exactly that
    # hole open.
    digests = sorted({r["chembl_sha256"] for r in tsv(POOL, root)})
    frz("D-18  the pool came from the frozen ChEMBL download, by DIGEST not by name",
        digests == [FROZEN["chembl_sha256"]],
        f"{[d[:16] + '...' for d in digests]}",
        f"[{FROZEN['chembl_sha256'][:16]}...] (D-2026-09-12-g)")

    # -- D-19  the accepted and refused SETS --------------------------------
    got_acc = tuple(sorted({r["receptor_slug"] for r in acc_rows}))
    got_ref = tuple(sorted(want_ref))
    got_clu = len({r["cluster"] for r in acc_rows})
    ok = (got_acc == tuple(sorted(FROZEN["accepted_receptors"]))
          and len(got_acc) == FROZEN["n_accepted_receptors"]
          and got_ref == tuple(sorted(FROZEN["refused_receptors"]))
          and len(got_ref) == FROZEN["n_refused_receptors"]
          and got_clu == FROZEN["n_accepted_clusters"])
    frz("D-19  exactly 11 receptors / 11 clusters accepted and 5 refused, and "
        "exactly WHICH", ok,
        f"{len(got_acc)} accepted {list(got_acc)} in {got_clu} clusters, "
        f"{len(got_ref)} refused {list(got_ref)}",
        f"{FROZEN['n_accepted_receptors']} accepted "
        f"{list(FROZEN['accepted_receptors'])} in "
        f"{FROZEN['n_accepted_clusters']} clusters, "
        f"{FROZEN['n_refused_receptors']} refused "
        f"{list(FROZEN['refused_receptors'])} (D-2026-09-12-h)")

    # -- D-20  the refusal CLASSES, frozen per receptor ---------------------
    got_cls = {s: w["cls"] for s, w in want_ref.items()}
    frz("D-20  B1B1U5 is refused because eligibility is UNESTABLISHABLE and the "
        "other four because too few candidates passed -- separately frozen",
        got_cls == FROZEN["refusal_classes"],
        f"{got_cls}",
        f"{FROZEN['refusal_classes']} (D-2026-09-12-h).  These are different facts: "
        f"B1B1U5 has no ChEMBL target, so the pool holds NO exclusion rows for it "
        f"and its eligibility was never establishable; the other four had 111k-120k "
        f"eligible candidates and too few passed the eight axes.  Flattening them "
        f"into one 'no decoy' is the error this check exists for")

    # -- D-21  the molecular identity of the arm ----------------------------
    ids = [r["candidate_chembl_id"] for r in acc_rows]
    iks = [r["inchikey"] for r in acc_rows]
    reused = sorted({i for i in ids if ids.count(i) > 1})
    ok = (len(ids) == FROZEN["n_accepted_molecules"]
          and len(set(ids)) == FROZEN["n_accepted_molecules"] and not reused)
    frz("D-21  33 accepted decoys, and no molecule is reused across receptors", ok,
        f"{len(ids)} rows, {len(set(ids))} distinct ids"
        + (f", reused: {reused}" if reused else ""),
        f"{FROZEN['n_accepted_molecules']} rows, all distinct (D-2026-09-12-h).  A "
        f"molecule serving as the decoy for two receptors makes 'decoy' and 'that "
        f"molecule' partly the same term across cells, which is the collision k=3 "
        f"exists to break")

    # -- D-22  THE SET-HASHES.  The load-bearing pair. ----------------------
    # Every count above survives a re-run that swaps one decoy for another eligible
    # candidate of the same receptor: 33 rows, 33 distinct ids, 11 receptors, 11
    # clusters, all still true.  These two do not survive it.
    got_h, got_k = set_sha256(ids), set_sha256(iks)
    frz("D-22  the SET of 33 ChEMBL ids hashes to the frozen digest",
        got_h == FROZEN["chembl_id_set_sha256"],
        f"{got_h}", f"{FROZEN['chembl_id_set_sha256']} (D-2026-09-12-h).  sha256 of "
        f"the '|'-joined SORTED candidate_chembl_id values, so it is invariant to "
        f"row order and to which receptor drew which molecule.  If this is the only "
        f"failing check, the arm has silently drawn a DIFFERENT molecule -- which no "
        f"count in this gate can see")
    frz("D-23  the SET of 33 InChIKeys hashes to the frozen digest",
        got_k == FROZEN["inchikey_set_sha256"],
        f"{got_k}", f"{FROZEN['inchikey_set_sha256']} (D-2026-09-12-h).  The same "
        f"pin on the CHEMISTRY rather than on the accession: a ChEMBL id can be "
        f"merged or withdrawn upstream, and an InChIKey cannot")

    # -- D-26  the ASSIGNMENT, not just the set -----------------------------
    got_a = set_sha256(f"{r['receptor_slug']}:{r['candidate_chembl_id']}"
                       for r in acc_rows)
    frz("D-26  each of the 33 decoys is frozen TO ITS RECEPTOR, not merely to the "
        "panel", got_a == FROZEN["assignment_sha256"],
        f"{got_a}", f"{FROZEN['assignment_sha256']} (added 2026-09-12).  sha256 of "
        f"the sorted 'slug:chembl_id' pairs.  D-22 and D-23 are over the sorted "
        f"VALUES, so they are blind to a permutation of the assignment -- the same "
        f"33 molecules scored against the wrong references keeps both of those "
        f"digests. This is the check that sees it")

    # -- D-24  MDE, RECOMPUTED from the observed clusters -------------------
    # Never a hardcoded 0.367.  Computed from what is in the file and then compared,
    # so that changing the accepted set MOVES the assertion rather than leaving a
    # stale number standing next to new data.
    k = len({r["cluster"] for r in acc_rows})
    mde = 1.218 / k ** 0.5 if k else float("inf")
    target = 1.218 / FROZEN["prereg_k"] ** 0.5
    loss = 100.0 * (mde / target - 1.0)
    ok = (f"{mde:.3f}" == FROZEN["mde_3dp"]
          and f"{loss:.1f}" == FROZEN["mde_loss_pct_1dp"])
    frz("D-24  the MDE recomputed from the observed cluster count is the frozen one",
        ok,
        f"k={k} -> MDE 1.218/sqrt({k}) = {mde:.3f}, {loss:+.1f}% against "
        f"k={FROZEN['prereg_k']}",
        f"MDE {FROZEN['mde_3dp']} and +{FROZEN['mde_loss_pct_1dp']}% "
        f"(D-2026-09-12-h).  This is RECOMPUTED, not stored: if the accepted set "
        f"changes, this check moves with it and fails, which is how the decision "
        f"record and the data are kept from drifting apart",
        held=f"k={k} clusters -> 1.218/sqrt({k}) = {mde:.3f} against "
             f"{target:.3f} at the pre-registered k={FROZEN['prereg_k']}, "
             f"+{loss:.1f}% -- recomputed here, not read from a cell")

    # -- D-25  the dispatch consequence in g2_systems.csv -------------------
    # The freeze has to reach the table that actually dispatches, or it freezes a
    # selection nobody runs.  g2_preflight re-derives the identity of every decoy
    # cell from drule_selected.tsv; what it does NOT pin is the totals, so they are
    # pinned here, where the decision lives.
    g2p = os.path.join(root, G2)
    if not os.path.exists(g2p):
        chk("D-25  the frozen selection reaches g2_systems.csv at the frozen totals",
            False, f"{G2} is ABSENT -- run redo/build/g2_systems.py")
        return
    with open(g2p) as fh:
        g2 = [r for r in csv.DictReader(fh) if r["ligand"] == "decoy_lig"]
    ready = [r for r in g2 if r["dispatch_status"] == "READY"]
    blk = [r for r in g2 if r["dispatch_status"] != "READY"]
    pooled = sum(int(r["predictions_pooled"]) for r in ready)
    percell = sum(int(r["predictions_percell"]) for r in ready)
    ok = (len(ready) == FROZEN["ready_cells"]
          and len(blk) == FROZEN["blocked_cells"])
    frz("D-25  the frozen selection reaches g2_systems.csv at the frozen cell counts",
        ok,
        f"{len(ready)} READY / {len(blk)} BLOCKED cells "
        f"(totals {pooled} pooled / {percell} per-cell, NOT frozen -- "
        f"the R7_full pi_choice and n=10/50 are open decisions)",
        f"{FROZEN['ready_cells']} READY / {FROZEN['blocked_cells']} BLOCKED "
        f"decoy cells (D-2026-09-12-h)",
        held=f"{len(ready)} READY / {len(blk)} BLOCKED decoy cells; prediction "
             f"totals are re-derived by g2_preflight G-10, not frozen here")


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


def _sub_rejection_line(path, n, old, new):
    """Rewrite ONE row of the rejection table, through the same gzip the gate reads.

    Streaming, because the table is 1.7 M rows; and gzip-aware, because it is stored
    compressed from 2026-09-12 and a plant that cannot open its own target does not
    plant anything.
    """
    rows = []
    with DS.open_rejections(path) as src:
        src.readline()                                    # the header is not a row
        for i, line in enumerate(src):
            f = line.rstrip("\n").split("\t")
            if i == n:
                f = [x.replace(old, new) for x in f]
            rows.append(f)
    DS.write_rejections(rows, path)


def _accepted_row(path, col, val, slug=None):
    """Set one column on the first `accepted` row (of receptor `slug`, if given)."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    for r in rows:
        if r["decoy_status"] == "accepted" and (slug is None
                                                or r["receptor_slug"] == slug):
            r[col] = val
            break
    else:
        raise AssertionError(f"no accepted row to plant on in {path}")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _drop_one_decoy(path, slug):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    out, dropped = [], False
    for r in rows:
        if not dropped and r["receptor_slug"] == slug and r["decoy_status"] == "accepted":
            dropped = True
            continue
        out.append(r)
    assert dropped, f"{slug} has no accepted decoy to drop"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(out)


def _grant_decoy_to_unresolved(path):
    """THE TRAP, planted.  Give the receptor with no ChEMBL target a decoy -- which
    is exactly what a naive implementation does, because the pool holds no exclusion
    rows for it and an empty exclusion set reads as universal eligibility."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    donor = next(r for r in rows if r["decoy_status"] == "accepted")
    hit = False
    for r in rows:
        if r["decoy_status"] == "decoy-unavailable" and "unestablishable" in r["reason"]:
            for k in ("decoy_status", "reason", "candidate_chembl_id",
                      "candidate_name", "smiles", "max_tanimoto"):
                r[k] = donor[k] if k != "reason" else ""
            r["decoy_status"] = "accepted"
            hit = True
            break
    assert hit, "no receptor is refused for unestablishable eligibility"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _revert_to_getformalcharge():
    """The regression this module exists to prevent: MAP §1.4 / §2.3 -- charge taken
    as written in the SMILES rather than at pH 7.4."""
    from rdkit import Chem
    keep = DS.charge_ph74
    DS.charge_ph74 = lambda m, explain=False: (
        (Chem.GetFormalCharge(m), [], [], 0) if explain else Chem.GetFormalCharge(m))

    def undo():
        DS.charge_ph74 = keep
    return undo


# (check, what is planted, the ONE input file it touches (None = a code plant),
#  the mutation).  A plant that touches no file still has to be proved, so D-13 is
#  planted in code -- reverting the charge rule to the frozen campaign's.
def _col_csv(path, row_match, col, val):
    """_col, for a comma-delimited file.  g2_systems.csv is the only one here."""
    rows = list(csv.DictReader(open(path)))
    cols = list(rows[0].keys())
    for r in rows:
        if row_match is None or all(r[k] == v for k, v in row_match.items()):
            r[col] = val
            break
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _drop_receptor_decoys(path, slug):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    out = [r for r in rows if not (r["receptor_slug"] == slug
                                   and r["decoy_status"] == "accepted")]
    assert len(out) < len(rows), f"{slug} has no accepted decoys to drop"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(out)


def _accepted_rows_all(path, slug, col, val):
    """Set one column on EVERY accepted row of `slug`.

    `_accepted_row` touches only the first match, which for a per-receptor property
    like `cluster` produces a plant that applies (the bytes change) and is still
    inert (the receptor keeps its old cluster through its other two rows, so the
    cluster COUNT never moves).  A plant that applies but changes nothing observable
    is the same failure as one that does not apply -- it scores `MISS` here, which is
    how this one was found.
    """
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    n = 0
    for r in rows:
        if r["receptor_slug"] == slug and r["decoy_status"] == "accepted":
            r[col] = val
            n += 1
    assert n, f"no accepted rows for {slug}"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _alt_candidate(d, slug):
    """A molecule the rule ACCEPTED for `slug` and did not draw.

    Derived, not picked: it is in the pool, carries no exclusion row for `slug`,
    appears in no rejection row for `slug`, and is not among the 33 drawn.  By
    D-14's conservation law (accepted + rejected == eligible) that is exactly the
    accepted-but-undrawn set.  So substituting it is a substitution the rule itself
    would have permitted -- which is what makes it the right plant for a set-hash:
    every count in the gate stays true and only the digest moves.
    """
    drawn = {r["candidate_chembl_id"] for r in tsv(SEL, d)
             if r["decoy_status"] == "accepted"}
    excl = set()
    with open(os.path.join(d, EXCL)) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["receptor_slug"] == slug:
                excl.add(r["candidate_chembl_id"])
    rej = set()
    with DS.open_rejections(os.path.join(d, REJ)) as fh:
        fh.readline()
        for line in fh:
            f = line.split("\t", 2)
            if f[0] == slug:
                rej.add(f[1])
    for r in tsv(POOL, d):
        cid = r["candidate_chembl_id"]
        if cid in drawn or cid in excl or cid in rej:
            continue
        a = DS.axes(r["smiles"])
        if a is not None:
            return cid, a["_inchikey"]
    raise AssertionError(f"no accepted-but-undrawn candidate found for {slug}")


def _swap_one_id(d):
    """THE SET-HASH PLANT.  Swap one drawn decoy's ChEMBL id for an undrawn one.

    Leaves intact: 33 rows, 33 DISTINCT ids, 11 accepted receptors, 11 clusters,
    5 refused, every refusal class, every rule parameter, the pool digest, the
    recomputed MDE, both g2_systems.csv totals, and the InChIKey set-hash.  D-22 is
    the only check in the gate that can see it.
    """
    cid, _ik = _alt_candidate(d, "OPSD")
    p = os.path.join(d, SEL)
    _accepted_row(p, "candidate_chembl_id", cid, slug="OPSD")


def _swap_one_inchikey(d):
    """THE OTHER SET-HASH PLANT.  The chemistry moves under a stable accession.

    Leaves intact: everything above, AND the ChEMBL id set-hash -- the accession
    is untouched, so nothing that keys on `candidate_chembl_id` notices.  D-23 is
    the only check in the gate that can see it.
    """
    _cid, ik = _alt_candidate(d, "OPSD")
    _accepted_row(os.path.join(d, SEL), "inchikey", ik, slug="OPSD")


def _permute_assignment(d):
    """THE PLANT THE SET-HASHES CANNOT SEE.  Swap one DRD3 decoy with one GHSR one.

    This is the plant the freeze was first specified with, and it proves the
    opposite of what it looks like: the sorted SET of 33 ChEMBL ids is unchanged, so
    D-22 passes; the sorted set of InChIKeys is unchanged, so D-23 passes; 33 rows,
    33 distinct ids, 11 receptors, 11 clusters, every count intact.  Neither
    molecule carries an exclusion row for its new receptor, so D-9 stays quiet, and
    `smiles` is untouched so D-12 still recomputes clean.  Only D-26 sees it.
    """
    p = os.path.join(d, SEL)
    rows = list(csv.DictReader(open(p), delimiter="\t"))
    cols = list(rows[0].keys())
    a = next(r for r in rows if r["receptor_slug"] == "DRD3"
             and r["decoy_status"] == "accepted")
    b = next(r for r in rows if r["receptor_slug"] == "GHSR"
             and r["decoy_status"] == "accepted")
    a["candidate_chembl_id"], b["candidate_chembl_id"] = (b["candidate_chembl_id"],
                                                          a["candidate_chembl_id"])
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


PLANTS = [
    ("D-1", "delete the target mapping", TARGETS,
     lambda d: os.remove(os.path.join(d, TARGETS))),
    ("D-2", "drop a panel receptor from the mapping", TARGETS,
     lambda d: _drop_row(os.path.join(d, TARGETS), "CCKAR")),
    ("D-3", "blank the slug on the unresolved receptor so it vanishes quietly",
     TARGETS,
     lambda d: _col(os.path.join(d, TARGETS), {"chembl_target_id": ""},
                    "receptor_slug", "")),
    ("D-4", "make one accession map to two targets", TARGETS,
     lambda d: _sub(os.path.join(d, TARGETS), "\t1\tChEMBL_37", "\t2\tChEMBL_37")),
    ("D-5", "strip the reason from an exclusion", EXCL,
     lambda d: _col(os.path.join(d, EXCL), None, "ineligible_because", "")),
    ("D-6", "blank the release on a pool row", POOL,
     lambda d: _col(os.path.join(d, POOL), None, "chembl_release", "")),
    ("D-7", "drop one decoy so a receptor runs at k-1", SEL,
     lambda d: _drop_one_decoy(os.path.join(d, SEL), "OPRD")),
    ("D-8", "hand a decoy to the receptor with no ChEMBL target", SEL,
     lambda d: _grant_decoy_to_unresolved(os.path.join(d, SEL))),
    ("D-9", "accept a decoy that carries an exclusion row for its own receptor", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "candidate_chembl_id",
                             _first_excluded(d))),
    ("D-10", "blank the seed on a drawn decoy", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "receptor_seed", "")),
    ("D-11", "name an axis the rule does not have", REJ,
     lambda d: _sub_rejection_line(os.path.join(d, REJ), 0, "mw", "vibes")),
    ("D-12", "swap an accepted decoy's SMILES for one that fails the window", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "smiles", "CCO")),
    ("D-13", "revert the charge axis to Chem.GetFormalCharge", None,
     lambda d: _revert_to_getformalcharge()),
    ("D-14", "lose a candidate between the pool and the two tables", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "n_eligible", "999999")),
    ("D-15", "blank the enacted cLogP window on a row, so nothing says what "
             "produced it", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "clogp_window", "")),
    ("D-16", "make two of a receptor's three decoys the same molecule", SEL,
     lambda d: _twin_the_draw(os.path.join(d, SEL))),
    # ---- the freeze, D-2026-09-12-g/h -----------------------------------
    ("D-17", "change the enacted cLogP window back to the relative form", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "clogp_window", "relative:0.2")),
    ("D-18", "swap the pinned ChEMBL download digest", POOL,
     lambda d: _col(os.path.join(d, POOL), None, "chembl_sha256", "0" * 64)),
    ("D-19", "drop a passing receptor out of the accepted set", SEL,
     lambda d: _drop_receptor_decoys(os.path.join(d, SEL), "OPSD")),
    ("D-20", "flatten B1B1U5's refusal into the other four receptors' class", SEL,
     lambda d: _col(os.path.join(d, SEL), {"receptor_slug": "B1B1U5"},
                    "n_eligible", "120973")),
    ("D-21", "reuse one receptor's decoy as another receptor's", SEL,
     lambda d: _accepted_row(os.path.join(d, SEL), "candidate_chembl_id",
                             next(r["candidate_chembl_id"] for r in tsv(SEL, d)
                                  if r["receptor_slug"] == "DRD3"
                                  and r["decoy_status"] == "accepted"),
                             slug="OPSD")),
    ("D-22", "swap one drawn decoy for an undrawn one the rule also accepted "
             "(no count in the gate changes)", SEL, _swap_one_id),
    ("D-23", "move the chemistry under a stable accession (the ChEMBL id set-hash "
             "still matches)", SEL, _swap_one_inchikey),
    ("D-24", "collapse two accepted receptors into one cluster, so k and the MDE "
             "move", SEL,
     lambda d: _accepted_rows_all(os.path.join(d, SEL), "OPSD", "cluster",
                                  next(r["cluster"] for r in tsv(SEL, d)
                                       if r["receptor_slug"] == "DRD3"))),
    ("D-26", "permute the assignment: the same 33 molecules against the wrong "
             "receptors (BOTH set-hashes still match)", SEL, _permute_assignment),
    # The plant must move what the check READS.  It used to set predictions_pooled
    # to 999, which D-25 no longer looks at now that the prediction totals are
    # deliberately unfrozen -- so it would have applied, changed bytes, and been
    # inert.  Flipping one READY decoy cell to BLOCKED moves the cell counts,
    # which is the frozen quantity.
    ("D-25", "flip one READY decoy cell to BLOCKED, moving the frozen cell counts",
     G2,
     lambda d: _col_csv(os.path.join(d, G2),
                        {"ligand": "decoy_lig", "dispatch_status": "READY"},
                        "dispatch_status", "BLOCKED_DECOY_UNAVAILABLE")),
]


def _twin_the_draw(path):
    """Amendment B's defect, planted: the first run's OPSD pair at T = 0.641, taken
    to its limit -- two of the three decoys are the identical molecule."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    cols = list(rows[0].keys())
    picks = [r for r in rows if r["decoy_status"] == "accepted"
             and r["receptor_slug"] == rows[0]["receptor_slug"]]
    assert len(picks) >= 2, "need a full draw to twin"
    for k in ("candidate_chembl_id", "smiles", "inchikey", "candidate_name"):
        picks[1][k] = picks[0][k]
    picks[1]["candidate_chembl_id"] = picks[0]["candidate_chembl_id"] + "_TWIN"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _first_excluded(d):
    """A molecule the exclusion table refuses for the receptor we plant on."""
    slug = next(r["receptor_slug"] for r in tsv(SEL, d)
                if r["decoy_status"] == "accepted")
    with open(os.path.join(d, EXCL)) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["receptor_slug"] == slug:
                return r["candidate_chembl_id"]
    raise AssertionError(f"no exclusion row for {slug}")


def _stage(tmp, touched):
    """Symlink every input, then COPY the one file the plant rewrites.

    The copy matters twice over: the plants open their target for writing, and a
    symlink would send that write straight through to redo/inputs/.  And the
    rejection table is 90 MB, so copying every file for every plant is a minute of
    the self-test spent on files no plant touches.
    """
    want = {f for f in os.listdir(INPUTS)
            if os.path.isfile(os.path.join(INPUTS, f)) and not f.startswith(".")}
    for f in want:
        os.symlink(os.path.join(INPUTS, f), os.path.join(tmp, f))
    # EVERY regular file, not a hand-written extension list.  This harness filtered
    # on (".tsv", ".csv") until 2026-09-12, and the day the rejection table became a
    # .gz that filter silently removed it from every planted copy: the gate then
    # failed on the missing input, "FAIL D-7" appeared in the output, and the D-7
    # plant was scored `fired` for a reason that had nothing to do with the plant,
    # while D-8 through D-16 never ran at all.  That is g0_preflight's defect of
    # 2026-09-12 reproduced in a different harness, in under a day, so the staging
    # now asserts what it staged rather than assuming it.
    have = set(os.listdir(tmp))
    if have != want:
        raise AssertionError(f"staging did not reproduce redo/inputs/: "
                             f"missing {sorted(want - have)}, extra {sorted(have - want)}")
    if touched:
        src = os.path.join(INPUTS, touched)
        if not os.path.exists(src):
            raise AssertionError(f"{touched} is not in redo/inputs/ -- the plant "
                                 f"would have been applied to nothing")
        dst = os.path.join(tmp, touched)
        os.remove(dst)
        shutil.copy(src, dst)
        return open(dst, "rb").read()
    return None


def selftest():
    if main() != 0:
        sys.stdout.write("baseline does not pass; fix that first\n")
        return 1
    sys.stdout.write("baseline: gate passes.  Planting one defect per check.\n\n")
    bad = 0
    for name, what, touched, plant in PLANTS:
        tmp = tempfile.mkdtemp()
        undo = None
        try:
            before = _stage(tmp, touched)
            undo = plant(tmp)
            # A plant that did not change anything proves nothing, and a harness
            # that cannot tell the difference prints a tidy tally anyway -- which
            # is exactly what g0_preflight's harness did for a day on 2026-09-12.
            if touched:
                p = os.path.join(tmp, touched)
                after = open(p, "rb").read() if os.path.exists(p) else None
                if after == before:
                    sys.stdout.write(f"  MISS {name}: {what} -> THE PLANT DID NOT "
                                     f"APPLY ({touched} is byte-identical)\n")
                    bad += 1
                    continue
            buf, old = io.StringIO(), sys.stdout
            sys.stdout = buf
            try:
                rc = main(root=tmp)
            finally:
                sys.stdout = old
        finally:
            if undo:
                undo()
            shutil.rmtree(tmp)
        fired = f"FAIL  {name}" in buf.getvalue()
        good = rc == 1 and fired
        bad += 0 if good else 1
        sys.stdout.write(f"  {'ok  ' if good else 'MISS'} {name}: {what}"
                         f" -> {'fired' if fired else 'DID NOT FIRE'}\n")
    sys.stdout.write(f"\n  {len(PLANTS) - bad}/{len(PLANTS)} checks proved by "
                     f"planting the defect each one exists to catch.\n\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv))
