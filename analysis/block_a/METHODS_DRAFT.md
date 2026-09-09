# Methods — Block A (draft)

Covers all nine items required by FIGURE_BRIEF §7. Markdown so that it can be
converted with `analysis/md2tex.py` once the lit session has finished editing
`manuscript/sections/`. Every number traces to a file in `data/block_a/`;
`analysis/block_a/verify_claims.py` re-derives the checkable ones.

**Unresolved before submission:** the reference-set denominator (D9) and the
four wording items in `DISCREPANCY_REPORT.md` (D1, D2, D3, D5) need a decision
from the PI. Placeholders below are marked `[PI]`.

---

## Panel

Predictions were run for 48 G-protein-coupled receptors — 40 Class A, 4 Class B
and 4 Class F — under two input conditions and on four co-folding backbones,
giving 380 receptor × backbone × arm cells and 9,490 scored predictions. Cells
hold a median of 25 predictions (minimum 20; the Boltz-2 cognate arm is short 10
rows, a documented gap).

Each receptor is paired with deposited active- and inactive-state reference
structures. The reference set comprises **[PI: 98 empirical / 89 as previously
stated]** unique Protein Data Bank entries across the panel — 44 in an
active-role and 54 in an inactive-role assignment — drawn from a total reference
collection of 167 entries. The three denominators are reconciled in Table S-T3
and the discrepancy with the previously circulated count of 89 is recorded as
D9; caveat C-6 documents the earlier figure. **This denominator must be stated
wherever the reference set is enumerated**, because the panel (48), the
panel-PDB set (98) and the full collection (167) are all defensible counts of
different things.

## Conformational predicates

Two intrinsic geometric measurements are computed on each predicted structure
alone. Neither is a comparison to a reference.

- **`d_npxxy_oh`** — the hydroxyl–hydroxyl distance between Tyr5.58 and Tyr7.53.
  On activation Tyr7.53 of the NPxxY motif rotates into the receptor core and
  packs against Tyr5.58 in an arrangement that is usually water-mediated. A
  prediction is called active on this axis **below** 9.080 Å.
- **`d_gpcrdb_tm6_tilt_246_637_ca`** — a Cα–Cα distance capturing outward
  displacement of the cytoplasmic end of TM6, the canonical activation
  signature. A prediction is called active **above** 14.932 Å.

A prediction is called active only when both fire. Thresholds are carried as
row-level columns (`threshold_npxxy_used`, `threshold_tilt_used`) and were read
from the data rather than reimplemented.

Both thresholds were derived from 80 tier-1 crystallographic reference rows by a
midpoint objective, and from no prediction. **Self-classification accuracy on
that set is a derivation-set figure, not a held-out one**, and is reported as
such. The models do not place water molecules; results are described as
consistent with the water-bridged arrangement, never as the bridge forming.

## Prediction protocol

Four co-folding models were used: Boltz-2, Chai-1, OpenFold3 and Protenix2. Each
received either the receptor sequence alone (**apo arm**) or the receptor
sequence together with its cognate Gα subunit (**cognate arm**). Templates were
disabled on all backbones, multiple sequence alignments were pinned, and no
reference structure was supplied to any model at any point. Twenty-five seeds
were run per condition.

The apo arm is a **computational reference condition, not a physical state** — no
ligand, no membrane, and no basal-activity equivalent. Real receptors show
constitutive activity that varies widely between receptors, and the apo arm
should not be equated with a physiological inactive state (C-7).

OpenFold3 seeds were generated as 5 outer × 5 inner after a seeding fix, so
OF3 rows are **less independent than the other backbones'**. This qualifies any
cross-backbone comparison of correlation magnitudes, including the confidence
correlations below.

Scoring used a single frozen scorer (version `0.1.0`, commit `04243c45`)
recorded per row.

## Uncertainty

**The cluster bootstrap is authoritative**: 1,000 resamples over 26 paralog
clusters, seed 20260909. A receptor-level bootstrap is approximately 1.10×
tighter and is reported as secondary, in supplementary tables only.

Eleven of the 26 clusters are singletons (42%), so the paralogy correction acts
on only 15 multi-member clusters (C-8). Cluster and receptor intervals are
compared in Figure S3.

All confidence intervals quoted in the main text and in Tables T2–T4 are cluster
intervals. **Intervals previously circulated as cluster bootstraps in the
internal claim sheet were in fact receptor bootstraps** and were correspondingly
narrower; they have been requoted from the cluster columns (D5).

## Exclusions

Five exclusion sets were pre-specified by cause and applied before results were
inspected. They are not a quality filter and are not applied as a union.

| set | n rows | rule | cause | scope |
|---|---:|---|---|---|
| E1 | 25 | cell mean pLDDT < 50 | one broken cell (ACM1/cognate/Protenix) | always |
| E2 | 4 | `d_npxxy_oh` < 2.4 Å | model-side atom clashes | always |
| E3 | 4,890 | receptor's reference fails its own predicate on that axis | reference-side failure, or the axis is undefined for that receptor | per axis, denominator and regression analyses only |
| E4 | 1,495 | Class B or Class F | instrument scope | Class-A claims |
| E5 | 500 | agonist-only actives (OPRD, CNR1, FZD4) | activation without transducer | sensitivity contrast only |

E1 and E2 together remove 29 rows (0.31%) and are applied everywhere. **E3 is
applied per axis** — `excl_E3_npxxy` (4,690 rows, 24 receptors) or
`excl_E3_tilt` (2,000 rows, 10 receptors) — and only where a reference value
serves as a denominator or a regression predictor. It merges two distinct causes:
references that genuinely fail the predicate, and receptors for which the axis is
not measurable at all (EDNRB, for example, carries Leu at 7.53, so an NPxxY
hydroxyl distance is undefined). The E3 union is never applied, and E3 is
irrelevant to raw distributions, predicate firing rates and confidence
correlations, which never touch a reference separation.

Every headline statistic was recomputed under every exclusion combination
(Table T5, Figure S5). **No sign flip occurs anywhere** and no statistic moves by
more than 0.5% from baseline.

## Confidence aggregation

Three aggregations of pLDDT were computed: the whole-complex mean
(`plddt_mean`), the mean over the six state-defining anchor residues 3.50, 3.51,
5.58, 6.30, 6.34 and 7.53 (`plddt_at_anchors`), and the minimum over those
anchors (`min_plddt_at_anchor`).

**`plddt_at_anchors` was designated the primary aggregation post hoc, after all
three had been computed** (W-2). All three are reported in Table T4. The
disclosure, not the designation, is what the result rests on.

## Data-layer verification

Both predicate axes were independently recomputed against non-scorer
implementations and agree bit-exactly (Pearson r = 1.000000). The predicate
booleans were recomputed from the raw axis values rather than trusted, and cell
counts were reconciled against the run manifest. Fold integrity was checked
independently: `tm6_helicity_pass` holds on 96.3% of rows.

## Known data-layer issues

Four rows carry sub-covalent hydroxyl–hydroxyl distances (< 2.4 Å), which are
model-side clashes rather than measurements; they are excluded as E2. One 25-row
cell (ACM1/cognate/Protenix) passed every assertion in the verification suite
because the suite has no pLDDT floor, and is excluded as E1. The NPxxY threshold
was truncated to 9.08 from 9.082, which changes the call for one borderline row
(C-12).

## Reference-set limitations

The `construct` annotation carried with the reference set contradicts the RCSB
record on approximately 40% of evaluable entries; the denominator for that rate
is **[PI: 162 empirical / 127 as previously stated]** (D9). Several references
carry fusion partners or engineered residues **inside the predicate windows**,
which is recorded per entry in Table S-T1 (`predicate_window_hit`, C-11). Nine
references deviate from their expected predicate call; **five of the nine are
unclassified** as to cause, with the remainder split between expected biology,
curation error, a measurement artifact, and one entry that could be either
(D10). Several entries annotated active were solved with agonist bound but no
transducer and do not form the NPxxY network, which the predicate reports
correctly.
