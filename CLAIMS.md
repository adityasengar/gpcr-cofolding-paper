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

## Two title claims have no evidence in ANY of the four blocks

**Found 2026-09-10 by recomputing from `data/block_b/01_rows/rows_tidy.csv`, and
it supersedes what this file said an hour earlier.**

This file previously stated that "Block B supplies the reduced 21-mer arm and
carries the titular claim." **It does not.** Block B's four arms are `apo`,
`decoy`, `shuffled` and `cognate`, and every arm that carries a partner carries
a **complete Gα subunit**. The decoy arm scrambles the last 9–11 residues of the
α5 C-terminal tail *within* a full-length subunit that is byte-identical to its
parent over the first 339–349 residues. There is no peptide arm.

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
- needs: `[R-B-LADDER]` ligand arm vs cognate arm
- lit support: `[hilger2020gcgr]` — "TM6 activation is only triggered by the engagement of the α5 helix of Gαs" (class B, GCGR)
- **must engage:** `[vo2026fiducials p8]` shows a high-efficacy agonist alone drives β2AR TM6 "almost complete outward movement", with the Gs α5 helix adding "less than 1 Å further outward at most positions". This is the strongest counter to C7 in the corpus and the draft must meet it head-on, not omit it. Note their state calls are visual, with no quantitative panel.
- status: **blocked on data + needs an argued position on vo2026fiducials**

**C8. Model confidence does not track conformational correctness.**
- needs: `[R-INFRA-AA2AR]` on a **partner-matched** subset — the current cross-backbone comparison is confounded by unequal partner mixes
- lit support: `[bryant2024cfold]` plDDT cannot select conformations; `[schafer2025confounds]`; `[junker2026peptidedesign]` PAE over-estimates for misplaced GPCR peptides
- status: **blocked on data** — one clause currently contradicted locally

**C9. The effect decomposes into occupancy, α5-CT sequence, and correct family.**
- needs: `[R-B-DECOMPOSITION]` — requires decoy and shuffled arms at full n
- status: **blocked on data**

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
