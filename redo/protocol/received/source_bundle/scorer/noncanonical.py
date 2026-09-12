"""Non-canonical scorers — currently: calmodulin (CaM).

CaM is one of the three Tier-A claims from the frozen work — the two-lever
mechanism paper's positive control (198 rows demonstrating the co-folding
models CAN produce coherent bound-state predictions when the biology
supports one). The frozen implementation had a bug structurally identical
to the GPCR offset-137 bug (audit #4): ``CAM_ANCHORS = (20, 129)`` was
applied to every ``cam_*`` arm regardless of input identity.

This module replaces that with:

  1. per-input verification of amino-acid identity at the CaM anchors,
     using the canonical human CaM sequence (UniProt P0DP23, mature
     numbering with initial Met removed — D20 and D129 are aspartate);
  2. three validated axes computed with actual coordinate geometry, not
     a hardcoded pair;
  3. an explicit ``bw_derivation_source`` value distinct from the GPCR
     path (see scorer/schema.py::BWDerivationSource).

Axes:

  d_D20_D129_ca          extended ~40 Å (open), wrapped ~22 Å (closed)
  lobe_angle_deg         angle between N-lobe helix D (56-67) and
                         C-lobe helix G (128-138); ~180° open, <90° closed
  n_lobe_c_lobe_contacts number of Cα-Cα pairs in [4, 8] Å between the
                         two lobes; open ≈ 0, closed >> 0
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import gemmi

from scorer.assertions import A1AminoAcidIdentity, A2FASTATrunc, A3WrongChain
from scorer.schema import BWDerivationSource
from scorer.structure import (
    STD_AA,
    UniProtModel,
    _load_structure,
    one_letter,
    select_chain,
)


# ---------------------------------------------------------------------------
# CaM canonical sequence (human, mature numbering — no initial Met)
# ---------------------------------------------------------------------------

CAM_SEQ_MATURE: str = (
    "ADQLTEEQIAEFKEAFSLF"   # 1-19
    "DKDGDGTITT"            # 20-29   (D20)
    "KELGTVMRSL"            # 30-39
    "GQNPTEAELQ"            # 40-49
    "DMINEVDADG"            # 50-59
    "NGTIDFPEFL"            # 60-69
    "TMMARKMKDT"            # 70-79
    "DSEEEIREAF"            # 80-89
    "RVFDKDGNGY"            # 90-99
    "ISAAELRHVM"            # 100-109
    "TNLGEKLTDE"            # 110-119
    "EVDEMIREAD"            # 120-129 (D129)
    "IDGDGQVNYE"            # 130-139
    "EFVQMMTAK"             # 140-148
)


def _expected(pos: int) -> str:
    """Canonical AA at `pos` in mature human CaM (P0DP23 with initial Met
    removed). Raises KeyError if pos is out of range."""
    if pos < 1 or pos > len(CAM_SEQ_MATURE):
        raise KeyError(f"CaM position {pos} outside 1..{len(CAM_SEQ_MATURE)}")
    return CAM_SEQ_MATURE[pos - 1]


# Six anchor positions covering both lobes + linker. Expected AAs are
# derived from CAM_SEQ_MATURE so this dict cannot get out of sync with
# the reference sequence.
CAM_ANCHOR_POSITIONS: tuple[int, ...] = (20, 56, 67, 79, 129, 138)
CAM_ANCHOR_IDENTITIES: dict[int, str] = {
    pos: CAM_SEQ_MATURE[pos - 1] for pos in CAM_ANCHOR_POSITIONS
}


BW_DERIVATION_SOURCE = BWDerivationSource.UNIPROT_CANONICAL_CAM.value


# ---------------------------------------------------------------------------
# I/O — no GPCRdb; the CaM sequence is small enough to inline
# ---------------------------------------------------------------------------


def _cam_wt_seq() -> dict[int, str]:
    return {i + 1: aa for i, aa in enumerate(CAM_SEQ_MATURE)}


def build_cam_uniprot_model(path: str) -> UniProtModel:
    """Load PDB/CIF, pick the CaM chain by identity match, renumber
    to canonical mature CaM positions. Raises A3 if no chain matches."""
    wt = _cam_wt_seq()
    struct = _load_structure(path)
    match = select_chain(struct, wt, min_matched=100, min_identity=0.90)
    model = struct[0]
    ch = next(c for c in model if c.name == match.name)
    residues = [r for r in ch if one_letter(r.name) in STD_AA]
    renumbered: dict[int, gemmi.Residue] = {}
    for idx, r in enumerate(residues):
        pos = match.index_to_uniprot.get(idx)
        if pos is None:
            continue
        renumbered[pos] = r
    return UniProtModel(
        entry_name="calm_human",
        chain_name=match.name,
        residues=renumbered,
        identity=match.identity,
        matched=match.n_residues_matched,
    )


# ---------------------------------------------------------------------------
# A1 for CaM — per-input AA-identity check at the six anchors
# ---------------------------------------------------------------------------


def verify_cam_identity(model: UniProtModel) -> None:
    """Raise A1AminoAcidIdentity if any CaM anchor's observed AA doesn't
    match the canonical human CaM sequence (P0DP23, mature numbering).

    This is the countermeasure for audit #4 — hardcoded (20, 129) applied
    blindly to any chain. Now: (20, 129) is only applied if the observed
    residue at position 20 is genuinely D and the residue at position 129
    is genuinely D.
    """
    mismatches: dict[int, tuple[str, str]] = {}
    for pos, expected in CAM_ANCHOR_IDENTITIES.items():
        r = model.residues.get(pos)
        if r is None:
            continue  # A2 handles absence; here we only check present anchors
        observed = one_letter(r.name)
        if observed != expected:
            mismatches[pos] = (expected, observed)
    if mismatches:
        raise A1AminoAcidIdentity(
            f"CaM AA-identity mismatch at {list(mismatches)}: {mismatches}. "
            f"The input is probably not calmodulin, or is a mutant construct "
            f"— tag it with an explicit --state-claim design_no_dry equivalent "
            f"or route through refs/reference_pdbs.csv.",
            mismatches=mismatches, entry_name="calm_human",
        )


def verify_cam_coverage(model: UniProtModel) -> None:
    """Raise A2 if either state-anchor position (20 or 129) is missing."""
    missing = [p for p in (20, 129) if p not in model.residues]
    if missing:
        raise A2FASTATrunc(
            f"CaM input missing state anchor(s) at position(s) {missing}",
            missing=missing, entry_name="calm_human",
        )


# ---------------------------------------------------------------------------
# Axes
# ---------------------------------------------------------------------------


NaN = float("nan")


def _ca(model: UniProtModel, pos: int) -> gemmi.Position | None:
    r = model.residues.get(pos)
    if r is None:
        return None
    atom = r.find_atom("CA", "\0")
    return atom.pos if atom is not None else None


def _dist(a: gemmi.Position | None, b: gemmi.Position | None) -> float:
    if a is None or b is None:
        return NaN
    return a.dist(b)


def _vector(a: gemmi.Position, b: gemmi.Position) -> tuple[float, float, float]:
    return (b.x - a.x, b.y - a.y, b.z - a.z)


def _angle_deg(v1: tuple[float, float, float],
               v2: tuple[float, float, float]) -> float:
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    dot = x1*x2 + y1*y2 + z1*z2
    m1 = math.sqrt(x1*x1 + y1*y1 + z1*z1)
    m2 = math.sqrt(x2*x2 + y2*y2 + z2*z2)
    if m1 == 0 or m2 == 0:
        return NaN
    c = max(-1.0, min(1.0, dot / (m1 * m2)))
    return math.degrees(math.acos(c))


def d_D20_D129_ca(model: UniProtModel) -> float:
    """CaM state metric: D20 CA -- D129 CA.

    Extended ~40 Å (open); wrapped ~22 Å (target-bound).
    """
    return _dist(_ca(model, 20), _ca(model, 129))


def lobe_angle_deg(model: UniProtModel) -> float:
    """Angle between the N-lobe helix D axis (residues 56 -> 67) and the
    C-lobe helix G axis (residues 128 -> 138).

    ~180° (open) vs << 90° (closed / target-wrapped).
    """
    p56, p67 = _ca(model, 56), _ca(model, 67)
    p128, p138 = _ca(model, 128), _ca(model, 138)
    if not all([p56, p67, p128, p138]):
        return NaN
    return _angle_deg(_vector(p56, p67), _vector(p128, p138))


def n_lobe_c_lobe_contacts(model: UniProtModel,
                           lower: float = 4.0, upper: float = 8.0) -> int:
    """Cα-Cα pairs between residues 5-77 and residues 82-148 with distance
    in [lower, upper]. Zero when the two lobes are far apart (open); high
    when wrapped around a target."""
    n_lobe = [(p, model.residues.get(p)) for p in range(5, 78)]
    c_lobe = [(p, model.residues.get(p)) for p in range(82, 149)]
    n = 0
    for _, ra in n_lobe:
        if ra is None:
            continue
        a = ra.find_atom("CA", "\0")
        if a is None:
            continue
        for _, rb in c_lobe:
            if rb is None:
                continue
            b = rb.find_atom("CA", "\0")
            if b is None:
                continue
            d = a.pos.dist(b.pos)
            if lower <= d <= upper:
                n += 1
    return n


def compute_all_cam_axes(model: UniProtModel) -> dict[str, Any]:
    """Full CaM vector, always emitted."""
    return {
        "d_D20_D129_ca": d_D20_D129_ca(model),
        "lobe_angle_deg": lobe_angle_deg(model),
        "n_lobe_c_lobe_contacts": n_lobe_c_lobe_contacts(model),
    }


def observed_cam_aas_at_anchors(model: UniProtModel) -> dict[int, str]:
    out: dict[int, str] = {}
    for pos in CAM_ANCHOR_IDENTITIES:
        r = model.residues.get(pos)
        if r is not None:
            aa = one_letter(r.name)
            if aa in STD_AA:
                out[pos] = aa
    return out
