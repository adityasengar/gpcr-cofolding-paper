# C-7 — "Apo" is not a physical state

## Caveat

Block A's "apo" arm is a computational reference condition, not a physical
state. There is no ligand, no partner, no membrane, no basal-activity
equivalent — the model is given just the receptor sequence and asked to
predict a structure. Physical apo receptors have basal activity that varies
substantially across receptors (GHSR, CB1, several 5-HT and melanocortin
receptors show high constitutive activity; most peptide receptors show
near-zero).

## Affects

- Any manuscript sentence framing "apo bistability" as a real biological
  property that the model recovers. The bistability is a property of the
  model's behaviour under a specific computational condition, not
  necessarily a biological property.
- Any comparison of apo-active rate to published constitutive activity.
  The demoted-P5 correlation analysis (constitutive activity rank vs
  apo-active rate) would test this, but literature constitutive-activity
  rankings are assay-dependent and contestable; a flat result would tell
  us little.

## Evidence

- Post-review dispatch Q6: "'Apo' is not a physical state".
- MANUSCRIPT_FLAGS.md Flag 12.

## Manuscript sentence

> The "apo" arm is a computational reference condition (receptor sequence,
> no ligand, no partner, no membrane) and not a physical state. Apo-active
> rates and per-cell bimodality patterns describe the model's behaviour
> under this condition; direct mapping to physical basal activity is
> deferred to a separate correlation analysis (currently a manuscript
> open-item).
