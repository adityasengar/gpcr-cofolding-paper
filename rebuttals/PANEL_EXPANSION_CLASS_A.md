# Class A GPCRs in the ConfoRNets benchmark that our panel does not contain

For the pipeline agent. Compiled 2026-09-10 by the orchestrator session.

**Scope: Class A only**, per Aditya. The ConfoRNets benchmark holds 51 both-state
receptors; 21 are absent from our 48-receptor panel; **19 of those 21 are Class
A**. The two dropped here are CALRL (class B1) and AGRE5 (class B2, adhesion) —
real gaps, but out of scope for this study.

## Provenance, because it decides what is citable

- **The pairs** come from the ConfoRNets authors' own released benchmark file,
  `assets/gpcr/references.csv` in `github.com/aqlaboratory/confornets`, extracted
  to `lit/panels/si_tables/lee2026confornets_gpcr_references.csv` — 51 rows,
  matching the paper's stated count exactly.
- **Resolution, method, species and state** come from a cached GPCRdb snapshot
  (1,716 entries, `lit/panels/cache/gpcrdb_structures.json`) — a database, not
  the corpus. Every one of the 38 PDB IDs below resolves in it, and GPCRdb
  annotates all 51 pairs cleanly as Active / Inactive.
- **Our own panel** is read from `data/block_a/01_rows/block_a_rows.csv` and
  `data/block_b/09_references/reference_audit.csv`.

Nothing here comes from general knowledge. A fabricated receptor list would be
acted on.

---

## 1. The 19 Class A receptors to add

| # | receptor | active PDB | Å | method | inactive PDB | Å | method | species |
|--:|---|---|--:|---|---|--:|---|---|
| 1 | **5HT2A** | 8UWL | 2.80 | cryo-EM | 7WC7 | 2.60 | X-ray | human |
| 2 | **ACM3** | 8E9Z | 2.69 | cryo-EM | 4U15 | 2.80 | X-ray | **human active / rat inactive** |
| 3 | **ADA1A** | 8THK | 2.60 | cryo-EM | 8HN1 | 2.90 | cryo-EM | human |
| 4 | **CCR2** | 7XA3 | 2.90 | cryo-EM | 6GPX | 2.70 | X-ray | human |
| 5 | **CCR6** | 6WWZ | 3.34 | cryo-EM | 9D3G | 3.26 | cryo-EM | human |
| 6 | **CCR8** | 8XML | 2.58 | cryo-EM | 8TLM | 2.90 | cryo-EM | human |
| 7 | **CXCR3** | 8HNM | 2.94 | cryo-EM | 8K2W | 3.00 | cryo-EM | human |
| 8 | **DRD4** | 8IRU | 3.20 | cryo-EM | 5WIU | 1.96 | X-ray | human |
| 9 | **GPR6** | 8TYW | 3.43 | cryo-EM | 8T1V | 2.60 | X-ray | human |
| 10 | **HRH2** | 8YN3 | 2.56 | cryo-EM | 7UL3 | 3.00 | cryo-EM | human |
| 11 | **MTR1A** | 7VGY | 3.10 | cryo-EM | 6ME2 | 2.80 | X-ray | human |
| 12 | **NK1R** | 8U26 | 2.50 | cryo-EM | 6E59 | 3.40 | X-ray | human |
| 13 | **NTR1** | 8FN1 | 2.88 | cryo-EM | 7UL2 | 2.40 | cryo-EM | **rat active / human inactive** |
| 14 | **OPRM** | 8E0G | 2.10 | X-ray | 7UL4 | 2.80 | cryo-EM | Mus musculus |
| 15 | **OXYR** | 7RYC | 2.90 | cryo-EM | 6TPK | 3.20 | X-ray | human |
| 16 | **PD2R2** | 8XXV | 2.33 | cryo-EM | 7M8W | 2.61 | X-ray | human |
| 17 | **S1PR5** | 7EW1 | 3.40 | cryo-EM | 7YXA | 2.20 | X-ray | human |
| 18 | **SSR2** | 7T10 | 2.50 | cryo-EM | 7XN9 | 2.60 | X-ray | human |
| 19 | **TSHR** | 7UTZ | 2.40 | cryo-EM | 7T9M | 3.10 | cryo-EM | human |

**Species is not uniform, and the paper does not flag any of it.** Three of the
nineteen need a decision before they are added:

- **ACM3** — human 8E9Z active against **rat** 4U15 inactive. Cross-species.
- **NTR1** — **rat** 8FN1 active against human 7UL2 inactive. Cross-species.
- **OPRM** — `oprm_mouse` on both sides (8E0G / 7UL4). Same-species, but
  **mouse**, not human.

The other sixteen are human on both sides. Take ACM3 and NTR1 only if a
cross-species contrast is acceptable, and say so in the methods if you do: our
own panel currently has **zero** cross-species pairs, which is worth keeping.
OPRM is a different question — a consistent mouse pair is internally sound, and
it only matters because it adds a third non-human receptor to a panel that
already has two.

Resolution range across the 38 structures: 1.96 to 3.43 A. Both resolutions are
recorded for all 19 pairs, so a quality floor can be applied before selection
rather than discovered afterwards.

## 2. A second finding, which may matter more than the first

**Of the 27 Class A receptors we share with ConfoRNets, 18 are scored against a
different reference pair than ours.** Same receptor, different structures. That
is not a gap in the panel; it is a disagreement about what "the active state of
this receptor" means, and it is invisible unless the two lists are laid side by
side.

| receptor | their active | our active | their inactive | our inactive | what differs |
|---|---|---|---|---|---|
| 5HT1B | 6G79 | 6G79 | 5V54 | 4IAR | inactive 5V54 3.90 vs our 4IAR 2.70 Å |
| AA2AR | 6GDG | 5G53 | 5NM4 | 5NM4 | active 6GDG 4.11 vs our 5G53 3.40 Å |
| ACM2 | 7T94 | 7T94 | 5ZK8 | 5ZKC | inactive 5ZK8 3.00 vs our 5ZKC 2.30 Å |
| ADRB1 | 8DCS | 7BU7 | 4BVN | 7BVQ | active 8DCS 2.50 vs our 7BU7 2.60 Å; **theirs is turkey, ours human**; inactive 4BVN 2.10 vs our 7BVQ 2.50 Å |
| ADRB2 | 8GG0 | 4LDE | 6PS2 | 6PS2 | active 8GG0 2.90 vs our 4LDE 2.79 Å |
| B1B1U5 | 9EPP | 9EPR | 6I9K | 6I9K | active 9EPP 4.06 vs our 9EPR 4.90 Å |
| CCKAR | 7MBX | 7MBX | 7F8U | 7F8Y | inactive 7F8U 2.80 vs our 7F8Y 2.50 Å |
| CCR5 | 7O7F | 7F1S | 6MEO | 5UIW | active 7O7F 3.15 vs our 7F1S 2.80 Å; inactive 6MEO 3.90 vs our 5UIW 2.20 Å |
| CNR1 | 8GHV | 5XRA | 9BA0 | 5U09 | active 8GHV 2.80 vs our 5XRA 2.80 Å; inactive 9BA0 3.13 vs our 5U09 2.60 Å |
| CXCR4 | 8U4N | 8U4N | 3OE0 | 3ODU | inactive 3OE0 2.90 vs our 3ODU 2.50 Å |
| EDNRA | 8HCQ | 8HCQ | 8XVL | 8XVK | inactive 8XVL 3.22 vs our 8XVK 3.21 Å |
| EDNRB | 8IY5 | 8IY5 | 5GLI | 6IGK | inactive 5GLI 2.50 vs our 6IGK 2.00 Å |
| GHSR | 7NA8 | 7NA7 | 6KO5 | 7F83 | active 7NA8 2.70 vs our 7NA7 2.70 Å; inactive 6KO5 3.30 vs our 7F83 2.94 Å |
| HRH3 | 8YN5 | 8YUU | 7F61 | 7F61 | active 8YN5 2.70 vs our 8YUU 2.70 Å |
| LSHR | 7FII | 7FIH | 7FIJ | 7FIJ | active 7FII 4.30 vs our 7FIH 3.20 Å |
| NPY2R | 8K6N | 7YON | 7DDZ | 7DDZ | active 8K6N 3.20 vs our 7YON 2.95 Å |
| OPRK | 8FEG | 8FEG | 6VI4 | 4DJH | inactive 6VI4 3.30 vs our 4DJH 2.90 Å |
| OPSD | 4X1H | 4X1H | 8A6E | 7ZBC | inactive 8A6E 1.80 vs our 7ZBC 1.80 Å |

Three of these repay a close read:

- **AA2AR.** They chose 6GDG (4.11 A cryo-EM) over our 5G53 (3.40 A X-ray) —
  *worse* resolution. Under their stated rule construct quality ranks **before**
  resolution, so 5G53 presumably carries more engineered mutations. AA2AR is the
  receptor that is recurrently anomalous in our own data (C-B-8; it alone drives
  the tilt covariate slope). **A thermostabilised active reference is a concrete,
  testable explanation for that anomaly**, and re-scoring AA2AR against 6GDG
  would test it at the cost of no new predictions.
- **ADRB1.** Their pair is **turkey** on both sides (8DCS / 4BVN, *Meleagris
  gallopavo*); ours is human (7BU7 / 7BVQ). We are ahead here.
- **B1B1U5.** They use 9EPP (4.06 A); we use 9EPR (4.90 A), and our audit records
  why — 9EPP is a Gi/q chimera whose coupling a UniProt lookup would mis-assign,
  and 9EPR is the native Gi heterotrimer from the same deposition. We traded
  0.84 A of resolution for a correct coupling assignment. Also ahead.

## 3. Their selection rule, which we could adopt or cite

`lee2026confornets` p.15, App. D.1, verbatim — the only stated both-states panel
rule in the 79-paper corpus, and the only rule anywhere in it that filters on
**construct quality**:

> "The GPCR benchmark was constructed from the GPCRdb structure database (Munk
> et al., 2016). We selected GPCRs with both fully active (100 per cent
> activation degree) and inactive structures available. We selected pairs with
> the fewest engineered mutations and highest crystallographic resolution,
> retaining 51 pairs where both structures contained at most one mutation."

**The caveat that must travel with it:** their state label is GPCRdb's own
activation-degree annotation. Adopting it wholesale makes the instrument
dependent on the annotation it is meant to adjudicate — the same circularity our
Methods already flags for our 80 threshold rows.

## 4. A species audit of our existing panel, done while checking theirs

All 80 of our references resolve in the GPCRdb snapshot. Two results:

- **Zero cross-species pairs.** Every one of our 40 pairs is same-organism. The
  lit session suspected OPSD might be human-active against bovine-inactive. It is
  not: 4X1H and 7ZBC are **both** `opsd_bovin`.
- **Two non-human receptors, not one.** **OPSD** is bovine throughout and
  **B1B1U5** is an opsin from *Hasarius adansoni*, a jumping spider. Both are
  legitimately Class A. **But no sentence may describe this panel as human
  receptors**, and one of ours currently comes close. Adding OPRM from the list
  above would make it three.

## 5. What we are asking for

1. **Add the 19 Class A receptors above**, or say why not. They arrive with
   resolutions and methods, so a quality floor can be set in advance.
2. **Decide ACM3 and NTR1 explicitly** — accept the cross-species pairing, or
   drop them.
3. **Re-score AA2AR against 6GDG** as a sensitivity check on the standing
   anomaly. No new predictions required.
4. **Add a `species` column to `reference_audit.csv`.** Its `method` column is
   the same placeholder string on all 80 rows and `resolution` is a second
   placeholder string, `not tracked in reference_set schema` — a NON-NULL, so a
   null check passes on it,
   so neither construct quality nor species can be checked from the drop as
   shipped. All three are available in GPCRdb.
5. **State the panel selection rule.** With 19 named additions available and a
   published rule to compare against, "we picked 40" needs to become a sentence
   a referee can evaluate.
