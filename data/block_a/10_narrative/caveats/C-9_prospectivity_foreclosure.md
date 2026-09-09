# C-9 — Prospectivity foreclosure at Block A; the real test is the date-stratified holdout

## Caveat

Block A's `fraction-of-way-to-active` metric requires an active reference
structure for the denominator. All 48 panel receptors have one by design
(refs/reference_set.csv is fully populated per P6's audit). This means:

- Every receptor in the 0.89–0.95 fraction has a deposited active structure.
- Nothing is truly held-out from training at the *reference-availability*
  level within Block A's headline metric.
- Block A's headline is a **retrospective** claim ("does the model reach
  the deposited state when given the cognate partner?"), not a
  prospectivity claim.

## Correction to a prior framing

The pre-review dossier's Phase 6a listed SC-1 and SC-2 as headline-level
findings without stating the prospectivity foreclosure explicitly. The
scientific review flagged this at abstract-level. Additionally, the
review's specific line "7 receptors with no active reference" is inaccurate
— 48/48 have active refs. The mechanism of the foreclosure is not a
data gap; it is the metric's design.

## Where prospectivity lives

**T5's cluster-level recount is the authoritative measurement**:

| Cutoff | Receptor-level (P6 initial) | Cluster-level (T5, authoritative) | Verdict |
|---|---:|---:|---|
| AF3-lineage 2021-09-30 (Boltz-1, Chai-1, OF3-preview) | 24–26 | **13** | Above n=10 threshold |
| Extended 2023-01-13 (Boltz-2, Protenix v2) | 11–12 | **8** | **Underpowered; descriptive not inferential** |

**Receptor-level counts overstate prospectivity** because a receptor whose
paralog's active-Gα complex predates a backbone's training cutoff is not
truly held out — the model saw the fold and coupling geometry. Cluster-
level counts are computed on 26 paralog clusters (T7 mapping) and require
every cluster member's active-Gα to postdate the cutoff for the cluster to
count as held out.

**The 4 multi-member clusters** (chemokine, opioid, Class B secretin,
Class F Frizzled) at AF3-lineage cutoff: opioid (OPRX 8F7X 2022-12) and
Frizzled (FZD6 8JHB 2023-05) are HOLDOUT; chemokine (CXCR2 6LFO 2020-09)
and Class B secretin (GCGR 6LMK 2019-12) are NOT.

**Underpowered warning**: the extended-cutoff cluster-level count (n=8) is
below P6's own n≥10 threshold. Report as descriptive, not inferential.

Additionally, Block C tier 3 is a genuine prospectivity setting —
pharmacology-panel predictions on receptors whose ligand-side chemistry
does not require an active reference to score.

## Manuscript sentence

> Block A's headline `fraction-of-way-to-active` metric is retrospective by
> design: every panel receptor has a deposited active reference. Prospectivity
> is established by (1) a date-stratified cluster-level holdout using
> per-backbone PDB training cutoffs on 26 paralog clusters: 13 clusters at
> AF3-lineage cutoff (2021-09-30), 8 clusters at extended cutoff (2023-01-13);
> and (2) Block C tier 3, a pharmacology-panel setting where the classifier
> operates independently of an active reference. Receptor-level counts (24–26
> and 11–12) overstate prospectivity by treating paralogs as independent and
> are not the primary measurement.

## Related

- MANUSCRIPT_FLAGS.md Flags 3, 31.
- P6 fork report.
