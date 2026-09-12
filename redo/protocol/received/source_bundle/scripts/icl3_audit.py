"""Audit ICL3 modeling status of every reference structure in the 40-receptor
Class A panel.

Panel-wide extension of the DRD2 forensics (docs/AUDIT_TRAIL.md #1 offset-137 +
docs/BLOCK_A_DRD2_MSA_FORENSICS_2026_09_01.md #C):

- DRD2 inactive (6CM4) replaces UniProt residues 223-362 with T4L (P00720).
- DRD2 active  (7JVR) leaves UniProt residues 226-364 disordered (unmodeled).

Both are ICL3-mode failures at the reference level. If a meaningful fraction of
the 40 inactive references have ICL3 removed, every `receptor_midpoint` in
`refs/reference_set.csv` carries a systematically shifted inactive anchor.

For every row of `refs/reference_set.csv` in the 40-receptor panel this
script derives four new columns:

    icl3_status                — full-length / partially-excised /
                                 fully-excised / replaced-with-fusion /
                                 disordered-not-modeled
    icl3_residues_missing      — comma-separated UniProt residues absent
                                 from crystal within canonical ICL3
    icl3_residues_missing_count — integer count
    fusion_partner             — T4L / BRIL / rubredoxin / flavodoxin /
                                 mini_Gs / nanobody / scFv / (empty)
    fusion_partner_insertion_range — comma-separated UniProt residues
                                     replaced by fusion (if in same
                                     entity as receptor)

Idempotent: rows already carrying these columns non-empty are skipped
(and preserved).

Usage:
    python -m scripts.icl3_audit \
        --reference-set refs/reference_set.csv \
        --coupling-csv  refs/gpcr_coupling.csv \
        --rcsb-cache    refs/cache/rcsb \
        --gpcrdb-cache  refs/cache/gpcrdb \
        --output-summary refs/icl3_audit_summary.json
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# UniProt fusion signature table
# ---------------------------------------------------------------------------

# Fusion partners commonly used in Class A GPCR crystallography.
# When an entity carries the receptor UniProt AND one of these, the residues
# not covered by the receptor's own alignment blocks are the fusion insertion.
FUSION_UNIPROT: dict[str, str] = {
    "P00720": "T4L",         # T4 phage lysozyme (Endolysin)
    "P0ABE7": "BRIL",        # Cytochrome b562 (E. coli) -- BRIL is a b562RIL variant
    "P0ABE9": "BRIL",        # Cytochrome b562 alternate id
    "P00268": "rubredoxin",  # Rubredoxin (Clostridium pasteurianum)
    "P00322": "flavodoxin",  # Flavodoxin (Desulfovibrio vulgaris)
    # Engineered mini-Gα scaffolds:
    "P63092": "mini_Gs",     # G(s) alpha subunit
    "P08754": "mini_Gi",     # G(i) alpha-1
    "P04898": "mini_Gi",     # G(i) alpha-2
    "P50148": "mini_Gq",     # G(q) alpha
    # Nanobody / scFv Fv fragments do not have canonical UniProt IDs;
    # detection falls through to stabilising_elements column.
}

# Additional sequence signatures for when RCSB has not annotated the fusion
# UniProt but the amino acid sequence contains a canonical fusion prefix.
FUSION_SIGNATURES: list[tuple[str, str]] = [
    ("T4L",         "MNIFEMLRIDEGLRLKIYKD"),
    ("T4L",         "NIFEMLRIDEGLRLKIYKD"),        # missing Met, common in crystal constructs
    ("BRIL",        "MADLEDNWETLNDNLKVIEKADNAA"),
    ("BRIL",        "ADLEDNWETLNDNLKVIEKADNAA"),   # missing Met
    ("rubredoxin",  "MKKYVCTVCGYIYD"),
    ("flavodoxin",  "AKIGLFYGTQTGVTQTIAESI"),      # canonical flavodoxin core
]


# ---------------------------------------------------------------------------
# RCSB / GPCRdb fetching (with on-disk cache)
# ---------------------------------------------------------------------------


def _http_get_json(url: str, cache_path: Path, sleep: float = 0.15) -> Optional[dict]:
    """Fetch JSON from a URL, caching under cache_path. Returns None on 404."""
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        time.sleep(sleep)
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    d = json.loads(data.decode("utf-8"))
    cache_path.write_bytes(data)
    return d


def fetch_rcsb_entry(pdb_id: str, rcsb_cache: Path) -> Optional[dict]:
    return _http_get_json(
        f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}",
        rcsb_cache / f"{pdb_id.upper()}_entry.json",
    )


def fetch_rcsb_entity(pdb_id: str, entity_id: str, rcsb_cache: Path) -> Optional[dict]:
    return _http_get_json(
        f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}",
        rcsb_cache / f"{pdb_id.upper()}_ent{entity_id}.json",
    )


def fetch_gpcrdb_protein(entry_name: str, gpcrdb_cache: Path) -> Optional[dict]:
    return _http_get_json(
        f"https://gpcrdb.org/services/protein/{entry_name.lower()}/",
        gpcrdb_cache / f"protein_{entry_name.lower()}.json",
    )


def fetch_gpcrdb_residues_ext(entry_name: str, gpcrdb_cache: Path) -> Optional[list]:
    d = _http_get_json(
        f"https://gpcrdb.org/services/residues/extended/{entry_name.lower()}/",
        gpcrdb_cache / f"residues_ext_{entry_name.lower()}.json",
    )
    return d if isinstance(d, list) else None


# ---------------------------------------------------------------------------
# ICL3 boundary derivation from GPCRdb residues
# ---------------------------------------------------------------------------


def canonical_icl3_range(residues_ext: list[dict]) -> tuple[Optional[int], Optional[int], set[int]]:
    """Return (icl3_min, icl3_max, set_of_icl3_uniprot_residues).

    GPCRdb protein_segment == 'ICL3' between TM5 and TM6. Sequence numbers
    are the receptor's UniProt canonical numbering.
    """
    positions = sorted(
        r["sequence_number"]
        for r in residues_ext
        if r.get("protein_segment") == "ICL3"
    )
    if not positions:
        return None, None, set()
    return positions[0], positions[-1], set(positions)


def segment_bounds(residues_ext: list[dict]) -> dict[str, tuple[int, int]]:
    """Return {segment: (min, max)}."""
    d: dict[str, list[int]] = defaultdict(list)
    for r in residues_ext:
        seg = r.get("protein_segment")
        if seg:
            d[seg].append(r["sequence_number"])
    return {seg: (min(v), max(v)) for seg, v in d.items()}


# ---------------------------------------------------------------------------
# Receptor-entity identification
# ---------------------------------------------------------------------------


def _is_seven_tm_entity(entity_json: dict) -> bool:
    for a in entity_json.get("rcsb_polymer_entity_annotation", []) or []:
        name = (a.get("name") or "").lower()
        if any(
            key in name
            for key in (
                "7 transmembrane",
                "7tm",
                "rhodopsin",
                "g-protein coupled receptor",
                "g protein-coupled receptor",
                "g-protein-coupled receptor",
                "gpcr",
            )
        ):
            return True
    return False


def find_receptor_entity(
    pdb_id: str,
    entity_ids: list[str],
    receptor_uniprot: str,
    receptor_sequence: str,
    rcsb_cache: Path,
) -> Optional[tuple[str, dict, str]]:
    """Return (entity_id, entity_json, matched_uniprot) for the entity that
    carries the receptor.

    Match priority:
      1. Entity whose ``uniprot_ids`` include ``receptor_uniprot``, largest
         alignment coverage first.
      2. Fallback: entity annotated as a 7TM receptor via Pfam
         (``rcsb_polymer_entity_annotation`` name containing "7 transmembrane"
         / "7tm" / "rhodopsin"), sequence-substring-matched to the receptor
         canonical sequence (~≥30-residue TM signature). Returned
         ``matched_uniprot`` is the receptor's canonical UniProt accession.
    """
    # First pass: strict UniProt match.
    best: Optional[tuple[str, dict, int]] = None
    for eid in entity_ids:
        e = fetch_rcsb_entity(pdb_id, eid, rcsb_cache)
        if e is None:
            continue
        cids = e.get("rcsb_polymer_entity_container_identifiers", {}) or {}
        ups = cids.get("uniprot_ids") or []
        if receptor_uniprot not in ups:
            continue
        cov = 0
        for a in e.get("rcsb_polymer_entity_align", []) or []:
            if a.get("reference_database_accession") == receptor_uniprot:
                for reg in a.get("aligned_regions", []) or []:
                    cov += int(reg.get("length") or 0)
        if best is None or cov > best[2]:
            best = (eid, e, cov)
    if best is not None:
        return best[0], best[1], receptor_uniprot

    # Second pass: 7TM Pfam-annotated entity whose sequence overlaps the
    # receptor's canonical sequence.
    canonical = (receptor_sequence or "").upper().replace("\n", "").strip()
    for eid in entity_ids:
        e = fetch_rcsb_entity(pdb_id, eid, rcsb_cache)
        if e is None:
            continue
        if not _is_seven_tm_entity(e):
            continue
        seq = ((e.get("entity_poly", {}) or {}).get("pdbx_seq_one_letter_code_can") or "")
        seq = seq.upper().replace("\n", "").strip()
        if not seq or not canonical:
            continue
        # look for a ≥30-residue exact substring from canonical inside entity seq
        found = False
        for pos in range(0, len(canonical) - 30, 30):
            probe = canonical[pos:pos + 40]
            if probe in seq:
                found = True
                break
        if found:
            return eid, e, receptor_uniprot
    return None


# ---------------------------------------------------------------------------
# ICL3 status derivation from a receptor entity
# ---------------------------------------------------------------------------


def receptor_coverage(
    entity_json: dict,
    receptor_uniprot: str,
    canonical_sequence: str = "",
) -> tuple[set[int], list[tuple[int, int, int, int]]]:
    """Return (uniprot_positions_covered, list_of_(uniprot_beg, uniprot_end, entity_beg, entity_end)).

    Primary path: use ``rcsb_polymer_entity_align`` entries whose
    ``reference_database_accession`` is ``receptor_uniprot``. Each region
    contributes a block ``(ref_beg, ref_end, entity_beg, entity_end)``.

    Fallback (when the deposition names the receptor under a chimera or
    non-canonical UniProt accession that we did not match): pass the receptor's
    canonical UniProt sequence and reconstruct blocks via
    ``difflib.SequenceMatcher`` matching of the entity sequence against the
    canonical sequence. Matching blocks give the (ref_beg, entity_beg, length)
    triple the same way an RCSB alignment would.
    """
    covered: set[int] = set()
    blocks: list[tuple[int, int, int, int]] = []
    for a in entity_json.get("rcsb_polymer_entity_align", []) or []:
        if a.get("reference_database_accession") != receptor_uniprot:
            continue
        for reg in a.get("aligned_regions", []) or []:
            beg = int(reg["ref_beg_seq_id"])
            length = int(reg["length"])
            end = beg + length - 1
            ebeg = int(reg["entity_beg_seq_id"])
            eend = ebeg + length - 1
            covered.update(range(beg, end + 1))
            blocks.append((beg, end, ebeg, eend))
    if covered:
        return covered, blocks

    # Fallback: sequence-match entity vs canonical.
    canonical = (canonical_sequence or "").upper().replace("\n", "").strip()
    entity_seq = ((entity_json.get("entity_poly", {}) or {}).get("pdbx_seq_one_letter_code_can") or "")
    entity_seq = entity_seq.upper().replace("\n", "").strip()
    if not canonical or not entity_seq:
        return covered, blocks
    from difflib import SequenceMatcher
    sm = SequenceMatcher(None, canonical, entity_seq, autojunk=False)
    for m in sm.get_matching_blocks():
        if m.size < 8:
            continue
        ref_beg = m.a + 1  # 1-based UniProt
        ent_beg = m.b + 1  # 1-based entity
        ref_end = ref_beg + m.size - 1
        ent_end = ent_beg + m.size - 1
        blocks.append((ref_beg, ref_end, ent_beg, ent_end))
        covered.update(range(ref_beg, ref_end + 1))
    return covered, blocks


def detect_fusion_in_entity(entity_json: dict, receptor_uniprot: str) -> tuple[Optional[str], list[tuple[int, int]]]:
    """Return (fusion_partner_name, list_of_(entity_beg, entity_end)) for
    fusion insertions in the *same* entity as the receptor.
    """
    cids = entity_json.get("rcsb_polymer_entity_container_identifiers", {}) or {}
    ups = cids.get("uniprot_ids") or []
    fusion_up = None
    fusion_name = None
    for up in ups:
        if up == receptor_uniprot:
            continue
        if up in FUSION_UNIPROT:
            fusion_up = up
            fusion_name = FUSION_UNIPROT[up]
            break
    # If no UniProt annotation, try sequence signature.
    if fusion_name is None:
        seq = (entity_json.get("entity_poly", {}) or {}).get("pdbx_seq_one_letter_code_can") or ""
        if seq:
            for name, sig in FUSION_SIGNATURES:
                if sig in seq:
                    fusion_name = name
                    break
    if fusion_name is None:
        return None, []

    # Entity blocks (entity coordinates) for this fusion, if annotated by UniProt.
    fusion_blocks: list[tuple[int, int]] = []
    if fusion_up is not None:
        for a in entity_json.get("rcsb_polymer_entity_align", []) or []:
            if a.get("reference_database_accession") == fusion_up:
                for reg in a.get("aligned_regions", []) or []:
                    ebeg = int(reg["entity_beg_seq_id"])
                    eend = ebeg + int(reg["length"]) - 1
                    fusion_blocks.append((ebeg, eend))
    return fusion_name, fusion_blocks


def map_entity_to_uniprot(entity_pos: int, blocks: list[tuple[int, int, int, int]]) -> Optional[int]:
    """Return UniProt residue for an entity position, or None if unmapped."""
    for ubeg, uend, ebeg, eend in blocks:
        if ebeg <= entity_pos <= eend:
            return ubeg + (entity_pos - ebeg)
    return None


def flanking_uniprot_range_for_entity_block(
    entity_beg: int,
    entity_end: int,
    blocks: list[tuple[int, int, int, int]],
) -> tuple[Optional[int], Optional[int]]:
    """The UniProt residues immediately flanking a fusion insertion (which
    lives between receptor blocks in entity space)."""
    left_ubeg = None
    right_uend = None
    for ubeg, uend, ebeg, eend in sorted(blocks, key=lambda b: b[2]):
        if eend < entity_beg:
            left_ubeg = uend  # last receptor position before the fusion
        if ebeg > entity_end and right_uend is None:
            right_uend = ubeg  # first receptor position after the fusion
    return left_ubeg, right_uend


# ---------------------------------------------------------------------------
# Auxiliary: fusion detection across ALL entities (BRIL/scFv/mini-G as
# separate chain).
# ---------------------------------------------------------------------------


def entity_fusion_partners_all(entity_id: str, entity_json: dict, receptor_uniprot: str) -> list[str]:
    """List fusion-partner names present on this entity.

    Considers both UniProt annotations and (when unannotated) sequence
    signatures.
    """
    names: list[str] = []
    cids = entity_json.get("rcsb_polymer_entity_container_identifiers", {}) or {}
    ups = cids.get("uniprot_ids") or []
    for up in ups:
        if up == receptor_uniprot:
            continue
        if up in FUSION_UNIPROT:
            names.append(FUSION_UNIPROT[up])
    # Sequence signature (only meaningful if no receptor annotation, else double-counts).
    seq = (entity_json.get("entity_poly", {}) or {}).get("pdbx_seq_one_letter_code_can") or ""
    for name, sig in FUSION_SIGNATURES:
        if sig in seq and name not in names:
            names.append(name)
    return names


def detect_scaffold_stabilisers(pdb_id: str, entity_ids: list[str], receptor_uniprot: str, rcsb_cache: Path) -> list[str]:
    """Detect non-receptor stabilisers across all entities of the assembly.

    - fusion partners on the receptor entity (T4L, BRIL, ...) — reported here
      even though also picked up by detect_fusion_in_entity for row context.
    - fusion partners on OTHER entities (BRIL as separate chain, mini-Gs, ...).
    - nanobody / scFv (by description keywords, since no UniProt).
    """
    names: list[str] = []
    for eid in entity_ids:
        e = fetch_rcsb_entity(pdb_id, eid, rcsb_cache)
        if e is None:
            continue
        names.extend(entity_fusion_partners_all(eid, e, receptor_uniprot))
        # keyword-based detection for scFv / nanobody
        desc = ((e.get("rcsb_polymer_entity", {}) or {}).get("pdbx_description") or "").lower()
        if "scfv" in desc or "single-chain fv" in desc or "single chain fv" in desc:
            names.append("scFv")
        if "nanobody" in desc or "vhh" in desc or "camelid" in desc:
            names.append("nanobody")
        if "mini-g" in desc or "mini g" in desc or "minigalpha" in desc:
            if "mini_Gs" not in names and "mini_Gi" not in names and "mini_Gq" not in names:
                names.append("mini_G")
    # dedupe preserving order
    seen = set()
    out = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


# ---------------------------------------------------------------------------
# Disordered-residue detection: polymer_entity_instance features
# ---------------------------------------------------------------------------


def fetch_rcsb_instance(pdb_id: str, asym_id: str, rcsb_cache: Path) -> Optional[dict]:
    return _http_get_json(
        f"https://data.rcsb.org/rest/v1/core/polymer_entity_instance/{pdb_id}/{asym_id}",
        rcsb_cache / f"{pdb_id.upper()}_inst{asym_id}.json",
    )


def observed_entity_positions_from_instance(inst_json: dict) -> Optional[set[int]]:
    """Return the set of entity_poly_seq positions OBSERVED in this chain.

    RCSB's `auth_to_entity_poly_seq_mapping` includes an author-assigned ID
    for every entity position — even unobserved ones (which still have a
    scheme-assigned number, sometimes negative for fusion tails). So the
    reliable source of truth is the ``UNOBSERVED_RESIDUE_XYZ`` feature: its
    ``feature_positions`` list ranges of unobserved entity_poly_seq indices.
    Observed = full-length minus unobserved.
    """
    ci = inst_json.get("rcsb_polymer_entity_instance_container_identifiers", {}) or {}
    mapping = ci.get("auth_to_entity_poly_seq_mapping")
    if not isinstance(mapping, list):
        return None
    total = len(mapping)
    if total == 0:
        return None
    unobserved: set[int] = set()
    for f in inst_json.get("rcsb_polymer_instance_feature", []) or []:
        if (f.get("type") or "") != "UNOBSERVED_RESIDUE_XYZ":
            continue
        for p in f.get("feature_positions", []) or []:
            beg = p.get("beg_seq_id")
            end = p.get("end_seq_id") or beg
            if beg is None:
                continue
            unobserved.update(range(int(beg), int(end) + 1))
    return set(range(1, total + 1)) - unobserved


def find_receptor_asym_id(
    pdb_id: str, entity_id: str, entity_json: dict, rcsb_cache: Path,
) -> Optional[str]:
    """Return an asym_id chain for the receptor entity.

    Uses the entity's own ``rcsb_polymer_entity_container_identifiers.asym_ids``
    when present; falls back to probing common letters.
    """
    cids = entity_json.get("rcsb_polymer_entity_container_identifiers", {}) or {}
    asyms = cids.get("asym_ids") or []
    for cand in asyms:
        inst = fetch_rcsb_instance(pdb_id, cand, rcsb_cache)
        if inst is not None:
            return cand
    for cand in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        inst = fetch_rcsb_instance(pdb_id, cand, rcsb_cache)
        if inst is None:
            continue
        ci = inst.get("rcsb_polymer_entity_instance_container_identifiers", {}) or {}
        if str(ci.get("entity_id") or "") == str(entity_id):
            return cand
    return None


# ---------------------------------------------------------------------------
# Main row-level classification
# ---------------------------------------------------------------------------


def classify_row(
    pdb_id: str,
    receptor_uniprot: str,
    icl3_positions: set[int],
    icl3_range: tuple[int, int],
    rcsb_cache: Path,
    canonical_sequence: str = "",
) -> dict[str, Any]:
    """Return a dict of icl3_* + fusion_* fields for a single (pdb, receptor)."""
    result: dict[str, Any] = {
        "icl3_status": "",
        "icl3_residues_missing": "",
        "icl3_residues_missing_count": 0,
        "fusion_partner": "",
        "fusion_partner_insertion_range": "",
        "note": "",
    }
    entry = fetch_rcsb_entry(pdb_id, rcsb_cache)
    if entry is None:
        result["icl3_status"] = "unknown-rcsb-fetch-failed"
        result["note"] = f"RCSB entry not found for {pdb_id}"
        return result
    ci = entry.get("rcsb_entry_container_identifiers", {}) or {}
    entity_ids = ci.get("polymer_entity_ids") or []
    if not entity_ids:
        result["icl3_status"] = "unknown-no-polymer-entities"
        result["note"] = f"no polymer_entity_ids in {pdb_id}"
        return result

    hit = find_receptor_entity(pdb_id, entity_ids, receptor_uniprot, canonical_sequence, rcsb_cache)
    if hit is None:
        result["icl3_status"] = "unknown-receptor-entity-not-identified"
        result["note"] = f"receptor UniProt {receptor_uniprot} not found in any entity of {pdb_id}"
        return result
    receptor_entity_id, receptor_entity, matched_uniprot = hit

    covered_uniprot, blocks = receptor_coverage(receptor_entity, matched_uniprot, canonical_sequence)
    fusion_name, fusion_blocks_entity = detect_fusion_in_entity(receptor_entity, receptor_uniprot)

    # Missing from construct = ICL3 positions not covered by any receptor
    # alignment block.
    missing_from_construct = sorted(icl3_positions - covered_uniprot)

    # Where present in construct, check whether the chain modeled them.
    disordered_within_icl3: list[int] = []
    icl3_positions_in_construct = sorted(icl3_positions & covered_uniprot)
    if icl3_positions_in_construct:
        asym = find_receptor_asym_id(pdb_id, receptor_entity_id, receptor_entity, rcsb_cache)
        if asym is not None:
            inst = fetch_rcsb_instance(pdb_id, asym, rcsb_cache)
            if inst is not None:
                observed = observed_entity_positions_from_instance(inst)
                if observed is not None:
                    for up in icl3_positions_in_construct:
                        # UniProt -> entity position via inverse of blocks
                        entity_pos = None
                        for ubeg, uend, ebeg, eend in blocks:
                            if ubeg <= up <= uend:
                                entity_pos = ebeg + (up - ubeg)
                                break
                        if entity_pos is not None and entity_pos not in observed:
                            disordered_within_icl3.append(up)

    all_missing = sorted(set(missing_from_construct) | set(disordered_within_icl3))
    result["icl3_residues_missing"] = ",".join(str(x) for x in all_missing)
    result["icl3_residues_missing_count"] = len(all_missing)

    # Fusion insertion range: if there is an actual fusion IN THIS ENTITY, map
    # its entity block(s) to the flanking UniProt residues. When the fusion
    # partner is annotated as a distinct UniProt on the same entity, we can
    # infer the range precisely; when it was only found via sequence signature
    # (no partner UniProt), the fusion inserted range is exactly the receptor's
    # own alignment gap (missing_from_construct).
    fusion_insertion_uniprot: list[int] = []
    if fusion_name is not None and fusion_blocks_entity:
        for ebeg, eend in fusion_blocks_entity:
            luend, ruend = flanking_uniprot_range_for_entity_block(ebeg, eend, blocks)
            if luend is not None and ruend is not None:
                if ruend > luend + 1:
                    fusion_insertion_uniprot.extend(range(luend + 1, ruend))
    if fusion_name is not None and not fusion_insertion_uniprot and missing_from_construct:
        # Signature-detected fusion or partner annotated under a T4L homolog
        # (e.g. 6PS2 D9IEF7): treat the receptor's own alignment gap as the
        # fusion insertion range.
        fusion_insertion_uniprot = list(missing_from_construct)

    # Look at ALL entities for context (mini-Gs / BRIL as separate chain,
    # nanobody, scFv, and any missed same-entity fusion). Use the union to
    # pick the most-informative fusion_partner name for reporting.
    all_partners = detect_scaffold_stabilisers(pdb_id, entity_ids, receptor_uniprot, rcsb_cache)
    if fusion_name is not None and fusion_name not in all_partners:
        all_partners.insert(0, fusion_name)
    # Prefer T4L/BRIL/rubredoxin/flavodoxin > mini_G* > nanobody/scFv
    prio = {"T4L": 0, "BRIL": 1, "rubredoxin": 2, "flavodoxin": 3,
            "mini_Gs": 4, "mini_Gi": 4, "mini_Gq": 4, "mini_G": 5,
            "nanobody": 6, "scFv": 7}
    if all_partners:
        fusion_name = sorted(all_partners, key=lambda n: prio.get(n, 99))[0]

    if fusion_insertion_uniprot:
        fusion_insertion_uniprot = sorted(set(int(x) for x in fusion_insertion_uniprot))
        result["fusion_partner_insertion_range"] = ",".join(str(x) for x in fusion_insertion_uniprot)
    result["fusion_partner"] = fusion_name or ""

    # Classification
    icl3_len = max(1, len(icl3_positions))
    missing_frac = len(all_missing) / icl3_len

    if not icl3_positions:
        result["icl3_status"] = "unknown-no-canonical-icl3"
    elif missing_frac == 0:
        result["icl3_status"] = "full-length"
    elif missing_from_construct and fusion_insertion_uniprot:
        result["icl3_status"] = "replaced-with-fusion"
    elif missing_frac >= 0.75:
        # Nearly all ICL3 missing:
        if missing_from_construct:
            # If not fused in same entity but construct excises ICL3
            result["icl3_status"] = "fully-excised"
        else:
            result["icl3_status"] = "disordered-not-modeled"
    elif missing_from_construct:
        result["icl3_status"] = "partially-excised"
    else:
        result["icl3_status"] = "disordered-not-modeled"

    return result


# ---------------------------------------------------------------------------
# CSV augmentation driver
# ---------------------------------------------------------------------------


def augment(
    reference_set: Path,
    coupling_csv: Path,
    rcsb_cache: Path,
    gpcrdb_cache: Path,
    output: Optional[Path],
    summary_json: Optional[Path],
) -> dict[str, Any]:
    output = output or reference_set
    panel = {
        r["receptor_slug"].strip().upper()
        for r in csv.DictReader(coupling_csv.open())
        if r.get("receptor_slug")
    }

    rows: list[dict[str, str]] = []
    with reference_set.open() as f:
        reader = csv.DictReader(f)
        base_cols = list(reader.fieldnames or [])
        for r in reader:
            rows.append(dict(r))

    new_cols = [
        "icl3_status",
        "icl3_residues_missing",
        "icl3_residues_missing_count",
        "fusion_partner",
        "fusion_partner_insertion_range",
    ]
    for c in new_cols:
        if c not in base_cols:
            base_cols.append(c)

    per_receptor_cache_uniprot: dict[str, str] = {}
    per_receptor_cache_icl3: dict[str, tuple[int, int, set[int]]] = {}
    per_receptor_cache_sequence: dict[str, str] = {}

    summary: dict[str, Any] = {
        "rows_total": len(rows),
        "panel_rows_seen": 0,
        "panel_rows_processed": 0,
        "panel_rows_skipped_prefilled": 0,
        "failed": [],
        "records": [],
    }

    for row in rows:
        # ensure new columns present
        for c in new_cols:
            row.setdefault(c, "")

        receptor = (row.get("receptor_slug") or "").strip().upper()
        if receptor not in panel:
            continue
        summary["panel_rows_seen"] += 1

        # idempotence
        if row["icl3_status"] and row.get("icl3_residues_missing_count", "") != "":
            summary["panel_rows_skipped_prefilled"] += 1
            continue

        entry_name = (row.get("uniprot_slug") or "").strip().lower()
        pdb_id = (row.get("pdb_id") or "").strip().upper()
        role = (row.get("role") or "").strip()

        # UniProt accession from GPCRdb
        if entry_name in per_receptor_cache_uniprot:
            receptor_uniprot = per_receptor_cache_uniprot[entry_name]
            icl3_min, icl3_max, icl3_positions = per_receptor_cache_icl3[entry_name]
            canonical_sequence = per_receptor_cache_sequence[entry_name]
        else:
            prot = fetch_gpcrdb_protein(entry_name, gpcrdb_cache)
            if prot is None:
                summary["failed"].append({
                    "receptor": receptor, "role": role, "pdb_id": pdb_id,
                    "error": f"GPCRdb protein lookup failed for {entry_name}",
                })
                continue
            receptor_uniprot = prot.get("accession") or ""
            canonical_sequence = prot.get("sequence") or ""
            residues = fetch_gpcrdb_residues_ext(entry_name, gpcrdb_cache) or []
            icl3_min, icl3_max, icl3_positions = canonical_icl3_range(residues)
            per_receptor_cache_uniprot[entry_name] = receptor_uniprot
            per_receptor_cache_icl3[entry_name] = (icl3_min, icl3_max, icl3_positions)
            per_receptor_cache_sequence[entry_name] = canonical_sequence

        if not receptor_uniprot:
            summary["failed"].append({
                "receptor": receptor, "role": role, "pdb_id": pdb_id,
                "error": "no UniProt accession from GPCRdb",
            })
            continue

        try:
            res = classify_row(pdb_id, receptor_uniprot, icl3_positions,
                               (icl3_min, icl3_max), rcsb_cache,
                               canonical_sequence=canonical_sequence)
        except Exception as e:
            summary["failed"].append({
                "receptor": receptor, "role": role, "pdb_id": pdb_id,
                "error": f"{type(e).__name__}: {e}",
            })
            continue

        row["icl3_status"] = res["icl3_status"]
        row["icl3_residues_missing"] = res["icl3_residues_missing"]
        row["icl3_residues_missing_count"] = str(res["icl3_residues_missing_count"])
        row["fusion_partner"] = res["fusion_partner"]
        row["fusion_partner_insertion_range"] = res["fusion_partner_insertion_range"]

        summary["panel_rows_processed"] += 1
        rec = {
            "receptor": receptor, "role": role, "pdb_id": pdb_id,
            "uniprot": receptor_uniprot,
            "icl3_range": [icl3_min, icl3_max],
            "icl3_len": len(icl3_positions),
            **res,
        }
        summary["records"].append(rec)
        print(f"OK  {receptor:<8s} {role:<10s} {pdb_id}  "
              f"status={res['icl3_status']:<24s}  "
              f"missing={res['icl3_residues_missing_count']:>3d}/{len(icl3_positions):<3d}  "
              f"fusion={res['fusion_partner']}", flush=True)

    with output.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base_cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in base_cols})

    if summary_json is not None:
        summary_json.parent.mkdir(parents=True, exist_ok=True)
        summary_json.write_text(json.dumps(summary, indent=2, default=str))

    print(f"\nprocessed {summary['panel_rows_processed']} / seen {summary['panel_rows_seen']} panel rows; "
          f"pre-filled skipped {summary['panel_rows_skipped_prefilled']}; failed {len(summary['failed'])}",
          file=sys.stderr)
    for fail in summary["failed"]:
        print(f"  FAIL {fail['receptor']:<8s} {fail['role']:<10s} {fail['pdb_id']}  {fail['error']}", file=sys.stderr)

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-set", default=str(REPO / "refs" / "reference_set.csv"))
    ap.add_argument("--coupling-csv", default=str(REPO / "refs" / "gpcr_coupling.csv"))
    ap.add_argument("--rcsb-cache", default=str(REPO / "refs" / "cache" / "rcsb"))
    ap.add_argument("--gpcrdb-cache", default=str(REPO / "refs" / "cache" / "gpcrdb"))
    ap.add_argument("--output", default=None)
    ap.add_argument("--summary-json", default=str(REPO / "refs" / "icl3_audit_summary.json"))
    args = ap.parse_args(argv)

    summary = augment(
        reference_set=Path(args.reference_set),
        coupling_csv=Path(args.coupling_csv),
        rcsb_cache=Path(args.rcsb_cache),
        gpcrdb_cache=Path(args.gpcrdb_cache),
        output=Path(args.output) if args.output else None,
        summary_json=Path(args.summary_json) if args.summary_json else None,
    )
    return 0 if not summary["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
