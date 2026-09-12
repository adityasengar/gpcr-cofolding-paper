"""Post-load receipts — Block C Stage 0 Step 1.4, 2026-09-04.

Two named receipts distinct from the sequenced A1..A6 pre-scoring
assertions:

  - :func:`check_receptor_slug_populated` — asserts every row carries a
    non-empty, non-NaN-like ``receptor_slug``. Defence-in-depth against
    the OPSD / B1B1U5 chain-matcher regression shape earlier this
    campaign.
  - :func:`check_ligand_present` — asserts that any row whose manifest
    declared a ligand (``ligand_type in {"peptide","small_molecule"}``
    or ``ligand_smiles``/``ligand_sequence`` non-empty) has ≥ 95 % of
    the SMILES- (or sequence-)implied heavy-atom / residue count on
    some non-buffer HETATM residue (or non-receptor protein chain,
    for peptides) in the produced CIF. Guards against the Chai
    silent-apo shape (audit #10 analogue) AND the partial-tokenization
    shape the Tier 1 audit named — a nominally-populated ligand carrying
    1 atom instead of the expected 25. On RDKit-unavailable or SMILES-
    unparseable rows the check gracefully falls back to the legacy
    ≥ 1-HETATM rule with ``receipt_threshold_source`` stamped on the
    detail dict.

Both receipts raise a ``ScorerAssertionError`` subclass on failure. The
batch driver's single sanctioned catch site
(``scorer.orchestrator.score_and_capture``) records the failing
assertion class name on the row and returns ``passed=False`` — same
mechanism as A1..A6.

**Buffer/water exclusion list** reuses
``scorer.pocket_metrics.NON_LIGAND_RESNAMES`` (waters, metals, halides,
buffers, lipids, PEGs, additives). The set matches the pocket-metrics
reference-ligand scan so a molecule scored as "ligand" here matches
what pocket_metrics would score as "reference ligand" on the same
structure. CLR (cholesterol), GOL (glycerol), and OLA/OLC (oleic acid)
are on the exclusion list because they overwhelmingly appear as
crystallographic contaminants. None of Block C's Tier 1 panel (ADRB2,
AGTR1, 5HT1B, ADRB1, MRGPRX2, GLP1R, DRD3, HRH3, OX2R) uses these as
the pharmacology ligand — no false-quarantine risk on the current
panel. A future block whose real ligand is a lipid would need a
per-receptor allowlist.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import gemmi

from scorer.assertions import ALigandPresence, AReceptorSlugMissing
from scorer.pocket_metrics import NON_LIGAND_RESNAMES
from scorer.structure import STD_AA, one_letter

# ---------------------------------------------------------------------------
# Ligand-presence receipt
# ---------------------------------------------------------------------------

# ``ligand_type`` values that indicate "no ligand expected in the CIF"
# per scorer.schema.LigandType. Matches the propose-flow contract:
# apo == deliberately-empty ligand slot, none == pre-Exp-Layer-1 default.
_LIGAND_TYPES_NO_CHECK: frozenset[str] = frozenset({"", "none", "apo"})

# Fraction of the SMILES-derived (or sequence-derived) expected heavy-atom
# count that must be present in the produced CIF for the ligand-presence
# receipt to pass. Raised from the legacy ≥1-HETATM rule as part of the
# post-Tier-3 Stage 0 gate (plan §Stage 0 item 4, 2026-09-06) to catch
# partial-tokenization silent failures that Tier 1 audit named — a
# nominally-populated ligand chain carrying 1 atom instead of the
# expected 25 previously passed. Threshold is deliberately loose (5 %
# tolerance) so a heavy-hydrogen add on the CIF or an RDKit heavy-atom
# count that rounds one direction never trips a healthy row.
_HEAVY_ATOM_PASS_FRACTION: float = 0.95

# RDKit availability probe. Imported lazily so the module continues to
# import (and every unrelated test continues to pass) on a host without
# rdkit — the check gracefully degrades to the legacy ≥1-HETATM rule
# with ``receipt_threshold_source="degraded_no_rdkit"`` stamped on the
# detail dict when the check fires.
try:
    from rdkit import Chem as _rdkit_Chem  # type: ignore

    _RDKIT_AVAILABLE = True
except Exception:  # noqa: BLE001 — rdkit imports can raise a wide range
    _rdkit_Chem = None  # type: ignore
    _RDKIT_AVAILABLE = False


def _expected_heavy_atoms_from_smiles(smi: str) -> Optional[int]:
    """Return the heavy-atom count implied by ``smi``.

    Returns ``None`` in either of two cases:
      - RDKit is not importable on this host (degraded fallback).
      - ``smi`` is unparseable / empty (SMILES-probe malformed cell).

    The caller distinguishes the two via ``_RDKIT_AVAILABLE``.
    """
    if not _RDKIT_AVAILABLE or _rdkit_Chem is None:
        return None
    smi = (smi or "").strip()
    if not smi:
        return None
    try:
        mol = _rdkit_Chem.MolFromSmiles(smi)
    except Exception:  # noqa: BLE001
        return None
    if mol is None:
        return None
    try:
        return int(mol.GetNumHeavyAtoms())
    except Exception:  # noqa: BLE001
        return None


def _expected_residues_from_peptide_sequence(seq: str) -> Optional[int]:
    """Return the residue count implied by a peptide ligand's
    ``ligand_sequence``. Returns ``None`` when the sequence is empty.

    The peptide receipt asserts residue-count coverage on the non-receptor
    chain rather than heavy-atom count: (a) peptide ligands are protein
    residues, ``count_ligand_heavy_atoms`` does not see them; (b) a
    residue-level 95 % threshold on the sequence-length is directly
    comparable to the small-molecule heavy-atom threshold and avoids a
    per-residue heavy-atom lookup that would need Biopython (unavailable
    on the current scoring venv).
    """
    if not seq:
        return None
    s = seq.strip()
    if not s:
        return None
    return len(s)


def _row_field(row: Any, name: str) -> str:
    """Read a field off a ScorerRow (or a dict-shaped stand-in used in
    tests). Returns the empty string for missing / None / NaN-string
    values so the caller's boolean semantics work uniformly.
    """
    if row is None:
        return ""
    if isinstance(row, dict):
        val = row.get(name, "")
    else:
        val = getattr(row, name, "")
    if val is None:
        return ""
    return str(val)


def _manifest_declared_ligand(row: Any) -> bool:
    """True iff the row's manifest fields imply a ligand should be
    present in the produced CIF.

    Trigger — any one of:
      - ``ligand_type`` in {"peptide", "small_molecule"} (non-empty,
        non-apo, non-none)
      - ``ligand_smiles`` non-empty
      - ``ligand_sequence`` non-empty
    """
    ltype = _row_field(row, "ligand_type").strip().lower()
    if ltype and ltype not in _LIGAND_TYPES_NO_CHECK:
        return True
    if _row_field(row, "ligand_smiles").strip():
        return True
    if _row_field(row, "ligand_sequence").strip():
        return True
    return False


def count_ligand_heavy_atoms(
    struct: Optional[gemmi.Structure],
    *,
    receptor_chain_name: Optional[str] = None,
    non_ligand_resnames: Iterable[str] = NON_LIGAND_RESNAMES,
) -> int:
    """Count non-hydrogen atoms across all HETATM-like residues in
    ``struct`` that are NOT in the buffer/water/metal/lipid exclusion
    list and NOT standard amino-acid residues.

    ``receptor_chain_name`` is honoured when known — a HETATM ligand
    residue that sits on the same chain as the receptor still counts
    (small molecules commonly land on the receptor chain), but the
    ``one_letter(r.name) in STD_AA`` gate removes receptor amino acids
    on any chain. When ``struct`` is None or has zero models, returns 0.

    Mirrors the ligand-scan logic in
    ``scorer.pocket_metrics.build_pocket_reference_cache`` so a molecule
    that pocket_metrics would treat as the reference ligand is the same
    molecule this receipt would recognise as "ligand present".
    """
    if struct is None:
        return 0
    if len(struct) == 0:
        return 0
    exclusion = frozenset(non_ligand_resnames)
    total = 0
    model = struct[0]
    for ch in model:
        for r in ch:
            if r.name in exclusion:
                continue
            if one_letter(r.name) in STD_AA:
                continue
            for a in r:
                elem = getattr(a.element, "name", "") or ""
                if elem != "H":
                    total += 1
    return total


def _count_extra_protein_chain_residues(
    struct: Optional[gemmi.Structure],
    receptor_chain_name: Optional[str],
) -> int:
    """Count standard-AA residues on chains OTHER than the receptor
    chain. Used to detect the presence of a peptide ligand — Boltz /
    OF3 / Protenix / Chai all emit peptide ligands as their own protein
    chain distinct from the receptor. Returns 0 when struct is empty or
    when only the receptor chain has standard-AA content.
    """
    if struct is None or len(struct) == 0:
        return 0
    total = 0
    model = struct[0]
    for ch in model:
        if receptor_chain_name and ch.name == receptor_chain_name:
            continue
        for r in ch:
            if one_letter(r.name) in STD_AA:
                total += 1
    return total


def check_ligand_present(
    struct: Optional[gemmi.Structure],
    row: Any,
    *,
    receptor_chain_name: Optional[str] = None,
) -> None:
    """Raise ``ALigandPresence`` when the manifest declared a ligand but
    the produced CIF is missing the expected heavy-atom / residue mass.

    History:
      - Block C Stage 0 Step 1.4 (2026-09-04): introduced the ≥ 1 heavy-atom
        gate — catches "no ligand at all" (Chai silent-apo shape).
      - Post-Audit Stage 1 (2026-09-05): chemistry-aware split — small-
        molecule branch counts HETATMs, peptide branch counts standard-AA
        residues on a non-receptor chain.
      - Post-Tier-3 Stage 0 item 4 (2026-09-06, this patch): raised the
        threshold from ≥ 1 present to ≥ 95 % of the SMILES- (or sequence-)
        implied count. Catches partial-tokenization silent failures where
        1 atom lands instead of the expected 25 — a nominally-populated
        but scientifically wrong ligand pose that the Tier 1 audit named.

    Branch summary:
      - ``ligand_type in {small_molecule}`` or non-empty ``ligand_smiles``
        (without ``ligand_sequence``): compare observed HETATM heavy atoms
        against RDKit's ``mol.GetNumHeavyAtoms()``. Below 95 % raises
        ``ALigandPresence`` with ``reason="partial_atoms"`` and the
        ``n_heavy_atoms_present`` / ``n_heavy_atoms_expected`` fields
        stamped on the detail dict. Zero HETATM heavy atoms still raise
        with the legacy ``reason="zero_ligand_heavy_atoms"`` so downstream
        failure-census bins do not shift.
      - ``ligand_type == peptide`` or non-empty ``ligand_sequence``: count
        standard-AA residues on non-receptor chains and require
        ≥ 95 % of ``len(ligand_sequence)``. Zero residues stays on the
        legacy ``zero_peptide_residues_off_receptor`` reason.
      - Ambiguous ligand context (SMILES + sequence both set, or neither
        set): fall back to the legacy ≥ 1 HETATM rule.

    ``receptor_chain_name`` is required for the peptide path — the
    HETATM heuristic ignores it (peptides are protein residues, not
    HETATM). When it's not known at call time, the peptide check
    quietly skips (better than a false raise).

    Graceful degradation — when RDKit is not importable OR the SMILES is
    unparseable, the small-molecule branch falls back to the legacy
    ≥ 1 HETATM rule and, when it fires, stamps
    ``receipt_threshold_source="degraded_no_rdkit"`` (or
    ``"degraded_smiles_unparseable"``) on the detail dict. Passing rows
    with the degraded path go through with no visible change — the new
    threshold cannot lie about atom counts it could not compute.
    """
    if not _manifest_declared_ligand(row):
        return
    ltype = _row_field(row, "ligand_type").strip().lower()
    smi = _row_field(row, "ligand_smiles").strip()
    seq = _row_field(row, "ligand_sequence").strip()

    is_smallmol = ltype == "small_molecule" or (bool(smi) and not seq)
    is_peptide = ltype == "peptide" or (bool(seq) and not smi)

    if is_smallmol:
        n_heavy = count_ligand_heavy_atoms(
            struct, receptor_chain_name=receptor_chain_name,
        )
        expected = _expected_heavy_atoms_from_smiles(smi)
        if expected is None:
            # Degraded fallback — RDKit missing or SMILES unparseable.
            # Stay on the legacy ≥ 1 HETATM rule, flag the source so a
            # census / rescore can distinguish these rows.
            threshold_source = (
                "degraded_no_rdkit"
                if not _RDKIT_AVAILABLE
                else "degraded_smiles_unparseable"
            )
            if n_heavy == 0:
                raise ALigandPresence(
                    "manifest declared small-molecule ligand but CIF has "
                    "zero non-buffer HETATM heavy atoms (silent-apo shape)",
                    reason="zero_ligand_heavy_atoms",
                    ligand_type=ltype,
                    ligand_smiles=smi,
                    ligand_sequence_len=len(seq),
                    receptor_chain=receptor_chain_name or "",
                    n_heavy_atoms_present=n_heavy,
                    n_heavy_atoms_expected=None,
                    receipt_threshold_source=threshold_source,
                )
            return
        # Full path — RDKit-parseable SMILES + non-degenerate expected.
        # Zero-heavy-atom keeps the legacy failure bin so downstream
        # census does not silently shift under this patch.
        if n_heavy == 0:
            raise ALigandPresence(
                "manifest declared small-molecule ligand but CIF has zero "
                "non-buffer HETATM heavy atoms (silent-apo shape)",
                reason="zero_ligand_heavy_atoms",
                ligand_type=ltype,
                ligand_smiles=smi,
                ligand_sequence_len=len(seq),
                receptor_chain=receptor_chain_name or "",
                n_heavy_atoms_present=n_heavy,
                n_heavy_atoms_expected=expected,
                receipt_threshold_source="rdkit_smiles",
            )
        # Partial-tokenization gate — the new bit.
        threshold = _HEAVY_ATOM_PASS_FRACTION * float(expected)
        if float(n_heavy) < threshold:
            raise ALigandPresence(
                "manifest declared small-molecule ligand but CIF has "
                f"only {n_heavy} of the expected {expected} heavy atoms "
                f"(<{int(_HEAVY_ATOM_PASS_FRACTION * 100)} %, partial "
                "tokenization)",
                reason="partial_atoms",
                ligand_type=ltype,
                ligand_smiles=smi,
                ligand_sequence_len=len(seq),
                receptor_chain=receptor_chain_name or "",
                n_heavy_atoms_present=n_heavy,
                n_heavy_atoms_expected=expected,
                pass_fraction=_HEAVY_ATOM_PASS_FRACTION,
                receipt_threshold_source="rdkit_smiles",
            )
    elif is_peptide:
        # Skip when we can't identify the receptor chain — a mis-fire
        # is worse than a missed silent-apo.
        if not receptor_chain_name:
            return
        n_pep = _count_extra_protein_chain_residues(
            struct, receptor_chain_name,
        )
        expected_pep = _expected_residues_from_peptide_sequence(seq)
        if n_pep == 0:
            raise ALigandPresence(
                "manifest declared peptide ligand but CIF has zero "
                "standard-AA residues on any non-receptor chain",
                reason="zero_peptide_residues_off_receptor",
                ligand_type=ltype,
                ligand_smiles=smi,
                ligand_sequence_len=len(seq),
                receptor_chain=receptor_chain_name or "",
                n_heavy_atoms_present=n_pep,
                n_heavy_atoms_expected=expected_pep,
                receipt_threshold_source="peptide_sequence",
            )
        if expected_pep is not None and expected_pep > 0:
            threshold_pep = _HEAVY_ATOM_PASS_FRACTION * float(expected_pep)
            if float(n_pep) < threshold_pep:
                raise ALigandPresence(
                    "manifest declared peptide ligand but CIF has "
                    f"only {n_pep} of the expected {expected_pep} "
                    "standard-AA residues on non-receptor chains "
                    f"(<{int(_HEAVY_ATOM_PASS_FRACTION * 100)} %, partial "
                    "tokenization)",
                    reason="partial_peptide_residues",
                    ligand_type=ltype,
                    ligand_smiles=smi,
                    ligand_sequence_len=len(seq),
                    receptor_chain=receptor_chain_name or "",
                    n_heavy_atoms_present=n_pep,
                    n_heavy_atoms_expected=expected_pep,
                    pass_fraction=_HEAVY_ATOM_PASS_FRACTION,
                    receipt_threshold_source="peptide_sequence",
                )
    else:
        # Ambiguous ligand context — neither small_molecule nor peptide
        # was declared, but the manifest carried ligand_smiles /
        # ligand_sequence. Fall back to the legacy HETATM-only check.
        n_heavy = count_ligand_heavy_atoms(
            struct, receptor_chain_name=receptor_chain_name,
        )
        if n_heavy == 0:
            raise ALigandPresence(
                "manifest declared ligand but CIF has zero non-buffer "
                "HETATM heavy atoms (silent-apo shape)",
                reason="zero_ligand_heavy_atoms",
                ligand_type=ltype,
                ligand_smiles=smi,
                ligand_sequence_len=len(seq),
                receptor_chain=receptor_chain_name or "",
                n_heavy_atoms_present=n_heavy,
                n_heavy_atoms_expected=None,
                receipt_threshold_source="ambiguous_ligand_context",
            )


# ---------------------------------------------------------------------------
# Receptor-slug receipt
# ---------------------------------------------------------------------------

# String values that CSV / pandas commonly emit for a missing scalar and
# that the receipt should treat as equivalent to "not populated".
_NAN_LIKE_SLUG_VALUES: frozenset[str] = frozenset({
    "", "nan", "NaN", "NAN", "None", "none", "null", "NULL",
})


def _slug_is_populated(slug: str) -> bool:
    """True iff ``slug`` is a non-empty, non-NaN-like receptor slug."""
    if slug is None:
        return False
    s = str(slug).strip()
    if not s:
        return False
    if s in _NAN_LIKE_SLUG_VALUES:
        return False
    # Guard against a stray float("nan") sneaking in as its repr.
    try:
        f = float(s)
        if math.isnan(f):
            return False
    except (TypeError, ValueError):
        pass
    return True


def check_receptor_slug_populated(row: Any) -> None:
    """Raise ``AReceptorSlugMissing`` when ``row.receptor_slug`` is empty
    or NaN-like.

    Defence-in-depth — ``scorer.receptors.resolve_receptor`` raises
    ``A6ReceptorIdentity`` on ambiguous / unresolved input and returns
    a non-empty upper-case slug on success. This receipt catches any
    future regression that blanks the slug between A6 success and axis
    emission (the failure shape seen with OPSD / B1B1U5 earlier this
    campaign, where receptor_slug landed as NaN on downstream tables).
    """
    slug = _row_field(row, "receptor_slug")
    if not _slug_is_populated(slug):
        raise AReceptorSlugMissing(
            "row missing populated receptor_slug",
            reason="empty_or_nan_receptor_slug",
            observed=slug,
        )
