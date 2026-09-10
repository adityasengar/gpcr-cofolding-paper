# What Block C still needs from the pipeline

Paste-ready for the coding agent that owns the HPC runs. Ordered by whether a
sentence in `manuscript/sections/` currently depends on the answer, not by
effort. Every "State" line was recomputed from `data/block_c/` today; the
recomputation is in `analysis/block_c/verify_claims.py` (53 checks, 0 mismatches)
unless another command is given inline.

**Cost classes**: **free** — re-analysis or re-export of data the pipeline
already holds, no scoring, no inference. **cheap** — re-scoring existing
predictions, no new inference. **real** — new predictions.

**The one-line summary of this document.** Block C shipped **one row-level
file** — `12_g4_off_site_census/g4_full_census_v2.csv`, 40,000 rows — and
summary JSON for everything else. That is why 30 of our 53 checks are
consistency-only, why **both of the block's surviving positive claims cannot be
recomputed from anything**, and why most of the asks below are one file each.
Ask 1 closes six of the other seventeen on its own.

**All eighteen asks are `free`.** Not one of them needs a prediction re-scored
or a model re-run: every number requested here has already been computed on the
pipeline side and is either sitting in a file that was not put in the zip, or is
one aggregation away from one that was. That is the whole shape of this drop.
The **cheap** and **real** asks — a class-matched pose rescore, chemistry columns
on the census, the 21-mer arm — are in `rebuttals/BLOCK_C.md` §3, where they
belong.

Asks 1–9 block or contradict a sentence that is in the `.tex` right now. Asks
10–18 remove a stated weakness. **Ask 10 is the single most valuable item here**
and it is deliberately not in the first section: no sentence depends on it yet
because the drop's own dispatch forbids writing one, and that instruction needs
re-adjudicating rather than quietly ignoring.

Nothing here blocks submission.

---

# Blocking or contradicting a sentence in the manuscript today

## 1. `rows.tier3.v2.csv` — the primary corpus. **free**

**Manuscript locator**: `results.tex:362–396` (the four 2×2 values and their
intervals, the Kendall's τ receptor fractions, the LORO AUROCs),
`results.tex:348` ("36 landed"), `methods.tex:395–417`, and
`methods.tex:428–436`, which is a paragraph whose whole subject is this file's
absence.

**State.** Named by SHA-256 `5ccf58ac…` in twenty separate places across the
drop — the claim sheet's Corpus block, `g1_bootstrap_s1_auroc.json.inputs`,
`s1_loro_classifier.json.inputs`, `g_scc1_cluster_boot.json.inputs`,
`s3_consensus_confidence.json.inputs`,
`stage3_2x2_ligand_state_specificity.json.reconstruction` — and shipped in none.
Consequence, recomputed:

| kind | n checks | what a green result means |
|---|---:|---|
| RECOMPUTED | 23 | derived from the census CSV, independent of any summary |
| CONSISTENCY | 30 | the same number read from two shipped files and compared |

SC-C-1 and SC-C-4 — the block's two surviving positives — are entirely in the
second group. A green consistency check catches transcription and staleness; it
cannot catch a computation that was wrong in the same way in every file. That is
exactly how Block B's per-backbone family shares passed their own
`matches_claim_sheet_bool` column while reproducing from nothing.

```bash
python3 analysis/block_c/verify_claims.py -v | head -3
```

**What we need.** The 40,800-row table, or a tidy export carrying:
`receptor_slug`, `backbone`, `arm`, `ligand_role`, `seed_outer`, `sample_idx`,
`passed`, `A5_species_match`, `pocket_ca_rmsd_active`, `pocket_ca_rmsd_inactive`,
`d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`, the pLDDT aggregations,
`pocket_ref_pdb_sha_active`, `pocket_ref_pdb_sha_inactive`,
`pocket_ref_role_active`, `pocket_ref_role_inactive`. Those columns alone close
asks 2, 6, 7, 8, 10 and 14 as well as this one.

**Promised?** Yes, as an input pinned by SHA in six analysis JSONs and in the
claim sheet's own Corpus paragraph. `data/block_c/tier3/MANIFEST_RAW_ROWS.md`
(also not shipped) is cited as the reason it is kept out of git. If the intent
is that it lives in the release repo rather than the zip, say so and we will
stop treating the SHA pin as a promise of delivery.

---

## 2. The 1.52 % reassurance is computed on a population SC-C-1 is not computed on. **free**

**Manuscript locator**: `results.tex:426–435`. Also
`data/block_c/README.md` §"Load-bearing numbers", `figures/FIGURES.md:605`,
`analysis/block_c/panels/BC-4_ligand_placement.md` §"What the panel has to say",
and `figures/block_c/panels/bc4_ligand_placement.py`.

**State.** The drop states, and we repeated, that SC-C-1's numerator is
1.52 % off-site — computed as apo × {full\_agonist, neutral\_antagonist} ×
`ligand_source == "hetatm"`. That filter is real and that number reproduces
exactly (149 of 9,800). **But SC-C-1 is not computed on small molecules.** Its
own artefacts pin it to the 23-receptor 2×2 common set
(`stage3_2x2_ligand_state_specificity.json`:
`interaction.n_receptors_in_common = 23`; `g_scc1_cluster_boot.json`:
`n_receptors_in_common = 23`), and eleven of those 23 are peptide-agonist
receptors. On the population SC-C-1 actually runs on:

| population | n rows | off-site > 15 Å |
|---|---:|---:|
| apo × {agonist, antagonist} × `hetatm`, all 36 receptors *(the quoted number)* | 9,800 | **1.52 %** |
| apo × {agonist, antagonist}, **the 23 common receptors, all ligands** | 9,200 | **18.92 %** |
| — its agonist half | 4,600 | **35.85 %** |
| — its antagonist half | 4,600 | **2.00 %** |
| apo × {agonist, antagonist}, the S1 15-set, all ligands | 6,000 | 22.12 % |
| — its agonist half | 3,000 | **41.63 %** |

Eight of SC-C-1's 23 receptors have their apo agonist off-site on 50–100 % of
rows: CXCR2, CCR5, CXCR4, NPY1R, NPY2R, EDNRB (all 100 %), MCHR1 (90.5 %), GRPR
(56.5 %). The asymmetry — 35.9 % against 2.0 % — is perfectly aligned with the
class label the 2×2 contrasts, which is the one alignment that matters.

```bash
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
S23=set('5HT1B 5HT5A AA1R AA2AR ACM2 ACM4 ADRB2 AGTR1 CCR5 CNR1 CNR2 CXCR2 CXCR4 EDNRB GRPR LPAR1 LT4R1 MCHR1 NPY1R NPY2R OPRD OPRK OPRX'.split())
b=c[(c.arm=='apo')&(c.role.isin(['full_agonist','neutral_antagonist']))&(c.receptor.isin(S23))]
for lbl,d in [('all',b),('agonist',b[b.role=='full_agonist']),('antag',b[b.role=='neutral_antagonist'])]:
    print(lbl, len(d), round(100*(d.distance_A>15).mean(),2))"
```

**We ran the strongest test we can run locally and it came back clean, and that
matters as much as the finding.** `pocket_ca_rmsd` is receptor-side (C-C-6:
twelve fixed BW positions, 7TM Cα Kabsch), so an off-site ligand does not
mechanically corrupt it. If the interaction were an empty-pocket artefact, the
ordinal recovery should collapse on the eight affected receptors. It does not:
Spearman(agonist off-site %, per-receptor median τ) = **−0.241, p = 0.268,
n = 23**; Mann–Whitney on the two groups p = 0.436 (medians 0.282 vs 0.386). At
classifier grain, Spearman(off-site %, per-receptor AUROC) = **−0.160, p = 0.568,
n = 15**, and the worst receptor in the whole classifier — AGTR1, AUROC 0.000 on
three backbones — has its agonist **in** the pocket on 97.5 % of rows, while
EDNRB, NPY2R and OPRX are at 0.99–1.00 with 48–100 % off-site.

**What we need.** Two things, neither of them a run:

1. Confirm which population SC-C-1's four point estimates are computed on. If it
   is the 23-receptor set irrespective of `ligand_source`, the claim sheet's
   "SC-C-1's numerator: 1.52 %" line and our `results.tex:426–435` sentence both
   need replacing with 18.92 % / 35.85 % / 2.00 % plus the receptor-side
   argument above.
2. The 2×2 interaction recomputed on the small-molecule-agonist receptors only
   (the 23 minus the eleven peptide receptors, so twelve: 5HT1B, 5HT5A, AA1R,
   AA2AR, ACM2, ACM4, ADRB2, CNR1, CNR2, LPAR1, LT4R1, OPRD). If the four signs
   survive on twelve receptors, the sentence becomes stronger than it is now and
   the whole objection is closed in one line. **We can run this ourselves the
   moment ask 1 lands.**

**Promised?** The 1.52 % figure is promised, prominently, as "SC-C-1's
numerator" in `README.md` §"Load-bearing numbers". The population it is a
numerator *of* is not stated anywhere.

---

## 3. `rescore_t7c_full/rows.csv` and `rescore_manifest.tier3.v2.csv` — the pose corpus. **free**

**Manuscript locator**: `results.tex:419–425` — the entire pose paragraph:
6.93 %, and the bimodal per-receptor dock rates 54–56 % / 0–18 % / 0 %.

**State.** Neither ships. `t7b_pose_accuracy.json` and
`task_E_v3_scoped_finding.json` do, and between them the 6.93 % arithmetic
recomputes — 88 + 83 + 68 + 73 = 312 over 1,100 + 1,150 + 1,100 + 1,150 = 4,500
— so the *sum* is checkable and the *measurement* is not. The bimodality
sentence (Boltz 54–56 %, Chai 0–18 %, OF3/Protenix 0 %) has **no shipped source
at all**: it appears only as prose in `T7C_POST_FIX_HEADLINE.md` and W-C-3, and
the two files that would carry it —
`step4_cell_receptor_distribution.csv` and `step4_ecdf_per_receptor.csv` — are
named in that same headline and are absent.

The manifest matters independently: `input_bound_pdb` is what defines SC-C-7's
"strictly matched-reference" scope, and `pocket_ligand_atom_map_method` is what
C-C-6 and C-C-8 are about. Neither column exists anywhere in the drop.

**What we need.** `rows.csv` (scorer `d9c646af…`) with `receptor_slug`,
`backbone`, `ligand_role`, `partner_type`, `ligand_rmsd_to_ref`,
`pocket_ligand_atom_map_method`, `input_bound_pdb`, `pocket_metric_ref_used`;
and `rescore_manifest.tier3.v2.csv` (SHA `7104a650…`). Failing the full table,
`step4_cell_receptor_distribution.csv` alone would let us draw the bimodality
rather than assert it.

**Promised?** Yes — pinned by scorer SHA in Flag C-7, named as
`inputs.rows_t7b` and `inputs.rows_v2` in `t7b_pose_accuracy.json`, and both
`step4_*` files are cited by name in `T7C_POST_FIX_HEADLINE.md`.

---

## 4. `pr2_fshr_lshr_class.json` — the PAM-inactive-reference reason. **free**

**Manuscript locator**: `results.tex:348–352` and `methods.tex:383–388` — "two
whose inactive reference is stabilised by an allosteric modulator rather than an
orthosteric antagonist, which makes the ligand-class contrast undefined for
them."

**State.** That sentence has one source, `pr2_fshr_lshr_class.json`, cited by
C-C-9 and by both closeout reports, and it is not shipped. **The shipped
reference survey says something different**: `09_references/reference_survey.csv`
gives FSHR/8I2H and LSHR/7FIJ `status = NO_HETATM_CANDIDATES` — no orthosteric
ligand candidate found — with curation notes about unresolved 5.58 and 7.53
sidechain hydroxyls and a 6.30 Asp/Glu substitution. "No HETATM candidate" and
"a PAM is bound in the pocket" are compatible but they are not the same claim,
and only the second is in our Methods.

```bash
python3 -c "
import pandas as pd
s=pd.read_csv('data/block_c/09_references/reference_survey.csv')
print(s[s.receptor_slug.isin(['FSHR','LSHR'])][['receptor_slug','role','pdb_id','status','curation_note']].to_string())"
```

**What we need.** The JSON, or one sentence per receptor naming the ligand
entity in 8I2H and 7FIJ and the rule that disqualified it. Either is enough; we
need the manuscript sentence to match the evidence behind it.

**Promised?** Yes, by filename, four times.

---

## 5. `refs/reference_set.csv` — the pinned reference set. **free**

**Manuscript locator**: `methods.tex:389–392` ("against the same pinned
reference set"); `results.tex:410–414` (AGTR1's biased-agonist reference).

**State.** Named in fourteen places in the drop; absent. Three consequences,
each of them concrete:

- **The one row-level file we hold cannot be regenerated without it.**
  `g4_full_census_v2.py` reads `anchor_positions` from `reference_set.csv` to
  build the pocket-anchor centroid that every one of the 40,000 `distance_A`
  values is measured against. We can check the census's internal arithmetic; we
  cannot check its geometry.
- **The AGTR1 sentence rests on a field we do not hold.** C-C-4 quotes
  `stabilising_elements = nanobody_beta_arrestin_biased_agonist` as the accurate
  label against an imprecise `resolved_state`. `reference_survey.csv` ships
  `resolved_state = Ga-coupled-active` and `active_stabilization_source =
  nanobody` for AGTR1/6OS2 — enough to say "nanobody", not enough to say
  "β-arrestin-biased agonist", which is what `results.tex:411` says.
- **`construct` is the column Block A's C-11 is about**, and its 29–41 %
  unreliability is a caveat we inherit and cannot re-measure.

**What we need.** The CSV. `receptor_slug`, `role`, `pdb_id`,
`anchor_positions`, `construct`, `resolved_state`, `stabilising_elements`,
`active_stabilization_source` are the columns that matter here.

**Promised?** Yes — pinned by SHA `6ee2cad8…` in `README.md` §"Provenance pins"
as the reference set Block C shares with Block B.

---

## 6. A per-cell predicate census — SC-C-6's "~65 %". **free**

**Manuscript locator**: `results.tex:353–361` and `methods.tex:405–411`, both of
which state "roughly 65 % of receptor × backbone × ligand-class cells" sit on a
saturation boundary. It is the sentence that justifies not using the predicate
at all, so it carries the whole methodological frame of the section.

**State.** **Unverifiable from anything shipped.** C-C-1 sources the figure to
`stage3_2x2_ligand_state_specificity.json` — that file carries pocket-Cα cell
means and a 2×2 interaction, and **no predicate rate of any kind**. The two
files that would carry it, `nan_reason_census.csv` and
`nan_reason_census_by_receptor.csv`, are named in `BLOCK_C_STATE_CHECK.md` and
absent. No other shipped file contains `d_npxxy_y558_y753_oh` or
`d_gpcrdb_tm6_tilt_246_637_ca` at any grain.

**What we need.** `blockc_predicate_by_cell.csv`: `receptor_slug`, `backbone`,
`arm`, `ligand_role`, `n_rows`, `n_predicate_active`, `frac_predicate_active`,
`median_d_npxxy`, `median_d_tilt`, and a `saturated` flag with its rule
(≥ 0.98 / ≤ 0.02, per E-C-4). 864 rows at most. Ask 1 supplies it implicitly.

**Promised?** The census files are named by name; the 65 % itself is attributed
to a file that does not contain it.

---

## 7. The reference-SHA × ligand-role table behind SC-C-10. **free**

**Manuscript locator**: `results.tex:436–441` — "the reference PDB they resolve
to is identical for every receptor, so there is no reference-identity
information for a classifier to exploit. We did not search for leakage and fail
to find it; the design does not admit it."

**State.** That is the strongest single sentence in the Block C section — it
converts an absence of evidence into a structural argument — and it is
**asserted in prose and nowhere else**. SC-C-10 and C-C-10 both state
"28/28 receptors with defined `pocket_ref_pdb_sha_inactive` have IDENTICAL SHAs
across all `ligand_role` values, 0/28 differ". No shipped file carries
`pocket_ref_pdb_sha_inactive`, or any per-role reference identifier, at any
grain.

Note also that 28 is neither 23 nor 15 nor 36. A fourth receptor count enters
the section here with no membership list attached.

**What we need.** Three columns × 36 receptors × 3 ligand roles — 108 rows:
`receptor_slug`, `ligand_role`, `pocket_ref_role_active`,
`pocket_ref_role_inactive`, `pocket_ref_pdb_sha_active`,
`pocket_ref_pdb_sha_inactive`. Plus the membership of the 28.

**Promised?** As a finding in `BLOCK_C_GATING_REPORT.md §G3`, not as a file.

---

## 8. SC-C-5's interval is receptor-boot where Flag C-1 says cluster-boot. **free**

**Manuscript locator**: `results.tex:397–409` — the refuted applicability
domain, "excluding a single receptor flattens it to an interval spanning zero".

**State.** Flag C-1 and SC-C-8 both declare cluster-boot over paralog clusters
authoritative for **every** CI in Block C and receptor-boot secondary. SC-C-5's
intervals are receptor-boot: `g2_refsep_vs_auroc.json.pooled_regression.bootstrap`
resamples 15 receptors, `g2_excl_agtr1.json` resamples 14. SC-C-5 is the only
surviving claim in the sheet whose interval does not follow the block's own
authoritative convention.

The regression itself **does** ship and recomputes exactly from
`05_ref_separation/g2_refsep_vs_auroc.csv` (60 rows), so we could do the
cluster-boot ourselves using the Block B paralogy map, and did:

| set | n receptors | n clusters | slope (Å⁻¹) | receptor-boot 95 % CI (shipped) | **cluster-boot 95 % CI (ours)** |
|---|---:|---:|---:|---|---|
| full 15, as-scored | 15 | 12 | −0.325 | [−0.571, −0.064] *excludes zero* | **[−1.015, +0.072]** *spans zero* |
| excluding AGTR1 | 14 | 11 | −0.060 | [−0.246, +0.087] | **[−0.282, +0.112]** |

```bash
python3 -c "
import pandas as pd, numpy as np
from scipy.stats import linregress
d=pd.read_csv('data/block_c/05_ref_separation/g2_refsep_vs_auroc.csv')
p=pd.read_csv('data/block_b/09_references/paralogy_clusters.csv')
d['cl']=d.receptor.str.upper().map(dict(zip(p.receptor.str.upper(),p.cluster_id)))
r=np.random.default_rng(1234); cl=sorted(d.cl.unique())
s=[linregress(*(lambda x:(x.pocket_ca_sep,x.auroc))(pd.concat([d[d.cl==k] for k in r.choice(cl,len(cl),True)]))).slope for _ in range(5000)]
print('full 15 cluster-boot', np.percentile(s,[2.5,97.5]).round(3))"
```

**This makes our result stronger, not weaker.** Under the block's own
convention the as-scored slope never signed either, so the applicability
hypothesis has no support at any stage — not merely after AGTR1 is removed. The
manuscript can drop the "excluding a single receptor" hedge from the load-bearing
position and keep it as a sensitivity.

**What we need.** Confirmation of the two cluster-boot intervals above (seed,
iterations and resampling unit matched to `g_scc1_cluster_boot.json`), and a
corrected SC-C-5 table. `paralogy_clusters.csv` is not requested — we hold a
byte-identical copy from Block B, SHA `6158081e…`, matching the SHA
`g_scc1_cluster_boot.json` names as its own input, and it reproduces 16 clusters
over the 23 and 12 over the 15.

**Promised?** The convention is promised twice, in Flag C-1 and SC-C-8. The
interval that follows it is not.

---

## 9. An **apo-arm** CXCR2 × OpenFold3 structure. **free**

**Manuscript locator**: `results.tex:415–418` — "CXCR2's inversion appears on
OpenFold3 and on no other backbone, and a structure from that cell shows the
ligand correctly seated in the pocket, so it is a classifier-feature effect
rather than a docking failure."

**State.** The structure that sentence rests on is
`13_structures/targeted/05_CXCR2_OF3_backbone_specific_inversion_flag_cognate_antag.cif`
— `distance_A = 6.51 Å`, in-pocket, and **cognate-arm**. The classifier it is
evidencing runs on the **apo** arm (`s1_loro_classifier.json` variant
`C_no_selfref_apo`). In the apo arm on OF3, CXCR2's small-molecule ligands are
off-site on 44 % of rows.

**The claim survives, on other evidence, and we say so.** Chai places CXCR2's
apo small molecules off-site on **100 %** of rows and still reaches AUROC 0.928;
OF3 is at 44 % and 0.135. Placement and inversion run in opposite directions, so
"classifier-feature effect, not docking failure" is right. What is wrong is the
exhibit: a cognate-arm structure cannot evidence an apo-arm claim, and a reader
who checks will find the 44 %.

```bash
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
x=c[(c.receptor=='CXCR2')&(c.arm=='apo')&(c.ligand_source=='hetatm')]
print(x.groupby('backbone').apply(lambda d: round(100*(d.distance_A>15).mean(),1)).to_dict())"
```

**What we need.** One CIF: a CXCR2 × OF3 × **apo** × neutral-antagonist
prediction, selected as the median of that cell by `distance_A`, with the rule
and the row's percentile stated. Median, not best — a best-of-cell render is
selection on outcome and will be read as such.

**Promised?** `13_structures/MANIFEST.json` promises a structure for the
"CXCR2 OF3 backbone-specific inversion flag". It delivers one from the wrong arm.

---

# Removes a stated weakness

## 10. The agonist-alone arm's state result. **free** — and the most valuable item in this document

**Manuscript locator**: none yet, and that is the point. `CLAIMS.md` C7 — *"the
agonist alone does not"* — is one of the paper's three title clauses and carries
an open `needs:` line. `CLAIMS.md:15` records it as "not testable on A or B".

**State. Block C is the first block in this project that supplies a ligand at
all, and it contains the arm.** Recomputed from the census:

| cell | rows | receptors |
|---|---:|---:|
| apo × `full_agonist` — **agonist, no partner** | **7,000** | 35 |
| cognate × `full_agonist` — **agonist + Gα, both inputs** | **7,000** | 35 |

`ligand_type` is NaN on all 32,000 Block B rows and Block A has no ligand column;
here there are 14,000 predictions across the two cells a title clause needs, and
**no state result is reported on either of them anywhere in the drop.** SC-C-6
says the predicate floor-pins in apo and ceiling-pins in cognate — which, read
plainly, *is* the C7 answer at a qualitative level — and then declines to quote
the rate.

**The instruction that blocks it, and why it needs re-adjudicating.** The
dispatch forbids connecting Block C to two-state generation (recorded at
`CLAIMS.md:31` and honoured in full — `analysis/block_c/CLAIM_TRACE.md`
§"Deliberately absent"), and Flag C-3 forbids quoting a binary-predicate rate for
a **ligand-class discrimination** claim. C7 is not a ligand-class discrimination
claim; it is a state-generation claim about a cell that happens to sit in this
campaign. Those two prohibitions may or may not be the same prohibition, and
only the people who wrote them can say.

**What we need.** Ask 6's per-cell table, restricted to `ligand_role =
full_agonist`, on both arms; plus an explicit ruling on whether a Block C
apo-agonist predicate rate may be quoted as evidence for C7. If the answer is
no, we want the reason in one sentence so it can go in the Limitations rather
than being an unexplained silence about the paper's own title.

**Promised?** No. Nobody has asked for it before. It is free.

---

## 11. `s4_bw_decomposition.json` — the only residue-level analysis in the whole paper. **free**

**Manuscript locator**: none. That is the weakness.

**State.** Named in `BLOCK_C_STATE_CHECK.md` and `SIGNAL_RECOVERY_REPORT.md`
alongside `s4_bw_position_decomposition.json`; neither ships. It is a
Ballesteros–Weinstein **position** decomposition — *which residues carry the
ligand-class signal*. Across Blocks A, B and C the paper has no residue-level
account of anything. The claim sheet itself names this as what keeps Rung 3 at
"partial": *"dominant single feature = whole-pocket-aggregate; no per-BW
activation-lever"*.

**What we need.** The JSON, or a `bw_position`, `backbone`, `importance`,
`direction` table over the twelve pocket positions.

**Promised?** Yes, by name, in two narrative reports.

---

## 12. `task6_p0_correlation.json` — the only quantitative link between blocks. **free**

**Manuscript locator**: none. W-C-2 quotes its result — Spearman ρ = 0.129,
95 % CI [−0.213, +0.443] at n = 35 — as the reason the "presence not identity"
unification was retracted, so a number from this file is already load-bearing
for a retraction we honour.

**State.** Named in `BLOCK_C_PAPER_DRAFT_v1.md`; absent. Blocks A, B and C have
never been related to one another quantitatively anywhere else.

**What we need.** The JSON, with the 35 common receptors named. A null here is
worth as much as a signal — it is what licenses treating the two interfaces as
separate subproblems, which is the Discussion's whole structure.

**Promised?** Yes, by name.

---

## 13. `task_D_species_match_root_cause.json`. **free**

**Manuscript locator**: `results.tex:348–352`, `methods.tex:383–386` — "two
receptors whose reference pair is non-human and failed a species-matching step".

**State.** We identified B1B1U5 (jumping spider) and OPSD (bovine) as the
panel's only two non-human receptors independently, from the reference tables,
before reading C-C-9; the two accounts agree. What we do not have is the
mechanism, and the mechanism decides whether the sentence is "a pipeline bug we
have fixed" or "a class of receptor this method cannot take".

**What we need.** The JSON, or `docs/AUDIT_TRAIL.md §21`, which is cited six
times across the drop and does not ship.

**Promised?** Yes, by name, twice.

---

## 14. The saturation evidence: `nan_reason_census.csv` and `nan_reason_census_by_receptor.csv`. **free**

**Manuscript locator**: `results.tex:353–361`; overlaps ask 6.

**State.** Both named in `BLOCK_C_STATE_CHECK.md`; both absent. Ask 6 asks for
the predicate rate per cell; these two carry *why a cell is unmeasurable*, which
is a different question and the one that decides whether the 8 receptors missing
an entire ligand role (below, ask 17) are a curation choice or a failure.

**What we need.** Both CSVs.

**Promised?** Yes, by name.

---

## 15. The nulls-and-ceilings set: `s7_nulls_ceilings.json`, `s7_s8_ceiling_domain.json`, `s8_applicability.json`. **free**

**Manuscript locator**: `results.tex:397–409` — the refuted applicability
domain rests on G2, and these three are the pre-registered work *behind* it.

**State.** All three named in `BLOCK_C_STATE_CHECK.md` and
`SIGNAL_RECOVERY_REPORT.md`; none ships. We report the applicability domain as
refuted; a reviewer will ask what the ceiling on it was and we have the
conclusion without the analysis.

**What we need.** The three JSONs, plus `s6_generalization.json` and
`s2_sample_budget.json` if they are cheap to include — the sample-budget result
bears directly on how many seeds a prospective user would need.

**Promised?** Yes, all five by name.

**And one more, which belongs with them**:
`task_A_v2_agonist_vs_decoy_apo_same_complex.json`, named in
`BLOCK_C_STATE_CHECK.md` and absent. Block C runs **14,400 `decoy_lig`
predictions** — 7,200 per arm — and reports no agonist-versus-decoy contrast
anywhere. The decoy role enters SC-C-2's three-class ordinal test and nothing
else; the 2×2 excludes it by construction. `CLAIMS.md:215` records
`yu2026domainmotion` — 82 enzymes, nonbinder ligands reproducing the
conformational change, ligand pLDDT insufficient to separate binders from
nonbinders — as the sharpest published challenge to our decoy arm, and this file
is the answer to it. See S4 in `rebuttals/BLOCK_C.md`.

---

## 16. SC-C-3 has no interval, and is not in the paper. **free**

**Manuscript locator**: none — and the paper's third title clause is
*confidence does not track state correctness*. SC-C-3 is the closest thing any
block has to a positive answer on confidence and it appears in no sentence.

**State.** `s3_consensus_confidence.json` reports consensus-vs-pLDDT AUROC at
top-25 % coverage as four point estimates per backbone and **no uncertainty of
any kind** — no receptor-boot, no cluster-boot, no permutation null — on a block
whose Flag C-1 declares cluster-boot authoritative for every CI. Its own
`kill_s3_verdict` field then reads `KILL_S3_DID_NOT_FIRE` with
`kill_s3_n_backbones_beat_plddt: 4`, while the claim sheet says 3 of 4 and calls
Boltz a tie. The disagreement is a Δ of **+0.0060 AUROC** being counted as a win
by one file and a tie by the other, with no interval to adjudicate between them.

**What we need.** Cluster-boot 95 % CIs on the four Δ values, over the same
paralog clusters as everything else. Four intervals. If Chai's +0.124 survives
and the other three straddle zero, that is a clean, publishable, single-backbone
result and it goes in the paper.

**Promised?** The convention is promised in Flag C-1. The intervals are not.

---

## 17. Say which of the 66 named-and-absent files are deliberate. **free**

**State.** Scanning every `.md`, `.json`, `.py` and small `.csv` in the drop for
named `.csv`/`.json` filenames and testing each against what is on disk:
**82 distinct data filenames referenced, 16 present, 66 absent (27 `.csv`,
39 `.json`).** The count matches `DISCREPANCY_REPORT.md` D-C-2 exactly. Widening
the pattern to every extension gives 280 referenced, 49 present, 231 absent —
the extra 165 are 94 reference-PDB `.cif` names, 41 `.md` documents and 29
`.py` scripts, none of which is a data file and none of which we are asking for
except `docs/AUDIT_TRAIL.md §21` (ask 13). Four adjustments we found on
re-checking the 66:

- One of the 66 is `Rows.tier3.v2.csv`, a capitalisation variant of
  `rows.tier3.v2.csv` in `BLOCK_C_WRAP_REPORT.md`. **65 distinct files.**
- Two — `g4_scoped_centroid_census.csv` and `.json` — are the **retracted v1
  census**. Their absence is correct and we are not asking for them.
- One — `paralogy_clusters.csv` — we hold, byte-identical (ask 8).
- One — `refsep_pocket_ca.csv` — **ships under a different basename.**
  `05_ref_separation/reference_separation_pocket_ca.csv` has SHA-256
  `ed8505771108beec…`, matching the pin in `README.md` §"Provenance pins"
  exactly. Not a gap.

That leaves **61 genuinely absent data files.** Grouped by what each would
unblock: source corpora and manifests (6, asks 1 and 3); reference curation (5,
ask 5); panel and ligand definition (6); pre-registered checks pr1–pr5 (5, ask
4); signal-recovery stages s2–s8 (10, asks 11, 15, 16); the task A–F audit set
(12, asks 12, 13); pose and matcher detail (6, ask 3); saturation census (2, ask
14); deferred-gate artefacts (2); Block A cross-references (4);
release-infrastructure files that are not data (3: `LEDGER.csv`, `MANIFEST.csv`,
`_rerun_plan.json`).

The bundle is **complete as declared** — all thirteen directories match the
`README.md` index, save `13_structures/`, whose index entry says 2 files where
16 are present and which the dispatch already flags as stale. What is missing is
everything the bundle *refers to*.

```bash
python3 - <<'PY'
import os,re
C='data/block_c'; on=set()
for dp,_,fn in os.walk(C): on|=set(fn)
pat=re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.\-/]*\.(?:csv|json)')
ref=set()
for dp,_,fn in os.walk(C):
    for f in fn:
        p=os.path.join(dp,f)
        if not f.endswith(('.md','.json','.py')) or os.path.getsize(p)>2_000_000: continue
        ref|={os.path.basename(m) for m in pat.findall(open(p,errors='replace').read())}
print(len(ref),'referenced;',len(ref-on),'absent')
PY
```

**What we need.** Not the files — a policy line. "Tidy data only" is a
defensible rule and would account for most of these. The bundle does not say
which of the 61 it covers, so every one of them currently reads as an oversight.

**Promised?** Each of the 61 is named as a completed piece of work with a
filename, in the drop's own documents.

---

## 18. Structures for a within-receptor, within-arm ligand-class contrast. **free**

**Manuscript locator**: the Block C section carries no figure of a structure.

**State.** `13_structures/` ships 14 CIFs, 7 targeted and 7 random, and two of
them — slots 06 and 07 — are exactly the right idea: ADRB2 × Boltz × apo ×
{agonist, antagonist}, `distance_A` 6.03 and 3.92 Å. But `MANIFEST.json` gives
their rule as the bare string `"targeted-selection"` for every targeted entry.
A pair selected on outcome and a pair selected by rule are byte-identical in
what shipped.

**What we need.** For the ADRB2 pair, the selection rule in one line — median of
its cell on which axis, and each row's percentile within the cell. If the rule
was "best", say so and we will caption it as an illustration rather than as an
exhibit. Second-best: the same pair on a receptor in the 2×2 common set with a
large per-receptor interaction, chosen by median.

**Promised?** `13_structures/README.md` promises "selection rules". The
MANIFEST carries one string for all seven.

---

## Not requested, deliberately

- **The 21-mer α5-CT arm, an agonist-only arm on a receptor panel, and a bulk
  non-Gα control.** S1–S3 in `rebuttals/BLOCK_B.md`. Campaign-level asks, filed
  once. Note that ask 10 is *not* the agonist arm S3 asks for: S3 asks for new
  predictions, ask 10 asks for a rate on 7,000 predictions that already exist.
- **Panel expansion, partner-chain sequence verification, and real
  `method`/`resolution`/`release_date` columns on the reference set.** Filed in
  `rebuttals/PANEL_EXPANSION.md`. Ask 5 depends on the third and cites it.
- **The v1 scoped census, `g4_scoped_centroid_census.{csv,json}`.** Retracted.
  Its absence is right: the retraction is recorded in prose without shipping the
  bad numbers in a form a figure script could read. We confirmed the 25.6 %
  figure does not reproduce from the corrected census under any band definition
  (pooled recomputes to 17.73 %) and that no live number in this repo carries it.
- **`paralogy_clusters.csv`.** Held, byte-identical, verified (ask 8).
- **The deferred gates G2d, G5, G6b, G7.** C-C-11 records them as
  recorded-not-followed and no manuscript sentence depends on any of them. G4 is
  the exception and it landed — the full census is the one row-level file we
  have. We would take `check2_fi_finite_subset.json`'s receptor list if it is
  free, and are not asking for the four re-runs.
- **A rebuild-and-diff harness for Block C.** `methods.tex:428–436` already says
  plainly that none exists and that file integrity, not reproduction, is what was
  verified. That is a disclosure we prefer to keep as a disclosure rather than
  convert into a deliverable someone has to build before submission.
- **CNR1's 20-anchor chain-picker path.** Real, single-receptor, and does not
  affect the metric — see open question D. Recorded, not requested.

---

# Open questions about the data itself

Not requests for new runs — questions about what we already have. Several affect
sentences currently in the manuscript.

## A. Eight receptors are missing an entire ligand role, and nothing says so

`5HT2C`, `ADA2A`, `ADRB1`, `APJ`, `DRD2`, `GHSR` and `HRH1` have **no
`neutral_antagonist` rows at all**; `HRH3` has **no `full_agonist` rows**. Each
of those eight carries 800 census rows where the other 28 carry 1,200. Cell size
is otherwise exactly 50 rows everywhere — 800 cells × 50 = 40,000, with no
exceptions.

```bash
python3 -c "
import pandas as pd
c=pd.read_csv('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv',low_memory=False)
m=c.groupby(['receptor','role']).size().unstack(fill_value=0)
print(m[(m==0).any(axis=1)])"
```

This is arithmetically consistent with the claim sheet — 36 landed × 4 × 2 × 3 ×
50 minus 8 × 4 × 2 × 50 = 40,000 — so it is not a discrepancy. But it is a
**third** panel-composition fact after the 40-vs-36 drop and the self-reference
exclusion, and no caveat mentions it. Was it curation (no clean antagonist for
those seven), dispatch, or scoring? It is also the direct reason those receptors
cannot enter the 23-receptor 2×2 common set, which C-C-3 explains only as an
intersection.

## B. `n_receptors_in_common = 23`, but the four 2×2 cells are not on the same receptors

`stage3_2x2_ligand_state_specificity.json` reports `n_receptors: {agonist: 28,
antag: 23, common: 23}` and, per cell, `cells.agonist_*.n_clusters = 28` against
`cells.antag_*.n_clusters = 23`. The **interaction** is correctly on the common
23. The four **cell means** are not: two are means over 28 receptors and two over
23, and a panel that draws all four side by side is comparing different
populations. Two questions: (i) confirm the four cell means are as-is and should
be redrawn on the common 23; (ii) the field is named `n_clusters` and holds a
receptor count — 23 receptors map to 16 clusters, so 23 cannot be a cluster
count. Is it a naming error, or is there a 23-cluster map we have not seen?

## C. SC-C-8's stated convention is contradicted by SC-C-1's own artefact

SC-C-8 and the claim sheet's Bootstrap-convention header both state
"500 receptor-boot / 500 cluster-boot / 200 permutation-null resamples; seeds
`20260910..20260920`". `g1_bootstrap_s1_auroc.json` matches exactly.
`g_scc1_cluster_boot.json` — the artefact behind SC-C-1, the block's headline —
carries `n_iter: 5000` and `rng_seed: 1234`. Our `methods.tex:401–403` follows
the artefact and says 5,000 and 1234. Which is the convention, and does SC-C-8's
sentence need correcting?

## D. `receptor_anchor_hits` is documented 0–6 and is 20 on CNR1

`g4_full_census_v2.py`'s header documents `receptor_anchor_hits (0-6; 6 = full
confidence)` and `flag_low_confidence: True if anchor_hits < 4`. The histogram
is `{6: 38800, 20: 1200}` and every one of the 1,200 is CNR1, on all four
backbones and all six cells. Hits equal target on every row, so the chain-picker
succeeded and the pocket centroid comes from `pocket_map`, not from the anchor
hits — **we checked, and this does not move `distance_A`.** CNR1's off-site rate
is 11.25 % against 17.93 % elsewhere, which is within the per-receptor spread.
Two small consequences: the documented range is wrong, and
`flag_low_confidence` can never fire (see E).

## E. `flag_low_confidence` is a self-certifying column

`False` on all 40,000 rows, and it cannot be anything else: it fires at
`anchor_hits < 4`, and the histogram's minimum is 6. A per-row quality
certificate that is a tautology given the rows that reached the file. This is
the third column of this kind across the three drops — Block A's
`matches_claim_sheet` and `passed`, Block B's `matches_claim_sheet_bool`. The
ask is the same as Block A's ask 8: emit `pass` / `fail` / `not_run`, or emit
the underlying count and let the reader threshold it.

Three more columns in the drop's CSVs carry no information:
`g4_full_census_v2.csv::note` (all-NaN), `::receptor_chain` (constant `A`),
`::ligand_seqid` (constant `1`); and
`reference_separation_pocket_ca.csv::pocket_missing` (all-NaN), `::n_pocket`
(constant 12), `::status` (constant `ok`). None of them is load-bearing; listed
so nobody spends an afternoon on them.

## F. `ligand_resname` is a slot label, not chemistry

Six distinct values across 40,000 rows: `LIG0`, `LIG1`, `LIG2`, `LIG3`, `l01`,
`PEPTIDE`. `ligand_n_heavy` is the only chemistry proxy in the file. So nothing
shipped lets us check that a `decoy_lig` is the decoy it is meant to be, or that
an agonist is the agonist named in `ligand_set_tier3.csv` (also absent). Was the
CCD code or SMILES available at census time?

## G. The KILL-S1 threshold was evaluated on the best of three feature sets

`s1_loro_classifier.json::per_backbone_best_auroc_kill_s1_row` reports Boltz
0.852, Chai **0.760**, OF3 **0.701**, Protenix 0.825, and the verdict
`KILL_S1_DID_NOT_FIRE (4/4 backbones ≥ 0.65)` is computed on those. The claim
sheet and our manuscript quote the **F\_iii** values — Chai 0.706, OF3 0.656 —
because Flag C-2 pins F\_iii. Chai's F\_ii is 0.760 and OF3's is 0.701, so the
JSON's headline field is a max over three feature sets. The verdict does not
change either way, but OF3 clears the pre-registered 0.65 by **0.0057** on
F\_iii and by 0.05 on the max. **Which feature set was pre-registered?** If it
was F\_iii, say so and the razor-thin margin goes in the text; if the test was
best-of-three, that is a multiplicity the pre-registration should name.

Separately: `s1_loro_classifier.json` reports `n_permutations: 5` and then
`permutation_p_value: 0.0` and `z_vs_null: 35.8` on every variant. At five
permutations the smallest attainable p-value is 1/6. Those two fields should be
suppressed or the permutation count raised;
`g1_bootstrap_s1_auroc.json`'s 200-resample null is the one the manuscript uses
and it is fine.

## H. The census's off-site CI treats 40,000 correlated rows as independent

`g4_full_census_v2.json::pooled.off_site_ci_95_wilson` is [0.1736, 0.1811], and
the per-arm intervals in `README.md` — apo [14.6, 15.6], cognate [19.8, 20.9] —
are the same construction. The rows are 50-sample replicates within 800 cells
over 36 receptors; a Wilson interval on n = 40,000 is not the interval anyone
wants. `results.tex:426–435` quotes the point estimates without intervals, so
nothing in the manuscript is affected — but `figures/FIGURES.md:663` carries
them into a caption, and a receptor- or cluster-bootstrapped version would cost
minutes. Ours to fix if you confirm the construction.

## I. Was `block_c_structures.zip` meant to be a different set?

It appears nowhere in the dispatch and is fully redundant with
`13_structures/`: 16 files, rooted differently, every one byte-identical by
SHA-256. Harmless. Recorded in `analysis/block_c/PROVENANCE.md` so a future
session does not re-derive which is authoritative. Worth confirming a
*different* structure set was not intended.

## J. Flag C-12 contradicts C-C-3 in the shipped files

Flag C-12 still reads "Cluster-boot CI on the 2×2 interaction NOT recomputed";
C-C-3 is marked RESOLVED and `g_scc1_cluster_boot.json` is present with the
recompute. The dispatch's §4(m) says C-C-3 wins. Confirmed by inspection and
followed. Logged only so the flag file gets corrected upstream — a later reader
of the drop alone would reach the opposite conclusion.
