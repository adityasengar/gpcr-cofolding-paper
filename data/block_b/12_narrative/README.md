# 12_narrative/ — claim sheet, flags, caveats, withdrawals, dossier, figures

All files here are **copied verbatim** from the working repo. Diff against
those originals if provenance matters — no reformatting or truncation was
applied.

## Contents

- `BLOCK_B_CLAIM_SHEET.md` — 13 SC-B surviving claims with published numbers,
  cluster-boot CIs, exclusion sets, and qualifier pointers.
- `BLOCK_B_MANUSCRIPT_FLAGS.md` — every flag with `text_only` /
  `data_pending` / `open_decision` / `resolved` labels.
- `EXPERIMENT_DOSSIER_BLOCK_B.md` — full experimental dossier
  (Phases 0..6 with gate summaries + numeric findings).
- `caveats/C-B-*.md` — 16 live caveats (structural limitations of surviving
  claims — belong in Methods / Limitations, not Results / Withdrawals).
- `withdrawals/W-B-*.md` — 6 retractions with reason, evidence, dossier
  reference, and the corrected sentence where one exists.
- `figures/BB-1_ladder_binary_predicate.md` .. `figures/BB-6_per_receptor_ladder.md`
  — 6 panel specifications with source-CSV pointers.

## Distinction from Block A

Block A caveats and withdrawals use `C-N` / `W-N` (no prefix); Block B uses
`C-B-N` / `W-B-N`. Some Block B items are Block-B-specific (C-B-2 Chai partial
MSA read; C-B-13 reconstructed cluster map); others (C-B-8 AA2AR) are
structurally similar to Block A items but re-derived on Block B evidence.

## What if the figure agent finds a number that disagrees?

- If the recomputed value falls **outside cluster-boot 95 % CI** of the claim
  sheet value, treat that as a discrepancy — surface it in the caption and
  ping the campaign lead.
- If it falls inside CI but drifts on the third decimal, the claim sheet's
  value is authoritative; the figure caption can use the claim-sheet value.
- Missing values (NaN) that the figure agent computes but the claim sheet
  doesn't list are usually the frame_40 side of a frame_36 headline — check
  the frame filter first.
