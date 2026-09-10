# C-B-14 — Ladder-height covariates: no panel slope excludes zero at 95% CI

## Caveat

Regressed per-receptor family term (two scales) against three testable
predictors on the 40 Class A receptors. A fourth candidate
(`deposition_count`) was originally listed but is degenerate at
Block B's reference-set proxy — every receptor has exactly 2 references
(1 active + 1 inactive) in `reference_set.blockb_pinned.csv`, so the
proxy has std = 0 and produces no OLS slope. Deposition count remains a
plausible predictor if it can be pulled from an RCSB-wide entry count
rather than the reference set; that pull is out of Block B scope and
recorded as a future item, not tested here.

Three testable predictors on the 40 Class A receptors:

1. **Δ_ref NPxxY-OH** = active_ref_NPxxY − inactive_ref_NPxxY.
2. **Δ_ref TM6-tilt** = active_ref_tilt − inactive_ref_tilt.
3. **Coupling promiscuity** = count of Gα families
   (primary + secondary) from `refs/gpcr_coupling.csv`.

Degenerate predictor (not tested):

4. **Deposition count** — reference-set proxy has std = 0; NaN slope.

Panel-level cluster-boot slopes over 26 paralog clusters:

| predictor | scale | slope (all 40) | 95% CI | slope (no AA2AR) | 95% CI (no AA2AR) |
|---|---|---:|---|---:|---|
| Δ_ref NPxxY | continuous | -0.002 | [-0.037, +0.032] | -0.009 | [-0.045, +0.025] |
| Δ_ref NPxxY | logit | -0.037 | [-0.128, +0.080] | -0.037 | [-0.127, +0.086] |
| Δ_ref tilt | continuous | +0.049 | [-0.122, +0.270] | -0.003 | [-0.149, +0.143] |
| Δ_ref tilt | logit | +0.134 | [-0.222, +0.486] | +0.137 | [-0.220, +0.492] |
| coupling promiscuity | continuous | -0.106 | [-0.563, +0.342] | -0.017 | [-0.464, +0.430] |
| coupling promiscuity | logit | -0.072 | [-0.841, +0.663] | -0.074 | [-0.877, +0.665] |

**No panel slope excludes zero at 95% CI on any of the three usable
predictors on either scale.** Coupling promiscuity signs weakly in the
learned-coupling direction (negative slope: promiscuous receptors show
smaller family term) but magnitude is dwarfed by CI.

## Why it matters

Under the CI-gated reading, ladder height does not scale with reference
gap or coupling promiscuity at the resolution 40 receptors support. The
family term is receptor-heterogeneous (see SC-B-2, C-B-7) but not
predictable from any of the three tested predictors. The under-power is
consistent with only 15 multi-member paralog clusters carrying the
resampling weight; 11 of 26 clusters are singletons.

## Affects

- SC-B-11 (no covariate slope excludes zero).
- The manuscript's interpretation of the family term as "structural" vs
  "learned" — currently untestable at this panel size.

## Manuscript sentence

> On the 40-receptor Block B panel, no ladder-height covariate (per-receptor
> Δ_ref NPxxY-OH, Δ_ref TM6-tilt, coupling promiscuity) has a panel
> slope excluding zero at cluster-boot 95% CI on either the continuous
> or the logit scale. Coupling promiscuity signs weakly in the
> learned-coupling direction (negative slope) but magnitude is dwarfed
> by CI. AA2AR alone accounts for the panel-level Δ_ref tilt
> continuous-scale slope (+0.049 → −0.003 when AA2AR excluded); other
> predictors are stable to AA2AR removal.

## Related

- MANUSCRIPT_FLAGS.md Flag B-11 (AA2AR sensitivity).
- Phase 6a §Panel regressions.
- Source CSVs: `ladder_height_covariates.csv` (40 rows),
  `ladder_height_regressions.csv` (80 rows).
