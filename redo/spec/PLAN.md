# PLAN.md — the campaign plan of record

> **Written 2026-09-12. This is the ORDERING document.** It says what runs, in what
> order, and what each stage buys. It does **not** restate the specs — every pillar
> points at the document that enumerates it, and where the two ever disagree **the
> enumerating spec and `inputs/` win, not this file.** A plan that carries its own
> copy of a count is how four counts on this project drifted from their own bodies.
>
> Supersedes any pillar or stage framing circulated in conversation. Decisions live
> in `DECISIONS.md`; this file only sequences them.

---

## 0a. THE ROUTE, DECIDED 2026-09-12 after an adversarial audit

**Four of seven load-bearing claims were contested by an audit commissioned for the
purpose, and the contests held.** The largest is `DECISIONS.md` **F-23**: C7 was not
answered, because `rows.tier3.v2.csv` has no ligand-free row. **Read F-23 before this
plan.** The route below is the post-audit one.

**Run "option-invariant first": do everything that does not depend on an open decision,
so the open decisions stop blocking.** Order, with three grafts taken from the
runner-up strategies:

| step | what | cost |
|---|---|---|
| 0 | strike the dead scope language; stage the C7 pre-registration | **free** |
| 1 | the **four-item** decision message (`ASKS.md` head), not nine | free |
| 2 | fix the adaptation band **before** it is stamped | free |
| 3 | seed pairing + the recording columns into `runs/README.md`, then send it | free |
| 4 | the free registry items, **E7.4 first** — it must precede the ligand arm | free |
| 5 | `ladder_pilot` as a **contract proof**, not science | 2,100 |
| 6 | the ladder **plus `wetlab_length_series`** as ONE curve — **graft 1** | 8,400 + **3,600** |
| 7 | apply the band mechanically, under a gate | free |
| 8 | nulls, bulk, composition controls and **G17** at the selected rung | 15,480 |
| 9 | all 313 READY Group 2 rows, **C7 arm named and pre-registered** — **graft 2** | 8,716 |

**≈38,300 pooled predictions in the first pass.** Hold the n=10→50 uplift in reserve,
with `ala_scan` (4,200) as its **first** call rather than a uniform increase.

**Graft 1 — the 13/17/19-mers exist.** Verified: `g1_partner_registry.tsv` carries
`R1b_ct13`, `R2b_ct17` and `R2c_ct19` for **16 Gα families, 50 rows, all `held=yes`,
all with a sha256**, and `g1_systems.csv` already enumerates them as 90
`wetlab_length_series` rows over the same 30 receptors at **3,600 pooled**. They are
missing only from `seq_rungs.tsv`. **For +3,600 the ladder's 11–21 window goes from
three points (11/15/21) to six (11/13/15/17/19/21)** — and §"analyse as a continuous
covariate" is the reason that matters: lit confirmed the mechanism predicts a **smooth
graded curve**, and three points cannot resolve a curve.

**Graft 2 — the C7 arm costs nothing.** `g2_systems.csv` already has 98 READY
ligand-free rows and **20 receptors / 19 clusters** with the complete 2×2, MDE **0.279**.
Pre-registration drafted at `redo/spec/C7_PREREGISTRATION.md`; it is **worthless after
dispatch**.

**Graft 3 — the memorisation defence is free, CONDITIONALLY.** `PANEL.md` §8
recommendation 1: use **Protenix's 2021-09-30** as the primary date stratification —
32/32 receptors, 23 vs 20 clusters, **zero panel change** — with Boltz-2's 12/52 as the
explicitly under-powered secondary.

> **CONDITION added 2026-09-13 (`F-24`).** `paper_af3` state that **three of their own
> documents give three different cutoff sets for the same quantity**, that every value is
> flagged `training_cutoff_verified=NO` in their own pre-registration, and — verbatim —
> **"do not build a stratification on any of them without re-deriving."** We inherited the
> current set, so the *number* is right; the *provenance* is not. **The stratification is
> conditional on re-deriving the cutoff from the model cards ourselves**, and until that
> is done this graft is not free — it is cheap and unverified, which is a different thing.
> **OpenFold3 has no cutoff at all** and is excluded from any date stratification by
> their documented position, not by our choice.

**The title this commits to**, with the numeral withheld until step 6 returns:

> *The Gα α5 C-terminus, supplied as a co-input, drives co-folding models into the active
> GPCR state — and its effect is graded with length.*

**If the band selects a rung shorter than 21, the title takes that number. That is the
finding, not a failure.**

---

## 0. The one-paragraph version

Two of the paper's three title clauses are reachable with **zero GPU**, and the
expensive arm serves only the third. So: **free work first, then the instrument, then
the defence against the competing explanation, then the main claim, then the ligand.**
Every pillar is a stopping point that buys a complete sentence. Nothing here is a
single commitment that buys nothing until all of it lands.

---

## Pillar 0 — Free. Nothing below starts before this.

| item | cost | why it blocks |
|---|---|---|
| Mine `rows.tier3.v2.csv`, steps 3–5 — cluster unit, continuous readout, seeds | **0 predictions** | steps 1–2 are done; the partner effect already survives per backbone |
| Add **pocket-Cα-RMSD to active** and **to inactive** to `g1_recording_spec.tsv` | 0 | see below — this is blocking, not cosmetic |
| Measure the real MSA depths along the ladder, receptor side **and paired** (Option Z) | 0 GPU, ~300 queries | a paired depth has never been measured by anyone |
| Re-derive the predicate thresholds (PF-6) | 0 | decides which receptors are evaluable |

**Why the two columns are blocking.** `g1_recording_spec.tsv` carries 47 columns and
**no pocket-RMSD column at all** — its only `rmsd` field measures the partner
(`ras_domain_ca_rmsd_to_R7`). Without them a depth sweep has **no reference-free
readout**, because `kalakoti2025afsample2` [p.6] states model confidences across
masking levels are *"not directly comparable"*. They are also what separates
*"shallow MSA moves the number"* from *"shallow MSA produces a different object that
trips the same two distances"* — the second being a far stronger result, and one we
currently cannot claim even if it is true. See `MSA_SUBSAMPLING.md` §5.2(c).

---

## Pillar 1 — The instrument. CPU only, no GPU.

**The measurement pass**: 726 calibration + 610 application + 98 pinned reference
rows, ~1–3 GB of cached mmCIF, two axes.

**Four of Group 0's eight outstanding dependencies sit behind it** (D3, D4, Q6, and
the F3 sensitivity), and **all five E0 experiments are BLOCKED on it**. Until it runs,
every state call in every pillar below rests on a threshold **inherited** from the
frozen campaign rather than derived here. It must also measure the **F3-removed**
structures, or that filter stays permanently unauditable (`DECISIONS.md` F-12).

**Does not start without Aditya's word.** Standing instruction, unchanged.

---

## Pillar 2 — The defence. Apo, monomer, four backbones.

**The competing explanation is: "the models call the receptor active because the
alignment was starved, not because a partner is present."** It is apo and partnerless
by construction, so measuring it is a **monomer** — which is why this pillar is the
only one deployable on all four backbones today: it never touches the per-chain MSA
mapping. Three arms, three distinct jobs:

| arm | job | where its setting comes from |
|---|---|---|
| uniform random depth `{1, 8, 32, default}` | the cheap floor; connects to Block D | **coverage** — placed where the response is *unexplored*, not where it optimises |
| **column masking at 40 %** | **the strongest available attack; never done on GPCRs** | **inherited from `kalakoti2026afsample3`** |
| column shuffle at one shallow cell | information, or noise? | `waymentsteele2025reply`'s own control |

Details, levels and the staged bill: `MSA_SUBSAMPLING_REGIMES.md`.

### The rule that makes this a control rather than a forking path

**Every hyperparameter is INHERITED from published work on other proteins and is
never swept on our panel.** Every paper in this area that tuned its subsampling
hyperparameter against deposited structures is recorded in our corpus as oracle
leakage — including `kalakoti2026afsample3`, whose AF3 40 % was fitted on the same
238 targets it reports results on, with no memorisation control. `suzuki2026pairscaling`
shows the clean form: a **structure-free** selection criterion on a fixed shared MSA.
**What separates the two is whether the criterion references the deposited answer.**

*(Our depth levels `{1, 8, 32, default}` were placed partly because no backbone turned
over at depth 8 in Block D. That is our own data — but used for **coverage**, not to
maximise an outcome. Say so in the Methods in those words rather than leaving it
implicit.)*

### DBSCAN / AF-Cluster is DECLINED, on five grounds

50–300× the cost (1–2 runs against 95–329, and at **matched n** — 330 vs 329 — plain
random still matches or beats it); a published rebuttal against it
(`schafer2025confounds`); **`min_samples` is never reported anywhere**, so we could not
reproduce it faithfully; **none of the three clustering papers touches a GPCR**, and two
say so explicitly; and `bryant2024cfold`'s chain filter actively discards the
G-protein/arrestin/nanobody partners that define an active-state GPCR entry.

### The caveat this pillar owes, stated up front

**An apo-only control defeats the rival explanation as stated, and does NOT bound the
complex case.** Across all 83 papers the monomer→complex boundary is **never discussed
as a boundary**. `mitjavila2026afsample2t` is the only paper with the design to measure
transfer — it masks the same receptor alone and in complex, 250 per cell — and it
**never contrasts them**: the two cells are pooled into one docking ensemble, the state
label is assigned to the input condition *a priori*, and the readout is binding-site
side-chain RMSD, producing *"local side-chain and backbone heterogeneity in the pocket,
not alternative global states"*. Sharper: **ye's subsampling arm runs on AlphaFold2, not
Multimer, so the only GPCR MSA-manipulation test with a state readout is itself
apo-side.** Write the caveat; do not spend predictions pretending to close it.

---

## Pillar 3 — The main claim. The ladder, with G17 as a blocking companion.

Enumerated in `GROUP1_SYSTEMS.md` and `inputs/g1_systems.csv` (2,039 rows, 23 arms).

- **Length ladder: 11, 13, 15, 17, 19, 21, 26, full.** **No 16-mer** — see below.
- **The matched nulls that answer "is it just bulk?"**: α5-deleted (`R6a_da5`),
  α5-scrambled-in-place (`R6b_a5perm`), poly-alanine α5 (`R6c_a5polyA`), and an
  unrelated protein of similar size (ubiquitin, `KaiB_2QKEE`).
- **Specificity**: family swap, the Gi/Gt single-residue natural pair, the 21-position
  alanine scan, and known uncoupling point mutants.
- **G17 — partner MSA on vs off — is BLOCKING and belongs here, not in the SI.**
  3,600 predictions. Our primary design runs the partner chain at query-only depth,
  which is **the first instance of one-chain single-sequence inside a complex anywhere
  in 83 papers**. With G17 that is a *measured* choice with its price attached; without
  it, it is an unmeasured manipulation under the arm that carries the headline, on four
  backbones, with **zero published prior on cross-chain effects**.

### Analyse the ladder as a CONTINUOUS covariate, not as a step test

`DECISIONS.md` **F-16** withdrew the length/taxonomy confound in three revisions, and
lit re-confirmed it 2026-09-12 with two further arguments:

- **Mazzoni's abstract argues the graded reading by itself.** Sentence [2] is plural —
  *"The Gαs peptides stimulated specific binding"* — and [3] is a **comparative**,
  *"Three peptides … were the most effective"*, which presupposes a field in which the
  others were effective. **The abstract asserts a ranking, not a threshold.**
- **The mechanism is helicity, and it is graded**: *"peptides containing 17 and more
  amino acid residues have a **stronger propensity** to assume an α-helical
  conformation"*. Both ends form helices of different length — the **11-mer's spans
  Arg389–Leu394, the 21-mer's Asp381–Leu394**. So the predicted observable is **helix
  length rising with peptide length, a continuous covariate. A smooth monotone response
  is what the mechanism predicts; a sharp step at any residue count is what would be
  surprising.**

**Therefore: do NOT build a 16-mer rung.** AF3's 16 governs training/evaluation set
construction, not inference (peptides are in its accuracy and calibration numbers,
excluded only from the low-homology generalization subset); Chai-1 uses 9 **and keeps
them**; Boltz-2 has no taxonomy line; and OpenFold3 has no length branch at inference
at all. There is no boundary at inference for a 16-mer to resolve.

**A ceiling, recorded 2026-09-12:** the α5 helix is **Asp368–Leu394, 27 residues**.
`R4_a5helix` (26) is inside it; **`R5_a5plus` (36) is past it**, so the Methods must
describe that construct as α5 **plus flanking**, never as a longer α5.

**What survives F-16 is a different question**: short chains were clustered at 100 %
identity in training and are absent from published generalization evidence. That is a
**memorisation** risk, answered by a date-stratified holdout (Pillar 5), not by a rung.

---

## Pillar 4 — The ligand. Partner held, ligand swapped.

Enumerated in `GROUP2_LIGANDS.md` and `inputs/g2_systems.csv` (350 rows).

T1 small-molecule agonist vs antagonist at a fixed partner condition. **This is title
clause C7.**

**State the goal as measurement, not as a predicted direction.** The honest goal is
*"measure the ligand's contribution at fixed partner condition"*. It is **not** "show
the drug flips the receptor" — our own data points the other way: on
`rows.tier3.v2.csv` the decoy is indistinguishable from the antagonist on all four
backbones (+0.011, −0.004, −0.016, −0.004), and the ligand effect is small beside the
partner's. **A null here is a finding, not a failure**, and the goal must be worded so
it can be reported as one.

The **decoy arm rides along as EXPLORATORY at k = 11**, frozen — `DECISIONS.md`
D-2026-09-12-h, gated by `drule.py` (26 checks, 26 proved).

---

## Pillar 5 — The SI.

- **Peptide tiers T2 and T3, kept separate.** A peptide ligand is another polymer
  chain, so pooling it with the small-molecule tier confounds the ligand axis with the
  chain-count axis. D-2026-09-12-f.
- **F-19, the decoy-refusal finding** — a property-matched, charge-matched,
  topologically dissimilar decoy set does not exist for 5 of 16 Class A GPCRs, and the
  limit is set by the native agonist's chemistry. Stands whether or not the arm runs.
- **A date-stratified holdout** for the memorisation risk that survives F-16.

---

## The pre-registered adaptation rule — how Pillar 3 feeds Pillar 4

**Aditya, 2026-09-12: the plan must stay flexible enough for the partner condition used
in the ligand arm to be informed by what the many-combination arms find.** It can, and
this is the mechanism that makes it an adaptive design rather than a post-hoc choice.
**The rule is committed BEFORE Pillar 3 runs; only then is the adaptation mechanical.**

### What is NOT adaptive

**The cognate identity stays frozen.** `coupling_cognate_map.tsv` reads each receptor's
Gα off the structure it was solved with — 47 from structure, 6 by convention, 1 with a
caveat, 10 chimeras that stop deliberately. It was frozen for a reason unrelated to
outcomes: **the supplied peptide and the scoring reference must be the same molecule.**
Re-picking the cognate on which assignment agrees better would destroy that guarantee
and the arm would stop measuring what it exists to measure.

**The matched nulls are not adaptive either.** Scrambled α5, poly-alanine, α5-deleted
and the unrelated-bulk control **run at whatever rung the real peptide runs at**,
selected by the same rule. A null and its treatment at different rungs is an
uninterpretable comparison, and it is the failure an adaptive design produces by
accident.

### What IS adaptive: the cognate rung for the ligand crossing

All 64 relevant rows of `g2_systems.csv` already carry
`pi_choice = "cognate rung for the ligand crossing: R3_ct21 | R7_full | both"`.
That is the adaptive parameter, and it is the only one.

### The rule

> **The ligand crossing runs at the SHORTEST rung whose pooled apo→cognate shift, measured
> on the Group 1 ladder, falls inside the interior band `[PI: lower]`–`[PI: upper]`.**
> Ties break toward the shorter construct. A rung is **excluded on feasibility** — never
> on its effect size — if (i) any backbone cannot represent it natively, or (ii) Option Z
> shows its partner alignment is single-sequence in practice at that rung.

**Why a band and not a maximum.** The criterion must reference **headroom**, a property
of the measurement, never **effect size**, a property of the result. Selecting the rung
with the largest shift would select the partner condition that maximises our own effect
— the identical error to tuning a masking rate on our own panel, or to picking the decoy
rule that clears its own cluster bar. And we already know headroom is the binding
constraint: **apo sits at 0.158 and cognate at 0.891**, both pinned, so an interaction
estimated at either endpoint has nowhere to move. `CATALOGUE.md` already advises the
middle rungs for exactly this reason.

**`[PI]` — Aditya sets the band before Pillar 3 runs.** A shift in roughly `0.25`–`0.75`
is the shape; the number is his, and it must be recorded here with its date **before**
any ladder result exists.

**Enforcement.** Once the band is set, a gate check asserts that the enacted rung equals
the rule applied to the Group 1 results, so the adaptation cannot drift silently — the
same treatment `drule.py` gives the decoy selection.

---

## Two attribution rules, to be honoured in Methods

1. **The OpenFold3 "no length branch at inference" finding is `paper_af3`'s package
   grep, NOT the literature.** The corpus holds no OpenFold3 paper at all. Attribute it
   to them.
2. **Mazzoni's six-peptide panel and all the helicity data reach us through a REVIEW** —
   `[dursi2011signalpeptides]`, reporting Mazzoni and Albrizio et al. *Biopolymers*
   2000;54(3):186–194. **Neither primary is held.** Cite the review as reporting them,
   never Mazzoni directly. A relayed quote is not a verified quote, and that rule has
   already been broken once on this project.

**One residual ambiguity, stated rather than resolved.** Mazzoni's sentence [10] can
still be read as "not effective at anything", and it bundles the length control with a
Gαi1/2 family control, so its scope cannot be pinned without the PDF. **That ambiguity
is itself an argument against building a rung on a threshold**, which is what F-16
concluded.

---

## Corrections from the registry triage, 2026-09-12 — what this plan MISSED

**Written the same day as the plan, by the triage that joined the registry to it.**
Recorded rather than silently patched, because a plan that quietly absorbs its own
gaps teaches nobody anything.

**1. `PLAN.md` names ZERO experiment ids.** A grep returns nothing, so the pillar ↔
experiment join could not be parsed and had to be authored by hand in
`run_registry.py`. The pillar column in `run_registry.tsv` is now the join; **read it
rather than inferring one from this document.**

**2. Pillar 2 discharges no catalogued experiment at all.** The pillar column runs
0, 1, 3, 4, 5 — never 2. Its arms come from `MSA_SUBSAMPLING_REGIMES.md`, whose
Stage 1 (2,720 predictions, that document's own top recommendation) carries **no
E-id**, and which assigns ids only to Stages 0, 2, 2b and 3. Either Stage 1 gets an
id or the catalogue is missing the experiment it is.

**3. Pillar 0 is NOT `RUN_MATRIX` Stage 0, and the difference is eleven free items.**
Stage 0 covers 14 experiments across S0.1–S0.7; Pillar 0 lists four and **none of
them is an S0.x row.** Omitted and free:

| omitted | why it matters |
|---|---|
| **E7.4** interaction power injection | `RUN_MATRIX` §4.3 and `CAMPAIGN` §2.8 both say it must **precede the ligand arm**. Pillar 4 says *"a null here is a finding, not a failure"* and does not schedule the one free thing that makes a null **bounded** rather than unanswerable |
| **E4.2** exposure vs effect size | `CAMPAIGN` promotes it to a **hard predecessor** of the bulk control, and PF-9 requires the median split declared **before** dispatch — which Pillar 3 does |
| **E5.4** dose–response on engagement depth | the placement covariate the ladder needs from 11 to 394 residues |
| **E9.1 / E9.3** the apo floor, and the never-pool convention | **Group 9 appears in no spec but `CATALOGUE.md` and `CAMPAIGN.md`** — not in `RUN_MATRIX` §7.1, not here — while **Pillar 2's depth levels are justified by Block D's floor** |
| E0.4, E4.3, E3.3, E5.3, E5.5, E7.1 | all free, none scheduled |

**4. `E6.4` — pair seeds across arms — is in no pillar, and it is FREE NOW AND
IMPOSSIBLE AFTER Pillar 3 dispatches.** Blocks A and B both failed it: 1,898 distinct
`seed_outer` over 380 cells, so the same seed never ran both arms of a cell. `ASKS.md`
A2.

**5. Pillar 1's measurement pass excludes exactly the structures `E0.3` measures.**
726 + 610 is the Active/Inactive population; the Class A **Intermediates** are 21 rows
that `D-2026-09-12-d` set aside. Adding them is one decision and 21 structures.

**6. Pillar 5 costs `E4.1` as SI work**, while `CAMPAIGN` §2.5 records that it **became
free** — Protenix splits 16/14 and Chai 21/9 on the frozen 30.

**7. A CONTRADICTION this plan created, and it needs Aditya, not a patch.** Pillar 2
says an apo-only control *"does NOT bound the complex case … write the caveat; do not
spend predictions pretending to close it."* `MSA_SUBSAMPLING_REGIMES.md` §5 schedules
Stage 2 as depth × partner rung, and `CAMPAIGN.md` §2.9 says E8.1 *"SURVIVES, and gains
urgency."* **Those cannot all stand.** `ASKS.md` A9.

**8. One disagreement about what is already done.** This plan says Pillar 0's mining
"steps 1 and 2 are DONE"; `FIRST_LOOK.md` says *"step 1 … is done; steps 2–5 are not."*
**The plan is right and `FIRST_LOOK.md`'s line is stale** — `PER_BACKBONE.md` is step 2
and it landed the same day. Steps 3–6 are now done too
(`STEPS_3_TO_6.md`, `WHAT_IT_MEANS.md`), so Pillar 0's mining item is **complete**.

---

## What this plan does NOT do

- It does not decide the **title**. Two of three clauses still have no result: C7 is
  reachable in Pillar 0, **C6 needs Pillar 3**. If the ladder does not run, the title
  narrows to a Gα co-input and its C-terminal determinant. That is Aditya's call and
  nothing here pre-empts it.
- It does not authorise any compute. **Pillars 1 onward each need his word.**
- It does not control for three of the four MSA-manipulation families — clustering,
  composition purification and column masking beyond the single inherited rate.
  **Bounding that claim in the paper is free; letting "we varied MSA depth" stand in for
  "we controlled for MSA manipulation" is not honest.**
