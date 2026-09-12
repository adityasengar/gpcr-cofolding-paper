# spec/DECISIONS.md — decisions that govern the redo, with their reasons

An outcome without its reason gets re-litigated. Newest first.

---

## D-2026-09-11-c · The manuscript stays frozen; the protocol findings feed the redo

**Aditya, 2026-09-11.** We established this afternoon that the frozen manuscript
describes an activation predicate the scorer never ran. His call: **the paper is
the record of what was done and it stays as it is.** The findings become inputs
to the redo, which is where they can still change something.

Consequence: nothing below is a correction to `manuscript/`. Every item is a
requirement on the redo.

---

## D-2026-09-12-b · D-H CLOSED — B1B1U5 stays, at 9EPP, as (c′); (e′) offered as an extension arm

**Aditya, 2026-09-12.** On the recommendation of `spec/D_H_RESOLUTION.md` §7.

**(c′).** B1B1U5 stays in the **PRIMARY** panel, which remains **30 receptors /
29 clusters**. Its `cognate_family` is **Gq** — the deposited tip is genuinely
jumping-spider Gαq1 (INSDC `LC799818`) and the experimenters' design intent was
Gq. Its `reference_tip` is **9EPP**, recorded explicitly as a spider-Gq-tipped
chimera on a human Gαi1 backbone.

**Methods must state that no native complex exists for this receptor.** 9EPP is a
chimera; 9EPR is human Gαi1 from *E. coli* reconstituted *in vitro* with **bovine**
Gβ1γ1. **`PANEL.md` Rule 4 is therefore INAPPLICABLE here, not merely
unimplemented** — its second clause requires a native option to demote to. Rule 4
stays on the books, scoped, and still unimplemented in code for the cases where it
*can* fire.

**(e′)** — supply the **spider** Gαq1 α5-CT instead of the human one — is an
EXTENSION arm, deliberately outside the primary ladder because it puts a
non-human partner into a human-partner ladder. It is **constructible only to 17
residues** (ceiling 18, the whole recorded segment): `tejero2024opsin` p10 records
18 spider residues and we do not hold `LC799818` itself, so `ct19`, `ct21`,
`a5helix`, `a5plus` and the full subunit are **not built and not invented**. In
particular the deposited 21-mer is *not* a spider 21-mer — its first three
residues are human backbone. `D_H_RESOLUTION.md` §9.2 has the rung table;
`g1_partner_registry.tsv` has the constructs, `spidertip_*`.

**Three statements this closes and corrects.**

- ~~"Three documents say 9EPR; the frozen artefact says 9EPP"~~ — the artefact was
  right. What said 9EPR was `PANEL.md`'s own prose contradicting its own §6.1
  table, plus two documents repeating it.
- ~~"the 0.86 tip is engineered"~~ — it is **species divergence**. RCSB's own
  `pdbx_mutation` for `9EPP_2` reproduces the spider segment from human Gαi1
  exactly, so this is checkable without the paper, and `gates/panel_verify.py`
  now checks it.
- ~~"invertebrate visual opsins are canonically Gq"~~ — **no locator**, and it
  must not be used as evidence (D_H_RESOLUTION §6f).

**A second defect found while implementing it.**
`g1_panel_freeze.tsv:supplied_partner_independence` claimed **"annotation only —
independent of the structure"** for **B1B1U5 and OPSD**, both PRIMARY. Neither has
any non-structure coupling authority: `coupling_assignments.csv` gives both
`n_authorities = 1`, and that authority is `authority_structure`. The column whose
whole purpose is to keep biology and structure apart was asserting independence
where the two are the same evidence. Fixed in the generator; both rows now say so.

**What is unblocked, and what is not.** B1B1U5's ligand curation is no longer
blocked on D-H, and F-11's shared-CCD trap turns out not to apply to it — 9EPP's
agonist is `A1H6M` (11,20-ethanoretinal), the 6I9K inverse agonist is `RET`
(11-cis retinal). What still blocks it is **amendment §C-1**, which dropped
`inverse_agonist` from Tier 3, and the fact that the existing curated agonist row
is keyed to 9EPR. Both are decisions, not chemistry. `LIGAND_CURATION_PROPOSAL.md`.

**What still makes this uncomfortable, recorded rather than resolved.**
`tejero2024opsin` reports that TM5/TM6 open **further** in the chimera complexes
than in the hGi complex and argues the Gα subtype sets the extent of TM6
movement — the axis our predicate measures. Both chimera models are also
incomplete at the cytoplasmic end of TM6, at 4.06/4.15 Å against 9EPR's 4.9 Å.
This does not argue for 9EPR, which is not native and worse-resolved; it means
**B1B1U5's reference geometry is the least trustworthy in the primary panel**,
and it deserves a per-receptor sensitivity check in the measurement pass.

---

## D-2026-09-12 · Four campaign decisions, from `CAMPAIGN.md` §10

**Aditya, 2026-09-12.** All four taken on the recommendation.

**D-A — the state is called from NPxxY-OH alone; the TM6 tilt is reported as a
continuous second axis, never conjoined.** Reason: it is the predicate that
actually ran, so Group 0 calibrates something real and our numbers stay
comparable with `paper_af3`'s. The tilt cannot be the second instrument — no
dynamic range, and circular on the same atom pair as GPCRdb's inactive pole.
Methods must state why it is reported and not conjoined. **Cost: 2 of the frozen
30 (EDNRB, HRH3) become NPxxY-blind with no inherited fallback** — they need an
explicit rule, not a silent NaN.

**D-B — closed by measurement, not choice** (see F-5). The partner runs MSA-free
at every rung. The residual arm (E1.9, +1,200 in the pilot) answers "how much did
we change by doing that?", which is the first question a referee asks. Keep it.

**D-C — curate small-molecule agonist/antagonist pairs for six receptors.**
Reason: at k = 9 clusters the interaction MDE is **0.406**, larger than every
Block B decomposition term but one, so the arm cannot do its job as it stands.
Six receptors takes k to 15 and MDE to **0.314**, for zero GPU. The eight
peptide-only-agonist receptors are a *different experiment* — a peptide agonist is
a third protein chain and flips OpenFold-3's `use_paired_msas`, and `endothelin1`
is exactly 21 residues, the same as `ct21`, so EDNRB cannot be crossed with a
peptide rung without explicit chain labelling.

**D-C WORKLIST, corrected and independently reproduced 2026-09-12.** The figures
in `CAMPAIGN.md` §5.2/§10 are **wrong** — they say 10 receptors / 9 clusters and
"curate six". Correct: **baseline 9 receptors / 8 clusters, MDE 0.431; curate
SEVEN; target 16 receptors / 15 clusters, MDE 0.314.** Aditya's decision stands and
the gain is slightly larger than he was told.

The test that matters, and the one my own first derivation missed: **a row is not a
curation.** `ADRB1`, `B1B1U5`, `GHSR`, `HRH3` and `OPSD` each carry a ligand row
with `is_peptide=false`, **no SMILES and no PDB** — verified directly against the
files. The reliable test is `is_peptide=false` AND a non-empty `smiles`, **on both
roles**. `n_agonist_smiles` in `panel_systems.csv` cannot do it: a peptide carries
a SMILES string too.

| receptor | cluster | missing | note |
|---|---|---|---|
| **S1PR1** | `001_004_004` | both | absent from both ligand sets entirely |
| **CCKAR** | `001_002_005` | agonist | curated agonist is CCK-8 (`DYMGWMDF`, peptide) |
| **GHSR** | `001_002_010` | both | agonist is ghrelin peptide |
| **ADRB1** | `001_001_003` | antagonist | placeholder row |
| **HRH3** | `001_001_005` | agonist | placeholder row |
| **OPSD** | `001_009_001_vert` | antagonist | **may be impossible — see below** |
| **B1B1U5** | `001_009_001_inv` | antagonist | **not blocked by chemistry after all** — D-2026-09-12-b |

Curate in that order; the first five carry the value.

**OPSD and B1B1U5 may not be curatable at all, and the reason is chemistry.** Both
are retinal receptors: agonist (all-*trans*-retinal) and antagonist
(11-*cis*-retinal) are the same molecule in different isomers, covalently bound
through a Schiff base. `PANEL.md` §10 already records these two among four that
Block C could not run, "and the reason is chemical, not operational."
**If they fail, k = 13 and MDE = 0.338** — still worth curating the other five.

**Coupling to D-H — now closed, see D-2026-09-12-b.** B1B1U5's curated agonist row
is keyed to **9EPR**, and D-H resolved to **9EPP**, so that row now points at a
structure the panel does not use. It must be re-keyed or explicitly marked
off-reference before it is curated. The *antagonist* candidate on `6I9K` is clean
and carries a different CCD from 9EPP's agonist, so the "both roles are `RET`"
objection above is **true for OPSD and false for B1B1U5**. {ref-history}

**D-D — build a defensible decoy rule, gate it, and run the arm only after the
rule's own search has reported a pool size.** Reason: it bears on no title clause,
so it must not consume compute before its own gate has passed. Their decoys fail
the module's own ±20% window on 3–5 of 6 axes and are systematically uncharged
against cationic real ligands.

**The ≥12-cluster threshold is WITHDRAWN.** It was set against the over-counted
ligand panel. The decoy arm can only draw on the ligand-complete set — at most 15
clusters, or 13 without the retinal pair — so ≥12 demanded an 80–92% pass rate from
a rule that all eight of `paper_af3`'s hand-picked decoys would fail. Pre-committing
to it risks building the rule, failing the gate at 9 or 10, and having nothing. Run
the search, report the pool, then pre-register a threshold against what was
observed, with a stated fallback (six-axis rule, or k=2 decoys). For planning only:
**≥10 of 15**.

**D-H — resolve the 9EPP/9EPR reference question rather than dropping B1B1U5.**
Reason: the 1.8% interval penalty is not the issue; dropping it halves the Gq arm
to n = 1, and a panel cannot be called a census with an unresolved member in it.
**→ RESOLVED the same day; see D-2026-09-12-b above. Outcome: option (c′) —
9EPP stays, cognate stays Gq, panel stays 30 / 29, and Rule 4 turns out to be
inapplicable rather than unimplemented.**

---

## D-2026-09-12-c · D-A RESOLVED — the conjunction, one axis calibrated, one inherited and validated

**Aditya, 2026-09-12**, re-decided on correct information after F-1 was retracted.
This supersedes the earlier D-A entry, which was taken on the false premise that
the two-instrument predicate never ran.

**THE DECISION. Class A keeps the conjunction — `NPxxY-OH < 9.08 AND tilt >
14.932` — which is what actually ran. Group 0 calibrates NPxxY and NOT the tilt.
The tilt threshold is inherited from `paper_af3` with its provenance stated, and
validated on the apo/cognate contrast rather than calibrated against any label.**

### Why the tilt is not calibrated

Every ground truth available to Group 0 for that axis is circular or retracted:

| candidate truth | why it fails |
|---|---|
| `state` (GPCRdb) | **the label is defined using this same atom pair**, 2×46–6×37 ≤ 11.9 Å |
| `transducer_type` | the Q0c circularity Aditya retracted; `G0-6` guards its return |
| `activation_degree` | same retraction |
| RMSD to a reference | calibration structures are off-panel and have **no reference pair**; and choosing which reference is "active" is itself a state label |

**My earlier option (c) — "calibrate the tilt against RMSD-nearest-reference" — is
withdrawn. It is circular one step removed**, and I proposed it before checking
that the data existed. It does not.

### What replaces calibration, and why it is stronger

**F-13's apo table validates the threshold without any label entering.** On Class A
the apo arm sits at tilt medians ~12 Å with only **3–15 of 40** cells above 14.932,
while the cognate arm calls **83–94%** active. That separation comes from an
**experimental manipulation — partner present or absent** — so no GPCRdb definition
participates and no circularity is possible.

**We can therefore say the threshold demonstrably separates apo from cognate on
Class A, without claiming to have derived it.** Methods states plainly that we did
not re-derive it because every available reference would have been defined using
the same measurement.

**The cost, stated rather than hidden:** we cannot claim a calibrated tilt.
Claiming a clean calibration we cannot have would be worse.

### Scope — Class A ONLY

F-13 showed the tilt fails outside Class A:

- **Class B** — Boltz and Protenix put apo at ~12 Å, Chai and OF3 at ~20 Å. A **9 Å
  disagreement about the same receptors with no partner.** No pooled Class B rate.
  **Independently confirmed by `paper_af3` 2026-09-12** to the decimal — boltz 12.38
  (1/4 above the cut), protenix 12.53 (1/4), chai 21.47 (3/4), of3 19.60 (4/4) — and
  **the control holds**: Class A apo is well-behaved on all four (medians
  12.12 / 11.94 / 12.78 / 12.36, with 6 / 3 / 15 / 3 of 40 above the cut), so this
  is not a generic threshold artefact.
- **Class F** — apo medians 14.20–16.12 straddle the 14.932 cut on **every**
  backbone. No discriminating power. Confirms the standing gate WAIT: re-measure on
  2×44–6×31 or drop the arm. **Independently confirmed by `paper_af3` 2026-09-12**
  (chai 14.20, boltz 15.09, protenix 16.10, of3 16.12), who add that their own brief
  already carries a standing rule that Class B/F thresholds are
  `descriptive_n_lt_5_per_side` and **must not be quoted as active-call fractions or
  as usable thresholds**. Our measurement is evidence for a constraint the project
  had already written down on geometric grounds.

**So the conjunction is a Class A instrument. B and F are separate decisions and
must not inherit this one.**

### Consequences to carry

- **`excl_npxxy_undefined` is set at DISPATCH from the anchor table, never
  discovered at scoring time.** Under a conjunction a missing NPxxY forces
  "inactive" on every row — which is how EDNRB and GRPR contributed 28% of the
  frozen campaign's errors from 5% of its rows (F-10). The exclusion is an input,
  not an outcome.
- **EDNRB and HRH3** are NPxxY-blind on the frozen panel. They are excluded from
  the binary rate, named in the figure caption, and **kept in every other arm** —
  both continuous axes, ladder geometry, engagement depth, partner pLDDT. Only the
  state call is withheld. **No tilt fallback for them**: calling 2 of 30 receptors
  on a different instrument from the other 28 is the pooled-instrument defect the
  frozen manuscript already carries.
- **The Cα variant is the coverage arm**, applied to all 30 receptors or to none.

---

## D-2026-09-12-d · SCOPE CLOSED — the redo is a Class A paper

**Aditya, 2026-09-12**, asked directly: does the redo claim Class A only, or all
classes? **Answer: Class A only.** This closes `E0.5` at option (a) — "drop B and F
and say the work is Class A" — and it is the scope `D-2026-09-12-c` was already
written against.

### What it ratifies — the artefacts were already there

Verified rather than assumed:

| artefact | composition |
|---|---|
| `g1_receptors.tsv` — the frozen G1 panel | **64 receptors, every one `gclass = A`**, 32 core-32 provisional |
| `g0_calibration_structures.csv` | **1,357 rows, one class present: Class A (Rhodopsin)** |
| its scored split | 965 Active + 371 Inactive = 1,336 → **726 calibration / 610 application**, matching gate G0-2; the 21 excluded rows are the Class A Intermediates |

**So the decision costs the primary campaign nothing.** Both the instrument's
calibration population and the panel it is applied to were already Class A by
construction. What changes is that the scope is now *claimed* rather than
*incidental*, and several open items close because of it.

### What it closes

- **`E0.5` — "decide the class B and class F instrument"** — resolved as option (a).
  It was a decision, never an experiment.
- **The G0 gate's `class F atom pair` WAIT** — "measure class F tilt on 2×44–6×31 or
  drop the class F arm". The arm is dropped; the WAIT is answered by scope, not by
  measurement.
- **The Class B and Class F instrument decisions** carried as Tier 3 open items.
  F-13 is no longer an open problem; it becomes the *stated reason* for the scope.

### Why F-13 is the justification rather than a casualty

The scope is not a convenience — we have measurement behind it, from the apo arm:

- **Class B:** Boltz and Protenix put apo at ~12 Å, Chai and OF3 at ~20 Å — a **9 Å
  disagreement about the same receptors with no partner**, larger than the
  separation the threshold is meant to detect.
- **Class F:** apo medians **14.20–16.12 straddle the 14.932 cut on every
  backbone** — no discriminating power at all.

A paper that says "we restrict to Class A because our instrument demonstrably does
not transfer, and here is the measurement" is stronger than one that reports
B and F rates it cannot defend.

### What it costs — stated, and PARKED rather than deleted

- **`E7.2` — the class B length ladder.** This is the real loss.
  `hilger2020gcgr` on GCGR: in class B the agonist produces no TM6 opening at all,
  so class B is **the sharpest venue for a partner-length ladder** — if the α5-CT
  ladder means what we think, class B should show the *larger* step. lit rated
  cross-class transfer **"ADJACENT on coverage, OPEN as transfer"**: several papers
  span classes, none holds a class out and tests transfer.
- **`G15` / tier `E-B1`** (class B transfer, 5 proposed → 4 receptors) — depended on
  `E0.5` and drops with it.
- **Tier `E-scope`** — the class F/B2 carry-over (AGRE5, FZD4, FZD6, FZD7, SMO),
  already "declared scope, no claim", now formally out. (An earlier version of this
  entry cited SMO as getting *less* open with the partner; **that was OF3-only and
  is retracted** — see F-13(c). The scope decision does not rest on it: its grounds
  are Class B's 9 Å inter-backbone split and Class F's threshold sitting inside the
  apo distribution, **both independently confirmed**.)

**`E7.2` is parked, not killed.** It needs a class B instrument, which needs its own
calibration; that is a second paper's worth of work and it is the obvious follow-on.
Recorded here so the reason it is absent is legible rather than looking like an
oversight.

---

## D-2026-09-12-e · D2 RESOLVED — the split, and two corrections to the option it was chosen from

**Aditya, 2026-09-12: "go with (c) for D2"** — expand onto the actives-rich
expansion receptors, reserve the inactive-rich ones for calibration. The decision
stands. **Two things in the option text it was chosen from are wrong**, and both
change what (c) delivers, so they are recorded before any regeneration.

### Correction 1 — the expansion set is 25 receptors, not 32

Asserted as "the 32 E-scope/E-B1 receptors" in `GROUP0_SYSTEMS.md` at the summary
table (§ *Decisions still with the PI*), in §0.3's body sentence, and in §6.3's
decision table. Counted from `g0_calibration_structures.csv` — `on_panel75` and not
`on_panel48` — it is **25**, of which **20 survive to the F4 pool**. The body
figures underneath were always right and reproduce exactly: **41 of the 61 F4
inactives come from 17 expansion receptors.**

The label is also loose: "E-scope/E-B1" names the class F/B2 and class B1 tiers,
which are **5 receptors each and are now out of scope entirely** under
D-2026-09-12-d. The 25 are Class A receptors on the expanded panel-75 and not on
panel-48. Nothing in the arithmetic depended on the label, but a reader chasing it
would land in the wrong tier.

### Correction 2 — the ranked reserve list was computed on the wrong pool

§6.3 recommends reserving `nk1r 6, oprm 4, ntr1 4, 5ht2a 4, c5ar1 3, acm3 3,
pd2r2 3, ccr2 3, drd4 3`. Recomputed on the **F4 pool** — the population the
calibration is actually fitted on — **`ntr1` and `pd2r2` contribute zero
inactives.** Their inactives (9 and 3 raw) are removed by F0b/F2/F3 before F4.
**Reserving them buys nothing.** The rest of the list reproduces.

### The real shape of the choice: it is a curve, and it has almost no free stretch

**Every one of the 17 expansion receptors that carries an F4 inactive is also a
both-state receptor, and all 17 both-state receptors in the pool are expansion
receptors.** Non-expansion contributes 269 actives, 20 inactives and **zero**
both-state receptors. So "expand onto the actives-rich" has far less room than the
option implies — the actives-rich expansion receptors (`oprm` A=21, `s1pr1` A=15,
`ssr2` A=13) each carry inactives and both-state pairing too.

| receptor | F4 inactives | F4 actives | cumulative inactives lost |
|---|---:|---:|---:|
| `nk1r` | 6 | 6 | 6 |
| `oprm` | 4 | 21 | 10 |
| `5ht2a` | 4 | 4 | 14 |
| `c5ar1` | 3 | 8 | 17 |
| `acm3` | 3 | 4 | 20 |
| `ccr2` | 3 | 1 | 23 |
| `drd4` | 3 | 1 | 26 |
| `s1pr1` | 2 | 15 | 28 |
| `ssr2` | 2 | 13 | 30 |
| `ada1a` | 2 | 3 | 32 |
| `ccr6` | 2 | 1 | 34 |
| `gpr6` | 2 | 1 | 36 |
| `ccr8` | 1 | 5 | 37 |
| `tshr` | 1 | 5 | 38 |
| `hrh2` | 1 | 4 | 39 |
| `oxyr` | 1 | 2 | 40 |
| `s1pr5` | 1 | 1 | 41 |

Every row is a both-state receptor. **Three expansion receptors carry no F4
inactive at all: `cxcr3`, `mtr1a`, `mtr1b`.**

### THE CUT — where (c) lands, and why there

**Expand onto `cxcr3`, `mtr1a` and `mtr1b`. Reserve the other 17.**

This is the only cut that costs the calibration nothing, and it is the faithful
reading of (c) once the pool is corrected:

| | before | after |
|---|---:|---:|
| F4 calibration pool | 433 | **425** |
| inactives | 61 | **61** |
| both-state receptors | 17 | **17** |
| calibration receptors | 106 | 103 |

The price is **8 actives out of 372**, against a 6.1:1 actives-to-inactives ratio —
the abundant class. The inactive pole, which is the binding constraint everywhere in
Group 0, is untouched.

**Stated plainly: (c) buys three panel receptors, not a tier.** The option text
implied a substantial actives-rich expansion, and after the filters that population
does not exist. If more panel breadth is wanted it has to be bought from the table
above at a known price in inactives and in both-state pairs — and the first rung,
`ccr8`/`tshr`/`hrh2`/`oxyr`/`s1pr5`, costs 1 inactive and 1 both-state receptor
each. **That further purchase is not made here.** It is the kind of trade that
should be made against a measured threshold shift, which is what the measurement
pass produces.

### What it implies mechanically — NOT executed

Moving three receptors across the calibration/application line changes
`on_panel48`, which changes the frozen constants three gate checks assert: G0-2's
726/610 split, G0-5's F4 = 433 ladder row, and G0-7's independence ladder. Those are
**deliberate freezes** and updating them is a generator re-run plus a manifest
restamp, not an edit. `redo/inputs/` is code-only and stays that way.

**Held until the measurement pass is authorised**, so the population is frozen once
rather than twice. The decision is recorded; the regeneration is one step of the
pass, not a separate change.

---

## F-14 · The three open coupling reversals are closed — the competing family has no native structure

**CCKAR, EDNRB and GHSR** all carried Block B prior **Gq** against a Rule-R structural
cognate that reads otherwise. They stayed open because most annotation authorities also
say Gq/11, so preferring the structure looked like preferring one source over four.

**It is not.** Enumerating the Gα entity in **every** active structure of each receptor —
not only the chosen reference — and classifying it by the deposition's own description,
its accessions and its length:

| receptor | actives | families present **natively** | Block B's Gq appears as |
|---|---:|---|---|
| CCKAR | 9 | Gs (394, 380, 380), Gi1 (354) | mGsqi chimera ×3, Gi/Gq fusion ×1 — **never native** |
| EDNRB | 10 | **Gi1 only** (354 ×2) | a 246 aa mini with no accession |
| GHSR | 5 | **Gi1 only** (354 ×2) | *"Engineered G-alpha-q"*, the depositors' own word |

**In all three, the family the Rule-R structure reads is the only family with a native,
full-length, non-engineered Gα anywhere in that receptor's active structures.**

**Resolution: CCKAR = Gs, EDNRB = Gi/o, GHSR = Gi/o** — all three unchanged in outcome,
**changed in basis.** Not "the structure beats four authorities", but "the family those
authorities name has no native structural representative, and the one we supply does".
EDNRB carries a second independent ground: Gi/o is the only family compatible with all
five authorities. Full evidence in `COUPLING_REVERSALS.md`; reproduce with
`redo/build/coupling_reversal_evidence.py` → `inputs/coupling_reversal_evidence.tsv`.

**This is the same shape as the Block C "cognate disagreements"** that turned out to sit
in a *secondary* coupling column: what a receptor couples to in an assay and what anyone
has deposited it bound to are different questions. And it aligns the three with the
standing chimera policy — Block B's Gq would have meant a chimeric partner at three of
thirty-two core receptors.

**What I got wrong on the way, recorded because the fix is the finding.** My first
classifier tested only the entity *description* and called four engineered constructs
native — `9BKK`, whose description says *"G(s) subunit alpha isoforms XLas"* while its
**title** says *"Gq chimera (mGsqi)"*, and three mini-G entries of 246–261 residues that
carry no engineering word anywhere. **Length was the discriminator I had left out.** The
classifier now tests description **and** title, family-mixing, and length against the
canonical value read from `seq_constructs.tsv`.

**Limit, stated:** structural availability is a publication artefact — mGsqi exists
because native Gq complexes are hard to resolve. A native Gq–CCKAR structure appearing
later reopens this, and re-running the generator against a newer snapshot is how that
gets noticed.

---

## F-15 · D-C's ligand picks are ENACTED — six of seven, and ADRB1 is blocked by the rule that blocks B1B1U5

**Affinity was the stated blocker and it is gone.** `LIGAND_CURATION_PROPOSAL.md`
ended by saying every row "still needs an affinity attached from a source we pin".
Aditya dissolved that on 2026-09-12 — ligand identity is evidenced *structurally*,
the molecule being co-crystallised in an active or inactive receptor, which is a
stronger claim than an assay number. So the picks became enactable, and they are
enacted: `redo/inputs/ligand_set_redo.tsv`, from `redo/build/ligand_set_redo.py`.

**Six picks across four receptors, four of them sitting ON one of our own reference
structures:**

| receptor | role | ligand | CCD | structure | provenance |
|---|---|---|---|---|---|
| S1PR1 | agonist | siponimod | `J8C` | 7TD4 2.6 Å | our ACTIVE reference |
| S1PR1 | antagonist | W146 | `ML5` | 3V2Y 2.8 Å | our INACTIVE reference |
| HRH3 | agonist | histamine | `HSM` | 8YN5 2.7 Å | our ACTIVE reference |
| GHSR | agonist | ibutamoren | `1KD` | 7NA8 2.7 Å | same deposition as our active ref |
| GHSR | antagonist | CHEMBL1956994 | `8QX` | 6KO5 3.3 Å | our INACTIVE reference |
| CCKAR | agonist | SR146131 | `IA1` | 7XOV 3.0 Å | off-reference, the only candidate |

**ADRB1 is blocked, and the proposal was wrong to list it as straightforward.**
Carazolol is on our own inactive reference `7BVQ` and is human — but GPCRdb types it
**`Inverse agonist`**, not a neutral antagonist, and **amendment C-1 dropped
`inverse_agonist` from Tier 3**. That is exactly what blocks B1B1U5. Every ADRB1
candidate GPCRdb calls a true `Antagonist` — `P32`@4BVN 2.1 Å, `3WC`@3ZPR,
`XF5`@3ZPQ, `I32`@2YCZ — is *Meleagris gallopavo*, against the standing rule that
**species follows the panel** (our ADRB1 is human, P08588). **Reopen C-1 for an
inverse agonist, or accept a cross-species antagonist — Aditya's call.**

**I made that error and a check caught it, not a re-reading.** The generator now
refuses any pick whose assigned role disagrees with GPCRdb's own `function_raw`;
proved by planting carazolol back into the list, where it exits 1.

**Power consequence: k = 12, not 13.** The proposal's own figures follow
`MDE = 1.218/sqrt(k)` — verified against all three of its points (k=8 → 0.431,
k=13 → 0.338, k=15 → 0.314) — so k = 12 gives **MDE ≈ 0.352** against a baseline of
**0.431**. The curation is still clearly worth doing, which is the point that matters.

**A new gate, `redo/gates/ligands.py`, 5 checks, each proved by planting:** the
table is present (a missing table FAILS, never skips); every pick traces to exactly
one candidate row; no role disagrees with its function label; every SMILES parses and
no receptor's two roles share an InChIKey — the OPSD problem, where agonist and
antagonist are one molecule in two isomers; every blocked receptor states its reason
in the table itself. Wired into `verify.sh`.

---

## D-2026-09-12-f · The ligand arm is TIERED, C-1 is relaxed, and one pick was refused

**Aditya, 2026-09-12.** Three instructions, taken together: **T1** is receptors with
both a small-molecule agonist and antagonist; **peptide receptors are kept but
treated separately**; receptors with **a ligand in one state and a peptide in the
other become T3**; **PAM, NAM and antibody/nanobody ligands are skipped
completely**; and **amendment C-1 is relaxed** so an inverse agonist is an
admissible off-state ligand.

### The axis is chain-ness, not the database's type string

A ligand that enters as a **separate polymer chain** is the thing this campaign is
about; a ligand carrying a **CCD code is a HETATM component** and is not a chain,
whatever its `type` says. Exactly **one record in 872** is typed `peptide` and
carries a CCD — EDNRB's `IRL 2500` (`D2U`), a peptidomimetic — and it was the only
thing making EDNRB look like a matched-peptide receptor. Its real antagonists
(bosentan, K-8794) are small molecules, so **EDNRB is T3, not T2.** That also
retires the hazard where endothelin-1, at exactly 21 residues, would have shared a
prediction with `ct21`.

### The tiers, on the frozen primary panel (30 receptors / 29 clusters)

| tier | rule | receptors | clusters | MDE |
|---|---|---:|---:|---:|
| **T1** | both arms chain-free | 17 eligible, **16 curated** | **15** | **0.314** |
| **T2** | both arms a chain | 2 (`C5AR1`, `SSR2`) | 2 | — |
| **T3** | one arm a chain, one not | 7 | 7 | — |
| X | one side has no ligand at all | 4 | 4 | — |

T1 + T2 = 17 clusters (0.295); all three tiers = 24 (0.249). **T2 and T3 are
reported apart and never pooled into T1**; at 2 and 7 clusters neither can carry
the headline contrast, and saying so is the point of tiering them.

### C-1 relaxed unblocked THREE, not two

`ADRB1` and `B1B1U5` were the known cases. **`OPSD` was a C-1 case too** — it has no
plain antagonist either, only an inverse agonist — and its second blocker dissolved
on inspection: its three `RET` records are **three different molecules**, same
skeleton, different stereo layer. `inverse_agonist` is recorded as **its own role**,
never relabelled `neutral_antagonist`.

### The isomer hazard, now demonstrated rather than asserted

**RCSB's canonical `RET` is ALL-TRANS retinal** (`…-OVSJKPMPSA-N`) — the *agonist*
form. Both our inverse-agonist picks are **11-cis** (`…-IOUUIBBYSA-N`). So **any
pipeline resolving `RET` through the CCD silently gets the agonist where the row
says inverse agonist.** F-11's "curate by ISOMER, never by CCD" is now a measurement.
It bites `B1B1U5` as well as `OPSD`, which a within-receptor shared-CCD test misses,
so both rows carry `must_key_by=inchikey` and `ccd_resolves_to_other_isomer`.

### PD2R2 is REFUSED, and this is the finding that justifies the whole check

`PD2R2` is tier-eligible and was never curated by anyone. Enacting it would have
supplied **a membrane lipid as the agonist**: the snapshot's record for `9IYB` reads
`{name: PGD2, type: lipid, function: Agonist, PDB: A1D5Q}` — but **CCD `A1D5Q` is
C43 H81 O13 P, a phosphatidylinositol**, while PGD2 is C20 H32 O5. Two different
molecules in one record, with **no SMILES to arbitrate**. It stays tier-eligible and
uncurated until the deposition itself settles it.

**`redo/build/ligand_ccd_verify.py` rebuilds the check that catches this class** —
the frozen campaign's own gate, whose stated reason was a measured **40–46%
curation-error rate on name-sourced SMILES**. Every CCD-sourced pick is now compared
to RCSB: 10 verified, 2 isomer mismatches flagged, 4 chains n/a. Gate `L-10`.

### What is inherited and cannot be audited here

**9 of T1's 16 curated receptors** — `5HT5A AA1R AA2AR ACM4 CNR2 DRD3 LPAR1 LT4R1
OPRD` — carry ligand rows from `paper_af3`'s `ligand_set.csv` / `ligand_set_tier3.csv`,
**which we do not hold**. Their *tier eligibility* is independently derived here from
the GPCRdb snapshot, but their actual SMILES and roles are not inspectable on our
side. Given what the PD2R2 check just found, **those nine rows are the largest
remaining unverified surface in the ligand arm**, and requesting the two files is
now a substantive ask rather than a tidiness one.

---

## D-2026-09-12-g · Two amendments to D-RULE, and the decoy arm is STILL REFUSED at 11 of 15

**Aditya's decision, 2026-09-12, taken after seeing the rule fail.** That timing is
recorded here deliberately, because it is the only thing that distinguishes a
correction from a fit and it will not be legible from the diff.

### What happened, in order

1. `drule_select.py` was written to implement §5.3 **literally** — no threshold,
   tolerance or k altered — and run. Result: **9 of 16 receptors, 9 of 15 clusters**
   reached k = 3. §5.3's gate is **≥12 clusters**, so the arm was refused.
2. The selector's own report then named two defects *in the rule*, not in the data.
   Aditya approved fixing both and re-running.
3. Re-run with both in force: **11 of 16 receptors, 11 of 15 clusters.**
   **The arm is still refused.** 11 < 12.

### Amendment A — cLogP gets an absolute window, because a percentage of a logarithm is a units error

§5.3 said "every continuous axis within ±20% of the reference's", cLogP included.
cLogP is already a logarithm, so `0.20·|cLogP_ref|` makes the tolerance proportional
to a quantity whose zero point is arbitrary. **Measured on the T1 panel it was
simultaneously too tight and too loose:** ACM4 (iperoxo, cLogP 0.40) got a window
**±0.09**, HRH3 (histamine, −0.09) got **±0.02**, while CCKAR (**±1.58**), S1PR1
(**±1.35**), OPSD (±1.14) and OPRD (±1.11) got windows *wider* than the absolute one
that replaces it. Eleven of sixteen references have |cLogP| > 2.5.

**Enacted: ±1.0 log unit.** MW and TPSA are genuinely proportional quantities and
keep the percentage form.

**It is not a loosening, and this is the number that proves it.** At ±1.0, cLogP
still refuses **81.9%** of eligible candidates — against 84.4% at ±20%, a reduction
of 2.9%. It **redistributed** refusals rather than removing them. And on the
candidates that matter — the **3,679** that pass all seven other axes — cLogP is the
sole refuser of **1,836, i.e. 49.9%**. It halves the otherwise-qualifying set. The
conservation identity closes exactly: 1,843 accepted + 1,836 cLogP-only refusals =
3,679.

**Why ±1.0 and not ±1.5:** ±1.5 adds **zero** clusters while refusing 13% fewer
candidates. A width that buys nothing costs credibility for free.

**Why the sweep is reported as a grid, not a point.** Because the change was made
after seeing a failure, a single post-hoc number is not evidence. Clusters reaching
k = 3, out of 15 (14 is the real ceiling — B1B1U5 can never pass):

| cLogP window | cap 0.30 | cap 0.40 | cap 0.50 | no cap |
|---|---|---|---|---|
| ±20% of \|ref\| *(as pre-registered)* | **9** | 9 | 9 | 9 |
| ±0.5 log | 7 | 7 | 7 | 9 |
| **±1.0 log** *(enacted)* | **11** | 11 | 11 | 11 |
| ±1.5 log | 11 | 11 | 11 | 11 |

**±0.5 is worse than ±20%, and that is the artefact's signature**, not a bug: for
two-thirds of the panel the relative window was already wider than half a log unit.

### Amendment B — the k = 3 decoys must be dissimilar to EACH OTHER

§5.3 capped similarity to the real ligands and said nothing about similarity within
the draw. The first run gave **OPSD two near-identical GPR52 ligands at pairwise
T = 0.641** — same MW to one decimal, same cLogP. §5.3's own justification for k = 3
is that it "converts *is this one molecule odd* into a within-receptor distribution";
two near-duplicates do not do that.

**Enacted: pairwise Morgan Tanimoto < 0.30 among the three drawn decoys** — the same
threshold already applied against the real ligands, so the rule carries one
dissimilarity number and one justification rather than two.

**On this panel the cap costs nothing** — 11 clusters at 0.30, 0.40, 0.50 and
uncapped. Its value is therefore set by **consistency, not by what it buys**, and
that is stated rather than implied. What it changed is *which* molecules are drawn:
worst within-draw similarity on the panel is now **0.274** (CCKAR) against 0.641
before; OPSD is 0.254 and keeps its three.

### Who moved, and the finding inside it

**Gained, both from Amendment A and both predicted in advance:** **5HT5A** 1 → 8
accepted (window ±0.15 → ±1.0) and **ACM4** 1 → 8 (±0.09 → ±1.0). **Lost to
Amendment B: none.**

**Still `decoy-unavailable` (5):**

| receptor | accepted | decisive axis |
|---|---:|---|
| **B1B1U5** | 0 | **no ChEMBL target — eligibility unestablishable** |
| AA1R | 1 | none; no single axis unblocks it (adenosine: MW 267, cLogP −2.0, TPSA 139.5, HBA 9) |
| AA2AR | 0 | MW (dropping it alone → 1) |
| **HRH3** | 0 | **MW** (dropping it alone → 11) |
| LPAR1 | 0 | Tanimoto (→ 1). LPA is charge **−2**, 0 rings, 20 rotatable bonds |

**HRH3 is the cleanest evidence the repair did real work.** Before Amendment A no
single axis unblocked it. After, its blocker is **MW** — histamine is 111.1 Da, a
window of [88.9, 133.4], and a pool of GPCR ligands contains almost nothing that
small. The repair **exposed the next binding constraint rather than dissolving the
gate**. That is what a units fix looks like; a loosening would have unblocked it.

### What this means for the paper, and what must be reported

**The decoy arm does not run.** `g2_systems.csv` is untouched, its 48 decoy cells
stay `BLOCKED_UNRESOLVED_DECOY_POOL`, and G-6 still passes — correct, because
11 < 12.

**Both numbers go in the paper, with the amendments and their dates.** "The
pre-registered rule yielded 9 of 15 clusters; correcting the cLogP window to an
absolute log tolerance and adding a within-draw dissimilarity cap yielded 11; the
pre-registered threshold of 12 was not met and the arm was not run." Reporting only
the 11 would hide a decision; reporting only the 9 would hide a real defect in our
own rule.

**Three things that are now known and were not:**

1. **≥12 of 15 was probably never attainable.** B1B1U5 is unresolvable in ChEMBL by
   construction, so the gate is really **≥12 of 14 — 86% of the panel** must yield
   three property-matched, charge-matched, mutually dissimilar non-binders.
2. **"Decoy" cannot be worded as "non-binder."** The pool is `within_panel`, so every
   accepted decoy is a **known active at some other panel GPCR** — and in 6 of the
   first 27 cases at another receptor *in this same arm* (all three of LT4R1's were
   S1PR1 ligands). Legal under §5.3 and arguably better science, but the Methods may
   say only **"no measured activity at this receptor or its paralog cluster."**
3. **The arm was never on the critical path.** §5.3's standing recommendation was to
   hold it back regardless: title clause 2 is *"the agonist alone does not drive the
   active state"*, which is answered by **agonist vs. no-ligand at fixed partner
   condition**, not by agonist vs. decoy. The refusal costs the paper a referee's
   answer, not a claim.

### Where it is enforced

`gates/drule.py` is **16 checks, 16 proved by planting** — including **D-15** (every
row records the enacted cLogP window and diversity cap, and D-12 recomputes against
*the window the row records*, not the module's current default) and **D-16** (the k
decoys are mutually dissimilar, recomputed from SMILES; its plant makes two of a draw
the same molecule). `drule_select.py --selftest` is **23/23**.

**The 86 MB rejection table is now `drule_rejections.tsv.gz`, 6.8 MB, 1,719,908
rows**, and `.gz` is admitted to `inputs/` by a narrow amendment to `layout.py`'s
`KINDS` — `.bz2` and `.zip` are still refused, and L2's plant was re-proved (7/7).
Determinism is by construction, not by assertion: the member is written with
**MTIME = 0 and no FNAME field** (verified in the header bytes), so two generator
runs produce byte-identical output and `manifest.py --check` passes without a
restamp.

---

## D-2026-09-12-h · The decoy arm RUNS at k = 11, as an EXPLORATORY arm — a declared deviation from the pre-registered ≥12

**Aditya's decision, 2026-09-12, after D-2026-09-12-g returned 11 of 15.** This is an
explicit, recorded deviation from a pre-registered threshold. It is not a threshold
modification: **the bar stays at 12, the arm is not claimed to have met it, and it is
labelled exploratory in the data as well as in the prose.**

### Why the deviation is small, with the arithmetic so a reader need not trust us

The ≥12 bar was never a cliff. It was chosen to guarantee a Minimum Detectable Effect,
and the MDE is

> **MDE = 1.218 / √k**

which reproduces this campaign's own recorded figures exactly — `GROUP2_LIGANDS.md:59`
gives **0.314 at k = 15** and `:211` gives **0.352 at k = 12**:

| k (paralog clusters) | MDE | vs the k = 12 target |
|---:|---:|---|
| 16 | 0.3045 | — |
| 15 | 0.3145 | *the figure at §6's full T1* |
| **12** | **0.3516** | **the pre-registered bar** |
| **11** | **0.3672** | **+4.4% — what we are accepting** |
| 9 | 0.4060 | +15.5% — the first run, correctly refused |

**The cost of running at 11 instead of 12 is a 4.4% loss of sensitivity.** That is the
whole penalty. For comparison, the arm costs **396 predictions pooled** (2,112
per-cell) — 0.3% of the four-block campaign.

**Both of the alternatives were worse, and both were declined on the record:**

- **Turning a third knob.** Two amendments have already been made to D-RULE *after*
  watching it fail (D-2026-09-12-g). A third change following a third failure is
  indistinguishable from fitting the rule to the outcome, however principled the
  argument for it. **Declined.**
- **Widening the candidate pool from `within_panel` to `anywhere`.** This is the one
  scientifically honest escape hatch and it is left on the shelf, pre-registered, in
  case a referee demands confirmatory status. It was declined *now* for three reasons.
  (i) It costs a ChEMBL re-download — the 28 GB database was deleted 2026-09-12 and the
  pool table is stamped `within_panel`. (ii) It **weakens the control**: a
  `within_panel` decoy is a demonstrated GPCR binder that does not bind *this*
  receptor; an `anywhere` decoy need not be GPCR-like at all. (iii) **It probably would
  not rescue the receptors that failed.** HRH3's blocker is MW — histamine is 111.1 Da
  with a window of [88.9, 133.4] — and the smaller and more generic a molecule is, the
  more "no activity recorded" means *never assayed* rather than *inactive*. The decoy
  label gets weaker exactly where the chemistry gets more extreme.
  **If it is ever taken, the exclusion side must widen in the same change**: our
  "no activity at the receptor or its paralog cluster" test is defined on *our panel's*
  clusters, so a wider inclusion pool admits binders of close relatives outside the
  panel — a serotonin ligand at 5HT1A becoming a candidate decoy for 5HT5A. That is a
  false-negative decoy label of the same class as the B1B1U5 trap.

### Four other routes considered and declined, with reasons

Recorded because each is plausible, each was proposed, and the reason for declining is
the useful part.

1. **DUD-E / LIT-PCBA as a decoy source.** Declined as a *source*: DUD-E decoys are
   drawn from ZINC and carry **no measured activity at all** — they are *presumed*
   inactive by property matching plus topological dissimilarity. D-RULE requires ≥1
   **measured** activity at an unrelated target, so adopting DUD-E would **lower** our
   evidential standard, not raise it, and its GPCR coverage is a handful of targets
   rather than our missing five. **Kept as a citation**: DUD-E is the peer-reviewed
   precedent for matching on these property axes and justifies our axis choice.
   LIT-PCBA is evidentially stronger (measured inactives from dose-response assays) but
   is ~15 targets; whether any of ours is among them is unchecked and worth 20 minutes,
   not a path.
2. **Structural isomers or stereoisomers of the true agonist.** Declined. An isomer is
   not *rendered* a non-binder by being an isomer — many isomers are active, and this
   campaign's own **F-11** is specifically about retinal isomers behaving differently,
   with `ccd_resolves_to_other_isomer` carried as a curation column for exactly that
   reason. A synthesised isomer also has no activity data by construction, so it fails
   requirement (iii) outright: we would be **asserting** inactivity. That is precisely
   the frozen campaign's defect — a prose "no known activity here" argument that no
   code checked (`MAP_LIGANDS_AND_ANALYSIS.md` §2).
3. **De novo / generatively designed decoys.** Declined, and most firmly. A generated
   molecule has zero activity data, so it is an *assumed* non-binder — strictly worse
   than the frozen campaign, which at least used molecules that had been assayed against
   something. Worse, **it introduces a confound that maps precisely onto our own
   result**: these models are sensitive to whether a chemotype is in their training
   distribution, so a synthetic SMILES never seen in the PDB or ChEMBL may place badly
   *because it is novel*, and we would read that as the model discriminating binders
   from non-binders. We would have manufactured our own positive result.
4. **Lowering the bar to 11 and calling the arm confirmatory.** Declined. The bar stays
   at 12. What changes is the arm's *status*, not the threshold.

### What must be true in the paper

1. **All three numbers are reported, with dates**: the rule as pre-registered gave
   **9 of 15** clusters; the two amendments of D-2026-09-12-g gave **11**; the
   pre-registered bar was **12** and was not met.
2. **The arm is exploratory and says so**, with `k = 11` and `MDE = 0.367` stated
   against the 0.352 targeted. No headline or confirmatory claim rests on it.
3. **The 5-receptor refusal is reported as a methodological finding in its own right**
   — see F-19. It does not depend on the arm running and is the more durable result.
4. **"Non-binder" may not be used.** The pool is `within_panel`, so every accepted decoy
   is a known active at some other panel GPCR, and in several cases at another receptor
   *in this same arm* — **all three of LT4R1's decoys are S1PR1 ligands**, CCKAR's
   `CHEMBL4279831` is a CNR1/CNR2 ligand, OPRD's `CHEMBL5915578` is an ACM4 ligand. Legal
   under §5.3 and arguably the better negative, but the Methods may say only **"no
   measured activity at this receptor or its paralog cluster."**
5. **The surviving 11 are a BIASED subset, and the MDE does not capture it.** This is the
   most important caveat on the arm and it was nearly missed, because k counts clusters
   and says nothing about *which* clusters. The five refused receptors are the small and
   polar end of the panel — histamine (111 Da), adenosine and NECA — plus a dianionic
   lipid (LPA) and the spider opsin. **So the 11 that survive are systematically the
   lipophilic, drug-like end**, and the ligand-class contrast is therefore evaluated on a
   narrower chemical space than the agonist arm it is compared against. The bias is a
   *consequence of the rule working*: D-RULE refuses exactly where matched chemistry is
   unreachable, so the arm's coverage is correlated with its own admission criterion.
   **One sentence stating this belongs wherever the arm is reported**, and it is not
   discharged by quoting MDE 0.367.

### FROZEN 2026-09-12 — the arm is locked

**Aditya locked the decoy plan as it stands.** Frozen means asserted by a gate that
fails when it changes and proved by planting — not a banner. The frozen object is the
**selection**, because `g2_preflight` re-derives dispatch from `drule_selected.tsv`, so
pinning the selection pins the arm.

| frozen | value |
|---|---|
| release | **ChEMBL_37**, sha256 `33c20374…`, scope `within_panel` |
| rule | cLogP window `absolute:1.0`, diversity cap `0.30`, `k = 3`, draw seed `20260912` |
| accepted | **11 receptors / 11 clusters** — `5HT5A ACM4 ADRB1 CCKAR CNR2 DRD3 GHSR LT4R1 OPRD OPSD S1PR1` |
| refused | **5** — `AA1R AA2AR HRH3 LPAR1` as `fewer_than_k_accepted`, **B1B1U5 separately** as `eligibility_unestablishable_no_chembl_target` |
| molecules | **33, all distinct across receptors**; ChEMBL-id set sha256 `9d363f1f…`, InChIKey set sha256 `a694022d…` |
| dispatch | 33 READY / 15 BLOCKED, **396 pooled / 2,112 per-cell** |
| power | `MDE = 1.218/√k` **recomputed from the observed cluster count**, not stored — 0.367 at k = 11 |

**THREE digests, not two, and the third exists because my first plant proved nothing.**
I specified the assignment plant as "permute one receptor's three molecules onto
another's" and it is **completely inert**: both digests are over *sorted* values, so
permuting which receptor a molecule is scored against leaves them byte-identical and moves
no count. **The same 33 molecules against the wrong reference ligands would have passed the
entire freeze.** Closed by a third digest over the sorted `receptor:molecule` **pairs**
(`e60eb91c…`), whose plant is that permutation. The three do three different jobs:

| digest | catches |
|---|---|
| ChEMBL-id set `9d363f1f…` | a different molecule drawn |
| InChIKey set `a694022d…` | the chemistry moved under a stable accession |
| **assignment pairs `e60eb91c…`** | **the right molecules against the wrong receptors** |

It surfaced only because the harness *runs* its plants instead of asserting they work —
the same reason `g0_preflight`'s dead harness was found. **Every count above survives a
re-run that silently draws or misassigns a molecule; the digests do not.**

**Prediction totals are deliberately NOT frozen, and that is a choice rather than an
omission.** 132 of the 396 pooled predictions are `G6fd(option)` at `R7_full`, behind an
**open** `pi_choice` on the cognate rung, and `n = 10/50` is a separate open decision. So
the freeze pins the **cell counts** — 33 READY / 15 BLOCKED, a property of the selection —
and leaves the totals to `g2_preflight` G-10, which re-derives them from backbones × n.
Freezing them would make this gate fire on decisions Aditya is entitled to take: friction
dressed as safety.

**Known behaviour, recorded so it is not mistaken for a fault: a ChEMBL_38 bump will fire
NINE freeze checks at once**, because a new release changes the pool, the eligibility sets
and therefore the draw. That is correct, but it presents as a broken gate rather than one
decision. If a release bump is coming, the first move is to key the outcome checks off a
single `release_epoch` so it fails once, with one message. And **the MDE is recomputed, never typed**, so if the accepted set ever changes the
power assertion moves with it and fails rather than going quietly stale — which is what
happened to four counts on this project already
(see `[[a-header-count-is-a-claim-nobody-checks]]`).

**B1B1U5's refusal class is frozen separately from the other four on purpose.** Its
eligibility was never establishable — no ChEMBL target, therefore no exclusion rows,
therefore a naive implementation calls all 120,973 molecules eligible for it. Flattening
it into `fewer_than_k_accepted` would hide the one failure mode that is a *hole in the
evidence* rather than a fact about chemistry.

**What the freeze does NOT forbid.** Changing any of it is allowed — by changing the
decision first. The freeze exists so that a third amendment to the chemistry, or a
re-run under different parameters, cannot happen *silently* after two amendments already
have. A gate failure here is not a broken gate; it means the decision record and the
data have diverged, and the record is what gets updated first.

### Where it is enforced

The exploratory status is carried in `g2_systems.csv` on every decoy row, not only in
prose, so the arm cannot be read downstream as confirmatory by accident. `g2_preflight`'s
G-6 was rewritten: it previously asserted that *every* decoy cell is unresolved, which is
now false, and it **re-derives the resolved and refused sets from `drule_selected.tsv`**
rather than asserting a constant — failing in both directions, so a decoy appearing for a
refused receptor and a passing receptor's arm going missing each trip it.

---

## F-19 · A property-matched decoy does not exist for a third of a Class A panel — and the frozen decoy arm was therefore not a controlled negative

**This is the durable result of the decoy work, and it does not depend on the arm
running.** Written for the Methods/SI.

### The finding

Applying D-RULE (`CAMPAIGN.md` §5.3, as amended) to 120,973 candidate molecules from a
hash-pinned release — **ChEMBL_37**, sha256 `33c20374…` — **five of sixteen Class A
GPCRs admit no set of three property-matched, charge-matched, topologically dissimilar
decoys at all:**

| receptor | reference agonist | eligible candidates | accepted | the axis that refuses |
|---|---|---:|---:|---|
| **B1B1U5** | — | 0 | 0 | **no ChEMBL target; eligibility unestablishable** |
| AA1R | adenosine | 111,240 | 1 | none singly — MW 267, cLogP −2.0, TPSA 139.5, HBA 9 |
| AA2AR | — | 111,240 | 0 | MW |
| **HRH3** | histamine | 114,172 | 0 | **MW — 111.1 Da, window [88.9, 133.4]** |
| LPAR1 | LPA | 120,207 | 0 | Tanimoto; charge **−2**, 0 rings, 20 rotatable bonds |

**The refusals are chemistry, not curation.** They concentrate on receptors whose native
agonist is chemically extreme — a 111 Da biogenic amine, a doubly-anionic lipid, a
polar nucleoside — and a pool of GPCR-active molecules contains almost nothing that
small, that charged, or that polar. **This is a statement about the reachable limits of
property-matched decoy design on GPCRs, and we have not found it stated anywhere.**

### Why it bears on the frozen campaign's result

The frozen arm's decoys were 8 hand-picked FDA-approved drugs in a hard-coded Python
dict, gated only on Morgan Tanimoto < 0.30. Its ±20% property window across six axes was
**computed and never enforced** — no branch raises — and **all 8 miss the window on three
to five of the six axes**. Its own source carries the reason as a comment:
*"Formal-charge mismatch is reported not raised (Decision A — aminergic +1 anchors force
neutral decoys)"* — so across the aminergic panel the decoy arm differs from the ligand
arms **systematically in net charge**, and nothing downstream corrects or stratifies for
it. See `MAP_LIGANDS_AND_ANALYSIS.md` §2.2–§2.4.

**Consequence for a result we hold.** On `rows.tier3.v2.csv` the decoy is
indistinguishable from the antagonist on every backbone — **+0.011, −0.004, −0.016,
−0.004**. That admitted two readings: the models are indifferent to pocket occupancy, or
the decoys were never decoy-like. **F-19 is evidence for the second.** The decoys were
off-window on most axes and systematically mischarged, and a properly-constructed decoy
is provably unavailable for a third of the panel.

**So the Block C decoy result must be re-scoped from a claim about the predictors to a
finding about the decoy set.** That is a withdrawal, and it is the kind that makes the
surrounding claims more believable rather than less — the partner effect on the same
rows survives per backbone (agonist apo→cognate 0.094→0.806, 0.259→0.634, 0.166→0.738,
0.052→0.879) and is untouched by it.

### The three sentences this earns

Stated here so they are written once and not re-derived:

1. *A decoy rule requiring measured activity at an unrelated target, matched molecular
   properties on eight axes, equal formal charge at pH 7.4 and topological dissimilarity
   from every ligand of the receptor and its paralog cluster admits no viable decoy set
   for 5 of 16 Class A GPCRs, including the histamine H3 and LPA₁ receptors.*
2. *The limit is set by the native agonist's chemistry, not by curation effort: the
   failures are the receptors whose agonists are smallest, most charged or most polar.*
3. *A decoy arm built by hand-picking approved drugs, as in the frozen campaign, does not
   meet this standard on any of its 8 receptors — all 8 miss their own stated ±20%
   property window on three to five of six axes and are uncharged where the reference
   ligands are cationic — so its agonist-versus-decoy contrast is not a controlled
   comparison for pocket occupancy.*

**What this finding does NOT claim.** It does not say decoys are impossible — widening
the pool beyond panel GPCRs would change the answer, and D-2026-09-12-h records why that
was declined. It says that under a stated, pre-registered rule on a pinned release, the
`within_panel` pool cannot supply them for a third of this panel, and it names the axis
that refuses in each case.

---

## D-OPEN-2026-09-12-j · Chain A's construct rule was never decided, and the built artefact silently enacts the option the spec calls indefensible

**OPEN. Aditya's decision. Recorded here because it was invisible in this file, which
is how it went un-taken for a day while everything downstream said `PENDING` and nobody
read the PENDING as a question.**

### What I got wrong, on 2026-09-12

I told Aditya that `chain_a_source = PENDING:SEQ_RECEPTORS.md` on all 2,039 Group 1 and
350 Group 2 rows was **a stale label** — that `seqrec_*.tsv` had since landed covering
64 of 64 receptors, so the generator simply needed rewiring, no decision required.

**That was wrong.** `SEQ_RECEPTORS.md` §3.1 states it plainly: *"it is a recommendation
and not a decision … the choice belongs to the PI."* The sequences exist; **which
sequence to supply does not.**

### And the built artefact is currently option (c)

§3.1 costs three options and names (c) — applying §4's terminal cap with no separate
signal-peptide rule — as *"the worst option and the numbers say so"*. **That is what
`seqrec_trimmed.fasta` currently is.** Measured from `seqrec_trim.tsv`:

| receptor | signal | trim_start | signal residues surviving |
|---|---|---:|---|
| **5HT2C** | 1–32 | 4 | **29 of 32** |
| **EDNRA** | 1–20 | 20 | **1 of 20** |
| EDNRB | 1–26 | 41 | 0 |
| FSHR | 1–17 | 312 | 0 |
| LSHR | 1–26 | 309 | 0 |
| TSHR | 1–20 | 364 | 0 |

Four clean; **two left as fragments.** The spec's own words: *a fragment of a signal
peptide is neither the leader nor its absence; it is an artefact of an unrelated rule.*

**So wiring `chain_a_source` at the built fasta — exactly what I proposed doing — would
have enacted the indefensible option across 2,389 rows with no decision recorded
anywhere.** The PENDING label was doing real work and I read it as drift. This is the
inverse of the failure class I have been chasing all day: not a stale label mistaken for
a live guard, but **a live guard mistaken for a stale label.** Both are cured the same
way — read what the label points at before believing it.

### The decision

| option | supplies | cost | risk |
|---|---|---|---|
| **(a) full canonical** | 1–L | zero; continues Blocks A–D | ~20–32 residues of hydrophobic leader in no reference structure; on TSHR it precedes a 394-residue ectodomain |
| **(b) remove the annotated signal peptide, BEFORE the cap** — *the spec's recommendation* | `CHAIN` start–L | one line; hashes already computed in `seqrec_receptors.tsv:mature_sha256`; six core sequences change | four of the six boundaries are **predicted**, not observed — removing a predicted boundary is a judgement dressed as data |
| **(c) status quo** | cap only | zero | **the two fragments above. Not defensible, per the spec.** |

**Required either way, and independent of which is chosen:** record
`signal_peptide_removed ∈ {true,false}` **per row**. No block has ever carried it and
**the question cannot be answered afterwards from a length.**

### Until it is taken

`chain_a_source` stays `PENDING:SEQ_RECEPTORS.md` and **nothing in Group 1 or Group 2
dispatches.** That is correct behaviour, not a bug, and this entry exists so the next
session reads the PENDING as a question rather than as rot.

---
## D-2026-09-12-i · The campaign has a plan of record, and ONE adaptive parameter with a pre-registered rule

**Aditya, 2026-09-12.** The ordering lives in `redo/spec/PLAN.md` — five pillars, free
work first, and every pillar a stopping point that buys a complete sentence. `PLAN.md`
sequences; it does not decide, and where it ever disagrees with an enumerating spec or
with `inputs/`, **those win**.

### The decision recorded here

He asked whether the partner condition used in the ligand arm can be informed by what
the many-combination arms (cognate, shuffled, varying length, mutants) find. **It can,
and the mechanism is a rule committed before the data exists.**

**NOT adaptive — the cognate identity.** `coupling_cognate_map.tsv` stays frozen. It was
frozen for a reason unrelated to outcomes: **the supplied peptide and the scoring
reference must be the same molecule.** Re-picking the cognate on which assignment agrees
better destroys that guarantee, and the arm stops measuring what it exists to measure.

**NOT adaptive — the matched nulls.** Scrambled α5, poly-alanine, α5-deleted and the
unrelated-bulk control run at **whatever rung the real peptide runs at**. A null and its
treatment at different rungs is an uninterpretable comparison, and it is precisely the
failure an adaptive design produces by accident.

**ADAPTIVE — the cognate rung for the ligand crossing, and only that.** It is already
open: all 64 relevant rows of `g2_systems.csv` carry
`pi_choice = "cognate rung for the ligand crossing: R3_ct21 | R7_full | both"`.

> **The rule.** The ligand crossing runs at the **shortest** rung whose pooled
> apo→cognate shift, measured on the Group 1 ladder, falls inside the interior band
> **`[PI: lower]`–`[PI: upper]`**. Ties break toward the shorter construct. A rung is
> excluded **on feasibility** — never on effect size — if any backbone cannot represent
> it natively, or if Option Z shows its partner alignment is single-sequence in practice
> at that rung.

**Why a band and not a maximum, and this is the whole point.** The criterion must
reference **headroom** — a property of the measurement — and never **effect size**, a
property of the result. Choosing the rung with the largest shift would select the
partner condition that maximises our own effect: the identical error to tuning an MSA
masking rate on our own panel, or to amending a decoy rule until it clears its own
cluster bar. Both were declined this same day, and this is the third instance of the
pattern.

Headroom is also the binding constraint in fact, not just in principle: **apo sits at
0.158 and cognate at 0.891**, both pinned, so an interaction estimated at either endpoint
has nowhere to move. `CATALOGUE.md` already advises the middle rungs for that reason.

**`[PI]` OUTSTANDING — the band is Aditya's and must be recorded here WITH ITS DATE
BEFORE any ladder result exists.** A band written afterwards is not a pre-registration,
whatever it says. Roughly 0.25–0.75 is the shape; the number is his.

**Enforcement, once the band is set:** a gate check asserts the enacted rung equals the
rule applied to the Group 1 results, so the adaptation cannot drift silently — the same
treatment `drule.py` gives the frozen decoy selection.

---
## F-16 · The ladder's length/taxonomy confound is MUCH weaker than I said — three revisions, each downward

**I over-called this, and it took two corrections from outside to get it right.**
Recorded in full because the pattern matters more than the conclusion.

**What I first claimed (2026-09-12):** our length ladder has rungs at 11 and 15
below AF3's 16-residue peptide line and 17/19/21 above it; `mazzoni2000gsctpeptide`
puts a wet-lab activity threshold at ≥17; therefore a length effect in that region
is confounded between biophysics and modelling taxonomy, and the ladder cannot
separate them.

**Revision 1 — the wet-lab threshold is contested.** The abstract's "shorter
peptides were not effective" sits beside its adenylyl-cyclase sentence and may
attach to signalling, not binding. A 2011 review enumerates the full panel the
abstract omits — 11, 13, 15, 17, 19, 21 — and reports **all six stimulate specific
binding**, the 11-mer merely *less active*. The proposed mechanism is **helicity**,
which is graded: the 11-mer and the 21-mer both form helices of different lengths.
**So there may be no clean biophysical cut at 17 at all, and we must not
pre-register the 11-mer as inactive.**

**Revision 2 — AF3's 16 is a benchmark filter, not an architectural limit.**
Peptides are in AF3's accuracy and calibration numbers; they are excluded only from
the **low-homology generalization subset**. And the backbones disagree: AF3 16,
Chai-1 **9 and keeps them**, Boltz-2 none, Protenix v1 inherits AF3's, OpenFold3 no
published rule.

**Revision 3 — `paper_af3` grepped the OpenFold3 package, and there is no
length line at inference at all.** No `length < 9|16|20|30` branch anywhere in the
package. Chain type is **declared by the caller** — `inference_query_format.py:51`,
`molecule_type` as a validated enum per chain — so *a chain declared protein is
treated as protein regardless of residue count*. The only peptide-specific logic is
`core/data/primitives/caches/clustering.py:172-199`, which implements AF3 SI 2.5.3
**training-set clustering**, not inference.

**Where that leaves it.** Every line we found — AF3's 16, Chai's 9, Protenix's
inherited 16 — governs **training or evaluation set construction**. None of them
reclassifies a chain at runtime. **So there is no mechanism by which a 15-mer is
processed differently from a 17-mer at inference, and the confound as I stated it
does not exist.**

**What survives, and it is real but different:** short chains were **clustered
differently in training** (100% identity for peptides) and are **absent from
published generalization evidence**. That is a memorization-risk question, not a
step-in-the-length-response question. `paper_af3`'s own caveat is the right one:
they can speak to the inference code path, not to what the weights learned.

**Consequence for the design:** do not build a 16-mer rung to resolve a taxonomy
boundary — there is no boundary to resolve. The four-backbone comparison remains
worth doing on its own merits, and the 13/17/18/19 constructs we already hold remain
useful for resolving a *graded* response, which is what the corrected reading of
Mazzoni actually predicts.

---

## F-17 · The threshold derivation is ANSWERED — and it reproduces to within 1%

**The load-bearing hole in `MAP_FROZEN_CAMPAIGN.md` is filled.** That document's
first stated hole was: *we can say that calls change under a new cut and by how
much, never why 9.08 sits where it does.* `paper_af3` answered it in prose on
2026-09-12, without needing to send the script.

**The rule is `midpoint(active_mean, inactive_mean)`. Nothing more elaborate.**

- fitted on the **32-receptor Class A panel**
- input `refs/reference_set.csv`, keyed on `receptor_slug` + `role ∈ {active, inactive}`
- reading three fields: `d_gpcrdb_tm6_tilt_ref`, `angle_class_b_kink_ref`, `d_npxxy_oh_ref`
- **aggregation: mean of PDBs per receptor per role FIRST, then mean across
  receptors** — explicitly so a receptor with two deposited PDBs does not
  double-weight the aggregate
- directions: tilt `active_gt`, kink `active_lt` (smaller angle = bent TM6 =
  active), NPxxY-OH `active_lt`

### Reproduced here, on the reference set we hold

`redo/protocol/received/source_bundle/refs/reference_set.csv`, 168 rows, applying
their aggregation exactly:

| metric | active mean | inactive mean | midpoint | published | gap |
|---|---:|---:|---:|---:|---:|
| NPxxY-OH | 5.520 (n=30) | 12.830 (n=35) | **9.175** | 9.08 | 1.0% |
| TM6 tilt | 17.872 (n=90) | 12.427 (n=65) | **15.149** | 14.932 | 1.5% |
| class B kink | 158.587 | 157.311 | 157.949 | 159.95 | 1.3% |

**This is corroboration, not exact reproduction, and the residual is the
population rather than the rule.** They fitted on the 32-receptor Class A panel;
the file we hold carries no `gpcr_class` column, so the numbers above are over
**all 168 rows, all classes**. Landing within 1–1.5% on the wrong population is
what a correct rule on a superset looks like. **Do not quote 9.175 as a
reproduction of 9.08** — quote the rule, and say the exact fit needs the panel
identity.

### The part that matters for D-2026-09-12-d

**Their own script's docstring says re-using Class A thresholds for Class B and F
IS SATURATION, and names it** — Class B median apo tilt 22.05 Å against a 14.932
cut; Class F tilt-only, so nearly always true. It carries a self-classification
gate: **if accuracy on the derivation set falls below 3/4 for a metric, that metric
is reported DESCRIPTIVELY rather than as a usable threshold**, because n=4 is too
small to defend — *"reporting saturated 4/4/4/4 numbers dressed as unanimous is the
anti-pattern this exists to prevent."*

That is the origin of the `descriptive_n_lt_5_per_side` rule, and it means **their
tooling had already diagnosed the Class F problem we measured from the apo arm.**
Third independent route to the same place, after our apo measurements and their
`PREREG.md:183` transducer-taxonomy argument. The Class A-only scope is now
supported from three directions.

### Status of the four asks, 2026-09-12

**Aditya approved all four in their session.** Delivery is blocked separately:
their platform's classifier is currently refusing **every** outbound file
regardless of size — `ligand_set.csv` at 33 KB was denied like the large one. The
approval is real; the delivery is not. **Do not look for a way around their
classifier**; the small files are expected to come from Aditya directly instead.

**Ask 1 is too big for the bridge in any case.** `rows.tier3.v2.csv` is **92 MB,
40,801 rows, ~100 columns**; `sendfile.sh` refuses above 14 MB and ntfy caps at 15,
and chunking 92 MB across a relay whose attachments expire in 3 hours is not a
delivery mechanism. **The agreed form is a ten-column projection** — smaller
because it contains less, not because it was sliced to fit:

`receptor_slug · receptor_class · input_state_claim · ligand_type · ligand_role ·
seed_used · confidence_flag · d_npxxy_y558_y753_oh · d_gpcrdb_tm6_tilt_246_637_ca ·
input_path`

**`ligand_type` is in that list**, which is exactly the modality column the ligand
arm needs (D-2026-09-12-f).

---

## F-18 · The approved files landed by hand — what they settle, and one malformed row

**Arrived 2026-09-12 as `paper6f_approved_2026_09_12.zip`** (sha256 `7bafbbc9…`),
by hand because `paper_af3`'s classifier refused every outbound file after Aditya
approved all four asks. Landed read-only at
`redo/protocol/received/approved_2026_09_12/` with `SHA256SUMS`. **Nobody looked
for a way around that classifier.**

Counts match their description exactly: `ligand_set.csv` **40 rows**,
`ligand_set_tier3.csv` **64**. `reference_set.csv` is **byte-identical** to the copy
we already held — which confirms our copy is the threshold fit input.

### Ask 2 is ANSWERED and the nine inherited receptors verify

**All nine T1 receptors we inherit — `5HT5A AA1R AA2AR ACM4 CNR2 DRD3 LPAR1 LT4R1
OPRD` — carry both roles, `is_peptide=FALSE`, with non-empty SMILES.** So the tier
eligibility we derived independently from the GPCRdb snapshot is confirmed against
their actual curation. That was the point of the ask and it holds.

*(My first run said all nine FAILED. `is_peptide` is `FALSE`/`TRUE` in upper case
and my test matched `'false'`. My checker, not their data.)*

### Ask 4 is HALF answered — the rule is confirmed, the fit set is still not

The script's own docstring states the prose answer verbatim: Class A thresholds
*"derived from the 32-receptor Class A panel by midpoint(active_mean,
inactive_mean)"*, mean of PDBs per receptor per role first, tilt `active_gt`, kink
`active_lt`, NPxxY-OH `active_lt`.

**But it does not derive them.** There is no `CLASS_A_SLUGS` in the file — only
`CLASS_B_SLUGS = {GLP1R, GCGR, PTH1R, CRHR1}` and `CLASS_F_SLUGS = {SMO, FZD4,
FZD6, FZD7}`. **So 9.08 and 14.932 remain unreproducible exactly**, and the
fit-set half of `MAP_FROZEN_CAMPAIGN.md`'s first hole stays open.

### Running it produces something worth having

| metric | derived from its OWN class | applied in the campaign | gap |
|---|---:|---:|---:|
| Class B tilt | 17.781 Å | 14.932 Å | 2.85 Å |
| **Class B kink** | **124.240°** | **159.95°** | **35.7°** |
| Class F tilt | 15.802 Å | 14.932 Å | 0.87 Å |

**The applied Class B kink threshold is 36° away from what the Class B reference
pairs themselves imply.** That is far worse than "saturation" conveys, and it is now
reproducible on our side rather than asserted.

**And Class F does not rescue itself.** Even its own correctly-derived threshold,
15.802, sits **inside** the apo distribution we measured (medians 14.20–16.12). So
the Class F axis fails on its own terms, not merely on borrowed ones —
**a fourth independent route to D-2026-09-12-d.**

**Do not quote the 8/8 self-accuracy as validation.** A midpoint fitted on 4+4
points and then tested on those same 8 is guaranteed to score well; it is fitting,
not evidence. Their docstring says the same thing in different words.

### One malformed row in 104

`ligand_set_tier3.csv` line 47, **`LPAR1 full_agonist`**: an unescaped comma inside
`protonation_ph74_note` (*"pKa1 ~1, pKa2 ~7"*) splits the field and **shifts every
column after it by two**. The result is that `ccd_code` holds prose, `ccd_smiles`
holds `NKP` (the actual CCD), and `smiles_source` holds the SMILES.

**The chemistry is unaffected** — `smiles`, `inchi` and `is_peptide` all sit in the
right columns, so LPAR1's T1 status stands. **The provenance is not**: LPAR1's CCD
cannot be verified against RCSB from this file, because the field that should name
it contains a sentence. One row of 104, and it is the only one.

---

## F-1 · **RETRACTED 2026-09-12. I was wrong. The two-instrument predicate IS what ran.**

**What I claimed** (and told Aditya, and told `paper_af3`): that the manuscript's
two-instrument conjunction — NPxxY-OH < 9.08 **AND** TM6 tilt > 14.932 — describes
a predicate that never scored a row, because `switch_signal.py::MotifThresholds`
holds a single metric with `K_OF_N = 1`.

**What Block A's own 9,490 rows say**, reconstructed from the raw metrics and the
per-row thresholds:

| class | n | rule that reproduces `active` |
|---|---:|---|
| **A** | 7,995 | **`npxxy AND tilt` — 100.0%** (npxxy alone 95.7%, tilt alone 91.1%) |
| B | 795 | `tilt` alone — 100.0% |
| F | 700 | `tilt` alone — 100.0% |

Zero mismatches on Class A. The conjunction is **load-bearing, not vacuous**: the
tilt overturns npxxy on **342** rows and npxxy overturns tilt on **708**.

**Where I went wrong.** There are **two instruments**, and `MotifThresholds` is only
one of them:

- the **motif instrument** — five metrics, collapsed to NPxxY-OH alone on
  2026-09-01 at 07:31;
- the **midpoint-crossing instrument** on `d_tm6` — the tilt — described at
  `switch_signal.py:71-72` as *"cross-validated against the midpoint-crossing
  instrument on d_tm6 (Pearson r = −0.681 — independent enough to carry
  non-redundant signal)"*.

**"Two-instrument success" means both, for Class A.** The 2026-09-01 collapse was
*within the motif instrument*, five metrics to one — **not** a collapse of two
instruments to one. `prediction_is_active_like` implements only the motif half,
which is why reading it alone made the predicate look single-metric.

`paper_af3`'s statement that "no scored campaign ever ran the 3-of-5 rule" is
**true and consistent with this** — the 3-of-5 was the motif instrument's internal
rule. I took their correct statement and drew a wrong conclusion from it.

**What stands, what falls:**

- **FALLS:** "the manuscript describes a predicate that produced no data." It
  describes the predicate that produced all of Block A. **The manuscript is right
  on this point and I was wrong.**
- **FALLS:** the premise under decision **D-A**. Aditya chose "NPxxY-OH alone,
  tilt reported" because I told him the conjunction never ran. **D-A must be
  re-decided on correct information.**
- **STANDS:** F-2 (the confidence circularity) — though note the gate is **not**
  baked into Block A's shipped `active`: 47 rows with `min_plddt_at_anchor < 50`
  are `active=True`, so **P7 is computable on this data**.
- **STANDS:** F-3 (9.08 applied vs 9.082 derived).
- **UNCHECKED, and now suspect:** `CLAUDE.md` says Class B "substitutes a kink
  angle". Block A's Class B rows reproduce as **tilt alone at 100%**, and
  `kink AND tilt` gives only 23.6%. The kink threshold is present on all 795 rows
  and appears unused.

---

## F-1c · WHERE THE CONJUNCTION LIVES — answered from source by `paper_af3`

Not in the scorer. `switch_signal.py::prediction_is_active_like` is **Class-A only**
and single-metric; it returns `"insufficient"` for Class B/F because NPxxY is NaN
there. **That file's docstring claim that Class B/F use "midpoint-crossing on the
per-class anchor pair" is itself stale** — the same defect class as the ≥3-of-5
language, in the same file.

**The class-conditional AND lives one layer up**, in
`scripts/block_a_campaign_analysis.py::two_instrument_state_calls()` (~line 486),
and it operates on **per-(receptor, backbone) medians** across the cognate arm's
5 seeds × 5 samples — *not* per row:

| class | rule |
|---|---|
| A | `npxxy_oh < 9.082` **AND** `tilt > 14.932` |
| B | `kink < 159.95` **AND** `tilt > 14.932` (~line 539) |
| F | `tilt > 14.932` alone |

Output artefact: `experiments/018_block_a_switch_test/analysis/two_instrument_state_calls.csv`,
offered and **worth requesting** — it is the authoritative Class B/F numbers.

**And the kink WAS eventually wired in.** `paper_af3` cite
`docs/POST_BLOCK_A_CLEANUP_2026_09_02.md` Finding 3 verbatim: *"Design error, not a
data error. The class-extension work delivered the Class B kink metric to the schema
but never wired the predicate to use it. The extension was on paper only."* Fixed
2026-09-02.

**So my "Class B reproduces as tilt alone, 100%; kink AND tilt gives 23.6%" is
correct for the state Block A's delivered rows are in — pre-fix — and must not be
read as describing the project's current Class B numbers.** Their standing rule:
do not diff pre-cleanup against post-cleanup Class B figures; they are different
axes. Block A's shipped rows carry `threshold_kink_used = 159.95` on all 795 Class B
rows, which is exactly the "delivered to the schema, never wired" signature.

---

## F-1b · What was actually stale (the surviving part of the original finding)

The **module header docstring** at `switch_signal.py:14-20` still describes the
motif instrument as "≥3 of the 5 motif metrics", which the 07:31 collapse
superseded. That much is genuinely stale and `paper_af3` confirmed it. It is a
docstring defect inside one instrument — **not** evidence that the second
instrument does not exist.

**What the scorer does** — `scorer/switch_signal.py::MotifThresholds`, in the
bundle at `protocol/received/source_bundle/`:

```
METRIC_SPECS = (("d_npxxy_y558_y753_oh", 9.08, "active_lt", "NPxxY OH-OH"),)
K_OF_N = 1        MAX_MISSING = 0
```

One metric. The GPCRdb TM6 tilt and the Class B kink appear only in the comment
on `K_OF_N`, as things that *could be re-added* — "a config change, not a code
change". The tilt is a **fallback** for receptors with non-Tyr at 5.58 or 7.53,
never a conjunct.

**What we have been writing** — two instruments ANDed, class-conditional:
NPxxY-OH < 9.08 Å AND tilt > 14.932 Å.

**Their collapse was sound and is not in dispute.** Locked 2026-09-01 on the
evidence in `refs/thresholds_panel.csv`: DRY is TM6 re-measured (r = +0.913),
NPxxY-OH and Y5.58-pack are collinear (r = +0.784) with the pack metric
self-classifying at only 71.1%, TM5-outward and ICL2 helicity separate by under
0.1 Å. NPxxY-OH alone reaches 94.3% (32/36 A→A, 34/34 I→I) on 70 of 80 tier-1 rows.

**`paper_af3` established the sharper fact**, from their git log: the collapse
landed 2026-09-01 07:31 and the Block A dispatch tag is *after* it. **No scored
campaign ever ran the ≥3-of-5 rule.** Our description names a predicate that
produced no data — not a superseded one, an unused one.

**Where it came from, and the lesson.** The module *header* docstring still
describes the pre-collapse ≥3-of-5 composite; the class docstring below it
records the collapse. We inherited the header. This is the project's recurring
failure exactly — scope asserted in the most-read text and qualified in the
least-read text. See `[[scope-is-asserted-where-it-is-most-read]]`.

**Requirement on the redo:** Group 0 calibrates the instrument that actually
exists — single-metric NPxxY-OH. If we want a second instrument, we build and
justify it ourselves rather than inheriting one from a docstring. `g0_preflight`
check **G0-10** already records the class F tilt defect and is the right place
to carry this.

---

## F-10 · P7 IS COMPUTED. The null holds: pLDDT does not separate.

**The paper's third title clause had never been computed anywhere.**
`paper_af3`'s own analysis emits it as
`{"status": "descriptive_placeholder", "note": "requires per-row pLDDT column;
deferred to analysis-time"}`. Computed 2026-09-12 on Block A's delivered rows, no
GPU. Code `build/p7_confidence_separation.py`; results
`inputs/p7_confidence_separation.{csv,json}` and `inputs/p7_per_receptor.csv`.

**Why it was computable here at all.** The scorer's row classifier forces
"inactive" below pLDDT 50 before reading geometry (F-2), which would make the
question circular. **Block A's shipped `active` column does not carry that gate** —
47 rows with `min_plddt_at_anchor < 50` are `active=True` — so on this data
confidence and the state call are independent and the question is answerable.

**Design.** Ground truth is structural, not the predicate's own output: a
prediction is really active iff `rmsd_to_active_ref < rmsd_to_inactive_ref`.
n = 7,886 rows, 40 receptors, 26 clusters. Predicate accuracy against that truth
is **92.3%**. Exclusions E1 + E2 only — never `excl_any`; E3 is excluded on our own
`METHODS_DRAFT.md:115-117`, which records it as irrelevant to confidence
correlations. Cluster bootstrap, 10,000 resamples, seed 20260912.

| metric | pooled AUC | within-receptor |
|---|---|---|
| `plddt_mean` | 0.600 [0.495, 0.689] | 0.558 [0.444, 0.660] |
| `min_plddt_at_anchor` | 0.473 [0.386, 0.588] | 0.567 [0.411, 0.705] |
| `plddt_at_anchors` | 0.545 [0.458, 0.661] | 0.552 [0.381, 0.697] |

**Every interval includes 0.5, at both scopes, on all three metrics. The null is
supported: confidence does not separate correct from incorrect state calls.**

**REFINED 2026-09-12 — the primary analysis now EXCLUDES the 400 forced-inactive
rows** (EDNRB, GRPR; see the mechanical-error trace below). Those rows cannot
answer this question, because no call was made from the geometry — including them
risks measuring "does confidence predict being an unevaluable receptor" instead.
Primary: **7,486 rows, 38 receptors, 24 clusters, predicate accuracy 94.2%.**

| metric | pooled (primary) | within-receptor | pooled if included |
|---|---|---|---|
| `plddt_mean` | 0.578 [0.455, 0.685] | 0.571 [0.438, 0.683] | 0.600 |
| `min_plddt_at_anchor` | 0.507 [0.407, 0.659] | 0.609 [0.442, 0.752] | 0.473 |
| `plddt_at_anchors` | 0.573 [0.467, 0.721] | 0.583 [0.395, 0.729] | 0.545 |

**Robustness, checked 2026-09-12.** All four generated artefacts reproduce
byte-identically on re-run, and the bootstrap intervals move by at most **0.0031**
under a different resample seed (20260912 vs 777001) — so 10,000 resamples is
ample and every interval spans 0.5 under both. The conclusion is not seed-dependent.

**The exclusion changes nothing, and that is the useful result.** The deltas are
**mixed in sign and ≤ 0.033** (+0.022, −0.033, −0.028), every interval still spans
0.5 at both scopes, and the conclusion is identical either way. **P7's null is
robust to the single most contestable analysis choice in it.** My first reading of
these deltas — that the excluded rows "inflate" the separation — was wrong; they do
not move it in a consistent direction at all.

**The error I made and caught.** The first run reported within-receptor AUCs of
0.645–0.681 with intervals *excluding* 0.5 — i.e. the opposite conclusion. That was
an artefact of my own aggregation: accuracy is 92.3%, so errors are rare and
**concentrated** — 10 of 40 receptors have zero wrong calls and 22 have fewer than
five — and an unweighted mean over receptors gave one with a single error the same
weight as one with a hundred. Requiring **≥10 wrong and ≥10 correct** leaves **14 of
40 receptors** carrying an AUC, and the effect disappears. The exciting version was
the wrong version.

**Two things worth carrying into the redo:**

- **The errors are concentrated: the top five receptors hold 59% of them.** A
  pooled accuracy figure hides that the predicate fails on specific receptors
  rather than degrading evenly. Per-receptor accuracy belongs in the redo's
  reporting.

- **AND HALF OF THAT CONCENTRATION IS MECHANICAL, NOT A PREDICATE FAILURE.**
  Traced 2026-09-12 after `paper_af3` sent `two_instrument_state_calls.csv`.
  **EDNRB and GRPR carry no NPxxY axis at all** — `d_npxxy_oh` is null on all
  400 of their Class A rows — and because the Class A rule is `npxxy AND tilt`,
  **NaN propagates to False and they are called active on ZERO rows.** Structural
  truth says **43%** of those rows are active, so their accuracy is **57%**, which
  is not the predicate being wrong about them; it is the predicate never running.

  **Those two receptors contribute 172 of 607 errors — 28% of every error in the
  campaign — from 5% of the rows.** Campaign accuracy is **92.3% including them
  and 94.2% excluding them**.

  **`5HT2C` is NOT in this class** — its NPxxY axis is defined and its 99/200
  errors are real. So of the two receptors I flagged as "at chance", one is an
  artefact of an unevaluable axis and one is a genuine failure. **They should never
  have been named in the same breath, and the distinction is only visible if you
  check which axis exists.**

  **This is decisive support for D-A's exclusion rule.** The campaign agent's
  recommendation — that `excl_npxxy_undefined` be a **per-row boolean set at
  dispatch from the anchor table**, not discovered at scoring time — is exactly
  what would have prevented this. A silent NaN did not merely lose two receptors;
  it injected 28% of the campaign's apparent error as a mechanical artefact and
  depressed the headline accuracy by 1.9 points.

- **Class B and F are unaffected** and it is worth saying why: their rule is `tilt`
  alone (B post-fix adds the kink), which needs no NPxxY, so the eight Class B/F
  receptors with undefined NPxxY are scored normally.

- **Three checker bugs of mine getting to this number**, all caught before it was
  recorded: I used `excl_E3_npxxy` as the blindness test (it flags *two* causes —
  failing references AND unmeasurable axes, as `METHODS_DRAFT.md:112-115` states),
  then `d_npxxy_oh.isna()` across all classes (which sweeps in Class B/F, who do
  not need the axis), before restricting to Class A. The first two gave 59% and
  34%; the right answer is 28%.
- **This bears on `HANDOVER.md`'s standing claim**, which says confidence separates
  pooled (AUC 0.60–0.96) and that this "evaporates when you control for receptor".
  The direction is right but the pooled figure is not reproduced here: pooled AUCs
  are 0.47–0.60 with intervals spanning 0.5. That claim should be re-derived or
  withdrawn before it reaches a sentence.

---

## F-13 · The apo arm: Class B is not saturated, but the backbones disagree by 9 Å — and the Class F threshold has no discriminating power at all

`paper_af3` sent `two_instrument_state_calls_apo.csv` (sha256 `361ce5a2…`) after
Aditya signed off in their session. It was requested to settle one question and
answered three.

**The question asked — is Class B saturated? No.** Cognate 1.000 against apo 0.250
on Boltz and Protenix is a large, real separation. The Class B result is not an
artefact of an instrument that calls everything active.

**But two backbones show ZERO separation, on both B and F:**

| class | backbone | cognate | apo | gap |
|---|---|---:|---:|---:|
| B | boltz | 1.000 | 0.250 | +0.750 |
| B | chai | 1.000 | 0.750 | +0.250 |
| **B** | **of3** | **1.000** | **1.000** | **0.000** |
| B | protenix | 1.000 | 0.250 | +0.750 |
| **F** | **of3** | **1.000** | **1.000** | **0.000** |

### (a) Class B — the backbones disagree by 9 Å on the same input

Apo tilt medians, same four receptors, same apo input, threshold 14.932:

| backbone | median apo tilt | above threshold |
|---|---:|---:|
| boltz | **12.38** | 1/4 |
| protenix | **12.53** | 1/4 |
| chai | **21.47** | 3/4 |
| of3 | **19.60** | 4/4 |

**Boltz and Protenix predict Class B apo receptors CLOSED at ~12 Å; Chai and OF3
predict them OPEN at ~20 Å.** That is an **8–9 Å disagreement about the same
receptors with no partner supplied** — larger than the active/inactive separation
the threshold was built to detect. This is not a threshold problem; it is two
backbones and two backbones predicting different structures.

**Requirement:** the redo cannot report a pooled Class B rate. A number averaged
over backbones that disagree this violently describes nothing.

### (b) Class F — the threshold sits inside the apo distribution, on every backbone

Apo tilt medians run **14.20, 15.09, 16.10, 16.12** against a **14.932** cut. Every
backbone straddles it. **The Class A-derived threshold has no discriminating power
on Class F at all**, regardless of backbone.

**This empirically confirms the standing `g0_preflight` WAIT** ("the redo must
measure class F tilt on 2×44–6×31, not 2×46–6×37, or drop the class F arm"). That
was a geometric argument; this is the measurement. **Class F as currently
instrumented cannot distinguish apo from cognate.**

### (c) ~~SMO gets LESS open when the partner is added~~ — **RETRACTED 2026-09-12**

> **This was an OF3-only observation stated as a receptor property, and it is the
> same defect I had flagged for Class B one paragraph earlier: pooling across
> backbones that disagree.** Caught by `paper_af3` on review; recomputed here from
> the two state-call tables we hold and confirmed to the decimal.

**Class F, cognate − apo tilt, all four backbones:**

| receptor | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| SMO | **+0.22** | **+0.04** | −2.14 | **+0.19** |
| FZD7 | +1.66 | +0.01 | −0.07 | +0.26 |
| FZD6 | −0.38 | +2.41 | +0.12 | +0.29 |

**SMO moves slightly POSITIVE on three of four backbones.** The −2.14 is OF3 alone.
FZD7's negative is −0.07 on OF3 alone, which is noise. So "two of three Class F
receptors do not move the way the model predicts" was a statement about one
backbone wearing the clothes of a statement about a class. **Do not put weight on
SMO specifically going backwards.**

**What survives, and it is the stronger claim:** Class F deltas span **−2.14 to
+2.41 with inconsistent sign across backbones**. That is what an axis which is not
measuring activation looks like — and it does not depend on any single receptor or
any single backbone. Conclusion (b) is unaffected and arguably reinforced.

**And a fourth receptor is not there at all — BY DESIGN, corrected 2026-09-12.**
`FZD4` appears in the apo table on all four backbones and is absent from the cognate
table on all four. I flagged that to `paper_af3` as a possible gap. It is not: their
`PREREG.md:277` reads *"FZD4 is apo-only in Block A (DVL2 transducer, not Ga;
substituting alphas as proxy is the W54 taxonomy failure at n=1)"*. **FZD4's
transducer is Dishevelled, not a Gα**, so there is no cognate partner to supply;
giving it Gαs would have been the taxonomy error we both keep citing. Its active
reference `8WM9` is Dishevelled-DEP-stabilised, which is what the `DVL_DEP` value in
their `active_stabilization_source` vocabulary is for. So the Class F contrast
resting on three receptors is **pre-registered design, not attrition.**

**And their prereg reached our conclusion by a different route.** `PREREG.md:183`
already reduces Class F to **SMO only** for the primary result — FZD4 uses DVL,
FZD6/7 use atypical Gs, SMO uses Gi, and three transducer mechanisms across four
receptors cannot share a derived anchor (GPCRdb itself uses a different TM6 measure
for Class F). **We got to "Class F needs a different atom pair or gets dropped" from
apo measurements; they got to "Class F is SMO-only" from transducer taxonomy. Same
destination, two independent routes** — which is worth more than either alone, and
it strengthens the Class A-only scope (D-2026-09-12-d) rather than merely agreeing
with it.

### Bearing on D-A

The tilt is one of the two instruments in the conjunction. **On Class A it behaves
well** — apo medians ~12 with only 3–15 of 40 above threshold, so the cut
discriminates. **It is on B and F that it fails**, which is where it is used
*alone* (B adds the kink post-fix; F is tilt-only). So D-A's choice about the Class
A conjunction is not undermined by this — but any decision to extend the tilt to
Class B or F is.

---

## F-12 · F3 may be discarding the inactives nearest the decision boundary — PRELIMINARY, n = 4

**Status: a signal worth testing, not a finding.** Stated with its n so it cannot be
quoted as more than it is.

F3 — "GPCRdb state label not contradicted by the entry's own ligand pharmacology" —
removes **27 inactives from the calibration pool (88 → 61), 31% of the scarce
class**, concentrated in five receptors (`5HT2A` loses 10). Inactives run 6.1:1
against actives in the frozen ladder, so this is the single largest discretionary
cut in Group 0.

**The full sensitivity arm cannot be built yet.** `g0_calibration_structures.csv`
carries **no measured axis values** — the measurement pass is still an outstanding
Group 0 dependency, and the cache holds 297 of 726+ structures. Only
`g0_pilot_measurements.csv` has `d_npxxy_oh` and `d_tilt`, for 30 structures.

**But the pilot happens to sample the discarded population — 6 of its 30 — so a
preliminary look is possible:**

| state | group | n | median `d_npxxy_oh` | median `d_tilt` |
|---|---|---:|---:|---:|
| Inactive | retained by F3 | 6 | **11.51** | 11.95 |
| Inactive | **F3-removed** | **4** | **9.43** | 11.79 |
| Active | retained | 7 | 4.47 | 17.87 |
| Active | **F3-removed** | **1** | **25.59** | 15.24 |

**The concern, in one line: the NPxxY threshold is 9.08, and the inactives F3
discards sit at 9.43 while those it keeps sit at 11.51.** If that holds at scale,
F3 is removing the inactives *nearest the decision boundary* — which would make the
inactive pole look cleaner than it is and bias the threshold outward, inflating the
apparent active/inactive separation.

**On the active side F3 looks straightforwardly right:** the one removed active has
`d_npxxy_oh = 25.59` against a retained median of 4.47. That is a genuine
mislabel, exactly what the rule is for.

**So F3 may be doing two different jobs** — correctly catching mislabelled actives,
and possibly over-removing borderline inactives — and a single flag cannot separate
them.

**n = 4 and n = 1. This is a direction, not a result.** The test that settles it:
run the measurement pass, then recompute both thresholds with F3 on and off and
report the shift. If the thresholds barely move, F3 is not consequential and D3
simplifies. If they move, **F3 needs to be split by which side of the label it is
correcting** — and that is a decision for Aditya, not a filter setting.

**Requirement on the redo:** the measurement pass must record the axis values for
the F3-*removed* structures too, not only the survivors. A filter whose effect
cannot be measured after the fact is a filter nobody can audit.

---

## F-11 · Retinal must be curated by ISOMER, not by CCD — and the agonist-bound-inactive population is not one thing

Both halves verified independently against the frozen GPCRdb snapshot; found by the
lit session, confirmed here.

**(a) One CCD code, two opposite pharmacologies.** Of the 41 snapshot entries
carrying CCD `RET`, GPCRdb ships **three distinct isomer names**:

| name | state | function | n |
|---|---|---|---:|
| Retinal (11-cis) | Inactive | **Inverse agonist** | 16 |
| Retinal (all-trans) | Active | **Agonist** | 14 |
| Retinal (all-trans) | Inactive | Agonist | 4 |
| Retinal (11-cis) | Inactive | Agonist | 3 |
| **Retinal (11-cis)** | **Active** | Agonist | **2 — 9EPR and 8IU2** |
| Retinal (9-cis) | Inactive | Inverse agonist | 2 |

**11-cis is the inverse agonist and all-trans is the agonist, and they share a CCD
because they are isomers of one compound.** Any pipeline keyed on CCD alone sees one
ligand where there are two pharmacological opposites. **Requirement: curate retinal
by isomer name, never by CCD.**

**CORRECTED 2026-09-12 — I reported the candidate POOL's property as the reference
PAIR's, and they differ.** I wrote that OPSD and B1B1U5 both carry `RET` in both
roles. True of every structure of those receptors; **false of the pairs we actually
score against**, which is the only scope curation cares about:

| receptor | active ref | its ligand | inactive ref | its ligand |
|---|---|---|---|---|
| **B1B1U5** | `9EPP` | **11,20-ethanoretinal, `A1H6M`**, Agonist | `6I9K` | 11-*cis* retinal, `RET`, Inverse agonist |
| OPSD | `4X1H` | β-nonylglucoside — a **detergent** | `7ZBC` | 11-*cis* retinal, `RET`, Inverse agonist |

**B1B1U5 is therefore NOT blocked by the shared-CCD problem.** Its two reference
ligands are chemically distinct and carry different codes. **OPSD is blocked, but
for a different reason than I gave** — its active reference carries no agonist at
all, only a detergent. A missing-ligand problem, not an isomer one.

The general finding is untouched: across all 41 `RET` entries, 11-*cis* is the
inverse agonist and all-*trans* the agonist.

**(b) 9EPR's isomer name is wrong in GPCRdb.** `tejero2024opsin` p2 states 9EPR was
reconstituted with **9-cis retinal and illuminated at 495 nm** to activate it, so
the modelled chromophore is **all-trans**. GPCRdb calls it 11-cis. It sits in a
two-entry outlier class against a fourteen-entry majority. **The function
annotation (Agonist) is right; only the isomer name is wrong** — a per-entry error,
not a systemic limitation, since GPCRdb demonstrably has the vocabulary.

**(c) Bears on Group 0's D3, and this is the part that matters.** Of **81**
agonist-bound *Inactive* structures in the snapshot, **8 are opsin/retinal
photo-intermediates** — agonist covalently bound, receptor not yet in the active
conformation — including **8A6E, which is in our own panel as an inactive
reference**. The other 73 are something else: partial agonism, or annotation drift.

**The agonist-bound-inactive population is heterogeneous, and D3 must not treat it
as one class.** Lumping a bathorhodopsin-like photo-intermediate with a
partial-agonist complex blurs exactly the distinction D3 is trying to measure.

**(d) SCOPE CORRECTED — and it does NOT land where I first thought.** I pursued
this as a threat to the Group 0 calibration ladder. It is not one:

- **All 8 opsin photo-intermediates carry `role='application'`, not
  `'calibration'`.** They are panel-receptor structures, excluded from the
  calibration pool at F0 by the panel/calibration split. **They never touch the
  frozen F4 ladder.**
- **F3 — "GPCRdb state label not contradicted by the entry's own ligand
  pharmacology" — removes 27 inactives from the calibration pool (88 → 61), and
  NONE of them are opsins.** They are `5HT2A` (10), `LGR4` (6), `MTR1A` (5),
  `MTR1B` (4), `NTR1_rat` (4) and four singletons. For these, "agonist-bound but
  labelled inactive" is a genuinely different phenomenon — partial agonism,
  annotation drift, or an inactive-state structure with an agonist soaked in —
  and *none* of it is photochemistry.

**So D3's real question is sharper than the one I was about to ask.** F3 discards
**31% of the inactive pool** (27 of 88) on a single rule, and the losses are
**concentrated in five receptors**, one of which (`5HT2A`) loses ten. Inactives are
the scarce class — the frozen ladder runs 372 active to 61 inactive, 6.1:1 — so a
rule that removes nearly a third of them, unevenly, deserves its own sensitivity
arm rather than a flag. **That is what D3 should decide, and it is not about
opsins.**

**(e) Where the opsin finding DOES land: the panel's own references.** `lee2026confornets`
uses **8A6E** as its inactive reference for bovine rhodopsin — a **100-picosecond
light-activated XFEL structure** from a time-resolved series (8A6C/8A6D/8A6E =
1/10/100 ps, "Ultrafast structural changes direct the first molecular events of
vision"). GPCRdb annotating it *Agonist on an Inactive structure* is the tell.

**We do not use it. We use 7ZBC** — same deposition, same 1.8 Å, but annotated
**inverse agonist**, consistent with the unilluminated dark-state control of that
series. **Our choice is the better one**, and this is the second receptor
(with B1B1U5) where our reference differs from the published benchmark's in our
favour. It is worth saying so in Methods rather than leaving it implicit.

**Two checker bugs of my own on the way to this**, both caught before anything was
recorded: I filtered the flag columns with `in ("1","True")` when
`flag_label_conflict` holds a *reason string*, and then with truthiness, when the
CSV writes `'0'` — a non-empty, therefore truthy, string. Both produced "0 removed"
and both were mine, not the data's.

---

## F-2 · The state call is not independent of confidence

`prediction_is_active_like` returns `"inactive"` **before any geometry is read**
when `confidence_flag == "low"`, and `confidence_flag` is a pure function of
`min_plddt_at_anchor` (low < 50, borderline 50–70, high ≥ 70), verified
independently across all 32,000 Block B rows.

So **every prediction with minimum anchor pLDDT below 50 is called inactive
whatever its structure.** `paper_af3` confirms it is intentional, that there is
exactly one classifier and no variant or toggle, and — in their words — that
this is *"a real circularity, not an artefact"*.

The paper's third title clause is that model confidence does not track state
correctness. That claim and the state call are not independent by construction.

**Requirement on the redo: drop the early return.** Let geometry stand alone and
carry confidence as a separate reported axis. `paper_af3` named the same fix.

---

## F-3 · 9.08 is applied; 9.082 is derived

`refs/thresholds_panel.csv` records `threshold = 9.082` from means (5.285,
12.878), whose true midpoint is 9.0815. The code constant is **9.08**, rounded,
and its inline comment rounds the means too, to (5.28, 12.88).

`paper_af3` told us 9.08 was locked and our 9.082 was drift on our side; their
own lock file says otherwise. Our number came from their panel and was right.
Corrected with them 2026-09-11.

**RESOLVED EXHAUSTIVELY 2026-09-12. Both values are live, in different layers.**

- **Row level (the scorer):** Block A's delivered rows carry
  `threshold_npxxy_used = 9.08` and nothing else, and `npxxy_active` reproduces
  from `d_npxxy_oh < 9.08` at **exactly 100.000%** of Class A rows.
- **Analysis level:** `paper_af3` report that
  `scripts/block_a_campaign_analysis.py::two_instrument_state_calls()` applies
  **`npxxy_oh < 9.082`**, on per-(receptor, backbone) medians.

**The two thresholds disagree on exactly ONE row in the entire campaign**, and we
can name it: **`B1B1U5` / `of3` / `apo`, `d_npxxy_oh = 9.080077`** — inactive under
9.08, active under 9.082. One row of 7,995 Class A, in the apo arm, and the
analysis layer works on medians, so the practical consequence is nil.

**The redo pins ONE value in ONE place and asserts it.** Two layers carrying two
roundings of the same derived number is how a discrepancy survives four blocks
unnoticed; that it cost nothing here is luck, not design.



---

## F-4 · There is no Gα-side numbering to inherit

`paper_af3` confirm: no CGN import anywhere in the scorer. Partner positions are
raw UniProt index, or counted from the C terminus ad hoc when treating α5-CT.

The redo's entire ladder is defined by position on the Gα C terminus.
**Requirement: we define a CGN-based convention, freeze it in `spec/`, and send
it to them** — they have said they will adopt whatever we define.

---

## F-5 · The ladder is not a smooth axis, and depth does not track length

Measured by `paper_af3`, in the bundle at
`experiments/019_block_b_partner_selection/analysis/msa_depth_report.md:353-359`
— verified against the primary table, not relayed:

| partner | aa | MSA depth |
|---|---:|---:|
| DAMGO | 5 | **1** |
| substanceP | 11 | **1** |
| endothelin1 | 21 | 732 |
| gcn4 zipper | 33 | 224 |
| random_helix_40mer | 40 | **1** |
| **arrestin_Ctail** | **41** | **1** |
| Gg2 | 71 | 3,191 |
| cognate Gα | 350-394 | 11,904-14,986 |

A 21-mer retrieves more than a 33-mer; a 40-mer returns query-only while a 15-mer
returns 84. **The predictor is naturalness, not length** — whether the sequence
has homologs in the searched databases. Their own note at `:378-383` says so.

**`arrestin_Ctail` is the case that governs our design.** 41 residues, an
*excised fragment* of a larger protein, depth 1. Our α5-CT rungs are excised
fragments of Gα — the same case.

**Consequence if the short rungs return depth 1:** on Boltz, OF3 and Protenix the
paired-alignment axis is degenerate for short rungs and progressively less so for
long ones. The apo→cognate operational difference then shrinks toward Chai's as
the partner shortens, and **the ladder varies peptide length and pairing regime
together** — the exact confound the redo exists to remove.

**MEASURED 2026-09-11 by `paper_af3`, 112 rows, 16 Gα families × 7 rungs. F-5 is
no longer a hypothesis — it is confirmed, and it is worse than predicted:**

| rung | measured MSA depth |
|---|---|
| **R1_ct11** | **0, across 16 of 16 families** — no database homologs at all |
| **R2_ct15** | **family-dependent: 0 for Gq/G11/G14/G15/G12, 2-459 for the rest** |
| R3_ct21 | 47-581, all non-zero |
| R4_a5helix | 186-1,995 |
| R5_a5plus | 2,273-3,043 |
| R6a_da5 / R7_full | 8,474-9,203 |

**Raw table received as a file: `protocol/received/rung_msa_depth.csv`, 112 rows,
sha256 `bb45b4b1…`.** Two refinements it forced, neither visible in the summary:

- **`ct15` is not "5 zero, 11 non-zero" — it is degenerate for 15 of 16 families
  with a single outlier.** The eleven non-zero families read Golf 2, Gz 6, G13 18,
  Ggust 21, Gt1 21, Gt2 21, Gi3 25, Gi1 33, Gi2 33, Go 42 — and **Gs 459**, an
  order of magnitude above everything else. Gs is the most common cognate partner
  on any GPCR panel including ours, so under an MSA-on design `ct15` would behave
  one way for Gs and another for every other family. **This makes the case for a
  constant regime without reference to the zeros at all:** even where alignments
  exist at the short rungs they vary across families by two orders of magnitude.
- **`unpaired_depth = -1` is a timeout sentinel**, not a depth — three rows
  (R7_full/Gi2, R7_full/Gz, R6a_da5/Gz). Any mean, min or monotonicity check over
  that column must filter on `note == "ok"` first. Flagged to `paper_af3`.

`ct11` at depth 0 forces single-sequence on every backbone. But **`ct15` is the
finding neither side predicted**: at a *single rung* the alignment regime varies
**by Gα family**. The ladder does not merely confound length with pairing along
its length — at `ct15` it confounds them *across the panel within one rung*.

**Consequence: the MSA-free partner is MANDATORY, not one mitigation among four.**
With a natural partner MSA the alignment regime becomes a function of both rung
and family and no contrast along the ladder is interpretable. Running the partner
MSA-free at every rung makes the regime constant by construction.

**This puts the harness change on the critical path.** The dict route already
exists (`propose.py:462-465` — an empty string for a chain makes the loop skip it,
which *is* MSA-free) but has no caller. Needed: a caller passing
`{"A": <receptor a3m>, "B": ""}`, the same for Protenix at `:589`, and a new
branch for Chai. **Feasibility ANSWERED 2026-09-12: yes.** `paper_af3` confirm OF3
(`chains[*].main_msa_file_paths` / `paired_msa_file_paths`) and Protenix
(`proteinChain.unpairedMsaPath` / `pairedMsaPath`) already take per-chain paths
natively in the JSON, and Boltz's inline YAML `sequences[*].protein.msa` is
per-chain too. **Chai is the sole gap** — `--msa-directory` is keyed by sequence
sha256, not chain id, and has no `MSA_A3M_PATH` branch at all, so it pulls
full-depth per chain regardless of rung. Their scoping: one caller building a
`chain_id -> path_or_empty` dict, plus for Chai writing the intended pqt directly
rather than relying on hash lookup into the shared cache. Not a redesign.

**Our refinement, sent the same day: the partner gets an explicit QUERY-ONLY
alignment (depth 1) at every rung on all four backbones — never an absent one.**
Omission relies on four different fallback behaviours we have not measured, and
the bad case is silent: a backbone that generates its own alignment for a chain
it finds no file for would deliver *full depth* exactly where we intended zero,
with nothing in any status JSON showing it. Depth 1 is constant by construction,
identical across backbones, and **verifiable after the fact** — an absence is not.

**And the partner's OBSERVED alignment depth must be recorded on every row**, not
its intended depth. Per F-6 no MSA metadata reaches any scored row today, which is
why the `ct11` cliff had to be established from a side report rather than from the
rows. With observed depth recorded, "the alignment regime was constant along the
ladder" becomes demonstrable from the data instead of asserted from the design.

**Decision D-B in `CAMPAIGN.md` is therefore closed by measurement, not by choice.**

Paired addendum authorised and scoped: skip `ct11` (depth 0 bounds paired at 0),
skip the zero-depth families at `ct15`, run `ct21`+ across ~3 receptors, ~40
alignment-only submissions. Its value is now **documentary** — it converts
"we avoided a confound" into "we measured it, then removed it". If the cliff is real, the
ladder is redesigned — candidate mitigations are to run the ladder
single-sequence on all four backbones so the alignment regime is constant, or to
carry depth as a measured covariate on every row, or both.

---

## F-6 · No MSA metadata reaches any scored row

Grep of every row-touching scorer module for `msa|a3m|pqt`: **zero matches**.
Across all 42,180 predictions there is no depth, source, pairing state or
alignment hash. **MSA cannot be joined to outcome at all** in the existing
campaign — which is why F-5 had to be established from a side report rather than
from the rows.

**Requirement:** `g1_recording_spec.tsv` carries partner-MSA depth, receptor-MSA
depth, pairing state and alignment provenance on every row. Already sent to
`paper_af3` as part of our frozen input set.

Related, and flagged to them as a question rather than a finding: `msa_prewarm.py`
appears to pre-warm only single sequences in `mode=env`, while the paired
directories are `pairgreedy-env` and OF3's paired hash is complex-keyed — which
would mean apo arms hit a warm cache and cognate arms paid a cold search, an
uncontrolled difference between the two arms the paper contrasts. Unconfirmed;
the `_of3_colabfold_http_summary.json` sidecars would settle it.

---

## F-7 · Block C's cognate arm supplies a non-cognate Gα for 35 of 40 receptors

All three Block C manifest builders hard-set `COGNATE_PARTNER_IDENTITY = "alphas"`
(`build_block_c_tier1_manifest.py:104`, `tier3:150`, `smoke:77`) and assign it to
every cognate row without consulting the coupling table. 6 of 8 Tier-1 and 29 of
32 Tier-3.

**Block A's own code names this failure and avoids it**
(`build_block_a_manifest.py:48-51`): *"A blanket alphas would recreate the W54
taxonomy failure."* They ship `verify_cognate_identity.py` to catch it. Nothing in
the bundle documents Block C as an exception. **Asked, not yet answered.**

Bears on the highest-value unblocked result in `HANDOVER.md` — the uncrossed
ligand-class × partner-presence comparison over ~18,400 scored predictions. If the
cognate arm is 35/40 non-cognate it contrasts apo against *arbitrary-Gα*.

**Requirement:** the redo reads the cognate Gα per receptor from
`coupling_cognate_map.tsv` and `g1_preflight` check **B16** already enforces that
every row carries both the supplied family and the reference tip. Keep it.

---

## F-8 · The analysis layer's stated unit is not its implemented unit

- The provenance JSON declares `two_stage_cluster_resample_receptors_then_seeds`
  (`analyse_block_c_tier1_headline.py:32-34`, `:601-604`); `bootstrap_receptor_mean`
  is one loop over receptor scalars and never draws a seed.
- Block A's primary axis is bootstrapped **over rows** — `task_f_block_a_recheck.py`
  builds `per_receptor_dtm6` and never reads it.
- The seed-is-the-unit-of-variance rule at `switch_signal.py:8-12` is implemented by
  `per_seed_mean`, `delta_d_tm6_per_cell` and `per_receptor_backbone_rollup`, all with
  **zero callers**; the wrapper its docstring names is not in the bundle. All 13
  analysis scripts work row-wise.
- `PREREG.md` contains the word "cluster" **zero times**.
- **P7, the pre-registered null that pLDDT does not separate, was never computed** —
  `analyse_block_c_tier1_headline.py:383-386` emits `"descriptive_placeholder"`. That
  is the paper's third title clause.

**Requirement:** the redo's statistical unit is the paralog cluster, declared once,
implemented once, and proved by a test that fails when the unit changes. P7 is
computed, not inherited.

---

## F-9 · Nothing in the pipeline compares output to input

Not sequence, not chain count, not seed-used vs seed-requested, not MSA depth. A
monomer returned where a receptor + Gα dimer was requested passes every check.
`ok = exit_code==0 and len(produced)>0`, so one CIF out of a requested hundred reads
`ok=true`. Two guards were found policing artefacts the run never consumed — OF3's
`sentinel_bug_seed_present` inspects a top-level `_runner_seeds.yml` that the chunked
branch writes and never reads.

**Requirement, and it is the cheapest hardening available:** three assertions in a
post-run receipt — returned sequence matches requested, chain count matches, seed used
matches seed requested. No GPU. The delivery contract in `runs/README.md` should
refuse a run that cannot answer them.

**Closed, not open:** the OF3 inner-seed formula is
`random.seed(pred_seed * 1_000_003 + chunk_idx)` (`qsub/rerun_of3.sh:194`), reproduced
exactly against all four chunks of the OPSD cell. The earlier failure to derive it was
ours reading a snapshot with no chunking branch.

---

## Still open at the close of 2026-09-11

- **Was a peptide ever dispatched as the partner chain?** Unresolved. Their
  catalogue stocks `endothelin1` (21 aa), `substanceP` (11), `arrestin_FL` (15,
  a legacy mislabel), `DAMGO` (5), and two decoys. The manifest they sent to
  settle it is the **deep-apo tier** — `partner_type=apo` on all 140 rows, no
  partner of any kind. Awaiting the `019_block_b_partner_selection` manifest.
- `build_weekend.py` — the templater `propose.py` says it was adapted from, with
  byte-parity where feasible. Not in the bundle; requested.
- `docs/BLOCK_A_STEP3_VALIDATION_2026_09_01.md` — the human-readable half of the
  threshold lock. Claimed present, absent from the archive; requested.
- Group 0 **D2, D3, D4** and the class F atom pair remain with Aditya.
