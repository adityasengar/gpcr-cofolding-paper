# C7_PREREGISTRATION.md — the agonist clause, pre-registered before dispatch

> **STATUS: ENACTED AND BINDING, 2026-09-13 — `DECISIONS.md` D-2026-09-13-a §3.**
>
> *This line read "DRAFTED AND NOT ENACTED" for several hours after enactment, in the
> most-read sentence of the document. Corrected 2026-09-13.* **It is worthless after Group 2
> dispatches** — at that point the same analysis is an unregistered post-hoc contrast,
> which is the weakest form of the strongest result available to this paper.
>
> Written 2026-09-12, hours after `DECISIONS.md` **F-23** retracted the claim that C7
> was already answered. Read F-23 first.

---

## 1. Why this document exists

**C7 — "the agonist alone does not drive the active state" — has never been tested.**
Blocks A, B and D supply no agonist-alone arm. Block C was believed to, and does not:
**all 40,800 rows of `rows.tier3.v2.csv` carry a ligand** (agonist 14,800 / antagonist
11,600 / decoy 14,400, no `none` level), so "apo" there means *no partner*, not *no
ligand*.

**The redo already contains the experiment, and nobody had noticed.** It was enumerated
as part of Group 2's design, has been `READY` since the ligand arm was built, and costs
**zero marginal predictions** because Group 2 dispatches those rows regardless.

## 2. The design, as it already exists in `inputs/g2_systems.csv`

A **2 × 2**: partner present/absent × agonist present/absent.

| cell | `partner_level` | `ligand_role_actual` | rows READY |
|---|---|---|---|
| neither | `apo` | `none` | **41** |
| agonist only | `apo` | `full_agonist` | — |
| partner only | `cognate` | `none` | **57** |
| both | `cognate` | `full_agonist` | — |

**98 ligand-free rows are READY.** Crossed against the agonist rows already in the arm,
**20 receptors in 19 distinct paralog clusters carry all four cells.**

**Power, stated in advance — and CORRECTED 2026-09-13 before any data exists.**

This section first quoted **`MDE = 1.218/√k` → 0.279 at k = 19**. That constant is the
**INTERACTION** figure: `RUN_MATRIX.md:515` gives the median *interaction* cluster SD as
**0.435**, and 2.80 × 0.435 = 1.218. **C7's primary contrast is a MAIN EFFECT**, and
`RUN_MATRIX.md:490-492` tabulates those separately — 0.189 for `cognate − apo`, 0.242 for
`cognate − decoy`. `:503` says so explicitly: *"An interaction is a difference of
differences and its cluster SD is roughly double a main effect's."*

| quantity | cluster SD | MDE at k = 19 |
|---|---:|---:|
| **main effect** (the C7 contrast) | 0.189 – 0.242 | **0.121 – 0.155** |
| interaction (partner × ligand) | 0.435 | 0.279 |

**Quoting 0.279 was conservative — it understated our power, so nothing was
overclaimed.** But it carried a constant across contrast types without re-deriving it,
which is this project's `compare-like-with-like` failure, and a pre-registration is the
one document where a power figure must be the right one.

**AND A LIMIT THAT MATTERS MORE THAN EITHER NUMBER.** Both are in **binary-predicate
units** — `redo/build/matrix_power.py` computes its SDs on
`(d_npxxy < threshold) AND (tilt > threshold)`, so they are percentage points of
active-call rate. **§3 below declares a CONTINUOUS axis primary, and no MDE exists for
it.** The honest statement is: **the primary axis for C7 is not yet powered, and the
figures above bound a secondary readout.**

**The free thing that would fix it is `E7.4`** — the interaction power injection, marked
`FREE_UNSCHEDULED` in `run_registry.tsv`, which `CAMPAIGN.md` §2.8 and `RUN_MATRIX` §4.3
both say **must precede the ligand arm**. It supplies the MDE on the declared axis, in
its own units, from the pilot's own rows. **It should run before this arm dispatches.**

## 3. What is pre-registered

**The contrast.** C7 is tested as **`apo/agonist` versus `apo/none`** — the agonist's own
contribution with no partner present. The partner effect (`cognate/none` − `apo/none`)
and the interaction are reported alongside it, from the same four cells.

**The readout, and this is the clause that matters most.** Report **every** axis the
recording spec carries — `pocket_ca_rmsd_active`/`_inactive`, the NPxxY-OH distance, the
TM6 tilt, and the binary predicate — **per backbone, on its own scale, with the partner
effect printed beside it.**

> **The agonist's effect is NEVER to be expressed as a share or percentage of the
> partner effect.** Measured on Block C, that share spans **an order of magnitude across
> readouts on the same predictions and the same panel** — 27–67% on pocket-Cα, 5–17% on
> TM6 tilt, 3–16% on NPxxY-OH, 5–9% on the binary predicate. It is a property of the
> readout, not of the ligand. F-23 records that we nearly published a literature bridge
> built on the largest of the five.

**Pocket-Cα RMSD is declared BIASED FOR THIS CONTRAST, in advance.**
`pocket_ca_rmsd_active` scores the pocket against a deposited **active** reference, which
for these receptors is **agonist-bound** — so it is the axis most responsive to an agonist
by construction. It is reported, and it is **not** the primary axis for C7. The primary
axis is the one the instrument was calibrated on.

**The unit** is the paralog cluster, aggregated
`row → (receptor, arm, role, backbone, seed) → receptor → cluster`. **Intervals are
cluster bootstraps**, paired within cluster. **Never pooled across backbones** — this
project has twice found that pooling across disagreeing backbones produces a statement
about one backbone in the clothes of a statement about a class.

**Seeds** are collapsed inside the receptor before the cluster mean, so five seeds of one
receptor cannot outvote one seed of another.

## 4. What counts as which answer, declared before the data

| outcome | statement |
|---|---|
| `apo/agonist` − `apo/none` **includes zero on the primary axis on ≥3 of 4 backbones** | **C7 holds**: the agonist alone does not drive the active state |
| it **excludes zero on ≥3 of 4**, and is **smaller** than the partner effect on the same axis | **C7 holds in weakened form**: the agonist alone shifts the receptor but does not reproduce the partner |
| it **excludes zero** and is **comparable to** the partner effect | **C7 FAILS.** The title's second clause is wrong and must be withdrawn |
| backbones disagree in **sign** | **no pooled claim is made.** Reported per backbone, and the disagreement is the result |

**The third row is written deliberately.** A pre-registration that cannot record its own
refutation is not one.

## 5. What this does NOT close

- **Not the peptide clause (C6).** Reachable only through the length ladder.
- **Not efficacy.** `full_agonist` only; partial and inverse agonists are elsewhere.
- **Modality stays confounded with receptor identity** — every peptide-ligand row is a
  peptide-family receptor, so this cannot separate *peptide ligand* from *peptide
  receptor*. `D-2026-09-12-f`'s T3 tier is the within-receptor contrast that can.
- **The instrument is still uncalibrated.** One predicate threshold is inherited rather
  than derived; that is the measurement pass, and it has not run. Every number here is
  conditional on it.

## 6. To enact

1. Aditya says yes.
2. A `D-2026-09-12-*` entry in `DECISIONS.md` points at this file and dates it.
3. A gate check asserts the 20 receptors / 19 clusters are present and `READY` before
   Group 2 dispatches, and fails if the arm shrinks — the same treatment `drule.py`
   gives the frozen decoy selection.

**Step 3 is not optional.** An arm that quietly loses receptors between registration and
dispatch is how a pre-registration becomes decoration.
