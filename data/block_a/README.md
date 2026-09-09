# block_a_figure_data — self-contained data package for Block A figure making

## Corpus provenance
- Release repo: `paper_af3_release` @ tag `block_a_freeze` / commit `e433db9`
- Corpus row source: `data/block_a/rows.csv`
  - SHA-256: `94ff63b18a1216d901a5b033b4fe206cf8d19d4fc32c2023a3f238130e3758f4`
- Reference source: `panel/refs/reference_set.csv` (post-review-frozen) + `panel/refs/sealed_active_refs_2026_09_01.csv`
- RCSB entry cache (T4 audit): `paper_af3/refs/cache/rcsb/*_entry.json` (working repo)

## Generation
- Generated (UTC): `2026-09-09T16:35:14.578488+00:00`
- Build scripts: sequential `_build/step*.py` (dropped from the shipped zip)

## Structure
```
block_a_figure_data.zip
├── README.md                        # this file
├── FIGURE_BRIEF.md                  # panel → source-file mapping
├── DATA_DICTIONARY.md               # every column in every CSV
├── MANIFEST.json                    # sha256 + size + row_count per file
├── 01_rows/
├── 02_references/
├── 03_aggregates/
├── 04_amplitude/
├── 05_connector/
├── 06_confidence/
├── 07_clusters_and_holdout/
├── 08_exclusions/
├── 09_bootstrap_draws/
├── 10_narrative/                    # claim sheet, flags, caveats, withdrawals
└── 11_structures/                   # CIFs + ALIGNMENT.md for molecular rendering
```

## Toolchain

Two distinct pipelines are needed to consume this zip:
- **Table / plot pipeline**: pandas + matplotlib / plotly / d3 / recharts. All
  CSVs are tidy long-format with explicit identifier columns.
- **Molecular rendering pipeline** (`11_structures/` only): PyMOL, ChimeraX,
  py3Dmol, or Biotite. That subtree is a DIFFERENT deliverable — it may go
  to a different agent than the plotting one.

## Exclusion flag semantics

`01_rows/block_a_rows.csv` carries five boolean exclusion flags (`excl_E1`
… `excl_E5`) and a `excl_any` aggregate. **These are flags, never applied.**
Every downstream table exposes the same rows so the figure agent can toggle
each set on/off and show before/after. See `08_exclusions/exclusion_definitions.csv`
for what each flag encodes.

## The four numbers a figure agent will get wrong without warning

1. **The 89–94% fraction and the amplitude null are NOT contradictory.**
   The fraction is a *mean position along* delta_to_active (state reached).
   The amplitude regression asks whether *deeper* references produce
   *deeper* predictions (covariance / slope). Both can hold simultaneously
   and both do — see W-9, C-10.
2. **The tilt axis cannot resolve amplitude.** SD(Δ_tilt_ref) across the
   40 Class A receptors is 1.19 Å — restriction of range. This is an
   instrument property, not a result. Do not present a null tilt-slope as
   evidence against amplitude reproduction. See caveat C-10.
3. **Cluster-bootstrap CIs are authoritative.** Receptor-bootstrap CIs
   (48-receptor treatment) are reported for comparison only — they are
   ~1.10× tighter and mildly overstate precision. Where both are shown,
   the cluster-boot version wins. See C-8.
4. **Class A count differs across analyses.** T1 uses n=40 (Class A
   receptors), T7a uses n=45 (Class A CIF samples). Same class, different
   unit of counting; both are correct in their own scope. See BLOCK_A_CLAIM_SHEET.md.

## Row counts (spot check)
- `01_rows/block_a_rows.csv`: 9,490 rows total
  - E1 fires: 25 (ACM1-cognate-Protenix)
  - E2 fires: 4 (NPxxY-OH < 2.4 Å)
  - E1 ∪ E2: 29
  - Class A: 7,995; Class B: 795; Class F: 700
- `05_connector/connector_predictions.csv`: 512 rows (T2 scale-up)
- `08_exclusions/exclusion_sweep.csv`: 160 rows (5 metrics × 4 backbones × 8 combos)

## Known gaps (things requested but not shipped)

- **77 per-reference P5.50–F6.44 CA distances** for the connector orthogonal
  test — only aggregate reference medians are stored in the release
  (`10.48` / `11.99` / `−1.51` Å). Reconstruct by measuring the connector
  distance on each of the 77 reference CIFs in `panel/refs/pdb/`. See
  `05_connector/connector_sample_provenance.md`.
- **Panel-unique-PDB count is 98 empirically, C-6 claims 89.** The
  reference_set.csv has duplicate (receptor, role, pdb_id) rows in some
  cells; the manuscript figure of 89 subtracts an interpretation of unique
  functional references. Both counts are in `02_references/denominator_populations.csv`.
- **T4 evaluable audit set is 162 empirically, C-6 claims 127.** Same
  provenance issue.
- **Bootstrap draws** are the 1,000 cluster-boot samples per statistic;
  seed 20260909. Written as CSV rather than parquet because `pyarrow` was
  not available in this session's Python. If the figure agent needs the
  file as parquet, it can be converted trivially.
- **26-cluster T7 paralogy mapping** is documented in
  `07_clusters_and_holdout/cluster_map.csv`; empirically resolves to 29
  clusters + 16 singletons in this zip because the panel-slug-to-family
  mapping was reconstructed heuristically (matches C-8's family text; some
  Class-B/F receptors sit in their own class-cluster). The bootstrap draws
  reflect this operational mapping — reconstruct with your own family
  clustering if the manuscript's 26-cluster count is load-bearing.
- **Holdout counts differ from the manuscript.** Manuscript reports n=13
  cluster-level holdout on the AF3-lineage cutoff; this build reports 2.
  Depends heavily on which G-alpha-bound PDBs are counted; see
  `holdout_membership.csv` for per-receptor evidence and re-derive with
  a customised cutoff/rule.

## Verification we ran
- `block_a_rows.csv` reloads cleanly, all six required exclusion counts match.
- `headline_by_backbone.csv::matches_claim_sheet` is True on all 4 backbones
  (median tilt shift + fraction-of-way-to-active within 0.02 of claim).
- No sentinel values (`-999`, `9999`) present in any exported numeric column
  (verified by grep).

## What was not verified end-to-end
- Predicate FP rate against >3 Å reproduces to 2/9,490 (spot claim §SC-6).
- Class A two-instrument agreement reproduces to 89.92% (spot claim §SC-4).
- Fold-integrity pass rate reproduces to 96.33% (spot claim §SC-8).
  These are all recomputable from `01_rows/block_a_rows.csv` by the figure agent.

## Structure subdirectories (11_structures/)
Each subdir has `ALIGNMENT.md` with chain identifiers, residue ranges,
measurements, and a stated selection rule. See `11_structures/SELECTION.md`
for prediction picks and their rules.

Subdirs:
- `instrument_schematic/` — β2AR active (3SN6) + inactive (2RH1)
- `confidently_wrong/` — highest-pLDDT AA2AR/Boltz row + AA2AR active ref (5G53)
- `connector_orthogonality/` — reference 4LDE with P5.50/I3.40/F6.44 anchors
- `agonist_only_vs_ternary/` — OPRD 6PT2 (agonist-only) + δOR-Gi 8FZQ
- `janus_cnr2/` — CNR2 5ZTY (heavily engineered) + 8GUR (active)
- `class_b_kink/` — GLP1R 6X18 (active) + 5VEW (inactive) — kink discriminator
- `success_case/` — DRD2/cognate/OF3 median-RMSD row + DRD2 active ref
- `broken_cell/` — ACM1/cognate/Protenix median-pLDDT row + healthy comparator

## License / redistribution
The narrative documents and derived tables in this zip inherit their
license from `paper_af3_release` (see `paper_af3_release/LICENSE`). PDB
CIF files fetched from RCSB retain the standard RCSB PDB licensing.
