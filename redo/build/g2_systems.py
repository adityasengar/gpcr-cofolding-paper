#!/usr/bin/env python3
"""g2_systems.py -- every dispatchable Group 2 system, one row each.

Group 2 is the LIGAND arm: catalogue E2.1-E2.4.  `g1_systems.py` enumerates the
partner axis and carries `ligand = none` on all 2,039 of its rows; this file is the
other half of that crossing and follows its conventions -- same item/experiment/arm/
receptor_set shape, the same chain-B resolution against `g1_partner_registry.tsv` and
`g1_cognate.tsv`, and the same two budget grains (`predictions_pooled` at n=10,
`predictions_percell` at n=50).

THE DESIGN
----------
Ligand role x partner presence, crossed.  Four ligand levels --

    none | full_agonist | antagonist | decoy_lig

-- and the partner axis at `R0_apo` plus a cognate rung.  `antagonist` is a LEVEL,
not a molecule: it resolves per receptor to a `neutral_antagonist` (13 of the 16
curated T1 receptors) or, where the receptor has no plain antagonist at all, to an
`inverse_agonist` (ADRB1, B1B1U5, OPSD).  D-2026-09-12-f relaxed amendment C-1 to
admit those three, and it requires that an inverse agonist is recorded as its OWN
role and never relabelled -- so every row carries both `ligand` (the design level)
and `ligand_role_actual` (the pharmacology), and gate check G-4 fails if they are
conflated.

THREE THINGS THIS FILE DELIBERATELY DOES NOT DO
-----------------------------------------------
1. **It does not invent a decoy.**  `DRULE_CHEMBL_SCOPE.md` specifies the rule,
   `drule_pool.py` implements it, and the pool does not exist because it needs a
   pinned ChEMBL release download -- Aditya's decision, not the script's.  So the
   decoy arm is enumerated as rows whose ligand is `UNRESOLVED:drule_pool` and whose
   `dispatch_status` says so.  The alternative -- omitting the arm -- makes a
   blocked experiment look exactly like one nobody thought of, which is the failure
   `drule_targets.py` records for B1B1U5.
2. **It does not choose the cognate rung.**  Whether the crossing runs at `R3_ct21`
   (the length in the title) or at `R7_full` (what Block C's "cognate" arm actually
   supplied, so the only rung that makes the 40,800 existing predictions a
   comparator) is a PI decision with a cost.  Both are enumerated, costed apart, and
   marked `pi_choice`.
3. **It does not pool a tier.**  T1 is the headline.  T2 (2 receptors, peptide on
   both sides) and T3 (7, one side a chain and one not) are enumerated in their own
   arms with `pool_group` saying REPORTED_APART, because at 2 and 7 clusters neither
   can carry the contrast and saying so is the point of tiering them.

Inputs:
    inputs/ligand_tiers.tsv          the tier assignment + the census's own picks
    inputs/ligand_set_redo.tsv       the 16 enacted picks, and PD2R2 blocked
    inputs/g1_receptors.tsv          the receptor axis
    inputs/g1_panel_freeze.tsv       the frozen primary panel
    inputs/g1_partner_registry.tsv   chain-B constructs, keyed by sha256
    inputs/g1_cognate.tsv            receptor -> cognate subtype
    protocol/received/approved_2026_09_12/ligand_set{,_tier3}.csv
                                     paper_af3's curation for the 9 inherited T1
                                     receptors.  READ ONLY, and every row sourced
                                     from it is labelled INHERITED so that the
                                     largest unverified surface in the ligand arm
                                     stays visible in the dispatch table itself.

Usage:  python3 redo/build/g2_systems.py
        python3 redo/build/manifest.py
"""
import csv
import os
import sys
from collections import defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, PROTOCOL          # noqa: E402

OUT = os.path.join(INPUTS, "g2_systems.csv")
APPROVED = os.path.join(PROTOCOL, "received", "approved_2026_09_12")
BACKBONES_4 = "boltz2|openfold3|protenix|chai1"
BB1 = "boltz2"

# The decoy pool is not built.  Every decoy cell points here instead of at a
# molecule, and nothing that points here may be dispatched.
DECOY_UNRESOLVED = "UNRESOLVED:drule_pool"

# DRULE_CHEMBL_SCOPE.md's pool report asks how many clusters yield >=3 accepted
# decoys.  A decoy arm run on ONE hand-picked molecule per receptor -- which is what
# the frozen campaign did -- makes "decoy" and "that particular molecule" the same
# term, which is the D2 collision in another costume.  So the arm's n is split
# across draws exactly as g1_systems.py splits a scramble arm's n across its five
# permutations: same total predictions, and the molecule becomes a random effect.
DECOY_DRAWS = 3

# ---------------------------------------------------------------------------
# The arms.  `partners` are registry `construct` values (plus the pseudo-construct
# R0_apo, which has no chain B).  `ligands` are DESIGN LEVELS, resolved per receptor
# below.  `msa_partner = off` on every arm, for the reason SEQUENCES.md 6.1 gives
# and g1_systems.py extends to every rung: a ladder whose short rungs are MSA-free
# and whose long rungs are not confounds length with alignment depth.  The ligand
# axis inherits that condition unchanged so that a G1 row and a G2 row at the same
# rung differ in the ligand and in nothing else.
# ---------------------------------------------------------------------------
ARMS = [
    # ---- E2.2 the crossing proper, at the title's rung -------------------
    dict(item="G6a/G6b", exp="E2.2", arm="ligand_x_partner", rset="LIG_T1",
         partners=["R0_apo", "R3_ct21"],
         ligands=["none", "full_agonist", "antagonist"],
         bb=BACKBONES_4, n=(10, 50), draws=1, pi_choice="",
         note="the 2x2 the paper's second title clause needs, plus the ligand-free "
              "level that makes it a crossing rather than two contrasts. The "
              "ligand-free cells are the SAME cells as g1_systems.csv's R0_apo and "
              "R3_ct21 on these receptors -- run once, read twice; they are "
              "enumerated here so the design is legible as a cube and the gate can "
              "check it is complete, not so they are dispatched twice"),
    dict(item="P2b", exp="E2.2", arm="ligand_x_partner_pilot", rset="LIG_T1",
         partners=["R0_apo", "R3_ct21"],
         ligands=["none", "full_agonist", "antagonist"],
         bb=BB1, n=(10, 10), draws=1, pi_choice="",
         note="single-backbone pilot. Its job is to find the harness defects -- a "
              "ligand entity that does not parse, a CCD that resolves to the wrong "
              "isomer -- before four backbones pay for them"),

    # ---- E2.4 the decoy, as a THIRD LEVEL of the same factor --------------
    dict(item="G6d", exp="E2.4", arm="decoy_third_role", rset="LIG_T1",
         partners=["R0_apo", "R3_ct21"], ligands=["decoy_lig"],
         bb=BACKBONES_4, n=(10, 50), draws=DECOY_DRAWS, pi_choice="",
         note="NOT a separate experiment: the decoy is the third level of the "
              "ligand-role factor and is crossed with the partner axis exactly like "
              "the agonist and the antagonist. That is what Block C deployed "
              "(verified on rows.tier3.v2.csv: decoy 7,200 apo / 7,200 cognate, "
              "balanced against agonist and antagonist) and it is the right shape, "
              "because the comparison yu2026domainmotion forces is decoy against "
              "antagonist at the SAME partner level. What changes is the molecule: "
              "a pool from a pinned ChEMBL release under DRULE_CHEMBL_SCOPE.md, the "
              "property window ENFORCED rather than reported, and n split across "
              "draws so the decoy is a random effect. UNRESOLVED until the pool "
              "exists"),

    # ---- E2.2 the same crossing at the full subunit -- PI CHOICE ----------
    dict(item="G6f(option)", exp="E2.2", arm="ligand_x_partner_full_subunit",
         rset="LIG_T1", partners=["R7_full"],
         ligands=["none", "full_agonist", "antagonist"],
         bb=BACKBONES_4, n=(10, 50), draws=1,
         pi_choice="cognate rung for the ligand crossing: R3_ct21 | R7_full | both",
         note="OPTION. The apo half of the crossing is shared with G6a/G6b, so this "
              "arm is the cognate half only and its cost is additive, not double. "
              "R7_full is what Block C's 'cognate' arm supplied, so this is the only "
              "rung at which the 40,800 existing predictions are a comparator; "
              "R3_ct21 is the length the title claims. Running both also answers "
              "whether the ligand x partner interaction depends on partner length, "
              "which nothing in the corpus has asked"),
    dict(item="G6fd(option)", exp="E2.4", arm="decoy_third_role_full_subunit",
         rset="LIG_T1", partners=["R7_full"], ligands=["decoy_lig"],
         bb=BACKBONES_4, n=(10, 50), draws=DECOY_DRAWS,
         pi_choice="cognate rung for the ligand crossing: R3_ct21 | R7_full | both",
         note="OPTION, and UNRESOLVED. The decoy level of G6f"),

    # ---- E2.3 the efficacy ladder's fourth level -------------------------
    dict(item="G21(proposed)", exp="E2.3", arm="efficacy_ladder_inverse_agonist",
         rset="LIG_T1_INV_EXTRA", partners=["R0_apo", "R3_ct21"],
         ligands=["inverse_agonist"],
         bb=BACKBONES_4, n=(10, 50), draws=1, pi_choice="",
         note="E2.3 asks whether the pocket response is graded with efficacy. Three "
              "of the four levels are already in G6a/G6b. This arm adds the "
              "inverse agonist ONLY on receptors whose antagonist level is a plain "
              "neutral antagonist -- on ADRB1, B1B1U5 and OPSD the antagonist level "
              "IS an inverse agonist, so running it there would be running one cell "
              "twice. The receptors left are those whose inherited curation already "
              "carries an inverse_agonist row with a SMILES; curation cost zero, "
              "which is what makes this arm cheap and what caps its size"),

    # ---- E2.2 on the tiers that are reported apart -----------------------
    dict(item="G6-T2", exp="E2.2", arm="ligand_x_partner_peptide_tier",
         rset="LIG_T2", partners=["R0_apo", "R3_ct21"],
         ligands=["none", "full_agonist", "antagonist"],
         bb=BACKBONES_4, n=(10, 50), draws=1, pi_choice="",
         note="T2: both ligands enter as a separate polymer CHAIN. Never pooled "
              "into T1 -- 2 receptors and 2 clusters cannot carry a contrast, and "
              "a chain ligand is a different input modality from a HETATM "
              "component, which is the axis D-2026-09-12-f tiered on. At R3_ct21 a "
              "peptide ligand and a 21-residue peptide partner are two peptide "
              "chains in one prediction; that is a harness hazard, not a design "
              "one, and it is why this tier runs its own arm"),
    dict(item="G6-T3", exp="E2.2", arm="ligand_x_partner_mixed_tier",
         rset="LIG_T3", partners=["R0_apo", "R3_ct21"],
         ligands=["none", "full_agonist", "antagonist"],
         bb=BACKBONES_4, n=(10, 50), draws=1, pi_choice="",
         note="T3: one arm is a chain and the other is not, so WITHIN each receptor "
              "the agonist/antagonist contrast is confounded with input modality. "
              "Never pooled into T1 and never read as a ligand-class result on its "
              "own; its use is as the modality contrast T1 cannot supply, read "
              "against T1's small-molecule-only cells"),

    # ---- the receptor that is tier-eligible and refused ------------------
    dict(item="G6x", exp="E2.2", arm="blocked_ligand_identity",
         rset="LIG_T1_BLOCKED", partners=["R0_apo", "R3_ct21"],
         ligands=["full_agonist"],
         bb=BACKBONES_4, n=(0, 0), draws=1, pi_choice="",
         note="PD2R2 is T1-eligible and REFUSED. Carried at zero predictions so the "
              "absence is a row rather than a silence: a receptor that vanishes from "
              "a table looks exactly like one nobody considered. Unblocking it means "
              "an agonist identity for 8XXV, not a file"),
]


def tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def csvf(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
def load_inherited():
    """paper_af3's curation, keyed (receptor, role) -> row + its file.

    Read-only, and every row that comes from here is labelled INHERITED in the
    output.  D-2026-09-12-f calls these nine receptors the largest remaining
    unverified surface in the ligand arm; a dispatch table that does not say which
    rows they are hides exactly that.
    """
    out = {}
    for f in ("ligand_set.csv", "ligand_set_tier3.csv"):
        p = os.path.join(APPROVED, f)
        if not os.path.exists(p):
            continue
        for r in csvf(p):
            out[(r["receptor"], r["ligand_role"])] = dict(r, _src=f)
    return out


def main():
    problems = []
    need = ["ligand_tiers.tsv", "ligand_set_redo.tsv", "g1_receptors.tsv",
            "g1_panel_freeze.tsv", "g1_partner_registry.tsv", "g1_cognate.tsv"]
    for f in need:
        if not os.path.exists(os.path.join(INPUTS, f)):
            problems.append(f"{f}: absent -- run its generator first")
    if problems:
        sys.stderr.write("!! " + "\n!! ".join(problems) + "\n")
        return 1

    tiers = {r["receptor_slug"]: r for r in tsv(os.path.join(INPUTS, "ligand_tiers.tsv"))}
    rec = {r["slug"]: r for r in tsv(os.path.join(INPUTS, "g1_receptors.tsv"))}
    frz = {r["receptor_slug"]: r
           for r in tsv(os.path.join(INPUTS, "g1_panel_freeze.tsv"))}
    reg = tsv(os.path.join(INPUTS, "g1_partner_registry.tsv"))
    cog = {r["receptor_slug"]: r
           for r in tsv(os.path.join(INPUTS, "g1_cognate.tsv"))
           if r["rung"] == "R3_ct21"}

    # our own enactment: only rows that actually enacted count as curated
    redo, blocked = defaultdict(dict), {}
    for r in tsv(os.path.join(INPUTS, "ligand_set_redo.tsv")):
        if r["status"] == "enacted":
            redo[r["receptor_slug"]][r["ligand_role"]] = r
        else:
            blocked[r["receptor_slug"]] = r
    inh = load_inherited()

    try:
        from rdkit import Chem, RDLogger
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        Chem = None

    # ---------------------------------------------------------------- panels
    # The primary panel is g1_panel_freeze's core_frozen set; verified here to be
    # the same set ligand_tiers calls PRIMARY rather than assumed to be.
    primary = {s for s, r in frz.items() if r["core_frozen"] == "yes"}
    if primary != {s for s, r in tiers.items() if r["panel_tier"] == "PRIMARY"}:
        sys.stderr.write("!! g1_panel_freeze's frozen core and ligand_tiers' PRIMARY "
                         "disagree -- one of them is stale\n")
        return 1

    def tier_members(t):
        return sorted(s for s in primary if tiers[s]["ligand_tier"] == t)

    t1_all = tier_members("T1_small_molecule")
    t1 = [s for s in t1_all if s not in blocked]        # curated T1
    t1_blocked = [s for s in t1_all if s in blocked]

    def off_state_role(slug):
        """The pharmacology the `antagonist` LEVEL resolves to for this receptor."""
        raw = tiers[slug]["antagonist_role"]
        return "inverse_agonist" if raw == "inverse_agonist" else "neutral_antagonist"

    def has_ligand(slug, role):
        if role in redo.get(slug, {}):
            return True
        r = inh.get((slug, role))
        return bool(r and (r.get("smiles", "").strip()
                           or r.get("peptide_sequence", "").strip()))

    # E2.3's extra level: an inverse agonist that is NOT already the antagonist
    # level of that receptor, and that is already curated (cost zero).
    t1_inv_extra = [s for s in t1
                    if off_state_role(s) != "inverse_agonist"
                    and has_ligand(s, "inverse_agonist")]

    RSET = {"LIG_T1": t1, "LIG_T1_BLOCKED": t1_blocked,
            "LIG_T1_INV_EXTRA": t1_inv_extra,
            "LIG_T2": tier_members("T2_peptide"),
            "LIG_T3": tier_members("T3_mixed")}
    POOL = {"LIG_T1": "T1_HEADLINE", "LIG_T1_BLOCKED": "T1_HEADLINE",
            "LIG_T1_INV_EXTRA": "T1_HEADLINE",
            "LIG_T2": "T2_REPORTED_APART", "LIG_T3": "T3_REPORTED_APART"}

    # --------------------------------------------------------- chain B lookup
    index = defaultdict(list)
    for r in reg:
        if r["held"] == "yes":
            index[r["construct"]].append(r)

    def resolve_partner(construct, slug):
        """-> (length, sha256, family_rule, evidence_class, n_chains_b)"""
        if construct == "R0_apo":
            return "0", "-", "-", "n/a", 0
        c = cog.get(slug)
        if not c or not c["cognate_subtype"]:
            return ("UNRESOLVED", "PENDING:PI-DECISION",
                    "PENDING:PI-DECISION", (c or {}).get("evidence_class", ""), 1)
        sub = c["cognate_subtype"]
        hit = [e for e in index.get(construct, []) if e["family"] == sub]
        if not hit:
            return ("UNRESOLVED", f"UNRESOLVED:no {construct} for {sub}",
                    f"{sub} ({c['cognate_family']})", c["evidence_class"], 1)
        return (hit[0]["length"], hit[0]["sha256"],
                f"{sub} ({c['cognate_family']}, {c['evidence_class']})",
                c["evidence_class"], 1)

    # --------------------------------------------------------- ligand lookup
    def resolve_ligand(slug, level):
        """A design LEVEL -> the molecule, its source, and whether it can dispatch.

        Returns a dict.  `role_actual` is the pharmacology and is never the level:
        D-2026-09-12-f requires that an inverse agonist stays an inverse agonist all
        the way into analysis, and the only way to guarantee that is to carry both.
        """
        if level == "none":
            return dict(role_actual="none", name="-", ccd="-", inchikey="-",
                        is_chain="0", source="-", status="RESOLVED_NO_LIGAND",
                        key_by="-", flag="")
        if level == "decoy_lig":
            return dict(role_actual="decoy_lig", name=DECOY_UNRESOLVED,
                        ccd="-", inchikey="-", is_chain="0",
                        source="PENDING:drule_pool.py (needs a pinned ChEMBL release)",
                        status="UNRESOLVED_DECOY_POOL", key_by="inchikey",
                        flag="pool not built")
        role = off_state_role(slug) if level == "antagonist" else level

        r = redo.get(slug, {}).get(role)
        if r:
            # A ligand that enters as a separate polymer CHAIN needs a SEQUENCE.
            # `ligand_set_redo.tsv` carries none -- not even for SSR2's agonist,
            # which has a SMILES for somatostatin, and a SMILES is not a chain
            # input.  D-2026-09-12-f's whole axis is chain-ness, so a chain row
            # with no sequence is unresolved however much chemistry sits beside it.
            return dict(role_actual=role, name=r["ligand_name"],
                        ccd=r["ligand_ccd"] or "-",
                        inchikey=r["inchikey"] or "-",
                        is_chain=r["is_peptide"],
                        source=f"REDO:ligand_set_redo.tsv ({r['bound_pdb']})",
                        status=("UNRESOLVED_CHAIN_NO_SEQUENCE"
                                if r["is_peptide"] == "1" else "RESOLVED_REDO"),
                        key_by=r["must_key_by"],
                        flag=("ccd_resolves_to_other_isomer"
                              if r["ccd_resolves_to_other_isomer"] == "1" else ""))

        r, relabelled = inh.get((slug, role)), False
        if r is None and role in ("neutral_antagonist", "inverse_agonist"):
            # The inherited files key the off-state ligand as `neutral_antagonist`
            # whatever GPCRdb calls it.  AGTR1's row is CCD `OLM` at 4ZUD --
            # olmesartan, which GPCRdb types `Inverse agonist`; that is the L-3
            # error class (carazolol) in somebody else's file.  The molecule is
            # real and its bytes are there, so it is taken under the role the
            # census assigns, ONLY when the deposition matches the one the census
            # picked, and the disagreement is flagged rather than absorbed.
            other = ("inverse_agonist" if role == "neutral_antagonist"
                     else "neutral_antagonist")
            cand = inh.get((slug, other))
            if cand and cand.get("bound_pdb", "").upper() == \
                    tiers[slug]["antagonist_pdb"].upper():
                r, relabelled = cand, True
        if r:
            smi = (r.get("smiles") or "").strip()
            seq = (r.get("peptide_sequence") or "").strip()
            ccd = (r.get("ccd_code") or "").strip()
            # F-18's column shift: an unescaped comma inside a note field pushes
            # every later column along by two, so ccd_code ends up holding prose.
            # Detected by shape -- a CCD code is <=5 characters and has no spaces --
            # rather than by hard-coding the one row we happen to know about.
            malformed = bool(ccd) and (" " in ccd or len(ccd) > 5)
            ik = "-"
            if Chem and smi:
                m = Chem.MolFromSmiles(smi)
                ik = Chem.MolToInchiKey(m) if m is not None else "SMILES_DOES_NOT_PARSE"
            chain = r.get("is_peptide") == "TRUE"
            if chain:
                # the received bundle DOES carry sequences for its chain ligands,
                # which is the one place a chain row resolves
                st = "INHERITED_CHAIN_SEQUENCE" if seq else "UNRESOLVED_CHAIN_NO_SEQUENCE"
            elif smi:
                st = ("INHERITED_SMILES_PARSED" if ik not in ("-", "SMILES_DOES_NOT_PARSE")
                      else "INHERITED_SMILES_UNPARSEABLE" if ik == "SMILES_DOES_NOT_PARSE"
                      else "INHERITED_SMILES_PRESENT_NOT_CHECKED")
            elif seq:
                st = "INHERITED_CHAIN_SEQUENCE"
            else:
                st = "UNRESOLVED_INHERITED_ROW_EMPTY"
            return dict(role_actual=role, name=r.get("iupac_name") or r.get("ligand_variant") or role,
                        ccd=("MALFORMED_PROVENANCE" if malformed else (ccd or "-")),
                        inchikey=ik, is_chain="1" if r.get("is_peptide") == "TRUE" else "0",
                        source=f"INHERITED:{r['_src']} ({r.get('bound_pdb') or 'no pdb'})"
                        + (f" [source row keys it as {r['ligand_role']}]"
                           if relabelled else ""),
                        status=st, key_by="inchikey",
                        flag="; ".join(f for f in (
                            "column_shift_in_source_row" if malformed else "",
                            "source_row_role_disagrees_with_gpcrdb" if relabelled else "")
                            if f))

        # Nothing anywhere.  The census knows a molecule exists; nobody has curated
        # it into bytes we can dispatch.
        t = tiers.get(slug, {})
        nm = t.get("agonist_name") if role == "full_agonist" else t.get("antagonist_name")
        return dict(role_actual=role, name=(nm or "") or "UNRESOLVED",
                    ccd="-", inchikey="-",
                    is_chain=(t.get("agonist_is_chain") if role == "full_agonist"
                              else t.get("antagonist_is_chain")) or "0",
                    source="UNCURATED (named in ligand_tiers.tsv, no bytes held)",
                    status="UNRESOLVED_UNCURATED", key_by="inchikey", flag="")

    # ------------------------------------------------------------ enumerate
    rows = []
    for a in ARMS:
        members = RSET[a["rset"]]
        nbb = len(a["bb"].split("|"))
        share = a["draws"]
        for slug in members:
            for partner in a["partners"]:
                plen, psha, pfam, pev, nb = resolve_partner(partner, slug)
                for level in a["ligands"]:
                    lg = resolve_ligand(slug, level)
                    if a["rset"] == "LIG_T1_BLOCKED":
                        lg = dict(lg, status="BLOCKED_LIGAND_IDENTITY",
                                  name=(blocked[slug]["ligand_name"] or "REFUSED"),
                                  source="REFUSED:ligand_set_redo.tsv")
                    is_chain = lg["is_chain"] == "1"
                    # dispatchable only if EVERY input is resolved
                    if lg["status"].startswith(("UNRESOLVED", "BLOCKED")):
                        ds = ("BLOCKED_UNRESOLVED_DECOY_POOL"
                              if lg["status"] == "UNRESOLVED_DECOY_POOL"
                              else lg["status"] if lg["status"].startswith("BLOCKED")
                              else "BLOCKED_" + lg["status"])
                    elif psha.startswith(("UNRESOLVED", "PENDING")):
                        ds = "BLOCKED_UNRESOLVED_PARTNER"
                    else:
                        ds = "READY"
                    nlo, nhi = a["n"][0] // share, a["n"][1] // share
                    dispatchable = ds == "READY"
                    rows.append(dict(
                        item=a["item"], experiment=a["exp"], arm=a["arm"],
                        receptor_set=a["rset"], pool_group=POOL[a["rset"]],
                        enumeration="per_receptor",
                        receptor_slug=slug,
                        receptor_uniprot=rec[slug]["uniprot"],
                        receptor_organism=rec[slug]["organism"],
                        receptor_cluster=rec[slug]["cluster"],
                        panel_tier=frz[slug]["tier"],
                        ligand_tier=tiers[slug]["ligand_tier"],
                        chain_a_source="PENDING:SEQ_RECEPTORS.md",
                        partner_level=("apo" if partner == "R0_apo" else "cognate"),
                        chain_b_construct=partner,
                        chain_b_family_rule=pfam,
                        chain_b_len=plen,
                        chain_b_sha256=psha,
                        cognate_evidence_class=pev or "n/a",
                        supplied_partner_family=frz[slug]["supplied_partner_family"],
                        supplied_partner_subtype=frz[slug]["supplied_partner_subtype"],
                        ligand=level,
                        ligand_role_actual=lg["role_actual"],
                        ligand_name=lg["name"],
                        ligand_ccd=lg["ccd"],
                        ligand_inchikey=lg["inchikey"],
                        ligand_is_chain=lg["is_chain"],
                        ligand_identity_source=lg["source"],
                        ligand_identity_status=lg["status"],
                        ligand_must_key_by=lg["key_by"],
                        ligand_flag=lg["flag"],
                        n_shared_draws=share,
                        n_chains=1 + nb + (1 if is_chain else 0),
                        n_nonpolymer_entities=(0 if level == "none" or is_chain else 1),
                        partner_msa=("n/a" if partner == "R0_apo" else "off"),
                        receptor_msa="on (default)",
                        backbones=a["bb"],
                        n_pooled=nlo, n_percell=nhi,
                        predictions_pooled=nbb * nlo if dispatchable else 0,
                        predictions_percell=nbb * nhi if dispatchable else 0,
                        blocked_predictions_pooled=0 if dispatchable else nbb * nlo,
                        blocked_predictions_percell=0 if dispatchable else nbb * nhi,
                        dispatch_status=ds,
                        pi_choice=a["pi_choice"],
                        note=a["note"]))

    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # ---------------------------------------------------------- reporting
    def clusters(slugs):
        return len({rec[s]["cluster"] for s in slugs})

    sys.stderr.write(f"# wrote {len(rows)} systems -> {OUT}\n\n")
    sys.stderr.write("# panels (receptors / paralog clusters)\n")
    for k in ("LIG_T1", "LIG_T1_BLOCKED", "LIG_T1_INV_EXTRA", "LIG_T2", "LIG_T3"):
        m = RSET[k]
        sys.stderr.write(f"#   {k:18s} {len(m):3d} receptors, {clusters(m):3d} clusters"
                         f"   {' '.join(m)}\n")
    t1c = clusters(t1)
    sys.stderr.write(f"#   T1 eligible incl. blocked: {len(t1_all)} receptors, "
                     f"{clusters(t1_all)} clusters\n")
    sys.stderr.write(f"#   headline MDE at k={t1c}: {1.218 / t1c ** 0.5:.3f}"
                     f"   (T1+T2 k={t1c + clusters(RSET['LIG_T2'])}: "
                     f"{1.218 / (t1c + clusters(RSET['LIG_T2'])) ** 0.5:.3f}, "
                     f"all tiers k={t1c + clusters(RSET['LIG_T2']) + clusters(RSET['LIG_T3'])}: "
                     f"{1.218 / (t1c + clusters(RSET['LIG_T2']) + clusters(RSET['LIG_T3'])) ** 0.5:.3f})\n\n")

    per = defaultdict(lambda: [0, 0, 0, 0, 0])
    for r in rows:
        s = per[r["item"]]
        s[0] += 1
        s[1] += r["predictions_pooled"]
        s[2] += r["predictions_percell"]
        s[3] += r["blocked_predictions_pooled"]
        s[4] += r["blocked_predictions_percell"]
    sys.stderr.write(f"{'item':16s} {'cells':>6s} {'preds@10':>10s} {'preds@50':>10s} "
                     f"{'blocked@10':>11s} {'blocked@50':>11s}\n")
    for k in sorted(per):
        n, p, q, bp, bq = per[k]
        sys.stderr.write(f"{k:16s} {n:6d} {p or '-':>10} {q or '-':>10} "
                         f"{bp or '-':>11} {bq or '-':>11}\n")
    tp = sum(v[1] for v in per.values())
    tq = sum(v[2] for v in per.values())
    bp = sum(v[3] for v in per.values())
    bq = sum(v[4] for v in per.values())
    sys.stderr.write(f"{'TOTAL':16s} {len(rows):6d} {tp:>10,} {tq:>10,} "
                     f"{bp:>11,} {bq:>11,}\n")

    # g1_systems.py's face_scramble arm splits n=(10,50) across 3 draws and lands
    # on 9 and 48; the same integer division happens here, and it is reported
    # rather than hidden, because a decoy arm quietly running 9 where the agonist
    # arm runs 10 is an unbalanced design that nobody would see in the totals.
    trunc = sorted({(a["item"], a["draws"], a["n"], a["draws"] * (a["n"][0] // a["draws"]),
                     a["draws"] * (a["n"][1] // a["draws"]))
                    for a in ARMS if a["draws"] > 1
                    and (a["n"][0] % a["draws"] or a["n"][1] % a["draws"])})
    if trunc:
        sys.stderr.write("\n# draw split does not divide n exactly (same convention "
                         "as g1_systems.py's face_scramble)\n")
        for it, d, nom, lo, hi in trunc:
            sys.stderr.write(f"#   {it:16s} {d} draws: nominal n={nom[0]}/{nom[1]}, "
                             f"realised {lo}/{hi} per receptor per cell\n")

    st = defaultdict(int)
    for r in rows:
        st[r["dispatch_status"]] += 1
    sys.stderr.write("\n# dispatch status\n")
    for k in sorted(st, key=lambda k: (-st[k], k)):
        sys.stderr.write(f"#   {k:38s} {st[k]:5d} cells\n")

    src = defaultdict(int)
    for r in rows:
        src[r["ligand_identity_status"]] += 1
    sys.stderr.write("\n# ligand identity\n")
    for k in sorted(src, key=lambda k: (-src[k], k)):
        sys.stderr.write(f"#   {k:38s} {src[k]:5d} cells\n")

    flagged = sorted({(r["receptor_slug"], r["ligand_role_actual"], r["ligand_flag"])
                      for r in rows if r["ligand_flag"]})
    if flagged:
        sys.stderr.write("\n# flags carried into the dispatch table\n")
        for f in flagged:
            sys.stderr.write(f"#   {f[0]:8s} {f[1]:20s} {f[2]}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
