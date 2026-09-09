# Coordinating with the lit session to finish Block A

Block A prose makes two different kinds of claim, and they have different owners.

**Claims about our data** — the shifts, the slopes, the correlations — are mine.
Every one carries a `[R-*]`-style locator into `data/block_a/` and is re-derived
by `analysis/block_a/verify_claims.py`.

**Claims about the field** — that this is novel, that prior work did not do it,
that a limitation is a known limitation of the field rather than of us — are the
lit session's. They carry `[citekey p.N]`. Block A currently contains several of
these, unsourced, and that is the gap this plan closes.

## The rule that has to come back

`CLAUDE.md` records honestly that the two-pass rule collapsed for the
introduction: the lit session both held the corpus and wrote the prose. That was
tolerable for an introduction that was purely literature.

**It is not tolerable here.** Numbers now enter sentences, and a session that both
retrieves and drafts writes the paragraph first and finds support afterwards.
So for Block A the split is restored, in this direction:

> **lit retrieves and never drafts. The orchestrator drafts and never retrieves.**

The lit session returns citekeys, page numbers and verbatim quotes. I turn those
into sentences. Neither session does both halves. Both messages already sent
say this explicitly.

## Five rounds, in order

**Round 1 — claim audit.** *(sent)* Every sentence in `results.tex` and
`methods.tex` that makes a novelty, priority or contrast claim without a
citation; anything the corpus contradicts, with the nearest counterexample
quoted; anything pre-empted. Output: a list of locators, not prose.

**Round 2 — figure design by analogy.** *(sent)* Eight questions on how this
literature draws partner-induced conformational change, nulls, confidence, and
peptides in cavities, plus six to ten specific panels to go and look at, with
licence flagged.

**Round 3 — positioning against `chiesa2025templatebias`.** The single largest
threat and it deserves its own round. It supplies a G protein as co-input **and**
measures activation state, on 63 post-cutoff Class A pairs — nothing else in the
corpus does both. What we still hold that it does not: a 21-mer peptide rather
than whole Gα; an operationalised predicate rather than RMSD to the deposited
answer; decoy and shuffled arms it never ran; AF3-lineage backbones it never
used. **Ask lit to attack that list**, not to confirm it. Each surviving
distinction needs a verbatim quote and page from chiesa showing the absence.

**Round 4 — the comparator table.** `metrics_reported` exists in every note as a
table so our numbers can be placed beside prior work. Note the schema rule:
extractors leave `comparable_to_ours` **empty by design**, because an extractor
cannot see our numbers. Populating it is my job, from their tables. Ask lit for
the metric rows; I do the placing.

**Round 5 — limitations framing.** Our caveats — the apo arm is not a physical
state (C-7), the fraction metric forecloses prospectivity (C-9), amplitude is
not reproduced (C-10) — should read as known limits of the field, not as
confessions unique to us. Ask lit which prior papers state the same limits in
their own words, verbatim, so each of ours can stand next to one.

## What the lit session must not be asked to do

Write any Block A sentence. Judge whether a number is right. Touch
`data/block_a/`, `analysis/`, or the figures. Run git.

## What crosses between sessions

Files, not messages, because neither session can rely on the other's context
surviving:

| file | carries |
|---|---|
| `analysis/block_a/DISCREPANCY_REPORT.md` | where the claim sheet and data disagree — 17 groups |
| `figures/block_a/FIGURE_PROVENANCE.md` | per-panel source, filter, n, claim |
| `figures/FIGURES.md` | the figure ledger |
| `SESSIONS.md` | why something changed and what not to redo |

Messages are for asking. Files are for remembering.

## Open items blocking the write-up

- **D9** — the reference-set denominator: 89 as previously stated, 98 empirical,
  167 total. Two `[PI]` placeholders sit in `methods.tex` waiting on this.
- **D12** — the "confidently wrong" structure is confidently right; BA-5e must
  not be built as a failure case.
- **D1, D2, D3, D5** — wording ratification. The drafts already say the
  defensible thing; these need sign-off, not rework.
- Three undefined citations in `intro.tex` awaiting extractions from lit.
