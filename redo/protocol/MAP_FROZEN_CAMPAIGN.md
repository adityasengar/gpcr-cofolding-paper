# MAP_FROZEN_CAMPAIGN.md — how the frozen paper was actually run, end to end

**One document, the whole pipeline.** The six maps beside it hold the detail and the
line numbers; this one holds the shape, so that a reader can follow a prediction from
a grid declaration to a number in a figure without opening any of them. Every section
ends with **→** pointers into the detailed maps.

**What this is built on.** `paper_af3`'s delivered bundle — 433 files in `received/`:
source modules pinned by commit, the four backbone status JSONs, the coupling table,
the panel sequences, the GPCRdb cache, and the `CURATE-*` proposal documents. It is a
reading of *their code*, not a description of what anyone intended.

**Status of the campaign it describes: FROZEN AS THE RECORD.** Blocks A–D stand as
what was done. Nothing here is a defect list to fix; it is the input to the redo.

---

## 0. The pipeline in one paragraph

A campaign begins as a **grid declared in a Python builder**, never as a request file.
The builder resolves receptor sequences from a FASTA, derives seeds from a salted
SHA-256, calls one of ten pure templater functions per backbone to render the model
input file's *content as a string*, writes it, hashes it, and emits a **34-column
manifest CSV — one row per (receptor × arm × backbone × seed)**. That manifest becomes
a queue. A worker claims a row under an `flock`, exports five to seven `PRED_*`
environment variables, and runs a launcher. The launcher calls the backbone CLI once
(OpenFold3: once per 25-sample chunk), then writes `_<backbone>_status.json` beside the
outputs. **Scoring is a separate later pass** which, when the sidecar is missing,
re-discovers provenance **by parsing the output path**. Analysis then aggregates,
bootstraps and reports.

Seven stages. Each one below is: what it does, what it silently permits, where to look.

---

## 1. Panel — which receptors, and how they were picked

**48 receptors: 40 Class A + 4 Class B1 + 4 Class F.** Two forties that coincide and
are *not* the same set — the 40 Class A and the 40 receptors-with-both-states are
different populations (the latter is 32 A + 4 B + 4 F). The "40/40 match" in the
Methods is a coincidence of two forties, still carried as a `[PI]` marker.

Aditya's stated criterion: *"unique GPCRs with both active and inactive, and I picked
40 out of them."* Authorial intent, consistent with the observation, **not formally
confirmed**.

**→** `PANEL.md` §1–§5 in `redo/spec/` for the redo's re-derivation;
`rebuttals/PANEL_EXPANSION_CLASS_A.md` for the 19 Class A receptors with both states
that the panel lacks.

---

## 2. References — the state annotation, and where it really comes from

**Five stages, only two of which are code in the bundle.** This is the single most
important fact for reproduction:

```
 stage 1   reference_panel_v2.csv       human/agent curation       NOT IN BUNDLE
 stage 2   refs/reference_pdbs.csv      211 rows, 52 excluded      in bundle
 stage 3   refs/reference_set.csv       measured, 12 columns       in bundle
 stage 4   refs/reference_set.csv       enriched, 35 columns       in bundle
 stage 5   + sealed_active_refs_2026_09_01.csv
```

**`refs_build.py` does not select references. It measures a list already decided.**
There is no ranking, no filter and no admission test in `cmd_build` beyond the
`excluded` column it is handed and a species gate.

The **actual** selection rule is recoverable only from the five `CURATE-*` proposal
documents, and as practised it is:

1. enumerate every deposited structure via GPCRdb, cross-checked against RCSB;
2. keep only `state=Active`;
3. **require a transducer in the complex** — applied by rejection, not by a stated
   rule (`7EZC`, `8UGW`, `5WF5`, `3QAK`, `2YDO`, `4UHR` all rejected as agonist-only);
4. check identity anchors 3.50=R, 5.58=Y, 7.53=Y — five receptors refused outright;
5. prefer higher resolution **as a tiebreak only**, no floor;
6. require the pair to discriminate: `|d_active − d_inactive| ≥ 3.0 Å`;
7. classify the stabiliser into `{native, mini_G, chimera, nanobody, agonist_only,
   DVL_DEP}` from RCSB text, never from the Gα accession;
8. write the row.

**The consequence that matters most:** step 3 makes "active" mean *transducer-bound*.
For a paper testing whether a transducer drives the active state, that is circular —
which is why GPCRdb's activation degree was retracted as a calibration criterion and
why `g0_preflight.py` check **G0-6** exists to stop it returning.

**→** `MAP_REFERENCES.md` §1 (procedure), §3 (where the label enters), §5 (coverage:
17 receptors with no active row, 42 with no inactive), §7 (whether their calibration
and our Group 0 are comparable at all).

---

## 3. Inputs — sequences, partners, ligands, decoys

### 3.1 The receptor chain
Resolved from a FASTA by slug. Templaters are **pure functions returning the input
file's content as a string**, which is then hashed — so the input is auditable by hash
even where nothing else is.

### 3.2 The partner chain — the fact the whole redo rests on

**No arm in any block ever supplied a peptide.** Every cognate arm is receptor + **one
complete Gα subunit**. `_partner_fasta` returns a whole catalogue entry verbatim and
**cannot truncate**. And **no three-chain path exists in any backbone templater** — the
heterotrimer was never run.

This was our inference for a long time; it is now stated by the party that ran it. The
manuscript's title speaks of a 21-residue α5 C-terminal peptide; the segment actually
manipulated is **eleven** residues, and it was never supplied as a peptide at all.

### 3.3 Ligands
Two tables of different shape: `refs/ligand_set.csv` (40 rows, 8 receptors, five roles)
and `refs/ligand_set_tier3.csv` (64 rows, 32 receptors, `full_agonist` and
`neutral_antagonist` **only**).

- **No 3-D ligand preparation exists anywhere.** Ligands enter as SMILES or as amino-acid
  sequences and the fold model builds the conformer. No docking, no protonation
  assignment, no tautomer enumeration. `tautomer_note` and `protonation_ph74_note` are
  free text that **nothing reads**.
- SMILES provenance is either `CCD:<pdb>:<ccd>` (from the crystal) or a name lookup
  (`PubChem:CID<n>`, `RCSB_FASTA:`). CCD sourcing exists because the measured
  curation-error rate on memory-based SMILES was **40–46% across four verification
  passes**.
- `gate_ligand_ccd_match.py` re-fetches every `CCD:`-sourced row and compares canonical
  SMILES plus InChIKey-14. **It covers no PubChem row and no decoy.**
- Multi-ligand PDBs disambiguate by *largest formula weight after excluding waters,
  ions, lipids, detergents, buffers, glycans and cryoprotectants*, with two deliberate
  overrides where a heavier PAM co-crystallised (ACM4 → IXO not IUE; AA1R → ADN not XTD).

### 3.4 Decoys — not what "property-matched" implies

> **A decoy is a hand-picked FDA-approved drug, hard-coded one per receptor, chosen by a
> human on a "known other target, no known activity here" argument. It is verified
> against one hard gate (Morgan Tanimoto < 0.30) and *reported against* a ±20% property
> window that has no power to reject anything.**

There is **no candidate pool, no search, no property-matched draw and no random draw**.
`DECOY_SMILES` is a literal dict: 8 Tier-1 entries, 26 Tier-3. ADRB2 → tramadol,
DRD3 → mefenamic acid, AA2AR → trimethoprim, ADRB1 → aspirin, HRH1 → metformin,
CCR5 → imatinib, MCHR1 → tamoxifen. The justification per pick is prose in a second
hard-coded dict; the `paralog_review` field is a literature assertion and **no code
checks it**.

The six property axes are tested against the **mean** across the receptor's real
ligands and **no branch raises on failure** — the only consequence of any miss is a
string appended to a `notes` column. Peptide decoys are composition-preserving
scrambles of the native agonist, seeded by `SHA-256(slug|salt|variant)`.

Tier 3's 32 decoys exist **only** as that Python dict and are synthesised into the
manifest in memory, so they are **never RDKit-canonicalised** on the way into a
prediction — unlike the 8 Tier-1 decoys.

**→** `MAP_LIGANDS_AND_ANALYSIS.md` §1–§6.

---

## 4. MSAs — three backbones pair, one does not

**Three of four fetched their MSAs live over HTTP at prediction time; the fourth read a
local cache.**

| backbone | source | pairs? |
|---|---|---|
| Boltz-2 | ColabFold public API | **yes** |
| OpenFold-3 | ColabFold public API | **yes** |
| Protenix | Protenix's own MSA server | **yes** |
| Chai-1 | local `.aligned.pqt`, keyed by `sha256(sequence.upper())` | **no** |

Chai's cache is built one sequence at a time and its `pairing_key` column is empty on
every row of all 120 cache files.

**So apo → cognate is a different operation on Chai than on the other three.** On
Boltz/OF3/Protenix, adding a partner adds a *new kind of alignment* — a complex-keyed
paired search that did not exist in the apo input. On Chai it adds a second independent
single-chain MSA and nothing else. Chai reads as the "soft predictor" throughout Blocks
A/B, and **part of that may be the harness rather than the model**.

Two further facts:

- **Nothing about the MSA reaches any scored row** — not depth, not source, not pairing,
  not a hash. F-6.
- **The paired half of every cognate prediction was fetched cold**, because the pre-warm
  only ever submitted single sequences.
- **ColabFold's public API is an unpinnable live dependency.** The traced row fetched its
  MSA live; that alignment cannot be regenerated, only re-requested.
- Chai once ran **silently single-sequence** while `_chai_status.json` reported
  `ok=true`. They found, fixed and guarded it before we saw it; it appears in our tree in
  exactly one Block C narrative aside and in no claim sheet.

**→** `MAP_MSA.md` §2–§5 per backbone, §6 depths, §7 what is recorded, §8 silent failures.

---

## 5. Dispatch and launch — two paths that disagree about "done"

| | **Path A — supervisor** | **Path B — worker pool** |
|---|---|---|
| driver | `scorer/supervisor.py` | `scripts/*_worker.sh` in tmux + `qrsh` |
| unit | one `qsub` per manifest row | one claimed queue row per iteration |
| retries | automatic, ≤ 2 | **none** — `failed` is terminal |
| completion test | `_<bb>_status.json` `ok == true` | **launcher shell exit code only** |

**Blocks A–D production ran Path B.** The launchers are SGE job scripts but in
production were executed **inline inside an already-running `qrsh` session**, so their
`#$` resource directives are inert.

**→** `MAP_LIFECYCLE.md` §1 (the two paths), §3 (launch), §4 (environment contract),
§5 (failure), §6 (what lands on disk), §7 (the four status JSONs diffed), §8 (the
34-column manifest).

---

## 6. Scoring — the two-instrument predicate

**There are two instruments, and `MotifThresholds` is only one of them.**

| class | predicate |
|---|---|
| **A** | `NPxxY-OH < 9.08` **AND** `TM6 tilt > 14.932` |
| **B** | `TM6 kink < 159.95` **AND** tilt |
| **F** | tilt alone |

The conjunction lives in `block_a_campaign_analysis.py::two_instrument_state_calls()`,
operating on **per-receptor-backbone medians** — *not* in the scorer. Block A reproduces
Class A as `npxxy AND tilt` at **100.0% on 7,995 rows**; tilt overturns npxxy on 342
rows and npxxy overturns tilt on 708.

**This corrects F-1, which claimed the predicate never ran. It ran.** The 2026-09-01
collapse was *within* the motif instrument.

Two properties of the thresholds themselves:

- **9.08 is applied; 9.082 is derived** — a truncation that changes the call for one
  borderline row, and Block B's check B20 fails on exactly this.
- **159.95 has no automated check anywhere.**
- **The 80 tier-1 rows the thresholds were fitted on are identified by no file**, and
  `scripts/derive_per_class_thresholds.py` is not in the bundle. See §9.

**→** `CLAIM_VS_CODE.md`; `DECISIONS.md` F-1, F-1b, F-1c, F-3.

---

## 7. Analysis — the resampling unit is not what the pre-registration says

**Four different units are in use across ~24 implementations.** The dominant unit is the
**receptor**, and in most of those places the code, the function names and the emitted
JSON keys all call it a **cluster**.

- exactly **two** genuine paralog-cluster bootstraps
- exactly **one** seed-unit bootstrap — **uncalled**
- **four** row-unit bootstraps, one of them under the Block A primary axis

The pre-registration says: *"Seed is the unit of variance. Report CI via bootstrap over
seeds, not over rows."* And: **`refs/PREREG.md` contains the word "cluster" zero
times** — the entire cluster vocabulary is post-hoc, and "receptor" is never named as a
resampling unit there either.

**→** `MAP_LIGANDS_AND_ANALYSIS.md` §8 (unit per implementation), §9 (the seed-unit code
that has never run), §10 (statistics computed and never reported).

---

## 8. What can fail silently — the guard map

The finding that generalises all of them: **nothing in the pipeline compares output to
input** (F-9). A monomer returned where a dimer was requested passes every check. That
is precisely the gap `redo/gates/run_receipt.py` exists to close — chain count, partner
identity, seed, partner MSA depth — and there **a missing column is a FAILURE, not a
skip**.

Others, by stage: a pipeline that reports `ok=true` while running single-sequence (§4);
a completion test that is only a shell exit code (§5); a scorer that re-derives
provenance by **parsing a file path** when the sidecar is absent (§0); a self-certifying
`matches_claim_sheet` column that reads `True` where the value disagrees; an `excl_any`
union that removes 54% of Block A; decoys never canonicalised (§3.4); property windows
that cannot reject (§3.4).

**→** `MAP_LIFECYCLE.md` §9, `MAP_MSA.md` §8, `MAP_LIGANDS_AND_ANALYSIS.md` §6.

---

## 9. The three holes — what this map cannot tell you

Stated plainly, because a map that hides its gaps is worse than no map.

1. **~~The thresholds' own derivation is not reproducible.~~ ANSWERED 2026-09-12 —
   see `DECISIONS.md` F-17.** The rule is `midpoint(active_mean, inactive_mean)`
   over the 32-receptor Class A panel, with the mean taken **per receptor per role
   first** so a receptor with two PDBs does not double-weight. Reproduced here to
   within 1–1.5% from the reference set we hold — corroboration, not exact
   reproduction, because we lack the panel identity to fit on. The original text
   is left below because the *fit-set* half of the gap is still open.**
   `scripts/derive_per_class_thresholds.py` is not in the bundle and there is no
   `scripts/` directory. The 80 tier-1 rows are **identified by no file** — the only
   80-row candidate carries the literal placeholder `"X-ray or cryo-EM (schema lacks
   explicit method column)"` in `method` on all 80 rows and `"not tracked in
   reference_set schema"` in `resolution`, so no tier rule can be checked against it.
   We can say *that* calls change under a new cut and *by how much*; we cannot say *why
   9.08 sits where it does*. **This is the load-bearing gap** — the instrument is what
   both surviving title clauses rest on.
2. **Each detailed map ends with a "Questions to `paper_af3`" section, and those are not
   marked resolved.** Some were answered in conversation and never written back. Treat
   any of them as open until checked.
3. **ColabFold's public API is a live dependency that cannot be pinned** (§4).

---

## 10. Where each detailed map lives

| document | lines | covers |
|---|---:|---|
| `MAP_LIFECYCLE.md` | 1,430 | one prediction end to end: dispatch, construction, launch, failure, disk, status JSONs, the manifest, the silent-failure map |
| `BLUEPRINT_REQUEST.md` | 1,449 | what we asked them for, and §12 what we could not resolve from the bundle |
| `MAP_LIGANDS_AND_ANALYSIS.md` | 1,112 | ligand prep, the decoy rule, agonist-vs-antagonist, then the bootstrap and the resampling unit |
| `CLAIM_VS_CODE.md` | 946 | each manuscript claim against the code that produced it |
| `MAP_MSA.md` | 761 | the MSA path per backbone, depth, what is recorded |
| `MAP_REFERENCES.md` | 749 | reference selection, the state annotation, coverage and fallbacks |
| `RECEIVED_LOG.md` | 634 | the 433-file bundle, hash-verified |
| `ROWS_SPEC_DERIVED.md` | 378 | the per-row schema, derived rather than shipped |
