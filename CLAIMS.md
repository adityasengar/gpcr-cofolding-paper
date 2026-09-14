# CLAIMS.md — the argument spine

**DURABLE.** Survives a data refresh; a block landing changes which claims have
evidence, never what the claims are.

Each claim carries a `needs:` line naming the block that must supply its
evidence. A claim with an open `needs:` is not yet writable, however good it
sounds. Numbers are verified by `analysis/block_<x>/verify_claims.py`, never
quoted from a claim sheet.

## Which block defends which claim

| claim | evidence from | status |
|---|---|---|
| C1–C5 | the literature corpus alone | **ready** — written into the intro |
| C6 (peptide drives active) | **no block supplies a peptide** — see below | **not testable on A, B, C or D** |
| C7 (agonist alone does not) | **no block supplies an agonist** — see below | **not testable on A, B or D. Block C HOLDS 7,000 apo x agonist predictions and reports no state result on them — see its Q5** |
| C8 (confidence ≠ correctness) | **Block A** | **written** — 2 of 4 backbones at anchor grain |
| C9 (decomposition) | **Block B** (apo / decoy / shuffled / cognate) | **written** — occupancy 55%, α5-CT sequence 34%, family 11% prob / 17.4% logit |
| *(new)* whole-Gα co-input drives active state, at panel scale | **Block A** | **written** |
| *(new)* the effect is partner presence far more than partner identity | **Block B** | **written** |
| *(new)* ligand class is written into pocket geometry, apo arm only | **Block C** | **written** — 4 backbones, SC-C-1 |
| *(new)* ligand class is prospectively callable from one structure | **Block C** | **written, scoped** — Boltz + Protenix only; Chai and OF3 inconclusive |
| *(new)* unsteered, apo state is receptor- and backbone-specific, not bistable | **Block D** (D1) | **written** — and the four outlier cells reproduce on Block A |
| *(new)* a partner steers toward active; a state-locking nanobody does not steer toward inactive | **Block D** (D2) | **written, bounded** — every Nb anchor predates every datable cutoff |
| *(new)* MSA depth moves the predicate, by two different mechanisms | **Block D** (D3) | **written, scoped** — Boltz a clean lever; OF3 and Protenix degradation |

## Block D, and the reason its status column reads differently

**Block D shipped no row-level data.** All three corpora its claim sheet names —
42,180 predictions — are absent from the bundle; five CSVs ship and every one is
panel or reference metadata. Twelve of its twelve claims are therefore
untestable here in whole or in part, and `analysis/block_d/verify_claims.py`
records each as PROSE-ONLY beside the file that would test it.

What could be recomputed was, and it held: the panel sizes, the 22 paralog
clusters that license D3's cluster bootstrap, D1 and D2's cluster-boot
degeneracy, all six exact binomial intervals, and fifteen NPxxY hydroxyl
distances measured from the deposited coordinates. Two of the manifest's three
stated distances reproduce to the decimal, and every structural spot-check's
state call matches the claim it was chosen to illustrate.

**So Block D claims are written with their evidential class attached, not
without it.** A sentence resting on a D-tier fraction is a sentence resting on a
number we could not check, and the Methods says so once rather than the figures
saying it five times.

**Block D does not close C6 or C7.** It supplies nanobodies and whole Gα
subunits, not a 21-residue peptide and not an agonist alone. The two title
claims below remain open after four blocks.

## Block C, and what it may not be joined to

Block C varies the **ligand**, not the transducer, and it is the paper's
"read from above" leg. Two rules travel with it, both from its own dispatch and
both load-bearing:

1. **Nothing in Block C may be connected to two-state generation.** Its arms were
   not designed to test it. The 2×2 result reads as though it bears on that
   claim; it does not. Checked 2026-09-10 — no sentence in Results or Methods
   makes the link.
2. **No Block C number may be compared against a Block A or Block B predicate
   rate.** The two-instrument predicate is saturated on this panel — floor-pinned
   in apo, ceiling-pinned in cognate, ~65% of cells unresolvable — so every Block
   C result is continuous pocket-Cα geometry and the two scales are not
   commensurable.

Block C also **refuted** its own pre-registered applicability domain: the
measured slope ran opposite to the prediction. What survives is an after-the-fact
failure list, and the Results say so rather than implying the method can flag its
own failures in advance.

## TWO title claims have no evidence in any block — RETRACTION 2026-09-12

**This heading said "ONE … the agonist clause is now answered" for part of 2026-09-12. That
was wrong and is withdrawn. Both title claims are unevidenced again.**

**Why, and I verified it myself rather than on report.** `rows.tier3.v2.csv` has **40,800 rows
and three `ligand_role` levels — `full_agonist` 14,800, `neutral_antagonist` 11,600,
`decoy_lig` 14,400 — summing to the entire file with NO `none` level.** `ligand_type` is only
`peptide` (6,800) and `small_molecule` (34,000). `A_LIGAND_PRESENT` is **empty on all 40,800
rows**. So **"apo" in that file means NO PARTNER, not no ligand: the agonist alone was never
predicted, and C7 asks a question the file cannot answer.**

**My own failure here, recorded because it is the reusable part.** I changed the status of a
title clause in the argument spine on a peer session's report, four times reinforced, **without
opening the file** — when the check was one `collections.Counter` over a column that was sitting
on disk. paper-6f's error was a misread completeness check; mine was accepting a status change
to *this* document without the one command that would have caught it. **A claim that moves a
title clause is exactly the claim to verify at source, whoever reports it.**

**Found 2026-09-10 by recomputing from `data/block_b/01_rows/rows_tidy.csv`, and
it supersedes what this file said an hour earlier.**

This file previously stated that "Block B supplies the reduced 21-mer arm and
carries the titular claim." **It does not.** Block B's four arms are `apo`,
`decoy`, `shuffled` and `cognate`, and every arm that carries a partner carries
a **complete Gα subunit**. There is no peptide arm.

**What each arm actually changes**, audited byte-level in
`02_constructs/decoy_scramble_verification.md` and re-checked here (B70–B72):

| arm | partner supplied | differs from cognate |
|---|---|---|
| `apo` | none | — |
| `decoy` | the correct Gα subunit | **the last 11 residues only** — `decoy[:-11] == cognate[:-11]` byte-identical on 40/40, tail Hamming 7–11, and the scramble is a *permutation* of the same residues, so whole-sequence composition is preserved |
| `shuffled` | a **different Gα class** entirely | the whole subunit, including its own real α5-CT |
| `cognate` | the correct Gα subunit | — |

So the ladder does isolate the α5 C-terminal sequence: the decoy arm perturbs
that segment and nothing else, and the shuffled arm changes the family. **But
the segment is ELEVEN residues, not the twenty-one the title claims.** The
construct report's own column is headed "α5-CT (last 11)"; the manipulated
quantity elsewhere in the drop is `partner_tail11_helicity_frac`; and 4X1H, the
only peptide-bound entry in the reference set, is an engineered 11-mer. The
project has three independent 11-residue objects and one 21-residue title.

All five canonical α5-CT sequences in that construct table verify against
UniProt, as do all five subunit lengths.

**And there is no ligand anywhere.** `ligand_type` and `ligand_sequence` are
NaN on all 32,000 Block B rows; Block A has no ligand column at all. Both
campaigns are apo-receptor plus partner.

So of the three clauses the title and `CLAUDE.md` assert:

| clause | status |
|---|---|
| a 21-residue α5-CT peptide co-input drives the models active | **untested** — no block supplies a peptide |
| the agonist alone does not | **untested** — no block supplies an agonist |
| confidence does not track state correctness | **written from Block A** |

What the two campaigns *do* establish is narrower and still substantial: a
co-folded Gα partner drives active-state geometry at panel scale on four
backbones; the effect is mostly partner **presence**, with the α5-CT sequence
second and the correct family a small, scale-dependent third; the models do not
read partner family on the continuous axes beneath the predicate; and confidence
does not track state correctness.

### The experimental precedent is already in our own reference set

**4X1H, the active reference for OPSD, is rhodopsin bound to a Gα$_t$
C-terminal peptide alone — no full Gα subunit.** X-ray, 2.29 Å, deposited
2014-11-24, released 2015-11-04. Our own instrument calls it active on both axes:
TM6 tilt 17.586 Å against a 14.932 Å threshold, NPxxY 4.921 Å against 9.08 Å. It
is the **only peptide-bound entry among the 80 references**, checked.

**But the peptide is an 11-mer and it is not native, so this is a weaker precedent
than it first reads — and a stronger anti-memorization argument.** Checked against
RCSB and UniProt 2026-09-10, because the reference audit's phrase *"native α5-CT
donor class Gt"* does not survive contact with the deposited sequence:

- Chain C is **11 residues**, `VLEDLKSCGLF` — not a 21-mer.
- Native bovine Gα$_t$1 (UniProt P04695) ends `IKENLKDCGLF`. The deposited peptide
  differs at **four of eleven positions** (I→V, K→L, N→D, D→S). It is an
  engineered high-affinity analogue, **not the native α5-CT**.

Three consequences, in order of how badly each could bite:

1. **Do not cite 4X1H in the introduction as precedent for a wild-type 21-mer.**
   An isolated *engineered 11-mer* holding rhodopsin open is a real result and a
   fair motivating observation, but it is not the claim in our title. A structural
   referee will pull the sequence, as this check did.
2. **It strengthens the anti-memorization case.** No wild-type 21-mer α5-CT
   appears with a receptor in any deposited structure — the isolated-peptide
   precedent is exclusively short, engineered opsin entries, all pre-cutoff. A
   wild-type 21-mer is therefore not a sequence the models have seen in this
   context. That argument is quantitative and it is ours to make.
3. **OPSD is still where to start a 21-mer arm** — it is the one receptor with any
   deposited peptide-bound active structure — but the arm would be predicting a
   21-mer complex that has never been solved, so 4X1H is the *motivation* for that
   arm, not its reference. Scoring a 21-mer prediction against an 11-mer analogue
   structure would be an interface mismatch of exactly the kind recorded for 6E67.

Corrected by the lit session 2026-09-10, overwriting an entry written from the
reference audit alone. The audit's `native` annotation is wrong for this entry and
should be re-checked wherever else it appears.

**This is Aditya's decision to make, not ours.** Either the title narrows to what
was run, or a later block supplies an isolated 21-mer arm and an agonist-only
arm. Nothing in the manuscript may imply the peptide or the agonist-alone result
until one of those happens — the existing rule below now applies to Block B's
prose as well as Block A's.

## Block A is groundwork; Block B carries the titular claim

**Decided by Aditya, 2026-09-10.** The title stands. The manuscript claims a
21-residue α5 C-terminal *peptide* co-input; **Block A does not test that** — its
cognate arm supplies the whole Gα subunit, with `d_ga_alpha5_r350_ca` and
`plddt_ga_alpha5` scoring the α5 as a feature of that subunit.

Block A's job is therefore to establish, at panel scale and on four independent
backbones, that **a co-folded partner drives active-state geometry**, together
with the instrument that measures it and an honest account of what the models do
not do.

**"Groundwork" is the right internal word and the wrong published one.** Four
corpus papers build an instrument and then apply it — `ku2026promise`,
`bryant2024cfold`, `paajanen2026activation`, `liu2026ensembletests` — and none
frames the first half as setup; each claims the instrument as a contribution in
its own abstract. Block A's calibration section should assert the predicate as a
result, not as permission for what follows. **Block B supplies the reduced 21-mer arm** and carries the titular
claim; without Block A's instrument and controls it would rest on far less.

Two rules follow, and they are load-bearing:

1. **No sentence in the paper may imply the peptide result or the
   agonist-alone result.** Neither is tested. Checked 2026-09-10 across Block A
   and Block B prose; none does. Re-check whenever either is edited. Two of four
   independent figure agents wrote that the 21-mer was supplied while holding
   this file, so the framing pulls that way and a written rule is not enough.
2. **No Block A sentence may depend on Block B having run.** Block A may say
   what it does not cover; it may not say what the next experiment showed.

Of that reduced-partner contrast, Block B answered **half**. Whether occupancy
or identity does the work: answered, by the decoy and shuffled arms — occupancy,
mostly. Whether the 21-mer alone suffices: **not answered, and not asked**, for
the reason recorded above.


---

**C1. Conformational state is the thing that matters for GPCRs, and a single predicted
structure cannot express it.**
- evidence: `[georgiou2025heterogeneity]` for the multistate/rheostat picture; `[paajanen2026activation]` for apo/agonist bimodality across deposited structures
- status: **ready** — lit only, no numbers needed

**C2. Current co-folding models collapse onto one basin, and their own authors say so.**
- evidence: `[abramson2024af3 p6]` — "multiple random seeds ... do not produce an approximation of the solution ensemble", and "AF3 exclusively predicts the closed state for both holo and apo systems". Corroborated by `[ku2026promise]`, `[ye2026multistatebias]`, `[sun2026kinconfbench]`
- status: **ready** — strongest citation in the corpus

## The gap — what nobody has done

**C3. The multi-state benchmarks that exist exclude GPCR activation by construction.**
- evidence: `[ku2026promise p9]` names "GPCR TM6 displacement" as excluded in its own Limitations; the TM-score 0.8 admission rule in `[bryant2024cfold]` and inherited by `[kalakoti2026afsample3]` has the same effect without naming it
- status: **ready**

**C4. Where directional state control exists, the state is supplied by the operator,
not induced by a biological co-input.**
- evidence: `[heo2022multistate]` state-annotated templates + MSA deletion; `[yang2025statespecific]` operator declares the state and the peptide is the designed *output*; `[ferguson2026deorphann]` pinned active templates; `[lee2026confornets]` transfer label is itself a deposited structure
- **QUALIFIED 2026-09-09 and no longer true as written.** `[chiesa2025templatebias]` supplies the G protein as a co-input to AlphaFold-Multimer on 63 post-cutoff class A pairs and measures the receptor's activation state, finding that the partner beats operator-supplied active templates on TM5/TM6/TM7 (p6302, p6305). The claim must be narrowed to the four distinctions that survive: (i) whole Gα or heterotrimer, not a 21-residue α5-CT peptide, so the α5 contact is never isolated; (ii) state scored by RMSD to the deposited active reference of that same complex, not by a predicate applicable to an unsolved receptor; (iii) no decoy or scrambled-partner arm, so occupancy and identity are not separated; (iv) AF2/AFM only, no AF3-lineage backbone (they say so, p6299).
- status: **needs rewriting** — the old sentence would be caught immediately by these authors

**C5. The largest GPCR + G-protein co-folding studies supply the partner and never
verify receptor state.**
- evidence: `[matic2023gpcrome]` 825 ligand-free models, no activation criterion; `[miglionico2026atlas]` whole GPCRome, "no state criterion"; `[pandyszekeres2024gproteindb]` 5,595 released complexes, no state assigned
- **QUALIFIED 2026-09-09.** The word that has to carry the claim is now **largest**. `[chiesa2025templatebias]` supplies the partner *and* verifies state, at 63 pairs — two orders of magnitude smaller than the resources above, but it is a genuine exception and the sentence must name it rather than imply none exists.
- status: **ready with the qualification above**

## The result — what we claim

**C6. An α5-CT peptide co-input drives the active state.**
- needs: `[R-B-LADDER]` at full n, plus a defined denominator (`[R-A-RECEPTORS]`)
- status: **blocked on data** — ordering reproduces, rungs do not

**C7. The agonist alone does not.**
- **status: NOT ANSWERED. RETRACTED 2026-09-12** — this slot read "ANSWERED" for part of
  2026-09-12 and that was wrong. See `DECISIONS.md` F-23 and the retraction banner on
  `analysis/block_c/received_2026_09_12/WHAT_IT_MEANS.md`.
- **Why it cannot be answered from Block C.** Verified here directly against
  `rows.tier3.v2.csv`: **40,800 rows, `ligand_role` ∈ {`full_agonist` 14,800,
  `neutral_antagonist` 11,600, `decoy_lig` 14,400} summing to the whole file, no `none`
  level**; `ligand_type` only `peptide`/`small_molecule`; `A_LIGAND_PRESENT` **empty on all
  40,800 rows**. **"apo" in that file means no PARTNER.** Every row has a ligand, so the
  agonist-alone condition does not exist in the data.
- **What Block C did measure, and it is a real result:** **agonist versus neutral antagonist at
  a fixed partner condition.** That is a ligand-class contrast, not the agonist clause. Report
  it as what it is.
- **Three things withdrawn with it:**
  1. **The `georgiou2025heterogeneity` bridge is withdrawn and must not be used.** It rested on
     "~30–45% of the partner's shift", and **that ratio must not be quoted at all**: it is the
     largest of five available readouts (pocket-Cα 27–67%, TM6 tilt 5–17%, NPxxY-OH 3–16%,
     normalised TM6 index 4–10%, binary 5–9%), and the elected readout is **agonist-biased by
     construction** — `pocket_ca_rmsd_active` scores the pocket against a deposited **active**
     reference, which for these receptors is agonist-bound. **The share is a property of the
     readout, not of the ligand.**
  2. **The `vo2026fiducials` tension is BACK and unresolved.** p.8 still shows a high-efficacy
     agonist alone driving β2AR TM6 "almost complete outward movement", with the Gs α5 helix
     adding "less than 1 Å further outward at most positions". **The draft must still meet it
     head-on.** Note their state calls are visual with no quantitative panel — that is the only
     thing standing, and it is a weakness in their evidence, not an answer to it.
  3. **"Does not reproduce the partner effect on any backbone" is false on the readout we
     elected.** Partner minus ligand, continuous, paired within cluster, k=14: boltz
     **+0.373 [+0.111, +0.629]** and protenix **+0.487 [+0.255, +0.730]** exclude zero;
     **chai +0.143 and of3 +0.106 do not.** "No backbone" holds only on the binary predicate —
     the instrument we agreed never to quote. Do not quote the claim on either basis.
  4. *(And "survives both opsin variants" was vacuous: all 800 opsin rows are NaN on all four
     axes, so the two variants are byte-identical.)*
- **THE CONSTRUCTIVE HALF, and it changes the plan rather than only subtracting. C7 is
  answerable at zero marginal cost inside the redo, and it is already READY.** Verified here
  against `redo/inputs/g2_systems.csv`: of 313 READY rows, **98 carry
  `ligand_role_actual = none` — 41 `apo` and 57 `cognate`** — and **20 receptors in 19 distinct
  receptor clusters carry the complete 2×2**: apo/none, apo/full_agonist, cognate/none,
  cognate/full_agonist. MDE at k=19 is **0.279**, better than the decoy arm's 0.367. Group 2
  dispatches these rows already.
  **So the slot is not "a claim we have" but "a claim we are one pre-registration away from
  having".** The requirement is explicit: **name these rows as the C7 instrument and
  pre-register the contrast BEFORE dispatch.** After dispatch it is an unregistered post-hoc
  contrast, which is the weakest form of the strongest available result.
- lit support, unchanged and still standing: `[hilger2020gcgr]` — "TM6 activation is only
  triggered by the engagement of the α5 helix of Gαs" (class B, GCGR);
  `[paajanen2026activation]` p.1 — "Agonist binding shifts this conformational ensemble towards
  the active state but does not fully stabilize it. Instead, a stable active state is only
  established upon G protein binding"; `[georgiou2025heterogeneity]` printed p.3697 —
  agonist-only complexes "adopt an intermediate active conformation". **These are the corpus's
  support for C7 and they are unaffected by the retraction** — they were never resting on
  Block C.

**C8. Model confidence does not track conformational correctness.**
- needs: `[R-INFRA-AA2AR]` on a **partner-matched** subset — the current cross-backbone comparison is confounded by unequal partner mixes
- lit support: `[bryant2024cfold]` plDDT cannot select conformations; `[schafer2025confounds]`; `[junker2026peptidedesign]` PAE over-estimates for misplaced GPCR peptides
- status: **blocked on data** — one clause currently contradicted locally

**C9. The effect decomposes into occupancy, α5-CT sequence, and correct family.**
- needs: `[R-B-DECOMPOSITION]` — requires decoy and shuffled arms at full n
- status: **blocked on data**

## The spine for the one-paper form — proposed 2026-09-12 by lit-3d

Aditya has decided on one paper rather than a split. paper-6f proposed a headline and asked
whether the corpus supports a paper that shape, and which claims hang off it. **It does, and
the shape is the dominant one among the strongest papers in this corpus — but the proposed
headline has a structural flaw that the corpus's own exemplars avoid.**

### The corpus says the shape is right

**Seven of 83 papers are tagged both `threat` and `precedent`** — they supply a positive
result *and* undermine a measurement the field relies on: `bret2025boltz2docking`,
`jung2026boltzperturb`, `ku2026promise`, `mattsson2026leakage`, `skrinjar2026generalization`,
`yu2026domainmotion`, `zhang2026generalization`. So the form is not unusual; it is what the
best work in this area looks like.

### But every one of them joins the halves with a HINGE, not a conjunction

Look at how their claims are actually built:

- `bret2025boltz2docking` — "discriminates true from false hits far better than any docking
  scoring function, **yet** … insensitive to binding-site mutation"
- `zhang2026generalization` — "predicts GPCR backbones accurately (1.44 Å) **but** ligand poses
  poorly (5.95 Å)"
- `ku2026promise` — recovers all states in only 8–29% of clusters, **and the collapse is traced
  to the structure module, not the distogram**
- `bryant2024cfold` — "recovers held-out alternative conformations for 52% of targets, **but
  only** …"
- `suzuki2026conforflux` — "broadens coverage without retraining, **but** fold switching
  plateaus"
- `jedryszek2026probing` — "linearly decodable … **yet** steering them barely moves output"

**In each case the positive and the negative are about the same object, and the negative
qualifies the positive.** They are not two findings in a list.

**The proposed headline joins its halves with "and":** *"control is driven by the transducer
co-input — **and** the instruments … do not support the claims commonly made from them."* Two
findings, conjoined. **A referee will immediately ask the question the conjunction leaves
open: by what instrument, then, did you establish the first half?** And we are exposed on
that: our predicate is floor-pinned in apo (C7), our tilt axis cannot be calibrated
non-circularly, and every published active-state reference set in this field — ours included —
is defined by partner presence (`lit/analysis_review/AGONIST_ONLY_STATE_ASSIGNMENT.md`).
**As written, the instrument critique includes our own instrument and the headline does not say
how the positive survives it.**

### The hinge is already in our data — and it does NOT depend on C7

**Independence note, added 2026-09-12.** This section was written when C7 was believed answered.
**The hinge does not rest on C7 and survives its retraction**: it is a claim about how two
instruments behave on a small effect versus a large one, and both effects it uses — the
ligand-class contrast and the partner contrast — are things `rows.tier3.v2.csv` genuinely
measures. What the retraction removes is the *interpretation* of the small effect as the
agonist's contribution, not the instrument comparison. S5 and the hinge stand; only the label
changes.


**UNITS CORRECTION 2026-09-12, by paper-6f, and it was mine.** An earlier version of this
section read *"the partner effect on those same two instruments: +0.78 and ~+0.62 — stable."*
**Those are not the same quantity — +0.78 is a change in fraction-active, +0.62 is Ångström.**
They cannot be compared and "stable" was not a claim that would survive a referee. This is the
project's own compare-like-with-like failure, and it is the fourth instance.

**The comparison that IS unit-free is the ratio**, because the partner effect is the
denominator of both and the units cancel. Per-backbone, from
`analysis/block_c/received_2026_09_12/STEPS_3_TO_6.md` §"The two instruments, compared
unit-free":

| backbone | ligand as % of partner, binary | continuous | paired fold change |
|---|---:|---:|---:|
| boltz | 8.4% | 45.7% | **5.4×** |
| chai | 8.5% | 49.1% | **5.8×** |
| of3 | 9.0% | 71.1% | **7.9×** |
| protenix | 4.8% | 29.5% | **6.2×** |

**Paired range 5.4–7.9×, and the consistency is the point.** (Do **not** quote the unpaired
"3–15×" form — 3.3× and 14.8× are min-of-one-backbone against max-of-another, which is the same
pairing error in a milder costume and makes a strikingly consistent result look erratic.)

**The second finding, and this half is ours alone.** The binary predicate does not merely
compress small effects — it **inflates the apparent differences between backbones**.
Between-cluster SD in the apo arm runs **0.073–0.421** on the binary predicate (a 6× spread,
protenix at the bottom because it is pinned near 0.01 apo and 0.99 cognate) against
**0.487–0.604** on the continuous readout (1.2×). Standardised by their own SD, the partner
effect reads **0.8–12.6 SD** binary against **0.5–1.3 SD** continuous. Protenix's 12.6 is not a
huge effect; it is a collapsed denominator.

**One precision, checked here:** the binary instrument does **not reorder** the backbones —
the ranking is `protenix > boltz > of3 > chai` on *both* readouts — so the claim to make is
that it **inflates the spread between them ~5×** (15.5× against 3.0×), not that it makes them
incomparable in rank.

**A second "precision" I asserted here was WRONG, and the correction matters more than the
error.** I wrote that because chai is the weakest backbone on both instruments (0.81 and
0.45 SD), "significance" could not be claimed across all four. **paper-6f refuted it with the
intervals and is right.** I had treated `partner ÷ between-cluster SD` — a standardised
**effect size** — as though it were a test statistic, which is `effect ÷ standard error`. They
differ by √n, and with 14–18 clusters a 0.45 SD effect can exclude zero comfortably. **Effect
size and interval exclusion are different claims and I inferred the second from the first.**
Same family as the units error above: reasoning across quantities of different kinds.

**All 24 partner contrasts — 3 roles × 4 backbones × 2 readouts — exclude zero.** Chai, the
weakest: `+0.343 [+0.161, +0.537]` binary, `+0.269 [+0.116, +0.481]` continuous.
**So "sign, direction and significance" stands for the partner effect and nothing is dropped.**

### The sharpest single datum for the hinge, and it is one cell

**RE-LABELLED 2026-09-12 after the C7 retraction.** This effect is the **agonist-versus-neutral-
antagonist contrast at a fixed partner condition** — *not* "the agonist's contribution" and not
"the ligand effect" in the sense C7 asks about. Every row in `rows.tier3.v2.csv` carries a
ligand, so there is no ligand-absent baseline here. **The hinge is unaffected — it is a claim
about instrument behaviour on a small effect, and this contrast is a real small effect — but it
must be named for what it is, or it silently re-imports the retracted framing.**

**Chai, agonist versus neutral antagonist at fixed partner (apo = no partner), two instruments:**

| readout | agonist − antagonist in apo | interval |
|---|---:|---|
| binary predicate | +0.029 | **[−0.045, +0.107] — includes zero** |
| continuous | +0.132 | **[+0.055, +0.206] — excludes zero** |

**One backbone, one contrast: resolvable on one instrument and unresolvable on the other.**
That is the whole thesis in a single row, and it is more persuasive than the aggregate
fold-change because a reader can check it without accepting any aggregation. **Lead with it.**

### The hinge, as it should be written

> **The choice of instrument changes a small effect (a ligand-class contrast at fixed partner)
> five- to eight-fold, and leaves a large
> one's sign and direction untouched on every backbone and its significance on every partner
> contrast we ran — while the binary predicate most of this literature uses inflates the
> apparent differences *between* backbones about fivefold, because its variance collapses on
> the backbone that is most pinned. That is simultaneously why we believe the partner result
> and why the smaller published claims in this area should not be believed.**

The second clause is the part nobody else can make: it needs four backbones on one panel to
notice that the instrument's variance collapses on one of them.

### Claims, reorganised under it

**Headline (H).** The transducer co-input, not the ligand and not the alignment, is what drives
these models between conformational states — and the effect is large enough to survive the
instrument problems that make smaller claims in this literature unsafe.
- carried by: **C6/C9** (the partner effect and its decomposition), **C7** (the ligand
  contribution, bounded), and the MSA control
- the "not the alignment" clause needs the MSA arm; on the corpus's evidence it is a
  *control*, not a competing result — `ye2026multistatebias` already reports MSA manipulation
  failing on β2AR where the partner succeeds

**Supporting claims, each with its own evidence slot — these are the instrument half, and each
must state which of OUR numbers it also constrains:**
- **S1. Confidence separates easy receptors, not correct structures.** Constrains C8. Our own
  operational gain is +1.1 pp from a 6% seed-disagreement slice.
- **S2. A property-matched decoy is unobtainable for 5 of 16 Class A GPCRs.** Constrains the
  decoy arm and therefore C9's occupancy term.
- **S3. The tilt axis cannot be calibrated non-circularly.** Constrains C6's own predicate —
  say so; it is the strongest form of the claim, not a weakness.
- **S4. Three of four backbones pair their MSAs, so apo→cognate changes two things at once for
  them.** Constrains the decomposition in C9 and the MSA control's interpretation.
- **S5. The two readouts disagree by 4–5× on a small effect and not at all on a large one.**
  **This is the hinge claim and I would promote it out of C7 into its own slot**, because it is
  the one that licenses the headline's second clause from our own data rather than from the
  literature.

**Methods, not claims:** the verification discipline. Agreed with paper-6f — it is a property
of how the work was done, and a claim slot would invite a reviewer to score it.

### Our own instrument must be disclosed, and that is what makes the second clause credible

paper-6f has recorded `DECISIONS.md` **F-21** (a generated input can go stale against its own
inputs with no guard noticing) and **F-22** (`inputs/` is "code only" but the guard catches only
edits made *after* stamping — 31 of 64 files name no generator, and `g1_recording_spec.tsv`,
the campaign's own 47-column recording contract, **has no writer anywhere in `redo/build/`**).
Neither is fixed. Their point is right and I would put it more strongly:

**A paper whose second clause is "the instruments this field uses do not support the claims
made from them" cannot leave its own instrument undisclosed. It is not merely a fairness
problem — it is the single easiest way for a referee to dismiss the whole second clause.**
`schafer2025confounds` is the model of how that dismissal reads: *"their Paper **lacks some
essential controls** needed to assess AF-cluster's reliability"*, and *"**Controls should be
performed with the same software**."* That is a Matters Arising written against a paper that
criticised others' methods.

**The corpus's own evidence is that disclosure buys credibility rather than costing it.**
`yu2026domainmotion` is the clearest case: routes 1, 2, 3, 4 and 6 all clean and *said to be*,
templates off and stated, full distributions rather than best-of-N — and it is the paper in
this corpus whose negative result is hardest to argue with. Its authority comes from what it
discloses, not from what it claims.

### What changed 2026-09-12, and the distinction worth drawing

**F-22's clearest instance is closed, and the difference matters.**
`g1_recording_spec.tsv` — the 47-column contract every delivered run must satisfy — was
hand-made, read by three scripts and written by none. It now has a generator; the rows are
code; `--check` regenerates and diffs; the unattributed count goes 31 → 30. Moving it changed
**zero** rows' non-empty content. **And it gained `pocket_ca_rmsd_active` and
`pocket_ca_rmsd_inactive`**, named to match what `rows.tier3.v2.csv` already carries.

**That last part is the one that belongs in the paper.** The readout the hinge's second clause
depends on is now **declared in the contract before dispatch**, not merely known after the fact
to have been the better instrument. The honest sentence is *"we fixed it before dispatching"*,
not *"we know our readout was inadequate"* — and those are genuinely different claims about the
same finding.

**The by-product is stronger evidence than the fix.** Making the contract into code revealed
that **10 of its 47 rows were ragged** — four tabs where five belonged — and **nothing had ever
parsed it strictly enough to notice**, across three consuming scripts. **That is this paper's
own thesis happening to this paper's own machinery**: an instrument that everything depended on,
that nobody had verified, whose defect was invisible because no consumer checked. We found it,
in our own contract, before the campaign ran. **Disclosed, that is the strongest credential the
instrument critique can have** — it is the difference between a paper that asserts the field
does not verify its instruments and one that demonstrates the failure mode on itself and says so.

**Two things not to overclaim, both of which belong in the same paragraph.**
- **A generator is not correctness.** `--check` regenerating and diffing proves the file is
  *reproducible*, not that it is *right*. A reproducibly generated file can still be stale
  against its inputs — which is **exactly F-21**, and F-21 is open and unfixed. Do not let the
  F-22 fix be read as covering it.
- **30 of 64 inputs still name no generator.** One instance closed is one instance, and the
  count should be given as a count.

**So, for Methods:** F-21 and F-22 are named there, as stated limits, in our own words before
anyone else's, with the F-22 instance recorded as closed **and** the residual 30 given. And **S3 is the load-bearing instance** — our tilt axis cannot be calibrated
non-circularly, and every published active-state reference set in this field including ours is
defined by partner presence. **Conceding S3 explicitly is what licenses us to say the same of
everyone else.** A supporting claim that indicts the field and exempts us would be the weakest
paragraph in the paper.

**One scope check on the hinge, which survives this.** Its second clause is already scoped to
*"the smaller published claims in this area"* — claims, not instruments in general — which is
what our data can evidence and which does not exempt us. Keep that scoping exactly; widening
it to "the instruments" would make it a claim about our own measurement too, and we would then
owe a verification we cannot currently give.

### One thing I would not do

**Do not let the instrument half become a survey.** `schafer2025confounds` is instrument
critique alone and it is a Matters Arising, not a paper. The corpus's `threat`+`precedent`
papers all anchor the critique to **one** positive measurement. Five supporting claims is
already at the limit; a sixth would turn the paper into the split Aditya has decided against.

## E0.2 is answerable now — and the sentence in intro.tex needs a companion, not a correction

**2026-09-14.** `intro.tex:325–332` ends: *"A usable state criterion therefore has to be fixed
before the data are seen, reported with its threshold, and checked against a second, independent
readout so that its disagreement rate is known rather than assumed. **No study in this corpus
reports such a rate.**"*

**That sentence is still true and should not be changed on grounds of falsity.** It is scoped to
the corpus, which is the correct scope, and no corpus study reports such a rate. What has changed
is that **we can now report one ourselves**, so the sentence has stopped being an observation and
become a setup — and a setup has to be discharged.

**What we can report** (paper-6f, from held Block D data, `a100_index` already computed on 38,820
predictions by `redo/protocol/received/axes.d9c646af.py`): our two-instrument conjunction against
the published **A100** index of `[ibrahim2019a100]` — **D1 88.3% agreement on n = 14,000; D3 90.8%
on n = 22,860**, with a consistent asymmetry in both blocks: **the published index calls more
predictions active than our conjunction does** (ours-inactive/A100-active 9.4% and 5.4%, against
2.3% and 3.9% the other way).

**Three constraints on how that may be written. All three are load-bearing and the first is the
one a referee will find.**

1. **Do not call A100 "independent" without saying in what sense.** On our own data
   `r(a100_index, TM6 tilt) = +0.846 / +0.764`. **It is not axis-independent from our tilt
   instrument; it is independently *published*.** Those are different claims and only the second
   is ours to make. A sentence that says "an independent readout" unqualified will be read as the
   first and is wrong.
2. **Ibrahim validated on 268 X-ray structures; ours are predictions.** Worth doing, but it is
   not the validation that paper performed, and the sentence should not borrow its accuracy
   figures as though it were.
3. **The A100 definition we computed with is a relay** — our pipeline's reading of a paper none
   of us has seen (closed access, ACS bot-walled). The five BW pairs, five coefficients and
   intercept are in `notes/ibrahim2019a100.md` marked as such. **A transposed coefficient would
   be invisible to every check available to us**, so the numbers must be checked against the PDF
   before any of them is printed.

**Drafting note: I have deliberately not written the replacement prose.** Numbers are now
entering this sentence, and `CLAUDE.md`'s two-pass rule says that is exactly when the
retrieve-and-draft separation must be restored. The constraints above are the retrieval half;
the sentence is for whoever holds the drafting seat.

**Two free follow-ons the corpus has now put in reach**, neither run: `[ibrahim2019a100]`'s
*"many active nanobody structures are predicted to be weakly active"* is directly testable
against **Block D2's nanobody arms**, and its **2:1 intermediate split** against the **21 Class A
Intermediate structures** E0.1 measured. If either disagrees with our labels, that is an
instrument finding we own rather than inherit.

## Threats a reviewer will raise — plan the response now

| threat | source | current position |
|---|---|---|
| the isolated peptide does **not** stabilise the active state without agonist | `[tran2026nanogs p8]` wet-lab, verbatim | ours is a *prediction-model* input, not a solution-phase equilibrium. State this explicitly; do not let it read as contradiction. |
| agonist alone nearly suffices at β2AR | `[vo2026fiducials p8]` | see C7 |
| partner-induced changes are predicted **worse** than ligand-induced | `[ku2026promise]` (their term is "protein-induced") | our result runs against this; engage it rather than omitting it |
| **a ligand known NOT to bind reproduces the conformational change** | `[yu2026domainmotion, Significance/Discussion]` — 82 enzymes, 500 AF3 models per condition, no templates | **the sharpest published challenge to our decoy arm.** They show the training-set prior (40.3 pp between apo- and holo-dominated enzymes) is 3–4× the ligand effect (9.1–17.5 pp), and that ligand pLDDT is "generally not sufficient for discriminating between binder and nonbinder ligands". Our decoy and shuffled arms are exactly the control they call for, so this is answerable — but the answer must be quantitative and must cite them by name. Added 2026-09-09. |
| co-folding wins only near training distribution | `[skrinjar2026generalization]`, `[roehrig2026docking]` | needs our anti-memorization arm — Block C claims it survives; verify when data lands |
| sequence-identity splits do not stop leakage | `[mattsson2026leakage]` | directly exposes our generalisation framing |
| **Boltz-2's output can be insensitive to target shuffling and to binding-site mutations that abolish binding** | `[bret2025boltz2docking]` — 943 screening hits, 10 mostly-GPCR targets | adjacent to our **shuffled arm** on one of our four backbones. Different quantity (affinity head, not geometry) and different shuffle direction, so not a refutation — but the response must be that we read receptor geometry, not an internal score. Sits with `[masters2025physics]`. Added 2026-09-09. |

---

## Refresh procedure — when new data lands

1. Extract the new block to `data/block_<x>/`, read-only.
2. Write `analysis/block_<x>/verify_claims.py` and run it: it recomputes every
   checkable number in that block's claim sheet from its tidy files.
3. Record every disagreement in `analysis/block_<x>/DISCREPANCY_REPORT.md`.
   **The data wins over the claim sheet, always.**
4. Update the claim-to-block map above. Invoke the `blockintake` skill, which
   carries the eight failure classes Block A hit.
5. Re-check every `blocked on data` claim above and flip the ones that clear.
