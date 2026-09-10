# 06_interface/ — interface geometry (CPU rescoring pass)

## Files

- `interface_continuous.csv` — 640 rows: per (receptor × arm × backbone) cell,
  tip depth, contacts, DSSP helicity, contact register, BSA.
- `interface_2x2.csv` — 480 rows: p(engaged) × p(active|engaged) per
  (frame × predicate × cutoff × arm × backbone stratum). Cutoffs {10, 12, 14,
  16, 18, 20} Å.
- `interface_pif_connector.csv` — 640 rows: P5.50–I3.40–F6.44 Cα-Cα PIF-sum
  per cell; orthogonal per-prediction axis for SC-B-4.
- `interface_fold_integrity.csv` — 16 rows: TM6 helicity pass rate per
  (arm × backbone).
- `interface_chai_plddt_inversion.csv` — 8 rows: Block A pLDDT-inversion tell
  attempted on Block B (Chai cognate only 5 non-engaged rows in 2,000 —
  unmeasurable; C-B-2, Flag B-2).

## SC-B claims supported

- **SC-B-3** (2×2 reproduction).
- **SC-B-4** (PIF connector on decoy engaged-but-inactive sits at apo).
- **SC-B-5** (TM6 helicity 0.988 panel-wide; stronger than Block A 0.963).
- **SC-B-12** (contact register: canonical Class A binding face across all
  arms).

See `claim_answers.csv`.

## Cutoff-sensitivity rule (C-B-6)

The 20 Å engagement cutoff is permissive at cognate (4× median cognate depth
12.19 Å) but load-bearing at decoy. Report both 14 Å and 20 Å where the
result is close.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
