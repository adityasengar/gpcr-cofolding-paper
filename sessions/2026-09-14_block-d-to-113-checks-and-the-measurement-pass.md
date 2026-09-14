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

---

# Afternoon — E0.2 answered free, two failure families named, and the experiment scope

## What happened

| | |
|---|---|
| **E0.2 ANSWERED, cost `free`** | the published Ibrahim A100 index was **already in our pipeline** and already computed on 38,820 predictions. **F-31** |
| **Two failure families named** | **F-32** denominators, **F-33** selection. Between them they cover most of this week |
| **The corpus had no AlphaFold paper** | nor del Alamo 2022, Škrinjar 2025, ColabFold, ESMFold. `refs.bib` resynced to 87 |
| **13 candidate experiments scoped** | 64-agent hunt over the 45-entry catalogue. `redo/spec/EXPERIMENT_GAPS_2026_09_14.md` |
| **Nothing authorised, nothing run** | the redo campaign is still at **zero predictions** |

## The corrected scope of the question

Aditya's instruction mid-session: *"remember your job is to just identify what all
other experiments i can run..in the redo plan, nothing ha been run yet."*

I had a workflow running that hunted **framing** — titles, referee objections,
negative-results positioning. **Wrong question.** Killed it and re-ran against the
catalogue, hunting experiments. The correction matters beyond this session: with zero
predictions spent, every factor is still choosable, and treating the campaign as
half-committed narrows it for no reason.

## E0.2, and how it was sitting in plain sight

Lit flagged `ibrahim2019a100` — a **published, operationalised class A activation
predicate** — as exactly the independent index E0.2 needs, with a blocking unknown:
the five distances and thresholds are not in the abstract.

**They are in `redo/protocol/received/axes.d9c646af.py:329–346`**, cited to the DOI,
with coefficients, intercept and both threshold schemes. `a100_index` has been
computed on every prediction in two blocks since the day they landed. A
`grep -rl a100` across `analysis/`, `redo/build/`, `redo/gates/`, `figures/` returns
nothing.

| block | n | agree | **disagree** |
|---|---:|---:|---:|
| D1 | 14,000 | 88.3% | **11.7%** |
| D3 | 22,860 | 90.8% | **9.2%** |

Asymmetric both times: **the published index calls more predictions active than our
conjunction does.** E0.2's novelty line says no study reports such a rate. We can
report one on 36,860 predictions for free.

**Two bounds that must travel with it**: r(a100, tilt) = **+0.846**, so this is
independently *published*, not axis-independent; and Ibrahim validated on X-ray while
these are predictions.

## The two families, and why they are the durable output

**F-32 — denominators.** *A count is not a rate until you can name what was in the
denominator and what could never have been in the numerator.* Four instances: F-28,
F-23, F-19, and lit's corpus negative. Lit's reading is right and is why it leads
with F-28: a corpus negative is visible as an absence once someone asks, but **a null
over an undefined population looks like data** — it has a value, a row count and a
confidence interval, all well-formed.

**F-33 — selection.** *When the selection criterion is the result, the agreement is
not information.* Three instances, and **the first is mine from the same afternoon**:
I offered r = +0.846 to lit as corroboration that our relayed transcription was
correctly oriented, having reported it *after* seeing it point the right way. The
third is the useful one — `delalamo2022sampling`'s authors say AF2 reaches active
GPCR states because the training set featured many active GPCRs, so **reaching active
is what the null does and reaching INACTIVE is the informative direction.** That
converts the strongest counter-evidence in the corpus into a design constraint on our
own MSA arm.

**The rule both impose, cheap only because nothing has run:** every arm whose method
or parameter is chosen must pre-register the choice rule, and the rule must not
mention the outcome. Select on a property of the **input**; where performance must
decide, decide it on a **held-out** set outside the reported panel.

## What the experiment hunt found, verified by hand

19 proposed, 13 cleared, 19 verdicts rejected across DUPLICATE / INFEASIBLE /
UNDERPOWERED / PREEMPTED. Four load-bearing claims re-checked before repeating:

- **The recording contract records less confidence data than we already hold.**
  `g1_recording_spec.tsv` names no `min_plddt_at_anchor`, `plddt_mean`,
  `plddt_at_anchors`, ipTM, PAE, Ramachandran, chain breaks, templates or recycles.
  Blocks B and D each hold **four**; the redo would record **two**, both partner-side.
  **Title clause 3 is a confidence claim.** Free to fix, impossible after dispatch.
- **Template has never been a factor in either campaign** — zero mentions in the
  recording spec, both systems files, `CAMPAIGN.md`, `MSA_SPEC.md` — and Block B's
  templates-off state is evidence class **(b)+(c)**, never (a). Nobody verified it.
  `delalamo2022sampling` reaches alternative conformations with templates **ON**.
- **All 2,039 Group 1 rows carry `ligand = none`.** The title's "graded with length"
  estimates its slope in exactly one ligand condition.
- **All 30 `family_swap` rows carry `chain_b_sha256 = PENDING:COUPLING.md`.** G9 is
  enumerated and not built; dispatching today sends an unbuilt control.

## What I got wrong and corrected, afternoon

1. **I told lit `intro.tex:325–332` needed changing** because we can now report the
   disagreement rate it says nobody reports. It reads *"No study in **this corpus**
   reports such a rate"* — **scoped to the corpus, correct, still true.** I had
   paraphrased a manuscript sentence without reading it, an hour after writing up
   that exact failure about my own work.
2. **I offered a selected statistic as corroboration** — see F-33.
3. **`CLAUDE.md` said `g1_recording_spec.tsv` has no writer anywhere in
   `redo/build/`.** It has one, `g1_recording_spec.py`, which reproduces the file
   byte-for-byte and refuses with a named FAIL on drift. I was about to report the
   recording fix as blocked by rule 1. Corrected in the brief.
4. **I ran a workflow against the wrong question** — framing, not experiments.

## What the next session should not redo

- **Do not treat the redo as partly committed.** Zero predictions. Every factor open.
- **Do not fit an E0.1 threshold before D4.**
- **Do not call A100 "independent" unqualified** — r = +0.846. Independently
  *published*, not axis-independent.
- **Do not maintain a second bibliography sweep.** `lit/validate/bibsweep.py` is the
  tool; mine is deleted. The convergence of two implementations on the same ranking
  is the part worth keeping.
- **Do not run the free nanobody A100 test ad hoc.** Its expected shape is
  pre-registered in F-33 precisely so both outcomes stay reportable.
- **Nothing in `EXPERIMENT_GAPS_2026_09_14.md` is authorised**, and its prediction
  counts, MDEs and cut figures are unverified.

---

# Late afternoon — the reference document, and the scope correction that produced it

## The correction that mattered most

Mid-session, asked to think about improving the paper for Nature Methods, I launched a
workflow hunting **framing** — titles, referee objections, negative-results
positioning. Aditya stopped it:

> *"remember your job is to just idenitfy what all otehr expeirments i can run..in the
> redo plan, nothing ha been run yet"*

**Wrong question, and the second half is the part worth carrying forward.** With zero
predictions spent, every factor is still choosable. Treating the campaign as
half-committed narrows it for no reason. Killed that workflow and re-ran against the
catalogue, hunting experiments. **The same error is easy to repeat**, because the
volume of specification makes the campaign *look* committed.

## What got built

| | |
|---|---|
| **`redo/spec/REDO_REFERENCE.md`** | **560 → 5,610 lines, 16 parts.** The single reference for the campaign |
| **`analysis/crosscheck_redo_reference.py`** | re-derives **104** load-bearing numbers from `redo/inputs/`. **104/104 reproduce**, in-repo and from a fresh unzip |
| **`redo/spec/EXPERIMENT_GAPS_2026_09_14.md`** | 13 experiments not in the 45-entry catalogue |
| **`~/Downloads/redo_campaign_2026_09_14.zip`** | 16 MB, 623 files, self-verifying |

## How the reference was built, and why that matters

Three independent passes. Seven domains gathered by agents under one standing rule:
**every number from a command actually run, and any count stated in prose RE-DERIVED
from the data file rather than copied.** Each domain then went to a second agent that
re-derived with its own commands. Then a third mechanical pass.

**The second pass rejected two claims**, corrected in the text rather than quietly
fixed:

- C7's 2×2 per-cell counts are **36/36/52/52 = 176** keyed on `partner_level`, not
  "36 in each of four cells" — `partner_level == cognate` covers **both** `R3_ct21`
  and `R7_full`.
- Catalogue arithmetic reproduces **26 of 31, not 28**. Two further products fail
  against their own factors: Block A's `48×4×2×25 = 9,600` (stated 9,490) and Block
  C's `36×4×3×2×50 = 43,200` (stated 40,000).

**Part 12 carries nine more disagreements** between this repo's prose and its data,
including `GROUP1_SYSTEMS.md` stating a registry count of 588 where the file holds 782
— and disagreeing with itself twice in the same document.

## The ambiguity that would have been a real error

**"Decoy" means two different things in this project**, and both senses appear in the
same tables:

- a **decoy PARTNER** is a Gα-like protein with an edited α5 tail — Block B's arms,
  confounded at the MSA;
- a **decoy LIGAND** is a property-matched inactive small molecule — the D-RULE arm.

**Block B's published ladder — apo 0.158 → decoy 0.558 → shuffled 0.809 → cognate
0.891 — is a ladder of PARTNERS.** I nearly wrote 0.558 into the ligand section. It is
now Part 2.7, flagged as the one thing to read before any table.

## What I got wrong, late session

1. **Ran a workflow against the wrong question** — framing rather than experiments.
2. **Two transcription errors in the first draft of the reference**, caught by
   re-querying before commit: `R7_full` is 124 rows not 114 (I dropped a fifth length
   variant), and the uncoupling peptide mutants are 42 rows not 18 (they exist on
   ct17, ct19, ct21 and a5helix, not only ct21). **The fix was structural** — stop
   transcribing, generate the tables from the files.
3. **One of my own cross-checks was the wrong shape.** "17 Gα families" is a count over
   `ga_rung` constructs; the registry's `family` column holds **30** distinct values,
   because reference-tip constructs put the *receptor* slug there. The document was
   right and my check was wrong; both now say so.

## What the next session should not redo

- **Do not treat the redo as partly committed.** Still zero predictions.
- **Do not hand-transcribe counts into documentation.** Run
  `python3 analysis/crosscheck_redo_reference.py` — it fails loudly.
- **Do not conflate the two senses of "decoy"** — Part 2.7.
- **Nothing in `EXPERIMENT_GAPS_2026_09_14.md` is authorised.**
- **The lit session's tree is in flight** — `lit/**`, `CLAIMS.md` and
  `manuscript/sections/intro.tex` are theirs and must not be committed by the
  orchestrator.
