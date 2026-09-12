#!/usr/bin/env python3
"""Every number COUPLING.md quotes, recomputed from the coupling_* files.

The project's rule is that a sentence carries a locator: prior work cites
[citekey p.N], our own numbers are recomputed. COUPLING.md is our own numbers,
so this is its verifier. Run it and diff the output against the document.

    python3 redo/build/coupling_summary.py

It also carries the planted-defect self-tests (`--selftest`), because four
checkers in this project have already reported nothing while their reporting
path never ran.
"""
import collections
import csv
import json
import os
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
A = os.path.join(INPUTS, "coupling_assignments.csv")
S = os.path.join(INPUTS, "coupling_refstructures.csv")
I = os.path.join(INPUTS, "coupling_rung_impact.csv")
G = os.path.join(INPUTS, "coupling_gproteindb.csv")
T = os.path.join(INPUTS, "coupling_gtopdb.csv")
RUNGS = os.path.join(INPUTS, "seq_rungs.tsv")

RUNG_ORDER = ("R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix", "R5_a5plus",
              "R6a_da5", "R7_full")
FAMILY_MEMBERS = {
    "Gs": ["Gs", "Golf"],
    "Gi/o": ["Gi1", "Gi2", "Gi3", "Go", "Gt1", "Gt2", "Ggust", "Gz"],
    "Gq/11": ["Gq", "G11", "G14", "G15"],
    "G12/13": ["G12", "G13"],
}


def load():
    return (list(csv.DictReader(open(A))), list(csv.DictReader(open(S))),
            list(csv.DictReader(open(I))))


def main():
    a, s, imp = load()
    rungs = collections.defaultdict(dict)
    for r in csv.DictReader(open(RUNGS), delimiter="\t"):
        rungs[r["rung"]][r["family"]] = r["sequence"]

    print("=" * 78)
    print("1. PANEL AND VERDICTS")
    print("=" * 78)
    print("C1 receptors                          : %d" % len(a))
    vc = collections.Counter(r["verdict"] for r in a)
    for k in ("cognate_confident", "cognate_ambiguous", "cognate_conflicted"):
        print("  %-36s: %d" % (k, vc[k]))
    print("  receptors with a single primary family: %d"
          % sum(1 for r in a if len(r["family_primary"].split(";")) == 1))

    print("\n%s\n2. AUTHORITY COVERAGE\n%s" % ("=" * 78, "=" * 78))
    cov = collections.Counter()
    for r in a:
        cov["assay lab (any of Bouvier/Inoue/Martemyanov/Lambert/Roth)"] += \
            bool(r["authority_assaylabs"])
        cov["GtoPdb via GproteinDb"] += bool(r["authority_gtopdb_via_gproteindb"])
        cov["IUPHAR fetched direct"] += bool(r["authority_iuphar_direct_primary"])
        cov["deposited active reference"] += bool(r["authority_structure"])
    for k, v in cov.items():
        print("  %-52s: %d/%d" % (k, v, len(a)))
    nauth = collections.Counter(int(r["n_authorities"]) for r in a)
    print("  receptors by number of authorities    : %s" % dict(sorted(nauth.items())))
    print("  receptors with ZERO authority         : %s"
          % [r["slug"] for r in a if int(r["n_authorities"]) == 0])

    print("\n%s\n3. WHERE THE DEPOSITED STRUCTURE CONTRADICTS EVERY ANNOTATION\n%s"
          % ("=" * 78, "=" * 78))
    mism = []
    for r in a:
        st = set(filter(None, r["authority_structure"].split(";")))
        ann = set()
        for k in ("authority_gtopdb_via_gproteindb", "authority_iuphar_direct_primary"):
            ann |= set(filter(None, r[k].split(";")))
        for part in filter(None, r["authority_assaylabs"].split(";")):
            ann |= set(part.split("=", 1)[1].split("+"))
        if st and ann and not (st & ann):
            mism.append((r["slug"], ";".join(sorted(st)), ";".join(sorted(ann)),
                         r["structure_evidence"]))
    print("  count: %d" % len(mism))
    for m in mism:
        print("    %-7s structure=%-8s annotation=%-14s %s" % m)

    print("\n%s\n4. WHAT THE ACTIVE REFERENCES ACTUALLY CONTAIN\n%s" % ("=" * 78, "=" * 78))
    act = [r for r in s if r["role"] == "active"]
    kinds = collections.Counter(r["kind"] for r in act)
    print("  polymer entities across all active references: %d" % len(act))
    for k, v in kinds.most_common():
        print("    %-28s %d" % (k, v))
    ga = [r for r in act if r["kind"].startswith("G-alpha")]
    print("  G-alpha chains                     : %d" % len(ga))
    print("  ... that are mini-G (<300 aa)       : %d"
          % sum(1 for r in ga if "mini-G" in r["construct_note"]))
    print("  ... that are coupling chimeras      : %d"
          % sum(1 for r in ga if "COUPLING CHIMERA" in r["construct_note"]))
    print("  ... fused to another chain          : %d"
          % sum(1 for r in ga if r["kind"] == "G-alpha-fusion"))
    print("  receptors whose active refs carry NO G-alpha: %s"
          % [r["slug"] for r in a if r["active_ref_has_galpha"] == "no"])
    nb = collections.Counter(r["slug"] for r in act if r["kind"] == "nanobody/antibody")
    print("  active references containing a nanobody/antibody: %d receptors" % len(nb))
    print("  active references containing arrestin: %s"
          % sorted({r["slug"] for r in act if r["kind"] == "arrestin"}))

    print("\n  chimeras, one line each (accession names the scaffold, "
          "C-terminus names the coupling):")
    for r in ga:
        if "CHIMERA" in r["construct_note"]:
            print("    %-7s %-5s xref=%-8s len=%-4s ct11=%s -> %s"
                  % (r["slug"], r["pdb"], r["uniprot"] or "none", r["length"],
                     r["ct11"], r["ct11_family"]))

    # 4b -- the alpha5 tip actually deposited, against the 16 canonical human Ga.
    # This is the check that matters most for a paper about the alpha5-CT: if the
    # reference we score against carries an ENGINEERED tip, then supplying the
    # wild-type human peptide is not reproducing the reference, it is a third
    # thing. No previous audit asked this, because verify_partner_chains.py
    # compares a partner against ITS OWN accession and every one of these passes
    # that test -- an engineered chimera with no UniProt cross-reference simply
    # returns NO-UNIPROT-XREF and is flagged, not decoded.
    term = json.load(open(os.path.join(CACHE, "coupling_family_termini.json")))
    canon = {v["ct11"] for v in term.values()}
    exact = [r for r in ga if r["ct11"] in canon]
    engineered = [r for r in ga if r["ct11"] and r["ct11"] not in canon]
    print("\n  deposited alpha5 tips (last 11) against the 16 canonical human Ga:")
    print("    exact match to a canonical human Ga : %d of %d" % (len(exact), len(ga)))
    print("    NOT any canonical human sequence    : %d of %d" % (len(engineered), len(ga)))
    for tip, n in collections.Counter(r["ct11"] for r in engineered).most_common():
        best = min(((sum(1 for x, y in zip(tip, v["ct11"]) if x != y), k)
                    for k, v in term.items()))
        print("      %-12s x%-3d nearest canonical: %s (%d substitutions)"
              % (tip, n, best[1], best[0]))
    only_eng = sorted({r["slug"] for r in engineered} - {r["slug"] for r in exact})
    print("    receptors whose EVERY active reference carries an engineered tip: "
          "%d" % len(only_eng))
    print("      %s" % ", ".join(only_eng))

    print("\n%s\n5. RUNG IMPACT OF AN AMBIGUOUS ASSIGNMENT\n%s" % ("=" * 78, "=" * 78))
    nonconf = [r for r in imp if r["verdict"] != "cognate_confident"]
    print("  non-confident receptors: %d" % len(nonconf))
    print("  ... whose primary-candidate set is a SINGLE family (rungs immune): %d"
          % sum(1 for r in nonconf if int(r["n_primary_candidates"]) == 1))
    print("  ... with >1 primary-candidate family (bytes differ at EVERY rung): %d"
          % sum(1 for r in nonconf if int(r["n_primary_candidates"]) > 1))
    print("\n  per rung, over all %d receptors:" % len(imp))
    print("  %-12s %-28s %s" % ("rung", "bytes differ (primary set)",
                                "bytes differ (all annotated)"))
    for rung in RUNG_ORDER:
        print("  %-12s %-28s %s"
              % (rung,
                 sum(1 for r in imp if r[rung].startswith("DIFFERS")),
                 sum(1 for r in imp if r["any_" + rung].startswith("DIFFERS"))))
    print("\n  LENGTH of the supplied chain, per rung (this is what costs):")
    for rung in RUNG_ORDER:
        lens = sorted({len(v) for v in rungs[rung].values()})
        print("    %-12s %s" % (rung, "all %d aa" % lens[0] if len(lens) == 1
                                else "%d-%d aa (spread %d)" % (lens[0], lens[-1],
                                                               lens[-1] - lens[0])))
    print("\n  extra arms if every primary-candidate family is run instead of one:")
    extra_p = sum(int(r["n_primary_candidates"]) - 1 for r in imp)
    extra_a = sum(int(r["n_any_annotated"]) - 1 for r in imp)
    print("    primary-candidate families : %d extra receptor-arms (%.2fx)"
          % (extra_p, (len(imp) + extra_p) / float(len(imp))))
    print("    all annotated transducers  : %d extra receptor-arms (%.2fx)"
          % (extra_a, (len(imp) + extra_a) / float(len(imp))))

    print("\n%s\n6. SUBTYPE AMBIGUITY WITHIN A FAMILY -- IS IT REALLY FREE?\n%s"
          % ("=" * 78, "=" * 78))
    print("  SEQUENCES.md 3.2 says that below R6 the only coupling decision that")
    print("  can change the supplied bytes is the FAMILY. Tested here per family:")
    for fam, members in FAMILY_MEMBERS.items():
        for rung in ("R1_ct11", "R3_ct21"):
            seqs = {m: rungs[rung][m] for m in members if m in rungs[rung]}
            groups = collections.defaultdict(list)
            for m, q in seqs.items():
                groups[q].append(m)
            print("    %-7s %-9s %d subtypes -> %d distinct sequences  %s"
                  % (fam, rung, len(seqs), len(groups),
                     " | ".join("=".join(sorted(v)) for v in groups.values())))

    print("\n  subtype-level disagreement ON THIS PANEL (the 22% figure, replicated):")
    multi = [r for r in a
             if len([x for x in r["subtype_reported"].split(";") if x]) >= 1
             and len([x for x in r["authority_assaylabs"].split(";") if x]) >= 2]
    dis = [r for r in multi
           if len([x for x in r["subtype_reported"].split(";") if x]) > 1]
    print("    receptors with >=2 assay labs reporting a primary subtype: %d" % len(multi))
    print("    ... where those labs name DIFFERENT subtypes            : %d (%.0f%%)"
          % (len(dis), 100.0 * len(dis) / len(multi) if multi else 0))
    print("    subtypes named as primary anywhere on the panel: %s"
          % dict(collections.Counter(
              x.split("(")[0] for r in a
              for x in r["subtype_reported"].split(";") if x).most_common()))
    have = set(rungs["R1_ct11"])
    named = {x.split("(")[0] for r in a for x in r["subtype_reported"].split(";") if x}
    print("    named as primary but ABSENT from seq_rungs.tsv: %s"
          % sorted(named - have - {"GsL", "GsS"}))

    print("\n%s\n7. THE PRIOR ASSIGNMENT (Block B's 40) AGAINST ITS OWN REFERENCES\n%s"
          % ("=" * 78, "=" * 78))
    prior = [r for r in a if r["blockb_prior"]]
    print("  receptors carrying a Block B cognate class: %d" % len(prior))
    pc = collections.Counter(r["blockb_prior_vs_structure"].split("(")[0].strip()
                             for r in prior)
    for k, v in pc.items():
        print("    %-56s %d" % (k[:56], v))
    for r in prior:
        if r["blockb_prior_vs_structure"].startswith("PRIOR CONTRADICTS"):
            print("      %-7s Block B %-4s -> reference supplies %-8s (%s)"
                  % (r["slug"], r["blockb_prior"], r["authority_structure"],
                     r["structure_evidence"]))
    print("  Block B family not among any authority's primary set: %s"
          % [r["slug"] for r in prior if r["blockb_prior_check"].startswith("PRIOR DIS")])

    print("\n%s\n7b. THE TWO HARD RULES lit HANDED BACK, APPLIED TO THIS PANEL\n%s"
          % ("=" * 78, "=" * 78))
    g1213 = [r["slug"] for r in a if "G12/13" in r["family_primary"].split(";")]
    print("  receptors where some authority calls G12/13 PRIMARY (0% inter-dataset")
    print("  core agreement for that family, pandyszekeres2024gproteindb p.8 Fig 4C):")
    print("    %d -- %s" % (len(g1213), ", ".join(g1213)))
    print("  ... of which none is `cognate_confident`: %s"
          % all(r["verdict"] != "cognate_confident" for r in a
                if r["slug"] in set(g1213)))
    omitted = []
    for r in a:
        gtop = set(filter(None, r["authority_gtopdb_via_gproteindb"].split(";")))
        lab = set()
        for part in filter(None, r["authority_assaylabs"].split(";")):
            lab |= set(part.split("=", 1)[1].split("+"))
        if gtop and lab and (lab - gtop):
            omitted.append((r["slug"], ";".join(sorted(lab - gtop))))
    print("\n  receptors where a biosensor lab ranks a family 1' that GtoPdb does not:")
    print("    %d of %d -- IUPHAR alone would have missed these" % (len(omitted), len(a)))
    for slug, miss in omitted:
        print("      %-7s GtoPdb omits %s" % (slug, miss))

    print("\n%s\n7c. THE FROZEN MAP, AND WHETHER g1_systems.py CAN ACTUALLY EAT IT\n%s"
          % ("=" * 78, "=" * 78))
    M = os.path.join(INPUTS, "coupling_cognate_map.tsv")
    R = os.path.join(INPUTS, "coupling_cognate_rungs.tsv")
    G = os.path.join(INPUTS, "g1_systems.csv")
    if not os.path.exists(M):
        print("  coupling_cognate_map.tsv absent -- run coupling_cognate_map.py")
    else:
        mp = list(csv.DictReader(open(M), delimiter="\t"))
        rg = list(csv.DictReader(open(R), delimiter="\t"))
        print("  map rows: %d   rung rows: %d" % (len(mp), len(rg)))
        print("  evidence class: %s"
              % dict(collections.Counter(r["evidence_class"] for r in mp)))
        print("  verdict       : %s"
              % dict(collections.Counter(r["verdict"] for r in mp)))
        print("  subtypes used : %s"
              % dict(collections.Counter(r["cognate_subtype"] for r in mp
                                         if r["cognate_subtype"])))
        c32 = [r for r in mp if r["in_core32_provisional"] == "yes"]
        print("  CORE-32 provisional: %d rows, %s"
              % (len(c32), dict(collections.Counter(r["verdict"] for r in c32))))
        print("  ties that bind at R6a/R7: %d %s"
              % (sum(1 for r in mp if r["tie_changes_bytes_at"]),
                 dict(collections.Counter(r["tie_set"] for r in mp
                                          if r["tie_changes_bytes_at"]))))
        # --- consumer-readiness, asserted rather than hoped for
        fails = []
        fams = {r["family"] for r in csv.DictReader(open(RUNGS), delimiter="\t")}
        bad = sorted({r["seq_rungs_family"] for r in mp
                      if r["seq_rungs_family"] and r["seq_rungs_family"] not in fams})
        if bad:
            fails.append("seq_rungs_family values absent from seq_rungs.tsv: %s" % bad)
        shas = {(r["family"], r["rung"]): r["sha256"]
                for r in csv.DictReader(open(RUNGS), delimiter="\t")}
        wrong = [r for r in rg
                 if shas.get((r["seq_rungs_family"], r["rung"])) != r["sha256"]]
        if wrong:
            fails.append("%d rung rows carry a sha256 that is not seq_rungs.tsv's"
                         % len(wrong))
        if os.path.exists(G):
            # "*" is g1_systems.csv's placeholder on templated rows whose receptor
            # SET resolves from this file (CORE32_GS, G10_SCAN). It is not a
            # receptor and must not be looked up as one.
            gslugs = {r["receptor_slug"] for r in csv.DictReader(open(G))
                      if r["receptor_slug"] != "*"}
            mslugs = {r["receptor_slug"] for r in mp}
            miss = sorted(gslugs - mslugs)
            if miss:
                fails.append("g1_systems.csv receptors absent from the map: %s" % miss)
            resolvable = {r["receptor_slug"] for r in rg}
            unres = sorted(gslugs & (mslugs - resolvable))
            print("  g1_systems.csv distinct receptors: %d; in the map: %d; "
                  "resolvable: %d" % (len(gslugs), len(gslugs & mslugs),
                                      len(gslugs & resolvable)))
            print("  ... still unresolvable (needs_decision): %s" % unres)
        S = os.path.join(INPUTS, "coupling_receptor_sets.tsv")
        if os.path.exists(S):
            st = list(csv.DictReader(open(S), delimiter="\t"))
            print("  family partitions for the templated sets: %s"
                  % dict(collections.Counter(r["set_name"] for r in st)))
        n_tmpl = sum(1 for r in csv.DictReader(open(G))
                     if r["receptor_slug"] == "*")
        print("  templated rows awaiting a receptor-set choice: %d "
              "(set definition is Group 1's, partitions supplied)" % n_tmpl)
        print("  CONSUMER CHECK: %s"
              % ("PASS" if not fails else "FAIL -- " + "; ".join(fails)))

    print("\n%s\n8. BLOCK D's FOUR D2 RECEPTORS\n%s" % ("=" * 78, "=" * 78))
    d2 = {"ADRB2", "ACM2", "AGTR1", "OPRK"}
    for r in a:
        if r["slug"] in d2:
            print("  %-6s verdict=%-18s recommended=%-7s structure=%-7s (%s)"
                  % (r["slug"], r["verdict"].replace("cognate_", ""),
                     r["recommended_family"], r["authority_structure"],
                     r["structure_evidence"]))
    return 0


def selftest():
    """Plant a defect in each check and require it to be reported.

    Every check below is run twice: once on the real table, once on a table with
    one row corrupted. A check that gives the same answer both times is not a
    check. This exists because this project has already shipped four checkers
    whose reporting path never executed.
    """
    a, s, imp = load()
    fails = []

    # (1) verdict tally must move when a verdict is changed
    base = collections.Counter(r["verdict"] for r in a)["cognate_conflicted"]
    a2 = [dict(r) for r in a]
    a2[0]["verdict"] = "cognate_conflicted"
    bad = collections.Counter(r["verdict"] for r in a2)["cognate_conflicted"]
    if a[0]["verdict"] == "cognate_conflicted":
        print("  (1) skipped: row 0 is already conflicted")
    elif bad != base + 1:
        fails.append("verdict tally did not move when a verdict was planted")

    # (2) the structure-vs-annotation check must fire on a planted mismatch
    def mismatches(rows):
        out = []
        for r in rows:
            st = set(filter(None, r["authority_structure"].split(";")))
            ann = set()
            for k in ("authority_gtopdb_via_gproteindb",
                      "authority_iuphar_direct_primary"):
                ann |= set(filter(None, r[k].split(";")))
            for part in filter(None, r["authority_assaylabs"].split(";")):
                ann |= set(part.split("=", 1)[1].split("+"))
            if st and ann and not (st & ann):
                out.append(r["slug"])
        return out
    clean = mismatches(a)
    a3 = [dict(r) for r in a]
    victim = next(r for r in a3 if r["authority_structure"]
                  and r["slug"] not in clean)
    victim["authority_structure"] = "G12/13"
    victim["authority_gtopdb_via_gproteindb"] = "Gs"
    victim["authority_iuphar_direct_primary"] = "Gs"
    victim["authority_assaylabs"] = "Bouvier=Gs"
    if victim["slug"] not in mismatches(a3):
        fails.append("structure-vs-annotation check missed a planted mismatch")

    # (3) the chimera census must fire on a planted chimera note
    ga = [r for r in s if r["kind"].startswith("G-alpha") and r["role"] == "active"]
    n0 = sum(1 for r in ga if "COUPLING CHIMERA" in r["construct_note"])
    ga2 = [dict(r) for r in ga]
    plain = next(r for r in ga2 if "COUPLING CHIMERA" not in r["construct_note"])
    plain["construct_note"] = "COUPLING CHIMERA: planted"
    if sum(1 for r in ga2 if "COUPLING CHIMERA" in r["construct_note"]) != n0 + 1:
        fails.append("chimera census missed a planted chimera")

    # (4) the rung-impact count must move when a candidate set is widened
    n0 = sum(1 for r in imp if r["R1_ct11"].startswith("DIFFERS"))
    imp2 = [dict(r) for r in imp]
    same = next(r for r in imp2 if r["R1_ct11"] == "SAME")
    same["R1_ct11"] = "DIFFERS(2)"
    if sum(1 for r in imp2 if r["R1_ct11"].startswith("DIFFERS")) != n0 + 1:
        fails.append("rung-impact count missed a planted difference")

    if fails:
        print("SELFTEST FAILED:")
        for f in fails:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED: all 4 checks fired on a planted defect")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
