# W-D-8 — D1 "two continuous basins" secondary claim (PREREG §D-1.4)

## Claim as previously stated

PREREG §D-1.4 secondary deliverable: Hartigan's dip test + Gaussian-mixture
k-mode fit on continuous axes (d_tm6_r350_r630_ca,
d_npxxy_y558_y753_oh, d_gpcrdb_tm6_tilt_246_637_ca, RMSD-to-active).

The originally-motivating expectation was that per-cell distributions
would show two peaks on continuous axes — a physical two-basin
signature the panel-scale D1 resample could confirm at n=500.

## Retraction

**Withdrawn from main text.** Panel-scale dip test outcome (Part A/D1 §3):
**2 of 112 cells signed** (dip_p < 0.05 AND BIC-selected GMM k=2).
Both signed cells are OPSD × OF3 (on d_tm6 and pocket_ca_rmsd_active).

PREREG §D-1.7 kill fires:

> "Dip test uninformative at n=500 on continuous axes → drop the
> two-mode claim from the manuscript, keep the CI-hardened hit-rate +
> apo-active-fraction distributions as the primary deliverable. Tier
> still ships value; the null result is a publishable qualifier, not
> a tier failure."

The kill fires cleanly at 2/112. §D-1.7's own contingency clause
retains D1's value via the primary CI-hardened distributions.

## Basis

- `dossiers/BLOCK_D/partA/PARTA_D1.md` §3 (dip test / GMM outcomes).
- PREREG §D-1.4 + §D-1.7 (`docs/BLOCK_D_PREREG_AMENDMENT_2026_09_06.md`).
- `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` — the input rows.

## What the manuscript should say instead

Drop the "two continuous basins" claim from main text. Keep OPSD × OF3
as a single-cell Discussion-appendix note (the one signed cell in 112
tested). D1's main-text value is the CI-hardened per-cell distributions
on the two-instrument axis and the sub-Å-to-active axis (SC-D-1
through SC-D-3), plus the cross-tier F1 reproducibility (SC-D-11).
