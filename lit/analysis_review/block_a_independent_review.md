# Block A — independent adversarial verification

**Date**: 2026-09-10. **Reviewer**: independent recompute session (lit-side, read-only).
**Scope**: `data/block_a/` (read-only), `analysis/block_a/` (read as claims, not truth),
and the Block A sentences in `manuscript/`.
**Method**: every number below was recomputed with pandas directly from the tidy files.
No function, filter or helper from `analysis/block_a/verify_claims.py` was reused, and
that script was never executed (it writes `verify_claims_results.json`, which is out of
bounds for this review).

**Bottom line**: the shipped tidy files are internally excellent — 79 of 80 MANIFEST
sha256 digests match, and every aggregate I tried to rebuild from `01_rows/` rebuilt
bit-exactly. The defects are in the claim sheet, in `analysis/block_a/`, and in the
manuscript. **I found 15 issues not among the 21 recorded, five of them BLOCKING, and I
show one recorded discrepancy (D-A-24) to be wrong.**

---

## 1. Findings

Severity: **BLOCKING** = a headline claim changes or is withdrawn; **MATERIAL** = a number,
denominator or Methods sentence must change; **MINOR** = precision/wording.

| # | Sev | What I recomputed (file :: column) | Claimed | My value | Reproduction |
|---|---|---|---|---|---|
| **N-1** | **BLOCKING** | `01_rows/block_a_rows.csv` :: `plddt_at_anchors` vs `rmsd_to_active_ref`, **within arm** | SC-11 / Flag 35: pLDDT tracks correctness; OF3 `anchor_mean` r = −0.626, "strongest signal in the campaign"; signed on 2 of 4 backbones | Pooled r reproduces exactly (−0.2207 / −0.1605 / −0.6255 / +0.0684). **Arm-centred it collapses: boltz −0.221 → +0.123 (sign reverses), of3 −0.626 → −0.079, chai −0.160 → −0.018, protenix +0.068 → +0.420.** Within the apo arm alone the correlation is **positive on all four backbones** (+0.251, +0.245, +0.313, +0.649) | `scratchpad/r11.py`, `r12.py` — see §1.1 |
| **N-2** | **BLOCKING** | `manuscript/main.tex:81`, `manuscript/si.tex:176-178` vs `01_rows` :: `input_state_claim`, `n_interface_contacts_ga_receptor` | main.tex graphical abstract: "with the **supplied** α5 C-terminal 21-mer"; si.tex Fig. ba8: "only the 21-mer **supplied to the model** is drawn, not the full Gα" | **False.** `input_state_claim` has exactly two values, `apo` (4,795) and `Ga-coupled-active` (4,695); the cognate arm carries whole-Gα metrics on all 4,695 rows. `manuscript/sections/methods.tex:324` states the truth ("Every partner arm supplies a complete Gα subunit… not an input in either campaign") and the two captions contradict it | `python3 -c "import pandas as pd;r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False);print(pd.crosstab(r.input_state_claim,r.arm))"` |
| **N-3** | **BLOCKING** | `07_clusters_and_holdout/holdout_counts.csv` :: `cutoff_date` vs `manuscript/sections/methods.tex:226-228` | Methods: Boltz-2 **2023-06-01**, Protenix2 **2021-09-30**, Chai-1 **2021-01-12** | Drop uses boltz **2021-09-30**, chai **2023-01-13**, of3 **2023-01-13**, protenix **2023-01-13**. **All four disagree with Methods.** C-9 and Flag 3 make this holdout the *sole* source of prospectivity | `python3 -c "import pandas as pd;print(pd.read_csv('data/block_a/07_clusters_and_holdout/holdout_counts.csv'))"` |
| **N-4** | **BLOCKING** | `01_rows` :: `active`, `rmsd_to_active_ref` vs `DISCREPANCY_REPORT.md` D-A-24 | D-A-24: "4,866 does not reproduce **under any predicate definition tried**… neither 4,866 nor 4,256 appears anywhere in `data/block_a/`"; recorded as standing mismatch `CAP12`; escalated as ask 3 in `DATA_REQUESTS.md` | **Both reproduce exactly.** `rows.active.sum()` = **4,866**; `rows[rows.active].rmsd_to_active_ref.notna().sum()` = **4,256**. The same script's own `CORPUS` check asserts 4,866 = `rows.active.sum()` and passes. `CAP12` fails only because it re-derives the predicate with the Class-A two-instrument rule, which the report's own "Not reproduced" section already identifies as wrong for a class-conditional column | `python3 -c "import pandas as pd;r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False);print(r.active.sum(), r[r.active].rmsd_to_active_ref.notna().sum())"` |
| **N-5** | **BLOCKING** | `08_exclusions/exclusion_sweep.csv` :: `pct_shift_from_baseline` | Claim sheet Statement B, SC-1, SC-2: "the fraction-of-way-to-active shifts by **≤ 0.5%** under every single combination"; "invariant to every specified exclusion set" | **False in 6 of 32 fraction cells.** chai `all_E1-E5` **+3.27%**, chai `E4` +1.58%, chai `E1+E2+E4+E5` −1.40%, of3 `all_E1-E5` −1.32%, boltz `all_E1-E5` −0.58%. On `median_tilt_shift` chai moves **+222%** under `all_E1-E5` and **+94%** under E4 — SC-1's own table concedes "E4 doubles Chai" two lines under a headline claiming ≤0.5% | `python3 -c "import pandas as pd;s=pd.read_csv('data/block_a/08_exclusions/exclusion_sweep.csv');print(s[s.pct_shift_from_baseline.abs()>0.5][['metric','backbone','exclusion_set','pct_shift_from_baseline']])"` |
| **N-6** | MATERIAL | `02_references/reference_metadata.csv` :: `transducer_present`, `state`, `is_panel` | Flag 32: "**6/48** active refs are not Gα-coupled"; `methods.tex:229`: "**The reference active states are themselves G protein complexes**" | Of 44 panel active-role PDBs, `transducer_present` is True on **13**; **27 of the 40 receptors with an active reference have no transducer-bearing active reference at all**. The column is also internally inconsistent: 7JVR (DRD2–Gi), 6X18 (GLP1R–Gs), 6LMK (GCGR–Gs), 8FLQ (PTH1R–Gs), 6P9X (CRHR1–Gs) are all **False**, while 4LDE (Nb80-only) and 6OS2 (nanobody) are **True**; `mini_G` → False but `mini_Gs`/`mini_Gq` → True. **Either Flag 32 understates by ~4.5×, or the column is wrong. No definition of it ships.** Nothing may be built on it either way | `python3 -c "import pandas as pd;m=pd.read_csv('data/block_a/02_references/reference_metadata.csv');a=m[m.is_panel&(m.state=='active')];print(a.transducer_present.value_counts());print(a.groupby('receptor').transducer_present.any().value_counts())"` |
| **N-7** | MATERIAL | `02_references/reference_predicates.csv` :: `predicate_call` vs `manuscript/sections/results.tex:14,16` | "passed on **159** and deviated on nine… **159/168** measures internal consistency" | 168 rows split **150 `expected_pass`+`expected_fail` / 9 deviations / 9 `missing_axis`**. The nine unevaluable rows (7 inactive, 2 active) are being counted as passes. Correct: 150/159 evaluable (94.3%) or 150/168 (89.3%), **not 159/168 (94.6%)**. This is the opening sentence of Results | `python3 -c "import pandas as pd;print(pd.read_csv('data/block_a/02_references/reference_predicates.csv').predicate_call.value_counts())"` |
| **N-8** | MATERIAL | `06_confidence/plddt_correlations.csv` :: `cluster_ci_*` vs `receptor_ci_*` | SC-11 heads its interval column **"cluster-boot"** | Same defect as the recorded D5, but on SC-11, which D5 does not cover. Quoted boltz [−0.357,−0.092] matches **receptor** [−0.3565,−0.0887] (d=0.004) not cluster [−0.3525,−0.1208] (d=0.033); chai and protenix likewise. **OF3's quoted [−0.827, −0.601] matches neither** (d=0.212 / 0.189) and **appears nowhere in the drop** — it is attached to the claim sheet's "strongest signal in the campaign" | `scratchpad/r9.py` |
| **N-9** | MATERIAL | `01_rows` :: `d_gpcrdb_tm6_tilt_246_637_ca`, receptor `AA2AR` | SC-5: "apo × 4 … Δ d_TM6 **7.4–8.1 Å**"; cognate 17.9–18.9; "a TM6 tilt-distance shift of **~11 Å** across arms" | **No AA2AR row anywhere in the corpus has tilt between 7.4 and 8.1 Å.** Full apo range is 11.58–17.50 Å; cell medians 11.82/12.15/11.92/11.88. Cognate cell medians 17.91–18.31. **Actual across-arm shift is 5.4–6.4 Å, not ~11 Å.** The RMSD half of SC-5 does reproduce (apo→inactive 0.38–0.67; cognate→active 0.53–0.71) | `python3 -c "import pandas as pd;r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False);a=r[r.receptor=='AA2AR'];print(a.groupby(['backbone','arm']).d_gpcrdb_tm6_tilt_246_637_ca.describe())"` |
| **N-10** | MATERIAL | `03_aggregates/receptor_summary.csv` :: `fraction_of_way_to_active` | SC-2 / results.tex: "reach **89–95%** of the way to the active reference" | The estimator is a **per-receptor ratio of medians with a signed, near-zero-capable denominator**, and its distribution is unbounded: OF3 mean **6.37**, SD **33.85**, **max 212.27**; **48 of 156** receptor×backbone values exceed 1.0 and **5 are negative** (min −1.31). The headline is the *median* of that. Quoting it as a percentage-of-the-way implies a bounded quantity it is not, and hides that ~31% of cells overshoot the active reference | `python3 -c "import pandas as pd;s=pd.read_csv('data/block_a/03_aggregates/receptor_summary.csv');f=s.fraction_of_way_to_active.dropna();print(s.groupby('backbone').fraction_of_way_to_active.describe());print((f>1).sum(),(f<0).sum(),len(f))"` |
| **N-11** | MATERIAL | `02_references/reference_metadata.csv` :: `construct_contradicted_by_rcsb`, `engineered_mutation_count`, `engineered_mutation_positions` | Flag 42 / C-11: "**52 / 127 = 40%** of evaluable PDBs have `construct = wt` contradicted by RCSB"; Flag 14 asks which refs carry engineered residues in the predicate windows | All three columns are **0 of 168 non-null**. The 40% headline has **no supporting data anywhere in the drop**; `construct_annotation_on_disk` is `wt` on 167 of 168. The fusion columns *are* populated (18 panel PDBs `predicate_window_hit`), so half of Flag 14 is answerable and half is not | `python3 -c "import pandas as pd;m=pd.read_csv('data/block_a/02_references/reference_metadata.csv');print(m[['construct_contradicted_by_rcsb','engineered_mutation_count','engineered_mutation_positions']].notna().sum())"` |
| **N-12** | MATERIAL | `04_amplitude/attenuation_sensitivity.csv` :: `slope_corrected` | Flag 21 REFINED / Flag 41: at σ_err = 1.0 Å, "Chai **−1.77** (physically impossible) and OF3 **+1.06** (near unity)" | At σ_err = 1.0 the shipped values are **chai −2.4400** and **of3 +0.8606** (boltz −1.1024, protenix +0.3045). Neither −1.77 nor +1.06 occurs at any σ in the 0–2 Å grid for those backbones. The *conclusion* (the correction is unstable on tilt) survives; the two quoted numbers do not | `python3 -c "import pandas as pd;a=pd.read_csv('data/block_a/04_amplitude/attenuation_sensitivity.csv');print(a[(a.axis=='tilt')&(a.sigma_err==1.0)][['backbone','slope_ols','slope_corrected','unstable']])"` |
| **N-13** | MATERIAL | `01_rows` :: `excl_E1` (rule: cell mean `plddt_mean` < 50) | E1 presented as a pre-specified exclusion "by cause" | **E1 is a confidence-based filter**, and the cell it removes (ACM1/cognate/protenix, 25 rows) has a predicate-active rate of **0.00** — the worst cognate cell in the corpus. Applying it can only raise the headline: `exclusion_sweep` shows protenix `cognate_active_rate` **+2.17%** under E1 alone. In a paper whose thesis is that confidence does not track state correctness, a confidence-thresholded exclusion that improves the state headline needs to be argued, not just declared pre-specified | `python3 -c "import pandas as pd;s=pd.read_csv('data/block_a/08_exclusions/exclusion_sweep.csv');print(s[(s.metric=='cognate_active_rate')&(s.exclusion_set=='E1')])"` |
| **N-14** | MATERIAL | `08_exclusions/exclusion_sweep.csv` :: `value`, set `E1+E2+E4+E5` | SC-2 table, E1+E2+E4+E5 column: boltz 0.9410, chai 0.8878, of3 0.9108, protenix 0.9113 | **All four wrong**: 0.9472 / 0.8718 / 0.9296 / 0.9160 (of3 off by 0.019). The recorded D6 covers only the *baseline* fractions, not this column. I reproduced the whole sweep independently from `01_rows` and it matches the shipped sweep to 4 dp on every cell | `scratchpad/r15.py` |
| **N-15** | MATERIAL | `01_rows` :: `(receptor, backbone, arm)` cells | SC-10 "Block A ran **48** receptors"; `headline_by_backbone` :: `n_receptors_tilt` = `n_receptors_delta` = 48 | **FZD4 has no cognate arm on any backbone** — 380 cells, not 384. So the panel is 48 apo / **47 cognate**, and every cognate-arm and shift statistic rests on 47. `n_receptors_tilt` = 48 against 47 non-null; `n_receptors_delta` = 48 against 39. (The recorded D15 notes the column overstatement but not the missing FZD4 cognate arm as its cause.) Two further cells carry 20 rows not 25: `B1B1U5/boltz/apo`, `CRHR1/boltz/cognate` | `python3 -c "import pandas as pd,itertools;r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False);h=set(map(tuple,r[['receptor','backbone','arm']].drop_duplicates().values));a=set(itertools.product(r.receptor.unique(),r.backbone.unique(),['apo','cognate']));print(sorted(a-h));print(r.groupby(['receptor','backbone','arm']).size().value_counts())"` |
| **N-16** | MINOR | `01_rows` :: `tm6_helicity_6_30_6_50`, `tm6_helicity_pass` | SC-8: "**21** low-helicity cells cluster on Class B secretin receptors" | 21 reproduces under no definition I tried: cell median < 0.80 → **13**; any failing row → **28**; pass rate < 0.5 → **13**; pass rate = 0 → **5**. And the Class A share is understated: 13 of the 28 cells with any failure are Class A (AGTR1 38 failing rows, LT4R1 26). The **rates all reproduce exactly** (overall 96.333%; 95.645 / 95.074 / 97.726 / 96.884) | `scratchpad/r22.py` |
| **N-17** | MINOR | `01_rows` :: `d_gpcrdb_tm6_tilt_246_637_ca` on `excl_E1` rows | Flag 46: broken cell has "tilt **> 30 Å** median" | Median is **25.76 Å**. Everything else in Flag 46 reproduces: 25 rows, mean `plddt_mean` 38.66, NPxxY median 28.17, `passed` True on all 25 | `python3 -c "import pandas as pd;r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False);b=r[r.excl_E1.astype(bool)];print(len(b),b.plddt_mean.mean(),b.d_gpcrdb_tm6_tilt_246_637_ca.median(),b.d_npxxy_oh.median())"` |
| **N-18** | MINOR | `01_rows` :: `npxxy_active`, `tilt_active`, Class A | SC-4: Class A agreement 89.92%, of3 83.67%, "n=32 deriv panel" | 89.94% and **83.73%** on the 32-receptor set; boltz/chai/protenix reproduce exactly (90.23 / 93.40 / 92.40); κ = 0.794 ≈ 0.79. Only **30** of the 32 receptors have both axes measurable, so "n=32" is the wrong n for this metric. Class B kink-vs-tilt 81.64%, κ = 0.305 both reproduce exactly | `scratchpad/r21.py` |
| **N-19** | MINOR | `02_references/reference_metadata.csv` :: `entry_json_cached` vs `denominator_populations.csv` :: `evaluable_audit_set` | `evaluable_audit_set` = **162**, defined as "PDBs with cached RCSB entry.json" | `entry_json_cached` is True on **163**. Even the drop's own reconciliation number is off by one against the table it is reconciling | `python3 -c "import pandas as pd;print(pd.read_csv('data/block_a/02_references/reference_metadata.csv').entry_json_cached.sum())"` |
| **N-20** | MINOR | `04_amplitude/amplitude_fits.csv` :: `n_receptors`, `sd_predictor`; `02_references/reference_separation.csv` | SC-3: NPxxY "n=34, SD(Δref) = 4.71"; tilt "SD = 1.19 across the **40** Class A receptors" | Extends recorded D1/D3 with the source table: `reference_separation` gives **28** panel receptors with a valid NPxxY Δ and **40** with a valid tilt Δ, of which only **32** are Class A. SD on those exact populations is **5.2222** (NPxxY, n=28) and **1.1706** (tilt, n=32). **Neither 34/4.71 nor 40/1.19 exists in any shipped object.** All 24 slopes, r², n and SD in `amplitude_fits.csv` reproduce bit-exactly from `amplitude_points.csv` | `scratchpad/r23.py`, `r28.py` |
| **N-21** | MINOR | `manuscript/main.tex:59` vs `manuscript/si.tex:18` | — | The two titles differ: main is "A Gα α5 C-terminal peptide co-input…", SI is "A **21-residue** Gα α5 C-terminal peptide co-input…". Given N-2 the SI variant is the more exposed of the two | `grep -n "co-input drives" manuscript/main.tex manuscript/si.tex` |
| **N-22** | MINOR | `MANIFEST.json` :: `source_rows_csv_sha256` vs `01_rows/block_a_rows.csv` | README: "Corpus row source … SHA-256 `94ff63b1…`" | The shipped tidy file hashes to `28852f60…`. This is presumably the upstream pre-tidy `rows.csv`, but nothing in the drop lets a reader confirm that, so the drop's headline provenance hash is unverifiable from the drop. **Every other digest is clean**: 79 of 80 MANIFEST entries match byte-for-byte (the exception is `MANIFEST.json` hashing itself), and every declared `row_count` matches | `python3 -c "import json,hashlib;m=json.load(open('data/block_a/MANIFEST.json'));print(m['source_rows_csv_sha256']);print(hashlib.sha256(open('data/block_a/01_rows/block_a_rows.csv','rb').read()).hexdigest())"` |

### 1.1 N-1 in full — the confidence result is a between-arm contrast

This is the finding I would not ship the paper without settling.

`plddt_correlations.csv` reproduces perfectly: all twelve Pearson r and Spearman ρ match
to six decimals on the population "Class A minus the eight sealed receptors" (32
receptors, 1,595–1,600 rows per backbone). The problem is not arithmetic; it is what the
statistic is a correlation *of*.

The population pools **both arms**, and the outcome is `rmsd_to_active_ref` for every
row. But `rmsd_to_active_ref` is only a correctness measure for the **cognate** arm. For
an apo row the correct target is the *inactive* reference. So half the sample is scored
against the state it was not supposed to reach — and in that half, higher confidence
goes with *larger* distance-to-active, which for apo means *more* correct.

Anchor pLDDT (`plddt_at_anchors`, the designated primary aggregation), r against
`rmsd_to_active_ref`:

| backbone | pooled (shipped) | apo only | cognate only | **arm-centred** |
|---|---:|---:|---:|---:|
| boltz | −0.221 | **+0.251** | −0.237 | **+0.123** (sign reverses) |
| chai | −0.160 | **+0.245** | −0.418 | **−0.018** |
| of3 | **−0.626** | **+0.313** | −0.383 | **−0.079** |
| protenix | +0.068 | **+0.649** | −0.068 | +0.420 |

Mean anchor pLDDT and mean RMSD-to-active by arm (boltz / chai / of3 / protenix):
apo 87.7 / 84.9 / 75.9 / 84.5 at RMSD 2.10 / 1.92 / 2.09 / 2.19; cognate 91.4 / 86.8 /
84.7 / 85.3 at RMSD 1.05 / 1.28 / 1.18 / 0.95. Cognate rows are simultaneously more
confident at the anchors and closer to the active reference, **by construction of the
experiment**. The pooled r is measuring that contrast. OF3 is "strongest in the
campaign" precisely because it has the largest apo→cognate anchor-pLDDT gap (8.8
points, the biggest of the four).

Two consequences:

1. **The "signed on 2 of 4 backbones" verdict and the OF3 ranking are both artefacts of
   the target mis-specification.** Score each row against its *arm-appropriate*
   reference (apo → `rmsd_to_inactive_ref`, cognate → `rmsd_to_active_ref`) and the
   arm-centred correlations become −0.136 / −0.296 / −0.416 / −0.336 — **all four
   negative, comparable in size, and OF3 stops being an outlier.** That is a cleaner and
   more defensible result than the one on the claim sheet, and it points the opposite way
   on which backbones "sign".
2. **There is a real but much smaller within-arm signal.** Splitting each arm into
   state-correct and state-incorrect rows (cognate should be predicate-active, apo
   predicate-inactive), correct rows carry higher anchor pLDDT by **+0.6 to +5.7 points**
   in all eight backbone×arm cells. That is the honest version of "pLDDT carries some
   information about conformational correctness", and it is nowhere near r = −0.63.

Note also the direct tension with the project's own framing: `CLAUDE.md` states the
manuscript's third claim as "**model confidence does not track state correctness**",
while SC-11 and `results.tex:193` assert that it *does* on two of four backbones. The
arm-centred numbers support the `CLAUDE.md` framing better than SC-11 does.

### 1.2 N-4 in full — a recorded discrepancy that is itself wrong

`DISCREPANCY_REPORT.md` D-A-24 states that the SI caption's 4,866 "does not reproduce,
under any predicate definition tried", that "neither 4,866 nor 4,256 appears anywhere in
`data/block_a/`", and instructs "**Do not 'fix' the caption to 3,739**". `CAP12` in
`verify_claims.py` records it as a standing mismatch and `DATA_REQUESTS.md` raises it as
ask 3 to the pipeline agent.

Both numbers are already in the drop, exactly:

```
rows.active.sum()                                  = 4866
rows[rows.active].rmsd_to_active_ref.notna().sum()  = 4256   (= 4866 − 610)
rows[rows.active].rmsd_to_active_ref.isna().sum()   = 610
```

`01_rows/block_a_rows_dictionary.csv` documents `active` as
`derived class-conditional: A=npxxy AND tilt; B=kink<159.95 AND tilt; F=tilt only`, and I
confirmed that definition against the rows with zero mismatches in all three classes.
`CAP12` gets 3,739 because it rebuilds the predicate as the **Class A rule applied after
E1+E2 to both-measured rows** — the exact error the report's own "Not reproduced" section
diagnoses two pages earlier ("the shipped `active` column is class-conditional… we read
that disagreement as the drop's rather than ours"). The same script's `CORPUS` check
already asserts `4866 == rows.active.sum()` and passes, so `verify_claims.py` currently
holds a passing check and a standing mismatch on the same number.

The 610 coincidence that made this look solid is not a coincidence: all 610 unreferenced
predicate-active rows are Class A, on six receptors (ACM1, ADA2A, ADRB1, CCKAR, DRD3,
OX2R), and they survive E1+E2, so both populations contain the identical 610 row_ids.

**Action**: D-A-24 should be withdrawn, `CAP12` rewritten against `rows.active`, and
`DATA_REQUESTS.md` ask 3 struck. The SI caption is correct as written.

### 1.3 The named traps, checked explicitly

| trap | verdict |
|---|---|
| **Never filter on `excl_any`** (removes 53.7%) | **No surviving claim filters on it.** But `08_exclusions/exclusion_sweep.csv` ships a row labelled `all_E1-E5` which **is** `excl_any` — I confirmed it reproduces the `excl_any` filter to 4 dp on the fraction for all four backbones. It is the single largest mover in the sweep (chai fraction +3.27%, chai tilt +222%) and it is labelled in a way that reads as a benign union of the five pre-specified sets. **Anything quoting the `all_E1-E5` column is quoting `excl_any`.** No manuscript sentence currently does. |
| **Whole Gα, not the 21-mer** | **The Block A drop is clean** — no narrative file claims a peptide input; `input_state_claim` is `apo` / `Ga-coupled-active` only. **The manuscript is not clean**: see N-2. `analysis/block_a/DATA_REQUESTS.md:36-47` and `methods.tex:324` both state the correct position; `main.tex:81` and `si.tex:178` contradict them. |
| **Confidence must not discriminate state without validation** | Two hits. **N-1**: the validation that exists (SC-11) is confounded by arm and reverses sign on boltz when de-confounded. **N-13**: `excl_E1` *is* a confidence threshold used as an exclusion, and it removes the corpus's worst cognate cell. Separately, `11_structures/confidently_wrong/`'s selection rule is "highest pLDDT" (recorded D12) — I re-verified it: row 567 is the cell's max-`plddt_mean` row, `SELECTION.md`'s stated rule selects 552, and **both are apo rows sitting 0.86–0.95 Å from the *inactive* reference and correctly called inactive.** D12 stands exactly as written. |
| **References whose state label is curated, not structural** | **The largest unrecorded exposure.** The `state` column is a curated annotation; the thresholds (9.08 / 14.932) were fitted on 80 of these same reference rows (Flag 15), so the instrument is calibrated on curated labels and `results.tex:16`'s self-consistency figure is derivation-set. On top of that, N-6 shows `transducer_present` cannot be trusted to tell which active references are actually ternary complexes, and N-7 shows 9 of 168 reference rows were never evaluable at all yet are counted as passes. |

### 1.4 Recorded discrepancies I re-tested and confirm

D1 (Protenix NPxxY slope 0.257, CI [0.074, 0.552] excludes zero on all three inclusion
sets; `baseline` and `class_a_only` byte-identical on NPxxY), D2 (pooled connector CI
[−1.196, +0.026] includes zero; ratio taken on |Δ| so its CI cannot cross zero — and
**all four** per-backbone CIs include zero, so the claim sheet's "per-backbone signing
collapses to 1/4, Chai only" is 0/4), D3 (tilt slopes −0.298/−0.659 under `class_a_only`),
D5 (all four SC-1 intervals are the receptor column; boltz byte-identical), D6/D15
(fractions 0.9472/0.8841/0.9340/0.9201 over **39** receptors), D7 (2/4,866 = 0.041%),
D9 (98 panel PDBs, 44 active-role, 54 inactive-role), D10 (five `deviation_class` levels,
5 `unclassified`), D12 (rows 552/567 both correct apo predictions — re-derived both
selection rules), D14 (610 untestable; 2/4,256 = 0.047%), D16 (32 receptors, not 40),
D17 (cluster/receptor width ratios 1.00–2.20; "~1.10×" holds on 2 of 12), **D18** (I read
`8FZQ.cif`'s `_struct.title`: *"Dehosphorylated, ATP-bound human cystic fibrosis
transmembrane conductance regulator (CFTR)"* — confirmed, and 6PT2 beside it is the
correct δOR entry), D-A-23 (`cluster_map.csv` = 29 clusters / 16 singletons / 55%, against
the 26-cluster / 42% convention).

### 1.5 What reproduced bit-exactly (stated so it is not mistaken for unchecked)

`MANIFEST.json` 79/80 sha256 and every `row_count`; all 380 rows × 10 columns of
`cell_summary.csv` rebuilt from `01_rows`; all 24 slopes, r², n and SD in
`amplitude_fits.csv` rebuilt from `amplitude_points.csv`; all 12 Pearson r and Spearman ρ
in `plddt_correlations.csv`; **every cluster CI in the drop reproduced as the exact
2.5/97.5 percentiles of `09_bootstrap_draws/bootstrap_draws.csv`** (32 headline intervals,
24 amplitude, 12 pLDDT — all to 4 dp); the whole `exclusion_sweep.csv` fraction metric
rebuilt independently from `01_rows` under eight filters; the connector (Δ_pred −0.5602,
204/256 = 79.7%, 205/256 = 80.1%, ratio 0.3710, and all four per-backbone deltas); SC-6's
per-backbone counts (1,167/1,273/1,229/1,197 and 1/0/1/0); SC-7 (99.145/97.702/97.191/
98.809 and `engaged` ≡ contacts > 30 with zero mismatches); SC-8's rates; the E1–E5
`affected_row_count` values; `npxxy_active` ≡ `d < 9.08` and `tilt_active` ≡ `d > 14.932`
with zero mismatches; and every caption number I could reach —
**7,166** Class A both-axes-measurable rows under E1+E2, **159** Class A cells with both
arms (120 up / 37 same / 2 down), the quadrant census **2,611 / 577 / 157 / 3,162**,
**111 of 160** apo cells never firing and **108 of 159** cognate cells always firing,
**98.2%** engagement at a median of **66** contacts, and methods.tex's **35 (81%) /
19 (44%) / 15 (35%)** training-cutoff counts on the 43 dated panel active references.

---

## 2. What I could NOT check, and why

Listed because an unchecked item reported as clean is worse than a known gap.

1. **Every receptor-bootstrap CI in the drop.** `09_bootstrap_draws/bootstrap_draws.csv`
   contains `bootstrap_type == 'cluster'` on all 48,000 rows and **zero receptor-boot
   draws**. So the `*_receptor_ci_*` columns in `headline_by_backbone.csv`,
   `amplitude_fits.csv` and `plddt_correlations.csv` cannot be reproduced from the drop
   at all. This matters more than it sounds: by D5 and N-8, the receptor intervals are
   exactly the ones SC-1 and SC-11 actually quote.
2. **The 26-cluster bootstrap object.** The draws were computed on a 26-cluster map that
   is not in the drop; `cluster_map.csv` holds a different 29-cluster object (D-A-23). I
   can confirm the CIs are consistent percentiles of the shipped draws, but **I cannot
   verify the resampling unit those draws were built on.** I did not attempt a
   re-clustering — D-A-23 documents that doing so previously produced a worse error.
3. **The connector reference denominator.** `connector_references.csv` is a four-line
   stub; the 77 per-reference P5.50–F6.44 distances are not shipped and `_analyze.py`
   hardcodes `REF_ACTIVE_MEDIAN` / `REF_INACTIVE_MEDIAN`. **The −1.51 Å denominator of
   the 0.37 magnitude ratio is unverifiable**, and its CI [0.04, 0.77] treats a
   hardcoded constant as error-free. Separately, note the T2 sample is a **balanced
   design** — exactly 32 rows per (backbone × arm × predicate-call), so 256/256 by
   construction. The 79.7% / 80.1% are properties of that design, **not corpus rates**,
   and must not be quoted as "80% of predictions".
4. **`rmsd_to_active_ref` / `rmsd_to_inactive_ref` against coordinates.** Recorded D22
   says row 8285 ships 1.218 Å and recomputes to 1.2952 Å with no trim reproducing it,
   and that the scorer's atom set is documented nowhere. I did not re-derive this — I
   have no independent superposition implementation here and `11_structures/` ships only
   8 predicted CIFs. **The RMSD columns are therefore unverified by me**, including the
   ones N-1 uses as the outcome variable; N-1's conclusion is about the *arm structure*
   of the correlation and does not depend on the absolute RMSD scale, but a systematic
   arm-dependent RMSD bias would need separate ruling out.
5. **Both predicate axes against coordinates.** Statement A of the claim sheet asserts
   bit-exact independent recomputation of tilt (n=45) and NPxxY-OH (n=41) against
   non-scorer implementations. **No per-sample recompute table ships in this drop**, so I
   verified only that `npxxy_active`/`tilt_active` follow from the stored distances and
   thresholds — not that the distances follow from the coordinates. Statement A is taken
   on trust.
6. **Templates-off and MSA configuration.** `block_a_rows.csv` has no column for either
   across all 55 (recorded D19). Unverifiable from the drop. This is load-bearing: an
   active-state template is the oracle route the whole design excludes.
7. **Whether `transducer_present` is wrong or merely differently defined.** No definition
   ships. I can show it is inconsistent with the deposited structures and with itself
   (N-6); I cannot say which of the two readings is right, and I did not open the
   reference CIFs to adjudicate.
8. **The seven remaining `11_structures/ALIGNMENT.md` files.** Recorded D13/D20 say all
   eight carry at least one wrong identifier. I independently re-verified only the two
   claims that are checkable against tidy columns (D12's row selection, D18's CFTR
   title). **The other six files are unverified by me** and should stay under the
   report's "treat all of them as unreliable" instruction.
9. **Bootstrap seed reproducibility.** The convention is seed 20260909, 1,000 resamples.
   The draws are shipped as values only, with no seed or index column, so I confirmed the
   CIs are the right percentiles **of these draws** but could not confirm the draws are
   the draws that seed produces.
10. **κ confidence intervals in SC-4** (85.60–93.38, 69.75–96.35). Point estimates and κ
    reproduce; the intervals have no draws in `09_bootstrap_draws` and are unverifiable.
11. **Anything Block B or Block C.** Out of scope; `results.tex` lines 229+ carry
    Block B numbers I made no attempt to verify. Note only that `methods.tex:324`'s
    "not an input in **either** campaign" means the peptide defect at N-2 is not rescued
    by a later block.

---

## 3. Suggested triage order

1. **N-1** — settle the confidence result before Fig. 4, Table 4 and the third headline
   claim are drawn. The de-confounded version is a better result; it is just a different
   one.
2. **N-2** — two caption edits. The paper currently asserts, in its graphical abstract and
   an SI caption, an input it did not use, against its own Methods.
3. **N-3** — the holdout cutoffs, because C-9 makes that holdout the only prospectivity
   evidence in the paper and its `powered` column is already `False` on all four rows.
4. **N-4** — withdraw D-A-24, fix `CAP12`, strike `DATA_REQUESTS.md` ask 3.
5. **N-5** — the ≤0.5% invariance sentence appears at the top of the claim sheet as one of
   "two methodological statements worth surfacing at front"; it is false as written and
   `si.tex:139` repeats it.
6. **N-6, N-7, N-11** — the reference-set Methods paragraph needs all three.

Nothing in this review found an error in the *shipped tidy data*. Every disagreement is
between a claim and the data, and in every case the data is the one that reproduces.
