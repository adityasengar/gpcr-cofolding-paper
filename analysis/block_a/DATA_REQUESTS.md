# What Block A still needs from the pipeline

Paste-ready for the coding agent that owns the HPC runs. Ordered by whether a
sentence in `manuscript/sections/` currently depends on the answer, not by
effort. Every "current state" line was recomputed from `data/block_a/` today;
the recomputation is in `analysis/block_a/verify_claims.py` (47 checks, 15
mismatches) unless another command is given inline.

**Cost classes**: **free** — re-analysis of data the pipeline already holds, no
scoring, no inference. **cheap** — re-scoring existing predictions, no new
inference. **real** — new predictions.

Asks 1–9 each block or contradict a sentence that is in the `.tex` right now.
Asks 10–15 remove a stated weakness. Nothing here blocks submission.

---

## What changed since the last revision

**Resolved, and cut from the numbered list:**

- **Old item 0 — a within-receptor apo/cognate structure pair.** Delivered by
  the Block B structure bundle: `data/block_b_structures/02_ladder_arms/{apo,
  cognate}/*.cif` are the GHSR × Boltz-2 rows closest to their cell median on
  `delta_to_active`, selected by a rule written before selection ran
  (`SELECTION_RULES.md` §4.1). It is a **Block B** exhibit; a Block A panel may
  not caption it as a Block A result. For Block A's own figures the gap stands
  — see ask 12.
- **Old item 2 — active references for the eight sealed receptors.** Delivered.
  `data/block_b/09_references/reference_audit.csv` names an active-role PDB for
  every one of the eight, each carrying `ref_source = sealed`: ACM1 6OIJ,
  ADA2A 9CBL, ADRB1 7BU7, CCKAR 7MBX, DRD3 8IRT, EDNRA 8HCQ, HRH3 8YUU,
  OX2R 7L1V. The references exist; what is still missing is the rescore of
  Block A's 1,600 sealed rows against them. That converts the ask from **real**
  to **cheap** — it is now ask 10.
- **Old item 7's α5-CT request — confirmed an error and already struck.** The
  previous revision corrected it in place; this revision states the finding
  rather than the correction. **No arm in Block A supplies a 21-residue
  peptide.** `block_a_rows.csv` carries two arms only, `apo` (4,795 rows) and
  `cognate` (4,695 rows), and its three partner columns —
  `n_interface_contacts_ga_receptor`, `d_ga_alpha5_r350_ca`, `plddt_ga_alpha5`
  — are subunit-level measurements taken *on* a Gα chain, not a record of a
  peptide input. Block B's four arms are `apo`/`decoy`/`shuffled`/`cognate` and
  every partner arm there carries a complete subunit
  (`02_constructs/construct_build_report.md`: decoys byte-identical to their
  parent over the first 339–349 residues). **The α5-CT 21-mer is a region we
  measure and draw. It has never been an input.** Asking for "the 21-mer as
  supplied to the model" asked for a file that cannot exist. The real request —
  a fifth arm supplying Gα 334–354 — is S2 in `rebuttals/BLOCK_B.md` and is not
  duplicated here.
- **Old open question A** (Block A vs the older export) stays resolved; **old
  open question D1** (Protenix 0.871) stays struck. Both were our error.

**Newly found, and now numbered:** the cluster map ships 29 clusters where six
manuscript sentences say 26 (ask 4); the drop's own holdout table assigns
per-backbone training cutoffs that contradict the three dates in Methods
(ask 5); FZD4 has no cognate arm on any backbone and nothing anywhere says so
(ask 7); `passed` is `True` on all 9,490 rows with all six of its evidence
columns shipped empty (ask 8); the claim sheet's "What ships in this archive"
list names sixteen files, of which **none ship** (ask 9); and Methods'
"no statistic moves by more than 0.5%" is contradicted by the drop's own
exclusion sweep, whose maximum shift is 222% (ask 6).

---

# Blocking a sentence that is in the manuscript today

## 1. The reference-set denominators — two `[PI]` placeholders. **free**

**Manuscript locator**: `methods.tex:20` and `methods.tex:251`, both literal
`[PI:]` blocks in the compiled PDF. Also `results.tex:11`, C-6, Flag 42, D9.

**State.** Three counts are in circulation for one population and the drop
contradicts its own narrative in its own `used_for` column:

| population | claimed | `02_references/denominator_populations.csv` |
|---|---:|---:|
| panel unique PDBs | 89 (C-6) / 40 active (brief) / 41 active (C-6) | **98** — 44 active-role, 54 inactive-role |
| evaluable audit set for the 40% construct rate | 127 (C-11, Flag 42) | **162** |

`reference_metadata.csv::is_panel` is `True` on exactly 98, independently
confirming the first. Nothing in the drop reproduces 89 or 127.

**What we need.** Which population each earlier number counted, and whether
either is still the one to quote. If 89 was "unique functional references" under
some rule, name the rule; if it was an error, say so and we quote 98/44/54 and
162 and cite C-6 as the record.

**Promised?** Yes — the brief §7.1 makes stating this denominator a Methods
requirement, and C-6 ships a ready-made manuscript sentence asserting 89.

---

## 2. The panel selection rule. **free**

**Manuscript locator**: `methods.tex:17`, a literal `[PI:]` block. Long form in
`rebuttals/BLOCK_A.md` §Q-A1 and `rebuttals/PANEL_EXPANSION.md` §1.

**State.** No selection rule exists anywhere in either drop. All 40 Class A
receptors have both an active and an inactive deposited reference, 40 of 40, so
"both states solved" is almost certainly the operative criterion — but that is
inferred from the output. `lee2026confornets` counts 51 both-state pairs under a
*stricter* rule and a GPCRdb snapshot counts 86 receptors, so **no sentence may
say we took every receptor with both states**; a referee can find those numbers.

**What we need.** The rule as applied, in one paragraph: the criterion, the
snapshot date it was applied to, anything that met it and was excluded, and why.
"Every Class A receptor with both states in GPCRdb as of `<date>`, minus `<list>`"
is all it takes, and it decides whether this is a census or a sample.

**Promised?** No. Nothing in the drop claims to record it. That is the finding.

---

## 3. Provenance of the 80 tier-1 rows, and the file they came from. **free**

**Manuscript locator**: `methods.tex:118`, a literal `[PI:]` block;
`methods.tex:67` and `results.tex:15` both assert the 80-row derivation set.

**Why.** The thresholds 9.082 and 14.932 are fitted on 80 rows that carry
activation-state annotations. An instrument calibrated on a labelling cannot then
adjudicate that labelling. Published work makes the concern concrete: curated
labels come from "GPCRdb annotations, structural criteria, and ligand binding
status" — ligand-binding status is not geometry — and an unsupervised geometric
index over 1,351 class A structures recovers entries whose state was originally
interpreted incorrectly.

**The question is binary and someone already knows the answer.** Were the 80 rows
selected **by crystallographic tier**, with labels attached afterwards, or
selected **by curated state label**?

**Two things now make this sharper than in the last revision.**

- **Which 80 rows are they?** No file identifies them. Block A's
  `02_references/reference_metadata.csv` *does* carry usable
  `experimental_method` (EM 98 / X-ray 65 / 5 null) and `resolution_A`
  (163/168 populated, 1.7–6.0 Å) across 168 reference rows, so a tier rule could
  in principle be checked here — but only against the 80 rows once they are
  named. Block B's 80-row `09_references/reference_audit.csv` is the opposite
  case: it has exactly 80 rows but its `method` is the identical placeholder
  *"X-ray or cryo-EM (schema lacks explicit method column)"* on all 80 and its
  `resolution` is *"not tracked in reference_set schema"* on all 80. (Adding real
  `method` / `resolution` / `release_date` there is already request 3 of
  `rebuttals/PANEL_EXPANSION.md` and is not re-asked here.)
- **Confirm whether Block B's 80-row audit is the same 80.** Flag 2's threshold
  fit set is "80 tier-1 crystal reference rows"; Block B's reference audit is 80
  rows (40 receptors × 2 roles), and Methods' Reference-set-limitations paragraph
  already treats "the eighty" as one set. If they are not the same 80, one of
  those sentences is wrong; if they are, ask 3 closes against a file we already
  hold.

**Deliverable.** One paragraph, or the selection script, plus
`refs/thresholds_panel.csv` (SHA `242b509f7b7a`, named in Flag 2, not shipped) so
the 80 rows can be enumerated.

---

## 4. The cluster map: the drop ships 29 clusters, the manuscript says 26. **free**

**Manuscript locator**: `methods.tex:154`, `methods.tex:159`, and
`results.tex:60`, `:101`, `:246`, `:281` — six sentences, every confidence
interval in the paper.

**State.**

```bash
python3 -c "
import pandas as pd; c=pd.read_csv('data/block_a/07_clusters_and_holdout/cluster_map.csv')
v=c.cluster_id.value_counts(); print(len(v),'clusters;',(v==1).sum(),'singletons')"
# -> 29 clusters; 16 singletons
```

Methods asserts 26 clusters of which 11 are singletons (42%). The shipped map
gives 29 and 16 (55%). The drop's README concedes the mapping "was reconstructed
heuristically" and that the bootstrap draws reflect the 29-cluster operational
map — so **every cluster-boot CI in the paper was computed over 29 clusters and
is described in the text as being over 26**. That is not a rounding difference;
it changes the resampling unit.

**What we need.** The canonical 26-cluster map as a two-column CSV
(`receptor,cluster_id`), or confirmation that 29 is now correct and the
manuscript should say 29 with 16 singletons. If the canonical map is gone, say
so — we will state the reconstruction, as Block B's Methods already does.

**Promised?** Yes, twice: the claim sheet's bootstrap convention names
"26 paralog clusters (T7 manual paralogy mapping; 42% singletons)", and the
README names a "26-cluster T7 paralogy mapping".

---

## 5. Per-backbone training cutoffs — one `[PI]`, and a contradiction. **free**

**Manuscript locator**: `methods.tex:212`, a literal `[PI: confirm the OpenFold3
cutoff]`; the whole Training-set-exposure paragraph, `methods.tex:208–215`.

**State.** Methods states Boltz-2 2023-06-01, Protenix2 2021-09-30, Chai-1
2021-01-12, OpenFold3 unknown. Those three dates reproduce their 35/19/15-of-43
counts exactly against `reference_metadata.csv`. But
`07_clusters_and_holdout/holdout_counts.csv` assigns **boltz 2021-09-30** and
**chai / of3 / protenix 2023-01-13** — a different set of dates, with Boltz-2 and
Protenix2 effectively swapped, and no date matching Methods for any backbone.
Both cannot be right, and the holdout counts (`cluster_level_count` 2/0/0/0) are
computed from the second set.

**What we need.** One four-row table: `backbone, structural_training_cutoff,
source`. Then the OF3 `[PI]` closes and the holdout table can be recomputed or
retired.

**Promised?** Partly — `holdout_counts.csv` carries a `backbone_cutoff_date`
column, so the drop asserts cutoffs without sourcing them.

---

## 6. The exclusion sweep does not cover what Methods says it covers. **free**

**Manuscript locator**: `methods.tex:190–193` — "Every headline statistic was
recomputed under every exclusion combination (Table 5). No sign flip occurs
anywhere and no statistic moves by more than 0.5% from baseline."

**State.** Both halves of that sentence overreach the shipped file.

```bash
python3 -c "
import pandas as pd; e=pd.read_csv('data/block_a/08_exclusions/exclusion_sweep.csv')
print(sorted(e.metric.unique())); print(sorted(e.exclusion_set.unique()))
print('rows >0.5%%:', (e.pct_shift_from_baseline.abs()>0.5).sum(), 'of', len(e))
print('max shift %%:', e.pct_shift_from_baseline.abs().max())"
```

- **Coverage**: five metrics only — `median_tilt_shift`,
  `fraction_of_way_to_active`, `apo_active_rate`, `cognate_active_rate`,
  `tilt_active_rate`. The amplitude slopes (SC-3), the pLDDT correlations
  (SC-11), the connector delta (SC-3), the two-instrument agreement (SC-4) and
  the false-positive rate (SC-6) are not swept at all.
- **E3 is never applied on its own**, or in any combination except
  `all_E1-E5`. E3 is 4,890 rows, 51.5% of the corpus.
- **"≤0.5%" is false under either reading.** 71 of 160 rows shift by more than
  0.5% relative; the maximum is **222%** (Chai median tilt shift,
  1.047 → 3.373 Å under `all_E1-E5`). Even the fraction, the one metric the
  claim sheet scopes the number to, moves 2.9 percentage points (Chai,
  0.884 → 0.913). The sign-flip half holds: `sign_flip` is `False` on all 160
  rows and reproduces from the shipped `value` / `baseline_value` pair.

**What we need.** The sweep extended to the five unswept headline statistics and
to E3 alone; failing that, tell us and the sentence is rewritten to say exactly
which five metrics were swept and to quote the real maximum shift per metric.

**Promised?** Yes — the claim sheet's §B asserts "applied … against every
headline metric" and the brief §6 requires T5 to sweep "every statistic under
every combination".

---

## 7. FZD4 has no cognate arm, and nothing says so. **real** (to fill) / **free** (to document)

**Manuscript locator**: `methods.tex:10–12` — "380 receptor × backbone × arm
cells", "the Boltz-2 cognate arm is short 10 rows, a documented gap".

**State.** 48 receptors × 4 backbones × 2 arms is 384 cells. 380 ship. The four
absentees are `FZD4 × {boltz, chai, of3, protenix} × cognate` — **FZD4 was never
run with a partner on any backbone.**

```bash
python3 -c "
import pandas as pd,itertools
r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False)
h=set(r.groupby(['receptor','backbone','arm']).groups)
print(sorted(set(itertools.product(r.receptor.unique(),r.backbone.unique(),r.arm.unique()))-h))"
```

No file in the drop names FZD4 as the missing receptor. SC-7 quotes "n=47
receptors" for the cognate arm without saying which one is absent, and the E5
count of 500 rows is only consistent with FZD4 contributing 100 apo rows rather
than 200. Methods' "the Boltz-2 cognate arm is short 10 rows" is also
mis-attributed: the two short cells are `B1B1U5/boltz/apo` (20 rows) and
`CRHR1/boltz/cognate` (20), one in each arm.

**What we need.** Either the FZD4 cognate cells (100 predictions, **real**), or
one line stating why they were not run so Methods can say it (**free**). The
second is acceptable; silence is not, because 380 currently reads as a rounding
of 384.

**Promised?** No. This is unrecorded anywhere in the drop or in our analysis.

---

## 8. `passed` is a self-certifying column, and it certifies a broken cell. **free**

**Manuscript locator**: `methods.tex:239–246` (Known data-layer issues — "One
25-row cell passed every assertion in the verification suite because the suite
has no pLDDT floor"); C-12; Flag 46.

**State.** `block_a_rows.csv::passed` is `True` on **9,490 of 9,490** rows. Its
six evidence columns — `A1_amino_acid_identity`, `A2_fasta_completeness`,
`A3_wrong_chain`, `A4_reference_class_match`, `A5_species_match`,
`A6_receptor_identity` — are **100% NaN on every row**, which
`block_a_rows_dictionary.csv` documents as "empty on pass by design". So an
assertion suite that ran and passed and an assertion suite that never ran are
byte-identical in the shipped data. The drop itself documents one cell where the
verdict is substantively wrong: ACM1 / cognate / Protenix, 25 rows at mean pLDDT
38.7 with unfolded TM6, all `passed = True` because A1–A6 has no pLDDT floor.

This is the second column of this kind in the drop. The first was
`matches_claim_sheet` (D8), which does what it says but at a tolerance stated
only in README prose. A third, `SELECTION.md`'s "No structure was chosen for
appearance; every prediction pick is rule-driven", is contradicted by D12: the
shipped `confidently_wrong` row is 567 while the stated rule selects 552.

**What we need.** Emit A1–A6 as explicit `pass` / `fail` / `not_run` values
rather than "empty on pass", on this corpus and on every later block. One
`assertion_suite_version` column beside them would let us say which checks were
in force. Nothing needs re-running — the assertion outcomes are known at scoring
time.

**Promised?** The columns are documented in `DATA_DICTIONARY.md` as shipped
columns of the row table. They ship with no information in them.

---

## 9. The claim sheet's "What ships in this archive" list is false, item for item. **free**

**Manuscript locator**: none directly, but it is the reason asks 1, 3 and 4
cannot be closed locally — every file that would settle them is on this list.

**State.** `BLOCK_A_CLAIM_SHEET.md` §"What ships in this archive vs what is
HPC-regenerable" lists sixteen items under **Ships**. Enumerated against the
drop, **none of them is present**:

| named as shipping | in the drop |
|---|---|
| `rows.csv`, `rows.rmsd.csv`, `rows.fold_integrity.csv`, `manifest.csv` | no (only the derived `01_rows/block_a_rows.csv`) |
| `panel/refs/reference_set.csv` (post-review-frozen) | no — also named in README, C-6, C-11, Flag 42 |
| `panel/refs/sealed_active_refs_2026_09_01.csv` | no — named in README and Flag 13 |
| "the 92 reference PDB CIFs" | no — the drop holds 15 CIFs in total |
| "50 curated + random-sample predicted CIFs + renders" | no — the drop holds 4 prediction CIFs |
| `_findings.json`, `_analysis.json`, `_selected_cifs.json`, `_pull_manifest.json`, `_pull.py`, `_score_connector.py`, `_analyze.py`, `_select.py`, `RESULTS.md` | no, none of the nine |

Two more named elsewhere and absent: `refs/gpcr_coupling.csv` (SC-10's
bit-exact panel-of-record source) and `refs/thresholds_panel.csv` (Flag 2).
`LEDGER.csv`, which Flag 37 says must be updated to cluster-boot CIs before
submission, is also absent.

**What we need.** `reference_set.csv`, `sealed_active_refs_2026_09_01.csv`,
`gpcr_coupling.csv` and `thresholds_panel.csv` — four small CSVs. They close
asks 1, 3 and part of 10 without any further conversation. If the intent was
that these ship in the *release repo* rather than the zip, say so and we will
stop treating the list as a manifest.

**Promised?** Explicitly, by name, in the drop's own claim sheet.

---

# Removes a stated weakness

## 10. Rescore the eight sealed receptors against their now-named actives. **cheap**

**Manuscript locator**: `results.tex:181` ("a median over 39 receptors"), D14,
D15.

**State.** `delta_to_active`, `rmsd_to_active_ref` and `ref_pdb_sha_active` are
null on all 1,600 rows of ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R.
Consequences we currently disclose: the headline fraction is a median over **39**
receptors, not the 40 `n_receptors_fraction` claims (D15); and **610 of 4,866**
predicate-active rows have no active reference, so SC-6's false-positive rate is
2/4,256 rather than 2/4,866 (D14).

Block B has since named an active PDB for all eight (see "What changed"). The
references are no longer the missing piece.

**What we need.** Those eight predictions rescored against the named actives —
existing structures, existing scorer, no inference — returning `row_id`,
`delta_to_active`, `rmsd_to_active_ref`, `ref_pdb_sha_active` for the 1,600 rows.
If any of the eight is deliberately sealed for a pre-registration reason, say
which and the disclosure stands as written.

**Promised?** The claim sheet's SC-2 already quotes a 38–39 denominator, so the
gap is disclosed; the fix is not promised.

---

## 11. Which Gα subunit did each cognate arm supply? **free**

**Manuscript locator**: `results.tex:104` — "The arm reported here supplies the
complete cognate G$\alpha$ subunit" — and `methods.tex:213`.

**State.** Nothing in the Block A drop records the partner. `block_a_rows.csv`
has 55 columns and none names, lengths or hashes the Gα chain; the three
partner columns are geometric measurements on it. The only Gα identifiers
anywhere in `data/block_a/` are inside reference CIF files. Block B ships
`02_constructs/donor_ga_class.csv` with `cognate_ga_identity` and
`cognate_ga_class` per receptor; Block A has no equivalent, and `refs/
gpcr_coupling.csv`, which SC-10 says the panel matches bit-exactly, does not
ship (ask 9).

The sentence is almost certainly true. It is currently supported by nothing in
the block it describes.

**What we need.** A 48-row CSV: `receptor, ga_identity, ga_uniprot,
ga_sequence_length, ga_sequence_sha256`. **free** — it is the launcher's input
manifest.

**Promised?** SC-10 asserts a bit-exact match to a coupling file that is not in
the drop.

---

## 12. Coordinates for the structural figures, on a Block A receptor. **free**

**Manuscript locator**: Figs. 1–5 are all data plots; the paper carries zero
renders against a corpus that is 19% structure renders, with 68 of 78 surveyed
papers carrying at least one.

**Partly answered.** The Block B bundle supplies a within-receptor GHSR pair, so
the graphical abstract has its contrast (see "What changed"). What Block A still
lacks is a render of its own rows.

**What we need**, for **one** Class A receptor with a large clean apo→cognate
shift:

- the **median** prediction of the apo cell and of the cognate cell — median by
  `d_gpcrdb_tm6_tilt_246_637_ca`, not best-scoring — with the selection rule and
  each row's percentile within its cell;
- that receptor's deposited active and inactive references;
- the cognate Gα chain **as supplied to the model**: the whole subunit, which is
  what the cognate arm supplies. There is no 21-mer input and no file to ask for.

**Deliverable.** Five coordinate files plus a `SELECTION.md` stating the rule.
Make the rule *median*, not *best* — a best-of-cell render is selection on
outcome and will be read as such. Given D12 and D20, please also state the rule
in a form we can re-run, and do not hand-write anchor residues into it.

**Promised?** `11_structures/` promises exhibits; it ships four prediction CIFs,
none of which is a matched pair.

---

## 13. The `agonist_only_vs_ternary` exhibit is unbuildable: 8FZQ is CFTR. **free**

**Manuscript locator**: `results.tex:23–29` — the agonist-bound-without-
transducer paragraph, currently supported by prose and a citation, with no
figure.

**State.** `11_structures/agonist_only_vs_ternary/8FZQ.cif` has
`_struct.title = 'Dehosphorylated, ATP-bound human cystic fibrosis transmembrane
conductance regulator (CFTR)'` — one chain, ~1,152 Cα, ATP and Mg bound. It is an
ABC transporter. Its companion 6PT2 is correct but has nothing to contrast
against. This is the most on-thesis structural comparison in the drop and the
render cannot be built.

**What we need.** The intended δOR–Gi ternary CIF (likely one of the Wang 2023
8F7* series; Flag 29 deferred the identification). Also, since the same directory
gave us this: `broken_cell/ALIGNMENT.md` names a file `MISSING_ACM1_active.cif`
that does not exist, and `confidently_wrong/` and `success_case/` each name an
HPC absolute path rather than the file beside them.

**Promised?** Yes — `FIGURE_BRIEF.md` and `SELECTION.md` both list the exhibit.

---

## 14. A genuine high-confidence failure case, or a statement that none exists. **free**

**Manuscript locator**: `results.tex:189–213` (the confidence section); D12.

**State.** `11_structures/confidently_wrong/` does not contain one. Both the
shipped row (567) and the row its own rule selects (552) are **apo-arm**
predictions sitting 0.86–0.95 Å from the **inactive** reference — correct
predictions, correctly called inactive. `SELECTION.md` concedes the rule was
substituted because no Class A row has `rmsd_to_active_ref > 8 Å`, which is the
wrong test: an apo row is not meant to reach the active reference.

**What we need.** A query over the full corpus for rows far from the reference
**they were meant to reach** — cognate rows far from active, apo rows far from
inactive — ranked by `plddt_at_anchors`. `rmsd_to_inactive_ref` is populated on
7,890 rows, so this is largely answerable locally and we will run it; what we
need from you is the full-corpus version and, if a case exists, its coordinates.
**If no such row exists above a sensible pLDDT threshold, that is a publishable
result** and strengthens the confidence section rather than weakening it.

**Deliverable.** `row_id`, arm, both RMSDs, `plddt_at_anchors`, percentile within
cell.

---

## 15. Two loose provenance threads. **free**

Grouped because each is one line of answer.

**15a — the atom selection behind `rmsd_to_active_ref`.** Row 8285
(DRD2/OF3/cognate) ships 1.218 Å; recomputed over all 269 shared receptor Cα
against 7JVR it is 1.2952 Å, and no trimmed window reproduces the shipped value
(closest 1.2456). No file in the drop describes which atoms enter the
superposition. Nothing in the manuscript turns on it, but a shipped RMSD that
cannot be reproduced from the shipped coordinates undercuts the archive's own
reproducibility claim. **One line of Methods, no compute.** (D22)

**15b — resolve the reference SHAs to PDB IDs.** `ref_pdb_sha_active` and
`ref_pdb_sha_inactive` carry 88 distinct SHA-256 values and **no file in the drop
maps any of them to a PDB ID** — the only join is `receptor` + `state`, and that
is ambiguous for eight receptor/role slots where 2–3 candidate PDBs exist
(ADRB2 has three inactive candidates, SMO three active and two inactive; also
AA2AR, CCR5, CNR1, FZD4, FZD7). D21 had to determine empirically that ADRB2's
ΔNPxxY is measured against 3NYA rather than 2RH1. **Add
`ref_pdb_id_active` / `ref_pdb_id_inactive` to the row table, or ship a
`sha256,pdb_id` lookup.**

---

## Not requested, deliberately

- **The 21-mer arm, an agonist arm, and a bulk non-Gα control.** These are S1,
  S2 and S3 in `rebuttals/BLOCK_B.md` and they are campaign-level asks, not Block
  A gaps. Two of the paper's three title clauses depend on the first two. Filing
  them here as well would split the ask across two documents and let each be read
  as the other's duplicate.
- **Panel expansion, partner-chain sequence verification, and real
  `method`/`resolution`/`release_date` columns.** All four are already filed in
  `rebuttals/PANEL_EXPANSION.md` §§1–2 and Requests 1–3. Ask 3 above depends on
  the third of them and cites it rather than re-asking.
- **Decoy and scrambled-partner arms, the date-stratified holdout as an
  inferential test, and directional control toward the inactive state.** Later
  blocks. Results names them as explicitly out of scope for Block A and adding
  them here would blur a boundary the write-up keeps clean.
- **A detection-limit simulation for the amplitude regression.** Previously item
  5. It is a simulation over `amplitude_points.csv`, which we hold — injecting
  slopes of 0.25/0.5/0.75/1.0 and counting cluster-bootstrap replicates that
  exclude zero. We will run it here rather than ask. It stops being ours only if
  the cluster map changes (ask 4).
- **A positive control for the amplitude null.** Previously item 1, and still the
  single most valuable thing that could be added — a null is only as strong as
  the reader's confidence that the method could have detected the effect. It is
  omitted from the numbered list because every version of it is **real**: a
  graded-reference arm, a wider-range receptor set, or a Class B extension. It
  belongs in the same conversation as S1–S3, not in a Block A data request. Ask
  for it there, with a compute budget attached.
- **Retiring or widening the tilt axis.** SD(Δ_tilt_ref) is 1.17 Å against
  NPxxY's 5.22 Å across the regression set, two of four Class-A slopes are
  negative, and Results already calls the axis uninformative for amplitude. That
  is a decision we have made, not data we lack.
- **Class B and Class F rescue.** Eight receptors, four per class, excluded from
  every quantitative claim by E4. The paper is coherent as a Class A result and
  says so. Nothing is requested until a scope claim beyond Class A is wanted.
- **The 77 per-reference P5.50–F6.44 connector distances.** The README lists them
  as a known gap and the aggregate medians support the reported claim. We would
  take them if the reference CIFs arrive under ask 9, but the connector result is
  reported as direction-plus-agreement, not as a signed magnitude, and per-PDB
  distances would not change that wording.

---

# Open questions about the data itself

Not requests for new runs — questions about what we already have.

## A. ~~Is Block A a different campaign from the older export?~~ — RESOLVED 2026-09-10

It was. Only 28 of Block A's 48 receptors appeared in the earlier export, no
prediction paths coincided, it carried nine arms against Block A's two, and an
`af2mm` backbone Block A does not have. **Blocks supersede**; the earlier export
was deleted on 2026-09-10 and is in git history. Nothing further is needed.

## B. Provenance of the archive — sharper now, and still open

Was `block_a_figure_data.zip` generated by a script or assembled by hand? Not
idle: `8FZQ.cif` is CFTR (D18); **eight of eight** `ALIGNMENT.md` files carry at
least one wrong identifier, including three that name chain A as the receptor
where chain A is Gα and one that names a file the drop does not contain (D13,
D20); and the claim sheet's ships-list is wrong on all sixteen entries (ask 9).
Those are hand-assembly failure modes. **The tabular data, by contrast, is
clean**: `MANIFEST.json` lists 80 files, all 80 are present, and every SHA-256
matches. `DATA_DICTIONARY.md` matches the shipped columns exactly, file for file.
No sentinel values are present in any numeric column, as README claims.

So the working hypothesis is: **tables generated, narrative and structures
hand-made.** Confirm it and we will trust the tidy files and treat
`10_narrative/` and `11_structures/` as needing independent verification — which
is what we already do, but as a rule rather than a habit.

Related and unchanged: which version of the claim sheet was
`headline_by_backbone.csv::matches_claim_sheet` computed against, and by what?

## C. Seeds are not paired between arms — and the OF3 caveat may be wrong

Zero `seed_outer` values are shared between the apo and cognate arms on any
backbone: each cell draws its own seeds. The comparison is paired **at the cell
level and not at the seed level**. Nothing in the manuscript assumes seed
pairing and the cluster bootstrap does not require it. **Was unpaired seeding
deliberate?**

**New, and it contradicts a Methods sentence.** `methods.tex:147` says
"OpenFold3 seeds were generated as 5 × 5 outer/inner after a seeding fix, so OF3
rows are less independent than the other backbones'." The shipped seed structure
is **identical on all four backbones**: every full cell holds exactly 5 distinct
`seed_outer` values with exactly 5 rows each, on boltz, chai, of3 and protenix
alike, and `seed_inner` equals `seed_outer` on all 9,490 rows (the row dictionary
documents it as "same as seed_outer in this corpus").

```bash
python3 -c "
import pandas as pd
r=pd.read_csv('data/block_a/01_rows/block_a_rows.csv',low_memory=False)
print(r.groupby(['receptor','backbone','arm','seed_outer']).size().value_counts())
print((r.seed_outer==r.seed_inner).all())"
```

So either the OF3 qualification applies to all four backbones, or the nesting it
describes is not what these two columns record. **Which?** The answer decides
whether `methods.tex:147` is deleted, generalised to all four, or kept with a
different justification. This also retires the previous revision's item 8: the
between-seed variance component is computable locally from `seed_outer` on every
backbone, so it is not a pipeline ask.

## D. Unexplained numbers

1. ~~Protenix cognate predicate rate 0.871 vs 0.890.~~ **STRUCK 2026-09-10 — our
   error.** The shipped `active` column is class-conditional; we had recomputed
   the Class A rule on every row.
2. **`n_receptors_fraction` is 40 but only 39 receptors carry a non-null
   fraction** (D15). Which receptor is counted but absent, and why? The same
   column pattern affects `n_receptors_tilt` (48 shipped, 47 non-null) and
   `n_receptors_delta` (48 shipped, 39 non-null), and
   `plddt_correlations.csv::n_receptors` is 40 on all 12 rows where the
   population has 32 (D16).
3. **5G53 chain A** gives 18.124 / 3.716 Å against a shipped 18.097 / 3.705 —
   consistent with the shipped value coming from the structure's second receptor
   copy. Confirm which copy is canonical. Nothing currently depends on it.

## E. Can the runtime config be back-attached?

**Manuscript locator**: `methods.tex:134`, a literal `[PI:]` block.

SC-9 notes the `_status.json.runtime_config` echo "landed post-Block-A". If those
files still exist for these runs, attaching template and MSA settings per row
would convert D19 from a disclosed evidence-class caveat into a row-level fact —
the difference between "established by launcher static analysis" and "recorded
per prediction". Templates-off is load-bearing: an active-state template would be
oracle route 1, and the whole design depends on its absence. A negative answer
closes the `[PI]` too; the sentence is already written for it.

## F. The construct audit's per-PDB verdicts were never shipped — NEW

C-11 and Flag 42 quote "52 / 127 evaluable PDBs (40%) have `construct = wt`
contradicted by RCSB", and `methods.tex:249–256` states the 40% rate. **The
columns that would identify those 52 are empty.** In
`02_references/reference_metadata.csv`, `construct_contradicted_by_rcsb`,
`engineered_mutation_count` and `engineered_mutation_positions` are **100% NaN on
all 168 rows** — and therefore on all 98 panel rows, and the first two are
likewise empty on all 98 rows of `analysis/block_a/tables/S-T1_reference_set.csv`,
the supplementary reference audit that declares them as columns. Methods already
discloses this in the negative ("the engineered-mutation
count is *not* [recorded] --- that column is empty on every row"), which is
honest but leaves a supplementary table shipping three declared columns with no
data in them.

`entry_json_cached` is `True` on 163 of 168 rows, so the RCSB payloads the audit
read were cached. **Was the audit output written anywhere?** If yes, ship it as
`pdb_id, construct_on_disk, rcsb_pdbx_mutation, contradicted, mutation_count,
mutation_positions, in_predicate_window` — that is one join away from closing
Flag 42's deferred "panel-only subset audit", which is the other half of the
127-vs-162 denominator in ask 1. **free** if the audit output exists; **free**
even if it does not, since the `_entry.json` cache is held.
