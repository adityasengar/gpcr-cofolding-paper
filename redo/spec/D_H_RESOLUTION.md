# D-H — B1B1U5, 9EPP vs 9EPR: the evidence, and what is and is not resolvable

> ## CLOSED 2026-09-12. Aditya chose **(c′) for the primary panel, with (e′) as an extension arm.**
>
> Everything below §7 is the *reasoning*, kept as the record. §9 is what was
> implemented. **Sections 1–5 contain statements that were true when written and
> are now superseded** — chiefly the framing "three documents say 9EPR, the frozen
> artefact says 9EPP, therefore the artefact is wrong". §6 already overturned that
> and §7 replaced the option set. Superseded selection statements are marked
> `{ref-history}` so the `gates/panel_verify.py` cross-document check can tell a
> record from a claim.

**Status: CLOSED.** Written 2026-09-12 during the curation phase; decided the same
day. No compute involved.

D-H blocks B1B1U5's ligand curation, because its curated agonist row is keyed to
**9EPR** while the frozen cognate map is keyed to **9EPP** — so curating before
resolving would pin the ligand and the cognate reference to different structures
for the same receptor.

---

## 1. CORRECTED 2026-09-12 — the defect is narrower than I first wrote

My first version of this section said the frozen map carries 9EPP because "rule 3
ran and rule 4 never did". **That framing is wrong for this receptor**, and the
correction came from the lit session.

**What is verified.** `lit/panels/si_tables/lee2026confornets_gpcr_references.csv`
— ConfoRNets' own published benchmark file — carries:

```
B1B1U5,9EPP_R,6I9K_A
```

and **`9EPR` appears zero times in that benchmark**. Our `lit/panels/panels.csv`
rows for B1B1U5 carry `provenance=authors-repo`. So 9EPP is the published
benchmark's choice and **9EPR was never in contention there**.

**What the provenance chain actually shows.** `coupling_cognate_map.tsv`'s
`rule_r_active_pdb` ← `g1_receptors.tsv:active_pdb` ← **parsed from `PANEL.md`
§6.1's own rendered tier-C1 table**, whose row 16 reads `9EPP 4.06Å EM`.

**So the accurate statement is:** `PANEL.md` §6.1's table says **9EPP** while
`PANEL.md` §6's prose says Rule 4 should give **9EPR** and calls 9EPP wrong. **Our
own document contradicts itself, and the frozen artefact followed the table.**
Whether the table derived 9EPP independently or inherited it from ConfoRNets is not
determinable from the chain, and it does not need to be — the self-contradiction is
the defect either way.

**Rule 4 is still unimplemented** (no code anywhere applies a partner-chain
override), and that remains worth fixing or striking. But it is **not established**
as the cause here, and §6(b) below shows it is inapplicable to this case regardless.

**The more interesting finding, which is not about us at all:** *a published GPCR
benchmark uses a Gq-tipped chimeric complex as its active reference for this
receptor.*

## 1b. The original finding, as it stands

Rule 4 exists in `PANEL.md` §6 prose:

> **Partner-chain override.** Where the top-ranked entry's transducer chain is a
> chimera and an entry of the same receptor and state with a native transducer
> exists, take the native one and record the demotion.

Grepping the campaign tree for `9EPP` / `9EPR` returns three hits: two comments and
one gate `WAIT`. **No selection code applies the override.**

`PANEL.md` §6 states the reference-selection rule. Step 4 reads:

> **Partner-chain override.** Where the top-ranked entry's transducer chain is a
> chimera and an entry of the same receptor and state with a native transducer
> exists, take the native one and record the demotion.

`PANEL.md` then says why it exists, in terms:

> Rule 4 exists because rule 3 gets **B1B1U5** wrong without it: it promotes
> `9EPP` over our `9EPR` … 9EPP is a Gi/q chimera and 9EPR is the native Gi
> heterotrimer from the same deposition. {ref-history}

**Rule 4 appears nowhere in `redo/build/` or `redo/gates/`.** Grepping the whole
campaign tree for `9EPP` / `9EPR` returns three hits: two comments and one gate
`WAIT` message. No selection code applies the override.

So the frozen `coupling_cognate_map.tsv` carries `rule_r_active_pdb = 9EPP` — the
chimera — because **rule 3 ran and rule 4 never did.** `g1_preflight` already
records the consequence as a pending dependency: *"B1B1U5 follows Rule R to 9EPP;
if the panel session settles on 9EPR it flips to Gi1 and the map must be rebuilt."* {ref-history}

**Three documents say 9EPR; the frozen artefact says 9EPP.** That is D-H.

## 2. What 9EPP actually is, from our own frozen data

| field | value |
|---|---|
| `rule_r_active_pdb` | `9EPP` |
| `source_entity` | `9EPP_2` |
| `source_description` | "Guanine nucleotide-binding protein **G(i) subunit alpha-1**" |
| `source_uniprot_xref` | **P63096** (human *GNAI1*) |
| `ct21_nearest` | **G11/Gq** |
| `ct21_identity` | **0.86** |
| assigned `cognate_subtype` | **Gq** |
| `evidence_class` | `STRUCTURE_NEAR` |

The entity is **described and cross-referenced as Gi**, and its **α5 tip scores as
Gq**. That is the chimera signature, and it is why `PANEL_EXPANSION.md` §5a records
9EPP as "a Gi/q chimera (Gαi1 scaffold with a Gαq α5-CT graft)" whose UniProt
lookup would mis-assign coupling.

`deposited_ct21` = `FVFCAVKDTILQNNLKECNLV`, which differs from canonical Gq at
**three of 21 positions** (4, 13, 18) — hence 0.86, not 1.00.

## 3. A systematic check this exposed — and one non-finding

Rule 4 was written to be **general** and applied in prose to **one** receptor. So
the obvious question is whether other receptors carry a chimeric reference
silently. Scanning the whole frozen map for entities whose **description names one
Gα family and whose α5 tip scores as another**:

| receptor | ref | entity says | tip says | `ct21_identity` | tier | caught? |
|---|---|---|---|---:|---|---|
| **OXYR** | 7RYC | G(i)/G(s)/G… | G11/G14/Gq/Gs | 0.62 | EXTENSION-chimeric | **yes** — `CHIMERA_SPLIT` |
| **ACM1** | 6OIJ | G(i) α-1 | G11/Gq | **1.00** | EXTENSION-census | not flagged |
| **B1B1U5** | 9EPP | G(i) α-1 | G11/Gq | **0.86** | **PRIMARY** | not flagged |

**ACM1 is checked and NOT a finding.** Its `ct21_identity` is **1.00** — the
deposited 21-mer is an exact match to canonical Gq/11. The construct is a Gi
scaffold carrying a **native** Gq tip, and since the tip is what we score against,
`STRUCTURE_EXACT` is the correct classification. It is also EXTENSION-census tier,
outside the primary panel. Nothing to do.

**B1B1U5 is the only primary-panel receptor whose reference tip is neither native
nor flagged.**

## 4. What is resolved, and what is not

**Resolved — the documentary question.** Our own Rule 4, our own audit note, and
our own panel prose all say **9EPR**. The frozen map says 9EPP only because rule 4
was never implemented. Whatever else is decided, **the map and the documents must
stop disagreeing**, and the fix is either to implement rule 4 or to strike it.

**Not resolved — the scientific question**, and it does not follow from rule 4:

- Invertebrate visual opsins are **canonically Gq**, which supports the Gq
  assignment that 9EPP's tip produces.
- The experimenters built a **Gq-tipped** construct for this receptor, which is
  itself evidence they expected Gq engagement.
- But **9EPR, a native Gi heterotrimer, exists from the same deposition** — which
  is hard to explain if the receptor is simply Gq.
- And the 0.86 tip may be an **engineered graft** *or* a genuine **spider** Gq
  sequence differing from the human canon. Our data cannot distinguish these: the
  `source_uniprot_xref` describes the whole entity, which is mostly Gi scaffold.

## 5. Options

| option | consequence |
|---|---|
| **(a) Implement rule 4. Reference → 9EPR, cognate → Gi1.** | Consistent with three of our own documents. Rebuilds the cognate map for one receptor. Halves nothing — Gq keeps its other member. Contradicts the canonical invertebrate-opsin biology. |
| **(b) Keep 9EPP and Gq, strike rule 4, record the tip as engineered.** | Matches the biology and the deposited tip. But 0.86 means **rungs R1–R4 would be scored against a non-native tip** — the exact reason the other ten chimeras were excluded from the primary panel. |
| **(c) Split it, as we already split cognate.** `cognate_family = Gq` (biology, what we supply); `reference_tip = 9EPR` native (what we score against); record the mismatch explicitly. | Honest about both halves. Costs an explanatory sentence in Methods. |
| **(d) Move B1B1U5 to EXTENSION-chimeric-reference**, beside OXYR. | Most consistent treatment — it is the same defect OXYR has. Drops the primary panel to 29 receptors / 28 clusters and **Gq to n = 1**, which is what Aditya declined when he chose "resolve it". |

**Recommendation: (c).** It is the framework already adopted for exactly this
problem — the `cognate_family` / `reference_tip` split made on 2026-09-11 — and it
is the only option that does not either contradict our own rule or score a ladder
rung against an engineered sequence. **(a) is the fallback** if the literature says
the spider opsin is Gi.

**Whichever is chosen, rule 4 must be implemented or struck.** A selection rule
that exists only in prose has already produced one silent disagreement between our
documents and our frozen data, and it would produce more as the panel grows.

## 6. THE LITERATURE ANSWER — `tejero2024opsin`, and it changes the question

The lit session found the deposition paper (Nat Commun 2024, 15:8928). It answers
all three questions and **invalidates the framing of §4-§5 above.**

**(a) The tip is genuinely SPIDER Gq. Our 0.86 is species divergence, not
engineering.** Methods p10 records the construct: human Gαi1 with `A31R; D193S;
L194I` plus residues 337–354 swapped to the jumping-spider Gαq1 sequence
(acc. `LC799818`). The swapped segment is `CAVKDTILQNNLKECNLV`, and our
`deposited_ct21` is `FVF` + exactly that. **The three mismatches to human Gq —
positions 4, 13, 18 — all fall inside the spider-derived segment.** So the tip is
native *for the organism*; it is not a graft of a human Gq tip and not backbone
bleed-through.

**(b) 9EPP is nonetheless a chimera, and — decisively — 9EPR is not native
either.** 9EPR is human Gαi1 expressed in *E. coli*, mixed *in vitro* with
**bovine** Gβ1γ1 separated from retinal transducin. 9EPP carries human Gβ1γ2.

> **Rule 4 does not merely lack an implementation. It is inapplicable to the case
> it was written for.** "Prefer the native transducer over a chimera" presumes a
> native option exists. Here the choice is between a spider-Gq-tipped chimera on a
> human backbone and a human/bovine in-vitro reconstitution. **Neither is native,
> and the βγ differs between them** — which no UniProt cross-reference surfaces.

**(c) The paper never measures coupling.** It states the Gq chimera was built
because "the production of active and pure jsGq for structural studies was not
successful", designed *from* the JSR1–hGi structure — so **hGi is an enabling
tool, not a coupling claim** — and says outright that "further experiments will be
needed to determine the signaling profile of JSR1". Design intent is Gq; evidence
of coupling is absent.

**(d) The fact that actually decides it, for a panel whose predicate is a TM6
measure.** The paper reports that in the chimera complexes "the outward movement
of TM5 and TM6 is larger than in the hGi complex", and argues "the G protein
subtype determines the extent of the TM6 movement". **The two candidate references
sit at measurably different positions along the very axis our predicate measures.**
Choosing between them is not a bookkeeping choice about coupling annotation — it
moves the active reference along the activation axis itself. Both chimera models
are also "incomplete at the cytoplasmic end of TM6", at 4.06/4.15 Å against 9EPR's
4.9 Å.

**(e) Two corrections to our own inputs.**

- **GPCRdb annotates all three entries as `gnai1_human`, chimera included.** So a
  GPCRdb-derived coupling map calls all three Gi, and **neither our frozen Gq nor
  Rule 4's Gi is derivable from GPCRdb.** This is the accession-names-the-backbone
  problem propagating into the database itself.
- **`lee2026confornets` also selected 9EPP.** Our frozen artefact may be
  *inherited from the published benchmark* rather than an independent divergence
  from Rule 4 — which would make §1's framing ("rule 3 ran, rule 4 did not") only
  half the story. Worth confirming before it is written up as our defect.

**(f) Unresolvable from our corpus, and recorded as such.** Whether Gq coupling is
universal across arthropod or chelicerate opsins is **not** answerable here — one
of 83 notes covers invertebrate opsins at all. The claim "invertebrate visual
opsins are canonically Gq", which §4 leaned on, has **no locator** and must not be
used as evidence.

## 7. Revised options

Option (a) of §5 — "implement rule 4, take the native one" — **is void**: there is
no native option. What remains:

| option | consequence |
|---|---|
| **(c′) Split, as we already split cognate.** `cognate_family = Gq` — supported by the spider-Gq tip and the design intent; `reference_tip = 9EPP`, recorded as the spider-Gq-tipped chimera it is. State in Methods that no native complex exists for this receptor. | Honest about every part. Keeps 30/29. Still scores rungs against a tip that is native-for-spider but 0.86 to the human Gq we supply — **which is now the real question, and it is about what we SUPPLY, not which PDB we pick.** |
| **(d′) Move B1B1U5 to EXTENSION-chimeric-reference.** | Most consistent: it has the same defect as OXYR. Costs 29/28 and Gq at n = 1. |
| **(e′) Keep 9EPP but supply the SPIDER Gq α5 rather than human.** | The only option where supplied partner and scoring reference are the same molecule. Requires adding `LC799818` to the partner catalogue. Makes B1B1U5 a one-receptor species-matched arm, which is arguably its own small result. |

**Recommendation: (c′) for the primary panel, with (e′) offered as an extension
arm.** (e′) is genuinely attractive — it is the only self-consistent version — but
it introduces a non-human partner into a human-partner ladder, and that is Aditya's
call rather than a curation decision.

## 8. What would still settle more

One literature answer: **does the jumping-spider rhodopsin couple Gq or Gi?** If
the 9EPP deposition's own paper states the coupling, that settles it outright. This
is a `litquery` question for the lit session, not a compute question.

---

# 9. THE DECISION, AND WHAT WAS BUILT — 2026-09-12

**Aditya: (c′) for the primary panel, with (e′) offered as an extension arm.**

## 9.1 (c′), exactly as implemented

| field | value |
|---|---|
| tier | **PRIMARY** — the panel stays **30 receptors / 29 clusters**, unchanged |
| `cognate_family` | **Gq** (`Gq/11`, subtype `Gq`, accession `P50148`) |
| `reference_tip` | **9EPP**, recorded as a **spider-Gαq1-tipped chimera on a human Gαi1 backbone** |
| supplied partner, R1–R5 | **human Gq**, 0.86 identity to the reference tip at ct21 |
| Methods must state | **no native complex exists for this receptor.** 9EPP is a chimera; 9EPR is human Gαi1 from *E. coli* reconstituted *in vitro* with **bovine** Gβ1γ1. PANEL.md **Rule 4 is inapplicable**, not merely unimplemented — its second clause ("an entry … with a native transducer exists") is never satisfied |

The biology behind `cognate_family = Gq`: the deposited tip is genuinely spider
Gαq1, and the experimenters' design intent was Gq (§6a, §6c). It is **not** a
coupling measurement — `tejero2024opsin` states outright that "further experiments
will be needed to determine the signaling profile of JSR1" — and no sentence may
say otherwise.

## 9.2 (e′), costed — and where it stops

(e′) supplies the **spider** Gαq1 α5-CT instead of the human one, so that what we
supply and what we score against are the same molecule.

**The source, and its limit.** `tejero2024opsin` Methods p10 records the swapped
segment as human Gαi1 residues **337–354** replaced by jumping-spider Gαq1,
accession `LC799818`:

```
CAVKDTILQNNLKECNLV      18 residues
```

That is the whole of the spider sequence this project holds. **We do not hold
`LC799818` itself.** So (e′) is constructible at every rung of length ≤ 18 and at
no rung longer, and the ladder stops there rather than being padded:

| rung | needs | (e′) sequence | human Gq at the same rung | diff | status |
|---|---:|---|---|---:|---|
| `R1_ct11` | 11 | `LQNNLKECNLV` | `LQLNLKEYNLV` | 2 | **held** — and byte-identical to `ref_tip/reftip_ct11/9EPP`: the last 11 lie wholly inside the spider window, so at this rung (e′) *is* the deposited tip |
| `R1b_ct13` | 13 | `TILQNNLKECNLV` | `TILQLNLKEYNLV` | 2 | **held** |
| `R2_ct15` | 15 | `KDTILQNNLKECNLV` | `KDTILQLNLKEYNLV` | 2 | **held** |
| `R2b_ct17` | 17 | `AVKDTILQNNLKECNLV` | `AVKDTILQLNLKEYNLV` | 2 | **held** |
| *(ceiling)* `ct18` | 18 | `CAVKDTILQNNLKECNLV` | `AAVKDTILQLNLKEYNLV` | 3 | **held** — the whole recorded segment; not a ladder rung |
| `R2c_ct19` | 19 | — | — | — | **NOT SUPPORTED** |
| `R3_ct21` | 21 | — | — | — | **NOT SUPPORTED** |
| `R4_a5helix` | 26 | — | — | — | **NOT SUPPORTED** |
| `R5_a5plus` | 36 | — | — | — | **NOT SUPPORTED** |
| `R6a_da5`, `R7_full` | subunit | — | — | — | **NOT SUPPORTED** — LC799818 records a segment, not a subunit |

**Why ct21 in particular is not available, and why this is a trap rather than a
rounding error.** The deposited 21-mer is `FVFCAVKDTILQNNLKECNLV`. Its first three
residues are the **human Gαi1 backbone** (`P63096` 334–336 = `FVF`), not spider.
Supplying it as "the spider 21-mer" would be supplying the deposited chimera under
a wrong name — and the bytes would look right, because **human Gq reads `FVF` at
the aligned positions too** (`P50148` 339–341). The deposited 21-mer *is* held, as
`ref_tip/reftip_ct21/9EPP`, and it is the honest construct for a "supply what was
crystallised" arm; it is not an (e′) rung.

**Cost of (e′).** Construction: **zero** — the five held constructs are derived
from files already in `inputs/`, `spidertip_*` in `g1_partner_registry.tsv`, all
hash-checked. Compute: one receptor × the rungs actually run; it is a
one-receptor, species-matched arm, so it can only ever be a demonstration, never a
powered contrast. **What it would cost to reach ct21 and above: a sequence
request.** `LC799818` (INSDC) in full would lift the ceiling from 18 to the whole
subunit and is the single ask that unblocks the rest of the ladder — but it also
raises a question this work has not answered, namely whether the rest of spider
Gαq1 aligns to human Gq closely enough for a rung boundary defined on human CGN
`G.H5` to mean the same thing there.

**Why it is not in the primary ladder:** it introduces a non-human partner into a
human-partner ladder. That is a scope change, not a curation fix.

## 9.3 What changed, mechanically

| artefact | change |
|---|---|
| `spec/PANEL.md` §4 | Rule 4 **scoped** — its second clause made explicit and load-bearing; its old justification struck *in place*, with the three reasons it was wrong. Rule 4 stays on the books, still unimplemented in code, for the cases where it *can* fire |
| `spec/PANEL.md` §6 | new note: the QC flags say nothing about the transducer chain; the 12 receptors with a non-canonical α5 tip on the rule-R active reference are named, and a gate check holds the list to `g1_refchimera.tsv` |
| `spec/PANEL.md` §11 | the B1B1U5 bullet corrected: rule 3 selects 9EPP and rule 4 does not override it |
| `spec/PANEL.md` §6.1 table | **unchanged** — it already said `9EPP`, and under (c′) it was right |
| `build/coupling_cognate_map.py` | R-COG-9: the generic note no longer claims a *cause* ("deposited tip is engineered") for the 8 near-canonical tips; cause is recorded per (slug, pdb) only where a source settles it. B1B1U5's says species divergence, with its locator |
| `build/g1_panel_freeze.py` | DECISION 4; new columns `reference_tip_pdb`, `reference_tip_note`; a stale-key guard so a curated note cannot outlive the reference it describes |
| `build/g1_panel_freeze.py` | **separate finding, see §9.4** — `supplied_partner_independence` |
| `build/g1_partner_registry.py` | the (e′) constructs, five held and six not-dispatchable, each with its reason |
| `build/ligand_curation_candidates.py` | B1B1U5's note: D-H no longer blocks it (§9.5) |
| `gates/panel_verify.py` | two new cross-document checks (§9.6) |
| `gates/g1_preflight.py` | the "4 assignments reverse Block B's prior" WAIT now says B1B1U5's half is closed |

## 9.4 A second defect, found while implementing this

`g1_panel_freeze.tsv:supplied_partner_independence` read **"annotation only —
independent of the structure"** for **B1B1U5 and OPSD**. Both are false. Neither
receptor has *any* non-structure coupling authority: `coupling_assignments.csv`
gives both `n_authorities = 1`, and that one authority is `authority_structure` —
a reading of their own deposited structures. So for these two the "biology" column
and the "reference" column were the same evidence written twice, and the column
whose entire purpose is to keep them apart said they were independent.

Both are **PRIMARY-panel** receptors. The generator now tests the authority
columns directly rather than the count, and both rows say so.

This does not change (c′) — Gq for B1B1U5 rests on the spider tip and the design
intent, which is what §6 established, not on an annotation. It changes what the
row is allowed to claim.

## 9.5 B1B1U5's ligand curation — unblocked, but not finished

`LIGAND_CURATION_PROPOSAL.md` marked B1B1U5 blocked on D-H. **That block is
lifted**, and the picture is better than expected but not clear:

- **The reference question is settled.** 9EPP is the active reference, and its
  agonist row already carries `is_our_reference = yes`.
- **F-11's trap does not bite this pair.** 9EPP's agonist is **11,20-ethanoretinal,
  CCD `A1H6M`** — a *different CCD* from the 11-cis retinal (`RET`) inverse agonist
  on our inactive reference `6I9K`. The "one CCD, two opposite pharmacologies"
  hazard is an OPSD problem here, not a B1B1U5 one.
- **What is still open is policy, not chemistry.** The delivered
  `ligand_set_tier3.csv` carries B1B1U5's antagonist as a deliberate `NA` under
  amendment §C-1, which dropped `inverse_agonist` from Tier 3 — and 11-cis retinal
  is an inverse agonist, not a neutral antagonist. Curating it means reopening
  §C-1 for this receptor, which is Aditya's call.
- **And the existing curated agonist row now points at a non-reference.** It is
  all-*trans* retinal keyed to **`9EPR`**, which is no longer a panel structure.
  Two options, and they are not equivalent: re-key to 9EPP's `A1H6M`, which is
  reference-matched but a **non-natural locked analogue**; or keep all-*trans*
  retinal and record that its `bound_pdb` is off-reference. Note F-11(b) —
  GPCRdb's isomer name for 9EPR is wrong, the modelled chromophore is all-*trans* —
  so the existing row is chemically right about 9EPR even though 9EPR is gone.
  **Not decided here.**

## 9.6 The two checks added

Both in `gates/panel_verify.py`, both proved by planting the defect they catch:

1. **the spider segment is derivable from RCSB alone.** Applying `9EPP_2`'s own
   `pdbx_mutation` record to human Gαi1 337–354 must reproduce
   `CAVKDTILQNNLKECNLV` exactly, and the three residues before it must be human
   backbone. This makes §6(a) checkable without the paper.
2. **no spec document asserts a reference that contradicts PANEL.md §6.1.** Any
   line in `redo/spec/*.md` that uses a selection verb near a receptor slug and a
   PDB id of that receptor must name the §6.1 pick, unless the line is marked
   `{ref-history}`. This is the check that would have caught D-H on the day it was
   created; the marker is deliberately visible and greppable so that "record the
   history" cannot quietly become "assert the alternative".

## 9.7 What still made me doubt the decision

Recorded because §6(d) is not disposed of by (c′): the paper reports that TM5/TM6
open **further** in the chimera complexes than in the hGi complex, and argues the
Gα subtype sets the extent of TM6 movement. Our predicate measures that axis. So
choosing 9EPP over 9EPR moves the active reference along the activation axis
itself, and it moves it in the direction that makes "active" easier to reach.
Both chimera models are also **incomplete at the cytoplasmic end of TM6**, at
4.06 Å against 9EPR's 4.9 Å. Neither fact argues for 9EPR — 9EPR has its own
problems and is not native — but they mean **B1B1U5's reference geometry is the
least trustworthy in the primary panel**, and a per-receptor sensitivity check
belongs in the measurement pass rather than a footnote.
