#!/usr/bin/env python3
"""g1_refchimera.py — which deposited ACTIVE references carry a non-canonical a5 tip.

WHY THIS MATTERS TO GROUP 1 AND TO ALMOST NOBODY ELSE
-----------------------------------------------------
Rungs R1-R4 *are* the alpha5 C terminus.  If a receptor's active reference was
solved with an **engineered** alpha5 tip -- a mini-Gs/q chimera, a Gi/Gt chimera,
a high-affinity peptide analogue -- then for that receptor the peptide we supply
is not the peptide that was crystallised, at exactly the residues the paper is
about.

SCOPE IT PRECISELY, BECAUSE OVERSTATING IT IS ITS OWN ERROR
------------------------------------------------------------
The state predicate is **receptor-internal**: d(Y5.58 OH, Y7.53 OH) and
d(2x46 CA, 6x37 CA).  The reference's Galpha chain is not scored.  So this is NOT
a direct scoring mismatch in the predicate.  It bites in three narrower places,
and only those three:

  (a) **Reference provenance.** The reference's "active" receptor geometry is the
      geometry an engineered tip produced.  Our predicate then defines active as
      "looks like what miniGsq produced".  Second-order and probably small -- the
      TM6 opening is large -- but it is unverified, not verified.
  (b) **Every interface readout in `g1_recording_spec.tsv` that compares our
      predicted partner placement to the deposited one** --
      `contact_register_last5_json`, `d_ga_alpha5_r350_ca`,
      `n_interface_contacts_ga_receptor`.  There a wild-type tip is compared
      against a chimeric tip residue by residue.  This is a like-for-unlike
      comparison and it is the real cost.
  (c) **E1.4 (G9), the family swap.**  For these receptors the "cognate Gq tip"
      the structural-biology community actually used is not canonical Gq.

Source: `redo/inputs/coupling_refstructures.csv` (coupling session), joined to
`redo/inputs/g1_receptors.tsv` so the verdict is restricted to the reference
PANEL.md's Rule R actually selects, and to the provisional CORE-32.

Usage:  python3 redo/build/g1_refchimera.py
"""
import csv
import os
import sys
from collections import Counter, defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
OUT = os.path.join(INPUTS, "g1_refchimera.tsv")


def tsv(name):
    with open(os.path.join(INPUTS, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    refs = list(csv.DictReader(open(os.path.join(INPUTS, "coupling_refstructures.csv"))))
    rec = {r["slug"]: r for r in tsv("g1_receptors.tsv")}
    canon = {r["sequence"]: r["family"] for r in tsv("seq_rungs.tsv")
             if r["rung"] == "R1_ct11"}
    canon_set = set(canon)

    withtip = [r for r in refs if r["ct11"]]
    sys.stderr.write(f"# {len(withtip)} reference entities carry an alpha5 tip\n")
    sys.stderr.write("# tip census (all roles, all references):\n")
    for tip, n in Counter(r["ct11"] for r in withtip).most_common():
        fams = sorted({f for s, f in canon.items() if s == tip})
        sys.stderr.write(f"#   {tip}  x{n:3d}  {'canonical ' + '/'.join(fams) if fams else '** NOT CANONICAL for any of the 16 human Galpha **'}\n")

    rows = []
    for r in withtip:
        if r["ct11"] in canon_set:
            continue
        slug = r["slug"]
        p = rec.get(slug)
        # is this the reference Rule R actually picked, per PANEL.md 6.1?
        chosen = ""
        if p:
            if r["pdb"] == p["active_pdb"]:
                chosen = "active"
            elif r["pdb"] == p["inactive_pdb"]:
                chosen = "inactive"
        # nearest canonical family, by Hamming on the 11-mer
        best = sorted(((sum(1 for a, b in zip(r["ct11"], s) if a != b), f)
                       for s, f in canon.items()))
        rows.append(dict(
            slug=slug, role=r["role"], pdb=r["pdb"], entity=r["entity"],
            is_rule_r_reference=chosen or "NO -- an alternative reference",
            in_core32_provisional=(p or {}).get("core32_provisional", "?"),
            partner_len=r["length"], ct11=r["ct11"],
            nearest_canonical=f"{best[0][1]} (Hamming {best[0][0]}/11)",
            all_at_min=" ".join(f for d, f in best if d == best[0][0]),
            ct11_identity=r["ct11_identity"], ct21=r["ct21"],
            ct21_identity=r["ct21_identity"],
            uniprot_xrefs=r["uniprot"] or "(none)",
            description=r["description"][:70],
            construct_note=r["construct_note"][:110]))

    cols = list(rows[0].keys())
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in sorted(rows, key=lambda r: (r["slug"], r["pdb"])):
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    # ---- the numbers that decide the options --------------------------------
    act = [r for r in rows if r["is_rule_r_reference"] == "active"]
    core = [r for r in act if r["in_core32_provisional"] == "yes"]
    sys.stderr.write(f"\n# non-canonical alpha5 tips: {len(rows)} reference entities, "
                     f"{len({r['slug'] for r in rows})} distinct receptors\n")
    sys.stderr.write(f"# of which on the Rule-R ACTIVE reference: {len(act)} entities, "
                     f"{len({r['slug'] for r in act})} receptors\n")
    sys.stderr.write(f"# of those, inside the provisional CORE-32: "
                     f"{len(core)} -> {sorted(r['slug'] for r in core)}\n")
    sys.stderr.write(f"# outside CORE-32 but on C1: "
                     f"{sorted({r['slug'] for r in act if r['in_core32_provisional']!='yes'})}\n")

    sys.stderr.write("\n# by tip class, on the Rule-R active reference:\n")
    byclass = defaultdict(list)
    for r in act:
        byclass[r["ct11"]].append(r["slug"])
    for tip, slugs in sorted(byclass.items(), key=lambda kv: -len(kv[1])):
        ex = [r for r in act if r["ct11"] == tip][0]
        sys.stderr.write(f"#   {tip}  n={len(slugs):2d}  nearest {ex['nearest_canonical']}"
                         f"  partner_len={ex['partner_len']}  {sorted(set(slugs))}\n")

    # does a receptor have ANY canonical-tip active reference to fall back on?
    sys.stderr.write("\n# is there a canonical-tip ACTIVE reference available instead?\n")
    canon_act = defaultdict(set)
    for r in withtip:
        if r["role"] == "active" and r["ct11"] in canon_set:
            canon_act[r["slug"]].add(f"{r['pdb']}({canon[r['ct11']]})")
    for slug in sorted({r["slug"] for r in act}):
        alt = sorted(canon_act.get(slug, []))
        sys.stderr.write(f"#   {slug:7s} {'yes: ' + ', '.join(alt) if alt else 'NO -- every active reference it has carries a non-canonical tip'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
