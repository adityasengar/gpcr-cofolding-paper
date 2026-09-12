#!/usr/bin/env python3
"""ICL3 audit of the 128 rule-R reference structures.

Why this exists. The lit session relayed `georgiou2025heterogeneity` pp.9,16:
T4 lysozyme fused into ICL3 of β2AR "causes the population of **only active
TM6 conformations independent of the efficacy of bound ligands**", and flags
A2AR `3PWH` as a possible artefactual broken ionic lock. `lee2026confornets`
p15 deletes "ICL3 and any fusion proteins inserted" from inactive structures
without stating a reason. So an *inactive* reference carrying an ICL3 fusion
may not be an inactive reference at all, and `PANEL.md` §9 already records
that 40 of 64 inactive references carry a fusion inside the receptor entity
against 7 of 64 active ones.

This classifies, per reference, **where** the fusion sits: ICL3, a terminus,
or elsewhere — which `panel_systems.csv`'s boolean `fusion_in_receptor_entity`
cannot say. An N-terminal BRIL and an ICL3 T4L are not the same object and
only the second is implicated by georgiou2025heterogeneity.

Inputs (all produced by sibling seqrec_ scripts, nothing fetched here)
  seqrec_refs.tsv      per-reference construct map, from seqrec_refs.py
  seqrec_features.tsv  UniProt TRANSMEM ranges, from seqrec_build.py
ICL3 is defined as the canonical interval between the end of TM5 and the start
of TM6 in the UniProt feature table, widened by ICL3_TOL residues at each end
(see the constant for why).

Output
  seqrec_icl3_audit.tsv   one row per (receptor, state, pdb)

Usage
  python3 redo/build/seqrec_icl3_audit.py
  python3 redo/build/seqrec_icl3_audit.py --selftest
"""
import collections
import csv
import os
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
REFS = os.path.join(INPUTS, "seqrec_refs.tsv")
FEATS = os.path.join(INPUTS, "seqrec_features.tsv")
OUT = os.path.join(INPUTS, "seqrec_icl3_audit.tsv")

# Fusion partners named in the 128 receptor-entity descriptions. Matched on
# the description string, which is the depositor's own text.
FUSION_TOKENS = [
    ("T4L", ("endolysin", "lysozyme", "t4 lysozyme")),
    ("BRIL", ("cytochrome b562", "b562ril", "bril")),
    ("PGS", ("glycogen synthase",)),
    ("rubredoxin", ("rubredoxin",)),
    ("flavodoxin", ("flavodoxin",)),
    ("nanoluc", ("luciferin", "luciferase", "nanoluc")),
    ("endoglucanase", ("endoglucanase",)),
    ("GFP", ("green fluorescent",)),
    ("mCherry", ("mcherry",)),
    ("thermostab_apocyt", ("apocytochrome",)),
    ("fusion_unnamed", ("fusion protein", "chimera")),
]
TERMINAL_MIN = 20          # entity residues beyond the mapped receptor span
INTERNAL_MIN = 20          # an internal insertion big enough to be a domain
# Tolerance on the ICL3 boundary, in canonical residues. UniProt's TM5-end and
# TM6-start are helix-boundary annotations, not splice sites, and depositors
# splice a fusion domain a few residues into the helix. With a +/-1 tolerance
# three ICL3 fusions were classified "other-internal" and would have been
# missed: 9D3G (CCR6, 127 aa BRIL spliced 4 residues before UniProt ICL3),
# 7UL3 (HRH2, 41 aa at -4) and 7UL2 (NTR1, 32 aa at -5). A >=20-residue
# insertion within 5 residues of the TM5/TM6 loop is an ICL3 fusion on any
# reading; a tighter window is precision the annotation does not have.
ICL3_TOL = 5


def fusion_names(desc):
    d = desc.lower()
    out = [name for name, toks in FUSION_TOKENS if any(t in d for t in toks)]
    return ";".join(out) or "none"


def tm_ranges():
    tm = collections.defaultdict(list)
    for r in csv.DictReader(open(FEATS), delimiter="\t"):
        if r["feature"] == "TRANSMEM":
            tm[r["slug"]].append((int(r["start"]), int(r["end"])))
    return {k: sorted(v) for k, v in tm.items()}


def parse_ins(field):
    """'207/161aa;318/12aa' -> [(207, 161), (318, 12)]"""
    if not field or field == "none":
        return []
    out = []
    for part in field.split(";"):
        pos, ln = part.split("/")
        out.append((int(pos), int(ln.replace("aa", ""))))
    return out


def parse_span(s):
    if not s or s == "NA":
        return None
    a, b = s.split("-")
    return int(a), int(b)


def main():
    tm = tm_ranges()
    rows = []
    for r in csv.DictReader(open(REFS), delimiter="\t"):
        slug = r["slug"]
        helices = tm.get(slug, [])
        if len(helices) < 7:
            icl3 = None
        else:
            icl3 = (helices[4][1] + 1, helices[5][0] - 1)      # TM5 end .. TM6 start
        ins = parse_ins(r["internal_insertions_canonpos_len"])
        present = parse_span(r["canon_present_span"])
        n_flank = int(r["n_term_extra_entity_aa"])
        c_flank = int(r["c_term_extra_entity_aa"])

        icl3_ins = [(p, L) for p, L in ins
                    if icl3 and icl3[0] - ICL3_TOL <= p <= icl3[1] + ICL3_TOL
                    and L >= INTERNAL_MIN]
        other_ins = [(p, L) for p, L in ins
                     if L >= INTERNAL_MIN and (p, L) not in icl3_ins]
        # ICL3 residues excised: canonical positions inside ICL3 that the
        # construct does not contain at all
        icl3_len = (icl3[1] - icl3[0] + 1) if icl3 else 0
        grafts = [] if r["grafted_canon_spans"] == "none" else [
            tuple(int(x) for x in g.split("-")) for g in r["grafted_canon_spans"].split(";")]
        icl3_graft = sum(b - a + 1 for a, b in grafts
                         if icl3 and not (b < icl3[0] or a > icl3[1]))

        where = []
        if icl3_ins:
            where.append("ICL3")
        if n_flank >= TERMINAL_MIN:
            where.append("N-term")
        if c_flank >= TERMINAL_MIN:
            where.append("C-term")
        if other_ins:
            where.append("other-internal")

        rows.append({
            "slug": slug, "state": r["state"], "pdb": r["pdb"],
            "description": r["description"],
            "fusion_named_in_description": fusion_names(r["description"]),
            "icl3_canon_range": f"{icl3[0]}-{icl3[1]}" if icl3 else "NA",
            "icl3_len": icl3_len,
            "fusion_location": "|".join(where) or "none",
            "icl3_insertion_aa": sum(L for _, L in icl3_ins),
            "icl3_insertion_at": ";".join(f"{p}/{L}aa" for p, L in icl3_ins) or "none",
            "icl3_graft_aa": icl3_graft,
            "other_internal_insertion_at": ";".join(f"{p}/{L}aa" for p, L in other_ins) or "none",
            "n_term_extra_entity_aa": n_flank,
            "c_term_extra_entity_aa": c_flank,
            "canon_present_span": r["canon_present_span"],
            "n_canon_resolved": r["n_canon_resolved"],
        })

    with open(OUT, "w") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    # --- summary to stderr, so a run always says what it found
    by_state = collections.Counter((r["state"], "ICL3" in r["fusion_location"])
                                   for r in rows)
    print(f"# wrote {OUT} ({len(rows)} references)", file=sys.stderr)
    for st in ("active", "inactive"):
        print(f"#   {st:8s} ICL3 fusion: {by_state[(st, True)]:3d} / "
              f"{by_state[(st, True)] + by_state[(st, False)]}", file=sys.stderr)
    print("#   fusion partners in ICL3: " + str(collections.Counter(
        r["fusion_named_in_description"] for r in rows
        if "ICL3" in r["fusion_location"])), file=sys.stderr)


def selftest():
    """Prove the classifier by planting each case it must separate."""
    ok = True
    cases = [
        ("ICL3 insertion",  "227/161aa", 0, 0, "ICL3"),
        ("N-terminal only", "none", 106, 0, "N-term"),
        ("C-terminal only", "none", 0, 106, "C-term"),
        ("nothing",         "none", 3, 4, "none"),
        ("short ICL3 gap below threshold", "227/6aa", 0, 0, "none"),
        ("insertion 4 residues before ICL3 (the 9D3G case)", "216/127aa", 0, 0, "ICL3"),
        ("insertion 40 residues before ICL3", "180/127aa", 0, 0, "none"),
    ]
    # ADRB2 TM5 ends 229, TM6 starts 267 in P07550, so 227/161aa lands in ICL3
    tm = tm_ranges()["ADRB2"]
    icl3 = (tm[4][1] + 1, tm[5][0] - 1)
    for label, ins, nf, cf, expect in cases:
        got = []
        parsed = [(p, L) for p, L in parse_ins(ins)
                  if icl3[0] - ICL3_TOL <= p <= icl3[1] + ICL3_TOL
                  and L >= INTERNAL_MIN]
        if parsed:
            got.append("ICL3")
        if nf >= TERMINAL_MIN:
            got.append("N-term")
        if cf >= TERMINAL_MIN:
            got.append("C-term")
        res = "|".join(got) or "none"
        print(f"  {label:34s} -> {res:8s} (expect {expect})")
        ok &= res == expect
    print(f"ADRB2 ICL3 = {icl3[0]}-{icl3[1]}")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
