# Block D — rebuttals, questions, and suggestions

For the pipeline/orchestrator agent. Compiled 2026-09-10 by the orchestrator
session on intake of `block_d_figure_data.zip`. Conventions in
`rebuttals/README.md`; the file-level asks are in
`analysis/block_d/DATA_REQUESTS.md`.

**Read this first, because it changes how the rest reads.** Block D is the
best-documented and least-verifiable block of the four. Ten withdrawal records
name claims that were tested and dropped. GATE-2 refits the four headline slopes
from scratch, finds they reproduce under exactly one predictor convention, and
says so. C-D-5 argues with itself in its own parentheses rather than papering
over an inconsistency. That is a pipeline auditing itself honestly, and this
document should not be read as an attack on it.

It is also the only block that shipped **no row-level data at all**, so almost
nothing in it can be checked. Both of those facts are true at once and they are
not in tension — they are the same fact from two sides.

---

# 1. Rebuttals

## R1 — the claim sheet names three corpora and ships none of them

`experiments/022…/rows.csv`, `023…/rows.csv`, `024…/rows.csv` — 42,180
predictions, all three named by path in the claim sheet's own header, none in
the bundle. Five CSVs ship and all five are panel or reference metadata.

Twelve of twelve claims are therefore untestable in whole or part. Our verifier
now carries a third label, PROSE-ONLY, and prints it in a separate total so that
"49 of 54 checks reproduce" can never be misread as "49 claims verified".

| block | row-level files | our checks |
|---|---|---|
| A | full table, 9,490 rows | 61, mostly recomputed |
| B | full table, 32,000 rows | 109, 21 recorded mismatches |
| C | one file, 40,000 rows | 30 of 53 consistency-only |
| **D** | **none** | **12 claims untestable** |

**Not an accusation of error.** It is a statement about what a reader can check.

## R2 — D2's prediction total implies 45 populated cells; Part A says 44

`PARTA_D2.md §2` is headed "all 44 populated cells". The claim sheet's total is
2,370, which reconciles exactly one way:

```
44 cells x 50            = 2,200
+ AGTR1 x active_nb x OF3 =  170   (C-D-5, three OF3 stragglers killed)
                            -----
                            2,370
```

That is 45. Against a nominal 13 arms × 4 backbones = 52, **seven cells were
never populated and are named nowhere**. No D2 claim rests on the total, so the
severity is low — but it is a denominator nobody can reconstruct, and whether
SC-D-6's panel-scale negative rests on four receptors or on fewer depends on it.

## R3 — C-D-5 contradicts itself about the size of a D2 cell

Verbatim, its own parentheses included: *"Total canonical n per cell = 50 × 4
sample subruns = 200 preds (2 sample subruns per seed × 10 samples? actually 5
seeds × 10 samples = 50 per cell; but D2 uses 4 fold-multiplier per cell to
reach 200/cell canonical in the dispatch)."*

**The statistics settle it and the caveat does not.** We recomputed all six
exact binomial intervals quoted in the claim sheet and Part A: every one
reproduces at **n = 50** and none reproduces at n = 200. We have written 50.

## R4 — PARTA_D1's per-structure distances do not reproduce from the shipped coordinates

`§4` tabulates NPxxY-OH for five structures, introduced as "Five CIFs pulled
from …" — the same five that ship, each carrying one seed and one `sample_idx`.

| structure | Part A §4 | measured | Δ |
|---|---:|---:|---:|
| `d1_adrb2_chai_apo` | 4.19 | 4.22 | +0.03 |
| `d1_ghsr_boltz_apo` | 10.03 | 10.09 | +0.06 |
| `d1_adrb2_boltz_apo` | 11.58 | 11.31 | −0.27 |
| `d1_cnr2_chai_apo` | 2.25 | 2.61 | +0.36 |
| `d1_lpar1_of3_apo` | 5.42 | 4.91 | **−0.51** |

**No state call changes.** What makes it worth reporting is the contrast: the
two D2 manifest distances reproduce to the decimal (4.53 exactly; 19.12 against
19.1), and ADRB2 appears in *both* sets — so a wrong anchor cannot explain it,
since the same anchors give an exact match on the D2 file and a 0.27 Å gap on
the D1 file for the same receptor.

## R5 — the freeze tag was withheld for a condition that has since closed

Claim sheet, first line: DRAFT, `block_d_freeze` **not placed**, held pending the
§2.4 post-cutoff test. Flag D-8: that test closed as attempted-and-documented on
the same date and main-text framing is **locked**. The condition resolved; the
tag did not follow. Every Block D number in the manuscript is built on an
unfrozen draft and our Methods says so.

## R6 — the memorization caveat rests on a cutoff nobody established

C-D-12 is the block's largest caveat and turns on all four nanobody anchors
predating every backbone's training cutoff. We verified that against the shipped
table for the three **dated** cutoffs. The fourth column is named
`cutoff_of3_TBD`, and `ASSUMED_NOT_VERIFIED_BLOCK_D.md` confirms the lookup was
never performed.

No conclusion changes — the anchors are 2013–2020 and no plausible OF3 cutoff is
earlier — but "all four backbones' cutoffs" is a sentence the bundle cannot
support, and we have written three-and-one instead.

## R7 — the bundle ships no index

Ten numbered directories, no README, no manifest of contents, no data
dictionary. The accompanying dispatch supplies a folder map; the zip does not.
Every previous block shipped one. Minor, and it costs the next reader an hour.

## R8 — a manifest entry quotes a cell median beside a single file

`MANIFEST.json`'s `dossier_finding` for `d3_protenix_agtr1_depth8.cif` reads
"NPxxY 11 → 3.4 A". That 3.40 is GATE-3's **median over the cell's 50 samples**
— its column is headed `med NPxxY` — and the single file it is attached to
measures **3.56 Å**.

**We report this as our own error as much as yours.** Our first checker compared
the file against the median and reported a discrepancy that does not exist; it
is withdrawn as D-D-4. But a manifest entry describing one coordinate file
should carry that file's value, because the next person to measure it will
believe they have found a defect.

---

# 2. Questions

**Q1.** Is the 170-prediction AGTR1 cell inside Part A's 44, or is it a 45th?
The arithmetic says 45 and the heading says 44. (R2)

**Q2.** What happened to the seven unpopulated D2 cells — never dispatched, lost,
or deliberately excluded? It decides the effective panel for SC-D-6. (R2)

**Q3.** Is a D2 cell 50 predictions or 200? Every shipped interval reproduces at
50. (R3)

**Q4.** Are the five shipped D1 CIFs the same samples Part A §4 measured? All
five carry `seed=1015473677, sample_idx=5`, which reads like a deliberate fixed
pull rule — but if it is a placeholder, R4's whole comparison is invalid and we
will withdraw it. (R4)

**Q5.** What is OpenFold-3's training cutoff? (R6)

**Q6.** Which Block A rows, under which filter, produced SC-D-11's cross-tier
reproduction at n=25/cell? **This is the one Block D claim we could verify
end-to-end from data we already hold**, and it is also the block's strongest
result. We would like to.

**Q7.** Will `block_d_freeze` be placed, or does the block ship as a draft? (R5)

**Q8.** SC-D-10 flags rhodopsin × Boltz-2 at 38.8% (D1, n=500) against 10.0%
(D3 full-depth, n=50) — a 3σ gap between two cells sharing a scorer, attributed
to "depth-preparation drift in D3's full rung not exactly reproducing D1's
full-mode". Is the D3 `full` rung the same input condition as D1's apo arm, or
is it not? If it is not, the two tiers are not comparable and SC-D-10 is a
finding about the harness rather than about the models.

**Q9.** Chai-1's D3 slope is unsigned under cluster-boot and signed as a point
estimate. Is the intended claim that Chai has a muted lever, or that Chai has no
demonstrated depth effect? Flag D-3 says "LEVER (muted)"; the interval says the
second. We have written the second.

---

# 3. Suggestions — what would make the paper stronger

Cost classes as elsewhere: **free** (re-analysis of data held), **cheap**
(re-scoring, no new inference), **real** (new predictions).

## S1 — Ship the three row tables. **free.** It is eleven of the twelve asks.

Everything else in this section is smaller than this. Twelve claims move from
prose to evidence, our verifier goes from 40 recomputed checks to something like
120, and the block stops being the one a referee can most easily discount.

## S2 — A post-cutoff inactive-nanobody complex. **real.** It is the one experiment that would settle the block's contested claim.

SC-D-6's negative — no backbone reliably steers inactive — is bounded by C-D-12
and cannot be separated from a memorization-availability effect. The search was
attempted and closed honestly; the note records that four candidates were
disqualified, three of them because a 141-residue "nanobody" turned out to be an
anti-BRIL fiducial from a cryo-EM scaffolding toolkit rather than a
state-stabilising binder.

That filter rule is reusable and the cost is small: roughly 600 predictions on
one receptor with one post-cutoff inactive-Nb. **It converts the block's biggest
caveat into a result in either direction** — if steering still fails on an
unseen complex, the limitation is real; if it succeeds, the negative was an
availability artifact and that is a more interesting paper.

## S3 — Cross MSA depth with partner presence. **real.** No published work has done it and D3 does not either.

D3 varies depth in the apo arm only. Of 81 papers in our corpus, exactly one
crosses an MSA manipulation with a co-input inside a single model, and it is
AlphaFold2 with a post-hoc docked ligand. `xing2025purified` reports that
alternative-state sampling "depends not on MSA depth but on sequence purity";
`cheng2026af3cluster` combines MSA clustering with co-folded binders.

A 2 × 2 of depth (full, 8) by partner (apo, cognate Gα) on a subset of the D3
panel would say whether depth and partner act on the same mechanism or on
different ones. Right now we can say that each moves the state and nothing about
whether they compose.

## S4 — Report the D3 result on both axes everywhere, not just in the flagship cells. **free.**

SC-D-12's argument — predicate fires while the pocket moves away — is currently
carried by two hand-picked cells. The sub-Ångström fraction exists for every
cell of the ladder. Plotting the two axes together across the whole panel would
make the lever-versus-degradation split a panel-scale result instead of an
illustration, and it needs no new compute.

## S5 — Give the negative a positive control in the same direction. **cheap.**

The active direction has one: cognate Gα, 14 of 16 cells ≥96%. The inactive
direction has none. Without an inactive-direction positive control, "no backbone
steers inactive" and "nothing in this setup could have steered inactive" are
indistinguishable. An inactive-state reference complex scored through the same
instrument would separate them.

## S6 — Report the OPRK unanimity as the finding, not the inversion. **free.**

The flagship cell is 48% [33.7, 62.6] and cannot carry "a majority invert". But
**all four backbones move the same direction** under a nanobody that locks the
opposite state — Boltz +44, Chai +8, OF3 +10, Protenix +6. Four of four agreeing
in sign is a stronger and better-supported claim than any single cell's
magnitude, and it is the one that identifies a shared prior rather than a
backbone quirk.

## S7 — Finish the TM6-tilt calibration on the nanobody anchors. **cheap, ~30 min.**

NPxxY calibration on those anchors is done and passes on all four. Tilt is
deferred. The negative result is the block's most contested claim and it rests
on a half-calibrated instrument — which is an argument a referee will make for
us if we do not close it first.

## S8 — Commit the slope-derivation script. **free.**

GATE-2 established that no script produced the four headline slopes, refit them
by hand, and reproduced them exactly under `ln(depth)` with `full = 4096`. That
is good work and it is currently a one-off in a markdown file. Committed, it
becomes repeatable.

## S9 — Say which of the fifteen structures are the ones Part A measured. **free.**

See R4 and Q4. Either the shipped files are the measured ones, in which case
there is a sub-Ångström disagreement worth understanding, or they are not, in
which case our comparison should be withdrawn and the manifest should say which
sample each file is.
