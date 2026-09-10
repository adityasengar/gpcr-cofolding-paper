# BB-3 — Panel C: 2×2 engagement × activation per backbone at 14 Å and 20 Å

## Purpose

Show the 2×2 grid of (arm × engagement state × activation state) per
backbone at two engagement cutoffs (14 Å and 20 Å). Load-bearing for
the mechanism claim: the decoy engaged-but-inactive cell has n well
above the ≥5 CONDITIONAL threshold on every backbone, and the cutoff
choice moves the decoy-arm active fraction more than the cognate-arm
one (see C-B-6, Flag B-8).

Load-bearing for **SC-B-3**.

## Data source

Primary CSV: `experiments/019_block_b_partner_selection/analysis/interface_2x2.csv`.

- Rows: 480 (2 frames × 2 predicates × 6 cutoffs × 4 arms × 5
  backbone-strata).
- Columns used: `frame`, `predicate`, `cutoff_angstrom`, `arm`,
  `backbone`, `p_engaged`, `p_engaged_ci_lo`, `p_engaged_ci_hi`,
  `p_active_given_engaged`, `p_active_given_engaged_ci_lo`,
  `p_active_given_engaged_ci_hi`, `n_engaged_but_inactive`, `n_active_engaged`.

Filter to `frame == "reproduction_36" AND predicate == "two_instrument"
AND cutoff_angstrom IN (14, 20)`.

## Panels

**Panel C.i — 2×2 heat/grid at 20 Å**

- Rows: arm ∈ {apo, decoy, shuffled, cognate}, top-to-bottom.
- Columns: 4 backbones (small multiples).
- Each cell: 2×2 sub-grid annotated with (n_active_engaged, p(engaged)
  × p(active|engaged)) — engagement on x, activation state on y.
- Value labels: n_engaged_but_inactive in the top-left of the decoy
  arm's cell — the mechanism-claim floor (278–540 per backbone; ≥ 5).

**Panel C.ii — cutoff sweep, panel row**

- x-axis: cutoff ∈ {10, 12, 14, 16, 18, 20} Å.
- y-axis: p(active | engaged), 0 → 1.
- Series: arm ∈ {apo (n/a), decoy, shuffled, cognate}.
- Cognate line nearly flat (~0.89 across all cutoffs).
- Decoy line rising 0.53 → 0.66 across 10 → 20 Å.
- Vertical dashes at 14 Å and 20 Å.

## Annotations

- Reproduction check: cognate 0.9983 / 0.8926, shuffled 0.9674 / 0.8353,
  decoy 0.7037 / 0.6647 at 20 Å frame_36 (matches published triples
  within ±0.012).
- Engaged-but-inactive n for decoy arm per backbone: boltz 464, chai
  417, of3 540, protenix 278 (pooled 1,699 in frame_36; 2,234 in
  frame_40).
- Callout: "20 Å cutoff = 4× median cognate depth (12.19 Å); 14 Å is
  reported alongside" (C-B-6).

## Exclusion flags to render as annotations

- E-B-1 (frame_36) applied.
- Class A only (C-B-15).

## Qualified by

C-B-5 (frame), C-B-6 (cutoff sensitivity), C-B-15 (Class A only),
Flag B-7, Flag B-8, Flag B-13 (non-inserted decoy contact-count
restatement).
