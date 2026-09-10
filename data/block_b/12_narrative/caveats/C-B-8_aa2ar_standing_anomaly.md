# C-B-8 — AA2AR is recurrently anomalous by non-saturation, NOT by missing reference

## Caveat

AA2AR is called anomalous across three separate analyses in this
campaign. On Block B specifically:

- **Family term +0.76 on Boltz** (cognate 0.80 − shuffled 0.04) —
  the single largest per-receptor family term on any (receptor,
  backbone) cell in the Block B panel.
- **Active ref**: 5G53, `active_stabilization_source = mini_G`
  (Gs mini-G), tilt 18.10 Å, NPxxY-OH 3.71 Å.
- **Inactive ref**: 5NM4, tilt 11.99 Å, NPxxY-OH 9.73 Å. **Primary
  inactive ref is PRESENT** in the `6ee2cad8` scoring-time bytes; both
  delta and RMSD to inactive computable on all rows.
- Δ_ref NPxxY = −6.02 Å (largest active-vs-inactive gap on NPxxY-OH in
  the panel, ties with several others).
- Δ_ref tilt = +6.10 Å.
- Saturation: 3/4 backbones ceiling-pinned at cognate; **NOT ceiling-pinned
  on boltz** (cognate 0.80). AA2AR is the only receptor in Block B whose
  shuffled cell (boltz) has < 0.10 AND cognate < 1.0.
- AA2AR alone accounts for the entire panel-level Δ_ref tilt continuous
  slope (Phase 6a): +0.049 → −0.003 when AA2AR excluded.

## Reconciliation across aggregations (added post-freeze, 2026-09-10)

Two AA2AR family-term numbers appear in the dossier and initially read
as a 4× swing. They are the same underlying data on different
aggregations:

| Aggregation | Value | Where cited |
|---|---:|---|
| Panel mean across 4 backbones | **+0.19** | Phase 3 §3f |
| Boltz-only per-cell | **+0.76** | Phase 6a |
| Chai / OF3 / Protenix per-cell | 0.00 | ceiling-saturated (shuffled = cognate = 1.0) |

Per-backbone AA2AR ladder from `ladder_per_receptor.csv`:

| backbone | apo | decoy | shuffled | cognate | family (prob) | family (logit) |
|---|---:|---:|---:|---:|---:|---:|
| boltz | 0.020 | 0.000 | 0.040 | 0.800 | **+0.760** | **+4.564** |
| chai | 0.000 | 0.900 | 1.000 | 1.000 | 0.000 | 0.000 |
| of3 | 0.000 | 0.560 | 1.000 | 1.000 | 0.000 | 0.000 |
| protenix | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |

Panel mean = (0.760 + 0.000 + 0.000 + 0.000) / 4 = 0.190. The panel
mean understates AA2AR's per-cell magnitude because 3 of 4 backbones
saturate at cognate=1.0 with shuffled=1.0, structurally forcing the
family term to zero on those cells. Boltz is the only backbone where
AA2AR's shuffled cell (0.04) is not ceiling-pinned, and it is where
AA2AR's family term is measurable.

**Manuscript quoting rule**: never quote AA2AR's family term without
naming the aggregation. "+0.19 panel mean across 4 backbones" and
"+0.76 Boltz-only" are both correct on their own; neither is a
per-receptor headline without a per-backbone context.

**Additional per-cell note (2026-09-10)**: on Boltz, AA2AR's decoy
cell (0.000) is BELOW apo (0.020) — a rare negative occupancy term.
Every other Block B receptor × backbone cell has apo ≤ decoy. This
receptor drives the tilt-Δ_ref covariate slope single-handedly
(Phase 6a: +0.049 → −0.003 when AA2AR excluded) and is the one cell
whose ladder is not monotonic apo ≤ decoy ≤ shuffled ≤ cognate at
Block B row-level counts. Consistent with C-B-8's non-saturation story;
no action beyond this note.

## Why it matters

**The AA2AR anomaly is not caused by a missing inactive reference.** The
primary inactive ref (5NM4) is present and complete on all axes.
`delta_to_inactive` for AA2AR is not NaN. The AA2AR family term is
instead most consistent with the **"non-saturated cell state exposes what
other cells hide"** reading — AA2AR is the receptor where the ceiling
does not saturate, so the family term reads as +0.76 boltz rather than
as a ceiling-pinned near-zero.

Any manuscript sentence attributing AA2AR anomaly to reference-set
incompleteness is unsupported by 6c.

## Affects

- SC-B-11 (ladder-height covariates); AA2AR-in vs AA2AR-out reporting.
- The recurrent-anomaly line in the paper's Discussion.

## Manuscript sentence

> AA2AR is a standing anomaly in the campaign — the single largest
> per-receptor family term in the Block B panel (+0.76 on boltz;
> cognate 0.80 vs shuffled 0.04). This is not caused by a missing
> reference: AA2AR's primary inactive reference (5NM4) is present in the
> scoring-time bytes and computable on both predicate axes. AA2AR is
> instead the only receptor in Block B whose shuffled cell state is
> not floor- or ceiling-pinned on a backbone (boltz), so the family
> term is measurable rather than saturation-flattened. Panel slopes on
> Δ_ref tilt (continuous scale) shift +0.049 → −0.003 when AA2AR is
> excluded; AA2AR should be reported in the panel with an in/out
> sensitivity, not as a broken-reference outlier.

## Related

- MANUSCRIPT_FLAGS.md Flag B-11.
- Phase 6a §Family-term heterogeneity, §Ladder-height covariates.
- Phase 6c §AA2AR — standing anomaly.
- Auto-memory `apo_bistability_reference_artefact_2026_09_06.md`.
