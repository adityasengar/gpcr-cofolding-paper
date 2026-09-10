---
name: dataquery
description: Query our own experimental results while writing the manuscript. Use this skill whenever a question touches our predictions, receptors, backbones, arms, exclusions, rates, or any number destined for Results or Methods — how many predictions, what fraction were called active, which receptors were run, does the data support a claim I am about to write, what is the n for this arm and what filter is behind it. Trigger it even when the user does not name a file: any question about our own numbers should go through this skill rather than being answered from memory or from a claim sheet.
---

# dataquery

Answer questions about **our own experiments**. The literature counterpart is
`litquery`. This skill retrieves and verifies; it does not draft prose.

## Data arrives one block at a time

**Each block is a zip that supersedes everything before it.** The current block
is `data/block_a/` — 9,490 scored predictions, 48 receptors (40 Class A, 4 B,
4 F), 4 backbones, 2 arms (apo and cognate). Block B will arrive the same way.

`data/block_<x>/` is **read-only**. Everything derived lives in
`analysis/block_<x>/`.

An earlier export was deleted on 2026-09-10. It was a *different campaign* —
different receptors, different arms, no shared prediction paths — and keeping it
invited a number from the wrong campaign reaching a sentence. If you find a
reference to `predictions.csv`, `rows_enriched_v3_7.csv`, `RESULTS.md`,
`STATUS.md` or `analysis/q.py`, it is stale; say so.

## The data wins over the claim sheet, always

Each drop ships a claim sheet beside the tidy data and **they disagree**.

```bash
python3 analysis/block_a/verify_claims.py     # 34 checks; exits 1 on mismatch
```

19 reproduce, 15 do not. All 21 discrepancy groups are recorded in
`analysis/block_a/DISCREPANCY_REPORT.md` — four were named in the shipped brief,
seventeen were found here, including a shipped structure that is the wrong
protein and four `ALIGNMENT.md` files naming anchors that do not reproduce the
shipped distances.

**Never quote a number from a claim sheet without checking it.** Never quote one
this skill cannot reproduce. Where they disagree, record the disagreement rather
than smoothing it.

## The exclusion trap — read before answering anything with an n

**Never filter on `excl_any`. It removes 5,093 of 9,490 rows (54%).** The five
sets have different causes and different scopes:

| set | rows | apply |
|---|---:|---|
| E1 | 25 | always — cell mean pLDDT below 50 |
| E2 | 4 | always — physically impossible geometry |
| E3 | 4,890 | **per axis** (`excl_E3_npxxy`, `excl_E3_tilt`), and only where a reference value is a denominator or a regression predictor |
| E4 | 1,495 | Class-A claims |
| E5 | 500 | sensitivity contrast only, never silently |

E1+E2 alone keeps 99.7%. E3 is irrelevant to raw distributions, predicate firing
rates and confidence correlations, which never touch a reference separation.

**Every answer states its filter and its n.** An n without a filter is not an
answer.

## Answer shape

Lead with the number, then the filter and the n it rests on, then the file it
came from. If a number cannot be reproduced from the tidy files, say so plainly
and point at the discrepancy report rather than reaching for the claim sheet.

Where the answer needs new data rather than a new query, add it to
`analysis/block_a/DATA_REQUESTS.md` instead of working around the gap.
