# C-C-3 — 2×2 interaction: 23-set pinned, cluster-boot CIs applied

**Applies to**: SC-C-1 (2×2 pocket-Cα-RMSD ligand-state × reference-state
interaction).

**Status: RESOLVED 2026-09-10** (post-verification recompute). The
caveat is retained for provenance; the "convention pending" concern is
closed.

## Receptor set (pinned)

SC-C-1's four point estimates (Boltz −0.306, Chai −0.137, OF3 −0.252,
Protenix −0.184 Å) are computed on the **23-receptor 2×2 common set**,
not on the S1 15-set (which is for SC-C-4 KILL-S1) nor on all 36 landed
receptors. Verified via
`experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3_2x2_ligand_state_specificity.json`
(`per_backbone.<bb>.interaction.n_receptors_in_common = 23` uniformly).

**Pinned 23-receptor list** (identical to `s1_loro_classifier.json`'s
`common_receptors`): 5HT1B, 5HT5A, AA1R, AA2AR, ACM2, ACM4, ADRB2,
AGTR1, CCR5, CNR1, CNR2, CXCR2, CXCR4, EDNRB, GRPR, LPAR1, LT4R1,
MCHR1, NPY1R, NPY2R, OPRD, OPRK, OPRX.

## Cluster-boot CIs (applied)

23 receptors map to **16 paralog clusters** (per
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`).
All 23 have cluster assignments. 5000-iteration bootstrap, seed 1234
(matching the receptor-boot's protocol with the resampling unit swapped
from receptor to cluster).

| backbone | point (Å) | cluster-boot 95 % CI | receptor-boot 95 % CI (secondary) | signed non-zero? |
|---|---:|---|---|---|
| boltz | −0.306 | **[−0.454, −0.164]** | [−0.431, −0.192] | YES |
| chai | −0.137 | **[−0.216, −0.045]** | [−0.223, −0.055] | YES |
| of3 | −0.252 | **[−0.405, −0.099]** | [−0.384, −0.129] | YES |
| protenix | −0.184 | **[−0.277, −0.088]** | [−0.271, −0.101] | YES |

**All four backbones' cluster-boot 95 % CIs sign non-zero.** SC-C-1's
"signed non-zero on all four backbones" claim survives cluster-boot.
Cluster-boot CIs are ~15–25 % wider than receptor-boot (expected — fewer
independent units). Chai's cluster-boot upper bound (−0.045) is closer
to zero than receptor-boot's (−0.055); still signed with a narrow
margin.

## Post-verification action

- `BLOCK_C_CLAIM_SHEET.md § SC-C-1` updated 2026-09-10 to name the
  cluster-boot 95 % CI as primary and the receptor-boot as secondary,
  per Block A's C-8 authoritative convention.
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json`
  is the on-disk recompute (5000 iterations, seed 1234, cluster map
  from Block B paralog file).

**Source of point estimates**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3_2x2_ligand_state_specificity.json`.
**Source of cluster-boot CIs**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json`.
