# DISCREPANCY_REPORT.md — Block A claim sheet vs shipped data

Required deliverable (brief §9.6). Every number below was recomputed from the
tidy files in `data/block_a/` alone. Reproduce with:

```bash
python3 analysis/block_a/verify_claims.py          # 34 checks, exits 1 on any mismatch
```

**Result: 19 of 34 checks reproduce, 15 mismatch.** Four mismatches were already
named in the brief (§4.1–4.4); **six further ones are new and are flagged here
for the first time** (D5–D10). Nothing in the shipped data is wrong — in every case the
tidy files are self-consistent and it is the claim sheet that has drifted.

Convention throughout: **the data wins, the discrepancy is stated, not smoothed**
(brief §8.4).

---

## Summary

| # | where | severity | one line |
|---|---|---|---|
| D1 | SC-3, brief §4.1 | **high** | "all CIs cross zero" is false; Protenix is signed positive |
| D2 | SC-3, brief §4.2 | **high** | connector effect is not signed; the ratio CI cannot cross zero by construction |
| D3 | SC-3, brief §4.3 | **high** | tilt slopes go negative; claim sheet mixes inclusion sets within one line |
| D4 | SC-11, brief §4.4 | medium | narrative pLDDT values differ from the CSV; CSV is source of truth |
| **D5** | **SC-1** | **high — new** | **CIs labelled "cluster-boot" are the receptor-boot column** |
| **D6** | **SC-2** | **medium — new** | **fractions differ, denominator is 40 not 38–39, range is 88–95% not 89–95%** |
| **D7** | **SC-6** | low — new | heading says 0.02%; the true rate is 0.041% and SC-6's own body says 0.04% |
| **D8** | `headline_by_backbone.csv` | low — new | `matches_claim_sheet` is `True` on all four rows but the fraction disagrees |
| **D9** | **Methods §7.1, C-6** | **high — new** | **reference-set denominator is 98 empirically, not the 89 the Methods requires stating** |
| **D10** | **BA-1b spec** | medium — new | `deviation_class` has five levels, not the three the panel spec assumes |
| **D23** | `*_active_rate_panel_mean` | medium — new | it is a pooled row-level rate over all classes, not a panel mean |
| **D22** | `rmsd_to_active_ref` | medium — new | does not reproduce from the coordinates, and the scorer's atom set is not in the drop |
| **D18** | `11_structures/agonist_only_vs_ternary/` | **CRITICAL — new** | **8FZQ.cif is CFTR, not an opioid receptor complex** |
| **D19** | Methods, templates and MSAs | **high — new** | no row-level record of either; MSA pinning is asserted on no evidence |
| **D20** | two more `ALIGNMENT.md` files | medium — new | ACM1 and DRD2 anchors wrong, same failure as D13 |
| **D21** | ADRB2 ΔNPxxY | medium — new | −6.581 is against the median inactive reference, not 2RH1 |
| **D11** | brief §8.1 vs §6 | low — new | "fraction in T2 only" cannot hold: §6 requires it in T5 and S-T2 too |
| **D12** | `11_structures/confidently_wrong/` | **CRITICAL — new** | **the shipped structure is not confidently wrong; it is confidently RIGHT** |
| **D13** | `ALIGNMENT.md` files | **high — new** | anchor residues and measured values do not match the shipped data |
| **D14** | SC-6 / D7 | medium — new | 610 of 4,866 predicate-active rows have no active reference and cannot be tested |
| **D15** | `headline_by_backbone.csv` | medium — new | the `n_receptors_*` columns overstate the effective n |
| **D16** | `plddt_correlations.csv` | low — new | `n_receptors = 40` on all 12 rows; the population has 32 |
| **D17** | Methods §7.4 | medium — new | "receptor bootstrap ~1.10× tighter" holds almost nowhere; ratios run 1.00–2.20 |

---

## D1 — The NPxxY amplitude null is not clean (SC-3, line 159)

**Claim sheet**: *"NPxxY-OH: 0.12 to 0.55 across backbones; all CIs cross zero;
SD(Δref) = 4.71 Å."*

**Data** (`amplitude_fits.csv`, `axis=npxxy`):

| backbone | slope | cluster CI | crosses zero |
|---|---:|---|---|
| boltz | 0.042 | [−0.327, 0.561] | yes |
| chai | 0.366 | [−0.001, 0.901] | yes, barely |
| of3 | 0.176 | [−0.036, 0.410] | yes, barely |
| **protenix** | **0.257** | **[0.074, 0.552]** | **no** |

`n_receptors` = 28 (not 34), `sd_predictor` = 5.222 (not 4.71).

**Beyond the brief — two things that make this firmer:**

1. **Protenix excludes zero in all three inclusion sets** — `baseline`,
   `class_a_only` and `class_a_no_holds`. It is not an artefact of the
   restriction choice, so the rewording is obligatory rather than arguable.
2. **For NPxxY, `baseline` and `class_a_only` are byte-identical** (same slopes,
   same n=28, same SD). So **no shipped inclusion set produces n=34 / SD=4.71.**
   That line did not come from a different subset of this data; it came from an
   analysis that is not in the archive.

**Panel must show**: four small multiples with the fitted line, its CI band, and
**the unity line on every panel** (BA-4a); the slope forest with **zero and unity
both marked** (BA-4b), Protenix's interval visibly clear of zero.

**Recommended wording**: "Three of four backbones show no evidence of amplitude
reproduction; one (Protenix) shows a weak signed positive slope of 0.26, roughly
a quarter of the expected receptor-to-receptor scaling and far below unity. No
backbone approaches a slope of 1." Do not write "all CIs cross zero" (brief §8.6).

---

## D2 — The connector effect is not signed (SC-3, orthogonal signature)

**Claim sheet**: magnitude ratio **0.37, CI [0.04, 0.77]** — reads as signed.

**Data** (`connector_summary.csv`, pooled): `delta_pred_median` = −0.560,
`delta_cluster_ci` = **[−1.196, +0.026]**, which includes zero. All four
per-backbone CIs include zero as well.

The ratio is computed from the **absolute value** of the delta, so its CI
**cannot cross zero by construction**. It is not evidence of a signed effect.

**Panel must show**: BA-3b forest with **zero marked** and every CI visibly
crossing it. Lead with BA-3c, the agreement counts, which are the strong part.

**Recommended wording**: report direction unanimity (4/4 same-signed as the
references), row-level agreement (204/256 = 79.7% and 205/256 = 80.1% — both
reproduce exactly), and magnitude "roughly one third of reference scale, with an
interval that includes zero". Never "the orthogonal signature confirms" at
signed-effect strength (brief §8.6).

---

## D3 — Tilt slopes go negative, and the claim sheet mixes inclusion sets

**Claim sheet**: *"Tilt: 0.03 to 0.50 across backbones"*, SD(Δref) = 1.19,
n = 40.

**Data**, by inclusion set:

| set | slopes (boltz / chai / of3 / protenix) | n | SD |
|---|---|---:|---:|
| `baseline` | +0.445 / +0.081 / +0.107 / +0.611 | 39 | 2.169 |
| `class_a_only` | **−0.298 / −0.659** / +0.233 / +0.082 | 32 | 1.171 |
| `class_a_no_holds` | **−0.319 / −0.558** / +0.250 / +0.085 | 27 | 1.195 |

**Beyond the brief**: the claim-sheet line is not simply the wrong set — it is a
**mixture of three**. Its all-positive range resembles `baseline`; its SD of 1.19
matches `class_a_no_holds` (1.195); its n = 40 matches none of the three. That is
a more precise and more fixable diagnosis than "the data disagrees", and it means
the fix is to name one inclusion set and quote it consistently.

A negative slope is not physically interpretable — it would mean the model moves
receptors backwards in proportion to how far they should move. With
`sd_predictor` = 1.17 Å this is a predictor with essentially no dynamic range.

**Panel must show**: BA-4c, tilt SD (1.17) beside NPxxY SD (5.22); BA-4d, the
attenuation instability curve with `unstable` regions shaded.

**Recommended wording**: report no tilt amplitude slope in either direction.
State the tilt axis as **uninformative for amplitude** — a property of the
instrument, not a result about the models.

---

## D4 — pLDDT values in the narrative differ from the CSV (SC-11)

`plddt_correlations.csv` is internally consistent, carries explicit
`signed_at_cluster_boot` and `primary_or_secondary` columns, and **is the source
of truth**. Several values in the narrative documents differ from it (for example
`of3` / `plddt_mean` is −0.258 in the CSV).

**Verified**: signed at cluster bootstrap on the primary aggregation for **2 of 4**
backbones (boltz −0.221, of3 −0.626; chai and protenix null). This reproduces.

`n_rows` ≈ 1,600 per backbone indicates a Class-A-restricted subset — **state the
restriction in the caption**.

**Panel must show**: BA-5a forest, all three aggregations, primary marked
distinctly; BA-5b the before/after for OF3 (strengthens, −0.258 → −0.626) and
Protenix (collapses, +0.327 → +0.068).

**Recommended wording**: `plddt_at_anchors` was designated primary **post hoc**,
after all three aggregations were computed. Say so, and report all three (W-2).
The disclosure is what protects the result, not the label.

---

## D5 — NEW: SC-1's CIs are receptor-bootstrap, labelled cluster-bootstrap

**Claim sheet SC-1** presents a column headed *"95% CI (cluster-boot)"*.

**Data** (`headline_by_backbone.csv`) carries both bootstraps separately. The
quoted intervals match the **receptor** column, not the cluster column:

| backbone | quoted as "cluster-boot" | true CLUSTER CI | true RECEPTOR CI | distance to cluster / receptor |
|---|---|---|---|---|
| boltz | [4.403, 5.502] | [3.528, 5.545] | **[4.403, 5.502]** | 0.918 / **0.000** |
| chai | [0.373, 3.452] | [0.358, 3.763] | **[0.391, 3.452]** | 0.326 / **0.018** |
| of3 | [4.072, 4.998] | [3.951, 5.215] | **[4.333, 4.994]** | 0.338 / **0.266** |
| protenix | [4.909, 5.603] | [4.633, 5.743] | **[4.901, 5.679]** | 0.416 / **0.084** |

Boltz is an exact byte-for-byte match to the receptor interval, which settles it.

**Why this matters.** Methods §7.4 makes the cluster bootstrap over 26 paralog
clusters authoritative and the receptor bootstrap secondary and ~1.10× tighter;
§8.4 requires cluster CIs in the text and receptor CIs in supplementary tables
only. As written, SC-1 quotes the tighter interval under the authoritative
label — **it overstates precision**. For boltz the true lower bound is 0.88 Å
below the one quoted.

**Panel must show**: every CI in BA-2 and T2 drawn from the `*_cluster_ci_*`
columns, with the receptor CI reserved for supplementary S3 (the cluster-vs-
receptor comparison, C-8).

**Recommended wording**: requote all four SC-1 intervals from the cluster
columns. Add to Methods that 11 of 26 clusters are singletons, so the paralogy
correction acts on only 15 multi-member clusters (C-8).

---

## D6 — NEW: SC-2's fractions, denominator and stated range all drift

**Claim sheet SC-2**: fractions 0.9456 / 0.8878 / 0.9152 / 0.9118, headline
range **"89–95%"**, denominator *"n=38–39 receptors (sealed 8 dropped)"*.

**Data** (`headline_by_backbone.csv`):

| backbone | claim | data | diff |
|---|---:|---:|---:|
| boltz | 0.9456 | 0.9472 | +0.0016 |
| chai | 0.8878 | 0.8841 | −0.0037 |
| of3 | 0.9152 | **0.9340** | **+0.0188** |
| protenix | 0.9118 | **0.9201** | **+0.0083** |

`n_receptors_fraction` = **40** on every row, not 38–39.

The true range is **0.884–0.947**, so **chai falls below the claimed 89% floor**.
The brief's §8.1 already uses 0.884–0.947, so the brief and the data agree and
only the claim sheet is stale — but §4 did not list this, so it is recorded here.

**Panel**: none. Per brief §6 and §8.1 the fraction appears in **Table T2 only**,
never in a figure and never in the abstract.

**Recommended wording**: "88–95% of the way to the active reference" with the
denominator stated as 40 receptors, immediately followed by the mean-versus-
covariance sentence required by §8.1. Never "reproduces the active structure".

---

## D7 — NEW: SC-6's headline false-positive rate is wrong in its own heading

The SC-6 heading reads *"0.02% false-positive rate"*. Its body says 2 of 4,866
predicate-active rows, which is **0.041%** — and the body itself says 0.04%.
Every per-backbone count and both >3 Å failures reproduce exactly; only the
heading number is wrong, by a factor of two.

**Recommended wording**: 0.04% (2 of 4,866). Quote the denominator with it.

---

## D8 — the `matches_claim_sheet` tolerance is undocumented where it is used

**Reworded 2026-09-10; the earlier version overstated this.** It read "the
shipped `matches_claim_sheet` flag is itself unreliable … false for the
fraction". That is too strong. The README defines the flag as agreement *within
0.02 of claim*, and every row satisfies it — OpenFold3's fraction is off by
0.0188, inside the stated tolerance. **The flag does what it says.**

The real defect is narrower: the tolerance lives only in README prose, while
SC-2 quotes the fractions to four decimals. A reader who takes `True` at the
precision the numbers are printed at will be wrong by up to 0.019. Do not use
the column as evidence that a number is safe to quote *at quoted precision*.

---

## D9 — NEW: the reference-set denominator the Methods must state does not match the data

Brief §7.1 requires Methods to state *"89 unique reference PDBs (40 active, 48
inactive, 1 sealed-active-only)"*. Caveat C-6 gives a ready-made manuscript
sentence asserting *"89 unique … 41 unique active-state references … 48 unique
inactive-state"*.

**The shipped `02_references/denominator_populations.csv` disagrees, and says so
in its own `used_for` column:**

| population | count | the file's own note |
|---|---:|---|
| `panel_unique_pdbs` | **98** | "C-6 (manuscript claim: 89; empirical: 98)" |
| `panel_unique_pdbs_active` | **44** | "C-6 (manuscript: 41)" |
| `panel_unique_pdbs_inactive` | **54** | "C-6 (manuscript: 48)" |
| `reference_set_total` | 167 | T4 total denominator (agrees) |
| `evaluable_audit_set` | **162** | "T4 contradiction rate denominator (manuscript: 127; empirical: 162)" |

`reference_metadata.csv` independently confirms it: `is_panel == True` on exactly
**98** PDBs. The role split depends on which table you ask:
`reference_predicates.csv` returns 99 rows for those 98 PDBs and splits them 45
active-role /
54 inactive-role rows.

Note also that the brief says **40** active while C-6 says **41** — the two
disagree with each other before either is compared to the data.

**Severity is high** because §7.1 makes stating this denominator a Methods
requirement, and three different numbers (89 claimed / 98 empirical / 167 total)
are in circulation for it. The 127 → 162 gap likewise changes the denominator of
the "construct annotation contradicts RCSB on 40% of evaluable PDBs" statement
in §7.9.

**Panel/table**: S-T3 must reproduce `denominator_populations.csv` verbatim,
including the `used_for` column, so the reconciliation is visible rather than
asserted.

**Recommended wording**: state the empirical 98 (44 active-role / 54
inactive-role across the 48-receptor panel), give 167 as the full reference set,
and cite C-6 as the record of the earlier 89. Do not repeat 89 without the
correction — it is contradicted by the archive shipped to support it.

---

## D-A-24 — WITHDRAWN. The number reproduced; my recomputation was wrong.

**What I recorded.** That supplementary table S-T5's "of 4,866 predicate-active
rows, 610 carry no active reference" was unsourced: 610 reproduced exactly,
4,866 reproduced under no predicate definition I tried (3,739 / 5,230 / 5,548),
and neither 4,866 nor 4,256 appeared anywhere in the drop.

**What is true.** `block_a_rows.csv` ships an `active` column. It sums to
**4,866** over all 9,490 rows, and 4,866 − 610 = **4,256**. Both figures are
exact and both were always there.

**Why I missed it.** I rebuilt the predicate myself as
`d_npxxy_oh < 9.08 AND tilt > 14.932` and applied it to every row.
`active` is **class-conditional**: Class A needs both axes, Class B substitutes
a kink angle, and Class F uses tilt alone. This paper's own Methods says so.

```
                 n     shipped `active`    my Class-A rule
  Class A     7,995            3,742              3,742     <- ZERO disagreements
  Class B       795              607                  0
  Class F       700              517                  0
                              -------
                                4,866
```

On the class the rule applies to, my recomputation and the shipped column agree
on **3,742 of 3,742 rows**. The entire gap is the 1,124 Class B and F rows where
I applied a rule that does not govern them.

**This is the second time this project has made exactly this mistake.** The
first was the "unexplained Protenix 0.871", recomputed with the Class A rule on
a class-conditional column and reported as a defect before being withdrawn. I
recorded that correction, and then made it again on the same block.

**What changed.** `CAP12` now checks the shipped column and passes; `CAP13` and
`CAP14` were added, the second asserting the zero-disagreement result above so
the class-conditional structure is pinned rather than remembered. Ask 3 of
`DATA_REQUESTS.md` is struck. Found by an independent re-verification run by the
corpus session, not by us.

**The generalisable part.** A column whose name states a property is not
necessarily computed the same way for every row of the table. Before declaring a
shipped aggregate irreproducible, check whether the quantity is conditional on
something — and check agreement *within* the stratum the rule governs, which is
the test that would have caught this in one line.

## D-A-23 — NEW: the shipped cluster map does not reproduce the bootstrap convention

`10_narrative/BLOCK_A_CLAIM_SHEET.md` line 7 states the **bootstrap convention**
as "26 paralog clusters (T7 manual paralogy mapping)", and caveat C-8 repeats it
as "26 paralog clusters, 42% singletons". Every cluster-bootstrap interval in the
Block A dossier was computed on that.

`07_clusters_and_holdout/cluster_map.csv` resolves the same 48 receptors into
**29 clusters with 16 singletons (55%)**.

```bash
python3 -c "
import pandas as pd
a = pd.read_csv('data/block_a/07_clusters_and_holdout/cluster_map.csv')
s = a.groupby('cluster_id').size()
print(len(a), 'receptors ->', a.cluster_id.nunique(), 'clusters,', (s==1).sum(), 'singletons')"
# 48 receptors -> 29 clusters, 16 singletons
```

**The intervals in the paper are the 26-cluster ones**, because that is what was
computed. The map is not the object the bootstrap ran on, and we cannot
establish its provenance relative to the published convention. Both numbers are
now stated in Methods, and Fig. S7 already drew the disagreement before anyone
wrote it down here.

**This entry exists to stop a well-meant correction.** On 2026-09-10 a request
audit reported that "six manuscript sentences depend on 26" while the shipped
map holds 29, and the orchestrator changed two Results sentences to say 29
before checking which object the bootstrap used. That made the Methods describe
a resampling unit that was never resampled --- a worse error than the one it
replaced, and one no verifier would have caught, because 29 IS what the shipped
file says. Reverted the same day. **The convention and the map are two different
objects and the manuscript must name which one it means every time.**

Direction of the effect, so the exposure is bounded: more clusters means more
resampling units and slightly narrower intervals, so the published 26-cluster
intervals are the conservative ones.

## D10 — NEW: `deviation_class` has five levels, not three

Brief §5, BA-1b: label every `deviation=True` point and **shape it by
`deviation_class`**, described as `{expected_biology, curation_error,
measurement_artifact}`.

`reference_predicates.csv` carries **five** distinct values across the 9
deviations:

| deviation_class | n |
|---|---:|
| `unclassified` | **5** |
| `measurement_artifact` | 1 |
| `curation_error` | 1 |
| `expected_biology` | 1 |
| `curation_error_or_expected_biology` | 1 |

A three-shape encoding drops or mislabels **two thirds** of the points the panel
exists to show. On the 48-receptor panel subset there are 7 deviations, 3 of them
unclassified.

**Panel must show**: all five levels, `unclassified` with its own neutral marker
rather than folded into a named class, and the compound label kept whole rather
than resolved to one half. The caption should say that 5 of 9 deviations are
unclassified — that is a fact about the reference set, and the encoding must not
hide it.

---

## D11 — NEW: the brief's own rules conflict on where the fraction may appear

§8.1 is categorical: *"Keep the fraction in Table 2, not in a figure … The
fraction goes in T2 only."* But §6 requires **T5** to sweep *"every statistic
under every combination"* — and `exclusion_sweep.csv` carries the fraction as one
of its metrics — and requires **S-T2** to be the per-receptor dump, and
`receptor_summary.csv` carries `fraction_of_way_to_active` as a column.

The two requirements cannot both be met literally.

**Resolved as follows**, and flagged rather than silently chosen: the column is
kept in all three tables, because dropping it would break the robustness
demonstration that §3 says is *"what makes the exclusions defensible rather than
convenient"*. The two supplementary footnotes now state that it appears there as
a data and robustness record, not as a headline, and that the headline reading
and its mean-versus-covariance caveat belong to T2 alone.

The rule's actual purpose — that no reader takes 0.88–0.95 as "reproduces the
active structure" — is preserved. **The no-figure-panel and no-abstract halves of
§8.1 are absolute and are being obeyed without exception.**

---

## D12 — NEW, CRITICAL: the "confidently wrong" structure is confidently right

`11_structures/confidently_wrong/` ships an AA2AR prediction that BA-5e is
specified to present as *"the high-pLDDT AA2AR prediction overlaid on 5G53 …
label it explicitly as a worst-case illustration"*.

**It is not a worst case. It is a correct prediction.**

| row | receptor / backbone / arm | RMSD to active | RMSD to inactive | pLDDT at anchors | predicate |
|---|---|---:|---:|---:|---|
| 552 (what `SELECTION.md`'s rule selects) | AA2AR boltz **apo** | 3.106 Å | **0.857 Å** | 84.3 | inactive |
| 567 (what actually shipped) | AA2AR boltz **apo** | 3.102 Å | **0.948 Å** | 84.6 | inactive |

Both are **apo-arm** predictions. Both sit within 1 Å of the **inactive**
reference, which is where an apo prediction should sit, and the predicate calls
both inactive — correctly. The 3.1 Å distance is from the *active* reference,
which is not the state this row is supposed to reach.

A panel captioned "confidently wrong" on this row would assert the opposite of
what the row shows. **The directory name, `SELECTION.md`'s rule, and the BA-5e
specification are all wrong together**, which is why this survived: each
corroborates the others and none was checked against the row.

Two further defects in the same directory: the shipped file is row **567** while
`SELECTION.md`'s stated rule ("top-quintile RMSD-to-active, highest pLDDT
within") selects row **552**; and 567 is simply the highest-`plddt_mean` row in the
whole cell, which is a different rule from the one recorded.

**Action**: do not build BA-5e as a worst case. Either drop it, or recaption it
for what it is — a confident apo prediction landing correctly on the inactive
reference, which is a *supporting* observation for Beat 5, not a counterexample.
If a genuine confidently-wrong case is wanted, it must be selected fresh, by a
stated rule, from rows that are far from the reference **they were meant to
reach**.

---

## D13 — NEW: the ALIGNMENT.md files name wrong anchor residues

`instrument_schematic/ALIGNMENT.md` gives the tilt anchors as L124/F282, which
measures 9.03 Å on 2RH1. The anchors that reproduce the shipped
`d_tilt_ref` = 11.9283 Å exactly are **L75/L275**. `confidently_wrong/` names
2×46 as L88 (actually **L48**) and Y5.58 as Y213 (actually **Y197**). NPxxY
Y7.53 is correct in both files.

`instrument_schematic/ALIGNMENT.md` also quotes "measured values (from
reference_predicates.csv)" of Δtilt ≈ 5.02 Å and ΔNPxxY ≈ +5.4 Å. **Neither
appears in `reference_predicates.csv` or `reference_separation.csv`**; ADRB2's
shipped values are +5.634 and **−6.581** — note the sign. And 3SN6 is not in the
reference set at all: ADRB2's panel active reference is 4LDE.

Any figure drawing measured distances onto a structure must take them from the
tidy files, not from these ALIGNMENT notes.

---

## D14 — NEW: 610 predicate-active rows cannot be tested at all

D7 corrected SC-6's headline from 0.02% to 0.041% (2 of 4,866). That denominator
is itself wrong: **only 4,256 of the 4,866 predicate-active rows carry an active
reference**; the other 610 have no reference to be scored against.

The testable false-positive rate is **2 / 4,256 = 0.047%**. Report it with the
testable denominator and state the 610 untestable rows, rather than letting rows
that cannot fail dilute the rate.

---

## D15 — NEW: the `n_receptors_*` columns overstate the effective n

`headline_by_backbone.csv` reports round numbers that exceed the non-null
per-receptor values in `receptor_summary.csv`:

| column | shipped | non-null |
|---|---:|---:|
| `n_receptors_tilt` | 48 | 47 |
| `n_receptors_delta` | 48 | 39 |
| `n_receptors_fraction` | 40 | **39** |

**This corrects D6**: the fraction's denominator is not 40 either — the shipped
fraction is a median over **39** receptors. Quote 39.

---

## D16 — NEW: `plddt_correlations.csv` misreports its receptor count

All 12 rows carry `n_receptors = 40`. The population that reproduces the r values
has **32** distinct receptors, and `plddt_per_receptor.csv` itself carries 32.
`n_rows` (~1,600) is consistent; only the receptor count is wrong. Quote 32 in
Table T4.

---

## D17 — NEW: "receptor bootstrap ~1.10× tighter" is not general

Methods §7.4 states the receptor bootstrap is approximately 1.10× tighter than
the cluster bootstrap. Measured across the headline statistics, the
cluster/receptor width ratio runs from **1.00 to 2.20**:

| statistic | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| median tilt shift | **1.84** | 1.11 | **1.91** | 1.43 |
| median Δ-to-active shift | 1.00 | 1.00 | 1.07 | **2.20** |
| fraction | 1.00 | 1.72 | 1.04 | 1.37 |

"~1.10×" holds on 2 of 12. The correct statement is that the cluster bootstrap is
**equal to or wider, by up to a factor of 2.2**, which strengthens rather than
weakens the case for treating it as authoritative — and makes D5 (receptor
intervals quoted under a cluster label) more consequential than a 10% error.

---

## D23 — NEW: `*_active_rate_panel_mean` is a pooled rate, not a panel mean

Adjudicated after two figure sessions reported conflicting versions of this.

**What the column is.** `apo_active_rate_panel_mean` for boltz ships 0.1598.
The pooled row-level rate over **all rows and all classes**, using the
class-aware `active` predicate, is **0.1598** — an exact match to four decimals.
The unweighted mean over cells is 0.1592, close but not the source.

So the column is a **pooled rate**, and the name says *mean*. A pooled rate
weights every prediction equally; a panel mean weights every receptor equally.
They differ whenever cells differ in size, and quoting one under the other's
name will mislead.

**The 16-point gap reported to me is a different thing.**
`cell_summary.both_fire_rate` averaged over all 48 cells gives 0.1017, which is
indeed ~16 points lower. But that compares two **different predicates**:
`both_fire_rate` is NPxxY ∧ tilt, while the shipped column uses the class-aware
`active`. Restricted to Class A the two agree exactly (0.1220 and 0.1220). The
gap is Class B and F, not an error in the column.

**Action.** Quote it as a pooled rate and say so, or recompute a genuine panel
mean and say which. Do not quote it as a "panel mean" unweighted by cell size.
The manuscript currently describes these as "pooled row-level rates", which is
correct.

---

## Not reproduced

One further mismatch was reported to me and **does not reproduce**: that
`*_active_rate_panel_mean` are pooled row rates differing from per-receptor means
by up to a factor of 2.9 (OF3 apo, 0.242 vs 0.083). Recomputing under E1+E2 on
the full panel gives OF3 apo pooled 0.241 and per-receptor mean 0.241 — the same
to three places. The reported figure is not reproducible as stated and is not
recorded as a discrepancy.

**WITHDRAWN 2026-09-10.** This section previously reported "a real and smaller
anomaly: Protenix cognate ships 0.871 where both the pooled rate and the
per-receptor mean are 0.890 … unexplained." There is no anomaly. The shipped
value 0.870638 **is** the pooled rate of the `active` column and **is** the mean
over receptors, to six decimals; 0.889565 is the same quantity after E1 drops
the broken ACM1/cognate/protenix cell, and `exclusion_sweep.csv` reports exactly
that under `exclusion_set == "E1"`.

We reached "unexplained" by recomputing the predicate as the two-instrument rule
on every row, which is wrong for this corpus: the shipped `active` column is
**class-conditional** — Class B substitutes a kink angle and Class F uses tilt
alone. Applying the Class A rule to all 1,175 rows gives 0.722, agreeing with
neither figure, and we read that disagreement as the drop's rather than ours.

```bash
python3 -c "
import pandas as pd
a=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False)
p=a[(a.backbone=='protenix')&(a.arm=='cognate')]
print('pooled        %.6f' % p.active.mean())
print('receptor mean %.6f' % p.groupby('receptor').active.mean().mean())
q=p[~p.excl_E1.astype(bool)]
print('after E1      %.6f' % q.active.mean())"
```

---

## D18 — NEW, CRITICAL: a shipped structure is the wrong protein entirely

`11_structures/agonist_only_vs_ternary/8FZQ.cif` is not an opioid-receptor
complex. Its own `_struct.title` reads:

> 'Dehosphorylated, ATP-bound human cystic fibrosis transmembrane conductance
> regulator (CFTR)'

One chain, ~1,152 C$\alpha$, ATP and Mg bound. It is CFTR — an ABC transporter,
not a GPCR.

The directory it sits in is meant to hold the agonist-only versus ternary
contrast, which is the most on-thesis structural comparison in the entire drop:
it is the visual form of Beat 1's finding that agonist-bound structures without a
transducer do not form the NPxxY network. **That render cannot be built.** The
companion file 6PT2 is correct but has nothing to contrast against.

Every other CIF in the drop was checked against its own title and is what it
claims to be.

**Action**: request the correct δOR ternary structure. Until then the
agonist-only comparison exists only as a sentence, not as a figure.

---

## D19 — NEW: templates-off and MSA-pinning have no row-level evidence

`block_a_rows.csv` has **no column recording template usage or MSA
configuration** — not one, across 55 columns.

For templates, the claim sheet is candid about this. SC-9's own qualifier reads:
*"no row-level echo (evidence class b + c + d, not a); `_status.json.runtime_config`
echo landed post-Block-A."* The claim rests on launcher static analysis,
source-code defaults and a propagation test — good evidence, but not per-row
provenance.

For MSAs there is no claim at all. **No surviving claim asserts MSA pinning**,
and nothing in the drop records it. My Methods draft asserted "multiple sequence
alignments were pinned" as fact. That was unsupported and is now corrected to
state what is actually evidenced and what is not.

This matters because templates-off is load-bearing: an active-state template
would be oracle route 1, and the whole design depends on its absence.

---

## D20 — every ALIGNMENT.md file in the drop carries at least one wrong identifier

**Widened 2026-09-10.** This was "two further ALIGNMENT.md files name wrong
anchors", and the report's summary said four of the drop's files were known to
be wrong. Once chain identifiers, measured values and file lists are all
checked, it is **eight of eight** — see the Block A audit's N13 (three files
name chain A as the receptor where chain A is Gα), N14 (residue numbers that do
not exist in the file beside it), N15 (kink angles contradicting the shipped
table) and N16 (a file listed that is not in the drop). No ALIGNMENT file in
this drop should be trusted for an identifier, a value or a filename.

### The two that started this entry

Same failure class as D13, found by recomputing every anchor against the tidy
values before drawing it:

- **ACM1**: NPxxY anchors are Y208/Y418, not the Y213 the file gives; the tilt
  anchors are L67/L367, which the file does not name at all.
- **DRD2**: Y209/Y426, not the Y208/Y399 in `success_case/ALIGNMENT.md`.

Four of the drop's ALIGNMENT files are now known to be wrong. **Treat all of them
as unreliable** and recompute anchors from coordinates against the tidy
distances. `figures/block_a/cifread.py:verify_anchor` does this and refuses to
return a distance that does not reproduce the shipped value.

---

## D21 — NEW: ADRB2's ΔNPxxY is against a different reference than assumed

The shipped ADRB2 ΔNPxxY of $-6.581$ Å is computed against the **median**
inactive reference (3NYA), not against 2RH1. The pairwise 4LDE$-$2RH1 value is
$-6.660$ Å. Printing $-6.581$ on a 4LDE/2RH1 render would attach a number to a
pair it was not measured on.

Related, and a practical trap: **4LDE carries a $+1000$ auth-numbering offset**,
and 2RH1's T4L fusion occupies residues 1002–1161. A single selection string
across both objects will align the receptor onto the lysozyme. Write the two
selections separately.

---

## D22 — NEW: `rmsd_to_active_ref` does not reproduce from the coordinates

Row 8285 (DRD2 / OpenFold3 / cognate) ships `rmsd_to_active_ref = 1.218` Å.
Recomputed over all 269 shared receptor C$\alpha$ (residues 34–441) against
7JVR it is **1.2952 Å** over all 269 shared Cα — a 6% difference, and no
trimmed window reproduces the shipped value; the closest any trim gets is
1.2456 Å.

**Corrected 2026-09-10.** This previously read "excluding ICL3 gives 1.290,
7TM-only 1.298, 34–420 gives 1.290". Those three windows are not distinguishable
here: 7JVR's ICL3 (226–365) is unresolved in the reference and is therefore
already absent from the 269 shared Cα, so "excluding ICL3" removes nothing. The
conclusion is unchanged — 1.2952 against a shipped 1.218, and nothing
reproduces — but the three figures were not measuring what the sentence said.

**The scorer's atom set is documented nowhere in the drop.** No file describes
which atoms enter the superposition or the RMSD.

This is not a large discrepancy and nothing in the manuscript turns on it, but
it means a shipped RMSD cannot be reproduced from the shipped coordinates, which
undercuts the archive's own reproducibility claim. Figures that quote it now do
so **as a selection statistic only**, printing the independently computed value
beside it and labelling both.

**Request**: the atom selection used by the scorer for `rmsd_to_active_ref` and
`rmsd_to_inactive_ref`. One line of Methods, no compute.

---

## A defect in our own code, recorded here because it affected shipped figures

`figures/block_a/camera.py` fits the membrane normal to **every** C$\alpha$ in
the receptor window. DRD2's predicted ICL3 is 147 residues of mean-pLDDT-38.5
coil out of 414 (the rest of the receptor averages 86.0), and fitting the axis
through it **bent the camera by 35.5°** on every DRD2 render shipped before
2026-09-10. The function's own docstring warned that the loop could flip the
extracellular *sign*; that it also bends the axis was not caught.

Fixed in `figures/dofrender.py:camera_frame`, which takes the point cloud
explicitly, with every scene passing the 7TM body and excluding ICL3. All
affected renders have been rebuilt. `camera.py` itself is unchanged because S10
still uses it, and the caveat is noted at its call site.

---

## Recommended sequence

D1, D2, D3 and D5 change the wording of Beats 3, 4 and 5 and the CIs on Beat 2,
so all four must be settled with the PI **before any panel is drawn** (brief §4
preamble). D6 changes one table and one sentence. D7 and D8 are corrections to
make in passing.

None of these is a defect in the shipped data. In every case the tidy files are
internally consistent and the claim sheet has drifted from them — which is the
expected direction, and the reason the archive ships tidy files at all.
