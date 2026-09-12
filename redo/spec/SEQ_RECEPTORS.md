# SEQ_RECEPTORS.md — chain A, the receptor sequence the redo hands to a model

Written 2026-09-11 by the chain-A session. Sibling to `redo/spec/SEQUENCES.md`,
which specifies **chain B** (every partner construct: 112 ladder rungs, 240
controls, all hashed) and which says of the receptor only this, in §8:

> Receptor chain. UniProt canonical, full length, wild type. No BRIL/T4L fusion,
> no thermostabilising mutations, no truncation.

That is a rule with no sequences behind it, and this file is the other half.
`redo/inputs/panel_systems.csv` carries the roster and a UniProt accession per
receptor; **no file in this repository has ever carried a receptor sequence**
(checked: `find` for `panel_receptor_sequences.fasta` returns nothing, and
`data/block_b/03_msa_audit/msa_depth_report.md` is the only place the pipeline's
own receptor lengths appear at all). So the molecule the whole experiment is
about has been specified by accession and by nothing else.

**Nothing below is written from memory.** Every sequence is sliced from a
fetched UniProt record with its accession, sequence version and
last-sequence-update date recorded; every deposited construct is read from an
RCSB entity; every segment boundary comes from UniProt's feature table or
GPCRdb's generic-numbering residue service. Every construct carries a sha256.
Fetch date for every record below: **2026-09-11**.

## Companions, all regenerable

| file | what | built by |
|---|---|---|
| `redo/inputs/seqrec_receptors.tsv` | 77 records: 64 core + 11 extension + 2 human-orthologue candidates. Accession, entry, SV, length, sha256, signal peptide, TM spans, N/C terminal lengths, isoform census, glyco/disulfide/lipidation counts | `seqrec_build.py` |
| `redo/inputs/seqrec_canonical.fasta` | the 77 canonical sequences, header carries accession, SV, length and sha256 | `seqrec_build.py` |
| `redo/inputs/seqrec_features.tsv` | long-format UniProt features: SIGNAL, CHAIN, TRANSMEM, TOPO_DOM, CARBOHYD, DISULFID | `seqrec_build.py` |
| `redo/inputs/seqrec_refs.tsv` | 128 rows, one per rule-R reference receptor entity: what was crystallised, which canonical residues it contains, which it resolves, the substitution recount, fusion insertion points | `seqrec_refs.py` |
| `redo/inputs/seqrec_scoreable.tsv` | 64 rows: canonical residues present and resolved in **both** references, as an exact residue-range string | `seqrec_refs.py` |
| `redo/inputs/seqrec_icl3_audit.tsv` | 128 rows: **where** each reference's fusion sits — ICL3, a terminus, or elsewhere | `seqrec_icl3_audit.py` |
| `redo/inputs/seqrec_trim.tsv` | the `miglionico2026atlas` terminal cap applied to all 75 panel receptors: boundaries from both authorities, capped range, capped sha256, residues removed at each end | `seqrec_trim.py` |
| `redo/inputs/seqrec_trimmed.fasta` | the capped chain-A sequences | `seqrec_trim.py` |
| `redo/cache/seqrec_rcsb_entities.json`, `seqrec_gpcrdb_residues.json` | the raw fetched responses, so nothing here needs the network twice | caches |
| `redo/gates/seqrec_verify.py` | **recomputes every number in this document**; 53 checks, all passing on 2026-09-11 | — |

`python3 redo/gates/seqrec_verify.py` is the live source of truth. The prose
below may lag it; it may not contradict it. `--plant` deliberately corrupts the
roster and is expected to fail — a verifier that passes under `--plant` is not
reading what it claims to.

---

# 0. The five conventions

**0.1 Constructs are keyed by hash, never by header.** Same rule and same reason
as `SEQUENCES.md` §0.1: `construct_id = sha256(uppercase one-letter sequence,
UTF-8, no header, no newline, no whitespace)`. Chain B earned that rule by
producing three mislabels in one 29-entry file. **Chain A has never been hashed
at all in any drop, A through D.** The near misses, checked rather than assumed:

- `rows_tidy.csv:input_sha256` and `block_a_rows.csv:input_sha256` **look** like
  the column that would settle it and are not. `data/block_b/DATA_DICTIONARY.md:149`
  defines it as a *"per-CIF byte hash"* — a hash of the output structure, one
  distinct value on each of the 32,000 rows. It identifies a prediction, not an
  input chain.
- `data/block_b/02_constructs/d2_arm_sequence_audit.csv` hashes nanobody chains
  and reads `unknown (partner_type=apo or g_alpha)` elsewhere; the Gα sequence
  hashes are in `03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md`. Neither file hashes
  a receptor chain.
- `block_a_rows.csv` carries `ref_pdb_sha_active` / `ref_pdb_sha_inactive` — the
  reference *structures*, not the supplied sequence.

The receptor is the one chain present in every single prediction the project has
ever run and it is the one chain whose identity is not recoverable from any
shipped file.

**0.2 A construct is expressed as a rule plus a canonical residue range, and both
are recorded.** `ADRB2 29–365` is meaningless without `P07550 SV 3`; the same
numbers on a different sequence version are a different molecule.

**0.3 The receptor's species and the partner's species are separate columns.**
`SEQUENCES.md` §3.3 introduced this for the partner side. Three of the 64 core
receptors are not human and the column is the only thing that makes a
cross-species row visible.

**0.4 What is supplied and what is scored are different sets, and both are
recorded per row.** We supply a chain; the reference contains a subset of it and
resolves a subset of that. §6 makes the difference explicit and the existing
`rmsd_n_residues_used` column shows the pipeline already knew.

**0.5 Where a decision is the PI's, it is presented costed and not made.** §4.3
(the glycoprotein-hormone ectodomains) and §3.1 (the signal peptide) are the two
that qualify. Flagging UNRESOLVED beats a wrong residue range.

---

# 1. The roster

From `redo/inputs/panel_systems.csv`, the core is the rows where
`'C1' in tier.split('|')`: **64 receptors, every one Class A**, every one with
seven UniProt-annotated transmembrane helices. Eleven further receptors sit in
the extension tiers and are specified here but flagged separately, because their
construct decisions are genuinely different:

| tier | n | receptors | why the construct differs |
|---|---:|---|---|
| **C1 — core** | **64** | all Class A | the working panel; Group 1 needs chain A for every one |
| `E-B1` | 5 | CALRL, CRHR1, GCGR, GLP1R, PTH1R | large, folded, functionally distinct ECD — §4.2 |
| `E-scope` | 5 | AGRE5 (B2), FZD4, FZD6, FZD7, SMO (F) | CRD / GAIN domains; declared scope, no claim |
| `X` | 1 | ACM3 | excluded by PANEL.md's species clause; sequence given for completeness |

`E-pro` (8 prospective Class A receptors, inactive structure only) has no row in
`panel_systems.csv` and therefore no accession here. **UNRESOLVED-1**: if E-pro
is run, its eight accessions must be added to `panel_systems.csv` first; this
file cannot invent them.

---

# 2. The canonical sequences

All 77 records fetched 2026-09-11 from `https://rest.uniprot.org/uniprotkb/{acc}.json`.
`scoreable` is §6's number: canonical residues resolved in **both** rule-R
references. `capped` is §4's construct.

| # | slug | accession | entry | SV | len | sha256[:16] | signal | TM1 | H8 | capped range | capped len | capped sha256[:16] | scoreable |
|---:|---|---|---|---:|---:|---|---|---:|---|---|---:|---|---:|
| 1 | **5HT1B** | `P28222` | 5HT1B_HUMAN | 1 | 390 | `0bc8c4af6f71c065` | — | 45 | 373-384 | 1–390 | 390 | `0bc8c4af6f71c065` | 260 |
| 2 | **5HT2A** | `P28223` | 5HT2A_HUMAN | 2 | 471 | `2b9b5928cca6ac49` | — | 69 | 384-397 | 19–471 | 453 | `6a863bfc1d508097` | 267 |
| 3 | **5HT2C** | `P28335` | 5HT2C_HUMAN | 2 | 458 | `8bb8e760c142b1a4` | 1-32 | 54 | 372-385 | 4–458 | 455 | `c5073ae11cd45c1f` | 261 |
| 4 | **5HT5A** | `P47898` | 5HT5A_HUMAN | 1 | 357 | `d2f2f70ece4e1535` | — | 36 | 342-353 | 1–357 | 357 | `d2f2f70ece4e1535` | 251 |
| 5 | **AA1R** | `P30542` | AA1R_HUMAN | 1 | 326 | `1287bf4746a29da7` | — | 6 | 292-314 | 1–326 | 326 | `1287bf4746a29da7` | 282 |
| 6 | **AA2AR** | `P29274` | AA2AR_HUMAN | 2 | 412 | `d1707e447ac7d7fc` | — | 1 | 292-314 | 1–412 | 412 | `d1707e447ac7d7fc` | 278 |
| 7 | **ACM1** | `P11229` | ACM1_HUMAN | 2 | 460 | `a9d70e6dd79a9d6d` | — | 21 | 422-435 | 1–460 | 460 | `a9d70e6dd79a9d6d` | 275 |
| 8 | **ACM2** | `P08172` | ACM2_HUMAN | 1 | 466 | `18e4fe4189d4300e` | — | 19 | 444-456 | 1–466 | 466 | `18e4fe4189d4300e` | 257 |
| 9 | **ACM4** | `P08173` | ACM4_HUMAN | 2 | 479 | `f70d1259f715e662` | — | 26 | 457-471 | 1–479 | 479 | `f70d1259f715e662` | 267 |
| 10 | **ADA1A** | `P35348` | ADA1A_HUMAN | 2 | 466 | `1e43c78d6315a3dc` | — | 20 | 330-342 | 1–442 | 442 | `7a7ac0d79fae033e` | 263 |
| 11 | **ADA2A** | `P08913` | ADA2A_HUMAN | 4 | 465 | `0153dbebb226a1e5` | — | 46 | 445-458 | 1–465 | 465 | `0153dbebb226a1e5` | 259 |
| 12 | **ADRB1** | `P08588` | ADRB1_HUMAN | 3 | 477 | `18fcd61221ac38d0` | — | 50 | 380-392 | 1–477 | 477 | `18fcd61221ac38d0` | 277 |
| 13 | **ADRB2** | `P07550` | ADRB2_HUMAN | 3 | 413 | `9abd88979dbbdef0` | — | 26 | 329-341 | 1–413 | 413 | `9abd88979dbbdef0` | 202 |
| 14 | **AGTR1** | `P30556` | AGTR1_HUMAN | 1 | 359 | `6dae55828357a788` | — | 24 | 306-320 | 1–359 | 359 | `6dae55828357a788` | 291 |
| 15 | **APJ** | `P35414` | APJ_HUMAN | 1 | 380 | `7c44a5c602ed3747` | — | 29 | 313-327 | 1–380 | 380 | `7c44a5c602ed3747` | 288 |
| 16 | **B1B1U5** | `B1B1U5` | B1B1U5_9ARAC | 1 | 372 | `ba8fa863e837d8a9` | — | 46 | 335-346 | 1–372 | 372 | `ba8fa863e837d8a9` | 306 |
| 17 | **C5AR1** | `P21730` | C5AR1_HUMAN | 2 | 350 | `dc48c194272465c0` | — | 34 | 305-314 | 1–350 | 350 | `dc48c194272465c0` | 273 |
| 18 | **CCKAR** | `P32238` | CCKAR_HUMAN | 1 | 428 | `db51d7d7e7d75f30` | — | 39 | 374-390 | 1–428 | 428 | `db51d7d7e7d75f30` | 277 |
| 19 | **CCR2** | `P41597` | CCR2_HUMAN | 1 | 374 | `7a8225f899d150ae` | — | 37 | 309-320 | 1–374 | 374 | `7a8225f899d150ae` | 260 |
| 20 | **CCR5** | `P51681` | CCR5_HUMAN | 1 | 352 | `7474668859b42bd1` | — | 22 | 301-313 | 1–352 | 352 | `7474668859b42bd1` | 298 |
| 21 | **CCR6** | `P51684` | CCR6_HUMAN | 2 | 374 | `b706a0519a8fe544` | — | 39 | 320-335 | 1–374 | 374 | `b706a0519a8fe544` | 262 |
| 22 | **CCR8** | `P51685` | CCR8_HUMAN | 1 | 355 | `5cd8cb49bc5ec707` | — | 31 | 304-317 | 1–355 | 355 | `5cd8cb49bc5ec707` | 266 |
| 23 | **CNR1** | `P21554` | CNR1_HUMAN | 1 | 472 | `4cf523e4f20641bd` | — | 112 | 401-413 | 62–472 | 411 | `ec6475daeb38ed8e` | 270 |
| 24 | **CNR2** | `P34972` | CNR2_HUMAN | 1 | 360 | `c497f29417b886ff` | — | 29 | 303-319 | 1–360 | 360 | `c497f29417b886ff` | 271 |
| 25 | **CXCR2** | `P25025` | CXCR2_HUMAN | 2 | 360 | `613b62553ee1c016` | — | 45 | 318-332 | 1–360 | 360 | `613b62553ee1c016` | 265 |
| 26 | **CXCR3** | `P49682` | CXCR3_HUMAN | 2 | 368 | `82869dc8d22e9b15` | — | 45 | 322-336 | 1–368 | 368 | `82869dc8d22e9b15` | 257 |
| 27 | **CXCR4** | `P61073` | CXCR4_HUMAN | 1 | 352 | `745dbb36c0968245` | — | 30 | 306-318 | 1–352 | 352 | `745dbb36c0968245` | 265 |
| 28 | **DRD2** | `P14416` | DRD2_HUMAN | 2 | 443 | `8c2b6e1477ff2109` | — | 31 | 430-442 | 1–443 | 443 | `8c2b6e1477ff2109` | 261 |
| 29 | **DRD3** | `P35462` | DRD3_HUMAN | 3 | 400 | `0c28b2bbcd26288e` | — | 26 | 387-399 | 1–400 | 400 | `0c28b2bbcd26288e` | 270 |
| 30 | **DRD4** | `P21917` | DRD4_HUMAN | 3 | 419 | `9a2657fa53c20731` | — | 31 | 404-416 | 1–419 | 419 | `9a2657fa53c20731` | 261 |
| 31 | **EDNRA** | `P25101` | EDNRA_HUMAN | 1 | 427 | `0e420a3caffe9e2f` | 1-20 | 70 | 373-386 | 20–427 | 408 | `5e45c783896dc44d` | 283 |
| 32 | **EDNRB** | `P24530` | EDNRB_HUMAN | 1 | 442 | `f203a5007cc0cf30` | 1-26 | 91 | 390-403 | 41–442 | 402 | `f8dd6d741c229fcb` | 301 |
| 33 | **FSHR** | `P23945` | FSHR_HUMAN | 4 | 695 | `7bbe9f46e81ee1d0` | 1-17 | 362 | 630-645 | 312–695 | 384 | `3afa338eef74ceed` | 568 |
| 34 | **GHSR** | `Q92847` | GHSR_HUMAN | 1 | 366 | `73fe68d1fe5d48b8` | — | 39 | 327-342 | 1–366 | 366 | `73fe68d1fe5d48b8` | 282 |
| 35 | **GPR52** | `Q9Y2T5` | GPR52_HUMAN | 2 | 361 | `dac50f0a84d7dc8a` | — | 40 | 321-341 | 1–361 | 361 | `dac50f0a84d7dc8a` | 267 |
| 36 | **GPR6** | `P46095` | GPR6_HUMAN | 1 | 362 | `b453663681613982` | — | 71 | 333-345 | 21–362 | 342 | `1c75b0e3f1404911` | 256 |
| 37 | **GRPR** | `P30550` | GRPR_HUMAN | 1 | 384 | `65221c4df869b796` | — | 37 | 326-339 | 1–384 | 384 | `65221c4df869b796` | 274 |
| 38 | **HRH1** | `P35367` | HRH1_HUMAN | 1 | 487 | `9112bbed27c42f31` | — | 29 | 472-484 | 1–487 | 487 | `9112bbed27c42f31` | 260 |
| 39 | **HRH2** | `P25021` | HRH2_HUMAN | 1 | 359 | `4388134c63cdaa3d` | — | 10 | 292-304 | 1–359 | 359 | `4388134c63cdaa3d` | 227 |
| 40 | **HRH3** | `Q9Y5N1` | HRH3_HUMAN | 2 | 445 | `d9bd4f76c847dbfb` | — | 36 | 416-428 | 1–445 | 445 | `d9bd4f76c847dbfb` | 284 |
| 41 | **LPAR1** | `Q92633` | LPAR1_HUMAN | 3 | 364 | `932606a6305d90f0` | — | 47 | 315-327 | 1–364 | 364 | `932606a6305d90f0` | 283 |
| 42 | **LSHR** | `P22888` | LSHR_HUMAN | 4 | 699 | `8ab4a7858bf09b30` | 1-26 | 359 | 627-641 | 309–699 | 391 | `f9081bb521770728` | 555 |
| 43 | **LT4R1** | `Q15722` | LT4R1_HUMAN | 2 | 352 | `44b3d3a6c920fab6` | — | 13 | NA | 1–352 | 352 | `44b3d3a6c920fab6` | 198 |
| 44 | **MCHR1** | `Q99705` | MCHR1_HUMAN | 3 | 353 | `9f42fc1aa2a3da79` | — | 106 | 384-396 | 56–353 | 298 | `e7b3bfb6bb00ebfc` | 270 |
| 45 | **MTR1A** | `P48039` | MTR1A_HUMAN | 1 | 350 | `61065c51ec32c120` | — | 23 | 299-315 | 1–350 | 350 | `61065c51ec32c120` | 276 |
| 46 | **MTR1B** | `P49286` | MTR1B_HUMAN | 1 | 362 | `994582d1d50e1dfe` | — | 38 | 312-328 | 1–362 | 362 | `994582d1d50e1dfe` | 269 |
| 47 | **NK1R** | `P25103` | NK1R_HUMAN | 1 | 407 | `c1c101b738eca478` | — | 28 | 309-320 | 1–407 | 407 | `c1c101b738eca478` | 279 |
| 48 | **NPY1R** | `P25929` | NPY1R_HUMAN | 1 | 384 | `b988033ce3865dd5` | — | 36 | 324-335 | 1–384 | 384 | `b988033ce3865dd5` | 295 |
| 49 | **NPY2R** | `P49146` | NPY2R_HUMAN | 1 | 381 | `5405ec4c579e6859` | — | 48 | 329-345 | 1–381 | 381 | `5405ec4c579e6859` | 286 |
| 50 | **NTR1** | `P30989` | NTR1_HUMAN | 2 | 418 | `0b4854a718c53840` | — | 59 | 368-383 | 9–418 | 410 | `5a17a95b86f7a269` | 251 |
| 51 | **OPRD** | `P41143` | OPRD_HUMAN | 4 | 372 | `b75060695513d21a` | — | 39 | 322-335 | 1–372 | 372 | `b75060695513d21a` | 289 |
| 52 | **OPRK** | `P41145` | OPRK_HUMAN | 2 | 380 | `945340616bafd8d3` | — | 57 | 334-346 | 7–380 | 374 | `ebe4f6df631e95cc` | 268 |
| 53 | **OPRM** | `P42866` | OPRM_MOUSE | 1 | 398 | `a3da4c29ab3b06e2` | — | 65 | 340-352 | 15–398 | 384 | `ffdc6938597e97e5` | 281 |
| 54 | **OPRX** | `P41146` | OPRX_HUMAN | 1 | 370 | `34c69b7a4be8168c` | — | 48 | 323-335 | 1–370 | 370 | `34c69b7a4be8168c` | 277 |
| 55 | **OPSD** | `P02699` | OPSD_BOVIN | 1 | 348 | `20e8fc797c8f2615` | — | 33 | 310-322 | 1–348 | 348 | `20e8fc797c8f2615` | 304 |
| 56 | **OX2R** | `O43614` | OX2R_HUMAN | 2 | 444 | `e6a80905b838e43a` | — | 53 | 368-384 | 3–444 | 442 | `d4fe73c09b89f6dd` | 276 |
| 57 | **OXYR** | `P30559` | OXYR_HUMAN | 2 | 389 | `944327688ddc36d8` | — | 35 | 333-349 | 1–389 | 389 | `944327688ddc36d8` | 247 |
| 58 | **PD2R2** | `Q9Y5Y4` | PD2R2_HUMAN | 3 | 395 | `9800e73d5db87c78` | — | 32 | 308-325 | 1–395 | 395 | `9800e73d5db87c78` | 301 |
| 59 | **PE2R4** | `P35408` | PE2R4_HUMAN | 1 | 488 | `0c3feb9a2e6d6c63` | — | 18 | 333-346 | 1–446 | 446 | `17adcec012def314` | 276 |
| 60 | **S1PR1** | `P21453` | S1PR1_HUMAN | 2 | 382 | `db9ec94c53b2528b` | — | 42 | 315-327 | 1–382 | 382 | `db9ec94c53b2528b` | 270 |
| 61 | **S1PR5** | `Q9H228` | S1PR5_HUMAN | 1 | 398 | `955064a6b00ad109` | — | 37 | 310-322 | 1–398 | 398 | `955064a6b00ad109` | 253 |
| 62 | **SSR2** | `P30874` | SSR2_HUMAN | 1 | 369 | `6001055d0866d9ee` | — | 40 | 316-328 | 1–369 | 369 | `6001055d0866d9ee` | 284 |
| 63 | **TA2R** | `P21731` | TA2R_HUMAN | 3 | 343 | `b21f1f7568d77ddb` | — | 27 | 312-331 | 1–343 | 343 | `b21f1f7568d77ddb` | 296 |
| 64 | **TSHR** | `P16473` | TSHR_HUMAN | 3 | 764 | `abb482de486eda31` | 1-20 | 414 | 682-696 | 364–764 | 401 | `dc09d883046387b0` | 555 |

## 2.1 The extension tiers

| slug | tier | class | accession | entry | SV | len | sha256[:16] | signal | TM1 | H8 | capped range | capped len | capped sha256[:16] |
|---|---|---|---|---|---:|---:|---|---|---:|---|---|---:|---|
| **ACM3** | X | A | `P20309` | ACM3_HUMAN | 1 | 590 | `f3a234965b33be05` | — | 64 | 548-561 | 14–590 | 577 | `9ef00ec3196fc091` |
| **AGRE5** | E-scope | B2 | `P48960` | AGRE5_HUMAN | 4 | 835 | `0136d98f553bd40c` | 1-20 | 541 | 790-806 | 491–835 | 345 | `861da8b5a84854d3` |
| **CALRL** | E-B1 | B1 | `Q16602` | CALRL_HUMAN | 3 | 461 | `0570c5d169e261bd` | 1-22 | 130 | 388-413 | 80–461 | 382 | `7b6f1987033db3a2` |
| **CRHR1** | E-B1 | B1 | `P34998` | CRHR1_HUMAN | 2 | 415 | `d606ec68b032c7d9` | 1-23 | 103 | 367-392 | 53–415 | 363 | `d8dc93ce675ad7ca` |
| **FZD4** | E-scope | F | `Q9ULV1` | FZD4_HUMAN | 2 | 537 | `c997d9577170e241` | 1-36 | 212 | 497-512 | 162–537 | 376 | `41023ca59e45ed81` |
| **FZD6** | E-scope | F | `O60353` | FZD6_HUMAN | 2 | 706 | `319dcaff69890876` | 1-18 | 191 | 496-512 | 141–612 | 472 | `3e4620ef51d50f94` |
| **FZD7** | E-scope | F | `O75084` | FZD7_HUMAN | 2 | 574 | `8ecc09d746ea0a01` | 1-32 | 245 | 550-566 | 195–574 | 380 | `adbeede8efc86a4a` |
| **GCGR** | E-B1 | B1 | `P47871` | GLR_HUMAN | 1 | 477 | `b236d1c797f666e4` | 1-25 | 131 | 404-429 | 81–477 | 397 | `0c0d2b1580a10a22` |
| **GLP1R** | E-B1 | B1 | `P43220` | GLP1R_HUMAN | 2 | 463 | `8cd3cf61857825c3` | 1-23 | 138 | 406-431 | 88–463 | 376 | `9e39e48473cb51b3` |
| **PTH1R** | E-B1 | B1 | `Q03431` | PTH1R_HUMAN | 1 | 593 | `db20616a415dae80` | 1-26 | 173 | 463-488 | 123–588 | 466 | `2d6fc43e163f83f2` |
| **SMO** | E-scope | F | `Q99835` | SMO_HUMAN | 1 | 787 | `2174c461817c3510` | 1-27 | 223 | 538-553 | 173–653 | 481 | `9e8b88c10f74385c` |

## 2.2 One check that can be run today, and its result

`data/block_b/03_msa_audit/msa_depth_report.md` is the only file in the project
that records the **length** of every receptor sequence the pipeline actually
dispatched — 48 of them, Block A and Block B. Compared against the canonical
records fetched here:

> **48 of 48 supplied lengths equal the UniProt canonical length exactly.**

So the pipeline's de facto convention has been full-length canonical, including
signal peptides and including the entire FSHR/LSHR ectodomain, and `SEQUENCES.md`
§8's rule describes what was already happening rather than proposing a change.

**That is a length check, not an identity check, and the distinction is the
point.** Equal length is compatible with a different isoform of the same length,
a polymorphism, or a wrong species. The file that would settle it —
`refs/panel_receptor_sequences.fasta` — has never shipped, and the drops carry no
receptor-chain hash (§0.1). The report itself records that this file holds **51**
entries for a 48-receptor panel, with **three receptors carrying two sequences
each**: an `ADRB1 G389R polymorphism` variant at 477 aa (the same length as
canonical P08588, so a length check cannot see it), and second-sequence variants
of `FSHR` (695 aa) and `MCHR1` (422 aa, against canonical 353). Which of the two
any row consumed is a hash question and the hash was never taken. **DATA ASK 1.**

---

# 3. The construct decision, per axis

## 3.1 Signal peptide — no convention exists, so this is a decision, not a lookup

The lit session's answer is that the corpus has no convention: one note of 81
mentions signal peptides and in the wrong context. So this file does not invent
one. What it can do is make the decision small and exact.

**Six of the 64 core receptors carry a signal-peptide annotation**, and the
evidence behind the six is not uniform:

| receptor | signal | UniProt evidence | mature chain |
|---|---|---|---|
| **5HT2C** | 1–32 | `ECO:0000269` — **experimental**, PubMed 22497996 | 33–458 |
| **EDNRA** | 1–20 | `ECO:0000255` — sequence-analysis prediction | 21–427 |
| **EDNRB** | 1–26 | `ECO:0000255` — prediction | 27–442 |
| **FSHR** | 1–17 | `ECO:0000255` — prediction | 18–695 |
| **LSHR** | 1–26 | `ECO:0000255` — prediction | 27–699 |
| **TSHR** | 1–20 | **no evidence code at all** | 21–764 |

Ten of the eleven extension receptors carry one too (every one except ACM3); for
Class B1 and Class F the signal peptide is upstream of a folded ECD/CRD and is a
different question from the Class A case.

**The three options, costed.**

| option | what it does | cost | risk |
|---|---|---|---|
| **(a) keep the full canonical chain** | supply 1–L | zero; it is what Blocks A–D did | a model is handed ~20–32 residues of hydrophobic leader that is not in the mature receptor and is in no reference structure. It is scored against nothing (§6) but it can occupy space, and on TSHR it precedes a 394-residue ectodomain |
| **(b) remove the annotated signal peptide** | supply `CHAIN` start–L, six core sequences change | one line; hashes in `seqrec_receptors.tsv:mature_sha256` are already computed | four of the six ranges are *predicted*, not observed. Removing a predicted boundary is a judgement dressed as data |
| **(c) let §4's terminal cap decide it as a side effect** | nothing extra | zero | **this is the worst option and the numbers say so** — see below |

**Why (c) fails.** Applying the `miglionico2026atlas` cap (§4) without a separate
signal-peptide rule produces, on the six:

| receptor | signal | cap starts at | signal residues left in the construct |
|---|---|---:|---|
| 5HT2C | 1–32 | 4 | **29 of 32** |
| EDNRA | 1–20 | 20 | **1 of 20** |
| EDNRB | 1–26 | 41 | 0 |
| FSHR | 1–17 | 312 | 0 |
| LSHR | 1–26 | 309 | 0 |
| TSHR | 1–20 | 364 | 0 |

Four are cleanly removed and two are left as *fragments* — a 29-residue stump of
a signal peptide, and a single residue of one. A fragment of a signal peptide is
neither the leader nor its absence; it is an artefact of an unrelated rule.

**Recommendation, and it is a recommendation and not a decision:** adopt **(b)**,
applied *before* the cap, and only where UniProt annotates a `CHAIN` start. It is
mechanical, it is recorded per receptor, it touches six core sequences, and it
removes the fragment case. The argument against it — that four of the six
boundaries are predicted — is real, and is why the choice belongs to the PI. If
(a) is preferred instead, that is defensible too and continues Blocks A–D; what
is not defensible is (c).

**Either way, record `signal_peptide_removed ∈ {true,false}` per row.** No block
has ever carried it and the question cannot be answered afterwards from a length.

## 3.2 Isoform — one receptor needs naming, and it is not the one expected

**29 of the 64 core entries have more than one UniProt isoform.** For 28 of them
the displayed (canonical) isoform is `-1` and there is nothing to decide. One is
different:

- **TA2R (thromboxane A2 receptor, P21731)** — UniProt's *displayed* isoform is
  **`P21731-3`**, 343 aa, not `-1`. This is the TPα/TPβ C-terminal splice pair,
  and the canonical record is the short one. The rule-R active reference `8XJN`
  maps cleanly onto canonical residues 1–331, so the deposited construct is the
  displayed isoform and no substitution is needed — but the isoform ID must be
  written down, because "the canonical sequence of P21731" is ambiguous in a way
  no other panel entry is.

Two further isoform facts, recorded so they are not rediscovered as surprises:

- **OPRM (mouse, P42866) has 19 annotated isoforms** — the MOR-1 splice family.
  The displayed isoform is `P42866-1` at 398 aa and the rule-R references
  (`5C1M` / `7UL4`) map onto it, so the choice is settled by the references. It
  is nonetheless the largest isoform fan-out on the panel and the single entry
  most likely to be quoted wrongly.
- **DRD2 (P14416)** is the classic D2L/D2S case and it resolves cleanly: the
  displayed isoform is D2L at 443 aa, and the active reference `8TZQ` maps
  **all 443** canonical residues, so the deposited construct contains the
  29-residue alternative exon. D2L is right. Nothing to decide.

Others worth a column but not a decision: ADA1A 9 isoforms, HRH3 7, EDNRA 5,
FSHR 4, TSHR / CNR1 / CXCR3 / DRD2 3 each.

## 3.3 C-terminal tail — the cap barely touches it, and helix 8 is the reason

The intuition behind truncating the C-tail is that deposited structures almost
never resolve it. Measured rather than assumed, that intuition is **mostly right
and wrong in an instructive place.**

Across the 64 core receptors the median C-terminal tail after TM7 is **54
residues** and there are 3,644 post-TM7 residues in total. Of those, **705 are
resolved in both rule-R references** — a median of **12 per receptor**, and only
**two** core receptors resolve none at all. So 81% of the tail is never scored
and the first ~12 residues of it almost always are: that is **helix 8**, which
packs against the membrane and is ordered.

This is the empirical argument for `miglionico2026atlas` anchoring its C-terminal
cap on **H8 rather than on TM7**, and it is why §4.1 goes to GPCRdb for an H8
boundary UniProt does not annotate. A rule anchored on TM7 + 100 would place the
boundary ~12 residues too early on a typical receptor and would cut into the one
post-TM7 element the references actually contain.

What the cap then does to the C-terminus is almost nothing: it reaches only
**two** of the 64 — PE2R4 (−42) and ADA1A (−24). Every other core receptor's
tail is already shorter than H8 end + 100. So on Class A the C-terminal decision
is not a construct decision at all. The distal tail is supplied, is absent or
unresolved in the references, and costs compute and sequence context rather than
correctness; **`LT4R1`, the one receptor with no GPCRdb H8, is the only place
where the fallback anchor could bite** (§4.1).

## 3.4 N-terminus — this is where the real variation lives

Median N-terminal length before TM1 across the core is **40 residues**, but the
distribution has a long tail and the tail is the whole story:

| receptor | canonical len | residues before TM1 | what they are |
|---|---:|---:|---|
| **TSHR** | 764 | 414 | LRR ectodomain + hinge |
| **FSHR** | 695 | 366 | LRR ectodomain + hinge |
| **LSHR** | 699 | 363 | LRR ectodomain + hinge |
| CNR1 | 472 | 116 | disordered N-term |
| EDNRB | 442 | 101 | signal + N-term |
| 5HT2A / EDNRA | 471 / 427 | 80 / 80 | N-term |
| GPR6 | 362 | 74 | N-term |
| NTR1 | 418 | 67 | N-term |
| OPRM | 398 | 66 | N-term |

Three of the 64 carry a folded, disulfide-bonded, hormone-binding domain of
300+ residues. Everything else carries between 7 and 116 residues of mostly
disordered terminus. §4 is how that is handled.

---

# 4. The construct rule: the `miglionico2026atlas` terminal cap

Adopted on the lit session's relay, verbatim from `miglionico2026atlas` p.19:

> *"N-termini were truncated to a maximum of 50 residues upstream of TM1, and
> C-termini to 100 residues downstream of helix H8, to reduce terminal
> disorder."*

Three reasons this is the right rule for this panel, in the order that matters:

1. **It is a cap, not a boundary.** A receptor whose N-terminus is already
   shorter than 50 residues upstream of TM1 is returned unchanged. That is why
   it needs no per-receptor special case, which is exactly the property the two
   alternatives lack — `zhang2026generalization` p.5 supplies full-length
   untrimmed UniProt (no rule at all), and `pandyszekeres2024gproteindb` p.3
   deletes long segments and retains Class A ICL3 at 14 residues "to avoid
   cross-chain clashes", which is a *different* kind of edit in a *different*
   place and is not a terminal rule.
2. **It is AF3-lineage and it is numeric.** 10,413 predictions behind it, and a
   stated reason.
3. **On this panel it is almost inert, and where it is not, it is loud.** See
   §4.1.

## 4.1 What the cap actually does to the core 64

`seqrec_trim.py` applies it. **The cap changes 16 of 64 core receptors and leaves
48 untouched**, removing 1,294 residues in total:

| receptor | canon | TM1 | H8 | capped range | removed N | removed C | % |
|---|---:|---:|---|---|---:|---:|---:|
| **TSHR** | 764 | 414 | 682–696 | 364–764 | **363** | 0 | 47.5 |
| **FSHR** | 695 | 362 | 630–645 | 312–695 | **311** | 0 | 44.7 |
| **LSHR** | 699 | 359 | 627–641 | 309–699 | **308** | 0 | 44.1 |
| MCHR1 | 353 | 106 | 384–396 | 56–353 | 55 | 0 | 15.6 |
| CNR1 | 472 | 112 | 401–413 | 62–472 | 61 | 0 | 12.9 |
| EDNRB | 442 | 91 | 390–403 | 41–442 | 40 | 0 | 9.0 |
| PE2R4 | 488 | 18 | 333–346 | 1–446 | 0 | 42 | 8.6 |
| GPR6 | 362 | 71 | 333–345 | 21–362 | 20 | 0 | 5.5 |
| ADA1A | 466 | 20 | 330–342 | 1–442 | 0 | 24 | 5.2 |
| EDNRA | 427 | 70 | 373–386 | 20–427 | 19 | 0 | 4.4 |
| 5HT2A | 471 | 69 | 384–397 | 19–471 | 18 | 0 | 3.8 |
| OPRM | 398 | 65 | 340–352 | 15–398 | 14 | 0 | 3.5 |
| NTR1 | 418 | 59 | 368–383 | 9–418 | 8 | 0 | 1.9 |
| OPRK | 380 | 57 | 334–346 | 7–380 | 6 | 0 | 1.6 |
| 5HT2C | 458 | 54 | 372–385 | 4–458 | 3 | 0 | 0.7 |
| OX2R | 444 | 53 | 368–384 | 3–444 | 2 | 0 | 0.5 |

Twelve of the sixteen lose fewer than 62 residues of disordered terminus. Three
lose an entire folded domain. One — MCHR1 — sits between and is discussed in §4.3.

**Two conventions inside the rule that had to be chosen, and were.**

- **H8 comes from GPCRdb, because UniProt does not annotate H8 at all.** The rule
  names helix H8; UniProt's feature table has seven `Transmembrane` features and
  no H8. GPCRdb's generic-numbering residue service
  (`https://gpcrdb.org/services/residues/{entry_name}/`, fetched 2026-09-11)
  does — the same service and the same convention `seq_build.py` used to make the
  Gα α5 boundaries exact. **`LT4R1` is the one panel receptor with no GPCRdb H8
  segment**; its C cap falls back to TM7 end + 100 and the row is flagged rather
  than guessed.
- **TM1 also comes from GPCRdb, for coherence, and the two authorities disagree
  on every single receptor.** UniProt and GPCRdb give different TM1 start
  positions on **75 of 75** panel entries, GPCRdb always earlier, by 2 to 12
  residues (e.g. AA2AR: UniProt 8, GPCRdb 1; 5HT2A: UniProt 81, GPCRdb 69).
  Mixing a UniProt TM1 with a GPCRdb H8 would apply the rule in two frames at
  once. Both columns are in `seqrec_trim.tsv` so the choice is auditable and
  reversible; choosing UniProt instead would shift 16 N-terminal boundaries by
  2–12 residues and change nothing else.

## 4.2 Class B1 — the cap and the "keep the ECD" instruction collide, and the ECD wins

The lit session's instruction is to keep the Class B1 ECD, on a mechanistic
argument rather than a conventional one: `hilger2020gcgr` p.1 reports that
glucagon *"induces conformational change on the extracellular side (ECD, TM1,
TM2, TM6, and TM7) **without inducing outward movement of TM6 on the
intracellular side**"*. The ECD is decoupled from the TM6 displacement our
predicate reads — so deleting it changes nothing we measure while destroying the
only place a B1 ligand effect could show up.

**The cap, applied naively, deletes most of it.** Measured against UniProt's own
first extracellular topological domain:

| receptor | ECD (UniProt topo dom) | ECD len | cap starts | ECD residues removed |
|---|---|---:|---:|---|
| PTH1R | 27–186 | 160 | 123 | **96 (60%)** |
| GLP1R | 24–139 | 116 | 88 | **64 (55%)** |
| GCGR | 26–136 | 111 | 81 | **55 (50%)** |
| CALRL | 23–139 | 117 | 80 | **57 (49%)** |
| CRHR1 | 24–113 | 90 | 53 | **29 (32%)** |

**Rule, stated as an exception rather than smuggled in:** the
`miglionico2026atlas` N-cap is applied to Class A only. For `E-B1` the
N-terminus is supplied from the mature chain start (or residue 1, per §3.1) to
the C-terminal cap. The exception is recorded on the row as
`nterm_rule ∈ {miglionico_cap, full_ecd}`, not left to be inferred from a
length.

The same argument extends by analogy — and only by analogy, which is why it is
flagged rather than asserted — to `E-scope`: the cap removes 67–88% of the
Frizzled CRD and of AGRE5's GAIN domain. **UNRESOLVED-2.** Those five receptors
are declared instrument scope with no claim attached, so nothing depends on the
answer today; if a claim is ever attached, the decision has to be made first.

## 4.3 FSHR, LSHR and TSHR — the decision that is the PI's

This is the case the coordinator flagged and it is the only place where the cap
amputates a domain by side effect rather than by intent. The numbers make it a
costed choice rather than an opinion.

**What the cap removes:** 84% of the FSHR ectodomain (294 of 349 residues), 84%
of LSHR's (282 of 337), 87% of TSHR's (343 of 394). These are leucine-rich-repeat
hormone-binding domains, not disordered termini.

**And unlike every other receptor on the panel, those residues are resolved in
the reference structures.** §6 computes, per receptor, the canonical residues
resolved in *both* rule-R references — the set on which an RMSD can actually be
taken. Intersecting that set with the capped window:

> **The cap removes 794 scoreable residues across the whole core. 776 of them are
> at FSHR, LSHR and TSHR** (268, 248, 260). **Of the other 61 core receptors, 60
> lose exactly zero and MCHR1 loses 18.**

So for 60 of 64 receptors the cap is free by construction: it removes only
residues the references do not resolve and against which nothing could have been
scored. For three receptors it deletes half the scoreable molecule.

**The three options, costed.**

| option | chain A for FSHR/LSHR/TSHR | compute | what it buys | what it costs |
|---|---|---|---|---|
| **(a) apply the cap** | 384 / 391 / 401 aa | **cheapest** — ~45% shorter chain on three receptors, and MSA/inference cost is superlinear in length | uniformity: one rule, 64 receptors, no exception to defend | 776 scoreable residues; the hormone-binding domain; any possibility of a B1-style extracellular result on the three GpHRs; comparability with every published GpHR structure |
| **(b) exempt the three, as for Class B1** | 695 / 699 / 764 aa (or mature-chain start) | most expensive three chains on the panel | the full molecule; consistency with the §4.2 exception, which rests on the same physical argument (a folded, ligand-binding extracellular domain) | a second exception, and three chains twice the length of the panel median |
| **(c) supply the ectodomain but score only the 7TM core** | full length in, restricted residue set out | same as (b) | separates the supply question from the scoring question, which §0.4 says are different anyway | does not reduce compute at all; needs the scoring mask specified, which §6.3 does |

**This file does not choose.** The recommendation, for what it is worth, is (b)
or (c) over (a): the argument that justifies keeping the Class B1 ECD —
`hilger2020gcgr`'s decoupling of the ECD from intracellular TM6 — applies with at
least equal force to a 349-residue LRR domain that the references actually
resolve, and an exception already exists for exactly this shape of domain. But
the compute difference is real and it is the PI's to weigh. **Do not let the cap
decide this silently.**

**MCHR1 is the fourth case and it is smaller but not zero.** The cap starts at 56;
the references resolve from 38. Eighteen scoreable residues are lost. Options:
apply the cap and accept an 18-residue reduction in the scoring set, or start
MCHR1 at 38. Recommendation: apply the cap, record the loss — the alternative is
a per-receptor override, which is exactly what a cap rule exists to avoid. Noted
so it is a decision rather than an oversight.

---

# 5. Non-human entries

`panel_systems.csv` flags three of the 64 core receptors as non-human. Each was
verified against a fetched record and each resolves differently.

## 5.1 ADRB1 — the brief is right about ConfoRNets and wrong about this panel

The brief says "ConfoRNets' ADRB1 is turkey". It is: `panel_systems.csv` records
ConfoRNets' pair as `8DCS` / `4BVN`, both *Meleagris gallopavo*.

**But this panel's ADRB1 is human and so are its references.** `uniprot_acc` is
**`P08588` (ADRB1_HUMAN, SV 2, 477 aa)**, and rule R selects `7BU7` / `7BVQ`,
both *Homo sapiens*, both mapping onto canonical residues 54–399. GPCRdb carries
both `adrb1_human` and `adrb1_melga` under the same slug, which is why 66
both-state Class A entries collapse to 64 (`PANEL.md` §1), and rule R step 1
prefers human where a human both-state entry exists. **No action. Supply human
P08588.**

The consequence that does need recording is a comparability one, not a construct
one: **on ADRB1 our references and ConfoRNets' are different species**, so an
ADRB1 number of ours is not directly comparable with theirs. That belongs to
`PANEL.md`, and is noted here only because it is the kind of thing that gets
attributed to a sequence decision after the fact.

## 5.2 OPSD — bovine, and the substitution is available but not obviously right

Panel entry is **P02699 (OPSD_BOVIN, SV 1, 348 aa)**; references `4X1H` / `7ZBC`
are both *Bos taurus*. The human orthologue **P08100 (OPSD_HUMAN, 348 aa)** was
fetched for comparison: the two are the same length and differ at **23 positions
(93.4% identical)** — `A16K Y26A V49M L88F S93T A173V L183M L194P K195H P196E
V198T T213I M216L I218V V266L S270G N282D S297T A298S I300V L318V I321L A335T`.

Substituting human rhodopsin would break the receptor–reference species match,
which rule R step 1 exists to prevent, and would do so for a 23-residue gain in
species tidiness. **Recommendation: keep bovine P02699, record
`receptor_species = Bos taurus`.** Note the asymmetry this creates with the
partner side: `SEQUENCES.md` §3.3(b) shows the Gα rungs are species-invariant for
OPSD through `a5plus`, so the *partner* needs no decision and the *receptor* is
already consistent with its references.

## 5.3 OPRM — mouse, and the same answer for the same reason

Panel entry is **P42866 (OPRM_MOUSE, SV 1, 398 aa)**; rule-R references
`5C1M` / `7UL4` are both *Mus musculus*. The human orthologue **P35372
(OPRM_HUMAN, 400 aa)** differs at 11 positions over the 359 residues that align
unambiguously (`D51G R55S D56H P61Q I68V T139N I189V V308I N359T T366A D374E`),
plus a short terminal length difference. **Keep mouse P42866**; swapping would
create the cross-species receptor/reference pair rule R was written to avoid.

## 5.4 B1B1U5 — the spider opsin, and the problem is the partner, not chain A

**B1B1U5 (`B1B1U5_9ARAC`, "Kumopsin1", *Hasarius adansoni*, 372 aa)**. Its
references `9EPP` / `6I9K` are the same species, so **chain A is internally
consistent and needs no decision**. Chain A is not where this receptor is broken.

`SEQUENCES.md` §10(1) already records the real problem — Block B assigned it
human GNAI1 as "cognate", and invertebrate visual opsins are the canonical
Gq-coupled opsins. That is a partner decision and a PANEL decision; it is
repeated here only so that "B1B1U5 resolved on the receptor side" is not read as
"B1B1U5 resolved".

One small inconsistency found while checking, and it belongs to PANEL: for
B1B1U5 `panel_systems.csv:gdb_active` is **`9EPP`**, while `PANEL.md`'s Rule R
step 4 (the partner-chain override, which exists specifically for this receptor)
selects **`9EPR`**. The column appears to be the pre-override pick. Not resolved
here — flagged for the panel owner. The §6 numbers for B1B1U5 use the column, i.e.
`9EPP`.

---

# 6. What the deposited references actually contain

This is the question the task frames as: *if we supply the full canonical
sequence and score against a reference that is a fusion construct, the RMSD
includes residues the reference does not have.*

## 6.1 Method, and why RCSB's own alignment was not used

`seqrec_refs.py` fetches the receptor polymer entity of all 128 rule-R
references (`gdb_active` / `gdb_inactive` for the 64 core) and maps the deposited
one-letter sequence onto the canonical UniProt sequence by unique 9-mer anchors,
chained by longest-increasing-subsequence and merged into collinear diagonal
blocks. The receptor entity of an entry is then whichever entity maps the most
canonical residues — self-validating, no matching on descriptions.

`rcsb_polymer_entity_align` looks like the right source and is not reliable here.
**On three of the 128 references RCSB's alignment does not name the receptor at
all**: `9D3G` (CCR6) and `8IRU` (DRD4) carry no UniProt alignment on the receptor
entity, and `8HCQ` (EDNRA) aligns its receptor entity only to `Q9GV45`, the
luciferase fusion partner. A first run of this script used RCSB's alignment and
returned **zero** mapped residues for CCR6, DRD4 and EDNRA — which is how those
three were found. It is used as a cross-check now and nothing more. This is also
the method `PANEL.md` §9(2) already names as the one that works.

The mapper is proved by planting each defect it must catch
(`seqrec_refs.py --selftest`): an identity map, a single point mutation, a
160-residue fusion plus an ICL3 excision, and a *length-matched* 15-residue
graft. The last of those is not hypothetical — see §6.4.

## 6.2 What is scoreable

| quantity | median | min | max |
|---|---:|---|---|
| canonical residues **present** in both references | 305 | 208 (LT4R1) | 693 (TSHR) |
| canonical residues **resolved** in both references | **273** | **198 (LT4R1)** | **568 (FSHR)** |
| fraction of the canonical chain that is scoreable | **0.70** | 0.49 (ADRB2) | 0.87 (OPSD) |

So on a typical core receptor, **roughly 30% of the supplied chain can never be
scored against either reference**, because it is absent from the construct or
unresolved in the density. The full per-receptor residue set is in
`seqrec_scoreable.tsv:resolved_both_ranges` as an explicit range string, not a
span — a span would over-count every internal gap, and ICL3 is an internal gap on
most of this panel.

## 6.3 Does the existing pipeline already solve this? Yes — and the column proves it

`data/block_b/01_rows/rows_tidy.csv` carries `rmsd_n_residues_used` on all 32,000
rows, described in `data/block_b/DATA_DICTIONARY.md:87-90` as **"7TM-only Cα RMSD
to closest active/inactive reference"** plus a residue count. Recomputed here:

- **exactly one distinct value per receptor**, invariant across all four arms and
  all seeds — so the residue set is determined by the reference pair, not by the
  prediction;
- values run **210 to 245, median 224**, on the Block B 40, whose canonical
  lengths run 326 (AA1R) to 699 (LSHR);
- **eight receptors carry a blank** with `rmsd_note = no_ref_pair_for_<slug>`
  (ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R) — 6,400 of the 32,000 rows.

**The answer to the task's question is therefore: yes, the pipeline already
restricts scoring to a per-receptor common set, and supplying residues the
reference lacks does not contaminate the RMSD.** Two caveats, and they are why
this is not simply a pass:

1. **The two numbers are not the same object and must not be compared as if they
   were.** `rmsd_n_residues_used` is a *7TM-only* set (~224 median); §6.2's number
   is the whole-chain resolved intersection (~273 median). The 7TM restriction is
   a further, tighter mask on top of the intersection. They agree in direction and
   are not interchangeable.
2. **The Block B column was computed against a different reference pair** —
   Block B used the pinned `our_active`/`our_inactive` set, this file uses rule R.
   For 31 of the 128 rule-R references there is no measurement in the pinned set
   at all (`PANEL.md` §9). So the per-receptor counts will change under rule R and
   must be recomputed, not carried over.

**What the redo must therefore record per row:** `rmsd_n_residues_used`,
`rmsd_residue_set_sha256` (a hash of the sorted canonical residue numbers used),
and `rmsd_mask ∈ {7TM_only, resolved_both, ...}`. A residue count without the set
behind it cannot be checked, and Block B's count cannot be reproduced today
because the set was never emitted. **DATA ASK 2.**

## 6.4 The reference constructs, recounted

RCSB's `pdbx_mutation` is the only machine-readable substitution record and
`methods.tex:303` already demonstrates it is empty for ten of fifteen verified
mutants. Recounted here by aligning every deposited receptor entity to canonical:

> **RCSB's floor over the 128 rule-R references is 76 substitutions. The
> sequence-level recount is 166 — and on 41 of the 128 references the recount
> exceeds RCSB's record.**

That closes the `free*` job `PANEL.md` §9(2) names as the prerequisite for
trusting rule R's step 3(a) ranking. Worst offenders: `6ME2` (MTR1A, 9,
RCSB records 0), `6PT2` (OPRD, 9, records 0), `6S0L` (AA2AR, 8, records 0),
`6ME6` (MTR1B, 8), `9D3G` (CCR6, 7), `6TPK` (OXYR, 7). Sixty-nine of the 128
references carry no substitution at all.

**Two references carry a foreign segment rather than substitutions, and telling
those apart mattered.** The first run of the recount reported SSR2's active
reference `7T10` as carrying *13 point mutations* at canonical 238–252. It does
not. RCSB's own alignment shows entity 40–276 → P30874 1–237, entity 292–408 →
P30874 253–369, and entity **277–291 → P41145 (OPRK) 256–270** — a 15-residue
κ-opioid ICL3 graft, length-matched and therefore on the same diagonal, which is
why a naive bridge mapped it as mutations of SSR2. The mapper now separates
isolated mismatches (substitutions) from runs (grafts), and the two references
with a graft are `7T10` (SSR2, 13 residues at 238–252) and `8IY5` (EDNRB, 8
residues at 58–65). This was my error before it was anyone else's data problem,
and the self-test now plants exactly that case.

## 6.5 The ICL3 fusion audit — 40 of 64 inactive references are affected

The coordinator's relay: `georgiou2025heterogeneity` pp.9,16 reports that T4
lysozyme fused into ICL3 of β2AR *"causes the population of only active TM6
conformations independent of the efficacy of bound ligands"*, and flags A2AR
`3PWH` as a possible artefactual broken ionic lock. `lee2026confornets` p.15
removes *"ICL3 and any fusion proteins inserted"* from inactive structures
without saying why.

`panel_systems.csv` carries a boolean `fusion_in_receptor_entity`. A boolean is
not enough: an N-terminal BRIL and an ICL3 T4L are different objects and only the
second is implicated. `seqrec_icl3_audit.py` classifies **where** the insertion
sits: ICL3 is UniProt's TM5-end to TM6-start interval widened by 5 residues at
each end, and an insertion counts if it is at least 20 residues. The ±5 is not
slack for its own sake — with a ±1 window three real ICL3 fusions were filed as
"other-internal" (`9D3G`, a 127-residue BRIL spliced 4 residues before the
annotated ICL3; `7UL3` at −4; `7UL2` at −5), because UniProt's TM5 end is a
helix-boundary annotation and not a splice site. The self-test plants both the
−4 case and a −40 case, so the widening is bounded rather than open.

> **43 of the 128 rule-R references carry a ≥20-residue insertion inside ICL3:
> 3 active and 40 inactive.**

That is a 13:1 asymmetry on the axis the predicate reads, pointing the wrong way
for the inactive class — **40 of the 64 inactive references and 3 of the 64
active ones**. Distribution of the remaining 85: 17 carry an N-terminal fusion
only, 8 a C-terminal only, 11 both termini, and **49 carry no insertion of 20
residues or more anywhere**.

| receptor | state | PDB | insert after (canon) | aa | fusion named by depositor |
|---|---|---|---:|---:|---|
| **ADA1A** | active | `7YM8` | 222 | 117 | **not named** |
| **AGTR1** | active | `6OS2` | 226 | 99 | BRIL |
| **DRD4** | active | `8IRU` | 283 | 59 | **not named** |
| **5HT1B** | inactive | `5V54` | 239 | 105 | **not named** |
| **5HT2A** | inactive | `7WC7` | 265 | 86 | BRIL |
| **5HT2C** | inactive | `6BQH` | 245 | 106 | BRIL |
| **AA1R** | inactive | `5UEN` | 211 | 114 | BRIL |
| **AA2AR** | inactive | `6S0L` | 201 | 113 | **not named** |
| **ACM1** | inactive | `6WJC` | 218 | 160 | T4L |
| **ACM2** | inactive | `5ZK8` | 217 | 106 | BRIL |
| **ACM4** | inactive | `5DSG` | 226 | 117 | T4L |
| **ADA2A** | inactive | `6KUX` | 242 | 106 | **not named** |
| **AGTR1** | inactive | `8TH3` | 226 | 115 | BRIL |
| **APJ** | inactive | `5VBL` | 229 | 54 | rubredoxin |
| **CCKAR** | inactive | `7F8U` | 240 | 160 | T4L |
| **CCR2** | inactive | `6GPX` | 231 | 61 | rubredoxin |
| **CCR6** | inactive | `9D3G` | 235 | 127 | BRIL |
| **CNR1** | inactive | `9BA0` | 301 | 204 | PGS |
| **CNR2** | inactive | `5ZTY` | 222 | 168 | T4L |
| **CXCR2** | inactive | `6LFL` | 241 | 202 | PGS |
| **CXCR3** | inactive | `8K2W` | 240 | 22 | BRIL |
| **DRD2** | inactive | `6CM4` | 222 | 160 | T4L |
| **DRD3** | inactive | `3PBL` | 221 | 160 | T4L |
| **DRD4** | inactive | `5WIU` | 228 | 105 | BRIL |
| **EDNRA** | inactive | `8XVK` | 281 | 117 | BRIL, endoglucanase |
| **EDNRB** | inactive | `5GLI` | 303 | 117 | **not named** |
| **GPR52** | inactive | `6LI2` | 235 | 56 | rubredoxin |
| **GPR6** | inactive | `8T1V` | 256 | 107 | BRIL |
| **GRPR** | inactive | `7W41` | 241 | 202 | PGS |
| **HRH1** | inactive | `8X5Y` | 217 | 106 | BRIL |
| **HRH2** | inactive | `7UL3` | 199 | 41 | **not named** |
| **LPAR1** | inactive | `4Z36` | 232 | 101 | BRIL |
| **MCHR1** | inactive | `8YNS` | 235 | 104 | BRIL |
| **MTR1A** | inactive | `6ME2` | 218 | 196 | PGS |
| **MTR1B** | inactive | `6ME6` | 231 | 53 | BRIL, rubredoxin |
| **NK1R** | inactive | `6E59` | 227 | 196 | PGS |
| **NPY2R** | inactive | `7DDZ` | 250 | 147 | *unnamed* |
| **NTR1** | inactive | `7UL2` | 255 | 32 | **not named** |
| **PD2R2** | inactive | `7M8W` | 236 | 125 | T4L |
| **S1PR1** | inactive | `3V2Y` | 231 | 168 | T4L |
| **S1PR5** | inactive | `7YXA` | 223 | 106 | BRIL |
| **SSR2** | inactive | `7XN9` | 239 | 185 | **not named** |
| **TA2R** | inactive | `6IIU` | 228 | 54 | BRIL, rubredoxin |

Four things follow, and only the first is mine to act on.

1. **Description-based fusion detection undercounts.** On **9 of the 43** the
   depositor's own `pdbx_description` names no fusion at all, yet a 32–185
   residue foreign insertion sits in ICL3: `5GLI` (EDNRB), `5V54` (5HT1B),
   `6KUX` (ADA2A), `6S0L` (AA2AR), `7UL2` (NTR1), `7UL3` (HRH2), `7XN9` (SSR2,
   an endo-1,4-β-xylanase), `7YM8` (ADA1A), `8IRU` (DRD4). Any audit built on the
   description string — or on
   `panel_systems.csv`'s `fusion_in_receptor_entity`, which derives from the same
   metadata — misses those nine. Sequence-level detection is the only kind that
   works. Same class of failure as `4X1H` and as RCSB's empty `pdbx_mutation`.
2. **`3PWH` is not on this panel.** `georgiou2025heterogeneity`'s named A2AR case
   is not among the 128 rule-R references; AA2AR's rule-R inactive is `6S0L` —
   which does carry a 113-residue ICL3 insertion the description does not name.
   So the specific structure is absent and the specific failure mode is present.
3. **This is a reference-selection problem, not a chain-A problem.** Nothing about
   the receptor sequence we supply changes it. It belongs to `PANEL.md` (rule R
   currently *records* fusion presence rather than filtering on it, by design) and
   to Group 0, whose threshold fit is where the damage lands. **Relayed, not
   resolved here.**
4. **What chain A can do about it is make the contamination visible per row.**
   Every prediction should carry `ref_inactive_icl3_fusion ∈ {true,false}` and
   `ref_inactive_icl3_fusion_aa`, both derivable today from
   `seqrec_icl3_audit.tsv`, so any result can be re-reported on the **24
   inactive references without an ICL3 fusion**. That subset is thin — it is
   fewer than half the panel — but it is the only clean comparison available and
   it is named in the file.

---

# 7. What changes between Group 0 and Group 1

The two groups need different things from this file, and one of them may need
almost nothing.

## 7.1 Group 0 — the instrument

Group 0 (E0.1–E0.5) measures geometry on **deposited** structures: 726 off-panel
Class A actives/inactives for the threshold fit, 21 intermediates, the 128
on-panel references held out as the application set. **It supplies no sequence to
any model and therefore needs no chain A.**

What it needs from this file is the *mapping*, not the sequence:

- **the canonical residue numbering per receptor**, so that a generic-numbered
  anchor (Y5.58, Y7.53, 2×46, 6×37) can be located in a deposited chain whose
  author numbering is its own. `seqrec_refs.tsv` gives the entity→canonical map
  for the 128 references; the same `anchor_map` in `seqrec_refs.py` extends to the
  726 off-panel structures at no new cost beyond the downloads Group 0 is already
  budgeting;
- **`seqrec_scoreable.tsv:resolved_both_ranges`**, to check that a predicate
  anchor is resolved before measuring it. `PANEL.md` §9(1) lists "whether the
  predicate anchors are resolved in every reference" as unresolved for want of
  coordinates; the unobserved-residue sets used here are fetched from RCSB and
  answer it without downloading a single structure;
- **`seqrec_icl3_audit.tsv`**, for §6.5. A threshold fitted on a population where
  the inactive class is 40/64 ICL3-fused is fitted on a contaminated class, and
  the contamination pushes the inactive side toward active. On a 5.3:1
  active-biased calibration set this lands on the small side.

**One decision Group 0 does force back onto chain A.** If Group 0 concludes that
ICL3-fused inactive references must be excluded or reweighted, the rule-R pairs
change for up to 40 receptors, and every §6.2 number in this file is recomputed
from the new pairs — `seqrec_refs.py` takes the pair columns as input, so it is a
rerun and not a rewrite. Stated so that nobody quotes a scoreable count from
before that decision as though it survived it.

## 7.2 Group 1 — the ladder

Group 1 (E1.1) needs chain A for **every prediction**: 64 receptors × 8–11 rungs
× 4 backbones × seeds. Concretely:

- **all 64 core receptors**, as the construct §4 specifies — not the 40 of Blocks
  A/B. Twenty-four receptors on the core panel have never had a sequence
  dispatched by this project;
- **exactly one chain-A sequence per receptor, byte-identical across every rung**,
  hashed once and recorded on every row. This is not a formality: Block B's
  `PHASE_1_CONSTRUCT_IDENTITY.md` §1b/1c establishes that the receptor chain was
  arm-invariant, and that invariance is *why* arm effects there are not
  receptor-MSA artefacts. The ladder's argument depends on the same property
  across eleven rungs instead of four arms, and the only way to demonstrate it is
  a per-row `receptor_seq_sha256`;
- **the extension tiers only if their arms are run.** `E-B1` is E7.2's
  cross-class transfer and needs §4.2's ECD exception; `E-scope` needs
  UNRESOLVED-2 answered first.

**A cost note that belongs to RUN_MATRIX, recorded here because it is a
consequence of a construct decision.** Any change to chain A changes its sha256,
and every backbone's MSA cache is keyed on that hash
(`msa_depth_report.md`: 120 unique sequences ↔ 120 cache files, exact 1:1).
Only **40 of the 64 core receptors were ever dispatched**, so 24 receptor MSAs
are new regardless. Of the 40, the cap changes **9** (5HT2C, CNR1, EDNRA, EDNRB,
FSHR, LSHR, MCHR1, OPRK, OX2R) — those must be rebuilt too. That leaves **31**
whose cached MSA is reusable, and only **if** the bytes in the never-shipped
`panel_receptor_sequences.fasta` match canonical, which §2.2 shows cannot be
verified today. **Budget 64 receptor MSA builds.** Any reuse is a bonus that
DATA ASK 1 has to earn first.

---

# 8. What must be recorded per row

Same form as `SEQUENCES.md` §9, for chain A. Everything below is **new**; no block
A–D carries any of it.

| column | why |
|---|---|
| `receptor_seq_sha256` | §0.1. The one chain in every prediction and the one never hashed |
| `receptor_uniprot_acc`, `receptor_seq_version` | a residue range means nothing without them (§0.2) |
| `receptor_construct_range` | e.g. `312-695`; the capped window actually supplied |
| `n_receptor_aa` | every construct verifiable from data, not from a dispatch note |
| `nterm_rule` ∈ `{miglionico_cap, full_ecd, none}` | §4.2's exception must be on the row, not inferred from a length |
| `signal_peptide_removed` ∈ `{true,false}` | §3.1; unanswerable afterwards |
| `receptor_species`, `receptor_isoform_id` | §5, §3.2. `P21731-3` is not `P21731-1` |
| `rmsd_residue_set_sha256`, `rmsd_mask` | §6.3. A count without its set cannot be checked |
| `ref_active_pdb`, `ref_inactive_pdb` | rule-R pairs move (§7.1); a row must say which pair graded it |
| `ref_inactive_icl3_fusion`, `ref_inactive_icl3_fusion_aa` | §6.5. Lets any headline be re-reported on the 24 clean inactive references |

---

# 9. Unresolved — flagged, not guessed

1. **`E-pro`'s eight receptors have no accession in `panel_systems.csv`.** §1.
   Cannot be specified from this file.
2. **Class F / B2 extracellular domains (`E-scope`).** The cap removes 67–88% of
   the Frizzled CRD and AGRE5's GAIN domain. §4.2. No claim depends on it today.
3. **FSHR / LSHR / TSHR ectodomains.** §4.3. **PI decision**, costed, not made.
4. **Signal peptide.** §3.1. No corpus convention; three options costed; (b)
   recommended; **PI decision**.
5. **Receptor sequence bytes are unverifiable for every prediction ever run.**
   §2.2. `refs/panel_receptor_sequences.fasta` has never shipped and no drop
   carries a receptor-chain hash. Lengths match canonical on 48 of 48; identity
   is unchecked. **DATA ASK 1.**
6. **Block B's RMSD residue sets were never emitted**, so `rmsd_n_residues_used`
   cannot be reproduced. §6.3. **DATA ASK 2.**
7. **B1B1U5's `gdb_active` column disagrees with `PANEL.md`'s own Rule R step 4**
   (`9EPP` vs `9EPR`). §5.4. PANEL's to resolve; §6 numbers use the column.
8. **Three references RCSB cannot align to their own receptor** (`9D3G`, `8IRU`,
   `8HCQ`). §6.1. Worked around here; worth reporting upstream.
9. **The TM1 authority.** GPCRdb and UniProt disagree on all 75 entries by 2–12
   residues (§4.1). GPCRdb chosen for coherence with H8. Reversible, both columns
   recorded, and `miglionico2026atlas` does not say which it used —
   **lit question 3.**
10. **`LT4R1` has no GPCRdb H8 segment.** §4.1. C cap falls back to TM7 + 100 and
    is flagged, not guessed.

**11. A possible overlap with a sibling session.** `redo/build/g1_receptors.py`
and `g1_receptors.tsv` were written concurrently by the Group 1 session and also
concern receptor chains. I have not read or edited them and this file was built
independently from `panel_systems.csv`. **If the two disagree on any accession,
length or hash, the disagreement is real and must be resolved before dispatch —
do not assume one is a copy of the other.** `seqrec_verify.py` will fail loudly
on any sequence whose sha256 does not match its record, which makes the
comparison one command.

---

# 10. Data asks (for `DATA_REQUESTS.md`, owned by the orchestrator)

Cost classes per `CLAUDE.md`: **free** = re-analysis of data already held,
**cheap** = re-scoring, no new inference, **real** = new predictions.

| # | ask | cost | what it unblocks |
|---:|---|---|---|
| 1 | **`refs/panel_receptor_sequences.fasta`**, all 51 entries, plus a per-row `receptor_seq_sha256` for Blocks A–D | **free** | the only way to check that what was dispatched is what we think. Settles the three duplicate-sequence receptors (ADRB1 G389R, FSHR 695, MCHR1 422) and retro-validates every receptor number in the paper |
| 2 | **The residue set behind `rmsd_n_residues_used`** — the sorted canonical residue numbers, per receptor, or a hash of them | **free** | makes Block B's RMSD reproducible; §6.3 currently has a count with no set |
| 3 | **`refs/gpcr_coupling.csv`** | **free** | already ask-listed in `SEQUENCES.md` §10(4); repeated because §5.4's B1B1U5 assignment cannot be audited without it |
| 4 | Confirmation of which sequence the 8 receptors with `no_ref_pair_for_<slug>` were scored against, if any | **free** | 6,400 of 32,000 Block B rows have no RMSD and the reason is a missing reference pair, not a missing sequence |

---

# Questions for lit

Each states what I would do differently depending on the answer. Numbered for
relay.

1. **Does any paper in the corpus report the *scoreable fraction* — the share of
   the supplied receptor chain that is present and resolved in the reference it
   is scored against?** §6.2 measures 0.70 median, 0.49–0.87, on our own panel.
   *If a comparable figure exists*, §6 gets an external anchor and the caveat goes
   in Methods as a known property of the field. *If not*, I must present it as our
   own measurement and it becomes a reportable methodological result rather than a
   caveat — which is a different sentence in a different section.

2. **Does any co-folding paper state whether it supplied the signal peptide?**
   The lit session says no convention exists and one of 81 notes mentions signal
   peptides at all. I am asking the narrower question because it is answerable by
   grep on the extractions: *if even one paper states it either way*, §3.1 cites a
   precedent and the PI decision gets easier. *If literally none does*, §3.1 stands
   as written and the redo should state its choice explicitly in Methods precisely
   because nobody else does.

3. **Does `miglionico2026atlas` say which TM1 and H8 annotation its cap was
   measured against?** §4.1: GPCRdb and UniProt disagree on TM1 start for all 75
   panel entries, by 2–12 residues, and UniProt does not annotate H8 at all. *If
   the paper names GPCRdb generic numbering*, our application is exact and I say
   so. *If it names its own or UniProt's*, 16 N-terminal boundaries shift and
   `seqrec_trim.py` is rerun with one flag. *If it says nothing*, §4.1 must carry a
   line stating the frame is ours and the correspondence is by convention.

4. **Is there any structural or functional result on a glycoprotein-hormone
   receptor (FSHR/LSHR/TSHR) predicted *without* its LRR ectodomain?** §4.3 is a
   PI decision and this is the evidence that would settle it. *If someone has
   shown the 7TM core predicts the same with and without the ectodomain*, option
   (a) becomes clearly right and saves the most expensive three chains on the
   panel. *If someone has shown it changes the result*, option (b)/(c) becomes
   mandatory rather than recommended.

5. **Does `hilger2020gcgr`'s ECD-decoupling argument have a Class A analogue —
   has anyone shown that a Class A N-terminal domain does or does not affect
   intracellular TM6 displacement?** §4.2 exempts B1 on hilger's mechanism and
   §4.3 extends the same reasoning to the GpHR LRR domain *by analogy only*. *If a
   Class A result exists*, the analogy becomes an argument and §4.3 stops being a
   PI decision. *If not*, the analogy must be labelled as one in the text.

6. **Does any paper report the effect of an ICL3 fusion on a *predicted*
   structure, as opposed to on the deposited one?** §6.5 finds 40 of 64 inactive
   references ICL3-fused, on `georgiou2025heterogeneity`'s deposited-structure
   argument. *If a co-folding paper has measured what happens when the reference
   is a fusion construct*, the contamination becomes a citable correction and
   Group 0 can quantify it. *If nobody has*, the 24 clean inactive references
   become our own internal control and §8's two columns become load-bearing rather
   than precautionary.

7. **Does the corpus contain any receptor-construct convention for non-human
   panel entries — specifically, does anyone substitute a human orthologue for a
   non-human receptor whose reference structures are non-human?** §5.2/§5.3
   recommend keeping bovine OPSD and mouse OPRM to preserve the
   receptor/reference species match. This is the chain-A half of `SEQUENCES.md`'s
   question 9, which asked the same thing about partners. *If precedent exists for
   substituting*, I reopen both. *If the corpus is silent*, matching the reference
   is the safe reading and I say so.

8. **Is there precedent for reporting a per-row construct hash for the receptor
   chain?** §0.1 and §8 rest on it, and the project has now been burned three
   times by header-vs-content mismatches on the partner side and once on the
   reference side (`4X1H`). *If a paper reports input-sequence hashes*, the
   practice is citable and goes in Methods in one line. *If none does* — which I
   expect — it is worth a sentence in the discussion as a reproducibility point,
   because the cost is one column and the failure it prevents is silent.
