# 2026-09-13 → 14 — four decisions enacted, Block D lands, and we find the paper we are arguing against

Orchestrator session. **No compute commissioned; no GPU.** The day's largest artefact is
not a result but a *frame*: there is a published paper claiming the thing this paper does
cannot be done, and it never tried our handle.

## What happened

| | |
|---|---|
| **All four open decisions TAKEN** | chain A at (b), seeds paired, C7 pre-registered, measurement pass authorised — `D-2026-09-13-a` |
| **Block D's three row tables LANDED** | 14,000 / 2,370 / 25,810, by hand, all pins verified. **Every block is row-level now** |
| **Block D's verifier** | **54 testable / 12 prose-only → 86 / 4** |
| **A refutation target found** | `obendorf2026statespecific` — **F-25** |
| **A readout nobody had ever read** | `a100_index`, on every prediction in two blocks |
| **The campaign reference** | `analysis/CAMPAIGN_REFERENCE.md`, generated, both campaigns, every experiment |

## Decisions Aditya made, with their reasons

**All four, together, on the four-item summary** (`D-2026-09-13-a`):

**Chain A at option (b)** — remove the annotated signal peptide *before* the terminal cap.
Mechanical, recorded per receptor, and it removes the fragment case. The argument against
— four of six boundaries are *predicted*, not observed — was put to him and accepted.
**Measured: only 2 of 75 constructs change** (5HT2C 29 signal residues → 0, EDNRA 1 → 0).

**Seed pairing, yes.** Free today, impossible after dispatch. Blocks A and B both failed
it — 1,898 distinct `seed_outer` over 380 cells.

**C7 pre-registered.** Binding *before* dispatch, which is the only state it is worth
anything in. 20 receptors / 19 clusters, already READY, zero marginal predictions.

**The measurement pass authorised** — CPU only. Standing condition intact: it authorises
*our* measurement of structures we hold, not commissioning anything from `paper_af3`.

**And: do not build the redo's MSA work on D3's ladder** — *"we can build a better setup
ourselves."* Correct, and separable from verifying their claims, which is nearly free.

## What the verification found

- **Chain A was adversarially reviewed before wiring, and all four reviewers said DO NOT
  PROCEED.** Eleven defects, three of them mine. Fixed before it touched 2,389 rows.
- **`verify.sh` never ran `seqrec_verify.py`** — it sat at 53/54 while the script printed
  ALL CHECKS PASSED. Now wired in at 60/60.
- **Block D verified on arrival**: row counts exact, every pin uniform, **102 columns not
  the 92 their covering note said** — vindicating the schema we reconstructed from one
  sample row.
- **`a100_index` is reference-free and never read** — `grep -rl a100` returns nothing
  across `analysis/`, `redo/build/`, `redo/gates/`, `figures/`. On it the partner effect
  is **2.7–5.2× the entire 64× MSA-depth sweep on every backbone**. **But r(a100, TM6
  tilt) = +0.846 / +0.764**, against the frozen prereg's own |r| < 0.7 bar — so it breaks
  *reference-set* circularity, not axis independence. Corroborating readout, not a third
  instrument.
- **SC-D-10 is the sharpest thing recomputed**: OPSD × boltz is **38.8% at n=500 and
  10.0% at n=50** — identical inputs, 29 points apart. A measured instance of small n
  giving a *different answer*, not a wider interval.

## What I got wrong and corrected

**Seven, and three were things I told Aditya with confidence.**

1. **"The frozen decoy arm holds MSA depth constant."** False. Chai decoy MSAs are **0/40
   byte-identical** to their parents; gap fraction at the α5-CT columns rises 36% → 47–70%.
   **Our own `CATALOGUE.md` already lists it under "Failed to establish"** and I did not
   check. The redo's `partner_msa = off` is the design that holds the alignment constant
   *by construction* — I had it backwards.
2. **"Instrument critique alone is a Matters Arising, not a paper."** A sample of one,
   misread. **`masters2025physics` is *Nature Communications* 16:8854**, peer-reviewed,
   benchmark-only, **no positive result of any kind**.
3. **"Three dead flag columns."** **Eleven**, on 40,800 rows — and `matches_claim_sheet`,
   which I kept naming, **is not a column in this corpus**; it was Block A's.
4. **"Chain A is a stale label."** It was an untaken decision, and the built artefact was
   the option the spec calls indefensible. Wiring it, as I proposed, would have enacted
   that silently across 2,389 rows.
5. **My comment asserted a check that did not exist** — *"Check S-1 below asserts it never
   does."* There was no S-1 anywhere. Written while fixing another instance of exactly
   that.
6. **The MDE in the pre-registration I wrote** was the *interaction* statistic applied to
   a **main effect**, in binary-predicate units, while §3 declares a continuous axis
   primary. 0.121–0.155, not 0.279. Conservative, so nothing was overclaimed — but wrong,
   in the one document where a power figure must be right.
7. **"30 experiments need triage."** 27. Three were a stale artefact — which became
   **F-21**.

**And four checker bugs before the data was wrong**: the `/pool/` regex on a doubled
segment; a positional path parse when Block D's depth varies by backbone; `float("nan")`
not raising; and `receptor` vs `receptor_slug` — **the identical mistake I had made on the
g4 census two days earlier and written up as a correction.**

## What the next session should not redo

- **Do not re-open the four decisions.** `D-2026-09-13-a`. Chain A is enacted and
  `grep '^## D-OPEN'` returns nothing.
- **Do not build a "three independent instruments" claim on `a100_index`.** r = +0.846.
- **Do not cite "decoy ≈ antagonist"** (F-19) or **the frozen decoy arm as MSA-constant**
  (F-26).
- **Do not re-derive C7 from Block C** — no ligand-free arm exists there (F-23).
- **Do not build a date stratification on any published cutoff without re-deriving it** —
  three of `paper_af3`'s documents give three different sets, all flagged unverified, and
  **OpenFold3 has none** (F-24).
- **Do not ask the working repo about `PARTA_D1` or the Block D claim sheet.** They live
  in the *release* repo and neither side holds them (F-24). Asking the wrong repository is
  not a refusal.
- **The remaining 4 prose-only claims** need the matched-seed pairing, a Kendall-τ table,
  helix/Rg columns, and bootstrap draws `GATE-2` says were never written. Two are probably
  unreachable from our side.
