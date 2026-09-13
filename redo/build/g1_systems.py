#!/usr/bin/env python3
"""g1_systems.py — every dispatchable Group 1 system, one row each.

Group 1 is the partner-length ladder: catalogue E1.1-E1.9.  This file turns the
design into a buildable list -- (receptor x chain-B construct x MSA condition x
ligand condition x n) -- and nothing else.  It does not re-derive the design, it
does not cost it, and it does not assign a cognate Galpha.

THREE THINGS THIS FILE DELIBERATELY DOES NOT DO
-----------------------------------------------
1. **It does not choose the cognate Galpha.**  `COUPLING.md` (sibling, concurrent)
   owns that.  Every rung is "the last N residues of the cognate subunit", so the
   partner column is keyed, not filled: `chain_b_family_rule = COGNATE` and
   `chain_b_sha256 = PENDING:COUPLING.md`.  Lengths that are family-invariant
   (11, 15, 21, 26, 36) are resolved anyway; lengths that are not are emitted as a
   measured min-max range over the 16 human families.
2. **It does not supply the receptor chain.**  `SEQ_RECEPTORS.md` (sibling,
   concurrent) owns chain A: construct rule, species, and the hash of the exact
   bytes.  `chain_a_source = PENDING:SEQ_RECEPTORS.md` on every row.
3. **It does not freeze CORE-32.**  `RUN_MATRIX.md` §10.3 records that PANEL.md
   owes the frozen slug list.  `g1_receptors.py` computes a PROVISIONAL one from
   RUN_MATRIX §3.1's written rule applied to PANEL.md §6.1, and it is labelled as
   such on every row.

Inputs (all built by g1_ companions or by the sequence session):
    g1_receptors.tsv          the receptor axis + provisional CORE-32
    g1_partner_registry.tsv   every chain-B construct, keyed by sha256
    g1_midrungs.tsv           the intermediate rungs

Usage:  python3 redo/build/g1_systems.py
"""
import csv
import os
import sys
from collections import defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
OUT = os.path.join(INPUTS, "g1_systems.csv")
BACKBONES_4 = "boltz2|openfold3|protenix|chai1"
BB1 = "boltz2"

# ---------------------------------------------------------------------------
# The arms.  `rungs` are registry `construct` values; `variant` selects within a
# construct where the registry has one.  `msa_partner` is the condition on the
# SUPPLIED chain only -- the receptor's own MSA is on everywhere in Group 1
# (varying it is Group 8, a different factor with a different literature).
#
# `msa_partner = off` is the PRIMARY condition on every rung including R7_full.
# SEQUENCES.md §6 measured why: MSA depth at peptide length tracks conservation,
# not length (endothelin-1, 21 aa, depth 732; a designed 40-mer, depth 1), and the
# alpha5-CT is byte-identical across Gi1/Gi2, Gt1/Gt2/Ggust and Gq/G11, so a
# wild-type-vs-scramble contrast at 21 residues run MSA-on would be a pure depth
# contrast.  §6.1(1)-(2) requires MSA-free on the peptide rungs and on R7_full;
# this file extends it to every rung in between, because a ladder whose short
# rungs are MSA-free and whose long rungs are not has rung length and alignment
# depth perfectly confounded along its whole length -- which is the confound the
# requirement exists to remove.  The MSA-ON arms below are the E1.9 contrast.
# ---------------------------------------------------------------------------
ARMS = [
    # ---- E1.1 the ladder proper -----------------------------------------
    dict(item="G1a/G1b", exp="E1.1", arm="ladder", rset="CORE32",
         rungs=["R0_apo", "R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix",
                "R5_a5plus", "R7_full"],
         family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="the 7 costed ladder rungs; R0_apo has no chain B"),
    dict(item="P1", exp="E1.1", arm="ladder_pilot", rset="CORE32",
         rungs=["R0_apo", "R1_ct11", "R2_ct15", "R3_ct21", "R4_a5helix",
                "R5_a5plus", "R7_full"],
         family_rule="COGNATE", msa_partner="off", ligand="none", bb=BB1, n=(10, 10),
         note="single-backbone pilot, gates G1a/G1b"),

    # ---- E1.1 the intermediate rungs (RUN_MATRIX §3.5) -------------------
    dict(item="G1c/G1d", exp="E1.1", arm="intermediate_nested", rset="CORE32",
         rungs=["M1_h4s6", "M2_h4", "M4_he"],
         family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="the 3 rungs RUN_MATRIX §3.5 costed: one below junker's 50-residue "
              "boundary, one just above, one mid-gap; all nested C-terminal"),
    dict(item="P1b", exp="E1.1", arm="intermediate_pilot", rset="CORE32",
         rungs=["M1_h4s6", "M2_h4", "M4_he"],
         family_rule="COGNATE", msa_partner="off", ligand="none", bb=BB1, n=(10, 10),
         note="mid-rung pilot; 960 predictions decide whether G1c is worth 3,840"),
    dict(item="G1c-opt", exp="E1.1", arm="intermediate_optional", rset="CORE32",
         rungs=["M3_h3"], family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="OPTIONAL 4th intermediate, fills the 61->204 gap; not costed by "
              "RUN_MATRIX §3.5"),
    dict(item="G1e", exp="E1.1", arm="hd_deletion_companion", rset="CORE32",
         rungs=["M5_dHD"], family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="OFF-LADDER: keeps the N terminus, so not a nested suffix. Length-"
              "paired with M4_he but topologically its complement -- M4 keeps the "
              "C-terminal half of the helical domain, M5 deletes the whole of it. "
              "If they agree, length dominates; if not, composition does."),
    dict(item="G1f", exp="E1.1", arm="deposited_minig_anchor", rset="CORE32",
         rungs=["MG_6fuf", "MG_5g53", "MG_8f76"], family_rule="EXPLICIT",
         msa_partner="off", ligand="none", bb=BB1, n=(10, 10),
         note="OFF-LADDER anchor: the literal deposited mini-G entities (6FUF 214 aa "
              "Go, 5G53 229 aa Gs, 8F76 261 aa Gs). Run only on receptors whose "
              "cognate family matches the construct's; ties our synthetic M4/M5 to "
              "a construct that has been crystallised."),

    # ---- E1.1 the wet-lab-matched rungs (mazzoni2000) --------------------
    dict(item="G18a(proposed)", exp="E1.1", arm="wetlab_length_series",
         rset="CORE32", rungs=["R1b_ct13", "R2b_ct17", "R2c_ct19"],
         family_rule="COGNATE",
         msa_partner="off", ligand="none", bb=BACKBONES_4, n=(10, 50),
         note="the wet-lab peptide panel is the last 11, 13, 15, 17, 19 and 21 of "
              "Gas -- a two-residue ladder on RAT A2AR striatal membranes. Five of "
              "the six are already rungs; 13 was not. NO PER-RUNG SIGN IS "
              "PRE-REGISTERED: the abstract calls shorter peptides not effective "
              "while a relay says all six stimulate binding and the 11-mer is "
              "merely less active, and whether that attaches to BINDING or to "
              "SIGNALLING is unresolved. What is pre-registered is the PATTERN -- "
              "monotone in length -- and that binding-like and signalling-like "
              "readouts may be different curves"),
    dict(item="G18b(proposed)", exp="E1.1", arm="wetlab_matched_peptides",
         rset="CORE32_GS", rungs=["R2b_ct17@C379A", "R2c_ct19@C379A",
                                  "R3_ct21@C379A"],
         family_rule="EXPLICIT", msa_partner="off", ligand="none", bb=BB1,
         n=(10, 10),
         note="the three peptides mazzoni2000 synthesised, byte for byte. C379A is "
              "a Gs-specific construct detail of that paper (the aligned position "
              "in Gi1/Gq/Gt1/G13 is not a cysteine), so this is an anchor arm and "
              "not a rung. Gs-coupled receptors only"),

    # ---- E1.1 the alpha5 tip that was actually crystallised --------------
    dict(item="G19(proposed)", exp="E1.1", arm="reference_matched_tip",
         rset="REFCHIMERA_CORE32", rungs=["reftip_ct11", "reftip_ct21"],
         family_rule="DEPOSITED_TIP", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="six CORE-32 receptors have a Rule-R ACTIVE reference whose alpha5 "
              "tip is not canonical for any of the 16 human Galpha. Supplying the "
              "deposited tip alongside the wild-type one measures whether the "
              "model cares about the 2-of-11 / 8-of-21 residues that separate "
              "them. Costs nothing to build; the bytes are in the reference. "
              "OPSD's deposited partner is an 11-residue peptide, so it has no "
              "reftip_ct21 cell"),

    # ---- E1.1 the ten chimeric-reference receptors, extension tier -------
    dict(item="G20(extension)", exp="E1.1", arm="chimeric_ref_extension",
         rset="EXT_CHIMERA", rungs=["R0_apo", "R3_ct21", "R7_full"],
         family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 10),
         note="DECISION 1: ineligible for the primary panel because the deposited "
              "active reference carries an engineered alpha5 tip 8 of 21 residues "
              "from canonical Gq at the title's rung -- a systematic construct "
              "mismatch at exactly the residues under study. Fully specified and "
              "dispatchable here, read against G19's matched control, never "
              "pooled with the primary panel"),

    # ---- E1.1 wide replication ------------------------------------------
    dict(item="G2", exp="E1.1", arm="wide_replication", rset="C1_REST",
         rungs=["R0_apo", "R3_ct21", "R7_full"], family_rule="COGNATE",
         msa_partner="off", ligand="none", bb=BACKBONES_4, n=(10, 10),
         note="the other 32 C1 census receptors at three rungs"),

    # ---- E1.2 + alpha5-null controls -------------------------------------
    dict(item="G3a/G3b", exp="E1.2", arm="a5null", rset="CORE32",
         rungs=["R6a_da5", "R6b_a5perm", "R6c_a5polyA"], family_rule="COGNATE",
         msa_partner="off", ligand="none", bb=BACKBONES_4, n=(10, 50),
         note="R6b is the true bulk control (SEQUENCES.md §1). Gate: Galpha-chain "
              "pLDDT + Ras-domain integrity before G3b dispatches"),
    dict(item="G3a/G3b", exp="E1.2", arm="non_ga_bulk", rset="CORE32",
         rungs=["ct21@gcn4_window", "ubiquitin", "KaiB_2QKEE"],
         family_rule="FAMILY_INVARIANT", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="the 3 non-Galpha bulk arms RUN_MATRIX §10.3 asked this session to "
              "name; all three bytes are held and hash-verified"),

    # ---- E1.3 composition and order controls at the title's length -------
    dict(item="G4a/G4b", exp="E1.3", arm="composition_controls", rset="CORE32",
         rungs=["ct21@reversed", "ct21@polyA",
                "ct21@scramble#1/5", "ct21@scramble#2/5", "ct21@scramble#3/5",
                "ct21@scramble#4/5", "ct21@scramble#5/5",
                "ct21@face_scramble#1/3", "ct21@face_scramble#2/3",
                "ct21@face_scramble#3/3"],
         family_rule="COGNATE", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(10, 50),
         note="4 ARMS, 10 dispatch cells: reversed, polyA, scramble (5 draws), "
              "face_scramble (3 draws). Split the arm's n across its draws so the "
              "permutation is a random effect rather than a single draw; total "
              "predictions unchanged. wt is R3_ct21, already in G1a/G1b"),

    # ---- E1.4 family swap -------------------------------------------------
    dict(item="G9", exp="E1.4", arm="family_swap", rset="CORE32",
         rungs=["R3_ct21"], family_rule="NONCOGNATE_MAXHAM", msa_partner="off",
         ligand="none", bb=BACKBONES_4, n=(50, 50),
         note="non-cognate alpha5-CT at the title's length. Read family contrasts "
              "at R3_ct21 and never at R7_full: at R7 the Gs arm supplies 44 more "
              "residues than the Gt arm, so a family contrast there is partly a "
              "length contrast (RUN_MATRIX §3.5)"),

    # ---- E1.6 the natural single-residue pair ----------------------------
    dict(item="G12", exp="E1.6", arm="gi_gt_single_residue", rset="CORE32",
         rungs=["R1_ct11"], family_rule="GI_GT_PAIR", msa_partner="off",
         ligand="none", bb=BACKBONES_4, n=(50, 50),
         note="AT R1_ct11, NOT R3_ct21. Gi1/Gt1 differ at 1 position at ct11, 2 at "
              "ct15, 2 at ct21, 4 at a5helix (recomputed). RUN_MATRIX anchors G12 "
              "at R3_ct21, where it is a 2-substitution pair and not the "
              "single-residue experiment it is named for"),

    # ---- E1.5 the per-position scan --------------------------------------
    dict(item="G10", exp="E1.5", arm="ala_scan", rset="G10_SCAN",
         rungs=[f"ct21@ala_pos{i:02d}" for i in range(1, 22)],
         family_rule="COGNATE", msa_partner="off", ligand="none", bb=BB1,
         n=(20, 20),
         note="21 single-alanine substitutions on a 21-residue chain. Runs "
              "MSA-free, which is the primary condition anyway -- so the "
              "masters2025physics retrieval null cannot be the explanation of a "
              "null here, by construction. Audit and ship the partner MSA per arm"),
    dict(item="G10b", exp="E1.5", arm="gi_to_gs_series", rset="G10_SCAN",
         rungs=[f"ct21@gi2gs_sub{i:02d}" for i in range(1, 16)],
         family_rule="EXPLICIT", msa_partner="off", ligand="none", bb=BB1,
         n=(20, 20),
         note="the Gi->Gs substitution series. THE CATALOGUE SAYS 11; recomputed, "
              "Gi1 and Gs ct21 differ at 15 positions (11 is the ct15 number, 9 is "
              "the ct11 number). 15 single substitutions, not 11"),

    # ---- E1.7 the heterotrimer -------------------------------------------
    dict(item="G11", exp="E1.7", arm="heterotrimer", rset="CORE32",
         rungs=["R8_hetero"], family_rule="COGNATE", msa_partner="off",
         ligand="none", bb=BACKBONES_4, n=(50, 50),
         note="3-chain input: cognate Galpha + Gbeta1 P62873 (340 aa) + Ggamma2 "
              "P59768 (71 aa), both hash-verified. HARNESS CHANGE, not a dispatch. "
              "Its comparator is R7_full, which is the Galpha-only rung"),

    # ---- E1.8 the uncoupling mutants -- NO RUN_MATRIX ITEM ---------------
    dict(item="G16(proposed)", exp="E1.8", arm="uncoupling_full", rset="CORE32_GS",
         rungs=["alphas_F376A_L388A_mutant", "alphas_F376A_L388A_R380A_triple_null"],
         family_rule="EXPLICIT", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(50, 50),
         note="both 394 aa, both already in partners.fasta, both consumed by zero "
              "rows. E1.8 has NO item in RUN_MATRIX §7.1"),
    dict(item="G16(proposed)", exp="E1.8+E1.1", arm="uncoupling_peptide",
         rset="CORE32_GS",
         rungs=["R3_ct21@F376A+L388A", "R3_ct21@F376A+R380A+L388A",
                "R4_a5helix@F376A+L388A", "R4_a5helix@F376A+R380A+L388A"],
         family_rule="EXPLICIT", msa_partner="off", ligand="none",
         bb=BACKBONES_4, n=(50, 50),
         note="E1.8 crossed with E1.1 at zero construction cost (SEQUENCES.md §2.1). "
              "NOT at R1_ct11: F376 and R380 fall outside the 11-mer, so there the "
              "double and triple mutants are the SAME MOLECULE "
              "(sha bf09617db4664cfd for both) -- running both is running one arm "
              "twice, which is the D2 collision one length down"),

    # ---- E1.9 partner MSA on/off -- NO RUN_MATRIX ITEM -------------------
    dict(item="G17(proposed)", exp="E1.9", arm="partner_msa_on", rset="CORE32",
         rungs=["R3_ct21", "R5_a5plus", "R7_full"], family_rule="COGNATE",
         msa_partner="ON", ligand="none", bb=BACKBONES_4, n=(10, 50),
         note="the MSA-on half of the contrast, at three fixed lengths. "
              "SEQUENCES.md §6.1 promotes E1.9 from an optional side-experiment to "
              "a load-bearing component of E1.1; it has NO item in RUN_MATRIX §7.1"),
]

# constructs whose chain-B bytes do not depend on the cognate family
FAMILY_INVARIANT_PREFIX = ("gcn4_window", "ubiquitin", "KaiB_2QKEE", "polyA")


def tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))



def _chain_a():
    """slug -> (construct id, sha256) for chain A.

    Wired 2026-09-13.  Until then this was the hardcoded literal
    "PENDING:SEQ_RECEPTORS.md" on every row, because WHICH receptor sequence to supply
    was an untaken decision (D-OPEN-2026-09-12-j).  Aditya took it -- option (b),
    D-2026-09-13-a -- so the construct exists and the rows may name it.

    A receptor in the systems table with no row in seqrec_trim.tsv resolves to
    UNRESOLVED, never to a default: the whole point of the decision was that a
    silent fallback restores the option the spec calls indefensible.
    """
    import csv as _csv
    src, sha = {}, {}
    path = os.path.join(INPUTS, "seqrec_trim.tsv")
    if not os.path.exists(path):
        sys.exit(f"FAIL: {path} is absent -- chain A cannot be named without it.")
    for r in _csv.DictReader(open(path, encoding="utf-8"), delimiter="	"):
        src[r["slug"]] = f"seqrec_trimmed.fasta:{r['trim_start']}-{r['trim_end']}"
        sha[r["slug"]] = r["trim_sha256"]
    return src, sha


def main():
    chain_a_src, chain_a_sha = _chain_a()
    problems = []
    for f in ("g1_receptors.tsv", "g1_partner_registry.tsv", "g1_midrungs.tsv"):
        p = os.path.join(INPUTS, f)
        if not os.path.exists(p):
            problems.append(f"{f}: absent -- run its generator first")
    if problems:
        sys.stderr.write("!! " + "\n!! ".join(problems) + "\n")
        return 1

    rec = tsv(os.path.join(INPUTS, "g1_receptors.tsv"))
    reg = tsv(os.path.join(INPUTS, "g1_partner_registry.tsv"))

    # DECISION 1+3: the panel is frozen by g1_panel_freeze.py -- chimeric-
    # reference receptors are ineligible for the primary tier and move to the
    # extension tier; AA2AR is a declared override IN.
    frz = {r["receptor_slug"]: r for r in tsv(os.path.join(INPUTS, "g1_panel_freeze.tsv"))}
    core32 = [r for r in rec if frz[r["slug"]]["core_frozen"] == "yes"]
    c1rest = [r for r in rec if frz[r["slug"]]["core_frozen"] != "yes"
              and frz[r["slug"]]["tier"] != "EXTENSION-chimeric-reference"]
    extchim = [r for r in rec
               if frz[r["slug"]]["tier"] == "EXTENSION-chimeric-reference"]
    chim = []
    cpath = os.path.join(INPUTS, "g1_refchimera.tsv")
    if os.path.exists(cpath):
        # every receptor with an engineered alpha5 tip, in either tier: the two
        # that resolve (B1B1U5, OPSD) sit in the primary panel and the ten that do
        # not sit in the extension tier. G19 is the matched control for all of
        # them, which is what makes DECISION 1's exclusion honest rather than
        # convenient.
        affected = {r["slug"] for r in tsv(cpath)
                    if r["is_rule_r_reference"] == "active"}
        chim = [r for r in rec if r["slug"] in affected]
    # the cognate map resolves what used to be keyed: receptor x rung -> sha256,
    # with the evidence class carried per row so a structure read and a convention
    # fallback can never be confused downstream.
    cog, g10, gs32 = {}, [], []
    gpath = os.path.join(INPUTS, "g1_cognate.tsv")
    if os.path.exists(gpath):
        for r in tsv(gpath):
            cog[(r["receptor_slug"], r["rung"])] = r
        g10 = [r for r in core32 if cog.get((r["slug"], "R3_ct21"), {})
               .get("in_g10_scan") == "yes"]
        if len(g10) < 10:   # the freeze may have removed a member; re-rank
            pool = [r for r in core32
                    if cog.get((r["slug"], "R3_ct21"), {}).get("cognate_subtype") == "Gi1"
                    and cog[(r["slug"], "R3_ct21")]["evidence_class"] == "STRUCTURE_EXACT"]
            g10 = sorted(sorted(pool, key=lambda r: (float(r["worse_res"]),
                                                     r["slug"]))[:10],
                         key=lambda r: r["slug"])
        gs32 = [r for r in core32
                if cog.get((r["slug"], "R3_ct21"), {}).get("cognate_subtype") == "Gs"]
    RSET = {"CORE32": core32, "C1_REST": c1rest, "REFCHIMERA_CORE32": chim,
            "G10_SCAN": g10, "CORE32_GS": gs32, "EXT_CHIMERA": extchim}

    # index the registry by (construct, variant-prefix, k)
    index = defaultdict(list)
    for r in reg:
        if r["held"] != "yes":
            continue
        index[r["construct"]].append(r)

    def parse(rung):
        """'ct21@scramble#2/5' -> ('ct21', 'scramble', '2', 5)"""
        share = 1
        if "/" in rung:
            rung, s = rung.rsplit("/", 1)
            share = int(s)
        k = ""
        if "#" in rung:
            rung, k = rung.split("#", 1)
        base, _, variant = rung.partition("@")
        return base, variant, k, share

    def resolve(base, variant, k):
        """-> (length string, sha info, family_dependent?, n_matching)"""
        if base == "R0_apo":
            return "0", "-", False, 1
        if base == "R8_hetero":
            L = sorted({int(r["length"]) for r in index["R7_full"]})
            return f"{L[0]+411}-{L[-1]+411}", "PENDING:COUPLING.md", True, 1
        cands = [r for r in index.get(base, [])
                 if (not variant or r["variant"].startswith(variant))
                 and (not k or r["k"] == k)]
        if not cands:
            return "UNRESOLVED", "UNRESOLVED", False, 0
        L = sorted({int(r["length"]) for r in cands})
        s = {r["sha256"] for r in cands}
        fam_dep = len({r["family"] for r in cands}) > 1 and len(s) > 1
        lstr = str(L[0]) if len(L) == 1 else f"{L[0]}-{L[-1]}"
        return lstr, ("one sha" if len(s) == 1 else "family-dependent"), fam_dep, len(cands)

    rows = []
    for a in ARMS:
        templated = a.get("enumeration") == "templated"
        receptors = RSET.get(a["rset"], [None]) if not templated else [None]
        nbb = len(a["bb"].split("|"))
        for rung in a["rungs"]:
            base, variant, k, share = parse(rung)
            lstr, sinfo, fam_dep, nmatch = resolve(base, variant, k)
            if a["family_rule"] == "COGNATE" and base != "R0_apo":
                sha_col = "PENDING:COUPLING.md"
                fam_col = "COGNATE(receptor)"
            elif a["family_rule"] == "NONCOGNATE_MAXHAM":
                sha_col = "PENDING:COUPLING.md"
                fam_col = "argmax Hamming to cognate at ct21 over {Gs,Gi1,Gq,G13,Gt1}"
            elif a["family_rule"] == "GI_GT_PAIR":
                sha_col = "e16ad41084f6a7b9(Gt1) / 07f3c67495a3d42d(Gi1)"
                fam_col = "Gi1 and Gt1, both supplied to every receptor"
            elif a["family_rule"] == "FAMILY_INVARIANT":
                sha_col = "resolved, family-invariant (see g1_partner_registry.tsv)"
                fam_col = "n/a"
            else:
                sha_col = "resolved, explicit (see g1_partner_registry.tsv)"
                fam_col = "explicit"
            if base == "R0_apo":
                sha_col, fam_col = "-", "-"

            for r in receptors:
                ev = ""
                if a["family_rule"] == "COGNATE" and r is not None \
                        and base != "R0_apo":
                    # One lookup gives the receptor's subtype; every COGNATE
                    # construct -- ladder rung, intermediate rung, alpha5-null,
                    # peptide control -- then resolves in OUR registry by
                    # (construct, variant, k, family).  The map's own rung table
                    # covers only the seven seq_rungs rungs, and it was verified
                    # byte-identical to seq_rungs.tsv, so going through the
                    # registry is the same answer for those and an answer at all
                    # for the rest.
                    c = cog.get((r["slug"], "R3_ct21"))
                    if c:
                        ev = c["evidence_class"]
                        sub = c["cognate_subtype"]
                        if not sub:
                            fam_col = (f"PENDING:PI-DECISION ({c['evidence_class']}: "
                                       f"tip={c['option_a_tip_subtype']} | "
                                       f"scaffold={c['option_b_scaffold_subtype']} | "
                                       f"deposited tip)")
                            sha_col = "PENDING:PI-DECISION"
                        else:
                            fam_col = (f"{sub} ({c['cognate_family']}, "
                                       f"{c['evidence_class']})")
                            hit = [e for e in index.get(base, [])
                                   if e["family"] == sub
                                   and (not variant or e["variant"].startswith(variant))
                                   and (not k or e["k"] == k)]
                            if base == "R8_hetero":
                                f7 = [e for e in index.get("R7_full", [])
                                      if e["family"] == sub]
                                if f7:
                                    sha_col = (f"{f7[0]['sha256']} + Gbeta1 "
                                               f"731c013dfd2af08e + Ggamma2 "
                                               f"32ec703375c0e761")
                                    lstr = str(int(f7[0]["length"]) + 411)
                                    fam_dep = False
                            elif hit:
                                sha_col = hit[0]["sha256"]
                                lstr = hit[0]["length"]
                                fam_dep = False
                            else:
                                sha_col = f"UNRESOLVED:no {base} for {sub}"
                if a["family_rule"] == "DEPOSITED_TIP":
                    # the construct is receptor-specific: it is that receptor's own
                    # deposited tip, keyed in the registry by (construct, family=slug)
                    hit = [e for e in index.get(base, [])
                           if e["family"] == r["slug"]]
                    if not hit:
                        continue          # e.g. OPSD has no deposited ct21
                    sha_col = hit[0]["sha256"]
                    fam_col = f"deposited tip from {hit[0]['variant']}"
                    lstr = hit[0]["length"]
                    fam_dep = True
                # a cell that shares an arm's n with sibling draws gets n/share,
                # so five scramble permutations cost what one scramble arm costs
                nlo = a["n"][0] // share
                nhi = a["n"][1] // share
                rows.append(dict(
                    item=a["item"], experiment=a["exp"], arm=a["arm"],
                    receptor_set=a["rset"] + ("(provisional)" if a["rset"] in RSET
                                              else "(PENDING COUPLING.md)"),
                    enumeration="per_receptor" if r is not None
                    else "templated_pending_receptor_set",
                    receptor_slug=r["slug"] if r else "*",
                    receptor_uniprot=r["uniprot"] if r else "*",
                    receptor_organism=r["organism"] if r else "*",
                    receptor_cluster=r["cluster"] if r else "*",
                    # templated rows (r is None) have no receptor yet, so chain A
                    # is legitimately unresolved for them -- distinguished from a
                    # receptor that IS named and simply missing from seqrec_trim.tsv,
                    # which is a defect rather than a pending enumeration.
                    chain_a_source=(chain_a_src.get(
                        r["slug"], "UNRESOLVED:not in seqrec_trim.tsv") if r
                        else "PENDING:receptor set not enumerated"),
                    chain_a_sha256=(chain_a_sha.get(r["slug"], "UNRESOLVED") if r
                                    else "PENDING"),
                    chain_b_construct=rung,
                    n_shared_draws=share,
                    registry_matches=nmatch,
                    chain_b_family_rule=fam_col,
                    cognate_evidence_class=ev or "n/a",
                    supplied_partner_family=(frz[r["slug"]]["supplied_partner_family"]
                                             if r is not None else ""),
                    supplied_partner_subtype=(frz[r["slug"]]["supplied_partner_subtype"]
                                              if r is not None else ""),
                    reference_tip_subtype=(frz[r["slug"]]["reference_tip_subtype"]
                                           if r is not None else ""),
                    supplied_partner_independence=(
                        frz[r["slug"]]["supplied_partner_independence"]
                        if r is not None else ""),
                    cognate_vs_reference_agree=(
                        frz[r["slug"]]["cognate_vs_reference_agree"]
                        if r is not None else ""),
                    tier=frz[r["slug"]]["tier"] if r is not None else "",
                    chain_b_len=lstr,
                    chain_b_len_family_dependent="yes" if fam_dep else "no",
                    chain_b_sha256=sha_col,
                    chain_c="Gbeta1 P62873 + Ggamma2 P59768"
                    if base == "R8_hetero" else "-",
                    n_chains=1 if base == "R0_apo" else (3 if base == "R8_hetero" else 2),
                    partner_msa=("n/a" if base == "R0_apo" else a["msa_partner"]),
                    receptor_msa="on (default)",
                    ligand=a["ligand"], backbones=a["bb"],
                    n_pooled=nlo, n_percell=nhi,
                    predictions_pooled=nbb * nlo * (1 if r is not None else 0) or "PENDING",
                    predictions_percell=nbb * nhi * (1 if r is not None else 0) or "PENDING",
                    note=a["note"]))

    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # ---- reporting ------------------------------------------------------
    per_item = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        s = per_item[r["item"]]
        s[0] += 1
        if isinstance(r["predictions_pooled"], int):
            s[1] += r["predictions_pooled"]
            s[2] += r["predictions_percell"]
    sys.stderr.write(f"# wrote {len(rows)} systems -> {OUT}\n")
    sys.stderr.write(f"# provisional CORE-32 = {len(core32)}, C1_REST = {len(c1rest)}\n\n")
    sys.stderr.write(f"{'item':18s} {'systems':>8s} {'preds@n_pooled':>15s} "
                     f"{'preds@n_percell':>16s}\n")
    for k in sorted(per_item):
        n, p, q = per_item[k]
        sys.stderr.write(f"{k:18s} {n:8d} {p if p else '-':>15} {q if q else '-':>16}\n")
    tot = sum(v[1] for v in per_item.values()), sum(v[2] for v in per_item.values())
    sys.stderr.write(f"{'TOTAL(enumerated)':18s} {len(rows):8d} {tot[0]:>15,} {tot[1]:>16,}\n")
    unresolved = [r["chain_b_construct"] for r in rows if r["chain_b_len"] == "UNRESOLVED"]
    if unresolved:
        sys.stderr.write(f"\n# NOT YET IN THE REGISTRY (must be built before dispatch): "
                         f"{sorted(set(unresolved))}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
