# DATA_DICTIONARY.md — every column in every CSV in this zip

Roll-up of per-file column dictionaries. For row-level column details,
see `01_rows/block_a_rows_dictionary.csv`.


### `01_rows/block_a_rows.csv`
- Rows: 9490
- Columns:
  - `row_id` — int64
  - `receptor` — object
  - `input_state_claim` — object
  - `uniprot` — object
  - `input_path` — object
  - `input_sha256` — object
  - `backbone` — object
  - `arm` — object
  - `seed_outer` — int64
  - `seed_inner` — int64
  - `cell_id` — object
  - `gpcr_class` — object
  - `d_npxxy_oh` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca` — float64
  - `tm6_kink_angle` — float64
  - `delta_to_active` — float64
  - `delta_to_inactive` — float64
  - `rmsd_to_active_ref` — float64
  - `rmsd_to_inactive_ref` — float64
  - `npxxy_active` — bool
  - `tilt_active` — bool
  - `active` — bool
  - `threshold_npxxy_used` — float64
  - `threshold_tilt_used` — float64
  - `threshold_kink_used` — float64
  - `plddt_mean` — float64
  - `plddt_at_anchors` — float64
  - `plddt_at_anchors_list` — object
  - `min_plddt_at_anchor` — float64
  - `n_interface_contacts_ga_receptor` — float64
  - `d_ga_alpha5_r350_ca` — float64
  - `plddt_ga_alpha5` — float64
  - `engaged` — float64
  - `tm6_helicity_6_30_6_50` — float64
  - `tm6_helicity_pass` — bool
  - `excl_E1` — bool
  - `excl_E2` — bool
  - `excl_E3` — bool
  - `excl_E3_tilt` — bool
  - `excl_E3_npxxy` — bool
  - `excl_E4` — bool
  - `excl_E5` — bool
  - `excl_any` — bool
  - `excl_reason` — float64
  - `ref_pdb_sha_active` — object
  - `ref_pdb_sha_inactive` — object
  - `passed` — bool
  - `A1_amino_acid_identity` — float64
  - `A2_fasta_completeness` — float64
  - `A3_wrong_chain` — float64
  - `A4_reference_class_match` — float64
  - `A5_species_match` — float64
  - `A6_receptor_identity` — float64
  - `scorer_git_sha` — object
  - `scorer_version` — object

### `01_rows/block_a_rows_dictionary.csv`
- Rows: 54
- Columns:
  - `column` — object
  - `dtype` — object
  - `units` — float64
  - `allowed_values` — object
  - `nan_convention` — object
  - `source` — object

### `02_references/denominator_populations.csv`
- Rows: 5
- Columns:
  - `population` — object
  - `definition` — object
  - `count` — int64
  - `used_for` — object

### `02_references/reference_metadata.csv`
- Rows: 168
- Columns:
  - `pdb_id` — object
  - `receptor` — object
  - `state` — object
  - `gpcr_class` — object
  - `experimental_method` — object
  - `resolution_A` — float64
  - `deposition_date` — object
  - `fusion_partner` — object
  - `fusion_insertion_range` — object
  - `fusion_in_tilt_window` — bool
  - `fusion_in_npxxy_window` — bool
  - `engineered_mutation_count` — float64
  - `engineered_mutation_positions` — float64
  - `transducer_present` — bool
  - `construct_annotation_on_disk` — object
  - `construct_contradicted_by_rcsb` — float64
  - `predicate_window_hit` — bool
  - `predicate_window_which` — object
  - `entry_json_cached` — bool
  - `is_panel` — bool

### `02_references/reference_predicates.csv`
- Rows: 168
- Columns:
  - `receptor` — object
  - `pdb_id` — object
  - `state` — object
  - `gpcr_class` — object
  - `d_tilt_ref` — float64
  - `d_npxxy_oh_ref` — float64
  - `angle_class_b_kink_ref` — float64
  - `tilt_pass` — bool
  - `npxxy_pass` — object
  - `kink_pass` — float64
  - `expected_pass` — bool
  - `predicate_call` — object
  - `deviation` — bool
  - `deviation_class` — object

### `02_references/reference_separation.csv`
- Rows: 107
- Columns:
  - `receptor` — object
  - `gpcr_class` — object
  - `delta_tilt_ref` — float64
  - `delta_npxxy_ref` — float64
  - `delta_tilt_valid` — bool
  - `delta_npxxy_valid` — bool
  - `axes_valid_for_receptor` — object

### `03_aggregates/cell_summary.csv`
- Rows: 380
- Columns:
  - `receptor` — object
  - `backbone` — object
  - `arm` — object
  - `gpcr_class` — object
  - `n_rows` — int64
  - `d_npxxy_oh_median` — float64
  - `d_npxxy_oh_p25` — float64
  - `d_npxxy_oh_p75` — float64
  - `d_npxxy_oh_p5` — float64
  - `d_npxxy_oh_p95` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca_median` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca_p25` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca_p75` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca_p5` — float64
  - `d_gpcrdb_tm6_tilt_246_637_ca_p95` — float64
  - `delta_to_active_median` — float64
  - `delta_to_active_p25` — float64
  - `delta_to_active_p75` — float64
  - `delta_to_active_p5` — float64
  - `delta_to_active_p95` — float64
  - `rmsd_to_active_ref_median` — float64
  - `rmsd_to_active_ref_p25` — float64
  - `rmsd_to_active_ref_p75` — float64
  - `rmsd_to_active_ref_p5` — float64
  - `rmsd_to_active_ref_p95` — float64
  - `plddt_mean_median` — float64
  - `plddt_mean_p25` — float64
  - `plddt_mean_p75` — float64
  - `plddt_mean_p5` — float64
  - `plddt_mean_p95` — float64
  - `plddt_at_anchors_median` — float64
  - `plddt_at_anchors_p25` — float64
  - `plddt_at_anchors_p75` — float64
  - `plddt_at_anchors_p5` — float64
  - `plddt_at_anchors_p95` — float64
  - `npxxy_active_rate` — float64
  - `tilt_active_rate` — float64
  - `both_fire_rate` — float64
  - `is_broken_cell` — bool

### `03_aggregates/headline_by_backbone.csv`
- Rows: 4
- Columns:
  - `backbone` — object
  - `median_tilt_shift` — float64
  - `median_tilt_shift_cluster_ci_lo` — float64
  - `median_tilt_shift_cluster_ci_hi` — float64
  - `median_tilt_shift_receptor_ci_lo` — float64
  - `median_tilt_shift_receptor_ci_hi` — float64
  - `n_receptors_tilt` — int64
  - `median_delta_to_active_shift` — float64
  - `median_delta_to_active_shift_cluster_ci_lo` — float64
  - `median_delta_to_active_shift_cluster_ci_hi` — float64
  - `median_delta_to_active_shift_receptor_ci_lo` — float64
  - `median_delta_to_active_shift_receptor_ci_hi` — float64
  - `n_receptors_delta` — int64
  - `fraction_of_way_to_active` — float64
  - `fraction_cluster_ci_lo` — float64
  - `fraction_cluster_ci_hi` — float64
  - `fraction_receptor_ci_lo` — float64
  - `fraction_receptor_ci_hi` — float64
  - `n_receptors_fraction` — int64
  - `npxxy_active_rate_panel_mean` — float64
  - `tilt_active_rate_panel_mean` — float64
  - `apo_active_rate_panel_mean` — float64
  - `cognate_active_rate_panel_mean` — float64
  - `matches_claim_sheet` — bool

### `03_aggregates/receptor_summary.csv`
- Rows: 192
- Columns:
  - `receptor` — object
  - `backbone` — object
  - `gpcr_class` — object
  - `apo_d_npxxy_oh_median` — float64
  - `cognate_d_npxxy_oh_median` — float64
  - `apo_d_gpcrdb_tm6_tilt_246_637_ca_median` — float64
  - `cognate_d_gpcrdb_tm6_tilt_246_637_ca_median` — float64
  - `apo_delta_to_active_median` — float64
  - `cognate_delta_to_active_median` — float64
  - `apo_rmsd_to_active_ref_median` — float64
  - `cognate_rmsd_to_active_ref_median` — float64
  - `apo_plddt_mean_median` — float64
  - `cognate_plddt_mean_median` — float64
  - `delta_cognate_minus_apo_tilt` — float64
  - `delta_cognate_minus_apo_npxxy` — float64
  - `delta_cognate_minus_apo_delta_to_active` — float64
  - `fraction_denominator` — float64
  - `fraction_numerator` — float64
  - `fraction_of_way_to_active` — float64
  - `delta_tilt_ref` — float64
  - `delta_npxxy_ref` — float64

### `04_amplitude/amplitude_fits.csv`
- Rows: 24
- Columns:
  - `backbone` — object
  - `axis` — object
  - `inclusion_set` — object
  - `slope` — float64
  - `intercept` — float64
  - `r_squared` — float64
  - `mad` — float64
  - `cluster_ci_lo` — float64
  - `cluster_ci_hi` — float64
  - `receptor_ci_lo` — float64
  - `receptor_ci_hi` — float64
  - `n_receptors` — int64
  - `sd_predictor` — float64

### `04_amplitude/amplitude_points.csv`
- Rows: 384
- Columns:
  - `receptor` — object
  - `backbone` — object
  - `axis` — object
  - `x` — float64
  - `y` — float64
  - `gpcr_class` — object
  - `cluster_id` — object
  - `n_rows_used` — int64
  - `included_baseline` — bool
  - `included_class_a_only` — bool
  - `included_no_holds` — bool

### `04_amplitude/attenuation_sensitivity.csv`
- Rows: 168
- Columns:
  - `backbone` — object
  - `axis` — object
  - `sigma_err` — float64
  - `var_ref` — float64
  - `var_err` — float64
  - `slope_ols` — float64
  - `slope_corrected` — float64
  - `unstable` — bool

### `05_connector/connector_predictions.csv`
- Rows: 512
- Columns:
  - `row_id` — int64
  - `receptor` — object
  - `backbone` — object
  - `arm` — object
  - `seed_used` — int64
  - `stratum` — object
  - `active_predicate_call` — bool
  - `p550_f644_ca_distance` — float64
  - `d_npxxy_oh` — float64
  - `d_tm6_tilt` — float64
  - `rmsd_to_active_ref` — float64
  - `rmsd_to_inactive_ref` — float64
  - `plddt_mean` — float64
  - `input_path` — object
  - `input_sha256_hint` — object
  - `cluster_id` — object

### `05_connector/connector_references.csv`
- Rows: 4
- Columns:
  - `pdb_id` — object
  - `receptor` — object
  - `state` — object
  - `p550_f644_ca_distance` — object
  - `note` — object

### `05_connector/connector_summary.csv`
- Rows: 5
- Columns:
  - `scope` — object
  - `delta_pred_median` — float64
  - `delta_ref_median` — float64
  - `magnitude_ratio` — float64
  - `delta_cluster_ci_lo` — float64
  - `delta_cluster_ci_hi` — float64
  - `n_pred_active_below_inactive_median` — int64
  - `n_pred_active_total` — int64
  - `pct_active_below_inactive` — float64
  - `n_pred_inactive_above_active_median` — int64
  - `n_pred_inactive_total` — int64
  - `pct_inactive_above_active` — float64

### `06_confidence/aa2ar_case.csv`
- Rows: 200
- Columns:
  - `row_id` — int64
  - `receptor` — object
  - `backbone` — object
  - `arm` — object
  - `plddt_mean` — float64
  - `plddt_at_anchors` — float64
  - `min_plddt_at_anchor` — float64
  - `rmsd_to_active_ref` — float64
  - `rmsd_to_inactive_ref` — float64
  - `delta_to_active` — float64
  - `excl_any` — bool

### `06_confidence/plddt_correlations.csv`
- Rows: 12
- Columns:
  - `backbone` — object
  - `aggregation` — object
  - `pearson_r` — float64
  - `spearman_rho` — float64
  - `cluster_ci_lo` — float64
  - `cluster_ci_hi` — float64
  - `receptor_ci_lo` — float64
  - `receptor_ci_hi` — float64
  - `n_rows` — int64
  - `n_receptors` — int64
  - `signed_at_cluster_boot` — bool
  - `primary_or_secondary` — object

### `06_confidence/plddt_per_receptor.csv`
- Rows: 384
- Columns:
  - `backbone` — object
  - `aggregation` — object
  - `receptor` — object
  - `pearson_r` — float64
  - `n_rows` — int64
  - `sign` — object

### `06_confidence/plddt_scatter_points.csv`
- Rows: 9490
- Columns:
  - `row_id` — int64
  - `receptor` — object
  - `backbone` — object
  - `arm` — object
  - `plddt_mean` — float64
  - `plddt_at_anchors` — float64
  - `min_plddt_at_anchor` — float64
  - `rmsd_to_active_ref` — float64
  - `excl_any` — bool

### `07_clusters_and_holdout/cluster_map.csv`
- Rows: 48
- Columns:
  - `receptor` — object
  - `cluster_id` — object
  - `cluster_name` — object
  - `cluster_size` — int64

### `07_clusters_and_holdout/holdout_counts.csv`
- Rows: 4
- Columns:
  - `backbone` — object
  - `cutoff_date` — object
  - `receptor_level_count` — int64
  - `cluster_level_count` — int64
  - `powered` — bool

### `07_clusters_and_holdout/holdout_membership.csv`
- Rows: 192
- Columns:
  - `receptor` — object
  - `backbone` — object
  - `earliest_ga_deposition_date` — object
  - `backbone_cutoff_date` — object
  - `receptor_level_holdout` — bool
  - `cluster_level_holdout` — bool

### `08_exclusions/exclusion_definitions.csv`
- Rows: 5
- Columns:
  - `name` — object
  - `rule` — object
  - `cause` — object
  - `affected_row_count` — int64
  - `affected_receptors` — object

### `08_exclusions/exclusion_sweep.csv`
- Rows: 160
- Columns:
  - `metric` — object
  - `backbone` — object
  - `exclusion_set` — object
  - `value` — float64
  - `baseline_value` — float64
  - `sign_flip` — bool
  - `pct_shift_from_baseline` — float64

### `09_bootstrap_draws/bootstrap_draws.csv`
- Rows: 48000
- Columns:
  - `statistic` — object
  - `backbone` — object
  - `axis` — float64
  - `bootstrap_type` — object
  - `draw` — int64
  - `value` — float64
  - `inclusion_set` — float64

## Missing-data conventions
- Empty string in a CSV cell = missing value.
- Never use `-999`, `0.0`, or any other sentinel for missing.
- Where the source has a sentinel (`anchor_6_30_uniprot_pos = -1`) it
  was converted to empty upstream; downstream tables do not carry it.

## Types
- `bool` columns are stored as literal `True`/`False`.
- `int` columns admit only integers; `float` columns admit NaN as empty.
- Timestamps are ISO-8601 (YYYY-MM-DD).
