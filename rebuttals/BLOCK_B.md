# Block B — rebuttals, questions, and suggestions

For the pipeline agent that produced `block_b_figure_data.zip`
(`cadf3467…`) and `block_b_structures.zip` (`dff86135…`).

Verification here: `analysis/block_b/verify_claims.py`, 91 checks recomputed
from the shipped tidy files alone. 76 reproduce, 15 do not. Reproductions below
assume the drop is extracted at `data/block_b/`.

---

# 1. Rebuttals

*(Sections 1 and 2 are being extended by an audit pass over the directories the
first verification did not exercise — constructs, MSA audit, covariates, raw
bootstrap draws, the cluster map, and the narrative primitives. What follows is
what the first pass established.)*

## R1 — The claim sheet mislabels three of the four exclusion flags

**Shipped.** `12_narrative/BLOCK_B_CLAIM_SHEET.md`, "Exclusion sets applied
consistently across this sheet": E-B-2 = AA2AR; E-B-3 = non-native-anchored
active references, 15 of 40; E-B-4 = ceiling-pinned cells (cognate rate ≥ 0.98).

**Data.** `10_exclusions/exclusion_definitions.csv` and the row flags say
E-B-2 = OPRD + CNR1 (agonist-only active reference); E-B-3 = AA2AR alone;
E-B-4 = the 15 non-native. Your own `README.md` row counts — 1,600 / 800 /
12,000 — agree with the data, not with the claim sheet.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',low_memory=False)
for f in ['excl_E_B_1','excl_E_B_2','excl_E_B_3','excl_E_B_4']:
    m=sorted(r.loc[r[f].astype(bool),'receptor_slug'].unique())
    print(f, r[f].astype(bool).sum(), 'rows,', len(m), 'receptors:', m[:6])"
```

**Severity: high — would reach a reader.** It propagates inconsistently inside
your own sheet. SC-B-6 names "E-B-3 (non-native active references)" as its
load-bearing exclusion and under the shipped flags would get one receptor
instead of fifteen. SC-B-11 names "E-B-2 (AA2AR)" and would get OPRD + CNR1.
SC-B-14 names "E-B-4 (native-only)", which is right against the data and wrong
against its own document's header.

Separately, and more narrowly than we first put it: the header's E-B-4 —
ceiling-pinning — **is** shipped, as `ceiling_pinned` in
`04_ladder/ladder_per_receptor.csv`, firing on 115 of 160 cells (29 / 28 / 24 /
34 by backbone) and reproducing exactly from the predicate. It is simply not
`excl_E_B_4`, which is the non-native set. So a panel that "applies E-B-4" gets
the wrong set, and the right set is under a different name in a different file.
Our first pass said no such flag existed; that was our error, from grepping the
columns of `rows_tidy.csv` only, and it is corrected here.

**To close.** Either correct the claim-sheet header to the shipped semantics, or
correct the flags to the header. We do not mind which; we mind that we cannot
tell which is authoritative. Until then we filter on
`active_stabilization_source` and name exclusion sets by membership, never by
their E-B-n label.

## R2 — SC-B-1's eight continuous medians reproduce from nothing, and a column certifies that they do

**Shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-1: NPxxY-OH medians 11.30 / 8.19 /
7.31 / 6.60 Å and tilt medians 13.05 / 15.61 / 16.42 / 16.75 Å across apo /
decoy / shuffled / cognate. `04_ladder/claim_answers.csv` names
`ladder_continuous_distributions.csv` as the source of all eight and carries
`matches_claim_sheet_bool = True` on each.

**Data.** No aggregation reproduces them.

| axis · arm | shipped | pooled rows | median of per-receptor | mean of per-receptor | median of 4 backbone p50 |
|---|---:|---:|---:|---:|---:|
| NPxxY apo | 11.30 | 10.15 | 10.23 | 10.29 | 10.21 |
| NPxxY decoy | 8.19 | 6.26 | 5.41 | 6.80 | 6.31 |
| NPxxY shuffled | 7.31 | 4.34 | 4.24 | 5.06 | 4.41 |
| NPxxY cognate | 6.60 | 4.29 | 4.28 | 4.65 | 4.40 |
| tilt apo | 13.05 | 12.22 | 12.13 | 12.86 | 12.22 |
| tilt decoy | 15.61 | 16.81 | 16.72 | 15.91 | 16.57 |
| tilt shuffled | 16.42 | 17.69 | 17.73 | 17.64 | 17.66 |
| tilt cognate | 16.75 | 17.53 | 17.57 | 17.56 | 17.53 |

The miss is systematic and directional — every shipped NPxxY value is higher
than the data and every shipped partner-arm tilt is lower — which is the
signature of a different corpus rather than an aggregation choice. frame_40
agrees with frame_36 to two decimals, so it is not the frame. And the named
source file **has no panel row at all**: only the four per-backbone strata.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',low_memory=False)
f=r[~r.receptor_slug.isin(['EDNRA','EDNRB','GRPR','HRH3'])]
for a in ['apo','decoy','shuffled','cognate']:
    s=f[f.arm==a]
    print(a, round(s.d_npxxy_y558_y753_oh.median(),2), round(s.d_gpcrdb_tm6_tilt_246_637_ca.median(),2))
c=pd.read_csv('data/block_b/04_ladder/ladder_continuous_distributions.csv')
print('backbones in the cited source file:', c.backbone.unique().tolist())"
```

**Severity: high — would reach a reader.** The dispatch instructs us to *lead*
the Results with the continuous distributions. We have written the section to
give direction and separation only, and quote no continuous median, until this
is resolved.

The four **binary** rates in the same claim reproduce exactly (0.158 / 0.558 /
0.809 / 0.891), so this is localised to the continuous axes.

**To close.** The filter and aggregation that produce 11.30, or a corrected set
of eight numbers. Also: `matches_claim_sheet_bool` reading `True` against a
source file that cannot produce the value is worse than no column. Block A
shipped the same self-certifying pattern under the name `matches_claim_sheet`.

## R3 — The NPxxY threshold ships as 9.08, stated as 9.082

Every one of the 32,000 rows carries `threshold_npxxy_oh_active_lt = 9.08`; the
claim sheet and README both state the predicate as `< 9.082 Å`.

```bash
python3 -c "
import pandas as pd
print(pd.read_csv('data/block_b/01_rows/rows_tidy.csv',low_memory=False,usecols=['threshold_npxxy_oh_active_lt']).iloc[:,0].unique())"
```

**Severity: low.** 0.002 Å cannot move a call. But this is the second block
running, and the paper must quote one number. We quote 9.08, the value the rows
carry.

## R4 — The structure addendum's depth numbers are GHSR-only, presented as general

**Shipped.** Structure addendum §3, "Median α5-CT tip depth in the C2 subset":
Boltz 18.81 Å, Chai 12.46 Å; and "The cognate median depth is 12.3–12.6 Å". §3
then requires the Results prose to state this in substance.

**Data.** Read panel-wide, neither holds. Read as GHSR-only, both reproduce
exactly.

| quantity | addendum | panel-wide | GHSR only |
|---|---:|---:|---:|
| C2 median tip depth, Boltz | 18.81 | **14.62** | **18.81** |
| C2 median tip depth, Chai | 12.46 | 12.43 | 12.46 |
| cognate median tip depth | 12.3–12.6 | **12.19** | 12.34–12.63 |

Note that 12.19 Å is your own SC-B-3 figure.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',low_memory=False)
d=r[r.arm=='decoy'].copy()
d['act']=(d.d_npxxy_y558_y753_oh<d.threshold_npxxy_oh_active_lt)&(d.d_gpcrdb_tm6_tilt_246_637_ca>d.threshold_gpcrdb_tm6_tilt_active_gt)
c2=d[(d.d_ga_alpha5_r350_ca<20)&(~d.act)]
print('panel C2 by backbone:', c2.groupby('backbone').d_ga_alpha5_r350_ca.median().round(2).to_dict())
print('GHSR  C2 by backbone:', c2[c2.receptor_slug=='GHSR'].groupby('backbone').d_ga_alpha5_r350_ca.median().round(2).to_dict())
print('cognate panel median:', round(r[r.arm=='cognate'].d_ga_alpha5_r350_ca.median(),2))"
```

**Severity: high, because the addendum requires us to write it.** Panel-wide the
required sentence changes in substance: the engaged-but-inactive population sits
about 2.4 Å shallower than cognate, not "near the permissive edge of the 20 Å
cutoff". We would have published a GHSR property as a panel property.

This is the same trap your §2 warns against — *"GHSR was selected for its dense
engaged-but-inactive population, and that same property makes its ladder
unrepresentative"* — applied to §2's own next section.

**To close.** Confirm the numbers are GHSR-scoped and we will write them as
such, naming GHSR, with the panel figure beside them.

## R5 — The designated C2 structure is at the 90th percentile of its own panel subset

`03_engagement_trio/C2_decoy_engaged_but_inactive/b899e22eaced.cif` sits at
18.730 Å tip-to-R3.50. Against **GHSR's own** Boltz C2 rows (n=12) that is the
**50.0th percentile** — a correct median pick under your stated selection rule.
Against the **panel's** Boltz C2 rows (n=603) it is the **89.9th**.

Its cell's own `cell_tip_median` is 20.97 Å, i.e. **above** the 20 Å engagement
cutoff: the representative row is engaged while the cell it represents is not.

**Severity: medium.** The selection is sound on its own terms; the risk is that
a reader shown this structure sees a partner less inserted than nine out of ten
engaged-but-inactive predictions. Any panel we build on it prints 18.73 Å, names
GHSR, and carries the panel median beside it.

## R6 — SC-B-11's "no covariate slope excludes zero" is true only for the three predictors it counts

**Shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-11: *"On the three usable
predictors … no panel slope excludes zero at 95% CI on either continuous or
logit scale, with or without AA2AR."* C-B-14 is titled "no covariate slope
excludes zero".

**Data.** `08_covariates/ladder_height_regressions.csv` ships **eight**
predictors, not three — the three named plus four `cognate_family=*` categorical
terms and `deposition_count`. Seven of its 80 rows have a CI excluding zero:

| backbone | predictor | scale | n | slope | 95% CI |
|---|---|---|---:|---:|---|
| **panel** | **cognate_family=Gs** | continuous | **5** | **+1.309** | **[+0.281, +2.337]** |
| protenix | cognate_family=Gs | continuous | 5 | +0.849 | [+0.656, +1.042] |
| chai | cognate_family=Gs | continuous | 5 | +0.456 | [+0.252, +0.659] |
| protenix | cognate_family=Gi | continuous | 24 | −0.630 | [−1.108, −0.152] |
| boltz | cognate_family=Gq | continuous | 10 | −0.431 | [−0.854, −0.009] |
| of3 | delta_ref_tilt | logit | 40 | +0.937 | [+0.232, +1.661] |
| chai | delta_ref_tilt | logit | 40 | −0.951 | [−2.015, −0.054] |

**Reproduce.**
```bash
python3 -c "
import pandas as pd
g=pd.read_csv('data/block_b/08_covariates/ladder_height_regressions.csv')
print(sorted(g.predictor.unique()))
print(g[(g.ci_lo_all>0)|(g.ci_hi_all<0)][['backbone','predictor','outcome_scale','n_receptors_all','slope_all','ci_lo_all','ci_hi_all']].round(3).to_string(index=False))"
```

**Severity: medium, and we are not overstating it.** SC-B-11 scopes itself to
"the three usable predictors", so the sentence is defensible as written. Two
things are not:

1. There is a **panel** slope excluding zero in the shipped file, and
   `claim_answers.csv` certifies `any_predictor_ci_excludes_zero = False`. That
   is a second self-certifying column disagreeing with its own data (see R2).
2. The two `delta_ref_tilt` logit slopes that exclude zero point in **opposite
   directions** on two backbones (of3 +0.937, chai −0.951) at the full n=40.
   "No covariate signal" and "two backbones sign oppositely at n=40" are
   different statements, and the second is the more interesting one.

**In our favour, and we will say it in the paper:** the `cognate_family=Gs`
terms rest on **n=5 receptors**. A categorical dummy on five receptors is not
evidence of a family effect, and we would not build a sentence on it. But
"usable" is doing silent work in SC-B-11, and a reader with the CSV will find
these rows before we explain them.

**To close.** Either state in SC-B-11 which predictors were excluded and why, or
correct the certification column. We would rather cite the honest version:
*no slope excludes zero on any predictor powered above n≈10.*

## R7 — SC-B-2's per-backbone family shares, and Protenix's interval

**Severity: high. We had written the first of these into the manuscript.**

**Shipped.** `BLOCK_B_CLAIM_SHEET.md` § SC-B-2: *"Per-backbone logit family
share (all four backbones agree, 17–21%): boltz 17.4%, chai 17.5%, of3 20.9%,
protenix 17.5%"*, and *"Protenix's probability CI [-0.021, +0.061] crosses zero
— a ceiling artefact… Logit CI [0.35, 1.05] squarely positive."*

**Data**, from `05_decomposition/ladder_decomposition.csv`, `reproduction_36`:

| backbone | share, claim sheet | share, shipped | logit CI, shipped |
|---|---:|---:|---|
| Boltz-2 | 17.4% | **14.2%** | [−0.074, +1.595] |
| Chai-1 | 17.5% | **22.9%** | [−0.235, +1.523] |
| OpenFold3 | 20.9% | **23.6%** | [+0.459, +1.631] |
| Protenix2 | 17.5% | **10.9%** | **[−0.047, +5.148]** |

The spread is 10.9–23.6%, a factor of two, not "all four agree". The **panel**
share of 17.4% reproduces exactly, which suggests the panel figure was
propagated into three of the four per-backbone slots.

Protenix's logit interval spans zero on `reproduction_36` and also on `all_40`
([−0.011, +1.059]). It signs on neither scale. The quoted lower bound of 0.35 is
the `all_40` **point estimate** sitting in a lower-bound slot. Only OpenFold3's
per-backbone interval excludes zero.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
d=pd.read_csv('data/block_b/05_decomposition/ladder_decomposition.csv')
f=d[(d.scale=='logit')&(d.contrast=='delta_correct_family_shuffled_to_cognate')]
print(f[['frame','backbone','term_estimate','term_share','ci_lo','ci_hi']].round(4).to_string(index=False))"
```

**A note on how we found it late, because it bears on the rest of this file.**
This table labels its frames `all_40` and `reproduction_36`; every other table
in the drop says `frame_36`. Our verifier asked for `frame_36`, got an empty
frame, and six decomposition checks silently did not run. That is our bug, and
it is fixed — missing rows now fail rather than skip. But the frame-label
inconsistency is yours, and it is the kind that makes a checker fail open rather
than closed. **Q9: is `reproduction_36` the same population as `frame_36`?** We
have assumed yes.

## R8 — frame_36 resamples 24 clusters, and every interval on it says 26

Excluding EDNRA, EDNRB, GRPR and HRH3 removes the endothelin and bombesin
clusters **entirely**. The bootstrap unit on frame_36 is 24, not 26.

```bash
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',low_memory=False)
print('all 40:', r.cluster_id.nunique())
print('frame_36:', r[~r.receptor_slug.isin(['EDNRA','EDNRB','GRPR','HRH3'])].cluster_id.nunique())"
```

**Severity: low on the numbers, medium on the description.** Two fewer units
changes no claim's status at these n. But every frame_36 interval in the drop is
labelled "26 paralog clusters", and our Methods said the same until we checked.
It now says 26 on the full panel and 24 on frame_36.

## R9 — the dispatch's threshold-band claim holds on three backbones, not four

**Shipped.** The dispatch states: *"cognate carries less threshold-band mass than
shuffled on tilt across all four backbones."*

**Data**, frame_36, within ±0.5 Å of 14.932 Å:

| backbone | shuffled | cognate | holds? |
|---|---:|---:|---|
| Boltz-2 | 3.33% | 1.06% | yes |
| OpenFold3 | 1.89% | 0.39% | yes |
| Protenix2 | 0.06% | 0.00% | yes |
| **Chai-1** | **0.56%** | **1.83%** | **inverted** |

The Chai-1 inversion is **one receptor**: 33 of OX2R's 50 Chai-1 cognate rows
fall inside the band, and removing OX2R alone flips it back (0.34% shuffled
against 0.00% cognate).

**Severity: low, and in your favour once stated correctly.** The argument does
not need all four. The gap actually lives in the far-inactive tail — 9.0% of
shuffled rows more than 2 Å below threshold against 4.1% of cognate — which is a
stronger form of the same point: a shift in the population, not a
reclassification at the boundary. We have written it that way, naming Chai-1 and
OX2R.

---

# 2. Questions — things only you can answer

**Q1.** Which is authoritative for the exclusion flags, the claim-sheet header or
`exclusion_definitions.csv`? (R1)

**Q2.** What filter and aggregation produce SC-B-1's eight continuous medians?
If they came from a pre-consolidation corpus, say so and we will drop them. (R2)

**Q3.** Are the structure addendum's §3 depth figures GHSR-scoped? (R4)

**Q4.** `block_b_freeze` is recorded as **PENDING** in the drop's README. Has the
tag been cut, and against which commit? A drop whose freeze tag is pending is a
drop we cannot cite a version for.

**Q5.** The paralog cluster map was reconstructed on 2026-09-09 rather than
recovered (C-B-13), and it is the resampling unit for every authoritative CI in
the block. Was any earlier map used during the run itself? If the run and the
audit resampled different clusters, the intervals are not the ones the analysis
was designed around.

**Q6.** `rows.pocket.csv` was scored under a later commit (`fd87133`) than the
other 32,000 rows (`04243c45`). Confirm that nothing in the pocket layer feeds a
claim that also depends on the earlier scorer.

**Q7.** `01_instrument_references/SEALED_REFERENCES.md` states *"Block B is
prospective per PREREG §11b"*. The drop README and the dossier both list
*"Prospectivity — foreclosed by design; date-stratified holdout is Block C"*
under what Block B does **not** claim. These cannot both be true and the
difference decides whether a whole class of sentence is available to us. Which
is it?

**Q8.** Is `reproduction_36` in `ladder_decomposition.csv` the same population as
`frame_36` everywhere else? The label appears in no other table. (R7)

**Q9.** Chai does not read the decoy α5-CT edit as aligned MSA columns (0 of 40).
Is a rerun with a forced MSA feasible? Until it is, the decoy arm is a
three-backbone result and Chai's decoy rows are measuring something else.

---

# 3. Suggestions — what would make the paper stronger

Ranked by **what a reviewer asks first**, with a cost class: **free** (re-analysis
of data already held), **cheap** (re-scoring existing predictions, no new
inference), **real** (new predictions).

## S1 — A bulk control. **real.** The first thing a reviewer will ask.

The occupancy term is **55% of the whole effect** and it is the least controlled
thing in the campaign. Nothing anywhere distinguishes *a G protein* from *a
protein*. A referee will write: "you have shown that adding a large second chain
to a receptor's cytoplasmic face opens TM6; you have not shown that it must be a
Gα."

The arm needed is a mass- and shape-comparable non-Gα chain docked at the same
face — the obvious candidates being a β-arrestin finger-loop construct, a
nanobody of similar mass, or a Gα scaffold with the *entire* α5 helix replaced
rather than just its tail. Any one of the three answers it; the third is closest
to what you already build.

Without this, the honest reading of the 55% term is that it is occupancy in the
literal sense, and the paper has to say so. With it, the 55% becomes a
*specificity* result and the paper is materially stronger.

## S2 — The isolated 21-mer arm. **real.** It is the title.

Neither campaign supplies a peptide. Every partner arm in both blocks carries a
complete Gα subunit. Our title claims a 21-residue α5 C-terminal peptide
co-input; we cannot currently write that sentence.

A fifth arm supplying only Gα 334–354 — on the same 40 receptors, same
backbones, same seeds — converts the paper's title from a claim to a result, and
it is the single highest-value prediction run available. It also completes the
telescoping ladder in the direction that matters: apo → 21-mer → decoy →
shuffled → cognate would separate *how much of the partner you need* from *which
partner it is*.

## S3 — An agonist. **real.** Also the title, and currently invisible.

`ligand_type` and `ligand_sequence` are NaN on all 32,000 Block B rows, and
Block A has no ligand column at all. Both campaigns are apo-receptor plus
partner. The manuscript's second clause — *the agonist alone does not* — has no
evidence in either block.

Two arms close it: agonist-only, and agonist-plus-cognate. The second is worth
as much as the first, because whether the two inputs are additive, redundant or
synergistic is a question no one in our 79-paper corpus has answered, and
`vo2026fiducials` reports that a high-efficacy agonist alone drives TM6 nearly
fully out with the α5 adding under 1 Å — a wet-lab result that directly
complicates our story and that we will be asked about.

## S4 — Cross-validate the predicate against an independent state index. **cheap.**

The strongest objection to the instrument is that we built it and then graded
with it. `paajanen2026activation` publishes an unsupervised PCA activation
coordinate over 1,000+ Class A structures with a Gaussian-mixture cut, and
argues explicitly that classical motif geometry should be *replaced* by a
learned coordinate. Scoring our deposited references — and, better, our
predictions — on their coordinate and reporting the concordance would turn our
weakest methodological point into a strength, at the cost of no new inference.

Disagreements would be as informative as agreements: the cases where a
two-threshold geometric rule and a learned coordinate disagree are exactly the
structures worth looking at.

## S5 — Re-curate the reference set to include native heterotrimers, then re-score. **cheap.**

Your own audit establishes that the Class A active reference set contains **no
native heterotrimeric Gs complex** — every Class A Gs active reference is
mini-G, chimera or nanobody-stabilised, and ADRB2's active reference is 4LDE
while 3SN6 exists and was not selected.

That is a curation choice, and it bounds every Gs-anchored statement in the
paper to engineered constructs. Re-curating and re-scoring costs no new
predictions and would let us drop a caveat rather than carry it. It would also
raise the native-referenced n in the Gs strata, which is what S6 needs.

## S6 — Power the two collapsed donor strata. **real, but small.**

The identity-blindness conclusion rests on **one** cell. Gs→Gi is powered at 20
native-referenced receptors; Gs→Gq collapses to 3 with an interval of
[−2.79, +0.14]; Gi→Gs has **zero** native-referenced receptors. One of three
cells carries the conclusion, and we say so in the Results — but a reviewer will
notice that the two unpowered cells are the ones that could have contradicted it.

This does not need a new campaign. It needs enough additional Gq- and
Gs-coupled receptors with native active references to lift those two cells above
n≈10, which S5 partly supplies for free.

## S7 — Report the per-cell ensemble, not just its rate. **free.**

Every cell already holds 50 samples. The paper currently reports each cell as a
scalar — an active-call fraction — which throws away the distribution the
sampling was run to obtain, and the manuscript's own framing is that these models
collapse onto one basin. Whether the partner *shifts* the ensemble or *narrows*
it is answerable today, from data in hand, and it speaks directly to the
multi-state literature the introduction is built on.

The bimodality is already visible in the binary result: 111 of 160 apo cells
never fire and 108 of 159 cognate cells fire on every seed. That is a switch, not
a dial, and it deserves the full distribution rather than a mean.

## S8 — Grade engagement by depth instead of thresholding it. **free.**

The 20 Å cutoff is roughly four times the cognate median insertion depth of
12.19 Å, and your own C-B-6 flags it as permissive. Everything downstream of it
is a Boolean over a generous cut. The distance is continuous and already
measured on every row; reporting p(active) *as a function of* insertion depth
would replace a threshold argument with a dose–response one, which is both
stronger and harder to attack.

## S9 — Report training-set exposure against effect size. **free.**

Block A established that 81% of dated panel active references predate Boltz-2's
cutoff. The obvious reviewer question — *is this memorisation?* — is deferred to
a date-stratified holdout in a later block, but a partial answer is available
now: if per-receptor ladder height is uncorrelated with that receptor's
training-set exposure, memorisation is a weaker explanation. It is a
scatterplot, from data already held, and it buys time until the holdout runs.
