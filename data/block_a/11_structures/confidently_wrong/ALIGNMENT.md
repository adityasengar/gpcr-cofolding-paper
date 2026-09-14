# confidently_wrong — highest-pLDDT AA2AR/Boltz row above the panel's RMSD tail

## Files
- `AA2AR__apo__boltz__seed748489558__row567.cif` — copied via rsync from /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/018_block_a_switch_test_aa2ar_apo_boltz/a37f8d64c3f9/boltz/seed_748489558/boltz_results_0002/predictions/0002/0002_model_0.cif
- `5G53.cif` — AA2AR active reference (thermostabilised β2AR-A2A construct with ZM241385)

## Selection rule
Per the coordinator's original criterion the target was AA2AR × Boltz with
`rmsd_to_active_ref > 8 Å` — highest pLDDT among such rows. **No Class-A row
in the 9,490-row corpus satisfies RMSD > 8 Å.** The corpus's Class A max
RMSD-to-active is 5.31 Å.
Substituted rule: **AA2AR/Boltz, top-quintile RMSD-to-active, highest pLDDT within that quintile.**
This yields a "maximally confident, maximally mislocated within the panel" row.

Selected row:
- row_id = 567
- arm = apo
- rmsd_to_active_ref = 3.102 Å
- plddt_mean = 73.93
- seed_outer = 748489558
- input_path (HPC): `/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/018_block_a_switch_test_aa2ar_apo_boltz/a37f8d64c3f9/boltz/seed_748489558/boltz_results_0002/predictions/0002/0002_model_0.cif`

## Cell context
AA2AR/Boltz/apo cell median RMSD:
2.941 Å.
This row's percentile ≈ 100% (top of cell).

## Superpose on
Receptor Cα atoms, chain A. Exclude any co-crystallised nanobody or fusion
if present. AA2AR reference 5G53 has chain A + Gs chains — align only against
the receptor 7TM bundle.

## AA2AR numbering (uniprot P29274)
- Y5.58 ≈ Y213
- Y7.53 ≈ Y288
- 2×46 tilt Cα ≈ L88, 6×37 tilt Cα ≈ L235 (verify from GPCRdb)
