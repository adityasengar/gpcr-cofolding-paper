# RESULTS.md — the results ledger

> **PERISHABLE — this file is a snapshot, `CLAIMS.md` is not.**
> Every verdict below is true only for data fingerprint
> `predictions.csv f281aeafe8be67fe (17,569 lines)`. New data will invalidate them.
> Run `python3 analysis/fingerprint.py --check` first; if it reports a change, treat
> every verdict as stale and re-derive with `python3 analysis/q.py`. The durable
> assets are `analysis/q.py` (the queries) and `CLAIMS.md` (the argument) — not the
> numbers on this page.

The counterpart to `lit/INDEX.md`. Every number the manuscript will state about **our
own** experiments gets one entry here, and a draft sentence cites the entry id the way
it cites `[abramson2024af3 p6]`.

**The rule:** a number may enter the manuscript only if it appears below with a
`query:` line that reproduces it. If it is not here, it is not citable yet.

Each entry carries a **verdict**:

| verdict | meaning |
|---|---|
| `VERIFIED` | the query reproduces the number from data in this repo |
| `LOCAL-PARTIAL` | the query runs but the local export is a subset; the number differs from `STATUS.md` |
| `NOT-LOCALLY-CHECKABLE` | the inputs needed are not in this repo (they are on the HPC) |
| `CONTRADICTED` | the local data does not support the claim as written |
| `PLANNED` | the experiment has not run; must not appear in any draft sentence |

**Scope caveat that applies to every entry.** `data/` and `rows_enriched_v3_7.csv`
hold **17,568 predictions**; `STATUS.md` describes roughly 41,500 across the landed
blocks. Every `prediction_path` points at `/hpc/scratch/sengaad1/...`. So this repo is
a partial export, and a number that fails to reproduce here is not thereby wrong — it
is *unverified*, which is a different and weaker statement. Run
`python3 analysis/q.py scope` before trusting anything below.

---

## R-SCOPE — what the local export covers

- **verdict:** VERIFIED
- **numbers:** 17,568 predictions · 92 receptors · 5 backbones (`af2mm boltz chai of3 protenix`) · 15 partner types · 89 experiment clusters · **39.0% of rows carry no `classified_state`**
- **query:** `python3 analysis/q.py scope`
- **provenance:** `data/predictions.csv` sha256[:16] `f281aeafe8be67fe`
- **note:** the 39% unclassified fraction is the most important number on this page. Every rate below is computed on the classified remainder, so every denominator is a subset of a subset.

## R-A-RECEPTORS — "48 receptors" in Block A

- **verdict:** CONTRADICTED (as a reproducible figure)
- **finding:** no definition of "receptor" in the local data yields 48, 46 or 40. Candidates: 92 (appear anywhere), 82 (`in_reference_set`), 83 (in both apo and cognate arms), 44 (`in_state_thresholds`), 43, 30 (run on ≥4 backbones), 28, 15.
- **query:** `python3 analysis/q.py receptor_counts`
- **action:** the denominator has to be *defined* before it is cited. "48 receptors, 4 backbones" is not currently a checkable sentence — and note only **30** receptors are run on ≥4 backbones at all, so the "4 backbones" half needs the same treatment.

## R-B-LADDER — the graded activation ladder

- **verdict:** LOCAL-PARTIAL
- **`STATUS.md` claims:** apo ~16% → decoy ~55% → shuffled ~81% → cognate ~89%
- **local data gives:** apo **11.9%** (n=2,017) · decoy_random_helix **39.5%** (n=43) · shuffled_ga **49.9%** (n=674) · cognate_ga **90.2%** (n=752)
- **query:** `python3 analysis/q.py ladder`
- **reading:** the top of the ladder reproduces well (90.2% vs ~89%) and the bottom is in the right region (11.9% vs ~16%). **The middle does not**: shuffled_ga is 49.9% locally against a claimed ~81%, a 31-point gap. The decoy arm has n=43 locally and cannot support a rate at all. The monotone ordering survives; the specific rungs do not. Do not cite 16/55/81/89 until the full export is here.

## R-INFRA-AA2AR — confidence does not track state correctness

- **verdict:** SPLIT — one clause VERIFIED, one CONTRADICTED, one NOT-LOCALLY-CHECKABLE
- **"Boltz-2 lands ~9 Å at AA2AR"** → VERIFIED. Median `d_tm6` = **9.61 Å** (n=1,598).
- **"with higher pLDDT than OF3/Protenix"** → half CONTRADICTED. Boltz **86.78** vs OF3 **82.52** (holds) but vs Protenix **87.01** (**does not hold — Protenix is higher**).
- **"OF3/Protenix land within 0.6 Å [of active]"** → NOT-LOCALLY-CHECKABLE. AA2AR has `in_state_thresholds = no` and **empty** `ref_pdb_active` / `d_tm6_active`, so `delta_to_active` is null for every AA2AR row. There is no local active reference to measure against.
- **query:** `python3 analysis/q.py aa2ar`
- **confound, and it is serious:** partner mixes differ by backbone — boltz is 735 cognate + 563 ligand, chai is 20 apo only, af2mm is 50 ligand only, of3 is 60 cognate + 40 apo. Cross-backbone medians here compare different conditions. The claim needs a partner-matched subset before it is stated.

## R-B-DECOMPOSITION — occupancy ~54% / α5-CT sequence ~35% / correct family ~11%

- **verdict:** NOT-LOCALLY-CHECKABLE
- **why:** the decomposition needs the decoy and shuffled arms at full n. Locally decoy_random_helix has n=43 and decoy_scaffold n=260.

## R-C-LIGANDCLASS — binary predicate inverted under continuous pocket geometry

- **verdict:** NOT-LOCALLY-CHECKABLE
- **why:** the local export carries `d_tm6`, `d_npxxy`, `d_tm5_out`, `d_dry`, `icl2_helical_frac` but no pocket-geometry columns.

## R-INTERMEDIATE — decoy arm interior fraction ~53.8%

- **verdict:** NOT-LOCALLY-CHECKABLE
- **why:** same decoy-arm n problem as R-B-DECOMPOSITION.

## R-A-OPSD — OPSD/apo/Boltz within 0.40 Å of active crystal

- **verdict:** NOT-LOCALLY-CHECKABLE — needs the active reference; see whether OPSD carries `d_tm6_active` before citing.

## R-A-PREDICATE — two-instrument predicate, 90.5% agreement, 572 disagreements over ~6,000

- **verdict:** NOT-LOCALLY-CHECKABLE — the second instrument's calls are not a column in the local export.

---

## PLANNED — must not appear in any draft sentence

`D1` deep apo sampling (~12,000) · `D2` β2AR Nb60/Nb80 directed-inactive arm (~800–4,800) ·
`D3` MSA-depth tier (~26,000) · `T1.5` redocking. See `STATUS.md`.

If `D2` lands the claim moves from state *selection* to directional conformational
*control*, and `lit/`'s gap paragraph must be rebuilt — the papers worth contrasting
against change.

---

## What would close the gaps

Most entries above are `NOT-LOCALLY-CHECKABLE` for one reason: the scored outputs live
on the HPC and only a 17.5k-row slice came back. Pulling the full scored table — with
`classified_state` populated, the pocket-geometry columns, the second predicate's
calls, and per-receptor active/inactive references — converts most of this page from
unverified to verified in one step.
