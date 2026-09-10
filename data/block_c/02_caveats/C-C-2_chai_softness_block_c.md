# C-C-2 — Chai is a soft predictor on Block C, backbone-heterogeneous

**Applies to**: every four-backbone claim in Block C.

**The finding**: on the KILL-S1 row (apo × self-ref-excluded × F_iii
features), Chai's pooled LORO AUROC (0.706) is materially below Boltz
(0.852) and Protenix (0.825), and its cluster-boot 95 % CI [0.351,
0.941] spans 0.5. Chai's 2×2 pocket-Cα-RMSD interaction magnitude
(−0.137 Å) is likewise the smallest of the four backbones (Boltz −0.306,
OF3 −0.252, Protenix −0.184). Chai's pLDDT is famously miscalibrated —
S3's consensus-vs-pLDDT test shows the biggest confidence-signal gain
on Chai (+0.124 AUROC at top-25 % coverage; see SC-C-3), which is
consistent with Chai's per-prediction confidence being noisier than
the other three.

**Consequence**: manuscript sentences that pool a "four-backbone
average" on Block C hide the Chai softness. Block A + Block B's
"never average across backbones silently" convention applies to Block C
verbatim — every four-backbone table in the manuscript shows the four
values separately, and any "consistent across backbones" language
requires Chai's row to sit within the same qualitative bucket.

**Backbone-independent adjudication**: on the SC-C-1 2×2 interaction,
all four backbones sign non-zero in the same direction (agonist closer
to active reference than antagonist). Chai is the smallest magnitude
but not the wrong sign. Cluster-boot CI on the 2×2 interaction was
not recomputed in this pass (Flag C-12); the signed-direction claim
rests on the receptor-boot CIs already recorded in the audit JSON.

**Do NOT**: quote a "four-backbone mean" without stating the range and
naming Chai as the softest.

**Source**: `g1_bootstrap_s1_auroc.json`, `stage3_2x2_ligand_state_specificity.json`,
`s3_consensus_confidence.json`.
