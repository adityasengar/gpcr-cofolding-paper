# C-8 — Cluster-bootstrap is the authoritative CI

## Caveat

Every CI in the dossier's Phase 4 and P1b/P3 analyses was computed with
receptor-bootstrap — treating each of the 48 panel receptors as an
independent draw. That treatment is optimistic because the panel contains
paralogous receptor pairs and small families (ADRB1/ADRB2, opioid family,
aminergic cluster, chemokine cluster, Class B secretin family, Class F
Frizzled). Cluster-bootstrap on 26 paralog clusters widens CIs.

## P7 findings

- Median CI widening: **1.10×** across all analyses (much less than the
  review's 30–100% expectation — paralogy is NOT the load-bearing driver
  of precision in this panel).
- Maximum widening: 2.21× (Protenix delta_to_active shift).
- 3 of 26 previously-signed findings flip to null under cluster-boot:
  - P1b Protenix tilt slope (+0.503 → null)
  - P3 Chai anchor_mean (−0.241 → null; anchor_min still signed)
  - P3 Protenix anchor_min (−0.315 → null)
- All 3 flips were "barely signed" at receptor-boot (upper/lower CI within
  0.1 of zero).

## Load-bearing findings that SURVIVE cluster-boot

- Phase 4a headline: 4/4 backbones on tilt shift, delta_to_active shift,
  and fraction-of-way-to-active.
- P1b amplitude flatness (all 4 backbones null on tilt slope) — reinforced.
- P3 anchor pLDDT: Boltz + OF3 signed on both anchor_mean and anchor_min.
- Phase 4d apo-active rate: 4/4 backbones signed non-zero.
- Phase 4c two-instrument agreement: 4/4 backbones above 0.5.

## Cluster size distribution (T5 finding)

The 26 clusters are dominated by singletons:

| Size | Count | Notable |
|---|---:|---|
| 1 | 11 | angiotensin, orexin, cholecystokinin, ghrelin, LPA, LT4, MCH, apelin, bombesin, ADA2A, SMO |
| 2 | 9 | ADRB, DRD, HRH, adenosine, cannabinoid, NPY, endothelin, glycoprotein, opsin |
| 3 | 5 | 5HT (5HT1B/2C/5A), ACM, opioid, chemokine, Frizzled |
| 4 | 1 | Class B secretin |

**42% of clusters are singletons**. The paralogy correction is doing work on
only the 15 multi-member clusters; singleton clusters get zero correction
from cluster-bootstrap. This is a partial explanation for the modest 1.10×
widening — paralogy is a real concern on the 15 multi-member clusters, but
half the panel is family-unique and gets no additional widening from the
cluster construct.

## Manuscript convention

**Report cluster-bootstrap CIs as authoritative.** Where a Methods section
mentions the bootstrap procedure, state:

> Confidence intervals are 1000-resample bootstraps over 26 paralog
> clusters (aminergic subfamilies grouped; opioid, chemokine, Class B
> secretin, Class F Frizzled+Smoothened as separate clusters; singletons
> for unique-family receptors — 11 of 26 clusters, 42%). Receptor-bootstrap
> CIs (48 receptors treated as independent) are ~1.10× tighter and are not
> the reported primary measurement.

**Post-hoc aggregation designation for anchor pLDDT**: three anchor
aggregations were computed (`plddt_mean`, `plddt_at_anchors` = anchor_mean,
`min_plddt_at_anchor` = anchor_min). `plddt_at_anchors` is designated
primary POST HOC (not pre-specified). Under primary + cluster-boot: **2 of
4 backbones signed** (Boltz + OF3). Chai anchor_min signal is secondary
sensitivity. See W-2.

## Related

- MANUSCRIPT_FLAGS.md Flags 11, 37, 38, 39, 40.
- P7 fork report (transcript preserved in session).
