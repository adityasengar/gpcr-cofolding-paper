# What Block A still needs from the pipeline

Paste-ready for the coding agent that owns the HPC runs. Ordered by what each
item buys the paper, not by effort. Every "current state" line was recomputed
from `data/block_a/` today; the recomputation is in
`analysis/block_a/verify_claims.py`.

Nothing here blocks submission. Items 1–3 would each remove a stated weakness a
referee is likely to find on their own.

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
