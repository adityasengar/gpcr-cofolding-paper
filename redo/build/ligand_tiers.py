#!/usr/bin/env python3
"""The redo's ligand tiers -- which receptors can enter the ligand arm, and how.

Aditya's criteria, 2026-09-12:
  T1  highest priority: receptors with BOTH a small-molecule agonist and a
      small-molecule antagonist.
  T2  peptide-based receptors are KEPT but TREATED SEPARATELY -- reported as
      their own tier, never pooled into T1.
  --  PAM, NAM and antibody/nanobody ligands are skipped completely.

THE AXIS THAT MATTERS IS NOT THE DATABASE'S TYPE STRING.  It is whether the
ligand enters the prediction as a SEPARATE POLYMER CHAIN, because our whole
claim is about what happens when you add a chain.  A ligand carrying a CCD code
is deposited as a HETATM component and is therefore NOT a chain, whatever the
type string says.

That distinction is not academic.  Exactly ONE record in the 872-record census
is typed `peptide` and carries a CCD: EDNRB's IRL 2500 (D2U), a peptidomimetic.
It is also the only thing that made EDNRB look like a matched-peptide receptor.
Classify on the type string and EDNRB joins T2 wrongly; classify on chain-ness
and it falls out, because its real antagonists (bosentan, K-8794) are small
molecules.  EDNRB is a MISMATCHED receptor.

    python3 redo/build/ligand_tiers.py
    python3 redo/build/manifest.py

Writes: inputs/ligand_tiers.tsv
"""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, CACHE  # noqa: E402

CENSUS = os.path.join(CACHE, "ligand_census_records.tsv")
OUT = os.path.join(INPUTS, "ligand_tiers.tsv")

AGONIST_SIDE = {"agonist", "partial_agonist"}
ANTAGONIST_SIDE = {"antagonist", "inverse_agonist"}
# skipped completely, per Aditya: no published labelling rule files these as
# active or inactive (khaleq2026hyaline p12 has no slot for them at all).
SKIP_ROLES = {"pam", "nam", "ago_pam", "allosteric_agonist", "allosteric_antagonist"}

# antibody / nanobody / scFv ligands are skipped: our PARTNER arm is
# Ga-or-nanobody, so an antibody in the LIGAND arm entangles the two factors
# far worse than a peptide does, and it is invisible in a modality column.
ANTIBODY = re.compile(r"\b(nanobody|antibody|scfv|fab|\bnb\d|mab|m22|cs-17|k1-70|"
                      r"at118|sybody|megabody)\b", re.I)


def is_chain(rec):
    """Does this ligand enter as a separate polymer chain?"""
    if rec["modality"] not in ("peptide", "protein"):
        return False
    # a CCD code means a HETATM component, not a chain -- see the module docstring
    return not rec["ligand_ccd"].strip()


def main():
    with open(CENSUS) as fh:
        census = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        panel = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(INPUTS, "g1_panel_freeze.tsv")) as fh:
        freeze = {r["receptor_slug"]: r["tier"] for r in csv.DictReader(fh, delimiter="\t")}
    ourref = {}
    for r in panel:
        ourref[r["slug"]] = {r["active_pdb"].upper(), r["inactive_pdb"].upper()}

    rows = []
    for p in panel:
        slug = p["slug"]
        recs = [c for c in census if c["receptor"] == slug]
        # skip rules, applied first and counted
        n_allo = sum(1 for c in recs if c["role"] in SKIP_ROLES)
        n_ab = sum(1 for c in recs if ANTIBODY.search(c["ligand_name"]))
        # SPECIES FOLLOWS THE PANEL, never the PDB.  Without this NTR1 enters T1
        # on a RAT structure (6ZA8, Rattus norvegicus, and Intermediate state at
        # that) while our NTR1 is human -- the same trap PANEL.md Rule R step 5
        # and LIGAND_CURATION_PROPOSAL.md both record.  B1B1U5 (spider) and OPSD
        # (bovine) are non-human and correctly KEPT: the rule is match-the-panel,
        # not prefer-human.
        org = p["organism"]
        usable = [c for c in recs
                  if c["role"] not in SKIP_ROLES
                  and not ANTIBODY.search(c["ligand_name"])
                  and c["site"] == "orthosteric"
                  and (c["structure_species"] in org or org in c["structure_species"])]

        def best(side, want_state, chain_wanted):
            """Best pick of a given chain-ness for one arm, or None.

            Ordering, and every term earns its place:
              1. provenance state -- an agonist co-crystallised in an ACTIVE
                 receptor is the evidence Aditya's "evidenced structurally"
                 rationale rests on. Agonists sitting in INACTIVE structures are
                 a real and separate population (F-11) and are demoted, not
                 dropped, with the state recorded.
              2. on one of OUR OWN reference structures -- a ligand bound to the
                 structure we score against beats an equally-resolved stranger.
                 This is the rule that caught HRH3's histamine.
              3. resolution.
            """
            cand = [c for c in usable
                    if c["role"] in side and is_chain(c) == chain_wanted]
            if not cand:
                return None
            def rank(c):
                try:
                    res = float(c["resolution"])
                except ValueError:
                    res = 99.0
                return (0 if c["structure_state"] == want_state else 1,
                        0 if c["pdb"].upper() in ourref[slug] else 1,
                        res)
            return sorted(cand, key=rank)[0]

        # Classify by what pairs are AVAILABLE, never by one greedy pick -- a
        # greedy pick with reference-first ordering chose an on-reference PEPTIDE
        # over an off-reference small molecule and mis-tiered four receptors we
        # have already curated.
        sm_ag = best(AGONIST_SIDE, "Active", False)
        sm_an = best(ANTAGONIST_SIDE, "Inactive", False)
        ch_ag = best(AGONIST_SIDE, "Active", True)
        ch_an = best(ANTAGONIST_SIDE, "Inactive", True)

        if sm_ag and sm_an:
            tier, why, ag, an = "T1_small_molecule", "", sm_ag, sm_an
        elif ch_ag and ch_an:
            tier, why, ag, an = ("T2_peptide",
                                 "both arms supply a separate polymer chain",
                                 ch_ag, ch_an)
        elif (sm_ag or ch_ag) and (sm_an or ch_an):
            ag = sm_ag or ch_ag
            an = sm_an or ch_an
            tier = "X_mismatched"
            why = ("agonist %s a chain but antagonist %s -- chain count differs "
                   "between the two ligand arms, the one confound this arm "
                   "cannot absorb" % ("IS" if is_chain(ag) else "is NOT",
                                      "IS" if is_chain(an) else "is NOT"))
        else:
            ag = sm_ag or ch_ag
            an = sm_an or ch_an
            tier = "T3_single_sided"
            why = ("no %s side available after skipping allosteric and "
                   "antibody ligands" % ("agonist" if ag is None else "antagonist"))

        rows.append({
            "receptor_slug": slug,
            "cluster": p["cluster"],
            "panel_tier": freeze.get(slug, ""),
            "ligand_tier": tier,
            "tier_note": why,
            "agonist_name": ag["ligand_name"][:44] if ag else "",
            "agonist_modality": ag["modality"] if ag else "",
            "agonist_is_chain": ("1" if is_chain(ag) else "0") if ag else "",
            "agonist_pdb": ag["pdb"] if ag else "",
            "agonist_res": ag["resolution"] if ag else "",
            "agonist_struct_state": ag["structure_state"] if ag else "",
            "agonist_species": ag["structure_species"] if ag else "",
            "agonist_site": ag["site"] if ag else "",
            "agonist_on_our_ref": ("1" if ag["pdb"].upper() in ourref[slug] else "0") if ag else "",
            "antagonist_name": an["ligand_name"][:44] if an else "",
            "antagonist_role": an["role"] if an else "",
            "antagonist_modality": an["modality"] if an else "",
            "antagonist_is_chain": ("1" if is_chain(an) else "0") if an else "",
            "antagonist_pdb": an["pdb"] if an else "",
            "antagonist_res": an["resolution"] if an else "",
            "antagonist_struct_state": an["structure_state"] if an else "",
            "antagonist_species": an["structure_species"] if an else "",
            "antagonist_site": an["site"] if an else "",
            "antagonist_on_our_ref": ("1" if an["pdb"].upper() in ourref[slug] else "0") if an else "",
            "n_allosteric_skipped": n_allo,
            "n_antibody_skipped": n_ab,
        })

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} rows)\n")

    prim = [r for r in rows if r["panel_tier"] == "PRIMARY"]
    def rep(rs, label):
        k = len({r["cluster"] for r in rs})
        mde = 1.218 / (k ** 0.5) if k else float("nan")
        print(f"  {label:<26} {len(rs):>2} receptors  {k:>2} clusters   MDE {mde:.3f}")
        return k
    print("  ON THE FROZEN PRIMARY PANEL (30 receptors / 29 clusters):")
    for t in ("T1_small_molecule", "T2_peptide", "X_mismatched", "T3_single_sided"):
        rep([r for r in prim if r["ligand_tier"] == t], t)
    print()
    t1 = [r for r in prim if r["ligand_tier"] == "T1_small_molecule"]
    t12 = [r for r in prim if r["ligand_tier"] in ("T1_small_molecule", "T2_peptide")]
    rep(t1, "T1 alone (headline)")
    rep(t12, "T1 + T2 (reported apart)")
    print()
    for t in ("T1_small_molecule", "T2_peptide", "X_mismatched"):
        rs = sorted(r["receptor_slug"] for r in prim if r["ligand_tier"] == t)
        print(f"  {t}: {', '.join(rs)}")
    ab = [r for r in prim if int(r["n_antibody_skipped"]) > 0]
    print(f"\n  receptors where an antibody/nanobody ligand was skipped: "
          f"{', '.join(sorted(r['receptor_slug'] for r in ab)) or 'none'}")
    print(f"  total allosteric records skipped: {sum(int(r['n_allosteric_skipped']) for r in rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
