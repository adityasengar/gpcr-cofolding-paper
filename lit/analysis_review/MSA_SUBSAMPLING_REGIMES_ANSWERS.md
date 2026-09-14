# MSA subsampling regimes — six retrieval questions

lit-3d, 2026-09-12, for paper-6f's MSA_SUBSAMPLING_REGIMES.md agent. Retrieval only.
Corpus 83 notes / 83 INDEX / 87 bib; staleness clean (zero unextracted PDFs).

**Contains a correction to something I told paper-6f yesterday — see Q4.**

---

## 1. COMPLEX vs MONOMER, and the PAIRED MSA

**Somebody does subsample a complex. Nobody says anything about the paired MSA.**

**The one paper that masks an MSA with partner chains present is `mitjavila2026afsample2t`.**
It runs AF2 / AF2-Multimer on class A GPCRs and its state axis *is* partner presence — the
note records that the method "can be pointed at a state, but not by the masking — **only by
including or omitting the Gα/Gβ/Gγ sequences**" (p.2, p.7, p.8). Masking is applied to
**columns within a sequence window covering the orthosteric pocket and part of EL2**, i.e.
the receptor's own alignment.

**On the paired MSA specifically: absent from corpus.** The string "paired" appears **once**
in that note and never in connection with the manipulation. Corpus-wide, only **5 of 83**
notes mention paired/unpaired MSAs at all — `feldman2026alphainterp`, `gilson2025casp16`,
`ku2026promise`, `skrinjar2026generalization`, `wohlwend2024boltz1` — and in four of those it
is pipeline description, not manipulation (e.g. `skrinjar2026generalization`: "standard
AlphaFold3 MSA generation pipeline was run to obtain the non paired and paired MSAs";
`gilson2025casp16`: "For unpaired sequences, pairing keys were set to −1").

**The single exception, and it is not what it looks like.** `feldman2026alphainterp` states
(p35): *"**All paired MSAs are replaced with the query sequence**, and all predictions are
computed with identical hyperparameters and random seeds to the control."* **But that paper's
systems are 400 monomers, SABmark and 46 fold-switch pairs — no complexes.** The sentence is
AF3 input-schema housekeeping (AF3's JSON carries `pairedMsa` and `unpairedMsa` fields even
for a monomer; its no-MSA arm "both `pairedMsa` and `unpairedMsa` explicitly omitted", p31).
**Do not cite it as a complex paired-MSA manipulation.**

**So the negative you wanted is available and it is clean: no paper in 83 subsamples,
masks, deletes or otherwise manipulates the PAIRED MSA of a complex as an experimental
variable. Nobody even reports what they did with it.**

## 2. LIGAND PRESENT

**Subsampling with a ligand present: YES, one paper. Crossing depth with ligand occupancy:
absent from corpus, and the corpus says so in its own words.**

`jung2026boltzperturb` — recorded `crossings:` **MSA × ligand HELD**: *"Because the ligand is
never varied, the MSA-degradation result (**SR_O 10.53% masked, 12.28% subsampled, both below
vanilla**, p.7) measures what MSA perturbation does *in the presence of* a ligand, not whether
the ligand and the alignment carry redundant information. It reads as a settled negative and
is not one."*

The opposite leg exists and also fails to cross. `lazou2026cryptic` — **MSA × ligand HELD
(ligand varied, MSA fixed)** — and its note states the gap directly:
*"`jung2026boltzperturb` is the opposite (MSA varied, ligand fixed). **Neither crosses them,
so the interaction between alignment depth and ligand occupancy is unmeasured on AF3-lineage
models from both directions.**"*

`xing2025purified` looks like a crossing and is not: *"AF2 predictions of the protein alone
were performed using the purified sequences", then "These purified sequences … were then used
for AF3 predictions, where the customized input MSA was provided along with the SMILES of the
ligand"* (p.5) — **protein-alone is AF2, ligand is AF3.**

Note also `mitjavila2026afsample2t` supplies **no ligand at all**: "No ligand is ever supplied
to AF2 — all models are generated apo. Ligands drive *model selection* (p.8), not model
generation."

## 3. `ye2026multistatebias` — CONFIRMED

**Your information is correct.** Verbatim, p.15:

> "To provide a baseline comparison using an **AlphaFold2-based** MSA manipulation approach
> distinct from the newer architectures evaluated above, we applied AF-Cluster to all four
> target proteins"

and the note's `crossings:` line: *"the MSA-manipulation arm runs on **AlphaFold2** while the
co-input arms run on **AF3/Boltz-2/Chai-1**, so the two axes never meet inside one model."*

**Exact protocol of the subsampling leg:**

| item | value |
|---|---|
| model | **AlphaFold2** (as the engine inside AF-Cluster; p.15, p.18) |
| methods | **AF-Cluster** (DBSCAN sub-MSAs by sequence similarity) + **U10** and **U100** (uniform random sub-MSAs of depth 10 and 100) |
| design quote | p.15: *"As controls, we also generated uniformly random sub-MSAs of depth 10 (U10) and 100 (U100) to test whether evolutionary structure in the clusters, as opposed to simple MSA depth reduction, drives any observed conformational shift."* |
| targets | **all four** — PfMATE, LAO, SecA, **β2AR** |
| samples/seeds per strategy | **NOT REPORTED.** The note records "per-strategy counts not stated except the SecA cluster count" |
| only stated count | SecA yielded *"only four DBSCAN clusters of size four to five sequences each"* — the baseline was underpowered there by MSA composition |
| readout | paired-reference RMSD scatter, **Fig 5A-B,D p16**, for PfMATE, LAO and β2AR |
| verdict | *"MSA-level manipulation alone, whether through evolutionary clustering or random subsampling, is largely insufficient to overcome the systematic conformational bias"* |

## 4. DEPTH UNIT — and a CORRECTION

**Correction first: I told paper-6f yesterday that no Neff figure appears anywhere in the
corpus. That was wrong. Neff appears in two papers.**

- **`abramson2024af3`**, Extended Data Fig 7A, **p18**: "Single-chain LDDT against MSA depth
  (**median per-residue Neff**), AF3 vs AF-M 2.3", x-axis "median per-residue Neff for the
  chain, **10⁰–10⁴**, log axis". **But the note flags it as observational**: "7a plots accuracy
  against **natural** Neff … **not interventional**".
- **`suzuki2026pairscaling`**, Fig 7, **p10**: "MSA depth **and Neff** for every target in the
  three datasets", bar chart, two overlaid series, for OC23 / TP16 / MS15.

**The refined claim, which is the one that survives: no paper in the corpus reports a
*subsampling depth* in Neff units. Neff appears only as a descriptive property of natural
alignments, never as a manipulated variable.** That is still the point you want, but it must
be stated that way.

**Units actually used for manipulated depth:**

| unit | papers |
|---|---|
| **raw row count** | `ye2026multistatebias` (U10, U100); `waymentsteele2024cluster` (\|MSA\| = 10, 100); `suzuki2026conforflux` (CF-random {2,4,8,16,32,64,128}); `feldman2026alphainterp` (depths {1,5,10} and {1,10,20,50,100}); `jung2026boltzperturb` (4,086 rows) |
| **ColabFold `max_seq` / `max_seq:max_extra_seq`** | `schafer2025confounds` (max-seq = 1, 8); `vo2026fiducials` (16:32 → 256:512); `lee2025seqassoc` (512:5120 default) |
| **cluster size** | `bryant2024cfold` ([16,32,64,128,256,512,1024,5120]) |
| **masking percentage** | `kalakoti2025afsample2`, `kalakoti2026afsample3`, `mitjavila2026afsample2t`, `jung2026boltzperturb` (rate 0.1), `feldman2026alphainterp` (shuffle rates 10–99%) |
| **fraction of full MSA** | `li2026embedding` (100/75/50/25/0%) |
| **Neff** | **nobody, as a manipulation** — see above |

## 5. NON-MONOTONE SHAPE — all four report a turning point

**Yes: three of the four report an interior optimum explicitly, and the fourth reports a
floor. None reports a monotone trend.**

**`kalakoti2025afsample2` (AF2, column masking).**
Levels swept: **0, 5, 10, 15, 20, 25, 30, 35, 40, 50 %** — ten levels; **45% is absent from
every axis** (Fig 2a, 2b, 2c, p4). Operating point chosen: 15%.
**Turning point, verbatim:** *"**Beyond 30% masking, performance drops** first for the open
conformations and subsequently for the closed conformations."*
**Target-dependent, verbatim and explicit:** *"20% masking generates the best model for
P40131, while 5% masking is optimal for P71147"* (p3); *"for real applications, the amount of
masking should be sampled for optimal performance"* (p3); *"while a lower masking fraction is
sometimes optimal, a higher fraction may be required in other situations"* (p6). Fig 2B is a
target × level heatmap whose stated purpose is "that the optimum is target-specific and that
15% is a compromise".
**Two things worth carrying**: confidence decays *monotonically* even while accuracy does not —
*"a 2% drop in confidence for every 5 percentage points of masking, followed by a rapid drop
beyond 35% masking"* (p3; ≈89 at 0% → ≈63 at 50%); and *"**model confidences from different
MSA masking levels are not directly comparable**"* (p6), which is why the sweep cannot be
resolved reference-free.

**`kalakoti2026afsample3` (AF3, same operation).**
Design: 24 settings = 2 networks × 6 masking levels × 2 subsampling states (Table 1, p2).
**Optima: AF3 40%, AF2 20%** (p4, Table S1 p13). **Turning point is network-dependent:**
"Full 0–50% masking sweep, both networks | Rules out that 40% is arbitrary; **shows AF2
degrades past 20% while AF3 does not** (Fig 3a,b)" (p4). Confidence at 50% masking: **AF3 >80,
AF2 ~58** (Fig 3c).
**Target-dependent, verbatim:** *"as observed in previous studies, **the optimal level of MSA
randomization is protein specific**"* (p4).
**Also relevant to your regime choice:** *"While AFsample3 still performs better overall with
49 better targets, **employing subsampling along with MSA masking was the optimal strategy for
a sizable number of targets**"* — masking and subsampling are not substitutes.

**`mitjavila2026afsample2t` (AF2, *targeted* masking).**
Levels: **0, 10, 20, 30%** in the deployed ensemble, **50% in the sweep**, applied **only
within the binding-site window**; the comparison arm AFsample2 applies **15% to the full MSA**.
**Turning point, recorded:** "Masking-probability sweep 10/20/30/50% | Dose–response; **rules
out a monotonic 'more masking is better' reading — 50% collapses**".
**The chosen regime is a pooled mixture, not a single level:** *"we combined sets of models
generated at different masking levels, which we refer to as the AFsample2T ensemble"*; "A
combination of **250 models each from masking levels of 0%, 10%, 20%, and 30%** resulted in the
highest structural accuracy (AUC …)". Contribution to the top-1% enriching models, Fig 5C p5:
**0% → 16%, 10% → 14%, 20% → 26%, 30% → 44%** — higher masking contributes disproportionately
but the unmasked arm still supplies 16%.

**`li2026embedding` (fraction of full MSA).**
Levels: **100%, 75%, 50%, 25%, 0%** (axis drawn descending), 3 targets × 9 runs per depth.
**Floor, verbatim (p27, Fig 11 caption):** *"**all methods collapse at 0% MSA**, signaling that
evolutionary [signal rather than structural memory]…"*; **25% still works** — "Both steering
methods beat the prior from 25% to 100% MSA; all three collapse at 0%".
**Caveat the note flags:** "**n = 3 at the two endpoint depths vs 9 elsewhere, so the collapse
point is the least-sampled point on every curve**."

## 6. CROSS-CHAIN EFFECT — absent from corpus

**Zero papers.** A sweep of all 83 notes for cross-chain MSA language ("one chain", "per-chain",
"other chain", "MSA of the partner/second/other chain", "chain-specific MSA" in proximity to
MSA/alignment) returns **0 hits**.

**Nothing in the corpus reports whether perturbing one chain's MSA in a complex affects the
other chain's predicted structure or the interface.** Given §1, this follows: essentially
nobody subsamples complexes, so nobody has measured the cross-chain consequence.

## Bonus — single-sequence (depth 1) for one chain only

**Depth 1 exists, but never for one chain of a complex.**

- `feldman2026alphainterp` uses **depth 1** twice — phylogenetic tiering at depths **{1, 5, 10}**
  and fake-MSA injection at depths **{1, 10, 20, 50, 100}** (p36–37) — but on **monomers**.
- `schafer2025confounds` uses ColabFold **max-seq = 1** for KaiB — again a monomer.
- `feldman2026alphainterp`'s "All paired MSAs are replaced with the query sequence" (p35) is
  formally a depth-1 paired channel, but on monomeric inputs, so it is not the one-chain-of-a-
  complex case.

**One-chain-only single-sequence in a complex: absent from corpus.**

---

## Summary of negatives, for direct use

1. **No paper manipulates the paired MSA of a complex.** Only 5 of 83 mention paired MSAs; four are pipeline description; the fifth is monomers.
2. **No paper crosses MSA depth with ligand occupancy** — and the corpus states this itself (`lazou2026cryptic` note).
3. **No paper reports a subsampling depth in Neff units** (Neff appears twice, both descriptive).
4. **No paper reports a cross-chain MSA effect.**
5. **No paper reduces one chain of a complex to single-sequence.**
