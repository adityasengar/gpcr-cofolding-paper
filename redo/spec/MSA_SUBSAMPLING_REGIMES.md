# MSA_SUBSAMPLING_REGIMES.md — which subsampling regime to deploy

**Status: a PROPOSAL, not a decision.** It answers one question Aditya asked —
(a) subsample the receptor MSA, (b) receptor + G-protein partner, or (c) receptor +
partner in the presence of a ligand — with a recommendation and the reasons for it.
Nothing here is committed; nothing in `redo/inputs/` was edited; no compute was
commissioned; no git was run.

**Written 2026-09-12** by the orchestrator's subagent, standing on
`redo/spec/MSA_SUBSAMPLING.md` (the 1,162-line standing analysis, which this does
not duplicate), `redo/protocol/MAP_MSA.md`, `redo/spec/MSA_SPEC.md`,
`redo/spec/CATALOGUE.md`, `redo/spec/RUN_MATRIX.md`, and direct reads of
`redo/inputs/g1_systems.csv`, `redo/inputs/g2_systems.csv`,
`redo/inputs/g1_recording_spec.tsv`, `redo/gates/g1_preflight.py` and
`redo/build/matrix_cost.py`.

Corpus evidence is first-hand from
**`lit/analysis_review/MSA_SUBSAMPLING_REGIMES_ANSWERS.md`** (lit-3d, 2026-09-12,
83 notes, staleness clean), answering six questions sent for this document. Lit
retrieved; the reasoning here is mine. §10 records what that answer changed.

> ### ⚠ A standing document carries a claim lit has now corrected
>
> **`redo/spec/MSA_SUBSAMPLING.md` §5.2(b) states "no Neff figure exists anywhere in
> the corpus." That is wrong** and lit withdrew it on 2026-09-12. Neff appears in
> **two** papers — `abramson2024af3` Extended Data Fig 7A p.18 (median per-residue
> Neff, log axis 10⁰–10⁴) and `suzuki2026pairscaling` Fig 7 p.10. **The claim that
> survives is narrower and is still the one we want: no paper reports a *subsampling
> depth* in Neff units — Neff appears only as a descriptive property of natural
> alignments, never as a manipulated variable.** Flagged here for the owner of that
> file; not edited by me. §3.3 uses the corrected form.

Path roots follow `MAP_MSA.md`: `B/` = `redo/protocol/received/source_bundle/`,
`R/` = `redo/protocol/received/`.

---

## 0. The recommendation in seven lines

1. **Deploy (a) — receptor-only depth — and deploy it in two stages.** Stage 1 is
   apo, no partner, no ligand. Stage 2 crosses it with the partner rung.
2. **Do not deploy (b) as stated. It is not a regime; it is G17.** Every two-chain
   row we have enumerated already runs the partner MSA **off**, which is depth 1.
   You cannot subsample a query-only alignment. Aditya's reading is correct and
   §1 is the verification.
3. **(c) is not premature, but it is third**, and G5a already contains it. Its cost
   is the whole cube; its claim is an interaction whose MDE at k=17 is 0.295.
4. **Stage 1 of (a) is the only one deployable on four backbones today.** It is a
   monomer, so it never touches the per-chain MSA mapping. Stage 2 and (c) both do,
   and that mapping fails in **opposite directions** on OF3 and Protenix with no
   error on either. §2.
5. **Four depth levels, not three, and not the three proposed: `{1, 8, 32,
   default}`.** Drop 128 and 512 (Block D says nothing turns there); **add depth 1**,
   because the literature puts the floor at zero evolutionary information and says
   AF3-lineage models tolerate more aggressive manipulation than AF2 — so our
   ladder's shallow end may be truncated, not saturated. §3.
6. **Twelve recorded columns, two of which decide the paper's claim** and neither of
   which is in the 47 the recording spec carries today. §4.
7. **Our primary design already does something no paper in 83 has done** — run one
   chain of a complex at single-sequence. That makes G17 mandatory, not optional. §1.4.

---

## 1. Regime (b) is already at the floor — verified, and the framing is wrong

**This is the finding that reorganises the question, so it goes first.**

`redo/inputs/g1_systems.csv`, 2,039 rows, read directly (not edited):

| `partner_msa` | rows | `n_chains` breakdown |
|---|---:|---|
| `off` | **1,855** | 1,825 two-chain, 30 three-chain |
| `n/a` | 94 | all 94 are `n_chains = 1` (apo monomers) |
| `ON` | **90** | all two-chain — and **all 90 are item `G17(proposed)`, arm `partner_msa_on`** |

`receptor_msa` has **exactly one distinct value across all 2,039 rows**:
`"on (default)"`. `ligand` has exactly one: `"none"`.

`redo/inputs/g2_systems.csv`, the ligand group added 2026-09-12, 350 rows, agrees:
`partner_msa` is `n/a` (143, monomer) or `off` (207); `receptor_msa` is
`"on (default)"` on all 350.

And the gate asserts it. `redo/gates/g1_preflight.py:157-168`:

```
B7  every row declares a partner-MSA and receptor-MSA condition
      fails if partner_msa ∉ {off, ON, n/a} OR receptor_msa != "on (default)"
B8  MSA-free on the partner chain is the primary condition
      fails unless count(off) > count(ON) among rows with n_chains != 1
```

**So: confirmed.** Every enumerated two-chain row runs the partner at MSA-off —
which `MSA_SPEC.md` §3 defines as an explicit query-only alignment, depth 1, at
every rung, on all four backbones. Regime (b) as literally stated — *subsample the
partner's MSA* — asks us to reduce the depth of an alignment that the design has
already pinned to its floor. It is a no-op.

### 1.1 Three reasons not to fix that by turning the partner MSA back on

**(i) Partner depth is collinear with the factor we are measuring.** From
`R/rung_msa_depth.csv`, recomputed in `MSA_SUBSAMPLING.md` §2 (body counted, not
quoted from the spec):

| rung | length | partner unpaired depth |
|---|---:|---|
| `R1_ct11` | 11 | **0 in 16 of 16 Gα families** |
| `R2_ct15` | 15 | **0 in 5 families; ≤42 in 10 more; Gs = 459** |
| `R3_ct21` | 21 | 47–582 |
| `R7_full` | 350–394 | 6,289–9,203 |

A partner-depth ladder cannot be set independently of the rung. At `R1_ct11` the
target is **unreachable on every family** — and `B/scripts/subsample_msa.py:106-107`
returns the input unchanged when it is shorter than the target while the manifest
still records the target label. A "partner depth 8" arm at ct11 is a depth-0 arm
wearing a depth-8 label, on 16 of 16 families, silently. `MSA_SPEC.md` §2 exists
precisely to remove this confound: *"a monotone trend along that ladder is what a
pairing artefact looks like."* Regime (b) reinstates it.

**(ii) The binary version of the question is better posed and already costed.**
`CATALOGUE.md:784-806` (E1.9) asks exactly what (b) is reaching for — *"Does the
partner's effect survive when the model has no alignment for it? If the effect
survives MSA-free, it is steric or structural; if it collapses, it is
co-evolutionary."* Two levels, not five. It is enumerated (the 90 `ON` rows),
costed (`RUN_MATRIX.md:778-779`: G17a pooled **3,600**, G17b per-cell 18,000), and
`MSA_SPEC.md:198` already calls it *"wanted anyway… it answers 'how much did we
change by doing that?', which is the first question a referee asks."*

**(iii) It is the arm that bounds the cost of our own primary design.**
`MAP_MSA.md:616-639` and `MSA_SUBSAMPLING.md` §6.4: at `R7_full`, query-only runs a
complete Gα with a crippled alignment, removing the coevolutionary pairing from the
arm that carries the headline. G17 is the only thing that measures what that cost
was. A five-level partner-depth ladder answers the same question with ~5× the
predictions and a confound attached.

### 1.2 What to do instead

Replace (b) with **receptor depth × partner-MSA {off, on}** — G17's binary factor,
crossed with (a) rather than run beside it, on the two rungs E1.9 names (`R3_ct21`
and `R7_full`). That is cheaper than (b), interpretable at every rung, and it is a
factor the corpus does not occupy (`CATALOGUE.md:1660`: *"Nobody asks it of a
protein partner."*).

### 1.3 One naming defect found on the way

`g1_systems.csv` labels the primary condition **`off`**. `MSA_SPEC.md` §3–§4
specifies it as **query-only, depth 1**, and §4 spends a page arguing that *absent*
and *query-only* are **not** equivalent on Boltz/OF3/Protenix — an omitted alignment
may trigger a live fetch at full depth, *"the inverse of the design"*. The column
value and the specification are one word apart and mean opposite things on three of
four backbones. **Rename the level `query_only` (or add an explicit
`partner_msa_depth_target = 1`), before someone implements `off` as `off`.** This
is a free fix in a generator, not a hand-edit.

### 1.4 The primary design does something nobody in 83 papers has done

Lit's answer, Q1 / Q6 / bonus — three clean absences, quoted as absences:

> **"One-chain-only single-sequence in a complex: absent from corpus."** Depth 1
> exists — `feldman2026alphainterp` at {1, 5, 10} and {1, 10, 20, 50, 100} (p.36–37),
> `schafer2025confounds` at ColabFold `max-seq = 1` for KaiB — **but all monomers.**
>
> **"No paper in 83 subsamples, masks, deletes or otherwise manipulates the PAIRED
> MSA of a complex as an experimental variable. Nobody even reports what they did
> with it."** Only 5 of 83 notes mention paired/unpaired at all, and four are
> pipeline description.
>
> **"Zero papers"** report whether perturbing one chain's MSA in a complex affects
> the other chain or the interface.

*(Trap lit flagged: `feldman2026alphainterp` p.35 says "All paired MSAs are replaced
with the query sequence" — but its systems are **400 monomers**, so that is AF3
input-schema housekeeping, not a complex manipulation. **Do not cite it as one.**)*

So: by running every cognate row with the partner chain at query-only, **our primary
Group 1 design is the first instance of one-chain single-sequence inside a complex
anywhere in the corpus.** Aditya's brief asked which this is — a novelty worth
claiming, or an uncontrolled choice worth bounding. **It is exactly one of the two,
and which one is decided by whether G17 runs.**

- **With G17** (partner MSA on vs off at R3_ct21 and R7_full), it is a *measured*
  choice: we can state what the query-only regime cost the headline arm, and the
  novelty is defensible — an unoccupied cell, deliberately entered, with its price
  attached.
- **Without G17**, it is an unmeasured manipulation applied to the arm that carries
  the paper's headline, on four backbones, in a configuration nobody has ever
  characterised, with **no published prior to say what it does** (lit: zero papers on
  cross-chain effects). That is not a bounded caveat; it is an open hole under the
  main result.

**This is the strongest argument in the document for promoting G17a (3,600
predictions) from "costed and in no budget tier" to blocking.** It is also the reason
regime (b) looks attractive and is still wrong: (b) would explore the partner's depth
*axis*, but what the design needs is not a curve — it is the **single contrast**
between the regime we chose and the regime everyone else uses.

---

## 2. What is technically deployable on four backbones

**A regime we cannot set identically on four backbones is not a four-backbone
claim.** Here is what each backbone actually does, and the answer is not symmetric.

### 2.1 The per-chain mapping, verified

| backbone | how a per-chain MSA is keyed | source |
|---|---|---|
| **OpenFold-3** | **chain ID** — `msa_a3m_path.get(cid)`, `cid = chain["chain_ids"][0]` | `B/scorer/propose.py:462` |
| **Protenix** | **integer position** — `msa_a3m_path.get(protein_idx)`, a 0-based counter | `B/scorer/propose.py:595` |
| **Boltz-2** | per-chain dict exists, commented *"D3 multi-chain support, currently unused"*; **no caller uses it** | `propose.py:358-360`; `MAP_MSA.md:480` |
| **Chai-1** | **not per-chain at all** — resolved by `sha256(sequence.upper())` inside `--msa-directory` | `B/qsub/rerun_chai.sh:167` |

Three incompatible conventions and one that is not a mapping. The consequence, from
`MSA_SPEC.md:74-93`, is the part to internalise: a caller passing
`{"A": receptor_a3m, "B": ""}`

- **works on OF3**;
- **fails silently on Protenix** — `.get("A")` against `{0:…, 1:…}` returns `None`,
  hits `if not path: continue`, sets **no MSA at all**, and Protenix falls through
  to its launcher default: a **live server fetch at full depth on both chains**.

And the failures run in **opposite directions**. Get it wrong one way on OF3 and a
rejected basename yields `warnings.warn` plus **single-sequence featurisation**
(`B/refs/msa_input_interfaces.md:171-174`) — depth 1 where you asked for 128. Get it
wrong on Protenix and you get **full depth where you asked for 8**. Neither raises.
And neither shows in a status JSON: `MAP_MSA.md:418-430` establishes that
`'use_msa_server': True` and `'msa_server_mode': 'protenix'` are **hardcoded Python
literals** written on the same code path that may have just disabled the server.

So today, a four-backbone two-chain depth arm can produce, in one cell, a genuine
depth-8 (Boltz, if the untested dict path works), a depth-1 (OF3, silent
degradation), a full-depth live fetch (Protenix, silent inflation) and whatever the
cache happened to hold (Chai) — with `ok: true` on all four.

### 2.2 Chai is a different operation

`MAP_MSA.md:131-165`: Chai does **not** pair. Three independent lines of evidence —
`generate_colabfold_msas(protein_seqs=[seq], …)` is a one-element list
(`build_chai_msa_cache.py:118-124`); the cache is deduplicated by sequence hash
**across the whole project** (`:77-81`); `pairing_key` is empty on every row of all
120 cache files (`msa_depth_report.md:56-68`).

Two consequences, and both bear on the regime choice:

1. **For Boltz/OF3/Protenix the apo→cognate transition changes the partner *and*
   the alignment regime; for Chai it changes only the partner.** So a depth × rung
   crossing is measuring a three-factor thing on three backbones and a two-factor
   thing on the fourth. That is not a reason to drop Chai — it is a reason to record
   the pairing state per row (§4) and to say so in the Methods.
2. **The cache-key trap is operational and mandatory.** The receptor sequence is
   identical at depth 8 and at full, so the same sha256 key must resolve to two
   different files. The only way is **one `--msa-directory` per depth arm** (per
   depth × draw × receptor), with the partner's `.pqt` written into the *same*
   directory. D3 did this implicitly because `msa_a3m_path_for()` returned a path
   per (receptor, depth, seed). **A flat shared cache silently serves the wrong
   depth on Chai and nothing catches it.**

### 2.3 The deployability verdict, per regime

| regime | needs per-chain mapping? | deployable on 4 backbones today? |
|---|---|---|
| **(a) Stage 1** — receptor depth, **apo monomer**, no ligand | **No** — one chain, one string | **YES.** This is the D3 code path; it landed 25,810 predictions on all four backbones (`CATALOGUE.md:1310-1312`). |
| **(a) Stage 2** — receptor depth × **partner rung** | **Yes** | **NO, not today.** §2.1. |
| **(b)** — partner depth ladder | Yes, plus a partner MSA the design pins to 1 | **NO**, and §1 says it should not be built. |
| **(c)** — receptor depth × partner × ligand | Yes | **NO, not today** — same blocker as Stage 2, plus a third factor. |

**The distinguishing fact is not (a) vs (b) vs (c).** All three of the *interesting*
forms need the same unbuilt, untested per-chain mapping across three incompatible
keying conventions. What separates them is only how many factors sit on top. That
reframes the sequencing question completely, and it is the argument for §5's order.

### 2.4 And a gate blocks the enumeration regardless

`g1_preflight.py:159-160` hard-codes `r["receptor_msa"] != "on (default)"` into
B7's failure condition. **A row with `receptor_msa = "8"` fails B7.** So a receptor-
depth arm cannot be added to `g1_systems.csv` without either failing the gate or
changing the gate. Combined with `MSA_SUBSAMPLING.md` §4.2 Gap 1 — G5 appears
nowhere in `g1_systems.csv` and nowhere in `SYSTEMS_LINK`
(`matrix_cost.py:165-178`, verified: 12 entries, no G5), so `check_against_systems()`
is structurally blind to it — the position is:

> **Group 8 is a multiplication in a cost model. Group 1 and Group 2 are
> specifications with per-row sequences and hashes. The depth axis has no input
> artefact of any kind.**

Whichever regime is chosen, it needs its own systems file (`g5_systems.csv`, or a
`receptor_msa` level set widened in B7 deliberately and re-proved by planting).

---

## 3. The depth levels

### 3.1 Three points cannot see a curve — and the curve is worse than that

The current spec is `{8, 128, default}` (`RUN_MATRIX.md:653`). Two arguments against,
one from the corpus and one from our own data.

**From the corpus** (lit-3d Q5, first-hand). **All four papers report a turning
point; none reports a monotone trend.** Levels and optima, with lit's locators:

| paper | levels swept | optimum | target-dependent? |
|---|---|---|---|
| `kalakoti2025afsample2` (AF2, column masking) | 0/5/10/15/20/25/30/35/40/**50 %** (45 % absent from every axis), Fig 2a-c p.4 | operating point 15 %; *"**beyond 30 % masking, performance drops** first for the open conformations and subsequently for the closed"* | **yes, explicitly** — *"20 % masking generates the best model for P40131, while 5 % masking is optimal for P71147"* (p.3) |
| `kalakoti2026afsample3` (AF3 **and** AF2, same operation) | 24 settings = 2 networks × 6 masking levels × 2 subsampling states (Table 1 p.2) | **AF3 40 %, AF2 20 %** (p.4, Table S1 p.13) | **yes** — *"as observed in previous studies, the optimal level of MSA randomization is protein specific"* (p.4) |
| `mitjavila2026afsample2t` (AF2, masking targeted at the pocket window) | 0/10/20/30 % deployed, **50 % swept** | pooled mixture, not a level; *"rules out a monotonic 'more masking is better' reading — **50 % collapses**"* | pooled across targets |
| `li2026embedding` (fraction of full MSA) | 100/75/50/25/**0 %** | *"**all methods collapse at 0 % MSA**"* (p.27, Fig 11 caption); 25 % still works | not stated |

A three-level arm fits a line through a curve whose turning point four independent
papers locate and two of them say moves per target.

**Three things in that table are new and change the design, not just the level
count.**

**(i) The turning point is architecture-dependent, and our four backbones are all on
the side that tolerates more.** `kalakoti2026afsample3` is the only paper that runs
the same operation on both generations: *"shows **AF2 degrades past 20 % while AF3
does not**"* (Fig 3a,b p.4), with confidence at 50 % masking **AF3 > 80 against
AF2 ~58** (Fig 3c). Boltz-2, OF3, Protenix and Chai-1 are all AF3-lineage. **So the
AF2-derived optima (15 %, 20 %) are the wrong prior for us, and the AF3 one (40 %) is
more aggressive than anything our ladder has ever reached** — Block D's shallowest
rung is depth 8, and on a 1,996–18,146-row alignment that is not 40 % of anything, it
is 0.04–0.4 %. Different unit, same direction: **the field says AF3-lineage models
take more manipulation before they break, and our shallow end may be truncated
rather than saturated.**

**(ii) Our own data agrees, and nobody noticed.** In the Block D table below, **no
backbone has turned over at depth 8** — every one of the four is still at its extreme
value there, with the steepest step (Boltz 17.77 → 7.00) immediately above it. A
response that is still climbing at the edge of the swept range has not been bounded.
`li2026embedding` puts the floor at **zero** evolutionary information. **Between
depth 1 and depth 8 sits an unexplored region containing both a possible interior
optimum and a known floor, and we have never looked at it.**

**(iii) Masking and subsampling are not substitutes.** `kalakoti2026afsample3`:
*"employing **subsampling along with MSA masking** was the optimal strategy for a
sizable number of targets."* That is direct evidence for §6's bounding paragraph —
a referee cannot be told that our depth arm covers the masking family, because the
one paper that ran both found they are complementary on a sizable number of targets.

**And one finding that makes §4's fidelity columns non-negotiable.**
`kalakoti2025afsample2` p.6: *"**model confidences from different MSA masking levels
are not directly comparable**"*, with confidence decaying **monotonically** (~2 % per
5 pp of masking, ≈89 at 0 % → ≈63 at 50 %) even where accuracy does not. **A depth
sweep therefore cannot be resolved reference-free.** Confidence moves smoothly while
the thing we care about turns over — which is, in another vocabulary, the paper's own
third title clause. Without `pocket_ca_rmsd_active`, a depth ladder has no
reference-based readout at all and the corpus says the confidence-based one will
mislead us.

**From our own Block D**, which is the stronger argument because it is our panel,
our predicate, our backbones. `GATE_2_D3_SLOPES.md:38-43`, predicate-active %:

| backbone | 8 | 32 | 128 | 512 | full |
|---|---:|---:|---:|---:|---:|
| Boltz-2 | **17.77** | **7.00** | 4.92 | 5.38 | 5.08 |
| Chai-1 | 25.08 | 20.16 | 19.69 | 18.38 | 19.37 |
| OF3 | 28.00 | 26.17 | 21.92 | 15.35 | 12.40 |
| Protenix | 15.54 | **16.77** | 9.69 | 2.08 | 0.08 |

Read the rows, not the slopes:

- **Boltz spends 10.8 of its 12.7-point swing between 8 and 32.** Above 32 it is
  flat (7.00 / 4.92 / 5.38 / 5.08). On a `{8, 128, default}` ladder, Boltz's 128 and
  `default` are the same point and the arm is effectively two levels.
- **Protenix is non-monotone at exactly the level the spec drops**: 15.54 → **16.77**
  is the only up-step in the table, and it is at 32.
- OF3 and Protenix do most of their collapse between 128 and full — which
  `GATE_3_STEERING_VS_DEGRADATION.md` shows is *degradation*, not steering, and which
  Block D has already characterised at n≈1,250/cell.
- **Nothing has turned over at 8.** All four backbones sit at an extreme there. Read
  next to `li2026embedding`'s floor and `kalakoti2026afsample3`'s "AF3 does not
  degrade past 20 %", the shallow end is the unexplored end.

### 3.2 Proposal: `{1, 8, 32, default}` — four levels, and not the four I first drafted

**Drop 128 and 512. Add 1.**

- **128 and 512 earn nothing.** Block D measured both, apo, at n≈1,250/cell. 128 is
  where three of four backbones show no step; 512 is inside the collapse region that
  `GATE_3` already classified as degradation rather than steering. Neither carries a
  turning point.
- **Depth 1 is the anchor the ladder has never had.** It is `li2026embedding`'s floor
  (*"all methods collapse at 0 % MSA"*), the level `schafer2025confounds` and
  `feldman2026alphainterp` use, and the only point on the axis where the answer is
  known in advance — which is exactly what makes it useful as a bound.
- **And depth 1 on the receptor is the mirror of what we already do to the partner.**
  A receptor at depth 1 beside a full-Gα partner at query-only is a **pure
  single-sequence two-chain prediction**: no evolutionary information anywhere in the
  input. If the α5 effect survives that, it is steric or structural by construction.
  It is the cheapest and cleanest version of E1.9's question, and it comes free as a
  level on an axis we are already varying.

**State it honestly in the Methods: depth 1 is not a point on a depth continuum, it
is the "no evolutionary information" endpoint.** Treat it as an anchor, not as a
regression point — and in particular do **not** include it when fitting a slope in
`ln(depth)`, where `ln(1) = 0` would give it leverage it has not earned.

| ladder | cells/receptor (× 3 rungs × 2 ligands) | CORE-L17 × 4 bb × n=10 |
|---|---:|---:|
| G5a as specified {8, 128, default} | 18 | 12,240 |
| **proposed {1, 8, 32, default}** | **24** | **16,320** |
| G5b {8, 32, 128, 512, default} | 30 | 20,400 |

**+4,080 predictions over G5a (8.9 % of MINIMAL), and 4,080 *fewer* than G5b for a
ladder placed where the evidence says the shape is.** If only three levels are
affordable, the honest three are **{1, 8, default}** — floor, our biggest measured
effect, and the anchor. `{8, 128, default}` is the one combination that spends three
levels to learn nothing new.

### 3.3 A unit problem nobody has written down

**The corpus's optimum is in fraction units; our ladder is in count units; and we
have never recorded the denominator.**

All four non-monotone papers report a **rate** — masking percentage
(`kalakoti2025afsample2`, `kalakoti2026afsample3`, `mitjavila2026afsample2t`) or a
fraction of the full MSA (`li2026embedding`, 100/75/50/25/0 %). The papers that
report a **raw row count** are a different set — `ye2026multistatebias` (U10, U100),
`waymentsteele2024cluster` (|MSA| = 10, 100), `suzuki2026conforflux`
({2,4,8,16,32,64,128}), `feldman2026alphainterp` ({1,5,10} and {1,10,20,50,100}) —
and **none of those is one of the four that found a turning point.** So the optimum
is only ever reported in a unit our ladder does not use.

And the information-theoretic unit that would bridge them is absent as a
manipulation. Lit, corrected 2026-09-12: **Neff appears in exactly two corpus papers
— `abramson2024af3` Ext. Data Fig 7A p.18 and `suzuki2026pairscaling` Fig 7 p.10 —
and in both it is a *descriptive* property of natural alignments. No paper reports a
subsampling depth in Neff units.** So if we compute Neff on our own rows there is no
published comparator to set beside it.

Meanwhile our receptor alignments span
**1,996 (CNR2) to 18,146 (DRD2)** rows, a ~9× range, with no receptor below 1,000
(`MAP_MSA.md:363-366`, from `msa_depth_report.md:74-123`).

So "depth 128" is **6.4 % of CNR2's alignment and 0.71 % of DRD2's**. A count-based
ladder is a *different* manipulation on each receptor, and the two units do not
convert without the per-receptor full depth — which F-6 means we have never stored.

**Proposal: keep counts as the primary axis** (so the new ladder joins Block D's,
which is worth more than matching the corpus), **and record
`receptor_msa_depth_at_full` per row** so fraction is derivable post hoc and the
corpus's optimum becomes comparable to ours. Report fraction as the secondary axis
in the paper. **Do not add a fraction-based arm** — that is a fifth level nobody has
funded, and the derived column gets most of the value for zero predictions.

### 3.4 One published design we should NOT copy, and why

`mitjavila2026afsample2t` does not deploy a depth level at all — it deploys a
**pooled mixture**: *"we combined sets of models generated at different masking
levels"*, specifically **250 models each at 0 %, 10 %, 20 % and 30 %**, with
contributions to the top-1 % enriching models of **0 % → 16 %, 10 % → 14 %,
20 % → 26 %, 30 % → 44 %** (Fig 5C p.5). The unmasked arm still supplies 16 %, which
is a real argument that the mixture beats any single level.

**It does not transfer to us, and the reason is the readout.** Their metric is
best-of-N enrichment against a reference, where pooling strictly helps: adding any
level can only add candidates. **Ours is a rate** — the fraction of samples that
satisfy a state predicate — where pooling across levels does not estimate anything;
it estimates a weighted average of the levels you happened to pool, and the weights
are a design choice masquerading as a result. `RUN_MATRIX.md` already commits us to
per-cell rates with cluster bootstraps.

So: **keep the levels separate, report per-level rates, and do not pool.** Worth
writing down because the mixture design is the most recent and most successful thing
in this corner of the literature, and importing it would quietly destroy our
estimand.

---

## 4. What must be recorded for the regime to be interpretable at all

`redo/inputs/g1_recording_spec.tsv` carries **47 columns** (counted from the body:
48 lines, one header). Four are MSA-related: `partner_msa_mode`,
`partner_msa_depth`, `partner_msa_depth_uniref90`, `receptor_msa_depth`.

They are necessary and roughly half sufficient. `MSA_SUBSAMPLING.md` §7 lists nine
additions; I endorse all nine and add three. **Below, the ones I would make
blocking** — without them the regime cannot answer the question it exists to answer.

### Blocking — the readout (this decides the paper's claim)

**1–2. `pocket_ca_rmsd_active` and `pocket_ca_rmsd_inactive`. Verified absent: I
grepped all 47 column names for `rmsd|pocket` and the only hit is
`ras_domain_ca_rmsd_to_R7`, which measures the *partner*, not the receptor pocket.**

This is the whole point of running depth at all. `GATE_3:80-101`: at depth 8, the
fraction of predicate-active samples within 1 Å of the deposited active pocket is
**88.7 % on Boltz, 68.3 % on Protenix and 42.9 % on OF3** (56.8 % for OF3 at full).
If the partner arm's predicate-actives are ~90 % sub-Å and the shallow-apo ones are
~43 %, then *"shallow MSA also produces active calls"* is **not a competing
explanation** — it produces a **different object that trips the same two distances**.
That is a far stronger result than an effect-size comparison, and it is the sentence
the depth axis is worth buying.

Without these two columns a G5 row can say *active by predicate* and cannot say
*active like the crystal*, and §5.2c's control is unavailable except post hoc from
structures. **Two columns. Zero predictions.**

### Blocking — the depth itself

3. **`receptor_msa_depth_target` AND `receptor_msa_depth_realised`, as two
   columns.** `subsample_msa.py:106-107`'s silent no-op means a rung label is not a
   depth. `CATALOGUE.md:1124-1127` says it in the same words: *"a rung label is a
   design fact; a depth is a measurement."*
4. **`receptor_msa_depth_at_full`** — the denominator. §3.3. *(New here; not in
   `MSA_SUBSAMPLING.md` §7.)*
5. **`msa_target_unreached`** (bool). The no-op must be **true**, never silent.
6. **A written definition of what `depth` counts** — is the query row in or out?
   `R/rung_msa_depth.csv` says 0 for `ct11`; the Chai cache says 1 for an 11-mer;
   `MSA_SPEC.md:151` asserts `== 1`. **Two of those three conventions make that
   check fire on every correct row.** One sentence in the spec.
7. **`msa_mode_label`** with `default` and `full` as **distinct** values, never
   collapsed. `PARTA_D3.md:128` — 12 of 28 cells disagree — is what happens
   otherwise.

### Blocking — provenance and the paired slot

8. **`receptor_msa_sha256` and `partner_msa_sha256`** — the file actually consumed.
   `RUN_MATRIX.md:631-636` already asks for exactly this.
9. **`msa_paired_depth` and `msa_paired_is_copy_of_unpaired`** (bool). §6.1 #3–#4:
   a paired depth has **never been measured by anyone**, and
   `propose.py:471-472` (OF3) / `:599-600` (Protenix) assign **one path to both
   slots** without raising.
10. **`msa_source`** — `live-colabfold` / `live-protenix` / `prefetched` / `cache` —
    **derived from the env var actually set**, as `rerun_of3.sh:244` already does,
    never from a literal. Two of four launchers assert it as a literal today.
11. **`msa_subsample_draw_id` and `msa_subsample_seed`**, distinct from the
    prediction seed. D3 shared one stream (`subsample_msa.py:104`); P3b cannot be
    analysed without this.
12. **`chai_msa_directory` and its hash.** *(New here.)* §2.2: Chai resolves by
    sequence hash, and the sequence is identical at every depth. **The directory is
    the only artefact that distinguishes a depth-8 Chai row from a depth-full one.**
    Record it or Chai's depth arm is unfalsifiable.

### And the checks, each proved by planting its defect

Following `redo/README.md` rule 4, `MSA_SPEC.md:145-178`, and the standing memory
that *a silent check is worse than none*:

- `receptor_msa_depth_realised <= target`, and `== target` unless
  `receptor_msa_depth_at_full < target`, in which case `msa_target_unreached` is
  **true**. Plant a short alignment; the flag must fire.
- `partner_msa_depth == <the agreed query-only value>` on every two-chain row.
  **Plant a row carrying the partner's real alignment; the check must fail.** This
  is the check that catches §2.1's Protenix key mismatch — it is the *only* thing
  that catches it, which is the argument for it being non-optional.
- `receptor_msa_sha256` identical between a depth row and its matched partner row at
  the same depth. Plant a subsampled receptor MSA; must fail.
- **The four-backbone mapping test, before any GPU.** One two-chain system, one
  depth, all four backbones, and assert the realised receptor depth equals the
  target and the realised partner depth equals 1 **on each**. Plant a chain-ID-keyed
  dict and assert Protenix **fails** rather than silently full-depth-fetching.
- **A missing column is a FAILURE, not a skip.** Per `CLAUDE.md` on
  `run_receipt.py`. An MSA check that skips when `receptor_msa_depth_realised` is
  null is F-6 recurring in the shape of a passing gate.

---

## 5. The recommendation, in order, with the sentence each buys

### Stage 0 — zero GPU. Blocking on everything below.

| item | what | cost |
|---|---|---|
| **E8.3 / P3** | Anchor the ladder: is D3's `full` rung the same condition as `default`? `CATALOGUE.md:1382+` marks it **blocking**; `PARTA_D3.md:128` — 12 of 28 cells outside D1's Wilson CI. | free (a sentence from the pipeline team) or 600 preds |
| **Option Z** | Measure the receptor-side and **paired** depth per (receptor, rung) on CORE-L17. Row counts only. A paired depth has never been measured by anyone. | 0 preds, ~200–400 server queries |
| **§4's 12 columns** | Especially the two pocket-RMSD columns. | 0 preds |
| **§2.1's mapping test** | Four backbones, one system, proved by planting. | ~8 preds |
| **§1's rename** | `off` → `query_only`. | 0 preds |

**Do not commission a two-chain depth cell before the mapping test passes by
planting.** §2.1 is a defect that produces a plausible number in every artefact.

### Stage 1 — regime (a), apo. **The competing-explanation control.**

Receptor depth `{1, 8, 32, default}` × **R0 apo** × no ligand, CORE-L17 × 4
backbones × n=10 = **2,720 predictions**.

**Why this is first, and it is the argument I most want on the record:** the
competing explanation is *"a shallow MSA alone drives GPCRs into the active
state."* That claim is **apo and partnerless by construction**. Refuting or
measuring it does not require a partner chain, so **it does not require the broken
per-chain mapping at all** — it is a monomer, on the code path that already landed
25,810 predictions on four backbones.

**It also removes the confound in the corpus's best existing answer, and lit has now
confirmed that confound from the source.** `ye2026multistatebias` is the paper that
asks our question on our receptor with a state readout, and it answers against the
competing explanation — *"MSA-level manipulation alone, whether through evolutionary
clustering or random subsampling, is largely insufficient to overcome the systematic
conformational bias"* — while the partner *"shifted predictions toward the expected
active conformation across predictors"* (p.13, p.15). But its subsampling leg is
explicitly a different architecture. Verbatim, p.15:

> *"To provide a baseline comparison using an **AlphaFold2-based** MSA manipulation
> approach distinct from the newer architectures evaluated above, we applied
> AF-Cluster to all four target proteins"*

Protocol, from lit's Q3: model **AlphaFold2**; methods **AF-Cluster (DBSCAN)** plus
**U10** and **U100** (uniform random sub-MSAs at depth 10 and 100); all four targets
including **β2AR**; readout paired-reference RMSD, **Fig 5A-B,D p.16**.

**Two facts about that baseline strengthen our case, and both must be stated
carefully rather than pushed.**

1. **Samples and seeds per strategy are NOT REPORTED** — lit swept the note and the
   only count given anywhere is SecA's. So *"subsampling is largely insufficient"*
   rests on an unstated n. We would run 17 receptors × 4 backbones × n=10 per cell
   with the n printed on every table.
2. **The one count that is given shows the baseline was underpowered by MSA
   composition:** SecA yielded *"only four DBSCAN clusters of size four to five
   sequences each."* That is a statement about SecA and AF-Cluster, **not about
   β2AR or about uniform subsampling** — do not generalise it, and do not use it to
   dismiss their result. Cite it only as a reason their baseline's power is unknown.

Stage 1 run beside our existing cognate arm puts both legs **in the same model, on
the same panel, with matched seeds and a stated n**. That is a correction of the
corpus's best existing answer to our own null, not a robustness appendix.

**And one paper is closer to our headline than any document here has acknowledged.**
`mitjavila2026afsample2t` runs AF2/AF2-Multimer on class A GPCRs where the state
axis **is partner presence**, and lit's note records its finding as: the method
*"can be pointed at a state, but not by the masking — **only by including or
omitting the Gα/Gβ/Gγ sequences**"* (p.2, p.7, p.8). **That is our claim, on our
receptor class, from an AF2 model.** It cuts two ways and both belong in the paper:
it is independent support for the co-input beating the MSA operator, and it means
our contribution on that specific point is *"first on AF3-lineage models, at scale,
with a state predicate"* rather than *"first."* It also supplies **no ligand at
all** — lit: *"all models are generated apo. Ligands drive model selection (p.8),
not model generation"* — so it does not touch clause 2.

> **Sentence it buys:** *"On the same panel and the same four models, reducing the
> receptor alignment to N rows raises the apo active-predicate fraction by X points,
> while supplying the α5 C-terminus raises it by Y — and of the shallow-MSA
> predicate-actives only Z % are within 1 Å of the deposited active pocket, against
> W % for the co-input."* The clause after the dash is what the two pocket-RMSD
> columns buy, and it is the strongest available form of the claim.

**What it does not buy:** any statement about interaction. It cannot say whether
depth and the partner act on one mechanism or two.

### Stage 2 — regime (a) × partner rung. **E8.1.**

Gated on Stage 0's mapping test. Depth `{1, 8, 32, default}` × `{R0, R3_ct21,
R7_full}` × no ligand, CORE-L17 × 4 bb × n=10 = **8,160 predictions — of which
Stage 1 already supplies the 2,720 R0 cells, so the marginal cost is 5,440.**

Two live tensions to resolve before this runs, and they are currently unreconciled
between two documents:

- `CATALOGUE.md:1318-1332` advises **against** crossing depth with apo and cognate,
  because both endpoints are pinned (apo 0.158, cognate 0.891), and recommends the
  **middle rungs**. That optimises for *estimating an interaction*.
- The control question in Stage 1 needs the pinned endpoints. G5a includes R0,
  R3_ct21 and R7_full, so it satisfies both — but the two documents give opposite
  advice and **neither cites the other**.

My read: keep all three rungs, and say in advance which contrast answers which
question. R0 vs R7_full is the control; R3_ct21 is where the interaction has
headroom.

> **Sentence it buys:** *"A supplied α5 C-terminus flattens / does not flatten the
> depth slope"* — i.e. one mechanism or two. `CATALOGUE.md:1331-1333`: **either
> result is publishable and they are distinguishable.**

**Caveat to state in advance, not afterwards:** interaction MDE at k=17 clusters is
**0.295** (`RUN_MATRIX.md:517`). An interaction below that is reported as
*unestimable at this n*, **never as absent**.

### Stage 2b — the partner-MSA binary, in place of regime (b). **G17 / E1.9.**

30 receptors × 4 bb × 3 arms × n=10 = **3,600**. Costed at `RUN_MATRIX.md:778`, and
**in no budget tier** — I verified `TIERS` (`matrix_cost.py:209-217`) lists none of
G16a/b, G17a/b, G18a/b, G19, G20, G1c-opt, G1e, G1f, G10b. Twelve costed items,
zero budget lines.

> **Sentence it buys:** *"The partner's effect survives / collapses when the model
> has no alignment for it"* — steric versus co-evolutionary. And it bounds what
> our own query-only design cost the headline arm, which is the first thing a
> referee asks.

### Stage 3 — regime (c), add the ligand. **E8.2 / the full cube.**

Depth `{1, 8, 32, default}` × 3 rungs × `{none, agonist}`, CORE-L17 × 4 bb × n=10
= **16,320** (Stage 2 is a subset of it, so the marginal cost over Stage 2 is
**+8,160**).

**Lit confirms the crossing is unoccupied, from both directions, and the corpus says
so in its own words.** `jung2026boltzperturb` perturbs the MSA with the ligand held
fixed; `lazou2026cryptic` varies the ligand with the MSA held fixed. Lit quotes the
`lazou2026cryptic` note: *"Neither crosses them, so **the interaction between
alignment depth and ligand occupancy is unmeasured on AF3-lineage models from both
directions**."* And `xing2025purified` looks like a crossing and is not —
protein-alone is AF2, the ligand leg is AF3 (p.5), the same two-models defect as
`ye2026multistatebias`.

**One prior effect size is available and it points the other way from the
hypothesis.** `jung2026boltzperturb` measures MSA perturbation *in the presence of*
a ligand on Boltz and reports **SR_O 10.53 % masked, 12.28 % subsampled, both below
vanilla** (p.7). So on an AF3-lineage model with a ligand held present, degrading the
alignment **hurts**. That is a usable prior for sizing Stage 3, and it is worth
noting that it is the opposite sign to the apo effect we measured in Block D
(+12–16 points of predicate-active at depth 8) — which is either a readout
difference (their SR_O is a success rate against a reference; ours is a predicate
fraction) or a real ligand × depth interaction. **Either way it is the first
quantitative reason to expect the ligand factor to do something.**

**(c) is not premature — the ligands exist.** `g2_systems.csv` carries 100
`full_agonist` rows over **26 distinct receptors**, of which **20 are
`dispatch_status = READY` spanning 19 clusters** (6 receptors are
`UNRESOLVED_UNCURATED` / `UNRESOLVED_CHAIN_NO_SEQUENCE` / `BLOCKED_LIGAND_IDENTITY`).
CORE-L17 is 17 receptors in 17 clusters (`matrix_cost.py:54-58`), so the ligand
panel covers it.

**But it is third, for a reason that is about claims and not money.** The falsifiable
hypothesis here is `CATALOGUE.md:1360-1380`'s: `ye2026multistatebias` (p.2) reports
*"large protein partners drive clear conformational switching between states"*
where small molecules do not, so the prediction is that **a partner rescues depth
loss and a ligand does not**. That is a *three-factor* statement resting on an
interaction we have just said is unestimable below 0.30. Stage 1 and Stage 2 each
buy a two-factor sentence that stands on its own. Stage 3 buys a third factor whose
headline is an interaction the design may not be able to resolve.

> **Sentence it buys:** *"A partner rescues what depth removed; an agonist does
> not"* — or, if the ligand does rescue, `ye2026multistatebias`'s asymmetry does not
> survive on an AF3-lineage panel at scale, **which is the more interesting
> result**.

### Two cheap additions I would fund before Stage 3

- **Option Z2 — the column-shuffle control, 680 predictions** (17 rec × 4 bb × 1
  extra level × n=10, restricted to the apo shallow cell).
  `waymentsteele2025reply`: *"column shuffling destroys the state-specific
  predictions."* Same row count, shuffled columns — depth held **exactly** constant
  while local coevolution is destroyed. It is the direct analogue of our
  scrambled-partner arm applied to the alignment, and it converts *"shallow MSA also
  produces active calls"* from an effect size into a mechanism statement. It is also
  the control `schafer2025confounds` says AF-Cluster lacked.
- **The seeds-only cell, 300 predictions** (6 rec × 1 bb × 1 cell × n=50 at
  `default` depth). `stein2022speachaf` is the one corpus paper that separates the
  contributions, and it **concedes seeds alone reach some alternate states**
  (p.8, p.13). Without this, P3b measures draw-variance against an unmeasured
  baseline.

**980 predictions, 2.1 % of MINIMAL, and each answers a question a published paper
has already shown matters.**

### The bill

Marginal, not gross — each stage reuses the cells below it.

| stage | marginal predictions | cumulative | % of MINIMAL (45,860) |
|---|---:|---:|---:|
| Stage 0 — anchor, Z, mapping test, columns | ~600 (or free) | 600 | 1.3 % |
| **Stage 1 — (a) apo, 4 depths** | **2,720** | 3,320 | 7.2 % |
| Z2 + seeds-only | 980 | 4,300 | 9.4 % |
| Stage 2 — (a) × partner rung (+R3, +R7) | 5,440 | 9,740 | 21.2 % |
| **Stage 2b — G17a, partner MSA on/off** | **3,600** | 13,340 | 29.1 % |
| Stage 3 — + agonist level | 8,160 | 21,500 | 46.9 % |

For comparison: G5a as specified is 12,240 and the whole A–D campaign was 124,470.
**Stages 0–2b total 13,340 — 9 % more than G5a alone, and they include G17, which
G5a does not.** Every intermediate stage is a stopping point that buys a complete
sentence; G5a as a single 12,240-prediction commitment buys nothing until all of it
lands. That is the case for staging, and it is not a budget argument.

---

## 6. What we would NOT be controlling for — stated bluntly

Bounding the claim is free. Letting *"we varied MSA depth"* stand in for *"we
controlled for MSA manipulation"* is not honest, and a referee whose competing
explanation is AF-Cluster-shaped is not answered by any of this.

**1. Three of the four MSA-manipulation families.** Ours is **uniform random depth
reduction** only (`subsample_msa.py:104-117`). Untested:

| family | what is manipulated | corpus exemplars |
|---|---|---|
| **clustering** | which rows, by sequence similarity | `waymentsteele2024cluster`, `bryant2024cfold`, `cheng2026af3cluster` |
| **composition purification** | which rows, by "sequence purity" — explicitly *not depth* | `xing2025purified` |
| **column masking** | which **positions**, not which rows | `kalakoti2025afsample2`, `kalakoti2026afsample3`, `mitjavila2026afsample2t`, `jung2026boltzperturb` |

**Column masking must be named separately**: it is what the corpus's only
`factors-crossed` paper does, and it is the family in which the non-monotone optimum
was established. **And it is not a substitute for ours, on the corpus's own
evidence** — `kalakoti2026afsample3` is the one paper that ran both operations
on the same targets and found *"employing **subsampling along with MSA masking** was
the optimal strategy for a sizable number of targets."* So a referee cannot be told
that depth covers masking, and we should not imply it.

**2. The paired depth, unless §4 #9 is implemented — and nobody has ever done it.**
Lit, Q1: **no paper in 83 subsamples, masks, deletes or otherwise manipulates the
paired MSA of a complex as an experimental variable, and nobody even reports what
they did with it.** Only 5 of 83 notes mention paired/unpaired MSAs at all; four are
pipeline description. So there is no published convention to inherit and no prior to
cite. Until we record it, *"we subsampled the receptor MSA"* is, on three of four
backbones, actually *"we subsampled the receptor's unpaired MSA **and** replaced its
paired MSA with the same file"* (`propose.py:471-472`, `:599-600`).

**2b. The cross-chain effect — zero papers, ours included.** Lit, Q6: *"Nothing in
the corpus reports whether perturbing one chain's MSA in a complex affects the other
chain's predicted structure or the interface."* Our design perturbs one chain (the
partner, to query-only) and reads out the other (the receptor's state), on four
backbones, with no published prior for what that does. §1.4 is the response — G17 is
how we bound it — but even with G17 we are bounding one binary contrast, not
characterising a cross-chain effect. **Say that.**

**3. The cold/warm paired-search asymmetry between the two arms the paper
contrasts.** `MAP_MSA.md:342-361`: the pre-warm submitted one sequence per ticket in
mode `env`, never a pair; Boltz's paired mode string is `pairgreedy-env`. **Every
cognate-arm prediction on Boltz/OF3/Protenix paid a cold paired search while its apo
counterpart hit a warm cache.** Stated there as a code-level inference, not a
measurement. It is uncontrolled in Blocks A–D and would remain so.

**4. Whether a short partner is typed as a partner at all.** On OF3,
`use_paired_msas` counts chains with `molecule_type == PROTEIN`
(`propose.py:502-504,524-525`), so **R0 and R1_ct11 are not "partner absent vs
partner present" in OF3's alignment machinery** unless `molecule_type` is set
deliberately.

**5. Chai is not the same experiment.** It never pairs, so its apo→cognate delta is
one chain where the other three are one chain plus an alignment regime. And Chai's
depth slope **does not survive its CI** — `−0.815 [−2.380, +0.357]`
(`GATE_2_D3_SLOPES.md:8-11`), withdrawal `W-D-5`. **"All four backbones" is already
withdrawn once on this axis. Do not let it back in through a heading.**

**6. Interactions below 0.295.** `RUN_MATRIX.md:517-525`. Reported as *unestimable
at this n*, never as *absent*.

**7. Depth in an information unit.** **No paper reports a *subsampling depth* in Neff
units** (lit, Q4, corrected). Neff appears twice in the corpus — `abramson2024af3`
Ext. Data Fig 7A p.18, `suzuki2026pairscaling` Fig 7 p.10 — and both are descriptive
measurements of natural alignments, not manipulations. Published manipulated depths
are raw counts, ColabFold `max_seq:max_extra_seq` pairs, cluster sizes, masking
percentages or MSA fractions. **If we compute Neff on our own rows there is no
published comparator to put beside it.** Report raw counts primary, fraction
secondary (§3.3), Neff only if it earns its place.

**7b. Confidence cannot arbitrate a depth sweep.** `kalakoti2025afsample2` p.6:
*"model confidences from different MSA masking levels are not directly comparable"*,
with confidence decaying monotonically while accuracy does not. So do **not** use
pLDDT/ipTM to pick a depth level or to compare across them. This is the same
phenomenon as the paper's third title clause, arriving on a new axis.

**8. One organism, one receptor class, 17 of 32 clusters.** CORE-L17 is the
ligand-complete one-per-cluster panel, not the census.

**9. The bound on `li2026embedding`'s floor is weaker than the sentence sounds.**
Lit flags it: *"n = 3 at the two endpoint depths vs 9 elsewhere, so the collapse
point is the least-sampled point on every curve."* Since §3.2 proposes depth 1 partly
on the strength of that floor, **do not quote the collapse as firmly as the
interior** — and note that our own depth-1 arm at 17 receptors × 4 backbones × n=10
would be considerably better sampled than the published floor it is anchored to,
which is a point in its favour, not against.

---

## 7. Corrections to the framing I was given

Aditya's brief asked to be corrected rather than agreed with. Five things:

1. **Regime (b) is not a regime.** Verified in §1 — the partner is already at depth
   1 in 1,855 of 1,945 two-chain rows by design, and the gate asserts it. The live
   question is receptor depth × partner-MSA on/off, which is G17, which is cheaper
   and better posed. **Aditya's own reading of this in the brief was correct.**
2. **The per-chain mapping defect is not specific to (b) or (c).** It blocks any
   two-chain depth arm, including regime (a) the moment (a) crosses with a partner
   rung. The brief framed it as a thing to understand before setting *per-chain
   depths*; it is broader than that — it fires whenever a per-chain MSA mapping is
   passed at all, including one that sets the receptor and pins the partner to 1.
3. **The apo control does not need any of it.** The strongest single sentence the
   depth axis buys is a monomer experiment. The brief treats (a) as the smallest of
   three options; it is better described as the **only one that is a control for
   the headline**, with (a)×partner and (c) being interaction studies layered on
   top. That is why §5 stages them rather than picking one.
4. **"No Neff figure exists anywhere in the corpus" is false**, and it is sitting in
   `redo/spec/MSA_SUBSAMPLING.md` §5.2(b) today. Lit withdrew it on 2026-09-12:
   Neff appears in `abramson2024af3` (Ext. Data Fig 7A p.18) and
   `suzuki2026pairscaling` (Fig 7 p.10). **The surviving claim is that no paper
   reports a *subsampling depth* in Neff units.** Flagged at the top of this file;
   the owner of `MSA_SUBSAMPLING.md` should fix that line.
5. **I over-committed to my own first depth proposal and reversed it.** My initial
   draft said `{8, 32, 128, default}`. Lit's Q5 answer — AF3's optimum at 40 % vs
   AF2's 20 %, AF2 degrading past 20 % while AF3 does not, and `li2026embedding`'s
   floor at zero — plus the observation that **no backbone has turned over at
   depth 8 in Block D**, says the unexplored end is the shallow one. The proposal is
   now `{1, 8, 32, default}`. Recorded because the first version was wrong for a
   reason worth remembering: I placed levels where our existing data had *moved*,
   rather than where the response was still unbounded.

Confirmed rather than corrected: **`g1_recording_spec.tsv` has no
pocket-Cα-RMSD-to-active/inactive column.** I grepped all 47 body columns for
`rmsd|pocket`; the sole hit is `ras_domain_ca_rmsd_to_R7`, which measures the
partner. The brief's reading is right, and §4 makes those two columns blocking.
Lit's Q5 independently strengthens it: `kalakoti2025afsample2` p.6 says confidence
across masking levels is *"not directly comparable"*, so a depth sweep has no
reference-free readout at all.

---

## 8. Checked and NOT a finding

- **"`receptor_msa` varies somewhere in the inputs."** It does not. One distinct
  value across all 2,039 rows of `g1_systems.csv` and all 350 of `g2_systems.csv`:
  `"on (default)"`. There is no depth arm anywhere in `redo/inputs/`.
- **"G17 is unenumerated like G5."** It is not. 90 rows,
  `item = G17(proposed)`, `arm = partner_msa_on`, `partner_msa = ON`, and it is
  linked in `SYSTEMS_LINK` (`matrix_cost.py:171-172`) with both a pooled and a
  per-cell grain. It is enumerated and costed; it is only **unbudgeted**.
- **"Chai's cache being shared across complexes breaks the depth arm."** It does not
  break it — it makes the per-depth `--msa-directory` **mandatory**, which D3
  already did implicitly. The trap is a flat cache, not the hash key.
- **"B8 would block a depth arm."** It would not; B8 only compares `off` against
  `ON` counts on the partner column. **B7 is the one that blocks it**, via the
  hard-coded `receptor_msa != "on (default)"` at `g1_preflight.py:160`.

---

## 9. What this proposal does NOT do

It does not enumerate systems, write a generator, touch `redo/build/`,
`redo/gates/` or `redo/inputs/`, or go near anything decoy-related. If a regime here
is adopted, the next artefact is a `g5_systems.csv` generator plus a B7 widening,
both written by a human, both re-proved by planting.

---

## 10. What lit's answer changed, and what it did not

Source: `lit/analysis_review/MSA_SUBSAMPLING_REGIMES_ANSWERS.md` (lit-3d,
2026-09-12, 83 notes, staleness clean). Six questions, six answers, all first-hand.

| # | question | answer | what it changed here |
|---|---|---|---|
| 1 | Does any paper subsample a **complex**, and what did it do with the **paired** MSA? | Somebody masks a complex (`mitjavila2026afsample2t`, GPCRs, AF2-Multimer). **Nobody manipulates the paired MSA of a complex, and nobody reports what they did with it.** | Added §1.4 (our design is the first one-chain-single-sequence complex in the corpus) and §6 #2/#2b. Added the `mitjavila2026afsample2t` engagement to §5 Stage 1 — it is closer to our headline than any document here had acknowledged. |
| 2 | Subsampling with a **ligand** present? Depth × occupancy crossed? | Subsampling-with-ligand yes (`jung2026boltzperturb`). **Crossing: absent, and the corpus says so in its own words** (`lazou2026cryptic` note). | §5 Stage 3 now carries a prior effect size (SR_O 10.53 % masked / 12.28 % subsampled, both below vanilla, p.7) that points the *opposite* way from our apo result. |
| 3 | `ye2026multistatebias` — different models? Protocol? | **CONFIRMED.** AF2 for the subsampling leg (p.15, verbatim), AF3-lineage for the co-input. **Samples/seeds NOT REPORTED**; the one count given shows the SecA baseline was underpowered. | §5 Stage 1's central argument now stands on the quote rather than on hearsay, with both caveats attached. |
| 4 | Depth unit; is Neff absent? | **CORRECTED.** Neff appears twice, both descriptive. The surviving claim: **no subsampling depth is reported in Neff units.** | §3.3 and §6 #7 rewritten; the wrong version flagged at the top of this file for the owner of `MSA_SUBSAMPLING.md` §5.2(b). |
| 5 | Exact levels and optima for the four non-monotone papers. | All four report a turning point. **AF3 optimum 40 %, AF2 20 %; AF2 degrades past 20 %, AF3 does not.** Masking and subsampling are **not substitutes**. Confidence across levels is **not comparable**. | **Reversed my own depth proposal** — `{8, 32, 128, default}` → `{1, 8, 32, default}` (§3.2, §7 #5). Added §3.4 (do not copy the pooled-mixture design). Strengthened §4's fidelity columns and §6 #1/#7b. |
| 6 | Cross-chain effect of perturbing one chain's MSA? | **Zero papers.** | §6 #2b, and it is why §1.4 concludes G17 is blocking rather than desirable. |

**What lit did not change:** the recommendation itself. Stage (a) first, replace (b)
with G17, defer (c) — that rests on `redo/inputs/`, `redo/gates/`,
`redo/protocol/` and `redo/build/`, all read directly here, and would stand on the
same evidence if the corpus said nothing at all. The corpus changed *where the depth
levels go*, *how hard the G17 argument is*, and *which negatives we may claim*.

**Three traps lit flagged, recorded so they are not walked into later:**

1. `feldman2026alphainterp` p.35 — *"All paired MSAs are replaced with the query
   sequence"* — is **400 monomers**, AF3 input-schema housekeeping. **Not** a complex
   paired-MSA manipulation. Do not cite it as one.
2. `xing2025purified` is **not** a depth × ligand crossing: protein-alone is AF2, the
   ligand leg is AF3 (p.5). Same two-models defect as `ye2026multistatebias`.
3. `li2026embedding`'s floor is the **least-sampled point on every curve** (n = 3 vs
   9 elsewhere). Do not quote the collapse as firmly as the interior.
