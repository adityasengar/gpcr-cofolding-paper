# Independent re-verification of Blocks A, B and C — consolidated

Three adversarial agents, run 2026-09-10, each recomputing from the tidy files with pandas and
reusing nothing from `verify_claims.py`. Read-only on `data/` and `analysis/`; all output written
here. Block D was deliberately **excluded** — `paper-6f` was mid-intake on it and a read there
would have collided.

| block | BLOCKING | MATERIAL | MINOR | verdict on the data itself |
|---|---|---|---|---|
| A | 5 | — | — | **excellent.** 79/80 MANIFEST sha256 match; every aggregate rebuilt bit-exactly |
| B | 8 | 13 | 14 | **excellent.** 103/103 sha256; ladder, decomposition, all 30 CIs, 2×2, connector all reproduce |
| C | **6** | 12 | 16 | reproduces where checkable; the G4 census reproduced to 15 decimal places |

**The single most important line in all three reports: every defect found is claim-side, not
data-side.** The drops are sound. What is wrong is what was written about them.

## The four findings that change the paper

**1. No block supplies a peptide — now proven, not inferred.** The Block B agent verified it two
independent ways: `n_partner_aa` across 640 cells, and by extracting chain B out of the shipped
ladder-arm CIFs (decoy = 359 aa Gαq with a permuted tail; shuffled = 394 aa Gαs, a different
protein). The string "21-mer" appears in **no markdown file in the drop.** Block B is the same
co-input type as Block A. This is what `intro.tex` was corrected for.

**2. The decomposition term named "α5-CT sequence" is not an α5-CT contrast.**
`delta_a5ct_sequence_decoy_to_shuffled` is credited with 34.3% of the ladder, and it swaps ~349 of
359 residues plus length, family and the partner's whole MSA. That is the confound this project
criticises `ye2026multistatebias`, `zhang2026generalization` and `chiesa2025templatebias` for, in
our own voice.

**And the fix is already in the drop.** `decoy → cognate` is a clean α5-CT-only contrast —
identical scaffold, identical length, identical family, only the 11-residue tail differs —
bootstrapped at **+0.333, 95% CI [+0.244, +0.435], signed.** It should be the headline term.

**3. The pLDDT result is an arm-pooling artifact.** Pooling apo and cognate while scoring both
against `rmsd_to_active_ref` — the wrong target for apo rows. Arm-centred, OF3's −0.626 collapses
to −0.079 and Boltz's −0.221 **reverses** to +0.123; within apo alone the correlation is positive
on all four backbones. Scored against arm-appropriate references: −0.14 / −0.30 / −0.42 / −0.34,
all four negative and consistent.

This does **not** overturn "confidence does not track state correctness" — it overturns the
*backbone split*. The honest version is simpler and stronger: one direction, four backbones, no
outlier.

**4. A pre-specified gate fired and its remedy was skipped — the most serious single finding.**
`BLOCK_C_GATING_REPORT.md` §G4 says in advance: *"If off-site fraction is material (≥5% per backbone
per class), restate G1 and G2 on the on-site subset before Part B."* It fires on **8 of 12 cells** —
agonist off-site is 27.9–34.9% on every backbone. G1 and G2 were never restated. The README
adjudicates "not material" from a **1.52%** figure computed on a small-molecule-only subset that
excludes the peptide-agonist rows the claim actually runs on. The gating report itself ends *"Gate
NOT clear… awaiting adjudication"*, and no adjudication record shipped.

**5. The drop retracts a claim its own sheet revalidates.** `T7C_POST_FIX_HEADLINE.md`: *"The
manuscript's scoped '6.93%' is now revealed as an artifact of pooling across a bimodal per-receptor
distribution."* `SC-C-7` calls the same number *"revalidated in this pass."* They shipped together.
The number is also cited to the pre-fix scorer that Flag C-7 forbids for pose.

**6. Two claim sheets publish intervals their own rules forbid.** Block C's SC-C-5 labels a CI
"receptor-boot over 15 receptors" and it reproduces as a **row** bootstrap over 60 points; a genuine
receptor bootstrap gives **[−0.850, +0.047], spanning zero** — while `SC-C-8` in the same sheet
says outright *"Row-boot is invalid."* Block B's `claim_answers.csv` ships retired row-boot CIs with
**all 101 rows flagged `True`**, including ones the agent falsified.

## Effect on the six-figure allocation

| figure | status |
|---|---|
| 1 — schematic + predicate + calibration | **unaffected** |
| 2 — main effect, four backbones | **unaffected** |
| 3 — the ladder | hold: the headline term should become `decoy → cognate` |
| 4 — decomposition | hold: family term unsigned on 3 of 4 backbones; shares misreported |
| 5 — the negatives | hold: restate the confidence result without the backbone split |
| 6 — Block C 2×2 + ordinal recovery | hold: "apo arm alone" is false by a factor of two |

**The allocation is not withdrawn.** None of these says a result is absent; they say the stated
term, scope or interval is wrong, and in Block B's case a better term already exists in the data.
Figures 1 and 2 can be built now. Figures 3–6 wait on restatement — which is cheaper than redrawing
them afterwards, and is the whole reason the dependency was flagged before any panel was made.

## Caveat that applies to all three reports

Each agent was told **not** to read the corresponding `DISCREPANCY_REPORT.md`, so its findings are
genuinely independent — and therefore **some will duplicate discrepancies already recorded.**
Cross-check before treating any single item as new. Block A's N-4 is the instructive case: it
reports that a *recorded* discrepancy (D-A-24) is itself wrong.

Each report also carries an explicit "what I could not check" section. Block A's most important
entry: **zero receptor-bootstrap draws ship**, which is what SC-1 and SC-11 actually quote.

## Three things that cleared, and are worth stating

The re-verification was adversarial by design, so what it *failed* to break matters:

- **Block C's LORO split is genuinely by receptor.** The agent was briefed to suspect a
  structure-level leak and cleared it — AUROC 0.000 on a held-out receptor is impossible under a
  structure split. The residual concern is subtler: paralogs are split across folds while the
  interval treats the paralog cluster as the independent unit (AA1R/AA2AR score exactly 1.000).
- **Block C's 2×2 interaction term was properly estimated and bootstrapped.** Only the four cell
  means shipped beside it fail — they are on different receptor sets.
- **Every number in the manuscript's own self-critical off-site paragraph reproduced** — 18.92 /
  35.85 / 2.00%, ρ = −0.241, medians 0.282 vs 0.386. Where the paper argued against itself, it was
  right.

Two findings share one disease across blocks, and it is the `hides` field made flesh: Block B's
tilt axis is non-monotonic (shuffled opens TM6 *further* than cognate on all four backbones) and
Block C's "65%" ordinal headline conceals that **Chai has 5 of 23 receptors running significantly
backwards.** Both are fixed the same way — report the sign, as `yu2026domainmotion` does.

## One relayed finding did NOT hold — recorded because the error is instructive

**Block C's "pose reversal" (C-BLOCKING-4) does not stand as stated.** The agent compared
`t7b_pose_accuracy.json`'s **pooled cell rates** against the manuscript's "54–56%", which the drop's
own Flag defines as a **per-receptor median** on the sibling corpus `rescore_t7c_full/rows.csv` —
which does not ship. Different statistics, different corpora; the comparison is not valid, and I
relayed it as "a straight reversal in live results.tex" without checking that the two numbers were
the same kind of number.

A real tension survives underneath it: the "0–18% on Chai / 0% on the other two" half traces only
to `T7C_POST_FIX_HEADLINE.md` and the claim sheet, and the shipped `t7b` JSON does put **Chai
highest at 0.421 / 0.358** with OF3 and Protenix at 6–8% rather than 0. But it cannot be settled
without the sibling corpus, which is Block C ask 1.

**The error class is worth naming because it recurred three times in one day across two sessions** —
comparing a value against a statistic of a different kind. It produced D-A-4, then D-A-24, then
this. The check is cheap: before comparing two numbers, confirm they are the same statistic on the
same corpus. See [[verification-must-be-self-tested]].

## Block A N-4, resolved by the orchestrator, and it is sharper than the agent could see

The agent was right to recommend withdrawing D-A-24. The orchestrator rebuilt the predicate with the
Class-A two-axis rule and applied it to every row:

| class | shipped | recomputed | |
|---|---|---|---|
| A | 3,742 | 3,742 | **zero disagreements** |
| B | 607 | 0 | rule does not govern — Class B substitutes a kink angle |
| F | 517 | 0 | rule does not govern — Class F uses tilt alone |

3,742 + 607 + 517 = 4,866. **On the class the rule governs, the recomputation is perfect.** The
entire apparent discrepancy was a class-conditional rule applied across classes — which our own
Methods documents. Two new checks now pin it rather than leaving it to memory.
