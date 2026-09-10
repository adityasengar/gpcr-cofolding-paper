# Block B — per-panel provenance

The companion to the ledger entries in `figures/FIGURES.md`. This carries what a
caption needs: source file, exact filter, n after filtering, and the claim.

**Frame.** Every panel here is frame_36 unless it says otherwise: 36 receptors,
after removing EDNRA, EDNRB, GRPR and HRH3, whose NPxxY axis is undefined
because position 7.53 is Leu rather than Tyr. That is biology, not missing data,
and the four are named on every panel that drops them.

**Resampling unit.** Cluster bootstrap over paralog clusters, 1,000 resamples,
seed 20260909. frame_36 contains **24** clusters, not the 26 every shipped
interval is labelled with — excluding the four receptors above removes the
endothelin and bombesin clusters entirely (D-B-8). Panels that compute their own
intervals use 24 and say so.

| panel | source | filter | n | claim |
|---|---|---|---|---|
| BB-1 | `01_rows/rows_tidy.csv`, checked against `04_ladder/ladder_four_scorings.csv` | frame_36, predicate recomputed per row | 36 receptors × 4 backbones × 4 arms | SC-B-1 |
| BB-2 | `05_decomposition/ladder_decomposition.csv` | `frame == reproduction_36` | panel + 4 backbone rows × 2 scales × 3 contrasts | SC-B-2 |
| BB-3 | `06_interface/interface_2x2.csv` | frame_36, `predicate == two_instrument`, all 6 cutoffs | 3 partner arms × 5 strata × 6 cutoffs | SC-B-3 |
| BB-4 | `06_interface/interface_pif_connector.csv` | by cell flags, no exclusion set applied | 160 / 130 / 118 / 69 / 47 cells | SC-B-4 |
| BB-5 | `07_donor_residuals/phase5_power_analysis.csv` | `backbone == panel`, `axis == residual_tilt` | 24 / 8 / 5 receptors, native 20 / 3 / 0 | SC-B-6, SC-B-14 |
| BB-6 | `04_ladder/ladder_per_receptor.csv` | frame_36 by membership | 144 cells, 36 receptors | SC-B-1 |

## What is deliberately not drawn

- **The superseded ladder** 0.158 / 0.552 / 0.810 / 0.892, which the BB-1 spec
  asks for as reference dashes. 0.552 is a pre-consolidation snapshot the drop's
  own README retires, and the spec contradicts itself two paragraphs later.
- **A structural render of the PIF connector.** The whole spread is 0.7 Å.
- **Anything from `02_ladder_arms/`** as a panel-ladder illustration. Those four
  structures are GHSR, whose decoy arm fires at 0.175 against the panel's 0.558.
- **Any Chai-1 structure as a primary panel.** Chai does not read the decoy
  α5-CT edit as aligned MSA columns, so its shallower C2 depth reflects that,
  not better seating (C-B-2).

## The threshold every panel had to decide about

Rows carry `threshold_npxxy_oh_active_lt = 9.08`; the claim sheet, README and
shipped aggregates use 9.082. Five rows of 32,000 fall between, and one of them
moves AA2AR/Chai-1/decoy from 0.90 to 0.88. Panels recompute with the value the
rows carry and `badata.predicate()` requires the choice to be explicit. BB-1's
guard is what found this (D-B-3).
