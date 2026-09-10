# 03_msa_audit/ — MSA α5-CT column audit + templates-off evidence

## Files

- `PHASE_1_CONSTRUCT_IDENTITY.md` — Phase 1 report; includes Chai `.aligned.pqt`
  audit at α5-CT positions.
- `PHASE_1D_EXTENSION.md` — Boltz + OF3 + Protenix MSA-column audit
  (6 receptors × cognate + decoy × 3 backbones = 36 MSAs).
- `msa_depth_report.md` — MSA depth by backbone × arm (context for the Chai
  partial-read finding).

## SC-B claims supported

- **SC-B-7** (templates off across all 4 backbones — evidence class (b) + (c),
  not (a); no per-row runtime echo).
- **SC-B-9** (decoy α5-CT edit reaches the model as aligned MSA column on
  Boltz + OF3 + Protenix; Chai is a partial-read outlier).

See `claim_answers.csv` for the exact numbers.

## Known gaps

- OF3 raw MSAs are purged post-run (`$TMPDIR/of3-of-sengaad1/colabfold_msas/`);
  column-level inspection is not possible after the fact. Read-through follows
  from the ColabFold-API mechanism verified empirically on Boltz + Protenix.

## Source

Working repo: `docs/BLOCK_B_DOSSIER_PHASE_1_CONSTRUCT_IDENTITY.md`,
`docs/BLOCK_B_DOSSIER_PHASE_1D_EXTENSION.md`, and the msa_depth_report under
`experiments/019_block_b_partner_selection/analysis/`.
