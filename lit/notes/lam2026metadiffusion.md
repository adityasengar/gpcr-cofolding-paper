# lam2026metadiffusion

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–24).** The PDF is
unpaginated (bioRxiv preprint, no printed page numbers anywhere), so PDF page = the only
page identifier. Layout: p1 abstract, p2–5 Introduction + Results, p6–7 Discussion, p7–9
Methods, p10 acknowledgements/code, p10–15 references, p15–16 funding, p17–21 main figure
captions with figures (Fig 1 p17, Fig 2 p18, Fig 3 p19 with caption continuing onto p20,
Fig 4 p20, Fig 5 p21), p22 Supplementary Table 1, p23 Supplementary Figure 1, p24
Supplementary Figure 2 + Supplementary File 1 legend.

**Pages rendered at 150 dpi and read directly:** 17, 18, 19, 20, 21, 23, 24. All seven
were necessary: the captions name panels but never give marks, axis variables, series
legends or in-panel numbers, and several of the paper's most important quantitative
results (the SAXS Wasserstein-1 values, the chemical-shift RMSD/MAE/R, the per-panel
RMSF means, the runtime table) exist **only as text printed inside figure panels** and
appear nowhere in the running text. Renders were written under `ocr/pages/` and deleted
after reading.

**Central mechanical fact for the corpus:** metadiffusion adds a gradient of a
user-defined potential **to the atomic coordinate displacement** at each denoising step
of a frozen Boltz-2. It does **not** touch the trunk, the pair representation, the MSA,
templates, or any internal embedding. See the `latent-steering` decision in the Tags
section — this paper is the reason that tag's definition needs revisiting.

**"Meta" here means metainference, not metadynamics.** Despite the name, **no
history-dependent bias accumulates**. There are no deposited hills, no time-accumulated
potential, no memory of visited CV values. The three energy forms (p8) depend only on
the *current* CV value, and the one Gaussian in the paper is a repulsion between
*concurrent samples in the same batch*, not between a trajectory and its own past. The
paper says the analogy is to metainference twice, explicitly (p3, p6).

---

## A. Identity

- **citekey**: `lam2026metadiffusion`
- **doi**: **bioRxiv 10.64898/2026.02.10.704873.** p1 header, verbatim: "bioRxiv preprint
  doi: https://doi.org/10.64898/2026.02.10.704873; this version posted February 11, 2026."
  No journal DOI anywhere in the 24 pages.
- **year**: **2026.** p1 header: "this version posted February 11, 2026".
- **venue**: **bioRxiv preprint. Explicitly not peer-reviewed.** p1 header, verbatim:
  "The copyright holder for this preprint (which was not certified by peer review) is the
  author/funder, who has granted bioRxiv a license to display the preprint in perpetuity.
  It is made available under a CC-BY 4.0 International license." No journal masthead, no
  received/accepted line, no submission statement. Tagged `preprint`, not `peer-reviewed`.
- **title**: "Metadiffusion: inference-time meta-energy biasing of biomolecular diffusion
  models" — p1.
- **authors**: Hilbert Yuen In Lam¹, Sebastián Pujalte Ojeda¹, Michaela Brezinova¹, Josef
  Hanke¹, Xing Er Ong, Yuguang Mu², Michele Vendruscolo^{1,*} (corresponding,
  mv245@cam.ac.uk) — p1. ¹ Centre for Misfolding Diseases, Yusuf Hamied Department of
  Chemistry, University of Cambridge, UK. ² School of Biological Sciences, Nanyang
  Technological University, Singapore. (Xing Er Ong carries no affiliation superscript in
  the author line as typeset.)
  **Self-citation note relevant to the central framing:** the metainference analogy that
  gives the method its name rests on the corresponding author's own work — ref 11 (Bonomi,
  Camilloni, Cavalli & Vendruscolo, *Sci. Adv.* 2016), invoked on p3 and p6. CamShift
  (ref 59, Kohlhoff … Vendruscolo 2009) and the ubiquitin ensemble (ref 37,
  Lindorff-Larsen … Vendruscolo 2005) are also the group's own.
  **Tooling disclosure, p10, verbatim:** "Claude Code (Opus 4.5 / Sonnet 4.5) was employed
  in the implementation of this work."

## B. Scope

- **system**: **General protein, dual with nucleic acid and protein–ligand.** This is not a
  single-family paper. The named systems span globins (*P. macrocephalus* myoglobin, p3/p18),
  lysozyme (T4 lysozyme, p4/p18), an O-methyltransferase (*S. drozdowiczii* MfnG, p3/p18), a
  small-molecule kinase (*E. coli* adenylate kinase, p4/p19), a periplasmic
  sialic-acid-binding protein (*H. influenzae* SiaP, p19), a penicillin-binding protein
  (*H. influenzae* dacB, p20), ubiquitin (p5/p24), a signalling complex (H-Ras / Raf-kinase
  RBD, p20), a serum carrier (human serum albumin, p20), a Ca²⁺ sensor (*H. sapiens*
  calmodulin, p5/p21), plus **pure-RNA and protein–nucleic-acid systems** (risdiplam–RNA
  duplex, p4/p19; class V GTP aptamer with GTP, p5/p21; Chlorella virus DNA ligase bound to
  DNA, p20) and **protein–ligand** cases (furosemide–HSA, p20). Abstract, p1: "enumeration of
  alternative binding poses across proteins, nucleic acids and ligands".
  **No GPCR and no transporter appears anywhere.** SiaP is the substrate-binding protein of
  a TRAP transporter (ref 62 title, p15: "SiaP, a Sialic Acid Binding Virulence Factor from
  *Haemophilus influenzae*"), which is a periplasmic binding protein, not a transporter.
  Raf appears **only as its Ras-binding domain**; no protein-kinase conformational state
  (DFG, αC) is studied anywhere — see the `kinase` tag note.

- **n_targets**: **269 total, and the number must be split three ways or it misleads.**
  - **13 named, individually-analysed systems**: myoglobin, T4 lysozyme, MfnG, *E. coli*
    adenylate kinase, risdiplam–RNA duplex (PDB 8R62), SiaP, dacB (PDB 3A3D), ubiquitin,
    H-Ras/Raf-RBD (PDB 4G0N), DNA ligase–DNA (PDB 2Q2U), furosemide–HSA, class V GTP
    aptamer–GTP, calmodulin.
  - **256 ATLAS proteins** for the single statistical result in the paper (RMSF correlation
    with MD), "256 randomly-selected structures covered by ATLAS" (p4).
  - **Every other result in the paper is n = 1 system.** Each of the 13 named systems
    carries exactly one demonstration; there is no second system anywhere that repeats a
    claim. The generality claim ("proteins, nucleic acids and ligands", p1;
    "model-agnostic", p3, p6) rests on 13 single-system vignettes plus one 256-protein
    correlation. **Worth flagging** per the schema note on single-system papers claiming
    generality.

- **method_class**: **Dual — `other` (inference-time gradient guidance on the diffusion
  coordinate trajectory) + `enhanced sampling` in framing, on a `co-folding` base.**
  - The mechanism is not in the schema's list: a differentiable meta-energy on a collective
    variable, differentiated w.r.t. the intermediate atomic coordinates, L2-normalised,
    clipped, scaled and **added to the denoiser's displacement vector**. No retraining, no
    fine-tuning, no MSA change, no template change.
  - The framing is enhanced sampling: the paper positions itself directly against
    metadynamics (p2: "enhanced sampling methods such as metadynamics where auxiliary
    potentials are introduced during simulations to push states into rarer, albeit
    physically plausible conformations") and against metainference (p3, p6).
  - The base engine is co-folding: Boltz-2 co-folds protein + ligand + nucleic acid, and
    Fig 4c/d is explicitly cofolding — p5: "a ligand can be biased which effectively allows
    Boltz-2 to co-fold the protein with a single ligand in different conformations in the
    same pocket".
  - It is **not** MD (no dynamics were run; the only force-field step is OpenMM energy
    *minimisation*, p8), and **not** an MD emulator (Boltz-2 is not trained on
    trajectories; BioEmu, which is, appears only as a comparator).

- **backbones**: **Boltz-2 only, for the method.** p7, verbatim: "Metadiffusion is
  implemented entirely through the addition of biases on top of Boltz-2 during denoising.
  As such, it relies entirely on Boltz-2's trunk and diffusion model with no additional
  training or fine-tuning of the base model."
  - **Comparator generator, not a metadiffusion backbone: BioEmu** (p9: "BioEmu conformers
    were generated using the Heun denoiser with 100 steps"), used once, in Fig 3a.
  - **AF3, OpenFold/OpenFold3, Chai-1 and IDPFold2 are named as compatible but were never
    run.** p6, verbatim: "Metadiffusion can be applied to other generative diffusion-based
    machine learning protein folding models such as AlphaFold3³, OpenFold^{38,39}, Chai-1⁴⁰,
    or IDPFold2⁴¹, without requiring any retraining or fine-tuning of these models." This is
    an **untested** portability claim; the word "in principle" appears in the preceding
    sentence. Not tagged `multi-backbone` — see Tags.

- **templates**: **NOT REPORTED.** The words "template" and "templates" do not appear in the
  24 pages (verified by full-text grep). Whether Boltz-2 was run with or without structural
  templates is never stated, in Methods (pp7–9) or anywhere else. This is a real gap: for a
  paper whose entire claim is that the *bias* moves the structure, whether a template was
  pinning the starting prior is load-bearing and unrecoverable from the PDF. "The exact
  biases and configurations used can be found in the code examples" (p7) pushes it to the
  GitHub repo.

- **msa_handling**: **NOT REPORTED.** MSAs are discussed only as *other people's* method
  (p2: "manipulation of the input multiple-sequence alignments (MSAs)^{15,16}"). The paper
  never states what MSA depth, source or setting its own Boltz-2 runs used. Presumably
  Boltz-2 defaults, but the paper does not say so and it must not be inferred. **Explicitly
  not subsampled and not state-filtered** — no MSA intervention of any kind is part of the
  method.

## C. Conformational core

- **states_generated**: **`ensemble`.** Every run produces a batch of samples and the paper's
  unit of analysis is the batch: n = 8 (SAXS aptamer, Rg minimisation arms), n = 16 (ATLAS
  per protein; calmodulin; each risdiplam strength condition), n = 128 (adenylate kinase;
  risdiplam total), n = 4,000 (BioEmu comparator), 2–128 (ubiquitin timing sweep). The
  abstract, p1: "metadiffusion generates diverse conformational ensembles".
  **Not dual.** There is no arm that collapses onto a single basin — the collapse this field
  usually catches is the opposite of this paper's failure mode. If anything the ensembles are
  too broad: Fig 3d, p19, prints mean RMSF 6.18 Å for metadiffusion against 1.06 Å for the
  matched MD, a ~5.8× over-spread on the same protein.
  **On populations and free energies — the paper claims neither, and says so.** p7, verbatim:
  "Thirdly, whilst metadiffusion is effective in generating diverse structures, **it does not
  inherently provide thermodynamic weighting.** Methods that use MD to further explore and
  thermodynamically weight the conformational space starting from generated structures as
  seeds may be helpful⁴⁶ to obtain free energy landscapes and potentially ligand binding
  paths^{47,48}." Full-text grep confirms the words "population", "Boltzmann" and
  "probability" appear nowhere in the paper, and "free energy" appears only in describing MD
  (p2) and in that disclaimer (p7). **This is the strong claim the paper deliberately does not
  make**, and the honesty is worth recording: the ensembles are conformational *hypotheses*
  (p6: "efficiently constructs physically-plausible conformational hypotheses"), unweighted.

- **structural_priors_used**: **Extensive, at design time, and not a defect.** Four distinct
  layers:
  1. **The pretrained model itself is the structural prior, and the paper says so as its
     central design principle.** p6, verbatim: "By leveraging the rich structural priors these
     models have learned from experimental data and combining them with gradient-based biasing
     through collective variables…". Fig 1a caption, p17: "…steered toward a user-defined
     objective **while remaining anchored to the learned structural prior of the model**." p6:
     "allowing ensembles to be generated with a learned structural prior rather than an
     explicit force field."
  2. **Deposited PDB entries chose and anchored every demonstration system.** 1AKE (AK closed,
     inhibitor-bound) and 4AKE (AK open), ref 28/29, p4 and p19; 6H76 (SiaP holo) and 2CEY
     (SiaP apo), plotted as reference markers in Fig 3c, p19; 3A3D (dacB native, the MD start
     structure), p20; 4G0N (Ras–Raf), p20; 2Q2U (DNA ligase–DNA), p20; 8R62 (risdiplam–RNA
     NMR ensemble, n = 14), p19; MfnG "from multiple crystal forms" (ref 26); T4 lysozyme's
     native Rg "approximately 16 Å" (ref 27, p4).
  3. **Prior structural knowledge defined a collective variable.** The MfnG hinge CV requires
     the user to nominate the regions and the vertex: Fig 2c caption, p18, verbatim:
     "Exploration of hinge angles in monomeric *S. drozdowiczii* MfnG **with steering regions
     and vertices defined with the different colour regions**, and the centroid of each
     differently coloured region used as the sides and vertex respectively for steering and
     calculation." The hinge is known to exist because of the crystal structure: p3, "the
     monomeric MfnG of *S. drozdowiczii*, **with the hinge which typically attaches to the
     other chain²⁶**". Same for Fig 4: which chain to align and which to bias is a decision
     made from knowing the complex.
  4. **Published experimental measurements as biasing targets** — SASBDB SASDWJ4 (GTP aptamer
     P(r)), SASBDB SASDJ64 (calmodulin P(r)), BMRB 51289 (calmodulin ¹³Cα/¹³Cβ shifts), p9 —
     and **ATLAS MD trajectories** (256 proteins, 100 ns, run in triplicate by ref 31) as the
     RMSF reference, p4. These are measurements/simulations, not deposited coordinates of a
     target state.

- **oracle_leakage**: **Pipeline is clean; the design is not. Route 7 present, route 5
  partially present in a descriptive and self-penalising form, routes 1/2/3/6 absent, route 4
  present-but-benign.** Enumerated separately:

  - **Route 1 — deposited structures as input or template: NONE FOUND.** No structure is fed
    to the model. The protocol is fully described on p7–8 and the only inputs to the bias are
    the intermediate coordinates the model itself produced: p7, verbatim: "Biases are
    introduced during the denoising process of the Boltz-2's diffusion model **into the atomic
    point cloud directly**… Biases are calculated using derivatives from CVs, and
    backpropagated into the atomic point cloud." Protocol page for checkability: **p7–8**.
    Caveat recorded honestly: the word "template" never appears in the paper (p7–9 Methods),
    so route 1 is *unstated* rather than *disproved*.
  - **Route 2 — state annotations from a curated database (GPCRdb / KLIFS / Kincore) driving
    templates or alignments: NONE FOUND.** No such database is named anywhere in the paper or
    in the 63 references. The curated resources used are SASBDB (scattering profiles, p9),
    BMRB (chemical shifts, p9) and ATLAS (MD trajectories, p4) — none of them state-annotated
    structure databases. Protocol page: **p9**.
  - **Route 3 — cluster labels derived from known states: NONE FOUND.** No clustering step
    exists in the method. Nothing is grouped, labelled or selected by state. Protocol page:
    **p7–9**.
  - **Route 4 — hyperparameters / sweep ranges / seeds / stopping criteria tuned against known
    states: PRESENT AS A SWEEP, BUT THE SELECTION CRITERION IS NOT A KNOWN STATE.** Two bias
    hyperparameters exist (strength k, and a "bias clip") and both are swept **on the
    evaluation systems**: seven strength/clip levels on the risdiplam–RNA duplex (Fig 3b, p19:
    "0.1, 0.5, 1.0, 2.0, 4.0, 8.0", n = 16 each), three levels on SiaP (Fig 3c, p19: "Strength
    = 1.0 / Bias clip = 1.0", "2.0/2.0", "3.0/3.0"), eleven target Rg values on T4 lysozyme
    (Supp Table 1, p22), and the ATLAS run is fixed at "strength=3 and bias clip=3" (p23, p24).
    The stated selection criterion is **physical plausibility and diversity, not proximity to a
    reference**: p4, verbatim: "**Therefore, tuning of the bias strengths is required to achieve
    both metadiffusion objectives whilst maintaining physically-plausible structures.**" And
    p7: "the method requires tuning of guidance weights and may be hyperparameter sensitive, at
    least in the implementation reported in this work."
    **The one place this shades toward leakage:** the SiaP sweep panels (Fig 3c, p19) plot the
    deposited holo (6H76) and apo (2CEY) structures as reference markers **on the very panels
    used to choose the strength**, and the caption's reading of the sweep is that stronger bias
    "allow[s] the method to push the model further away from its learned prior, thereby
    generating more diverse structures" (p19). The paper never states that a value was chosen
    by looking at those markers, and no such criterion is described. **Recorded as a route-4
    concern that the PDF cannot resolve either way**, not as demonstrated leakage.
    Seeds: never mentioned (grep confirms "seed" appears only at p7 in "generated structures as
    seeds" for a *future-work* MD suggestion). No stopping criterion is tuned; the bias is
    applied for a fixed fraction — p7: "Typically, the biases are applied for the first 70-90%
    of the denoising process".
  - **Route 5 — success defined post hoc by RMSD or TM to a structure they had: PARTIALLY
    PRESENT, AND IT REPORTS AGAINST ITSELF.** Fig 3a (p19) is a 2-D plot of "RMSD to 1AKE"
    against "RMSD to 4AKE" — a coordinate defined entirely by two deposited structures of the
    target states. But it is used as a *descriptive* axis, not a success criterion, and the
    reported outcome is negative: p4, verbatim: "Structures of different conformers of *E. coli*
    adenylate kinase were explored and compared with BioEmu and unbiased Boltz-2 demonstrating
    that metadiffusion can generate structures that are even more diverse. **However, the
    structures generated are further away from the reference inhibitor-bound closed and open
    states (PDB 1AKE²⁸ and 4AKE²⁹, respectively).**" Nowhere in the paper is a run called
    successful because it approached a held reference. Likewise the SiaP markers (Fig 3c) and
    the dacB MD comparison (Fig 3d) are reference overlays with no success threshold attached.
  - **Route 6 — best/worst model labels assigned against a held reference: NONE FOUND.** There
    is no model selection, ranking, filtering or "best-of-n" anywhere in the paper. Every
    reported number is an ensemble statistic over all generated samples (n = 8, 16, 128), and
    no confidence score is used to pick a representative. Protocol page: **p7–9**; confirmed by
    grep — "pLDDT", "pTM", "ipTM" and "confidence" do not appear in the paper.
  - **Route 7 — DESIGN-LEVEL ORACLE USE: PRESENT, AND IT IS THE paper's REAL EXPOSURE.
    Labelled design-level, not pipeline leakage.** Every demonstration system was chosen
    because the answer was already known, and in two cases the CV itself encodes that answer:
    - Adenylate kinase is the textbook open/closed pair and both states were in hand before
      the run (p4).
    - The MfnG hinge exists *because the crystal structures show it* — p3: "the monomeric MfnG
      of *S. drozdowiczii*, **with the hinge which typically attaches to the other chain²⁶**,
      can be effectively sampled across a wide range of angles". The user then hand-defines the
      hinge regions and vertex (Fig 2c, p18). **A collective variable that must be located by
      the user using prior structural knowledge of the system is route 7 by construction.**
    - T4 lysozyme's native Rg ("approximately 16 Å", p4, from ref 27) sets the centre of the
      steering sweep.
    - SiaP is presented as "the native state" (p19) while the panel carries its known apo and
      holo markers.
    - HSA is a protein famous for multiple drug-binding sites, chosen to demonstrate
      "different pockets" (p5, Fig 4d).
    - Calmodulin and the class V GTP aptamer were chosen because SAXS and NMR data for them
      are already deposited (p9).
    None of this is a methodological sin on its own — it is a demonstration paper — but the
    expected answer is declared before the result is read in every single case, and there is
    **no system anywhere in the paper where the outcome was unknown in advance**.

- **prospective**: **no — retrospective throughout, and the paper never claims otherwise.**
  Every system is a solved, deposited case; every experimental restraint (SASBDB SASDWJ4,
  SASDJ64, BMRB 51289) is a pre-existing published measurement; the MD comparator (ATLAS) is a
  published dataset. No prediction was made before an answer existed, and no new experiment or
  structure was produced. The word "prospective" does not appear in the paper. The one place a
  prospective reading could be argued — the furosemide–HSA alternative pockets (Fig 4d, p20) —
  is presented with no quantitative panel and no comparison to any known site, so it cannot be
  scored either way.

- **state_metric**: **Triple, and the third value is the rigour defect: `continuous
  coordinate` + `RMSD-to-reference` + `visual only`.** These co-exist in the same paper on
  different systems and forcing one would lose the interesting half.
  - **Continuous coordinate** — the dominant mode. Rg in Å (Fig 2b, p18, actual vs target);
    SASA in Å² (Fig 2a, p18); hinge angle in degrees (Fig 2c, p18); end-to-end distance in Å
    against Rg (Fig 3c, p19); pairwise RMSD in Å (Fig 3b, p19); Wasserstein-1 / Cramér distance
    on P(r) (Fig 5a/b, p21); Pearson R and Spearman ρ on RMSF (Fig 3e, p19); chemical-shift
    RMSD/MAE/R in ppm (Fig 5b, p21).
  - **RMSD-to-reference** — Fig 3a (p19), RMSD to 1AKE and to 4AKE, deposited references.
  - **Visual only** — **the whole of Figure 4 (p20)**. The claims "different poses of the
    H-Ras and Raf kinase RBD complex can be resolved" and "DNA ligases can be mapped to
    different binding conformations" and "different pockets" (all p5) are supported by
    structure renders and nothing else. There is no pose RMSD, no pocket identification, no
    count of distinct poses, no comparison to a crystallographic pose, and no scoring function.
    The state is called by eye. See `hides`, Fig 4.
  - **Exact thresholds recorded, with the justification gap:**
    - Peptide bond break: **C–N > 1.7 Å.** p8, verbatim: "Peptide bond breaks are defined by
      the C-N bond exceeding 1.7 Å." **No justification given for 1.7 Å.**
    - Steric clash: **heavy-atom pair distance < (sum of vdW radii − 0.4 Å)**, excluding same
      and adjacent residues of the same chain. p8–9: "For steric clash detection, all heavy
      atom pairs were considered, excluding those within the same or adjacent residues of the
      same chain. A clash was counted when the interatomic distance fell below the sum of the
      two van der Waals radii minus a 0.4 Å tolerance." **No justification given for the 0.4 Å
      tolerance.**
    - Bias application window: **first 70–90% of denoising steps**, p7. **NOT REPORTED which
      value was used for which system**; "Typically" is the only qualifier.
    - SAXS binning: **32 bins**, p9, justified — "to ensure that different SAXS profiles are
      divided similarly, and to prevent diminished gradients from too many bins."
    - **No threshold at all is defined for what counts as a distinct binding pose, a distinct
      pocket, or a successfully sampled state.**

- **metric_saturation**: **YES — a hard numeric ceiling on the paper's own control variable,
  stated in the text and visible in Fig 2b.** p3, verbatim: "The steering of the Rg was also
  achieved through the use of metadiffusion - the distance between the N- and C-terminus
  regions increased with specification of Rg, **although at conservative metadiffusion
  strengths the Rg capped at approximately 45 Å** (Fig. 2b). Higher strengths were able to
  force the Rg into further extrema, but at the cost of more unphysical structures
  (Supplementary Table 1)." The Fig 2b scatter (p18) runs the target axis to 70 Å while the
  achieved values flatten at ~44–45 Å from a target of ~45 Å onward — so the last third of the
  panel's x-range is a saturated plateau. This is genuine numeric saturation of the steering
  handle, not a plotting artefact.
  **Second, subtler ceiling:** the ¹³Cβ chemical-shift Pearson R is **already 0.97 in the
  unbiased arm** and reaches 0.99 after steering (p5) — a metric with only 0.02 of headroom.
  The Cβ result is therefore near-saturated at baseline and carries almost no discriminating
  power, while the Cα result (0.66 → 0.97) does. The paper reports the two side by side without
  noting the asymmetry.
  Cross-reference: Fig 2b's flat tail and Fig 3b's log-scaled y-axis are catalogued under
  `hides`, not duplicated here.

- **directional_control**: **YES, genuinely — but the target is a scalar CV value or an
  experimental curve, never a named conformational state.** This distinction is the whole
  answer for this paper.
  - **The handle is a differentiable collective variable and a target value for it.** p8,
    verbatim, defining the steering mode: "**Steering.** Steering biases the structure towards
    a user-defined value for a collective variable. It is calculated using a harmonic loss …
    where E is the final energy, k is the strength, and CV is the user-specified collective
    variable." Fig 1b caption, p17: "steering - in which the biases push structures toward a
    **user-defined value**".
  - **It demonstrably works over a range**: Fig 2b (p18) is an actual-Rg vs target-Rg scatter
    tracking the y = x diagonal from 10 Å to ~45 Å before saturating, with structure renders at
    Rg = 12, 16 (native) and 25 Å.
  - **Named handles, complete list:**
    1. **A target CV value** — Rg in Å, an inter-group distance, a dihedral, a hinge angle,
       SASA, shape gyration (p4: "a variety of other CVs can also be manipulated, including:
       distances, dihedral angles and shape gyration").
    2. **An experimental SAXS P(r) curve** — the target is the deposited pair-distance
       distribution, fitted by minimising the Cramér distance over 32 bins (p9).
    3. **An experimental NMR chemical-shift table** — ¹³Cα/¹³Cβ from BMRB, fitted by minimising
       a concordance-correlation-coefficient distance through a PyTorch CheShift-2 (p9).
    4. **A group/chain mask plus a Kabsch alignment group** — the spatial handle. p5, verbatim:
       "In doing the Kabsch alignment during the denoising process, the RMSD of the ligand can
       be calculated relative to one group (such as a chain) while aligned to another. By
       aligning one chain and applying biases solely to another, the relative binding poses
       between the two can be explored. **This is effectively holding one component fixed while
       sampling conformational diversity in the other.**"
    5. **Bias strength k and bias clip** — magnitude, not direction (Fig 3b/3c, p19).
    6. **Direction of optimisation** — minimise or maximise a CV without a target (p8).
  - **What it is NOT.** There is no way to say "produce the active state" or "produce the
    closed state". A conformational state can only be requested if someone first expresses it
    as a CV value, and doing so requires knowing the state. **On the one system where the
    method was pointed at a landscape with two known basins (adenylate kinase), the biased
    structures moved *further* from both** (p4). No partner, ligand, nanobody, peptide,
    state-annotated template, state-filtered MSA, subsample depth or seed is used as a handle
    anywhere in this paper.
  - **Prior structural knowledge is required for the interesting CVs.** Rg and SASA are
    global and need none. But the hinge-angle CV (Fig 2c, p18) and the align-one-chain /
    bias-the-other pose CV (Fig 4, p20) both require the user to nominate regions using
    knowledge of the structure. Recorded as **route 7** above.

- **anti_memorization_design**: **NONE.** There is no held-out set, no temporal split, no
  post-cutoff structure set, and no training-cutoff date is mentioned anywhere for Boltz-2 or
  for BioEmu. Full-text grep confirms "held-out", "cutoff" and "training set" do not appear.
  The 256 ATLAS proteins are randomly selected from a public MD database of PDB entries with no
  date filter (p4: "256 randomly-selected structures covered by ATLAS"). Every demonstration
  system is a long-deposited entry (1AKE 1992, 4AKE 1996, 2Q2U 2007, 3A3D 2010, 4G0N 2015).
  The paper is aware of the issue in the abstract sense — it cites the memorisation literature
  in the Discussion, p6, verbatim: "This is likely more pronounced in rarely-seen proteins -
  which previous work has shown that the models do not predict as well because they are
  out-of-distribution^{42,43}" (refs 42 = Škrinjar *et al.*, "Have protein-ligand cofolding
  methods moved beyond memorisation?"; 43 = FoldBench) — **but it converts that awareness into
  no experiment.**

- **anti_memorization_control**: **NONE RUN.** No arm of any kind tests whether the results
  depend on the base model having seen the target. The closest thing in the paper is the
  discussion sentence above (p6), which is a citation, not a control. Not marked `UNPOWERED`
  because there is no set to be underpowered — the design is simply absent.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| **Unbiased Boltz-2, run head-to-head in five separate places** (MfnG hinge-angle density, Fig 2c; adenylate kinase RMSD cloud, Fig 3a, n = 128; risdiplam pairwise RMSD, Fig 3b, n = 16; GTP-aptamer SAXS P(r), Fig 5a, n = 8; calmodulin SAXS P(r), Fig 5b, n = 16; runtime, Supp Fig 2) | That the diversity, the SAXS/NMR fit and the runtime cost come from Boltz-2 alone rather than from the bias. **This is the paper's single most important control and it is run consistently and with matched n.** | 18, 19, 21, 24 |
| **BioEmu, 4,000 conformers, Heun denoiser, 100 steps** (adenylate kinase only) | That the diversity is merely what any modern ensemble generator produces. Rules in a dedicated MD-trained emulator as the bar. **n is 31× the metadiffusion arm (4,000 vs 128) — see `hides`, Fig 3a.** | 19 (fig), 9 (method) |
| **ATLAS MD, 100 ns, 256 proteins** as the RMSF reference | That the generated fluctuation pattern is unrelated to physical flexibility. | 4, 19 |
| **MD-replicate-vs-MD-replicate correlation (ATLAS triplicates), Pearson R = 0.88** | **The best control in the paper.** It establishes a reproducibility ceiling, so the metadiffusion R = 0.81 can be read against what MD itself achieves rather than against 1.0. p4: "between the MD simulations themselves, an average Pearson's R of 0.88 was achieved, indicating that fluctuations from metadiffusion are close to the reproducibility ceiling." | 4, 19 |
| **Experimental NMR ensemble of the risdiplam–RNA duplex (PDB 8R62, n = 14)** plotted as a diversity arm alongside the generated ensembles | That the generated diversity is merely the diversity an experimental ensemble already shows. p4: "The generated structures controllably exceed the diversity generated resulting from NMR structural determination". | 19 |
| **Energy-minimisation before/after arm** (OpenMM 8.4, ff14SB, GB-Neck2 implicit solvent, H-bond constraints, PDBfixer hydrogens at pH 7.0) across 256 × 16 ATLAS structures | That the biased structures are physically broken. Peptide bond breaks 3.5 ± 4.8 → 0.0 ± 0.1; steric clashes 52.3 ± 81.9 → 5.3 ± 6.0. | 8, 23 |
| **Energy minimisation applied to the Rg-steering extremes (n = 8 each)** | That the *steered* Rg survives relaxation. It partly does not: over-compact 9.55 ± 0.03 → 14.1 ± 0.1 Å (a 48% rebound); over-extended 43.9 ± 1.5 → 42.6 ± 1.5 Å (holds). **An honest, self-penalising control.** | 4 |
| **Target-Rg sweep, 11 levels (10–45 Å), quality scored before and after minimisation** | That a single Rg setting was cherry-picked; maps the strength/plausibility trade-off across the whole range. Steric clashes fall 4,602 → 0.0 as Rg rises; bond breaks rise 0.0 → 21.0. | 22 |
| **Bias strength/clip sweep, 7 levels (0.1–8.0), n = 16 each** (risdiplam–RNA) and **3 levels (1.0/2.0/3.0)** (SiaP) | That diversity is a threshold artefact rather than a monotone, controllable response. p4: "The diversity of structures also scales monotonically to the strength of bias applied in both protein and nucleic acid regimes". | 19 |
| **Orthogonal SASA implementation** — biased with the LCPO algorithm, *reported* with BioPython 1.84 `PDB.SASA` | That the SASA change is an artefact of the differentiable estimator used to compute the gradient. p9, verbatim: "the SASA reported in the results calculated using the BioPython 1.84 PDB.SASA module **for orthogonality**". **A genuinely good control and the kind most papers skip.** | 9 |
| **Automatic chemical-shift offset** between mean experimental and mean CheShift-2 shifts, recomputed at every biasing iteration | That the shift agreement is a reference-frame artefact (CheShift-2 DFT frame vs experimental DSS frame). Offsets printed in-panel: +2.25 ppm (Cα), +1.28 ppm (Cβ). | 9, 21 |
| **Deposited apo/holo reference markers overlaid on the SiaP sweep (6H76 holo, 2CEY apo) and on the AK plot (1AKE, 4AKE)** | Not a control arm — reference points for orientation. Recorded because they are the route-4/route-5 contact surface. | 19 |
| **Runtime control: unbiased Boltz-2 timed at every ensemble size** (2–128 samples, ubiquitin, RTX 3090) | That the O(N²) cost claim is asserted rather than measured. | 24 |

  **Controls conspicuously NOT run:** no scrambled/decoy CV arm (biasing toward a nonsense
  target); no random-direction bias of matched magnitude; no repeat of any single-system result
  on a second system; no accuracy control asking whether a *steered* structure is closer to a
  known target state than the unbiased baseline (the only such test, adenylate kinase, went the
  wrong way and is reported as such); no held-out/post-cutoff arm; no ablation of the twice-per-
  step bias evaluation or of the 70–90% window.

- **confidence_as_discriminator**: **NO — not used at all, and not validated.** pLDDT, pTM and
  ipTM appear nowhere in the 24 pages (full-text grep). No model is selected, ranked or filtered
  by any confidence score; every reported statistic is over the full generated ensemble. Boltz-2's
  confidence head is simply never invoked. Recorded as a clean absence rather than a defect —
  but it also means the paper offers **no internal signal for whether a biased structure is
  trustworthy**, which matters given that its own quality control (bond breaks, clashes) is an
  external geometric check applied after the fact.

## D. Claims

- **central_conclusion**: A differentiable meta-energy defined on a user-chosen collective
  variable, differentiated with respect to the intermediate atomic coordinates and added to the
  denoiser's displacement vector at each step of a **frozen** Boltz-2, converts a single-structure
  co-folding model into a controllable ensemble generator — supporting three bias forms
  (optimise a CV, steer to a target CV value, repel concurrent samples apart) — with no
  retraining. The resulting ensembles reproduce MD's per-residue flexibility *pattern* (Pearson
  R = 0.81 over 256 ATLAS proteins, against an MD-replicate ceiling of 0.88) though not its
  *magnitude* (R = 0.65 on mean RMSF, and ~5.8× over-spread on the one worked example), and can
  be fitted to deposited SAXS P(r) and NMR chemical shifts far better than unbiased Boltz-2. The
  ensembles carry **no thermodynamic weighting**, which the authors state explicitly.

- **necessity_claims** (verbatim, with page):
  1. p2: "AlphaFold3 and Boltz-2, on their own, however, **are not well-suited** to predict a
     diverse ensemble of structures, as they were trained on native structures in the Protein
     Data Bank (PDB)13."
  2. p2: "While effective in certain settings, these approaches **often require task-specific
     adaptation, and provide limited control** in driving structures towards experimental
     observables at inference time."
  3. p4: "Therefore, **tuning of the bias strengths is required** to achieve both metadiffusion
     objectives whilst maintaining physically-plausible structures."
  4. p6: "The development of diffusion-based structure prediction models represents a major
     advance in structural biology, yet their focus on single, compact conformations inherited
     from crystallographic training data **leaves conformational dynamics largely unaddressed**."
  5. p6: "The base model captures the biomolecular distributions in a way that might be hard to
     model with force fields and traditional methods, but similarly **may be unsuitable in cases
     which are less represented in its training data**."
  6. p7: "First, **the method requires tuning of guidance weights and may be hyperparameter
     sensitive**, at least in the implementation reported in this work."
  7. p7: "Secondly, **the structures generated are fundamentally limited by the expressivity of
     the base model**, as diffusion biases can be argued as compromising the fidelity of the
     learned prior44,45."
  8. p7: "Thirdly, whilst metadiffusion is effective in generating diverse structures, **it does
     not inherently provide thermodynamic weighting**."
  9. p7: "Lastly, for heterogeneous systems such as disordered proteins, since the conformational
     landscapes are vast and training data sparse, **the utility of metadiffusion may be
     constrained** until base models are better able to represent these systems."
  10. p9: "CamShift59, the default method in PLUMED 260, **was not used as contributions from
      hydrogens would be necessary**, and Boltz-2 does not generate hydrogens in its denoising
      process."
  11. p9 (SAXS): "Since Boltz-2 does not generate hydrogens in its diffusion process, these are
      ignored in the pairwise calculation."

- **novelty_claims** (verbatim, with page). **Note first: the paper makes NO "first" claim
  anywhere** — the words "first to", "novel", "unprecedented" and "for the first time" do not
  appear. It positions itself as a *unification* of named prior work (refs 18–25: particle
  guidance, Richman *et al.* 2025 inference-time landscapes, Maddipatla *et al.* 2025
  experiment-guided AF, Nam *et al.* 2025 CV-guided molecular diffusion, idpSAM, ExEnDiff,
  universal guidance). That restraint is itself worth recording for any priority question.
  1. p1 (abstract): "**This work introduces metadiffusion**, where an additional meta-energy
     biasing layer on top of diffusion steers pretrained biomolecular diffusion models through
     gradient-guided denoising."
  2. p1 (abstract): "Metadiffusion thus **provides a practical route to connect** diffusion-based
     structure generation with ensemble-level, experimentally-restrained structural analysis."
  3. p3: "**Metadiffusion unifies these directions** by defining a meta-energy that encodes
     collective-variable objectives and applying its gradients as additional updates during
     diffusion denoising."
  4. p3: "Metadiffusion operates directly on pretrained biomolecular diffusion models without
     retraining or fine-tuning, **bringing together ideas from enhanced sampling, experimental
     ensemble refinement and score-guided diffusion within a single, composable inference-time
     framework**. **This positions metadiffusion as a general, model-agnostic approach** for
     generating diverse, experiment-consistent conformational ensembles."
  5. p6: "This approach positions conformational ensemble generation **not as a separate modeling
     task requiring specialised training, but as a controllable property of inference** that can
     be adapted to experimental constraints and mechanistic questions on demand7."
  6. p6: "Because metadiffusion applies inference-time meta-energy guidance to pretrained
     biomolecular diffusion models, **it is model-agnostic in principle**."
  7. p6: "**A key advantage of metadiffusion is its ability to generate rare, metastable states at
     low computational cost, orders of magnitude faster than microsecond-scale MD simulations.**"
     (Note: this is asserted; the only timing benchmark is ubiquitin at 76 residues, Supp Fig 2,
     and no microsecond-scale MD was run for comparison.)
  8. p7: "Overall, **metadiffusion occupies an intermediate space between a physics-driven and
     data-driven generative modelling**."

- **stated_limits** (the authors' own, all p6–7, and unusually candid):
  1. Hyperparameter sensitivity and required tuning of guidance weights (p7, quote 6 above).
  2. Ceiling set by base-model expressivity; biases may compromise the fidelity of the learned
     prior (p7, quote 7).
  3. **No thermodynamic weighting** — no free energies, no populations (p7, quote 8).
  4. Poor prospects for disordered/heterogeneous systems until base models improve (p7, quote 9).
  5. Base model unreliable for rarely-seen, out-of-distribution proteins (p6, quote 5).
  6. High bias or too few unbiased relaxation steps causes bond breaks and steric clashes
     (p4): "high biases and/or disallowing Boltz-2 sufficient iterations to relax the structure
     unbiased can result in an increased number of bond breakages and steric clashes."
  7. Energy minimisation shifts the very Rg that was steered (p4, the 9.55 → 14.1 Å rebound).
  8. Rg saturates at ~45 Å at conservative strengths (p3).
  9. Cost is O(N²) for the pairwise-RMSD CV; SAXS and NMR CVs are slow (p5).
  10. The SAXS implementation approximates electron scattering by interatomic distances and
      ignores hydrogens (p9).
  **Not stated by the authors, but visible in their own figures:** the ~5.8× RMSF magnitude
  inflation (6.18 Å vs 1.06 Å, Fig 3d, p19) is printed in the panel and never mentioned in the
  text; and the adenylate-kinase result — biased structures further from *both* known states —
  is reported in one sentence (p4) and never returned to.

- **stance**: **`precedent` on mechanism + `contrast` on rigour. Provisional — the user's call.**
  - **Precedent (strong).** This is the cleanest general statement of inference-time
    energy-biased guidance on a biomolecular diffusion trajectory in the corpus: frozen model,
    gradient added to the coordinate update, three composable bias forms, no retraining, applied
    across protein / nucleic acid / ligand. Any claim that a diffusion structure generator can be
    steered at inference without touching its weights is anticipated here in its most general
    form, and the paper explicitly claims the model-agnostic generalisation (p3, p6).
  - **Contrast (on rigour).** Thirteen single-system vignettes; one statistical result (n = 256);
    no accuracy test that a steered structure lands closer to a target state than the unbiased
    baseline — and the one place that was measurable, it went the wrong way (p4); Figure 4's
    entire binding-pose claim has no quantitative panel; no held-out or post-cutoff arm; template
    and MSA settings unreported; portability to AF3/Chai-1/OpenFold asserted but never run.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Mean Pearson R, per-residue Cα RMSF, metadiffusion vs MD | **0.81** | correlation | ATLAS 100 ns MD, n = 256 proteins × 16 structures | 4, 19 (Fig 3e) |
| Mean Pearson R, MD replicate vs MD replicate (**reproducibility ceiling**) | **0.88** | correlation | ATLAS triplicate MD, n = 256 | 4, 19 (Fig 3e) |
| Mean Spearman ρ, per-residue RMSF, metadiffusion vs MD | **0.77** | correlation | ATLAS MD, n = 256 | 19 (Fig 3e, in-panel) |
| Mean Spearman ρ, MD vs MD (ceiling) | **0.87** | correlation | ATLAS triplicate MD, n = 256 | 19 (Fig 3e, in-panel) |
| Pearson R, **mean RMSF per protein** (magnitude, not pattern) | **0.65** | correlation | ATLAS MD, n = 256 | 4 |
| Worked example (dacB, 3A3D), Pearson r with MD | **0.815** | correlation | ATLAS MD of same protein | 19 (Fig 3d, in-panel) |
| Worked example (dacB), Pearson r **within** MD replicates | **0.882 ± 0.118** | correlation | ATLAS MD replicates | 19 (Fig 3d, in-panel) |
| Worked example (dacB), mean RMSF — **metadiffusion** | **6.18** | Å | — | 19 (Fig 3d, in-panel) |
| Worked example (dacB), mean RMSF — **MD** | **1.06** | Å | — | 19 (Fig 3d, in-panel) |
| **RMSF magnitude ratio, metadiffusion : MD** (derived from the two rows above) | **≈5.8×** | ratio | ATLAS MD, same protein | 19 |
| SAXS Wasserstein-1 distance, **unbiased Boltz-2**, class V GTP aptamer + GTP | **7.67** | Å | experimental P(r), SASBDB SASDWJ4 | 21 (Fig 5a, in-panel) |
| SAXS Wasserstein-1 distance, **metadiffusion**, class V GTP aptamer + GTP | **0.11** | Å | experimental P(r), SASBDB SASDWJ4 | 21 (Fig 5a, in-panel) |
| SAXS Wasserstein-1 distance, **unbiased Boltz-2**, calmodulin | **9.64** | Å | experimental P(r), SASBDB SASDJ64 | 21 (Fig 5b, in-panel) |
| SAXS Wasserstein-1 distance, **metadiffusion**, calmodulin | **0.26** | Å | experimental P(r), SASBDB SASDJ64 | 21 (Fig 5b, in-panel) |
| ¹³Cα chemical-shift Pearson R, unbiased → steered | **0.66 → 0.97** | correlation | BMRB 51289, n = 16 | 5 |
| ¹³Cβ chemical-shift Pearson R, unbiased → steered | **0.97 → 0.99** | correlation | BMRB 51289, n = 16 | 5 |
| ¹³Cα chemical shift, steered: RMSD / MAE / R | **1.15 / 0.91 / 0.971** | ppm / ppm / correlation | BMRB 51289, n = 16 | 21 (Fig 5b, in-panel) |
| ¹³Cβ chemical shift, steered: RMSD / MAE / R | **1.04 / 0.80 / 0.997** | ppm / ppm / correlation | BMRB 51289, n = 16 | 21 (Fig 5b, in-panel) |
| Applied chemical-shift offset (CheShift-2 DFT frame → DSS) Cα / Cβ | **+2.25 / +1.28** | ppm | mean experimental − mean calculated | 21 (Fig 5b, in-panel) |
| Steric-clash reduction after energy minimisation, ATLAS set | **89.9%** | reduction | 256 × 16 structures, pre- vs post-minimisation | 5 |
| Peptide bond breaks, ATLAS set, before → after minimisation | **3.5 ± 4.8 → 0.0 ± 0.1** | count per structure | ff14SB / GB-Neck2 minimisation | 23 (Supp Fig 1, in-panel) |
| Steric clashes, ATLAS set, before → after minimisation | **52.3 ± 81.9 → 5.3 ± 6.0** | count per structure | ff14SB / GB-Neck2 minimisation | 23 (Supp Fig 1, in-panel) |
| Rg rebound after minimisation, over-compact T4 lysozyme arm | **9.55 ± 0.03 → 14.1 ± 0.1** (n = 8) | Å | native Rg ≈ 16 Å | 4 |
| Rg after minimisation, over-extended T4 lysozyme arm | **43.9 ± 1.5 → 42.6 ± 1.5** (n = 8) | Å | native Rg ≈ 16 Å | 4 |
| Rg steering ceiling at conservative strengths | **≈45** | Å | target Rg up to ~70 Å on the axis | 3, 18 (Fig 2b) |
| Steric clashes vs target Rg (10 → 45 Å), before minimisation | **4,602.0 ± 119.0 → 0.0 ± 0.0** | count | 11-level target-Rg sweep | 22 (Supp Table 1) |
| Peptide bond breaks vs target Rg (10 → 45 Å), before minimisation | **0.0 ± 0.0 → 21.0 ± 7.7** | count | 11-level target-Rg sweep | 22 (Supp Table 1) |
| Myoglobin SASA: minimised / default / maximised | **7,541 / 7,948 / 10,179** | Å² | BioPython `PDB.SASA` (orthogonal to the LCPO CV) | 18 (Fig 2a, in-panel) |
| MfnG hinge angles, unbiased Boltz-2 (3 shown) | **116.25 / 117.77 / 118.02** | degrees | centroid-defined hinge CV | 18 (Fig 2c, in-panel) |
| MfnG hinge angles, metadiffusion exploration (3 shown) | **87.99 / 110.09 / 145.31** | degrees | centroid-defined hinge CV | 18 (Fig 2c, in-panel) |
| Runtime, ubiquitin (76 aa), **Boltz-2** at n = 2/4/8/16/32/64/128 samples | **32 / 32 / 37 / 48 / 69 / 122 / 265** | s | Nvidia RTX 3090 | 24 (Supp Fig 2, in-panel) |
| Runtime, ubiquitin (76 aa), **metadiffusion (max pairwise RMSD)** at the same n | **32 / 34 / 43 / 72 / 168 / 515 / 1,915** | s | Nvidia RTX 3090 | 24 (Supp Fig 2, in-panel) |
| Runtime ratio at n = 128 (derived) | **≈7.2×** | ratio | metadiffusion : unbiased Boltz-2 | 24 |
| Computational complexity, pairwise-RMSD CV | **O(N²)** | — | N = number of samples | 5 |
| Computational complexity, Rg / distance CVs | **O(N)** | — | N = number of samples | 5 |
| Pairwise RMSD vs bias strength, risdiplam–RNA (7 conditions + NMR + Boltz-2) | **~0.2 → ~11** (read from a log axis; no numeric labels) | Å | NMR ensemble 8R62 (n = 14) and unbiased Boltz-2 (n = 16) | 19 (Fig 3b) |
| Bias application window | **first 70–90%** of denoising steps | % of trajectory | — | 7 |
| Peptide-bond-break threshold | **> 1.7** | Å (C–N) | — | 8 |
| Steric-clash threshold | **sum of vdW radii − 0.4** | Å | heavy-atom pairs, excluding same/adjacent residues | 8–9 |
| SAXS P(r) binning | **32** | bins | — | 9 |

  **Consistency flag for anyone quoting these:** the running text and the Fig 5 panels call the
  SAXS agreement metric **"Wasserstein-1" / D_W1** (p5, p21), while Methods states the quantity
  actually minimised is the **Cramér distance** (p9), citing Bellemare *et al.* (ref 54, a paper
  titled "The Cramer Distance as a Solution to Biased Wasserstein Gradients"). These are related
  but not identical. Quote the number with the label the figure uses and note the discrepancy.
  **Second flag:** the p5 sentence "Pearson's R in 13Cα increased from 0.66 to 0.97 and 13Cβ
  increased from 0.97 to 0.99 for n = 16 structures **with and without SAXS steering**
  respectively" is garbled — the arms are unbiased vs steered, and the ordering of "with and
  without" contradicts the direction of the improvement. The Fig 5b in-panel numbers (R = 0.971,
  0.997) confirm the steered arm is the high one.

- **n_predictions**: **Recorded separately — a single total would be meaningless here.**
  - **Samples per target, by experiment:** 128 (adenylate kinase, metadiffusion); 128 (adenylate
    kinase, unbiased Boltz-2); 4,000 (adenylate kinase, BioEmu comparator); 16 per condition ×
    8 conditions = 128 (risdiplam–RNA strength sweep, p19); 16 per protein (ATLAS); 8 (GTP
    aptamer, metadiffusion) + 8 (unbiased); 16 (calmodulin, metadiffusion) + 16 (unbiased); 8 per
    target-Rg level (T4 lysozyme minimisation arms); 2–128 (ubiquitin timing sweep); **n = 1
    shown** for the myoglobin SASA panel and for each Fig 4 pose render.
  - **Targets:** 269 (13 named + 256 ATLAS). Only the 256-protein ATLAS arm is statistical;
    every other result is n = 1 target.
  - **Total metadiffusion structures generated (lower bound, as reported):** 256 × 16 = **4,096**
    (ATLAS) + 128 (AK) + 128 (risdiplam) + 8 (aptamer) + 16 (calmodulin) + 88 (11 Rg levels × 8)
    + 254 (timing sweep, 2+4+…+128) ≈ **4,718**, plus the unquantified Fig 2 and Fig 4 runs.
  - **Comparator structures:** 4,000 (BioEmu) + 128 (unbiased Boltz-2, AK) + 16 (unbiased,
    risdiplam) + 8 + 16 (unbiased SAXS arms) + 254 (unbiased timing sweep).
  - **Experimental reference ensemble:** n = 14 (PDB 8R62 NMR models).

- **comparable_to_ours**: *(left empty by the extractor per schema v3)*

- **si_in_scope**: **Partially held — one item is missing and it is the one holding the
  per-protein numbers.**
  - **Held, in this PDF:** Supplementary Table 1 (p22, the 11-level target-Rg quality sweep, with
    means ± SD), Supplementary Figure 1 (p23, before/after minimisation quality, with in-panel
    summary statistics), Supplementary Figure 2 (p24, runtime bar chart with every bar labelled).
    All three carry usable numbers and are transcribed into `metrics_reported` above.
  - **SI NOT HELD — Supplementary File 1.** p24 legend: "Supplementary File 1. ATLAS trajectory
    IDs used to calculate correlation with metadiffusion and individual Pearson R values. RMSD
    biases were calculated with strength=3 and bias clip=3." Also referenced at p4: "The exact
    Pearson's R correlation metrics and protein identities selected from the ATLAS dataset are
    available in Supplementary File 1." **This means the 256 per-protein Pearson R values — the
    only distribution behind the paper's only statistical claim — are not in the corpus.** Only
    the mean (0.81), the box plot (Fig 3e) and the ceiling (0.88) are recoverable. Any re-analysis
    of the RMSF result requires fetching that file.
  - **Also outside the PDF:** all bias configurations. p7, verbatim: "The exact biases and
    configurations used can be found in the code examples" — i.e. in the GitHub repo
    (https://github.com/Chokyotager/Boltz-Metadiffusion, p10), not in the paper. Per-system
    strength, clip and window values are therefore **NOT REPORTED** in the PDF except for the
    ATLAS run (strength = 3, clip = 3) and the sweep levels shown in Fig 3b/3c.

## F. Figures

One row per panel group. Splits are on `mark` or `measure`, never on `facet` alone. Letters
appearing in two rows are noted in `panels`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| **1A–D** | 17 | The whole mechanism: denoising row with bias arrows injected between steps; three cartoon densities naming the optimise / steer / explore modes; an illustrative P(r) curve and an illustrative NMR spectrum captioned as the SAXS and chemical-shift fitting objectives. | schematic | `SCHEMATIC \| denoising trajectory with per-step gradient injection, plus three CV-density cartoons and two illustrative experimental-observable traces \| no data` | 4 panels (A: 6 sub-boxes in two rows, denoised and biased; B: 3 density cartoons; C: 1 P(r) sketch + a scattering-pattern inset; D: 1 spectrum sketch + a tryptophan structure). **Every curve in B, C and D is drawn, not measured** — no axis carries numbers. | | CC-BY 4.0, **no ND clause**. Redrawing and modification both permitted with attribution. License stated in the header of every page, p1–24. |
| **2A + 2B(left) + 2C(left)** | 18 | Structure renders carrying the CV results as printed annotations: myoglobin at minimised / default / maximised SASA; T4 lysozyme cartoons at Rg = 12, 16 (native), 25 Å; MfnG monomer under default Boltz-2 vs metadiffusion exploration with per-conformer hinge angles labelled. | structure render | `RENDER \| facet: CV demonstration (3: SASA optimisation, Rg steering, hinge exploration) \| views: 1 (single camera angle per sub-image; 2C's two sub-images are overlays of many conformers) \| overlay: NOT REPORTED predictions on 0 reference(s) \| axis: none` | 3 panels contributing renders (A: 3 renders; B-left: 4 cartoons; C-left: 2 overlay renders). Panels **B and C each also appear in a plot row below**. | **2A carries the SASA claim on n = 1 structure per condition with no distribution** — three numbers (7,541 / 7,948 / 10,179 Å²) with no spread, no repeat and no n stated. **2C's angle labels are 3 hand-picked conformers out of an ensemble**, with no indication of how they were selected. | CC-BY 4.0, no ND. p18. |
| **2B** | 18 | Achieved Rg plotted against requested Rg for the steering mode, with a y = x guide — the paper's only direct demonstration that directional control works, and its saturation. | scatter | `PLOT \| facet: none (1) \| vary: target Rg, 0–70 Å (continuous) \| series: none (1) \| measure: actual Rg (Å) \| mark: point \| n: NOT REPORTED per mark, ~13 points per panel` | 1 plot panel (the right half of panel B; B's left half is in the render row above). | **n behind each point is never stated** — each is presumably a mean over an ensemble but no error bar is drawn. The x-axis extends to 70 Å while the achieved values plateau at ~45 Å from ~45 Å onward, so **the last third of the panel is a flat, unlabelled saturation** that the caption does not mention (it is stated in the running text, p3). | CC-BY 4.0, no ND. p18. |
| **2C** | 18 | Hinge-angle distributions, unbiased Boltz-2 vs metadiffusion exploration, on the same axis — the sharp red spike versus the broad blue shelf is the clearest single image of what the exploration mode does. | line (filled KDE) | `PLOT \| facet: none (1) \| vary: hinge angle, 40–180 degrees (continuous) \| series: method (2: Boltz-2, metadiffusion) \| measure: density \| mark: line \| n: NOT REPORTED per curve` | 1 plot panel (right of panel C; C's left half is in the render row). | **n behind each KDE is never given** — neither in the caption nor the text. A density estimate whose sample size is unstated cannot be assessed. | CC-BY 4.0, no ND. p18. |
| **3A** | 19 | Adenylate kinase conformers in the (RMSD-to-1AKE, RMSD-to-4AKE) plane, three generators overlaid as KDE contours with the metadiffusion samples also drawn as points; dashed guides at 7.5 Å; two structure renders alongside. | scatter + contour | `PLOT \| facet: none (1) \| vary: RMSD to 1AKE (closed), 0–20 Å (continuous) \| series: generator (3: Boltz-2, BioEmu, metadiffusion) \| measure: RMSD to 4AKE (open) (Å) \| mark: point + contour \| n: 1 per point; 128 (metadiffusion), 128 (Boltz-2), 4,000 (BioEmu) per panel` | 1 plot panel + 2 accompanying renders (the renders carry no data and are not split out — they illustrate two metadiffusion conformers). | **Three KDEs with wildly unequal n (4,000 vs 128 vs 128) are overlaid as if comparable** — contour density is n-dependent and the visual impression of BioEmu's tightness is partly a sample-size artefact. **The two dashed guides at 7.5 Å are unlabelled and unexplained** in caption and text. The panel's actual finding — metadiffusion is further from *both* references — is legible only if the reader knows the axes are distances to the two answers. | CC-BY 4.0, no ND. p19. |
| **3B** | 19 | Pairwise RMSD between generated structures across seven bias strength/clip settings, benchmarked against an experimental NMR ensemble and unbiased Boltz-2; an overlay render of the RNA duplex alongside. | box | `PLOT \| facet: none (1) \| vary: arm (8: NMR, Boltz-2, strength/clip 0.1, 0.5, 1.0, 2.0, 4.0, 8.0) \| series: none (1) \| measure: pairwise RMSD (Å, log scale) \| mark: box (with all points overlaid) \| n: n = 14 (NMR arm), n = 16 (each of the other 7 arms), stated under every box` | 1 plot panel + 1 accompanying overlay render (PDB 8R62). | **Log y-axis with only two decade ticks (10⁻¹, 10¹) and no numeric labels on any box** — the monotone-scaling claim (p4) can be read as a trend but no value can be extracted. **The NMR arm (n = 14 deposited models) is placed on the same axis as generated ensembles** without noting that experimental model spread and generative spread are not the same quantity, yet the paper's claim that it "controllably exceed[s] the diversity … from NMR structural determination" (p4) rests on exactly that comparison. | CC-BY 4.0, no ND. p19. |
| **3C** | 19 | SiaP conformers in the (end-to-end distance, Rg) plane at three strength/clip settings, each panel carrying the deposited holo (6H76) and apo (2CEY) structures as reference markers; an overlay render alongside. | scatter + contour | `PLOT \| facet: strength/clip setting (3: 1.0/1.0, 2.0/2.0, 3.0/3.0) \| vary: end-to-end distance, 30–57 Å (continuous) \| series: point class (3: generated conformer, 6H76 holo, 2CEY apo) \| measure: Rg (Å) \| mark: point + contour \| n: 1 per point, NOT REPORTED per panel` | 3 sub-panels sharing identical axes + 1 accompanying render. | **n per panel is never stated** anywhere. All three panels share fixed axes (good), but **no quantitative summary of the spread is given** — the "more diverse" claim is left to the eye. **The apo/holo markers are drawn but never used**: no distance to either is reported, so the reader cannot tell whether the added diversity moves toward or away from the known states. | CC-BY 4.0, no ND. p19. |
| **3D** | 19 | dacB: metadiffusion ensemble and ATLAS MD ensemble as conformer overlays with a red arrow on the flexible domain, above per-residue Cα RMSF traces for each, with the correlation and mean RMSF printed underneath. | line (+ accompanying renders) | `PLOT \| facet: source (2: metadiffusion, ATLAS MD) \| vary: residue number, 0–450 (continuous) \| series: none (1; the trace is colour-graded by position, not by condition) \| measure: Cα RMSF (Å) \| mark: line \| n: 16 structures (metadiffusion), 100 ns trajectory (MD), per panel` | 2 line sub-panels + 2 conformer-overlay renders above them (the renders share the letter and are described in `panels` rather than split, since they carry no measure). | **The two RMSF traces are drawn on the same 0–20 Å axis, and the metadiffusion trace visibly fills it while the MD trace hugs zero — a ~5.8× magnitude gap (6.18 Å vs 1.06 Å, printed in-panel) that the caption and the running text never mention.** The figure is honest; the text is silent. Also **a single hand-picked protein is shown as the worked example with no statement of how it was chosen** from the 256. | CC-BY 4.0, no ND. p19 (caption continues p20). |
| **3E** | 19 | Distribution over 256 ATLAS proteins of the metadiffusion-vs-MD RMSF correlation, plotted against the MD-vs-MD replicate correlation — the paper's only statistical result and its ceiling. | box | `PLOT \| facet: correlation statistic (2: Pearson's r, Spearman's ρ) \| vary: arm (2: metadiffusion, MD) \| series: none (1) \| measure: correlation coefficient \| mark: box (horizontal, with outlier points) \| n: 256 proteins per box` | 2 sub-panels, same two arms, different statistic. | **Only outlier points are drawn, not the full distribution** — the body of 256 values is represented by the box alone, so the shape of the distribution (and any bimodality) is invisible. Means are printed in the axis labels, which is good practice; **n = 256 is stated in the caption but not on the panel**. | CC-BY 4.0, no ND. p19. |
| **4A–D** | 20 | Alternative binding poses generated by aligning one group and biasing another: three Ras/Raf-RBD poses (4G0N); three DNA-ligase/DNA conformations (2Q2U); four furosemide poses in one HSA pocket on a Connolly surface; four furosemide poses across different HSA sites. | structure render | `RENDER \| facet: system (3: Ras–Raf, DNA ligase–DNA, furosemide–HSA) × depiction (2: cartoon, Connolly surface) \| views: 1 (all sub-images share one camera per panel; C and D annotated "structures aligned with same camera view") \| overlay: NOT REPORTED predictions on 0 reference(s) \| axis: none` | 4 panels, 14 sub-images total (A: 3, B: 3, C: 4, D: 4). Biased group highlighted by a blue halo in A and B. | **This is the paper's clearest figure-level defect: an entire results section — "different poses … can be resolved", "can be mapped to different binding conformations", "different pockets" (all p5) — is supported by renders and nothing else.** No pose RMSD, no pocket identification or naming, no count of distinct poses recovered, no comparison to the deposited pose in 4G0N / 2Q2U, no scoring, no n. The claim that "even though only the ligand receives the biases … the protein also adopts slightly different conformations" (p5) has **no quantitative panel at all**. The number of poses shown (3, 3, 4, 4) is a layout choice, not a result. | CC-BY 4.0, no ND. p20. |
| **5A + 5B(right)** | 21 | Experimental SAXS P(r) overlaid with the ensemble-averaged P(r) of unbiased Boltz-2 and of SAXS-steered metadiffusion, with the Wasserstein-1 distance printed in each legend entry; for the GTP aptamer and for calmodulin. | line (filled) | `PLOT \| facet: system (2: class V GTP aptamer + GTP, calmodulin) \| vary: pair distance r, 0–75 Å (continuous) \| series: source (3: experimental SAXS, unbiased Boltz-2, metadiffusion) \| measure: P(r) \| mark: line \| n: 8 structures per generated curve (aptamer), 16 (calmodulin), 1 experimental curve` | 2 plot sub-panels (5A left, and the upper-right sub-panel of 5B) sharing mark and measure. Accompanied by 4 + 4 structure renders (aptamer, calmodulin) that carry no data. | **The generated curves are ensemble averages presented as a single line, with no band showing the spread across the 8 or 16 members** — a broad ensemble and a tight one that happen to share a mean are indistinguishable here, which matters because the paper's own claim is that these ensembles are simultaneously highly diverse *and* well-fitted (p5). **The fit is to the same data that was used as the biasing target**, which the caption does not flag. | CC-BY 4.0, no ND. p21. |
| **5B(left)** | 21 | Calculated vs experimental ¹³Cα and ¹³Cβ chemical shifts with y = x guides and per-point error bars, with the applied reference-frame offset printed in-panel. | scatter | `PLOT \| facet: nucleus (2: ¹³Cα, ¹³Cβ) \| vary: experimental chemical shift, 20–70 ppm (continuous) \| series: none (1) \| measure: metadiffusion (CheShift-2) chemical shift (ppm) \| mark: point (with vertical error bars) \| n: 16 structures behind each point; ~150 residues per panel` | 2 correlation sub-panels. | **No unbiased-Boltz-2 comparison points are plotted**, although the text gives the unbiased R values (0.66 and 0.97, p5) — so the improvement the text claims is not visible in the figure. **The error bars are undefined** (SD? SEM? range?) in caption and Methods. | CC-BY 4.0, no ND. p21. |
| **5B(bottom)** | 21 | Per-residue ¹³Cα and ¹³Cβ chemical shifts, experimental vs metadiffusion ensemble average, along the calmodulin sequence, with RMSD / MAE / R printed in-panel. | line | `PLOT \| facet: nucleus (2: ¹³Cα, ¹³Cβ) \| vary: residue number, 0–150 (continuous) \| series: source (2: experimental, metadiffusion) \| measure: chemical shift (ppm) \| mark: line (with point markers and error bars) \| n: 16 structures per metadiffusion point` | 2 sub-panels. Panel letter B therefore appears in three rows (correlation scatters, P(r) line, per-residue traces), as permitted by the schema. | **Traces are drawn as connected lines across residue index**, which implies continuity between non-adjacent assigned residues and visually inflates agreement; a per-residue difference plot would show the actual errors. Gaps from unassigned residues are not marked. | CC-BY 4.0, no ND. p21. |
| **S1** | 23 | Peptide bond breaks and steric clashes across 256 ATLAS proteins, before and after energy minimisation, as point clouds over two categories with summary statistics boxed in-panel. | scatter (strip) | `PLOT \| facet: defect type (2: peptide bond breaks > 1.7 Å, steric clashes) \| vary: minimisation stage (2: before, after) \| series: none (1) \| measure: count per structure (mean over 16 structures) \| mark: point (strip, with a small box/whisker beneath) \| n: 1 point = mean over 16 structures; 256 points per category` | 2 sub-panels, same mark and measure, differing only in the quantity counted. | **Linear y-axis with a long upper tail compresses the entire body of the distribution into the bottom decade** — the visible difference between "before" and "after" is carried by a handful of outliers while the bulk is an unreadable black band at zero. A log axis or a violin would show the actual shift. **The n per point (16) is given in the caption but the number of points (256) must be inferred.** | CC-BY 4.0, no ND. p23. |
| **S2** | 24 | Wall-clock time to generate ensembles of 2–128 ubiquitin samples, unbiased Boltz-2 vs metadiffusion maximising pairwise RMSD, every bar value labelled. | bar | `PLOT \| facet: none (1) \| vary: number of samples (7: 2, 4, 8, 16, 32, 64, 128) \| series: method (2: Boltz-2, metadiffusion) \| measure: wall-clock time (s, log scale) \| mark: bar \| n: NOT REPORTED — no repeat timings, no error bars` | 1 panel, 14 bars. | **Single timing run per bar with no error bars and no stated repeats.** The log y-axis compresses the O(N²) blow-up (265 s → 1,915 s at n = 128) so it reads as a modest gap; every bar is numerically labelled, which rescues it. **Benchmarked on one 76-residue protein only**, so the cost claim does not transfer to the 450-residue systems elsewhere in the paper. | CC-BY 4.0, no ND. p24. |

**Panel-group row count: 16 rows** (Fig 1: 1; Fig 2: 3; Fig 3: 5; Fig 4: 1; Fig 5: 3;
Supplementary: 2). Supplementary Table 1 (p22) is a table, not a figure, and is not given a row;
its numbers are in `metrics_reported`.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), session of 2026-09-08
- **schema_version**: v3
- **confidence**: **high** for A, B, D, E and the mechanism in C; **medium** for two specific
  things.
  - The text layer of this PDF is clean and complete for running prose. **But every equation is
    missing.** `pdftotext` renders the three energy definitions on p8 as blank space between
    "The energy function is" and "where k is the strength…". The *forms* are unambiguous from the
    surrounding prose (linear in CV for optimisation; "harmonic loss" for steering; "Gaussian
    RBF" with a user-defined spread σ, normalised by the number of pairs N, for exploration) and
    are recorded as such, but **the literal expressions were not read** and are not quoted.
  - Figure-panel text extracts as scrambled fragments, so seven pages were rendered at 150 dpi
    and read as images (17, 18, 19, 20, 21, 23, 24). Roughly **half of the numbers in
    `metrics_reported` exist only inside figure panels** and were transcribed from those renders;
    they are legible but were read from a 150-dpi raster, so the last digit of the smallest
    in-panel annotations carries some risk. The values cross-checked against running text (0.81,
    0.88, 0.65, 0.66→0.97, 0.97→0.99, 89.9%) agree exactly.
- **unresolved**:
  1. **A tag is genuinely missing from the v3 vocabulary, and this paper is the reason.** See the
     `latent-steering` discussion in Tags. The corpus has no tag for **inference-time guidance on
     the sampled coordinate / score trajectory of a diffusion model** — a family that includes
     this paper, particle guidance (ref 18), Richman *et al.* 2025 (ref 19), Maddipatla *et al.*
     2025 (ref 20), Nam *et al.* 2025 (ref 21) and ExEnDiff (ref 23), all cited here. `latent-steering`
     is defined as intervention on an *internal tensor* and its four examples are all
     representation tensors; this method touches only the atomic point cloud. I declined to
     stretch the tag and declined to invent one. **A tag such as `coordinate-guidance` or
     `score-guidance` is needed** — the schema owner's call.
  2. **Whether templates were used is unrecoverable from the PDF.** The word never appears. For a
     paper whose claim is that the bias moves the structure, this is a material gap.
  3. **Whether an MSA was used, and at what depth**, is likewise never stated for the authors'
     own runs.
  4. **Per-system bias strength, clip and denoising window are not in the paper** — pushed to the
     GitHub repo ("The exact biases and configurations used can be found in the code examples",
     p7). Only the ATLAS run (strength = 3, clip = 3) and the sweep levels in Fig 3b/3c are
     recoverable. This makes every single-system result in Figs 2, 4 and 5 **unreproducible from
     the paper alone**.
  5. **The 256 per-protein Pearson R values are in Supplementary File 1, which is not in the
     PDF** (see `si_in_scope`). The distribution behind the paper's only statistical claim is not
     in the corpus.
  6. **Wasserstein-1 vs Cramér distance:** the text and figures label the SAXS metric one way and
     Methods names another (p5, p21 vs p9). Not resolvable from the PDF.
  7. **The p5 chemical-shift sentence is internally garbled** ("with and without SAXS steering
     respectively" attached to arms that are actually unbiased vs steered). Direction resolved
     from Fig 5b in-panel values, but the sentence as written should not be quoted.
  8. **No affiliation superscript is typeset for author Xing Er Ong** (p1).
  9. **The MfnG hinge-angle range claim** ("This range is larger than that of default Boltz-2",
     p3–4) is supported only by the Fig 2c density, whose n is never stated.
  10. **Ambiguity encountered in v3 itself** (beyond the tag gap, reported bluntly below in Tags):
      the RENDER form's `overlay` slot asks for "`<k>` predictions on `<n>` reference(s)", but
      several renders here overlay many *predictions on each other* with **zero** references
      (Fig 3a's conformer bundles, Fig 4's pose sets). I wrote `overlay: NOT REPORTED predictions
      on 0 reference(s)`, which is legal but reads oddly; the grammar has no natural way to say
      "an overlay of predictions with nothing to compare against", which is itself a meaningful
      and recurring shape.
- **why_it_matters**: *(left empty by the extractor per schema v3)*

---

## Tags

`general-protein` `periplasmic-binding` `cofolding` `enhanced-sampling` `ensemble`
`continuous-metric` `visual-metric` `saturating-metric` `design-level-oracle`
`no-anti-memorization` `directed-state` `preprint` `precedent` `contrast` `comparator-numbers`

**Tag notes — every judgement call, and the two the brief asked about:**

- **`latent-steering` — DELIBERATELY NOT APPLIED. This is the vocabulary problem, and it is
  real.** The v3 definition is: "any inference-time intervention on an **internal tensor** — pair
  representation, trunk embedding, distogram head, conditioning embedding. It is not MSA
  manipulation, not template bias, not seeds." Metadiffusion intervenes on **none of those**. It
  intervenes on the **atomic point cloud**, i.e. the sampled 3-D coordinates that are the
  diffusion state itself. p7, verbatim: "Biases are introduced during the denoising process of
  the Boltz-2's diffusion model **into the atomic point cloud directly**… The displacement
  vectors from Boltz-2's denoising process and biases are summed before being applied
  simultaneously in each iteration." And p7: "it **relies entirely on Boltz-2's trunk and
  diffusion model** with no additional training or fine-tuning" — the trunk is read, never
  written.
  The counter-argument I considered and rejected: an intermediate noisy point cloud x_t is
  arguably "internal", since it never leaves the sampler. But (a) all four of the tag's examples
  are *representation* tensors in the network's feature space, and coordinates are the model's
  output space, not its feature space; (b) if x_t counted, then every guidance method and every
  classifier-guided diffusion sampler would be `latent-steering`, which would make the tag
  useless for its actual purpose — finding papers that reach inside the network. Applying it
  here would make a false claim about where the intervention lands and would pollute reverse
  lookups for genuine representation-level methods.
  **Neither fits, so no tag was invented.** The gap is recorded under `unresolved` item 1: the
  corpus needs a distinct tag for coordinate/score-trajectory guidance, and it will need it for
  at least five other papers this one cites.
- **`enhanced-sampling` — applied, as the closest honest fit, with a caveat.** The paper's own
  framing is metadynamics-derived (p2 on auxiliary potentials pushing into rarer states; p3 on
  CV-based guidance) and its meta-energy is literally a biasing potential on a collective
  variable. But it is enhanced sampling of a *generative model*, not of a dynamical trajectory.
  Anyone using this tag for a reverse lookup will get this paper alongside genuine MD enhanced
  sampling; that seems right, but note the difference.
- **`cofolding` — applied.** Boltz-2 co-folds protein + nucleic acid + ligand throughout, and
  Fig 4c/d is explicitly a co-folding result (p5: "effectively allows Boltz-2 to co-fold the
  protein with a single ligand in different conformations in the same pocket").
- **`md` — NOT applied.** No molecular dynamics was run by these authors. MD appears only as a
  published comparator (ATLAS, ref 31). The only force-field step is OpenMM energy
  *minimisation* (p8), which is not dynamics. Tagging `md` would false-positive every query for
  papers that ran simulations.
- **`md-emulator` — NOT applied.** Boltz-2 is trained on the PDB, not on trajectories. BioEmu is
  an MD emulator but appears only as a comparator, not as a method component.
- **`multi-backbone` — NOT applied.** The schema requires "more than two [backbones] compared
  head to head". Metadiffusion runs on **one** backbone (Boltz-2). BioEmu is a comparator
  generator, not a backbone the method was ported to. AF3, OpenFold, Chai-1 and IDPFold2 are
  named as compatible (p6) but **were never run** — an untested portability claim must not
  become a tag.
- **`directed-state` — applied, with an explicit narrowing.** The steering mode is a genuine
  directional handle: a harmonic potential toward a user-specified CV value (p8), demonstrated
  tracking targets from 10 to 45 Å (Fig 2b). But **the target is a scalar CV value or an
  experimental curve, never a named conformational state.** You cannot ask for "the active
  state"; you can only ask for "Rg = 25 Å" or "this P(r) curve" or "these chemical shifts", and
  translating a state into such a target requires already knowing the state. Tagged because a
  reverse lookup for pointable methods should return this paper; narrowed here so nobody quotes
  it as state-directed.
- **`ligand-driven` / `partner-driven` — NOT applied.** Ligands and partners are present (GTP,
  risdiplam, furosemide; H-Ras, DNA) but they are the **biased objects**, not the handle that
  drives the state. The handle is always the meta-energy.
- **`apo-sampling` / `seed-only` / `nanobody` / `g-protein-mimetic` / `peptide-driven` — NOT
  applied.** None of these mechanisms appears. Seeds are never mentioned.
- **`kinase` — NOT applied, deliberately.** Raf is a protein kinase, but only its **Ras-binding
  domain** is modelled (Fig 4a, p20) and no kinase conformational state (DFG, αC, activation
  loop) is studied anywhere. Tagging would false-positive every kinase-conformation query.
  *E. coli* adenylate kinase is `general-protein` by the v3 rule, which names that case
  explicitly.
- **`periplasmic-binding` — applied, narrowly.** *H. influenzae* SiaP (Fig 3c, p19) is the
  periplasmic sialic-acid-binding protein of a TRAP transporter (ref 62, p15). It is one system
  among thirteen, used for the strength/clip sweep, with deposited apo (2CEY) and holo (6H76)
  markers on the panel — genuinely useful for a reverse lookup on that family, but do not read
  this paper as being *about* periplasmic binding proteins.
- **`transporter` — NOT applied.** SiaP is the soluble binding protein, not the transmembrane
  transporter. No membrane protein appears in the paper.
- **`gpcr` / `atpase` / `fold-switching` — NOT applied.** None appears.
- **`ensemble` — applied, singly.** Every result is an ensemble statistic. No arm collapses onto
  a single basin, so the `ensemble + single-state` pair is not warranted. `two-state` and
  `continuum` are both wrong: the method has no notion of discrete states, and it produces a
  spread rather than a resolved continuum along a reaction coordinate.
- **`continuous-metric` — applied** (Rg, SASA, angle, RMSD, W1, Pearson R, ppm).
- **`visual-metric` — applied, and it is a rigour finding, not a formality.** The entire
  binding-pose results section (p5) and all of Figure 4 (p20) call the state by eye from renders,
  with no operationalised predicate, no pose RMSD, no pocket assignment and no quantitative
  panel of any kind.
- **`rmsd-only` — NOT applied.** RMSD-to-reference appears (Fig 3a) but is one coordinate among
  many and is never the sole discriminator; the paper's primary metrics are CV values and
  experimental-observable distances.
- **`binary-predicate` — NOT applied.** No binary state call exists anywhere.
- **`saturating-metric` — applied.** Two numeric ceilings: Rg plateaus at ~45 Å against targets
  running to ~70 Å (p3, Fig 2b), and the ¹³Cβ Pearson R starts at 0.97 unbiased with only 0.02 of
  headroom (p5).
- **`design-level-oracle` — applied (route 7).** Every one of the thirteen systems was chosen
  because the structural answer was already known, and in the hinge case the collective variable
  itself must be located by the user from prior structural knowledge (p3, Fig 2c p18).
- **`oracle-leak` — NOT applied, after a close reading.** Routes 1, 2, 3 and 6 are cleanly
  absent; route 4's sweep is selected on physical plausibility rather than on proximity to a
  reference; route 5's reference RMSDs are a descriptive axis whose reported result is
  *negative* for the method (p4). Nothing leaks into the pipeline. Keeping `design-level-oracle`
  and `oracle-leak` distinct is exactly what the v3 changelog asks for.
- **`prospective` — NOT applied.** Every system, every restraint and every comparator is
  pre-existing and published.
- **`anti-memorization` — NOT applied; `no-anti-memorization` applied.** No held-out set, no
  post-cutoff set, no training-cutoff discussion, no control arm. The paper cites the
  memorisation literature (refs 42–43, p6) and runs nothing.
- **`unpowered` — NOT applied.** That marks an underpowered anti-memorisation control; here the
  control does not exist at all, which `no-anti-memorization` already says.
- **`confidence-as-discriminator` — NOT applied.** pLDDT/pTM/ipTM appear nowhere; no confidence
  score is used to select, rank or filter anything.
- **`experimental-validation` — NOT applied, and this one matters.** The paper fits to
  **published, pre-existing** SAXS (SASBDB) and NMR (BMRB) data. No experiment was performed. And
  crucially, **those data were the biasing target**, so agreement with them is partly circular —
  it demonstrates that the optimiser works, not that the ensemble is right. The only
  non-circular check in the paper is the ATLAS MD RMSF comparison, which is a simulation
  comparator, not lab validation.
- **`no-template-no-msa` / `templates-on` / `state-annotated-input` — NONE applied.** The input
  regime is genuinely unreported: the paper never states whether templates or MSAs were used
  (see `unresolved` 2 and 3). Asserting either protocol tag would be inference, not extraction.
- **`allosteric-site` / `orthosteric` / `cryptic-pocket` / `allosteric-failure` — NOT applied.**
  Fig 4d shows furosemide at "multiple different docking sites" on HSA (p20) but the sites are
  never named, classified or compared to known drug sites, so no site claim can be tagged.
- **`negative-result` — NOT applied.** The adenylate-kinase result is negative (structures move
  further from both reference states, p4) and the mean-RMSF magnitude correlation is weak
  (R = 0.65, p4), but the paper as a whole is a positive methods report; the tag would misfile it.
- **`figure-exemplar` — NOT applied.** The tag is for papers "kept mainly for [their] figures …
  must be excluded from gap analysis". This paper is kept for its mechanism and its numbers, and
  belongs in gap analysis. (Fig 1 is nonetheless a good mechanism-schematic model, and Fig 3e's
  "plot the method against its own reproducibility ceiling" layout is worth copying.)
- **`comparator-numbers` — applied.** Thirty-plus reusable values, most notably the
  metadiffusion-vs-MD RMSF correlations with an explicit MD-replicate ceiling, the paired
  unbiased/biased SAXS distances, and the paired runtime series.
- **`precedent` + `contrast` — both applied**, per the dual `stance` above. Provisional; the
  user's call.
