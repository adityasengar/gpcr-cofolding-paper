# georgiou2025heterogeneity

> **Reader's warning — this is a REVIEW, not a primary study.** It presents no new
> predictions, no new structures, no new simulations and no new experiments. Every
> number, structure and mechanism in it is attributed to a cited primary source.
> Most of section **C** is therefore `NOT APPLICABLE` **by design, not by sloppiness**:
> `states_generated`, `oracle_leakage` (all seven routes), `prospective`,
> `metric_saturation`, `directional_control`, `anti_memorization_design`,
> `anti_memorization_control`, `controls_run` and `confidence_as_discriminator` each
> carry one line of why. Do **not** read a benchmark result out of this note; there
> isn't one.
>
> **Its value to the corpus is two things:**
> 1. **The authoritative reference for what a Class A "active" / "inactive" /
>    "intermediate" state actually consists of.** Every structural criterion the
>    review reports — TM6 outward displacement and the exact distances, the DRY motif
>    and ionic lock, NPxxY, PIF, CWxP/toggle switch, the Na⁺ pocket, the YY-lock, the
>    "activating ionic lock", and the S1/S2/I1/I2/A nomenclature — is tabulated with
>    values and pages under **`state_metric`** in section C. That table is the single
>    most reusable thing in this note.
> 2. **A source of citable mechanistic sentences for the introduction** — in
>    particular that agonist binding alone is *not sufficient* to stabilise a fully
>    active state, and that the transducer is required. Those are in
>    **`necessity_claims`**, verbatim, with pages.
>
> **Page numbering.** All page references in this note are **PDF pages 1–38**. The
> journal paginates 3691–3728, so `journal page = PDF page + 3690` (PDF p.1 = 3691).
> The body ends on PDF p.27; pp.28–38 are the 311-item reference list.
>
> **Citation-accuracy warning.** The review's attributions are occasionally
> mismatched to its own reference list — verified examples in `unresolved`. Do not
> cite a primary result *through* this review without checking the primary source.

## A. Identity

- **citekey**: `georgiou2025heterogeneity`
- **doi**: 10.1021/acsptsci.5c00102 (p.1)
- **year**: **2025.** Received February 6, 2025; Revised September 18, 2025; Accepted September 29, 2025; Published October 7, 2025 (p.1).
- **venue**: *ACS Pharmacology & Translational Science* **2025, 8, 3691−3728**. Article type is explicitly **"Review"** (running head, every page). **Peer-reviewed journal article, not a preprint** (p.1).
- **title**: Conformational Heterogeneity Underlying Divergent Signaling in Class A G Protein-Coupled Receptors
- **authors**: **Kyriakos Georgiou and Antonios Kolocouris\*** (two authors only). Laboratory of Medicinal Chemistry, Section of Pharmaceutical Chemistry, Department of Pharmacy, School of Health Sciences, National and Kapodistrian University of Athens, 15771 Athens, Greece. Corresponding: A. Kolocouris, ankol@pharm.uoa.gr, ORCID 0000-0001-6110-1903 (p.27).
- **author contributions** (p.27, worth recording because it bears on figure provenance): *"A.K. wrote the manuscript. K.G. prepared the figures."* Funding: Chiesi Hellas (SARG/NKUA grant No. 10354); open-access fees by HEAL-Link. *"The authors declare no competing financial interest."*

## B. Scope

- **system**: **GPCR — class A specifically.** Class A only; classes B/B2/C/F are named once for taxonomy (p.2) and never revisited. One class B receptor (glucagon receptor, GCGR) appears twice as a deliberate contrast case (pp.3, 5).
- **n_targets**: **4 receptors reviewed in depth**, per the abstract (p.1): *"We review findings about the functional, conformational states of four class A GPCRs, including detailed results for the adenosine A2A and β2 adrenergic receptors and important observations for the β1 and μ opioid receptors."* Weighting is very uneven: **A2AR** (§4.1, pp.8–14, by far the deepest), **β2AR** (§4.2, pp.14–20), **β1AR** (§4.3, p.20, ~1 page), **μOR** (§4.4, pp.20–21, ~1.5 pages). A further ~15 receptors appear as supporting citations only: rhodopsin (RhoR), NTS1R, κOR, M2R, M3R, 5-HT1BR, A1R, A2BR, A3R, V2R, AT1R, α2AR, D2R, GHSR, GCGR.
  - **Generality claim on a narrow base — flag this.** The title and abstract generalise to "Class A G Protein-Coupled Receptors"; the detailed evidence is essentially two receptors (A2AR, β2AR). The authors themselves warn against over-generalising (p.7): *"The detailed activation mechanism by which the binding of the agonist at the extracellular region of the GPCR is transmitted allosterically at the intracellular region, which opens to bind a G protein, is likely to differ between different categories of class A GPCRs and even for distinct subtypes of the same family."*
- **method_class**: **other — narrative literature review (secondary source).** No new computation and no new experiment of any kind. There is no methods section, no protocol, no data availability statement, and no supplementary information. Nothing in the paper is a co-folding, MSA, template, MD, enhanced-sampling, clustering or benchmark protocol *run by these authors*; MD, GaMD, metadynamics, REST, AWH, coarse-grained MD and Monte Carlo all appear **only as results attributed to other groups**.
- **backbones**: **NOT APPLICABLE.** No structure-prediction backbone appears anywhere. AF2/AF3/Boltz/Chai/OpenFold/Protenix are never used and never discussed. The string "AlphaFold2" occurs exactly once in the whole PDF — inside the *title of reference 79* (GPCRdb in 2023: *"State-Specific Structure Models Using AlphaFold2 and New Ligand Resources"*, p.30) — and the review's body never mentions predicted models. **This is itself a useful fact: an authoritative 2025 Class A conformational review that engages with GPCRdb but not with structure prediction at all.**
- **templates**: **NOT APPLICABLE** in the prediction sense. All structural input is deposited experimental structure (X-ray, XFEL, cryo-EM), used as the *subject of discussion*, not as a modelling template.
- **msa_handling**: **NOT APPLICABLE.** No alignment is built or used. Sequence appears only as Ballesteros–Weinstein superscript numbering (p.3, ref 51) and GPCRdb generic numbering (e.g. F139^ICL2 = 34.51, p.7).

## C. Conformational core

> Section C is written against prediction papers. For a review the honest answer to
> most of it is NOT APPLICABLE. The two fields that *do* carry real content here are
> **`state_metric`** (which becomes the state-criteria reference table) and
> **`structural_priors_used`** (which becomes the evidence-base inventory).

- **states_generated**: **NOT APPLICABLE — a review; nothing is generated, predicted, sampled or measured by these authors.** What the review *asserts exists*, and what it is authoritative for, is a **multistate ensemble approaching a continuum**, explicitly against a two-state model (p.6):
  > *"Class A GPCRs can exist in three different conformational states (active, inactive, intermediate-active) that can be interconverted for the activation/inactivation process according to a multistate, rheostat-like model,14,137 instead of a binary (on/off) switch model."* (p.6)

  and, at the finer level it actually spends the paper on, **a five-state-per-helix nomenclature** (S1, S2, I1, I2, A along TM6; the parallel S1, S2, I1, I2, A along TM7), plus supernumerary states (Ix^TM6, I^TM7) that different techniques keep adding. The abstract's framing (p.1): *"GPCRs in their apo-forms exhibit conformational heterogeneity, and more than a single active and inactive conformation exists in equilibrium."*

- **structural_priors_used**: **The review's evidence base. This is the field that carries the answer to "what is this review built on".**

  **(i) Deposited structures — the census the review itself gives.**
  - p.4: *"Overall, as regards the static structures, there are now more cryo-EM structures (623 structures) than X-ray structures (477 structures), while most cryo-EM GPCR structures are available, due to the size requirements of the protein, in the fully activated conformation of the GPCR, according to data selected in the GPCRdb (GPCR database).78,79"* — **1,100 deposited GPCR structures total, with an explicit statement that the cryo-EM half is biased toward the fully activated conformation.** This sentence is the single most quotable line in the paper for a "the PDB is state-biased" argument.
  - p.3: *"A study of ∼230 structures of 45 class A GPCRs revealed a set of 34 amino acid residue pairs that contribute to the activation pathway.43"* (Zhou et al., eLife 2019).
  - p.5: **only two GPCR–GRK complexes exist** — *"while a few high-resolution structures of GPCR-arr complexes have been deposited, only two exist for GPCR-GRK complexes"* (7MT9 RhoR–GRK1; 8JPB/8JPC NTS1R–GRK2–Gαq).
  - p.6: *"An analysis of a large data set of MD simulations covering 60% of currently available GPCR structures by Selent and collaborators in 2025136"* (GPCRmd-type resource).
  - ~90 individual PDB IDs are cited by accession in the body. The core anchor set the state assignments hang on: **active/fully activated** — 3SN6, 4LDE, 3P0G, 6N48 (β2AR); 5G53, 6GDG (A2AR); 7JJO (β1AR); 5C1M/8E0G, 6DDE (μOR); 6CMO, 3CAP, 3DQB (RhoR); 6E67, 6EG8 (β2AR–GsGDP/mini-Gs); 9BUY (β2AR–Gi). **Intermediate active** — 2YDV, 2YDO (A2AR + agonist only); 3PDS (β2AR + covalent agonist FAUC50); 9EE8/9EE9/9EEA (R291^7.56A A2AR–mini-Gαsβγ). **Inactive** — 4EIY, 3EML, 3PWH (A2AR); 2RH1, 3NY8, 3NYA, 5D5B, 2R4S (β2AR); 2VT4, 2Y02/2Y03/2Y04 (β1AR); 4DKL (μOR); 1I19 (RhoR); 8RLN, 7ARO (A2AR + partial agonist, inactive-like).
  - **Databases**: GPCRdb (gpcrdb.org, refs 78, 79, 126) for the structure census and for generic residue numbering; IUPHAR/BPS Guide to Pharmacology (ref 73) for transducer-coupling summaries (pp.4, 6, 7).

  **(ii) Biophysical technique base — what the conformational-heterogeneity picture actually rests on.** The review's whole argument is that crystallography and cryo-EM *cannot see* the states that matter, and that a technique stack is required. Abstract (p.1): *"The characterization of such transient conformational states, which may have eluded identification by X-ray crystallography and cryogenic electron microscopy, can be achieved through a combination of biophysical techniques."* Techniques actually drawn on:
  - **Crystallography / XFEL / cryo-EM** (throughout; §3, pp.6–8)
  - **Solution NMR** — the dominant evidence: **¹⁹F** (Prosser, Ye, Wüthrich, Eddy, Kobilka groups; the S1/S2/I1/I2/A assignments come from here), **¹³C** ([¹³C,¹H] ε-N[¹³CH₃]-Lys and ¹³C-Met labelling, Kobilka and Shimada groups), **¹⁵N** ([¹⁵N,¹H] TROSY, Grzesiek, Eddy, Shimada), **²³Na**, **¹H** with trimethylsilyl (TMS/TMSF) reporters, **EXSY** and **STD** 2D experiments, **PRE** (paramagnetic relaxation enhancement), and **¹⁹F MAS solid-state NMR in liposomes** (Eddy 2025) (pp.8–21)
  - **DEER / electron–electron double resonance** (Hubbell, Kobilka, Elgeti) (pp.4, 16, 17, 21, 26)
  - **Single-molecule fluorescence: SMF/TIRF, smFRET, FCS with photoinduced electron transfer (PET)** (pp.9–14, 16–21)
  - **Ensemble fluorescence / bimane / monobromobimane quenching / AFM-based SMF** (pp.15, 16, 18)
  - **Mass spectrometry** — HDX-MS, HRF-MS (time-resolved), LiP-MS, nMS, MALDI-MS (§5, pp.21–23)
  - **Simulation** — conventional MD, **GaMD**, **metadynamics** (incl. minute-timescale, well-tempered, "biologically motivated" CVs), **REST** replica exchange, **AWH** accelerated weight histogram, coarse-grained MD, Monte Carlo (pp.9, 11–12, 16–18, 22–23)
  - **Cell/solution pharmacology** — BRET, BiFC, live-cell FRET with SPASM sensors, LRET, cAMP accumulation, GTP-hydrolysis and BODIPY-FL nucleotide-exchange assays, radioligand kinetics (pp.5–6, 11–12, 18, 20)
  - **Membrane mimetics matter and are tracked throughout**: DDM/CHS, DM/CHS, MNG-3/CHS, MNG-3, LMNG/CHS, LMNG micelles; POPC/POPG, POPC/POPS, POPC/POPS/POPE nanodiscs; DOPC/DOPS/DOPG; liposomes; LCP. The review explicitly warns the mimetic changes the answer (see `stated_limits`).

  **(iii) Design-time priors.** None in the methodological sense — there is no design. The *selection* prior is stated openly (p.24): the four receptors were chosen because they are the ones with a deep 19F-NMR/DEER/smFRET literature (*"only some GPCRs, including the A2AR and β2AR, have had their conformational states profiled by 19F NMR studies"*, p.25).

- **oracle_leakage**: **NOT APPLICABLE — there is no pipeline, no model, no prediction and no scored outcome, so there is nothing that knowledge of a deposited structure could leak into.** Enumerated per route as the schema requires, so the absence is checkable rather than assumed:
  1. *Structures used as input or template* — **NOT APPLICABLE.** Deposited structures are the review's subject matter, discussed as published results (§3, pp.6–8). Nothing is fed to anything.
  2. *State annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or alignments* — **NOT APPLICABLE, but note the database is used.** GPCRdb supplies the structure census and generic residue numbering (pp.4, 6, 7, refs 78/79/126). No template or alignment is driven by it, because there is neither.
  3. *Cluster labels derived from known states* — **NOT APPLICABLE.** No clustering is performed. The S1/S2/I1/I2/A labels are **NMR chemical-shift assignments taken from the primary literature**, and the review is transparent that mapping them onto PDB entries is *inference*, hedged throughout: *"it was suggested that A^TM6 conformation is similar to the fully activated conformation observed in the X-ray structure … (PDB ID 5G53)"* and *"conformation I2^TM6 might be like the intermediate-active conformation … (PDB ID 2YDV)"* (p.10, both with "suggested"/"might"). Recording that hedging matters: **these state↔PDB mappings are proposals, not measurements.**
  4. *Hyperparameters, sweeps, seeds or stopping criteria tuned against known states* — **NOT APPLICABLE.** Nothing is tuned; no free parameter exists.
  5. *Success defined post hoc by RMSD or TM to a structure they had* — **NOT APPLICABLE.** There is no success criterion. The one RMSD in the paper (RMSD(Cα) = 1.7 Å, 5G53 vs 3SN6, p.6) is a descriptive comparison of two deposited active-state structures, not a scoring of any prediction.
  6. *Best/worst model labels assigned against a held reference* — **NOT APPLICABLE.** No models exist to label.
  7. *Design-level oracle use — systems or conditions chosen because the expected answer is known* — **NOT APPLICABLE as a defect, but the analogous selection is disclosed.** The four receptors were selected precisely because their answers are already extensively characterised (p.24, p.25). For a review that is the correct selection rule, not a rigour failure. **Do not tag `design-level-oracle` for this** — the tag is for a pipeline that declared its expected state before reading a result, and there is no result being read.

- **prospective**: **NOT APPLICABLE — a review is retrospective by construction.** It makes no forward prediction that could later be checked. The closest thing to a forward statement is a research agenda (p.23, items (a)–(c)) and a call for work on Gβγ (p.11) and on GRK-coupled conformations (p.26); neither is a testable prediction with a stated expected outcome.

- **coinput_composition**: **New in v3.1. NOT APPLICABLE** — a review; it collates other groups' conditions rather than supplying any.

- **binding_order**: **New in v3.1. ADDRESSED, and it is the corpus's only source for the pre-coupled route.** The review records an activation intermediate that *is* the pre-coupled complex: I1^TM6 *"corresponds to the complex GPCR−G"*, more stable with GDP present than without, with pre-assembled β2AR-Gs^empty and β2AR-Gs^GDP both showing low-to-intermediate FRET consistent with I1^TM6 (Fig 4, **p.10**; β2AR **p.19**). The nucleotide state is what separates the routes: swapping G^GDP, G^empty and +GTP *"separates pre-coupled (I1) from nucleotide-free ternary (A); GDP removal shifts equilibrium to A^TM6/A^TM7"* (pp.11−12, 14). So a receptor and G protein can be associated *before* agonist, sitting in an intermediate, with agonist and nucleotide release driving the transition on. Tags `pre-coupled`. Read alongside `paajanen2026activation`, which argues the ligand-first route from deposited structures.

- **state_metric**: **NOT APPLICABLE as an *applied* metric — the review measures nothing.** But it **reports, collates and reconciles the criteria other people use**, and that is the reason to hold this note. Full table below. Two kinds of criterion are present and the review keeps them distinct: **structural predicates** (distances, angles, contacts, motif rotamers, read off deposited structures) and **spectroscopic predicates** (chemical-shift regions, FRET efficiency, DEER distance distributions, quenching), which are the only ones that can see the transient states.

  ### C.1 — Structural criteria for calling a Class A state (the reference table)

  | # | criterion | what it distinguishes | reported value / range | page |
  |---|---|---|---|---|
  | 1 | **TM6 outward swing, cytoplasmic end — the review's headline generic number** | inactive → active | **∼7−14 Å** — *"this allosteric network stabilizes an outward swing of TM6 by ∼7−14 Å, generating a cytoplasmic cavity for Gα protein binding, as demonstrated in crystallographic, biophysical, and biochemical studies"* | **p.24** |
  | 2 | **TM6 displacement measured as the Cα−Cα distance at Thr224^6.26** (the review's operational handle) | inactive → agonist+G-protein active, **per receptor** | **∼6 Å in rhodopsin; ∼14−18 Å in β2AR and A2AR** — *"a large outward shift of TM6, as the distance between the Cα atoms of Thr224^6.26 from the inactive to the active conformation has been measured in class A GPCRs bound to an agonist and a G protein, for example, ∼6 Å in RhoR, and ∼14−18 Å in β2AR, and A2AR"* | **p.7** |
  | 3 | **A2AR three-step ladder: inactive (3EML) → intermediate active (2YDV) → fully active (5G53)** | inactive vs intermediate vs full | **∼40° rotation of TM6 about F282^6.44**, **∼4 Å between the Cα atoms of Thr224^6.26** (inactive→intermediate), **plus an additional ∼14 Å** to fully active | **p.7** |
  | 4 | TM6 end accessibility / displacement, agonist-only vs mini-Gs-bound A2AR (LiP-MS cross-checked against structures) | intermediate active → fully active | *"residue T224^6.26 at the cytoplasmic TM6 end moves outward from the receptor core by ∼14 Å relative to the agonist-only bound A2AR structure"* | **p.22** |
  | 5 | **TM6 outward movement is transducer-dependent** | Gs/Gq-coupled vs Gi/o-coupled active states | Qualitative, **no number given**: *"the outward movement of TM6 is smaller compared to Gs and Gq/11 complexes because of the smaller size of the Gαi protein binding pocket"* (3SN6 vs 6DDE) | **p.7**, repeated **p.25** |
  | 6 | Same, for β2AR–Gi specifically | β2AR–Gs vs β2AR–Gi active | *"the outward movement of cytosolic TM6 is smaller compared with structures of agonist−β2AR−Gs complexes"* (9BUY, LM189−β2AR−Gi). **No number.** | **p.17** |
  | 7 | TM6 displacement on ionic-lock rupture by Gα-α5 insertion (metadynamics, Goddard 2023) | inactive → activated, in a simulation coordinate | *"when the ionic lock is broken, Gαs-α5 experiences a remarkable expansion in the β2AR cytoplasmic region, causing **TM6 to displace outward by ∼5 Å from TM3**"* | **p.18** |
  | 8 | **"Ionic lock" DR³·⁵⁰Y−E⁶·³⁰ (R3.50−E6.30 salt bridge)** | *nominally* inactive vs active — **but the review's key message is that it does NOT work as a state predicate** | Present in inactive rhodopsin (1I19) and inactive A2AR (3EML/4EIY); broken in active. **Absent from the inactive X-ray structures of β1AR, β2AR and μOR**, where instead *"residue R3.50 … forms a salt bridge with the adjacent D3.49 of the DRY sequence"*. Verdict: *"the DR3.50Y-E6.30 interaction **does not differentiate the inactive from the active conformational ensemble** since it occurs during the transition between two inactive states, which is required for the activation of these class A GPCRs"* | **p.3**, restated **p.7** |
  | 9 | **S1^TM6 vs S2^TM6 — two *inactive* states separated by the ionic lock** | inactive-with-lock vs inactive-without-lock | *"Conformations S1^TM6 and S2^TM6 were considered with a formed and broken 'ionic lock' interaction, respectively"*; *"There is no interaction between the GαβγGDP and GPCR in the inactive conformations S1^TM6, S2^TM6"* | **p.9**, Fig 4 caption **p.10** |
  | 10 | **Cation-π contacts as auxiliary inactive-state stabilisers (A2AR)** | inactive vs intermediate vs active | Inactive S1^TM6 stabilised by the ionic lock **plus** **R291^7.56−H230^6.32** and **R293^8.48−H230^6.32** cation-π, with TM3/TM6/TM7-H8 clustered. In S2^TM6 the lock is broken and *"only the R291^7.56-H230^6.32 is required for the stabilization of the I2^TM6 conformation"*. In the **fully activated** conformation the stabilising contact is **R^8.48−H^6.32**. Mutation **R291^7.56A traps A2AR in I2^TM6**, preventing the fully activated A^TM6 | **pp.3, 9** |
  | 11 | **DRY motif (D3.49−R3.50−Y3.51)** | inactive → active | Activation: *"the inward movement of residues I3.40 from the PIF motif and **R3.50 from the E/DRY motif that pushes F6.44 (PIF motif) and L6.34 outward**, resulting in the outward displacement of the cytoplasmic portion of TM6 from TM7"*. In the complex, R3.50 makes polar contacts with the Gα Cα5 helix, and the compact fully-activated complex is stabilised by **R7.56−E392(Gα) ionic H-bond and R3.50−Y391(Gα) cation-π** | **p.24**; Cα5 contacts **p.4** |
  | 12 | **NPxxY motif (N7.49−P7.50−x−x−Y7.53)** | inactive → active | TM7 rotates with **inward movement of NPxxY**; *"allowing Y7.53 to lose contact with residues in TM1 or H8 and shift toward TM3, enhancing TM3-TM7 packing"*. Upstream trigger: TM5 motion collapses the Na⁺ pocket → contacts between **N7.49 and N7.45, D2.50, S3.39**, pulling TM7 toward TM3 | **p.3** |
  | 13 | **"YY-lock" / Y−Y interaction (Y5.58···W6.48···Y7.53 or Y5.58···water···Y7.53)** | the defining active-state polar lock | *"A key step in activation is the downward movement of Y5.58 in TM5, enabling a water-mediated hydrogen bond with Y7.53 of the NPxxY motif — forming the so-called 'YY-lock'"*; it *"strengthen[s] the TM5-TM7 packing and stabiliz[es] the outward shift of TM6"*. Part of the **T3.46−Y5.58−Y7.53** polar motif | **p.24**, mechanism **p.3** |
  | 14 | NPxxY read out by proteolytic accessibility (LiP-MS, A2AR) | antagonist vs potent agonist | *"For potent agonists, reduced accessibility was observed for the N7.49P7.50xxY7.53 motif (F286^7.51, Y288^7.53) at the cytoplasmic end of TM7, which undergoes a slight inward movement toward the receptor core for class A GPCRs upon agonist activation"* | **p.22** |
  | 15 | **PIF / connector motif (P5.50−I3.40−F6.44)** | inactive vs intermediate vs active — **and the criterion that separates A2AR from β2AR/β1AR** | Active packing: *"residues P5.50 and F6.44 in a cis position form a CH-π hydrophobic interaction, while the CH3 group of I3.40 similarly forms a CH3-π interaction. The packing rearrangement in I3.40, P5.50, L5.51, and F6.44 motifs weakens TM5/TM6 contacts"*; the P5.50 rotamer change transmits TM5→TM6. **The receptor-dependent split**: in agonist-only **A2AR** (2YDV/2YDO) PIF is already **active-like** and matches the fully active state; in agonist-only **β2AR** (3PDS) and **β1AR** (2Y02/2Y03/2Y04) PIF is **inactive-like** | **p.3**; the split **pp.7−8** |
  | 16 | PIF as an NMR-visible discriminator between the active-region states | I2^TM6 vs A^TM6 | ¹⁵N PRE NMR: *"I2^TM6 and S1^TM6 conformational states have similar structure in the PIF motif and TM6 cytosolic conformation"*, whereas *"compared to S1^TM6 or I2^TM6, conformation A^TM6 exhibits a **major TM6 outward pivotal movement associated with a large conformation change in the PIF motif**"* | **p.17**, restated **p.25** |
  | 17 | **CWxP / "toggle switch" W6.48 (C6.47−W6.48−P6.50)** | agonist-engaged vs not | W6.48 *"changes side chain rotamer state"* and *"move[s] lower, toward residue F6.44"*; **P6.50 acts as a hinge in TM6, reducing the activation energy barrier to opening the intracellular cavity**. F6.44 is *"conserved in 82% of class A GPCRs"*. The W6.48 conformation and shift are *"affected by the orientation of the neighbor F6.44"*, coupling CWxP to PIF | Fig 1 caption **p.2**; mechanism **p.3**; W6.48/F6.44 coupling **p.11** |
  | 18 | **Na⁺ pocket / D2.50** | inactive stabiliser | A water-filled cavity around **D2.50** holds a Na⁺ in inactive-state crystal structures and *"allosterically stabilizes TM3 and TM7 in the inactive state"*. On activation: *"The motion of TM5 causes the putative sodium-binding pocket to collapse, leading to dehydration of D2.50 and displacement of the sodium cation, which is free to egress in the cytosol and a possible protonation of D2.50"* | **p.3** |
  | 19 | **TM5 displacement** | inactive → active | *"the intracellular part of TM5 swings outward, while its central and EC segments **shift inward by ∼2.5 Å**"* | **p.24** |
  | 20 | **"Activating ionic lock" R5.66−E6.30 — a *second*, active-side ionic lock** | marks a **pseudo-active intermediate Ix^TM6**, and is also present in I2^TM6 and A^TM6 | Found by minute-timescale metadynamics (D'Amore/Limongelli 2024): *"an additional 'pseudo-active' intermediate conformation, Ix^TM6, was found, characterized by an 'activating ionic lock' formed also in A^TM6 and I2^TM6 conformations."* Observed in the active rhodopsin X-ray structures **3CAP and 3DQB** (which carry the R5.66K mutation). **Caveat the review gives**: in 5G53, 6GDG, 7LD3 and 8HDP the ICL3 near E6.30 is **unresolved**, so this contact cannot be checked in those entries | **p.11** |
  | 21 | **Cross-receptor active-state similarity — the review's own RMSD** | how alike two different receptors' fully active states are | *"the superposition of the NECA−A2AR−mini-Gs complex (PDB ID 5G53) with the BI-167107−β2AR−Gs complex (PDB ID 3SN6) reveals that the conformations of the corresponding GPCRs are strikingly very similar, as evidenced by the root-mean-square deviation (RMSD) in Cα carbons [**RMSD(Cα) = 1.7 Å over 1239 Cα carbons**]. The intracellular segments of the receptors, including the significant outward displacement of the cytoplasmic end of TM6 during activation, are very well aligned."* | **p.6** |
  | 22 | ICL2 secondary structure as a coupling-selectivity criterion | Gs-coupled vs Gi-coupled active | On Gs coupling *"ICL2 adopts an α-helix conformation"* and F139^ICL2 (34.51) inserts into the Gαs αN/β1-hinge, β2/β3-loop, F376 pocket. With Gi1, ICL2 *"was more flexible … and could not form an α-helix"* | **p.7**; Gi contrast **p.17** |
  | 23 | ICL3 N-terminal helix formation | inactive → Gs-active | *"in the extension of TM5, the N-end of ICL3 forms an α-helix, and TM6 is extended outward"* | **p.7** |

  ### C.2 — Spectroscopic / biophysical criteria (the ones that see transient states)

  | # | criterion | what it distinguishes | reported value / range | page |
  |---|---|---|---|---|
  | 24 | **¹⁹F NMR chemical-shift regions at a cytoplasmic label** — the origin of the whole S1/S2/I1/I2/A vocabulary | five states along one helix | Label sites used: **TM6** V229^6.31C, L225^6.27C (A2AR); C265^6.27, L266^6.28C (β2AR); A282^6.27C (β1AR). **TM7** A289^7.54C (A2AR); C327^7.54 (β2AR); C344^7.54 (β1AR). Apo-A2AR shows *"the equilibrium of the inactive conformations S1^TM6 and S2^TM6, the active intermediates I1^TM6, I2^TM6, and the A^TM6 that correspond to the fully activated conformation"* | **pp.8−9**; β2AR **pp.15−16**; β1AR **p.20** |
  | 25 | **smFRET TM4−TM6 separation — note the polarity, it is the opposite of the naive reading** | active vs inactive cytoplasmic cavity | *"full agonists produce a primarily **high-FRET** population (**active** conformation with a **closed cytoplasmic cavity and small TM4-TM6 distance**), inverse agonists produce a predominantly **low-FRET** population (**inactive** conformation with an **open cytoplasmic cavity and large TM4-TM6 distance**)"*. Dye pairs: AF488/AF647 at T119(TM4)/Q226^6.28 (A2AR); Cy3B\*/Cy7\* at N148C^4.40/L266C^6.28 (β2AR) | **p.19**, Fig 5 **p.19**; A2AR labels **p.9** |
  | 26 | **Bimane–tryptophan quenching distance window (ionic-lock reporter, β2AR)** | ionic lock intact vs disrupted | *"When the fluorescent probe groups bimane and tryptophan were at **5−15 Å**, quenching of bimane fluorescence by tryptophan reported an interaction."* In the inactive conformation of apo-β2AR *"the distance between Cα carbons of **A271^6.33 and I135^3.54 is ∼11 Å**"* (construct: A271^6.33C, I135^3.54W) | **p.15** |
  | 27 | DEER TM4−TM6 distance distribution | inactive vs active populations, with population weights | Spin labels at **C265^6.27, L266^6.28C (TM6) and N148^4.40C (TM4)** in β2AR; the broken-lock **S2^TM6 was the predominant inactive conformation** | **p.16** |
  | 28 | ¹³C-Met chemical shift as a region-specific reporter (β2AR) | OBS vs connector vs cytoplasmic | **M82^2.53** reports the OBS environment (*"at a 4−5 Å distance close to many amino acids that interact with both agonists and antagonists"*); **M215^5.54** and **M279^6.41** report the connector/TM region; **L272^6.34M** reports the cytoplasmic TM6 end | **pp.15−16** |
  | 29 | ¹⁵N-Trp reporters at helix ends (A2AR) | one signal = one state, two = two | F201^5.62W, K233^6.35W, Y290^7.55W; *"a single ¹⁵N−¹H signal for each of these tryptophans was measured for the complexes with antagonists, two signals were observed for a complex of K233^6.35W A2AR with an agonist"*; adding mini-Gαs collapses the two peaks to one | **pp.10−11** |
  | 30 | ¹⁹F line width as a dynamics (not population) reporter | orthosteric antagonist vs NAM | *"the line width of state I2^TM7 was reduced by **30 Hz** in the presence of ZM241385 but increased by **70 Hz** in the presence of hexamethylene amiloride (HMA) or Fg754"* | **p.13** |

  ### C.3 — The state nomenclature, and how it maps onto deposited structures

  | state label | what it is | proposed structural counterpart | page |
  |---|---|---|---|
  | **S1^TM6** | inactive, **ionic lock formed**, cation-π contacts present, TM3/TM6/TM7-H8 clustered | ZM241385−A2AR−T4L (3EML) — with the caveat in the next row | pp.9, 10 |
  | **S2^TM6** | inactive, **ionic lock broken**; the *predominant* inactive state of apo-β2AR by DEER | ZM241385−A2AR-StaR2 (3PWH) — **but the review flags this as possibly a construct artefact**: *"the T4 lysozyme fusion in ICL3 may cause an outward movement and rotation in TM6 in structure PBD ID 3PWH, which is why the 'ionic lock' may be absent in the A2AR−T4L structure"* | pp.9, 16 |
  | **I1^TM6** | activation intermediate; **corresponds to the pre-coupled GPCR−G complex**; more stable with GDP present than without | *"I1^TM6 conformation corresponds to the complex GPCR−G"* (no PDB); pre-assembled β2AR-Gs^empty and β2AR-Gs^GDP show low/intermediate FRET consistent with I1^TM6 | Fig 4 **p.10**; β2AR **p.19** |
  | **I2^TM6** | active-region **intermediate**; **low-efficacy** activation state; preferentially stabilised by a **partial agonist**; binds G^GDP but has *"a limited rate for the critical GDP/GTP exchange"*; corresponds to **noncognate Go/Gi**-coupled states | A2AR: agonist-only 2YDV/2YDO; **and, definitively, the R291^7.56A A2AR−mini-Gαsβγ cryo-EM structures 9EE8/9EE9/9EEA**. β2AR: 3PDS (FAUC50−β2AR); also 2Y02, and its PIF resembles 3NY8/3NYA | pp.10, 11, 25 |
  | **A^TM6** | **fully activated-like**; **high-efficacy**; stabilised by a **full agonist plus transducer**; corresponds to **cognate Gs^empty** | A2AR: **5G53** (NECA−A2AR−mini-Gs), **6GDG** (adenosine−A2AR−Gαβγs^empty). β2AR: **3SN6**, **4LDE**, **3P0G** | pp.10, 16, 25 |
  | **Ix^TM6** | a **sixth**, "pseudo-active" intermediate found only by minute-timescale metadynamics, defined by the R5.66−E6.30 "activating ionic lock"; may serve as I1^TM6 | 3CAP / 3DQB (active rhodopsin, R5.66K) | p.11 |
  | **S1/S2/I1/I2/A^TM7** | the **parallel series along TM7**. Explicitly **not** the same as the TM6 series: *"The populations of the TM6 activation states (I1^TM6, I2^TM6, A^TM6) and TM7 activation states (I1^TM7, I2^TM7, A^TM7) may be correlated, albeit they are not identical."* A further unnamed **I^TM7** appears with partial agonists at 280/298/310 K and *"was not previously found in the spectra of apo-A2AR, agonist-bound, or antagonist-bound A2AR"* | A^TM7 and I2^TM7 *"have not been seen in reported crystal structures of A2AR"* | Fig 3 **p.9**; TM7 series **pp.12−13**; I^TM7 **p.13** |

  **The practical warning this table encodes**: a single-coordinate predicate ("TM6 out by X Å" or "ionic lock broken") is **not sufficient** to call a Class A state according to this review. The ionic lock separates two *inactive* states, not inactive from active (p.3). PIF separates active from intermediate in A2AR but not in β2AR/β1AR (pp.7−8). TM6 and TM7 give correlated-but-non-identical answers (p.14). A defensible predicate needs at least the TM6 displacement **plus** the NPxxY/YY-lock **plus** PIF, and even then the receptor identity matters.

- **metric_saturation**: **NOT APPLICABLE — the review reports no metric of its own, so nothing of its own can floor or ceiling.** (The one measurement-validity concern it raises — anomalously high active-state populations in nanodiscs — is a systematic bias, not saturation, and is recorded in `stated_limits`. No axis break or truncation exists in any figure; see `hides` in section F for Figure 3's unlabelled axes, which is the related figure-level defect.)


> **CORRECTION, 2026-09-11 (lit-3d).** The two entries below citing "p.10" for a 21-residue GαS C-terminal peptide are correct about the *content* — the verbatim is on printed p.3700 — but the review's own attribution of it to "Eddy and collaborators in 2021" (ref 155, Structure 29(2):170–176) is **wrong**: that paper's complete full text contains no G protein, no peptide and no 6.35/5.62/7.55. The primary is **Eddy et al., J. Am. Chem. Soc. 2018, 140(26):8228–8235, DOI 10.1021/jacs.8b03805**, residues 374–394 of GαS at 10-fold molar excess, A2AR only, no length series. The primary also does **not** call the 21-mer a "mini-Gαs"; that label is this review's. Never quote this review for the 21-mer. Full text and detail: `lit/source/pending_text/` and `lit/analysis_review/EDDY_PRIMARY_SOURCE.md`.

- **directional_control**: **NOT APPLICABLE as a method property** — the review controls nothing. **But it is one of the best available inventories of the *physical* handles that direct a Class A receptor to a state**, which is why it matters to us:
  - **Orthosteric ligand, graded by efficacy** — inverse agonist → S1/S2; neutral antagonist → inactive-like; **partial agonist → I2**; **full agonist → shifts toward A but does not reach it alone**; superefficacy agonist (BU72, lofentanil at μOR) → *"stabilize only the two active conformations, A^TM6 and I2^TM6"* (p.21).
  - **Transducer** — Gs / Gi / Go heterotrimer, **Gs^GDP vs Gs^empty** (nucleotide state changes the answer), mini-Gs (a 21-residue Gαs C-terminal peptide is enough to shift populations, p.10), Gα C-terminal peptides.
  - **G-protein-mimetic nanobodies** — **Nb80, Nb6B9, Nb39, Nb6** used throughout as the surrogate that produces A^TM6.
  - **β-arrestin** and **GRK** — direct to distinct, non-Gs active states; β-arr-biased agonists act on **TM7** rather than TM6 (p.15).
  - **Allosteric modulators** — PAM Cmpd-6FA (β2AR, 6N48), NAMs amiloride/HMA/Fg754 at the Na⁺ site, SBI-553 at NTS1R.
  - **Ions** — **Na⁺ stabilises inactive**; **Ca²⁺/Mg²⁺ shift toward active** (I2/A), an effect amplified when agonist + mini-Gαs are present (p.9).
  - **Lipids and membrane mimetic** — anionic phospholipids (**PIP₂**) *"enhanced the population of active-like conformation A^TM6, thus priming the receptor toward recognizing Gαs"*; **cholesterol/CHS acts oppositely in different receptors** — shifts A2AR toward active but acts as a **NAM against β1AR** (pp.23, 26).
  - **Mutations** — **R291^7.56A traps A2AR in I2^TM6** (the cleanest single state-trapping handle in the review, p.9); constitutively activating mutations I92^3.40N and R291^7.56Q; D52^2.50N reduces activity and *"eliminated the sensitivity of the receptor to the efficacy of bound ligands"* (p.13).
  - **Construct artefacts that act as unintended handles** — **T4L fused into ICL3 forces active TM6 conformations regardless of ligand efficacy** in β2AR (p.16) and may create an artefactual broken lock in A2AR 3PWH (p.9). **Relevant to anyone using T4L-fusion structures as state references.**

- **anti_memorization_design**: **NOT APPLICABLE.** No trained model, no training set, no cut-off, nothing that could be memorised. The nearest analogue — whether the review's conclusions depend on structures deposited after some date — is not a meaningful question for a secondary source.
- **anti_memorization_control**: **NOT APPLICABLE**, same reason. `NONE RUN` would be technically true and semantically empty.

- **controls_run**: **NOT APPLICABLE — the authors ran no experiment, therefore no control arm.** For reuse, the **control and perturbation arms the review reports from the primary literature** are listed below; these are other people's controls, recorded here because they are the most reusable operational content in this part of the paper and because several of them are exactly the arms a state-prediction paper would want to cite.

  | control / perturbation (from the primary literature) | what it rules out or establishes | page |
  |---|---|---|
  | **Apo (unliganded) receptor arm**, run in essentially every NMR/DEER/smFRET study cited | Establishes that heterogeneity and a populated active-like state exist **without any ligand** — the basal-activity baseline | pp.9, 15, 16, 19, 20 |
  | **Inverse agonist arm** (ZM241385, carazolol, ICI 118,551, timolol) | Rules out "agonist merely reveals a pre-existing single active state" by showing the equilibrium moves the other way; also shows a **residual ~40% active-like population persists even with an inverse agonist** | pp.9, 16 |
  | **Neutral antagonist arm** (alprenolol, naloxone) vs inverse agonist | Separates "blocks agonist" from "actively stabilises inactive" — alprenolol-bound β2AR still couples Gs | p.14 |
  | **Agonist-only (no transducer) arm** — the load-bearing control for our purposes | **Establishes that agonist alone does not produce the fully active state**; produces I2^TM6 instead | pp.7−8, 16−17, 20−21 |
  | **Transducer-only (no agonist) arm** — Gs^empty-bound β2AR, β1AR + Nb80/mini-Gs without agonist | Shows a transducer alone stabilises a closed/active-like receptor and increases agonist affinity; MALDI-MS shows β1AR binds Gs/Gq *"even in the absence of agonist"* | pp.20, 22 |
  | **Nucleotide state swap** — G^GDP vs G^empty vs +GTP | Separates pre-coupled (I1) from nucleotide-free ternary (A); GDP removal shifts equilibrium to A^TM6/A^TM7 | pp.11−12, 14 |
  | **Cognate vs noncognate G protein** — Gs vs Go for A2AR; Gs vs Gi1 for β2AR | Shows the "active state" is transducer-specific: Go^empty preferentially stabilises I2^TM6 and *reduces* A^TM6 | pp.12, 14, 17 |
  | **State-trapping mutant R291^7.56A (A2AR)** | Isolates the I2^TM6 intermediate as a structure-determinable species (9EE8/9EE9/9EEA); shows it binds GDP but cannot do efficient GDP/GTP exchange | pp.9, 11, 25 |
  | **CAM / loss-of-function mutants** — I92^3.40N, R291^7.56Q (activating), D52^2.50N (attenuating) | Ties measured population shifts to basal activity in both directions | p.13 |
  | **F139^ICL2A (β2AR) and L174^34.51A (M3R)** | Separates "makes initial contact with G protein" from "causes GDP release" — the mutant still contacts Gs but cannot release GDP | pp.21−22 |
  | **T4L-fusion vs native receptor (β2AR, A2AR)** | The construct control that shows **ICL3 fusion itself forces active TM6 conformations** — a caution about using fusion-construct structures as state references | pp.9, 16 |
  | **Membrane-mimetic swap** — DDM/CHS vs MNG-3/CHS vs LMNG vs POPC/POPG or POPC/POPS nanodiscs vs liposomes vs LCP | Establishes that state populations and exchange rates are **mimetic-dependent**, and that nanodiscs inflate the active population (see `stated_limits`) | pp.11−14, 20, 25 |
  | **Cholesterol/CHS present vs absent; anionic vs neutral lipid** | Isolates direct lipid effects on the equilibrium and shows they are **receptor-specific and opposite in sign** between A2AR and β1AR | pp.23, 26 |
  | **Ergosterol vs cholesterol (STD NMR, β2AR)** | Rules out generic sterol binding — β2AR binds cholesterol but not the structurally related ergosterol | p.23 |

- **confidence_as_discriminator**: **NOT APPLICABLE.** No pLDDT/pTM/ipTM, and no predictive confidence measure of any kind. The nearest analogue — using a spectroscopic observable to judge conformational correctness — is exactly what the review documents, and it treats those assignments as **hypotheses**, hedging every state↔PDB mapping with "suggested" / "might correspond" / "may correspond" (pp.10, 16, 25).

## D. Claims

- **central_conclusion**: A Class A GPCR is not a two-state switch. In the apo form it already occupies an equilibrium of at least two distinguishable *inactive* states (separated by the ionic lock) plus one or more populated *active-region* states, and activation proceeds through a ladder of intermediates (S1 → S2 → I1 → I2 → A) that different ligands and different transducers populate differently, producing divergent signalling. Crucially, **agonist binding alone is generally not sufficient to stabilise the fully active conformation** — the transducer (G protein, mimetic nanobody, or arrestin) is required, and the strength of the allosteric coupling between the orthosteric site and the cytoplasmic face varies by receptor (strong in A2AR, weak in β2AR/β1AR/μOR). The transient states that carry this behaviour are largely invisible to crystallography and cryo-EM and are resolved instead by NMR, DEER, single-molecule fluorescence, MS and simulation.

- **necessity_claims**: **Verbatim, with pages. These are the sentences to cite for "an agonist is not enough" and "the transducer is required".**

  **(1) The strongest single statement that agonist binding alone cannot produce the active state — β2AR, from structures (p.17):**
  > *"The I2^TM6 conformation of agonist-only bound β2AR is different from that of A^TM6, since, according to the X-ray or cryo-EM structures, **the agonist binding alone cannot stabilize the fully active conformation**."* (p.17)

  **(2) The strongest statement that BOTH the agonist and the transducer are required — β1AR (p.20):**
  > *"The results from X-ray, cryo-EM, and NMR studies showed that, similar to β2AR and in contrast to A2AR, **the conformational changes in TM5 and TM6, which are required for the full engagement of a G protein, are almost completely dependent on the presence of both the agonist and the G protein or mimetic Nb**, revealing a weak allosteric coupling between the OBS and the G-protein-coupling interface (TM5 and TM6), with an intermediate active conformation of the agonist−β1AR complex being inactive-like."* (p.20)

  **(3) The same, stated as an absolute for μOR — the cleanest "no partner, no motion" sentence in the paper (p.21):**
  > *"…the movement of TM5, TM6, which are linked with the coupling of the GPCR with the G protein, **is observed only when both the agonist and the G protein or mimetic Nb are present; no movement of TM5, TM6 is observed when only the agonist is present**."* (p.21)

  **(4) Generic requirement across a class A and a class B receptor (p.3):**
  > *"**Both agonist and G protein binding are required for the receptor to move toward an active state in both receptors.**"* (p.3, on β2AR vs GCGR)

  **(5) The transducer's mechanical role — why an agonist cannot do it alone (p.5):**
  > *"Even with the glucagon agonist present, the GCGR-βarr1 complex assumes a conformation of GPCR more like the inactive state than the active one possibly because **the agonist by itself is unable to completely maintain the active conformation in the absence of the transducer to enlarge the intracellular pocket**."* (p.5)

  **(6) The simulation statement of the same point — the ionic lock is not broken by agonist alone (p.17):**
  > *"…it was observed that **the ionic lock is not broken by agonist binding to the inactive β2AR alone, which prevents the β2AR from moving toward the activated conformation**. Nevertheless, it was observed that when the inactive Gs (Gs^empty) is attached to the agonist-bound inactive β2AR (which has the ionic lock), Gαs-α5 helix partially inserts into the β2AR core, breaking the ionic lock and activating the Gs protein connected to β2AR."* (pp.17−18)

  **(7) What a state predicate must contain — the motif network requirement (p.24):**
  > *"**The successful coupling of a class A GPCR to a G protein requires that the canonical "microswitch" motif network be composed of the following motifs: C6.47W6.48P6.50 (CWxP), the P5.50I3.40F6.44 (PIF), Na+ pocket, D3.49R3.50Y3.51 (DRY), N7.49P7.50xxY7.53 (NPxxY) along with the conserved Y5.58 residue in the T3.46Y5.58Y7.53 motif.**"* (p.24)

  **(8) The same requirement stated for activation (p.3):**
  > *"…**for the activation of a class A GPCR by an agonist, amino acid residues that belong to or correlate to a motif network should adopt certain conformations.**"* (p.3)

  **(9) The receptor-dependence of the OBS↔cytoplasm coupling — A2AR is the exception, not the rule (p.8):**
  > *"Thus, a strong allosteric connection in A2AR exists between the conformation of the intracellular region where the G protein binds and the agonist-bound OBS region. **This connection must be assumed for the receptor to bind the Gs protein, which triggers the signaling cascade.**"* (p.8)
  >
  > and the contrast, same page: *"Thus, in contrast to A2AR, β2AR, or β1AR showed a **weak allosteric connection** between the agonist's OBS and the cytoplasmic ends of TM5 and TM6 that must be engaged with the G protein for activation."* (p.8)

  **(10) The ionic lock is not a state discriminator — the sentence that should stop anyone using it as a binary predicate (p.3):**
  > *"Thus, the **DR3.50Y-E6.30 interaction does not differentiate the inactive from the active conformational ensemble** since it occurs during the transition between two inactive states, which is required for the activation of these class A GPCRs."* (p.3)

  **(11) The careful version of the same, for β2AR (p.16):**
  > *"These findings … **demonstrated that complete activation of the β2AR requires, but is not dependent upon, the disruption of this important molecular switch motif.**"* (p.16)

  **(12) Intermediate states and a continuum, against a binary model (p.6):**
  > *"Class A GPCRs can exist in **three different conformational states (active, inactive, intermediate-active)** that can be interconverted for the activation/inactivation process according to a **multistate, rheostat-like model, instead of a binary (on/off) switch model**."* (p.6)

  **(13) Even the inactive state is heterogeneous (p.9):**
  > *"The results suggested that **even in the inactive state, class A GPCRs exhibit conformational heterogeneity**."* (p.9)

  **(14) Agonist-only complexes are intermediates, and they are under-characterised (p.7):**
  > *"**Class A GPCRs in complex with only full agonists (without G or βarr protein) adopt an intermediate active conformation, which might be a preactive conformation in the activation pathway.** Τhe structure of class A GPCRs in such transient conformations **has not yet been thoroughly characterized**, despite its importance in understanding the different interactions with diverse signal transducers…"* (p.7)

  **(15) The mechanical requirement on the G protein side (p.4):**
  > *"The Cα5 helix, and particularly the distal C-end part (known as the 'wavy hook'), **must be inserted into the receptor's cytoplasmic cleft to couple with the GPCR**"* (p.4); and *"**The Cα5 helix requires a conformational shift to couple with the GPCR.**"* (p.5)

  **(16) Gβγ is required for efficacy transmission — often forgotten in receptor-only modelling (p.11):**
  > *"It was also suggested the **Gβγ subunit is essential for transmitting the efficacy of the ligand from the receptor to the GDP binding site in Gα**. Therefore, while investigating allosteric mechanisms linked to G protein activation mediated by the receptor, research must be performed on the Gβγ subunit in addition to the Gα subunit."* (p.11)

  **(17) The programmatic necessity claim that opens the Discussion (p.23):**
  > *"**The identification and structural characterization of the conformational equilibrium and the kinetics of the conformational changes of class A GPCRs are required toward understanding and controlling signaling selectivity and agonist efficacy.**"* (p.23)

  **(18) The paper's opening impossibility claim (p.1):**
  > *"On the question of which conformations of a G protein-coupled receptor (GPCR) are best for a given transducer protein coupling that can activate one signaling pathway over another, **an answer cannot be given in general**."* (p.1)

  **(19) What is still not known — useful as a "the field has not solved this" citation (p.27):**
  > *"**The molecular determinants of G protein or β-arr coupling specificity are still not accurately defined, despite many available experimental structures of class A GPCRs in combination with different G protein subtypes.**"* (p.27)

  **(20) A narrower open problem (p.22, restated p.26):**
  > *"…**it is still unclear what structural features allow the release of GDP during primary class A GPCR-Gi/o coupling.**"* (p.22)

  **(21) Counter-example worth holding — an inactive OBS conformation can still be bound to a G protein (p.4):**
  > *"Strikingly, three cryogenic electron microscopy (cryo-EM) structures of κOR-Gi protein complexes with different inverse agonists (norBNI, JDTic, GB18) showed that the complexes of inverse agonist-GPCR are also bound to Gi proteins (PDB IDs 8VVE, 8VVF, 8VVG). Remarkably, **the OBS has an inactive receptor conformation, yet the receptor stays attached to the Gi protein.**"* (p.4) — *This breaks the naive implication "G-protein-bound ⇒ active", and is a direct threat to any predicate that infers state from the presence of a partner.*

- **novelty_claims**: **Essentially NONE — and that absence is itself worth recording.** This is a review; it makes no priority claim, claims no first, and describes nothing as unprecedented. Exhaustive search of the body for "novel", "first", "unprecedented", "for the first time" returns exactly one candidate, and it is a claim about a *criterion*, not about the authors' own work:
  > *"Thus, ligands have the innate ability to alter the receptor's conformational exchange kinetics, causing signaling bias. **This is a novel and additional criterion that should be considered in drug-discovery initiatives.**"* (p.25)

  Two further "new-finding" statements are made **about other people's papers**, not about this one, and must not be mis-attributed:
  > *"…**an agonist−GPCR−G protein complex with GPCR (R291^7.56A A2AR) in an intermediate active conformation was resolved** by the collaborative effort of the laboratories of Ye, Cheng, Miao, and reported in 2025 (PDB IDs 9EE8, 9EE9, 9EEA)."* (p.4) — and *"**This work addresses a knowledge gap in the intricacy of class A GPCR signaling.**"* (p.25, referring to that same ref 80.)
  >
  > *"…the presence of a **previously unseen active intermediate I^TM7**…"* (p.13, referring to Eddy and collaborators 2024, ref 157.)

  The only self-referential statement of scope is (p.1): *"In this review, we focus on results showing the complexity of describing the conformational landscape and signaling of the β2 adrenergic receptor (β2AR), adenosine A2A receptor (A2AR), as well as the β1 adrenergic receptor (β1AR) and μ opioid receptor (μOR)."*

- **stated_limits**: The authors are unusually candid about the limits of the evidence base. Recorded here in the order that matters most to us.

  1. **The deposited-structure base is state-biased toward the active conformation** (p.4): *"most cryo-EM GPCR structures are available, due to the size requirements of the protein, in the fully activated conformation of the GPCR, according to data selected in the GPCRdb"* (623 cryo-EM vs 477 X-ray structures).
  2. **The states that matter are not in the PDB at all** (p.1, abstract): transient states *"may have eluded identification by X-ray crystallography and cryogenic electron microscopy"*. Specific instance (p.13): *"It was suggested that A^TM7 and I2^TM7 conformations have not been seen in reported crystal structures of A2AR."*
  3. **Agonist-only intermediate states are poorly characterised** (p.7): *"has not yet been thoroughly characterized, despite its importance."*
  4. **The activation mechanism is not transferable between receptors or even subtypes** (p.7): *"likely to differ between different categories of class A GPCRs and even for distinct subtypes of the same family."* Direct evidence: PIF is active-like in agonist-only A2AR but inactive-like in agonist-only β2AR/β1AR (pp.7−8); the ionic lock is absent from inactive β1AR/β2AR/μOR structures (pp.3, 7).
  5. **Nanodisc/HDL measurements give anomalously high active-state populations** — a systematic-error warning that directly undermines quoted population numbers (p.25): *"It must be underlined that there is a concern regarding the consistency of results from the HDL system in lipid nanodiscs with pharmacological research. Thus, the percentage of conformations in the active region of the conformational landscape was observed for both A2AR and β2AR using 19F NMR, abnormally high compared to the micelles system, e.g., MNG-3/CHS. For example, β2AR contains over 40% activation conformations by solution 19F NMR in lipid nanodiscs, in contrast to the low constitutive activity of the receptor. … it seems that the HDL system may not be appropriate, possibly because the scaffold protein MSP1D5 may affect the chemical shifts, perturbing its conformational profile."*
  6. **¹⁹F NMR — the technique most of the state assignments rest on — has a known blind spot** (p.24): *"there are cases where 19F chemical shifts were not sensitive to conformational alterations that have been identified by other techniques in GPCR research. Interestingly … all 19F labeling sites that displayed conformational changes are situated close to aromatic residues."*
  7. **Fusion-construct artefacts** (pp.9, 16): T4L in ICL3 may create the apparent broken ionic lock in 3PWH, and in β2AR *"the effect of T4L linked to IL3 of β2AR … is to cause the population of only active TM6 conformations independent of the efficacy of bound ligands."*
  8. **MS methods mostly see loops, not helices** (p.22): *"Most HDX-MS and HRF-MS-based structural investigations track conformational changes of specific loops or N/C-terminal regions, and relatively few dynamics of TM domains are revealed."*
  9. **Coverage gaps**: only two GPCR–GRK structures exist (p.5); *"The conformational space for binding to GRKs is understudied"* (p.26); *"little is known about"* noncognate GPCR–G interactions (p.18); *"the level of progress for A2AR is low"* on biased ligands (p.27).
  10. **Direct contradictions between techniques are reported and left unresolved** — e.g. partial agonist stabilises a distinct I2^TM6 by ¹⁹F NMR/smFRET, but *"the addition of a partial agonist showed no effect on the A2AR conformation"* in TM7-labelled DDM/CHS ¹⁹F NMR (p.13); and the smFRET-vs-crystal disagreement about whether A^TM6 corresponds to 5G53/6GDG (p.13).
  11. **Mechanistic gaps named as unexplained**: how D52^2.50N reduces signalling *"has not been decided"* (p.13); *"The impact of agonist-free GPCR−G protein complexes and the conformation of the corresponding GPCR in the pharmacological response is not well understood"* (p.24); the *"wavy hook's"* mechanism in primary Gi/o coupling is cast into doubt (p.22).
  12. **Scope limit, self-declared** (p.24): the review positions itself against six prior reviews of the same material and confines itself to *"important observations for A2AR, β2AR, β1AR, and μOR."*

- **stance**: **`background` — a single stance, and provisional (the user's call).** This paper is not a competitor, not a precedent for any method, and poses no threat to a methodological claim. It is the **authoritative reference source** for (a) what the states are, (b) what the structural criteria for calling them are, and (c) the mechanistic fact that a transducer is required. There is a case for a secondary `contrast` reading — the review's insistence that a single structural coordinate cannot call a Class A state is an implicit argument against any binary state predicate, including ones the corpus holds — but that is a use we make of it, not a position it takes, so it is recorded here rather than promoted to a second stance.

## E. Quantitative comparators

- **metrics_reported**: The review reports no metric of its own; every number is attributed. What follows is the harvest, because these are the values a table of ours could sit beside. Grouped, one row per number.

  **E.1 — Structural distances and angles**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | TM6 outward swing, cytoplasmic end, generic class A | ∼7−14 | Å | inactive vs active, crystallographic/biophysical/biochemical studies | 24 |
  | TM6 displacement at Thr224^6.26 Cα, rhodopsin | ∼6 | Å | inactive vs agonist+G-protein-bound | 7 |
  | TM6 displacement at Thr224^6.26 Cα, β2AR and A2AR | ∼14−18 | Å | inactive vs agonist+G-protein-bound | 7 |
  | A2AR TM6 rotation about F282^6.44, inactive→intermediate→active | ∼40 | ° | 3EML → 2YDV → 5G53 | 7 |
  | A2AR Thr224^6.26 Cα shift, inactive→intermediate active | ∼4 | Å | 3EML → 2YDV | 7 |
  | A2AR Thr224^6.26 Cα further shift, intermediate→fully active | ∼14 (additional) | Å | 2YDV → 5G53 | 7 |
  | A2AR T224^6.26 outward movement, agonist-only vs mini-Gs-bound | ∼14 | Å | agonist-only A2AR vs agonist−A2AR−mini-Gs | 22 |
  | β2AR TM6 outward displacement from TM3 on Gs-α5 insertion (metadynamics) | ∼5 | Å | inactive agonist-bound β2AR + Gs^empty | 18 |
  | TM5 central/EC segment inward shift on activation | ∼2.5 | Å | inactive vs active | 24 |
  | RMSD(Cα), A2AR−mini-Gs (5G53) vs β2AR−Gs (3SN6) | **1.7** | Å over **1239** Cα | two fully activated complexes of different receptors | 6 |
  | β2AR inactive, A271^6.33−I135^3.54 Cα distance | ∼11 | Å | apo-β2AR inactive conformation | 15 |
  | Bimane−Trp quenching window | 5−15 | Å | probe-pair interaction detection | 15 |
  | Distance, nucleotide-binding pocket ↔ GPCR/G interface | ∼30 | Å | the allosteric span GDP release must cross | 21 |

  **E.2 — State populations (all from cited primary work; see `stated_limits` item 5 before using the nanodisc numbers)**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | β2AR active-like population, apo (enhanced-sampling MD, AWH) | 38 | % | basal activity of β2AR | 16 |
  | β2AR active-like population, ¹⁹F NMR MNG-3 micelles, **even with inverse agonist** | 40 | % | same | 16 |
  | β2AR inactive S1+S2 population with ultrahigh-affinity full agonist BI-167107 (DEER) | 40−50 | % | reduction from apo | 16 |
  | β2AR S2^TM6 population with low-affinity full agonist isoproterenol | 15−20 | % | ¹⁹F NMR / DEER, MNG-3(/CHS) | 16 |
  | β2AR inactive population with balanced agonist formoterol | ∼35 | % | ¹⁹F NMR, DDM/CHS | 15 |
  | β2AR active-region population, ¹⁹F NMR in **lipid nanodiscs** | >40 | % | flagged by the authors as anomalously high vs low constitutive activity | 25 |
  | A2AR active-state population, ¹⁹F NMR POPC/POPG nanodiscs | 50 | % | apo/ligand conditions | 11 |
  | A2AR TM7 (SMF/TIRF, nanodiscs): apo and antagonist | 63 inactive / 37 active | % | three-state fit | 13 |
  | A2AR TM7, agonist NECA-bound | 49 inactive / 37 I2^TM7 / 14 A^TM7 | % | same | 13 |
  | A2AR A^TM7 population change on mini-Gs addition, apo/antagonist | <1 → 8 | % | ± mini-Gs | 13 |
  | A2AR A^TM7 population change on mini-Gs addition, NECA-bound | 14 → 21 | % | ± mini-Gs | 13 |
  | A2AR I2^TM7 population change with ZM241385 | −13 | % | ¹⁹F NMR, DDM/CHS | 13 |
  | A2AR I2^TM7 population change with NAM amiloride | +5 | % | same | 13 |
  | A2AR I2^TM7 population change with NAM Fg754 | +8 | % | same | 13 |
  | A2AR I2^TM7 line width, +ZM241385 / +HMA or Fg754 | −30 / +70 | Hz | same | 13 |
  | β1AR I2^TM6 population with isoprenaline | 20 | % | ¹⁹F NMR micelles; rises with agonist efficacy | 20 |
  | μOR population shift to active (A^TM6 + I2^TM6) with DAMGO | 25 | % | DEER TM4−TM6; noted as **not** reflecting DAMGO's 100% efficacy | 21 |
  | β1AR selectivity: drop in receptor−mini-Gi complex vs mini-Gs (nMS) | 30 | % | equimolar mini-Gs vs mini-Gi | 23 |

  **E.3 — Kinetics and lifetimes**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Receptor activation time | several | ms | time-resolved MS, β2AR | 3 |
  | A2AR inactive↔active exchange, micelles (¹⁹F NMR) | low-ms | — | S1/S2 ↔ active region | 12 |
  | A2AR inactive↔active exchange, POPC/POPG nanodiscs (smFRET) | ∼3 | ms | apo and antagonist-bound | 12 |
  | A2AR S1^TM6↔S2^TM6 exchange, nanodiscs | ∼2 | ms | vs faster in LMNG micelles | 12 |
  | A2AR inactive↔active exchange, ¹³C NMR micelles | slower than ∼20 | ms | Met signal intensity | 12 |
  | A2AR exchange between the ≥2 active species (different NPxxY conformations) | faster than 20 | ms | ¹³C NMR | 12 |
  | A2AR cytosolic TM6 rearrangements (FCS/PET) | 150 ns − 300 μs | — | apo and antagonist-bound | 12 |
  | A2AR I2^TM6↔A^TM6, agonist-bound (smFRET) | 300−500 | μs | sub-ms | 12 |
  | A2AR I2^TM6↔A^TM6 (smFRET, micelles) | ≥3 | ms | apo, partial and full agonist | 12 |
  | A2AR agonist-bound dynamics (SMF/TIRF) | 390 ± 80 | μs | vs slower apo | 14 |
  | A2AR SMF/TIRF exchange | >100 | ms | longer-timescale processes | 14 |
  | A2AR inactive-state occupancy time (SMF/TIRF), A2AR and D52^2.50N | ∼2.9 | s | vs CAM receptors | 14 |
  | A2AR inactive-state occupancy time, CAM receptors | ∼1.5 | s | vs wild type | 14 |
  | A2AR inactive-state occupancy time, agonist-bound + mini-Gs | ∼1.8 | s | ± mini-Gs | 14 |
  | β2AR S1^TM6↔S2^TM6 exchange | hundreds of | μs | ¹⁹F NMR, MNG-3 | 19 |
  | β2AR I2^TM6 lifetime | ∼600 | ms | ¹⁹F NMR, MNG-3 | 19 |
  | β2AR TM6 end movements on full-agonist binding (SMF) | hundreds of | ms | DDM micelles | 19 |
  | β2AR inactive↔active switching (SMF/TIRF, nanodiscs) | 0.2−2 | s | apo, agonist, inverse agonist | 20 |
  | β2AR TM6 movements, single-liposome assay | long ms − min | — | truncated β2AR at C365 | 20 |
  | β2AR inactive↔active exchange enthalpy difference | ∼40 | kJ/mol | ¹⁹F NMR, DDM/CHS | 18 |
  | β1AR exchange, inactive↔I2^TM6 and I1^TM6↔A^TM6 | sub-s | — | ¹⁹F NMR micelles | 20 |
  | μOR S1^TM6↔S2^TM6 exchange | sub-ms | — | smFRET, antagonist and low-efficacy agonists | 21 |
  | μOR inactive↔I2^TM6 exchange | >100 | ms | smFRET Cy3/Cy7 | 21 |
  | Agonist−β2AR−Gs^empty complex lifetime | 5−10 | min | smFRET, nucleotide-free | 20 |
  | Same, with 30 μM GDP or 100 μM GTP | 6−12 s (a 20−100-fold reduction) | — | physiological nucleotide | 20 |
  | β2AR−mini-Gs complex dissociation after ICI 118,551 | >15 | min | BRET in live cells | 20 |
  | Isoproterenol−β2AR−Gs^GDP ternary complex formation | a few | s | time-resolved MS / crystallography | 21 |
  | GDP release and formation of agonist−β2AR−Gs^empty | **2−3** | h | HDX-MS / HRF-MS | 21, 24 |

  **E.4 — Free energies (all from cited simulation or AFM work)**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | apo-A2AR barrier separating pseudo-active from inactive, TM6 **rotation** | ∼15 | kcal/mol | metadynamics, POPC/cholesterol | 12 |
  | apo-A2AR barrier, TM6 **translation** | ∼7 | kcal/mol | same | 12 |
  | NECA-bound A2AR barrier, TM6 rotation / translation | ∼13 / ∼12 | kcal/mol | same | 12 |
  | Metadynamics convergence time, apo-A2AR / NECA-A2AR | 2.4 / 3.5 | μs | same | 12 |
  | β2AR free-energy barrier for structural-segment motions (AFM-SMF) | ∼52−72 kJ/mol (∼12−17 kcal/mol) | — | unliganded β2AR in DOPC/cholesterol liposomes | 16 |

  **E.5 — Corpus/database counts (useful for framing sentences)**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Deposited GPCR cryo-EM structures | 623 | structures | GPCRdb | 4 |
  | Deposited GPCR X-ray structures | 477 | structures | GPCRdb | 4 |
  | Structures / receptors in the activation-pathway analysis | ∼230 structures of 45 class A GPCRs → 34 residue pairs | — | Zhou et al. eLife 2019 | 3 |
  | GPCR structures covered by the large MD dataset | 60 | % of currently available | Selent and collaborators 2025 | 6 |
  | Distinct human GPCRs expressed | 826 | receptors | — | 2 |
  | Class A GPCRs as drug targets | ∼36 | % of commercial drugs | — | 1, 2 |
  | Human Gα genes / arrestin subtypes / GRKs | 16 / 4 / 7 | — | — | 2, 3 |
  | Deposited GPCR−GRK complexes | **2** | structures | — | 5 |
  | F6.44 conservation in class A | 82 | % | — | 3 |

- **n_predictions**: **NOT APPLICABLE.** No predictions, no samples, no targets in the sampling sense. The nearest analogue is the coverage of the review: 4 receptors treated in depth, ~90 PDB entries discussed by accession, 311 references.

- **comparable_to_ours**:

- **si_in_scope**: **No supplementary information exists and none is needed.** The PDF is complete: 27 pages of body (1−27) plus 11 pages of references (28−38). Every number in section E is in the main text. There is no SI table, no data availability statement, no code, and nothing withheld. **`SI NOT HELD` does not apply** — the gap that field exists to catch is absent here.

## F. Figures

**License note applies to all rows: `CC-BY 4.0`.** The statement *"This article is licensed under CC-BY 4.0"* appears in the header of **p.1**, and *"© 2025 The Authors. Published by American Chemical Society"* on the same page. **No ND clause and no NC clause** — redrawing, modification, adaptation and commercial reuse are all permitted with attribution. This is the most permissive licence in the corpus so far and makes Figures 1, 3 and 4 directly redrawable as background schematics.

**Six figures, six panel-group rows** (one row each; no figure mixes two data shapes, because — being a review — five of the six carry no measured data at all). Figures 5 and 6 share page 19. Figure attribution note from p.27: *"K.G. prepared the figures"*, and four of the six captions end with **"figure inspired by ref N"** — i.e. they are redrawn adaptations of published figures (Fig 1 ← ref 58; Figs 3 and 4 ← ref 153; Fig 5 ← ref 97; Fig 6 ← ref 230). **If we reuse them, the CC-BY here covers this rendering, but the underlying design is derived; cite both.**

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **The canonical microswitch figure.** Overlay of A2AR fully active (blue, 5G53, NECA−A2AR−mini-Gs) on inactive (green, 4EIY, ZM241385), with four insets showing the microswitches that change: (A) toggle switch W6.48 rotamer, top view; (B) PIF motif coupled motion, side view; (C) TM3−TM6 ionic lock and TM6 outward displacement, side view; (D) NPxxY inward/outward shift, side view | structure render | `RENDER \| facet: microswitch (4: CWxP/W6.48, PIF, ionic lock + TM6 outward, NPxxY) \| views: 2 (top view for A, side view for B–D) + 1 whole-receptor overlay \| overlay: 0 predictions on 2 reference(s) (5G53, 4EIY) \| axis: none` | 1 whole-receptor cartoon overlay + 4 lettered insets (A–D); insets vary by microswitch, not by system | The overlay is qualitative only: **no distance, angle or RMSD is annotated on any panel**, although the body text (pp.7, 24) supplies exactly those numbers. A reader taking the state criteria from the figure alone gets no values. Hydrogens omitted (stated) | CC-BY 4.0, p.1; "figure inspired by ref 58" |
| 2 | 4 | The G-protein cycle: Gα conformational changes from GPCR coupling with GDP bound, through GDP dissociation and the nucleotide-free complex, to GTP binding, heterotrimer activation, Gβγ release and separation from the receptor | schematic | `SCHEMATIC \| membrane-embedded cartoon strip of six labelled stages of the GPCR−Gαβγ nucleotide cycle (agonist; G-protein/GPCR association; nucleotide-free complex; GTP-bound open AHD; GTP-bound closed AHD; functional dissociation), with GDP/GTP and Cα5/RLD/AHD annotated \| no data` | 6 cartoon stages in a single horizontal membrane strip, left to right, with arrows; no lettering | | CC-BY 4.0, p.1 |
| 3 | 9 | **The free-energy landscape figure — the visual definition of the five-state model.** A drawn free-energy profile along a TM6-activation reaction coordinate, with the five minima labelled S1^TM6, S2^TM6, I1^TM6, I2^TM6, A^TM6, under five ligand/transducer conditions | line (drawn energy profile) | `SCHEMATIC \| free-energy profile of A2AR along a TM6 activation coordinate, five curves for apoprotein / +partial agonist / +full agonist / +G protein / +full agonist +G protein, with five labelled minima S1TM6 S2TM6 I1TM6 I2TM6 ATM6 \| no data` | 1 panel; 5 overlaid coloured curves (the condition is the legend dimension, shown as five colour-coded header labels) | **Yes, and this is the important one.** The figure is drawn *as if* quantitative — it has a "Free Energy" ordinate and an "Activation (TM6)" abscissa — but **neither axis carries units, ticks, or a single number**, and no curve is derived from data. The relative well depths, which are what a reader takes away about state populations, are **illustrative and not measured**. The barrier heights that *are* measured (∼7−15 kcal/mol, p.12) and the populations that *are* measured (section E.2) appear nowhere on it. Treat as a concept diagram, never as evidence | CC-BY 4.0, p.1; "figure inspired by ref 153" |
| 4 | 10 | **The state-inventory figure.** Membrane cartoons of the five functional TM6 states (S1, S2 inactive; I1, I2, A active-region) plus the +GTP forms of A^TM6 and I2^TM6, with a legend distinguishing ionic lock "on" / "off", agonist, GDP and GTP | schematic | `SCHEMATIC \| seven membrane-embedded receptor cartoons labelled S1TM6, S2TM6, I1TM6, ATM6, I2TM6, ATM6+GTP, I2TM6+GTP, showing G-protein engagement and ionic-lock status, with a four-item symbol legend \| no data` | 7 labelled cartoon states in a 2+3+2 arrangement, plus a legend block; states vary by conformation and by nucleotide/transducer occupancy | The ionic lock is drawn as a **binary on/off glyph**, which is exactly the simplification the body text (p.3) says is wrong — the same lock state occurs on both sides of the S1/S2 boundary and does not separate inactive from active. The figure and the text disagree in emphasis; the caption is where the nuance lives | CC-BY 4.0, p.1; "figure inspired by ref 153" |
| 5 | 19 | TM6 conformations through G-protein activation, mapped onto FRET level: a left-to-right strip of receptor−G cartoons banded as GDP-bound → nucleotide-free → GTP-bound, each labelled High / Int / Low / Int / High FRET | schematic | `SCHEMATIC \| seven receptor−Gαβγ cartoons in a horizontal strip banded by nucleotide state (GDP Bound / GTP Bound) and annotated with the FRET level each state gives (High, Int, Low, Int, High) \| no data` | 7 cartoons in one strip, grouped into 3 shaded bands; varies by nucleotide state and FRET level | The caption discloses the key weakness itself and it should be quoted whenever the figure is used: *"the low-FRET β2AR−Gs(GTP) complex was **deduced rather than seen experimentally**"* — one of the seven states shown is an inference, not an observation, and the figure does not distinguish it visually | CC-BY 4.0, p.1; "figure inspired by ref 97" |
| 6 | 19 | Agonist-facilitated G-protein coupling and GDP release, drawn as a branch: open inactive low-affinity R; agonist binding; the two routes to a closed active R\* with and without agonist (the lower branch is basal activity); ending in closed, active, high-affinity R\* with GDP released | schematic | `SCHEMATIC \| branching cartoon of receptor−Gαβγ states annotated "open, inactive, low affinity" / "closed, active" / "closed, active, high affinity", showing GDP release on both an agonist-driven and a basal-activity route \| no data` | 5 cartoon states on 2 branches (agonist-driven upper, constitutive lower) | | CC-BY 4.0, p.1; "figure inspired by ref 230" |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent
- **schema_version**: `v3`
- **confidence**: **high on content, medium on some attributions.** The PDF is a clean digital original; `pdftotext -layout` extracted the two-column body without loss, and every verbatim quote in `necessity_claims` was re-verified against a second, reading-order extraction (`pdftotext` without `-layout`) before being recorded, so no quote is a column-interleaving artefact. All six figures were checked: pages 4, 9, 10 and 19 were rendered at 150 dpi and read as images to establish panel counts and axis labelling (Figure 3's unlabelled axes and Figure 4's seven-state layout could not be recovered from the captions); Figure 1's caption enumerates its own panels A−D explicitly and was not rendered. What lowers confidence is **not** the reading but the source: the review's citation attributions are demonstrably imperfect (see `unresolved` 1), so any number in section E should be traced to its primary paper before it enters a manuscript.
- **unresolved**:
  1. **Verified citation mismatches in the review — the most important caveat in this note.** At least three attributions do not match the reference list.
     - **p.9**: *"This effect of Na+ ions on class A GPCRs conformation has been shown using **nMS by Robinson and collaborators in 2021**.⁵⁵"* — but **ref 55 is Wang, Neale, Kim, Goddard, Ye, *Nat. Commun.* 2023, "Intermediate-State-Trapped Mutants Pinpoint GPCR Conformational Allostery"** (p.29). Neither the authors, the year, nor the technique match.
     - **p.9**: *"as was shown by **Prosser and collaborators in 2018** using ¹⁹F solution NMR of A2AR in **MNG-3/CHS micelles**.¹⁵³"* — but **ref 153 is Huang, Pandey, Tran, … Sljoka, Prosser, *Cell* 2021**, which is the **lipid-nanodisc** study (p.31). The year and the membrane mimetic are both wrong in the sentence.
     - **p.13**: *"[¹⁵N,¹H] solution NMR experiments by **Wütrich and collaborators in 2018**¹⁸⁸ showed that this mutation altered the conformational dynamics…"* — **ref 188 is White, Stevens and collaborators 2018**, the UK432097−D52^2.50N A2AR crystal structure, cited two sentences earlier for a different claim.
     There are likely more. **Consequence: use this review to find the primary source, never as the citation of record for a specific number.**
  2. **No tag exists for a review / secondary source.** This is the one gap that matters. The v3 Method vocabulary is entirely composed of *methods a paper performs*; this paper performs none. I applied **`experimental`** because its v3 definition — *"marks a paper with no structure prediction in it at all, whose section C will be mostly NOT APPLICABLE by design rather than by sloppiness"* — is satisfied literally and describes this note's shape exactly. But **`experimental` also connotes wet-lab work the authors did**, which is false here, and a reverse lookup for "papers with lab data" will now return a review. A tag such as **`review`** or **`secondary-source`** is needed. Recorded, not invented.
  3. **No tag exists for "state-definition reference" / "structural-criteria source"**, which is this note's primary use. `background` and `comparator-numbers` between them approximate it but neither says "go here for the definition of an active state". Given that section C.1 is the deliverable, a tag like `state-criteria-reference` would earn its place.
  4. **Figure 3 sits exactly on the PLOT/SCHEMATIC boundary and the v3 grammar forces a lossy choice.** It has a measure (free energy), an independent axis (TM6 activation coordinate), a five-level series (ligand/transducer condition) and a mark (line) — every PLOT slot is fillable. But it carries **no measured data**: no units, no ticks, no values, and the curves are drawn. I chose `SCHEMATIC` per the rule ("anything carrying no measured data"), and recorded the quantitative structure in `hides` so it is not lost. The cost is real: a future query "what figure should I make for a free-energy landscape across five conditions?" will not join to this row, even though this figure is the answer. **Suggested v3.1 fix**: either allow a `SCHEMATIC` row to carry an optional `would_be:` slot holding the PLOT string it mimics, or add a sixth form (`ILLUSTRATIVE-PLOT`) for the drawn-as-if-quantitative case. Three of this review's six figures are diagrams of quantitative concepts, so the case is not rare.
  5. **`states_generated`, `state_metric` and `metric_saturation` are all mis-shaped for a review that *reports* criteria without applying them.** The v3 rubric asks what the paper *produced* and *measured*; the useful answer for a review is what it *documents*. I resolved this by putting the state-criteria tables inside `state_metric` — which is where they naturally belong, since state_metric is the "how is state called" field — but a schema note saying "for a review, `state_metric` holds the criteria the review collates" would prevent the next extractor solving it differently.
  6. **`controls_run` has the same shape problem** and I handled it the same way: `NOT APPLICABLE` for the authors, followed by an explicitly labelled table of the control arms the review reports from the primary literature. That table is reusable and would have been lost under a bare `NOT APPLICABLE`. Flagging it because the v3 changelog records that an extractor previously smuggled a control table into `stated_limits`; this is the mirror-image case and deserves a rule.
  7. **Page-number ambiguity is a live risk for anyone quoting from this note.** The journal paginates 3691−3728 while the PDF paginates 1−38. Every page reference here is a **PDF page**; convert with `journal = PDF + 3690`. If the corpus ever standardises on journal pages, this note needs a global re-map.
  8. **The state↔PDB mappings in table C.3 are the review's proposals, not measurements**, and the review hedges every one ("suggested", "might correspond", "may correspond"). They should never be quoted as established equivalences. The one exception is **I2^TM6 ≡ R291^7.56A A2AR (9EE8/9EE9/9EEA)**, which the review states flatly (p.10: *"It was shown that I2^TM6 for A2AR has the conformation determined for adenosine−A2AR−mini-Gαsβγ complex with receptor bearing the mutation R291^7.56A"*) on the basis of a structure solved for that purpose.
  9. **The review contains no discussion of structure prediction whatsoever.** "AlphaFold2" occurs exactly once in the entire 38-page PDF and only inside the *title* of reference 79 (the GPCRdb 2023 database paper); the body never mentions predicted models, and no ML method appears except in three further reference titles (GaMD + deep learning, refs 172/173). For a 2025 review of Class A conformational states this is a substantive absence and may itself be citable as evidence of the gap our work addresses — but it is an absence, so treat any use of it carefully.
  10. **Internal inconsistency in the review's own text at p.24**, which reads: *"While the formation of the agonist isoproterenol−β2AR−Gs^GDP complex takes a few seconds, the HRF-MS studies showed the very slow rate (2−3 h) … In contrast, the study found that it takes 2−3 h for releasing GDP and forming the more stable agonist−β2AR−Gs^empty."* The sentence states the same 2−3 h figure twice, the second time introduced by "In contrast". The **2−3 h** value itself is consistent with p.21 and is safe; the sentence construction is not, so quote from **p.21** rather than p.24.
  11. **Not determined: whether the numbers in section E.2 are directly comparable across studies.** Populations are drawn from different labels, different mimetics, different temperatures and different fitting models, and the review itself warns that the mimetic changes the answer (`stated_limits` 5). I have recorded each with its condition, but **no cross-study normalisation is possible from this paper alone.**
- **why_it_matters**:

## Tags

`gpcr` `experimental` `ensemble` `continuum` `ligand-driven` `partner-driven` `g-protein-mimetic` `nanobody` `orthosteric` `allosteric-site` `peer-reviewed` `background` `comparator-numbers`

Tag justifications, and — as importantly — what was deliberately **not** applied:

- **`gpcr`**: class A only, four receptors in depth (p.1).
- **`experimental`**: applied on the v3 letter of the definition — *"marks a paper with no structure prediction in it at all, whose section C will be mostly NOT APPLICABLE by design rather than by sloppiness"*. That is precisely this note's shape. **Applied under protest**: the connotation of wet-lab work performed by the authors is false, and the missing tag is `review` (see `unresolved` 2).
- **`ensemble` + `continuum`**: the review's central positive claim is a multistate ensemble — *"a multistate, rheostat-like model … instead of a binary (on/off) switch model"* (p.6) — with a landscape of many transient conformers (p.23). Both tags are needed: `ensemble` for the five named states, `continuum` because the review explicitly rejects a discrete-state reading and stresses that new intermediates keep appearing as techniques improve (Ix^TM6 p.11, I^TM7 p.13).
- **`ligand-driven`**: the efficacy ladder inverse agonist → antagonist → partial agonist → full agonist maps onto distinct populations throughout (pp.9, 15−16, 20−21).
- **`partner-driven`**: the review's load-bearing conclusion is that the transducer, not the agonist, closes the gap to the fully active state (`necessity_claims` 1−6). **This is the tag a query for "evidence that a partner is required" must return.**
- **`g-protein-mimetic`**: mini-Gs (a 21-residue Gαs C-terminal peptide is sufficient to shift populations, p.10), Gα C-terminal peptides, and Gs^empty are used as surrogates throughout.
- **`nanobody`**: Nb80, Nb6B9, Nb39 and Nb6 recur as the G-protein-mimetic handle in both structures and spectroscopy (pp.6, 16, 17, 20, 23).
- **`orthosteric`**: the OBS and its allosteric connection to the cytoplasmic face is the spine of the review (pp.2−3, 8).
- **`allosteric-site`**: substantively covered, not incidental — the Na⁺ pocket (D2.50) with amiloride/HMA/Fg754 (pp.3, 13), the PAM Cmpd-6FA site at the lipid interface of β2AR (pp.14−15), SBI-553 at NTS1R (p.6), cholesterol and PIP₂ sites (§6, pp.23), and the intracellular transducer cavity itself.
- **`peer-reviewed`**: ACS journal, dated review cycle Feb−Sep 2025 (p.1). Licence CC-BY 4.0, **no ND clause** (p.1).
- **`background`**: see `stance`. Provisional — the user's call.
- **`comparator-numbers`**: section E holds ~70 extracted values — TM6 displacement ranges, state populations, exchange rates, free-energy barriers — that a results table of ours could be placed beside. This is a principal reason to keep the note.

**Deliberately NOT applied, with reasons** (recorded because silence here would look like an oversight):
- **`md`, `enhanced-sampling`, `md-emulator`, `cofolding`, `msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`, `latent-steering`, `benchmark-only`** — the review *reports* MD, GaMD, metadynamics, REST, AWH and coarse-grained MD results but **performs none of them**. Tagging `md` would false-positive every "which papers ran simulations" query with a paper that ran nothing.
- **`no-template-no-msa`, `templates-on`, `state-annotated-input`** — no input regime exists.
- **`single-state`, `two-state`** — would invert the paper's thesis.
- **`binary-predicate`, `continuous-metric`, `rmsd-only`, `visual-metric`, `saturating-metric`** — the review applies no metric of its own. It *documents* both binary predicates (ionic lock formed/broken) and continuous ones (TM6 displacement), which is why the Metric family cannot express it; a metric tag here would misreport the review as having measured something.
- **`oracle-leak`, `design-level-oracle`, `prospective`, `anti-memorization`, `no-anti-memorization`, `unpowered`, `confidence-as-discriminator`, `multi-backbone`, `experimental-validation`** — every one of these presupposes a predictive pipeline. `no-anti-memorization` in particular would be technically true and semantically false: there is no model that could memorise anything. The v3 vocabulary still has no way to say **"this rigour axis does not exist for this paper"**, which the previous extractor of `tran2026nanogs` also flagged; this is now a second independent report of the same gap.
- **`directed-state`, `apo-sampling`, `seed-only`** — `directed-state` and `seed-only` describe a method's control handle and there is no method; `apo-sampling` describes sampling an apo receptor computationally, whereas the apo receptor here is characterised experimentally (and is, incidentally, one of the review's most important subjects — see `controls_run` row 1).
- **`cryptic-pocket`, `allosteric-failure`** — no cryptic pocket is the subject, and `allosteric-failure` is a *result* about sampling that no computation here produced.
- **`precedent`, `contrast`, `threat`, `negative-result`, `figure-exemplar`** — see `stance`. `figure-exemplar` was considered for Figures 3 and 4 (the CC-BY licence makes them freely redrawable and they are the clearest available depictions of the five-state model) but was rejected because that tag is defined as "kept **mainly** for its figures … must be excluded from gap analysis", and this note is kept mainly for its text.
