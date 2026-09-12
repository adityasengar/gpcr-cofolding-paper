# 2026-09-12 (e) — C7 CLAIMED AND RETRACTED, the decoy arm frozen, and four findings about our own machinery

> **CORRECTED LATER THE SAME DAY.** This log was written titled *"C7 answered"* and
> that claim is **withdrawn** — `DECISIONS.md` **F-23**. All 40,800 rows of
> `rows.tier3.v2.csv` carry a ligand, so the agonist alone was never predicted and
> that file cannot answer C7. The original headings are left visible below rather
> than rewritten, because a session log that quietly corrects itself is worth less
> than one that shows what was believed and when.

Orchestrator session, continuing into an autonomous run while Aditya was away. No
block landed and no compute was commissioned. **The payload I thought I had was that
C7 was answered from data we already held. It was not** — see the banner. What the day
actually produced: the partner result hardened through four corrections, an instrument
comparison that survives the retraction, the decoy arm frozen, and **four** findings
about our own machinery, the last of which is the retraction itself.

## What happened

| | |
|---|---|
| **Pillar 0's mining** | **COMPLETE.** Steps 3–6 done: cluster unit, cluster bootstrap, continuous readout, seeds, opsins |
| ~~**C7**~~ | ~~ANSWERED~~ **RETRACTED, F-23.** What was measured is agonist vs neutral antagonist at fixed partner condition. The two-instrument finding survives and does not depend on C7 |
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
- **The agonist−antagonist contrast survives its most obvious confound** *(written as "the C7 result"; relabelled after F-23).* In apo the off-site rate is
  severely role-asymmetric (agonist 29.3%, antagonist 1.6%), so a third of agonist rows
  have no agonist in the pocket. Restricting to on-site rows: all four backbones still
  exclude zero, magnitudes barely move, no systematic direction.
- **Every gate is now self-proving.** layout 8 checks (L2 6 plants, L1/L3–L8 7 plants),
  drule 26/26, g2 14 checks/15 plants, ligands 10/10, g0 12/12, registry 12/12.

## What I got wrong and corrected

**Nine, and the ninth is the largest error I have made on this project.**

0. **"C7 is answered."** Retracted the same day by an adversarial audit I commissioned
   and then verified myself. **All 40,800 rows carry a ligand** — I had *printed* those
   three role counts hours earlier while checking for nulls and read "no missing values"
   instead of "no ligand-free arm", and `A_LIGAND_PRESENT`, the flag that would have
   said so, is empty on all 40,800. I caught the dead flag *beside* it and not this one.
   **Every guard I built that day worked; none could catch a wrong belief about what the
   data was.** F-23, and now G-15.


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
- **Do not quote the agonist effect as a SHARE of the partner effect at all** — that
  share spans an order of magnitude across five readouts on the same predictions, and
  the elected readout is agonist-biased by construction. *(This line read "do not quote
  both readouts for C7"; F-23 makes the stronger instruction the right one.)*
- **Do not re-derive C7 from Block C.** The file has no ligand-free arm. The redo does:
  `g2_systems.csv`, 20 receptors / 19 clusters, zero marginal cost, guarded by **G-15**
  and pre-registration drafted at `redo/spec/C7_PREREGISTRATION.md`.
- **Do not restructure `CLAIMS.md`** — lit's.
- **Do not trust the manifest to mean an input is current or code-written.** F-21, F-22.
