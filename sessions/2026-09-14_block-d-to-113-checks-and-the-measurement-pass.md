# 2026-09-14 — Block D's last four claims, and E0.1 finally starts

Orchestrator session. **No GPU, nothing commissioned.** Two things happened: Block D's
claim sheet went from four prose-only claims to **one**, and **E0.1's measurement pass
is running** — the first time the campaign's blocking item has actually been executing.

## What happened

| | |
|---|---|
| **Block D's verifier** | **86 testable / 4 prose-only → 113 / 1** |
| **SC-D-9** | reproduces **30/30**, worst 0.005 — and the convention that makes it work is **F-28** |
| **SC-D-12** | row half exact; fold half honestly marked NOT reproduced |
| **SC-D-8a** | four slopes recovered, three exact to 3 dp; CI independently replicated |
| **SC-D-8d** | unreachable, but its precondition verified — and D3 is the seed precedent |
| **E0.1** | measurement pass **RUNNING**, ~850 of 1,357 structures |

## The finding: F-28

`PARTA_D3` §4 ships a 5 × 6 Kendall-τ table and says only "τ over the 26 receptors'
per-cell active fractions" — not which τ, not what it did with receptors the
predicate cannot describe. Both had to be recovered by reproducing it:

| convention | reproduced |
|---|---:|
| τ-a, n = 26 | 1 / 30 |
| τ-b, n = 24 (undefined dropped) | 9 / 30 |
| **τ-b, n = 26, undefined carried at 0 %** | **30 / 30**, worst 0.005 |

**EDNRB and GRPR carry LEUCINE at 7.53.** `d(Y5.58 OH, Y7.53 OH)` is a quantity that
does not exist for them; the rows say so in `anchor_7_53_aa_expected`, all **1,960** of
their rows are `nan` on that axis, and **all 1,960 carry `passed=True`**. Entered at
0 % they read "never active" and mean "never measurable".

Measured cost: **29 of 30 cells rise**, **two flip sign** (both `bol~of3`), and the
inflation concentrates on the pairs the text calls "near zero" (`cha~of3` +0.050,
`bol~of3` +0.044, against `bol~cha` +0.018). **The qualitative reading survives at
n = 24**, so the conclusion stands and the numbers are biased — worth saying plainly
rather than pushing harder than that.

Separately, needing no rows at all: §4's own sentence "Boltz~Chai is the strongest
cross-backbone correlation" is contradicted by the table printed directly above it at
**2 of 5 depths** (depth 8 and 32, where `of3~pro` is larger).

## What else the rows settled

- **SC-D-8a is n-WEIGHTED.** Unweighted reproduces boltz and protenix and misses chai
  and of3 — exactly the two backbones carrying C-D-6's 190-prediction shortfall.
  Weighting by cell row count gives **three of four to three decimals**. The CI cannot
  be replayed (no draws, no seed), so an independent 1,000-replicate cluster bootstrap
  over the same 22 clusters was run instead: **all four verdicts agree**, including
  chai crossing zero. That is worth more than a replay — a replay checks arithmetic, an
  independent draw checks the verdict does not depend on their draws.
- **GATE_3's 0.76 and 1.24 are MEDIANS**, not means (0.78 and 1.32). Catching that
  early is the only reason it was not filed as a discrepancy.
- **GATE_3 sampled a ladder at two points and read a trend into it.** All five depths
  are in the rows: depth 128 sits at median pocket **0.73 Å**, *closer* to the active
  pocket than full depth's 0.76, while the predicate fires on 60 % of its samples. The
  degradation signature belongs to **depth 8**, not to shallowness.
- **D3 is the campaign's own seed-pairing precedent.** Five seeds, reused at every
  depth, 88 of 104 cells with an identical seed set. Block A has **1,898 distinct
  `seed_outer` over 9,490 rows**. `D-2026-09-13-a` has an in-house worked example, not
  just an argument.

## What I got wrong and corrected

1. **I armed a second bridge receiver on top of a live one.** Two top-level `recv.sh`
   instances — 75599 running since 09-11, and mine from this session. Killed mine; the
   long-lived one has handled every message through 09-13. No messages were duplicated
   because none arrived in the window.
2. **I introduced a fourth check label, "DISCREPANCY".** The testable total is
   RECOMPUTED + CONSISTENCY, so such a check can FAIL — lowering the numerator — while
   sitting in neither total of the denominator. `check()` now refuses an unknown kind;
   proved by planting it back.
3. **I promoted the one genuinely unmeasurable claim out of PROSE-ONLY.** Naming
   SC-D-8d's *precondition* checks `SC-D-8d/...` tripped the prefix-based promotion
   rule, and the summary line read **"0 PROSE-ONLY claims remain"** while the
   deviation was still unmeasurable — two edits after adding a check to stop exactly
   that for SC-D-12. Preconditions are now `PRE-<claim>/...`.
4. **The verifier's banner still said "BLOCK D SHIPS NO ROW-LEVEL DATA ... are
   absent".** False since 2026-09-13 and printed at the top of every run.
5. **I gave `--out` a default and opened a footgun in the same edit** — `--limit 20`
   with no `--out` would have overwritten the full measurement with a 20-row file that
   looks identical. Guarded and proved before it could fire.
6. **My inflation script printed "all 30 shifts are POSITIVE".** It aggregated by pair
   mean, not per cell; one cell is −0.002. 29 of 30, and the log says 29.
7. **My AGTR1 script printed that the predicate-active depths are the ones furthest
   from the active pocket.** That is τ = +0.30 on five points and the path is not
   monotone. Stated as depth-8-specific instead.

## Where E0.1 stands

**Running.** 1,357 structures, no GPU, resumable, cache on the natural key.

- It **stalled once** at structure 594 on a hung keep-alive socket. `Api._get` uses
  `timeout=300` with four attempts, so a single dead URL costs up to ~20 minutes. The
  `Api` class is a **deliberate verbatim port** (`GROUP0_SYSTEMS` §3.5, "kept rather
  than improved on"), so the timeout was **not** retuned. Killing and restarting cost
  nothing — it replayed 593 from cache in seconds. **That is the documented resumability
  actually working.**
- Rate is bandwidth-bound and uneven: ~36/min at best, ~3/min while pulling 900 KB
  CIFs. §4's "budget days, not hours" is right.

**The fit does NOT follow automatically.** `GROUP0_SYSTEMS` §6: "This section must be
settled before any threshold is fitted", and **D4 — the balancing rule — is open**
(`ASKS.md:106`). Recommendation on record is equal-weight headline with A, D and E
reported. **Measure now, fit after D4.**

## What the next session should not redo

- **Do not re-open the four decisions** (`D-2026-09-13-a`) — `grep '^## D-OPEN'` still
  returns nothing.
- **Do not fit an E0.1 threshold before D4 is answered.**
- **Do not retune `Api`'s timeout** without reopening §3.5's decision; restart instead.
- **Do not treat SC-D-8d as settled.** It needs structure-to-structure Cα RMSD and we
  hold 10 CIFs of 42,180 predictions. Its precondition is verified; the measurement is
  not, and cannot be from here.
- **Do not quote the τ table as n=26** without F-28's qualifier.
