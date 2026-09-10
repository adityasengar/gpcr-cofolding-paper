# Block B — narrative-primitive cross-document audit

**Scope**: the Block B *narrative* primitives only — `data/block_b/README.md`,
`data/block_b/FIGURE_BRIEF.md`, all of `data/block_b/12_narrative/` (claim sheet,
flags, post-freeze checks, E1–E4 follow-up, Item 3, assumed-not-verified, dossier,
16 caveats, 6 withdrawals, 6 figure specs), the per-directory `claim_answers.csv`
answer-beside-data files, and `data/block_b_structures/` (bundle manifest,
`SUPERPOSITION.md`, `LADDER_FRAMING.md`, `SEALED_REFERENCES.md`).

**Failure class hunted**: cross-document contradiction — two documents in one
delivered bundle asserting different things about the same quantity, scope, or
status. Not "does the drop reproduce" (that is
`analysis/block_b/DISCREPANCY_REPORT.md`, D-B-1..D-B-5, not re-reported here).

**Result**: **27 contradictions**, ranked by whether they reach a reader of the
published paper. Plus two corrections to `DISCREPANCY_REPORT.md` and a section of
things checked that turned out **not** to be contradictions.

Nothing under `data/` was modified. `data/block_b/` and `data/block_b_structures/`
are `chmod a-w` and were read only.

---

## How to run the reproductions

Every reproduction below is a `python3` snippet run from the repo root
`/Users/aditya/Documents/tools/Novartis_projects/paper`. They assume only pandas.
Where a contradiction is document-vs-document with no data side, the reproduction
is a `grep` and both sides are quoted verbatim — per `rebuttals/README.md` an
unquoted contradiction is not usable, and I have quoted both sides of all 27.

---

# TIER 1 — would reach a reader of the published paper

## N-B-1 — One document says Block B **is** prospective; two say prospectivity is foreclosed

**The claim as shipped.**
`data/block_b_structures/01_instrument_references/SEALED_REFERENCES.md`,
§"Role of these references in Block B scoring":

> "These references were used to compute delta axes during scoring; they
> were **never shown to any predictor** — Block B is prospective per
> PREREG §11b and per the panel-wide templates-OFF audit (SC-B-7)."

**What the rest of the bundle says.** `data/block_b/README.md`, §"What Block B
does NOT claim":

> "- Prospectivity — foreclosed by design; date-stratified holdout is Block C."

And `data/block_b/12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md`, §Executive summary:

> "Block B does NOT claim: prospectivity (foreclosed by design; date-stratified
> holdout is Block C); mechanism at the residue level (Block C tier 3);
> directional control (Block D D2)."

The two are not reconcilable by scope. `SEALED_REFERENCES.md` also mis-cites its
authority: PREREG §11b is the *templates-off* evidence-class rule everywhere else
it is named — `caveats/C-B-1_templates_evidence_class.md` §"Why it matters":
*"PREREG §11b accepts class (b) + (c) as sufficient for the templates-off lock."*
Templates-off is not prospectivity, and SC-B-7's own evidence is class (b)+(c),
explicitly not runtime-verified (C-B-1, Flag B-5).

**Reproduction.**
```
grep -rn "prospective\|Prospectivity" data/block_b/README.md \
  data/block_b/12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md \
  data/block_b_structures/01_instrument_references/SEALED_REFERENCES.md
```

**Severity: highest. It reaches the reader and it is the strongest claim in the
bundle.** "Prospective" is the single word a reviewer will weight most, and a
figure or Methods agent reading the structure bundle in isolation — which is
exactly how that bundle is designed to be consumed — has written permission to
use it.

**What would close it.** Delete the prospectivity clause from
`SEALED_REFERENCES.md` and replace it with the narrow claim actually supported:
the two reference CIFs were used by the scorer and never supplied to any
predictor. Confirm which PREREG section, if any, is being invoked.

---

## N-B-2 — "No ladder-height covariate has a slope excluding zero" — the drop's own regression table has one that does

**The claim as shipped.** `12_narrative/BLOCK_B_CLAIM_SHEET.md` § SC-B-11 title
and claim:

> "### SC-B-11 — No ladder-height covariate has a slope excluding zero at 95% CI
> **Claim**: On the three usable predictors (Δ_ref NPxxY-OH, Δ_ref TM6-tilt,
> coupling promiscuity from `refs/gpcr_coupling.csv`), no panel slope excludes
> zero at 95% CI on either continuous or logit scale, with or without AA2AR."

`caveats/C-B-14_no_covariate_slope_excludes_zero.md` §"Manuscript sentence" turns
it into the reader-facing form:

> "> On the 40-receptor Block B panel, no ladder-height covariate (per-receptor
> Δ_ref NPxxY-OH, Δ_ref TM6-tilt, coupling promiscuity) has a panel slope
> excluding zero at cluster-boot 95% CI on either the continuous or the logit
> scale."

`08_covariates/claim_answers.csv` certifies it:
`SC-B-11,any_predictor_ci_excludes_zero,False,,,ladder_height_regressions.csv,True`

**What the data says.** `08_covariates/ladder_height_regressions.csv`, panel rows,
carries a fourth predictor the claim sheet does not mention — a categorical
`cognate_family` term — and one of its levels excludes zero:

| backbone | predictor | scale | n | slope | 95% CI |
|---|---|---|---:|---:|---|
| panel | `cognate_family=Gs` | continuous | 5 | **+1.309** | **[+0.281, +2.337]** |
| panel | `cognate_family=Gi` | continuous | 24 | −0.503 | [−1.432, +0.425] |
| panel | `cognate_family=Gq` | continuous | 10 | +0.052 | [−1.081, +1.185] |

And the dossier says all four were regressed —
`EXPERIMENT_DOSSIER_BLOCK_B.md` §6a:

> "Regressed against four predictors:
> 1. Δ_ref on NPxxY and Δ_ref on tilt.
> 2. Coupling promiscuity … **the discriminating predictor**.
> 3. Deposition count (from ref set, degenerate…).
> 4. **Cognate family (categorical Gs / Gi/o / Gq/11 / G12/13 / Gt).**"

So the dossier says four predictors were tested; the claim sheet and C-B-14 say
three; the fourth is in the shipped table; and one of its panel-level levels signs
at 95% CI on the continuous scale. `BLOCK_B_POSTFREEZE_CHECKS.md` Check 3 tightened
C-B-14's intro on the *deposition-count* predictor and did not touch cognate family.

**Reproduction.**
```
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/08_covariates/ladder_height_regressions.csv')
p=r[r.backbone=='panel']
print(p[p.predictor.str.startswith('cognate_family')][['predictor','outcome_scale','n_receptors_all','slope_all','ci_lo_all','ci_hi_all']].to_string(index=False))
print('CI excludes zero:', ((p.ci_lo_all>0)|(p.ci_hi_all<0)).sum(), 'panel rows')"
```

**Severity: highest. It reaches the reader and it inverts a headline negative.**
"No covariate predicts ladder height" is a claim about the whole analysis. The one
level that signs is n=5 and categorical, so it may well not deserve a sentence —
but that is a decision to disclose and defend, not to omit, and
`any_predictor_ci_excludes_zero=False` with `matches_claim_sheet_bool=True` is the
Block A self-certifying-column failure class firing again (see the correction to
D-B-2 below).

**What would close it.** Either (a) state in SC-B-11 and C-B-14 that a fourth,
categorical cognate-family predictor was regressed, that its Gs level (n=5,
continuous scale) has a panel CI excluding zero, and why that is not a
ladder-height covariate result; or (b) if cognate family was never intended as a
ladder-height covariate, say so in the dossier §6a and drop rows 72–79 from
`ladder_height_regressions.csv` or move them to a separate file.

---

## N-B-3 — AA2AR's +0.76 is called "the single largest per-receptor family term in the panel". Six cells are larger.

**The claim as shipped.** `caveats/C-B-8_aa2ar_standing_anomaly.md` §"Caveat":

> "- **Family term +0.76 on Boltz** (cognate 0.80 − shuffled 0.04) —
> the single largest per-receptor family term on any (receptor,
> backbone) cell in the Block B panel."

Repeated as the reader-facing sentence in the same file, §"Manuscript sentence":

> "> AA2AR is a standing anomaly in the campaign — the single largest
> per-receptor family term in the Block B panel (+0.76 on boltz;
> cognate 0.80 vs shuffled 0.04)."

And in `BLOCK_B_MANUSCRIPT_FLAGS.md` Flag B-11:

> "On Block B: family term +0.76 (boltz cognate 0.80 − shuffled 0.04) —
> the single largest per-receptor family term in the panel."

**What the data says.** Recomputing `cognate_rate − shuffled_rate` on every one of
the 160 (receptor × backbone) cells in `04_ladder/ladder_per_receptor.csv` — and
independently from `01_rows/rows_tidy.csv` under the two-instrument predicate —
AA2AR/boltz ranks **7th**:

| receptor | backbone | shuffled | cognate | family term |
|---|---|---:|---:|---:|
| DRD3 | chai | 0.00 | 1.00 | **+1.00** |
| AA1R | boltz | 0.00 | 1.00 | **+1.00** |
| NPY2R | chai | 0.02 | 1.00 | +0.98 |
| NPY1R | chai | 0.04 | 1.00 | +0.96 |
| NPY2R | of3 | 0.16 | 1.00 | +0.84 |
| ACM4 | of3 | 0.00 | 0.80 | +0.80 |
| AA2AR | boltz | 0.04 | 0.80 | +0.76 |

AA2AR's own row (0.02 / 0.00 / 0.04 / 0.80) reproduces exactly as C-B-8 states it —
the receptor's numbers are right, the superlative is not.

**Reproduction.**
```
python3 -c "
import pandas as pd
lp=pd.read_csv('data/block_b/04_ladder/ladder_per_receptor.csv')
lp['ft']=lp.cognate_rate-lp.shuffled_rate
print(lp.nlargest(7,'ft')[['receptor','backbone','shuffled_rate','cognate_rate','ft']].to_string(index=False))"
```

**Severity: high. It reaches the reader** — C-B-8 supplies the sentence verbatim,
and the AA2AR standing-anomaly line is Discussion material. The *argument* survives
(AA2AR is measurable because it is not ceiling-pinned); only the superlative fails.

**What would close it.** Replace "the single largest" with the true rank, or with
the defensible version: AA2AR is the largest family term among receptors that are
*not* saturated at cognate on the backbone in question. Note that the six larger
cells are all cognate = 1.00, i.e. ceiling-pinned, which is exactly C-B-7's point.

---

## N-B-4 — SC-B-12's direction-of-effect sentence attributes 327 partner contacts to the apo arm, which has no partner

**The claim as shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-12 claim:

> "Absolute counts on TM6 apex positions fall
> apo → shuffled → decoy (e.g. 6.33: 327 → 297 → 156), i.e. decoy makes
> fewer TM6-apex contacts even when engaged."

Repeated in `BLOCK_B_MANUSCRIPT_FLAGS.md` Flag B-15:

> "The decoy arm makes fewer TM6-apex contacts even when engaged (6.33 counts
> fall apo → shuffled → decoy: 327 → 297 → 156)."

**What the data says.** The contact register lives in
`06_interface/interface_continuous.csv` as `contact_register_last5_json` — the
register of receptor BW positions contacting *the terminal 5 partner residues*.
All 160 apo cells have an empty register, because apo rows carry no partner chain.
`data/block_b_structures/STRUCTURE_BUNDLE_MANIFEST.md` §5 says so explicitly:
*"(apo rows carry no partner chain — tip and contacts are undefined by
construction…)"*. Recomputed 6.33 counts:

| arm | cells with a non-empty register | 6.33 count |
|---|---:|---:|
| apo | **0 / 160** | **none** |
| cognate | 160 / 160 | **304** |
| shuffled | 160 / 160 | 297 ✓ |
| decoy | 160 / 160 | 156 ✓ |

So the second and third terms of the triple are right, the first names an arm that
structurally cannot contribute, and 327 reproduces nowhere (cognate is 304).

**Reproduction.**
```
python3 -c "
import pandas as pd,json,collections
c=pd.read_csv('data/block_b/06_interface/interface_continuous.csv')
for arm in ['apo','cognate','shuffled','decoy']:
    ct=collections.Counter()
    for s in c[c.arm==arm].contact_register_last5_json.dropna():
        for k,v in json.loads(s).items():
            for bw in v: ct[bw]+=1
    print(arm,'cells',len(c[c.arm==arm]),'6.33 =',ct.get('6.33'))"
```

**Severity: high. It reaches the reader** and it is the only *directional* sentence
in SC-B-12 — the sentence that carries the "engaged but not fully inserted"
mechanism reading (Flag B-15 says so). A reader who checks it finds a physically
impossible measurement.

**What would close it.** Confirm the intended first term. If it is cognate, the
triple is `cognate → shuffled → decoy: 304 → 297 → 156` and the monotone story
survives intact. If 327 has a source, name it.

---

## N-B-5 — SC-B-12 says its counts are restricted to engaged cells; they are not, and the restriction changes them

**The claim as shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-12:

> "**Numbers** (top BW positions by contact count; aggregated across 160
> engaged cells per arm)"

and, in the same claim:

> "**Exclusion set applied**: baseline. Restricted to engaged cells
> (tip < 20 Å) by construction."

Flag B-15 repeats: *"Across 160 engaged cells per arm…"*.

**What the data says.** `06_interface/interface_continuous.csv` has 160 cells per
arm but `cell_engaged_20 == True` on **160 cognate, 154 shuffled, 116 decoy** —
never 160 for every arm. The shipped counts reproduce over **all 160 cells**, not
over the engaged subset. Decoy, both ways:

| BW | SC-B-12 | all 160 decoy cells | engaged decoy cells (n=116) |
|---|---:|---:|---:|
| 3.50 | 227 | **227** ✓ | 223 |
| 8.47 | 212 | 211 | 211 |
| 6.36 | 171 | **171** ✓ | 167 |
| 6.33 | 156 | **156** ✓ | 152 |

Cognate and shuffled are unaffected (essentially every cell is engaged), which is
why the error hides.

**Reproduction.**
```
python3 -c "
import pandas as pd,json,collections
c=pd.read_csv('data/block_b/06_interface/interface_continuous.csv')
print(c.groupby('arm').cell_engaged_20.sum().to_dict())
for sub,lab in [(c,'ALL'),(c[c.cell_engaged_20==True],'ENGAGED')]:
    ct=collections.Counter()
    for s in sub[sub.arm=='decoy'].contact_register_last5_json.dropna():
        for k,v in json.loads(s).items():
            for bw in v: ct[bw]+=1
    print(lab, [(b,ct[b]) for b in ['3.50','8.47','6.36','6.33']])"
```

**Severity: high. It reaches the reader through the Methods**, and it is the
opposite of harmless: the claim's whole point is that decoy makes fewer TM6-apex
contacts *even when engaged*, and the counts shipped are not the engaged ones. The
qualitative conclusion holds on either filter; the stated filter does not match the
stated numbers.

**What would close it.** State which filter produced the table. If "even when
engaged" is load-bearing, ship the engaged-only counts (223 / 211 / 167 / 152 for
decoy) and the engaged cell counts per arm (160 / 154 / 116).

---

## N-B-6 — The dossier's headline ladder table gives different rungs *and* inadmissible CIs, and `claim_answers.csv` ships the same inadmissible CIs marked "matches"

**The claim as shipped.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §3d,
"**Ladder reproduction on frame_36 (n=36), binary panel predicate**":

> | Arm | Observed | Published | Cluster-boot 95% CI |
> | apo | 0.158 | 0.158 | [0.14, 0.18] |
> | decoy | 0.558 | 0.558 | [0.445, 0.664] |
> | shuffled | **0.810** | **0.810** | **[0.78, 0.84]** |
> | cognate | **0.892** | **0.892** | **[0.87, 0.91]** |

and `04_ladder/claim_answers.csv`:

```
SC-B-1,panel_apo_rate_frame36,0.158,0.14,0.18,ladder_four_scorings.csv,True
SC-B-1,panel_decoy_rate_frame36,0.558,0.51,0.60,ladder_four_scorings.csv,True
SC-B-1,panel_shuffled_rate_frame36,0.809,0.78,0.84,ladder_four_scorings.csv,True
SC-B-1,panel_cognate_rate_frame36,0.891,0.87,0.91,ladder_four_scorings.csv,True
```

**What the other documents and the data say.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-1,
`data/block_b_structures/02_ladder_arms/LADDER_FRAMING.md`, and the named source
file `04_ladder/ladder_four_scorings.csv` all agree on different numbers:

| arm | rate | cluster-boot 95% CI (shipped CSV) | dossier §3d / claim_answers |
|---|---:|---|---|
| apo | 0.1579 | [0.0809, 0.2564] | [0.14, 0.18] |
| decoy | 0.5579 | [0.4446, 0.6640] | [0.51, 0.60] (claim_answers) / [0.445, 0.664] (dossier) |
| shuffled | **0.8094** | [0.7468, 0.8693] | 0.810, [0.78, 0.84] |
| cognate | **0.8911** | [0.8381, 0.9424] | 0.892, [0.87, 0.91] |

Two things compound this. First, `BLOCK_B_POSTFREEZE_CHECKS.md` Check 2 §"Verdict"
says *"Every dossier/claim-sheet occurrence of `0.552` is corrected to `0.558` in
this pass"* — the decoy rung was corrected and the shuffled/cognate rungs were left
at the superseded dispatch values in the same table. Second, the decoy interval
`[0.51, 0.60]` in `claim_answers.csv` is the exact interval the drop elsewhere
orders everyone to disregard. `11_bootstrap_draws/ci_convention_audit_readme.md`:

> "The post-freeze report (r2) compared cluster-boot [0.445, 0.664] against
> a tighter [0.51, 0.60] and inferred '2× width ratio…'. Item 2 recomputation
> shows the tighter interval was row-boot (8000 decoy rows treated independent),
> NOT proper receptor-boot."

and `data/block_b/README.md` §"What a figure agent will get wrong… (post-freeze
update)" item 2:

> "Row-boot values (treating 50 rows per cell as 50 independent draws)
> are NOT admissible and give artificially tight CIs."

`claim_answers.csv` carries `matches_claim_sheet_bool = True` on all four rows.

**Reproduction.**
```
python3 -c "
import pandas as pd
f=pd.read_csv('data/block_b/04_ladder/ladder_four_scorings.csv')
print(f[(f.frame=='reproduction_36')&(f.backbone=='panel')][['arm','binary_predicate','cluster_boot_ci_lo_binary','cluster_boot_ci_hi_binary']].to_string(index=False))
print(open('data/block_b/04_ladder/claim_answers.csv').read().split('median')[0])"
```

**Severity: high. The CIs reach the reader.** The rungs differ by 0.001 and cannot
move a conclusion, but a Results table built from `claim_answers.csv` prints
intervals roughly a third the width of the authoritative ones, on the paper's
headline result, in a bundle that spends two documents insisting cluster-boot is
authoritative.

**What would close it.** Regenerate `04_ladder/claim_answers.csv` from
`ladder_four_scorings.csv`'s `cluster_boot_ci_*_binary` columns; correct dossier
§3d to 0.809 / 0.891 with the cluster-boot intervals; and state what
`matches_claim_sheet_bool` is actually comparing, since it is `True` here against a
value it does not match.

---

## N-B-7 — Two shipped files give two different cluster-boot CIs for SC-B-6's headline residual, and the claim sheet cites the file it did not use

**The claim as shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-6:

> "the tilt residual against each receptor's active reference is +0.024 Å
> with cluster-boot 95% CI **[-0.29, +0.30]**"

with **"Source CSV**: `donor_class_residuals_summary.csv` +
`phase5_power_analysis.csv`". Repeated as [-0.29, +0.30] in
`caveats/C-B-10_...md`, Flag B-4's manuscript sentence, `figures/BB-5_...md`,
`BLOCK_B_FOLLOWUP_E1_E4.md` §"Manuscript sentence", and
`07_donor_residuals/claim_answers.csv` (sourced to
`donor_class_residuals_summary.csv`).

**What the other document says.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §5.1–5.4:

> "    residual_tilt = +0.024 Å, cluster-boot 95% CI **[−0.31, +0.30]**  → indistinguishable from zero"

**What the data says.** Both are in the drop, in different files, for the same
statistic:

| file | panel Gs→Gi `residual_tilt` | ci_lo | ci_hi |
|---|---:|---:|---:|
| `07_donor_residuals/donor_class_residuals_summary.csv` | +0.023674 | **−0.306595** | +0.301001 |
| `07_donor_residuals/phase5_power_analysis.csv` (`all_*`) | +0.023674 | **−0.288306** | +0.299058 |

The claim sheet's −0.29 is the *power-analysis* value; it cites the *summary* file.
The dossier's −0.31 is the summary value. `claim_answers.csv` attributes −0.29 to
the summary file, which does not contain it.

**Reproduction.**
```
python3 -c "
import pandas as pd
s=pd.read_csv('data/block_b/07_donor_residuals/donor_class_residuals_summary.csv')
p=pd.read_csv('data/block_b/07_donor_residuals/phase5_power_analysis.csv')
print(s[(s.backbone=='panel')&(s.donor_ga_class=='Gs')&(s.cognate_ga_class=='Gi')&(s.axis=='residual_tilt')][['median','ci_lo','ci_hi']].to_string(index=False))
print(p[(p.backbone=='panel')&(p.donor_ga_class=='Gs')&(p.cognate_ga_class=='Gi')&(p.axis=='residual_tilt')][['all_median','all_ci_lo','all_ci_hi']].to_string(index=False))"
```

**Severity: high. It reaches the reader.** SC-B-6 is the Outcome-A claim, and the
CI is the entire claim — "signed with a CI spanning zero" is a statement about that
interval. Two intervals in one bundle, and the manuscript sentence is prescribed
"use verbatim" (`data/block_b/README.md` post-freeze item 5).

**What would close it.** Say which bootstrap produced which interval and which is
of record, and fix the `Source CSV` line in SC-B-6 and the `source_file` column in
`07_donor_residuals/claim_answers.csv`. The native-only figures (−0.062,
[−0.41, +0.21], n 24→20, 83.3%) reproduce exactly from `phase5_power_analysis.csv`
and are not in question.

---

## N-B-8 — W-B-4 is simultaneously withdrawn and not-a-withdrawal, in seven places

**The claim as shipped, side A.** `12_narrative/withdrawals/W-B-4_outcome_b_reads_partner_identity.md`,
title and body:

> "# W-B-4 — MOVED to SC-B-14 (post-freeze reclassification, 2026-09-10)
> …
> **No withdrawn claim remains under number W-B-4.**"

`BLOCK_B_POSTFREEZE_CHECKS.md` Check 4 §"Verdict — MOVE" and
`withdrawals/README.md` agree, and `BLOCK_B_CLAIM_SHEET.md` § SC-B-14 says:

> "This is a signed test result on a pre-registered alternative, not a
> retracted claim; it lives on the claim sheet rather than in
> withdrawals."

**The claim as shipped, side B — seven surviving live references.**

1. `BLOCK_B_CLAIM_SHEET.md` §"Withdrawn claims (see `withdrawals/`)":
   *"- **W-B-4** — Outcome B ("model reads partner identity on continuous axis")"* —
   listed without qualification, four lines above SC-B-14's own footnote.
2. `BLOCK_B_CLAIM_SHEET.md` § SC-B-6 "Qualified by":
   *"W-B-4 (Outcome B withdrawn)"*.
3. `caveats/C-B-10_reference_bias_caveat_does_not_localise.md` §"Affects":
   *"- W-B-4 (Outcome B withdrawn)."*
4. `figures/BB-5_donor_class_residuals.md` §"Qualified by":
   *"W-B-4 (Outcome B withdrawn)"*.
5. `withdrawals/W-B-3_gs_to_gq_third_finding_manuscript_line.md` §"Related":
   *"- Not related to W-B-4: Outcome B is withdrawn on the Gs → Gi cell
   (bulk-only reading)…"*
6. `BLOCK_B_MANUSCRIPT_FLAGS.md` Flag B-4 §"Related": *"SC-B-6, C-B-10, W-B-3, W-B-4."*
7. `EXPERIMENT_DOSSIER_BLOCK_B.md` §Cross-cutting item 3:
   *"**Continuous residual axis: Outcome A signed, firmed by native-only power
   analysis** (SC-B-6, W-B-4)."*

**Reproduction.**
```
grep -rn "W-B-4" data/block_b --include='*.md'
```

**Severity: high, and it is the one contradiction the bundle is *most* exposed on.**
`withdrawals/README.md` itself says: *"Retractions are load-bearing for
credibility. Reviewers who see a paper that never withdraws anything have a
different reaction than reviewers who see a paper with a transparent retraction
ledger."* A retraction ledger that cannot say whether an entry is a retraction is
worse than none. It also reaches the reader directly: SC-B-14 and SC-B-6 are both
manuscript claims, and the "Withdrawn claims" list is the ledger a reviewer reads.

**What would close it.** Sweep the six stale pointers to `SC-B-14`, and annotate
the claim sheet's "Withdrawn claims" list entry the way `withdrawals/README.md`
already does.

---

## N-B-9 — C-B-7's top-5 per-receptor family terms reproduce nowhere, and BB-6 tells the figure agent to print them as value labels

**The claim as shipped.** `caveats/C-B-7_ceiling_pinning_on_family_term.md`,
"**Top 5 receptors by boltz family term**":

> | receptor | shuffled | cognate | Δp |
> | NPY2R | 0.30 | 0.98 | 0.68 |
> | NPY1R | 0.66 | 0.94 | 0.28 |
> | OX2R | 0.79 | 0.99 | 0.20 |
> | DRD3 | 0.78 | 0.98 | 0.20 |
> | ACM4 | 0.79 | 0.98 | 0.19 |
>
> "All 5 have shuffled < 0.85, i.e. the ceiling has room."

`figures/BB-6_per_receptor_ladder.md` Panel F.ii instructs:

> "- Value labels for the top 5 non-saturated: NPY2R (+0.68),
> NPY1R (+0.28), OX2R (+0.20), DRD3 (+0.20), ACM4 (+0.19)."

and Flag B-9 repeats the same five pairs.

**What the data says.** `04_ladder/ladder_per_receptor.csv`, boltz rows — none of
the five shuffled/cognate pairs exists, and four of the five receptors are
ceiling-pinned at cognate on boltz, i.e. the "ceiling has room" statement is false
for them:

| receptor | boltz shuffled | boltz cognate | Δp | ceiling_pinned |
|---|---:|---:|---:|---|
| NPY2R | **1.00** | 1.00 | **0.00** | True |
| NPY1R | **0.98** | 1.00 | **0.02** | True |
| OX2R | **0.90** | 1.00 | **0.10** | True |
| DRD3 | **1.00** | 0.92 | **−0.08** | False |
| ACM4 | **0.98** | 1.00 | **0.02** | True |

The five *values* (0.68 / 0.28 / 0.20 / 0.20 / 0.19) are close to the **panel-mean
across four backbones** for NPY2R / NPY1R / OX2R / DRD3 / ACM4 — 0.455 / 0.270 /
0.250 / 0.245 / 0.205 — but not equal to them either. On the panel mean the
correct top five are NPY2R 0.455, NPY1R 0.270, OX2R 0.250, DRD3 0.245, ACM4 0.205.

**Reproduction.**
```
python3 -c "
import pandas as pd
lp=pd.read_csv('data/block_b/04_ladder/ladder_per_receptor.csv')
b=lp[lp.backbone=='boltz'].set_index('receptor')
print(b.loc[['NPY2R','NPY1R','OX2R','DRD3','ACM4'],['shuffled_rate','cognate_rate','ceiling_pinned']])
lp['ft']=lp.cognate_rate-lp.shuffled_rate
print(lp.groupby('receptor').ft.mean().nlargest(5))"
```

**Severity: high. It reaches the reader as printed value labels on a main panel.**
BB-6 Panel F.ii is a per-receptor bar chart with these five annotated, and F.ii's
whole rhetorical job is "the family term lives in the unsaturated cells" — the
table shipped to make that point consists of saturated cells.

**What would close it.** Name the aggregation C-B-7's table uses and re-derive it,
or replace it with the boltz-only top five from
`ladder_per_receptor.csv`. Note this collides with C-B-8's own rule: *"never quote
AA2AR's family term without naming the aggregation"* — the same discipline is not
applied to C-B-7's table.

---

## N-B-10 — Ceiling- and floor-pinned counts per backbone: dossier vs caveat vs figure spec vs data

**The claim as shipped.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §3f:

> "Ceiling-pinned counts (cognate ≥ 0.98): Boltz 34, Chai 24, OF3 30, Protenix 33
> out of 40. Floor-pinned counts (apo ≤ 0.02): Boltz 25, Chai 33, OF3 32,
> Protenix 31."

**What the other documents say.** `caveats/C-B-7_...md` and
`figures/BB-6_...md` Panel F.iii both give:

> | backbone | ceiling_pinned / 40 | floor_pinned / 40 |
> | boltz | **29** | 31 |
> | chai | **28** | 27 |
> | of3 | **24** | 25 |
> | protenix | **34** | 36 |

**What the data says.** The C-B-7 / BB-6 table is correct — it reproduces exactly
from the shipped `ceiling_pinned` / `floor_pinned` flags and independently from the
raw rates. The dossier's numbers match no backbone.

**Reproduction.**
```
python3 -c "
import pandas as pd
lp=pd.read_csv('data/block_b/04_ladder/ladder_per_receptor.csv')
print(lp.groupby('backbone')[['ceiling_pinned','floor_pinned']].sum())
lp['c']=lp.cognate_rate>=0.98; lp['f']=lp.apo_rate<=0.02
print(lp.groupby('backbone')[['c','f']].sum())"
```

**Severity: high — BB-6 Panel F.iii is a shipped table**, and the drop's own
summary range "24–34 of 40" is true of both sets, so the disagreement is invisible
unless a panel prints per-backbone. A figure printing the dossier's numbers next to
a caption citing C-B-7 contradicts itself on the page.

**What would close it.** Correct dossier §3f to 29 / 28 / 24 / 34 and 31 / 27 / 25 / 36.

---

## N-B-11 — Engaged-but-inactive counts per backbone: the dossier's four numbers do not sum to its own pooled total

**The claim as shipped.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §4b:

> "**Engaged-but-inactive floor per backbone on decoy arm**: n = 278–540
> (Boltz 540, Chai 306, OF3 458, Protenix 278)."

540 + 306 + 458 + 278 = **1,582**, against the pooled 1,699 the same document,
SC-B-3, and `claim_answers.csv` all state.

**What the other documents and the data say.**
`figures/BB-3_2x2_engagement_activation.md` §Annotations:

> "- Engaged-but-inactive n for decoy arm per backbone: boltz 464, chai
> 417, of3 540, protenix 278 (pooled 1,699 in frame_36; 2,234 in frame_40)."

464 + 417 + 540 + 278 = 1,699 ✓, and this reproduces exactly from
`06_interface/interface_2x2.csv` at `frame_36 / two_instrument / cutoff_A == 20`:
boltz 464, chai 417, of3 540, protenix 278, `panel_all` 1699.

**Reproduction.**
```
python3 -c "
import pandas as pd
i=pd.read_csv('data/block_b/06_interface/interface_2x2.csv')
s=i[(i.frame=='frame_36')&(i.predicate=='two_instrument')&(i.cutoff_A==20)&(i.arm=='decoy')]
print(s[['backbone','n_engaged_but_inactive']].to_string(index=False))"
```

**Severity: high — this is the mechanism-claim cell.** SC-B-3 calls it "the
mechanism-claim cell" and BB-3 prints the per-backbone n in the panel. A reader who
adds up the dossier's four numbers finds they miss the stated pooled total by 117.

**What would close it.** Correct dossier §4b to boltz 464 / chai 417 / of3 540 /
protenix 278.

---

# TIER 2 — would reach a figure, a caption, or a Methods line

## N-B-12 — AA2AR is anomalous in "three separate analyses" and in "five appearances", in the same bundle — and the dispatch asks for one

**Side A — three.** `caveats/C-B-8_aa2ar_standing_anomaly.md`, opening line:

> "AA2AR is called anomalous across **three** separate analyses in this campaign."

`BLOCK_B_MANUSCRIPT_FLAGS.md` Flag B-11: *"AA2AR is called anomalous across three
separate analyses across the campaign."*
`10_exclusions/exclusion_definitions.csv`, `excl_E_B_3` rationale: *"Recurrently
anomalous across three separate analyses; excluded from pooled inference on
family-term slope where AA2AR alone drives the slope."*

**Side B — five.** `data/block_b/README.md` §"What a figure agent will get wrong…"
item 7:

> "7. **AA2AR is recurrently anomalous but the five appearances are
> independent, not a single structural cause.** … Report AA2AR-included and
> AA2AR-excluded numbers side by side for pooled inferences (C-B-8), but do not
> collapse the five appearances into one footnote — they need separate wording."

`12_narrative/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md` §3 enumerates them —
*"Block A anti-calibration; Block C bimodality; Block B family-term +0.76 on Boltz;
ladder-height covariate slope driver; E1 ruler fragility"* — and concludes:

> "The five anomalies remain independent. **They need separate footnotes.**"

`data/block_b_structures/STRUCTURE_BUNDLE_MANIFEST.md` §1 §4.1:
*"3. **E-B-3** AA2AR (five unexplained anomalies)."*

**Side C — one.** The closeout dispatch relayed to this session (not present on
disk in this working tree — quoted as supplied by the orchestrator) says: *"AA2AR
gets exactly one consolidated mention… Do not scatter it across five places
implying five causes."*

So the bundle carries two counts of its own, and the dispatch carries a third
instruction that directly negates the drop README's *"do not collapse the five
appearances into one footnote"*. The drop README and the dispatch cannot both be
followed.

**Reproduction.**
```
grep -rn "three separate analyses\|five appearances\|five unexplained\|five anomalies" \
  data/block_b data/block_b_structures --include='*.md' --include='*.csv'
```

**Severity: medium-high. It reaches the reader as footnote structure**, which is a
visible editorial choice: one footnote vs five changes how a reviewer reads the
recurrence. Note that Item 3 is the *later* document and that its verdict —
"NOT SUPPORTED", the anomalies do not share a structural cause — is the reason the
count grew and the reason the drop README argues for separate wording. The
dispatch's instruction is the one that would need to be overridden, or the two need
reconciling by whoever owns the manuscript.

**What would close it.** Adjudicate: one consolidated mention or five. Then update
C-B-8, Flag B-11 and `exclusion_definitions.csv` (which still say three) so the
bundle carries one count.

---

## N-B-13 — POSTFREEZE Check 1 says the Gs→Gi cell has 19 native receptors; everything else says 20

**The claim as shipped.** `BLOCK_B_POSTFREEZE_CHECKS.md` Check 1, §"Family
grouping and per-family tilts":

> "**Gi group composition (n=24)**: **19 native** + 3 mini-G + 2 agonist-only.
> Native-dominated; the median 17.518 Å is on native transducer complexes."

**What the other documents and the data say.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-6:
*"Restricted to the **20** receptors whose active reference is native"*;
`caveats/C-B-10_...md`: *"**The manuscript-load-bearing Gs→Gi cell is 83.3%
native-anchored** (20 of 24 receptors…)"*; `BLOCK_B_FOLLOWUP_E1_E4.md` §E1c native
stratum: *"| Gi | **20** | 20 | 17.518 |"*. And
`07_donor_residuals/phase5_power_analysis.csv` panel Gs→Gi `residual_tilt`:
`total_n_rec = 24, native_n_rec = 20, chimera_n_rec = 4`.

Check 1's own arithmetic sums to 24 (19+3+2), so the error is a mis-split, not a
transcription slip — and it puts the native fraction at 79.2% instead of 83.3%.

**Reproduction.**
```
python3 -c "
import pandas as pd
p=pd.read_csv('data/block_b/07_donor_residuals/phase5_power_analysis.csv')
print(p[(p.backbone=='panel')&(p.donor_ga_class=='Gs')&(p.cognate_ga_class=='Gi')][['axis','total_n_rec','native_n_rec','chimera_n_rec']].to_string(index=False))"
```

**Severity: medium. It reaches the reader only via the 83.3% figure**, which is
quoted in C-B-10's manuscript sentence and BB-5's callout. Check 1 is a
supporting document, but it is the one the claim sheet points at for the SC-B-6
post-freeze note, so a reader who follows the pointer finds a different denominator.

**What would close it.** Correct Check 1 to 20 native + 2 mini-G + 2 agonist-only
(or whatever the true split is) and confirm the 4 non-native members.

---

## N-B-14 — The post-run inactive-reference preload check names three Block B receptors; CCR5 is a fourth

**The claim as shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-13 "Preload check":

> "the 6 inactive references added post-run (AA2AR/5MZP,
> ADA1A/7YMJ, ADRB2/2RH1, ADRB2/3NYA, **CCR5/4MBS**, CNR1/5TGZ) are all
> secondary; the primary inactive references for **the 3 Block B receptors**
> in the list (AA2AR/5NM4, ADRB2/6PS2, CNR1/5U09) were present in `6ee2cad8`"

Repeated in `caveats/C-B-9_...md` §"Preload check — the three Block B receptors
that gained an inactive ref" (a three-row table: AA2AR, ADRB2, CNR1), Flag B-6
(*"Three receptors in the Block B 40 (AA2AR, ADRB2, CNR1)"*),
`data/block_b/README.md` §Known gaps (*"the three Block B receptors"*), and the
dossier §6c.

**What the data says.** CCR5 is in the Block B 40 — it is in the dossier's own
panel list (§"Panel of record", line: *"…CCKAR, **CCR5**, CNR1, CNR2, CXCR2…"*)
and in all 32,000 rows of `01_rows/rows_tidy.csv`. ADA1A is *not* in the panel
(ADA2A is a different receptor). So four Block B receptors gained a post-run
inactive reference, not three, and CCR5 was never checked. CCR5's primary inactive
in `09_references/reference_audit.csv` is **5UIW**, present in the pinned set — so
the *conclusion* survives; the enumeration and the check do not.

**Reproduction.**
```
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',usecols=['receptor_slug'])
recs=set(r.receptor_slug)
for x in ['AA2AR','ADA1A','ADRB2','CCR5','CNR1']: print(x, x in recs)
a=pd.read_csv('data/block_b/09_references/reference_audit.csv')
print(a[(a.receptor=='CCR5')][['receptor','role','pdb_id','active_stabilization_source']].to_string(index=False))"
```

**Severity: medium. It reaches the reader through a Methods provenance sentence**
(C-B-9's manuscript sentence asserts *"none of the six shifts the primary inactive
reference of any Block B receptor"* — a claim about all of them, verified on three
quarters of them).

**What would close it.** Add CCR5/5UIW to the preload table in C-B-9, SC-B-13,
Flag B-6 and the drop README, and change "three" to "four".

---

## N-B-15 — C-B-14 labels every regression "all 40"; four of the six ran on 28–34 receptors

**The claim as shipped.** `caveats/C-B-14_no_covariate_slope_excludes_zero.md`
opens *"Regressed per-receptor family term (two scales) against three testable
predictors **on the 40 Class A receptors**"*, its table column header is
**`slope (all 40)`**, and its manuscript sentence begins *"On the 40-receptor Block
B panel…"*.

**What the other document and the data say.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-11
ships the same six slopes *with* an `n` column: 28, 34, 32, 40, 32, 40. That
matches `08_covariates/ladder_height_regressions.csv` `n_receptors_all` exactly.
`08_covariates/ladder_height_covariates.csv` explains it: `family_term_continuous`
is non-null on only 32 of 40 receptors.

**Reproduction.**
```
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/08_covariates/ladder_height_regressions.csv')
p=r[(r.backbone=='panel')&(r.predictor.isin(['delta_ref_npxxy','delta_ref_tilt','n_ga_families']))]
print(p[['predictor','outcome_scale','n_receptors_all']].to_string(index=False))"
```

**Severity: medium. It reaches the reader** — C-B-14's manuscript sentence is
written to be used, and "on the 40-receptor Block B panel" over-states the n on
two-thirds of the rows. This also compounds N-B-2: an under-powered regression
described as full-panel is exactly where an omitted signing predictor hides.

**What would close it.** Rename the column to `slope` and carry SC-B-11's `n`
column into C-B-14; change the manuscript sentence to name the per-predictor n.

---

## N-B-16 — BB-1 instructs the figure agent to draw the superseded dispatch ladder on the primary panel

**The claim as shipped.** `figures/BB-1_ladder_binary_predicate.md`, Panel A.i:

> "- Annotate dispatch cite (0.158 / 0.552 / 0.810 / 0.892) at panel row
> as reference dashes."

three lines above §Annotations:

> "- Panel value labels above each error bar on panel row: 0.158, 0.558,
> 0.809, 0.891."

**What the other documents say.** `data/block_b/README.md` post-freeze item 1:

> "1. **Decoy panel rate is 0.558, not 0.552.** The older 0.552 appears in
> superseded documents (dispatch prompt, some Phase 3 report cites) and
> is a pre-consolidation snapshot value. Canonical on-corpus: 0.558."

`BLOCK_B_POSTFREEZE_CHECKS.md` Check 2: *"Every dossier/claim-sheet occurrence of
`0.552` is corrected to `0.558` in this pass."* The figure specs were not swept.
The other survivor is `withdrawals/W-B-2_midpoint_ladder_28_receptor.md`, which
states the superseded ladder as if live:

> "as a companion to the panel-binary-predicate ladder 0.158 / 0.552 /
> 0.810 / 0.892."

**Reproduction.**
```
grep -rn "0\.552\|0\.810\|0\.892" data/block_b --include='*.md' | grep -v POSTFREEZE
```

**Severity: medium-high. It would reach the reader as ink on the main ladder
panel** — two ladders, 0.006 apart, one of them a value the drop README calls a
different corpus's snapshot, with no stated purpose beyond "reference dashes".

**What would close it.** Delete the dispatch-cite annotation from BB-1, or state
why a superseded value belongs on a published panel. Correct W-B-2's opening
paragraph to the canonical rungs.

---

## N-B-17 — SC-B-12, BB-4 and `claim_answers.csv` all name the wrong file for the contact register

**The claim as shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-12:

> "**Dossier**: `§Phase 4a`. **Source CSV**: `interface_pif_connector.csv`
> (BW register JSON per cell)."

`figures/BB-4_pif_connector_engaged_but_inactive.md` §"Data source" lists, among
the columns of `interface_pif_connector.csv`, *"`bw_register` (JSON)"*.
`06_interface/claim_answers.csv` sources all three SC-B-12 rows to
`interface_pif_connector.csv`.

**What the data says.** `06_interface/interface_pif_connector.csv` has 12 columns
and no register: `receptor_slug, arm, backbone, pif_d_5_50_3_40_ca,
pif_d_3_40_6_44_ca, pif_sum_ca, npxxy_median, tilt_median, tip_median, cell_active,
cell_engaged_20, cell_engaged_but_inactive`. The register is
`contact_register_last5_json` in `06_interface/interface_continuous.csv`.

**Reproduction.**
```
python3 -c "
import pandas as pd
print([c for c in pd.read_csv('data/block_b/06_interface/interface_pif_connector.csv',nrows=1).columns])
print([c for c in pd.read_csv('data/block_b/06_interface/interface_continuous.csv',nrows=1).columns if 'regist' in c])"
```

**Severity: medium. It stops a verification rather than producing a wrong number** —
but it is the reason SC-B-12 reads as unverifiable, and the answer-beside-data
discipline the drop README prescribes ("Recompute from the tidy source and diff
against these") fails on the first step for this claim.

**What would close it.** Point SC-B-12, BB-4 and `06_interface/claim_answers.csv`
at `interface_continuous.csv` / `contact_register_last5_json`.

---

## N-B-18 — BB-3's stated filter returns zero rows, and FIGURE_BRIEF gives a different one

**The claim as shipped.** `figures/BB-3_2x2_engagement_activation.md`
§"Data source":

> "Filter to `frame == "reproduction_36" AND predicate == "two_instrument"
> AND cutoff_angstrom IN (14, 20)`."

with the column list *"`frame`, `predicate`, `cutoff_angstrom`, `arm`,
`backbone`, `p_engaged`, `p_engaged_ci_lo`, `p_engaged_ci_hi`,
`p_active_given_engaged`, `p_active_given_engaged_ci_lo`,
`p_active_given_engaged_ci_hi`, `n_engaged_but_inactive`, `n_active_engaged`."*

**What the other document says.** `data/block_b/FIGURE_BRIEF.md` § BB-3:

> "- `06_interface/interface_2x2.csv` — primary; filter `predicate ==
> "two_instrument" AND cutoff_A == 20.0 AND frame == "frame_36" AND backbone ==
> "panel_all"` for the headline row."

**What the data says.** `interface_2x2.csv` uses `frame ∈ {frame_36, frame_40}` and
the column is `cutoff_A`. BB-3's filter selects **0 of 480 rows**. Of BB-3's twelve
named columns, six do not exist (`cutoff_angstrom`, `p_engaged_ci_lo/hi`,
`p_active_given_engaged_ci_lo/hi`, `n_active_engaged`) — and `n_active_engaged` has
no equivalent under any name, so Panel C.i's per-cell annotation cannot be built
from this file. The same rename problem, without the empty-result consequence,
affects BB-1 (`binary_predicate_mean`, `binary_predicate_ci_lo/hi`, `logit` →
`binary_predicate`, `cluster_boot_ci_lo/hi_binary`, `logit_active_fraction`),
BB-2 (`estimate`, `share` → `term_estimate`, `term_share`), BB-4 (`receptor`,
`pif_*_median`, `cell_active_predicate` → `receptor_slug`, `pif_d_*`,
`cell_active`) and BB-6 (`apo_to_decoy` etc. → `delta_apo_to_decoy`).
Note `reproduction_36` *is* correct for `ladder_four_scorings.csv` and
`ladder_decomposition.csv` — the two families of files use different frame labels,
which is the underlying trap.

**Reproduction.**
```
python3 -c "
import pandas as pd
i=pd.read_csv('data/block_b/06_interface/interface_2x2.csv')
print('BB-3 filter rows:', len(i[(i.frame=='reproduction_36')]))
print('frames:', sorted(i.frame.unique()), '| cutoff col:', 'cutoff_A' in i.columns)"
```

**Severity: medium. It costs a figure agent an hour, and it is the class of defect
that gets "fixed" by guessing** — which is how a panel ends up on frame_40 or at a
14 Å cutoff without anyone noticing, against C-B-5 and C-B-6.

**What would close it.** Regenerate the figure specs' column lists and filters from
the shipped headers, or unify the frame labels across the two file families.

---

## N-B-19 — BB-2's per-backbone family-term labels are in the wrong order

**The claim as shipped.** `figures/BB-2_ladder_decomposition_both_scales.md`,
Panel B.ii — x-axis declared as *"backbone ∈ {boltz, chai, of3, protenix}"* — then:

> "- Annotate protenix probability CI crossing zero as a **ceiling
> artefact** callout (magnitude labels: prob 0.024 / 0.089 / 0.148 /
> 0.066; logit 0.35–1.05 for protenix, panel 0.39–1.09)."

**What the claim sheet says.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-2:

> "**Per-backbone probability family term**: boltz 0.066, chai 0.089, of3
> 0.148, protenix 0.024."

In the spec's own x-axis order the labels read boltz 0.024 and protenix 0.066 —
boltz and protenix transposed. This is not cosmetic: the same bullet asks for
protenix to be called out as the ceiling artefact, and under the printed order the
callout lands on the largest of the four rather than the smallest.

**Reproduction.**
```
python3 -c "
import pandas as pd
d=pd.read_csv('data/block_b/05_decomposition/ladder_decomposition.csv')
print(d[(d.frame=='reproduction_36')&(d.scale=='probability')&(d.contrast.str.startswith('delta_correct_family'))][['backbone','term_estimate','ci_lo','ci_hi']].to_string(index=False))"
```

**Severity: medium. It silently produces the wrong figure** — the D-B-1 severity
class. Four numbers, correct set, wrong assignment, no error message.

**What would close it.** Write the labels as `backbone: value` pairs in BB-2.

---

## N-B-20 — BB-1 and FIGURE_BRIEF point at a bootstrap-draws file that cannot supply per-arm ladder CIs

**The claim as shipped.** `data/block_b/FIGURE_BRIEF.md` § BB-1:

> "- `05_decomposition/ladder_decomposition_bootstrap_draws.csv` — cluster-boot
> draws for CI shading."

`figures/BB-1_...md` §"Data source" hedges the same pointer:
*"Bootstrap draws (for CI): `ladder_decomposition_bootstrap_draws.csv`
carries panel-level draws; per-arm CIs on `binary_predicate_mean`
are already stored in `ladder_four_scorings.csv`."*

**What the data says.** That file's columns are
`draw_id, backbone, frame, contrast, scale, term_estimate` — three *contrasts*
(apo→decoy, decoy→shuffled, shuffled→cognate), no `arm` column and no binary-rate
draws. There is no per-arm ladder draw anywhere in the drop; the only per-arm
intervals are the stored `cluster_boot_ci_*_binary` columns.

**Reproduction.**
```
python3 -c "
import pandas as pd
d=pd.read_csv('data/block_b/05_decomposition/ladder_decomposition_bootstrap_draws.csv',nrows=5)
print(list(d.columns)); print(d.contrast.unique() if 'contrast' in d else '')"
```

**Severity: medium — CI shading on BB-1 cannot be built as specified.**

**What would close it.** Either ship per-arm binary-rate draws or correct
FIGURE_BRIEF to point at the stored intervals, as BB-1 itself already does.

---

## N-B-21 — Two documents enumerate "the three 94% referents" and list different sets

**Side A.** `BLOCK_B_MANUSCRIPT_FLAGS.md` Flag B-17: *"Three "94%" referents
surfaced on grep:"* — (1) Block A protenix cognate 94.4%; (2) Block A cognate
normalised position ~94%; (3) the dispatch-plan "Block A shuffled 94%"
misattribution. `withdrawals/W-B-5_...md` ships the same three as a table.

**Side B.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §3g, *"Three referents identified;
naming which each is:"* — (1) **"0.810 — panel-wide absolute shuffled rate on Block
B, load-bearing"**; (2) 94.4% Block A protenix cognate; (3) **E1's 94%, "from a
first-era corpus retired for six measurement artifacts"**.

The two "three" lists share exactly one member. The dossier's list additionally
carries the superseded 0.810 (see N-B-6) as a live load-bearing number, and treats
E1's 94% as one of the three while Flag B-17 keeps it outside the three as
"UNVERIFIED, not closed".

**Reproduction.**
```
grep -n "94" data/block_b/12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md | sed -n '1,12p'
sed -n '392,418p' data/block_b/12_narrative/BLOCK_B_MANUSCRIPT_FLAGS.md
```

**Severity: medium. The manuscript action is "attribute every 94% cite
explicitly"** (Flag B-17), and the two enumerations give different attribution maps.

**What would close it.** One list. If there are four referents, say four.

---

## N-B-22 — "~40% chimera/mini-G" and "37.5% non-native" are treated as the same number; they are not the same set

**The claim as shipped.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §5.6 (recorded as the
verbatim pre-hoc Phase 5 caveat):

> "~40% of Block B active references are **chimera/mini-G donors** (mostly
> Gs-tagged)."

and §6c reconciles it: *"25 native + 15 non-native active references = **37.5%
non-native** (matches Phase 5 §5.6 "~40%")."*

**What the data says.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-13 and
`09_references/reference_audit.csv` break the 15 down as **10** chimera-or-miniG,
**3** nanobody-stabilised, **2** agonist-only-no-partner. Chimera/mini-G alone is
10/40 = **25%**, not ~40%. The 37.5% figure — which C-B-10 carries into a
manuscript sentence — is the non-native total, a different and broader category
than the §5.6 caveat was written about.

**Reproduction.**
```
python3 -c "
import pandas as pd
a=pd.read_csv('data/block_b/09_references/reference_audit.csv')
act=a[a.role=='active']
print(act.activation_class.value_counts().to_dict())
print('chimera/miniG frac', (act.activation_class=='Ga-complexed-chimera-or-miniG').mean())"
```

**Severity: medium. It reaches the reader** through C-B-10's Limitations sentence
(*"37.5% of Block B active references are non-native"*) presented as the same
caveat Phase 5 recorded about chimera/mini-G donors. The reference-bias mechanism
§5.6 describes — a chimeric α5 donor producing a family-atypical opening — does not
apply the same way to a nanobody-stabilised or agonist-only reference.

**What would close it.** State both numbers with their categories: 25% chimera or
mini-G, 37.5% non-native by any route, and say which one the reference-bias caveat
is about.

---

## N-B-23 — The structure bundle tells the figure agent GHSR's cognate cell is "4 Å looser" than panel; it is 0.39 Å

**The claim as shipped.** `data/block_b_structures/STRUCTURE_BUNDLE_MANIFEST.md`
§7 item 2:

> "the median-tip C1 pick (12.58 Å tip) is exactly the cell median,
> which is **4 Å looser** than the panel cognate median (12.19 Å per
> SC-B-3). GHSR's cognate cell tips **slightly** looser than panel — again
> a receptor-specific characteristic, not a selection artefact."

12.58 − 12.19 = **0.39 Å**. The sentence contradicts itself in consecutive clauses
("4 Å looser" / "slightly looser"), and "4" appears to be a corruption of the "4×"
in `caveats/C-B-6_...md`: *"The 20 Å tip-to-R3.50 Cα engagement cutoff … is 4× the
median cognate tip depth (12.19 Å…)"*.

**Reproduction.** Arithmetic; the two inputs are quoted above. Cross-check
12.19 against `06_interface/interface_continuous.csv`:
```
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_b/06_interface/interface_continuous.csv')
print('panel cognate tip median', c[c.arm=='cognate'].tip_median.median())"
```

**Severity: medium. §7 is the section a caption writer reads** — it is titled
"Cases where the selected representative does not visually match the claim it
illustrates", and a caption saying the C1 structure sits 4 Å off panel is both
wrong and self-defeating for a bundle that is otherwise careful about
representativeness (see D-B-5).

**What would close it.** "0.39 Å looser".

---

## N-B-24 — Dossier §3f's top-five family-heavy receptors are a panel-mean list with no aggregation named, and one member is wrong on that aggregation too

**The claim as shipped.** `EXPERIMENT_DOSSIER_BLOCK_B.md` §3f:

> "- Family-heavy: NPY2R +0.45, NPY1R +0.27, OX2R +0.25, DRD3 +0.24, AA2AR +0.19
> (Phase 3 §3f cite; AA2AR is +0.76 on Boltz alone per Phase 6a…)"

**What the data says.** Those values are the **panel mean across four backbones**,
which reproduces to two decimals — but the fifth largest on that aggregation is
**ACM4 at +0.205**, ahead of AA2AR at +0.190. Meanwhile C-B-7 and BB-6 ship a
*boltz-only* top five with different values and ACM4 in fifth (see N-B-9). Neither
the dossier list nor C-B-7's table names its aggregation, against C-B-8's own rule:
*"never quote AA2AR's family term without naming the aggregation."*

**Reproduction.**
```
python3 -c "
import pandas as pd
lp=pd.read_csv('data/block_b/04_ladder/ladder_per_receptor.csv')
lp['ft']=lp.cognate_rate-lp.shuffled_rate
print(lp.groupby('receptor').ft.mean().nlargest(7))"
```

**Severity: medium. It reaches BB-6's Panel F.ii**, which is instructed to
cross-reference this list against C-B-7's — *"Note: AA2AR (+0.76 in Phase 6a,
boltz; not from Phase 3f cite of +0.19 — see Flag B-11 for the discrepancy)"* —
and Flag B-11 does not carry that reconciliation; it is in C-B-8 and POSTFREEZE
Check 3.

**What would close it.** Name the aggregation on both lists, fix the fifth member,
and repoint BB-6's note at C-B-8.

---

# TIER 3 — bookkeeping, provenance, and pointers; would not reach the reader

## N-B-25 — The bundle names four different baselines and says the freeze tag does not exist yet

- `data/block_b/README.md` §"Corpus provenance": *"Repo: `paper_af3` @ commit
  `04531b8328ea4a71714a1b9ed7629736ec16f55a`. Freeze tag: `block_b_freeze` —
  **PENDING** (annotated after this zip lands)."*
- `BLOCK_B_POSTFREEZE_CHECKS.md` header: *"**Baseline**: `block_b_freeze` at
  `d6c1bef`"*, and §"Tag convention" creates `block_b_freeze_r2`.
- `BLOCK_B_FOLLOWUP_E1_E4.md` header: *"**Baseline**: `block_b_freeze_r3` at
  `7036a4a`."*
- `data/block_b_structures/STRUCTURE_BUNDLE_MANIFEST.md` header: *"**Baseline**:
  paper_af3 tag `block_b_final` at `c237120` (origin/main)."*
- `EXPERIMENT_DOSSIER_BLOCK_B.md` §Freeze: *"Tag `block_b_freeze` **will be**
  annotated on the HEAD after this dossier + companion files land."*

The README's "PENDING" is false against three documents shipped in the same zip,
and no document states which commit the shipped narrative corresponds to.
**Reproduction**: `grep -rn "block_b_freeze\|block_b_final\|Baseline" data/block_b
data/block_b_structures --include='*.md'`.
**Severity: low for the reader, medium for us** — we cannot pin what we are
citing. **Closes with**: one line in the drop README naming the tag and commit the
zip was cut from.

## N-B-26 — Object counts are stale in three index documents

- `data/block_b/README.md` §"Answer-beside-data discipline (**13** SC-B claims)"
  and its claim→directory table lists SC-B-1..SC-B-13. SC-B-14 exists, is a
  surviving claim, and has no directory and no `claim_answers.csv` row anywhere.
- `12_narrative/README.md`: *"`BLOCK_B_CLAIM_SHEET.md` — **13** SC-B surviving
  claims"* and *"`withdrawals/W-B-*.md` — **6 retractions**"*. There are 14 claims
  and, per N-B-8, 5 retractions.
- `BLOCK_B_MANUSCRIPT_FLAGS.md` §"Summary counts": `data_pending` = **8**. Counting
  the status lines gives text_only 18 ✓, resolved 3 ✓, data_pending **6**
  (B-18, B-20, B-22, B-23, B-26, B-27) — and 18+6+3 = 27 = the stated total, so 8
  is the one that is wrong.
- `EXPERIMENT_DOSSIER_BLOCK_B.md` §Freeze also says "6 withdrawals".

**Reproduction**: `grep -c '^## Flag B-' data/block_b/12_narrative/BLOCK_B_MANUSCRIPT_FLAGS.md`
and `grep -n 'Status.*data_pending' data/block_b/12_narrative/BLOCK_B_MANUSCRIPT_FLAGS.md | wc -l`.
**Severity: low.** **Closes with**: a recount, and an SC-B-14 row in a
`claim_answers.csv` (07_donor_residuals is the natural home).

## N-B-27 — `ASSUMED_NOT_VERIFIED_E.md` uses "45" for two different sets

> "After Class A + Gα-complexed filters, **45 structures** remained."

and, four paragraphs later:

> "Approximately **45 receptors** are in the ruler set beyond the 48-panel; each is
> defaulted-Class-A."

`BLOCK_B_FOLLOWUP_E1_E4.md` §E1a settles which is right: *"**Ruler-eligible after
all three restrictions**: 45 structures across 45 receptors"* — out of 103 total
active rows. So the second sentence should be about the number of ruler-set
receptors that lie *outside* the 48-receptor Block A panel, and 45 cannot be both
the whole ruler set and the part of it beyond the panel.
**Reproduction**: `grep -n "45" data/block_b/12_narrative/ASSUMED_NOT_VERIFIED_E.md
data/block_b/12_narrative/BLOCK_B_FOLLOWUP_E1_E4.md`.
**Severity: low.** It sizes an unverified-Class-A-assignment risk, so the number
matters to how large that risk is. **Closes with**: the count of ruler receptors
not in the 48-panel.

---

# Corrections to `analysis/block_b/DISCREPANCY_REPORT.md`

Two numbers in our own report are wrong. Per `rebuttals/README.md` these do **not**
go upstream; they are recorded here so the report can be fixed before anything is
sent.

1. **D-B-1, closing paragraph** — *"Recomputing the condition directly gives 28–29
   pinned cells per backbone, inside C-B-7's stated 24–34."* The actual per-backbone
   counts are **boltz 29, chai 28, of3 24, protenix 34**, which is not "28–29" and
   is not merely *inside* C-B-7's range — it **is** C-B-7's table, exactly. The
   ceiling condition is implemented after all, as the `ceiling_pinned` column of
   `04_ladder/ladder_per_receptor.csv`; what is missing is a *row-level* `excl_E_B_4`
   flag matching it. That sharpens D-B-1 rather than weakening it, and it means
   C-B-7 and BB-6 are correct and the dossier is not (N-B-10).
2. **§"What reproduces"** — *"the engaged-but-inactive floor at 1,699 rows pooled,
   **248**–540 per backbone."* The per-backbone range is **278–540** (protenix 278).
   SC-B-3 and BB-3 both say 278; 248 appears nowhere in the drop.

**Extensions to D-B-1** (the exclusion-flag mislabelling). Four further witnesses
agree with the *data*, not the claim-sheet header, which makes the header the odd
one out beyond reasonable doubt:
`EXPERIMENT_DOSSIER_BLOCK_B.md` §"Exclusion sets" (E-B-2 = OPRD/CNR1, E-B-3 = AA2AR,
E-B-4 = non-native 15 of 40); `data/block_b_structures/STRUCTURE_BUNDLE_MANIFEST.md`
§1 §4.1 (same); `10_exclusions/exclusion_definitions.csv` (same). But note that
CSV's `claim_sheet_reference` column points each flag at the claim-sheet section
that contradicts it — e.g. `excl_E_B_2` (OPRD, CNR1) → *"BLOCK_B_CLAIM_SHEET.md §
E-B-2"*, which defines E-B-2 as AA2AR. The mislabel is self-certifying. Two figure
specs inherit it: BB-2 (*"E-B-4 (ceiling-pinned cells) is the reason…"*) and BB-5
(*"E-B-3 (non-native active references) applied as the native-only filter"*).

**Extension to D-B-2** (the self-certifying `matches_claim_sheet_bool` column). It
fires on more than SC-B-1's eight continuous medians: `04_ladder/claim_answers.csv`
carries `True` on four CIs that do not match the claim sheet and are the
inadmissible row-boot family (N-B-6), and `08_covariates/claim_answers.csv` carries
`any_predictor_ci_excludes_zero = False … True` against a source file that contains
a CI excluding zero (N-B-2). The column should be regenerated by comparison, not
asserted.

---

# Checked and found NOT to be a contradiction

This section is deliberately as long as the findings. Each of these looked like a
contradiction on first read and turned out to be correctly scoped, correctly
rounded, or right.

**Scope differences that are stated, not hidden**

- **Two different Gs−Gi "rulers".** `BLOCK_B_POSTFREEZE_CHECKS.md` Check 1
  bootstraps Gs (n=5) − Gi (n=24) to +0.579 Å [+0.006, +1.025];
  `BLOCK_B_FOLLOWUP_E1_E4.md` §E1c bootstraps Gs (n=3) − Gi (n=22) to +0.541 Å
  [+0.162, +0.995] and Gs (n=6) − Gi (n=22) to +1.033 Å [+0.390, +1.415]. Same
  seed (20260910), same method, different answers — but each names its inclusion
  rule: Check 1 groups Block B's own 40 active references by family and keeps
  nanobody-stabilised entries (ADRB1, ADRB2); E1 applies a Gα-complexed filter that
  excludes nanobody by construction (*"Excludes `nanobody` (Nb-stabilised active
  states with no Gα in the complex)"*). Not a contradiction. Worth noting only that
  SC-B-6's post-freeze note quotes Check 1's ruler and the drop README points at
  both documents without saying they compute different things.
- **E3 "queued, not run" vs a shipped CI-convention audit.**
  `BLOCK_B_FOLLOWUP_E1_E4.md` §E3 defers the cluster-boot convention audit and says
  *"No `ci_convention_audit.csv` produced (E3 not run)"*, while
  `11_bootstrap_draws/ci_convention_audit_sc_b_1.csv` exists. Different jobs: E3's
  scope is *"Enumerate **every** CI in the Block B dossier"*; the shipped file is
  *"Item 2 of the closeout dispatch"* and covers SC-B-1 only. The filenames differ
  accordingly. Not a contradiction.
- **`SUPERPOSITION.md` excludes TM6; Item 3 aligns on full 7TM.** The former is a
  figure-making rule, the latter a measurement, and `SUPERPOSITION.md` says so:
  *"The scorer aligns on full 7TM … Deviation from the scorer's own alignment is
  deliberate."* Not a contradiction.
- **"Zero native Gs" vs "25 native references".** README post-freeze item 9 and
  `ASSUMED_NOT_VERIFIED_E.md` are about the Class A **Gs** subset; SC-B-13's 25
  natives are panel-wide and are overwhelmingly Gi/Gq. Consistent.
- **`BLOCK_B_ITEM3` bottom-5 / top-5 reference separations** agree cell-for-cell
  with the `pca_rank` / `np_rank` / `tilt_rank` columns of
  `STRUCTURE_BUNDLE_MANIFEST.md` §2, including AA2AR at 34 / 34 / 31. No
  contradiction.
- **Flag B-1's "24–34 of 40" vs Flag B-9's "60% (of3) to 85% (protenix)"** — the
  same numbers expressed two ways (24/40 = 60%, 34/40 = 85%).

**Roundings and near-misses that are not disagreements**

- SC-B-2's `+0.252` vs Check 2's `0.251`: the shipped value is 0.251528.
- SC-B-5's "cell floor: 0.941, Chai shuffled" vs its own table's 0.942: the shipped
  value is 0.9415.
- Structure manifest §5's apo row Δ_active −6.048 vs `LADDER_FRAMING.md`'s
  −6.045: one is the selected row, the other the cell median. Same for cognate
  (−0.232 / −0.229).
- `ci_convention_audit_sc_b_1.csv`'s cluster-boot CIs differ from
  `ladder_four_scorings.csv`'s in the third decimal (e.g. decoy [0.4503, 0.6716] vs
  [0.4446, 0.6640]) — two independent resamplings of the same statistic, not two
  conventions. Both are cluster-boot and both round to SC-B-1's stated interval at
  two decimals. Not reportable.

**Claims I tried to break and could not**

- **SC-B-1's four binary rates, `delta_to_active` medians, logits and cluster-boot
  CIs** all reproduce exactly from `04_ladder/ladder_four_scorings.csv` at
  `frame == reproduction_36, backbone == panel` (0.157917 / 0.557917 / 0.809444 /
  0.891111).
- **SC-B-2's decomposition** — estimates, shares and CIs on both scales — reproduces
  exactly from `05_decomposition/ladder_decomposition.csv`.
- **SC-B-3's three triples**, the pooled engaged-but-inactive floor (1,699) and the
  per-backbone spread (278–540) reproduce from `interface_2x2.csv`.
- **SC-B-4's five subset medians and five cell counts**, and BB-4's per-backbone
  n = 11 / 13 / 13 / 10 (sum 47), are internally consistent.
- **SC-B-5's full 16-cell fold-integrity table** reproduces cell-for-cell from
  `06_interface/interface_fold_integrity.csv`.
- **SC-B-6's native-only figures** — −0.062 Å, [−0.41, +0.21], n 24 → 20, 83.3%,
  and the n = 23/19 and 21/17 on the other two axes — reproduce exactly from
  `phase5_power_analysis.csv`. Only the all-refs CI is contested (N-B-7).
- **SC-B-12's cognate and shuffled BW registers** reproduce exactly, position for
  position and count for count. Only the decoy row and the scope statement fail
  (N-B-4, N-B-5).
- **`ladder_per_receptor.csv`'s `ceiling_pinned` / `floor_pinned` flags** reproduce
  from the raw rates in `rows_tidy.csv`, and the raw rates reproduce from the
  two-instrument predicate. The per-receptor table is sound; three narrative
  documents disagree with it, not the other way round.
- **The `deposition_count` degeneracy** is real: all 40 receptors carry exactly 2,
  std = 0, NaN slope, exactly as C-B-14 and POSTFREEZE Check 3 state.
- **C-B-14's cluster arithmetic** ("11 of 26 clusters are singletons", 15
  multi-member) sums correctly.
- **C-B-9's reference-set arithmetic** — 6 added inactive rows across 5 receptors —
  is correct. Only the Block B intersection is wrong (N-B-14).
- **The structure bundle's anchor selection** (GHSR) follows its own written rules,
  and it discloses its own atypicality — GHSR decoy 0.175 vs panel 0.558 — rather
  than hiding it. The 13 shipped CIFs, their SHAs and the C2/D-boltz duplication
  are all accounted for.
- **W-B-6's restatement** (1,623 / 2,398 frame_40; 1,427 / 2,133 frame_36) is
  carried identically in Flag B-13, W-B-6 and dossier §4b.

**On the equivalence question (task item f) — nothing live survives**

I grepped every narrative file for `equivalen`, `ruled out`, and `0.4 Å`. Every
occurrence is inside a retraction or a statement of what was *not* concluded:

- `BLOCK_B_CLAIM_SHEET.md` § SC-B-6's post-freeze note quotes the retracted phrase
  inside quotation marks — *"an attempt to strengthen SC-B-6 to an equivalence-style
  claim (\"family-specific opening ruled out above ~0.4 Å…\") did not survive"* —
  and concludes *"SC-B-6 stays as the 'Outcome A signed, CI spans zero' Phase 6b
  wording … not an equivalence claim."*
- `BLOCK_B_POSTFREEZE_CHECKS.md` Check 1 carries the word eight times, all in the
  service of a **UNDETERMINABLE** verdict.
- `BLOCK_B_FOLLOWUP_E1_E4.md`'s proposed Methods sentence is scrupulously
  non-equivalence: *"the family-specific opening the deposited record shows is
  **not resolvably reproduced or excluded** by the Block B models on this axis."*
- No caveat, flag, figure spec, dossier section or structure document carries
  equivalence wording at all.

**One thing to watch rather than report.** `BLOCK_B_FOLLOWUP_E1_E4.md` §E1d records
that the chimera-inclusive stratum *does* clear the pre-registered Branch-1 bar —
*"**All (incl. chimera)**: lower bound 0.390 > 0.21, nominally Branch-1 territory"* —
and E1's Methods sentence quotes that interval (+1.033 [+0.390, +1.415]) in prose.
It is correctly refused (*"Adopting the chimera-inclusive result as the ruler would
let engineered scaffold geometry drive the SC-B-6 sign flip. **Not adopted.**"*),
but it is the one number in the bundle from which an equivalence sentence could be
reconstructed by a drafting agent that reads the table and not the verdict. Worth a
note in `analysis/block_b/DISCREPANCY_REPORT.md`, not a rebuttal entry — the drop
did this correctly.

---

## Summary table

| # | contradiction | reaches reader | severity |
|---|---|---|---|
| N-B-1 | Block B "is prospective" vs prospectivity foreclosed | yes | highest |
| N-B-2 | "no covariate signs" vs cognate_family=Gs [+0.281,+2.337] | yes | highest |
| N-B-3 | AA2AR +0.76 "single largest"; six cells larger | yes | high |
| N-B-4 | 327 TM6-apex contacts attributed to the partner-less apo arm | yes | high |
| N-B-5 | SC-B-12 "160 engaged cells per arm"; decoy has 116 | yes | high |
| N-B-6 | dossier §3d ladder rungs + row-boot CIs, echoed in claim_answers | yes | high |
| N-B-7 | SC-B-6 all-refs CI: [−0.29,+0.30] vs [−0.31,+0.30] | yes | high |
| N-B-8 | W-B-4 withdrawn and not-withdrawn, 7 places | yes | high |
| N-B-9 | C-B-7 top-5 boltz family terms reproduce nowhere; BB-6 prints them | yes | high |
| N-B-10 | ceiling/floor counts: dossier vs C-B-7/BB-6/data | figure | high |
| N-B-11 | engaged-but-inactive per backbone: 1,582 vs 1,699 | figure | high |
| N-B-12 | AA2AR: three anomalies vs five vs dispatch's one | yes | med-high |
| N-B-13 | Gs→Gi native n: 19 vs 20 | via 83.3% | medium |
| N-B-14 | preload check: three Block B receptors vs four (CCR5) | Methods | medium |
| N-B-15 | C-B-14 "all 40" vs n = 28/34/32/40/32/40 | Methods | medium |
| N-B-16 | BB-1 annotates the superseded 0.552/0.810/0.892 | figure | med-high |
| N-B-17 | BW register sourced to the wrong CSV, 3 places | no | medium |
| N-B-18 | BB-3 filter returns 0 rows; 6 columns misnamed | figure | medium |
| N-B-19 | BB-2 family-term labels: boltz/protenix transposed | figure | medium |
| N-B-20 | BB-1 CI shading from a file with no per-arm draws | figure | medium |
| N-B-21 | two different "three 94% referents" lists | no | medium |
| N-B-22 | "~40% chimera/mini-G" vs 37.5% non-native (25% chimera) | Limitations | medium |
| N-B-23 | "4 Å looser" vs 0.39 Å | caption | medium |
| N-B-24 | dossier §3f top-5: unnamed aggregation, wrong 5th member | figure | medium |
| N-B-25 | four baselines; freeze tag "PENDING" but already cut | no | low |
| N-B-26 | 13 vs 14 claims; 6 vs 5 withdrawals; data_pending 8 vs 6 | no | low |
| N-B-27 | "45" used for two different sets | no | low |
