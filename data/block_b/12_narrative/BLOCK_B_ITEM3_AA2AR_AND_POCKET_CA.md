# Block B — Item 3: pocket-Cα RMSD table and AA2AR adjudication

Deliverables:
- Table: `experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`
  (40 rows, one per Block B receptor)
- Report: this file

Bounded scope: 40 Block B receptors, all Class A. No new predictions, no
edits outside the ownership list, no push/tag/commit.

## 1. Method

### 1a. Pocket residue selection

The 12 pocket-Cα BW positions come verbatim from
`scorer/pocket_metrics.py:81-86` (`POCKET_BW_LABELS`):

```
3.32, 3.33, 3.36
5.42, 5.43, 5.46
6.48, 6.51, 6.52, 6.55
7.39, 7.42
```

Class A only; Block B panel is Class A only (Class B = 4 receptors in
Block A; Class F = 4 in Block A; neither carries into Block B) so the
pocket definition applies to every row.

Per-receptor BW → UniProt-position mapping comes from the GPCRdb
`residues/extended/<entry>/` cache under
`refs/cache/gpcrdb/residues_ext_<uniprot_slug>.json` — the campaign's
canonical BW source (see `scorer/bw_numbering.py:118-150` and
`docs/BW_SOURCE.md`). Every one of the 12 pocket labels resolved on all
40 receptors (`n_pocket=12` on every row).

### 1b. CIF source

Reference CIFs come from
`paper_af3_release/panel/refs/cifs/` — the 92-CIF Block-A dossier
bundle:
`/Users/SENGAAD1/Documents/claude/paper_af3_release/panel/refs/pdb/`.

Full coverage: all 40 active + 40 inactive PDBs present. Sealed active
refs (8 receptors: ACM1/6OIJ, ADA2A/9CBL, ADRB1/7BU7, CCKAR/7MBX,
DRD3/8IRT, EDNRA/8HCQ, HRH3/8YUU, OX2R/7L1V — from
`refs/sealed_active_refs_2026_09_01.csv`) all present in the same
directory. `cif_source_note` on each row records the two file paths.

### 1c. Alignment method

For every (active, inactive) pair:

1. Build a UniProt-numbered residue model for each PDB via
   `scorer.structure.build_uniprot_model` (same path the production
   scorer uses — chain selection through `select_chain`, then
   deposited-or-aligned numbering per `_score_deposited` /
   `_score_aligned`).
2. Kabsch alignment (`gemmi.superpose_positions`) on the common set of
   7TM CAs, where "7TM" means all UniProt positions annotated
   `TM1`..`TM7` by GPCRdb (via `tm_positions_from_bw_map`, same rule as
   `scripts/rescore_rmsd.py`). No manual TM cut-points, no ECD/ICL3/
   N-term/C-term inclusion; H8 is excluded.
3. Apply the Kabsch transform to the active pocket Cα atoms; compute
   root-mean-square residue-wise distance to the inactive pocket Cα
   atoms in the shared frame.

Common TM-CA counts range 206–244 across the 40 pairs; every pair
comfortably clears the `MIN_KABSCH_CA=20` floor
(`scorer/pocket_metrics.py:98`).

## 2. Results

### 2a. Distribution (Å)

    n   min   Q1    median  Q3    max   mean
    40  0.53  1.03  1.23    1.55  1.90  1.25

Pocket-Cα RMSD is bounded, unimodal-looking, and centred on ~1.2 Å.

### 2b. Bottom-5 (smallest reference separation)

| Rank | Receptor | Active / inactive PDB | pocket_ca_rmsd (Å) | Δ npxxy_ca (Å) | Δ tilt (Å) |
|------|----------|-----------------------|--------------------|----------------|------------|
| 1    | 5HT1B    | 6G79 / 4IAR           | 0.532              | −2.693         | +3.795     |
| 2    | APJ      | 8XZH / 8S4D           | 0.629              | −4.702         | +2.292     |
| 3    | CNR2     | 8GUR / 5ZTY           | 0.780              | −3.583         | +4.888     |
| 4    | FSHR     | 8I2G / 8I2H           | 0.798              | −0.366         | +5.273     |
| 5    | EDNRB    | 8IY5 / 6IGK           | 0.820              | −0.743         | +2.724     |

### 2c. Top-5 (largest reference separation)

| Rank | Receptor | Active / inactive PDB | pocket_ca_rmsd (Å) |
|------|----------|-----------------------|--------------------|
| 40   | LSHR     | 7FIH / 7FIJ           | 1.900              |
| 39   | AGTR1    | 6OS2 / 4ZUD           | 1.872              |
| 38   | OPSD     | 4X1H / 7ZBC           | 1.849              |
| 37   | CXCR2    | 6LFO / 6LFL           | 1.734              |
| 36   | GHSR     | 7NA7 / 7F83           | 1.710              |

### 2d. AA2AR-specific row

| Metric                                     | Value    | Rank among 40                        |
|--------------------------------------------|----------|--------------------------------------|
| pocket_ca_rmsd (Å)                         | 1.6195   | **34 / 40** (higher = more separation) |
| Δ_ref d_npxxy_ca (Å)                       | −5.1080  | 34 / 40 by |Δ| ascending (higher = more separation) |
| Δ_ref d_gpcrdb_tm6_tilt (Å)                | +6.1038  | 31 / 40 by |Δ| ascending             |

AA2AR (5G53/5NM4) sits in the top third of the panel on ALL THREE
reference-separation axes. It is not unusually close on any of them.

## 3. AA2AR footnote adjudication

**Hypothesis** — the five AA2AR anomalies (Block A anti-calibration;
Block C bimodality; Block B family-term +0.76 on Boltz; ladder-height
covariate slope driver; E1 ruler fragility) share a single structural
cause: the AA2AR active + inactive reference PDBs are unusually close,
so any per-cell metric is inside the reference-noise floor and each
anomaly is actually the same fact repeated.

**Verdict** — **NOT SUPPORTED**. AA2AR ranks 34/40 (well above the
median) on pocket-Cα, 34/40 on npxxy-CA reference-Δ, 31/40 on tilt
reference-Δ. On every axis tested the AA2AR active↔inactive separation
is larger than that of a majority of Block B receptors. If closeness of
reference structures were the shared cause, AA2AR should have been in
the bottom-5 (say, sub-1 Å pocket) on at least one axis; it is not on
any.

The five anomalies remain independent. They need separate footnotes.

## 4. Cross-check against Block A's degenerate-pair candidates

Block A flagged three receptors as having small axis-Δ proxy reference
separations (`d_r350_r630_ca` and `d_npxxy_oh`): OPRD (0.49 Å), FZD6
(1.03 Å, Class F, out of Block B scope), 5HT1B (1.33 Å).

- **5HT1B** — Block A axis-Δ ≈ 1.33 Å → pocket-Cα RMSD = 0.532 Å,
  rank **1/40**. The two axes AGREE at the top: 5HT1B is the closest
  reference pair in Block B by pocket-Cα, and Block A saw it small on
  axis-Δ too. Confirmed degenerate pair.
- **OPRD** — Block A axis-Δ ≈ 0.49 Å (very small) → pocket-Cα RMSD =
  1.082 Å, rank **15/40**. The pocket-Cα axis does NOT reproduce OPRD
  as an outlier. Block A's OPRD signal is axis-specific (NPxxY OH-OH
  and/or 3.50–6.30) — the pocket residues sit outside the domain the
  axis-Δ is measuring, so pocket-Cα captures a different aspect of the
  same active/inactive contrast. Not degenerate on pocket geometry.
- **FZD6** — Class F, out of Block B panel; not evaluated here.

Interpretation: axis-Δ proxy closeness and pocket-Cα closeness are
correlated but not identical. 5HT1B is small on both; OPRD is small on
the anchor-atom axis-Δ only. Downstream applicability-domain filters
should use whichever axis matches the metric they are gating on.

## 5. Verdict for Block C

The pocket-Cα RMSD table is available at:

    experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv

Columns:
`receptor, active_pdb, inactive_pdb, pocket_ca_rmsd_A,
 delta_ref_npxxy_A, delta_ref_tilt_A, pocket_ca_rank_of_40,
 cif_source_note, n_pocket, n_common_tm, tm_kabsch_rmsd_A, status,
 pocket_missing`

Every row is `status=ok, n_pocket=12` — no receptor was skipped, no BW
label went missing, no Kabsch failed. Ready to feed Block C's
applicability-domain analysis as an a priori structural discriminator
independent of any empirical failure list.

Suggested next step (deferred out of this dispatch): join the
per-receptor pocket_ca_rmsd_A onto Block C's Tier-3 per-cell result
table and check whether cells whose reference pair sits in the
bottom-quartile (pocket_ca_rmsd < 1.03 Å, 10 receptors) systematically
under-perform two-instrument agreement vs the top-quartile.

## 6. Provenance and audit

- Compute driver: `/tmp/compute_pocket_ca_rmsd.py` (session-scratch,
  not committed).
- Pocket definition source: `scorer/pocket_metrics.py:81-86`
  (`POCKET_BW_LABELS`), 12 positions.
- BW-to-UniProt map source: `refs/cache/gpcrdb/residues_ext_<slug>.json`
  (cached GPCRdb `residues/extended/`), same source the scorer uses.
- 7TM Kabsch definition: `scorer.pocket_metrics.tm_positions_from_bw_map`,
  which returns positions whose GPCRdb `protein_segment` is one of
  TM1..TM7. Same rule as `scripts/rescore_rmsd.py`.
- Reference role map: `experiments/019_block_b_partner_selection/analysis/reference_audit.csv`.
- Active-role PDBs pulled from `refs/reference_set.blockb_pinned.csv`
  and `refs/sealed_active_refs_2026_09_01.csv` (sealed subset:
  ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R).
- Reference deltas `d_npxxy_ca_ref` and `d_gpcrdb_tm6_tilt_ref` from
  the same two pinned CSVs (`delta_ref_*` columns = active − inactive
  for the same numeric field).

No commits, no push, no tag. This report and the CSV are the two
deliverables.
