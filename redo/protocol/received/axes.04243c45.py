"""Per-axis geometry.

Every ``compute_all_axes`` call emits the full vector. There is no scalar
return option and no threshold branching inside this module — thresholds
live in ``refs/state_thresholds.csv`` and are consulted only at
classification time in ``scorer/references.py``. Audit finding #3
(5HT2 subfamily undiscriminable on a single-coordinate metric) is the
reason multi-axis is a hard invariant.

**Every function here takes ``VerifiedModel`` — not UnverifiedUniProtModel.**
Founding premise (docs/AUDIT_TRAIL.md): A1/A2/A3 cannot be bypassed. The
type constraint is checked at runtime via ``isinstance`` on the entry
point ``compute_all_axes``; individual axis functions dereference
``.residues``/``.ca()`` via the same read-only view.

Axes emitted (all in ångströms unless noted):

  d_tm6_r350_r630_ca                R3.50 CA -- 6.30 CA
  d_npxxy_y558_y753_ca              Y5.58 CA -- Y7.53 CA
                                    (CA-CA, not OH-OH — see w56 correction
                                    in docs/AUDIT_TRAIL.md; the frozen code
                                    misread the OH-OH literature threshold)
  d_tm5_outward_r350_r558_ca        R3.50 CA -- 5.58 CA (used to be TM5-out)
  d_y558_pack_min_heavy             Y5.58 OH -> nearest heavy atom on TM3/6
  d_dry_sidechain_r350cz_e630oe1    R3.50 CZ -- 6.30 side-chain carboxyl O
  icl2_helical_frac                 residues 132..145 helicity fraction
                                    (approximated by (i, i+4) CA-CA in
                                    3.8..4.5 Å window)
  plddt_at_anchors                  per-anchor pLDDT (from B-factor field)
  plddt_mean                        mean pLDDT across the receptor chain

Anchors come from the AnchorSet embedded in the VerifiedModel; the
caller cannot pass a mismatched anchor set.
"""
from __future__ import annotations

import math
from typing import Any

import gemmi

from scorer.verified import VerifiedModel


NaN = float("nan")


# ---------------------------------------------------------------------------
# AXIS_APPLICABILITY — which GPCR classes each axis is calibrated for.
#
# Added in the class-aware rescore work (v3.7). Purely annotative — no axis
# computation branches on this table. The measurement still runs whenever
# the required atoms are physically present (a Class-B receptor with an
# unexpected Tyr 5.58 would still get a `d_y558_pack_min_heavy` value).
# The `not_applicable_axes_for(class)` helper below produces the per-row
# annotation so a NaN reads as "not applicable to this class" rather than
# "measurement failed".
#
# Class-A canonical axes require Class-A residue chemistry (DRY R at 3.50,
# NPxxY Tyr at 7.53, Y at 5.58, E/D at 6.30):
#   d_y558_pack_min_heavy       — needs Y5.58 hydroxyl
#   d_dry_sidechain_r350cz_e630oe1 — needs R3.50 guanidinium + E/D 6.30 carboxyl
#   d_npxxy_y558_y753_ca        — NPxxY motif is Class A
#   d_tm5_outward_r350_r558_ca  — TM5-outward interpretation is Class A
#
# Universal geometric axes measure a valid CA-CA distance in any class;
# only the biological interpretation of the number changes across classes:
#   d_tm6_r350_r630_ca          — TM6-out marker, all classes
#
# icl2_helical_frac — ICL2 helicity is well-established for Class A and B.
# Class C/F use different intracellular loops; the axis measures a real
# helicity but classification thresholds are not calibrated for those.
# ---------------------------------------------------------------------------

AXIS_APPLICABILITY: dict[str, frozenset[str]] = {
    "d_tm6_r350_r630_ca":             frozenset({"A", "B", "C", "F", "T2R"}),
    "d_npxxy_y558_y753_ca":           frozenset({"A"}),
    "d_tm5_outward_r350_r558_ca":     frozenset({"A"}),
    "d_y558_pack_min_heavy":          frozenset({"A"}),
    "d_dry_sidechain_r350cz_e630oe1": frozenset({"A"}),
    "icl2_helical_frac":              frozenset({"A", "B"}),
}


def not_applicable_axes_for(receptor_class: str) -> tuple[str, ...]:
    """Return the axis names NOT calibrated for a given GPCR class.

    Used to populate the `not_applicable_axes` annotation column on
    ScorerRow. Downstream analyses read this to distinguish an axis NaN
    caused by class-inapplicability (documented, expected) from an axis
    NaN caused by measurement failure (an anchor CA missing on a chain
    that should have it — worth investigating).

    A class not in AXIS_APPLICABILITY (e.g. "N" for calmodulin, or an
    unrecognised class token) returns an empty tuple — every axis is
    reported as "applicable" and any NaN falls back to the historic
    reading ("physics didn't apply here" — the caller can inspect the
    residue chemistry columns).
    """
    if not receptor_class:
        return ()
    out: list[str] = []
    for axis, classes in AXIS_APPLICABILITY.items():
        if receptor_class not in classes:
            out.append(axis)
    return tuple(sorted(out))


def _dist(a: gemmi.Position | None, b: gemmi.Position | None) -> float:
    if a is None or b is None:
        return NaN
    return a.dist(b)


def _ca(model: VerifiedModel, uniprot_pos: int) -> gemmi.Position | None:
    r = model.residues.get(uniprot_pos)
    if r is None:
        return None
    atom = r.find_atom("CA", "\0")
    return atom.pos if atom is not None else None


def _atom(model: VerifiedModel, uniprot_pos: int, name: str) -> gemmi.Atom | None:
    r = model.residues.get(uniprot_pos)
    if r is None:
        return None
    return r.find_atom(name, "\0")


def _anchor_pos(model: VerifiedModel, label: str) -> int | None:
    a = model.anchor_set.anchors.get(label)
    return None if a is None else a.uniprot_pos


# ---------------------------------------------------------------------------
# individual axes
# ---------------------------------------------------------------------------


def d_tm6_r350_r630_ca(model: VerifiedModel) -> float:
    """R3.50 CA -- 6.30 CA. The classic TM6-outward marker."""
    p350 = _anchor_pos(model, "3.50")
    p630 = _anchor_pos(model, "6.30")
    if p350 is None or p630 is None:
        return NaN
    return _dist(_ca(model, p350), _ca(model, p630))


def d_npxxy_y558_y753_ca(model: VerifiedModel) -> float:
    """Y5.58 CA -- Y7.53 CA.

    CA-CA, NOT OH-OH — the frozen scorer misread a literature OH-OH
    threshold as CA-CA and produced retracted Wave 55 verdicts. See
    docs/AUDIT_TRAIL.md.
    """
    p558 = _anchor_pos(model, "5.58")
    p753 = _anchor_pos(model, "7.53")
    if p558 is None or p753 is None:
        return NaN
    return _dist(_ca(model, p558), _ca(model, p753))


def d_npxxy_y558_y753_oh(model: VerifiedModel) -> float:
    """Y5.58 side-chain OH -- Y7.53 side-chain OH, in Å.

    Companion to ``d_npxxy_y558_y753_ca``. Literature NPxxY-collapse
    thresholds (Weis & Kobilka 2018 and follow-ups) are quoted on OH-OH
    at ~7–8 Å; PREREG §10 requires this column so a literature-derived
    threshold can be applied without ambiguity. The CA-CA column stays
    alongside as the frozen-scorer measurement.

    Returns NaN if either Tyr is absent from the model, or if the OH
    atom is not resolved (Y5.58 → non-Tyr point mutant, or an atom-level
    truncation).
    """
    p558 = _anchor_pos(model, "5.58")
    p753 = _anchor_pos(model, "7.53")
    if p558 is None or p753 is None:
        return NaN
    r558 = model.residues.get(p558)
    r753 = model.residues.get(p753)
    if r558 is None or r753 is None:
        return NaN
    oh558 = r558.find_atom("OH", "\0")
    oh753 = r753.find_atom("OH", "\0")
    if oh558 is None or oh753 is None:
        return NaN
    return oh558.pos.dist(oh753.pos)


def d_tm5_outward_r350_r558_ca(model: VerifiedModel) -> float:
    """R3.50 CA -- 5.58 CA. Proxy for TM5-outward displacement."""
    p350 = _anchor_pos(model, "3.50")
    p558 = _anchor_pos(model, "5.58")
    if p350 is None or p558 is None:
        return NaN
    return _dist(_ca(model, p350), _ca(model, p558))


def d_y558_pack_min_heavy(model: VerifiedModel) -> float:
    """Y5.58 side-chain OH -> nearest heavy atom on TM3 or TM6 (excluding
    Y5.58 itself). Active-state Y5.58 packs into a TM3/6 hydrophobic pocket.
    """
    p558 = _anchor_pos(model, "5.58")
    if p558 is None:
        return NaN
    r558 = model.residues.get(p558)
    if r558 is None:
        return NaN
    oh = r558.find_atom("OH", "\0")
    if oh is None:
        return NaN
    # sweep candidate TM3+TM6 residues around anchor 3.50 and 6.30
    p350 = _anchor_pos(model, "3.50")
    p630 = _anchor_pos(model, "6.30")
    candidate_positions: list[int] = []
    if p350 is not None:
        candidate_positions.extend(range(p350 - 3, p350 + 4))
    if p630 is not None:
        candidate_positions.extend(range(p630 - 3, p630 + 4))
    best = NaN
    for pos in candidate_positions:
        r = model.residues.get(pos)
        if r is None or pos == p558:
            continue
        for at in r:
            if at.element.name == "H":
                continue
            if at.name == "CA":
                continue
            d = oh.pos.dist(at.pos)
            if math.isnan(best) or d < best:
                best = d
    return best


def d_dry_sidechain_r350cz_e630oe1(model: VerifiedModel) -> float:
    """R3.50 guanidinium CZ -- 6.30 side-chain carboxyl (OE1 for E, OD1 for D)
    if the 6.30 residue is E or D; otherwise NaN (no ionic-lock geometry
    defined for non-E/D 6.30).
    """
    p350 = _anchor_pos(model, "3.50")
    p630 = _anchor_pos(model, "6.30")
    if p350 is None or p630 is None:
        return NaN
    r350 = model.residues.get(p350)
    r630 = model.residues.get(p630)
    if r350 is None or r630 is None:
        return NaN
    cz = r350.find_atom("CZ", "\0")
    if cz is None:
        return NaN
    for atom_name in ("OE1", "OE2", "OD1", "OD2"):
        oe = r630.find_atom(atom_name, "\0")
        if oe is not None:
            return cz.pos.dist(oe.pos)
    return NaN


# ---------------------------------------------------------------------------
# Literature-derived cross-class activation metrics (PREREG §2b + §2c-revised).
#
# These are ADDITIVE geometry columns — the current single-metric NPxxY-OH
# predicate does NOT depend on them (see scorer/switch_signal.py::
# MotifThresholds, user-locked). Emitted here for downstream enrichment
# after correlation review.
#
# Every function returns NaN if any required BW anchor is not resolvable
# via GPCRdb for this receptor (Class-A-only anchors on a Class-B receptor,
# or vice-versa, will legitimately be absent). NaN also propagates through
# residue-not-in-model and CA-not-resolved paths — never a default value.
# ---------------------------------------------------------------------------


def _ca_at_bw(model: VerifiedModel, bw_label: str) -> "gemmi.Position | None":
    """Return the Cα gemmi.Position at BW label ``bw_label``, or None if
    the anchor is missing from GPCRdb, the residue is not modelled, or
    its CA atom is absent from the coordinate set.

    Unlike the DRY/NPxxY axes, the literature metrics only require the
    Cα coordinate — they carry no residue-identity constraint (the
    A100 formula and TM6 tilt are defined at BW positions regardless
    of which residue occupies the position in the target receptor).
    """
    pos = _anchor_pos(model, bw_label)
    if pos is None:
        return None
    return _ca(model, pos)


def d_gpcrdb_tm6_tilt_246_637_ca(model: VerifiedModel) -> float:
    """GPCRdb primary cross-class TM6 tilt marker: 2.46 CA -- 6.37 CA (Å).

    Per GPCRdb's own activation-classifier docs, this pair is the primary
    cross-class TM6-tilt readout for Class A/B/C. Class F uses a different
    measure. NaN when 2.46 or 6.37 is absent from GPCRdb for the receptor
    or the CA is missing from the model.
    """
    return _dist(_ca_at_bw(model, "2.46"), _ca_at_bw(model, "6.37"))


# A100 activation index (Ibrahim, Wifling, Clark, J. Chem. Inf. Model.
# 2019, 59(9), 3938-3945; DOI 10.1021/acs.jcim.9b00604).
#
# Five Cα-Cα distances (Å) in the paper's canonical order:
#   c1: 1.53 -- 7.55  (TM1-TM7)
#   c2: 2.50 -- 3.37  (TM2-TM3)
#   c3: 3.42 -- 4.42  (TM3-TM4)
#   c4: 5.66 -- 6.34  (TM5-TM6 outward-swing)
#   c5: 6.58 -- 7.35  (TM6-TM7 extracellular tip)
#
# Composite:
#   A100 = -14.43*c1 - 7.62*c2 + 9.11*c3 - 6.32*c4 - 5.22*c5 + 278.88
#
# Two-state threshold: inactive < 25, active > 25.
# Three-state:         inactive < 0, intermediate 0-55, active > 55.
# Validation: 268 X-ray structures, 50 unique Class-A receptors;
#             two-state accuracy 94% actives / 99% inactives.

_A100_PAIRS: tuple[tuple[str, str], ...] = (
    ("1.53", "7.55"),
    ("2.50", "3.37"),
    ("3.42", "4.42"),
    ("5.66", "6.34"),
    ("6.58", "7.35"),
)

_A100_COEFFS: tuple[float, ...] = (-14.43, -7.62, 9.11, -6.32, -5.22)
_A100_INTERCEPT: float = 278.88


def _a100_component(model: VerifiedModel, i: int) -> float:
    """One A100 component (Cα-Cα distance for the i-th BW pair, 0-indexed)."""
    a, b = _A100_PAIRS[i]
    return _dist(_ca_at_bw(model, a), _ca_at_bw(model, b))


def a100_component_1_ca(model: VerifiedModel) -> float:
    """A100 component 1: 1.53 CA -- 7.55 CA (Å). NaN if either absent."""
    return _a100_component(model, 0)


def a100_component_2_ca(model: VerifiedModel) -> float:
    """A100 component 2: 2.50 CA -- 3.37 CA (Å). NaN if either absent."""
    return _a100_component(model, 1)


def a100_component_3_ca(model: VerifiedModel) -> float:
    """A100 component 3: 3.42 CA -- 4.42 CA (Å). NaN if either absent."""
    return _a100_component(model, 2)


def a100_component_4_ca(model: VerifiedModel) -> float:
    """A100 component 4: 5.66 CA -- 6.34 CA (Å). NaN if either absent."""
    return _a100_component(model, 3)


def a100_component_5_ca(model: VerifiedModel) -> float:
    """A100 component 5: 6.58 CA -- 7.35 CA (Å). NaN if either absent."""
    return _a100_component(model, 4)


def a100_index(model: VerifiedModel) -> float:
    """A100 composite index (Ibrahim/Wifling/Clark 2019).

    NaN when ANY of the five components is NaN — never substitute a
    default value. Downstream two-state cutoff: active if A100 > 25.
    """
    components: list[float] = []
    for i in range(5):
        c = _a100_component(model, i)
        if math.isnan(c):
            return NaN
        components.append(c)
    total = _A100_INTERCEPT
    for coeff, c in zip(_A100_COEFFS, components):
        total += coeff * c
    return total


def angle_class_b_tm6_kink_639_650_654_deg(model: VerifiedModel) -> float:
    """Class B TM6 kink angle (Kobayashi et al., Nature 2023).

    Cα-Cα-Cα angle at BW positions 6.39, 6.50, 6.54 with vertex at 6.50,
    in degrees. Active state ≈ 90° (sharp kink; PxxG motif fully bent);
    inactive/moderate ≈ 145°. Class B's real activation switch since
    NPxxY and DRY don't exist in Class B1.

    NaN if any of the three anchors is not resolvable via GPCRdb, if
    any CA is missing from the model, or if degenerate geometry (two
    vertices coincident) makes the angle undefined.

    Implementation uses the law of cosines so this function only ever
    calls ``.dist()`` on the three positions — no vector-arithmetic
    dependency on gemmi. Given the triangle with sides
    ``a = |v-a|``, ``c = |v-c|``, and ``ac = |a-c|`` (the opposite side
    to the vertex angle):

        cos(θ) = (a² + c² - ac²) / (2·a·c)
    """
    p_a = _ca_at_bw(model, "6.39")
    p_v = _ca_at_bw(model, "6.50")
    p_c = _ca_at_bw(model, "6.54")
    if p_a is None or p_v is None or p_c is None:
        return NaN
    a = p_a.dist(p_v)
    c = p_c.dist(p_v)
    ac = p_a.dist(p_c)
    if a == 0.0 or c == 0.0:
        return NaN
    cos_theta = (a * a + c * c - ac * ac) / (2.0 * a * c)
    # numerical guard for values marginally outside [-1, 1]
    if cos_theta > 1.0:
        cos_theta = 1.0
    elif cos_theta < -1.0:
        cos_theta = -1.0
    return math.degrees(math.acos(cos_theta))


def icl2_helical_frac(model: VerifiedModel, window: int = 14) -> float:
    """Approximated ICL2 helicity fraction over `window` residues C-terminal
    to R3.50. Counts (i, i+4) CA-CA distances in the α-helix range [3.8, 4.5] Å.
    """
    p350 = _anchor_pos(model, "3.50")
    if p350 is None:
        return NaN
    good = 0
    total = 0
    for i in range(p350 + 1, p350 + 1 + window):
        j = i + 4
        pi = _ca(model, i)
        pj = _ca(model, j)
        if pi is None or pj is None:
            continue
        total += 1
        d = pi.dist(pj)
        if 3.8 <= d <= 6.4:  # loose α-helix envelope for CA(i)-CA(i+4)
            good += 1
    if total == 0:
        return NaN
    return good / total


# ---------------------------------------------------------------------------
# pLDDT helpers
# ---------------------------------------------------------------------------


def _residue_plddt(r: gemmi.Residue) -> float:
    """Mean B-factor across residue atoms. For co-folding outputs (Boltz,
    OF3, Protenix, AF2) this is pLDDT."""
    vals = [at.b_iso for at in r if not math.isnan(at.b_iso)]
    if not vals:
        return NaN
    return sum(vals) / len(vals)


def plddt_at_anchors(model: VerifiedModel) -> dict[str, float]:
    out: dict[str, float] = {}
    for label, a in model.anchor_set.anchors.items():
        r = model.residues.get(a.uniprot_pos)
        out[label] = NaN if r is None else _residue_plddt(r)
    return out


def plddt_mean(model: VerifiedModel) -> float:
    vals: list[float] = []
    for r in model.residues.values():
        v = _residue_plddt(r)
        if not math.isnan(v):
            vals.append(v)
    if not vals:
        return NaN
    return sum(vals) / len(vals)


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------


def compute_all_axes(model: VerifiedModel) -> dict[str, Any]:
    """Full six-axis vector, always. No scalar-return option — this is a
    hard invariant of the scorer (audit #3).

    ``model`` MUST be a VerifiedModel produced by
    ``scorer.verified.verify()``. Passing an ``UnverifiedUniProtModel``
    is a TypeError. The lint additionally bans direct construction of
    the verified type from any file other than scorer/verified.py.
    """
    if not isinstance(model, VerifiedModel):
        raise TypeError(
            f"compute_all_axes requires a VerifiedModel; got {type(model).__name__}. "
            "Route through scorer.verified.verify(model, anchor_set)."
        )
    return {
        "d_tm6_r350_r630_ca": d_tm6_r350_r630_ca(model),
        "d_npxxy_y558_y753_ca": d_npxxy_y558_y753_ca(model),
        "d_npxxy_y558_y753_oh": d_npxxy_y558_y753_oh(model),
        "d_tm5_outward_r350_r558_ca": d_tm5_outward_r350_r558_ca(model),
        "d_y558_pack_min_heavy": d_y558_pack_min_heavy(model),
        "d_dry_sidechain_r350cz_e630oe1": d_dry_sidechain_r350cz_e630oe1(model),
        "icl2_helical_frac": icl2_helical_frac(model),
        "plddt_mean": plddt_mean(model),
        "plddt_at_anchors": plddt_at_anchors(model),
        # -- literature-derived cross-class metrics (additive, not in predicate)
        "d_gpcrdb_tm6_tilt_246_637_ca": d_gpcrdb_tm6_tilt_246_637_ca(model),
        "a100_component_1_ca": a100_component_1_ca(model),
        "a100_component_2_ca": a100_component_2_ca(model),
        "a100_component_3_ca": a100_component_3_ca(model),
        "a100_component_4_ca": a100_component_4_ca(model),
        "a100_component_5_ca": a100_component_5_ca(model),
        "a100_index": a100_index(model),
        "angle_class_b_tm6_kink_639_650_654_deg": angle_class_b_tm6_kink_639_650_654_deg(model),
    }


def observed_aas_at_anchors(model: VerifiedModel) -> dict[str, str]:
    """Observed 1-letter AA at each resolved anchor position on a VerifiedModel.

    Note: this is a diagnostic accessor. The A1 identity check itself runs
    inside ``scorer.verified.verify()`` — a VerifiedModel by definition has
    already passed that check.
    """
    from scorer.structure import STD_AA, one_letter
    out: dict[str, str] = {}
    for label, a in model.anchor_set.anchors.items():
        r = model.residues.get(a.uniprot_pos)
        if r is None:
            continue
        aa = one_letter(r.name)
        if aa in STD_AA:
            out[label] = aa
    return out
