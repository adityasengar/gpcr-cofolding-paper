# GROUP1_SYSTEMS.md — the partner-length ladder, as a buildable system list

Written 2026-09-11 by the Group 1 systems session. Companion to
`redo/spec/CATALOGUE.md` §3 (the experiments, E1.1–E1.9),
`redo/spec/SEQUENCES.md` (the constructs), `redo/spec/PANEL.md` (the
receptors) and `redo/spec/RUN_MATRIX.md` (the cost). **This file owns the
dispatchable list only** — which (receptor × partner × condition) cells are
submitted. It does not re-derive the design, it does not set the budget, and it
does not assign a cognate Gα.

**Why Group 1 is the centrepiece.** The paper's title says a 21-residue Gα α5
C-terminal peptide drives GPCRs active. No arm in any of the four campaigns ever
supplied a peptide — every partner arm was a complete Gα subunit or a nanobody.
The ladder supplies progressively less of the G protein and finds where the
active state stops appearing, which converts *"a partner helps"* into *"how much
partner do you need"*.

## Machine-readable companions, all regenerable

| file | what | rows |
|---|---|---:|
| `g1_systems.py` → `g1_systems.csv` | **every dispatchable system**, one row per cell | 2,039 |
| `g1_receptors.py` → `g1_receptors.tsv` | the receptor axis + a **provisional** CORE-32 | 64 |
| `g1_midrungs.py` → `g1_midrungs.tsv` | the intermediate rungs, CGN-defined, 16 families | 80 |
| `g1_minig.py` → `g1_minig.tsv` | what a deposited mini-G actually is, block by block | 3 |
| `g1_refchimera.py` → `g1_refchimera.tsv` | **active references whose α5 tip is not canonical** | 13 |
| `g1_cognate.py` → `g1_cognate.tsv` | **verifies the cognate map and resolves receptor × rung → sha256**, evidence class per row | 448 |
| `g1_panel_freeze.py` → `g1_panel_freeze.tsv` | **the frozen panel and the two cognate columns** — Decisions 1, 2, 3 | 64 |
| `g1_partner_registry.py` → `g1_partner_registry.tsv` | **every chain-B construct, keyed by sha256** | 771 |
| `g1_recording_spec.tsv` | what must be on every row for the ladder to mean anything | 47 cols |
| `g1_preflight.py` | the dispatch gate; `--selftest` plants a defect per check | **16 checks** |

Run order: `g1_midrungs.py` → `g1_minig.py` → `g1_receptors.py` →
`g1_refchimera.py` → `g1_cognate.py` → **`g1_panel_freeze.py`** →
`g1_partner_registry.py` → `g1_systems.py` → `g1_preflight.py`.

**Current gate state: 16 blocking checks pass, 0 fail, 7 dependencies
outstanding (exit 2).** All sixteen were
proved by planting a defect — `g1_preflight.py --selftest` corrupts one artefact
per check in a scratch copy and asserts that check, and only that check, fires.
A checker that has never failed is not known to work.

---

# 0. The four rules this list is built under

These were established elsewhere and are designed around here, not relitigated.

**0.1 The ladder had a 336-residue hole and it straddled a published accuracy
boundary.** Rung lengths were 0, 11, 15, 21, 26, 36 and then 350–394.
`junker2026peptidedesign` stratifies GPCR peptide/protein complexes at **≤50 vs
>50 residues** and reports that above 50, *"35.5% of Boltz-2-predicted
GPCR-protein ligand complexes achieve DockQ below 0.23"* (p5), and that
cross-length comparison of an interface score is unsound (p16). The comparison
carrying the title — short peptide vs full subunit — is exactly the one that
crosses it. §2 fills the hole with five concrete constructs.

**0.2 Every peptide rung runs MSA-free on the partner chain, and so does
`R7_full`.** `SEQUENCES.md` §6 measured why from this project's own cache: MSA
depth at peptide length tracks **conservation, not length** — `endothelin1`
(21 aa) has depth **732**, `random_helix_40mer` (40 aa) has depth **1**. The
α5-CT is byte-identical across Gi1/Gi2, Gt1/Gt2/Ggust and Gq/G11, so it has a
deep alignment, and a wild-type-vs-scramble contrast at 21 residues run MSA-on
would be a **pure depth contrast**. **This list extends the rule to every rung in
between** (§3.1): a ladder whose short rungs are MSA-free and whose long rungs
are not has rung length and alignment depth perfectly confounded along its whole
length, which is the confound the rule exists to remove.

**0.3 Partner-chain helicity is recorded per row.** `tran2026nanogs`: an
unstapled linear α5 peptide is a random coil and does nothing (p.5, p.8); the
stapled 15-mer works only with agonist present. A co-folding model has no
solution-phase equilibrium and will fold whatever it is handed. Without
partner-chain helicity and partner-chain pLDDT **per row** — Block B put
`partner_tail11_helicity_frac` in a 640-row cell-level file — the ladder measures
**reach** rather than **recognition**. `g1_recording_spec.tsv` carries
`SEQUENCES.md` §9's spec forward and §6 below makes it per-system explicit. **And
it is more than a control**: helicity is the literature's stated mechanism for
the length effect, twice, twenty-five years apart — see §7.2, which registers it
as the hypothesis the ladder tests.

**0.4 The per-position scan runs where the partner MSA is empty.**
`masters2025physics` states the mechanism of its own null (p.9): a mutated
sequence *"will return exactly the same results as before"* from alignment and
template search. A null inside a supplied partner with an unchanged alignment is
a **retrieval artefact, not a model property**. Under 0.2's rule the scan is
compliant by construction — the partner chain has no alignment at all — and
`waymentsteele2024cluster`, which ran its scan with no MSA for exactly this
reason, is the protocol cited. The per-arm partner-MSA audit still ships
(`data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md` is the template), because a
null is only reportable if the audit shows the perturbation reached the model.

---

# 1. The dependency contract — mostly discharged

Three siblings were written concurrently with this one. **Two have landed and are
consumed; one artefact is still owed.**

| owed by | what | state |
|---|---|---|
| `COUPLING.md` | **cognate Gα per receptor** | **LANDED and consumed.** Aditya's decision: read the subtype off the structure the receptor was solved with. `g1_cognate.py` verifies the map against our own sources and resolves receptor × rung → sha256 |
| `SEQ_RECEPTORS.md` | **chain-A bytes and their hash** | landed 14:08; `chain_a_source = PENDING:SEQ_RECEPTORS.md` on every row, not yet joined here |
| `PANEL.md` | **the frozen CORE-32 slug list** | still owed. `receptor_set = CORE32(provisional)`, from `RUN_MATRIX.md` §3.1's written rule applied to `PANEL.md` §6.1 |
| `RUN_MATRIX.md` | **n, backbone count, tier** | carried, copied from §7.1, never re-derived |

## 1.1 The cognate map was verified before any of it was used

A sibling's table is a claim sheet like any other. `g1_cognate.py` runs five
checks and all five pass: the slug set matches `g1_receptors.tsv`; every
`seq_rungs_family` value is a real family; **every one of the 378 rung rows'
`sha256`, `sequence` and `len` reproduces `seq_rungs.tsv` byte for byte**; every
`rule_r_active_pdb` matches the reference PANEL.md §6.1 selects; every CORE-32
flag agrees with ours.

**An independent corroboration worth recording.** The map's ten `needs_decision`
receptors are exactly the nine mini-Gs/q chimeras plus DRD4 that §8.11 found from
a different file by a different route — and the two receptors §8.11 flagged that
the map *resolves*, B1B1U5 and OPSD, are precisely the two whose deposited tip has
an unambiguous nearest family. Two analyses, two sources, one answer.

## 1.2 What the map resolves, and what it deliberately does not

| verdict | n | meaning |
|---|---:|---|
| `frozen` | 47 | read off the Rule-R active reference |
| `frozen_by_convention` | 6 | **no Gα in the Rule-R reference at all** — a declared fallback |
| `frozen_with_caveat` | 1 | OPSD |
| `needs_decision` | 10 | cross-family chimera — **not hashable, and the rule stops on purpose** |

Subtypes in use: **Gi1 ×32, Gs ×12, Go ×5, Gq ×3, Gi3 ×1, Gt1 ×1** — six labels,
all already in the rung table. **54 of 64 receptors are hashable; of the
provisional CORE-32, 28 resolve and 4 do not.**

**The evidence class travels per row** (`cognate_evidence_class` in
`g1_systems.csv`, enforced by preflight **B14**), so a structure read and a
convention fallback can never be confused downstream:

| class | rows | |
|---|---:|---|
| `STRUCTURE_EXACT` | 1,010 | the deposited tip is a canonical subtype exactly |
| `STRUCTURE_NEAR` | 168 | engineered tip, but one family at the best score |
| `CONVENTION_FALLBACK` | 164 | **no Gα in the reference**; family from annotation, subtype is the declared representative |
| `CHIMERA_SPLIT` | 172 | the rule stops; three options, §1.4 |
| `PEPTIDE_ENTITY` | 40 | OPSD |

**The map's rung table covers seven rungs; the ladder needs more than seven.**
`coupling_cognate_rungs.tsv` carries R1–R5, R6a and R7. The intermediate rungs,
the α5-null variants, the composition controls and the heterotrimer are all
cognate-parameterised too. So the join here is done **once per receptor** — the
subtype — and every construct then resolves in our own registry by
`(construct, variant, k, family)`. For the seven rungs the two routes give the
same bytes, which is what verification (iii) proves; for the rest ours is the only
route. **That took the unresolved column from 1,086 rows to 204**, and the 204 are
exactly the chimeras.

## 1.3 Three rows that must carry a visible caveat, not a silent value

- **OPSD → Gt1, not Gi1.** `PEPTIDE_ENTITY`, from 4X1H's 11-residue peptide.
  The margin is decisive despite 0.64 identity — 4 substitutions to Gt/Ggust
  against 7 to the nearest other family. **The Gi1 family fallback would have
  differed from Gt1 at exactly the residue E1.6/G12 measures**, so the
  structure-read rule earned its keep on the one receptor where it mattered most.
  Carried caveat: **everything past rung `R1_ct11` is extrapolation**, because
  OPSD has no α5 reference beyond the 11-mer at all.
- **Six convention fallbacks** — AA2AR, ADRB1, AGTR1, NTR1, OPRD, OPRM — where
  the Rule-R active reference contains **no Gα entity**. Two need the caveat
  said out loud: **OPRM has no active reference containing a Gα at all**, and
  **NTR1's fallback rests on a non-Rule-R structure against a unanimous Gq/11
  annotation**. Preflight reports all six by name every run.
- **Four assignments reverse Block B's prior** — B1B1U5, CCKAR, EDNRB, GHSR.
  B1B1U5 is live: it follows Rule R to **9EPP**, and **if the panel session
  settles on 9EPR it flips to Gi1 and the map must be rebuilt**. That row is
  therefore never hard-coded here; it is read from the map on every run.

## 1.4 DECISION 1 — the ten chimeras are ineligible for the primary panel

**Aditya's decision, with the governing principle: Group 1 must be STRICT —
stricter than Group 0, because Group 0 is us tuning a measure and Group 1 is what
actually gets dispatched.**

Rungs R1–R4 *are* the α5 C terminus. On these ten the deposited active reference
carries an engineered tip **8 of 21 residues from canonical Gq at the title's
rung**. Supplying a wild-type peptide and scoring it against an engineered
reference is not a measurement of what we claim to measure, so **a strict primary
panel cannot contain a systematic construct mismatch at exactly the residues
under study.** All ten move to the extension tier — fully specified, fully
dispatchable, never pooled with the primary panel — and **G19, the deposited-tip
arm, stays additive as the matched control**, which is what makes the exclusion
honest rather than convenient.

**Implemented as an eligibility filter on the pool, not as a deletion of the
chosen representative — and that recovers one cluster.** `RUN_MATRIX.md` §3.1
says *"from each cluster take exactly one member: the one whose worse-resolution
reference has the lowest resolution"*. Filter the pool first and the same rule
re-selects inside any cluster that still has a clean member. It does for one:

| cluster | was | now | cost |
|---|---|---|---|
| `001_001_001` serotonin | 5HT2A (2.80 Å, chimeric) | **5HT5A (3.10 Å, clean)** | 0.30 Å of reference resolution |
| `001_002_003` bombesin | GRPR | — | **cluster lost**, no other member |
| `001_002_023` orexin | OX2R | — | **cluster lost** |
| `001_002_032` oxytocin | OXYR | — | **cluster lost** |

**So the exclusion costs three clusters, not four, and the power penalty is
√(32/29) = 1.050×, not the 1.069× quoted when the cost was assumed to be four.**
`BACKFILL = False` in `g1_panel_freeze.py` reproduces the harsher reading (drop
the cluster outright, 28 clusters, 1.069×) and both numbers are printed on every
run, so the choice stays visible rather than buried. **Flagging this because the
decision was costed at four clusters and it is three.**

## 1.5 DECISION 3 — AA2AR is IN, as a declared override

It loses the adenosine cluster to AA1R by **0.14 Å** of worse-reference
resolution, and it is **the only receptor on the panel with wet-lab data on our
exact 21-mer** — `eddy2018extrinsictrp`'s W233^6.35 measurement and
`mazzoni2000`'s 11/13/15/17/19/21 length series are both A2AR. Excluding the one
receptor the ladder can be validated against, on a 0.14 Å tiebreak, is the wrong
trade.

Recorded as a **declared override with its reason**, not a rule change: the
resolution rule stands everywhere else, AA1R stays, and AA2AR **adds a receptor
rather than a cluster**. Its power contribution is therefore ≈0 — it is a
cluster-mate of AA1R and the bootstrap is over clusters. **Its value is
validation, not power, and the document should never claim otherwise.**

## 1.6 The frozen panel

**30 receptors in 29 clusters**, from `g1_panel_freeze.py`:

```
5HT5A AA1R AA2AR ACM4 ADRB1 AGTR1 APJ B1B1U5 C5AR1 CCKAR CCR2 CNR2 DRD3 EDNRB
GHSR GPR52 HRH3 LPAR1 LT4R1 MCHR1 MTR1A NK1R NPY1R NTR1 OPRD OPSD PD2R2 S1PR1
SSR2 TSHR
```

| tier | receptors | system rows | predictions (pooled / per-cell) |
|---|---:|---:|---:|
| **PRIMARY** | **30** | 1,917 | **70,080 / 204,840** |
| EXTENSION — chimeric reference | 10 | 50 | 1,200 / 1,200 |
| EXTENSION — census (G2 replication) | 24 | 72 | 2,880 / 2,880 |
| — | | **2,039** | **74,960 / 212,920** |

Derived sets move with it: **`CORE32_GS` is now 6** (AA2AR is Gs-coupled, so
Decision 3 adds a Gs receptor and E1.8's arms grow), and **`G10_SCAN` is
unchanged** at ACM4, APJ, C5AR1, CCR2, CNR2, DRD3, EDNRB, HRH3, PD2R2, S1PR1 —
none of the ten was chimeric, so the freeze did not disturb the scan.

Preflight **B9** now enforces the frozen panel rather than the provisional one:
one per cluster, declared overrides the only exception, **and no
chimeric-reference receptor anywhere in it**.

## 1.7 DECISION 2 — the cognate assignment is two columns, never one

`supplied_partner_family` / `supplied_partner_subtype` is **the biology — what we
hand the model**. `reference_tip_subtype` / `reference_tip_family` is **the
structure — what we score against**. We had been conflating them. Both are on
every system row, the biology wins for the supplied partner where they disagree,
and preflight **B16** fails the run if any row carries one without the other.

**Three things I could not reproduce, reported rather than asserted.**

1. **`paper_af3`'s coupling table is not on this machine**, so the 31-of-35 diff
   cannot be re-derived here. What follows is from the files we hold.
2. **At family level I find zero disagreements, not four.** On all 54 resolvable
   receptors the structure-read family is **inside** the receptor's annotated
   family set. Checked two ways: against `coupling_assignments.csv`'s
   `recommended_family` (0 disagreements) and against the multi-valued
   `annotation_family` set (0 outside the set; 20 apparent mismatches were all
   *containment* — the annotation lists several families and the structure picked
   one of them).
3. **The four named receptors — B1B1U5, CCKAR, EDNRB, GHSR — are the four that
   reverse *Block B's prior*, which is a third question again.** They are tagged
   `reverses_blockb_prior` in our own map and were flagged as such before this
   decision arrived. It is likely the same four fall out of `paper_af3`'s table
   for the same reason, but I cannot verify that from here.

**The two-column split is still right, and it bought something — just not what
was expected.** It exposed that **the biology column is not independent of the
structure column on 13 of 64 receptors**, where `recommended_basis` reads *"taken
from the deposited active reference"*. On **three of those thirteen — 5HT2C,
EDNRA, TA2R — the deposited reference is the chimera**, so the coupling
recommendation inherits exactly the circularity the coordinator described for
`jsGiq`: *its tip reads Gq because someone made it read Gq*. **All three are in
the excluded tier**, so none of the circularity reaches the primary panel — but it
was invisible until the columns were separated, and it is recorded per row as
`supplied_partner_independence`.

**What would change my answer.** If `paper_af3`'s table is put on this machine I
re-run the diff in one command and either confirm the four or report where ours
differs. Until then the biology column is `recommended_family` with its basis
recorded, and the disagreement count from *our* sources is zero.

## 1.8 GoA / GoB

`seq_rungs.tsv`'s bare **`Go` is P09471 canonical = isoform Alpha-1 = GoA** —
checked by hash here, not assumed (`399d5823731a6349` both ways). All five Go
picks are GoA. **The bare label is ambiguous and should be read as `GoA`
everywhere**; no sequence changes.

GoB (P09471-2, `0d1b77601732694e`) is registered so a within-subtype minimal pair
can be costed, with two corrections to how it was relayed and one constraint that
decides it:

| pair | ct11 | ct15 | ct21 | a5helix | a5plus |
|---|---:|---:|---:|---:|---:|
| **GoA vs GoB** | **1** | 2 | **3** | 3 | 5 |
| **Gi1 vs Gt1** (E1.6/G12) | **1** | 2 | **2** | 4 | 6 |

**At `ct11` they tie at one substitution; at `ct21` Gi/Gt is the tighter pair, not
GoB** (3, not the 4 relayed). GoB's real advantage is not distance but
cleanliness: both isoforms are **human** and differ only by alternative splicing,
whereas the Gi/Gt pair needs OPSD — a bovine receptor and the panel's only Gt.
**But the constraint that decides it: zero Go receptors are in CORE-32.** All five
(5HT1B, ACM2, ADA2A, CCR6, DRD2) are C1-only, so a GoA/GoB arm cannot run on the
headline panel at all — it would have to run on G2's set. Costed nowhere; the
constructs exist if it is wanted.

# 2. The intermediate rungs — five constructs, with residue ranges and hashes

`RUN_MATRIX.md` §3.5 asks for three rungs at ≈60/≈100/≈200 residues "expressed as
C-terminal truncations of the cognate subunit" and says *"SEQUENCES.md owns the
exact boundaries"*. `SEQUENCES.md` is frozen, so they are built here, under its
conventions exactly.

## 2.1 The construction rule, and why it is a segment and not a number

A rung is defined by a **CGN protein segment**, the way `R4_a5helix` is "G.H5"
and `R5_a5plus` is "G.S6 → C-term" — never by a raw length. A rung defined by a
raw length supplies a *different structural element* in each family; a rung
defined by a segment supplies the same element and lets the length vary, which is
the honest parameterisation. Boundaries come from GPCRdb/GproteinDb CGN residue
tables (`https://gpcrdb.org/services/residues/{entry_name}/`, fetched 2026-09-11,
cached in `g1_cgn_cache.json`); bytes come from `seq_rungs.tsv`'s held canonical
UniProt sequences.

**One boundary is defined twice in the literature and the two agree.** CGN
`G.H5` gives Gs 369–394, 26 residues, and reproduces at 26 on all 16 human Gα.
The Gsα crystal structure (Sunahara *et al.*, *Science* 1997, reported via the
`dursi2011signalpeptides` relay and therefore not citable until retrieved) gives
the α5 helix as **Asp368–Leu394, 27 residues**. Checked here: P63092 position 368
**is** D and 394 **is** L, so the two definitions differ by exactly one residue at
the helix N terminus — a convention difference about where a helix is declared to
begin, not a disagreement about the helix. **`R4_a5helix` stays at CGN `G.H5`**,
because that definition is family-general and verified uniform at 26 across all
sixteen subunits, whereas the 27-residue window is a Gs crystal-structure
observation. The 27-mer is registered anyway (`R4b_a5helix27`, sha
`f0936d17fc8bb8f0`) so the convention is auditable rather than asserted.

`g1_midrungs.py` runs three checks on itself and all three were proved by
planting a defect: (i) every CGN residue identity must equal the UniProt byte at
that position; (ii) the re-derived G.H5 and G.S6 truncation lengths must
reproduce `SEQUENCES.md` §0.2's invariants (26 and 36) on all 16 families; (iii)
every emitted construct must be a suffix of its parent, except the declared
non-nested one.

## 2.2 The five constructs

| rung | rule | Gi1 | Gq | Gt1 | G13 | Gs | nested? |
|---|---|---:|---:|---:|---:|---:|---|
| `M1_h4s6` | CGN **G.h4s6** → C-term | 310–354 (45) | 316–359 (44) | 306–350 (45) | 333–377 (45) | 348–394 (47) | yes |
| `M2_h4` | CGN **G.H4** → C-term | 294–354 (61) | 299–359 (61) | 290–350 (61) | 316–377 (62) | 332–394 (63) | yes |
| `M3_h3` | CGN **G.H3** → C-term | 242–354 (113) | 247–359 (113) | 238–350 (113) | 264–377 (114) | 265–394 (130) | yes |
| `M4_he` | CGN **H.HE** → C-term | 151–354 (204) | 156–359 (204) | 147–350 (204) | 173–377 (205) | 174–394 (221) | yes |
| `M5_dHD` | full subunit, CGN **H.HA…H.HF deleted** | 1–62+177–354 (240) | 1–68+182–359 (246) | 1–58+173–350 (236) | 1–77+199–377 (256) | 1–84+200–394 (279) | **no** |

Gi1 sha256[:16] — `M1` `8f352b0ebaa84e68`, `M2` `e93035d875ce8b96`, `M3`
`ebed470d248ced39`, `M4` `9bfc3b4d59a9400d`, `M5` `a2afee46d2476b8d`. All 80
constructs (16 families × 5) with full hashes in `g1_midrungs.tsv`.

**How they sample the boundary.** `R5_a5plus` is 36, below 50. `M1` is 44–47,
still below. `M2` is 60–63, just above. `M3` 112–130 and `M4` 203–221 sit inside
the gap. So the ≤50/>50 transition is bracketed by two rungs 15 residues apart
instead of by a 314-residue leap.

**A property of the intermediates nobody has recorded.** The family-to-family
length spread, over the five panel families:

| rung | spread | family contrasts readable here? |
|---|---:|---|
| `R1`–`R3` (11/15/21) | **0** | yes — every family is exactly equal length |
| `M1_h4s6` | 3 | yes, marginally |
| `M2_h4` | 3 | yes, marginally |
| `M3_h3` | 17 | no |
| `M4_he` | 17 | no |
| `M5_dHD` | 43 | no |
| `R7_full` | 44 | no |

This extends `RUN_MATRIX.md`'s anomaly 8 (Gs supplies 44 more residues than Gt at
`R7_full`, so the family term there is partly a length term) down the whole
ladder: **read every family contrast at `R3_ct21`, where the spread is exactly
zero, and never above `M2`.** G9 and G12 are anchored accordingly.

## 2.3 Grounding the mid-gap rung in a deposited construct, and one measured fact

The lit session swept the corpus for a standard partner truncation between 50 and
350 residues. **Nothing exists**, and the absence is recorded three times
independently: `ye2026multistatebias` (the words "mini-G", "α5" and "alpha5" do
not occur in the paper at all), `miglionico2026atlas` (full heterotrimer only,
pp19–20, stated so it is checkable) and `pandyszekeres2024gproteindb` (mini-G and
nanobodies *"appear only as annotation"*). Its recommendation: take the mid-gap
rung from a deposited complex rather than from arithmetic.

So `g1_minig.py` fetched the three deposited mini-G entities and aligned each to
its canonical parent. **The result changes what the rung can be:**

| entry | entity | len | canonical blocks present | non-matching residues | pure C-terminal truncation? |
|---|---|---:|---|---:|---|
| **6FUF** mini-Go | P09471 | 214 | 19–41; 44–63; 177–226; 242–249; 251–331; 336–354 | 13 | **no** |
| **5G53** mini-Gs | P63092 | 229 | 26–48; 51–62; 204–248; 264–271; 273–371; 376–394 | 23 | **no** |
| **8F76** miniGs399 | P63092 | 261 | 5–48; 51–64; 204–248; 264–371; 376–394 | 31 | **no** |

**A mini-G is a helical-domain deletion plus engineered substitutions and linker
replacements — not a truncation.** It therefore cannot be a rung on a nested
length ladder, and a design that called it one would be comparing a truncation
series against a mutant. What it *can* do is anchor the length:

- The deposited window is **214–261 residues**. `M4_he` is **203–221** and
  `M5_dHD` is **236–279**. Both sit inside or adjacent to it, so the mid-gap rung
  is now justified by three crystallised constructs rather than by "about 200".
- **`M4_he` and `M5_dHD` are length-paired and topologically complementary.**
  `M4` keeps the C-terminal half of the helical domain and drops the N-terminal
  half; `M5` deletes the whole helical domain and keeps the N terminus — which is
  the mini-G topology. **If they behave the same, length dominates; if they
  differ, composition does.** That is a direct test of `junker`'s
  placement-regime worry and it costs one extra arm.
- **G1f** runs the three literal deposited entities (hashed: `567265d3167c96c9`,
  `22857a87c6e6bb3f`, `562bc4a0c78a7b34`) as an off-ladder anchor, on receptors
  whose cognate family matches the construct's. 6FUF is a **rhodopsin** complex
  and OPSD is in the provisional CORE-32, so that anchor has a directly matched
  reference.

**The naming trap, and why it vindicates the "last N residues" rule.**
`georgiou2025heterogeneity` uses "mini-Gs" for both the ~229-residue engineered
construct and *"a mini-Gαs consisting of a 21-residue polypeptide"* two sentences
apart. A rung named "mini-G" is ambiguous by a factor of ten. The primary source
does not do this — it says *"the polypeptide derived from the GαS carboxy
terminus"* throughout and reserves *"engineered 'mini GαS' protein"*, in scare
quotes, for the protein. **So the justification for the rule is not "the field is
ambiguous"; it is "one review is ambiguous and we will not propagate its
label".** Preflight check **B5** enforces it mechanically: no system row may
carry a construct name without a resolved numeric length.

**`georgiou2025heterogeneity` is cited here for the naming trap and for nothing
else.** Its attribution of the 21-mer NMR result is wrong — its ref 155 points at
a different Eddy paper (*Structure* 2021), which contains no occurrence of `Gs`,
`Gα`, `mini-G`, `21-residue` or `6.35`. The primary is `eddy2018extrinsictrp`
(§7.4). Do not cite the review for any 21-mer biology.

## 2.4 What each intermediate rung costs

Arithmetic only; `RUN_MATRIX.md` owns the decision. CORE-32 × 4 backbones.

| rung | pilot (Boltz-2, n=10) | pooled (4 bb, n=10) | per-cell (4 bb, n=50) |
|---|---:|---:|---:|
| `M1_h4s6` | 320 | 1,280 | 6,400 |
| `M2_h4` | 320 | 1,280 | 6,400 |
| `M4_he` | 320 | 1,280 | 6,400 |
| **the three RUN_MATRIX costed (P1b / G1c / G1d)** | **960** | **3,840** | **19,200** |
| `M3_h3` *(optional 4th, fills 61→204)* | 320 | 1,280 | 6,400 |
| `M5_dHD` *(off-ladder companion)* | 320 | 1,280 | 6,400 |
| `MG_6fuf` + `MG_5g53` + `MG_8f76` *(anchor, family-matched subset)* | ≤960 | — | — |

`M1`, `M2` and `M4` reproduce `RUN_MATRIX.md` §3.5's P1b/G1c/G1d exactly (960 /
3,840 / 19,200). The two additions cost 2,560 pooled between them.

---

# 3. Conditions

## 3.1 MSA

| chain | condition | where |
|---|---|---|
| receptor (chain A) | **on, default depth**, everywhere | all 2,039 rows (96 of which are `R0_apo` and have no chain B at all). Varying it is Group 8 — a different factor, a different literature, a different open question |
| partner (chain B) | **off — MSA-free, single sequence — as the primary condition on every rung** | 1,855 rows |
| partner (chain B) | **on**, at `R3_ct21`, `R5_a5plus`, `R7_full` only | 96 rows, item G17 (E1.9) |

`SEQUENCES.md` §6.1 requires MSA-free on the peptide rungs and on `R7_full`.
**This list extends it to `R4`, `R5`, `R6a/b/c`, `M1`–`M5` and the deposited
anchors**, and the reason is the same one §6.1 gives: any rung left MSA-on
reintroduces the length/depth confound at that rung. The MSA-on arm is then a
clean second factor at three fixed lengths rather than a contaminant of the
first.

**This promotes E1.9 from an optional side-experiment to a load-bearing component
of E1.1** — which `SEQUENCES.md` §6.1(2) says in as many words, and which
**`RUN_MATRIX.md` §7.1 has no line item for**. See §8.

Before anything dispatches, the ~60 distinct peptide-rung sequences go through
the same ColabFold pipeline with `n_seqs` recorded (`SEQUENCES.md` §6.1(4)).
Hours of wall-clock, no inference, and it turns the paragraph above from a
prediction into a measurement.

## 3.2 Ligand

**`ligand = none` on all 2,039 Group 1 systems.** That is `RUN_MATRIX.md` §3.2's
reference level and it is what Blocks A and B ran, so the ladder joins to them.

One flag, not an arm: `tran2026nanogs` finds the stapled 15-mer works **only with
agonist present**. The ligand × partner crossing is **G6 (E2.2), Group 2, on
CORE-L17** and it should include `R2_ct15` and `R3_ct21` among its partner
levels. That is a Group 2 decision; recorded here so it is not lost.

## 3.3 n and backbones

Copied from `RUN_MATRIX.md` §7.1, never re-derived. Four backbones =
`boltz2|openfold3|protenix|chai1`; Boltz-2 is the single-backbone reference
(the only one with a datable cutoff). Pilots are Boltz-2, n=10; pooled arms are
4 backbones, n=10; per-cell arms are 4 backbones, n=50.

---

# 4. The system table

Full enumeration in `g1_systems.csv` — **2,039 rows, 82 distinct chain-B
construct keys, every one enumerated per receptor.** Nothing is templated any
more: the cognate map resolved the four receptor sets that were pending, so
`G10_SCAN`, `CORE32_GS` and the Gs-only arms now carry real slugs and real costs.
**1,365 rows carry a resolved 64-hex sha256**; the 204 that do not are the
chimera rows of §1.4 and no others.

| item | exp | arm | receptors | rungs / cells | partner MSA | bb | n | predictions |
|---|---|---|---|---|---|---:|---:|---:|
| **P1** | E1.1 | ladder pilot | CORE-32 | R0, ct11, ct15, ct21, a5helix, a5plus, full (7) | off | 1 | 10 | **2,240** |
| **G1a/G1b** | E1.1 | the ladder | CORE-32 | the same 7 | off | 4 | 10 / 50 | **8,960 / 44,800** |
| **P1b** | E1.1 | mid-rung pilot | CORE-32 | M1, M2, M4 | off | 1 | 10 | **960** |
| **G1c/G1d** | E1.1 | intermediate rungs | CORE-32 | M1, M2, M4 | off | 4 | 10 / 50 | **3,840 / 19,200** |
| G1c-opt | E1.1 | optional 4th rung | CORE-32 | M3 | off | 4 | 10 / 50 | 1,280 / 6,400 |
| **G1e** | E1.1 | ΔHD companion | CORE-32 | M5_dHD | off | 4 | 10 / 50 | 1,280 / 6,400 |
| **G1f** | E1.1 | deposited mini-G anchor | family-matched | MG_6fuf, MG_5g53, MG_8f76 | off | 1 | 10 | ≤960 |
| **G18a (proposed)** | E1.1 | wet-lab length series | CORE-32 | **ct13, ct17, ct19** | off | 4 | 10 / 50 | **3,840 / 19,200** |
| **G18b (proposed)** | E1.1 | wet-lab-matched peptides | **CORE32_GS (5)** | ct17/ct19/ct21 @C379A | off | 1 | 10 | **150** |
| **G19 (proposed)** | E1.1 | reference-matched α5 tip | 6 affected (§8.11) | reftip_ct11, reftip_ct21 | off | 4 | 10 / 50 | **440 / 2,200** |
| G2 | E1.1 | wide replication | C1 rest (32) | R0, ct21, full | off | 4 | 10 | **3,840** |
| **G3a/G3b** | E1.2 | α5-null | CORE-32 | R6a_da5, R6b_a5perm, R6c_a5polyA | off | 4 | 10 / 50 | 3,840 / 19,200 |
| **G3a/G3b** | E1.2 | non-Gα bulk | CORE-32 | ct21@gcn4_window, ubiquitin, KaiB_2QKEE | off | 4 | 10 / 50 | 3,840 / 19,200 |
| **G4a/G4b** | E1.3 | composition controls | CORE-32 | 4 arms in 10 cells at ct21 | off | 4 | 10 / 50 | 4,992 / 25,344 |
| G9 | E1.4 | family swap | CORE-32 | ct21, non-cognate | off | 4 | 50 | **6,400** |
| **G12** | E1.6 | Gi/Gt single-residue pair | CORE-32 | **ct11**, not ct21 | off | 4 | 50 | **6,400** |
| G10 | E1.5 | per-position Ala scan | **G10_SCAN (10, §1.5)** | 21 cells at ct21 | off | 1 | 20 | **4,200** |
| G10b | E1.5 | Gi→Gs series | **G10_SCAN (10)** | **15** cells at ct21 | off | 1 | 20 | **3,000** |
| G11 | E1.7 | heterotrimer | CORE-32 | R8_hetero, 3 chains | off | 4 | 50 | **6,400** |
| **G16 (proposed)** | E1.8 | uncoupling mutants | **CORE32_GS (5)** | 2 full + 4 peptide-rung | off | 4 | 50 | **6,000** |
| **G17 (proposed)** | E1.9 | partner MSA on | CORE-32 | ct21, a5plus, full | **ON** | 4 | 10 / 50 | 3,840 / 19,200 |

Bold rows either reproduce a `RUN_MATRIX.md` §7.1 figure exactly or are new here.
Every figure that overlaps §7.1 reproduces it — G1a 8,960, G1b 44,800, G1c 3,840,
G1d 19,200, G2 3,840, G3a 7,680, G3b 38,400, G9/G11/G12 6,400, P1 2,240, P1b 960.
Two do not, on purpose, and both are explained in §8: **G4** and **G10b**.

## 4.1 The four composition controls, and why they are ten cells

`SEQUENCES.md` §5.1 draws **five** scramble permutations and **three**
face-scrambles per (family × rung), because at peptide length there is no
receptor term left and a single draw would rest the whole control on one
permutation. `RUN_MATRIX.md` costs G4 as four arms. Both are right and they
compose: **four arms, ten dispatch cells, n split across the draws.**

| arm | cells | n at G4b | what it preserves | what it destroys |
|---|---:|---|---|---|
| `reversed` | 1 | 50 | length, composition, charge, near-identical helical propensity | N→C order and register — the cleanest single control |
| `polyA` | 1 | 50 | length only | everything; **raises** helical propensity, so it is the upper bound on "any helix will do" |
| `scramble` | **5** | 10 each | length, composition, charge | order, register **and the hydrophobic face** |
| `face_scramble` | **3** | 16 each | length, composition, charge **and the hydrophobic/polar pattern** | residue identity only — the intended control |

Total predictions unchanged; the permutation becomes a random effect instead of a
fixed sequence, which is the question a referee asks. `wt` is `R3_ct21`, already
in G1a/G1b, and is not re-dispatched.

## 4.2 The three non-Gα bulk arms — the decision `RUN_MATRIX.md` §10.3 asked for

`RUN_MATRIX.md` §10.3 asks this session which three of six candidates are
dispatched, **keyed by sequence SHA not header**. The answer:

| dispatched | len | provenance, hash-verified against `SEQUENCES.md` §2 | why |
|---|---:|---|---|
| `ct21@gcn4_window` | 21 | P03069 249–269, `e6403a1af54b3e1a` | **length-matched exactly** to the title's rung; strongly helical; evolutionarily unrelated to Gα |
| `ubiquitin` | 76 | P0CG48 1–76, `233b4b0b8c461609` | a folded non-Gα domain; nearest rung `M2_h4` (60–63) |
| `KaiB_2QKEE` | 91 | RCSB 2QKE entity 1 residues 5–95, `e7e1c7e7d0960a55` | a folded non-Gα domain; nearest rung `M3_h3` (112–130) |

| **not** dispatched | why |
|---|---|
| `random_helix_40mer` | **bytes not held**, and it length-matches no rung |
| `arrestin_FL` | **mislabelled** — it is β-arrestin-1 P49407 residues 22–36, a β-strand fragment of the N-domain, not a finger loop and not full length |
| `arrestin_Ctail` | **bytes not held**; no 41-mer window of any candidate arrestin or opsin hashes to the recorded value |

All three fetches were re-verified this session and reproduce
`SEQUENCES.md` §2's recorded sha prefixes exactly — an independent confirmation
made from a separate fetch.

**Honest about the length mismatch.** `ubiquitin` and `KaiB` match no rung
exactly (Δ13–16 and Δ21–39). Per `junker2026peptidedesign` p16, **compare a
non-Gα arm only against the rung whose length it matches within a stated
tolerance, never across rungs**, and record the Δ per row. The mass-matched bulk
control at subunit scale is `R6b_a5perm`, not any of these — it is in G3's other
three cells.

---

# 5. What is already held versus what must be built

`g1_partner_registry.tsv`, 588 constructs, **keyed by sha256 and never by
header** — `partners.fasta` has three known mislabels (`Nb60` carries the Nb80
CDR3, `GASR` is the gastrin *receptor*, `arrestin_FL` is not a finger loop), so
an arm that resolves its partner by header can silently dispatch the wrong
molecule.

| class | n | status |
|---|---:|---|
| `ga_rung` | 261 | held (`seq_rungs.tsv` 112, `g1_midrungs.tsv` 80, `seq_a5null.tsv` 15) + **48 built this session** (`R1b_ct13`, `R2b_ct17`, `R2c_ct19` × 16 families) |
| `peptide_control` | 336 | held (`seq_controls.tsv` 240) + **96 built this session for Gi3**, which `seq_controls.tsv` does not cover — see §8.12 |
| `ala_scan` | 105 | **built this session** — 21 positions × 5 families |
| `gi_to_gs_scan` | 15 | **built this session** |
| `uncoupling_mutant` | 8 | **built this session**; the two full-length ones rebuilt and hash-verified against `SEQUENCES.md` §2 |
| `minig_deposited` | 3 | **fetched this session** |
| `wetlab_matched` | 3 | **built this session** — `mazzoni2000`'s three C379A peptides, §7.1 |
| `ref_tip` | 23 | **built this session** — the α5 tips actually present in the 12 engineered active references, §8.11 |
| `ga_rung_isoform` | 6 | **built this session** — GoB rungs, §1.6 |
| `boundary_variant` | 1 | **built this session** — the 27-residue Sunahara α5 window, so the G.H5 convention is auditable rather than asserted, §2.1 |
| `non_ga_chain` | 5 | fetched and hash-verified |
| `not_dispatchable` | 5 | **`random_helix_40mer`, `arrestin_Ctail`, `DAMGO`, `Nb60` — bytes not held. `arrestin_FL` held but mislabelled.** |

Preflight **B4** fails the run if any system references a construct in the last
row.

## 5.1 The helicity-matched control the literature lacks, made concrete per rung

`tran2026nanogs`'s negative controls are all **structural**; nobody in the
co-folding corpus scrambles sequence while preserving length and charge.
**The novelty claim is not settled, though, and must not be written as if it
were.** `mazzoni2000`'s own controls are unusually strong for a 2000 paper —
basal and forskolin cyclase both unaffected, ±GTPγS, antagonist radioligand
alongside agonist, a length control and a family control — and whether it also
ran a **sequence-scrambled** peptide is **UNRESOLVED from the abstract, not
absent**. Until the PDF is retrieved, `face_scramble`'s novelty is recorded as
open rather than as first. `random_helix_40mer` was to be the
helicity-matched arm and **its bytes are not held** — it is designed, not
derivable, and at 40 residues it length-matches no rung anyway. `SEQUENCES.md`
§5.2's substitute is grounded by hash and is used here:

**`gcn4_window` = P03069 residues 249..(249+N−1)**, the leucine-zipper record
whose full 33-mer already reproduces `partners.fasta:gcn4_leucine_zipper_33`
(`9569a7eb08514dbd`). Every sub-window is therefore equally grounded:

| rung | N | sequence | sha256[:16] |
|---|---:|---|---|
| `R1_ct11` | 11 | `RMKQLEDKVEE` | `41ed6b4dfbf6977e` |
| `R2_ct15` | 15 | `RMKQLEDKVEELLSK` | `2fd275ca6aa5dbe0` |
| `R3_ct21` | 21 | `RMKQLEDKVEELLSKNYHLEN` | `e6403a1af54b3e1a` |
| `R4_a5helix` | 26 | `RMKQLEDKVEELLSKNYHLENEVARL` | `3e6c15f660b87625` |
| `R5_a5plus` | 36 | — | **not available: P03069's zipper is 33 residues** |

**Measured, not assumed: `gcn4_window` and `polyA` are byte-identical across all
five families at every rung.** They have no family term, so dispatching them per
family is five times the same inference. One construct per length, not five.

The remaining limit is honest: the length-matched helical control exists at four
of the seven ladder rungs and stops at 33 residues. It is not a live gap — every
control arm is anchored at `R3_ct21` — but if a control is ever wanted at
`R5_a5plus`, the window has to be extended N-terminally outside the annotated
zipper, and that should be a decision rather than a side effect.

---

# 6. What must be on every row

`g1_recording_spec.tsv` — 47 columns, each with grain, dtype, status
(new/exists/exists-at-cell-level) and the reason it is there. It carries
`SEQUENCES.md` §9's twelve forward and adds the ones this list needs:
**`partner_helix_span_len` / `_start` / `_end` / `_uniprot_range`** (§7.2 — the
length hypothesis is about helix *length*, and a helicity fraction cannot express
it), `interface_score_dockq_like` (because `junker` reports PAE **over-estimates**
exactly where a GPCR peptide is misplaced, so a confidence metric is the one
thing that will not catch the failure mode), `ras_domain_ca_rmsd_to_R7` (the
`R6a/b/c` and `M5_dHD` integrity gate), `active_frac_deposited` +
`n_deposited_active/inactive` (E1.2's exposure stratification, which
`RUN_MATRIX.md` §10.5 makes a hard predecessor), and `chain_role_json`.

Three things that decide whether the ladder means anything:

**Reach versus recognition.** A rung that raises active fraction *and* whose
partner chain is helical *and* engages the crevice is recognition. A rung that
raises it with a low-helicity, low-pLDDT partner chain barely touching TM3/TM6 is
reach — the receptor opened and the chain went along. Both are reportable; only
the first supports the title. This measurement can only be added before the runs.

**Chain roles are hashed, not named.** `partners.fasta:endothelin1` is 21
residues — exactly `ct21`'s length. If EDNRA/EDNRB ever get an agonist arm
crossed with `R3_ct21`, two 21-mers enter the same prediction and a model given
two unlabelled 21-mers can place either in the intracellular crevice.

**Gα fold integrity is a gate, not a caveat.** α5 packs against the Ras domain,
so `R6a`–`R6c` may not fold as Gα at all. If they arrive as molten globules they
are not mass-matched to anything, the bulk control has not been run, and G3b's
38,400 predictions are wasted. G3's pilot leg runs first and the integrity
readout is checked before the full arm dispatches. The same gate applies to
`M5_dHD` and to `M4_he`, which is a fragment of a fold rather than a fold.

---

# 7. Pre-registered expectations

Written down now so they cannot be discovered afterwards. **7.1 is the reason
the ladder is a test rather than a scan.**

## 7.1 There is a wet-lab length series at our rungs — and no per-rung sign may be pre-registered

`mazzoni2000` (Mazzoni *et al.*, *Mol. Pharmacol.* **58**:226–236) tested Gαs
C-terminal peptides on **rat** A2AR in striatal membranes. From the abstract,
verbatim: *"Three peptides, **Gαs(378–394)C379A, Gαs(376–394)C379A, and
Gαs(374–394)C379A**, were the most effective. … **Shorter peptides from Gαs and
Gαi1/2 carboxyl termini were not effective.**"* Those windows are the **last 17,
19 and 21 residues** of GNAS.

**The abstract never gives a number for any ineffective peptide.** The only
length-bearing strings in it are `374-394`, `376-394`, `378-394` and `100 µM`.
So on the abstract alone, "shorter" is unquantified and 17 is an **upper bound**
on any threshold, not the threshold.

**The full panel is known, but only through a relay, and the relay contradicts
the abstract.** `dursi2011signalpeptides`, a 2011 open-access review whose
reference 77 matches `mazzoni2000` by DOI and PMID, enumerates the peptides as
**384–394, 382–394, 380–394, 378–394(C379A), 376–394(C379A), 374–394(C379A)** —
the last **11, 13, 15, 17, 19 and 21**, a two-residue ladder — and says all six
*stimulate specific binding*, with the 11-mer merely **less active**. That is a
different claim from "not effective".

> **Handling, and it is strict.** `dursi2011signalpeptides` is a **relay, not a
> source** (`lit/source/pending_text/dursi2011signalpeptides.RELAY.txt`, named
> `.RELAY.` deliberately). **Nothing in it may be cited as `mazzoni2000`.** Its
> adenylyl-cyclase percentage is in the same category — useful for knowing what
> to look for in the PDF, not citable. The peptide concentration for the cyclase
> effect remains unknown.

**One internal check was run on the relay before any of it was used here.** C379A
appears on exactly the three windows that contain position 379 (378–394, 376–394,
374–394) and on none of the three that do not (384–394, 382–394, 380–394), and
P63092 position 379 is a cysteine. The panel enumeration is therefore internally
consistent with the canonical record. **That makes garbling unlikely; it does not
make the relay citable.**

**The likeliest reconciliation, flagged as a reading and not a finding:** the
abstract's "not effective" sentence sits immediately after its adenylyl-cyclase
sentence and may attach to **signalling** rather than to **binding** — all six
peptides bind, only the longer ones disrupt signal transduction. **This is the
single most decision-relevant open item on the ladder, because it is what decides
a rung's predicted sign.**

**So the pre-registration is about the pattern, not the rungs.**

| registered | not registered |
|---|---|
| **The response is monotone in supplied length** across 11 → 13 → 15 → 17 → 19 → 21 | any individual rung's sign |
| **Binding-like and signalling-like readouts may be different curves**, and are analysed as two, not pooled | which readout our predicate is an analogue of |
| `R2_ct15` is **the decisive rung** | that 15 is above or below a threshold |

**`R2_ct15` is still the decisive rung, and the reason has changed.** It is no
longer "the threshold sits between 11 and 17 and 15 is inside that window" — that
statement rested on the abstract's unquantified "shorter". It is now that **the
binding-versus-signalling attachment is unresolved**, so at 15 residues the wet
lab does not tell us what to expect on *either* reading. A referee will
distinguish "we lack power there" from "the literature is ambiguous there", and
the second is what is true.

**Our rungs now cover the whole wet-lab panel.** Five of the six lengths were
already rungs; **13 was not, and is added** (`R1b_ct13`, Gs `382–394` =
`IIQRMHLRQYELL`, sha `6a778b189b5ebdd2`). Item **G18a** carries 13, 17 and 19.

**The three peptides `mazzoni2000` names are now constructs.** P63092 position
379 is a cysteine and lies inside all three windows — verified, not assumed:

| construct | range | sequence (C379A applied) | sha256[:16] |
|---|---|---|---|
| `R2b_ct17@C379A` | 378–394 | `DARDIIQRMHLRQYELL` | `860804a4d60caaaf` |
| `R2c_ct19@C379A` | 376–394 | `FNDARDIIQRMHLRQYELL` | `a5f007c4c89d8f63` |
| `R3_ct21@C379A` | 374–394 | `RVFNDARDIIQRMHLRQYELL` | `087df286de75b66b` |

C379A is a **Gs-specific construct detail of that paper** — the aligned position
in Gi1, Gq, Gt1 and G13 is not a cysteine — so these are an anchor arm
(**G18b**), not rungs. The rungs are wild type.

**Species, and it is not a footnote.** `eddy2018extrinsictrp` is **human** A2AR;
`mazzoni2000` is **rat** striatal membranes. This project's standing rule is that
`_human` is never a silent default. Any sentence joining the two carries the
species difference.

**And do not say the 21-mer reconstitutes the ternary complex.** `mazzoni2000`
raised specific agonist binding but *"did not stabilize the high-affinity
state"*, with competition curves fitted by **one-site** models. The textbook
ternary-complex signature is absent on that paper's own evidence.

## 7.2 Helicity is the hypothesis — and it is helix *length*, not a helicity switch

The mechanism is stated twice, twenty-five years apart, on different receptors,
partners and assays: `mazzoni2000` reports the peptides' propensity to form
α-helix in solution, and `tran2026nanogs` finds the **unstapled linear** α5
peptide is a random coil and does nothing while the stapled 15-mer works.

**But "too short to be helical" is the wrong binary, and getting it right changes
the covariate.** Per Albrizio *et al.*, *Biopolymers* 2000, **54**(3):186–194
(reported via the same relay, so not citable until retrieved), **the 11-mer and
the 21-mer are both helical** — the 11-mer with the shortest helix, roughly
Arg389–Leu394, the 21-mer with the longest, roughly Asp381–Leu394 — and peptides
of **17 residues and more** have the stronger propensity. So the quantity that
changes with length is **helix length**, which is continuous and monotone, not
**helix presence**, which would be a switch.

**That is a stronger and more falsifiable hypothesis, and it re-specifies the
recording spec.** A helicity *fraction* cannot express it: a 6-residue helix in
an 11-mer is fraction 0.55, and a 14-residue helix in a 21-mer is 0.67 — nearly
the same number for very different objects. `g1_recording_spec.tsv` therefore now
requires **`partner_helix_span_len`, `partner_helix_span_start`,
`partner_helix_span_end` and `partner_helix_span_uniprot_range`** — the longest
contiguous helical run, where it sits, and the same span in parent Gα numbering —
alongside the fraction.

**Registered:** if the state response is monotone in length and
`partner_helix_span_len` is monotone in length with it, the two explain each
other. If the active fraction rises where helix span does not, the model
reproduces the threshold without reproducing the mechanism — a different result,
and equally reportable.

## 7.3 This is the first *in silico* titration, and not the first titration

`mazzoni2000` ran a six-point length series in vitro. **Ours is the first
titration of a biological co-input's length against a structure predictor** — a
narrower and correct claim. No sentence anywhere may read "first titration". Nor
may any sentence read "consistent with the published length dependence" without
naming the paper, the species and the assay: the literature's lengths are the
opsin 11-mers, `tran2026nanogs`'s stapled 15, `mazzoni2000`'s 11–21 panel and
`eddy2018extrinsictrp`'s 21, and only the third is a series.

## 7.4 The 21-mer rung's range matches the NMR peptide exactly

`eddy2018extrinsictrp` (Eddy, Gao, Mannes, Patel, Jacobson, Katritch, Stevens,
Wüthrich, *J. Am. Chem. Soc.* 2018, **140**(26):8228–8235, DOI
10.1021/jacs.8b03805) used *"a 10-fold molar excess of a 21-residue synthetic
polypeptide corresponding to residues 374–394 of the carboxy terminus of the
intracellular partner protein GαS"* on human A2AR. **Our `R3_ct21` for Gs is
P63092 residues 374–394, `RVFNDCRDIIQRMHLRQYELL`, sha `39355d83d34556e4` — the
same range, derived here independently from the "last N residues" rule.** The
paper reports one NMR peak for W233^6.35 where the agonist complex shows two,
with extracellular tryptophans showing at most a very small response. W233^6.35
is the cytoplasmic end of TM6, the axis our predicate reads.

**Record the structural observation; do not characterise it as activation.** The
surviving resonance sits off *both* pre-existing signals, so conformer selection
is one reading and fast exchange is another, and the paper does not adjudicate.
Whether the title says "drives active" is Aditya's call, not this document's.

## 7.5 Partner *type* may change *where* in the receptor the effect appears

`eddy2018extrinsictrp` reports a G-protein-mimicking nanobody perturbing β1AR
near the **extracellular** surface while the 21-mer perturbs A2AR
**intracellularly only**. ADRB1 is in the provisional CORE-32. Any comparison
between a nanobody arm and a Gα arm must read the **position** of the effect and
not only its sign — much better stated in advance than explained afterwards.

## 7.6 A family-specificity result predating E1.4, recorded as suggestive only

`mazzoni2000`'s abstract says Gαi1/2 C-terminal peptides were not effective on
this Gs-coupled receptor — which is the wet-lab shape of E1.4's family swap.
**But the abstract bundles "shorter" and "Gαi1/2" into one clause**, so it cannot
be determined whether a *full-length* 21-mer Gαi C terminus was ever tested — and
§7.1's binding-versus-signalling ambiguity applies to this clause too, since it is
the same sentence. **Recorded as suggestive, not as a positive prediction.** G9's
prediction is not registered on this basis. It is one of the two items the PDF
would close.

## 7.7 The two ends of the ladder sit in different placement-accuracy regimes

Declared in advance per `RUN_MATRIX.md` §3.5(2): **no single curve is fitted
through ≤50 and >50 residues.** The ladder is reported as two dose–response
segments plus a stated between-regime step. If the intermediates show the curve
is continuous across 50, that is a result; if they show a break, the two segments
were the right frame all along. The analysis plan is the same either way and it
costs nothing.

---

# 8. Findings this session made, each chased down before being called one

**8.1 `G12` cannot run at `R3_ct21`.** `RUN_MATRIX.md` §7.1 anchors the Gi/Gt
single-residue pair at `R3_ct21`. Recomputed from `seq_rungs.tsv`, Gi1 and Gt1
differ at **1** position at `ct11`, **2** at `ct15`, **2** at `ct21` and **4** at
`a5helix`. **The single-residue natural minimal pair exists at the 11-mer rung
and nowhere else** — which is what `SEQUENCES.md` §3.2 says, and which corrects
catalogue E1.6's own text as well. G12 is dispatched at `R1_ct11` here. Cost
unchanged (6,400).

**8.2 The Gi→Gs series is 15 substitutions, not 11.** Catalogue E1.5 specifies
"the 11 Gi→Gs substitutions as a second series" alongside a 21-position scan.
Recomputed: Gi1 and Gs `ct21` differ at **15** positions. **11 is the `ct15`
number and 9 is the `ct11` number** — the count was carried across from a
different rung. G10b is 15 cells, 3,000 predictions, not 11 cells.

**8.3 At `R1_ct11` the double and triple uncoupling mutants are the same
molecule.** P63092 F376 and R380 lie outside the 11-mer; only L388 is inside. So
`alphas_F376A_L388A` and `alphas_F376A_L388A_R380A` collapse to one sequence at
`ct11` (`bf09617db4664cfd` for both). Running both there is running one arm
twice — **the D2 nanobody collision, one length down**, and it is caught by
construction rather than by audit. G16's peptide-rung cells are at `R3_ct21` and
`R4_a5helix` only.

**8.4 The alanine scan has no-op positions, and they differ by family.** Gi1 and
Gt1 `ct21` already carry alanine at position 5; Gq carries it at 4 and 5. So the
"21-position scan" is 20 distinct perturbations for Gi/Gt and **19** for Gq.
These cells are worth running — they are a free within-arm wild-type replicate —
but they must be labelled `is_noop=true` and never counted as perturbations.
Preflight reports them separately from genuine collisions.

**8.5 E1.8 and E1.9 have no line item in `RUN_MATRIX.md` §7.1.** E1.8 appears
once, inside §1's 22-arm accounting; E1.9 appears **zero times** in the whole
document. E1.9 is the one `SEQUENCES.md` §6.1(2) promotes to a load-bearing
component of E1.1. Proposed here as **G16** and **G17**; both are uncosted and
`RUN_MATRIX.md` owns whether they run.

**8.6 `G4`'s cost moves by −128 / −256 predictions, and the reason is integer
division, not disagreement.** Splitting an arm's n across 5 scramble and 3
face-scramble draws gives 10×5 = 50 exactly at G4b, but 16×3 = 48 for the
face-scrambles, and 2×5 = 10 exactly but 3×3 = 9 at G4a. G4a 4,992 against §7.1's
5,120; G4b 25,344 against 25,600. **The draws are kept balanced rather than the
total kept round** — an unbalanced draw would make the permutation a fixed effect
again, which is the thing the five draws exist to avoid. If the exact §7.1 total
is wanted, raise the arm's n rather than giving one draw two extra samples.

**8.7 Two receptors with unresolved construct questions are inside the
provisional CORE-32, and subsetting does not avoid them.** `B1B1U5` (Kumopsin1,
*Hasarius adansoni* — a jumping-spider opsin, assigned cognate **Gi** by Block B
when invertebrate visual opsins are the canonical **Gq**-coupled ones) and
`OPSD` (*Bos taurus*) are the sole members of clusters `001_009_001_inv` and
`001_009_001_vert`, so the one-per-cluster rule selects them necessarily.
`SEQUENCES.md` §10 lists B1B1U5 as unresolved and it lands in the centrepiece
panel. Two mitigations are already true and worth recording: every rung from
`ct11` to `a5plus` is **species-invariant** for OPSD (human and bovine Gt1 differ
at 3 positions, none in the C-terminal 36), so only `R7`/`R8` are affected there;
and `PANEL.md`'s tier C1 uses **human** ADRB1 (P08588), which resolves
`SEQUENCES.md` §10 item 2 — the turkey mismatch is a Block B problem, not a C1
one. The spider opsin is not resolved by anything.

**8.8 `AA2AR` — the one receptor with a wet-lab result on our exact 21-mer — is
on the census but not in the provisional CORE-32.** The adenosine cluster
`001_006_001` holds AA1R (worse reference 3.20 Å) and AA2AR (3.34 Å), so the
resolution rule picks AA1R by **0.14 Å**. `eddy2018extrinsictrp`'s NMR result is
on A2AR. A pre-registered exception that swaps the adenosine representative to
AA2AR uses no quantity computed from any prediction, so it does not violate
§3.1's rule — but it is a `PANEL.md` decision and the arithmetic is recorded here
rather than acted on.

**8.9 `COUPLING.md` assigns at family level; the ladder needs a subtype, and the
gap is up to 12 of 21 residues. — SUPERSEDED, and this is how.** Recorded because
it is why the next artefact exists: a family label does not determine the bytes,
so the map was re-cut to **subtype, read off the structure** (§1). The measurement
below is what made that the obvious fix, and it still stands as the reason. `COUPLING.md` landed at 14:16 and
`coupling_assignments.csv` gives `recommended_family ∈ {Gi/o, Gq/11, Gs}` for all
64, covering all 32 CORE-32 slugs. **Family is the right grain for coupling
confidence** — inter-dataset agreement is 68% at family and 22% at subtype — but
**a family label does not determine the supplied bytes at any rung**, because
GproteinDb's families are wider than the byte-identical sets `SEQUENCES.md` §3.2
names. Recomputed here from `seq_rungs.tsv`, Hamming distance to the family's
canonical representative:

| family | rung | within-family spread |
|---|---|---|
| **Gi/o** | `ct21` | Gi2 **0**, Gi3 2, Gt1/Gt2/Ggust 2, Gz 4, **Go 6** |
| **Gi/o** | `ct11` | Gi2 **0**, Gi3 2, Gt1/Gt2/Ggust **1**, Go 4, Gz 4 |
| **Gq/11** | `ct21` | G11 **0**, G14 2, **G15 12** |
| **Gq/11** | `ct11` | G11 **0**, G14 2, G15 6 |
| **Gs** | `ct21` / `ct11` | Golf **1** |

`SEQUENCES.md` §3.2's "at peptide length most of the subtype worry evaporates" is
exactly true for the pairs it names (Gi1≡Gi2, Gt1≡Gt2≡Ggust, Gq≡G11) and **not
true for the families as the coupling authority draws them**. So one more
artefact is needed before the keyed column can resolve: **a declared family →
representative-subtype map**, fixed in advance. The cheapest defensible rule, and
it is not this document's to freeze: take the subtype named most often in
`coupling_assignments.csv:subtype_reported` for that receptor; where a deposited
structure names a subtype, prefer it; otherwise fall back to the family canonical
(Gi/o→Gi1, Gq/11→Gq, Gs→Gs, G12/13→G13). Record `partner_ga_family`,
`partner_ga_accession` and the rule that chose them per row.

**8.10 OPSD's cognate must resolve to Gt1, and the family default would not. —
CLOSED by the map, in our favour.** The structure-read rule returns **Gt1**, not
the Gi1 family fallback (§1.3). Kept because it is the one receptor where the
choice of rule changed a byte that an experiment measures.
`coupling_assignments.csv` gives OPSD `recommended_family = Gi/o` with
`subtype_reported` **empty**. Rhodopsin's transducer is transducin, and Gt1 sits
inside Gi/o by GproteinDb's grouping — so the family label is not wrong, but a
fallback to the family canonical would supply **Gi1**, which differs from Gt1 by
2 residues at `ct21` and **1 at `ct11`**. That single `ct11` residue is precisely
the contrast **G12 (E1.6) exists to measure**. OPSD is the only Gt receptor on
the panel and it is in the provisional CORE-32; its cognate is a named exception,
not a default. Also worth stating plainly: on CORE-32 the coupling verdicts are
**5 `cognate_confident`, 20 `cognate_ambiguous`, 7 `cognate_conflicted`** — so
"cognate" is a confident label for 5 of the 32 receptors carrying the
centrepiece, and every rung below `R6` inherits that uncertainty only through the
family→subtype step above.

**8.11 Twelve active references carry an engineered α5 tip, and rungs R1–R4
*are* that tip.** Relayed to me as "ten receptors, one chimeric tip
`LQMNLREYNLV`, including DRD4 and OPSD". Checked against
`coupling_refstructures.csv` before writing it down, and the substance holds while
the specifics do not. `g1_refchimera.py` → `g1_refchimera.tsv`.

*The corrections first.* `LQMNLREYNLV` appears on **10 reference entities but 9
distinct receptors** — ADA1A has two. The nine are 5HT2A, 5HT2C, ADA1A, EDNRA,
**GRPR**, HRH1, OX2R, OXYR, TA2R. **DRD4 and OPSD are not among them and GRPR was
omitted.** DRD4 and OPSD do carry non-canonical tips, but different ones, and
OPSD's is the most consequential single construct on the panel.

*What is actually there.* Of 81 reference entities carrying an α5 tip, **13 are
non-canonical for all 16 human Gα — 12 distinct receptors, and on all 12 the
offending entity is the reference Rule R actually picks.** Four classes:

| tip (ct11) | n | nearest canonical | partner len | receptors |
|---|---:|---|---:|---|
| `LQMNLREYNLV` | 9 | G11/Gq, **2/11** | 244–361 | 5HT2A, 5HT2C, ADA1A, EDNRA, GRPR, HRH1, OX2R, OXYR, TA2R |
| `LQNNLKECNLV` | 1 | G11/Gq, 2/11 | 352 | B1B1U5 |
| `IKMNLRDCGLF` | 1 | Ggust, 2/11 | 361 | DRD4 |
| `VLEDLKSCGLF` | 1 | Gt/Ggust, **4/11** | **11** | **OPSD** |

**Six are in the provisional CORE-32: 5HT2A, B1B1U5, GRPR, OPSD, OX2R, OXYR.**
The other six are C1-only and therefore hit G2, not the headline arm.

**The mismatch grows with rung length, and it is worst at the title's rung.** The
nine mini-Gs/q chimeras are two-window constructs — a mini-**Gs** scaffold with a
Gq-like tip — so at `ct11` they are 2 of 11 from canonical Gq (identity 0.82) but
at `ct21` the deposited 21-mer is `RIFNDCKDIILQMNLREYNLV` against Gq's
`FVFAAVKDTILQLNLKEYNLV`: **8 of 21 residues differ, identity 0.62**. Supplying
wild-type Gq `R3_ct21` to those receptors and reading interface register against
their active reference compares a 21-mer with a 21-mer that differs at eight
positions.

**Scope it honestly, because overstating it is its own error.** The state
predicate is **receptor-internal** — d(Y5.58 OH, Y7.53 OH) and d(2×46 Cα, 6×37
Cα). The reference's Gα chain is not scored. So this is **not** a direct scoring
mismatch in the predicate. It bites in three narrower places and only those:
(a) *reference provenance* — the reference's active receptor geometry is the
geometry an engineered tip produced, so the predicate's "active" is defined as
"looks like what miniGsq produced"; probably small, since the TM6 opening is
large, but unverified rather than verified; (b) **every interface readout in §6
that compares our predicted partner placement to the deposited one** —
`contact_register_last5_json`, `d_ga_alpha5_r350_ca`,
`n_interface_contacts_ga_receptor` — which is the real cost; (c) **E1.4 (G9)**,
where the "cognate Gq tip" the structural-biology community used is not canonical
Gq.

**OPSD is a separate case and it is the sharpest on the panel.** Its Rule-R
active reference **4X1H** supplies an **11-residue peptide entity**,
`VLEDLKSCGLF`, described as a C-terminal derived peptide of Gt and 4 of 11
residues from canonical Gt1. Two consequences pull in opposite directions and
both should be said. **It is the only deposited structure on the whole panel
where the partner is a peptide at one of our rung lengths** — so `R1_ct11` on
OPSD is the single best-referenced cell in the ladder. And it is an *engineered
high-affinity analogue*, so the wild-type Gt1 11-mer we would supply is not it.
`verify_partner_chains.py` already knows: its source comment names 4X1H by name
and flags it `NO-UNIPROT-XREF`. Note also that OPSD's deposited entity is 11
residues long, so **OPSD has no α5 reference at all beyond 11 residues** —
rungs R2 through R8 have no partner-conformation reference for it.

**B1B1U5 gains a third independent line of evidence.** Its active reference 9EPP
carries a Gα whose tip is **Gq-like** (2 of 11 from Gq) while its only UniProt
cross-reference is **P63096, Gi1**. Block B assigned it Gi; §8.7 and §10.1 record
the coupling as unresolved; the deposited structure independently says the tip
that was crystallised is not Gi's.

**And a correction to how the detector was described.** I was told
`verify_partner_chains.py` cannot catch this class because the chimeras return
`NO-UNIPROT-XREF`. That is right for ten of the thirteen and it is the script
behaving correctly. **For the other three it is worse than that.** ADA1A/8THK
carries `P04899;P50148;P63092` and GRPR/8H0Q carries `P63092;P63096` — a chimera's
real tell is **more than one** cross-reference, not zero — and the script takes
the **first** xref and `break`s (`verify_partner_chains.py:88-91`). It then
compares a Gs-scaffold/Gq-tip chimera against canonical **Gi2** and reports a long
substitution list attributed to the wrong parent. A silent wrong answer, not a
flag.

**Three options, costed, none chosen here.** Affected CORE-32 receptors: 6 of 32.

| option | build cost | compute cost | what it buys, what it costs |
|---|---|---:|---|
| **1. Supply wild-type, declare the mismatch** | 0 | **0** | Keeps all 32 comparable. Every register/contact readout on those 6 becomes like-for-unlike at 8 of 21 residues at `R3_ct21`; they must be excluded from any interface comparison and `ref_alpha5_tip_identity` reported per row |
| **2. Supply the deposited tip *alongside* the wild-type one** | **0 — built, hashed, in the registry** | **440 pooled / 2,200 per-cell** (item **G19**, 11 systems) | Measures directly whether the model cares about the 2-of-11 / 8-of-21 residues. Adds an arm rather than replacing one, so comparability is untouched. **This is the cheapest informative option in the whole document** |
| **3. Drop the 6 from the primary arm** | 0 | saves ~19% of every CORE-32 arm | CORE-32 → 26 clusters, so every pooled half-width widens by √(32/26) = **1.11**, and it loses **OPSD — the only Gt receptor on the panel — and B1B1U5** |

Option 2 is registered as **G19 (proposed)** in §4 and costs nothing to build
because the bytes are already in the reference. Whether it runs is
`RUN_MATRIX.md`'s and the PI's call. Preflight **B12** fails the run if an
affected CORE-32 receptor is not carried explicitly, and
`g1_recording_spec.tsv` now carries `ref_alpha5_tip_identity`,
`ref_alpha5_is_canonical` and `ref_alpha5_pdb` so that under *any* of the three
options the mismatch is visible per row rather than assumed away.

**8.12 One CORE-32 receptor resolves to a family neither control table covered —
and the two tables behaved very differently under it. CLOSED.** The cognate map
puts **SSR2** on **Gi3** (`STRUCTURE_EXACT`, 7T10, tie set Gi3 — unambiguous).
`seq_controls.tsv` (240 peptide controls) and `seq_a5null.tsv` (15 α5-null
variants) each covered five families — Gs, Gi1, Gq, G13, Gt1 — and Gi3 was not
among them, so SSR2's G4 composition controls and its G3 α5-null arms had no
construct at all. **Found by resolving the map rather than by reading it:** the
systems table reported 12 `UNRESOLVED` cells and named the family.

The two tables split on one thing — whether the generator shipped — and that
decided everything else.

- **`seq_controls.tsv` had its generator, so the rule was reused rather than
  re-invented.** `seq_controls.py`'s own `scramble`, `face_scramble` and `rng_for`
  are imported and called with the same key order. **Proved before use:** that
  code path reproduces all **160** existing scramble and face-scramble draws byte
  for byte, and `g1_partner_registry.py` re-proves it on an existing draw every
  run before extending. 96 Gi3 controls built, same rule, no new convention.
- **`seq_a5null.tsv` did not**, and the permutation was not recoverable: eight
  plausible key orders through `rng_for` were tried and none reproduced it,
  though the draw was confirmed a genuine permutation of G.H5 (same multiset). So
  `R6c_a5polyA` was rebuilt exactly — poly-alanine is deterministic — and
  `R6b_a5perm` was built only under a **declared substitute rule**, labelled as
  not byte-consistent with the other five families. Flagged, never silently
  adopted.

**`seq_a5null.py` now exists and the key was
`(family, "a5null", "permute", "redo_v1", 1)`.** Four things hid it at once and
none announces itself: no rung term (one α5-null per family, not per rung), the
control term split across two fields, the trailing `1` an `int` stringified by
`map(str, parts)`, and — the one that makes brute force useless — **every
rejected draw still consumes RNG state**, so the accepted permutation depends on
every draw before it. The table is regenerated to seven families and **the
substitute constructs are withdrawn**; every α5-null construct now comes from one
generator, which preflight **B15** enforces.

**The cross-generator check the swap made possible, and it passed.** Three
constructs are deterministic, so two independent generators must agree on them
byte for byte — and a disagreement would have been about the core slice, not the
seed, meaning one generator was wrong. Checked rather than assumed:

| construct | family | our independent rebuild | `seq_a5null.tsv` | |
|---|---|---|---|---|
| `R6c_a5polyA` | Gi3 | `2a4b0d53d0378be5` | `2a4b0d53d0378be5` | agree |
| `R6c_a5polyA` | Go | `24d43f151c3f5cb4` | `24d43f151c3f5cb4` | agree |
| `R6a_da5` | Gi3 | `d1518b6c4a99cca1` *(from `seq_rungs.tsv`)* | `d1518b6c4a99cca1` | agree |
| `R6a_da5` | Go | `2b951794efb82c9b` *(from `seq_rungs.tsv`)* | `2b951794efb82c9b` | agree |

All fifteen original rows are unchanged, both new permutations preserve
composition exactly (Hamming 24/26 for Gi3, 21/26 for Go), and the two
authoritative `R6b_a5perm` shas — Gi3 `16830343462a56a0`, Go `9d59dfcdc64a11da`
— are taken from the file rather than retyped. **The poly-Ala rebuild is kept in
`g1_partner_registry.py` as a live cross-generator check over all seven families
rather than deleted**, because it is the one place two generators can be held
against each other for free.

**What generalises.** This is the durability split the project already names,
caught in the act: a *perishable* table shipped without its *durable* generator
cost a working day of unrecoverable search, while the table that shipped with one
was extended in minutes under the identical rule. The guard that replaced the
substitute path fails loudly the next time a cognate subtype appears that the
α5-null table does not cover — it no longer builds anything itself.

**8.13 `R6a_da5` agrees byte-for-byte between its two independent source
tables.** `seq_rungs.tsv` and `seq_a5null.tsv` both emit it; all five shared
families match. Checked because two tables producing one construct is exactly
where a silent divergence lives. Preflight **B10**.

**8.14 One GPCRdb/UniProt residue disagreement, chased and cleared.** GPCRdb's
CGN table for **G15** (GNA15, P30679) gives **Y** at position 147 where UniProt
gives **C**. It is inside H.HD, outside every residue span this session slices,
and G15 is not on the panel. Constructs are emitted and their provenance is
UniProt, not GPCRdb. The check that found it drops any construct whose emitted
span *would* contain a mismatch, and it was proved by planting one.

---

# 9. Dispatch-readiness checklist

Run `python3 redo/gates/g1_preflight.py`. Exit 0 means dispatch may proceed.

## Blocking — mechanical, all sixteen currently pass and all sixteen were proved

| | check |
|---|---|
| B1 | every input artefact exists |
| B2 | every chain-B construct resolves in the registry — **re-resolved against the registry, not read back from the column the generator wrote** |
| B3 | every held construct carries a full 64-hex sha256 |
| B4 | no system dispatches a construct whose bytes are not held |
| B5 | every system row resolves chain B to a numeric length — the naming trap |
| B6 | no two cells within one arm are the same molecule — the D2 defect, by construction |
| B7 | every row declares a partner-MSA and a receptor-MSA condition |
| B8 | MSA-free on the partner chain is the primary condition |
| B9 | the **frozen** panel is one per cluster, declared overrides the only exception, and carries no chimeric-reference receptor — §1.4 |
| B10 | `R6a_da5` agrees byte-for-byte between its two source tables |
| B11 | the per-row recording spec carries the load-bearing columns |
| B12 | every receptor whose active reference carries an engineered α5 tip is carried explicitly, and the per-row identity columns exist — §8.11 |
| B13 | every cognate row resolves to a 64-hex sha, or is a declared chimera naming all three options — §1.4 |
| B14 | every cognate row carries its evidence class, so a structure read and a convention fallback cannot be confused — §1.2 |
| B15 | every α5-null construct comes from `seq_a5null.tsv` — one generator for the whole arm — §8.12 |
| B16 | every row carries **both** the supplied-partner family and the reference tip, never one without the other — §1.7 |

## Outstanding before a single prediction is submitted

| | what | owner |
|---|---|---|
| D1 | **DONE.** `COUPLING.md` landed, was verified against our own sources, and is consumed; 54 of 64 receptors and 28 of 32 CORE-32 members are hashable — §1.1–§1.2 | — |
| D1b | **DONE.** OPSD resolves to Gt1 from the structure, not to a family default — §1.3 | — |
| D1c | **DONE.** The ten chimeras are excluded from the primary panel and carried in the extension tier with G19 as the matched control — §1.4 | — |
| D1d | **DONE.** `seq_a5null.py` shipped, the table covers seven families, the substitute constructs are withdrawn and B15 enforces one generator — §8.12 | — |
| D2 | **`SEQ_RECEPTORS.md` joined** — chain-A bytes hashed per row (landed; not yet joined here) | this list, on the join |
| D3 | **DONE by declaration.** The panel is frozen at 30 receptors / 29 clusters — `PANEL.md`'s provisional list, minus the chimeras, plus the AA2AR override — §1.4–§1.6 | — |
| D4 | **the pre-flight partner-MSA depth measurement** on the ~60 distinct peptide-rung sequences — `cheap`, no inference, and it is what turns §0.2 from a prediction into a measurement | pipeline |
| D5 | **`RUN_MATRIX.md` decides G16/G17** (E1.8, E1.9), and whether `M3_h3`, `M5_dHD` and the G1f anchors run | run-matrix session |
| D6 | **B1B1U5's cognate Gα resolved, or the receptor leaves the panel** | PI / panel session |
| D7 | **the row-level delivery contract agreed** (`g1_recording_spec.tsv`), including seed pairing across arms within a cell — impossible to add after dispatch | pipeline |
| D8 | **E4.2's exposure covariate exists and the median split is declared**, before G3 dispatches — `RUN_MATRIX.md` §10.5(a) makes this a hard predecessor, not a parallel item | analysis |
| D9 | **G3's pilot leg run and the Gα fold-integrity gate checked** before G3b's 38,400 | pipeline |
| D10 | **a three-chain input schema exists** for G11 — a harness change, not a dispatch | pipeline |
| D11 | **the §8.11 option chosen**, and `ref_alpha5_tip_identity` / `ref_alpha5_is_canonical` / `ref_alpha5_pdb` emitted per row whichever option it is | PI / pipeline |
| D12 | **`verify_partner_chains.py` fixed for multi-xref entities** — it takes the first cross-reference and `break`s, so a three-xref chimera is compared against the wrong parent and reports a confident wrong answer (§8.11). Not blocking for Group 1, which uses the hash path, but it is the detector everyone else trusts | orchestrator |

## Standing rules for the dispatcher

1. Resolve chain B by **sha256**, never by header, and fail loudly on a miss.
2. Emit `n_partner_aa` and `partner_seq_sha256` per row, so every rung is
   verifiable from the data rather than from the dispatch note.
3. Never name a construct in a manifest, a caption or a heading without its
   resolved length beside it.
4. Pair seeds across arms within a cell.
5. Run G3's and G1e's integrity readout before their full arms.

---

# 10. Open — flagged, not guessed

1. **B1B1U5 has no defensible cognate Gα** and the one-per-cluster rule puts it
   in CORE-32. §8.7. `coupling_assignments.csv` now records the same verdict
   independently: `recommended_family = Gi/o`, `verdict = cognate_ambiguous`,
   basis *"NONE — plurality of 1 authorities only; needs a PI decision"*.
2. **The family → representative-subtype map.** §8.9. Without it no rung below
   `R6` has determinate bytes, and it is the single artefact standing between
   this list and a dispatchable one.
3. **Which of the three options in §8.11 is taken for the six CORE-32 receptors
   whose active reference carries an engineered α5 tip.** Option 2 is built and
   costs 440 predictions; option 3 widens every pooled half-width by 11% and
   loses OPSD and B1B1U5. PI and `RUN_MATRIX.md`.
4. **Whether the adenosine representative should be AA2AR rather than AA1R.**
   §8.8. `PANEL.md`'s call.
5. **Whether `M3_h3`, `M5_dHD` and the three deposited anchors are funded.**
   `RUN_MATRIX.md`'s call; the constructs exist and are hashed either way.
6. **Whether `R2_ct15` should carry `tran2026nanogs`'s two chemical
   modifications** (Y391Nal, E392hGlu). Non-canonical residues are outside every
   backbone's vocabulary, so the answer is probably no — but it is the gap
   between our 15-mer and the only 15-mer with a wet-lab result, and it should be
   stated rather than omitted.
7. **Nanobody tags.** `Nb60/5JQH` and `Nb6/6VI4` carry C-terminal `HHHHHH`;
   Nb9-8 carries a leading `GPGS`. If nanobody arms are ever compared with Gα
   arms — and §7.3 says they should be — decide once whether tags stay. Six
   unstructured residues at the end of a 125-mer is exactly the kind of thing that
   shows up in a contact count.
8. **`ubiquitin` and `KaiB` match no rung exactly.** §4.2. Compare within
   tolerance and record Δ, or add a rung at 76 and 91 — but there is no CGN
   segment boundary there, so such a rung would be defined by a number and would
   break §2.1's rule.
9. **`gcn4_window` stops at 33 residues**, so the helicity-matched control does
   not reach `R5_a5plus`. §5.1. Not currently load-bearing.
10. **`mazzoni2000` is abstract-only and the relay contradicts it.** Three things
   turn on the PDF, in priority order: **(i) whether "not effective" attaches to
   BINDING or to SIGNALLING** — this decides every rung's predicted sign and is the
   single most decision-relevant open item on the ladder; (ii) the peptide
   concentration for the adenylyl-cyclase effect; (iii) whether a full-length Gαi
   21-mer was ever tested on this Gs-coupled receptor, which decides whether G9
   has a registered prediction or only a suggestion. §7.1, §7.6. Until then,
   `dursi2011signalpeptides` is a relay and nothing in it is citable as
   `mazzoni2000`.
11. **Albrizio *et al.*, *Biopolymers* 2000, 54(3):186–194** — the source of the
   helix-length observation §7.2 rests on — reaches us through the same relay and
   is not in the corpus. The recording-spec change stands regardless (a helix-span
   column is better than a fraction either way), but the *prediction* that helix
   span is monotone in length needs the primary.
12. **Block D's three non-Gs "cognate_ga" arms** remain unresolvable from the
   drop, because the Gα chains were never hashed. Nothing in Group 1 depends on
   it; recorded because it is the strongest argument for rule B3.

---

---

# 11. Frozen — what is settled, what is deferred, what is uncosted

Group 1 is frozen as of 2026-09-11. **The governing principle for everything
above: Group 1 is strict — stricter than Group 0 — because Group 0 is us tuning a
measure and Group 1 is what actually gets dispatched.** Where the two could be
traded off, strictness won and the power cost is stated rather than absorbed.

## 11.1 Frozen

| | |
|---|---|
| **Panel** | **30 receptors in 29 clusters.** `PANEL.md`'s provisional list, minus the ten chimeric-reference receptors (which are ineligible, not merely dropped), plus AA2AR as a declared override. Backfill recovered one cluster; the penalty is √(32/29) = **1.050×** on every pooled half-width |
| **Rungs** | 0, 11, 13, 15, 17, 19, 21, 26, 36, ~45, ~61, ~113, ~204, ~240, 350–394, +βγ — every one a CGN segment or a "last N residues" rule, every one hashed, none named after a construct |
| **Conditions** | partner MSA **off** everywhere as primary, on at three fixed lengths as the E1.9 contrast; ligand **none** throughout; n and backbones copied from `RUN_MATRIX.md` §7.1 |
| **Cognate** | **two columns, never one** — biology supplied, structure scored — with the independence of the biology column recorded per row |
| **Constructs** | **771**, keyed by sha256, never by header; `1,451` system rows carry a resolved 64-hex sha |
| **Systems** | **2,039**, every one enumerated per receptor, nothing templated |
| **Gate** | **16 blocking checks, all passing, all proved by planting a defect** (`g1_preflight.py --selftest`) |

Total dispatch: **74,960 pooled / 212,920 per-cell**, of which the primary tier is
70,080 / 204,840 and the two extension tiers 4,880 / 8,080.

## 11.2 Deliberately deferred — not defects, and each one visible in the gate

- **The partner-MSA depth pre-flight** (`SEQUENCES.md` §6.1(4)). The single
  design claim the whole ladder rests on — that at peptide length MSA depth
  tracks conservation, not length — is measured from this project's own cache but
  has not been re-measured on our ~60 distinct rung sequences. **It cannot be run
  here: there is no MSA tooling on this machine.** It is hours of wall-clock and
  no inference for whoever has the pipeline, and until it runs, §0.2 is an
  inference from a cache rather than a measurement on our constructs.
- **OPSD past rung `R1_ct11`.** Its active reference supplies an 11-residue
  peptide, so it is the best-referenced cell in the ladder at rung 1 and has **no
  α5 reference at all** at rungs 2 through 8. Everything above 11 residues for
  OPSD is extrapolation. It stays in the panel — it is the only Gt receptor and
  the only Gt-subtype read on the panel — with the caveat carried per run.
- **Two no-op cells in the alanine scan.** Gq `ct21` already carries alanine at
  positions 4 and 5, so those two arms are byte-identical to wild type. Run them,
  label them `is_noop=true`, and count them as within-arm wild-type replicates —
  never as perturbations.

## 11.3 Uncosted — real experiments with no line item

- **G16 (E1.8, uncoupling mutants)** — 36 systems, **7,200 predictions**. E1.8
  appears once in `RUN_MATRIX.md`, inside a counting sentence, and has no item in
  §7.1. Decision 3 grew it: AA2AR is Gs-coupled, so `CORE32_GS` went from 5 to 6.
- **G17 (E1.9, partner MSA on/off)** — 90 systems, **3,600 / 18,000**. E1.9
  appears **zero** times in `RUN_MATRIX.md`, and `SEQUENCES.md` §6.1(2) promotes
  it from an optional side-experiment to a load-bearing component of E1.1.
- Also uncosted, smaller: **G18a/b** (the wet-lab length series, 3,600 / 18,000
  and 180), **G19** (the matched control that makes Decision 1 honest, 920 /
  4,600), **G1e/G1f/G1c-opt** (the ΔHD companion, the deposited mini-G anchors
  and the optional fourth intermediate), and **G20** (the chimeric extension tier,
  1,200).

## 11.4 The seven standing dependencies

Every one is a real dependency and none was removed to make the gate pass — a
gate that passes because the checks were deleted is worse than one that fails.

| | what | owner |
|---|---|---|
| 1 | the MSA-depth pre-flight (§11.2) | pipeline |
| 2 | OPSD's extrapolation caveat travels with every OPSD row above rung 1 | analysis |
| 3 | the two no-op alanine cells are labelled, not counted | pipeline |
| 4 | six convention fallbacks named on every run — **OPRM has no active reference containing a Gα at all**; NTR1's rests on a non-Rule-R structure | analysis |
| 5 | four assignments reverse Block B's prior; **B1B1U5 is read from the map every run, never hard-coded**, because 9EPP → 9EPR would flip it to Gi1 | coupling |
| 6 | G16 / G17 uncosted (§11.3) | run-matrix |
| 7 | the ten chimeras' PI decision is *recorded as taken* — they are excluded — but the tip-vs-scaffold question survives for anyone who runs the extension tier | PI |

## 11.5 Three things I could not close, stated plainly

1. **`paper_af3`'s coupling table is not on this machine**, so the 31-of-35 diff
   behind Decision 2 cannot be re-derived here. From our own sources the
   family-level disagreement count is **zero**, and the four named receptors are
   the four that reverse *Block B's prior* — a different question. §1.7.
2. **Decision 1 was costed at four lost clusters and it is three.** The
   eligibility-filter reading of "strict" re-selects 5HT5A inside the serotonin
   cluster, so the penalty is 1.050× rather than 1.069×. Both numbers print on
   every run; `BACKFILL = False` gives the harsher reading if that was intended.
3. **The biology column is not independent of the structure column on 13 of 64
   receptors**, and on three of those the deposited reference is the chimera —
   circular in exactly the way `jsGiq` is. All three are in the excluded tier, so
   none reaches the primary panel, but it was invisible until Decision 2 forced
   the columns apart. §1.7.

## 11.6 What would unfreeze this

A changed `PANEL.md` reference under Rule R (B1B1U5's 9EPP → 9EPR is the live
one), `paper_af3`'s coupling table landing, the MSA-depth measurement coming back
different from §0.2's expectation, or the `mazzoni2000` PDF resolving whether
"not effective" attaches to binding or to signalling — which is the one open
literature item that decides a rung's predicted sign. Everything else is a
budget decision, not a specification one.

---

# Questions for lit

Each states what changes per answer.

1. **Does any paper report a per-position or per-residue analysis of a *supplied*
   partner chain — not a self-mutation of the receptor or the target?** The
   catalogue's sweeps say no (`/deep mutational|saturation mutagenesis/` 0 of 81;
   `/alanine scan/` 1, wet lab). *If that holds*, G10 is stated as the first and
   `waymentsteele2024cluster` is cited as the protocol. *If someone has done it on
   a supplied chain*, I need their construction rule so the 21 substitutions are
   comparable rather than merely different, and G10's framing moves from first to
   replication.

2. **Is `eddy2018extrinsictrp` now in the corpus with page numbers, and does it
   state a concentration-dependence or only the single 10-fold molar excess?**
   §7.1 rests on it. *If it reports a titration*, the ladder has a wet-lab dose
   analogue and §7.2's "no published length series" needs softening to "no
   published *length* series; one published *concentration* series". *If it is a
   single concentration*, §7.2 stands as written.

3. **Does any paper supply a deposited engineered construct — a mini-G, a
   thermostabilised subunit, a chimera — as a model input rather than as a
   reference?** G1f does exactly this. *If there is precedent*, I cite it and the
   anchor arm is routine. *If not*, G1f needs a sentence saying that supplying an
   engineered construct to a model trained on wild-type sequences is itself a
   choice, and the engineered substitutions (13/23/31 residues) should be reported
   as a covariate.

4. **Has anyone measured how a co-folding model treats a fragment that cannot
   fold on its own — a half-domain, a domain-swapped truncation?** `M3_h3` and
   `M4_he` are fragments of a fold, not folds. *If the corpus has a partner-chain
   pLDDT baseline for such fragments*, the §6 integrity gate gets an external
   threshold instead of an internal one. *If not*, `polyA` and `gcn4_window` have
   to bracket the pLDDT range internally, which adds an analysis step and no
   predictions.

5. **Is there any structural or wet-lab result on a Gα α5 peptide between 21 and
   50 residues?** The rungs are 11/15/21/26/36 then 44–47. *If a 30-mer or a
   40-mer result exists*, it becomes a rung and it is the cheapest possible
   addition, since every length in that window is a CGN-free slice. *If not*, the
   spacing stands as literature lengths plus the two CGN invariants plus the
   junker boundary — a defensible rule.

6. **Does the corpus say anything about chain-order sensitivity in multi-chain
   co-folding inputs?** G11 supplies three chains and nothing in any block
   establishes order-invariance. *If a paper measures it*, I cite the effect size
   and run one order-swapped cell as confirmation. *If nobody has*, the
   order-swapped cell becomes a first-class arm and G11's cost rises.

7. **What is the shortest peptide `mazzoni2000` actually tested, and is any Gαi
   21-mer among them?** The abstract says only "shorter peptides from Gαs and
   Gαi1/2 … were not effective". *If the PDF names the shortest length*, §7.1's
   registered prediction sharpens from "the transition is between 11 and 17" to a
   bracket, and `R2_ct15`'s status as the decisive rung is either confirmed or
   moved. *If a full-length Gαi 21-mer was tested and failed*, §7.6 stops being
   suggestive and G9 gets a registered prediction rather than an open question.

8. **`tran2026nanogs`'s stapled 15-mer works only with agonist present. Does any
   paper report a partner effect that is conditional on ligand occupancy in
   silico?** Group 1 runs ligand-free throughout, and §3.2 hands the crossing to
   Group 2's G6. *If the corpus has an in-silico conditional effect*, the case for
   putting `R2_ct15` and `R3_ct21` into G6's partner levels becomes a citation
   rather than an inference — which is worth having, because it is the one place
   Group 1's ligand-free design could be argued to have missed the effect.
