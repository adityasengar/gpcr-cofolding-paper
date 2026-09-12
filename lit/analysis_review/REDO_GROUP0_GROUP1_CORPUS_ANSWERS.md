# Corpus answers — Group 0 (instrument) and Group 1 (ladder) system specification

lit-3d, 2026-09-11, for paper-6f. Five questions. Locators are **PDF pages** unless
marked printed; `georgiou2025heterogeneity` is offset **+3690** (`PAGE_CONVENTION.md`),
so its PDF p.10 is printed p.3700 — both are given below where it matters.

---

## 1. What do co-folding papers supply as the receptor chain?

**There is no single convention. There are three, they are all stated, and they disagree
by hundreds of residues.** Cite whichever you adopt; do not invent a fourth.

| convention | paper | what it says |
|---|---|---|
| **Full-length canonical UniProt, untrimmed** | `zhang2026generalization` p5 | inputs are the "full-length receptor sequence obtained from the UniProt database and the native ligand SMILES from ChEMBL". Boltz-2, 253 structures. No trimming anywhere. |
| **Cap the termini, keep everything between** | `miglionico2026atlas` p19 | "GPCR **N-termini were truncated to a maximum of 50 residues upstream of TM1**, and **C-termini to 100 residues downstream of helix H8**, to reduce terminal disorder." AF3 v3.0.1, **10,413 predictions** — the largest GPCR co-folding run in the corpus. |
| **Delete long segments to protect the interface** | `pandyszekeres2024gproteindb` p.3 | "To increase model accuracy and **avoid cross-chain clashes**, it was necessary to truncate or delete very long receptor segments in some GPCR classes." Concretely: class A **ICL3 retained at 14 residues**; class B2 truncated after the GPS site (18 receptors) or N-terminally (14 receptors). AF2-Multimer, 5,595 models. |

**Recommendation.** `miglionico2026atlas` is the one to follow. It is the largest run, it
is AF3-lineage, it states a numeric rule with a reason, and the rule is a **cap** rather
than a deletion — so it degrades gracefully on receptors with short termini and solves the
FSHR/LSHR problem without a special case. It also keeps the ECD, which matters (see below).

**Signal peptide: the corpus has no convention, and I will not invent one.** The string
appears in exactly **1 of 81 notes** and not in a construct context. The one thing the
corpus does say is indirect but real: `jedryszek2026probing` Table S1 p.17 probes 11
concepts across Boltz-1's trunk→diffusion boundary, and **signal peptide is the most
strongly discarded concept of all** — probe F1 **0.76 → 0.35, Δ −0.40**, against helix
0.90 → 0.90 (Δ 0.00), disorder Δ −0.16, amino-acid identity Δ −0.34. That is a
representation-probing result on one model, not a construct ablation, so treat it as weak
evidence that the choice matters little to the generated geometry — not as licence.

**Class B1 ECD — keep it, and here is the reason, which is better than a convention.**
`hilger2020gcgr` p.1, verbatim: *"Glucagon binding to GCGR induces conformational change
on the extracellular side of the receptor (ECD, TM1, TM2, TM6, and TM7) **without
inducing outward movement of TM6 on the intracellular side**."* And p.6: *"In family B
GPCRs, peptide binding results in conformational changes on the extracellular side that
leads to **an expansion rather than a contraction of the ligand binding cavity**, as seen
in family A receptors."* So for B1 the ECD is where the ligand-side change lives, and it
is **decoupled from the intracellular TM6 movement our predicate reads**. Deleting the ECD
would not change what the predicate sees, but it would destroy the only place a B1
ligand effect could show up — and Group 2 wants that contrast. Keep it.

**The glycoprotein-hormone LRR ectodomain (FSHR, LSHR) has no corpus precedent either
way.** Under the miglionico cap it is retained, because the LRR is N-terminal to TM1 by
far more than 50 residues — so the cap **does** cut it. Decide that case explicitly and
record it; it is the one place the rule you adopt has a large, silent consequence.

**One more construct fact, and it is a reference-set problem rather than an input one.**
`georgiou2025heterogeneity` pp.9, 16 records that **T4 lysozyme fused into ICL3 forces the
active TM6 conformation regardless of ligand efficacy** — verbatim: *"the effect of T4L
linked to IL3 of β2AR … is to cause the population of only active TM6 conformations
independent of the efficacy of bound ligands"* — and that the same fusion may create the
artefactual broken ionic lock in A2AR **3PWH**. `lee2026confornets` acts on this without
saying why: p15, *"Inactive structures were further post-processed to remove ICL3 and any
fusion proteins inserted, as well as helix 8."* **Audit our 64 receptors' references for
T4L/BRIL ICL3 fusions before the thresholds are fitted** — a fusion-construct "inactive"
reference with a forced-active TM6 poisons the cut from the small side of a 5.3:1 split.

*Scope note:* `lee2026confornets`'s 7TM trimming (p15: "each chain was trimmed to the 7TM
domain by global pairwise sequence alignment to the canonical sequence") sits in the note
under *reference-structure preprocessing*. I could not determine from the note whether it
also applies to model input. Do not cite it as an input convention without opening p15.
`chib2025gpcrstates` truncates to TM-only at **scoring** time, excluding "termini, ECD and
ICL3" (SI p22), while feeding untrimmed AFDB models — the two are different decisions and
the note keeps them apart.

---

## 2. Cognate Gα assignment — what authority do good papers cite?

**The two papers that model partners at scale both refuse to pick a cognate, and both say
why in a quotable sentence.** That is the corpus's answer, and it is the opposite of
"choose an authority".

- `pandyszekeres2024gproteindb` p.8, verbatim: *"We choose to model **all theoretical G
  protein–GPCR complexes**, as it is difficult to definitely rule out specific complexes
  that cannot form."* And p.5: *"Whereas not all complexes will occur biologically, it is
  difficult to definitely rule out unseen couplings as they depend on many factors e.g.
  ligand and tissue/cell type…"*
- `miglionico2026atlas` models **every human GPCR against all 13 Gα subunits** in the full
  heterotrimer — 10,413 predictions — and then uses coupling data as **labels to rank
  against**, never as a selection rule.

**The one paper that does pick, picks from the structure, not a database.**
`chiesa2025templatebias`'s benchmark is *"all experimental structures of class A GPCRs
bound to G-protein released after 01 Jan 2023"* (p6302) — so the Gα is whichever one is in
the deposited entry. Our own panel reconstruction confirms what that yields: **nine Gα
subtypes across its 145 structures, dominated by Gαi1 (77) with Gαs second (44)**
(`lit/panels/`). `zhang2026generalization` likewise co-folds "the cognate G-protein
sequence" on 201 paired complexes, and its benchmark is deposited complexes.

**Does anyone report the disagreement instead of picking one? Yes — `miglionico2026atlas`,
twice, and it is the precedent you want.** It runs an **independent IUPHAR/GtoPDB test
set** (316 couplings, 114 pos / 202 neg, 79 receptors "not present in the training set",
p5) and treats the TGFα-shedding dataset as *"largely removed from GproteinDb … can be
regarded as an additional validation set"* at **Spearman ρ = 0.514** (p15) — explicitly to
calibrate against assay-to-assay noise. It also runs **leave-one-G-protein-out** (whole
coupling group withheld; AUROC > 0.8 for GNAL, GNAS, GNA11, GNAQ, GNA14, GNAI1, GNAI2,
GNAO1, p6).

**Your 68% / 22% numbers, confirmed and extended** — all `pandyszekeres2024gproteindb` p.8,
Fig. 4C–D:

| quantity | value |
|---|---|
| primary Gα **family** agreement, 3 datasets | **54 of 79 (68%)** GPCR–transducer-family pairs |
| pairwise family agreement | 85% (GtoPdb vs GEMTA), 77% and 71% (each vs FreeGβγ-Nluc) |
| primary Gα **subtype** agreement | **24 of 108 (22%)**; 42 (39%) unique to each dataset |
| per-family three-dataset core agreement | Gs 64%, Gi/o 59%, Gq/11 46%, **G12/13 0%** |
| couplings absent **only** from GtoPdb | 26% (Gi/o), 42% (Gq/11), 39% (G12/13) of family couplings |

**Two consequences for the spec.** (i) **Do not use IUPHAR/GtoPDB alone** — it
systematically omits 26–42% of family couplings relative to the two biosensor datasets.
(ii) **For any G12/13-coupled receptor in the panel, no two datasets agree at all (0%
core).** Those receptors need the assignment taken from a deposited structure or flagged
as undetermined; a database pick there is a coin flip wearing a citation.

**Careful with one number in that paper.** Its headline Gq agreement — 94% couplings / 82%
non-couplings — is **fitted, not measured**: the log(Emax/EC50) ≥ 7.0 cutoff was chosen
*"based on the largest agreement with couplings and non-couplings determined by both the
Bouvier GEMTA and Martemyanov FreeGβγ-Nluc datasets"* (Methods p.2), and that same
agreement is then reported as a finding (p.6, Fig. 4A). Recorded as route-4 leakage in the
note. The 68% and 22% figures are **not** affected — they are cross-dataset counts, not
threshold-fitted.

---

## 3. Calibrating a state predicate outside the test set, and class imbalance

**Precedent for an out-of-test calibration population: partial. Nobody splits by
receptor.** The two GPCR-state instruments in the corpus both hold out by **date only**:

- `paajanen2026activation` — **1006 train / 345 held-out** (Supp. Tables, p.22). The model
  was frozen, then *"the GPCRdb query was rerun, adding new structures published during
  the training phase"* and the frozen index applied.
- `khaleq2026hyaline` — *"trained exclusively on structures deposited … before January
  2023 (n = 1,312) and evaluated on structures deposited between January 2023 and December
  2024 (n = 278)"* (p4).

**`khaleq2026hyaline`'s gap is precisely the property you are proposing to have**, and its
note is blunt about it: *"No sequence- or family-level holdout is applied to the temporal
test set, and no receptor-level holdout is reported anywhere."* Its 30% MMseqs2
sequence-identity clustering exists but only inside the CV protocol behind the ablation
table (p8, p13). So **a receptor-disjoint calibration population would be stronger than
anything in the corpus**, and the justification writes itself: cite khaleq's temporal-only
split as what is currently done and its own unreported receptor overlap as the reason to
go further.

**The threshold-fitting rule to cite is `paajanen2026activation`, and it dissolves your
imbalance problem rather than managing it.** The cut is not hand-picked and not fitted to
labels: it is the **decision boundary of a two-component 1-D Gaussian mixture fitted on
PC1, with the uncertainty from bootstrap resampling** — **G_CA = −1.72 ± 0.44**, the
threshold and its CI both reported (`state_metric`, p.4). The GMM is fitted **without
labels**; the labels enter only afterwards, to orient and validate.

**Why that is the right answer to 611 : 115.** A supervised threshold — Youden, F1,
balanced accuracy — forces you to declare a balancing rule, and whichever you declare you
will be asked why. An unsupervised density fit has no class prior to declare: the cut
lands where the distribution is bimodal, which is a property of the geometry rather than
of the sampling. State that in advance and the 5.3:1 stops being a degree of freedom.

**Two honest caveats.**

1. **Paajanen's own leakage is in the axis, not the cut.** PC1 is chosen from five
   candidate components *because it separates the labelled classes* — "only the first
   component distinguishes antagonist-bound vs. G protein and agonist-bound" (route 2/4 in
   the note). We can do better by **fixing the axes in advance** (TM6 and NPxxY are
   pre-specified by the biology, not selected for separation) and fitting only the cut.
   That turns their defect into our contribution.
2. **A 1-D GMM on a 5.3:1 population can still be dragged by the majority component.** The
   minority mode must be visible before you trust the boundary — report the fitted
   component weights and the bootstrap CI, and if the CI on the cut is wide, say so rather
   than reporting a point.

**The threat to a receptor-level split, which should be stated rather than discovered.**
`mattsson2026leakage` p1, verbatim: *"splitting by protein-sequence identity is
**inherently insufficient** to prevent data leakage due to 'target mirroring,' in which
homologous proteins with low overall sequence identity still exhibit highly correlated
binding profiles."* It is an affinity-benchmark result, but the mechanism transfers: two
class A receptors with low sequence identity can still share conformational behaviour. A
receptor-disjoint calibration set buys independence of *identity*, not of *behaviour*.
Say what it buys and what it does not.

**Also relevant: `khaleq2026hyaline` states our exact imbalance as a limitation and does
nothing about it** — *"The class imbalance toward active structures (72.7%) and the
predominance of Class A receptors (79.4%) may limit performance on underrepresented
categories"* — and its **decision threshold is never reported at all** (recoverable as 0.5
only by inference; the headline AuROC 0.995/0.991 is threshold-free). That is the standard
to beat, and it is low.

---

## 4. Partner length between 50 and 350 residues

**Nothing exists. No paper in 81 supplies a partial G protein of any length to a structure
predictor.** The corpus records the absence three times, independently, which is as strong
as this corpus gets:

- `ye2026multistatebias`: *"They never ran any PARTIAL G-protein construct. No isolated α5
  helix, no α5 C-terminal peptide, no mini-G protein, no nanobody, no Gα-only or Gs-peptide
  arm appears anywhere in the paper. The words 'nanobody', 'mini-G', 'α5' and 'alpha5' do
  not occur in the text"* (full-text search; `controls_run` also records "ABSENT — reduced
  or partial partner construct", p.18).
- `miglionico2026atlas`, stated so the absence is checkable: every prediction uses the
  **full heterotrimer** (a named Gα plus full-length GNB1 and GNG1, p19); *"No α5 helix, no
  α5 C-terminal peptide, no mini-G, no nanobody, no scFv, no G-protein mimetic appears in
  the input protocol (pp19–20) or in Table 1 (p21)."* Its three near-misses are all
  non-inputs — the mini-Gs in 8F76 is a deposited reference for a figure; the chimeric and
  ΔC Gαq are wet-lab reagents; the pLDDT<70 filter is post-prediction.
- `pandyszekeres2024gproteindb`: *"mini-G proteins and nanobodies appear only as
  annotation…"* — never as a model input.

So there is **no standard truncation to borrow from the prediction literature.** There is
one in structural biology, and the corpus's reference structures instantiate it.

**A warning that will otherwise cost you a rung.** *"Mini-G" means two different things in
this corpus, differing by an order of magnitude.*

- The engineered GTPase-domain construct, ~200–230 residues, as deposited in
  **6FUF** (bovine rhodopsin–mini-Go) and **5G53** (NECA–A2AR–mini-Gs)
  [`tejero2024opsin` p11 comparison set].
- A **21-residue peptide**. `georgiou2025heterogeneity`, PDF p.10 = **printed p.3700**,
  verbatim: *"a **mini-Gαs consisting of a 21-residue polypeptide from the Gαs carboxy
  terminus**"* — and the same review uses "mini-Gs" for 5G53's real construct two
  sentences earlier.

**If the spec says "a mini-G rung" it is ambiguous by a factor of ten. Express every rung
as "the last N residues of the cognate subunit" and give N** — which is already
E1.1's own specification warning (§0.3 item 4); it now has a documented instance.

**Recommendation for the 60 / 100 / 200 rungs.** Do not invent round numbers. Take them
from deposited complexes that exist, so every rung names a construct someone has
crystallised: the **mini-G** boundary (6FUF, 5G53, 8F76), and the **Gα-only, no βγ**
boundary that `pandyszekeres2024gproteindb` adopted for the whole interactome with a
stated reason — p.8, verbatim: *"We focused on the **Gα subunit**, as it has the vast
majority of receptor interactions, and it was not possible to compute high-quality models
including Gβ and Gγ for the complete interactome."* That sentence justifies an
"α5+β6+GTPase-domain, no βγ" rung better than any number we could pick.

**And one piece of evidence for the low end that changes the ladder's premise.** The
corpus's only verbatim support for a **21-residue** α5 peptide being functionally
sufficient is in the same passage, and it is on the axis we measure —
`georgiou2025heterogeneity`, printed **p.3700–3701**:

> "Importantly, when the mini-Gαs was added to the UK432097−A2AR complex, **one peak for
> W233^6.35 was observed in comparison to the two peaks** in the agonist UK432097−A2AR
> complex… While endogenous tryptophans at the **extracellular** surface did not exhibit
> any signal after the mini-Gαs peptide addition, the endogenous tryptophans at the
> **intracellular** surface showed an NMR signal."

W233^6.35 is the cytoplasmic end of TM6. A 21-residue Gαs C-terminal polypeptide collapses
two conformational populations to one **there and not extracellularly** — corroborated in
the same paragraph against X-ray, where NECA−A2AR−mini-Gαs (5G53) differs from binary
agonist−A2AR (2YDV) *"in the intracellular region but not in the extracellular region"*.
Attributed by the review to "Eddy and collaborators in 2021" (its ref 155), which is **not
in our corpus** — retrieve it before it carries a sentence.

**This is the first corpus evidence that 21 is a defensible number for the biology**, and
it bears on the title decision, which is Aditya's. It does not change what our arms
supplied.

---

## 5. `khaleq2026hyaline` circularity, and whether arrestin-active is geometrically separable

**The corpus has a clear view, and it is favourable to your instrument.**
`georgiou2025heterogeneity` p.15: **β-arrestin and GRK direct the receptor to *distinct,
non-Gs* active states, and β-arrestin-biased agonists act on TM7 rather than TM6.**

So arrestin-active and G-protein-active are **not** the same conformation, and they differ
**exactly along the split our two-axis predicate uses**: a G-protein-active receptor is
defined by the TM6 outward movement; an arrestin-biased one moves TM7/NPxxY. Three
consequences:

1. **It is an argument for keeping the two axes separate**, and the strongest one available
   — a single pooled predicate would merge two states the literature distinguishes.
2. **The contamination is directional and predictable.** If arrestin-complexed structures
   sit in our *active* reference class, they drag the **TM6** threshold **down** (they may
   not show the full outward movement) while leaving NPxxY roughly where it is. On a 5.3:1
   active-majority population, that is a loosening of the cut on the majority side — the
   direction that most flatters a partner-driven result. Worth checking before fitting,
   not after.
3. **So yes, audit our 64 receptors' active references for arrestin complexes** — you
   already have someone on it. The same pass should flag T4L/BRIL ICL3 fusions (§1).

**We do not inherit khaleq's rule unless our labels come from the same place.** Khaleq's
active class is defined by "(1) G protein-coupled or G protein-mimetic nanobody-bound
structures; (2) arrestin-coupled structures; (3) full agonist-bound structures with
conformational [changes]" — a rule that is *"itself partly pharmacological, not
geometric"* (note, p-level quote at note line 50). Khaleq also states its own limit
(p11): the model *"does not address the continuum of activation states or the distinction
between G protein-biased and arrestin-biased conformations."* If our references are
GPCRdb-annotated rather than khaleq-labelled, we inherit **GPCRdb's** rule, not theirs —
and `lit/CLAUDE.md` already warns that GPCRdb labels are circular for us. Either way the
audit is the same and the fix is the same: know which active references are
arrestin-complexed, and decide whether they calibrate the ruler.

**Cross-experiment consequence, repeating the one from the last round because it lands
here too.** `paajanen2026activation` **excluded arrestins** — *"Arrestins have not been
included in the analysis because there is not enough data to influence the graph"* (p.2) —
so E0.2's independent-index concordance cannot cover any arrestin-complexed reference or
any E7.6 arrestin arm.

**Useful comparator numbers from khaleq while we are here** (all p6): attention
fold-enrichment DRY **3.2×**, NPxxY **2.8×**, CWxP **2.4×**, all p < 0.001 on a
10,000-permutation test; and the correlation between learned attention weight and **TM6
outward displacement, r = 0.78, p < 0.001**. Its p2/p3 sentence is also a ready-made
argument for a two-instrument predicate: *"The DRY motif in TM3 and the NPxxY motif in TM7
are separated by approximately 15–20 Å, and their coordinated rearrangement upon
activation cannot be captured by local features alone."*

---

## What I could not answer from the corpus

- **Signal peptide in or out** — no convention exists (1 of 81 notes, wrong context).
- **The glycoprotein-hormone LRR ectodomain** — no paper in the corpus handles FSHR/LSHR
  construct preparation explicitly. The miglionico cap decides it by side effect; decide
  it deliberately instead.
- **Whether `lee2026confornets`'s 7TM trim is input-side or reference-side** — the note is
  ambiguous and p15 must be opened.
- **"Eddy and collaborators 2021"** (georgiou ref 155), the primary source for the 21-mer
  NMR result — not in the corpus.
