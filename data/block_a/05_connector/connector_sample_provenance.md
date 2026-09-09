# Connector sample provenance (P2 → T2)

## Original P2 (n=43)
Mixed convenience sample:
- 25 curated per-backbone best/worst/mid CIFs
- AA2AR × 8 arms/backbones
- OPSD/apo/Boltz single case
- 25 random-sampled via `sample(random_state=20260909)` (Python `random.Random`)

## T2 scale-up (n=512)
Stratified across 16 strata (backbone × arm × predicate call → 32 per stratum).
- Backbones: boltz, chai, of3, protenix (4)
- Arms: apo, cognate (2)
- Predicate call: predicate-active vs predicate-inactive (2)
- Sample size per stratum: 32 → 4 × 2 × 2 × 32 = 512

## Physical CIF availability
The 500 CIFs used for the T2 scale-up are NOT in the release archive.
They are reconstructible via:
- `paper_af3_release/structures/block_a/p2_scale_up/_pull.py` (fetch script)
- `paper_af3_release/structures/block_a/p2_scale_up/_pull_manifest.json` (input_sha256 for every selected CIF)
- HPC source: `basel-hpc:/hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test/...`

Each CIF's `input_path` and `input_sha256` are also columned in `05_connector/connector_predictions.csv`.

## Reference distribution (n=77)
The 77 Class A reference PDBs' P5.50–F6.44 CA distances are NOT persisted per-PDB
in the release. Only aggregate medians are available:
- active_median = 10.48 Å
- inactive_median = 11.99 Å
- delta = -1.51 Å

Source: `structures/block_a/p2_scale_up/_analyze.py` (hardcoded from dispatch text).
Reconstructing per-PDB requires measuring d(P5.50 CA − F6.44 CA) on each of the
77 reference CIFs in `panel/refs/pdb/`.
