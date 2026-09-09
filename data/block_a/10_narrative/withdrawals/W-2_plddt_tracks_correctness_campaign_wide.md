# W-2 — "pLDDT tracks correctness" as a campaign-wide claim (RESTATED post-review)

## Claim as previously stated in the pre-scientific-review dossier

Prior campaign framing held that model confidence (`plddt_mean`) tracks
correctness, backbone-dependent per Phase 4f's per-backbone breakdown:

| Backbone | plddt_mean Pearson r [95% CI] |
|---|---|
| boltz | −0.064 [−0.233, +0.104] null |
| chai | +0.025 [−0.301, +0.292] null |
| of3 | −0.327 [−0.518, −0.128] signed neg |
| **protenix** | **+0.274 [+0.121, +0.437] signed POS** (overconfident) |

The pre-review framing was: "OF3 signed negative; Protenix signed positive
(overconfident); Boltz + Chai null" — leading to the claim "Protenix is
overconfident across the entire panel". This file's earlier version
underwrote that claim.

## Restatement (P3 finding, post-review)

**The Protenix-overconfident-across-panel claim was a `plddt_mean` artifact
of non-anchor residues** (Gα chain in the cognate arm; loops; termini). At
anchor-restricted grain (residues 3.50, 3.51, 5.58, 6.30, 6.34, 7.53 — the
state-defining anchors), the Protenix correlation collapses to null:

| Backbone | plddt_mean r (Phase 4f) | anchor_mean r (P3) | cluster-boot verdict (P7) |
|---|---|---|---|
| boltz | −0.064 null | **−0.221 [−0.357, −0.092]** SIGNED NEG | signed |
| chai | +0.025 null | −0.160 [−0.462, +0.144] null; anchor_min −0.332 signed | anchor_mean → NULL under cluster-boot; anchor_min holds |
| of3 | −0.327 signed neg | **−0.626 [−0.736, −0.497]** SIGNED STRONGLY NEG | signed strongly (strongest signal in the campaign) |
| **protenix** | **+0.274 signed POS** | **+0.068 [−0.159, +0.276] NULL** | **NULL both bootstraps** |

## Aggregation-search disclosure (T3)

Three anchor aggregations were computed on the same rows:
- `plddt_mean` — global mean over all residues (the retracted aggregation)
- `plddt_at_anchors` — mean over the state-defining anchor residues (3.50, 3.51, 5.58, 6.30, 6.34, 7.53) — what P3 reported as `anchor_mean`
- `min_plddt_at_anchor` — the minimum pLDDT across those six anchors — what P3 reported as `anchor_min`

`plddt_at_anchors` (anchor_mean) is designated **primary post hoc, not pre-specified**, on the rationale that it is the natural analogue of the retracted `plddt_mean` restricted to residues that carry state identity. Under the primary aggregation + cluster-boot, the campaign has **2 of 4 backbones signed** (Boltz + OF3), not 3. `anchor_min` is reported as secondary sensitivity; Chai's signed correlation on `anchor_min` (−0.332) is a secondary finding, not a primary one.

## OF3 independence caveat

OF3's r = −0.626 [−0.827, −0.601] (cluster-boot) is the strongest anchor-pLDDT-vs-RMSD correlation in the campaign. Two independence caveats apply that don't apply to the other three backbones equally:

1. **Effective independence of samples within a cell**. Per T3, primary Block A rows point at post-fix OF3 CIFs (100% overlap with rerun tree, 0 sentinel hits at inner-seed grain). OF3 has 5 unique outer seeds × 5 unique inner seeds per cell — clean. Within-cell independence at that grain is equivalent to the other three backbones. HOWEVER, OF3 pre-fix used a single internal seed (2746317213); primary rows are POST-fix but the corpus history is documented in W-6 and C-5. When comparing OF3 correlations to other-backbone correlations, note the OF3 corpus is a specific post-fix rescore of the same set of CIFs; other backbones' predictions never had this issue.
2. **The 5x within-cell factor**. Even with 5 real seeds, samples within a seed's 5-sample cluster share stochastic sampling from the same seeded process. Cross-backbone magnitude comparison of r-values is not like-for-like; cluster-boot already accounts for receptor-level dependence but not for the fine-grained within-seed correlation structure.

## What the manuscript should say instead

> pLDDT-vs-correctness is aggregation-dependent. Global `plddt_mean` is
> diluted by the Gα chain (cognate arm), loop residues, and termini, and
> reports a spurious positive correlation on Protenix (r=+0.274 [+0.121,
> +0.437]) that reverses at anchor-restricted grain (r=+0.068 [−0.159,
> +0.276]). At the state-defining anchor residues (3.50, 3.51, 5.58, 6.30,
> 6.34, 7.53), pLDDT tracks correctness on 2 of 4 backbones (Boltz r=−0.221
> [−0.357, −0.092]; OpenFold-3 r=−0.626 [−0.736, −0.497] — the strongest
> single confidence-vs-correctness signal in the campaign), with Chai
> signed only on the weakest-anchor aggregation (anchor_min r=−0.332), and
> Protenix null. Protenix is not overconfident at anchor grain.

## Related flags in `MANUSCRIPT_FLAGS.md`

- Flag 34: plddt_mean is the wrong aggregation
- Flag 35: OF3 anchor-pLDDT r=−0.626 is the strongest signal in the campaign
- Flag 39: Chai anchor_mean flips to null under cluster-boot (anchor_min holds)
- Flag 40: Anchor pLDDT signed-neg is authoritative on Boltz + OF3 only (cluster-boot)

## Provenance

- Prior claim: dossier §Phase 4f (`plddt_mean` × `rmsd_to_active_ref`), bootstrap over receptors, 1000 resamples seed 20260909.
- Restatement: P3 fork (anchor-pLDDT redo), same bootstrap, cluster-boot from P7 (26 paralog clusters).
- Column used: `plddt_at_anchors` in `data/block_a/rows.csv` (0% NaN, populated on all 9,490 rows; anchors defined by scorer's canonical position dictionary).

## Downstream implication (RESURFACED for other blocks)

**Prior version's claim about "downstream blocks that gate rows by pLDDT and
pool across backbones inherit Protenix's overconfidence" is retracted.** At
anchor grain, Protenix is not overconfident. The correct downstream rule:
downstream blocks that use pLDDT as a filter should use anchor pLDDT, not
plddt_mean.
