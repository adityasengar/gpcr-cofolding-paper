# MAP — ligands & decoys, and the analysis layer

**What this is.** A read of `paper_af3`'s source tree as it was delivered, covering two
areas we have held no description of: (1) how ligands and decoys are chosen and how they
reach a prediction input, and (2) everything downstream of a scored row — bootstraps,
confidence intervals, and the statistics that exist but were never reported to us.

**Framing: reproduction, not audit.** The purpose is to be able to *re-run* this. Where
the code and its own prose disagree, that is recorded because the redo has to pick one,
not because someone erred. Several items below are latent hazards that this campaign
never actually tripped; they are marked as such, and a hazard that never fired is not a
defect in the delivery.

**Path convention.** Every path is relative to
`redo/protocol/received/source_bundle/` unless it starts with `redo/` or `manuscript/`.

**Dates.** Written 2026-09-11 against the bundle as unpacked. No file in the bundle was
modified.

---

# HALF ONE — LIGANDS AND DECOY SELECTION

## 1. Where ligand structures come from, and how they are prepared

### 1.1 There are two ligand tables and they are not the same shape

| file | rows | receptors | roles present |
|---|---|---|---|
| `refs/ligand_set.csv` | 40 | 8 | `none`, `decoy_lig`, `neutral_antagonist`, `inverse_agonist`, `full_agonist` |
| `refs/ligand_set_tier3.csv` | 64 | 32 | `full_agonist`, `neutral_antagonist` **only** |

Both carry 20 columns. The important ones are `smiles`, `peptide_sequence`,
`is_peptide`, `activity_class`, `bound_pdb`, `ccd_code`, `ccd_smiles`, `smiles_source`,
`affinity_metric` / `affinity_value_nM` / `affinity_source`.

**Tier 3 holds no decoy rows at all.** Its 32 decoys exist only as a hard-coded Python
dict (§2.1) and are injected into the manifest at build time —
`scripts/build_block_c_tier3_manifest.py:208-222` synthesises a `decoy_lig` row in
memory from `build_block_c_decoys.DECOY_SMILES`, tagged
`smiles_source = "scripts/build_block_c_decoys.py::DECOY_SMILES[<slug>]"`
(`:220`). Those 32 decoy SMILES are therefore never RDKit-canonicalised on the way
into a prediction — unlike the 8 Tier-1 decoys, whose canonical form is written into
the CSV (`scripts/build_block_c_decoys.py:1605-1610`, via `props["canonical_smiles"]`
at `:653`).

### 1.2 Two provenance classes, and an explicit statement of the error rate

`smiles_source` takes two forms:

- `CCD:<pdb>:<ccd>` — SMILES taken from the RCSB Chemical Component Dictionary entry
  for the ligand as it sits in a named co-crystal (e.g. `CCD:3NYA:JTZ`).
- `PubChem:CID<n>` / `RCSB_FASTA:<pdb>` / `RCSB:<pdb>:polymer_entity_N` — looked up by
  name.

`scripts/gate_ligand_ccd_match.py:15-18` states why CCD sourcing exists:

> Curation-error rate on memory-based SMILES was ~40-46% (four verification passes
> logged in `experiments/020_.../ligand_curation_notes.md`). CCD sourcing keys on the
> actual crystal chemistry rather than on named-molecule PubChem lookups.

That gate re-fetches every `CCD:`-sourced row from the RCSB Data REST API and compares
the RDKit-canonical SMILES plus the first 14 characters of the InChIKey
(`gate_ligand_ccd_match.py:5-9`). It is a pre-dispatch gate with a non-zero exit
(`:12`). **It does not cover PubChem-sourced rows**, and it does not cover any decoy
(§2.4).

### 1.3 The primary-ligand disambiguation rule at multi-ligand PDBs

`scripts/gate_ligand_ccd_match.py:22-31` — the default is *largest formula weight after
excluding waters, ions, lipids (CLR/OLA/OLC/OLB/1WV), detergents (LMT/BOG/HTG), buffers
(PGE/PG4/1PE/PEG/GOL/EDO/MES/EPE), glycans (NAG/BMA/BGC), cryoprotectants (EDT/TAM)*.
Two rows deliberately override it because a heavier PAM co-crystallised alongside the
orthosteric agonist:

- ACM4 `full_agonist` @ 7TRP → IXO (iperoxo, 0.197 kDa) not IUE (0.312 kDa, M4 PAM)
- AA1R `full_agonist` @ 7LD3 → ADN (adenosine, 0.267 kDa) not XTD (0.45 kDa, A1 PAM)

`:36-38` flags this as a rebuild hazard: the gate verifies only what the CSV declares,
so a future rebuild that picks the PAM would surface as a `ccd_code != smiles_source`
FAIL rather than as a chemistry error.

### 1.4 Preparation

No 3-D ligand preparation happens anywhere in the bundle. Ligands enter the pipeline as
**SMILES strings or amino-acid sequences** and the fold model builds the conformer.
There is no docking, no protonation-state assignment, no tautomer enumeration. The CSV
carries `tautomer_note` and `protonation_ph74_note` as free-text human annotations only
(e.g. ADRB2 antagonist: `secondary amine protonated (+1) at pH 7.4; pKa~9.5`) — nothing
reads those columns. `scripts/build_block_c_decoys.py:401-420` computes formal charge
with `Chem.GetFormalCharge`, which is the charge **as written in the SMILES**, not at
pH 7.4. This matters for §2.3.

---

## 2. How a decoy is chosen — the rule, as a procedure

**This is the headline answer and it is not what "property-matched" implies.**

### 2.1 The rule

> **A decoy is a hand-picked FDA-approved drug, hard-coded one per receptor, chosen by a
> human on a "known other target, no known activity at this receptor family" argument.
> It is then *verified* against one hard gate (Morgan Tanimoto < 0.30) and *reported
> against* a ±20 % property window that has no power to reject anything.**

Procedure, step by step:

1. **Selection — human, offline, hard-coded.** `scripts/build_block_c_decoys.py:96-282`
   is a literal dict `DECOY_SMILES: dict[str, tuple[str, str, str]]` mapping receptor
   slug → `(SMILES, common name, source string)`. Eight Tier-1 entries at `:97-172`,
   twenty-six Tier-3 entries at `:173-282`. Examples: ADRB2 → tramadol (`:98-102`),
   DRD3 → mefenamic acid, AA2AR → trimethoprim, ADRB1 → aspirin (`:168-172`),
   HRH1 → metformin, CCR5 → imatinib, MCHR1 → tamoxifen.

   There is **no candidate pool, no search, no property-matched draw, and no random
   draw.** The justification for each pick is prose in a second hard-coded dict,
   `TIER3_DECOY_ANNOTATIONS` (`:1086` onward), with fields `fda_status`,
   `primary_target`, `paralog_review`, `chosen_because`, `fallback`. The `paralog_review`
   text is a literature assertion ("IUPHAR & PubChem BindingDB: no reported affinity at
   any muscarinic subtype") — **no code checks it**; `:174-177` says the claim "rests on
   receptor-family paralog literature" with "coordinator-approved uncertainty flags".

2. **Harvest the receptor's real ligands.** `harvest_real_ligands`
   (`build_block_c_decoys.py:548-601`) reads both CSVs and keeps rows whose
   **`activity_class`** is in `REAL_ROLES = {"full_agonist", "neutral_antagonist",
   "inverse_agonist"}` (`:545`, `:575`). Note the filter is on `activity_class`, not
   `ligand_role` — rows curated as `activity_class = "NA"` are silently excluded from
   the comparison set (§6.2).

3. **Hard gate — topological dissimilarity.** Morgan fingerprint, radius 2, 1024 bits
   (`:366`); Tanimoto against every parseable real ligand; `TANIMOTO_MAX = 0.30`
   (`:364`). `_build_small_mol_report:1569-1573` raises `RuntimeError` if
   `max_t >= 0.30`, telling the operator to "Escalate to fallback candidate (edit
   DECOY_SMILES)". **This is the only gate that can reject a decoy.**

4. **Property window — reported, never enforced.** Six axes
   `PROPERTY_AXES = ("mw", "logp", "hbd", "hba", "rot", "charge")` (`:361`),
   `PROPERTY_TOLERANCE = 0.20` (`:358`), tested against the **mean** across the
   receptor's parseable real ligands (`per_receptor_property_window:613-626`).
   `_build_small_mol_report:1576-1589` records `within_tolerance` per axis into a report
   dict, and **no branch raises on failure**. The only consequence of any miss is
   `charge_missmatched` (`:1590-1592`), which appends the string
   `formal_charge_missmatched=true` to the CSV `notes` field (`:650-651`).

5. **Peptide decoys — a composition-preserving scramble of the native agonist.**
   `PEPTIDE_DECOYS` (`:294-308`) holds three: GLP1R / GLP-1(7-36) (Tier-1 legacy, gated
   off after the Step 1.5 drop), APJ / apelin-13, GHSR / ghrelin-28.
   `scramble_peptide:505-541` shuffles the native sequence with
   `random.Random(seed_from(receptor, salt, variant))` where
   `seed_from` is `SHA-256(f"{slug}|{salt}|{variant}")[:8]` (`:388-393`), retrying up to
   `MAX_SEED_RETRIES = 256` (`:346`) until Hamming distance ≥
   `max(8, round(0.65 * len(seq)))` (`:349-351`). Composition is asserted preserved
   (`:533-536`).

### 2.2 What "property-matched" means here, quantified

The module's own first line (`build_block_c_decoys.py:1`) is:

> `"""Build Block C property-matched decoy ligands for Gate 0.4 (Tier 1 + Tier 3).`

I recomputed the six axes with RDKit 2022.09.5 against the **current**
`refs/ligand_set.csv`. All 8 Tier-1 decoys pass the Tanimoto gate comfortably
(max observed T = 0.157, ADRB2 / AA2AR). **All 8 fail the ±20 % window on between three
and five of the six axes:**

| receptor | max T | axes outside ±20 % of the real-ligand mean |
|---|---|---|
| ADRB2 | 0.154 | hbd (1 vs 3.0), rot (4 vs 6.7) |
| DRD3 | 0.131 | mw (241 vs 322), logp, hbd, hba, rot |
| AA2AR | 0.157 | mw (274 vs 383), logp, hbd, hba, rot |
| ACM4 | 0.103 | logp, hbd, rot, **charge (0 vs +0.67)** |
| OX2R | 0.090 | logp, hbd, rot (12 vs 4.5) |
| ACM2 | 0.104 | logp, hbd, rot, **charge (0 vs +0.33)** |
| 5HT1B | 0.112 | logp, hbd, hba, rot, **charge (0 vs +0.5)** |
| AA1R | 0.074 | mw (346 vs 286), logp (2.2 vs 0.2), hbd |

The script's own generated prose is honest about this where it is least read: three
Tier-3 `chosen_because` strings say the pick is outside the window and was taken anyway
— `:1210` "MW 414.52 within +29% of bavisant MW 322.42 (marginally outside ±20% MW
gate; logP/HBD/HBA closer)", `:1231` "MW 371.52 within -22% of SNAP-94847 MW 494
(marginally outside strict ±20% MW gate)".

**The operative selection rule is therefore: *topologically dissimilar approved drug
with a plausible no-binding story*, not *property-matched non-binder*.** For the redo
this is the single most consequential fact in Half One, because the Block C ligand-class
contrast rests on the decoy being the right kind of negative. A decoy that is much
smaller, much less polar and uncharged where the real ligands are cationic is not a
controlled negative for pocket occupancy — it is a different experiment.

This is also the project's own recurring failure class: scope asserted in the most-read
text (the module docstring title) and withdrawn in the least-read text (a
`chosen_because` string 1,200 lines down). See `[[scope-is-asserted-where-it-is-most-read]]`.

### 2.3 The charge decision is explicit and one-directional

`build_block_c_decoys.py:18-21` — "Formal-charge mismatch is reported not raised
(Decision A — aminergic +1 anchors force neutral decoys)". Every aminergic receptor's
real ligands carry a protonated amine; every approved-drug decoy picked is neutral. So
across the aminergic panel the decoy arm differs from the ligand arms not only in
identity but **systematically in net charge**. Nothing in the pipeline corrects for it
and nothing downstream stratifies on it.

### 2.4 The gate is stale relative to the ligand set it guards

The Tanimoto summary is frozen into the CSV `notes` column at build time
(`build_small_mol_decoy_row:641-648`). Comparing those notes against the current CSV:

- **ADRB2** notes read `n=3 parseable ... T(S-(-)-propranolol)=0.159`. ADRB2's
  `neutral_antagonist` row is now **(S)-alprenolol**; its own `notes` field records
  `substituted 2026-09-04 (Step 1.1) from S-(-)-propranolol -> (S)-alprenolol`.
  The decoy gate was evaluated against a ligand that is no longer in the panel.
- **AA2AR** notes say `n=2 parseable`; the CSV now has 3 parseable real ligands.
- **OX2R** notes say `n=1 parseable`; the CSV now has 2.
- **No decoy row carries `formal_charge_missmatched=true`**, although ACM4, ACM2 and
  5HT1B now fail the charge axis on my recomputation.

`build_block_c_decoys.py` is idempotent and has a `--selfcheck` that diffs two runs
(`:1848-1900`), so re-running it would refresh all of this. It was not re-run after the
2026-09-04 ligand substitutions. Nothing in the bundle would have noticed: the notes
are a string in a CSV cell, not a checked artefact.

---

## 3. How an antagonist is chosen, and how agonist-vs-antagonist is decided

**This is curation, not code.** There is no classifier, no threshold, no assay parse.

The decision is recorded in three columns filled by hand:

- `activity_class` ∈ {`full_agonist`, `neutral_antagonist`, `inverse_agonist`,
  `decoy_lig`, `NA`, ``}
- `affinity_metric` / `affinity_value_nM` / `affinity_source` — e.g. ADRB2
  neutral_antagonist: `Ki`, `4.0`, `Baker 2005 Br J Pharmacol 144:317 PMID:15655528;
  Wacker 2010 JACS 132:11443 PMID:20690642`
- `bound_pdb` — the co-crystal the ligand is taken from

The stated criterion appears only inside a skip comment:
`scripts/build_block_c_tier1_manifest.py:15-18` —

> OX2R, 5HT1B, AA1R have `activity_class=NA` on their inverse_agonist row (**no clean
> CAM-assay-classified inverse agonist with < 100 nM affinity** meeting the amendment
> criteria).

So the operative rule is *classified by a constitutive-activity (CAM) assay in the
literature, with affinity < 100 nM, and with a co-crystal*. The amendment that defines
it (`PREREG` amendment § C-2 / § C-13(f)) is referenced but the amendment text is not in
the bundle.

The **antagonist-side reference structures** are curated separately in
`refs/pending_curation_block_c.csv` and `refs/pending_curation_block_c_tier3.csv`, one
row per (receptor, role) with `resolved_state` ∈
{`inactive-neutral-antagonist`, `inactive-inverse-agonist`}, the PDB, the CCD code, the
resolution, the deposition date and a PMID. Example row:
`ADRB2, inactive_inverse_agonist, 2RH1, ..., ligand_ccd=CAU; ligand=carazolol;
resolution=2.40; deposited=2007-10-05; source=PMID:17962520 (Cherezov 2007)`.
`refs/pending_curation_block_c_tier3_notes.md:5-16` gives the sidecar shape: 42 rows
over 40 receptors, 18 mirrored from Tier 1, 20 newly curated, 5 with `pdb_id=NA`.

**Where the agonist/antagonist distinction actually bites in the scoring:**
`scorer/pocket_metrics.py:928-990`. `_role_for_state_claim` picks which crystal the
prediction is compared against, and — for Block C — it keys on `ligand_role`, not on
the row's `state_claim`:

```
full_agonist        → active reference
neutral_antagonist  → inactive, role_specific = inactive_neutral_antagonist
inverse_agonist     → inactive, role_specific = inactive_inverse_agonist
none / decoy_lig    → active reference
```
(`pocket_metrics.py:975-981`.) Every Block C manifest row carries
`state_claim = "Ga-coupled-active"` unconditionally
(`build_block_c_tier1_manifest.py:312`), which `:944-947` documents as deliberate:
"which is what Block C dispatches on every row so the run tests whether the model
behaves activated-like when fed each ligand".

**Consequence worth stating plainly:** a `decoy_lig` row is scored against the **active**
reference, same as a full agonist. The decoy is a negative control for ligand identity
and simultaneously carries the agonist's reference assignment.

---

## 4. What `build_shuffled_decoy_constructs.py` shuffles, exactly

**It shuffles the last 11 residues of a Gα subunit. It has nothing to do with ligands.**

This script builds **partner-chain** arms for Block B, not ligand arms. Two arms, and
only one of them is a shuffle:

### 4.1 The `decoy` arm — a scramble of 11 residues

`build_shuffled_decoy_constructs.py:70-72`:
```python
# α5-CT length (residues). Matches the plan: "the C-terminal ~11 residues
# of the Gα α5 helix (the RECOGNITION SEQUENCE)".
A5_CT_LEN = 11
```

The α5-CT is defined *positionally*: `a5_ct = seq[-A5_CT_LEN:]` (`:303`) — the last 11
characters of the UniProt sequence. There is no CGN numbering, no structural definition,
no alignment. This is the same absence recorded in `redo/spec/DECISIONS.md` F-4.

The decoy construct is `cognate_seq[:-11] + scrambled_ct` (`:395`), i.e. the **full
cognate Gα scaffold with its final 11 residues permuted**, composition preserved,
Hamming ≥ `MIN_HAMMING = 5` (`:123`), deterministic seed
`SHA-256(f"{slug}|block_b_decoy_v1|{variant}")` (`:175-179`, salt at `:117`), up to
`MAX_SEED_RETRIES = 64` (`:124`). Two hard asserts follow: composition preserved
(`:405-407`) and scaffold unchanged (`:408-410`).

Verified against the delivered artefacts: `refs/constructs_block_b/adrb2_decoy.fasta`
header reads `alpha5_ct_original=QRMHLRQYELL | alpha5_ct_scrambled=MLELRYQLHRQ |
scramble_seed=5005397641416405544 | hamming=10 | length=394`. 394 aa is full-length
GNAS. **No arm here is a peptide** — both arms are complete Gα subunits.

Five canonical Gα, one per class, in `GA_BY_CLASS` (`:78-84`): Gs/GNAS/P63092,
Gi/GNAI1/P63096, Gq/GNAQ/P50148, G12/GNA13/Q14344, Gt/GNAT1/P11488. Across the 40
receptors only **four distinct α5-CTs** appear — `IKNNLKDCGLF` (Gi, 24 receptors),
`LQLNLKEYNLV` (Gq, 10), `QRMHLRQYELL` (Gs, 5), `IKENLKDCGLF` (Gt, 1). Each receptor gets
its own seeded permutation of its class's CT, so there are 40 distinct decoy sequences
built on 4 distinct compositions.

### 4.2 The `shuffled` arm — not a shuffle at all

`:8-12`: "receptor + **full non-cognate Gα** (wrong family)". No sequence is permuted;
a different real Gα is substituted. The choice rule (`pick_shuffled_class:218-263`):

1. Collapse families: `{Gt, Go, Gz} → Gi`, `{G11} → Gq`, `{G13} → G12` (`:88-97`).
2. Try `DEFAULT_SWAP = {Gs: Gi, Gi: Gs, Gq: Gs, G12: Gq}` (`:107-112`).
3. If that target is in the receptor's coupled set, fall back to the first entry of
   `FALLBACK_ORDER = [Gi, Gs, Gq, G12]` not in that set (`:113`, `:256-258`).

The generated report asserts this "gives **balanced Gs↔Gi coverage**" (`:544`). It does
not. Because both `Gi → Gs` and `Gq → Gs` point at Gs, and the panel is 24 Gi + 10 Gq,
the realised distribution over the 40 receptors is:

| shuffled partner | receptors |
|---|---|
| Gαs | **33** |
| Gαi | 6 |
| Gα12 | 1 |

(counted from `refs/constructs_block_b/build_manifest.csv`.) Gt/`alphat` is emitted into
`refs/partner_gα_by_class.csv` and is never used as a shuffled partner —
`FALLBACK_ORDER` does not contain it. So the shuffled arm has **3 distinct partner
sequences across 320 manifest rows** (verified: `len(set(partner_seq_sha))` = 3), and
"non-cognate" is 82.5 % synonymous with "Gαs".

### 4.3 Outputs

`refs/partner_gα_by_class.csv`, 80 FASTAs in `refs/constructs_block_b/`, and
`build_manifest.csv` with 320 rows = 40 receptors × 2 arms × 4 backbones (verified).

---

## 5. How a ligand reaches a prediction input

**Chain assignment.** A small molecule becomes chain **`L`**, a separate non-protein
entity. A peptide ligand becomes an **extra protein chain**, also `L` on Boltz/OF3.
The receptor is chain `A`; a Gα partner is chain `B`.

**Templater path** — all four emitters live in `scorer/propose.py`:

| backbone | function | small molecule | peptide |
|---|---|---|---|
| Boltz-2 | `_boltz_ligand_block:400-428` | `- ligand: {id: L, smiles: '<smi>'}` (`:422-427`) | `- protein: {id: L, sequence: <seq>}` (`:417-421`) |
| OpenFold3 | `_of3_ligand_chain:492-512` | `{molecule_type: LIGAND, chain_ids: [L], smiles}` or `ccd_codes: [<code>]` when the string starts `CCD:` (`:505-511`) | `{molecule_type: PROTEIN, chain_ids: [L], sequence}` (`:502-504`) |
| Protenix | `_protenix_ligand_entry:545-571` | `{"ligand": {"ligand": "CCD_<code>" or "<smi>", "count": 1}}` (`:565-570`) | `{"proteinChain": {sequence, count: 1}}` (`:563-564`) |
| Chai-1 | `_chai_ligand_fasta:625-648` | `>ligand\|name=lig\n<smiles or ccd>` (`:640-646`) | `>protein\|name=lig\n<seq>` (`:638-639`) |

**Validation before emission.** `_validate_ligand_block:193-226` enforces:
`peptide` requires `sequence` and forbids `smiles`; `small_molecule` requires `smiles`
and forbids `sequence`; `apo`/`none` forbid both. Absent `ligand:` block defaults to
`{"type": "none"}` (`:181-183`).

**Where `ligand_type` is decided.** Tier 1:
`ligand_type = "small_molecule" if smiles and ligand_role != "none" else ""`
(`build_block_c_tier1_manifest.py:238-239`) — **Tier 1 never dispatches a peptide
ligand.** Tier 3 does: `build_block_c_tier3_manifest.py:383-388` sets
`"peptide"` when `is_peptide` is TRUE or a `peptide_sequence` exists with no SMILES.
15 of the 64 Tier-3 ligand rows are `is_peptide=TRUE`.

**How the ligand is found again in the output structure.**
`scorer/pocket_metrics.py:714+` `ligand_rmsd_to_ref` sweeps every chain of the model,
excluding standard amino acids on the receptor chain and on any chain with
≥ `_GPROTEIN_LEN_THRESHOLD = 50` standard residues (`:820`). The comment at `:806-819`
records the 2026-09-07 fix this replaced: before it, Gα amino acids entered the ligand
atom pool and MCS "found spurious substructure matches on Gα, producing garbage
`ligand_rmsd_to_ref` values (e.g. **96 Å on DRD2 full_agonist × cognate × Chai**)".

**The ligand–reference matcher** (asked about as "the rdkit/MCS matcher") is two-stage,
and the module header does not say so:

1. `(atom_name, element)` exact pairing — the fast path, kept byte-identical for
   OF3/Protenix which preserve CCD atom names.
2. RDKit MCS fallback (`_mcs_ligand_rmsd:583-711`) when the fast path yields fewer than
   `MCS_FALLBACK_MIN_MATCHED = 5` matches (`:506`) **or** when matched atoms cover less
   than `MCS_FALLBACK_MIN_COVERAGE = 0.8` of either side (`:508-517`, "Bug #4 fix
   2026-09-07"). Molecules are built from a synthetic PDB block with
   `proximityBonding=True` (`:549-582`); `rdFMCS.FindMCS` runs with
   `CompareElements` / `BondCompare.CompareAny` / `ringMatchesRingOnly=True` /
   `completeRingsOnly=True` / `timeout=5` (`:612-622`).

Two documented bug fixes inside that fallback are worth carrying forward because they
quantify how wrong the pre-fix numbers were. `:664-673`: the previous version used
`GetSubstructMatch` (singular) independently on both molecules, so any symmetry in the
MCS query produced a pairing driven by atom-order-in-file rather than geometry —
"**Reviewer test: 57 % of true docks were miscalled as failures under random atom
orderings; direction of error was both inflating and deflating.**" The fix enumerates
all matches (`uniquify=False`, capped at `_MAX_MATCHES = 256`) and minimises.

---

## 6. What can go wrong silently here

Ordered by how much a manuscript sentence would depend on it.

### 6.1 The Block C "cognate" arm is Gαs for every receptor — **highest severity**

`scripts/build_block_c_tier1_manifest.py:104` and
`scripts/build_block_c_tier3_manifest.py:150`:

```python
COGNATE_PARTNER_IDENTITY = "alphas"
```

Used unconditionally for the non-apo arm — tier1 `:250-251`, tier3 `:398-399`. There is
no per-receptor lookup. Cross-referencing `refs/gpcr_coupling.csv`:

- **Tier 1: 6 of 8** receptors are not Gs-coupled (DRD3, ACM4, ACM2, 5HT1B, AA1R = Gi;
  OX2R = Gq). Only ADRB2 and AA2AR are Gs.
- **Tier 3: 29 of 32** are not Gs-coupled (19 Gi, 9 Gq, 1 Gt).

So in **35 of 40 Block C receptors the arm named `cognate`, and recorded in the manifest
as `partner_identity=alphas`, carries a non-cognate Gα.**

This is not a subtle judgement call — the codebase names it as a known bug class.
`scripts/build_block_a_manifest.py:50-51`: "**A blanket alphas would recreate the W54
taxonomy failure.**" Again at `:65-66`, `:121-123`, `:178-180`. Block A resolves the
partner per receptor from `gpcr_coupling.csv` via a `COGNATE_LOOKUP_SENTINEL`
(`:181`, `:206-210`). There is a dedicated verifier,
`scripts/verify_cognate_identity.py:10-12` — "Guards against the founding W54 taxonomy
failure: a blanket alphas partner applied to all 40 receptors regardless of documented
primary G-protein coupling. **Fails LOUD on any mismatch.**" It takes a `--manifest`
argument and, on this evidence, was never pointed at a Block C manifest.

**Nothing in the bundle documents this as intentional for Block C.** Grepping the two
Block C experiment directories for `alphas` returns nothing (those directories are
empty in the delivery). This goes to §8 as a question, not as a verdict — but the redo
must not inherit it either way.

### 6.2 `activity_class = "NA"` rows silently shrink the decoy comparison set

`harvest_real_ligands` filters on `activity_class ∈ REAL_ROLES`
(`build_block_c_decoys.py:545`, `:575`). Three Tier-1 rows and 14 Tier-3 rows carry
`activity_class = "NA"`. Those receptors' property window and Tanimoto gate are computed
over 1–2 ligands instead of 3, with no warning: `mean_and_sigma:603-611` returns
`sigma = 0.0` for a single value, and `per_receptor_property_window` reports a mean of
one. OX2R's decoy note records `n=1 parseable` — a ±20 % window around a single
molecule. The only guard is `_build_small_mol_report:1550-1554`, which raises only when
the count reaches **zero**.

### 6.3 The decoy verification notes can drift from the ligand set without any check

Demonstrated in §2.4. The Tanimoto values, the ligand names they were computed against,
and the `formal_charge_missmatched` flag are frozen strings in a CSV cell. Nothing
recomputes them and nothing compares them to the current CSV. `analysis/audit_asks.py`
on our side has an analogue of the right idea; there is no equivalent here.

### 6.4 `CSV_HEADER` in the decoy builder is 17 columns; `ligand_set.csv` has 20

`build_block_c_decoys.py:449-467` lists 17 fields. The live CSV has 20 — `ccd_code`,
`ccd_smiles`, `smiles_source` were added later. `parse_row_dict:484-490` does
`dict(zip(CSV_HEADER, r))`, which truncates at 17, and `format_csv_row:492-499` writes
17. Re-running the builder today would therefore **drop three columns from the 8 decoy
rows it rewrites**, and the byte-integrity check (`verify_non_decoy_byte_integrity:773-801`)
would not catch it because it exempts exactly the rows being rewritten
(`build_all:1799-1807`). This is latent — the delivered CSV has 20 fields on all 40 rows
— but it is a live trap for anyone who re-runs the generator.

### 6.5 Boltz is the only backbone with no `CCD:` branch

`_of3_ligand_chain:507-509`, `_protenix_ligand_entry:565-567` and
`_chai_ligand_fasta:643-645` all detect a `CCD:`-prefixed string. `_boltz_ligand_block`
(`:422-427`) emits `smiles: '<string>'` verbatim with no check. A `CCD:JTZ` string
reaching that path becomes a literal SMILES and would either fail to parse or silently
produce something else. **Latent in this campaign** — see §7.1.

### 6.6 A peptide ligand would inherit the receptor's MSA

`_protenix_apply_msa_paths:574-598` assigns `unpairedMsaPath`/`pairedMsaPath` to **every**
`proteinChain` when `msa_a3m_path` is a plain string, and the ligand entry is appended
to `seqs` *before* it runs (`:607-609`, `:621-623`). `_of3_apply_msa_paths:431-472` skips
non-PROTEIN chains — which correctly excludes small molecules but **not** a peptide
ligand, which is `molecule_type: PROTEIN` with `chain_ids: ["L"]`. A dict-valued
`msa_a3m_path` is safe (the key would be absent); a string-valued one is not.

Related, in the same region: `_of3_json_monomer:521-524` comments "A monomer receptor +
a ligand still uses paired-MSA logic OFF" and then computes
`is_multimer = sum(1 for c in chains if molecule_type == "PROTEIN") > 1`, which is
**True** when a peptide ligand is attached. Comment and code disagree.
**Latent in this campaign** — see §7.1.

### 6.7 `ligand_rmsd_to_ref` computes a meaningless number on decoy rows, by design

`scorer/pocket_metrics.py:48-54` and `:785-789`:

> **Consumers of `ligand_rmsd_to_ref` MUST filter `decoy_lig` rows via the manifest /
> spec.** The scorer does not have a decoy flag on the row and will happily compute a
> pose distance between a decoy ligand and a real-ligand reference — that number is
> meaningless. This is Ambiguity #4 (approved 2026-09-03) and is the documented posture;
> **the analysis layer owns the filter.**

The scorer emits the number; a downstream script must drop it. That is a contract
between files with no enforcement at either end. We do not hold `rows.tier3.v2.csv`, so
we cannot check whether the filter was applied.

### 6.8 The construct builder drops receptors on stdout and exits 0

`build_shuffled_decoy_constructs.py` collects `ambiguous_couplings` and
`same_class_bugs` and `continue`s past the receptor (`:355-358`, `:365-371`, `:398-404`).
At the end it **prints** them (`:488-496`) including a line literally reading
`"{n} SAME-CLASS-BUG rows (must be 0)"` — and returns normally. A run producing 37
constructs instead of 40 is distinguishable from a clean run only by reading terminal
output. This campaign built all 40 (81 files = 40 × 2 + manifest, verified), so it never
fired.

### 6.9 `receptor_seq_sha` is promised and never written

`build_shuffled_decoy_constructs.py:456`:
```python
"receptor_seq_sha": "",  # filled in below if we resolve it
```
There is no "below" — that is the only occurrence of the name in the file. All 320 rows
of the delivered `build_manifest.csv` have it empty (verified). A column that looks like
provenance and carries none.

### 6.10 The scorer's own module headers describe superseded behaviour

Two instances, both the pattern `[[scope-is-asserted-where-it-is-most-read]]`:

- `scorer/pocket_metrics.py:37-47` (module header) describes ligand matching as
  "Match reference ligand atoms by (atom_name, element) **exactly**; if the ligand
  identity differs ... the comparison is undefined and returns NaN". The MCS fallback,
  added 2026-09-06, is documented only in the function docstring 700 lines lower
  (`:748-757`).
- `ligand_rmsd_to_ref`'s own docstring (`:752`) says MCS runs with `CompareOrder`; the
  code (`:617-619`) uses `BondCompare.CompareAny`, with an inline comment explaining
  that `CompareOrder` was vacuous under `proximityBonding`.

This is the same failure `redo/spec/DECISIONS.md` F-1 records for
`scorer/switch_signal.py`. It is not a one-off; it is how this codebase ages.

---

# HALF TWO — THE ANALYSIS LAYER

## 7. Preliminary: what this half could and could not be checked against

The bundle ships the analysis **code** but almost none of the row-level data it reads.
Absent and referenced: `experiments/021_.../analysis/rows.tier3.v2.csv`,
`experiments/019_.../analysis/paralogy_clusters.csv`,
`experiments/018_.../analysis/rows.csv`, and the entire
`experiments/020_block_c_ligand_pharmacology/` tree (the directory does not exist).
`experiments/` in the bundle contains exactly one file:
`019_block_b_partner_selection/analysis/msa_depth_report.md`. So every statement below
is about code, verified by reading it; none is a recomputation.

**A scripts/analyse_switch_signal.py does not exist in the bundle.** It was named in my
brief and is named by `scorer/switch_signal.py:31-32` as its own wrapper. `find` for it
returns only `scorer/switch_signal.py`. This matters a great deal — see §9.

---

## 8. The bootstrap: where the resampling unit is the cluster, the receptor, and the row

**Direct answer.** Four different units are in use across ~24 implementations. The
dominant unit is the **receptor**, and in most of those places the code, the function
names and the emitted JSON keys all call it a **cluster**. There are exactly **two**
genuine paralog-cluster bootstraps, exactly **one** seed-unit bootstrap (uncalled), and
**four** row-unit bootstraps, one of which sits under the Block A primary axis.

### 8.1 What was pre-registered

`refs/PREREG.md:222-223`:
> Aggregate each arm to a **per-seed mean** first (variance-of-variance safe) ...
> **Seed is the unit of variance.** Report CI via bootstrap over seeds, not over rows.

`refs/PREREG.md:225`:
> **Not done**: pairwise row-by-row subtraction across arms.

`refs/PREREG.md:521`:
> **Seed as unit of variance** — `per_seed_mean()` collapses to seed-level; bootstrap CI
> never over rows.

**`refs/PREREG.md` contains the word "cluster" zero times** — verified,
`grep -ci cluster refs/PREREG.md` → `0`. The whole cluster vocabulary is post-hoc;
"receptor" is never named as a resampling unit in the pre-registration either.

### 8.2 The unit, per implementation

| unit actually resampled | where |
|---|---|
| **per-seed means** | `scorer/switch_signal.py:169-186` — and nothing calls it (§9) |
| **receptor**, labelled "cluster" | ~18 implementations; the bulk of the corpus |
| **paralog cluster**, genuinely | `scripts/block_c_closeout/g1_bootstrap_s1_auroc.py:223-259`; `scripts/block_c_closeout/recompute_2x2_cluster_boot.py:127-153` |
| **row / individual prediction** | `scripts/post_audit_corrections/task_f_block_a_recheck.py:45-58`; `task_aa2ar_unimodal_block_a_counter.py:94-106`; `scripts/reaudit_2026_09_07/s3_cross_backbone_consensus.py:303-322`; `scripts/block_c_closeout/g2_refsep_vs_auroc.py:209-214` |

### 8.3 The three label-vs-code mismatches

**(a) "two-stage cluster … then seeds within receptor" — there is no second stage.**

`scripts/analyse_block_c_tier1_headline.py:32-34` (verified by direct read):
> **Bootstrap**: two-stage cluster — resample receptors within group, then seeds within
> receptor. 10,000 replicates.

Worse, that claim is **written into the provenance JSON the analysis emits** —
`analyse_block_c_tier1_headline.py:601-604`:
```json
"bootstrap": {"type": "two_stage_cluster_resample_receptors_then_seeds", ...}
```
`analyse_block_c_tier3_headline.py:30-32` and `:634-636` are identical.

The implementation, `bootstrap_receptor_mean:181-205`, is **one loop over receptor-level
scalars**:
```python
clean = [v for v in per_receptor_values.values() if ...]   # one scalar per receptor
sample = [clean[rng.randint(0, k - 1)] for _ in range(k)]
```
No seed is ever drawn. The per-receptor scalar it consumes comes from
`cell_fraction_active` (`tier1:158-166`), which iterates
`for _seed, rows in seeds_dict.items(): for r in rows:` — the seed level is **built and
then discarded**. Tier 3 is character-identical at `:176-198` and `:153-161`.

This is precisely the failure the brief flagged: *a claim sheet labelled one unit and
computed another*. Here the label is not in a claim sheet — it is in a machine-emitted
provenance field, which is the most-trusted place it could possibly be.

**(b) "cluster" means "receptor" throughout `lib_common` and `stage3`.**

`scripts/post_audit_corrections/lib_common.py` defines `cluster_bootstrap_diff` (`:97`),
`cluster_bootstrap_two_group_diff` (`:130`), `cluster_bootstrap_interaction` (`:161`);
all resample keys of a receptor-keyed dict and return `"n_clusters": len(common)`
(`:124`) — a receptor count reported under a cluster name.

`scripts/stage3_post_audit_analysis.py:157-187` `_cluster_bootstrap_ci` — verified by
direct read: `clusters = list(values_by_cluster.keys())` (`:165`),
`sample = [rng.choice(clusters) for _ in range(n_c)]` (`:177`), and those keys are
receptor slugs (`:238-242`, `agonist_active.setdefault(recep, [])`). The file's own
header is honest — `:16-17` "Cluster-bootstrap CIs use the **receptor** as the
resampling unit" — while every function and variable name says cluster.

The campaign audited itself on this and wrote the answer down:
`scripts/reaudit_2026_09_07/t2_bootstrap_sanity.py:112,127,134` records `"cluster":
"receptor"` for all three traced implementations.

**(c) A comment says mean-of-means; the line under it computes a row-pooled mean.**

`stage3_post_audit_analysis.py:286-287`, verified by direct read:
```python
# Point estimate: pool per-receptor cell means, not per-row.
ag_a = _mean([v for c in common_list for v in agonist_active[c]])
```
That is a flat mean over every row of every receptor. A receptor with 200 surviving rows
outweighs one with 20. The same construction is at `:171-172` (under the comment "pool
across clusters **uniformly**"), `:276-279`, `:489-490`, `:496-497`, and throughout
`lib_common.py:112-119,145-152,173-184`.

`t2_bootstrap_sanity.py:393-396` records the caveat that this is only equivalent to a
mean-of-means "under balanced n_rows per receptor" — which, after NaN drops, it is not.

**Two weighting schemes coexist under identical output keys.**
`task_a_v2_agonist_vs_decoy_apo.py:50-79` genuinely takes the mean of per-receptor means
(`per_r = [_mean(values_by_receptor[k]) for k in sample_keys]`, `:64`), unlike
`lib_common`'s row-pooled version — and `task_a_v2` calls **both** in the same loop
(`:174-176`), each emitting `"est"`/`"ci_lo"`/`"ci_hi"`/`"n_clusters"`. Nothing in the
output distinguishes them.

### 8.4 The Block A primary axis is bootstrapped over rows

`scripts/post_audit_corrections/task_f_block_a_recheck.py`, verified by direct read.
Section comment `:148-151`: "Continuous cognate−apo effect on d_tm6 (**Block A primary
axis**) per backbone + Class A (**main claim**)."

`bootstrap_diff_ci:45-58` does `sa = [rng.choice(a) for _ in range(len(a))]` — and it is
called at `:177` with `d["cog"]` / `d["apo"]`, which are appended **one element per row**
(`:169`, `:172`). The output keys name the unit out loud: `"n_apo_rows"`, `"n_cog_rows"`
(`:179-180`).

**The receptor-level aggregation is collected and then never read.**
`per_receptor_dtm6` is created at `:154` and appended at `:170` and `:173`; `grep` for
the name in the file returns exactly those three lines. The intent was there; the CI
does not use it. The interval is anticonservative by whatever the intra-receptor
correlation is, and it contravenes `PREREG.md:223` directly.

One thing it *does* get right: the two arms are resampled independently and the means
subtracted, which honours `PREREG.md:225` (no cross-arm row pairing).

### 8.5 The only two real cluster bootstraps — and the file that defines the clusters is missing

`scripts/block_c_closeout/g1_bootstrap_s1_auroc.py` is the one place where
receptor-boot and cluster-boot are run **side by side on the same statistic**
(`receptor_bootstrap_ci:196-220`, `cluster_bootstrap_ci:223-259`), which is the right
design. The cluster version draws `n_cl` clusters with replacement (`:240`) and then
takes every receptor of each drawn cluster with multiplicity (`:242-244`).
`N_ITER = 500` (`:54`), `RNG_SEED = 20260910` (`:56`).

Its clusters come from `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
(`:42`), described at `:19-20` as "Block B's paralog clusters (26 clusters over 40 Class
A + Class B + Class F receptors)". **That file is not in the bundle** — verified,
`find . -name "paralogy_clusters*"` returns nothing, and that analysis directory contains
only `msa_depth_report.md`. No script in the bundle constructs it, and there is no
`mmseqs` / `cd-hit` / sequence-identity clustering anywhere. So the clustering is by
paralogy/family judgement and its provenance is outside what we hold.

**Silent-degradation hazard.** `load_clusters:183-188` returns `{}` if the CSV is
missing, and `:230` then does `cluster_map.get(r, f"single_{r}")` — every receptor
becomes a singleton cluster. The cluster bootstrap silently degrades into a receptor
bootstrap, and the script still writes
`"authoritative_convention": "cluster_boot (per Block A C-8); receptor_boot secondary"`
(`:362`). A run without the clusters file is indistinguishable in its output from a run
with it.

**A convention conflict we should resolve before reusing any of this.**
`recompute_2x2_cluster_boot.py:3,201` and `g1_bootstrap_s1_auroc.py:362` both assert that
paralog-cluster bootstrap is the "**Block A C-8 authoritative convention**" and that
receptor-boot is secondary. Every other implementation — including
`stage3_post_audit_analysis.py`, whose `stage3_2x2_ligand_state_specificity.json` supplies
the interaction numbers quoted at `t2_bootstrap_sanity.py:66-71` — uses the receptor.
Grepping for "C-8" finds no document defining it.

### 8.6 One more binomial interval worth naming

`scripts/block_c_closeout/g4_scoped_centroid_census.py:350` computes
`wilson_ci(s["off_site"], n_measurable)` where `n_measurable` is a **prediction count**
(`:345`). Not a bootstrap — a binomial CI that treats correlated predictions from the
same receptor and the same seed as independent Bernoulli trials. This is the interval
behind the G4 off-site gate.

---

## 9. Is the seed-is-the-unit rule honoured? No — the code that implements it has never run

### 9.1 The rule, and where it lives

`scorer/switch_signal.py:8-12`, verified by direct read — it is a **module header
docstring**, prose only:

> 1. **Seed is the unit of variance.** For each (receptor, backbone, arm), collapse rows
>    to per-seed means FIRST, then compute means / bootstrap CIs over seeds. Never
>    subtract individual rows across arms (seeds are not matched between arms — row-wise
>    pairing would fabricate structure).

Restated at `:24-28` (the Δd_tm6 recipe: `CI = bootstrap over seeds (10,000 resamples,
2.5/97.5 pctile)`) and at `:173` ("Not row-level. Values here are per-seed means").

### 9.2 It is implemented correctly and it is dead code

Four pure functions implement it: `per_seed_mean:147-162` (the actual collapse),
`bootstrap_ci:169-186`, `delta_d_tm6_per_cell:193-245`,
`per_receptor_backbone_rollup:252-281`. The module is deliberately I/O-free (`:30`).

A repo-wide grep for `per_seed_mean|delta_d_tm6_per_cell|per_receptor_backbone_rollup`
returns **hits only inside `scorer/switch_signal.py` itself** — verified. The single
external importer, `scripts/step3_cross_validate_instruments.py:32-35`, imports
`MotifThresholds` and `prediction_is_active_like` — the row-level classifier — and
nothing else.

The wrapper its own docstring names, `scripts/analyse_switch_signal.py` (`:31-32`), is
not in the bundle.

`PREREG.md:520` records this module as landed "with 19 passing tests". **The seed-unit
machinery is present, tested, and unused.**

### 9.3 Verdict per analysis script

None of the thirteen collapses to per-seed means. No script uses pandas for this; all
group with `defaultdict` / `setdefault`.

| script | verdict | grouping | statistic |
|---|---|---|---|
| `analyse_switch_signal.py` | **absent from bundle** | — | — |
| `block_a_campaign_analysis.py` | ROW-WISE | `:172` `by_receptor[(rec,bb)][arm].append(d)` | `:180-182` median(cog) − median(apo); `n_cognate_valid = len(cog)` = 25 rows (`:187`) |
| `analyse_npxxy_primary.py` | ROW-WISE | `:241` `key = (bb, arm, slug)` | `:248-249` per-row counters; `:306` denominator = 50 rows |
| `gate_0_1_analyse.py` | ROW-WISE | `:212` `(corpus, backbone, arm)` | `:250-251` `fire_frac = pocket_yes_trans_no / n`, n = rows |
| `analyse_block_a.py` | ROW-WISE | `:97-103` `grouped[(rec,bb)].append(r)` | `:116-117` hitrate over rows; `:152-153` mean over rows |
| `block_b_headline_analysis.py` | ROW-WISE | `:125` pools receptors **and** seeds | `:175` `100 * n_active / n` with n = 8,000 rows; `:238` says so: "Using medians across all receptors and seeds" |
| `analyse_block_c_tier1_headline.py` | ROW-WISE | `:154` builds a seed level | `:158-166` then flattens it; fraction over 50 rows |
| `analyse_block_c_tier3_headline.py` | ROW-WISE | `:149` identical | `:153-161` identical |
| `analyse_block_b_ceiling.py` | ROW-WISE | `:134` `(slug, backbone, arm)` | `:16` states it: "Denominator = every landed prediction in the cell (50 = 5 seeds × 10 samples)" |
| `mn_confidence_analysis.py` | ROW-WISE (by design) | `:141` backbone only | seed/sample split is the independent variable here |
| `stage3_post_audit_analysis.py` | ROW-WISE, receptor-clustered | `:238-242` receptor is the cluster; **no seed level** | `:172-173`, `:287` pool rows |
| `held_out_threshold_validation.py` | N/A | crystal refs only | `:88` midpoint of means; `:152` accuracy over 8 held-out structures. `SEED = 20260901` (`:26`) is a split RNG |
| `step7_dispatch_gate.py` | N/A | — | `:1432-1436` groups **by** seed only to count distinct seeds per cell for manifest evenness (`:1449-1455`) — the opposite of collapsing |

### 9.4 The size of the effect

Seeds per cell is 5 everywhere; samples per seed varies:

- Block A — `build_block_a_manifest.py:164-169` `DEFAULT_MN = {"boltz": (5,5), ...}` →
  **5 seeds × 5 samples = 25 rows/cell**
- Block B — **5 × 10 = 50 rows/cell** (`block_b_headline_analysis.py:25,154`;
  `analyse_block_b_ceiling.py:16`)
- Block C Tier 1 — `build_block_c_tier1_manifest.py:106-108`,
  `CANONICAL_SEEDS = [554068910, 2095051020, 1854187058, 189590006, 1623169759]`, with a
  derivation-drift assert at `:119-121`
- Block C Tier 3 — `build_block_c_tier3_manifest.py:152-154`, different salt →
  `[524593679, 1607363019, 1779092953, 1393717870, 262604171]`

**So the pre-registered n per cell is 5 and every script reports 25 or 50.**
Denominators are inflated 5× (Block A) or 10× (Blocks B/C) relative to the pre-registered
unit, and any interval computed from them is correspondingly too narrow. Requirement on
the redo: the collapse is a *gate*, not a docstring.

### 9.5 Seed handling: 11 non-reproducible call sites

`PYTHONHASHSEED` is set nowhere in the bundle. These derive an RNG seed from Python's
`hash()` on strings or tuples, which is salted per process under PEP 456 — **these CIs
differ from run to run**:

- `stage3_post_audit_analysis.py:485` — `random.Random(hash((bb, arm_label, stratum)) & 0xffff)`
  (the training-cutoff stratum CIs)
- `task_a_v2_agonist_vs_decoy_apo.py:174,175`; `task_a_v3_composition_check.py:267`
- `g1_bootstrap_s1_auroc.py:329,332,335`; `g2_refsep_vs_auroc.py:194`;
  `g2_excl_agtr1.py:149,157`
- `side_quest_nsb_figures.py:162` (cosmetic jitter only)

Everything else uses fixed literals (`42`, `99`, `1234`, `7`, `20260904/05/06/07/10`).
`task_cohens_d_block_a_d_tm6.py:231` does it correctly —
`bb_seed = args.seed ^ (0x9e3779b1 * (BACKBONES.index(bb) + 1)) & 0xFFFFFFFF`.
`pr4_stratum_cis.py:90-92,146-148` reuses `SEED = 20260907` unchanged across all six
strata, so those six CIs share identical draws.

### 9.6 Percentile method

**Every interval in the bundle is a plain percentile bootstrap.** No BCa, no bias
correction, no acceleration, no normal approximation, no studentisation. Two idioms,
equivalent within one order statistic:

- sort-and-index: `lo = reps[max(0, int(n*0.025)-1)]`, `hi = reps[min(n-1, int(n*0.975))]`
  — `lib_common.py:120-121`, `stage3:187-188`, `task_f:55-56`, `recompute_2x2:150-151`
- `np.percentile(reps, [2.5, 97.5])` — `g1:218,257`, `pr4:59-60`, `t9:330`, `s8:57`

`n_boot` is 10,000 in the Block C headline scripts (`tier1:87`) and in
`switch_signal.bootstrap_ci` (`:169`), 5,000 in `stage3` (`:158`) / `lib_common` /
`task_f` / `recompute_2x2`, 500 in `g1` (`:54`, whose own docstring at `:24-25` says
300), 200 for permutation nulls.

---

## 10. Statistics that exist and we have never seen reported

Grouped by where they live. These are computed and printed or written to JSON; none of
them appears in anything we hold.

**Confidence calibration — bears directly on the paper's third title clause**
- `analyse_block_a.py:310-326` — per-backbone **high-confidence-wrong rate**, with
  `:326` stating that a nonzero rate means pLDDT is not a trustworthy filter.
- `mn_confidence_analysis.py:185-190` — per-cell median pLDDT, low-conf and high-conf
  fractions.
- `analyse_block_c_tier1_headline.py:380-386` — **P7, "pLDDT does not separate", is an
  unimplemented placeholder.** The confidence-calibration null was pre-registered and
  never computed. P6 likewise.

**The seed-vs-sample variance question, measured empirically**
- `mn_confidence_analysis.py:26-31,254-268` — `ratio_5 = std(1×5)/std(5×1)` and
  `ratio_20 = std(1×20)/std(20×1)`, with `classify_axis` (`:224-229`) returning
  `"samples"` / `"seeds"` / `"balanced"`. **This is a direct empirical test of the
  premise `switch_signal.py:8` asserts.** A `"samples"` verdict would contradict the
  pre-registration. `:340-345` emits a recommended sampling rule which can come out
  `seeds=1, samples_per_seed=5`. `:290-307` returns `UNSTABLE` when the winning axis
  flips between receptors.

**Threshold and scoring-rule sensitivity**
- `analyse_npxxy_primary.py:210-211,316-331` — a **six-variant threshold sensitivity
  sweep** (tilt-only / panel / per-receptor-40 / per-receptor-28 / composite /
  span-safe), printed as a full backbone × arm × variant grid. This is the "does the
  headline survive a different scoring rule" table.
- `analyse_npxxy_primary.py:251-261,307-312` — five pairwise disagreement counts per cell
  (`B_vs_C`, `B_vs_E`, `B_vs_F`, `C_vs_E`, `E_vs_F`): rows where two scoring variants
  give opposite calls.
- `gate_0_1_analyse.py:330-331,441-442` — the pocket × transmission 2×2 recomputed under
  a second threshold rule (panel median), with `:455-457` noting the fractions "tend to
  be substantially larger" under it.
- `held_out_threshold_validation.py:163-165,178` — train self-classification accuracy vs
  **held-out accuracy** under re-derived and full-panel thresholds, plus the threshold
  delta; `:184-193` per-receptor MISS lists.

**A second, independent structural axis**
- `scripts/rescore_rmsd.py:11-24` computes `rmsd_to_active_ref`, `rmsd_to_inactive_ref`
  and `rmsd_pos = rmsd_inactive / (rmsd_inactive + rmsd_active)` over the **common CA
  residue set of prediction + both references**. Its own header (`:6-8`) says "The
  delivered analysis reports Δd_tm6 ... and never computed structural RMSD to the
  reference PDBs, even though those CIFs are on disk. This script fills the gap."
- `block_a_campaign_analysis.py:254-310` — the whole normalised-position table,
  described at `:256-258` as the Phase-4 confirmation gate for the two-state result.
- `block_a_campaign_analysis.py:376-389` — **below-inactive / between / above-active**
  fractions, headline at `:319-321` as 56/27/17 pooled on cognate. "Above active" means
  predictions overshooting the active crystal.

**Physical-plausibility and failure counts**
- `block_a_campaign_analysis.py:410-479` — the A1 range check: 22 ACM1 × protenix ×
  cognate rows with `d_tm6 > 25 Å` and 19 rows with `NPxxY-OH > 25 Å`.
- `gate_0_1_analyse.py:412-423` — per-(corpus × backbone × arm) **NaN fraction for
  `pocket_ca_rmsd`**: a measurability table.
- `analyse_block_b_ceiling.py:171-185` — `CEILING_LOCKED_EXCLUDE_FROM_P1` (apo arm
  already active), `COGNATE_AT_UNITY_SENSITIVITY_LIMITED`,
  `COGNATE_NEAR_ZERO_P2_INVERTED`. Cells where the apo arm is *already* active are an
  untestability finding in their own right.

**Decoy- and ligand-arm results**
- `block_b_headline_analysis.py:214-234` — the pre-registered **decoy 2×2 split by
  engagement**, with `:218` "Only the engaged-and-inactive cell tests the α5-CT chemistry
  claim"; `:201-211` median contacts, median d(α5→3.50), fraction engaged per arm ×
  backbone; `:236-269` a four-cell decision table that auto-emits one of five verbatim
  verdicts including `:264` "sequence specificity real — steering paper unblocked".
- `analyse_block_c_tier1_headline.py:323-341` / `tier3:367-387` — **P5 null**:
  |decoy ligand − full agonist| on the apo arm. A direct decoy-arm null.
- `tier1:343-374` / `tier3:274-298` — **P0**: discriminator-vs-control effect size for
  (agonist − antagonist).
- `tier1:391-408` / `tier3:398-414` — the full fraction-active grid, 8×5×2×4 and
  40×3×2×4, every cell in the provenance JSON.

**Memorisation / training-cutoff tests**
- `stage3_post_audit_analysis.py:341-538` — every pocket contrast stratified pre/post
  each backbone's training cutoff, with `:522-529` verdicts `SURVIVES_POST_CUTOFF` /
  `PRE_CUTOFF_ONLY` / `UNDERPOWERED` / `NO_SIGNAL_IN_EITHER_STRATUM`.
- `stage3_post_audit_analysis.py:546-621` — effect size regressed on
  `log10(n deposited PDBs)` with Pearson r and a normal-approximation two-tailed p
  (`:606-614`), framed at `:554-555` as memorisation (positive r) vs physics (null).
- `stage3_post_audit_analysis.py:709-728` — sensitivity re-run excluding LPAR1 / 5HT1B /
  AA1R (flagged SMILES provenance), emitting `full_panel` and `flagged_excluded` side by
  side.
- `stage3_post_audit_analysis.py:261-283` — the **2×2 interaction term**
  (agonist−antagonist on active ref) − (agonist−antagonist on inactive ref) with
  bootstrap CI; `:424-429` the sidechain-RMSD variants of every pocket contrast.

**Cross-backbone structure**
- `analyse_block_a.py:294-308` — cross-backbone consensus histogram
  (unanimous / majority / split / minority / none); `:329-345` an AA2AR-specific
  breakdown testing the anecdote at population scale.

**And what is *not* computed.** Block A and Block B headline analyses report point
estimates and standard deviations with **no interval at all** — verified by keyword grep
over `analyse_block_a.py`, `block_a_campaign_analysis.py`, `block_b_headline_analysis.py`,
`analyse_npxxy_primary.py`, `gate_0_1_analyse.py`, `analyse_block_b_ceiling.py`,
`step3_cross_validate_instruments.py`, `compute_dip_test_per_cell.py`,
`diversity_analyse.py`: none contains a bootstrap, resample, percentile-CI or RNG.
Every interval in the corpus comes from the Block C post-audit and re-audit scripts.

---

## 11. Checked, and NOT a finding

Each of these looked like a defect on first pass and is not. Listed so the next reader
does not re-open them.

1. **"The apo guard in `ligand_rmsd_to_ref` never fires on Block C."** True but harmless.
   `pocket_metrics.py:786-787` returns NaN when `input_state_claim == "apo"`, and Block C
   sets `state_claim = "Ga-coupled-active"` on every row including apo-arm rows. But the
   very next guard, `:788-789`, returns NaN when `ligand_type in ("apo","none","")`, and
   `ligand_role = "none"` produces `ligand_type = ""`
   (`build_block_c_tier1_manifest.py:238-239`). The no-ligand case is covered.

2. **"Boltz will receive a `CCD:` string as a SMILES."** Latent, not realised. Both
   Block C manifest builders pass the `smiles` column, which always holds real SMILES;
   `ccd_code` and `ccd_smiles` are separate columns written to the manifest as metadata
   (`tier1:329-331`). No code path in the bundle feeds a `CCD:`-prefixed string to
   `_boltz_ligand_block`. It remains a trap for a future caller.

3. **"A peptide ligand inherits the receptor MSA."** Latent, not realised. The only
   caller that passes `msa_a3m_path` is `build_tier_d3_manifest.py:187-197`, and every
   call there is `_boltz_yaml_monomer(rseq, ...)` / OF3 / Protenix **monomer with no
   ligand** — the D3 MSA-depth tier is apo-only. The Block C builders pass no MSA path
   at all (grep for `msa` in both returns nothing). Real hazard, zero incidence here.

4. **"All eight Tier-1 decoys fail the property window, so the gate is broken."**
   The gate is not broken; it was never a gate. `_build_small_mol_report:1576-1589`
   records the axis results and only `charge` produces even a note. My ±20 % recomputation
   is against the **current** CSV; the window at build time (2026-09-03) was computed over
   a different ligand set, so I cannot claim these specific eight failed at the time. The
   claim I *can* make, and did (§2.2), is that the window has no rejecting power in the
   code as written, and that at least three Tier-3 picks are documented as taken despite
   missing it.

5. **"The decoy scramble seed and the ligand-decoy scramble seed collide."** They do not.
   Two different salts — `block_b_decoy_v1` for the α5-CT scramble
   (`build_shuffled_decoy_constructs.py:117`) and `block_c_decoy_lig_v1` /
   `block_c_tier3_decoy_lig_v1` for peptide ligand decoys
   (`build_block_c_decoys.py:294-308`). Different `MIN_HAMMING` too (5 vs
   `max(8, 0.65·len)`).

6. **"`verify_cognate_identity.py` would misidentify the partner when a peptide ligand is
   present."** It takes `prots[1]` / `chains[1]` — the second protein chain
   (`:59`, `:67`). A peptide ligand is appended *after* the partner
   (`propose.py:538-539`), so index 1 is always the partner in a two-chain arm. Safe as
   written; it would break on a monomer + peptide-ligand input, which it is never pointed
   at.

7. **"Tier-3 decoys were never gate-checked."** They were.
   `_build_small_mol_report:1569-1573` raises on Tanimoto ≥ 0.30 for every entry of
   `DECOY_SMILES`, Tier 1 and Tier 3 alike, and Tier 3 reports are emitted into
   `S3_decoy_construction_notes.md`. What is true is that the Tier-3 decoy SMILES reach
   the manifest as the **raw dict string**, not the canonical form (§1.1).

8. **`g1_bootstrap_s1_auroc.py`'s cluster bootstrap draws a variable number of receptors
   per replicate.** That is correct behaviour for a cluster bootstrap, not a bug.

---

## 12. Questions to put to `paper_af3`

Phrased as questions because the code cannot settle them.

**Ligands and decoys**

- **Q-L1 (highest value).** Block C Tier 1 and Tier 3 set
  `COGNATE_PARTNER_IDENTITY = "alphas"` for every receptor
  (`build_block_c_tier1_manifest.py:104`, `tier3:150`), so 35 of the 40 Block C
  receptors get a Gα they are not coupled to in the arm labelled `cognate`. Block A
  resolves this per receptor and calls the blanket form "the W54 taxonomy failure"
  (`build_block_a_manifest.py:50-51`), with a loud verifier
  (`verify_cognate_identity.py:10-12`). **Was the uniform Gαs deliberate for Block C —
  and if so, where is that decision recorded? Was `verify_cognate_identity.py` ever run
  against a Block C manifest?**
- **Q-L2.** The decoy selection is a hand-curated dict with a Tanimoto < 0.30 hard gate
  and a ±20 % property window that cannot reject. **Was a property-matched candidate pool
  (DUD-E / DeepCoy / property-matched ChEMBL draw) considered and rejected, or was the
  hand-pick the plan from the start?** The answer determines whether the redo can reuse
  these 34 decoys or must rebuild the set.
- **Q-L3.** Every aminergic decoy is neutral where the real ligands are cationic
  ("Decision A", `build_block_c_decoys.py:18-21`). **Is there a stratification anywhere
  that separates the charge effect from the identity effect?**
- **Q-L4.** `refs/ligand_set.csv` decoy notes reference `S-(-)-propranolol` for ADRB2,
  which was replaced by `(S)-alprenolol` on 2026-09-04. **Was
  `build_block_c_decoys.py` re-run after the Step 1.1 ligand substitutions?** If not, the
  Tanimoto gate as recorded was evaluated against a superseded panel.
- **Q-L5.** `pocket_metrics.py:48-54` requires the analysis layer to drop `decoy_lig`
  rows from `ligand_rmsd_to_ref`. **Which script does that, and on which column?** We
  hold no row-level file to check.
- **Q-L6.** `build_shuffled_decoy_constructs.py` defines the α5-CT as `seq[-11:]`
  (`:303`) with no CGN numbering. `redo/spec/DECISIONS.md` F-4 already requires us to
  define a CGN convention and send it. **Confirm the 11-residue positional definition is
  what every delivered Block B decoy construct used**, so we know what the redo is
  superseding.
- **Q-L7.** The shuffled arm is 33/40 Gαs, and the generated report calls it "balanced
  Gs↔Gi coverage" (`:544`). **Was the imbalance known?** It changes what a "non-cognate
  partner" result means.

**Analysis layer**

- **Q-A1 (highest value).** `analyse_block_c_tier1_headline.py` and its Tier-3 twin
  declare a two-stage bootstrap in their docstrings (`:32-34`) **and in the provenance
  JSON they emit** (`:601-604`, `"two_stage_cluster_resample_receptors_then_seeds"`),
  while `bootstrap_receptor_mean:181-205` has one stage over receptor scalars.
  **Which is right — is there a second implementation we do not have, or is the
  provenance field wrong?** Every Block C interval we might quote depends on the answer.
- **Q-A2.** `PREREG.md:223,521` say the bootstrap unit is the seed.
  `scorer/switch_signal.py` implements that and **has no callers**, and the wrapper its
  docstring names (`scripts/analyse_switch_signal.py:31-32`) is not in the bundle.
  **Does that wrapper exist? Was any published interval computed with seed as the unit?**
- **Q-A3.** `task_f_block_a_recheck.py:148-180` bootstraps the **Block A primary axis
  over rows**, builds `per_receptor_dtm6` (`:154`) and never reads it. **Is there a
  receptor-unit version of that CI?**
- **Q-A4.** `paralogy_clusters.csv` is referenced by the only two genuine cluster
  bootstraps and is absent from the bundle. **Please send it, with how the 26 clusters
  were defined** (family assignment? sequence identity at what threshold?).
  `g1_bootstrap_s1_auroc.py:185-186` degrades silently to singletons without it.
- **Q-A5.** `recompute_2x2_cluster_boot.py:3,201` and `g1_bootstrap_s1_auroc.py:362` name
  paralog-cluster bootstrap as "the Block A C-8 authoritative convention" while every
  other script uses the receptor. **What is C-8, and which convention stands behind the
  numbers in the frozen manuscript?**
- **Q-A6.** Eleven bootstrap call sites seed from Python's `hash()` with no
  `PYTHONHASHSEED` set (§9.5), including the training-cutoff stratum CIs at
  `stage3_post_audit_analysis.py:485`. **Were any of those numbers re-run to check
  stability?**
- **Q-A7.** `mn_confidence_analysis.py` measures whether the seed or the sample is the
  dominant variance axis (`:26-31`, `:254-268`) — the exact premise the pre-registration
  asserts. **What did it return?** If it returned `"samples"`, the seed-unit rule needs a
  new justification before the redo adopts it.
- **Q-A8.** P6 and P7 are placeholders in the Tier-1 headline
  (`analyse_block_c_tier1_headline.py:380-386`). **P7 is the confidence-calibration null,
  which is the paper's third title clause. Was it ever computed anywhere?**
- **Q-A9.** Please send the row-level files these scripts read —
  `rows.tier3.v2.csv` above all (already our highest-value ask),
  `experiments/018_.../analysis/rows.csv`, and the `experiments/020_...` tree, which is
  entirely absent. Without them nothing in Half Two can be recomputed rather than read.

---

## 13. Requirements this places on the redo

Stated tersely; each follows from a numbered section above.

1. **Define the negative control before running it.** If the redo keeps a decoy-ligand
   arm, the selection rule is written into `spec/` as a procedure with a rejecting gate —
   pool, matching axes, acceptance criterion — not a hand-picked dict verified after the
   fact (§2).
2. **Resolve the partner per receptor, always, and gate it.** A `verify_cognate_identity`
   equivalent runs over every manifest the redo dispatches, not just one block's (§6.1).
3. **The seed collapse is a gate, not a docstring.** Any statistic in the redo asserts
   its resampling unit in code — a check that fails when a denominator counts rows where
   the spec says seeds (§9.2, §9.4). Prove it by planting the defect.
4. **A resampling unit named in output must be the unit in the loop.** The provenance
   JSON is the most-trusted text in the pipeline; it is the last place a label may drift
   from the code (§8.3a).
5. **Grep the short text.** Three separate module headers in this bundle
   (`switch_signal.py`, `pocket_metrics.py`, `build_block_c_decoys.py`) assert a scope the
   code below withdrew. Every redo gate that changes scope must grep headers, titles and
   generated-report lines (§6.10).
6. **Recomputed provenance, never frozen strings.** Decoy Tanimoto values, `n parseable`
   counts and charge flags live in a regenerated artefact with a hash, not in a CSV
   `notes` cell (§2.4, §6.3).
