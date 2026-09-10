# Block C — signal-recovery pre-registration

**Locked**: 2026-09-07 (before any S1 evaluation number is computed)
**Scope**: Block C v5 landed data only. `experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv` + Block A rows for Task-F-relevant cells. No new predictions.
**Goal**: Determine whether the Block C corpus supports a **prospective single-structure classifier** (a method) or only a **group-mean characterization**.

## Standing discipline (non-negotiable)

1. **LORO cross-validation on every performance number.** No threshold, scaler, feature weight, or hyperparameter is fitted on a receptor that appears in the evaluation fold. Pooled-fit-then-evaluate is the failure mode.
2. **Permutation null on every performance number.** 1000 permutations, ligand-class labels shuffled WITHIN receptor, full pipeline including LORO re-run on each. Raw AUROCs without their null are not results.
3. **Kill criteria (below) are binding.** If a criterion fires, that IS the finding. Do not search for a variant that passes. Report the negative.
4. **Every number carries its script path + provenance sidecar (SHA of inputs, git HEAD, RNG seed).**
5. **Per-receptor breakdowns are mandatory**; pooled AUROCs carried by a subset are not methods.
6. **Regex on `input_path`** for arm/backbone/seed/receptor; do not trust pre-parsed columns without cross-checking against the manifest.
7. **No git push. No manuscript prose edits.** Local commits only for pre-reg + final report.

## Pre-registered kill criteria (BINDING)

### KILL-S1 (centerpiece)
If LORO AUROC on the **apo arm**, **self-reference-excluded**, is **< 0.65 on ALL four backbones**, there is no prospective single-structure classifier in this corpus. Report that verdict; stop the method-extraction line. The 2×2 characterization result is retained; a method claim is not made.

### KILL-S3
If cross-backbone agreement predicts distance-to-crystal **no better** than pLDDT does on matched folds (paired Δ AUROC ≤ 0, CI clears zero on at least 2 of 4 backbones), report the negative and stop the confidence-signal claim line.

### KILL-S4 (secondary)
If the top-k reduced instrument (k ≤ 10) does NOT match whole-pocket RMSD (within 0.03 AUROC on LORO, apo arm), the whole-pocket aggregate remains the reference readout; no minimal-instrument claim.

## Feature sets (S1)

Reported separately:
- **(i)** `Δ = pocket_ca_rmsd_active − pocket_ca_rmsd_inactive` — single scalar.
- **(ii)** (i) + `pocket_ca_rmsd`, `pocket_sidechain_rmsd_active`, `pocket_sidechain_rmsd_inactive`, `w648_chi1`.
- **(iii)** (ii) + `d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`, `d_r350_r630_ca` as continuous values (NOT thresholded).

All features are per-row (not per-cell). Aggregation to per-cell happens inside the classifier evaluation (mean over 5 seeds × 10 samples per row).

## Model choice (S1)

- **Feature (i)**: single-threshold classifier. Threshold selected by Youden's J on the training fold; evaluated on held-out receptor.
- **Feature (ii)**, **(iii)**: L2-regularized logistic regression with standardization inside the training fold. No tree ensembles. If the ratio of features to training receptors exceeds 1:3, features are dropped by univariate ANOVA on the training fold only.

## LORO protocol

- Panel = 23 receptors in the 2×2 common set (intersection of full_agonist × neutral_antagonist × active-ref × inactive-ref).
- Fold = one receptor held out. 23 folds total.
- Within a fold: scaling, threshold, coefficient fit on the 22 training receptors' rows; prediction on the 23rd's rows.
- Cell-level evaluation: AUROC on the held-out receptor's full_agonist vs neutral_antagonist rows.
- Report per-receptor AUROC distribution + LORO pooled AUROC + LORO pooled average precision.

## Permutation null protocol (S7 integrated)

- For each of 1000 permutations: shuffle ligand-class labels WITHIN receptor (preserves per-receptor class balance). Rerun the full LORO pipeline including fold-internal scaling and threshold selection.
- Report null AUROC distribution (mean, 2.5th, 50th, 97.5th percentiles).
- Observed AUROC compared against the null via: (a) permutation p-value, (b) z-score against null mean.

## Sample-budget protocol (S2)

- For each cell (receptor × ligand_role × arm × backbone), sub-sample N ∈ {1, 2, 5, 10, 20, 50} rows without replacement, 100 draws per N.
- Aggregate per cell by: mean, median, best-of-N (nearest to active reference).
- Additional readout: within-cell dispersion (SD or IQR of `pocket_ca_rmsd`).
- Report AUROC(N) curve with bootstrap CIs on the sub-sample resampling.
- Seed-vs-sample variance: two-way ANOVA on `pocket_ca_rmsd` per (receptor, backbone, ligand_role, arm) with seed and sample-index as random effects.

## Backbone protocol

- All 4 backbones (Boltz, Chai, OF3, Protenix) run independently.
- Pooled backbone AUROC reported alongside per-backbone.
- **S3 uses ALL 4 backbones to compute consensus**; S1 uses each backbone alone.

## Self-reference exclusion (from T1 result)

The 9 receptors that are 100 % self-reference on the antag_inactive cell: **ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD, OPRK**.
- S1 primary run: include all 23 receptors.
- S1 apo-arm run: include all 23 receptors (self-reference is on the antag_inactive cell, which uses `pocket_ca_rmsd_inactive`; apo arm still uses both metrics but no partner).
- S1 self-reference-excluded run: 14 receptors (23 − 9). This is the run against KILL-S1.
- Ceiling estimate (S7b): the 9 self-reference receptors alone.

## Data sources (SHA-pinned)

- Rows: `experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv` (SHA `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`)
- Manifest: `experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv`
- Reference set: `refs/reference_set.csv` (SHA `7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a87493295a8d8382b90c`)
- Block A rows (for prerequisite recomputes): `experiments/018_block_a_switch_test/analysis/rows.pocket.csv`, `rows.rmsd.csv`
- BW numbering: use the `panel_bw` canonical UniProt anchors (per `docs/AUDIT_TRAIL.md` this is the closest-to-correct convention). Cross-check S4 top positions across `panel_bw_realigned` and `confornet_bw`; report any convention-dependent instability.

## Prerequisites (gate interpretation, not execution)

Run in parallel with S1 setup. Findings enter the final report before conclusions are drawn.

- **PR1**: sweep every consumer of `rows.tier3.csv` (pre-fix) vs `rows.tier3.v2.csv`. Establish which landed numbers share the P0 defect (ρ 0.129 → 0.180 shift).
- **PR2**: resolve FSHR/LSHR GPCR class (glycoprotein hormone receptors are Class A per GPCRdb; report says Class F) and the 7FIH vs 7FIJ discrepancy.
- **PR3**: confirm which reference enters `apo coherent-active`. If it uses only the two-instrument predicate (no reference), the FSHR/LSHR PAM strip does not apply to that metric; clean-bound n and mean must be restated.
- **PR4**: attach cluster-bootstrap CIs to every clean-bound stratum mean.
- **PR5**: fast-path match-count census on Boltz/Chai ligand rows. Distinguish 0, 1-4 (spurious RMSD!), ≥5 matches. Establish whether the current NaN or non-NaN state on Boltz/Chai reflects actual coverage or spurious readings.

## Claim ladder (target destinations)

Every claim in the final report is tagged with the rung it supports.

- **Rung 0** — Characterization: models encode ligand identity in pocket geometry (group-mean 2×2). Status entering this investigation: **established**.
- **Rung 1** — Discrimination: pocket geometry separates ligand classes at the level of a single held-out receptor (LORO AUROC > null on a majority of folds).
- **Rung 2** — Prospective readout: Rung 1 in the apo arm, with a stated sample budget (S2) and a stated applicability domain (S8).
- **Rung 3** — Instrument: a minimal (S4), interpretable, mechanistically localized metric with a working confidence signal (S3) that outperforms pLDDT.

The final report states plainly which rung the data supports. Language for lower rungs must not imply higher ones.

## Kill-criteria ledger (populated by the final report)

| criterion | fired? | evidence | action taken |
|---|---|---|---|
| KILL-S1 | (tbd) | (tbd) | (tbd) |
| KILL-S3 | (tbd) | (tbd) | (tbd) |
| KILL-S4 (secondary) | (tbd) | (tbd) | (tbd) |

If any criterion fires and downstream analysis continues, that must be stated explicitly and justified (with reference to which rung of the ladder the continuation is targeting).

## Output artifact

`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/SIGNAL_RECOVERY_REPORT.md`

Per task S1–S8: recomputed number, permutation-null distribution, LORO status, script path, provenance sidecar path.

Then: claim ladder with evidence + kill-criteria ledger.

## Anti-shopping guard

**This document is version-locked at the moment of the first commit.** Any subsequent edit is a violation of pre-registration discipline and must be flagged explicitly in the final report's "Pre-registration deviations" section. Feature sets, kill criteria, thresholds, and folds are frozen. Prerequisite findings may change what numbers are trusted but must not change the pipeline's evaluation contract.
