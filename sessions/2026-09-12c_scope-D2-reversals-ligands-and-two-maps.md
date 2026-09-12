# 2026-09-12c — the scope closes, and four gate WAITs become checks

Orchestrator session, continuing after the wrap. Curation only: no inference, no
GPU, no ask to `paper_af3` — Aditya's instruction was to work independently of that
client and sort its asks later.

**The theme of this session is that a dependency someone wrote down is not a check.**
Four standing WAITs were converted into guards, and three of the four found something
the WAIT had not said.

## What happened

| | |
|---|---|
| **scope** | **Class A only** — D-2026-09-12-d. Costs the primary campaign nothing; closes three items |
| **D2** | **RESOLVED at (c)** — D-2026-09-12-e, with two corrections to the option it was chosen from |
| **the three coupling reversals** | **CLOSED** — F-14, on stronger grounds than the existing basis |
| **D-C's ligand picks** | **ENACTED** — F-15, six of seven; ADRB1 turns out to be blocked |
| **the costing gap** | **CLOSED** — B18; the WAIT named two arms, the check found twelve |
| **the decoy rule** | DRULE deliverables **1 and 3 built and proved**; the pool waits on a pinned release |
| **two maps** | written: the frozen campaign end to end, and what the redo runs |

Gates went from **12 pass / 9 wait** and **16 / 7** to **13 / 8** and **18 / 5**, plus
a new ligand gate of 5. Seven commits, all pushed, tree clean.

## Decisions Aditya made, with their reasons

**The redo claims Class A only.** Asked directly and answered directly. The grounds
are measured rather than economic: F-13's apo arm found a **9 Å inter-backbone
disagreement** on Class B and **no discriminating power at all** on Class F (medians
14.20–16.12 straddling the 14.932 cut on every backbone). A paper that says "we
restrict to Class A because our instrument demonstrably does not transfer, and here
is the measurement" is stronger than one reporting B and F rates it cannot defend.

**D2 at option (c), the split.** Expand onto the actives-rich expansion receptors,
reserve the inactive-rich ones.

**Work independently of `paper_af3`.** Their asks get sorted later; nothing this
session waits on them.

## What the verification found

**The scope decision costs the primary campaign nothing.** Checked rather than
assumed: `g1_receptors.tsv` is 64 receptors, every one `gclass = A`, and
`g0_calibration_structures.csv` is 1,357 rows with exactly one class present. Both
populations were already Class A by construction. What the decision buys is a
*claimed* scope and three closed items — `E0.5`, the class F atom-pair WAIT, and the
Class B / Class F instrument decisions.

**The cost is `E7.2`**, the class B length ladder, and it is real:
`hilger2020gcgr` has agonist alone producing *no* TM6 opening in class B, which makes
it the sharpest venue for a length ladder, and lit rated cross-class transfer OPEN.
Parked with a banner in `CATALOGUE.md` rather than deleted.

**D2's option text was wrong in two ways.** The expansion set is **25 receptors, not
the 32 asserted in three places** (20 survive to F4); and the recommended reserve list
was ranked on the raw pool — on F4, **`ntr1` and `pd2r2` contribute zero inactives**,
so reserving them buys nothing. More important, the option implied a free split and
there isn't one: **all 17 expansion receptors carrying an F4 inactive are also
both-state receptors, and all 17 both-state receptors in the pool are expansion
receptors.** Non-expansion contributes zero. The cut taken — `cxcr3`, `mtr1a`,
`mtr1b` — is the only one that costs calibration nothing: 8 actives of 372, inactives
and both-state pairs untouched.

**The three coupling reversals close on better grounds (F-14).** Enumerating the Gα
in *every* active structure, not just the chosen reference: in CCKAR, EDNRB and GHSR
alike, **the family the Rule-R structure reads is the only family with a native,
full-length, non-engineered Gα anywhere**. Block B's Gq prior exists for all three
only as an mGsqi chimera, a mini-G, or a subunit the depositors themselves label
*engineered*. So it was never structure-versus-four-authorities; it is what a
receptor couples to in an assay versus what anyone has managed to deposit it bound
to — the same shape as the Block C "cognate disagreements" that sat in a secondary
column.

**The costing WAIT understated the gap by a factor of six.** It named E1.8 and E1.9.
A check that actually compares `g1_systems.csv` against `matrix_cost.py` found
**twelve** uncosted arms, including four — `G1c-opt`, `G1e`, `G1f`, `G10b` — listed
nowhere at all.

## What I got wrong and corrected

1. **G0's self-test was dead, and I had been claiming the opposite in three
   documents.** `_clone` copied only the **top-level** files of `redo/`, which was
   right while `redo/` was flat and silently wrong from the 2026-09-11 migration to
   the guarded layout onward. Every plant failed to *apply*, every check reported
   MISS, and the harness still printed a tidy tally. **0 of 11 were being proved**
   while `CLAUDE.md`, `HANDOVER.md` and a session log all said "every check was
   proved by planting the defect it catches." Now recursive: **12/12 fire.**
   `g1_preflight`'s harness uses a different mechanism and was never affected.
2. **My first Gα classifier called four engineered constructs native.** It tested
   only the entity *description*. `9BKK`'s description says "G(s) subunit alpha
   isoforms XLas"; its **title** says "Gq chimera (mGsqi)". Three mini-G entries of
   246–261 residues carry no engineering word anywhere. **Length was the
   discriminator I had left out.** It now tests description **and** title, family
   mixing, and length against the canonical value read from `seq_constructs.tsv`.
3. **I recorded carazolol as a neutral antagonist and it is an inverse agonist.**
   GPCRdb types it `Inverse agonist`, and amendment **C-1 dropped `inverse_agonist`
   from Tier 3** — which is exactly what blocks B1B1U5. So **ADRB1 is blocked too**,
   and `LIGAND_CURATION_PROPOSAL.md` was wrong to list it among the straightforward
   picks. Every ADRB1 candidate GPCRdb calls a true `Antagonist` is *Meleagris
   gallopavo*, against the standing rule that species follows the panel. A guard
   caught this, not a re-reading.
4. **B18 first read a variable named `rows` that is not the systems table**, so it
   passed on the wrong data and its plant did not fire; and its first id matcher
   treated `"G1a/G1b"` as one unknown id. Both caught by the plant refusing to fire.
5. **A near-miss worth recording: I used `git add -u`.** It has the same failure mode
   as `git add -A` — it stages every tracked modification, including another
   session's. Nothing was swept because no other session had edits in flight. That
   was luck, not discipline. **Explicit paths, always.**

## The decoy rule — built, and deliberately not run

`drule_targets.py` resolves **63 of 64 receptors** to a ChEMBL SINGLE PROTEIN
target against **ChEMBL_37 (2026-05-01)**, covering **31 of 32 clusters**. The one
unresolved is **B1B1U5**, the jumping-spider opsin, which has no ChEMBL target at
all — recorded with an empty target rather than dropped, because a receptor that
vanishes from a pool looks exactly like one that had no decoys.

`drule_pool.py` implements the absence rule and is **proved on a fixture**: a
four-molecule world exercising every branch — active at the receptor, at a
cluster-mate only, only elsewhere (the decoy case), and only in a confidence-7
assay, which must not be a candidate at all. 4/4.

**It refuses to run against the live web API, and that refusal is the spec's own
rule enforced in code.** `DRULE_CHEMBL_SCOPE.md` says an unpinned pull is
`paper_af3`'s ColabFold problem in another costume; building the pool off the API
would have reproduced exactly the defect the document warns about. It needs a
downloaded release with `--release` and `--sha256` written into every row, and
**that download is Aditya's decision, not the script's.**

`redo/gates/drule.py` gates what exists and **announces the unbuilt pool on every
run**. That is the distinction the project's missing-input rule turns on: a
deliverable not yet produced is reported loudly; an input that has disappeared is a
failure. Reporting the first one *silently* is the thing that is forbidden.

## A correction that arrived on the bridge, after the work above

`paper_af3` verified three of our apo-arm findings against their own tables. **Two
confirm exactly; the third does not survive.**

**Confirmed — the Class B backbone split**, to the decimal: boltz 12.38 (1 of 4
above the cut), protenix 12.53 (1/4), chai 21.47 (3/4), of3 19.60 (4/4). And the
control holds: Class A apo is well-behaved on all four (12.12 / 11.94 / 12.78 /
12.36, with 6 / 3 / 15 / 3 of 40 above), so the 9 Å split is not a generic
threshold artefact.

**Confirmed — the Class F threshold sits inside the apo distribution** (chai 14.20,
boltz 15.09, protenix 16.10, of3 16.12, against a 14.932 cut). They add that their
own brief already carries a standing rule that Class B/F thresholds are
`descriptive_n_lt_5_per_side` and must never be quoted as active-call fractions.
Our measurement is evidence for a constraint they had already written down.

**Retracted — "SMO gets less open when the partner is added".** That was **OF3
only**, stated as a receptor property. Recomputed here from the two state-call
tables we hold: SMO is **+0.22 / +0.04 / −2.14 / +0.19** across boltz / chai / of3 /
protenix — *slightly positive on three of four*. FZD7's negative is −0.07 on OF3
alone, which is noise. **It is the same pooling-across-disagreeing-backbones error
I had flagged for Class B one paragraph earlier**, which is what makes it worth
recording rather than quietly fixing.

**The conclusion survives and is stronger**: Class F deltas span **−2.14 to +2.41
with inconsistent sign across backbones**, which does not depend on any single
receptor or backbone. **The Class A-only scope decision is unaffected** — its
grounds are the two confirmed findings, not this one.

**And one thing neither of us had noticed: `FZD4` is absent from the cognate table
entirely** on all four backbones, while present in the apo table on all four. The
Class F cognate/apo contrast rests on **three receptors, not four**.

## What the next session should not redo

- **Do not re-open the scope, D2, D-A or D-H.** All four are decided with reasons in
  `DECISIONS.md`. `G0-13` guards the scope; `B17` guards the reversals.
- **Do not re-derive the coupling reversals from annotation authorities.** That
  framing is what kept them open. The evidence is structural and it is in
  `inputs/coupling_reversal_evidence.tsv`.
- **Do not chase affinity for the ligand picks.** Dissolved; the picks are enacted.
- **Do not regenerate the D2 population yet.** It changes `on_panel48` and therefore
  the frozen constants in G0-2, G0-5 and G0-7. Held deliberately so the population
  freezes once, as part of the measurement pass.
- **Do not start the measurement pass without Aditya's word.** It is still the
  largest outstanding dependency, and it must record axis values for the F3-**removed**
  structures too (F-12).
- **Do not restate "SMO goes backwards".** Retracted; it is OF3-only. The Class F
  claim that survives is the inconsistent sign across backbones.
- **Do not build the decoy pool off the ChEMBL web API.** The script refuses, and
  that refusal is deliberate. It needs a pinned download.
- **Amendment C-1 is the open question worth his time**: reopening it unblocks both
  ADRB1 and B1B1U5, taking the ligand arm from 6 picks to 8 and k from 12 to 14.
