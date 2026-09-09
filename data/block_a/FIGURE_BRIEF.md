# FIGURE_BRIEF.md — proposed panels → source files

This zip is DATA ONLY. All design decisions (colors, layouts, panel arrangements)
are the figure-making agent's. Below is a rough mapping from proposed figure
panels to the tidy CSVs that feed them.

## Panels

### BA-1 — Reference landscape
The reference PDBs' predicate behaviour: which pass their own predicate,
which deviate, and why.
- `02_references/reference_predicates.csv` — per-PDB pass/fail + deviation class
- `02_references/reference_separation.csv` — per-receptor active-vs-inactive gap
- `02_references/reference_metadata.csv` — construct annotations, transducer
  presence, fusion overlap with predicate window
- `02_references/denominator_populations.csv` — 89 / 167 / 127 denominators

### BA-2 — Arm shift
Cognate arm vs apo arm on the two predicate axes and RMSD.
- `01_rows/block_a_rows.csv` (filter with any `excl_*` set)
- `03_aggregates/cell_summary.csv` — per (receptor, backbone, arm)
- `03_aggregates/receptor_summary.csv` — per (receptor, backbone) with cognate−apo shifts
- `03_aggregates/headline_by_backbone.csv` — pooled per-backbone summary + claim-sheet match

### BA-3 — Orthogonal signature (P5.50–F6.44 connector)
- `05_connector/connector_predictions.csv` — n=512 rows of the T2 scale-up
- `05_connector/connector_references.csv` — stub; aggregate refs only (n=77 reconstructible)
- `05_connector/connector_summary.csv` — pooled + per-backbone

### BA-4 — Amplitude regression
Cognate−apo shift on each axis vs the receptor's reference-active vs
reference-inactive gap on the same axis.
- `04_amplitude/amplitude_points.csv` — one point per (receptor, backbone, axis)
- `04_amplitude/amplitude_fits.csv` — slopes + cluster-boot CIs, three inclusion sets
- `04_amplitude/attenuation_sensitivity.csv` — σ_err sweep 0..2 Å

### BA-5 — Confidence vs correctness
- `06_confidence/plddt_correlations.csv` — three aggregations × four backbones
- `06_confidence/plddt_per_receptor.csv` — per-receptor breakdown
- `06_confidence/plddt_scatter_points.csv` — row-level scatter (large; can be
  regenerated from `01_rows/block_a_rows.csv`)
- `06_confidence/aa2ar_case.csv` — AA2AR-only case slice

## Tables

- `03_aggregates/headline_by_backbone.csv` — Table 1 (per-backbone headline)
- `08_exclusions/exclusion_sweep.csv` — Table 2 (every metric under every combo)
- `02_references/reference_metadata.csv` — Supplementary reference audit
- `02_references/denominator_populations.csv` — Supplementary count reconciliation
- `07_clusters_and_holdout/cluster_map.csv` — Supplementary clustering
- `07_clusters_and_holdout/holdout_counts.csv` — Supplementary date-stratified holdout

## Structural exhibits (for figure agent using PyMOL/ChimeraX)

- `11_structures/instrument_schematic/` — β2AR active + inactive (3SN6 + 2RH1)
- `11_structures/confidently_wrong/` — high-pLDDT low-fidelity Class A example
- `11_structures/connector_orthogonality/` — P5.50–F6.44 PIF geometry
- `11_structures/agonist_only_vs_ternary/` — OPRD 6PT2 (agonist-only) vs 8FZQ
- `11_structures/janus_cnr2/` — CNR2 5ZTY (heavily engineered) vs 8GUR
- `11_structures/class_b_kink/` — GLP1R 6X18 + 5VEW kink discriminator
- `11_structures/success_case/` — DRD2/cognate/OF3 median-RMSD row
- `11_structures/broken_cell/` — ACM1/cognate/Protenix broken cell + healthy comparator
