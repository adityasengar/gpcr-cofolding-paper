# tejero2024opsin

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` **with a reason** where the field presupposes a structure-prediction
pipeline this paper does not have.

**What this paper is.** A pure wet-lab structural-biology paper: single-particle cryo-EM
of an invertebrate bistable opsin (jumping spider rhodopsin-1, JSR1, from *Hasarius
adansoni*) in complex with G-protein heterotrimers. **There is no structure prediction of
any kind in it** — no AlphaFold, Boltz, Chai, no MSA handling, no templates in the
prediction sense, no sampling. Model building is classical cryo-EM: rigid-body docking of
deposited coordinates in UCSF Chimera, MDFLEX, then `phenix.real_space_refine` and Coot
(p11). Consequently most of section C is `NOT APPLICABLE`, by design and not by
sloppiness — this is what the `experimental` tag exists to mark.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–13), and the PDF page
equals the printed page throughout** (PDF p12 prints "12"). Layout: title/abstract p1,
introduction p2, Results p2–7, Discussion p7–9, Methods p9–11, Data availability +
references p12–13, licence/peer-review statement p13. Figures 1–6 are inline in the text
pages (Fig 1 p3, Fig 2 p4, Fig 3 p6, Fig 4 p7, Fig 5 p8, Fig 6 p8).

**SI status: NOT HELD, and it matters.** Supplementary Figs 1–18, Supplementary Tables
1–4, Supplementary Movies 1–8 and the Source Data file are all referenced and none are in
the held PDF. **Supplementary Table 1 is the cryo-EM data-collection and refinement
statistics table** — so map resolution is the only map statistic recoverable from the main
text, and B-factors, FSC curves, map-to-model CC, clash scores, Ramachandran statistics
and per-map particle/pixel details beyond those quoted below are absent. Supplementary
Tables 2 and 3 hold the per-residue receptor–Gα interaction lists whose *totals* the main
text quotes. Supplementary Fig. 5 is the jsGiq chimera sequence alignment — the primary
document for the construct question, and it is not held. See `si_in_scope`.

**One page rendered:** p3 at 150 dpi, to read the mark type and axis of Fig 1b, which the
caption does not state ("Data is presented as mean values +/− standard deviation" does not
say whether the glyph is a bar, a point or a box; it is a box-and-whisker with whiskers).
Render deleted afterwards.

---

## THE CONSTRUCT TABLE — read this before using any of these three entries

This is the single most consequential content in the note. A database cross-reference can
present any of these as "the native complex". **None of the three is a native heterotrimer
of a single species**, and two of the three carry an explicitly engineered chimeric Gα.

| PDB | EMDB | Paper's name | Gα | Gβγ | Chimera? | Receptor construct | Chromophore / ligand state | Resolution |
|---|---|---|---|---|---|---|---|---|
| **9EPP** | EMD-19882 | JSR1-jsGiq_1 (fully engaged) | **jsGαiq — engineered chimera**: human Gαi1 mutated to jumping-spider Gαq1 sequence at the receptor interface (A31R; D193S; L194I; residues 337–354 wholly replaced) | **human** Gβ1 + **human** Gγ2 | **YES — chimeric Gα** | wild-type JSR1 (*H. adansoni*), C-terminal 1D4 epitope tag only; no fusion, no thermostabilising mutation, no truncation stated; 4 residues Asp265⁶·²³–Lys268⁶·²⁶ unmodelled | **ATR6.11** (all-*trans* retinal 6.11), a **non-natural synthetic retinal analog agonist**, covalently linked to Lys321⁷·⁴³ via a protonated Schiff base; nucleotide-free (apyrase) | 4.1 Å (4.06 Å) |
| **9EPQ** | EMD-19883 | JSR1-jsGiq_2 (rotated G protein) | **same jsGαiq chimera as 9EPP** | **human** Gβ1 + **human** Gγ2 | **YES — chimeric Gα** | as 9EPP; ICL3 residues R261–N263 **not** resolved (they are resolved in 9EPP) | as 9EPP (ATR6.11, PSB to Lys321⁷·⁴³, nucleotide-free) | 4.2 Å (4.17 Å) |
| **9EPR** | EMD-19884 | JSR1-hGi | **human Gαi1**, wild-type sequence, N-terminal TEV-cleavable deca-His tag | **bovine** Gβ1γ1, physically separated from **bovine retinal transducin** | **NO chimera — but cross-species reconstituted, not native**: human Gαi1 + bovine Gβ1γ1 mixed in vitro | as 9EPP/9EPQ (wild-type JSR1 + 1D4 tag); ICL3 fully resolved here; atypical bend of TM6 | **native all-*trans* retinal**, generated in situ by reconstituting with **9-*cis*** retinal and illuminating through a 495 nm long-pass filter; nucleotide-free (apyrase) | 4.9 Å ("sub-5 Å") |

### Verbatim construct quotes, with pages

**Assignment of names to accession codes** — p12, Data availability, the *only* place in
the paper where any accession code appears:

> "Atomic coordinates of JSR1-jsGiq_1, JSR1-jsGiq_2, and JSR1-hGi without the AHD have
> been deposited to the Protein Data Bank under accession codes 9EPP, 9EPQ and 9EPR,
> respectively. Cryo-EM maps of JSR1-jsGiq_1, JSR1-jsGiq_2, and JSR1-hGi have been
> deposited in the Electron Microscopy Data Bank under accession codes EMD-19882,
> EMD-19883 and EMD-19884, respectively." (p12)

**The chimera, design rationale** — p2:

> "However, the production of active and pure jsGq for structural studies was not
> successful. Therefore, we decided to create a human Gi/jumping spider Gq chimera (jsGiq)
> by engineering hGi to match the sequence of jsGq at the interface where the hGi protein
> contacts the receptor based on our JSR1-hGi cryo-EM structure. These residues, mainly in
> the C-terminal α5 helix, were substituted (Supplementary Fig. 5; see "Methods" for
> details). An in vitro activity assay showed that this chimera retains intrinsic GTPase
> activity (Fig. 1b)." (p2)

**The chimera, exact substitutions** — p10, Methods, "Gαiqβ1γ2 expression":

> "Mutations were introduced to the human Gαi to match the sequence of the jumping spider
> Gαq1 (HaGq1: acc. No. LC799818) (A31R; D193S; L194I; [residues 337–354 =
> DAVTDVIIKNNLKDCGLF] Gαi1 to [residues 337–354 = CAVKDTILQNNLKECNLV]) (Supplementary
> Fig. 5). The Gαiq chimera, hGβ1 and hGγ2 subunits were cloned into the pAC8RED vector
> for insect cell expression." (p10)

So the swap is: **three point substitutions (A31R, D193S, L194I) plus wholesale
replacement of the 18-residue C-terminal segment 337–354 — the α5 helix / C-hook — of
human Gαi1 by the corresponding jumping-spider Gαq1 segment.** The β and γ subunits of
this complex are human (Gβ1, Gγ2) and are **not** chimeric. The Gα backbone is human Gi;
only the receptor-contacting surface is spider Gq. Calling 9EPP/9EPQ "a Gq complex" or "a
spider G protein complex" would be wrong in both directions.

**The "hGi" heterotrimer is cross-species reconstituted** — p10, Methods, "Gαi1β1γ1
Expression and purification":

> "Human Gαi subunit (Gαi1) with an N-terminal TEV protease-cleavable deca-histidine tag
> was expressed in E. coli BL21 (DE3) cells (Sigma-Aldrich) and purified as described
> previously48. The Gβ1γ1 subunits were separated from the transducin G protein
> heterotrimer, which was purified from bovine retinae as described by Maeda et al.49.
> Human Gαi1 and bovine Gβ1γ1 were mixed to generate the Gαi1β1γ1 heterotrimer used for
> complex formation with JSR." (p10)

This entry (9EPR) is the closest of the three to "native", but it is a **human Gαi1 +
bovine transducin-derived Gβ1γ1 hybrid heterotrimer assembled in vitro**, not a native
human Gi heterotrimer and not a native spider heterotrimer. Note also the asymmetry that a
cross-reference will not surface: **the two jsGiq entries use human Gβ1γ2, the hGi entry
uses bovine Gβ1γ1** — the βγ pair differs between 9EPP/9EPQ and 9EPR.

**Receptor construct, all three** — p9, Methods, "JSR1 Expression and purification":

> "Wild-type Jumping Spider Rhodopsin isoform-1 (JSR) from Hasarius adansoni tagged with a
> C-terminal 1D4 epitope15, was recombinantly expressed in HEK293 GnTI− cells as described
> previously16." (p9)

The receptor is **wild type**. The only modification stated anywhere is the C-terminal 1D4
epitope tag (used for antibody-affinity purification and eluted with the 1D4 peptide
TETSQVAPA, p9). **No BRIL/T4L/rubredoxin fusion, no thermostabilising mutation, no
N- or C-terminal truncation is reported for any of the three entries.** The S199⁴⁵·⁴⁹F and
Y126³·²⁸F and E194⁴⁵·⁴⁴D mutants discussed in the text are cited from **previous** work
(refs 12, 45) and were **not** used for any deposited structure here.

**Chromophore, 9EPP / 9EPQ** — p2 and p4:

> "Rather than activating JSR1•9-cis retinal with light, we reconstituted JSR1 with
> ATR6.11, a non-natural retinal analog that has an agonist activity18." (p2)

> "The electron density in the orthosteric binding pocket shows the presence of ATR6.11
> covalently linked to Lys3217.43 via a PSB (Supplementary Fig. 9a and b)." (p4)

**Chromophore, 9EPR** — p2:

> "The JSR1•all-trans retinal-human Gi complex (JSR1-hGi) was prepared by reconstituting
> JSR1 with 9-cis retinal and illuminating with 495 nm long-pass filtered light under
> light-controlled conditions to activate the receptor and induce coupling to the hGi
> heterotrimer." (p2)

9EPR therefore carries the **native all-*trans* retinal**; 9EPP and 9EPQ carry a
**synthetic analog**. Anyone treating all three as "the active-state JSR1 structure" is
mixing a natural and a non-natural chromophore. The paper argues they are equivalent —
"The JSR1-hGi map shows density for all-trans-retinal and overlays well with the ATR6.11
analog, indicating a similar binding pose for both ligands" (p4) — but that is an argument,
not an identity.

**Nucleotide state, all three** — p10: "supplemented with apyrase (New England Biolabs)
(25 mU/mL) to degrade any GTP and GDP present in the solution"; p9 confirms the complexes
are read as "two of the conformations of this dynamic process even in a nucleotide-free
condition". All three are **nucleotide-free** complexes.

**Detergent:** JSR1-jsGiq purified and frozen in **DDM** (p3, p10); the JSR1 sample for
the hGi complex was exchanged "from 0.01% DDM to 0.01% lauryl maltose neopentyl glycol
(LMNG)" (p9). No nanodisc, no amphipol, no lipid reconstitution.

### Disagreements and parse ambiguities — recorded, not resolved

1. **Scope of "without the AHD" (p12).** The sentence reads "JSR1-jsGiq_1, JSR1-jsGiq_2,
   and JSR1-hGi **without the AHD**". Two readings:
   - **Reading A** (modifier attaches to JSR1-hGi only) — supported by the rest of the
     paper: "The quality of both JSR1-jsGiq maps allowed us to model the position of the
     AHD" (p7), and the hGi processing "was subjected to post-processing with a soft mask
     excluding the Gα AH domain" (p11), with 3D refinement also run "with a soft mask
     excluding the AH domain" (p11). Under Reading A, **9EPP and 9EPQ contain a
     rigid-body-fitted AHD; 9EPR does not.**
   - **Reading B** (modifier distributes over all three) is contradicted by p7 and p11.

   I record Reading A as the one the paper's own body text supports, and flag that the
   sentence is genuinely ambiguous as written.
2. **The AHD in 9EPP/9EPQ is rigid-body fitted, not refined at side-chain level.** "Density
   for the α-helical domain (AHD) was observed in both JSR1-jsGiq maps, allowing rigid body
   fitting of the AHD into the map, but the resolution did not allow precise modeling of
   side chains" (p3). Anyone measuring AHD geometry from 9EPP/9EPQ is measuring a docked
   rigid body.
3. **The accession codes appear exactly once, on p12.** No figure caption, no Methods
   paragraph, and no table in the held PDF carries a PDB or EMDB code for any of the three
   new structures. **There is therefore no internal cross-check** — the p12 sentence is the
   sole authority and cannot be corroborated against the figures. This is a *gap*, not a
   contradiction: I found **no disagreement** between text, figures and data availability,
   because there is only one source. Do not read the absence of a contradiction as
   confirmation.
4. **Naming inconsistency in the body text.** The complexes are written "JSR1-jsGiq_1" and
   "JSR1-jsGiq_2" in most places but "JSR1-Giq_1" / "JSR1-Giq_2" on p6 and "JSR-jsGiq_1" /
   "JSR-jsGiq_2" on p7, and "JSR1-JSGiq_1" on p9. Same structures; cosmetic only, but a
   string match against the paper will miss rows.
5. **The chimera was designed from the authors' own JSR1-hGi cryo-EM structure** (p2). So
   9EPP/9EPQ are not independent of 9EPR: the construct in the two higher-resolution
   entries was engineered using the lower-resolution entry as its design input.

---

## A. Identity

- **citekey**: `tejero2024opsin`
- **doi**: `10.1038/s41467-024-53208-2` (p1 header, repeated every page; confirmed against
  `MANIFEST.csv`)
- **year**: 2024. Received 10 April 2024; accepted 4 October 2024 (p1). Published version.
  **Not a preprint** — peer-reviewed, with an explicit peer-review statement on p13:
  "Nature Communications thanks Takefumi Morizumi and the other anonymous reviewer(s) for
  their contribution to the peer review of this work. A peer review file is available."
- **venue**: *Nature Communications* 15:8928 (2024) (p1 footer, all pages)
- **title**: "Active state structures of a bistable visual opsin bound to G proteins" (p1)
- **authors**: Oliver Tejero, Filip Pamula, Mitsumasa Koyanagi, Takashi Nagata, Pavel
  Afanasyev, Ishita Das, Xavier Deupi, Mordechai Sheves, Akihisa Terakita, Gebhard F. X.
  Schertler, Matthew J. Rodrigues & Ching-Ju Tsai (p1). Corresponding: Schertler, Rodrigues,
  Tsai (p1, p13). PSI / ETH Zurich / Osaka Metropolitan University / Weizmann.
  Competing interests (p13): "G.F.X.S. declares that he is a co-founder and scientific
  advisor of the company leadXpro AG and InterAx Biotech AG."

## B. Scope

- **system**: **GPCR** — class A, light-sensitive opsin subfamily. Jumping spider
  rhodopsin isoform-1 (JSR1), an invertebrate **bistable** opsin, in complex with
  heterotrimeric G proteins. Comparators drawn in are bovine rhodopsin (monostable), squid
  rhodopsin, β2-adrenergic receptor, M1, NTSR1, GABA(B), CB2 (p11).
- **n_targets**: **1 receptor** (JSR1), solved in **3 complexes** with **2 distinct
  G-protein preparations** (the jsGiq chimera and the human-Gαi1/bovine-Gβ1γ1 hybrid),
  yielding **3 deposited coordinate sets** and **3 deposited maps**. Generality claims are
  made about bistable opsins as a class and about invertebrate opsins as a class from this
  single receptor, supported by sequence-conservation analysis rather than by additional
  structures (p11: 202 vertebrate + 113 invertebrate opsin sequences aligned) — worth
  flagging as single-system generalisation.
- **method_class**: **other — experimental structure determination (single-particle
  cryo-EM)**, plus an in-vitro nucleotide-exchange/GTPase functional assay and
  bioinformatic sequence-conservation analysis. Not co-folding, not MSA-subsampling, not
  MSA-state-filtering, not template-biasing, not MD, not enhanced sampling, not clustering,
  not benchmark-only. **No structure prediction of any kind appears in the paper.**
- **backbones**: `NOT APPLICABLE` — no structure-prediction model is used, so there is no
  backbone to name. The computational stack is cryoSPARC, Relion4, MotionCor2, CTFFIND4.1,
  Topaz, crYOLO, SIDESPLITTER, UCSF Chimera, MDFLEX, Phenix, Coot, PyMOL, Clustal Omega,
  WebLogo (p11).
- **templates**: `NOT APPLICABLE` in the prediction sense. In the cryo-EM sense, deposited
  coordinates **were** used as starting models for rigid-body docking and real-space
  refinement — see `structural_priors_used` for the full list with pages. Recording that
  under `templates` would make this note join falsely against template-biasing prediction
  papers.
- **msa_handling**: `NOT APPLICABLE` — no MSA is used to drive any structure calculation.
  Multiple sequence alignments **are** built (Clustal Omega, p11), but purely for
  conservation logos comparing opsin clades at positions 3.28, 6.44 and 6.47; they feed
  interpretation, not modelling. Depths: "202 vertebrate opsin sequences" and "113
  invertebrate opsin sequences" (p11).

## C. Conformational core

**Framing note.** Every field in this section is written against a structure-prediction
pipeline. This paper has none. Below, each field is answered `NOT APPLICABLE` **with the
specific reason**, and where the field has an honest experimental analogue that analogue is
recorded so the row is not simply empty.

- **states_generated**: `NOT APPLICABLE — equilibrium displaced, nothing generated`.
  Nothing was computationally generated. What the paper does is displace the receptor's
  photostationary equilibrium into the active state and then trap it. Two displacement
  routes are used: (i) reconstitute with 9-*cis* retinal and illuminate at >495 nm to
  drive isomerisation to all-*trans* (9EPR); (ii) reconstitute directly with the
  non-natural agonist ATR6.11, which needs no illumination (9EPP/9EPQ). The G-protein
  heterotrimer plus apyrase then traps the nucleotide-free active complex.
  **Experimental analogue worth recording:** from one purified jsGiq sample the authors
  *separated* two distinct conformations by 3D classification — "With 3D classification,
  cryo-EM maps for two conformations of the JSR1-jsGiq complex were separated and
  independently refined" (p3) — so the deposited output is **two conformers of one
  functional state**, not two functional states. Both 9EPP and 9EPQ are active-state
  complexes. The inactive state is taken from the previously deposited crystal structure
  6I9K, not determined here.
- **structural_priors_used**: **Extensive, explicit, and — per the v3 note — not a defect.**
  This is a wet-lab paper and deposited structural knowledge shaped it at design time in
  five separate ways:
  1. **Chimera design from their own solved structure.** "we decided to create a human
     Gi/jumping spider Gq chimera (jsGiq) by engineering hGi to match the sequence of jsGq
     at the interface where the hGi protein contacts the receptor **based on our JSR1-hGi
     cryo-EM structure**" (p2). The construct in 9EPP/9EPQ was designed from 9EPR.
  2. **Starting models for 9EPP/9EPQ.** "The initial model of JSR was obtained from the
     crystal structure of the inactive state (6I9K), and the initial model for the jsGiq
     heterotrimer was obtained from the crystal structure of the human Gi heterotrimer
     (6CRK). Residues in the Gai subunit were mutated to match the jsGiq sequence." (p11)
  3. **Starting models for 9EPR.** "A sharpened and locally filtered volume was rigidly
     fitted in UCSF Chimera59 with dark state JSR1 (6I9K), Gαi1 (PDB: 6PT0), and Gβ1γ1
     dimer (PDB: 6OY9)." (p11)
  4. **Ligand pose modelled by analogy to a deposited active structure.** This is the one
     prior that directly shapes a reported result: "The density for the β-ionone ring of
     ATR6.11 is not sufficiently well defined to determine its orientation based on the
     experimental cryo-EM map alone. We have therefore modeled it rotated 180° relative to
     that of the 9-cis retinal β-ionone ring, **which is consistent with the pose observed
     for all-trans-retinal in the active bovine rhodopsin metarhodopsin-II structure**"
     (p4). The subsequent statement "This pose of ATR6.11 agrees with that of all-trans-
     retinal in the active metarhodopsin-II state of bovine rhodopsin" (p4) is therefore
     partly circular by construction, and the paper says so plainly in the first sentence.
  5. **A curated comparison set of deposited structures** (p11), listed verbatim: inactive
     — JSR1 (6I9K), bovine rhodopsin (1GZM), squid rhodopsin (2Z73); active GPCR-G protein
     — bovine rhodopsin-Gαt peptide (4A4M), (3PQR), bovine rhodopsin-Gi (6CMO), bovine
     rhodopsin-mini Go (6FUF), bovine rhodopsin-Gαt peptide (5EN0), β2AR-Gs (3SN6),
     M1-G11 (6OIJ), NTSR1-Gi NC (6OSA); AHD comparison — GABA(B)-hGi (7EB2), NTSR1-hGi
     (7L0S), CB2-hGi (6PT0). Superposition uses fixed TM residue ranges (Ballesteros-
     Weinstein 1.45–1.54, 2.46–2.56, 3.34–3.44, 4.48–4.56, 7.38–7.46; p11) — a stated,
     reproducible alignment definition, which is better practice than most.
- **oracle_leakage**: `NOT APPLICABLE` **as pipeline leakage — there is no prediction
  pipeline into which knowledge of a target-state structure could leak** (protocol
  described p9–p11). Enumerating the seven v3 routes anyway, so the claim is checkable
  rather than waved away:
  1. *Structures used as input or template* — **PRESENT but not leakage.** 6I9K, 6CRK,
     6PT0, 6OY9 are starting models for real-space refinement against experimental density
     (p11). In cryo-EM this is standard and the experimental map is the arbiter. Recorded
     under `structural_priors_used`, not here. **The one place it edges toward a
     conclusion is the β-ionone ring** (route detail 4 above, p4), where the model is
     placed by analogy because the density does not decide — the authors flag this
     themselves.
  2. *State annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
     or alignments* — **NONE FOUND.** GproteinDb is cited (ref 38, p12) but only as the
     source of the **G-protein generic residue numbering scheme** ("the superscript
     corresponds to the G protein general residue number38", p5); no state annotation and
     no alignment or template is drawn from it. Protocol: p11, "Structure alignment".
  3. *Cluster labels derived from known states* — **NONE FOUND.** 3D classification is
     unsupervised over the experimental particle set: "Ab initio models were generated with
     cryoSPARC and 3D classification was performed to separate different conformations of
     the complex" (p11). Classes were not labelled against any known state.
  4. *Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states*
     — **NONE FOUND.** Processing parameters are stated as fixed (CTF fit cutoff 8 Å,
     FSC = 0.143, defocus −1.0 to −2.4 µm, p10–11) and none is described as chosen by
     reference to a reference structure. No sweep of any kind is reported. Protocol p10–11.
  5. *Success defined post hoc by RMSD or TM to a structure they had* — **NONE FOUND.** No
     RMSD or TM-score to any reference is reported anywhere in the paper. Success is map
     resolution and model-to-density fit. Protocol p11.
  6. *Best/worst model labels assigned against a held reference* — **NONE FOUND.** The two
     jsGiq conformers are ranked by **experimental** criteria — contact counts and density
     quality, not agreement with a reference: "we conclude that JSR-jsGiq_1 represents a
     tighter, more engaged conformation of the G protein than JSR-jsGiq_2" (p7), on 31 vs
     18 total receptor–Gα interactions and 8 vs 5 C-hook contacts. The choice to "focus on
     the JSR1-jsGiq_1 structure due to its higher resolution" (p3) is a resolution
     criterion, not a reference criterion.
  7. *Design-level oracle use — inputs or systems chosen because the expected answer is
     already known* — **PRESENT, weakly, and it is design-level only.** Three instances:
     (a) the jsGiq chimera's substituted residues were chosen from the receptor-contact
     interface **seen in their own JSR1-hGi structure** (p2) — the interface was known
     before the interface was resolved at higher resolution; (b) the β-ionone ring
     orientation was set to match metarhodopsin-II because the experimental map could not
     decide (p4); (c) the whole experiment is designed so the answer is an active state —
     agonist plus G protein plus apyrase — and the active state is what is reported.
     (c) is not a defect: it is how a GPCR-G-protein complex is prepared, and the paper is
     transparent about all three. **Label this `design-level-oracle`, never `oracle-leak`.**
- **prospective**: `NOT APPLICABLE` — the prospective/retrospective distinction presupposes
  a prediction whose truth is checked afterwards. **Nearest honest answer:** the structures
  themselves are genuinely new experimental observations, not retrospective reproductions
  of anything ("Structures of bistable opsins in the activated state have proven elusive",
  p1). The *interpretation* is retrospective in that every activation motif is read against
  previously deposited class A structures (p5, p7, p11). One prediction is made and left
  untested: "We hypothesize that selectivity for Gi proteins could be achieved through a
  stable packing in TM6/TM7 that locks TM6" (p9).
- **state_metric**: **DUAL — `continuous coordinate` + `visual only`.**
  - *Continuous coordinate*: interatomic distances in the retinal pocket, helix-rotation
    angles, translational shifts, residue counts within 4 Å, and interaction counts. All
    values with pages are tabulated below.
  - *Visual only*: **the central activation claim — the outward movement of TM5/TM6 — is
    never given a number anywhere in the main text.** It is asserted and shown as a render
    with arrows (Fig 1e, p3; Fig 5, p8): "The outward movement of TM5 and TM6 relative to
    the inactive state opens a cytoplasmic cleft" (p3); "In the two conformations of the
    jsGiq complex, the outward movement of TM5 and TM6 is larger than in the hGi complex"
    (p6); "in the JSR1-jsGiq structures, the outward movement of TM5 and TM6 is even larger"
    (p9). **Larger than what, by how many ångström, is not stated** — the supporting panel
    is Supplementary Fig. 14, which is not held.
  - **Thresholds**: `NOT REPORTED`. No cut-off defines "active", "engaged", "outward" or
    "shallow"; no distance criterion defines the tabulated contacts (the contact-counting
    criterion behind "31 interactions" vs "18 interactions", p7, is in Supplementary Tables
    2–3, not held). The one stated numeric criterion in the paper is the 4 Å shell used for
    retinal-contacting residue counts (p4).

  **Every geometric measurement of activation reported, with page:**

  | Measurement | Inactive / reference | Active / comparison | Page |
  |---|---|---|---|
  | Schiff base (PSB) to Tyr126³·²⁸ distance | 2.9 Å (inactive JSR1, 6I9K) | **3.5 Å** (JSR1-jsGiq_1) | p5, Fig 2c/d p4 |
  | Schiff base (PSB) to Ser199⁴⁵·⁴⁹ distance | 3.9 Å (inactive) | **5.7 Å** (active) | p5, Fig 2c/d p4 |
  | Retinal-contacting residues within 4 Å, JSR1 | 15 (9-*cis*, inactive) | **7** (ATR6.11, active) | p4 |
  | Retinal-contacting residues within 4 Å, bovine rhodopsin | 15 (11-*cis*) | **8** (all-*trans*) | p4 |
  | α5-helix rotation between the two jsGiq conformers | JSR1-jsGiq_1 | **17°** in JSR1-jsGiq_2 | p6 |
  | AHD opening relative to Ras domain | JSR1-jsGiq_1 | **17° rotation toward the αN helix** in JSR1-jsGiq_2 | p7 |
  | Whole-G-protein rotation | JSR1-jsGiq_1 | **17°** in JSR1-jsGiq_2 | p9 |
  | TM6+TM7 combined shift toward ICL1 | JSR1-jsGiq_1 | **~2 Å** further in JSR1-jsGiq_2 | p6 |
  | C-hook contacts with receptor | 8 (JSR1-jsGiq_1) | 5 (JSR1-jsGiq_2) | p7 |
  | Total receptor–Gα interactions | 31 (JSR1-jsGiq_1) | 18 (JSR1-jsGiq_2) | p7 |
  | β-ionone ring rotation applied during modelling | — | **180°** relative to the 9-*cis* ring (modelled, not measured) | p4 |
  | **TM6 outward displacement (Å)** | — | **NOT REPORTED — asserted and rendered, never quantified** | p3, p6, p9 |
  | Residues unmodelled at cytoplasmic TM6 | — | 4 residues, Asp265⁶·²³–Lys268⁶·²⁶ | p3 |
  | Unassigned distance labels, Fig 2c (inactive) | 2.5, 2.3, 2.7, 2.6, 3.0, 3.9, 4.5, 2.9 Å | — | Fig 2c p4 |
  | Unassigned distance labels, Fig 2d (active) | — | 2.8, 2.9, 3.0, 4.6, 3.7, 5.7, 3.5 Å | Fig 2d p4 |

  The last two rows are the numeric labels printed in the Fig 2 panels; only the
  PSB–Tyr126³·²⁸ and PSB–Ser199⁴⁵·⁴⁹ pairs are assigned to atom pairs in the running text,
  so I do not assign the rest. Spectroscopic (non-geometric) values, for completeness:
  λmax 535 nm (JSR1 + 11-*cis*, inactive), 505 nm (JSR1 + 9-*cis*), 535 nm (active
  all-*trans*) (p2); E194⁴⁵·⁴⁴D causes an 8 nm blue shift (p7); S199⁴⁵·⁴⁹F gives λmax
  380 nm inactive / 540 nm active (p7, p9) — all from **previous** work, cited not measured
  here.
- **metric_saturation**: `NOT APPLICABLE` — no numeric score with a floor or ceiling is
  reported, so nothing can saturate. The GTP-depletion axis in Fig 1b runs 0–100 % and the
  highest condition (JSR1 + hGi) sits near ~77 %, so **that percentage metric does not
  ceiling** in the arms shown. The genuine limits in this paper — 4.1/4.2/4.9 Å resolution,
  unmodelled TM6 residues, side chains not resolvable in the AHD — are **resolving-power**
  limits, not metric saturation; they are recorded in `stated_limits`. Figure-level defects
  (single unlabelled time point in Fig 1b; TM6 movement with no quantitative panel) are in
  `hides` on the Fig 1B and Fig 5 rows, per v3 rule 9.
- **directional_control**: `NOT APPLICABLE` as a computational instruction handle. **The
  experimental handles are real, explicit and enumerable**, and this is the field's honest
  analogue:
  - **Ligand/chromophore**: ATR6.11, a non-natural all-*trans* retinal analog with agonist
    activity, drives the active state without illumination (p2, p10).
  - **Light**: 495 nm long-pass filtered illumination isomerises 9-*cis* → all-*trans*,
    driving activation (p2, p10). Reverse direction available in principle by a second
    photon (bistability), not exercised here.
  - **Dark / dim red light**: holds the inactive state (p9, p10).
  - **G-protein partner**: choice of jsGiq chimera vs human-Gαi1/bovine-Gβ1γ1 changes the
    trapped conformation — "the G protein subtype determines the extent of the TM6 movement
    rather than the mono- or bistability properties of the receptor" (p9).
  - **Nucleotide depletion**: apyrase traps the nucleotide-free state (p10).
  - **3D classification**: separates the two conformers post hoc; a *sorting* handle, not a
    steering one.
- **anti_memorization_design**: `NOT APPLICABLE` — no model is trained, so there is no
  training set to hold out from and no cutoff to define. The only date-sensitive object in
  the paper is the deposited comparison set (p11), which is prior art being compared
  against, not held-out data.
- **anti_memorization_control**: `NOT APPLICABLE` — same reason; `NONE RUN` would falsely
  imply a control was available and skipped.
- **controls_run**: **a substantial control set for a structural paper.** Table below;
  every row is a control arm actually run and reported, not merely available.

  | control | what it rules out | page |
  |---|---|---|
  | GTPase-Glo with **G protein alone** (hGi; jsGiq), no receptor | Receptor-independent basal hydrolysis as the source of signal; **establishes the jsGiq chimera retains intrinsic GTPase activity**, i.e. the engineered α5/C-hook swap did not break the enzyme | p2, Fig 1b p3, p11 |
  | GTPase-Glo with **JSR1 + G protein**, dark vs light-activated | That the increase is ligand-independent; establishes agonist-dependent catalysis of nucleotide exchange — "JSR1 bound to ATR6.11 triggers an increase in GTPase activity, confirming that the receptor is activated and can catalyze nucleotide exchange in jsGiq, similarly to hGi" (p3) | p2–3, p11 |
  | GTPase-Glo **reference samples: receptor alone** (0.2 µM JSR1 with 9-*cis* or ATR6.11, dark and light-activated) | Receptor-intrinsic luminescence contribution | p11 |
  | GTPase-Glo **no-protein control well** | Plate/reagent background; supplies Lum₀, the normalisation baseline in the stated GTP-hydrolysis formula | p11 |
  | **Octuplicate** replication of every condition + **Grubbs outlier test** | Single-well artefacts and outlier-driven means | p11, Fig 1b caption p3 |
  | **Two independent routes to the active state** — (i) 9-*cis* + 495 nm light → all-*trans*; (ii) direct ATR6.11 reconstitution | That the retinal pose is an artefact of the non-natural analog: "The JSR1-hGi map shows density for all-trans-retinal and overlays well with the ATR6.11 analog, indicating a similar binding pose for both ligands" (p4) | p2, p4 |
  | **Two different G-protein preparations** (chimeric jsGiq; human Gαi1/bovine Gβ1γ1) | That receptor features are an artefact of one particular G-protein construct; separates receptor-intrinsic from partner-dependent changes | p2, p6, p9 |
  | **Dim red light / light-controlled handling throughout**, including blotting and freezing under dim red light for JSR1-hGi | Stray-light or thermal activation contaminating the "inactive"-handled samples | p9, p10 |
  | **Apyrase (25 mU/mL)** in complex formation | Residual GTP/GDP leaving a nucleotide-bound population | p10 |
  | **3D classification into two conformers + cryoSPARC 3D variability analysis** | That one averaged map is hiding discrete heterogeneity; directly produced 9EPP vs 9EPQ | p3, p11 |
  | **SIDESPLITTER-coupled refinement; soft mask excluding the Gα AH domain; local CTF refinement** | Local over-fitting during reconstruction; AHD flexibility dragging global resolution | p11 |
  | **Micrographs with CTF fit resolution > 8 Å discarded**; FSC = 0.143 criterion | Poor-quality micrographs inflating apparent resolution | p10, p11 |
  | **Opsin sequence-conservation analysis** (202 vertebrate, 113 invertebrate sequences, Clustal Omega + WebLogo) | That the JSR1 substitutions (Trp at 6.44 instead of Phe; Ala/Ser at 6.47 instead of Cys; Tyr at 3.28 instead of Glu) are idiosyncratic to this receptor rather than clade-wide | p5, p11 |
  | **Comparison against a fixed, listed set of deposited inactive and active structures**, superposed on stated TM residue ranges | That the observed changes are crystallisation/detergent/method artefacts rather than activation | p5, p6, p11 |
- **confidence_as_discriminator**: `NOT APPLICABLE` — pLDDT, pTM and ipTM do not exist in
  this work; no predictor is run. **Experimental analogues used to judge model quality**:
  Fourier Shell Correlation at FSC = 0.143 for resolution (p11); local resolution to flag
  ICL3 and cytoplasmic TM6 as flexible (p3); and an explicit refusal to over-interpret
  where confidence is low — "four residues at the start of TM6 (Asp265⁶·²³-Lys268⁶·²⁶)
  could not be modeled into the experimental map with confidence and were, therefore,
  omitted from the atomic model" (p3), and "the resolution did not allow precise modeling
  of side chains" for the AHD (p3). **These were not validated as discriminators of
  conformational correctness**; they are standard map-quality measures.

## D. Claims

- **central_conclusion**: The first active-state structures of a bistable opsin bound to
  G-protein heterotrimers (JSR1 with an engineered human-Gi/spider-Gq chimera at 4.1 and
  4.2 Å, and with a human-Gαi1/bovine-Gβ1γ1 heterotrimer at 4.9 Å) show that JSR1 uses the
  same conserved class A activation microswitches (C-W-x-P, P-I-F, D/E-R-Y, N-P-x-x-Y) as
  vertebrate GPCRs, but keeps its Schiff base protonated through activation — because a
  bulky Tyr126³·²⁸ occupies the position of the vertebrate proximal counterion Glu³·²⁸ and
  leaves no room for the water that drives hydrolysis in bovine rhodopsin — with the
  PSB–counterion link remodelled onto an extended, water-mediated network to Glu194⁴⁵·⁴⁴
  from which Ser199⁴⁵·⁴⁹ withdraws. In several respects the D/E-R-Y environment resembles
  β2AR more than it resembles bovine rhodopsin, and the extent of TM6 movement tracks the
  G-protein subtype rather than mono- versus bistability.

- **necessity_claims** — **verbatim, with page**:
  - "In class A GPCRs, including JSR1, there are several known conformational changes in
    conserved micro-domains **required** for receptor activation." (p5)
  - "The conserved D/E3.49-R3.50-Y3.51 motif (Supplementary Fig. 12e) is **crucial** to
    stabilize the active state of the receptor and its interactions with the G protein."
    (p5)
  - "This is very similar to, for instance, the prototypical class A GPCRs bovine rhodopsin
    and human β2-adrenergic receptor, in which it was shown that this interaction is
    **critical** in forming the active state32,33." (p5)
  - "Formation of the cytoplasmic cleft in the activated receptor enables binding of the G
    protein, which is a **prerequisite** for catalysis of nucleotide exchange by the
    activated receptor." (p6)
  - "Monostable opsins, responsible for vision in vertebrates, release the chromophore
    after activation and **must** bind another retinal molecule to remain functional."
    (p1, abstract)
  - "The positively charged Schiff base **must** be stabilized by a nearby negatively
    charged amino acid residue termed the counterion." (p2)
  - "Understanding the nature of the retinal binding site is, therefore, **key** to
    determining how opsins have evolved to absorb specific wavelengths of light with high
    sensitivity and control of the isomerization product." (p2)
  - "The ability to maintain the Schiff base in a protonated state throughout the
    photocycle **ensures** thermal stability of the Schiff base in the active state and
    **allows** retinal to revert to the 11-cis form after a second photo-isomerization
    event, thereby conferring bistability to the receptor10,16." (p2)

  **Impossibility / failure statements — verbatim, with page** (these are the load-bearing
  "cannot be done" sentences, and two of them are the direct cause of the construct choices
  recorded above):
  - "However, it was **not possible** to identify conditions under which all-trans retinal
    would bind the receptor18." (p2) — *this is why ATR6.11 was used.*
  - "However, the production of active and pure jsGq for structural studies was **not
    successful**." (p2) — *this is why the jsGiq chimera exists. The native spider Gq
    complex was attempted and failed.*
  - "Several obstacles **prevented** the determination of a higher-resolution structure."
    (p2)
  - "Structures of bistable opsins in the activated state have **proven elusive**, limiting
    our understanding of how they function as bidirectional photoswitches." (p1, abstract)
  - "The density for the β-ionone ring of ATR6.11 is **not sufficiently well defined** to
    determine its orientation based on the experimental cryo-EM map alone." (p4)
  - "four residues at the start of TM6 (Asp2656.23-Lys2686.26) **could not be modeled** into
    the experimental map with confidence and were, therefore, omitted from the atomic
    model." (p3)
  - "the resolution **did not allow** precise modeling of side chains." (p3)
  - "Despite remodeling of the hydrogen bond network upon activation, the Schiff base
    remains protonated throughout the whole wild-type JSR1 photocycle12,16 and therefore
    **cannot be hydrolyzed**." (p7)
  - "the activity of JSR1 **cannot** be controlled precisely16." (p9)
  - "however further experimental evidence **is required** to confirm this observation."
    (p4, on the putative ordered waters)
  - "Thus, further engineering of JSR1 **is still required** to optimize its spectroscopic
    properties as an optogenetic tool." (p9)
  - "For optogenetic applications, further experiments **will be needed** to determine the
    signaling profile of JSR1 with different human G protein subtypes and homologs" (p9)

- **novelty_claims** — **verbatim, with page**:
  - "In this work, we **disclose the first structures of activated signaling complexes
    between a bistable opsin and G proteins**." (p9)
  - "Here we present active state structures of a bistable opsin, jumping spider rhodopsin
    isoform-1 (JSR1), in complex with its downstream signaling partners, the Gi and Gq
    heterotrimers." (p1, abstract)
  - "Structures of bistable opsins in the activated state have proven elusive, limiting our
    understanding of how they function as bidirectional photoswitches." (p1, abstract)
  - "However, critical aspects of their active-state conformation and interactions with
    downstream signaling partners **remain unexplored**. For instance, the lack of
    structural data on signaling complexes of bistable opsins has hindered the efforts to
    determine their activation mechanism and how they may revert back to the 11-cis-bound
    inactive state." (p2)
  - "This study lays the groundwork for future investigations into the activation dynamics
    of these unique light-sensitive receptors" (p2)
  - Note on the abstract's phrasing: **"in complex with its downstream signaling partners,
    the Gi and Gq heterotrimers" (p1) is the sentence most likely to be over-read.** The Gq
    arm is the **jsGiq chimera** — a human Gi scaffold carrying a spider Gq α5/C-hook — not
    a Gq heterotrimer, and the paper says as much on p2 and p10. The abstract does not carry
    that qualification.

- **Verbatim statements on what stabilises the active state in this bistable opsin** (the
  paper's own mechanistic core, quoted rather than paraphrased):
  - "The presence of a tyrosine instead of glutamate at this position **might contribute to
    the thermal stability of the Schiff base in the active state** JSR1 and other
    invertebrate opsins." (p4)
  - "In JSR1, this position is occupied by a bulkier Tyr1263.28, leaving no space for a
    water molecule at a similar position as is seen in the active bovine rhodopsin
    structures" (p4)
  - "The rotamer change of Arg1483.50 is further **stabilized by interactions with
    Tyr2345.58 and Tyr3317.53**." (p5)
  - "This arrangement allows Arg1483.50 to interact with the backbone oxygen of Cys351H5.23
    ... of the C-hook in jsGαiq (Fig. 4 ...) and **stabilize the active complex**." (p5)
  - "we propose a model in which **water molecules stabilized by Tyr2936.51 and Glu19445.44
    contribute to an extended hydrogen bond network linking the PSB and the counterion in
    the active state** (Fig. 6). The model is supported by resonance Raman experiments
    showing the presence of a water molecule that hydrogen bonds to the PSB in both the
    inactive 9-cis and active all-trans states16." (p7)
  - "Despite remodeling of the hydrogen bond network upon activation, the Schiff base
    remains protonated throughout the whole wild-type JSR1 photocycle12,16 and therefore
    cannot be hydrolyzed." (p7)
  - "This is consistent with this position being **important only for stabilizing the
    inactive state PSB**" (p7, on Ser199⁴⁵·⁴⁹)
  - "This cap is conserved in all opsins, but the structure of the cap can vary between
    receptors ... indicating that it **might be important for the stability of the retinal-
    binding pocket and receptor stability overall**." (p3, on the N-terminus/ECL2 cap)
  - "We hypothesize that **selectivity for Gi proteins could be achieved through a stable
    packing in TM6/TM7 that locks TM6, preventing it from moving further**, as observed in
    bovine rhodopsin" (p9)

- **Verbatim statements on how it differs from vertebrate / monostable rhodopsin**:
  - "In contrast to the monostable bovine rhodopsin, **the Schiff base in JSR1 is not
    deprotonated and hydrolyzed upon retinal isomerization to the all-trans
    conformation**2,12. The proximal counterion in monostable opsins, Glu3.28, together with
    a water molecule, is partially responsible for the hydrolysis of the Schiff
    base27–29." (p4)
  - "In monostable bovine rhodopsin, the Meta-II signaling state has a lowered pKa of the
    Schiff base resulting in deprotonation, which is followed by hydrolysis41. On the other
    hand, **JSR1 can maintain a thermostable Schiff base in both the inactive and active
    states, resulting in bistability**2." (p7)
  - "In bovine rhodopsin, the corresponding Tyr2235.58 points away from the transmembrane
    core in the inactive state and moves toward the transmembrane core in the active
    state32,33. **In contrast, in the inactive state of JSR1, this Tyr5.58 is already
    oriented towards the core and only changes its rotamer in the active state, more
    closely resembling the β2-adrenergic receptor**, a prototypical class A GPCR binding
    diffusible ligands" (p5)
  - "**Thus, the sequence and local structure of the D/E3.49-R3.50-Y3.51 motif and
    surrounding residues of the bistable JSR1 are more similar to those of
    non-photosensitive class A GPCRs than to the monostable light-sensitive bovine
    rhodopsin.**" (p5)
  - "**This indicates that, in some respects, bistable opsins are structurally more similar
    to non-photosensitive human class A GPCRs than to monostable opsins.**" (p9)
  - "Our structures show that the major activation microswitches (such as the C-W-x-P,
    P-I-F, N-P-x-x-Y, and E/D-R-Y motifs) follow the structural changes previously observed
    in other class A vertebrate GPCRs (Figs. 3, 4 ...). **This demonstrates that both
    invertebrate and vertebrate opsins (or vertebrate class A GPCRs) have similar
    evolutionary conserved activation mechanisms.**" (p7)
  - "In this motif, **JSR1 features a tryptophan instead of a phenylalanine at position
    6.44** ... while vertebrate opsins almost exclusively have the expected phenylalanine,
    invertebrate opsins mainly feature a tryptophan" (p5)
  - "The C6.47-W6.48-x-P6.50 motif is highly conserved in class A GPCRs, but **invertebrate
    opsins feature an alanine or serine at position 6.47 rather than cysteine**" (p5)
  - "9-cis retinal is tightly packed in the inactive state with 15 residues within 4 Å ...
    while ATR6.11 has only seven ... **This indicates that in the active state, water
    molecules surround the retinal in the retinal binding pocket and bridge interactions
    with nearby side chains.**" (p4)
  - "**Our structures indicate that the G protein subtype determines the extent of the TM6
    movement rather than the mono- or bistability properties of the receptor.**" (p9)
  - "Compared to other class A GPCR-hGi complexes, the JSR1-hGi complex shows a somewhat
    unusual binding pose of the human Gαi. The α5 helix adopts a somewhat shallower binding
    pose compared to other GPCR-hGi complexes" (p9)
  - "Unlike in many existing GPCR-G protein complexes, we observe a relatively ordered
    ICL3, including the cytoplasmic ends of TM5 and TM6." (p9)
  - "In contrast to other GPCR structures, we observe an elongated TM5 that interacts with
    the G protein." (p3)

- **stated_limits** (authors' own):
  - "Several obstacles prevented the determination of a higher-resolution structure.
    Firstly, steady state illumination of JSR1 generates a dynamic equilibrium of retinal
    in the 9-cis, 11-cis, and all-trans isomers with λmax within 30 nm of each other,
    producing a mixed population of active/inactive states due to back-isomerization16.
    Secondly, this JSR1-hGi complex was prone to dissociation during grid preparation,
    suggesting a low affinity between the receptor and the G protein heterotrimer; this
    also reduced the number of fully assembled complex particles in the EM dataset.
    Finally, the flexibility of the JSR1-hGi complex resulted in heterogeneity in the
    particle set, lowering the overall resolution of the cryo-EM map." (p2)
  - "Nevertheless, a structural model built based on this map still provides valuable
    insights" (p2) — i.e. the 4.9 Å JSR1-hGi model (**9EPR**) is offered as indicative, not
    definitive. Treat 9EPR accordingly.
  - "the Gα subunit shows a particularly high degree of flexibility that lowers the
    resolution in this area and, therefore, also the global resolution" (p3)
  - "Density for the α-helical domain (AHD) was observed in both JSR1-jsGiq maps, allowing
    rigid body fitting of the AHD into the map, but the resolution did not allow precise
    modeling of side chains." (p3)
  - "four residues at the start of TM6 (Asp2656.23-Lys2686.26) could not be modeled into
    the experimental map with confidence" (p3)
  - "These structural differences may reflect the ambiguity of modeling flexible side chain
    conformations at this resolution" (p4)
  - "The density for the β-ionone ring of ATR6.11 is not sufficiently well defined to
    determine its orientation based on the experimental cryo-EM map alone." (p4)
  - "This density may be attributed to one or two ordered water molecule(s) ... however
    further experimental evidence is required to confirm this observation." (p4)
  - "both JSR1-jsGiq models are incomplete at the cytoplasmic end of TM6" (p6)
  - "in three of the four existing structures of JSR1 there are missing or poorly resolved
    densities at different positions in this region [ICL3]" (p9)
  - "For optogenetic applications, further experiments will be needed to determine the
    signaling profile of JSR1 with different human G protein subtypes and homologs, e.g.,
    to measure G protein activation efficiency profiles." (p9)
  - "Thus, further engineering of JSR1 is still required to optimize its spectroscopic
    properties as an optogenetic tool." (p9)
  - **Not stated as a limit by the authors, but recorded here as an extractor observation:**
    the paper never flags that its two highest-resolution entries use an engineered chimeric
    Gα, or that its βγ pair differs between the jsGiq and hGi complexes, as a caveat on the
    generality of the conclusions.

- **stance**: `precedent + background` — **provisional, the user's call.**
  - *precedent on findings*: it is a clean, explicit reference for what an experimentally
    determined active-state GPCR–G-protein complex looks like, with a stated superposition
    definition and a full list of comparison PDB entries. It is exactly the kind of
    deposited active-state reference a prediction paper would score against — and this note
    is the record that **two of the three entries are chimeric constructs, so scoring
    against them scores against an engineered interface.**
  - *background on method*: it contains no structure prediction, so it cannot be a
    precedent, contrast or threat on any methodological axis of ours. It supplies target
    ground truth and construct provenance, nothing more.
  - Not `threat` (no competing method), not `negative-result`.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | PDB accession, JSR1-jsGiq_1 | **9EPP** | — | Protein Data Bank deposition | p12 |
  | PDB accession, JSR1-jsGiq_2 | **9EPQ** | — | Protein Data Bank deposition | p12 |
  | PDB accession, JSR1-hGi (without the AHD) | **9EPR** | — | Protein Data Bank deposition | p12 |
  | EMDB accession, JSR1-jsGiq_1 map | **EMD-19882** | — | Electron Microscopy Data Bank | p12 |
  | EMDB accession, JSR1-jsGiq_2 map | **EMD-19883** | — | Electron Microscopy Data Bank | p12 |
  | EMDB accession, JSR1-hGi map | **EMD-19884** | — | Electron Microscopy Data Bank | p12 |
  | Global resolution, JSR1-jsGiq_1 | 4.1 (refined value 4.06) | Å | FSC = 0.143, non-uniform refinement | p3, p11 |
  | Global resolution, JSR1-jsGiq_2 | 4.2 (refined value 4.17) | Å | FSC = 0.143, non-uniform refinement | p3, p11 |
  | Global resolution, JSR1-hGi | 4.9 (described in Results as "sub-5 Å") | Å | post-processing with soft mask excluding Gα AH domain | p2, p11 |
  | Resolution criterion | FSC = 0.143 | — | Fourier Shell Correlation | p11 |
  | Particles auto-picked, jsGiq dataset | 2,964,739 | particles | Topaz automated picking, full dataset | p11 |
  | Particles in good 2D classes, jsGiq | 768,100 | particles | 2D classification | p11 |
  | Particles in final map, JSR1-jsGiq_1 | 159,665 | particles | non-uniform refinement | p11 |
  | Particles in final map, JSR1-jsGiq_2 | 134,167 | particles | non-uniform refinement | p11 |
  | Particles extracted, hGi dataset | 8.4 million (binned ×3) | particles | crYOLO general model | p11 |
  | Good-quality particles retained, hGi | 1.2 million (**14 %** of initially picked) | particles | 2D classification in Relion | p11 |
  | Pixel size, jsGiq acquisition | 0.51 (binned ×2 to 1.02 during processing) | Å/pixel | K3 detector, Titan Krios 300 kV | p10, p11 |
  | Pixel size, hGi acquisition | 0.85 | Å/pixel | K3 detector, Titan Krios 300 kV | p10 |
  | Total dose, jsGiq | 70 | e⁻/Å² | 40 frames/micrograph, dose rate 19 e⁻/px/s | p10 |
  | Total dose, hGi | 50 | e⁻/Å² | 40 frames/micrograph, dose rate 19 e⁻/px/s | p10 |
  | Energy filter slit width | 20 | eV | GIF Quantum LS | p10 |
  | Target defocus range | −1.0 to −2.4, in 0.2 steps | µm | EPU automated acquisition | p10 |
  | Micrograph rejection threshold | CTF fit resolution > 8 discarded | Å | patch CTF estimation (multi) | p11 |
  | Sample concentration, JSR1-hGi | 1 | mg/ml | grid application | p10 |
  | Sample concentration, JSR1-jsGiq | 8 | mg/ml | grid application | p10 |
  | Blot time, JSR1-hGi / JSR1-jsGiq | 3 / 6 | s | Vitrobot Mark IV, 4 °C, 100 % humidity | p10 |
  | Receptor : G protein molar ratio | 1 : 1.25 | — | complex formation | p10 |
  | Apyrase concentration | 25 | mU/mL | complex formation | p10 |
  | Total receptor–Gα interactions, jsGiq_1 vs jsGiq_2 | 31 vs 18 | contacts | Supplementary Tables 2 and 3 (**not held**) | p7 |
  | C-hook contacts, jsGiq_1 vs jsGiq_2 | 8 vs 5 | contacts | Supplementary Tables 2 and 3 (**not held**) | p7 |
  | Retinal-contacting residues within 4 Å, JSR1 inactive vs active | 15 vs 7 | residues | 9-*cis* (6I9K) vs ATR6.11 (this work) | p4 |
  | Retinal-contacting residues within 4 Å, bovine rhodopsin | 15 vs 8 | residues | 11-*cis* vs all-*trans* | p4 |
  | PSB–Tyr126³·²⁸ distance, inactive → active | 2.9 → 3.5 | Å | 6I9K vs JSR1-jsGiq_1 | p5 |
  | PSB–Ser199⁴⁵·⁴⁹ distance, inactive → active | 3.9 → 5.7 | Å | 6I9K vs JSR1-jsGiq_1 | p5 |
  | α5-helix rotation between jsGiq conformers | 17 | degrees | JSR1-jsGiq_1 vs JSR1-jsGiq_2 | p6 |
  | AHD rotation toward αN helix | 17 | degrees | JSR1-jsGiq_1 vs JSR1-jsGiq_2 | p7 |
  | Whole G-protein rotation | 17 | degrees | JSR1-jsGiq_1 vs JSR1-jsGiq_2 | p9 |
  | TM6+TM7 shift toward ICL1 | ~2 | Å | JSR1-jsGiq_1 vs JSR1-jsGiq_2 | p6 |
  | GTP depletion, hGi alone | ~33 (read from Fig 1b; exact value in Source Data, **not held**) | % | no-protein control (Lum₀) | Fig 1b p3 |
  | GTP depletion, JSR1 + hGi | ~77 (read from Fig 1b) | % | no-protein control (Lum₀) | Fig 1b p3 |
  | GTP depletion, jsGiq alone | ~17 (read from Fig 1b) | % | no-protein control (Lum₀) | Fig 1b p3 |
  | GTP depletion, JSR1 + jsGiq | ~66 (read from Fig 1b) | % | no-protein control (Lum₀) | Fig 1b p3 |
  | Replicates per GTPase condition | 8 (octuplicate) | wells | Grubbs outlier test applied | p3, p11 |
  | Incubation times tested, GTPase assay | 30, 60, 120 | minutes | plate shaking at 500 rpm, 20 °C | p11 |
  | Vertebrate opsin sequences aligned | 202 | sequences | BLASTp vs human rhodopsin, Clustal Omega | p11 |
  | Invertebrate opsin sequences aligned | 113 | sequences | BLASTp vs jumping spider rhodopsin, Clustal Omega | p11 |
  | Superposition residue ranges (Ballesteros-Weinstein) | 1.45–1.54, 2.46–2.56, 3.34–3.44, 4.48–4.56, 7.38–7.46 | — | PyMOL structure alignment | p11 |
  | **TM6 outward displacement** | **NOT REPORTED** | Å | asserted qualitatively (p3, p6, p9); quantitative panel is Supplementary Fig. 14, **not held** | p3, p6, p9 |
  | B-factors, map-to-model CC, clash score, Ramachandran, EMRinger | **NOT REPORTED in main text** | — | Supplementary Table 1, **not held** | p3 (cited) |

  The four GTP-depletion percentages are **read off the rendered Fig 1b axis**, not stated
  numerically anywhere in the text; exact values are in the Source Data file, which is not
  held. They are marked "~" and should not be quoted as the paper's numbers.

- **n_predictions**: `NOT APPLICABLE` — nothing is predicted, so samples-per-target and
  total-predictions have no referent. **Experimental scale, recorded in the same three-part
  spirit:**
  - *Targets*: 1 receptor (JSR1), 2 G-protein preparations, 3 complexes.
  - *"Samples" per target*: 2,964,739 particles auto-picked for the jsGiq dataset, of which
    768,100 survived 2D and 159,665 / 134,167 entered the two final maps; 8.4 million
    particles extracted for the hGi dataset, of which 1.2 million (14 %) were retained (p11).
  - *Total deposited outputs*: 3 coordinate sets, 3 maps.
- **comparable_to_ours**: *(left empty by the extractor, per v3)*
- **si_in_scope**: **SI NOT HELD — and it removes the cryo-EM statistics table, the
  interaction tables and the chimera alignment.** Referenced and absent: Supplementary
  Figs 1–18 (notably Fig 1 sample prep/SEC, Fig 2 models, Figs 3–4 hGi processing,
  **Fig 5 the jsGiq chimera sequence alignment**, Fig 6 jsGiq classification and local
  resolution, Figs 9–10 retinal density and pocket comparison, Figs 11–13 microswitch
  comparisons, **Fig 14 the TM6/α5 outward-movement comparison**, Fig 15 ICL3, Fig 16 AHD,
  Fig 17 S199F spectra, Fig 18 TM6/TM7 packing); **Supplementary Table 1 = cryo-EM data
  collection and refinement statistics**; Supplementary Tables 2 and 3 = per-residue
  receptor–Gα interaction lists; Supplementary Table 4 = **exact protein sequences and
  their sources** ("Exact protein sequences and their sources are summarized in
  Supplementary Table 4", p11); Supplementary Movies 1–8; and the Source Data file
  underlying Fig 1b. **Consequence for the construct question:** Supplementary Table 4 and
  Supplementary Fig. 5 are the definitive construct documents and neither is held, so the
  construct table above is built from the Methods prose on p9–p10 alone. That prose is
  detailed enough to be decisive on chimera identity, but a residue-by-residue construct
  audit requires the SI.

## F. Figures

Six main-text figures, split into **8 panel-group rows** by the v3 rule (split on `mark` or
`measure`, not on `facet`). Figures 1a, 1c–e, 2, 3, 4 and 5 are all structure renders or
schematics; only Fig 1b carries a dependent measure.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | Chemical structures of all-*trans*-retinal and the synthetic analog all-*trans* retinal 6.11, both drawn with a protonated Schiff base linkage — the ligand-identity panel for the whole paper | schematic | `SCHEMATIC \| two 2D chemical structures of retinal isomers/analogs with PSB linkage \| no data` | 1 panel, 2 stacked structures; varies by chemical species | — | CC BY 4.0, no ND, p13 |
| 1B | 3 | GTPase-Glo assay: GTP depletion for hGi and jsGiq, each with and without JSR1•ATR6.11 — the functional control establishing the jsGiq chimera is active and receptor-responsive | box | `PLOT \| facet: none (1) \| vary: sample condition (4: hGi, JSR1 + hGi, jsGiq, JSR1 + jsGiq) \| series: none (1) \| measure: GTP depletion (%) \| mark: box \| n: 8 per mark (octuplicate), 32 per panel` | 1 panel, 4 conditions; conditions vary by G-protein construct × receptor presence | **Caption says "mean values +/− standard deviation" but the drawn glyph is a box-and-whisker, so the stated statistic and the plotted statistic do not match.** Methods state incubations of "30, 60, or 120 minutes" (p11) but the panel is a **single unlabelled time point** — which one is never stated, and the other two are never shown. Exact values only in the unheld Source Data. No axis break; y runs 0–100 | CC BY 4.0, no ND, p13 |
| 1C-E | 3 | Cryo-EM map of JSR1-jsGiq_1 coloured by subunit (c); overall atomic model with retinal-site and G-protein-site insets (d); overlay of inactive JSR1•9-*cis* (6I9K) on active JSR1•ATR6.11 in side and cytoplasmic views, with arrows on TM5/TM6 (e) | structure render | `RENDER \| facet: representation (3: density map, model + insets, inactive/active overlay) \| views: 2 (side, cytoplasmic) \| overlay: 1 prediction on 1 reference \| axis: none` | 3 panels (c, d, e); e itself holds 2 camera views; panels vary by representation and by camera angle | Panel e asserts the outward movement of TM5/TM6 with arrows and **no distance annotation** — the paper's central activation claim has no number in any main-text panel | CC BY 4.0, no ND, p13 |
| 2A-D | 4 | Retinal binding site, inactive vs active: all-*trans*-retinal (from JSR1-hGi) overlaid on ATR6.11 (from JSR1-jsGiq_1) (a); 9-*cis* vs ATR6.11 with the Lys321⁷·⁴³ Schiff base and the ATR6.11 density (b); the PSB–counterion environment in the inactive state with distances (c) and in the active state with distances (d) | structure render | `RENDER \| facet: comparison (4: ligand-vs-ligand, isomer-vs-analog, inactive environment, active environment) \| views: 1 \| overlay: 2 structures on 1 reference \| axis: none` | 4 panels (a–d); panels vary by which pair of structures is compared; c and d share the same residue set so they read as a matched pair | Panels c and d print 8 and 7 distance labels respectively, but **only two of those distances are assigned to named atom pairs in the running text** (PSB–Tyr126³·²⁸, PSB–Ser199⁴⁵·⁴⁹); the rest cannot be attributed from the figure alone. The active-state ligand shown is the **non-natural ATR6.11**, and the β-ionone ring in it is a **modelled** orientation, not one resolved by the map (p4) — the caption does not say so | CC BY 4.0, no ND, p13 |
| 3A-F | 6 | Microswitch comparison, bistable JSR1 (left column) against monostable bovine rhodopsin (right column), each inactive vs active: C-W-x-P / retinal-Trp⁶·⁴⁸ (a, b), P-I-F (c, d), D/E-R-Y (e, f) | structure render | `RENDER \| facet: motif (3: CWxP, PIF, DRY) × receptor (2: JSR1, bovine rhodopsin) \| views: 1 \| overlay: 1 active on 1 inactive per panel \| axis: none` | 6 panels in a 3 × 2 grid; rows vary by motif, columns vary by receptor; every panel overlays an inactive and an active structure | No distances or angles are annotated on any panel — every microswitch change is shown, none is measured. Structures compared are named in the caption (6I9K, this work, 1GZM, 5EN0) | CC BY 4.0, no ND, p13 |
| 4A-B | 7 | Whole-receptor activation summary: inactive JSR1 (6I9K) and active JSR1-jsGiq_1 side by side, each annotated with callouts naming the retinal, the CWxP Trp, the PIF motif, Tyr234⁵·⁵⁸/Tyr331⁷·⁵³, the ionic lock state, and (active only) the Arg148³·⁵⁰–Cys351^H5.23 hydrogen bond and the TM5/TM6 outward movement | structure render | `RENDER \| facet: activation state (2: inactive, active) \| views: 1 (membrane-normal, extracellular top) \| overlay: 0 predictions on 1 reference per panel \| axis: none` | 2 panels (a, b); panels vary by activation state; each carries 5–6 text callouts rather than data marks | The panel is a labelled cartoon of the mechanism: **"Outward movement of TM5 and TM6" is a text callout with no magnitude**, and "Open Ionic Lock" / "Closed Ionic Lock" are categorical labels with no distance behind them | CC BY 4.0, no ND, p13 |
| 5A-D | 8 | G-protein binding site compared across the three structures: JSR1-jsGiq_1 vs JSR1-hGi from the side (a) and from the cytoplasm (b); JSR1-jsGiq_1 vs JSR1-jsGiq_2 α5-helix relative rotation with axis arrows and the 17° label (c) and the same pair viewed at the binding site (d) | structure render | `RENDER \| facet: structure pair (2: jsGiq_1 vs hGi, jsGiq_1 vs jsGiq_2) \| views: 2 (side, cytoplasmic) \| overlay: 1 structure on 1 reference per panel \| axis: none` | 4 panels (a–d); panels vary by which pair of structures is superposed and by camera angle; only the α5 helix of Gα is drawn in a, c, d | Carries the paper's comparative claims — "the outward movement of TM5 and TM6 is larger than in the hGi complex" (p6), "a shallower binding pose" (p9) — with **only one number on the whole figure (17°) and no per-helix displacement anywhere**. The quantitative version is Supplementary Fig. 14, which is not held | CC BY 4.0, no ND, p13 |
| 6 | 8 | Schematic of the PSB–counterion hydrogen-bond network, inactive (left) vs active (right): Glu194⁴⁵·⁴⁴, Ser199⁴⁵·⁴⁹, Tyr293⁶·⁵¹, waters and the PSB, showing Ser199⁴⁵·⁴⁹ leaving the network on activation | schematic | `SCHEMATIC \| proposed water-mediated hydrogen-bond network linking PSB to counterion, inactive vs active \| no data` | 2 panels (inactive, active); panels vary by activation state | This is explicitly a **proposal**, not an observation — "We propose that Ser199⁴⁵·⁴⁹ does not participate in this network in the active state" (caption, p8) and "possibly Tyr293⁶·⁵¹" — and the waters drawn were not resolved ("This density may be attributed to one or two ordered water molecule(s) ... however further experimental evidence is required", p4). A reader taking Fig 6 as a determined structure would be over-reading it | CC BY 4.0, no ND, p13 |

**Licence, verbatim, p13:** "Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing, adaptation, distribution
and reproduction in any medium or format, as long as you give appropriate credit to the
original author(s) and the source, provide a link to the Creative Commons licence, and
indicate if changes were made." **CC BY 4.0 — no NonCommercial clause, no NoDerivatives
clause.** Redrawing and modification are permitted with attribution. One caveat also
verbatim from p13: "The images or other third party material in this article are included
in the article's Creative Commons licence, unless indicated otherwise in a credit line to
the material." No such credit line appears on any of Figs 1–6, so all six are covered.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), schema v3 pass
- **schema_version**: `v3`
- **confidence**: **high** on identity, constructs, accession codes, resolutions, claims and
  licence — the Methods are unusually explicit about the chimera and the sequence of every
  substituted segment is printed in the running text on p10, so the construct question is
  answerable from the main PDF alone without the SI. **Medium** on the figure `n` and mark
  details for Fig 1b (mark type read from a 150 dpi render, not stated in the caption;
  the four percentage values are read off an axis, not printed) and on the assignment of
  the unlabelled distance annotations in Fig 2c/d. **Low** on anything routed to the SI:
  cryo-EM refinement statistics, the residue-level interaction tables, the chimera
  alignment figure, and the TM6-displacement comparison. The text layer of the PDF is clean
  throughout; superscript GPCR residue numbers run together with residue names
  (`Tyr1263.28` = Tyr126³·²⁸, `Lys3217.43` = Lys321⁷·⁴³) but are unambiguous.
- **unresolved**:
  1. **The "without the AHD" clause on p12 is grammatically ambiguous** as to whether it
     modifies JSR1-hGi alone or all three depositions. The body text (p7, p11) supports
     "JSR1-hGi alone", and that is what the construct table records, but the deposition
     sentence itself does not settle it. Verifying requires the PDB entries.
  2. **The accession codes appear exactly once in the whole paper** (p12). There is no
     second occurrence in any figure caption, Methods paragraph or table to cross-check
     against, so the name→code mapping rests on a single sentence. No contradiction was
     found; equally, no corroboration exists.
  3. **The number 17° appears three times for what may or may not be three different
     things**: the α5-helix rotation between the two jsGiq conformers (p6), the AHD rotation
     toward the αN helix (p7), and "a G protein rotation by 17°" (p9). These may be three
     independent measurements that coincide, one measurement described three ways, or a
     transcription of one value into three contexts. The paper does not distinguish them and
     I do not resolve it.
  4. **Which incubation time Fig 1b shows** is not stated. Methods list 30, 60 and 120 min
     (p11); the figure shows one unlabelled time point.
  5. **The contact-distance criterion behind "31 interactions" vs "18 interactions" and
     "eight" vs "five" C-hook contacts** (p7) is not given in the main text; it lives in
     Supplementary Tables 2 and 3, not held. The counts are therefore not reproducible from
     the held document.
  6. **TM6 outward displacement is never quantified.** This is the most-cited single number
     for GPCR activation and the paper's comparative claims about it (jsGiq > hGi;
     JSR1 > bovine rhodopsin) rest entirely on a supplementary figure that is not held.
  7. **Tag I needed and could not use.** There is **no tag in the v3 vocabulary for an
     engineered chimeric or otherwise non-native construct.** `g-protein-mimetic` is the
     nearest and is **wrong** — a mimetic is a mini-G protein, a nanobody or a synthetic
     surrogate; jsGiq is a chimera of two genuine Gα proteins with a real, GTPase-competent
     nucleotide-binding core, and the note's whole point is that mislabelling it would
     propagate the exact error the corpus is trying to make checkable. I have **not**
     invented one. Suggested addition under **Control** or a new **Construct** group:
     `chimeric-construct` (an engineered hybrid of two natural proteins), and possibly
     `non-native-complex` (a complex assembled across species or from separately purified
     non-cognate subunits — which would also catch the human-Gαi1 + bovine-Gβ1γ1 heterotrimer
     in 9EPR). Without one of these, a reverse lookup for "which corpus papers deposit
     chimeric constructs" returns nothing, and this paper is precisely the case that lookup
     exists for.
  8. **Second tag gap, smaller:** there is no publication tag for *version of record with a
     public peer-review file*. `peer-reviewed` is correct and sufficient; noting only that
     the peer review file (p13) is a citable object the corpus has no slot for.
  9. **Schema ambiguity in v3, reported bluntly** (see the closing note below).
- **why_it_matters**: *(left empty by the extractor, per v3)*

---

## Tags

`gpcr` `experimental` `single-state` `orthosteric` `directed-state` `ligand-driven`
`partner-driven` `continuous-metric` `visual-metric` `design-level-oracle` `peer-reviewed`
`precedent` `background` `comparator-numbers`

Tag notes, so the choices are auditable:

- `experimental` — the paper contains no structure prediction at all; this is exactly the
  case the v3 tag was added for, and it is why section C is mostly `NOT APPLICABLE`.
- `single-state` — all three deposited structures are **active**-state complexes. The two
  jsGiq entries are two *conformers of one state*, not two states; the inactive state is
  taken from previously deposited 6I9K and was not determined here. `two-state` would be
  wrong.
- `directed-state` + `ligand-driven` + `partner-driven` — the active state is reached and
  held by an agonist (ATR6.11, or all-*trans* generated by 495 nm illumination), by the
  G-protein partner, and by nucleotide depletion. All three handles are exercised.
- `continuous-metric` + `visual-metric` — both, matching the dual `state_metric`: real
  continuous geometry (distances, angles, contact counts) for the retinal pocket and the
  G-protein interface, but the headline TM6/TM5 activation movement is called by eye from
  renders with no number in any main-text panel.
- `design-level-oracle`, **not** `oracle-leak` — route 7 only, and weakly: the chimera
  interface was chosen from their own prior structure, the β-ionone orientation was modelled
  to match metarhodopsin-II because the density could not decide, and the experiment is
  designed so that the active state is the answer. There is no prediction pipeline, so
  pipeline leakage is not merely absent but inapplicable.
- `orthosteric` — the retinal binding site is the orthosteric pocket of this receptor and is
  the paper's main structural subject. No allosteric small-molecule site is studied, so no
  `allosteric-site` / `cryptic-pocket` / `allosteric-failure`.
- `comparator-numbers` — the resolutions, the pocket distances, the 4 Å contact counts and
  the interface contact totals are numbers our results could sit beside in a table, with the
  construct caveat above attached.
- `precedent` + `background` — see `stance`; provisional.
- **Deliberately not used**: `experimental-validation` (that tag marks a *computational*
  paper that tested a prediction in the lab; this paper is not computational and applying it
  would false-positive every query for prediction-plus-validation papers);
  `g-protein-mimetic` (jsGiq is a chimera, not a mimetic — see `unresolved` item 7);
  `prospective`, `anti-memorization`, `no-anti-memorization`, `unpowered`,
  `confidence-as-discriminator`, `multi-backbone` (all presuppose a prediction pipeline);
  every Protocol tag (`no-template-no-msa`, `templates-on`, `state-annotated-input` — these
  describe prediction input regimes and would join this note falsely against biasing papers);
  every Method tag except `experimental`; `preprint`; `figure-exemplar`; `negative-result`.

---

## Note to whoever is tuning the schema

Blunt, as EXTRACT_PROMPT.md asks. Points 1 and 2 cost real time on this paper.

1. **v3 has no way to record a construct.** This is the largest gap I hit. For an
   experimental paper, *what was actually in the tube* is the single most consequential
   fact, and it determines whether every downstream use of the deposited coordinates is
   valid. v3 has `system`, `n_targets` and `structural_priors_used`, and none of them holds
   "human Gαi1 with residues 337–354 replaced by jumping-spider Gαq1". I had to invent a
   pre-section table above section A to carry it. **Suggest a `constructs` field in
   section B**, specified as a table with columns `deposited id` | `receptor construct` |
   `partner construct` | `chimera?` | `ligand / cofactor state` | `page`, populated for every
   experimental paper and `NOT APPLICABLE` for pure prediction papers. Without it, the corpus
   cannot answer "is this reference structure native?" — which is the question that makes a
   deposited entry safe or unsafe to score against.
2. **Section C's `NOT APPLICABLE` guidance is thin for `experimental` papers.** v3 added the
   `experimental` tag and one worked phrase for `states_generated`, but the other eleven
   fields in section C still read as if a pipeline exists, so each one needs a bespoke
   sentence explaining why it does not apply. Five of the twelve have honest experimental
   analogues (`directional_control` → agonist/light/partner/nucleotide handles;
   `confidence_as_discriminator` → FSC and local resolution; `state_metric` → geometry;
   `oracle_leakage` route 7 → design choices; `controls_run` → works directly). Suggest v4
   state, once, that for `experimental` papers section C is answered as
   `NOT APPLICABLE — <reason>` plus an optional experimental analogue, rather than leaving
   each extractor to improvise the convention. Two extractors will otherwise write it two
   ways.
3. **`state_metric` conflates "how a state is *called*" with "what geometry is *reported*".**
   For a wet-lab paper the state is not called by a metric at all — it is established by
   construction (agonist + partner + nucleotide depletion). The measurements are the
   *output*, not the discriminator. I used the dual form to record both, and the dual half
   that matters here is that the headline number is missing. That worked, but the field name
   points the wrong way for experimental papers.
4. **RENDER's `overlay` slot is under-specified for the common case of superposing two
   experimental structures.** The slot reads "`<k or NOT REPORTED>` predictions on `<n>`
   reference(s)", but Figs 2, 3 and 5 overlay two *deposited experimental* structures with
   no prediction anywhere. Writing "1 prediction on 1 reference" is literally false. I wrote
   "1 structure on 1 reference" and "2 structures on 1 reference"; **suggest v4 rename the
   slot content to `<k> structures on <n> reference(s)`**, which covers predictions and
   experiments alike without changing the join.
5. **The panel-split rule needs a line for renders that carry printed annotations.** Fig 2c
   and 2d are structure renders with 8 and 7 numeric distance labels printed on them. They
   carry real measured values but have no axes, so they are RENDER, not PLOT — I am confident
   that is right, and a `MATRIX`/`PLOT` reading would put a variable in the wrong slot. But
   v3 never says so, and an extractor who reads "carrying no measured data" in the SCHEMATIC
   definition might infer that annotated renders belong elsewhere. One sentence would settle
   it: annotations do not make a render a plot; the presence of a *data axis* does.
6. **Minor:** `reuse` asks for "the page the license appears on", which for a Nature journal
   is always the last page and is the same for every figure. Eight identical cells. Consider
   allowing a single paper-level licence statement with the figure rows inheriting it.
