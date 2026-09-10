# Block B — discrepancy report

`verify_claims.py` recomputes every checkable number in the Block B claim sheet,
the drop README and the structure addendum from the shipped tidy files.

**91 checks. 76 reproduce. 15 do not, in 5 groups.**

The data wins over the claim sheet, always. Nothing here is repaired in the
drop; `data/block_b/` and `data/block_b_structures/` are `chmod a-w`.

Four further checks failed on the first run and were **my** bugs, not the
drop's — fixed before this report was written, and named here so nobody
re-reports them: I matched `role.str.contains("active")`, which also matches
`inactive`; I looked for the pooled stratum under `panel` when the 2×2 table
labels it `panel_all`; I read SC-B-6's native-only split from the residuals
summary when it lives in `phase5_power_analysis.csv`; and I compared C-B-7's
*per-backbone* 24–34 range against an all-backbone total. Block A's checker
false-positived three times in the same way. Run the anomaly down before
calling it a finding.

---

## D-B-1 — The claim sheet mislabels three of the four exclusion flags

**Severity: high. This one silently produces the wrong figure.**

| flag | claim-sheet header says | `exclusion_definitions.csv` and the data say | rows |
|---|---|---|---|
| `excl_E_B_1` | all-NaN NPxxY (EDNRA, EDNRB, GRPR, HRH3) | same | 3,200 ✓ |
| `excl_E_B_2` | **AA2AR** | **OPRD, CNR1** — agonist-only active reference | 1,600 |
| `excl_E_B_3` | **non-native active reference, 15 of 40** | **AA2AR alone** | 800 |
| `excl_E_B_4` | **ceiling-pinned cells (cognate rate ≥ 0.98)** | **non-native active reference, 15 receptors** | 12,000 |

The drop's own `README.md` row counts (1,600 / 800 / 12,000) agree with the
**data**, not with the claim sheet header. So the header is the odd one out.

It propagates into individual claims, inconsistently:

- **SC-B-6** names *"E-B-3 (non-native active references)"* as its load-bearing
  exclusion. Under the data's labelling, E-B-3 is AA2AR — one receptor, not the
  15 the native-only re-run needs.
- **SC-B-11** names *"E-B-2 (AA2AR)"*. Under the data's labelling, E-B-2 is
  OPRD + CNR1.
- **SC-B-14** names *"E-B-4 (native-only)"*, which is correct against the data
  and contradicts its own document's header.
- **SC-B-2** names *"E-B-4 (ceiling-pinning)"*, which matches the header and
  contradicts the data.

**Corrected 2026-09-10.** An earlier version of this section said "there is no
ceiling-pinning flag anywhere in the drop". That was wrong, and it was wrong
because I grepped the columns of `rows_tidy.csv` only. The flag exists as
`ceiling_pinned` in `04_ladder/ladder_per_receptor.csv`, it fires on 115 of 160
cells — **29 / 28 / 24 / 34** by backbone — and it reproduces exactly from the
predicate. C-B-7's stated 24–34 is that table, not a range. My own script had
printed those four numbers; I transcribed the first two as "28–29".

What survives is smaller and still real: the claim sheet's header calls the
ceiling-pinning set **E-B-4**, and `excl_E_B_4` is the non-native set. The
quantity is shipped, under a different name, in a different file. A panel that
"applies E-B-4" still gets the non-native set.

**What we will do.** Refer to exclusion sets by their **membership**, never by
their E-B-n label, in every caption and every sentence. Where a claim needs the
non-native restriction, say "the 20 of 24 receptors whose active reference is
native" and filter on `active_stabilization_source`, which is unambiguous.

**Recommended wording.** None — the labels do not reach the reader. This is a
plumbing hazard, and the fix is that no panel script ever writes `excl_E_B_3`.

---

## D-B-2 — SC-B-1's eight continuous medians do not reproduce, and a column vouches that they do

**Severity: high. The dispatch asks us to LEAD with these numbers.**

Dispatch §2.3: *"Lead with the continuous distributions and predicate rates; the
fractions go in a table, not in the lead sentence."*

The four **binary** rates reproduce exactly: 0.158 / 0.558 / 0.809 / 0.891, from
`ladder_four_scorings.csv` and independently from `rows_tidy.csv`. Those are
sound.

The eight **continuous** medians do not, under any aggregation:

| axis | arm | claim sheet | pooled rows | median of per-receptor | mean of per-receptor | median of the 4 backbone p50 |
|---|---|---:|---:|---:|---:|---:|
| NPxxY-OH | apo | 11.30 | 10.15 | 10.23 | 10.29 | 10.21 |
| NPxxY-OH | decoy | 8.19 | 6.26 | 5.41 | 6.80 | 6.31 |
| NPxxY-OH | shuffled | 7.31 | 4.34 | 4.24 | 5.06 | 4.41 |
| NPxxY-OH | cognate | 6.60 | 4.29 | 4.28 | 4.65 | 4.40 |
| tilt | apo | 13.05 | 12.22 | 12.13 | 12.86 | 12.22 |
| tilt | decoy | 15.61 | 16.81 | 16.72 | 15.91 | 16.57 |
| tilt | shuffled | 16.42 | 17.69 | 17.73 | 17.64 | 17.66 |
| tilt | cognate | 16.75 | 17.53 | 17.57 | 17.56 | 17.53 |

The miss is systematic and directional: every claim-sheet NPxxY value is
**higher** than the data and every claim-sheet tilt value on the three partner
arms is **lower**. That is the signature of a different corpus, not of an
aggregation choice — the shipped values describe a *less activated* population
than the one shipped. frame_40 gives the same answer to two decimals, so it is
not the frame either.

Two aggravating facts:

1. `claim_answers.csv` names `ladder_continuous_distributions.csv` as the source
   of all eight. **That file has no panel row** — only the four per-backbone
   strata. The cited source cannot produce a panel median at all.
2. The same file carries `matches_claim_sheet_bool = True` on all eight.

That second point is Block A's failure class recurring verbatim: a
self-certifying column that reads `True` where the value disagrees. It was
`matches_claim_sheet` in Block A and `matches_claim_sheet_bool` here.

**What we will plot.** The recomputed values, per-backbone, with the pooled row
median stated as the panel figure and the aggregation named on the panel.

**Recommended wording.** Lead the Results on the **binary ladder**, which
reproduces, and give the continuous axes as *direction and separation* rather
than as quoted medians until the discrepancy is resolved upstream. A
`[NUMBER NOT IN BUNDLE]`-style flag is not right here — the numbers are in the
bundle, they just do not reproduce from it.

---

## D-B-3 — The NPxxY threshold ships as 9.08, not 9.082

**Severity: low, but it is the second block in a row.**

The claim sheet and the drop README both state the predicate as
`d_npxxy_y558_y753_oh < 9.082 Å`. Every one of the 32,000 rows carries
`threshold_npxxy_oh_active_lt = 9.08`.

Block A had the same truncation and it is already recorded in our Methods. The
0.002 Å difference cannot move a call at this precision, but the paper must
quote **one** number and it should be the one the rows carry.

**Recommended wording.** Quote 9.08 Å, as Block A's Methods already does, and
note once that the claim sheet's 9.082 is the untruncated value.

---

## D-B-4 — The structure addendum's two depth numbers are GHSR-only, presented as general

**Severity: high, because the addendum requires the prose to state them.**

Addendum §3 gives a table headed *"Median α5-CT tip depth in the C2 subset"* —
Boltz 18.81 Å, Chai 12.46 Å — and says *"The cognate median depth is 12.3–12.6
Å."* It then requires: *"The Results prose must state this, in substance."*

Read panel-wide, neither reproduces:

| quantity | addendum | panel-wide | GHSR only |
|---|---:|---:|---:|
| C2 median tip depth, Boltz | 18.81 | **14.62** | **18.81** |
| C2 median tip depth, Chai | 12.46 | 12.43 | 12.46 |
| cognate median tip depth | 12.3–12.6 | **12.19** (SC-B-3's own figure) | 12.34–12.63 |

Both are **GHSR-only** figures, and both reproduce exactly when read that way.

The addendum is written about a GHSR bundle, so the numbers are not wrong — the
scope statement is missing. And it matters more here than it would elsewhere,
because **§2 of the same document warns against exactly this**: *"Do not build a
'ladder made visible' panel from these four structures… GHSR was selected for
its dense engaged-but-inactive population, and that same property makes its
ladder unrepresentative."* §3 then quotes GHSR's depths without the same
qualifier.

Panel-wide the honest statement is different in substance. At 14.62 Å against a
cognate 12.19 Å and a 20 Å cutoff, the C2 population sits about 2.4 Å shallower
than cognate — not "near the permissive edge of the cutoff."

**Recommended wording.** State the depth constraint for GHSR, named as GHSR,
alongside the panel figure. The addendum's underlying instruction — print the
actual depth in Å on every C2 panel and never label a structure "engaged"
without it — stands regardless and we will follow it.

---

## D-B-5 — The shipped Boltz C2 structure is at the 90th percentile of its own panel subset

**Severity: medium. It is the structure the addendum designates for the primary panel.**

`03_engagement_trio/C2_decoy_engaged_but_inactive/b899e22eaced.cif` sits at
**18.730 Å** tip-to-R3.50.

- Against **GHSR's own** Boltz C2 rows (n=12): the **50.0th percentile**. A
  proper median pick, exactly as the manifest's selection rule states.
- Against the **panel's** Boltz C2 rows (n=603): the **89.9th percentile**.

So the selection is sound on its own terms and unrepresentative of the panel in
the shallow direction. A reader shown this structure sees a partner less
inserted than nine out of ten engaged-but-inactive predictions.

Note also that the cell this structure comes from has `cell_tip_median` =
20.97 Å, which is **above** the 20 Å engagement cutoff — the representative row
is engaged while its cell's median is not.

**What we will do.** Any panel built on this structure prints its 18.73 Å depth,
names GHSR, and carries the panel-wide C2 median beside it. The addendum's
instruction not to adjust the camera to make the α5 look more inserted is
right, and this is why.

---

## What reproduces, which is most of it

Worth stating plainly, because the headline is sound and four of the five groups
above are about scope and labelling rather than about the result.

- **The ladder**: 0.158 / 0.558 / 0.809 / 0.891 on frame_36, and monotonic on
  all four backbones independently. Not 0.552.
- **The decomposition**: +0.400 / +0.252 / +0.082 probability, 54.6 / 34.3 /
  11.1 %; +1.907 / +1.214 / +0.656 logit, 50.5 / 32.1 / 17.4 %.
- **The 2×2**: all three (arm, p_engaged, p_active|engaged) triples, and the
  engaged-but-inactive floor at 1,699 rows pooled, 278–540 per backbone.
- **The PIF connector**: all five subset medians and all five cell counts,
  including decoy engaged-but-inactive at 15.42 Å on 47 cells.
- **SC-B-6**: +0.024 [−0.29, +0.30] on all 24, −0.062 [−0.41, +0.21] on the 20
  native, CI spanning zero — Outcome A signed, not an equivalence result.
- **The reference audit**: 25 / 10 / 3 / 2, 15 non-native = 37.5 %, and **zero
  native heterotrimeric Gs anywhere in the Class A active set**, which is the
  Methods sentence the dispatch asks for.
- **Grid completeness**: 32,000 rows, 640 cells, exactly 50 rows and 5 seeds
  each, no sentinel seed, one scorer SHA, one pinned reference-set SHA.
- **GHSR's own decoy rate**: 0.175 against the panel's 0.558 — the addendum's
  §2 warning is correct and quantified.
- **Every predicted CIF**: 11 of 11 hash to their filename stem.
