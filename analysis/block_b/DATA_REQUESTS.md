# What Block B still needs from the pipeline

Paste-ready for the coding agent that owns the HPC runs. Ordered by whether a
sentence now in `manuscript/` depends on the answer, not by effort. Every
"current state" line was recomputed from `data/block_b/` today against the
shipped tables; the drop itself was never modified.

**Read `rebuttals/BLOCK_B.md` first.** R1–R10, Q1–Q9 and S1–S9 are already
written and unsent. This document does not restate them. Where an ask below
touches one, it says so and says what it adds. Twelve of the seventeen asks
here are **not** in that file.

**The drop is internally complete.** All 103 files in `MANIFEST.json` are
present, every sha256 matches, every `row_count` matches. Nothing the manifest
promised is missing. Every gap below is a gap in a *column*, in *precision*, in
*documentation*, or in a file the prose cites that was never part of the zip.

Cost classes: **free** = re-analysis of data already held · **cheap** =
re-scoring existing predictions, no new inference · **real** = new predictions.

---

# Rank 1 — a manuscript sentence depends on the answer

## 1. Re-emit `threshold_npxxy_oh_active_lt` at full precision — **free, and the cheapest correction in this document**

**Why.** `methods.tex:309-311` currently says the NPxxY threshold is applied
"at the value the rows carry (9.08 Å)". That sentence rests on a rounding
artefact, and the number is wrong.

`01_rows/rows_tidy.csv` carries the literal string `9.08` on all 32,000 rows —
three significant figures. Every other document says 9.082. R3 and D-B-3
recorded the conflict and could not settle it. It is now settled, by
recomputation:

| threshold | panel decoy rate, frame_36 | shipped | `ladder_per_receptor.csv` cells disagreeing |
|---|---|---|---|
| 9.08 | 0.557778 | 0.557917 | **1 of 640** (AA2AR / chai / decoy) |
| **9.082** | **0.557917** | 0.557917 | **0 of 640** |

Exactly 5 rows sit in [9.080, 9.082), and they are what moves the decoy rate.
**The shipped aggregates were all computed at 9.082; the row column is a
rounded export that reproduces none of them.** Anyone who recomputes the
predicate from the column alone — which is what the column is for — gets a
different SC-B-1 headline number.

**What we need.** `threshold_npxxy_oh_active_lt` re-emitted at the full stored
precision, plus one sentence confirming 9.082 is the operative value and how it
was derived. `threshold_gpcrdb_tm6_tilt_active_gt` (14.932) is unaffected.

**Unblocks.** SC-B-1, `methods.tex:309-311`, `results.tex:242-246`.
**Promised?** Yes — `DATA_DICTIONARY.md` documents the column as the pin for
the predicate. **Cost: free.** Refines R3 / D-B-3, which are now answerable.

---

## 2. Unseal the eight active references that were audited but never scored — **cheap, highest value**

**Why.** `09_references/reference_audit.csv` names a specific active-state PDB
for eight receptors and marks each `ref_source = sealed`:

| receptor | active PDB | stabilisation |
|---|---|---|
| ACM1 | 6OIJ | chimera |
| ADA2A | 9CBL | native |
| ADRB1 | 7BU7 | nanobody |
| CCKAR | 7MBX | native |
| DRD3 | 8IRT | native |
| OX2R | 7L1V | mini_G |
| EDNRA | 8HCQ | mini_G |
| HRH3 | 8YUU | native |

**Zero of the eight appear in `reference_set.blockb_pinned.csv`**, the pinned
bytes every row was scored against. All 72 `ref_source = pinned` rows are in
it; all 8 sealed rows are not. The consequence is exact and measurable:
`receptor_d_active_ref`, `delta_to_active` and `rmsd_to_active_ref` are NaN on
**every one of those receptors' 800 rows**.

EDNRA and HRH3 are already gone under E-B-1, so unsealing buys six receptors:
**4,800 of 28,800 frame_36 rows — 16.7% — currently cannot be measured against
an active reference at all.** Every active-anchored Block B statement is on 30
receptors, not 36.

This bears directly on a live sentence. `residual_delta_to_active` is one of
SC-B-6's three axes (`results.tex:309-315`), and it is null for those six.

**What we need.** The eight PDBs entered into the pinned reference set and the
32,000 rows re-scored against it — or, per receptor, an explicit statement of
why the reference was sealed and must stay sealed. The second answer is nearly
as good: it converts an apparent hole into a documented boundary we can write
one sentence about.

**Unblocks.** SC-B-6, SC-B-13, `results.tex:309-315`; restores 4,800 rows to
`delta_to_active` / `rmsd_to_active_ref`.
**Promised?** No — the drop discloses the seal but never flags the cost.
**Cost: cheap** (re-scoring; the structures are named and the scorer exists).

**Cross-block note.** `analysis/block_a/DATA_REQUESTS.md` §2 asked for active
references for these same eight receptors, phrased as "does a structure exist?"
The Block B drop **answers that question — yes, with PDB IDs — and still did
not score them.** The ask is now much cheaper and much more concrete than when
Block A filed it. Not in `rebuttals/BLOCK_B.md`.

---

## 3. Recover `rmsd_to_inactive_ref` for the same six receptors — **cheap, independent of ask 2**

**Why.** This one needs no new reference at all. For those 4,800 rows,
`receptor_d_inactive_ref` and `delta_to_inactive` are **fully populated** — the
inactive reference is present and was used. But `rmsd_to_inactive_ref` is NaN
on all 4,800, with `rmsd_note = no_ref_pair_for_<RECEPTOR>`.

The RMSD job evidently requires a *pair* of references and skips the receptor
entirely when the active side is missing, discarding an inactive-side RMSD it
had everything it needed to compute. That is a job-control gap, not a data gap,
and it is fixable today whether or not ask 2 is granted.

**What we need.** `rows.rmsd.csv` regenerated with the pairing requirement
relaxed to per-role: emit `rmsd_to_inactive_ref` wherever an inactive reference
exists, `rmsd_to_active_ref` wherever an active one does, independently.

**Unblocks.** Any RMSD-anchored Block B statement on 36 rather than 30
receptors; the `rmsd_to_inactive_ref` row of
`04_ladder/ladder_continuous_distributions.csv`, currently n=1600 with n_nan=400
in every cell.
**Promised?** The dictionary documents the column with no NaN convention for
this case. **Cost: cheap.** Not in `rebuttals/BLOCK_B.md`.

---

## 4. Ship the two Phase 0 documents behind SC-B-7 — **free**

**Why.** SC-B-7 is the templates-off claim. The dossier calls it *"load-bearing
for the entire prospectivity framing"* and `methods.tex:336-342` states it as
fact. Its only cited evidence is:

- `docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md §0d`
- `docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md §4a–§4d`

**Neither is in the drop, and no shipped CSV carries template state on any
row.** C-B-1 already concedes the evidence is class (b)+(c) — launcher static
analysis and upstream defaults — not a per-row runtime echo. But we cannot even
read the class (b) evidence: the sweep of 20 job-status records exists only as
a claim in a file we do not have.

**What we need.** Both markdown files. If the 20-file sweep has a tabular
output, that too. This is a copy, not a computation.

**Unblocks.** SC-B-7, `methods.tex:336-342`.
**Promised?** Yes — cited as "Source docs" in the claim sheet.
**Cost: free.** Not in `rebuttals/BLOCK_B.md`.

Eighteen distinct `docs/BLOCK_B_DOSSIER_PHASE_*.md` paths are cited across the
narrative and none is shipped; see ask 16 for the rest. These two are pulled
forward because a Methods sentence rests on them.

---

## 5. The compute driver for the pocket-Cα table — **free**

**Why.** `results.tex:337-341` states that AA2AR's pocket-Cα reference
separation is 1.62 Å and ranks 34th of 40 — the number that closes out the
AA2AR anomaly (C-B-8). Its source,
`08_covariates/reference_separation_pocket_ca.csv`, is shipped. Its generator
is not:

> "**Compute driver**: `/tmp/compute_pocket_ca_rmsd.py` (session-scratch, not
> committed)." — `12_narrative/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md` §6

A number in Results whose recipe was written to `/tmp` and lost is a number we
cannot defend if a referee asks how the pocket was defined. The table's own
columns do not help: `n_pocket` is 12 on all 40 rows, `status` is `ok` on all
40, and `pocket_missing` is entirely NaN — so the file records no selection rule
and no failure mode.

**What we need.** The script, or the twelve pocket BW positions and the
superposition selection written out.

**Unblocks.** `results.tex:337-341`, C-B-8.
**Promised?** No. **Cost: free.** Not in `rebuttals/BLOCK_B.md`.

---

# Rank 2 — no sentence depends yet, but a claim we want does

## 6. The isolated 21-mer arm — specification for **S2**

**Why this sits here and not at the top.** No manuscript sentence depends on
it, because the manuscript is currently honest about not having it.
`results.tex:239` says "no arm supplies an isolated peptide, and no arm carries
an orthosteric ligand", and `methods.tex:291-293` says "the α5 C-terminal
21-mer is a region we measure and draw, not an input in either campaign". Both
sentences are true. By the ranking rule they place this ask low; by consequence
it is the most important thing in the file, because it is the paper's title.

**What Block B actually supplies — measured, not inferred.** From
`06_interface/interface_continuous.csv`, `n_partner_aa` over all 640 cells:

| arm | partner | residues | chains | n cells |
|---|---|---|---|---|
| apo | none | **0** | 1 (receptor) | 160 |
| decoy | cognate Gα, last 11 residues permuted | 350 / 354 / 359 / 394 | 2 | 160 |
| shuffled | a wild-type Gα of the **wrong** family | 354 / 377 / 394 | 2 | 160 |
| cognate | the receptor's wild-type Gα | 350 / 354 / 359 / 394 | 2 | 160 |

**Minimum partner length on any non-apo row is 350 residues. The maximum is
394. There is no arm below 350 and no arm at 21.** Decoy length equals cognate
length for 40 of 40 receptors (the scramble is a permutation); shuffled length
differs from cognate for 40 of 40 (it is a different subunit). `ligand_type`,
`ligand_sequence` and `ligand_smiles` are null on 32,000 of 32,000 rows.

**And the unit is 11, not 21.** Every construct document defines the α5-CT as
the *last 11 residues* — `α5-CT (last 11)` in the class table, `decoy[:-11] ==
cognate[:-11]` in the verification, and the shipped column is literally named
`partner_tail11_helicity_frac`. Block B does not manipulate a 21-mer anywhere,
in any arm, at any point.

**What would have to be added for the title's claim to become testable.** One
new arm, specified:

- partner chain = Gα residues **334–354** of the receptor's cognate subunit
  (the 21-mer), supplied **alone** as chain B, no scaffold;
- the same 40 receptors × 4 backbones × 5 seeds × 10 samples = 8,000 rows, so
  the arm slots into the existing ladder without a denominator change;
- scored on the identical predicate and the identical pinned reference set, so
  the new rung is comparable to apo / decoy / shuffled / cognate;
- `n_partner_aa` emitted per cell so the arm can be verified as 21 from the
  data rather than from the dispatch note.

The claim becomes testable when that arm sits between apo and cognate on the
same ladder. Without it, the title's first clause has no evidence in any landed
block, which is what `CLAIMS.md:66` already records.

**Cost: real.** **Already asked as S2** in `rebuttals/BLOCK_B.md:450` — this
entry is the specification, not a second request. S1 (bulk control) and S3
(agonist arms) are the companion real asks and are also already filed.

---

## 7. `deposition_count` is constant and its regression ships NaN — **cheap**

**Why.** `08_covariates/ladder_height_covariates.csv` carries
`deposition_count = 2` on all 40 receptors, SD exactly 0 — every receptor has
precisely two references in the pinned set, because that is how the set was
built. A predictor with no variance has no slope, and
`ladder_height_regressions.csv` duly ships **NaN in all 10 of its
`deposition_count` rows** (5 backbone strata × 2 scales).

SC-B-11 certifies `any_predictor_ci_excludes_zero = False`. One of the four
predictors behind that certification was never testable. C-B-14 concedes the
point and defers it out of scope.

**What we need.** `deposition_count` re-derived from an RCSB-wide entry count
per receptor — total deposited structures, not references selected — and the
regression re-run. If that pull is not wanted, then the predictor should be
dropped from SC-B-11's denominator rather than reported as a null.

**Unblocks.** SC-B-11, C-B-14. **Promised?** C-B-14 names it as a future item.
**Cost: cheap.** Adjacent to R6, which found 7 of 80 regression rows *do*
exclude zero; this is the complementary defect — a row that could not have.

---

## 8. Bootstrap draws for `all_40` decomposition — **free**

**Why.** `05_decomposition/ladder_decomposition.csv` ships 30 `all_40` rows,
each with a populated `ci_lo` and `ci_hi`. But `frame` is constant
`reproduction_36` on all 30,000 rows of
`ladder_decomposition_bootstrap_draws.csv`. **The `all_40` intervals exist with
no draws behind them in the drop.** We cannot reproduce them, check their
convention, or state their cluster count.

**What we need.** The `all_40` draws, or a statement that the `all_40` CIs were
produced by a different method — in which case, which.

**Unblocks.** SC-B-2 sensitivity; any frame_40 companion to the decomposition.
**Promised?** The dictionary documents the draws file as "1,000 draws × 3
contrasts × 2 scales × 5 backbone strata" with no frame restriction — 30,000
rows is exactly one frame's worth, so the count is right and the coverage is
half what the text implies. **Cost: free.** Not in `rebuttals/BLOCK_B.md`.

---

## 9. A join key on `donor_class_residuals.csv` — **free**

**Why.** The dictionary documents this 32,000-row file as beginning with
`input_sha256`. It does not have it. Shipped columns are:

```
receptor, arm, backbone, donor_ga_class, cognate_ga_class, cluster_id,
row_tilt, row_npxxy_oh, row_delta_to_active, ref_tilt, ref_npxxy_oh,
ref_source, residual_tilt, residual_npxxy, residual_delta_to_active
```

There is no per-row identifier of any kind — no sha, no seed, no sample index.
The 32,000 rows are keyed only by (receptor, arm, backbone), which identifies
640 cells of 50 indistinguishable rows. **The residuals cannot be joined back
to `rows_tidy.csv` row-for-row**, so no residual can be traced to the
prediction that produced it, and no residual can be cross-checked against the
pLDDT, the fold integrity or the exclusion flags on the same row.

`active_stabilization_source` is also documented for this file and also absent —
that is the native-vs-chimera label SC-B-6's stratification turns on.

**What we need.** `input_sha256` and `active_stabilization_source` added. Both
were present upstream; this is an emitter fix.

**Unblocks.** Any per-row audit of SC-B-6; the native-only stratum without a
second join.
**Promised?** Yes, explicitly, in `DATA_DICTIONARY.md`. **Cost: free.**
Not in `rebuttals/BLOCK_B.md`.

---

## 10. Bootstrap draws for statistics other than the median — **free**

**Why.** `07_donor_residuals/donor_class_residuals_bootstrap_draws.csv` is
documented as `draw_id, backbone, donor_ga_class, cognate_ga_class, axis,
statistic, value`. It ships `backbone, donor_ga_class, cognate_ga_class, axis,
draw_idx, median`. There is **no `statistic` column** — every one of the 180,000
draws is a median. No interval on a mean, a spread or a quantile can be
recomputed for SC-B-6 from what was sent.

**What we need.** Either the `statistic` column as documented, or a line in the
dictionary saying the median is the only statistic bootstrapped. The second is
free and may well be the honest answer.

**Cost: free.** Not in `rebuttals/BLOCK_B.md`.

---

## 11. The other seven native-Gs candidates — **free**

**Why.** `09_references/native_gs_curation_audit.csv` has 8 rows and a
`native_gs_alternative_available` column. It is populated on **exactly one**
row — `3SN6`, the ADRB2 alternative — and NaN on the other seven. So the audit
establishes that a native heterotrimer was available and not chosen in one
case, and is silent on whether one exists in the other seven.

S5 asks for the reference set to be re-curated to include native heterotrimers.
That ask cannot be actioned without the candidate list.

**What we need.** The column filled for all eight, or "none deposited" recorded
per row.

**Unblocks.** S5; `methods.tex:351-355`; SC-B-13.
**Cost: free.** Sharpens S5 rather than duplicating it.

---

# Rank 3 — table integrity; nothing depends on these today, all will bite the next block

## 12. Reconcile `matches_claim_sheet_bool` with what it certifies — **free**

**Why.** Across the nine `claim_answers.csv` files there are **101 rows, and
`matches_claim_sheet_bool` is `True` on all 101.** `ci_lo` and `ci_hi` are NaN
on 74 of them. The column has never once been observed to be `False`.

It certifies at least three groups that are independently known not to
reproduce:

- SC-B-1's eight continuous medians (D-B-2, R2). I tested these exhaustively:
  **no shipped geometry axis reproduces them under either frame.** All seven
  axes in `rows_tidy.csv`, pooled and per-backbone, closest miss 1.27 Å on the
  intended tilt axis and 2.97 Å on the intended NPxxY axis. They also cannot be
  read off `ladder_continuous_distributions.csv`, which has no pooled stratum
  at all — its `backbone` column holds only the four backbones, no `panel` row.
- SC-B-2's per-backbone family shares (D-B-6, R7).
- SC-B-11's `any_predictor_ci_excludes_zero = False` (R6).

**What we need.** Either the column recomputed against the shipped tables so it
can read `False`, or its removal. A boolean that vouches for numbers it has not
checked is worse than no boolean, because a figure agent will trust it.

**Cost: free.** Extends D-B-2 / R2 / R6 / R7 — the systemic point (one column,
never false, three disproven groups) is not in `rebuttals/BLOCK_B.md`.

---

## 13. One vocabulary for frame and pooled stratum — **free**

**Why.** The drop uses two names for each of two concepts, split across files:

| file | frame values | pooled backbone |
|---|---|---|
| `04_ladder/ladder_four_scorings.csv` | `all_40` / `reproduction_36` | `panel` |
| `05_decomposition/ladder_decomposition.csv` | `all_40` / `reproduction_36` | `panel` |
| `06_interface/interface_2x2.csv` | `frame_40` / `frame_36` | `panel_all` |

`FIGURE_BRIEF.md` compounds it: BB-1 says filter `frame == "reproduction_36"`,
BB-3 says `frame == "frame_36" AND backbone == "panel_all"`, and the brief's own
global rule says "every panel uses frame_36". A script that filters
`backbone == "panel_all"` against `ladder_four_scorings.csv` silently returns
zero rows.

**What we need.** One vocabulary, or a documented alias table.
**Cost: free.** Extends R8, which covers the cluster-count label; the
`panel` / `panel_all` split is separate and is not in the rebuttal.

---

## 14. Reconcile `DATA_DICTIONARY.md` with the shipped columns — **free**

**Why.** Nine files disagree with their own dictionary entry. Documented but
absent: `median` (it is `p50`), `input_sha256` and `active_stabilization_source`
(ask 9), `draw_id` / `statistic` / `value` (ask 10). Present but undocumented:
`n_nan` — which matters, because it is the column that keeps
`ladder_continuous_distributions.csv` honest about its own denominator — plus
the entire column set of `ladder_adjacent_pair_separation.csv`,
`ladder_threshold_proximity.csv`, `midpoint_ladder_28.csv`,
`interface_chai_plddt_inversion.csv` and
`donor_class_covariate_regression.csv`.

The dictionary also describes `donor_class_covariate_regression.csv` as a
regression "against `alpha5_donor_class`", but that column is populated on **2
of 80** rows of `reference_audit.csv` and 15 of 162 of the pinned set. The file
actually strata by `native` / `chimera`, which is a different and better-populated
column. See open question C.

**Cost: free.**

---

## 15. Figure-spec column names — **free**

**Why.** Four of the six `12_narrative/figures/BB-*.md` specs name columns that
do not exist in the CSVs they point at. BB-1 names
`binary_predicate_mean` / `_ci_lo` / `_ci_hi` / `logit` against a file whose
columns are `binary_predicate` / `cluster_boot_ci_lo_binary` /
`cluster_boot_ci_hi_binary` / `logit_active_fraction`. BB-3 names
`n_active_engaged` and BB-4 names `bw_register`; **neither exists anywhere in
the drop.** BB-2 names `estimate` / `share` against `term_estimate` /
`term_share`.

SC-B-12 compounds this by naming the wrong file outright: it cites
`interface_pif_connector.csv` for the BW contact register, which lives in
`interface_continuous.csv` as `contact_register_last5_json`.

**Cost: free.**

---

## 16. The eighteen unshipped `docs/` dossier files — **free**

**Why.** Beyond the two in ask 4, the narrative cites sixteen more phase
reports, audits and plans that are not in the zip — including
`docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md` (the decomposition source),
`docs/BLOCK_B_CLAIM_AUDIT.md` (cited as documenting the denominator finding),
and `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`, the primary partner
sequence file every construct in the campaign is built from. Twenty `refs/`
paths are cited and exactly one is shipped.

None of this blocks a sentence today. It blocks every attempt to check one.

**What we need.** The `docs/BLOCK_B_DOSSIER_PHASE_*.md` set and
`refs/constructs_block_b/` in the next drop, or a statement that the zip is
deliberately self-contained and the citations should be stripped.

**Cost: free.**

---

## 17. Placeholder strings in `reference_audit.csv` — **cheap**

**Why, and a correction.** Three columns of the 80-row reference audit are
constant, and two of them are **not NaN as previously believed — they are
placeholder strings**, which is worse, because a script reading them gets a
non-null value and proceeds:

| column | value on all 80 rows |
|---|---|
| `method` | `"X-ray or cryo-EM (schema lacks explicit method column)"` |
| `resolution` | `"not tracked in reference_set schema"` |
| `construct` | `"wt"` |
| `missing_inactive_flag` | `False` |
| `alpha5_donor_class` | NaN on 78 of 80; `"Gq"` on 2 |

`construct = "wt"` on all 80 is asserted flatly against a reference set the drop
itself describes as "entirely mini-G/nanobody/chimera stabilised" — 15 of 40
active references are non-native by its own count. `07_donor_residuals/external_ruler.csv`
carries the same `construct = "wt"` on all 103 rows.

**What we need.** Real `method` and `resolution` per PDB from RCSB; `construct`
either populated truthfully or dropped; `alpha5_donor_class` filled or removed.

**Unblocks.** SC-B-13; the D-B-9 / R10 line of work.
**Cost: cheap** (RCSB API, 80 lookups). **Already asked as R10 ask 3** — the
correction this adds is that `method` and `resolution` are placeholder strings
rather than nulls, so R10's premise ("`resolution` is entirely NaN") should be
fixed before that document is sent.

---

# Not requested, deliberately

**The three real-cost arms.** S1 (a mass- and shape-matched non-Gα bulk
control), S2 (the isolated 21-mer), and S3 (agonist-only and agonist+cognate)
are the experiments that would close the paper's two unevidenced title clauses.
They are already filed in `rebuttals/BLOCK_B.md` and are not re-filed here; ask
6 gives S2 a specification and nothing more. Filing them twice would let the
pipeline team answer the weaker version.

**Class B and Class F.** Out of Block B by design (C-B-15), and the paper says
so. Four receptors each would not support a scope claim.

**Prospectivity.** Foreclosed by design; the date-stratified holdout is Block C
and has landed. Nothing should be asked of Block B here — though see open
question F, which is about a contradiction in the drop's own documents, not a
request for data.

**Chai's MSA-feature builder.** Q9 already asks whether a forced-MSA Chai rerun
is feasible. The code-inspection question behind it (C-B-2, Flag B-26) is a
question for whoever owns `chai_lab`, not a data request, and answering it does
not change a Block B number — SC-B-9 is already written as a three-backbone
claim.

**Block D.** The D2 nanobody arm is resolved and needs nothing.

---

# Open questions about the data itself

Not requests for new runs — places where I could not determine the answer from
the drop, and want to know rather than guess.

## A. Where did SC-B-1's eight continuous medians come from?

They reproduce from nothing I can construct. Not from either predicate axis, not
from the five descriptive axes, not under frame_36 or frame_40, not pooled and
not as a mean of per-backbone medians. The claimed values are monotone in the
right direction, which suggests a real computation on a different population
rather than a transcription error. The README warns that a pre-consolidation
snapshot put the decoy rate at 0.552 rather than 0.558 — **were these medians
computed against that same earlier snapshot?** Q2 asks for the recipe; this asks
which corpus.

## B. Why is `median_tm6_helicity_6_30_6_50` identical in all sixteen cells?

`06_interface/interface_fold_integrity.csv` reports exactly `0.9523809523809524`
— 20/21 — as the median for every arm × backbone combination, with `n` and
`n_with_tm6_helicity` both constant at 2000 and `median_chain_breaks` constant
at 0.0. The pass-rate column varies sensibly (0.941 to 1.000), so the underlying
per-row data clearly is not constant. A median pinned to the same 21-residue
window boundary in all sixteen cells is plausible but should be confirmed, not
assumed — any panel plotting it will show a flat line and a reader will ask.

## C. Which column does the native-vs-chimera stratification actually use?

The dictionary says `donor_class_covariate_regression.csv` regresses against
`alpha5_donor_class`. That column is populated on 2 of 80 audit rows and 15 of
162 pinned rows, all on the active role. `active_stabilization_source` is
well-populated (64 native, 17 mini_G, 7 chimera, 3 nanobody, 3 agonist_only, 1
DVL_DEP) and the shipped file's own columns are `n_native_rec` / `n_chimera_rec`.
I believe the analysis is correct and the dictionary wrong, but SC-B-6's
native-only stratum is load-bearing enough that I would rather be told.

## D. Is `reproduction_36` the same population as `frame_36`?

I get 28,800 rows and 36 receptors from both, and the ladder rates agree, so I
believe they are. But they are named differently in different files by the same
drop (ask 13), and Q8 asks the same thing. Recording it here because my
recomputation is what the Methods frame sentence now rests on.

## E. Which cluster map was used *during the run*?

C-B-13 says the 26-cluster paralog map was reconstructed on 2026-09-09, after
the campaign ran, and that no canonical on-disk map was found. Every published
Block B interval is anchored to that reconstruction. Under frame_36 it yields
**24** clusters, not 26 — the `bombesin` and `endothelin` clusters vanish
entirely with GRPR, EDNRA and EDNRB — yet every shipped interval is labelled 26.
Q5 asks whether an earlier map existed. The sharper question: **were the shipped
CIs computed on 26 clusters or on the 24 that survive the frame?** The label
says 26; the population supports 24.

## F. `block_b_freeze` is still `PENDING`, and two documents disagree about prospectivity

`README.md` says the freeze tag is "PENDING — annotated after this zip lands";
`MANIFEST.json` says `freeze_tag_pending: block_b_final`. So the drop has no
version identifier we can cite. Separately, `SEALED_REFERENCES.md` says Block B
is prospective per PREREG §11b while the README and dossier say prospectivity is
foreclosed by design. No Block B sentence currently claims prospectivity, so
nothing breaks today — but no sentence could be written either way until this is
settled. Both are Q4 and Q7; repeated here because they are the two that would
change what may be written.

## G. Was the CI-convention audit run or not?

`12_narrative/BLOCK_B_FOLLOWUP_E1_E4.md` closes with "No `ci_convention_audit.csv`
produced (E3 not run)." The zip ships
`11_bootstrap_draws/ci_convention_audit_sc_b_1.csv` plus a readme describing it
as Item 2 of the closeout dispatch. Two other closeout outputs —
`native_gs_curation_audit.csv` and `reference_separation_pocket_ca.csv` — are
likewise shipped but not indexed by the section READMEs that contain them.

The narrative layer appears to be one dispatch behind the data layer. That is
not itself a defect, but it means **the `12_narrative/` documents cannot be
trusted as an index of what shipped**, and we have been reading them as one.
Confirming which layer is authoritative would change how the next block is
intaken.
