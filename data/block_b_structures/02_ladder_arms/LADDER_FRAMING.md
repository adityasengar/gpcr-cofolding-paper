# Ladder framing — the ladder is a *rate*, not a per-structure property

## The claim these four CIFs illustrate

The four-arm ladder (SC-B-1) is a **panel-level active-call fraction**.
Across 40 Class A receptors × 4 backbones × 5 seeds × 10 samples per arm
(2,000 rows / arm / backbone; 8,000 rows / arm panel-wide), the
two-instrument active-call fraction rises monotonically:

| arm       | panel fraction (frame_36) | 95% CI (cluster-boot) |
|-----------|--------------------------:|-----------------------|
| apo       | 0.158                     | [0.081, 0.256]        |
| decoy     | 0.558                     | [0.445, 0.664]        |
| shuffled  | 0.809                     | [0.747, 0.869]        |
| cognate   | 0.891                     | [0.838, 0.942]        |

## What the four shipped CIFs are (and are not)

Each CIF is the row in the (GHSR, arm, boltz) cell whose
`delta_to_active` is CLOSEST to that cell's median value (50 rows per
cell). They are **arm representatives, not exemplars of the ladder
outcome**. Do not:

- infer arm activity from any single CIF (an apo representative may
  happen to sit near median-active or near median-inactive for GHSR
  boltz; a decoy representative may be active or inactive);
- read the median-position CIF as "the model's answer" for that arm
  (the answer is the fraction across 50 samples × 40 receptors, not
  any one structure);
- generalise from GHSR to the panel — GHSR is one receptor's typicality
  slice, chosen per §4.1 rules in `SELECTION_RULES.md`. GHSR's decoy
  arm active-call fraction on boltz is 0.22 vs the panel 0.558; the
  representative structure will reflect that receptor-specific
  behaviour.

## The 4 CIFs

| arm       | file                      | GHSR × boltz per-cell active fraction |
|-----------|---------------------------|--------------------------------------:|
| apo       | apo/aa4e77c50f34.cif      | 0.00                                  |
| decoy     | decoy/86d2a2e19f92.cif    | 0.22                                  |
| shuffled  | shuffled/3ad9efb4824a.cif | 1.00                                  |
| cognate   | cognate/0e2dfb5b8206.cif  | 1.00                                  |

## Why GHSR

GHSR is the receptor that survives §4.1 hard exclusions (E-B-1..E-B-3),
bottom-quartile filters on reference separation, and the explicit
typicality-exclusion lists (occupancy / sequence-required /
family-specific-heavy), and has n ≥ 10 decoy engaged-but-inactive rows on
all four backbones — the only receptor that meets those constraints.
It is the only viable Bundle-C anchor, not a "clearest cognate" cherry-pick.
See STRUCTURE_BUNDLE_MANIFEST §2 for the full survivor table.

## Notes for the figure agent

- The apo representative on GHSR × boltz has median `delta_to_active`
  = −6.045 Å — well on the inactive side of the two-instrument
  predicate. The active-call fraction on the arm is 0.00 (0 / 50 active),
  so this CIF is faithful to the arm's central tendency.
- The cognate representative on GHSR × boltz has median delta = −0.229
  Å, tightly grouped near the active side; active-call fraction is 1.00
  (50 / 50 active).
- Every CIF is model output as delivered on 2026-09-03 rescore — no
  side-chain fix, no chain rename, no atom-renumbering.
