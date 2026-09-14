# ASKS.md — the standing register of what is owed, and by whom

**Maintained by the orchestrator session. Rewritten, never appended.**
Last rewrite **2026-09-12**, during the autonomous run.

Three audiences, and they are kept apart because merging them produces a document
nobody can act on: **Aditya** (decisions only he can take), **`paper_af3`** (files and
answers only they hold), **lit** (corpus work).

Cost classes for `paper_af3` asks, as used in the per-block request documents:
**free** = re-analysis of data already held · **cheap** = re-scoring existing
predictions, no new inference · **real** = new predictions.

---

# A. Aditya — decisions

## ► THE FOUR TO TAKE FIRST — everything else can wait

Nine items follow. **Four of them are the message.** Three expire at dispatch; the
fourth is what everything else is conditional on. Read these, answer these, and the
rest can sit.

| # | decision | why now | cost of yes |
|---|---|---|---|
| ~~**1**~~ | ~~Chain A's construct rule~~ **TAKEN 2026-09-13 at (b)** — `D-2026-09-13-a` | was blocking every dispatch; `chain_a_source` now resolves on all 2,389 rows | done |
| ~~**2**~~ | ~~Pair seeds across arms~~ **TAKEN 2026-09-13** | still to be written into `runs/README.md` before that document is sent | done |
| ~~**3**~~ | ~~Pre-register the C7 arm~~ **ENACTED 2026-09-13** — guarded by `G-15` | 20 receptors / 19 clusters, MDE 0.279 | done |
| ~~**4**~~ | ~~Authorise the measurement pass~~ **AUTHORISED 2026-09-13** | not yet started; it is now the critical path | no GPU, ~1,430 structures |

**ALL FOUR TAKEN 2026-09-13 (`D-2026-09-13-a`).** The next decision is **A3, the adaptation band**, and it is the last free-now-worthless-later item. My recommendation was (b), yes, yes, yes. The reasoning is in the entries
below and in `DECISIONS.md`. Items 2 and 3 cost nothing and cannot be recovered later,
so declining them should be a decision rather than a delay.

**The fifth, when you have a moment:** the adaptation band (A3). It expires later — when
the ladder returns — but it is equally worthless if taken after.

---

Ordered by what they block, not by when they arose.

### A1. Chain A's construct rule — **BLOCKS EVERY DISPATCH IN THE CAMPAIGN**
`DECISIONS.md` **D-OPEN-2026-09-12-j**. `chain_a_source = PENDING:SEQ_RECEPTORS.md` on
all 2,039 Group 1 and 350 Group 2 rows. The sequences exist for all 64 receptors;
**which sequence to supply does not.** Three options costed in `SEQ_RECEPTORS.md` §3.1:
(a) full canonical, (b) remove the annotated signal peptide before the cap — the spec's
recommendation, (c) status quo, which the spec calls indefensible and which is
**what the built artefact currently is** (5HT2C keeps 29 of 32 signal residues; EDNRA
keeps 1 of 20). **Do not let anyone "fix" the PENDING by wiring it — I tried, and it
would have enacted (c) silently across 2,389 rows.** Record
`signal_peptide_removed ∈ {true,false}` per row either way.

### A2. **E6.4 — pair seeds across arms. FREE NOW, IMPOSSIBLE AFTER DISPATCH.**
Surfaced by the registry triage 2026-09-12 and it belongs this high purely because of
its shape: it costs nothing today and **cannot be done at all once Pillar 3 dispatches
2,039 systems.** Blocks A and B both failed it — 1,898 distinct `seed_outer` values
over 380 cells — so the same seed never ran the apo and cognate arms of a cell, and
every interval in both blocks is wider than it needed to be. Saying yes tightens every
interval in the ladder for zero predictions. **It appears in no pillar.** One word.

### A2b. **Pre-register the C7 arm — `redo/spec/C7_PREREGISTRATION.md`**
Drafted 2026-09-12 and **not enacted**. C7 was never tested by any block, and I wrongly
claimed Block C had answered it (`DECISIONS.md` F-23). **The redo already contains the
experiment**: 98 `ligand_role_actual = none` rows are READY in `g2_systems.csv`, and
**20 receptors in 19 clusters carry the complete apo/none × apo/agonist × cognate/none ×
cognate/agonist 2×2**. `MDE = 1.218/√19 = 0.279`, better than the decoy arm. **Zero
marginal predictions** — Group 2 dispatches those rows already.

The document pre-registers the contrast, the readout rule (**never as a share of the
partner effect** — that share spans an order of magnitude across readouts), the
declaration that pocket-Cα is biased for this contrast *by construction*, and **what
counts as C7 failing**. It needs your yes, a dated `D-` entry, and a gate check that the
arm has not shrunk before dispatch.

### A3. The adaptation band — **TIME-SENSITIVE, worthless if taken late**
`DECISIONS.md` **D-2026-09-12-i**. The interior band that selects the cognate rung for
the ligand crossing from the Group 1 ladder. **It must be recorded with its date BEFORE
any ladder result exists** — a band written afterwards is not a pre-registration,
whatever it says. Roughly 0.25–0.75 is the shape. Everything else about the adaptation
is already specified and will be gated.

### A4. The measurement pass — the largest single dependency
CPU only, no GPU, ~1,430 structures. **Four of Group 0's eight dependencies sit behind
it, and all five E0 experiments are BLOCKED on it.** Until it runs, every state call in
the campaign — including everything in `WHAT_IT_MEANS.md` — rests on a threshold
inherited from the frozen campaign rather than derived here. Standing instruction is
that it does not start without your word.

### A5. The title, and whether the ladder runs
C6 (the 21-residue peptide) is reachable only through Pillar 3's ~213,000 predictions.
C7 is **NOT** answered — I claimed it was on 2026-09-12 and retracted it the same day
(`DECISIONS.md` **F-23**); see §B0. It is *answerable* at zero marginal cost inside the
redo, and is now pre-registered. If the ladder does not run, the title narrows to a Gα
co-input and its C-terminal determinant.

*(This paragraph said "C7 is now answered" while §B0, 35 lines below, said it is not —
the same file contradicting itself. Caught 2026-09-13.)* **This is the
decision the whole campaign's size turns on.**

### A6. Group 2 — may the antagonist level be heterogeneous?
`GROUP2_LIGANDS.md` §6. Restricting it costs **3 clusters**, MDE 0.314 → 0.352.

### A7. Group 0's three open items
**D1** NPxxY hydroxyl vs Cα (deferred by you 2026-09-11; consequence if kept as OH:
42 of 199 Class A receptors unevaluable) · **D3** agonist-only admissibility ·
**D4** the balancing rule for the reported cut.

### A8. The `paper_af3` co-authorship conversation — **do this before anything is written**
If the silent-failure audit goes into the one paper, they are co-authors on a paper
documenting defects in their own pipeline. You obtained that access on a stated
*reproduction, not audit* framing, which is explicitly why the exchange was as open as
it was. **This has to be their explicit choice, agreed before the section is drafted,
not discovered at submission.** It is the largest non-scientific risk in the one-paper
plan.

### A9. Five more surfaced by the registry triage, 2026-09-12
Each is a real decision nobody has taken, with its cost:

| item | the decision | cost / what it turns on |
|---|---|---|
| **E8.1** depth × partner | **`PLAN.md` Pillar 2 and `MSA_SUBSAMPLING_REGIMES.md` §5 contradict each other** — Pillar 2 says *"write the caveat; do not spend predictions pretending to close it"*, REGIMES schedules it as Stage 2, and `CAMPAIGN.md` §2.9 says it "SURVIVES, and gains urgency". Those cannot all stand. | 5,440 predictions, or a written caveat |
| **E8.2** depth × ligand | nobody has ruled. Pillar 2's own rationale (a monomer never touches the per-chain MSA mapping) does **not** exclude it — a small-molecule ligand is still one protein chain | +8,160 marginal |
| **E0.3** admit a third state | add **21 rows** to the measurement pass. `D-2026-09-12-d` says the excluded rows are the Class A Intermediates, and **Pillar 1 as written excludes exactly the structures E0.3 measures** | 21 structures, no GPU; buys a three-state instrument claim or bounds it |
| **E2.3** efficacy ladder | **spec conflict**: `CAMPAIGN.md` §2 says DIES, but `g2_systems.csv` carries **6 READY `inverse_agonist` cells** as `G21(proposed)` after C-1 was relaxed. By `PLAN.md`'s own rule `inputs/` wins over a narrative, so **the narrative is what needs updating** | 240 / 1,200 predictions |
| **E7.6** arrestin finger loop | **the reagent is mislabelled.** `arrestin_FL` in `partners.fasta` is β-arrestin-1 P49407 residues 22–36 — an N-domain β-strand — **not the finger loop (45–86)**. `arrestin_Ctail`'s bytes are not held at all | 8,000–16,000 plus construction |

---

# B. `paper_af3` — files and answers

### B0. Nothing new is needed to finish Pillar 0 — but C7 is NOT answered from it
`rows.tier3.v2.csv` arrived and steps 1–6 are done. **I claimed C7 was answered from it
and retracted that the same day (`DECISIONS.md` F-23): every one of its 40,800 rows
carries a ligand, so the agonist alone was never predicted.** No further ask blocks the
free work, and **C7 is answerable at zero marginal cost inside the redo** — 20 receptors
/ 19 clusters already READY in `g2_systems.csv`, needing only to be named and
pre-registered before dispatch.

### B1. Block D's row-level data — **free, and the largest hole**
All three corpora its claim sheet names, **42,180 predictions**, are absent from the
bundle; five CSVs ship and every one is panel or reference metadata. **Twelve of Block
D's twelve claims are therefore untestable here** and are recorded PROSE-ONLY. This is
the single largest unverifiable surface in the manuscript.

### B2. Three named-but-unshipped Block C files — **free**
`s4_bw_decomposition.json` (the only residue-level analysis named in any block),
`task6_p0_correlation.json` (the only quantitative cross-block link, n=35),
`task_D_species_match_root_cause.json`.

### B3. The G4 off-site gate — **free**
It fired on **8 of 12 cells** and its remedy was never applied. `rows.tier3.v2.csv` was
supposed to unblock it; that work has not been done here yet and may need their
intended remedy rather than our reconstruction of it.

### B4. Two data defects found 2026-09-12 in `rows.tier3.v2.csv` — **report, not a request**
1. **`A_RECEPTOR_SLUG_MISSING` never fires.** The 800 opsin rows carry an empty
   `receptor_slug` *and* an empty `receptor_class`, and the flag that exists to mark
   exactly that is **empty on all 800**. Identity is recoverable from `input_path`
   (`b1b1u5`, `opsd`, 400 each), so nothing is lost — but nothing in the file says so.
   Same defect class as Block A's `matches_claim_sheet`.
2. **Every opsin row is `full_agonist`**, so dropping them for an empty class removes
   agonist observations only. Any table that drops them silently is comparing ligand
   levels on populations they do not share.

### B5. `MSA_SPEC.md` — their review, and the defect they already found
They caught a per-chain mapping defect inside the mechanism our own spec recommended:
OF3 keys by chain ID, Protenix by integer position, so `{"A": receptor, "B": ""}` works
on one and **fails silently on the other** — no MSA set, launcher default, live fetch at
full depth, invisible in every status JSON. **We owe them the corrected spec; they owe
us the rest of the review.** Pillar 2 Stage 2 onward depends on it.

### B6. The delivery contract — **agree it before the campaign runs, not after**
`redo/runs/README.md` is drafted and **unsent**: one directory per run, one row per
prediction, fixed identity columns, a `manifest.json` naming the input hashes consumed.
Blocks A–D each cost a bespoke verifier — 63, 116, 69 and 54 checks — because their
shape was settled after the data existed. **This is the cheapest thing on this list
relative to what it prevents.** It should go with the frozen `inputs/` set as one
document, once their §2 blueprint says which measured-axis columns they can produce.

### B7. Two artefacts claimed present and absent from the archive — **free**
`build_weekend.py` (the templater `propose.py` says it was adapted from, with
byte-parity where feasible) and
`docs/BLOCK_A_STEP3_VALIDATION_2026_09_01.md` (the human-readable half of the threshold
lock).

### B8. Was a peptide EVER dispatched as a partner chain? — **free, and it is the redo's premise**
Still unresolved. Their catalogue stocks `endothelin1` (21 aa), `substanceP` (11),
`arrestin_FL` (15, a legacy mislabel), `DAMGO` (5) and two decoys. The manifest sent to
settle it was the **deep-apo tier** — `partner_type=apo` on all 140 rows, no partner of
any kind. **Awaiting the `019_block_b_partner_selection` manifest.** The entire redo
rests on the answer being no.

### B9. Anything that would let us close the monomer→complex transfer question — **probably nothing exists**
lit swept all 83 corpus papers: the boundary is **never discussed as a boundary**. If
they hold internal evidence on whether manipulating one chain's MSA in a complex affects
the other chain, it would be the only such evidence anywhere. Low expectation, high value.

---

# C. lit

### C0. **THE CORPUS DOES NOT CONTAIN THE ALPHAFOLD PAPER** — and five more foundational ones

**Found 2026-09-14, independently and twice.** The live tool is lit's
`lit/validate/bibsweep.py`; the orchestrator built the same sweep the same day and
**retired it** rather than maintain two. **The convergence is the finding worth more
than either tool**: two separate implementations, over slightly different source sets,
put the same three works at the top of the ranking — AlphaFold at 11 citers, del Alamo
at 10, Škrinjar at 9. That is the check neither tool can perform on itself. Every line below is quoted from the bibliography of a paper we
hold, so each is checkable rather than author-year guesswork.

| citers | work | why it matters here |
|---:|---|---|
| **11** | Jumper, J. et al. **Highly accurate protein structure prediction with AlphaFold.** *Nature* **596**, 583–589 (2021). `10.1038/s41586-021-03819-2` | the paper the entire corpus is about |
| **10** | del Alamo, D., Sala, D., McHaourab, H. S. & Meiler, J. **Sampling alternative conformational states of transporters and receptors with AlphaFold2.** *eLife* **11**, e75751 (2022). `10.7554/elife.75751` | **the canonical MSA-subsampling-for-alternative-states paper, absent from a corpus built around MSA subsampling.** Highest-cost gap of the six |
| **9** | Evans, R. et al. **Protein complex prediction with AlphaFold-Multimer.** bioRxiv `10.1101/2021.10.04.463034` | every partner arm we run is a complex prediction |
| **9** | Škrinjar, P., Eberhardt, J., Tauriello, G., Schwede, T. & Durairaj, J. **Have protein-ligand cofolding methods moved beyond memorisation?** bioRxiv (2025). `10.1101/2025.02.03.636309` | cofolding **and** memorisation — squarely the threats table |
| **6** | Mirdita, M. et al. **ColabFold: making protein folding accessible to all.** *Nat. Methods* **19**, 679–682 (2022). `10.1038/s41592-022-01488-1` | the MSA pipeline most of this literature actually runs |
| **6** | Lin, Z. et al. **Evolutionary-scale prediction of atomic-level protein structure with a language model.** *Science* **379**, 1123–1130 (2023). `10.1126/science.ade2574` | the MSA-free comparator |

**And it re-ranks two of the nine the survey agent found by hand.**
`10.1002/pro.4353` — Chakravarty & Porter, *AlphaFold2 fails to predict protein fold
switching*, Protein Science 31:e4353 (2022) — was filed **Tier 3** from five
bibliographies. **Five of our own papers cite it.** `10.1038/s41467-024-51801-z`
(Chakravarty et al., *Nat Commun* 15:7296, 2024), the agent's Tier 1 and the authority
the field uses for clause 3, shows 3 citers. Both confirmed absent from `refs.bib`.

**Status, 2026-09-14 later the same day: lit has ACTED on this.** `delalamo2022sampling`,
`chakravarty2024memorization`, `ibrahim2019a100` and `monteirodasilva2024subsampled`
are extracted; corpus 87/87/91. `manuscript/refs.bib` regenerated by the orchestrator
(87 citable, 4 deliberately commented, 0 undefined citations). **What remains open is
the ≥3-citer tail lit listed:** Chakravarty & Porter 2022 (5 citers), *Have
protein-ligand cofolding methods moved beyond memorisation?* (9), *Impact of protein
conformational diversity on AlphaFold predictions* (4), *Can Protein Structure
Prediction Methods Capture Alternative Conformations?* (3), AFsample massive
sampling (3).

**What the sweep is and is not.** 801 distinct DOIs are cited across the 75 PDFs and 29
are in `refs.bib`; that ratio is not itself a defect, since an 87-paper corpus cannot
contain everything its members cite. **The ranking is the finding.** It is also a
**floor**: conference and older works often carry no DOI, so several of the nine found
by hand (ICML 2026, OpenReview) cannot appear in it at all. A clean run means no
DOI-bearing gap, never no gap.

**The reason to run it rather than read five bibliographies.** The survey agent reported
one paper as missing that we already hold with a 41 KB note, and missed del Alamo and
Škrinjar entirely. Both directions of error are exactly what `lit/CLAUDE.md` warns about:
*"Answering 'nothing in the corpus does X' while the paper that does X sits unextracted
is the highest-cost failure this skill can produce."*

### C1. **`CLAIMS.md` needs restructuring onto the single-paper spine** — and it is THEIRS
Aditya chose to report everything in one paper (2026-09-12). The argument spine is still
in the old shape: C1–C9 plus five "new" claims, with the instrument findings scattered
rather than carried as supporting claims under one headline. **I nearly did this myself
and stopped — `CLAUDE.md:260` gives `CLAIMS.md` to lit.** Proposed headline, for them to
accept, reject or rewrite:

> *The apparent conformational control these models show is driven by the transducer
> co-input — and the instruments the field uses to measure it (state predicates, decoy
> negatives, confidence scores, delivery pipelines) do not support the claims commonly
> made from them.*

with the positive result as the headline claim and the instrument findings — confidence
separating receptors rather than structures; decoys unobtainable for a third of a Class A
panel; the tilt axis uncalibratable non-circularly; three of four backbones changing two
things at once between apo and cognate — as supporting claims with their own evidence
slots. **The verification discipline moves to Methods; it is not a claim.**

**Also for them: C7's status has changed and `CLAIMS.md` does not know it.** It is
recorded there as *"not testable on A, B or D; Block C holds 7,000 apo × agonist
predictions and reports no state result"*. As of 2026-09-12 **it is answered** — see
`analysis/block_c/received_2026_09_12/WHAT_IT_MEANS.md` §3 — with the caveat that the two
readouts disagree about the effect's size and the continuous one should be quoted.

### C2. `corpus_check.sh` classifies the four deliberately-unread `refs.bib` entries as **hard** drift
so it can never exit 0. **This does not fail `verify.sh`** — both branches call `ok()`
(`verify.sh:26-27`) — but a permanently-present warning is one everyone learns to skip.
Proposed fix: demote that one report from hard to soft, as the "note with no PDF" report
already is. **Theirs to action, not ours.**

*(Everything else asked of lit on 2026-09-12 came back answered, and two of their answers
corrected me — the Neff claim, and the confirmation that F-16 was not an over-correction.)*

---

# D. Mine — no decision needed, just time

1. **Triage of the 30 `NEEDS_TRIAGE` experiments** against the five pillars — in flight.
2. **`layout.py`'s L1 and L3–L7 have no runnable plants.** Only L2 does. Recorded in
   `CLAUDE.md`; converting them is outstanding work, not a completed claim.
3. **The G4 gate remedy**, to whatever extent it can be reconstructed without B3.
