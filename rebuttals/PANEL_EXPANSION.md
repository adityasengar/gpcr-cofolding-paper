# Panel expansion — receptors with both states solved that we do not have

For the pipeline agent. Compiled 2026-09-10 by the orchestrator from the lit
session's `lit/panels/` extraction, with every claim about *our* data verified
here against `data/block_a/` and `data/block_b/`.

**Provenance labelling matters in this document.** Entries marked **PAPER** come
from a published benchmark's own released table. Entries marked **GPCRDB** come
from a cached database snapshot and are a lead to chase, not a corpus finding.
Nothing here is from general knowledge; a fabricated receptor list would be
acted on.

---

## 1. The headline: the panel is a subset, not a census

| source | both-state receptors | our panel |
|---|---:|---:|
| `lee2026confornets` released benchmark (**PAPER**) | 51 pairs | we hold 29 of them |
| GPCRdb snapshot, 1,716 entries (**GPCRDB**) | 86 receptors, 80 human | 40 |

`lee2026confornets` counted **51** both-state receptors under a rule *stricter*
than ours — they additionally require at most one engineered mutation per
structure. A referee can find that number, so **no sentence may say we took
every receptor with both states**. The honest framing is *40 of roughly 80 human
both-state receptors*, which is about half the available universe and the
second-largest both-states GPCR panel in this literature.

Context worth keeping, because it runs in our favour: only **257** GPCRs have
any deposited structure at all (229 human), and only **86** have both states.
Our 40 is ~50% of the human ceiling, not 5% of 800.

## 2. A selection rule we could cite instead of inventing one

The only stated both-states panel rule in the 79-paper corpus, and the only rule
anywhere in it that filters on **construct quality** —
`lee2026confornets` p.15, App. D.1, verbatim:

> "The GPCR benchmark was constructed from the GPCRdb structure database (Munk
> et al., 2016). We selected GPCRs with both fully active (100% activation
> degree) and inactive structures available. We selected pairs with the fewest
> engineered mutations and highest crystallographic resolution, retaining 51
> pairs where both structures contained at most one mutation."

Given how many active GPCR structures are BRIL/T4L fusions or thermostabilised,
adopting or citing this would strengthen us. **One caveat that must travel with
it:** its state label comes from GPCRdb's activation-degree annotation, which is
circular if the same annotation is also what you are predicting.

For contrast: `heo2022multistate` states no rule — its 15 both-state receptors
fall out of a date filter. `chiesa2025templatebias` is 145/145 **active** with no
inactive arm at all, and `zhang2026generalization` is 225 active / 28 inactive.

## 3. The 21 receptors to add — PAPER-sourced, with PDB pairs

From `lee2026confornets`' released benchmark (`assets/gpcr/references.csv`),
verified against GPCRdb on all 51 rows. Resolutions active/inactive in Å.

| receptor | active | inactive | res | | receptor | active | inactive | res |
|---|---|---|---|---|---|---|---|---|
| 5HT2A | 8UWL | 7WC7 | 2.8 / 2.6 | | MTR1A | 7VGY | 6ME2 | 3.1 / 2.8 |
| ACM3 | 8E9Z | 4U15 | 2.69 / 2.8 | | NK1R | 8U26 | 6E59 | 2.5 / 3.4 |
| ADA1A | 8THK | 8HN1 | 2.6 / 2.9 | | NTR1 | 8FN1 | 7UL2 | 2.88 / 2.4 |
| AGRE5 | 8IKL | 8IKJ | 2.33 / 3.2 | | OPRM | 8E0G | 7UL4 | 2.1 / 2.8 |
| CALRL | 6UVA | 7KNT | 2.3 / 3.15 | | OXYR | 7RYC | 6TPK | 2.9 / 3.2 |
| CCR2 | 7XA3 | 6GPX | 2.9 / 2.7 | | PD2R2 | 8XXV | 7M8W | 2.33 / 2.61 |
| CCR6 | 6WWZ | 9D3G | 3.34 / 3.26 | | S1PR5 | 7EW1 | 7YXA | 3.4 / 2.2 |
| CCR8 | 8XML | 8TLM | 2.58 / 2.9 | | SSR2 | 7T10 | 7XN9 | 2.5 / 2.6 |
| CXCR3 | 8HNM | 8K2W | 2.94 / 3.0 | | TSHR | 7UTZ | 7T9M | 2.4 / 3.1 |
| DRD4 | 8IRU | 5WIU | 3.2 / 1.96 | | | | | |
| GPR6 | 8TYW | 8T1V | 3.43 / 2.6 | | | | | |
| HRH2 | 8YN3 | 7UL3 | 2.56 / 3.0 | | | | | |

**Two of these are cross-species pairs and lee's paper does not say so.**
**ACM3** is human 8E9Z active against **rat** 4U15 inactive; **NTR1** is **rat**
8FN1 active against human 7UL2 inactive. Take them only if a cross-species
contrast is acceptable, and if taken, say so.

`heo2022multistate` Table S2 names 8 further both-state receptors we lack, but
that table gives per-state **counts**, not PDB IDs — receptors without
references.

## 4. Thirteen more, GPCRDB-only — a lead, not a finding

Named by no paper in the corpus: AGRL3, C5AR1, GLR, GP156, GPR52, GRM3, GRM4,
GRM5, MTR1B, O52E4, S1PR1, T2R14, TA2R. Several are class C, so they would
extend scope rather than deepen it. **Total both-state receptors we lack: 38**
(25 named by a paper, 13 database-only).

---

## 5. Two problems in the panel we already have

Both verified here against our own reference audit.

### 5a. B1B1U5 is not a human receptor

`b1b1u5_9arac` is an opsin from *Hasarius adansoni*, a jumping spider — the only
non-human entry among the 40. Class A is correct; **any sentence describing the
panel as human receptors is wrong as written.** lee's benchmark carries the same
entry under the same accession-as-name, so it is a shared blind spot rather than
ours alone.

**Where we are ahead:** lee uses **9EPP** as its active reference. We use
**9EPR**, and our own audit note records why — 9EPP is a Gi/q chimera (Gαi1
scaffold with a Gαq α5-CT graft) that would mis-assign coupling through a UniProt
lookup, and 9EPR is the native Gi heterotrimer from the same deposition. That is
a better choice than the published benchmark's and it is worth saying so.

### 5b. OPSD's reference pair is probably cross-species

GPCRdb holds four human rhodopsin structures and annotates **all four as
active**; every classic dark-state rhodopsin — 1F88, 2I37, 3C9M, 6OFJ — is
**bovine**. Our pair is 4X1H active / 7ZBC inactive, and nothing in the drop
records species for either. So the pair is either human-active against
bovine-inactive, or silently all-bovine.

This is also why the lit session's audit finds **39** of our 40 with both states
in GPCRdb where our own reference audit says 40/40. Resolving it resolves both.

**To close:** the species of 4X1H and 7ZBC, and whether the cross-species pairing
was deliberate. `reference_audit.csv` has no species column; it should.

---

## 6. Something already in our reference set that nobody has used — and an
## annotation defect found while checking it

**4X1H, our OPSD active reference, is a receptor bound to a Gα<sub>t</sub>
C-terminal peptide alone — no full Gα subunit.** X-ray, 2.29 Å, deposited
2014-11-24, released 2015-11-04. Our instrument calls it **active**: TM6 tilt
17.586 Å against a 14.932 Å threshold, NPxxY 4.921 Å against 9.08 Å. Both fire.
It is the only peptide-bound entry in the whole reference set — checked, one of
80 — an experimental structure in which an isolated α5-CT-derived peptide holds a
receptor open, sitting unremarked inside our own data.

**But the annotation shipped with it is wrong, and that is the actionable half of
this section.** `reference_audit.csv` calls it *"native α5-CT donor class Gt"*.
Checked against RCSB and UniProt on 2026-09-10:

| | sequence | length |
|---|---|---:|
| 4X1H chain C | `VLEDLKSCGLF` | **11** |
| native bovine Gα<sub>t</sub>1 (UniProt P04695) C-terminus | `IKENLKDCGLF` | 11 |

Four of eleven positions differ (I→V, K→L, N→D, D→S). It is an engineered
high-affinity analogue, **not the native α5-CT and not a 21-mer**. RCSB names the
entity a *"C-terminal **derived** peptide"*; the deposition never claimed
otherwise. The entry is also **opsin** — title *"Opsin/G(alpha) peptide complex
stabilized by nonyl-glucoside"* — so the receptor is ligand-free, which
`activation_class = Ga-complexed-native` does not convey.

**Neither of our audits could have caught this.** The construct audit behind
C-11 compares `construct` against RCSB `pdbx_mutation` on the **receptor**
entity, so a partner-chain substitution is out of scope by construction. And
RCSB reports `pdbx_mutation_count = 0` for the peptide entity, because it is
deposited as its own derived-peptide entity rather than as a mutant — so running
the audit there would have returned **clean**. The drop already says the bin is
unverified: `ASSUMED_NOT_VERIFIED_E.md` records that *"the distinction between
wild-type Gαs and DNGαs is not captured in the current schema; a fresh dispatch
would need to inspect construct strings PDB-by-PDB."*

### What this changes

1. **4X1H is not citable as precedent for a wild-type 21-mer.** An engineered
   11-mer holding opsin open is a real result and a fair motivating observation,
   but it is not the title claim, and a structural referee will pull the sequence
   exactly as this check did.
2. **It strengthens the anti-memorization case, which is the part worth keeping.**
   No wild-type 21-mer α5-CT appears with a receptor in any deposited structure;
   the isolated-peptide precedent is exclusively short, engineered, pre-cutoff
   opsin entries. A wild-type 21-mer is therefore not a sequence the models have
   seen in this context — a quantitative argument, and ours to make.
3. **OPSD is still where to start a 21-mer arm** (suggestion S2), but 4X1H is
   that arm's *motivation*, not its scoring reference. Scoring a 21-mer prediction
   against an 11-mer-analogue structure is an interface mismatch of the same class
   already recorded for 6E67 — right state, wrong register, and no metric we have
   catches it.

### Requests

1. **Re-derive `active_stabilization_source` from partner sequence, not from
   composition.** 25 of the 40 active references carry `native`, and no partner
   chain behind any of them has been compared to UniProt. The other 24 are
   probably fine — for them `native` denotes a full heterotrimer, which
   `G2_REFERENCE_HOMOGENEITY.md` verifies from deposition titles for twelve — but
   "probably" is what this campaign keeps having to retract.
2. **Add a partner-chain sequence check to the reference audit.** Nothing in this
   project currently checks the sequence of any non-receptor chain, and the α5-CT
   donor is the one chain the title is about.
3. **Add `species`, `method`, `resolution` and `release_date` columns** (see §5b
   and item 4 of the Class A list). `method` is the same placeholder string on all
   80 rows, `resolution` is entirely NaN, and release date is absent — so neither
   construct quality nor a training-cutoff argument can be checked from the drop
   as shipped.
4. **If the 21-mer arm is scheduled, start it on OPSD** — as motivation, with a
   predicted rather than a deposited reference.
