# W-D-3 — "Boltz + OF3 respond correctly to Nb-inactive; Chai + Protenix fail" (D2 smoke story)

## Claim as previously stated

The D2 smoke (ADRB2 alone, 1 seed) suggested a clean dichotomy:
Boltz + OF3 respond correctly to Nb-inactive (drive receptor to
inactive-like); Chai + Protenix fail.

## Retraction

**Withdrawn.** Panel-scale D2 at n=50 per (receptor × arm × backbone)
across ADRB2 and OPRK inactive_nb cells shows **no backbone is a
reliable inactive-directing partner**. Per-backbone breakdown:

| Test | ADRB2 | OPRK |
|---|---|---|
| Boltz apo→inactive_nb Δ%active | 0 → 0 ✓ | 4 → 48 ✗ (goes ACTIVE) |
| Chai apo→inactive_nb Δ%active | 100 → 100 ✗ (refuses) | 74 → 82 ✗ (refuses) |
| OF3 apo→inactive_nb Δ%active | 10 → 10 ✓ | 0 → 10 ≈ |
| Protenix apo→inactive_nb Δ%active | 0 → 76 ✗ (goes ACTIVE) | 0 → 6 ✓ |

Boltz corrects on ADRB2 but INVERTS on OPRK. Protenix is the mirror
image — correct on OPRK, INVERTS on ADRB2. Chai stays where it started
on both. OF3 is stable at ~10 % on both, without a discriminative
active-vs-inactive readout.

## Basis

- `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` — 2,370 preds.
- `dossiers/BLOCK_D/partA/PARTA_D2.md` §1 F3.
- `dossiers/BLOCK_D/gates/GATE_1_D2_NB_SHA.md` (all 4 arms consumed correct real sequences — F3 is not a data-contamination artifact).

## What the manuscript should say instead

Per SC-D-6 with C-D-12 confound acknowledged:

> No backbone is a reliable inactive-directing partner on the D2 panel
> (n=2 receptors × 4 backbones). The failure has a systematic direction:
> on OPRK all four backbones shift up toward active under inactive-Nb
> (Boltz +44, Chai +8, OF3 +10, Protenix +6 pts). All four Nb-anchor
> references predate every backbone's training cutoff (C-D-12) — the
> negative finding cannot yet be distinguished from a
> training-data-availability effect.
