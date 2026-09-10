# What Block A still needs from the pipeline

Paste-ready for the coding agent that owns the HPC runs. Ordered by what each
item buys the paper, not by effort. Every "current state" line was recomputed
from `data/block_a/` today; the recomputation is in
`analysis/block_a/verify_claims.py`.

Nothing here blocks submission. Items 1–3 would each remove a stated weakness a
referee is likely to find on their own.

---

## 0. One prediction that makes the graphical abstract a real contrast — **cheapest win in this document**

**Why.** `11_structures/` ships exactly four prediction CIFs: one apo (AA2AR)
and three cognate (DRD2, ACM1 ×2). **No receptor has both arms.** So the
graphical abstract's before and after are two different receptors — AA2AR on the
left, DRD2 on the right — and it has to say so in frame. The population strip
underneath carries the real contrast, which is why the figure is still honest,
but a within-receptor before/after would be far stronger and is the first thing
a reader looks for.

**What we need.** *One* coordinate file: the median apo prediction for DRD2, or
the median cognate prediction for AA2AR. Either one turns the abstract into a
true within-receptor contrast. Median by the tilt axis, not best-scoring, with
the selection rule and the row's percentile stated.

**Cost.** One structure already computed — this is an export, not a run.

---

## 1. A positive control for the amplitude null — **highest value**

**Why.** Beat 4 is our load-bearing negative result: predicted shift does not
track reference separation. A null is only as strong as the reader's confidence
that the method could have detected the effect had it been there. The best
exemplar in our literature corpus pairs its null with a positive-control panel
in identical grammar, showing the same measurement detecting the same kind of
effect when it genuinely exists. We have no such panel and it is the first thing
a referee will ask for.

**What we need.** Any arm where predicted shift *should* track a known
magnitude, run through the identical regression. Candidates, cheapest first:

- **Same-receptor dose analogue**: if any receptor has references in more than
  two states (partial-agonist as well as full-agonist), regress predicted shift
  on the graded reference separation. Even 6–8 receptors would do.
- **Synthetic positive control**: regress predicted shift against a quantity it
  *must* track — e.g. the receptor's own apo-to-cognate shift measured on a
  second axis. Zero new compute; it demonstrates the regression machinery
  responds when signal exists.
- **Cross-family**: Class B receptors have larger TM6 excursions. If their
  reference separations span a wider range, the same regression on Class B (even
  underpowered, n=4) shows the predictor working where range exists.

**Deliverable.** Same columns as `amplitude_points.csv` plus an
`arm`/`control_type` label.

---

## 2. Active references for the eight sealed receptors

**Why.** `delta_to_active` is null for every row of eight receptors — ACM1,
ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R. Consequences we currently have to
disclose: the fraction is a median over **39** receptors rather than the panel's
40 (D15), and **610 of 4,866 predicate-active rows cannot be tested** against an
active reference at all, so the false-positive rate has to be quoted on 4,256
(D14). Both are honest but both are avoidable if references exist.

**What we need.** For each of the eight: an active-state PDB if one has been
deposited since the reference set was frozen, or an explicit statement that none
exists. The second answer is almost as good as the first — it converts an
apparent gap into a documented boundary.

**Deliverable.** Rows appended to `reference_set.csv` with
`ref_pdb_sha_active`, or a short list of "no active structure deposited as of
<date>".

---

## 3. Provenance of the state labels on the 80 tier-1 rows — **cheapest, no compute**

**Why.** This is currently a `[PI]` marker in Methods and it is the sharpest
methodological objection available against us. The thresholds are derived from
80 tier-1 crystallographic reference rows. Those rows carry activation-state
annotations. An instrument calibrated on a labelling cannot then adjudicate that
labelling. Published work confirms the concern is real: curated activation
labels are assigned from "GPCRdb annotations, structural criteria, and ligand
binding status" — ligand-binding status is not geometry — and an unsupervised
geometric index over 1,351 class A structures recovers entries whose state was
originally interpreted incorrectly.

**The question is binary and someone already knows the answer.** Were the 80
rows selected **by crystallographic tier**, with state labels attached only
afterwards? Or selected **by curated state label**? The first leaves the
instrument independent of the annotation and we say so in one sentence. The
second does not, and needs a different sentence.

**Deliverable.** One paragraph, or the selection script.

---

## 4. A genuine high-confidence failure case

**Why.** `11_structures/confidently_wrong/` does not contain one. Both the
shipped row and the row its own selection rule picks are **apo-arm** predictions
sitting 0.86–0.95 Å from the *inactive* reference — correct predictions, and the
predicate calls them inactive correctly (D12). Beat 5 argues that confidence at
whole-complex grain can mislead, and a structural companion showing a genuinely
confident wrong answer would carry that argument. We should not manufacture one.

**What we need.** A query over the full corpus, not the local export: rows with
high `plddt_at_anchors` that are far from the reference **they were meant to
reach** — i.e. cognate-arm rows far from active, or apo-arm rows far from
inactive. Currently `rmsd_to_inactive_ref` is populated, so this may be
answerable locally; if the answer is that no such row exists above a sensible
pLDDT threshold, **that is a publishable result in itself** and strengthens Beat
5 rather than weakening it.

**Deliverable.** `row_id`, arm, both RMSDs, `plddt_at_anchors`, percentile
within cell; plus coordinates for the top case if one exists.

---

## 5. Detection limit for the amplitude regression

**Why.** A bounded null is far harder to dismiss than an unbounded one. We can
say "no evidence of amplitude reproduction"; we cannot yet say "we would have
detected a slope of X".

**What we need.** A power calculation or a simulation: injecting a true slope of
0.25, 0.5, 0.75 and 1.0 into the observed predictor distribution, what fraction
of cluster-bootstrap replicates return an interval excluding zero? Reportable in
one sentence and one supplementary panel.

**Deliverable.** `slope_injected`, `power`, `n_receptors`, `axis`, `backbone`.

---

## 6. Widen the tilt predictor's range, or retire the axis

**Why.** The tilt axis cannot resolve amplitude and we say so. The cause is
restriction of range: across 32 Class A receptors the reference separation runs
only 2.29 to 7.86 Å, SD 1.17 Å, against NPxxY's SD of 5.22 Å over 28 receptors.
Two of four slopes go negative, which is not physically interpretable.

**What we need.** Either receptors whose reference pair shows a genuinely large
TM6 excursion, to extend the predictor's range, or confirmation that the
observed range is the biological range — in which case the axis is retired for
amplitude work permanently and we say so once, with the number.

---

## 7. Coordinates for the structural figures

**Why.** All 14 current figures are data plots. Zero renders. The literature
this paper sits in is 19% structure renders, and 68 of 78 surveyed papers carry
at least one.

**What we need**, for **one** Class A receptor with a large, clean apo→cognate
shift:

- the **median** prediction of the apo cell and of the cognate cell (median by
  `d_gpcrdb_tm6_tilt_246_637_ca`, not best-scoring), with the selection rule and
  each row's percentile within its cell;
- the same receptor's deposited active and inactive references;
- the α5-CT 21-mer coordinates **as supplied to the model**, so the rendered
  peptide is the input rather than a reconstruction.

**Deliverable.** Five coordinate files plus a `SELECTION.md` stating the rule.
Please make the rule *median*, not *best* — a best-of-cell render is selection
on outcome and will be treated as such.

---

## 8. Quantify the OpenFold3 seed dependence

**Why.** OF3 seeds are 5 outer × 5 inner after a seeding fix, so OF3 rows are
less independent than the other backbones'. We disclose this, and it qualifies
every cross-backbone comparison of correlation magnitude — including Beat 5,
where OF3 has the strongest confidence correlation of the four.

**What we need.** An effective sample size for OF3, or the within-outer-seed
variance component, so the qualification carries a number instead of a caveat.

---

## 9. Class B and Class F, if scope claims are wanted

**Why.** Eight receptors are excluded from every quantitative claim by E4. The
supplementary shows them descriptively. If we want to say anything about scope
beyond Class A, they need enough receptors to support it; four each does not.

**Lowest priority** — the paper is coherent as a Class A result and says so.

---

## Not requested, deliberately

Decoy and scrambled-partner arms, date-stratified holdout, and directional
control toward the inactive state all belong to later blocks and are named in
the Results as explicitly out of scope here. Adding them to Block A would blur
a boundary the write-up currently keeps clean.

---

# Open questions about the data itself

Not requests for new runs — questions about what we already have. Several affect
sentences currently in the manuscript.

## A. Is Block A a different campaign from the older export? *(most important)*

`data/predictions.csv` (17,568 rows) and `data/block_a/` (9,490 rows) **are not
the same experiments**:

- 28 of Block A's 48 receptors appear in the older export; **20 do not**
- **zero** shared prediction-path strings
- the older export has nine arms (apo, ligand, antagonist, α5_ct_fragment,
  α5_ct_variant, cognate_ga, shuffled_ga, decoy_scaffold, arrestin…); Block A
  has two (apo, cognate)
- the older export includes an `af2mm` backbone; Block A does not

So the repo holds two unrelated drops. This matters because **`RESULTS.md` and
`analysis/q.py` describe the older one**, and `analysis/fingerprint.py` watches
the older one. Nothing currently tracks whether Block A has gone stale.

**Questions.** Does the older export supersede, get superseded, or run in
parallel as a different block? Should `RESULTS.md` be split, or does Block A get
its own ledger? Is the older export still the basis of any claim we intend to
make?

## B. Provenance of the archive

Was `block_a_figure_data.zip` generated by a script, or assembled by hand? The
question is not idle: **`agonist_only_vs_ternary/8FZQ.cif` is CFTR** (D18), and
**four of the `ALIGNMENT.md` files name anchor residues that do not reproduce the
shipped distances** (D13, D20). Those are hand-assembly failure modes. If the
tabular data is generated and only the structure directory is hand-made, the
tables are trustworthy and the structures are not — worth knowing which.

Related: `headline_by_backbone.csv` carries `matches_claim_sheet = True` on all
four rows while the fraction disagrees by up to 0.019 (D8). **Which version of
the claim sheet was that column computed against, and by what?**

## C. Seeds are not paired between arms

Zero `seed_outer` values are shared between the apo and cognate arms on any
backbone: each cell draws its own 25 seeds. The apo→cognate comparison is
therefore paired **at the cell level and not at the seed level**.

Nothing in the manuscript currently assumes seed pairing, and the cluster
bootstrap does not require it. But if it was *intended* to be paired, the
within-receptor slopegraph and the permutation null both mean something slightly
different from what was designed. **Was unpaired seeding deliberate?**

## D. Three unexplained numbers

1. **Protenix cognate predicate rate ships as 0.871**, while both candidate
   definitions — the pooled row rate and the mean over receptors — give 0.890.
   No other backbone/arm cell disagrees with both. What is it?
2. **`n_receptors_fraction` is 40 but only 39 receptors carry a non-null
   fraction** (D15). Which receptor is counted but absent, and why?
3. **5G53 chain A** gives 18.124 / 3.716 Å against shipped 18.097 / 3.705 —
   consistent with the shipped value coming from the structure's second receptor
   copy. Confirm which copy is canonical. Nothing currently depends on it.

## E. Can the runtime config be back-attached?

SC-9 notes the `_status.json.runtime_config` echo "landed post-Block-A". If
those files still exist for these runs, attaching template and MSA settings
per row would convert D19 from a disclosed evidence-class caveat into a
row-level fact. That is the difference between "established by launcher static
analysis" and "recorded per prediction", and templates-off is load-bearing —
an active-state template would be oracle route 1.
