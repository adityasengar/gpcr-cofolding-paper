"""A1..A6 assertion classes. Filled at commit 7 with orchestrator; the
classes themselves exist from C6 so scorer/structure.py and
scorer/anchors.py can raise them directly.

None of these classes is caught anywhere under scorer/. ci/lint_anti_patterns.sh
enforces the ban. See docs/ASSERTIONS.md.
"""
from __future__ import annotations

from typing import Any


class ScorerAssertionError(AssertionError):
    """Base for every assertion the scorer raises.

    Inherits from AssertionError so ``pytest.raises(AssertionError)`` and
    ``pytest.raises(ScorerAssertionError)`` both work. Carries a
    machine-readable ``assertion_id`` and free-form ``detail`` for CSV
    reporting.
    """

    assertion_id: str = ""

    def __init__(self, message: str, **detail: Any):
        super().__init__(message)
        self.detail = dict(detail)

    def __str__(self) -> str:
        base = super().__str__()
        if self.detail:
            return f"{base} [detail={self.detail}]"
        return base


class A1AminoAcidIdentity(ScorerAssertionError):
    """Base for the two A1 sub-kinds.

    The full-corpus rescore needs to distinguish two very different failure
    modes, both of which raise A1 today:

      - A1AnchorMappingFail  — sequence matches the intended receptor
                               (chain identity ≥ 0.90) but the ANCHOR
                               positions themselves are wrong. Cause is
                               typically a numbering shift, a fusion-insert
                               register slip, or an engineered anchor
                               mutation. RECOVERABLE by re-deriving anchors
                               per-PDB. Flag for re-derivation.

      - A1WrongIdentity      — sequence does NOT match the claimed receptor
                               (chain identity < 0.90 after A3 admitted the
                               chain at ≥0.70). The input is likely a
                               distant homolog, wrong species, or a
                               mislabelled construct. NOT recoverable by
                               re-anchoring.

    Both subclasses inherit ``assertion_id = "A1_amino_acid_identity"`` so
    the CSV column and the census consumers that read ``.assertion_id``
    still work. The distinction is on ``type(err).__name__`` — the batch
    driver's census bins on that already, so subclassing gives a clean
    separation in ``docs/figures/failure_census.tex`` without any
    per-caller wiring.
    """
    assertion_id = "A1_amino_acid_identity"


class A1AnchorMappingFail(A1AminoAcidIdentity):
    """Chain sequence matches the claimed receptor; only the anchor lookup
    is wrong. Recoverable by re-deriving anchors per-PDB."""
    sub_kind = "anchor_mapping"


class A1WrongIdentity(A1AminoAcidIdentity):
    """Chain sequence does not match the claimed receptor. Not recoverable
    by re-anchoring — the input is a different sequence."""
    sub_kind = "wrong_identity"


class A2FASTATrunc(ScorerAssertionError):
    assertion_id = "A2_fasta_completeness"


class A3WrongChain(ScorerAssertionError):
    assertion_id = "A3_wrong_chain"


class A4ReferenceClassMismatch(ScorerAssertionError):
    assertion_id = "A4_reference_class_match"


class A5SpeciesMismatch(ScorerAssertionError):
    assertion_id = "A5_species_match"


class A6ReceptorIdentity(ScorerAssertionError):
    assertion_id = "A6_receptor_identity"


# ---------------------------------------------------------------------------
# Post-run receipts (Block C Stage 0 Step 1.4, 2026-09-04)
#
# These are NOT sequenced A1..A6 pre-scoring assertions — they are named
# post-load receipts that run once the input CIF and the manifest fields
# are both in hand. Two failure shapes motivated the extension:
#
#   1. Chai silent-apo on malformed SMILES — the receptor cofolds, no
#      ligand chain is built, and ``ok=true`` lands in the status file.
#      Downstream analysis would credit apo behaviour to a
#      mis-parsed ligand. Same class of bug as audit #10 (Chai silent
#      single-sequence), one layer downstream.
#   2. ``receptor_slug=NaN`` — the OPSD/B1B1U5 chain-matcher failure
#      shape earlier in this campaign. Post-species-fix rescore
#      populates the slug correctly on every row today; the receipt is
#      defence-in-depth against a future regression.
#
# The ``A_*`` prefix (rather than ``A7`` / ``A8``) is deliberate —
# positional identity of a check is a name, not an ordinal. Same
# ``ScorerAssertionError`` catch site in ``score_and_capture``.
# ---------------------------------------------------------------------------


class ALigandPresence(ScorerAssertionError):
    """Manifest declared a ligand but the produced CIF has zero ligand
    heavy atoms. Fires only when the manifest-declared ligand fields
    (``ligand_type`` / ``ligand_smiles`` / ``ligand_sequence``) indicate a
    ligand should be present. Apo / none rows skip the check."""
    assertion_id = "A_LIGAND_PRESENT"


class AReceptorSlugMissing(ScorerAssertionError):
    """Row lacks a populated receptor_slug (empty string or NaN-like).
    resolve_receptor guarantees a non-empty slug or raises A6, so this
    is defence-in-depth against a future regression that blanks the
    field between A6 success and axis emission."""
    assertion_id = "A_RECEPTOR_SLUG_MISSING"


ALL: tuple[type[ScorerAssertionError], ...] = (
    A1AminoAcidIdentity,
    A2FASTATrunc,
    A3WrongChain,
    A4ReferenceClassMismatch,
    A5SpeciesMismatch,
    A6ReceptorIdentity,
    ALigandPresence,
    AReceptorSlugMissing,
)

# Sub-kinds carry finer-grained bin identity for the failure census.
# type(err).__name__ is the canonical bin key; ScorerRow's per-assertion
# column records the full subclass name so downstream analysis can group
# recoverable vs unrecoverable A1 failures without re-running.
A1_SUBCLASSES: tuple[type[A1AminoAcidIdentity], ...] = (
    A1AnchorMappingFail,
    A1WrongIdentity,
)
