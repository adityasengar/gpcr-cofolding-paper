# MSA subsampling and conformational diversity — corpus answers

lit-3d, 2026-09-12, for paper-6f. Written to disk at their request because their session
was about to compact. **Staleness check run first: zero PDFs without an extraction.**
Corpus 83 notes / 83 INDEX / 87 bib. Nothing unextracted bears on these.

**The headline, up front: the competing explanation is weaker than you fear, and the
corpus's best evidence against it is on β2AR with a receptor-state readout.
`ye2026multistatebias` ran MSA clustering and depth reduction on β2AR and reports that they
do NOT recover the active state, while supplying the partner does. But it is not a clean
within-model comparison, and one backbone reaches both states on apo β2AR with no
manipulation at all. Both caveats matter and are set out in §2.**

---

## 1. Which papers subsample, and what they achieved

**Your expected list is wrong in one place and incomplete by fifteen.** `msa-subsample`
fires on **20 of 83** papers:

`bryant2024cfold`, `cheng2026af3cluster`, `chiesa2025templatebias`, `feldman2026alphainterp`,
`jung2026boltzperturb`, `kalakoti2025afsample2`, `kalakoti2026afsample3`, `lee2025seqassoc`,
`lee2026foldswitch`, `mitjavila2026afsample2t`, `richman2025conformix`, `schafer2025confounds`,
`suzuki2026conforflux`, `suzuki2026pairscaling`, `swapna2025memorization`, `vo2026fiducials`,
`waymentsteele2024cluster`, `waymentsteele2025reply`, `xing2025purified`, `ye2026multistatebias`.

**`heo2022multistate` is NOT one of them.** It carries `msa-state-filter`, and its protocol is
**state-annotated templates plus total MSA deletion applied together** — a confound by
construction, not a depth manipulation. Do not cite it as subsampling.

`af-cluster` fires on 11, and note the collision already recorded in `lit/CLAUDE.md`: in
`kohlhoff2014gpcr` that tag marks a **Markov state model**, not MSA clustering.

**What the main ones actually did:**

| paper | method | systems | outcome |
|---|---|---|---|
| `waymentsteele2024cluster` | AF-Cluster: DBSCAN on ColabFold MSA by edit distance, AF2 per cluster. **Uniform subsampling at \|MSA\| = 10 and 100, 500 samples each, is reported as a distinct and *weaker* arm, not the method** | KaiB, RfaH, MAD2 (metamorphic) | both states sampled with high pLDDT; three predicted point mutations flipped KaiB_RS, NMR-confirmed |
| `schafer2025confounds` | CF-random: plain random shallow MSAs, max-seq = 1 (KaiB), 8 (Mad2) | KaiB, Mad2, RfaH | **rebuttal — see §6** |
| `waymentsteele2025reply` | column shuffling as a control | same three | **rebuttal of the rebuttal — see §6** |
| `kalakoti2025afsample2` | AFsample2 — random MSA *column* masking to X at AF2 inference | open/closed + transporters | 15% masking improves alternate-state models; **non-monotonic optimum, target-specific** |
| `kalakoti2026afsample3` | same idea ported to AF3 | — | **40% optimal for AF3**; "the optimal level of MSA randomization is protein specific" |
| `mitjavila2026afsample2t` | **targeted** column masking around the orthosteric pocket | **GPCR class A** | 73.8% of binding sites within 1.5 Å vs 60.7% default AF2 |
| `bryant2024cfold` | MSA clustering at 8 cluster sizes [16…5120], 13 samples each = 104 predictions/target | general protein; **no GPCR, no 7TM of any kind** | alternative conformations recovered |
| `jung2026boltzperturb` | masking rate 0.1; depth reduced to 4,086 rows | Boltz-2, single-chain single-ligand | **both degrade below vanilla** (SR_O 10.53% and 12.28%) |
| `ye2026multistatebias` | AF-Cluster + uniform **U10 / U100** | PfMATE, LAO, SecA, **β2AR** | **insufficient — §2** |
| `xing2025purified` | subsetted MSA by "sequence purity" | EGFR | *"the successful sampling of alternative states depends **not on MSA depth but on sequence purity**"* (p.3) |

## 2. GPCRs specifically — and did it give the ACTIVE state? **This is the crux and the answer is no**

**Only 4 of 83 papers carry both `gpcr` and `msa-subsample`**: `chiesa2025templatebias`,
`mitjavila2026afsample2t`, `vo2026fiducials`, `ye2026multistatebias`. Of those:

- **`mitjavila2026afsample2t`** masks around the **orthosteric pocket** and reads out
  **binding-site RMSD**, not activation state. Its states come from the *input* (receptor-alone
  inactive vs G-protein active), not from the masking.
- **`vo2026fiducials`** tested subsampling **only in a benchmark sweep** — *"limiting the depth
  of the MSA sampling ranging from 16:32 to 256:512"* with 50 seeds per approach (p17) — and its
  receptor states are `NOT APPLICABLE`, determined by cryoEM.
- **`chiesa2025templatebias`** subsamples/masks only inside two of six protocols, and its own
  finding is that **the partner beats the operator handles**.

**`ye2026multistatebias` is the one that actually asks our question, on β2AR, with a state
readout — and it answers against the competing explanation.** Design, verbatim (p.15):

> "As controls, we also generated **uniformly random sub-MSAs of depth 10 (U10) and 100 (U100)**
> to test whether evolutionary structure in the clusters, as opposed to simple MSA depth
> reduction, drives any observed conformational shift."

Result, verbatim:

> "These results indicate that **MSA-level manipulation alone, whether through evolutionary
> clustering or random subsampling, is largely insufficient to overcome the systematic
> conformational bias** observed across the deep learning tools evaluated in this study."

And the contrast on the same receptor (p.13):

> "When provided with the partners and ligands required for activation of β2AR (i.e., agonist
> and G protein), **all predictions clustered tightly toward the active conformation**"
>
> "For β2AR, providing the agonist together with the heterotrimeric G protein **shifted
> predictions toward the expected active conformation across predictors**"

The β2AR subsampling evidence is drawn: **Fig 5A-B,D (p16)** plots AF-Cluster vs U10 vs U100 on
paired-reference RMSD axes for PfMATE, LAO **and β2AR**. References are 9CHU (inactive) /
8GEG (active).

**Two caveats you must carry, because a referee will.**

1. **It is not a clean within-model comparison.** The note records
   `input_factor_design: NOT CROSSED, and the two legs live in different models` — the
   AF-Cluster/U10/U100 arm runs on **AlphaFold2**, while the co-input arms run on
   AF3/Boltz-2/Chai-1/BioEmu. Same structural defect as `xing2025purified`. So "subsampling
   fails and partners work" is confounded with "AF2 fails and AF3-lineage works".
2. **One backbone reaches both states on apo β2AR with no manipulation at all**:
   *"Chai-1 identifies clusters within both conformations without any constraints"* (p.10) —
   Chai-1 on **apo** β2AR sampled two states. That is not subsampling, but it means apo
   bistability is observable on at least one backbone, and it connects directly to the
   per-backbone apo floor (Chai-1 calls 100% of apo β2AR samples active; Boltz-2 0%).

## 3. Depths actually used, and the shape of the response

**Absolute values, as stated:**

| paper | depth / rate |
|---|---|
| `ye2026multistatebias` | **U10, U100** — uniform random depth 10 and 100 |
| `waymentsteele2024cluster` | \|MSA\| = **10 and 100**, 500 samples each; plus closest-N-by-edit-distance |
| `schafer2025confounds` | CF-random **max-seq = 1** (KaiB), **8** (Mad2) |
| `suzuki2026conforflux` | CF-random depths **{2, 4, 8, 16, 32, 64, 128}** |
| `vo2026fiducials` | **16:32 to 256:512** (ColabFold cluster:extra notation), 50 seeds |
| `bryant2024cfold` | cluster sizes **[16, 32, 64, 128, 256, 512, 1024, 5120]** |
| `lee2025seqassoc` | default **512:5120**; 5 models × 5 seeds per depth |
| `jung2026boltzperturb` | masking rate **0.1**; depth reduced to **4,086 rows** |
| `kalakoti2025afsample2` | column masking swept **0/5/10/15/20/25/30/35/40/50%** |
| `kalakoti2026afsample3` | swept to **40% optimal for AF3** |
| `mitjavila2026afsample2t` | **0/10/20/30%** (and 50% in the sweep), 250 models per level |

**The shape — three independent statements, and they agree with your Block D finding that it
is not one mechanism:**

- **Non-monotone with an interior optimum.** `kalakoti2025afsample2`'s sweep "establishes a
  **non-monotonic optimum** and locates where the preferred state starts to break — *'Beyond
  30% masking, performance drops…'*".
- **Confirmed independently.** `mitjavila2026afsample2t`'s 10/20/30/50% sweep is recorded as
  "Dose–response; **rules out a monotonic 'more masking is better' reading — 50% collapses**".
- **Target-specific.** `kalakoti2026afsample3`: *"as observed in previous studies, the optimal
  level of MSA randomization is **protein specific**"*.
- **And there is a floor.** `li2026embedding`: *"all methods collapse at 0% MSA, signaling that
  evolutionary [information is required]"* — but **25% still works** (p26–27, 3 targets × 9 runs
  per depth).

**So the published shape is: flat-to-improving, an optimum somewhere in 15–40% masking that
moves by target, then collapse.** A monotone depth→state relationship is *not* what the
literature reports, and your two-mechanism Block D result is consistent with the field rather
than anomalous.

## 4. Does anyone cross MSA depth with a binding partner? **Exactly one paper, and it is GPCR**

**`mitjavila2026afsample2t`** — the only `factors-crossed` paper in the corpus, verbatim:

> "**For each masking probability, 250 structures were generated, with equal numbers of active
> and inactive receptors**"

So: masking level (0/10/20/30%) × partner presence (active/inactive receptor input),
**balanced at 250 models per cell**, 2,000 models per receptor. Its note records
`crossings: MSA x partner CROSSED and balanced`.

**But it does not answer our question**, for two reasons: the readout is **binding-site RMSD**,
not activation state; and the "partner presence" axis is the *input* state of the receptor
construct rather than a supplied partner chain whose effect is being measured. **The crossing
exists; the state result does not.** Everything else in the corpus holds one of the two fixed —
`chiesa` HELD, `zhang` HELD, `ye` CONFOUNDED and split across models, `vo` crosses none.

## 5. Seeds versus subsampling draws — the resampling unit

**Nobody states a resampling unit as a design principle.** What they do state is the count, and
the practice splits three ways:

- **Draw treated as a sample, pooled**: `waymentsteele2024cluster` — 500 samples each at
  depth 10 and 100. `ye2026multistatebias` — 50 predictions per condition. `bryant2024cfold` —
  *"We take 13 samples per clustering threshold, resulting in 104 predictions per target"*.
- **Draw crossed with seed**: `lee2025seqassoc` — *"5 models × 5 seeds per depth"*, i.e. the
  seed is a second axis nested inside depth. `vo2026fiducials` — 50 seeds per depth setting.
- **Draw treated as the model**: `mitjavila2026afsample2t` — 250 models per masking level, then
  **pooled across levels** into one ensemble, and the paper's own ensemble-size analysis
  (10/100/250/500/1,000) finds 100–250 suffices.

**The one paper that separates the contributions is `stein2022speachaf`**, and it is the most
useful for your design question: it runs **random-seed variation alone (3 seeds per MSA) as a
distinct arm**, and its note records that "**the paper concedes seeds alone reach some
alternate states**" (p8, p13). **So seeds and subsampling draws are not cleanly separable
sources of diversity, and at least one paper has measured that overlap.** If you want the
resampling unit settled, that is the precedent to follow: run a seeds-only arm at fixed depth.

## 6. Negative results and noise warnings — the strongest material here

**There is a live published dispute, and it is exactly about whether shallow-MSA diversity is
signal or artefact.**

**`schafer2025confounds`** rebuts AF-Cluster. Verbatim:

> p1: "However, their Paper **lacks some essential controls** needed to assess AF-cluster's
> reliability."
> p1: "Further, we observe that **AF-cluster mistakes some single-folding KaiB homologs for fold
> switchers, a critical flaw bound to mislead users**."
> p5: "However, **neither CF-random nor AF-cluster predicts fold switching reliably**, especially
> in more difficult cases."
> p5: "In short, AF2 is an outstanding tool for generating three-dimensional models of protein
> structure, but **its current ability to accurately predict alternative conformations is
> limited**."

Its central finding is that **plain random shallow MSA sampling matches or beats AF-Cluster** at
1–2 runs instead of 95–329, that AF-Cluster's proposed coupling-deconvolution mechanism is
**not supported by contact analysis**, and that it **calls experimentally confirmed single
folders metamorphic with high confidence**. That last is your noise-not-signal warning, stated
by a published rebuttal: *a method that produces a second state for a protein that does not have
one.*

**`waymentsteele2025reply`** answers with a control worth copying: **column shuffling destroys
the state-specific predictions**, so "local coevolution, not MSA depth alone, carries the
signal". **A shuffled-column arm is the cheapest available test of whether an observed shift is
information or noise**, and it is the direct analogue of our scrambled-partner arm.

**Other negative results:**

- **`jung2026boltzperturb`** — masking and depth reduction both made Boltz-2 **worse than
  vanilla** (SR_O 10.53% and 12.28%). Recorded in `lit/CLAUDE.md` as reading like a settled
  negative until you notice the ligand is never removed.
- **`xing2025purified`** p.3 — *"the successful sampling of alternative states depends **not on
  MSA depth but on sequence purity**"*. Depth is the wrong knob, on their evidence.
- **`lee2026foldswitch`** — *"None of the RfaH clusters produced conformations consistent…"*
- **`richman2025conformix`** and **`suzuki2026pairscaling`** both run subsampling as an
  **ablation to be beaten**: "CF-random-Boltz | that random shallow-MSA subsampling already
  achieves it" and "MSA subsampling | that depth reduction already achieves it". Two independent
  method papers treat "shallow MSA already does this" as the null they must exclude.
- **`ye2026multistatebias`** — §2 above.

---

## What the corpus does not cover

- **No paper reports getting active-state GPCRs out of shallow-MSA sampling with no
  transducer.** The nearest attempt (`ye2026multistatebias`) reports the opposite, on β2AR.
- **No paper crosses MSA depth with a supplied partner chain and reads out receptor state.**
  The one crossing that exists (`mitjavila2026afsample2t`) reads out binding-site RMSD.
- **No paper states a resampling unit for subsampled MSAs as a design principle** — only counts.
- **No subsampling depth is reported in Neff units.** Every *manipulated* depth in §3 is a
  sequence count, a cluster:extra pair, or a masking percentage. **CORRECTED 2026-09-12:** an
  earlier version of this line said "no Neff values anywhere", which is wrong. Neff appears in
  **two** papers, both descriptively and neither as a manipulation — `abramson2024af3` Extended
  Data Fig 7A, p18 ("median per-residue Neff", 10⁰–10⁴ log axis; the note flags it as plotting
  accuracy against *natural* Neff, "not interventional") and `suzuki2026pairscaling` Fig 7, p10
  ("MSA depth and Neff for every target"). See `MSA_SUBSAMPLING_REGIMES_ANSWERS.md` §4.
