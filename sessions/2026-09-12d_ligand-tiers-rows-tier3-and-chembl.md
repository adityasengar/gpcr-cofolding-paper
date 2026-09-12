# 2026-09-12d — the ligand arm becomes runnable, Block C's missing file arrives, and ChEMBL lands

Orchestrator session, continuing after the scope/D2/reversals wrap. **The longest
and most productive session on this project so far**, and the one where the other
team started correcting us as fast as we corrected ourselves.

## What happened

| | |
|---|---|
| **the ligand arm** | tiered, curated, enumerated, gated — **decided → runnable** |
| **`rows.tier3.v2.csv`** | **arrived**, hash-verified against 18 pins, arm mapping established and cross-validated |
| **the 2×2** | computed, then re-computed **per backbone** — it survives |
| **ChEMBL_37** | downloaded, verified, extracted; pool extraction in flight at session end |
| **two maps** | frozen campaign end-to-end, and what the redo runs |
| **the run registry** | 45 experiments, joined for the first time |
| **`paper_af3`** | answered four asks; **corrected us twice** |

## Decisions Aditya made, with their reasons

**Class A only.** Grounds are measured, not economic — Class B shows a 9 Å
inter-backbone disagreement and Class F has no discriminating power.

**D2 at option (c)**, the split, taken at the only cut that costs calibration
nothing.

**Keep peptide receptors, treat them separately.** Not pooled into T1, because a
peptide ligand is another polymer chain and the paper's whole claim is about what
adding a chain does.

**Relax amendment C-1** — an inverse agonist is an admissible off-state ligand.
**It unblocked three receptors, not the two we expected.**

**Skip PAM/NAM and antibody ligands entirely.** Vindicated by lit: **no published
labelling rule covers PAM/NAM at all** — `khaleq2026hyaline` p12 has no slot for
them, so they would have entered on our authority alone.

**Mixed-modality receptors become Tier 3** rather than being excluded.

**Work independently of `paper_af3`; sort their asks later.** Then, later:
**approve all four asks**, and **take the full ChEMBL download** after being shown
the disk cost.

## What the verification found

**`rows.tier3.v2.csv` is the file Block C pinned 18 times and never shipped**, and
its sha256 matches that pinned value exactly. 40,801 lines, 101 columns.

**The arm is in none of the obvious columns** — `experiment_id` is empty on all
40,800 rows and `input_state_claim` is a constant. It is in `input_path`. Parsing
there gives a perfectly balanced apo 20,400 / cognate 20,400 and 10,200 per
backbone, and **cross-validation against the g4 census's explicit `arm` column
matches on all 800 shared cells with zero discrepancies.**

**THE PARTNER EFFECT SURVIVES PER BACKBONE.** agonist rows, apo → cognate:
**0.094→0.806** (boltz), **0.259→0.634** (chai), **0.166→0.738** (of3),
**0.052→0.879** (protenix). Four backbones, same direction, large on all. That is
title clause **C7 — the agonist alone does not** — on predictions already paid
for. But the apo **floor** is wildly backbone-specific (chai 0.19–0.26 vs protenix
0.01–0.05), so **no pooled apo rate is quotable**; the contrast transfers, the
level does not.

**THE DECOY DOES NOT DISCRIMINATE ON ANY BACKBONE.** antagonist − decoy:
+0.011, −0.004, −0.016, −0.004. A hand-picked FDA drug behaves exactly like a
curated neutral antagonist. **That is a finding about the decoys, not the models**
— and it is direct evidence for rebuilding the rule, and it sharpens
`yu2026domainmotion`: they show a non-binder reproduces the conformational change;
here one reproduces the **state call**.

**The threshold rule is `midpoint(active_mean, inactive_mean)`**, per receptor per
role first. Reproduced to within 1–1.5% from the reference set we hold — and the
script they sent **does not implement the Class A fit**, so the fit set is still
unknown.

**ChEMBL, measured rather than assumed:** the spec's "activity anywhere" rule gives
**1,203,741 candidates per receptor**; within-panel gives **120,973**. And the
**paralog-cluster exclusion removes more than the receptor exclusion** (192,630 vs
170,737) — the spec argued that on principle; it now has numbers.

## What I got wrong and corrected — the long list, and it is the point

**Retractions of substantive claims:**

1. **F-13(c), "SMO gets less open with the partner"** — OF3-only. SMO is +0.22 /
   +0.04 / −2.14 / +0.19; slightly *positive* on three of four. Caught by
   `paper_af3`. **It was the same pooling-across-disagreeing-backbones error I had
   flagged for Class B one paragraph earlier.**
2. **I flagged FZD4's absence from the cognate table as a gap.** It is
   pre-registered design — FZD4's transducer is Dishevelled, not a Gα, so there is
   no cognate partner to supply. Their `PREREG.md:277` said so before the data.
3. **The ladder length/taxonomy confound — revised downward three times and finally
   retracted.** Mazzoni's ≥17 threshold is contested; AF3's 16 is a *benchmark*
   filter not an architectural limit; and `paper_af3` grepped OpenFold3 and found
   **no length branch at inference anywhere**. Every line we found governs training
   or evaluation set construction. **The confound as I stated it does not exist.**

**Curation and code defects caught by gates rather than by reading:**

4. **carazolol recorded as a neutral antagonist** — GPCRdb types it an inverse
   agonist, which is what blocks it under C-1. ADRB1 was not straightforward.
5. **NTR1 entered T1 on a rat structure** in an Intermediate state. Species follows
   the panel, not the PDB.
6. **The tier picker ranked reference-first above chain-ness**, so an on-reference
   peptide beat an off-reference small molecule and **mis-tiered four receptors we
   had already curated**; it also let an agonist be picked from an *inactive*
   structure.
7. **I typed PD2R2's CCD from memory and got it wrong** — then found GPCRdb's own
   record names PGD2 while giving a CCD for a phosphatidylinositol, and **refused
   the pick**. A membrane lipid would have been supplied as the agonist.
8. **`is_peptide` is upper-case `FALSE`** — my test matched lower-case and reported
   all nine inherited receptors as failing.
9. **The census's column is `receptor`, not `receptor_slug`** — my first
   cross-validation reported *zero* overlap.
10. **B18 read a variable named `rows` that is not the systems table**, so it passed
    on the wrong data and its plant did not fire.
11. **A `.tsv` written into the `.json` cache directory** — the layout guard caught
    it, and the fix was to promote the census to a proper generated input.
12. **L-5 began passing vacuously** once C-1 left zero blocked receptors; its plant
    could not apply. The plant now *creates* the condition.
13. **I taught the generator a new role vocabulary and not the gate.**
14. **`drule_pool`'s fixture had one cluster**, so it could not express the rule it
    was testing — and it **masked a plumbing bug**: `tid` was never populated, so
    the first real run produced zero rows.

**The one that matters most:**

15. **G0's self-test was dead and I had been asserting the opposite in three
    documents.** `_clone` copied only the top-level files of `redo/`, correct while
    it was flat and silently wrong from the layout migration onward. **0 of 11
    checks were being proved while `CLAUDE.md` said every check was proved.**

**And a near-miss:** I used `git add -u`, which has the same failure mode as
`git add -A`. Nothing was swept only because no other session had edits in flight.

## IN FLIGHT at session end

**The ChEMBL pool extraction is still running** — `redo/build/drule_pool.py`
against `/Users/aditya/chembl_37/chembl_37/chembl_37_sqlite/chembl_37.db`,
writing `inputs/drule_pool_molecules.tsv` and `inputs/drule_pool_exclusions.tsv`.
Log at `/tmp/drule_run2.log`. **When it finishes:** restamp the manifest, run
`gates/drule.py` (it should stop announcing an unbuilt pool), and **delete the
28 GB database** — the pool and its provenance are what we keep.

**Uncommitted and not ours:** `lit/analysis_review/LIGAND_MODALITY_CORPUS_ANSWERS.md`
and `MSA_SUBSAMPLING_CORPUS_ANSWERS.md`. Aditya has not said lit is finished.

## What the next session should not redo

- **Do not re-open** the scope, D2, D-A, D-H, the coupling reversals, the ligand
  tiers, or C-1. All decided with reasons in `DECISIONS.md`, all gated.
- **Do not restate "SMO goes backwards"** or the ladder taxonomy confound. Both
  retracted.
- **Do not treat FZD4's absence as a gap.** Pre-registered.
- **Do not quote the pooled 2×2** in `FIRST_LOOK.md` — use `PER_BACKBONE.md`, and
  note even that still needs cluster aggregation, the continuous readout, and seeds.
- **Do not build the decoy pool with the `anywhere` scope.** Measured at 1.2 M per
  receptor.
- **Do not trust a self-test you have not run.** Run `--selftest` on every gate.
