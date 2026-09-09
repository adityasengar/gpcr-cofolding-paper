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

## D8 — NEW: the shipped `matches_claim_sheet` flag is itself unreliable

`03_aggregates/headline_by_backbone.csv` carries `matches_claim_sheet = True` on
all four rows, and the brief §2 describes this as verified. It is true for the
median shifts but **false for the fraction**, which differs by up to 0.019 (D6).
Do not use that column as evidence that a number is safe to quote.

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
**98** PDBs, and `reference_predicates.csv` splits those 98 as 45 active-role /
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
within") selects row **552**; and 567 is simply the highest-pLDDT row in the
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

## Not reproduced

One further mismatch was reported to me and **does not reproduce**: that
`*_active_rate_panel_mean` are pooled row rates differing from per-receptor means
by up to a factor of 2.9 (OF3 apo, 0.242 vs 0.083). Recomputing under E1+E2 on
the full panel gives OF3 apo pooled 0.241 and per-receptor mean 0.241 — the same
to three places. The reported figure is not reproducible as stated and is not
recorded as a discrepancy.

It did, however, surface a real and smaller anomaly: **Protenix cognate ships
0.871 where both the pooled rate and the per-receptor mean are 0.890.** That one
value differs from both candidate definitions and is unexplained. Flagged for the
PI rather than resolved here.

---

## Recommended sequence

D1, D2, D3 and D5 change the wording of Beats 3, 4 and 5 and the CIs on Beat 2,
so all four must be settled with the PI **before any panel is drawn** (brief §4
preamble). D6 changes one table and one sentence. D7 and D8 are corrections to
make in passing.

None of these is a defect in the shipped data. In every case the tidy files are
internally consistent and the claim sheet has drifted from them — which is the
expected direction, and the reason the archive ships tidy files at all.
