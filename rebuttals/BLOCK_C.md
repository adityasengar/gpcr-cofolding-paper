# Block C — rebuttals, questions, and suggestions

For the pipeline agent that produced `block_c_figure_data.zip`
(`2c3af764…`) and `block_c_structures.zip` (`1375f5e9…`).

Verification here: `analysis/block_c/verify_claims.py`, **53 checks, 53
reproduce, 0 do not** — the first drop in this project where nothing in the claim
sheet disagrees with the shipped data. Read the next paragraph before taking
that at face value.

**Block C shipped one row-level file.** `12_g4_off_site_census/g4_full_census_v2.csv`,
40,000 rows. Blocks A and B shipped their prediction rows — 9,490 and 32,000 —
so every headline could be recomputed from source. Here 23 of the 53 checks
recompute from the census and **30 compare two shipped summaries to each other**.
A green consistency check catches transcription and staleness; it cannot catch a
computation that was wrong in the same way in every file. **SC-C-1 and SC-C-4 —
the block's two surviving positives — are both in that second group.** Every
rebuttal below is therefore either recomputed from the census, recomputed from a
shipped tidy CSV, or a demonstrated internal contradiction between two shipped
files. Nothing here is "this looks odd".

Reproductions assume the drop is extracted at `data/block_c/`. Requests are in
`analysis/block_c/DATA_REQUESTS.md`; this document is the evidence behind them.

---

# 1. Rebuttals

## R1 — "SC-C-1's numerator: 1.52 %" is the numerator of a population SC-C-1 is not computed on

**Shipped.** `README.md` §"Load-bearing numbers (post-verification)":

> **Small-molecule apo × {agonist, antag} (SC-C-1's numerator): 1.52 %.**
> Not material for SC-C-1.

**The number is right and the label is wrong.** 1.52 % reproduces exactly —
149 off-site rows of 9,800, filtering `arm == apo`, `role in {full_agonist,
neutral_antagonist}`, `ligand_source == "hetatm"`. But SC-C-1 does not filter on
`ligand_source`. Its own two artefacts pin it to the 23-receptor 2×2 common set
(`stage3_2x2_ligand_state_specificity.json`:
`per_backbone.*.interaction.n_receptors_in_common = 23`;
`g_scc1_cluster_boot.json`: `n_receptors_in_common = 23`), and eleven of those
23 are peptide-agonist receptors whose agonist cells the `hetatm` filter removes.

**Data.** On the population SC-C-1 is actually computed on:

| population | n rows | off-site > 15 Å |
|---|---:|---:|
| apo × {agonist, antagonist} × `hetatm`, all 36 receptors *(as shipped)* | 9,800 | 1.52 % |
| apo × {agonist, antagonist}, **the 23 common receptors, all ligands** | 9,200 | **18.92 %** |
| — its **agonist** half | 4,600 | **35.85 %** |
| — its **antagonist** half | 4,600 | **2.00 %** |
| apo × {agonist, antagonist}, the S1 15-set, all ligands | 6,000 | 22.12 % |
| — its **agonist** half | 3,000 | **41.63 %** |

Eight of SC-C-1's 23 receptors place their apo agonist off-site on 50–100 % of
rows: CXCR2, CCR5, CXCR4, NPY1R, NPY2R and EDNRB at 100 %, MCHR1 at 90.5 %, GRPR
at 56.5 %. The 35.85 % / 2.00 % asymmetry is aligned exactly with the class label
the 2×2 contrasts, which is the one alignment that matters. Separately, the
1.52 % is itself two receptors: CXCR2 at 39.0 % and LT4R1 at 12.75 % carry 129 of
the 149 off-site rows, 28 of the 34 receptors are at exactly 0 %, and dropping
those two takes it to 0.22 %. A pooled rate over a distribution that shaped is
the defect W-C-3 retracts for pose accuracy, in a different cell.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
S23=set('5HT1B 5HT5A AA1R AA2AR ACM2 ACM4 ADRB2 AGTR1 CCR5 CNR1 CNR2 CXCR2 CXCR4 EDNRB GRPR LPAR1 LT4R1 MCHR1 NPY1R NPY2R OPRD OPRK OPRX'.split())
b=c[(c.arm=='apo')&(c.role.isin(['full_agonist','neutral_antagonist']))]
for lbl,d in [('shipped filter',b[b.ligand_source=='hetatm']),
              ('SC-C-1 population',b[b.receptor.isin(S23)]),
              ('  its agonist half',b[b.receptor.isin(S23)&(b.role=='full_agonist')]),
              ('  its antagonist half',b[b.receptor.isin(S23)&(b.role=='neutral_antagonist')])]:
    print('%-22s n=%5d  off-site %5.2f%%'%(lbl,len(d),100*(d.distance_A>15).mean()))
print(b[b.ligand_source=='hetatm'].groupby('receptor').apply(lambda d:round(100*(d.distance_A>15).mean(),2)).sort_values(ascending=False).head(4).to_dict())"
```

**We ran the test that would break the claim, and it did not break.** This is not
us saying the 2×2 is wrong. `pocket_ca_rmsd` is receptor-side by construction
(C-C-6: twelve fixed BW positions, 7TM Cα Kabsch), so an off-site ligand does not
mechanically corrupt it. If the interaction were an empty-pocket artefact, the
per-receptor ordinal recovery should collapse on the eight affected receptors.
It does not — Spearman(agonist off-site %, per-receptor median τ) = **−0.241,
p = 0.268, n = 23**; Mann–Whitney between the two groups p = 0.436, medians 0.282
against 0.386. At classifier grain, Spearman(off-site %, per-receptor AUROC) =
**−0.160, p = 0.568, n = 15**, and the sign runs the wrong way for the artefact
story: AGTR1, the worst receptor in the whole classifier at AUROC 0.000 on three
backbones, has its agonist **in** the pocket on 97.5 % of rows, while EDNRB,
NPY2R and OPRX sit at 0.99–1.00 with 48–100 % off-site.

**Severity: high — it would reach a reader, and it already reached ours.** The
sentence at `manuscript/sections/results.tex:426–435` currently says the contrast
"is not built on mis-docked ligands" and cites 1.52 % as the proof. A reviewer
who reads the census will get 18.92 %, and the honest answer — *the readout is
receptor-side, and here is the test showing placement does not predict signal* —
is stronger than the one we are giving. The same framing is in
`analysis/block_c/panels/BC-4_ligand_placement.md` and `figures/FIGURES.md:605`
on our side, and we are fixing those.

**What would close it.** (1) Confirm which population SC-C-1's four point
estimates run on. (2) The 2×2 recomputed on the twelve small-molecule-agonist
receptors of the 23 — 5HT1B, 5HT5A, AA1R, AA2AR, ACM2, ACM4, ADRB2, CNR1, CNR2,
LPAR1, LT4R1, OPRD. If the four signs survive on twelve receptors the objection
is closed in one line and the claim is stronger than it is today. We can run it
ourselves the moment `rows.tier3.v2.csv` arrives.

---

## R2 — SC-C-2's table is headed "Kendall's τ" and contains a fraction of receptors

**Shipped.** `BLOCK_C_CLAIM_SHEET.md` § SC-C-2:

> **Numbers** (Kendall's τ, receptor-panel-median):
>
> | panel | boltz | chai | of3 | protenix |
> | Tier 3 apo × 23 | 74% | 65% | 74% | 87% |

**Data.** Those values are neither Kendall's τ nor a median. They are
`tier3_apo_23_receptors.summary.<bb>.fraction_positive_significant` from the
claim's own cited JSON — the proportion of receptors whose τ is positive *and*
significant.

| backbone | claim-sheet "τ" | what it is | actual median τ |
|---|---:|---:|---:|
| boltz | 74 % | `fraction_positive_significant` 0.7391 | **0.386** |
| chai | 65 % | 0.6522 | **0.259** |
| of3 | 74 % | 0.7391 | **0.328** |
| protenix | 87 % | 0.8696 | **0.366** |

**Reproduce.**
```bash
python3 -c "
import json, numpy as np
o=json.load(open('data/block_c/07_ordinal_recovery/s5_p4_ordinal.json'))
t=o['tier3_apo_23_receptors']
for bb in ['boltz','chai','of3','protenix']:
    taus=[v['tau'] for v in t['per_backbone'][bb].values()]
    print(bb,'claim-sheet %.0f%%'%(100*t['summary'][bb]['fraction_positive_significant']),
          'median tau %.3f'%np.median(taus))"
```

**Severity: high — it reached a reader.** Our Results said *"gives Kendall's τ of
65–87 % across backbones"*. A reader takes "τ of 74 %" as a correlation of 0.74,
roughly twice the true value. It has been corrected: the section now says a
positive and significant τ on 65–87 % **of receptors**, names it as a count
rather than a correlation, and gives the median τ (0.26–0.39) beside it.

**How it was caught, which is the part worth passing back.** The claim sheet, the
dispatch and our own prose all carried the mislabel and all read fine. It
surfaced only when the panel was built and the per-receptor τ were plotted: the
violins sat around 0.3 while the panel labels printed 0.74. A number that
survives three prose reviews can still be wrong, and drawing it is what finds
out.

**What would close it.** Relabel the SC-C-2 table, or report both columns. The
underlying JSON is correct and self-describing; only the heading is wrong.

---

## R3 — SC-C-8 states a bootstrap convention that SC-C-1's own artefact does not follow

**Shipped.** `BLOCK_C_CLAIM_SHEET.md` §"Bootstrap convention (Block A C-8
authoritative)": *"500 receptor-boot / 500 cluster-boot / 200 permutation-null
resamples; seeds `20260910..20260920`."* SC-C-8 restates it: *"All Block C CIs in
this claim sheet use cluster-boot over paralog clusters … 500–1000 resamples per
statistic, seed `20260910..20260920`."*

**Data.** `g1_bootstrap_s1_auroc.json` follows it exactly — `n_bootstrap_iter:
500`, `n_perm: 200`. `g_scc1_cluster_boot.json`, the artefact behind SC-C-1 and
therefore behind the block's headline, carries **`n_iter: 5000`** and
**`rng_seed: 1234`**. Neither number is in the stated range and the seed is not
in the stated set. C-C-3 and POST_CLOSEOUT §1b.ii both describe the 5000/1234
protocol openly, so this is a stale claim-sheet sentence rather than a hidden
choice — but SC-C-8 *is* a claim, it is the one that tells a reader how every
interval in the block was made, and it is false about the block's most important
interval.

**Reproduce.**
```bash
python3 -c "
import json
print(json.load(open('data/block_c/06_2x2_interaction/g_scc1_cluster_boot.json'))['n_iter'],
      json.load(open('data/block_c/06_2x2_interaction/g_scc1_cluster_boot.json'))['rng_seed'])
print(json.load(open('data/block_c/04_classifier/g1_bootstrap_s1_auroc.json'))['n_bootstrap_iter'])"
```

**Severity: medium — it would reach a reader through Methods.** Our
`methods.tex:401–403` follows the artefact and says 5,000 resamples, seed 1234.
If SC-C-8 is authoritative our Methods is wrong; if the artefact is
authoritative SC-C-8 is wrong. One of the two sentences has to move and only you
can say which.

**Two things that checked out clean and are recorded so nobody re-reports them.**
SC-C-8's cluster counts are both correct: the Block B paralogy map gives **26**
clusters over the 40-receptor panel and **12** over the S1 15-set, exactly as
stated, and 16 over the 23-receptor 2×2 set as `g_scc1_cluster_boot.json` says.
And `paralogy_clusters.csv` — which the drop names as an input and does not ship
— is byte-identical to the copy we hold from Block B, SHA-256 `6158081e…`,
matching the SHA `g_scc1_cluster_boot.json` names. **Block C does not repeat
Block A's defect** of shipping a column headed "cluster-boot" that holds
receptor-boot values: `g_scc1_cluster_boot.json` carries `cluster_boot` and
`receptor_boot_recomputed` as separate blocks with genuinely different numbers,
and we checked that on all four backbones.

---

## R4 — SC-C-5 is the one surviving claim whose interval breaks the block's own authoritative convention, and under that convention its as-scored slope does not sign

**Shipped.** `BLOCK_C_CLAIM_SHEET.md` § SC-C-5, "receptor-boot CI over 15
receptors, 1000 iterations":

| set | n | pooled slope (Å⁻¹) | pooled slope 95 % CI |
|---|---:|---:|---|
| full 15 (as-scored) | 15 | −0.325 | **[−0.570, −0.068]** |
| excluding AGTR1 | 14 | −0.060 | [−0.246, +0.087] |

Flag C-1: *"Every CI in `BLOCK_C_CLAIM_SHEET.md` uses cluster-boot over paralog
clusters … Receptor-boot is the secondary statement."*

**Data.** SC-C-5's intervals are receptor-boot on both rows —
`g2_refsep_vs_auroc.json.pooled_regression.bootstrap` resamples 15 receptors,
`g2_excl_agtr1.json.excl_agtr1_14.bootstrap` resamples 14. No cluster-boot
interval exists for either. The regression itself ships and recomputes exactly
from `05_ref_separation/g2_refsep_vs_auroc.csv` (slope −0.32499, R² 0.16177,
ρ −0.20561 on the full set; −0.05995, 0.01045, −0.01513 excluding AGTR1), so we
did the cluster-boot ourselves against the Block B paralogy map:

| set | receptors | clusters | slope | receptor-boot 95 % CI (shipped) | **cluster-boot 95 % CI (ours)** |
|---|---:|---:|---:|---|---|
| full 15, as-scored | 15 | 12 | −0.325 | [−0.571, −0.064] *excludes zero* | **[−1.015, +0.072]** *spans zero* |
| excluding AGTR1 | 14 | 11 | −0.060 | [−0.246, +0.087] | **[−0.282, +0.112]** |

**Reproduce.**
```bash
python3 -c "
import pandas as pd, numpy as np
from scipy.stats import linregress
d=pd.read_csv('data/block_c/05_ref_separation/g2_refsep_vs_auroc.csv')
p=pd.read_csv('data/block_b/09_references/paralogy_clusters.csv')
d['cl']=d.receptor.str.upper().map(dict(zip(p.receptor.str.upper(),p.cluster_id)))
for lbl,dd in [('full 15',d),('excl AGTR1',d[d.receptor!='AGTR1'])]:
    r=np.random.default_rng(1234); cl=sorted(dd.cl.unique())
    s=[linregress(*(lambda x:(x.pocket_ca_sep,x.auroc))(pd.concat([dd[dd.cl==k] for k in r.choice(cl,len(cl),True)]))).slope for _ in range(5000)]
    print(lbl, len(cl),'clusters  slope %.3f  cluster-boot'%linregress(dd.pocket_ca_sep,dd.auroc).slope, np.percentile(s,[2.5,97.5]).round(3))"
```

**Severity: medium, and it moves in your favour.** Under the block's own
authoritative convention the as-scored slope never signed either, so the
pre-registered applicability hypothesis has no support at any stage — not merely
after AGTR1 is removed. That is a cleaner refutation than the one the claim sheet
states, and it lets the manuscript drop the "excluding a single receptor" hedge
from the load-bearing position and keep it as a sensitivity. We have not applied
it yet, because a number we computed against a convention you own is not a number
we should put in a paper without your confirmation.

**One more label on the same file.** `g2_refsep_vs_auroc.json.pooled_regression`
reports `n_points: 15` while its own `bimodality.n` is 60 and the OLS is fitted
on 60 rows — 15 receptors × 4 backbones, four non-independent points per
receptor. The bootstrap correctly resamples receptors; the R² of 0.162 is
computed on 60 correlated points and labelled as if on 15.

**What would close it.** Cluster-boot CIs on both rows of the SC-C-5 table, with
`n_points` corrected to 60.

---

## R5 — The four 2×2 cell means are not on the same receptors, and the field that says so is named `n_clusters` and holds a receptor count

**Shipped.** `06_2x2_interaction/stage3_2x2_ligand_state_specificity.json`,
`per_backbone.boltz`:

```
cells.agonist_active   = {est 0.768, ci_lo 0.698, ci_hi 0.839, n_clusters: 28}
cells.agonist_inactive = {est 0.976, ...,                      n_clusters: 28}
cells.antag_active     = {est 0.898, ...,                      n_clusters: 23}
cells.antag_inactive   = {est 0.767, ...,                      n_clusters: 23}
n_receptors = {agonist: 28, antag: 23, common: 23}
```

**Data.** Two separate problems in four lines.

1. **`n_clusters` is a receptor count.** 23 receptors map to **16** paralog
   clusters — `g_scc1_cluster_boot.json.n_clusters = 16`, and we reproduce 16
   from the Block B map. 23 cannot be a cluster count for the same 23 receptors.
   The values equal `n_receptors` exactly, which is what they are.
2. **The four cell means are on two different populations.** The agonist cells
   are means over 28 receptors, the antagonist cells over 23. The *interaction*
   is correctly on the common 23 (`interaction.n_receptors_in_common: 23`) — that
   part is right and we checked it. But a panel that draws all four cell means
   side by side, which is the obvious figure for SC-C-1 and is what our BC-1
   spec calls for, is comparing a 28-receptor mean against a 23-receptor mean and
   nothing in the JSON says so.

`n_rows` in the same block is `{agonist_*: 2800, antag_*: 2300}`, which is
`n_receptors × 50 × 2` — 50 rows per cell, counted once against each of the two
references. We confirmed the 50-per-cell figure independently from the census
(800 cells × 50 = 40,000, no exceptions), so the row counts are consistent with
apo-only and this is not a hidden second arm.

**Reproduce.**
```bash
python3 -c "
import json
b=json.load(open('data/block_c/06_2x2_interaction/stage3_2x2_ligand_state_specificity.json'))['per_backbone']['boltz']
print({k:v['n_clusters'] for k,v in b['cells'].items()}, b['n_receptors'], b['n_rows'])
print('actual clusters over the 23:', json.load(open('data/block_c/06_2x2_interaction/g_scc1_cluster_boot.json'))['n_clusters'])"
```

**Severity: medium — it would reach a reader through a figure.** The interaction
is unaffected. The four numbers a reader looks at are.

**What would close it.** Rename the field, and either recompute the four cell
means on the common 23 or state the two populations on the face of the JSON.

---

## R6 — The pre-registered KILL-S1 verdict is computed on the maximum over three feature sets

**Shipped.** `s1_loro_classifier.json`:

```
kill_s1_threshold: 0.65
per_backbone_best_auroc_kill_s1_row: {boltz 0.8523, chai 0.7595, of3 0.7009, protenix 0.8254}
kill_s1_verdict: "KILL_S1_DID_NOT_FIRE (4/4 backbones >= 0.65)"
```

**Data.** Those four values are the **best of three feature sets** per backbone,
not the values of any single feature set. On `F_iii_pocket_plus_axes`, which
Flag C-2 pins and which the claim sheet, the abstract template and our manuscript
all quote:

| backbone | F\_i\_delta | F\_ii\_pocket\_family | **F\_iii (pinned)** | JSON's "kill_s1_row" |
|---|---:|---:|---:|---:|
| boltz | 0.398 | 0.814 | **0.852** | 0.852 (= F_iii) |
| chai | 0.462 | **0.760** | 0.706 | 0.760 (= F_ii) |
| of3 | 0.323 | **0.701** | 0.656 | 0.701 (= F_ii) |
| protenix | 0.400 | 0.787 | **0.825** | 0.825 (= F_iii) |

The verdict does not change — F\_iii clears 0.65 on all four too. But OF3 clears
it by **0.0057** on the pinned feature set and by 0.05 on the max, and a
pre-registered threshold evaluated against the best of three feature sets is a
multiplicity the pre-registration should name.

**Reproduce.**
```bash
python3 -c "
import json
l=json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))
print(l['per_backbone_best_auroc_kill_s1_row'])
for v in l['variants']:
    if v['variant']=='C_no_selfref_apo': print(v['backbone'],v['feature_set'],round(v['pooled_auroc'],4))"
```

**Severity: medium.** It does not change the verdict, so it would not reach a
reader as a wrong number. It would reach a reviewer as a question about the
pre-registration, and that is worse to answer late.

**What would close it.** Which feature set was pre-registered. If F\_iii, say so
and OF3's 0.0057 margin goes in the text.

---

## R7 — `permutation_p_value: 0.0` and `z_vs_null: 35.8` are reported from five permutations

**Shipped.** `s1_loro_classifier.json`: `n_permutations: 5`, and every one of the
36 variants carries `null_permutation_n: 5` with `permutation_p_value: 0.0`
(or 1.0) and a `z_vs_null` in the tens.

**Data.** At five permutations the smallest attainable p-value is 1/6 ≈ 0.167;
0.0 is not a value the statistic can take. `z_vs_null` — 28.4 on Boltz F\_iii,
35.8 on Boltz F\_ii — is computed against a null standard deviation estimated
from five draws. The block's *other*
null is fine — `g1_bootstrap_s1_auroc.json` uses `n_perm: 200` and reports the
null as an interval ([0.477, 0.520] on Boltz), which is what our manuscript
cites.

**Reproduce.**
```bash
python3 -c "
import json
l=json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))
v=[x for x in l['variants'] if x['variant']=='C_no_selfref_apo' and x['backbone']=='boltz'][-1]
print(l['n_permutations'], v['permutation_p_value'], round(v['z_vs_null'],2))"
```

**Severity: medium — it would reach a reader if anyone quoted it.** Nobody has;
we checked our own draft. It is the kind of field that gets picked up later
precisely because it looks decisive.

**What would close it.** Suppress both fields at n = 5, or raise the count to
match `g1`.

---

## R8 — The CXCR2 exhibit is a cognate-arm structure evidencing an apo-arm claim

**Shipped.** `13_structures/MANIFEST.json`, targeted slot 05:
`05_CXCR2_OF3_backbone_specific_inversion_flag_cognate_antag.cif`,
`distance_A: 6.5135`, `arm: cognate`. Flag C-5 makes CXCR2's OF3-only inversion a
named manuscript finding, and this is the only structure shipped for it.

**Data.** The inversion is a property of the **apo** arm — SC-C-4 and G2 both run
on `s1_loro_classifier.json` variant `C_no_selfref_apo`. In the apo arm CXCR2's
small-molecule ligands are off-site on:

| backbone | apo small-molecule off-site | per-receptor AUROC |
|---|---:|---:|
| boltz | 2 % | 0.900 |
| chai | **100 %** | 0.928 |
| of3 | **44 %** | **0.135** |
| protenix | 14 % | 0.999 |

**The conclusion the exhibit is meant to support is correct, and the exhibit does
not support it.** Chai places every apo small molecule off-site and still reaches
0.928; OF3 places 44 % off-site and collapses to 0.135. Placement and inversion
run in opposite directions, so "classifier-feature effect rather than a docking
failure" is right — and the shipped structure, being from the other arm, is not
the evidence for it.

**Reproduce.**
```bash
python3 -c "
import pandas as pd, json
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
x=c[(c.receptor=='CXCR2')&(c.arm=='apo')&(c.ligand_source=='hetatm')]
print(x.groupby('backbone').apply(lambda d: round(100*(d.distance_A>15).mean(),1)).to_dict())
l=json.load(open('data/block_c/04_classifier/s1_loro_classifier.json'))
print({v['backbone']:v['per_receptor_auroc']['CXCR2'] for v in l['variants']
       if v['variant']=='C_no_selfref_apo' and v['feature_set']=='F_iii_pocket_plus_axes'})"
```

**Severity: medium — it would reach a reader who checks.**
`manuscript/sections/results.tex:415–418` currently says "a structure from that
cell shows the ligand correctly seated in the pocket". The cell in question is
the apo one.

**What would close it.** One CIF: CXCR2 × OF3 × apo × neutral-antagonist,
selected as the **median** of that cell by `distance_A`, with the rule and the
row's percentile stated. Median, not best.

---

## R9 — `flag_low_confidence` certifies every row and can never fire

**Shipped.** `g4_full_census_v2.py` header: *"receptor_anchor_hits (0-6; 6 = full
confidence) … flag_low_confidence: True if anchor_hits < 4"*. The column ships on
all 40,000 census rows.

**Data.** `flag_low_confidence` is `False` on 40,000 of 40,000 rows, and it is
structurally incapable of being anything else: the anchor-hit histogram is
`{6: 38800, 20: 1200}` and the minimum is 6. `pooled.n_low_confidence` is
correspondingly 0. A per-row quality certificate that is a tautology given the
rows that reached the file. **This is the third column of this kind across three
drops** — Block A's `matches_claim_sheet` and `passed`, Block B's
`matches_claim_sheet_bool`. It is worth naming as a pattern rather than as a
third instance.

The same histogram carries a smaller inconsistency: the documented range is 0–6
and CNR1 is **20**, on all 1,200 of its rows, all four backbones, all six cells.
`receptor_anchor_target` is 20 on those rows too, so the chain picker succeeded;
the centroid is built from `pocket_map`, not from the anchor hits, and we
verified this does not move `distance_A` — CNR1's off-site rate is 11.25 %
against 17.93 % elsewhere, inside the per-receptor spread. So: the metric is
fine, the docstring is wrong, and the confidence threshold is calibrated for a
6-anchor target on a receptor with 20.

**Reproduce.**
```bash
python3 -c "
import pandas as pd, json
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
print(c.flag_low_confidence.value_counts().to_dict())
print(json.load(open('data/block_c/12_g4_off_site_census/g4_full_census_v2.json'))['receptor_anchor_hit_histogram'])
print(c[c.receptor_anchor_hits==20].receptor.unique())"
```

**Severity: low on its own; medium as a pattern.** No number moves. But a
downstream script that filters `~flag_low_confidence` believes it has applied a
quality gate and has applied nothing, and the same shape of column has now
carried a wrong number twice in this project.

**What would close it.** Emit the count and let the reader threshold it, or emit
`pass`/`fail`/`not_run`. And fix the docstring's 0–6.

Three further columns carry no information and are listed only so nobody spends
an afternoon on them: `g4_full_census_v2.csv::note` (all-NaN),
`::receptor_chain` (constant `A`), `::ligand_seqid` (constant `1`); and in
`reference_separation_pocket_ca.csv`, `pocket_missing` (all-NaN), `n_pocket`
(constant 12), `status` (constant `ok`).

---

## R10 — The FSHR/LSHR drop reason in the caveats is not the reason in the shipped reference table

**Shipped.** C-C-9 and both closeout reports: FSHR was dropped because 8I2H is
*"FSH + compound-21f PAM at 6.00 Å — a positive-allosteric-modulator bound in
the 'inactive' pocket, not a clean orthosteric antagonist reference"*; LSHR
likewise for 7FIJ. The source cited for both is
`pr2_fshr_lshr_class.json`, which does not ship.

**Data.** The reference table that *does* ship,
`09_references/reference_survey.csv`, gives both inactive references
`status = NO_HETATM_CANDIDATES` — no orthosteric ligand candidate found at all —
with curation notes about unresolved 5.58 and 7.53 sidechain hydroxyls and a 6.30
Asp-for-Glu substitution. Neither row mentions a PAM. "No HETATM candidate in the
pocket" and "a PAM is in the pocket" are compatible readings of the same
structure, but they are different statements and only the second is in our
Methods.

**Reproduce.**
```bash
python3 -c "
import pandas as pd
s=pd.read_csv('data/block_c/09_references/reference_survey.csv')
print(s[s.receptor_slug.isin(['FSHR','LSHR'])][['receptor_slug','role','pdb_id','status','curation_note']].to_string())"
```

**Severity: medium — it would reach a reader.**
`manuscript/sections/results.tex:348–352` and `methods.tex:383–388` both carry
the PAM sentence as the reason two of the four panel losses are systematic, and
that sentence has no shipped evidence behind it.

**What would close it.** `pr2_fshr_lshr_class.json`, or one sentence per receptor
naming the ligand entity in 8I2H and 7FIJ and the rule that disqualified it.

---

## R11 — SC-C-3's own verdict field disagrees with SC-C-3, and neither has an interval

**Shipped.** Claim sheet § SC-C-3: *"Consensus … outperforms pLDDT on 3 of 4
backbones"*, with Boltz's +0.006 marked "(tie)".
`s3_consensus_confidence.json`: `kill_s3_n_backbones_beat_plddt: 4`,
`kill_s3_n_backbones_measured: 4`, `kill_s3_verdict: KILL_S3_DID_NOT_FIRE`.

**Data.** Three of four, or four of four, turning on whether Δ = **+0.0060 AUROC**
is a win — and the file carries no uncertainty of any kind on any of the eight
AUROCs: no receptor-boot, no cluster-boot, no permutation null. It is the only
quantitative claim in the sheet with no interval at all, in a block whose Flag
C-1 declares cluster-boot authoritative for every CI.

**Reproduce.**
```bash
python3 -c "
import json
o=json.load(open('data/block_c/08_confidence_signal/s3_consensus_confidence.json'))
print({k:round(v['delta_c_minus_p'],4) for k,v in o['s3d_paired_vs_plddt_top25'].items()})
print(o['kill_s3_verdict'], o['kill_s3_n_backbones_beat_plddt'], 'of', o['kill_s3_n_backbones_measured'])"
```

**Severity: medium, and it is the reason the result is not in the paper.** The
manuscript's third title clause is *confidence does not track state correctness*;
SC-C-3 is the closest thing any block has to a positive answer on confidence and
it appears in no sentence, because we cannot write "beats pLDDT on three
backbones" against a file that says four and gives no interval to adjudicate.
See S3.

**What would close it.** Cluster-boot 95 % CIs on the four Δ values. Four
intervals.

---

## R12 — Eight receptors are missing an entire ligand role and no caveat says so

**Shipped.** The claim sheet's Corpus block describes the design as
"40 Class A × 4 backbones × 2 arms × 3 ligand\_roles × 5 seeds × 10 samples".
C-C-9 documents the 40→36 drop in detail. Nothing documents the third
panel-composition fact.

**Data.** Seven receptors — 5HT2C, ADA2A, ADRB1, APJ, DRD2, GHSR, HRH1 — have
**zero `neutral_antagonist` rows**; HRH3 has **zero `full_agonist` rows**. Each
carries 800 census rows where the other 28 carry 1,200. Cell size is otherwise
exactly 50 everywhere, with no exceptions: 800 cells × 50 = 40,000.

It is arithmetically consistent with the claim sheet's own 40,000, so it is not a
discrepancy — it is an undocumented design fact, and it is the direct mechanical
reason those receptors cannot enter the 23-receptor 2×2 common set, which C-C-3
explains only as "the intersection of receptors with ≥ 1 non-NaN row in each
class".

**Reproduce.**
```bash
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
m=c.groupby(['receptor','role']).size().unstack(fill_value=0)
print(m[(m==0).any(axis=1)])"
```

**Severity: medium.** It would reach a reader as an unexplained gap between "36
landed" and "23 in the common set" — a gap the manuscript currently steps over
without a number.

**What would close it.** One line in C-C-9 naming the eight and the reason
(curation, dispatch or scoring).

---

## R13 — Flag C-12 contradicts C-C-3 in the shipped files

Brief, because the dispatch already flags it and we followed the instruction.
Flag C-12 reads *"Cluster-boot CI on the 2×2 interaction NOT recomputed … the
JSON's CI is receptor-boot"*; C-C-3 is marked **RESOLVED 2026-09-10** and
`06_2x2_interaction/g_scc1_cluster_boot.json` is present with the recompute. Both
files ship. C-C-3 wins, per §4(m), and that is what we used.

**Severity: low for us, medium for anyone reading the drop alone** — a reader
with only the bundle reaches the opposite conclusion from Flag C-12 and would
report our SC-C-1 intervals as receptor-boot mislabelled as cluster-boot, which
is precisely the Block A defect and is precisely not what happened here.

**What would close it.** Delete or restate Flag C-12.

---

# 2. Questions — things only you can answer

**Q1.** Which population are SC-C-1's four point estimates computed on — the 23
common receptors irrespective of `ligand_source`, or a small-molecule subset? The
claim sheet says 23; the README's "SC-C-1's numerator" line implies a
`hetatm` filter. They cannot both be the scope. (R1)

**Q2.** Which bootstrap convention is authoritative for SC-C-1 — SC-C-8's
"500–1000 resamples, seed 20260910..20260920", or `g_scc1_cluster_boot.json`'s
5,000 resamples at seed 1234? Our Methods currently follows the artefact. (R3)

**Q3.** Which feature set was pre-registered for KILL-S1? If F\_iii, OF3 clears
the 0.65 threshold by 0.0057 and we will say so. If the test was best-of-three,
the pre-registration should name the multiplicity. (R6)

**Q4.** Seven receptors have no `neutral_antagonist` cell and HRH3 has no
`full_agonist` cell. Curation, dispatch, or scoring? (R12)

**Q5 — the one with the most riding on it.** **May a Block C apo-arm agonist
predicate rate be quoted as evidence for the paper's "the agonist alone does not"
clause?** Block C is the first block in this project that supplies a ligand at
all: `ligand_type` is NaN on all 32,000 Block B rows and Block A has no ligand
column, while Block C carries **7,000 apo × full\_agonist predictions over 35
receptors** — agonist, no partner — and 7,000 more with the cognate Gα alongside.
SC-C-6 already states the predicate floor-pins on apo and ceiling-pins on
cognate, which read plainly *is* the answer, and then declines to quote the rate.
Two instructions block it and they may not be the same instruction: the dispatch
forbids connecting Block C to two-state generation (we have honoured that in
full — `analysis/block_c/CLAIM_TRACE.md` §"Deliberately absent"), and Flag C-3
forbids quoting a binary-predicate rate for a **ligand-class discrimination**
claim. This is not a ligand-class discrimination claim. If the answer is still
no, we need the reason in one sentence for the Limitations, because a silence
about the paper's own title reads worse than a stated boundary.

**Q6.** SC-C-10's reference-identity check reports "28/28 receptors … 0/28
differ". Which 28? It is a fourth receptor count in a section that already
carries 36, 23 and 15, and no shipped file contains
`pocket_ref_pdb_sha_inactive` at any grain. The manuscript sentence at
`results.tex:436–441` — leakage excluded by construction rather than by audit —
is the strongest sentence in the section and rests entirely on prose.

**Q7.** Sixty-one data files are named as completed work in the drop's own
documents and are not in the bundle. Which of them are deliberately excluded as
working record? "Tidy data only" is a defensible policy and would account for
most; the bundle does not say which it covers, so every one currently reads as an
oversight. Full triage in `analysis/block_c/DATA_REQUESTS.md` ask 17.

**Q8.** Was `block_c_structures.zip` meant to be a different structure set? It
appears nowhere in the dispatch and is fully redundant with `13_structures/` —
16 files, rooted differently, every one byte-identical by SHA-256.

**Q9.** `13_structures/MANIFEST.json` gives `"rule": "targeted-selection"` for all
seven targeted entries. For the ADRB2 agonist/antagonist apo pair (slots 06 and
07) — the one exhibit that could carry SC-C-1 visually — was the pair chosen by
rule or by outcome? A best-of-cell render is selection on outcome and will be
read as such; median-of-cell is not. We need the axis and each row's percentile.

**Q10.** `ligand_resname` in the census takes six values across 40,000 rows —
`LIG0`, `LIG1`, `LIG2`, `LIG3`, `l01`, `PEPTIDE` — so nothing shipped identifies
which molecule was placed. Were CCD codes or SMILES available at census time? It
is the difference between being able to check that a `decoy_lig` is the decoy it
was meant to be and having to take it on trust.

**Q11.** `g4_full_census_v2.json.pooled.off_site_ci_95_wilson` is [0.1736,
0.1811], and the per-arm intervals in the README are the same construction — a
Wilson interval treating 40,000 rows as independent when they are 50-sample
replicates within 800 cells over 36 receptors. Confirm the construction and we
will replace them with cluster-bootstrapped intervals ourselves; nothing in the
manuscript quotes them, but `figures/FIGURES.md:663` carries them into a caption.

---

# 3. Suggestions — what would make the paper stronger

Ranked by **what a reviewer asks first**, with a cost class: **free**
(re-analysis of data already held), **cheap** (re-scoring existing predictions,
no new inference), **real** (new predictions).

## S1 — Report the agonist-alone and agonist-plus-Gα state result. **free.** It is a title clause and the predictions already exist.

The manuscript's second clause is *the agonist alone does not*. Block A and
Block B cannot test it — neither supplies a ligand. **Block C already has the
arm**, twice:

| cell | predictions | receptors |
|---|---:|---:|
| apo × `full_agonist` — agonist, no partner | **7,000** | 35 |
| cognate × `full_agonist` — agonist and Gα together | **7,000** | 35 |

Nothing in the drop reports a state result on either. What is needed is a per-cell
predicate table — `receptor_slug`, `backbone`, `arm`, `ligand_role`, `n`,
`n_predicate_active`, `frac_predicate_active`, medians of the two axes — at most
864 rows, computed from a corpus you already hold. It is free, it is the single
highest-value item in either document, and it is blocked on an instruction rather
than on data (Q5).

The second row is worth as much as the first. Whether the two inputs are
additive, redundant or synergistic is a question no paper in our 79-paper corpus
has answered, and `vo2026fiducials` reports a high-efficacy agonist alone driving
TM6 nearly fully out with the α5 adding under 1 Å — a wet-lab result that
directly complicates our story and that we will be asked about. Block C's two
cells are the in-silico version of that experiment and they have already run.

## S2 — Recompute the 2×2 on small-molecule-agonist receptors only. **free.** It closes R1 in one line.

Twelve of SC-C-1's 23 receptors have their agonist in the pocket: 5HT1B, 5HT5A,
AA1R, AA2AR, ACM2, ACM4, ADRB2, CNR1, CNR2, LPAR1, LT4R1, OPRD. If the four signs
survive on twelve receptors, the "35.9 % of your agonist rows have no ligand in
the pocket" objection is answered by data instead of by an argument about which
side of the complex the metric reads. If they do not survive, we need to know
that before submission rather than after. Either way it is one run of an analysis
you already have, and we can do it ourselves the moment `rows.tier3.v2.csv`
arrives.

## S3 — Put an interval on everything that currently has none. **free.**

Three quantities in this block are quoted as bare point estimates in a block
whose own Flag C-1 declares cluster-boot authoritative for every CI:

- **SC-C-3's four consensus-minus-pLDDT deltas** (R11). If Chai's +0.124 survives
  a cluster bootstrap and the other three straddle zero, that is a clean
  single-backbone methods result and it goes in the paper. Right now it goes
  nowhere.
- **SC-C-7's 6.93 %** — 312 of 4,500, with no interval anywhere, on 4,500 rows
  drawn from 29 receptors × 2 backbones × 2 arms at 50 replicate samples per
  cell. The effective n is the receptor count, not the row count, and every other
  headline in the block is resampled at receptor or cluster grain.
- **The census off-site rates**, currently Wilson on 40,000 correlated rows
  (Q11).

## S4 — An agonist-versus-decoy result. **free.** The decoy predictions exist and report nothing.

Block C ran **14,400 `decoy_lig` predictions**, 7,200 per arm. The decoy role
enters SC-C-2's three-class ordinal test and nothing else; the 2×2 excludes it by
construction and the classifier is trained on agonist-versus-antagonist.
`task_A_v2_agonist_vs_decoy_apo_same_complex.json` is named in
`BLOCK_C_STATE_CHECK.md` and does not ship.

This is the arm that answers the sharpest published challenge to the paper.
`yu2026domainmotion` shows nonbinder ligands reproducing the conformational
change across 82 enzymes, with the training-set prior at 40.3 pp against a ligand
effect of 9.1–17.5 pp, and reports that ligand pLDDT is "generally not sufficient
for discriminating between binder and nonbinder ligands". A referee who knows
that paper will ask for exactly our decoy arm, and we have run it and not looked
at it. The answer has to be quantitative and has to cite them by name.

## S5 — The per-Ballesteros–Weinstein decomposition. **free.**

`s4_bw_decomposition.json` and `s4_bw_position_decomposition.json` are named in
two narrative reports and neither ships. **Across all three blocks the paper has
no residue-level account of anything.** Your own claim sheet names this as what
keeps Rung 3 at partial — *"dominant single feature = whole-pocket-aggregate; no
per-BW activation-lever"*. Twelve pocket positions, four backbones, an importance
and a direction: that is a figure, and it is the difference between "the models
encode ligand class somewhere in the pocket" and "here is where".

## S6 — Rescore the pose metric against a class-matched reference. **cheap.**

C-C-10 states the problem precisely: for agonist and decoy input rows scored
against the inactive-side reference, `ligand_rmsd_to_ref` compares a predicted
agonist pose against a bound antagonist, and the resulting RMSD carries a floor
unrelated to prediction quality. C-C-8 adds that coverage is 93–97 % on
antagonist rows and ~50 % on agonist and decoy rows, and that the missingness is
chemistry-correlated rather than random. So the one pose number the paper quotes
is scoped to the only cell where both problems vanish, and the corpus-wide
numbers are uninterpretable.

Re-running the matcher with a class-matched reference — agonist poses against
agonist-bound references — on the existing predictions would turn the pose
section from one scoped percentage into a real result. No new inference.

## S7 — A positive control for the refuted applicability domain. **free or cheap.**

SC-C-5 is a null: reference separation does not predict per-receptor classifier
reliability. A null is only as strong as the reader's confidence that the method
could have detected the effect had it been there, and we currently cannot say
"we would have detected a slope of X". The cheapest version is a power
calculation on the 60 points already in `g2_refsep_vs_auroc.csv`: inject true
slopes of 0.25, 0.5, 0.75 and report the fraction of cluster-bootstrap replicates
whose interval excludes zero. One sentence and one supplementary panel. This is
the same ask as Block A's item 5 and it is cheaper here because the regression
table shipped.

## S8 — Add real chemistry columns to the census. **cheap.**

`ligand_resname` is a slot label (Q10) and `ligand_n_heavy` is the only chemistry
in the file. Adding the CCD code or SMILES, plus a `ligand_class` derived from
the input rather than from the role label, would let anyone check that a decoy is
a decoy and let the peptide/small-molecule split — which is the load-bearing
variable in the whole census, and the one a reader will not expect — be derived
rather than trusted.

## S9 — The 21-mer α5-CT arm, with a ligand. **real.** Still the title.

Not re-asked here: S2 and S3 of `rebuttals/BLOCK_B.md` ask for the isolated
21-mer arm and for an agonist arm, and both are campaign-level. What Block C adds
is that the ligand half is now half-solved — the agonist exists, on 35 receptors,
in both partner conditions — so the outstanding run is smaller than it was. A
21-mer arm dispatched on Block C's ligand panel rather than on a bare receptor
panel would produce the paper's whole title in one campaign: peptide alone,
agonist alone, both together, against apo and against the full subunit.

One thing to reuse and one to avoid, from your own reference survey. Block C's
`reference_survey.csv` already records for OPSD/4X1H: *"α5-CT peptide of Gαt only
(no full Gα subunit); native α5-CT donor class Gt; not a heterotrimer."* That is
the only deposited peptide-bound active structure in the panel and it is the
natural motivation for the arm — and per R10 of `rebuttals/BLOCK_B.md` its
peptide is an engineered 11-mer four residues from native Gαt1, so it is the
arm's motivation and not its reference. Block C's survey knew this before our
audit found it independently, which is worth saying: the curation notes in that
file are better than the schema fields around them.
