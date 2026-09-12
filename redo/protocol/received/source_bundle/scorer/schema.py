"""ScorerRow — the single output row schema.

Every scored prediction produces exactly one ScorerRow, written to CSV and
mirrored as a JSON sidecar next to the input. A row that cannot be traced
back to its inputs is the failure mode this repo exists to eliminate — see
docs/AUDIT_TRAIL.md.

Foreign keys back into the three ledgers under ``refs/`` (see docs/TRACKING.md):

    experiment_id       -> refs/experiments.csv
    prediction_sha      -> refs/predictions.csv     (equals input_sha256)
    ref_pdb_sha_active,
    ref_pdb_sha_inactive-> refs/pdbs.csv
    scorer_git_sha      -> git history

CSV column order is fixed by the dataclass field order and additionally
locked by CSV_COLUMNS. Reordering fields is a breaking change to every
downstream consumer.
"""
from __future__ import annotations

import enum
import json
from dataclasses import asdict, dataclass, field, fields
from typing import Any


# ---------------------------------------------------------------------------
# Enums (grep-visible; adding a value is a code change, not a config change)
# ---------------------------------------------------------------------------


class StateClaim(str, enum.Enum):
    """input_state_claim — mandatory on every call.

    design_no_dry and class_bc_native_no_dry are values, NOT silencing flags.
    When set, A1 skips the DRY-anchor AA-identity check for THOSE receptors
    only; every other axis remains strict and every axis value is still
    emitted. See docs/ASSERTIONS.md.
    """

    Ga_COUPLED_ACTIVE = "Ga-coupled-active"
    ARRESTIN_COUPLED = "arrestin-coupled"
    INACTIVE_ANTAGONIST = "inactive-antagonist"
    INACTIVE_INVERSE_AGONIST = "inactive-inverse-agonist"
    APO = "apo"
    DESIGN_NO_DRY = "design_no_dry"
    CLASS_BC_NATIVE_NO_DRY = "class_bc_native_no_dry"


class Backbone(str, enum.Enum):
    BOLTZ = "boltz"
    OF3 = "of3"
    PROTENIX = "protenix"
    AF2 = "af2"
    AFCLUSTER = "afcluster"
    CONFORNETS = "confornets"
    UNKNOWN = "unknown"


class BWDerivationSource(str, enum.Enum):
    """The literal string emitted on every row. Two permitted values total.

    Adding a third requires a corresponding entry in scorer/anchors.py or
    scorer/noncanonical.py plus a test — see docs/BW_SOURCE.md.
    """

    GPCRDB_RESIDUES_EXTENDED = "gpcrdb:services/residues/extended"
    UNIPROT_CANONICAL_CAM = "uniprot_canonical:calmodulin_human"


class NumberingSource(str, enum.Enum):
    DEPOSITED = "deposited"
    ALIGNED_TO_UNIPROT = "aligned-to-uniprot"


class LigandType(str, enum.Enum):
    """The four permitted values for ``ScorerRow.ligand_type`` and the
    ``ligand.type:`` field in a gpcr-propose YAML spec (Exp-Layer 1).

    peptide       — a proteinogenic peptide ligand; ``ligand_sequence``
                    carries the FASTA. Materialised as a Boltz protein
                    chain (or the equivalent per backbone).
    small_molecule — a small-molecule ligand; ``ligand_smiles`` carries
                    the SMILES. Materialised as a Boltz ``ligand`` block
                    (or the equivalent per backbone) when a supported
                    backbone accepts SMILES inputs; refused with a
                    clear SpecError otherwise.
    apo           — deliberately-empty ligand slot (analyst is running
                    apo controls to compare against holo).
    none          — the row has no ligand context (default; corresponds
                    to the pre-Exp-Layer-1 behaviour where the spec
                    doesn't mention a ligand).
    """
    PEPTIDE = "peptide"
    SMALL_MOLECULE = "small_molecule"
    APO = "apo"
    NONE = "none"


class AssertionId(str, enum.Enum):
    A1 = "A1_amino_acid_identity"
    A2 = "A2_fasta_completeness"
    A3 = "A3_wrong_chain"
    A4 = "A4_reference_class_match"
    A5 = "A5_species_match"
    A6 = "A6_receptor_identity"


# ---------------------------------------------------------------------------
# Anchor keys — BW positions the scorer resolves per PDB.
#
# ``CANONICAL_ANCHOR_KEYS`` — the original six positions that each carry
# three hardcoded ScorerRow columns (``anchor_X_YY_uniprot_pos``,
# ``_aa_expected``, ``_aa_observed``). These drive DRY/NPxxY/TM6/TM5-out/
# Y5.58-pack — the canonical Class-A axes plus the primary TM6 marker.
# Adding to this tuple is a schema change (three new columns each).
#
# ``LIT_METRIC_ANCHOR_KEYS`` — literature-derived metric anchors added in
# the 2026-09-01 scorer extension (PREREG §2b + §2c-revised):
#   - GPCRdb cross-class TM6 tilt (2.46 CA -- 6.37 CA)
#   - A100 activation index — Ibrahim, Wifling & Clark, J. Chem. Inf.
#     Model. 2019, 59(9), 3938-3945 (DOI 10.1021/acs.jcim.9b00604).
#     Five Cα-Cα distances: 1.53-7.55, 2.50-3.37, 3.42-4.42, 5.66-6.34,
#     6.58-7.35. (6.34 already present in CANONICAL.)
#   - Class B TM6 kink angle (Kobayashi et al., Nature 2023):
#     Cα angle at 6.39 - 6.50 - 6.54.
# These are fetched from GPCRdb identically to the canonical six but do
# NOT get their own ``anchor_X_YY_*`` columns — the literature metrics
# consume them directly. Adding to this tuple is a schema change (new
# metric columns), but existing anchor_* columns are unaffected.
# ---------------------------------------------------------------------------

CANONICAL_ANCHOR_KEYS: tuple[str, ...] = ("3.50", "3.51", "5.58", "6.30", "6.34", "7.53")

LIT_METRIC_ANCHOR_KEYS: tuple[str, ...] = (
    # GPCRdb TM6 tilt (Class A/B/C primary cross-class marker per GPCRdb)
    "2.46", "6.37",
    # A100 index (Ibrahim, Wifling & Clark 2019). 6.34 already canonical.
    "1.53", "7.55", "2.50", "3.37", "3.42", "4.42", "5.66", "6.58", "7.35",
    # Class B TM6 kink angle (Kobayashi et al. 2023)
    "6.39", "6.50", "6.54",
)

ANCHOR_KEYS: tuple[str, ...] = CANONICAL_ANCHOR_KEYS + LIT_METRIC_ANCHOR_KEYS


# ---------------------------------------------------------------------------
# ScorerRow
# ---------------------------------------------------------------------------


@dataclass
class ScorerRow:
    # -- identity -----------------------------------------------------------
    input_path: str = ""
    input_sha256: str = ""          # == prediction_sha in refs/predictions.csv
    receptor_slug: str = ""
    receptor_disambig_source: str = ""  # "explicit_table" | "word_boundary_regex" | "manual_hint"
    input_state_claim: str = ""     # StateClaim value
    n_ca: int = 0
    chain_selected: str = ""
    chain_selection_method: str = ""    # "identity_match_to_wt" | "manual_override"

    # -- foreign keys -------------------------------------------------------
    experiment_id: str = ""         # FK -> refs/experiments.csv (may be empty on single-file calls)
    ref_pdb_sha_active: str = ""    # FK -> refs/pdbs.csv
    ref_pdb_sha_inactive: str = ""  # FK -> refs/pdbs.csv
    scorer_git_sha: str = ""
    scorer_version: str = ""

    # -- BW provenance ------------------------------------------------------
    bw_derivation_source: str = ""  # BWDerivationSource value
    gpcrdb_slug: str = ""           # e.g. "adrb2_human"
    gpcrdb_entry_url: str = ""
    gpcrdb_residues_ext_sha256: str = ""

    # -- anchor resolution (6 x 3 = 18 columns; flat for CSV grep-ability) --
    anchor_3_50_uniprot_pos: int = -1
    anchor_3_50_aa_expected: str = ""
    anchor_3_50_aa_observed: str = ""
    anchor_3_51_uniprot_pos: int = -1
    anchor_3_51_aa_expected: str = ""
    anchor_3_51_aa_observed: str = ""
    anchor_5_58_uniprot_pos: int = -1
    anchor_5_58_aa_expected: str = ""
    anchor_5_58_aa_observed: str = ""
    anchor_6_30_uniprot_pos: int = -1
    anchor_6_30_aa_expected: str = ""
    anchor_6_30_aa_observed: str = ""
    anchor_6_34_uniprot_pos: int = -1
    anchor_6_34_aa_expected: str = ""
    anchor_6_34_aa_observed: str = ""
    anchor_7_53_uniprot_pos: int = -1
    anchor_7_53_aa_expected: str = ""
    anchor_7_53_aa_observed: str = ""

    numbering_source: str = ""      # NumberingSource value
    align_identity: float = float("nan")   # 0..1, NaN if numbering_source == DEPOSITED

    # -- axes (all always emitted) ------------------------------------------
    d_tm6_r350_r630_ca: float = float("nan")
    d_npxxy_y558_y753_ca: float = float("nan")
    d_tm5_outward_r350_r558_ca: float = float("nan")
    d_y558_pack_min_heavy: float = float("nan")
    d_dry_sidechain_r350cz_e630oe1: float = float("nan")
    icl2_helical_frac: float = float("nan")
    plddt_mean: float = float("nan")
    plddt_at_anchors: str = ""     # JSON-encoded list of 6 floats

    # -- reference-anchored labels -----------------------------------------
    receptor_d_active_ref: float = float("nan")
    receptor_d_inactive_ref: float = float("nan")
    receptor_midpoint: float = float("nan")
    delta_to_active: float = float("nan")
    delta_to_inactive: float = float("nan")

    # -- confidence tier (Trap 3 — AI predictions with pLDDT<threshold at ---
    #   any anchor are geometrically measurable but not classifiable). Values
    #   {"high", "borderline", "low"} derived from min(plddt_at_anchors) vs
    #   refs/state_thresholds.csv::min_plddt_at_anchor. State classification
    #   returns "insufficient_confidence" bucket rather than active/inactive
    #   when confidence_flag == "low".
    confidence_flag: str = ""
    min_plddt_at_anchor: float = float("nan")

    # -- per-assertion (empty on pass; exception class name on fail) --------
    A1_amino_acid_identity: str = ""
    A2_fasta_completeness: str = ""
    A3_wrong_chain: str = ""
    A4_reference_class_match: str = ""
    A5_species_match: str = ""
    A6_receptor_identity: str = ""

    # -- provenance ---------------------------------------------------------
    ref_set_csv_sha256: str = ""
    run_ts_utc: str = ""            # ISO-8601, UTC
    cache_key: str = ""             # content-hash cache key (see scorer/cache.py)
    passed: bool = False            # True iff all six assertions pass

    # -- class-aware annotations (v3.7 add-on, additive only) ---------------
    # `receptor_class` — GPCR class per RECEPTOR_CLASS in scorer/receptors.py
    # ("A" / "B" / "C" / "F" / "T2R" / "N" for non-canonical). Populated
    # whenever the receptor_slug has been resolved (i.e. everything after
    # A6 passes); empty on early A6 failures.
    #
    # `not_applicable_axes` — semicolon-separated list of axis column names
    # whose biological interpretation is NOT calibrated for this receptor's
    # class (from AXIS_APPLICABILITY in scorer/axes.py). Purely annotative:
    # the axis value itself is still emitted in its usual column (NaN when
    # the physics doesn't apply, numeric otherwise). Downstream analyses
    # use this to distinguish "NaN because class-inapplicable" from "NaN
    # because measurement failed".
    #
    # These columns are strictly ADDITIVE: every prior column preserves its
    # v3.6b position and value byte-identical when the same input is
    # rescored. See docs/PIPELINE_INTERPRETATION.md#class-aware-rescore.
    receptor_class: str = ""
    not_applicable_axes: str = ""

    # -- proposal provenance (Layer 4 add-on, additive only) --------------
    # Populated only for rows scored from a ``gpcr-propose``-emitted input
    # (i.e. a ``_rerun_plan.json`` sidecar sits next to the prediction
    # output). Blank for M2.4 rerun rows and frozen-corpus scoring. The
    # sidecar's ``manifest_row.pre_check_status`` is lifted verbatim so
    # downstream analysis can filter "known-warned proposal runs" from
    # "clean proposal runs" from "non-proposal frozen corpus".
    pre_check_status: str = ""

    # -- seed + ligand provenance (Exp-Layer 1 add-on, additive only) ------
    # `seed_used` — the integer seed the fold model was invoked with.
    # Extracted from the input path (``.../seed_<N>/...``) when a sidecar
    # is absent; lifted verbatim from a propose sidecar when present.
    # 0 when neither source is available.
    seed_used: int = 0
    # `ligand_type` — one of {"peptide", "small_molecule", "apo", "none"}
    # (see LigandType enum). Populated when the row was scored via a
    # gpcr-propose flow whose spec declared a `ligand:` block. Empty
    # string for frozen-corpus scoring and M2.4 rerun rows.
    ligand_type: str = ""
    # `ligand_sequence` — FASTA of the peptide ligand (empty otherwise).
    ligand_sequence: str = ""
    # `ligand_smiles` — SMILES of the small-molecule ligand (empty
    # otherwise).
    ligand_smiles: str = ""

    # -- partner-interface metrics (PREREG §10 Block A add-on, additive) ----
    # Emitted on every scored row. When the prediction is single-chain (apo,
    # or any run without a docked partner) the three Gα-dependent metrics
    # are NaN — never zero. n_interface_contacts_ga_receptor is a float
    # (not int) so its "no partner" sentinel is NaN, consistent with the
    # other three.
    #
    # `d_npxxy_y558_y753_oh` — Y5.58 OH → Y7.53 OH distance in Å. Literature
    #   NPxxY-collapse thresholds are quoted on OH-OH (~7–8 Å); the frozen
    #   CA-CA column stays alongside for the class of measurements it was
    #   calibrated for. NaN if either Y5.58 or Y7.53 lacks an OH atom on the
    #   VerifiedModel.
    # `d_ga_alpha5_r350_ca` — CA distance from the Gα α5-CT (C-terminal
    #   residue of the Gα chain) to receptor R3.50. NaN when no Gα chain
    #   is present in the input.
    # `n_interface_contacts_ga_receptor` — number of Gα heavy atoms within
    #   5.0 Å of any receptor TM3/TM5/TM6 heavy atom (each Gα atom counted
    #   at most once). NaN in the no-partner case (design decision — kept
    #   as NaN rather than 0 so downstream analyses cannot conflate an apo
    #   run with a coupled-but-non-contacting run; both would produce 0
    #   under the "count" reading).
    # `plddt_ga_alpha5` — mean pLDDT across the last 20 residues of the Gα
    #   chain (the α5 helix + α5-CT). NaN when no Gα chain is present or
    #   pLDDT (B-factor field) is missing.
    d_npxxy_y558_y753_oh: float = float("nan")
    d_ga_alpha5_r350_ca: float = float("nan")
    n_interface_contacts_ga_receptor: float = float("nan")
    plddt_ga_alpha5: float = float("nan")

    # -- literature-derived cross-class activation metrics (2026-09-01 add-on,
    #    additive only). PREREG §2b + §2c-revised. These columns are emitted
    #    for future analysis and to enable enriched two-instrument success
    #    rules once user reviews the correlations with the current single-
    #    metric NPxxY-OH predicate. NONE of them enter the active-call
    #    predicate today (predicate remains single-metric NPxxY-OH; see
    #    scorer/switch_signal.py::MotifThresholds — user-locked).
    #
    # `d_gpcrdb_tm6_tilt_246_637_ca` — GPCRdb-doc primary cross-class TM6
    #   tilt marker: 2.46 CA -- 6.37 CA distance in Å. Applies to Class A,
    #   B, C (NOT F — GPCRdb uses a different measure there). NaN if
    #   either anchor is not resolvable via GPCRdb.
    # `a100_component_1_ca` … `a100_component_5_ca` — the five Cα-Cα
    #   distances (Å) feeding the Ibrahim/Wifling/Clark 2019 index, in
    #   the paper's canonical order:
    #     1: 1.53 -- 7.55  (TM1-TM7)
    #     2: 2.50 -- 3.37  (TM2-TM3)
    #     3: 3.42 -- 4.42  (TM3-TM4)
    #     4: 5.66 -- 6.34  (TM5-TM6 outward-swing)
    #     5: 6.58 -- 7.35  (TM6-TM7 extracellular tip)
    #   NaN per component if its two anchors are not resolvable.
    # `a100_index` — composite:
    #     A100 = -14.43 * c1 - 7.62 * c2 + 9.11 * c3
    #            - 6.32 * c4 - 5.22 * c5 + 278.88
    #   Two-state: inactive < 25, active > 25. Three-state: inactive < 0,
    #   intermediate 0-55, active > 55. NaN when ANY component is NaN.
    # `angle_class_b_tm6_kink_639_650_654_deg` — Class B TM6 kink angle
    #   (Kobayashi et al., Nature 2023). Cα-Cα-Cα angle vertex at 6.50,
    #   in degrees. Active state ≈ 90° (sharp kink), inactive ≈ 145°.
    #   NaN for receptors where 6.39 / 6.50 / 6.54 aren't resolvable
    #   (typical of Class A receptors, where the PxxG motif that drives
    #   the Class-B kink is absent).
    d_gpcrdb_tm6_tilt_246_637_ca: float = float("nan")
    a100_component_1_ca: float = float("nan")
    a100_component_2_ca: float = float("nan")
    a100_component_3_ca: float = float("nan")
    a100_component_4_ca: float = float("nan")
    a100_component_5_ca: float = float("nan")
    a100_index: float = float("nan")
    angle_class_b_tm6_kink_639_650_654_deg: float = float("nan")

    # -- predicate threshold provenance (2026-09-01) -----------------------
    # Every row carries the exact threshold values used by the scorer at
    # scoring time. Prevents silent generation-mixing when the panel
    # thresholds are re-derived — a re-scored CSV can be compared against
    # a pre-derivation CSV row-by-row on threshold_* columns and
    # thresholds_panel_csv_sha256 to detect the change. See PREREG §2b.
    threshold_npxxy_oh_active_lt: float = 9.08              # locked 2026-09-01
    threshold_gpcrdb_tm6_tilt_active_gt: float = 14.932     # locked 2026-09-01
    thresholds_panel_csv_sha256: str = ""

    # -- pocket metrics (Block C Gate 0.1, 2026-09-03 add-on) --------------
    # PREREG amendment pending (Gate 0.6). Additive-only extension: every
    # prior column preserves its position and value byte-identical when the
    # same input is rescored. See scorer/pocket_metrics.py and
    # experiments/020_block_c_ligand_pharmacology/analysis/
    # scorer_extension_notes.md.
    #
    # Frames: one 7TM-CA Kabsch (mobile=prediction, target=role-matched
    # reference PDB) produces the alignment transform used for all three
    # RMSD-style metrics — pocket_ca_rmsd, pocket_sidechain_rmsd, and
    # ligand_rmsd_to_ref sit in the same aligned frame. w648_chi1 is a
    # local dihedral, alignment-independent.
    #
    # `pocket_ca_rmsd` — Cα RMSD (Å) over 12 BW positions:
    #     3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55,
    #     7.39, 7.42. NaN for Class B / F receptors (Class A pocket set
    #     does not transfer; peptide-binding cavity definition deferred);
    #     NaN when <6 of 12 residues resolve.
    # `pocket_sidechain_rmsd` — same residues, sidechain heavy atoms only
    #     (element != H; atom name not in {N, CA, C, O}). Atoms matched
    #     by name between prediction and reference at the same UniProt
    #     position. Same NaN posture as pocket_ca_rmsd.
    # `w648_chi1` — W6.48 χ1 dihedral N-Cα-Cβ-Cγ (degrees). Class B / F
    #     NaN with "class_X_no_w648" flag (no direct equivalent). NaN if
    #     6.48 residue is not tryptophan (point-mutant construct) or if
    #     the four dihedral atoms are not all modelled.
    # `ligand_rmsd_to_ref` — heavy-atom RMSD (Å) from prediction ligand
    #     to reference crystal ligand after the 7TM-CA Kabsch transform
    #     is applied to the reference ligand. Atoms matched by
    #     (atom_name, element) — bond-graph-free (DUD-E-style match).
    #     NaN for apo rows (state_claim == "apo") and rows with
    #     ligand_type in {apo, none, ""}. **CONSUMERS MUST FILTER
    #     decoy_lig rows via the manifest / spec** — the number is
    #     computed against the real-ligand reference even for decoy_lig
    #     and is not meaningful in that setting.
    # `pocket_ca_rmsd_missing_residues` — debug column: ";"-joined BW
    #     labels not present on either prediction or reference side.
    #     Empty when all 12 residues contribute.
    # `pocket_notes` — ";"-joined per-metric notes: which reference was
    #     used, 7TM Kabsch residue count, class-deferred flags, matched-
    #     atom counts on the ligand pose. Human-readable diagnostic; not
    #     parsed by downstream code beyond `""`-check for "clean".
    pocket_ca_rmsd: float = float("nan")
    pocket_sidechain_rmsd: float = float("nan")
    w648_chi1: float = float("nan")
    ligand_rmsd_to_ref: float = float("nan")
    pocket_ca_rmsd_missing_residues: str = ""
    pocket_notes: str = ""

    # -- post-run receipts (Block C Stage 0 Step 1.4, 2026-09-04 add-on) ---
    # Two named post-load receipts distinct from the sequenced A1..A6
    # pre-scoring assertions. Both columns are empty on a passing row;
    # the exception subclass name is stamped on a failing row (same
    # convention as A1..A6). See scorer/post_run_receipts.py and
    # scorer/assertions.py::ALigandPresence / AReceptorSlugMissing.
    #
    # `A_LIGAND_PRESENT` — fires when the manifest declared a ligand
    #   (``ligand_type in {"peptide","small_molecule"}`` or
    #   ``ligand_smiles``/``ligand_sequence`` non-empty) but the produced
    #   CIF has zero non-buffer heavy atoms on any HETATM residue.
    #   Empty on apo / none rows (skip condition) and on rows whose CIF
    #   has any real ligand present.
    # `A_RECEPTOR_SLUG_MISSING` — fires when ``receptor_slug`` is empty
    #   or NaN-like at scoring time. Defence-in-depth for the OPSD /
    #   B1B1U5 chain-matcher regression shape.
    #
    # Appended at the very end of the dataclass to preserve every prior
    # CSV column position byte-identical — same additive-only discipline
    # as A4 landed for the pocket-metrics columns.
    A_LIGAND_PRESENT: str = ""
    A_RECEPTOR_SLUG_MISSING: str = ""

    # -- Block C role_specific plumbing (2026-09-04 add-on) -----------------
    # `ligand_role` — the pharmacology-class label from the Block C
    # manifest. One of {"none", "decoy_lig", "neutral_antagonist",
    # "inverse_agonist", "full_agonist"} on Block C-scored rows; empty
    # on Block A / Block B rows (the column didn't exist in their
    # manifests). Consumed by
    # scorer.pocket_metrics._role_for_state_claim to select the
    # role_specific-tagged inactive reference PDB (containing the
    # matching small-molecule ligand) when the state_claim is
    # ``Ga-coupled-active`` but the ligand's pharmacology is
    # antagonist / inverse-agonist. Appended at the tail to preserve
    # strict additive-only column-order discipline (matches the
    # A_LIGAND_PRESENT / A_RECEPTOR_SLUG_MISSING landing pattern).
    ligand_role: str = ""

    # -- Block C Post-Audit dual-reference pocket metrics (2026-09-05) ------
    # Explicit "always against reference X" pocket-RMSD variants so a
    # single row carries pocket-geometry deltas to BOTH the active and
    # the inactive reference regardless of the role-based routing that
    # selects `pocket_ca_rmsd` / `pocket_sidechain_rmsd`. Enables the
    # ligand-state-specificity 2×2 test (Stage 3a of the Post-Audit
    # plan): the (agonist − antagonist)_on_active_ref minus
    # (agonist − antagonist)_on_inactive_ref interaction term separates
    # ligand-state-specific pocket geometry from general fold-quality
    # variation.
    #
    # `_active` columns always compare against the ACTIVE reference PDB
    # for this receptor (``lookup.active``). NaN when no active ref is
    # curated or when the pocket-metrics load fails.
    # `_inactive` columns always compare against the role_specific-tagged
    # inactive PDB matching the row's ``ligand_role``:
    #   ligand_role == "neutral_antagonist" -> inactive_neutral_antagonist
    #   ligand_role == "inverse_agonist"    -> inactive_inverse_agonist
    #   otherwise                           -> generic inactive
    # Falls back to the generic inactive PDB when no role_specific PDB
    # is curated. NaN when no inactive ref is curated for this receptor.
    # Both variants share the SAME 7TM Kabsch frame per row (the one
    # picked for the role-matched ``pocket_ca_rmsd`` column) — measuring
    # "how far the prediction's pocket sits from ref X in that shared
    # frame" — which keeps the (active − inactive) interaction term
    # arithmetically well-defined.
    pocket_ca_rmsd_active: float = float("nan")
    pocket_ca_rmsd_inactive: float = float("nan")
    pocket_sidechain_rmsd_active: float = float("nan")
    pocket_sidechain_rmsd_inactive: float = float("nan")
    # SHA + role provenance for the two references actually consulted.
    # `pocket_ref_pdb_sha_active` is the provenance_sha256 of the PDB
    # loaded as the always-active variant; `pocket_ref_role_active` is
    # the fixed literal ``"active"`` — kept in the schema for symmetry
    # with the inactive column and to make downstream joins uniform.
    # `pocket_ref_pdb_sha_inactive` is the SHA of the inactive PDB the
    # row's ligand_role routed to; `pocket_ref_role_inactive` records
    # which role_specific was chosen ("", "inactive_neutral_antagonist",
    # "inactive_inverse_agonist", or "generic_inactive_fallback"). Empty
    # when the corresponding reference was not available for the
    # receptor at scoring time.
    pocket_ref_pdb_sha_active: str = ""
    pocket_ref_pdb_sha_inactive: str = ""
    pocket_ref_role_active: str = ""
    pocket_ref_role_inactive: str = ""

    # -- ligand-atom-matcher method (2026-09-06) ---------------------------
    # `pocket_ligand_atom_map_method` — 2026-09-06 MCS-fallback rework
    # (memory [[ligand-rmsd-atom-name-gap-2026-09-06]]). Records which
    # atom-pairing path produced `ligand_rmsd_to_ref`. One of:
    #   ""                    — early exit (apo / no transform / no ref
    #                            ligand / empty struct); NaN in the value
    #                            column.
    #   "atom_name_element"   — legacy (name, element) matcher succeeded
    #                            with >=5 atoms; byte-identical numerical
    #                            behaviour to the pre-2026-09-06 code.
    #                            Expected for OF3 / Protenix rows whose
    #                            CIFs preserve CCD atom names.
    #   "mcs"                 — RDKit MCS fallback fired and matched >=5
    #                            atoms. Unlocks Boltz / Chai rows whose
    #                            atom names are SMILES-derived and do
    #                            not overlap the CCD reference.
    #   "mcs_too_small"       — MCS returned <5 atoms; RMSD is NaN.
    #   "no_match"            — MCS query construction / substructure
    #                            match failed; RMSD is NaN.
    #   "parse_failure"       — either side failed to build an RDKit Mol;
    #                            RMSD is NaN.
    #   "rdkit_unavailable"   — RDKit not importable at scoring time;
    #                            RMSD is NaN.
    # Analysis code stratifies cross-backbone comparability filters on
    # this column: ``method in {atom_name_element, mcs}`` = trustworthy.
    # Appended at the tail per the schema additive-only discipline.
    pocket_ligand_atom_map_method: str = ""

    # -- serialisation ------------------------------------------------------

    @classmethod
    def csv_columns(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def to_csv_row(self) -> dict[str, Any]:
        """Flat dict suitable for csv.DictWriter."""
        return {f.name: getattr(self, f.name) for f in fields(self)}

    def to_json_sidecar(self) -> str:
        d = asdict(self)
        # plddt_at_anchors is stored JSON-encoded to keep CSV rectangular;
        # invalid JSON here is a schema violation by the emitter — raise.
        d["plddt_at_anchors"] = json.loads(self.plddt_at_anchors or "[]")
        return json.dumps(d, indent=2, sort_keys=False)


CSV_COLUMNS: tuple[str, ...] = ScorerRow.csv_columns()


# ---------------------------------------------------------------------------
# PROPOSE_MANIFEST_COLUMNS — schema for `gpcr-propose` manifest CSV
# ---------------------------------------------------------------------------
#
# Strict superset of the ``refs/rerun_manifest.csv`` columns emitted by
# ``scorer.rerun.build_manifest`` (see rerun.py:807-813). The rerun-manifest
# columns are preserved verbatim so the supervisor / rerun dispatch can
# consume propose-generated manifests without a schema change (Layer 4 of
# the plan silly-leaping-aho.md).
#
# Added by the propose flow:
#   - request_id, biological_question follow the analyst's YAML through
#     the pipeline
#   - state_claim, species, partner_type, partner_identity, partner_perturbation
#     carry the proposal spec into the manifest so per-row provenance is
#     complete
#   - seed_index disambiguates the (backbone × seed) product
#   - receptor_class mirrors the class-aware annotation added in Layer 1
#     of the class-aware work
#   - pre_check_status is the single-tag verdict from the five pre-checks
#     ("pass", "warn_A1", "warn_A2", "warn_A3", "warn_A5", "warn_A6",
#     "warn_multiple")
#   - pre_check_details_json is a JSON string carrying the per-check
#     (status, reason) tuples for downstream forensics
#
# Ordering is stable so downstream consumers can rely on column positions;
# adding a new column here is a schema change and requires a bump.

PROPOSE_MANIFEST_COLUMNS: tuple[str, ...] = (
    # --- rerun_manifest-compatible columns (from rerun.py:807-813) --------
    "prediction_path", "prediction_sha", "experiment_slug", "wave_group",
    "branch", "tier", "backbone",
    "receptor_from_path_substring", "receptor_resolved",
    "disambig_conflict", "receptor_unresolved_in_original",
    "expected_control_json", "new_seed",
    # --- propose-specific additions --------------------------------------
    "request_id", "seed_index",
    "state_claim", "species",
    "partner_type", "partner_identity", "partner_perturbation",
    "receptor_class",
    # Layer 3 additions — materialised input file provenance
    "input_path", "input_sha",
    "pre_check_status", "pre_check_details_json",
    # Exp-Layer 1 additions — seed + ligand context propagated end-to-end
    "seed_used",
    "ligand_type", "ligand_sequence", "ligand_smiles",
    # Diversity-study addition — how many samples one qsub job should emit
    # per seed. Default 1 (backward compatible; every prior manifest is
    # implicitly samples_per_seed=1). Values >1 tell the dispatcher to
    # bump the backbone-specific "samples per fold" flag (Boltz
    # `--diffusion_samples`, OF3 `--num-diffusion-samples`, Protenix
    # `--sample`, Chai `--num-diffn-samples`) so a single job emits N
    # diffusion samples from the same seed.
    "samples_per_seed",
)
