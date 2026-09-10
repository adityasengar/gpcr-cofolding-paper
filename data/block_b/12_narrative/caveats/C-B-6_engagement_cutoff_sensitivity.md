# C-B-6 — 20 Å engagement cutoff is permissive at cognate; report 14 Å alongside

## Caveat

The 20 Å tip-to-R3.50 Cα engagement cutoff used by the 2×2 table is
4× the median cognate tip depth (12.19 Å across 160 cognate cells,
range 10.64–14.66 Å across per-backbone medians). p(active|engaged)
on cognate is nearly flat across the 10–20 Å sensitivity sweep:

| cutoff (Å) | p(engaged) | p(active\|engaged) | n(engaged-but-inactive) |
|---:|---:|---:|---:|
| 10 | 0.033 | 0.897 | 24 |
| 12 | 0.503 | 0.902 | 355 |
| 14 | 0.881 | 0.895 | 665 |
| 16 | 0.964 | 0.893 | 745 |
| 18 | 0.994 | 0.893 | 771 |
| 20 | 0.998 | 0.893 | 772 |

On the decoy arm the same sweep runs 0.05 → 0.70 in p(engaged), with
p(active|engaged) rising from 0.53 to 0.66 — a 0.13 shift. **The 20 Å
cutoff is load-bearing at decoy: it moves the decoy-arm active fraction
more than the cognate-arm one.**

## Why it matters

Any chemistry-claim table comparing cognate to decoy engagement, or
comparing engaged-but-inactive rates between arms, that quotes 20 Å
alone hides how much of the decoy-arm active fraction is cutoff-choice
driven. The engagement conclusion depends on where the cutoff sits.

## Affects

- SC-B-3 (2×2 engagement × activation).
- Downstream: any α5-CT-chemistry-claim table (e.g. Block C plan §1)
  that pools engaged rows across arms.

## Manuscript sentence

> Engagement is defined at a 20 Å tip-to-R3.50 Cα cutoff (4× median
> cognate depth of 12.19 Å). Sensitivity across the 10–20 Å range moves
> cognate p(active | engaged) by ≤ 0.01, but moves decoy p(active |
> engaged) by 0.13 (0.53 at 10 Å → 0.66 at 20 Å). Both 14 Å and 20 Å
> values are reported in the primary chemistry-claim table.

## Related

- MANUSCRIPT_FLAGS.md Flag B-8.
- Phase 4b sensitivity sweep.
