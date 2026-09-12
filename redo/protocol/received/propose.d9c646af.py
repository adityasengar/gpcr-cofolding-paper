"""gpcr-propose — pre-flight acceptance gate for new prediction proposals.

Layer 2 of the pre-check work (plan silly-leaping-aho.md). Takes a YAML
proposal spec, runs all five pre-checks per (backbone × seed) row, and
emits a manifest CSV that is a strict superset of ``refs/rerun_manifest.csv``
plus a ``pre_check_status`` column.

The CLI never refuses a proposal (per user's "warn but never refuse"
decision). Every row is emitted; every row carries a ``pre_check_status``
value from ``{pass, warn_A1, warn_A2, warn_A3, warn_A5, warn_A6,
warn_multiple}``. Downstream analysis filters on this flag to distinguish
"known-to-fail run" from "unknown-outcome run" (see Q7 in
docs/PIPELINE_INTERPRETATION.md).

Usage:

    gpcr-propose --spec refs/proposals/aa2ar_gs_2026_09.yaml
    gpcr-propose --spec ... --pre-check-only
    gpcr-propose --spec ... --out refs/proposals/aa2ar_gs_2026_09.manifest.csv

YAML schema (all fields required unless noted):

    request_id: aa2ar_gs_confirmation_2026_09
    biological_question: "Does AA2AR fold to active with cognate Gs?"
    receptor: AA2AR              # receptor slug OR uniprot slug (aa2ar_human)
    partner:
      type: g_alpha              # g_alpha / peptide / small_molecule / apo / arrestin
      identity: alphas           # partners.fasta header id, or "" for apo
      sequence_fasta: "MG..."    # optional inline override
    state_claim: Ga-coupled-active   # a valid StateClaim enum value
    backbones: [boltz, of3, protenix]
    seeds: 10
    samples_per_seed: 1          # optional; >1 tells the backbone qsub to
                                 # emit N diffusion samples per seed
                                 # (Boltz --diffusion_samples, OF3
                                 # --num-diffusion-samples, Protenix
                                 # --sample, Chai --num-diffn-samples).
    species: human
    partner_perturbation: wt     # wt / truncated_Naa / shuffled / mutated / chimeric / designed
    receptor_sequence_fasta: ""  # optional inline receptor override

Every row emitted equals one (backbone × seed_index) proposal. Seeds are
derived deterministically from a per-row SHA of the request_id + backbone
+ seed_index (see ``_derive_row_seed``).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# yaml is a hard dependency (added to pyproject.toml alongside this module).
# Failing loudly here is preferable to a hand-parser that misses edge cases.
import yaml

from scorer.bw_numbering import Api, get_generic_numbers
from scorer.cache import content_sha256
from scorer.pre_check import (
    load_ref_species_map,
    run_all_checks,
    summarise,
)
from scorer.receptors import KNOWN_RECEPTORS, RECEPTOR_CLASS
from scorer.rerun import fresh_seed_for
from scorer.schema import LigandType, PROPOSE_MANIFEST_COLUMNS, StateClaim
from scorer.structure import STD_AA


REPO = Path(__file__).resolve().parent.parent
REF_SET_CSV = REPO / "refs" / "reference_set.csv"
PARTNERS_FASTA = REPO / "docs" / "EXPERIMENT_CATALOG" / "sequences" / "partners.fasta"
RECEPTORS_FASTA = REPO / "docs" / "EXPERIMENT_CATALOG" / "sequences" / "receptors.fasta"
DEFAULT_CACHE_DIR = REPO / "refs" / "cache" / "gpcrdb"
DEFAULT_OUTPUT_ROOT = Path("/hpc/scratch/sengaad1/paper_af3/propose")

# Every backbone we materialise. Kept ordered so downstream tools that
# enumerate backbones get a stable list.
KNOWN_BACKBONES = ("boltz", "of3", "protenix", "chai", "af2mm")

# Filename extensions per backbone
_BACKBONE_EXT = {
    "boltz":    "yaml",
    "of3":      "json",
    "protenix": "json",
    "chai":     "fasta",
    "af2mm":     "fasta",
}

# Fold-model output filename patterns per backbone (what the qsub scripts
# eventually write when they finish folding — this is what the scorer
# joins on later). Layer 3 stamps this into `prediction_path`.
_BACKBONE_OUTPUT_LEAF = {
    "boltz":    "model_0.pdb",
    "of3":      "model_0.cif",
    "protenix": "sample_0.cif",
    "chai":     "pred.model_idx_0.cif",
    "af2mm":     "model_1.pdb",
}


# ---------------------------------------------------------------------------
# YAML loading + validation
# ---------------------------------------------------------------------------


class SpecError(ValueError):
    """A YAML spec is missing required fields or carries invalid values."""


_REQUIRED_TOP_LEVEL = ("request_id", "receptor", "state_claim",
                       "backbones", "seeds", "species", "partner_perturbation")

_KNOWN_BACKBONES = frozenset({"boltz", "of3", "protenix", "chai", "af2mm"})


def load_spec(spec_path: str | Path) -> dict[str, Any]:
    """Load and validate a proposal YAML.

    Raises SpecError with a specific message on missing/invalid fields.
    Returns the parsed dict (with defaults filled in for optional keys).
    """
    p = Path(spec_path)
    if not p.exists():
        raise SpecError(f"spec file not found: {p}")
    with p.open() as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise SpecError(f"spec must be a YAML mapping; got {type(data).__name__}")

    missing = [k for k in _REQUIRED_TOP_LEVEL if k not in data]
    if missing:
        raise SpecError(f"missing required field(s): {missing}")

    state_claim = data["state_claim"]
    valid_states = {s.value for s in StateClaim}
    if state_claim not in valid_states:
        raise SpecError(
            f"state_claim {state_claim!r} not valid; must be one of {sorted(valid_states)}"
        )

    backbones = data["backbones"]
    if not isinstance(backbones, list) or not backbones:
        raise SpecError("backbones must be a non-empty list")
    unknown_bb = [b for b in backbones if b not in _KNOWN_BACKBONES]
    if unknown_bb:
        raise SpecError(
            f"unknown backbones {unknown_bb}; valid: {sorted(_KNOWN_BACKBONES)}"
        )

    seeds = data["seeds"]
    if not isinstance(seeds, int) or seeds < 1:
        raise SpecError(f"seeds must be a positive integer; got {seeds!r}")

    # Diversity-study extension (2026-08-27): `samples_per_seed` (default 1).
    # Values >1 tell the dispatcher to bump the backbone-specific "samples
    # per fold" flag so ONE qsub job emits N diffusion samples from the same
    # seed (single model load, N decoder passes). Default 1 preserves the
    # historical one-sample-per-seed behaviour byte-for-byte.
    sps = data.get("samples_per_seed", 1)
    if not isinstance(sps, int) or sps < 1:
        raise SpecError(
            f"samples_per_seed must be a positive integer; got {sps!r}"
        )
    data["samples_per_seed"] = sps

    # partner block is optional (apo); when present it must be a dict
    partner = data.get("partner") or {}
    if not isinstance(partner, dict):
        raise SpecError(f"partner block must be a mapping; got {type(partner).__name__}")
    data["partner"] = partner
    data.setdefault("biological_question", "")

    # Exp-Layer 1: optional `ligand:` block. When present it MUST be a
    # mapping with a valid `type` (matching LigandType enum). Field
    # combinations are validated by check_ligand_block below.
    ligand = data.get("ligand")
    if ligand is None:
        data["ligand"] = {"type": LigandType.NONE.value}
    else:
        if not isinstance(ligand, dict):
            raise SpecError(f"ligand block must be a mapping; got {type(ligand).__name__}")
        _validate_ligand_block(ligand)
        data["ligand"] = ligand

    return data


def _validate_ligand_block(ligand: dict[str, Any]) -> None:
    """Raise SpecError when the ligand block is malformed.

    Rules:
      - `type` is required and must be one of LigandType enum values.
      - `peptide` requires a non-empty `sequence` and forbids `smiles`.
      - `small_molecule` requires a non-empty `smiles` and forbids
        `sequence`.
      - `apo` / `none` forbid both `sequence` and `smiles`.
    """
    valid_types = {t.value for t in LigandType}
    lt = ligand.get("type", "")
    if lt not in valid_types:
        raise SpecError(
            f"ligand.type must be one of {sorted(valid_types)}; got {lt!r}"
        )
    seq = (ligand.get("sequence") or "").strip()
    smi = (ligand.get("smiles") or "").strip()
    if lt == LigandType.PEPTIDE.value:
        if not seq:
            raise SpecError("ligand.type=peptide requires a non-empty `sequence`")
        if smi:
            raise SpecError("ligand.type=peptide forbids `smiles` (use type=small_molecule)")
    elif lt == LigandType.SMALL_MOLECULE.value:
        if not smi:
            raise SpecError("ligand.type=small_molecule requires a non-empty `smiles`")
        if seq:
            raise SpecError("ligand.type=small_molecule forbids `sequence` (use type=peptide)")
    else:  # apo, none
        if seq or smi:
            raise SpecError(
                f"ligand.type={lt!r} forbids `sequence` and `smiles` "
                f"(these apply only to peptide / small_molecule)"
            )


# ---------------------------------------------------------------------------
# Sequence resolution — receptor + partner
# ---------------------------------------------------------------------------


def _canonicalise_receptor(slug_or_entry: str) -> str:
    """Normalise the receptor field to a KNOWN_RECEPTORS key (uppercase).

    Accepts either the receptor family slug ("AA2AR", "aa2ar") or the
    UniProt entry name ("aa2ar_human"). Returns the family slug in
    uppercase. Empty string if not recognised.
    """
    s = slug_or_entry.strip()
    if not s:
        return ""
    up = s.upper()
    if up in KNOWN_RECEPTORS:
        return up
    # try uniprot entry-name lookup (case-insensitive)
    low = s.lower()
    for slug, entry in KNOWN_RECEPTORS.items():
        if entry == low:
            return slug
    return up  # unknown; keep the caller-provided form for A6 to catch


def _parse_fasta(path: Path) -> dict[str, str]:
    """Return ``{header_id: sequence}`` from a multi-record FASTA.

    ``header_id`` is the first ``|``-separated token from the record's
    header line (immediately after ``>``).
    """
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    header: str = ""
    chunks: list[str] = []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if header:
                out[header] = "".join(chunks)
            header = line[1:].split("|", 1)[0].strip()
            chunks = []
        else:
            chunks.append(line.strip())
    if header:
        out[header] = "".join(chunks)
    return out


def _wt_receptor_fasta(receptor_slug: str, api: Api) -> str:
    """Return the canonical UniProt WT receptor FASTA.

    Sourced from GPCRdb ``get_generic_numbers`` (the same call the scorer
    uses to resolve BW anchors). This gives the UniProt-canonical WT,
    which is the correct starting point for a NEW proposal: the fold
    model will be handed exactly this sequence.

    Deliberately does NOT read
    ``docs/EXPERIMENT_CATALOG/sequences/receptors.fasta`` — those entries
    are the FROZEN-CORPUS CONSTRUCT sequences (with N-terminal FLAG tags,
    signal peptides, thermostabilising mutations) used to reproduce prior
    experimental setups. A pre-check must be measured against the WT the
    proposal will actually run, so GPCRdb is the right source.

    Empty string if the receptor is unknown or GPCRdb resolution fails —
    PC1/PC3/PC4 handle that gracefully.

    Analysts who want to run against a specific construct (thermostabilised
    variant, signal-peptide fusion, chimera) can inline the sequence in
    the YAML under ``receptor_sequence_fasta``.
    """
    up = receptor_slug.strip().upper()
    if up not in KNOWN_RECEPTORS:
        return ""
    entry_name = KNOWN_RECEPTORS[up]
    try:
        bw_map = get_generic_numbers(api, entry_name)
    except Exception:
        return ""
    positions = {int(p): info["aa"] for p, info in bw_map.items()
                 if info.get("aa") and info["aa"] in STD_AA}
    if not positions:
        return ""
    max_pos = max(positions)
    chars = ["-"] * max_pos
    for pos, aa in positions.items():
        chars[pos - 1] = aa
    return "".join(chars)


def _partner_fasta(identity: str) -> str:
    """Return the partner FASTA for a partner-identity slug.

    Reads docs/EXPERIMENT_CATALOG/sequences/partners.fasta. Empty
    identity ("") means apo — returns empty.
    """
    if not identity:
        return ""
    partners = _parse_fasta(PARTNERS_FASTA)
    key = identity.strip()
    # partners.fasta uses lowercase family names (alphas, alphai1, ...)
    for k in (key, key.lower(), key.upper()):
        if k in partners:
            return partners[k]
    return ""


# ---------------------------------------------------------------------------
# Input-file templaters (per backbone)
#
# These emit the exact input-file schema each fold model consumes, using
# the same shape as the frozen corpus's inputs. Adapted (byte-parity where
# feasible) from `subsampling/scripts/weekend/build_weekend.py` — the
# reference templater under the source branch that produced the frozen
# corpus's Boltz/OF3/Protenix inputs. That way a proposal materialised
# here scores identically at the fold-model level to a corpus experiment.
#
# Every templater is a pure function of (rseq, pseq) — or (rseq,) for
# monomer — and returns the file *content* as a string. The dispatcher
# below writes the string to disk and stamps its SHA into the manifest.
# ---------------------------------------------------------------------------


def _boltz_yaml_monomer(rseq: str) -> str:
    return (
        "version: 1\n"
        "sequences:\n"
        "  - protein:\n"
        "      id: A\n"
        f"      sequence: {rseq}\n"
    )


def _boltz_yaml_two_chain(rseq: str, pseq: str) -> str:
    return (
        "version: 1\n"
        "sequences:\n"
        "  - protein:\n"
        "      id: A\n"
        f"      sequence: {rseq}\n"
        "  - protein:\n"
        "      id: B\n"
        f"      sequence: {pseq}\n"
    )


def _boltz_ligand_block(
    ligand_type: str,
    ligand_sequence: str,
    ligand_smiles: str,
    ligand_chain_id: str = "L",
) -> str:
    """Emit the Boltz YAML block for a ligand attachment. Empty string
    for ligand_type in {"none", "apo", ""} (nothing to add).

    Peptide ligands are appended as a `protein:` chain (Boltz treats
    peptides as short proteins). Small-molecule ligands are appended as
    a `ligand:` block with a `smiles:` field — Boltz's canonical way to
    accept a SMILES-defined small molecule.
    """
    if not ligand_type or ligand_type in ("none", "apo"):
        return ""
    if ligand_type == "peptide":
        return (
            "  - protein:\n"
            f"      id: {ligand_chain_id}\n"
            f"      sequence: {ligand_sequence}\n"
        )
    if ligand_type == "small_molecule":
        return (
            "  - ligand:\n"
            f"      id: {ligand_chain_id}\n"
            f"      smiles: '{ligand_smiles}'\n"
        )
    raise ValueError(f"unsupported ligand_type for Boltz: {ligand_type!r}")


def _of3_query_dict(name: str, chains: list[dict[str, Any]], is_multimer: bool, seed: int) -> dict[str, Any]:
    return {
        "seeds": [seed],
        "queries": {
            name: {
                "query_name": name,
                "chains": chains,
                "use_msas": True,
                "use_paired_msas": is_multimer,
                "use_main_msas": True,
            }
        },
    }


def _of3_ligand_chain(ligand_type: str, ligand_sequence: str,
                      ligand_smiles: str, chain_id: str = "L") -> dict[str, Any] | None:
    """Return the OF3 chain entry for a ligand, or None for apo/none.

    Small-molecule → ``{molecule_type: "LIGAND", chain_ids: [L], smiles: <smi>}``
    or ``ccd_codes: ["<code>"]`` when smiles starts with ``CCD:``.
    Peptide → ``{molecule_type: "PROTEIN", chain_ids: [L], sequence: <seq>}``.
    """
    if not ligand_type or ligand_type in ("none", "apo"):
        return None
    if ligand_type == "peptide":
        return {"molecule_type": "PROTEIN", "chain_ids": [chain_id],
                "sequence": ligand_sequence}
    if ligand_type == "small_molecule":
        smi = ligand_smiles.strip()
        if smi.upper().startswith("CCD:"):
            return {"molecule_type": "LIGAND", "chain_ids": [chain_id],
                    "ccd_codes": [smi.split(":", 1)[1]]}
        return {"molecule_type": "LIGAND", "chain_ids": [chain_id],
                "smiles": smi}
    raise ValueError(f"unsupported ligand_type for OF3: {ligand_type!r}")


def _of3_json_monomer(name: str, rseq: str, seed: int,
                      ligand_chain: dict[str, Any] | None = None) -> str:
    chains = [{"molecule_type": "PROTEIN", "chain_ids": ["A"], "sequence": rseq}]
    if ligand_chain is not None:
        chains.append(ligand_chain)
    # A monomer receptor + a ligand still uses paired-MSA logic OFF (no
    # protein-protein pair to align); use_paired_msas mirrors the "is
    # there more than one protein chain" test rather than raw chain count.
    is_multimer = sum(1 for c in chains
                      if c.get("molecule_type", "").upper() == "PROTEIN") > 1
    return json.dumps(_of3_query_dict(name, chains, is_multimer=is_multimer, seed=seed), indent=2) + "\n"


def _of3_json_two_chain(name: str, rseq: str, pseq: str, seed: int,
                        ligand_chain: dict[str, Any] | None = None) -> str:
    chains = [
        {"molecule_type": "PROTEIN", "chain_ids": ["A"], "sequence": rseq},
        {"molecule_type": "PROTEIN", "chain_ids": ["B"], "sequence": pseq},
    ]
    if ligand_chain is not None:
        chains.append(ligand_chain)
    return json.dumps(_of3_query_dict(name, chains, is_multimer=True, seed=seed), indent=2) + "\n"


def _protenix_ligand_entry(ligand_type: str, ligand_sequence: str,
                           ligand_smiles: str) -> dict[str, Any] | None:
    """Return a Protenix ``sequences`` entry for a ligand, or None.

    Per the Protenix runtime schema
    (`protenix/data/inference/json_parser.py::add_entity_atom_array`),
    a ligand entity is ``{"ligand": {"ligand": "<smiles|CCD_XXX>",
    "count": 1}}``. SMILES go in verbatim; CCD codes carry the
    ``CCD_`` prefix. Historically the enricher extractor's
    ``_protenix_json_ligand`` also probes ``ligandChain{smiles}`` /
    ``ccdChain{ccdCode}`` shapes — kept as defensive parsing for
    other tools that may emit those, but the Protenix runtime only
    accepts the ``ligand`` key.

    Peptide → an extra ``proteinChain``.
    """
    if not ligand_type or ligand_type in ("none", "apo"):
        return None
    if ligand_type == "peptide":
        return {"proteinChain": {"sequence": ligand_sequence, "count": 1}}
    if ligand_type == "small_molecule":
        smi = ligand_smiles.strip()
        if smi.upper().startswith("CCD:"):
            code = smi.split(":", 1)[1]
            return {"ligand": {"ligand": f"CCD_{code}", "count": 1}}
        return {"ligand": {"ligand": smi, "count": 1}}
    raise ValueError(f"unsupported ligand_type for Protenix: {ligand_type!r}")


def _protenix_json_monomer(name: str, rseq: str,
                           ligand_entry: dict[str, Any] | None = None) -> str:
    seqs: list[dict[str, Any]] = [{"proteinChain": {"sequence": rseq, "count": 1}}]
    if ligand_entry is not None:
        seqs.append(ligand_entry)
    payload = [{"name": name, "sequences": seqs}]
    return json.dumps(payload, indent=2) + "\n"


def _protenix_json_two_chain(name: str, rseq: str, pseq: str,
                             ligand_entry: dict[str, Any] | None = None) -> str:
    seqs: list[dict[str, Any]] = [
        {"proteinChain": {"sequence": rseq, "count": 1}},
        {"proteinChain": {"sequence": pseq, "count": 1}},
    ]
    if ligand_entry is not None:
        seqs.append(ligand_entry)
    payload = [{"name": name, "sequences": seqs}]
    return json.dumps(payload, indent=2) + "\n"


def _chai_ligand_fasta(ligand_type: str, ligand_sequence: str,
                       ligand_smiles: str, name: str = "lig") -> str:
    """Return the extra FASTA record(s) for a Chai ligand, or ''.

    Small-molecule SMILES → ``>ligand|name=<name>\\n<smiles>\\n`` (Chai
    accepts SMILES in a ligand record per chai-lab docs).
    Small-molecule CCD → ``>ligand|name=<name>\\n<ccd>\\n`` (Chai's
    ligand record accepts a CCD three-letter code the same way).
    Peptide → ``>protein|name=<name>\\n<seq>\\n``.
    """
    if not ligand_type or ligand_type in ("none", "apo"):
        return ""
    if ligand_type == "peptide":
        return f">protein|name={name}\n{ligand_sequence}\n"
    if ligand_type == "small_molecule":
        smi = ligand_smiles.strip()
        if smi.upper().startswith("CCD:"):
            code = smi.split(":", 1)[1]
            return f">ligand|name={name}\n{code}\n"
        return f">ligand|name={name}\n{smi}\n"
    raise ValueError(f"unsupported ligand_type for Chai: {ligand_type!r}")


def _chai_fasta_monomer(name: str, rseq: str, ligand_fasta: str = "") -> str:
    # Chai format per corpus samples: >protein|name=<name>
    return f">protein|name={name}\n{rseq}\n" + ligand_fasta


def _chai_fasta_two_chain(rname: str, rseq: str, pname: str, pseq: str,
                          ligand_fasta: str = "") -> str:
    return (
        f">protein|name={rname}\n{rseq}\n"
        f">protein|name={pname}\n{pseq}\n"
        + ligand_fasta
    )


def _af2mm_fasta_monomer(name: str, rseq: str) -> str:
    # AF2-multimer accepts a bare-header FASTA: >chain_name
    return f">{name}\n{rseq}\n"


def _af2mm_fasta_two_chain(rname: str, rseq: str, pname: str, pseq: str) -> str:
    return f">{rname}\n{rseq}\n>{pname}\n{pseq}\n"


def _partner_is_apo(partner_type: str, partner_identity: str) -> bool:
    if partner_type == "apo":
        return True
    if not partner_type and not partner_identity:
        return True
    return False


def _partner_is_small_molecule(partner_type: str) -> bool:
    return partner_type in ("small_molecule", "ligand", "antagonist",
                            "neutral_ligand", "wrong_agonist")


def _row_input_content(
    backbone: str,
    row: dict[str, str],
    receptor_seq: str,
    partner_seq: str,
    apo: bool,
) -> str:
    """Return the input-file content string for one manifest row."""
    request_id = row["request_id"]
    seed = int(row["new_seed"])
    receptor_slug = row["receptor_resolved"]
    partner_id = row["partner_identity"] or "partner"
    # A short, deterministic input name — helps fold-model tools that
    # embed the input name in output filenames.
    input_name = f"{request_id}_{receptor_slug}_{row['backbone']}_{row['seed_index']}"
    ligand_type = row.get("ligand_type", "") or ""
    ligand_sequence = row.get("ligand_sequence", "") or ""
    ligand_smiles = row.get("ligand_smiles", "") or ""

    if backbone == "boltz":
        if apo:
            base = _boltz_yaml_monomer(receptor_seq)
        else:
            base = _boltz_yaml_two_chain(receptor_seq, partner_seq)
        # Append ligand block (empty string when ligand_type in {none,
        # apo, ""} — the common case). Chain ID "L" avoids collision
        # with the receptor (A) and partner (B).
        ligand_block = _boltz_ligand_block(
            ligand_type, ligand_sequence, ligand_smiles, ligand_chain_id="L",
        )
        return base + ligand_block
    if backbone == "of3":
        of3_lig = _of3_ligand_chain(ligand_type, ligand_sequence, ligand_smiles)
        if apo:
            return _of3_json_monomer(input_name, receptor_seq, seed,
                                     ligand_chain=of3_lig)
        return _of3_json_two_chain(input_name, receptor_seq, partner_seq, seed,
                                   ligand_chain=of3_lig)
    if backbone == "protenix":
        ptx_lig = _protenix_ligand_entry(ligand_type, ligand_sequence, ligand_smiles)
        if apo:
            return _protenix_json_monomer(input_name, receptor_seq,
                                          ligand_entry=ptx_lig)
        return _protenix_json_two_chain(input_name, receptor_seq, partner_seq,
                                        ligand_entry=ptx_lig)
    if backbone == "chai":
        chai_lig = _chai_ligand_fasta(ligand_type, ligand_sequence, ligand_smiles,
                                      name="lig")
        if apo:
            return _chai_fasta_monomer(receptor_slug.lower(), receptor_seq,
                                       ligand_fasta=chai_lig)
        return _chai_fasta_two_chain(receptor_slug.lower(), receptor_seq,
                                     partner_id.lower(), partner_seq,
                                     ligand_fasta=chai_lig)
    if backbone == "af2mm":
        if apo:
            return _af2mm_fasta_monomer(f"{receptor_slug}_alone", receptor_seq)
        return _af2mm_fasta_two_chain(f"{receptor_slug}_A", receptor_seq,
                                      f"{partner_id.lower()}_B", partner_seq)
    raise ValueError(f"unknown backbone {backbone!r}")


# ---------------------------------------------------------------------------
# Row expansion + seed derivation
# ---------------------------------------------------------------------------


def _derive_row_seed(request_id: str, backbone: str, seed_index: int) -> int:
    """Deterministic per-row seed. SHA-256 of the composite key, first 8
    hex bytes → int with the sign bit cleared (same convention as
    ``scorer.rerun.fresh_seed_for``)."""
    composite = f"{request_id}|{backbone}|{seed_index}".encode("utf-8")
    sha = hashlib.sha256(composite).hexdigest()
    return fresh_seed_for(sha)


def _expand_rows(spec: dict[str, Any]) -> list[dict[str, str]]:
    """Cross-product spec.backbones × range(spec.seeds) → list of row dicts.

    Every row carries the same receptor / species / state_claim / partner
    metadata; only backbone + seed_index vary. Empty ``pre_check_status``
    at this stage — set by ``run_pre_checks_on_rows`` next.
    """
    receptor_slug = _canonicalise_receptor(spec["receptor"])
    request_id = spec["request_id"]
    state_claim = spec["state_claim"]
    species = spec["species"].strip().lower()
    partner = spec["partner"] or {}
    partner_type = (partner.get("type") or "").strip()
    partner_identity = (partner.get("identity") or "").strip()
    perturbation = spec["partner_perturbation"]
    ligand = spec.get("ligand") or {"type": LigandType.NONE.value}
    ligand_type = (ligand.get("type") or LigandType.NONE.value).strip()
    ligand_sequence = (ligand.get("sequence") or "").strip()
    ligand_smiles = (ligand.get("smiles") or "").strip()
    samples_per_seed = int(spec.get("samples_per_seed") or 1)

    rows: list[dict[str, str]] = []
    for bb in spec["backbones"]:
        for i in range(spec["seeds"]):
            seed = _derive_row_seed(request_id, bb, i)
            row = {c: "" for c in PROPOSE_MANIFEST_COLUMNS}
            # rerun_manifest-compatible columns (populated where meaningful)
            row["prediction_path"] = ""      # not yet materialised (Layer 3)
            row["prediction_sha"] = ""
            row["experiment_slug"] = request_id
            row["wave_group"] = request_id
            row["branch"] = "propose"
            row["tier"] = ""
            row["backbone"] = bb
            row["receptor_from_path_substring"] = receptor_slug
            row["receptor_resolved"] = receptor_slug
            row["disambig_conflict"] = "false"
            row["receptor_unresolved_in_original"] = "false"
            row["expected_control_json"] = ""
            row["new_seed"] = str(seed)
            # propose-specific columns
            row["request_id"] = request_id
            row["seed_index"] = str(i)
            row["state_claim"] = state_claim
            row["species"] = species
            row["partner_type"] = partner_type
            row["partner_identity"] = partner_identity
            row["partner_perturbation"] = perturbation
            row["receptor_class"] = RECEPTOR_CLASS.get(receptor_slug, "")
            row["pre_check_status"] = ""
            row["pre_check_details_json"] = ""
            # Exp-Layer 1 — seed + ligand context propagated per row
            row["seed_used"] = str(seed)
            row["ligand_type"] = ligand_type
            row["ligand_sequence"] = ligand_sequence
            row["ligand_smiles"] = ligand_smiles
            # Diversity-study add-on — samples-per-seed multiplier
            row["samples_per_seed"] = str(samples_per_seed)
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Run pre-checks over the row set
# ---------------------------------------------------------------------------


def run_pre_checks(
    spec: dict[str, Any],
    rows: list[dict[str, str]],
    api: Api,
    ref_species_map: dict[str, set[str]],
) -> list[dict[str, str]]:
    """Populate ``pre_check_status`` and ``pre_check_details_json`` on every
    row. The five checks are deterministic in ``(receptor_slug, species,
    fasta_seq, partner_perturbation)`` — all identical across a spec's
    rows — so we run them once and stamp the result on every row.

    Returns the same list of rows, mutated in-place.
    """
    receptor_slug = _canonicalise_receptor(spec["receptor"])
    species = spec["species"].strip().lower()
    perturbation = spec["partner_perturbation"]

    # Optional receptor override; otherwise fetch WT
    receptor_seq = (spec.get("receptor_sequence_fasta") or "").strip()
    if not receptor_seq:
        receptor_seq = _wt_receptor_fasta(receptor_slug, api)

    results = run_all_checks(
        receptor_slug=receptor_slug,
        species=species,
        fasta_seq=receptor_seq,
        partner_perturbation=perturbation,
        ref_species_map=ref_species_map,
        api=api,
    )
    status = summarise(results)
    details_json = json.dumps(
        {k: list(v) for k, v in results.items()},
        separators=(",", ":"),
    )
    for row in rows:
        row["pre_check_status"] = status
        row["pre_check_details_json"] = details_json
    return rows


# ---------------------------------------------------------------------------
# Materialise on-disk input files (Layer 3)
# ---------------------------------------------------------------------------


def materialise_inputs(
    spec: dict[str, Any],
    rows: list[dict[str, str]],
    output_root: Path,
    api: Api,
) -> None:
    """Write per-row input files to ``<output_root>/<request_id>/inputs/<backbone>/<row_index>.<ext>``,
    stamp ``prediction_sha`` (= input-file SHA-256) and ``prediction_path``
    (= where the fold model WILL write output) onto every row.

    Byte-identical across runs of the same spec: templater output is a
    pure function of (rseq, pseq, seed_composite), and both sequences are
    resolved deterministically from the spec + GPCRdb cache.

    Also copies the source YAML to ``<output_root>/<request_id>/spec.yaml``
    for downstream provenance.
    """
    request_id = spec["request_id"]
    request_dir = output_root / request_id
    inputs_dir = request_dir / "inputs"
    request_dir.mkdir(parents=True, exist_ok=True)

    # Resolve sequences ONCE per spec (identical across rows)
    receptor_slug = _canonicalise_receptor(spec["receptor"])
    receptor_seq = (spec.get("receptor_sequence_fasta") or "").strip()
    if not receptor_seq:
        receptor_seq = _wt_receptor_fasta(receptor_slug, api)
    if not receptor_seq:
        raise SpecError(
            f"could not resolve receptor sequence for {receptor_slug!r}. "
            f"Either the slug is unknown or GPCRdb is unreachable. To "
            f"provide the sequence yourself, add "
            f"`receptor_sequence_fasta: '...'` to the spec."
        )

    partner_block = spec.get("partner") or {}
    partner_type = (partner_block.get("type") or "").strip()
    partner_identity = (partner_block.get("identity") or "").strip()
    apo = _partner_is_apo(partner_type, partner_identity)
    if _partner_is_small_molecule(partner_type):
        # Small-molecule ligand partners require SMILES / CCD code — not
        # extractable from a name alone. Layer 3 supports protein/peptide
        # partners; small-molecule support is deferred.
        raise SpecError(
            f"partner.type {partner_type!r} (small molecule) is not "
            f"supported by Layer 3 input materialisation. Provide a "
            f"protein/peptide partner, or edit the spec to describe "
            f"the ligand's SMILES/CCD once Layer 3+ lands SMILES support."
        )

    partner_seq = ""
    if not apo:
        partner_seq = (partner_block.get("sequence_fasta") or "").strip()
        if not partner_seq:
            partner_seq = _partner_fasta(partner_identity)
        if not partner_seq:
            raise SpecError(
                f"could not resolve partner sequence for identity "
                f"{partner_identity!r}. Either add the entry to "
                f"docs/EXPERIMENT_CATALOG/sequences/partners.fasta or inline "
                f"it in the spec as partner.sequence_fasta."
            )

    # Copy spec.yaml alongside the manifest for provenance
    spec_dest = request_dir / "spec.yaml"
    if not spec_dest.exists():
        spec_dest.write_text(yaml.safe_dump(spec, sort_keys=False))

    # Write per-row input files (deterministic; idempotent)
    for i, row in enumerate(rows):
        backbone = row["backbone"]
        ext = _BACKBONE_EXT[backbone]
        input_dir = inputs_dir / backbone
        input_dir.mkdir(parents=True, exist_ok=True)
        input_path = input_dir / f"{i:04d}.{ext}"
        content = _row_input_content(backbone, row, receptor_seq, partner_seq, apo)
        input_path.write_text(content)
        input_sha = content_sha256(input_path)
        # Manifest field naming:
        #   input_path   — where WE wrote the fold-model input file
        #   input_sha    — SHA-256 of that input file (change-detection key)
        #   prediction_path — where the fold model WILL write its output
        #                     (the row's primary key for the scorer's join)
        #   prediction_sha  — SHA of the fold-model OUTPUT; empty at
        #                     propose time (no prediction exists yet)
        sha12 = input_sha[:12]
        seed = row["new_seed"]
        out_leaf = _BACKBONE_OUTPUT_LEAF[backbone]
        row["input_path"] = str(input_path)
        row["input_sha"] = input_sha
        row["prediction_path"] = str(
            output_root / request_id / sha12 / backbone / f"seed_{seed}" / out_leaf
        )
        row["prediction_sha"] = ""     # no output file yet


# ---------------------------------------------------------------------------
# Summary line
# ---------------------------------------------------------------------------


def format_summary(rows: list[dict[str, str]]) -> str:
    """Return one-line summary: 'N rows: K pass, W warn (breakdown)'."""
    n = len(rows)
    counts = Counter(r["pre_check_status"] for r in rows)
    passes = counts.get("pass", 0)
    warns = n - passes
    parts = [f"pass={passes}"]
    for k, c in sorted(counts.items()):
        if k != "pass":
            parts.append(f"{k}={c}")
    return f"{n} rows: " + ", ".join(parts)


def format_matrix(rows: list[dict[str, str]]) -> str:
    """Render the per-row PASS/WARN matrix for --pre-check-only mode.

    One line per row: backbone × seed_index → summarised status.
    """
    lines = [f"{'backbone':<10} {'seed_index':<10} {'seed':<12} status"]
    for r in rows:
        lines.append(
            f"{r['backbone']:<10} {r['seed_index']:<10} {r['new_seed']:<12} {r['pre_check_status']}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-propose",
        description="Pre-flight acceptance gate + manifest emitter for new prediction proposals.",
    )
    p.add_argument("--spec", required=True, type=Path,
                   help="path to the proposal YAML")
    p.add_argument("--out", type=Path, default=None,
                   help="path to write the manifest CSV. Default: alongside spec, "
                        "with .manifest.csv extension.")
    p.add_argument("--pre-check-only", action="store_true",
                   help="run pre-checks and print the per-row matrix; do not "
                        "emit a manifest CSV or materialise input files")
    p.add_argument("--materialise", dest="materialise",
                   action="store_true", default=None,
                   help="write per-row input files to the output_root. Default "
                        "when --out is set. --pre-check-only implies no.")
    p.add_argument("--no-materialise", dest="materialise", action="store_false",
                   help="skip on-disk input-file materialisation; manifest "
                        "columns input_path/input_sha remain empty")
    p.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT,
                   help=f"root directory for materialised inputs (default: "
                        f"{DEFAULT_OUTPUT_ROOT}). Each request lands at "
                        f"<output_root>/<request_id>/inputs/<backbone>/...")
    p.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR,
                   help=f"GPCRdb Api cache directory (default: {DEFAULT_CACHE_DIR})")
    p.add_argument("--ref-set", type=Path, default=REF_SET_CSV,
                   help=f"reference_set.csv path (default: {REF_SET_CSV})")
    return p


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Never refuses a spec — exit 0 regardless of
    pre-check warnings. Non-zero exit is reserved for hard errors
    (SpecError, missing files, YAML parse failure)."""
    args = _build_parser().parse_args(argv)

    try:
        spec = load_spec(args.spec)
    except SpecError as e:
        print(f"gpcr-propose: {e}", file=sys.stderr)
        return 2

    # Warn (do not fail) if the receptor doesn't resolve — PC1 will surface it
    receptor_slug = _canonicalise_receptor(spec["receptor"])
    if receptor_slug not in KNOWN_RECEPTORS:
        print(
            f"gpcr-propose: receptor {receptor_slug!r} not in KNOWN_RECEPTORS; "
            f"PC1 will warn on every row. Continuing anyway.",
            file=sys.stderr,
        )

    api = Api(cache_dir=args.cache_dir)
    ref_species_map = load_ref_species_map(args.ref_set)
    rows = _expand_rows(spec)
    run_pre_checks(spec, rows, api, ref_species_map)

    summary = format_summary(rows)
    print(summary)

    if args.pre_check_only:
        print()
        print(format_matrix(rows))
        return 0

    # Materialisation: default ON when we're emitting a manifest, unless
    # explicitly disabled with --no-materialise. --pre-check-only already
    # returned above.
    do_materialise = args.materialise
    if do_materialise is None:
        do_materialise = True
    if do_materialise:
        try:
            materialise_inputs(spec, rows, args.output_root, api)
        except SpecError as e:
            print(f"gpcr-propose: {e}", file=sys.stderr)
            return 2
        print(f"materialised {len(rows)} input file(s) under "
              f"{args.output_root / spec['request_id']}/inputs/")

    out = args.out
    if out is None:
        out = args.spec.with_suffix(".manifest.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(PROPOSE_MANIFEST_COLUMNS))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
