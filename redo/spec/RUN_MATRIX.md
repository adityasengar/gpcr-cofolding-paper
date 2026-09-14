# RUN_MATRIX.md — what actually runs, on which subset, at what cost

Compiled 2026-09-11. Input to the redo that supersedes Blocks A–D. Companion to
`redo/spec/CATALOGUE.md`, which ranks 33 candidate experiments.
This document does not re-rank them. It answers the question the catalogue
leaves open — *given that we cannot run the full crossing, what is the run plan?*

Every number here is either recomputed from a file named beside it, or labelled
an estimate with its arithmetic shown. The two companions reproduce all of it:

```bash
python3 redo/build/matrix_power.py     # the power arithmetic
python3 redo/build/matrix_cost.py      # the cost arithmetic
```

**Panel membership and partner sequences are not decided here.** Sibling sessions
own `redo/spec/PANEL.md` and `redo/spec/SEQUENCES.md`, and both landed
while this was being written. **This document is costed against their decisions**
— PANEL.md's tier C1 (64 receptors, 32 paralog clusters) and SEQUENCES.md's
11-rung ladder — and §10 records where my design and theirs disagree and which
way I resolved it.

---

## The one-paragraph answer

The full crossing on the panel that was actually chosen is **1,792,000
predictions** for the core ladder alone and **5,632,000** with the catalogue's
control arms — **14.4× and 45.2×** everything ever delivered (§1). It is not
affordable and, more importantly, **most of it is statistically redundant**.
Three facts recomputed from our own rows say where the redundancy is: (a) cutting
predictions per cell from 50 to 10 costs at most **0.002** of the 95% half-width
on every pooled contrast in Block B, because 385 of 576 cells are pinned at 0 or
1 and the interval is set by cluster count, not sampling depth (§2.1); (b) the
panel's statistical n is **paralog clusters, not receptors** — 64 receptors are
32 clusters, so half the census is statistical duplication and one-per-cluster
buys the same interval for half the compute (§2.2); (c) the deep-apo floor the
brief asks about is already unanimous at n=25 on two independent corpora, so
re-running it at 500 samples buys one sentence and nothing else (§6). Spending
those three savings on **arms** instead of on repeats gives a plan at **46k /
155k / 250k predictions** across three budget tiers (§7) — the middle one costing
about what Blocks A–D cost in total, once, on a design that answers what none of
them could.

---

# 1. The full factorial, priced

## 1.1 The axes

| axis | levels | source |
|---|---:|---|
| receptor | **64** (PANEL.md tier C1, the Class A both-state census) | `redo/spec/PANEL.md` §5; 32 paralog clusters |
| backbone | 4 | boltz / chai / of3 / protenix, `data/block_b/01_rows/rows_tidy.csv` |
| partner rung | 7 (R0_apo, R1_ct11, R2_ct15, R3_ct21, R4_a5helix, R5_a5plus, R7_full) | `redo/spec/SEQUENCES.md` §1 |
| ligand class | 4 (none / agonist / antagonist / decoy) | `data/block_c/12_g4_off_site_census/g4_full_census_v2.csv`, `role` ∈ {full_agonist, neutral_antagonist, decoy_lig} + the no-ligand condition |
| MSA depth | 5 (8 / 32 / 128 / 512 / full) | `data/block_d/07_partA/HEADLINE_D3_tier_d3_full_2026_09_08.md:12` |
| predictions per cell | 50 (5 seeds × 10 samples) | `data/block_b/README.md:6-10`, recomputed: all 640 cells exactly 50 |

## 1.2 The multiplication, written out

```
   64 receptors          (PANEL.md tier C1)
 ×  4 backbones
 ×  7 partner rungs      (SEQUENCES.md ladder, excluding the a5-null controls)
 ×  4 ligand classes
 ×  5 MSA depths
 × 50 predictions per cell
 ─────────────────────────
 =  1,792,000 predictions        core ladder only
```

With the catalogue's control arms folded into the partner axis — the 7 ladder
rungs plus SEQUENCES.md's 3 α5-null variants (`R6a_da5`, `R6b_a5perm`,
`R6c_a5polyA`), 3 non-Gα bulk controls (E1.2), 4 composition controls at peptide
length (E1.3), family swap (E1.4), Gi/Gt pair (E1.6), heterotrimer `R8_hetero`
(E1.7), 2 uncoupling mutants (E1.8), 1 arrestin construct (E7.6) = **22 arms**:

```
 64 × 4 × 22 × 4 × 5 × 50 = 5,632,000 predictions
```

## 1.3 How far over budget

Delivered to date, recomputed: A **9,490** (`data/block_a/01_rows/block_a_rows.csv`),
B **32,000** (`data/block_b/01_rows/rows_tidy.csv`), C **40,800** landed
(`data/block_c/01_claims/BLOCK_C_CLAIM_SHEET.md:15-22`; the census file itself
holds the 40,000 that passed), D **42,180** claimed and zero shipped
(`data/block_d/08_dossier/EXPERIMENT_DOSSIER_BLOCK_D.md:13`). **Total 124,470.**

| | predictions | Block-B drops | × everything ever run |
|---|---:|---:|---:|
| core full factorial | 1,792,000 | 56 | **14.4×** |
| + every control arm | 5,632,000 | 176 | **45.2×** |

## 1.4 In GPU-hours — and why the bracket is 6.6× wide

> **CORRECTED 2026-09-14.** This section said **13×** in four places and that is the
> wrong ratio. 13.2× is *planning estimate ÷ measured apo rate* — an apo-to-planning
> comparison. The three two-chain scenarios `matrix_cost.py` actually prices span
> **2.0× → 13.2×**, i.e. a **6.62× spread in H100-hours** (MINIMAL 577 h → 3,822 h).
>
> **And the deeper problem, which asking for a wall-time will not fix:** chain-B
> length enters the cost model **nowhere**. `size()` is `panel × backbones × arms × n`,
> and all three multipliers are derived for a **394-residue full Gα** (774 tokens). A
> 21-residue chain B is 401 tokens — **1.06–1.11×, below the model's own floor of
> 2.0×**. So a single measured two-chain number would not close the bracket; it would
> reveal that the model prices the cheap rungs at full-Gα rates.
>
> **The fix is already made and costs nothing.** `g1_recording_spec.tsv` now carries
> `wall_seconds` (column 77), so the cost-versus-chain-B-length curve falls out of the
> campaign across all seven rungs at zero extra GPU time, and ask P1 retires itself.

**The one measured throughput anywhere in four blocks**
(`data/block_d/07_partA/HEADLINE_D3_tier_d3_full_2026_09_08.md:3-6`):

> "D3 full drained 2581/2600 rows (99.3 %) on 25 H100 workers in ~6.5 h wall …
> rescored to 25,810 predictions"

`25,810 / 6.5 h / 25 workers = 158.8 preds per H100-hour = 22.7 s per prediction`.
**D3 is apo only** — one chain, median 380 Cα (`data/block_d/06_gate_reports/GATE_3_STEERING_VS_DEGRADATION.md`,
`med_n_ca`). The only two-chain figure on disk is a planning estimate that was
never validated (`data/block_d/05_state_check/BLOCK_D_S2_4_POST_CUTOFF_SCOPING.md:99-100`):
"600 preds × ~5 min/pred on H100 = ~50 GPU-hours" — **13.2× the measured apo rate**.

A receptor (≈380 aa) plus a Gα (350–394 aa, `data/block_b/02_constructs/construct_build_report.md`)
is ≈774 tokens against 380, so a pairformer-quadratic guess is 4.2×. **ESTIMATE**,
three scenarios:

| | 2.0× (linear) | 4.2× (quadratic) | 13.2× (planning) |
|---|---:|---:|---:|
| core factorial, H100-hours | 22,565 | 46,808 | 149,333 |
| …days wall on the 25-worker pool | 38 | 78 | **249** |
| + controls, days wall | 118 | 245 | **782** |

The two-chain bracket — **6.6×**, see the correction at §1.4 — is the single biggest
unknown in this document. Ask **P1** in §8 no longer needs answering by message: the
`wall_seconds` column measures it during the campaign. Corpus anchors for context, none of them our workload:
`tang2026steeraf` [p.6] is the only per-method GPU-hour table in 81 papers —
Boltz-sample 0.42 GPU-h per target at 500 samples = 3.0 s/sample, monomer;
`passaro2025boltz2` [p.42] quotes "Boltz-2 20 GPU sec" for a *ligand* inference in
an affinity benchmark. **Do not scale this campaign off either.** Our own D3
drain is the exact workload for the apo leg and the honest floor for everything
else.

---

# 2. Why the full crossing is the wrong target, in three measurements

Not an excuse — a measurement. Each of these is recomputed from our own rows.

### 2.1 Sampling depth is nearly free variance
`python3 redo/build/matrix_power.py depth`

385 of 576 Block B cells (**66.8%**) sit at exactly 0 or 1. Mean within-cell
`p(1−p)` is **0.0386**, so the binomial variance contributed by sampling is
**0.00077 at n=50** against a between-cluster variance of **0.036–0.058**. The
sampling term is **1.3–2.1%** of the total. Consequence, measured not argued:

| predictions per cell | total preds (576 cells) | cognate−apo | decoy−apo | cognate−decoy | cognate−shuffled |
|---:|---:|---|---|---|---|
| 50 | 28,800 | +0.725 ± 0.074 | +0.390 ± 0.076 | +0.335 ± 0.094 | +0.082 ± 0.035 |
| 20 | 11,520 | +0.724 ± 0.074 | +0.390 ± 0.076 | +0.334 ± 0.095 | +0.081 ± 0.036 |
| **10** | **5,760** | +0.724 ± 0.074 | +0.388 ± 0.078 | +0.336 ± 0.096 | +0.080 ± 0.037 |
| 5 | 2,880 | +0.721 ± 0.077 | +0.390 ± 0.080 | +0.331 ± 0.097 | +0.082 ± 0.039 |

**50 → 10 costs ≤0.002 of half-width and saves 80% of the compute.** The point
estimates are stable to 0.004. (Sanity: at n=50 these reproduce the catalogue's
shipped decomposition — +0.400 [0.334, 0.464], +0.333 [0.242, 0.432], +0.082
[0.047, 0.127] — to within 0.01 on every term.)

Block C reached the same conclusion independently by a different route
(`data/block_c/11_manuscript_narrative/SIGNAL_RECOVERY_REPORT.md:76`): σ²_seed
0.0004 against σ²_within-seed 0.0023, ratio 0.11, verdict **"MORE_SAMPLES_PER_SEED:
for future dispatches at fixed compute, more samples per seed reduces uncertainty
faster than more seeds."** So when the cell shrinks, **cut seeds before samples**:
the wide-tier cell is **2 seeds × 5 samples**, not 5 × 2.

### 2.2 The statistical n is clusters, and it is about half the receptor count
`python3 redo/build/matrix_power.py clusters`

**On the panel that was chosen:** PANEL.md tier C1 is **64 receptors in 32 paralog
clusters** (§5 of that document), so the census doubles the receptor count while
raising the bootstrap n from Block B's 24 to 32. Every interval in the paper
scales as 1/√(clusters), not 1/√(receptors) — that is the single fact that decides
which reductions are free and which are not, and it is demonstrated below on the
panel we actually hold rows for.

Recomputed from `cluster_id` in `data/block_b/01_rows/rows_tidy.csv`: **26 paralog
clusters over 40 receptors**, 14 singletons, largest cluster 3 (`muscarinic` =
ACM1/ACM2/ACM4; `serotonin` = 5HT1B/5HT2C/5HT5A). Four receptors carry **no NPxxY
axis at all** — EDNRA, EDNRB, GRPR, HRH3, all 3,200 of their rows — which is Block
B's own frame_36 (`data/block_b/README.md:84-90`) and costs three clusters.
**Effective clusters for a two-axis predicate: 24.**

Bootstrap is over clusters (`data/block_d/02_caveats/C-D-1_cluster_boot_degeneracy_d1_d2.md`),
so 24 is the real n for every pooled interval — and 12 of the 36 measurable
receptors are statistical duplicates of a cluster-mate.

| panel | receptors | clusters | cognate−apo hw | cognate−decoy hw | cost |
|---|---:|---:|---:|---:|---:|
| all measurable | 36 | 24 | 0.073 | 0.096 | 1.00 |
| **one per cluster** | **24** | **24** | **0.083** | **0.097** | **0.67** |
| one per cluster | 17 | 17 | 0.098 | 0.115 | 0.47 |

**Dropping 36 → 24 receptors costs ≤0.010 of half-width for a 33% saving.** That
is the cheapest real reduction available and it is pre-registrable (§3.1).

**Carried onto C1**: one representative per cluster gives **CORE-32 — 32
receptors, 32 clusters, half the cost of the full 64-receptor census for an
interval penalty of ≤0.010.** This matters more than it looks, because it is
strictly better than the reduced core PANEL.md offers as its fallback: **tier C1r
spends 29 receptors to buy 21 clusters; CORE-32 spends 32 to buy 32.** Three more
receptors, eleven more clusters, and every pooled half-width ~20% narrower. C1r's
rule (both references ≤3.00 Å) filters on structure quality, which is a good rule
for a different purpose — it is not a rule for maximising bootstrap n. See §10.

### 2.3 Backbone and depth do not both need the whole grid
Everything the paper claims across backbones is a **main effect** (does the ladder
rise on all four). Everything it claims about depth is currently apo-only. There is
no claim anywhere in `CLAIMS.md` that requires a depth × backbone × rung × ligand
cell. Crossing depth against all four backbones multiplies by 4 to answer a
question nobody is asking — the reference backbone answers it, and one confirmation
arm on the other three tests whether it generalises.

---

# 3. The subsetting strategy

The design is a **staged funnel**, not a fractional factorial.

**Why not a fractional factorial.** The literature session swept all 81 corpus
papers: **there is no fractional-factorial, Latin-square or formal reduced-design
precedent in this field at all.** A referee would meet it for the first time in our
paper, and would have to evaluate the design before evaluating the result. What the
corpus does supply is the funnel: `zhang2026generalization` narrows 253 complexes →
27 congeneric series → 14 series on 8 receptors, then [p.4] *"we performed full
IFD-MD refinement on all five Boltz models for each of the eight FEP+-validated
receptors, then ran FEP+ validation on the top 5 IFD-MD poses from each model."*
Cheap wide screen, expensive narrow confirm, **narrowing criterion stated**. Three
more papers stage depth the same way: `yu2026domainmotion` runs two conditions on
all 82 enzymes and the third on only 12; `feldman2026alphainterp` runs perturbation
on 200 proteins, phylogenetic tiering on the 61 with ≥10 sequences per tier, nested
identity on 183, each reduction carrying its inclusion rule; `liu2026ensembletests`
runs 82 chains headline, 36 Lockbox, an 8-protein Deep subset, all frozen in
advance [p.13–14]. That is the shape we copy.

## 3.1 The selection rule, in pre-registrable form

> **CORE-k.** Take every receptor on the delivered Class A panel that satisfies, in
> this order: (i) a deposited Active **and** a deposited Inactive reference exist in
> the GPCRdb snapshot `lit/panels/cache/gpcrdb_structures.json`; (ii) **both**
> predicate axes — d(Y5.58 OH, Y7.53 OH) and d(2×46 Cα, 6×37 Cα) — are computable
> on that receptor by the delivered scorer; (iii) for the ligand-bearing tiers
> only, a curated agonist, antagonist and decoy already exist. Group the survivors
> by the `cluster_id` paralog label shipped in `data/block_b/01_rows/rows_tidy.csv`.
> From each cluster take exactly **one** member: the one whose *worse-resolution*
> reference structure has the lowest resolution in the snapshot; ties broken by
> alphabetical receptor slug. CORE-k is the resulting set, k = number of clusters.
>
> **No quantity computed from any prediction — ours or anyone else's — may enter
> this rule.** Resolution, deposition date, reference separation and cluster label
> are all properties of deposited structures and are fixed before any model runs.
> The rule is written down, the resulting slug list is frozen, and the campaign does
> not get to revise it after seeing a result.

Applied to PANEL.md's tier C1 and to the delivered Block B/C data, this gives:

| label | rule | receptors | clusters | carries |
|---|---|---:|---:|---|
| **C1** | PANEL.md Rule P — the full census | 64 | 32 | the wide replication arm only |
| **CORE-32** | §3.1 applied to C1: one per cluster | **32** | **32** | **the partner-rung axis, every control arm** |
| **CORE-L17** | CORE-32 ∩ ligand-complete | **17** | **17** | **the ligand and MSA-depth axes** |
| H-B | PANEL.md tier H, Boltz-2 stratum | 12 | 8 | the memorization holdout |
| E-pro | PANEL.md tier E-pro | 8 | 8 | the prospective arm |
| E-B1 | PANEL.md tier E-B1 | 5 | 4 | class B transfer |

**CORE-L17** is the binding constraint and is worth stating precisely. Block C's
36 receptors are a **strict subset** of Block B's 40 (verified here: C-only = ∅,
B-only = B1B1U5, FSHR, LSHR, OPSD); 28 of them carry all three ligand roles; 25 of
those 28 also have both predicate axes, spanning **17 clusters** (`adenosine
adrenergic_beta angiotensin cannabinoid chemokine_ccr chemokine_cxcr
cholecystokinin dopamine leukotriene lysophosphatidic
melanin_concentrating_hormone muscarinic npy opioid opioid_nociceptin orexin
serotonin`).

**So a design that crosses depth × ligand × partner on existing ligand curation
tops out at 17 paralog clusters.** Below ~8, cluster-boot degenerates to
receptor-boot and cannot support an interval at all — Block D says so for n=7 and
n=4 (`data/block_d/02_caveats/C-D-1_cluster_boot_degeneracy_d1_d2.md:5-24`). 17 is
comfortably above that floor and materially below 32. Raising it is a **curation**
cost, not a compute cost: curating agonist/antagonist/decoy for the 15 CORE-32
clusters that are ligand-incomplete would take CORE-L from 17 to 32 clusters, cut
the interaction MDE from 0.295 to 0.215, and cost **zero GPU hours**. PANEL.md
already carries the per-receptor agonist/antagonist modality columns needed to
scope it. That is ask **P4** in §8 and it is the best value in the document.

## 3.2 The spine: which level of each axis is the reference

Every axis is crossed fully **against the reference level of the others**, and only
the headline axis is crossed widely. Reference levels, fixed in advance:

| axis | reference level | why this one |
|---|---|---|
| backbone | **Boltz-2** | the only backbone with a datable cutoff (2023-06-01, `methods.tex:222-246`) and an apo floor that is neither pinned at zero nor saturated — 0.123 (Block A) / 0.127 (Block B), recomputed |
| partner rung | **R0_apo** and **R7_full** | already measured on 40 receptors in two blocks; every new rung is read against them |
| ligand | **none** | what Blocks A and B ran; keeps the ladder joinable |
| MSA depth | **`msa_mode=default`** | *not* the "full" rung of a subsample-and-reinflate pipeline — see §5.2 |
| cell size | **2 seeds × 5** wide / **5 seeds × 10** core | §2.1; core matches Block B exactly so a join stays legal |

Seeds must be **paired across every arm within a receptor** (catalogue E6.4). This
is free if specified before dispatch and impossible afterwards, and Blocks A and B
both failed to do it: recomputed, Block A has **1,898 distinct `seed_outer` values
across 380 cells** and Block B **3,200 distinct `seed_used` across 640** — every
cell drew its own seeds, so no within-seed contrast can be read anywhere in either
block. Pairing converts the whole ladder into a matched-pair design at no compute
cost and tightens every adjacent-rung interval.

## 3.3 The gate: what the pilot has to show before the grid runs

Sequential design is only honest if the stopping rule is written before the pilot.
Borrowing `liu2026ensembletests`' reportability gate [p.18] — separation ≥0.30 with
a 95% bootstrap CI excluding zero, else the verdict is *not reportable* rather than
*model failure* — the gate is:

> **Stage 1 → Stage 2 gate.** Stage 2's partner-rung grid dispatches only if, on
> the Stage-1 pilot (Boltz-2, CORE-32, n=10, cluster bootstrap over 24 clusters):
> **(a)** the R3_ct21 − R0 contrast has a 95% CI excluding zero, **and** **(b)** the rung
> ordering R0 ≤ R1 ≤ R2 ≤ R3 ≤ R7 holds at cluster grain on at least 4 of the 5
> adjacent steps. If (a) fails, the peptide rungs do not separate and the 33,600-
> prediction grid buys a flat line — stop and report the pilot as a bounded null
> with its MDE stated. If (a) holds and (b) fails, the ladder is a step and not a
> dose–response; run R0/R3_ct21/R7_full only and drop R1/R3/R4, saving 40%.
>
> The depth cube (G5) and the ligand 2×2 (G6) have **no gate** — they are
> unoccupied ground (§4.1) and a null there is publishable, which is exactly the
> condition under which a gate is inappropriate.

The catalogue already recommends this for E1.1 ("Run the single-backbone pilot
before the full grid — if the rungs do not separate on Boltz-2 at n=2,000, the
40,000 buys a flat line", `redo/spec/CATALOGUE.md:1046-1047`). This
just supplies the threshold and the fallback.

## 3.4 What we must refuse to do

- **No selecting cells on the redo's own outcomes.** The CORE slug list, the gate
  thresholds, the exclusions and the bootstrap unit are frozen before Stage 2
  dispatches. `kalakoti2025afsample2` is the corpus's cautionary case: its masking
  fraction, sampling budget and selection threshold are all tuned on the evaluation
  set against deposited references, and `kalakoti2026afsample3` repeats it — *"20%
  and 40% randomization level for AF2 and AF3, respectively, yielded the best
  overall performance"* [p.4]. Tuning a *range* on the evaluation set is the same
  defect even when no per-target value is picked.
- **No assuming additivity for an interaction we cannot power.** Declare it
  unestimable instead, with the precedent: `suzuki2026conforflux` [p.21] — *"With
  n=10 targets and across-target standard error ∼0.6 Å, we cannot resolve
  non-additivity between the two factors."* See §3.5.
- **One exception, declared.** The deep-tier cell list (§5) *is* chosen using Block
  A/B/D outcomes. That is legitimate sequential design across campaigns, not
  cherry-picking within one — but only if the list is published in the
  pre-registration and the redo may not revise it. It is stated as such.

## 3.5 The ladder crosses a placement-regime boundary, and must be designed across it

**This is a defect in the centrepiece, not a caveat.** Recomputed from
`redo/inputs/seq_rungs.tsv`, the rung lengths are:

| rung | length (aa) |
|---|---|
| `R0_apo` | 0 |
| `R1_ct11` | 11 |
| `R2_ct15` | 15 |
| `R3_ct21` | 21 |
| `R4_a5helix` | 26 |
| `R5_a5plus` | **36** |
| `R6a_da5` | **324–368** (family-dependent) |
| `R7_full` | **350–394** (family-dependent) |
| `R8_hetero` | 761–805 |

Six rungs lie between 0 and 36 residues and the next lies at 324. **The
`R5_a5plus` → `R7_full` step is +314 (Gt1) to +358 (Gs) residues with nothing in
between**, and `junker2026peptidedesign` stratifies GPCR peptide/protein complexes
at **≤50 vs >50 residues** because placement accuracy changes regime there — p5:
*"100% of AF2IG-predicted, 82.1% of RF3- and 35.5% of Boltz-2-predicted GPCR-protein
ligand complexes achieve DockQ below 0.23"* — and states at p16 that cross-length
comparison of an interface score is itself unsound.

So the boundary falls **inside our empty gap**, and what we have been calling a
dose–response curve is two tight clusters separated by a void. The comparison that
carries the title — short peptide against full subunit — is exactly the comparison
that crosses the regime, and a monotone-looking result could be a placement
artefact rather than a recognition effect.

**A second problem the length table exposes, which nobody has named.** The gap is
not the same size for every family: 314 for Gt1, 318 for Gi, 323 for Gq, 345 for
G12, 358 for Gs — **a 44-residue spread**. At `R7_full` the Gs arm supplies 44 more
residues than the Gt arm, so Block B's family term (+0.082) and E1.4's family swap
are, at full-subunit length, **partly length comparisons**. At `R1`–`R3` every
family is exactly equal length. That is an independent argument for reading every
family contrast at `R3_ct21` and never at `R7_full`, and it is why G9 and G12 are
anchored at R3 in §7.1.

### The response: all three, in this order

**(1) Add three intermediate rungs — and pilot the middle first.** Target lengths
≈60, ≈100 and ≈200 residues, expressed as C-terminal truncations of the cognate
subunit so they inherit SEQUENCES.md's convention (§0.2) and its MSA-free
requirement on the partner chain. `SEQUENCES.md` owns the exact boundaries; the
design requirement from here is only that **one rung sits below 50, one just above,
and one mid-gap**, so the regime boundary is sampled rather than leapt.

| item | what | cost |
|---|---|---:|
| **P1b** | mid-rung pilot: Boltz-2 × CORE-32 × 3 rungs × n=10 | **960** |
| **G1c** | 3 intermediate rungs × 4 backbones × CORE-32 × n=10 | **3,840** |
| G1d | the same at n=50, if per-cell claims are wanted about them | 19,200 |

**960 predictions test whether the curve bends at 50 before 3,840 are committed,
and 3,840 is 2.5% of the INTENDED tier.** This is the cheapest defect-closure in
the document and it goes into every tier including MINIMAL. G1d is EXPANSIVE-only:
per §4.1 the regime question is a *pooled* question, so n=10 answers it and n=50
buys nothing for it.

**(2) Analyse within regime, always — and this is not optional even after (1).**
Declare the discontinuity in advance: **no single curve is fitted through ≤50 and
>50.** The ladder is reported as two dose–response segments plus a stated
between-regime step, with junker cited for why. If the intermediate rungs show the
curve is continuous across 50, that is a *result* (and a rebuttal of the concern
for our readout); if they show a break, the two segments were the right frame all
along. Either way the analysis plan is the same and it costs nothing.

**(3) Carry a placement covariate — and partner pLDDT is not enough.** The
recording spec already has partner-chain pLDDT and interface contacts, but
`junker2026peptidedesign` reports PAE **over-estimates** precisely where a GPCR
peptide is misplaced, so a confidence metric is the one thing that will not catch
the failure mode. A DockQ-like interface score is needed.

The awkward part, stated rather than hidden: **DockQ against the peptide's own
deposited complex is not computable at the peptide rungs, because no wild-type
21-mer α5-CT appears with a receptor in any deposited structure** (catalogue E4.3;
the only peptide-bound entry, 4X1H, carries an engineered 11-mer). The workaround
is well-defined and cheap: score every rung against the **α5-CT segment of the
deposited cognate complex** after receptor superposition — the α5-CT residues are
present in that complex at every rung length, so a fragment-restricted interface
RMSD (and a register check) is computable from R1 to R7 on one scale. It needs
coordinates, not predictions, and rides on S0.6 / catalogue E5.1, which requests
one representative cognate structure per receptor already.

**What this does not threaten.** junker's length axis is observational and it never
assesses receptor state, so the novelty of the ladder is untouched. This is a
threat to interpretation, and it is now designed against.

---

---

# 4. Power, stated in advance

`python3 redo/build/matrix_power.py kcurve cell`

## 4.1 Per-cell resolution — the floor

Wilson 95% half-width for a single cell, recomputed:

| n per cell | p=0.5 | p=0.9 | upper bound when 0 of n fire |
|---:|---:|---:|---:|
| 10 | 26.3 pts | 19.3 pts | 27.8% |
| 25 | 18.2 | 12.9 | 13.3% |
| **50** | **13.4** | **8.5** | **7.1%** |
| 100 | 9.6 | 6.0 | 3.7% |
| 500 | 4.4 | 2.6 | 0.8% |

n=50 reproduces Block D's stated resolution floor exactly
(`data/block_d/07_partA/PARTA_D2.md:6`: *"n=50 per cell yields CI half-width ≈ 8–14
points"*). **Rule: any claim about a single cell requires n ≥ 50. Any claim pooled
over clusters requires n ≥ 10 and nothing more.** At n=10 a per-cell half-width of
26 points is not a claim, and no sentence may be written from a wide-tier cell.
This is the specific failure the lit session flagged as endemic — arms that exist
but cannot support a claim: `masters2025physics` n=1, `gilson2025casp16` n=1 on the
arm that matters, `swapna2025memorization` n=3, `stein2022speachaf` n=4.

## 4.2 Pooled resolution — what k clusters buys

Empirical cluster-bootstrap 95% half-width on the Block B contrasts, as a function
of how many clusters are actually run (median over 80 random cluster subsets):

| clusters k | cognate−apo | decoy−apo | cognate−decoy | cognate−shuffled |
|---:|---:|---:|---:|---:|
| 4 | 0.157 | 0.135 | 0.183 | 0.055 |
| 8 | 0.123 | 0.124 | 0.159 | 0.056 |
| 12 | 0.102 | 0.104 | 0.128 | 0.052 |
| **17** | **0.088** | **0.089** | **0.112** | **0.042** |
| 20 | 0.078 | 0.083 | 0.104 | 0.039 |
| **24** | **0.074** | **0.076** | **0.094** | **0.035** |
| 30 *(est.)* | 0.067 | 0.067 | 0.084 | 0.032 |
| **32** *(est., CORE-32)* | **0.064** | **0.066** | **0.081** | **0.030** |

*(k>24 is a √(24/k) extrapolation from the observed panel — ESTIMATE, and it
assumes the census receptors have the same between-cluster variance as ours, which
is untested.)*

**Minimum detectable effect, 80% power, two-sided α=0.05** (2.80 × SD / √k), using
the observed cluster-grain SDs:

| contrast | cluster SD | MDE at k=32 | k=24 | k=17 | k=8 |
|---|---:|---:|---:|---:|---:|
| cognate − apo | 0.189 | **0.094** | 0.108 | 0.129 | 0.187 |
| decoy − apo (the occupancy term) | 0.194 | **0.096** | 0.111 | 0.132 | 0.192 |
| cognate − decoy (the α5 term) | 0.242 | **0.120** | 0.138 | 0.164 | 0.239 |
| cognate − shuffled (the family term) | 0.090 | **0.045** | 0.051 | 0.061 | 0.089 |

So **at CORE-32 we can detect a rung-to-rung step of ≈0.09–0.12, and a small step
of ≈0.045**; at CORE-L17, ≈0.13–0.16 and ≈0.06. Block B's three decomposition
terms are +0.400, +0.333 and +0.082, so all three remain detectable at k=17 — the
family term only just, which is why the family-sensitive arms (G9, G12) run on
CORE-32 and not on the ligand core.

## 4.3 Interactions — the number that decides how much of §4 is honest

An interaction is a difference of differences and its cluster SD is roughly double a
main effect's. Measured directly from Block B's real arm × backbone factorial (the
only genuine two-factor crossing we hold), at cluster grain over 24 clusters:

| interaction | cluster SD | bootstrap 95% hw |
|---|---:|---:|
| (cognate−apo) boltz − chai | 0.540 | 0.211 |
| (cognate−apo) boltz − of3 | 0.420 | 0.163 |
| (cognate−apo) boltz − protenix | 0.284 | 0.111 |
| (cognate−apo) chai − of3 | 0.505 | 0.198 |
| (cognate−apo) chai − protenix | 0.450 | 0.174 |
| (cognate−apo) of3 − protenix | 0.370 | 0.146 |
| **median** | **0.435** | — |

Interaction MDE at 80% power: **k=8 → 0.431, k=12 → 0.352, k=17 → 0.295, k=21
(PANEL.md tier C1r) → 0.266, k=24 → 0.249, k=32 (CORE-32) → 0.215.** Against a main effect of +0.725, a *main-effect-sized*
interaction is detectable at k=17 and a half-sized one is not.

**Stated in advance, and in the paper:** the depth × partner × ligand cube (G5) and
the ligand × partner 2×2 (G6) at CORE-L17 are powered for **main effects and for
interactions of ≥0.30**. An interaction below 0.30 will be reported as
*unestimable at this n*, with this number, and never as *absent*. This is exactly
`suzuki2026conforflux`'s position [p.21] and it is the honest one. If the PI wants
the interaction *powered* rather than *bounded*, the lever is clusters, not samples
— running G6 on CORE-32 rather than CORE-L17 would bring the interaction MDE from
0.295 to **0.215**, for an extra 15 receptors × 4 backbones × 8 cells × 50 =
**24,000** predictions *plus* the ligand curation in ask P4. That is the only
upgrade in this document that improves an interval rather than adding an arm, and
its GPU half is the smaller half.

Two free items make this cheaper than it looks. Catalogue **E7.4** injects known
interaction effects into the existing 22,400-row Block C design and reports the
fraction of cluster-bootstrap replicates whose interval excludes zero — that
calibrates the above against real data and costs nothing once `rows.tier3.v2.csv`
lands. Do it **before** G6 dispatches.

## 4.4 The seed allocation, and a correction to the brief

`python3 redo/build/matrix_power.py unanimity`

The brief supplied "**256 of 319 cells were unanimous across seeds**". Recomputed on
Block A under its own caption filter (E1+E2 then Class A, `analysis/block_a/verify_claims.py:130-147`,
CAP8 = 319 cells):

- **256 of 319 (80.3%)** are unanimous across all **25 predictions** — *sample* grain.
- **300 of 319 (94.0%)** are unanimous at **seed-majority** grain.
- **Only 19 of 319 cells (6.0%) show any seed-to-seed disagreement at all.**

So the number is right and the description is not: 256/319 is sample-grain
unanimity, not seed unanimity. A search of all four drops found no on-disk source
for the sentence; the nearest real one is `data/block_a/10_narrative/MANUSCRIPT_FLAGS.md:227`
(204/256 and 205/256, unanimity **across four backbones**, not seeds). **Do not let
"256 of 319 cells unanimous across seeds" into the manuscript in that form.**

The corrected number strengthens the brief's conclusion rather than weakening it:
**94% of cells carry no seed information whatsoever**, and Block C's variance
decomposition agrees from the continuous side (σ²_seed / σ²_within-seed = 0.11,
`data/block_c/11_manuscript_narrative/SIGNAL_RECOVERY_REPORT.md:76`). Hence the
wide-tier cell is **2 seeds × 5 samples**, and the 3 seeds freed per cell go to
arms.

---

# 5. MSA depth — the PI's named example

## 5.1 What exists and what does not

D3 ran 26 receptors × 4 backbones × 5 depths (8/32/128/512/full) × 5 seeds × 10
samples = 25,810 predictions, **apo only**
(`data/block_d/07_partA/PARTA_D3.md:5-9`, 22 paralog clusters). Never with a
partner, never with a ligand. The catalogue does not design depth × ligand or
depth × partner either; `rebuttals/BLOCK_D.md` S3 asks for depth × partner and
nothing asks for depth × ligand.

**The gap is confirmed unoccupied.** Across 81 corpus papers, exactly one crosses an
MSA manipulation with a co-input: `mitjavila2026afsample2t`, masking at 0/10/20/30%
× G-protein present/absent, 250 models per cell, 10 class A receptors, balanced
[p.8] — and it is AF2, which has **no ligand channel**, so depth × ligand is not
crossed there either. The three nearest misses each break in a different place:
`xing2025purified` purifies the MSA in AF2 and supplies the ligand in AF3 — *"the
legs are in different models"* [p.5]; `jung2026boltzperturb` varies the MSA with
**the ligand present in every arm and never removed** [p.7]; `lazou2026cryptic`
varies the ligand with **the MSA held constant by design** — *"While the choice of
ligand has no effect on the MSA"* [p.5]. They bracket the crossing from both sides
and neither performs it.

`xing2025purified`'s sentence is the reframe, and the locator matters:

> *"Our findings reveal that the successful sampling of alternative states depends
> not on MSA depth but on sequence purity."* — [p.3]

That sentence is in their **Introduction**, summarising their own prior
protein-only work, and **was never re-tested under a ligand**. So the question our
cube asks — *does a physical co-input rescue what removing the alignment took
away?* — is open on both the ligand and the partner leg.

## 5.2 The D1/D3 conflict is worse than one receptor, and it is a design constraint

The brief names rhodopsin × Boltz-2, 38.8% vs 10.0%. Sourced:
`data/block_d/02_caveats/C-D-8_opsd_boltz_cross_tier_divergence.md:10-20` — same
scorer `d9c646af`, same receptor, same predicate, 28.8 points, ~3σ, hypothesised
*"D3 sub-samples then re-inflates, and the identity-behaviour at `full` is subtly
different from Block A / D1's default."*

But `data/block_d/07_partA/PARTA_D3.md:128` says it is not one cell:

> "**28 cells; 12 outside D1's Wilson 95 % CI.**"

**Twelve of twenty-eight cells disagree.** The drift is systemic, not a rhodopsin
quirk, and it means D3's `full` rung and D1's default mode are **different
conditions with the same name**. Two tiers that should have shared a condition did
not, and nothing in the drop could have caught it because no cell was run both
ways.

Worse: the probe that would have caught it was specced and never delivered.
`data/block_c/11_manuscript_narrative/BLOCK_C_PAPER_DRAFT_v1.md:352` planned *"a
subsample-variance probe: 3 independent draws at depth=32 × 2 receptors × 4
backbones × (5, 10) = 1,200 preds, measuring which-N-1 draw-variance against
seed-variance."* D3 delivered 25,810 ≈ 26,000, not the planned 27,200. The probe is
absent from every D3 artefact.

**Three design requirements follow, and all three are cheap:**

1. **A passthrough rung that is provably identical.** The depth ladder carries
   `msa_mode=default` as a rung *in addition to* `depth=full`, and the two are run
   on the same receptors and seeds. Item **P3**, 600 predictions. If they agree,
   the ladder is anchored; if they diverge, we have measured the drift instead of
   inheriting it.
2. **Hash the delivered alignment per cell.** The contract must emit
   `msa_sha256` and `msa_n_rows` per row. `data/block_d/07_partA/HEADLINE_D3_tier_d3_full_2026_09_08.md:20-21`
   shows the cache exists (546 a3m/pqt pairs — and note the doc's own formula
   "26 × 5 × 5 = 546" is wrong; 26 × 5 × 5 = 650, the correct decomposition is
   26 × (4 depths × 5 seeds + 1 unsubsampled full) = 26 × 21 = 546). Hashing costs
   nothing and makes this class of drift impossible to ship again.
3. **Reinstate the subsample-draw variance probe.** Item **P3b**, 900 predictions:
   3 independent subsample draws at depth 32 on 6 receptors at n=50, so
   draw-variance can be separated from seed-variance. Without it, every depth
   interval in the paper conflates two noise sources.

## 5.3 The cube

Depth is the **most expensive axis per unit of claim** — it multiplies everything
and is the least load-bearing of the paper's three title clauses. So it is crossed
on **CORE-L17 only**, and on all four backbones only because the D3 result
(*"MSA depth moves the predicate on all four backbones, and on a second axis two of
those four are degradation rather than steering"*, catalogue §1.4) makes the
backbone a real moderator here rather than a replication.

| | depth | partner rung | ligand | cells/receptor |
|---|---|---|---|---:|
| **G5a** (Minimal, Intended) | 8, 128, `default` | R0, R3_ct21, R7_full | none, agonist | 18 |
| **G5b** (Expansive) | 8, 32, 128, 512, `default` | R0, R3_ct21, R7_full | none, agonist | 30 |

G5a on CORE-L17 × 4 backbones × n=10 = **12,240 predictions**. G5b = **20,400**.
Pilot (P2, Boltz-2 only, 2 depths × 3 rungs × 2 ligands) = **2,040**.

**This is the single most novel cell in the whole plan and it costs 1% of the full
factorial.** It also answers the PI's question directly: we do not run MSA
subsampling for all ligand and GPCR pairs — we run it for **17 receptors, one per
paralog cluster, chosen by a rule fixed before any result**, which is the largest
set that supports a cluster bootstrap on curated ligands, and we say so.

---

# 6. The deep-apo floor

## 6.1 It is a real result and it is cheaper than anyone thinks

The brief is right that the floor is backbone-specific by 100 points, and it is
right that the catalogue has no entry for it. Recomputed here from two independent
corpora that the Block D result never touched:

| | Block A (n=25/cell) | Block B (n=50/cell) | Block D D1 (n=500/cell) |
|---|---:|---:|---:|
| ADRB2 apo, Boltz-2 | **0.00** | **0.00** | 0.0% [0.0, 0.0] |
| ADRB2 apo, Chai-1 | **1.00** | **1.00** | 100.0% [100.0, 100.0] |
| ADRB2 apo, OF3 | 0.04 | 0.08 | 4.0% [2.4, 5.8] |
| ADRB2 apo, Protenix | 0.00 | 0.00 | 0.0% [0.0, 0.0] |

*(Block D values: `data/block_d/07_partA/HEADLINE_D1_tier_d1_full_2026_09_06.md:23`
and `PARTA_D1.md:21`. Block A/B recomputed by `matrix_power.py floor`.)*

And pooled across the panel, the floor reproduces across corpora to within 0.04:

| backbone | Block A pooled apo | Block B pooled apo |
|---|---:|---:|
| boltz | 0.123 | 0.127 |
| chai | **0.287** | **0.323** |
| of3 | 0.099 | 0.110 |
| protenix | 0.069 | 0.072 |

**So the floor is unanimous at n=25 and has been measured three times.** Chai-1
pins 7 of 36 apo cells at 1.0 and 22 at 0.0; Protenix pins 32 of 36 at 0.0. This is
not a quantity that needs 500 samples to see.

## 6.2 The decision, and it is a recommendation not to spend

**Fold R0 into the ladder's bottom rung at the ladder's own sampling depth — n=50
on CORE-32, n=10 on WIDE — and do not re-run it at 500.** Justification, from the
table in §4.1: going from n=50 to n=500 changes nothing about a point estimate and
improves the per-cell half-width from 13.4 to 4.4 points. The floor differences we
are reporting are **25 points pooled** (chai 0.323 vs protenix 0.072) and **100
points per-cell** (ADRB2). n=50 resolves both with room to spare. A 500-sample apo
pass on CORE-32 × 4 backbones would cost **48,000 predictions** — 1.5 Block B drops
— to sharpen an interval that is already six times narrower than the effect.

**The one thing n=500 does buy is the zero cell.** When 0 of 50 fire, the Wilson
upper bound is 7.1%; at 0 of 500 it is 0.8%. That difference *is* the bistability
claim — "this backbone has no second basin above 1%" is a sentence n=50 cannot
write. So:

> **G7 — deep tier.** 4 receptors × 4 backbones × R0 apo × **n=500** = **8,000
> predictions**. The four receptors are fixed in advance from Block A/B/D outcomes
> and published in the pre-registration (declared exception, §3.4): one where the
> backbones disagree maximally (ADRB2, 0 vs 100 on three corpora), one where D1
> already ran deep and D3 disagreed with it (OPSD, §5.2), and two more chosen by
> the sibling PANEL.md from the apo cells that are pinned at 0.0 on three or more
> backbones. Its only claim is the minority-basin bound. It is **not** the source
> of any rate in the paper — the rates come from the ladder's own R0.

That is 8,000 predictions to convert Block D's most reproducible result into a
bounded statement, against 48,000 to gold-plate a number already measured three
times. Recommend the 8,000 and explicitly recommend against the 48,000.

**One caution on interpretation.** D1's 7 receptors span 7 clusters and D2's 4 span
4, so cluster-boot ≡ receptor-boot in both
(`data/block_d/02_caveats/C-D-1_cluster_boot_degeneracy_d1_d2.md`). G7 at 4
receptors inherits that: **its per-cell CIs are authoritative and its panel mean is
not a claim.** Block D says exactly this about D1
(`data/block_d/07_partA/PARTA_D1.md:71`) and the redo must not quietly promote it.

---

# 7. The plan, by budget tier

`python3 redo/build/matrix_cost.py`

The compute envelope has not been given to us, so the plan is a function of budget.
The unit is a **Block-B drop (32,000 predictions)** — a quantity the pipeline has
demonstrably delivered in one go, grid-complete.

## 7.1 Items

Recomputed by `matrix_cost.py`. Rung names follow `SEQUENCES.md` §1; panels follow
§3.1.

| id | what | panel | bb | cells/rec | n | predictions |
|---|---|---|---:|---:|---:|---:|
| **P1** | ladder pilot, 7 rungs | CORE-32 | 1 | 7 | 10 | 2,240 |
| **P2** | depth × rung × ligand cube pilot | CORE-L17 | 1 | 12 | 10 | 2,040 |
| **P3** | MSA-preparation drift control (§5.2) | 6 | 1 | 2 | 50 | 600 |
| **P3b** | subsample-draw variance probe (§5.2) | 6 | 1 | 3 | 50 | 900 |
| **P4** | bulk / biological control pilot | CORE-32 | 1 | 3 | 10 | 960 |
| **P1b** | mid-rung pilot, ≈60/100/200 aa (§3.5) | CORE-32 | 1 | 3 | 10 | 960 |
| G1a | headline ladder, pooled | CORE-32 | 4 | 7 | 10 | 8,960 |
| **G1b** | headline ladder, per-cell | CORE-32 | 4 | 7 | 50 | 44,800 |
| **G1c** | 3 intermediate rungs, pooled (§3.5) | CORE-32 | 4 | 3 | 10 | 3,840 |
| G1d | 3 intermediate rungs, per-cell | CORE-32 | 4 | 3 | 50 | 19,200 |
| G2 | wide replication on all of C1, R0/R3/R7 | +32 | 4 | 3 | 10 | 3,840 |
| G3a/b | α5-null ×3 + non-Gα bulk ×3 (E1.2, E7.6) | CORE-32 | 4 | 6 | 10/50 | 7,680 / 38,400 |
| G3c | exposure-paired cluster-mates for G3 (§10.5) | +12 | 4 | 6 | 50 | 14,400 |
| G4a/b | composition controls at R3_ct21 (E1.3) | CORE-32 | 4 | 4 | 10/50 | 5,120 / 25,600 |
| **G5a/b** | depth cube (§5.3) | CORE-L17 | 4 | 18/30 | 10 | 12,240 / 20,400 |
| **G6a/b** | ligand × partner 2×4 (E2.2) | CORE-L17 | 4 | 8 | 10/50 | 5,440 / 27,200 |
| **G7** | deep-apo floor / bistability (§6) | 4 | 4 | 1 | 500 | 8,000 |
| G8 | date-stratified holdout (tier H-B, E4.1) | H-B (12) | 4 | 3 | 50 | 7,200 |
| G9 | family swap at R3_ct21 (E1.4) | CORE-32 | 4 | 1 | 50 | 6,400 |
| G10 | per-position Ala scan (E1.5) | 10 | 1 | 21 | 20 | 4,200 |
| G11 | heterotrimer rung R8_hetero (E1.7) | CORE-32 | 4 | 1 | 50 | 6,400 |
| G12 | Gi/Gt single-residue pair (E1.6) | CORE-32 | 4 | 1 | 50 | 6,400 |
| G13 | post-cutoff inactive nanobody (E4.4) | 1 | 4 | 3 | 50 | 600 |
| G14 | prospective, tier E-pro (E7.3) | E-pro (8) | 4 | 3 | 50 | 4,800 |
| ~~G15~~ | ~~class B1 transfer, tier E-B1 (E7.2)~~ | ~~E-B1 (5)~~ | 4 | 4 | 50 | ~~4,000~~ |
| **G16a** | uncoupling nulls, full-length (**E1.8**) | 6 | 4 | 2 | 50 | **2,400** |
| **G16b** | uncoupling nulls, peptide rungs (**E1.8**+E1.1) | 6 | 4 | 4 | 50 | **4,800** |
| **G17a** | partner MSA on/off, pooled (**E1.9**) | 30 | 4 | 3 | 10 | **3,600** |
| **G17b** | partner MSA on/off, per-cell (**E1.9**) | 30 | 4 | 3 | 50 | **18,000** |
| **G18a** | wet-lab length series, per-cell | 30 | 4 | 3 | 50 | **18,000** |
| **G18b** | wet-lab matched peptides (boltz2 only) | 6 | 1 | 3 | 10 | **180** |
| **G19** | reference-matched tip, 23 cells | 23 | 4 | 1 | 10 | **920** |
| **G20** | chimeric-reference extension tier | 10 | 4 | 3 | 10 | **1,200** |
| **G1c-opt** | intermediate rung, optional 4th | 30 | 4 | 1 | 10 | **1,200** |
| **G1e** | helical-domain deletion companion | 30 | 4 | 1 | 10 | **1,200** |
| **G1f** | deposited mini-G anchor (boltz2 only) | 30 | 1 | 3 | 10 | **900** |
| **G10b** | Gi→Gs stepwise substitution series | 10 | 1 | 15 | 20 | **3,000** |

> **Added 2026-09-12.** `g1_preflight.py` carried a standing WAIT that §7.1 had no
> line item for **E1.8** (uncoupling mutants) or **E1.9** (partner MSA on/off).
> It named two arms; **twelve were missing.** G18a/b, G19 and G20 were absent, and
> when the WAIT was replaced by a check (**B18**) that actually compares the two
> files, it immediately found four more nobody had listed anywhere: **G1c-opt,
> G1e, G1f and G10b**. That is the difference between a dependency someone wrote
> down and a check that looks. Every row is **derived** from
> `inputs/g1_systems.csv` — receptors × constructs × backbones × n — and
> `matrix_cost.py::check_against_systems()` asserts each reproduces that file's own
> prediction totals: **12 of 12 agree**. A cost table that disagrees with the system
> table is worse than no cost table, because both look authoritative and only one
> gets read.
>
> Counts are explicit integers, not panel names: these arms run on the frozen
> **30-receptor** primary panel, not on the 32 that `CORE-32` names.
>
> **`G15` is struck** — class B1 transfer left with the scope decision
> (`DECISIONS.md` D-2026-09-12-d). It is still in `matrix_cost.py`'s `EXPANSIVE`
> tier, and that tier's total therefore still includes its 4,000; the strike is
> recorded here rather than silently removed so the total stays auditable.


G2 is the only item that runs on receptors *outside* CORE-32: it adds the other 32
members of C1 at three rungs and wide-tier depth, so the paper can say the headline
result holds on the full 64-receptor census and not only on the cluster
representatives. It is cheap (3,840) precisely because it is a replication, not a
new arm.

## 7.2 Tiers

| tier | items | predictions | Block-B drops | % of core factorial | × campaign to date |
|---|---|---:|---:|---:|---:|
| **MINIMAL** | Stage 0 + P1 P1b P2 P3 P3b P4 + G1a G1c G3a G5a G6a | **45,860** | 1.4 | 4.1% | 0.37× |
| **INTENDED** | + G1b for G1a, G3b for G3a, G4a G6b G7 G8 G13 | **155,100** | 4.8 | 13.8% | **1.25×** |
| **EXPANSIVE** | + G1d G2 G3c G4b G5b G9 G10 G11 G12 G14 G15 | **249,540** | 7.8 | 22.3% | 2.00× |

Wall-clock on the 25-H100 pool that actually ran D3, under the three cost scenarios
of §1.4 (**ESTIMATE** — the 2-chain rate is the unknown):

| tier | 2.0× | 4.2× | 13.2× |
|---|---:|---:|---:|
| MINIMAL | 1.0 d | 2.0 d | 6.4 d |
| INTENDED | 3.3 d | 6.8 d | **21.5 d** |
| EXPANSIVE | 5.2 d | 10.9 d | **34.7 d** |

**Even EXPANSIVE is 22% of the core full factorial and 4.4% of the full crossing
with controls.** The design buys nearly every answerable question for a fifth of
the naive grid, and §2 says exactly where the other four fifths were going to be
spent: on repeats within cells that are already unanimous, and on receptors that
are cluster-mates of receptors already in the run.

### What each tier buys and gives up

**MINIMAL — 45,860.** Buys: title clause 1 as a pooled result on 4 backbones and 32
clusters; the α5-null and bulk controls; the depth × partner × ligand cube (the
novel cell); the clean ligand × partner crossing; and both MSA-drift controls.
It also carries both halves of the §3.5 fix — the mid-rung pilot and the three
intermediate rungs — because without them the headline comparison crosses a
placement-regime boundary unsampled. Gives up: **every per-cell claim** — at n=10
no sentence about a single receptor × backbone cell may be written; the composition
controls; the residue map; the holdout; the bistability bound; the wide
replication; the within-cluster exposure pairing. Report reads: "the ladder
rises, here is the decomposition with intervals, here is the first depth × co-input
crossing." Defensible, thin.

**INTENDED — 155,100 ≈ 1.25 A–D campaigns, spent once.** Adds n=50 on the headline
ladder, the controls and the ligand 2×2 (so per-cell claims and per-receptor
figures become legal), the deep-apo bistability bound, the date-stratified holdout,
and the one post-cutoff inactive-nanobody arm. Gives up: the residue-level map, the
heterotrimer, the family swap, the prospective and class-B arms, the wide
replication on the other 32 census receptors. **This is the recommendation.** It
closes title clause 1 outright, closes the half of clause 2 that new inference can
close, carries the memorization control a referee will demand, and every headline
number survives at cluster grain with an interval we can size today.

**EXPANSIVE — 249,540.** Adds the composition controls at full depth, two more
depths, the family swap, the per-position scan, the heterotrimer, the Gi/Gt pair,
the prospective arm, the class B1 transfer arm, and the wide replication across all
64 census receptors. If a fourth tier is ever affordable, the best-value upgrade is
**G6 on CORE-32 rather than CORE-L17** (+24,000 predictions and the P4 curation),
which takes the interaction MDE from 0.295 to 0.215 — the only upgrade that
narrows an interval rather than adding an arm.
## 7.3 Stage 0 — costs nothing, gates everything

None of the above dispatches until these land. All are `free`, `free (them)`,
`free*` or `cheap`; none is new inference.

| | item | class | why it gates |
|---|---|---|---|
| S0.1 | ship `rows.tier3.v2.csv` + Block D's three `rows.csv` (E6.2/E6.3) | free (them) | 42,180 predictions are currently unverifiable and 30 of Block C's 53 checks are consistency-only. Designing a fifth campaign against unverified numbers is what Block A's 21 discrepancy groups (17 found in-house) argue against. |
| S0.2 | off-panel recalibration of the predicate (E0.1) | free* | **every rate in the redo is graded by this ruler.** 726 off-panel Class A structures, 611 active vs 115 inactive — the balancing rule must be fixed before fitting. |
| S0.3 | export state calls on Block C's 40,800 (E2.1, E2.4) | free (them) | may make half of G6 redundant, and answers the decoy-ligand challenge (`yu2026domainmotion`) from data already run. |
| S0.4 | power injection on the existing 2×2 (E7.4) | free | calibrates §4.3 against real data before G6 spends 27,200. |
| S0.5 | delivery contract (E6.1) **+ seed pairing (E6.4) + MSA hashing (§5.2)** | free | impossible to add after dispatch. |
| S0.6 | steric exclusion at panel scale (E5.1) | cheap | the paper's only mechanism, currently n=2; needs coordinates, not predictions. |
| S0.7 | free re-analyses on A and B: E0.4, E3.1, E3.2, E3.3, E4.2, E5.3, E5.4 | free | three of the catalogue's top five cost no new inference; they should be finished before any GPU spins. |

## 7.4 Dependency order

```
  S0.1 ─┬─> S0.3 ─> S0.4 ──────────────────┐
        └─> S0.7                            │
  S0.2 ──────────────────────────> (thresholds) ──┐
  S0.5 ──────────────────────────> (contract) ────┤
                                                  v
              P3, P3b ─> (MSA anchored) ─> P1, P1b, P2, P4 ─> [GATE §3.3] ─> G1 G3 G5 G6
                                        G1c <── needs P1b's mid-rung lengths ───┤
                                                                          │
                                        G2, G4, G8, G13 ── independent ───┤
                                        G7 ── independent, needs P3 only ─┤
                        G9, G12 <── need G1's R3_ct21 ───────────────────┤
                        G10 <── needs a length chosen from G1 ────────────┤
                        G11 <── needs a 3-chain input schema (harness) ───┤
                        G14 <── needs S0.2 only ──────────────────────────┤
                        G15 <── needs E0.5, the class B predicate ────────┘
```

Hard orderings, and the reason for each:
- **S0.2 before any rate is reported**, not before dispatch. Axes are continuous and
  storable, so a campaign can run while the threshold is being fitted — provided the
  contract ships both axes per row, which §7.3 S0.5 requires.
- **P3/P3b before any depth cell.** Running G5 on an unanchored `full` rung would
  reproduce the D1/D3 defect at four times the scale.
- **G1 before G9, G10, G12.** Each needs a rung length chosen from the ladder.
- **G11 last among the real items.** It is a harness change (three-chain input), not
  a dispatch; Block A's FASTA schema is single-partner.
- **S0.7's E4.2 before G3.** The exposure covariate has to exist, and the median
  split has to be declared, before the bulk control dispatches — §10.5(a). E4.2 is
  free and already in Stage 0; this makes it a hard predecessor rather than a
  parallel item.
- **G10 at `R3_ct21` only, with the partner-MSA audit as a gate** — §10.5(b). Run
  at a subunit rung it produces a null that is a property of retrieval.
- **G15 needs a class B instrument first.** Class B1 has no NPxxY and no validated
  predicate; the current substitute is an uncalibrated TM6 kink angle
  (`methods.tex:53-63`). Catalogue E0.5 must resolve to option (b) — calibrate on
  the 148 B1 snapshot entries — before G15 means anything. If it resolves to (a),
  drop and say the work is Class A.
- **The panel decision is a multiplier, not an experiment.** Whether the run is on
  CORE-32 or on all 64 of C1 scales every cost linearly and every half-width as
  1/√k. Decide it once, early, from §10.1 — but apply the *full* census only to the
  arms whose conclusions are power-limited (that is G2's job, at 3,840), never
  uniformly.

---

# 8. What I would ask the pipeline team, to learn the real cost

Ranked by how much of this document changes on the answer.

1. **P1 — the two-chain rate.** Wall-clock and worker count for a single
   receptor+Gα prediction on each of the four backbones, at the production settings
   (recycles, diffusion steps, sample batching). The measured apo rate is 22.7
   s/pred/H100 and the only two-chain figure on disk is a 5 min/pred planning
   estimate. That is a 13.2× apo-to-planning ratio; the **two-chain spread is 6.6×**, and
   chain-B length enters the model nowhere (§1.4). Nothing on disk anywhere in four blocks records
   recycles, diffusion steps or model sizes. *If the answer is near 2×, EXPANSIVE is
   a week and the tiering question dissolves; if it is near 13.2×, INTENDED is **21.5 days**
   and G15 becomes the first thing cut.* (This read "17 days"; the table at §7 and
   `matrix_cost.py` both say 21.5.)
2. **P2 — per-backbone relative cost.** Is one backbone 5–10× another? The catalogue
   flags this as open (§6 item 8) and it changes the ranking: an arm that is
   4-backbone-crossed costs 4× the reference backbone only if they are comparable.
   *If one backbone dominates the bill, the wide-tier arms drop to 3 backbones and
   the expensive one runs on CORE only.*
3. **P3 — MSA build cost and cache reuse.** D3's cache is 546 a3m/pqt pairs for 26
   receptors × 21 depth-seed combinations. Is an MSA built once per (receptor,
   depth, subsample seed) and reused across arms and backbones, or rebuilt?
   *If rebuilt per arm, the depth cube's cost is dominated by alignment building,
   not inference, and G5 should be restructured to hold the alignment fixed across
   the rung and ligand axes within a cell.*
4. **P4 — ligand curation cost.** What does it take to add agonist/antagonist/decoy
   for 7 more paralog clusters? This is the cheapest available power upgrade in the
   whole plan: it takes CORE-L from 17 to 24 clusters, cutting the interaction MDE
   from 0.295 to 0.249 and every pooled half-width by ~15%, **for zero GPU hours**.
5. **P5 — can a three-chain input be supplied at all?** G11 (heterotrimer) is the
   only item that needs a harness change. *If no, drop it and say why in the
   Discussion; the reference-set mismatch it addresses is then carried as a caveat.*
6. **P6 — is the D3 depth pipeline's `full` rung bit-identical to default mode?**
   The 12-of-28-cells divergence (§5.2) says probably not. *If they can answer from
   code, P3 (600 predictions) becomes unnecessary; if not, it runs.*

---

# 9. What I recommend NOT running, and why

- **The 500-sample apo pass on the full panel.** 48,000 predictions to narrow an
  interval already six times narrower than the effect it measures (§6.2). Run 8,000
  on four receptors for the minority-basin bound instead.
- **50 predictions per cell on any pooled-claim arm.** It is a 5× multiplier that
  buys ≤0.002 of half-width (§2.1). Reserve n=50 for arms whose *claims are per-cell*.
- **Depth crossed against the full receptor panel.** The PI's instinct is right and
  the measurement backs it: depth is the most expensive axis per unit of claim.
  CORE-L17 × 4 backbones is 12,240 predictions; the same cube on CORE-32 would be
  23,040 for an interval improvement of 0.112 → 0.081 on a contrast that is not a
  title clause. Spend that budget on G6 instead, where the same 15 extra clusters
  buy a *powered interaction* rather than a tighter main effect.
- **The intermediate rungs at n=50 (G1d, 19,200), before the pilot.** The regime
  question is pooled, so n=10 answers it (§4.1) and P1b's 960 predictions decide
  whether the three rungs are worth 3,840 at all. Committing 19,200 up front spends
  5× the budget on per-cell resolution nobody will quote.
- **A fifth backbone.** Agreeing with the catalogue §5.3: architecture independence
  at four is already the strongest structural argument in the paper, and a fifth
  multiplies every cost in this document by 1.25.
- **Running every arm on all 64 of C1.** It is a 2× uplift on everything to fix
  power problems that three arms have, and §2.2 shows the second receptor in a
  cluster buys ≤0.010 of half-width. Run CORE-32 for the arms and G2 (3,840) for
  the census replication.
- **Re-running Blocks A and B wholesale.** Their axes are continuous and stored, so
  re-scoring under a new threshold is free (`E0.4`) and should happen regardless of
  budget. What is *not* free is that the 24 census receptors absent from Block B
  have no apo or cognate arm at all — but the redo's own G1/G2 supply exactly those
  rungs, so nothing needs re-running as a separate item.

---

# 10. Reconciliation with PANEL.md and SEQUENCES.md

Both siblings landed while this was being written. Everything above is costed
against their decisions. Five places where my design and theirs differ, or where a
corpus finding changed one of them, and how each is resolved.

### 10.1 The reduced core: I do not use C1r, and here is why

PANEL.md §5 offers **C1r — 29 receptors, 21 clusters**, filtered by "both rule-R
references ≤ 3.00 Å", and says explicitly that the subsetting decision "is a budget
call and belongs to `RUN_MATRIX.md`". Taking that up: **CORE-32 dominates C1r on
the only axis that sets an interval.** C1r spends 29 receptors to buy 21 clusters;
one-per-cluster spends 32 to buy 32. Three more receptors, eleven more clusters,
every pooled half-width ~20% narrower (§4.2), and — PANEL.md's own objection to
C1r — it does not drop 26 of ConfoRNets' 45 comparison cases.

The resolution filter is still worth keeping, as a **covariate rather than a
filter**: record the worse-reference resolution per receptor and report the
headline with and without a 3.00 Å restriction, which is free and answers the same
concern without spending clusters on it. If the PI prefers C1r anyway, every cost
in §7 scales by 29/32 = 0.91 and every half-width by √(32/21) = 1.23.

### 10.2 The ladder is 11 rungs, of which 7 are the ladder

SEQUENCES.md §1 renumbers the catalogue's E1.1 and inserts `R2_ct15` for
`tran2026nanogs`'s stapled 15-mer, then splits the single `a5null` into three
(`R6a_da5` removes α5, `R6b_a5perm` permutes it in place, `R6c_a5polyA` replaces it
with poly-Ala). **This matrix treats the 7 length rungs as the ladder (G1) and the
3 α5-null variants as control arms (G3).** That is why G3 is 6 arms here rather
than the 4 I first costed: 3 α5-null variants plus 3 non-Gα bulk controls.

**Note the title's length is now `R3_ct21`, not R2.** Everywhere this document
says "the 21-mer" it means `R3_ct21`; §3.3's gate and G4/G9's arms are anchored
there.

SEQUENCES.md flags that `R6a`–`R6c` may not fold as Gα at all, since α5 packs
against the Ras domain, and requires a Gα-chain pLDDT and a Ras-domain integrity
readout on those arms. **That is a gate, not a caveat, and this matrix adopts it:**
if the α5-null arms arrive as molten globules they are not mass-matched to
anything, the bulk control has not been run, and G3b's 38,400 predictions are
wasted. So G3 runs its pilot leg (P4, 960 predictions) *first* and the integrity
readout is checked before the full arm dispatches.

### 10.3 Where I still need a number

| from | what | what changes here |
|---|---|---|
| `PANEL.md` | the CORE-32 slug list under §3.1's rule — one representative per cluster of C1, chosen by worse-reference resolution then alphabetical | none of the arithmetic; all of the dispatch. This is the one artefact §7 cannot run without. |
| `PANEL.md` | which CORE-32 receptors have a curated agonist **and** antagonist **and** decoy, beyond Block C's delivered 25 | CORE-L17 is a floor derived from Block C's roles. PANEL.md's modality columns show several census receptors with `**none**` for antagonist (GPR52, MTR1A, MTR1B), so the true ligand-complete cluster count may be above or below 17. Every G5/G6 cost scales linearly with it; the interaction MDE scales as 1/√k. |
| `PANEL.md` | whether the four NPxxY-blind receptors (EDNRA, EDNRB, GRPR, HRH3) are an anchor-mapping bug that re-scoring fixes | recovers 3 clusters on the Block B side and, if the same mapping affects census members, more on C1. Free if it is a mapping fix. |
| `PANEL.md` | confirmation that tier H's Boltz-2 stratum is 12 receptors / 8 clusters | G8 is costed at 12 × 4 × 3 × 50 = 7,200. At 8 clusters its interval half-width is ≈0.12 on the ladder contrast (§4.2) — which is enough for a stratum *comparison* and not for a per-stratum rate. Say so in the caption. |
| `SEQUENCES.md` | which 3 of the non-Gα bulk candidates are dispatched (`gcn4_leucine_zipper_33`, `ubiquitin`, `KaiB_2QKEE`, `random_helix_40mer`, `arrestin_FL`, `arrestin_Ctail`), keyed by **sequence SHA not header** | G3 is priced at 6 arms. Each arm dropped saves 6,400 (n=50) or 1,280 (n=10). Two `partners.fasta` headers are known-wrong: `GASR` is a gastrin receptor and `Nb60` carries the Nb80 CDR3. |
| `SEQUENCES.md` | pre-dispatch SHA verification of chain B on every arm | the D2 defect — both ADRB2 nanobody subarms fed sha256 `1406ad7ea26451…`, one arm contrasted with itself — must be impossible by construction. If SHA verification is not pre-dispatch, G13 is not worth running. |

### 10.4 One thing I would ask the panel session to reconsider

PANEL.md's tier **E-pro** is 8 receptors (`acm5 ada1b ada2c ccr7 ccr9 gnrhr lgr4
ox1r`); the catalogue's §7.3 counted 9, including `q9wtk1`. The difference is
almost certainly a species/paralog collapse and PANEL.md is likely right — but the
prospective arm is the one whose whole value is that its membership rule is
airtight, so the discrepancy should be resolved explicitly rather than silently.
G14 is costed at 8; at 9 it is 5,400.
### 10.5 Two corpus findings that change a dependency and a protocol

**(a) E1.2 now depends on E4.2. The bulk control must be exposure-stratified.**
`yu2026domainmotion`'s decisive covariate is not the ligand: the ligand moves the
holo-like fraction 11.9%/9.1% while **training composition moves it 40.3%**, and
their own note says that crossing *is* the result. A bulk control that is not
stratified by each receptor's deposited exposure is uninterpretable on their design.

Recomputed here from `lit/panels/cache/gpcrdb_structures.json` over the 40-receptor
Block B panel, using **deposited active fraction** = Active / (Active + Inactive)
as the exposure variable — because the catalogue records that Block B's own
`deposition_count` covariate is constant and its regression ships NaN, so the
variable has to be rebuilt from the snapshot:

- Range **0.15 (AA2AR, 80 structures) to 0.86 (HRH3)**, median 0.667, SD 0.205.
  All 40 receptors match the snapshot; nothing is missing.
- **Exposure variance is 2.2× larger *within* paralog clusters than between them**
  (within-cluster MS 0.0649 vs between-cluster MS 0.0293). Within-cluster range is
  0.28 median and **0.65 maximum** — muscarinic spans ACM1 0.17 / ACM2 0.57 /
  ACM4 0.82; serotonin spans 5HT1B 0.20 / 5HT5A 0.80; histamine 0.29 / 0.86.

Two consequences, and the second is a defect in my own §3.1 rule:

1. **The free fix is adequate and goes in INTENDED.** Exposure is near-orthogonal
   to cluster, so a **median split declared in advance** does not collide with the
   cluster bootstrap: 32 clusters split ~16/16, giving MDE 0.136 for the occupancy
   term against yu's 40.3-point training effect. Two strata, not three (at three,
   k≈11 and MDE 0.164 — still detectable, but 16 is the safe call). Costs nothing;
   requires only that `active_frac` is recorded per row and the split is fixed
   before dispatch.
2. **My one-per-cluster rule picks each cluster's exposure almost arbitrarily,
   and with a tilt.** Because 69% of exposure variance is within-cluster, the choice
   of representative swings that cluster's exposure by up to 0.65. Selecting by best
   resolution — §3.1's rule — gives a panel with mean active fraction **0.564**
   against the full panel's **0.602** (median 0.569 vs 0.667), because
   better-resolved structures accrue to heavily-deposited, inactive-rich receptors
   (AA2AR wins adenosine at af=0.15 with 80 entries; ACM1 wins muscarinic at 0.17).
   The bias is modest but it is in the direction that matters, and it is invisible
   unless measured.

   **Resolution, in two parts.** (i) Keep the resolution rule — it preserves the
   full exposure spread (0.15–0.86), which is what E4.2 needs, whereas a
   "closest-to-median" rule would compress it (mean rises to 0.653) and destroy the
   very variance E4.2 regresses on. (ii) Record `active_frac`, `n_deposited_active`
   and `n_deposited_inactive` per row, report CORE-32's exposure distribution
   against C1's, and treat exposure as a modelled covariate rather than something
   balanced away. The 4–10 point shift is then reportable rather than hidden.

   **The better design, if the budget reaches EXPANSIVE — G3c, +14,400.** For each
   multi-member cluster, add the cluster-mate whose exposure is most distant from
   the representative's. On the Block B panel that is **+12 receptors**, turning the
   bulk control's exposure contrast into a **within-cluster matched pair** — which
   is where 69% of the exposure variance lives, and a far stronger test than a
   between-cluster median split. It is priced as G3c and it is the single best
   EXPANSIVE-only item after the interaction upgrade.

**(b) E1.5 must run at peptide length, or its null is a retrieval artefact.**
Both papers that motivate the per-position scan are receptor-side *self*-mutation,
and `masters2025physics` states the mechanism of its own null at p.9: a mutated
sequence *"will return exactly the same results as before"* from alignment and
template search. So mutating inside a supplied partner **whose alignment is
unchanged** would reproduce that null for the same reason — a property of
retrieval, not of the model.

`SEQUENCES.md` already requires the peptide rungs, and `R7_full`, to run **MSA-free
on the partner chain**, so the protocol is available. Three requirements are added
to G10:

- **G10 runs at `R3_ct21`, not at a subunit rung.** At 21 residues the partner's
  alignment is empty by construction, so the 21 alanine substitutions are the whole
  perturbation. Conveniently the scan is then exactly 21 positions on a 21-residue
  chain, which is why G10's cost is unchanged at 4,200.
- **Audit the partner MSA per arm and ship the audit**, as
  `data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md` did for the decoy tail. A scan
  whose arms differ in sequence but not in alignment depth has not tested what it
  claims to test. `waymentsteele2024cluster` ran its mutation scan with no MSA for
  exactly this reason and is the protocol to copy.
- **A null from G10 is only reportable if the audit shows the perturbation reached
  the model.** Otherwise the verdict is *not reportable*, per §4.1's rule, and the
  4,200 predictions are a methods note rather than a result.

This also retro-fits the Block B decoy confound: the catalogue records that on
Chai-1 the tail edit *"does not reach the model as aligned upper-case columns at
all"*. The same defect, one length down, is what E1.3 and E1.5 exist to escape.

# 11. Anomalies found while building this, reported plainly

Each was chased down before being called a finding, per the project's own rule.

1. **"256 of 319 unanimous across seeds" is sample-grain, not seed-grain.** 256/319
   is correct at sample grain, 300/319 at seed grain, and no on-disk source for the
   sentence exists in any of the four drops. §4.4. The corrected reading strengthens
   the conclusion.
2. **My first Block B recompute was wrong before the drop was.** Pooling all 32,000
   rows gives apo/decoy/shuffled/cognate = 0.142/0.502/0.728/0.802, which disagrees
   with the catalogue's 0.158/0.558/0.809/0.891. Restricting to rows where **both**
   axes were measured (28,800 = frame_36) reproduces the catalogue to four decimal
   places. Same data, different denominator — `data/block_b/README.md:84-90` states
   the frame and I had not applied it. Every number in this document uses frame_36.
3. **The D1/D3 divergence is 12 of 28 cells, not one.**
   `data/block_d/07_partA/PARTA_D3.md:128`. The brief and `C-D-8` both present it as
   a rhodopsin problem. It is a pipeline problem. §5.2.
4. **The D3 MSA-cache formula in the headline is wrong.** "26 × 5 × 5 = 546"
   (`HEADLINE_D3_tier_d3_full_2026_09_08.md:20-21`); 26 × 5 × 5 = 650. The count 546
   is right under 26 × (4×5 + 1). Cosmetic, but it is the file we would size a depth
   campaign from.
5. **Block A is missing 4 cells nobody disclosed.** FZD4 × cognate × all four
   backbones, 100 predictions, absent from `data/block_a/README.md` and the claim
   sheet. Two further cells are short (B1B1U5 apo boltz = 20, CRHR1 cognate boltz =
   20). Recomputed, not claimed.
6. **Block C's landed-panel arithmetic does not close.** 36 receptors × 4 × 2 × 3 ×
   50 = 43,200 against 40,800 landed — **48 cells unaccounted for** — and
   `BLOCK_C_CLAIM_SHEET.md:326` contains the literal sentence "36 × 4 = 40,800".
   It also cannot be simultaneously true that the landed corpus has 36 slugs and
   that 800 rows fail on an OPSD/B1B1U5 pattern.
7. **Block C's 36 receptors are a strict subset of Block B's 40** (C-only = ∅;
   B-only = B1B1U5, FSHR, LSHR, OPSD). This is load-bearing and good news: one panel
   carries both the partner and the ligand axis, and the ligand curation already
   exists for it.
8. **The ladder's gap is family-dependent by 44 residues.** Recomputed from
   `redo/inputs/seq_rungs.tsv`: `R5_a5plus` → `R7_full` is +314 for Gt1 and +358
   for Gs. So at full-subunit length the Gs arm supplies 44 more residues than the
   Gt arm, and Block B's family term (+0.082) is partly a length contrast. At
   `R1`–`R3` every family is exactly equal length. Not previously recorded anywhere;
   §3.5.
9. **Block B's `deposition_count` covariate is unusable and the exposure variable
   had to be rebuilt.** The catalogue flags it as constant with a NaN regression;
   confirmed, and §10.5 rebuilds active/inactive counts from
   `lit/panels/cache/gpcrdb_structures.json` instead, matching all 40 panel
   receptors.
10. **Seeds are unpaired everywhere.** 1,898 distinct `seed_outer` across Block A's
   380 cells; 3,200 distinct `seed_used` across Block B's 640. No within-seed
   contrast is readable in either block. §3.2.

---

## Questions for lit

1. **`cheng2026af3cluster` — does it co-fold the binder while varying the MSA?** The
   corpus note is abstract-only and says this is the one question that decides how
   much of the depth-cube novelty survives. *If it crosses MSA clustering with a
   co-folded ligand or partner inside AF3, G5 stops being the first such crossing
   and becomes a replication on a new substrate — still worth running, but it moves
   from the headline to the supplement, and the Minimal tier should spend G5a's
   12,240 predictions on promoting G6 from its n=10 form (5,440) toward its n=50
   form (27,200) instead. If it holds the binder fixed, G5 stays the novel cell.*
2. **Is there any published per-prediction cost for a two-chain co-folding run on
   Boltz-2 / Chai-1 / Protenix / OpenFold3?** `tang2026steeraf` [p.6] gives per-target
   GPU-hours for monomers and `passaro2025boltz2` [p.42] gives 20 GPU-sec per ligand
   inference. *Any published receptor+partner figure would narrow the 13× bracket in
   §1.4 independently of the pipeline team, and would let me pick one tier rather
   than three.*
3. **Does any corpus paper report a sample-count ablation on a BINARY state call
   rather than on RMSD or TM-score?** The saturation evidence I have —
   `kalakoti2026afsample3`'s median ~300 models [p.5], `lazou2026cryptic`'s
   convergence by ~80 of 100 seeds [p.5] — is all on continuous or best-of-N metrics,
   where more samples monotonically help. Our predicate is a *fraction*, where 67% of
   cells are pinned. *If a paper reports the binary version and finds saturation
   later than n=10, I raise the wide-tier cell from 10 to 20 and the Minimal tier
   costs 68k instead of 34k. If none exists, our §2.1 measurement is the evidence and
   should be reported as a methods result in its own right.*
4. **Has any paper reported a per-model "apo floor" — the fraction of unliganded,
   unpartnered predictions that land in the active basin — and does anyone else see a
   100-point spread between architectures?** *If this is unreported, §6 is a
   standalone result worth a figure and G7's 8,000 predictions are underspending; I
   would extend the deep tier to 8 receptors (16,000). If it is known, G7 shrinks to a
   confirmation and the citation goes in the caption.*
5. **`paajanen2026activation`'s 10,000-resample GMM threshold ±0.44 [pp.10–11] — is
   the resampling unit structures or receptors?** Ours must be paralog clusters.
   *If theirs is structures, the off-panel recalibration (S0.2) cannot quote their
   interval as a precedent for ours and needs its own cluster-level statement, which
   changes what E0.1 has to deliver.*
6. **Does `mitjavila2026afsample2t` report the masking × partner interaction term
   itself, or only the two main effects?** [p.8] says the design is balanced at 250
   models per cell on 10 receptors. *If they report an interaction with an interval, I
   can quote a prior effect size and size G5 against it rather than against Block B's
   backbone × arm proxy (§4.3). If they only report main effects, the interaction is
   unoccupied even in the one paper that could have estimated it — which is a stronger
   novelty sentence than the one currently in §5.1.*
7. **Does `junker2026peptidedesign` report where in 3–137 aa the regime actually
   breaks, or only that ≤50 vs >50 separates?** §3.5 places three intermediate rungs
   at ≈60/100/200 on the assumption that 50 is the boundary and that one rung either
   side brackets it. *If they report a continuous placement-accuracy curve against
   length, I would site the three rungs on their curve's steepest region instead of
   around a threshold, and P1b's 960 predictions would test that specific shape. If
   the 50 cut is an arbitrary median of their own set rather than an observed
   break, the whole concern weakens and G1c could drop to two rungs.*
8. **Does any corpus paper compute an interface score for a peptide against the
   corresponding segment of a larger deposited complex** — i.e. fragment-restricted
   DockQ or interface RMSD, rather than against the peptide's own reference? That is
   the workaround §3.5(3) proposes for the fact that no wild-type 21-mer α5-CT is
   deposited with any receptor. *If it is standard, it goes in Methods with a
   citation. If nobody does it, I need to know whether it is unconventional because
   it is wrong — in which case the placement covariate at peptide rungs falls back
   to insertion depth plus a register check, and the regime effect can be described
   but not regressed out.*
9. **Is there a citable precedent for stratifying a receptor panel by paralog cluster
   and taking one representative per cluster?** The selection rule in §3.1 is the
   backbone of this whole design and I have no precedent for it. *If one exists, it
   goes in Methods as "following [x]". If not, §3.1 needs a paragraph justifying the
   rule from the bootstrap unit — which is doable but costs a referee's patience, and
   I would also want to know whether anyone has been criticised for the opposite
   (reporting n as receptors when the resampling unit is families).*
