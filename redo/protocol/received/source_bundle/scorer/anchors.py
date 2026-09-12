"""AnchorSet: BW anchors for the six positions the scorer resolves.

Every scored row identifies exactly six anchors from the GPCRdb residues/extended
payload for the receptor:

    3.50, 3.51, 5.58, 6.30, 6.34, 7.53

Position 3.50 is DRY-motif Arg (or receptor-expected residue). 7.53 is the
NPxxY Tyr. Two of the audit findings live here — A1 (identity check at every
resolved anchor) and A2 (7.53 must be present, no silent-drop).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from scorer.assertions import (
    A1AminoAcidIdentity,
    A1AnchorMappingFail,
    A1WrongIdentity,
    A2FASTATrunc,
)
from scorer.bw_numbering import Api, get_generic_numbers, lookup_bw
from scorer.cache import sha256_json
from scorer.schema import ANCHOR_KEYS


@dataclass(frozen=True)
class Anchor:
    bw_label: str          # "3.50"
    uniprot_pos: int       # 131 for β2AR 3.50
    aa_expected: str       # "R" for β2AR 3.50

    def as_tuple(self) -> tuple[int, str]:
        return self.uniprot_pos, self.aa_expected


@dataclass
class AnchorSet:
    """Six anchors resolved from GPCRdb, plus provenance."""

    entry_name: str        # "adrb2_human"
    anchors: dict[str, Anchor]
    residues_ext_payload_sha256: str  # SHA of the exact GPCRdb JSON used
    entry_url: str

    def get(self, bw_label: str) -> Anchor:
        if bw_label not in self.anchors:
            raise A2FASTATrunc(
                f"BW anchor {bw_label} not resolvable via GPCRdb for {self.entry_name}",
                anchor=bw_label, entry_name=self.entry_name,
            )
        return self.anchors[bw_label]

    def uniprot_positions(self) -> dict[str, int]:
        return {k: a.uniprot_pos for k, a in self.anchors.items()}

    def expected_aas(self) -> dict[str, str]:
        return {k: a.aa_expected for k, a in self.anchors.items()}


def resolve_anchors(api: Api, entry_name: str) -> AnchorSet:
    """Build the AnchorSet for `entry_name` from GPCRdb residues/extended.

    Any anchor GPCRdb cannot resolve (i.e. the receptor doesn't have a
    canonical position for that BW label — Class B/C receptors legitimately
    lack DRY) is simply absent from the resulting ``anchors`` dict; the
    caller (assertions.A1) decides whether that is a schema violation for
    the input's ``state_claim``.
    """
    bw_map = get_generic_numbers(api, entry_name)
    if not bw_map:
        raise A2FASTATrunc(
            f"GPCRdb returned no residues for entry {entry_name!r}",
            entry_name=entry_name,
        )
    anchors: dict[str, Anchor] = {}
    for label in ANCHOR_KEYS:
        hit = lookup_bw(bw_map, label)
        if hit is not None:
            pos, aa = hit
            anchors[label] = Anchor(bw_label=label, uniprot_pos=pos, aa_expected=aa)
    return AnchorSet(
        entry_name=entry_name,
        anchors=anchors,
        residues_ext_payload_sha256=sha256_json(bw_map),
        entry_url=f"https://gpcrdb.org/services/residues/extended/{entry_name}/",
    )


def verify_aa_identity(
    anchor_set: AnchorSet,
    observed_aas: dict[str, str],
    *,
    skip_dry: bool = False,
    model_identity: float | None = None,
    anchor_mapping_threshold: float = 0.90,
) -> None:
    """Raise A1 unless every anchor's observed AA matches GPCRdb.

    ``observed_aas`` — {bw_label: one_letter_aa} for anchors present in the
    input structure. Anchors ABSENT from observed_aas (i.e. the CA is not
    resolved) are NOT this assertion's problem — A2 handles that.

    ``skip_dry=True`` — when input_state_claim is ``design_no_dry`` or
    ``class_bc_native_no_dry``, the DRY anchors (3.50, 3.51) are exempted
    from identity checking for those receptors only. Every OTHER anchor
    remains strict. See docs/ASSERTIONS.md.

    ``model_identity`` — the whole-chain sequence identity to the WT (from
    ``UnverifiedUniProtModel.identity``). Decides which A1 subclass fires
    on mismatch:

      - ``model_identity >= anchor_mapping_threshold`` (default 0.90):
        the sequence matches; only the anchor lookup is wrong.
        Raise ``A1AnchorMappingFail`` — recoverable by re-deriving anchors.

      - ``model_identity < anchor_mapping_threshold`` (or unknown):
        the sequence itself is off. Raise ``A1WrongIdentity`` —
        not recoverable by re-anchoring.

    Census in the batch driver bins on ``type(err).__name__``, so this
    split feeds ``docs/figures/failure_census.tex`` without any
    per-call-site wiring.
    """
    mismatches: dict[str, tuple[str, str]] = {}
    for label, anchor in anchor_set.anchors.items():
        if skip_dry and label in ("3.50", "3.51"):
            continue
        observed = observed_aas.get(label)
        if observed is None:
            continue
        if observed != anchor.aa_expected:
            mismatches[label] = (anchor.aa_expected, observed)
    if not mismatches:
        return
    # decide sub-kind by whole-chain identity
    if model_identity is not None and model_identity >= anchor_mapping_threshold:
        cls: type[A1AminoAcidIdentity] = A1AnchorMappingFail
    else:
        cls = A1WrongIdentity
    raise cls(
        f"AA-identity mismatch at {list(mismatches)}: expected/observed = "
        f"{mismatches}",
        mismatches=mismatches,
        entry_name=anchor_set.entry_name,
        model_identity=model_identity,
        sub_kind=cls.sub_kind,
    )


# Class-conditional required anchors per refs/anchors_per_class.csv.
# 3.50, 5.58, 7.53 are structurally conserved across A/B/F; the TM6
# anchor differs:
#   Class A: 6.30 (DRY R6.30 / TM6 intracellular tip)
#   Class B: 6.34 (TM6 intracellular tip in Wootten numbering; Class B
#            legitimately lacks GPCRdb-canonical 6.30 — GLR_HUMAN was
#            the trigger, all 200 Block A GCGR rows landed A2FASTATrunc
#            on the hardcoded 6.30 check before this parameterisation)
#   Class F: 6.31 (empirically-derived per anchors_per_class.csv;
#            similar rationale — Class F TM6 geometry differs)
# 7.53 is always required (audit #5: silent-drop-past-7.53 countermeasure).
REQUIRED_ANCHORS_BY_CLASS: dict[str, tuple[str, ...]] = {
    "A":   ("3.50", "5.58", "6.30", "7.53"),
    "B":   ("3.50", "5.58", "6.34", "7.53"),
    # Class F: refs/anchors_per_class.csv lists 6.31 as the analysis-side
    # anchor, BUT GPCRdb does NOT return a canonical 6.31 position for
    # FZD4/6/7 or SMO — verified 2026-09-02 on all four Class F
    # receptors. The scorer needs a GPCRdb-provided anchor here, and
    # 6.30 IS available for every Class F entry. Using 6.30 for A2
    # coverage keeps FZD6 (Block A) resolving; the 6.31 label from
    # anchors_per_class.csv is a derivation-side convention, not a
    # GPCRdb BW position, so we cannot demand it in A2 without silently
    # failing every Class F receptor (as the 2026-09-02T09:00 rescore
    # 34934363 did on FZD6 before this correction).
    "F":   ("3.50", "5.58", "6.30", "7.53"),
    # Class C (mGluRs) and T2R (bitter taste): dimer-interface activation
    # mechanism, no single TM6-outward anchor is the field convention. Fall
    # back to the intersection: 3.50 + 7.53 alone until class-specific
    # anchors are curated.
    "C":   ("3.50", "7.53"),
    "T2R": ("3.50", "7.53"),
    # 'N' = not-a-GPCR (partner protein) — verify_anchor_coverage should
    # never be called on those, but if it is, don't require any.
    "N":   (),
}
_DEFAULT_REQUIRED = REQUIRED_ANCHORS_BY_CLASS["A"]


def required_anchors_for_class(receptor_class: str | None) -> tuple[str, ...]:
    """Return the required anchor labels for A2 coverage per receptor
    class. Unknown / None class falls back to Class A defaults — a
    conservative choice that will surface as A2FASTATrunc rather than
    silently pass an unclassified receptor.
    """
    if receptor_class is None:
        return _DEFAULT_REQUIRED
    return REQUIRED_ANCHORS_BY_CLASS.get(receptor_class.upper(), _DEFAULT_REQUIRED)


def verify_anchor_coverage(
    anchor_set: AnchorSet,
    observed_positions: set[int],
    *,
    required_labels: tuple[str, ...] | None = None,
    receptor_class: str | None = None,
) -> None:
    """Raise A2 if any of the required anchors has no observed CA in
    the input structure. 7.53 is always required — that is the
    silent-drop-past-7.53 countermeasure (audit #5).

    If ``required_labels`` is passed explicitly, that list is used
    verbatim (callers that want to override the class-based default).
    Otherwise ``receptor_class`` selects the anchor set via
    ``required_anchors_for_class`` — Class A: 3.50/5.58/6.30/7.53,
    Class B: 3.50/5.58/6.34/7.53, Class F: 3.50/5.58/6.31/7.53. See
    ``REQUIRED_ANCHORS_BY_CLASS``.

    If neither is provided, defaults to the Class A anchor set for
    backwards compatibility with pre-2026-09-02 callers.
    """
    if required_labels is None:
        required_labels = required_anchors_for_class(receptor_class)
    missing: list[str] = []
    for label in required_labels:
        if label not in anchor_set.anchors:
            missing.append(f"{label} (not in GPCRdb for {anchor_set.entry_name})")
            continue
        pos = anchor_set.anchors[label].uniprot_pos
        if pos not in observed_positions:
            missing.append(f"{label} @ UniProt {pos}")
    if missing:
        raise A2FASTATrunc(
            f"input structure missing required anchors: {missing}. "
            f"Input probably truncated past 7.53 (see docs/AUDIT_TRAIL.md#5).",
            missing=missing, entry_name=anchor_set.entry_name,
        )
