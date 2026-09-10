# Block B — second-pass data audit (the directories `verify_claims.py` did not touch)

Scope: `02_constructs/`, `03_msa_audit/`, `04_ladder/` (the four files not in the
first pass), `08_covariates/`, `09_references/paralogy_clusters.csv`,
`11_bootstrap_draws/`, `DATA_DICTIONARY.md`, `FIGURE_BRIEF.md`, plus the
threshold-band question the dispatch raises.

Out of scope because the first pass covered them: grid completeness, exclusion
flags, thresholds, the four-arm binary ladder, the decomposition point
estimates, the 2×2, the PIF connector, fold integrity, SC-B-6's donor residual
tilt row, the reference audit, the structure bundle.

**206 checks recomputed. 166 reproduce. 40 do not, in 13 groups.** Plus one
correction to our own first-pass report.

A "check" here is one distinct assertion — a named number, a named column, a
labelled interval, one file's filter. Bulk comparisons count as one: "all 180
donor-residual CIs equal the percentiles of their own draws" is a single check,
not 180. By directory: 11_bootstrap_draws 34, 03_msa_audit 40, 08_covariates 31,
DATA_DICTIONARY 28, 04_ladder 22, 02_constructs 16, FIGURE_BRIEF 14, the
threshold band 13, paralogy_clusters 8.

Every command below was run against `data/block_b/` as shipped. All paths are
relative to the repo root. Nothing under `data/` was modified.

**Frame convention.** Unless a finding says otherwise, every number here is
**frame_36** (36 receptors; EDNRA, EDNRB, GRPR, HRH3 excluded because 7.53 is
Leu not Tyr, so NPxxY-OH is intrinsically NaN). Where a shipped number turns out
to be frame_40, that is itself the finding and it is labelled.

**Construct language.** Block B's partner is a **full Gα subunit**. The decoy arm
scrambles the last 11 residues of that subunit's α5 C-terminal tail and leaves
the remaining 339–383 residues byte-identical. No Block B arm supplies a
21-residue peptide; do not describe one that way.

---

## Answer to the two questions the dispatch asked directly

### 1. Does Block B repeat Block A's cluster-boot / receptor-boot column swap?

**No. The bootstrap labelling in Block B is honest.** This is the strongest
positive result in this pass and it should be stated plainly in the rebuttal.

I recomputed both bootstraps independently from `01_rows/rows_tidy.csv` —
resampling the 24 frame_36 paralog clusters with replacement, and separately the
36 frame_36 receptors — 20,000 draws each, and compared against every shipped
interval:

| arm | column headed `cluster_boot_ci_*_binary` | my cluster-boot | my receptor-boot | verdict |
|---|---|---|---|---|
| apo | [0.0809, 0.2564] w=0.176 | [0.0782, 0.2581] w=0.180 | [0.0937, 0.2319] w=0.138 | **cluster** |
| decoy | [0.4446, 0.6640] w=0.219 | [0.4512, 0.6661] w=0.215 | [0.4631, 0.6518] w=0.189 | **cluster** |
| shuffled | [0.7468, 0.8693] w=0.123 | [0.7483, 0.8697] w=0.121 | [0.7367, 0.8724] w=0.136 | **cluster** |
| cognate | [0.8381, 0.9424] w=0.104 | [0.8377, 0.9404] w=0.103 | [0.8262, 0.9439] w=0.118 | **cluster** |

Every arm is 4–10× closer to my cluster-boot than to my receptor-boot. Note the
discriminating detail: on shuffled and cognate the cluster interval is *narrower*
than the receptor interval, so this is not a "wider must be cluster" heuristic —
the shipped column tracks cluster in both directions.

`11_bootstrap_draws/ci_convention_audit_sc_b_1.csv` is also correctly labelled:
its `bootstrap_unit == "cluster"` rows match my cluster-boot to ≤0.006 and its
`bootstrap_unit == "receptor"` rows match my receptor-boot to ≤0.004.

The raw draw files are cluster resamples too. Two independent lines:

- Interval widths track cluster, not receptor, on 16 of 18 decomposition
  strata (e.g. panel logit occupancy: shipped 0.881, cluster 0.917, receptor
  0.791; panel probability family: shipped 0.077, cluster 0.077, receptor 0.067).
- The implied denominator of the per-draw probability statistics **varies**
  between draws and exceeds 36 on some draws (values not divisible into 36 —
  e.g. 35, 37, 41 receptor-slots). A receptor bootstrap on frame_36 would give a
  fixed 36 every draw. Only a cluster resample produces a varying receptor count.

**One real defect inside an otherwise honest convention** — see F-B-10: every
frame_36 interval is *described* as "over 26 paralog clusters", but frame_36
contains only **24** clusters. E-B-1 removes the whole `endothelin` cluster
(EDNRA + EDNRB) and the whole `bombesin` cluster (GRPR). My 24-cluster
reproduction is what matches, so the computation used 24; only the label says 26.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import pandas as pd, numpy as np
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',
  usecols=['receptor_slug','arm','cluster_id','d_npxxy_y558_y753_oh',
           'd_gpcrdb_tm6_tilt_246_637_ca','excl_E_B_1'])
r['active']=((r.d_npxxy_y558_y753_oh<9.08)&(r.d_gpcrdb_tm6_tilt_246_637_ca>14.932)).fillna(False)
f=r[~r.excl_E_B_1.astype(bool)]
arms=['apo','decoy','shuffled','cognate']
g=f.groupby(['receptor_slug','cluster_id','arm']).active.agg(['sum','count']).reset_index()
P=g.pivot_table(index=['receptor_slug','cluster_id'],columns='arm',values='sum')[arms]
S=P.values.astype(float)
N=g.pivot_table(index=['receptor_slug','cluster_id'],columns='arm',values='count')[arms].values.astype(float)
clus=P.index.get_level_values(1).values
cl=sorted(set(clus)); print("frame_36 clusters:",len(cl),"receptors:",len(clus))
def boot(units,idx,B=20000,seed=20260909):
    rng=np.random.default_rng(seed); out=np.empty((B,4))
    for b in range(B):
        rows=np.concatenate([idx[units[k]] for k in rng.integers(0,len(units),len(units))])
        out[b]=S[rows].sum(0)/N[rows].sum(0)
    return out
cb=boot(cl,{c:np.where(clus==c)[0] for c in cl})
rb=boot(list(range(len(clus))),{i:np.array([i]) for i in range(len(clus))})
d=pd.read_csv('data/block_b/04_ladder/ladder_four_scorings.csv')
s=d[(d.frame=='reproduction_36')&(d.backbone=='panel')].set_index('arm')
for i,a in enumerate(arms):
    print(f"{a:9s} shipped[{s.loc[a,'cluster_boot_ci_lo_binary']:.4f},{s.loc[a,'cluster_boot_ci_hi_binary']:.4f}]"
          f" cluster{np.round(np.percentile(cb[:,i],[2.5,97.5]),4)}"
          f" receptor{np.round(np.percentile(rb[:,i],[2.5,97.5]),4)}")
EOF
```

### 2. Does the shuffled→cognate gap concentrate in the ±0.5 Å tilt threshold band?

The dispatch asserts: *"cognate carries less threshold-band mass than shuffled on
tilt across all four backbones."*

**Panel-wide it is true. "Across all four backbones" is false — Chai inverts.**

Fraction of frame_36 rows with `|tilt − 14.932| ≤ 0.5`:

| backbone | shuffled | cognate | cognate < shuffled? |
|---|---:|---:|---|
| boltz | 0.0333 | 0.0106 | yes |
| **chai** | **0.0056** | **0.0183** | **NO — cognate carries 3.3× more** |
| of3 | 0.0189 | 0.0039 | yes |
| protenix | 0.0006 | 0.0000 | yes |
| **panel** | **0.0146** | **0.0082** | **yes** |

I ran this down before calling it a finding:

- It is not a band-width artefact. Chai inverts at every half-width from ±0.25 Å
  to ±1.5 Å. At ±2.0 Å three of four backbones invert.
- It is not a frame artefact. frame_40 gives the same 3-of-4 verdict.
- **It is one receptor.** Of the 36 frame_36 receptors, exactly **one** — OX2R —
  has any Chai cognate band mass at all, and it has a lot: 33 of its 50 Chai
  cognate rows sit within ±0.5 Å of the tilt threshold (median tilt 15.165 Å
  against a 14.932 Å threshold). Only 3 receptors have any Chai *shuffled* band
  mass. Remove OX2R and the Chai inversion disappears.
- OX2R × Chai × cognate is genuinely knife-edge: its active rate runs
  0.86 → 0.82 → 0.70 → 0.48 → 0.20 as the tilt threshold moves −0.5, −0.25, 0,
  +0.25, +0.5 Å. That single cell's call is decided at sub-Ångström resolution.

**Where the gap actually lives.** Panel-wide the shuffled→cognate tilt-pass gap
is +0.061 (0.892 → 0.953), and it comes from the **far-inactive tail**, not the
band: rows more than 2 Å *below* threshold fall from 9.0 % (shuffled) to 4.1 %
(cognate), while the whole ±0.5 Å band holds ≤1.5 % of rows in either arm. That
is the shape the "model property, not instrument" argument needs, and it holds.

**How to say it.** The argument survives, but the sentence must not say "all four
backbones". Say it panel-wide, give the per-backbone table, and name OX2R × Chai
as the single knife-edge cell — which also satisfies C-B-2's standing
instruction to report Chai separately.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import pandas as pd
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',
  usecols=['receptor_slug','arm','backbone','d_gpcrdb_tm6_tilt_246_637_ca','excl_E_B_1'])
f=r[~r.excl_E_B_1.astype(bool)].copy()
f['band']=(f.d_gpcrdb_tm6_tilt_246_637_ca-14.932).abs()<=0.5
t=f[f.arm.isin(['shuffled','cognate'])]
print(t.pivot_table(index='backbone',columns='arm',values='band',aggfunc='mean').round(4))
print("panel:", t.groupby('arm').band.mean().round(4).to_dict())
ox=f[(f.backbone=='chai')&(f.arm=='cognate')]
print("receptors with any chai cognate band mass:",
      (ox.groupby('receptor_slug').band.mean()>0).sum(), "of", ox.receptor_slug.nunique())
print("OX2R chai cognate rows in band:", int(ox[ox.receptor_slug=='OX2R'].band.sum()), "of 50")
EOF
```

---

## Findings

### F-B-1 — SC-B-2's Protenix rescue is false: the logit family CI spans zero on both frames

**Severity: high. It would reach a reader.** This is the sentence that keeps the
third rung of the ladder alive on all four backbones.

**As shipped**, `12_narrative/BLOCK_B_CLAIM_SHEET.md` (SC-B-2) and
`05_decomposition/README.md` both state, verbatim:

> Protenix's probability CI [-0.021, +0.061] crosses zero — a ceiling artefact
> (cognate = 0.974, shuffled = 0.950). Logit CI [0.35, 1.05] squarely positive.

`05_decomposition/README.md` adds the instruction: *"Report the logit CI when
Protenix appears in a per-backbone panel."*

**What the data says.** `05_decomposition/ladder_decomposition.csv`, Protenix,
`delta_correct_family_shuffled_to_cognate`, logit:

| frame | estimate | ci_lo | ci_hi |
|---|---:|---:|---:|
| reproduction_36 | +0.6745 | **−0.0472** | +5.1484 |
| all_40 | +0.1853 | **−0.0111** | +1.0594 |

**Both lower bounds are below zero.** Recomputing the 2.5th percentile directly
from the 1,000 raw draws in `11_bootstrap_draws/` gives −0.0472, matching the
shipped `ci_lo` exactly — the CSV is right and the prose is wrong. **5.7 % of the
Protenix logit family draws are ≤ 0.**

I tried every defensible variant before calling this. None produces a positive
lower bound:

| bootstrap unit | logit regularisation | frame_36 CI | frame_40 CI |
|---|---|---|---|
| cluster | clip 1e-6 | [−0.037, +10.713] | [−0.012, +0.866] |
| cluster | clip 1e-3 | [−0.037, +3.957] | [−0.012, +0.866] |
| cluster | Haldane +0.5 | [−0.037, +5.051] | [−0.012, +0.860] |
| receptor | clip 1e-6 | [−0.047, +10.694] | [−0.011, +0.726] |
| receptor | clip 1e-3 | [−0.047, +3.939] | [−0.011, +0.726] |
| receptor | Haldane +0.5 | [−0.047, +5.074] | [−0.010, +0.724] |

The quoted pair looks constructed rather than computed: **0.35 ≈ the all_40
Protenix logit family *point estimate* (0.3493)** and **1.05 ≈ the all_40 *upper*
bound (1.0594)**. A point estimate appears to have been read into the lower-bound
slot. (The quoted probability lower bound, −0.021, matches nothing in the drop;
the file carries −0.0011 on all_40 and −0.0016 on frame_36.)

**Consequence.** Under the CI-gated reading the block uses everywhere else,
Protenix's correct-family term **does not sign on either scale**. The logit scale
does not rescue it. Any per-backbone family-term panel that prints "squarely
positive" for Protenix prints a false claim.

**What would close it.** Upstream re-derives the Protenix per-backbone CI and
either corrects the claim sheet and `05_decomposition/README.md`, or explains
what run produced [0.35, 1.05]. Until then: quote the shipped `ci_lo`/`ci_hi`
from `ladder_decomposition.csv`, state the frame, and say Protenix's family term
is undetermined on both scales.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import pandas as pd, numpy as np
s=pd.read_csv('data/block_b/05_decomposition/ladder_decomposition.csv')
print(s[(s.backbone=='protenix')&(s.contrast=='delta_correct_family_shuffled_to_cognate')]
      [['frame','scale','term_estimate','ci_lo','ci_hi']].round(4).to_string(index=False))
d=pd.read_csv('data/block_b/11_bootstrap_draws/ladder_decomposition_bootstrap_draws.csv')
p=d[(d.backbone=='protenix')&(d.scale=='logit')&
    (d.contrast=='delta_correct_family_shuffled_to_cognate')].term_estimate
print("draws 2.5/97.5 pct:", np.percentile(p,[2.5,97.5]).round(4), " frac<=0:", (p<=0).mean())
EOF
```

---

### F-B-2 — SC-B-11's "no covariate signal" is a panel average of two significant, oppositely-signed backbone slopes

**Severity: high. It would reach a reader.** This is the claim that ladder height
is not predictable from reference geometry.

**As shipped**, `12_narrative/BLOCK_B_CLAIM_SHEET.md` (SC-B-11):

> **Claim**: On the three usable predictors … no panel slope excludes zero at
> 95% CI on either continuous or logit scale, with or without AA2AR. Under the
> CI-gated reading, ladder height does not scale with reference gap or coupling
> promiscuity at the resolution 40 receptors support.

`12_narrative/caveats/C-B-14_no_covariate_slope_excludes_zero.md` repeats it and
prescribes a manuscript sentence saying the same. Neither document reports any
per-backbone slope.

**What the data says.** `08_covariates/ladder_height_regressions.csv` ships 80
rows, of which the claim sheet quotes only the 6 `backbone == "panel"` rows. Two
of the per-backbone rows exclude zero, and they point in opposite directions:

| backbone | predictor | scale | slope | 95% CI | excludes 0? |
|---|---|---|---:|---|---|
| **chai** | delta_ref_tilt | logit | **−0.951** | **[−2.015, −0.054]** | **yes** |
| **of3** | delta_ref_tilt | logit | **+0.937** | **[+0.232, +1.661]** | **yes** |
| boltz | delta_ref_tilt | logit | +0.247 | [−0.282, +0.755] | no |
| protenix | delta_ref_tilt | logit | +0.305 | [−0.003, +0.892] | no (touches) |
| **panel** | delta_ref_tilt | logit | **+0.134** | [−0.222, +0.486] | no |

Both survive AA2AR removal (chai −0.949 [−2.019, −0.058]; of3 +0.985
[+0.289, +1.748]), so this is not the AA2AR anomaly C-B-8 already covers.

**And the panel row is arithmetically the mean of the four backbone slopes** —
exactly, to 1e-9, on all six predictor × scale combinations. So the panel null is
not an independent pooled estimate that failed to find signal; it is
`(+0.247 − 0.951 + 0.937 + 0.305)/4`. Three backbones sign positive or touch
zero; Chai alone carries a large negative and cancels them.

**`claim_answers.csv` vouches for the false version.**
`08_covariates/claim_answers.csv` carries the row

```
SC-B-11,any_predictor_ci_excludes_zero,False,,,ladder_height_regressions.csv,True
```

That is contradicted by its own cited file — four rows on the named predictors
exclude zero, plus five `cognate_family` rows (including `panel`,
`cognate_family=Gs`, continuous: +1.309 [+0.281, +2.337]). This is the same
self-certifying-column failure class as `matches_claim_sheet_bool` in D-B-2 and
`matches_claim_sheet` in Block A, and here it certifies a boolean summary of the
whole file.

**Secondary.** The claim sheet lists three predictors plus a degenerate fourth.
The file ships a **fifth**, `cognate_family` (40 rows), never mentioned in
SC-B-11 or C-B-14 — and it is the one that signs at panel level. Its rows are
per-family group estimates, not slopes on a continuous predictor, so "excludes
zero" means something different there; it should be named and scoped, not
silently omitted.

**Consequence.** "Ladder height does not scale with reference gap" is defensible
*panel-wide*, and only panel-wide. The honest statement is that two of four
backbones show a Δ_ref-tilt effect on the logit scale with CI excluding zero, in
opposite directions, and that the panel-level null is their average. That is a
*different and more interesting* result than "no signal", and it is a
Chai-versus-the-rest result, which C-B-2 already predicts.

**What would close it.** Report the per-backbone table alongside the panel row in
SC-B-11 and C-B-14; correct `any_predictor_ci_excludes_zero`; and state that the
panel slope is a mean over backbones, not a pooled regression.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import pandas as pd
g=pd.read_csv('data/block_b/08_covariates/ladder_height_regressions.csv')
m=g[g.predictor.isin(['delta_ref_npxxy','delta_ref_tilt','n_ga_families'])]
sig=m[((m.ci_lo_all>0)|(m.ci_hi_all<0))|((m.ci_lo_no_aa2ar>0)|(m.ci_hi_no_aa2ar<0))]
print("CI excludes zero on a named predictor:")
print(sig[['backbone','predictor','outcome_scale','slope_all','ci_lo_all','ci_hi_all',
           'slope_no_aa2ar','ci_lo_no_aa2ar','ci_hi_no_aa2ar']].round(4).to_string(index=False))
for pred in ['delta_ref_npxxy','delta_ref_tilt','n_ga_families']:
    for sc in ['continuous','logit']:
        s=g[(g.predictor==pred)&(g.outcome_scale==sc)]
        bb=s[s.backbone!='panel'].slope_all.mean(); pn=s[s.backbone=='panel'].slope_all.iloc[0]
        print(f"{pred:16s} {sc:11s} mean(backbones)={bb:+.6f} panel={pn:+.6f} equal={abs(bb-pn)<1e-9}")
print("\nclaim_answers says:")
print(pd.read_csv('data/block_b/08_covariates/claim_answers.csv').tail(1).to_string(index=False))
EOF
```

---

### F-B-3 — SC-B-2's four per-backbone logit family shares do not exist in the cited file

**Severity: high. It would reach a reader** — it is the sentence that says the
family rung is consistent across backbones.

**As shipped**, `12_narrative/BLOCK_B_CLAIM_SHEET.md` (SC-B-2):

> **Per-backbone logit family share** (all four backbones agree, 17–21%):
> boltz 17.4%, chai 17.5%, of3 20.9%, protenix 17.5%.

`05_decomposition/claim_answers.csv` carries all four as
`family_logit_share_{boltz,chai,of3,protenix}_pct` with
`source_file = ladder_decomposition.csv` and `matches_claim_sheet_bool = True`.

**What the data says.** `ladder_decomposition.csv`'s own `term_share` column, on
the `delta_correct_family_shuffled_to_cognate` / `logit` rows:

| backbone | claim sheet | frame reproduction_36 | frame all_40 |
|---|---:|---:|---:|
| boltz | 17.4 % | **14.2 %** | 10.0 % |
| chai | 17.5 % | **22.9 %** | 19.8 % |
| of3 | 20.9 % | **23.6 %** | 19.0 % |
| protenix | 17.5 % | **10.9 %** | 4.0 % |
| *(panel)* | *17.4 %* | *17.4 %* | *12.9 %* |

Not one of the four matches on either frame. The true frame_36 spread is
**10.9 – 23.6 %**, not 17–21 %, and the true all_40 spread is 4.0 – 19.8 %. So
"all four backbones agree" is false on both frames: Protenix is the low outlier
by a factor of two, which is exactly the backbone F-B-1 shows has an unsigned
family term.

Note that the quoted boltz value, 17.4 %, is numerically the **panel** share
(17.37 %) — consistent with the per-backbone slots having been filled from the
pooled row rather than read from the file.

I tried the defensible alternatives and none reproduces the quoted set: pooled
rows per backbone (the table above), median of per-receptor logit shares
(boltz 0.0, chai 0.0, of3 17.9, protenix 0.0), and mean of per-receptor shares
(boltz 7.1, chai −∞, of3 11.5, protenix 2.4). The per-receptor routes degenerate
because many receptors are ceiling- or floor-pinned (C-B-7).

**What would close it.** Replace the four numbers with the file's own `term_share`
values, state the frame, and drop "all four backbones agree" — or replace it with
"10.9 – 23.6 % on frame_36, with Protenix the low outlier".

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd
s=pd.read_csv('data/block_b/05_decomposition/ladder_decomposition.csv')
f=s[(s.contrast=='delta_correct_family_shuffled_to_cognate')&(s.scale=='logit')]
print(f.pivot(index='backbone',columns='frame',values='term_share').round(4)*100)
print(pd.read_csv('data/block_b/05_decomposition/claim_answers.csv').tail(4).to_string(index=False))"
```

---

### F-B-4 — SC-B-11's logit regressions are frame_40, and the frame flips its only directional claim

**Severity: medium-high. It would reach a reader** through C-B-14's prescribed
manuscript sentence.

**As shipped.** The claim sheet's own frame rule states: *"Every published
two-instrument Block B number uses frame_36."* The ladder height being regressed
is a two-instrument predicate rate. But SC-B-11's table reports `n = 40` for both
logit rows (Δ_ref tilt and coupling promiscuity) — i.e. frame_40 — and the
`08_covariates/` README and C-B-14 say "on the 40 Class A receptors" without
naming a frame.

**What the data says.** `ladder_height_covariates.csv` carries all 40 receptors,
and the four E-B-1 receptors carry `family_term_logit = 0.0` **exactly**:

| receptor | family_term_continuous | family_term_logit | delta_ref_tilt |
|---|---:|---:|---:|
| EDNRA | NaN | **0.0** | 3.754 |
| EDNRB | −0.308 | **0.0** | 2.724 |
| GRPR | 2.070 | **0.0** | 5.386 |
| HRH3 | NaN | **0.0** | 3.749 |

Those zeros are structural, not measured: with NPxxY-OH intrinsically NaN the
two-instrument predicate is False on every arm, so shuffled and cognate rates are
both 0 and the family term is forced to exactly 0. Four forced zeros are being
fed into a 40-point regression as if they were observations.

Refitting the same OLS on frame_36:

| predictor | scale | frame_40 (as shipped) | frame_36 |
|---|---|---:|---:|
| delta_ref_npxxy | logit | −0.0374 (n=34) | −0.0374 (n=34) — unaffected |
| delta_ref_tilt | logit | **+0.1343** (n=40) | **+0.0018** (n=36) |
| coupling promiscuity | logit | **−0.0719** (n=40) | **+0.0305** (n=36) |

The NPxxY rows are unaffected because all four E-B-1 receptors already drop out
on `delta_ref_npxxy = NaN`. The tilt slope shrinks by 75×. **The coupling
promiscuity slope changes sign.**

That matters because it is the one direction C-B-14 asserts:

> Coupling promiscuity signs weakly in the learned-coupling direction (negative
> slope: promiscuous receptors show smaller family term)

On frame_36 the slope is **positive**. The claim's only directional content
reverses under the frame the block otherwise mandates. (The headline "no slope
excludes zero" survives — the frame_36 slopes are closer to zero, not further.)

**What would close it.** Refit the logit rows on frame_36, or state explicitly
that SC-B-11 is a frame_40 result and why, and delete the coupling-promiscuity
direction sentence.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import pandas as pd, numpy as np
c=pd.read_csv('data/block_b/08_covariates/ladder_height_covariates.csv')
e=['EDNRA','EDNRB','GRPR','HRH3']
print(c[c.receptor.isin(e)][['receptor','family_term_continuous','family_term_logit','delta_ref_tilt']].to_string(index=False))
for pred in ['delta_ref_npxxy','delta_ref_tilt','n_ga_families']:
    a=c[[pred,'family_term_logit']].dropna()
    b=c[~c.receptor.isin(e)][[pred,'family_term_logit']].dropna()
    print(f"{pred:16s} frame_40 n={len(a)} slope={np.polyfit(a[pred],a.family_term_logit,1)[0]:+.4f}"
          f" | frame_36 n={len(b)} slope={np.polyfit(b[pred],b.family_term_logit,1)[0]:+.4f}")
EOF
```

---

### F-B-5 — The data dictionary names the wrong pooled-stratum label, and the drop uses two vocabularies

**Severity: medium. Plumbing, but it silently produces an empty panel.** It cost
me a false positive in this very audit.

**As shipped**, `DATA_DICTIONARY.md` § `04_ladder/ladder_four_scorings.csv`:

> | backbone | string | {boltz, chai, of3, protenix, **panel_all**} |

**What the data says.** That file's `backbone` column contains `panel`, not
`panel_all`. Filtering on the documented value returns **zero rows, silently** —
which is what happened to me on my first pass at this file, and is the mirror
image of the `panel` / `panel_all` false positive the first-pass report already
records.

The drop carries two vocabularies with no key:

| label | files |
|---|---|
| `backbone == "panel"` | ladder_four_scorings, ladder_decomposition, both decomposition draw files, donor_class_residuals_summary, donor_class_covariate_regression, phase5_power_analysis, both donor draw files, ladder_height_regressions (**10 files**) |
| `backbone == "panel_all"` | `06_interface/interface_2x2.csv` (**1 file**) |
| `frame ∈ {all_40, reproduction_36}` | ladder_four_scorings, ladder_decomposition, both decomposition draw files |
| `frame ∈ {frame_36, frame_40}` | `06_interface/interface_2x2.csv` |

`FIGURE_BRIEF.md` gets both right (BB-1 says `frame == "reproduction_36"`, BB-3
says `frame == "frame_36"` and `backbone == "panel_all"`) — so the brief is
correct and the dictionary is not.

**What would close it.** Correct the dictionary entry, and add a one-line
vocabulary key to `DATA_DICTIONARY.md` stating that `interface_2x2.csv` alone
uses `panel_all` / `frame_36`. Our own panel scripts should assert non-empty
after every stratum filter.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd
d=pd.read_csv('data/block_b/04_ladder/ladder_four_scorings.csv')
print('backbone values:',sorted(d.backbone.unique()))
print('rows matching documented value panel_all:',(d.backbone=='panel_all').sum())
i=pd.read_csv('data/block_b/06_interface/interface_2x2.csv')
print('interface_2x2 backbone:',sorted(i.backbone.unique()),'frame:',sorted(i.frame.unique()))"
grep -n 'panel_all' data/block_b/DATA_DICTIONARY.md
```

---

### F-B-6 — The data dictionary names columns that do not exist, including in two files the figure brief points at

**Severity: medium.** A panel script that follows the dictionary raises a
KeyError at best.

**As shipped.** `DATA_DICTIONARY.md` claims in its opening line: *"Every column
of every CSV shipped in this zip: name, dtype, units, allowed values, NaN
convention, source."*

**What the data says.** Five sections name columns absent from the file:

| file | dictionary names | file actually has |
|---|---|---|
| `04_ladder/ladder_continuous_distributions.csv` | `median` | `p50` (and undocumented `n_nan`) |
| `04_ladder/ladder_adjacent_pair_separation.csv` | `arm_from`, `arm_to`, `signals_beyond_iqr_bool` | `adjacent_pair`, `axis`, `shift_over_iqr_ratio`, `median_low/high`, `iqr_low/high`, `n_low/high` |
| `07_donor_residuals/donor_class_residuals_bootstrap_draws.csv` | `draw_id`, `statistic`, `value` | `draw_idx`, `median` |
| `07_donor_residuals/donor_class_covariate_regression.csv` | `slope`, `ci_lo`, `ci_hi`, `n` | `stratum`, `native_minus_chimera_delta`, `delta_ci_lo`, `delta_ci_hi`, … |
| `07_donor_residuals/donor_class_residuals.csv` | `active_stabilization_source`, `input_sha256` | neither present |

Two of these are files `FIGURE_BRIEF.md` sends the figure agent to directly:
BB-1 → `ladder_continuous_distributions.csv` for "the continuous-axis companion
table" (the very quantity D-B-2 is about — and the column the agent would reach
for, `median`, is named `p50`), and BB-5 → `donor_class_residuals_bootstrap_draws.csv`
for CI shading (**all three** documented column names are wrong).

Four further sections name **no** columns at all:
`ladder_threshold_proximity.csv` (11 columns), `midpoint_ladder_28.csv` (13),
`interface_chai_plddt_inversion.csv` (7), `reference_set.blockb_pinned.csv` (34).

Seventeen of the drop's 44 CSVs have no section at all. Nine are the
per-directory `claim_answers.csv` files, which are arguably self-describing. The
other **eight are undocumented data files**: `02_constructs/donor_ga_class.csv`
(the table Phase 5 and Phase 6b depend on),
`02_constructs/d2_arm_sequence_audit.csv`, `07_donor_residuals/external_ruler.csv`,
`08_covariates/reference_separation_pocket_ca.csv`,
`09_references/native_gs_curation_audit.csv`, and **all three files in
`11_bootstrap_draws/`** — the directory `FIGURE_BRIEF.md` sends the figure agent
to for CI shading.

All row-count claims in the dictionary are **correct** (27 of 27).

**What would close it.** Regenerate `DATA_DICTIONARY.md` from the CSV headers
rather than by hand. Until then, no panel script should take a column name from
the dictionary without checking it against `pd.read_csv(...).columns`.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import re, os, pandas as pd
B='data/block_b/'; txt=open(B+'DATA_DICTIONARY.md').read()
for p in re.split(r'\n## ','\n'+txt)[1:]:
    m=re.match(r'`?([0-9]{2}_[a-z_]+/[A-Za-z0-9_.\-]+\.csv)`?', p.split('\n',1)[0].strip())
    if not m or not os.path.exists(B+m.group(1)): continue
    cols=set(c for c in re.findall(r'^\|\s*`?([A-Za-z_]\w*)`?\s*\|',p,re.M) if c.lower()!='column')
    for blk in re.findall(r'[Cc]olumns[\s\w]*?:?\s*`([^`]+)`',p):
        cols|={c.strip() for c in blk.replace('\n',' ').split(',') if c.strip() and c.strip()!='...'}
    actual=list(pd.read_csv(B+m.group(1)).columns)
    ghost=sorted(c for c in cols if c not in actual)
    if not cols: print(f"NO COLUMNS DOCUMENTED: {m.group(1)} ({len(actual)} columns)")
    elif ghost: print(f"GHOST COLUMNS in {m.group(1)}: {ghost}")
EOF
```

---

### F-B-7 — SC-B-8 misdescribes the decoy construct on two counts

**Severity: medium. It would reach a reader** — this is the Methods sentence
describing what a decoy is.

**As shipped**, `12_narrative/BLOCK_B_CLAIM_SHEET.md` (SC-B-8):

> **Claim**: Every decoy is length-matched to its cognate Gα parent,
> byte-identical over the first **339–349 residues**, and edited over the last
> **9–11 residues** at the α5-CT tail (median tail Hamming 9.5).

**What the data says**, from the 40-row per-receptor table in
`02_constructs/decoy_scramble_verification.md`:

1. **The byte-identical prefix runs 339–383 residues, not 339–349.** Prefix
   length is `parent_length − 11`, and there are four parent lengths:

   | cognate class | parent | length | prefix | n receptors |
   |---|---|---:|---:|---:|
   | Gt | alphat | 350 | **339** | 1 |
   | Gi | alphai1 | 354 | 343 | 24 |
   | Gq | alphaq | 359 | 348 | 10 |
   | **Gs** | **alphas** | **394** | **383** | **5** |

   The stated upper bound of 349 excludes all five Gs receptors (AA2AR, ADRB1,
   ADRB2, FSHR, LSHR), whose decoys are byte-identical over 383 residues.

2. **The edited region is exactly the last 11 residues in all 40 cases**, not
   "9–11". `cognate_len − prefix_len == 11` for every one of the 40. The 9–11
   appears to be a garbled reading of the Hamming distance, which itself runs
   **7–11**, not 9–11: two decoys (ACM4, APJ) differ from their parent at only
   **7** of 11 tail positions and three more (CCKAR, CNR1, GHSR) at 8.

   The median Hamming **is** 9.5 as claimed (mean 9.525), so that half of the
   sentence reproduces.

Conflating "length of the edited region" with "number of positions changed" is
the specific hazard: a reader told the edit spans "9–11 residues" will think the
construct varies in edit *extent*. It does not. What varies is how many of the
fixed 11 positions the permutation happened to move, and the weakest decoy moved
only 7 — a fact the "9–11" wording hides.

**Everything else in SC-B-8 reproduces** — see the not-a-finding section.

**What would close it.** Reword to: *"byte-identical over the first 339–383
residues (all but the last 11), with the last 11 α5-CT positions permuted; tail
Hamming 7–11, median 9.5."*

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 - <<'EOF'
import re, pandas as pd
t=open('data/block_b/02_constructs/decoy_scramble_verification.md').read()
rows=re.findall(r'^\| (\w+) \| (G\w+) \| (\w+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| yes \| PASS \|$',t,re.M)
d=pd.DataFrame(rows,columns=['receptor','class','parent','cog','dec','prefix','ham'])
d[['cog','dec','prefix','ham']]=d[['cog','dec','prefix','ham']].astype(int)
print("n =",len(d))
print("prefix range:",d.prefix.min(),"-",d.prefix.max(),"| by class:",d.groupby('class').prefix.unique().to_dict())
print("edited-region length (cog-prefix), unique:",sorted((d.cog-d.prefix).unique()))
print("hamming: min %d max %d median %.1f mean %.3f"%(d.ham.min(),d.ham.max(),d.ham.median(),d.ham.mean()))
print("receptors with hamming < 9:",d[d.ham<9].receptor.tolist())
EOF
```

---

### F-B-8 — SC-B-9's "verified on 18/18" is arithmetically inconsistent and overstates OF3

**Severity: medium. It would reach a reader** — it is the instrument-validity
sentence for the decoy arm.

**As shipped**, `12_narrative/BLOCK_B_CLAIM_SHEET.md` (SC-B-9):

> … carries the scrambled α5-CT residues as uppercase aligned columns (verified
> on **18/18 audited cells, 6 receptors × 2 arms × 3 backbones**).

**What the data says.**

1. **6 × 2 × 3 = 36, not 18.** `03_msa_audit/PHASE_1D_EXTENSION.md` is explicit:
   *"Scope: read-only ssh, bounded to 6 receptors × 2 arms × 3 backbones = 36
   MSAs."* The 18 is the **decoy-only** subset (6 receptors × 3 backbones). The
   claim sheet has attached the decoy-only numerator to the full audit's
   denominator description.

2. **12 of the 18 are empirically verified, not 18.** The claim sheet's own table
   one line below marks OF3 as "6/6 **(by construction)**", and PHASE_1D_EXTENSION
   states that OF3's raw MSAs are purged from `$TMPDIR` post-run so *"direct
   column-level inspection is not possible"*. Its verdict reads *"READ (uppercase)
   by construction; not directly re-verifiable at column level"*. The word
   "verified" in the headline sentence covers 12 empirical cells (Boltz 6,
   Protenix 6) and 6 inferred ones.

The compensating chain for OF3 is genuinely tight (query bytes recorded in
`inference_query_set.json`, shim forwards verbatim, ColabFold row 0 is the query
by construction, confirmed empirically on Boltz and Protenix on the same
queries), and C-B-1/C-B-2 carry the caveat. The defect is the headline word, not
the underlying evidence.

**Related, and worth carrying into any Chai sentence.** Phase 1 §1d records that
for **2 of the 40** Chai decoy `.aligned.pqt` files (ADRB1 and LSHR) the query row
ends with the **WT parent** α5-CT in uppercase — i.e. at the MSA layer those two
decoys look like their cognate. 19 have ≥3 trailing gaps, 19 have 1–2 trailing
gaps plus mostly-WT residues, 21 of 40 carry scrambled residues as lowercase
insertions. Whether Chai's feature builder reads the pqt query row or re-aligns
the raw decoy sequence is explicitly undecided and on the deferred list.

**What would close it.** Reword to *"36 MSAs audited (6 receptors × 2 arms × 3
backbones); the decoy edit is read as uppercase aligned columns in 12/12
empirically inspectable decoy cells (Boltz, Protenix) and 6/6 by construction on
OF3, whose raw MSA is purged post-run."*

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper
grep -n '6 receptors × 2 arms × 3 backbones' data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md data/block_b/12_narrative/BLOCK_B_CLAIM_SHEET.md
grep -n 'by construction' data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md | head -5
grep -n 'ends with WT parent tail' data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md
```

---

### F-B-9 — See "Answer to question 2" above (Chai inverts the threshold-band claim)

Recorded there in full rather than repeated. Severity: medium; it would reach a
reader, because the dispatch asks us to make "across all four backbones" the
form of the argument.

---

### F-B-10 — Every frame_36 CI is labelled "over 26 paralog clusters"; frame_36 has 24

**Severity: medium.** It reaches the reader through the Methods statement of the
resampling unit.

**As shipped.** `BLOCK_B_CLAIM_SHEET.md` header: *"**Bootstrap convention**: 26
paralog clusters"*, and SC-B-1, SC-B-2, SC-B-3, SC-B-6 and SC-B-11 each say
"cluster-boot 95% CI over 26 paralog clusters" on numbers that are frame_36.
`DATA_DICTIONARY.md` describes `cluster_boot_ci_lo_binary` as "26-cluster
bootstrap CI".

**What the data says.** `09_references/paralogy_clusters.csv` has 26 clusters
over 40 receptors. E-B-1 removes EDNRA, EDNRB (the entire `endothelin` cluster)
and GRPR (the entire `bombesin` cluster). **frame_36 therefore contains 24
clusters, not 26** — and my 24-cluster reproduction is the one that matches the
shipped intervals (see question 1 above), so the computation was correct; only
the label is wrong.

**Also in C-B-14**, which describes the same resampling unit:

> The under-power is consistent with only **15 multi-member** paralog clusters
> carrying the resampling weight; **11 of 26** clusters are singletons.

Actual, from the file: **12 multi-member** (2 of size 3 — serotonin, muscarinic;
10 of size 2) and **14 singletons**. Both numbers are wrong, and they are wrong
in the direction that overstates the resampling weight available.

**What would close it.** State "24 clusters on frame_36 / 26 on frame_40" in the
Methods, and correct C-B-14 to 12 multi-member and 14 singletons.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd
p=pd.read_csv('data/block_b/09_references/paralogy_clusters.csv')
sz=p.cluster_id.value_counts()
print('all_40: clusters',len(sz),'multi-member',(sz>1).sum(),'singletons',(sz==1).sum())
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',usecols=['cluster_id','excl_E_B_1'])
print('frame_36 clusters:',r[~r.excl_E_B_1.astype(bool)].cluster_id.nunique())
print('clusters removed by E-B-1:',set(r.cluster_id.unique())-set(r[~r.excl_E_B_1.astype(bool)].cluster_id.unique()))"
```

---

### F-B-11 — Three subset labels in `midpoint_ladder_28.csv` contradict their own receptor counts

**Severity: low-medium.** It would reach a reader only through a caption that
names a subset by its label.

`04_ladder/midpoint_ladder_28.csv` enumerates 13 candidate subsets attempted for
the withdrawn W-B-2 midpoint ladder. Three carry a receptor count in the label
that contradicts the file's own `n_receptors` column:

| subset label | label says | `n_receptors` |
|---|---:|---:|
| `native_active_only_no_nan_np_25` | 25 | **22** |
| `exclude_nan_np_and_sealed_28` | 28 | **30** |
| `exclude_nan_np_and_chim_and_agonist_only_28` | 28 | **32** |

(`exclude_nan_np_only_36` → 36, `exclude_nan_np_and_heldout_28` → 28,
`exclude_heldout_only_32` → 32 and the rest are consistent.)

The file itself is honest about the withdrawal: **0 of 13** subsets carry
`reproduces_within_0_02 = True`, the closest being
`native_active_only_no_nan_np_25` at Euclidean distance 0.038 from the
0.130/0.500/0.801/0.887 target. W-B-2 is well supported.

**What would close it.** Never quote a subset by its label; quote `n_receptors`
and the `members` list. Upstream should rename the three.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd, re
m=pd.read_csv('data/block_b/04_ladder/midpoint_ladder_28.csv')
for _,r in m.iterrows():
    x=re.search(r'_(\d+)\$', r.subset)
    if x and int(x.group(1))!=r.n_receptors: print(r.subset,'label',x.group(1),'actual',r.n_receptors)
print('subsets reproducing within 0.02:', int(m.reproduces_within_0_02.sum()), 'of', len(m))"
```

---

### F-B-12 — All seven SC-B-7 metrics are sourced to a file containing no templates evidence

**Severity: low. Plumbing — it does not reach a reader**, but it is the same
self-certifying pattern and it makes SC-B-7 look unverifiable when it is not.

`03_msa_audit/claim_answers.csv` names `PHASE_1_CONSTRUCT_IDENTITY.md` as
`source_file` for all seven SC-B-7 rows (launcher greps for all four backbones,
the row-echo absence, the 20-file sweep size and its zero positive hits), each
with `matches_claim_sheet_bool = True`.

**That file contains zero occurrences of the string "template".** So does
`msa_depth_report.md`. The only "template" in `PHASE_1D_EXTENSION.md` is a
`$TMPDIR/.../template}/` directory path.

The evidence **is** in the drop — `12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md`
§0d (per-backbone evidence class) and §"Phase 0 §Item 3 — Templates-off HPC
sweep" (0/20 files with a `runtime_config` block, 0/20 with any
`template*`/`pdb70`/`pdb_seqres`/`custom_templates` key). The claim sheet's own
cited sources (`docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md`,
`docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md`) are **not** shipped.

One substantive nuance while we are here: SC-B-7's header says "Class b + c
evidence" for all four backbones, but the dossier §0d assigns class (b) to **OF3
only** (explicit `--use-templates false`) and class (c) to Boltz, Chai and
Protenix (absence of a flag plus upstream default). Absence of a flag is arguably
class (b), but the two documents do not agree, and C-B-1 is the caveat that has
to carry it.

**What would close it.** Point `claim_answers.csv` at
`12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md`, or ship the two Phase 0 docs.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper
grep -c -i template data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md
grep SC-B-7 data/block_b/03_msa_audit/claim_answers.csv
grep -n -i 'Templates-off' data/block_b/12_narrative/EXPERIMENT_DOSSIER_BLOCK_B.md
```

---

### F-B-13 — `ladder_threshold_proximity.csv` computes against 9.082; the corpus uses 9.08

**Severity: low.** Extends the first pass's D-B-3 from the prose into a derived
data file.

D-B-3 records that the claim sheet and drop README state the NPxxY predicate as
`< 9.082 Å` while all 32,000 rows carry `threshold_npxxy_oh_active_lt = 9.08`.
The derived file `04_ladder/ladder_threshold_proximity.csv` carries
`threshold = 9.082` in all 16 NPxxY rows — so its `frac_within_0p5A` and
`frac_within_1p0A` are measured around a threshold the corpus does not use. Its
tilt threshold, 14.932, matches the rows.

At 0.002 Å the numerical effect is below anything the panel can show. The reason
to record it is that this is the second derived artefact in two blocks computed
against a threshold the rows do not carry.

**What would close it.** Quote 9.08 Å once in Methods, as D-B-3 already
recommends, and note that the proximity file's band is centred 0.002 Å away.

**Reproduction**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd
t=pd.read_csv('data/block_b/04_ladder/ladder_threshold_proximity.csv')
print(t.groupby('axis').threshold.unique().to_dict())
r=pd.read_csv('data/block_b/01_rows/rows_tidy.csv',usecols=['threshold_npxxy_oh_active_lt','threshold_gpcrdb_tm6_tilt_active_gt'])
print('rows carry:', r.threshold_npxxy_oh_active_lt.unique(), r.threshold_gpcrdb_tm6_tilt_active_gt.unique())"
```

---

## Correction to our own first-pass report

**D-B-1 says: "There is no ceiling-pinning flag anywhere in the drop." That is
wrong, and I should retract it.**

`04_ladder/ladder_per_receptor.csv` ships a `ceiling_pinned` boolean column that
implements exactly the definition D-B-1 says is unimplemented — `cognate_rate ≥
0.98` — matching on **160 of 160** rows, and giving **29 / 28 / 24 / 34** pinned
cells for boltz / chai / of3 / protenix, inside C-B-7's stated 24–34. The same
file also ships an undocumented-in-the-claim-sheet `floor_pinned` column
(`apo_rate ≤ 0.02`; 31 / 27 / 25 / 36) and `all_nan_np_arm`, which flags exactly
EDNRA, EDNRB, GRPR, HRH3.

What D-B-1 got right and should keep: there is no *row-level* `excl_E_B_4`
ceiling flag — the row-level `excl_E_B_4` is the non-native active-reference set,
and a panel that "applies E-B-4" still gets the wrong thing. The correct wording
is: **the ceiling-pinning flag exists, at cell grain, in
`ladder_per_receptor.csv`; it is not the `excl_E_B_4` row flag, and the claim
sheet's exclusion header mislabels which is which.**

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper && python3 -c "
import pandas as pd
d=pd.read_csv('data/block_b/04_ladder/ladder_per_receptor.csv')
print('ceiling_pinned == (cognate_rate>=0.98):',(d.ceiling_pinned==(d.cognate_rate>=0.98)).sum(),'/',len(d))
print('per backbone:',d.groupby('backbone').ceiling_pinned.sum().to_dict())
print('floor_pinned == (apo_rate<=0.02):',(d.floor_pinned==(d.apo_rate<=0.02)).sum(),'/',len(d))"
```

---

## What I checked that turned out NOT to be a finding

This section is the point of the pass as much as the findings are. Each of the
following looked like a defect and was run down until it wasn't.

**Bootstrap machinery — the headline negative result.**

1. **The cluster/receptor swap does not recur.** Covered in full above. Four
   independent shipped intervals, the `ci_convention_audit` file's two labelled
   columns, and the draw-level denominators all agree with cluster resampling.
2. **The 30 decomposition summary CIs reproduce from the raw draws exactly** —
   `ci_lo`/`ci_hi` in `ladder_decomposition.csv` equal the 2.5th/97.5th
   percentiles of the matching 1,000 draws to floating-point (max deviation
   4×10⁻¹⁶) on all 30 frame_36 strata.
3. **The 180 donor-residual summary CIs reproduce from the raw draws** to
   ≤1.2×10⁻³, with a typical deviation of ~3×10⁻⁵ — a percentile-interpolation
   difference (linear vs nearest-rank), not a different computation.
4. **The two copies of each draw file are byte-equal.**
   `11_bootstrap_draws/donor_class_residuals_bootstrap_draws.csv` and
   `07_donor_residuals/donor_class_residuals_bootstrap_draws.csv` are identical,
   as the README says.
5. **The 90 donor-residual strata with no draws are correctly handled.** All 90
   carry `note = "n_receptors<5_no_bootstrap"` and null `ci_lo`/`ci_hi`. None
   ships a CI it cannot support. This is good hygiene and worth saying so.
6. **SC-B-6's `residual_npxxy` and `residual_delta_to_active` CIs are not
   irreproducible.** The claim sheet quotes [−0.50, +0.29] and [−0.32, +0.50];
   the draws give [−0.477, +0.317] and [−0.301, +0.561]. I bootstrapped the
   1,000 draws to get the Monte-Carlo standard error of the percentile endpoints
   themselves: 0.009–0.037. The differences are 1–2 MC standard errors, i.e.
   ordinary run-to-run bootstrap noise, and no signed status changes (all three
   span zero either way). Not a finding.
7. **SC-B-6's `n_receptors` of 23 and 21 are not wrong.**
   `donor_class_residuals_summary.csv` reports `n_receptors = 24` on all three
   axes, which looked like a contradiction. It is a column-semantics difference:
   the summary's `n_receptors` is the stratum's receptor count, while the claim
   sheet's 23 and 21 are `n_rows_axis / 200` (4,600/200 and 4,200/200) — the
   receptors with non-NaN data on that axis. Both are defensible; they measure
   different things.

**Paralogy clusters (C-B-13).**

8. **`09_references/paralogy_clusters.csv` is well-formed.** 40 rows, 40 distinct
   receptors, zero duplicates, 26 clusters, every receptor in exactly one
   cluster, no receptor missing and none extra. Sizes are sensible: 2 clusters of
   3 (serotonin, muscarinic), 10 of 2, 14 singletons. The `cluster_id` column in
   `rows_tidy.csv` agrees with this file on **40 of 40** receptors with zero
   mismatches — so the reconstructed map is what the corpus actually used.
   (The counting error is in C-B-14's prose, F-B-10, not in the file.)

**Constructs (SC-B-8).**

9. **Donor sequence census reproduces exactly**: 3 distinct shuffled donors,
   alphas × 33, alphai1 × 6, alpha13 × 1.
10. **Wrong-family check reproduces, including secondaries**: 0 of 40 shuffled
    donors fall inside `{cognate_class} ∪ {secondary_classes}`, verified against
    the `secondary` column of the build report's own assignment table, including
    all 13 promiscuous receptors.
11. **Cognate routing is internally consistent 40/40**, with the edge cases
    correct: OPSD → alphat (the only Gt), EDNRA → alphaq for the decoy parent
    even though its *shuffled* arm borrows G12.
12. **The build report and `donor_ga_class.csv` agree on the shuffled class for
    all 40 receptors**, and `donor_ga_class.csv` is internally consistent (640
    rows, 4 per receptor per arm, apo donor empty, decoy donors receptor-specific,
    cognate donor == cognate identity 40/40).
13. **Length-match, composition preservation and the prefix boundary all hold
    40/40**, and `cognate_len − prefix_len == 11` in every row, confirming the
    scramble boundary sits at N−11 and not N−10 or N−12.
14. **The `Gi_scaffold_scrambled`-style class labels read backwards but are not
    wrong.** `donor_ga_class` for decoy cells is `<class>_scaffold_scrambled`,
    which sounds like the scaffold was scrambled and the tail left alone — the
    opposite of the construction. The build report and the verification report
    both confirm the scaffold is byte-identical and only the α5-CT is permuted.
    Worth never quoting the raw label in a caption, but not a data defect.

**MSA audit (SC-B-7, SC-B-9).**

15. **`msa_depth_report.md` reproduces throughout.** All 40 decoy Δ and Δ% values
    are arithmetically consistent with their parent/decoy depths; the summary
    statistics reproduce (min −3.45 % HRH1, max +3.68 % DRD2, mean +0.40 %,
    median +0.65 %, sd 1.60 %); all 40 are inside ±5 %; the 48-receptor table has
    40 Class A + 4 Class B + 4 Class F, is genuinely sorted by depth, has
    `uniref90 + bfd + 1 query == total` on 48 of 48, and its minimum is CNR2 at
    1,996 with none below 1,000 as claimed. The 51 + 29 + 40 + 0 = 120
    unique-sequence census adds up.
16. **The Hamming column agrees across two independent documents** —
    `msa_depth_report.md` and `decoy_scramble_verification.md` give the same
    tail Hamming for all 40 receptors.
17. **The two duplicate decoy depths are coincidence, not a copy-paste.** AA2AR
    and LSHR both land at 12,227 (both Gs, parent 12,080) and B1B1U5 and HRH3
    both at 14,977 (both Gi, parent 14,986, both Δ = −9). Within-parent-group
    depths cluster tightly (sd ≈ 200 counts on 40 draws), so two exact ties are
    unremarkable; the underlying sequences and Hamming distances differ.
18. **The templates evidence itself is present and consistent** — 0/20 status
    JSONs with a `runtime_config` block, 0/20 with any template key. Only the
    `source_file` pointer is wrong (F-B-12).

**Ladder files.**

19. **`ladder_per_receptor.csv` is fully internally consistent**: 160 rows
    (40 × 4), all four `*_n` columns exactly 50, all three `delta_*` columns
    equal to the corresponding rate difference on 160 of 160 rows,
    `all_nan_np_arm` flagging exactly the four E-B-1 receptors.
20. **SC-B-1's ladder is aggregation-robust.** The mean of per-receptor rates on
    frame_36 gives 0.1579 / 0.5579 / 0.8094 / 0.8911, matching the pooled-row
    figures to <10⁻³. Whatever else is wrong in Block B, the headline ladder is
    not an artefact of how rows were pooled.
21. **W-B-2 is well supported by its own file** — 0 of 13 subsets reproduce the
    withdrawn midpoint ladder within 0.02.

**Covariates.**

22. **All six panel slopes reproduce exactly** by plain OLS on
    `ladder_height_covariates.csv`, and all six `n_receptors` values (28, 34, 32,
    40, 32, 40) reproduce as the non-NaN counts. The regression file is
    arithmetically sound; the problem is what the claim sheet selects from it.
23. **`n_ga_families` reproduces** as `1 + len(secondaries)` from the build
    report's assignment table on 40 of 40 receptors.
24. **`deposition_count` really is degenerate** — every one of the 40 receptors
    carries exactly 2, so std = 0 and the NaN slope is correct, as C-B-14 says.

**Figure brief.**

25. **`FIGURE_BRIEF.md` is clean.** Every one of the 13 named source CSVs exists
    and loads; every named filter column exists and every named filter value
    matches a non-zero number of rows, including the `panel_all` / `frame_36`
    pair on `interface_2x2.csv` and the `cutoff_A ∈ {10, 14, 20}` sweep (the file
    ships 10/12/14/16/18/20). All three columns BB-4 names for its groupby
    (`arm`, `cell_engaged_but_inactive`, `cell_active`) exist. The only slip is
    cosmetic: BB-6 says "per-receptor `family_term` values on both scales" where
    the columns are `family_term_continuous` and `family_term_logit`.
26. **All 27 row-count claims in `DATA_DICTIONARY.md` are correct.**

**My own false positive, recorded so nobody repeats it.**

27. I filtered `ladder_four_scorings.csv` on `backbone == "panel_all"` and got
    zero rows, and briefly had it as a missing-stratum finding. The file uses
    `panel`; `panel_all` is `interface_2x2.csv`'s vocabulary. The first-pass
    report warned about exactly this label and I walked into the mirror image of
    it. The finding that survives is F-B-5 — that the *dictionary* documents the
    wrong value — not that the stratum is missing.

---

## Summary table

| id | claim | severity | reaches reader |
|---|---|---|---|
| F-B-1 | SC-B-2 Protenix logit family CI "squarely positive" | high | yes |
| F-B-2 | SC-B-11 panel null averages two signed, opposite backbone slopes | high | yes |
| F-B-3 | SC-B-2 per-backbone logit family shares not in cited file | high | yes |
| F-B-4 | SC-B-11 logit rows are frame_40; promiscuity slope flips on frame_36 | med-high | yes |
| F-B-5 | dictionary documents `panel_all` where file has `panel` | medium | no (silent empty panel) |
| F-B-6 | dictionary names non-existent columns in 5 files | medium | no |
| F-B-7 | SC-B-8 prefix range 339–349 (actual 339–383); "9–11 residues" | medium | yes |
| F-B-8 | SC-B-9 "18/18 … 6×2×3"; OF3 inferred not verified | medium | yes |
| F-B-9 | threshold-band claim false on Chai (one receptor: OX2R) | medium | yes |
| F-B-10 | "26 paralog clusters" on frame_36 (24); C-B-14 15/11 (12/14) | medium | yes |
| F-B-11 | three `midpoint_ladder_28` labels contradict `n_receptors` | low-med | only via caption |
| F-B-12 | SC-B-7 sourced to a file with no templates evidence | low | no |
| F-B-13 | `ladder_threshold_proximity.csv` uses 9.082, rows use 9.08 | low | no |
| — | **correction**: D-B-1's "no ceiling-pinning flag" is wrong | — | — |
