---
name: blockintake
description: Take delivery of a new results block and turn it into a manuscript section. Use this whenever a new block zip arrives — block_b, block_c, or any later drop — or when the user says a new dataset has landed, asks to verify a claim sheet against its data, or asks to start writing a new section from new results. Covers extraction, claim verification, the discrepancy report, tables, panels, prose and the adversarial pass, in that order.
---

# blockintake

Turn a delivered block into a section of the paper. Block A took many rounds of
improvisation; this is what that converged on. Follow it in order — each step
protects the one after it.

## The model

**Each block arrives as a zip and supersedes everything before it for new
claims.** Earlier blocks are not deleted; they remain the record behind the
sections already written. But no new claim is built on an older block, and data
from two blocks is never mixed — Block A and the export before it turned out to
be different campaigns with different receptors and no shared prediction paths.

## 1. Land it, read-only

```bash
unzip -q <block>.zip -d data/block_<x>
```

`data/block_<x>/` is **pristine**. Never edit the drop, never "fix" a file in
it — defects get recorded, not repaired. Gitignore the coordinates and the zip;
commit the tabular data, because every number must trace to a shipped file.

Read the drop's own README, data dictionary and brief **fully** before writing
code. Then read `analysis/block_a/DISCREPANCY_REPORT.md` — not for its findings
but for its failure *classes*, which recur.

## 2. Verify the claim sheet against the data — before anything else

Write `analysis/block_<x>/verify_claims.py`: one check per checkable number in
the shipped claim sheet, recomputed from the tidy files, exiting 1 on any
mismatch. **Do this before a single panel or sentence.**

Block A: 34 checks, 19 reproduced, 15 did not. Four mismatches were named in the
brief; **seventeen were not**. Expect the same.

**The data wins over the claim sheet, always.** Record the disagreement in
`analysis/block_<x>/DISCREPANCY_REPORT.md` with, for each: what the claim sheet
says, what the data says, what you will plot, and the recommended wording.

## 3. Failure classes that recurred in Block A

Check each against the new drop by name:

- **An exclusion-flag union that removes most of the data.** Block A's
  `excl_any` removed 54% of rows. The flags were separate sets with different
  scopes, exported separately *on purpose*. Read the exclusion definitions and
  apply each where it belongs; never the union.
- **Confidence intervals labelled as one bootstrap and computed as another.**
  Block A's claim sheet headed a column "cluster-boot" and quoted the receptor
  values, which were narrower. Check the widths against both columns.
- **`n` columns that overstate the effective n.** Compare every stated `n`
  against the non-null count of the thing it counts.
- **Denominators that cannot be tested.** Block A had 610 predicate-active rows
  with no reference to score against, quietly diluting a rate.
- **Structure files that are the wrong protein.** Check every coordinate file
  against its own `_struct.title`. Block A shipped CFTR in place of an opioid
  receptor complex.
- **`ALIGNMENT.md`-style notes naming residues that do not reproduce the shipped
  distances.** Four of Block A's were wrong. Recompute every anchor from
  coordinates and refuse any that does not match the tidy value.
- **A self-certifying column.** Block A's `matches_claim_sheet` read `True`
  where the value disagreed. Never trust a flag that vouches for itself.
- **A claim asserted in a brief with no column behind it.** Block A had no
  template or MSA field at all, while the Methods asserted both.

## 4. Tables, then panels, then prose

- Tables to `analysis/block_<x>/tables/`, with a second copy written into
  `manuscript/tables/` so the LaTeX build stays self-contained. Every caption
  states its exact filter and its n.
- Panels to `figures/block_<x>/panels/`, built on `figures/figstyle.py` and
  `figures/figpanels.py`, following `figbuild`. Read
  `lit/RENDER_CONVENTIONS.md` before any structural render.
- Prose to `manuscript/sections/`. **Write it into the manuscript, not into a
  markdown draft** — a section that lives outside the paper is a section the
  paper does not have.

## 5. Ask the corpus, in this direction

The lit session **retrieves and never drafts**; the orchestrator **drafts and
never retrieves**. Ask it for: a claim audit of the new section (uncited novelty
or contrast claims, contradictions with the nearest counterexample quoted,
pre-emption), design-by-analogy for the new data shapes, and prior papers
stating the same limitations in their own words. Ask for citekeys, pages and
verbatim quotes; turn those into sentences yourself.

## 6. Adversarial pass, last

Before the section is called done, spend one agent whose **only** job is to
break it — given the discrepancy report, the data and the corpus, briefed to
attack the claims rather than polish them. Do not commission a "sort the story"
agent per block: a block's story is constrained by its data, and an agent asked
to improve a story will overclaim. The story pass across all blocks happens once,
at the end, in a fresh session.

## 7. Update the spine

Add the block to the claim-to-block map in `CLAIMS.md` and mark which claims it
moves from open to written. If the block does not test what the title claims,
**say so there** rather than letting the gap close quietly.

## Deliverables

```
data/block_<x>/                  the drop, read-only
analysis/block_<x>/verify_claims.py
analysis/block_<x>/DISCREPANCY_REPORT.md
analysis/block_<x>/DATA_REQUESTS.md
analysis/block_<x>/tables/
figures/block_<x>/panels/  + FIGURE_PROVENANCE.md
manuscript/sections/<section>.tex
```
