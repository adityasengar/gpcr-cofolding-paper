# D-H — B1B1U5, 9EPP vs 9EPR: the evidence, and what is and is not resolvable

**Status: the documentary half is resolved. The scientific half needs Aditya.**
Written 2026-09-12 during the curation phase. No compute involved.

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
> heterotrimer from the same deposition.

**Rule 4 appears nowhere in `redo/build/` or `redo/gates/`.** Grepping the whole
campaign tree for `9EPP` / `9EPR` returns three hits: two comments and one gate
`WAIT` message. No selection code applies the override.

So the frozen `coupling_cognate_map.tsv` carries `rule_r_active_pdb = 9EPP` — the
chimera — because **rule 3 ran and rule 4 never did.** `g1_preflight` already
records the consequence as a pending dependency: *"B1B1U5 follows Rule R to 9EPP;
if the panel session settles on 9EPR it flips to Gi1 and the map must be rebuilt."*

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
