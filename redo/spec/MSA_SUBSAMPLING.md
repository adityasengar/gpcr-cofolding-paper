# MSA_SUBSAMPLING.md — what the redo should do about MSA depth

**Status: a decision document for Aditya, not a decision.** It lays out what the
frozen campaign did, what we already own, what the redo currently proposes, and
**seven costed options** — Z and Z2 (near-zero GPU, and they belong in every other
option), then A, B, C, D, E in rising cost. It does not pick one.

**Written 2026-09-12** by the orchestrator's subagent, from `redo/protocol/MAP_MSA.md`,
`redo/spec/MSA_SPEC.md`, `redo/spec/RUN_MATRIX.md`, `redo/spec/CATALOGUE.md`,
`redo/build/matrix_cost.py`, `redo/inputs/`, and `data/block_d/`. Every number
below carries a locator or a recomputation. Nothing in `redo/inputs/` was edited;
no compute was commissioned; no git was run.

Two path roots are abbreviated, following `MAP_MSA.md`:

| abbrev | real path |
|---|---|
| `B/` | `redo/protocol/received/source_bundle/` |
| `R/` | `redo/protocol/received/` |

---

## 0. The four things a reader must not miss

1. **The competing explanation is real but weaker than feared, and the corpus has
   already tested it on β2AR with a state readout.** Shallow MSA is the field's
   standard route to alternative conformations, and two independent method papers
   treat "shallow MSA already does this" as the null they must exclude
   (`richman2025conformix`, `suzuki2026pairscaling`). But `ye2026multistatebias`
   ran uniform random sub-MSAs at depth 10 and 100 **on β2AR** as an explicit
   control and reports that *"MSA-level manipulation alone, whether through
   evolutionary clustering or random subsampling, is largely insufficient to
   overcome the systematic conformational bias"* — while the partner, on the same
   receptor, *"shifted predictions toward the expected active conformation across
   predictors"* (p.13, p.15). **Two caveats make that not a free pass** (§5.1). So
   the depth axis is still a **control for the headline**, not a robustness
   appendix — but it is a control we are favoured to win. §5 says how far the
   current design goes and where it stops.

2. **"Depth 8" is not one number once there are two chains.** The frozen campaign's
   depth ladder was **apo only** (`B/scripts/build_tier_d3_manifest.py:237` — every
   D3 row is `partner_type: "apo"`), so the question never arose. The moment a
   partner chain exists there are at least four depths — receptor unpaired, partner
   unpaired, paired, and whether paired is a copy of unpaired — and **the four
   backbones disagree about every one of them**, including how the per-chain
   mapping is keyed (`propose.py:462` chain-ID for OF3, `:595` integer-position for
   Protenix). §6.

3. **The depth cube is costed but not specified.** `G5a`/`G5b` exist as arithmetic
   in `redo/build/matrix_cost.py:128-129` and as prose in `RUN_MATRIX.md:651-657`.
   They appear **nowhere** in `redo/inputs/g1_systems.csv` — all 2,039 enumerated
   systems carry `receptor_msa = "on (default)"` and `ligand = "none"`, and
   `SYSTEMS_LINK` (`matrix_cost.py:165-178`) has no G5 entry, so
   `check_against_systems()` cannot catch the gap. Group 1 has per-row sequences and
   hashes; Group 8 has a multiplication. §4.2, Gap 1.

4. **The published depth response is non-monotone with a target-specific interior
   optimum**, established independently three times (`kalakoti2025afsample2`,
   `mitjavila2026afsample2t`, `kalakoti2026afsample3`), with a floor at 0 % MSA
   (`li2026embedding`). **Block D's two-mechanism result is therefore the field's
   expected shape, not an anomaly** — which changes how we frame it (§5.1) — and it
   means a three-level depth arm `{8, 128, default}` is specified in a shape the
   field has already ruled out (§9, Option E).

---

# 1. What the FROZEN campaign actually did

## 1.1 In Blocks A–D proper: **no subsampling at all, on any backbone**

`MAP_MSA.md` §2–§5, per backbone, "Subsampling / depth cap / filtering":

| backbone | subsampling in A–D | source of the MSA | paired? |
|---|---|---|---|
| Boltz-2 2.2.1 | **none** (`MAP_MSA.md:90-96`) | live, ColabFold public API, `--use_msa_server` at `R/rerun_boltz.d9c646af.sh:120` | **yes**, server-side |
| Chai-1 0.6.1 | **none** (`MAP_MSA.md:167-174`) | local `.aligned.pqt` cache, `--msa-directory` at `B/qsub/rerun_chai.sh:135-136` | **no** — `pairing_key` empty on every row of all 120 cache files (`MAP_MSA.md:142-146`) |
| OF3-preview 0.4.4 | **none** (`MAP_MSA.md:230-237`) | live ColabFold via `B/qsub/colabfold_shim.py` | **yes**, `"use_paired_msas": is_multimer` at `B/scorer/propose.py:485` |
| Protenix 2.0.0 | **none** (`MAP_MSA.md:294-298`) | live, **Protenix's own server**, `--msa_server_mode protenix` at `R/rerun_protenix.d9c646af.sh:103` | **yes**, decided internally |

`MAP_MSA.md:545-552` (§9.1) is the sharpest statement: `_row_input_content`
(`B/scorer/propose.py:687-746`), the function every manifest row passes through,
calls the templaters **without** `msa_a3m_path` at `:708,710` / `:721,723` /
`:728,730`. Only two callers ever pass it, and both are D3-only and monomer-only.

## 1.2 The one depth ladder: Tier D3, and its exact parameters

`B/scripts/build_tier_d3_manifest.py:60` — `DEPTHS = ("full", 512, 128, 32, 8)`.
Grid at `:3-5`: 26 receptors × 4 backbones × 5 depths × 5 seeds × 10 samples =
26,000 dispatched; **25,810 landed** (190 short, 0.73%, non-uniform — worst cells
n=1,250 at OF3×full and Chai×full; `CATALOGUE.md:1310-1312`).

**The draw, exactly** (`B/scripts/subsample_msa.py:104-117`): keep row 0 (the
query), draw `depth − 1` rows **uniformly** with `random.Random(seed)`, sort them
back into original a3m order, write atomically (`:209-213`). Byte-identical replay
is self-checked (`:129-147`). So the subsample is **random uniform depth
reduction** — not clustering, not composition purification. That distinction is
load-bearing in §5.

Three parameter facts that a re-run must inherit or deliberately break:

- **Seed behaviour.** The subsample draw uses the *same* `seed` as the prediction
  (`subsample_msa.py:104`). So depth arm and sampling arm share one seed stream:
  draw-variance and seed-variance are **not separable** in anything D3 shipped.
  That is precisely what `P3b` exists to fix (§4.2).
- **Silent no-op below target.** `subsample_msa.py:106-107`: if
  `len(entries) <= depth`, the input is returned **unchanged**, and the manifest
  still records `msa_depth: 512` (`build_tier_d3_manifest.py:246`). Row counts print
  only under `--print-stats` (`subsample_msa.py:215-224`) and are stored nowhere.
  **A "depth 512" arm on a 300-row alignment is a 300-row arm wearing a 512 label.**
- **`full` is not `default`.** `build_tier_d3_manifest.py:59` says `"full"` means
  "live-fetch or no subsample", but `msa_a3m_path_for()` returns a concrete cached
  path for `full` too (`:118-120`), which sets `MSA_A3M_PATH` and therefore
  **disables** the live server. `full` is a cached full fetch through the subsample
  pipeline; `default` is a live fetch. `MAP_MSA.md:330-334`. This is the mechanism
  behind the D1/D3 drift in §3.4.

Per-backbone delivery of the subsampled file also differs, and it is not cosmetic
(`MAP_MSA.md:463-484`, §8.5):

- **Boltz** — inline YAML `msa:` field.
- **OF3** — `_of3_apply_msa_paths` hands OF3 the **parent directory**, not the file
  (`B/scorer/propose.py:465-470`), and OF3 accepts only basenames in its
  `max_seq_counts` registry (`:438-441`). `msa_a3m_path_for()` names the file
  `colabfold_main.a3m` for exactly this reason (`build_tier_d3_manifest.py:114-120`).
  **Nothing verifies OF3 accepted it**; a rejected file yields a `warnings.warn` and
  single-sequence featurisation (`B/refs/msa_input_interfaces.md:171-174`).
- **Protenix** — `pc["unpairedMsaPath"] = path; pc["pairedMsaPath"] = path`
  (`propose.py:599-600`). OF3 the same at `:471-472`. **One file in both slots.**
- **Chai** — `B/scripts/subsample_msa_chai.py` writes a `.pqt` with
  `pairing_keys.append("")` (`:92`).

## 1.3 What was recorded — and F-6

`MAP_MSA.md` §7, and it is unambiguous. All four row-touching scorer modules
(`B/scorer/schema.py`, `rerun.py`, `pocket_metrics.py`, `switch_signal.py`) grepped
for `msa|a3m|pqt` return **zero matches** (`MAP_MSA.md:376-381`). The one real
scored row we hold, `R/rows_csv_line.txt`, has no MSA-named field among its ~90
columns, and `redo/protocol/ROWS_SPEC_DERIVED.md` lists none.

> **You cannot join MSA depth, source, or pairing state to a single scored
> prediction. Not for one row, not for 42,180.** (`MAP_MSA.md:384-385`)

### Knowable from code vs unknowable after the fact

| question | knowable? | how |
|---|---|---|
| Which MSA server each backbone used | **knowable** | launcher flags, `MAP_MSA.md` §2–§5 |
| Whether pairing was on for a two-chain input | **knowable in principle** | code: `propose.py:485` for OF3; inferred for Boltz/Protenix from output-tree directory names (`PHASE_1D_EXTENSION.md:33,62`) — but those trees **were not shipped** |
| Which depth rung a D3 row belongs to | **knowable** | reconstructable from the path (`GATE_2_D3_SLOPES.md:128`, regex `/pool/([^/]+)/([^/]+)/([^/]+)/seed_\d+/`) |
| **The realised row count that reached the model** | **UNKNOWABLE** | never recorded anywhere; §1.2's silent no-op means the rung label is not a proxy |
| **Whether a cognate row's paired search succeeded, was warm, or truncated** | **UNKNOWABLE** | only `_of3_colabfold_http_summary.json` could say, and only for OF3, and it was not shipped (`MAP_MSA.md:249-254`) |
| Whether Boltz/Protenix status JSON's MSA mode is true | **KNOWN FALSE in D3 mode** | `'use_msa_server': True` and `'msa_server_mode': 'protenix'` are Python **string/bool literals** written on the same path that may have just disabled the server (`B/qsub/rerun_boltz.sh:164`, `rerun_protenix.sh:137`; `MAP_MSA.md:418-430`) |

The last row is the one to carry forward: **for Protenix in depth mode the status
JSON asserts a live full-depth server fetch while the run used a pre-fetched
depth-8 a3m, and nothing in any artefact contradicts it.**

## 1.4 One asymmetry that the frozen campaign never controlled

`MAP_MSA.md` §6.3: the pre-warm (`B/scripts/msa_prewarm.py:135-138`) submitted
**one sequence per ticket, mode `env`** — never a pair. Boltz's output directories
are `msa/<N>_unpaired_tmp_env/` and `msa/<N>_paired_tmp_pairgreedy-env/`
(`PHASE_1D_EXTENSION.md:33`); the paired mode string is different. So **every
cognate-arm prediction on Boltz/OF3/Protenix paid a cold paired search while its
apo counterpart hit a warm cache** — an uncontrolled difference between exactly
the two arms the paper contrasts. `MAP_MSA.md:360-361` states this as a code-level
inference, not a measurement, and Q1 to `paper_af3` would settle it.

---

# 2. Interlude: the partner-side measurement we already hold

`R/rung_msa_depth.csv` — **recomputed here, body counted, not quoted from
`MSA_SPEC.md`.** 112 rows = 7 rungs × 16 Gα families. Filtering to `note == "ok"`
(three rows carry `unpaired_depth = -1`, a ColabFold timeout sentinel, not a depth):

| rung | len | n ok | depth = 0 | min | max |
|---|---:|---:|---:|---:|---:|
| `R1_ct11` | 11 | 16 | **16 of 16** | 0 | 0 |
| `R2_ct15` | 15 | 16 | **5** | 0 (Gq, G11, G12, G14, G15) | **459 (Gs)** |
| `R3_ct21` | 21 | 16 | 0 | 47 (G15) | 582 (Golf) |
| `R4_a5helix` | 26 | 16 | 0 | 186 (G15) | 1,995 (G11) |
| `R5_a5plus` | 36 | 16 | 0 | 2,273 (G15) | 3,043 (Gi3) |
| `R6a_da5` | 324–368 | 15 | 0 | **5,764 (G12)** | 9,176 (Gi1) |
| `R7_full` | 350–394 | 14 | 0 | **6,289 (G12)** | 9,203 (Gi1) |

The other ten `R2_ct15` families are 2, 6, 18, 21, 21, 21, 25, 33, 33, 42 — all
≤ 42, as `MSA_SPEC.md:32` says.

**Two corrections to `MSA_SPEC.md` §2, both small, both in a document sent to the
pipeline team:**

- `MSA_SPEC.md:35` gives R6a/R7 as **"8,474–9,203"**. The true `note == "ok"`
  ranges are **5,764–9,176** (R6a) and **6,289–9,203** (R7). The lower bound is
  understated by ~2,700 rows. Four families (G12, G13, Golf, G15) sit below 7,000
  on both rungs. The argument is unaffected — everything is still three orders of
  magnitude above `ct11` — but the number is wrong.
- `MSA_SPEC.md:35` gives lengths as "368 / 394". Those are **Gs**; the families
  span 324–368 (R6a) and 350–394 (R7).

**And a units question that is not cosmetic.** `rung_msa_depth.csv` reports
`unpaired_depth = 0` for all 16 `ct11` rows. The Chai cache reports **1** for
substanceP, an 11-mer (`msa_depth_report.md:355`, "depth (rows incl. query)";
`MAP_MSA.md:591-593`). Those are almost certainly the same physical outcome —
query only — counted two ways. `MSA_SPEC.md:151` then asks for the check
`partner_msa_depth == 1`. **If the recorder counts the way `rung_msa_depth.csv`
does, that check fires on every correct row.** `redo/inputs/g1_recording_spec.tsv`
defines `partner_msa_depth` only as "the ladder is uninterpretable without it" —
it does not say whether the query row is counted. This is a one-line fix in the
recording spec and a silent-failure class if it is not made. See §7.

---

# 3. What Block D already measured — and it is OURS, already paid for

`CLAIMS.md:26`: *"MSA depth moves the predicate, by two different mechanisms —
Boltz a clean lever; OF3 and Protenix degradation."* Status: **written, scoped**.
Note the standing caveat from `CLAUDE.md`: **Block D shipped no row-level data**,
so everything below is read off Block D's own gate documents, which recompute from
`experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` on their side. We cannot
re-derive it here. It is PROSE-ONLY in `analysis/block_d/verify_claims.py`'s sense.

## 3.1 The design

26 Class A receptors × 4 backbones × 5 depths (8/32/128/512/full) × 5 seeds ×
10 samples = 25,810 landed. **Apo only. No partner at any depth, no ligand at any
depth** (`CATALOGUE.md:1310-1313`; `PARTA_D3.md:5-9`, 22 paralog clusters).
Predicate: `d_npxxy_y558_y753_oh < 9.082 Å` **AND**
`d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`.

## 3.2 The effect — predicate-active %, per (backbone × depth)

`data/block_d/06_gate_reports/GATE_2_D3_SLOPES.md:38-43`, n stated per cell:

| backbone | depth 8 | 32 | 128 | 512 | full | **swing (8 − full)** |
|---|---:|---:|---:|---:|---:|---:|
| **Boltz-2** | **17.77** | 7.00 | 4.92 | 5.38 | 5.08 | **+12.7 pts** |
| **Chai-1** | 25.08 | 20.16 | 19.69 | 18.38 | 19.37 | +5.7 pts |
| **OF3** | 28.00 | 26.17 | 21.92 | 15.35 | 12.40 | **+15.6 pts** |
| **Protenix** | 15.54 | 16.77 | 9.69 | 2.08 | **0.08** | **+15.5 pts** |

n per cell 1,250–1,300. **This is the number that makes the axis load-bearing.**
Going from a full alignment to 8 rows moves the apo active-fraction by **12–16
points on three of four backbones, with no partner and no ligand present.**

Slopes, reproduced exactly by GATE-2 under `ln(depth)` with `full` imputed as 4096
(`GATE_2_D3_SLOPES.md:54-64,84-89`), with a cluster bootstrap over the 26 receptors
that the original headline lacked:

| backbone | slope %/ln(depth) | 95% CI (cluster boot, 1000 reps) | signed? |
|---|---:|---|---|
| Boltz | −1.684 | [−2.692, −0.812] | **yes** |
| Chai | −0.815 | [−2.380, **+0.357**] | **NO — crosses zero** |
| OF3 | −2.732 | [−4.365, −1.145] | **yes** |
| Protenix | −2.956 | [−4.678, −1.581] | **yes** |

Three things travel with those slopes and all three must travel with any redo
sentence that quotes them:

- **"All four backbones" does not survive the CI.** Chai is inconclusive
  (`GATE_2_D3_SLOPES.md:8-11,96-100`). The corresponding withdrawal is
  `data/block_d/03_withdrawals/W-D-5_d3_all_four_backbones_lever.md`.
- **The log is natural, not base-10.** The headline label "%/log(depth)" is off by
  2.303 if read as log10 (`GATE_2_D3_SLOPES.md:79,101-103`; withdrawal
  `W-D-6_d3_slope_unit_log_vs_ln.md`).
- **`full = 4096` is nominal.** The real full-MSA row count is per-receptor and
  spans ~2K–11K (`:72-74,104-107`), and Block B's audit shows Boltz consuming
  **13,678** rows for one ADRB1 cell (`CATALOGUE.md:1426-1427`). **Every slope is
  fitted against an x-axis whose top point is wrong by more than an e-fold**, because
  no realised depth was ever recorded. This is F-6 costing us a number, today.

## 3.3 The two mechanisms — this is the part that matters most

`data/block_d/06_gate_reports/GATE_3_STEERING_VS_DEGRADATION.md`. The question:
is "more predicate-active at shallow depth" a real move toward the active state
(**LEVER**) or structural degradation that happens to trip two coarse distances
(**DEGRADATION**)?

| backbone | slope | matched-seed 7TM Cα RMSD full→d8 | ΔpLDDT | **% of predicate-active that are also sub-Å to active** | verdict |
|---|---:|---|---:|---:|---|
| Boltz-2 | −1.68 | ~1–4 Å | −0.5 | **88.7 %** at d8 (85–99 % across depths) | **LEVER (clean)** |
| Chai-1 | −0.82 | ~2–5 Å | −1.0 | 75.7 % (76–83 %) | **LEVER (muted)** |
| OF3 | −2.73 | **~10–14 Å** on high-swing receptors | **−3.9** | **42.9 %** at d8, 56.8 % at full | **DEGRADATION-leaning** |
| Protenix | −2.96 | **~16–20 Å** on high-swing receptors | **−3.2** | 68.3 % at d8 | **MIXED, receptor-dependent** |

(`GATE_3:10-15`, `:80-101`, `:120-144`.) Supporting detail worth having in hand:

- The (b) column — fraction sub-Å to the **active** reference — moves *with* (a) on
  Boltz (42.5 → 51.2 % as depth falls) and *against* it on OF3 (50.6 → 29.7 %).
  `GATE_3:68-71`.
- Exemplars: **Boltz OPSD** depth-8, `pocket_ca_rmsd_active` 1.25 → **0.41 Å**,
  backbone RMSD-to-full 3.9 Å — a textbook lever (`:162,195`). **Protenix AGTR1**
  depth-8, predicate clears but `pocket_ca_rmsd_active` moves **0.76 → 1.24 Å**,
  *away* from active, 15.8 Å from full — a textbook degradation (`:166`).
  **Protenix LT4R1** depth-8 is lever-at-pocket *and* 15–20 Å novel global fold
  (`:164`) — both at once.
- **Anchor identity is 4/4 on every spot-check row** (`:170`). These are not shredded
  folds; they are "different plausible folds".

**GATE-3's own verdict on the D3 headline:** *"the ranking is nearly inverted once
fidelity is required… The −2.96 / −2.73 slopes are inflated by degradation samples
that a geometry-fidelity filter would exclude."* (`:227-233`)

**The right claim form, in GATE-3's words (`:235-240`): a conditional lever.**

### A denominator discrepancy inside GATE-3 — checked, and it is real

GATE-3 prints predicate-active % twice, and the two disagree by 1–2 points:
Boltz depth-8 is **17.77 %** in the population table (`:39`, n = 1,300) and
**19.25 %** in the fidelity table (`:82`, no n given). I recomputed the implied
denominators across all 20 cells: **the numerator is identical in every cell**
(e.g. Boltz d8 = 231 actives; 231/1300 = 17.77 %, 231/1200 = 19.25 %), and the
fidelity table's denominator is smaller by **exactly 90–100 rows per cell**, i.e.
two receptors' worth (2 × 5 seeds × 10 samples).

So the fidelity table — **the basis of the entire LEVER/DEGRADATION verdict** — is
computed on a **24-receptor subset, and GATE-3 states n nowhere in it.** The
`frac_pred_that_are_subA` ratios are internally consistent (same subset top and
bottom), so **the verdicts stand**. But the two `pred%` columns in one document are
not the same quantity, and only the first carries an n. *Quote `:39` for rates,
`:82` only for the fidelity ratio, and never put the two side by side.*

## 3.4 The D1/D3 anchor conflict — a constraint, not a curiosity

`data/block_d/02_caveats/C-D-8_opsd_boltz_cross_tier_divergence.md:10-20`: OPSD ×
Boltz-2 apo reads **38.8 %** in D1 (n=500) and **10.0 %** at D3's `full` rung
(n=50). Same scorer, same receptor, same predicate. 28.8 points, ~3σ.

`data/block_d/07_partA/PARTA_D3.md:128` shows it is not one cell:
**"28 cells; 12 outside D1's Wilson 95 % CI."**

`RUN_MATRIX.md:599-622` and `CATALOGUE.md:1389-1417` add the evidence that decides
which hypothesis survives — Block B's apo arm is an independent third measurement
of all 28 D1 cells, and **D1's point estimate falls inside Block B's 95 % Wilson
interval on 26 of 28**. So D1 reproduces, and D3's `full` rung is the odd one out.
Undersampling does not explain it: if the true rate were 0.388, observing 5/50 is a
~3.7σ draw (p ≈ 5×10⁻⁴).

**Conclusion: D3's `full` and D1's `default` are different conditions wearing the
same name** — exactly what §1.2's third bullet predicts from the code. Twelve of
28 cells disagree, and nothing in the drop could have caught it because no cell was
run both ways.

**This is a hard precondition on any new depth work.** A depth ladder whose top
rung is not the same condition as the rest of the campaign's default measures a
slope against an undefined origin.

---

# 4. What the redo currently PROPOSES

## 4.1 The four items, as specified

From `redo/build/matrix_cost.py:111-129` (the cost model) and
`RUN_MATRIX.md:624-664` / `:752-766` (the design):

| item | what it is | panel | bb | cells/rec | n | **predictions** |
|---|---|---|---:|---:|---:|---:|
| **P3** | MSA-preparation drift control | 6 receptors | 1 | 2 | 50 | **600** |
| **P3b** | subsample-draw variance probe | 6 receptors | 1 | 3 | 50 | **900** |
| **P2** | depth × rung × ligand cube **pilot** | CORE-L17 | 1 | 2×3×2 = 12 | 10 | **2,040** |
| **G5a** | depth cube 3×3×2 | CORE-L17 | 4 | 3×3×2 = 18 | 10 | **12,240** |
| **G5b** | depth cube 5×3×2 | CORE-L17 | 4 | 5×3×2 = 30 | 10 | **20,400** |

(Verified by running `python3 redo/build/matrix_cost.py`; CORE-L17 = 17 receptors,
17 clusters, `matrix_cost.py:58,66`.)

The cube's levels, `RUN_MATRIX.md:651-654`:

| | depth | partner rung | ligand |
|---|---|---|---|
| **G5a** (Minimal/Intended) | 8, 128, **`default`** | R0 (apo), R3_ct21, R7_full | none, agonist |
| **G5b** (Expansive) | 8, 32, 128, 512, `default` | R0, R3_ct21, R7_full | none, agonist |

**P3** runs `msa_mode=default` *and* `depth=full` on the same 6 receptors and seeds,
to anchor the ladder against §3.4's drift (`RUN_MATRIX.md:626-630`). **P3b** runs
**3 independent subsample draws at depth 32** on 6 receptors at n=50, so
draw-variance separates from seed-variance (`:637-640`) — reinstating a probe that
Block C specced and D3 never delivered (`:617-622`).

Sequencing is already specified and is correct: `RUN_MATRIX.md:894` puts
`P3, P3b → (MSA anchored) → P1, P1b, P2, P4 → [GATE §3.3] → G1 G3 G5 G6`, and `:910`
says **"P3/P3b before any depth cell. Running G5 on an unanchored `full` rung would
—"**. G5a sits in the **MINIMAL** tier (`matrix_cost.py:210-211`), so the depth cube
is funded at the lowest budget.

Tier totals, recomputed: **MINIMAL 45,860** / INTENDED 155,100 / EXPANSIVE 249,540.
G5a is **26.7 % of MINIMAL**. G5a+P2+P3+P3b = **15,780 = 34.4 % of MINIMAL.**

## 4.2 Is the design coherent? Mostly yes. **Six gaps** — 1, 2, 3, 4, 5a, 5.

**What is right, and worth saying plainly:**

- **The cube is a genuine 3-factor crossing of depth × partner × ligand**, and
  `RUN_MATRIX.md:577-587` establishes that the crossing is unoccupied in the corpus:
  of 81 papers exactly one crosses an MSA manipulation with a co-input
  (`mitjavila2026afsample2t`, masking 0/10/20/30 % × partner present/absent, 250
  models per cell, 10 class A receptors [p.8]) and it is AF2, with **no ligand
  channel**. `xing2025purified` [p.5], `jung2026boltzperturb` [p.7] and
  `lazou2026cryptic` [p.5] each break in a different place.
- **Running on CORE-L17 only is the right economy.** Depth multiplies everything and
  is the least load-bearing title clause (`RUN_MATRIX.md:644-646`).
- **All four backbones is justified, not reflexive** — §3.3 makes backbone a real
  moderator (lever vs degradation), not a replication (`RUN_MATRIX.md:646-649`).
- **The power position is stated in advance and honestly.** G5 is powered for main
  effects and for interactions ≥ 0.30; an interaction below that is reported as
  *unestimable at this n*, never as *absent* (`RUN_MATRIX.md:517-525`). Interaction
  MDE at k=17 is **0.295**; at k=32 it would be 0.215.
- **P3 and P3b are correctly placed as blocking preconditions**, and each addresses
  a defect that actually shipped (§3.4; and D3's shared seed stream, §1.2).

**Gap 1 — G5 is not enumerated anywhere.** `redo/inputs/g1_systems.csv` holds 2,039
rows with per-row sequences, sha256s and cluster assignments. **Every one carries
`receptor_msa = "on (default)"` and `ligand = "none"`, and no row has `item`
beginning `G5`.** `SYSTEMS_LINK` (`matrix_cost.py:165-178`) links 12 items to that
file and **G5 is not among them**, so `check_against_systems()` — the guard that
exists precisely because "a cost table that disagrees with the system table is worse
than no cost table" (`matrix_cost.py:183-185`) — is structurally blind to G5. There
is no generator, no input artefact, no hash. **G5 is a multiplication, and Group 1
is a specification.**

**Gap 2 — P3/P3b anchor one backbone; the drift was measured on four.** Both are
`1` backbone (Boltz, by `matrix_cost.py:113-114` and the rest of the pilot stage).
The D1/D3 divergence is **12 of 28 cells across all four backbones**
(`PARTA_D3.md:128`). A Boltz-only drift control anchors Boltz. Extending P3 to four
backbones costs 6 × 4 × 2 × 50 = **2,400** (+1,800); P3b likewise 6 × 4 × 3 × 50 =
**3,600** (+2,700). **+4,500 predictions, 9.8 % of MINIMAL, to anchor the axis on
the backbones where the effect is largest and the mechanism is worst understood.**

**Gap 3 — the levels are named but not defined.** `default` is a *mode*; `8`/`128`
are *targets*. §1.2 shows a target is not a realised depth (silent no-op below
target) and that `full ≠ default`. The spec must say, for each level: is the file
pre-fetched or live; what the target is; what happens when the alignment is shorter
than the target; and **what is recorded** (§7). It says none of that today.

**Gap 4 — depth is varied on the receptor; the partner's regime is specified
elsewhere and the two documents have not been reconciled.** `MSA_SPEC.md:57-59`
requires the **partner** chain to hold a query-only depth-1 alignment at every rung,
on all four backbones. `CATALOGUE.md:800` says "Group 8 varies the depth of the
**receptor's own** alignment". Those are compatible — but only if stated jointly, per
cell, in one table. G5's R7_full cells would then run the **complete Gα with a
crippled, depth-1 alignment**, which is a deliberate choice with a real cost (it
removes the coevolutionary pairing that is arguably part of how a Gα drives the
receptor active) and it is nowhere written down as a choice. See §6.4.

**Gap 5a — P3b's premise is right, but seeds and draws may not be separable, and one
paper has measured the overlap.** P3b assumes draw-variance and seed-variance are
two sources to be told apart. Lit's answer: *"nobody states a resampling unit as a
design principle"*, and the practice splits three ways — draw pooled as a sample
(`waymentsteele2024cluster`, 500 samples each at depth 10 and 100;
`ye2026multistatebias`, 50 per condition; `bryant2024cfold`, 13 per threshold),
draw crossed with seed (`lee2025seqassoc`, *"5 models × 5 seeds per depth"*;
`vo2026fiducials`, 50 seeds per depth), and draw treated as the model
(`mitjavila2026afsample2t`, 250 per masking level, then pooled). **The one paper
that separates the contributions is `stein2022speachaf`**, which runs random-seed
variation alone (3 seeds per MSA) as a distinct arm and **concedes seeds alone
reach some alternate states** (p.8, p.13). So the two are not cleanly separable, and
the precedent for settling it is a **seeds-only arm at fixed depth**. P3b as
specified (3 draws × 50 at depth 32, 6 receptors, Boltz) gives draw-variance at
fixed seed-budget; adding a seeds-only cell at `default` depth — 6 × 1 × 1 × 50 =
**300** — completes the decomposition. Cheap, and it is the only published design
for this question.

**Gap 5 — the residual arm that answers "how much did we change by doing that?" is
costed and in no budget.** `G17a` ("partner MSA on/off, pooled", E1.9) =
`30 × 4 × 3 × 10` = **3,600**; `G17b` per-cell = **18,000**. `MSA_SPEC.md:198` calls
this arm **"Wanted anyway, on top of the primary. It answers *how much did we change
by doing that?*, which is the first question a referee asks."** But `TIERS`
(`matrix_cost.py:209-217`) was written before the 2026-09-12 additions: **none of
G16a, G16b, G17a, G17b, G18a, G18b, G19, G20, G1c-opt, G1e, G1f or G10b appears in
MINIMAL, INTENDED or EXPANSIVE.** Twelve costed items, zero budget lines. G17a is
the one of those twelve that the MSA decision depends on.

---

# 5. Is this a control for the headline, or just varying depth?

## 5.1 Why the question is not rhetorical — and what the corpus already settles

*(This section rests on `lit/analysis_review/MSA_SUBSAMPLING_CORPUS_ANSWERS.md`,
2026-09-12, written by the lit session in answer to the questions that were at the
end of this document. Corpus: 83 notes. The `msa-subsample` tag fires on **20 of
83** papers.)*

Random shallow-MSA subsampling is **the** established route to alternative
conformations from a single-sequence-input folding model, and the corpus proves it
is the standing null: **`richman2025conformix` and `suzuki2026pairscaling` each run
subsampling as an ablation they must beat** — *"that random shallow-MSA subsampling
already achieves it"*, *"that depth reduction already achieves it"*. Two
independent method papers treat "shallow MSA already does this" as the hypothesis
to exclude. **It is our null too.**

### The evidence that the competing explanation does NOT reach the active state

**`ye2026multistatebias` is the paper that asks our question, on our receptor, with
a state readout — and it answers against the competing explanation.** Design,
verbatim (p.15):

> "As controls, we also generated **uniformly random sub-MSAs of depth 10 (U10) and
> 100 (U100)** to test whether evolutionary structure in the clusters, as opposed to
> simple MSA depth reduction, drives any observed conformational shift."

Result, verbatim:

> "These results indicate that **MSA-level manipulation alone, whether through
> evolutionary clustering or random subsampling, is largely insufficient to
> overcome the systematic conformational bias** observed across the deep learning
> tools evaluated in this study."

And the contrast on the same receptor (p.13):

> "For β2AR, providing the agonist together with the heterotrimeric G protein
> **shifted predictions toward the expected active conformation across
> predictors**"

The β2AR subsampling evidence is drawn — Fig 5A-B,D (p.16), AF-Cluster vs U10 vs
U100 on paired-reference RMSD axes, references 9CHU (inactive) / 8GEG (active).

**Corpus-wide, lit's answer is categorical on both halves:**

- *"No paper reports getting active-state GPCRs out of shallow-MSA sampling with no
  transducer. The nearest attempt (`ye2026multistatebias`) reports the opposite, on
  β2AR."*
- *"No paper crosses MSA depth with a supplied partner chain and reads out receptor
  state."* The one crossing that exists — `mitjavila2026afsample2t`, masking
  0/10/20/30 % × receptor state, **250 structures per cell, balanced** [p.8] —
  **reads out binding-site RMSD, not activation state**, and its "partner" axis is
  the *input* state of the receptor construct rather than a supplied partner chain
  whose effect is measured. **The crossing exists; the state result does not.**

Only 4 of 83 papers carry both `gpcr` and `msa-subsample`: `chiesa2025templatebias`
(subsamples inside 2 of 6 protocols; its own finding is that the partner beats the
operator handles), `mitjavila2026afsample2t`, `vo2026fiducials` (subsampling only in
a benchmark sweep, 16:32 → 256:512, receptor states `NOT APPLICABLE`), and
`ye2026multistatebias`.

### Two caveats that must be carried, because a referee will

1. **`ye2026multistatebias` is not a clean within-model comparison.** Its note
   records `input_factor_design: NOT CROSSED, and the two legs live in different
   models` — **the AF-Cluster/U10/U100 arm runs on AlphaFold2** while the co-input
   arms run on AF3 / Boltz-2 / Chai-1 / BioEmu. So *"subsampling fails and partners
   work"* is confounded with *"AF2 fails and AF3-lineage works"*. Same structural
   defect as `xing2025purified`, whose two legs also sit in different models.
   **This is precisely the confound our G5 would remove**, because our depth arm and
   our partner arm would run in the same model, on the same panel, with matched
   seeds. It is the single strongest scientific argument for spending on the cube.
2. **One backbone reaches both states on apo β2AR with no manipulation at all.**
   *"Chai-1 identifies clusters within both conformations without any constraints"*
   (p.10). That is default sampling, not subsampling — but it means **apo
   bistability is real on at least one backbone**, and it connects directly to our
   own per-backbone apo floor (`RUN_MATRIX.md:675-680`: ADRB2 apo is **1.00** on
   Chai-1 and **0.00** on Boltz-2, reproduced across three corpora). A shallow-MSA
   effect on Chai is measured on top of a backbone that is already bistable there,
   which is the likeliest explanation for Chai's flat, CI-crossing depth slope in
   §3.2.

### And our own Block D is consistent with the field, not anomalous

Block D measured the competing explanation's effect size on our panel, our
predicate, our backbones: **+12–16 points of apo predicate-active on three of four
backbones** (§3.2). Read next to the corpus, three things fall into place:

- **The published shape is non-monotone with an interior optimum**, and this is
  settled across three papers. `kalakoti2025afsample2` establishes a *"non-monotonic
  optimum"* and locates the break — *"Beyond 30 % masking, performance drops"*.
  `mitjavila2026afsample2t`'s 0/10/20/30/50 % sweep *"rules out a monotonic 'more
  masking is better' reading — 50 % collapses"*. `kalakoti2026afsample3` finds the
  optimum is **protein specific** (*"as observed in previous studies, the optimal
  level of MSA randomization is protein specific"*), and 40 % for AF3.
  `li2026embedding` finds the floor — all methods collapse at 0 % MSA, 25 % still
  works.
- **So our two-mechanism result (lever on Boltz, degradation on OF3/Protenix) is
  the field's expected shape, not an anomaly.** Say that explicitly. It reframes
  §3.3 from *"our data are messy"* to *"we located, per backbone, where the known
  non-monotone response crosses from steering into collapse — and we did it with a
  geometry-fidelity criterion nobody else applied."*
- **And it has a direct design consequence**: a three-level depth arm
  {8, 128, `default`} cannot see an interior optimum. See Option E in §9.

### The published noise-not-signal warning

`schafer2025confounds` rebuts AF-Cluster, verbatim: *"AF-cluster mistakes some
single-folding KaiB homologs for fold switchers, **a critical flaw bound to mislead
users**"* (p.1); *"neither CF-random nor AF-cluster predicts fold switching
reliably"* (p.5). **A method that produces a second state for a protein that does
not have one** is the exact failure our own GATE-3 found in a different vocabulary
(§3.3): a predicate satisfied by a conformation that is not the reference state.

`waymentsteele2025reply` answers with **the control we should copy: column
shuffling destroys the state-specific predictions**, so local coevolution — not
depth alone — carries the signal. That is the direct analogue of our
scrambled-partner arm, applied to the alignment, and it is the cheapest available
test of whether an observed shift is information or noise. See §9, Option Z2.

## 5.2 The plain answer

**G5a as specified is a control against the *depth* explanation, and it is
well-constructed for that. It is not a control against the MSA-manipulation family
as a whole, and it does not currently carry the readout that decides whether a
"shallow-MSA active" and a "partner-driven active" are the same object.**

Three parts, separately.

**(a) The factorial does contain the control.** G5a's `(depth=8, R0, no ligand)` vs
`(depth=default, R0, no ligand)` cells are the competing explanation, measured on
the ligand-complete panel; `(default, R7_full, none)` vs `(default, R0, none)` is
the headline. Comparing those two differences — and the interaction — is exactly
the control. Both endpoints are present in G5a. *(Note a tension: `CATALOGUE.md:1324-1329`
advises **against** crossing depth with apo and cognate, on the grounds that both
are pinned — apo 0.158, cognate 0.891 — and recommends the middle rungs for
headroom. That advice optimises for **estimating an interaction**. The control
question needs the pinned endpoints. G5a includes R0, R3_ct21 **and** R7_full, so
it satisfies both; but the two documents give opposite advice and neither cites the
other.)*

**(b) It tests one of FOUR MSA manipulation families.** The frozen subsampler is
**uniform random depth reduction** (`subsample_msa.py:104-117`, §1.2). From lit's
answer, the corpus's families are:

| family | what is manipulated | corpus exemplars | depths/rates actually used |
|---|---|---|---|
| **random depth subsampling** | how many rows | `ye2026multistatebias` (U10/U100), `schafer2025confounds` (max-seq 1, 8), `suzuki2026conforflux` ({2,4,8,16,32,64,128}), `vo2026fiducials` (16:32→256:512) | **this is ours** |
| **clustering** | which rows, by sequence similarity | `waymentsteele2024cluster` (DBSCAN on edit distance), `bryant2024cfold` (8 cluster sizes 16→5120), `cheng2026af3cluster` | not tested by us |
| **composition purification** | which rows, by "sequence purity" | `xing2025purified` — explicitly *"not depth"* | not tested by us |
| **column masking** | which *positions*, not which rows | `kalakoti2025afsample2` (0–50 % swept), `kalakoti2026afsample3` (40 % optimal for AF3), `mitjavila2026afsample2t` (targeted at the orthosteric pocket), `jung2026boltzperturb` (rate 0.1) | not tested by us |

**Column masking is a separate family and must be named separately** — it is what
the only `factors-crossed` paper in the corpus does, and it is the family where the
non-monotone optimum was established. A referee whose competing explanation is
AF-Cluster- or masking-shaped is not answered by G5. **Say so in the paper rather
than letting "we varied MSA depth" stand in for "we controlled for MSA
manipulation."** Adding a clustering or masking arm is not proposed here; bounding
the claim is free.

*Two corrections that travel with this table.* **`heo2022multistate` is NOT a
subsampling paper** — it carries `msa-state-filter`, and its protocol is
state-annotated templates **plus total MSA deletion applied together**, a confound
by construction. Do not cite it as subsampling anywhere. And **no paper reports a
SUBSAMPLING DEPTH in Neff units**: every depth above is a raw sequence count, a
ColabFold `cluster:extra` pair, or a masking percentage. **If we want Neff on our
own rows we must compute it ourselves**, and there is no published comparator to
put it beside — which is an argument for reporting raw row counts as the primary
depth unit and Neff, if at all, as a secondary column.

> **CORRECTED 2026-09-12 by lit.** This paragraph previously read *"no Neff figure
> exists anywhere in the corpus."* That was wrong. Neff appears in two notes —
> `abramson2024af3` Extended Data Fig 7A [p.18] ("Single-chain LDDT against MSA
> depth (median per-residue Neff)", 10^0-10^4 log axis) and `suzuki2026pairscaling`
> Fig 7 [p.10] ("MSA depth and Neff for every target"). **Both plot Neff as a
> descriptive property of a NATURAL alignment; neither manipulates it.** The
> abramson note flags this explicitly — it plots accuracy against *natural* Neff,
> *not interventional*. So the operative claim is unchanged in consequence and
> narrower in statement: Neff is never a manipulated variable in this corpus.

**(c) The readout is under-specified, and this is the fixable part.** §3.3 is the
whole point: at shallow depth, **only 42.9 % of OF3's predicate-active samples and
68.3 % of Protenix's are within 1 Å of the deposited active pocket, against 88.7 %
for Boltz.** If the partner arm's predicate-actives are ~90 % sub-Å and the
shallow-apo ones are ~43 %, then "shallow MSA also produces active calls" is
**not** a competing explanation — it produces a *different object* that trips the
same two distances, and that is a far stronger result than an effect-size
comparison.

**To claim that, the fidelity stratification has to be a pre-registered readout on
every G5 row.** It is not. `redo/inputs/g1_recording_spec.tsv` has 47 columns
(counted from the body, not the header) and carries `axis_npxxy`, `axis_tm6`,
`state_call`, `worse_reference_res`, `plddt_partner_chain_mean`, `plddt_ga_alpha5`,
`ras_domain_ca_rmsd_to_R7` — **and no pocket-Cα-RMSD-to-active/inactive column at
all.** The exact quantity GATE-3 used to overturn the D3 headline is absent from the
redo's recording contract. See §7.

---

# 6. What "subsampling" means when the four backbones disagree about what an MSA is

## 6.1 A depth is not one number once there are two chains

For a single chain there is one alignment and one depth. For receptor + partner
there are **four** quantities, and D3 never had to name any of them because it was
apo-only:

| # | quantity | who sets it | frozen-campaign status |
|---|---|---|---|
| 1 | receptor **unpaired** depth | the subsampler | the only one D3 varied |
| 2 | partner **unpaired** depth | the partner's own search | measured once, off-GPU, in `R/rung_msa_depth.csv` (§2) |
| 3 | **paired** depth | the server (Boltz, Protenix) or the query flag (OF3) | **never measured, by anyone** (`MAP_MSA.md:696-701`, Q2) |
| 4 | is paired a **copy** of unpaired? | `propose.py:471-472` / `:599-600` | **yes, silently**, whenever a plain string is passed |

An arm labelled "depth 8" can mean any of: receptor-8 + partner-full + paired-full;
receptor-8 + partner-1 + paired-degenerate; or, on the D3 code path in two-chain
mode, receptor-8 + partner-**inherits-the-receptor's-alignment** + paired = the same
file again. **All three would carry the same rung label and produce the same
`ok: true`.**

## 6.2 The per-chain mapping defect `paper_af3` found

`MSA_SPEC.md:74-93`, verified against source:

| backbone | line | key |
|---|---|---|
| OpenFold-3 | `propose.py:462` | `msa_a3m_path.get(cid)`, `cid = chain["chain_ids"][0]` — **chain ID** |
| Protenix | `propose.py:595` | `msa_a3m_path.get(protein_idx)`, a 0-based counter — **integer position** |

So a caller passing `{"A": receptor_a3m, "B": ""}` works on OF3 and **fails silently
on Protenix**: `.get("A")` against a `{0:…, 1:…}` dict returns `None`, hits
`if not path: continue`, sets **no MSA at all**, and Protenix falls through to its
launcher default — **a live server fetch, full depth on both chains**, invisible in
every status JSON. And §1.3 shows Protenix's status JSON would *assert*
`msa_server_mode: 'protenix'` either way, because it is a hardcoded literal.

**The inverse of the intended design, reached through the mechanism the design
proposes, with a status file that says it worked.** `MSA_SPEC.md:93` is right that
§6's first check (assert observed partner depth == 1) is what catches it — which is
the argument for the observed-depth column being non-optional.

Boltz has the per-chain dict form (`propose.py:358-360`, commented "D3 multi-chain
support, currently unused") and **no caller uses it** (`MAP_MSA.md:480`).

## 6.3 Chai is a different operation, and its cache key is a trap

`MAP_MSA.md:131-165`: Chai does **not** pair. Three independent lines of evidence,
two from code, one measured — `generate_colabfold_msas(protein_seqs=[seq], …)`, a
one-element list (`build_chai_msa_cache.py:118-124`); the cache is deduplicated by
sequence hash **across the whole project** (`:77-81`); and `pairing_key` is
empty-string on every row of all 120 cache files
(`msa_depth_report.md:56-68`). **The receptor's MSA is byte-identical between the
apo and the cognate run.**

Consequence for subsampling, and it is operational: **Chai resolves an alignment by
`sha256(sequence.upper())` inside `--msa-directory`** (`rerun_chai.sh:167`). The
receptor sequence is the same at depth 8 and at full, so **the same key must resolve
to two different files.** The only way to do that is **one directory per depth arm**
(per depth × draw × receptor). D3 did this implicitly because
`msa_a3m_path_for()` returns a path per (receptor, depth, seed). Any new depth work
must keep it, and a two-chain depth arm needs the partner's `.pqt` written into the
*same* directory. A flat shared cache silently serves the wrong depth.

Also: on Chai, absent and query-only are **behaviourally identical** — chai-lab
0.6.1 `data/dataset/msas/load.py:47-58`, `if not path.is_file()` returns
`MSAContext.create_single_seq()`, no fetch (`MSA_SPEC.md:129-137`). The explicit
`.pqt` buys **verifiability, not different behaviour**. And that fallback path
**has never fired in a real campaign** — the launcher pre-checks every chain's
`.pqt` and refuses to launch without it, so it is dormant code.

## 6.4 The consequence for the ladder, and the honest framing

`MAP_MSA.md:616-639` (§10) is the piece to carry into any design discussion:

- **Depth is not monotone in length.** From the Chai cache: a 21-mer (endothelin1)
  retrieves **732** rows; a 33-mer (gcn4) **224**; a 40-mer (`random_helix_40mer`)
  **one**; a 41-mer (`arrestin_Ctail`, an excised natural fragment) **one**; a
  15-mer (`arrestin_FL`) **84**. The predictor is not length — it is **whether the
  sequence is natural with homologs in UniRef/BFD**. An α5-CT fragment excised from
  Gα is exactly the `arrestin_Ctail` case.
- **A depth-1 partner makes the paired MSA degenerate.** Pairing needs homologs on
  both sides. So "paired" and "unpaired" **converge as partner length falls**, and
  the apo→cognate operational difference on Boltz/OF3/Protenix **shrinks toward
  Chai's**. A length effect and a pairing-mode effect are confounded along our own
  ladder unless the partner regime is pinned.
- **On OF3, a short partner scored as a *ligand* still flips `use_paired_msas`**
  (`propose.py:502-504,524-525`), because the flag counts `molecule_type == PROTEIN`
  chains, not partner chains. **Our R0 rung and our R1_ct11 rung are not
  "partner absent vs partner present" in OF3's alignment machinery** unless the
  chain's `molecule_type` is controlled deliberately.

**So `MSA_SPEC.md`'s query-only proposal is not a fussy detail — it is the only way
to make the ladder's rungs comparable at all.** But it has a real cost that no
document states: at R7_full it runs a complete Gα with a depth-1 alignment, removing
the coevolutionary pairing signal from the arm that carries the headline. **That is
the reason G17 (partner MSA on/off) is not optional**, and why Gap 5 in §4.2 is the
most consequential of the five.

---

# 7. What must be RECORDED, so this is never unknowable again

F-6 is the failure to design against: **no MSA metadata reaches any scored row, for
any of 42,180 predictions** (§1.3). Two concrete costs, today: the D1/D3 anchor
conflict (§3.4) could not be resolved from the rows, and every D3 slope is fitted
against `full = 4096` when the true top rung may be ~13,700 (§3.2).

`redo/inputs/g1_recording_spec.tsv` carries **47 columns** (counted from the body).
Four are MSA-related:

| col | dtype | status | `why`, as written |
|---|---|---|---|
| `partner_msa_mode` | str | new | "off (primary) / on (E1.9 contrast). SEQUENCES.md 6.1" |
| `partner_msa_depth` | int | new | "the ladder is uninterpretable without it: a 21-aa conserved query pulled 732 homologs in this project's own cache while a designed 40-mer pulled 1" |
| `partner_msa_depth_uniref90` | int | new | *(blank)* |
| `receptor_msa_depth` | int | exists | "on in Group 1 everywhere; varying it is Group 8" |

## Are those four sufficient? **No. They are necessary and about half of what is needed.**

They are the right instinct and they close the Group 1 ladder question. They do not
close Group 8, and they do not close the two failures that actually shipped.

**Missing — MSA side (would have prevented §3.4 and the `full = 4096` problem):**

1. **`receptor_msa_depth_realised` vs `receptor_msa_depth_target`, as two columns.**
   §1.2's silent no-op means a rung label is not a depth. `CATALOGUE.md:1124-1127`
   says this in the same words: *"a rung label is a design fact; a depth is a
   measurement, and a regression needs the measurement."* One column cannot be both.
2. **A definition of what `depth` counts.** Does it include the query row?
   `R/rung_msa_depth.csv` says 0 for `ct11`; the Chai cache says 1 for an 11-mer.
   `MSA_SPEC.md:151`'s verification asserts `== 1`. **Two of those three conventions
   make that check fire on correct rows.** One sentence in the spec.
3. **`receptor_msa_sha256` and `partner_msa_sha256`** — the alignment file actually
   consumed. `RUN_MATRIX.md:631-636` asks for exactly this
   (*"hashing costs nothing and makes this class of drift impossible to ship again"*)
   and it is not in the 47 columns.
4. **`msa_paired_depth` and `msa_paired_is_copy_of_unpaired`** (bool). §6.1 #3 and
   #4. Nobody has ever measured a paired depth, and `propose.py:471-472` / `:599-600`
   will make the paired file a copy without raising.
5. **`msa_source`** — `live-colabfold` / `live-protenix` / `prefetched` / `cache`.
   §1.3 shows two of four launchers currently assert this as a hardcoded literal.
   Derive it from the env var actually set, as OF3 already does
   (`rerun_of3.sh:244`), never from a literal.
6. **`msa_subsample_draw_id` and `msa_subsample_seed`**, distinct from the prediction
   seed. D3 shared one seed stream (§1.2) — that is the defect `P3b` exists to
   measure, and P3b cannot be analysed without a draw id on the row.
7. **`msa_mode_label`** with `default` and `full` as **distinct** values, never
   collapsed. §3.4 is what happens when they are not.

**Missing — readout side, and this one decides the paper's claim (§5.2c):**

8. **`pocket_ca_rmsd_active` and `pocket_ca_rmsd_inactive`.** GATE-3's entire
   LEVER/DEGRADATION verdict is `frac_pred_that_are_subA` = the fraction of
   predicate-active samples with `pocket_ca_rmsd_active < 1.0 Å`
   (`GATE_3:33-34,80-101`). **Neither column is in the 47.** Without them, a G5 row
   can say *active by predicate* and cannot say *active like the crystal*, and the
   competing-explanation control in §5.2c is unavailable — post hoc, from
   structures, at best.
9. **`n_ca_resolved` and a global `ca_rmsd_to_matched_default_depth_row`.** GATE-3's
   (d) analysis — matched (receptor, backbone, seed, sample) 7TM Cα RMSD full vs
   depth-N — is what produced the 15–20 Å Protenix signature (`GATE_3:120-144`). It
   required matched seeds across depth arms. `g1_recording_spec.tsv`'s `seed` entry
   already says *"Pair seeds across arms within a cell or no within-seed contrast is
   readable"* — **that rule must extend across depth arms, not only partner arms.**

**Also worth stating, since GATE-3 is the precedent:** every derived table must
print its own **n**. §3.3's denominator finding is a 24-vs-26-receptor subset that
a reader cannot see because one table states n and the next does not.

## And the checks, each proved by planting its defect

Following `README.md` rule 4 and `MSA_SPEC.md:145-178`:

- `receptor_msa_depth_realised <= target` on every subsampled row, and
  `== target` unless `receptor_msa_depth_at_full < target` (the §1.2 no-op) —
  in which case a dedicated `msa_target_unreached` flag must be **true**, not silent.
- `partner_msa_depth == <the agreed query-only value>` on every ladder row.
  **Plant a row with the partner's real alignment; the check must fail.** This is
  the check that catches §6.2's Protenix key mismatch.
- `receptor_msa_sha256` is **identical** between a ladder row and its matched apo row
  at the same depth. Plant a subsampled receptor MSA; the check must fail.
- **A missing column is a FAILURE, not a skip.** `CLAUDE.md` on
  `redo/gates/run_receipt.py`: *"a check that quietly does nothing when its input is
  absent is the defect it exists to catch."* An MSA check that skips when
  `receptor_msa_depth_realised` is null is the exact shape of F-6 recurring.

---

# 8. Where we stand versus the frozen paper

| | **frozen campaign (Blocks A–D)** | **redo as currently specified** | **what changes, and why** |
|---|---|---|---|
| subsampling in the main arms | **none**, all four backbones (`MAP_MSA.md` §2–§5) | none in Group 1; depth is a crossed factor in G5 only | depth stops being an isolated tier and becomes a factor crossed with the headline |
| depth ladder | D3 only: 8/32/128/512/full, **apo only, no ligand** (`build_tier_d3_manifest.py:60,237`) | G5a 8/128/`default` × 3 rungs × 2 ligands; G5b adds 32/512 | **the crossing** — depth × partner × ligand, unoccupied in 81 corpus papers (`RUN_MATRIX.md:577-587`) |
| the top rung | `full` ≠ `default`; 12 of 28 cells disagree with D1 (`PARTA_D3.md:128`) | **P3**, 600 preds, runs both on the same receptors and seeds | anchors the ladder's origin instead of inheriting a drift |
| draw variance | draw seed == prediction seed; inseparable | **P3b**, 900 preds, 3 draws at depth 32 | separates draw-variance from seed-variance; every depth interval today conflates them |
| partner alignment | whatever the server returned; 0 rows at ct11, 459 at ct15 for Gs alone (§2) | `MSA_SPEC.md`: query-only depth-1 at **every** rung, all four backbones | removes a confound that looks exactly like the effect: a monotone trend along the ladder is what a pairing artefact looks like |
| pairing | on for Boltz/OF3/Protenix, off for Chai; never measured | still unmeasured; `MSA_SPEC.md:95-106` requires the paired slot be **declared**, not inherited | `propose.py:471-472`/`:599-600` put one file in both slots silently |
| MSA provenance | live third-party servers, 3 of 4 backbones; not frozen, not recorded (`MAP_MSA.md:536-539`) | not yet decided — `MAP_MSA.md:739-745` recommends pre-fetch + hash | **a re-run today requests new alignments, it does not re-read ours** |
| recorded per row | **nothing** (F-6) | 4 MSA columns of 47 | §7: necessary, ~half sufficient; the fidelity columns are absent |
| readout | predicate only in the rows; fidelity computed post hoc in GATE-3 on a 24-receptor subset | predicate columns only | §5.2c: the fidelity stratification is what makes depth a *control* rather than a comparison |
| claim form | "MSA depth moves the predicate, by two different mechanisms" — **written, scoped** (`CLAIMS.md:26`) | not yet stated | must remain a **conditional lever** (`GATE_3:235-240`); Chai's slope does not survive its CI |

---

# 9. Options, with costs

Currency: **predictions**, and **paralog clusters** where power is involved, per
`redo/build/matrix_cost.py`. Reference points: MINIMAL = **45,860**; one Block-B
drop = **32,000**; the whole A–D campaign = **124,470**. The measured apo throughput
is 22.67 s/pred/H100 (158.8 preds/H100-h); a two-chain prediction is estimated at
2.0×–13.2× that and **the bracket is unclosed** (`matrix_cost.py:16-24`) — so
wall-clock figures below use the 4.2× pairformer-L² midpoint and are estimates.

**Option Z — the zero-GPU item, and it belongs in every option below.**

| | |
|---|---|
| cost | **0 predictions**, ~200–400 server queries |
| what | Extend `R/rung_msa_depth.csv` to (a) the **receptor** side on CORE-L17 and (b) the **paired** query for each (receptor, rung) pair. Record row counts only. |
| why | `MAP_MSA.md:641-647`: *"the code cannot tell us whether alignment quality varies along the ladder. Only a measurement can."* And §6.1 #3: a paired depth has **never been measured by anyone**. The tooling exists — `B/scripts/msa_prewarm.py:126-165` and `build_chai_msa_cache.py:107-155`. |
| risk of skipping | We commit GPU to a ladder half of which may be single-sequence in practice, and to depth arms whose paired axis we cannot interpret. |

**Option Z2 — the column-shuffle control, added on lit's recommendation.**

| | |
|---|---|
| cost | **+2 cells per depth arm**, i.e. a third level on the depth factor rather than a new factor |
| what | At one shallow depth, add an arm whose alignment has the **same number of rows but shuffled columns**, destroying local coevolution while holding depth exactly constant. |
| why | `waymentsteele2025reply`: *"column shuffling destroys the state-specific predictions"*, so local coevolution rather than depth alone carries the signal. It is the **direct analogue of our scrambled-partner arm** — the same logic we already use on the α5 sequence, applied to the alignment — and it is the cheapest published test of whether an observed shift is information or noise. It is also the control `schafer2025confounds` says AF-Cluster lacked. |
| size, if run as a G5 level | replacing nothing: 17 receptors × 4 bb × (1 extra depth level × 3 rungs × 2 ligands) × 10 = **4,080**. Restricted to the apo, no-ligand rung only: 17 × 4 × 1 × 10 = **680**. |
| my read | **The 680-prediction version is the buy.** It sits exactly where the competing explanation lives (shallow depth, apo, no ligand) and it converts "shallow MSA also produces active calls" from an effect size into a mechanism statement. It is not in `matrix_cost.py` and would need adding. |

---

### Option A — Anchor only. Do not cross depth with anything.

| | |
|---|---|
| items | P3 + P3b |
| cost | **1,500** predictions (1.2 % of A–D; 3.3 % of MINIMAL) |
| Boltz-only as specified | 600 + 900 |
| all-four-backbone variant | **6,000** (2,400 + 3,600), +4,500 — closes Gap 2 |
| delivers | The ladder's origin is defined; draw-variance is separated from seed-variance; D3's slopes become quotable against a known anchor. |
| does **not** deliver | Any answer to the competing explanation. Depth stays a Block-D-only, apo-only result. |
| the sentence it buys | "We re-anchored Block D's depth ladder and confirmed/measured the drift." A methods sentence, not a result. |
| when this is right | If the redo's scope is the **length ladder** and depth is deliberately out of scope. Then say so in the paper, and bound the claim per §5.2b. |

### Option B — the pilot, then decide. *(defers the decision one step)*

| | |
|---|---|
| items | P3 + P3b + **P2** (depth × rung × ligand cube pilot, Boltz-2 only, 2 depths × 3 rungs × 2 ligands, CORE-L17, n=10) |
| cost | **3,540** predictions (2.8 % of A–D; 7.7 % of MINIMAL) |
| all-four-backbone anchor variant | **8,040** |
| delivers | The first two-chain depth cell ever run on this project, on one backbone. Closes the §6 unknowns empirically — does the per-chain dict work on each backbone, what does a paired depth look like with a depth-1 partner, does the cube's effect size on Boltz match D3's +12.7 points. |
| does **not** deliver | A publishable control. n=10 × 17 receptors = 170/cell pooled, one backbone. |
| when this is right | If Gaps 1, 3 and 4 (§4.2) are unresolved and you want them resolved by measurement rather than by argument before spending 12,240. **P2 is already in all three budget tiers**, so this is not a new commitment. |

### Option C — MINIMAL as specified: the depth cube at G5a.

| | |
|---|---|
| items | P3 + P3b + P2 + **G5a** |
| cost | **15,780** predictions (12.7 % of A–D; **34.4 % of MINIMAL**; 0.49 Block-B drops) |
| est. wall | ~1,850 H100-h at 4.2× ≈ **3.1 days on 25 H100** |
| all-four-backbone anchor variant | **20,280** |
| panel / power | CORE-L17, **17 receptors = 17 clusters**. Main effects detectable at ≈0.13–0.16, small steps ≈0.06 (`RUN_MATRIX.md:495-496`). **Interaction MDE 0.295** (`:517`). |
| delivers | The unoccupied crossing. Depth × partner × ligand, four backbones, 18 cells/receptor. A direct effect-size comparison between the competing explanation and the headline, on one panel with matched seeds. |
| caveat to state in advance | An interaction below 0.30 is reported as **unestimable at this n**, never as absent (`RUN_MATRIX.md:521-525`). |
| gaps it does not close on its own | Gap 1 (G5 not enumerated), Gap 3 (levels undefined), Gap 4 (partner regime unreconciled), Gap 5 (no G17 in any tier), and §5.2c (no fidelity columns) — **five items, all specification work, zero compute.** Gap 2 (+4,500) and Gap 5a (+300) are the two that cost predictions. |

### Option D — Option C, plus the residual arm that a referee will ask for.

| | |
|---|---|
| items | P3 + P3b + P2 + G5a + **G17a** (partner MSA on/off, pooled, 30 receptors × 4 bb × 3 arms × n=10) |
| cost | **19,380** predictions (15.6 % of A–D; **42.3 % of MINIMAL**) — G17a adds **3,600** |
| all-four-backbone anchor variant | **23,880** |
| why | `MSA_SPEC.md:198` — *"Wanted anyway, on top of the primary. It answers 'how much did we change by doing that?', which is the first question a referee asks."* §6.4: query-only at R7_full removes the coevolutionary pairing from the arm carrying the headline. G17 is the only arm that bounds what that cost. It is **costed and in no budget tier** (Gap 5). |
| G17b instead | per-cell n=50, **18,000** → total **33,780**. Almost certainly not worth it at this stage; the contrast is binary and pooled n=1,200/arm is ample. |

### Option E — Expansive: the five-depth cube.

| | |
|---|---|
| items | P3 + P3b + P2 + **G5b** (+ optionally G17a) |
| cost | **23,940** (52.2 % of MINIMAL), or **27,540** with G17a |
| what the extra 8,160 buys | Depths 32 and 512. From §3.2: **32 and 512 are where the shape lives.** Protenix is 16.77 % at 32 and 2.08 % at 512 — non-monotone at 32, collapsing between 128 and full. `GATE_2_D3_SLOPES.md:118-120` explicitly does not settle whether the response is linear in `ln(depth)` and notes Chai looks saturating. **With only {8, 128, default}, a curve cannot be distinguished from a line.** |
| **the corpus argument, added 2026-09-12** | Lit's answer makes this stronger than it looked. **The published shape is non-monotone with an interior optimum, established independently three times** (`kalakoti2025afsample2` — *"beyond 30 % masking, performance drops"*; `mitjavila2026afsample2t` — *"50 % collapses"*; `kalakoti2026afsample3` — the optimum is *"protein specific"*), with a floor at 0 % MSA (`li2026embedding`). **A three-level arm is specified in a shape the field has already ruled out.** If we report a slope from {8, 128, default} we are fitting a line through a curve whose turning point the literature says exists and is target-dependent. |
| when this is right | If the paper wants a **dose–response** on depth rather than a two-point contrast — and the corpus now says a two-point contrast is the wrong instrument for this response. If depth is purely a control (is the partner effect bigger than the depth effect?) three levels suffice and Option C is the better buy. |

---

## What I would put in front of the decision, stated as trade-offs not a pick

- **Option Z is free and nothing argues against it.** It is the only item here that
  can change the *design* rather than the interpretation, and `MAP_MSA.md:750-753`
  already recommends it.
- **The specification gaps are worth more than the marginal compute.** Gap 1 (G5 is
  not enumerated), Gap 3 (levels undefined), the missing fidelity columns (§7 #8),
  and the paired/unpaired declaration (§6.1) cost **zero predictions** and decide
  whether the 12,240 of Option C is interpretable. The gap between Option A and
  Option C is 14,280 predictions; the gap between a G5 that can answer §5.2c and one
  that cannot is a handful of columns.
- **Gap 2 is the cheapest real upgrade.** +4,500 predictions (9.8 % of MINIMAL)
  extends the anchor and the draw probe from Boltz to all four backbones — and OF3
  and Protenix are where the slopes are largest and the mechanism is worst
  understood. A Boltz-only anchor on a four-backbone claim is a `compare-like-with-like`
  problem waiting to happen.
- **The choice between A and C is a choice about what the paper claims**, not a
  budget question. If depth is out of scope, Option A + an explicit scope sentence
  is honest and cheap. If the paper says the α5 co-input drives the active state,
  a referee who knows `ye2026multistatebias` will ask what shallow MSA does on the
  same panel — and we will either have measured it (C/D) or be citing Block D's
  apo-only, differently-anchored answer.
- **Lit's answer changes the case for C in one specific way, and it is the strongest
  single argument in this document.** `ye2026multistatebias` already reports that
  subsampling does not reach the active state on β2AR while the partner does — but
  **its two legs live in different models** (AF2 for subsampling, AF3-lineage for the
  co-input), so *"subsampling fails, partners work"* is confounded with *"AF2 fails,
  AF3-lineage works"*. `xing2025purified` has the same defect. **G5 removes that
  confound**: same model, same panel, matched seeds, both legs. That is not a
  robustness upgrade — it is a publishable correction of the corpus's best existing
  answer to our own competing explanation, and it is what makes the crossing
  *"OPEN"* in `CATALOGUE.md:1350` rather than merely unrun.
- **Two cheap additions are now better supported than parts of the specified
  design**: the column-shuffle control (Option Z2, 680 predictions at the apo
  shallow cell) and the seeds-only cell (Gap 5a, 300 predictions). Together **980
  predictions, 2.1 % of MINIMAL**, and each answers a question a published paper
  has already shown matters.

---

# 10. Checked and NOT a finding

- **"GATE-3 and GATE-2 report different predicate-active percentages."** They do
  not. GATE-2 `:38-43` and GATE-3 `:37-62` agree to two decimals on all 20 cells.
  The 1–2 point difference is *inside GATE-3*, between its population table and its
  fidelity table, and is a denominator difference of ~100 rows per cell with an
  identical numerator (§3.3). Recomputed all 20 cells before writing it up.
- **"`MSA_SPEC.md` overstates the ct15 single-sequence problem."** It does not.
  Recounted from the body of `R/rung_msa_depth.csv`: exactly 5 of 16 families at 0,
  ten more at ≤ 42, Gs at 459. Every figure in `MSA_SPEC.md:32` checks out.
  (The R6a/R7 range in `:35` does **not** — §2 — but that is a separate number.)
- **"G5a's 18 cells/receptor doesn't match 3 depths × 3 rungs × 2 ligands."**
  It does: `matrix_cost.py:128` is literally `3*3*2`, and 17 × 4 × 18 × 10 = 12,240,
  matching `RUN_MATRIX.md:656`. Ran the script rather than trusting the table.
- **"The depth ladder used 5 seeds, so draw and seed variance are separable."**
  No. `subsample_msa.py:104` uses the prediction seed as the draw seed, so the five
  "seeds" move both at once. This is why P3b is a separate item and not a
  re-analysis. *(I first read the 5-seed design as sufficient; the code says
  otherwise.)*
- **"`full` and `default` are the same condition."** They are not
  (`build_tier_d3_manifest.py:59` vs `:118-120`), and the 28-cell divergence is the
  observable consequence. I checked the comment against the function before
  concluding the comment was the wrong half.
- **"G17a is missing from the cost model."** It is not — `matrix_cost.py:150`,
  3,600 predictions, and `check_against_systems()` confirms it against
  `g1_systems.csv`. It is missing from the **TIERS** dict (`:209-217`), along with
  the other eleven items added 2026-09-12. Different defect, smaller.
- **"`g1_recording_spec.tsv` has 47 columns" — quoted from `README.md:35`
  ("47 generated artefacts"), which is a different 47.** Counted the body of the TSV
  independently: 47 data rows. The two 47s are a coincidence, not a citation.
- **"Chai's cache being deduplicated by sequence hash breaks depth arms."** Only if
  a single flat directory is used. D3 avoided it by returning a per-(receptor,
  depth, seed) path. Recorded in §6.3 as a constraint on any new design, not as a
  defect in what shipped.
- **"`heo2022multistate` is an MSA-subsampling precedent."** It is not — corrected by
  lit, 2026-09-12. `msa-state-filter`; state-annotated templates **plus total MSA
  deletion together**. I had not cited it, but `CLAIMS.md:223` names it as "MSA
  deletion" in the threats evidence line and that is the correct framing; nothing in
  this document should promote it to a depth precedent.
- **"A three-level depth arm is adequate because Block D's response looked
  monotone."** Not established, and the corpus says otherwise — three independent
  papers report a non-monotone optimum (§5.1). Block D's own Protenix column is
  already non-monotone between depth 8 (15.54 %) and 32 (16.77 %). I had initially
  read Option E's extra two depths as a luxury; they are the difference between
  fitting a line and seeing a curve.
- **"`MSA_SPEC.md` §6's `partner_msa_depth == 1` check is wrong."** Not established.
  It is right under the Chai-cache convention and wrong under the
  `rung_msa_depth.csv` convention, and **no document states which convention the
  recorder will use**. Recorded in §2 and §7 #2 as an undefined unit, not as an error.

---

# 11. What I could not determine

Stated plainly rather than filled in.

1. **Whether the fidelity metrics can be emitted per row at all**, or only computed
   post hoc from structures. GATE-3 computed `pocket_ca_rmsd_active` from CIFs on
   HPC (`GATE_3:117-118,175-186`). Whether the delivered scorer can write it as a
   row column is a question for `paper_af3`, not answerable from the bundle.
2. **Why GATE-3's fidelity table drops ~2 receptors per cell.** The arithmetic is
   unambiguous (§3.3) but the reason — a 24-receptor subset by design, or rows
   lacking `pocket_ca_rmsd` — is not stated in the document and Block D shipped no
   rows, so it cannot be checked here.
3. **The two-chain GPU cost.** `matrix_cost.py:16-24` brackets it at 2.0×–13.2× the
   measured apo rate and says the bracket is unclosed (ask P1). Every wall-clock
   number in §9 inherits that uncertainty; the *prediction counts* do not.
4. **Whether CORE-L17 is really 17.** `RUN_MATRIX.md:1050` flags that `PANEL.md`'s
   modality columns show census receptors with `**none**` for antagonist (GPR52,
   MTR1A, MTR1B), so "the true ligand-complete cluster count may be above or below
   17. Every G5/G6 cost scales linearly with it; the interaction MDE scales as 1/√k."
   G5's costs above are therefore **provisional on a panel count that is itself open**.
5. **Whether Boltz requests a paired search from ColabFold or pairs a single
   response itself.** `B/refs/msa_input_interfaces.md:74-76` says the latter; the
   on-disk directory name `pairgreedy-env` suggests the former. `MAP_MSA.md` Q4,
   unresolved, and it is needed for a correct methods sentence.
6. **Whether the redo will pre-fetch and freeze MSAs at all.** `MAP_MSA.md:739-745`
   recommends it strongly; no `redo/spec/` document decides it. Until it is decided,
   §8's "MSA provenance" row stays open and a re-run of our own ladder in six months
   is a different experiment.
7. **Whether any Block A–D prediction ever dispatched a partner shorter than ~120 aa.**
   `MAP_MSA.md` Q3, open. It bears on whether the peptide rungs are novel territory
   for the pipeline or merely undocumented.

---

# 12. ANSWERS FROM LIT — folded in, and what remains open

The questions this document originally ended with were answered by the lit session
on 2026-09-12. **Full text: `lit/analysis_review/MSA_SUBSAMPLING_CORPUS_ANSWERS.md`
(229 lines).** Staleness check run first — zero PDFs without an extraction. Corpus
83 notes / 83 INDEX / 87 bib.

| asked | answered | where it landed in this document |
|---|---|---|
| L1 — what `ye2026multistatebias` actually did on β2AR | **U10 / U100 uniform random sub-MSAs, run explicitly as a control** against clustering; verdict *"largely insufficient"*; partner shifts it. Fig 5A-B,D p.16; refs 9CHU/8GEG | **§5.1**, with both caveats |
| L2 — does any paper get an ACTIVE GPCR from shallow MSA alone? | **No.** *"The nearest attempt (`ye2026multistatebias`) reports the opposite, on β2AR."* Only 4 of 83 carry both `gpcr` and `msa-subsample` | **§5.1**, and it is why the competing explanation is weaker than feared |
| L3 — is `xing2025purified` a failed depth arm? | It is a **composition-purification** paper; depth is the wrong knob *on their evidence*, and its two legs sit in **different models** | **§5.1** caveat 1, **§5.2b** family table |
| L4 — what did `mitjavila2026afsample2t`'s interaction do? | The crossing is real and balanced (250/cell) but **the readout is binding-site RMSD, not activation state**, and its "partner" axis is the input receptor state, not a supplied chain. **The crossing exists; the state result does not** | **§5.1**; strengthens `CATALOGUE.md:1350`'s OPEN |
| L5 — is LEVER-vs-DEGRADATION known? | Adjacent and published: `schafer2025confounds` — *"AF-cluster mistakes some single-folding KaiB homologs for fold switchers, a critical flaw bound to mislead users"* (p.1) | **§5.1**; our GATE-3 finding is the GPCR/state-predicate instance of a known caution |
| L6 — the taxonomy | **Four families, not three** — column masking is separate. And `heo2022multistate` is **not** a subsampling paper | **§5.2b**, rewritten |
| L7 — `suzuki2026conforflux` [p.21] | **Not answered.** Still open below | — |

**Three corrections lit made to what this document had assumed:**

1. **`heo2022multistate` is NOT subsampling.** It carries `msa-state-filter`;
   state-annotated templates **plus** total MSA deletion, applied together — a
   confound by construction. It must not be cited as subsampling anywhere, in this
   document or in the manuscript.
2. **The `msa-subsample` tag fires on 20 of 83, not the handful named in passing.**
   The full list: `bryant2024cfold`, `cheng2026af3cluster`, `chiesa2025templatebias`,
   `feldman2026alphainterp`, `jung2026boltzperturb`, `kalakoti2025afsample2`,
   `kalakoti2026afsample3`, `lee2025seqassoc`, `lee2026foldswitch`,
   `mitjavila2026afsample2t`, `richman2025conformix`, `schafer2025confounds`,
   `suzuki2026conforflux`, `suzuki2026pairscaling`, `swapna2025memorization`,
   `vo2026fiducials`, `waymentsteele2024cluster`, `waymentsteele2025reply`,
   `xing2025purified`, `ye2026multistatebias`.
3. **No published SUBSAMPLING DEPTH is reported in Neff units.** Every published
   depth is a raw count, a `cluster:extra` pair, or a masking percentage. Neff
   itself does appear, in `abramson2024af3` [p.18] and `suzuki2026pairscaling`
   [p.10], but only as a descriptive property of a natural alignment — never as a
   manipulated variable. **This item previously read "no Neff value exists anywhere
   in the corpus", which was wrong; corrected 2026-09-12 by lit.** §5.2b.

## Still open — for lit, or for `paper_af3`

- **L7 (lit).** Does `suzuki2026conforflux` [p.21] actually take the position
  `RUN_MATRIX.md:525` attributes to it — an underpowered interaction reported as
  *unestimable at this n* rather than *absent*? I have that locator second-hand and
  am about to lean on it in a spec.
- **L8 (lit, new).** `schafer2025confounds` says plain random shallow sampling
  matches or beats AF-Cluster **at 1–2 runs versus 95–329**. Does it report a
  *geometric* criterion for calling a second state — anything analogous to our
  sub-Å-to-deposited-reference filter — or only pLDDT and visual inspection?
  *Changes:* whether §5.2c's fidelity stratification has a citable precedent or is
  ours alone, and therefore whether it earns a figure.
- **L9 (lit, new).** `ye2026multistatebias` p.10: *"Chai-1 identifies clusters
  within both conformations without any constraints."* On **apo** β2AR with the
  default MSA? And how many samples? This is the only external observation of apo
  bistability on a backbone we run, and it bears directly on our own apo floor
  (Chai 1.00 / Boltz 0.00 on ADRB2, `RUN_MATRIX.md:675-680`) and on why Chai's depth
  slope crosses zero.
- **Q1–Q6 to `paper_af3`** remain as `MAP_MSA.md:687-728` lists them; **Q2 (paired
  a3m row counts, apo vs cognate, free) is the one this document most needs**, per
  §6.1 #3.

---

## Provenance of this document

Read in full: `CLAUDE.md`, `redo/README.md`, `redo/protocol/MAP_MSA.md`,
`redo/spec/MSA_SPEC.md`, `redo/build/matrix_cost.py`,
`data/block_d/06_gate_reports/GATE_2_D3_SLOPES.md`,
`data/block_d/06_gate_reports/GATE_3_STEERING_VS_DEGRADATION.md`.
`lit/analysis_review/MSA_SUBSAMPLING_CORPUS_ANSWERS.md` (lit session, 2026-09-12,
229 lines, in answer to this document's original QUESTIONS FOR LIT — now §12).
Read in part: `redo/spec/RUN_MATRIX.md` (§4.2–§6.2, §8–§9, the item tables),
`redo/spec/CATALOGUE.md` (Group 8, E1.9, §1.4 context), `CLAIMS.md`, `lit/INDEX.md`.
**Every verbatim quote attributed to a corpus paper in §5 and §12 comes from lit's
answer file, not from a PDF read here** — page locators are theirs.
Recomputed here: `R/rung_msa_depth.csv` (all 112 rows, per-rung), GATE-3's two
predicate-active tables (all 20 cells, implied denominators),
`redo/inputs/g1_recording_spec.tsv` (47 columns, counted from the body),
`redo/inputs/g1_systems.csv` (2,039 rows, distinct `partner_msa`/`receptor_msa`/
`ligand` values), and `python3 redo/build/matrix_cost.py` (all item and tier totals).
Nothing under `redo/inputs/`, `redo/cache/`, `redo/runs/` or `redo/protocol/` was
modified. No git was run. No compute was commissioned.
