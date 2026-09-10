# BLOCK B — PHASE 1: CONSTRUCT IDENTITY

**Date:** 2026-09-09
**Corpus under audit:** `experiments/019_block_b_partner_selection/analysis/rows.csv` (32,000 rows) — the same corpus Phase 0 provenance was signed off on.
**Purpose:** Establish, by sequence hash rather than by label, what the four arms `{apo, decoy, shuffled, cognate}` actually are on all 40 Class A receptors × 4 backbones. Read-only. No commits, no scoring, no manifest changes. Companion table `experiments/019_block_b_partner_selection/analysis/donor_ga_class.csv` emitted alongside for Phase 5 downstream.

Prior Phase 0 reports: `BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md`, `BLOCK_B_DOSSIER_PHASE_0_ADDENDUM.md`. Phase 0's GATE 0 was CONDITIONAL — no invalidating finding — with five items adjudicated; that adjudication holds into this phase.

---

## 1a. `partners.fasta` consumption

**Enumeration.** `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` carries **29 entries** (file sha of bytes on disk is Phase 0's `partners_fasta_sha256 = 0066084e91…c311700c`). Header-declared category, length, and the first 16 hex characters of sha256 for each entry:

| header (label) | len | sha256[:16] | category (self-declared) |
|---|---:|---|---|
| alphas | 394 | 6dedace6845efaa2 | Gα |
| alphai1 | 354 | 57f8013fce15aa58 | Gα |
| alpha13 | 377 | b84f2fe8ce27cec1 | Gα |
| alphaq | 359 | aae9e1c2493fd384 | Gα |
| alphagust | 354 | 69d69c3bddc7e9c1 | Gα |
| alphao | 354 | 399d5823731a6349 | Gα |
| alphai2 | 355 | e0640cb9c3678ef3 | Gα |
| alphaz | 355 | c929d6e535ca2db1 | Gα |
| alpha11 | 359 | 5a59fb4c4388d703 | Gα |
| alphat | 350 | 61cc7bb7a310e3f2 | Gα |
| random_helix_40mer | 40 | 7cd426fc21dc7444 | decoy |
| gcn4_leucine_zipper_33 | 33 | 9569a7eb08514dbd | decoy |
| alphas_F376A_L388A_mutant | 394 | 5c6ac55d09af0460 | Gα |
| alphas_F376A_L388A_R380A_triple_null | 394 | cf709703d5ae80b1 | Gα |
| KaiB_2QKEE | 91 | e7e1c7e7d0960a55 | partner_misc |
| ubiquitin | 76 | 233b4b0b8c461609 | ubiquitin_control |
| HCAR2 | 363 | 82d815907e654032 | partner_misc |
| TAAR1 | 339 | 35a1e025e9505e55 | partner_misc |
| **GASR** | **396** | **30f4709b2d1b3c25** | **Gα (self-declared) — see finding G below** |
| GP161 | 511 | 1c77073c6117e470 | partner_misc |
| **Nb60** | **126** | **b9ad1bad7a2933d8** | **nanobody (self-declared) — see finding N below** |
| arrestin_FL | 15 | a0a09ab53dbc98a2 | arrestin |
| Gg2 | 71 | 32ec703375c0e761 | partner_misc |
| arrestin_Ctail | 41 | 7f7135b3c50ca201 | arrestin |
| GIPR | 528 | 083301fe76c9dfd7 | partner_misc |
| ACM3 | 568 | 298a02a4c76d9897 | partner_misc |
| endothelin1 | 21 | 0b453f9bbe97de92 | partner_misc |
| substanceP | 11 | 7e10bca1b6e43cbe | partner_misc |
| DAMGO | 5 | 96a7bb49fe72f902 | partner_misc |

**Consumption by Block B.** Distinct `partner_identity` values in `experiments/019_block_b_partner_selection/manifest/manifest.csv` (3,200 rows, all 640 cells):

- apo cells (160): `partner_identity` empty; no partner.
- cognate cells (160): exactly four distinct identities used — `alphai1`, `alphaq`, `alphas`, `alphat`. All 40 receptors' cognate arm routes match `refs/gpcr_coupling.csv:primary_ga_identity` (checked: 40/40 OK).
- decoy cells (160): 40 distinct identities of the form `<receptor>_decoy`, each pointing to its own `refs/constructs_block_b/<receptor>_decoy.fasta`.
- shuffled cells (160): 40 distinct identities of the form `<receptor>_shuffled`, each pointing to its own `refs/constructs_block_b/<receptor>_shuffled.fasta`.

**No Block B row consumed any of the following partners.fasta entries:** `alpha13`, `alphagust`, `alphao`, `alphai2`, `alphaz`, `alpha11`, `random_helix_40mer`, `gcn4_leucine_zipper_33`, `alphas_F376A_L388A_mutant`, `alphas_F376A_L388A_R380A_triple_null`, `KaiB_2QKEE`, `ubiquitin`, `HCAR2`, `TAAR1`, `GASR`, `GP161`, `Nb60`, `arrestin_FL`, `Gg2`, `arrestin_Ctail`, `GIPR`, `ACM3`, `endothelin1`, `substanceP`, `DAMGO`. All 25 unused entries are inert with respect to the Block B corpus.

**Finding G — GASR (self-declared `category=Gα`, len=396) — NOT consumed in Block B.** GASR's sequence begins `MELLKLNRSVQGTGPGPGASLCRPGAPLLNSSSVGN…` and encodes seven trans-membrane helices; it is the **CCKB / gastrin receptor**, a Class A GPCR, not a Gα. The mislabel does not touch Block B (0 rows consumed it, CCKAR's cognate arm correctly uses `alphaq`). It is nonetheless a documented mislabel in the primary partner file and would silently masquerade as a Gα in any downstream analysis that trusts the header. Recommendation lives outside this phase; only the sequence-hash-based finding is recorded here.

**Finding N — Nb60 (self-declared, len=126) — NOT consumed in Block B; MISLABEL confirmed by hash.** Sequence bytes and hashes side by side:

| source | sha256[:16] | length | last 20 chars |
|---|---|---:|---|
| `partners.fasta:Nb60` | b9ad1bad7a2933d8 | 126 | `LTAPWYDYWGQGTQVTVSS` |
| `refs/nanobody_sequences.fasta:Nb60\|Nb\|5JQH\|inactive\|receptor=ADRB2` | 1406ad7ea2645114 | 125 | `TQVTVSSHHHHHH` (with 6×His tag) |

Different bytes. The `partners.fasta` Nb60 CDR3 `RRIYGSSWYLTAPWYDY` is the **Nb80** CDR3 (Rasmussen 2011 β2AR active-state nanobody, PDB 3P0G), not the real Nb60 (Staus 2016 β2AR inactive-state nanobody, PDB 5JQH). The nanobody-sequences file's `Nb60|5JQH` entry has the correct 5JQH CDR3 `KVAGTFSIYDY`. **`partners.fasta` header `Nb60` is a mislabel of Nb80.** The `refs/tier_d2_panel.csv` notes column already flags this: *"partners.fasta already carries an entry keyed 'Nb60' whose sequence is Rasmussen 2011 Nb80 (mislabelled); this FASTA uses PDB-suffixed keys to disambiguate."* Not new; confirmed by hash here.

**Cross-block audit — Block D D2 active-Nb vs inactive-Nb for ADRB2 use IDENTICAL sequences.** Read the two `.yaml` input files on HPC:

- `experiments/023_tier_d2_directed_inactive/full/pool/inputs/boltz/tier_d2_adrb2_active_nb_boltz_seed0.yaml` chain B sequence: `QVQLQESGGGLVQAGGSLRLSCAASGSIFSLNDMGWYRQAPGKLRELVAAITSGGSTKYADSVKGRFTISRDNAKNTVYLQMNSLKAEDTAVYYCNAKVAGTFSIYDYWGQGTQVTVSSHHHHHH` — sha256 = `1406ad7ea26451149ea73339e2282ef0f77f52d693c680cbf790db7af767db62`, len 125.
- `.../tier_d2_adrb2_inactive_nb_boltz_seed0.yaml` chain B sequence: identical bytes, same sha256 (`1406ad7ea…`).

Both subarms fed the **same** Nb60_5JQH (inactive-state) nanobody to Boltz. The D2 manifest itself explicitly annotates the active-Nb subarm with `partner_perturbation=placeholder_nb80_from_nb60_5jqh` — the pipeline intended to substitute 4LDE's engineered Nb ("Nb80-like") but the substitution never landed, and Nb60_5JQH bytes were emitted as the chain-B sequence for BOTH ADRB2 D2 subarms.

**Implication (recorded, not interpreted here per the brief):** Block D D2's active-Nb-vs-inactive-Nb ADRB2 contrast is confounded — the same 125-aa Nb60_5JQH sequence is present in both subarms. Any Block D manuscript sentence contrasting D2 active-Nb vs inactive-Nb ADRB2 needs to route through this fact. Not a Block B invalidator; Block B never touched D2's Nb sequences.

---

## 1b. Decoy construction

**Files enumerated.** `refs/constructs_block_b/` holds one `<slug>_decoy.fasta` per receptor plus `build_manifest.csv` (320 rows = 40 receptors × 4 backbones × 2 arms, all pointing at the 40+40 fasta files). Every decoy fasta is single-entry, non-empty.

**Method.** For each receptor, hash-load the decoy fasta (single sequence) and the cognate Gα parent from `partners.fasta` per `refs/gpcr_coupling.csv:primary_ga_identity` (edge cases: `EDNRA → alphaq` and `OPSD → alphat` both routed correctly). Prefix identity is the length of the byte-identical head; tail edit length is `|decoy| − prefix`; Hamming distance is character-mismatch across the aligned suffix.

**Result — 40 rows.** Every decoy is length-matched to its parent Gα, byte-identical over the first 339–349 residues, and edited over the last 9–11 (α5-CT tail). All rows pass `length_match_ok`.

| receptor | parent Gα | \|P\|=\|D\| | prefix_identical_len | tail_edit_len | tail_hamming | note |
|---|---|---:|---:|---:|---:|---|
| 5HT1B | alphai1 | 354 | 343 | 11 | 10 | OK |
| 5HT2C | alphaq | 359 | 348 | 11 | 9 | OK |
| 5HT5A | alphai1 | 354 | 343 | 11 | 10 | OK |
| AA1R | alphai1 | 354 | 343 | 11 | 11 | OK |
| AA2AR | alphas | 394 | 383 | 11 | 9 | OK |
| ACM1 | alphaq | 359 | 348 | 11 | 9 | OK |
| ACM2 | alphai1 | 354 | 344 | 10 | 9 | OK |
| ACM4 | alphai1 | 354 | 343 | 11 | 7 | OK |
| ADA2A | alphai1 | 354 | 344 | 10 | 9 | OK |
| ADRB1 | alphas | 394 | 383 | 11 | 10 | OK |
| ADRB2 | alphas | 394 | 383 | 11 | 10 | OK |
| AGTR1 | alphaq | 359 | 348 | 11 | 10 | OK |
| APJ | alphai1 | 354 | 344 | 10 | 7 | OK |
| B1B1U5 | alphai1 | 354 | 343 | 11 | 10 | OK |
| CCKAR | alphaq | 359 | 349 | 10 | 8 | OK |
| CCR5 | alphai1 | 354 | 343 | 11 | 10 | OK |
| CNR1 | alphai1 | 354 | 343 | 11 | 8 | OK |
| CNR2 | alphai1 | 354 | 345 | 9 | 9 | OK |
| CXCR2 | alphai1 | 354 | 343 | 11 | 10 | OK |
| CXCR4 | alphai1 | 354 | 343 | 11 | 9 | OK |
| DRD2 | alphai1 | 354 | 343 | 11 | 9 | OK |
| DRD3 | alphai1 | 354 | 343 | 11 | 9 | OK |
| EDNRA | alphaq | 359 | 348 | 11 | 11 | OK |
| EDNRB | alphaq | 359 | 348 | 11 | 10 | OK |
| FSHR | alphas | 394 | 383 | 11 | 11 | OK |
| GHSR | alphaq | 359 | 349 | 10 | 8 | OK |
| GRPR | alphaq | 359 | 348 | 11 | 9 | OK |
| HRH1 | alphaq | 359 | 348 | 11 | 9 | OK |
| HRH3 | alphai1 | 354 | 343 | 11 | 9 | OK |
| LPAR1 | alphai1 | 354 | 343 | 11 | 10 | OK |
| LSHR | alphas | 394 | 383 | 11 | 9 | OK |
| LT4R1 | alphai1 | 354 | 343 | 11 | 11 | OK |
| MCHR1 | alphai1 | 354 | 343 | 11 | 11 | OK |
| NPY1R | alphai1 | 354 | 343 | 11 | 11 | OK |
| NPY2R | alphai1 | 354 | 343 | 11 | 11 | OK |
| OPRD | alphai1 | 354 | 343 | 11 | 9 | OK |
| OPRK | alphai1 | 354 | 343 | 11 | 10 | OK |
| OPRX | alphai1 | 354 | 343 | 11 | 11 | OK |
| OPSD | alphat | 350 | 339 | 11 | 10 | OK |
| OX2R | alphaq | 359 | 348 | 11 | 9 | OK |

Content-based verification (the compensating control Phase 0 §2 required, given empty `propose_py_git_sha` / `build_manifest_py_git_sha`) is met on all 40: byte-identical prefix, length parity, tail confined to α5-CT, Hamming ≥ 7 per tail (tail-Hamming median 9.5). The two edge-case routings (EDNRA → alphaq, OPSD → alphat) match `refs/gpcr_coupling.csv`. **No decoy fails content verification.**

---

## 1c. Shuffled construction + `donor_ga_class` column

**Method.** For each `<slug>_shuffled.fasta`, hash-load its single sequence and identify the donor by sha256 lookup against `partners.fasta`. Class of donor (`Gs`, `Gi`, `Gq`, `G12`, `Gt`) is derived from partners.fasta identity via the mapping `alphas/alphai1_2_o_z_gust/alphaq_11/alpha13/alphat`. Cognate class is `refs/gpcr_coupling.csv:primary_ga_class`; secondary classes are the receptor's `secondary_ga_classes` column.

**Result.** Only **3 distinct donor sequences** are used across the 40 shuffled arms:

| donor identity | donor class | sha256[:16] | # receptors |
|---|---|---|---:|
| alphas | Gs | 6dedace6845efaa2 | 33 |
| alphai1 | Gi | 57f8013fce15aa58 | 6 |
| alpha13 | G12 | b84f2fe8ce27cec1 | 1 |

Per-receptor breakdown of donor vs cognate:

| receptor | cognate class | secondary classes | shuffled donor | donor class | donor ≠ cog and ≠ any secondary? |
|---|---|---|---|---|---|
| 5HT1B | Gi | — | alphas | Gs | yes |
| 5HT2C | Gq | — | alphas | Gs | yes |
| 5HT5A | Gi | — | alphas | Gs | yes |
| AA1R | Gi | — | alphas | Gs | yes |
| AA2AR | Gs | — | alphai1 | Gi | yes |
| ACM1 | Gq | — | alphas | Gs | yes |
| ACM2 | Gi | — | alphas | Gs | yes |
| ACM4 | Gi | — | alphas | Gs | yes |
| ADA2A | Gi | — | alphas | Gs | yes |
| ADRB1 | Gs | — | alphai1 | Gi | yes |
| ADRB2 | Gs | — | alphai1 | Gi | yes |
| AGTR1 | Gq | Gi, G12 | alphas | Gs | yes |
| APJ | Gi | Gq | alphas | Gs | yes |
| B1B1U5 | Gi | Gq | alphas | Gs | yes |
| CCKAR | Gq | Gs | alphai1 | Gi | yes |
| CCR5 | Gi | — | alphas | Gs | yes |
| CNR1 | Gi | — | alphas | Gs | yes |
| CNR2 | Gi | — | alphas | Gs | yes |
| CXCR2 | Gi | — | alphas | Gs | yes |
| CXCR4 | Gi | — | alphas | Gs | yes |
| DRD2 | Gi | — | alphas | Gs | yes |
| DRD3 | Gi | — | alphas | Gs | yes |
| EDNRA | Gq | Gs, Gi | alpha13 | G12 | yes |
| EDNRB | Gq | Gi | alphas | Gs | yes |
| FSHR | Gs | Gq | alphai1 | Gi | yes |
| GHSR | Gq | Gi, G12 | alphas | Gs | yes |
| GRPR | Gq | — | alphas | Gs | yes |
| HRH1 | Gq | — | alphas | Gs | yes |
| HRH3 | Gi | — | alphas | Gs | yes |
| LPAR1 | Gi | Gq, G12 | alphas | Gs | yes |
| LSHR | Gs | Gq | alphai1 | Gi | yes |
| LT4R1 | Gi | Gq | alphas | Gs | yes |
| MCHR1 | Gi | Gq | alphas | Gs | yes |
| NPY1R | Gi | — | alphas | Gs | yes |
| NPY2R | Gi | — | alphas | Gs | yes |
| OPRD | Gi | — | alphas | Gs | yes |
| OPRK | Gi | — | alphas | Gs | yes |
| OPRX | Gi | — | alphas | Gs | yes |
| OPSD | Gt | — | alphas | Gs | yes |
| OX2R | Gq | Gi | alphas | Gs | yes |

**40/40 rows have donor_ga_class strictly outside `{cognate_class} ∪ {secondary_classes}`** — the "shuffled" arm is genuinely wrong-family across the panel, including for the seven promiscuous receptors that carry secondary couplings (AGTR1, APJ, B1B1U5, CCKAR, EDNRA, EDNRB, FSHR, GHSR, LPAR1, LSHR, LT4R1, MCHR1, OX2R). **No receptor's shuffled donor is same-class as cognate; no receptor's shuffled donor is even in the receptor's known secondary set.**

**`donor_ga_class.csv` emitted.** `experiments/019_block_b_partner_selection/analysis/donor_ga_class.csv` — one row per (receptor, arm, backbone) cell, 640 rows, 7 columns: `receptor, arm, backbone, donor_ga_identity, donor_ga_class, cognate_ga_identity, cognate_ga_class`. Semantics:

- apo cells: `donor_ga_identity = ""` and `donor_ga_class = ""` (no partner).
- cognate cells: `donor_ga_identity` = the manifest-declared cognate (`alphai1`/`alphaq`/`alphas`/`alphat`); `donor_ga_class` = its class.
- decoy cells: `donor_ga_identity = "<slug>_decoy"`; `donor_ga_class = "<cognate_class>_scaffold_scrambled"` (scaffold is the cognate parent).
- shuffled cells: `donor_ga_identity` resolved from the shuffled fasta's sha (one of the three donors above); `donor_ga_class` is that donor's class.

Phase 5 downstream reads this file directly.

---

## 1d. MSA column-repair audit (the load-bearing check)

**Scope.** The decoy edit is confined to the α5-CT tail (~9–11 residues). If the MSA columns at those positions are dominated by wild-type Gα residues from homolog rows, the decoy is not a decoy at the layer the model reads. This section examines what the actual MSA files contain per backbone × arm × receptor, keeping every observation strictly separate from interpretation.

### 1d.i Chai — `.aligned.pqt` cache on HPC

**Location and coverage.** `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai/` — 139 files of form `<sha256>.aligned.pqt`. Each pqt is a per-chain MSA keyed by sha256 of that chain's sequence. Chai's launcher `qsub/rerun_chai.sh` defaults `CHAI_MSA_DIRECTORY=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai` with an in-line `.aligned.pqt` pre-flight (audit #10 countermeasure).

Coverage vs Block B partners:

- **40/40 receptor pqts present** (`<panel_sha>.aligned.pqt`, one per receptor).
- **4/4 cognate Gα pqts present** (`alphai1`, `alphas`, `alphaq`, `alphat`; correct 64-hex shas match `partners.fasta`).
- **40/40 decoy pqts present** (keyed by each `<slug>_decoy` sha256 from `refs/constructs_block_b/build_manifest.csv:partner_seq_sha`).
- **3/3 shuffled donor pqts present** (`alphas`, `alphai1`, `alpha13` — same shas as the cognate `alphas` and `alphai1`; `alpha13` is unique to shuffled).

**Schema.** Every pqt has 4 columns: `sequence` (aligned string with `-` gaps and lowercase insertions), `source_database` (`query`, `uniref90`, `bfd_uniclust`), `pairing_key` (string; expected non-empty for paired rows), `comment`. Row 0 is the query row.

**File-hash collision check.** Decoy pqts vs their cognate parent pqts — **0/40 byte-identical** (different row counts, different md5s). Decoy pqts are not copies of cognate pqts.

**Receptor-side MSA identity across arms.** The receptor's sequence is invariant across `{apo, cognate, decoy, shuffled}`, and Chai's msa_directory is keyed by chain sha256 → the SAME `<receptor_sha>.aligned.pqt` file is loaded for the receptor chain in all four arms of every receptor. **Receptor-side MSA is identical across arms by construction (40/40).**

**Pairing status.** In every Chai pqt inspected (cognate alphai1, cognate alphas, decoy 5HT1B, decoy AA2AR, decoy OPSD, decoy EDNRA, and the three shuffled donors) — `pairing_key` is **empty for 100 % of rows**. No paired hits are supplied to Chai for any Block B arm — cognate included. **Pairing was never wired into the Block B Chai MSAs**, and this is invariant across arms (not a decoy-specific gap).

**Query-row content per arm (α5-CT columns).** The pqt query rows contain the α5-CT tail only in the cognate and shuffled arms; the decoy pqt's query rows do not.

Concrete per-arm samples — last 20 raw characters of the query row (uppercase = matched to alignment consensus, lowercase = insertion, `-` = gap in query):

| pqt | last 20 chars of query row (raw) | ends with WT parent tail | ends with scrambled tail |
|---|---|---|---|
| **cognate alphai1** (sha `57f8013f…`) | `VFDAVTDVIIKNNLKDCGLF` | YES (`IKNNLKDCGLF`) | n/a |
| **cognate alphas** (sha `6dedace6…`) | `VFNDCRDIIQRMHLRQYELL` | YES (`QRMHLRQYELL`) | n/a |
| **cognate alphaq** (sha `aae9e1c2…`) | `VFAAVKDTILQLNLKEYNLV` | YES (`LQLNLKEYNLV`) | n/a |
| **cognate alphat** (sha `61cc7bb7…`) | `VFDAVTDIIIKENLKDCGLF` | YES (`IKENLKDCGLF`) | n/a |
| **shuffled donor alphas** (sha `6dedace6…`) | `VFNDCRDIIQRMHLRQYELL` | YES (WT donor tail) | n/a |
| **shuffled donor alphai1** (sha `57f8013f…`) | `VFDAVTDVIIKNNLKDCGLF` | YES | n/a |
| **shuffled donor alpha13** (sha `b84f2fe8…`) | `VKDTILHDNLKQLMLQ` (last 16) | YES | n/a |
| **decoy 5HT1B** (sha `fcaf9cbb…`) | `DAVTDVIIknNLKD------` | NO | **NO** |
| **decoy AA2AR** (sha `d8a9dac9…`) | `VFNDCRDIIQRMHLRQYE--` | ends 9 WT chars + 2 gaps | NO |
| **decoy OPSD** (sha `450ca373…`) | `VFDAVTDII-----------` | 11 trailing gaps at α5-CT | NO |
| **decoy EDNRA** (sha `584c8caf…`) | `VKDTILQLNlkeyNLRQ---` | mostly WT parent + gaps + lowercase | NO |

Panel-wide across all 40 decoy pqts:

| observation | count / 40 |
|---|---:|
| decoy pqt query row ends with scrambled tail (uppercase) | **0** |
| decoy pqt query row ends with WT parent tail (uppercase) | 2 (ADRB1, LSHR) |
| decoy pqt query row has ≥3 trailing gaps at the α5-CT position | 19 |
| decoy pqt query row has 1–2 trailing gaps + mostly-WT residues before them | 19 |
| decoy pqt query row nogap-uppercase length < raw decoy length | 40 |

**Interpretation-free summary.** The 40 decoy pqt files exist under the decoy sequences' sha256 filenames, but the **query row's aligned uppercase content in every decoy pqt is either (a) trailing gaps at the α5-CT positions, or (b) WT parent Gα residues at those positions, or (c) lowercase-marked insertions**. None of the 40 decoy pqts have the scrambled α5-CT residues as uppercase-aligned columns in the pqt query row. Concretely, for 5HT1B_decoy — the raw decoy tail is `CNLKDILFGKN`; the pqt-decoy query nogap-uppercase last 15 chars are `FDAVTDVIIKNNLKD`, matching `alphai1[335:350]` (WT parent), followed by 6 trailing gaps. For 21 of the 40 decoys, some scrambled-position characters appear in the query row as **lowercase** (MMseqs2's "column not part of the aligned block" annotation), meaning those residues are present in the pqt query but marked as insertions rather than aligned columns.

**MSA-content probe — WT-match and gap fraction at aligned columns.** For 5HT1B (cognate `alphai1`) at its α5-CT columns (positions 343–353 of the alignment, which are aligned uppercase residues in the query), the homolog rows show:

| tail_i | col | q | wt | gap% | wt_match% |
|---:|---:|---|---|---:|---:|
| 0 | 343 | I | I | 37.27 | 13.15 |
| 5 | 348 | K | K | 39.75 | 5.77 |
| 10 | 353 | F | F | 46.73 | 4.29 |

(medians across the 11 α5-CT columns: gap ≈ 40 %, wt_match ≈ 6 %). For **cognate `alphas`** at its α5-CT columns (383–393): gap ≈ 44 %, wt_match ≈ 8–17 %. For **decoy 5HT1B** at "last 11 aligned uppercase columns of query" (which correspond to alphai1 positions 339–349, NOT to any position of the scrambled tail — because the pqt query has no aligned uppercase columns at scrambled positions): gap ≈ 37–53 %, WT-match at each column vs the scrambled residue is < 6 %. This means: the columns where a scrambled-tail decoy input residue would map (0-indexed 343–353 in the raw decoy) **do not exist as aligned columns in the pqt at all**; the pqt's homolog rows are anchored to a query row whose α5-CT is either gapped or WT-parent.

**What this means at the MSA-feature layer, per the three-outcome frame requested:**

- **(High WT-match)** No — the scrambled positions have no aligned MSA column to match against.
- **(High gap in the aligned pqt for scrambled positions)** YES — all 40 decoys have the scrambled residues either as trailing gaps or as lowercase insertions in the pqt query. Chai's MSA feature at the model-input positions 343–353 is anchored to columns that do not carry decoy residues in the query row.
- **(Mixed)** For 21/40 decoys, scrambled residues appear as **lowercase** in the pqt query (MMseqs "insertion" annotation) rather than pure gaps; the aligned columns adjacent to the α5-CT show WT-parent residues in the query, and the homolog rows aligned to those columns are anchored to the parent Gα profile.

**Not decided here (out of Phase 1 scope):** whether Chai's downstream MSA-feature builder ingests the raw decoy sequence (from the input yaml, 354 aa) and re-aligns it against the pqt, or ingests the pqt's query row as-is (350 aa nogap for 5HT1B) and pads. Either behavior has a load-bearing consequence for what the model reads at scrambled positions. Chai code inspection is not part of this phase. **What is established here is that the pqt query row for every decoy does not carry the scrambled α5-CT residues as aligned uppercase columns.**

### 1d.ii Boltz, Protenix, OpenFold-3 — not covered in this pass

Per PREREG §11c-d, Boltz and Protenix consume ColabFold public-API cached a3m/MSA outputs; OF3 runs ColabFold via the shim (`qsub/colabfold_shim.py`) at each dispatch. These three backbones do not share Chai's `.aligned.pqt` cache — each has its own MSA fetch and cache layout that would need a separate audit against the same three-outcome frame. That audit was not run in this Phase 1 pass; it can be scoped as a follow-up if the Chai-side observation is deemed load-bearing enough to require the same reading per backbone. The Chai observation reported above is one backbone of four and does not automatically generalise to the other three.

**Receptor-side MSA identity across arms (all four backbones by construction).** Regardless of MSA source, the receptor chain's sequence bytes are identical across `{apo, cognate, decoy, shuffled}` for every receptor (per §1b: no decoy modifies the receptor chain; per §1c: no shuffled modifies the receptor chain; and cognate/apo differ only in whether a partner chain is present). All four backbones key MSAs by chain content, so **receptor-side MSA is identical across arms for every backbone by construction** (Chai verified above; Boltz/OF3/Protenix rely on their respective ColabFold caches keyed on the receptor sha, which is arm-invariant). This is the axis that would be most likely to introduce arm-dependent receptor bias, and it does not — arm effects observed in the corpus are not receptor-MSA-driven.

---

## GATE 1 verdict — CONDITIONAL

**Not FAIL.** Arm construction is fully established on the 40 Class A receptors:

- Cognate arm: 40/40 receptors route to the correct `refs/gpcr_coupling.csv` primary Gα partner (verified by hash on the manifest's `partner_identity`).
- Decoy arm: 40/40 decoys are length-matched, byte-identical over the prefix, and edited only in the α5-CT tail (Hamming 7–11). Cognate parent routing including edge cases (OPSD → alphat, EDNRA → alphaq) correct.
- Shuffled arm: 40/40 use a donor whose Gα class is strictly outside `{cognate_class} ∪ {secondary_classes}`; only three donor sequences shared across the 40 (`alphas`, `alphai1`, `alpha13`); no same-class or same-secondary confusions.
- Companion `donor_ga_class.csv` emitted; Phase 5 can proceed.
- Two mislabels confirmed in `partners.fasta` (`Nb60` really Nb80, `GASR` really CCKB receptor) — **both entries UNUSED by Block B**, so neither invalidates the corpus.

**CONDITIONAL on the following observations, none of which by itself invalidates Block B:**

1. **Chai decoy `.aligned.pqt` query rows do not contain the scrambled α5-CT residues as aligned uppercase columns** (0/40). The MSA feature at the scrambled positions of the model-input decoy is anchored — in the pqt — to WT parent Gα residues, gaps, and lowercase insertions. Whether Chai's downstream MSA-feature builder re-aligns the pqt against the raw decoy or trusts the pqt query row as-is is not decided by this phase; both routes have load-bearing consequences and code inspection is out of scope. **User adjudication required** on whether this warrants scoped Chai code inspection before Phase 6 interpretation of Block B decoy vs cognate effects lands. Recommendation (recorded, not chased): a targeted read of `chai_lab`'s msa loader and a paired probe of one Chai decoy run's runtime tensor at positions 343–353 would settle it in an afternoon.

2. **Pairing_key is empty across every pqt row inspected** — both cognate and decoy arms. Chai received unpaired receptor-partner MSAs for all 640 Block B cells. This is invariant across arms (not a decoy-specific gap) but it means "pairing_key was reported as not preserved for decoy MSAs" (per the phase 1 brief framing) is actually "pairing_key was never preserved for any Block B Chai arm." Pairing effects cannot be responsible for decoy-vs-cognate differences.

3. **Boltz / OF3 / Protenix MSA content at α5-CT columns is not audited in this phase.** The three-outcome frame was applied only to Chai. The other three backbones each fetch MSAs from ColabFold (either via the pre-warmed public-API cache or via the OF3 shim); the decoy vs cognate MSA-column comparison for them is a separate audit that was not run here. Absence of the audit is not evidence of correctness on those backbones. **User adjudication required** on whether Phase 1 should be extended, or whether the Chai finding is sufficient as a per-arm construct-identity observation.

4. **Cross-block finding — Block D D2 active-Nb vs inactive-Nb for ADRB2 use IDENTICAL sequences** (both fed the 125-aa Nb60_5JQH inactive-state nanobody as chain B; manifest's `partner_perturbation=placeholder_nb80_from_nb60_5jqh` marks the failed substitution). Not a Block B invalidator — Block B never touched D2 Nb sequences — but load-bearing for any Block D manuscript sentence contrasting D2 active-Nb vs inactive-Nb ADRB2. Recorded here because the phase-1 brief specifically requested the cross-block sequence-hash comparison; adjudication of what to do with it belongs to a Block D dossier.

5. **`partners.fasta` mislabels documented, not consumed.** `Nb60` (really Nb80) and `GASR` (really CCKB receptor) are inert w.r.t. Block B rows but remain mislabelled in the primary partner file. Any future block that consumes `partners.fasta:Nb60` or `partners.fasta:GASR` without sha-based routing will inherit the mislabels silently.

Ladder computation for Block B is authorised on the strength of §1a–1c passing 40/40 by content. Phase 2 can proceed. **§1d Chai observation should be raised to the user before Block B's decoy-vs-cognate manuscript sentence is anchored to an MSA-feature interpretation; the corpus itself is not invalidated.**
