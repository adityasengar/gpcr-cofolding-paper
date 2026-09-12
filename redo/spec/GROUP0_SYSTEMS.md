# GROUP0_SYSTEMS.md — the instrument, made buildable

Compiled 2026-09-11 by the Group 0 session. Scope: **the activation predicate itself —
what it is calibrated on, what it can and cannot measure, and the build step that has to
run before E0.1 exists.**

Read `redo/spec/CATALOGUE.md` §3 Group 0 (E0.1–E0.5) first; this file makes
those five entries concrete and, in three places, corrects the population they assume.
Siblings own the panel (`PANEL.md`), the supplied chains (`SEQUENCES.md`), the budget
(`RUN_MATRIX.md`) and Group 1. Nothing here sets a prediction budget; Group 0 spends no
GPU at all.

# Status: FROZEN, 2026-09-11

**Group 0 is a measure, not a result. It is deliberately revisable** — if a later pass
improves the instrument, that is a success, not a correction. Frozen means only this: the
numbers below can be acted on without re-deriving them, and `redo/gates/g0_preflight.py`
is the gate that says so. It runs 11 blocking checks, all 11 proved by planting a defect
and confirming the check fires, and lists 9 outstanding dependencies that are **not**
defects.

```
python3 redo/gates/g0_preflight.py             # FROZEN / NOT FROZEN
python3 redo/gates/g0_preflight.py --selftest  # prove every check fires
```

**The calibration population of record.** Off-panel Class A, after the §5 filters:
**433 structures — 372 active, 61 inactive, 6.1:1, across 106 receptors, 17 of which have
both states.** Independence ladder I1/I2/I3/I4 = 433 / 289 / 260 / 193.

## What is decided

| | decision | where |
|---|---|---|
| **anchors** | `paajanen2026activation`'s convention, stated openly as an anchor choice: **active = ternary complexes**, **inactive = antagonist-bound with no transducer**. Not laundered through a percentage. | §5.1, §6.2 |
| **fit** | **unsupervised, with bootstrap**, and the **mixing weights reported alongside the boundary** — a two-component mixture estimates a class prior whether or not anyone declares one. | §6.2 |
| **middle** | **agonist-only and Intermediate structures are reported as distributions, never assigned to a pole.** | §5.1, §8 |
| **circularity** | carried **per axis**, not as a single posture. Of four axis × pole cells, **only NPxxY-versus-inactive is clean.** | §5.1 |
| **limitation** | the sentence in §5.1 goes into the Methods as written, as a contribution. | §5.1, §7 |
| **D1** | **deferred** — Aditya, 2026-09-11. Does not block; resolve when the calibration is built. Consequence if the OH axis is kept: 42 of 199 Class A receptors are unevaluable. | §0.1, §6.3 |
| **Q0c** | **retracted.** GPCRdb's activation degree encodes partner presence. Must not return; `g0_preflight.py` check G0-6 enforces it. | §5.1 |

## Decisions still with the PI

Three, and each changes the population or the objective. Nothing downstream of Group 0
should be started as though any of them were settled.

| # | decision | consequence of each option |
|---|---|---|
| **D2** | **expand the panel to the 32 E-scope/E-B1 receptors [**25**, corrected 2026-09-12 — see D-2026-09-12-e], or reserve them for calibration.** They cannot both happen. | **Expand:** calibration inactives fall 61 → 20 and paired receptors fall to **zero** — E0.1 becomes a between-receptor fit with no within-receptor evidence. **Reserve:** the expansion in `PANEL_EXPANSION_CLASS_A.md` does not happen. **Split** (recommended): expand onto the actives-rich expansion receptors and reserve the inactive-rich ones — the ranked list is printed by `g0_calibration_set.py`. Must be decided **before** either job starts. |
| **D3** | **do agonist-only, transducer-free structures count as Active?** Reopened — GPCRdb's degree cannot settle it, because that number *is* partner presence. | **Admit** (81 structures): "active" means two things inside one class, and `paajanen2026activation` p.1 says agonist-bound structures are bimodal on this coordinate. **Exclude:** 7 receptors lose their entire active class. **Admit, flag, report both ways** (recommended). It may not be decided by appeal to our own thesis. |
| **D4** | **the balancing rule for the reported cut.** The anchors and the unsupervised fit are settled; the reweighting is not. | Prevalence-weight inherits the PDB's deposition history as if it were a prior on activation. Equal-weight makes calibration and application comparable, since their priors differ (6.1:1 vs 1.4:1). Matched sampling attacks the resolution confound but leaves ~122 structures. Recommended: **equal-weight headline, the others reported**. |

## How to read this

Every number below is produced by a script in this directory from frozen inputs, and every
script prints the sha256 of what it read. Nothing is from memory.

| file | what it is |
|---|---|
| `redo/gates/g0_preflight.py` | **the gate** — 11 blocking checks, each proved by planting a defect; plus the outstanding-dependency list |
| `redo/build/g0_calibration_set.py` | enumerates the population; writes the six CSVs below |
| `redo/build/g0_measure_axes.py` | **the build step** — measures both axes on a deposited structure |
| `redo/build/g0_anchor_conservation.py` | asks, per receptor, whether the axes are defined at all |
| `g0_calibration_structures.csv` | 1,357 rows — every Class A structure with a state annotation, with panel membership and every pre-declared flag |
| `g0_anchor_conservation.csv` | 199 rows — the residue at 5.58, 7.53, 2×46, 6×37 for every Class A receptor entry |
| `g0_filter_ladder.csv` | each exclusion applied in fixed order, with what it removes |
| `g0_independence_ladder.csv` | what each further degree of independence costs in inactives |
| `g0_reference_axis_gap.csv` | the 162 pinned reference rows — what the build step must measure |
| `g0_label_conflicts.csv` | 98 rows whose GPCRdb state label is contradicted by their own ligand |
| `g0_activation_degree.csv` | GPCRdb's graded 0–100 activation degree per population — kept as a **circularity audit**, not a rule; see §5.1 |
| `g0_class_variants.csv` | per-class census for E0.5 |
| `g0_intermediates.csv` | the 21 Class A Intermediates for E0.3 |
| `g0_panel_exclusions.csv` | the receptors withdrawn from calibration, and why |
| `g0_selftest.txt` | the build step reproducing eight shipped reference values |
| `g0_pilot_measurements.csv` | 30 off-panel structures measured end to end |

Frozen inputs, so this is reproducible:

```
77e0b077…a87a91  lit/panels/cache/gpcrdb_structures.json                     (1,716 entries)
b1a115a1…a1b5f3  redo/inputs/panel_systems.csv                             (75 receptors)
25058ee0…da028e  redo/cache/panel_rcsb_cache.json                         (962 entries)
6ee2cad8…5202ef  data/block_b/09_references/reference_set.blockb_pinned.csv  (162 rows)
<see script>       redo/inputs/panel_gpcrdb_degree.csv                       (1,716 rows)
```

---

# 0. The three findings that should be read before anything else

**Group 0 was scoped as an arithmetic job — download 726 structures, measure two distances,
refit two thresholds. It is not one.** Three things came out of building it, each of which
changes what E0.1 can claim.

### 0.1 The NPxxY axis is not defined on a quarter of Class A, and the panel hid it

`d(Y5.58 OH, Y7.53 OH)` is a **hydroxyl-to-hydroxyl** distance. It exists only where both
positions are tyrosine. They are not conserved across Class A.

Measured on all 199 Class A receptor entries in the snapshot, straight from GPCRdb
`residues/extended`, no coordinates required (`g0_anchor_conservation.csv`):

| position | Tyr | not Tyr |
|---|---:|---|
| 5.58 | 164 / 199 | N 12, S 10, T 8, F 1, C 1, H 1, I 1, Q 1 |
| 7.53 | 189 / 199 | L 5, F 3, T 1, M 1 |
| **both** | **157 / 199** | |

And the split is not random with respect to our panel:

| population | receptors on which NPxxY is defined | structures |
|---|---|---|
| application set (our 48) | **40 / 44** (91%) | 333 of 354 active, 243 of 256 inactive |
| calibration set (off-panel) | **117 / 155** (75%) | 419 of 611 active, 95 of 115 inactive |

**Of the 44 panel entries, 43 have Tyr at 5.58. Of the 155 off-panel entries, 121 do.**
The panel is enriched in exactly the receptors where the instrument is defined, which is
why nothing upstream ever noticed. Moving off-panel loses **212 of the 726 structures
outright** — not to a quality rule, but because the quantity does not exist on them.

The tilt axis has no such problem: **2×46 and 6×37 are present on 199 of 199 entries.**

Consequences, and they are not cosmetic:

- The two axes have **different domains of definition**, so the conjunction is undefined
  wherever the NPxxY axis is. `methods.tex:45` says "A prediction is called active only
  when both fire"; on 42 of 199 Class A receptors only one can ever fire. Nothing in
  Block A or Block B distinguishes *did not fire* from *could not be evaluated* — Block A
  ships `excl_E3_npxxy`, but the reference side has no equivalent.
- The calibration set cannot be "the full Class A structural population". It is the
  population **on which the instrument is defined**, and that has to be said in the
  Methods, not discovered by a referee.
- A CA-variant is available and is not affected: `d_npxxy_ca_ref` already exists as a
  column in `reference_set.blockb_pinned.csv`, needs no hydroxyl and no tyrosine, and
  would be defined on all 199. Whether to switch is **PI decision D1** (§6), and Aditya has **deferred it** — it does not block, and it is resolved when the calibration is actually built.

### 0.2 The build step is written, it runs, and it reproduces the shipped numbers

`redo/build/g0_measure_axes.py --selftest` measures both axes on the eight deposited
Class A entries this repo already holds and compares them against
`reference_set.blockb_pinned.csv` (`g0_selftest.txt`):

| PDB | receptor | NPxxY Δ | tilt Δ |
|---|---|---:|---:|
| 4LDE | ADRB2 | +0.0000 | +0.0000 |
| 6PT2 | OPRD | +0.0000 | +0.0000 |
| 5ZTY | CNR2 | +0.0000 | +0.0000 |
| 8GUR | CNR2 | +0.0000 | +0.0000 |
| 7JVR | DRD2 | +0.0000 | +0.0000 |
| 7NA7 | GHSR | +0.0000 | +0.0000 |
| 7F83 | GHSR | +0.0000 | +0.0000 |
| 5G53 | AA2AR | **+0.0106** | **+0.0266** |

**Seven of eight reproduce exactly, to 1e-4 Å, on both axes**, from GPCRdb numbering alone
with no hardcoded anchor table — and the UniProt anchor positions the script derives agree
with the pinned `anchor_positions` on all eight. So the numbering convention below is not
a proposal; it is the convention the campaign actually used, re-derived independently.

**5G53 is a real, small disagreement and it is ours to record, not to smooth.** The
measurement is deterministic: chain A, no alternate conformers, TYR at 197 and 288, LEU at
48 and 235, and the local `data/block_a/11_structures/confidently_wrong/5G53.cif` and a
fresh RCSB download give identical values. The 0.011 Å / 0.027 Å gap is in the shipped
reference value, not in the recomputation. It moves no call (3.72 vs 3.71 against a 9.08
cut; 18.12 vs 18.10 against 14.932) and belongs in the discrepancy record, not in the
blocker list.

### 0.3 Independence and power trade off directly, and total independence is unavailable

The rule "calibrate on receptors that will never be predicted on" has a cost that nobody
has priced. `g0_independence_ladder.csv`, all rows after the pre-declared filters of §5:

| rule | n | active | inactive | A:I | receptors | both-state receptors |
|---|---:|---:|---:|---:|---:|---:|
| **I1** off our 48 | **433** | 372 | **61** | 6.1:1 | 106 | 17 |
| I2 · I1 and not a redo-expansion receptor | 289 | 269 | **20** | 13.4:1 | 86 | **0** |
| I3 · I1 and not sharing a GPCRdb level-3 family with a panel receptor | 260 | 242 | **18** | 13.4:1 | 64 | 7 |
| I4 · I2 and I3 | 193 | 192 | **1** | 192:1 | 55 | 0 |

The inactive class is the binding constraint, and **the inactive signal lives almost
entirely in the 32 receptors `PANEL.md` proposes to add to the panel.**
> **CORRECTION 2026-09-12: it is 25 receptors, not 32** (`on_panel75` and not
> `on_panel48`, counted from `g0_calibration_structures.csv`); 20 of them survive to
> the F4 pool. The body figures beneath — 41 inactives from 17 expansion receptors —
> are correct and reproduce exactly. D-2026-09-12-e. Of the
61 inactives surviving every rule in §5, **41 come from 17 expansion receptors**; of the 20
that do not, **14 are OX1R alone**, and OX1R sits in the same GPCRdb level-3 family
(`001_002_023`) as OX2R, which is already on the panel. The remaining six — ACM5, ADA1B,
ADA2C, CCR7, CCR9, LGR4 — have exactly one inactive each and no active at all.

So the choice is forced and it is **PI decision D2** (§6): the panel cannot both absorb
the E-scope/E-B1 expansion and be calibrated independently of it.

---

# 1. The blocker, resolved

`redo/spec/PANEL.md` §9.1 found that E0.1 cannot simply be run:

> in `reference_set.blockb_pinned.csv`, `d_gpcrdb_tm6_tilt_ref` is populated on all 162
> rows and `d_npxxy_oh_ref` on only 64 … all 69 off-panel rows carry the tilt axis and
> *zero* carry the NPxxY axis.

Recomputed here (`g0_reference_axis_gap.csv`, and the figures agree with PANEL.md exactly):

| | rows | NPxxY populated | tilt populated |
|---|---:|---:|---:|
| pinned reference set | 162 | 64 | 162 |
| …on-panel | 93 | 64 | 93 |
| …off-panel | **69** | **0** | 69 |

Receptors with both axes measured in both roles: **28**, against the 40 the manuscript
claims. **98 rows need an NPxxY measurement made.**

**What the build step needs, and what it already has.** The pinned rows carry
`anchor_positions`, a JSON map of BW label → UniProt position. Across 162 rows it holds
`5.58` on 151 and `7.53` on 156; of the 98 rows needing a measurement, 87 already have a
5.58 anchor and 92 a 7.53 anchor recorded. **No row carries a 2.46 or a 6.37 anchor** —
the tilt axis was resolved by some other route that left no trace in the reference set, so
the build step derives all four anchors itself rather than half-trusting the table. It
does, and §0.2 shows it agrees with the table on every case tested.

**The blocker is therefore closed as a specification problem.** What remains is execution:
726 structures, no GPU, described in §4.

---

# 2. The calibration population, enumerated

## 2.1 The rule

> **A structure is a calibration candidate if and only if no ortholog of its receptor
> appears anywhere in the prediction panel.**

Species-collapsed, deliberately: calibrating on bovine rhodopsin while predicting on human
rhodopsin is not independence. Membership is tested against the union of the
species-collapsed `gpcrdb_proteins` entries and the `gpcrdb_slug` column of
`panel_systems.csv`, which is what makes the test total (some rows carry composite slugs
such as `opsd_bovin;opsd_human;opsd`).

This rule reproduces the catalogue's split exactly — 726 off-panel (611 active / 115
inactive) across 155 receptor entries, and 610 on-panel (354 / 256) across 44 — which is
the check that we are enumerating the same object E0.1 named.

## 2.2 The split

| | structures | active | inactive | A:I | receptor entries |
|---|---:|---:|---:|---:|---:|
| Class A with a state annotation | 1,336 | 965 | 371 | 2.6:1 | 199 |
| **calibration** (off our 48) | **726** | 611 | 115 | **5.3:1** | 155 |
| **application** (on our 48) | **610** | 354 | 256 | 1.4:1 | 44 |

Class A also holds **21 Intermediate** structures (§8) and 1 annotated "Other", excluded.

**Every PDB ID is enumerated in `g0_calibration_structures.csv`** — 1,357 rows, one per
structure, carrying `receptor_slug`, `state`, `species`, `method`, `resolution`,
`publication_date`, `transducer_type`, `ligand_functions`, `on_panel48`, `on_panel75`,
`role` (calibration / application) and every flag of §5. The file is the artefact to act
on; the tables in this document are projections of it.

Structure of the calibration set, which matters for how it may be analysed:

- 147 receptors, of which **25 have both states**, 113 are active-only and 9 inactive-only.
  A within-receptor paired analysis is available on 25 receptors and no more.
- 584 cryo-EM, 142 X-ray. Resolution runs 1.94–5.50 Å, median 3.00.
- 646 human, 37 mouse, 27 rat, and 13 others including 7 human-cytomegalovirus entries.

## 2.3 The resolution–state confound, which must be read before §5

| | n | X-ray | cryo-EM | median resolution |
|---|---:|---:|---:|---:|
| calibration active | 611 | 51 (8%) | 560 (92%) | 3.02 Å |
| calibration inactive | 115 | 91 (**79%**) | 24 (21%) | 2.90 Å |

Mann–Whitney U on resolution, active vs inactive: p = 0.0095.

**Method and state are almost perfectly confounded in this population**, so every
resolution rule is also a class-balance rule. It shows up immediately:

| resolution floor | n | active | inactive | A:I | both-state receptors |
|---|---:|---:|---:|---:|---:|
| ≤ 2.5 Å | 48 | 29 | 19 | **1.5:1** | 1 |
| ≤ 3.0 Å | 364 | 299 | 65 | 4.6:1 | 16 |
| ≤ 3.2 Å | 535 | 452 | 83 | 5.5:1 | 22 |
| ≤ 3.5 Å | 678 | 572 | 106 | 5.4:1 | 25 |
| no cut | 726 | 611 | 115 | 5.3:1 | 25 |

A tight floor does not clean the set; it silently re-weights it toward crystallographic
inactives. This is the reason the resolution rule is declared in §5 **before** the
balancing rule in §6 and not chosen alongside it.

---

# 3. The measurement spec

## 3.1 What is measured

```
d_npxxy_oh = | Y5.58:OH  -  Y7.53:OH |     Ballesteros–Weinstein labels,  hydroxyl atoms
d_tilt     = | 2x46:CA   -  6x37:CA  |     GPCRdb generic numbers,        alpha carbons
```

**Two numbering systems, and the difference is load-bearing.** The shipped column names
say so: `d_npxxy_y558_y753_oh` uses dotted BW labels, `d_gpcrdb_tm6_tilt_246_637_ca` says
*gpcrdb* and uses `x` notation. GPCRdb's `display_generic_number` carries both — `6.37x37`
splits into BW `6.37` and generic `6x37` — and **where a helix carries a bulge the two
diverge.** Matching the tilt anchors on the BW field would land on a different residue in
exactly the receptors whose TM6 geometry is most unusual. So NPxxY anchors are looked up on
the `bw` field and tilt anchors on the `generic` field.

`~/.ntfy-bridge/inbox/bw_numbering.d9c646af.py` ships `lookup_bw` and **no generic
equivalent**; `lookup_generic` in `g0_measure_axes.py` is the missing sibling and is the
only convention this work adds to the pipeline's. Everything else — the `Api` cache class,
the throttle, the retry ladder, the endpoints, `get_generic_numbers` — is that module's
behaviour, kept rather than improved on.

## 3.2 How generic numbering reaches a deposited structure

1. **GPCRdb entry → UniProt accession.** `/services/protein/<entry>/`. Needed because SIFTS
   is keyed by accession, and §3.3 explains why that matters more than it sounds.
2. **GPCRdb entry → generic numbers.** `/services/residues/extended/<entry>/`, the module's
   declared "ONLY SANCTIONED BW SOURCE". Returns UniProt sequence positions.
3. **UniProt position → `auth_seq_id`.** EBI SIFTS `uniprot_segments`, filtered to the
   receptor's own accession, applied **per segment** — a construct with an excised ICL3
   has two segments with different offsets and taking the first mis-numbers everything
   after the excision.
4. **Identity check, always.** 5.58 and 7.53 must be `TYR` with a modelled `OH`. A position
   that is not what it claims returns a refusal, never a number. This is
   `analysis/block_d/cifmeasure.py`'s rule and the reason that file was trusted.
5. **Alternate conformers.** Highest occupancy wins and the choice is recorded in the row.
   On a 2 Å structure two Tyr-OH rotamers can differ by more than the gap between the
   active and inactive NPxxY populations, so this is not a tie-break, it is a declared rule.

No hardcoded anchor table, no canonical offset, no panel-FASTA realignment shortcut —
those are audit findings #1 and #5 in the pipeline's own trail and they are not
re-introduced.

## 3.3 What goes wrong — four failure classes, all observed, none hypothetical

These are not risks imagined at a whiteboard. Each fired during the self-test or the
30-structure pilot, and the first two produced **wrong numbers**, not errors.

**(a) The fusion partner shares the auth chain.** 4LDE chain A carries T4 lysozyme
(P00720, UniProt 2–161, offset +865) *and* ADRB2 (P07550, UniProt 29–348, offset +1000).
BW 2×46 is UniProt 75, which falls inside **both** ranges. Taking the first covering SIFTS
segment lands on T4 lysozyme and returns **d(2×46, 6×37) = 62.34 Å** against a shipped
17.56 Å. 5ZTY does the same with its own fusion over 2–161: **44.14 Å** against 11.50 Å.
The fix is the accession filter, and the point to hold on to is the direction: **this bug
fires selectively on fusion constructs, which are 40 of 64 inactive references**
(`PANEL.md` §9). Silently, it would have corrupted the small side of the split and nothing
else.

**(b) SIFTS segment records are sometimes simply wrong.** For 7JVR, SIFTS reports one
segment, UniProt 1–443 at offset +145, when chain R plainly runs 34–441 in UniProt
numbering. For 7F83 it maps UniProt 252–342 onto auth 1111–1201 when the chain ends at
1111. Both cases refuse rather than lie — the identity check catches them — and both are
recoverable, because the deposited auth numbering *is* the UniProt numbering. The build
step therefore runs a **two-strategy ladder**: SIFTS first, identity numbering second, and
identity is accepted only when all four anchors pass the same residue-identity check. The
strategy used is recorded on every row. A number is never produced by a strategy that
could not prove it landed on the right residue.

**(c) The anchor is not the residue the axis assumes.** Dominant in practice. In the
30-structure pilot, 11 of 30 refused because 5.58 is not a tyrosine — ASN, HIS, ALA, SER,
PHE, CYS, ILE, GLN. §0.1 is that finding generalised to the whole population.

**(d) The anchor is not modelled.** Disordered loops and unresolved termini. 2 of 30 in
the pilot (`7X9Y` 7.53 absent; `6M9T` 5.58 absent). Recorded as a refusal with the reason,
never as a missing value.

**The pilot result, end to end** (`g0_pilot_measurements.csv`, 15 inactive + 15 active
drawn at seed 11 from the calibration set): **17 measured, 13 refused** — 11 for (c), 2 for
(d), 0 for (a) or (b) after the fixes. So the expected yield of the full pass is
governed by §0.1's conservation table, not by data quality, and the two are worth keeping
apart in the reporting.

One measured value in the pilot deserves a flag rather than a filter: `6RNK` returns
**25.59 Å** on the NPxxY axis, far outside any plausible Tyr–Tyr hydroxyl separation in a
folded 7TM bundle. It passes every identity check. Outlier screening on the measured
distribution is therefore a **declared step**, not an optional cleanup: see §5 rule Q7.

## 3.4 Output schema

One row per structure, written by `g0_measure_axes.py --from-csv … --out …`:

```
pdb_id, gpcrdb_entry, uniprot_acc, chain_used, numbering_strategy,
d_npxxy_oh, d_tilt,
pos_5_58, pos_7_53, pos_2x46, pos_6x37,        (UniProt positions used)
auth_5_58, auth_7_53, auth_2x46, auth_6x37,    (auth_seq_id actually read)
npxxy_note, tilt_note,                          (altloc / strategy provenance)
status                                          ("ok", or the refusal and its reason)
```

Column names deliberately match the campaign's reference-side convention
(`d_npxxy_oh_ref`, `d_gpcrdb_tm6_tilt_ref`) rather than the prediction-side one, because
these are reference measurements. Note for whoever joins them later: **the tilt column is
named differently on the two sides already** — `d_gpcrdb_tm6_tilt_246_637_ca` on prediction
rows, `d_gpcrdb_tm6_tilt_ref` on reference rows — and that is a pre-existing trap, not one
introduced here.

## 3.5 Tooling, and one thing the orchestrator must do

`gemmi` is **not installed** on this laptop (checked 2026-09-11); `biopython` 1.83 is, but
its `MMCIFParser` refuses some of our files (`figures/block_a/cifread.py:4`). The mmCIF
reader in `g0_measure_axes.py` is the same hand-rolled one `cifmeasure.py` and `cifread.py`
use, and it takes column order from **each file's own** `_atom_site` loop header, because
the order is not the same in every file and assuming one has already crashed this project.

`numpy` 1.24.4 sits against `scipy` 1.6.2 and emits a version warning on import; nothing in
the build step needs either, but anything that fits a GMM or an ROC will, and that pairing
should be resolved before the fitting stage rather than during it.

Network endpoints used: `gpcrdb.org`, `www.ebi.ac.uk/pdbe/api`, `files.rcsb.org` — all
reachable, all cached on disk under `redo/cache/structures/`.

> **Orchestrator action:** `redo/cache/structures/` will hold ~726 mmCIF files, on the
> order of 1–3 GB, and is entirely regenerable. It belongs in `.gitignore` beside
> `lit/pdfs/` and `figures/out/`. **This session does not edit `.gitignore`.**

---

# 4. What the build step costs

| item | count | note |
|---|---:|---|
| calibration structures to measure | 726 | 514 after the axis-definability gate of §0.1 |
| application structures to measure | 610 | the held-out arm of §7 |
| pinned reference rows needing NPxxY | 98 | of 162; `g0_reference_axis_gap.csv` |
| mmCIF downloads | ≤ 1,336 | ~1–3 GB, cached, resumable |
| GPCRdb `residues/extended` calls | 199 | one per receptor entry, **already run** — `g0_anchor_conservation.csv` |
| GPCRdb `protein/<entry>` calls | 199 | accession lookup, cached |
| SIFTS calls | ≤ 1,336 | one per structure, cached |
| RCSB metadata fetches for QC | 503 | 223 of the 726 are already in `panel_rcsb_cache.json` |
| coordinates held in this repo today | **0** | of the 726; 13 deposited entries exist on disk in total |
| GPU | **none** | |

`free*` in the catalogue's sense, and the catalogue's "budget days, not hours" is right —
the throttle alone (0.15 s between calls, ~4,000 calls) is a floor, and the download is
bandwidth-bound. It is resumable and idempotent: everything is cached on the natural key of
the resource, so an interrupted pass costs nothing.

---

# 5. Quality filtering — rules stated in advance

**Every exclusion here is a rule, applied to the whole population, never a judgement made
per structure.** They are applied in the fixed order below, and `g0_filter_ladder.csv`
records what each one removes. If any rule changes after a threshold has been fitted, the
fit is re-run from scratch and both fits are reported.

| # | rule | why | source |
|---|---|---|---|
| **Q0** | Class A, GPCRdb `state` ∈ {Active, Inactive}, receptor not on the panel | the population | §2.1 |
| **Q0b** | **NPxxY axis defined: Tyr at both 5.58 and 7.53** | the quantity does not otherwise exist | §0.1 |
| ~~**Q0c**~~ | ~~Active class restricted to GPCRdb activation degree = 100~~ **RETRACTED — see §5.1.** GPCRdb defines degree 100 as "in complex with a signaling protein", so the rule calibrates the active pole on partner presence. Not applied. | — | §5.1 |
| **Q1** | resolution ≤ **3.5 Å**, with 2.5 / 3.0 / 3.2 / 3.5 / 4.0 / none reported as a declared sweep | `khaleq2026hyaline` p.12 uses ≤4.0 Å X-ray / ≤4.5 Å cryo-EM; we tighten, and report the sweep because §2.3 shows the floor is also a balance rule | `khaleq2026hyaline` p.12 |
| **Q2** | drop structures whose GPCRdb state label is contradicted by their own ligand: labelled Active with antagonist-class ligands only and no transducer, or labelled Inactive while agonist-bound | §5.2 | `khaleq2026hyaline` p.9 |
| **Q3** | **arrestin-complexed structures are not admitted as Active** | §5.3 | `georgiou2025heterogeneity` p.15 |
| **Q4** | **fusion inside a measurement window excludes the structure** | §5.4 | `georgiou2025heterogeneity` pp.9, 16 |
| **Q5** | non-human orthologs **retained**; human-only run as a declared sensitivity arm | dropping them costs receptors we cannot replace | — |
| **Q6** | engineered-substitution cap: **declared, not yet enforceable** | §5.5 | `lee2026confornets` p.15 |
| **Q7** | outlier screen on the measured distribution, pre-declared bounds | §3.3, `6RNK` at 25.59 Å | — |

The ladder, on the calibration pool (`g0_filter_ladder.csv`):

| step | rule | n | active | inactive | A:I | receptors | both-state |
|---|---|---:|---:|---:|---:|---:|---:|
| F0 | Q0 | 726 | 611 | 115 | 5.3:1 | 147 | 25 |
| F0b | Q0b — NPxxY defined | **514** | 419 | 95 | 4.4:1 | 110 | 20 |
| F2 | Q1 — ≤ 3.5 Å | 483 | 395 | 88 | 4.5:1 | 109 | 20 |
| F3 | Q2 — label vs pharmacology | 434 | 373 | 61 | 6.1:1 | 106 | 17 |
| F4 | Q3 — arrestin | **433** | 372 | **61** | 6.1:1 | 106 | 17 |
| F5 | Q5 — human only *(sensitivity arm)* | 385 | 332 | 53 | 6.3:1 | 100 | 15 |

**Q4 and Q6 are not yet in the ladder and that is stated rather than hidden** — see §5.4
and §5.5. Both need the RCSB metadata pass of §4, and both will remove further structures.

## 5.1 A retracted rule, and the finding that replaces it

**Q0c — "restrict the Active class to GPCRdb activation degree = 100" — was adopted on
2026-09-11 and withdrawn the same day. It must not be reinstated.** Every filter count in
an earlier version of this file that ran through it (466 after F0c, 414 at F4) is void; the
ladder in §5 is back to the pre-Q0c numbers and `g0_calibration_set.py` carries the
retraction in a comment where the constant used to be.

### Why it was wrong

GPCRdb's own documentation (`lit/panels/cache/gpcrdb_activation_degree_definition.txt`,
from docs.gpcrdb.org/structures.html), verbatim:

> "For each class, **structures in complex with a signaling protein are set as the reference
> structures for the active state (100% degree activation)**. Subsequently, structures with
> a highly closed conformation are set as the reference structures for the inactive state
> (0% degree activation) **based on a maximum distance between 2x46 to 6x37** … maximum
> distances are **11.9 Å, 13 Å, 14.5 Å, 13 Å for classes A, B, C, and F**."

**"Activation degree = 100" means "a transducer is bound."** It is not an independent
geometric criterion, and the justification attached to it — somebody else's published cut on
an independent graded annotation, decided before anyone looks at geometry — was false for
the active pole.

Calibrating the active pole on partner presence, and then using the resulting predicate to
test whether supplying a Gα co-input drives the active state, is **circular**. It is the
same circularity `methods.tex:95` concedes and E0.1 exists to escape, relocated from the
agonist-only question into the rule proposed as its fix.

**Checked here rather than taken on trust** (`g0_calibration_set.py` prints this on every
run): of 807 degree-100 Class A actives, **795 (98.5%) carry a transducer**; of the 158
below 100, **155 (98.1%) carry none**.

**So the two results reported as corroboration were one signal counted twice.** "Q0c
subsumes the Active half of Q2" and "the external annotation and transducer presence agree
on ~97% without either deriving from the other" are not two instruments agreeing. The
agreement is *definitional*. I reported it as validation and it was not; that is my error,
recorded here rather than quietly dropped.

### The finding that replaces it — only one of four cells is clean

The inactive pole **is** genuinely geometric: a published, reimplementable, partner-
independent maximum Cα–Cα distance. But it is a distance **on 2×46–6×37**, which is *our
tilt axis*. GPCRdb's own text confirms the identity — its "TM6 tilt" descriptor is "the
distance between the Ca atoms for the residues 2x46 and 6x37". Our second axis **is**
GPCRdb's TM6 tilt measure, and the column we consume is named `d_gpcrdb_tm6_tilt_246_637_ca`
accordingly.

So the entanglement is not one thing, it is a 2×2:

| our axis | vs GPCRdb's **active** pole (= a transducer is bound) | vs GPCRdb's **inactive** pole (= d(2×46,6×37) ≤ 11.9 Å) |
|---|---|---|
| **tilt** d(2×46, 6×37) | circular — partner presence is our independent variable | **circular — the same atom pair, the same measurement** |
| **NPxxY** d(Y5.58, Y7.53) | circular — partner presence | **independent — different helices, different atoms** |

**Exactly one cell of four is clean.** The recommendation to "adopt the inactive pole as-is"
is safe for the NPxxY axis and circular for the tilt axis, and the difference has to be
carried per axis rather than as a single posture.

### What the data says about the tilt entanglement, stated proportionately

A 30-structure pilot suggested something stronger than is true, and running it down first
is the point. In the pilot the ten inactive-labelled structures spanned **11.00–12.28 Å** on
the tilt axis — a 1.28 Å spread straddling the 11.9 Å line — against 15.24–18.38 Å for the
eight actives. That looks like a hard cut.

**On the 162 pinned references, which we already hold, it is softer than that.** Inactive
tilt values run 10.98–17.25 Å (median 12.24, sd 1.15); **only 20 of 67 are at or below
11.9 Å** and 16 are above 13.0 Å. So the 11.9 Å rule selects GPCRdb's inactive *reference*
set, and every other structure's Inactive label is assigned by proximity to those references
in a Cα-distance space that includes this pair — entangled, not thresholded.

The cleanest empirical statement is the one-sided one: **0 of 95 active references fall at
or below 11.9 Å.** The line is a perfect separator in the direction GPCRdb constructed it,
which is what one expects of a constructed pole and not evidence about receptors.

For contrast, on the NPxxY axis the same references scatter far more widely — active
2.84–16.75 Å (sd 3.22), inactive 9.35–24.62 Å (sd 3.84) — consistent with an axis that had
no hand in the labelling.

### The revised recommendation

Adopt `paajanen2026activation`'s anchor convention, **stated openly as an anchor choice
rather than laundered through a percentage**:

- **active pole:** ternary complexes — "bound to both G protein and agonist";
- **inactive pole:** "G protein-free and antagonist-bound";
- fit the cut **unsupervised, with bootstrap**, per §6.2;
- report agonist-only and Intermediate structures as **distributions**, not assignments.

paajanen's active anchor has the same partner-presence property. The difference that matters
is that it is *declared as an anchor* and its index is fitted without labels, so the
dependence is visible in the method rather than hidden inside a number that looks like a
measurement.

### The limitation to write into the manuscript before a referee writes it

> **Every published active-state reference set in this field is defined by partner presence.
> Our predicate therefore cannot be validated against those labels without circularity.**

That sentence is a contribution, not a weakness, and it is the honest frame for §7's
held-out arm. It also bounds E0.2: a concordance check against GPCRdb's annotation (§9)
measures agreement with a partner-presence rule at the active pole and with a tilt-distance
rule at the inactive one — which is worth reporting, and is not independent validation.

### Three properties of the degree number, recorded so nobody reuses it

1. **It is min–max normalised within class**, so it is a relative rank that **rescales as
   GPCRdb grows**. A structure's degree today is not the degree `lee2026confornets` selected
   on, which also weakens any attempt to reproduce that paper's selection exactly.
2. **GPCRdb's own text may have its sign inverted.** The activation score is defined as
   "substracting the mean distance to the inactive-state structures from the mean distance
   to the active-state structures", which read literally gives a *higher* score to
   structures *further* from the active set. **Do not build on the score's direction without
   checking it against a known active/inactive pair.**
3. **The data is fine; only the meaning was circular.** `redo/inputs/panel_gpcrdb_degree.csv`
   (1,716 rows, scraped by the panel session, zero state disagreements against the frozen
   snapshot) is kept, and the degree columns are still emitted into
   `g0_calibration_structures.csv`. lit reports the degree is exposed by none of GPCRdb's 53
   API endpoints, so this scrape is the only copy we have and is worth keeping. It is
   carried as **data, not as a rule**.

### D3 is therefore reopened

The agonist-only question — do transducer-free, agonist-bound structures count as Active? —
goes back to being **an open PI decision** (§6.3, D3). It cannot be settled by GPCRdb's
degree, because that number answers "is a transducer bound?", which is the question D3 is
asking, not an independent answer to it.

What survives from the retracted section and is still worth having is the **physical**
evidence, which was never the circular part:

- `paajanen2026activation` p.1: *"Agonist binding shifts this conformational ensemble
  towards the active state but does not fully stabilize it. Instead, a stable active state
  is only established upon G protein binding."* And: *"the apo form … exists in both the
  inactive and active states, and **the agonist-bound form also exists in both**."* So
  agonist-only structures are **bimodal on the coordinate being calibrated**.
- `georgiou2025heterogeneity` p.3697: agonist-only class A receptors "adopt an
  **intermediate active conformation**"; p.3703, A2AR TM7 with the full agonist NECA is
  **49% inactive / 37% intermediate / 14% active**.
- `vo2026fiducials` pp.8–9 is the counter-evidence: BI-167107 *"induces almost complete
  outward movement of TM6 even in the absence of G-protein"*, α5 adding under 1 Å. The
  reconciliation stands — vo reports a **deposited structure**, georgiou reports **ensemble
  populations**, and a deposited structure is the conformer that crystallised, not the
  ensemble mean.

**And the move to avoid is unchanged, and now has no substitute:** do not exclude
agonist-only structures because our own thesis says an agonist alone does not activate.
Q0c was offered as the non-circular route to that exclusion and it was not one. D3 must be
decided on the physical evidence above, declared in advance, and reported both ways.

## 5.2 Q2 — the state label disagrees with the structure's own pharmacology

`g0_label_conflicts.csv`, 98 rows:

| conflict | Class A total | in the calibration set |
|---|---:|---:|
| labelled **Active**, antagonist-class ligand only, no transducer | 25 | **25** |
| labelled **Inactive**, agonist-bound | 73 | 34 |

**Both classes are removed by Q2 itself.** An earlier version of this section said rule
Q0c subsumed the first of them; Q0c is retracted (§5.1) and Q2 is doing the work alone.
The apparent subsumption was definitional — GPCRdb's degree encodes transducer presence, and
24 of these 25 structures have no transducer — not a second instrument agreeing.

The first class is the worrying one. CLTR1 (`6RZ4`, `6RZ5`), CLTR2 (`6RZ6`–`6RZ9`), AGTR2
and PAR2 supply antagonist-bound crystal structures with no transducer in the assembly that
GPCRdb annotates **Active**. Whatever curatorial reasoning produced those labels, they are
not the same object as a Gα-complexed agonist-bound active state, and 25 of them sit in a
calibration set whose entire inactive class is 115.

This is not our discovery and the corpus is blunt about it. `khaleq2026hyaline` assigns
labels from "GPCRdb annotations, structural criteria, and ligand binding status" (p.12) and
then finds its own classifier "correctly identifies these as geometrically closer to the
inactive state, even though they are annotated as active based on ligand pharmacology"
(p.9) — 15 of 39 of its errors. `paajanen2026activation` p.3 reports structures "whose
state of activity was originally interpreted incorrectly", and attributes the cause to
"experimental artifacts, construct design, or nonphysiological stabilization methods"
(p.6). Neither applies a filter for it. Q2 is ours.

**Corollary that has to be stated somewhere the referee will see it:** the recalibrated
instrument is only as independent as GPCRdb's labels, and Q2 mitigates that without
removing it. E0.2's disagreement rate (§9) is the honest way to bound what remains.

## 5.3 Q3 — arrestin, audited across the whole population

The coordinator flagged that `khaleq2026hyaline`'s active-label rule counts
arrestin-coupled structures as active, and asked whether our reference set inherits it.
Re-derived here rather than taken on trust, joining every Class A structure to
`signalling_protein.type` in the snapshot:

| population | state | n | G protein | arrestin | none |
|---|---|---:|---:|---:|---:|
| calibration | Active | 611 | 526 | **4** | 81 |
| calibration | Inactive | 115 | — | — | 115 |
| application | Active | 354 | 260 | **8** | 86 |
| application | Inactive | 256 | — | — | 256 |

**The blast radius is small: 4 structures in the calibration set** — `6PWC` and `6UP7`
(NTR1), `7R0C` (V2R), `7SRS` (5HT2B) — and **no receptor's active class is defined solely
by arrestin coupling**, so Q3 removes structures and costs no receptor.

**One correction to the coordinator's check, and it matters for which column is consumed.**
ACM2's `strict_active_pdb` is indeed `6U1N`, an arrestin complex (`arrb1_rat`, 4.0 Å
cryo-EM). But ACM2's `our_active` and `gdb_active` are both `7T94`. Across the 48 panel
receptors the `our_active` reference picks are **42 G protein, 6 no transducer, zero
arrestin**. So the arrestin exposure is real in the strict-ConfoRNets column and absent in
the column the campaign actually used. Both facts should be recorded; the mechanism the
coordinator identified is right, its incidence on our references is zero.

**Why Q3 excludes rather than admits.** `georgiou2025heterogeneity` p.15 has β-arrestin and
GRK directing to distinct, non-Gs active states, with β-arrestin-biased agonists acting on
**TM7 rather than TM6** — a difference that runs along precisely the axis split our two
measurements use. An arrestin-complexed structure in the active class would be expected to
pull the TM6 cut down while leaving NPxxY roughly put, which is a loosening on the majority
side of the imbalance and in the direction that most flatters a partner-driven result. At
n = 4 the effect is negligible; the rule is declared anyway, because a rule declared at
n = 4 is a rule, and a rule adopted later at n = 40 is a choice.

**The 81 no-transducer actives are the larger and less examined question.** By ligand
function they are 38 agonist, 19 antagonist, 7 apo, 4 inverse agonist, 4 partial agonist,
3 allosteric agonist and 6 mixed. Q2 removes the antagonist-class ones. The agonist-only
ones are a real and defensible category — `methods.tex` already knows it, and the reference
audit counts 2 "agonist-only-no-partner" rows — but they are a *different kind of active*
from a Gα-complexed structure, and **seven receptors have no other kind**: `ackr3`,
`agtr2`, `cltr1`, `cltr2`, `par2`, `q08bg4`, `q80km9`. Whether to keep them is **PI decision D3** (§6.3), which was briefly thought settled by
GPCRdb's activation degree and is not: that number encodes transducer presence, so it
answers D3's own question back to it (§5.1).

## 5.4 Q4 — fusion inside a measurement window

This is the exclusion with the sharpest literature behind it and the one we cannot yet
apply.

> "the effect of T4L linked to IL3 of β2AR … is to cause the population of **only active
> TM6 conformations independent of the efficacy of bound ligands**"
> — `georgiou2025heterogeneity` p.16

and a possible artefactual broken ionic lock in A2AR `3PWH` at p.9. `lee2026confornets`
p.15 strips "ICL3 and any fusion proteins inserted, as well as helix 8" from inactive
structures without saying why; this is why.

**The direction is what makes it urgent.** A fusion-bearing inactive reference with a
forced-active TM6 does not add noise — it drags the cut in one direction, and it does so
from the small side of a 5.3:1 split, which is the worst place in the population to take
contamination. §0.3's independence ladder and §2.3's resolution confound both say the same
thing from different angles: the inactive class is where this instrument is fragile.

**What the repo already holds, and what it does not.** The concept exists:
`data/block_a/02_references/reference_metadata.csv` carries `fusion_in_tilt_window` (True
on 16 of 168) and `fusion_in_npxxy_window` (True on 11 of 168) — exactly the right
predicate. It exists for the 168 Block A references and for nothing else.
`panel_reference_qc.csv` carries `fusion_in_receptor_entity` for 962 candidates, 223 of
which are in the calibration set. **For the other 503 the flag has to be computed**, and
the SIFTS segment structure the build step already retrieves is the clean way to do it: a
second accession inside the receptor's auth chain *is* a fusion, and comparing its UniProt
span against the anchors' positions gives "in the window" directly. That is a small
addition to `g0_measure_axes.py`, not a new job, and it should land before the fit.

**Pre-declared rule, effective when the flag exists:** a structure is excluded if a fusion
partner is inserted within the span between 2×46 and 6×37, or between 5.58 and 7.53, in
the receptor's own sequence. Fusions at the N- or C-terminus outside both windows do not
exclude. Exclusion is on window overlap, not on the presence of a fusion, because
excluding every fusion construct would remove 40 of 64 inactive references and there would
be no inactive class left.

## 5.5 Q6 — the engineered-substitution cap, and why it is declared but not enforced

`lee2026confornets` p.15 retains pairs "where both structures contained at most one
mutation", and that is the natural rule to adopt. We cannot yet apply it honestly:

- `data/block_a/02_references/reference_metadata.csv` has an
  `engineered_mutation_count` column that is **empty on all 168 rows**.
- RCSB's `pdbx_mutation` is the only machine-readable source and `methods.tex:303`
  demonstrates it is empty for ten of fifteen verified mutants. `PANEL.md` §9.2 says every
  `mutN` count in that document is a **floor**.
- The method that works is `analysis/verify_partner_chains.py`'s — align the deposited
  sequence against canonical UniProt — and running it over the calibration receptor chains
  is its own `free*` job.

So Q6 is declared now with its threshold (**≤ 1 engineered substitution in the receptor
entity**) and marked **not enforceable today**. Reporting a cap we did not apply would be
worse than reporting no cap. Note that `hilger2020gcgr` p.2 treats freedom from
thermostabilising mutations as what makes a structural comparison valid, so this is not a
cosmetic filter.

## 5.6 The coverage rule that does not transfer, and why it is not applied

`khaleq2026hyaline` p.12 requires that a structure "contained at least 80% of the canonical
transmembrane domain resolved". `redo/inputs/panel_gpcrdb_degree.csv` carries a `pct_seq`
column, populated on all 1,357 rows, median 73% — so an earlier draft of this file was wrong
to say no coverage data existed. It does.

**It still cannot be used as khaleq's rule, and the reason is a like-for-like problem.**
`pct_seq` is coverage of the **whole UniProt sequence**, not of the transmembrane domain.
GPCR constructs routinely delete long N-termini, C-termini and ICL3 without touching a
single transmembrane residue, so `pct_seq` penalises exactly the constructs khaleq's rule
was designed to keep. Applied at the end of the ladder it is destructive:

| `pct_seq` floor | n | active | inactive | receptors | both-state |
|---|---:|---:|---:|---:|---:|
| none | 433 | 372 | 61 | 106 | 17 |
| ≥ 60% | 392 | 339 | 53 | 94 | 14 |
| ≥ 70% | 319 | 278 | 41 | 78 | 11 |
| **≥ 80%** | **122** | 119 | **3** | 37 | 1 |

At khaleq's own threshold the inactive class falls to **three structures**. That is not a
quality filter, it is a construct filter wearing one.

**So no `pct_seq` rule is applied.** The coverage question that actually matters for this
instrument is anchor-specific, not global, and the build step already answers it exactly:
all four anchors must be modelled, or the row is a refusal with its reason (§3.2, §3.3d).
That is the right coverage test for a four-atom measurement, and it is already enforced.

## 5.7 Two things this section cannot screen, stated as unresolved

1. **Register.** `6E67` is the documented case — right state, wrong register — and no
   metric we hold catches it. The identity check catches a *shifted* anchor but not a
   locally mis-threaded backbone that keeps the right residue at the right number.
2. **Receptor–receptor chimeras.** `7LD3`, the current active reference for AA1R, is
   deposited as "Chimera protein of Muscarinic acetylcholine receptor M4 and Adenosine
   receptor A1" (`PANEL.md` §9). GPCRdb assigns it to `aa1r_human` and the CFTR-class
   check found no other. A chimera whose TM5/TM6 come from a different receptor is a
   structure on which BW numbering is coherent and the *identity* is not.

---

# 6. The imbalance decision — and a disagreement worth having

**This section must be settled before any threshold is fitted.** After the §5 filters the
calibration set is **372 active against 61 inactive, 6.1:1** (before them, 611 : 115 =
5.3:1). The application set is 354 : 256 = 1.4:1. The two populations do not have the same
class prior, and no rule makes that go away.

## 6.1 The candidate rules, and what each implies

| rule | what it does | implies |
|---|---|---|
| **A · prevalence-weight** | fit on the pool as it stands | the threshold inherits the PDB's deposition history — which receptors got solved with a G protein bound — as if it were a prior on activation. It is not. |
| **B · equal-weight by class** | reweight to 1:1 | the cut sits where the two class densities cross. Defensible, and it is the one thing that makes calibration and application comparable, since their priors differ. |
| **C · matched sampling** | pair each inactive with a resolution- and method-matched active | directly attacks §2.3's confound. At 61 inactives it yields ~122 structures; power is low and the discarded actives carry information. |
| **D · Youden on balanced classes** | maximise sensitivity + specificity − 1 after reweighting | B plus an explicit objective. Reports an operating point rather than a crossing. |
| **E · unsupervised mixture** | 1-D two-component GMM per axis, no labels consumed | §6.2 |

**DECIDED (§ status, top of file): the anchors and the fit are settled; only the weighting
is still open as D4.** The active pole is ternary complexes and the inactive pole is
antagonist-bound with no transducer — `paajanen2026activation`'s convention, adopted as an
anchor choice and stated as one. The cut is fitted **unsupervised with bootstrap**, and the
**mixing weights are reported alongside the boundary**. Agonist-only and Intermediate
structures are **reported as distributions and never assigned to a pole**.

**Still open (D4): the weighting for the reported cut.** Recommendation stands at **B as
the headline, with A, D and E reported** — B because the application set's prior differs
from the calibration set's (1.4:1 against 6.1:1), so a prevalence-weighted cut is
calibrated for a population we will never grade; A because a reader will ask; D because it
names an operating point; E because §6.2.

Whatever is chosen, the fit must be **grouped by receptor**: 147 receptors supply 726
structures, 113 of them active-only, so a pooled ROC confounds receptor identity with
state and a leave-one-receptor-out estimate is the only honest one. This is separate from
the balancing rule and is not optional.

## 6.2 On the claim that an unsupervised fit dissolves the problem — it does not, and it is
still worth running

The coordinator's position, from lit: `paajanen2026activation`'s cut is the boundary of a
two-component 1-D GMM fitted on PC1 **without labels**, published as G_CA = −1.72 ± 0.44
with 10,000 bootstrap resamples (p.4, pp.10–11), and "an unsupervised density fit has no
class prior to declare", so the imbalance stops being a degree of freedom.

**Half of this is right and the important half is not.** A two-component mixture fits
**mixing weights** π and 1−π along with the component parameters, and on a 6:1 population
those weights are fitted to the deposition record. The decision boundary of a
two-component GMM depends on the mixing weights — that is what makes it a *decision*
boundary rather than an intersection of two densities. So the procedure does not remove the
class prior; it **estimates it from the PDB and then stops asking**. Under this project's
own rule — every threshold statable in advance — that is a regression, not an improvement:
rule A at least declares the prior it is using.

There is a second, sharper problem at our n. The minority class is **61 structures across
17 both-state receptors** after filtering, with per-receptor counts from 1 to 14. A 1-D
two-component GMM on that will not reliably recover a minority component at all; it is more
likely to split the majority. The coordinator anticipates this — "report the fitted mixture
weights alongside the bootstrap CI" — and reporting them is exactly right; what follows
from it is that E is a **cross-check, not the headline**.

**So: run E, and pre-declare it as a concordance check against B.** Concretely — per axis,
a two-component 1-D GMM with the mixing weights reported, k = 2 asserted (as paajanen
asserts it, with no BIC/AIC selection, p.10) and the bootstrap CI from 10,000 resamples for
comparability. If E's boundary falls inside B's bootstrap CI, that is a strong sentence.
If it does not, that is a more interesting one. Neither may be chosen after seeing which
answer we prefer, which is why both are named here.

**And the coordinator's framing of the contribution is right and should be kept.**
paajanen's leakage is in the **axis**: PC1 was selected from the decomposition "based on
our previous observation … which shows that the first component is able to distinguish
active GPCR structures bound to G protein from inactive ones" (p.10), i.e. the labels
chose the coordinate. We pre-specify both axes from biology — the YY-lock
(`georgiou2025heterogeneity` p.24) and TM6 outward movement (`hilger2020gcgr` p.3) — and
fit only the cut. **Their defect is our contribution, and it should be said in one sentence
in the Methods.**

## 6.3 The PI decisions, each with its consequence

| # | decision | options | consequence |
|---|---|---|---|
| **D1** *(deferred — Aditya, 2026-09-11: does not block, resolve when the calibration is actually built; do not spend on it now)* | keep `d(Y5.58 OH, Y7.53 OH)`, or switch the NPxxY axis to the CA–CA variant | (a) keep OH — 42 of 199 Class A receptors are unevaluable, calibration set 726 → 514 | the instrument stays as published and as already measured on 64 rows, and the Methods must state the domain of definition |
| | | (b) switch to `d_npxxy_ca` — defined on all 199 | the axis becomes class-wide, the calibration set recovers 212 structures, and **every published number on this axis changes**; the column already exists on references (`d_npxxy_ca_ref`) and on Block B prediction rows (`d_npxxy_y558_y753_ca`) |
| | | (c) report both, headline OH, CA as the coverage arm | costs one extra column and no inference; my recommendation |
| **D2** | expand the panel to the 32 E-scope/E-B1 receptors [**25**, corrected 2026-09-12 — see D-2026-09-12-e], or reserve them for calibration | (a) expand — calibration inactives fall 61 → 20 and **both-state receptors fall to zero** | E0.1 becomes a between-receptor fit with no paired evidence |
| | | (b) reserve them — the panel stays at 48 | the expansion in `PANEL_EXPANSION_CLASS_A.md` does not happen |
| | | (c) split: expand onto the actives-rich expansion receptors, reserve the inactive-rich ones (`nk1r` 6, `oprm` 4, `ntr1` 4, `5ht2a` 4, `c5ar1` 3, `acm3` 3, `pd2r2` 3, `ccr2` 3, `drd4` 3) | the list is in `g0_calibration_set.py`'s "inactive contributors" output; recommended, and it has to be decided **before** either job starts |
| **D3** *(reopened — the rule that briefly closed it is retracted, §5.1)* | admit agonist-only, no-transducer structures as Active | (a) admit — status quo, 81 structures | "active" means two different things inside one class, and `paajanen2026activation` p.1 says agonist-bound structures are bimodal on this very coordinate |
| | | (b) exclude — 7 receptors lose their entire active class | supported by `georgiou2025heterogeneity` p.3697/p.3703 (agonist-only = intermediate active; A2AR TM7 with NECA is 14% active), opposed by `vo2026fiducials` pp.8–9 |
| | | (c) admit, flag, report the cut both ways | recommended; and **it may not be decided by appeal to our own thesis**, nor by GPCRdb's degree, which encodes partner presence |
| **D4** | the balancing rule | A / B / C / D / E of §6.1 | B headline, A+D+E reported — recommended |

---

# 7. How the result is validated

**The sentence a referee cannot argue with is a held-out one, and we are in a position to
write a stronger one than anything in the corpus.** Both published GPCR state instruments
hold out by **deposition date only** — `paajanen2026activation` 1006 train / 345 held out
with no calendar cutoff stated (p.10); `khaleq2026hyaline` pre-2023 n = 1,312 / 2023–24
n = 278 (p.4). **Neither splits by receptor**, and khaleq's own limitations section names
that as its gap. A receptor-disjoint calibration is new.

Reported, in this order:

1. **Separation on the calibration set**, per axis and jointly: ROC and AUC with a
   **leave-one-receptor-out** grouping, the fitted cut, and the bootstrap CI (10,000
   resamples, matching `paajanen2026activation` pp.10–11 so the two are comparable).
2. **The threshold's sensitivity** to the resolution floor (the §2.3 sweep) and to the
   balancing rule (all of §6.1's options on one axis of one plot). If the cut moves more
   across those than the bootstrap CI, the CI is not the uncertainty that matters and the
   sweep is the result.
3. **Where it fails**, structurally, not statistically: the receptors and the construct
   classes on which the two axes disagree. A structure satisfying one rule and not the
   other is "the case a conjunction is meant to catch" (`methods.tex:45`), so the
   disagreement set is a finding rather than an error rate.
4. **Held-out performance on the 610 panel structures.** Fitted off-panel, applied
   on-panel, never refitted. This is the number that replaces the current derivation-set
   figure, and the comparison is the point: `results.tex:11–18` reports 159 of 168 reference
   rows returning the expected call while conceding "This is a derivation-set figure, not a
   held-out one". `lit/analysis_review/block_a_independent_review.md:32` (N-7) further shows
   9 of those 168 are `missing_axis` and are being counted as passes, so the honest current
   figure is 150 of 159 evaluable. **The held-out number replaces both.**
5. **The comparison against the old thresholds**, on the same rows: how many calls change
   at 9.08 → the new NPxxY cut and 14.932 → the new tilt cut, and which arms move. Note
   that 9.08 is itself already a known truncation of 9.082 that "changes the call for one
   borderline row" (`methods.tex:260`), that Block B's check B20 **fails** on exactly this
   (`analysis/block_b/verify_claims_results.json:315`), and that `159.95` has **no
   automated check at all** (`analysis/NUMBER_REGISTRY.md:323`, below the "NOT covered"
   header).

**The threat to this design, stated rather than discovered later.** Receptor-disjoint
splitting buys independence of identity, not of behaviour: `mattsson2026leakage` p.1 —
"splitting by protein-sequence identity is **inherently insufficient** to prevent data
leakage due to 'target mirroring'". §0.3's I3 row is the measurable version of this — a
paralogy-strict rule costs 173 further structures and 43 receptors — and OX1R is the worked
example, supplying 14 of the calibration set's inactives while sitting in OX2R's own
level-3 family. The honest posture is: report I1 as the headline, report I3 as the
sensitivity arm, and say in one sentence that neither is proof against target mirroring.

**A provenance gap that §7.5 depends on and that nobody can close from this repo.** The
80 tier-1 rows the current thresholds were fitted on are **not identified by any file** —
`analysis/block_a/DATA_REQUESTS.md:137` asks "Which 80 rows are they?" and answers
"No file identifies them." The only 80-row file, `data/block_b/09_references/reference_audit.csv`,
carries the literal placeholder `"X-ray or cryo-EM (schema lacks explicit method column)"`
in its `method` column on all 80 rows and `"not tracked in reference_set schema"` in
`resolution`, so no tier rule can be checked against it. The script that produced the
thresholds, `scripts/derive_per_class_thresholds.py`, is requested at
`redo/protocol/BLUEPRINT_REQUEST.md:834` and **is not in this repo** — there is no
`scripts/` directory. So item 5 can report *that* the calls change and *by how much*, but
not *why the old cut sat where it did*. That is an upstream ask, not a Group 0 job.

---

# 8. E0.3 — what n = 21 can and cannot conclude, decided in advance

The catalogue offers 21 Class A Intermediate structures as a third state. **They are 21
structures and 6 receptors** (`g0_intermediates.csv`):

| receptor | n | on our 48 | on the expanded 75 |
|---|---:|---|---|
| 5HT2B | **8** | no | no |
| NTR1 | 4 | no | **yes** |
| ADRB2 | 3 | **yes** | yes |
| MC4R | 3 | no | no |
| MRGRD | 2 | no | no |
| ACKR1 | 1 | no | no |

18 are off our 48; only 14 are off the expanded 75. One receptor supplies 38% of them.

**And they are a residual class, not a curated one.** GPCRdb assigns state by proximity to
its two constructed reference sets: close to the inactive references → Inactive, close to
the active references → Active, and *"if both are not the case then the structure is defined
as intermediate"*; a further escape hatch says *"when an unlikely conformation is
encountered its state is defined as other"*
(`lit/panels/cache/gpcrdb_activation_degree_definition.txt`). So "Intermediate" is **what is
left over when neither pole claims a structure** — and since the active pole is
transducer-bound structures and the inactive pole is a 2×46–6×37 distance cut, the residue
is defined by those two choices rather than by any positive criterion. That materially
weakens what E0.3 can conclude: a structure landing between our two cuts would be agreeing
with a *leftover*, not with an independent annotation of an intermediate state.

**Declared in advance, before measuring:**

- With 6 receptors and one contributing eight structures, **no rate computed over the 21 is
  a rate over intermediates** — it is a rate over 5HT2B with five receptors of context. Any
  reported fraction is reported **per receptor**, never pooled.
- The claim the design can support is **existence and placement**: whether intermediate-
  annotated structures fall between the two cuts on both axes, on the receptors where they
  exist. That is a statement about the instrument's expressive range and it does not need n.
- The claim it **cannot** support is that a middle band generalises across Class A, or any
  three-state rate. `georgiou2025heterogeneity` is the reason to want it — Class A
  receptors "can exist in three different conformational states … according to a
  multistate, rheostat-like model, instead of a binary (on/off) switch model" (p.6) — and
  also the reason 6 receptors cannot settle it, since the same review has the TM6 and TM7
  ladders correlated but not identical (p.9) and receptor-dependent (pp.7–8).
- If the 21 **scatter** rather than sit between, that is reported as-is. It bounds what the
  instrument can express, which is the stated purpose of E0.3.
- Because the class is residual, **agreement is weak evidence and disagreement is strong**.
  If intermediates land between our cuts, that is consistent with them being whatever the
  two poles did not claim. If they land *on* a pole, GPCRdb's proximity rule and our two
  distances disagree about the same structures, which is a reportable fact about both.

`paajanen2026activation` dropped intermediates — "Structures reported as 'intermediate' or
'other' have been ignored because their number is too low to be distinguished from the
graph" (p.2) — and **never reports the count**. So scoring them through a fixed predicate is
genuinely open, as the catalogue says, and it is open at n = 6 receptors.

---

# 9. E0.2 — the independent cross-check, with one arm removed before it starts

The catalogue proposes concordance against (a) GPCRdb's own annotation, (b) the PIF
connector, (c) `paajanen2026activation`'s coordinate.

**(c) cannot be run, and the reason should be stated as a finding rather than a failure.**
The lit pass found no weight vector, no mean-coordinate vector, no retained generic-number
list, no residue count, no superposition convention, no URL, no repository and no
data-availability statement in the paper. The tool is described as "openly available"
(p.3) and is not locatable. **`G_CA > −1.72` cannot be evaluated on any structure today.**
That is worth a sentence in the manuscript: the nearest published instrument to ours is not
reimplementable from its own description. `khaleq2026hyaline` is in the same position for a
different reason — its decision threshold is **never stated**, inferable only as 0.5 from
a passing remark about misclassifications "near the decision boundary (mean confidence:
0.58)" (p.9).

**(a) and (b) run, on the measurement pass E0.1 is already doing.** Report the
disagreement rate between the geometric predicate and GPCRdb's Active/Inactive annotation
on the calibration set, and the same for the PIF connector as a third geometric axis. No
study in the corpus reports such a rate; `intro.tex:325–332` already says so.

**The caution that bounds it.** `paajanen2026activation` **excluded arrestins** —
"Arrestins have not been included in the analysis because there is not enough data to
influence the graph" (p.2, Fig. 1 caption). So **no arrestin arm anywhere in this project
can be concordance-checked against paajanen**, whether or not (c) ever becomes runnable.
Under Q3 we exclude arrestin structures from calibration anyway, which makes the two
instruments' scopes agree on this point — but a future arrestin-finger-loop arm (E7.6) has
no external referent and should be told so in advance.

---

# 10. E0.5 — the class B and class F instrument

Per-class census from the snapshot (`g0_class_variants.csv`):

| class | structures | active | inactive | intermediate | receptors | both-state | **off-panel inactives** |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 1,358 | 965 | 371 | 21 | 188 | 65 | 115 |
| **B1** | 148 | 128 | **19** | 1 | 16 | 5 | **2** |
| B2 | 34 | 32 | **2** | 0 | 9 | 2 | 2 |
| C | 115 | 47 | **58** | 10 | 13 | 7 | **58** |
| **F** | 34 | 20 | **14** | 0 | 8 | 3 | **1** |
| T2 | 18 | 16 | 2 | 0 | 2 | 1 | 2 |
| O1 / O2 / D1 | 9 | 8 | 1 | 0 | 7 | 1 | 1 |

**What is possible, class by class:**

- **Class A.** Calibratable off-panel, at the cost §0.3 prices. This is the only class
  where E0.1 as written is a real experiment.
- **Class B1.** 148 structures but **19 inactives across 16 receptors, of which 2 are
  off-panel.** An off-panel calibration is arithmetically impossible. A pooled calibration
  on all 19 is possible and would be a derivation-set figure again — the exact thing E0.1
  exists to escape. So the catalogue's option (b), "calibrate a class B predicate on the
  148 B1 entries as a separate instrument", is **available but cannot be made independent**,
  and must be reported as a derivation-set instrument if it is reported at all.
  The kink threshold 159.95° has, additionally, **no automated check anywhere**
  (`NUMBER_REGISTRY.md:323`) and no code in this repo computes a kink angle from
  coordinates. Note the one operationalised class B geometry in the corpus is
  `hilger2020gcgr` p.3's "sharp kink in the middle of TM6 (105.5°, measured between
  V368-G359-K344)" — **a different residue triple and a different value from ours**, with
  no cut-off proposed; the two numbers are not comparable and should not be presented as if
  they were.
- **Class F.** **14 inactives across 8 receptors, 1 off-panel.** FZD6 has no inactive
  structure in GPCRdb at all. Not calibratable, independently or otherwise. The tilt-alone
  rule is uncalibrated today and will remain so.
- **Class B2, T2, O1, O2, D1.** 2 inactives or fewer each. Not instruments.
- **Class C is the surprise and deserves a look.** 58 inactives — more than any class but
  A, more inactives than actives, 7 both-state receptors, 10 intermediates, and **every one
  of the 58 is off-panel**, because no class C receptor is on our panel at all. It is the
  only class besides A where an off-panel calibration is arithmetically available. Class C
  is a dimeric, Venus-flytrap-domain class whose activation mechanism is not the TM6-swing
  story, so this is very likely a dead end — but it is the only untried one, and the census
  is already computed.

**D3 has a different answer in class B, and E0.5 should say so.** `hilger2020gcgr` p.1 —
"agonist binding alone is insufficient to promote TM6 opening" and "The outward movement of
TM6 of GCGR is only observed upon interaction with Gs" — makes an agonist-only class B
structure a **stronger** exclusion candidate than its class A counterpart, where
`vo2026fiducials` at least supplies a counter-example (§5.1). Whatever is done with class B,
an agonist-only class B structure should not anchor an active pole.

**Two cautions on using that argument.** It is a statement about *class B biology from an
independent paper*, not about our own result, and it must stay that way — the circular move
§5.1 warns against is available here too and is no more legitimate. And GPCRdb's inactive
reference cut for class B is **13.0 Å on 2×46–6×37**, the same atom pair as our tilt axis, so
the §5.1 entanglement applies to class B exactly as it does to class A: GPCRdb's class B
inactive labels cannot calibrate a class B tilt rule. For class F GPCRdb uses a **different atom pair entirely**, and that
turns out to be a defect in our own instrument — see below.

**A class F defect, found while checking the above.** GPCRdb is explicit that the TM6 tilt
for class F is measured on **2×44–6×31**, not 2×46–6×37: *"the distance between the Ca atoms
for the residues 2x46 and 6x37 for all classes except for class F for which the distance
between 2x44 and 6x31 is used"*
(`lit/panels/cache/gpcrdb_activation_degree_definition.txt`). **Our class F rows do not do
this.** `data/block_a/01_rows/block_a_rows.csv` carries exactly one tilt column,
`d_gpcrdb_tm6_tilt_246_637_ca`, populated on all **700 class F rows**, each with
`threshold_tilt_used = 14.932` — the class A atom pair and the class A threshold, applied to
class F receptors. The string `2x44` appears nowhere in `methods.tex` or in any Block A row.

So the class F rule — which `methods.tex:62–63` describes as the tilt rule "used alone",
because neither class A substitution is established there — is measuring the class A
positions under a GPCRdb-derived column name that promises otherwise. This is a **naming-
versus-content defect of exactly the kind the scope rule in `CLAUDE.md` warns about**: the
column says `gpcrdb`, and for class F it is not what GPCRdb means by that name.

It carries no headline claim — `methods.tex:62–63` reports class F as instrument scope only
— so nothing in the manuscript falls. But the class F arm is not measuring what its column
name says.

**What the redo must do, stated so it is not rediscovered.** One of:

1. **Measure class F tilt on 2×46–6×37 and rename the column**, dropping `gpcrdb` from the
   name, since the value is then ours and not GPCRdb's. Cheapest, and honest.
2. **Measure class F tilt on 2×44–6×31**, GPCRdb's actual class F pair, as a *separate*
   column with its *own* threshold — 14.932 Å was fitted on the class A pair and does not
   transfer to a different pair on a different helix. `g0_measure_axes.py` already resolves
   arbitrary GPCRdb generic numbers, so this is a two-line change and one more measurement
   pass over 34 class F structures.
3. **Drop the class F arm**, which §10's census recommends anyway: 14 inactives across 8
   receptors, 1 off-panel, and FZD6 with no inactive structure in GPCRdb at all.

Option 3 is the recommendation; option 1 is the minimum if any class F number is reported.
What is not acceptable is the status quo, because the column name asserts a provenance the
values do not have — the defect class `CLAUDE.md`'s scope rule names, arriving through a
column header rather than a section heading.

`g0_preflight.py` check **G0-10** asserts the defect is still present exactly as described,
so that an upstream fix is noticed here rather than silently diverging from this section.

**Recommendation for E0.5: option (a), narrowed.** Report the work as Class A. Keep class B
and F as declared instrument scope with no claim — the status quo, option (c) — and add
the sentence this census licenses: *the classes cannot be calibrated because their inactive
populations are 19, 14 and 2 structures.* That is a stronger statement than silence and it
is defensible in one line.

**The argument against dropping B entirely, which should be recorded rather than lost.**
`hilger2020gcgr` makes class B the sharpest possible venue for a partner-length ladder:
"agonist binding alone is insufficient to promote TM6 opening" (p.1) and "The outward
movement of TM6 of GCGR is only observed upon interaction with Gs, suggesting that TM6
activation is only triggered by the engagement of the α5 helix of Gαs" (p.1). That is the
project's own hypothesis, stated as an experimental result, in a class we would be
declining to measure. E7.2 depends on E0.5 and E0.5 cannot deliver an independent
instrument — so if E7.2 runs, it runs with a derivation-set instrument and says so.

---

# 11. What has to be true before a single threshold is fitted

A checklist, in order. Nothing below is optional and nothing below needs a GPU.

1. **D2, D3 and D4 answered** (§6.3). D1 is deferred and does not block. All three change
   the population or the objective, and D3 is back open because rule Q0c is retracted (§5.1).
2. **The RCSB metadata pass**, 503 fetches, so Q4 can be applied (§5.4).
3. **The fusion-window flag computed** from the SIFTS segment structure the build step
   already retrieves (§5.4).
4. **The measurement pass**, 726 calibration + 610 application + the 98 pinned reference
   rows (§4).
5. **The refusal ledger reconciled** — every refusal classified as (c) axis-undefined or
   (d) anchor-unmodelled, and the counts reported. §0.1 predicts the first; anything else
   is a defect in the build step and is treated as one.
6. **Q7's outlier bounds declared** on the measured distribution *before* looking at which
   structures they remove.
7. Only then: the fit.

---

## Questions for lit

Numbered, each stating what changes per answer.

1. **Does any paper in the corpus define an activation distance on a CA pair at 5.58/7.53
   rather than the hydroxyls, or otherwise measure the YY-lock on backbone atoms?**
   *If yes:* D1(b)/(c) has a citation and switching the NPxxY axis to CA–CA becomes a
   defensible published convention rather than our own convenience. *If no:* D1(c) is the
   only safe route — keep OH as the headline, report CA as a coverage arm — and the
   Methods must state the 157-of-199 domain of definition as a limitation.

2. **Does any paper report that Y5.58 (or Y7.53) is non-conserved across Class A, and does
   any published state-classifier say what it does on receptors lacking them?**
   `khaleq2026hyaline` and `paajanen2026activation` are both Cα-only, so neither would have
   hit this. *If a paper names it:* §0.1 becomes a cited limitation rather than a discovery
   and the framing in the Methods is one sentence. *If nobody names it:* it is a reportable
   finding in its own right — a widely used activation motif is undefined on ~21% of the
   class — and it belongs in the Results, not the Methods.

3. **Does any paper exclude fusion constructs by whether the insertion falls inside the
   measurement window, rather than by presence of a fusion?** We have
   `georgiou2025heterogeneity` pp.9,16 for the effect and `lee2026confornets` p.15 for
   blanket stripping. *If a windowed rule exists:* Q4 cites it and the threshold of "inside
   the window" is not ours to invent. *If not:* Q4 stands as declared and we must justify
   the window definition ourselves, which is a paragraph in the Methods.

4. **Is there a published disagreement rate between GPCRdb's Active/Inactive annotation and
   any geometric or learned state index?** `intro.tex:325–332` currently asserts none. *If
   one exists:* E0.2's novelty claim weakens to a second measurement and the sentence in
   the introduction needs changing. *If none:* E0.2 (a) is the first, and §5.2's 98 label
   conflicts are the beginning of the answer.

5. **Has `paajanen2026activation`'s tool, weight vector or residue list appeared anywhere —
   a repository, a supplement, a later preprint?** *If yes:* E0.2(c) becomes runnable and
   the concordance check gains its strongest arm. *If no:* §9's sentence stands — the
   nearest published instrument to ours is not reimplementable from its own description —
   and that sentence should go in the Methods beside `methods.tex:83–100`.

6. **Does the corpus settle whether an agonist-bound, transducer-free structure counts as
   "active"?** Reopened: `lee2026confornets`'s 100%-activation-degree rule is **not** an
   independent answer, because GPCRdb defines degree 100 as "in complex with a signaling
   protein" (§5.1). The physical evidence is split — `paajanen2026activation` p.1
   (agonist-bound is bimodal on the activation coordinate) and
   `georgiou2025heterogeneity` p.3697/p.3703 (agonist-only = intermediate active; A2AR TM7
   with NECA is 14% active) against `vo2026fiducials` pp.8–9 (BI-167107 gives almost
   complete TM6 outward movement with no G protein). *If the corpus has any state-assignment
   rule for agonist-only structures that does not reduce to partner presence:* D3 closes on
   it. *If not:* D3 is decided on the physical evidence, declared in advance, and reported
   both ways — and the Methods carries the §5.1 limitation sentence.

6a. **Is there any published active-state reference set in this field that is NOT defined by
   partner presence?** This is the load-bearing question for §7 and §5.1. Everything checked
   so far — GPCRdb's degree, `khaleq2026hyaline` p.12's rule (1) and (2),
   `paajanen2026activation`'s anchor — resolves to a transducer or a transducer-mimetic.
   *If one exists:* our predicate can be validated against it and §5.1's limitation sentence
   is wrong as written. *If none does:* the sentence stands and is a contribution.

6b. **Does any note record how GPCRdb's `degree_active` behaves under the sign ambiguity in
   its own documentation?** The text defines the activation score as "substracting the mean
   distance to the inactive-state structures from the mean distance to the active-state
   structures", which read literally inverts the direction. *If a note settles it:* the
   column can be read with confidence as a covariate. *If not:* it is checked here against a
   known active/inactive pair before any use, and §5.1's open item 2 stands.

7. **Does any paper report a Class C activation predicate, or state that the TM6-swing
   story does not transfer to Class C?** §10 found Class C is the only class besides A with
   an arithmetically available off-panel calibration (58 inactives, all off-panel).
   *If the corpus says the mechanism differs fundamentally:* drop it in one line and the
   census sentence in §10 is complete. *If it is open:* it is a cheap, genuinely
   unattempted arm and worth costing.

8. **Is `mattsson2026leakage`'s "target mirroring" argument made about structures, or only
   about sequences and binding data?** *If structures:* §7's threat sentence cites it
   directly and the I3 paralogy arm becomes a required sensitivity analysis rather than an
   optional one. *If sequence/affinity only:* the citation is an analogy and must be
   flagged as one.
