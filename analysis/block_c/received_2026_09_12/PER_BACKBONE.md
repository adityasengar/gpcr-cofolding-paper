# Step 2 — per backbone. The headline survives; the decoy arm does not.

**2026-09-12.** `FIRST_LOOK.md` step 2 of the order of work. This is the test that
retracted F-13(c) and exposed the Class B 9 Å split, so it is the one that decides
whether the pooled table meant anything.

**Class A rows only.** That drops `B1B1U5` and `OPSD`, whose exclusion is
**role-asymmetric** — all 800 are `full_agonist` — so agonist-vs-antagonist
comparisons below are still drawn on slightly different populations. Steps 3–5
(cluster unit, continuous readout, seeds) are **not** done.

## The table

active fraction, two-instrument predicate, thresholds as carried in the file

| backbone | arm | full agonist | neutral antagonist | decoy |
|---|---|---:|---:|---:|
| boltz | apo | 0.094 | 0.063 | 0.062 |
| boltz | **cognate** | **0.806** | 0.736 | 0.725 |
| chai | apo | 0.259 | 0.202 | 0.186 |
| chai | **cognate** | **0.634** | 0.614 | 0.618 |
| of3 | apo | 0.166 | 0.112 | 0.105 |
| of3 | **cognate** | **0.738** | 0.663 | 0.679 |
| protenix | apo | 0.052 | 0.011 | 0.016 |
| protenix | **cognate** | **0.879** | 0.854 | 0.858 |

*n = 1,750 agonist / 1,450 antagonist / 1,800 decoy per backbone per arm.*

## 1. The partner effect is real on every backbone

apo → cognate, agonist rows: **0.094 → 0.806**, **0.259 → 0.634**, **0.166 →
0.738**, **0.052 → 0.879**. Four backbones, same direction, large on all of them.

**This is not a pooling artefact**, and that matters because two previous claims in
this project died at exactly this step. It is the paper's C7 clause — *the agonist
alone does not* — measured on 40,000 predictions that were already paid for.

**But the apo floor is wildly backbone-specific**: chai sits at 0.186–0.259 while
protenix sits at 0.011–0.052, a 5–20× spread on the same inputs. So **no pooled apo
rate should ever be quoted**; the contrast is what transfers, not the level.

## 2. Ligand class moves it a little, consistently

agonist − antagonist, cognate arm: **+0.070, +0.020, +0.076, +0.025** — positive on
**4 of 4**. In the apo arm too (0.094/0.063, 0.259/0.202, 0.166/0.112, 0.052/0.011).
Small, but it does not change sign anywhere, which is more than the tilt managed on
Class F.

## 3. The decoy does not discriminate — on any backbone

antagonist − decoy, cognate arm: **+0.011, −0.004, −0.016, −0.004**. Straddles zero,
three of four negative. **A hand-picked FDA drug behaves exactly like a curated
neutral antagonist**, on every backbone.

**This is the most useful negative result in the file.** The frozen decoy arm was
not measuring what it was built to measure, and the reason is visible in its own
construction: the decoys were chosen by hand and the ±20% property window was
computed and never enforced, so "decoy" meant "some other drug" rather than
"matched on everything except binding".

It is also **direct evidence for the redo's decoy design** (`DRULE_CHEMBL_SCOPE.md`,
`G-6`): a pool with the property window **enforced**, the molecule drawn as a random
effect across three draws rather than one hand-pick per receptor, and absence of
activity established against the whole paralog cluster. **If the rebuilt arm still
shows antagonist ≈ decoy, that is a finding about the models. As it stands it is a
finding about the decoys.**

And it sharpens `yu2026domainmotion`, the sharpest published challenge to this arm:
they show a known non-binder reproduces the conformational change. Here a known
non-binder reproduces the *state call*. We cannot answer them with this decoy set.

## What must still happen before any of this is quotable

3. aggregate to **paralog clusters** and bootstrap over them — rows are not the unit;
4. switch to `pocket_ca_rmsd_active/_inactive`, the continuous readout `SC-C-6` says
   to prefer because the binary predicate is floor- and ceiling-pinned on ~65% of cells;
5. handle **seeds** — `seed_used` is in the file and the pre-registration makes seed
   the unit of variance;
6. resolve the **role-asymmetric opsin exclusion** noted above.
