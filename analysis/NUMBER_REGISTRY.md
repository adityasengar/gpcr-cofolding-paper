# NUMBER_REGISTRY.md — every number in the paper, and where it came from

**Generated and maintained alongside `analysis/sweep_manuscript.py`.** Run:

```bash
python3 analysis/sweep_manuscript.py     # exits 1 if a number has no entry
```

## Why this exists

Three times now a number reached a draft from a claim sheet that its own data
did not reproduce: Block A's `matches_claim_sheet` column, Block B's
`matches_claim_sheet_bool` on eight continuous medians, and Block B's
per-backbone family shares, which had the panel figure copied into three of the
four slots. Rereading the sections caught none of them. A number cannot be
checked by looking at it.

So: **a number may not enter Results or Methods without a line here.** Adding
the line is the step that forces the question "where did this come from?" at the
moment the sentence is written, rather than at review.

This registry does **not** re-verify values. `analysis/block_a/verify_claims.py`
and `analysis/block_b/verify_claims.py` do that. This answers a different
question: *is there anything in the paper nobody has accounted for?*

## Status

| | count |
|---|---:|
| unique numeric tokens in Results + Methods | **255** |
| covered by an automated check | **117** |
| **not covered by any automated check** | **138** |

**That second row is the finding of this sweep, and it is not comfortable.**
Fewer than half the numbers in the paper are recomputed by anything. The rest
are transcriptions from shipped tables — the exact class of number that has now
been wrong four times: Block A's `matches_claim_sheet`, Block B's
`matches_claim_sheet_bool` on eight continuous medians, Block B's per-backbone
family shares with the panel figure copied into three of four slots, and Block
C's SC-C-2 table headed "Kendall's τ" while containing a fraction of receptors.

**The fourth was caught by drawing it, not by reading it** (D-C-3). It had
passed the claim sheet, the dispatch and our own Results.

The fix is not to write prose entries for the remaining 138. It is to **extend
the three verifiers to cover them**, and let this file shrink to the numbers
that genuinely cannot be recomputed. Entries marked `auto` were matched
mechanically against a check id at the manuscript's own precision — the paper
writes 5.04 where the check holds 5.036 — and should be confirmed, not trusted.

---

## Covered by an automated check

| number | where | source | context |
|---|---|---|---|
| 48 | M8 | Block A, verify_claims check CORPUS | Predictions were run for 48 G-protein-coupled receptors --- 40 Class~A, 4 |
| 10 | M12 | Block B, verify_claims check B28.apo,B49.Ga-complexed-chimera-or-miniG | Boltz-2 cognate arm is short 10 rows, a documented gap). |
| 9.080 | M39 | Block B, verify_claims check B20 | axis below 9.080~\AA. |
| 14.932 | M43 | Block B, verify_claims check B22 | activation signature  . A prediction is called active above 14.932~\AA. |
| 7 | M74 | Block B, verify_claims check B28.cognate,B28.decoy,B28.shuffled | applicable to an unseen one: an outward swing of some 7--14~\AA{} at 6.26 |
| 14 | M74 | Block B, verify_claims check B32.boltz | applicable to an unseen one: an outward swing of some 7--14~\AA{} at 6.26 |
| 6.26 | M74 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | applicable to an unseen one: an outward swing of some 7--14~\AA{} at 6.26 |
| 6.42 | M75 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | ; 18~\AA{} at 6.42 and 17.4~\AA{} at |
| 6.36 | M76 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 6.36 in the same work  ; and around 14~\AA{} with |
| 6 | M116 | Block B, verify_claims check B08 | 2$\times$46 and 6$\times$37 and hydroxyl positions at Ballesteros--Weinstein |
| 12 | M177 | Block B, verify_claims check B59 | consequences, and we report them separately. On the NPxxY axis, 12 receptors |
| 500 | M188 | Block A, verify_claims check EXCL | instrument scope. E5 (500 rows) marks agonist-only actives and is shown as a |
| 32 | M200 | Block B, verify_claims check B33b.alpha5ct | 1,600 rows and 32 receptors per backbone. |
| 19 | M210 | Block B, verify_claims check B56,B57 | \textbf{35 (81\%) predate the Boltz-2 structural cutoff of 2023-06-01}, 19 |
| 9.08 | M244 | Block B, verify_claims check B20, the value every row carries | and is excluded as E1. The NPxxY threshold was truncated to 9.08 from 9.082, |
| 9.082 | M244 | Block B, verify_claims check B20 establishes rows carry 9.08 not this | and is excluded as E1. The NPxxY threshold was truncated to 9.08 from 9.082, |
| 18.92 | R438 | Block C, verify_claims check C56 | restriction. Across those 23, \textbf{18.92\%} of apo-arm agonist and antagonist |
| 35.85 | R440 | Block C, verify_claims check C57.agonist | \textbf{35.85\% of agonist rows against 2.00\% of antagonist rows}. An asymmetry |
| 2.00 | R440 | Block C, verify_claims check C57.antag | \textbf{35.85\% of agonist rows against 2.00\% of antagonist rows}. An asymmetry |
| 0.241 | R447 | Block C, verify_claims check C58 | receptor's own median $\tau$ gives Spearman $\rho = -0.241$ ($p = 0.268$, |
| 0.268 | R447 | Block C, verify_claims check C58.p | receptor's own median $\tau$ gives Spearman $\rho = -0.241$ ($p = 0.268$, |
| 0.436 | R449 | Block C, verify_claims check C59.p | either (Mann--Whitney $p = 0.436$, medians 0.282 against 0.386). The receptors |
| 0.282 | R449 | Block C, verify_claims check C59.hi | either (Mann--Whitney $p = 0.436$, medians 0.282 against 0.386). The receptors |
| 0.386 | R449 | Block C, verify_claims check C59.lo | either (Mann--Whitney $p = 0.436$, medians 0.282 against 0.386). The receptors |
| 21 | M271 | Block B, verify_claims check B32.of3 | G$\alpha$ subunit.} The $\alpha$5 C-terminal 21-mer is a region we measure and |
| 0.09 | M294 | Block C, verify_claims check C14.protenix | 0.06--0.09 on conditional activation rates. Engagement is a separate, |
| 12.19 | M297 | Block B, verify_claims check B59 | insertion depth of 12.19~\AA{} --- so engagement is reported alongside the |
| 37.5 | M332 | Block B, verify_claims check B51 | mini-G, chimera or nanobody-stabilised; 15 of 40 active references (37.5\%) are |
| 8 | M383 | Block B, verify_claims check B28.decoy | 8~\AA, entrance-bound between 8 and 15~\AA, and off-site above 15~\AA. |
| 168 | R11 | Block C, verify_claims check C18 | reference structures, where the answer is already known. Across 168 reference |
| 80 | R16 | Block B, verify_claims check B48 | were fitted on 80 of these same reference rows, so 159/168 measures internal |
| 1 | R35 | Block B, verify_claims check B07,B17,B19 | equivalent would inherit that heterogeneity silently (Fig.~1). |
| 40 | R44 | Block B, verify_claims check B09 | the 40 Class~A receptors (Fig.~2, Table~2), though with a five-fold spread in |
| 2 | R44 | Block B, verify_claims check B33.occupancy,B49.agonist-only-no-partner | the 40 Class~A receptors (Fig.~2, Table~2), though with a five-fold spread in |
| 1.05 | R46 | Block A, verify_claims check SC-1 | Chai-1's $+1.05$~\AA{} against Protenix2's $+5.31$~\AA{} should not be read as |
| 5.31 | R46 | Block A, verify_claims check SC-1 | Chai-1's $+1.05$~\AA{} against Protenix2's $+5.31$~\AA{} should not be read as |
| 160 | R48 | Block B, verify_claims check B40.apo_all | than a graded shift: 111 of 160 apo cells never fire the predicate on any of 25 |
| 25 | R48 | Block B, verify_claims check B49.Ga-complexed-native | than a graded shift: 111 of 160 apo cells never fire the predicate on any of 25 |
| 5.04 | R54 | Block A, verify_claims check SC-1 | $+5.04$~\AA{} (Boltz-2, 95\% CI $[3.53, 5.55]$), |
| 4.81 | R56 | Block A, verify_claims check SC-1 | $+4.81$~\AA{} (OpenFold3, $[3.95, 5.21]$) and |
| 16.0 | R58 | Block B, verify_claims check B41.cognate_active_engaged,B41.decoy_active_engaged,B41.shuffled_active_engaged | Pooled row-level predicate-active rates move from 16.0\% to 83.4\% (Boltz-2), |
| 26 | R60 | Block B, verify_claims check B12 | (Protenix2). All intervals are cluster bootstraps over 26 paralog clusters and |
| 5 | R105 | Block B, verify_claims check B04,B14.4,B28.cognate | reduced partner --- the $\alpha$5 C-terminus alone --- is sufficient, and whether |
| 204 | R139 | Block A, verify_claims check SC-3 | active, 204 of 256 (79.7\%) fall below the reference-inactive median on the |
| 0.56 | R145 | Block B, verify_claims check B25.decoy | delta $-0.56$~\AA{} against a reference delta of $-1.51$~\AA). The interval on |
| 5.22 | R161 | Block A, verify_claims check SC-3 | 5.22~\AA{} --- the regression of predicted shift on reference separation gives |
| 0.04 | R162 | Block A, verify_claims check SC-6 | slopes of 0.04 (Boltz-2), 0.37 (Chai-1), 0.18 (OpenFold3) and 0.26 (Protenix2) |
| 28 | R163 | Block A, verify_claims check SC-3 | across 28 Class~A receptors (Fig.~3, Table~3). Three of four show no evidence of |
| 3 | R163 | Block B, verify_claims check B49.nanobody-stabilised | across 28 Class~A receptors (Fig.~3, Table~3). Three of four show no evidence of |
| 1.17 | R171 | Block A, verify_claims check SC-3 | 1.17~\AA{} against NPxxY's 5.22~\AA, and under Class-A restriction two of four |
| 0.66 | R172 | Block B, verify_claims check B33.family,B37.decoy | slopes are negative (Boltz-2 $-0.30$, Chai-1 $-0.66$). A negative slope is not |
| 39 | R181 | Block A, verify_claims check SC-2 | fraction in Table~2, a median over 39 receptors. \textbf{The fraction is a mean; |
| 3.50 | R189 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | and by termini. Restricted to the six state-defining anchor residues (3.50, |
| 3.51 | R190 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 3.51, 5.58, 6.30, 6.34, 7.53) it carries information about conformational |
| 5.58 | R190 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 3.51, 5.58, 6.30, 6.34, 7.53) it carries information about conformational |
| 6.30 | R190 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 3.51, 5.58, 6.30, 6.34, 7.53) it carries information about conformational |
| 6.34 | R190 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 3.51, 5.58, 6.30, 6.34, 7.53) it carries information about conformational |
| 7.53 | R190 | generic numbering (Ballesteros--Weinstein / GPCRdb position, not a measurement) | 3.51, 5.58, 6.30, 6.34, 7.53) it carries information about conformational |
| 4 | R191 | Block A, verify_claims check EXCL | correctness --- on two of four backbones (Fig.~4, Table~4). |
| 0.10 | R193 | Block C, verify_claims check C14.of3 | Whole-complex against anchor-restricted Pearson correlations are $-0.10$ (null) |
| 0.22 | R194 | Block C, verify_claims check C13.chai | against $-0.22$ (signed) for Boltz-2; $+0.07$ (null) against $-0.16$ (null) for |
| 0.16 | R194 | Block B, verify_claims check B25.apo | against $-0.22$ (signed) for Boltz-2; $+0.07$ (null) against $-0.16$ (null) for |
| 640 | R229 | Block B, verify_claims check B02 | samples --- 32,000 predictions, every one of the 640 receptor $\times$ arm |
| 50 | R230 | Block B, verify_claims check B03,B33b.occupancy | $\times$ backbone cells delivering exactly 50 rows with five distinct seeds. |
| 9 | R233 | Block B, verify_claims check B20 | the receptor's own cognate G$\alpha$ subunit with the last 9--11 residues of the |
| 11 | R233 | Block B, verify_claims check B28.apo,B31b.family,B32.protenix | the receptor's own cognate G$\alpha$ subunit with the last 9--11 residues of the |
| 0.158 | R243 | Block B, verify_claims check B25.apo | monotonically across those four arms: 0.158 [0.081, 0.256] apo, 0.558 |
| 0.558 | R243 | Block B, verify_claims check B25.decoy | monotonically across those four arms: 0.158 [0.081, 0.256] apo, 0.558 |
| 0.809 | R244 | Block B, verify_claims check B25.shuffled | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.891 | R244 | Block B, verify_claims check B25.cognate | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.942 | R244 | Block B, verify_claims check B43 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 36 | R245 | Block B, verify_claims check B24 | cognate, on the 36 receptors whose NPxxY axis is defined, with cluster-bootstrap |
| 0.5 | R255 | Block C, verify_claims check C13.boltz | not: within $\pm$0.5~\AA{} of the tilt threshold the cognate arm carries |
| 0.00 | R257 | Block B, verify_claims check B05,B06,B23 | against 3.33\% on Boltz-2, 0.39\% against 1.89\% on OpenFold3, 0.00\% against |
| 0.06 | R258 | Block B, verify_claims check B46 | 0.06\% on Protenix2). Chai-1 inverts, at 1.83\% against 0.56\%, and that |
| 0.400 | R266 | Block B, verify_claims check B31.occupancy | partner, even one whose $\alpha$5 tail is scrambled, accounts for $+0.400$ |
| 55 | R267 | Block B, verify_claims check B31b.occupancy,B35 | [0.328, 0.464] of the total rise, 55\%. Restoring a real $\alpha$5-CT sequence |
| 0.252 | R268 | Block B, verify_claims check B31.alpha5ct | adds $+0.252$ [0.188, 0.321], 34\%. Getting the family \emph{right} adds |
| 34 | R268 | Block B, verify_claims check B31b.alpha5ct,B35 | adds $+0.252$ [0.188, 0.321], 34\%. Getting the family \emph{right} adds |
| 0.082 | R269 | Block B, verify_claims check B31.family | $+0.082$ [0.047, 0.125]. On the probability scale that last term is 11\% of the |
| 17.4 | R270 | Block B, verify_claims check B32.boltz,B33b.family | total; on the logit scale it is 17.4\% [0.39, 1.09], and both are correct. The |
| 24 | R272 | Block B, verify_claims check B32.of3,B45 | above 0.98 in 24--34 of 40 cells per backbone, and a probability-scale |
| 14.2 | R277 | Block B, verify_claims check B32.boltz | Its per-backbone logit shares span 14.2\%, 22.9\%, 23.6\% and 10.9\% for |
| 22.9 | R277 | Block B, verify_claims check B32.chai | Its per-backbone logit shares span 14.2\%, 22.9\%, 23.6\% and 10.9\% for |
| 23.6 | R277 | Block B, verify_claims check B32.of3 | Its per-backbone logit shares span 14.2\%, 22.9\%, 23.6\% and 10.9\% for |
| 10.9 | R277 | Block B, verify_claims check B32.protenix | Its per-backbone logit shares span 14.2\%, 22.9\%, 23.6\% and 10.9\% for |
| 20 | R291 | Block B, verify_claims check B47 | 20~\AA{} $\alpha$5-tip-to-R3.50 cutoff, the cognate arm engages on 0.998 of rows |
| 0.998 | R291 | Block B, verify_claims check B36.cognate | 20~\AA{} $\alpha$5-tip-to-R3.50 cutoff, the cognate arm engages on 0.998 of rows |
| 0.893 | R292 | Block B, verify_claims check B37.cognate | and is active on 0.893 of those; shuffled engages on 0.967 and is active on |
| 0.967 | R292 | Block B, verify_claims check B36.shuffled | and is active on 0.893 of those; shuffled engages on 0.967 and is active on |
| 0.835 | R293 | Block B, verify_claims check B37.shuffled | 0.835; decoy engages on 0.704 and is active on 0.665. The engaged-but-inactive |
| 0.704 | R293 | Block B, verify_claims check B36.decoy | 0.835; decoy engages on 0.704 and is active on 0.665. The engaged-but-inactive |
| 0.665 | R293 | Block B, verify_claims check B37.decoy | 0.835; decoy engages on 0.704 and is active on 0.665. The engaged-but-inactive |
| 15.42 | R301 | Block B, verify_claims check B41.decoy_engaged_but_inactive | active sit at 15.42~\AA{} (47 cells), against 15.35~\AA{} for apo and 16.00--16.04~\AA{} |
| 47 | R301 | Block B, verify_claims check B40.decoy_engaged_but_inactive | active sit at 15.42~\AA{} (47 cells), against 15.35~\AA{} for apo and 16.00--16.04~\AA{} |
| 15.35 | R301 | Block B, verify_claims check B41.apo_all | active sit at 15.42~\AA{} (47 cells), against 15.35~\AA{} for apo and 16.00--16.04~\AA{} |
| 16.00 | R301 | Block B, verify_claims check B41.shuffled_active_engaged | active sit at 15.42~\AA{} (47 cells), against 15.35~\AA{} for apo and 16.00--16.04~\AA{} |
| 16.04 | R301 | Block B, verify_claims check B41.cognate_active_engaged | active sit at 15.42~\AA{} (47 cells), against 15.35~\AA{} for apo and 16.00--16.04~\AA{} |
| 0.024 | R310 | Block B, verify_claims check B44 | the tilt residual against each receptor's own active reference is $+0.024$~\AA{} |
| 0.062 | R311 | Block B, verify_claims check B46 | [$-0.29$, $+0.30$] across 24 receptors, and $-0.062$~\AA{} [$-0.41$, $+0.21$] |
| 0.41 | R311 | Block B, verify_claims check B47b | [$-0.29$, $+0.30$] across 24 receptors, and $-0.062$~\AA{} [$-0.41$, $+0.21$] |
| 0.21 | R311 | Block B, verify_claims check B47b | [$-0.29$, $+0.30$] across 24 receptors, and $-0.062$~\AA{} [$-0.41$, $+0.21$] |
| 0.454 | R365 | Block C, verify_claims check C13.boltz | backbones: $-0.306$~\AA{} on Boltz-2 [$-0.454$, $-0.164$], $-0.137$ on Chai-1 |
| 0.164 | R365 | Block C, verify_claims check C14.boltz | backbones: $-0.306$~\AA{} on Boltz-2 [$-0.454$, $-0.164$], $-0.137$ on Chai-1 |
| 0.216 | R366 | Block C, verify_claims check C13.chai | [$-0.216$, $-0.045$], $-0.252$ on OpenFold3 [$-0.405$, $-0.099$] and $-0.184$ |
| 0.045 | R366 | Block C, verify_claims check C14.chai | [$-0.216$, $-0.045$], $-0.252$ on OpenFold3 [$-0.405$, $-0.099$] and $-0.184$ |
| 0.405 | R366 | Block C, verify_claims check C13.of3 | [$-0.216$, $-0.045$], $-0.252$ on OpenFold3 [$-0.405$, $-0.099$] and $-0.184$ |
| 0.099 | R366 | Block C, verify_claims check C14.of3 | [$-0.216$, $-0.045$], $-0.252$ on OpenFold3 [$-0.405$, $-0.099$] and $-0.184$ |
| 0.277 | R367 | Block C, verify_claims check C13.protenix | on Protenix2 [$-0.277$, $-0.088$], over 23 receptors resampled as 16 paralog |
| 0.088 | R367 | Block C, verify_claims check C14.protenix | on Protenix2 [$-0.277$, $-0.088$], over 23 receptors resampled as 16 paralog |
| 23 | R367 | Block B, verify_claims check B32.chai | on Protenix2 [$-0.277$, $-0.088$], over 23 receptors resampled as 16 paralog |
| 16 | R367 | Block B, verify_claims check B29.decoy,B29.shuffled,B41.cognate_active_engaged | on Protenix2 [$-0.277$, $-0.088$], over 23 receptors resampled as 16 paralog |
| 15 | R381 | Block B, verify_claims check B17,B22,B41.apo_all | is 0.26--0.39 across backbones, on the 23-receptor panel. On the 15-receptor |
| 67 | R382 | Block C, verify_claims check C07b | self-reference-excluded subset the receptor fractions are 67--87\% and the |
| 0.45 | R383 | Block C, verify_claims check C13.boltz | median $\tau$ 0.20--0.45. Because its threshold was fixed in advance, this test |
| 0.656 | R391 | Block B, verify_claims check B33.family | permutation null. On Chai-1 (0.706) and OpenFold3 (0.656) the same intervals |
| 54 | R422 | Block A, verify_claims check EXCL | bimodal --- median dock rates of 54--56\% on Boltz-2 against 0--18\% on Chai-1 |
| 0 | R422 | Block B, verify_claims check B05,B06,B23 | bimodal --- median dock rates of 54--56\% on Boltz-2 against 0--18\% on Chai-1 |
| 18 | R422 | Block B, verify_claims check B29.cognate,B29.shuffled,B32.chai | bimodal --- median dock rates of 54--56\% on Boltz-2 against 0--18\% on Chai-1 |
| 15.1 | R427 | Block C, verify_claims check C05.apo | across all 40,000 predictions: 15.1\% of apo-arm and 20.3\% of cognate-arm |
| 20.3 | R427 | Block C, verify_claims check C05.cognate | across all 40,000 predictions: 15.1\% of apo-arm and 20.3\% of cognate-arm |
| 1.52 | R430 | Block C, verify_claims check C07 | antagonist --- that figure is \textbf{1.52\%}. The contrast is not built on |
| 17.5 | R431 | Block B, verify_claims check B29.cognate,B32.chai,B32.protenix | mis-docked ligands. Peptide agonists sit at a median of 17.5~\AA{} because |
| 66.5 | R433 | Block B, verify_claims check B37.decoy | counting it as failure would produce a 66.5\% error rate where the true |
| 9,461 | S98 | Block A, verify_claims check CAP1 | E1+E2; $n = 9,461$ rows. Overall pass rate 96.3\%. |
| 5,093 | S34 | Block A, verify_claims check CAP2 | Applying the union would remove 5,093 of 9,490 rows (54\%) and would change |
| 7,966 | F32 | Block A, verify_claims check CAP3 | E1+E2, then Class~A only --- 7,966 of 9,490 rows, forming |
| 120 | F28 | Block A, verify_claims check CAP5 | cognate, with the identity line labelled; 120 of 159 move up, 37 are unchanged |
| 319 | F33 | Block A, verify_claims check CAP8 | 319 cells and 159 receptor x backbone pairs with both arms. |
| 2,611 | S170 | Block A, verify_claims check CAP9.apo | 2,611 firing neither predicate, 577 firing both. Cognate: 157 and 3,162. |
| 577 | S170 | Block A, verify_claims check CAP10.apo | 2,611 firing neither predicate, 577 firing both. Cognate: 157 and 3,162. |
| 157 | S170 | Block A, verify_claims check CAP9.cognate | 2,611 firing neither predicate, 577 firing both. Cognate: 157 and 3,162. |
| 3,162 | S170 | Block A, verify_claims check CAP10.cognate | 2,611 firing neither predicate, 577 firing both. Cognate: 157 and 3,162. |
| 610 | S88 | Block A, verify_claims check CAP11 | Note the denominator: of 4,866 predicate-active rows, 610 carry no active |
| 61.8 | R521 | Block D, verify_claims check D16 | (95\% CI $[61.8, 86.9]$) --- and the shipped structure shows why that is not a |
| 86.9 | R521 | Block D, verify_claims check D16 | (95\% CI $[61.8, 86.9]$) --- and the shipped structure shows why that is not a |
| 4.53 | R524 | Block D, verify_claims check D22 | 4.53~\AA{}, which we measured from the coordinates \textbf{[FIG:nb-structures]}. |
| 33.7 | R531 | Block D, verify_claims check D15 | and at 50 samples that interval is $[33.7, 62.6]$.} And the whole of this |
| 62.6 | R531 | Block D, verify_claims check D15 | and at 50 samples that interval is $[33.7, 62.6]$.} And the whole of this |
| 14,000 | M455 | Block D, verify_claims check D09 | purpose, and it does so three ways. \textbf{D1} runs 14,000 predictions on |
| 2,370 | M457 | Block D, verify_claims check D11c | and asks what the models do when nothing is supplied. \textbf{D2} runs 2,370 |
| 22 | M466 | Block D, verify_claims check D07 | arithmetic rather than preference.} D3's 26 receptors resolve into 22 paralog |
| 22 | M472 | Block D, verify_claims check D07 | 22, 7 and 4 all reproduce from the shipped paralogy map. |
| 2.303 | M477 | Block D, verify_claims check D21 | 2.303. The unit is written \%/ln(depth) everywhere it appears. |
| 4,866 | S88 | Block A, verify_claims check CAP12 | of 4,866 predicate-active rows, 610 carry no active |
| 4,256 | S87 | Block A, verify_claims check CAP13 | n = 4,256 testable of 4,866 predicate-active |
## NOT covered by any automated check

Each of these needs one of three things: a new check in the relevant
`verify_claims.py`; a registry line naming the shipped file and filter it was
transcribed from; or removal from the manuscript. Ranked work, not a to-do list
to be admired.

Known categories in what follows:

- **literature values** belonging to a citation (`1,351 class~A structures`,
  `63 post-cutoff pairs`) — these are the lit session's to verify, not ours, and
  `lit/validate/` already checks quotes and pages.
- **design constants** (48 receptors, 4 backbones, 25 seeds, 1,000 resamples,
  seed 20260909) — recomputable and worth a cheap check each.
- **exclusion-set row counts** (4,890, 1,495, 500, 2,295, 2,395) — these are
  recomputable from the flags and should be checked, because Block B's
  exclusion labels were wrong in the claim sheet and ours could be too.
- **two `[PI]` placeholders** (98/89 and 162/127) — blocked on the pipeline
  agent, tracked in `analysis/block_a/DATA_REQUESTS.md`.
- **tokeniser noise** (`0.1.0`, `20260909`, date fragments) — the sweep should
  learn to skip these rather than have them registered.

| number | where | context |
|---|---|---|
| 70 | F62 | references carrying the NPxxY axis, drawn in BA-1a panel d; 2,295 of the reference rows have no NPxxY because 7.53 is not Tyr |
| 350 | S236 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 394 | S236 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 0.53 | S272 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 0.000 | S329 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 1.000 | S332 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 14.6 | S341 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 15.6 | S341 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 19.8 | S341 | SI caption, corpus session; Block C v2 off-site census (12_g4_off_site_census) -- interval bound, not separately recomputed here |
| 25.6 | S342 | the RETRACTED Block C v1 pooled off-site figure; superseded by the v2 census (15.1% apo / 20.3% cognate). Block C verify_claims check C06 asserts it does NOT reproduce, which is the check working -- it is quoted here only as the retraction it is |
| 0.340 | S361 | DERIVED, not shipped: stage3_2x2_ligand_state_specificity.json per_backbone.boltz, (0.7680-0.9762)-(0.8983-0.7665) = -0.3400, against interaction.estimate -0.3062. The agonist cells carry n_clusters 28 and the antagonist cells 23; the interaction is on the 23 in common, which is why the cell means cannot reconstruct it |
| 27.9 | S364 | Block C G4 gate, agonist off-site fraction lower bound; independent re-verification 2026-09-10, not recomputed here |
| 34.9 | S364 | Block C G4 gate, agonist off-site fraction upper bound; same source |
| 0.43 | R215 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.42 | R215 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.01 | R218 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.334 | R293 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 45 | R294 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.333 | R295 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.242 | R295 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.432 | R295 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.333 | R300 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.733 | R300 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.179 | R307 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.320 | R307 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 0.127 | R313 | Block A/B cluster-boot over 24 clusters, recomputed 2026-09-10 |
| 100 | R468 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 91.8 | R470 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 0.2 | R470 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 100 | R485 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 112 | R491 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 6.6 | R496 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 100 | R498 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 96 | R508 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 100 | R509 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 58 | R510 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 100 | R514 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 82 | R514 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 100 | R515 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 76 | R520 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 125 | R522 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 4.21 | R542 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 11.16 | R542 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 12.88 | R543 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 1.68 | R549 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 2.69 | R550 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 0.81 | R550 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 0.82 | R550 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 2.38 | R550 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 2.73 | R551 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 4.37 | R551 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 1.15 | R551 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 2.96 | R551 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 4.68 | R552 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 1.58 | R552 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 8.7 | R560 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 20.9 | R561 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 8.7 | R561 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 1.25 | R572 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 10.93 | R573 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 3.40 | R574 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 11.19 | R574 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 16.78 | R574 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 0.76 | R575 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 1.24 | R575 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 38.8 | R600 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 10.0 | R601 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 42,180 | R611 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 25,810 | M461 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 128 | M462 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 4096 | M476 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |
| 42,180 | M496 | Block D claim sheet / Part A -- PROSE-ONLY, no row table shipped (D-D-1) |


| 84 | F47 | exclusion-sweep points; sweep table not shipped at row level |
| 1.1 | S114 | the widening factor PREVIOUSLY assumed, quoted as superseded by 2.2 |
| 77 | S194 | reference rows drawn in the S-T8 panel; not recomputed here |
| 512 | S194 | prediction rows drawn in the S-T8 panel; not recomputed here |
| 159.95 | M61 | Class B kink-angle threshold | 159.95$^\circ$; for the 4 class~F receptors, where neither substitution is |
| 13 | M165 | 29 clusters - 16 singletons; data/block_a/07_clusters_and_holdout/cluster_map.csv | acts on 13 and 12 multi-member clusters respectively. All confidence intervals |
| 354 | M283 | UniProt P63096 sequence length, recomputed by analysis/verify_partner_chains.py | the $\alpha$5 C-terminal 21 residues.} G$\alpha_{\mathrm{i}}$1 is 354 residues, |
| 334 | M284 | 354 - 21 + 1, the first residue of the $\alpha$5-CT; analysis/verify_partner_chains.py ALPHA5_CT_LEN | so the segment the title concerns is 334--354, and every substitution we found |
| 354 | M284 | UniProt P63096 sequence length, last residue of the $\alpha$5-CT | so the segment the title concerns is 334--354, and every substitution we found |
| 380 | M10 | backbones, giving 380 receptor $\times$ backbone $\times$ arm cells and 9,490 |
| 98 | M20 | data.]} The reference set comprises \textbf{[PI: 98 empirical / 89 as |
| 89 | M20 | data.]} The reference set comprises \textbf{[PI: 98 empirical / 89 as |
| 44 | M21 | previously stated]} unique Protein Data Bank entries across the panel --- 44 in |
| 1,351 | M107 | an unsupervised geometric index over 1,351 class~A structures recovers |
| 46 | M116 | 2$\times$46 and 6$\times$37 and hydroxyl positions at Ballesteros--Weinstein |
| 37 | M116 | 2$\times$46 and 6$\times$37 and hydroxyl positions at Ballesteros--Weinstein |
| 0.1.0 | M150 | frozen scorer (version 0.1.0, commit  ) recorded per row. |
| 1,000 | M154 | The cluster bootstrap is authoritative: 1,000 resamples over 26 paralog |
| 20260909 | M155 | clusters, seed 20260909. A receptor-level bootstrap is reported as secondary, in |
| 42 | M159 | Eleven of the 26 clusters are singletons (42\%), so the paralogy correction acts |
| 2.4 | M169 | removes model-side atom clashes with   below 2.4~\AA. These |
| 29 | M170 | two together remove 29 rows (0.31\%) and are applied everywhere. |
| 0.31 | M170 | two together remove 29 rows (0.31\%) and are applied everywhere. |
| 4,890 | M172 | E3 (4,890 rows) flags receptors whose reference fails its own predicate on a |
| 4,690 | M174 | (4,690 rows, 24 receptors) or   (2,000 rows, 10 |
| 2,000 | M174 | (4,690 rows, 24 receptors) or   (2,000 rows, 10 |
| 2,295 | M178 | (2,295 rows) have no measurable value because the axis is undefined for them |
| 2,395 | M180 | not exist --- while a further 12 receptors (2,395 rows) have a measurable |
| 1,495 | M187 | E4 (1,495 rows) restricts to Class~A; Class~B and~F are reported separately as |
| 1,600 | M200 | 1,600 rows and 32 receptors per backbone. |
| 43 | M209 | substantial: of the 43 panel active-state references carrying a deposition date, |
| 35 | M210 | \textbf{35 (81\%) predate the Boltz-2 structural cutoff of 2023-06-01}, 19 |
| 81 | M210 | \textbf{35 (81\%) predate the Boltz-2 structural cutoff of 2023-06-01}, 19 |
| 06 | M210 | \textbf{35 (81\%) predate the Boltz-2 structural cutoff of 2023-06-01}, 19 |
| 01 | M210 | \textbf{35 (81\%) predate the Boltz-2 structural cutoff of 2023-06-01}, 19 |
| 09 | M211 | (44\%) predate Protenix2's 2021-09-30, and 15 (35\%) predate Chai-1's |
| 30 | M211 | (44\%) predate Protenix2's 2021-09-30, and 15 (35\%) predate Chai-1's |
| 1.000000 | M234 | implementations and agree bit-exactly (Pearson $r = 1.000000$). The predicate |
| 96.3 | M237 | independently: the TM6 helicity anchor holds on 96.3\% of rows. |
| 162 | M251 | is \textbf{[PI: 162 empirical / 127 as previously stated]}. Several references |
| 127 | M251 | is \textbf{[PI: 162 empirical / 127 as previously stated]}. Several references |
| 9.5 | M277 | Hamming distance of 9.5, and each shuffled donor is checked against the |
| 0.90 | M305 | independent evidence. Receptor-level intervals are 0.90--1.26$\times$ the width |
| 1.26 | M305 | independent evidence. Receptor-level intervals are 0.90--1.26$\times$ the width |
| 5,000 | M365 | spanning those 23 receptors, 5,000 resamples, seed 1234. Receptor-level |
| 1234 | M365 | spanning those 23 receptors, 5,000 resamples, seed 1234. Receptor-level |
| 167 | R12 | rows --- 167 unique PDB entries, one of which is scored twice because it serves |
| 159 | R14 | on 159 and deviated on nine, five annotated active and four annotated inactive. |
| 111 | R48 | than a graded shift: 111 of 160 apo cells never fire the predicate on any of 25 |
| 108 | R49 | seeds, while 108 of 159 cognate cells fire on all 25. The distributions behind |
| 95 | R54 | $+5.04$~\AA{} (Boltz-2, 95\% CI $[3.53, 5.55]$), |
| 3.53 | R54 | $+5.04$~\AA{} (Boltz-2, 95\% CI $[3.53, 5.55]$), |
| 5.55 | R54 | $+5.04$~\AA{} (Boltz-2, 95\% CI $[3.53, 5.55]$), |
| 0.36 | R55 | $+1.05$~\AA{} (Chai-1, $[0.36, 3.76]$), |
| 3.76 | R55 | $+1.05$~\AA{} (Chai-1, $[0.36, 3.76]$), |
| 3.95 | R56 | $+4.81$~\AA{} (OpenFold3, $[3.95, 5.21]$) and |
| 5.21 | R56 | $+4.81$~\AA{} (OpenFold3, $[3.95, 5.21]$) and |
| 4.63 | R57 | $+5.31$~\AA{} (Protenix2, $[4.63, 5.74]$). |
| 5.74 | R57 | $+5.31$~\AA{} (Protenix2, $[4.63, 5.74]$). |
| 83.4 | R58 | Pooled row-level predicate-active rates move from 16.0\% to 83.4\% (Boltz-2), |
| 32.7 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 75.0 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 24.2 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 79.9 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 14.5 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 87.1 | R59 | 32.7\% to 75.0\% (Chai-1), 24.2\% to 79.9\% (OpenFold3) and 14.5\% to 87.1\% |
| 2.2 | R61 | are the authoritative ones; the cluster interval is up to $2.2\times$ wider than |
| 63 | R67 | showed on 63 post-cutoff Class~A receptor--G$_s$ |
| 6302 | R69 | template-biased alternatives (p.~6302), and attribute the gain to co-folding |
| 6305 | R70 | rather than to training-set composition (p.~6305); |
| 129 | R82 | Relatedly, 129 of the 145 references in   are |
| 145 | R82 | Relatedly, 129 of the 145 references in   are |
| 6299 | R98 | as ``a baseline'' for newer models (p.~6299); this is that evaluation. |
| 9,490 | R100 | Fourth, **the evidence is distributional rather than a point estimate**: 9,490 |
| 31 | R102 | means with standard deviations over 31 families. |
| 98.2 | R128 | docked rather than merely present: 98.2\% of samples meet the interface-contact |
| 66 | R129 | criterion, with a median of 66 receptor--G$\alpha$ contacts. |
| 256 | R139 | active, 204 of 256 (79.7\%) fall below the reference-inactive median on the |
| 79.7 | R139 | active, 204 of 256 (79.7\%) fall below the reference-inactive median on the |
| 205 | R140 | connector; of predictions it called inactive, 205 of 256 (80.1\%) fall above the |
| 80.1 | R140 | connector; of predictions it called inactive, 205 of 256 (80.1\%) fall above the |
| 1.51 | R145 | delta $-0.56$~\AA{} against a reference delta of $-1.51$~\AA). The interval on |
| 1.20 | R146 | that delta, $[-1.20, +0.03]$, includes zero, as do all four per-backbone |
| 0.03 | R146 | that delta, $[-1.20, +0.03]$, includes zero, as do all four per-backbone |
| 0.37 | R162 | slopes of 0.04 (Boltz-2), 0.37 (Chai-1), 0.18 (OpenFold3) and 0.26 (Protenix2) |
| 0.18 | R162 | slopes of 0.04 (Boltz-2), 0.37 (Chai-1), 0.18 (OpenFold3) and 0.26 (Protenix2) |
| 0.26 | R162 | slopes of 0.04 (Boltz-2), 0.37 (Chai-1), 0.18 (OpenFold3) and 0.26 (Protenix2) |
| 0.07 | R164 | amplitude reproduction. Protenix2's interval, $[0.07, 0.55]$, excludes zero: a |
| 0.55 | R164 | amplitude reproduction. Protenix2's interval, $[0.07, 0.55]$, excludes zero: a |
| 0.30 | R172 | slopes are negative (Boltz-2 $-0.30$, Chai-1 $-0.66$). A negative slope is not |
| 0.63 | R195 | Chai-1; $-0.26$ (signed) against $-0.63$ (signed) for OpenFold3; and $+0.33$ |
| 0.33 | R195 | Chai-1; $-0.26$ (signed) against $-0.63$ (signed) for OpenFold3; and $+0.33$ |
| 0.49 | R207 | useful decision metric'' for \emph{ligand pose} ($R^2 = 0.49$); their |
| 0.046 | R208 | pLDDT-against-receptor-C$\alpha$ result, $R^2 = 0.046$, is the same null we |
| 32,000 | R229 | samples --- 32,000 predictions, every one of the 640 receptor $\times$ arm |
| 339 | R235 | parent over the first 339--349 residues, verified by sequence hash on 40 of 40 |
| 349 | R235 | parent over the first 339--349 residues, verified by sequence hash on 40 of 40 |
| 0.081 | R243 | monotonically across those four arms: 0.158 [0.081, 0.256] apo, 0.558 |
| 0.256 | R243 | monotonically across those four arms: 0.158 [0.081, 0.256] apo, 0.558 |
| 0.445 | R244 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.664 | R244 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.747 | R244 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.869 | R244 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 0.838 | R244 | [0.445, 0.664] decoy, 0.809 [0.747, 0.869] shuffled, 0.891 [0.838, 0.942] |
| 1.06 | R256 | \emph{less} mass than the shuffled arm on three of four backbones (1.06\% |
| 3.33 | R257 | against 3.33\% on Boltz-2, 0.39\% against 1.89\% on OpenFold3, 0.00\% against |
| 0.39 | R257 | against 3.33\% on Boltz-2, 0.39\% against 1.89\% on OpenFold3, 0.00\% against |
| 1.89 | R257 | against 3.33\% on Boltz-2, 0.39\% against 1.89\% on OpenFold3, 0.00\% against |
| 1.83 | R258 | 0.06\% on Protenix2). Chai-1 inverts, at 1.83\% against 0.56\%, and that |
| 33 | R259 | inversion is one receptor: 33 of OX2R's 50 Chai-1 cognate rows fall in the band, |
| 9.0 | R261 | lives in the far-inactive tail instead --- 9.0\% of shuffled rows sit more than |
| 4.1 | R262 | 2~\AA{} below the threshold against 4.1\% of cognate rows --- which is a shift |
| 0.328 | R267 | [0.328, 0.464] of the total rise, 55\%. Restoring a real $\alpha$5-CT sequence |
| 0.464 | R267 | [0.328, 0.464] of the total rise, 55\%. Restoring a real $\alpha$5-CT sequence |
| 0.188 | R268 | adds $+0.252$ [0.188, 0.321], 34\%. Getting the family \emph{right} adds |
| 0.321 | R268 | adds $+0.252$ [0.188, 0.321], 34\%. Getting the family \emph{right} adds |
| 0.047 | R269 | $+0.082$ [0.047, 0.125]. On the probability scale that last term is 11\% of the |
| 0.125 | R269 | $+0.082$ [0.047, 0.125]. On the probability scale that last term is 11\% of the |
| 1.09 | R270 | total; on the logit scale it is 17.4\% [0.39, 1.09], and both are correct. The |
| 0.98 | R272 | above 0.98 in 24--34 of 40 cells per backbone, and a probability-scale |
| 0.46 | R280 | ([$+0.46$, $+1.63$]); the other three span it. The panel term signs because the |
| 1.63 | R280 | ([$+0.46$, $+1.63$]); the other three span it. The panel term signs because the |
| 1,699 | R295 | populated on every backbone, 1,699 rows pooled and 278--540 per backbone |
| 278 | R295 | populated on every backbone, 1,699 rows pooled and 278--540 per backbone |
| 540 | R295 | populated on every backbone, 1,699 rows pooled and 278--540 per backbone |
| 0.29 | R311 | [$-0.29$, $+0.30$] across 24 receptors, and $-0.062$~\AA{} [$-0.41$, $+0.21$] |
| 2.79 | R332 | receptors with an interval of [$-2.79$, $+0.14$], and |
| 0.14 | R332 | receptors with an interval of [$-2.79$, $+0.14$], and |
| 1.62 | R339 | survive: its pocket-C$\alpha$ separation of 1.62~\AA{} ranks 34th of 40, in the |
| 65 | R355 | apo arm and ceiling-pinned in the cognate arm, leaving roughly 65\% of |
| 0.306 | R365 | backbones: $-0.306$~\AA{} on Boltz-2 [$-0.454$, $-0.164$], $-0.137$ on Chai-1 |
| 0.137 | R365 | backbones: $-0.306$~\AA{} on Boltz-2 [$-0.454$, $-0.164$], $-0.137$ on Chai-1 |
| 0.184 | R366 | [$-0.216$, $-0.045$], $-0.252$ on OpenFold3 [$-0.405$, $-0.099$] and $-0.184$ |
| 87 | R379 | positive and significant Kendall's $\tau$ on \textbf{65--87\% of receptors} --- |
| 0.20 | R383 | median $\tau$ 0.20--0.45. Because its threshold was fixed in advance, this test |
| 0.852 | R389 | curve of 0.852 on Boltz-2 and 0.825 on Protenix2, with cluster-bootstrap |
| 0.825 | R389 | curve of 0.852 on Boltz-2 and 0.825 on Protenix2, with cluster-bootstrap |
| 0.560 | R390 | intervals of [0.560, 0.974] and [0.528, 0.960] that exclude both chance and a |
| 0.974 | R390 | intervals of [0.560, 0.974] and [0.528, 0.960] that exclude both chance and a |
| 0.528 | R390 | intervals of [0.560, 0.974] and [0.528, 0.960] that exclude both chance and a |
| 0.960 | R390 | intervals of [0.560, 0.974] and [0.528, 0.960] that exclude both chance and a |
| 0.706 | R391 | permutation null. On Chai-1 (0.706) and OpenFold3 (0.656) the same intervals |
| 0.351 | R392 | reach 0.351 and 0.382. \textbf{Those two backbones are inconclusive, not |
| 0.382 | R392 | reach 0.351 and 0.382. \textbf{Those two backbones are inconclusive, not |
| 6.93 | R420 | 6.93\% of predictions place the ligand within 3~\AA{} of its reference pose on |
| 56 | R422 | bimodal --- median dock rates of 54--56\% on Boltz-2 against 0--18\% on Chai-1 |
| 40,000 | R427 | across all 40,000 predictions: 15.1\% of apo-arm and 20.3\% of cognate-arm |
