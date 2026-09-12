# Tier D2 nanobody-state-anchor provenance

Date compiled: 2026-09-06.
Source of record: RCSB PDB entry pages + FASTA (public, no auth). See per-row URLs below.

## Panel summary

| receptor_slug | pdb_id | state | nb_name | nb_chains | outcome |
|---|---|---|---|---|---|
| ADRB2 | 5JQH | inactive | Nb60 | C, D | verified |
| OPRK  | 6VI4 | inactive | Nb6 | C, D | verified |
| ACM2  | 4MQS | active   | Nb9-8 | B | verified |
| AGTR1 | 6OS2 | active   | Nb.AT110i1_le | B (auth D) | verified (already in refs) |

**Anchors verified: 4 / 4.** No exclusions.

**Panel composition:**
- 2 Nb-inactive (5JQH ADRB2/Nb60; 6VI4 OPRK/Nb6).
- 2 Nb-active (4MQS ACM2/Nb9-8; 6OS2 AGTR1/Nb.AT110i1_le).
- 1 matched pair candidate: ADRB2 (5JQH Nb-inactive vs 4LDE Nb-active, already in refs).

**Unique Nb sequences to MSA-warm: 4** (Nb60, Nb6, Nb9-8, Nb.AT110i1_le are all distinct llama VHH sequences; no duplicates across the panel).

## Per-entry verification

### 5JQH — ADRB2 / Nb60 (inactive)

- URL: https://www.rcsb.org/structure/5JQH
- FASTA: https://www.rcsb.org/fasta/entry/5JQH
- Title: "Structure of beta2 adrenoceptor bound to carazolol and inactive-state stabilizing nanobody, Nb60"
- Publication: Staus et al. 2016 Nature, "Allosteric nanobodies reveal the dynamic range and diverse mechanisms of G-protein-coupled receptor activation."
- Polymer chains:
  - A, B — β2AR / T4L chimera (471 aa)
  - C, D — Nanobody Nb60 (125 aa incl. C-term His6 tag)
- Ligands: CAU (carazolol, inverse agonist), CLR (cholesterol).
- State evidence: title states "inactive-state stabilizing nanobody"; abstract describes Nb60 as stabilizing a low-affinity inactive receptor conformation. Carazolol is an inverse agonist.
- Deposited 2016-05-05; released 2016-07-13. Pre-dates Chai / Protenix / Boltz-2 cutoffs; OF3 TBD.
- Nb chain selection: C and D are duplicates (crystallographic); either can be used. Sequence pulled verbatim from FASTA header `5JQH_2 | Chains C, D | Nanobody60, Nb60`.

### 6VI4 — OPRK / Nb6 (inactive)

- URL: https://www.rcsb.org/structure/6VI4
- FASTA: https://www.rcsb.org/fasta/entry/6VI4
- Title: "Nanobody-Enabled Monitoring of Kappa Opioid Receptor States"
- Publication: Che et al. 2020 Nat Struct Mol Biol (same-titled).
- Polymer chains:
  - A, B — κ-opioid receptor (307 aa)
  - C, D — Nanobody 6 (133 aa incl. N-term M + C-term His6-EPEA)
- Ligands: JDC (JDTic, antagonist scaffold), CLR (cholesterol).
- State evidence: entry description states Nb6 stabilizes a "ligand-dependent inactive state"; JDTic is a well-characterized κOR antagonist.
- Deposited 2020-01-11; released 2020-03-18. Pre-dates Chai / Protenix / Boltz-2; OF3 TBD.
- Nb chain selection: C, D duplicates. Sequence from FASTA header `6VI4_2 | Chains C, D | Nanobody 6`.

### 4MQS — ACM2 / Nb9-8 (active)

- URL: https://www.rcsb.org/structure/4MQS
- FASTA: https://www.rcsb.org/fasta/entry/4MQS
- Title: "Structure of active human M2 muscarinic acetylcholine receptor bound to the agonist iperoxo"
- Publication: Kruse et al. 2013 Nature, "Activation and allosteric modulation of a muscarinic acetylcholine receptor."
- Polymer chains:
  - A — M2 muscarinic receptor (351 aa)
  - B — Nanobody 9-8 (125 aa incl. N-term GPGS linker; no C-term tag)
- Ligand: IXO (iperoxo, high-affinity agonist).
- State evidence: title states "active"; Nb9-8 mimics G-protein coupling, selected by yeast display for the active conformation.
- Deposited 2013-09-16; released 2013-11-27. Pre-dates all backbone cutoffs; OF3 TBD.
- Nb chain selection: unique (only chain B is Nb).

### 6OS2 — AGTR1 / Nb.AT110i1_le (active)

- URL: https://www.rcsb.org/structure/6OS2
- FASTA: https://www.rcsb.org/fasta/entry/6OS2
- Title: "Structure of synthetic nanobody-stabilized angiotensin II type 1 receptor bound to TRV026"
- Publication: Wingler et al. 2019 Cell, "Angiotensin and biased analogs induce structurally distinct active conformations within a GPCR."
- Polymer chains:
  - A — AT1R / BRIL fusion (425 aa)
  - B (auth D) — Nanobody Nb.AT110i1_le (128 aa incl. C-term LE)
  - C (auth B) — TRV026 peptide (8 aa)
- Ligands: CLR (cholesterol), OLC, NAG (co-crystal accessories).
- State evidence: publication title explicitly frames the structure as an "active conformation." TRV026 is a Sar1-biased AngII analog (β-arrestin-biased agonist); the Nb.AT110i1 series is an engineered active-state stabilizer (matures from AT110 conformational selection).
- Deposited 2019-05-01; released 2020-02-19. Pre-dates all backbone cutoffs; OF3 TBD.
- Nb chain selection: unique among protein chains. FASTA header `6OS2_2 | Chain B[auth D] | Nanobody Nb.AT110i1_le`.
- **Duplication caveat:** 6OS2 already appears in `refs/reference_set.csv`. Include in Tier D2 anchor manifest but do NOT double-count in the cognate reference set. Cross-reference the pending ceremony noted in `MEMORY.md` before adding it to reference_set.csv again.

## Notes on scoping-claim vs actual PDB metadata

- The parent-agent scoping note called the AGTR1 nanobody "Sarile-Nb + AngII." The actual PDB entry uses "Nb.AT110i1_le + TRV026." TRV026 is a Sar1-Ile-substituted AngII analog (biased agonist), so the scoping description is a compressed but recognisable form of the actual chemistry — no fabrication risk. Recorded as `nb_name = Nb.AT110i1_le` (RCSB nomenclature) for reproducibility.
- All four Nb sequences are pasted **verbatim from FASTA** including engineering tags (His6 on Nb60 and Nb6; N-term GPGS on Nb9-8; C-term LE on Nb.AT110i1_le). Downstream users may wish to strip tags before MSA warm-up, but the sequences as given here are the canonical RCSB record and should not be silently edited.

## Backbone-cutoff status

All four anchors deposited on or before 2020-01-11, i.e. before the Chai (2021-01-12), Protenix (2021-09-30), and Boltz-2 (2023-06-01) cutoffs. OF3 training cutoff not yet public — flagged `TBD` per column spec. This means all four anchors could in principle appear in any of the three known training sets; the Tier D2 existence-proof is not a hold-out prospectivity claim but a **steerability** claim (input chain redirects the predicted state).

## What was NOT done

- No modifications to `refs/reference_set.csv`, `refs/sealed_active_refs_2026_09_01.csv`, or any other file outside the two deliverables.
- No commits.
- No downstream MSA warm-up dispatched — that belongs to Tier D2 dispatch.
