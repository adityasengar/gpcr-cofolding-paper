"""VerifiedModel — a UniProt-numbered receptor model that CANNOT be constructed
without A1/A2/A3 verification having run.

Founding premise (see docs/AUDIT_TRAIL.md): assertions cannot be
bypassed. The first real use of the scorer at M1 exposed a bypass —
``scorer.refs_build.cmd_thresholds`` called ``compute_all_axes`` on a
raw ``UnverifiedUniProtModel`` for AGTR1 (6OS2) even though A1 had
raised at build time, and wrote garbage axes (TM6=32.11 Å, NPxxY=44.71
Å) to the ledger.

Fix — architectural, not local: this module is the ONLY place that can
mint a ``VerifiedModel``, and it does so only through ``verify()``,
which runs A2 (anchor coverage) and A1 (AA identity) before returning.
Downstream, ``scorer.axes.compute_all_axes`` and every threshold /
axis / classification call accepts ONLY ``VerifiedModel`` — passing a
raw model is a type error.

The lint bans direct construction of ``VerifiedModel`` outside this
file (see ci/lint_anti_patterns.sh).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from scorer.anchors import (
    AnchorSet,
    verify_aa_identity,
    verify_anchor_coverage,
)
from scorer.assertions import (
    A1AminoAcidIdentity,
    A1AnchorMappingFail,
    A1WrongIdentity,
)

if TYPE_CHECKING:
    from scorer.structure import UnverifiedUniProtModel


# Construction sentinel — no external code can forge this because it's a
# module-private object and the lint bans references from outside this file.
_SEAL = object()


@dataclass(frozen=True)
class VerifiedModel:
    """Immutable wrapper carrying proof that A1, A2, A3 ran and passed.

    Construction is restricted: any call site must go through ``verify()``.
    The sentinel check in ``__post_init__`` is a defence-in-depth check;
    the lint's grep-based ban on ``VerifiedModel(`` outside this file is
    the primary guard.
    """

    _unverified: object  # UnverifiedUniProtModel from scorer.structure
    _anchor_set: AnchorSet
    _seal: object
    _skip_dry: bool = False

    def __post_init__(self) -> None:
        if self._seal is not _SEAL:
            raise TypeError(
                "VerifiedModel cannot be constructed directly; go through "
                "scorer.verified.verify(). See docs/ASSERTIONS.md."
            )

    # -- read-only accessors mirroring UnverifiedUniProtModel's surface -----

    @property
    def entry_name(self) -> str:
        return self._unverified.entry_name

    @property
    def chain_name(self) -> str:
        return self._unverified.chain_name

    @property
    def residues(self) -> "dict":
        return self._unverified.residues

    @property
    def identity(self) -> float:
        return self._unverified.identity

    @property
    def matched(self) -> int:
        return self._unverified.matched

    @property
    def anchor_set(self) -> AnchorSet:
        return self._anchor_set

    @property
    def skip_dry(self) -> bool:
        return self._skip_dry

    def observed_positions(self) -> set[int]:
        return self._unverified.observed_positions()

    def ca(self, uniprot_pos: int):
        return self._unverified.ca(uniprot_pos)

    def observed_aa_at(self, uniprot_pos: int) -> str | None:
        return self._unverified.observed_aa_at(uniprot_pos)


def verify_reference_pdb(
    unverified: "UnverifiedUniProtModel",
    anchor_set: AnchorSet,
) -> "VerifiedReferenceResult":
    """Lenient verify() for CURATED reference crystals — refs_build path only.

    Finding #7 (docs/AUDIT_TRAIL.md): the strict verify() gate was too
    coarse-grained for reference PDBs. It raised A1 on ANY resolved-anchor
    identity mismatch (killing NPY2R/LT4R1 measurements because their
    thermostabilising H3.51Y / S3.51Y mutation triggered A1 on an anchor
    that doesn't participate in the d_r350_r630_ca axis), and it raised A2
    globally when ANY required anchor was missing (killing NPxxY as
    collateral damage when only 6.30 was disordered). Every failure was
    swallowed by the bare-except in ``refs_build.cmd_build`` and written
    as ``nan`` to ``refs/reference_set.csv`` — silent measurement failure,
    the class of bug this scorer was designed to eliminate.

    This function is intentionally more permissive than ``verify()``:

      - A1 identity check runs **only on IDENTITY-DEFINING anchors** —
        3.50 (DRY-R, whose CZ atom the DRY axis needs), 5.58 (Y whose OH
        the Y5.58-pack axis needs), 7.53 (Y whose CA the NPxxY axis
        anchors on). Mismatches at 3.51 / 6.30 / 6.34 are recorded in the
        returned per-anchor status but do NOT raise — those anchors carry
        no identity requirement for the CA-CA axes and a mismatch there
        on a curated reference is a thermostabilising point mutation, not
        a wrong-chain error (A3 already rules that out with its
        ≥0.70 identity + ≥200 matched gate).

      - A2 coverage does NOT raise globally. Coverage is checked per
        anchor and returned in the result; the caller decides per-axis
        whether a measurement is possible (axes.py returns NaN already
        when the specific anchor CA is missing).

    Guardrails preserved:

      - A3 remains authoritative (chain-picker + ≥0.70 identity + ≥200
        matched, in ``structure.build_uniprot_model``).
      - Identity-defining anchor mismatches still raise A1 — 3.50 R→L
        (NTR1 6YVR wrong chain) and 7.53 Y→X still fire.
      - Coverage of 3.50 CA and 6.30 CA is still checked (only the d_tm6
        axis fires NaN cleanly when either is missing).

    Returns a ``VerifiedReferenceResult`` carrying the sealed
    ``VerifiedModel`` plus per-anchor availability / mismatch info the
    caller records in provenance and uses to explain any NaN.

    NEVER call this from the scoring path. It exists to measure
    reference crystals only.
    """
    # A2: per-anchor coverage. Record what is / isn't present; do not
    # raise. axes.py handles missing anchors by returning NaN for the
    # specific axis that needs them.
    obs_positions = unverified.observed_positions()
    per_anchor_present: dict[str, bool] = {}
    for label, anchor in anchor_set.anchors.items():
        per_anchor_present[label] = anchor.uniprot_pos in obs_positions
    coverage_missing: list[str] = [
        label for label, ok in per_anchor_present.items() if not ok
    ]

    # A1: identity check on IDENTITY-DEFINING anchors only. Non-defining
    # anchors (3.51, 6.30, 6.34) may legitimately carry point mutations
    # in curated reference crystals — see docstring.
    #
    # Identity-defining rationale, per axis:
    #   - 3.50 R: DRY axis uses guanidinium CZ (needs Arg)
    #   - 5.58 Y: NPxxY & Y5.58-pack axes use side-chain OH (needs Tyr)
    #   - 7.53 Y: NPxxY axis CA anchors on the canonical NPxxY tyrosine
    #
    # 3.51, 6.30, 6.34 mismatches are diagnostic and do not corrupt any
    # CA-CA axis or side-chain axis. They are recorded, not raised.
    from scorer.structure import STD_AA, one_letter
    identity_defining = ("3.50", "5.58", "7.53")
    identity_defining_mismatches: dict[str, tuple[str, str]] = {}
    per_anchor_observed: dict[str, str] = {}
    for label, anchor in anchor_set.anchors.items():
        r = unverified.residues.get(anchor.uniprot_pos)
        if r is None:
            continue
        aa = one_letter(r.name)
        if aa not in STD_AA:
            continue
        per_anchor_observed[label] = aa
        if aa != anchor.aa_expected and label in identity_defining:
            identity_defining_mismatches[label] = (anchor.aa_expected, aa)

    if identity_defining_mismatches:
        # Sub-kind by whole-chain identity (same convention as strict A1)
        model_identity = getattr(unverified, "identity", None)
        anchor_mapping_threshold = 0.90
        if model_identity is not None and model_identity >= anchor_mapping_threshold:
            cls: type[A1AminoAcidIdentity] = A1AnchorMappingFail
        else:
            cls = A1WrongIdentity
        raise cls(
            f"identity-defining anchor mismatch at {list(identity_defining_mismatches)}: "
            f"expected/observed = {identity_defining_mismatches}",
            mismatches=identity_defining_mismatches,
            entry_name=anchor_set.entry_name,
            model_identity=model_identity,
            sub_kind=cls.sub_kind,
        )

    # Non-defining mismatches (recorded, not raised)
    diagnostic_mismatches: dict[str, tuple[str, str]] = {}
    for label, anchor in anchor_set.anchors.items():
        aa = per_anchor_observed.get(label)
        if aa is None or label in identity_defining:
            continue
        if aa != anchor.aa_expected:
            diagnostic_mismatches[label] = (anchor.aa_expected, aa)

    vmodel = VerifiedModel(
        _unverified=unverified,
        _anchor_set=anchor_set,
        _seal=_SEAL,
        _skip_dry=False,
    )
    return VerifiedReferenceResult(
        model=vmodel,
        anchor_present=per_anchor_present,
        anchor_observed=per_anchor_observed,
        diagnostic_mismatches=diagnostic_mismatches,
        coverage_missing=coverage_missing,
    )


@dataclass(frozen=True)
class VerifiedReferenceResult:
    """Return type of ``verify_reference_pdb``.

    Carries the sealed VerifiedModel plus per-anchor availability / point-
    mutation info so refs_build.cmd_build can record it in provenance
    and explain any NaN.
    """
    model: VerifiedModel
    anchor_present: "dict"           # {bw_label: bool}
    anchor_observed: "dict"          # {bw_label: one_letter_aa} (only for observed)
    diagnostic_mismatches: "dict"    # {bw_label: (expected, observed)} — non-defining
    coverage_missing: "list"         # [bw_label,...] anchors not observed

    def has_axis_coverage(self, *labels: str) -> bool:
        """Are all given anchor labels observed? (Per-axis coverage check.)"""
        return all(self.anchor_present.get(label, False) for label in labels)


def verify(
    unverified: "UnverifiedUniProtModel",
    anchor_set: AnchorSet,
    *,
    skip_dry: bool = False,
    receptor_class: str | None = None,
) -> VerifiedModel:
    """Run A2 (anchor coverage) and A1 (AA identity) on ``unverified``.

    Raises ``A2FASTATrunc`` if any required anchor's CA is missing.
    Raises ``A1AminoAcidIdentity`` if any resolved anchor's observed AA
    differs from the GPCRdb-canonical AA (with ``skip_dry=True`` exempting
    DRY 3.50/3.51 for design_no_dry / class_bc_native_no_dry claims).

    ``receptor_class`` (A/B/F/C/T2R) selects the class-conditional
    A2 required-anchor set — Class B legitimately lacks 6.30 (GLR_HUMAN
    was the trigger for parameterising this on 2026-09-02); Class F
    uses 6.31 per refs/anchors_per_class.csv. When None, defaults to
    Class A anchors for backwards compatibility.

    Only on both passes does this return a ``VerifiedModel``; ``axes.py``
    and every downstream axis / classification path accepts only that
    type. There is no other way to obtain one.

    A3 is a precondition — ``unverified`` came out of
    ``structure.build_uniprot_model`` which raises A3 on chain selection.
    So a VerifiedModel represents proof that A1, A2, A3 all passed.
    """
    # A2: anchor coverage. Raises A2FASTATrunc if 7.53 (or other required
    # anchor) has no observed CA. Class-conditional required anchor set —
    # see scorer/anchors.py::REQUIRED_ANCHORS_BY_CLASS.
    verify_anchor_coverage(
        anchor_set,
        unverified.observed_positions(),
        receptor_class=receptor_class,
    )

    # A1: AA identity at every resolved anchor.
    # Compute observed AAs at the anchor positions (avoiding a scorer.axes
    # dependency cycle — inline the small helper).
    from scorer.structure import STD_AA, one_letter
    observed_aas: dict[str, str] = {}
    for label, anchor in anchor_set.anchors.items():
        r = unverified.residues.get(anchor.uniprot_pos)
        if r is None:
            continue
        aa = one_letter(r.name)
        if aa in STD_AA:
            observed_aas[label] = aa
    verify_aa_identity(
        anchor_set, observed_aas, skip_dry=skip_dry,
        model_identity=getattr(unverified, "identity", None),
    )

    return VerifiedModel(
        _unverified=unverified,
        _anchor_set=anchor_set,
        _seal=_SEAL,
        _skip_dry=skip_dry,
    )
