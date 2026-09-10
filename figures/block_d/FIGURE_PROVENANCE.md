# Block D — figure provenance

One entry per panel: what it draws, where each number came from, and **whether
it was recomputed or transcribed**. That last column matters more in this block
than in any before it.

**Block D shipped no row-level data.** The three corpora its claim sheet names —
14,000 + 2,370 + 25,810 = 42,180 predictions — are not in the bundle. Five CSVs
ship and all five are panel or reference metadata. So the honest default for a
Block D number is *transcribed from a markdown document*, and the exceptions are
worth naming individually.

## What was recomputed, and by what

| quantity | how | where |
|---|---|---|
| panel sizes 7 / 4 / 26 | counted from the three tier CSVs | `verify_claims.py` D01–D03 |
| 22 paralog clusters over D3's 26 receptors | intersected the D3 panel with the shipped paralogy map | D07 |
| D1 and D2 cluster-boot degeneracy | 7 receptors in 7 clusters, 4 in 4 | D08 |
| every exact binomial interval drawn in BD-2 | Clopper–Pearson from k and n at n=50 | D15–D20 |
| the ln-vs-log₁₀ factor on the D3 slopes | −3.877 / −1.684 = 2.302 = ln 10 | D21 |
| **fifteen NPxxY hydroxyl distances** | measured from the deposited coordinates | `cifmeasure.py`, D22–D27 |
| every nanobody anchor's cutoff comparison | deposition date against the three dated cutoffs | D13 |

Everything else on every panel is transcribed, and each panel says so on its
face.

## Per panel

### BD-1 — `bd1_apo_landscape.py`
- **a, b** — `data/block_d/07_partA/PARTA_D1.md` §1, tables 1 and 2. 28 cells
  each, 7 receptors × 4 backbones, apo arm, 500 samples/cell. **Transcribed.**
- **green rings** — the five cells whose shipped structure we measured.
  ADRB2/Chai 4.22 Å, ADRB2/Boltz 11.31 Å, GHSR/Boltz 10.09 Å, CNR2/Chai 2.61 Å,
  LPAR1/OF3 4.91 Å. **Recomputed** from coordinates.
- **c** — `01_claims/BLOCK_D_CLAIM_SHEET.md` SC-D-1 for the D1 deltas and
  `04_flags/` Flag D-5 for the Block A reproduction. **Transcribed.**
- CI convention: receptor-boot, and the reason (7 receptors, 7 clusters) is in
  the caption.

### BD-2 — `bd2_direction_asymmetry.py`
- **a** — `PARTA_D2.md` F2, the ACM2 apo → active-Nb deltas. **Transcribed.**
- **shaded band** — SC-D-4, 14 of 16 cells ≥96%. **Transcribed**; the count is
  cross-checked against Flag D-9, which exists because an earlier draft said 15.
- **b** — `PARTA_D2.md` F3, both receptors × four backbones. Rates
  **transcribed**; **every interval recomputed** and matching to the stated
  decimal.
- **caption** — C-D-12, with the four anchor deposition dates verified against
  the shipped `nanobody_state_anchors.csv`.

### BD-3 — `bd3_depth_ladder.py`
- **a–d** — `PARTA_D3.md` §1, the five-depth ladder per backbone.
  **Transcribed.**
- **slopes and intervals** — SC-D-8, cross-checked against `GATE_2_D3_SLOPES.md`
  §5, which refit them independently and reproduced them exactly under
  `ln(depth)` with full = 4096. The **point estimates are corroborated**; the
  intervals rest on bootstrap draws that were not shipped and are therefore
  transcribed.
- **e** — `GATE_3_STEERING_VS_DEGRADATION.md` §1, matched-seed Cα ranges.
  **Transcribed.**
- **f** — SC-D-8(b) for the sub-Å deltas, GATE-3 §1 for the pLDDT deltas.
  **Transcribed.** Chai's sub-Å delta is not reported in the source and is drawn
  as `n/r` rather than as zero.

### BD-4 — `bd4_nb_structures.py`
- **every value on this panel was measured**, by `analysis/block_d/cifmeasure.py`,
  between the hydroxyl oxygens of Tyr5.58 and Tyr7.53.
- Tyr7.53 was located independently in each file from its own NPxxY motif and
  **agreed with the GPCRdb-mapped position on all fifteen structures**, which is
  what licenses taking Tyr5.58 from the same table. Both anchors are
  identity-checked; the script refuses rather than guesses.
- **Selection rule**, stated on the panel: the pipeline's hand-picked D2
  illustrations, one sample per cell, not a draw. No rate may be read from them.

### BD-5 — `bd5_lever_vs_degradation.py`
- **a, b lines** — `GATE_3` §, the two flagship cells. These are **cell medians
  over 50 samples** — the source's columns are headed `med pca_active`,
  `med NPxxY`, `med tilt` — and are **transcribed**.
- **b diamonds** — the single shipped structure for each cell, **measured**.
  Drawn apart from the medians deliberately: comparing one to the other produced
  a phantom discrepancy in our own first checker (`DISCREPANCY_REPORT` D-D-4).

## The structures, in full

`analysis/block_d/tables/D-T1_structures_measured.csv` carries all 18 manifest
entries with the measured distance, both anchor positions, whether the motif
agreed, and the resulting state call. **Fifteen landed; three failed to pull**
(SSH throttle, error text preserved in the manifest) and are recorded as failed
rather than dropped, so the random set is 4 of an intended 7 and any use of it
must say so.
