# 05_decomposition/ — telescoping ladder decomposition on both scales

## Files

- `ladder_decomposition.csv` — 60 rows: (frame × backbone × contrast × scale).
  Contrasts: `delta_occupancy_apo_to_decoy`,
  `delta_a5ct_sequence_decoy_to_shuffled`,
  `delta_correct_family_shuffled_to_cognate`. Scales: `probability`, `logit`.
- `ladder_decomposition_bootstrap_draws.csv` — 30,000 rows: per-draw estimates
  under the 26-cluster paralog bootstrap, seed `20260909`.

## SC-B claims supported

- **SC-B-2** (occupancy 55 % / α5-CT 34 % / correct family 11–17 %,
  scale-dependent).

See `claim_answers.csv`.

## The "both scales" rule (Flag B-1)

The correct-family share is **11.1 % on the probability scale** and **17.4 %
on the logit scale** (share ratio 1.57×). Report BOTH scales; the 11.1 %
figure is partly a ceiling artefact of the probability scale
(24–34 of 40 receptors × backbones ceiling-pinned at cognate; C-B-7). When
contrasting occupancy vs α5-CT-sequence vs family, use the logit share.

## Protenix probability-CI note

Protenix's probability-scale family term CI [-0.021, +0.061] crosses zero — a
ceiling artefact. Logit CI [0.35, 1.05] is squarely positive. Report the logit
CI when Protenix appears in a per-backbone panel.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
