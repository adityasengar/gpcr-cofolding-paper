---
name: dataquery
description: Query our own experimental results while writing the manuscript. Use this skill whenever a question touches our predictions, receptors, backbones, conditions, rates, or any number destined for the Results or Methods section — how many predictions, what was the active fraction, which receptors were run, does the data support a claim I am about to write, what is the n for this arm. Trigger it even when the user does not name a file: any question about our numbers should go through this skill rather than being answered from memory of STATUS.md.
---

# dataquery

Answer questions about **our own experiments**. The literature counterpart is
`litquery`; this skill is its mirror and follows the same discipline for the same
reason. It retrieves and verifies. It does not draft prose.

## The one thing to know first

`STATUS.md` is a **claims** file. `RESULTS.md` is the **ledger** that records which of
those claims reproduce from data actually present in this repo. They disagree in
places, and where they disagree `RESULTS.md` is the honest one.

This repo holds a **partial export**: 17,568 predictions against roughly 41,500
described in `STATUS.md`, with every `prediction_path` pointing at
`/hpc/scratch/sengaad1/...`. **39% of local rows have no `classified_state` at all.**

Run this before answering anything:

```bash
python3 analysis/q.py scope
```

A number that does not reproduce locally is **unverified, not wrong**. Say it that
way. Collapsing "I cannot check this here" into "this is wrong" is its own failure.

## Layout

```
STATUS.md      landed vs planned blocks — claims, not evidence
RESULTS.md     the ledger: one entry per citable number, each with a query + verdict
analysis/q.py  the queries themselves; `python3 analysis/q.py --list`
data/          predictions.csv (17,568) · conditions.csv · receptors.csv
               backbones.csv · coverage_matrix.csv · experiments.jsonl
rows_enriched_v3_7.csv   19M, 68 cols, per-prediction with full provenance
               (input_sha256, scorer_git_sha, scorer_version, ref_pdb_sha…)
report/        summary.tex / summary.pdf, predictions_minimal.csv
```

## Rules

- **Every number carries a locator**: a `RESULTS.md` entry id (`[R-B-LADDER]`), or a
  query that reproduces it. A number with neither does not go in an answer.
- **Never quote a number from `STATUS.md` as if it were verified.** Check `RESULTS.md`
  first. If the entry says `LOCAL-PARTIAL` or `NOT-LOCALLY-CHECKABLE`, say so in the
  same breath as the number.
- **Report denominators.** Rates here are computed on the classified subset of a
  partial export. "56.9% active" without "of 1,207 classified rows, out of a 17,568-row
  partial export" is misleading even when arithmetically right.
- **Check the partner mix before comparing backbones.** The arms are not balanced —
  chai's AA2AR rows are apo-only, af2mm's are ligand-only. A cross-backbone median
  over unmatched conditions is a confound, not a result. This has already produced one
  half-wrong claim (see `R-INFRA-AA2AR`).
- **If a new number becomes citable, add it to `RESULTS.md` with its query.** The
  ledger is the deliverable, not the chat answer.
- **`STATUS.md` planned blocks are radioactive.** D1, D2, D3 and T1.5 have not run.
  Flag any question whose answer would depend on them.

## Query classes

**Point lookup** — "what is the active fraction for shuffled Gα". Check `RESULTS.md`;
if absent, write the query, run it, report it with its denominator, then offer to add
a ledger entry.

**Claim audit** — the user states a sentence destined for Results. Identify the columns
that would falsify it, run them, and report clause by clause. A claim with three
clauses can be two-thirds true; say which third is not.

**Coverage** — "do we have enough n for X". Answer with the cell counts, not a verdict.
`python3 analysis/q.py coverage`.

**Methods support** — the provenance columns in `rows_enriched_v3_7.csv`
(`scorer_git_sha`, `scorer_version`, `bw_derivation_source`, `gpcrdb_*`,
`ref_pdb_sha_*`) are what a reproducible Methods section is built from. Prefer them
over prose recollection of the protocol.

## What this skill does not do

It does not write Results or Methods prose. Same reason as `litquery`: a session that
both computes and drafts writes the sentence first and finds the number that fits.
Hand back numbers, denominators, queries and ledger ids; a separate drafting session
turns them into sentences.
