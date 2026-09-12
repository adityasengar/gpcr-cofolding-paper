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
import io
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, BUILD  # noqa: E402

sys.path.insert(0, BUILD)
import drule_select as DS  # noqa: E402

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
        n_elig = int(rows[0]["n_eligible"] or 0)
        n_acc = int(rows[0]["n_accepted"] or 0)
        if n_elig != n_acc + per_rec.get(s, 0):
            lost.append(f"{s}: {n_elig:,} eligible != {n_acc:,} accepted + "
                        f"{per_rec.get(s, 0):,} rejected")
    chk("D-14  accepted + rejected == eligible, for every receptor: no candidate is "
        "silently dropped", not lost, "; ".join(lost[:4]) if lost else
        f"conserved over {len([s for s in scope if tg.get(s, {}).get('chembl_target_id')])}"
        f" receptors with a resolved target")


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
