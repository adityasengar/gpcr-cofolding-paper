# C-D-1 — Cluster-boot degeneracy on D1 (n=7) and D2 (n=4)

## Caveat

D1's 7 receptors span 7 distinct paralog clusters (adrenergic_beta,
cannabinoid, chemokine_cxcr, ghrelin, lysophosphatidic, npy,
opsin_vertebrate — 1 receptor per cluster). D2's 4 receptors span
4 clusters (adrenergic_beta, angiotensin, muscarinic, opioid — also
1 rec/cluster).

**Cluster-boot equals receptor-boot** at this n. Reporting either as
"cluster-boot" adds no information beyond the receptor-level bootstrap
and would misleadingly imply hierarchical variance decomposition.

Per-cell CIs (n=500 samples for D1, n=50 for D2) are the authoritative
D1/D2 output. Panel-mean CIs are wide by construction — for example,
D1 Chai panel-mean at n=7 receptors is 42.6 % receptor-boot [14.1,
85.1]. This is 71 points wide because bootstrapping over 7 receptors
where 3 are near 100 % and 4 near 0 % has huge sample variance.

D3 (26 receptors, 22 clusters — some doubled: serotonin has 5HT1B/5HT2C;
chemokine_cxcr has CXCR2/CXCR4; opioid has OPRD/OPRK; opsin has invertebrate
JSR1 + vertebrate OPSD) has valid cluster-boot that adds signal beyond
receptor-boot.

## References

- `EXPERIMENT_DOSSIER_BLOCK_D.md` §Section 4 (this caveat).
- `BLOCK_D_STATE_CHECK.md` §Q6.
- `partA/PARTA_D1.md` §2 (D1 panel-level receptor-boot CIs).
- `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv` (cluster mapping, Block A C-8 convention).
