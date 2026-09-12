# GROUP2_LIGANDS.md — the ligand arm, enumerated

**Written 2026-09-12.** `g1_systems.csv` enumerates the partner axis in 2,039 rows and
carries `ligand = none` on every one of them. This document is the other half of that
crossing: what the ligand arm runs, on which receptors, with which molecules, and —
the part that needs stating rather than assuming — **how the decoy is deployed**.

Generator: `redo/build/g2_systems.py` → `redo/inputs/g2_systems.csv`.
Gate: `redo/gates/g2_preflight.py`, 11 blocking checks, each proved by planting the
defect it catches. Wired into `verify.sh`.

---

## 1. The design

**Ligand role × partner presence, crossed.** Four ligand levels and a partner axis:

| factor | levels |
|---|---|
| ligand | `none` · `full_agonist` · `antagonist` · `decoy_lig` |
| partner | `R0_apo` · `R3_ct21` (the title's rung) · `R7_full` (the whole cognate Gα) |

`agonist × antagonist × apo × cognate` is the 2×2 the paper's second title clause
needs. `none` makes it a crossing rather than two contrasts. `decoy_lig` is the third
level of the same factor — §3.

**`antagonist` is a LEVEL, not a molecule.** It resolves per receptor to a
`neutral_antagonist` (13 of the 16 curated T1 receptors) or, where the receptor has
no plain antagonist at all, to an `inverse_agonist` (ADRB1, B1B1U5, OPSD — the three
D-2026-09-12-f unblocked by relaxing amendment C-1). Every row carries **both**
`ligand` (the design level) and `ligand_role_actual` (the pharmacology), because D-f
requires that an inverse agonist is recorded as its own role and never relabelled,
and gate check **G-4** fails if they are conflated.

**The ligand-free cells are the same cells as `g1_systems.csv`'s.** They are
enumerated here so the design reads as a cube and the gate can check it is complete
(**G-9**), not so they are dispatched twice.

Partner MSA is **off** on every cognate row, apo rows carry `n/a` — the same
condition `g1_systems.py` runs, so a G1 row and a G2 row at the same rung differ in
the ligand and in nothing else (**G-11**, the analogue of g1's B7/B8).

---

## 2. The panel, and the three tiers that are never pooled

From `redo/inputs/ligand_tiers.tsv` on the frozen primary panel (30 receptors /
29 clusters), reproducing D-2026-09-12-f exactly:

| receptor set | receptors | clusters | members |
|---|---:|---:|---|
| **LIG_T1** — the headline | **16** | **15** | 5HT5A AA1R AA2AR ACM4 ADRB1 B1B1U5 CCKAR CNR2 DRD3 GHSR HRH3 LPAR1 LT4R1 OPRD OPSD S1PR1 |
| LIG_T1_BLOCKED | 1 | 1 | PD2R2 |
| LIG_T1_INV_EXTRA | 3 | 3 | AA2AR ACM4 DRD3 |
| LIG_T2 — reported apart | 2 | 2 | C5AR1 SSR2 |
| LIG_T3 — reported apart | 7 | 7 | AGTR1 CCR2 EDNRB MCHR1 NK1R NPY1R NTR1 |

T1 **eligible** is 17 receptors / 16 clusters; **curated** is 16 / 15 once PD2R2 is
refused. MDE at k=15 is **0.314**, and the T1+T2 (0.295) and all-tier (0.249) figures
reproduce from the same rule — so the tiers are worth exactly what D-f says and no
more. **T2 and T3 are never pooled into T1** (**G-2**): at 2 and 7 clusters neither
can carry the contrast, T2's ligands enter as separate polymer chains on both sides,
and in T3 one side is a chain and the other is not, so *within* a T3 receptor the
agonist/antagonist contrast is confounded with input modality.

**PD2R2 is carried as a row at zero predictions, not omitted.** A receptor that
vanishes from a table looks exactly like one nobody considered — which is the reason
`drule_targets.py` keeps B1B1U5 with an empty ChEMBL target. Unblocking it means an
agonist identity for `8XXV`, not a file.

---

## 3. The decoy — how the frozen campaign deployed it, and what changes

### 3.1 What it was

From `redo/protocol/MAP_LIGANDS_AND_ANALYSIS.md` §2: a decoy was a **hand-picked
FDA-approved drug, one hard-coded per receptor** in a Python dict (ADRB2→tramadol,
ADRB1→aspirin, HRH1→metformin, CCR5→imatinib, AA2AR→trimethoprim). The **only**
enforced gate was Morgan Tanimoto < 0.30. The ±20% property window over six axes was
computed, written to a report and **never acted on** — all eight Tier-1 decoys miss it
on 3–5 of 6 axes. Peptide decoys were composition-preserving scrambles of the native
agonist seeded by `SHA-256(slug|salt|variant)`. Tier 3's 32 decoys existed **only** as
that dict and were never RDKit-canonicalised.

### 3.2 How it was deployed — verified here, not taken on trust

Streaming parse of `analysis/block_c/received_2026_09_12/rows.tier3.v2.csv` (92 MB,
read-only), arm taken from the `input_path` segment after `pool/<receptor>/<role>/`:

| ligand_role | apo | cognate | total |
|---|---:|---:|---:|
| full_agonist | 7,400 | 7,400 | 14,800 |
| neutral_antagonist | 5,800 | 5,800 | 11,600 |
| decoy_lig | 7,200 | 7,200 | **14,400** |

40,800 rows, perfectly balanced. **So the decoy was a third level of the ligand-role
factor, crossed with both arms** — not a side experiment. That shape is right and is
kept.

*Recorded while checking: the 800 rows `FIRST_LOOK.md` excludes for an empty
`receptor_class` are **all `full_agonist`**, 400 per arm, and their `receptor_slug` is
empty too. FIRST_LOOK's agonist cells sum to 7,000 per arm against the file's 7,400,
so that exclusion is **not role-neutral**. It does not change FIRST_LOOK's qualitative
reading, and FIRST_LOOK already says its numbers are not results — but a 2×2 built by
dropping rows on a column missing in one cell only is a biased denominator, and
whoever recomputes should know before they start.*

### 3.3 What the redo does differently — deliberately, not by accident

1. **Identity comes from a pool, not a dict.** `DRULE_CHEMBL_SCOPE.md` pins a ChEMBL
   release by version and download checksum; `drule_pool.py` implements the rule and
   **refuses to run against the live web API**.
2. **The property window is enforced, not reported.** A window that is computed and
   ignored is the precise reason the frozen decoys test "does a dissimilar,
   unmatched molecule fail to activate" instead of the question.
3. **The decoy is a random effect.** `n` is split across `DECOY_DRAWS = 3` draws per
   receptor, exactly as `g1_systems.py` splits a scramble arm's `n` across its five
   permutations. One hand-picked molecule per receptor makes "decoy" and "that
   particular molecule" the same term — the D2 collision in another costume.
   *(The split truncates: n=10/50 over 3 draws realises 9/48, the same integer
   division `g1_systems.py`'s three-draw `face_scramble` lives with. The generator
   prints it rather than hiding it, because a decoy arm quietly running 9 where the
   agonist arm runs 10 is an unbalanced design nobody would see in the totals.)*
4. **Peptide decoys are a different control class.** The composition-preserving
   scramble is retained for chain ligands but recorded as `peptide_scramble` and
   never pooled with small-molecule decoys.
5. **Every decoy is RDKit-canonicalised and keyed by InChIKey**, never by CCD —
   F-11's rule, now a measurement (`RET` resolves to all-trans through the CCD while
   two of our rows mean 11-cis).

### 3.4 The pool is BUILT and the selection has RUN — 2026-09-12

> **SUPERSEDED. This section was titled "Until the pool exists" and described the arm as
> wholly blocked. That was true when written and false within the day.** The original
> text is kept below the current state, because a heading that asserts a state the system
> has left is this project's most frequent defect
> (see `[[scope-is-asserted-where-it-is-most-read]]`).

**Current state.** The pool is built (`inputs/drule_pool_molecules.tsv`, **ChEMBL_37**,
sha256 `33c20374…`, 120,973 molecules, scope `within_panel`) and `drule_select.py` has
run. Of 16 T1 receptors, **11 yield three D-RULE-accepted decoys and 5 do not**:

| | cells | pooled | per-cell |
|---|---:|---:|---:|
| **`READY` / `RESOLVED_DRULE_DECOY`** (11 receptors, 11 clusters) | **33** | **396** | **2,112** |
| `BLOCKED_DECOY_UNAVAILABLE` (5 receptors) | 15 | 180 *(blocked)* | 960 *(blocked)* |
| total | 48 | | |

Of the 33 `READY` cells, **22 are `G6d`** (`R0_apo` + `R3_ct21`, the non-optional arm) at
**264 pooled / 1,408 per-cell**, and **11 are `G6fd(option)`** at `R7_full`, **132 pooled
/ 704 per-cell**, still behind the `pi_choice` on the cognate rung. **Taking `R3_ct21`
only, the arm is 264 pooled, not 396.**

**The arm runs EXPLORATORY, below its own pre-registered bar.** §5.3 requires ≥12
clusters; 11 pass. `MDE = 1.218/√11 = 0.367` against 0.352 at k = 12 — a 4.4% loss.
Aditya's decision, recorded with the alternatives he declined, is `DECISIONS.md`
**D-2026-09-12-h**. Every decoy row carries
`EXPLORATORY_MISSED_PREREG_CLUSTER_BAR` in `ligand_flag`, so the arm cannot be read as
confirmatory by accident, and the 5 refused rows carry a second token separating
**`eligibility_unestablishable_no_chembl_target`** (B1B1U5 — categorically different, and
never flattened into the others) from **`fewer_than_k_accepted`** (AA1R, AA2AR, HRH3,
LPAR1).

**The three molecules travel in the cell**, pipe-delimited in `ligand_name` and
`ligand_inchikey`, because `n_shared_draws = 3` already means "the three decoys are the
three draws". SMILES stay in `drule_selected.tsv` and are joined on InChIKey rather than
copied — a second copy is what drifted in the frozen campaign
(`MAP_LIGANDS_AND_ANALYSIS.md` §2.4).

**And the 11 are a biased subset.** The five refused are the small and polar references
plus a dianionic lipid, so the survivors are the lipophilic, drug-like end of the panel.
The ligand-class contrast is evaluated on narrower chemical space than the agonist arm it
is compared against, and **k does not capture that**. D-2026-09-12-h item 5.

**Which checks now hold this.** `G-6` no longer asserts that every decoy cell is
unresolved — it and `G-12`/`G-13`/`G-14` **re-derive** the resolved and refused sets from
`drule_selected.tsv`, and `G-13` fails in **both** directions: a decoy appearing for a
refused receptor, and a passing receptor's arm going missing. `g2_systems.py` **fails**
if `drule_selected.tsv` is absent rather than reverting to blocked cells. 15 plants over
14 blocking checks, all proved.

<details><summary>The original §3.4, superseded 2026-09-12</summary>

> **The pool is not built and building it is Aditya's decision** — it needs a pinned
> ChEMBL release download. So the arm is **enumerated as rows whose ligand is
> `UNRESOLVED:drule_pool`**, `ligand_identity_status = UNRESOLVED_DECOY_POOL`,
> `dispatch_status = BLOCKED_UNRESOLVED_DECOY_POOL`, and whose predictions are counted
> in `blocked_predictions_*` so they can never reach a dispatchable total. **G-6** fails
> if a decoy cell acquires a molecule, a READY status or a non-zero prediction count —
> and it also fails if the decoy arm is **absent entirely**, because omitting a blocked
> experiment makes it look like one nobody thought of.

</details>

---

## 4. Where every ligand comes from

| source | cells | what it is |
|---|---:|---|
| `RESOLVED_NO_LIGAND` | 98 | the ligand-free level |
| `INHERITED_SMILES_PARSED` | 114 | `paper_af3`'s curation, SMILES re-parsed and InChIKey recomputed here |
| `RESOLVED_REDO` | 60 | our own enacted picks, `ligand_set_redo.tsv` |
| `RESOLVED_DRULE_DECOY` | 33 | §3.4 — 11 receptors × 3 partners, ChEMBL_37 |
| `BLOCKED_DECOY_UNAVAILABLE` | 15 | §3.4 — 5 receptors D-RULE refuses |
| ~~`UNRESOLVED_DECOY_POOL`~~ | ~~48~~ | **superseded 2026-09-12; the pool is built and selected** |
| `UNRESOLVED_UNCURATED` | 12 | named by the census, no bytes held (CCR2, NK1R, NTR1) |
| `INHERITED_CHAIN_SEQUENCE` | 8 | T3 peptide agonists, sequence in the received bundle |
| `UNRESOLVED_CHAIN_NO_SEQUENCE` | 8 | T2 — curated structurally, **no sequence anywhere** |
| `BLOCKED_LIGAND_IDENTITY` | 2 | PD2R2 |

**The nine inherited T1 receptors stay visible as inherited.** D-2026-09-12-f calls
them the largest remaining unverified surface in the ligand arm; a dispatch table that
does not say which rows they are hides exactly that.

### Three things the resolution found

- **T2 cannot dispatch.** C5AR1's BM213 and PMX53 and SSR2's CYN 154806 are curated
  *structurally* — the deposition is named — but the **polymer-chain sequence is
  nowhere in `redo/inputs/`**. SSR2's agonist carries a SMILES for somatostatin, and a
  SMILES is not a chain input; D-f's whole axis is chain-ness, so a chain row with no
  sequence is unresolved however much chemistry sits beside it.
- **AGTR1's inherited off-state row mislabels its own role.** `ligand_set_tier3.csv`
  keys CCD `OLM` @ 4ZUD as `neutral_antagonist`; GPCRdb types olmesartan **`Inverse
  agonist`**. That is the L-3 error class — carazolol — in somebody else's file. The
  molecule is real and its bytes are there, so it is taken under the **census's**
  role, only because the deposition matches the one the census picked, and the
  disagreement is flagged (`source_row_role_disagrees_with_gpcrdb`) rather than
  absorbed.
- **F-18's column shift is detected by shape, not by name.** A `ccd_code` containing a
  space or longer than five characters is malformed; that fires on LPAR1's
  `full_agonist` row and nothing else, and it would fire on the next one too.

---

## 5. The budget

| item | exp | cells | preds @n=10 | preds @n=50 | blocked @10 | blocked @50 |
|---|---|---:|---:|---:|---:|---:|
| P2b (pilot, boltz2) | E2.2 | 96 | 960 | 960 | — | — |
| **G6a/G6b** ligand × partner at `R3_ct21` | E2.2 | 96 | **3,840** | **19,200** | — | — |
| **G6d** decoy, third role *(EXPLORATORY)* | E2.4 | 32 | **264** | **1,408** | 120 | 640 |
| G6f *(option)* same crossing at `R7_full` | E2.2 | 48 | 1,920 | 9,600 | — | — |
| **G6fd** *(option)* decoy at `R7_full` *(EXPLORATORY)* | E2.4 | 16 | **132** | **704** | 60 | 320 |
| G21 *(proposed)* inverse-agonist level | E2.3 | 6 | 240 | 1,200 | — | — |
| G6-T2 peptide tier | E2.2 | 12 | 160 | 800 | 320 | 1,600 |
| G6-T3 mixed tier | E2.2 | 42 | 1,200 | 6,000 | 480 | 2,400 |
| G6x PD2R2, refused | E2.2 | 2 | — | — | — | — |
| **TOTAL** | | **350** | **8,716** | **39,872** | **980** | **4,960** |

> **The two decoy rows changed on 2026-09-12 and the totals moved with them.** They
> previously read `— | — | 384 | 2,048` and `— | — | 192 | 1,024`, i.e. the whole decoy
> arm blocked, with a campaign total of **8,320 / 37,760 and 1,376 / 7,072 blocked**. The
> pool was then built and `drule_select.py` run: **11 of 16 receptors yield decoys and 5
> do not**, so each decoy item splits into a dispatchable and a blocked part. Both decoy
> arms run **EXPLORATORY** — k = 11 against a pre-registered bar of 12, MDE 0.367 vs
> 0.352 (`DECISIONS.md` D-2026-09-12-h). **Every figure in this table is re-derived from
> `inputs/g2_systems.csv`, not carried forward**, because a budget row is a count and
> counts in this project have drifted from their own bodies four times.

---

## 6. Decisions reserved for Aditya, with their costs

1. **Which cognate rung the ligand crossing runs at.** `R3_ct21` is the length in the
   title. `R7_full` is what Block C's "cognate" arm supplied, so it is the **only**
   rung at which the 40,800 existing predictions are a comparator. The **apo half is
   shared**, so running both is additive, not double: `+1,920 / +9,600` on top of
   G6a/G6b, and it answers whether the ligand × partner interaction depends on partner
   length — which nothing in the corpus has asked. Rows for both are enumerated and
   marked `pi_choice`.
2. **Whether the antagonist level may be heterogeneous.** Taking it as enumerated,
   three of sixteen receptors contribute an inverse agonist. Restricting it to plain
   neutral antagonists costs **3 receptors and 3 clusters** — k drops 15 → 12 and the
   MDE rises 0.314 → 0.352, the same arithmetic F-15 records for k=12. D-f's C-1
   relaxation points at taking them; the alternative is on the table and costed.
3. **The ChEMBL release download** that unblocks the decoy pool (§3.4).
4. **Whether T2 and T3 run at all.** They can never be pooled into T1. T2 additionally
   needs four peptide sequences we do not hold.
5. **Raising `DECOY_DRAWS` above 3** once the pool report says how many accepted
   decoys a cluster actually yields.

## 7. Open, and not ours to close

- `RUN_MATRIX.md` §7.1 has **no line item for any Group 2 arm** beyond `G6a/b`, and it
  costs that one on **CORE-L17** — 17 clusters of a Block C-derived core, a different
  object from the frozen panel's T1 (16 receptors / 15 clusters) with the same number
  on it. `CAMPAIGN.md`:1273 already records three different "17"s. Reported by the
  gate as a WAIT, in the same class as the drift g1's **B18** found.
- `CATALOGUE.md` E2.1 (export the state call on Block C's existing predictions) is
  `free (them)` and is **not** a dispatchable system, so it is not in this file. It is
  the same ask as Block C's ask 1.
- **`README.md`'s counts have drifted.** It says `build/` holds **28** generators and
  `inputs/` **47** artefacts; on disk they are **40** and **60** besides
  `MANIFEST.tsv`, and both were already wrong before this file added two. Not edited
  here — it is not this session's file — but it is the same shape as `CAMPAIGN.md`'s
  "33 experiments in 9 groups" against a body of 45 in 10. A header count is a claim
  nobody checks.

---

## 8. Checked, and NOT a finding

Recorded because the near-misses are the useful part.

1. **"`ligand_set_redo.tsv` has 18 rows."** `wc -l` says 19 lines; it holds **17
   records**, because PD2R2's `why` field contains a real newline inside a quoted
   field. Counted with a CSV parser. My line count, not the file.
2. **"PD2R2 is curated."** My first pass keyed on row *presence* and counted PD2R2's
   `full_agonist` row. Its `status` is `BLOCKED`. Keying on `status == enacted` gives
   16 curated, which is what D-2026-09-12-f says.
3. **"HRH3 has no antagonist."** `ligand_set_redo.tsv` curates only its agonist; the
   antagonist is inherited (`ligand_set_tier3.csv`, 7F61, CCD `1IB`, SMILES present).
   T1 status stands.
4. **"CORE-L17 is the ligand panel."** It is not — see §7.
5. **"`g1_systems.py`'s CORE32 is 32 receptors."** It is **30**: `g1_panel_freeze.tsv`
   `core_frozen == yes` is 30, and that set is equal to `ligand_tiers.tsv`'s
   `panel_tier == PRIMARY`. Checked by set equality, and the generator refuses to run
   if the two ever disagree.
6. **"The decoy split loses predictions."** It truncates exactly as
   `g1_systems.py`'s three-draw `face_scramble` does. Same convention, now printed.
7. **"ADRB1 / B1B1U5 / OPSD have no off-state ligand."** They have an inverse agonist,
   which C-1 relaxation admits. Their `neutral_antagonist` rows in the inherited files
   are present but empty, which is why they look absent.
