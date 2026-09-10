# W-D-4 — Dichotomous "correct backbones vs failing backbones" framing on D2

## Claim as previously stated

Companion to W-D-3. The D2 smoke's per-backbone dichotomy ("Boltz +
OF3 respond correctly; Chai + Protenix fail") suggested that D2's
inactive-Nb steering is a per-backbone success/failure binary that
some backbones pass and others don't.

## Retraction

**Withdrawn.** Panel-scale D2 shows the failure is not backbone-binary
— it is per-(receptor × backbone) with systematic direction:

- Boltz: correct on ADRB2, inverts on OPRK. Not a backbone-binary
  success/failure.
- Chai: refuses to shift on either receptor. Reads apo-locked, not
  Nb-directed.
- OF3: stable at ~10 % on both. Neither correct nor inverting; a
  weakest-signal-across-4-bb behaviour.
- Protenix: mirror of Boltz — inverts on ADRB2, correct on OPRK.

Replaced with F3's per-receptor breakdown plus OPRK's unanimous_up
direction (all 4 backbones shift active) as the systematic
Nb-B-as-active signature.

## Basis

- `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` — per-cell active fractions.
- `dossiers/BLOCK_D/partA/PARTA_D2.md` §1 F3 (per-receptor breakdown).
- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §SC-D-6.

## What the manuscript should say instead

Report per-receptor per-backbone. Do not report "which backbones
succeed at inactive-Nb steering" as a dichotomy — the failure has
receptor structure that averaging into a backbone-only readout would
hide. See W-D-3 for the recommended panel-scale sentence.
