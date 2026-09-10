# 09_references/ — reference audit + paralog cluster map + pinned reference bytes

## Files

- `reference_audit.csv` — 80 rows: per (receptor × role) reference metadata,
  activation class, stabilising elements, `active_stabilization_source`
  (drives E-B-4).
- `paralogy_clusters.csv` — 40 rows: reconstructed cluster map (2026-09-09;
  26 clusters, standard GPCR-family taxonomy).
- `reference_set.blockb_pinned.csv` — reference bytes actually used at
  scoring time. **SHA-256
  `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`** —
  every Block B row's `ref_set_csv_sha256` column pins this exact value.

## SC-B claims supported

- **SC-B-13** (0 new curation errors, 0 changed PDB assignments; 25 native /
  10 chimera-or-miniG / 3 nanobody-stabilised / 2 agonist-only-no-partner =
  37.5 % non-native).

See `claim_answers.csv`.

## Cluster-map caveat (C-B-13)

The cluster map was reconstructed on 2026-09-09 from standard GPCR-family
taxonomy — no on-disk canonical map was found. Phase 0 addendum cites 26
clusters but ships no file. Every bootstrap in this zip uses this
reconstruction.

## Reference-set drift (C-B-9)

Six inactive rows were added post-run (2026-09-06) for AA2AR / ADA1A / ADRB2 /
ADRB2 / CCR5 / CNR1. All six are secondary references; primary inactives for
the three Block B receptors involved (AA2AR / 5NM4, ADRB2 / 6PS2, CNR1 / 5U09)
were present in `6ee2cad8` and are complete on both axes. `delta_to_inactive`
is NOT NaN for those three.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/` and
`refs/reference_set.blockb_pinned.csv`.
