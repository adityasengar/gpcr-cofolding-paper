# success_case — DRD2/cognate/OF3 median-RMSD row

## Files
- `DRD2__cognate__of3__seed849213874__row8285.cif` — copied via rsync
- `7JVR.cif` — DRD2 active reference.

## Selection rule
Median-RMSD row within the DRD2/cognate/of3 cell, after excl_any filter
(excludes the E1–E5 sweep sets). Row index = 12 of 25
non-excluded rows; percentile = 50.0%.

Selected row:
- row_id = 8285
- rmsd_to_active_ref = 1.218 Å
- plddt_mean = 65.34
- active (predicate call) = True
- seed_outer = 849213874
- input_path (HPC): `/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test_of3_rerun_2026_09_02/018_block_a_switch_test_drd2_cognate_of3/72924d3fb711/of3/seed_849213874/018_block_a_switch_test_drd2_cognate_of3_DRD2_of3_1/seed_43716199/018_block_a_switch_test_drd2_cognate_of3_DRD2_of3_1_seed_43716199_sample_1_model.cif`

## Superpose on
Chain A receptor Cα, TM1–TM7. Exclude Gα/Gβ/Gγ heterotrimer chains present
in the cognate-arm prediction. Exclude any co-modeled fusion.

## DRD2 numbering (uniprot P14416)
- Y5.58 ≈ Y208
- Y7.53 ≈ Y399
- BW anchors from `rows.csv:anchor_*_uniprot_pos` for this row.
