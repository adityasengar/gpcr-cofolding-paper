"""Receptor-identity resolver.

Countermeasure for the receptor-substring bug documented in
docs/AUDIT_TRAIL.md (see audit_a1v3_register.py:53-58 in the frozen
`capabilities-expansion` branch, plus quick_score_tm6.py:59-60).

Two rules, in order:

1. Never substring-match. ``if r.upper() in p`` is banned by
   ci/lint_anti_patterns.sh under scorer/. Tokens are extracted from the
   path by a word-boundary regex.
2. Ambiguous ADA1A / ADA2A / AA1R / AA2AR / AA2BR / AA3R matches are
   resolved through EXPLICIT_DISAMBIG first, BEFORE any generic pattern.

When multiple distinct receptors are found in the same path, the resolver
RAISES A6ReceptorIdentity rather than guessing. Ambiguous inputs are a
data-quality signal — do not silence them.

Species disambiguation (human / mouse / turkey / rat / bovin) is A5's job,
not this module's — see scorer/references.py. This resolver returns the
receptor *family* slug (uppercase).
"""
from __future__ import annotations

import re
from pathlib import Path


class UnresolvedReceptorError(ValueError):
    """Raised when no known receptor is present in the path."""


class AmbiguousReceptorError(ValueError):
    """Raised when the path contains tokens for more than one distinct
    receptor family (audit-#6 disambig case). Never guess; raise."""


# ---------------------------------------------------------------------------
# EXPLICIT_DISAMBIG — matched BEFORE any other pattern.
#
# ADA*  = adrenergic α-adrenoceptors (α1A/1B/1D/2A/2B/2C)
# AA*   = adenosine A-receptors (A1R / A2AR / A2BR / A3R)
#
# These families are the historical false-match trap: "A2A" in a filename
# for ada2a_human matches inside the substring "AA2AR" under the frozen
# rule.
# ---------------------------------------------------------------------------
EXPLICIT_DISAMBIG: dict[str, str] = {
    # adenosine
    "AA1R":  "aa1r_human",
    "AA2AR": "aa2ar_human",
    "AA2BR": "aa2br_human",
    "AA3R":  "aa3r_human",
    # α-adrenergic
    "ADA1A": "ada1a_human",
    "ADA1B": "ada1b_human",
    "ADA1D": "ada1d_human",
    "ADA2A": "ada2a_human",
    "ADA2B": "ada2b_human",
    "ADA2C": "ada2c_human",
    # 2026-08-26 recovery patch (consultant): XCR1 substring-collides
    # with CXCR1. Force word-boundary match here BEFORE any CXCR1
    # substring hit. See docs/AUDIT_TRAIL.md#recovery-2026-08-26.
    "XCR1":  "xcr1_human",
    # 2026-08-26 recovery patch (consultant): alias mappings for arms
    # where the frozen filename uses a non-canonical name for the
    # canonical GPCRdb entry.
    "MGLUR2": "grm2_human",   # path uses MGLUR2, GPCRdb canonical GRM2
    "MGLUR3": "grm3_human",
    "MGLUR4": "grm4_human",
    "MGLUR5": "grm5_human",
    "GABBR2": "gabr2_human",  # path uses double-B, canonical single-B
    "OPRL":   "oprx_human",   # opioid receptor-like 1
    "CALCRL": "calrl_human",  # calcitonin receptor-like
    # 2026-09-02 Block A closeout: three Class B/F aliases surfaced from
    # 018_block_a_switch_test panel (crhr1/gcgr/fzd6 cells returned NaN
    # rows because their HUGO/UniProt symbols do not match GPCRdb entry
    # names). All three verified in refs/reference_set.csv against real
    # PDB active/inactive pairs. See plan §3 in silly-leaping-aho.md.
    "CRHR1":  "crfr1_human",  # HUGO CRHR1 = GPCRdb crfr1 (CRF-R1)
    "GCGR":   "glr_human",    # HUGO GCGR = GPCRdb glr (glucagon receptor)
}

# ---------------------------------------------------------------------------
# KNOWN_RECEPTORS — the panel from the frozen reference_panel_v2.csv, plus
# EXPLICIT_DISAMBIG (folded in below). Every entry maps its uppercase family
# slug to the canonical GPCRdb entry_name (lowercase, species suffix).
#
# For species-multi entries (adrb1_human vs adrb1_melga; oprm_mouse vs
# oprm_human; ntr1_human vs ntr1_rat; smo_human vs smo_mouse) the family
# slug points at the human canonical when one exists; A5 handles species
# gating at reference-selection time (scorer/references.py).
# ---------------------------------------------------------------------------
KNOWN_RECEPTORS: dict[str, str] = {
    # β-adrenergic
    "ADRB1": "adrb1_human",
    "ADRB2": "adrb2_human",
    "ADRB3": "adrb3_human",
    # muscarinic
    "ACM1": "acm1_human", "ACM2": "acm2_human", "ACM3": "acm3_human",
    "ACM4": "acm4_human", "ACM5": "acm5_human",
    # serotonergic
    "5HT1A": "5ht1a_human", "5HT1B": "5ht1b_human", "5HT2A": "5ht2a_human",
    "5HT2B": "5ht2b_human", "5HT2C": "5ht2c_human", "5HT5A": "5ht5a_human",
    "5HT6R": "5ht6r_human", "5HT7R": "5ht7r_human",
    # dopamine
    "DRD1": "drd1_human", "DRD2": "drd2_human", "DRD3": "drd3_human",
    "DRD4": "drd4_human", "DRD5": "drd5_human",
    # opioid
    "OPRD": "oprd_human", "OPRK": "oprk_human",
    "OPRM": "oprm_human",  # note: 5C1M is mouse — see docs/REFERENCE_SET.md
    "OPRX": "oprx_human",
    "OPSD": "opsd_bovin",
    # histamine
    "HRH1": "hrh1_human", "HRH2": "hrh2_human",
    "HRH3": "hrh3_human", "HRH4": "hrh4_human",
    # tachykinin
    "NK1R": "nk1r_human", "NK2R": "nk2r_human", "NK3R": "nk3r_human",
    # peptide
    "GHSR": "ghsr_human",
    "MC1R": "mc1r_human", "MC4R": "mc4r_human",
    "CNR1": "cnr1_human", "CNR2": "cnr2_human",
    "GLP1R": "glp1r_human", "GLR": "glr_human",
    "CALRL": "calrl_human", "CALCR": "calcr_human",
    "GIPR": "gipr_human",
    "PTH1R": "pth1r_human", "PTH2R": "pth2r_human",
    # chemokine
    "CXCR1": "cxcr1_human", "CXCR2": "cxcr2_human", "CXCR3": "cxcr3_human",
    "CXCR4": "cxcr4_human", "CXCR5": "cxcr5_human", "CXCR6": "cxcr6_human",
    "CCR2": "ccr2_human", "CCR5": "ccr5_human",
    "CCR6": "ccr6_human", "CCR8": "ccr8_human",
    # melatonin, sst, edn, etc.
    "MTR1A": "mtr1a_human", "MTR1B": "mtr1b_human",
    "EDNRA": "ednra_human", "EDNRB": "ednrb_human",
    "SSR2": "ssr2_human",
    "TRHR": "trhr_human",
    "V1AR": "v1ar_human", "V1BR": "v1br_human", "V2R": "v2r_human",
    "FSHR": "fshr_human", "LSHR": "lshr_human", "TSHR": "tshr_human",
    "AGTR1": "agtr1_human",
    "APJ": "apj_human",
    "C5AR1": "c5ar1_human",
    "CASR": "casr_human",
    "CCKAR": "cckar_human",
    "CRFR1": "crfr1_human",
    "GRM2": "grm2_human", "GRM3": "grm3_human",
    "GRM4": "grm4_human", "GRM5": "grm5_human",
    "GRPR": "grpr_human",
    "LPAR1": "lpar1_human",
    "LT4R1": "lt4r1_human",
    "MCHR1": "mchr1_human",
    "NPY1R": "npy1r_human", "NPY2R": "npy2r_human",
    "NTR1": "ntr1_human",  # also ntr1_rat
    "OX2R": "ox2r_human",
    "OXYR": "oxyr_human",
    "PD2R2": "pd2r2_human",
    "PE2R4": "pe2r4_human",
    "S1PR1": "s1pr1_human", "S1PR5": "s1pr5_human",
    "SMO": "smo_human",
    "TA2R": "ta2r_human",
    # calmodulin (non-canonical / positive control) — handled by
    # scorer/noncanonical.py; still registered here so the resolver can
    # route on filename.
    "CALM": "calm_human",
    "CAM":  "calm_human",   # alias for shorthand names in the frozen tree

    # Class B (secretin family) — added on the M1 rerun after 11 were
    # silently skipped by the (now-removed) skip-not-raise path. See
    # docs/AUDIT_TRAIL.md for the reasoning: absence-because-of-us is a
    # scoring failure, not a "not applicable".
    "AGRE5": "agre5_human",       # adhesion GPCR
    "AGRL3": "agrl3_human",       # adhesion GPCR
    "FZD4":  "fzd4_human",        # Frizzled
    "FZD6":  "fzd6_human",        # Frizzled — added 2026-09-02 Block A closeout
    "FZD7":  "fzd7_human",        # Frizzled
    "GABR2": "gabr2_human",       # GABA-B2
    "GP156": "gp156_human",       # GPR156, orphan
    "GPR52": "gpr52_human",       # orphan — has landed predictions on steering branch
    "GPR6":  "gpr6_human",        # orphan
    "O52E4": "o52e4_human",       # olfactory
    "T2R14": "t2r14_human",       # bitter taste
    # B1B1U5 is a spider-mite receptor (species '9arac'); flagged as
    # non-human — resolver returns the slug but A5 will refuse a human
    # construct vs this reference.
    "B1B1U5": "b1b1u5_9arac",

    # 2026-08-26 recovery patch (consultant): additional GPCRs surfaced
    # by A6-fail rows in M2.2 v3. All 6 BW anchors verified in GPCRdb
    # `services/residues/extended/`; all collision-checked against
    # existing entries. See docs/AUDIT_TRAIL.md#recovery-2026-08-26 and
    # refs/known_receptors_patch.py for full provenance.
    #
    # Trace amines / rare aminergic
    "TAAR1": "taar1_human",
    "TAA7F": "taa7f_mouse",   # note: mouse — A5 gates species
    # Melanocortin
    "MC3R":  "mc3r_human",
    "MC5R":  "mc5r_human",
    # Bombesin
    "BRS3":  "brs3_human",
    "NMBR":  "nmbr_human",
    # Chemokines / immune (chemerin-like)
    "CML2":  "cml2_human",
    # Free fatty acid + hydroxycarboxylic acid
    "FFAR2": "ffar2_human",
    "HCAR3": "hcar3_human",
    "SUCR1": "sucr1_human",
    # Orphan / adhesion / non-canonical
    "GP101": "gp101_human",
    "GP132": "gp132_human",
    "GPER1": "gper1_human",
    "GPR3":  "gpr3_human",
    "GPR12": "gpr12_human",
    "GPR15": "gpr15_human",
    "GPR34": "gpr34_human",
    "GPR55": "gpr55_human",
    "GPR84": "gpr84_human",
    "KISSR": "kissr_human",
    "MCHR2": "mchr2_human",
    "OPSR":  "opsr_human",
    "P2Y10": "p2y10_human",
    # Prostanoid / lipid signalling
    "PF2R":  "pf2r_human",
    "PI2R":  "pi2r_human",
    "PE2R1": "pe2r1_human",   # 15 rows
    # Somatostatin
    "SSR1":  "ssr1_human",
    "SSR3":  "ssr3_human",
    "SSR5":  "ssr5_human",
    # Other
    "PRLHR": "prlhr_human",
    "QRFPR": "qrfpr_human",
}

# Fold EXPLICIT_DISAMBIG entries into KNOWN_RECEPTORS so a single lookup
# suffices *after* the disambig step below.
for _k, _v in EXPLICIT_DISAMBIG.items():
    KNOWN_RECEPTORS.setdefault(_k, _v)


# Word-boundary token extraction. Tokens are 3..8 alnum chars, delimited
# by any of _ - . / or path boundary. Case-insensitive.
_TOKEN_RE = re.compile(r"(?:^|[_\-./\\])([A-Za-z0-9]{3,8})(?=[_\-./\\]|$)")


def _tokens(path_or_name: str) -> list[str]:
    """All candidate receptor tokens in a path/filename. Uppercased."""
    stem = Path(path_or_name).name  # last component; still contains ext
    all_matches: list[str] = []
    for text in (str(path_or_name), stem):
        all_matches.extend(_TOKEN_RE.findall(text))
    # dedupe preserving order, uppercased
    seen = set()
    out: list[str] = []
    for t in all_matches:
        up = t.upper()
        if up not in seen:
            seen.add(up)
            out.append(up)
    return out


def resolve_receptor(
    path_or_name: str,
    hint: str | None = None,
) -> tuple[str, str]:
    """Return (receptor_slug_upper, source).

    Resolution order:
      1. ``hint`` provided by caller (CLI --receptor). Verified against
         KNOWN_RECEPTORS; if unknown → UnresolvedReceptorError.
      2. Explicit-disambig match on any token in the path (uppercased,
         word-bounded).
      3. KNOWN_RECEPTORS match on any remaining token.

    A single distinct hit is returned. Multiple distinct hits → raise
    AmbiguousReceptorError. Zero hits → UnresolvedReceptorError.

    ``source`` values:
      - ``"hint"``                 — user supplied
      - ``"explicit_table"``       — matched via EXPLICIT_DISAMBIG
      - ``"word_boundary_regex"``  — matched via KNOWN_RECEPTORS
    """
    if hint:
        up = hint.upper()
        if up not in KNOWN_RECEPTORS:
            raise UnresolvedReceptorError(
                f"hint {hint!r} is not a known receptor slug "
                f"(add to scorer/receptors.py::KNOWN_RECEPTORS to allow)"
            )
        return up, "hint"

    tokens = _tokens(path_or_name)
    if not tokens:
        raise UnresolvedReceptorError(
            f"no candidate tokens extracted from {path_or_name!r}"
        )

    # Step 2: explicit-disambig hits
    disambig_hits: list[str] = [t for t in tokens if t in EXPLICIT_DISAMBIG]
    # Step 3: any other known-receptor hits (excluding disambig set)
    other_hits: list[str] = [
        t for t in tokens
        if t in KNOWN_RECEPTORS and t not in EXPLICIT_DISAMBIG
    ]

    # If the disambig table matched, use ONLY those (do not mix in generic
    # KNOWN_RECEPTORS hits that might overlap by prefix).
    hits = disambig_hits if disambig_hits else other_hits
    source = "explicit_table" if disambig_hits else "word_boundary_regex"

    distinct = list(dict.fromkeys(hits))  # preserve order

    if len(distinct) == 0:
        raise UnresolvedReceptorError(
            f"path {path_or_name!r} contained tokens {tokens!r} but none "
            f"matched a known receptor"
        )
    if len(distinct) > 1:
        raise AmbiguousReceptorError(
            f"path {path_or_name!r} contained multiple receptors: "
            f"{distinct!r} — supply --receptor to disambiguate"
        )
    return distinct[0], source


def uniprot_slug(receptor_upper: str) -> str:
    """Canonical GPCRdb entry_name for a receptor family slug."""
    if receptor_upper not in KNOWN_RECEPTORS:
        raise UnresolvedReceptorError(
            f"unknown receptor {receptor_upper!r} — extend scorer/receptors.py"
        )
    return KNOWN_RECEPTORS[receptor_upper]


# ---------------------------------------------------------------------------
# RECEPTOR_CLASS — GPCR class (A/B/C/F/T2R) per receptor family slug.
#
# Added in the class-aware rescore work (v3.7). Purely annotative — the
# scorer does NOT branch on this. Its purpose is to make the CSV row
# self-describing so downstream analysis can interpret axis NaN correctly
# (a Class-B receptor NaN on `d_dry_sidechain_r350cz_e630oe1` means
# "physics doesn't apply here", not "measurement failed"), and to enable
# the per-axis `AXIS_APPLICABILITY` table in scorer/axes.py.
#
# Class definitions:
#   A    — rhodopsin-like (majority): DRY motif at 3.50/3.51, NPxxY at
#          7.53, TM6 outward on activation (~5-8 Å swing).
#   B    — secretin family: HETX polar network (H2.50/E3.49), much larger
#          TM6 kink on activation (~10-15 Å), no DRY, no NPxxY Tyr.
#   C    — glutamate/GABA-B/CaSR family: obligate dimers, VFT (Venus
#          flytrap) ECD, unique FYNP motif, no DRY.
#   F    — Frizzled / Smoothened: unique molecular switch at 6.48, no DRY.
#   T2R  — bitter taste (Class T): distinct from A/B/C/F under some
#          nomenclatures; single receptor T2R14 in v3.6b.
#
# Assignments verified against GPCRdb protein family classification.
# When adding a receptor to KNOWN_RECEPTORS, add a class here too — the
# `receptor_class()` helper raises on missing entries so the omission
# surfaces immediately rather than silently defaulting to "A".
# ---------------------------------------------------------------------------

RECEPTOR_CLASS: dict[str, str] = {
    # --- Class A (rhodopsin-like) -----------------------------------------
    # β-adrenergic
    "ADRB1": "A", "ADRB2": "A", "ADRB3": "A",
    # α-adrenergic
    "ADA1A": "A", "ADA1B": "A", "ADA1D": "A",
    "ADA2A": "A", "ADA2B": "A", "ADA2C": "A",
    # muscarinic
    "ACM1": "A", "ACM2": "A", "ACM3": "A", "ACM4": "A", "ACM5": "A",
    # serotonergic
    "5HT1A": "A", "5HT1B": "A", "5HT2A": "A", "5HT2B": "A", "5HT2C": "A",
    "5HT5A": "A", "5HT6R": "A", "5HT7R": "A",
    # dopamine
    "DRD1": "A", "DRD2": "A", "DRD3": "A", "DRD4": "A", "DRD5": "A",
    # opioid
    "OPRD": "A", "OPRK": "A", "OPRM": "A", "OPRX": "A",
    # rhodopsin / opsin
    "OPSD": "A", "OPSR": "A",
    # histamine
    "HRH1": "A", "HRH2": "A", "HRH3": "A", "HRH4": "A",
    # tachykinin
    "NK1R": "A", "NK2R": "A", "NK3R": "A",
    # peptide
    "GHSR": "A",
    "MC1R": "A", "MC3R": "A", "MC4R": "A", "MC5R": "A",
    "CNR1": "A", "CNR2": "A",
    # chemokine
    "CXCR1": "A", "CXCR2": "A", "CXCR3": "A",
    "CXCR4": "A", "CXCR5": "A", "CXCR6": "A",
    "CCR2": "A", "CCR5": "A", "CCR6": "A", "CCR8": "A",
    "XCR1": "A",
    # melatonin, somatostatin, endothelin, others
    "MTR1A": "A", "MTR1B": "A",
    "EDNRA": "A", "EDNRB": "A",
    "SSR1": "A", "SSR2": "A", "SSR3": "A", "SSR5": "A",
    "TRHR": "A",
    "V1AR": "A", "V1BR": "A", "V2R": "A",
    "FSHR": "A", "LSHR": "A", "TSHR": "A",
    "AGTR1": "A",
    "APJ": "A",
    "C5AR1": "A",
    "CCKAR": "A",
    "GRPR": "A",
    "LPAR1": "A",
    "LT4R1": "A",
    "MCHR1": "A", "MCHR2": "A",
    "NPY1R": "A", "NPY2R": "A",
    "NTR1": "A",
    "OX2R": "A",
    "OXYR": "A",
    "PD2R2": "A",
    "PE2R4": "A",
    "PE2R1": "A",
    "S1PR1": "A", "S1PR5": "A",
    "TA2R": "A",
    "KISSR": "A",
    "PRLHR": "A",
    "QRFPR": "A",
    # adenosine
    "AA1R": "A", "AA2AR": "A", "AA2BR": "A", "AA3R": "A",
    # trace amines
    "TAAR1": "A", "TAA7F": "A",
    # bombesin
    "BRS3": "A", "NMBR": "A",
    # chemerin
    "CML2": "A",
    # prostanoid
    "PF2R": "A", "PI2R": "A",
    # free fatty acid / hydroxycarboxylic / succinate
    "FFAR2": "A", "HCAR3": "A", "SUCR1": "A",
    # orphan Class A / rhodopsin-like
    "GPR3": "A", "GPR6": "A", "GPR12": "A", "GPR15": "A",
    "GPR34": "A", "GPR52": "A", "GPR55": "A", "GPR84": "A",
    "GPER1": "A",
    "GP101": "A", "GP132": "A",
    "P2Y10": "A",
    # olfactory (Class A)
    "O52E4": "A",
    # non-human Class A
    "B1B1U5": "A",   # spider mite receptor — orphan, ectodomain-truncated Class A
    # --- Class B (secretin family) ----------------------------------------
    # Class B1 — secretin family
    "CALCR": "B", "CALRL": "B",
    "CRFR1": "B",
    "GLP1R": "B", "GLR": "B",
    "GIPR": "B",
    "PTH1R": "B", "PTH2R": "B",
    # Class B2 — adhesion GPCRs
    "AGRE5": "B", "AGRL3": "B",
    # --- Class C (glutamate / GABA-B / CaSR / GP156) ----------------------
    "GRM2": "C", "GRM3": "C", "GRM4": "C", "GRM5": "C",
    "GABR2": "C",
    "CASR": "C",
    "GP156": "C",     # GPR156 — Class C orphan
    # --- Class F (Frizzled / Smoothened) ----------------------------------
    "FZD4": "F", "FZD6": "F", "FZD7": "F",
    "SMO": "F",
    # --- T2R (bitter taste) -----------------------------------------------
    "T2R14": "T2R",
    # --- Non-canonical / positive control (not a GPCR at all) -------------
    # calmodulin is a positive-control target that flows through the same
    # scoring pipeline via scorer/noncanonical.py; annotate as "N" for
    # non-canonical so downstream analyses can filter it out cleanly.
    "CALM": "N", "CAM": "N",
    # --- Alias entries from EXPLICIT_DISAMBIG ------------------------------
    # These map to canonical GPCRdb entries above; annotate the alias key
    # explicitly so callers using either form get the same class.
    "OPRL":   "A",   # opioid receptor-like 1 → oprx_human
    "CALCRL": "B",   # calcitonin receptor-like alias → calrl_human
    "GABBR2": "C",   # GABA-B2 alias → gabr2_human
    "MGLUR2": "C", "MGLUR3": "C", "MGLUR4": "C", "MGLUR5": "C",
    # 2026-09-02 Block A closeout aliases (see EXPLICIT_DISAMBIG above)
    "CRHR1":  "B",   # HUGO CRHR1 → crfr1_human (Class B secretin)
    "GCGR":   "B",   # HUGO GCGR  → glr_human   (Class B secretin)
}


def receptor_class(receptor_upper: str) -> str:
    """Return the GPCR class ('A', 'B', 'C', 'F', 'T2R', 'N') for a receptor
    family slug. Raises UnresolvedReceptorError if the slug is not in
    RECEPTOR_CLASS — silently defaulting to 'A' would let a class-aware
    downstream analysis misinterpret an unclassified receptor. Adding a
    receptor to KNOWN_RECEPTORS without a class entry surfaces here.
    """
    up = receptor_upper.upper()
    if up not in RECEPTOR_CLASS:
        raise UnresolvedReceptorError(
            f"receptor {up!r} has no class assignment in RECEPTOR_CLASS "
            f"(scorer/receptors.py) — add it before it can be scored"
        )
    return RECEPTOR_CLASS[up]
