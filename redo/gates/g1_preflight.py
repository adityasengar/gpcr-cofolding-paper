#!/usr/bin/env python3
"""g1_preflight.py — the dispatch-readiness gate for Group 1.

Nothing in Group 1 is submitted until this exits 0.  It is deliberately
mechanical: every check either passes on the files as they stand or names the
artefact that is missing.  Checks marked BLOCKING must pass; checks marked
PENDING are dependencies on sibling documents that have not landed, and they are
reported as NOT READY rather than as failures, because a sibling document being
in flight is not a defect.

Run:  python3 redo/gates/g1_preflight.py
Exit: 0 = every BLOCKING check passed and nothing is PENDING (dispatch may proceed)
      1 = a BLOCKING check failed
      2 = all BLOCKING checks passed but a PENDING dependency is outstanding

Prove the checks rather than trusting them:
  python3 redo/gates/g1_preflight.py --selftest
plants a defect for each blocking check in a scratch copy and asserts it fires.
"""
import csv
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEN_OK = re.compile(r"^\d+(-\d+)?$")


def tsv(name):
    with open(os.path.join(INPUTS, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def csvf(name):
    with open(os.path.join(INPUTS, name)) as fh:
        return list(csv.DictReader(fh))


def main(argv):
    blocking, pending, passed = [], [], []

    def B(ok, label, detail=""):
        (passed if ok else blocking).append(f"{label}" + (f" -- {detail}" if detail and not ok else ""))

    # ---------------------------------------------------------------- files
    need = ["g1_systems.csv", "g1_partner_registry.tsv", "g1_midrungs.tsv",
            "g1_receptors.tsv", "g1_recording_spec.tsv", "g1_minig.tsv",
            "g1_refchimera.tsv", "g1_cognate.tsv", "g1_panel_freeze.tsv",
            "seq_rungs.tsv", "seq_controls.tsv", "seq_a5null.tsv"]
    absent = [f for f in need if not os.path.exists(os.path.join(INPUTS, f))]
    B(not absent, "B1 every input artefact exists", f"absent: {absent}")
    if absent:
        report(blocking, pending, passed)
        return 1

    sysrows = csvf("g1_systems.csv")
    reg = tsv("g1_partner_registry.tsv")
    rec = tsv("g1_receptors.tsv")
    spec = tsv("g1_recording_spec.tsv")

    # ------------------------------------------------- B2 every chain B resolves
    # Re-resolved here against the registry rather than read back from the column
    # g1_systems.py wrote -- a check that trusts the generator's own verdict is
    # not a check.
    known = {r["construct"] for r in reg if r["held"] == "yes"}
    known |= {"R0_apo", "R8_hetero"}
    unres = sorted({r["chain_b_construct"] for r in sysrows
                    if r["chain_b_construct"].split("@")[0].split("#")[0]
                    .split("/")[0] not in known
                    or r["chain_b_len"] == "UNRESOLVED"
                    or r["chain_b_sha256"].startswith("UNRESOLVED")})
    B(not unres, "B2 every chain-B construct resolves in the registry",
      f"unresolved: {unres}")

    # ------------------------------------------------- B3 sha256 well formed
    bad = [f"{r['construct']}/{r['family']}/{r['variant']}" for r in reg
           if r["held"] == "yes" and not HEX64.match(r["sha256"])]
    B(not bad, "B3 every held construct carries a full 64-hex sha256",
      f"{len(bad)} malformed, e.g. {bad[:4]}")

    # ------------------------------------------- B4 nothing un-held is dispatched
    notheld = {r["construct"] for r in reg if r["held"] != "yes"}
    used = {r["chain_b_construct"].split("@")[0].split("#")[0] for r in sysrows}
    leak = sorted(notheld & used)
    B(not leak, "B4 no system dispatches a construct whose bytes are not held",
      f"{leak}")

    # ------------------------------------- B5 the naming trap: length is explicit
    # georgiou2025heterogeneity uses "mini-Gs" for a ~229-residue construct and for
    # a 21-residue peptide two sentences apart. No system row may carry a construct
    # name without a resolved numeric length or length range.
    noname = sorted({r["chain_b_construct"] for r in sysrows
                     if not LEN_OK.match(r["chain_b_len"])})
    B(not noname, "B5 every system row resolves chain B to a numeric length",
      f"{noname}")

    # --------------------------------- B6 no two cells of one arm are one molecule
    # The D2 defect: both ADRB2 nanobody subarms fed sha 1406ad7e..., one arm
    # contrasted with itself. Here: within an (item, arm) the set of chain-B
    # constructs must map to distinct sequences for every family.
    byfam = defaultdict(list)
    for r in reg:
        if r["held"] == "yes":
            byfam[r["family"]].append(r)

    def key_parts(k):
        """'ct21@scramble#2/5' -> ('ct21', 'scramble', '2')"""
        if "/" in k:
            k = k.rsplit("/", 1)[0]
        kk, _, var = k.partition("@")
        var, _, idx = var.partition("#")
        return kk, var, idx

    collide, noop = [], []
    for a, rows in groupby_items(sysrows):
        keys = sorted({r["chain_b_construct"] for r in rows})
        for fam, entries in byfam.items():
            shas = defaultdict(set)
            for k in keys:
                base, var, idx = key_parts(k)
                for e in entries:
                    if e["construct"] != base:
                        continue
                    if var and not e["variant"].startswith(var):
                        continue
                    if idx and e["k"] != idx:
                        continue
                    shas[e["sha256"]].add(k)
            for s, ks in shas.items():
                if len(ks) < 2:
                    continue
                # an alanine substitution at a position that is already alanine is
                # a declared no-op, flagged in the registry, not a design error --
                # it is a free within-arm wild-type replicate, and must be labelled
                # as one rather than counted as a perturbation.
                flags = {e["note"][:6] for e in entries if e["sha256"] == s}
                if "NO-OP:" in flags:
                    noop.append(f"{a} / {fam}: {sorted(ks)} (position already Ala)")
                else:
                    collide.append(f"{a} / family {fam}: {sorted(ks)} are the same "
                                   f"molecule (sha {s[:16]})")
    B(not collide, "B6 no two cells within one arm are the same molecule",
      "; ".join(sorted(set(collide))[:6]))
    if noop:
        pending.append("P: declared no-op cells (alanine substitution at a position "
                       "that is already alanine) -- run them, but label them "
                       "is_noop=true and count them as within-arm wild-type "
                       "replicates, never as perturbations: "
                       + "; ".join(sorted(set(noop))))

    # ------------------------------------------- B7 MSA condition set on every row
    badmsa = [r["chain_b_construct"] for r in sysrows
              if r["partner_msa"] not in ("off", "ON", "n/a")
              or r["receptor_msa"] != "on (default)"]
    B(not badmsa, "B7 every row declares a partner-MSA and receptor-MSA condition",
      f"{sorted(set(badmsa))[:5]}")

    # --------------------------- B8 MSA-off is the primary condition on every rung
    off = Counter(r["partner_msa"] for r in sysrows if r["n_chains"] != "1")
    B(off.get("off", 0) > off.get("ON", 0),
      "B8 MSA-free on the partner chain is the primary condition",
      f"off={off.get('off',0)} ON={off.get('ON',0)}")

    # ------------------------------- B9 the frozen primary panel is well formed
    # One per cluster, with declared overrides the only exception, and NO
    # chimeric-reference receptor anywhere in it (DECISION 1).
    frz = {r["receptor_slug"]: r for r in tsv("g1_panel_freeze.tsv")}
    core = [r for r in frz.values() if r["core_frozen"] == "yes"]
    cl = Counter(r["cluster"] for r in core)
    over = {r["receptor_slug"] for r in core if r["override_reason"]}
    dirty = sorted(r["receptor_slug"] for r in core
                   if r["reference_tip_subtype"].startswith("CHIMERIC"))
    extra = sum(v - 1 for v in cl.values())
    B(not dirty and extra == len(over),
      "B9 the frozen primary panel is one per cluster, overrides declared, "
      "and carries no chimeric-reference receptor",
      f"chimeric in panel: {dirty}; clusters with >1 member: {extra}, "
      f"declared overrides: {sorted(over)}")

    # ---------- B16 the cognate assignment is TWO columns, never one
    # DECISION 2. A row that carries the biology without the structure, or the
    # structure without the biology, has re-conflated the two questions.
    half = sorted({r["receptor_slug"] for r in sysrows
                   if bool(r["supplied_partner_family"])
                   != bool(r["reference_tip_subtype"])}
                  | {r["receptor_slug"] for r in sysrows
                     if r["receptor_slug"] != "*"
                     and not r["cognate_vs_reference_agree"]})
    B(not half, "B16 every row carries BOTH the supplied-partner family and the "
                "reference tip, never one without the other", f"{half[:6]}")

    # ------------------------------- B10 R6a agrees between its two source tables
    a5 = {r["family"]: r["sha256"] for r in tsv("seq_a5null.tsv")
          if r["construct"] == "R6a_da5"}
    rr = {r["family"]: r["sha256"] for r in tsv("seq_rungs.tsv")
          if r["rung"] == "R6a_da5"}
    dis = sorted(f for f in a5 if a5[f] != rr.get(f))
    B(not dis, "B10 R6a_da5 agrees byte-for-byte between seq_rungs and seq_a5null",
      f"{dis}")

    # ----------------------------------- B11 recording spec covers the essentials
    have = {r["column"] for r in spec}
    must = {"partner_seq_sha256", "n_partner_aa", "partner_chain_helicity_frac",
            "plddt_partner_chain_mean", "partner_msa_depth", "partner_msa_mode",
            "receptor_seq_sha256", "cross_species_partner", "axis_npxxy", "axis_tm6",
            "interface_score_dockq_like", "ras_domain_ca_rmsd_to_R7"}
    B(must <= have, "B11 the per-row recording spec carries the load-bearing columns",
      f"missing {sorted(must - have)}")

    # --------- B12 every engineered-reference receptor is carried, not silent
    # Twelve census receptors have a Rule-R ACTIVE reference whose alpha5 tip is
    # not canonical for any human Galpha, and rungs R1-R4 *are* that tip. Every
    # affected CORE-32 receptor must appear in the reference-matched arm, and the
    # recording spec must carry the per-row identity columns, or the mismatch
    # becomes invisible exactly where the paper is most specific.
    chim = tsv("g1_refchimera.tsv")
    affected = {r["slug"] for r in chim if r["is_rule_r_reference"] == "active"
                and r["in_core32_provisional"] == "yes"}
    carried = {r["receptor_slug"] for r in sysrows if r["arm"] == "reference_matched_tip"}
    missing = sorted(affected - carried)
    cols_ok = {"ref_alpha5_tip_identity", "ref_alpha5_is_canonical"} <= have
    B(not missing and cols_ok,
      "B12 every engineered-alpha5-reference receptor is carried explicitly",
      f"not in the reference-matched arm: {missing}; "
      f"recording-spec columns present: {cols_ok}")

    # ------- B13 every cognate row resolves, or says exactly why it does not
    # The cognate map made this checkable for the first time: a row may carry a
    # 64-hex sha, or be a declared chimera with all three options named, or be a
    # declared no-chain-B / multi-chain row. Nothing else.
    HEXOK = re.compile(r"^[0-9a-f]{64}")
    unclear = []
    for r in sysrows:
        v = r["chain_b_sha256"]
        if HEXOK.match(v) or v == "-":
            continue
        if v.startswith("PENDING:PI-DECISION"):
            if not ("tip=" in r["chain_b_family_rule"]
                    and "scaffold=" in r["chain_b_family_rule"]
                    and "deposited" in r["chain_b_family_rule"]):
                unclear.append(f"{r['receptor_slug']}/{r['chain_b_construct']}: "
                               f"chimera row does not name all three options")
            continue
        if v.startswith(("resolved,", "PENDING:COUPLING.md",
                         "e16ad41084f6a7b9", "one sha", "family-dependent")):
            continue
        unclear.append(f"{r['receptor_slug']}/{r['chain_b_construct']}: {v[:40]}")
    B(not unclear, "B13 every cognate row resolves or names its three options",
      "; ".join(sorted(set(unclear))[:5]))

    # ------------- B14 the evidence class travels with every cognate row
    cogrows = [r for r in sysrows if r["cognate_evidence_class"] not in ("", "n/a")]
    classes = set(r["cognate_evidence_class"] for r in cogrows)
    B(cogrows and classes <= {"STRUCTURE_EXACT", "STRUCTURE_NEAR", "PEPTIDE_ENTITY",
                              "CONVENTION_FALLBACK", "CHIMERA_SPLIT"},
      "B14 every cognate row carries its evidence class",
      f"classes seen: {sorted(classes)}")

    # ---------- B15 the alpha5-null arm comes from ONE generator
    # It briefly did not: seq_a5null.tsv shipped without seq_a5null.py, a cognate
    # subtype appeared that it did not cover, and two constructs were built here
    # under a declared substitute rule. seq_a5null.py now exists and the table
    # covers seven families. This check makes the regression impossible rather
    # than remembered.
    a5used = {r["chain_b_construct"].split("@")[0] for r in sysrows} & {
        "R6a_da5", "R6b_a5perm", "R6c_a5polyA"}
    offenders = sorted({f"{r['construct']}/{r['family']} <- {r['source_table']}"
                        for r in reg if r["construct"] in a5used
                        and r["held"] == "yes"
                        and r["construct_class"] == "a5null_substitute_rule"})
    a5_from = {r["source_table"] for r in reg if r["construct"] == "R6b_a5perm"
               and r["held"] == "yes"}
    B(not offenders and a5_from <= {"seq_a5null.tsv"},
      "B15 every alpha5-null construct comes from seq_a5null.tsv, one generator",
      f"substitute-rule constructs still dispatched: {offenders}; "
      f"R6b sources: {sorted(a5_from)}")

    # ------------------------------------------------------- pending dependencies
    for f, what in (("SEQ_RECEPTORS.md", "chain-A receptor sequences and their hashes"),
                    ("COUPLING.md", "cognate Galpha per receptor")):
        if not os.path.exists(os.path.join(SPEC, f)):
            pending.append(f"P: {f} has not landed -- {what}")
    cogm = tsv("g1_cognate.tsv")
    nd = sorted({r["receptor_slug"] for r in cogm if not r["cognate_subtype"]})
    ndc = sorted({r["receptor_slug"] for r in cogm if not r["cognate_subtype"]
                  and r["in_core32_provisional"] == "yes"})
    n_pend = sum(1 for r in sysrows if r["chain_b_sha256"].startswith("PENDING"))
    if nd:
        ext = sorted({r["receptor_slug"] for r in sysrows
                      if r["tier"] == "EXTENSION-chimeric-reference"})
        pending.append(
            f"P: DECIDED -- the {len(nd)} cross-family chimeras are EXCLUDED from "
            f"the primary panel and carried in the extension tier with G19 as the "
            f"matched control: {ext}. What survives is narrower: anyone who runs "
            f"that tier still has to choose tip vs scaffold vs deposited for its "
            f"{n_pend} rows. Nothing in the primary panel depends on it")
    conv = sorted({r["receptor_slug"] for r in cogm
                   if r["evidence_class"] == "CONVENTION_FALLBACK"})
    if conv:
        pending.append(f"P: {len(conv)} receptors have NO Galpha in their Rule-R "
                       f"active reference and take a declared convention fallback "
                       f"-- {conv}. OPRM has no active reference containing a "
                       f"Galpha at all; NTR1's fallback rests on a non-Rule-R "
                       f"structure against a unanimous Gq/11 annotation")
    # -- B17  the reversals stay resolved -----------------------------------
    # This was a wait() until 2026-09-12.  All four assignments that reverse
    # Block B's prior are now closed: B1B1U5 by D-H (reference 9EPP, a
    # spider-Gq-tipped chimera with no native alternative), and CCKAR, EDNRB and
    # GHSR by F-14 -- in each of those three the family the Rule-R structure
    # reads is the ONLY family with a native, full-length, non-engineered Ga
    # anywhere in that receptor's active structures.  Block B's Gq prior exists
    # for all three only as a chimera, a mini-G or a subunit the depositors
    # themselves label "engineered".
    #
    # So the check is: for every reversal receptor we have evidence for, the
    # cognate family we supply must be one that HAS a native representative.
    # A future snapshot carrying a native Gq-CCKAR structure reopens F-14, and
    # this is what would notice.
    rev = sorted({r["receptor_slug"] for r in cogm
                  if r["reverses_blockb_prior"] == "yes"})
    ev_name = "coupling_reversal_evidence.tsv"
    ev_path = os.path.join(INPUTS, ev_name)
    if not os.path.exists(ev_path):
        # A missing input is a FAILURE, not a skip.  A check that quietly does
        # nothing when its evidence is absent is the defect it exists to catch.
        B(False, "B17 every Block-B reversal supplies a natively-represented "
                 "Ga family",
          "coupling_reversal_evidence.tsv is ABSENT -- run "
          "redo/build/coupling_reversal_evidence.py")
    else:
        ev = tsv(ev_name)
        native_fams = {}
        for r in ev:
            if r["construct_class"] == "native":
                native_fams.setdefault(r["receptor_slug"], set()).update(
                    r["ga_family"].split(";"))
        bad = []
        for slug in sorted(native_fams):
            row = next((r for r in cogm if r["receptor_slug"] == slug), None)
            if row is None:
                bad.append(f"{slug}: in the evidence table, absent from the map")
                continue
            # the map records a FAMILY (Gi/o, Gs, Gq/11); the evidence records a
            # SUBTYPE accession (Gi1, Gs, Gq).  Compare on the family prefix.
            fam = row["cognate_family"]
            want = {f.split("(")[0] for f in native_fams[slug]}
            hit = any(w in fam or fam.split("/")[0] in w for w in want)
            if not hit:
                bad.append(f"{slug}: supplies {fam}, natively represented "
                           f"families are {sorted(want)}")
        covered = sorted(native_fams)
        B(not bad, "B17 every Block-B reversal supplies a natively-represented "
                   "Ga family", "; ".join(bad))
        if not bad:
            passed[-1] += (f"  [{len(covered)} of {len(rev)} reversal receptors "
                           f"have structural evidence: {', '.join(covered)}; "
                           f"B1B1U5 is closed by D-H, not by this check]")
    sub = [r for r in reg if r["construct_class"] == "a5null_substitute_rule"]
    if sub:
        pending.append(f"P: {len(sub)} alpha5-null constructs were built under a "
                       f"DECLARED SUBSTITUTE rule because seq_a5null.tsv has no "
                       f"generator on disk and its seed convention is not "
                       f"recoverable -- ask for seq_a5null.py, or declare the "
                       f"substitute rule for the whole arm "
                       f"({sorted(r['family'] for r in sub)})")
    dis = sorted({r["receptor_slug"] for r in sysrows
                  if r["cognate_vs_reference_agree"] == "NO"})
    if dis:
        pending.append(f"P: {len(dis)} receptors where the coupling annotation and "
                       f"the deposited reference tip disagree at family level -- "
                       f"{dis}. The biology wins for the supplied partner; the row "
                       f"is flagged either way")
    # -- B18  every proposed arm is costed ----------------------------------
    # This was a wait() until 2026-09-12: RUN_MATRIX.md §7.1 had no line item for
    # E1.8 or E1.9.  G18a/b, G19 and G20 were missing too.  They are costed now,
    # derived from THIS file, and matrix_cost.py::check_against_systems() asserts
    # each reproduces the totals here.  The check below is the other direction:
    # no arm may appear in g1_systems.csv without a line in the cost table.
    mc = os.path.join(BUILD, "matrix_cost.py")
    if not os.path.exists(mc):
        B(False, "B18 every arm in g1_systems.csv has a line item in "
                 "matrix_cost.py", "matrix_cost.py is ABSENT")
    else:
        # the ids matrix_cost declares, read from its ITEMS tuples
        costed = set(re.findall(r'^\s*\("([A-Za-z0-9-]+)"', open(mc).read(),
                                flags=re.M))
        # an arm "G16(proposed)" is costed if G16, G16a or G16b is declared
        # an arm id may name several cost items at once ("G1a/G1b", "G3a/G3b"),
        # and a bare id may be costed as an a/b pair ("G16" -> G16a, G16b).
        uncosted = []
        for item in sorted({r["item"] for r in sysrows}):
            parts = [t.strip() for t in item.split("(")[0].split("/") if t.strip()]
            if not all({t, t + "a", t + "b"} & costed for t in parts):
                uncosted.append(item)
        B(not uncosted, "B18 every arm in g1_systems.csv has a line item in "
                        "matrix_cost.py", f"uncosted: {uncosted}")
        if not uncosted:
            passed[-1] += (f"  [{len({r['item'] for r in sysrows})} arms, all "
                           f"costed; matrix_cost declares {len(costed)} ids]")
    pending.append("P: pre-flight partner-MSA depth measurement (SEQUENCES.md "
                   "§6.1(4)) has not been run on the ~60 distinct peptide-rung "
                   "sequences; it is hours of wall-clock and no inference")
    pending.append("P: OPSD resolves to Gt1 from an 11-residue peptide entity "
                   "(4X1H). Everything past rung R1_ct11 is EXTRAPOLATION -- it "
                   "has no alpha5 reference beyond the 11-mer")

    report(blocking, pending, passed)
    if blocking:
        return 1
    return 2 if pending else 0


def groupby_items(rows):
    g = defaultdict(list)
    for r in rows:
        g[f"{r['item']}/{r['arm']}"].append(r)
    return sorted(g.items())


def report(blocking, pending, passed):
    for p in passed:
        sys.stdout.write(f"  PASS  {p}\n")
    for b in blocking:
        sys.stdout.write(f"  FAIL  {b}\n")
    for p in pending:
        sys.stdout.write(f"  WAIT  {p[3:]}\n")
    sys.stdout.write(f"\n{len(passed)} passed, {len(blocking)} failed, "
                     f"{len(pending)} pending\n")
    if blocking:
        sys.stdout.write("DO NOT DISPATCH.\n")
    elif pending:
        sys.stdout.write("Blocking checks pass; dependencies outstanding.\n")
    else:
        sys.stdout.write("READY.\n")


def selftest():
    """Plant one defect per blocking check and assert that check fires.

    A checker that has never failed is not known to work. Each case below copies
    the real artefacts into a scratch directory, corrupts exactly one thing, and
    asserts that (a) the run fails and (b) the named check is the one that fails.
    """
    import io
    import shutil
    import tempfile
    global INPUTS
    real = INPUTS
    cases = {
        "B1": ("g1_midrungs.tsv", lambda t: os.remove(t)),
        "B2": ("g1_systems.csv", lambda t: _sub(t, "R3_ct21", "R3_ct99", 1)),
        "B3": ("g1_partner_registry.tsv",
               lambda t: _sub(t, "\t9569a7eb", "\tZZZZZZZZ", 1)),
        "B4": ("g1_systems.csv", lambda t: _sub(t, "ubiquitin", "DAMGO", 999)),
        "B5": ("g1_systems.csv", lambda t: _col(t, "chain_b_len", "mini-G")),
        # two distinct construct keys resolving to the same bytes -- the D2 defect
        "B6": ("g1_partner_registry.tsv",
               lambda t: _clone_sha(t, ("ct21", "G13", "polyA"),
                                    ("ct21", "G13", "reversed"))),
        "B7": ("g1_systems.csv", lambda t: _col(t, "partner_msa", "maybe")),
        "B8": ("g1_systems.csv", lambda t: _col(t, "partner_msa", "ON")),
        "B9": ("g1_panel_freeze.tsv", lambda t: _col_tsv(t, "core_frozen", "yes")),
        "B10": ("seq_a5null.tsv", lambda t: _sub(t, "7c75cc25", "7c75cc26", 1)),
        "B11": ("g1_recording_spec.tsv",
                lambda t: _drop_line(t, "partner_msa_depth\t")),
        "B12": ("g1_systems.csv",
                lambda t: _sub(t, "reference_matched_tip", "ladder", 999)),
        "B13": ("g1_systems.csv", lambda t: _col(t, "chain_b_sha256", "ask the map")),
        "B14": ("g1_systems.csv",
                lambda t: _col(t, "cognate_evidence_class", "probably fine")),
        "B15": ("g1_partner_registry.tsv",
                lambda t: _retag(t, "R6b_a5perm", "Gi3")),
        "B16": ("g1_systems.csv",
                lambda t: _col(t, "reference_tip_subtype", "")),
        # flip GHSR back to Block B's Gq -- a family present only as an
        # "Engineered G-alpha-q" subunit in both structures that carry it
        "B17": ("g1_cognate.tsv",
                lambda t: _retag_cognate(t, "GHSR", "Gq/11")),
        # rename an arm to an id matrix_cost.py has never heard of
        "B18": ("g1_systems.csv",
                lambda t: _sub(t, "G16(proposed)", "G99(proposed)", 999)),
    }
    ok = True
    for name, (fn, corrupt) in cases.items():
        tmp = tempfile.mkdtemp()
        for f in os.listdir(real):
            if f.endswith((".tsv", ".csv", ".md")):
                shutil.copy(os.path.join(real, f), tmp)
        corrupt(os.path.join(tmp, fn))
        INPUTS = tmp
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            rc = main(["g1_preflight.py"])
        finally:
            sys.stdout = old
            INPUTS = real
            shutil.rmtree(tmp)
        out = buf.getvalue()
        fired = f"FAIL  {name} " in out or f"FAIL  {name}\n" in out
        good = rc == 1 and fired
        ok &= good
        sys.stdout.write(f"  {'ok  ' if good else 'MISS'} {name}: planted a defect in "
                         f"{fn} -> rc={rc}, {name} fired={fired}\n")
    sys.stdout.write("\nall blocking checks proved\n" if ok
                     else "\nSOME CHECKS DID NOT FIRE -- they cannot be trusted\n")
    return 0 if ok else 1


def _retag_cognate(path, slug, family):
    """Rewrite one receptor's cognate_family in the cognate map."""
    lines = open(path).read().split("\n")
    hdr = lines[0].split("\t")
    i_slug, i_fam = hdr.index("receptor_slug"), hdr.index("cognate_family")
    for n, ln in enumerate(lines[1:], 1):
        if not ln.strip():
            continue
        f = ln.split("\t")
        if f[i_slug] == slug:
            f[i_fam] = family
            lines[n] = "\t".join(f)
            break
    open(path, "w").write("\n".join(lines))


def _sub(path, old, new, n):
    s = open(path).read()
    open(path, "w").write(s.replace(old, new, n))


def _drop_line(path, prefix):
    lines = [l for l in open(path) if not l.startswith(prefix)]
    open(path, "w").writelines(lines)


def _clone_sha(path, src, dst):
    """Copy one registry row's sha256 onto another, making two headers one molecule."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    def find(k):
        return next(r for r in rows
                    if (r["construct"], r["family"], r["variant"]) == k)
    find(dst)["sha256"] = find(src)["sha256"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _retag(path, construct, family):
    """Make one alpha5-null row look like a substitute-rule build again."""
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    for r in rows:
        if r["construct"] == construct and r["family"] == family:
            r["construct_class"] = "a5null_substitute_rule"
            r["source_table"] = "derived here -- DECLARED SUBSTITUTE RULE"
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def _col(path, col, val):
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        r[col] = val
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _col_tsv(path, col, val):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    for r in rows:
        r[col] = val
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv))
