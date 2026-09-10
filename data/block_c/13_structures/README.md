# Block C — structures/

14 predicted CIFs sampled from Block C Tier 3's landed corpus
(`rows.tier3.v2.csv`, 40,000 passed rows, SHA
`5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`).

Per Block A / Block B convention: **7 targeted picks** carrying the
block's specific story + **7 random picks** as a control, both stated
in writing so a reviewer can check whether the targeted sample was
cherry-picked. Full per-file metadata + selection rule in `MANIFEST.json`.

## targeted/ — 7 CIFs

Sampled to illustrate Block C's story-carrying cells and its flagged
outliers. Every pick states the receptor + reason:

| slot | receptor · backbone · role · arm | dist (Å) | story |
|---|---|---:|---|
| 01 | ACM2 · boltz · antag · apo | 1.65 | Best small-molecule in-pocket (< 2 Å; this is the visual anchor for "the pocket-Cα-RMSD claim looks like when the ligand is exactly where it should be") |
| 02 | DRD3 · chai · decoy · cognate | 80.03 | Worst Chai far-mode (post-v2-fix residual — 175 of 176 remaining ≥ 60 Å rows are on Chai; extends C-C-2 Chai-softness) |
| 03 | CXCR4 · of3 · antag · cognate | 10.53 | Mid-range entrance-bound (8–15 Å; adjudicated as VALID pose per BLOCK_C_WRAP_v2 dispatch) |
| 04 | AGTR1 · of3 · decoy · cognate | 6.42 | AGTR1 biased-agonist-reference flag (C-C-4) — visual context for why AGTR1's inversion is a curation-scope issue, not a docking failure |
| 05 | CXCR2 · of3 · antag · cognate | 6.51 | CXCR2-on-OF3 backbone-specific inversion flag (SC-C-5) — ligand IS in-pocket here; the inversion is a classifier-feature issue, not a docking issue |
| 06 | ADRB2 · boltz · agonist · apo | 6.03 | Agonist arm of the 2×2 pocket-shape comparison (SC-C-1) |
| 07 | ADRB2 · boltz · antag · apo | 3.92 | Antagonist arm of the 2×2 pocket-shape comparison (SC-C-1); pair with slot 06 |

## random/ — 7 CIFs

Uniformly-random-sampled from the Class-A `passed=True` rows,
`random_state = 20260910` (numpy default RNG). Same corpus, no curation.
Provided as a "vs targeted" control — if the targeted picks are a
biased slice, the random picks should look qualitatively different.

| slot | receptor · backbone · role · arm | dist (Å) |
|---|---|---:|
| 01 | OPRK · of3 · antag · apo | 5.89 |
| 02 | HRH1 · boltz · agonist · cognate | 2.86 |
| 03 | ADA2A · boltz · decoy · cognate | 2.83 |
| 04 | CCKAR · protenix · decoy · cognate | 7.64 |
| 05 | CNR1 · chai · antag · cognate | 8.93 |
| 06 | NPY2R · protenix · decoy · apo | 7.17 |
| 07 | ADA2A · of3 · agonist · cognate | 3.05 |

Random median distance ≈ 5 Å (in-pocket) — consistent with the census
finding that 63.4 % of apo × {agonist, antag} rows are in-pocket
(< 8 Å) and 19.8 % are entrance-bound. No random pick landed in the
far-mode tail (that tail is 0.44 % of the corpus, dominated by Chai).

## Sanity-check viewers

Standalone dark-theme single-page 3Dmol.js viewers built to visually
confirm the census's classification of each row are shipped separately
at:

- `../../artefacts/g4_viz_2026_09_10_v2/pose_sanity_clean.html`
  (10 predictions rendered clean — receptor cartoon + ligand sticks,
  matching the `pose_comparison_v2.html` aesthetic).

## Source

- Prediction CIFs live at
  `/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool/…`
  per the manifest at `analysis/block_c/g4_full_census_v2.csv`.
- Census script:
  `code/scripts/block_c_closeout/g4_full_census_v2.py` (once synced to
  release/code/).

## Census summary (from `analysis/block_c/g4_full_census_v2.json`)

- 40,000 Class-A `passed=True` rows measured, 40,000 anchor-hits ≥ 6/6
  (zero low-confidence rows on the v2 receptor-chain picker).
- **Apo arm off-site fraction: 15.1 %** (95 % CI [14.6, 15.6]).
- **Cognate arm off-site fraction: 20.3 %** (95 % CI [19.8, 20.9]).
- **Small-molecule apo × {agonist, antag} off-site: 1.52 %** — the
  SC-C-1-relevant subset is essentially all in-pocket.
- Peptide-agonist rows (6,800 rows across 20 peptide-receptor Class A
  panel members) show median centroid 17.5 Å from pocket-Cα centroid —
  extracellular-vestibule binding by biology, not a docking failure.
- Chai residual far-mode: 175 rows ≥ 60 Å (of 10,200 Chai rows) — 1.7 %
  Chai-specific pathological tail. Extends caveat C-C-2.

## Superseded / retracted from this directory

- The earlier `structures/block_c/README.md` with the "deferred pointer
  to G4" text is superseded by this file.

## Provenance

Selection rules + per-file metadata: `MANIFEST.json`.
