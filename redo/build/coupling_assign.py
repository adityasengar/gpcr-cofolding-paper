#!/usr/bin/env python3
"""Merge the three coupling authorities into one per-receptor verdict table.

Reads what coupling_fetch.py cached; writes coupling_refstructures.csv (re-derived,
with the entity classifier corrected), coupling_assignments.csv and
coupling_rung_impact.csv. No network. No file outside coupling_* is touched.

THE THREE THINGS THIS SCRIPT REFUSES TO DO
------------------------------------------
1. It does not pick a winner when authorities disagree. `primary_family_annot`
   is a SET, and a receptor with two entries in it is `cognate_conflicted`, not
   quietly resolved to the most common one.
2. It does not read a partner's family from its UniProt cross-reference.
   Mini-G constructs are coupling chimeras by construction -- a mini-Gs scaffold
   carrying another family's alpha5 -- so the accession names the scaffold and
   the C-terminus names the coupling. Ten of the C1 active references carry one.
3. It does not break Gi1/Gi2, Gq/G11 or Gt1/Gt2/Ggust ties. Those are
   byte-identical over every peptide rung (verified against seq_rungs.tsv), so a
   subtype call there would be manufactured.

WHY THE SCORING WINDOW IS 11 AND NOT 21. verify_alpha5ct_family.py scores the
last 21 because that is the length the paper's title claims. That window is the
wrong one for mini-G chimeras: the published mini-Gs/q and mini-Gs/i constructs
graft only the last ~5-12 residues onto a Gs scaffold, so at 21 they score ~0.62
against every family and fall out as UNRECOGNISED. Ten C1 references do exactly
that. This script scores BOTH windows and reports both, and calls the family
from the 11 -- which is also the rung the ladder's shortest peptide uses.
"""
import collections
import csv
import json
import os
import re
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
ROOT = os.path.dirname(os.path.dirname(INPUTS))          # .../paper

PANEL = os.path.join(INPUTS, "panel_systems.csv")
RUNGS = os.path.join(INPUTS, "seq_rungs.tsv")
ENTITIES = os.path.join(CACHE, "coupling_rcsb_entities.json")
TERMINI = os.path.join(CACHE, "coupling_family_termini.json")
GPDB = os.path.join(INPUTS, "coupling_gproteindb.csv")
GTOP = os.path.join(INPUTS, "coupling_gtopdb.csv")
BLOCKB = os.path.join(ROOT, "data", "block_b", "02_constructs",
                      "construct_build_report.md")

# Family lists are joined with ";" and NEVER with "/". "Gi/o" and "Gq/11"
# contain a slash themselves, so a "/"-joined list splits back into nonsense
# ("Gi", "o") -- which is how the first run of this script reported that an
# ambiguous assignment changes the supplied bytes at zero rungs out of seven.
SEP = ";"

FAMILY_OF = {
    "Gs": "Gs", "Golf": "Gs", "GsL": "Gs", "GsS": "Gs",
    "Gi1": "Gi/o", "Gi2": "Gi/o", "Gi3": "Gi/o", "Go": "Gi/o",
    "GoA": "Gi/o", "GoB": "Gi/o", "Gt1": "Gi/o", "Gt2": "Gi/o",
    "Ggust": "Gi/o", "Gz": "Gi/o", "Gt": "Gi/o",
    "Gq": "Gq/11", "G11": "Gq/11", "G14": "Gq/11", "G15": "Gq/11",
    "G12": "G12/13", "G13": "G12/13",
}
# Block B / pipeline class labels -> family
FAMILIES_ACC = {
    "Gs": "P63092", "Golf": "P38405", "Gi1": "P63096", "Gi2": "P04899",
    "Gi3": "P08754", "Go": "P09471", "Gt1": "P04695", "Gt2": "P19087",
    "Ggust": "P29033", "Gz": "P19086", "Gq": "P50148", "G11": "P29992",
    "G14": "O95837", "G15": "P30679", "G12": "Q03113", "G13": "Q14344",
}
ORTHOLOG_ACC = {"P02699": "P08100", "P42866": "P35372"}
BLOCKB_FAMILY = {"Gs": "Gs", "Gi": "Gi/o", "Gt": "Gi/o", "Gq": "Gq/11",
                 "G12": "G12/13", "G13": "G12/13"}
# IUPHAR transducer prose -> family
IUPHAR_TOKEN = re.compile(r"(?<![A-Za-z0-9])G(11|12|13|14|15|s|i|o|q|z|t)(?![0-9])")
IUPHAR_TOKEN_FAMILY = {
    "s": "Gs", "i": "Gi/o", "o": "Gi/o", "t": "Gi/o", "z": "Gi/o",
    "q": "Gq/11", "11": "Gq/11", "14": "Gq/11", "15": "Gq/11",
    "12": "G12/13", "13": "G12/13",
}


def strip(t):
    return " ".join(re.sub(r"<[^>]+>", " ", t or "").replace("&nbsp;", " ").split())


# ------------------------------------------------ corrected entity classifier

def classify(desc, length):
    """What KIND of chain is this.

    Order matters and two of the branches exist only because an earlier version
    got them wrong:

    * A chain described as "...subunit gamma-2, ...subunit alpha-2, ...subunit
      alpha isoforms short" is a Gamma-Galpha FUSION and it is the Ga chain of
      the complex. Matching "subunit gamma" first filed OXYR/7RYC's mini-Gas/q
      chimera as a G-gamma and left that receptor looking as if its active
      reference had no G protein in it at all.
    * "ENGINEERED DOMAIN OF HUMAN G ALPHA S LONG ISOFORM" (AA2AR/5G53) contains
      neither "subunit alpha" nor "nucleotide-binding", so it fell through to
      `other` and 5G53 also looked transducer-free. It is mini-Gs.
    """
    d = (desc or "").lower()
    has_alpha = ("subunit alpha" in d or "g alpha" in d or "g-alpha" in d
                 or "galpha" in d or "mini-g" in d or "minig" in d
                 or re.search(r"\bg\s*protein subunit q\b", d))
    if "arrestin" in d:
        return "arrestin"
    if has_alpha:
        # a Ga chain, whether or not it is fused to beta, gamma or a scaffold
        if "subunit gamma" in d or "subunit beta" in d or "," in d:
            return "G-alpha-fusion"
        return "G-alpha"
    if ("nanobody" in d or re.search(r"\bnb[\s.]?\d", d) or "megabody" in d
            or "single-chain variable" in d or "scfv" in d or "vhh" in d
            or re.search(r"\bfab\b", d) or "antibody" in d
            or "heavy chain" in d or "light chain" in d
            or "camelid" in d or "immunoglobulin" in d):
        return "nanobody/antibody"
    if "g(i)/g(s)/g(t)" in d or "g(i)/g(s)/g(o)" in d:
        return "G-beta" if (length or 0) > 200 else "G-gamma"
    if "subunit beta" in d:
        return "G-beta"
    if "subunit gamma" in d:
        return "G-gamma"
    if "nucleotide-binding protein" in d:
        return "G-alpha"
    if ("lysozyme" in d or "rubredoxin" in d or "bril" in d or "cytochrome b562" in d
            or "glycogen synthase" in d or d.strip() == "pgs"):
        return "fusion-partner" if ("receptor" in d or "chimera" in d) else "fiducial"
    if "receptor" in d or "rhodopsin" in d or "opsin" in d:
        return "receptor"
    if (length or 0) <= 50:
        return "ligand-peptide"
    return "other"


def score_ct(seq, termini, n):
    if not seq or len(seq) < n:
        return [], 0.0
    ct = seq[-n:]
    key = "ct%d" % n
    scored = sorted(((sum(1 for a, b in zip(ct, t[key]) if a == b) / float(n), name)
                     for name, t in termini.items()), reverse=True)
    top = scored[0][0]
    return sorted(nm for i, nm in scored if i == top), top


def canonical_termini_from_rungs():
    """The 16 canonical Ga C-termini, read from seq_rungs.tsv and nowhere else.

    WHY NOT A SECOND ACCESSION LIST. coupling_fetch.py carried its own
    accession->family map, copied from verify_alpha5ct_family.py, and it drifted:
    it listed Ggust as **P29033, which is Gap junction beta-2 protein
    (Connexin 26)**, not gustducin (GNAT3 is A8MTJ3). The failure was silent in
    the worst way -- a wrong C-terminus can never WIN a match, so Ggust simply
    never appeared in any tie set, and every report looked clean. It also listed
    Gt1 as bovine P04695 where seq_rungs.tsv uses human P11488; those two happen
    to share their last 36 residues, so that one cost nothing, but two files
    disagreeing about which record a family name means is exactly the
    label-vs-identity trap SEQUENCES.md 3.4 documents.

    seq_rungs.tsv is the file the rung hashes come from, so reading the termini
    from it makes the family label in this map a valid join key into it BY
    CONSTRUCTION rather than by coincidence.
    """
    by_rung = collections.defaultdict(dict)
    acc = {}
    for r in csv.DictReader(open(RUNGS), delimiter="\t"):
        by_rung[r["rung"]][r["family"]] = r["sequence"]
        acc[r["family"]] = r["accession"]
    out = {}
    for fam in by_rung["R3_ct21"]:
        out[fam] = {"acc": acc[fam],
                    "ct21": by_rung["R3_ct21"][fam],
                    "ct11": by_rung["R1_ct11"][fam]}
    missing = [f for f, v in out.items() if len(v["ct21"]) != 21 or len(v["ct11"]) != 11]
    if missing:
        raise SystemExit("seq_rungs.tsv rung lengths are wrong for %s" % missing)
    return out


def c1_receptors():
    out = []
    for r in csv.DictReader(open(PANEL)):
        if "C1" not in r["tier"].split("|"):
            continue
        act, inact = [], []
        for k in ("strict_active_pdb", "our_active", "gdb_active", "cn_active"):
            v = (r.get(k) or "").strip().upper()
            if v and v not in act:
                act.append(v)
        for k in ("strict_inactive_pdb", "our_inactive", "gdb_inactive", "cn_inactive"):
            v = (r.get(k) or "").strip().upper()
            if v and v not in inact:
                inact.append(v)
        out.append({"slug": r["slug"], "gene": r["gene"], "acc": r["uniprot_acc"],
                    "organism": r["organism"], "gpcrdb_slug": r["gpcrdb_slug"],
                    "tier": r["tier"], "active_pdbs": act, "inactive_pdbs": inact})
    return out


def blockb_assignment():
    """The 40-row prior assignment, recovered from Block B's construct report.

    This is the only surviving trace of `refs/gpcr_coupling.csv`, which ships in
    no drop. It is read here so the redo's assignment can be diffed against the
    one 40,000 predictions were actually routed by.
    """
    out = {}
    if not os.path.exists(BLOCKB):
        return out
    started = False
    for line in open(BLOCKB):
        if line.startswith("| receptor | cognate class"):
            started = True
            continue
        if started:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or cells[0].startswith("---"):
                continue
            sec = [] if cells[2] in ("-", "") else [s.strip() for s in cells[2].split(",")]
            out[cells[0]] = {"cognate": cells[1], "secondary": sec,
                             "shuffled": cells[3]}
    return out


def main():
    recs = c1_receptors()
    termini = canonical_termini_from_rungs()
    entries = json.load(open(ENTITIES))
    bb = blockb_assignment()

    # ---------------------------------------------- A3: reference structures
    ref_rows = []
    struct = collections.defaultdict(list)      # slug -> list of dicts
    for r in recs:
        for role, plist in (("active", r["active_pdbs"]),
                            ("inactive", r["inactive_pdbs"])):
            for pdb in plist:
                e = entries.get(pdb)
                if not e:
                    ref_rows.append({"slug": r["slug"], "role": role, "pdb": pdb,
                                     "kind": "FETCH-FAILED"})
                    continue
                for pe in e.get("polymer_entities") or []:
                    meta = pe.get("rcsb_polymer_entity") or {}
                    poly = pe.get("entity_poly") or {}
                    seq = (poly.get("pdbx_seq_one_letter_code_can") or "").replace("\n", "")
                    ids = pe.get("rcsb_polymer_entity_container_identifiers") or {}
                    accs = [x.get("database_accession")
                            for x in ids.get("reference_sequence_identifiers") or []
                            if x.get("database_name") == "UniProt"]
                    orgs = sorted({(o or {}).get("ncbi_scientific_name") or ""
                                   for o in pe.get("rcsb_entity_source_organism") or []})
                    desc = meta.get("pdbx_description") or ""
                    n = poly.get("rcsb_sample_sequence_length")
                    kind = classify(desc, n)
                    row = {"slug": r["slug"], "receptor_acc": r["acc"],
                           "receptor_organism": r["organism"], "role": role,
                           "pdb": pdb, "method": (e.get("rcsb_entry_info") or {}).get(
                               "experimental_method", ""),
                           "title": (e.get("struct") or {}).get("title", ""),
                           "entity": pe["rcsb_id"],
                           "chains": "/".join(ids.get("auth_asym_ids") or []),
                           "kind": kind, "description": desc, "length": n,
                           "uniprot": ";".join(a for a in accs if a),
                           "organism": ";".join(x for x in orgs if x),
                           "pdbx_mutation": meta.get("pdbx_mutation") or "",
                           "ct11": "", "ct11_family": "", "ct11_identity": "",
                           "ct21": "", "ct21_family": "", "ct21_identity": "",
                           "construct_note": ""}
                    if kind in ("G-alpha", "G-alpha-fusion") and len(seq) >= 11:
                        f11, i11 = score_ct(seq, termini, 11)
                        f21, i21 = score_ct(seq, termini, 21)
                        row.update(ct11=seq[-11:], ct11_family="/".join(f11),
                                   ct11_identity="%.2f" % i11,
                                   ct21=seq[-21:] if len(seq) >= 21 else "",
                                   ct21_family="/".join(f21),
                                   ct21_identity="%.2f" % i21)
                        notes = []
                        if (n or 0) < 300:
                            notes.append("mini-G (%d aa; full subunit is 350-395)" % n)
                        # Two independent chimera tests, because they catch
                        # different constructs and each misses the other's.
                        #  (a) the two windows disagree: the last 21 match nothing
                        #      while the last 11 match cleanly -- a short graft on
                        #      a foreign scaffold (the mini-Gs/q and mini-Gs/i case)
                        #  (b) verify_alpha5ct_family.py's own test: the deposited
                        #      C-terminus names a family other than the accession's.
                        #      B1B1U5/9EPP passes (a) -- its last 21 still score 0.86
                        #      -- and fails (b): xref GNAI1, C-terminus Gq.
                        xfam = next((n2 for n2, ac in FAMILIES_ACC.items()
                                     if ac in accs), "")
                        fam11 = {FAMILY_OF.get(x, x) for x in f11}
                        if i21 < 0.80 <= i11:
                            notes.append("COUPLING CHIMERA (two-window): scaffold from "
                                         "one family, alpha5 tip from %s" % "/".join(f11))
                        elif xfam and i11 >= 0.80 and FAMILY_OF.get(xfam) not in fam11:
                            notes.append("COUPLING CHIMERA (xref-vs-C-terminus): "
                                         "accession is %s, alpha5 tip is %s"
                                         % (xfam, "/".join(f11)))
                        if i11 < 0.80:
                            notes.append("C-TERMINUS UNRECOGNISED at 11 (%.2f)" % i11)
                        if kind == "G-alpha-fusion":
                            notes.append("fused chain")
                        row["construct_note"] = "; ".join(notes)
                        if role == "active":
                            struct[r["slug"]].append(row)
                    ref_rows.append(row)

    cols = ["slug", "receptor_acc", "receptor_organism", "role", "pdb", "method",
            "entity", "chains", "kind", "description", "length", "uniprot",
            "organism", "ct11", "ct11_family", "ct11_identity", "ct21",
            "ct21_family", "ct21_identity", "construct_note", "pdbx_mutation",
            "title"]
    with open(os.path.join(INPUTS, "coupling_refstructures.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in ref_rows:
            w.writerow(r)

    # ---------------------------------------------------- A1: GproteinDb rows
    gp = collections.defaultdict(list)
    for r in csv.DictReader(open(GPDB)):
        gp[r["acc"]].append(r)

    # ---------------------------------------------------- A2: IUPHAR direct
    gt = {r["slug"]: r for r in csv.DictReader(open(GTOP))}

    def iuphar_families(text):
        """Families named in an IUPHAR transducer string, in the order written.

        HTML stripping turns "G<sub>i</sub>/G<sub>o</sub> family" into
        "G i /G o family", so whitespace is removed before tokenising. The first
        version of this function matched the rendered form ("Gi/Go", "Gs family")
        and therefore returned an EMPTY list for essentially every receptor --
        and an empty list is just one fewer authority, so nothing failed and
        nothing was reported. `main` now asserts the complement: no receptor may
        have non-empty IUPHAR text and zero parsed families.
        """
        t = re.sub(r"\s+", "", text or "")
        fams = []
        for m in IUPHAR_TOKEN.finditer(t):
            fam = IUPHAR_TOKEN_FAMILY[m.group(1)]
            if fam not in fams:
                fams.append(fam)
        return fams

    # ------------------------------------------------------------- verdicts
    #
    # WHY THE `primary_family` COLUMN IS NOT USED AS-IS. GproteinDb renders a
    # single primary per row even when its own rank-order columns show a tie.
    # AGTR1's GtoPdb row ranks Gi/o 1' AND Gq/11 1' and displays "Gi/o";
    # LPAR1's ranks Gi/o, Gq/11 and G12/13 all 1' and displays "G12/13". Taking
    # the displayed value would have manufactured an IUPHAR-vs-assay conflict on
    # AGTR1 and an IUPHAR "G12/13 primary" on LPAR1, neither of which the
    # underlying annotation asserts. The rank-1' SET is used instead, and a tie
    # is carried forward as a tie.
    RANKCOL = {"Gs": "rank_Gs", "Gi/o": "rank_Gio", "Gq/11": "rank_Gq11",
               "G12/13": "rank_G1213"}

    def rank1(g):
        fams = {f for f, c in RANKCOL.items() if (g.get(c) or "").strip() == "1'"}
        if fams:
            return fams
        p = (g.get("primary_family") or "").strip()
        return {p} if p and p != "-" else set()

    def ranked_secondary(g):
        return {f for f, c in RANKCOL.items()
                if re.match(r"^[2-9]'$", (g.get(c) or "").strip())}

    # PROVE THE PARSER RAN. A parser that returns nothing looks exactly like a
    # receptor with no annotation, so absence is asserted against, not assumed.
    unparsed = [g["slug"] for g in gt.values()
                if g.get("transducers", "").strip() and not iuphar_families(g["transducers"])]
    if unparsed:
        raise SystemExit("IUPHAR parser returned no family for receptors with "
                         "non-empty transducer text: %s" % unparsed)
    print("IUPHAR parser: %d receptors with text, all parsed"
          % sum(1 for g in gt.values() if g.get("transducers", "").strip()))

    out = []
    for r in recs:
        slug, acc = r["slug"], r["acc"]
        rows = gp.get(acc, []) or gp.get(ORTHOLOG_ACC.get(acc, ""), [])

        assay_rows = [g for g in rows if g["lab"] not in ("GproteinDb", "GtoPdb")]
        assay_primary = {}                       # lab -> set of rank-1' families
        for g in assay_rows:
            f = rank1(g)
            if f:
                assay_primary.setdefault(g["lab"], set())
                assay_primary[g["lab"]] |= f
        gpdb_primary = set().union(*[rank1(g) for g in rows
                                     if g["lab"] == "GproteinDb"]) \
            if any(g["lab"] == "GproteinDb" for g in rows) else set()
        gtop_primary = set().union(*[rank1(g) for g in rows
                                     if g["lab"] == "GtoPdb"]) \
            if any(g["lab"] == "GtoPdb" for g in rows) else set()

        # IUPHAR direct: the FIRST transduction record is the curator's primary
        # statement; later "||" records are additional annotated transducers.
        iu_text = gt.get(slug, {}).get("transducers", "")
        iu_primary = iuphar_families(iu_text.split("||")[0])
        iu_all = iuphar_families(iu_text)

        secondary = set()
        for g in assay_rows + [g for g in rows if g["lab"] == "GtoPdb"]:
            secondary |= ranked_secondary(g)
        secondary |= set(iu_all)

        # structural evidence -- the only non-annotation authority
        sfams, snotes, spdbs = set(), [], []
        for s in struct.get(slug, []):
            if not s["ct11_family"]:
                continue
            fams = {FAMILY_OF.get(x, x) for x in s["ct11_family"].split("/")}
            if len(fams) == 1:        # a tie spanning families is evidence for neither
                sfams |= fams
            spdbs.append("%s:%s" % (s["pdb"], s["ct11_family"]))
            if s["construct_note"]:
                snotes.append("%s %s" % (s["pdb"], s["construct_note"]))
        has_ga_ref = bool(struct.get(slug))

        # every independent primary claim, one per authority
        claims = {}
        for lab, f in assay_primary.items():
            claims["assay:" + lab] = f
        if gtop_primary:
            claims["GtoPdb(via GproteinDb)"] = gtop_primary
        if iu_primary:
            claims["IUPHAR(direct)"] = set(iu_primary)
        if sfams:
            claims["active reference structure"] = sfams

        # ---- VERDICT
        #
        # The distinction that matters, and that the first version of this
        # function got wrong: an authority that reports a TIE is not
        # contradicting an authority that reports one member of that tie -- it
        # is reporting the same thing at lower resolution. EDNRB's GtoPdb row
        # ranks Gs, Gi/o and Gq/11 all 1' and IUPHAR lists all three, while both
        # assay labs and the deposited structure say Gi/o. Treating unequal sets
        # as disagreement filed that as `conflicted`, which would have sent a
        # receptor with a perfectly clear answer to the PI as a blocker.
        # CONFLICTED now means two authorities are DISJOINT -- they cannot both
        # be right. Everything softer is AMBIGUOUS.
        reasons = []
        distinct = set().union(*claims.values()) if claims else set()
        inter = set.intersection(*claims.values()) if claims else set()
        pairs = sorted(claims.items())
        disjoint = [(a, b) for i, (a, va) in enumerate(pairs)
                    for (b, vb) in pairs[i + 1:] if not (va & vb)]
        primary_union = sorted(distinct)
        secondary = sorted(secondary - distinct)
        n_auth = len(claims)

        if not claims:
            verdict = "cognate_conflicted"
            reasons.append("NO AUTHORITY AT ALL: absent from GproteinDb and IUPHAR, "
                           "and no G-alpha in any active reference")
        elif disjoint:
            verdict = "cognate_conflicted"
            reasons.append("authorities that cannot both be right: "
                           + "; ".join("%s=%s vs %s=%s"
                                       % (a, "/".join(sorted(claims[a])),
                                          b, "/".join(sorted(claims[b])))
                                       for a, b in disjoint))
        elif not inter:
            verdict = "cognate_conflicted"
            reasons.append("no family is compatible with every authority: "
                           + "; ".join("%s=%s" % (k, "/".join(sorted(v)))
                                       for k, v in pairs))
        elif len(distinct) > 1:
            verdict = "cognate_ambiguous"
            reasons.append("authorities are compatible on %s but at least one "
                           "reports a wider set (%s)"
                           % (SEP.join(sorted(inter)), SEP.join(primary_union)))
        elif secondary:
            verdict = "cognate_ambiguous"
            reasons.append("primary agreed (%s) but %s is annotated as a further "
                           "transducer; 'the cognate Ga' is a choice, not a fact"
                           % (SEP.join(primary_union), SEP.join(secondary)))
        elif n_auth < 2:
            verdict = "cognate_ambiguous"
            reasons.append("only one authority available (%s)" % list(claims)[0])
        else:
            verdict = "cognate_confident"
            reasons.append("%d authorities agree on %s and none annotates a further "
                           "transducer" % (n_auth, SEP.join(primary_union)))

        # lit's hard rule: G12/13 has 0% inter-dataset core agreement
        # (pandyszekeres2024gproteindb p.8 Fig 4C), so it never passes as confident.
        if "G12/13" in distinct and verdict == "cognate_confident":
            verdict = "cognate_ambiguous"
            reasons.append("downgraded: a G12/13 primary cannot be called confident "
                           "-- 0% inter-dataset core agreement for that family")

        # WHAT WE WOULD SUPPLY, if forced to supply one. Named separately from
        # the verdict so the ladder builder can key off `verdict` and the PI can
        # overrule `recommended_family` without touching anything else.
        if len(inter) == 1:
            recommended = sorted(inter)[0]
            basis = "the only family compatible with all %d authorities" % n_auth
        elif sfams and len(sfams) == 1:
            recommended = sorted(sfams)[0]
            basis = ("taken from the deposited active reference, following "
                     "chiesa2025templatebias p.6302 -- the one precedent in the "
                     "corpus for picking a single Ga")
        else:
            votes = collections.Counter(f for v in claims.values() for f in v)
            recommended = votes.most_common(1)[0][0] if votes else ""
            basis = "NONE -- plurality of %d authorities only; needs a PI decision" % n_auth
        # subtype, recorded and never used to break a tie
        subtypes = collections.Counter()
        for g in assay_rows:
            s = (g.get("primary_subtype") or "").strip()
            if s and s != "-":
                subtypes[s] += 1

        prior = bb.get(slug)
        prior_fam = BLOCKB_FAMILY.get(prior["cognate"], "") if prior else ""
        prior_flag = ""
        if prior_fam:
            if distinct and prior_fam not in distinct:
                prior_flag = "PRIOR DISAGREES (Block B %s = %s; here %s)" % (
                    prior["cognate"], prior_fam, SEP.join(primary_union))
            elif distinct:
                prior_flag = "prior consistent"

        prior_struct = ""
        if prior_fam and sfams:
            prior_struct = ("prior matches the deposited partner"
                            if prior_fam in sfams else
                            "PRIOR CONTRADICTS THE DEPOSITED PARTNER (Block B %s, "
                            "reference supplies %s)" % (prior_fam, SEP.join(sorted(sfams))))
        elif prior_fam:
            prior_struct = "no G-alpha in the active reference to check against"

        out.append({
            "slug": slug, "gene": r["gene"], "uniprot": acc,
            "receptor_organism": r["organism"],
            "verdict": verdict,
            "family_primary": SEP.join(primary_union),
            "family_compatible_with_all": SEP.join(sorted(inter)),
            "recommended_family": recommended,
            "recommended_basis": basis,
            "family_secondary_annotated": SEP.join(secondary),
            "subtype_reported": SEP.join("%s(%d)" % (s, n)
                                         for s, n in subtypes.most_common()),
            # "+" and not "/": "Gi/o" and "Gq/11" already contain a slash, so a
            # "/"-joined list cannot be split back. This exact mistake produced a
            # 35-receptor "GtoPdb omits Gi;o" finding that did not exist.
            "authority_assaylabs": SEP.join(
                "%s=%s" % (k.split(":", 1)[1], "+".join(sorted(v)))
                for k, v in sorted(claims.items()) if k.startswith("assay:")),
            "authority_gproteindb_merged": SEP.join(sorted(gpdb_primary)),
            "authority_gtopdb_via_gproteindb": SEP.join(sorted(gtop_primary)),
            "authority_iuphar_direct_primary": SEP.join(iu_primary),
            "authority_iuphar_direct_all": SEP.join(iu_all),
            "authority_iuphar_text": iu_text,
            "authority_structure": SEP.join(sorted(sfams)),
            "structure_evidence": "; ".join(spdbs),
            "structure_construct_notes": "; ".join(snotes),
            "active_ref_has_galpha": "yes" if has_ga_ref else "no",
            "n_authorities": n_auth,
            "blockb_prior": prior["cognate"] if prior else "",
            "blockb_prior_family": prior_fam,
            "blockb_prior_check": prior_flag,
            "blockb_prior_vs_structure": prior_struct,
            "reason": " | ".join(reasons),
        })

    acols = list(out[0].keys())
    with open(os.path.join(INPUTS, "coupling_assignments.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=acols)
        w.writeheader()
        w.writerows(sorted(out, key=lambda x: x["slug"]))

    # -------------------------------------------------------- rung impact
    rung_seq = collections.defaultdict(dict)
    for r in csv.DictReader(open(RUNGS), delimiter="\t"):
        rung_seq[r["rung"]][r["family"]] = (r["sequence"], r["sha256"])
    REP = {"Gs": ["Gs"], "Gi/o": ["Gi1"], "Gq/11": ["Gq"], "G12/13": ["G13"]}

    # WHAT "AFFECTED" MEANS INPUTS. A rung is affected by an ambiguous assignment
    # if the candidate families would put DIFFERENT BYTES on the wire at that
    # rung. Two separate quantities are reported per rung, because they carry
    # different costs: whether the sequence differs at all, and whether its
    # LENGTH differs. At every peptide rung the length is fixed by construction
    # (11, 15, 21, 26, 36), so a second arm there is the same size as the first;
    # at R7_full the families differ in length by up to 44 residues (Gt1 350 vs
    # Gs 394), so a second arm is a different and larger job.
    RUNG_ORDER = ("R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix", "R5_a5plus",
                  "R6a_da5", "R7_full")
    def rung_verdict(cands, rung):
        shas, lens = set(), set()
        for f in cands:
            for rep in REP.get(f, []):
                if rep in rung_seq[rung]:
                    seq, sha = rung_seq[rung][rep]
                    shas.add(sha)
                    lens.add(len(seq))
        if len(shas) <= 1:
            return "SAME"
        return ("DIFFERS+LEN(%d)" if len(lens) > 1 else "DIFFERS(%d)") % len(shas)

    impact = []
    for a in out:
        # TIER P -- families some authority calls PRIMARY. This is the set the
        # "which cognate do we supply" decision actually ranges over.
        prim = sorted({f for f in a["family_primary"].split(SEP) if f})
        # TIER A -- every family annotated as a transducer at all. This is the
        # set the "supply the top-N families as separate arms" option ranges
        # over, and it is much larger: promiscuity is the norm, not the exception.
        anyf = sorted(set(prim) | {f for f in a["family_secondary_annotated"].split(SEP) if f})
        cands = prim
        row = {"slug": a["slug"], "verdict": a["verdict"],
               "primary_candidate_families": SEP.join(prim),
               "n_primary_candidates": len(prim),
               "any_annotated_families": SEP.join(anyf),
               "n_any_annotated": len(anyf)}
        for rung in RUNG_ORDER:
            row["any_" + rung] = rung_verdict(anyf, rung)
        for rung in RUNG_ORDER:
            shas, lens = set(), set()
            for f in cands:
                for rep in REP.get(f, []):
                    if rep in rung_seq[rung]:
                        seq, sha = rung_seq[rung][rep]
                        shas.add(sha)
                        lens.add(len(seq))
            if len(shas) <= 1:
                row[rung] = "SAME"
            elif len(lens) > 1:
                row[rung] = "DIFFERS+LEN(%d)" % len(shas)
            else:
                row[rung] = "DIFFERS(%d)" % len(shas)
        impact.append(row)
    icols = (["slug", "verdict", "primary_candidate_families", "n_primary_candidates",
              "any_annotated_families", "n_any_annotated"] + list(RUNG_ORDER)
             + ["any_" + r for r in RUNG_ORDER])
    with open(os.path.join(INPUTS, "coupling_rung_impact.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=icols)
        w.writeheader()
        w.writerows(impact)

    # -------------------------------------------------------- console summary
    print("verdicts: %s" % dict(collections.Counter(a["verdict"] for a in out)))
    print("prior check: %s" % dict(collections.Counter(
        a["blockb_prior_check"] or "(not in Block B 40)" for a in out)))
    print("\nreceptors whose active reference contains NO G-alpha: %s"
          % [a["slug"] for a in out if a["active_ref_has_galpha"] == "no"])
    print("\ncoupling chimeras / mini-G in the active references:")
    for a in out:
        if "CHIMERA" in a["structure_construct_notes"]:
            print("  %-7s %s" % (a["slug"], a["structure_construct_notes"]))
    print("\nrung immunity among non-confident receptors:")
    nonconf = [i for i in impact if i["verdict"] != "cognate_confident"]
    for rung in ("R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix", "R5_a5plus",
                 "R6a_da5", "R7_full"):
        print("  %-11s DIFFERS on %d of %d" % (
            rung, sum(1 for i in nonconf if i[rung].startswith("DIFFERS")), len(nonconf)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
