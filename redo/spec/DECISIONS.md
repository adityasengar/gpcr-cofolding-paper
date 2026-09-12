# spec/DECISIONS.md — decisions that govern the redo, with their reasons

An outcome without its reason gets re-litigated. Newest first.

---

## D-2026-09-11-c · The manuscript stays frozen; the protocol findings feed the redo

**Aditya, 2026-09-11.** We established this afternoon that the frozen manuscript
describes an activation predicate the scorer never ran. His call: **the paper is
the record of what was done and it stays as it is.** The findings become inputs
to the redo, which is where they can still change something.

Consequence: nothing below is a correction to `manuscript/`. Every item is a
requirement on the redo.

---

## D-2026-09-12-b · D-H CLOSED — B1B1U5 stays, at 9EPP, as (c′); (e′) offered as an extension arm

**Aditya, 2026-09-12.** On the recommendation of `spec/D_H_RESOLUTION.md` §7.

**(c′).** B1B1U5 stays in the **PRIMARY** panel, which remains **30 receptors /
29 clusters**. Its `cognate_family` is **Gq** — the deposited tip is genuinely
jumping-spider Gαq1 (INSDC `LC799818`) and the experimenters' design intent was
Gq. Its `reference_tip` is **9EPP**, recorded explicitly as a spider-Gq-tipped
chimera on a human Gαi1 backbone.

**Methods must state that no native complex exists for this receptor.** 9EPP is a
chimera; 9EPR is human Gαi1 from *E. coli* reconstituted *in vitro* with **bovine**
Gβ1γ1. **`PANEL.md` Rule 4 is therefore INAPPLICABLE here, not merely
unimplemented** — its second clause requires a native option to demote to. Rule 4
stays on the books, scoped, and still unimplemented in code for the cases where it
*can* fire.

**(e′)** — supply the **spider** Gαq1 α5-CT instead of the human one — is an
EXTENSION arm, deliberately outside the primary ladder because it puts a
non-human partner into a human-partner ladder. It is **constructible only to 17
residues** (ceiling 18, the whole recorded segment): `tejero2024opsin` p10 records
18 spider residues and we do not hold `LC799818` itself, so `ct19`, `ct21`,
`a5helix`, `a5plus` and the full subunit are **not built and not invented**. In
particular the deposited 21-mer is *not* a spider 21-mer — its first three
residues are human backbone. `D_H_RESOLUTION.md` §9.2 has the rung table;
`g1_partner_registry.tsv` has the constructs, `spidertip_*`.

**Three statements this closes and corrects.**

- ~~"Three documents say 9EPR; the frozen artefact says 9EPP"~~ — the artefact was
  right. What said 9EPR was `PANEL.md`'s own prose contradicting its own §6.1
  table, plus two documents repeating it.
- ~~"the 0.86 tip is engineered"~~ — it is **species divergence**. RCSB's own
  `pdbx_mutation` for `9EPP_2` reproduces the spider segment from human Gαi1
  exactly, so this is checkable without the paper, and `gates/panel_verify.py`
  now checks it.
- ~~"invertebrate visual opsins are canonically Gq"~~ — **no locator**, and it
  must not be used as evidence (D_H_RESOLUTION §6f).

**A second defect found while implementing it.**
`g1_panel_freeze.tsv:supplied_partner_independence` claimed **"annotation only —
independent of the structure"** for **B1B1U5 and OPSD**, both PRIMARY. Neither has
any non-structure coupling authority: `coupling_assignments.csv` gives both
`n_authorities = 1`, and that authority is `authority_structure`. The column whose
whole purpose is to keep biology and structure apart was asserting independence
where the two are the same evidence. Fixed in the generator; both rows now say so.

**What is unblocked, and what is not.** B1B1U5's ligand curation is no longer
blocked on D-H, and F-11's shared-CCD trap turns out not to apply to it — 9EPP's
agonist is `A1H6M` (11,20-ethanoretinal), the 6I9K inverse agonist is `RET`
(11-cis retinal). What still blocks it is **amendment §C-1**, which dropped
`inverse_agonist` from Tier 3, and the fact that the existing curated agonist row
is keyed to 9EPR. Both are decisions, not chemistry. `LIGAND_CURATION_PROPOSAL.md`.

**What still makes this uncomfortable, recorded rather than resolved.**
`tejero2024opsin` reports that TM5/TM6 open **further** in the chimera complexes
than in the hGi complex and argues the Gα subtype sets the extent of TM6
movement — the axis our predicate measures. Both chimera models are also
incomplete at the cytoplasmic end of TM6, at 4.06/4.15 Å against 9EPR's 4.9 Å.
This does not argue for 9EPR, which is not native and worse-resolved; it means
**B1B1U5's reference geometry is the least trustworthy in the primary panel**,
and it deserves a per-receptor sensitivity check in the measurement pass.

---

## D-2026-09-12 · Four campaign decisions, from `CAMPAIGN.md` §10

**Aditya, 2026-09-12.** All four taken on the recommendation.

**D-A — the state is called from NPxxY-OH alone; the TM6 tilt is reported as a
continuous second axis, never conjoined.** Reason: it is the predicate that
actually ran, so Group 0 calibrates something real and our numbers stay
comparable with `paper_af3`'s. The tilt cannot be the second instrument — no
dynamic range, and circular on the same atom pair as GPCRdb's inactive pole.
Methods must state why it is reported and not conjoined. **Cost: 2 of the frozen
30 (EDNRB, HRH3) become NPxxY-blind with no inherited fallback** — they need an
explicit rule, not a silent NaN.

**D-B — closed by measurement, not choice** (see F-5). The partner runs MSA-free
at every rung. The residual arm (E1.9, +1,200 in the pilot) answers "how much did
we change by doing that?", which is the first question a referee asks. Keep it.

**D-C — curate small-molecule agonist/antagonist pairs for six receptors.**
Reason: at k = 9 clusters the interaction MDE is **0.406**, larger than every
Block B decomposition term but one, so the arm cannot do its job as it stands.
Six receptors takes k to 15 and MDE to **0.314**, for zero GPU. The eight
peptide-only-agonist receptors are a *different experiment* — a peptide agonist is
a third protein chain and flips OpenFold-3's `use_paired_msas`, and `endothelin1`
is exactly 21 residues, the same as `ct21`, so EDNRB cannot be crossed with a
peptide rung without explicit chain labelling.

**D-C WORKLIST, corrected and independently reproduced 2026-09-12.** The figures
in `CAMPAIGN.md` §5.2/§10 are **wrong** — they say 10 receptors / 9 clusters and
"curate six". Correct: **baseline 9 receptors / 8 clusters, MDE 0.431; curate
SEVEN; target 16 receptors / 15 clusters, MDE 0.314.** Aditya's decision stands and
the gain is slightly larger than he was told.

The test that matters, and the one my own first derivation missed: **a row is not a
curation.** `ADRB1`, `B1B1U5`, `GHSR`, `HRH3` and `OPSD` each carry a ligand row
with `is_peptide=false`, **no SMILES and no PDB** — verified directly against the
files. The reliable test is `is_peptide=false` AND a non-empty `smiles`, **on both
roles**. `n_agonist_smiles` in `panel_systems.csv` cannot do it: a peptide carries
a SMILES string too.

| receptor | cluster | missing | note |
|---|---|---|---|
| **S1PR1** | `001_004_004` | both | absent from both ligand sets entirely |
| **CCKAR** | `001_002_005` | agonist | curated agonist is CCK-8 (`DYMGWMDF`, peptide) |
| **GHSR** | `001_002_010` | both | agonist is ghrelin peptide |
| **ADRB1** | `001_001_003` | antagonist | placeholder row |
| **HRH3** | `001_001_005` | agonist | placeholder row |
| **OPSD** | `001_009_001_vert` | antagonist | **may be impossible — see below** |
| **B1B1U5** | `001_009_001_inv` | antagonist | **not blocked by chemistry after all** — D-2026-09-12-b |

Curate in that order; the first five carry the value.

**OPSD and B1B1U5 may not be curatable at all, and the reason is chemistry.** Both
are retinal receptors: agonist (all-*trans*-retinal) and antagonist
(11-*cis*-retinal) are the same molecule in different isomers, covalently bound
through a Schiff base. `PANEL.md` §10 already records these two among four that
Block C could not run, "and the reason is chemical, not operational."
**If they fail, k = 13 and MDE = 0.338** — still worth curating the other five.

**Coupling to D-H — now closed, see D-2026-09-12-b.** B1B1U5's curated agonist row
is keyed to **9EPR**, and D-H resolved to **9EPP**, so that row now points at a
structure the panel does not use. It must be re-keyed or explicitly marked
off-reference before it is curated. The *antagonist* candidate on `6I9K` is clean
and carries a different CCD from 9EPP's agonist, so the "both roles are `RET`"
objection above is **true for OPSD and false for B1B1U5**. {ref-history}

**D-D — build a defensible decoy rule, gate it, and run the arm only after the
rule's own search has reported a pool size.** Reason: it bears on no title clause,
so it must not consume compute before its own gate has passed. Their decoys fail
the module's own ±20% window on 3–5 of 6 axes and are systematically uncharged
against cationic real ligands.

**The ≥12-cluster threshold is WITHDRAWN.** It was set against the over-counted
ligand panel. The decoy arm can only draw on the ligand-complete set — at most 15
clusters, or 13 without the retinal pair — so ≥12 demanded an 80–92% pass rate from
a rule that all eight of `paper_af3`'s hand-picked decoys would fail. Pre-committing
to it risks building the rule, failing the gate at 9 or 10, and having nothing. Run
the search, report the pool, then pre-register a threshold against what was
observed, with a stated fallback (six-axis rule, or k=2 decoys). For planning only:
**≥10 of 15**.

**D-H — resolve the 9EPP/9EPR reference question rather than dropping B1B1U5.**
Reason: the 1.8% interval penalty is not the issue; dropping it halves the Gq arm
to n = 1, and a panel cannot be called a census with an unresolved member in it.
**→ RESOLVED the same day; see D-2026-09-12-b above. Outcome: option (c′) —
9EPP stays, cognate stays Gq, panel stays 30 / 29, and Rule 4 turns out to be
inapplicable rather than unimplemented.**

---

## D-2026-09-12-c · D-A RESOLVED — the conjunction, one axis calibrated, one inherited and validated

**Aditya, 2026-09-12**, re-decided on correct information after F-1 was retracted.
This supersedes the earlier D-A entry, which was taken on the false premise that
the two-instrument predicate never ran.

**THE DECISION. Class A keeps the conjunction — `NPxxY-OH < 9.08 AND tilt >
14.932` — which is what actually ran. Group 0 calibrates NPxxY and NOT the tilt.
The tilt threshold is inherited from `paper_af3` with its provenance stated, and
validated on the apo/cognate contrast rather than calibrated against any label.**

### Why the tilt is not calibrated

Every ground truth available to Group 0 for that axis is circular or retracted:

| candidate truth | why it fails |
|---|---|
| `state` (GPCRdb) | **the label is defined using this same atom pair**, 2×46–6×37 ≤ 11.9 Å |
| `transducer_type` | the Q0c circularity Aditya retracted; `G0-6` guards its return |
| `activation_degree` | same retraction |
| RMSD to a reference | calibration structures are off-panel and have **no reference pair**; and choosing which reference is "active" is itself a state label |

**My earlier option (c) — "calibrate the tilt against RMSD-nearest-reference" — is
withdrawn. It is circular one step removed**, and I proposed it before checking
that the data existed. It does not.

### What replaces calibration, and why it is stronger

**F-13's apo table validates the threshold without any label entering.** On Class A
the apo arm sits at tilt medians ~12 Å with only **3–15 of 40** cells above 14.932,
while the cognate arm calls **83–94%** active. That separation comes from an
**experimental manipulation — partner present or absent** — so no GPCRdb definition
participates and no circularity is possible.

**We can therefore say the threshold demonstrably separates apo from cognate on
Class A, without claiming to have derived it.** Methods states plainly that we did
not re-derive it because every available reference would have been defined using
the same measurement.

**The cost, stated rather than hidden:** we cannot claim a calibrated tilt.
Claiming a clean calibration we cannot have would be worse.

### Scope — Class A ONLY

F-13 showed the tilt fails outside Class A:

- **Class B** — Boltz and Protenix put apo at ~12 Å, Chai and OF3 at ~20 Å. A **9 Å
  disagreement about the same receptors with no partner.** No pooled Class B rate.
- **Class F** — apo medians 14.20–16.12 straddle the 14.932 cut on **every**
  backbone. No discriminating power. Confirms the standing gate WAIT: re-measure on
  2×44–6×31 or drop the arm.

**So the conjunction is a Class A instrument. B and F are separate decisions and
must not inherit this one.**

### Consequences to carry

- **`excl_npxxy_undefined` is set at DISPATCH from the anchor table, never
  discovered at scoring time.** Under a conjunction a missing NPxxY forces
  "inactive" on every row — which is how EDNRB and GRPR contributed 28% of the
  frozen campaign's errors from 5% of its rows (F-10). The exclusion is an input,
  not an outcome.
- **EDNRB and HRH3** are NPxxY-blind on the frozen panel. They are excluded from
  the binary rate, named in the figure caption, and **kept in every other arm** —
  both continuous axes, ladder geometry, engagement depth, partner pLDDT. Only the
  state call is withheld. **No tilt fallback for them**: calling 2 of 30 receptors
  on a different instrument from the other 28 is the pooled-instrument defect the
  frozen manuscript already carries.
- **The Cα variant is the coverage arm**, applied to all 30 receptors or to none.

---

## F-1 · **RETRACTED 2026-09-12. I was wrong. The two-instrument predicate IS what ran.**

**What I claimed** (and told Aditya, and told `paper_af3`): that the manuscript's
two-instrument conjunction — NPxxY-OH < 9.08 **AND** TM6 tilt > 14.932 — describes
a predicate that never scored a row, because `switch_signal.py::MotifThresholds`
holds a single metric with `K_OF_N = 1`.

**What Block A's own 9,490 rows say**, reconstructed from the raw metrics and the
per-row thresholds:

| class | n | rule that reproduces `active` |
|---|---:|---|
| **A** | 7,995 | **`npxxy AND tilt` — 100.0%** (npxxy alone 95.7%, tilt alone 91.1%) |
| B | 795 | `tilt` alone — 100.0% |
| F | 700 | `tilt` alone — 100.0% |

Zero mismatches on Class A. The conjunction is **load-bearing, not vacuous**: the
tilt overturns npxxy on **342** rows and npxxy overturns tilt on **708**.

**Where I went wrong.** There are **two instruments**, and `MotifThresholds` is only
one of them:

- the **motif instrument** — five metrics, collapsed to NPxxY-OH alone on
  2026-09-01 at 07:31;
- the **midpoint-crossing instrument** on `d_tm6` — the tilt — described at
  `switch_signal.py:71-72` as *"cross-validated against the midpoint-crossing
  instrument on d_tm6 (Pearson r = −0.681 — independent enough to carry
  non-redundant signal)"*.

**"Two-instrument success" means both, for Class A.** The 2026-09-01 collapse was
*within the motif instrument*, five metrics to one — **not** a collapse of two
instruments to one. `prediction_is_active_like` implements only the motif half,
which is why reading it alone made the predicate look single-metric.

`paper_af3`'s statement that "no scored campaign ever ran the 3-of-5 rule" is
**true and consistent with this** — the 3-of-5 was the motif instrument's internal
rule. I took their correct statement and drew a wrong conclusion from it.

**What stands, what falls:**

- **FALLS:** "the manuscript describes a predicate that produced no data." It
  describes the predicate that produced all of Block A. **The manuscript is right
  on this point and I was wrong.**
- **FALLS:** the premise under decision **D-A**. Aditya chose "NPxxY-OH alone,
  tilt reported" because I told him the conjunction never ran. **D-A must be
  re-decided on correct information.**
- **STANDS:** F-2 (the confidence circularity) — though note the gate is **not**
  baked into Block A's shipped `active`: 47 rows with `min_plddt_at_anchor < 50`
  are `active=True`, so **P7 is computable on this data**.
- **STANDS:** F-3 (9.08 applied vs 9.082 derived).
- **UNCHECKED, and now suspect:** `CLAUDE.md` says Class B "substitutes a kink
  angle". Block A's Class B rows reproduce as **tilt alone at 100%**, and
  `kink AND tilt` gives only 23.6%. The kink threshold is present on all 795 rows
  and appears unused.

---

## F-1c · WHERE THE CONJUNCTION LIVES — answered from source by `paper_af3`

Not in the scorer. `switch_signal.py::prediction_is_active_like` is **Class-A only**
and single-metric; it returns `"insufficient"` for Class B/F because NPxxY is NaN
there. **That file's docstring claim that Class B/F use "midpoint-crossing on the
per-class anchor pair" is itself stale** — the same defect class as the ≥3-of-5
language, in the same file.

**The class-conditional AND lives one layer up**, in
`scripts/block_a_campaign_analysis.py::two_instrument_state_calls()` (~line 486),
and it operates on **per-(receptor, backbone) medians** across the cognate arm's
5 seeds × 5 samples — *not* per row:

| class | rule |
|---|---|
| A | `npxxy_oh < 9.082` **AND** `tilt > 14.932` |
| B | `kink < 159.95` **AND** `tilt > 14.932` (~line 539) |
| F | `tilt > 14.932` alone |

Output artefact: `experiments/018_block_a_switch_test/analysis/two_instrument_state_calls.csv`,
offered and **worth requesting** — it is the authoritative Class B/F numbers.

**And the kink WAS eventually wired in.** `paper_af3` cite
`docs/POST_BLOCK_A_CLEANUP_2026_09_02.md` Finding 3 verbatim: *"Design error, not a
data error. The class-extension work delivered the Class B kink metric to the schema
but never wired the predicate to use it. The extension was on paper only."* Fixed
2026-09-02.

**So my "Class B reproduces as tilt alone, 100%; kink AND tilt gives 23.6%" is
correct for the state Block A's delivered rows are in — pre-fix — and must not be
read as describing the project's current Class B numbers.** Their standing rule:
do not diff pre-cleanup against post-cleanup Class B figures; they are different
axes. Block A's shipped rows carry `threshold_kink_used = 159.95` on all 795 Class B
rows, which is exactly the "delivered to the schema, never wired" signature.

---

## F-1b · What was actually stale (the surviving part of the original finding)

The **module header docstring** at `switch_signal.py:14-20` still describes the
motif instrument as "≥3 of the 5 motif metrics", which the 07:31 collapse
superseded. That much is genuinely stale and `paper_af3` confirmed it. It is a
docstring defect inside one instrument — **not** evidence that the second
instrument does not exist.

**What the scorer does** — `scorer/switch_signal.py::MotifThresholds`, in the
bundle at `protocol/received/source_bundle/`:

```
METRIC_SPECS = (("d_npxxy_y558_y753_oh", 9.08, "active_lt", "NPxxY OH-OH"),)
K_OF_N = 1        MAX_MISSING = 0
```

One metric. The GPCRdb TM6 tilt and the Class B kink appear only in the comment
on `K_OF_N`, as things that *could be re-added* — "a config change, not a code
change". The tilt is a **fallback** for receptors with non-Tyr at 5.58 or 7.53,
never a conjunct.

**What we have been writing** — two instruments ANDed, class-conditional:
NPxxY-OH < 9.08 Å AND tilt > 14.932 Å.

**Their collapse was sound and is not in dispute.** Locked 2026-09-01 on the
evidence in `refs/thresholds_panel.csv`: DRY is TM6 re-measured (r = +0.913),
NPxxY-OH and Y5.58-pack are collinear (r = +0.784) with the pack metric
self-classifying at only 71.1%, TM5-outward and ICL2 helicity separate by under
0.1 Å. NPxxY-OH alone reaches 94.3% (32/36 A→A, 34/34 I→I) on 70 of 80 tier-1 rows.

**`paper_af3` established the sharper fact**, from their git log: the collapse
landed 2026-09-01 07:31 and the Block A dispatch tag is *after* it. **No scored
campaign ever ran the ≥3-of-5 rule.** Our description names a predicate that
produced no data — not a superseded one, an unused one.

**Where it came from, and the lesson.** The module *header* docstring still
describes the pre-collapse ≥3-of-5 composite; the class docstring below it
records the collapse. We inherited the header. This is the project's recurring
failure exactly — scope asserted in the most-read text and qualified in the
least-read text. See `[[scope-is-asserted-where-it-is-most-read]]`.

**Requirement on the redo:** Group 0 calibrates the instrument that actually
exists — single-metric NPxxY-OH. If we want a second instrument, we build and
justify it ourselves rather than inheriting one from a docstring. `g0_preflight`
check **G0-10** already records the class F tilt defect and is the right place
to carry this.

---

## F-10 · P7 IS COMPUTED. The null holds: pLDDT does not separate.

**The paper's third title clause had never been computed anywhere.**
`paper_af3`'s own analysis emits it as
`{"status": "descriptive_placeholder", "note": "requires per-row pLDDT column;
deferred to analysis-time"}`. Computed 2026-09-12 on Block A's delivered rows, no
GPU. Code `build/p7_confidence_separation.py`; results
`inputs/p7_confidence_separation.{csv,json}` and `inputs/p7_per_receptor.csv`.

**Why it was computable here at all.** The scorer's row classifier forces
"inactive" below pLDDT 50 before reading geometry (F-2), which would make the
question circular. **Block A's shipped `active` column does not carry that gate** —
47 rows with `min_plddt_at_anchor < 50` are `active=True` — so on this data
confidence and the state call are independent and the question is answerable.

**Design.** Ground truth is structural, not the predicate's own output: a
prediction is really active iff `rmsd_to_active_ref < rmsd_to_inactive_ref`.
n = 7,886 rows, 40 receptors, 26 clusters. Predicate accuracy against that truth
is **92.3%**. Exclusions E1 + E2 only — never `excl_any`; E3 is excluded on our own
`METHODS_DRAFT.md:115-117`, which records it as irrelevant to confidence
correlations. Cluster bootstrap, 10,000 resamples, seed 20260912.

| metric | pooled AUC | within-receptor |
|---|---|---|
| `plddt_mean` | 0.600 [0.495, 0.689] | 0.558 [0.444, 0.660] |
| `min_plddt_at_anchor` | 0.473 [0.386, 0.588] | 0.567 [0.411, 0.705] |
| `plddt_at_anchors` | 0.545 [0.458, 0.661] | 0.552 [0.381, 0.697] |

**Every interval includes 0.5, at both scopes, on all three metrics. The null is
supported: confidence does not separate correct from incorrect state calls.**

**REFINED 2026-09-12 — the primary analysis now EXCLUDES the 400 forced-inactive
rows** (EDNRB, GRPR; see the mechanical-error trace below). Those rows cannot
answer this question, because no call was made from the geometry — including them
risks measuring "does confidence predict being an unevaluable receptor" instead.
Primary: **7,486 rows, 38 receptors, 24 clusters, predicate accuracy 94.2%.**

| metric | pooled (primary) | within-receptor | pooled if included |
|---|---|---|---|
| `plddt_mean` | 0.578 [0.455, 0.685] | 0.571 [0.438, 0.683] | 0.600 |
| `min_plddt_at_anchor` | 0.507 [0.407, 0.659] | 0.609 [0.442, 0.752] | 0.473 |
| `plddt_at_anchors` | 0.573 [0.467, 0.721] | 0.583 [0.395, 0.729] | 0.545 |

**Robustness, checked 2026-09-12.** All four generated artefacts reproduce
byte-identically on re-run, and the bootstrap intervals move by at most **0.0031**
under a different resample seed (20260912 vs 777001) — so 10,000 resamples is
ample and every interval spans 0.5 under both. The conclusion is not seed-dependent.

**The exclusion changes nothing, and that is the useful result.** The deltas are
**mixed in sign and ≤ 0.033** (+0.022, −0.033, −0.028), every interval still spans
0.5 at both scopes, and the conclusion is identical either way. **P7's null is
robust to the single most contestable analysis choice in it.** My first reading of
these deltas — that the excluded rows "inflate" the separation — was wrong; they do
not move it in a consistent direction at all.

**The error I made and caught.** The first run reported within-receptor AUCs of
0.645–0.681 with intervals *excluding* 0.5 — i.e. the opposite conclusion. That was
an artefact of my own aggregation: accuracy is 92.3%, so errors are rare and
**concentrated** — 10 of 40 receptors have zero wrong calls and 22 have fewer than
five — and an unweighted mean over receptors gave one with a single error the same
weight as one with a hundred. Requiring **≥10 wrong and ≥10 correct** leaves **14 of
40 receptors** carrying an AUC, and the effect disappears. The exciting version was
the wrong version.

**Two things worth carrying into the redo:**

- **The errors are concentrated: the top five receptors hold 59% of them.** A
  pooled accuracy figure hides that the predicate fails on specific receptors
  rather than degrading evenly. Per-receptor accuracy belongs in the redo's
  reporting.

- **AND HALF OF THAT CONCENTRATION IS MECHANICAL, NOT A PREDICATE FAILURE.**
  Traced 2026-09-12 after `paper_af3` sent `two_instrument_state_calls.csv`.
  **EDNRB and GRPR carry no NPxxY axis at all** — `d_npxxy_oh` is null on all
  400 of their Class A rows — and because the Class A rule is `npxxy AND tilt`,
  **NaN propagates to False and they are called active on ZERO rows.** Structural
  truth says **43%** of those rows are active, so their accuracy is **57%**, which
  is not the predicate being wrong about them; it is the predicate never running.

  **Those two receptors contribute 172 of 607 errors — 28% of every error in the
  campaign — from 5% of the rows.** Campaign accuracy is **92.3% including them
  and 94.2% excluding them**.

  **`5HT2C` is NOT in this class** — its NPxxY axis is defined and its 99/200
  errors are real. So of the two receptors I flagged as "at chance", one is an
  artefact of an unevaluable axis and one is a genuine failure. **They should never
  have been named in the same breath, and the distinction is only visible if you
  check which axis exists.**

  **This is decisive support for D-A's exclusion rule.** The campaign agent's
  recommendation — that `excl_npxxy_undefined` be a **per-row boolean set at
  dispatch from the anchor table**, not discovered at scoring time — is exactly
  what would have prevented this. A silent NaN did not merely lose two receptors;
  it injected 28% of the campaign's apparent error as a mechanical artefact and
  depressed the headline accuracy by 1.9 points.

- **Class B and F are unaffected** and it is worth saying why: their rule is `tilt`
  alone (B post-fix adds the kink), which needs no NPxxY, so the eight Class B/F
  receptors with undefined NPxxY are scored normally.

- **Three checker bugs of mine getting to this number**, all caught before it was
  recorded: I used `excl_E3_npxxy` as the blindness test (it flags *two* causes —
  failing references AND unmeasurable axes, as `METHODS_DRAFT.md:112-115` states),
  then `d_npxxy_oh.isna()` across all classes (which sweeps in Class B/F, who do
  not need the axis), before restricting to Class A. The first two gave 59% and
  34%; the right answer is 28%.
- **This bears on `HANDOVER.md`'s standing claim**, which says confidence separates
  pooled (AUC 0.60–0.96) and that this "evaporates when you control for receptor".
  The direction is right but the pooled figure is not reproduced here: pooled AUCs
  are 0.47–0.60 with intervals spanning 0.5. That claim should be re-derived or
  withdrawn before it reaches a sentence.

---

## F-13 · The apo arm: Class B is not saturated, but the backbones disagree by 9 Å — and the Class F threshold has no discriminating power at all

`paper_af3` sent `two_instrument_state_calls_apo.csv` (sha256 `361ce5a2…`) after
Aditya signed off in their session. It was requested to settle one question and
answered three.

**The question asked — is Class B saturated? No.** Cognate 1.000 against apo 0.250
on Boltz and Protenix is a large, real separation. The Class B result is not an
artefact of an instrument that calls everything active.

**But two backbones show ZERO separation, on both B and F:**

| class | backbone | cognate | apo | gap |
|---|---|---:|---:|---:|
| B | boltz | 1.000 | 0.250 | +0.750 |
| B | chai | 1.000 | 0.750 | +0.250 |
| **B** | **of3** | **1.000** | **1.000** | **0.000** |
| B | protenix | 1.000 | 0.250 | +0.750 |
| **F** | **of3** | **1.000** | **1.000** | **0.000** |

### (a) Class B — the backbones disagree by 9 Å on the same input

Apo tilt medians, same four receptors, same apo input, threshold 14.932:

| backbone | median apo tilt | above threshold |
|---|---:|---:|
| boltz | **12.38** | 1/4 |
| protenix | **12.53** | 1/4 |
| chai | **21.47** | 3/4 |
| of3 | **19.60** | 4/4 |

**Boltz and Protenix predict Class B apo receptors CLOSED at ~12 Å; Chai and OF3
predict them OPEN at ~20 Å.** That is an **8–9 Å disagreement about the same
receptors with no partner supplied** — larger than the active/inactive separation
the threshold was built to detect. This is not a threshold problem; it is two
backbones and two backbones predicting different structures.

**Requirement:** the redo cannot report a pooled Class B rate. A number averaged
over backbones that disagree this violently describes nothing.

### (b) Class F — the threshold sits inside the apo distribution, on every backbone

Apo tilt medians run **14.20, 15.09, 16.10, 16.12** against a **14.932** cut. Every
backbone straddles it. **The Class A-derived threshold has no discriminating power
on Class F at all**, regardless of backbone.

**This empirically confirms the standing `g0_preflight` WAIT** ("the redo must
measure class F tilt on 2×44–6×31, not 2×46–6×37, or drop the class F arm"). That
was a geometric argument; this is the measurement. **Class F as currently
instrumented cannot distinguish apo from cognate.**

### (c) SMO gets LESS open when the partner is added

`SMO` apo tilt 18.38, cognate 16.24 — **−2.14 Å in the direction opposite to the
hypothesis**. `FZD7` is also negative (−0.07, negligible). Two of three Class F
receptors do not move the way the model predicts, which is consistent with (b):
the axis is not measuring activation on this class.

### Bearing on D-A

The tilt is one of the two instruments in the conjunction. **On Class A it behaves
well** — apo medians ~12 with only 3–15 of 40 above threshold, so the cut
discriminates. **It is on B and F that it fails**, which is where it is used
*alone* (B adds the kink post-fix; F is tilt-only). So D-A's choice about the Class
A conjunction is not undermined by this — but any decision to extend the tilt to
Class B or F is.

---

## F-12 · F3 may be discarding the inactives nearest the decision boundary — PRELIMINARY, n = 4

**Status: a signal worth testing, not a finding.** Stated with its n so it cannot be
quoted as more than it is.

F3 — "GPCRdb state label not contradicted by the entry's own ligand pharmacology" —
removes **27 inactives from the calibration pool (88 → 61), 31% of the scarce
class**, concentrated in five receptors (`5HT2A` loses 10). Inactives run 6.1:1
against actives in the frozen ladder, so this is the single largest discretionary
cut in Group 0.

**The full sensitivity arm cannot be built yet.** `g0_calibration_structures.csv`
carries **no measured axis values** — the measurement pass is still an outstanding
Group 0 dependency, and the cache holds 297 of 726+ structures. Only
`g0_pilot_measurements.csv` has `d_npxxy_oh` and `d_tilt`, for 30 structures.

**But the pilot happens to sample the discarded population — 6 of its 30 — so a
preliminary look is possible:**

| state | group | n | median `d_npxxy_oh` | median `d_tilt` |
|---|---|---:|---:|---:|
| Inactive | retained by F3 | 6 | **11.51** | 11.95 |
| Inactive | **F3-removed** | **4** | **9.43** | 11.79 |
| Active | retained | 7 | 4.47 | 17.87 |
| Active | **F3-removed** | **1** | **25.59** | 15.24 |

**The concern, in one line: the NPxxY threshold is 9.08, and the inactives F3
discards sit at 9.43 while those it keeps sit at 11.51.** If that holds at scale,
F3 is removing the inactives *nearest the decision boundary* — which would make the
inactive pole look cleaner than it is and bias the threshold outward, inflating the
apparent active/inactive separation.

**On the active side F3 looks straightforwardly right:** the one removed active has
`d_npxxy_oh = 25.59` against a retained median of 4.47. That is a genuine
mislabel, exactly what the rule is for.

**So F3 may be doing two different jobs** — correctly catching mislabelled actives,
and possibly over-removing borderline inactives — and a single flag cannot separate
them.

**n = 4 and n = 1. This is a direction, not a result.** The test that settles it:
run the measurement pass, then recompute both thresholds with F3 on and off and
report the shift. If the thresholds barely move, F3 is not consequential and D3
simplifies. If they move, **F3 needs to be split by which side of the label it is
correcting** — and that is a decision for Aditya, not a filter setting.

**Requirement on the redo:** the measurement pass must record the axis values for
the F3-*removed* structures too, not only the survivors. A filter whose effect
cannot be measured after the fact is a filter nobody can audit.

---

## F-11 · Retinal must be curated by ISOMER, not by CCD — and the agonist-bound-inactive population is not one thing

Both halves verified independently against the frozen GPCRdb snapshot; found by the
lit session, confirmed here.

**(a) One CCD code, two opposite pharmacologies.** Of the 41 snapshot entries
carrying CCD `RET`, GPCRdb ships **three distinct isomer names**:

| name | state | function | n |
|---|---|---|---:|
| Retinal (11-cis) | Inactive | **Inverse agonist** | 16 |
| Retinal (all-trans) | Active | **Agonist** | 14 |
| Retinal (all-trans) | Inactive | Agonist | 4 |
| Retinal (11-cis) | Inactive | Agonist | 3 |
| **Retinal (11-cis)** | **Active** | Agonist | **2 — 9EPR and 8IU2** |
| Retinal (9-cis) | Inactive | Inverse agonist | 2 |

**11-cis is the inverse agonist and all-trans is the agonist, and they share a CCD
because they are isomers of one compound.** Any pipeline keyed on CCD alone sees one
ligand where there are two pharmacological opposites. **Requirement: curate retinal
by isomer name, never by CCD.**

**CORRECTED 2026-09-12 — I reported the candidate POOL's property as the reference
PAIR's, and they differ.** I wrote that OPSD and B1B1U5 both carry `RET` in both
roles. True of every structure of those receptors; **false of the pairs we actually
score against**, which is the only scope curation cares about:

| receptor | active ref | its ligand | inactive ref | its ligand |
|---|---|---|---|---|
| **B1B1U5** | `9EPP` | **11,20-ethanoretinal, `A1H6M`**, Agonist | `6I9K` | 11-*cis* retinal, `RET`, Inverse agonist |
| OPSD | `4X1H` | β-nonylglucoside — a **detergent** | `7ZBC` | 11-*cis* retinal, `RET`, Inverse agonist |

**B1B1U5 is therefore NOT blocked by the shared-CCD problem.** Its two reference
ligands are chemically distinct and carry different codes. **OPSD is blocked, but
for a different reason than I gave** — its active reference carries no agonist at
all, only a detergent. A missing-ligand problem, not an isomer one.

The general finding is untouched: across all 41 `RET` entries, 11-*cis* is the
inverse agonist and all-*trans* the agonist.

**(b) 9EPR's isomer name is wrong in GPCRdb.** `tejero2024opsin` p2 states 9EPR was
reconstituted with **9-cis retinal and illuminated at 495 nm** to activate it, so
the modelled chromophore is **all-trans**. GPCRdb calls it 11-cis. It sits in a
two-entry outlier class against a fourteen-entry majority. **The function
annotation (Agonist) is right; only the isomer name is wrong** — a per-entry error,
not a systemic limitation, since GPCRdb demonstrably has the vocabulary.

**(c) Bears on Group 0's D3, and this is the part that matters.** Of **81**
agonist-bound *Inactive* structures in the snapshot, **8 are opsin/retinal
photo-intermediates** — agonist covalently bound, receptor not yet in the active
conformation — including **8A6E, which is in our own panel as an inactive
reference**. The other 73 are something else: partial agonism, or annotation drift.

**The agonist-bound-inactive population is heterogeneous, and D3 must not treat it
as one class.** Lumping a bathorhodopsin-like photo-intermediate with a
partial-agonist complex blurs exactly the distinction D3 is trying to measure.

**(d) SCOPE CORRECTED — and it does NOT land where I first thought.** I pursued
this as a threat to the Group 0 calibration ladder. It is not one:

- **All 8 opsin photo-intermediates carry `role='application'`, not
  `'calibration'`.** They are panel-receptor structures, excluded from the
  calibration pool at F0 by the panel/calibration split. **They never touch the
  frozen F4 ladder.**
- **F3 — "GPCRdb state label not contradicted by the entry's own ligand
  pharmacology" — removes 27 inactives from the calibration pool (88 → 61), and
  NONE of them are opsins.** They are `5HT2A` (10), `LGR4` (6), `MTR1A` (5),
  `MTR1B` (4), `NTR1_rat` (4) and four singletons. For these, "agonist-bound but
  labelled inactive" is a genuinely different phenomenon — partial agonism,
  annotation drift, or an inactive-state structure with an agonist soaked in —
  and *none* of it is photochemistry.

**So D3's real question is sharper than the one I was about to ask.** F3 discards
**31% of the inactive pool** (27 of 88) on a single rule, and the losses are
**concentrated in five receptors**, one of which (`5HT2A`) loses ten. Inactives are
the scarce class — the frozen ladder runs 372 active to 61 inactive, 6.1:1 — so a
rule that removes nearly a third of them, unevenly, deserves its own sensitivity
arm rather than a flag. **That is what D3 should decide, and it is not about
opsins.**

**(e) Where the opsin finding DOES land: the panel's own references.** `lee2026confornets`
uses **8A6E** as its inactive reference for bovine rhodopsin — a **100-picosecond
light-activated XFEL structure** from a time-resolved series (8A6C/8A6D/8A6E =
1/10/100 ps, "Ultrafast structural changes direct the first molecular events of
vision"). GPCRdb annotating it *Agonist on an Inactive structure* is the tell.

**We do not use it. We use 7ZBC** — same deposition, same 1.8 Å, but annotated
**inverse agonist**, consistent with the unilluminated dark-state control of that
series. **Our choice is the better one**, and this is the second receptor
(with B1B1U5) where our reference differs from the published benchmark's in our
favour. It is worth saying so in Methods rather than leaving it implicit.

**Two checker bugs of my own on the way to this**, both caught before anything was
recorded: I filtered the flag columns with `in ("1","True")` when
`flag_label_conflict` holds a *reason string*, and then with truthiness, when the
CSV writes `'0'` — a non-empty, therefore truthy, string. Both produced "0 removed"
and both were mine, not the data's.

---

## F-2 · The state call is not independent of confidence

`prediction_is_active_like` returns `"inactive"` **before any geometry is read**
when `confidence_flag == "low"`, and `confidence_flag` is a pure function of
`min_plddt_at_anchor` (low < 50, borderline 50–70, high ≥ 70), verified
independently across all 32,000 Block B rows.

So **every prediction with minimum anchor pLDDT below 50 is called inactive
whatever its structure.** `paper_af3` confirms it is intentional, that there is
exactly one classifier and no variant or toggle, and — in their words — that
this is *"a real circularity, not an artefact"*.

The paper's third title clause is that model confidence does not track state
correctness. That claim and the state call are not independent by construction.

**Requirement on the redo: drop the early return.** Let geometry stand alone and
carry confidence as a separate reported axis. `paper_af3` named the same fix.

---

## F-3 · 9.08 is applied; 9.082 is derived

`refs/thresholds_panel.csv` records `threshold = 9.082` from means (5.285,
12.878), whose true midpoint is 9.0815. The code constant is **9.08**, rounded,
and its inline comment rounds the means too, to (5.28, 12.88).

`paper_af3` told us 9.08 was locked and our 9.082 was drift on our side; their
own lock file says otherwise. Our number came from their panel and was right.
Corrected with them 2026-09-11.

**RESOLVED EXHAUSTIVELY 2026-09-12. Both values are live, in different layers.**

- **Row level (the scorer):** Block A's delivered rows carry
  `threshold_npxxy_used = 9.08` and nothing else, and `npxxy_active` reproduces
  from `d_npxxy_oh < 9.08` at **exactly 100.000%** of Class A rows.
- **Analysis level:** `paper_af3` report that
  `scripts/block_a_campaign_analysis.py::two_instrument_state_calls()` applies
  **`npxxy_oh < 9.082`**, on per-(receptor, backbone) medians.

**The two thresholds disagree on exactly ONE row in the entire campaign**, and we
can name it: **`B1B1U5` / `of3` / `apo`, `d_npxxy_oh = 9.080077`** — inactive under
9.08, active under 9.082. One row of 7,995 Class A, in the apo arm, and the
analysis layer works on medians, so the practical consequence is nil.

**The redo pins ONE value in ONE place and asserts it.** Two layers carrying two
roundings of the same derived number is how a discrepancy survives four blocks
unnoticed; that it cost nothing here is luck, not design.



---

## F-4 · There is no Gα-side numbering to inherit

`paper_af3` confirm: no CGN import anywhere in the scorer. Partner positions are
raw UniProt index, or counted from the C terminus ad hoc when treating α5-CT.

The redo's entire ladder is defined by position on the Gα C terminus.
**Requirement: we define a CGN-based convention, freeze it in `spec/`, and send
it to them** — they have said they will adopt whatever we define.

---

## F-5 · The ladder is not a smooth axis, and depth does not track length

Measured by `paper_af3`, in the bundle at
`experiments/019_block_b_partner_selection/analysis/msa_depth_report.md:353-359`
— verified against the primary table, not relayed:

| partner | aa | MSA depth |
|---|---:|---:|
| DAMGO | 5 | **1** |
| substanceP | 11 | **1** |
| endothelin1 | 21 | 732 |
| gcn4 zipper | 33 | 224 |
| random_helix_40mer | 40 | **1** |
| **arrestin_Ctail** | **41** | **1** |
| Gg2 | 71 | 3,191 |
| cognate Gα | 350-394 | 11,904-14,986 |

A 21-mer retrieves more than a 33-mer; a 40-mer returns query-only while a 15-mer
returns 84. **The predictor is naturalness, not length** — whether the sequence
has homologs in the searched databases. Their own note at `:378-383` says so.

**`arrestin_Ctail` is the case that governs our design.** 41 residues, an
*excised fragment* of a larger protein, depth 1. Our α5-CT rungs are excised
fragments of Gα — the same case.

**Consequence if the short rungs return depth 1:** on Boltz, OF3 and Protenix the
paired-alignment axis is degenerate for short rungs and progressively less so for
long ones. The apo→cognate operational difference then shrinks toward Chai's as
the partner shortens, and **the ladder varies peptide length and pairing regime
together** — the exact confound the redo exists to remove.

**MEASURED 2026-09-11 by `paper_af3`, 112 rows, 16 Gα families × 7 rungs. F-5 is
no longer a hypothesis — it is confirmed, and it is worse than predicted:**

| rung | measured MSA depth |
|---|---|
| **R1_ct11** | **0, across 16 of 16 families** — no database homologs at all |
| **R2_ct15** | **family-dependent: 0 for Gq/G11/G14/G15/G12, 2-459 for the rest** |
| R3_ct21 | 47-581, all non-zero |
| R4_a5helix | 186-1,995 |
| R5_a5plus | 2,273-3,043 |
| R6a_da5 / R7_full | 8,474-9,203 |

**Raw table received as a file: `protocol/received/rung_msa_depth.csv`, 112 rows,
sha256 `bb45b4b1…`.** Two refinements it forced, neither visible in the summary:

- **`ct15` is not "5 zero, 11 non-zero" — it is degenerate for 15 of 16 families
  with a single outlier.** The eleven non-zero families read Golf 2, Gz 6, G13 18,
  Ggust 21, Gt1 21, Gt2 21, Gi3 25, Gi1 33, Gi2 33, Go 42 — and **Gs 459**, an
  order of magnitude above everything else. Gs is the most common cognate partner
  on any GPCR panel including ours, so under an MSA-on design `ct15` would behave
  one way for Gs and another for every other family. **This makes the case for a
  constant regime without reference to the zeros at all:** even where alignments
  exist at the short rungs they vary across families by two orders of magnitude.
- **`unpaired_depth = -1` is a timeout sentinel**, not a depth — three rows
  (R7_full/Gi2, R7_full/Gz, R6a_da5/Gz). Any mean, min or monotonicity check over
  that column must filter on `note == "ok"` first. Flagged to `paper_af3`.

`ct11` at depth 0 forces single-sequence on every backbone. But **`ct15` is the
finding neither side predicted**: at a *single rung* the alignment regime varies
**by Gα family**. The ladder does not merely confound length with pairing along
its length — at `ct15` it confounds them *across the panel within one rung*.

**Consequence: the MSA-free partner is MANDATORY, not one mitigation among four.**
With a natural partner MSA the alignment regime becomes a function of both rung
and family and no contrast along the ladder is interpretable. Running the partner
MSA-free at every rung makes the regime constant by construction.

**This puts the harness change on the critical path.** The dict route already
exists (`propose.py:462-465` — an empty string for a chain makes the loop skip it,
which *is* MSA-free) but has no caller. Needed: a caller passing
`{"A": <receptor a3m>, "B": ""}`, the same for Protenix at `:589`, and a new
branch for Chai. **Feasibility ANSWERED 2026-09-12: yes.** `paper_af3` confirm OF3
(`chains[*].main_msa_file_paths` / `paired_msa_file_paths`) and Protenix
(`proteinChain.unpairedMsaPath` / `pairedMsaPath`) already take per-chain paths
natively in the JSON, and Boltz's inline YAML `sequences[*].protein.msa` is
per-chain too. **Chai is the sole gap** — `--msa-directory` is keyed by sequence
sha256, not chain id, and has no `MSA_A3M_PATH` branch at all, so it pulls
full-depth per chain regardless of rung. Their scoping: one caller building a
`chain_id -> path_or_empty` dict, plus for Chai writing the intended pqt directly
rather than relying on hash lookup into the shared cache. Not a redesign.

**Our refinement, sent the same day: the partner gets an explicit QUERY-ONLY
alignment (depth 1) at every rung on all four backbones — never an absent one.**
Omission relies on four different fallback behaviours we have not measured, and
the bad case is silent: a backbone that generates its own alignment for a chain
it finds no file for would deliver *full depth* exactly where we intended zero,
with nothing in any status JSON showing it. Depth 1 is constant by construction,
identical across backbones, and **verifiable after the fact** — an absence is not.

**And the partner's OBSERVED alignment depth must be recorded on every row**, not
its intended depth. Per F-6 no MSA metadata reaches any scored row today, which is
why the `ct11` cliff had to be established from a side report rather than from the
rows. With observed depth recorded, "the alignment regime was constant along the
ladder" becomes demonstrable from the data instead of asserted from the design.

**Decision D-B in `CAMPAIGN.md` is therefore closed by measurement, not by choice.**

Paired addendum authorised and scoped: skip `ct11` (depth 0 bounds paired at 0),
skip the zero-depth families at `ct15`, run `ct21`+ across ~3 receptors, ~40
alignment-only submissions. Its value is now **documentary** — it converts
"we avoided a confound" into "we measured it, then removed it". If the cliff is real, the
ladder is redesigned — candidate mitigations are to run the ladder
single-sequence on all four backbones so the alignment regime is constant, or to
carry depth as a measured covariate on every row, or both.

---

## F-6 · No MSA metadata reaches any scored row

Grep of every row-touching scorer module for `msa|a3m|pqt`: **zero matches**.
Across all 42,180 predictions there is no depth, source, pairing state or
alignment hash. **MSA cannot be joined to outcome at all** in the existing
campaign — which is why F-5 had to be established from a side report rather than
from the rows.

**Requirement:** `g1_recording_spec.tsv` carries partner-MSA depth, receptor-MSA
depth, pairing state and alignment provenance on every row. Already sent to
`paper_af3` as part of our frozen input set.

Related, and flagged to them as a question rather than a finding: `msa_prewarm.py`
appears to pre-warm only single sequences in `mode=env`, while the paired
directories are `pairgreedy-env` and OF3's paired hash is complex-keyed — which
would mean apo arms hit a warm cache and cognate arms paid a cold search, an
uncontrolled difference between the two arms the paper contrasts. Unconfirmed;
the `_of3_colabfold_http_summary.json` sidecars would settle it.

---

## F-7 · Block C's cognate arm supplies a non-cognate Gα for 35 of 40 receptors

All three Block C manifest builders hard-set `COGNATE_PARTNER_IDENTITY = "alphas"`
(`build_block_c_tier1_manifest.py:104`, `tier3:150`, `smoke:77`) and assign it to
every cognate row without consulting the coupling table. 6 of 8 Tier-1 and 29 of
32 Tier-3.

**Block A's own code names this failure and avoids it**
(`build_block_a_manifest.py:48-51`): *"A blanket alphas would recreate the W54
taxonomy failure."* They ship `verify_cognate_identity.py` to catch it. Nothing in
the bundle documents Block C as an exception. **Asked, not yet answered.**

Bears on the highest-value unblocked result in `HANDOVER.md` — the uncrossed
ligand-class × partner-presence comparison over ~18,400 scored predictions. If the
cognate arm is 35/40 non-cognate it contrasts apo against *arbitrary-Gα*.

**Requirement:** the redo reads the cognate Gα per receptor from
`coupling_cognate_map.tsv` and `g1_preflight` check **B16** already enforces that
every row carries both the supplied family and the reference tip. Keep it.

---

## F-8 · The analysis layer's stated unit is not its implemented unit

- The provenance JSON declares `two_stage_cluster_resample_receptors_then_seeds`
  (`analyse_block_c_tier1_headline.py:32-34`, `:601-604`); `bootstrap_receptor_mean`
  is one loop over receptor scalars and never draws a seed.
- Block A's primary axis is bootstrapped **over rows** — `task_f_block_a_recheck.py`
  builds `per_receptor_dtm6` and never reads it.
- The seed-is-the-unit-of-variance rule at `switch_signal.py:8-12` is implemented by
  `per_seed_mean`, `delta_d_tm6_per_cell` and `per_receptor_backbone_rollup`, all with
  **zero callers**; the wrapper its docstring names is not in the bundle. All 13
  analysis scripts work row-wise.
- `PREREG.md` contains the word "cluster" **zero times**.
- **P7, the pre-registered null that pLDDT does not separate, was never computed** —
  `analyse_block_c_tier1_headline.py:383-386` emits `"descriptive_placeholder"`. That
  is the paper's third title clause.

**Requirement:** the redo's statistical unit is the paralog cluster, declared once,
implemented once, and proved by a test that fails when the unit changes. P7 is
computed, not inherited.

---

## F-9 · Nothing in the pipeline compares output to input

Not sequence, not chain count, not seed-used vs seed-requested, not MSA depth. A
monomer returned where a receptor + Gα dimer was requested passes every check.
`ok = exit_code==0 and len(produced)>0`, so one CIF out of a requested hundred reads
`ok=true`. Two guards were found policing artefacts the run never consumed — OF3's
`sentinel_bug_seed_present` inspects a top-level `_runner_seeds.yml` that the chunked
branch writes and never reads.

**Requirement, and it is the cheapest hardening available:** three assertions in a
post-run receipt — returned sequence matches requested, chain count matches, seed used
matches seed requested. No GPU. The delivery contract in `runs/README.md` should
refuse a run that cannot answer them.

**Closed, not open:** the OF3 inner-seed formula is
`random.seed(pred_seed * 1_000_003 + chunk_idx)` (`qsub/rerun_of3.sh:194`), reproduced
exactly against all four chunks of the OPSD cell. The earlier failure to derive it was
ours reading a snapshot with no chunking branch.

---

## Still open at the close of 2026-09-11

- **Was a peptide ever dispatched as the partner chain?** Unresolved. Their
  catalogue stocks `endothelin1` (21 aa), `substanceP` (11), `arrestin_FL` (15,
  a legacy mislabel), `DAMGO` (5), and two decoys. The manifest they sent to
  settle it is the **deep-apo tier** — `partner_type=apo` on all 140 rows, no
  partner of any kind. Awaiting the `019_block_b_partner_selection` manifest.
- `build_weekend.py` — the templater `propose.py` says it was adapted from, with
  byte-parity where feasible. Not in the bundle; requested.
- `docs/BLOCK_A_STEP3_VALIDATION_2026_09_01.md` — the human-readable half of the
  threshold lock. Claimed present, absent from the archive; requested.
- Group 0 **D2, D3, D4** and the class F atom pair remain with Aditya.
