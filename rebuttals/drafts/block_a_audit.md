# Block A audit — working draft for `rebuttals/BLOCK_A.md`

**Status**: draft. Sections 1–3 are the entries; section 4 ("checked and NOT a
finding") and section 5 ("where our own report is wrong") are draft-only and
must be stripped before this is sent upstream, per `rebuttals/README.md`.

Everything below was recomputed from `block_a_figure_data.zip` alone. Every
reproduction was executed before being written down.

## How to run the reproductions

Unzip the drop and `cd` into its root — the directory that contains `README.md`,
`01_rows/`, `02_references/` and so on. Every snippet below assumes that working
directory and needs only `python3` + `pandas`; the structure snippets need
`numpy` and nothing else (no `gemmi`, no PyMOL). Two snippets use a small
stdlib mmCIF reader given once in **Appendix A**; save it as `anchors_lib.py`
in the drop root before running those.

## Framing note, so the entries read correctly

Block A supplied **the whole cognate Gα subunit** as the co-input on the cognate
arm. It did not supply a 21-residue peptide. The cognate prediction CIFs confirm
this directly — `success_case/DRD2__cognate__of3__…row8285.cif` carries a
354-residue chain B beside the 443-residue receptor, and the ACM1 files carry a
359-residue chain B. The α5 C-terminal 21-mer is a rendering choice on our side
only. Where item 7 of our earlier `DATA_REQUESTS.md` asked for "the α5-CT 21-mer
coordinates as supplied to the model", that request was malformed; what we want
is the Gα chain as supplied.

---

# 1. The 23 groups already recorded in `analysis/block_a/DISCREPANCY_REPORT.md`

Ordering here follows the report's numbering, not severity. Severity ranking is
section 3.

---

## D1 — "all CIs cross zero" is false on the NPxxY amplitude regression

**1. Claim as shipped.** `10_narrative/BLOCK_A_CLAIM_SHEET.md`, §SC-3,
"Amplitude regression slopes (Class-A-only, cluster-boot)":

> "NPxxY-OH: 0.12 to 0.55 across backbones; all CIs cross zero; SD(Δref) =
> 4.71 Å well-powered; attenuation-robust."

**2. What the data says.** `04_amplitude/amplitude_fits.csv`, filter
`axis == "npxxy" & inclusion_set == "class_a_only"`. Protenix's cluster CI is
`[0.0738, 0.5517]` — it excludes zero. It also excludes zero on `baseline` and
on `class_a_no_holds`, so it is not an artefact of the inclusion choice. The
shipped `n_receptors` is 28, not 34, and `sd_predictor` is 5.222, not 4.71. For
this axis `baseline` and `class_a_only` are byte-identical, so no shipped
inclusion set yields n=34 / SD=4.71.

**3. Reproduction.**

```python
import pandas as pd
f = pd.read_csv('04_amplitude/amplitude_fits.csv')
n = f[(f.axis=='npxxy') & (f.inclusion_set=='class_a_only')]
print(n[['backbone','slope','cluster_ci_lo','cluster_ci_hi','n_receptors','sd_predictor']])
print('all CIs cross zero:', bool(((n.cluster_ci_lo<0)&(n.cluster_ci_hi>0)).all()))   # False
```

**4. Severity — high; reaches a reader.** This is the wording of a load-bearing
negative result. "All CIs cross zero" published as-is is a false statement about
a number in the same archive.

**5. What would close it.** Either the analysis that produced n=34 / SD=4.71
(it is not in the archive), or confirmation that the shipped fits supersede the
claim-sheet line so we reword to "three of four backbones show no evidence;
Protenix shows a weak signed positive slope of 0.26".

---

## D2 — the connector magnitude ratio cannot cross zero by construction

**1. Claim as shipped.** §SC-3, "Numbers (orthogonal signature, T2 scale-up
n=512)": magnitude ratio **0.37, CI [0.04, 0.77]**, presented beside
"Direction unanimous across all 4 backbones". Read together this asserts a
signed effect.

**2. What the data says.** `05_connector/connector_summary.csv`,
`scope == "pooled"`: `delta_pred_median = −0.5602`, `delta_cluster_ci =
[−1.1960, +0.0259]`, which contains zero. All four per-backbone CIs contain
zero too. `magnitude_ratio` is exactly `abs(delta_pred_median) /
abs(delta_ref_median)`, so its interval is a folded interval and cannot cross
zero whatever the underlying delta does.

**3. Reproduction.**

```python
import pandas as pd
c = pd.read_csv('05_connector/connector_summary.csv'); p = c[c.scope=='pooled'].iloc[0]
print(p.magnitude_ratio, abs(p.delta_pred_median)/abs(p.delta_ref_median))   # 0.370991 0.370991
print(p.delta_cluster_ci_lo < 0 < p.delta_cluster_ci_hi)                     # True
print(bool(((c.delta_cluster_ci_lo<0)&(c.delta_cluster_ci_hi>0)).all()))     # True — all scopes
```

**4. Severity — high; reaches a reader.** The strong part of this result is the
agreement counts (204/256 and 205/256, both of which reproduce exactly). The
ratio-with-CI framing converts a null-crossing delta into an apparently signed
one.

**5. What would close it.** Confirmation that the ratio CI is the folded
interval, so we report direction unanimity and the counts as the result and the
magnitude as "roughly one third of reference scale, interval includes zero".

---

## D3 — tilt slopes go negative, and the claim-sheet line mixes three inclusion sets

**1. Claim as shipped.** §SC-3: "Tilt: 0.03 to 0.50 across backbones; all CIs
cross zero; SD(Δref) = 1.19 Å"; and the same line elsewhere as "SD(Δ_tilt_ref)
= 1.19 Å across 40 Class A receptors".

**2. What the data says.** `04_amplitude/amplitude_fits.csv`, `axis == "tilt"`:

| inclusion_set | boltz | chai | of3 | protenix | n | sd_predictor |
|---|---:|---:|---:|---:|---:|---:|
| baseline | +0.445 | +0.081 | +0.107 | +0.611 | 39 | 2.169 |
| class_a_only | **−0.298** | **−0.659** | +0.233 | +0.082 | 32 | 1.171 |
| class_a_no_holds | **−0.319** | **−0.558** | +0.250 | +0.085 | 27 | 1.195 |

The claimed all-positive range resembles `baseline`; the claimed SD of 1.19
matches `class_a_no_holds` (1.195); the claimed n=40 matches none of the three.

**3. Reproduction.**

```python
import pandas as pd
f = pd.read_csv('04_amplitude/amplitude_fits.csv'); t = f[f.axis=='tilt']
print(t.pivot_table(index='inclusion_set', columns='backbone', values='slope').round(3))
print(t.groupby('inclusion_set')[['n_receptors','sd_predictor']].first().round(3))
```

**4. Severity — high; reaches a reader.** A negative amplitude slope is not
physically interpretable, and the claim-sheet line hides it by quoting across
sets.

**5. What would close it.** Name one inclusion set for the tilt amplitude
regression and quote n, SD and slopes consistently from it.

---

## D4 — narrative pLDDT values differ from `plddt_correlations.csv`

**1. Claim as shipped.** §SC-11 quotes per-backbone r values in a table; several
narrative documents in `10_narrative/` carry different values for the same
quantities (for example `of3` / `plddt_mean`).

**2. What the data says.** `06_confidence/plddt_correlations.csv` is internally
consistent, carries explicit `signed_at_cluster_boot` and `primary_or_secondary`
columns, and is the only place all three aggregations appear together. `of3` /
`plddt_mean` is −0.2579 there. The headline claim ("signed at cluster bootstrap
on the primary aggregation for 2 of 4 backbones") reproduces exactly.

**3. Reproduction.**

```python
import pandas as pd
p = pd.read_csv('06_confidence/plddt_correlations.csv')
print(p[['backbone','aggregation','pearson_r','cluster_ci_lo','cluster_ci_hi',
         'signed_at_cluster_boot','primary_or_secondary']].round(3).to_string(index=False))
print(int(p[p.primary_or_secondary=='primary'].signed_at_cluster_boot.sum()))   # 2
```

**4. Severity — medium; would reach a reader only through a mis-transcribed
number.** The CSV wins; the narrative should be regenerated from it.

**5. What would close it.** Confirmation that `plddt_correlations.csv` is the
source of truth and the narrative text is stale, so we quote only the CSV.

---

## D5 — SC-1's intervals are the receptor bootstrap under a "cluster-boot" heading

**1. Claim as shipped.** §SC-1 table header reads **"95% CI (cluster-boot)"**,
and the front matter states "Receptor-bootstrap CIs are ~1.10× tighter and are
NOT the reported primary measurement."

**2. What the data says.** `03_aggregates/headline_by_backbone.csv` carries both
bootstraps. Every quoted interval is nearer the receptor column, and boltz is an
exact match to it:

| backbone | quoted | cluster CI | receptor CI | |Δ| to cluster / receptor |
|---|---|---|---|---|
| boltz | [4.403, 5.502] | [3.528, 5.545] | **[4.403, 5.502]** | 0.918 / **0.000** |
| chai | [0.373, 3.452] | [0.358, 3.763] | [0.391, 3.452] | 0.326 / 0.018 |
| of3 | [4.072, 4.998] | [3.951, 5.215] | [4.333, 4.994] | 0.338 / 0.266 |
| protenix | [4.909, 5.603] | [4.633, 5.743] | [4.901, 5.679] | 0.416 / 0.084 |

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
q = {'boltz':(4.403,5.502),'chai':(0.373,3.452),'of3':(4.072,4.998),'protenix':(4.909,5.603)}
for b,(lo,hi) in q.items():
    r = h.loc[b]
    dc = abs(lo-r.median_tilt_shift_cluster_ci_lo)+abs(hi-r.median_tilt_shift_cluster_ci_hi)
    dr = abs(lo-r.median_tilt_shift_receptor_ci_lo)+abs(hi-r.median_tilt_shift_receptor_ci_hi)
    print(b, round(dc,3), round(dr,3), 'RECEPTOR' if dr<dc else 'cluster')
```

**4. Severity — high; reaches a reader.** These are the Table 1 intervals on the
headline result. As written they overstate precision under the label the Methods
declares authoritative. For boltz the true cluster lower bound is 0.88 Å below
the one quoted.

**5. What would close it.** Confirmation that the claim sheet was populated from
the `*_receptor_ci_*` columns, so we requote all four from `*_cluster_ci_*`.

---

## D6 — SC-2's fractions, denominator and stated range all drift

**1. Claim as shipped.** §SC-2: fractions 0.9456 / 0.8878 / 0.9152 / 0.9118,
heading "89–95%", denominator "n=38–39 receptors (sealed 8 dropped)".

**2. What the data says.** `03_aggregates/headline_by_backbone.csv`: 0.9472 /
0.8841 / 0.9340 / 0.9201, so the range is 0.884–0.947 and chai falls below the
claimed 89% floor; of3 differs by 0.0188. `n_receptors_fraction` is 40 on every
row (and see D15 — the effective n is 39).

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv')
print(h[['backbone','fraction_of_way_to_active','n_receptors_fraction']].round(4))
print(h.fraction_of_way_to_active.min(), h.fraction_of_way_to_active.max())   # 0.8841 0.9472
```

**4. Severity — medium; reaches a reader.** It is one table and one sentence,
but the claimed floor is wrong in the direction that flatters the result.

**5. What would close it.** Which version of the claim sheet the CSV was built
against, and confirmation that the CSV supersedes it.

---

## D7 — SC-6's heading false-positive rate is wrong by a factor of two

**1. Claim as shipped.** §SC-6 heading: "0.02% false-positive rate against
RMSD > 3 Å". Its own body says "only 2 (0.04%)".

**2. What the data says.** `01_rows/block_a_rows.csv`, filter `active == True`:
4,866 rows, 2 above 3 Å, i.e. 0.041%. Every per-backbone count and both >3 Å
rows reproduce exactly; only the heading is wrong.

**3. Reproduction.**

```python
import pandas as pd
a = pd.read_csv('01_rows/block_a_rows.csv').query('active')
print(len(a), int((a.rmsd_to_active_ref>3).sum()), 100*(a.rmsd_to_active_ref>3).sum()/len(a))
# 4866 2 0.0411
```

**4. Severity — low; would reach a reader only if the heading were quoted.**

**5. What would close it.** Correct the heading to 0.04% (2 of 4,866) — see
also D14 on the denominator.

---

## D8 — `matches_claim_sheet` is coarser than the precision the numbers are quoted at

**1. Claim as shipped.** `03_aggregates/headline_by_backbone.csv` carries
`matches_claim_sheet = True` on all four rows, and `README.md` §"Verification we
ran" describes the check as "median tilt shift + fraction-of-way-to-active
within 0.02 of claim".

**2. What the data says.** The flag is honest under its own documented
tolerance: the largest disagreement is of3's fraction at 0.0188, which is inside
0.02. But the fractions are quoted to four decimals in SC-2, so a flag with a
0.02 band certifies a number that is wrong at the precision it is published at.
The tolerance appears only in README prose, not in `DATA_DICTIONARY.md` and not
in the CSV.

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
cs = {'boltz':(5.036,0.9456),'chai':(1.047,0.8878),'of3':(4.814,0.9152),'protenix':(5.307,0.9118)}
for b,(t,f) in cs.items():
    r = h.loc[b]
    print(b, round(abs(r.median_tilt_shift-t),4), round(abs(r.fraction_of_way_to_active-f),4),
          r.matches_claim_sheet)
# of3 0.0002 0.0188 True   <- inside the documented 0.02, still a visible drift
```

**4. Severity — low as a data defect, medium as a process defect.** It does not
reach a reader directly, but it is the column that told us the fractions were
verified, and it is the reason D6 was not caught upstream.

**5. What would close it.** Put the tolerance in `DATA_DICTIONARY.md` and, if
possible, ship the per-quantity absolute difference beside the boolean rather
than the boolean alone.

---

## D9 — the reference-set denominator the Methods must state does not match the data

**1. Claim as shipped.** `10_narrative/caveats/C-6_manuscript_pdb_count.md` and
§C-6 assert "89 unique reference PDBs … 41 unique active-state references … 48
unique inactive-state"; `FIGURE_BRIEF.md` §BA-1 describes
`denominator_populations.csv` as the "89 / 167 / 127 denominators".

**2. What the data says.** `02_references/denominator_populations.csv` says 98 /
44 / 54 / 167 / 162 and records the disagreement in its own `used_for` column.
`reference_metadata.csv` has `is_panel == True` on exactly 98 PDBs (44 active,
54 inactive); `reference_predicates.csv` returns 99 rows for those 98 PDBs
(45 active / 54 inactive) because of the CRHR1/CRFR1 duplicate — see N17. The
T4 evaluable audit set is 162, not 127.

**3. Reproduction.**

```python
import pandas as pd
print(pd.read_csv('02_references/denominator_populations.csv')[['population','count','used_for']])
rm = pd.read_csv('02_references/reference_metadata.csv')
rp = pd.read_csv('02_references/reference_predicates.csv')
print(int(rm.is_panel.sum()), rm[rm.is_panel].state.value_counts().to_dict())   # 98 {'inactive':54,'active':44}
panel = set(rm[rm.is_panel].pdb_id)
print(len(rp[rp.pdb_id.isin(panel)]), rp[rp.pdb_id.isin(panel)].state.value_counts().to_dict())  # 99 {'inactive':54,'active':45}
```

**4. Severity — high; reaches a reader.** §7.1 makes stating this denominator a
Methods requirement, and three numbers (89 / 98 / 167) are in circulation for
it. The 127 → 162 change also moves the denominator of the "construct annotation
contradicts RCSB on 40% of evaluable PDBs" statement.

**5. What would close it.** A one-line ruling: is the manuscript's 89 a
deliberate "unique functional reference" count with a stated rule, or is it
stale? If deliberate, the rule; if stale, we state 98 and cite C-6 as the record.

---

## D10 — `deviation_class` has five levels, not the three the panel spec assumes

**1. Claim as shipped.** `FIGURE_BRIEF.md` §BA-1 and the brief's BA-1b spec:
shape every `deviation = True` point by `deviation_class`, described as
`{expected_biology, curation_error, measurement_artifact}`.

**2. What the data says.** `02_references/reference_predicates.csv` carries five
distinct values across the 9 deviations: `unclassified` (5),
`measurement_artifact` (1), `curation_error` (1), `expected_biology` (1),
`curation_error_or_expected_biology` (1). On the 48-receptor panel subset there
are 7 deviations, 3 of them `unclassified`. A three-shape encoding would drop or
mislabel two thirds of the points the panel exists to show.

**3. Reproduction.**

```python
import pandas as pd
rp = pd.read_csv('02_references/reference_predicates.csv')
rm = pd.read_csv('02_references/reference_metadata.csv')
print(rp[rp.deviation].deviation_class.value_counts().to_dict())
panel = set(rm[rm.is_panel].pdb_id)
print(rp[rp.deviation & rp.pdb_id.isin(panel)].deviation_class.value_counts().to_dict())
```

**4. Severity — medium; reaches a reader through the figure.**

**5. What would close it.** Either classify the 5 `unclassified` deviations, or
confirm they stay unclassified so the panel can show them with a neutral marker
and the caption can say 5 of 9 are unclassified.

---

## D11 — the brief's own rules conflict on where the fraction may appear

**1. Claim as shipped.** Brief §8.1: "Keep the fraction in Table 2, not in a
figure … The fraction goes in T2 only." Brief §6 requires T5 to sweep "every
statistic under every combination" and S-T2 to be the per-receptor dump.

**2. What the data says.** `08_exclusions/exclusion_sweep.csv` carries
`fraction_of_way_to_active` as one of its five metrics, and
`03_aggregates/receptor_summary.csv` carries `fraction_of_way_to_active` as a
column. Both requirements cannot be met literally.

**3. Reproduction.**

```python
import pandas as pd
print(sorted(pd.read_csv('08_exclusions/exclusion_sweep.csv').metric.unique()))
print('fraction_of_way_to_active' in pd.read_csv('03_aggregates/receptor_summary.csv').columns)
```

**4. Severity — low; a specification conflict, not a data defect.** Recorded so
the resolution is visible: we keep the column in all three tables with
supplementary footnotes, and obey the no-figure-panel and no-abstract halves of
§8.1 without exception.

**5. What would close it.** Confirmation that §8.1's intent is "no headline
reading outside T2", not "the column may not exist elsewhere".

---

## D12 — CRITICAL: the "confidently wrong" structure is confidently right

**1. Claim as shipped.** `11_structures/SELECTION.md` and
`11_structures/confidently_wrong/ALIGNMENT.md`: row 567 is the "maximally
confident, maximally mislocated within the panel" row, to be presented as a
worst-case illustration overlaid on 5G53.

**2. What the data says.** Row 567 is an **apo**-arm prediction. It sits 0.948 Å
from the *inactive* reference and 3.102 Å from the active one, and the predicate
calls it inactive — correctly. So does row 552, which is what SELECTION.md's
own stated rule ("top-quintile RMSD-to-active, highest pLDDT within") actually
selects: 0.857 Å from inactive, called inactive. Row 567 is instead simply the
highest-`plddt_mean` row in the entire cell, which is a different rule from the
one recorded. The 3.1 Å figure is distance from the state this row was never
meant to reach.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv')
c = r[(r.receptor=='AA2AR')&(r.backbone=='boltz')&(r.arm=='apo')]
top = c[c.rmsd_to_active_ref >= c.rmsd_to_active_ref.quantile(0.8)]
print('SELECTION.md rule picks row', int(top.loc[top.plddt_mean.idxmax()].row_id))   # 552
print(r[r.row_id.isin([552,567])][['row_id','arm','rmsd_to_active_ref',
      'rmsd_to_inactive_ref','plddt_at_anchors','active']].to_string(index=False))
print('highest plddt_mean in the whole cell:', int(c.loc[c.plddt_mean.idxmax()].row_id))  # 567
```

**4. Severity — critical; reaches a reader as a figure asserting the opposite of
what its data shows.** The directory name, the selection rule and the panel
specification all corroborate each other, which is why it survived; none was
checked against the row.

**5. What would close it.** A query over the full corpus for rows with high
`plddt_at_anchors` that are far from the reference **they were meant to reach**
(cognate far from active, or apo far from inactive), with coordinates for the
top case. If no such row exists above a sensible pLDDT threshold, say so — that
is a publishable result on its own and we will report it as one.

---

## D13 — `instrument_schematic/ALIGNMENT.md` names anchors that do not reproduce

**1. Claim as shipped.** `11_structures/instrument_schematic/ALIGNMENT.md`:
"2×46 tilt anchor Cα (~L124 ADRB2)", "6×37 tilt anchor Cα (~F282 ADRB2)", and
under "Measured values (from reference_predicates.csv)": "Δ tilt … ≈ 5.02 Å",
"Δ NPxxY-OH … ≈ 5.4 Å". The file ships 3SN6 as the active β2AR reference.

**2. What the data says.** On the shipped `2RH1.cif`, L124–F282 Cα is 9.032 Å.
The pair that reproduces the shipped `d_tilt_ref` of 11.9283 Å exactly is
**L75/L275**. The NPxxY anchors (Y219/Y326) are correct — they give 11.4727 Å,
matching `d_npxxy_oh_ref`. Neither stated Δ appears in
`reference_predicates.csv` or `reference_separation.csv`: ADRB2 ships
`delta_tilt_ref = +5.634` and `delta_npxxy_ref = −6.581` (note the sign). And
**3SN6 is not in the reference set at all** — ADRB2's panel active reference is
4LDE.

**3. Reproduction.** (needs `anchors_lib.py`, Appendix A)

```python
from anchors_lib import atoms, dist
import pandas as pd
A = atoms('11_structures/instrument_schematic/2RH1.cif')
print('L124-F282 %.4f' % dist(A,'A',124,282))      # 9.0317
print('L75-L275  %.4f' % dist(A,'A',75,275))       # 11.9283  == shipped d_tilt_ref
O = atoms('11_structures/instrument_schematic/2RH1.cif','OH')
print('Y219-Y326 %.4f' % dist(O,'A',219,326))      # 11.4727  == shipped d_npxxy_oh_ref
rp = pd.read_csv('02_references/reference_predicates.csv')
print('3SN6 in reference_predicates:', '3SN6' in set(rp.pdb_id))   # False
```

**4. Severity — high; reaches a reader through any render that prints distances
onto a structure.**

**5. What would close it.** Regenerate the ALIGNMENT files from the same anchor
table the scorer uses, or ship that table. See also N13/N14 — the problem is
larger than this one file.

---

## D14 — 610 predicate-active rows have no active reference and cannot be tested

**1. Claim as shipped.** §SC-6: "Across 4,866 predicate-active rows on the
9,490-row corpus, only 2 (0.04%) land more than 3 Å from the active reference."

**2. What the data says.** Only 4,256 of those 4,866 rows carry a non-null
`rmsd_to_active_ref`; the other 610 have no active reference to be scored
against and cannot fail. The testable rate is 2 / 4,256 = 0.047%. The 610 come
from the eight sealed receptors (ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3,
OX2R), for which `delta_to_active`, `rmsd_to_active_ref` and
`rmsd_to_inactive_ref` are null on all 1,600 rows.

**3. Reproduction.**

```python
import pandas as pd
a = pd.read_csv('01_rows/block_a_rows.csv').query('active')
tst = int(a.rmsd_to_active_ref.notna().sum())
print(len(a), tst, len(a)-tst, 100*(a.rmsd_to_active_ref>3).sum()/tst)
# 4866 4256 610 0.04699
```

**4. Severity — medium; reaches a reader as a diluted rate.** Rows that cannot
fail should not sit in the denominator of a false-positive rate.

**5. What would close it.** Active-state PDBs for the eight sealed receptors if
any have been deposited since the reference freeze, or an explicit statement
that none exists as of a stated date. The second answer is nearly as good as the
first — it converts a gap into a documented boundary.

---

## D15 — the `n_receptors_*` columns overstate the effective n

**1. Claim as shipped.** `03_aggregates/headline_by_backbone.csv` reports
`n_receptors_tilt = 48`, `n_receptors_delta = 48`, `n_receptors_fraction = 40`
on every row; §SC-2 states "n=38–39 receptors".

**2. What the data says.** Counting distinct receptors with a non-null value in
`03_aggregates/receptor_summary.csv` gives 47, 39 and 39 respectively. The
headline fraction is a median over 39 receptors, not 40 and not 38.

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv')
rs = pd.read_csv('03_aggregates/receptor_summary.csv')
for hc, rc in [('n_receptors_tilt','delta_cognate_minus_apo_tilt'),
               ('n_receptors_delta','delta_cognate_minus_apo_delta_to_active'),
               ('n_receptors_fraction','fraction_of_way_to_active')]:
    print(hc, h[hc].max(), '->', rs[rs[rc].notna()].receptor.nunique())
# n_receptors_tilt 48 -> 47 ; n_receptors_delta 48 -> 39 ; n_receptors_fraction 40 -> 39
```

**4. Severity — medium; reaches a reader as an inflated n.**

**5. What would close it.** Confirm the intended definition — "receptors in the
panel" or "receptors contributing a value" — and repopulate with the latter.
The identity of the missing receptors is now known: see N7.

---

## D16 — `plddt_correlations.csv` misreports its receptor count

**1. Claim as shipped.** All 12 rows of `06_confidence/plddt_correlations.csv`
carry `n_receptors = 40`.

**2. What the data says.** `06_confidence/plddt_per_receptor.csv` carries 32
distinct receptors for every backbone × aggregation. `n_rows` (~1,600) is
consistent with a 32-receptor Class A subset; only the receptor count is wrong.

**3. Reproduction.**

```python
import pandas as pd
print(sorted(pd.read_csv('06_confidence/plddt_correlations.csv').n_receptors.unique()))  # [40]
print(pd.read_csv('06_confidence/plddt_per_receptor.csv').receptor.nunique())            # 32
```

**4. Severity — low to medium; reaches a reader through Table T4's n.**

**5. What would close it.** Repopulate `n_receptors` from the same population
the r values were computed on.

---

## D17 — "receptor bootstrap ~1.10× tighter" holds on 2 of 12 statistics

**1. Claim as shipped.** `README.md` §"The four numbers a figure agent will get
wrong", item 3, and the claim sheet's bootstrap convention: "Receptor-bootstrap
CIs … are ~1.10× tighter and mildly overstate precision."

**2. What the data says.** Cluster/receptor CI width ratios across the headline
statistics run 1.00 to 2.20:

| statistic | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| median tilt shift | 1.84 | 1.11 | 1.91 | 1.43 |
| median Δ-to-active shift | 1.00 | 1.00 | 1.07 | 2.20 |
| fraction | 1.00 | 1.72 | 1.04 | 1.37 |

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
for s in ['median_tilt_shift','median_delta_to_active_shift','fraction']:
    w = lambda k: h[f'{s}_{k}_ci_hi'] - h[f'{s}_{k}_ci_lo']
    print(s, (w('cluster')/w('receptor')).round(2).to_dict())
```

**4. Severity — medium.** It strengthens rather than weakens the case for the
cluster bootstrap being authoritative, but it makes D5 (receptor intervals
quoted under a cluster label) a much larger error than a 10% one.

**5. What would close it.** Replace "~1.10× tighter" with "equal to or wider by
up to a factor of 2.2", or the derivation that produced 1.10.

---

## D18 — CRITICAL: a shipped structure is the wrong protein entirely

**1. Claim as shipped.** `README.md` §"Structure subdirectories":
"`agonist_only_vs_ternary/` — OPRD 6PT2 (agonist-only) + δOR-Gi 8FZQ";
`11_structures/agonist_only_vs_ternary/ALIGNMENT.md`: "`8FZQ.cif` — 8FZQ
(δOR–Gi complex)".

**2. What the data says.** The file's own `_struct.title` reads
'Dehosphorylated, ATP-bound human cystic fibrosis transmembrane conductance
regulator (CFTR)'. One chain, ~1,152 Cα, ATP and Mg bound. It is an ABC
transporter, not a GPCR. The companion 6PT2 is correct.

**3. Reproduction.**

```bash
grep -A1 '_struct.title' 11_structures/agonist_only_vs_ternary/8FZQ.cif
grep -A2 '_struct.title' 11_structures/agonist_only_vs_ternary/6PT2.cif
```

**4. Severity — critical; blocks the most on-thesis structural comparison in the
drop.** This directory is the visual form of the finding that agonist-bound
structures without a transducer do not form the NPxxY network. The render cannot
be built. Every other CIF in the drop was checked against its own title and is
what it claims to be.

**5. What would close it.** The correct δOR–Gi ternary coordinates. Flag 7 in
`MANUSCRIPT_FLAGS.md` already says the identification was deferred and is
"likely one of Wang et al. 2023 Cell's 8F7* series" — that transposition is the
most probable origin of the 8FZQ fetch.

---

## D19 — templates-off and MSA configuration have no row-level evidence

**1. Claim as shipped.** §SC-9: "Templates off across all four backbones.
Evidence: launcher static analysis + source-code defaults + propagation test PASS
5/5", qualified by "no row-level echo (evidence class b + c + d, not a);
`_status.json.runtime_config` echo landed post-Block-A."

**2. What the data says.** `01_rows/block_a_rows.csv` has no column recording
template usage or MSA configuration — none of its 55 columns. For MSAs there is
no claim in the drop at all, and nothing records the setting.

**3. Reproduction.**

```python
import pandas as pd
c = list(pd.read_csv('01_rows/block_a_rows.csv', nrows=1).columns)
print(len(c), [x for x in c if any(k in x.lower() for k in ('templ','msa','a3m','align'))])
# 55 []
```

**4. Severity — high, because templates-off is load-bearing.** An active-state
template would be an oracle route, and the whole design depends on its absence.
SC-9 is candid about the evidence class; we are flagging it because the
manuscript has to state it, not because the drop hid it.

**5. What would close it.** If `_status.json` still exists for these runs,
back-attaching `runtime_config` per row converts this from a disclosed
evidence-class caveat into a row-level fact. Separately: were MSAs pinned, and
if so to what?

---

## D20 — two further `ALIGNMENT.md` files name wrong NPxxY anchors

**1. Claim as shipped.** `11_structures/broken_cell/ALIGNMENT.md`: "ACM1
numbering … Y5.58 ≈ Y213, Y7.53 ≈ Y418". `11_structures/success_case/
ALIGNMENT.md`: "DRD2 numbering … Y5.58 ≈ Y208, Y7.53 ≈ Y399".

**2. What the data says.** On the shipped prediction CIFs, the OH–OH pair that
reproduces the row's `d_npxxy_oh` exactly is **Y208/Y418** for ACM1 (not Y213)
and **Y209/Y426** for DRD2 (not Y208/Y399). ACM1's tilt anchors are L67/L367,
which the file does not name at all. The coordinates and the tidy tables agree
perfectly; it is only the ALIGNMENT text that is wrong.

**3. Reproduction.**

```python
from anchors_lib import atoms, find
b = '11_structures/broken_cell/ACM1__cognate__chai__seed966761149__row948__HEALTHY.cif'
print(find(atoms(b,'OH'),'A', 4.015519))   # [('TYR',208,'TYR',418, 4.0155)]  row 948 d_npxxy_oh
print(find(atoms(b),      'A',17.166073))  # [('LEU', 67,'LEU',367,17.1661)]  row 948 d_tilt
d = '11_structures/success_case/DRD2__cognate__of3__seed849213874__row8285.cif'
print(find(atoms(d,'OH'),'A', 3.988277))   # [('TYR',209,'TYR',426, 3.9883)]  row 8285
```

**4. Severity — high; reaches a reader through any labelled render.**

**5. What would close it.** Same as D13 — ship the scorer's anchor table, or
regenerate the ALIGNMENT files from it.

---

## D21 — ADRB2's ΔNPxxY is measured against a different reference than the render assumes

**1. Claim as shipped.** `instrument_schematic/ALIGNMENT.md` pairs 3SN6/2RH1 and
quotes measured Δ values as though they belong to that pair.

**2. What the data says.** ADRB2 has three inactive references (2RH1, 3NYA,
6PS2). `reference_separation.csv` takes a **per-axis median** over them: for
tilt the median lands on 2RH1 (17.5625 − 11.9283 = +5.6342), for NPxxY it lands
on **3NYA** (4.8131 − 11.3943 = −6.5812). The pairwise 4LDE−2RH1 NPxxY value is
−6.6596. So printing −6.581 on a 4LDE/2RH1 render attaches a number to a pair it
was not measured on. Related practical trap: 4LDE carries a **+1000 auth
numbering offset** (chain A runs 858–1342) and 2RH1's T4L fusion occupies
1002–1161, so a single selection string across both objects aligns the receptor
onto the lysozyme.

**3. Reproduction.**

```python
import pandas as pd
rp = pd.read_csv('02_references/reference_predicates.csv'); a = rp[rp.receptor=='ADRB2']
act, ina = a[a.state=='active'], a[a.state=='inactive']
print(act.d_tilt_ref.median()-ina.d_tilt_ref.median())            # 5.6342  (median inactive = 2RH1)
print(act.d_npxxy_oh_ref.median()-ina.d_npxxy_oh_ref.median())    # -6.5812 (median inactive = 3NYA)
print(4.813055-11.472679)                                         # -6.6596 pairwise 4LDE-2RH1
```

**4. Severity — medium; reaches a reader as a number printed on the wrong pair.**

**5. What would close it.** State in the data dictionary that
`delta_*_ref` are per-axis medians over all inactive references for the
receptor, and give the per-pair values if the render is to carry one.

---

## D22 — `rmsd_to_active_ref` does not reproduce from the shipped coordinates

**1. Claim as shipped.** `11_structures/success_case/ALIGNMENT.md` and
`01_rows/block_a_rows.csv`: row 8285 (DRD2 / OpenFold3 / cognate) ships
`rmsd_to_active_ref = 1.218 Å`.

**2. What the data says.** Kabsch superposition over all 269 shared receptor Cα
against 7JVR chain R gives **1.2952 Å**. No simple window reproduces 1.218: the
closest trim over a scan of N- and C-terminal boundaries is 38–429 at 1.2456 Å;
7TM-only (34–225) gives 0.8532 Å; the C-terminal half alone gives 1.8040 Å. The
scorer's atom set is documented nowhere in the drop.

**3. Reproduction.** (needs `anchors_lib.py` + numpy; see Appendix A)

```python
import numpy as np
from anchors_lib import atoms
A = {k[1]: np.array(v[1:]) for k,v in atoms(
     '11_structures/success_case/DRD2__cognate__of3__seed849213874__row8285.cif').items() if k[0]=='A'}
B = {k[1]: np.array(v[1:]) for k,v in atoms('11_structures/success_case/7JVR.cif').items() if k[0]=='R'}
def rms(keys):
    X = np.array([A[i] for i in keys]); Y = np.array([B[i] for i in keys])
    X, Y = X-X.mean(0), Y-Y.mean(0)
    U,S,Vt = np.linalg.svd(X.T@Y); R = U@np.diag([1,1,np.sign(np.linalg.det(U@Vt))])@Vt
    return np.sqrt((((X@R)-Y)**2).sum()/len(keys))
sh = sorted(set(A)&set(B))
print(len(sh), round(rms(sh),4))                                    # 269 1.2952 (shipped 1.218)
for lo,hi in [(38,429),(34,225),(366,441)]:
    k=[i for i in sh if lo<=i<=hi]; print(lo,hi,len(k),round(rms(k),4))
```

**4. Severity — medium as a number, high as a reproducibility claim.** Nothing
in the manuscript turns on this value, but a shipped RMSD that cannot be
recomputed from the shipped coordinates undercuts the archive's own
reproducibility premise. Figures that quote it now print the independently
computed value beside it and label both.

**5. What would close it.** The atom selection used by the scorer for
`rmsd_to_active_ref` and `rmsd_to_inactive_ref` — which chains, which residue
window, Cα or all-atom, and whether the superposition set equals the scored set.
One line of Methods, no compute.

---

## D23 — `*_active_rate_panel_mean` is a pooled rate, not a panel mean

**1. Claim as shipped.** `03_aggregates/headline_by_backbone.csv` columns
`apo_active_rate_panel_mean`, `cognate_active_rate_panel_mean`,
`npxxy_active_rate_panel_mean`, `tilt_active_rate_panel_mean`. The name says
*mean*, over the *panel*.

**2. What the data says.** Every one of the eight apo/cognate values equals the
**pooled row-level rate** over all rows and all classes using the class-aware
`active` predicate. For boltz apo the pooled rate is 0.15983 (shipped 0.15983)
while the unweighted mean over receptors is 0.15917. The two differ whenever
cells differ in size; a pooled rate weights every prediction equally, a panel
mean weights every receptor equally.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv')
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
pooled = r.groupby(['backbone','arm']).active.mean().unstack()
permean = r.groupby(['backbone','arm','receptor']).active.mean().groupby(['backbone','arm']).mean().unstack()
for b in h.index:
    print(b, round(h.loc[b,'apo_active_rate_panel_mean'],5),
          round(pooled.loc[b,'apo'],5), round(permean.loc[b,'apo'],5))
# boltz 0.15983 0.15983 0.15917  -> shipped == pooled, not the receptor mean
```

**4. Severity — medium; reaches a reader through a mis-stated statistic name.**

**5. What would close it.** Rename the columns to `*_active_rate_pooled`, or add
the genuine unweighted panel mean beside them. The manuscript currently
describes these as "pooled row-level rates", which is correct.

---

# 2. New findings

Numbered N1… to keep them distinct from the D-series. Each was recomputed and
each reproduction was executed.

---

## N1 — the "invariant to every exclusion set (≤ 0.5%)" claim is contradicted by the drop's own sweep

**1. Claim as shipped.** Claim sheet front matter §B: "The fraction-of-way-to-
active shifts by ≤ 0.5% under every single combination." §SC-1: "this shift is
invariant to every specified exclusion set (≤ 0.5% under any exclusion)". §SC-2:
"invariant to every specified exclusion set (≤ 0.5% shift under any combination
of E1–E5)."

**2. What the data says.** `08_exclusions/exclusion_sweep.csv`, all non-baseline
rows. `median_tilt_shift` exceeds 0.5% on **14 of 28** combinations, with a
maximum of **222.0%** (chai, `all_E1-E5`, 1.047 → 3.373).
`fraction_of_way_to_active` exceeds 0.5% on **6 of 28**, maximum **3.26%** (chai,
`all_E1-E5`, 0.8841 → 0.9130). SC-1's own table already contradicts SC-1's
sentence — it records chai going 1.047 → 2.03 under E4.

Separately, the sweep does not cover what §B says it covers. The
`exclusion_set` column holds only `baseline, E1, E2, E4, E1+E2, E1+E2+E4,
E1+E2+E4+E5, all_E1-E5`. **E3 and E5 are never applied singly, and E3 appears in
no combination except `all_E1-E5`** — and E3 alone removes 51.5% of the corpus.
"Applied the five pre-specified exclusion sets … singly and in every material
combination" is not what shipped.

**3. Reproduction.**

```python
import pandas as pd
s = pd.read_csv('08_exclusions/exclusion_sweep.csv'); x = s[s.exclusion_set!='baseline']
for m in ['median_tilt_shift','fraction_of_way_to_active']:
    d = x[x.metric==m]
    print(m, int((d.pct_shift_from_baseline.abs()>0.5).sum()), 'of', len(d),
          'max', round(d.pct_shift_from_baseline.abs().max(),2))
# median_tilt_shift 14 of 28 max 222.04 ; fraction_of_way_to_active 6 of 28 max 3.26
print(sorted(s.exclusion_set.unique()))   # no 'E3', no 'E5', no 'E3+...' pairs
```

**4. Severity — high; reaches a reader.** This is the robustness sentence that
§3 of the brief calls "what makes the exclusions defensible rather than
convenient". It is the single most quotable claim in the sheet and it is false
against the file shipped to support it.

**5. What would close it.** Either a corrected statement of the actual maximum
shift per metric, or a sweep that includes E3 and E5 singly and in pairs. If the
≤0.5% figure came from a restricted metric set (say, only the two headline
medians on Class A), say which — that would make it recoverable rather than
wrong.

---

## N2 — `excl_any` removes 53.7% of the corpus, and the README never says so

**1. Claim as shipped.** `README.md` §"Row counts (spot check)" lists "E1 fires:
25", "E2 fires: 4", "E1 ∪ E2: 29", then class counts. §"Exclusion flag
semantics" says "These are flags, never applied."

**2. What the data says.** `excl_E3` fires on **4,890 rows (51.5%)** and
`excl_any` on **5,093 rows (53.7%)**. A downstream agent who reads the spot-check
list, sees 25 / 4 / 29, and then applies `excl_any` as "the exclusions" silently
loses more than half the corpus. Every exclusion flag is internally consistent
with its stated rule — this is a documentation gap, not a flag bug.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv')
for c in ['excl_E1','excl_E2','excl_E3','excl_E4','excl_E5','excl_any']:
    print(c, int(r[c].sum()), round(100*r[c].mean(),2))
# excl_E3 4890 51.53 ; excl_any 5093 53.67
```

**4. Severity — medium; reaches a reader only through a figure built on the
wrong filter, but that is exactly the failure mode a spot-check list is meant to
prevent.**

**5. What would close it.** Add `excl_E3`, `excl_E4`, `excl_E5` and `excl_any`
row counts to the README spot-check block, with a line saying `excl_any` is not
the intended default filter for any headline number.

---

## N3 — four Class A receptors cannot produce a predicate-active call by construction

**1. Claim as shipped.** `01_rows/block_a_rows_dictionary.csv` documents
`npxxy_active` as "False on NaN axis" and `active` as "never null … A = npxxy
AND tilt". §SC-4 reports Class A two-instrument agreement on that basis; §SC-6
uses `active` for its 4,866-row denominator. `DATA_DICTIONARY.md`
§"Missing-data conventions" states "Never use `-999`, `0.0`, or any other
sentinel for missing."

**2. What the data says.** 2,295 rows have a null `d_npxxy_oh` and
`npxxy_active = False` on every one of them. 800 of those are **Class A**:
EDNRA, EDNRB, GRPR and HRH3, 200 rows each. Because Class A's `active` is
`npxxy AND tilt`, those four receptors return `active = False` on 100% of their
rows — while `tilt_active` fires on 36%, 35%, 50% and 62.5% of them
respectively. They remain in every Class A denominator: including them, Class A
two-instrument agreement is 86.87%; excluding them it is 90.51%. The column-level
convention is documented; this consequence is not documented anywhere, and it
converts "not measured" into "not active" rather than into missing.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv'); m = r.d_npxxy_oh.isna()
print(int(m.sum()), r[m].npxxy_active.unique().tolist())            # 2295 [False]
A = r[(r.gpcr_class=='A') & m]
print(sorted(A.receptor.unique()))                                  # EDNRA EDNRB GRPR HRH3
print(r[r.receptor.isin(A.receptor.unique())].groupby('receptor')
        .agg(rows=('active','size'), active_rows=('active','sum'), tilt_rate=('tilt_active','mean')))
cA = r[r.gpcr_class=='A']
print(round(100*(cA.npxxy_active==cA.tilt_active).mean(),2),
      round(100*(cA[~m.loc[cA.index]].npxxy_active==cA[~m.loc[cA.index]].tilt_active).mean(),2))
# 86.87 90.51
```

**4. Severity — high; reaches a reader.** It deflates every Class A predicate
rate and every Class A agreement statistic by a fixed amount, invisibly. Four of
forty Class A receptors — 10% of the panel — are structurally incapable of the
positive call the paper is about.

**5. What would close it.** Why is `d_npxxy_oh` null for these four? If the
NPxxY anchors are undefined for them, they should be excluded from Class A
denominators (or `npxxy_active` should be null, not False) and the count stated.
If it is a measurement gap, the measurement.

---

## N4 — SC-11's confidence intervals are the receptor bootstrap under a cluster-boot label

**1. Claim as shipped.** §SC-11 table, "Numbers (Pearson r, cluster-boot)":
boltz −0.221 [−0.357, −0.092]; chai −0.160 [−0.462, +0.144]; of3 −0.626
[−0.827, −0.601]; protenix +0.068 [−0.159, +0.276]. The prose calls OF3's
"the strongest signal in the campaign".

**2. What the data says.** All four quoted intervals are nearer the
`receptor_ci_*` columns of `06_confidence/plddt_correlations.csv` than the
`cluster_ci_*` columns — the same failure as D5, in a different claim. And OF3's
reproduces from **neither**: the shipped cluster CI is [−0.741, −0.475] and the
receptor CI is [−0.744, −0.495], against a quoted [−0.827, −0.601]. The quoted
interval asserts |r| ≥ 0.601 where the authoritative interval allows |r| as low
as 0.475.

**3. Reproduction.**

```python
import pandas as pd
p = pd.read_csv('06_confidence/plddt_correlations.csv')
p = p[p.aggregation=='plddt_at_anchors'].set_index('backbone')
q = {'boltz':(-0.357,-0.092),'chai':(-0.462,0.144),'of3':(-0.827,-0.601),'protenix':(-0.159,0.276)}
for b,(lo,hi) in q.items():
    r = p.loc[b]
    dc = abs(lo-r.cluster_ci_lo)+abs(hi-r.cluster_ci_hi)
    dr = abs(lo-r.receptor_ci_lo)+abs(hi-r.receptor_ci_hi)
    print(b, round(dc,3), round(dr,3), 'RECEPTOR' if dr<dc else 'cluster')
# every backbone -> RECEPTOR ; of3 dc=0.212 dr=0.189, i.e. neither
```

**4. Severity — high; reaches a reader.** OF3's correlation is the headline of
Beat 5 and its published interval would be materially tighter than the data
supports.

**5. What would close it.** The provenance of the four SC-11 intervals, and in
particular where [−0.827, −0.601] came from — no shipped column produces it.

---

## N5 — SC-2's fraction CIs reproduce from no shipped column, and one cluster CI exceeds 100%

**1. Claim as shipped.** §SC-2, "95% CI (cluster-boot)": boltz [0.892, 0.983],
chai [0.744, 0.959], of3 [0.861, 0.993], protenix [0.897, 0.978].

**2. What the data says.** None matches either shipped column to the precision
quoted. The smallest total discrepancy is protenix against the *receptor* column
(0.0058); chai's quoted lower bound of 0.744 is 0.147 above the shipped cluster
lower bound of 0.5967. Three of four lean receptor, so this is probably D5's
failure again plus rounding, but it is not recoverable as stated. Separately,
of3's shipped `fraction_cluster_ci_hi` is **1.0022** — a "fraction of the way to
the active reference" interval whose upper bound exceeds 100%.

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
q = {'boltz':(0.892,0.983),'chai':(0.744,0.959),'of3':(0.861,0.993),'protenix':(0.897,0.978)}
for b,(lo,hi) in q.items():
    r = h.loc[b]
    print(b, round(abs(lo-r.fraction_cluster_ci_lo)+abs(hi-r.fraction_cluster_ci_hi),4),
             round(abs(lo-r.fraction_receptor_ci_lo)+abs(hi-r.fraction_receptor_ci_hi),4))
print(h.loc['of3','fraction_cluster_ci_hi'])   # 1.0022
```

**4. Severity — medium; reaches a reader as a Table 2 interval.**

**5. What would close it.** Same question as D5 and N4: which column populated
the claim sheet. And whether the fraction is intended to be bounded at 1 — see
N6.

---

## N6 — `fraction_of_way_to_active` is unbounded and unstable at small denominators

**1. Claim as shipped.** §SC-2: "Predictions reach 89–95% of the way to the
active reference", presented as a percentage. `README.md` item 1 describes it as
"a *mean position along* delta_to_active (state reached)".

**2. What the data says.** In `03_aggregates/receptor_summary.csv` the column is
a ratio `fraction_numerator / fraction_denominator` with no bound. Of the 156
receptor × backbone cells that carry a value, **48 exceed 1**, **5 are
negative**, the maximum is **212.27** (GLP1R / of3, denominator −0.0050 Å) and
the minimum is −1.31. Seven cells have |denominator| < 0.5 Å, and those are
exactly the extreme values (AGTR1 2.60, CNR1 4.83, CRHR1 2.41, GLP1R 212.27,
PTH1R 2.09 and −0.71). OPRD sits at 4.6–5.7 on all four backbones. The
per-backbone headline is a median, which is why it looks well behaved, but any
per-receptor panel of this column is unplottable on a percentage axis.

**3. Reproduction.**

```python
import pandas as pd
d = pd.read_csv('03_aggregates/receptor_summary.csv').dropna(subset=['fraction_of_way_to_active'])
print(len(d), int((d.fraction_of_way_to_active>1).sum()), int((d.fraction_of_way_to_active<0).sum()),
      round(d.fraction_of_way_to_active.max(),2), round(d.fraction_of_way_to_active.min(),2))
# 156 48 5 212.27 -1.31
print(d[d.fraction_denominator.abs()<0.5][['receptor','backbone','fraction_denominator',
      'fraction_numerator','fraction_of_way_to_active']].round(4).to_string(index=False))
```

**4. Severity — high; reaches a reader.** A number presented as "89–95% of the
way" is a median over a quantity that runs to 212× and goes negative. That is a
defensible summary statistic only if the distribution is disclosed, and the
paper cannot show the distribution without explaining the tail.

**5. What would close it.** Is the ratio intended to be clipped or is the
unbounded form deliberate? And is `fraction_denominator` allowed to be near zero
(the apo prediction already at the active reference), or should those receptors
be dropped from the median?

---

## N7 — the fraction's 39 receptors are not the Class A panel

**1. Claim as shipped.** §SC-2: "n=38–39 receptors (sealed 8 dropped)", quoted
next to a result the paper frames as Class A. §SC-10: "Block A ran 48 receptors
(40 Class A + 4 Class B + 4 Class F)".

**2. What the data says.** The 39 receptors carrying a fraction are **32 Class A
plus 7 Class B/F** (CRHR1, FZD6, FZD7, GCGR, GLP1R, PTH1R, SMO). The 9 without
are the 8 sealed receptors — all Class A — plus **FZD4**, which has **no cognate
arm at all**: it ships 100 apo rows and zero cognate rows, which is why
`cell_summary.csv` has 380 cells instead of 48 × 4 × 2 = 384. So the headline
fraction pools Class A with Class B/F, and E4 (Class B/F) moves it by up to
1.58% — see N1.

This also answers the open question of which receptor `n_receptors_fraction = 40`
counts but `receptor_summary.csv` lacks: 40 is 48 minus the sealed 8, and the
missing one is FZD4.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv'); rs = pd.read_csv('03_aggregates/receptor_summary.csv')
have = set(rs[rs.fraction_of_way_to_active.notna()].receptor); cls = r.groupby('receptor').gpcr_class.first()
print(len(have), sum(cls[x]=='A' for x in have), sorted(x for x in have if cls[x]!='A'))
# 39 32 ['CRHR1','FZD6','FZD7','GCGR','GLP1R','PTH1R','SMO']
print(sorted(set(r.receptor)-have))
print({k:sorted(v) for k,v in r.groupby('receptor').arm.agg(set).items() if v!={'apo','cognate'}})
# {'FZD4': ['apo']}
print(len(pd.read_csv('03_aggregates/cell_summary.csv')))   # 380
```

**4. Severity — medium; reaches a reader as a scope error.** The paper is
positioned as a Class A result; the headline fraction is not a Class A number.

**5. What would close it.** Was FZD4's cognate arm intended to run? And should
the headline fraction be recomputed Class-A-only (32 receptors), with the
48-receptor version as the supplementary?

---

## N8 — SC-4's Class A agreement, κ and n reproduce from no subset of the shipped rows

**1. Claim as shipped.** §SC-4: "Two-instrument predicate agrees at 89.9%
[85.6, 93.4] on the Class A derivation panel (κ = 0.79, substantial) … Class A
n=32 deriv panel"; per-backbone boltz 90.23%, chai 93.40%, of3 83.67%,
protenix 92.40%. `README.md` already lists this under "What was not verified
end-to-end".

**2. What the data says.** No defensible Class A subset returns those five
numbers. Seven candidates, all recomputed as `npxxy_active == tilt_active`:

| subset | receptors | overall | κ | boltz / chai / of3 / protenix |
|---|---:|---:|---:|---|
| Class A, all | 40 | 86.87 | 0.737 | 87.12 / 90.90 / 81.30 / 88.15 |
| Class A, NPxxY measured | 36 | 90.51 | 0.807 | 91.20 / 94.11 / 84.33 / 92.39 |
| Class A amplitude panel | 32 | 87.91 | 0.756 | 87.77 / 92.19 / 81.94 / 89.75 |
| Class A NPxxY panel | 28 | 89.85 | 0.795 | 89.53 / 93.07 / 84.71 / 92.07 |
| Class A `no_holds` | 27 | 89.26 | 0.783 | 88.96 / 93.56 / 83.11 / 91.41 |
| Class A minus E1,E2 | 40 | 87.12 | 0.742 | 87.12 / 90.90 / 81.28 / 89.21 |
| Class A minus E3 | 23 | 91.76 | 0.833 | 92.61 / 95.04 / 85.65 / 93.74 |
| Class A minus E5 | 38 | 86.66 | 0.733 | 87.02 / 90.42 / 81.21 / 88.00 |

The closest overall is the 28-receptor NPxxY-valid subset at 89.85% (of3 84.71
vs the claimed 83.67). The claimed **n = 32** subset gives 87.91%, not 89.92%.
No κ column exists anywhere in the drop.

**Class B is a different story and reproduces exactly**: pairing kink-active
(`tm6_kink_angle < threshold_kink_used`) against `tilt_active` on Class B rows
gives 81.64% and κ = 0.305, matching the claimed 81.64% and κ = 0.31 to the
digit. Our first reading used `npxxy_active` for Class B and got 23.65%; that was
our error, not the drop's.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv'); ap = pd.read_csv('04_amplitude/amplitude_points.csv')
A = r[r.gpcr_class=='A']
ag = lambda d: 100*(d.npxxy_active==d.tilt_active).mean()
def kap(d):
    a=d.npxxy_active.astype(bool); b=d.tilt_active.astype(bool); po=(a==b).mean()
    pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe)
subs = {'all 40': A,
        'NPxxY measured': A[A.d_npxxy_oh.notna()],
        'amplitude panel 32': A[A.receptor.isin(set(ap[(ap.axis=='tilt')&ap.included_class_a_only].receptor))],
        'npxxy panel 28': A[A.receptor.isin(set(ap[(ap.axis=='npxxy')&ap.included_class_a_only].receptor))],
        'no_holds 27': A[A.receptor.isin(set(ap[(ap.axis=='tilt')&ap.included_no_holds].receptor))],
        'minus E1,E2': A[~A.excl_E1 & ~A.excl_E2], 'minus E3': A[~A.excl_E3], 'minus E5': A[~A.excl_E5]}
for k,d in subs.items():
    print('%-20s %2d %6.2f %.3f' % (k, d.receptor.nunique(), ag(d), kap(d)),
          d.groupby('backbone').apply(ag).round(2).to_dict())
B = r[r.gpcr_class=='B']; kink = B.tm6_kink_angle < B.threshold_kink_used
print('Class B', round(100*(kink==B.tilt_active).mean(),2))   # 81.64 — matches the claim
```

**4. Severity — medium to high; reaches a reader.** 89.9% with κ = 0.79 is the
sentence that establishes the instrument. It should not be published until it
recomputes.

**5. What would close it.** The exact filter behind SC-4's Class A row: which 32
receptors, which exclusion flags, and whether rows with an unmeasured axis were
dropped (that is the difference between 86.87% and 90.51%). A κ column in
`headline_by_backbone.csv` would make it checkable in future drops.

---

## N9 — the Class B kink discriminator does not discriminate

**1. Claim as shipped.** §SC-4: "Class B's two axes are non-independent … kink is
discriminator"; `class_b_kink/ALIGNMENT.md`: "Illustrate the TM6 kink
discriminator: Class B active-vs-inactive is identified by kink angle rather than
by 3.50–6.30 tilt"; the row dictionary gives Class B `active` as "kink < 159.95
AND tilt".

**2. What the data says.** Among the eight Class B references,
`angle_class_b_kink_ref < 159.95` on **4 of 4 active and 2 of 4 inactive** —
5VEW (133.8°) and 4K5Y (156.8°) both pass, and both are flagged
`inactive_passes_predicate` with `deviation_class = unclassified`. In the
prediction corpus there is **not one Class B row** where `tilt_active` is True
and the kink test is False, so `active` equals `tilt_active` on every Class B
row; the kink conjunct never binds. The same is true for Class F, which is
tilt-only by design.

Related: `class_b_kink/ALIGNMENT.md` states "active reference ≈ 154 deg,
inactive reference ≈ 161 deg". The shipped values for the pair it ships are
**88.413°** (6X18, active) and **133.788°** (5VEW, inactive) — both below the
159.95° threshold, i.e. the pair chosen to illustrate the discriminator is a pair
on which the discriminator returns the same call.

**3. Reproduction.**

```python
import pandas as pd
rp = pd.read_csv('02_references/reference_predicates.csv')
b = rp[(rp.gpcr_class=='B') & rp.angle_class_b_kink_ref.notna()]
print(b[['receptor','pdb_id','state','angle_class_b_kink_ref','kink_pass','predicate_call']].to_string(index=False))
print(b.assign(k=b.angle_class_b_kink_ref<159.95).groupby('state').k.sum().to_dict())  # active 4, inactive 2
r = pd.read_csv('01_rows/block_a_rows.csv'); B = r[r.gpcr_class=='B']
print(int((B.tilt_active & ~(B.tm6_kink_angle < B.threshold_kink_used)).sum()))  # 0
print(bool((B.active==B.tilt_active).all()))                                    # True
```

**4. Severity — medium; reaches a reader as an overstated instrument.** Class B
is out of scope for every headline claim, so it does not touch the main result,
but the paper describes a two-instrument predicate for Class B that is
operationally single-instrument.

**5. What would close it.** Either a kink threshold that separates the Class B
references, or an explicit statement that Class B is tilt-only in practice and
the kink test is retained for scope documentation.

---

## N10 — `passed` is a self-certifying column with no evidence behind it

**1. Claim as shipped.** `01_rows/block_a_rows.csv` ships `passed` (bool) plus
six gate columns `A1_amino_acid_identity` … `A6_receptor_identity`, all listed as
data in `DATA_DICTIONARY.md`. Caveat C-12 describes A1–A6 as scorer gates with
no pLDDT floor.

**2. What the data says.** `passed` is **True on all 9,490 rows**, and all six
A1–A6 columns are **100% null** — zero non-null values between them. So the drop
asserts that every row cleared six audit gates while shipping no per-row record
of any gate. The lowest `plddt_mean` among "passed" rows is 36.83.

**3. Reproduction.**

```python
import pandas as pd
r = pd.read_csv('01_rows/block_a_rows.csv')
print(int(r.passed.sum()), len(r))                                        # 9490 9490
print({c: int(r[c].notna().sum()) for c in r.columns if c[:2] in ('A1','A2','A3','A4','A5','A6')})
# all zero
print(round(r[r.passed].plddt_mean.min(),2))                              # 36.83
```

**4. Severity — medium; does not reach a reader directly but removes an audit
trail we relied on.** A column that reads True everywhere with no supporting
data cannot be cited as evidence of anything.

**5. What would close it.** Populate A1–A6, or drop them and `passed` from the
export and state in the README that the gates were applied upstream with the
pass rate given as a single number.

---

## N11 — `connector_references.csv` is a comment stub, and the −1.51 Å reference delta has no data behind it

**1. Claim as shipped.** `FIGURE_BRIEF.md` §BA-3 lists
`05_connector/connector_references.csv` as a panel source;
`DATA_DICTIONARY.md` describes it as 4 rows with columns `pdb_id, receptor,
state, p550_f644_ca_distance, note`. §SC-3 quotes "Reference Δ (active −
inactive median) = −1.51 Å (non-overlapping refs)" and derives the magnitude
ratio 0.37 from it.

**2. What the data says.** The file contains a header and four `#` comment
lines; the comments contain commas, so they spill across the declared columns
and parse as data. `p550_f644_ca_distance` has zero non-null values. The −1.51 Å
value is hardcoded in a script (`_analyze.py`) that is not in the drop, and the
77 per-reference distances behind it are stated to be absent. It is the
denominator of the only quantitative number in the orthogonal-signature claim
and it is unverifiable from the archive.

**3. Reproduction.**

```bash
cat 05_connector/connector_references.csv
```
```python
import pandas as pd
c = pd.read_csv('05_connector/connector_references.csv')
print(len(c), int(c.p550_f644_ca_distance.notna().sum()))   # 4 0
print(pd.read_csv('05_connector/connector_summary.csv').delta_ref_median.unique())  # [-1.51] on every row
```

**4. Severity — medium; reaches a reader as an unverifiable denominator.** The
prediction side of the connector result reproduces exactly (pooled delta
−0.5602, 204/256 and 205/256 all recompute), so only the reference scale is
affected.

**5. What would close it.** The 77 per-reference P5.50–F6.44 Cα distances as a
CSV, or the list of 77 PDB IDs so we can measure them ourselves. Either turns a
hardcoded constant into a checkable one. Also: make the file a real CSV or drop
it from the manifest — as shipped it reads as data and is not.

---

## N12 — the stated bootstrap convention does not describe the shipped cluster map, and only cluster draws ship

**1. Claim as shipped.** Claim sheet front matter: "**Bootstrap convention**: 26
paralog clusters (T7 manual paralogy mapping; 42% singletons; see C-8), 1000
resamples, seed 20260909." C-8 makes the cluster bootstrap authoritative.
`README.md` acknowledges "empirically resolves to 29 clusters + 16 singletons in
this zip".

**2. What the data says.** `07_clusters_and_holdout/cluster_map.csv` has **29
clusters and 16 singletons over 48 receptors — 33% singletons, not 42%**. The
shipped `09_bootstrap_draws/bootstrap_draws.csv` was computed on that 29-cluster
map: its 2.5/97.5 percentiles reproduce every `*_cluster_ci_*` value in
`headline_by_backbone.csv` exactly. So the authoritative intervals in the drop
are 29-cluster intervals while the manuscript is being asked to state 26.

Separately, `bootstrap_draws.csv` has a single `bootstrap_type` — `cluster`. The
receptor-bootstrap intervals, which are the ones the claim sheet actually quotes
(D5, N4), have **no draws in the archive at all** and cannot be audited.

**3. Reproduction.**

```python
import pandas as pd, numpy as np
cm = pd.read_csv('07_clusters_and_holdout/cluster_map.csv')
print(cm.cluster_id.nunique(), int((cm.cluster_size==1).sum()), len(cm))   # 29 16 48
b = pd.read_csv('09_bootstrap_draws/bootstrap_draws.csv')
print(b.bootstrap_type.unique())                                           # ['cluster'] only
h = pd.read_csv('03_aggregates/headline_by_backbone.csv').set_index('backbone')
for bb in h.index:
    d = b[(b.statistic=='tilt_shift') & (b.backbone==bb)].value
    print(bb, np.round(np.percentile(d,[2.5,97.5]),4),
          round(h.loc[bb,'median_tilt_shift_cluster_ci_lo'],4), round(h.loc[bb,'median_tilt_shift_cluster_ci_hi'],4))
# identical to 4 dp on all four backbones
```

**4. Severity — high; reaches a reader as a Methods statement that does not
describe the computation.** The README flags the 29-vs-26 gap; the claim sheet
does not, and it is the claim sheet that the manuscript quotes.

**5. What would close it.** The 26-cluster mapping, if it exists, and a rerun of
the draws on it; or confirmation that 29 is operational and the Methods should
say 29 clusters / 16 singletons. Also, ship the receptor-bootstrap draws or
state that the receptor CIs are not auditable.

---

## N13 — three `ALIGNMENT.md` files name chain A as the receptor when the receptor is chain R

**1. Claim as shipped.** `success_case/ALIGNMENT.md`: "Superpose on Chain A
receptor Cα, TM1–TM7." `janus_cnr2/ALIGNMENT.md`: "Chain A (receptor) TM1–TM7 Cα
only." `class_b_kink/ALIGNMENT.md`: "Chain A (receptor) TM1–TM7 Cα."
`confidently_wrong/ALIGNMENT.md`: "Receptor Cα atoms, chain A."

**2. What the data says.** In 7JVR, 8GUR and 6X18 chain A is the **Gα subunit**
and the receptor is **chain R**. Following the instruction literally superposes
the prediction onto the G protein:

| file | chain A | receptor chain |
|---|---|---|
| `success_case/7JVR.cif` | A: 224 Cα, 5–354 (Gαi) | **R: 269 Cα, 34–441** |
| `janus_cnr2/8GUR.cif` | A: 227 Cα, 3–354 (Gαi) | **R: 282 Cα, 22–312** |
| `class_b_kink/6X18.cif` | A: 355 Cα, 11–394 (Gαs) | **R: 384 Cα, 29–423** |
| `confidently_wrong/5G53.cif` | A: 283 Cα, 6–312 (AA2AR copy 1) | **B** — the shipped values match copy 2 |

For 5G53 chain A is a receptor chain, but the shipped `d_tilt_ref` (18.0974) and
`d_npxxy_oh_ref` (3.7052) reproduce on **chain B**, not chain A.

Taken with D13 and D20, **all eight `ALIGNMENT.md` files carry at least one
wrong identifier** — chain, residue, measured value or file name. Our earlier
report said four; it is eight.

**3. Reproduction.**

```python
from anchors_lib import atoms, chains, find
for f in ['11_structures/success_case/7JVR.cif','11_structures/janus_cnr2/8GUR.cif',
          '11_structures/class_b_kink/6X18.cif','11_structures/confidently_wrong/5G53.cif']:
    print(f.split('/')[-1], chains(atoms(f)))
print(find(atoms('11_structures/success_case/7JVR.cif','OH'),'R', 4.252152))
# [('TYR',209,'TYR',426, 4.2522)]  == shipped d_npxxy_oh_ref for 7JVR
print(find(atoms('11_structures/confidently_wrong/5G53.cif','OH'),'B', 3.705183))
# [('TYR',197,'TYR',288, 3.7052)]  == shipped d_npxxy_oh_ref for 5G53, chain B not A
print(find(atoms('11_structures/janus_cnr2/8GUR.cif','OH'),'R', 3.276825))
# [('TYR',209,'TYR',299, 3.2768)]  ALIGNMENT says Y223/Y293
print(find(atoms('11_structures/agonist_only_vs_ternary/6PT2.cif','OH'),'A', 16.748669))
# [('TYR',233,'TYR',318,16.7487)]  ALIGNMENT says Y226/Y308
```

**4. Severity — high; reaches a reader through any render.** A chain error is
worse than a residue error: it produces a picture that looks plausible and is of
the wrong molecule.

**5. What would close it.** Regenerate all eight `ALIGNMENT.md` files
programmatically from the same table the scorer uses, with each stated distance
recomputed from the shipped file before it is written down. Until then we treat
all of them as unreliable and recompute anchors from coordinates against the
tidy values.

---

## N14 — `connector_orthogonality/ALIGNMENT.md` gives residue numbers that do not exist in the file beside it

**1. Claim as shipped.** `connector_orthogonality/ALIGNMENT.md`: "ADRB2
numbering (uniprot P07550, chain A) — P5.50 = P211, I3.40 = I121, F6.44 = F290,
Y5.58 = Y219, Y7.53 = Y326"; "Measured values: d(P5.50 Cα – F6.44 Cα) on active
β2AR ≈ 10.5 Å".

**2. What the data says.** The shipped `4LDE.cif` carries a **+1000 auth
numbering offset**: chain A runs 858–1342. Residues 211, 121, 290, 219 and 326
are simply absent. With the offset applied, P1211–F1290 is **12.32 Å**, not
"≈10.5 Å". The 6.44 position is **F1282**, and P1211–F1282 is **10.80 Å**,
consistent with the stated value and with the 10.48 Å active median. The
+1000 offset is documented nowhere in the file.

**3. Reproduction.**

```python
from anchors_lib import atoms, chains, dist
A = atoms('11_structures/connector_orthogonality/4LDE.cif')
print(chains(A)['A'])                       # (454, 858, 1342)
print(round(dist(A,'A',1211,1290),4))       # 12.3177  <- ALIGNMENT's F6.44 = F290
print(round(dist(A,'A',1211,1282),4))       # 10.8017  <- F6.44 = F282
print(round(dist(A,'A',1075,1275),4))       # 17.5625  == shipped d_tilt_ref for 4LDE
```

**4. Severity — medium; reaches a reader through the connector render.**

**5. What would close it.** Confirm F6.44 = F282 for ADRB2 and add the auth
offset to the file. Fold into the N13 regeneration.

---

## N15 — `class_b_kink/ALIGNMENT.md` quotes kink angles that contradict the shipped table

Covered in N9 §2 and reproduced there. Stated separately here because the fix is
a different one: the ALIGNMENT file's "active ≈ 154 deg, inactive ≈ 161 deg"
should be replaced with the shipped 88.413° / 133.788°, and the panel needs a
different Class B pair if it is to illustrate a discriminator.

**Severity — low as a number, medium as a figure premise. What would close it**:
a Class B reference pair that straddles the 159.95° threshold, or a decision to
drop the panel.

---

## N16 — `broken_cell/ALIGNMENT.md` lists a file that is not in the drop

**1. Claim as shipped.** `11_structures/broken_cell/ALIGNMENT.md`, §Files:
"`MISSING_ACM1_active.cif` — ACM1 active reference."

**2. What the data says.** The directory contains only the two prediction CIFs
and `ALIGNMENT.md`. The filename is self-documenting — ACM1 is one of the eight
sealed receptors with no active reference (D14) — but a manifest-style Files
list that names a non-existent file will send a downstream agent looking for it.

**3. Reproduction.**

```bash
grep -n MISSING_ACM1_active 11_structures/broken_cell/ALIGNMENT.md
ls 11_structures/broken_cell/
```

**4. Severity — low; wastes time, reaches no reader.**

**5. What would close it.** Replace the line with "no ACM1 active reference
exists in the reference set (sealed receptor)".

---

## N17 — CRHR1 is entered twice in the reference tables under two names, with different inactive references

**1. Claim as shipped.** `README.md` §"Known gaps": "The reference_set.csv has
duplicate (receptor, role, pdb_id) rows in some cells" — stated as the reason
the panel count is 98 rather than 89.

**2. What the data says.** The duplicate is specific and consequential.
`reference_predicates.csv` carries CRHR1 twice: once as **CRHR1** (active 6P9X,
inactive 4K5Y) and once as **CRFR1** (active 6P9X, inactive **8GTI**).
`reference_metadata.csv` has 6P9X twice, `is_panel = True` under CRHR1 and
`False` under CRFR1. `reference_separation.csv` therefore carries two rows with
different separations for the same receptor — `delta_tilt_ref` 7.7666 (CRHR1)
and 7.5601 (CRFR1) — and the CRFR1 row has a **null `gpcr_class`** and lists
`axes_valid_for_receptor = "tilt"` where CRHR1 lists `"tilt,kink"`. CRFR1 is not
a corpus receptor. This alias is the whole of the 98-vs-99 gap in D9, and it
means 8GTI — a real CRHR1 inactive reference that is in the drop — is excluded
from CRHR1's own separation.

**3. Reproduction.**

```python
import pandas as pd
rp = pd.read_csv('02_references/reference_predicates.csv')
print(rp[rp.receptor.isin(['CRHR1','CRFR1'])][['receptor','pdb_id','state','d_tilt_ref']].to_string(index=False))
print(pd.read_csv('02_references/reference_metadata.csv').query("pdb_id=='6P9X'")[['receptor','state','is_panel']])
print(pd.read_csv('02_references/reference_separation.csv').query("receptor in ['CRHR1','CRFR1']"))
print('CRFR1' in set(pd.read_csv('01_rows/block_a_rows.csv').receptor))   # False
```

**4. Severity — medium; does not reach a reader (CRHR1 is Class B, excluded by
E4 from every headline claim) but it corrupts the reference denominators the
Methods must state.**

**5. What would close it.** Merge CRFR1 into CRHR1, decide whether 8GTI or 4K5Y
is the canonical inactive reference (or both, taking the per-axis median as
elsewhere), and re-emit `denominator_populations.csv`.

---

## N18 — SC-3's stated NPxxY slope range reproduces from no inclusion set

**1. Claim as shipped.** §SC-3: "NPxxY-OH: 0.12 to 0.55 across backbones".

**2. What the data says.** `amplitude_fits.csv`, `axis == "npxxy"`: `baseline`
and `class_a_only` both run **0.042 to 0.366**; `class_a_no_holds` runs 0.058 to
0.450. Neither bound of "0.12 to 0.55" appears. This is separate from D1 (which
covers the CI and n/SD claims on the same line) and separate from D3 (which
covers the tilt range).

**3. Reproduction.**

```python
import pandas as pd
n = pd.read_csv('04_amplitude/amplitude_fits.csv').query("axis=='npxxy'")
print(n.groupby('inclusion_set').slope.agg(['min','max']).round(3))
# baseline 0.042 0.366 ; class_a_no_holds 0.058 0.450 ; class_a_only 0.042 0.366
```

**4. Severity — medium; reaches a reader as a quoted range.**

**5. What would close it.** Same as D1: the analysis that produced these
numbers, or confirmation that the shipped fits supersede.

---

## N19 — the README's own "four numbers a figure agent will get wrong" box carries two wrong numbers

**1. Claim as shipped.** `README.md` §"The four numbers a figure agent will get
wrong without warning": item 1 — "The 89–94% fraction and the amplitude null are
NOT contradictory"; item 2 — "SD(Δ_tilt_ref) across the 40 Class A receptors is
1.19 Å".

**2. What the data says.** The fraction range is **88.4–94.7%** — the README says
89–94%, the claim sheet says 89–95%, and the data agrees with neither. The tilt
SD is **1.171 Å over 32 receptors**, not 1.19 over 40; 1.195 is the
`class_a_no_holds` value over 27.

**3. Reproduction.**

```python
import pandas as pd
h = pd.read_csv('03_aggregates/headline_by_backbone.csv')
print(round(100*h.fraction_of_way_to_active.min(),1), round(100*h.fraction_of_way_to_active.max(),1))  # 88.4 94.7
t = pd.read_csv('04_amplitude/amplitude_fits.csv').query("axis=='tilt' and inclusion_set=='class_a_only'").iloc[0]
print(round(t.sd_predictor,3), int(t.n_receptors))   # 1.171 32
```

**4. Severity — medium; reaches a reader through whoever builds the figures.**
This box is the first thing a downstream agent reads and it is the place a wrong
number does the most damage.

**5. What would close it.** Regenerate the box from the tidy files rather than
from the claim sheet.

---

# 3. Ranking — would it reach a reader of the published paper?

**Tier 1 — would appear in the paper as a wrong statement, number or picture.**

1. **D18** — CFTR shipped as the δOR ternary structure. The agonist-only vs
   ternary render cannot be built at all.
2. **D12** — the "confidently wrong" exhibit is a correct apo prediction. A panel
   built to spec asserts the opposite of its own data.
3. **N1** — "invariant to every exclusion set (≤0.5%)" is false by up to 222% on
   the drop's own sweep, and E3 is never swept singly.
4. **D5 + N4** — the CIs on the headline shift and on the strongest confidence
   correlation are the receptor bootstrap printed under a cluster-boot label.
5. **D1 + D2 + D3 + N18** — the amplitude and connector wording: "all CIs cross
   zero" is false, the ratio CI cannot cross zero by construction, tilt slopes go
   negative, and neither stated slope range reproduces.
6. **N3** — four Class A receptors cannot fire the predicate by construction and
   stay in every Class A denominator.
7. **N6** — the headline "89–95% of the way" is a median over an unbounded ratio
   that reaches 212× and goes negative.
8. **D9** — the reference denominator the Methods must state: 89 claimed, 98
   empirical, 167 total, 127 → 162 for the audit set.
9. **N13 + D13 + D20 + N14** — all eight ALIGNMENT files are wrong; three name
   the G protein as the receptor.
10. **D6 + D15** — the fraction values, its range floor, and its denominator.
11. **N12** — 26 clusters claimed, 29 shipped and used for every authoritative CI.

**Tier 2 — a referee would find it; a casual reader would not.**

N8 (SC-4 unreproducible), N7 (the 39 are not Class A), D14 (610 untestable
rows), D17 (bootstrap width ratio), N5 (SC-2 CIs), D16 (n_receptors = 40 vs 32),
D19 (no template/MSA record), N9 (kink does not discriminate), N10 (`passed`
self-certifies), N11 (connector reference stub), D22 (RMSD irreproducible),
D21 (ΔNPxxY against a different reference), D10 (five deviation classes),
N17 (CRHR1/CRFR1 duplicate), N2 (`excl_any` removes 54%).

**Tier 3 — corrections to make in passing.**

D7 (0.02% → 0.04%), D4 (narrative pLDDT values), D8 (`matches_claim_sheet`
tolerance), D11 (brief-internal conflict), D23 (pooled rate named a mean),
N15 (kink angles in ALIGNMENT), N16 (missing file listed), N19 (README box).

**Sequence.** D1, D2, D3, D5 and N1 change the wording of Beats 3, 4 and 5 and
the intervals on Beat 2, so all five must be settled before any panel is drawn.
D18 and D12 determine whether two structural exhibits exist at all. N3, N6 and
N7 determine what the Class A denominators are, and therefore what SC-2 and SC-4
mean.

---

# 4. Checked and NOT a finding (draft-only — strip before sending)

These were run down and cleared. Several were things we initially got wrong; the
list is kept because the same checks will run against the next drop.

- **Exclusion flags are internally consistent with their stated rules.** E1
  fires on exactly the 25 rows of the one cell with mean `plddt_mean` < 50; E2 on
  exactly the 4 rows with `d_npxxy_oh` < 2.4; E4 exactly on Class B ∪ F; E5
  exactly on CNR1, FZD4, OPRD; and `excl_E3 == excl_E3_tilt | excl_E3_npxxy`
  exactly. No cell with mean pLDDT below 50 is left unflagged.
- **Every cluster-bootstrap CI in the drop reproduces from
  `bootstrap_draws.csv`** at the 2.5/97.5 percentiles, to four decimals, for
  tilt shift, delta-to-active shift, fraction, all 24 amplitude slopes and all 12
  pLDDT correlations. The bootstrap machinery is sound; the labelling is not
  (D5, N4).
- **`MANIFEST.json` verifies.** All 80 entries present, all sha256 match, all
  CSV row counts match. The only mismatch is `MANIFEST.json`'s own hash, which is
  self-referential and unavoidable, and `total_bytes` off by 522 for the same
  reason. Nothing on disk is unlisted and nothing listed is missing.
- **No sentinel values.** Scanned every numeric column of every CSV for −999,
  9999 and −1. None present. Their README claim holds.
- **The connector prediction side reproduces exactly.** Pooled
  `delta_pred_median` −0.5602 recomputes from `connector_predictions.csv`;
  204/256 and 205/256 recompute; the 512 rows are 16 balanced strata of 32.
- **SC-4's Class B numbers reproduce exactly.** 81.64% agreement and κ = 0.305
  against a claimed 0.31 — pairing kink-active with tilt-active. *Our first
  reading used `npxxy_active` for Class B and got 23.65%, which is meaningless
  because NPxxY is never measured on Class B.* Our error, not theirs.
- **SC-6, SC-7, SC-8, SC-10 reproduce exactly.** Per-backbone predicate-active
  counts 1167/1273/1229/1197 and both >3 Å rows; engagement 99.1/97.7/97.2/98.8%
  over 47 cognate receptors, with `engaged` identical to
  `n_interface_contacts_ga_receptor > 30` on all 4,695 rows; fold integrity
  96.33% overall and 95.64/95.07/97.73/96.88 per backbone; 48 receptors as
  40 A + 4 B + 4 F.
- **The `active` predicate matches its documented definition exactly** in all
  three classes: A = `npxxy_active & tilt_active`, B = kink AND tilt, F = tilt.
- **GLP1R/chai's identical `delta_cognate_minus_apo_tilt` and
  `delta_cognate_minus_apo_delta_to_active` (both 1.047307481027726) is not a
  duplication bug.** For the four Class B receptors `delta_to_active` is a
  constant offset from the tilt distance, so the two cognate−apo differences are
  the same number by definition. We flagged it as a bug first; it is not. (It is
  worth noting in Methods that for Class B the "state reached" metric and the
  tilt axis are the same measurement — but that is a wording matter, not a defect.)
- **`reference_separation.csv`'s per-axis medians are a rule, not an
  inconsistency.** ADRB2's tilt separation lands on 2RH1 and its NPxxY separation
  on 3NYA because each axis takes the median over the three inactive references
  independently. We first read this as two axes using two different references
  arbitrarily. It is consistent; it is just undocumented (D21).
- **`janus_cnr2/ALIGNMENT.md`'s engineered-mutation claim is correct.** 5ZTY
  residues 242 and 304 are both GLU, matching the stated R242E and G304E.
- **The four shipped prediction CIFs reproduce their own rows exactly.** Once the
  correct anchors are used, `d_npxxy_oh` and `d_gpcrdb_tm6_tilt_246_637_ca`
  recompute to the last decimal on all four. The coordinates and the tidy tables
  agree; only the ALIGNMENT prose is wrong.
- **`success_case`'s selection rule reproduces.** Row 8285 is rank 12 of 25
  non-excluded rows by `rmsd_to_active_ref` — the 50th percentile, exactly as
  `SELECTION.md` states. So does `SELECTION.md`'s note that no Class A row
  exceeds 8 Å from active: the corpus maximum is 5.3068 Å.
- **`matches_claim_sheet` is not lying.** It is True within the 0.02 tolerance
  the README documents for it. Our report called the column "unreliable"; the
  correct criticism is that its tolerance is five times the drift it is being
  used to rule out (see §5).

---

# 5. Where our own `DISCREPANCY_REPORT.md` is wrong or overstated (draft-only)

Fix these in `analysis/block_a/DISCREPANCY_REPORT.md` before anything is sent.

1. **The "Protenix cognate 0.871" anomaly does not exist.** The report's
   "Not reproduced" section says: "Protenix cognate ships 0.871 where both the
   pooled rate and the per-receptor mean are 0.890. That one value differs from
   both candidate definitions and is unexplained." It is not unexplained. The
   shipped 0.870638 **is** the pooled all-rows rate and **is** the mean over
   receptors — both give 0.870638 to six decimals. 0.889565 is the rate after E1
   is applied, i.e. after the broken ACM1/cognate/protenix cell is dropped, and
   `exclusion_sweep.csv` reports exactly that under `exclusion_set == "E1"`.
   Reproduce with the D23 snippet above. The same claim appears as open question
   **D.1** in `analysis/block_a/DATA_REQUESTS.md` and should be struck from both.

2. **D8 is overstated.** "The shipped `matches_claim_sheet` flag is itself
   unreliable" is too strong. The README defines the flag as agreement "within
   0.02 of claim", and every row satisfies that — of3's fraction is off by
   0.0188. The flag does what it says. The real defect is that the tolerance is
   documented only in README prose and is looser than the four-decimal precision
   at which SC-2 quotes the fractions. Reword accordingly.

3. **D20's "four of the drop's ALIGNMENT files are now known to be wrong" is
   understated.** It is eight of eight once chain identifiers, measured values
   and file lists are checked (N13, N14, N15, N16). The sentence should be
   "every ALIGNMENT file in the drop carries at least one wrong identifier".

4. **D9's "45 active-role / 54 inactive-role" needs its source named.** 45/54 is
   what `reference_predicates.csv` returns for the 98 panel PDBs (99 rows);
   `reference_metadata.csv` returns 44/54 (98 rows). Both are right; the extra
   row is the CRHR1/CRFR1 duplicate (N17). As written the report reads as if
   44 + 54 = 98 and 45 + 54 = 98 were both being asserted.

5. **D12's "567 is simply the highest-pLDDT row in the whole cell" should say
   which pLDDT.** It is the highest `plddt_mean` row. The highest
   `plddt_at_anchors` row in that cell is 557, not 567.

6. **D22's trimmed-window figures do not reproduce as stated.** The report gives
   "excluding ICL3 gives 1.290, 7TM-only 1.298, 34–420 gives 1.290". 7JVR's ICL3
   (226–365) is unresolved in the reference, so it is already absent from the
   269 shared Cα and those three windows are not distinguishable that way. The
   conclusion is unaffected — 1.2952 over all shared Cα, closest trim 1.2456,
   shipped 1.218, nothing reproduces — but the numbers should be replaced with
   the ones the snippet in D22 above prints.

7. **`DATA_REQUESTS.md` item 7 asks for the wrong thing.** It requests "the
   α5-CT 21-mer coordinates **as supplied to the model**". Block A supplied the
   whole cognate Gα subunit; there is no 21-mer input. Reword to ask for the Gα
   chain as supplied.

---

# Appendix A — `anchors_lib.py`

Save in the drop root. Pure stdlib; no `gemmi`, no PyMOL. `atoms()` returns
`{(chain, auth_seq_id): (comp_id, x, y, z)}` for one atom name.

```python
import math

def atoms(path, want='CA'):
    out = {}
    lines = open(path).read().split('\n'); i = 0
    while i < len(lines):
        if lines[i].strip() == 'loop_':
            j = i + 1; cols = []
            while j < len(lines) and lines[j].strip().startswith('_'):
                cols.append(lines[j].strip()); j += 1
            if cols and cols[0].startswith('_atom_site.'):
                n = [c.split('.')[1] for c in cols]; ix = {k: v for v, k in enumerate(n)}
                ch = ix.get('auth_asym_id', ix.get('label_asym_id'))
                rn = ix.get('auth_seq_id', ix.get('label_seq_id'))
                while (j < len(lines) and lines[j].strip()
                       and lines[j].strip() != 'loop_' and not lines[j].startswith('#')):
                    p = lines[j].split()
                    if len(p) >= len(n) and p[ix['label_atom_id']] == want:
                        try: k = (p[ch], int(p[rn]))
                        except ValueError: j += 1; continue
                        out.setdefault(k, (p[ix['label_comp_id']], float(p[ix['Cartn_x']]),
                                           float(p[ix['Cartn_y']]), float(p[ix['Cartn_z']])))
                    j += 1
            i = j
        else:
            i += 1
    return out

def dist(A, ch, a, b):
    if (ch, a) not in A or (ch, b) not in A: return None
    return math.dist(A[(ch, a)][1:], A[(ch, b)][1:])

def find(A, ch, target, tol=1e-3):
    """Every residue pair in chain `ch` whose distance equals `target`."""
    ks = sorted(k for k in A if k[0] == ch)
    return [(A[a][0], a[1], A[b][0], b[1], math.dist(A[a][1:], A[b][1:]))
            for i, a in enumerate(ks) for b in ks[i+1:]
            if abs(math.dist(A[a][1:], A[b][1:]) - target) < tol]

def chains(A):
    c = {}
    for (ch, rn) in A: c.setdefault(ch, []).append(rn)
    return {k: (len(v), min(v), max(v)) for k, v in sorted(c.items())}
```
