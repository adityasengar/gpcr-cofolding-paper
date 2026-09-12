# DRULE_CHEMBL_SCOPE.md — the decoy pool extraction, specified

**Decision D-D (2026-09-12): build a defensible decoy rule, gate it, and run the
arm only after the rule's own search reports a pool size.** `CAMPAIGN.md` §5.3
specifies the *rule*. This specifies the *extraction that feeds it*, which
`CAMPAIGN.md` explicitly leaves undesigned. No compute; this is a scoping document.

## Why the existing decoys cannot be reused

A decoy in Block C is a **hand-picked FDA-approved drug, one hard-coded per
receptor** — ADRB2 → tramadol, ADRB1 → aspirin, HRH1 → metformin, CCR5 → imatinib.
The module's title says "property-matched". The only enforced gate is Morgan
Tanimoto < 0.30; the ±20% property window is computed, written to a report, and
never acted on. **All eight Tier-1 decoys pass the similarity gate and miss the
property window on three to five of six axes**, and they are systematically
uncharged against cationic real ligands.

So the decoy arm currently tests "does a structurally dissimilar, physicochemically
unmatched molecule fail to activate?" — which is not the question. The question is
whether a molecule *matched on everything except binding* fails to activate.

## What "no measured activity" must mean, precisely

The rule requires candidates with **no measured activity at the receptor or at any
receptor in its paralog cluster**, and **≥1 measured activity elsewhere** (so the
molecule is a real ligand of something, not an untested compound).

Each clause needs a decision, and each is a place the extraction can go quietly
wrong:

| decision | proposal | why |
|---|---|---|
| **release** | Pin one ChEMBL release by version *and* download checksum, recorded in the manifest | ChEMBL is versioned and revised; an unpinned pull is `paper_af3`'s ColabFold problem in another costume |
| **activity types** | `Ki`, `Kd`, `IC50`, `EC50` only | `AC50`, `%inhibition`, `Potency` mix functional and binding readouts and have no common scale |
| **assay confidence** | `confidence_score >= 8` (direct single-protein target) | Below 8 the assay may target a complex or homologue, so "no activity here" becomes unverifiable |
| **what counts as ACTIVITY** | any qualifying record, whatever its value | A weak measured affinity is still evidence the molecule binds. Thresholding on potency would admit known weak binders as decoys |
| **what counts as ABSENCE** | no qualifying record at the receptor **or any cluster-mate** | Absence of evidence, and it must be stated as such — see the limitation below |
| **target mapping** | UniProt accession → ChEMBL target, single-protein only | Slug or gene-symbol matching collides across species; we already have three non-human receptors on the panel |
| **species** | record, never filter | Matches `PANEL.md` Rule R step 5, and a human-only filter would silently drop the turkey/bovine/spider entries |

## The limitation that must be stated, not hidden

**"No measured activity in ChEMBL" is absence of evidence, not evidence of
absence.** A decoy chosen this way may simply never have been assayed against that
receptor. This is inherent to the method and it is not fixable by a better query —
so it belongs in Methods as a stated limitation, and it is the strongest reason to
keep the **paralog-cluster** exclusion rather than the receptor-only one: a
molecule untested at the receptor but inactive across its whole cluster is a
better-evidenced decoy than one merely untested.

> **STATUS 2026-09-12 — deliverables 1 and 3 are BUILT; the pool is not, and that
> is deliberate.** `drule_targets.py` has resolved **63 of 64 receptors** to a
> ChEMBL SINGLE PROTEIN target against **ChEMBL_37 (2026-05-01)** —
> `inputs/drule_targets.tsv`, covering **31 of 32 clusters**. The one unresolved is
> **B1B1U5**, the jumping-spider opsin, which has no ChEMBL target at all; it is
> recorded with an empty target rather than dropped, because a receptor that
> vanishes from a pool looks exactly like one that had no decoys.
>
> `drule_pool.py` is written and its rule is **proved on a fixture** — a
> four-molecule world exercising every branch: active at the receptor, active at a
> cluster-mate only, active only elsewhere (the decoy case), and active only in a
> confidence-7 assay (not a candidate at all). `--selftest` runs it, 4/4.
>
> **It refuses to run against the live web API**, and that refusal is this
> document's own rule enforced in code: an unpinned pull is `paper_af3`'s ColabFold
> problem in another costume. It needs `--db` pointing at a downloaded release plus
> `--release` and `--sha256`, both recorded into every output row. **Downloading a
> ChEMBL release is a decision with a cost and it is Aditya's, not the script's.**
>
> `redo/gates/drule.py` gates what exists — 4 checks, each proved by planting — and
> **announces the unbuilt pool loudly on every run** rather than falling silent
> about it. D-5 and D-6, which check that no eligible candidate has activity at its
> receptor or a cluster-mate and that every row carries its provenance, activate
> the moment the pool appears.

## Deliverables, in order

1. `redo/build/drule_pool.py` — extraction. Writes
   `redo/inputs/drule_candidate_pool.tsv`, one row per (receptor, candidate) with
   every property axis and the provenance of each activity record consulted.
2. `redo/build/drule_select.py` — applies `CAMPAIGN.md` §5.3's eight axes and the
   similarity gate; writes the accepted decoys and, for every rejection, **which
   axis rejected it**. A rule that cannot say why it refused is not auditable.
3. `redo/gates/drule.py` — proved by planting a defect, per project rule. At
   minimum: no accepted decoy has a measured activity at its receptor or a
   cluster-mate; every accepted decoy passes every axis it claims to; the pool is
   reproducible from the pinned release.
4. **A pool report before any threshold is fixed.** How many clusters yield ≥3
   accepted decoys. Only then does the go/no-go threshold get pre-registered —
   D-D withdrew the ≥12 figure precisely because it was set before this number
   existed.

## What this does not decide

Whether the arm runs. That is D-D's gate, and the gate is downstream of the pool
report. **If fewer than ~10 of 15 clusters yield decoys, the honest outcome is to
report that a defensible decoy set cannot be built on this panel** — which is
itself a publishable answer to the nonbinder challenge, and a better one than an
arm built on molecules that fail their own stated criteria.
