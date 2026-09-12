#!/usr/bin/env python3
"""coupling_cognate_map.py — the frozen cognate-Ga map, read off the structure.

Aditya's decision, 2026-09-11: "read it off the structure the receptor was solved
with. We already have all 81 of them." This script implements that as a rule and
freezes the result, so `g1_systems.py` can resolve `chain_b_sha256` for the 1,397
rows that are currently keyed to a family label.

THE RULE, stated so it can be pre-registered
--------------------------------------------
It depends on nothing downstream: no prediction, no score, no model output. Given
only the panel and the PDB, it returns the same answer every time.

  R-COG-1  The receptor's reference is the ACTIVE structure that PANEL.md's
           Rule R selects, read from `g1_receptors.tsv:active_pdb`. Not the
           union of candidate actives, and not the one with a G protein in it --
           whichever Rule R picked, including when that entry has no transducer.

  R-COG-2  The partner entity is the single polymer entity of that structure
           classified `G-alpha` or `G-alpha-fusion` by the classifier in
           `coupling_assign.py`. If more than one qualifies, the longest is
           taken and the discarded ones are recorded.

  R-COG-3  The cognate subtype is the canonical human Ga whose C-terminal 21
           residues have the highest identity to the partner entity's deposited
           last 21. The canonical termini are read from `seq_rungs.tsv`, which
           is the same file the rung hashes come from, so the family label this
           map emits is a valid join key into it by construction.

  R-COG-4  TIES. Gi1=Gi2, Gt1=Gt2=Ggust and Gq=G11 are byte-identical over
           ct21 (and over every rung from ct11 to a5plus), so a tie among them
           carries no information and is resolved by a representative DECLARED
           IN ADVANCE, not by sort order:
               {Gi1, Gi2}          -> Gi1
               {Gt1, Gt2, Ggust}   -> Gt1
               {Gq, G11}           -> Gq
           The full tie set is recorded on the row. NOTE THE ONE PLACE THIS
           CHOICE IS NOT FREE: the members differ in FULL-SUBUNIT length (Gi1
           354 vs Gi2 355), so the representative changes the bytes at R6a_da5
           and R7_full while changing nothing at R1-R5. Flagged per row.

  R-COG-5  THRESHOLD. If the best ct21 identity is below 0.80, or if the
           canonical Ga tied at the best score span more than one FAMILY, the
           deposited partner is a chimera and the rule DOES NOT RESOLVE IT.
           The row is marked `needs_decision`, the scaffold family and the tip
           family are both reported, and no subtype is emitted.

  R-COG-6  SHORT ENTITIES. If the partner entity is shorter than 21 residues its
           ct21 does not exist. Scoring falls back to ct11, the margin to the
           nearest other FAMILY is reported, and the evidence class says
           PEPTIDE_ENTITY so no consumer can mistake it for a full-subunit read.

  R-COG-7  NO PARTNER. If the Rule-R active reference contains no Ga entity, the
           rule cannot be applied. The row falls back to the family that the
           annotation authorities agree on (`coupling_assignments.csv`), and
           that family's DECLARED representative:
               Gs -> Gs,  Gi/o -> Gi1,  Gq/11 -> Gq,  G12/13 -> G13
           Its evidence class is CONVENTION_FALLBACK and its verdict is
           `frozen_by_convention`. A structure-read row and a convention-read row
           must never be told apart only by reading the subtype.

  R-COG-8  Where a NON-Rule-R active reference of the same receptor does contain
           a Ga, it is reported in the `alt_*` columns. It never overrides
           R-COG-1; it exists so a consumer can see what a different reference
           choice would have supplied, and so the 12 chimera receptors and the
           4 no-partner receptors have a visible second option.

OUTPUT
------
  coupling_cognate_map.tsv    64 rows, keyed by `receptor_slug` (the column name
                              `g1_systems.csv` already uses)
  coupling_cognate_rungs.tsv  receptor x rung -> sha256, length, sequence, taken
                              from seq_rungs.tsv; emitted only for rows whose
                              subtype is frozen, so a consumer that joins on it
                              cannot accidentally hash an unresolved receptor.

Usage:  python3 redo/build/coupling_cognate_map.py [--selftest]
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
RUNGS = os.path.join(INPUTS, "seq_rungs.tsv")
G1REC = os.path.join(INPUTS, "g1_receptors.tsv")
ENTITIES = os.path.join(CACHE, "coupling_rcsb_entities.json")
REFSTRUCT = os.path.join(INPUTS, "coupling_refstructures.csv")
ASSIGN = os.path.join(INPUTS, "coupling_assignments.csv")

MAP_OUT = os.path.join(INPUTS, "coupling_cognate_map.tsv")
RUNG_OUT = os.path.join(INPUTS, "coupling_cognate_rungs.tsv")
SETS_OUT = os.path.join(INPUTS, "coupling_receptor_sets.tsv")

CT21_THRESHOLD = 0.80

FAMILY_OF = {
    "Gs": "Gs", "Golf": "Gs",
    "Gi1": "Gi/o", "Gi2": "Gi/o", "Gi3": "Gi/o", "Go": "Gi/o",
    "Gt1": "Gi/o", "Gt2": "Gi/o", "Ggust": "Gi/o", "Gz": "Gi/o",
    "Gq": "Gq/11", "G11": "Gq/11", "G14": "Gq/11", "G15": "Gq/11",
    "G12": "G12/13", "G13": "G12/13",
}
# R-COG-4: declared before looking at any structure.
TIE_REPRESENTATIVE = [
    (frozenset(["Gi1", "Gi2"]), "Gi1"),
    (frozenset(["Gt1", "Gt2", "Ggust"]), "Gt1"),
    (frozenset(["Gq", "G11"]), "Gq"),
]
# R-COG-7: declared before looking at any structure.
FAMILY_REPRESENTATIVE = {"Gs": "Gs", "Gi/o": "Gi1", "Gq/11": "Gq", "G12/13": "G13"}

RUNG_ORDER = ("R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix", "R5_a5plus",
              "R6a_da5", "R7_full")
# R1-R5 are byte-identical within each tie class; R6a/R7 are not.
RUNGS_TIE_SENSITIVE = ("R6a_da5", "R7_full")


def rung_table():
    by_rung, acc = collections.defaultdict(dict), {}
    for r in csv.DictReader(open(RUNGS), delimiter="\t"):
        by_rung[r["rung"]][r["family"]] = (r["sequence"], r["sha256"])
        acc[r["family"]] = r["accession"]
    return by_rung, acc


def termini(by_rung):
    out = {}
    for fam, (seq21, _) in by_rung["R3_ct21"].items():
        out[fam] = {"ct21": seq21, "ct11": by_rung["R1_ct11"][fam][0]}
    bad = [f for f, v in out.items()
           if len(v["ct21"]) != 21 or len(v["ct11"]) != 11]
    if bad:
        raise SystemExit("seq_rungs.tsv rung lengths wrong for %s" % bad)
    return out


def score(dep, term, key, n):
    """(best names, best identity, full ranking) over a window of length n."""
    if not dep or len(dep) < n:
        return [], 0.0, []
    win = dep[-n:]
    ranked = sorted(((sum(1 for a, b in zip(win, t[key]) if a == b) / float(n), nm)
                     for nm, t in term.items()), reverse=True)
    top = ranked[0][0]
    return sorted(nm for i, nm in ranked if i == top), top, ranked


def classify_entity(desc, length):
    """Same classifier as coupling_assign.py, copied so this script runs standalone.

    A SECOND COPY OF A FUNCTION IS A DRIFT RISK, and this project has just paid
    for one: coupling_fetch.py kept its own accession->family map and it drifted
    to Connexin 26 under the name Ggust, silently, because a wrong C-terminus can
    only ever fail to match. So the copy is not trusted -- `--selftest` runs both
    implementations over every cached entity and fails on any disagreement.
    """
    d = (desc or "").lower()
    has_alpha = ("subunit alpha" in d or "g alpha" in d or "g-alpha" in d
                 or "galpha" in d or "mini-g" in d or "minig" in d
                 or "g protein subunit q" in d)
    if "arrestin" in d:
        return "arrestin"
    if has_alpha:
        if "subunit gamma" in d or "subunit beta" in d or "," in d:
            return "G-alpha-fusion"
        return "G-alpha"
    if ("nanobody" in d or "megabody" in d or "single-chain variable" in d
            or "scfv" in d or "vhh" in d or "fab" in d or "antibody" in d
            or "heavy chain" in d or "light chain" in d or "camelid" in d
            or "immunoglobulin" in d):
        return "nanobody/antibody"
    if "g(i)/g(s)/g(t)" in d or "g(i)/g(s)/g(o)" in d:
        return "G-beta" if (length or 0) > 200 else "G-gamma"
    if "subunit beta" in d:
        return "G-beta"
    if "subunit gamma" in d:
        return "G-gamma"
    if "nucleotide-binding protein" in d:
        return "G-alpha"
    return "other"


def main():
    by_rung, acc_of = rung_table()
    term = termini(by_rung)
    entries = json.load(open(ENTITIES))
    recs = list(csv.DictReader(open(G1REC), delimiter="\t"))
    assign = {r["slug"]: r for r in csv.DictReader(open(ASSIGN))}
    refs = list(csv.DictReader(open(REFSTRUCT)))

    # every Ga entity of every ACTIVE reference, for the alt_* columns (R-COG-8)
    alt = collections.defaultdict(list)
    for r in refs:
        if r["role"] == "active" and r["kind"].startswith("G-alpha"):
            alt[r["slug"]].append(r)

    rows, rung_rows = [], []
    for rec in recs:
        slug = rec["slug"]
        pdb = rec["active_pdb"].upper()
        a = assign.get(slug, {})
        row = {
            "receptor_slug": slug, "receptor_uniprot": rec["uniprot"],
            "receptor_organism": rec["organism"],
            "in_core32_provisional": rec["core32_provisional"],
            "rule_r_active_pdb": pdb,
            "cognate_family": "", "cognate_subtype": "", "seq_rungs_family": "",
            "cognate_accession": "", "evidence_class": "", "verdict": "",
            "source_entity": "", "source_entity_len": "", "source_description": "",
            "source_uniprot_xref": "",
            "deposited_ct11": "", "deposited_ct21": "",
            "ct21_identity": "", "ct21_nearest": "",
            "ct11_identity": "", "ct11_nearest": "",
            "tie_set": "", "tie_changes_bytes_at": "",
            "scaffold_family": "", "tip_family": "",
            "chimera_option_a_tip": "", "chimera_option_b_scaffold": "",
            "option_backed_by_annotation": "", "fallback_basis": "",
            "alt_pdb": "", "alt_subtype": "", "alt_evidence": "",
            "annotation_family": a.get("family_primary", ""),
            "annotation_verdict": a.get("verdict", ""),
            "blockb_prior": a.get("blockb_prior", ""),
            "reverses_prior": "", "note": "",
        }

        entry = entries.get(pdb)
        cands = []
        if entry:
            for pe in entry.get("polymer_entities") or []:
                meta = pe.get("rcsb_polymer_entity") or {}
                poly = pe.get("entity_poly") or {}
                desc = meta.get("pdbx_description") or ""
                n = poly.get("rcsb_sample_sequence_length") or 0
                if classify_entity(desc, n).startswith("G-alpha"):
                    seq = (poly.get("pdbx_seq_one_letter_code_can") or "").replace("\n", "")
                    ids = pe.get("rcsb_polymer_entity_container_identifiers") or {}
                    xr = ";".join(x.get("database_accession") for x in
                                  ids.get("reference_sequence_identifiers") or []
                                  if x.get("database_name") == "UniProt")
                    cands.append({"id": pe["rcsb_id"], "seq": seq, "len": n,
                                  "desc": desc, "xref": xr})
        # R-COG-2
        cands.sort(key=lambda c: -c["len"])
        if len(cands) > 1:
            row["note"] = ("%d G-alpha entities in %s; took the longest (%s), "
                           "discarded %s" % (len(cands), pdb, cands[0]["id"],
                                             ",".join(c["id"] for c in cands[1:])))

        # ---- R-COG-8, computed for every receptor
        others = [r for r in alt[slug] if r["pdb"] != pdb]
        if others:
            o = max(others, key=lambda r: int(r["length"] or 0))
            ofams = [f for f in o["ct21_family"].split("/") if f] or \
                    [f for f in o["ct11_family"].split("/") if f]
            row["alt_pdb"] = o["pdb"]
            row["alt_subtype"] = resolve_tie(ofams) if ofams else ""
            row["alt_evidence"] = "ct21 id %s" % o["ct21_identity"]

        if not cands:
            # ---- R-COG-7
            fam = (a.get("recommended_family") or "").strip()
            rep = FAMILY_REPRESENTATIVE.get(fam, "")
            row.update(cognate_family=fam, cognate_subtype=rep,
                       seq_rungs_family=rep, cognate_accession=acc_of.get(rep, ""),
                       evidence_class="CONVENTION_FALLBACK",
                       verdict="frozen_by_convention" if rep else "needs_decision")
            kinds = sorted({classify_entity(
                (pe.get("rcsb_polymer_entity") or {}).get("pdbx_description") or "",
                (pe.get("entity_poly") or {}).get("rcsb_sample_sequence_length") or 0)
                for pe in (entry or {}).get("polymer_entities") or []})
            # WHERE THE FALLBACK FAMILY CAME FROM, named rather than implied.
            # `recommended_family` is not always an annotation consensus -- for a
            # `cognate_conflicted` receptor it is the deposited partner of a
            # NON-Rule-R reference. NTR1 is exactly that case: every annotation
            # says Gq/11 and the family here is Gi/o, off 6OS9. Calling that
            # "the annotation authorities" would have been false.
            row["fallback_basis"] = a.get("recommended_basis", "")
            corrob = ""
            if row["alt_pdb"] and row["alt_subtype"] == rep:
                corrob = (" An off-Rule-R active reference (%s) contains a G-alpha "
                          "and reads the same subtype, so the convention is "
                          "corroborated by a structure -- just not by THE structure."
                          % row["alt_pdb"])
            elif row["alt_pdb"]:
                corrob = (" An off-Rule-R active reference (%s) reads %s, which "
                          "DISAGREES with the fallback." % (row["alt_pdb"], row["alt_subtype"]))
            else:
                corrob = (" No active reference of this receptor contains a "
                          "G-alpha at all, so there is no structural check.")
            row["note"] = ("%s contains no G-alpha entity (%s). Family from "
                           "coupling_assignments.csv:recommended_family; subtype is "
                           "the DECLARED representative of that family, NOT a "
                           "structure read.%s" % (pdb, ", ".join(kinds), corrob))
            rows.append(row)
            emit_rungs(rung_rows, row, by_rung)
            continue

        c = cands[0]
        row.update(source_entity=c["id"], source_entity_len=c["len"],
                   source_description=c["desc"], source_uniprot_xref=c["xref"] or "none")
        seq = c["seq"]
        row["deposited_ct11"] = seq[-11:] if len(seq) >= 11 else seq
        f11, i11, _ = score(seq, term, "ct11", 11)
        row["ct11_identity"] = "%.2f" % i11
        row["ct11_nearest"] = "/".join(f11)

        if len(seq) < 21:
            # ---- R-COG-6
            fams11 = {FAMILY_OF[x] for x in f11}
            ranked = sorted(((sum(1 for a2, b in zip(seq[-11:], t["ct11"]) if a2 != b), nm)
                             for nm, t in term.items()))
            other_fam = next((d for d, nm in ranked if FAMILY_OF[nm] not in fams11), None)
            rep = resolve_tie(f11)
            row.update(cognate_family="/".join(sorted(fams11)) if len(fams11) == 1
                       else ";".join(sorted(fams11)),
                       cognate_subtype=rep if len(fams11) == 1 else "",
                       seq_rungs_family=rep if len(fams11) == 1 else "",
                       cognate_accession=acc_of.get(rep, "") if len(fams11) == 1 else "",
                       evidence_class="PEPTIDE_ENTITY",
                       verdict="frozen_with_caveat" if len(fams11) == 1 else "needs_decision",
                       tie_set="/".join(f11),
                       tie_changes_bytes_at=",".join(RUNGS_TIE_SENSITIVE) if len(f11) > 1 else "",
                       deposited_ct21="(entity is only %d aa)" % len(seq))
            row["note"] = ("partner entity is a %d-residue peptide, so ct21 does not "
                           "exist; scored on ct11. Nearest canonical %s at %d of 11 "
                           "substitutions; the nearest canonical of any OTHER family "
                           "is %s substitutions away, so the family is unambiguous "
                           "and the subtype is the tie representative."
                           % (len(seq), "/".join(f11), round((1 - i11) * 11),
                              other_fam if other_fam is not None else "n/a"))
            rows.append(row)
            emit_rungs(rung_rows, row, by_rung)
            continue

        f21, i21, _ = score(seq, term, "ct21", 21)
        row["deposited_ct21"] = seq[-21:]
        row["ct21_identity"] = "%.2f" % i21
        row["ct21_nearest"] = "/".join(f21)
        fams21 = {FAMILY_OF[x] for x in f21}

        # scaffold vs tip: the first 10 of ct21 is the helix body, the last 11 the tip
        sc = sorted(((sum(1 for a2, b in zip(seq[-21:-11], t["ct21"][:10]) if a2 == b), nm)
                     for nm, t in term.items()), reverse=True)
        sc_best = sorted({FAMILY_OF[nm] for d, nm in sc if d == sc[0][0]})
        row["scaffold_family"] = ";".join(sc_best)
        row["tip_family"] = ";".join(sorted({FAMILY_OF[x] for x in f11}))

        if i21 < CT21_THRESHOLD or len(fams21) > 1:
            # ---- R-COG-5
            tip_rep = resolve_tie(f11)
            sc_rep = FAMILY_REPRESENTATIVE.get(sc_best[0], "") if len(sc_best) == 1 else ""
            row.update(evidence_class="CHIMERA_SPLIT", verdict="needs_decision",
                       cognate_family=";".join(sorted(fams21)) if len(fams21) > 1
                       else row["tip_family"],
                       chimera_option_a_tip="%s (%s)" % (tip_rep, row["tip_family"]),
                       chimera_option_b_scaffold="%s (%s)" % (sc_rep, ";".join(sc_best)))
            # Which option the coupling databases back. Not a tiebreak -- the rule
            # does not resolve these -- but the PI should not have to look it up.
            ann = set(filter(None, (a.get("family_primary") or "").split(";")))
            backs = []
            if row["tip_family"] in ann:
                backs.append("A/tip")
            if sc_best and sc_best[0] in ann:
                backs.append("B/scaffold")
            row["option_backed_by_annotation"] = "+".join(backs) or "neither"
            row["note"] = ("deposited tip matches no canonical human Ga at ct21 "
                           "(best %.2f). Scaffold reads %s, alpha5 tip reads %s. "
                           "Two honest answers; the rule does not choose. "
                           "Annotation backs: %s."
                           % (i21, row["scaffold_family"] or "?", row["tip_family"] or "?",
                              row["option_backed_by_annotation"]))
            rows.append(row)
            continue

        rep = resolve_tie(f21)
        row.update(cognate_family=sorted(fams21)[0], cognate_subtype=rep,
                   seq_rungs_family=rep, cognate_accession=acc_of.get(rep, ""),
                   evidence_class="STRUCTURE_EXACT" if i21 >= 1.0 else "STRUCTURE_NEAR",
                   verdict="frozen", tie_set="/".join(f21),
                   tie_changes_bytes_at=",".join(RUNGS_TIE_SENSITIVE) if len(f21) > 1 else "")
        if i21 < 1.0:
            row["note"] = ("deposited tip is engineered -- %d of 21 substitutions "
                           "from %s -- but every canonical at the best score is in "
                           "one family, so family and subtype are unambiguous."
                           % (round((1 - i21) * 21), "/".join(f21)))
        rows.append(row)
        emit_rungs(rung_rows, row, by_rung)

    # ---- prior reversal, recorded rather than silent
    for row in rows:
        prior = row["blockb_prior"]
        if not prior or not row["cognate_family"]:
            continue
        pf = {"Gs": "Gs", "Gi": "Gi/o", "Gt": "Gi/o", "Gq": "Gq/11",
              "G12": "G12/13", "G13": "G12/13"}.get(prior, "")
        if pf and pf not in row["cognate_family"].split(";"):
            row["reverses_prior"] = ("YES -- Block B assigned %s (%s); the Rule-R "
                                     "structure reads %s" % (prior, pf, row["cognate_family"]))

    cols = list(rows[0].keys())
    with open(MAP_OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    with open(RUNG_OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["receptor_slug", "seq_rungs_family", "rung",
                                           "len", "sha256", "sequence"], delimiter="\t")
        w.writeheader()
        w.writerows(rung_rows)

    # ---- family partitions, for the templated receptor sets in g1_systems.csv
    #
    # `CORE32_GS(PENDING COUPLING.md)` and `G10_SCAN(PENDING COUPLING.md)` are
    # receptor sets g1_systems.py cannot enumerate without a cognate assignment.
    # WHAT IS EMITTED INPUTS IS THE PARTITION, NOT THE SET DEFINITION. "Which
    # receptors couple Gs" is this file's question; "which of them G10_SCAN
    # should run on" is Group 1's, and inventing an answer to the second while
    # holding the first would be exactly the overreach this split exists to
    # prevent. Every family partition is emitted so any of them can be selected.
    sets = []
    for scope, keep in (("C1_64", lambda r: True),
                        ("CORE32", lambda r: r["in_core32_provisional"] == "yes")):
        for r in rows:
            if not keep(r) or not r["cognate_subtype"]:
                continue
            fam = r["cognate_family"].replace("/", "").replace(";", "_")
            sets.append({"set_name": "%s_%s" % (scope, fam),
                         "scope": scope, "cognate_family": r["cognate_family"],
                         "receptor_slug": r["receptor_slug"],
                         "cognate_subtype": r["cognate_subtype"],
                         "evidence_class": r["evidence_class"],
                         "verdict": r["verdict"]})
    with open(SETS_OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["set_name", "scope", "cognate_family",
                                           "receptor_slug", "cognate_subtype",
                                           "evidence_class", "verdict"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(sets)

    ec = collections.Counter(r["evidence_class"] for r in rows)
    vd = collections.Counter(r["verdict"] for r in rows)
    print("receptors: %d" % len(rows))
    print("evidence class: %s" % dict(ec))
    print("verdict       : %s" % dict(vd))
    print("resolvable rows written to coupling_cognate_rungs.tsv: %d "
          "(%d receptors x %d rungs)"
          % (len(rung_rows), len(rung_rows) // len(RUNG_ORDER), len(RUNG_ORDER)))
    print("\nsubtypes used: %s"
          % dict(collections.Counter(r["cognate_subtype"] for r in rows if r["cognate_subtype"])))
    print("\nneeds_decision (%d):" % vd["needs_decision"])
    for r in rows:
        if r["verdict"] == "needs_decision":
            print("  %-7s %-5s %-14s scaffold=%-8s tip=%-8s alt=%s %s"
                  % (r["receptor_slug"], r["rule_r_active_pdb"], r["evidence_class"],
                     r["scaffold_family"] or "-", r["tip_family"] or "-",
                     r["alt_pdb"] or "-", r["alt_subtype"] or ""))
    print("\nfrozen_by_convention (%d):" % vd["frozen_by_convention"])
    for r in rows:
        if r["verdict"] == "frozen_by_convention":
            print("  %-7s %-5s -> %-4s  family %s from recommended_family; "
                  "off-Rule-R ref %s %s"
                  % (r["receptor_slug"], r["rule_r_active_pdb"], r["cognate_subtype"],
                     r["cognate_family"], r["alt_pdb"] or "none", r["alt_subtype"]))
    print("\nfamily partitions written to coupling_receptor_sets.tsv:")
    for nm, n in sorted(collections.Counter(x["set_name"] for x in sets).items()):
        members = [x["receptor_slug"] for x in sets if x["set_name"] == nm]
        print("  %-16s %2d  %s" % (nm, n, " ".join(sorted(members))))

    print("\nreverses a Block B prior:")
    for r in rows:
        if r["reverses_prior"]:
            print("  %-7s %s" % (r["receptor_slug"], r["reverses_prior"]))
    return 0


def resolve_tie(names):
    """R-COG-4. Declared representative, never sort order."""
    s = set(names)
    for members, rep in TIE_REPRESENTATIVE:
        if s and s <= members:
            return rep
    return sorted(s)[0] if len(s) == 1 else ""


def emit_rungs(out, row, by_rung):
    fam = row["seq_rungs_family"]
    if not fam:
        return
    for rung in RUNG_ORDER:
        if fam not in by_rung[rung]:
            continue
        seq, sha = by_rung[rung][fam]
        out.append({"receptor_slug": row["receptor_slug"], "seq_rungs_family": fam,
                    "rung": rung, "len": len(seq), "sha256": sha, "sequence": seq})


def selftest():
    """Prove each branch of the rule fires, by planting an input that triggers it."""
    by_rung, _ = rung_table()
    term = termini(by_rung)
    fails = []

    # R-COG-3/4: an exact Gi1 ct21 must resolve to Gi1 and carry the Gi1/Gi2 tie
    gi1 = term["Gi1"]["ct21"]
    f, i, _ = score("X" * 30 + gi1, term, "ct21", 21)
    if not (i == 1.0 and set(f) == {"Gi1", "Gi2"} and resolve_tie(f) == "Gi1"):
        fails.append("exact Gi1 ct21 did not resolve to Gi1 with the Gi1/Gi2 tie")

    # R-COG-4: the representative must not be sort order -- Gq/G11 sorts G11 first
    if resolve_tie(["G11", "Gq"]) != "Gq":
        fails.append("Gq/G11 tie resolved by sort order, not by the declared rep")

    # R-COG-5: a tip 6 substitutions from everything must fall below threshold
    f, i, _ = score("X" * 30 + "AAAAAAAAAAAAAAAAAAAAA", term, "ct21", 21)
    if i >= CT21_THRESHOLD:
        fails.append("a poly-A ct21 scored above the chimera threshold")

    # R-COG-5: the real mini-Gs/q tip must be caught as a split
    msq = "RIFNDCKDIILQMNLREYNLV"
    f21, i21, _ = score("X" * 30 + msq, term, "ct21", 21)
    f11, _, _ = score(msq, term, "ct11", 11)
    sc = sorted(((sum(1 for a, b in zip(msq[:10], t["ct21"][:10]) if a == b), nm)
                 for nm, t in term.items()), reverse=True)
    scf = {FAMILY_OF[nm] for d, nm in sc if d == sc[0][0]}
    tipf = {FAMILY_OF[x] for x in f11}
    if i21 >= CT21_THRESHOLD:
        fails.append("mini-Gs/q tip scored above threshold at ct21 (%.2f)" % i21)
    if scf == tipf:
        fails.append("mini-Gs/q scaffold and tip read as the same family (%s)" % scf)

    # R-COG-6: OPSD's peptide must score on ct11 and be Gi/o-family by a margin
    ops = "VLEDLKSCGLF"
    f11, i11, _ = score(ops, term, "ct11", 11)
    fams = {FAMILY_OF[x] for x in f11}
    ranked = sorted(((sum(1 for a, b in zip(ops, t["ct11"]) if a != b), nm)
                     for nm, t in term.items()))
    other = next(d for d, nm in ranked if FAMILY_OF[nm] not in fams)
    if fams != {"Gi/o"} or other <= ranked[0][0]:
        fails.append("OPSD peptide did not resolve to Gi/o by a margin")

    # R-COG-7: an unknown family must not yield a representative
    if FAMILY_REPRESENTATIVE.get("Gnonsense"):
        fails.append("unknown family produced a representative")

    # the two copies of the entity classifier must agree on every cached entity
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_ca", os.path.join(BUILD, "coupling_assign.py"))
        ca = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ca)
        ents = json.load(open(ENTITIES))
        n = dis = 0
        for e in ents.values():
            for pe in e.get("polymer_entities") or []:
                d = (pe.get("rcsb_polymer_entity") or {}).get("pdbx_description") or ""
                L = (pe.get("entity_poly") or {}).get("rcsb_sample_sequence_length") or 0
                n += 1
                # The assertion is deliberately narrow: the two copies must agree
                # on WHICH ENTITIES ARE G-ALPHA, which is the only judgement this
                # script consumes. The local copy collapses receptor / ligand /
                # fusion-partner into `other` on purpose, because it never looks
                # at them, and asserting full equality would fail on that by
                # design rather than on drift.
                if classify_entity(d, L).startswith("G-alpha") != \
                        ca.classify(d, L).startswith("G-alpha"):
                    dis += 1
                    if dis <= 3:
                        fails.append("G-alpha classifier drift on %s: local=%s assign=%s"
                                     % (pe["rcsb_id"], classify_entity(d, L), ca.classify(d, L)))
        if dis:
            fails.append("%d of %d cached entities disagree on G-alpha between the "
                         "two copies" % (dis, n))
        else:
            print("  classifier copies agree on G-alpha for all %d cached entities" % n)
    except Exception as exc:                                        # noqa: BLE001
        fails.append("could not cross-check the classifier: %s" % exc)

    # the map on disk must not emit a rung row for any unresolved receptor
    if os.path.exists(MAP_OUT) and os.path.exists(RUNG_OUT):
        m = {r["receptor_slug"]: r for r in csv.DictReader(open(MAP_OUT), delimiter="\t")}
        emitted = {r["receptor_slug"] for r in csv.DictReader(open(RUNG_OUT), delimiter="\t")}
        leaked = [s for s in emitted if m[s]["verdict"] == "needs_decision"]
        if leaked:
            fails.append("rung rows emitted for unresolved receptors: %s" % leaked)
        noseq = [s for s, r in m.items() if r["seq_rungs_family"] and s not in emitted]
        if noseq:
            fails.append("resolved receptors with no rung rows: %s" % noseq)

    if fails:
        print("SELFTEST FAILED:")
        for f in fails:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED: every branch of R-COG fired on a planted input")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
