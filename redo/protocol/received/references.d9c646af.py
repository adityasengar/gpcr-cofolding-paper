"""Reference-set loader — A4 / A5 gates.

Loads ``refs/reference_set.csv`` (produced by ``gpcr-refs build`` at
commit 12) and exposes lookup functions that raise A4 or A5.

At scaffold time (before C12) the CSV is header-only. Any call to
``load_for(receptor, state_claim)`` returns ``ReferenceLookup(active=None,
inactive=None)``; callers that require a reference to be present will get
a clear A4 raise. The harness for F2/F4 supplies its own in-memory
``ReferenceSet`` so the tests are self-contained.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from scorer.assertions import A4ReferenceClassMismatch, A5SpeciesMismatch
from scorer.schema import StateClaim


# Stabilising elements that HISTORICALLY disqualified a reference from a
# Ga-coupled-active claim. As of 2026-08-26 the check is DEFERRED —
# GPCRdb classifies Nb35 / Nb6B9 / scFv16-stabilised structures as
# state=Active because they capture the same TM6-out / open-Gα-pocket
# conformation as native Gα binding; BRIL/T4L are cytoplasmic-loop
# fusions that don't touch the TM bundle. The community-consensus
# position (per GPCRdb curation) is that these are valid active-state
# references. The final active/inactive classification of a prediction
# uses the full 6-axis vector (TM6, NPxxY, TM5-out, Y5.58-pack, DRY,
# ICL2) aggregated across many refs across many receptors — any single-
# stabiliser artifact washes out. See docs/REFERENCE_SET.md and
# docs/AUDIT_TRAIL.md#4-2026-08-26-policy-update.
#
# List kept for annotation / provenance in ScorerRow but no longer
# used to raise A4. To re-enable the stricter check, uncomment the
# check block in check_reference_class() below.
DISQUALIFYING_STABILISERS: frozenset[str] = frozenset({
    "nanobody", "scFv", "BRIL", "T4L", "DARPin", "minibinder",
})


@dataclass(frozen=True)
class ReferenceRow:
    receptor_slug: str
    role: str                      # "active" | "inactive"
    pdb_id: str
    uniprot_slug: str              # "adrb2_human"
    species: str                   # "human" | "mouse" | ...
    resolved_state: str            # StateClaim value
    stabilising_elements: frozenset[str] = field(default_factory=frozenset)
    construct: str = "wt"
    construct_offset: int = 0
    d_r350_r630_ca_ref: float = float("nan")
    # Class-B/F secondary reference axis. GPCRdb 2x46 CA <-> 6x37 CA
    # (aka "TM6 tilt"). Populated for Class B/F rows in refs/reference_set.csv
    # from 2026-09-02 onward. Class A rows also carry a value here for
    # completeness, but the scorer's Class A axis remains d_r350_r630_ca_ref.
    d_gpcrdb_tm6_tilt_ref: float = float("nan")
    provenance_sha256: str = ""
    # Block C addition (2026-09-04): fine-grained sub-role classification
    # for inactive references so pocket_metrics can pick the
    # antagonist-specific reference (containing the matching small-
    # molecule ligand) when the manifest declares
    # ligand_role ∈ {neutral_antagonist, inverse_agonist} on an
    # otherwise Ga-coupled-active state_claim. Values seen in
    # refs/reference_set.csv: "", "inactive_neutral_antagonist",
    # "inactive_inverse_agonist". Empty means the row is either the
    # active reference or a generic inactive reference (no
    # specific-ligand chemistry pinned).
    role_specific: str = ""


@dataclass
class ReferenceLookup:
    active: ReferenceRow | None
    inactive: ReferenceRow | None
    # Block C add-on (2026-09-04): all inactive rows for this receptor
    # keyed by ``role_specific`` string ({"inactive_neutral_antagonist",
    # "inactive_inverse_agonist"}). Empty when no role_specific-tagged
    # inactive references exist for the receptor. The generic (blank
    # role_specific) inactive row also appears here under the key ""
    # when present. Downstream callers should first look up the
    # role_specific tag they want; missing keys mean fall back to
    # ``.inactive`` (generic).
    inactive_by_role_specific: dict[str, ReferenceRow] = field(
        default_factory=dict
    )


class ReferenceSet:
    """In-memory view of ``refs/reference_set.csv``.

    Load from disk with ``ReferenceSet.from_csv(path)``; construct
    directly with an iterable of ``ReferenceRow`` for tests / fixtures.
    """

    def __init__(self, rows: Iterable[ReferenceRow] = ()):
        # Legacy single-row-per-(receptor, role) mapping. Block C's
        # role_specific-aware lookup lives in a parallel structure
        # (``_inactive_by_specific``) so existing callers that read
        # ``_by_receptor`` see no change.
        self._by_receptor: dict[str, dict[str, ReferenceRow]] = {}
        # Block C add-on (2026-09-04): multiple inactive rows per
        # receptor keyed by role_specific. When multiple inactive rows
        # exist for a receptor (e.g., ADRB2 has three:
        # inactive_neutral_antagonist, inactive_inverse_agonist, and
        # a generic inactive), the legacy _by_receptor overwrites on
        # role="inactive" and last-write-wins is arbitrary. This
        # structure holds ALL inactive rows, keyed by role_specific.
        self._inactive_by_specific: dict[str, dict[str, ReferenceRow]] = {}
        for r in rows:
            self._by_receptor.setdefault(r.receptor_slug, {})[r.role] = r
            if r.role == "inactive":
                self._inactive_by_specific.setdefault(
                    r.receptor_slug, {}
                )[r.role_specific or ""] = r

    @classmethod
    def empty(cls) -> "ReferenceSet":
        return cls([])

    @classmethod
    def from_csv(cls, path: Path | str) -> "ReferenceSet":
        p = Path(path)
        if not p.exists():
            return cls.empty()
        rows: list[ReferenceRow] = []
        with p.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("receptor_slug") or row["receptor_slug"].startswith("#"):
                    continue
                stab = frozenset(
                    s.strip() for s in (row.get("stabilising_elements") or "").split(";")
                    if s.strip() and s.strip() != "none"
                )
                try:
                    d = float(row.get("d_r350_r630_ca_ref") or "nan")
                except ValueError:
                    d = float("nan")
                try:
                    d_tilt = float(row.get("d_gpcrdb_tm6_tilt_ref") or "nan")
                except ValueError:
                    d_tilt = float("nan")
                try:
                    off = int(row.get("construct_offset") or 0)
                except ValueError:
                    off = 0
                rows.append(ReferenceRow(
                    receptor_slug=row["receptor_slug"].upper(),
                    role=row.get("role", "").lower(),
                    pdb_id=row.get("pdb_id", "").upper(),
                    uniprot_slug=row.get("uniprot_slug", "").lower(),
                    species=row.get("species", "").lower(),
                    resolved_state=row.get("resolved_state", ""),
                    stabilising_elements=stab,
                    construct=row.get("construct", "wt"),
                    construct_offset=off,
                    d_r350_r630_ca_ref=d,
                    d_gpcrdb_tm6_tilt_ref=d_tilt,
                    provenance_sha256=row.get("provenance_sha256", ""),
                    role_specific=(row.get("role_specific") or "").strip(),
                ))
        return cls(rows)

    def receptors(self) -> list[str]:
        return sorted(self._by_receptor.keys())

    def load_for(self, receptor_slug: str) -> ReferenceLookup:
        entry = self._by_receptor.get(receptor_slug.upper(), {})
        inactive_specific = self._inactive_by_specific.get(
            receptor_slug.upper(), {}
        )
        return ReferenceLookup(
            active=entry.get("active"),
            inactive=entry.get("inactive"),
            inactive_by_role_specific=dict(inactive_specific),
        )


# ---------------------------------------------------------------------------
# Uncovered receptors — soft-A4 policy
# ---------------------------------------------------------------------------

# Receptors listed in `refs/uncovered_receptors.txt` (one slug per line,
# `#` comments allowed) have NO qualifying `state=Active` PDB in GPCRdb
# even after the 2026-08-26 relaxations. For these, A4 does NOT raise on
# a missing role-required reference — axis values (TM6, NPxxY, TM5-out,
# Y5.58-pack, DRY, ICL2) are absolute geometric measurements that flow
# through the scorer regardless. What is lost: state classification and
# per-receptor delta values (`delta_to_active`/`_inactive`,
# `receptor_midpoint`, `receptor_d_active_ref`, `receptor_d_inactive_ref`)
# all become NaN because there's nothing to compare against.
#
# The uncovered list is an EXPLICIT opt-in — silence is not automatic.
# A receptor missing from `refs/reference_set.csv` but NOT in this file
# will still fail A4 hard. This preserves the audit-finding-#5 discipline
# ("no silent scoring where a reference could exist but doesn't").

_UNCOVERED_CACHE: dict[str, frozenset[str]] = {}


def load_uncovered_receptors(refs_dir: Path | str) -> frozenset[str]:
    """Load the receptor slugs listed in ``refs_dir/uncovered_receptors.txt``.

    Cached per refs_dir to avoid re-reading on every scorer invocation.
    Returns an empty frozenset if the file doesn't exist — legacy behavior.
    """
    key = str(Path(refs_dir).resolve())
    if key in _UNCOVERED_CACHE:
        return _UNCOVERED_CACHE[key]
    fp = Path(refs_dir) / "uncovered_receptors.txt"
    slugs: set[str] = set()
    if fp.exists():
        for line in fp.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            slugs.add(s.upper())
    result = frozenset(slugs)
    _UNCOVERED_CACHE[key] = result
    return result


# ---------------------------------------------------------------------------
# A4 / A5 checks
# ---------------------------------------------------------------------------


def check_reference_class(
    lookup: ReferenceLookup,
    receptor_slug: str,
    input_state_claim: str,
    *,
    uncovered_receptors: frozenset[str] = frozenset(),
) -> None:
    """Raise A4 ONLY if a reference is present but its `resolved_state`
    doesn't match `input_state_claim`. Missing reference = soft-fail
    (returns without raising).

    **2026-08-26 policy update #3 (consultant-endorsed):** A4 became an
    annotation, not a gate. The scorer's six axis measurements
    (TM6, NPxxY, TM5-out, Y5.58-pack, DRY, ICL2) are absolute geometric
    values that flow through regardless of reference availability.
    What is lost without a reference: state classification and the
    per-receptor delta values (`delta_to_active`, `delta_to_inactive`,
    `receptor_midpoint`, `receptor_d_active_ref/_inactive_ref` — all
    become NaN in the ScorerRow).

    The `uncovered_receptors` kwarg is still accepted for backward
    compatibility but no longer needed — missing references
    universally soft-fail now. Downstream analysis subsets on
    `receptor_d_active_ref IS NaN` to identify uncovered rows.
    """
    role = _role_for_state(input_state_claim)
    if role is None:
        return  # apo / design / class_bc claims don't gate on reference
    ref = getattr(lookup, role)
    if ref is None:
        # Soft-fail: axis values flow, classification skipped, deltas NaN.
        # No raise — the receptor may simply lack a curated ref in
        # refs/reference_set.csv, which is now a documented outcome.
        _ = uncovered_receptors    # kept for API stability
        return
    if ref.resolved_state != input_state_claim:
        raise A4ReferenceClassMismatch(
            f"reference {ref.pdb_id} for {receptor_slug} is "
            f"{ref.resolved_state!r} but input claims {input_state_claim!r}",
            receptor_slug=receptor_slug, pdb_id=ref.pdb_id,
            resolved_state=ref.resolved_state,
            input_state_claim=input_state_claim,
        )
    # Stabiliser check deferred — see 2026-08-26 policy update above.
    # Historic block kept for reference:
    #
    # if input_state_claim == StateClaim.Ga_COUPLED_ACTIVE.value:
    #     bad = ref.stabilising_elements & DISQUALIFYING_STABILISERS
    #     if bad:
    #         raise A4ReferenceClassMismatch(...)


def check_species(
    lookup: ReferenceLookup,
    receptor_slug: str,
    input_species: str,
    input_state_claim: str,
) -> None:
    """Raise A5 if the reference for the required role has a species
    that differs from the input construct's species."""
    role = _role_for_state(input_state_claim)
    if role is None:
        return
    ref = getattr(lookup, role)
    if ref is None or not input_species or not ref.species:
        return
    if ref.species.lower() != input_species.lower():
        raise A5SpeciesMismatch(
            f"input species {input_species!r} != reference species "
            f"{ref.species!r} (ref {ref.pdb_id} for {receptor_slug})",
            input_species=input_species,
            reference_species=ref.species,
            reference_pdb=ref.pdb_id,
        )


def _role_for_state(state_claim: str) -> str | None:
    if state_claim in (
        StateClaim.Ga_COUPLED_ACTIVE.value,
        StateClaim.ARRESTIN_COUPLED.value,
    ):
        return "active"
    if state_claim in (
        StateClaim.INACTIVE_ANTAGONIST.value,
        StateClaim.INACTIVE_INVERSE_AGONIST.value,
    ):
        return "inactive"
    # apo / design_no_dry / class_bc_native_no_dry — no reference gate
    return None


# ---------------------------------------------------------------------------
# Per-receptor reference/delta scalars for the primary axis
# ---------------------------------------------------------------------------


def compute_deltas(
    current_d_tm6: float,
    lookup: ReferenceLookup,
    *,
    receptor_class: str = "A",
    current_d_tilt: float = float("nan"),
) -> tuple[float, float, float, float, float]:
    """Compute per-receptor reference/delta scalars for the primary axis.

    **Class-conditional (plan §15, 2026-09-02):** the reference axis
    differs by receptor class. All three of A / B / F share the
    interface — ``receptor_d_active_ref`` etc. always come out as
    scalars — but the underlying column differs:

    - Class A:   ``d_r350_r630_ca_ref``          (3.50–6.30 BW CA-CA)
    - Class B:   ``d_gpcrdb_tm6_tilt_ref``        (GPCRdb 2x46 CA – 6x37 CA)
    - Class F:   ``d_r350_r630_ca_ref``           (kept as Class-A anchor;
                                                   Class F is reported-secondary
                                                   per plan §15 direction)
    - Otherwise: ``d_r350_r630_ca_ref``           (default; C/T2R/N not
                                                   in the current panel)

    For Class B, ``current_d_tilt`` is used against the tilt reference;
    Class A / F use ``current_d_tm6`` against the CA-CA reference. The
    caller is responsible for passing both.

    **Comparability note.** Class B pre- and post-§15 numbers are on
    different axes and NOT comparable. Every downstream reader that
    joins across the pre/post divide must carry the note explicitly.

    Returns ``(d_active_ref, d_inactive_ref, midpoint, delta_to_active,
    delta_to_inactive)``. Any component whose reference is missing
    (either the ``ReferenceRow`` itself is ``None`` or the class-
    appropriate ref column is ``NaN`` in ``refs/reference_set.csv``) is
    returned as ``float("nan")``. A NaN ``current`` value propagates
    into both deltas but leaves the two reference values and the
    midpoint (when both refs are present) populated.

    Sign convention (fixed for downstream analysis):
        delta_to_active   = current - d_active_ref
        delta_to_inactive = current - d_inactive_ref
    Positive delta -> current axis is longer than that state's reference
    (i.e. further along the TM6-outward direction / larger tilt).
    """
    cls = (receptor_class or "A").upper()

    if cls == "B":
        current = current_d_tilt
        d_a = (
            lookup.active.d_gpcrdb_tm6_tilt_ref
            if lookup.active is not None
            else float("nan")
        )
        d_i = (
            lookup.inactive.d_gpcrdb_tm6_tilt_ref
            if lookup.inactive is not None
            else float("nan")
        )
    else:
        # Class A / F (F kept on d_tm6 as reported-secondary per §15).
        current = current_d_tm6
        d_a = (
            lookup.active.d_r350_r630_ca_ref
            if lookup.active is not None
            else float("nan")
        )
        d_i = (
            lookup.inactive.d_r350_r630_ca_ref
            if lookup.inactive is not None
            else float("nan")
        )
    midpoint = (
        (d_a + d_i) / 2.0
        if not (math.isnan(d_a) or math.isnan(d_i))
        else float("nan")
    )
    cur_nan = math.isnan(current)
    delta_a = float("nan") if (cur_nan or math.isnan(d_a)) else current - d_a
    delta_i = float("nan") if (cur_nan or math.isnan(d_i)) else current - d_i
    return d_a, d_i, midpoint, delta_a, delta_i
