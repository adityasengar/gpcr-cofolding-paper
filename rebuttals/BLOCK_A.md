# Block A — rebuttals, questions, and suggestions

For the pipeline agent that produced `block_a_figure_data.zip`.

Verification here: `analysis/block_a/verify_claims.py`, 34 checks recomputed
from the shipped tidy files alone. 19 reproduce, 15 do not.

---

# 1. Rebuttals

*(In assembly. The 23 discrepancy groups in
`analysis/block_a/DISCREPANCY_REPORT.md` are being converted into entries with
tested reproduction commands, and an audit pass is looking for what the first
pass missed.)*

The five that would have put something false in the paper, in one line each:

- **`8FZQ.cif` is CFTR, not the opioid-receptor complex it is shipped as.**
- **The "confidently wrong" structure is confidently right** — the claim inverts.
- **SC-1's intervals headed "cluster-boot" contain the receptor-boot values**,
  which are narrower.
- **Every `ALIGNMENT.md` file in the drop — eight of eight — carries at least
  one wrong identifier**: anchor residues that do not reproduce the shipped
  distances, chain A named as the receptor where chain A is Gα, residue numbers
  absent from the file beside them, kink angles contradicting the shipped table,
  and one file listing a structure the drop does not contain.
- **No template or MSA column exists in the drop**, while the brief asserts both
  were pinned.

# 2. Questions

Already written and paste-ready in `analysis/block_a/DATA_REQUESTS.md` — ten
requests and five open questions, of which two block a Methods sentence today:

- **D9** — the reference-set denominator: 89 as previously stated, 98 empirical,
  167 total. Two `[PI]` placeholders sit in the manuscript because of it.
- **D19** — were the 80 threshold rows selected by crystallographic tier, or by
  curated state label? The first leaves the instrument independent of the
  annotation; the second does not, and would need saying in Methods. **Costs no
  compute. Someone knows.**

## Q-A1 — **How was the panel selected?** There is no rule anywhere in either drop.

**Severity: high, and it is the first question a referee asks.**

We searched both drops' READMEs and data dictionaries, `10_narrative/` and
`12_narrative/` in full, both claim sheets, both dossiers, and every `*.md` in
`11_structures/`. The only file named `SELECTION.md` is about which *prediction
row to render* in a figure — a good file, every pick rule-driven with
percentiles stated — and says nothing about which receptors enter the panel.

What we can verify: **all 40 Class A receptors have both an active and an
inactive deposited reference, 40 of 40.** So "both states solved" is almost
certainly the operative criterion. But that is inferred from the output, not
stated, and it leaves four things open:

1. Was the panel **every** receptor meeting that criterion, or a subset? If a
   subset, chosen how?
2. Was a resolution or method floor applied? `reference_audit.csv` has a
   `method` column and a `resolution` column, and **both hold a single
   placeholder string on all 80 rows** — `X-ray or cryo-EM (schema lacks
   explicit method column)` and `not tracked in reference_set schema`. They are
   non-null, so a `notna()` check passes on both and reports the columns as
   populated. Neither can be checked here, and nothing warns you of it.
3. Was any receptor meeting the criterion **excluded**, and why?
4. When was the selection frozen relative to the deposition record?

**Why it is not a formality.** "The effect holds across 40 receptors" means one
thing if those are *every* receptor with both states solved and something quite
different if they are a curated subset — a census versus a sample with an
unstated sampling frame. It also rhymes with something already established: the
reference set contains no native heterotrimeric Gs complex, which your own Item 1
verdict calls **a curation choice**. If the reference curation was a choice, the
panel selection was one too, and at present we can describe only one of them.

**To close.** The selection rule as it was applied, in one paragraph, including
anything excluded and why. If the rule was "every class A receptor with both
states in GPCRdb as of <date>", that sentence is all we need and it makes the
panel a census, which is the stronger claim.

A `[PI]` marker now sits in the manuscript's Panel subsection pending this.

---

# 3. Suggestions — what would make the paper stronger

Cost classes as in `README.md`: **free** (re-analysis of data already held),
**cheap** (re-scoring, no new inference), **real** (new predictions).

Three suggestions in `BLOCK_B.md` apply to both campaigns and are not repeated
here: **S1 a bulk control**, **S2 the isolated 21-mer arm**, and **S3 an
agonist** — neither block supplies a peptide or a ligand, and two of the
manuscript's three title clauses have no evidence in either.

## A1 — Scale the steric-exclusion observation. **real, but tiny.** The only mechanism in the paper.

Everything else in Block A is *what* the models do. This is the only measurement
that says *why* the co-input works: α5 heavy atoms fall within 4 Å of where TM6
sits in the deposited **inactive** structure on 52% and 39% of contacts, against
11% for the active structure and 2–4% for the prediction's own TM6. The partner
cannot be placed without displacing TM6 — a steric account, from coordinates,
that no paper in our 79-paper corpus offers.

It is at **n = 2 receptors**, and the active-structure control is not zero.

Extending it to the full panel needs coordinates, not new predictions — one
representative cognate structure per receptor, which is the same request as
item 7 of `DATA_REQUESTS.md`. At n=48 with the active control quantified, this
stops being an observation and becomes the mechanistic section the paper
currently lacks.

## A2 — Publish the anchor-versus-global confidence reversal as a recommendation. **free.**

Block A's confidence result is usually read as a negative: pLDDT does not track
state correctness. The more useful finding is buried inside it. Protenix2's
whole-complex correlation is **+0.33** — apparent overconfidence — and that
reversal **disappears entirely** at anchor grain (+0.07). OpenFold3 moves the
other way, from −0.26 to −0.63. A single pooled pLDDT correlation would have
produced two opposite and equally misleading conclusions on the same corpus.

That is a methodological recommendation the field can act on, from data already
held: *report confidence at the residues that define the state, not over the
complex.* It costs a paragraph and a panel, and it converts a null result into
an instruction.

## A3 — A positive control for the amplitude null. **real.** Already requested; restating why it matters.

The amplitude regression is the paper's most exposed claim: slopes of 0.04–0.37
against unity, three of four intervals including zero. As written, a reader
cannot distinguish *the models do not reproduce receptor-specific amplitude*
from *this regression could not have detected it if they did*. Item 1 of
`DATA_REQUESTS.md` asks for the control; without it the claim has to be softened,
and it is a claim worth keeping sharp.

## A4 — Retire or widen the tilt predictor. **free, and it is a decision, not an experiment.**

The tilt axis carries an SD of 1.17 Å across the regression set against NPxxY's
5.22 Å. A predictor with that little dynamic range cannot resolve a slope, and
we already say so on the panel. Either widen the receptor selection until the
axis has range, or report the tilt regression as an instrument property and stop
presenting it beside the NPxxY one as though the two were comparable tests.

## A5 — Report the exclusion sweep as a robustness figure, not a table. **free.**

Every headline statistic was recomputed under every exclusion combination and
nothing moved by more than 0.5%, with no sign flip anywhere. That is currently a
supplementary table. Given that `excl_any` removes 54% of the corpus and that
the exclusion semantics have now been mislabelled in **both** blocks' claim
sheets, a compact figure showing the headline surviving every combination is
worth more than the table — it answers the objection before it is raised.
