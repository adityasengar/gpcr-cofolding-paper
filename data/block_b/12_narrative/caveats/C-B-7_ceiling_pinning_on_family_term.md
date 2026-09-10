# C-B-7 — Ceiling-pinning on the family term: use logit or continuous, not bare probability

## Caveat

Between 60% (of3) and 85% (protenix) of receptors are ceiling-pinned at
cognate (cognate two-instrument rate ≥ 0.98). Correspondingly 62–90%
are floor-pinned at apo (apo rate ≤ 0.02):

| backbone | ceiling_pinned (cognate ≥ 0.98) / 40 | floor_pinned (apo ≤ 0.02) / 40 |
|---|---:|---:|
| boltz | **29** | 31 |
| chai | **28** | 27 |
| of3 | **24** | 25 |
| protenix | **34** | 36 |

Under this compression, the panel-level probability-scale family term
(shuffled → cognate Δp) is a **bimodal average**: three-quarters of the
cells produce zero family shift and one-quarter produce a large one.
Top 5 receptors by boltz family term:

| receptor | shuffled | cognate | Δp |
|---|---:|---:|---:|
| NPY2R | 0.30 | 0.98 | 0.68 |
| NPY1R | 0.66 | 0.94 | 0.28 |
| OX2R | 0.79 | 0.99 | 0.20 |
| DRD3 | 0.78 | 0.98 | 0.20 |
| ACM4 | 0.79 | 0.98 | 0.19 |

All 5 have shuffled < 0.85, i.e. the ceiling has room. The receptors
where the family term is 0 (or negative) all have cognate = 1.0 already
at shuffled.

## Why it matters

The panel-level 11% probability-scale family term (SC-B-2) is the average
of a bimodal distribution. All four backbones agree the logit-scale
family share is 17–21% — because logit expands the ceiling zone back
open. Manuscript sentence "everywhere else the term is ≈ 0" (Block C
plan §1.1) is arithmetically accurate but the mechanism is **ceiling
saturation**, not intrinsic model insensitivity.

## Affects

- SC-B-2 (ladder decomposition on both scales).
- The scale-choice decision at Flag B-1.

## Manuscript sentence

> Between 60% and 85% of receptors × backbones are ceiling-pinned at
> cognate (cognate rate ≥ 0.98) on Block B's two-instrument predicate.
> The probability-scale correct-family term (median 11%) is the average
> of a bimodal distribution — most cells produce ≈ 0 because the ceiling
> is already reached at shuffled — and the term "everywhere else the
> family shift is ≈ 0" is a ceiling-saturation statement, not a
> statement about intrinsic model insensitivity. The logit-scale family
> share (17–21% across all four backbones) is not compressed and is the
> interpretable statistic.

## Related

- MANUSCRIPT_FLAGS.md Flag B-1, Flag B-9.
- Phase 3 §3e (family share on both scales), §3f (per-receptor + saturation flags).
- Source CSV: `ladder_per_receptor.csv` — 160 rows, ceiling/floor flags per (receptor, backbone).
