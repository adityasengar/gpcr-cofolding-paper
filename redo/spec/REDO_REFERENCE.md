# REDO_REFERENCE.md — the single reference for the redo campaign

**Written 2026-09-14.** Every count in this document was measured from the files it
names, on the date above. Where this document and `inputs/` ever disagree,
**`inputs/` wins** — it is the thing that dispatches, this is the thing that explains.

**Nothing in this campaign has run. Zero predictions. No GPU time has been spent.**

---

# 1. What the paper is trying to show

Three claims. They are independent, and they are in different states.

| # | claim | status |
|---|---|---|
| **1** | A 21-residue piece of the Gα α5 C-terminus, supplied as a **second input chain**, drives four co-folding models into the **active** GPCR state | **No peptide arm has ever run.** Every partner arm in the frozen campaign is a complete Gα subunit or a nanobody, and the segment varied is **11 residues**, not 21 |
| **2** | The **agonist alone** does not do this | **Retracted.** Every row of the file used to answer it carries a ligand; "apo" there meant *no partner*, not *no ligand*. So "agonist alone" was never predicted (`DECISIONS.md` F-23) |
| **3** | Model **confidence** does not track state correctness | The only clause with data behind it |

The redo exists to put data behind claims 1 and 2 without breaking claim 3.

---

# 2. Vocabulary — read this before any table below

**Backbones.** Four structure-prediction models: **Boltz-2**, **OpenFold3**,
**Protenix**, **Chai-1**. In `inputs/`, `backbones` is either
`boltz2|openfold3|protenix|chai1` (1,271 of 2,039 Group 1 rows) or `boltz2` alone
(768 rows — the pilots and the single-backbone scans).

**Chain A** is always the GPCR. **Chain B**, when present, is the partner. **Chain C**
appears only in the heterotrimer arm.

**The state readout.** A structure is called **active** when both of:

```
d(Y5.58 hydroxyl , Y7.53 hydroxyl)  <  9.08 Å      "NPxxY-OH"
d(2×46 Cα        , 6×37 Cα)         > 14.932 Å     "TM6 tilt"
```

Both thresholds are `midpoint(mean of actives, mean of inactives)` fitted on the
32-receptor panel (`DECISIONS.md` F-17). Continuous values are recorded alongside the
binary call, because the binary call alone throws away the size of the effect.

**The statistical unit is the paralog cluster, not the receptor.** Two receptors in
the same cluster are not independent evidence. Minimum detectable effect:
`1.218/√k` for interactions, `0.189–0.242` for main effects.

**Cost classes.** `free` = re-analysis of data already on disk. `cheap` = re-scoring
existing predictions, no new inference. `real` = new GPU inference.

**Prediction counts come in two grains.** `predictions_pooled` uses n=10 samples per
cell and supports pooled claims only. `predictions_percell` uses n=50 and supports
per-receptor claims. Group 1 totals **74,960 pooled / 212,920 per-cell** across all
2,039 rows; `PLAN.md`'s first pass is a **~38,300-prediction subset** of that.

---

# 3. The receptors — 64 in Group 1, all class A

Scope was closed to **class A only** on 2026-09-12 (`D-2026-09-12-d`). Class B and
class F receptors are excluded, not deferred.

Species: 1,933 rows human, 52 *Hasarius adansoni* (a jumping spider opsin, `B1B1U5`),
51 bovine (rhodopsin `OPSD`), 3 mouse.

### CORE32 — the main panel. 30 receptors, 29 clusters, 1,500 rows

The ladder, the composition controls, the nulls and the family swap all run here.

```
5HT5A  AA1R   AA2AR  ACM4   ADRB1  AGTR1  APJ    B1B1U5 C5AR1  CCKAR
CCR2   CNR2   DRD3   EDNRB  GHSR   GPR52  HRH3   LPAR1  LT4R1  MCHR1
MTR1A  NK1R   NPY1R  NTR1   OPRD   OPSD   PD2R2  S1PR1  SSR2   TSHR
```

**29 clusters over 30 receptors** — so MDE is `1.218/√29 = 0.226` for an interaction,
and `0.189–0.242` for a main effect.

### CORE32_GS — the Gs subset. 6 receptors, 6 clusters, 54 rows

`AA2AR  ADRB1  CCKAR  GPR52  NK1R  TSHR`. Used where the supplied partner must be Gs.

### G10_SCAN — the alanine scan panel. 10 receptors, 10 clusters, 360 rows

`ACM4  APJ  C5AR1  CCR2  CNR2  DRD3  EDNRB  HRH3  PD2R2  S1PR1`.
Ten receptors because the scan is 21 positions wide and the cost multiplies.

### C1_REST — the replication census. 24 receptors, 14 clusters, 72 rows

```
5HT1B ACM1  ACM2  ADA2A ADRB2 CCR5  CCR6  CCR8  CNR1  CXCR2 CXCR3 CXCR4
DRD2  FSHR  GPR6  HRH2  LSHR  MTR1B NPY2R OPRK  OPRM  OPRX  PE2R4 S1PR5
```
**24 receptors but only 14 clusters** — heavily paralogous, which is exactly why the
cluster unit matters.

### EXT_CHIMERA and REFCHIMERA_CORE32 — 10 and 12 receptors, 53 rows

```
5HT2A  5HT2C  ADA1A  DRD4  EDNRA  GRPR  HRH1  OX2R  OXYR  TA2R  (+ B1B1U5, OPSD)
```
Receptors whose only deposited reference is a chimera. Marked `EXTENSION` tier, kept
separate from `PRIMARY` so they cannot silently enter a primary count.

---

# 4. The partners — every chain B construct, with its length

`inputs/g1_partner_registry.tsv` holds **782 rows**, **771 with `held=yes` and a
sha256**, **10 marked `NO`**, one mislabelled. Sequences exist for **17 Gα families**:

```
Gi1 Gi2 Gi3 Go GoB Gz Gs Golf Gq G11 G14 G15 G12 G13 Gt1 Gt2 Ggust
```

Dispatched families across Group 1: **Gi/o 1,517 rows, Gs 372, Gq/11 150.**

### 4.1 The length ladder — the centrepiece

Each rung is the **C-terminal suffix** of the receptor's own cognate Gα α5 helix.
Every rung shares the same final residue; only the start moves.

| construct | residues | families held | rows | role |
|---|---:|---:|---:|---|
| `R0_apo` | **0** | — | 94 | no partner at all. The floor |
| `R1_ct11` | **11** | 17 | 90 | shortest rung |
| `R1b_ct13` | **13** | 16 | 30 | *(the "wet-lab" rungs — exist in the registry, missing only from `seq_rungs.tsv`)* |
| `R2_ct15` | **15** | 17 | 60 | |
| `R2b_ct17` | **17** | 16 | 30 | *(helicity rises sharply from 17 residues up)* |
| `R2c_ct19` | **19** | 16 | 30 | |
| `R3_ct21` | **21** | 17 | 154 | **the title's construct.** Also the reference rung for every control |
| `R4_a5helix` | **26** | 17 | 60 | the α5 helix as crystallographers define it |
| `R5_a5plus` | **36** | 17 | 90 | **α5 plus flanking.** The α5 helix is Asp368–Leu394, 27 residues, so 36 is *past* it. The Methods must never call this "a longer α5" |
| `R7_full` | **350–394** | 17 | 124 | the complete Gα subunit. The ceiling |
| `R8_hetero` | **761–805** | — | 30 | Gα + Gβ1 (340 aa) + Gγ2 (71 aa), three chains |

**Why a ladder and not a single length.** The proposed mechanism is helix formation,
which increases gradually with peptide length. The prediction is therefore a **smooth
curve**, and three points cannot resolve a curve. With the 13/17/19-mers the window
from 11 to 21 has **six points instead of three**.

**No 16-residue rung.** AlphaFold3's "16" governs how its training set was built, not
what it does at prediction time; Chai-1 uses 9 and keeps them; Boltz-2 has no such
line; OpenFold3 has no length branch at inference. There is no boundary for a 16-mer
to resolve (`DECISIONS.md` F-16).

### 4.2 The negative controls — "is it just bulk?"

Every one of these runs at **the same rung the real peptide runs at**. A control at a
different rung is uninterpretable.

| construct | residues | what it removes | rows |
|---|---:|---|---:|
| `R6a_da5` | 324–368 | the full subunit **with α5 deleted**. Same mass, same fold, no α5 | 30 |
| `R6b_a5perm` | 350–394 | full subunit with α5 **scrambled in place**. Same composition, wrong order | 30 |
| `R6c_a5polyA` | 350–394 | full subunit with α5 replaced by **poly-alanine**. Same length, no side chains | 30 |
| `ubiquitin` | **76** | an unrelated protein of similar size to a mini-Gα | 30 |
| `KaiB_2QKEE` | **91** | a second unrelated protein, different fold | 30 |
| `ct21@polyA` | 21 | the peptide itself as poly-alanine | 30 |
| `ct21@reversed` | 21 | the peptide backwards | 30 |
| `ct21@scramble#1..5` | 21 | five independent scrambles | 150 |
| `ct21@face_scramble#1..3` | 21 | scrambles that preserve the contact face | 90 |
| `ct21@gcn4_window` | 21 | a 21-mer from an unrelated helix (GCN4 leucine zipper) | 30 |

### 4.3 Specificity constructs

| construct | residues | question | rows |
|---|---:|---|---:|
| `ct21@ala_pos01..21` | 21 | **the alanine scan.** Each of the 21 positions replaced by alanine, one at a time | 210 |
| `ct21@gi2gs_sub01..15` | 21 | **Gi → Gs stepwise.** 15 single substitutions walking one family's tip into the other's | 150 |
| `@C379A`, `@F376A+L388A`, `@F376A+R380A+L388A` on ct17/ct19/ct21/a5helix | 17–26 | known uncoupling point mutants, as peptides | 42 |
| `alphas_F376A_L388A_mutant`, `..._triple_null` | 394 | the same mutants in the full subunit | 12 |
| **family swap** (`G9`) | varies | the receptor's **non-cognate** Gα | 30 |

### 4.4 Mini-G and deposited anchors

`M1_h4s6` (44–47), `M2_h4` (60–63), `M3_h3` (112–130), `M4_he` (203–221),
`M5_dHD` (236–279) — a nested series from the α5 outward, so the length axis is
covered from 11 residues to the full subunit without a gap.
`MG_5g53` (229), `MG_6fuf` (214), `MG_8f76` (261) — **deposited** mini-G constructs,
used as anchors because they exist in the PDB and are not our invention.

---

# 5. The MSA settings — what each chain is given

| setting | rows | meaning |
|---|---:|---|
| `receptor_msa = on (default)` | **2,039 — all of them** | chain A always gets its full alignment |
| `partner_msa = off` | **1,855** | chain B is supplied as **a single sequence, no alignment** |
| `partner_msa = ON` | **90** | the `G17` arm, which exists to price the choice above |
| `partner_msa = n/a` | 94 | the apo rows — there is no chain B |

**Why the partner alignment is off by default.** It holds the partner's evolutionary
information constant by construction, so a length effect cannot be an alignment
effect. **This is the first instance of one-chain single-sequence inside a complex in
all 83 papers we hold**, which is why `G17` (3,600 predictions) is blocking rather
than supplementary: without it, the headline arm carries an unmeasured manipulation on
four backbones with no published prior.

**A naming defect worth knowing:** `off` should read `query_only`. The chain is not
given *no* MSA; it is given itself.

**The receptor-side depth levels, for the Stage 2 control below: `{1, 8, 32, default}`.**
128 and 512 were dropped — Block D measured both and neither carries a turning point.
**Depth 1 was added** as the "no evolutionary information" endpoint. It is an anchor,
not a regression point, and must be excluded when fitting a slope in `ln(depth)`,
where `ln(1)=0` would give it leverage it has not earned.

---

# 6. The ligands — `inputs/g2_systems.csv`

**350 rows, 26 receptors, 25 clusters, 313 READY.**

```
5HT5A AA1R  AA2AR ACM4  ADRB1 AGTR1 B1B1U5 C5AR1 CCKAR CCR2  CNR2  DRD3  EDNRB
GHSR  HRH3  LPAR1 LT4R1 MCHR1 NK1R  NPY1R  NTR1  OPRD  OPSD  PD2R2 S1PR1 SSR2
```

### 6.1 The design: ligand role × partner level

Three partner levels — `R0_apo` (none), `R3_ct21` (the 21-mer), `R7_full` (the whole
subunit) — crossed with five ligand roles:

| ligand role | distinct ligands | apo | ct21 | full |
|---|---:|---:|---:|---:|
| **none** | — | 41 | 41 | 16 |
| **full agonist** | 20 | 36 | 36 | 16 |
| **neutral antagonist** | 16 | 29 | 29 | 13 |
| **inverse agonist** | 6 | 10 | 10 | 3 |
| **decoy** | 11 | 11 | 11 | 11 |

Named examples: agonists include adenosine (`NEC`), serotonin (`8K3`), LTB4 (`LTB`);
antagonists include **ZM241385** (`ZMA`), bosentan (`K86`), naltrexone-class (`EJ4`);
inverse agonists include **carazolol** (`CAU`) and **11-*cis*-retinal** (`RET`).

**The 98 ligand-free READY rows are title clause 2.** They give the complete 2×2 —
{partner, no partner} × {ligand, no ligand} — on **20 receptors / 19 clusters**, MDE
**0.279**, at **zero marginal cost**. The pre-registration is
`spec/C7_PREREGISTRATION.md` and is worthless once anything runs.

### 6.2 Ligand tiers, kept separate on purpose

`T1_small_molecule` 296 rows · `T2_peptide` 12 · `T3_mixed` 42.

A peptide ligand is **another polymer chain**, so pooling it with the small-molecule
tier would confound the ligand axis with the chain-count axis (`D-2026-09-12-f`).

### 6.3 The decoys, and the finding that came out of building them

A decoy is a molecule matched to the real ligand on molecular weight, logP, charge,
hydrogen-bond donors/acceptors and rotatable bonds, while being **topologically
dissimilar** and **inactive at the target**. Selection is frozen and gated by
`gates/drule.py` — **26 checks, every one proved by planting the defect it catches**,
with three digests including the assignment pairs.

**A property-matched decoy does not exist for 5 of 16 receptors** (`DECISIONS.md`
F-19). The limit is set by the native agonist's own chemistry: for very small or very
polar natural ligands, nothing in ChEMBL matches the properties while differing in
topology. The arm therefore runs as **EXPLORATORY at k=11 clusters** (MDE 0.367
against 0.352 at k=12 — a 4.4% cost) rather than being silently dropped.

**This finding stands whether or not the arm runs**, and it is a result about the
field's standard negative control, not about us.

---

# 7. What runs, stage by stage

The ordering principle: **everything that needs no GPU first**, so the decisions that
need Aditya stop blocking the rest.

## Stage 0 — costs nothing. Blocks everything below.

| item | what | why it blocks |
|---|---|---|
| Mine `rows.tier3.v2.csv` | cluster unit, continuous readout, seeds | **done** |
| **Add two pocket-RMSD columns** to `g1_recording_spec.tsv` | distance from the predicted pocket to the deposited **active** and **inactive** structures | Without them a depth sweep has **no reference-free readout** — model confidences are not comparable across masking levels. They are also what separates *"shallow MSA moves the number"* from *"shallow MSA makes a different object that trips the same two distances"* |
| **Option Z** | measure the real alignment depth per (receptor, rung), receptor side **and paired** | **A paired depth has never been measured by anyone** |
| Re-derive the thresholds | | decides which receptors are evaluable at all |
| **Pair the random seeds across arms** | | **free now, impossible after dispatch.** Blocks A and B both failed it: 1,898 distinct seeds over 380 cells, so the same seed never ran both arms of a cell |

## Stage 1 — the instrument. CPU only, no GPU. **This has run.**

**What it did:** measured the two axes on **1,357 deposited PDB structures** —
**726 calibration** (no ortholog anywhere in our panel), **610 application**
(on-panel, held out), **21 intermediates**.

**Why:** the thresholds were fitted on the same annotated structures the study then
grades with. The first objection a referee makes is that the ruler was built from the
answer sheet.

**Result — the inherited rule, applied unchanged to structures it never saw:**

| set | rule | n | sensitivity | specificity | Youden |
|---|---|---:|---:|---:|---:|
| calibration | both axes (AND) | 487 | 86.5% | **100.0%** | +0.865 |
| calibration | NPxxY alone | 487 | 86.7% | 98.8% | +0.855 |
| calibration | **TM6 tilt alone** | 585 | 96.6% | **100.0%** | **+0.966** |
| application | both axes (AND) | 485 | 93.4% | 100.0% | +0.934 |
| application | **TM6 tilt alone** | 501 | 100.0% | 97.8% | +0.978 |

**Two things fall out.** The rule survives off-panel with **zero false positives on 81
inactives** — a direct answer to the circularity objection, at no GPU cost. And **the
conjunction is worse than one of its halves**: tilt alone scores +0.973 against the
AND rule's +0.865 on the same rows. The NPxxY axis removes true actives and adds
nothing. That comparison is on rows the NPxxY axis itself selected, so it is not yet
safe to act on.

**What it did NOT do: fit a new threshold.** `GROUP0_SYSTEMS.md` §6 forbids fitting
before the balancing rule is settled, and that is **D4, still open**.

**Two counterexamples to carry into that decision:** one off-panel **inactive** sits
at 8.95 Å on NPxxY, below the 9.08 cut; one off-panel **active** sits at 12.11 Å on
tilt, below 14.932.

**A defect found while running it (`F-30`):** the two axes were **coupled** — a
non-tyrosine at 5.58 silently discarded the tilt measurement too, on an axis that
shares no atom with it. Fixing it withdrew **54** values produced by a numbering
nothing had validated (several sitting on the decision boundary: 14.760, 14.920,
14.951 against a cut at 14.932) and gained 115.

## Stage 2 — the competing explanation. Apo, monomer, four backbones.

**The rival claim is: "the models call the receptor active because you starved the
alignment, not because you added a partner."**

That claim is **apo and partnerless by construction**, so testing it needs **one
chain** — which is why this is the only stage deployable on all four backbones today.
It never touches the per-chain MSA mapping.

**Stage 1 of the control:** receptor depth `{1, 8, 32, default}` × `R0_apo` × no
ligand, on **CORE-L17 × 4 backbones × n=10 = 2,720 predictions**.

Three arms with three distinct jobs:

| arm | job | where the setting comes from |
|---|---|---|
| uniform random depth `{1,8,32,default}` | the cheap floor; connects to Block D | **coverage** — placed where the response is unexplored |
| **column masking at 40%** | the strongest available attack; **never done on GPCRs** | **inherited from `kalakoti2026afsample3`** |
| column shuffle at one shallow cell | information, or noise? | `waymentsteele2025reply`'s own control |

**The rule that makes this a control and not a fishing expedition: every
hyperparameter is inherited from published work on other proteins and is never tuned
on our panel.** Every paper in this area that tuned its subsampling parameter against
deposited structures is recorded in our corpus as oracle leakage — including the paper
we inherit the 40% from, which fitted it on the same 238 targets it reports.

**DBSCAN / AF-Cluster is declined**, on five grounds: 50–300× the cost, and at matched
sample size plain random matches or beats it; a published rebuttal exists; its
`min_samples` is never reported anywhere so it cannot be reproduced faithfully; none
of the three clustering papers touches a GPCR; and one of them discards exactly the
G-protein and nanobody partners that define an active GPCR entry.

**The caveat this stage owes, stated up front:** an apo-only control defeats the rival
explanation **as stated** and does **not** bound the complex case. Across all 83 papers
the monomer→complex boundary is never discussed as a boundary. Write the caveat; do
not spend predictions pretending to close it.

## Stage 3 — the main claim. The ladder.

`inputs/g1_systems.csv`, **2,039 rows, 23 arms**. The arms, by size:

| arm | item | rows | receptors | what it asks |
|---|---|---:|---:|---|
| `composition_controls` | G4a/G4b | 300 | 30 | is it the sequence, or just bulk? |
| `ladder` | G1a/G1b | 210 | 30 | **the main curve** |
| `ladder_pilot` | P1 | 210 | 30 | the same, as a contract proof before the real run |
| `ala_scan` | G10 | 210 | 10 | which of the 21 positions matter |
| `gi_to_gs_series` | G10b | 150 | 10 | walking one family's tip into another's |
| `intermediate_nested` | G1c/G1d | 90 | 30 | mini-Gα series, 44→279 residues |
| `intermediate_pilot` | P1b | 90 | 30 | its pilot |
| `deposited_minig_anchor` | G1f | 90 | 30 | deposited mini-G constructs as anchors |
| `wetlab_length_series` | G18a | 90 | 30 | **the 13/17/19-mers** |
| `a5null` | G3a/G3b | 90 | 30 | full subunit with α5 removed |
| `non_ga_bulk` | G3a/G3b | 90 | 30 | ubiquitin and KaiB |
| `partner_msa_on` | **G17** | 90 | 30 | **blocking.** Prices the query-only partner choice |
| `wide_replication` | G2 | 72 | 24 | does it hold on 24 more receptors |
| `family_swap` | **G9** | 30 | 30 | non-cognate partner — **NOT BUILT, see §10** |
| `gi_gt_single_residue` | G12 | 30 | 30 | a natural single-residue Gi/Gt pair |
| `heterotrimer` | G11 | 30 | 30 | Gα+Gβ+Gγ, three chains |
| `hd_deletion_companion` | G1e | 30 | 30 | helical-domain deletion |
| `intermediate_optional` | G1c-opt | 30 | 30 | |
| `chimeric_ref_extension` | G20 | 30 | 10 | chimera-only receptors |
| `uncoupling_peptide` / `_full` | G16 | 36 | 6 | known uncoupling mutants |
| `reference_matched_tip` | G19 | 23 | 12 | tip matched to the reference structure |
| `wetlab_matched_peptides` | G18b | 18 | 6 | peptides matched to published wet-lab work |

**Analyse length as a continuous variable, not as a step test.** The mechanism is
helicity and helicity is graded. A smooth monotone response is what the mechanism
predicts; a sharp step at any residue count is what would be surprising.

## Stage 4 — the ligand.

`inputs/g2_systems.csv`, §6 above. **313 READY rows, 8,716 pooled predictions.**

**State the goal as measurement, not as a predicted direction.** The honest goal is
*"measure the ligand's contribution at a fixed partner condition"*. It is **not**
"show the drug flips the receptor" — our own data points the other way: on
`rows.tier3.v2.csv` the decoy is indistinguishable from the antagonist on all four
backbones (+0.011, −0.004, −0.016, −0.004), and the ligand effect is small beside the
partner's. **A null here is a finding**, and the goal is worded so it can be reported
as one.

## Stage 5 — supporting material.

Peptide tiers kept separate from small molecules. The F-19 decoy-refusal finding. A
**date-stratified holdout** for the memorisation risk — using **Protenix's 2021-09-30**
as primary (32/32 receptors, 23 vs 20 clusters, zero panel change), **conditional on
re-deriving the cutoff from the model cards ourselves**, because `paper_af3` report
that three of their own documents give three different cutoff sets and every value is
flagged unverified in their own pre-registration. **OpenFold3 has no cutoff at all**
and is excluded from any date stratification.

---

# 8. The one adaptive parameter

Aditya asked that the partner condition used in the ligand arm be informed by what the
ladder finds. It can be, and this is the mechanism that makes it an adaptive design
rather than a choice made after seeing results.

> **The ligand crossing runs at the SHORTEST rung whose pooled apo→cognate shift,
> measured on the Group 1 ladder, falls inside the band `[PI lower]`–`[PI upper]`.**
> Ties break toward the shorter construct. A rung is excluded **on feasibility** —
> never on its effect size — if a backbone cannot represent it, or if its partner
> alignment is single-sequence in practice at that rung.

**Why a band and not a maximum.** The criterion must reference **headroom**, a property
of the measurement, never **effect size**, a property of the result. Selecting the rung
with the largest shift would select the partner condition that most flatters our own
effect. And headroom is the binding constraint: apo sits at **0.158** and cognate at
**0.891**, both pinned, so an interaction estimated at either endpoint has nowhere to
move.

**What is NOT adaptive:** the cognate identity (frozen so the supplied peptide and the
scoring reference are the same molecule), and the matched nulls (they run at whatever
rung the real peptide runs at — a null and its treatment at different rungs is
uninterpretable, and it is the failure an adaptive design produces by accident).

**The band is not set.** Roughly 0.25–0.75 is the shape; the number is Aditya's and
must be recorded **with its date, before any ladder result exists**. A gate then
asserts mechanically that the enacted rung equals the rule applied to the results.

---

# 9. Thirteen experiments that are NOT in the catalogue

Found 2026-09-14 by an audit against all 45 catalogued experiments; each screened for
already-catalogued, already-published, and feasible-and-powered. Full detail in
`EXPERIMENT_GAPS_2026_09_14.md`. **Six cost nothing.** The four that matter:

**R0 — the recording-contract amendment.** Not an experiment; a precondition. See §10.

**T2 — the register slide, 600 predictions.** Every construct in the campaign is a
**suffix** of its parent, by construction — so every rung, null and scramble shares the
same final residue. The campaign varies length, composition and identity and has
**never varied position**. Take the native α5 sequence and slide the window: if a
21-mer from the wrong section works as well, the title must say "an α5-derived
peptide", not "the α5 C-terminus".

**X1 — the anchor-quality census, free.** 65.5% of 32,000 existing rows have at least
one of the atoms used for the state call below pLDDT 70. The rate differs sharply by
arm — 55.9% cognate against 28.6% apo, and OpenFold3's apo cells keep 19 of 2,000
rows. So every arm comparison is partly a comparison of which rows survived. Carry
`min_plddt_at_anchor` as a **covariate**, never as a filter — conditioning on a
post-treatment variable is a collider.

**T1 — templates crossed with partner.** Templates are the field's standard way of
supplying structural information, and **nobody has ever switched them on in either
campaign**. This matters because the strongest published counter-example to our work
reaches alternative conformations **with templates on**.

---

# 10. Known defects — stated, not hidden

1. **The recording contract records LESS confidence data than the frozen campaign
   already holds.** `inputs/g1_recording_spec.tsv` is 49 rows and names
   `plddt_partner_chain_mean` and `plddt_ga_alpha5` — **both partner-side**. It does
   **not** name `plddt_mean`, `plddt_at_anchors`, `min_plddt_at_anchor`, ipTM, PAE,
   Ramachandran, chain breaks, templates or recycles. **Blocks B and D each hold four
   confidence columns.** Title clause 3 is a confidence claim. Fix by editing
   `build/g1_recording_spec.py`, re-running, then `build/manifest.py`. **Free today,
   impossible after dispatch.**
2. **`family_swap` (G9) is enumerated and NOT built.** All 30 rows carry
   `chain_b_sha256 = PENDING:COUPLING.md`.
3. **Templates have never been a factor**, and the frozen campaign's "templates off"
   rests on launcher defaults and static analysis, never on a per-row runtime echo.
4. **15 of 65 files in `inputs/` name no generator.** Two are unattributable by
   construction — written through an argparse `--out` the static scan cannot see.
5. **There is no GPU-hour model.** Every cost figure anywhere is a **count of
   predictions**, and `RUN_MATRIX.md` §1.4's own bracket spans a factor of **13**.
6. **`PLAN.md` names zero experiment IDs**, so the stage ↔ experiment join had to be
   authored by hand in `build/run_registry.py`. Read `run_registry.tsv`'s pillar
   column rather than inferring one.
7. **Stage 2 discharges no catalogued experiment at all** — its main arm has no E-id.
8. **A contradiction needing a decision, not a patch:** Stage 2 says an apo-only
   control does not bound the complex case and not to spend predictions on it, while
   two other documents schedule exactly that.

---

# 11. Two failure patterns that govern how results may be reported

Both were identified on 2026-09-14 after each had already occurred more than once.

**F-32 — a count is not a rate until you can name what was in the denominator and
what could never have been in the numerator.** Two Block D receptors (EDNRB, GRPR)
carry **leucine at 7.53**, so the NPxxY distance does not exist for them; all 1,960 of
their rows are `nan` on that axis, and they entered a published table at **0% active**
— which reads "never active" and means "never measurable". A null over an undefined
population **looks like data**: it has a value, a row count and a confidence interval.

**F-33 — when the selection criterion is the result, the agreement is not
information.** If we pick the subsampling method that produces the most active-state
calls, we have picked the method that best mimics our own result. The published
finding that AlphaFold reaches active GPCR states because its training set contained
many active GPCRs sharpens this: **reaching active is what the null does, and reaching
INACTIVE is the informative direction.**

**The rule both impose, cheap only because nothing has run:** every arm whose method
or parameter is chosen must **pre-register the choice rule, and the rule must not
mention the outcome**. Select on a property of the **input** — depth, diversity,
cluster count — never on a property of the **output**. Where performance must decide,
decide it on a **held-out** set outside the reported panel, and say so.

---

# 12. Decisions waiting

| decision | blocks | where |
|---|---|---|
| **D4** — the balancing rule for fitting the state threshold | the whole Group 0 fit | `GROUP0_SYSTEMS.md` §6, `ASKS.md` |
| **the adaptation band** `[PI lower]`–`[PI upper]` | must be recorded **before** Stage 3 runs | §8 above |
| **the recording contract** | free now, impossible after dispatch | §10 item 1 |
| **which of the 13** | — | `EXPERIMENT_GAPS_2026_09_14.md` |

---

# 13. How to check any of this yourself

```bash
python3 build/manifest.py                  # re-hash all 65 inputs
python3 gates/layout.py --selftest-all     # prove the structural checks by planting
python3 gates/g0_preflight.py --selftest   # Group 0
python3 gates/g1_preflight.py --selftest   # Group 1
python3 gates/g2_preflight.py --selftest   # Group 2, the ligand arm
python3 gates/ligands.py --selftest        # 10 checks
python3 gates/drule.py --selftest          # 26 checks, the decoy rule
python3 build/g0_measure_axes.py --selftest    # reproduces 16 shipped values
```

**Run the self-tests rather than trusting a sentence about coverage.** On 2026-09-12 a
claim that every check was proved by planting had been false for a day: the harness
copied only top-level files, every plant failed to apply, every check reported MISS,
and it printed a tidy tally.
