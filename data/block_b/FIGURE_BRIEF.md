# FIGURE_BRIEF — panel → source-file map

Six figure specs live under `12_narrative/figures/BB-*.md`. This brief maps each
figure and its panels to the CSVs the figure agent will read out of this zip.
Every load-bearing number stated in the panel specs is echoed in the
corresponding directory's `claim_answers.csv` for verification.

Frame convention: **every panel that pools across receptors uses frame_36**
(n=36 = 40 − E-B-1) unless explicitly named otherwise. See C-B-5.

---

## BB-1 — Panel A: The ladder (four-arm × four-backbone binary predicate)

**Load-bearing for**: SC-B-1 (ladder monotone + reproduces exactly).

Source CSVs:

- `04_ladder/ladder_four_scorings.csv` — primary; filter `frame == "reproduction_36"`.
- `04_ladder/ladder_continuous_distributions.csv` — for the continuous-axis
  companion table.
- `05_decomposition/ladder_decomposition_bootstrap_draws.csv` — cluster-boot
  draws for CI shading.

Claim reference: `04_ladder/claim_answers.csv`.

---

## BB-2 — Panel A: Ladder decomposition on both scales

**Load-bearing for**: SC-B-2 (occupancy 55 % / α5-CT 34 % / correct family 11–17 %).

Source CSVs:

- `05_decomposition/ladder_decomposition.csv` — primary; both probability and
  logit scales in one file.
- `05_decomposition/ladder_decomposition_bootstrap_draws.csv` — 30,000 draws;
  1,000 per (backbone × contrast × scale).

Claim reference: `05_decomposition/claim_answers.csv`. See Flag B-1 for the
both-scales rule (never quote 11 % alone).

---

## BB-3 — Panel A: 2 × 2 engagement × activation

**Load-bearing for**: SC-B-3 (2×2 reproduces published triples).

Source CSVs:

- `06_interface/interface_2x2.csv` — primary; filter `predicate ==
  "two_instrument" AND cutoff_A == 20.0 AND frame == "frame_36" AND backbone ==
  "panel_all"` for the headline row.
- Sensitivity: read the same file at `cutoff_A ∈ {10, 14, 20}` to show the
  cutoff sweep (C-B-6).

Claim reference: `06_interface/claim_answers.csv` (SC-B-3 rows).

---

## BB-4 — Panel A: PIF connector on engaged-but-inactive decoy

**Load-bearing for**: SC-B-4 (PIF geometry sits at apo on decoy engaged-but-inactive).

Source CSVs:

- `06_interface/interface_pif_connector.csv` — primary; group by
  `arm × cell_engaged_but_inactive × cell_active`.
- `06_interface/interface_continuous.csv` — for per-cell tip-depth /
  contact-count context.

Claim reference: `06_interface/claim_answers.csv` (SC-B-4 rows).

---

## BB-5 — Panel A: Donor-class residuals (Outcome A signed)

**Load-bearing for**: SC-B-6 (Gs → Gi residual ≈ 0 on tilt / NPxxY / delta_to_active).

Source CSVs:

- `07_donor_residuals/donor_class_residuals_summary.csv` — filter
  `donor_ga_class == "Gs" AND cognate_ga_class == "Gi"` for the headline row.
- `07_donor_residuals/phase5_power_analysis.csv` — native-only re-run per cell.
- `07_donor_residuals/donor_class_residuals_bootstrap_draws.csv` — 180,000
  draws for CI shading.

Claim reference: `07_donor_residuals/claim_answers.csv`. See C-B-10 for the
"caveat does not localise" reading.

---

## BB-6 — Panel A: Per-receptor ladder heatmap

**Load-bearing for**: SC-B-1 supporting evidence (per-receptor distribution),
SC-B-11 covariate signal (or lack thereof).

Source CSVs:

- `04_ladder/ladder_per_receptor.csv` — primary; 160 rows (40 receptors × 4
  backbones), carries `ceiling_pinned` / `floor_pinned` flags for annotation.
- `08_covariates/ladder_height_covariates.csv` — per-receptor `family_term`
  values on both scales.
- `08_covariates/ladder_height_regressions.csv` — for a small stat inset.

Claim reference: `08_covariates/claim_answers.csv`.

---

## Global rules for BB-1 .. BB-6

1. **Export data, not figures.** No PNG / PDF / SVG in this zip. Colour,
   layout, and stylistic choices belong to the figure agent.
2. **Report both scales for the family term** (Flag B-1). Never quote 11 %
   without the 17.4 % logit companion.
3. **State the frame in every table** (C-B-5). Every panel above uses frame_36.
4. **Report Chai separately or note per-backbone caveat** (C-B-2). Chai is
   systematically different on three axes.
5. **Cluster-boot CIs are the reported measurement** (C-B-13). Receptor-boot
   CIs are tighter and reported only for comparison.
