# C-B-5 — Frame-36 vs frame-40 denominator convention

## Caveat

Two receptor denominators appear side-by-side in the Block B docs:

- **frame_36** — n=36 receptors excluding EDNRA / EDNRB / GRPR / HRH3
  (all have 7.53 = L not Y — no OH atom to measure NPxxY-OH). Used by
  every published two-instrument predicate number and by the
  `BLOCK_C_LIGAND_BLOCK_PLAN_2026_09_03.md §1` cite of Block B binary
  ladder.
- **frame_40** — n=40, the naïve Class A denominator. Used by
  `analysis/headline_results.md`'s tilt-only single-instrument table
  (tilt doesn't NaN on the four excluded receptors).

The two conventions disagree by 1–9% per arm on the two-instrument
predicate:

| Arm | frame_36 binary | frame_40 binary | Δ |
|---|---:|---:|---:|
| apo | 0.158 | 0.142 | −0.016 |
| decoy | 0.558 | 0.502 | −0.056 |
| shuffled | 0.809 | 0.729 | −0.080 |
| cognate | 0.891 | 0.802 | −0.089 |

## Why it matters

Neither convention is wrong. Both are internally consistent. But a reader
who quotes the tilt-only headline table (frame_40) and the two-instrument
plan cite (frame_36) side-by-side without signposting sees the same
"cognate rate" cited as either 0.80 or 0.89, and cannot reconstruct why.

**Every headline table in the manuscript must call which convention it
uses.**

## Affects

- SC-B-1 (ladder), SC-B-3 (2×2 engagement × activation), and any
  panel-level active-call fraction.

## Manuscript sentence

> Panel-level two-instrument active-call fractions are computed on the
> 36-receptor Class A stratum (frame_36 = 40 receptors excluding EDNRA,
> EDNRB, GRPR, HRH3 whose 7.53 = L not Y, so NPxxY-OH is undefined and
> the two-instrument predicate collapses to false). Tilt-only
> single-instrument fractions use the full n=40 (frame_40) because tilt
> is defined on all 40. Every headline table names which frame it uses.

## Related

- MANUSCRIPT_FLAGS.md Flag B-7.
- Phase 3 §3d, Phase 4b, Phase 6 midpoint reconciliation.
- `docs/BLOCK_B_CLAIM_AUDIT.md §C3` (documents the denominator finding).
