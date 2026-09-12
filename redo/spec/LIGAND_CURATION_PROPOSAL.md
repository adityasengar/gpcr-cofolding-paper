# LIGAND_CURATION_PROPOSAL.md — the D-C picks, with reasons

**Decision D-C (2026-09-12): curate small-molecule agonist/antagonist pairs for the
seven receptors that have the modality but not the curation.** Baseline is 9
receptors / 8 clusters, MDE **0.431**; the target is 16 / 15, MDE **0.314**.

This proposes the specific picks. It does not enact them — `paper_af3`'s
`ligand_set.csv` schema wants `affinity_metric`, `affinity_value_nM` and
`affinity_source`, none of which are in our frozen snapshot, so **every row below
still needs an affinity attached from a source we pin.** Candidates and their
provenance are in `redo/inputs/ligand_curation_candidates.tsv` (59 rows), generated
by `redo/build/ligand_curation_candidates.py` from
`lit/panels/cache/gpcrdb_structures.json`.

## The selection rule, and why it is this one

**Prefer a ligand already bound to one of our own reference structures.** A ligand
co-crystallised with the structure we score against carries strictly better
provenance than an equally-resolved stranger: same construct, same conditions, same
deposition.

This is not cosmetic. Histamine appears on HRH3's `8YUU` and `8YN5` at the **same
2.7 Å**, and a resolution-only tiebreak kept `8YUU` and silently discarded `8YN5` —
**which is the panel's own active reference.** The rule was added after that, and
the generator now ranks on (is-our-reference, resolution).

**Species follows the panel, not the PDB.** `panel_systems.csv:species_modal`
describes which species is commonest among *deposited* structures and is **not**
what our panel uses — ADRB1 reads `Meleagris gallopavo` there while our ADRB1 is
`adrb1_human`, P08588, referenced to 7BU7 / 7BVQ. The authority is
`g1_receptors.tsv:organism`.

## The picks

| receptor | needs | proposed | CCD | structure | provenance |
|---|---|---|---|---|---|
| **S1PR1** | both | **siponimod** | `J8C` | `7TD4` 2.6 Å | **our ACTIVE reference** |
| | | **W146** | `ML5` | `3V2Y` 2.8 Å | **our INACTIVE reference** |
| **HRH3** | agonist | **histamine** | `HSM` | `8YN5` 2.7 Å | **our ACTIVE reference** |
| **ADRB1** | antagonist | **carazolol** | `CAU` | `7BVQ` 2.5 Å | **our INACTIVE reference** |
| **GHSR** | both | **ibutamoren** | `1KD` | `7NA8` 2.7 Å | same deposition as our active ref `7NA7` |
| | | **CHEMBL1956994** | `8QX` | `6KO5` 3.3 Å | **our INACTIVE reference** |
| **CCKAR** | agonist | **SR146131** | `IA1` | `7XOV` 3.0 Å | **off-reference — the only candidate** |

**Six of seven picks sit on, or in the same deposition as, a structure the panel
already uses.** That was not designed for; it is what the rule produced.

**CCKAR is the only genuinely new curation.** Its active reference `7MBX` carries
`CHEMBL216166`, which GPCRdb types **protein**, not small-molecule — consistent
with the existing curated row being the CCK-8 peptide. `SR146131` at `7XOV` is the
sole small-molecule agonist candidate on the panel's receptor, at 3.0 Å and from a
different deposition. It needs the most scrutiny of the seven.

## The two that are blocked, and why it is chemistry

**OPSD and B1B1U5 cannot be curated conventionally.** Both carry CCD `RET` for
**both** roles — agonist and antagonist are the same molecule in different isomers,
covalently bound through a Schiff base. `PANEL.md` §10 already records them among
four that Block C could not run, "and the reason is chemical, not operational."

**If they are dropped, k = 13 and MDE = 0.338** — still worth curating the other
five, which is the whole of D-C's value.

Two constraints if anyone attempts them anyway:

- **Curate retinal by ISOMER, never by CCD** (finding F-11). One code carries two
  opposite pharmacologies: 11-cis is the inverse agonist in 16 snapshot entries,
  all-trans the agonist in 14.
- **B1B1U5 is additionally blocked on D-H.** Its candidate agonist sits on `9EPP`
  and its antagonist on `6I9K`; D-H decides whether `9EPP` is the reference at all.
  **Resolve D-H before curating it.**

## What each row still needs

| field | status |
|---|---|
| `receptor`, `ligand_role`, `smiles`, `bound_pdb`, `ligand_ccd` | **have** — from the frozen snapshot |
| `is_peptide` | **have** — all seven picks are `type=small-molecule` |
| `affinity_metric`, `affinity_value_nM`, `affinity_source` | **MISSING — this is the remaining work** |
| `inchi`, `iupac_name` | derivable from SMILES with RDKit |

The affinity source must be pinned the way `DRULE_CHEMBL_SCOPE.md` pins the decoy
pool: one release, recorded activity types, stated assay-confidence floor. Using a
different provenance for the agonist/antagonist affinities than for the decoy pool
would make the two halves of the ligand arm incomparable.
