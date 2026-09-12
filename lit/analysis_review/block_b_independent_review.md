# Block B — independent adversarial verification

**Reviewer**: lit-session adversarial checker, read-only pass.
**Date**: 2026-09-10.
**Scope**: `data/block_b/`, `data/block_b_structures/` (read-only), cross-read against
`data/block_b/12_narrative/BLOCK_B_CLAIM_SHEET.md`.
**Method**: every number below was recomputed from `01_rows/rows_tidy.csv` (32,000 rows) or
from the shipped bootstrap draws, not read out of a summary table. Where the drop ships both
a tidy source and a summary, both were checked against each other.
**Rule applied**: the data wins over the claim sheet.

---

## 0. Summary

The **arithmetic in this drop is very good**. The ladder, the decomposition, the 2×2, the PIF
connector, the fold integrity, the construct scramble and the donor residuals all reproduce
exactly from the tidy rows — in several cases to four decimal places, including bootstrap
interval bounds recomputed from the shipped draws. All 103 files match their `MANIFEST.json`
sha256. The reference-set pin sha256 verifies.

The problems are **not** in the computation. They are in three places:

1. **What the arms actually contain.** No arm in Block B supplies a 21-residue peptide. Every
   non-apo arm supplies a **full-length Gα subunit of 350–394 residues**. This is stated
   plainly in the dossier and in `02_constructs/`; it is the parent framing ("Block B is where
   the peptide claim must be established") that does not survive contact with the drop.
2. **One contrast label is a confound**, and it is the one carrying 34% of the effect.
3. **The claim sheet contains numbers that are not in the data it cites**, including one that
   reverses a sign verdict, and one whose sub-claim is contradicted by every backbone.

Findings below. 8 BLOCKING, 13 MATERIAL, 14 MINOR.

---

## 1. THE CENTRAL CHECK — what was actually supplied as co-input

Recomputed from `06_interface/interface_continuous.csv:n_partner_aa` (640 cells) and verified
independently by extracting chain sequences from the four shipped ladder-arm CIFs.

| arm | partner chain length (cells) | what it is |
|---|---|---|
| apo | `0` × 160 | no partner chain at all |
| cognate | `354` × 96, `359` × 40, `394` × 20, `350` × 4 | full-length WT Gα of the receptor's own family |
| decoy | `354` × 96, `359` × 40, `394` × 20, `350` × 4 | **the same full-length cognate Gα**, last 11 residues permuted |
| shuffled | `394` × 132, `354` × 24, `377` × 4 | full-length WT Gα of a **different** family |

Direct sequence extraction from the GHSR ladder CIFs (`02_ladder_arms/`):

```
apo       chain A 366 aa (receptor only), no chain B
decoy     chain B 359 aa  MTLESIMACC…ILYELQKVLNNL   (Gαq, tail scrambled)
cognate   chain B 359 aa  MTLESIMACC…ILQLNLKEYNLV   (Gαq, WT)
shuffled  chain B 394 aa  MGCLGNSKTE…IQRMHLRQYELL   (Gαs — a different protein)
```

- decoy vs cognate: **byte-identical over the first 349 residues**, 8 of the last 11 differ.
- decoy vs shuffled: **different protein, 359 → 394 residues, ~2.8% residue-block identity.**

The drop's own labels confirm this: `donor_ga_class` on decoy rows is `Gq_scaffold_scrambled`
/ `Gi_scaffold_scrambled` — i.e. **the decoy carries the correct-family scaffold**. On shuffled
rows it is a bare `Gs` / `Gi` / `G12`.

**Reproduce:**
```bash
cd data/block_b && python3 -c "
import csv,collections
r=list(csv.DictReader(open('06_interface/interface_continuous.csv')))
for a in ['apo','cognate','decoy','shuffled']:
    print(a, dict(collections.Counter(x['n_partner_aa'] for x in r if x['arm']==a)))"
```

### F-1 — BLOCKING — Block B supplies a whole Gα, not a 21-mer; it cannot carry the titular claim

| | |
|---|---|
| **Severity** | BLOCKING |
| **File + column** | `06_interface/interface_continuous.csv:n_partner_aa`; `data/block_b_structures/02_ladder_arms/*/*.cif` chain B |
| **Claimed** | (parent framing) "Block B is where the 21-residue α5-CT peptide co-input claim must be established" |
| **Found** | Minimum partner length anywhere in Block B = **350 aa**. Zero peptide arms. The string "21-mer" / "21 residues" appears in **no** markdown file in the drop. |

The drop itself is honest about this — `EXPERIMENT_DOSSIER_BLOCK_B.md` §Arms reads: *"apo
(receptor alone); decoy (full cognate Gα, α5-CT ~10–11 residues scrambled); shuffled (a real
Gα from the wrong family); cognate (the receptor's own Gα)"*, and describes the experiment as
*"testing whether the model reads partner **identity** or partner **mass**"*. That is a
different experiment from the one the paper's title claims.

Consequences that must be settled before any Block B sentence is drafted:

- Block B is **the same co-input type as Block A** (whole Gα). It is a partner-*selection*
  experiment, not a partner-*minimisation* experiment. It does not narrow the novelty gap
  against `chiesa2025templatebias`, which also supplied a whole G protein.
- **No arm contains an agonist.** `ligand_type`, `ligand_sequence`, `ligand_smiles` are empty
  on all 32,000 rows. Block B's "apo" is receptor-alone-with-nothing, not
  receptor-plus-agonist. The paper's "the agonist alone does not" comparison is **not in this
  block**, and no Block B arm supplies agonist + peptide together — so the specific confound
  named in the review brief does not occur here. A different one does (F-2).
- The only α5-CT-length peptides in the campaign (`endothelin1` 21 aa, `random_helix_40mer`,
  `substanceP`, `DAMGO`) appear in `03_msa_audit/msa_depth_report.md`'s appendix as **Block A
  exploratory partners**, explicitly "not part of the Block A/B receptor-Gα narrative".

### F-2 — BLOCKING — the `Δ α5-CT sequence` contrast swaps the entire subunit

| | |
|---|---|
| **Severity** | BLOCKING |
| **File + column** | `05_decomposition/ladder_decomposition.csv:contract=delta_a5ct_sequence_decoy_to_shuffled` |
| **Claimed** | SC-B-2: "Δ_α5CT_seq (decoy→shuffled) +0.252, **34.3%** of the ladder" |
| **Found** | The estimate reproduces exactly (+0.2515). The **label does not.** decoy→shuffled changes ~349 of 359 partner residues, changes the chain length, changes the Gα family, and changes the partner MSA to a different protein's MSA. It is not an α5-CT-sequence contrast. |

This is precisely the defect the manuscript criticises in `ye2026multistatebias`,
`zhang2026generalization` and `chiesa2025templatebias`: one arm changes more than one thing and
the effect is attributed to one of them.

The same objection applies, more mildly, to the other two terms:

- **`delta_occupancy_apo_to_decoy` (+0.400, 54.6%)** is labelled "occupancy". The thing added
  is not bulk — it is **97% of the receptor's own cognate Gα**, including the entire α5 helix
  except the terminal 11 residues. **Block B ships no bulk / nonspecific-partner arm**, so the
  occupancy term cannot be separated from "correct Gα scaffold present". A reader will take
  "occupancy is 55% of the effect" to mean "any mass does most of the work". The data does not
  say that.
- **`delta_correct_family_shuffled_to_cognate` (+0.082, 11.1%)** is also a whole-subunit swap,
  but it is honestly named at the subunit level.

**The constructive finding.** Block B *does* contain exactly one clean, unconfounded α5-CT
contrast, and it is not one of the three published terms: **decoy → cognate**, in which the
Gα scaffold is byte-identical and only the 11-residue α5-CT tail changes (Hamming 7–11,
composition preserved). I bootstrapped it independently:

| contrast | what actually changes | estimate | 26/24-cluster 95% CI |
|---|---|---:|---|
| **decoy → cognate** | **only the 11-residue α5-CT tail** | **+0.3332** | **[+0.244, +0.435]** signed |
| apo → decoy | adds ~97%-cognate Gα (labelled *occupancy*) | +0.4000 | [+0.330, +0.465] |
| decoy → shuffled | whole subunit swap (labelled *α5-CT sequence*) | +0.2515 | [+0.184, +0.322] |
| shuffled → cognate | whole subunit swap (labelled *family*) | +0.0817 | [+0.046, +0.124] |

The decoy→cognate contrast is strong, clean and signed, and it is the only sentence in this
block that can honestly be written as "the α5-CT sequence itself is what the model reads". It
is not a named claim anywhere in the claim sheet. **Recommend it replace SC-B-2's three-term
decomposition as the headline.**

**Reproduce:**
```bash
cd data/block_b && python3 - <<'EOF'
import csv,collections,math,random
rows=list(csv.DictReader(open('01_rows/rows_tidy.csv')))
def f(v):
    try: return float(v)
    except: return float('nan')
E={'EDNRA','EDNRB','GRPR','HRH3'}
def act(r):
    a=f(r['d_npxxy_y558_y753_oh']);b=f(r['d_gpcrdb_tm6_tilt_246_637_ca'])
    return (not math.isnan(a)) and (not math.isnan(b)) and a<9.082 and b>14.932
agg=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0]))
for r in rows:
    if r['receptor_slug'] in E: continue
    c=agg[r['cluster_id']][r['arm']]; c[0]+=1; c[1]+=act(r)
clus=sorted(agg)
def stat(pick,a,b):
    na=ka=nb=kb=0
    for c in pick:
        x=agg[c][a]; na+=x[0]; ka+=x[1]; y=agg[c][b]; nb+=y[0]; kb+=y[1]
    return kb/nb-ka/na
random.seed(20260909)
for a,b in [('decoy','cognate'),('apo','decoy'),('decoy','shuffled'),('shuffled','cognate')]:
    d=sorted(stat([random.choice(clus) for _ in clus],a,b) for _ in range(2000))
    print(a,'->',b, round(stat(clus,a,b),4), [round(d[50],4),round(d[1949],4)])
EOF
```

---

## 2. Findings table

### BLOCKING

| # | Finding | File + column recomputed | Claimed | My value |
|---|---|---|---|---|
| F-1 | No peptide arm; every co-input is a 350–394 aa full Gα | `interface_continuous.csv:n_partner_aa`; ladder-arm CIFs chain B | (parent) 21-mer co-input | min 350 aa; zero peptide arms |
| F-2 | `Δ α5-CT sequence` term swaps the whole subunit | `ladder_decomposition.csv:contrast` | "α5-CT sequence, 34.3%" | ~349/359 residues change; length 359→394 |
| F-3 | Protenix logit family CI mis-stated; sign verdict flips | `ladder_decomposition.csv:ci_lo,ci_hi` (protenix, family, logit) | SC-B-2: "**Logit CI [0.35, 1.05] squarely positive**" | frame_36 **[−0.047, +5.148]**; all_40 **[−0.011, +1.059]** — **both cross zero** |
| F-4 | Per-backbone logit family shares are not in the data | `ladder_decomposition.csv:term_share` | SC-B-2 / W-B-1: "all four backbones agree, 17–21%: boltz 17.4, chai 17.5, of3 20.9, protenix 17.5" | frame_36: **14.17 / 22.90 / 23.61 / 10.91**; all_40: **9.97 / 19.77 / 19.01 / 4.00**. Neither set matches; spread is 10.9–23.6%, not 17–21%. The only 17.37% in the file is the **panel** value. |
| F-5 | Family term is unsigned on 3 of 4 backbones, both scales, both frames | `ladder_decomposition.csv` | SC-B-2 presents family-term agreement | boltz, chai, protenix all have CI spanning zero on probability **and** logit, on **both** frames. Only OF3 signs. Panel signs. |
| F-6 | SC-B-1 continuous-axis medians reproduce on no axis, arm, frame or backbone — and the tilt axis is **not monotonic** | `01_rows/rows_tidy.csv:d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`; `04_ladder/ladder_continuous_distributions.csv:p50` | "medians 11.30/8.19/7.31/6.60 Å; 13.05/15.61/16.42/16.75 Å — **also monotonic** apo→decoy→shuffled→cognate" | npxxy **10.15/6.26/4.34/4.29**; tilt **12.22/16.81/17.69/17.53**. Tilt **shuffled > cognate on all four backbones**. Claimed npxxy apo 11.30 **exceeds every per-backbone value in the file** (max 10.58). |
| F-7 | `claim_answers.csv` ships row-boot CIs flagged as verified | `04_ladder/claim_answers.csv:ci_lo,ci_hi,matches_claim_sheet_bool` | apo [0.14,0.18], decoy [0.51,0.60], shuffled [0.78,0.84], cognate [0.87,0.91], all `True` | These are the **row-boot** intervals that `11_bootstrap_draws/ci_convention_audit_readme.md` was written to retire as "mislabeled row-boot". Authoritative cluster-boot is [0.081,0.256] / [0.445,0.664] / [0.747,0.869] / [0.838,0.942]. The apo interval is **4.4× too narrow**. |
| F-8 | Claim-sheet exclusion numbering does not match the shipped flags | `10_exclusions/exclusion_definitions.csv` vs `BLOCK_B_CLAIM_SHEET.md § Exclusion sets` | sheet: E-B-2 = AA2AR, E-B-3 = 15 non-native, E-B-4 = ceiling-pinned (≥0.98) | data: `excl_E_B_2` = OPRD/CNR1, `excl_E_B_3` = AA2AR, `excl_E_B_4` = 15 non-native. The sheet's E-B-4 (ceiling-pinned) **has no flag in the drop at all**. |

**F-8 consequences.** SC-B-6 says "Load-bearing exclusion: E-B-3 (non-native active
references)" → applying `excl_E_B_3` gives **AA2AR only**. SC-B-11 says "E-B-2 (AA2AR)" →
applying `excl_E_B_2` gives **OPRD/CNR1**. SC-B-2 says "E-B-4 (ceiling-pinning)" → applying
`excl_E_B_4` gives **the 15 non-native receptors**. Three of the four references are wrong, and
each silently yields a different analysis. `DATA_DICTIONARY.md` and
`EXPERIMENT_DOSSIER_BLOCK_B.md` §494 both agree with the *data*; the claim sheet is the outlier.

**Reproduce F-3/F-4/F-5:**
```bash
cd data/block_b && awk -F, 'NR==1||/delta_correct_family/' 05_decomposition/ladder_decomposition.csv | column -t -s,
```
**Reproduce F-6:**
```bash
cd data/block_b && python3 -c "
import csv,statistics,math
r=list(csv.DictReader(open('01_rows/rows_tidy.csv')))
def f(v):
    try: return float(v)
    except: return float('nan')
E={'EDNRA','EDNRB','GRPR','HRH3'}
for ax in ['d_npxxy_y558_y753_oh','d_gpcrdb_tm6_tilt_246_637_ca']:
    print(ax,[round(statistics.median([f(x[ax]) for x in r if x['arm']==a and x['receptor_slug'] not in E and not math.isnan(f(x[ax]))]),2) for a in ['apo','decoy','shuffled','cognate']])"
```

### MATERIAL

| # | Finding | File + column | Claimed | My value |
|---|---|---|---|---|
| F-9 | Every frame_36 CI is a **24**-cluster bootstrap, not 26 | `01_rows/rows_tidy.csv:cluster_id` | claim sheet header: "26 paralog clusters" on every frame_36 number | frame_36 drops the whole `endothelin` (EDNRA, EDNRB) and `bombesin` (GRPR) clusters → **24** clusters. Resample unit count overstated by 8% on every headline interval. |
| F-10 | SC-B-3 engagement-cutoff sweep is misattributed and directionally wrong | `06_interface/interface_2x2.csv:p_active_given_engaged` | "nearly flat 10→20 Å at cognate (0.897→0.893); on decoy the sweep moves 0.53→0.66" | frame_36 / panel / two-instrument: cognate **0.316 → 0.893** (collapses at 10 Å, n_engaged = **19** of 7,200); decoy **0.714 → 0.665** — it **falls**, not rises. The quoted 0.897 exists only in **frame_40 × tilt_only × boltz**. No stratum in the file produces the decoy 0.53→0.66 sweep. |
| F-11 | SC-B-12 names an arm that has no partner, and its cognate anchor number is wrong | `06_interface/interface_continuous.csv:contact_register_last5_json` | "counts on TM6 apex fall **apo → shuffled → decoy** (6.33: **327** → 297 → 156)" | apo cells carry an **empty** register on all 160 cells — apo has no partner chain to contact. Recomputed 6.33 counts: **cognate 304**, shuffled 297, decoy **152**. Cognate and shuffled top-8 tables reproduce **exactly**; the decoy row is 3–5 low on every position, i.e. computed on a slightly different engaged-cell selection than the shipped `cell_engaged_20` flag. |
| F-12 | Ceiling saturation is far more severe than C-B-7 conveys | `04_ladder/ladder_per_receptor.csv:cognate_rate,shuffled_rate` | "24–34 of 40 per backbone are ceiling-pinned" (true) | **115 of 160** cells have cognate ≥ 0.98; **106 of 160 are exactly 1.000**; **89 of 160 shuffled cells are exactly 1.000**; on **89 cells shuffled and cognate are both 1.000**, so the family term is structurally zero on 56% of the panel. 16 cells have shuffled > cognate (negative family term). Only 134/160 cells are fully monotone. |
| F-13 | The logit scale — offered as the fix for ceiling artefacts — is itself artefact-driven on Protenix | `11_bootstrap_draws/ladder_decomposition_bootstrap_draws.csv` | SC-B-2 / W-B-1: use the logit share to escape ceiling compression | The ε = 1/8000 continuity clamp is log(7999) = **8.987**. Protenix family-term logit draws: **218 of 1000 exceed 3.0**, max 5.898 — driving the [−0.047, **+5.148**] interval. Protenix occupancy logit has **12 draws at/over the clamp**. The logit scale does not rescue Protenix; it relocates the artefact. |
| F-14 | Silent exclusion inside SC-B-11's headline n | `08_covariates/ladder_height_covariates.csv` | SC-B-11 table prints "n = 28" for Δ_ref NPxxY × continuous | **12 of 40 receptors are dropped** by an undocumented rule: 8 have NaN `family_term_continuous` (ceiling-saturated, term undefined) and 6 have NaN `delta_ref_npxxy`. Dropped set = ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, EDNRB, FSHR, GRPR, HRH3, LSHR, OX2R. Neither `DATA_DICTIONARY.md` nor `10_exclusions/` defines this rule. **This is the one place a headline number applies an exclusion the dictionary does not define.** |
| F-15 | SC-B-11's title overclaims relative to its own body | `08_covariates/ladder_height_regressions.csv:ci_lo_all,ci_hi_all` | title: "**No** ladder-height covariate has a slope excluding zero at 95% CI" | The six *named* predictors do all span zero (verified exactly). But the same file carries `cognate_family=*` predictors, and **panel `cognate_family=Gs` continuous slope = +1.309 [+0.281, +2.337], excludes zero** (n=5). Six more per-backbone slopes exclude zero. 10 of 16 panel rows are not reported in the claim sheet. |
| F-16 | MSA is **not** constant across arms; the audit checks the wrong pair | `03_msa_audit/msa_depth_report.md` | "decoy depth is NOT systematically lower than cognate depth… depth is not a plausible mediator" | Correct for decoy-vs-cognate (±3.7%, verified as reported). But the confounded contrast is **decoy → shuffled**, and there the partner MSA is a *different protein's* alignment entirely (e.g. Gαq 14,368 rows → Gαs 12,080 rows). The audit never compares shuffled to decoy. Additionally the report states `pairing_key` is empty in all 120 cache files, so **paired-MSA depth cannot be assessed at all** — it names this as "the single biggest analytical gap". Any arm effect at decoy→shuffled remains confounded with alignment. |
| F-17 | Half the shipped decomposition CIs cannot be reproduced from the drop | `05_decomposition/ladder_decomposition.csv` vs `..._bootstrap_draws.csv` | dictionary implies draws back the file | Draws cover **`reproduction_36` only** (30 groups × 1000). All **30 `all_40` CI rows have no draws**. The 30 frame_36 rows reproduce to 4 dp on both bounds — flawless — but the all_40 half is unverifiable. |
| F-18 | One third of donor-residual CIs have no draws | `07_donor_residuals/donor_class_residuals_summary.csv` (270 rows) vs draws (180 groups) | — | **90 of 270** summary rows have no shipped draws. Of the 180 checkable, 167 reproduce exactly; 12 differ at the 3rd–4th decimal (percentile interpolation); **1 differs materially**: `(of3, APO, Gq, residual_npxxy)` published lo **2.9343**, recomputed **3.4576**. |
| F-19 | `Δ_to_active` is non-monotonic and the shuffled arm overshoots cognate | `01_rows/rows_tidy.csv:delta_to_active` | SC-B-1 table prints apo −5.93 / decoy −1.35 / shuffled +0.04 / cognate −0.35 (reproduces exactly) | The values reproduce but the reading does not: **shuffled sits closer to the active reference (\|+0.038\|) than cognate does (\|−0.353\|)**. Same pattern on `d_tm6_r350_r630_ca` (shuffled 15.63 > cognate 14.91) and `d_dry_sidechain` (17.93 > 17.66). On the continuous geometry the **wrong-family** Gα opens TM6 *further* than the cognate one; only the binary threshold puts cognate on top. Nowhere reported. |
| F-20 | SC-B-4's mechanism cell is thin and carries no interval | `06_interface/interface_pif_connector.csv` | "decoy engaged-but-inactive… statistically indistinguishable from apo" | All five n / median / IQR reproduce **exactly** (47 / 15.416 / [14.86, 15.86]). But n = 47 **cells**, i.e. **10–13 per backbone**, and no CI is computed anywhere in the drop for the PIF axis. "Statistically indistinguishable" is asserted without a statistic. |
| F-21 | "4× median depth" is 1.65× | `01_rows/rows_tidy.csv:d_ga_alpha5_r350_ca` | SC-B-3: "the 20 Å cutoff is permissive at cognate (**4×** median depth of 12.19 Å)" | median cognate tip = **12.15 Å**; 20 / 12.15 = **1.65×**. Same error in the dossier §4b. |

### MINOR

| # | Finding | Detail |
|---|---|---|
| F-22 | `threshold_npxxy_oh_active_lt` ships as **9.08**, dictionary and claim sheet say **9.082**. 5 rows fall in [9.08, 9.082). Effect on the ladder: decoy 0.5579 → 0.5578. Immaterial, but the pin is not the pin. |
| F-23 | Three different published CI sets for SC-B-1: `claim_answers.csv` [0.14,0.18]…, claim sheet + `ladder_four_scorings.csv` [0.081,0.256]…, `ci_convention_audit_sc_b_1.csv` [0.083,0.259]…. The last two differ by ~0.002 (reseeding); the first is a different estimator (see F-7). |
| F-24 | `receptor_class` = `"A"` in the data; dictionary says `"class_A"`. |
| F-25 | `confidence_flag` values are `{high, borderline, low}`; dictionary says `{ok, low_min_plddt, …}`. |
| F-26 | `plddt_at_anchors` is a **JSON list of 20 floats**, not a scalar, and not "the 6 BW anchors" as the dictionary states. |
| F-27 | Backbone stratum is `panel` in `ladder_four_scorings.csv` / `ladder_decomposition.csv` but `panel_all` in `interface_2x2.csv`; dictionary says `panel_all` for the ladder file (wrong). |
| F-28 | Frame labels are `{all_40, reproduction_36}` in 04/05 but `{frame_36, frame_40}` in 06. Same two frames, two vocabularies, one drop. |
| F-29 | `ladder_continuous_distributions.csv` has `p50` and `n_nan`; dictionary says `median` and omits `n_nan`. It has **no panel rows** (4 backbones only) — so SC-B-1's *panel* continuous medians have no source row in their cited file (see F-6). |
| F-30 | `donor_class_residuals_bootstrap_draws.csv` columns are `backbone, donor_ga_class, cognate_ga_class, axis, draw_idx, median`; dictionary says `draw_id, …, statistic, value`. |
| F-31 | SC-B-12 cites `interface_pif_connector.csv` as its source; that file has **no register column**. The data is in `interface_continuous.csv`. |
| F-32 | Two different CIs for the same SC-B-6 quantity inside the drop: `phase5_power_analysis.csv` panel all = [−0.2883, +0.2990]; `donor_class_residuals_summary.csv` = [−0.3066, +0.3010]; my reproduction from draws = [−0.3067, +0.3011]. The claim sheet quotes **[−0.29, +0.30]**, the narrower of the two. |
| F-33 | `interface_chai_plddt_inversion.csv` cognate/non_engaged row: `mean` = 67.23 sits **outside** its own `[lo95, hi95]` = [68.04, 69.96] (the interval is on the median, 69.87). n = 5. |
| F-34 | **All 101 rows** across the nine `claim_answers.csv` files report `matches_claim_sheet_bool = True`, including the rows carrying F-4 (shares not in the source file), F-6 (medians not in the source file) and F-7 (wrong estimator). The flag is asserted, not computed. |
| F-35 | Chai's SC-B-6 bootstrap is degenerate: `all_ci_lo` = **−4.63**, native **−5.27** on `residual_tilt` (vs panel −0.29). The claim sheet's "CI width unchanged" applies to the panel only. |

---

## 3. What reproduced exactly (recomputed, not confirmed)

These are clean. I recomputed each from `01_rows/rows_tidy.csv` or the shipped draws.

| Claim | Result |
|---|---|
| **Grid completeness (SC-B-10)** | 32,000 rows; 640 cells; **every** cell exactly 50 rows; **every** cell exactly 5 distinct seeds; single `scorer_git_sha`; single `ref_set_csv_sha256`; `passed=True` on all rows. ✓ |
| **Four-arm ladder (SC-B-1 binary)** | frame_36 panel **0.1579 / 0.5579 / 0.8094 / 0.8911** — matches to 4 dp. All 40 rows of `ladder_four_scorings.csv` (n_rows, binary_predicate, delta_to_active_median, n_receptors) reproduce; **zero mismatches**. |
| **E-B-1 membership** | NaN NPxxY is confined to exactly EDNRA/EDNRB/GRPR/HRH3, 800 rows each = 3,200. Zero NaN on the tilt axis. ✓ |
| **Decomposition (SC-B-2 estimates)** | All **60 rows** of `ladder_decomposition.csv` — estimate, share and total, both scales, both frames — reproduce exactly. **Zero mismatches.** |
| **Decomposition CIs** | All **30 `reproduction_36` CI pairs** reproduce from the shipped draws to 4 dp on both bounds. |
| **2×2 engagement (SC-B-3)** | cognate 0.9983 / 0.8926, shuffled 0.9674 / 0.8353, decoy 0.7037 / 0.6647, decoy n_engaged_but_inactive = **1,699**. All CIs match to ±0.001. ✓ |
| **PIF connector (SC-B-4)** | All five subsets: n = 160/130/118/69/**47**, medians 15.347/16.038/16.004/16.034/**15.416**, IQRs all match. Per-backbone boltz 15.09 / chai 15.18 / protenix 15.40 / of3 15.83. ✓ |
| **Fold integrity (SC-B-5)** | All **16** arm × backbone pass rates match to 3 dp; panel-wide **0.9876** (claimed 0.988); 0 NaN rows. ✓ |
| **Donor residuals (SC-B-6)** | panel all **+0.0237 [−0.288, +0.299]**, native **−0.0616 [−0.408, +0.211]** — matches the claim sheet. 167 of 180 checkable CIs reproduce exactly. |
| **Construct identity (SC-B-8)** | All 40 decoys: composition preserved (`Counter` equal), length 11, Hamming matches the table on all 40, min 7 / max 11 / **mean 9.53**, no scramble equals its parent, every receptor gets a distinct scramble. Verified independently from a CIF: byte-identical over the first **349** residues. ✓ |
| **Contact register (SC-B-12)** | cognate and shuffled top-8 BW positions and counts reproduce **exactly** (3.50 379, 8.47 325, 6.36 313, 6.33 304 …). Decoy row off by 3–5 (F-11). |
| **Covariates (SC-B-11 named predictors)** | All six panel slopes, CIs and n values match exactly. ✓ |
| **Ceiling counts (W-B-1)** | "24–34 of 40 per backbone" verified: of3 24, chai 28, boltz 29, protenix 34. ✓ |
| **Drop integrity** | **103 / 103** files match their `MANIFEST.json` sha256. `reference_set.blockb_pinned.csv` hashes to `6ee2cad8…5202ef` as pinned in all 32,000 rows. ✓ |

---

## 4. Powering of the decoy and shuffled arms

Asked explicitly in the brief.

**Row-level n is ample.** decoy and shuffled each carry 8,000 rows (7,200 on frame_36), 2,000
per backbone, 50 per cell, on all 640 cells. No arm shortfall anywhere.

**Cell-level n on the mechanism claims is thin.**

- decoy engaged-but-inactive: **1,699 rows** but only **47 cells** (10–13 per backbone) — and
  the PIF claim (SC-B-4) is a statement about cell-medians (F-20).
- The independent bootstrap unit is the **paralog cluster**, of which frame_36 has **24**, not
  26 (F-9). Nine of the 26 clusters are singletons in the shuffled design: only **three
  distinct donor sequences** are used across all 40 shuffled arms (`alphas` × 33, `alphai1` ×
  6, `alpha13` × 1). So the shuffled arm's effective diversity on the *partner* side is 3, not
  40. Any "wrong family" statement is a statement about **Gαs-into-Gi-receptor** in 33 of 40
  cases.
- The load-bearing SC-B-6 cell is 24 receptors (20 native) — this is stated and handled well.

**Does the shuffled control preserve composition?** **No — and it is not the composition
control.** The naming is inverted relative to the usual convention and relative to how the
paper's controls are described:

| Block B arm | what it actually is | composition preserved? |
|---|---|---|
| **decoy** | cognate Gα with the 11-residue α5-CT **permuted** | **Yes** — `Counter(scrambled) == Counter(original)` verified on all 40 |
| **shuffled** | a **different family's wild-type Gα** | No — different protein, different length (359 vs 394), nothing preserved |

So the composition-preserving scramble control in Block B is the arm called *decoy*, and it
scrambles only 11 of ~360 residues. The arm called *shuffled* is not a shuffle. Any manuscript
sentence of the form "our shuffled control preserves amino-acid composition" would be false as
applied to Block B's shuffled arm and would need to point at the decoy arm instead.

---

## 5. What I could NOT check, and why

Reported explicitly, because an unchecked item reported as clean is the worst outcome.

1. **SC-B-7 (templates off).** Unverifiable from this drop. The evidence is class (b) launcher
   static analysis and class (c) upstream defaults; the drop ships **no** `qsub/rerun_*.sh`, no
   `_<backbone>_status.json`, and no `runtime_config` echo on any row. The claim sheet itself
   labels this "not class (a)". I confirmed only that no template-related column exists in
   `rows_tidy.csv` — which is consistent with the claim and equally consistent with templates
   having been on. **C-B-1 is correctly flagged and I could not strengthen or weaken it.**
2. **SC-B-9 (decoy edit reaches the model as an aligned MSA column).** Unverifiable. No
   `.aligned.pqt`, no `.a3m`, no `inference_query_set.json` in the drop. The OF3 half is
   admitted to be unverifiable even upstream (raw MSAs purged from `$TMPDIR`). The Chai
   non-read finding — 0/40 uppercase-aligned — is the load-bearing one and I could not audit it.
   Note this matters for F-2: if Chai does not read the decoy edit, Chai's decoy arm is
   MSA-identical to its cognate arm, which would make Chai's apo→decoy term partly a
   *cognate*-MSA term.
3. **SC-B-10's recovery journey.** `rescore_parallel.provenance.json`, the round-1/2/3 reports
   and the 300 silent-fails patch are not in the drop. I verified only the **end state**
   (32,000/32,000, zero sentinel seeds), which is clean.
4. **The geometry itself.** No scorer source, and only **11 CIFs** for 32,000 rows. I could not
   check that `d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`, `pif_sum_ca`,
   `tm6_helicity_6_30_6_50` or `rmsd_to_*_ref` are computed correctly from structure. Every
   ladder number in this review is conditional on those columns being right.
5. **Input FASTAs.** `refs/constructs_block_b/*.fasta` are not shipped. I verified the
   construct claims by extracting chain sequences from the four GHSR ladder CIFs — a strong
   proxy (it is what the model actually emitted) but a sample of **one receptor**. The other
   39 rest on `construct_build_report.md` plus the `n_partner_aa` length distribution, which
   is consistent with it.
6. **Reference curation (SC-B-13).** No PDB files, no method/resolution columns
   (`ASSUMED_NOT_VERIFIED_E.md` records these as never retrieved). I verified the pinned
   reference file's sha256 and nothing about whether the chosen PDBs are the right ones. Note
   `ASSUMED_NOT_VERIFIED_E.md` already concedes the ADRB2 active reference is `4LDE`
   (nanobody) while the canonical native `3SN6` heterotrimer exists and was not selected.
7. **Whether the decoy scramble is reproducible from its seed.**
   `build_shuffled_decoy_constructs.py` is not shipped. I verified the *outputs* are internally
   consistent (composition, Hamming, distinctness) but not that re-running regenerates them.
   C-B-12 already records that the generator SHAs are empty.
8. **Paired-MSA depth.** Structurally impossible from the shipped artefacts —
   `msa_depth_report.md` records `pairing_key` as empty on every row of all 120 cache files.
   For a receptor–Gα docking experiment this is the depth measure that would matter most.
9. **Cross-block consistency.** I did not compare Block B against Block A or Block C, or
   against `analysis/block_b/verify_claims.py` / `DISCREPANCY_REPORT.md` — this pass was
   deliberately independent of the existing verification so the findings above are arrived at
   from the data alone. Some may duplicate what that report already records; **F-1 through F-8
   should be checked against it before being treated as new.**

---

## 6. Recommended actions (report only — nothing was changed)

1. **Settle F-1 first.** Either the paper's titular claim moves to a block that supplies a
   21-mer, or the claim changes to what Block B tests: partner *identity* versus partner
   *mass*, with a whole-Gα co-input.
2. **Retire the three-term decomposition as the headline** and promote the clean
   **decoy → cognate** contrast (+0.333 [+0.244, +0.435], only the 11-residue α5-CT tail
   changes). It is the strongest honest α5-CT-sequence sentence in the block.
3. **Correct or withdraw the SC-B-2 per-backbone paragraph** (F-3, F-4, F-5). As written it
   states a positive CI where the data gives one crossing zero, and asserts a four-backbone
   agreement the data contradicts.
4. **Fix the exclusion numbering in the claim sheet** to match the shipped flags (F-8), or the
   first person to apply an exclusion will apply the wrong one.
5. **Correct "26 clusters" to 24 on every frame_36 interval** (F-9).
6. **Withdraw or re-source the SC-B-1 continuous-median sentence** (F-6), and report the tilt
   non-monotonicity (F-19) rather than letting the binary predicate hide it — it is a real
   result and a reviewer will find it.
7. **Regenerate `claim_answers.csv`** so `matches_claim_sheet_bool` is computed rather than
   asserted (F-34), and so `04_ladder`'s CI columns carry cluster-boot intervals (F-7).
