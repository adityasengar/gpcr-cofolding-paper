#!/usr/bin/env python3
"""Identify each reference's Ga family from its DEPOSITED alpha5-CT, not its accession.

WHY. Coupling chimeras are a Ga backbone carrying a different family's C-terminal
helix, and they are used precisely because the alpha5-CT is what determines
coupling. On such an entry the UniProt cross-reference names the BACKBONE, so
anything keyed on the accession assigns the wrong family: the lit session found
an entry cross-referenced to Gas (P63092) whose deposited C-terminus is Gai's.

This matters here more than it looks. Block B's arms are FAMILY-DEFINED --
cognate, decoy, shuffled -- so a reference whose family is read from the
accession rather than from the graft would put a receptor in the wrong arm and
no downstream check would notice.

`reference_audit.csv` carries an `alpha5_donor_class` column populated on
exactly 2 of 80 rows, both annotated CHIMERA by hand. This script asks whether 2
is the true count.

METHOD, and why it is not the positional diff used by verify_partner_chains.py.
Positions are meaningless across constructs of different length: a substitution
reported at "position 68" means one thing in a 354-mer and another in a 71-mer,
and a truncated construct silently shifts every position. So this compares
TERMINI -- the deposited last 21 residues against each family's canonical last
21 -- which needs no alignment and no numbering at all. A chimera announces
itself by matching a family other than its own accession.

Usage:  python3 analysis/verify_alpha5ct_family.py
"""
import csv
import sys

from verify_partner_chains import (ALPHA5_CT_LEN, canonical, is_partner,
                                   partner_entities)

REF_AUDIT = "data/block_b/09_references/reference_audit.csv"

# One canonical accession per Ga family. The C-terminal 21 of each is the
# coupling determinant.
#
# TWO PAIRS ARE BYTE-IDENTICAL OVER THIS WINDOW, which is a fact about the
# biology and not a defect to work around:
#     Gi1 / Gi2  ->  FVFDAVTDVIIKNNLKDCGLF
#     Gq  / G11  ->  FVFAAVKDTILQLNLKEYNLV
# So the alpha5-CT CANNOT distinguish Gi1 from Gi2, or Gq from G11. An earlier
# version of this script sorted the family scores and reported the top one,
# which resolved every one of those ties lexically and announced 18 unannotated
# coupling chimeras that do not exist. Ties are now reported as ties, and a
# chimera is called ONLY when the deposited C-terminus fails to match the
# accession's own family.
FAMILIES = {
    "Gs":     "P63092",   # GNAS
    "Golf":   "P38405",
    "Gi1":    "P63096",
    "Gi2":    "P04899",
    "Gi3":    "P08754",
    "Go":     "P09471",
    "Gt1":    "P04695",
    "Gz":     "P19086",
    "Gq":     "P50148",
    "G11":    "P29992",
    "G14":    "O95837",
    "G15":    "P30679",
    "G12":    "Q03113",
    "G13":    "Q14344",
}


def family_termini():
    out = {}
    for name, acc in FAMILIES.items():
        seq = canonical(acc)
        if seq:
            out[name] = seq[-ALPHA5_CT_LEN:]
    return out


def identity(a, b):
    return sum(1 for x, y in zip(a, b) if x == y) / float(len(a))


def main():
    termini = family_termini()
    if len(termini) < len(FAMILIES):
        missing = set(FAMILIES) - set(termini)
        print(f"WARNING: could not fetch {sorted(missing)} -- verdicts below are "
              f"against a partial family table\n", file=sys.stderr)

    rows = [r for r in csv.DictReader(open(REF_AUDIT)) if r["role"] == "active"]
    print(f"checking the alpha5-CT of {len(rows)} active references "
          f"against {len(termini)} Ga family C-termini\n")

    print(f"{'pdb':6} {'recep':9} {'xref':9} {'by C-term':11} {'id':>5}  verdict")
    print("-" * 100)

    mismatched, checked, unresolved = [], 0, 0
    for r in rows:
        pdb, receptor = r["pdb_id"].upper(), r["receptor"]
        annotated = r["alpha5_donor_class"].strip() or "-"
        entities, err = partner_entities(pdb)
        if err:
            print(f"{pdb:6} {receptor:9} FETCH FAILED: {err}")
            continue
        for ent in entities:
            if not is_partner(ent["description"]):
                continue
            seq = ent["sequence"]
            if len(seq) < ALPHA5_CT_LEN:
                continue
            ct = seq[-ALPHA5_CT_LEN:]
            scored = sorted(((identity(ct, t), n) for n, t in termini.items()),
                            reverse=True)
            best_id = scored[0][0]
            # EVERY family at the top score, not an arbitrary winner among ties
            best = sorted(n for i, n in scored if i == best_id)

            acc = ent["uniprot"]
            xref = next((n for n, a in FAMILIES.items() if a == acc), acc or "none")
            checked += 1

            if best_id < 0.80:
                verdict = "UNRECOGNISED C-TERMINUS"
                unresolved += 1
            elif xref not in FAMILIES:
                verdict = f"xref is not a canonical family entry ({acc})"
            elif xref in best:
                # the accession's own family is among the best matches: consistent,
                # whether or not a sibling family ties with it
                verdict = ("consistent" if len(best) == 1 else
                           "consistent (tie: " + "/".join(best) + " share this C-term)")
            else:
                verdict = f"** CHIMERA: xref {xref}, C-term {'/'.join(best)} **"
                mismatched.append((pdb, receptor, xref, "/".join(best), annotated))
            print(f"{pdb:6} {receptor:9} {xref:9} {'/'.join(best):11} {best_id:5.2f}  "
                  f"{verdict}")

    print(f"\n  Ga chains with a readable C-terminus : {checked}")
    print(f"  C-terminus DISAGREES with the accession : {len(mismatched)}")
    print(f"  unrecognised C-terminus (flagged, not passed) : {unresolved}")
    if mismatched:
        print("\n  Each of these is a coupling chimera. The accession names the "
              "backbone;\n  the C-terminus is the coupling determinant and is what "
              "the paper measures.\n")
        for pdb, rec, xref, best, ann in mismatched:
            state = ("ALREADY ANNOTATED as " + ann) if ann != "-" \
                else "NOT ANNOTATED in reference_audit.csv"
            print(f"    {pdb} {rec:9} backbone {xref:5} -> alpha5-CT {best:5}  ({state})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
