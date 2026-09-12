"""Pre-flight acceptance gate — predicts A1/A2/A3/A5/A6 for a proposal.

Five pure functions plus one orchestrator. Each check answers "would this
proposal fail its corresponding A-gate at score time?" *without* running the
scorer, without a structure prediction, without any HPC access.

The rules are the SAME rules the scorer uses at score time — same GPCRdb
anchor resolution, same reference-set CSV, same aligner. The only
difference is that the scorer runs post-hoc on a fold model; the pre-check
runs pre-flight on the analyst's YAML. If the scorer's A-gates ever
tighten, this module picks it up automatically because the code paths
overlap. See docs/PIPELINE_INTERPRETATION.md#pre-check and
`silly-leaping-aho` plan for the design.

Design principles (from the plan):

  1. **Warn but never refuse** — every function returns
     ``("pass", "")`` or ``("warn_A<N>", "<reason>")``. The caller
     always emits the manifest; the pre-check is an interpretation-time
     signal, not a gate.
  2. **Pure functions** — no side effects; deterministic given
     ``(inputs, GPCRdb cache)``. Cache lives at the same location the
     scorer uses (``refs/cache/gpcrdb/``).
  3. **Reuse the scorer's own primitives** — ``resolve_anchors``,
     ``_score_aligned``, ``KNOWN_RECEPTORS``, ``ReferenceSet``. No
     duplication of gate logic; drift-free by construction.
  4. **PC5 is only fired for `partner_perturbation == "wt"`** —
     chimeric / truncated / designed / shuffled specs have low
     identity to WT by design; running the A3 predictor on them
     would produce a false positive.

Usage from Python:

    from scorer.pre_check import run_all_checks, load_ref_species_map
    from scorer.bw_numbering import Api

    api = Api(cache_dir="refs/cache/gpcrdb")
    ref_species_map = load_ref_species_map("refs/reference_set.csv")
    results = run_all_checks(
        receptor_slug="AA2AR",
        species="human",
        fasta_seq="MP...KLR",          # UniProt-canonical WT for AA2AR
        partner_perturbation="wt",
        ref_species_map=ref_species_map,
        api=api,
    )
    # results = {"pc1": ("pass", ""), "pc2": ("pass", ""), ...}
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scorer.anchors import resolve_anchors
from scorer.bw_numbering import Api
from scorer.receptors import KNOWN_RECEPTORS
from scorer.structure import _score_aligned


# ---------------------------------------------------------------------------
# Helper — build the (receptor, species) map from refs/reference_set.csv
# ---------------------------------------------------------------------------


def load_ref_species_map(ref_csv_path: str | Path) -> dict[str, set[str]]:
    """Return ``{receptor_slug: {species, species, ...}}`` from the raw
    CSV. Necessary because ``ReferenceSet._by_receptor`` deduplicates by
    (receptor, role) and would silently discard cross-species reference
    rows (NTR1 has both human and rat rows, for example). PC2 needs the
    full set.
    """
    p = Path(ref_csv_path)
    if not p.exists():
        return {}
    out: dict[str, set[str]] = {}
    with p.open() as f:
        for row in csv.DictReader(f):
            slug = (row.get("receptor_slug") or "").strip().upper()
            species = (row.get("species") or "").strip().lower()
            if not slug or not species:
                continue
            out.setdefault(slug, set()).add(species)
    return out


# ---------------------------------------------------------------------------
# 1-letter → 3-letter (used by PC5's aligner shim)
# ---------------------------------------------------------------------------

_ONE_TO_THREE = {
    "A": "ALA", "C": "CYS", "D": "ASP", "E": "GLU", "F": "PHE",
    "G": "GLY", "H": "HIS", "I": "ILE", "K": "LYS", "L": "LEU",
    "M": "MET", "N": "ASN", "P": "PRO", "Q": "GLN", "R": "ARG",
    "S": "SER", "T": "THR", "V": "VAL", "W": "TRP", "Y": "TYR",
}


@dataclass(frozen=True)
class _MockResidue:
    """Minimal residue-like object for feeding ``_score_aligned``.

    ``_score_aligned`` calls ``one_letter(r.name)`` on each element of the
    residues list — nothing else. Our mock exposes the 3-letter code as
    ``.name`` and lets the aligner run on a FASTA string.
    """
    name: str


def _fasta_to_mock_residues(fasta_seq: str) -> list[_MockResidue]:
    """FASTA one-letter string → list of _MockResidue with 3-letter names.

    Unknown one-letter codes (e.g. ``X`` for placeholder) become
    ``"UNK"`` — the aligner treats them as non-standard and drops them
    from match blocks. That matches the scorer's own behaviour.
    """
    return [_MockResidue(name=_ONE_TO_THREE.get(c.upper(), "UNK")) for c in fasta_seq]


# ---------------------------------------------------------------------------
# PC1 — predicts A6 (receptor identity)
# ---------------------------------------------------------------------------


def pc1_receptor_known(receptor_slug: str) -> tuple[str, str]:
    """Return ``("pass", "")`` if the receptor slug is in
    ``scorer.receptors.KNOWN_RECEPTORS``; otherwise ``("warn_A6", reason)``.

    Predicts A6 exactly — the same dict is what the scorer's receptor
    resolver validates against.
    """
    up = receptor_slug.strip().upper()
    if not up:
        return "warn_A6", "empty receptor_slug"
    if up not in KNOWN_RECEPTORS:
        return (
            "warn_A6",
            f"receptor {up!r} is not in KNOWN_RECEPTORS — curate the "
            f"receptor first (add to scorer/receptors.py::KNOWN_RECEPTORS "
            f"and refs/reference_pdbs.csv). At score time this would raise "
            f"A6ReceptorIdentity.",
        )
    return "pass", ""


# ---------------------------------------------------------------------------
# PC2 — predicts A5 (species mismatch)
# ---------------------------------------------------------------------------


def pc2_species_ref_exists(
    receptor_slug: str,
    species: str,
    ref_species_map: dict[str, set[str]],
) -> tuple[str, str]:
    """Return ``("pass", "")`` if the receptor has at least one reference
    row for the requested species; else ``("warn_A5", reason)``.

    A missing reference isn't a strict fail (A4 is annotation-only for
    missing refs per the 2026-08-26 policy) — but if references EXIST
    for the receptor and none match the input species, A5 will fire at
    score time. That's what this check predicts.
    """
    up = receptor_slug.strip().upper()
    sp = species.strip().lower()
    if not sp:
        return "pass", "empty species; A5 does not gate"
    ref_species = ref_species_map.get(up, set())
    if not ref_species:
        # No refs at all → A5 doesn't fire (nothing to compare against).
        # A4 was here to gate "no reference" but is now annotation-only.
        return "pass", f"no reference rows for {up}; A5 does not gate (soft-fail)"
    if sp in ref_species:
        return "pass", ""
    return (
        "warn_A5",
        f"reference rows for {up} exist only in species {sorted(ref_species)!r}; "
        f"input species {sp!r} would fail A5SpeciesMismatch at score time. "
        f"Curate a cross-species reference (see NTR1 rat precedent), or "
        f"accept the A5 warning as an expected outcome.",
    )


# ---------------------------------------------------------------------------
# PC3 — predicts A2 (FASTA doesn't cover required anchors)
# ---------------------------------------------------------------------------


_REQUIRED_ANCHORS = ("3.50", "5.58", "6.30", "7.53")


def pc3_fasta_covers_anchors(
    receptor_slug: str,
    fasta_seq: str,
    api: Api,
) -> tuple[str, str]:
    """Verify the FASTA is long enough that positions 3.50/5.58/6.30/7.53
    (UniProt-numbered) fall inside it.

    Predicts A2FASTATrunc: at score time the scorer would fail if any of
    those anchor CAs isn't in the structure — usually because the FASTA
    was truncated past TM7. Pre-check catches it before compute is spent.

    Uses ``resolve_anchors`` — same GPCRdb call the scorer uses; cache is
    shared, so this is a no-op after the first call per receptor.
    """
    up = receptor_slug.strip().upper()
    if up not in KNOWN_RECEPTORS:
        return "pass", "unknown receptor; A6 will fire before A2 is reached"
    entry_name = KNOWN_RECEPTORS[up]
    try:
        aset = resolve_anchors(api, entry_name)
    except Exception as e:  # pragma: no cover - GPCRdb failure is noisy
        return "pass", f"could not resolve anchors ({type(e).__name__}): skipping PC3"
    fasta_len = len(fasta_seq)
    missing: list[str] = []
    for label in _REQUIRED_ANCHORS:
        anchor = aset.anchors.get(label)
        if anchor is None:
            # Anchor not in GPCRdb for this receptor (e.g. Class B/C lacks
            # DRY). The scorer's A2 requires the ANCHOR to exist and its
            # CA to be present; if it doesn't exist in GPCRdb, A2 won't
            # be checked for that anchor.
            continue
        if anchor.uniprot_pos > fasta_len:
            missing.append(f"{label}@UniProt{anchor.uniprot_pos}")
    if missing:
        return (
            "warn_A2",
            f"FASTA length {fasta_len} does not cover required anchor(s) "
            f"{missing} — at score time A2FASTATrunc would fire. Extend "
            f"the FASTA past position {max(aset.anchors[l].uniprot_pos for l in _REQUIRED_ANCHORS if l in aset.anchors)}.",
        )
    return "pass", ""


# ---------------------------------------------------------------------------
# PC4 — predicts A1 (identity-anchor AA mismatch)
# ---------------------------------------------------------------------------


_IDENTITY_ANCHORS = ("3.50", "5.58", "7.53")


def pc4_identity_anchors_match(
    receptor_slug: str,
    fasta_seq: str,
    api: Api,
) -> tuple[str, str]:
    """Compare the observed AA at each identity-defining anchor
    (3.50/5.58/7.53) in the FASTA against GPCRdb's canonical residue for
    the receptor. Warns on any mismatch.

    Predicts A1AminoAcidIdentity. Non-identity anchors (3.51, 6.30, 6.34)
    are diagnostic-only and do NOT warn — thermostabilising point
    mutations there are accepted by the scorer's lenient reference-side
    path and expected in engineered constructs.

    FASTA indexing: UniProt positions are 1-based (position N is
    ``fasta_seq[N-1]`` in Python), which is what the scorer uses.
    """
    up = receptor_slug.strip().upper()
    if up not in KNOWN_RECEPTORS:
        return "pass", "unknown receptor; A6 will fire before A1 is reached"
    entry_name = KNOWN_RECEPTORS[up]
    try:
        aset = resolve_anchors(api, entry_name)
    except Exception as e:  # pragma: no cover
        return "pass", f"could not resolve anchors ({type(e).__name__}): skipping PC4"
    mismatches: list[str] = []
    for label in _IDENTITY_ANCHORS:
        anchor = aset.anchors.get(label)
        if anchor is None:
            continue    # class B/C legitimately lacks DRY etc.; not our concern
        pos = anchor.uniprot_pos
        if pos > len(fasta_seq) or pos < 1:
            continue    # A2 will catch it
        observed = fasta_seq[pos - 1].upper()
        if observed != anchor.aa_expected:
            mismatches.append(
                f"{label}@{pos} expected {anchor.aa_expected}, got {observed}"
            )
    if mismatches:
        return (
            "warn_A1",
            f"identity-anchor mismatch(es): {mismatches} — at score time "
            f"A1AminoAcidIdentity would fire. Either the FASTA is a "
            f"different species/orthologue, or the wrong receptor_slug "
            f"was set. Fix the FASTA or update the slug.",
        )
    return "pass", ""


# ---------------------------------------------------------------------------
# PC5 — predicts A3 (chain-picker: identity ≥0.70 + matched ≥200 vs WT)
# ---------------------------------------------------------------------------


_A3_MIN_IDENTITY = 0.70
_A3_MIN_MATCHED = 200


def pc5_identity_matched_pass(
    receptor_slug: str,
    fasta_seq: str,
    partner_perturbation: str,
    api: Api,
) -> tuple[str, str]:
    """Run the scorer's own aligner on the proposal FASTA vs the WT
    sequence from GPCRdb, and predict whether it would pass the A3
    chain-picker's ≥0.70 identity + ≥200 matched-residue gate.

    Skipped when the proposal's ``partner_perturbation`` is non-wt —
    chimeric / truncated / designed / shuffled specs have low identity
    to WT by design and would produce false positives here. The A3 gate
    at score time still runs on the RECEPTOR chain of the prediction,
    not the perturbed partner, so pre-check on the receptor's own FASTA
    is still meaningful; but the analyst who submitted a non-wt
    perturbation is telling us the low identity is intentional.
    """
    if partner_perturbation and partner_perturbation != "wt":
        return "pass", f"skipped: non-wt perturbation ({partner_perturbation})"
    up = receptor_slug.strip().upper()
    if up not in KNOWN_RECEPTORS:
        return "pass", "unknown receptor; A6 will fire before A3 is reached"
    entry_name = KNOWN_RECEPTORS[up]
    try:
        aset = resolve_anchors(api, entry_name)
    except Exception as e:  # pragma: no cover
        return "pass", f"could not resolve anchors ({type(e).__name__}): skipping PC5"
    # Build the WT sequence dict {uniprot_pos: one_letter_aa}. `resolve_anchors`
    # already used the residues/extended payload; we re-fetch it via the same
    # Api call inside `get_generic_numbers`. That call is cached — no extra
    # network traffic after the first invocation.
    from scorer.bw_numbering import get_generic_numbers
    from scorer.structure import STD_AA
    bw_map = get_generic_numbers(api, entry_name)
    wt_seq: dict[int, str] = {
        int(pos): str(info["aa"])
        for pos, info in bw_map.items()
        if info.get("aa") and info["aa"] in STD_AA
    }
    residues = _fasta_to_mock_residues(fasta_seq)
    match = _score_aligned(residues, wt_seq)
    if match is None:
        return (
            "warn_A3",
            f"aligner found no matching block between the FASTA and WT — "
            f"A3WrongChain would fire at score time (chain identity below "
            f"the minimum matching-block threshold).",
        )
    if match.identity < _A3_MIN_IDENTITY or match.n_residues_matched < _A3_MIN_MATCHED:
        return (
            "warn_A3",
            f"aligner reports identity={match.identity:.2%}, matched="
            f"{match.n_residues_matched} — below the A3 gate "
            f"(≥{_A3_MIN_IDENTITY:.0%} identity, ≥{_A3_MIN_MATCHED} matched). "
            f"At score time A3WrongChain would fire. Likely a wrong-species "
            f"or wrong-orthologue FASTA.",
        )
    return "pass", ""


# ---------------------------------------------------------------------------
# Orchestrator — run all 5 checks
# ---------------------------------------------------------------------------


def run_all_checks(
    receptor_slug: str,
    species: str,
    fasta_seq: str,
    partner_perturbation: str,
    ref_species_map: dict[str, set[str]],
    api: Api,
) -> dict[str, tuple[str, str]]:
    """Run every pre-check on one proposal spec and return the dict.

    Returns ``{"pc1": (status, reason), ..., "pc5": (status, reason)}``.
    Every value is either ``("pass", "")`` or ``("warn_A<N>", reason)``
    or ``("pass", "skipped: <why>")`` when the check does not apply.

    The caller aggregates these into a single ``pre_check_status`` for
    the manifest row (``pass`` if all five pass; ``warn_A<N>`` when
    exactly one warns; ``warn_multiple`` when two or more warn).
    """
    return {
        "pc1": pc1_receptor_known(receptor_slug),
        "pc2": pc2_species_ref_exists(receptor_slug, species, ref_species_map),
        "pc3": pc3_fasta_covers_anchors(receptor_slug, fasta_seq, api),
        "pc4": pc4_identity_anchors_match(receptor_slug, fasta_seq, api),
        "pc5": pc5_identity_matched_pass(
            receptor_slug, fasta_seq, partner_perturbation, api
        ),
    }


def summarise(results: dict[str, tuple[str, str]]) -> str:
    """Aggregate a run_all_checks() result into a single manifest tag.

    Values:
      - "pass"           — every check returned pass
      - "warn_A<N>"      — exactly one check warned (A1/A2/A3/A5/A6)
      - "warn_multiple"  — two or more checks warned; the reasons stay
                           in the per-row provenance JSON emitted by
                           gpcr-propose (Layer 2)
    """
    warns = [(k, v[0]) for k, v in results.items() if v[0].startswith("warn_")]
    if not warns:
        return "pass"
    if len(warns) == 1:
        return warns[0][1]
    return "warn_multiple"
