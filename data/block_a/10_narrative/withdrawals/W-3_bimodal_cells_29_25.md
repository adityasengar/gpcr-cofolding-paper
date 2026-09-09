# W-3 — "29 bimodal cells, 25 in apo (86%)"

## Claim as previously stated

Prior campaign framing held that 29 (receptor, arm, backbone) cells landed
bimodal on the two-instrument predicate, 25 of them in the apo arm — a
86% apo enrichment interpreted as apo-bistability evidence.

## Retraction

**Withdrawn.** The "29 / 25 in apo" phrasing does not resolve to any
current on-disk figure. Nearest predecessors were 12 Class-A cognate
bimodal cells (`campaign_completion_report.md:130`) and an 8-cell
dip-test list (`POST_BLOCK_A_CLEANUP_2026_09_02.md:166`) — both
SUPERSEDED 2026-09-02 as OF3-seed-bug contaminated. Per the cleanup
doc's own note, "OF3's five-structures-replicated-five-times [under the
seed bug] read as five modes".

**Current authoritative counts** on the post-Round-2 rows.csv:

| Definition | Total cells | Apo | Cognate | Apo-share |
|---|---:|---:|---:|---:|
| def-A (0 < active < 25) | 72 | 46 | 26 | **64%** |
| def-B (5 ≤ active ≤ 20) strongly bimodal | 26 | 16 | 10 | 62% |

Apo IS enriched (64% vs a 50% null), but not at the pre-fix 86% figure.

**Per-backbone** (def-A):

| Backbone | Bimodal cells | Apo share |
|---|---:|---:|
| OF3 | **36** (50% of the total) | 61% |
| Boltz | 16 | 62% |
| Chai | 11 | 55% |
| Protenix | 9 | 89% |

## Evidence

- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 4e
- Superseded predecessors: `_internal/superseded_docs/campaign_completion_report.md:130`, `analysis/block_a/POST_BLOCK_A_CLEANUP_2026_09_02.md:166`

## What the manuscript should say instead

> On the post-Round-2 corpus, 72 of 380 cells (19%) are bimodal under
> the class-conditional two-instrument predicate (46 apo, 26 cognate);
> apo-share is 64%. OpenFold-3 contributes half of all bimodal cells,
> consistent with its softer per-backbone two-instrument agreement rate
> (§Phase 4c). Multi-backbone-consensus apo-bimodal receptors are FSHR
> (4/4 backbones), CNR1 (3/4), and OPSD (3/4).
