# rebuttals/ — what we send back to the pipeline agent

One file per block. These are **not** for the manuscript. They go back upstream
to whoever produced the drop, at the end of the campaign or whenever Aditya
sends them.

## Why this exists separately from the discrepancy reports

`analysis/block_<x>/DISCREPANCY_REPORT.md` is written for **us**: what we will
plot, what we will write, and how we worded around a disagreement. It is a
record of decisions made here.

A rebuttal is written for **them**: what is wrong in the drop, how we know, how
to reproduce our finding, and what we would need to close it. Different reader,
different job. The same discrepancy usually appears in both, phrased
differently — the report says "we will therefore plot X", the rebuttal says
"your claim sheet says Y and your own data says Z, here is the one-line
recomputation."

## Three sections per block, and they answer different questions

| section | question it answers | reader's next move |
|---|---|---|
| **1. Rebuttals** | what in the drop is wrong, and how do we know | fix it, or show us we are wrong |
| **2. Questions** | what can only *you* answer | answer it |
| **3. Suggestions** | what would make the paper stronger, and what would it cost | decide whether to run it |

The third section is the one worth the most and the easiest to skip. A drop that
answers every question we asked can still leave the paper one experiment short of
what a reviewer will demand, and the moment to say so is while the machine is
still warm and the next campaign is still being planned --- not after the
manuscript is submitted.

Rank suggestions by **what a reviewer would ask first**, not by what is
interesting. Give each one a cost class:

- **free** --- pure re-analysis of data we already hold
- **cheap** --- re-scoring existing predictions, no new inference
- **real** --- new predictions

A free suggestion that answers a reviewer's first question outranks an expensive
one that answers their fifth.

## What goes in one

Every entry carries five things, and an entry missing any of them is not ready:

1. **The claim as shipped** — quoted, with the file and section it came from.
2. **What the data says** — recomputed, with the file and the filter.
3. **A reproduction** — a command or a few lines someone else can run on their
   own copy of the drop. Without this it is an assertion, not a finding.
4. **Severity, and specifically whether it would reach a reader.** A mislabelled
   flag that silently produces the wrong figure outranks a truncated decimal.
5. **What would close it** — the number, the column, the file, or the answer to
   a question only they can answer.

## What does not go in one

- Anything we got wrong ourselves. Those go in the discrepancy report's own
  "these were my bugs" section and stay there. Sending someone a list of
  findings that includes four of our own parsing errors costs us the credibility
  of the other eleven.
- Style, naming and ergonomics, unless they caused a wrong number.
- Anything not recomputed. "This looks odd" is not a rebuttal entry.

## Tone

Flat and checkable. No adjectives about the work. Every claim of ours carries
its own reproduction, so they can disagree with us the same way we disagreed
with them. Where their number is right and our first reading was wrong, say so
in the entry — it is the cheapest way to be trusted on the rest.

## Files

| file | block | status |
|---|---|---|
| `BLOCK_A.md` | Block A | drafting |
| `BLOCK_B.md` | Block B | suggestions written; rebuttals and questions in assembly |

`drafts/` holds per-agent working notes and is not what gets sent.
