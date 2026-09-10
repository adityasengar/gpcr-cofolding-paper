# BB-5 — Panel E: Donor-class residuals (scatter or forest) — all refs and native-only

## Purpose

Show that the model does not encode donor-family-specific cavity
geometry at a magnitude resolvable from cluster-bootstrap noise on the
manuscript-load-bearing Gs → Gi shuffled cell (24 receptors). Report
both the all-refs Phase 5 result (+0.024 Å) and the native-only Phase
6b re-run (−0.062 Å) — Outcome A firms up.

Load-bearing for **SC-B-6** and Flag B-4.

## Data source

Primary CSVs:

- `donor_class_residuals_summary.csv` — 270 rows (backbone × donor ×
  cognate × axis medians + cluster-boot 95% CIs).
- `phase5_power_analysis.csv` — 45 rows (native-only re-run per
  (backbone, stratum, axis)).

Auxiliary: `donor_class_residuals_bootstrap_draws.csv` (180,000 draws)
if beeswarm is preferred.

Filter: `axis == "residual_tilt"` for the primary panel; `residual_npxxy`
and `residual_delta_to_active` as sensitivity supplementaries.

## Panels

**Panel E.i — forest plot, all shuffled strata × axes, panel-level**

- y-axis: 9 rows (3 qualifying shuffled strata × 3 axes:
  Gs → Gi, Gs → Gq, Gi → Gs × tilt, NPxxY, delta_to_active).
- x-axis: residual (Å) with 0-line prominent.
- Point + 95% CI whiskers per row.
- Annotate CI-excludes-zero cells with a mark; only 1 of 9 excludes
  zero (Gs → Gq tilt, anti-B).

**Panel E.ii — Gs → Gi tilt: all refs vs native only**

- Two rows: `all refs (n=24)` vs `native only (n=20)`.
- x-axis: residual_tilt (Å) with 0-line.
- Points: +0.024 vs −0.062.
- 95% CIs: [-0.29, +0.30] vs [-0.41, +0.21].
- Note the CI-width comparison (0.59 → 0.62) — sign flips within
  noise, CI width unchanged despite dropping 4 receptors.

**Panel E.iii — Optional per-backbone dot plot for Gs → Gi tilt
native-only**

- x-axis: backbone.
- y-axis: residual_tilt with 0-line.
- 4 dots + 95% CI each (from `donor_class_residuals_summary.csv`).

## Annotations

- Sanity anchors (in a text box or supplementary): cognate → cognate
  Gi rows anchor at −0.144 Å [CI includes zero] on tilt; apo Gi rows
  anchor at −5.28 Å [CI [-5.61, -4.76]].
- Callout: "Reference-bias caveat is real at panel level (37.5%
  non-native active refs) but does NOT localise to this cell —
  Gs → Gi shuffled cell is 83.3% native-anchored" (C-B-10).

## Exclusion flags to render as annotations

- E-B-3 (non-native active references) applied as the native-only
  filter on Panel E.ii.
- Bootstrap seed 20260909; 1000 draws; 26 paralog clusters.

## Qualified by

C-B-10 (reference-bias caveat does not localise), W-B-3 (Gs → Gq third
finding held pending native-only power), W-B-4 (Outcome B withdrawn),
Flag B-4, Flag B-27 (Gi → Gs cell cannot be resolved).
