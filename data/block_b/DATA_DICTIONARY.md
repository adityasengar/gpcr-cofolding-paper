# DATA_DICTIONARY — block_b_figure_data

Every column of every CSV shipped in this zip: name, dtype, units, allowed
values, NaN convention, source.

Where a column echoes rows.csv verbatim (e.g. `d_npxxy_y558_y753_oh`), the
"Source" cell points to `experiments/019_block_b_partner_selection/analysis/rows.csv`
in the working repo.

## 01_rows/rows_tidy.csv (32,000 rows)

Tidy long-format merge of `rows.csv` + `rows.rmsd.csv` (join on
`input_sha256`) + `rows.pocket.csv` (join on `input_sha256`) + `rows.fold_integrity.csv`
(join on `input_path`, since fold-integrity file lacks per-row sha per C-B-3),
with parsed arm/backbone and exclusion flags.

### Identifiers

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| receptor_slug | string | — | 40 Class A receptors (see panel of record) | rows.csv:receptor_slug |
| arm | string | — | {apo, decoy, shuffled, cognate} — parsed from input_path | derived at build time |
| backbone | string | — | {boltz, chai, of3, protenix} — parsed from input_path | derived at build time |
| seed_used | string | — | numeric string; 5 distinct seeds per cell | rows.csv:seed_used |
| cluster_id | string | — | 26 paralog clusters | 09_references/paralogy_clusters.csv |
| receptor_class | string | — | Always "class_A" here (Block B is Class A only) | rows.csv:receptor_class |
| input_state_claim | string | — | {apo, decoy, shuffled, cognate} — dispatch-time claim | rows.csv:input_state_claim |

### Scoring provenance

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| scorer_git_sha | string | git-sha40 | `04243c45bdd2285ca195add098a7f333a0d60476` (single value) | rows.csv |
| scorer_version | string | — | Always `0.1.0+04243c45…` | rows.csv |
| ref_set_csv_sha256 | string | sha256hex | `6ee2cad8…` (single value) | rows.csv |
| run_ts_utc | ISO8601 | — | RFC3339 UTC timestamp | rows.csv |
| passed | bool | — | Assertion-pass gate; True on the entire delivered corpus | rows.csv |

### Geometry axes (predicate + descriptive)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| d_npxxy_y558_y753_oh | float | Å | NaN when 7.53 ≠ Y (E-B-1 receptors) or partner Y missing | rows.csv — **primary predicate axis 1** |
| d_gpcrdb_tm6_tilt_246_637_ca | float | Å | NaN if BW numbering incomplete | rows.csv — **primary predicate axis 2** |
| d_tm6_r350_r630_ca | float | Å | Legacy TM6-outward axis | rows.csv |
| d_npxxy_y558_y753_ca | float | Å | Legacy CA-CA NPxxY axis | rows.csv |
| d_tm5_outward_r350_r558_ca | float | Å | Descriptive | rows.csv |
| d_y558_pack_min_heavy | float | Å | Descriptive | rows.csv |
| d_dry_sidechain_r350cz_e630oe1 | float | Å | Descriptive | rows.csv |
| angle_class_b_tm6_kink_639_650_654_deg | float | deg | NaN on Class A rows (Block B is all Class A) | rows.csv |
| icl2_helical_frac | float | fraction 0..1 | Descriptive | rows.csv |

### Reference-anchored scalars (per Class A protocol)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| receptor_d_active_ref | float | Å | median-of-references distance on active side | rows.csv |
| receptor_d_inactive_ref | float | Å | median-of-references distance on inactive side | rows.csv |
| receptor_midpoint | float | Å | (d_active + d_inactive) / 2 | rows.csv |
| delta_to_active | float | Å | observed axis − receptor_d_active_ref (signed) | rows.csv |
| delta_to_inactive | float | Å | observed axis − receptor_d_inactive_ref | rows.csv |
| threshold_npxxy_oh_active_lt | float | Å | `9.082` (single value on 32,000 rows) | rows.csv |
| threshold_gpcrdb_tm6_tilt_active_gt | float | Å | `14.932` (single value on 32,000 rows) | rows.csv |
| thresholds_panel_csv_sha256 | string | sha256hex | pins the panel-threshold table | rows.csv |

### Confidence

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| plddt_mean | float | 0..100 | model-wide mean | rows.csv |
| plddt_at_anchors | float | 0..100 | mean pLDDT at the 6 BW anchors | rows.csv |
| min_plddt_at_anchor | float | 0..100 | min over the 6 anchors | rows.csv |
| confidence_flag | string | — | {ok, low_min_plddt, …} | rows.csv |

### Partner geometry (α5-CT interface)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| d_ga_alpha5_r350_ca | float | Å | α5-CT tip → R3.50 Cα; NaN on apo (no partner chain) | rows.csv |
| n_interface_contacts_ga_receptor | int | count | interface heavy-atom contacts; NaN on apo | rows.csv |
| plddt_ga_alpha5 | float | 0..100 | mean pLDDT of α5-CT residues; NaN on apo | rows.csv |

### RMSD (from rows.rmsd.csv)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| rmsd_to_active_ref | float | Å | 7TM-only Cα RMSD to closest active reference | rows.rmsd.csv |
| rmsd_to_inactive_ref | float | Å | 7TM-only Cα RMSD to closest inactive reference | rows.rmsd.csv |
| rmsd_pos | int | count | number of positions used | rows.rmsd.csv |
| rmsd_n_residues_used | int | count | residue count | rows.rmsd.csv |
| rmsd_note | string | — | completeness-gate note | rows.rmsd.csv |

### Pocket (from rows.pocket.csv, scorer commit `fd87133`)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| pocket_ca_rmsd | float | Å | pocket-residue Cα RMSD | rows.pocket.csv |
| pocket_sidechain_rmsd | float | Å | pocket-residue side-chain RMSD | rows.pocket.csv |
| w648_chi1 | float | deg | tryptophan 6.48 chi1 rotamer | rows.pocket.csv |
| ligand_rmsd_to_ref | float | Å | ligand-heavy-atom RMSD; NaN on apo/decoy/shuffled | rows.pocket.csv |
| pocket_notes | string | — | | rows.pocket.csv |

### Fold integrity (from rows.fold_integrity.csv; C-B-3)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| tm6_helicity_6_30_6_50 | float | fraction 0..1 | H/G/I DSSP fraction over BW 6.30–6.50 | rows.fold_integrity.csv |
| chain_breaks | int | count | receptor-chain break count | rows.fold_integrity.csv |
| ramachandran_outlier_frac | float | 0..1 | receptor Cα Ramachandran outlier fraction | rows.fold_integrity.csv |
| icl3_modelled_count | int | count | ICL3 residues modelled | rows.fold_integrity.csv |
| icl3_range | string | — | ICL3 residue-range string | rows.fold_integrity.csv |
| fold_integrity_load_error | string | — | load-side error (empty on success) | rows.fold_integrity.csv:load_error |

### Construct metadata (from donor_ga_class.csv per Phase 1)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| donor_ga_identity | string | — | e.g. `alphas`; empty on apo rows | donor_ga_class.csv |
| donor_ga_class | string | — | {Gs, Gi, Gq, G12/13, Gt}; empty on apo | donor_ga_class.csv |
| cognate_ga_identity | string | — | e.g. `alphai1` | donor_ga_class.csv |
| cognate_ga_class | string | — | {Gs, Gi, Gq, G12/13, Gt} | donor_ga_class.csv |
| active_stabilization_source | string | — | {native, mini_G, chimera, nanobody, scFv, agonist_only} | reference_audit.csv |

### Ligand (mostly empty on Block B — no ligand arms)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| ligand_type | string | — | empty on Block B | rows.csv |
| ligand_sequence | string | — | empty on Block B | rows.csv |
| ligand_smiles | string | — | empty on Block B | rows.csv |

### Assertion columns (empty on passed=True by design)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| A1_amino_acid_identity | string | — | Raise-name on failure only; empty on success | rows.csv |
| A2_fasta_completeness | string | — | Raise-name on failure only; empty on success | rows.csv |
| A3_wrong_chain | string | — | Raise-name on failure only; empty on success | rows.csv |
| A4_reference_class_match | string | — | Raise-name on failure only; empty on success | rows.csv |
| A5_species_match | string | — | Raise-name on failure only; empty on success | rows.csv |
| A6_receptor_identity | string | — | Raise-name on failure only; empty on success | rows.csv |
| pre_check_status | string | — | {ok, …} | rows.csv |

### Provenance IDs

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| input_path | string | absolute HPC path | preserved verbatim | rows.csv |
| input_sha256 | string | sha256hex | per-CIF byte hash | rows.csv |
| cache_key | string | — | scorer-side cache key | rows.csv |

### Exclusion flags (never applied)

| Column | dtype | Units | Allowed / NaN | Source |
|---|---|---|---|---|
| excl_E_B_1 | bool | — | True for EDNRA/EDNRB/GRPR/HRH3 | derived (10_exclusions/exclusion_definitions.csv) |
| excl_E_B_2 | bool | — | True for OPRD/CNR1 | derived |
| excl_E_B_3 | bool | — | True for AA2AR | derived |
| excl_E_B_4 | bool | — | True for 15 non-native-active receptors | derived |
| excl_any | bool | — | logical OR of the four | derived |
| excl_reason | string | comma-separated | matching reason labels | derived |

---

## 04_ladder/ladder_four_scorings.csv (40 rows)

Ladder rate per (frame, arm, backbone) — 2 frames × 4 arms × 5 backbone strata
= 40 rows.

| Column | dtype | Notes |
|---|---|---|
| frame | string | {all_40, reproduction_36} |
| arm | string | {apo, decoy, shuffled, cognate} |
| backbone | string | {boltz, chai, of3, protenix, panel_all} |
| n_rows | int | rows contributing to the cell |
| binary_predicate | float | two-instrument active-call fraction |
| per_receptor_midpoint_mean | float | mean of per-receptor midpoint distances |
| per_receptor_midpoint_median | float | median |
| delta_to_active_median | float | median observed − active-ref |
| logit_active_fraction | float | logit with ε = 1/8000 continuity |
| cluster_boot_ci_lo_binary | float | 26-cluster bootstrap CI low |
| cluster_boot_ci_hi_binary | float | 26-cluster bootstrap CI high |
| n_receptors | int | receptor count contributing |

## 04_ladder/ladder_continuous_distributions.csv (96 rows)

(arm × backbone × axis) medians, percentiles, IQR on the geometry axes.

Columns: `arm, backbone, axis, n, median, p5, p25, p75, p95, iqr`. `axis` ∈
{d_npxxy_y558_y753_oh, d_gpcrdb_tm6_tilt_246_637_ca, delta_to_active,
delta_to_inactive, rmsd_to_active_ref, rmsd_to_inactive_ref}.

## 04_ladder/ladder_threshold_proximity.csv (32 rows)

Fraction of rows in the ±0.5 Å band around each axis threshold, per (arm ×
backbone). See dossier §3b for interpretation.

## 04_ladder/ladder_adjacent_pair_separation.csv (24 rows)

Adjacent-pair median shift + pooled IQR per (arm-pair × backbone). Columns
include `arm_from, arm_to, backbone, median_shift, pooled_iqr,
signals_beyond_iqr_bool`.

## 04_ladder/ladder_per_receptor.csv (160 rows)

Per-receptor × backbone rates on every arm, with `ceiling_pinned` and
`floor_pinned` flags. Columns: `receptor, backbone, cluster, apo_rate, apo_n,
apo_n_nan_np, decoy_rate, decoy_n, decoy_n_nan_np, shuffled_rate, shuffled_n,
shuffled_n_nan_np, cognate_rate, cognate_n, cognate_n_nan_np,
delta_apo_to_decoy, delta_decoy_to_shuffled, delta_shuffled_to_cognate,
ceiling_pinned, floor_pinned, all_nan_np_arm`.

## 04_ladder/midpoint_ladder_28.csv (13 rows)

Enumeration of 28-receptor subsets attempted for the dispatch-cite
0.130/0.500/0.801/0.887 reproduction. See W-B-2.

## 05_decomposition/ladder_decomposition.csv (60 rows)

Telescoping decomposition on both scales per (frame × backbone × contrast).

Columns: `frame, backbone, contrast, scale, term_estimate, term_share,
total_apo_to_cognate, ci_lo, ci_hi`. `contrast` ∈
{delta_occupancy_apo_to_decoy, delta_a5ct_sequence_decoy_to_shuffled,
delta_correct_family_shuffled_to_cognate}. `scale` ∈ {probability, logit}.

## 05_decomposition/ladder_decomposition_bootstrap_draws.csv (30,000 rows)

Per-draw estimates. Columns: `draw_id, backbone, frame, contrast, scale,
term_estimate`. 1,000 draws × 3 contrasts × 2 scales × 5 backbone strata.

## 06_interface/interface_2x2.csv (480 rows)

2 frames × 2 predicates × 6 cutoffs × 4 arms × 5 backbone strata.

Columns: `frame, predicate, cutoff_A, arm, backbone, n, n_engaged, p_engaged,
p_engaged_lo95, p_engaged_hi95, p_active_given_engaged, p_agv_lo95, p_agv_hi95,
n_engaged_but_inactive`.

## 06_interface/interface_continuous.csv (640 rows)

Per (receptor × arm × backbone) cell:

Columns: `receptor_slug, arm, backbone, tip_median, tip_p25, tip_p75,
contacts_total_median, plddt_alpha5_median, npxxy_median, tilt_median,
active_frac, n_rows, pif_d_5_50_3_40_ca, pif_d_3_40_6_44_ca, pif_sum_ca,
n_contacts_TM3, n_contacts_TM5, n_contacts_TM6, contact_register_last5_json,
bsa_A2, partner_tail11_helicity_frac, partner_chain_id, n_partner_aa,
cell_active_predicate, cell_engaged_20, cell_engaged_but_inactive`.

Values in `contact_register_last5_json` are JSON arrays of receptor BW
positions in contact with the last 5 partner residues on the cell's
representative CIF.

## 06_interface/interface_pif_connector.csv (640 rows)

Per cell PIF connector geometry.

Columns: `receptor_slug, arm, backbone, pif_d_5_50_3_40_ca, pif_d_3_40_6_44_ca,
pif_sum_ca, npxxy_median, tilt_median, tip_median, cell_active, cell_engaged_20,
cell_engaged_but_inactive`.

## 06_interface/interface_fold_integrity.csv (16 rows)

Per (arm × backbone) fold integrity summary.

Columns: `arm, backbone, n, n_with_tm6_helicity,
median_tm6_helicity_6_30_6_50, p_tm6_helical_pass_ge_0p8, tm6_pass_lo95,
tm6_pass_hi95, median_chain_breaks, median_ramachandran_outlier_frac`.

## 06_interface/interface_chai_plddt_inversion.csv (8 rows)

Block A pLDDT-inversion tell replicated per (arm × backbone) — reported
unmeasurable at Block B scale on Chai (only 5 non-engaged cognate rows in
2,000). See C-B-2, Flag B-2.

## 07_donor_residuals/donor_class_residuals.csv (32,000 rows)

Per-row residuals against each receptor's active + inactive references, along
with donor / cognate Gα class labels for the row's arm.

Columns include: `input_sha256, receptor, arm, backbone, donor_ga_class,
cognate_ga_class, active_stabilization_source, residual_tilt, residual_npxxy,
residual_delta_to_active, ...`.

## 07_donor_residuals/donor_class_residuals_summary.csv (270 rows)

Per (backbone × donor_class × cognate_class × axis) summary with cluster-boot
CIs. Columns: `backbone, donor_ga_class, cognate_ga_class, n_receptors,
n_rows_axis, axis, median, ci_lo, ci_hi, note`.

## 07_donor_residuals/donor_class_residuals_bootstrap_draws.csv (180,000 rows)

Per-draw estimates. Seed `20260909`. Columns: `draw_id, backbone,
donor_ga_class, cognate_ga_class, axis, statistic, value`.

## 07_donor_residuals/phase5_power_analysis.csv (45 rows)

Native-only re-run per (backbone × donor_class × cognate_class × axis).
Columns: `backbone, donor_ga_class, cognate_ga_class, axis, total_n_rec,
native_n_rec, chimera_n_rec, all_median, all_ci_lo, all_ci_hi, native_median,
native_ci_lo, native_ci_hi, chimera_median, chimera_ci_lo, chimera_ci_hi`.

## 07_donor_residuals/donor_class_covariate_regression.csv (30 rows)

Absolute-residual regression against `alpha5_donor_class` (native vs
chimera-or-mini_G-or-Gt) controlled for cognate family. Columns include
`backbone, axis, slope, ci_lo, ci_hi, n`.

## 08_covariates/ladder_height_covariates.csv (40 rows)

Per-receptor derived covariates.

Columns: `receptor, family_term_continuous, family_term_logit, active_npxxy,
active_tilt, inactive_npxxy, inactive_tilt, delta_ref_npxxy, delta_ref_tilt,
cognate_family, n_ga_families, deposition_count, saturation_frac_backbones,
cluster_id`.

## 08_covariates/ladder_height_regressions.csv (80 rows)

Panel regressions per (backbone × predictor × outcome_scale), with AA2AR
sensitivity. Columns: `backbone, predictor, outcome_scale, n_receptors_all,
slope_all, ci_lo_all, ci_hi_all, n_receptors_no_aa2ar, slope_no_aa2ar,
ci_lo_no_aa2ar, ci_hi_no_aa2ar`.

## 09_references/reference_audit.csv (80 rows)

Per (receptor × role) reference audit.

Columns: `receptor, role, pdb_id, method, resolution, stabilising_elements,
construct, alpha5_donor_class, active_stabilization_source, activation_class,
deviation_class, pending_annotation_correction, correction_note,
missing_inactive_flag, notes, ref_source`.

## 09_references/paralogy_clusters.csv (40 rows)

Cluster map (reconstructed 2026-09-09).

Columns: `receptor, cluster_id, reconstructed, reconstruction_source, note`.

## 09_references/reference_set.blockb_pinned.csv

Reference bytes actually used at scoring time. SHA-256
`6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`. Do NOT
edit — this is a reproducibility pin, not a live file.

## 10_exclusions/exclusion_definitions.csv (5 rows)

The four E-B flags plus `excl_any`. Columns: `flag, members, n_receptors,
rationale, claim_sheet_reference`.

## 10_exclusions/exclusion_counts.csv (5 rows)

Row-count effect if each flag is applied singly.

Columns: `flag, n_receptors, n_rows_fired, n_rows_remaining_if_applied,
total_rows`.

## 10_exclusions/exclusion_membership.csv (40 rows)

Per-receptor boolean membership + reason label.

Columns: `receptor_slug, excl_E_B_1, excl_E_B_2, excl_E_B_3, excl_E_B_4,
excl_any, reason`.

## 11_bootstrap_draws/

Duplicates of both `ladder_decomposition_bootstrap_draws.csv` and
`donor_class_residuals_bootstrap_draws.csv` collected in one directory for
figure-agent convenience. See dictionary entries for §05 and §07.

## 12_narrative/

Copied verbatim from the working repo:

- `BLOCK_B_CLAIM_SHEET.md` — 13 SC-B surviving claims + published numbers +
  cluster-boot CIs + qualifiers.
- `BLOCK_B_MANUSCRIPT_FLAGS.md` — every flag with status labels.
- `EXPERIMENT_DOSSIER_BLOCK_B.md` — full experimental narrative.
- `caveats/C-B-*.md` — 16 live caveats.
- `withdrawals/W-B-*.md` — 6 retractions with corrected sentences where
  applicable.
- `figures/BB-*.md` — 6 figure specifications (panel-by-panel design + source
  CSV pointers).

## Claim-answer summary CSVs

Every `claim_answers.csv` (in 01_rows, 02_constructs, 03_msa_audit, 04_ladder,
05_decomposition, 06_interface, 07_donor_residuals, 08_covariates,
09_references) has columns: `claim_id, metric, observed_value, ci_lo, ci_hi,
source_file, matches_claim_sheet_bool`. `observed_value` is the number as
stated in `BLOCK_B_CLAIM_SHEET.md`; recompute from the tidy source to verify.
