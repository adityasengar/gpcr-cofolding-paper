# Ligand modality — six corpus questions

lit-3d, 2026-09-12, for paper-6f. **Staleness check run first: zero PDFs without an
extraction.** Corpus 83 notes / 83 INDEX / 87 bib. Nothing unextracted bears on these.

Page offsets that apply below: `yang2025statespecific` **+11424** (its p1 = printed
11425); `abramson2024af3` **+492**. Others are printed pages already.

**The headline is Q3: the entanglement you are worried about is real, it is published as a
design principle, and there is a second boundary at 16 residues that nobody has connected
to it.**

---

## 1. Ligand class × partner presence — still zero at 83, and the denominator is now 8

`factors-crossed` still fires on **exactly one paper**, `mitjavila2026afsample2t`, and it
crosses MSA masking × partner presence with **no ligand channel at all**.

Papers carrying **both** `ligand-driven` and `partner-driven`: **8 of 83** (was 7 of 81;
`eddy2018extrinsictrp` joined). Every one, and why it misses:

| paper | why it is not a crossing |
|---|---|
| `chiesa2025templatebias` | recorded `partner × ligand HELD` — the ligand is present in every arm and never removed |
| `ye2026multistatebias` | recorded `partner × ligand CONFOUNDED` — β2AR gets agonist AND Gαβγ together, no agonist-free partner condition (p.18) |
| `vo2026fiducials` | its own note: "Despite carrying `msa-subsample`, `ligand-driven` and `partner-driven` together, this paper **crosses none of them**" |
| `ku2026promise` | ligand-induced and protein-induced are **separate, non-overlapping sets** with different success criteria — parallel arms, not a crossing |
| `eddy2018extrinsictrp` | **the closest partner-alone contrast in the corpus, and it is wet-lab.** Peptide added to an *existing* agonist complex, so ligand is held and partner is the only change — but one receptor, solution NMR, no predictor, and the peptide is never added to the antagonist complex. Recorded `ligand × partner NOT CROSSED` |
| `georgiou2025heterogeneity` | narrative review, no computation |
| `hilger2020gcgr` | experimental structural biology + biophysics |
| `tejero2024opsin` | cryo-EM + functional assay, `oracle: NOT APPLICABLE, no prediction pipeline` |

Also recorded: `zhang2026generalization` `partner × ligand HELD`, `mazzoni2000gsctpeptide`
`partner × ligand HELD`. **The claim holds and is now better bounded: of the 8 papers that
could hold the crossing, 4 are not prediction papers and the other 4 have explicit
recorded verdicts.**

## 2. Does any benchmark stratify by ligand MODALITY? — Yes, two do, and both report a gap

**`chitsazi2025gpcrdock4`** is the clearest. Its INDEX claim: *"In a genuinely blind
GPCR-ligand assessment, **AF2-Multimer peptide co-folding drove all successes; small-molecule
poses still lag 2010 results**."* The targets are split by modality — "five 2021 targets were
complexes with small molecules; three were with peptides" (p-level in note). Its head-to-head
verdict for peptides (Fig 5C, p11): docking to homology model / apo AF2 model / experimental
structure all "well below 1%"; co-folding with AF-Multimer is "the real improvement" for
NPY1R and NMUR2 — best peptide-complex models NMUR2 **3.91%**, NPY1R **1.32%** correctness —
**but it failed for OPRK**. And p-level: *"challenges for shorter peptides and small molecules
remained, and induced fit was…"*.

**`junker2026peptidedesign`** stratifies by ligand *size*, which is modality by proxy:
**peptide-ligand vs protein-ligand at ≤50 vs >50 residues**, and the gap is large —
*"100% of AF2IG-predicted, 82.1% of RF3-predicted and 35.5% of Boltz-2-predicted GPCR-**protein**
ligand complexes achieve a DockQ score below 0.23"* (p5, S2 Fig). Its benchmark spans
**peptide lengths 3–137 aa** across 113 GPCR complexes. **Receptor state is never assessed**,
so it stratifies the *docking* problem by modality, not the *state* problem.

**`ku2026promise`** separates **ligand-induced** and **protein-induced** sets and scores them
with different criteria (ligand RMSD ≤ 2 Å vs pair-level, p3) — a modality split by
construction, though the two sets are different systems so the comparison is between-set.

**Nobody stratifies a conformational-state result by ligand modality.** That is the gap.

## 3. Does a peptide ligand change the prediction problem? — YES, and it is published as a *design principle*

**This is the crux and it is not unremarked. `yang2025statespecific` builds a pipeline on
exactly the entanglement you fear**, verbatim (p1 = printed **11425**):

> "**This framework enables the tailored design of agonists or antagonists based on the
> active or inactive conformational states of GPCR structures.**"

Its Filter 2 is *"pAE_inactive < pAE_active or pLDDT_inactive > pLDDT_active"* (p6), and
*"All candidate peptides… are paired with **state-specific GPCR targets** and undergo
structural prediction"* (p12). **The peptide's pharmacological class is assigned by which
receptor state it is folded against.** For peptide ligands in a co-folding model, ligand class
and receptor state are not independent variables — one published pipeline *defines* the first
by the second. **Your 2×2 cannot treat "peptide agonist" as a clean factor level.**

**And there is a second boundary nobody has connected to it.** `abramson2024af3`, Methods
(p10 PDF = printed **p.502**), defines the peptide/protein line:

> "Individual polymer chains in evaluation complexes are filtered out if the maximum sequence
> identity to chains in the training set is greater than 40%… **Individual peptide chains
> (protein chains with less than 16 residues) are always filtered out.**"

Two consequences. **(i) AF3's own taxonomy puts the peptide/protein boundary at 16 residues.**
**(ii) AF3's low-homology evaluation subset contains no peptide chains at all**, so its
published anti-memorization numbers say nothing about peptide-liganded complexes. If your six
candidate receptors have agonists below 16 residues, they sit in a regime AF3 never reports on.

**Two papers exclude peptide/protein ligands by construction rather than stratify them** —
`jung2026boltzperturb` selects *"test systems containing a single protein chain and a single
ligand"* (p321-level) and `bryant2024cfold` extracts *"the first protein chain in each PDB
file"* (p.7). So the field's common move is to **remove** the multi-chain case, not to model it.

**A note that bears on E1.1 rather than on this question.** The 16-residue AF3 boundary sits
almost exactly on `mazzoni2000gsctpeptide`'s wet-lab threshold (**≥17 residues active,
shorter not**). Our proposed rungs 11 and 15 fall below both; 17, 19, 21 above both.
**A length effect observed between 15 and 17 is confounded between a biophysical threshold
and a modelling-taxonomy boundary**, and neither the ladder nor the literature can separate
them as currently designed. Worth recording before the rungs are frozen.

## 4. Allosteric contamination — nobody folds PAM/NAM into agonist/antagonist, and nobody warns against it

**PAM** appears in **2 of 83** notes (`georgiou2025heterogeneity`, `vo2026fiducials`); **NAM**
in **4 of 83**. Neither `khaleq2026hyaline` (the only explicit label rule in the corpus), nor
`chib2025gpcrstates`, nor `lee2026confornets` mentions allosteric modulators in a selection or
labelling rule.

**The most useful fact is an absence, and it is checkable.** khaleq's rule, verbatim (p12):

> "Active structures included: (1) G protein-coupled or G protein-mimetic nanobody-bound
> structures; (2) arrestin-coupled structures; (3) full agonist-bound structures with
> conformational criteria indicating activation. **Inactive structures included: (1) apo
> structures; (2) antagonist-bound structures; (3) inverse agonist-bound structures.**"

**A PAM- or NAM-bound structure falls into no class in that rule.** It is not mis-assigned —
there is no slot for it. So the corpus offers neither a precedent for folding them in nor a
warning against it.

**The closest thing to a warning is taxonomic.** `georgiou2025heterogeneity`'s
directional-control inventory lists **allosteric modulators as a separate handle** from
orthosteric ligands graded by efficacy — "**Allosteric modulators** — PAM Cmpd-6FA (β2AR,
6N48), NAMs amiloride/HMA/Fg754 at the Na⁺ site, SBI-553 at NTS1R" — i.e. the review keeps
them apart from the agonist/antagonist axis rather than merging them. And it records that
**Na⁺-site NAMs act at a different site entirely**, alongside ions as their own handle class.

**Your 69 PAM / 36 NAM / 11 allosteric agonist / 7 allosteric antagonist / 8 Ago-PAM records
are therefore uncovered by any published rule we hold.** If they enter an agonist/antagonist
2×2 they do so on our authority alone, and that should be stated.

## 5. Relaxed set + covariate column — yes, and the best precedent shows the payoff

**`yu2026domainmotion` is the precedent, and it is a strong one.** It does not filter to
enzymes with a clean apo:holo balance. It keeps **all 82** and partitions them by the covariate:
**Group 1** = 19 with more apo than holo; **Group 2** = 25 with more holo than apo;
**Group 3** = 38 with "five or fewer structures, or exactly equal numbers" — the ambiguous,
low-data group it could most easily have dropped.

**And Group 3 is where the effect lives**: the trigger ligand raises the holo-like fraction by
11.9% and 9.1% in Groups 1 and 2, **rising to 17.5% in Group 3, where the memorised prior is
weak**, against a 40.3% between-group difference. **Filtering to the clean cases would have
removed the group that carries the paper's most interpretable result.** That is the argument
for Aditya's proposal, made by a PNAS paper on 82 systems.

Second precedent, different shape: **`chib2025gpcrstates`** takes GPCRdb's activity level
**0–100% as a continuous x-axis** (Fig 2a–d, p6) rather than binarising and filtering.
Third: **`skrinjar2026generalization`** reports every training-similarity stratum rather than
restricting to the hard one — 8–25% success in the least-similar bin against 81–89% in the
most-similar.

**The counter-practice exists too and should be named**: `jung2026boltzperturb` and
`bryant2024cfold` both filter up front to single-chain single-ligand systems. So the corpus
holds both designs; the stratify-and-report design is the one with the better worked example.

## 6. `yu2026domainmotion` on ligand size or modality — it says **nothing**, and that is decisive for your framing

Checked directly. The paper has **no size stratification, no modality stratification, and no
peptide or protein ligand anywhere.** Its systems are **82 enzymes from DynDom** — "No GPCR,
no receptor" — and the ligand enters as **SMILES**: "input is sequence + MSA (**+ ligand SMILES
in the ligand arms**)". Its nonbinder arm is a nonbinding **small molecule**.

**So yu tells you that within the small-molecule regime, ligand *specificity* barely matters —
and it tells you nothing at all about whether a peptide chain behaves the same way.** The two
enter an AF3-lineage model by different paths: a small molecule as atom-level tokens with no
alignment, a peptide as a polymer chain with its own MSA and pairing. **Yu's result does not
cross that boundary, and nothing in the corpus does.**

**Direct answer to your framing question**: the corpus cannot tell you whether peptide-vs-small-
molecule is a first- or second-order confound. It can tell you that (a) the two modalities are
handled by different machinery, (b) two benchmarks that stratify by modality both find large
gaps (§2), and (c) one paper builds a pipeline that makes peptide class and receptor state
mutually defining (§3). **On the corpus's evidence the presumption should be first-order until
measured, not second-order until contradicted.**

---

## What the corpus does not cover

- **No paper stratifies a conformational-state result by ligand modality.** §2's two
  stratifications are both on docking/pose accuracy.
- **No paper reports accuracy for peptide-liganded vs small-molecule-liganded *receptors* on a
  state predicate.** The numbers in §2 are pose/DockQ numbers.
- **No rule anywhere covers PAM/NAM structures** in an active/inactive classification.
- **Nothing tests whether a peptide agonist's chain-ness changes a partner-driven state result** —
  which is the specific thing your 2×2 would be exposed to.

---

# Addendum 2026-09-12 — the short-chain rule for all four backbones

Asked after the AF3 finding above: do Boltz-2, Chai-1, Protenix and OpenFold3 use the same
16-residue peptide boundary? **They do not. There are three different conventions and one
model with no published rule at all.**

| model | short-chain / peptide rule | where |
|---|---|---|
| **AF3** | **peptide = protein chain with <16 residues**; such chains are *"always filtered out"* of the **low-homology evaluation subset**. Confidence/accuracy numbers are computed *"with no homology filtering and **including peptides**"* | `abramson2024af3`, printed p.502 (filter) and p.497 (inclusion) |
| **Chai-1** | **a different boundary, at 9 residues, and the opposite treatment**: peptides are **kept**. *"Individual polymer chains were clustered at 40% sequence identity for proteins **more than 9 residues**, and **100% sequence identity for proteins with 9 or fewer residues**"*. Only *"Polymer-peptide interfaces where the **non-peptide** entity has 40% or greater sequence identity"* are removed | `chai2024chai1` §5.6, p11 |
| **Boltz-2** | **no peptide/protein taxonomy line.** Data curation applies *"the same filters as AlphaFold3 … filtering out chains with **fewer than 4 resolved residues**"*; affinity clustering at 90% identity | `passaro2025boltz2` |
| **Boltz-1** | **nothing found.** One occurrence of "peptide" in the whole PDF and it is a reference title | `wohlwend2024boltz1` |
| **Protenix v1** | **no own rule — inherits AF3's by reference.** Evaluates on the *"Low Homology Recent PDB Set"* and states *"we follow their procedure [4]"* (AF3). So the <16-residue removal applies transitively | `protenix2025` |
| **Protenix v2** | one 30% identity threshold in a very-low-homology setting citing BoltzGen; no peptide rule | `protenix2026v2` |
| **OpenFold3** | **no model paper exists in the corpus, and none found externally** (Europe PMC and arXiv searched 2026-09-12). Its rules live in the code release, not a publication. The nearest published item is a third-party evaluation, *"Systematic Evaluation of AlphaFold2 and OpenFold3 on Protein–Peptide Complexes"* (2026), not extracted | — |

**What this means for a length ladder run on four backbones.**

1. **The peptide/protein boundary is not a property of the field; it is a property of each
   model's benchmark.** AF3 says 16, Chai-1 says 9, Boltz-2 says 4 (for a different purpose),
   Protenix inherits AF3's, OpenFold3 is undocumented. A rung at 11 or 15 residues sits on a
   different side of the line depending on which backbone scores it.
2. **Only AF3 (and Protenix by inheritance) removes short chains from its generalization
   evidence.** Chai-1 keeps them and merely clusters them more strictly. So "we have no
   anti-memorization evidence for short chains" is true of AF3/Protenix and **not** of Chai-1.
3. **None of these is a training-time or architectural limit.** Every rule above is an
   evaluation-set construction rule. No paper in the corpus states a minimum chain length the
   model will accept as input.

**Method note, recorded because it cost three attempts.** Shell `grep` returned *no output at
all* — not "0" — on the extracted Chai-1 text, which read as "the rule is absent" when the
rule was present on p11. The extraction was fine; the shell was not. **Every count above was
produced in Python.** This is the silent-check failure mode again: a search that reports
nothing is indistinguishable from a search that found nothing, and the fix was to use a tool
that reports its denominator.
