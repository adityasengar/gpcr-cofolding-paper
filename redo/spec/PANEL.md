# PANEL.md — the exact systems the redo runs on

Compiled 2026-09-11 by the panel session. Scope: **which receptors, which reference
structures, which ligands, which clusters, and the rule that selects them.**
Siblings own what is supplied to these systems (`SEQUENCES.md`) and how much runs
(`RUN_MATRIX.md`); nothing here sets a prediction budget.

Read `redo/spec/CATALOGUE.md` §0.2 first. This file makes its panel
assumptions concrete and, in four places, corrects them.

## How to read this

Every receptor row is machine-generated from files with paths. The readable tables below
are a projection of **`redo/inputs/panel_systems.csv`** (75 rows × 138 columns), which is
the artefact to act on. Three companions carry the evidence:

| file | what it holds |
|---|---|
| `redo/inputs/panel_systems.csv` | one row per receptor, 138 columns: identity, class, cluster, three candidate reference pairs, membership, QC flags, cutoffs, ligands, tier, and the `passes_strict` filter columns of §14 |
| `redo/inputs/panel_reference_qc.csv` | one row per **candidate structure**, 962 rows: RCSB title, receptor polymer-entity description, engineered substitutions, fusion/fiducial flags, resolution, method, release date |
| `redo/inputs/panel_uniprot.tsv` | 86 UniProt accessions, retrieved 2026-09-11, one per GPCRdb protein entry appearing anywhere in the panel |
| `redo/cache/panel_rcsb_cache.json` | the raw RCSB response the QC table is derived from (962 entries) |
| `redo/cache/panel_rcsb_status.json` | RCSB holdings status for the 192 reference candidates checked entry-by-entry |

**Nothing in this document is from general knowledge.** Every PDB ID, resolution, method,
species and date is either read from `lit/panels/cache/gpcrdb_structures.json` or retrieved
from RCSB and cached in the files above; the two agree on resolution and release date for
all 191 entries where both were available, with zero mismatches. UniProt accessions were
retrieved from `rest.uniprot.org` because **no file in this repository carries a UniProt
accession for more than four receptors** — `data/block_a/01_rows/block_a_rows.csv`'s column
named `uniprot` holds GPCRdb *entry names* (`5ht1b_human`), not accessions. The four real
accessions we already held are in `data/block_d/09_references/nanobody_state_anchors.csv`.

Frozen inputs, so this is reproducible:

```
77e0b077…a87a91  lit/panels/cache/gpcrdb_structures.json          (1,716 entries)
bd08abab…df6dd7  lit/panels/si_tables/lee2026confornets_gpcr_references.csv (51 pairs)
6ee2cad8…5202ef  data/block_b/09_references/reference_set.blockb_pinned.csv (162 rows)
6158081e…675a59  data/block_b/09_references/paralogy_clusters.csv (40 rows)
```

---

# 1. The structural universe, recomputed — and five numbers reconciled

Recomputed here from the snapshot, independently of §0.2:

| quantity | value | agrees with |
|---|---:|---|
| entries in snapshot | 1,716 | catalogue §0.2 |
| Class A entries | 1,358 | ✓ |
| Class A annotated Active or Inactive | 1,336 (965 A / 371 I) | ✓ |
| Class A annotated **Intermediate** | 21 | ✓ |
| unique Class A receptors with an Active/Inactive entry | 199 | ✓ |
| Class A receptors with **both** states, **same UniProt entry** | **66** | ✓ |
| …those 66 collapsed to receptor slugs | **64** | ✓ |
| …slugs both-state **allowing cross-species pairing** | **65** | catalogue says 64 |
| …restricted to human | 61 | ✓ |
| all-class both-state, same UniProt entry | **86** (80 human) | `PANEL_EXPANSION.md` §1 says 86 |
| all-class both-state slugs | 84 | catalogue says 83 |

**The two disagreements are one receptor and one rule, not an error.** `acm3` is both-state
*only* if a human active (`8E9Z`) is paired with a **rat** inactive (`4U15`). Under a
species-strict rule it is not both-state; under a species-collapsed rule it is. The
catalogue's 64 and 83 are the species-strict counts collapsed to slugs; my 65 and 84 are
the cross-species-permissive counts. **Both are right; the rule has to be stated.** This
panel uses the species-strict rule, so ACM3 is excluded and named as excluded (§6).

`PANEL_EXPANSION.md` §1's **86** is an **all-class** count and the catalogue's **66** is a
**Class A** count. They were never in conflict. Two receptors in the 66 have two both-state
species entries each — `adrb1` (human *and* turkey) and `ntr1` (human *and* rat) — which is
why 66 collapses to 64 rather than 65.

**Correction to the catalogue, §E7.3.** It lists 9 Class A receptors with an inactive
structure and no active one anywhere: `acm5 ada1b ada2c ccr7 ccr9 gnrhr lgr4 ox1r q9wtk1`.
**`q9wtk1_cavpo` is the guinea-pig LTB4 receptor (5X33, 3.7 Å, 2018-01-03)** — UniProt
`Q9WTK1_CAVPO`, "LTB4 receptor". It is the same receptor as `lt4r1_human`, which is already
on our panel and *has* active structures. It survives at slug level only because GPCRdb
names it by accession rather than by mnemonic, so the species-collapse that removed
`acm3_rat` and `drd4_mouse` does not touch it. **The prospective set is 8, not 9.**
There are nine accession-as-name slugs in the snapshot; the two that matter are `b1b1u5`
(known) and `q9wtk1` (new). The other seven are active-only viral, zebrafish, rabbit and
*Xenopus* entries, out of scope.

---

# 2. The ConfoRNets overlap: all three numbers are right, for three different objects

Every one of the 102 PDB IDs in the ConfoRNets file resolves in the snapshot; 51 test cases,
**53 distinct GPCRdb proteins**, because ACM3 and NTR1 each pair two species.

| overlap counted as | value | matches |
|---|---:|---|
| exact GPCRdb protein entry (species-strict) vs our **48** | **29** | `PANEL_EXPANSION.md` §1 |
| receptor slug (species-collapsed) vs our **48** | **30** | catalogue §0.3 |
| receptor slug vs our **40 Class A** | **27** | catalogue §0.3, `PANEL_EXPANSION_CLASS_A.md` §2 |

**The single receptor separating 29 from 30 is ADRB1.** ConfoRNets' pair is
`adrb1_melga` — turkey, 8DCS/4BVN — and ours is `adrb1_human`, 7BU7/7BVQ. So it is the same
receptor slug and a different protein entry. `PANEL_EXPANSION_CLASS_A.md` §2 already noticed
the turkey pair; what was not said is that it is the entire arithmetic difference between the
two headline overlap numbers. **All three numbers should be retired in favour of one sentence
with its rule attached**, and I recommend: *"27 of ConfoRNets' 51 test cases are Class A
receptors on our current panel; 30 of 51 if the four Class B/F receptors we carry are
counted; and 29 if same-species identity is required."*

**The known non-human list is incomplete.** `CLAUDE.md` and the brief name OPSD (bovine),
OPRM (mouse) and B1B1U5 (jumping spider). **ConfoRNets adds a fourth: ADRB1, turkey
(*Meleagris gallopavo*), on both sides of its pair.** Any script that adopts their
references inherits it silently.

**ConfoRNets' class composition, which no project document states.** Its 51 test cases are
**46 Class A, 2 B1 (CALRL, GLP1R), 1 B2 (AGRE5), 2 F (FZD7, SMO)**. 45 of the 46 Class A
cases are species-strict both-state and therefore inside our census; the 46th is ACM3.
`PANEL_EXPANSION_CLASS_A.md` describes the 51 as "Class A plus CALRL and AGRE5" — it also
contains FZD7 and SMO, which happen to be on our panel already, which is why they were not
noticed as gaps.

---

# 3. A defect in the published benchmark, found while checking it

**`7EVW` — ConfoRNets' active reference for FZD7 — was removed from the PDB on 2024-04-24
and superseded by `8YY8`.** RCSB holdings status `REMOVED / OBS`, replacement `8YY8`;
`data.rcsb.org` returns 404 for the entry. The GPCRdb snapshot still carries it (3.22 Å,
released 2021-08-04) because the snapshot is not re-validated against holdings.

It is the only non-current entry among the 192 reference candidates checked one by one, and
the only one of 963 candidate structures that RCSB's GraphQL `entries` endpoint declines to
return — which makes that endpoint a free obsolescence check for any future panel build.

Our own pinned set already carries `8YY8` for FZD7 (`reference_set.blockb_pinned.csv`), so
we are not exposed. But **a reference list must be validated against live PDB holdings, not
against a cached snapshot**, and any sentence citing ConfoRNets' FZD7 pair should cite
8YY8/9EPO rather than 7EVW.

---

# 4. The selection rule, in a form that could have been pre-registered

Two rules, deliberately separated: **membership** decides which receptors, and admits nothing
about structure quality; **reference choice** decides which coordinates, and is where quality
lives. Keeping them apart is what stops the panel being a sample of well-behaved receptors.

## Rule P — panel membership

> A receptor enters the core panel if and only if, in the frozen GPCRdb snapshot
> `lit/panels/cache/gpcrdb_structures.json` (SHA-256 `77e0b077…a87a91`, 1,716 entries),
> there exists at least one structure annotated `Active` **and** at least one annotated
> `Inactive` **for the same UniProt entry**, and the receptor's GPCRdb class is A.
>
> No resolution term, no construct term, no mutation term, no deposition-date term and no
> ligand term enters membership. Receptors satisfying the rule are taken **without
> exception**, and each excluded receptor is named with the clause that excluded it.

This yields **64 receptors** — a complete census of the Class A both-state universe as of the
snapshot — and it answers `rebuttals/BLOCK_A.md` Q-A1 and the `[PI]` at `methods.tex:16`
with a sentence a referee can evaluate: *the panel is not a sample.*

**It contains all 40 of our current Class A receptors and 45 of ConfoRNets' 46 Class A test
cases.** The one it does not contain is ACM3, excluded by the species clause, which
ConfoRNets does not state and, on its own data, does not apply.

## Rule R — reference choice, applied after membership

> 1. **Species.** Use *Homo sapiens* if a human entry of this receptor has both states;
>    otherwise the single species that does. Never pair two species. Record the species.
> 2. Drop entries that are not CURRENT in RCSB holdings on the freeze date.
> 3. Within each state, rank ascending on, in order:
>    (a) engineered substitutions recorded on the **receptor** polymer entity;
>    (b) fusion partner present in the receptor polymer entity (absent before present);
>    (c) resolution; (d) most recent release date.
>    Take the top-ranked entry.
> 4. **Partner-chain override.** Where the top-ranked entry's transducer chain is a chimera
>    **and an entry of the same receptor and state with a NATIVE transducer exists**, take the
>    native one and record the demotion. **The rule is conditional on that second clause and
>    does not fire without it**: "prefer native over chimeric" has no meaning where every
>    candidate is a construct. Where no native option exists, rule 3's pick stands and the
>    construct is recorded (§6.1 QC flags and `g1_panel_freeze.tsv:reference_tip_note`).
> 5. **Record, never filter on:** fusion partner identity, fiducial (nanobody / scFv / Fab)
>    presence, ICL3 excision, mutation count, transducer identity, ligand.

**Rule 4's written justification was wrong, and is corrected here rather than deleted
(2026-09-12).** This paragraph used to read:


> ~~Rule 4 exists because rule 3 gets **B1B1U5** wrong without it: it promotes `9EPP` over
> our `9EPR`, undoing a decision our own audit made for a good reason — 9EPP is a Gi/q
> chimera and 9EPR is the native Gi heterotrimer from the same deposition
> (`PANEL_EXPANSION.md` §5a).~~ {ref-history}

Three things are wrong with it, and the document contradicted its own §6.1 table — which
says `9EPP` — for two days as a result. The frozen artefacts followed the table; the prose
was the defect. See `spec/D_H_RESOLUTION.md`, and `DECISIONS.md` D-H (decided 2026-09-12).

1. **9EPR is not a native heterotrimer.** `tejero2024opsin` Methods: it is human Gαi1
   expressed in *E. coli* and reconstituted *in vitro* with **bovine** Gβ1γ1 separated from
   retinal transducin. 9EPP carries human Gβ1γ2. Neither entry is native, and the βγ differs
   between them — which no UniProt cross-reference surfaces.
2. **So rule 4 is INAPPLICABLE to B1B1U5, not merely unimplemented.** Its second clause is
   never satisfied. It was never the reason the map says 9EPP; rule 3 selecting 9EPP is the
   whole story, and that selection is correct.
3. **9EPP's α5 tip is not a graft of a human Gq tip.** It is jumping-spider Gαq1 (INSDC
   `LC799818`) swapped into human Gαi1 at 337–354 — so the three ct21 differences from human
   Gq/G11 are *species* divergence, and all three fall inside the spider window. RCSB's own
   `pdbx_mutation` for `9EPP_2` records exactly those eight substitutions inside 337–354 and
   three outside it, so this is checkable from the PDB entry alone.

Rule 4 is therefore **kept, scoped, and still unimplemented in code** — no selection script
reads a partner chain. That remains a gap for the receptors where it *can* fire, and it must
be implemented or struck before the panel grows; it is simply not what happened here. Rule 3
reads the *receptor* entity only, and nothing in this project has ever read a partner chain
as part of reference selection (`methods.tex:282`).

### Rule R reconstructs 80% of ConfoRNets' reference choices

Applied to the 51 receptors ConfoRNets covers, rule R selects **the same PDB entry on 82 of
their 102 reference slots (80%)**. A resolution-only rule gets **67 of 102 (66%)**. So the
"fewest engineered mutations, then highest resolution" ordering in their Appendix D.1 is
real and reconstructible on the *reference-choice* step, even though `lit/panels/README.md`
shows their *membership* is not reconstructible from the text.

This is a membership-controlled comparison — the receptors are given, only the choice varies
— so it is not the count-matching that the README warns against. It is the strongest
validation of a published selection rule available in this corpus.

### What ConfoRNets' ≤1-mutation cap would cost us

Applying their cap to the census, using RCSB's `pdbx_mutation` record on the receptor entity
and summing across the rule-R pair:

| cap | receptors retained of 64 |
|---|---:|
| ≤1 substitution across both references | **47** |
| ≤2 | 50 |
| ≤3 | 56 |
| no cap | 64 |

**A decision for Aditya, not for me.** My recommendation is **no cap**, because:

- The cap is a **selection on the covariate the paper is about**. If engineered receptors
  behave differently under a supplied partner, capping mutations removes exactly the variance
  the analysis should be estimating. Recording the count keeps it available as a covariate.
- **RCSB's mutation record is a floor, and a bad one.** `methods.tex:303` reports that for
  fifteen reference partner chains verified against canonical UniProt sequence,
  **RCSB's `pdbx_mutation` was empty for ten of them**. A cap computed on that field prunes
  the receptors whose depositors were diligent, not the receptors that are engineered.
- The cap is what shrinks ConfoRNets' panel to 51. Not applying it is what lets us say
  *census*.

If a cap is wanted anyway, ≤3 costs 8 receptors and keeps 31 clusters; ≤1 costs 17.

---

# 5. The recommended panel

| tier | rule | n | paralog clusters | contains |
|---|---|---:|---:|---|
| **C1 — core** | Rule P | **64** | 32 | all 40 of our Class A; 45 of ConfoRNets' 46 Class A |
| **C1r — reduced core** *(only if budget forces one)* | Rule P + both rule-R references ≤ 3.00 Å | 29 | 21 | 17 of our 40; 19 of ConfoRNets' 45 |
| **H — date-stratified strata** | subsets of C1, by backbone cutoff | 42 / 32 / 12 | 27 / 23 / 8 | see §8 |
| **E-B1 — cross-class transfer** | Rule P with class = B1 | 5 | 4 | CALRL, CRHR1, GCGR, GLP1R, PTH1R |
| **E-scope — declared instrument scope, no claim** | our current class F/B2 carry-over | 5 | 2 | AGRE5, FZD4, FZD6, FZD7, SMO |
| **E-pro — prospective, ungradeable by construction** | Class A, inactive structure only, no active anywhere | **8** | 8 | `acm5 ada1b ada2c ccr7 ccr9 gnrhr lgr4 ox1r` |
| **X — excluded, named** | fails a clause of Rule P | 2 | — | ACM3 (species clause), FZD6 (no inactive) |

**The core is C1 = 64, and it is the working panel.** Whether ConfoRNets' stricter criteria
should later be applied on top is an open decision, carried as the `passes_strict` filter
column rather than as a second panel — see §14. **61 of the 64 pass it**; the three that do
not are ACM1, ADRB1 and S1PR1.

The catalogue's caution — "adopt 64 only for the arms whose
conclusions depend on power" — is a budget call and belongs to `RUN_MATRIX.md`; what belongs
here is that **any arm run on a subset of C1 is a sample again, and the subsetting rule must
be stated with the arm.** C1r is supplied so that, if a subset is unavoidable, there is one
pre-registrable rule to use rather than an ad-hoc pick. C1r is a poor comparability anchor —
it drops 26 of ConfoRNets' 45 — and I would run the reduced core only for exploratory arms.

**Intermediate states.** The snapshot holds **21 Class A `Intermediate` entries**, plus 10
class C and 1 class B1, across 13 receptor entries in total: `5ht2b_human ackr1_human
adrb2_human casr_human gabr2_human glp1r_human grm1_human grm2_human grm4_human grm5_human
mc4r_human mrgrd_human ntr1_rat`. **Exactly one of them, `adrb2_human`, is a core-panel
receptor** — so the intermediate set is almost entirely off-panel, which is convenient: it can
be measured as part of the E0.1 off-panel calibration pass without contaminating the
application set. Intermediates enter no tier; they are the measurement set for catalogue E0.3.

---

# 6. The receptors

Columns: **in** = `both` (ours + ConfoRNets) / `ours` / `CN` / `neither`. **QC flags**:
`A:`/`I:` = active/inactive reference; `fus` = fusion partner inside the receptor polymer
entity; `fid` = nanobody/scFv/Fab/megabody in the deposited assembly; `mutN` = N engineered
substitutions in RCSB's record for the receptor entity (**a floor**, §4). **post-cutoff** =
active reference released on or after `C` Chai-1 2021-01-12, `P` Protenix 2021-09-30,
**`B`** Boltz-2 2023-06-01; `(both)` = both references post-Boltz-2. OpenFold3's cutoff is
undated and still an open ask (`methods.tex:225`). **Ligands** = agonist modality /
antagonist modality / Block C coverage (`C` both roles run, `c` one role, `–` not run).
References are the **rule-R** picks; `panel_systems.csv` also carries our current pinned pair,
ConfoRNets' pair and the resolution-only pick for every receptor.

**What the QC flags do NOT tell you, and where to look instead (added 2026-09-12).** Every
flag in this table is read off the **receptor** polymer entity. None of them says anything
about the **transducer** chain, so a reference whose Gα α5 tip is a chimera looks identical
here to one that is canonical. **Twelve of the 64 have a non-canonical α5 tip on their
rule-R active reference** — nine mini-Gs/q chimeras, a Gi/Gq chimera, a Gi/Gt chimera, and
rhodopsin's 11-residue peptide analogue in `4X1H`. The census is
`inputs/g1_refchimera.tsv`, one row per entity, and the check *"§6 note — receptors with a
non-canonical α5 tip on the rule-R active reference"* in `gates/panel_verify.py` fails if
that set stops matching this list:

> `5HT2A 5HT2C ADA1A B1B1U5 DRD4 EDNRA GRPR HRH1 OPSD OX2R OXYR TA2R`

**Ten of the twelve are cross-family chimeras and are excluded from the primary panel**
(`g1_panel_freeze.tsv`, DECISION 1). The two that stay are the two where the rule resolves:
**OPSD**, whose partner entity is an 11-residue peptide (`PEPTIDE_ENTITY`, and everything
past rung `R1_ct11` is extrapolation), and **B1B1U5**, by **D-H (c′)** — its tip is spider
Gαq1, native for the organism, and there is no native alternative to demote to. B1B1U5's
reference is spelled out in `g1_panel_freeze.tsv:reference_tip_note`.


## 6.1 Tier C1 — the core panel, 64 receptors

| # | slug | UniProt | GPCRdb | cl | cluster | active ref | inactive ref | in | QC flags | post-cutoff | agonist / antagonist / BlkC |
|--:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **5HT1B** | P28222 | `5ht1b_human` | A | `001_001_001` | 6G79 3.78Å EM 2018-06-20 | 5V54 3.9Å X 2018-02-07 | both | I:mut1 | pre-all | sm / sm / C |
| 2 | **5HT2A** | P28223 | `5ht2a_human` | A | `001_001_001` | 8UWL 2.8Å EM 2024-05-29 | 7WC7 2.6Å X 2022-01-26 | CN | A:fid I:fus | pre-all | sm / sm / – |
| 3 | **5HT2C** | P28335 | `5ht2c_human` | A | `001_001_001` | 8DPF 2.84Å EM 2022-08-24 | 6BQH 2.7Å X 2018-02-14 | both | A:fid I:fus | pre-all | sm / sm / c |
| 4 | **5HT5A** | P47898 | `5ht5a_human` | A | `001_001_001` | 7X5H 3.1Å EM 2022-09-14 | 7UM4 2.8Å X 2022-07-20 | ours | A:fus+fid I:mut2 | C P | sm / sm / C |
| 5 | **AA1R** | P30542 | `aa1r_human` | A | `001_006_001` | 7LD3 3.2Å EM 2021-09-08 | 5UEN 3.2Å X 2017-03-01 | both | I:fus | pre-all | sm / sm / C |
| 6 | **AA2AR** | P29274 | `aa2ar_human` | A | `001_006_001` | 8WDT 3.34Å X 2024-01-17 | 6S0L 2.65Å X 2020-07-15 | both | A:fid | pre-all | sm / sm / C |
| 7 | **ACM1** | P11229 | `acm1_human` | A | `001_001_002` | 6OIJ 3.3Å EM 2019-05-08 | 6WJC 2.55Å X 2020-07-08 | ours | A:fid+mut2 I:fus | pre-all | sm / sm / C |
| 8 | **ACM2** | P08172 | `acm2_human` | A | `001_001_002` | 7T94 3.16Å EM 2023-01-25 | 5ZK8 3.0Å X 2018-11-21 | both | A:fid I:fus | pre-all | sm / sm / C |
| 9 | **ACM4** | P08173 | `acm4_human` | A | `001_001_002` | 7TRP 2.4Å EM 2023-05-17 | 5DSG 2.6Å X 2016-03-16 | both | A:fid I:fus | C P | sm / sm / C |
| 10 | **ADA1A** | P35348 | `ada1a_human` | A | `001_001_003` | 7YM8 2.92Å EM 2023-07-05 | 8HN1 2.9Å EM 2023-12-20 | CN | A:fid I:fid | C P **B** (both) | sm / pep;sm / – |
| 11 | **ADA2A** | P08913 | `ada2a_human` | A | `001_001_003` | 7EJ8 3.0Å EM 2022-04-13 | 6KUX 2.7Å X 2019-12-04 | both | A:fid | C P | sm / sm / c |
| 12 | **ADRB1** | P08588 | `adrb1_human` | A | `001_001_003` | 7BU7 2.6Å X 2020-12-02 | 7BVQ 2.5Å X 2020-12-02 | both | A:fus+fid+mut2 I:fus+mut2 | pre-all | sm / sm / c |
| 13 | **ADRB2** | P07550 | `adrb2_human` | A | `001_001_003` | 8GG0 2.9Å EM 2024-03-06 | 2R4R 3.4Å X 2007-11-06 | both | I:fid | pre-all | sm / sm / C |
| 14 | **AGTR1** | P30556 | `agtr1_human` | A | `001_002_001` | 6OS2 2.7Å X 2020-02-19 | 8TH3 3.0Å EM 2024-05-22 | ours | A:fus+fid I:fus+fid | pre-all | pep;prot / prot;sm / C |
| 15 | **APJ** | P35414 | `apj_human` | A | `001_002_002` | 8XZH 2.6Å EM 2024-03-20 | 5VBL 2.6Å X 2017-05-31 | ours | A:fid I:fus+mut5 | C P | pep;prot;sm / **none** / c |
| 16 | **B1B1U5** | B1B1U5 | `b1b1u5_9arac` | A | `001_009_001_inv` | 9EPP 4.06Å EM 2024-10-23 | 6I9K 2.15Å X 2019-07-03 | both | I:mut1 **spider** | C P **B** | sm / sm / – |
| 17 | **C5AR1** | P21730 | `c5ar1_human` | A | `001_002_006` | 7Y66 2.9Å EM 2023-03-01 | 6C1R 2.2Å X 2018-05-30 | neither | A:fid I:fus+mut3 | C P | pep / pep;sm / – |
| 18 | **CCKAR** | P32238 | `cckar_human` | A | `001_002_005` | 7MBX 1.95Å EM 2021-05-26 | 7F8U 2.8Å X 2021-10-13 | both | A:fid I:fus | C | pep;prot;sm / sm / C |
| 19 | **CCR2** | P41597 | `ccr2_human` | A | `001_003_002` | 7XA3 2.9Å EM 2022-08-24 | 6GPX 2.7Å X 2019-01-02 | CN | A:fid I:fus | C P | pep / sm / – |
| 20 | **CCR5** | P51681 | `ccr5_human` | A | `001_003_002` | 7O7F 3.15Å EM 2021-06-30 | 6MEO 3.9Å EM 2018-12-12 | both | A:fid | C | pep / prot;sm / C |
| 21 | **CCR6** | P51684 | `ccr6_human` | A | `001_003_002` | 6WWZ 3.34Å EM 2020-06-24 | 9D3G 3.26Å EM 2024-09-11 | CN | A:fid I:fus+fid | pre-all | pep / sm / – |
| 22 | **CCR8** | P51685 | `ccr8_human` | A | `001_003_002` | 8KFX 2.96Å EM 2024-02-07 | 8TLM 2.9Å EM 2023-12-20 | CN | A:fid I:fus+fid | C P **B** (both) | prot;sm / prot / – |
| 23 | **CNR1** | P21554 | `cnr1_human` | A | `001_004_005` | 8GHV 2.8Å EM 2023-05-24 | 9BA0 3.13Å EM 2024-11-20 | both | A:fid I:fus | pre-all | sm / sm / C |
| 24 | **CNR2** | P34972 | `cnr2_human` | A | `001_004_005` | 8GUR 2.84Å EM 2023-05-10 | 5ZTY 2.8Å X 2019-01-30 | ours | A:fid I:fus+mut7 | pre-all | sm / sm / C |
| 25 | **CXCR2** | P25025 | `cxcr2_human` | A | `001_003_002` | 6LFO 3.4Å EM 2020-09-02 | 6LFL 3.2Å X 2020-09-02 | ours | A:fid I:fus+mut3 | pre-all | prot / sm / C |
| 26 | **CXCR3** | P49682 | `cxcr3_human` | A | `001_003_002` | 8HNM 2.94Å EM 2023-11-29 | 8K2W 3.0Å EM 2023-11-29 | CN | A:fus+fid I:fus+fid | C P **B** (both) | pep;sm / sm / – |
| 27 | **CXCR4** | P61073 | `cxcr4_human` | A | `001_003_002` | 8U4N 2.72Å EM 2024-03-13 | 8U4R 3.1Å EM 2024-03-13 | both | I:fid | C P **B** | pep;prot;sm / pep;sm / C |
| 28 | **DRD2** | P14416 | `drd2_human` | A | `001_001_004` | 8TZQ 3.2Å EM 2024-08-21 | 6CM4 2.87Å X 2018-03-14 | both | A:fid I:fus | pre-all | sm / sm / c |
| 29 | **DRD3** | P35462 | `drd3_human` | A | `001_001_004` | 8IRT 2.7Å EM 2023-06-07 | 3PBL 2.89Å X 2010-11-03 | ours | A:fus+fid I:fus+mut3 | C | sm / sm / C |
| 30 | **DRD4** | P21917 | `drd4_human` | A | `001_001_004` | 8IRU 3.2Å EM 2023-06-21 | 5WIU 1.96Å X 2017-10-18 | CN | A:fid I:fus | C P **B** | sm / sm / – |
| 31 | **EDNRA** | P25101 | `ednra_human` | A | `001_002_007` | 8HCQ 3.01Å EM 2023-03-22 | 8XVK 3.21Å EM 2024-08-28 | both | A:fus+fid I:fus+fid | C P | prot / sm / C |
| 32 | **EDNRB** | P24530 | `ednrb_human` | A | `001_002_007` | 8IY5 2.8Å EM 2023-08-16 | 5GLI 2.5Å X 2016-09-07 | both | A:fid | C P | pep;prot / pep;sm / C |
| 33 | **FSHR** | P23945 | `fshr_human` | A | `001_003_003` | 8I2G 2.8Å EM 2023-03-29 | 8I2H 6.0Å EM 2023-03-22 | both | A:fid+mut1 | C P | pep;sm / **none** / – |
| 34 | **GHSR** | Q92847 | `ghsr_human` | A | `001_002_010` | 7NA7 2.7Å EM 2021-12-15 | 6KO5 3.3Å X 2020-08-12 | both | A:fid I:fus | C | pep;sm / sm / c |
| 35 | **GPR52** | Q9Y2T5 | `gpr52_human` | A | `001_010_001` | 8HMP 2.77Å EM 2023-06-21 | 6LI2 2.8Å X 2020-02-26 | neither | A:fid I:fus+mut5 | pre-all | sm / **none** / – |
| 36 | **GPR6** | P46095 | `gpr6_human` | A | `001_010_001` | 8TYW 3.43Å EM 2024-12-04 | 8T1V 2.6Å X 2024-12-04 | CN | A:fid I:fus | C P **B** (both) | — / sm / – |
| 37 | **GRPR** | P30550 | `grpr_human` | A | `001_002_003` | 8H0Q 3.3Å EM 2023-08-09 | 7W41 2.95Å X 2023-02-22 | ours | A:fid+mut1 I:fus+mut3 | C P | pep / sm / C |
| 38 | **HRH1** | P35367 | `hrh1_human` | A | `001_001_005` | 8YN2 2.66Å EM 2024-10-09 | 8X5Y 3.0Å EM 2024-01-17 | both | A:fid I:fus | C | sm / sm / c |
| 39 | **HRH2** | P25021 | `hrh2_human` | A | `001_001_005` | 8YN3 2.56Å EM 2024-10-09 | 7UL3 3.0Å EM 2022-06-29 | CN | A:fid I:fid | C P **B** | sm / sm / – |
| 40 | **HRH3** | Q9Y5N1 | `hrh3_human` | A | `001_001_005` | 8YN5 2.7Å EM 2024-10-09 | 7F61 2.6Å X 2022-10-26 | both | A:fid I:mut1 | C P **B** | lip;sm / sm / c |
| 41 | **LPAR1** | Q92633 | `lpar1_human` | A | `001_004_003` | 7TD0 2.83Å EM 2022-02-09 | 4Z36 2.9Å X 2015-06-03 | ours | I:fus+mut3 | C P | sm / sm / C |
| 42 | **LSHR** | P22888 | `lshr_human` | A | `001_003_003` | 7FII 4.3Å EM 2021-09-29 | 7FIJ 3.8Å EM 2021-09-29 | both | — | C | prot;sm / **none** / – |
| 43 | **LT4R1** | Q15722 | `lt4r1_human` | A | `001_004_002` | 7VKT 2.9Å EM 2022-03-09 | 7K15 2.88Å X 2021-02-17 | ours | A:fid+mut1 I:fus | C P | sm / sm / C |
| 44 | **MCHR1** | Q99705 | `mchr1_human` | A | `001_002_013` | 8WWK 2.61Å EM 2024-11-13 | 8YNS 3.33Å EM 2024-12-18 | both | A:fid I:fus+fid | C P **B** (both) | pep / sm / C |
| 45 | **MTR1A** | P48039 | `mtr1a_human` | A | `001_005_001` | 7VGY 3.1Å EM 2022-03-02 | 6ME2 2.8Å X 2019-04-24 | CN | A:fid I:fus | C | sm / **none** / – |
| 46 | **MTR1B** | P49286 | `mtr1b_human` | A | `001_005_001` | 7VH0 3.46Å EM 2022-03-02 | 6ME6 2.8Å X 2019-04-24 | neither | A:fid I:fus+mut11 | C P | sm / **none** / – |
| 47 | **NK1R** | P25103 | `nk1r_human` | A | `001_002_029` | 8U26 2.5Å EM 2023-11-15 | 6E59 3.4Å X 2018-12-12 | CN | A:fid I:fus | C P | pep / sm / – |
| 48 | **NPY1R** | P25929 | `npy1r_human` | A | `001_002_020` | 7X9A 3.2Å EM 2022-05-18 | 5ZBQ 2.7Å X 2018-04-25 | ours | I:fus+mut3 | C P | pep / sm / C |
| 49 | **NPY2R** | P49146 | `npy2r_human` | A | `001_002_020` | 8K6N 3.2Å EM 2024-07-31 | 7DDZ 2.8Å X 2021-01-27 | both | A:fid | C P | pep / sm / C |
| 50 | **NTR1** | P30989 | `ntr1_human` | A | `001_002_021` | 8JPF 3.02Å EM 2023-08-09 | 7UL2 2.4Å EM 2022-06-29 | CN | I:fid | pre-all | pep;prot / sm / – |
| 51 | **OPRD** | P41143 | `oprd_human` | A | `001_002_022` | 6PT2 2.8Å X 2019-12-11 | 4N6H 1.8Å X 2013-12-25 | ours | I:fus+mut4 | pre-all | pep;prot;sm / pep;sm / C |
| 52 | **OPRK** | P41145 | `oprk_human` | A | `001_002_022` | 8FEG 2.54Å EM 2023-12-06 | 6VI4 3.3Å X 2020-03-18 | both | A:fid I:fid+mut1 | pre-all | pep;sm / sm / C |
| 53 | **OPRM** | P42866 | `oprm_mouse` | A | `001_002_022` | 5C1M 2.07Å X 2015-08-05 | 7UL4 2.8Å EM 2022-06-29 | CN | A:fid I:fid **mouse** | pre-all | pep;sm / prot;sm / – |
| 54 | **OPRX** | P41146 | `oprx_human` | A | `001_002_022` | 8F7X 3.28Å EM 2022-12-14 | 5DHH 3.0Å X 2015-10-21 | ours | A:fid I:fus+mut3 | C P | pep / sm / C |
| 55 | **OPSD** | P02699 | `opsd_bovin` | A | `001_009_001_vert` | 4X1H 2.29Å X 2015-11-04 | 7ZBC 1.8Å X 2023-03-29 | both | **bovine** | pre-all | sm / sm / – |
| 56 | **OX2R** | O43614 | `ox2r_human` | A | `001_002_023` | 7L1V 3.0Å EM 2021-02-10 | 7XRR 2.89Å X 2022-11-23 | both | A:fid | C | pep;sm / sm / C |
| 57 | **OXYR** | P30559 | `oxyr_human` | A | `001_002_032` | 7RYC 2.9Å EM 2022-03-09 | 6TPK 3.2Å X 2020-08-05 | CN | A:fid | C P | pep / sm / – |
| 58 | **PD2R2** | Q9Y5Y4 | `pd2r2_human` | A | `001_004_008` | 8XXV 2.33Å EM 2024-12-04 | 7M8W 2.61Å X 2021-08-25 | CN | A:fid I:fus | C P **B** | lip / sm / – |
| 59 | **PE2R4** | P35408 | `pe2r4_human` | A | `001_004_008` | 8GDB 3.1Å EM 2024-01-10 | 5YHL 4.2Å X 2018-12-05 | neither | A:fid I:fid+mut5 | pre-all | lip;sm / sm / – |
| 60 | **S1PR1** | P21453 | `s1pr1_human` | A | `001_004_004` | 7TD4 2.6Å EM 2022-02-09 | 3V2Y 2.8Å X 2012-02-15 | neither | I:fus+mut2 | C | pep;sm / sm / – |
| 61 | **S1PR5** | Q9H228 | `s1pr5_human` | A | `001_004_004` | 7EW1 3.4Å EM 2021-09-29 | 7YXA 2.2Å X 2022-08-10 | CN | A:fid I:fus | C | sm / sm / – |
| 62 | **SSR2** | P30874 | `ssr2_human` | A | `001_002_028` | 7T10 2.5Å EM 2022-03-09 | 7XN9 2.6Å X 2022-08-03 | CN | A:fid | C P | pep;prot;sm / pep / – |
| 63 | **TA2R** | P21731 | `ta2r_human` | A | `001_004_008` | 8XJN 3.06Å EM 2024-02-28 | 6IIU 2.5Å X 2018-12-19 | neither | A:fus+fid I:fus+mut1 | C P **B** | sm / sm / – |
| 64 | **TSHR** | P16473 | `tshr_human` | A | `001_003_003` | 7UTZ 2.4Å EM 2022-08-03 | 7T9M 3.1Å EM 2022-08-10 | CN | A:fid | C P | prot / prot / – |

## 6.2 Tier E-B1 — class B1, cross-class transfer (catalogue E7.2)

| # | slug | UniProt | GPCRdb | cl | cluster | active ref | inactive ref | in | QC flags | post-cutoff | agonist / antagonist / BlkC |
|--:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **CALRL** | Q16602 | `calrl_human` | B1 | `002_001_001` | 6UVA 2.3Å EM 2020-04-01 | 7KNT 3.15Å EM 2021-02-24 | CN | A:fid | pre-all | pep / **none** / – |
| 2 | **CRHR1** | P34998 | `crfr1_human` | B1 | `002_001_002` | 6P9X 2.91Å EM 2020-02-05 | 8GTI 2.2Å X 2023-09-13 | ours | A:fid I:mut11 | pre-all | pep / sm / – |
| 3 | **GCGR** | P47871 | `glr_human` | B1 | `002_001_003` | 8WG8 2.71Å EM 2024-03-06 | 5XEZ 3.0Å X 2017-05-24 | ours | A:fid I:fus+fid+mut2 | pre-all | pep / sm / – |
| 4 | **GLP1R** | P43220 | `glp1r_human` | B1 | `002_001_003` | 6X18 2.1Å EM 2020-09-09 | 5VEW 2.7Å X 2017-05-24 | both | A:fid I:fus | pre-all | pep;prot;sm / **none** / – |
| 5 | **PTH1R** | Q03431 | `pth1r_human` | B1 | `002_001_004` | 8FLQ 2.55Å EM 2023-04-26 | 6FJ3 2.5Å X 2018-11-21 | ours | A:fid I:fus+mut40 | pre-all | pep;sm / **none** / – |

## 6.3 Tier E-scope — class F and B2, declared scope, no claim

| # | slug | UniProt | GPCRdb | cl | cluster | active ref | inactive ref | in | QC flags | post-cutoff | agonist / antagonist / BlkC |
|--:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **AGRE5** | P48960 | `agre5_human` | B2 | `003_001_002` | 8IKL 2.33Å EM 2024-01-24 | 8IKJ 3.2Å EM 2024-02-14 | CN | I:fus | C P **B** (both) | — / **none** / – |
| 2 | **FZD4** | Q9ULV1 | `fzd4_human` | F | `006_001_001` | 8WMA 3.47Å EM 2024-09-11 | 6BD4 2.4Å X 2018-08-22 | ours | I:fus+mut4 | C P **B** | — / **none** / – |
| 3 | **FZD6** | O60353 | `fzd6_human` | F | `006_001_001` | **none under rule R** | **none under rule R** | ours | — | C P **B** | — / **none** / – |
| 4 | **FZD7** | O75084 | `fzd7_human` | F | `006_001_001` | 9EW2 3.2Å EM 2024-10-02 | 9EPO 1.9Å EM 2024-10-02 | both | A:fid | C | — / **none** / – |
| 5 | **SMO** | Q99835 | `smo_human` | F | `006_001_001` | 6XBM 3.15Å EM 2020-09-30 | 7ZI0 3.0Å X 2022-06-15 | both | A:fid I:fus | pre-all | sm / sm / – |

## 6.4 Tier X — excluded, with the clause that excluded it

| # | slug | UniProt | GPCRdb | cl | cluster | active ref | inactive ref | in | QC flags | post-cutoff | agonist / antagonist / BlkC |
|--:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **ACM3** | P20309 | `acm3_human` | A | `001_001_002` | **none under rule R** | **none under rule R** | CN | — | C P | — / **none** / – |

### Why the two exclusions are exclusions

**ACM3** is Class A and has both states, but only by pairing human `8E9Z` (2.69 Å cryo-EM,
active) with **rat** `4U15` (2.80 Å X-ray, inactive). ConfoRNets includes it and does not
disclose the pairing (`lit/panels/README.md`). Our current panel has **zero** cross-species
pairs and that is worth keeping: a within-receptor conformational contrast that is in fact a
cross-species contrast puts sequence difference inside the very comparison the predicate is
meant to measure. If Aditya wants it, it is a one-line rule change — drop the species clause
in Rule P — and it must then be declared in Methods, because it also readmits NTR1's
rat/human pairing that Rule P currently resolves in favour of an all-human pair.

**FZD6** has an active structure (`8JH7`, 3.2 Å cryo-EM) and **no inactive structure anywhere
in the snapshot**. It is the only one of our current 48 that fails the both-states
requirement, confirming catalogue §0.3 item 3. It stays in E-scope as declared instrument
scope — it carries no state claim today and should carry none after the redo.

---

# 7. Paralog clusters — the bootstrap unit, and a defect in the current map

Every confidence interval in this project is a cluster bootstrap, so the cluster map is
load-bearing. The one in use, `data/block_b/09_references/paralogy_clusters.csv`, is honest
about its own provenance: *"no on-disk canonical map found; Phase 0 addendum cites 26
clusters but ships no file"* — it was **reconstructed on 2026-09-09 from standard GPCR-family
taxonomy**, covers only the 40 Class A receptors, and every Block B bootstrap uses it.

**Proposal: derive the cluster from GPCRdb's own family code**, `family` truncated to three
fields (`001_003_002` = chemokine receptors). It is in the snapshot, it extends to all 75
receptors in this document at zero cost, it is reproducible, and it is not a judgement call.

**Where it disagrees with the current map — and the disagreement matters.** At depth 3 the
GPCRdb taxonomy conflicts with the reconstructed map in exactly four places, and in all four
the current map **splits** what GPCRdb keeps together:

| GPCRdb family | current map splits it into | verdict |
|---|---|---|
| `001_001_003` adrenoceptors | `adrenergic_alpha` + `adrenergic_beta` | **split not defensible** — α and β adrenoceptors are paralogs, and ADRB1/ADRB2 are the least independent pair on the panel |
| `001_003_002` chemokine receptors | `chemokine_ccr` + `chemokine_cxcr` | **split not defensible** |
| `001_002_022` opioid receptors | `opioid` + `opioid_nociceptin` | **split not defensible** — OPRX is an opioid-family paralog |
| `001_009_001` opsins | `opsin_vertebrate` + `opsin_invertebrate_jsr1` | **split is right** — bovine rhodopsin and a jumping-spider opsin are not paralogs in any useful sense |

So the current map has **26 clusters over 40 receptors where the taxonomy supports 23**.
A bootstrap that resamples 26 independent units when 23 exist produces intervals narrower
than the data support, on three of the paper's largest receptor families. **This is a real
defect in every Block B interval and it is free to fix.** The recommended map keeps the opsin
split as a single documented override; the column is `cluster_gpcrdb_fam3` and the override is
encoded as `001_009_001_vert` / `001_009_001_inv`.

Over the 64-receptor core the recommended map gives **32 clusters, 16 of them singletons**.
The largest are chemokine (7), then serotonin / adrenoceptor / opioid (4 each). That is the
real n for any receptor-level interval the redo reports, and it is the number to put in a
power statement — not 64.

---

# 8. Post-cutoff status, and the holdout that can actually be powered

Per-backbone cutoffs are taken from `data/block_d/09_references/nanobody_state_anchors.csv`,
which carries them as columns: **Chai-1 2021-01-12, Protenix 2021-09-30, Boltz-2 2023-06-01,
OpenFold3 TBD.** Computed on the **rule-R active reference**, over the 64-receptor core:

| cutoff | active reference post-cutoff | clusters | pre-cutoff | clusters |
|---|---:|---:|---:|---:|
| Chai-1 2021-01-12 | 42 | 27 | 22 | 13 |
| **Protenix 2021-09-30** | **32** | **23** | **32** | **20** |
| Boltz-2 2023-06-01 | 12 | 8 | 52 | 30 |

Both states post-Boltz-2: **5** — `ADA1A CCR8 CXCR3 GPR6 MCHR1` — spanning **4** clusters.
Active post-Boltz-2: **12** — the twelve the catalogue names, reproduced exactly.

**The design is not the problem; the power is.** The Boltz-2 stratum is 12 receptors in 8
clusters against 52 in 30. Against the exemplars the lit session identified —
`feldman2026alphainterp` n=200 per arm, `kim2026mac1` n=550 — an 8-cluster arm cannot
support a claim about a modest difference in ladder height. It can support a bounded one.

**Three recommendations, in order:**

1. **Make Protenix's 2021-09-30 the primary date stratification.** It splits the core
   **32 / 32, 23 clusters against 20** — a balanced, well-powered, pre-registrable split that
   needs no panel change at all, because the panel is already a census. Report Boltz-2's
   12/52 as the secondary, explicitly under-powered stratum, and say so in the sentence that
   reports it.
2. **Quantify the residual, `chiesa2025templatebias`-style.** The strongest number available
   is already computed: **GPCRdb records a G-protein complex for 58 of the 64 core active
   references**, and records no transducer for **6** — `AA2AR ADRB1 AGTR1 NTR1 OPRD OPRM`. So
   "supplying a cognate Gα to a model trained on such complexes is closer to naming a
   deposited structure" (`methods.tex:230`) applies to **91%** of the panel, and there are six
   receptors where the annotation says the active state was solved without one. That is a
   residual-exposure stratum the project has never named and it costs no new predictions to
   define. **Verify the six before using them**: GPCRdb's `signalling_protein` field is not
   complete — NTR1's rule-R active reference `8JPF` is titled *"Focused refinement structure
   of NTSR1 in NTSR1-GRK2-Galpha(q) complexes"* and plainly does contain a Gα, so the true
   stratum is at most five and possibly smaller. The field to trust is the deposited entity
   list in `panel_reference_qc.csv`, not the snapshot's annotation.
3. **State the power before running it.** The catalogue's E7.4 (inject a known effect, report
   the fraction of cluster-bootstrap replicates excluding zero) should be run on the 8-cluster
   stratum *before* it is dispatched. If it cannot resolve the effect size we care about, say
   so in Methods and report the stratum as a bound rather than a test.

---

# 9. Quality flags — what is recorded, what cannot be checked yet

Over the 64 core rule-R reference pairs (128 structures):

| flag | active refs | inactive refs |
|---|---:|---:|
| fusion partner inside the **receptor** polymer entity | 7 | 40 |
| nanobody / scFv / Fab / megabody in the deposited assembly | 52 | 14 |
| ≥1 engineered substitution in RCSB's receptor-entity record | — | see below |
| non-human | 3 receptors: B1B1U5 (*Hasarius adansoni*), OPRM (*Mus musculus*), OPSD (*Bos taurus*) | |

Pair mutation totals (RCSB floor): 40 receptors at 0, 7 at 1, 3 at 2, 6 at 3, 3 at 4,
3 at 5, 1 at 7, 1 at 11.

The active/inactive asymmetry is itself a finding worth reporting: **inactive references are
overwhelmingly fusion constructs (40 of 64) and active references are overwhelmingly
fiducial-stabilised (52 of 64).** The two roles of the predicate are not measured on the same
kind of object, on any panel, ours or ConfoRNets'.

**Three things this file cannot yet establish, and the honest label is *unresolved*:**

1. **Whether the predicate anchors are resolved in every reference.** The rule needs it and
   I cannot check it without coordinates. What the held files do say is worse than expected:
   in `reference_set.blockb_pinned.csv`, **`d_gpcrdb_tm6_tilt_ref` is populated on all 162
   rows and `d_npxxy_oh_ref` on only 64**, and the split is not random — **all 93 on-panel
   rows carry the tilt axis, 64 carry both, and all 69 off-panel rows carry the tilt axis and
   *zero* carry the NPxxY axis.** Only **28 receptors** have both roles measured on both axes,
   fewer than the 40 we currently claim. So the NPxxY axis has never been computed for a
   single expansion candidate. Measuring it on the 128 core references is `free*` in the
   catalogue's sense — no inference, a download and a measurement pass — and it is a
   prerequisite for E0.1, not an optional extra. **31 of the 128 rule-R references are not in
   the pinned set at all** and have never been measured on either axis.
2. **The true engineered-substitution count.** RCSB's `pdbx_mutation` is the only machine-
   readable source and `methods.tex:303` demonstrates it is empty for ten of fifteen
   verified mutants. Every `mutN` in §6 is a floor. The method that works is
   `analysis/verify_partner_chains.py`'s: align the deposited sequence to canonical UniProt.
   Running it on the 128 **receptor** chains is the free* job that makes rule R's step 3(a)
   trustworthy; until then the ranking is approximate and the ≤1-cap arithmetic in §4 is a
   lower bound on what a cap would remove.
3. **Register.** `6E67` is the documented case — right state, wrong register, and no metric
   we hold catches it. Nothing in this file detects it either. It is not in the core panel's
   rule-R picks, but the class of defect is not screened anywhere, and a register check on
   128 references is not something I can specify from metadata.

**The CFTR-class check was run and is clean.** Every one of the 963 candidate structures was
fetched with its `struct.title` and its per-entity `pdbx_description`; no entry's receptor
polymer entity describes a protein of a different family. One near-miss worth recording:
**`7LD3`, the rule-R and current active reference for AA1R, is deposited as "Chimera protein
of Muscarinic acetylcholine receptor M4 and Adenosine receptor A1"** — a receptor-receptor
chimera, correctly assigned to `aa1r_human` by GPCRdb, but the only such construct in the
core panel and one that a partner-chain or anchor check should look at first.

---

# 10. Ligands

Source: the `ligands` array in the GPCRdb snapshot, which carries `function`
(Agonist / Antagonist / Inverse agonist / PAM / NAM / …), `type` (small-molecule, peptide,
protein, lipid) and, for 1,269 of 1,828 ligand records, a **SMILES string**. For Block C
receptors the delivered census `data/block_c/12_g4_off_site_census/g4_full_census_v2.csv`
also names the ligand actually used, per prediction.

| | count |
|---|---:|
| core receptors with ≥1 agonist and ≥1 antagonist record | **57 of 64** |
| …with a SMILES for both | 39 |
| core receptors with **no antagonist record at all** | **6** — `APJ FSHR GPR52 LSHR MTR1A MTR1B` |
| core receptors with **no agonist record at all** | **1** — `GPR6` (orphan; its only annotated ligands are inverse agonists) |
| core receptors whose only agonists are peptide or protein | **17** — `AGTR1 C5AR1 CCR2 CCR5 CCR6 CXCR2 EDNRA EDNRB GRPR MCHR1 NK1R NPY1R NPY2R NTR1 OPRX OXYR TSHR` |
| Block C ran both an agonist and an antagonist | 28 |
| Block C ran only one role | 8 |
| Block C did not run at all | 4 of our 40 — `B1B1U5 FSHR LSHR OPSD` (caveat `C-C-9`, "36 of 40 landed") |

**Consequences for the ligand axis (catalogue E2.1/E2.2), which are panel facts, not run
facts:**

- The 2×2 of *ligand presence × partner presence* cannot be crossed on the full core. Six
  receptors have no antagonist to supply and GPR6 has no agonist to supply. **57 is the
  maximum, not 64**, and the honest denominator for the interaction estimate is the 57, or 28
  if it must be restricted to what Block C already scored.
- "Usable chemical representation" is not one thing. For 17 receptors the agonist is a
  **peptide or a protein**, so the ligand co-input is a chain, not a SMILES — which changes
  what "ligand alone" means and makes the agonist arm for those receptors structurally
  similar to the partner arm the paper is trying to contrast it with. **That confound is a
  property of the panel and it should be declared, not discovered in the results.** A
  `ligand_modality` covariate is in `panel_systems.csv` (`agonist_modalities`,
  `antagonist_modalities`) and every ligand-axis result should be reported split on it.
- FSHR and LSHR have glycoprotein-hormone agonists and no antagonist at all; together with
  B1B1U5 (retinal) and OPSD (retinal) these are the four Block C could not run, and the
  reason is chemical, not operational. Expect the same four to be absent again.

---

# 11. What changes if this panel is adopted

| | now | proposed |
|---|---|---|
| Class A receptors | 40, no stated rule | **64**, Rule P, a census |
| class B | 4 (CRHR1 GCGR GLP1R PTH1R) | 5 — **CALRL added**, the only both-state B1 we lack |
| class F / B2 | 4 (FZD4 FZD6 FZD7 SMO) | 5 — AGRE5 added for ConfoRNets comparability; declared scope, no claim |
| receptors added | — | **24 Class A** + CALRL + AGRE5 |
| cross-species pairs | 0 | 0 (ACM3 excluded; NTR1 resolved to an all-human pair) |
| non-human receptors | 2 (OPSD, B1B1U5) | **3** — OPRM (*Mus musculus*) joins. No sentence may call this panel human. |
| paralog clusters | 26, reconstructed, Class A only | **32**, from GPCRdb family codes, all classes |
| reference pairs | pinned, no stated rule | Rule R, 80% concordant with the only published rule in the corpus |
| ConfoRNets test cases covered | 27 of 51 Class A / 30 of 51 | **45 of 46 Class A; 50 of 51 overall** |

**The 24 Class A receptors added** are exactly the catalogue's §0.2 list:
`5ht2a ada1a c5ar1 ccr2 ccr6 ccr8 cxcr3 drd4 gpr52 gpr6 hrh2 mtr1a mtr1b nk1r ntr1 oprm oxyr
pd2r2 pe2r4 s1pr1 s1pr5 ssr2 ta2r tshr`. **Nineteen are ConfoRNets test cases**
(`PANEL_EXPANSION_CLASS_A.md` §1 lists them, and its 19 is correct for its universe). The
**six that no paper in the corpus names** are `C5AR1 GPR52 MTR1B PE2R4 S1PR1 TA2R` — GPCRdb
leads, not corpus findings, and `PANEL_EXPANSION.md` §4's list of database-only candidates
contains three of them plus GLR and MTR1B. That §4 list is the one with the two documented
traps: **GLR is our GCGR** (`glr_human`, 13 active / 5 inactive) and it is not a gap, and
**PE2R4 is omitted from it** although it has 6 active / 2 inactive and is on no panel.
Both traps are handled here by mapping through the GPCRdb protein identifier rather than by
lowercasing a slug — and `CRHR1` is the third instance of the same trap, resolving as
`crfr1_human` in GPCRdb and, as of this retrieval, as **`CRHR1_HUMAN` (P34998) in UniProt,
which has renamed the entry**. It is the only one of 86 accession lookups that failed on the
entry name and had to be recovered by gene symbol; the failure is recorded in the header of
`panel_uniprot.tsv`. **Any slug→identifier mapping must fail loudly on an unresolved name.**
The build script that produced these files asserts on unresolved input and does not skip.

**Twenty-five of the 72 comparable reference slots on our existing 40 receptors change under
rule R.** They are listed in `panel_systems.csv` (`our_active` / `our_inactive` against
`gdb_active` / `gdb_inactive`). Three are worth naming because they are decisions, not
bookkeeping:

- **AA2AR**: our `5G53` active → `8WDT`. ConfoRNets picked `6GDG` (4.11 Å) over our `5G53`
  (3.40 Å), and `PANEL_EXPANSION_CLASS_A.md` §2 reads that as implying 5G53 is more heavily
  engineered. Rule R agrees that 5G53 is not the best pick and selects a *third* structure.
  AA2AR is the recurrently anomalous receptor (C-B-8). **Re-scoring AA2AR against all three
  costs no new predictions and is the cheapest test of the standing anomaly.**
- **B1B1U5**: our pinned `9EPR` active → **`9EPP`**, by rule 3, and **rule 4 does not
  override it** — 9EPR is a human/bovine *in-vitro* reconstitution, so there is no native
  option and rule 4's second clause is never satisfied (§4, corrected 2026-09-12; D-H
  decided as option (c′)). It is still the case that proves the panel cannot be selected on
  receptor-entity metadata alone: nothing about the *receptor* entity distinguishes the two,
  and what distinguishes them is a spider-Gαq1-tipped Gα and a swapped βγ.
- **ADRB2 inactive**: our `6PS2` → `2R4R`. Both are T4L fusions; the change is driven by
  RCSB's mutation record, which §9 says is a floor. **Do not action this one before the
  sequence-level substitution audit runs.** {ref-history}


---

# 12. Traps from the brief, re-verified

| trap | status |
|---|---|
| `PANEL_EXPANSION.md` §4 lists GLR as a gap; GLR_HUMAN is our GCGR | **confirmed.** Mapping is through GPCRdb protein identifiers; GCGR↔`glr_human` and CRHR1↔`crfr1_human` both resolve, neither by lowercasing |
| The §4 list omits PE2R4 | **confirmed.** PE2R4 has 6 active / 2 inactive and is in tier C1 |
| A drop once shipped CFTR for an opioid complex | **checked, clean.** All 963 candidate structures fetched with `struct.title` and per-entity descriptions; no cross-family substitution. One receptor-receptor chimera found (7LD3, M4/A1) and flagged |
| OPSD/4X1H annotated `native`, carries an engineered 11-mer | **confirmed, and it survives into the proposed panel.** Rule R selects 4X1H / 7ZBC for OPSD (*Bos taurus*, 2.29 Å / 1.80 Å) — the same pair we already use. The defect is not re-derivable from metadata: RCSB's mutation record for that entity is empty, because the peptide is deposited as its own molecule rather than as a mutant of the subunit it derives from (`methods.tex:286`). **No rule written on receptor-entity metadata can catch it**, which is the argument for rule R step 4 and for the sequence-level audit in §9.2. Until that audit runs, OPSD is the one core receptor whose active reference is known to be mis-annotated |
| 6E67 register mismatch | **not detected by anything in this file.** Unresolved, §9.3 |
| Three numbers for the ConfoRNets overlap (29/27/30) | **all three are right.** §2 gives the rule for each and names ADRB1 as the whole difference |
| Never let `_human` be a silent default | **enforced.** Rule P step 1 chooses the species explicitly and records it; three non-human receptors survive into the core and a fourth (ADRB1 turkey) is in ConfoRNets but not in our pairs |
| Never pipe an existence check through `head` | observed; the 963-entry fetch and the 192-entry holdings check are exhaustive, not sampled |

**One new trap, for whoever builds the next panel:** *the GPCRdb snapshot is not validated
against PDB holdings.* It served `7EVW` as a current 3.22 Å entry twenty-eight months after
the PDB obsoleted it. The cheap check is that RCSB's GraphQL `entries` endpoint returns
nothing for a removed entry.

---

# 13. What I could not resolve

1. **Predicate-anchor completeness** on the 128 core references. Needs coordinates. §9.1.
2. **True engineered-substitution counts**, needed for rule R step 3(a) and for any mutation
   cap. Needs a sequence-level alignment pass. §9.2.
3. **Register correctness** of any reference. No metric we hold catches it. §9.3.
4. **The OpenFold3 training cutoff.** Still `TBD` in
   `data/block_d/09_references/nanobody_state_anchors.csv` and still `[PI]` in
   `methods.tex:225`. Every post-cutoff column here is blank for that backbone. **The
   date-stratified holdout cannot be reported per-backbone for one of four backbones until
   this is answered.**
5. **Whether GPCRdb's `Active`/`Inactive` annotation should gate membership at all.** It is
   the same annotation our predicate is meant to adjudicate. See Q3 below — this is the one
   open question I would not decide without the corpus.

---

# Questions for lit

1. **Does any paper in the corpus state a GPCR panel rule that does *not* select on the state
   annotation?** Rule P inherits GPCRdb's `Active`/`Inactive` label, which is exactly the
   circularity `methods.tex:117` already flags for our 80 threshold rows, and which
   `PANEL_EXPANSION_CLASS_A.md` §3 flags for ConfoRNets. *What I would do differently:* if
   such a rule exists, adopt it and cite it. If none does, I would keep Rule P but add a
   mandatory reporting line — **panel membership under GPCRdb's label, and again under our
   own recalibrated predicate (catalogue E0.1)** — and report any receptor where the two
   disagree as a result rather than as a panel decision. That second line is cheap once E0.1
   has run off-panel, and it converts the circularity from an objection into a measurement.

2. **Do `paajanen2026activation` or `khaleq2026hyaline` name specific deposited entries whose
   state annotation they find incorrect?** `paajanen2026activation` p.3 says its coordinate
   recovers entries "whose state of activity was originally interpreted incorrectly".
   *What I would do differently:* if named entries are in our 128 rule-R references, I would
   promote the demotion of those specific structures into Rule R as a step 2b with a citation,
   rather than leaving it to a general caveat. If the paper names none, Rule R stays as
   written and the caveat stays general.

3. **Is there a corpus paper that reports a receptor-level paralog or family clustering used
   for resampling — and at what granularity?** §7 proposes GPCRdb family depth 3 (32 clusters
   over 64 receptors) against the current reconstructed 26-over-40. *What I would do
   differently:* if a published GPCR benchmark resamples at a coarser unit (ligand class, or
   GPCRdb depth 2, which would give 11 clusters here), our intervals are still too narrow and
   I would switch the recommendation. If published practice is per-receptor with no
   clustering, I would keep depth 3 and report the per-receptor interval alongside as an
   explicit upper bound on confidence.

4. **Do any of the six GPCRDB-only additions — `C5AR1 GPR52 MTR1B PE2R4 S1PR1 TA2R` — appear
   in a corpus paper's panel under a different name?** `lit/panels/panels.csv` covers four
   papers; these six are named by none of them. *What I would do differently:* a hit changes
   nothing about membership (Rule P admits them regardless) but it would let the added
   receptors be described as corpus-supported rather than database-only, which matters for how
   §11's table reads. GPR52 is the one I would check first: it is an orphan, self-activated
   receptor with **no antagonist structure at all**, and if a corpus paper treats it as a
   special case we should say so rather than let it fail the ligand axis silently.

5. **`tran2026nanogs` used β2AR.** Is any *other* receptor in the corpus's wet-lab literature
   a venue where a Gα α5-CT peptide has been tested? *What I would do differently:* catalogue
   C4 requires the length ladder to carry a helicity readout so it can be discussed against
   that paper. If a second receptor exists, I would flag it in `panel_systems.csv` as a
   priority for any single-backbone pilot, so the pilot lands on a receptor with wet-lab
   comparanda rather than on whichever receptor is cheapest.

6. **`hilger2020gcgr` makes class B the sharpest venue for a length ladder (E7.2), but tier
   E-B1 is five receptors in four clusters.** Does the corpus contain a class B1 both-state
   benchmark larger than five? *What I would do differently:* five receptors cannot support a
   class-transfer claim, only a bounded one. If a larger set exists — even one not in
   GPCRdb's both-state census, e.g. one built from an intermediate or a modelled inactive —
   I would extend E-B1 to it and say what the additional references are. If not, E7.2 should
   be pre-registered as a bounded comparison from the start, with the n stated in the
   hypothesis.

---

# Files written by this session

*(§14, the appendix on the pending strict-ConfoRNets decision, follows this section.)*

```
redo/spec/PANEL.md              this file
redo/inputs/panel_systems.csv     75 receptors × 138 columns   b1a115a1…5fa1b5f3
redo/inputs/panel_reference_qc.csv 962 structures × 15 columns  (regenerated)
redo/inputs/panel_uniprot.tsv     86 UniProt records            f0a8ecf8…0cda422
redo/cache/panel_rcsb_cache.json raw RCSB responses, 962 entries
redo/cache/panel_rcsb_status.json RCSB holdings status, 192 entries
redo/gates/panel_verify.py       recomputes every checkable number in this file
redo/inputs/panel_gpcrdb_degree.csv      1,716 rows — GPCRdb activation degree (§14)
redo/inputs/panel_gpcrdb_constructs.csv  1,716 rows — GPCRdb mutation counts (§14)
redo/inputs/panel_strict_confornets.csv  71 rows — the strict rule's output, evidence only
redo/build/panel_strict_confornets.py   the strict rule, executable
redo/build/panel_strict_columns.py      writes the passes_strict filter columns
```

```bash
python3 redo/gates/panel_verify.py    # 82 checks; exits non-zero and names the failure
```

**Every number in this document that can be recomputed from a file is recomputed by
`panel_verify.py`**, including the three frozen input SHAs, so a snapshot refresh fails
loudly rather than silently changing the panel. It was proved non-silent by planting a
defect: with the core size expectation changed from 64 to 63 it reports
`FAIL core panel size` and exits 1. It caught one real error while this file was being
written — a transducer count computed against an earlier version of the reference picks —
which is recorded as corrected in §8, not smoothed.

No file outside `redo/` was created or modified. No git command was run.

---
---

# 14. Appendix — evidence for the pending strict-ConfoRNets decision

**The working panel is the relaxed 64 of §§1–13. There is no second list.** The PI's
instruction is *"come back with a relaxed 64, and then we decide later"*, so everything the
strict question needs is carried as **filter columns on the one table** and the decision is a
one-line selection whenever he wants to make it:

```python
import csv
rows = list(csv.DictReader(open('redo/inputs/panel_systems.csv')))
core   = [r for r in rows if 'C1' in r['tier'].split('|')]              # the working 64
strict = [r for r in core if r['passes_strict'] == 'TRUE']              # 61, whenever wanted
unres  = [r for r in core if r['passes_strict'] == 'UNRESOLVED']        # currently 0 — never treat as FALSE
```

| column in `panel_systems.csv` | values |
|---|---|
| `confornets_member` | TRUE / FALSE — is this receptor one of their published 51 |
| `ref_activation_degree` | GPCRdb degree for **our** active reference, or `UNRESOLVED`, or `NO_REFERENCE` |
| `n_mut_active`, `n_mut_inactive` | GPCRdb mutation count for our two references, same three states |
| `passes_strict` | TRUE / FALSE / **UNRESOLVED** — does *some* pair for this receptor satisfy their published rule |
| `strict_active_pdb`, `strict_inactive_pdb` | the pair the strict rule would use |
| `strict_fail_reason` | why, in words, when `passes_strict` is FALSE |

**`UNRESOLVED` is a first-class value and is never silently read as FALSE.** As it happens
there are **zero UNRESOLVED cells in all 75 rows** — GPCRdb publishes an activation degree
for 1,591 of 1,716 structures and a mutation count for all 1,716, and none of the gaps falls
on a panel receptor or on a candidate that would change a verdict. Two rows carry
`NO_REFERENCE` rather than a value (ACM3 and FZD6, which Rule R pairs no references for);
that is a distinct state and the column says so. **Nothing in the 64 was gated on this
retrieval**, and if the retrieval had failed the panel would have shipped with three
unresolved columns and an ask attached.

**Of the working 64: `passes_strict` is TRUE for 61, FALSE for 3, UNRESOLVED for none.**
The three are named in §14.5. The rest of this appendix is the evidence behind those columns
and behind the eventual decision; it does not propose a different panel.

## 14.1 The two fields we did not hold, and where they came from

The rule has four criteria and **two of them cannot be evaluated from
`lit/panels/cache/gpcrdb_structures.json`**, which carries no activation degree and no
mutation count. Both were retrieved from GPCRdb itself on 2026-09-11 and written to new
companions; the cache was not touched.

| criterion | field | source | companion |
|---|---|---|---|
| (i) 100% activation degree | `Degree active (%)` | GPCRdb structure browser, `gpcrdb.org/structure/` | `redo/inputs/panel_gpcrdb_degree.csv` |
| (ii) an inactive structure exists | `state` | the cached snapshot | — |
| (iii)/(iv) fewest / ≤1 engineered mutation | `Mutations` | GPCRdb **construct browser**, `gpcrdb.org/construct/` | `redo/inputs/panel_gpcrdb_constructs.csv` |

**Both companions were validated against the cached snapshot before use**: each parses to
exactly **1,716 rows**, the PDB sets are identical in both directions (0 in one and not the
other), and the `state` label disagrees on **0 of 1,716** entries. So the scrape is the same
GPCRdb release as our frozen cache, with two columns added. Resolution agrees to the
browser's 1-decimal rounding. A first parse silently dropped 334 rows because 334 `<tr>`
tags carry a `class="repr-st"` attribute before `model_id`; the row count is asserted
against 1,716 in `panel_verify.py` so that failure cannot recur silently.

Coverage of the two new fields: **1,591 of 1,716 structures carry a numeric activation
degree** (125 are published as `-`), of which **991 are exactly 100**. Mutation counts are
published for all 1,716: 1,455 at zero, 95 at one, 166 above one.

**Option 2 was not needed and that is worth saying.** The coordinator's fallback was to
count substitutions by diffing the deposited sequence against canonical UniProt, the way
`analysis/verify_partner_chains.py` does. GPCRdb publishes the count itself, for every
structure, with no gaps — so no receptor is UNRESOLVED on the mutation criterion and nothing
here is inferred. **The sequence-diff job is still owed**, because §14.2 shows GPCRdb's count
and RCSB's disagree badly and neither has been checked against a sequence; but it is not
blocking the strict list.

## 14.2 GPCRdb's mutation count and RCSB's disagree on a third of entries

Over the 962 structures for which both are available, the two counts are **identical on 636
(66%)**. RCSB reports ≥1 where GPCRdb reports 0 on 163 entries, and GPCRdb reports ≥1 where
RCSB reports 0 on 33.

The decisive cases go GPCRdb's way. **`4BVN`, the ultra-thermostabilised turkey β1 that is
ConfoRNets' own ADRB1 inactive reference, carries 11 mutations in GPCRdb and 1 in RCSB**;
its RCSB title is literally *"Ultra-thermostable beta1-adrenoceptor with cyanopindolol
bound"*. `2YDV`, the thermostabilised A2A, is 5 in GPCRdb and 1 in RCSB. This is the same
failure mode `methods.tex:303` documents for partner chains — RCSB's `pdbx_mutation` is
null far more often than it is wrong — and it means **§4's ≤1-cap arithmetic, which used
RCSB, understated the cap's cost.** The strict rule below uses GPCRdb's count, which is what
ConfoRNets used; §4's table is left as written and superseded here.

## 14.3 The strict list: 71 pairs, 62 Class A

`redo/build/panel_strict_confornets.py` implements the rule exactly: active member must
have `Degree active = 100`; an inactive structure must exist for the same GPCRdb protein
entry; each member must carry **≤1 mutation**; within each state rank by fewest mutations
then best resolution. **No species constraint is applied, because their rule states none.**

| | |
|---|---:|
| pairs retained | **71** |
| …Class A (62 entries, **61 slugs**) | 62 |
| …class B1 / B2 / F / T2 | 4 / 2 / 2 / 1 |
| receptors with both states that **fail the cap** | 4 |
| receptors UNRESOLVED for want of a mutation count | **0** |
| non-human | 4 — B1B1U5 (spider), NTR1 (**rat**), OPRM (mouse), OPSD (bovine) |

Cap sensitivity, holding every other criterion fixed: **≤0 → 64, ≤1 → 71, ≤2 → 73, ≤3 → 74,
no cap → 75.** The cap is nearly free at today's GPCRdb: it costs **four receptors**, not
the eighteen the coordinator's calibration suggested. §14.4 explains why.

| # | slug | UniProt | GPCRdb | cl | active PDB | deg | mut | Å | inactive PDB | mut | Å | in CN51 | in Rule-P C1 |
|--:|---|---|---|---|---|--:|--:|--:|---|--:|--:|---|---|
| 1 | **5HT1B** | P28222 | `5ht1b_human` | A | 6G79 EM | 100 | 0 | 3.78 | 4IAR X | 1 | 2.7 | yes | yes |
| 2 | **5HT2A** | P28223 | `5ht2a_human` | A | 8UWL EM | 100 | 0 | 2.8 | 7WC8 X | 0 | 2.45 | yes | yes |
| 3 | **5HT2C** | P28335 | `5ht2c_human` | A | 8DPF EM | 100 | 0 | 2.84 | 8ZMF X | 0 | 3.6 | yes | yes |
| 4 | **5HT5A** | P47898 | `5ht5a_human` | A | 7UM5 EM | 100 | 0 | 2.73 | 7UM4 X | 0 | 2.8 | — | yes |
| 5 | **AA1R** | P30542 | `aa1r_human` | A | 7LD3 EM | 100 | 0 | 3.2 | 5UEN X | 1 | 3.2 | yes | yes |
| 6 | **AA2AR** | P29274 | `aa2ar_human` | A | 5G53 X | 100 | 1 | 3.4 | 4EIY X | 0 | 1.8 | yes | yes |
| 7 | **ACM2** | P08172 | `acm2_human` | A | 6U1N EM | 100 | 0 | 4.0 | 5ZKC X | 0 | 2.3 | yes | yes |
| 8 | **ACM4** | P08173 | `acm4_human` | A | 7TRP EM | 100 | 0 | 2.4 | 5DSG X | 0 | 2.6 | yes | yes |
| 9 | **ADA1A** | P35348 | `ada1a_human` | A | 8THK EM | 100 | 0 | 2.6 | 8HN1 EM | 0 | 2.9 | yes | yes |
| 10 | **ADA2A** | P08913 | `ada2a_human` | A | 9CBL EM | 100 | 0 | 2.8 | 6KUX X | 0 | 2.7 | yes | yes |
| 11 | **ADRB2** | P07550 | `adrb2_human` | A | 8GG0 EM | 100 | 0 | 2.9 | 8JJO EM | 0 | 3.4 | yes | yes |
| 12 | **AGRE5** | P48960 | `agre5_human` | B2 | 8IKL EM | 100 | 0 | 2.33 | 8IKJ EM | 0 | 3.2 | yes | — |
| 13 | **AGRL3** | — | `agrl3_human` | B2 | 7SF7 EM | 100 | 0 | 2.9 | 8JMT EM | 0 | 3.3 | — | — |
| 14 | **AGTR1** | P30556 | `agtr1_human` | A | 7F6G EM | 100 | 0 | 2.9 | 4ZUD X | 0 | 2.8 | — | yes |
| 15 | **APJ** | P35414 | `apj_human` | A | 8XZH EM | 100 | 0 | 2.6 | 8S4D X | 0 | 2.58 | — | yes |
| 16 | **B1B1U5** **spider** | B1B1U5 | `b1b1u5_9arac` | A | 9EPP EM | 100 | 0 | 4.06 | 6I9K X | 0 | 2.15 | yes | yes |
| 17 | **C5AR1** | P21730 | `c5ar1_human` | A | 7Y67 EM | 100 | 0 | 2.8 | 6C1R X | 0 | 2.2 | — | yes |
| 18 | **CALRL** | Q16602 | `calrl_human` | B1 | 6UVA EM | 100 | 0 | 2.3 | 7KNT EM | 0 | 3.15 | yes | — |
| 19 | **CCKAR** | P32238 | `cckar_human` | A | 7MBX EM | 100 | 0 | 1.95 | 7F8Y X | 0 | 2.5 | yes | yes |
| 20 | **CCR2** | P41597 | `ccr2_human` | A | 7XA3 EM | 100 | 0 | 2.9 | 6GPX X | 0 | 2.7 | yes | yes |
| 21 | **CCR5** | P51681 | `ccr5_human` | A | 7O7F EM | 100 | 0 | 3.15 | 6MEO EM | 0 | 3.9 | yes | yes |
| 22 | **CCR6** | P51684 | `ccr6_human` | A | 6WWZ EM | 100 | 0 | 3.34 | 9D3E EM | 0 | 3.02 | yes | yes |
| 23 | **CCR8** | P51685 | `ccr8_human` | A | 8XML EM | 100 | 0 | 2.58 | 8TLM EM | 0 | 2.9 | yes | yes |
| 24 | **CNR1** | P21554 | `cnr1_human` | A | 8GHV EM | 100 | 0 | 2.8 | 7FEE X | 0 | 2.7 | yes | yes |
| 25 | **CNR2** | P34972 | `cnr2_human` | A | 8GUR EM | 100 | 0 | 2.84 | 5ZTY X | 0 | 2.8 | — | yes |
| 26 | **CXCR2** | P25025 | `cxcr2_human` | A | 6LFO EM | 100 | 0 | 3.4 | 6LFL X | 0 | 3.2 | — | yes |
| 27 | **CXCR3** | P49682 | `cxcr3_human` | A | 8HNM EM | 100 | 0 | 2.94 | 8K2W EM | 0 | 3.0 | yes | yes |
| 28 | **CXCR4** | P61073 | `cxcr4_human` | A | 8U4N EM | 100 | 0 | 2.72 | 8U4R EM | 0 | 3.1 | yes | yes |
| 29 | **DRD2** | P14416 | `drd2_human` | A | 7JVR EM | 100 | 0 | 2.8 | 6LUQ X | 0 | 3.1 | yes | yes |
| 30 | **DRD3** | P35462 | `drd3_human` | A | 7CMV EM | 100 | 0 | 2.7 | 3PBL X | 1 | 2.89 | — | yes |
| 31 | **DRD4** | P21917 | `drd4_human` | A | 8IRU EM | 100 | 0 | 3.2 | 5WIU X | 0 | 1.96 | yes | yes |
| 32 | **EDNRA** | P25101 | `ednra_human` | A | 8HCQ EM | 100 | 0 | 3.01 | 8XVK EM | 0 | 3.21 | yes | yes |
| 33 | **EDNRB** | P24530 | `ednrb_human` | A | 8IY5 EM | 100 | 0 | 2.8 | 6IGK X | 0 | 2.0 | yes | yes |
| 34 | **FSHR** | P23945 | `fshr_human` | A | 8I2G EM | 100 | 0 | 2.8 | 8I2H EM | 0 | 6.0 | yes | yes |
| 35 | **FZD7** | O75084 | `fzd7_human` | F | 9EW2 EM | 100 | 0 | 3.2 | 9EPO EM | 0 | 1.9 | yes | — |
| 36 | **GHSR** | Q92847 | `ghsr_human` | A | 7NA7 EM | 100 | 0 | 2.7 | 7F83 X | 0 | 2.94 | yes | yes |
| 37 | **GLP1R** | P43220 | `glp1r_human` | B1 | 6X18 EM | 100 | 0 | 2.1 | 6KK1 X | 0 | 2.8 | yes | — |
| 38 | **GLR** | — | `glr_human` | B1 | 8WG8 EM | 100 | 0 | 2.71 | 5XEZ X | 0 | 3.0 | — | — |
| 39 | **GPR52** | Q9Y2T5 | `gpr52_human` | A | 8HMP EM | 100 | 0 | 2.77 | 6LI0 X | 0 | 2.2 | — | yes |
| 40 | **GPR6** | P46095 | `gpr6_human` | A | 8TYW EM | 100 | 0 | 3.43 | 8T1V X | 0 | 2.6 | yes | yes |
| 41 | **GRPR** | P30550 | `grpr_human` | A | 7W40 EM | 100 | 0 | 3.0 | 7W41 X | 0 | 2.95 | — | yes |
| 42 | **HRH1** | P35367 | `hrh1_human` | A | 8YN2 EM | 100 | 0 | 2.66 | 8X5Y EM | 0 | 3.0 | yes | yes |
| 43 | **HRH2** | P25021 | `hrh2_human` | A | 8YN3 EM | 100 | 0 | 2.56 | 7UL3 EM | 0 | 3.0 | yes | yes |
| 44 | **HRH3** | Q9Y5N1 | `hrh3_human` | A | 8YUU EM | 100 | 0 | 2.7 | 7F61 X | 0 | 2.6 | yes | yes |
| 45 | **LPAR1** | Q92633 | `lpar1_human` | A | 7TD0 EM | 100 | 0 | 2.83 | 4Z35 X | 0 | 2.9 | — | yes |
| 46 | **LSHR** | P22888 | `lshr_human` | A | 7FIH EM | 100 | 0 | 3.2 | 7FIJ EM | 0 | 3.8 | yes | yes |
| 47 | **LT4R1** | Q15722 | `lt4r1_human` | A | 7VKT EM | 100 | 0 | 2.9 | 7K15 X | 0 | 2.88 | — | yes |
| 48 | **MCHR1** | Q99705 | `mchr1_human` | A | 8WWK EM | 100 | 0 | 2.61 | 8YNS EM | 0 | 3.33 | yes | yes |
| 49 | **MTR1A** | P48039 | `mtr1a_human` | A | 7VGY EM | 100 | 0 | 3.1 | 6ME2 X | 0 | 2.8 | yes | yes |
| 50 | **MTR1B** | P49286 | `mtr1b_human` | A | 7VH0 EM | 100 | 0 | 3.46 | 6ME6 X | 0 | 2.8 | — | yes |
| 51 | **NK1R** | P25103 | `nk1r_human` | A | 8U26 EM | 100 | 0 | 2.5 | 6HLP X | 0 | 2.2 | yes | yes |
| 52 | **NPY1R** | P25929 | `npy1r_human` | A | 7VGX EM | 100 | 0 | 3.2 | 5ZBQ X | 1 | 2.7 | — | yes |
| 53 | **NPY2R** | P49146 | `npy2r_human` | A | 7YON EM | 100 | 0 | 2.95 | 7DDZ X | 0 | 2.8 | yes | yes |
| 54 | **NTR1** | P30989 | `ntr1_human` | A | 6OS9 EM | 100 | 0 | 3.0 | 7UL2 EM | 0 | 2.4 | yes | yes |
| 55 | **NTR1** **rat** | P30989 | `ntr1_rat` | A | 8FN1 EM | 100 | 0 | 2.88 | 6YVR X | 1 | 2.46 | yes | yes |
| 56 | **OPRD** | P41143 | `oprd_human` | A | 8F7S EM | 100 | 0 | 3.0 | 4RWD X | 0 | 2.7 | — | yes |
| 57 | **OPRK** | P41145 | `oprk_human` | A | 8FEG EM | 100 | 0 | 2.54 | 4DJH X | 1 | 2.9 | yes | yes |
| 58 | **OPRM** **mouse** | P42866 | `oprm_mouse` | A | 5C1M X | 100 | 0 | 2.07 | 4DKL X | 0 | 2.8 | yes | yes |
| 59 | **OPRX** | P41146 | `oprx_human` | A | 8F7X EM | 100 | 0 | 3.28 | 5DHH X | 0 | 3.0 | — | yes |
| 60 | **OPSD** **bovine** | P02699 | `opsd_bovin` | A | 4X1H X | 100 | 0 | 2.29 | 7ZBC X | 0 | 1.8 | yes | yes |
| 61 | **OX2R** | O43614 | `ox2r_human` | A | 7L1V EM | 100 | 0 | 3.0 | 6TPN X | 0 | 2.61 | yes | yes |
| 62 | **OXYR** | P30559 | `oxyr_human` | A | 7RYC EM | 100 | 0 | 2.9 | 6TPK X | 0 | 3.2 | yes | yes |
| 63 | **PD2R2** | Q9Y5Y4 | `pd2r2_human` | A | 8XXV EM | 100 | 0 | 2.33 | 7M8W X | 0 | 2.61 | yes | yes |
| 64 | **PE2R4** | P35408 | `pe2r4_human` | A | 8GCP EM | 100 | 0 | 3.1 | 5YWY X | 0 | 3.2 | — | yes |
| 65 | **PTH1R** | Q03431 | `pth1r_human` | B1 | 8FLQ EM | 100 | 0 | 2.55 | 6FJ3 X | 0 | 2.5 | — | — |
| 66 | **S1PR5** | Q9H228 | `s1pr5_human` | A | 7EW1 EM | 100 | 0 | 3.4 | 7YXA X | 0 | 2.2 | yes | yes |
| 67 | **SMO** | Q99835 | `smo_human` | F | 6XBM EM | 100 | 0 | 3.15 | 4JKV X | 0 | 2.45 | yes | — |
| 68 | **SSR2** | P30874 | `ssr2_human` | A | 7T10 EM | 100 | 0 | 2.5 | 7XN9 X | 0 | 2.6 | yes | yes |
| 69 | **T2R14** | — | `t2r14_human` | Class T2 (Taste 2) | 8VY7 EM | 100 | 0 | 2.68 | 9IJA EM | 0 | 3.05 | — | — |
| 70 | **TA2R** | P21731 | `ta2r_human` | A | 8XJN EM | 100 | 0 | 3.06 | 6IIU X | 0 | 2.5 | — | yes |
| 71 | **TSHR** | P16473 | `tshr_human` | A | 7UTZ EM | 100 | 0 | 2.4 | 7T9M EM | 0 | 3.1 | yes | yes |
*The four receptors that have both states but fail the ≤1 cap are* **ACM1, ADRB1, FZD4 and
S1PR1** *— each has no qualifying structure in at least one state.*

## 14.4 Reconciliation against their published 51

**Six of ConfoRNets' own 51 pairs violate their own stated rule**, audited against GPCRdb's
fields today:

| test case | violation |
|---|---|
| AA2AR | inactive `5NM4` carries **9** mutations |
| ACM2 | active `7T94` carries **2** |
| ADRB1 | inactive `4BVN` carries **11** |
| CXCR4 | inactive `3OE0` carries **2** |
| DRD2 | inactive `6CM4` carries **3** |
| GLP1R | inactive `5VEW` carries **10** |

45 of 51 satisfy it. The remaining six are either an annotation that GPCRdb has revised since
their snapshot or a rule they did not apply as written; both are possible and the data cannot
separate them. **ADRB1 is the one that is not explainable by drift**: *every* turkey β1
inactive structure in GPCRdb carries **≥8** mutations, minimum 8, so no qualifying ADRB1 pair
has ever existed under their cap. Their own panel contains it anyway.

**At receptor level the strict rule reproduces 49 of their 51** today. The two it does not:

- **ACM3** — no single UniProt entry has both states; `acm3_human` is Active-only (4 entries)
  and `acm3_rat` Inactive-only (5). Their pair is cross-species and undisclosed. Excluded
  here by criterion (ii) read strictly, with no species clause needed.
- **ADRB1** — excluded by the ≤1 cap, per the paragraph above.

**Why 71 today and 51 in their paper: the database grew.** Freezing the strict rule at
successive snapshot dates:

| entries released before | strict pairs |
|---|---:|
| 2022-01-01 | 30 |
| 2023-01-01 | 48 |
| **2023-03-29** | **51** |
| 2023-06-01 | 53 |
| 2024-01-01 | 58 |
| 2025-01-01 and later | 71 |

The rule crosses exactly 51 at a **2023-03-29** cutoff, which is a plausible snapshot date
for their work. **But the count match is not a membership match, and that is the important
half**: at that date the strict rule and their panel share only **35 of 51** receptors. This
is `lit/panels/README.md`'s finding reproduced on a second paper — *"a matching count is not
a matching membership. A count check can only ever falsify a reconstruction, never confirm
one."* Something excludes ~16 receptors their panel omits and the paper does not say what.
**So the strict rule is not a reconstruction of ConfoRNets' panel and must not be described
as one.** It is their stated criteria applied to today's database.

On the shared receptors the strict rule picks **the same reference entry on 67 of 98 slots
(68%)** — lower than the 80% Rule R achieved in §4, because GPCRdb's mutation counts reorder
the ranking and because newer, cleaner structures now exist (5HT2C `8ZMF`, ADRB2 `8JJO`,
CNR1 `7FEE`, GLP1R `6KK1`). `7EVW`, their FZD7 active, is one of the 31: it was obsoleted
2024-04-24 (§3) and the strict rule picks `9EW2`. {ref-alt}


**The 21 receptors the strict rule adds that ConfoRNets does not have** —
`5HT5A AGRL3 AGTR1 APJ C5AR1 CNR2 CXCR2 DRD3 GCGR GPR52 GRPR LPAR1 LT4R1 MTR1B NPY1R OPRD
OPRX PE2R4 PTH1R T2R14 TA2R` — are 15 Class A, 2 B1, 2 B2, 1 F-adjacent and 1 taste receptor.
**Ten of the fifteen Class A additions are already on our current panel**, so on those the
strict rule agrees with us and disagrees with them.

> **A trap fired inside this comparison and is worth recording.** The strict list names GCGR
> as `GLR`, because GPCRdb's entry is `glr_human`. A first draft of this section reported
> class B1 losing "CRHR1 and GCGR" when it loses only CRHR1. **This is the third independent
> instance of the `GLR`/`GCGR` trap in this project**, after `PANEL_EXPANSION.md` §4 and the
> brief's own warning. Any comparison of two receptor lists must join on the GPCRdb protein
> identifier, never on a display slug.

## 14.5 Strict as a filter on the 64, not a rival to it

| | **Rule P** (§4) | **strict ConfoRNets** (§14) |
|---|---|---|
| membership criteria | Active + Inactive for one UniProt entry; Class A | Degree = 100 + Inactive exists; ≤1 mutation each; all classes |
| state criterion | coarse `Active` label | **`Degree active = 100`** |
| mutation cap | none — recorded as a covariate | **≤1 per structure** |
| species | human preferred, never cross-species | **none stated, so none applied** |
| Class A receptors | **64** | **61** |
| paralog clusters (Class A) | **32** | **32** |
| all-class total | 64 A + 5 B1 + 5 scope = 74 | 71 across A/B1/B2/F/T2 |
| ConfoRNets' 51 covered | 50 (all but ACM3) | 49 (all but ACM3, ADRB1) |
| Class A receptors it uniquely has | ACM1, ADRB1, S1PR1 | none |
| non-human | 3 | **4** (adds NTR1 rat) |
| defensible sentence | *"a complete census of Class A receptors with both states"* | *"the published ConfoRNets criteria, applied to the 2026 database"* |

**The two panels differ by three receptors and by zero clusters.** Every strict Class A
receptor is inside Rule P's C1; strict adds nothing Rule P lacks and drops exactly three,
each for a different reason, all recorded in `strict_fail_reason`:

| receptor | why it fails the strict rule |
|---|---|
| **ACM1** | its **only** degree-100 active, `6OIJ`, carries **3** mutations. Every ACM1 inactive is at degree 3 and would fail criterion (i) if the roles were reversed. |
| **ADRB1** | **human** ADRB1's three active structures are all at degree **99**, not 100 — it fails by one percentage point. **Turkey** ADRB1 has six degree-100 actives at zero mutations, but its *best* inactive carries **8**. So no ADRB1 pair qualifies in either species, which is why ConfoRNets used `4BVN` (11 mutations) in violation of its own cap. |
| **S1PR1** | fifteen degree-100 actives at zero mutations, and **both** inactive structures (`3V2Y`, `3V2W`) carry **2**. Fails on the inactive side only. |

Two of the three fail on a **single structure's** annotation, which is the argument against
making the cap a membership criterion: ACM1 and S1PR1 would both re-enter the moment one
cleaner structure is deposited, and a panel whose membership moves with the deposition
calendar is not a frame.

The second row of that table is the one that matters scientifically: strict replaces the
coarse `Active` label with **activation degree = 100**, which is a *stronger* and more
defensible state criterion, and it is available to Rule P at no cost. **That part of the
strict rule I would adopt regardless of the decision below** — it is in
`panel_gpcrdb_degree.csv` and costs nothing.

## 14.6 Contingency: what a later switch to strict would do to the run plan

**The primary run plan is built on the relaxed 64 and does not change.** This section exists
so that if the PI later picks strict, the cost is already known and nobody has to re-derive
it. Computed against `RUN_MATRIX.md` §3.1 and §7.1, which I have read and not edited.

| run-matrix panel | under Rule P C1 | under strict | delta |
|---|---:|---:|---|
| **C1** (wide replication, item G2) | 64 | 61 | **−3 receptors** |
| **CORE-32** (partner-rung axis, every control arm) | 32 clusters | **32 clusters** | **no change in size** |
| **CORE-L17** (ligand + MSA-depth axes) | 17 clusters | **17 clusters** | **no change** |
| **H-B** (memorization holdout, G8) | 12 rec / 8 clusters | **12 / 8** | **no change** |
| **E-pro** (prospective, G14) | 8 | 8 | no change — not both-state by construction, untouched |
| **E-B1** (class B transfer, G15) | 5 | **4** | **−1**: CRHR1 drops (its inactive `8GTI` carries 11 mutations) |
| E-scope (F/B2, no claim) | 5 | 4 | FZD4 fails the cap, FZD6 has no inactive |

**Every prediction total in §7.1 is unchanged except two.** G2 drops from 3,840 to 3,480
(it runs on the 32 C1 members outside CORE-32, which becomes 29). G15 drops from 4,000 to
3,200. **Nothing else moves: no item that uses CORE-32, CORE-L17 or H-B changes by a single
prediction, and no MDE in §4 changes, because the cluster counts that drive them — 32, 17
and 8 — are identical under both rules.** Total campaign delta: **−1,160 predictions**, about
0.4% of the G1b-anchored plan.

**What does change is membership, in five of the 32 CORE-32 cells.** §3.1 picks the cluster
representative whose *worse-resolution* reference is best; the strict references differ, so:

| cluster | C1 representative | strict representative |
|---|---|---|
| `001_001_003` adrenoceptors | ADRB1 | **ADA2A** |
| `001_004_005` cannabinoid | CNR2 | **CNR1** |
| `001_002_020` NPY | NPY1R | **NPY2R** |
| `001_002_022` opioid | OPRD | **OPRM** (mouse) |
| `001_004_004` S1P | S1PR1 | **S1PR5** |

Three of the five substitutions are forced (ADRB1, S1PR1 fail the cap; CNR2/NPY1R/OPRD are
displaced by better strict references). **The opioid substitution is the one to look at:
OPRM is *Mus musculus*, so adopting strict puts a mouse receptor into CORE-32 where the
current representative is human.** Note also that CORE-L17's ligand tier loses ACM1, but the
muscarinic cluster is still represented by ACM2/ACM4, which is why 17 holds.

**Two items in §7.1 would need their receptor lists reissued, not their budgets:** G2 (+29
instead of +32) and G15 (4 instead of 5 receptors). **Nothing in §3.2, §3.3, §4 or §5 is
affected.** That is the whole delta, and the honest summary is that **the strict rule costs
the run plan almost nothing** — which is itself the most useful finding in this appendix,
because it means the choice in §14.7 can be made on scientific grounds alone.

## 14.7 The decision, framed — deferred to the PI

| | **Rule P (census)** | **Strict ConfoRNets** |
|---|---|---|
| receptors | 64 Class A | 61 Class A |
| clusters | 32 | 32 |
| run-plan cost | baseline | **−1,160 predictions (0.4%)** |
| comparability | 50 of their 51 covered; reference pairs differ on 20% of slots | their criteria, but **35/51 membership at the count-matching date** — *not* receptor-for-receptor comparability |
| the sentence it buys | *"every Class A receptor in GPCRdb with both states, without exception"* | *"the selection criteria of `lee2026confornets`, applied to the 2026 database"* |
| the objection it invites | *"you chose a database annotation"* | *"you selected on construct quality, which is a covariate of the thing you measure"* — and *"this is not their panel"* |
| non-human receptors | 3 | 4 |

**The thing the strict rule does not buy is the thing it was wanted for.** Receptor-for-
receptor comparability with the published benchmark comes from *containing their 51*, and
**Rule P contains 50 of 51 while strict contains 49**. Strict is not closer to their panel;
it is their rule run on a database that has since added twenty receptors, and at the date
where it matches their count it shares only 35 of 51 receptors with them. A referee who
checks will find that, and the sentence *"we applied the ConfoRNets criteria"* will then have
to be defended against their own table.

### Does the relaxed 64 cost us comparability? No — and here is the arithmetic

The coordinator's reading is that the 64 does not lose direct comparability, because
ConfoRNets' 46 Class A cases are a subset of it and the overlap can always be reported
separately. **That reading is correct, and it is stronger than "does not lose": the 64 is the
*more* comparable of the two panels.**

- **Containment.** The 64 contains **45 of their 46 Class A test cases** (all but ACM3) and
  50 of their 51 overall. The strict 61 contains **44 of 46** — it additionally drops ADRB1.
  On the currency that matters, the relaxed panel is ahead by one receptor, not behind.
- **The subset is addressable.** `confornets_member` is TRUE on **45 of the 64**, so
  *"restricted to the 45 receptors we share with `lee2026confornets`"* is a one-line filter
  and can be reported beside every headline. That is the receptor-for-receptor comparison,
  and it exists under either panel.
- **What is *not* obtainable under either panel** is agreement on the reference structures.
  Rule R picks a different entry from theirs on 20% of slots and the strict rule on 32%;
  `7EVW` is obsolete; `4BVN` is turkey and carries 11 mutations. **Comparability of numbers
  across the two papers is bounded by reference choice, not by panel membership** — so if we
  want a like-for-like number we must re-score against *their* pairs, which
  `panel_systems.csv` carries in `cn_active` / `cn_inactive` for exactly this purpose. That is
  a re-scoring job, `cheap`, and it is orthogonal to the panel decision. {ref-alt}


So the honest sentence is: *the relaxed 64 gives up nothing in comparability; what limits
comparability is that neither panel's reference pairs match theirs, and that is fixable by
re-scoring rather than by re-selecting receptors.*

**My recommendation, in three parts:**

1. **Adopt the activation-degree criterion now, regardless.** Replacing the coarse `Active`
   label with `Degree active = 100` is strictly better, is free, and removes the weakest part
   of Rule P. It changes membership by zero receptors (all 64 C1 receptors have a
   degree-100 active structure available) and strengthens the rule's wording.
2. **Keep Rule P for membership — no mutation cap.** Capping selects on construct quality,
   which is a covariate of conformational behaviour; §9 already shows inactive references are
   40/64 fusions and active references 52/64 fiducial-stabilised, so construct quality is not
   balanced across the two roles and capping it prunes asymmetrically. Record the count
   instead; it is now in `panel_gpcrdb_constructs.csv` for every structure.
3. **Report strict as a pre-registered sensitivity filter, not a panel.** It is
   `passes_strict == 'TRUE'` on 61 of the 64, the same 32 clusters, and it costs nothing
   because the campaign already ran on those receptors. Re-reporting the headline on the
   filtered subset answers *"would your result survive ConfoRNets' own selection criteria?"*
   with a number rather than an argument, and it needs no new predictions at all. This is
   strictly better than picking strict up front, because a subset can always be taken out of
   a census and a census can never be recovered from a subset.

**If the PI later wants strict as the primary panel**, §14.6 is the whole cost: reissue G2's
list as 29 receptors and G15's as 4, swap the five CORE-32 representatives, and accept a mouse
receptor in the opioid cell. No budget, power or MDE number in `RUN_MATRIX.md` changes.
**Either answer is defensible; what is not defensible is describing the strict subset as
ConfoRNets' panel.**

## 14.8 New companions

```
redo/inputs/panel_gpcrdb_degree.csv      1,716 rows — activation degree, state, % of seq
redo/inputs/panel_gpcrdb_constructs.csv  1,716 rows — mutations, deletions, modifications, insertions
redo/inputs/panel_strict_confornets.csv     71 rows — the strict rule's own output, evidence for §14.4
redo/build/panel_strict_confornets.py            — the rule, executable
redo/build/panel_strict_columns.py               — writes the filter columns onto panel_systems.csv
```

`panel_strict_confornets.csv` is **evidence, not a panel**. The decision object is the
`passes_strict` column on the 64.
