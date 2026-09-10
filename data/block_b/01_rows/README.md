# 01_rows/ — tidy long-format row corpus

**32,000 rows**, one per predicted CIF. Every column of `rows.csv` + the RMSD /
pocket / fold-integrity companion files is joined here (see DATA_DICTIONARY.md
for the full list).

Parsed at build time: `arm` and `backbone` from `input_path` (regex
`019_block_b_partner_selection_.+_(apo|decoy|shuffled|cognate)_(boltz|chai|of3|protenix)/`);
`cluster_id` from `09_references/paralogy_clusters.csv`; `active_stabilization_source`
from `09_references/reference_audit.csv`.

## Exclusion flags — never applied

- `excl_E_B_1` — EDNRA / EDNRB / GRPR / HRH3 (all-NaN NPxxY).
- `excl_E_B_2` — OPRD / CNR1 (agonist-only active reference).
- `excl_E_B_3` — AA2AR (recurrent anomaly).
- `excl_E_B_4` — 15 non-native active-reference receptors.
- `excl_any` — logical OR.
- `excl_reason` — text label.

## SC-B claims supported

- **SC-B-10** (grid-complete corpus) — see `claim_answers.csv`.

The row corpus is the substrate for every downstream aggregate in this zip.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/rows.csv`
(+ `.rmsd.csv`, `.pocket.csv`, `.fold_integrity.csv`).
