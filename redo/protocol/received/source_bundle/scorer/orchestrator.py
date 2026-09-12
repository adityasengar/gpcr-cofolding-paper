"""End-to-end orchestrator — composes A1..A6 into a single ScorerRow.

Two public entry points:

    row = run_scorer(input_path, receptor_hint, state_claim, out_dir, ...)
        Composes A6 -> A3 -> A2 -> A1 -> A4 -> A5 in a fixed order.
        Raises the ScorerAssertionError subclass on any failure. No
        internal try/except (grep-clean — see docs/ASSERTIONS.md).

    row = score_and_capture(...)
        Wraps run_scorer, catches at exactly ONE site the batch driver
        needs (never abort mid-corpus per amendment 3), populates the
        failing assertion column on the returned row. The lint allows
        the single catch here via the ``# lint-allow: capture-and-record``
        marker.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
from pathlib import Path

from scorer import __version__ as SCORER_VERSION
from scorer.anchors import (
    resolve_anchors,
)
from scorer.assertions import (
    A6ReceptorIdentity,
    ScorerAssertionError,
)
from scorer.axes import (
    compute_all_axes,
    not_applicable_axes_for,
    observed_aas_at_anchors,
)
from scorer.pocket_metrics import (
    PocketReferenceCache,
    build_pocket_reference_cache,
    compute_pocket_axes_bundle,
)
from scorer.bw_numbering import Api, get_generic_numbers
from scorer.cache import cache_key, content_sha256
from scorer.partner_metrics import compute_partner_metrics
from scorer.post_run_receipts import (
    check_ligand_present,
    check_receptor_slug_populated,
)
from scorer.receptors import (
    AmbiguousReceptorError,
    UnresolvedReceptorError,
    receptor_class,
    resolve_receptor,
    uniprot_slug,
)
from scorer.references import (
    ReferenceSet,
    check_reference_class,
    check_species,
    compute_deltas,
)
from scorer.schema import (
    ANCHOR_KEYS,
    CANONICAL_ANCHOR_KEYS,
    BWDerivationSource,
    NumberingSource,
    ScorerRow,
    StateClaim,
)
from scorer.structure import _load_structure, build_uniprot_model
from scorer.verified import verify


DESIGN_STATES = frozenset({
    StateClaim.DESIGN_NO_DRY.value,
    StateClaim.CLASS_BC_NATIVE_NO_DRY.value,
})


def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git_sha() -> str:
    return SCORER_VERSION.split("+", 1)[1] if "+" in SCORER_VERSION else SCORER_VERSION


_REPO_ROOT = Path(__file__).resolve().parent.parent
_THRESHOLDS_PANEL_CSV = _REPO_ROOT / "refs" / "thresholds_panel.csv"


# ---------------------------------------------------------------------------
# Pocket-metrics reference cache (Block C Gate 0.1, 2026-09-03).
#
# The pocket metrics (pocket_ca_rmsd, pocket_sidechain_rmsd, w648_chi1,
# ligand_rmsd_to_ref) need a role-matched reference PDB per receptor.
# Loading the PDB and renumbering it to UniProt on every scored row would
# be prohibitive — Block A scored ~9,490 predictions where a receptor
# typically covers 100-200 rows, so we amortise per (receptor, role).
#
# Key: (receptor_slug_upper, role, refs_cache_pdb_dir).
# Value: PocketReferenceCache | None (None = load failed, cached to skip
#        the retry).
# ---------------------------------------------------------------------------
_POCKET_REF_CACHE: dict[tuple[str, str, str], PocketReferenceCache | None] = {}


def _pocket_ref_for(
    receptor_slug: str,
    role: str,
    pdb_id: str,
    entry_name: str,
    api,
    refs_cache_pdb_dir: Path,
) -> PocketReferenceCache | None:
    """Get-or-build the PocketReferenceCache for (receptor, role).

    ``refs_cache_pdb_dir`` — directory holding ``<pdb_id>.cif`` files.
    Standard scorer path uses ``refs/cache/pdb/`` alongside the GPCRdb
    cache under ``refs/cache/gpcrdb/``. Cache miss loads the PDB via
    ``build_pocket_reference_cache``; a load failure is cached as None
    so the next 100 rows for the same receptor don't retry the failed
    load 100 times.
    """
    slug = receptor_slug.upper()
    key = (slug, role, str(refs_cache_pdb_dir))
    if key in _POCKET_REF_CACHE:
        return _POCKET_REF_CACHE[key]
    pdb_path = refs_cache_pdb_dir / f"{pdb_id.lower()}.cif"
    if not pdb_path.exists():
        _POCKET_REF_CACHE[key] = None
        return None
    cache = build_pocket_reference_cache(
        str(pdb_path), entry_name, api, pdb_id=pdb_id.upper(),
    )
    _POCKET_REF_CACHE[key] = cache
    return cache


def _thresholds_panel_sha256() -> str:
    """SHA256 of `refs/thresholds_panel.csv` content at scoring time.
    Stamped on every ScorerRow (post-2026-09-01) so a re-derivation of
    panel thresholds is detectable row-by-row without hunting through
    git history — cf. PREREG §11 threshold provenance."""
    try:
        return hashlib.sha256(_THRESHOLDS_PANEL_CSV.read_bytes()).hexdigest()
    except FileNotFoundError:
        return "missing"


# Fold-model output paths embed the seed in a ``seed_<N>`` folder name
# (Boltz + OF3 + Protenix all use this convention; see
# rerun_dispatch._plan_propose_row's ``seed_{fresh_seed}``). Recover the
# seed from the path when a sidecar is missing (frozen corpus + M2.4
# rerun) — same regex the plan doc calls out.
_SEED_FROM_PATH_RE = re.compile(r"/seed_(\d+)(?:/|$)")


# Block C Tier 3 pool-tree path shape (Post-Audit Stage 1, 2026-09-05):
# `.../tier3/pool/<receptor>/<ligand_role>/<partner_arm>/<backbone>/seed_<N>/...`
# `block_b_worker.sh` (the Block C dispatch) does NOT emit
# ``_rerun_plan.json`` sidecars, so ``_lift_provenance_from_sidecar``
# returns empty on every scored Tier 3 row. This regex recovers
# ``ligand_role`` (which routes the role_specific-tagged pocket-ref
# lookup in pocket_metrics) from the path itself. The receptor slug is
# lower-case in the path; the ligand_role is the exact literal from the
# manifest (e.g. "decoy_lig", "neutral_antagonist"). The remaining
# ligand fields — ligand_smiles / ligand_type / ligand_sequence — are
# not encoded in the path and must arrive via the caller-supplied
# ``manifest_*`` kwargs.
_POOL_PATH_RE = re.compile(
    r"/pool/(?P<receptor>[A-Za-z0-9_-]+)/"
    r"(?P<ligand_role>[A-Za-z0-9_-]+)/"
    r"(?P<partner_arm>[A-Za-z0-9_-]+)/"
    r"(?P<backbone>[A-Za-z0-9_-]+)/seed_\d+"
)


def _int_or_none(value: object) -> int | None:
    """Try to convert to int; return None on TypeError / ValueError.

    Small local helper to keep the lift-in loop readable without
    tripping the "except pass" silent-swallow lint. None-signalled
    failure is explicit at the call site.
    """
    if value is None or value == "" or value == 0:
        return None
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _lift_provenance_from_pool_path(input_path: str) -> dict[str, str]:
    """Recover ``ligand_role`` (and the routing hints ``partner_arm`` /
    ``backbone``) from a Block C Tier 3 pool-tree path.

    Called as a fallback when ``_lift_provenance_from_sidecar`` returns
    empty because ``block_b_worker.sh`` (the Block C dispatch) did not
    emit ``_rerun_plan.json`` sidecars. Only ``ligand_role`` reaches
    the ScorerRow (via the orchestrator's field-copy loop); the other
    keys are informational for logging.

    Returns an empty dict when the input path does not match the pool
    shape. Never raises.
    """
    m = _POOL_PATH_RE.search(input_path)
    if not m:
        return {}
    return {
        "ligand_role": m.group("ligand_role"),
        # Two more path-parsed fields kept for callers that want to
        # audit routing without opening the manifest — the orchestrator
        # itself only consumes ``ligand_role``.
        "partner_arm": m.group("partner_arm"),
        "backbone_from_path": m.group("backbone"),
    }


def _seed_used_from_input_path(input_path: str) -> int:
    """Extract the seed from ``.../seed_<N>/...`` in the input path.

    Returns 0 when no ``seed_<N>`` segment is present (frozen corpus
    predictions don't have one — they lived under
    ``outputs/<experiment>/predictions/...`` with the seed in the
    filename instead). 0 also communicates "not extractable" to
    downstream analysis without requiring a nullable int.
    """
    m = _SEED_FROM_PATH_RE.search(input_path)
    if not m:
        return 0
    try:
        return int(m.group(1))
    except ValueError:
        return 0


def _lift_provenance_from_sidecar(input_path: str, max_up: int = 8) -> dict[str, object]:
    """Walk up to ``max_up`` levels from ``input_path`` looking for a
    ``_rerun_plan.json`` sidecar (written by scorer.supervisor before
    dispatching a proposal-manifest row). Returns a dict of fields
    lifted from ``manifest_row``:

      pre_check_status   : str
      seed_used          : int    (from manifest_row["new_seed"])
      ligand_type        : str
      ligand_sequence    : str
      ligand_smiles      : str

    Empty dict if no sidecar is found in the walk, if the sidecar is
    malformed, or if it carries no ``manifest_row`` block. Never
    raises — a bad sidecar must not fail the scoring path.

    The bounded walk stops well before hitting scratch root, so a
    rogue sidecar in an unrelated ancestor cannot poison the value.
    """
    p = Path(input_path)
    ancestor = p.parent if not p.is_dir() else p
    for _ in range(max_up):
        try:
            sidecar = ancestor / "_rerun_plan.json"
            if sidecar.is_file():
                data = json.loads(sidecar.read_text())
                break
        except (OSError, json.JSONDecodeError):
            return {}
        parent = ancestor.parent
        if parent == ancestor:
            return {}
        ancestor = parent
    else:
        return {}

    row = data.get("manifest_row") or {}
    if not isinstance(row, dict):
        return {}
    out: dict[str, object] = {}
    if row.get("pre_check_status"):
        out["pre_check_status"] = str(row["pre_check_status"])
    # seed lift-in: prefer the manifest's `new_seed` (propose stamps the
    # deterministic per-row seed there); fall back to `seed_used` if
    # someone wrote it directly. Non-integer strings from either key are
    # silently skipped — the caller falls back to `_seed_used_from_input_path`.
    for seed_key in ("new_seed", "seed_used"):
        seed_int = _int_or_none(row.get(seed_key))
        if seed_int is not None:
            out["seed_used"] = seed_int
            break
    if row.get("ligand_type"):
        out["ligand_type"] = str(row["ligand_type"])
    if row.get("ligand_sequence"):
        out["ligand_sequence"] = str(row["ligand_sequence"])
    if row.get("ligand_smiles"):
        out["ligand_smiles"] = str(row["ligand_smiles"])
    # Block C add-on (2026-09-04): the pharmacology-class label. Empty
    # for Block A / Block B rows (manifest didn't carry this column).
    # Present on every Block C row: one of {"none", "decoy_lig",
    # "neutral_antagonist", "inverse_agonist", "full_agonist"}.
    # Consumed by pocket_metrics._role_for_state_claim to pick the
    # role_specific-tagged inactive reference for antagonist /
    # inverse-agonist rows.
    if row.get("ligand_role"):
        out["ligand_role"] = str(row["ligand_role"])
    return out


def _lift_pre_check_status_from_sidecar(input_path: str, max_up: int = 8) -> str:
    """If a ``_rerun_plan.json`` sits at or above ``input_path`` (written by
    scorer.supervisor before dispatching a proposal-manifest row), lift
    ``manifest_row.pre_check_status`` from it and return the string.

    Sidecar location per supervisor._submit (rerun_dispatch.py:472):
      <seed_dir>/_rerun_plan.json    e.g. .../seed_211792217/_rerun_plan.json

    Fold-model output layouts nest several directories deeper — e.g.
    Boltz writes to:
      <seed_dir>/boltz_results_<stem>/predictions/<stem>/<stem>_model_0.cif

    So we walk up from the prediction file's parent for up to ``max_up``
    levels, returning as soon as a ``_rerun_plan.json`` is found. The
    bounded walk stops well before hitting scratch root, so a rogue
    sidecar in an unrelated ancestor cannot poison the value.

    Empty string when no sidecar is found in that window (frozen-corpus
    scoring or M2.4 rerun, neither of which carry a pre_check_status),
    when the file exists but doesn't parse, or when the field is
    missing. Never raises — a bad sidecar must not fail the scoring path.
    """
    p = Path(input_path)
    ancestor = p.parent if not p.is_dir() else p
    for _ in range(max_up):
        try:
            sidecar = ancestor / "_rerun_plan.json"
            if sidecar.is_file():
                data = json.loads(sidecar.read_text())
                row = data.get("manifest_row") or {}
                return str(row.get("pre_check_status") or "")
        except (OSError, json.JSONDecodeError):
            return ""
        parent = ancestor.parent
        if parent == ancestor:
            break
        ancestor = parent
    return ""


def _resolve_receptor_or_A6(input_path: str, receptor_hint: str | None) -> tuple[str, str]:
    """Wrap the receptor resolver's exceptions into A6ReceptorIdentity.

    The bare resolver raises ValueError subclasses (Unresolved/Ambiguous)
    so its call sites in refs_build etc. don't have to depend on
    scorer/assertions.py. Here we upcast for the pipeline.
    """
    try:
        return resolve_receptor(input_path, hint=receptor_hint)
    except (AmbiguousReceptorError, UnresolvedReceptorError) as e:
        raise A6ReceptorIdentity(str(e), input_path=input_path) from e


def run_scorer(
    input_path: os.PathLike[str] | str,
    receptor_hint: str | None,
    input_state_claim: str,
    output_dir: os.PathLike[str] | str,
    *,
    ref_set: ReferenceSet | None = None,
    ref_set_csv_path: os.PathLike[str] | str | None = None,
    cache_dir: os.PathLike[str] | str | None = None,
    input_species: str = "human",
    manifest_ligand_type: str | None = None,
    manifest_ligand_smiles: str | None = None,
    manifest_ligand_sequence: str | None = None,
    manifest_ligand_role: str | None = None,
) -> ScorerRow:
    """Score one prediction. Raises ScorerAssertionError on any failure.

    A fully populated ScorerRow is returned only when A1..A6 all pass.
    Callers that need to record the failing assertion into a row without
    aborting the batch use ``score_and_capture`` instead.

    Manifest-fallback kwargs (Post-Audit Stage 1, 2026-09-05):
    ``manifest_ligand_type`` / ``manifest_ligand_smiles`` /
    ``manifest_ligand_sequence`` / ``manifest_ligand_role`` supply
    ligand-annotation fields that the batch driver read from the
    campaign manifest. They are used ONLY when the primary sidecar-lift
    path yields empty for the corresponding row field (i.e., no
    ``_rerun_plan.json`` sidecar was written by dispatch — the Block C
    Tier 3 shape). Sidecar values still win when present, so an
    existing propose-flow campaign sees no behavioural change. When
    both sidecar AND manifest kwargs are silent for a field, a pool-
    tree path fallback (``_lift_provenance_from_pool_path``) recovers
    ``ligand_role`` from the ``pool/<r>/<lrole>/<arm>/<bb>/seed_<N>``
    shape as a last resort.
    """
    input_path = str(input_path)
    output_dir = str(Path(output_dir).resolve())
    cache_dir = str(cache_dir) if cache_dir is not None else str(Path("refs/cache").resolve())

    row = ScorerRow()
    row.input_path = input_path
    row.input_state_claim = input_state_claim
    row.scorer_version = SCORER_VERSION
    row.scorer_git_sha = _git_sha()
    row.thresholds_panel_csv_sha256 = _thresholds_panel_sha256()
    row.run_ts_utc = _now_utc()
    row.numbering_source = NumberingSource.ALIGNED_TO_UNIPROT.value

    # A6 first — file need not exist yet; identity failure short-circuits
    # before we ever touch the disk. Important for F3.
    receptor_upper, disambig_source = _resolve_receptor_or_A6(input_path, receptor_hint)
    row.receptor_slug = receptor_upper
    row.receptor_disambig_source = disambig_source

    # Class-aware annotations (v3.7 add-on). Populated as soon as A6
    # succeeds so any downstream failure (A1..A5) still carries the class.
    # `receptor_class()` raises UnresolvedReceptorError only for slugs
    # missing from RECEPTOR_CLASS; every slug in KNOWN_RECEPTORS is
    # covered, and _resolve_receptor_or_A6 above guarantees the slug is
    # in KNOWN_RECEPTORS. Purely annotative — no downstream code branches
    # on these values.
    row.receptor_class = receptor_class(receptor_upper)
    row.not_applicable_axes = ";".join(not_applicable_axes_for(row.receptor_class))

    row.input_sha256 = content_sha256(input_path)

    # ------------------------------------------------------------------
    # Post-load receipts (Block C Stage 0 Step 1.4, 2026-09-04).
    #
    # Hoisted from later in the flow so the two receipts can short-circuit
    # scoring BEFORE any axis computation on a row whose CIF has silently
    # dropped its ligand (Chai malformed-SMILES shape per A3's SMILES
    # probe 2026-09-03) or whose receptor_slug has NaN'd out
    # (OPSD/B1B1U5 chain-matcher regression shape). ``_struct_full`` and
    # the sidecar lift both used to live further down the function; both
    # are pure loads that need only ``input_path`` and are safe to run
    # here. Later uses of ``_struct_full`` (partner_metrics, pocket
    # metrics) reuse the same object — no double-parse.
    # ------------------------------------------------------------------
    _struct_full = _load_structure(input_path)

    # Layer 4 + Exp-Layer 1 lift-in: when the input was produced by a
    # ``gpcr-propose`` dispatch, the supervisor writes
    # ``_rerun_plan.json`` alongside the prediction output. Lift
    # pre_check_status + seed + ligand fields off it and stamp on the
    # scored row. No sidecar → empty fields; never a failure mode.
    lifted = _lift_provenance_from_sidecar(input_path)
    if lifted.get("pre_check_status"):
        row.pre_check_status = str(lifted["pre_check_status"])
    if lifted.get("seed_used"):
        row.seed_used = int(lifted["seed_used"])  # type: ignore[arg-type]
    else:
        # No sidecar seed → try to recover from the input path itself
        # (frozen corpus predictions under
        # ``.../seed_<N>/model_X.<ext>``).
        row.seed_used = _seed_used_from_input_path(input_path)
    if lifted.get("ligand_type"):
        row.ligand_type = str(lifted["ligand_type"])
    if lifted.get("ligand_sequence"):
        row.ligand_sequence = str(lifted["ligand_sequence"])
    if lifted.get("ligand_smiles"):
        row.ligand_smiles = str(lifted["ligand_smiles"])
    if lifted.get("ligand_role"):
        row.ligand_role = str(lifted["ligand_role"])

    # Post-Audit Stage 1 fallback chain (2026-09-05): fill any ligand
    # field still empty from (a) caller-supplied manifest kwargs and
    # (b) the pool-tree path parser. The sidecar path is the primary
    # provenance source and always wins when it fires; these
    # fallbacks only fill fields the sidecar did NOT set. `ligand_role`
    # is the load-bearing one — it routes the role_specific-tagged
    # pocket-metrics reference lookup downstream, and Block C Tier 3
    # dispatch (block_b_worker.sh) does NOT emit sidecars.
    if not row.ligand_type and manifest_ligand_type:
        row.ligand_type = str(manifest_ligand_type)
    if not row.ligand_smiles and manifest_ligand_smiles:
        row.ligand_smiles = str(manifest_ligand_smiles)
    if not row.ligand_sequence and manifest_ligand_sequence:
        row.ligand_sequence = str(manifest_ligand_sequence)
    if not row.ligand_role and manifest_ligand_role:
        row.ligand_role = str(manifest_ligand_role)
    # Final fallback for ligand_role only: parse the pool-tree path.
    # Runs after sidecar + manifest so it does not clobber either.
    if not row.ligand_role:
        pool_lifted = _lift_provenance_from_pool_path(input_path)
        if pool_lifted.get("ligand_role"):
            row.ligand_role = str(pool_lifted["ligand_role"])

    # Receipt 1: receptor_slug must be populated. resolve_receptor
    # already guarantees this; the check is defence-in-depth against a
    # future regression that blanks the field between A6 success and
    # axis emission.
    check_receptor_slug_populated(row)

    # Receipt 2 (ligand-presence) is called LATER, after A3 chain
    # resolution — the peptide branch of the check needs
    # ``receptor_chain_name`` (the actual chain the receptor landed
    # on) to distinguish a peptide LIGAND chain from the receptor
    # chain, per the Post-Audit chemistry-aware refactor.

    entry_name = uniprot_slug(receptor_upper)
    row.gpcrdb_slug = entry_name
    row.gpcrdb_entry_url = f"https://gpcrdb.org/services/residues/extended/{entry_name}/"
    row.bw_derivation_source = (
        BWDerivationSource.UNIPROT_CANONICAL_CAM.value
        if entry_name == "calm_human"
        else BWDerivationSource.GPCRDB_RESIDUES_EXTENDED.value
    )

    api = Api(cache_dir=Path(cache_dir) / "gpcrdb")
    aset = resolve_anchors(api, entry_name)
    row.gpcrdb_residues_ext_sha256 = aset.residues_ext_payload_sha256
    # Only the canonical six anchors carry hardcoded ScorerRow columns
    # (anchor_X_YY_uniprot_pos / _aa_expected / _aa_observed). The literature-
    # metric anchors (LIT_METRIC_ANCHOR_KEYS in schema.py) feed the new
    # metric columns directly and don't get per-anchor CSV slots.
    for label in CANONICAL_ANCHOR_KEYS:
        anchor = aset.anchors.get(label)
        if anchor is None:
            continue
        pref = "anchor_" + label.replace(".", "_")
        setattr(row, f"{pref}_uniprot_pos", anchor.uniprot_pos)
        setattr(row, f"{pref}_aa_expected", anchor.aa_expected)

    # A3 + A2: load structure, pick chain, renumber
    model = build_uniprot_model(input_path, entry_name, api)
    row.chain_selected = model.chain_name
    row.chain_selection_method = "identity_match_to_wt"
    row.n_ca = len(model.residues)
    row.align_identity = model.identity

    # Receipt 2 (post-Audit-refactored, 2026-09-05): the ligand-presence
    # check now needs the receptor chain name so the peptide-ligand
    # branch can look for standard-AA residues on chains other than
    # the receptor. Runs after A3 chain resolution but before axis
    # computation, so a silent-apo row is still short-circuited.
    check_ligand_present(
        _struct_full, row, receptor_chain_name=model.chain_name,
    )

    # A2 + A1 fold into scorer.verified.verify() — no code path from here
    # onward can call compute_all_axes on an unverified model. Pass the
    # receptor class so the class-conditional required-anchor set drives
    # A2 (Class B lacks GPCRdb-canonical 6.30, Class F uses 6.31 — see
    # scorer/anchors.py::REQUIRED_ANCHORS_BY_CLASS).
    vmodel = verify(
        model, aset,
        skip_dry=(input_state_claim in DESIGN_STATES),
        receptor_class=row.receptor_class,
    )

    # populate observed AA columns (diagnostic; A1 has already passed)
    obs = observed_aas_at_anchors(vmodel)
    for label, aa in obs.items():
        pref = "anchor_" + label.replace(".", "_")
        setattr(row, f"{pref}_aa_observed", aa)

    # axes — always
    axes = compute_all_axes(vmodel)
    row.d_tm6_r350_r630_ca = axes["d_tm6_r350_r630_ca"]
    row.d_npxxy_y558_y753_ca = axes["d_npxxy_y558_y753_ca"]
    row.d_npxxy_y558_y753_oh = axes["d_npxxy_y558_y753_oh"]
    row.d_tm5_outward_r350_r558_ca = axes["d_tm5_outward_r350_r558_ca"]
    row.d_y558_pack_min_heavy = axes["d_y558_pack_min_heavy"]
    row.d_dry_sidechain_r350cz_e630oe1 = axes["d_dry_sidechain_r350cz_e630oe1"]
    row.icl2_helical_frac = axes["icl2_helical_frac"]
    row.plddt_mean = axes["plddt_mean"]
    import json as _json
    row.plddt_at_anchors = _json.dumps(list(axes["plddt_at_anchors"].values()))

    # -- literature-derived cross-class metrics (additive, not in predicate) --
    row.d_gpcrdb_tm6_tilt_246_637_ca = axes["d_gpcrdb_tm6_tilt_246_637_ca"]
    row.a100_component_1_ca = axes["a100_component_1_ca"]
    row.a100_component_2_ca = axes["a100_component_2_ca"]
    row.a100_component_3_ca = axes["a100_component_3_ca"]
    row.a100_component_4_ca = axes["a100_component_4_ca"]
    row.a100_component_5_ca = axes["a100_component_5_ca"]
    row.a100_index = axes["a100_index"]
    row.angle_class_b_tm6_kink_639_650_654_deg = axes[
        "angle_class_b_tm6_kink_639_650_654_deg"
    ]

    # Partner-interface metrics — PREREG §10 Block A. ``_struct_full``
    # was loaded earlier in the flow for the post-load receipts (Block C
    # Stage 0 Step 1.4, 2026-09-04) — re-used here rather than
    # re-parsed. bw_map is re-fetched from the cached GPCRdb payload —
    # no extra network hit.
    _bw_map = get_generic_numbers(api, entry_name)
    partner_metrics = compute_partner_metrics(
        _struct_full,
        vmodel,
        _bw_map,
        receptor_chain_name=model.chain_name,
        input_state_claim=input_state_claim,
    )
    row.d_ga_alpha5_r350_ca = partner_metrics["d_ga_alpha5_r350_ca"]
    row.n_interface_contacts_ga_receptor = partner_metrics[
        "n_interface_contacts_ga_receptor"
    ]
    row.plddt_ga_alpha5 = partner_metrics["plddt_ga_alpha5"]

    # Trap 3 — pLDDT-at-anchor confidence tier. This does NOT gate axis
    # emission (a low-confidence axis value is still a measurable geometric
    # fact); it flags the row so state classification returns the
    # "insufficient_confidence" bucket rather than "active" / "inactive".
    import math as _math
    valid_plddt = [v for v in axes["plddt_at_anchors"].values()
                   if v is not None and not _math.isnan(v)]
    if valid_plddt:
        row.min_plddt_at_anchor = min(valid_plddt)
        # Thresholds match co-folding conventions (Boltz/OF3/Protenix/AF2):
        #   pLDDT >= 70 : "high"       — trust the local structure
        #   50 <= pLDDT < 70 : "borderline"
        #   pLDDT < 50 : "low"         — the model threw this residue
        #                                 into the void (Trap 3)
        if row.min_plddt_at_anchor >= 70:
            row.confidence_flag = "high"
        elif row.min_plddt_at_anchor >= 50:
            row.confidence_flag = "borderline"
        else:
            row.confidence_flag = "low"

    # A4 / A5
    rs = ref_set if ref_set is not None else (
        ReferenceSet.from_csv(ref_set_csv_path) if ref_set_csv_path else ReferenceSet.empty()
    )
    lookup = rs.load_for(receptor_upper)
    if lookup.active is not None:
        row.ref_pdb_sha_active = lookup.active.provenance_sha256
    if lookup.inactive is not None:
        row.ref_pdb_sha_inactive = lookup.inactive.provenance_sha256

    # Per-receptor reference/delta scalars for the primary axis.
    # Class-conditional (plan §15, 2026-09-02):
    #   Class A -> d_r350_r630_ca_ref anchored on d_tm6_r350_r630_ca
    #   Class B -> d_gpcrdb_tm6_tilt_ref anchored on d_gpcrdb_tm6_tilt_246_637_ca
    #   Class F -> kept on Class A anchor (reported-secondary)
    # NaN in any component means the class-appropriate reference is missing
    # (uncovered receptor, or NaN in the ref column of reference_set.csv).
    # Downstream analysis subsets on `receptor_d_active_ref IS NaN` to
    # identify uncovered rows. See references.py::compute_deltas.
    (row.receptor_d_active_ref,
     row.receptor_d_inactive_ref,
     row.receptor_midpoint,
     row.delta_to_active,
     row.delta_to_inactive) = compute_deltas(
        row.d_tm6_r350_r630_ca, lookup,
        receptor_class=row.receptor_class,
        current_d_tilt=row.d_gpcrdb_tm6_tilt_246_637_ca,
    )

    if input_state_claim not in DESIGN_STATES and input_state_claim != StateClaim.APO.value:
        check_reference_class(lookup, receptor_upper, input_state_claim)
        check_species(lookup, receptor_upper, input_species, input_state_claim)

    row.cache_key = cache_key(input_path, output_dir, aset.residues_ext_payload_sha256)
    if ref_set_csv_path and Path(ref_set_csv_path).exists():
        row.ref_set_csv_sha256 = content_sha256(ref_set_csv_path)

    # NOTE: sidecar lift + `_struct_full` load were hoisted to right
    # after `row.input_sha256 = ...` so the post-load receipts (Block C
    # Stage 0 Step 1.4, 2026-09-04) can short-circuit before axis
    # computation. `row.ligand_type` and friends are already populated
    # by the time we reach the pocket-metrics block below.

    # -- pocket metrics (Block C Gate 0.1, 2026-09-03) --------------------
    # Four BW-anchored metrics on top of the transmission-side axes. Runs
    # AFTER the sidecar-lift so ``row.ligand_type`` is populated before we
    # read it, and AFTER the A4/A5 block so ``lookup`` is available. Reads
    # the role-matched reference (active for Ga-coupled-active / arrestin-
    # coupled; inactive for antagonist / inverse-agonist; apo falls back to
    # active) via the module-level ``_POCKET_REF_CACHE`` and reuses
    # ``_struct_full`` + ``_bw_map`` already loaded above. Every column
    # defaults to NaN and is populated iff the metric can be computed
    # cleanly; see scorer/pocket_metrics.py for the class-conditional
    # posture (Class B/F: pocket_ca/pocket_sc/w648_chi1 → NaN with flag;
    # ligand_rmsd_to_ref still runs).
    _refs_cache_pdb_dir = Path(cache_dir) / "pdb"
    _ref_active_cache: PocketReferenceCache | None = None
    _ref_inactive_cache: PocketReferenceCache | None = None
    if lookup.active is not None and lookup.active.pdb_id:
        _ref_active_cache = _pocket_ref_for(
            receptor_upper, "active", lookup.active.pdb_id,
            entry_name, api, _refs_cache_pdb_dir,
        )
    if lookup.inactive is not None and lookup.inactive.pdb_id:
        _ref_inactive_cache = _pocket_ref_for(
            receptor_upper, "inactive", lookup.inactive.pdb_id,
            entry_name, api, _refs_cache_pdb_dir,
        )
    # Block C add-on (2026-09-04): build role_specific-tagged inactive
    # caches so pocket_metrics can route neutral_antagonist /
    # inverse_agonist rows to the antagonist-specific reference PDB
    # (which contains the matching small-molecule ligand). Keyed by
    # role_specific string; the same cache-key pattern
    # (receptor, "inactive:<role_specific>", refs_dir) keeps the
    # per-receptor amortisation.
    _ref_inactive_by_specific: dict[str, PocketReferenceCache] = {}
    for spec_key, spec_row in (
        lookup.inactive_by_role_specific.items()
        if hasattr(lookup, "inactive_by_role_specific") else ()
    ):
        if not spec_key or not spec_row.pdb_id:
            continue
        _cache = _pocket_ref_for(
            receptor_upper, f"inactive:{spec_key}", spec_row.pdb_id,
            entry_name, api, _refs_cache_pdb_dir,
        )
        if _cache is not None:
            _ref_inactive_by_specific[spec_key] = _cache
    pocket_axes = compute_pocket_axes_bundle(
        vmodel, _struct_full, _bw_map,
        receptor_class=row.receptor_class,
        receptor_chain_name=model.chain_name,
        input_state_claim=input_state_claim,
        ligand_type=row.ligand_type or "",
        ref_active=_ref_active_cache,
        ref_inactive=_ref_inactive_cache,
        ref_inactive_by_role_specific=_ref_inactive_by_specific,
        ligand_role=row.ligand_role or "",
    )
    row.pocket_ca_rmsd = pocket_axes["pocket_ca_rmsd"]
    row.pocket_sidechain_rmsd = pocket_axes["pocket_sidechain_rmsd"]
    row.w648_chi1 = pocket_axes["w648_chi1"]
    row.ligand_rmsd_to_ref = pocket_axes["ligand_rmsd_to_ref"]
    row.pocket_ligand_atom_map_method = pocket_axes.get(
        "pocket_ligand_atom_map_method", ""
    )
    row.pocket_ca_rmsd_missing_residues = pocket_axes[
        "pocket_ca_rmsd_missing_residues"
    ]
    row.pocket_notes = pocket_axes["pocket_notes"]
    # Post-Audit Stage 2 dual-reference companions (2026-09-05).
    row.pocket_ca_rmsd_active = pocket_axes["pocket_ca_rmsd_active"]
    row.pocket_ca_rmsd_inactive = pocket_axes["pocket_ca_rmsd_inactive"]
    row.pocket_sidechain_rmsd_active = pocket_axes[
        "pocket_sidechain_rmsd_active"
    ]
    row.pocket_sidechain_rmsd_inactive = pocket_axes[
        "pocket_sidechain_rmsd_inactive"
    ]
    row.pocket_ref_pdb_sha_active = pocket_axes["pocket_ref_pdb_sha_active"]
    row.pocket_ref_pdb_sha_inactive = pocket_axes[
        "pocket_ref_pdb_sha_inactive"
    ]
    row.pocket_ref_role_active = pocket_axes["pocket_ref_role_active"]
    row.pocket_ref_role_inactive = pocket_axes["pocket_ref_role_inactive"]

    row.passed = True
    return row


def score_and_capture(
    input_path: os.PathLike[str] | str,
    receptor_hint: str | None,
    input_state_claim: str,
    output_dir: os.PathLike[str] | str,
    **kwargs,
) -> tuple[ScorerRow, ScorerAssertionError | None]:
    """Never raises. Wraps ``run_scorer`` for the batch driver.

    Returns ``(row, err)`` where ``err`` is None on success. On failure,
    the row is populated up to the point of raise, ``passed=False``, and
    the corresponding per-assertion column carries the exception class
    name. Amendment 3: batch driver never aborts on raise — this is the
    single sanctioned catch site.
    """
    try:
        row = run_scorer(input_path, receptor_hint, input_state_claim,
                         output_dir, **kwargs)
        return row, None
    except ScorerAssertionError as e:  # lint-allow: capture-and-record — the ONE sanctioned catch site
        # Reconstruct a partial row so the caller has SOMETHING to write
        row = ScorerRow()
        row.input_path = str(input_path)
        row.input_state_claim = input_state_claim
        row.scorer_version = SCORER_VERSION
        row.scorer_git_sha = _git_sha()
        row.thresholds_panel_csv_sha256 = _thresholds_panel_sha256()
        row.run_ts_utc = _now_utc()
        row.passed = False
        setattr(row, e.assertion_id, type(e).__name__)
        # Post-Audit Stage 1 (2026-09-05): also stamp the manifest
        # ligand-annotation kwargs onto the failure row so downstream
        # write-time join assertions can distinguish a real join
        # failure from an early A6/A3/A2/A1 raise that never reached
        # the sidecar-lift block. The fields carry manifest provenance
        # regardless of scoring outcome.
        m_type = kwargs.get("manifest_ligand_type")
        m_smi = kwargs.get("manifest_ligand_smiles")
        m_seq = kwargs.get("manifest_ligand_sequence")
        m_role = kwargs.get("manifest_ligand_role")
        if m_type:
            row.ligand_type = str(m_type)
        if m_smi:
            row.ligand_smiles = str(m_smi)
        if m_seq:
            row.ligand_sequence = str(m_seq)
        if m_role:
            row.ligand_role = str(m_role)
        return row, e
