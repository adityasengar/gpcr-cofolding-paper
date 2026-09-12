# SEQUENCES.md — every sequence the redo supplies to a model

Written 2026-09-11 by the sequence-specification session. Companion to
`redo/spec/CATALOGUE.md` (the experiment list) and to the two
sibling documents `redo/spec/PANEL.md` (which receptors) and
`redo/spec/RUN_MATRIX.md` (how many predictions, what they cost). **This
file owns constructs only.** Where a decision belongs to a sibling it is written
as a dependency, not resolved here.

**Nothing below is written from memory.** Every sequence is either sliced from a
fetched UniProt record (accession + sequence version + last-sequence-update date
recorded), sliced from an RCSB entity, or constructed from one of those by a
stated rule. Every construct carries a sha256. Machine-readable companions,
regenerable:

| file | what |
|---|---|
| `redo/build/seq_build.py` → `seq_constructs.tsv` | the 17 Gα records, CGN segment boundaries, per-family α5-CT |
| `redo/build/seq_rungs.py` → `seq_rungs.tsv` | every ladder rung × 16 human Gα families, 112 constructs |
| `redo/build/seq_controls.py` → `seq_controls.tsv` | 240 peptide-rung controls (reversed, poly-Ala, scrambles, face-preserving scrambles, helicity-matched) |
| `redo/build/seq_a5null.py` → `seq_a5null.tsv` | the three α5-null full-subunit variants × 7 families (21 constructs) |

Fetch date for every UniProt and RCSB record below: **2026-09-11**.

---

## 0. The three conventions, and why each exists

### 0.1 Constructs are keyed by hash, never by header

```
construct_id = sha256(uppercase one-letter sequence, UTF-8, no header, no newline, no whitespace)
```

This is not a preference. It is the convention that **reproduces all ten Gα
entries in the pipeline's own `partners.fasta`** (§2 below), and it is the check
that the project has twice failed to run:

- `partners.fasta:Nb60` carries the **Nb80** CDR3, and `partners.fasta:GASR` is
  the gastrin *receptor*, not a Gα
  (`data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md`, findings G and N).
- A third, not previously recorded: **`partners.fasta:arrestin_FL` is not the
  arrestin finger loop.** Its 15 bytes reproduce exactly as β-arrestin-1
  (UniProt P49407, SV 3) **residues 22–36**, `LGKRDFVDHIDLVDP`. UniProt's own
  feature table (P49407, SV 2, 418 aa) puts residues 16–43 in four β-strands of
  the N-domain β-sandwich, and puts the receptor-interaction region
  (`Interaction with CHRM2`) at 45–86. So the entry is a β-strand fragment
  labelled as a loop, and
  "FL" cannot be read as "full length" either — arrestin is ~418 residues.

Three mislabels in one 29-entry file. Every arm in the redo must resolve its
chain by hash and fail loudly on a miss.

### 0.2 Length is expressed from the C terminus, never as a residue range

**"Gα residues 334–354" is correct only for Gi1.** It is currently written into
`analysis/block_b/DATA_REQUESTS.md:221` and `rebuttals/BLOCK_B.md:479`. For Gs
(394 aa) that range ends **40 residues short of the C terminus** and would
supply a fragment of the H4 helix instead of the α5-CT.

The correct general form, and the two CGN facts that make it exact:

| rung | rule | resolved length | uniform across families? |
|---|---|---|---|
| `ct11` | last 11 residues | 11 | yes |
| `ct15` | last 15 residues | 15 | yes |
| `ct21` | last 21 residues | 21 | yes |
| `a5helix` | CGN segment **G.H5** | **26** | **yes — verified on all 16 human Gα** |
| `a5plus` | CGN **G.S6** → C terminus (β6–s6h5–α5) | **36** | **yes — verified on all 16 human Gα** |

Both invariants were computed here from GproteinDb's CGN residue tables
(`https://gpcrdb.org/services/residues/{entry_name}/`, fetched 2026-09-11) for
all 16 human Gα subunits. G.H5 ends at the last residue in every one, and
G.S6 begins at L−35 in every one. So the two "~" figures in the catalogue can be
made exact: **α5 is 26, not "~26"; α5+β6 is 36, not "~45"**.

Worked example of why this matters — the same rung, four families:

| family | `ct21` residue range | `a5helix` range | `a5plus` range |
|---|---|---|---|
| Gs (394) | **374–394** | 369–394 | 359–394 |
| Gi1 (354) | **334–354** | 329–354 | 319–354 |
| Gq (359) | **339–359** | 334–359 | 324–359 |
| G13 (377) | **357–377** | 352–377 | 342–377 |

`analysis/verify_partner_chains.py` hard-codes `ALPHA5_CT_LEN = 21` and applies
it as `position > n - 21` on the *deposited* chain, which is length-relative and
therefore correct; only its docstring generalises the Gi1 numbers. No code
change is needed there. The two outgoing ask documents do need one, and they are
owned by the orchestrator.

### 0.3 Every supplied chain is recorded per row, not per cell

See §9. Block B recorded `n_partner_aa`, `partner_tail11_helicity_frac`,
`plddt_ga_alpha5` and `n_interface_contacts_ga_receptor` — but
`partner_tail11_helicity_frac` lives only in
`data/block_b/06_interface/interface_continuous.csv`, which is **640 rows =
cell-level medians**, not the 32,000-row table. A ladder cannot be argued from
cell medians.

---

## 1. The ladder

Rungs renumbered from the catalogue's E1.1 to insert the 15-mer and to split the
α5-null into three explicit variants. Chain B is the supplied partner; chain A is
always the receptor.

| rung | chain B | len | what it removes relative to the rung above |
|---|---|---:|---|
| `R0_apo` | none | 0 | the partner |
| `R1_ct11` | last 11 of cognate Gα | 11 | 4 residues of α5-CT |
| `R2_ct15` | last 15 | 15 | 6 residues — **the `tran2026nanogs` length** |
| `R3_ct21` | last 21 | 21 | 5 residues — **the title's length** |
| `R4_a5helix` | CGN G.H5 | 26 | the rest of α5 |
| `R5_a5plus` | CGN G.S6 → C-term | 36 | β6 and the s6h5 turn |
| `R6a_da5` | full Gα, G.H5 deleted | L−26 | **all of α5, keeping the rest of the subunit** |
| `R6b_a5perm` | full Gα, G.H5 permuted in place | L | α5 *identity*, keeping α5 bulk |
| `R6c_a5polyA` | full Gα, G.H5 → poly-Ala | L | α5 identity and composition |
| `R7_full` | full cognate Gα | 350–394 | nothing |
| `R8_hetero` | Gα + Gβ1 + Gγ2 | +411 | — (adds, does not remove) |

`R2_ct15` is new and the coordinator's relay is why. `tran2026nanogs` stapled a
**15-mer** at I382–R389 with Y391Nal and E392hGlu. The literature therefore
already carries three distinct lengths — the opsin 11-mers, tran's 15, and our
title's 21 — and a ladder that omits 15 cannot be set against the one wet-lab
result that bears on it. Gs `ct15` = P63092 **380–394** = `RDIIQRMHLRQYELL`,
which is exactly tran's GαsCT15 window; the staple spans I382–R389, i.e.
positions 3–10 of that 15-mer, and Y391/E392 are positions 12/13.

`R6a/b/c` replace the catalogue's single `a5null`. The catalogue's phrasing
("the entire α5 replaced") does not say replaced *with what*, and the three
answers are different controls: `R6a` removes the contact and keeps the object;
`R6b` keeps bulk, helical propensity and composition and removes only identity;
`R6c` keeps length and removes composition too. **`R6b` is the true bulk
control** S1 asked for. Caveat that must be designed for: α5 packs against the
Ras domain, so `R6a`–`R6c` may not fold as Gα at all — which is why §9 requires
a Gα-chain pLDDT and a Ras-domain integrity readout on those arms. A bulk
control that arrives as a molten globule is not mass-matched to anything.

### 1.1 The rung sequences — the five families the current panel needs

Full 112-row table (16 families × 7 rungs) in `redo/inputs/seq_rungs.tsv`.

**Gs — GNAS, UniProt P63092, SV 1, last sequence update 1987-08-13, 394 aa**

| rung | range | sequence | sha256 (first 16) |
|---|---|---|---|
| ct11 | 384–394 | `QRMHLRQYELL` | `f159565cbda52c2b` |
| ct15 | 380–394 | `RDIIQRMHLRQYELL` | `fb163fbce24f88f9` |
| ct21 | 374–394 | `RVFNDCRDIIQRMHLRQYELL` | `39355d83d34556e4` |
| a5helix | 369–394 | `TENIRRVFNDCRDIIQRMHLRQYELL` | `95d5cf5e3eab4dc5` |
| a5plus | 359–394 | `CYPHFTCAVDTENIRRVFNDCRDIIQRMHLRQYELL` | `52ab88cba555bdfc` |
| full | 1–394 | (394 aa) | `6dedace6845efaa2` |

**Gi1 — GNAI1, P63096, SV 2, 2007-01-23, 354 aa**

| rung | range | sequence | sha256[:16] |
|---|---|---|---|
| ct11 | 344–354 | `IKNNLKDCGLF` | `07f3c67495a3d42d` |
| ct15 | 340–354 | `TDVIIKNNLKDCGLF` | `a79fe76aa984b5e3` |
| ct21 | 334–354 | `FVFDAVTDVIIKNNLKDCGLF` | `ff6db386f5b9f549` |
| a5helix | 329–354 | `TKNVQFVFDAVTDVIIKNNLKDCGLF` | `083c1a4dccd253e1` |
| a5plus | 319–354 | `IYTHFTCATDTKNVQFVFDAVTDVIIKNNLKDCGLF` | `e931f1049440108a` |
| full | 1–354 | (354 aa) | `57f8013fce15aa58` |

**Gq — GNAQ, P50148, SV 4, 2009-07-07, 359 aa**

| rung | range | sequence | sha256[:16] |
|---|---|---|---|
| ct11 | 349–359 | `LQLNLKEYNLV` | `352936d3e72c33c9` |
| ct15 | 345–359 | `KDTILQLNLKEYNLV` | `7861ee15ebd234c9` |
| ct21 | 339–359 | `FVFAAVKDTILQLNLKEYNLV` | `ca9c43b3512da42d` |
| a5helix | 334–359 | `TENIRFVFAAVKDTILQLNLKEYNLV` | `04cdb830714025ab` |
| a5plus | 324–359 | `IYSHFTCATDTENIRFVFAAVKDTILQLNLKEYNLV` | `324cb7f2f4220c7e` |
| full | 1–359 | (359 aa) | `aae9e1c2493fd384` |

**G13 — GNA13, Q14344, SV 2, 2003-10-31, 377 aa** *(the pipeline calls this
`alpha13` and files it under class label "G12" — see §3.4)*

| rung | range | sequence | sha256[:16] |
|---|---|---|---|
| ct11 | 367–377 | `LHDNLKQLMLQ` | `222a63d77c98083f` |
| ct15 | 363–377 | `KDTILHDNLKQLMLQ` | `272a31159467f707` |
| ct21 | 357–377 | `LVFRDVKDTILHDNLKQLMLQ` | `1d21ab51f3d357cf` |
| a5helix | 352–377 | `TENIRLVFRDVKDTILHDNLKQLMLQ` | `c7cdf018c29ec914` |
| a5plus | 342–377 | `LYHHFTTAINTENIRLVFRDVKDTILHDNLKQLMLQ` | `b481123adc4d3293` |
| full | 1–377 | (377 aa) | `b84f2fe8ce27cec1` |

**Gt1 — GNAT1, P11488, SV 5, 2007-01-23, 350 aa** *(human; see §3.3 for the
species question this raises)*

| rung | range | sequence | sha256[:16] |
|---|---|---|---|
| ct11 | 340–350 | `IKENLKDCGLF` | `e16ad41084f6a7b9` |
| ct15 | 336–350 | `TDIIIKENLKDCGLF` | `2a011e9407b8234d` |
| ct21 | 330–350 | `FVFDAVTDIIIKENLKDCGLF` | `309f3b882916ffb0` |
| a5helix | 325–350 | `TQNVKFVFDAVTDIIIKENLKDCGLF` | `c9d74b339d55e83e` |
| a5plus | 315–350 | `IYSHMTCATDTQNVKFVFDAVTDIIIKENLKDCGLF` | `723c7d83e340185b` |
| full | 1–350 | (350 aa) | `61cc7bb7a310e3f2` |

Independent cross-check: `analysis/verify_alpha5ct_family.py`'s docstring states
Gi1/Gi2 last-21 = `FVFDAVTDVIIKNNLKDCGLF` and Gq/G11 last-21 =
`FVFAAVKDTILQLNLKEYNLV`. Both reproduce exactly above, from a fetch made
independently of that script. The α5-CT (last-11) column of
`data/block_b/02_constructs/construct_build_report.md` also reproduces exactly
for all five.

### 1.2 α5-null full-subunit variants

`redo/inputs/seq_a5null.tsv`, 21 constructs. Extended 2026-09-11 to Gi3
(P08754) and Go (P09471) under the frozen cognate-Gα rule; generated and
verified by `redo/build/seq_a5null.py`. Gs shown:

| construct | len | supplied α5 (26) | sha256[:16] |
|---|---:|---|---|
| `R6a_da5` Gs | 368 | (deleted) | `7c75cc25b56cb2da` |
| `R6b_a5perm` Gs | 394 | `RRQQIYLHICMEETRRLNVDDLFNRI` | `770f480e689a720f` |
| `R6c_a5polyA` Gs | 394 | `AAAAAAAAAAAAAAAAAAAAAAAAAA` | `fac2a8d031178c96` |

The two families added under the frozen rule (SSR2 → Gi3; five receptors → Go):

| construct | len | supplied α5 (26) | sha256[:16] |
|---|---:|---|---|
| `R6a_da5` Gi3 | 328 | (deleted) | `d1518b6c4a99cca1` |
| `R6b_a5perm` Gi3 | 354 | `DILNANQDYVCKFVVGTFLEKVNIKT` | `16830343462a56a0` |
| `R6c_a5polyA` Gi3 | 354 | `AAAAAAAAAAAAAAAAAAAAAAAAAA` | `2a4b0d53d0378be5` |
| `R6a_da5` Go | 328 | (deleted) | `2b951794efb82c9b` |
| `R6b_a5perm` Go | 354 | `TDIINGIFNAIVYTVCRQNNDLVLAG` | `9d59dfcdc64a11da` |
| `R6c_a5polyA` Go | 354 | `AAAAAAAAAAAAAAAAAAAAAAAAAA` | `24d43f151c3f5cb4` |

**Seed key, because it is not guessable from the peptide-rung convention.**
`R6b_a5perm` draws on `(family, "a5null", "permute", "redo_v1", 1)` — no rung
term, because there is one construct per family; the control term split in two;
the trailing `1` an **int**, stringified by `map(str, parts)`; and every
rejected draw consumes RNG state, so the accepted permutation depends on all
draws before it. Any one of those four alone changes the bytes and none
announces itself. `seq_a5null.py` runs `--verify` by default and refuses to emit
a table it cannot reproduce.

---

## 2. What is already built — verified here by hash, not asserted

The catalogue's §0.4 says the bulk control and the α5 point mutants "already
exist as sequences". That is right, and it is now stronger than a claim about a
file we do not hold: **19 of the 29 `partners.fasta` entries were reconstructed
here from named database records and reproduce the audit's sha256 exactly.** We
therefore hold the bytes, not just the hashes.

| partners.fasta entry | len | reconstructed from | sha256[:16] | match |
|---|---:|---|---|---|
| `alphas` | 394 | UniProt P63092 canonical | `6dedace6845efaa2` | ✓ |
| `alphai1` | 354 | P63096 | `57f8013fce15aa58` | ✓ |
| `alphai2` | 355 | P04899 | `e0640cb9c3678ef3` | ✓ |
| `alphao` | 354 | P09471 | `399d5823731a6349` | ✓ |
| `alphaz` | 355 | P19086 | `c929d6e535ca2db1` | ✓ |
| `alphat` | 350 | **P11488 (human GNAT1)** | `61cc7bb7a310e3f2` | ✓ |
| `alphagust` | 354 | A8MTJ3 | `69d69c3bddc7e9c1` | ✓ |
| `alphaq` | 359 | P50148 | `aae9e1c2493fd384` | ✓ |
| `alpha11` | 359 | P29992 | `5a59fb4c4388d703` | ✓ |
| `alpha13` | 377 | **Q14344 (GNA13)** | `b84f2fe8ce27cec1` | ✓ |
| `alphas_F376A_L388A_mutant` | 394 | P63092 with F376A + L388A | `5c6ac55d09af0460` | ✓ |
| `alphas_F376A_L388A_R380A_triple_null` | 394 | + R380A | `cf709703d5ae80b1` | ✓ |
| `gcn4_leucine_zipper_33` | 33 | UniProt **P03069 residues 249–281** `RMKQLEDKVEELLSKNYHLENEVARLKKLVGER` | `9569a7eb08514dbd` | ✓ |
| `ubiquitin` | 76 | UniProt **P0CG48 residues 1–76** | `233b4b0b8c461609` | ✓ |
| `KaiB_2QKEE` | 91 | RCSB **2QKE entity 1, residues 5–95** | `e7e1c7e7d0960a55` | ✓ |
| `Gg2` | 71 | UniProt **P59768 (GBG2_HUMAN) full** | `32ec703375c0e761` | ✓ |
| `arrestin_FL` | 15 | UniProt **P49407 residues 22–36** | `a0a09ab53dbc98a2` | ✓ (**mislabel, §0.1**) |
| `endothelin1` | 21 | UniProt **P05305 residues 53–73** | `0b453f9bbe97de92` | ✓ |
| `substanceP` | 11 | UniProt **P20366 residues 58–68** | `7e10bca1b6e43cbe` | ✓ |

**Ten not reconstructed.** Six are irrelevant to the ladder (`HCAR2`, `TAAR1`,
`GASR`, `GP161`, `GIPR`, `ACM3` — all receptors). Four matter and their bytes
exist only on HPC:

| entry | len | status |
|---|---:|---|
| `random_helix_40mer` | 40 | **bytes not held.** Designed; not derivable. Must be requested verbatim before it can be used or reasoned about. |
| `arrestin_Ctail` | 41 | **bytes not held.** No 41-mer window of P49407, P32121, P08168, P10523, P30518, P08100 or P02699 hashes to `7f7135b3c50ca201`. Source unresolved. |
| `DAMGO` | 5 | **bytes not held.** Synthetic opioid peptidomimetic; not a UniProt subsequence. |
| `Nb60` (=Nb80 CDR3) | 126 | **bytes not held.** Not byte-identical to RCSB 3P0G entity 2 (126 aa, sha `3e4dbf73ccc8ab7a`) or 4LDE entity 2 (120 aa). A variant of Nb80 from an unrecorded source. |

**Consequence for the catalogue's E1.2.** "The bulk control is a dispatch, not a
construction job" holds for `ubiquitin`, `KaiB_2QKEE`, `gcn4_leucine_zipper_33`
and both Gs mutants — all five now in hand. It does **not** hold for
`random_helix_40mer`, which is the one the coordinator's relay wants as the
helicity-matched control. See §5.2 for the replacement that does not need it.

### 2.1 Both α5 point mutants sit inside the 21-mer — a free, sharp arm

P63092 position 376 is F, 380 is R, 388 is L, all verified against the fetched
sequence. All three are inside `ct21` (374–394) and inside `a5helix`; F376 and
R380 are outside `ct11` (384–394) but L388 is inside it.

So `alphas_F376A_L388A_mutant` is not only a full-subunit arm. The same two
substitutions can be made **at every peptide rung**:

| rung | Gs WT | F376A+L388A | F376A+L388A+R380A |
|---|---|---|---|
| ct21 | `RVFNDCRDIIQRMHLRQYELL` | `RVANDCRDIIQRMHARQYELL` | `RVANDCADIIQRMHARQYELL` |
| a5helix | `TENIRRVFNDCRDIIQRMHLRQYELL` | `TENIRRVANDCRDIIQRMHARQYELL` | `TENIRRVANDCADIIQRMHARQYELL` |

This is the catalogue's E1.8 crossed with E1.1 at no construction cost, and it
is the biologically motivated negative control that the combinatorial scramble
is not. It is restricted to the Gs-coupled receptors — currently **5 of 40**,
which is a PANEL.md dependency, not a construct one.

---

## 3. Which Gα per receptor, and on what authority

This is the PI's explicit worry. It has four distinct parts and they have
different answers.

### 3.1 The authority disagrees with itself, and the corpus says by how much

The project's current assignment comes from `refs/gpcr_coupling.csv`
(`primary_ga_identity` / `primary_ga_class` / `secondary_ga_classes`), a file
held on HPC and never shipped in any drop. **No block contains the coupling
table its own arms were routed by.** The 40-row assignment is recoverable from
`data/block_b/02_constructs/construct_build_report.md`, but its provenance is
not.

The natural authority is GproteinDb. What the corpus says about how much weight
it will bear (`lit/notes/pandyszekeres2024gproteindb.md`):

- Couplings are integrated from six datasets — GtoPdb, Inoue TGFα shedding,
  Inoue NanoBiT-G, Bouvier GEMTA/EMTA, Martemyanov FreeGβγ-Nluc, Lambert
  RGB-GDP (p.2, p.4).
- Agreement on the **primary transducer** between GEMTA and FreeGβγ-Nluc is
  **68% at family level and 22% at subtype level** (p.8, 66 shared GPCRs, 79
  combinations).
- The Inoue cutoff log(Emax/EC50) ≥ 7.0 was *chosen to maximise* agreement with
  the other two datasets, so the 94%/82% agreement figures are fitted, not
  measured (note, route 4b).

**So subtype-level "cognate Gα" is not a fact that can be asserted from any
single source.** The design must stop treating it as one.

Recommended procedure, and it is cheap:

1. Assign at **family** level (Gs / Gi-o / Gq-11 / G12-13), which is where
   inter-dataset agreement is 68% rather than 22%.
2. Record per receptor: `ga_family`, `ga_subtype`, `ga_source_datasets`,
   `n_datasets_agreeing`, `datasets_disagreeing`, `assignment_confidence`.
3. Where two datasets disagree at family level, **run both as separate arms**
   rather than pick one. On a 40-receptor panel this is a handful of extra
   cells, and it converts a hidden assumption into a measured one.
4. The coupling table itself ships with the drop, with a fetch date. Not on HPC.

### 3.2 At peptide length, most of the subtype worry evaporates

Computed here from the 16 fetched Gα records. At **every** peptide rung
(11, 15, 21 and 26):

| identical over the whole rung | consequence |
|---|---|
| **Gi1 ≡ Gi2** | the Gi1/Gi2 assignment is unobservable at peptide length |
| **Gt1 ≡ Gt2 ≡ Ggust** | ditto |
| **Gq ≡ G11** | ditto |
| **Gs vs Golf: 1 substitution** (ct11 `QRMHLRQYELL` vs `QRMHLKQYELL`) | near-unobservable |

Hamming distances from Gi1 at `ct21`: Gi2 0, Gi3 2, Gt1/Gt2/Ggust 2, Gz 4, Go 6,
Gq 10, G13 12, Gs 15.

**This is a real result for the ladder's design.** Below `R6`, the only coupling
decision that can possibly change the supplied bytes is the **family**. So the
PI's worry, for the centrepiece experiment, reduces from "is the subtype right"
(unanswerable, 22% agreement) to "is the family right" (68% agreement, and
resolvable by running both where they disagree). Say this in Methods.

It also **corrects catalogue E1.6.** "Gi and Gt differ at exactly one position"
is true at `ct11` only. At `ct21` they differ at 2 positions, at `a5helix` at 4.
The single-residue natural minimal pair exists at the 11-mer rung and nowhere
else.

### 3.3 Species — human Gα was paired with non-human receptors, and it should not have been

From `lit/panels/receptors.csv`, three of the 40 Class A panel receptors are not
human:

| panel slug | GPCRdb entry | species | Gα supplied (Block B) | native partner |
|---|---|---|---|---|
| `OPSD` | `opsd_bovin` | *Bos taurus* | human GNAT1 **P11488** | bovine GNAT1 **P04695** |
| `ADRB1` | `adrb1_melga` | *Meleagris gallopavo* (turkey) | human GNAS P63092 | turkey Gαs |
| `B1B1U5` | `b1b1u5_9arac` | *Hasarius adansoni* (jumping spider) | human GNAI1 P63096 | see below |

Three consequences, in descending severity.

**(a) B1B1U5 is "Kumopsin1", a jumping-spider opsin** (UniProt B1B1U5, 372 aa,
fetched 2026-09-11). Block B assigns it cognate class **Gi** with secondary Gq.
Invertebrate visual opsins are the canonical Gq-coupled opsins. Supplying human
GNAI1 to a spider opsin and calling it "cognate" is the single least defensible
construct on the panel. **Unresolved — this needs an authority or the receptor
needs to leave the panel.** It is a PANEL.md decision; flagged here because the
construct cannot be specified without it.

**(b) OPSD/bovine.** Checked here: human P11488 and bovine P04695 are both 350
aa and differ at exactly **3 positions over the whole subunit**, none of them in
the C-terminal 36. Their last 11, 15, 21, 26 **and 36** are byte-identical
(`IKENLKDCGLF`, `FVFDAVTDIIIKENLKDCGLF`, …). **So every ladder rung from `ct11`
through `a5plus` is species-invariant for OPSD**, and only `R6`/`R7`/`R8` are
affected at all — and there by 3 residues. For those, supply bovine P04695 and
record the swap. Note the latent inconsistency this exposes:
`analysis/verify_alpha5ct_family.py` maps `"Gt1": "P04695"` (bovine) while the
pipeline built `alphat` from P11488 (human). Both are defensible; they are
different records and must not be quoted interchangeably.

**(c) ADRB1/turkey.** Turkey β1AR with human Gαs is a cross-species complex that
does not exist. It is also the classic crystallography construct, so the
references are turkey too. Options: swap the receptor to human ADRB1 (a PANEL.md
call), or supply turkey Gαs and record it. **Decision required; do not leave the
mismatch silent.**

**The general rule for the redo: receptor species and Gα species are recorded as
separate columns on every row, and any row where they differ carries
`cross_species_partner=true`.** No block has ever carried this column, and the
three mismatches above were invisible as a result.

### 3.4 Two label-vs-identity traps already in the pipeline

- **`alpha13` is filed under class label "G12".** Verified: its bytes are GNA13
  (Q14344, 377 aa), not GNA12 (Q03113, 381 aa). The header is honest; the class
  column is not. `donor_ga_class.csv` and the construct report both say "G12"
  for a G13 sequence. Human GNA12 `ct11` is `LQENLKDIMLQ` and GNA13's is
  `LHDNLKQLMLQ` — they are different peptides and the redo must say which it
  supplied.
- **Block D's four "cognate_ga" arms all supplied `alphas`.**
  `data/block_d/06_gate_reports/GATE_1_D2_NB_SHA.md` lines 35–44 and
  `data/block_b/02_constructs/d2_arm_sequence_audit.csv` both record
  `partner_identity = alphas` for ADRB2, **ACM2, AGTR1 and OPRK**. Block B
  assigns ACM2→Gi, OPRK→Gi, AGTR1→Gq. So either the manifest column is
  mislabelled on three of four receptors, or three of four D2 "cognate" arms
  were not cognate. **It cannot be told apart from the drop**, because the D2
  audit's `consumed_sequence_sha256` column reads `unknown (partner_type=apo or
  g_alpha)` on exactly those rows — the Gα chains were never hashed, only the
  nanobody chains were. This is the strongest possible argument for §0.1: a
  hash on the Gα chain would have settled it in one line. Block D's F1 positive
  control ("cognate Gα drives active on 14 of 16 cells") rests on it.

---

## 4. The two construct errors already found, stated so they cannot recur

**(1) The 334–354 error** — §0.2. Fixed by the "last N residues" rule and the
per-family ranges in §1.1.

**(2) The D2 ADRB2 nanobody collision — and a correction to how it has been
described.** The brief I was given says the active-Nb and inactive-Nb arms "fed
the SAME 125-aa sequence". The two HPC input YAMLs are indeed byte-identical
(`PHASE_1_CONSTRUCT_IDENTITY.md`, both sha
`1406ad7ea26451149ea73339e2282ef0f77f52d693c680cbf790db7af767db62`). But
`GATE_1_D2_NB_SHA.md` — a later audit, on the dispatch manifest and the landed
corpus — finds **ADRB2 active_nb contributed 0 rows**: "0 rows in the analysed
corpus and 0 rows in `tier_d2_manifest.dispatch.csv` (no such row ever entered
the dispatch pool)", and `d2_arm_sequence_audit.csv` records
`arm_survived_to_analysis=False`, `rows_contributing_to_D2_manuscript_sentence=0`.

So the accurate statement is: **the placeholder was written into the input files
and the arm was removed before dispatch.** No contrast compared an arm with
itself, because the arm does not exist. The near-miss is the lesson, not a
corrupted result — and the near-miss is entirely a consequence of keying
constructs by header. Both statements should travel together; the shorter one is
wrong in the direction that overstates our own data's defects.

The four real nanobody sequences are held, in
`data/block_d/09_references/nanobody_sequences.fasta`, with hashes confirmed in
`GATE_1_D2_NB_SHA.md`: Nb60/5JQH (125, `1406ad7e…`), Nb6/6VI4 (133,
`a7b413fe…`), Nb9-8/4MQS (125, `4888b397…`), Nb.AT110i1_le/6OS2 (128,
`d8c31820…`). Note Nb60/5JQH and Nb6/6VI4 carry C-terminal **`HHHHHH`** tags and
Nb6 additionally `EPEA` and a leading `M`; Nb9-8 carries a leading `GPGS`. If
nanobody arms are rerun, decide once whether tags stay, and record it — a His
tag is 6 residues of unstructured chain at the end of a 125-mer, and it is
exactly the kind of thing that shows up in a contact count.

---

## 5. Controls at peptide length — construction rules, what each preserves, what it confounds

Full table: `redo/inputs/seq_controls.tsv`, 240 constructs = 5 families × 4
rungs × 12 controls. Seed rule, stated so anyone can regenerate:

```
seed = int(sha256(f"{family}|{rung}|{control}|redo_v1|{k}").hexdigest()[:16], 16)
```

This is Block B's convention
(`SHA-256(receptor_slug + '|block_b_decoy_v1|' + variant)`) with the
per-receptor term replaced by a per-family term — **because at peptide length
the construct no longer depends on the receptor.** Block B needed 40 decoy
FASTAs; the redo needs 5 per rung. That is a real simplification and it changes
what the control means: one scramble per family is a fixed sequence, not a
sample of permutations.

### 5.1 The control set

| control | preserves | destroys | confounds it introduces |
|---|---|---|---|
| `wt` | — | — | — |
| `reversed` | length, composition, net charge, aa content, and near-identical helical propensity | N→C order and register | none beyond order; the cleanest single control |
| `scramble_k` (k=1..5) | length, composition, net charge | order, register, **and the hydrophobic face** | confounds identity with amphipathicity — a scramble is usually a worse helix |
| `face_scramble_k` (k=1..3) | length, composition, charge, **and the hydrophobic/polar pattern along the chain**, hence the amphipathic face and the helical hydrophobic moment | residue identity only | the intended control: identity without geometry |
| `polyA` | length only | everything | **raises** helical propensity; an upper bound on "any helix will do" |
| `gcn4_window` | length; strong helical propensity; no evolutionary relation to Gα | composition, charge, identity | the helicity-matched bulk control |

`face_scramble` partitions positions into `AVLIMFWYC` and the rest and permutes
within each class, so an ideal-helix wheel keeps the same face. The partition is
written into `seq_controls.py` so it is auditable rather than asserted.

**Five scrambles, not one.** Block B drew one permutation per receptor, so
"scrambled" is 40 draws of one thing. At peptide length there is no receptor term
left, so a single draw would make the whole control rest on one permutation.
Drawing k=5 per (family × rung) and treating the draw as a random effect answers
"is it this permutation, or permutations in general" — which is the question a
referee asks. Cost: it multiplies the scramble arm by 5, or the arm is run at
n/5 per draw for the same total. RUN_MATRIX.md owns that trade.

Worked example, Gs `ct21` (WT `RVFNDCRDIIQRMHLRQYELL`):

| control | sequence | Hamming | sha256[:16] |
|---|---|---:|---|
| reversed | `LLEYQRLHMRQIIDRCDNFVR` | 20 | `8b88b049315c38b4` |
| polyA | `AAAAAAAAAAAAAAAAAAAAA` | 21 | `f48de1653fdfa9b6` |
| scramble 1 | `LMIEIRLFVDQYRRRLHNCQD` | 20 | `71fa66b0c9b2c163` |
| scramble 2 | `ILDLERQVQFLRDHNRMIYRC` | 18 | `661209f8b3230ae8` |
| face_scramble 1 | `QFLERIRRILNDLRVQHYDMC` | 18 | `92e4bcf6b6edf07a` |
| face_scramble 2 | `NYIHQMDDICRRLRFEQLRLV` | 16 | `f4006fbbae191dcb` |
| gcn4_window | `RMKQLEDKVEELLSKNYHLEN` | 20 | `e6403a1af54b3e1a` |

### 5.2 Can `random_helix_40mer` or `gcn4_leucine_zipper_33` serve directly?

The coordinator asked this directly. The answer is **no for the first, partly for
the second, and there is a better option.**

- `random_helix_40mer` is **40 residues** and we do **not hold its bytes**
  (§2). It length-matches no rung. It could serve only as a fixed-length
  designed-helix arm alongside the ladder, and only after the bytes are
  requested. Do not build a design around it.
- `gcn4_leucine_zipper_33` is **33 residues** — it length-matches no rung either
  (11/15/21/26/36). Used as-is it confounds length with sequence, which is the
  one confound the ladder exists to remove.
- **What does work:** the GCN4 zipper is `P03069` residues **249–281**, and that
  is now established by hash, so any sub-window of it is equally grounded.
  `gcn4_window` above is P03069 249..(249+N−1) for each rung length N. It is
  length-matched, strongly helical, evolutionarily unrelated to Gα, and free.
  It is the helicity-matched bulk control `tran2026nanogs` lacks, at every rung.

| rung | `gcn4_window` sequence | sha256[:16] |
|---|---|---|
| 11 | `RMKQLEDKVEE` | `41ed6b4dfbf6977e` |
| 15 | `RMKQLEDKVEELLSK` | `2fd275ca6aa5dbe0` |
| 21 | `RMKQLEDKVEELLSKNYHLEN` | `e6403a1af54b3e1a` |
| 26 | `RMKQLEDKVEELLSKNYHLENEVARL` | `3e6c15f660b87625` |

One caveat to record: the zipper is a **coiled-coil** helix, so it is helical
*as a dimer*. Supplied as a single chain to a co-folding model it may or may not
be delivered helical — which is precisely why §9's per-row helicity readout is
what makes the control interpretable rather than decorative.

### 5.3 The `R6b` full-subunit scramble is the length-matched partner of these

Same rule, 26 positions instead of 11 — so the redo's decoy is a **26-residue**
edit on a full subunit, against Block B's 9–11. That widens the edit from 3% of
the partner to 7%, and it removes the whole α5 rather than its tip.

---

## 6. The finding that governs the whole ladder: rung length and partner-MSA depth are confounded

**This is the most consequential thing in this document and it contradicts both
the catalogue and the coordinator's relay. It should be read before anything is
dispatched.**

Catalogue E1.3's caveat says: *"At 21 residues the partner chain's MSA is
essentially empty, so scramble and wild type differ in sequence but not in
alignment depth — which removes the Block B confound rather than repeating it."*
The coordinator's relay says something similar. **Both are wrong, and this
project's own cache proves it.**

`data/block_b/03_msa_audit/msa_depth_report.md` (lines ~350–376) tabulates
measured MSA depth for every `partners.fasta` entry, from the pipeline's own
Chai `.aligned.pqt` cache:

| entry | len | total MSA depth | uniref90 | bfd/uniclust |
|---|---:|---:|---:|---:|
| `DAMGO` | 5 | **1** | 0 | 0 |
| `substanceP` | 11 | **1** | 0 | 0 |
| `random_helix_40mer` | 40 | **1** | 0 | 0 |
| `arrestin_Ctail` | 41 | **1** | 0 | 0 |
| `arrestin_FL` | 15 | **84** | 79 | 4 |
| `gcn4_leucine_zipper_33` | 33 | **224** | 153 | 70 |
| `endothelin1` | 21 | **732** | 565 | 166 |
| `alphas` | 394 | 12,080 | 7,355 | 4,724 |
| `alphai1` | 354 | 14,986 | 9,327 | 5,658 |

A **21-residue** query from a real, conserved human protein pulled **732
homologs**. A 15-mer pulled 84. A designed 40-mer pulled 1. Depth at peptide
length is not a function of length — it is a function of **conservation**. And
the Gα α5-CT is among the most conserved 21 residues in the proteome: it is
byte-identical across Gi1/Gi2, across Gt1/Gt2/Ggust, and across Gq/G11 (§3.2),
and near-identical across the whole Gi/o branch.

So the expected outcome, if the rungs are run with MSAs on:

| arm | expected partner MSA depth |
|---|---|
| `ct21` wild type | hundreds to thousands (it will retrieve the entire Gα family) |
| `ct21` scramble / face_scramble / gcn4_window / polyA | ≈ 1 |

**The sequence-identity contrast at peptide length would be a pure MSA-depth
contrast.** That is not a weaker version of the Block B confound — it is a
stronger one. Block B's cognate (12,080) and decoy arms at least both had deep
alignments; here one arm has an alignment and the other has a single row.

### 6.1 What follows, concretely

1. **Every peptide rung runs MSA-free on the partner chain as the primary
   condition.** Partner chain supplied as a single sequence; receptor chain keeps
   its normal MSA. This is the only configuration in which `wt` vs `scramble` at
   21 residues measures sequence recognition rather than alignment depth.
2. **`R7_full` must also be run MSA-free**, or rung length and partner-alignment
   depth stay perfectly confounded along the whole ladder (short rungs have no
   MSA, long rungs do). One MSA-free full-Gα arm is what separates "the model
   needs the bulk" from "the model needs the alignment". This promotes catalogue
   **E1.9 from an optional side-experiment to a load-bearing component of E1.1.**
3. **The MSA-on condition is still worth running at `R7` and `R5`**, because the
   on/off contrast at fixed length is itself the E1.9 result.
4. **Measure the depths before dispatching anything.** The exact query sequences
   are in `redo/inputs/seq_rungs.tsv` and `seq_controls.tsv`. Submitting the
   ~60 distinct peptide-rung sequences to the same ColabFold pipeline and
   recording `n_seqs` is hours of wall-clock and no inference — `cheap` at worst,
   and it turns the paragraph above from a prediction into a measurement. **Do
   this first.**
5. **`partner_msa_depth` becomes a required per-row column** (§9), not an audit
   artefact. Block B had to reconstruct it from an HPC cache after the fact.

### 6.2 What the Block B MSA audit actually found, since it is usually mis-cited

The coordinator's relay says the Block B decoy is confounded because "scrambling
the tail also disrupts inter-chain MSA pairing at the same columns". That is not
what `PHASE_1D_EXTENSION.md` concludes. Its verdict:

- **Boltz, Protenix, OpenFold3: the scrambled residues ARE present as aligned
  uppercase columns in the query row** — 3 of 4 backbones read the decoy edit.
  Boltz and Protenix verified by direct column inspection; OF3 by construction
  (raw MSA purged, hash keys decoy-specific).
- **Chai is the outlier**: its `.aligned.pqt` cache anchors the decoy query row
  to WT-parent residues, gaps or lowercase insertions at the α5-CT positions
  (0/40 carry the scrambled tail as aligned uppercase).
- **Chai's `pairing_key` is empty on 100% of rows in every arm, cognate
  included** — pairing was never wired in for Block B on Chai, so pairing cannot
  explain any decoy-vs-cognate difference there.
- Boltz and Protenix do use pairing, and decoy MSA files are distinct from
  cognate ones on all 18 cells inspected.

So the Block B confound is **content and depth, not pairing**, and it is
**per-backbone, not panel-wide**. Any redo sentence about it needs that shape.

---

## 7. Gβγ

`R8_hetero` only. Gα alone everywhere else, matching Blocks A–D.

| chain | UniProt | SV | len | sha256[:16] |
|---|---|---|---:|---|
| Gβ1 | **P62873** (GBB1_HUMAN) | 3 | 340 | `731c013dfd2af08e` |
| Gγ2 | **P59768** (GBG2_HUMAN) | 2 | 71 | `32ec703375c0e761` |

Gγ2 is already in `partners.fasta` as `Gg2` and its hash matches the canonical
human record exactly (§2), so only Gβ1 is new. Neither has ever been consumed by
any row.

Three things `R8` requires beyond the sequences, all noted here because they are
construct-adjacent:

- **A three-chain input schema.** The construct report is explicit that "β and γ
  subunits are outside the scope of the single-partner-chain pipeline this
  feeds" and that Block A's FASTA schema is single-partner. This is a harness
  change.
- **Lipidation is not modelled.** Gγ2 is prenylated at its C-terminal CAAX and
  Gα is myristoylated/palmitoylated; none of the four backbones place those. The
  heterotrimer is therefore a sequence-only heterotrimer and must be described
  as one.
- **Chain-order sensitivity.** With three chains, record the order supplied and
  run at least one order-swapped cell; nothing in any block establishes that the
  backbones are order-invariant.

---

## 8. Receptor and ligand chains — rules, and the dependencies

These are supplied sequences too, so the rules belong here even though the
selections belong to PANEL.md and RUN_MATRIX.md.

**Receptor chain.**

- UniProt canonical, full length, wild type. No BRIL/T4L fusion, no
  thermostabilising mutations, no truncation.
- Species recorded per receptor (§3.3). Three of the current 40 are non-human.
- **Hash-check against the panel's declared sequence.** Block A's audit #12 hit
  exactly this: `panel_receptor_sequences.fasta` carries an **ADRB1 G389R
  polymorphism variant** at 477 aa alongside the Class-A ADRB1 entry, plus
  second-sequence variants of FSHR (695 aa) and MCHR1 (422 aa)
  (`msa_depth_report.md` lines 33–38, 148–156). Three receptors on a 40-receptor
  panel have two sequences each in the pipeline's own file. Which one a row
  consumed is a hash question.

**Ligand chain, when the ligand is a peptide.** From
`data/block_c/09_references/reference_survey.csv`, 42 of 168 reference rows are
`NO_HETATM_CANDIDATES` — i.e. no small-molecule ligand — and **9 of them are on
the current 40-receptor Class A panel**: APJ (active), CCR5 (active), CXCR2
(active), CXCR4 (active), EDNRB (active), MCHR1 (active), OPRX (active), FSHR
(inactive), LSHR (inactive).

For those receptors an agonist arm supplies a **second peptide chain**, and the
ladder's own partner is a peptide. Three requirements follow:

1. Chain roles are explicit and hashed: `chain_role ∈ {receptor, partner,
   peptide_ligand}` with a sha256 each. A model given two unlabelled ~21-mers
   can place either in the intracellular crevice.
2. **`partners.fasta:endothelin1` is 21 residues** — the same length as `ct21`.
   If EDNRA/EDNRB ever get an agonist arm crossed with `R3`, two 21-mers enter
   the same prediction. Hash-keyed roles, not headers.
3. Peptide-agonist sequences are specified the same way as everything else
   (UniProt accession + residue range + sha256); `endothelin1` = P05305 53–73
   and `substanceP` = P20366 58–68 are already done (§2).

FSHR and LSHR are a harder case still: their agonists are heterodimeric
glycoprotein hormones (two chains, N-glycosylated). Flag as unresolved; they may
be better served by keeping those two receptors partner-only.

---

## 9. What must be recorded per row for the ladder to mean anything

`tran2026nanogs` is unopposed in the corpus (the lit session confirms only three
notes mention helicity at all, and only tran tests it): the **unstapled linear
GαsCT15 is a random coil by CD and does nothing**, and the stapled 15-mer works
only with agonist present. A co-folding model has no solution-phase equilibrium
and will fold whatever it is handed. **Without a helicity readout on the
supplied chain, a positive ladder result cannot be distinguished from the model
having folded the peptide for us.** This measurement can only be added before
the runs.

Required per row — not per cell. Block B put `partner_tail11_helicity_frac` in a
640-row cell-level file; that is not usable for a ladder.

| column | why | status |
|---|---|---|
| `partner_seq_sha256` | the whole of §0.1 | **new** — Block B hashed the FASTA, Block D hashed only nanobody chains |
| `n_partner_aa` | every rung verifiable from data, not from the dispatch note | exists (cell level) |
| `partner_chain_helicity_frac` | DSSP H/G/I over the **whole** supplied chain | **new**; generalises `partner_tail11_helicity_frac`, which is meaningless at the 11-mer rung where the tail is the chain |
| `partner_tail11_helicity_frac` | continuity with Block B | exists (cell level) → promote to row |
| `plddt_partner_chain_mean` | the closest in-silico analogue of tran's CD measurement | **new** (Block B has `plddt_ga_alpha5` only) |
| `plddt_ga_alpha5` | per-rung comparability | exists |
| `n_interface_contacts_ga_receptor` | engagement, not just presence | exists |
| `contact_register_last5_json` | **which** receptor positions the last 5 partner residues touch — the register question `tran2026nanogs` leaves open (3SN6 puts Y391 on R131^3.50, 6E67 puts E392 there) | exists (cell level) → promote to row |
| `d_ga_alpha5_r350_ca` | engagement depth into the crevice | exists |
| `partner_msa_depth`, `partner_msa_depth_uniref90`, `partner_msa_mode` | §6 — the ladder is uninterpretable without it | **new** |
| `partner_chain_order`, `n_chains` | R8 | **new** |
| `receptor_species`, `partner_species`, `cross_species_partner` | §3.3 | **new** |

Two derived readouts that turn the above into the actual argument:

- **Reach vs recognition.** A rung that raises active fraction *and* whose
  partner chain is helical *and* engages the crevice is recognition. A rung that
  raises active fraction with a low-helicity, low-pLDDT partner chain that barely
  contacts TM3/TM6 is reach — the receptor opened and the chain went along. Both
  are reportable; only the first supports the title.
- **Gα fold integrity on `R6a/b/c`.** Record `plddt_partner_chain_mean` and a
  Ras-domain Cα RMSD to the cognate Gα prediction. A bulk control that misfolds
  is not mass-matched.

### 9.1 Should any rung be supplied conformationally restrained?

Recommendation: **no restraint in the primary ladder; one restrained arm as a
targeted follow-up, and only if the primary ladder shows the reach signature.**

Reasons: (i) none of the four backbones has a documented, uniform restraint or
staple mechanism, so a restrained arm would not be comparable across backbones
and the paper's four-backbone claim would not survive it; (ii) a covalent staple
is a non-standard residue pair, which changes the input schema and the MSA path;
(iii) the free-peptide helicity readout in §9 already answers the question the
restraint was meant to answer — if the model delivers the peptide helical
unprompted, restraining it adds nothing, and if it does not, that is the result.

The cheapest partial substitute, if one is wanted: an **(i, i+4) double-Ala→Aib
analogue is not available**, but a **helix-favouring register control already
is** — `polyA` at matched length is an upper bound on helical propensity with no
sequence, and `gcn4_window` is a high-propensity helix with a different
sequence. Those two bracket the question without touching the schema.

---

## 10. Unresolved — flagged, not guessed

1. **B1B1U5 (Kumopsin1, jumping spider) has no defensible cognate Gα.** Assigned
   Gi in Block B. Needs an authority or removal. §3.3(a). PANEL.md dependency.
2. **ADRB1 is turkey.** Supply turkey Gαs, or swap to human ADRB1. §3.3(c).
3. **OPSD is bovine.** All rungs `ct11`–`a5plus` are species-invariant
   (verified: human and bovine Gt1 differ at 3 positions, none in the last 36);
   `R6`–`R8` differ by those 3. §3.3(b). Low severity, but record it.
4. **`refs/gpcr_coupling.csv` has never shipped.** The 40-receptor assignment is
   recoverable from the construct report; its provenance is not. Must ship.
5. **Block D's three non-Gs "cognate_ga" arms.** §3.4. Cannot be resolved from
   the drop; needs the HPC input files or a Gα chain hash.
6. **Four `partners.fasta` byte sets not held**: `random_helix_40mer`,
   `arrestin_Ctail`, `DAMGO`, `Nb60`(=Nb80). §2.
7. **`arrestin_FL` is a β-strand fragment, not a finger loop.** If an
   arrestin comparison arm is wanted, the construct must be respecified from a
   named source. §0.1.
8. **FSHR/LSHR peptide agonists are heterodimeric glycoprotein hormones.** §8.
9. **Whether `ct15` should also be run with the two chemical modifications
   `tran2026nanogs` found necessary (Y391Nal, E392hGlu).** Non-canonical residues
   are outside every backbone's vocabulary, so the answer is probably no, but it
   should be stated rather than omitted — it is the gap between our 15-mer and
   the only 15-mer with a wet-lab result.

---

## Questions for lit

Each says what I would do differently depending on the answer. Numbered for
relay.

1. **Does any paper in the corpus supply a partner chain with MSAs disabled
   while leaving the receptor's MSA on — and does anyone report partner-chain
   MSA depth at all?** §6 makes the MSA-free partner the primary condition for
   every peptide rung. *If there is precedent*, I cite it and treat MSA-free as
   the default without further defence. *If there is none*, the redo must run the
   MSA-on/MSA-off contrast at `R7` as a first-class arm and report it as a
   methodological result, which changes RUN_MATRIX by one full arm.

2. **Does any paper report an MSA-depth figure for a short (<40 aa) supplied
   chain?** Our own cache gives endothelin-1 (21 aa) a depth of 732 and a
   designed 40-mer a depth of 1. *If the corpus has a comparable figure*, the
   §6 argument gets an external anchor and can go in Methods. *If not*, I must
   present it as our own measurement and the pre-flight depth measurement in
   §6.1(4) becomes mandatory rather than advisable.

3. **`tran2026nanogs` numbers its α5 residues in the Gαs frame (I382, R389,
   Y391, E392). Does the paper state the parent sequence or accession?** I have
   matched its GαsCT15 to UniProt P63092 residues 380–394 on length and on the
   stated residue identities, but not against a quoted sequence. *If the paper
   names the accession*, I pin `ct15` to it and the correspondence is exact. *If
   it does not*, §1 must carry a line saying the register correspondence is
   inferred from residue numbering alone.

4. **Is there any structural or wet-lab result on a Gα α5 peptide shorter than
   11 residues, or between 15 and 21?** The rungs are currently 11/15/21/26/36 —
   11 from the opsin peptides, 15 from tran, 21 from our title, 26 and 36 from
   CGN. *If the corpus has an 8-mer or an 18-mer result*, I add that rung. *If
   not*, I state the ladder's spacing is set by the literature's lengths plus the
   two structural boundaries, which is a defensible rule.

5. **Does any paper run a helicity-matched but sequence-scrambled peptide against
   a receptor — in silico or in vitro?** The lit session says tran's negative
   controls are all structural and no scrambled-sequence peptide was run. *If
   that absence holds corpus-wide*, `face_scramble` (§5.1) is the novelty and I
   will say so in the design note. *If someone has done it*, I need the
   construction rule they used so ours is comparable rather than merely
   different.

6. **What does the corpus say about supplying a coiled-coil peptide as a
   monomer?** `gcn4_window` is the helicity-matched control (§5.2) and GCN4's
   helix is a dimer helix. *If any paper reports that co-folding models deliver
   isolated zipper monomers as helices*, the control is sound as specified. *If
   the evidence is that they do not*, I replace it with a monomeric designed
   helix — which means requesting `random_helix_40mer`'s bytes and building
   windowed variants, a different and slower path.

7. **Is there precedent for reporting a per-row partner-chain pLDDT as a proxy
   for peptide order/disorder?** §9 rests on it. *If yes*, the "reach vs
   recognition" readout is a citable method. *If no*, it must be introduced and
   validated internally — e.g. by showing `polyA` and `gcn4_window` bracket the
   pLDDT range — which adds an analysis step but no predictions.

8. **Does the corpus contain a coupling-assignment authority we should prefer
   over GproteinDb's integrated table, or any paper reporting how often
   coupling-based partner selection changes a structural result?** §3.1 proposes
   family-level assignment with both arms run where datasets disagree. *If a
   better single authority exists*, I simplify to it. *If a paper shows the
   choice does not matter structurally*, the dual-arm hedge can be dropped and
   RUN_MATRIX gets cheaper.

9. **Cross-species complexes: does any co-folding paper pair a non-human
   receptor with a human partner, and does anyone measure the cost?** Three of
   our 40 are non-human (§3.3). *If there is precedent with a measured effect*,
   I follow it. *If the corpus is silent*, the safe reading is to match species
   where a record exists (bovine Gt1 for OPSD) and to flag ADRB1/B1B1U5 to the
   PI as panel decisions.
