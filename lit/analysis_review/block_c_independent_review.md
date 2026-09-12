# Block C — independent adversarial verification

**Scope**: `data/block_c/` and `analysis/block_c/`, both read-only. Nothing was
fixed; nothing outside `lit/analysis_review/` was written; no git was run.
**Method**: recomputation from shipped row-level data where it exists; arithmetic
reconciliation against the design grid where it does not.
**Date**: 2026-09-10.

> **Concurrency note.** While this review was being written, another session was
> active in the same working tree: `analysis/block_c/verify_claims_results.json`
> was rewritten at 20:15, and `manuscript/`, `CLAIMS.md` and `refs.bib` were
> rebuilt. Nothing in `data/block_c/` changed (it is `chmod a-w`), so every
> recomputation below stands. But the quotations from
> `manuscript/sections/results.tex` and the comparisons against
> `analysis/block_c/` are a snapshot taken before 20:15 and may already be
> stale. Re-check those line references before acting on them.

**Relationship to the existing check.** `analysis/block_c/DISCREPANCY_REPORT.md`
already records **D-C-1** (most of Block C is not recomputable), **D-C-2** (66
named files absent) and **D-C-3** (SC-C-2's τ mislabel), and
`OPEN_QUESTIONS.md` Q3 records the Flag C-12 / C-C-3 conflict. Those are not
re-reported as new. This pass asks what a *second* checker finds once those are
known. It finds twenty-three further items: **six blocking**, twelve material.

---

## The two findings that matter most

### 1. A surviving claim rests on a withdrawn tier

The brief asked whether anything downstream still depends on a withdrawn claim.
It does — and it is the claim the sheet itself calls *"arguably load-bearing
beyond the 2×2 finding."*

`W-C-9` retires Tier 1 without qualification: *"**Also retires**: the entire
Tier 1 headline set. Manuscript's Results rests on Tier 3."* Flag C-9 repeats it.
`BLOCK_C_STATE_CHECK.md` repeats it: *"Live Block C claims rest on Tier 3
alone."*

`SC-C-2` does not. Its claim sentence reads *"Recovery holds on **Tier 1**
(5-class, all 4 backbones at 75%) and Tier 3 (…)"*, and its numbers table carries
a Tier 1 row. Tier 1 is the **only** panel that meets the threshold on all four
backbones — Tier 3 × 23 is 74/65/74/87 and Tier 3 × 15 is 67/67/67/87, so 3 of
those 8 cells reach 75 %. `SIGNAL_RECOVERY_REPORT.md` L129 makes the dependence
explicit: *"**Tier 1 hits 75 % on all 4 backbones — meeting the pre-registered
≥ 6/8 threshold.**"*

Worse, the four identical 75 % values on an 8-receptor pilot are the same
signature W-C-9 retracted Tier 1 for: *"when every cell is ceiling-pinned at 1.0
or floor-pinned at 0.0, the bootstrap has no variance to sample."*

And the threshold itself cannot be located. `PREREG_SIGNAL_RECOVERY.md` — the
shipped pre-registration — contains **zero** occurrences of "P4", "ordinal",
"Kendall", "τ", "6/8" or "Tier 1", and scopes itself to *"Block C v5 landed data
only … No new predictions."* Its kill criteria are KILL-S1, KILL-S3, KILL-S4
only. "W-C-9" appears nowhere in `SIGNAL_RECOVERY_REPORT.md`.

**Manuscript exposure**: `manuscript/sections/results.tex` L379–386 correctly
drops the Tier 1 row and reports only the 23- and 15-receptor panels. But it
retains *"Because its threshold was fixed in advance, this test carries
evidential weight the 2×2 does not: it could have failed."* On the two panels it
actually reports, the fixed threshold is **not met on 5 of 8 cells**. The
evidential-weight sentence stands on the withdrawn panel while citing the
surviving ones.

### 2. Three hard-stop gates were triggered, one pre-specified remedy was skipped, and no adjudication record shipped

`BLOCK_C_GATING_REPORT.md` closes: *"**Gate NOT clear.** Three of the five
section-4 stop conditions are met"* (G1, G2, G3), and *"**Not proceeding to Part
B (release commit) or Part C (writing bundle) in this run.** Status: awaiting
adjudication."* `G2_REFERENCE_HOMOGENEITY.md`, written the same day, still says
*"**Held state**: BLOCK_C_CLOSEOUT Parts B/C remain held. AGTR1 diagnostic
remains recorded but not adjudicated."*

The claim sheet nevertheless presents *"Summary: 10 surviving claims"*, and
SC-C-4 and SC-C-5 are each headed *"(adjudicated from the G1 gating result)"* /
*"(adjudicated from G2 + …)"* — without naming who adjudicated, when, or on what
grounds. **No adjudication record is in the bundle.** Gate G1's stop condition
is quoted verbatim as *"Boltz's `~0.85` figure does not survive receptor-boot
(lower bound 0.64)"* — and 0.852 is the manuscript headline.

The G4 gate is the sharper case, because it is a **pre-specified conditional
remedy that the data then triggered and nobody executed**. Gating report,
§G4 design step 8:

> *"If off-site fraction is material (dispatch heuristic: **≥ 5 % per backbone
> per class**), **restate G1 and G2 on the on-site subset before Part B**."*

The census subsequently ran. Recomputed from the shipped 40,000 rows, the
trigger fires on **8 of the 12 (backbone × class) cells** — Boltz agonist 30.8 %,
Chai decoy 37.6 %, Chai agonist 34.9 %, OF3 agonist 27.9 %, Protenix agonist
29.5 %, Chai antagonist 11.8 %, Boltz decoy 16.8 %, OF3 decoy 8.0 %. **G1 and G2
were never restated on the on-site subset**; no such file exists in the bundle,
and the bundle `README` instead adjudicates *"Not material for SC-C-1"* from the
**1.52 %** small-molecule-only figure — a subset that excludes the 3,000
peptide-agonist rows SC-C-1 actually runs on.

The bin definitions also moved between design and execution: the gate designed
`{<5 inside | 5–10 near | 10–15 margin | ≥15 off-site}`; the delivered census
used `{<8 in-pocket | 8–15 entrance-bound = VALID | ≥15 off-site}`. Pooled, the
fraction beyond the pocket is 17.73 % at ≥ 15 Å but **36.10 % at ≥ 8 Å**.

`manuscript/sections/results.tex` already carries the honest version of half of
this (the 18.92 % / 35.85 % / 2.00 % paragraph, which reproduces exactly). What
it does not carry is that a pre-registered gate said to redo G1 and G2 on the
on-site subset, and that this was not done.

---

## Findings

**BLOCKING** = a number or scope statement in the manuscript or claim sheet is
wrong or unsupported as written. **MATERIAL** = the number is right but the
method, denominator or label misrepresents it. **MINOR** = internal inconsistency
with no manuscript consequence today.

| # | Sev | File + field | Claimed | Recomputed / found | Reproduce |
|---|---|---|---|---|---|
| 1 | **BLOCKING** | `01_claims/BLOCK_C_CLAIM_SHEET.md` SC-C-2; `11_manuscript_narrative/SIGNAL_RECOVERY_REPORT.md` L127–129, L229, L252 | "pre-registered P4 … ≥ 6/8 cells reach the pre-registered threshold"; Tier 1 row 75/75/75/75 | Threshold met on all four backbones **only on Tier 1**, retired in full by W-C-9. No P4 threshold exists in the shipped prereg. Tier 3 × 23 = 74/65/74/87; Tier 3 × 15 = 67/67/67/87 → 3 of 8 cells at ≥ 75 % | `grep -ciE 'P4\|ordinal\|kendall\|6/8\|Tier 1' data/block_c/11_manuscript_narrative/PREREG_SIGNAL_RECOVERY.md` → 0 |
| 2 | **BLOCKING** | `11_manuscript_narrative/BLOCK_C_GATING_REPORT.md` §G4 step 8 vs `12_g4_off_site_census/` | README: "Not material for SC-C-1" | The pre-specified trigger (≥ 5 % off-site per backbone per class) **fires on 8 of 12 cells**. The mandated remedy — restate G1 and G2 on the on-site subset — was never run. The "not material" adjudication is computed on a small-molecule-only subset (1.52 %) that excludes the peptide-agonist rows SC-C-1 runs on (16.76 % on all apo agonist+antagonist rows; 18.92 % on SC-C-1's own 23 receptors) | block R2 below |
| 3 | **BLOCKING** | `05_ref_separation/g2_refsep_vs_auroc.json` `pooled_regression.bootstrap.slope_ci_95`; SC-C-5 labels it *"receptor-boot CI over 15 receptors, 1000 iterations"* | full-15 slope −0.325, 95 % CI **[−0.570, −0.068]**, excludes zero | The published interval reproduces a **row bootstrap over the 60 (receptor × backbone) points** — my row-boot = [−0.570, −0.078]. A genuine **receptor** bootstrap gives **[−0.850, +0.047] — spans zero**. `SC-C-8`: *"Row-boot is invalid."* The gating report itself concedes the defect: *"Block C's audit reports currently mix receptor-boot and (in one case) **row-boot** labels."* The excl-AGTR1 case agrees under both schemes, which is why it was never caught | block R3 |
| 4 | **BLOCKING** | `06_2x2_interaction/stage3_2x2_ligand_state_specificity.json` `per_backbone.*.n_rows`; scope *"in the apo arm alone"* (claim sheet, `results.tex` L373) | agonist cells 2,800 rows on 28 receptors; antagonist cells 2,300 on 23, described as apo-only | The grid is **50 rows per (receptor × backbone × role × arm)** — verified exactly, 800 cells × 50 = 40,000. Apo-only would be 28 × 50 = **1,400** and 23 × 50 = **1,150**. The shipped counts are exactly **28 × 100** and **23 × 100** — i.e. both arms. `g_scc1_cluster_boot.json` reproduces the point estimates to 15 significant figures, so the cluster-boot recompute inherited the same filter | `python3 -c "import csv,collections;r=list(csv.DictReader(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv')));print(collections.Counter(collections.Counter((x['receptor'],x['backbone'],x['role'],x['arm']) for x in r).values()))"` → `{50: 800}` |
| 5 | **BLOCKING** | `10_pose_accuracy/task_E_v3_scoped_finding.json` `reconstruction.inputs.rows_csv` vs claim sheet + Flag C-7 | *"All pose-accuracy statements below cite this corpus"* (the sibling `rescore_t7c_full/rows.csv`, scorer `d9c646af…`); Flag C-7: *"Do not conflate."* | The 6.93 % / 312 / 4,500 figures come from **`rows.tier3.v2.csv`, SHA `5ccf58ac…`** — the **primary** corpus, scorer `3d9c6fa…`, generated **2026-09-05**, i.e. before the MCS + Bug #2 fixes. The block's flagship pose number is cited to the one corpus its own rule forbids for pose numbers. `T7C_POST_FIX_HEADLINE.md` cites a third scorer SHA in prose, `891041e8…` | `python3 -c "import json;print(json.load(open('data/block_c/10_pose_accuracy/task_E_v3_scoped_finding.json'))['reconstruction']['inputs']['rows_csv'])"` |
| 6 | **BLOCKING** | `10_pose_accuracy/T7C_POST_FIX_HEADLINE.md` L72 vs SC-C-7 | SC-C-7: *"**Claim** (unchanged in scope from manuscript v1, **revalidated in this pass**)"* … 6.93 % | The file that supersedes it says, verbatim: *"The manuscript's scoped '6.93 %' is now revealed as an **artifact of pooling across a bimodal per-receptor distribution**."* That is the same defect W-C-3 retracted. The claim sheet never surfaces its own source's verdict on its own headline | `sed -n '70,74p' data/block_c/10_pose_accuracy/T7C_POST_FIX_HEADLINE.md` |
| 7 | **MATERIAL** | `08_confidence_signal/s3_consensus_confidence.json` `s3c_accuracy_vs_coverage`; SC-C-3 reports **only** top-25 % | "Consensus outperforms pLDDT on 3/4 backbones" | 25 % is one of five shipped coverage levels and the only one where consensus wins on all four. **At top-10 % pLDDT beats consensus on every backbone by a wide margin**: 0.990 vs 0.791 (boltz), 0.918 vs 0.764 (chai), 0.932 vs 0.766 (of3), 0.821 vs 0.766 (protenix). At 100 % the two are identical by construction. KILL-S3 was pre-registered with **no coverage level** and a different endpoint (*"predicts distance-to-crystal"*; *"paired Δ AUROC ≤ 0, **CI clears zero**"*); the CI requirement was dropped, no CI is reported for S3 anywhere, and the top-25 % choice is not among the report's three declared deviations | block R4 |
| 8 | **MATERIAL** | same file, `s3b_spearman_consensus_vs_pca_active` | consensus "acts as a per-prediction confidence signal" | Spearman between consensus and the accuracy it is meant to signal is **≈ 0 on every backbone**: +0.018, −0.057, +0.065, +0.022 (pLDDT: +0.076, −0.083, −0.137, −0.070). The direct test of "does this confidence track accuracy" sits in the same JSON and is null; SC-C-3's coverage-filtered AUROC answers a different question, and the JSON never states the AUROC's positive class. **This is the brief's trap: confidence used as a state discriminator without validation.** SC-C-3 does not appear in `manuscript/sections/` today and should not enter without this | block R4 |
| 9 | **MATERIAL** | `04_classifier/s1_loro_classifier.json` `per_backbone_best_auroc_kill_s1_row`, `kill_s1_verdict` | "KILL_S1_DID_NOT_FIRE (4/4 backbones ≥ 0.65)" | That field is the **maximum over feature sets**: 0.852 / **0.7595** / **0.7009** / 0.825 — chai and of3 are F_ii, not the F_iii the sheet quotes. The kill verdict is adjudicated on best-of-three. Compounding it, `SIGNAL_RECOVERY_REPORT.md` L279 reports a **pocket-only** set at mean 0.765 vs F_iii's 0.760, beating F_iii on exactly the two backbones SC-C-4 scopes out (Chai 0.760 vs 0.706; OF3 0.701 vs 0.656). The Boltz+Protenix scoping is a function of a feature-set choice another shipped file calls sub-optimal. OF3's F_iii clears the 0.65 threshold by **0.0057** | block R5 |
| 10 | **MATERIAL** | `04_classifier/g1_bootstrap_s1_auroc.json` protenix; `results.tex` L391–393 *"intervals … that exclude both chance and a permutation null"* | both CIs exclude the permutation null | Protenix cluster-boot lower bound **0.5280650** vs permutation-null upper **0.5272648** — a margin of **0.0008**, from 500 bootstrap and 200 permutation resamples. Monte-Carlo error on either quantile is one to two orders of magnitude larger. Boltz's margin is comfortable (0.5596 vs 0.5197); one verb covers both. The gating report is franker: *"Protenix cluster-boot [0.528, 0.960]. CI **just** excludes 0.5. **Marginally above chance**."* | `python3 -c "import json;d=json.load(open('data/block_c/04_classifier/g1_bootstrap_s1_auroc.json'))['per_backbone']['protenix'];print(d['cluster_boot']['ci_95'][0]-d['permutation_null']['ci_95'][1])"` |
| 11 | **MATERIAL** | AGTR1 exclusion, `09_references/AGTR1_REFASSIGN_REPORT.md` + `G2_REFERENCE_HOMOGENEITY.md`; SC-C-5 leads with the excluded number | "Excluding AGTR1 for scope-consistency reasons is defensible on curation grounds" | The exclusion was decided **after** AGTR1 was identified as the receptor that breaks the hypothesis. Both reports are self-labelled *"follow-up to G2's … regression"* and *"cross-check of the AGTR1 diagnostic's curation observation"*. The AGTR1 report certifies there is **no mechanical defect** (*"no swap, no mapping error"*; both references pass the activation predicate) and declines a corrected rerun because *"The biased-agonist curation observation is a **judgment call**, not a mechanical defect."* The homogeneity report concedes the structure: *"the … hypothesis has a **sample size of 1** and cannot be tested against counterexamples in this panel."* Removal flips the headline (−0.325 → −0.060) and SC-C-5's manuscript sentence leads with the post-exclusion number. **Read with finding 3**: under the block's own bootstrap convention there was no signal to remove, so the exclusion was never needed and the "AGTR1 carries ~85 %" framing describes an artifact of an invalid bootstrap | read the two reports; block R3 |
| 12 | **MATERIAL** | design fact, absent from every claim, caveat and flag | SC-C-1 / SC-C-4 discriminate "ligand class" / "ligand identity" | On **8 of the 15** S1 receptors and **11 of the 23** 2×2 receptors the agonist is a **peptide** and the antagonist a **small molecule**. The contrast is confounded with ligand modality on roughly half the panel, and peptide rows are ≥ 15 Å off-site on **72.5 %** of the 23-set apo rows against **2.0 %** for antagonists. The confound does **not** inflate the result — mixed-modality receptors score *lower* (mean LORO AUROC 0.863/0.714/0.606/0.834 vs 0.952/0.875/0.915/0.955) — which is a defence the paper does not make and a reviewer will ask for | block R6 |
| 13 | **MATERIAL** | `04_classifier/s1_loro_classifier.json`, split unit vs CI unit | leave-one-receptor-out with cluster-bootstrap CI | The **split** unit is genuinely the receptor — `PREREG_SIGNAL_RECOVERY.md` L42–48: *"Fold = one receptor held out. 23 folds total… scaling, threshold, coefficient fit on the 22 training receptors' rows"*. **The brief's structure-vs-receptor leak is not present.** But the **CI** unit is the paralog cluster, and 6 of the 15 S1 receptors have a paralog left in their training fold. Those 6 average **+0.073 AUROC** over the 9 singletons, and the adenosine pair **AA1R / AA2AR score exactly 1.000 on all four backbones** — the only pair to do so. If the cluster is the independent unit for the interval it is the independent unit for the fold; the convention is applied to one and not the other. Separately, the fold count for the 15-receptor headline row is stated nowhere (the prereg specifies 23 folds on the 23-set) | block R6 |
| 14 | **MATERIAL** | `04_classifier/s1_loro_classifier.json` AUROC denominator | "pooled AUROC", n_rows 1,500 | 1,500 = 15 receptors × 2 classes × **50 correlated rows** (5 seeds × 10 samples of a single receptor–ligand pair). Prereg L47 confirms the AUROC is over the held-out receptor's *rows*. The effective independent unit is the (receptor, ligand) pair; per-receptor AUROC is exactly 1.000 on 8/15 receptors for Protenix. Only the interval is clustered, never the point estimate. Same assumption in the G4 Wilson interval (binomial over rows) and in 312/4,500 (no CI, no clustering) | block R5 |
| 15 | **MATERIAL** | `10_pose_accuracy/task_E_v3_scoped_finding.json`; SC-C-7 *"6.93 % (312 of 4,500 rows)"* | 6.93 % on n = 4,500 | 312/4,500 = 6.93 % reproduces exactly, but 4,500 is the **populated** subset of **5,800** passed rows in those four cells. On all passed rows the rate is **5.38 %**. The 1,300 dropped rows are `no_atom_match` — a matcher reason not independent of pose. Also, the four cells are OF3 and Protenix × **both arms** (`partner_type` = apo *and* `g_alpha`); SC-C-7 and `results.tex` describe the subset without saying it pools the arms, in a paper whose thesis is that the arm matters. The JSON's own verdict string reads *"n=4500 rows out of 1400 antag"*, which cannot be parsed | block R7 |
| 16 | **MATERIAL** | `10_pose_accuracy/T7C_POST_FIX_HEADLINE.md` denominators | per-receptor medians 54–56 / 0–18 / 0 / 0 % | Three chained exclusions, none carried into the claim sheet: *"real ligand roles only (`decoy_lig` **excluded** per scorer docstring), `passed=true`, **numeric** `ligand_rmsd_to_ref`"* → **18,306** usable of 40,800, i.e. **22,494 rows dropped**. A fourth exclusion is silent: only the **redock** partition is printed; cross-dock cells are dropped from every cell. Per-receptor row counts behind each median are given nowhere — the only printed denominator is `n_rec`. The file also flags an uninvestigated artifact of its own matcher: *"**Chai × neutral_antag × cross-dock × apo → 100 % median on 6 receptors** — suspicious, possibly Bug #4 firing … **Not investigated in this pass**"* | read the file |
| 17 | **MATERIAL** | Chai's pose number across two shipped files | `results.tex` L424–426: *"median dock rates of 54–56 % on Boltz-2 against **0–18 % on Chai-1** and 0 % on the other two"* | The other shipped pose file, `t7b_pose_accuracy.json`, gives Chai neutral-antagonist **0.421 (apo) / 0.358 (cognate)** — *above* Boltz's 0.384/0.384 — and OF3/Protenix at 0.062–0.080, not 0. `SIGNAL_RECOVERY_REPORT.md`'s conservative ≥ 21-MCS-match filter gives **Boltz 53.6 %, Chai 38.3 %**. T7C gives a reason for the reversal (cross-dock rows and Bugs #2/#3 in t7b), so this is not a bare contradiction — but the manuscript sentence puts T7C's medians and the 6.93 % side by side when they come from **different corpora and different scorer SHAs** (finding 5), and no shipped file produces 0–18 % for Chai under any filter I can reconstruct | block R8 |
| 18 | **MATERIAL** | `09_references/reference_survey.csv` `picked_resname` | reference-ligand inventory; 10/126 Bug #2 events | **5 of 126** OK references pick a species that is on the *census script's own* `NON_LIGAND` blocklist, and `bug2_fires` is `no` on **4 of the 5** — the survey's centroid tripwire does not cover this class. Worst case: **AGTR1 active 6OS2 → `NAG`** (a glycan, 14 heavy atoms, `bug2=no`) chosen over the `SAR`-capped peptide agonist in chain B. AGTR1 is the receptor that inverts on all four backbones and carries the whole G2 story. Two more pick `NH2` — a **1-heavy-atom** amide cap (OXYR 7RYC, PRLHR 8ZPT). 15 of 126 pick a ligand with < 15 heavy atoms; 42 of 168 references have no HETATM candidate at all. Bounds `ligand_rmsd_to_ref` and reference routing, not pocket-Cα | block R9 |
| 19 | **MATERIAL** | Flag C-12, C-C-2, C-C-11 item 6, `02_caveats/README_BLOCK_C.md` vs SC-C-1 / C-C-3 | C-C-3 RESOLVED; SC-C-1 prints cluster-boot as primary | **Four** live files still say the 2×2 cluster-boot was never recomputed — Q3 in `OPEN_QUESTIONS.md` caught only Flag C-12. C-C-2 goes further and says *"the signed-direction claim **rests on the receptor-boot CIs**"*. The recompute exists (`g_scc1_cluster_boot.json`, 5,000 iter, seed 1234, 16 clusters) so the sheet is right and four files are stale — but a reviewer reading the caveats set gets the opposite | `grep -rn "not recomputed" data/block_c/01_claims data/block_c/02_caveats` |
| 20 | **MINOR** | `12_g4_off_site_census/g4_full_census_v2.py` far-mode tripwire | *"Chai residual far-mode: 175 rows ≥ 60 Å (1.7 % Chai-specific tail)"* | The script's own note reads *"if any survive at ≥ 60 Å on cognate, **second bug likely present**"*. 175 do, all on cognate. The tripwire fired and was relabelled a "residual far-mode" rather than investigated. Recomputed: 176 rows ≥ 60 Å, 175 Chai + **1 Boltz** (the Boltz row is mentioned nowhere) | block R8 |
| 21 | **MINOR** | `README.md` "Load-bearing numbers"; `results.tex` L432 | *"Peptide-agonist 'off-site' median centroid **17.5 Å** — extracellular vestibule binding by biology"* | 17.51 Å is the median over **all 6,800 peptide rows**, in-pocket ones included. Median over the peptide rows that are actually off-site is **27.0 Å**, running to 80 Å. A vestibule reading needs 27, not 17.5. Also note `results.tex` mixes scopes in one paragraph: 66.5 % is over all 36 receptors while 18.92/35.85/2.00 % are over the 2×2's 23 (72.50 % on that scope) | block R8 |
| 22 | **MINOR** | claim sheet `E-C-2` | *"**8 receptors** that are 100 % self-reference … (ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD, OPRK…)"* | Nine names follow the number 8. The JSON has 9; the intersection with the 23-set is 8. C-C-5 and `BLOCK_C_STATE_CHECK.md` state it correctly | read the file |
| 23 | **MINOR** | claim sheet SC-C-9 "Numbers"; Flag C-8 | *"40 dispatched Class A × 4 backbones = 40,000 target rows; 36 × 4 = 40,800 landed rows"* | 40 × 4 = 160 and 36 × 4 = 144. Neither closes. 40,000 is the **passed** count, not a target; the same sheet's preamble gives the target as 48,000. Separately, C-C-9 records FSHR and LSHR as *"Dispatched: **no**; 0 rows"* — so **38** were dispatched, not 40, and "dispatched" is used in two senses across the sheet | read the files |
| 24 | **MINOR** | claim sheet bootstrap preamble vs `g_scc1_cluster_boot.json`, SC-C-1, SC-C-8, Flag C-1 | *"**500** cluster-boot resamples; seeds `20260910..20260920`"*; *"cluster-boot over the **12** paralog clusters"*; SC-C-8 *"500–1000 resamples"* | The 2×2 cluster-boot used **5,000** iterations at **seed 1234** over **16** clusters. G2 used 1,000 receptor-boot. **No statistic in the sheet uses a seed in `20260910..20260920`.** Three seed conventions appear across the block (1234, 20260909, 20260910). `methods.tex` L417 states 5,000/1234/16 correctly | `python3 -c "import json;d=json.load(open('data/block_c/06_2x2_interaction/g_scc1_cluster_boot.json'));print(d['n_iter'],d['rng_seed'],d['n_clusters'])"` |
| 25 | **MINOR** | `manuscript/sections/results.tex` L397 | *"Boltz-2's bootstrap median, 0.809"*, next to cluster-bootstrap intervals | 0.809 is the **receptor**-boot median (0.80912). The cluster-boot median is 0.80820 → 0.808. A one-digit convention slip in the sentence whose subject is the bootstrap convention | `python3 -c "import json;d=json.load(open('data/block_c/04_classifier/g1_bootstrap_s1_auroc.json'))['per_backbone']['boltz'];print(d['cluster_boot']['median'],d['receptor_boot']['median'])"` |
| 26 | **MINOR** | `11_manuscript_narrative/BLOCK_C_PAPER_DRAFT_v1.md` L19 (abstract) | *"cluster-bootstrap 95 % CI excludes zero"*, citing `stage3_2x2_ligand_state_specificity.json` | That file's `interaction.ci_lo/ci_hi` are **bit-identical to the receptor bootstrap** in `g_scc1_cluster_boot.json` (boltz −0.4306353217487532 vs −0.4306353217487542). The draft calls a receptor-boot interval a cluster-boot one, three days before the cluster-boot existed. `results.tex` uses the correct intervals, so this is upstream-only — but the draft ships in the bundle | block R1 |
| 27 | **MINOR** | two quantities both named **P4** | — | SC-C-2's P4 is a Kendall-τ ordinal test on continuous Δ. `BLOCK_C_PAPER_DRAFT_v1.md` L232's P4 is *"per-receptor `antag_cog < agonist_cog` on ≥ 30/40"*, a binary-predicate count that **fires below on all four backbones (12/28 or 3/28)**. Same label, opposite verdict, both shipped | `grep -n 'P4' data/block_c/11_manuscript_narrative/BLOCK_C_PAPER_DRAFT_v1.md` |
| 28 | **MINOR** | `12_g4_off_site_census/g4_full_census_v2.csv` `receptor_anchor_hits` | script docstring *"0-6; 6 = full confidence"*; `flag_low_confidence` if < 4 | 1,200 rows report **20** hits. The named-anchor count is receptor-dependent, so both the documented range and the fixed `< 4` rule are wrong for those receptors. **Zero** of 40,000 rows are flagged low-confidence, which makes the flag uninformative rather than reassuring | `python3 -c "import csv,collections;print(collections.Counter(r['receptor_anchor_hits'] for r in csv.DictReader(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv'))))"` |
| 29 | **MINOR** | `03_withdrawals/W-C-8` | *"the verdict was authored under the binary-predicate framing (**SC-C-6** / C-C-1 — later retired)"* | SC-C-6 is a **surviving** claim in the same bundle. A withdrawal document says a live claim was retired | read the file |
| 30 | **MINOR** | `09_references/G2_REFERENCE_HOMOGENEITY.md` §2 | *"CXCR2 inverts on OF3 only. **OPRX** inverts on OF3 only"* | Its own stated rule is AUROC < 0.30, and OPRX/OF3 is **0.361**. The AGTR1 report's `n_inverted` for OF3 (2 full, 1 excl-AGTR1) counts CXCR2 only. SC-C-5, Flag C-4 and Flag C-5 name only AGTR1 and CXCR2. Either the homogeneity sentence is wrong or the empirical failure list is short by one receptor | `grep -n OPRX data/block_c/05_ref_separation/g2_refsep_vs_auroc.csv` |
| 31 | **MINOR** | `11_manuscript_narrative/BLOCK_C_WRAP_REPORT.md` | retraction banner: *"**Adjudication**: not material for SC-C-1 or SC-C-4"* | The banner was prepended; **the body was not revised**. Lines 52–369 still read `RESULT: MATERIAL`, *"§1(b) verdict — MATERIAL"*, *"it is a first-order finding"*, and ask *"Is 25.6 % pooled off-site material enough to require SC-C-1 / SC-C-2 / SC-C-4 rewrites?"* A reader who scrolls past the banner gets the opposite adjudication. (The 25.6 % itself is correctly retracted — it does not reproduce under any band definition; pooled is 17.73 %) | read the file |
| 32 | **MINOR** | `02_caveats/C-C-11` | *"none of these are load-bearing on any surviving Block C claim"* | **G2d** tests whether Check 2's 10-receptor fold-integrity subset is drawn from the low-separation mode, and SC-C-5 is precisely a claim about which receptors the classifier works on; `G2_REFERENCE_HOMOGENEITY.md` agrees it is unresolved (*"G2d stays on its own deferred-caveats line"*). **G4** is finding 2. C-C-11 also lists 7 numbered items then says *"any of these **six** items"*, while Flag C-11 says *"**Five** deliverables"* and the caveats README lists 6 | read the files |
| 33 | **MINOR** | permutation count | claim sheet: *"200 permutation-null resamples"* | Correct for `g1_bootstrap_s1_auroc.json` (`n_perm: 200`). But `s1_loro_classifier.json` — the source of every per-variant `permutation_p_value = 0.0` — ran at `null_permutation_n: **5**`, against the prereg's *"**1000** permutations"*; `SIGNAL_RECOVERY_REPORT.md` L29 concedes *"the 200-perm run was **killed** after 30+ min"* and L214 says *"Rerun at n=200 or n=1000 **before publication**."* No caveat or flag records this | `python3 -c "import json;print(json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))['n_permutations'])"` |
| 34 | **MINOR** | `04_classifier/s1_loro_classifier.json` F_i variants | `SIGNAL_RECOVERY_REPORT.md` L40: *"**F_i (single scalar) fails on all 4 backbones.**"* | All 12 F_i variants sit **below 0.5**, in the same direction, with `permutation_p_value = 1.000` — 0.323 to 0.462. That is not a null; it is a one-sided test run against an inverted sign convention. Flipped, F_i gives 0.54–0.68, which is exactly the direction SC-C-1 claims. The framing correction the report draws from it (*"the 2×2 rescue … is a group-mean contrast, not a per-row scalar"*) may still be right, but not for the reason given | block R5 |

---

## What reproduced exactly

Recomputed independently from `12_g4_off_site_census/g4_full_census_v2.csv`
(40,000 rows) and `05_ref_separation/g2_refsep_vs_auroc.csv`:

- **G4 census, every band**: 25,559 in-pocket / 7,349 entrance-bound / 7,092
  off-site; pooled 17.73 %; apo 15.135 % [14.645, 15.638]; cognate 20.325 %
  [19.773, 20.888]. Wilson intervals match to 15 decimal places.
- **SC-C-1's stated numerator**: 149/9,800 = **1.520 %**, exact.
- **G2 point estimates**: full-15 slope −0.32499, R² 0.16177, ρ −0.20561;
  excl-AGTR1 −0.05995, R² 0.01045, ρ −0.01513 — all exact. AGTR1 rank 39/40,
  second largest in the Block B panel, confirmed against
  `reference_separation_pocket_ca.csv`. (The sheet's *"~85 % of the signal"* is
  81.6 % on the arithmetic.)
- **SC-C-4's F_iii row** and all four cluster-boot intervals: exact.
- **SC-C-7's aggregate**: 312/4,500 = 6.933 %, exact.
- **Chai far mode**: 175 Chai rows ≥ 60 Å, exact.
- **The manuscript's own added off-site paragraph** reproduces to the last digit:
  18.92 % on the 23-set, 35.85 % agonist vs 2.00 % antagonist, Spearman
  ρ = −0.241 at n = 23, split medians 0.282 vs 0.386. That paragraph is the
  strongest piece of self-criticism in the section and it is arithmetically
  sound.
- **D-C-3 confirmed**, with an extension. SC-C-2's table values are
  `fraction_positive_significant`, not τ; median τ is 0.386/0.259/0.328/0.366 on
  the 23-set. The claim sheet is **still mislabelled as shipped**; `results.tex`
  is corrected. What D-C-3 does not say is that the fraction also discards
  **sign**: on the 23-set the count of receptors with a *significantly negative*
  τ is 2 (Boltz), **5 (Chai)**, 1 (OF3), 2 (Protenix). `EDNRB` and `LT4R1`
  invert on three of four backbones. No panel is free of them.

---

## Trap-by-trap answers to the brief

**LORO split key — receptor or structure?** **Receptor.**
`PREREG_SIGNAL_RECOVERY.md` L42–48 states it and puts scaling and the Youden
threshold inside the fold. Two data checks agree: a structure-level split could
not yield AUROC **0.000** on a held-out receptor (AGTR1 on chai/of3/protenix) or
0.135 (CXCR2 on of3), because sibling rows in training would pull those toward 1.
**The leak that is present is a different one** — paralogs split across folds
while the interval treats the paralog cluster as the independent unit
(finding 13) — plus pseudo-replication of 50 correlated rows per class
(finding 14). Note also that the *gating report* never states the fold
construction at all; it exists only in the prereg.

**2×2 — interaction term tested, or four cell means compared?** The interaction
term was genuinely estimated and bootstrapped: per receptor as
Δ_active − Δ_inactive across agonist vs antagonist, averaged, then resampled.
That is the right construction. Three riders. (a) The four cell means shipped in
the same JSON are computed on **different receptor sets** (28 agonist, 23
antagonist) and therefore do **not** reconstruct the interaction:
(0.768 − 0.976) − (0.898 − 0.767) = −0.340 against a reported −0.306 for Boltz.
Any panel drawing the four cells with the interaction beneath them shows two
things that do not add up. (b) The cell blocks label the receptor count
`n_clusters`, which it is not. (c) The row counts say the arm scope is wrong
(finding 4).

**07 — does the summary hide per-receptor heterogeneity?** Yes, twice over: the
τ-vs-fraction mislabel (D-C-3) and the discarded sign (above). Chai has 5 of 23
receptors running significantly backwards under a "65 %" headline.

**08 — is confidence used as a state discriminator without validation?** Yes.
Findings 7 and 8; the validation test is in the same file and is null.

**12 — off-site fraction, and does any accuracy claim silently exclude it?**
17.73 % pooled at the shipped ≥ 15 Å definition; **36.10 %** at ≥ 8 Å
(entrance-bound is adjudicated valid — defensible and stated in `methods.tex`,
but it more than doubles the failure rate if a reviewer disagrees). Off-site is
strongly role-dependent: agonist rows 27–31 % on every backbone, antagonist rows
0–5 %, chai × decoy × cognate **52.4 %**. The silent exclusions are not in the
census — they are in the pose claims: SC-C-7 drops 1,300 of 5,800 rows for
`no_atom_match` (finding 15), and T7C drops 22,494 of 40,800 plus the entire
cross-dock partition (finding 16). And the block's own reassurance is computed
on a subset chosen to exclude the worst-behaving rows (finding 2).

---

## What I could NOT check, and why

1. **SC-C-1's 2×2 and SC-C-4's classifier cannot be recomputed at all.**
   `rows.tier3.v2.csv` (SHA `5ccf58ac…`) is not in the bundle. Finding 4 is an
   arithmetic inference from the design grid and the shipped `n_rows`, not a
   recomputation. One command against the source rows settles it; nothing else
   will. Same for finding 14's effective n.
2. **The pose sibling corpus** (`rescore_t7c_full/rows.csv`, scorer
   `d9c646af…`) is not in the bundle, so T7C's per-receptor medians — including
   the 0–18 % Chai figure — are unverifiable in either direction. I can show they
   disagree with the pose file that *was* shipped and that they come from a
   different corpus than the 6.93 % beside them; I cannot show which is right.
3. **Only one analysis script shipped** (`g4_full_census_v2.py`).
   `stage3_post_audit_analysis.py`, `g1_bootstrap_s1_auroc.py`,
   `g2_refsep_vs_auroc.py` and `recompute_2x2_cluster_boot.py` are named and
   absent. Findings 3 and 9 are inferred from emitted numbers, not read off code
   — though finding 3's inference is strong (my row-boot reproduces the
   published interval to three decimals on both the 15- and 14-receptor sets
   while the receptor-boot does not, and the gating report independently admits a
   row-boot label is in use).
4. **SC-C-6's "~65 % of cells unresolvable"** — `nan_reason_census.csv` is named
   and absent. Not checked.
5. **SC-C-10's "28/28 receptors have identical `pocket_ref_pdb_sha_inactive`"** —
   the SHA column is in the undelivered rows file. Not checked. Note the claim is
   about the *current corpus*, so "by construction" holds only while the routing
   stays collapsed; the claim text says so, C-C-10 says so, `results.tex` says so.
6. **`BLOCK_C_WRAP_REPORT_v2.md`**, named by the retraction banner as carrying
   the authoritative 17.7 / 15.1 / 20.3 / 1.52 figures, **is not in the bundle**.
   I verified those four directly from the census instead.
7. **Whether top-25 % (S3) was chosen before or after seeing the sweep** cannot
   be established from the shipped files — only that it is absent from the
   pre-registration and absent from the declared deviations list. I report the
   fact, not an intent. The same caution applies to finding 9's feature-set
   choice; finding 11's AGTR1 exclusion is different, because the documents
   themselves establish the ordering.
8. **The 800 failing rows** (OPSD/B1B1U5 `A5_species_match`) are excluded by
   `passed=True` from the census, so nothing here touches them.
   `docs/AUDIT_TRAIL.md §21` is not in the bundle.
9. **No figure panel was opened.** This pass is numeric only.

---

## Reproduction

From the repo root, `/Users/aditya/Documents/tools/Novartis_projects/paper`. All
read-only.

```bash
# R1 — stage3's "interaction" CI is the receptor bootstrap, not the cluster one
python3 - <<'PY'
import json
a=json.load(open('data/block_c/06_2x2_interaction/stage3_2x2_ligand_state_specificity.json'))
b=json.load(open('data/block_c/06_2x2_interaction/g_scc1_cluster_boot.json'))
for bb in a['per_backbone']:
    s=a['per_backbone'][bb]['interaction']; g=b['per_backbone'][bb]
    print(bb,'stage3',s['ci_lo'],'| receptor_boot',g['receptor_boot_recomputed']['ci_lo'],
             '| cluster_boot',g['cluster_boot']['ci_lo'])
    print('   n_rows',a['per_backbone'][bb]['n_rows'],'n_receptors',a['per_backbone'][bb]['n_receptors'])
PY

# R2 — the pre-specified G4 gate (>=5% off-site per backbone per class) fires on 8/12
python3 - <<'PY'
import csv, collections
rows=list(csv.DictReader(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv')))
d=lambda r: float(r['distance_A'])
agg=collections.defaultdict(list)
for r in rows: agg[(r['backbone'],r['role'])].append(r)
fired=0
for k in sorted(agg):
    rs=agg[k]; f=sum(1 for r in rs if d(r)>=15)/len(rs); hit=f>=0.05; fired+=hit
    print(f"{k[0]:<9}{k[1]:<20}{100*f:6.1f}%  {'FIRES' if hit else '-'}")
print(f"{fired} of {len(agg)} cells fire")
for lo in (5,8,10,15):
    print(f"pooled >= {lo:>2} A: {100*sum(1 for r in rows if d(r)>=lo)/len(rows):5.2f}%")
PY

# R3 — G2: the published CI is a ROW bootstrap; a receptor bootstrap spans zero
python3 - <<'PY'
import csv, random
rows=list(csv.DictReader(open('data/block_c/05_ref_separation/g2_refsep_vs_auroc.csv')))
def ols(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
def boot(sub,mode,iters=5000,seed=11):
    random.seed(seed); out=[]
    if mode=='row':
        pts=[(float(r['pocket_ca_sep']),float(r['auroc'])) for r in sub]
        for _ in range(iters):
            s=[random.choice(pts) for _ in pts]
            out.append(ols([p[0] for p in s],[p[1] for p in s]))
    else:
        byr={}
        for r in sub: byr.setdefault(r['receptor'],[]).append(r)
        ks=list(byr)
        for _ in range(iters):
            xx=[];yy=[]
            for k in (random.choice(ks) for _ in ks):
                for r in byr[k]: xx.append(float(r['pocket_ca_sep'])); yy.append(float(r['auroc']))
            try: out.append(ols(xx,yy))
            except ZeroDivisionError: pass
    out.sort(); return round(out[int(.025*len(out))],4), round(out[int(.975*len(out))],4)
for lab,keep,pub in (("full 15",lambda r:True,"[-0.5710,-0.0643]"),
                     ("excl AGTR1",lambda r:r['receptor']!='AGTR1',"[-0.2464,+0.0866]")):
    sub=[r for r in rows if keep(r)]
    print(f"{lab:11} published {pub}  row-boot {boot(sub,'row')}  receptor-boot {boot(sub,'receptor')}")
PY

# R4 — S3: pLDDT wins at top-10%; consensus-vs-accuracy Spearman is ~0
python3 - <<'PY'
import json
d=json.load(open('data/block_c/08_confidence_signal/s3_consensus_confidence.json'))
cov=('10','25','50','75','100')
print("coverage:","".join(f"{c:>8}" for c in cov))
for bb,v in d['s3c_accuracy_vs_coverage'].items():
    c=[v['consensus'][k]['auroc'] for k in cov]; p=[v['plddt'][k]['auroc'] for k in cov]
    print(f"{bb:9} cons " + "".join(f"{x:8.3f}" for x in c))
    print(f"{'':9} pLDD " + "".join(f"{x:8.3f}" for x in p))
    print(f"{'':9} win  " + "".join(f"{('CONS' if a>b else 'PLDDT'):>8}" for a,b in zip(c,p)))
for bb,v in d['s3b_spearman_consensus_vs_pca_active'].items():
    print(f"{bb:9} rho(consensus,acc)={v['spearman_full']:+.4f}  rho(pLDDT,acc)={v['plddt_spearman_full']:+.4f}")
PY

# R5 — LORO: best-of-feature-set verdict, pooled vs per-receptor, F_i inversion
python3 - <<'PY'
import json, statistics
d=json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))
print("kill_s1_row (max over feature sets):", d['per_backbone_best_auroc_kill_s1_row'])
print("verdict:", d['kill_s1_verdict'], "| n_permutations:", d['n_permutations'])
for v in d['variants']:
    if v['variant']!='C_no_selfref_apo': continue
    pr=list(v['per_receptor_auroc'].values())
    print(f"  {v['backbone']:9} {v['feature_set']:24} pooled={v['pooled_auroc']:.4f} "
          f"mean_per_rec={statistics.mean(pr):.4f} n_rows={v['n_rows']} perm_p={v['permutation_p_value']}")
PY

# R6 — paralog-in-fold, and peptide/small-molecule modality confound
python3 - <<'PY'
import csv, json, collections, statistics
rows=list(csv.DictReader(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv')))
d=json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))
g=json.load(open('data/block_c/04_classifier/g1_bootstrap_s1_auroc.json'))
cmap=g['per_backbone']['boltz']['cluster_boot']['cluster_map_receptor_to_cluster']
sz=collections.Counter(cmap.values())
paired=[r for r,c in cmap.items() if sz[c]>1]; single=[r for r,c in cmap.items() if sz[c]==1]
mod=collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in rows:
    if r['arm']=='apo': mod[r['receptor']][r['role']][r['ligand_source']]+=1
M=lambda rec,role:'peptide' if mod[rec][role]['peptide_chain']>mod[rec][role]['hetatm'] else 'smallmol'
print("paralog-in-fold:",sorted(paired)," singletons:",sorted(single))
for v in d['variants']:
    if v['variant']!='C_no_selfref_apo' or v['feature_set']!='F_iii_pocket_plus_axes': continue
    pr=v['per_receptor_auroc']
    mixed=[r for r in pr if M(r,'full_agonist')!=M(r,'neutral_antagonist')]
    print(f"{v['backbone']:9} paralog {statistics.mean(pr[r] for r in paired):.4f} "
          f"singleton {statistics.mean(pr[r] for r in single):.4f} | "
          f"mixed-modality {statistics.mean(pr[r] for r in mixed):.4f} (n={len(mixed)}) "
          f"same {statistics.mean(pr[r] for r in pr if r not in mixed):.4f}")
PY

# R7 — pose accuracy denominators
python3 - <<'PY'
import json
d=json.load(open('data/block_c/10_pose_accuracy/task_E_v3_scoped_finding.json'))
c=d['dock_rate_per_cell']
print("cells:", [(x['backbone'],x['partner_type']) for x in c])
tot=sum(x['n_passed'] for x in c); pop=sum(x['n_populated_ligand_rmsd'] for x in c)
dk=sum(x['n_ligand_rmsd_lt_3A'] for x in c)
print(f"passed={tot} populated={pop} dock={dk} | on populated {dk/pop:.4f} | on passed {dk/tot:.4f}")
print("corpus cited:", d['reconstruction']['inputs']['rows_csv']['sha256'])
PY

# R8 — Chai pose ordering, peptide median, far-mode tripwire
python3 - <<'PY'
import json, csv, statistics, collections
t=json.load(open('data/block_c/10_pose_accuracy/t7b_pose_accuracy.json'))
for x in t['canonical_pose_row_neutral_antag_all_backbones']:
    print(f"{x['backbone']:9}{x['arm']:9} dock_rate_numeric={x['dock_rate_numeric']:.3f} cov={x['coverage']:.3f}")
rows=list(csv.DictReader(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv')))
f=lambda r: float(r['distance_A'])
pep=[f(r) for r in rows if r['ligand_source']=='peptide_chain']
print("peptide median ALL:",round(statistics.median(pep),2),
      "| OFF-SITE only:",round(statistics.median([d for d in pep if d>=15]),2))
far=[r for r in rows if f(r)>=60]
print(">=60A:",len(far),collections.Counter(r['backbone'] for r in far),collections.Counter(r['arm'] for r in far))
PY

# R9 — reference ligand picking
python3 - <<'PY'
import csv
NON={"HOH","NAG","BMA","MAN","FUC","BGC","NH2","GOL","EDO","PGE","PG4","SO4","PO4","CLR","CHS","OLC","OLA"}
rows=[r for r in csv.DictReader(open('data/block_c/09_references/reference_survey.csv')) if r['status']=='OK']
bad=[r for r in rows if r['picked_resname'] in NON]
print(f"{len(bad)} of {len(rows)} OK references pick a blocklisted species as 'the ligand'")
for r in bad:
    print(" ",r['receptor_slug'],r['role'],r['pdb_id'],r['picked_resname'],
          "n_heavy="+r['picked_n_heavy'],"bug2="+r['bug2_fires'])
print("no HETATM candidate at all:",
      sum(1 for r in csv.DictReader(open('data/block_c/09_references/reference_survey.csv'))
          if r['status']=='NO_HETATM_CANDIDATES'))
PY
```

---

## Suggested order of attention

1. **Finding 4** — one command against `rows.tier3.v2.csv` settles whether the
   headline 2×2 is apo-only. *"This holds in the apo arm alone"* is the scope
   sentence the entire ligand-attribution argument rests on, and the shipped row
   counts say it is not true.
2. **Finding 1** — SC-C-2's "pre-registered" framing. If the ≥ 6/8 threshold
   exists only in a document not in the bundle and is met only on the panel
   W-C-9 withdrew, the evidential-weight sentence in `results.tex` L385 has to
   go or the pre-registration has to be produced.
3. **Findings 2 and 11 together** — the G4 gate was pre-specified, it fired on
   8 of 12 cells, its remedy was skipped, and AGTR1 was excluded post hoc on a
   criterion articulated after it broke the hypothesis. Both are decisions the
   Methods should record rather than the data hide.
4. **Finding 3** — re-run the G2 bootstrap over receptors. The likely outcome
   *strengthens* SC-C-5 (no signal either way, so no "AGTR1 carries 85 % of it"
   story is needed) while removing a violation of the block's own convention.
5. **Findings 5, 6, 16, 17** before any pose sentence is finalised: the 6.93 %
   is cited to the forbidden corpus, its own successor calls it a pooling
   artifact, and the Chai figure beside it comes from a third file that the
   other shipped pose file contradicts.
6. **Findings 7, 8** before SC-C-3 enters the manuscript at all. It currently
   does not, which is the right state.
