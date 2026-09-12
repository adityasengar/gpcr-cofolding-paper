# MAP_REFERENCES.md — reference selection and the state annotation in `paper_af3`

**Written 2026-09-11. Frame: REPRODUCTION, NOT AUDIT.** Nothing here is a charge. The
purpose is to state their reference-selection rule precisely enough that we could re-run
it, and to establish whether their calibration and our Group 0 calibration can be
compared at all.

## What this is built on

Root for every path below unless stated otherwise:

```
redo/protocol/received/source_bundle/
```

Read in full this session: `refs/PREREG.md` (544 lines), `scorer/refs_build.py` (731),
`scorer/references.py` (409), `scorer/switch_signal.py` (282), `refs/reference_set.csv`,
`refs/reference_pdbs.csv`, `refs/thresholds_panel.csv`, `refs/anchors_per_class.csv`,
`refs/uncovered_receptors.txt`, `refs/reference_set_named_exclusions.md`,
`refs/reference_provenance_grid.csv`, `refs/sealed_active_refs_2026_09_01.csv`,
`scripts/bootstrap_reference_pdbs.py`, `scripts/analyse_lit_metric_refs.py`,
`scripts/curate_phase3_derive_refs.py`, plus targeted reads of
`scorer/orchestrator.py`, `scorer/pocket_metrics.py`, `scorer/bw_numbering.py`,
`scripts/step3_cross_validate_instruments.py`, `scripts/verify_active_stabilization.py`,
and the five `refs/reference_pdbs_proposal_CURATE-*.md` documents.

**Version provenance.** `scorer/references.py` in the bundle is byte-identical to
`redo/protocol/received/references.d9c646af.py`
(`ee7dac0c…21bde`); it differs from `references.04243c45.py` only by the Block C
`role_specific` addition. **The A4 block is identical at both SHAs**, so every statement
in §4 holds at both commits. `scorer/pocket_metrics.py` in the bundle matches the sha
pinned in `refs/scorer_expected_shas.json` (`dabc097c…`) and is *later* than
`received/pocket_metrics.d9c646af.py`.

**Attribution rule.** No file is said to do anything that was not read here. Where a
claim rests on a file we do not hold, that is stated. Every apparent discrepancy was
treated as our own error first; §8 lists the ones that dissolved.

---

# 1. The procedure, stated so it can be re-run

Reference selection is **five stages, only two of which are code in the bundle.** This
is the single most important fact for reproduction: `refs_build.py` does not select
references. It *measures* a list that was already decided.

```
 stage 1   reference_panel_v2.csv          human/agent curation      NOT IN BUNDLE
              |  scripts/bootstrap_reference_pdbs.py
 stage 2   refs/reference_pdbs.csv         211 rows (52 excluded)      IN BUNDLE
              |  scorer/refs_build.py  build
 stage 3   refs/reference_set.csv          measured, 12 columns      IN BUNDLE
              |  derive_*_refs.py, curate_phase3_derive_refs.py, sidecar merges
 stage 4   refs/reference_set.csv          enriched, 35 columns      IN BUNDLE
              |  scripts/seal_active_refs.py
 stage 5   reference_set.csv  +  sealed_active_refs_2026_09_01.csv
```

## 1.1 How the **active** reference is chosen

There is **no algorithm.** The choice is made by a human-or-agent curator per receptor,
written into a CSV, and the code downstream never revisits it. The decision rule, as
practised, is recoverable from the five `CURATE-*` proposal documents, which record the
reasoning per PDB in a fixed template. Re-runnable statement:

1. **Enumerate** every deposited structure for the receptor, via GPCRdb
   `/services/structure/protein/<slug>/`, cross-checked against RCSB full-text search
   where GPCRdb is incomplete (`refs/reference_pdbs_proposal_CURATE-E.md:38`).
2. **Keep only those GPCRdb annotates `state=Active`.** Recorded per PDB on an
   "Activation evidence" line — e.g. `CURATE-A.md:50` "state=Active per GPCRdb";
   `CURATE-E.md:54` "GPCRdb `state=Active`".
3. **Require a transducer in the complex.** This is the operative filter and it is
   applied by rejection, not by a stated rule. From `CURATE-A.md:54-60`, on AA2AR:
   - `7EZC` rejected — "agonist UK-432,097 bound, 3.8 Å — but d=8.92 Å, TM6 essentially
     closed; **no Gα coupling → unsuitable as 'active'**";
   - `8UGW` rejected — "**no Gα in complex**";
   - `5WF5` rejected — "agonist-only … **without Gα the TM6 doesn't swing open in AA2AR**";
   - `3QAK`, `2YDO`, `4UHR` rejected — agonist-only, "TM6 not open".
4. **Check the identity anchors** 3.50 = R, 5.58 = Y, 7.53 = Y against GPCRdb
   `residues/extended`. A receptor whose *wild-type* violates them is refused at the
   receptor level (`CURATE-E.md:11`; five receptors refused on this ground alone).
5. **Prefer higher resolution among survivors**, as a tiebreak only — `6GDG` rejected for
   AA2AR at 4.11 Å in favour of `5G53` at 3.4 Å (`CURATE-A.md:54`); no floor is applied
   (see §2).
6. **Require the pair to discriminate**: `|d_active − d_inactive| ≥ 3.0 Å` on
   `d_r350_r630_ca`. Stated as the gate in `CURATE-A.md:23` and `CURATE-E.md:9`;
   `8IYX` is refused for GPR34 at `|Δd| = 2.96 Å` (`CURATE-E.md:23`, `:147`).
7. **Classify what stabilised it** into the controlled vocabulary
   `{native, mini_G, chimera, nanobody, agonist_only, DVL_DEP}` from RCSB polymer-entity
   text, never from the Gα UniProt accession (`refs/PREREG.md:249-253`;
   classifier at `scripts/verify_active_stabilization.py:306,552-565`). Where `chimera`,
   `alpha5_donor_class` names the parent whose α5 C-terminus is grafted.
8. **Write the row** into `refs/reference_pdbs.csv` with `role=active` and a
   `candidate_state` (§3).

## 1.2 How the **inactive** reference is chosen

Same procedure with `state=Inactive` and an antagonist- or inverse-agonist-bound,
transducer-free deposit. Two additions:

- The pharmacology of the bound ligand sets the sub-class:
  `Antagonist → inactive-antagonist`, `Inverse agonist → inactive-inverse-agonist`
  (`scripts/bootstrap_reference_pdbs.py:28-37`).
- From Block C (2026-09-04) a receptor may carry **several** inactive rows distinguished
  by `role_specific ∈ {"", inactive_neutral_antagonist, inactive_inverse_agonist}`
  (`scorer/references.py:63-73`). Seven receptors do; five are on the 48-receptor panel.

## 1.3 What `refs_build.py build` actually does

Per row of `refs/reference_pdbs.csv` that is not `excluded=true`
(`scorer/refs_build.py:139-145`):

| step | line |
|---|---|
| species / `uniprot_slug` consistency gate — raises `ValueError` | `refs_build.py:157-165` |
| read `construct`, `construct_offset` (renumbering shift) | `refs_build.py:175-183` |
| resolve BW anchors from GPCRdb `residues/extended` | `refs_build.py:190` |
| fetch coordinates (local cache first, else RCSB mmCIF) | `refs_build.py:193`, `75-99` |
| **heuristic** stabiliser detection from RCSB entry JSON, unioned with the manual column | `refs_build.py:199-203`, `47-72` |
| build UniProt-numbered model, `verify_reference_pdb`, `compute_all_axes` | `refs_build.py:220-229` |
| record `d_tm6_r350_r630_ca` as `d_r350_r630_ca_ref` | `refs_build.py:230` |
| write provenance JSON + sha256, then the CSV row | `refs_build.py:260-313` |
| **silent-NaN tripwire** — any curated row producing NaN raises unless `--allow-nan-tripwire` | `refs_build.py:361-393` |

`--dry-run` is a mandatory first pass (amendment S2, `refs_build.py:8`, `705-707`).

**It selects nothing.** There is no ranking, no filter, no admission test in `cmd_build`
other than the `excluded` column it is handed and the species gate.

## 1.4 The thresholds, and how to reproduce them exactly

`gpcr-refs thresholds` (`refs_build.py:402-560`) writes per-receptor distributions, but
the **applied** thresholds come from `scripts/analyse_lit_metric_refs.py`, and the rule
is one line:

```
threshold = (active_mean + inactive_mean) / 2.0
direction = "active_gt" if active_mean > inactive_mean else "active_lt"
```
`scripts/analyse_lit_metric_refs.py:119-122`; `sensitivity_lo/hi = threshold × 0.8 / 1.2`
(`:136`). The population is `refs/reference_set.csv` restricted to the receptor slugs in
`refs/gpcr_coupling.csv` (`analyse_lit_metric_refs.py:83-93`).

**We reproduced both applied thresholds exactly**, from
`refs/reference_set.pre_seal.csv` ∩ the 48 slugs of `refs/gpcr_coupling.csv`:

| metric | n active | active mean | n inactive | inactive mean | midpoint | shipped |
|---|---:|---:|---:|---:|---:|---:|
| `d_npxxy_oh_ref` | 36 | 5.285 | 34 | 12.878 | **9.0815** | 9.082 |
| `d_gpcrdb_tm6_tilt_ref` | 40 | 17.595 | 40 | 12.269 | **14.9318** | 14.932 |

Matching `refs/thresholds_panel.csv:2` and `:8` to every digit shipped. This settles
three things:

- **The derivation set is `reference_set.pre_seal.csv`, not `reference_set.csv`.** The
  current file gives 9.0807 and 14.93 on different n (30/39), because the §14 seal
  removed eight active rows afterwards. Anyone re-deriving from the shipped
  `reference_set.csv` will not reproduce the locked numbers.
- **Both thresholds are Class A only.** All 8 Class B/F panel members are NaN on both ref
  columns; the tilt "n=40" is 40 Class A receptors, one row each.
- **F-3 is confirmed independently of their lock file.** 9.0815 derived, 9.082 recorded,
  **9.08 applied** (`scorer/switch_signal.py:77`). Our 9.082 came from their panel and
  was right.

The four Class A receptors that drop out of NPxxY-OH on the active side are exactly
**EDNRA, EDNRB, GRPR, HRH3** — the four PREREG §2b names (`refs/PREREG.md:100`) — and six
more drop on the inactive side, giving the "70 of 80 tier-1 rows" of that same line.

---

# 2. Admission criteria, and where each is enforced

| criterion | stated where | enforced in code where | verdict |
|---|---|---|---|
| **Resolution floor** | nowhere as a number. Per-PDB resolutions are quoted in every `CURATE-*` entry and used as a tiebreak | **nowhere.** `grep -n resolution scorer/*.py` returns six hits, none crystallographic. In `scripts/verify_active_stabilization.py` resolution is a **sort key only** (`:611`, `:623`) | **NOT ENFORCED.** No floor exists in their pipeline. |
| **Deposited state (active/inactive)** | `refs/reference_pdbs.csv` column `role` | read verbatim at `refs_build.py:299`; copied to `resolved_state` at `:292`, `:303` | **CURATION, NOT CODE** — see §3 |
| **Experimental method (X-ray / cryo-EM)** | recorded in the `CURATE-*` prose | **nowhere** | **NOT ENFORCED** |
| **Stabilisation source** | `PREREG.md:249` controlled vocabulary, curated from PDB entry text | classified by `scripts/verify_active_stabilization.py:306`; written to `active_stabilization_source`. **Never gates anything** — see §4 | **ANNOTATION ONLY** |
| **Identity anchors 3.50 R / 5.58 Y / 7.53 Y** | `CURATE-E.md:11` | `scorer/verified.py::verify_reference_pdb`, called at `refs_build.py:228`; A1 raises only on the three identity anchors, per the Finding #7 comment at `refs_build.py:205-216` | **ENFORCED** |
| **Pair discriminator `\|Δd\| ≥ 3 Å`** | `CURATE-A.md:23`; `CURATE-E.md:9` | **nowhere at build time.** `refs_build.py:677-683` (the report text) explicitly *supersedes* it: "Refuse a reference pair only if the observed Δ is outside the panel's [P5, P95] range or flips sign" — and that rule is prose in a generated Markdown report, not code | **CURATION ONLY** |
| **Species match to the input construct** | A5 | `refs_build.py:157-165` at build; `scorer/references.py:285-306` at score time | **ENFORCED** (both ends) |
| **Per-axis coverage** | Finding #7 | `refs_build.py:243-254` — `d_r350_r630_ca_ref` NaNs cleanly when 3.50 or 6.30 is absent, rather than taking every axis down | **ENFORCED** |

**The short version: of the four criteria named in the brief, one (deposited state) is a
curated column, one (stabilisation source) is an annotation that gates nothing, and two
(resolution floor, method) do not exist in their code at all.** The gating that *is* in
code is about anchor identity and measurement integrity, not about admission.

---

# 3. The state annotation — where it actually enters

The claim to verify was: *"GPCRdb activation label as consumed by `refs_build.py`."*

## 3.1 Verdict: **half right, and the half that is wrong matters.**

**`refs_build.py` never reads a GPCRdb state field.** GPCRdb is contacted from exactly
three endpoints in the whole scorer (`scorer/bw_numbering.py:15-16`, `scorer/anchors.py:86`):

```
/services/protein/accession/<acc>/      identity
/services/residues/extended/<entry>/    BW generic numbering
```
plus EBI SIFTS for chain mapping. **`/services/structure/` — the endpoint that carries
`state` — is never called by any module under `scorer/`.** A repo-wide grep for
`gpcrdb.org` returns five hits in `scorer/`, all of them `residues/extended` or the
service root; every `gpcrdb.org/structure/<PDB>` URL in the tree is inside a
`CURATE-*.md` **prose** document.

## 3.2 So where does the label come from?

Three hops, and the GPCRdb label enters at hop 0 as a **human reading**:

| hop | what carries the state | file:line |
|---|---|---|
| 0 | curator reads GPCRdb's `state=Active/Inactive` per PDB and writes it into the proposal prose | `CURATE-A.md:50`, `CURATE-E.md:54` — "Activation evidence: state=Active per GPCRdb" |
| 1 | `reference_panel_v2.csv` carries `active_pdb` / `inactive_pdb` columns. **The role is the column the PDB sits in.** | `scripts/bootstrap_reference_pdbs.py:89-92`. *This file is not in the bundle* — path `/Users/SENGAAD1/Documents/claude/subsampling-cap-exp/inputs/reference_panel_v2.csv` (`:23`) |
| 2 | `candidate_state` is inferred **from the ligand's pharmacology**, not from any state label: `Agonist → Ga-coupled-active`, `Antagonist → inactive-antagonist`, `Inverse agonist → inactive-inverse-agonist`, `PAM → Ga-coupled-active`, `NAM → inactive-antagonist` | `scripts/bootstrap_reference_pdbs.py:28-37`, `69-73` |
| 3 | `refs_build.py` copies `candidate_state` verbatim into `resolved_state` | `refs_build.py:292`, `:303` |
| 4 | `resolved_state` is the *only* state the scorer ever sees | `scorer/references.py:158`, `:268` |

**Precise statement for our records:** their state annotation is a **two-source hybrid** —
GPCRdb's `state` decides which column of a hand-curated CSV a PDB lands in (hence the
`role`), and the bound ligand's pharmacology decides the finer `candidate_state`. Neither
is machine-read. Both are frozen into `refs/reference_pdbs.csv` before any code runs.

## 3.3 Consequence for reproduction

`reference_panel_v2.csv` is the root of the whole reference set and **we do not hold it**.
Everything downstream is reproducible from `refs/reference_pdbs.csv`, which we do hold
(211 rows). The un-reproducible part is *why any given PDB is in the active column*.
Question for them in §9.

---

# 4. A4 — confirmed disabled, and what it would exclude

## 4.1 Confirmed from code

`scorer/references.py:276-282`, in `check_reference_class`, verbatim:

```python
    # Stabiliser check deferred — see 2026-08-26 policy update above.
    # Historic block kept for reference:
    #
    # if input_state_claim == StateClaim.Ga_COUPLED_ACTIVE.value:
    #     bad = ref.stabilising_elements & DISQUALIFYING_STABILISERS
    #     if bad:
    #         raise A4ReferenceClassMismatch(...)
```

The list survives as data (`references.py:40-42`):
`{nanobody, scFv, BRIL, T4L, DARPin, minibinder}`. `refs_build.py:32` imports it and
**never uses it** — the import is the only reference to the symbol outside
`references.py`.

The rationale is stated in the module comment, `references.py:24-39`:

> "As of 2026-08-26 the check is DEFERRED — GPCRdb classifies Nb35 / Nb6B9 /
> scFv16-stabilised structures as state=Active because they capture the same TM6-out /
> open-Gα-pocket conformation as native Gα binding … The community-consensus position
> (per GPCRdb curation) is that these are valid active-state references."

**So the disabling is explicit, dated, reasoned, and identical at both commit SHAs.** It
is a deliberate policy, exactly as reported.

Note the justification's second clause — "The final active/inactive classification of a
prediction uses the full 6-axis vector … aggregated across many refs across many receptors
— any single-stabiliser artifact washes out" (`references.py:31-34`). That sentence has
been false since 2026-09-01: the predicate is one metric on one receptor's own references
(`switch_signal.py:84-87`). The comment is stale in the same way the module header is
(F-1); it is not a second policy.

## 4.2 What it would exclude if re-enabled

The check is an **exact-token** set intersection on `;`-split `stabilising_elements`, and
fires only for `input_state_claim == Ga-coupled-active` — i.e. only on active-role rows.
Computed over `refs/reference_set.csv` (script in §10):

**22 active references would be refused**, 19 on `scFv` and 3 on `nanobody`:

| token | n | receptors |
|---|---:|---|
| scFv | 19 | 5HT5A, ACM2, ACM3, ACM4, CCR6, CCR8, CML2, CXCR3, EDNRB, GPR34, GPR84, GRPR, HRH1, HRH4, NPY2R, NTR1, OXYR, TA2R |
| nanobody | 3 | ADRB2 (4LDE), CRFR1 (6P9X), GPR12 (7Y3G), GPER1 (8XOF) |

Plus **3 more from the sealed file** if unsealed: ADRB1 `7BU7` (`nanobody`),
CCKAR `7MBX` (`nanobody`), EDNRA `8HCQ` (`scFv`)
(`refs/sealed_active_refs_2026_09_01.csv`, rows 4, 5, 8). **Total 25.**

**Three would escape on a tokenisation accident**, though a stabiliser is named:

| receptor | pdb | `stabilising_elements` |
|---|---|---|
| AGTR1 | 6OS2 | `nanobody_beta_arrestin_biased_agonist` |
| FZD6 | 8JHB | `Nb35+XLas_Gs` |
| FZD7 | 8YY8 | `mini-Gs+Nb35` |

None of these three contains the bare token `nanobody`, so `frozenset & frozenset` misses
them. If we ever re-enable an equivalent check we must match on substrings or normalise
the vocabulary first.

**Impact on the threshold.** Of the 36 active rows that produced `active_mean = 5.285`,
three are nanobody-stabilised — ADRB1 `7BU7`, ADRB2 `4LDE`, AGTR1 `6OS2`. Re-enabling A4
would remove two of them (AGTR1 escapes) and move the NPxxY-OH threshold. We have not
recomputed the shifted value; it is a one-line change to the script in §10 if wanted.

---

# 5. Coverage — who has no reference, and what the fallback is

`refs/reference_set.csv` holds **168 rows over 107 receptors** — a superset of the
48-receptor panel of record (`refs/gpcr_coupling.csv`). On the panel: 52 active rows and
49 inactive rows over 48 receptors.

## 5.1 Receptors with no active row (17)

```
ACM1  ADA2A  ADRB1  CCKAR  DRD3  EDNRA  HRH3  OX2R     <- the §14 sealed 8, physically moved
5HT2A  ADA1A  DRD4  GPR6  HRH2  MTR1A  MTR1B  OPRM  SSR2  <- genuinely absent
```

The first eight are absent **by design**: `refs/PREREG.md:434-466` pre-registers the seal,
and `refs/sealed_active_refs_2026_09_01.csv` (header lines 1-8) records seed `20260903`,
timestamp `2026-09-01T14:33:41Z`, and `physical_move: True`.

**Verified against Block B**: `refs/reference_set.blockb_pinned.csv` contains **no active
row for any of the eight**. So Block B was scored with the seal in force — and since
PREREG §12 puts **ADRB1 and EDNRA** in the 12-receptor Block B panel (an overlap §12
calls "allowed by design"), **two of the twelve Block B receptors had no active reference
at scoring time**, which makes `receptor_midpoint`, `delta_to_active` and the entire
midpoint instrument NaN for them. Pre-registered, but load-bearing for anyone reading a
Block B midpoint number.

## 5.2 Receptors with no inactive row (42)

Mostly off-panel `GPR*` orphans and chemokine receptors. The `CURATE-E` finding explains
the pattern: the 2023-25 cryo-EM wave solved these receptors **only** in the Gα-coupled
active state (`CURATE-E.md:9`).

## 5.3 The fallback rules, in order of how much they matter

**(a) Missing reference → soft-fail, not an error.** `references.py:262-267`: if the
role-matched reference is `None`, `check_reference_class` returns without raising. Axis
values still flow; only the deltas, the midpoint and the state classification go NaN
(`references.py:240-256`, `compute_deltas` at `:400-408`).

**(b) `refs/uncovered_receptors.txt` is a dead carve-out.** The file exists and contains
**only comments — zero slugs**. It was designed as an explicit opt-in list
(`references.py:196-201`: "A receptor missing from `refs/reference_set.csv` but NOT in
this file will still fail A4 hard"), but the 2026-08-26 policy update made the soft-fail
universal, so the file is never consulted for a decision. `references.py:266` keeps the
kwarg "for API stability" and discards it.

**(c) Multiple inactive rows → last-write-wins.** `references.py:115` overwrites
`_by_receptor[slug]["inactive"]` per row, so `lookup.inactive` — which feeds
`compute_deltas` and therefore every midpoint — is **whichever inactive row appears last
in the CSV**. Seven receptors have more than one; five are on the panel:

| receptor | inactive rows in file order | `lookup.inactive` |
|---|---|---|
| AA2AR | 5MZP *(neutral_ant)*, 5NM4 *(inverse_ag)* | **5NM4** |
| ADRB2 | 2RH1 *(inverse_ag)*, 3NYA *(neutral_ant)*, 6PS2 *(generic)* | **6PS2** |
| CCR5 | 4MBS *(neutral_ant)*, 5UIW *(generic)* | **5UIW** |
| CNR1 | 5TGZ *(neutral_ant)*, 5U09 *(generic)* | **5U09** |
| SMO | 4JKV, 8CXO | **8CXO** |
| ADA1A *(off-panel)* | 7YMJ *(neutral_ant)*, 8HN1 | **8HN1** |
| GPR6 *(off-panel)* | 8TF5, 8T1V | **8T1V** |

They know: `references.py:107-112` says "the legacy `_by_receptor` overwrites on
role='inactive' and last-write-wins is **arbitrary**". We checked whether the Block C
sidecar merge silently changed any panel midpoint by inserting rows: it did not — the six
sidecar rows added since the Block B pin were all inserted *before* the generic row, so
the winner is unchanged in every case. **That is file order, not a rule.** A re-sort of
the CSV would change five panel midpoints without touching a single value.

**(d) Pocket metrics use a separate, ligand-aware ladder.**
`scorer/pocket_metrics.py:928-990` (`_role_for_state_claim`) → `:1152-1176`:
`full_agonist / none / decoy / empty → active`; `neutral_antagonist → inactive` with
`role_specific=inactive_neutral_antagonist`, falling back to the generic inactive and
noting `ref_role_specific_fallback_to_generic_inactive`; **apo / design →
`ref_active if ref_active is not None else ref_inactive`** (`:1173-1175`). With no
reference at all it emits `no_reference_available` and still returns `w648_chi1`
(`:1180-1189`).

**(e) The fallback PREREG promises for non-Tyr receptors is NOT implemented.**
`refs/PREREG.md:100` and `switch_signal.py:100-104` both say a NaN NPxxY-OH "drops with
`metric_coverage_insufficient`" and "**falls back to midpoint-crossing on
`d_tm6_r350_r630_ca` as the sole active-call**". In code:
`prediction_is_active_like` returns the literal string `"insufficient"`
(`switch_signal.py:130-131`) and **there is no fallback branch anywhere**. The string
`metric_coverage_insufficient` does not occur in any `.py` file in the bundle.
`scripts/step3_cross_validate_instruments.py` does define `midpoint_active_like` (`:147`)
and `gpcrdb_tilt_active_like` (`:171`), but it runs them **in parallel** to build an
agreement matrix, never as a fallback chain. So for EDNRA, EDNRB, GRPR and HRH3 the
motif instrument yields `insufficient` and nothing catches it.

**(f) Named "NaN by design" exclusions** are enumerated in
`refs/reference_set_named_exclusions.md` — 5HT1B (no clean neutral antagonist exists),
GLP1R (only inactive crystal is a NAM outside the orthosteric pocket), and DRD3 / ACM4 /
OX2R / AA1R (no inverse-agonist crystal exists). These are documented absences, not gaps.

---

# 6. PREREG §2a versus `switch_signal.py`

**Question asked: was PREREG amended to match the collapse, or does it still describe the
pre-collapse design? Answer: it was never amended. §2a still specifies ≥3-of-5, and the
document carries four mutually inconsistent statements of the predicate.**

`refs/PREREG.md` was extended by **appending** sections, never by editing §2a. The result:

| # | location | predicate as written | matches code? |
|---|---|---|---|
| 1 | `PREREG.md:79` (**§2a, the locked combination rule**) | "A prediction is called **active-like** iff **≥ 3 of the 5 metrics** cross their pre-registered threshold … AND `confidence_flag != "low"`" | **NO** |
| 2 | `PREREG.md:100` (§2b, "Motif composite (final)") | "single-metric NPxxY-OH. K_OF_N = 1, MAX_MISSING = 0" | **YES** |
| 3 | `PREREG.md:118` (§2b, "DRY caveat (locked)") | "Under `MAX_MISSING = 1` in the k-of-n rule … the k-of-**2** quorum … can still be called active-like on NPxxY OH + Y5.58 pack alone" | **NO** — a two-metric era |
| 4 | `PREREG.md:140` (§2c, "Two-instrument summary") | "Class A success rides on motif metrics (biology-derived, **3-metric composite**)" | **NO** |
| 5 | `PREREG.md:480` (Open TODOs, checked off) | "Composite is now **k-of-2 over 3 metrics**: DRY (11.54 Å), NPxxY OH (9.08 Å), Y5.58 pack (4.37 Å). Codified in `scorer/switch_signal.py::MotifThresholds`" | **NO** |
| 6 | `PREREG.md:523` (Consolidated findings, Step 4) | "**k-of-n (≥3 of 5)** motif rule with NaN-as-fail semantics" | **NO** |

Against the code, `scorer/switch_signal.py:84-104`:

```python
    METRIC_SPECS = (
        ("d_npxxy_y558_y753_oh", NPXXY_OH_OH_ACTIVE_LT, "active_lt", "NPxxY OH-OH"),
    )
    K_OF_N = 1
    MAX_MISSING = 0
```

**Only entries 2 and §2c-revised (`PREREG.md:148-190`) describe what runs.** Everything
else in the document — including the section that carries the word "locked" and the
sign-off checklist — describes a predicate that never scored a row.

### The same failure repeats inside the module

`switch_signal.py` carries **three** stale layers above the correct one:

| layer | line | says |
|---|---:|---|
| module header docstring | `:14-22` | "≥3 of the 5 motif metrics"; "≥2 NaN metrics ⇒ drop" |
| threshold-table banner | `:43-47` | "**Placeholder values; DO NOT USE for Block A** until user reviews and locks them" |
| `prediction_is_active_like` docstring | `:114` | "Applies PREREG **§2a k-of-n** rule" — pointing at the stale section |
| **class docstring** | `:55-73` | **correct** — records the collapse and its evidence |

This is `[[scope-is-asserted-where-it-is-most-read]]` three times in one 282-line file,
and once more across a 544-line pre-registration. It is not one stale docstring.

### One live hazard worth carrying into the redo

`scripts/step3_cross_validate_instruments.py:126-140` (`install_panel_thresholds`)
**mutates the class attributes at runtime**:

```python
        MotifThresholds.METRIC_SPECS = tuple(active_metrics)
        MotifThresholds.K_OF_N = min(3, len(active_metrics))
```

Today `min(3, 1) = 1`, so it is a no-op. **The moment a second metric is re-added — which
the `K_OF_N` comment invites as "a config change, not a code change"
(`switch_signal.py:96-98`) — this line silently re-inflates K toward 3.** If we adopt
their module we must delete this.

### F-1, F-2, F-3 as re-checked here

- **F-1 confirmed and extended.** The predicate is single-metric. What DECISIONS.md
  attributes to the module header alone is also in PREREG §2a, §2b's DRY caveat, §2c's
  summary, the TODO checklist and the Step 4 findings. **PREREG itself still describes
  the pre-collapse design in its most-read section.**
- **F-2 confirmed in code.** `switch_signal.py:116-117` returns `"inactive"` before any
  geometry is read when `confidence_flag == "low"`; `confidence_flag` is set purely from
  `min_plddt_at_anchor` at `scorer/orchestrator.py:613-622` (<50 low, 50-70 borderline,
  ≥70 high). Note `orchestrator.py:604-607` states the *intended* behaviour — "flags the
  row so state classification returns the `insufficient_confidence` bucket rather than
  `active`/`inactive`" — and `scorer/schema.py:222` repeats it. **The classifier does not
  do that**; it returns `inactive`, which is a pole, not a bucket. The early return is a
  deliberate choice ("conservative", `:117`) that contradicts its own design note.
- **F-3 confirmed independently.** See §1.4. 9.0815 derived / 9.082 recorded / 9.08 applied.

---

# 7. Can our Group 0 and their calibration be compared? — the answer this section exists for

## 7.1 Plainly

**They can be compared. They cannot be used to validate each other, because both anchor
the active pole on the same thing our own thesis treats as the independent variable —
whether a transducer is present.**

A joint calibration is **not** circular in the sense of double-counting the same rows:
the populations are disjoint by construction (our §2.1 rule excludes every panel
ortholog, and their reference set *is* the panel). It is circular in the sense that
matters: **neither set contains a meaningful number of transducer-free active-state
structures, so neither can tell us what "active" looks like without a partner.**

## 7.2 The evidence, on their side

`spec/GROUP0_SYSTEMS.md:475-513` retracted Q0c after establishing that GPCRdb's
"activation degree = 100" means "a transducer is bound" — 795 of 807 degree-100 Class A
actives carry one. `paper_af3`'s active pole has the same property, arrived at by a
different route, and **more strongly**, because theirs is enforced per structure by hand:

**Of the 36 active references that produced `active_mean = 5.285 Å` — the number that
*is* the 9.08 threshold:**

| `active_stabilization_source` | n | share |
|---|---:|---:|
| `native` (Gα heterotrimer) | 22 | 61% |
| `mini_G` | 7 | 19% |
| `chimera` (Gα scaffold + grafted α5) | 2 | 6% |
| **subtotal: a Gα-derived transducer is present** | **31** | **86%** |
| `nanobody` | 3 | 8% |
| `agonist_only` — **no partner of any kind** | **2** | **6%** |

The two transducer-free actives are **CNR1 `5XRA`** and **OPRD `6PT2`**. Both are:

- demoted to "reported-secondary" in `PREREG.md:43` — "CNR1 + OPRD reported-secondary
  (agonist-only active refs, **swap to 6N4B / 6PT3 post-Block-A**)";
- and OPRD's was in fact replaced: `scripts/curate_phase3_derive_refs.py:19` —
  "OPRD 8F7S … **REPLACEMENT for 6PT2 agonist-only** — 3.0 Å 2022 **Gi-bound** cryo-EM".

So the only two structures in their active pole that could have spoken to the
agonist-alone question were flagged as defects and scheduled for removal *because* they
lacked a Gα. And the rejection log in §1.1 shows the same rule applied prospectively —
`7EZC`, `8UGW`, `5WF5`, `3QAK`, `2YDO`, `4UHR` all rejected as active candidates for
having no transducer.

## 7.3 What this means for each axis

Our `GROUP0_SYSTEMS.md:514-533` carries the entanglement as a 2×2. The same 2×2 applies
to their set, with one cell worse:

| axis | vs their **active** pole | vs their **inactive** pole |
|---|---|---|
| **tilt** `d(2×46, 6×37)` | circular — 94% partner-bound | **circular — this is GPCRdb's own inactive-pole definition, same atom pair** (`GROUP0_SYSTEMS.md:514-521`) |
| **NPxxY** `d(Y5.58,Y7.53)` | circular — 94% partner-bound | **clean** — different helices, different atoms, and their inactive pole is antagonist-bound and transducer-free |

**Exactly one of four cells is clean on their side too, and it is the same cell.** That is
the strongest comparability statement available: our two calibrations are entangled in the
*same place, on the same axis, for the same reason*, so a disagreement between them is
informative and an agreement is not.

## 7.4 What is genuinely comparable

| | `paper_af3` | our Group 0 |
|---|---|---|
| population | 40 Class A panel receptors, 1 active + 1 inactive each, 70 usable rows on the OH axis | 433 off-panel Class A structures, 372 / 61, 106 receptors, 17 paired (`GROUP0_SYSTEMS.md:26-28`) |
| overlap with ours | **zero by construction** — our §2.1 excludes every panel ortholog | — |
| active anchor | transducer present, curated per structure, rule unstated | ternary complexes, declared as an anchor choice (`GROUP0_SYSTEMS.md:558-562`) |
| inactive anchor | antagonist/inverse-agonist-bound, transducer-free | same |
| resolution rule | **none** | ≤ 3.5 Å with a declared 2.5/3.0/3.2/3.5/4.0/none sweep (Q1) |
| method balance | not examined | examined and reported as a confound, p = 0.0095 (`GROUP0_SYSTEMS.md:264-289`) |
| NPxxY-definedness | discovered as a per-receptor drop-out (10 of 40) | **pre-filter Q0b**, measured on all 199 Class A entries (`GROUP0_SYSTEMS.md:96-137`) |
| fit | midpoint of two class means, `(a+i)/2` | unsupervised mixture with bootstrap, mixing weights reported (`GROUP0_SYSTEMS.md:35`) |
| class balance | 36 : 34 ≈ 1:1 **by construction** (one pair per receptor) | 6.1 : 1, and the reweighting is open decision D4 |

**The comparison to run.** Their threshold is the midpoint of a 1:1 paired panel; ours is
a fit to a 6:1 unpaired population. Those are not the same estimator and will not agree
by default. The clean cross-check is to **re-derive their estimator on our calibration
population and ours on their 70 rows**, and report both — not to adopt 9.08 and not to
replace it silently.

**The one thing that would make a joint calibration genuinely circular**, and it is worth
stating so nobody does it by accident: **pooling their 70 panel rows into our calibration
set.** Their rows are the *application* population — `GROUP0_SYSTEMS.md:241-251` splits
610 on-panel structures out precisely so they are never calibrated on. Their reference
PDBs are a subset of those 610. Fitting a threshold on a set that includes them and then
scoring panel predictions with it is the failure our §2.1 rule exists to prevent.

## 7.5 Two properties of their set we should copy, and two we should not

Copy: the **paired design** (one active and one inactive per receptor, so the receptor is
its own control — we have this on only 17 receptors and it is our scarcest resource); and
the **`active_stabilization_source` vocabulary**, which is the cleanest per-structure
record of partner presence anyone in this project has built, and is exactly the column
D3 needs.

Do not copy: the **absent resolution rule** (our §2.3 shows the floor is also a
balance rule, so "no floor" is a silent choice, not a neutral one); and the **midpoint
estimator**, which assumes a 1:1 prior that their construction manufactures and our
population does not have.

---

# 8. Checked and NOT a finding

Five things that looked wrong and were our error, recorded so nobody re-derives them.

**8.1 `refs_build.py:32` imports `DISQUALIFYING_STABILISERS` and never uses it.** Looked
like the A4 gate had been ripped out of the build path. It had not — the symbol is only
ever a gate inside `references.py`, where it is commented out with a dated rationale
(§4.1). The import is cosmetic dead weight, not evidence of a second disabled check.

**8.2 `refs/reference_set.csv` has 35 columns; `refs_build.py` writes 12.** Looked like
the shipped file could not have come from the shipped builder. Correct, and it is not a
defect: the file is a **five-stage artefact** (§1). `cmd_build` writes columns 1-12
(`refs_build.py:325-330`); `derive_npxxy_refs.py` / `derive_motif_refs.py` /
`derive_lit_metric_refs.py` add the `*_ref` measurement columns; `seal_active_refs.py`
and the construct audit add `active_stabilization_source` / `alpha5_donor_class` /
`curation_note`; the ICL3 audit adds five more (`PREREG.md:209`); the Block C sidecar
merge adds `role_specific`. **Consequence for us: re-running `gpcr-refs build` alone does
not regenerate the shipped file**, and the derivation scripts must be run in order.

**8.3 `resolved_state` carries four values that are not in `StateClaim`.** `ADA1A`/`CNR1`/
`ADRB2`/`AA2AR`/`CCR5` inactive rows carry `inactive-neutral-antagonist`; GCGR carries
`inactive-full-length`; FZD4 `DVL-coupled-active`; FZD6 `inactive-apo`. Against
`scorer/schema.py:42-48` those are unknown strings, and `references.py:268` compares
`resolved_state != input_state_claim` **by exact string**, so they looked like guaranteed
A4 raises. They are not, for three compounding reasons: (a) A4 only fires when a
reference *is* present for the role the claim maps to (`references.py:258-267`); (b)
`_role_for_state` returns `None` — no gate at all — for `apo`, `design_no_dry` and
`class_bc_native_no_dry` (`references.py:309-321`), and `orchestrator.py:653` skips the
call entirely for those; (c) in every panel case the last-write-wins winner is the
*generic* row, whose `resolved_state` is canonical. The single residual case is AA2AR,
whose winner `5NM4` is `inactive-inverse-agonist` — which would raise against an
`inactive-antagonist` claim. **Latent, not live**: the only manifest we hold
(`received/tier_d1_full_manifest.csv`) is `state_claim=apo` on all 140 rows, and Block C
dispatches `Ga-coupled-active` on every row by design (`pocket_metrics.py:941-944`). We
cannot see Block A/B manifests, so this stays a question (§9).

**8.4 The `|Δd| ≥ 3 Å` discriminator looked like a build-time gate.** It is quoted as a
rule in the `CURATE-*` documents (`CURATE-A.md:23`, `CURATE-E.md:9`). It is not in `cmd_build`,
and the generated threshold report at `refs_build.py:677-683` **explicitly supersedes it**
with a [P5, P95] / sign-flip rule — which is itself prose in a Markdown file, not code.
Neither version gates anything at runtime. This is curation discipline, not enforcement,
and calling it a gate would have been our mistake.

**8.5 Six rows differ between `reference_set.csv` and `reference_set.blockb_pinned.csv`,
which looked like the Block B references had drifted.** The six are exactly the Block C
`role_specific` sidecar inactives (AA2AR 5MZP, ADA1A 7YMJ, ADRB2 2RH1 + 3NYA, CCR5 4MBS,
CNR1 5TGZ); `set(pinned) - set(current)` is **empty**. And
`refs/reference_set.blockb_pinned.csv` is **byte-identical** to
`data/block_b/09_references/reference_set.blockb_pinned.csv`
(`6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`) — the file Group 0
already pins as a frozen input (`GROUP0_SYSTEMS.md:84`). **Their Block B reference set
and our pinned copy are the same object.** That is the strongest reproduction anchor in
this document.

---

# 9. What the code cannot answer — questions to ask them

Phrased as they should be sent.

**Q-R1 (blocking for reproduction).** `scripts/bootstrap_reference_pdbs.py:23` reads
`/Users/SENGAAD1/.../inputs/reference_panel_v2.csv`, which is the root of the entire
reference set — it decides which PDB is the active one for every receptor. It is not in
the bundle. **Can you send it?** Without it we can reproduce every measurement but not a
single selection.

**Q-R2 (the one that decides comparability).** For the active pole, was "a transducer is
present" a **stated admission rule**, or an emergent consequence of preferring the
best-resolved TM6-open structure? We ask because the `CURATE-*` rejection logs read as a
rule (`7EZC`, `5WF5`, `8UGW`, `3QAK` all rejected for "no Gα"), but no document states it
as one. **Our Group 0 needs to record whether your active anchor is partner-presence by
design or by accident**, because we are writing the same limitation into our Methods
either way and want to attribute it correctly.

**Q-R3.** Were CNR1 `5XRA` and OPRD `6PT2` — the only two transducer-free actives in the
36-row NPxxY-OH derivation set — still in the set when 9.08 was locked on 2026-09-01, and
was the threshold re-derived after `curate_phase3_derive_refs.py` swapped OPRD to the
Gi-bound `8F7S`? If yes, what is the post-swap value?

**Q-R4.** Was a resolution floor ever applied at curation time? We find none in code and
none stated as a number, but `6GDG` was rejected at 4.11 Å. If there was a working cut we
would like to state it; if there was not, we would like to say that too rather than guess.

**Q-R5.** `refs/uncovered_receptors.txt` ships with zero slugs. Was it ever populated, or
did the 2026-08-26 soft-fail policy retire it before it was used? (We are asking because
`references.py:196-201` still describes it as load-bearing.)

**Q-R6.** `refs/PREREG.md` §2a still specifies the ≥3-of-5 rule, and four other passages
describe k-of-2-over-3 or a 3-metric composite. We read §2b's "Motif composite (final)"
and §2c-revised as the operative text and everything else as pre-collapse residue —
**is that right?** We ask because §2a is the section headed "locked, no post hoc tuning"
and the TODO checklist at line 480 signs off on the k-of-2 version.

**Q-R7.** Which `state_claim` values actually appear in the Block A, B and C manifests?
The only manifest we hold is all-`apo`. We need this to know whether the A4 reference-class
check ever fired at all — and specifically whether any AA2AR row was dispatched with
`inactive-antagonist`, which would hit the `5NM4` mismatch in §8.3.

**Q-R8.** `switch_signal.py:100-104` and `PREREG.md:100` both promise that receptors with
non-Tyr at 5.58/7.53 "fall back to midpoint-crossing on `d_tm6_r350_r630_ca`". We find no
such fallback in the bundle. **For EDNRA, EDNRB, GRPR and HRH3, what was the active call
made from?** If the answer is "they were reported as `insufficient`", we would like to
know how many rows that was.

**Q-R9.** `references.py:107-112` acknowledges that `lookup.inactive` is last-write-wins
over multiple inactive rows. Is the row order in `reference_set.csv` deliberate — i.e.
is "generic inactive last" an invariant something maintains — or did it happen to come
out that way? If we re-sort the file we change five panel midpoints.

---

# 10. Reproduction appendix

Every number computed here comes from one of these, run from the bundle root
`redo/protocol/received/source_bundle/`. They are read-only and touch nothing.

**Threshold reproduction (§1.4)** — reproduces 9.0815 and 14.9318:

```python
import csv, statistics
pset = {r['receptor_slug'] for r in csv.DictReader(open('refs/gpcr_coupling.csv'))}
rows = [r for r in csv.DictReader(open('refs/reference_set.pre_seal.csv'))
        if r.get('receptor_slug') in pset]
def col(role, c):
    out = []
    for r in rows:
        if r['role'] != role: continue
        try:
            v = float(r.get(c, ''))
        except ValueError:
            continue
        if v == v: out.append(v)
    return out
for c in ('d_npxxy_oh_ref', 'd_gpcrdb_tm6_tilt_ref'):
    a, i = col('active', c), col('inactive', c)
    print(c, len(a), round(statistics.mean(a), 3), len(i), round(statistics.mean(i), 3),
          round((statistics.mean(a) + statistics.mean(i)) / 2, 4))
```

**A4 impact (§4.2)** — `frozenset({"nanobody","scFv","BRIL","T4L","DARPin","minibinder"})`
intersected with the `;`-split `stabilising_elements` of every `role=active` row of
`refs/reference_set.csv`, plus the three rows of
`refs/sealed_active_refs_2026_09_01.csv`.

**Pinned-file identity (§8.5)**:

```
shasum -a 256 refs/reference_set.blockb_pinned.csv \
  ../../../../data/block_b/09_references/reference_set.blockb_pinned.csv
# 6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef  (both)
```

---

## One-line summary for the orchestrator

Their reference selection is **human curation frozen into a CSV**, measured but never
filtered by code; the state annotation is GPCRdb's `state` read by a person plus the
ligand's pharmacology, not a machine-read label; A4 is deliberately off and would refuse
25 of their active references; **their active pole is 94% partner-bound and the two
exceptions were flagged for removal** — so their calibration and our Group 0 are
entangled in the same cell of the same 2×2, which makes them comparable but means neither
validates the other, and pooling their panel rows into our calibration set is the one
move that would make it genuinely circular.
