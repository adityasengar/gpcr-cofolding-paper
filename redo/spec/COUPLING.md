# COUPLING.md — which Gα is cognate, per receptor, and on what authority

**Scope.** The 64 core receptors of `redo/inputs/panel_systems.csv` (rows where
`'C1' in tier.split('|')`). This file decides nothing about panel membership,
ligands, run matrix or rung construction — those belong to `PANEL.md`,
`SEQUENCES.md`, `RUN_MATRIX.md` and the Group 0 / Group 1 system files, which are
owned by other sessions and are not touched here.

**Why this file exists.** Every rung of the partner-length ladder is defined as
*"the last N residues of the **cognate Gα**"*, so the centrepiece experiment is
parameterised by an assignment nobody has audited. The PI raised it himself:
*"how to give G-protein, whether it is accurate or not."* It has already gone
wrong once — see §11.

**Everything below is recomputed**, not asserted. `coupling_summary.py` prints
every number in this document; `coupling_summary.py --selftest` plants a defect
in each of its four checks and requires each to fire.

---

## 0. DECIDED — read the cognate off the structure the receptor was solved with

**Aditya, 2026-09-11:** *"read it off the structure the receptor was solved with.
We already have all 81 of them."* Option A below is now the rule. The options
table is kept in §0b because the choice should stay visible, not because it is
still open.

**The map is built and frozen: `coupling_cognate_map.tsv`, 64 rows, keyed by
`receptor_slug`** — the column name `g1_systems.csv` already uses. Companion
`coupling_cognate_rungs.tsv` gives receptor × rung → `sha256`, `len`, `sequence`
lifted from `seq_rungs.tsv`, so `g1_systems.py` can fill `chain_b_sha256` by a
join and no arithmetic.

| | count | what a consumer should do |
|---|---:|---|
| `frozen` — read off the Rule-R structure | **47** | use `cognate_subtype`; hash from `coupling_cognate_rungs.tsv` |
| `frozen_with_caveat` — OPSD, read off an 11-mer | **1** | usable, but see §14.3 before any `R6`/`R7` arm |
| `frozen_by_convention` — no Gα in the Rule-R reference | **6** | usable, but **not a structure read**; `evidence_class = CONVENTION_FALLBACK` |
| `needs_decision` — the deposited partner is a cross-family chimera | **10** | **do not hash.** Two options per receptor, §14.2 |

**54 of 64 resolve; 336 + 42 = 378 rung rows are emitted.** Of the provisional
CORE-32: **28 resolve** (23 frozen, 4 by convention, 1 OPSD) and **4 need a
decision** — 5HT2A, GRPR, OX2R, OXYR.

**Subtypes the panel actually uses: Gi1 ×32, Gs ×12, Go ×5, Gq ×3, Gi3 ×1,
Gt1 ×1.** Six labels, all of which already exist in `seq_rungs.tsv`.

---

## 0a. The rule, in pre-registrable form

It consumes only the panel and the PDB. No prediction, no score, no model output;
run it before any inference and it gives the same answer. Implemented in
`coupling_cognate_map.py`, whose `--selftest` plants an input for every branch.

> **R-COG-1 — the reference.** The receptor's reference is the **active**
> structure that `PANEL.md`'s Rule R selects, read from
> `g1_receptors.tsv:active_pdb`. Not the union of candidate actives, and **not
> whichever active happens to contain a G protein** — whichever Rule R picked,
> including when that entry has no transducer at all.
>
> **R-COG-2 — the entity.** The partner is the polymer entity of that structure
> classified `G-alpha` or `G-alpha-fusion`. Where more than one qualifies, the
> longest is taken and the discarded ones are recorded on the row.
>
> **R-COG-3 — the subtype.** The cognate subtype is the canonical human Gα whose
> **C-terminal 21 residues** have the highest identity to the deposited entity's
> last 21. The canonical termini are read from `seq_rungs.tsv` itself.
>
> **R-COG-4 — ties.** Gi1≡Gi2, Gt1≡Gt2≡Ggust and Gq≡G11 are byte-identical over
> ct21, so a tie among them carries no information and is resolved by a
> representative **declared in advance**, never by sort order: `{Gi1,Gi2}→Gi1`,
> `{Gt1,Gt2,Ggust}→Gt1`, `{Gq,G11}→Gq`. The full tie set is kept on the row.
>
> **R-COG-5 — the threshold.** If the best ct21 identity is **below 0.80**, or if
> the canonical Gα tied at the best score **span more than one family**, the
> deposited partner is a chimera and **the rule does not resolve it**. Verdict
> `needs_decision`; scaffold family and tip family both reported; no subtype
> emitted.
>
> **R-COG-6 — short entities.** If the entity is shorter than 21 residues its
> ct21 does not exist. Scoring falls back to ct11, the **margin to the nearest
> canonical of any other family** is reported, and the class is `PEPTIDE_ENTITY`.
>
> **R-COG-7 — no partner.** If the Rule-R active reference contains no Gα, the
> rule cannot be applied. The row falls back to the family in
> `coupling_assignments.csv:recommended_family` and that family's **declared**
> representative — `Gs→Gs, Gi/o→Gi1, Gq/11→Gq, G12/13→G13` — with class
> `CONVENTION_FALLBACK` and verdict `frozen_by_convention`.
>
> **R-COG-8 — the alternative.** Where a **non**-Rule-R active reference of the
> same receptor contains a Gα, it is reported in `alt_pdb` / `alt_subtype`. It
> never overrides R-COG-1.

**Two properties worth stating because they are what make the rule
pre-registrable rather than merely deterministic.** First, the tie
representatives and the family representatives are declared constants in the
script, above the code that uses them, so they cannot be chosen after seeing a
result. Second, R-COG-1 deliberately refuses the most tempting shortcut: *pick
whichever active reference has a G protein in it*. That shortcut is
result-dependent in a subtle way — it would silently re-select the reference for
**6 receptors** and would have turned NTR1, AGTR1, OPRD, AA2AR, ADRB1 and OPRM
from convention rows into structure rows by choosing a different structure than
the one the panel is scored against. R-COG-1 keeps the reference and the partner
read from **the same** entry, which is the whole point of "read it off the
structure the receptor was solved with".

### The one place the tie representative is not free

`R-COG-4` costs nothing at `R1`–`R5`, where the tie members are byte-identical.
At `R6a_da5` and `R7_full` they are not: Gi1 is 354 aa and Gi2 355.
**32 of the 54 resolved receptors carry a tie** — 29 `Gi1/Gi2`, 2 `G11/Gq`, 1
`Ggust/Gt1/Gt2` — and for those the full-subunit rungs depend on the declared
representative. Every such row carries `tie_changes_bytes_at = R6a_da5,R7_full`.
If the PI would rather resolve those by subtype annotation than by declaration,
that is a live option and it affects only the two longest rungs.

---

## 0b. The three options, kept visible

Costs recomputed as before; Option A is the one taken.

| | option | what it is | extra receptor-arms | status |
|---|---|---|---|---|
| **A** | **Structure-grounded pick** | supply the Gα family that is in the receptor's own active reference | **0** (1.00×) | **CHOSEN 2026-09-11** |
| **B** | Hedge the primary set | one arm per family some authority calls primary | +34 (1.53×) | not taken |
| **C** | Hedge everything annotated | one arm per family annotated as a transducer at all | +107 (2.67×) | not taken |

Option A is what `chiesa2025templatebias` p.6302 does — the only corpus precedent
for picking — and it is the only option under which the supplied partner and the
reference the state predicate is calibrated on are the same family. Its cost is
that partner identity stops being a measured axis; the Block D question in §11
("is the effect cognate-specific at all?") is therefore **not answered by Group
1 under this rule** and needs its own arm. Recorded so the limitation is not
discovered later.

---

## 1. What was consulted, and why the structure outranks the databases

Three authorities, fetched separately and never merged into a single "consensus"
column. Fetch date **2026-09-11**, scripts `coupling_fetch.py` (network) and
`coupling_assign.py` (no network).

| | authority | what it is | how it was obtained | coverage of the 64 |
|---|---|---|---|---|
| **A1** | **GproteinDb couplings** | one row per receptor × source lab: GproteinDb merged, GtoPdb, Bouvier/GEMTA, Inoue/TGFα-shedding, Martemyanov/FreeGβγ-Nluc, Lambert/RGB-GDP, Roth/TRUPATH | `https://gproteindb.org/signprot/couplings`, 964 rows parsed, 263 matching a C1 accession → `coupling_gproteindb.csv` | 53 with ≥1 assay lab; 61 with a GtoPdb row |
| **A2** | **IUPHAR/BPS Guide to PHARMACOLOGY, direct** | the curator's own transducer annotation, fetched from IUPHAR rather than through GproteinDb's copy, so the two can be diffed | `guidetopharmacology.org/services/targets?accession=…` then `/transduction` → `coupling_gtopdb.csv` | 61 of 64 |
| **A3** | **The deposited active reference** | every polymer entity of every active reference PDB: description, UniProt xref, organism, full one-letter sequence | RCSB GraphQL, 189 entries (active + inactive) → `coupling_rcsb_entities.json`, `coupling_refstructures.csv` | 63 of 64 |

**A3 is the only one that is not an annotation.** A1 and A2 say what a receptor
is *believed* to couple. A3 says what is physically in the coordinate file our
own state predicate is calibrated against. When our supplied partner and the
reference assembly's partner are different families, that is an internal
inconsistency in our own experiment and needs no external authority to
adjudicate. Every receptor row cites its own sources; nothing here is cited once
globally.

### A3 is not read from the UniProt cross-reference

Following `analysis/verify_alpha5ct_family.py`: a coupling chimera is a Gα
backbone carrying another family's C-terminal helix, and on those entries the
UniProt cross-reference names the **backbone**. The family is therefore read from
the **deposited C-terminal residues**, with ties kept as ties.

**One deliberate change from that script, and it matters.**
`verify_alpha5ct_family.py` scores the last **21** because that is the length the
paper's title claims. That window is wrong for mini-G constructs, which graft
only the last handful of residues onto a Gs scaffold: at 21 they score ~0.62
against *every* family and fall out as `UNRECOGNISED`. Eleven of the C1 active-reference
Ga chains do exactly that. `coupling_assign.py` scores **both** windows, reports
both, and calls the family from the **11** — which is also the ladder's shortest
rung. All eleven resolve cleanly at 11.

A twelfth chimera is caught by the other test — `verify_alpha5ct_family.py`'s own:
the deposited C-terminus names a family other than the accession's. B1B1U5/9EPP
passes the two-window test (its last 21 still score 0.86) and fails this one
(cross-referenced to GNAI1, alpha5 tip Gq). Both tests are applied; neither alone
is sufficient.

### Correction to the brief I was given

> *"Our GPCRdb snapshot's `signalling_protein` field is too coarse (it records
> only `G protein` / `Arrestin` / none, verified)."*

**This is not what the snapshot contains.** `lit/panels/cache/gpcrdb_structures.json`
carries, for **1,007 of its 1,716 entries**, a `signalling_protein.data` dict
naming each partner chain by GPCRdb entry name and auth chain — `gnas2_human`,
`gnai1_human`, `gnaq_human`, `gnat1_bovin`, `arrb1_human` and 30 others. So the
subtype *is* in the snapshot. It is still not sufficient, for a different reason:
it names the entry the chain is cross-referenced to, which on a mini-G chimera is
the scaffold. RCSB entity sequences were fetched anyway, and that is what caught
the twelve chimeras in §6. The conclusion stands; the stated reason for it did
not.

---

## 2. The verdict column

Three values, so the ladder builder can key off one field and the PI can see the
blast radius at a glance.

| verdict | n | meaning |
|---|---:|---|
| `cognate_confident` | **8** | every available authority names the **same single family**, at least two authorities exist, and no further transducer is annotated anywhere |
| `cognate_ambiguous` | **42** | authorities are **compatible** but not identical — one reports a tie, or a secondary transducer is annotated, or only one authority exists. There is a family to supply; it is a choice, not a fact |
| `cognate_conflicted` | **14** | two authorities are **disjoint** — they cannot both be right — or no family is compatible with all of them |

**The distinction that took a rewrite to get right.** An authority reporting a
*tie* is not contradicting an authority reporting one member of that tie; it is
reporting the same thing at lower resolution. EDNRB's GtoPdb row ranks Gs, Gi/o
and Gq/11 all `1'` and IUPHAR lists all three, while both assay labs and the
deposited structure say Gi/o. The first version of the verdict rule treated
unequal sets as disagreement and filed EDNRB as `conflicted`, which would have
sent the PI a blocker on a receptor with a perfectly clear answer. `conflicted`
now means **disjoint**.

**Two hard rules imported from lit, both applied mechanically:**

1. **A `G12/13` primary never passes as confident.** Inter-dataset core agreement
   for that family is **0%** (`pandyszekeres2024gproteindb` p.8, Fig. 4C). Eight
   C1 receptors have some authority calling G12/13 primary — CCKAR, CCR6, EDNRA,
   GHSR, LPAR1, PE2R4, S1PR5, TA2R — and none of them is `cognate_confident`.
2. **IUPHAR is never used alone.** It omits 26–42% of family couplings relative
   to the biosensor datasets, depending on family (same source). On this panel,
   **11 of 64** receptors have a family that a biosensor lab ranks `1'` and
   GtoPdb does not list at all: 5HT2C (Gi/o), AA1R (Gq/11), C5AR1 (Gq/11), CCKAR
   (G12/13), CCR6 (G12/13), CNR1 (Gq/11), EDNRA (G12/13 + Gi/o), GHSR (G12/13),
   HRH2 (Gs), PE2R4 (G12/13), TA2R (G12/13).

### The eight confident receptors

CCR2, CCR8, CXCR3 (3 authorities each), DRD3, DRD4, HRH3, PD2R2 (4 each),
NPY1R (5). **All eight are Gi/o.** No Gs, Gq/11 or G12/13 receptor on this panel
reaches `confident` — a fact worth stating in Methods, because it means the
panel's confidence is not evenly distributed over the families whose α5-CT the
ladder varies.

---

## 3. Per-receptor assignment, with the authority named on every row

> **This table is the evidence survey, not the deliverable.** It weighs all three
> authorities against each other and was what §0's decision was taken *from*.
> The frozen, machine-readable answer that `g1_systems.py` consumes is **§14**,
> built by R-COG off the Rule-R reference alone. Where the two differ — six
> receptors, listed in §14.1 — **§14 wins**, because it is the rule Aditya chose.

`supply` is `recommended_family` from `coupling_assignments.csv` — the family
compatible with every authority where one exists, else the deposited reference's
family (basis: `chiesa2025templatebias` p.6302), else a plurality with the basis
recorded as `NONE — needs a PI decision`. The `active reference contains` column
is read from the **deposited sequence**, not the accession; `(chimera)` means the
scaffold is one family and the α5 tip another, `(mini-G)` means the chain is
under 300 aa where the full subunit is 350–395.

| # | receptor | gene | verdict | supply | assay labs (rank 1') | GtoPdb | IUPHAR direct | active reference contains | 2nd transducers |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5HT1B | HTR1B | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 6G79 Go (mini-G) | Gq/11 |
| 2 | 5HT2A | HTR2A | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Lambert=Gq/11<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 8UWL G11/G14/Gq (chimera) | Gi/o |
| 3 | 5HT2C | HTR2C | **CONFLICTED** | `Gq/11` | Bouvier=Gi/o<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 8DPF G11/G14/Gq (chimera) | G12/13 |
| 4 | 5HT5A | HTR5A | ambiguous | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 7UM5 Go (mini-G)<br>7X5H Gi1/Gi2 | Gq/11 |
| 5 | AA1R | ADORA1 | **CONFLICTED** | `Gi/o` | Bouvier=Gq/11<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7LD3 Gi1/Gi2 | G12/13;Gs |
| 6 | AA2AR | ADORA2A | ambiguous | `Gs` | Bouvier=Gs<br>Martemyanov=Gs | Gs | Gs | 5G53 Gs (mini-G)<br>6GDG Gs (mini-G) | G12/13;Gi/o;Gq/11 |
| 7 | ACM1 | CHRM1 | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 6OIJ G11/Gq | Gi/o;Gs |
| 8 | ACM2 | CHRM2 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7T94 Go | Gq/11;Gs |
| 9 | ACM4 | CHRM4 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7TRP Gi1/Gi2 | G12/13;Gq/11;Gs |
| 10 | ADA1A | ADRA1A | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 7YM8 G11/G14/Gq (chimera)<br>8THK G11/G14/Gq (chimera) | G12/13;Gi/o;Gs |
| 11 | ADA2A | ADRA2A | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7EJ8 Go<br>9CBL Gi1/Gi2 | G12/13;Gq/11;Gs |
| 12 | ADRB1 | ADRB1 | ambiguous | `Gs` | Bouvier=Gs<br>Martemyanov=Gs | Gs | Gs | 8DCS Gs | G12/13;Gi/o;Gq/11 |
| 13 | ADRB2 | ADRB2 | ambiguous | `Gs` | Bouvier=Gs<br>Lambert=Gs<br>Martemyanov=Gs<br>Roth=Gs | Gs | Gs | 8GG0 Gs | Gi/o;Gq/11 |
| 14 | AGTR1 | AGTR1 | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Lambert=Gq/11 | Gi/o;Gq/11 | Gi/o;Gq/11 | 7F6G G11/Gq | G12/13 |
| 15 | APJ | APLNR | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8XZH Gi1/Gi2 | G12/13;Gq/11 |
| 16 | B1B1U5 | HaRh1 | ambiguous | `Gi/o` | — | — | — | 9EPP G11/Gq (chimera)<br>9EPR Gi1/Gi2 | — |
| 17 | C5AR1 | C5AR1 | **CONFLICTED** | `Gi/o` | Bouvier=Gq/11<br>Lambert=Gi/o | Gi/o | Gi/o | 7Y66 Gi1/Gi2<br>7Y67 Gi1/Gi2 | — |
| 18 | CCKAR | CCKAR | **CONFLICTED** | `Gs` | Bouvier=G12/13<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 7MBX Gs | Gi/o |
| 19 | CCR2 | CCR2 | **confident** | `Gi/o` | — | Gi/o | Gi/o | 7XA3 Gi1/Gi2 | — |
| 20 | CCR5 | CCR5 | ambiguous | `Gi/o` | Bouvier=Gi/o | Gi/o | Gi/o | 7F1S Gi1/Gi2<br>7O7F Gi1/Gi2 | Gq/11 |
| 21 | CCR6 | CCR6 | **CONFLICTED** | `Gi/o` | Bouvier=G12/13 | Gi/o | Gi/o | 6WWZ Go (mini-G) | Gq/11 |
| 22 | CCR8 | CCR8 | **confident** | `Gi/o` | — | Gi/o | Gi/o | 8KFX Gi1/Gi2<br>8XML Gi1/Gi2 | — |
| 23 | CNR1 | CNR1 | **CONFLICTED** | `Gi/o` | Bouvier=Gq/11<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8GHV Gi1/Gi2 | G12/13;Gs |
| 24 | CNR2 | CNR2 | ambiguous | `Gi/o` | Bouvier=Gi/o | Gi/o | Gi/o | 8GUR Gi1/Gi2 | Gq/11;Gs |
| 25 | CXCR2 | CXCR2 | ambiguous | `Gi/o` | Bouvier=Gi/o | Gi/o | Gi/o | 6LFO Gi1/Gi2 | Gq/11 |
| 26 | CXCR3 | CXCR3 | **confident** | `Gi/o` | — | Gi/o | Gi/o | 8HNM Gi1/Gi2 | — |
| 27 | CXCR4 | CXCR4 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8U4N Gi1/Gi2 | Gq/11 |
| 28 | DRD2 | DRD2 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7JVR Gi1/Gi2<br>8TZQ Go | Gq/11;Gs |
| 29 | DRD3 | DRD3 | **confident** | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 7CMV Gi1/Gi2<br>8IRT Gi1/Gi2 | — |
| 30 | DRD4 | DRD4 | **confident** | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 8IRU Gi1/Gi2/Gt1/Gt2 (chimera) | — |
| 31 | EDNRA | EDNRA | **CONFLICTED** | `Gq/11` | Bouvier=G12/13<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gq/11 | Gq/11 | 8HCQ G11/G14/Gq (chimera) | Gs |
| 32 | EDNRB | EDNRB | ambiguous | `Gi/o` | Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o;Gq/11;Gs | Gs;Gi/o;Gq/11 | 8IY5 Gi1/Gi2 | G12/13 |
| 33 | FSHR | FSHR | ambiguous | `Gs` | — | Gi/o;Gq/11;Gs | Gs;Gi/o;Gq/11 | 8I2G Gs (mini-G) | — |
| 34 | GHSR | GHSR | **CONFLICTED** | `Gi/o` | Bouvier=G12/13 | Gq/11 | Gq/11 | 7NA7 Gi1/Gi2<br>7NA8 Gi1/Gi2 | — |
| 35 | GPR52 | GPR52 | **CONFLICTED** | `Gs` | Lambert=Gq/11<br>Martemyanov=Gs | — | — | 8HMP Gs (mini-G) | Gi/o |
| 36 | GPR6 | GPR6 | ambiguous | `Gs` | — | Gi/o;Gs | Gs;Gi/o | 8TYW Gs | — |
| 37 | GRPR | GRPR | ambiguous | `Gq/11` | Martemyanov=Gq/11 | Gq/11 | Gq/11 | 7W40 G11/Gq<br>8H0Q G11/G14/Gq (chimera) | G12/13;Gi/o |
| 38 | HRH1 | HRH1 | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Lambert=Gq/11<br>Martemyanov=Gq/11 | Gq/11 | Gq/11 | 8YN2 G11/G14/Gq (chimera) | G12/13;Gi/o;Gs |
| 39 | HRH2 | HRH2 | **CONFLICTED** | `Gs` | Bouvier=Gs<br>Lambert=Gs<br>Martemyanov=Gs | Gq/11 | Gq/11 | 8YN3 Gs (mini-G) | G12/13;Gi/o |
| 40 | HRH3 | HRH3 | **confident** | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 8YN5 Gi1/Gi2<br>8YUU Gi1/Gi2 | — |
| 41 | LPAR1 | LPAR1 | ambiguous | `Gi/o` | Bouvier=Gi/o | G12/13;Gi/o;Gq/11 | Gi/o;Gq/11;G12/13 | 7TD0 Gi1/Gi2 | — |
| 42 | LSHR | LHCGR | ambiguous | `Gs` | — | Gs | Gs | 7FIH Gs<br>7FII Gs | Gq/11 |
| 43 | LT4R1 | LTB4R | ambiguous | `Gi/o` | Bouvier=Gi/o | Gi/o;Gq/11 | Gi/o;Gq/11 | 7VKT Gi1/Gi2 | G12/13 |
| 44 | MCHR1 | MCHR1 | ambiguous | `Gi/o` | — | Gi/o;Gq/11;Gs | Gs;Gi/o;Gq/11 | 8WWK Gi1/Gi2 | — |
| 45 | MTR1A | MTNR1A | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7VGY Gi1/Gi2 | Gq/11 |
| 46 | MTR1B | MTNR1B | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7VH0 Gi1/Gi2 | Gq/11 |
| 47 | NK1R | TACR1 | **CONFLICTED** | `Gs` | Martemyanov=Gq/11 | Gq/11;Gs | Gs;Gq/11 | 8U26 Gs (mini-G) | G12/13;Gi/o |
| 48 | NPY1R | NPY1R | **confident** | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7VGX Gi1/Gi2<br>7X9A Gi1/Gi2 | — |
| 49 | NPY2R | NPY2R | ambiguous | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 7YON Gi1/Gi2<br>8K6N Gi1/Gi2 | Gq/11 |
| 50 | NTR1 | NTSR1 | **CONFLICTED** | `Gi/o` | Martemyanov=Gq/11<br>Roth=Gq/11 | Gq/11 | Gq/11 | 6OS9 Gi1/Gi2<br>8FN1 Go (mini-G) | G12/13;Gs |
| 51 | OPRD | OPRD1 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8F7S Gi1/Gi2 | G12/13;Gq/11 |
| 52 | OPRK | OPRK1 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8FEG Gi1/Gi2 | G12/13;Gq/11 |
| 53 | OPRM | Oprm1 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Lambert=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | — none — | Gq/11 |
| 54 | OPRX | OPRL1 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 8F7X Gi1/Gi2 | Gq/11 |
| 55 | OPSD | RHO | ambiguous | `Gi/o` | — | — | — | 4X1H Gt1/Gt2 (11-mer peptide) | — |
| 56 | OX2R | HCRTR2 | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Martemyanov=Gq/11 | Gi/o;Gq/11;Gs | Gq/11 | 7L1V G11/G14/Gq (chimera) | G12/13 |
| 57 | OXYR | OXTR | ambiguous | `Gq/11` | Bouvier=Gq/11<br>Lambert=Gq/11<br>Martemyanov=Gq/11 | Gq/11 | Gi/o;Gq/11 | 7RYC G11/G14/Gq (chimera) | — |
| 58 | PD2R2 | PTGDR2 | **confident** | `Gi/o` | Martemyanov=Gi/o | Gi/o | Gi/o | 8XXV Gi1/Gi2 | — |
| 59 | PE2R4 | PTGER4 | **CONFLICTED** | `Gs` | Bouvier=Gs<br>Inoue=G12/13<br>Martemyanov=Gs | Gs | Gs | 8GCP Gi1/Gi2<br>8GDB Gs | Gq/11 |
| 60 | S1PR1 | S1PR1 | ambiguous | `Gi/o` | Bouvier=Gi/o | Gi/o | Gi/o | 7TD4 Gi1/Gi2 | G12/13;Gq/11 |
| 61 | S1PR5 | S1PR5 | ambiguous | `Gi/o` | — | G12/13;Gi/o | Gi/o;G12/13 | 7EW1 Gi1/Gi2 | — |
| 62 | SSR2 | SSTR2 | ambiguous | `Gi/o` | Bouvier=Gi/o<br>Martemyanov=Gi/o | Gi/o | Gi/o | 7T10 Gi3 | G12/13;Gq/11 |
| 63 | TA2R | TBXA2R | **CONFLICTED** | `Gq/11` | Inoue=G12/13<br>Lambert=Gq/11<br>Martemyanov=G12/13 | Gq/11 | Gq/11 | 8XJN G11/G14/Gq (chimera) | — |
| 64 | TSHR | TSHR | ambiguous | `Gs` | — | Gs | Gs | 7UTZ Gs (mini-G) | Gq/11 |

Full machine-readable form, with every rank order, percentage, biosensor,
reference DOI and reason string: `coupling_assignments.csv` (28 columns) and
`coupling_gproteindb.csv` (263 rows, one per receptor × source).

---

## 4. The fourteen conflicts, reported not resolved

Each of these has two authorities that **cannot both be right**. The `supply`
column above gives what I would use and the one-line reason; the conflict is the
finding and stays on the record either way.

| receptor | the conflict | what I would use, and why |
|---|---|---|
| **5HT2C** | Bouvier/GEMTA ranks **Gi/o** 1'; Martemyanov, GtoPdb, IUPHAR and the structure all say **Gq/11** | `Gq/11` — 4 authorities to 1, and the structure is among them |
| **AA1R** | Bouvier ranks **Gq/11** 1'; Lambert, Martemyanov, GtoPdb, IUPHAR and 7LD3 say **Gi/o** | `Gi/o` — same shape |
| **C5AR1** | Bouvier **Gq/11** vs Lambert **Gi/o**; GtoPdb, IUPHAR and both structures (7Y66, 7Y67 Gi1) say Gi/o | `Gi/o` |
| **CCKAR** | Bouvier **G12/13**, Martemyanov/GtoPdb/IUPHAR **Gq/11**, and the deposited 7MBX is a **Gs** heterotrimer | `Gs` **only if the goal is internal consistency with the reference.** Biologically CCKAR is Gq-primary. **This one needs a PI decision** |
| **CCR6** | Bouvier **G12/13** against Gi/o everywhere else, structure 6WWZ mini-Go | `Gi/o`; Bouvier's G12/13 is in the 0%-agreement family |
| **CNR1** | Bouvier **Gq/11** against Lambert/Martemyanov/GtoPdb/IUPHAR/8GHV **Gi/o** | `Gi/o` |
| **EDNRA** | three answers on one receptor — Bouvier **G12/13**, Lambert and Martemyanov **Gi/o**, and GtoPdb/IUPHAR/8HCQ **Gq/11**. No assay lab supports the annotated primary | `Gq/11` — GtoPdb, IUPHAR and the 8HCQ chimera tip agree, but note that both biosensor labs that tested it disagree with all three |
| **GHSR** | Bouvier **G12/13**, GtoPdb/IUPHAR **Gq/11**, **both** deposited actives (7NA7, 7NA8) are **Gi1** | `Gi/o` if the reference governs; **PI decision** — no annotation supports Gi/o as primary |
| **GPR52** | Lambert **Gq/11** vs Martemyanov **Gs**; no IUPHAR record at all; 8HMP is mini-Gs | `Gs` — the structure is the tiebreak |
| **HRH2** | all three assay labs and the 8YN3 mini-Gs say **Gs**; GtoPdb/IUPHAR say **Gq/11** | `Gs` — this is the clearest case of the IUPHAR omission lit warned about |
| **NK1R** | Martemyanov **Gq/11**; GtoPdb/IUPHAR tie Gq/11 with Gs; 8U26 is **mini-Gs** | `Gs` for internal consistency, `Gq/11` for pharmacology. **PI decision** |
| **NTR1** | every annotation says **Gq/11**; **both** deposited actives (6OS9 Gi1, 8FN1 mini-Go) are **Gi/o** | **PI decision.** This is the sharpest annotation-vs-structure split on the panel |
| **PE2R4** | Inoue **G12/13** against Bouvier/Martemyanov/GtoPdb/IUPHAR **Gs**; and its two active references disagree with *each other* — 8GCP is Gi1, 8GDB is Gs | `Gs`, and **pick one reference**; a receptor whose two actives carry different Gα cannot have one "reference state" |
| **TA2R** | Inoue and Martemyanov **G12/13**, Lambert/GtoPdb/IUPHAR **Gq/11**, 8XJN chimera tip Gq | `Gq/11`, flagged — G12/13 is the 0%-agreement family |

**Three receptors where the deposited structure contradicts *every* annotation**
— CCKAR (structure Gs, annotations Gq/11 and G12/13), GHSR (structure Gi/o,
annotations Gq/11 and G12/13), NTR1 (structure Gi/o, annotation Gq/11). These are
the receptors where Option A and Option B give different answers, and they are
the ones to put in front of the PI first.

---

## 5. Promiscuity — where "the cognate Gα" is not well defined

**39 of 64 receptors have a single primary family; 25 do not.** Beyond that, a
*secondary* transducer is annotated for the great majority: taking every family
annotated as a transducer at all, **55 of 64** receptors have more than one.

Receptors flagged `cognate_ambiguous` **because the primary is agreed but a
second transducer is annotated** (31 of them) are the cheap case — one family to
supply, and the ambiguity costs nothing at any rung. Receptors with **more than
one primary-candidate family** (25) are the expensive case: their bytes differ at
every rung.

**Receptors where a PI decision or a per-family arm is genuinely required** —
more than one family called primary, and no structure to break the tie, or a
structure that contradicts:

The 25 multi-primary receptors are **5HT2C, AA1R, AGTR1, B1B1U5, C5AR1, CCKAR,
CCR6, CNR1, EDNRA, EDNRB, FSHR, GHSR, GPR52, GPR6, HRH2, LPAR1, LT4R1, MCHR1,
NK1R, NTR1, OX2R, OXYR, PE2R4, S1PR5, TA2R**. Fourteen of them are the
`cognate_conflicted` set of §4 and already carry a recommendation there; the
remaining **eleven are `cognate_ambiguous` only because the authorities tie** —
AGTR1, B1B1U5, EDNRB, FSHR, GPR6, LPAR1, LT4R1, MCHR1, OX2R, OXYR, S1PR5 — and
for these the tie is resolved by the deposited structure in every case except
**B1B1U5**, whose two references disagree with each other (§8).

**Shortlist for the PI, in priority order:** the three annotation-vs-structure
splits **CCKAR, GHSR, NTR1** (Option A and Option B give different answers);
then **PE2R4**, whose two active references contain different Gα families; then
**NK1R**, where structure says Gs and the only assay lab says Gq/11; then
**B1B1U5** and **OPSD**, which have no annotation authority at all (§8).

---

## 6. What each active reference actually contains

Read from the deposited sequences of **440 polymer entities** across the 91
active reference PDBs. This is the part that is independently checkable and it is
the strongest evidence available.

| entity kind | count |
|---|---:|
| receptor | 83 |
| G-beta | 82 |
| G-gamma | 76 |
| **G-alpha** | **75** |
| nanobody / antibody / Fab / megabody / scFv | 75 |
| ligand peptide | 26 |
| fusion partner (T4L, BRIL, rubredoxin, PGS) | 8 |
| **G-alpha fused to another chain** | **6** |
| arrestin | 1 |

**81 Gα chains in total** (75 standalone + 6 fused). Of these:

- **20 are mini-G** — under 300 aa where the full subunit is 350–395.
- **12 are coupling chimeras** — the scaffold is one family and the α5 tip
  another, so the UniProt cross-reference names the wrong family. Eleven are
  caught by the two-window test, the twelfth (B1B1U5/9EPP) by the
  xref-vs-C-terminus test.
- **6 are fused to another chain**, most notably **OXYR / 7RYC**, whose Gα is a
  326-residue **Gγ2–Gαi2–Gαs fusion**. Because its description begins "…subunit
  gamma-2…", a classifier that matches "subunit gamma" first files it as a G-γ
  and OXYR then looks as though its active reference contains no G protein at
  all. That is exactly the trap `verify_partner_chains.py` documents for G-γ C68S
  and it bit again here in a new place; fixed, and the fix is commented in
  `coupling_assign.py`.
- **AA2AR / 5G53** contains "ENGINEERED DOMAIN OF HUMAN G ALPHA S LONG ISOFORM" —
  no "subunit alpha", no "nucleotide-binding", so it fell through to `other` on
  the first pass and 5G53 also looked transducer-free. It is mini-Gs.

### The twelve chimeras, one line each

The accession names the scaffold; the C-terminus names the coupling.

| receptor | PDB | UniProt xref | len | deposited last 11 | family by C-terminus | caught by |
|---|---|---|---:|---|---|---|
| 5HT2A | 8UWL | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| 5HT2C | 8DPF | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| ADA1A | 7YM8 | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| ADA1A | 8THK | P04899;P50148;P63092 | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| B1B1U5 | 9EPP | P63096 | 352 | `LQNNLKECNLV` | G11/Gq | xref-vs-C-term |
| DRD4 | 8IRU | none | 361 | `IKMNLRDCGLF` | Gi1/Gi2/Gt1/Gt2 | two-window |
| EDNRA | 8HCQ | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| GRPR | 8H0Q | P63092;P63096 | 361 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| HRH1 | 8YN2 | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| OX2R | 7L1V | none | 244 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| OXYR | 7RYC | none | 326 | `LQMNLREYNLV` | G11/G14/Gq | two-window |
| TA2R | 8XJN | none | 246 | `LQMNLREYNLV` | G11/G14/Gq | two-window |

Note **GRPR/8H0Q**: cross-referenced to **GNAS** (P63092) and GNAI1, described
"G-alpha q", and its deposited α5 tip is the Gq-family chimera tip. Three
different answers on one chain, and only the sequence is load-bearing.

### The finding I did not expect, and it matters most for this paper

**13 of the 81 deposited Gα α5 tips are not any canonical human Gα sequence.**

| deposited last 11 | count | nearest canonical | substitutions |
|---|---:|---|---:|
| `LQMNLREYNLV` | 10 | G11 (= Gq) | 2 |
| `LQNNLKECNLV` | 1 | G11 (= Gq) | 2 |
| `IKMNLRDCGLF` | 1 | Gi1 (= Gi2) | 2 |
| `VLEDLKSCGLF` | 1 | Gt1 (= Gt2) | 4 |

**Ten receptors have an engineered α5 tip in *every* one of their active
references**: 5HT2A, 5HT2C, ADA1A, DRD4, EDNRA, HRH1, OPSD, OX2R, OXYR, TA2R.

For a paper whose title is about the α5 C-terminus, this is not a footnote. If we
supply wild-type human Gq `LQLNLKEYNLV` and score against a reference whose
partner tip is `LQMNLREYNLV`, we are not reproducing the reference — we are
comparing a third thing to it. **No existing audit catches this**, because
`verify_partner_chains.py` compares a partner against *its own accession*, and
these chimeras carry no UniProt cross-reference at all: they return
`NO-UNIPROT-XREF`, which is flagged, not decoded.

**OPSD/4X1H deserves its own line.** Its "Gα" entity is an **11-residue peptide**
— which is to say the PDB already contains an `R1_ct11` complex of exactly the
kind the ladder builds. Its sequence is `VLEDLKSCGLF`, the engineered
high-affinity Gαt C-terminal analogue: **4 substitutions from wild-type Gt1
`IKENLKDCGLF`**. This confirms and sharpens Block D caveat D-B-9. It is also the
single best positive control available to the redo, and it must be supplied and
labelled as the analogue, not as "Gt".

### Active references with no Gα at all

| receptor | active PDB | what is in it instead |
|---|---|---|
| **OPRM** | 5C1M, 8E0G | **Nanobody 39 only** — OPRM has *no* Gα in any of its active references, so it has no structural authority at all |
| AA2AR | 8WDT | Fab heavy + light |
| ACM2 | 6U1N | **β-arrestin-1** + Fab30 (the only arrestin complex on the panel) |
| ADRB1 | 7BU7 | camelid antibody fragment |
| ADRB2 | 4LDE | Nb80 |
| AGTR1 | 6OS2 | Nb.AT110i1 + TRV026 peptide |
| CNR1 | 5XRA | receptor alone (agonist-bound, no transducer) |
| NTR1 | 8JPF | receptor + NTS only |
| OPRD | 6PT2 | receptor + peptide agonist only |

These receptors still have a Gα-containing active reference *somewhere* in the
list except **OPRM**, which does not. Each of them is a reminder that "active
reference" and "G-protein complex" are not the same predicate, and the run
manifest should carry which one a row was scored against.

---

## 7. Rung impact — exactly which rungs an ambiguous assignment touches

This is the reframe the brief asked for, quantified.

**Confirmed, from `seq_rungs.tsv` by hash, 16 human Gα × 7 rungs:** at every
peptide rung (`R1_ct11`, `R2_ct15`, `R3_ct21`, `R4_a5helix`, `R5_a5plus`) the
byte-identical groups are exactly **Gi1≡Gi2**, **Gt1≡Gt2≡Ggust**, **Gq≡G11**, and
no others. At `R7_full` no two families are identical.

| rung | length supplied | receptors whose bytes differ under their **primary** candidate set | under **every annotated** family |
|---|---|---:|---:|
| `R1_ct11` | all 11 aa | 25 / 64 | 55 / 64 |
| `R2_ct15` | all 15 aa | 25 | 55 |
| `R3_ct21` | all 21 aa | 25 | 55 |
| `R4_a5helix` | all 26 aa | 25 | 55 |
| `R5_a5plus` | all 36 aa | 25 | 55 |
| `R6a_da5` | **324–368 aa (spread 44)** | 25 | 55 |
| `R7_full` | **350–394 aa (spread 44)** | 25 | 55 |

**What this actually says, and it is not what I expected going in.** The number
of *affected receptors* is the same at every rung — a family choice changes the
bytes wherever it is expressed. What changes with the rung is the **cost of not
choosing**: at every peptide rung all candidate arms are the *same length*, so a
hedged arm is the same size as the one it hedges; only at `R6`/`R7` does the
second arm become a different and larger job (up to 44 extra residues, and the
full subunit is 32–36× the length of the 11-mer).

So the correct statement for Methods is **not** "ambiguity is free at peptide
length" but:

> An ambiguous coupling assignment changes the supplied sequence at every rung.
> What is free at peptide length is **hedging it** — running both candidate
> families costs one extra arm of identical size. At full-subunit length the same
> hedge costs an arm ~32–36× larger. The ladder should therefore hedge below `R6` and
> commit above it, and the commitment should be recorded per row.

**31 of the 56 non-confident receptors are immune anyway**, because their
primary-candidate set is a single family — their ambiguity is about *secondary*
transducers, which changes nothing we supply.

### Correction to `SEQUENCES.md` §3.2

`SEQUENCES.md` §3.2 states, after correctly establishing Gi1≡Gi2, Gt1≡Gt2≡Ggust
and Gq≡G11 at peptide length:

> *"Below `R6`, the only coupling decision that can possibly change the supplied
> bytes is the **family**."*

**The three equivalences are correct and I reproduce them exactly. The
generalisation drawn from them is not.** Recomputed per family, at both `R1_ct11`
and `R3_ct21`:

| family | subtypes | distinct sequences | the groups |
|---|---:|---:|---|
| Gs | 2 | **2** | `Gs` \| `Golf` |
| Gi/o | 8 | **5** | `Gi1=Gi2` \| `Gi3` \| `Go` \| `Ggust=Gt1=Gt2` \| `Gz` |
| Gq/11 | 4 | **3** | `Gq=G11` \| `G14` \| `G15` |
| G12/13 | 2 | **2** | `G12` \| `G13` |

A **subtype** decision inside Gi/o has five possible answers at `ct11`, and Gi1
vs Go differ at 6 of 21 positions. The sentence holds only once the subtype has
already been fixed to one of those equivalence classes. Proposed replacement,
for the lit/orchestrator session to apply — **I have not edited `SEQUENCES.md`**:

> Below `R6`, the coupling decision changes the supplied bytes at both the family
> and the subtype level. What the three equivalences buy is narrower and still
> useful: **Gi1 vs Gi2, Gt1 vs Gt2 vs Ggust, and Gq vs G11 are unobservable at
> peptide length**, so those three ambiguities — and only those — can be left
> unresolved.

### And the subtype problem is worse on this panel than in the corpus

`pandyszekeres2024gproteindb` p.8 reports **22%** three-dataset agreement on the
primary *subtype*. On our 64: of the **37** receptors where two or more assay
labs both name a primary subtype, **32 (86%)** name different ones. Examples:
ACM2 GoB vs GoA; ADA2A Gi1 vs Gz vs GoA; TA2R G12 vs Gq vs G13.

**A concrete gap this exposes, and what it costs under R-COG.** The subtype most
often named primary by the assay labs on this panel is **GoA (25 receptors)**,
with **GoB** named for 7 — **32 receptors between them**, and neither label
exists in `seq_rungs.tsv`, which carries a single `Go` row keyed to P09471
canonical.

**Under the structure rule this is no longer blocking, and that is worth saying
explicitly.** R-COG never consults the assay-lab subtype annotation, so `GoB` is
never requested: all **five** receptors that resolve to Go (5HT1B, ACM2, ADA2A,
CCR6, DRD2) match the **GoA** sequence, which is what `seq_rungs.tsv`'s `Go`
already is (P09471-1). Checked, not assumed — GoB's ct21 is 4 substitutions from
GoA's and none of the five deposited entities is closer to GoB.

Two things are still owed to `seq_rungs.tsv`, and the Group 1 session owns that
file:

1. **Rename `Go` to `GoA`, or document that `Go` means the P09471-1 isoform.**
   The bare label is ambiguous in a panel where the annotation vocabulary
   distinguishes GoA from GoB, and an ambiguous partner label is precisely the
   trap `SEQUENCES.md` §3.4 documents. Zero sequence change; it is a rename.
2. **Add `GoB` only if a subtype-contrast arm is wanted.** It is not needed by
   R-COG. If it is wanted, the construct is fully specified — P09471-2, 354 aa,
   and the rungs are:

   | rung | len | sequence |
   |---|---:|---|
   | `R1_ct11` | 11 | `IAKNLRGCGLY` |
   | `R2_ct15` | 15 | `TDVIIAKNLRGCGLY` |
   | `R3_ct21` | 21 | `FVFDAVTDVIIAKNLRGCGLY` |
   | `R4_a5helix` | 26 | `TNNIQFVFDAVTDVIIAKNLRGCGLY` |
   | `R5_a5plus` | 36 | `IYTHVTCATDTNNIQFVFDAVTDVIIAKNLRGCGLY` |
   | `R7_full` | 354 | P09471-2 canonical |

   GoA vs GoB is **1 substitution at `ct11` and 4 at `ct21`** — a natural
   within-family minimal pair, and a cheaper one than the Gi/Gt pair catalogue
   item E1.6 uses, since both members are human and both are *bona fide* primary
   transducers on this panel.

---

## 8. Species — three receptors, three different problems

| receptor | species | annotation authority | structural authority | status |
|---|---|---|---|---|
| **OPSD** | *Bos taurus* | **none** — IUPHAR 404s on P02699, GproteinDb has no bovine row; human RHO P08100 was queried as a fallback and also returns no transduction record | 4X1H, engineered Gt 11-mer | **one authority only.** Gt is not in doubt biologically, but it is not in either database in a form we can cite per row |
| **OPRM** | *Mus musculus* | IUPHAR via human ortholog **P35372** (recorded in `coupling_gtopdb.csv` as `ortholog_note`), GproteinDb via the same | **none** — both active references are Nb39 complexes | annotation-only receptor |
| **B1B1U5** | *Hasarius adansoni* (jumping spider) | **none at all** — no IUPHAR target, no GproteinDb row, no human ortholog | 9EPP and 9EPR, and they **disagree** | **see below** |

### B1B1U5 — the structures answer the question `SEQUENCES.md` §3.3(a) left open

`SEQUENCES.md` §3.3(a) flags Kumopsin1 as *"the single least defensible construct
on the panel"* — Block B assigns it cognate **Gi** with secondary Gq, and
invertebrate visual opsins are canonically Gq. **Its own two active references
settle it, and nobody had looked:**

| PDB | Gα chain | UniProt xref | len | deposited last 11 | family by C-terminus |
|---|---|---|---:|---|---|
| **9EPP** | "G(i) subunit alpha-1" | **P63096 (GNAI1)** | 352 | **`LQNNLKECNLV`** | **G11/Gq**, 9 of 11 |
| 9EPR | "G(i) subunit alpha-1" | P63096 (GNAI1) | 357 | `IKNNLKDCGLF` | Gi1/Gi2, 11 of 11 |

**9EPP is a Gi backbone carrying a Gq-family α5 tip** — a coupling chimera, and
the accession names the backbone. So the depositors built a Gq-tipped construct
for this receptor on purpose. Supplying **human GNAI1 and calling it cognate**,
as Block B did, is contradicted by the receptor's own structure.

This does not by itself decide the assignment — the pair 9EPP/9EPR is itself a
disagreement and I am reporting it rather than resolving it — but it converts the
question from "we have no authority" to "we have structural evidence, and it
points at Gq". **Recommendation: either supply a Gq-family rung for B1B1U5 and
record the 9EPP chimera as its basis, or drop the receptor.** Do not supply GNAI1
under the label "cognate".

**Cross-species rows generally.** `SEQUENCES.md` §3.3 asks for
`cross_species_partner` on every row and that request stands unchanged. Note only
that at `R1`-`R5` the OPSD case is species-invariant — confirmed independently
here by fetching both: human GNAT1 P11488 and bovine GNAT1 P04695 are both 350 aa
and their last 36 are byte-identical (`IYSHMTCATDTQNVKFVFDAVTDIIIKENLKDCGLF`) — so the species column is a `R6`/`R7` problem, while
the **engineered-analogue** problem in §6 is an `R1`–`R5` problem.

---

## 9. The prior assignment, audited against its own references

Block B's 40-row cognate table (`data/block_b/02_constructs/construct_build_report.md`
lines 33–72) is the only surviving trace of `refs/gpcr_coupling.csv`, which ships
in no drop. It is parsed by `coupling_assign.py` and diffed here.

- **40 of 40** Block B cognate families are among the families some authority
  calls primary. The prior is not reckless.
- **37 of 40** match the Gα actually deposited in the receptor's active reference.
- **3 of 40 contradict it:**

| receptor | Block B says | the active reference actually contains |
|---|---|---|
| **CCKAR** | Gq | **Gs** (7MBX, full GNAS heterotrimer) |
| **EDNRB** | Gq | **Gi1** (8IY5) |
| **GHSR** | Gq | **Gi1** (7NA7 and 7NA8, both) |

For those three, Block B's cognate arm supplied one family while the reference
its state predicate is calibrated on contains another. That is an internal
mismatch of exactly the kind the brief asked me to look for, and it is present in
the shipped 40-receptor panel, not only in Block D.

---

## 10. Two label-vs-identity traps, re-verified

Both are in `SEQUENCES.md` §3.4; both hold, and one gains a detail.

1. **`alpha13` filed under class label "G12".** Confirmed independently here from
   the rung table: `G12` and `G13` are distinct at every rung (`LQENLKDIMLQ` vs
   `LHDNLKQLMLQ` at `ct11`). Nothing new to add; the correction stands.
2. **Block D's four `cognate_ga` arms all supplied `alphas`.** §11.

---

## 11. Block D's four D2 receptors — cross-check, and what to tell `paper_af3`

### What the drop records

`data/block_d/06_gate_reports/GATE_1_D2_NB_SHA.md` lines 35–44 and
`data/block_b/02_constructs/d2_arm_sequence_audit.csv` both record
`partner_identity = alphas` on the `cognate_ga` arm of **all four** D2 receptors.

### What this analysis says the cognate is

| receptor | verdict | authorities' primary | deposited active reference | Block B's own table | D2 supplied | cognate? |
|---|---|---|---|---|---|---|
| **ADRB2** | ambiguous | **Gs** (4 assay labs + GtoPdb + IUPHAR) | 8GG0 **Gs** | Gs | `alphas` | **yes** |
| **ACM2** | ambiguous | **Gi/o** (Bouvier, Martemyanov, GtoPdb, IUPHAR) | 7T94 **Go** | Gi | `alphas` | **no** |
| **AGTR1** | ambiguous | **Gq/11** (Bouvier, Lambert) | 7F6G **Gq/G11** | Gq | `alphas` | **no** |
| **OPRK** | ambiguous | **Gi/o** (Bouvier, Martemyanov, GtoPdb, IUPHAR) | 8FEG **Gi1** | Gi | `alphas` | **no** |

**Three of four D2 "cognate" arms are not cognate under any authority I can find
— including Block B's own coupling table.**

### Is `alphas` a generic label or a literal sequence key? The drop leans one way

`SEQUENCES.md` §3.4 says this cannot be told apart from the drop, because the D2
audit's `consumed_sequence_sha256` reads `unknown (partner_type=apo or g_alpha)`
on exactly those rows. That remains true — **the Gα chains were never hashed**,
only the nanobody chains were. But two pieces of evidence in the drop point the
same way and should be stated:

1. **`alphas` is one of seven named entries in a partner FASTA.**
   `data/block_d/02_caveats/C-D-4_partners_fasta_nb60_mislabel.md` lines 13–14:
   *"`docs/EXPERIMENT_CATALOG/sequences/partners.fasta` … is set up for Gα family
   partners: **alphas, alphai1, alphaq, alpha13, alphagust**, GP161,
   arrestin_FL."* A file that carries five distinct Gα entries under five
   distinct keys is a sequence lookup, not a generic label vocabulary.
2. **Block B uses the same three slugs for three different accessions** —
   `construct_build_report.md` lines 25–27 maps `alphas`→P63092,
   `alphai1`→P63096, `alphaq`→P50148, each with a different α5-CT.

**So the probable reading is that GNAS was literally supplied to a Gi receptor, a
Gq receptor and another Gi receptor**, and Block D's F1 positive control is not
what it says it is. It is not proof. `manifest_input_sha_first_seed` differs
across the four receptors, but that hash covers the whole input YAML including
the receptor chain, so it has **no** discriminating power on the partner — which
is worth saying explicitly, because it is the one column that looks as if it
might settle the question.

### If Gs really was supplied, the result is more interesting, not less

Block D's `SC-D-4` / `F1`: cognate_gα reaches ≥96% predicate-active on **14 of
16** (receptor × backbone) cells; both misses are OpenFold3 — **ACM2 58%** and
**OPRK 36%** (`data/block_d/07_partA/PARTA_D2.md` §F1). Every non-OF3 cell is
100%.

- The two misses are **two of the three non-Gs receptors**. That is the direction
  a cognate-specificity effect would predict.
- But **AGTR1 — also non-Gs — hits ≥96% on all four backbones**, and ADRB2, the
  only genuinely-cognate receptor, is not distinguishable from it.

So the evidence cuts both ways and **the honest reading is that F1 does not
currently measure what it claims**: it measures the effect of supplying *a* Gα, and on
three of four receptors that Gα was probably the wrong one. Whether the effect is
cognate-specific is **undetermined by Block D** and is a good, cheap experiment
for the redo: the same four receptors × {true cognate Gα, Gs, shuffled} is 12
cells on already-built machinery.

### Paste-ready for `paper_af3`

> **D2 `cognate_ga` arm — three of four receptors look non-cognate.**
> `GATE_1_D2_NB_SHA.md` lines 35–44 and `d2_arm_sequence_audit.csv` both record
> `partner_identity = alphas` for ADRB2, ACM2, AGTR1 and OPRK. Independently
> checked against GproteinDb (Bouvier/Inoue/Martemyanov/Lambert biosensor
> datasets), IUPHAR/GtoPdb fetched direct, and the deposited Gα chain of each
> receptor's own active reference: **ACM2 is Gi/o (7T94 contains GNAO1), OPRK is
> Gi/o (8FEG contains GNAI1), AGTR1 is Gq/11 (7F6G contains GNAQ/GNA11)**. Block
> B's own coupling table (`construct_build_report.md` lines 33–72) says the same:
> ACM2→Gi, OPRK→Gi, AGTR1→Gq. Only ADRB2 is Gs.
>
> **Confidence: high that the manifest column is wrong or the arm is
> mis-specified; moderate that GNAS was literally the sequence supplied.** The
> literal-sequence reading is supported by `partners.fasta` carrying five
> distinct Gα entries under the keys `alphas / alphai1 / alphaq / alpha13 /
> alphagust` (C-D-4 lines 13–14), and by Block B mapping those same three slugs
> to three different accessions. It cannot be confirmed from the drop because the
> Gα chains were never hashed —
> `consumed_sequence_sha256 = unknown (partner_type=apo or g_alpha)` on exactly
> these rows. **`manifest_input_sha_first_seed` does not settle it**: it covers
> the whole input file including the receptor, so it differs between receptors
> regardless of the partner.
>
> **Two asks, both free.** (1) `sha256` of the chain-B sequence actually consumed
> by one representative input per `(receptor, cognate_ga, backbone)` cell — 16
> hashes, from files already on HPC. (2) `partners.fasta` itself, or the five Gα
> entries' hashes, so the slugs can be resolved to sequences.
>
> **Why it matters beyond bookkeeping.** If GNAS was supplied, then three non-Gs
> receptors still reached ≥96% active on 10 of their 12 cells, which is evidence
> the Gα-drives-active effect is **not cognate-specific** — a substantive result
> and a reason to run {cognate, Gs, shuffled} × 4 receptors before any sentence
> calls the Gα arm a "cognate" positive control. Both misses (OF3 ACM2 58%, OF3
> OPRK 36%) are non-Gs receptors, but so is AGTR1, which does not miss.

---

---

## 12. What is still open after the decision

The structure rule closed four of the six items that stood here before it. What
it closed and what it did not:

**Closed by R-COG.**

- *OPSD's single authority.* Still one authority, but the rule now says exactly
  what that authority yields and with what margin — Gt1, family unambiguous at
  4-vs-7 substitutions, `frozen_with_caveat` (§14.3). It is no longer an open
  question, it is a labelled one.
- *B1B1U5's contradictory references.* Rule R picks 9EPP, so the rule resolves it
  to Gq and records the prior reversal (§14.4). Conditional on the panel session
  not changing that reference — see below.
- *PE2R4's two active references.* Rule R picks 8GDB, so the answer is Gs. The
  disagreement is recorded but no longer blocks.
- *The GoA/GoB gap.* Not blocking under R-COG, because the rule never consults
  the subtype annotation; all five Go picks are GoA, which is what
  `seq_rungs.tsv` already carries. Two items still owed to that file, specified
  in §7.

**Still open, and each needs someone else's decision.**

1. **The ten chimeric tips** (§14.2). The rule declines them by design. Two
   options per receptor plus a `DEPOSITED_TIP` control arm; **four are in the
   provisional CORE-32** — 5HT2A, GRPR, OX2R, OXYR — so this is on the critical
   path, not a tail case.
2. **B1B1U5's reference is contested between two files.** `panel_systems.csv`
   and `PANEL.md`'s Rule R disagree about which 9EP\* entry is active, and the
   two entries give **different families**. The map follows Rule R (9EPP → Gq).
   **If the panel session settles on 9EPR, B1B1U5 flips to Gi1 and the map must
   be rebuilt.** This is the one row whose answer depends on an unsettled
   decision in another session's file.
3. **OPRM has no structural authority at all.** Both its active references are
   Nb39 complexes, so its `Gi1` is annotation-only and nothing structural checks
   it — the only one of the six convention rows with no corroborating structure
   anywhere (§14.5).
4. **NTR1's fallback family comes from a non-Rule-R structure**, against a
   unanimous Gq/11 annotation (§14.5). Defensible, but it is the one convention
   row where the convention contradicts every database, and a PI should see it.
5. **The tie representatives bind at `R6a_da5` and `R7_full`** for 32 of the 54
   resolved receptors (§0a). Declared rather than derived; if the PI would rather
   resolve Gi1-vs-Gi2 by annotation than by declaration, only the two longest
   rungs change.
6. **Option A removes partner identity as a measured axis** (§0b), so the Block D
   question in §11 — is the Gα effect cognate-specific at all? — is not answered
   by Group 1 under this rule and needs its own arm.
7. **The `chiesa2025templatebias` "nine Gα subtypes across 145 structures"
   figure** is quoted from lit's writeup; I did not reconstruct it and it
   supports no number in this file.

---

## 13. Files written, and how to reproduce

All writes are `redo/spec/COUPLING.md` plus `coupling_`-prefixed companions.
Nothing else was touched; no git was run; `data/block_*/` was read only.

| file | what it is | rows |
|---|---|---:|
| `COUPLING.md` | this document | — |
| **`coupling_cognate_map.tsv`** | **the frozen map.** One row per receptor, keyed `receptor_slug`; carries `cognate_subtype`, `seq_rungs_family`, `rule_r_active_pdb`, `source_entity`, `deposited_ct11`/`ct21`, `evidence_class`, `verdict`, tie set, chimera options, `alt_*`, `reverses_prior` | **64** |
| **`coupling_cognate_rungs.tsv`** | **receptor × rung → `sha256`, `len`, `sequence`**, lifted from `seq_rungs.tsv`. Emitted only for resolved receptors, so a consumer joining on it cannot hash an unresolved one | **378** |
| **`coupling_receptor_sets.tsv`** | the family partitions of C1-64 and of CORE-32, for the two templated receptor sets in `g1_systems.csv` (§14.6) | **82** |
| `coupling_cognate_map.py` | builds both, implements R-COG-1..8; `--selftest` plants an input for every branch and cross-checks the entity classifier against `coupling_assign.py` | — |
| `coupling_fetch.py` | network: GproteinDb couplings, IUPHAR transduction, RCSB GraphQL, UniProt family termini | — |
| `coupling_assign.py` | no network: entity classification, α5-CT family calls, verdicts, rung impact | — |
| `coupling_summary.py` | recomputes every number quoted above; `--selftest` plants a defect in each of its four checks | — |
| `coupling_assignments.csv` | the verdict table, one row per receptor, 27 columns | 64 |
| `coupling_refstructures.csv` | every polymer entity of every active **and** inactive reference, classified, with the deposited α5 tip | 590 |
| `coupling_rung_impact.csv` | per receptor × rung, whether the candidate families put different bytes on the wire, under both the primary and the all-annotated candidate set | 64 |
| `coupling_gproteindb.csv` | GproteinDb couplings rows for the C1 accessions, one per receptor × source lab | 263 |
| `coupling_gtopdb.csv` | IUPHAR transduction per receptor, with the ortholog substitution recorded where one was used | 64 |
| `coupling_rcsb_entities.json` | raw RCSB GraphQL cache, 189 entries | — |
| `coupling_family_termini.json` | the 16 canonical human Gα C-termini used for family calls | 16 |

```bash
python3 redo/build/coupling_fetch.py         # network; ~3 min, caches the 9 MB couplings page
python3 redo/build/coupling_assign.py        # no network
python3 redo/build/coupling_cognate_map.py   # the frozen map -- run after assign
python3 redo/build/coupling_summary.py       # prints every number in this file

python3 redo/build/coupling_cognate_map.py --selftest
python3 redo/build/coupling_summary.py --selftest
```

**For `g1_systems.py`.** Join `g1_systems.csv:receptor_slug` to
`coupling_cognate_map.tsv:receptor_slug`. For a row with
`chain_b_family_rule = COGNATE`, take `seq_rungs_family` and look up
`(receptor_slug, rung)` in `coupling_cognate_rungs.tsv` for `sha256` and `len`.
**Rows whose `verdict` is `needs_decision` have no `seq_rungs_family` and appear
in neither rung file** — they must stay `PENDING` until §14.2 is decided, and a
preflight check that they do is worth having.

### Six defects found in my own work, recorded so they cannot recur

Per the project's rule that the first run is wrong before the drop is:

1. **Family lists joined with `/`.** `Gi/o` and `Gq/11` contain a slash, so a
   `/`-joined list split back into `Gi`, `o`. This produced a confident-looking
   "an ambiguous assignment changes the bytes at **zero** of seven rungs" — the
   exact opposite of the truth — and a 35-receptor "GtoPdb omits Gi/o" finding
   that does not exist. Separator is now `;` between families and `+` inside a
   per-lab cell.
2. **The IUPHAR parser matched the rendered form.** `G<sub>i</sub>/G<sub>o</sub>`
   strips to `G i /G o`, so patterns written as `Gi/Go` matched nothing and the
   parser returned an empty family list for essentially every receptor. Because
   an empty list is simply one fewer authority, **nothing failed and nothing was
   reported** — the silent-check failure mode. `coupling_assign.py` now asserts
   that no receptor has non-empty IUPHAR text and zero parsed families, and
   `--selftest` plants a defect in each of the four downstream checks.
3. **The 64-row table in §3 was first written out by hand.** Diffing it against
   the generator found **27 wrong cells in 66 lines** — a receptor's verdict
   flipped (OX2R written `CONFLICTED`, actually `ambiguous`), a lab's answer
   swapped (EDNRA Martemyanov written Gq/11, actually Gi/o), a reference added
   that belongs to a different receptor (6GDG under AA1R), and a Gα subtype
   wrong (SSR2/7T10 written Gi1/Gi2, actually Gi3). The table in this file is now
   **spliced verbatim from the CSVs by script**, and the splice can be re-run.
   No table of 64 rows should be typed.

4. **My canonical-Gα accession table had the wrong protein under `Ggust`.**
   `coupling_fetch.py` carried its own accession→family map, copied from
   `verify_alpha5ct_family.py`, listing Ggust as **P29033 — which is Gap junction
   beta-2 protein (Connexin 26)**, not gustducin (human GNAT3 is `A8MTJ3`, which
   is what `seq_rungs.tsv` uses). It also listed Gt1 as bovine P04695 where
   `seq_rungs.tsv` uses human P11488. **The failure mode is the nastiest in this
   document**: a wrong C-terminus can only ever *fail* to match, so Ggust simply
   never appeared in any tie set and every report looked clean. Caught by
   diffing against the Group 1 session's `g1_refchimera.tsv`, which had it right.
   Effect: tie sets under-reported Ggust in two places (OPSD, DRD4); no family
   call, verdict or receptor-level conclusion changed. **Fix: the canonical
   termini are now read from `seq_rungs.tsv` and from nowhere else**, so the
   family label this file emits is a valid join key into the rung table by
   construction rather than by coincidence.

5. **The map emitted no rung rows for the six convention receptors.** They have a
   resolved subtype, so a consumer joining on `coupling_cognate_rungs.tsv` would
   have found nothing and silently dropped six receptors. Caught by the
   `--selftest` assertion that every row with a `seq_rungs_family` has rung rows
   — an assertion written *before* the bug existed, which is the only reason it
   fired.

6. **Unequal authority sets treated as disagreement.** A tie is lower resolution,
   not a contradiction; the first rule filed EDNRB, FSHR, MCHR1 and others as
   `conflicted`. `conflicted` now requires two authorities to be **disjoint**,
   which moved 10 receptors from `conflicted` to `ambiguous`.

---

## 14. The frozen map — every receptor, and the four cases that need handling

Built by `coupling_cognate_map.py` under the rule in §0a. `C32` marks the
provisional CORE-32. `id` is ct21 identity, or ct11 identity where the entity is
too short for ct21. A `—` subtype means the rule declined to resolve.

| # | receptor | C32 | Rule-R active | partner entity | len | deposited ct21 | id | subtype | evidence | verdict |
|---|---|---|---|---|---:|---|---:|---|---|---|
| 1 | 5HT1B | · | 6G79 | 6G79_3 | 225 | `VIFDAVTDIIIANNLRGCGLY` | 0.95 | **Go** | near | frozen |
| 2 | 5HT2A | Y | 8UWL | 8UWL_2 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 3 | 5HT2C | · | 8DPF | 8DPF_2 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 4 | 5HT5A | · | 7X5H | 7X5H_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 5 | AA1R | Y | 7LD3 | 7LD3_1 | 355 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 6 | AA2AR | · | 8WDT | — none — | — | — | — | **Gs** | **convention** | frozen_by_convention |
| 7 | ACM1 | · | 6OIJ | 6OIJ_1 | 353 | `FVFAAVKDTILQLNLKEYNLV` | 1.00 | **Gq** | exact | frozen |
| 8 | ACM2 | · | 7T94 | 7T94_2 | 354 | `VVFDAVTDIIIANNLRGCGLY` | 1.00 | **Go** | exact | frozen |
| 9 | ACM4 | Y | 7TRP | 7TRP_5 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 10 | ADA1A | · | 7YM8 | 7YM8_1 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 11 | ADA2A | · | 7EJ8 | 7EJ8_1 | 354 | `VVFDAVTDIIIANNLRGCGLY` | 1.00 | **Go** | exact | frozen |
| 12 | ADRB1 | Y | 7BU7 | — none — | — | — | — | **Gs** | **convention** | frozen_by_convention |
| 13 | ADRB2 | · | 8GG0 | 8GG0_1 | 380 | `RVFNDCRDIIQRMHLRQYELL` | 1.00 | **Gs** | exact | frozen |
| 14 | AGTR1 | Y | 6OS2 | — none — | — | — | — | **Gq** | **convention** | frozen_by_convention |
| 15 | APJ | Y | 8XZH | 8XZH_2 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 16 | B1B1U5 | Y | 9EPP | 9EPP_2 | 352 | `FVFCAVKDTILQNNLKECNLV` | 0.86 | **Gq** | near | frozen |
| 17 | C5AR1 | Y | 7Y66 | 7Y66_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 18 | CCKAR | Y | 7MBX | 7MBX_1 | 394 | `RVFNDCRDIIQRMHLRQYELL` | 1.00 | **Gs** | exact | frozen |
| 19 | CCR2 | Y | 7XA3 | 7XA3_3 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 20 | CCR5 | · | 7O7F | 7O7F_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 21 | CCR6 | · | 6WWZ | 6WWZ_4 | 250 | `VIFDAVTDIIIANNLRGCGLY` | 0.95 | **Go** | near | frozen |
| 22 | CCR8 | · | 8KFX | 8KFX_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 23 | CNR1 | · | 8GHV | 8GHV_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 24 | CNR2 | Y | 8GUR | 8GUR_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 25 | CXCR2 | · | 6LFO | 6LFO_1 | 353 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 26 | CXCR3 | · | 8HNM | 8HNM_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 27 | CXCR4 | · | 8U4N | 8U4N_1 | 365 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 28 | DRD2 | · | 8TZQ | 8TZQ_5 | 354 | `VVFDAVTDIIIANNLRGCGLY` | 1.00 | **Go** | exact | frozen |
| 29 | DRD3 | Y | 8IRT | 8IRT_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 30 | DRD4 | · | 8IRU | 8IRU_1 | 361 | `RIFNDVTDIIIKMNLRDCGLF` | 0.71 | **—** | **chimera** | needs_decision |
| 31 | EDNRA | · | 8HCQ | 8HCQ_1 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 32 | EDNRB | Y | 8IY5 | 8IY5_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 33 | FSHR | · | 8I2G | 8I2G_1 | 259 | `RVFNDCRDIIQRMHLRQYELL` | 1.00 | **Gs** | exact | frozen |
| 34 | GHSR | Y | 7NA7 | 7NA7_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 35 | GPR52 | Y | 8HMP | 8HMP_5 | 249 | `RIFNDCRDIIQRMHLRQYELL` | 0.95 | **Gs** | near | frozen |
| 36 | GPR6 | · | 8TYW | 8TYW_3 | 394 | `RVFNDCRDIIQRMHLRQYELL` | 1.00 | **Gs** | exact | frozen |
| 37 | GRPR | Y | 8H0Q | 8H0Q_3 | 361 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 38 | HRH1 | · | 8YN2 | 8YN2_1 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 39 | HRH2 | · | 8YN3 | 8YN3_1 | 246 | `RIFNDCRDIIQRMHLRQYELL` | 0.95 | **Gs** | near | frozen |
| 40 | HRH3 | Y | 8YN5 | 8YN5_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 41 | LPAR1 | Y | 7TD0 | 7TD0_3 | 379 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 42 | LSHR | · | 7FII | 7FII_1 | 361 | `RIFNDCRDIIQRMHLRQYELL` | 0.95 | **Gs** | near | frozen |
| 43 | LT4R1 | Y | 7VKT | 7VKT_2 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 44 | MCHR1 | Y | 8WWK | 8WWK_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 45 | MTR1A | Y | 7VGY | 7VGY_2 | 353 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 46 | MTR1B | · | 7VH0 | 7VH0_2 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 47 | NK1R | Y | 8U26 | 8U26_1 | 248 | `RIFNDCRDIIQRMHLRQYELL` | 0.95 | **Gs** | near | frozen |
| 48 | NPY1R | Y | 7X9A | 7X9A_2 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 49 | NPY2R | · | 8K6N | 8K6N_1 | 355 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 50 | NTR1 | Y | 8JPF | — none — | — | — | — | **Gi1** | **convention** | frozen_by_convention |
| 51 | OPRD | Y | 6PT2 | — none — | — | — | — | **Gi1** | **convention** | frozen_by_convention |
| 52 | OPRK | · | 8FEG | 8FEG_1 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 53 | OPRM | · | 5C1M | — none — | — | — | — | **Gi1** | **convention** | frozen_by_convention |
| 54 | OPRX | · | 8F7X | 8F7X_3 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 55 | OPSD | Y | 4X1H | 4X1H_2 | 11 | `VLEDLKSCGLF` *(11-mer)* | 0.64 | **Gt1** | **peptide** | frozen_with_caveat |
| 56 | OX2R | Y | 7L1V | 7L1V_1 | 244 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 57 | OXYR | Y | 7RYC | 7RYC_3 | 326 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 58 | PD2R2 | Y | 8XXV | 8XXV_2 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 59 | PE2R4 | · | 8GDB | 8GDB_1 | 394 | `RVFNDCRDIIQRMHLRQYELL` | 1.00 | **Gs** | exact | frozen |
| 60 | S1PR1 | Y | 7TD4 | 7TD4_2 | 379 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 61 | S1PR5 | · | 7EW1 | 7EW1_3 | 354 | `FVFDAVTDVIIKNNLKDCGLF` | 1.00 | **Gi1** | exact | frozen |
| 62 | SSR2 | Y | 7T10 | 7T10_2 | 354 | `FVFDAVTDVIIKNNLKECGLY` | 1.00 | **Gi3** | exact | frozen |
| 63 | TA2R | · | 8XJN | 8XJN_1 | 246 | `RIFNDCKDIILQMNLREYNLV` | 0.62 | **—** | **chimera** | needs_decision |
| 64 | TSHR | Y | 7UTZ | 7UTZ_5 | 261 | `RIFNDCRDIIQRMHLRQYELL` | 0.95 | **Gs** | near | frozen |

### 14.1 Reading this table

**39 `STRUCTURE_EXACT`** — the deposited last 21 is a canonical human Gα
verbatim. **8 `STRUCTURE_NEAR`** — engineered, but every canonical at the best
score is in one family, so family and subtype are unambiguous. Seven of the eight
are the standard single-substitution mini-G scaffold: `RIFNDCRDIIQRMHLRQYELL`
(Gs, V→I, in GPR52, HRH2, LSHR, NK1R, TSHR) and `VIFDAVTDIIIANNLRGCGLY` (Go,
V→I, in 5HT1B and CCR6). The eighth is B1B1U5, §14.4.

**The rule changes six answers relative to §3's annotation-weighted table**, all
because Rule R picks a different active reference than the first-listed
candidate: DRD2 resolves to **Go** (8TZQ), not Gi1 (7JVR); SSR2 to **Gi3**
(7T10); ACM2 and ADA2A to **Go**; PE2R4's two-reference conflict resolves to
**Gs** (8GDB); and NTR1's annotation-vs-structure conflict is not resolved by a
structure at all, because Rule R picks 8JPF, which has no Gα (§14.5).

### 14.2 Case 1 — the ten chimeric tips, options presented and not chosen

These are the receptors where "read it off the structure" yields a **chimera**,
not a canonical subtype. In every case the construct is a mini-Gs scaffold
carrying a foreign α5 tip, so it spans two families and has **two honest
answers**. The rule marks them and stops. `option_backed_by_annotation` records
which option the coupling databases support — information, not a tiebreak.

| receptor | C32 | Rule-R ref | deposited ct21 | ct21 id | **A: tip** | **B: scaffold** | annotation backs | off-Rule-R alternative |
|---|---|---|---|---:|---|---|---|---|
| **5HT2A** | Y | 8UWL | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |
| **5HT2C** | · | 8DPF | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |
| **ADA1A** | · | 7YM8 | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | 8THK (also chimeric) |
| **DRD4** | · | 8IRU | `RIFNDVTDIIIKMNLRDCGLF` | 0.71 |  (Gi/o) | Gs (Gs) | A/tip | none |
| **EDNRA** | · | 8HCQ | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |
| **GRPR** | Y | 8H0Q | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | 7W40 Gq |
| **HRH1** | · | 8YN2 | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |
| **OX2R** | Y | 7L1V | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip+B/scaffold | none |
| **OXYR** | Y | 7RYC | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |
| **TA2R** | · | 8XJN | `RIFNDCKDIILQMNLREYNLV` | 0.62 |  (Gq/11) | Gs (Gs) | A/tip | none |

**What the construct is.** `RIFNDCKDIILQMNLREYNLV` is the published
mini-Gαs/q chimera: its first 10 read Gs (2 substitutions from
`RVFNDCRDII`) and its last 11 read Gq/G14 (2 substitutions from Gq's
`LQLNLKEYNLV`). It is **not any human Gα** — the nearest canonical over the whole
21 is 8 substitutions away. DRD4's `RIFNDVTDIIIKMNLRDCGLF` is the same idea with
a Gi/Gt tip (mini-Gαs/i).

**The consequence for a paper about the α5-CT, stated plainly.** For these ten
receptors, supplying the wild-type human tip and scoring against the deposited
reference is **not** reproducing the reference — the reference's own tip differs
from wild-type at 2 of 11. Option A supplies what the databases and the biology
say; Option B supplies what the scaffold says; **neither supplies what is
actually in the coordinate file.** A third option exists and the Group 1 session
has already built the arm for it — `g1_refchimera.tsv`, rungs `reftip_ct11` /
`reftip_ct21`, `family_rule = DEPOSITED_TIP` — which supplies the deposited
sequence itself. **Recommendation: Option A for the ladder (it is the biological
claim), with the `DEPOSITED_TIP` arm as the matched control on these ten.** The
choice is Aditya's; the rule does not make it.

### 14.3 Case 2 — OPSD, the case that proves the rule

Rule R selects **4X1H**, whose partner entity `4X1H_2` is an **11-residue
peptide**: `VLEDLKSCGLF`, the engineered high-affinity Gαt C-terminal analogue,
with **no UniProt cross-reference at all**. OPSD has **no α5 reference longer
than 11 residues anywhere in its reference set**.

So R-COG-6 applies, and here is exactly what it yields and how confident it is:

- Nearest canonical: **Gt1 / Gt2 / Ggust at 4 substitutions of 11** (identity
  0.64 — below the 0.80 threshold R-COG-5 would have used at ct21).
- **The nearest canonical of any other family is 7 substitutions away.** The
  margin is 4 vs 7, so the **family is unambiguous** even though the identity is
  low, and the tie is the Gt/Ggust class, whose members are byte-identical at
  every rung through `a5plus`.
- Resolved subtype **Gt1** (`P11488`, human GNAT1 — the record `seq_rungs.tsv`
  uses), verdict **`frozen_with_caveat`**, class **`PEPTIDE_ENTITY`**.
- It agrees with Block B's prior (`Gt`), which is the only receptor-level
  agreement that matters here since no database carries a transduction record for
  P02699 or for human RHO P08100.

**Why the family-level fallback would have been actively wrong, not merely
imprecise.** A `Gi/o → Gi1` fallback supplies `IKNNLKDCGLF`. The correct Gt1 tip
is `IKENLKDCGLF`. They differ at **exactly one residue, position 3 (N vs E)** —
and that single residue is what catalogue item **E1.6 / G12** exists to measure.
Falling back to the family representative would have run the one-residue
experiment **on the wrong residue**, and the arm would have looked like it worked.
This is the strongest argument in the whole document for `evidence_class` being a
column rather than a footnote.

**The caveat attached to `frozen_with_caveat`, and it bites only above `R5`.**
The deposited evidence is 11 residues long. Everything the rule says about OPSD
beyond position 11 — `R2`–`R7` — is an **extrapolation from the family call**,
not a structure read. At `R1_ct11` the supplied `IKENLKDCGLF` is 4 substitutions
from what 4X1H actually contains. Two things follow: any `R6`/`R7` OPSD arm
should be marked as extrapolated, and **the deposited 11-mer is itself the
natural positive control for `R1_ct11`** — it is the only receptor on the panel
whose reference *is* an α5-CT peptide complex at the ladder's shortest rung.

### 14.4 Case 3 — B1B1U5, a prior reversed in the open

Rule R selects **9EPP**. Its Gα entity `9EPP_2` is cross-referenced to **GNAI1
(P63096)** and described "G(i) subunit alpha-1", and its deposited last 21 is
`FVFCAVKDTILQNNLKECNLV` — **Gq/G11 at 0.86**, with the whole window reading
Gq-family (the scaffold is 1 substitution from Gq's `FVFAAVKDTI`, the tip 2 from
Gq's `LQLNLKEYNLV`). Because every canonical at the best score is in one family
and 0.86 ≥ 0.80, the rule **resolves it**: `Gq`, class `STRUCTURE_NEAR`, verdict
`frozen`.

**This reverses Block B**, which assigned Kumopsin1 cognate **Gi** with secondary
Gq and supplied human GNAI1. It is recorded in the map as
`reverses_prior = YES — Block B assigned Gi (Gi/o); the Rule-R structure reads
Gq/11`, and it is one of **four** such reversals:

| receptor | Block B assigned | Rule-R structure reads | evidence |
|---|---|---|---|
| **B1B1U5** | Gi | **Gq/11** | 9EPP, ct21 0.86 to Gq/G11 |
| **CCKAR** | Gq | **Gs** | 7MBX, ct21 1.00 to Gs |
| **EDNRB** | Gq | **Gi/o** | 8IY5, ct21 1.00 to Gi1/Gi2 |
| **GHSR** | Gq | **Gi/o** | 7NA7, ct21 1.00 to Gi1/Gi2 |

All four are visible rather than silent, which is the point. Note that the
B1B1U5 reversal is also the one that `SEQ_RECEPTORS.md` flags independently:
`panel_systems.csv:gdb_active` and Rule R disagree about which 9EP* entry is the
active reference, and the two entries give **different families** — 9EPP is the
Gq-tipped chimera, 9EPR is wild-type Gi1. Under Rule R it is 9EPP and therefore
Gq. **If the panel session changes B1B1U5's active reference to 9EPR, this row
flips back to Gi1 and the map must be rebuilt.** That dependency is real and is
recorded here rather than assumed away.

### 14.5 Case 4 — six receptors whose Rule-R reference has no Gα at all

These cannot be read off a structure. R-COG-7 gives them a **declared family
representative** and an evidence class that can never be confused with a
structure read.

| receptor | C32 | Rule-R ref | what is in it instead | family | subtype | off-Rule-R active with a Gα |
|---|---|---|---|---|---|---|
| **AA2AR** | · | 8WDT | Fab heavy + light chains | Gs | `Gs` | 6GDG → Gs |
| **ADRB1** | Y | 7BU7 | camelid antibody fragment | Gs | `Gs` | 8DCS → Gs |
| **AGTR1** | Y | 6OS2 | Nb.AT110i1 + TRV026 peptide | Gq/11 | `Gq` | 7F6G → Gq |
| **NTR1** | Y | 8JPF | receptor + neurotensin only | Gi/o | `Gi1` | 6OS9 → Gi1 |
| **OPRD** | Y | 6PT2 | receptor + peptide agonist only | Gi/o | `Gi1` | 8F7S → Gi1 |
| **OPRM** | · | 5C1M | Nanobody 39 only | Gi/o | `Gi1` | **none** |

**Five of the six are corroborated by a structure — just not by *the*
structure.** AA2AR/6GDG, ADRB1/8DCS, AGTR1/7F6G, NTR1/6OS9 and OPRD/8F7S each
contain a Gα that reads the *same* subtype as the fallback, so for those the
convention is a formality. **OPRM is the one that is not:** no active reference of
OPRM contains a Gα at all (both are Nb39 complexes), so its `Gi1` rests on
annotation alone and nothing structural checks it.

**One provenance point that must not be glossed.** The fallback family comes from
`recommended_family`, and for a `cognate_conflicted` receptor that value is
itself the deposited partner of a **non**-Rule-R reference, not an annotation
consensus. **NTR1 is exactly that case**: every annotation authority says Gq/11,
and the fallback gives **Gi/o**, off 6OS9. Calling that "the annotation
authorities" would be false, so the row carries `fallback_basis` naming where the
family actually came from. NTR1 is the sharpest remaining annotation-vs-structure
split on the panel (§4) and Option A resolves it toward the structure — by a
route that runs through a reference Rule R did not pick. **Worth a PI glance.**

### 14.6 The two templated receptor sets, and what I am deliberately not deciding

45 rows of `g1_systems.csv` carry `receptor_slug = *` because their **receptor
set** — not their partner — resolves from this file:
`CORE32_GS(PENDING COUPLING.md)` (9 rows, G18b, the mazzoni2000 matched peptides,
"Gs-coupled receptors only") and `G10_SCAN(PENDING COUPLING.md)` (36 rows, the
alanine scan and the Gi→Gs substitution series).

`coupling_receptor_sets.tsv` supplies **the partitions, not the set
definitions**:

| set | n | members |
|---|---:|---|
| `CORE32_Gs` | 5 | ADRB1, CCKAR, GPR52, NK1R, TSHR |
| `CORE32_Gio` | 21 | AA1R, ACM4, APJ, C5AR1, CCR2, CNR2, DRD3, EDNRB, GHSR, HRH3, LPAR1, LT4R1, MCHR1, MTR1A, NPY1R, NTR1, OPRD, OPSD, PD2R2, S1PR1, SSR2 |
| `CORE32_Gq11` | 2 | AGTR1, B1B1U5 |
| `C1_64_Gs` / `C1_64_Gio` / `C1_64_Gq11` | 12 / 39 / 3 | the same partition over all 64 |

**`CORE32_GS` is answered: it is `CORE32_Gs`, five receptors.** Note that this is
small, and two of the five are `frozen_by_convention` or a Block B reversal
(ADRB1 by convention, CCKAR reversed from Gq) — so a Gs-only arm on CORE-32 rests
on a narrow and partly non-structural base. Worth knowing before costing it.

**`G10_SCAN` I am not answering.** "Which receptors couple Gi" is this file's
question; "which of them the per-position scan should run on" is Group 1's, and
deciding the second while holding the first is the overreach the session split
exists to prevent. G10b is explicitly a Gi→Gs series, so `CORE32_Gio` is the
obvious candidate, but the arm's own note does not say the set equals the
partition and I will not assume it does.

---

## Questions for lit

1. **`chiesa2025templatebias` p.6302 picks the Gα from the deposited structure.
   Does it say anything about what to do when a receptor has two deposited
   active complexes with *different* Gα families?** PE2R4 has exactly that (8GCP
   Gi1, 8GDB Gs), and B1B1U5 has a near-miss version (9EPR wild-type Gi, 9EPP a
   Gq-tipped chimera). *Changes per answer:* if the paper has a rule we adopt it;
   if not, PE2R4 and B1B1U5 become PI decisions and §5's "PI decision" list grows
   by two.

2. **Does any corpus paper supply a mini-G or a coupling chimera as the
   co-folded partner, rather than a wild-type subunit?** Eleven of our active
   references contain chimeras and twenty contain mini-G. `pandyszekeres2024gproteindb`
   is quoted in lit's writeup as saying *"mini-G proteins and nanobodies appear
   only as…"* — the full sentence would settle it. *Changes per answer:* if the
   corpus supplies wild-type against chimeric references without comment, we can
   do the same and cite it; if not, we owe a caveat on ten receptors (§6) and
   possibly an arm that supplies the chimeric tip itself.

3. **Is the engineered high-affinity Gαt analogue `VLEDLKSCGLF` (OPSD/4X1H, 4
   substitutions from wild-type Gt1) named and characterised anywhere in the
   corpus?** *Changes per answer:* it is the only 11-residue α5-CT complex in our
   whole reference set and therefore the natural positive control for `R1_ct11`.
   If the corpus characterises its affinity relative to wild-type, we can say
   what the control demonstrates; if not, it is a construct we supply without
   knowing what it means.

4. **Does `miglionico2026atlas` report performance as a function of how
   *confidently* a receptor is coupled?** We have 8 confident, 42 ambiguous and
   14 conflicted receptors, and if confidence correlates with predictive success
   in their 10,413 predictions, our verdict column becomes a covariate to
   stratify on rather than only a caveat. *Changes per answer:* if yes, `verdict`
   enters the results as an axis; if no, it stays a Methods column.

5. **Does the corpus contain any receptor-specific statement about the three
   annotation-vs-structure splits — CCKAR (Gs deposited, Gq annotated), GHSR
   (Gi deposited, Gq annotated), NTR1 (Gi deposited, Gq annotated)?** *Changes
   per answer:* a primary-literature statement for any of the three collapses a
   PI decision into a citation and moves that receptor out of §5's list.

6. **Is there a corpus statement on whether a GPCR–Gα prediction is sensitive to
   Gα *subtype* within a family at all** — Gi1 vs Go vs Gz, which differ at 6 of
   21 α5-CT positions? *Changes per answer:* if predictions are known to be
   subtype-insensitive, the 86% subtype disagreement on our panel (§7) is a
   non-issue and can be dismissed in one sentence; if not, the `GoA`/`GoB` gap in
   `seq_rungs.tsv` becomes blocking for 25 receptors rather than a note.
