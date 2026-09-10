# W-B-1 — "Family term is ~11% of the ladder" as a single scale-neutral number

## Claim as previously stated

Prior campaign narrative summarised the apo → cognate ladder decomposition
as: occupancy 55%, α5-CT sequence 34%, **correct family ~11%** — reported
as a single figure representing the family-identity contribution to the
ladder rise.

## Retraction

**Withdrawn as a bare scale-neutral figure.** The family-term share
depends on the reporting scale. On the probability scale it is 11.1%
[0.047, 0.125]; on the logit scale it is **17.4% [0.39, 1.09]** — share
ratio 1.57×.

All four backbones agree the logit-scale family share is 17–21%. The
probability-scale figure is a **ceiling artefact** — 24 to 34 of 40
receptors × backbones are ceiling-pinned at cognate (cognate rate ≥
0.98), and the shuffled → cognate arms sit at 0.81 → 0.89, deep in the
compression zone where identical amounts of "identity-driven activation"
produce smaller Δp than the same amount would produce at mid-scale.

## What supersedes it

Report both scales. Recommended primary statistic is the logit share
(17–21% across all four backbones); the probability share is reported
alongside as the intuitive-communication scale with the ceiling caveat
attached. See:

- SC-B-2 (both scales in the claim sheet).
- C-B-7 (ceiling-pinning caveat).
- MANUSCRIPT_FLAGS.md Flag B-1, Flag B-9.

## What the manuscript should say instead

> The apo → cognate ladder decomposes into three telescoping terms
> whose share depends on the reporting scale. On the probability scale:
> occupancy 54.6%, α5-CT sequence 34.3%, correct family 11.1%. On the
> logit scale — which does not suffer the probability-scale ceiling
> compression that pins 60–85% of receptors × backbones at cognate rate
> ≥ 0.98 — the shares are 50.5% / 32.1% / 17.4%. All four backbones
> agree the logit-scale family share is 17–21%; the probability-scale
> family term ranges from 2.4% (Protenix, saturation-driven) to 14.8%
> (OpenFold-3), and Protenix's probability CI crosses zero as an
> artefact of ceiling saturation.

## Evidence

- `docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md §3e` (decomposition on both scales).
- Source CSV: `ladder_decomposition.csv` (60 rows: 5 backbones × 2 frames
  × 2 scales × 3 contrasts) + `ladder_decomposition_bootstrap_draws.csv`
  (30,000 draws).
- `docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md §3f` (per-receptor saturation flags).
