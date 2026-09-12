# 2026-09-12 (e) — C7 answered, the decoy arm frozen, and three findings about our own machinery

Orchestrator session, continuing into an autonomous run while Aditya was away. No
block landed and no compute was commissioned. **The scientific payload is that C7 —
one of the paper's three title clauses — is answered from data we already held.**

## What happened

| | |
|---|---|
| **Pillar 0's mining** | **COMPLETE.** Steps 3–6 done: cluster unit, cluster bootstrap, continuous readout, seeds, opsins |
| **C7** | **ANSWERED** — and the two instruments disagree about the effect's size by 5.5–7.9× |
| **The decoy arm** | rule amended twice, refused at 11 of 15 clusters, then run as **EXPLORATORY at k = 11** and **FROZEN** — 26 checks, 26 proved, three digests |
| **The campaign** | got a plan of record (`PLAN.md`), one pre-registered adaptive parameter, and a triaged registry |
| **`ASKS.md`** | new — the standing register of what is owed by Aditya, by `paper_af3`, by lit |
| **Three machinery findings** | F-20, F-21, F-22 — recorded; one of the three now closed |

## Decisions Aditya made, with their reasons

**Report everything in ONE paper.** Not three. The negatives are what make the positive
believable, and split across papers the main one ends up citing its own caveats — which
is how caveats get lost.

**Run the decoy arm at k = 11 as EXPLORATORY**, rather than turning a third knob or
re-downloading ChEMBL. Reason, and it is arithmetic rather than taste: `MDE = 1.218/√k`
gives 0.352 at the pre-registered k = 12 and **0.367 at k = 11 — a 4.4% loss** for 396
predictions. **The bar stays at 12; what changed is the arm's status.** The two
alternatives were declined on the record, with the `anywhere` pool left pre-registered
on the shelf in case a referee demands confirmatory status.

**Amend D-RULE twice, after watching it fail** — cLogP to an absolute ±1.0 log window,
and a within-draw dissimilarity cap. Reason: a percentage of a logarithm is a units
artefact, not a chemical tolerance. **Reported as a (width × cap) grid rather than a
point, precisely because the change came after a failure.**

**Lock the decoy plan.** Frozen means asserted by a gate that fails when it changes and
proved by planting — not a banner.

**Keep the plan flexible for the partner condition** used in the ligand arm, informed by
the many-combination arms. Enacted as a **pre-registered adaptation rule** committed
before the data exists: the cognate identity stays frozen (the supplied peptide and the
scoring reference must be the same molecule), the matched nulls run at whatever rung the
real peptide runs at, and **only the cognate rung is adaptive** — selected on
**headroom**, never on effect size.

## What the verification found

- **The headline survives every correction asked of it.** 24 of 24 partner contrasts —
  3 roles × 4 backbones × 2 readouts — exclude zero, under both opsin variants.
- **The C7 result survives its most obvious confound.** In apo the off-site rate is
  severely role-asymmetric (agonist 29.3%, antagonist 1.6%), so a third of agonist rows
  have no agonist in the pocket. Restricting to on-site rows: all four backbones still
  exclude zero, magnitudes barely move, no systematic direction.
- **Every gate is now self-proving.** layout 8 checks (L2 6 plants, L1/L3–L8 7 plants),
  drule 26/26, g2 14 checks/15 plants, ligands 10/10, g0 12/12, registry 12/12.

## What I got wrong and corrected

**Eight, and the pattern is more useful than any one of them.**

1. **"Chain A is a stale label."** Wrong, and dangerously so. It is an untaken PI
   decision, and the built artefact already embodies the option the spec calls
   indefensible — 5HT2C keeps 29 of 32 signal residues. **Wiring it, as I proposed,
   would have enacted that silently across 2,389 rows.** The inverse of the day's other
   failures: a live guard mistaken for a stale label.
2. **"Decoy ≈ antagonist on all four backbones."** Conflated *shift* with *level*. The
   shift is ligand-independent — that stands. The level is not: **agonist > decoy >
   antagonist** on the continuous readout, 7 of 8 cells. F-19's citation withdrawn; F-19
   itself is unaffected because it rests on the chemistry.
3. **The freeze plant I specified proved nothing.** "Permute one receptor's molecules
   onto another's" is inert against both set-hashes, because they are over *sorted*
   values. **The same 33 molecules against the wrong receptors would have passed the
   entire freeze.** Closed with a third digest over assignment pairs.
4. **The fold change was unpaired** — "3–15×" is min-of-one-backbone against
   max-of-another. Paired: **5.5–7.9×**. The same error I had corrected in lit an hour
   earlier. It cost something real: it made a strikingly consistent result look erratic.
5. **"The binary predicate makes the backbones incomparable."** Too strong — it does not
   reorder them (identical ranking on both readouts). It **inflates the spread ~5×**.
6. **The SD spread printed where the standardised-effect spread belonged.** Right idea,
   wrong variable, and **the sentence read plausibly either way** — which is why it
   passed my review and lit's.
7. **"30 experiments need triage."** 27. Three were a stale artefact.
8. **`CLAIMS.md` is not mine to restructure.** I nearly did; `CLAUDE.md:260` gives it to
   lit. Proposed instead.

**And three findings about our own machinery, which are the durable part:**

- **F-20** — `rows.tier3.v2.csv` landed and nothing recorded that it had, while three
  documents already rested on it.
- **F-21** — a generated input can go **stale** against its own inputs and no guard
  notices. `manifest.py --check` compares a file to its *own* hash, not its sources.
- **F-22** — `inputs/` is "code only", but the guard catches only edits made *after*
  stamping. 31 of 64 inputs named no generator; **`g1_recording_spec.tsv`, the campaign's
  own recording contract, had no writer anywhere.** L8 added; that instance now closed.

**The recurring shape, four times in one day:** a check that applies cleanly and tests
nothing. Three inert plants, and a self-test harness whose extension filter silently
dropped a file. **Every one was caught by running the thing rather than reading it.**

## What the next session should not redo

- **Do not wire chain A.** `ASKS.md` A1. It is a decision, not drift.
- **Do not re-open the decoy rule.** Frozen, 26 checks. A third amendment after two is
  indistinguishable from fitting.
- **Do not re-derive Pillar 0.** Steps 1–6 are done and `STEPS_3_TO_6.md` regenerates.
- **Do not build a 16-mer rung.** F-16, re-confirmed by lit with two further arguments.
- **Do not quote both readouts for C7.** The continuous one; the binary is floor-pinned.
- **Do not restructure `CLAIMS.md`** — lit's.
- **Do not trust the manifest to mean an input is current or code-written.** F-21, F-22.
