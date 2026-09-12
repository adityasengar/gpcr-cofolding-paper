# FIRST LOOK at rows.tier3.v2.csv — and it is a FIRST LOOK, not a finding

**Written 2026-09-12, the day the file arrived.** Everything here is pooled over
receptors and backbones, which is the analysis this project has repeatedly shown to
be wrong. **Do not quote these numbers.** They are recorded so the next session
starts from something rather than nothing.

## The arm mapping, established and checkable

There is **no `arm` column**, `experiment_id` is **empty on all 40,800 rows**, and
`input_state_claim` is the constant `"Ga-coupled-active"` on every row — so none of
the obvious columns carries it. **The arm is in `input_path`:**

```
/hpc/scratch/.../021_block_c_tier3_pharmacology/tier3/pool/
        <receptor>/<ligand_role>/<arm>/<backbone>/seed_<n>/...
                                  ^^^^^
```

Parsed on the `pool` segment, this gives a **perfectly balanced design**:
**apo 20,400 / cognate 20,400**, and **boltz / protenix / chai / of3 at 10,200
each**. That balance is itself evidence the parse is right.

### CROSS-VALIDATED 2026-09-12 — the parse is exact

`data/block_c/12_g4_off_site_census/g4_full_census_v2.csv` carries its own
**explicit `arm` column**. Keyed on (receptor, arm, role, backbone):

- **800 census cells, 800 of them present in `rows.tier3.v2` with IDENTICAL row
  counts. Zero mismatches.** The path-derived arm agrees with the recorded arm on
  every shared cell.
- `rows.tier3.v2` carries **16 cells the census does not**, and they are fully
  accounted for: **`B1B1U5` and `OPSD`, 400 rows each**. Both are the non-human
  opsins, and **they are exactly the 800 rows with an empty `receptor_class`** —
  so the two anomalies are one anomaly, and it is explained rather than excluded.

*(My first attempt reported zero overlap. The census's receptor column is
`receptor`, not `receptor_slug`, so every key had `None` in first position. My
checker, not the data — as usual.)*

**The arm mapping can now be relied on.** Step 1 of the order of work below is
done; steps 2–5 are not.

## The 2×2, Class A, pooled — the shape, not the number

Active call = `d_npxxy_y558_y753_oh < threshold_npxxy_oh_active_lt` **AND**
`d_gpcrdb_tm6_tilt_246_637_ca > threshold_gpcrdb_tm6_tilt_active_gt`, using the
thresholds **as carried in the file**.

| arm | ligand role | modality | active | n | rate |
|---|---|---|---:|---:|---:|
| apo | decoy | peptide | 17 | 400 | 0.043 |
| apo | decoy | small molecule | 647 | 6,800 | 0.095 |
| apo | **full agonist** | peptide | 525 | 3,000 | **0.175** |
| apo | **full agonist** | small molecule | 473 | 4,000 | **0.118** |
| apo | neutral antagonist | small molecule | 562 | 5,800 | 0.097 |
| cognate | decoy | peptide | 303 | 400 | 0.757 |
| cognate | decoy | small molecule | 4,882 | 6,800 | 0.718 |
| cognate | **full agonist** | peptide | 2,076 | 3,000 | **0.692** |
| cognate | **full agonist** | small molecule | 3,276 | 4,000 | **0.819** |
| cognate | neutral antagonist | small molecule | 4,158 | 5,800 | 0.717 |

### What it looks like, stated as impressions

1. **Partner presence dominates.** apo 0.04–0.18 against cognate 0.69–0.82. Every
   other factor is small beside it.
2. **The agonist alone does not do it.** Agonist + no partner = **0.118**; agonist +
   partner = **0.819**. That is the paper's C7 clause, and it is the arm that has to
   answer `vo2026fiducials` p.8, where a high-efficacy agonist alone drove β2AR TM6
   *"almost complete outward movement"*. Across 40 receptors and four backbones,
   agonist-alone does not reproduce that here.
3. **Ligand class moves it a little, inside the cognate arm.** agonist 0.819 vs
   antagonist 0.717 vs decoy 0.718 — the antagonist and the decoy are
   indistinguishable, which is its own finding if it survives.
4. **Modality moves it, and in OPPOSITE directions by arm.** Agonist rows: peptide
   *higher* than small molecule in apo (0.175 vs 0.118), *lower* in cognate (0.692
   vs 0.819). If that survives, it is an interaction, and it is the question
   D-2026-09-12-f was tiered to handle.
5. **There is no peptide/neutral-antagonist cell at all** — consistent with what the
   ligand census found independently: peptide receptors are drugged with
   small-molecule blockers.

## Why none of the above is a result yet

- **Modality is confounded with receptor identity.** Every peptide-ligand row is a
  peptide-family receptor. This file cannot separate "peptide ligand" from "peptide
  receptor" any more than the AUROC probe could.
- **Pooled across backbones.** This project has now twice found that pooling across
  backbones that disagree produces a statement about one backbone wearing the
  clothes of a statement about a class (F-13(c), and the Class B 9 Å split). **Redo
  every line of the table per backbone before believing any of it.**
- **Pooled across receptors, and rows are the unit.** The statistical unit here is
  the **paralog cluster**. Row-level rates have no interval that means anything.
- **The binary predicate is the wrong readout.** `SC-C-6` records it as floor-pinned
  on apo and ceiling-pinned on cognate for ~65% of cells. The file carries
  `pocket_ca_rmsd_active` / `_inactive`, which is the continuous readout that
  document says to prefer. **This table uses the readout its own drop warns against.**
- **Seeds are ignored.** `seed_used` is in the file and the pre-registration says
  seed is the unit of variance.
- **THE 800 EXCLUDED ROWS ARE NOT ROLE-NEUTRAL, and this table does not account
  for that.** Added 2026-09-12 after the Group 2 build caught it. The 800 rows
  dropped for an empty `receptor_class` are **`B1B1U5` and `OPSD`, 200 per arm
  each, and every one of them is `full_agonist`** — zero antagonist rows and zero
  decoy rows are excluded. So the exclusion removes agonist observations only,
  from two receptors, symmetrically across arms. Any comparison of the agonist
  level against the antagonist or decoy levels in the table above is therefore
  drawn on a population the other levels do not share. **Recompute with the two
  opsins handled explicitly — included with a class assigned, or excluded from
  every role — before comparing ligand levels at all.**

## The order of work when someone picks this up

1. Cross-validate the path-derived arm against the g4 census's `arm` column.
2. Re-run the table **per backbone**, and stop if they disagree.
3. Aggregate to paralog clusters, then bootstrap over clusters.
4. Switch the readout to `pocket_ca_rmsd_active/_inactive` and see whether the
   shape survives.
5. Only then ask whether modality does anything, and expect to need a
   within-receptor contrast to answer it.
