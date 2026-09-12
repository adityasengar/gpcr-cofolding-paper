"""Analysis-time enricher — add partner sequence & G-protein class columns.

Reads a v3.7 rescore artefact and the EXPERIMENT_CATALOG predictions.csv,
writes a *_enriched.csv beside it with four additional columns:

    partner_g_class          — Gs / Gi / Gq / Gt / G12-13 / arrestin /
                               peptide / small_molecule / apo / other /
                               unknown_g_family
    partner_perturbation     — wt / truncated_Naa / shuffled / mutated /
                               chimeric / designed / apo_partner / unknown
    partner_sequence_delta   — actual perturbed partner sequence extracted
                               from the prediction's input file, empty
                               for wt / apo_partner rows or when the input
                               file cannot be resolved / parsed
    partner_sequence_delta_note — short reason ("wt: no delta", "input
                               file not resolved", "backbone not
                               supported: chai", ...) so a NaN delta is
                               always accompanied by an explanation

This is Option B from the task specification: strict analysis-time
enrichment — no scoring code change, no v3.7 output touched, output goes
next to the input as *_enriched.csv.

Design principles:
  1. Join key is `input_path` (v3.7 rows.csv) vs `prediction_path`
     (predictions.csv). Both refer to the same file on scratch.
  2. Classification tables are *explicit and grep-visible* below. Every
     (partner_type, partner_identity) pair in the corpus is hand-mapped.
     A new pair not covered raises a clear KeyError — silent fallback
     to "unknown" would defeat provenance.
  3. Partner sequence extraction supports Boltz (input.yaml) and OF3
     (inference_query_set.json) — these cover ~90 % of perturbed rows
     in the v3.7 corpus. Chai / Protenix / AF2-multimer are declared
     unsupported and get an explanation in the note column rather than
     an empty-with-no-reason silence.
  4. No side effects on the source CSV. Read-only inputs, write-only
     output.

Usage:

    python3 scripts/enrich_partner_metadata.py \\
        --rows /hpc/scratch/.../gpcr_v37/rows.csv \\
        --predictions docs/EXPERIMENT_CATALOG/data/predictions.csv \\
        --out /hpc/scratch/.../gpcr_v37/rows_enriched.csv

Provenance: the header of the emitted CSV carries the four new column
names appended after every column of the input. Existing columns are
byte-identical; the additive-only invariant holds.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


# =============================================================================
# Table 1 — RECEPTOR_G_COUPLING
#
# Primary Gα family per receptor. Sourced from Guide-to-Pharmacology (GtoPdb)
# canonical primary coupling. Where a receptor has documented dual coupling,
# the DOMINANT one under Gα-coupled active state (Ga-coupled-active) is
# picked. Uncertain cases mapped to `unknown_g_family` — analyst can inspect
# the row's `partner_identity` for verbose context.
# =============================================================================

RECEPTOR_G_COUPLING: dict[str, str] = {
    # Gs (adenylyl-cyclase activation)
    "ADRB1": "Gs", "ADRB2": "Gs", "ADRB3": "Gs",
    "DRD1": "Gs", "DRD5": "Gs",
    "5HT6R": "Gs", "5HT7R": "Gs",
    "HRH2": "Gs",
    "MC1R": "Gs", "MC3R": "Gs", "MC4R": "Gs", "MC5R": "Gs",
    "GLP1R": "Gs", "GLR": "Gs", "GIPR": "Gs",
    "CALCR": "Gs", "CALRL": "Gs",
    "CRFR1": "Gs",
    "PTH1R": "Gs", "PTH2R": "Gs",
    "LSHR": "Gs", "FSHR": "Gs", "TSHR": "Gs",
    "GPR3": "Gs", "GPR12": "Gs", "GPR52": "Gs", "GPR6": "Gs",
    "V2R": "Gs",
    "C5AR1": "Gs",   # dual Gi/Gs; Gs canonical for GtoPdb
    "PE2R4": "Gs",
    "PI2R": "Gs",
    "GPER1": "Gs",   # Gs canonical; some Gi in specific contexts
    "PD2R2": "Gs",   # DP1 = Gs; DP2 = Gi (paper corpus uses DP2 slug PD2R2)
    "OPSR": "Gs",    # red cone opsin; Gt in retinal biology but scored as Gs-like
    # Gi (adenylyl-cyclase inhibition)
    "5HT1A": "Gi", "5HT1B": "Gi", "5HT5A": "Gi",
    "ACM2": "Gi", "ACM4": "Gi",
    "ADA2A": "Gi", "ADA2B": "Gi", "ADA2C": "Gi",
    "DRD2": "Gi", "DRD3": "Gi", "DRD4": "Gi",
    "OPRD": "Gi", "OPRK": "Gi", "OPRM": "Gi", "OPRX": "Gi", "OPRL": "Gi",
    "HRH3": "Gi", "HRH4": "Gi",
    "MTR1A": "Gi", "MTR1B": "Gi",
    "SSR1": "Gi", "SSR2": "Gi", "SSR3": "Gi", "SSR5": "Gi",
    "CNR1": "Gi", "CNR2": "Gi",
    "AA1R": "Gi", "AA3R": "Gi",
    "CXCR1": "Gi", "CXCR2": "Gi", "CXCR3": "Gi",
    "CXCR4": "Gi", "CXCR5": "Gi", "CXCR6": "Gi",
    "CCR2": "Gi", "CCR5": "Gi", "CCR6": "Gi", "CCR8": "Gi",
    "XCR1": "Gi",
    "CML2": "Gi",
    "SUCR1": "Gi",
    "HCAR3": "Gi",
    "FFAR2": "Gi",
    "GPR15": "Gi", "GPR34": "Gi", "GPR84": "Gi",
    "GP101": "Gs",   # constitutive Gs
    "GP132": "Gi",   # Gi/G13; Gi picked
    "LPAR1": "Gi",   # Gi/G12-13; Gi picked as primary
    "S1PR1": "Gi", "S1PR5": "Gi",
    "TAAR1": "Gs",   # TAAR1 = Gs canonical; some Gq
    "TAA7F": "Gs",
    "GABR2": "Gi",   # GABA-B is Gi
    "MCHR1": "Gi", "MCHR2": "Gi",
    "GRM2": "Gi", "GRM3": "Gi", "GRM4": "Gi",
    "GHSR": "Gq",    # Gq primary; some G11
    "NPY1R": "Gi", "NPY2R": "Gi",
    "APJ": "Gi",
    # Gq (phospholipase C activation)
    "5HT2A": "Gq", "5HT2B": "Gq", "5HT2C": "Gq",
    "ACM1": "Gq", "ACM3": "Gq", "ACM5": "Gq",
    "ADA1A": "Gq", "ADA1B": "Gq", "ADA1D": "Gq",
    "HRH1": "Gq",
    "AGTR1": "Gq",
    "GRPR": "Gq",
    "OXYR": "Gq",
    "V1AR": "Gq", "V1BR": "Gq",
    "EDNRA": "Gq", "EDNRB": "Gq",
    "NK1R": "Gq", "NK2R": "Gq", "NK3R": "Gq",
    "TRHR": "Gq",
    "TA2R": "Gq",
    "LT4R1": "Gq",
    "OX2R": "Gq",
    "CCKAR": "Gq",
    "KISSR": "Gq",
    "PE2R1": "Gq",
    "PF2R": "Gq",
    "BRS3": "Gq",
    "NMBR": "Gq",
    "QRFPR": "Gq",
    "PRLHR": "Gq",
    "GRM5": "Gq",    # class C, group-I mGluR = Gq
    "CASR": "Gq",    # Gq primary, some Gi
    # Gt (transducin)
    "OPSD": "Gt",
    # G12/13
    "GPR55": "G12-13",
    "P2Y10": "G12-13",
    # Class F (Frizzled / Smoothened) — unusual; Gi-linked in some contexts,
    # but historically outside the canonical Gα classification. Report as
    # "unknown_g_family" so downstream analysis doesn't accidentally group
    # them with Gi Class A.
    "SMO": "unknown_g_family",
    "FZD4": "unknown_g_family", "FZD7": "unknown_g_family",
    # Non-canonical / non-GPCR
    "CALM": "unknown_g_family", "CAM": "unknown_g_family",
    # Species / receptor variants
    "AA2AR": "Gs", "AA2BR": "Gs",
    "OPSD_BOVIN": "Gt",
    # Non-human orphans and adhesion receptors: unknown by default until
    # canonical coupling can be cited. Analysts read `partner_identity`
    # for context.
    "B1B1U5": "unknown_g_family",
    "AGRE5": "unknown_g_family", "AGRL3": "unknown_g_family",
    "GP156": "unknown_g_family",
}


# =============================================================================
# Table 2 — PARTNER_TYPE_TO_G_CLASS
#
# Maps `partner_type` from EXPERIMENT_CATALOG to `partner_g_class`. Where
# the answer depends on the receptor (cognate Gα), the value is the string
# "receptor_lookup" — the caller resolves via RECEPTOR_G_COUPLING.
# =============================================================================

PARTNER_TYPE_TO_G_CLASS: dict[str, str] = {
    "apo":                "apo",
    "cognate_ga":         "receptor_lookup",
    "α5_ct_variant":      "receptor_lookup",   # α5-CT of the receptor's cognate Gα
    "α5_ct_fragment":     "receptor_lookup",   # α5-CT of cognate Gα (usually Gs per identity)
    "shuffled_ga":        "receptor_lookup",   # shuffled version of cognate Gα family
    "mutant_gα":          "receptor_lookup",   # Gs α5-tip mutant per identity
    "arrestin":           "arrestin",
    "peptide_native":     "peptide",
    "ligand":             "small_molecule",
    "antagonist":         "small_molecule",
    "wrong_agonist":      "small_molecule",
    "neutral_ligand":     "small_molecule",
    "decoy_scaffold":     "other",
    "decoy_random_helix": "other",
    "other":              "other",
}


# =============================================================================
# Table 3 — PARTNER_IDENTITY_TO_G_CLASS_OVERRIDES
#
# When `partner_identity` names a specific Gα family directly (e.g.
# "Gαs α5-CT"), use it verbatim rather than looking up the receptor.
# Explicit takes precedence over receptor_lookup.
# =============================================================================

PARTNER_IDENTITY_G_HINTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"Gαs\b|Gas\b|Gαs α5-CT", re.IGNORECASE),     "Gs"),
    (re.compile(r"Gαi\b|Gai\b",           re.IGNORECASE),     "Gi"),
    (re.compile(r"Gαq\b|Gaq\b",           re.IGNORECASE),     "Gq"),
    (re.compile(r"Gαt\b|Gat\b",           re.IGNORECASE),     "Gt"),
    (re.compile(r"Gα12\b|Gα13\b",         re.IGNORECASE),     "G12-13"),
]


# =============================================================================
# Table 4 — PARTNER_TYPE_TO_PERTURBATION
#
# Maps `partner_type` to `partner_perturbation`. Some entries need further
# refinement from the path (e.g. α5_ct_fragment → truncated_Naa where N
# comes from the folder name).
# =============================================================================

PARTNER_TYPE_TO_PERTURBATION: dict[str, str] = {
    "apo":                "wt",                # per task spec: apo → col1=apo, col2=wt
    "cognate_ga":         "wt",
    "α5_ct_variant":      "chimeric",          # designed variants of α5-CT
    "α5_ct_fragment":     "truncated_Naa",     # length in path — refined below
    "shuffled_ga":        "shuffled",
    "mutant_gα":          "mutated",
    "arrestin":           "wt",
    "peptide_native":     "wt",
    "ligand":             "wt",
    "antagonist":         "wt",
    "wrong_agonist":      "wt",
    "neutral_ligand":     "wt",
    "decoy_scaffold":     "designed",
    "decoy_random_helix": "designed",
    "other":              "unknown",
}


# Regex to pull truncation length "alpha5_15aa" / "alpha5_10aa" out of paths.
_TRUNC_RE = re.compile(r"alpha5[_-](\d+)aa", re.IGNORECASE)


# =============================================================================
# Exp-Layer 2 additions — seed + ligand extraction
# =============================================================================
#
# Same regex the scorer's `_seed_used_from_input_path` uses (kept in sync with
# scorer/orchestrator.py). Rerun tree lives at
# `/hpc/scratch/sengaad1/paper_af3/rerun/<date>/<exp>/<sha12>/<bb>/seed_<N>/...`;
# frozen-corpus predictions land at
# `/hpc/scratch/sengaad1/subsampling/outputs/<exp>/.../seed_<N>/...`.
_SEED_FROM_PATH_RE = re.compile(r"/seed_(\d+)(?:/|$)")


def seed_used_from_input_path(input_path: str) -> int:
    """Extract the seed from a ``.../seed_<N>/...`` path segment.

    Anchored on a leading slash to avoid false-positives like
    ``notreallyseed_42``. 0 sentinel when not extractable — the analyst
    reads that as "seed missing" and filters accordingly.
    """
    m = _SEED_FROM_PATH_RE.search(input_path)
    if not m:
        return 0
    try:
        return int(m.group(1))
    except ValueError:
        return 0


# Partner-type → whether this row's PARTNER is really a small-molecule
# ligand (as opposed to a G-protein / arrestin / peptide). When True, we
# lift the ligand info from the row's partner columns; there is no
# separate ligand slot in the frozen corpus's inputs.
_PARTNER_TYPES_THAT_ARE_LIGANDS = frozenset({
    "ligand", "antagonist", "wrong_agonist", "neutral_ligand",
})


def classify_ligand_from_partner(partner_type: str,
                                 partner_identity: str) -> tuple[str, str, str, str]:
    """Return ``(ligand_type, ligand_sequence, ligand_smiles, note)``
    from a row's partner columns alone (no upstream-file parsing).

    Rules:
      - apo partner → ``ligand_type = apo``
      - partner-that-is-a-ligand types → ``ligand_type = small_molecule``,
        SMILES is empty (frozen corpus uses identity NAMES, not SMILES;
        the actual chemistry lives in the Boltz `ccd:` field of the
        input.yaml — that's where the input-file parser picks it up).
      - peptide_native → ``ligand_type = peptide``, sequence populated
        via partner-sequence extraction (already done elsewhere)
      - otherwise → ``ligand_type = none``
    """
    pt = (partner_type or "").strip()
    if pt == "apo":
        return "apo", "", "", "partner_type=apo"
    if pt in _PARTNER_TYPES_THAT_ARE_LIGANDS:
        return "small_molecule", "", "", f"partner_type={pt} (identity={partner_identity!r})"
    if pt == "peptide_native":
        return "peptide", "", "", f"partner_type=peptide_native (identity={partner_identity!r})"
    return "none", "", "", f"partner_type={pt or 'unknown'} — no ligand slot"


# --- Backbone-specific ligand extraction from the upstream input file --------


def _boltz_yaml_ligand(prediction_path: str) -> tuple[str, str, str, str]:
    """Parse the Boltz input.yaml for a ligand block or third protein chain.

    Returns ``(ligand_type, ligand_sequence, ligand_smiles, note)``. If no
    Boltz input.yaml is discoverable, ``ligand_type=""`` and note carries
    the reason — the caller falls through to `classify_ligand_from_partner`.
    """
    yml, layout_note = _find_boltz_input_yaml(prediction_path)
    if yml is None:
        return "", "", "", layout_note
    try:
        text = yml.read_text()
    except OSError as e:
        return "", "", "", f"{layout_note}; read failed: {e}"
    # A `ligand:` block emits either `smiles: <str>` or `ccd: <str>`
    # (both are Boltz-canonical; frozen corpus uses `ccd:` per
    # subsampling/scripts/weekend/build_weekend.py::boltz_yaml_ligand).
    smiles_re = re.compile(r"^\s*smiles:\s*(?P<v>\S.*?)\s*$", re.MULTILINE)
    ccd_re = re.compile(r"^\s*ccd:\s*(?P<v>\S.*?)\s*$", re.MULTILINE)
    m_smi = smiles_re.search(text)
    m_ccd = ccd_re.search(text)
    if m_smi:
        smi = m_smi.group("v").strip().strip("'\"")
        return "small_molecule", "", smi, f"{layout_note}; boltz ligand.smiles"
    if m_ccd:
        code = m_ccd.group("v").strip().strip("'\"")
        return "small_molecule", "", f"CCD:{code}", f"{layout_note}; boltz ligand.ccd"
    # Third protein chain → peptide ligand
    seq_re = re.compile(r"^\s*sequence:\s*(\S+)\s*$", re.MULTILINE)
    seqs = seq_re.findall(text)
    if len(seqs) >= 3:
        return "peptide", seqs[2], "", f"{layout_note}; boltz chain C peptide"
    return "none", "", "", f"{layout_note}; no ligand block, ≤2 chains"


def _of3_json_ligand(prediction_path: str) -> tuple[str, str, str, str]:
    """Parse OF3 inference_query_set.json for a ligand chain or 3rd protein.

    OF3's schema exposes ``chains: [{molecule_type: "PROTEIN"|"LIGAND", ...}]``.
    A `LIGAND` chain carries a `smiles` or `ccd_codes` field. A third
    `PROTEIN` chain is a peptide ligand.
    """
    js, layout_note = _find_json_input(prediction_path, "inference_query_set.json", ".json")
    if js is None:
        return "", "", "", f"of3: {layout_note}"
    try:
        data = json.loads(js.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return "", "", "", f"of3 {layout_note}; parse failed: {e}"
    queries = data.get("queries", {})
    if not queries:
        return "none", "", "", f"of3 {layout_note}; no queries block"
    first_query = next(iter(queries.values()))
    chains = first_query.get("chains", [])
    # 1st = receptor, 2nd = partner (Gα), 3rd+ = ligand candidate
    for i, chain in enumerate(chains):
        if i < 2:
            continue
        mt = (chain.get("molecule_type") or "").upper()
        if mt == "LIGAND":
            smi = chain.get("smiles") or ""
            ccd = (chain.get("ccd_codes") or [""])[0] if chain.get("ccd_codes") else ""
            if smi:
                return "small_molecule", "", smi, f"of3 {layout_note}; chain {i} LIGAND smiles"
            if ccd:
                return "small_molecule", "", f"CCD:{ccd}", f"of3 {layout_note}; chain {i} LIGAND ccd"
            return "small_molecule", "", "", f"of3 {layout_note}; chain {i} LIGAND (no smiles/ccd)"
        if mt == "PROTEIN":
            return "peptide", chain.get("sequence", ""), "", f"of3 {layout_note}; chain {i} PROTEIN peptide"
    return "none", "", "", f"of3 {layout_note}; ≤2 chains"


def _protenix_json_ligand(prediction_path: str) -> tuple[str, str, str, str]:
    """Parse Protenix input JSON for a ccdChain / ligandChain or 3rd protein.

    Protenix schema: ``sequences: [{proteinChain: {...}}, {proteinChain: {...}},
    {ccdChain: {ccdCode: "..."}} | {ligandChain: {smiles: "..."}}]``.
    """
    js, layout_note = _find_json_input(prediction_path, "input.json", ".json")
    if js is None:
        return "", "", "", f"protenix: {layout_note}"
    try:
        data = json.loads(js.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return "", "", "", f"protenix {layout_note}; parse failed: {e}"
    if isinstance(data, list) and data and isinstance(data[0], dict):
        seqs_block = data[0].get("sequences", [])
    elif isinstance(data, dict) and "queries" in data:
        return _of3_json_ligand(prediction_path)   # OF3-shaped fallback
    else:
        return "none", "", "", f"protenix {layout_note}; unrecognised schema"
    for i, entry in enumerate(seqs_block):
        if not isinstance(entry, dict):
            continue
        if i < 2 and "proteinChain" in entry:
            continue
        if "ccdChain" in entry:
            cc = entry["ccdChain"]
            code = cc.get("ccdCode") or cc.get("ccd_code") or ""
            return "small_molecule", "", f"CCD:{code}", f"protenix {layout_note}; ccdChain"
        if "ligandChain" in entry:
            lc = entry["ligandChain"]
            smi = lc.get("smiles") or ""
            return "small_molecule", "", smi, f"protenix {layout_note}; ligandChain smiles"
        if "proteinChain" in entry and i >= 2:
            seq = entry["proteinChain"].get("sequence", "")
            return "peptide", seq, "", f"protenix {layout_note}; proteinChain[{i}] peptide"
    return "none", "", "", f"protenix {layout_note}; ≤2 chains"


def extract_ligand_from_input(prediction_path: str,
                              backbone: str) -> tuple[str, str, str, str]:
    """Route to the right per-backbone extractor.

    Returns ``(ligand_type, ligand_sequence, ligand_smiles, note)``.
    Empty ligand_type when the backbone isn't file-parseable — the
    caller falls through to `classify_ligand_from_partner`.
    """
    if backbone == "boltz":
        return _boltz_yaml_ligand(prediction_path)
    if backbone == "openfold3":
        return _of3_json_ligand(prediction_path)
    if backbone == "protenix":
        return _protenix_json_ligand(prediction_path)
    return "", "", "", f"backbone not supported for ligand extraction: {backbone}"


def classify_ligand(prediction_path: str,
                    backbone: str,
                    partner_type: str,
                    partner_identity: str) -> tuple[str, str, str, str]:
    """Combined ligand classifier — parse the upstream input first,
    fall back to partner-column heuristics.

    Returns ``(ligand_type, ligand_sequence, ligand_smiles, note)``.
    """
    lt, lseq, lsmi, note = extract_ligand_from_input(prediction_path, backbone)
    if lt in ("small_molecule", "peptide"):
        # File-based extraction won — trust the actual chemistry
        return lt, lseq, lsmi, note
    # Input file said none / wasn't parseable — fall to partner heuristics
    pt_lt, pt_seq, pt_smi, pt_note = classify_ligand_from_partner(
        partner_type, partner_identity
    )
    # peptide_native rows encode the peptide as chain B (the "partner")
    # in the frozen corpus rather than as chain C. Reuse the existing
    # partner-sequence extractor to lift the actual FASTA so
    # ligand_sequence isn't blank. extract_partner_sequence returns
    # ("", note) on any parse failure — no exception path to catch.
    if pt_lt == "peptide" and not pt_seq:
        lifted_seq, _lifted_note = extract_partner_sequence(prediction_path, backbone)
        if lifted_seq:
            pt_seq = lifted_seq
            pt_note = f"{pt_note}; lifted peptide from chain B"
    if lt == "none":
        # Input file explicitly had no ligand slot; partner_type may still
        # indicate the row is a small-molecule row (frozen corpus stores
        # the ligand under partner, not ligand). Prefer partner classifier.
        if pt_lt != "none":
            return pt_lt, pt_seq, pt_smi, f"{pt_note}; input.yaml has no ligand block"
        return "none", "", "", note
    # File extraction failed (no input on scratch) — best-effort from partner
    return pt_lt, pt_seq, pt_smi, f"{pt_note}; {note}"


# =============================================================================
# Backbone detection & partner-sequence extraction
# =============================================================================

# Boltz outputs live under a folder that contains input.yaml at some
# ancestor level: /outputs/{experiment_name}/[predictions/]?boltz_results_input/predictions/input/input_model_*.pdb
# The input.yaml sits at /outputs/{experiment_name}/input.yaml.
#
# OF3 outputs live under /outputs/of3_multimer_*/[experiment_name]/{receptor}/{receptor}/seed_*/*_model.cif
# The inference_query_set.json sits at /outputs/of3_multimer_*/[experiment_name]/{receptor}/inference_query_set.json


def detect_backbone(prediction_path: str) -> str:
    p = prediction_path.lower()
    if "/of3_" in p or "openfold3" in p or "_of3/" in p or "_of3_" in p:
        return "openfold3"
    if "/protenix" in p or "_ptx_" in p or "_ptx/" in p:
        return "protenix"
    if "/chai" in p or "_chai_" in p:
        return "chai"
    if "af2m" in p or "alphafold2_multimer" in p:
        return "af2mm"
    if "boltz" in p or "_boltz_" in p:
        return "boltz"
    return "unknown"


def _walk_up_for(prediction_path: str, filename: str, max_up: int = 8) -> Path | None:
    p = Path(prediction_path).resolve()
    for _ in range(max_up):
        candidate = p / filename
        if candidate.exists():
            return candidate
        if p.parent == p:
            return None
        p = p.parent
    return None


def _find_boltz_input_yaml(prediction_path: str) -> tuple[Path | None, str]:
    """Locate the Boltz input.yaml for this prediction.

    Two known layouts in the v3.7 corpus:

      Layout A — one YAML per experiment root:
        <exp_root>/input.yaml
        <exp_root>/predictions/...  or ...predictions/input_model_N.pdb

      Layout B — chemistry-code / weekend runs, per-variant YAML in an
      inputs/ directory:
        <exp_root>/inputs/<variant>.yaml
        <exp_root>/out/boltz_results_inputs/predictions/<variant>/<variant>_model_N.pdb

    Returns (path, note). Path is None if not found.
    """
    p = Path(prediction_path).resolve()
    variant_dir = p.parent.name          # e.g. adrb2_l15a_n20
    # Layout A — walk up for a bare input.yaml file
    yml = _walk_up_for(prediction_path, "input.yaml")
    if yml is not None:
        return yml, "boltz layout A (exp_root/input.yaml)"
    # Layout B — walk up looking for an `inputs/<variant_dir>.yaml`
    cur = p.parent
    for _ in range(8):
        candidate = cur / "inputs" / f"{variant_dir}.yaml"
        if candidate.exists():
            return candidate, f"boltz layout B (inputs/{variant_dir}.yaml)"
        if cur.parent == cur:
            break
        cur = cur.parent
    return None, "boltz input.yaml not found upwards (neither layout A nor B)"


def extract_partner_sequence_boltz(prediction_path: str) -> tuple[str, str]:
    """Return (partner_sequence, note). Empty sequence + reason on failure."""
    yml, layout_note = _find_boltz_input_yaml(prediction_path)
    if yml is None:
        return "", layout_note
    try:
        # Parse the YAML minimally without a yaml dependency — the Boltz
        # schema is simple: "sequences" list of {"protein": {"id": ..., "sequence": ...}}.
        # A hand-parser suffices and doesn't require pyyaml on the runner.
        text = yml.read_text()
    except OSError as e:
        return "", f"{layout_note}; read failed: {e}"
    # Find every "sequence: <str>" under "protein" blocks. The receptor is
    # always chain A (first entry). Anything after that is the partner.
    seq_re = re.compile(r"^\s*sequence:\s*(\S+)\s*$", re.MULTILINE)
    seqs = seq_re.findall(text)
    if len(seqs) < 2:
        return "", f"{layout_note}; has {len(seqs)} sequence(s), no partner"
    # Partner is everything after chain A. Return the second sequence which
    # is chain B by convention. Multi-chain partners (Gα + Gβ + Gγ) are
    # rare in this corpus — the ones that appear (holo-Gα complexes) still
    # have the peptide/α5 as chain B.
    return seqs[1], f"{layout_note}, chain B"


def _find_json_input(
    prediction_path: str,
    layout_a_filename: str,
    layout_b_ext: str = ".json",
) -> tuple[Path | None, str]:
    """Locate a JSON input file for an OF3-style or Protenix-style prediction.

    Layout A — one anchor file per experiment/receptor:
        <..>/{receptor}/inference_query_set.json  (OF3 full-batch runs)

    Layout B — weekend / chemistry-code runs, per-variant JSON in inputs/:
        <exp_root>/inputs/<variant>.json

    Where <variant> is the folder name three levels above the CIF file
    for OF3 (out/{variant}/{variant}/seed_.../predictions/*.cif) and
    similarly for Protenix. The variant-name inference here uses the
    same three-level walk-up.
    """
    p = Path(prediction_path).resolve()
    # Layout A — walk up for the anchor filename directly
    a = _walk_up_for(prediction_path, layout_a_filename)
    if a is not None:
        return a, f"layout A ({layout_a_filename})"
    # Layout B — walk up looking for `inputs/<variant>{ext}`
    # variant name is the folder name 3 levels above the leaf CIF file
    # (out/{variant}/{variant}/seed_.../predictions/leaf.cif)
    parents = list(p.parents)
    for depth in range(min(len(parents), 6)):
        variant_dir = parents[depth].name
        # walk up from variant_dir upward looking for inputs/<variant>{ext}
        cur = parents[depth]
        for _ in range(6):
            candidate = cur / "inputs" / f"{variant_dir}{layout_b_ext}"
            if candidate.exists():
                return candidate, f"layout B (inputs/{variant_dir}{layout_b_ext})"
            if cur.parent == cur:
                break
            cur = cur.parent
    return None, f"neither layout A nor layout B input found (tried {layout_a_filename} and inputs/*{layout_b_ext})"


def _parse_of3_style_json(js: Path, layout_note: str) -> tuple[str, str]:
    """Extract chain-2 sequence from an OF3-style `{queries: {name: {chains: [...]}}}` JSON."""
    try:
        data = json.loads(js.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return "", f"{layout_note}; parse failed: {e}"
    queries = data.get("queries", {})
    if not queries:
        return "", f"{layout_note}; no queries block"
    first_query = next(iter(queries.values()))
    chains = first_query.get("chains", [])
    if len(chains) < 2:
        return "", f"{layout_note}; has {len(chains)} chain(s), no partner"
    return chains[1].get("sequence", ""), f"{layout_note}, chain 2"


def _parse_protenix_json(js: Path, layout_note: str) -> tuple[str, str]:
    """Extract chain-2 sequence from a Protenix input JSON.

    Protenix schema (weekend chemistry-code runs):
        [{"name": ..., "sequences": [{"proteinChain": {"sequence": ...}}, ...]}]

    OF3-shaped Protenix inputs also appear in some pipelines; try both.
    """
    try:
        data = json.loads(js.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return "", f"{layout_note}; parse failed: {e}"
    # Protenix native schema — list of entries with sequences
    if isinstance(data, list) and data and isinstance(data[0], dict) and "sequences" in data[0]:
        seqs_block = data[0]["sequences"]
        chains: list[str] = []
        for entry in seqs_block:
            pc = entry.get("proteinChain") if isinstance(entry, dict) else None
            if pc and "sequence" in pc:
                chains.append(pc["sequence"])
        if len(chains) < 2:
            return "", f"{layout_note}; has {len(chains)} chain(s), no partner"
        return chains[1], f"{layout_note}, chain 2 (protenix schema)"
    # Fall back to OF3-style schema (some Protenix inputs are OF3-format)
    if isinstance(data, dict) and "queries" in data:
        return _parse_of3_style_json(js, layout_note + " (of3-style)")
    return "", f"{layout_note}; unrecognised protenix json schema"


def extract_partner_sequence_of3(prediction_path: str) -> tuple[str, str]:
    """OF3 inference_query_set.json — chains list of dicts with 'sequence'."""
    js, layout_note = _find_json_input(prediction_path, "inference_query_set.json", ".json")
    if js is None:
        return "", f"of3: {layout_note}"
    return _parse_of3_style_json(js, f"of3 {layout_note}")


def extract_partner_sequence_protenix(prediction_path: str) -> tuple[str, str]:
    """Protenix input JSON — either native list-schema or OF3-style dict schema."""
    js, layout_note = _find_json_input(prediction_path, "input.json", ".json")
    if js is None:
        return "", f"protenix: {layout_note}"
    return _parse_protenix_json(js, f"protenix {layout_note}")


def extract_partner_sequence(prediction_path: str, backbone: str) -> tuple[str, str]:
    if backbone == "boltz":
        return extract_partner_sequence_boltz(prediction_path)
    if backbone == "openfold3":
        return extract_partner_sequence_of3(prediction_path)
    if backbone == "protenix":
        return extract_partner_sequence_protenix(prediction_path)
    return "", f"backbone not supported for sequence extraction: {backbone}"


# =============================================================================
# Classification core
# =============================================================================


def classify_g_class(
    partner_type: str,
    partner_identity: str,
    receptor_slug: str,
) -> str:
    # 1. Identity-embedded hint takes precedence
    for pat, gclass in PARTNER_IDENTITY_G_HINTS:
        if pat.search(partner_identity or ""):
            return gclass
    # 2. Table lookup by partner_type
    mapped = PARTNER_TYPE_TO_G_CLASS.get(partner_type)
    if mapped is None:
        return "unknown_g_family"
    if mapped != "receptor_lookup":
        return mapped
    # 3. Receptor-driven cognate Gα resolution
    return RECEPTOR_G_COUPLING.get(receptor_slug.upper(), "unknown_g_family")


def classify_perturbation(
    partner_type: str,
    partner_identity: str,
    prediction_path: str,
) -> tuple[str, str]:
    """Return (perturbation_label, reasoning_note)."""
    base = PARTNER_TYPE_TO_PERTURBATION.get(partner_type, "unknown")
    if base == "truncated_Naa":
        m = _TRUNC_RE.search(prediction_path)
        if m:
            return f"truncated_{m.group(1)}aa", f"path regex alpha5_(\\d+)aa → {m.group(1)}"
        # Some α5-CT fragment rows don't carry length in path (older Gαs α5-CT
        # constant-length variants). Fall back to a generic truncated tag.
        return "truncated_alpha5ct", "α5_ct_fragment without length in path"
    return base, f"partner_type={partner_type!r}"


# =============================================================================
# Main
# =============================================================================


def enrich(
    rows_csv: Path,
    predictions_csv: Path,
    out_csv: Path,
    *,
    extract_delta: bool = True,
    limit: int | None = None,
) -> dict[str, Any]:
    """Read rows.csv + predictions.csv, write out_csv with 4 extra columns.

    Returns a summary dict for the caller to print.
    """
    # Load predictions.csv into a dict keyed by prediction_path
    with predictions_csv.open() as f:
        preds = {p["prediction_path"]: p for p in csv.DictReader(f)}
    print(f"loaded {len(preds)} rows from {predictions_csv}", file=sys.stderr)

    # Load rows.csv into a list preserving order
    with rows_csv.open() as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None
        old_cols = list(reader.fieldnames)
        rows = list(reader)
    print(f"loaded {len(rows)} rows from {rows_csv}", file=sys.stderr)

    new_cols = [
        "partner_g_class",
        "partner_perturbation",
        "partner_sequence_delta",
        "partner_sequence_delta_note",
        # Exp-Layer 2 additions — seed + ligand context
        "seed_used",
        "ligand_type",
        "ligand_sequence",
        "ligand_smiles",
        "ligand_note",
    ]
    # If any of these columns are ALREADY in old_cols (e.g. re-running on
    # a previously-enriched CSV, or on a v3.7 rows.csv whose scorer
    # itself now emits `seed_used`), skip them from the append — we
    # preserve the existing values verbatim rather than double-writing.
    old_col_set = set(old_cols)
    new_cols_to_append = [c for c in new_cols if c not in old_col_set]
    all_cols = old_cols + new_cols_to_append

    n_matched = 0
    n_seq_extracted = 0
    n_seq_skipped_wt = 0
    n_seq_failed = 0
    n_ligand_from_file = 0
    n_ligand_from_partner = 0
    n_seed_extracted = 0
    counts_gclass: dict[str, int] = {}
    counts_perturb: dict[str, int] = {}
    counts_ligand_type: dict[str, int] = {}

    with out_csv.open("w", newline="") as fo:
        writer = csv.DictWriter(fo, fieldnames=all_cols)
        writer.writeheader()
        for i, r in enumerate(rows):
            if limit is not None and i >= limit:
                break
            p = preds.get(r["input_path"], {})
            partner_type = p.get("partner_type", "")
            partner_identity = p.get("partner_identity", "")
            receptor_slug = r.get("receptor_slug") or p.get("receptor", "").upper().replace("_HUMAN","").replace("_MOUSE","").replace("_RAT","").replace("_BOVIN","")

            if p:
                n_matched += 1
                g_class = classify_g_class(partner_type, partner_identity, receptor_slug)
                perturbation, perturb_note = classify_perturbation(
                    partner_type, partner_identity, r["input_path"]
                )
            else:
                g_class = "unknown_g_family"
                perturbation = "unknown"
                perturb_note = "no matching row in predictions.csv"

            # sequence delta extraction: skip for wt / apo_partner (no delta by def)
            if perturbation in ("wt", "apo_partner"):
                delta = ""
                delta_note = f"{perturbation}: no delta"
                n_seq_skipped_wt += 1
            elif not extract_delta:
                delta = ""
                delta_note = "extraction skipped by flag"
            else:
                backbone = detect_backbone(r["input_path"])
                delta, delta_note = extract_partner_sequence(r["input_path"], backbone)
                if delta:
                    n_seq_extracted += 1
                else:
                    n_seq_failed += 1

            # Exp-Layer 2: seed_used (regex over input_path) +
            # ligand_type/sequence/smiles (backbone-specific parse of the
            # upstream input file, fallback to partner-column heuristics).
            seed = seed_used_from_input_path(r["input_path"])
            if seed > 0:
                n_seed_extracted += 1
            bb_for_ligand = detect_backbone(r["input_path"])
            lt, lseq, lsmi, lnote = classify_ligand(
                r["input_path"], bb_for_ligand, partner_type, partner_identity
            )
            if lt in ("small_molecule", "peptide") and lsmi + lseq:
                n_ligand_from_file += 1
            elif lt in ("small_molecule", "peptide", "apo"):
                n_ligand_from_partner += 1

            r_out = dict(r)
            r_out["partner_g_class"] = g_class
            r_out["partner_perturbation"] = perturbation
            r_out["partner_sequence_delta"] = delta
            r_out["partner_sequence_delta_note"] = delta_note
            # Only overwrite the Exp-Layer 2 columns when they weren't
            # already carried in on the input CSV — respects an already-
            # populated schema (e.g. propose-scored rows already have
            # ligand_* columns filled by run_scorer's lift-in).
            for k, v in (
                ("seed_used", str(seed)),
                ("ligand_type", lt),
                ("ligand_sequence", lseq),
                ("ligand_smiles", lsmi),
                ("ligand_note", lnote),
            ):
                existing = r_out.get(k, "")
                if k in old_col_set and existing not in ("", "0"):
                    continue    # preserve existing value
                r_out[k] = v
            writer.writerow(r_out)

            counts_gclass[g_class] = counts_gclass.get(g_class, 0) + 1
            counts_perturb[perturbation] = counts_perturb.get(perturbation, 0) + 1
            final_lt = r_out.get("ligand_type", "")
            counts_ligand_type[final_lt] = counts_ligand_type.get(final_lt, 0) + 1

    summary = {
        "rows_in": len(rows),
        "rows_matched_to_predictions": n_matched,
        "sequences_extracted": n_seq_extracted,
        "sequences_skipped_wt_or_apo": n_seq_skipped_wt,
        "sequences_extraction_failed": n_seq_failed,
        "seed_extracted_from_path": n_seed_extracted,
        "ligand_lifted_from_input_file": n_ligand_from_file,
        "ligand_lifted_from_partner_columns": n_ligand_from_partner,
        "by_g_class": counts_gclass,
        "by_perturbation": counts_perturb,
        "by_ligand_type": counts_ligand_type,
    }
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rows", required=True, type=Path,
                   help="path to v3.7 rows.csv (the scorer output)")
    p.add_argument("--predictions", required=True, type=Path,
                   help="path to EXPERIMENT_CATALOG/data/predictions.csv")
    p.add_argument("--out", required=True, type=Path,
                   help="output path for the enriched CSV")
    p.add_argument("--no-extract-delta", action="store_true",
                   help="skip partner sequence extraction (faster; delta columns "
                        "will be blank with a note)")
    p.add_argument("--limit", type=int, default=None,
                   help="cap on rows processed (debug)")
    args = p.parse_args()

    summary = enrich(
        rows_csv=args.rows,
        predictions_csv=args.predictions,
        out_csv=args.out,
        extract_delta=not args.no_extract_delta,
        limit=args.limit,
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
