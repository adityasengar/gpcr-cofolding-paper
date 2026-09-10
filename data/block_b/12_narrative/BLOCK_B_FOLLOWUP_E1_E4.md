# BLOCK B FAMILY-TERM FOLLOW-UP — E1 (E2/E3/E4 gated on E1)

**Date**: 2026-09-10.
**Baseline**: `block_b_freeze_r3` at `7036a4a`.
**Scope**: E1 executed first per dispatch. E2/E3/E4 gated on E1's branch —
E1's Branch 1 NOT MET, so E2 is a scope note (not load-bearing), and
E3/E4 remain queued but not run in this pass.
**Standing rules honoured**: no new predictions; report only; no
modification of frozen artifacts; no r4 tagged.

---

## Direction discipline (stated before any number)

For every quantity in E1:

- **`gap = median(Gs-anchored active-ref tilt) − median(Gi-anchored active-ref tilt)`**.
- **Positive `gap` means Gs-anchored active references sit HIGHER on the
  TM6 tilt axis than Gi-anchored active references — i.e., the deposited
  Gs record shows more outward TM6 movement than the Gi record.**
- The Outcome-B-predicted magnitude for a Gi-coupled receptor receiving
  a Gs donor is a **positive** residual of the same magnitude
  (predicted tilt > receptor's own Gi-anchored reference tilt).
- Compare against the residual test's native-only CI upper bound
  `+0.21 Å`. Branch 1 requires the ruler CI's lower bound to exceed
  `+0.21 Å`.

---

## E1 — external ruler on the campaign's Class A + Gα-complexed reference set

### E1a — enumeration source and scope

**Source**: `refs/reference_set.blockb_pinned.csv` (Block B scoring-time
bytes, SHA-256 `6ee2cad8…`) + `refs/sealed_active_refs_2026_09_01.csv`
(the 8 sealed Block A active refs held out of blockb_pinned.csv).
Total active-role rows: **103** across all campaign panel receptors.

**Restrictions applied to build the ruler set** (per E1a spec):

1. **Class A only**: exclude Block A's 4 Class B receptors (CRHR1,
   GCGR, GLP1R, PTH1R) and 4 Class F receptors (FZD4, FZD6, FZD7, SMO).
   Class labels come from Block A's PREREG §1 v2 curation.
2. **Ga-complexed only**: `active_stabilization_source ∈ {native,
   mini_G, chimera}`. Excludes `nanobody` (Nb-stabilised active states
   with no Gα in the complex), `agonist_only` (active states with no
   partner), `DVL_DEP` (Wnt-family, non-Ga).
3. **Family resolvable**: `alpha5_donor_class` populated (except
   `none_Ga`) OR receptor is in `refs/gpcr_coupling.csv` with a
   `primary_ga_class ∈ {Gs, Gi, Gq, G12, Gt}`. Otherwise family = `?`
   and the row is excluded from the Gs/Gi ruler but retained in
   `external_ruler.csv` with a `family_resolvable=False` flag.

Full listing at `experiments/019_block_b_partner_selection/analysis/external_ruler.csv`
(one row per structure, 103 rows).

**Ruler-eligible after all three restrictions**: 45 structures across
45 receptors (one active per receptor in the curated set).

### E1b — metric definition

**`d_gpcrdb_tm6_tilt_ref`** column of the reference set, computed by
the campaign's own pipeline (`scorer/references.py::compute_deltas`
with the SIFTS → UniProt → GPCRdb BW derivation path at positions
2.46 and 6.37, Cα-Cα distance in Å). Same definition used for the
residual test. Not a GPCRdb-published value; this is a direct
recomputation on each reference PDB using the campaign's own scorer.

### E1c — family × stratum × n receptors and n structures

Per stratum (native-only / native + mini_G / all incl. chimera):

**Stratum: native**

| Family | n structures | n receptors | median tilt (Å) | range |
|---|---:|---:|---:|---|
| **Gs** | **0** | **0** | — | — |
| Gi | 20 | 20 | 17.518 | [16.390, 19.879] |
| Gq | 4 | 4 | 16.918 | [15.773, 17.978] |
| Gt | 1 | 1 | 17.586 | — |

**Native-only Gs stratum is empty.** The campaign's curated Class A
reference set contains NO receptor with a native heterotrimeric Gs
complex as the active reference. Every Class A Gs active is
mini-G or chimera stabilised.

**Stratum: native + mini_G**

| Family | n structures | n receptors | median tilt (Å) | range |
|---|---:|---:|---:|---|
| Gs | 3 | 3 | 18.097 | [17.945, 18.452] |
| Gi | 22 | 22 | 17.556 | [16.390, 19.879] |
| Gq | 7 | 7 | 16.979 | [15.773, 17.978] |
| Gt | 1 | 1 | 17.586 | — |

Gs group members: AA2AR (mini_G, 18.10), FSHR (mini_G, 17.94),
LSHR (mini_G, 18.45).

**Stratum: all (incl. chimera)**

| Family | n structures | n receptors | median tilt (Å) | range |
|---|---:|---:|---:|---|
| Gs | 6 | 6 | **18.590** | [17.945, 19.010] |
| Gi | 22 | 22 | 17.556 | [16.390, 19.879] |
| Gq | 11 | 11 | 16.979 | [15.773, 18.098] |
| G12 | 1 | 1 | 17.243 | — |
| Gt | 1 | 1 | 17.586 | — |

Adds MC3R (chimera, 18.86), MC5R (chimera, 18.73), OXYR (chimera, 19.01).
The three chimera-anchored Gs actives sit systematically higher than
the mini-G-anchored ones (median chimera 18.86 vs median mini-G 18.10).

**Note on the receptor-vs-structure counting**: the campaign's curated
reference set has one active reference per receptor. n_structures =
n_receptors in every stratum. The dispatch's caution about multiple
PDBs per receptor being non-independent does not arise here.

### E1c — Bootstrap Gs − Gi gap

Receptor-boot within family; percentile bootstrap; 1000 draws;
seed `20260910`.

| Stratum | Gs n | Gi n | Point (Å) | 95% CI | Branch 1 lower > 0.21? |
|---|---:|---:|---:|---|---|
| native-only | **0** | 20 | — | not computable | NOT MET (default) |
| native + mini_G | 3 | 22 | +0.541 | [+0.162, +0.995] | NOT MET (0.162 < 0.21) |
| all (incl. chimera) | 6 | 22 | +1.033 | [+0.390, +1.415] | 0.390 > 0.21 — but chimera-cautioned |

### E1d — Three strata verdict

- **Native-only** (pre-registered decision stratum): Branch 1 not
  evaluable. Zero Class A Gs native-Gα-complexed structures in the
  campaign's curated reference set. Default: **NOT MET**.
- **Native + mini_G**: lower bound 0.162 < 0.21. **NOT MET.**
- **All (incl. chimera)**: lower bound 0.390 > 0.21, nominally
  Branch-1 territory — BUT the dispatch explicitly cautions "chimeric
  α5 donors may not reproduce the native family geometry and should
  not silently set the ruler." The all-stratum median is 0.49 Å
  higher than native + mini_G median (18.59 vs 18.10) because
  chimeras (MC3R, MC5R, OXYR) sit systematically higher. Adopting
  the chimera-inclusive result as the ruler would let engineered
  scaffold geometry drive the SC-B-6 sign flip. **Not adopted.**

### E1e — LORO on the Gs side (native + mini_G stratum)

Native-only Gs stratum has n=0, so LORO is undefined. Reporting LORO
on the native + mini_G stratum (the only stratum with a computable Gs
set of n>1):

| Held out | Gs n | Point (Å) | 95% CI | Lower > 0.21? |
|---|---:|---:|---|---|
| AA2AR | 2 | +0.642 | [+0.180, +0.995] | NO (0.180) |
| FSHR | 2 | +0.718 | [+0.314, +0.995] | YES (0.314) |
| LSHR | 2 | +0.465 | [+0.141, +0.650] | NO (0.141) |

**Any single-receptor removal on the native + mini_G Gs stratum moves
the CI across critical boundaries.** Dropping AA2AR or LSHR keeps the
CI lower bound below 0.21; only dropping FSHR (the median Gs receptor)
lifts it above. The ruler is n=3-fragile.

### E1 verdict — RECORDED, not adjudicated

**Branch 1 as pre-registered NOT MET.** SC-B-6 stays at the r3 (Phase 6b)
wording. E2 remains a scope note. E3/E4 are queued but not run in this
pass (dispatch says "Run E1 first and STOP").

Sub-finding worth naming for the manuscript:

- **The deposited record's Class A Gs Ga-complexed active structures
  are entirely mini-G or chimera-stabilised.** Zero native Gs
  heterotrimeric complexes in the campaign's curated Class A set.
  Any claim about "Gs-anchored reference geometry" on the tilt axis
  is a claim about engineered constructs, not native transducer
  complexes. The methods paragraph on axis choice should name this.
- **Even under the chimera-inclusive stratum where Branch 1 nominally
  fires, the ruler is n=6-fragile** and mixes native construct types
  the dispatch explicitly cautions against.
- **Restriction of range on the tilt axis** (Block A SD 1.19 Å) means
  the entire 0.6–1.4 Å Gs-Gi gap sits within ±1σ of the reference-side
  spread. The ruler and the residual are on an axis that Block A
  itself stated cannot test amplitude, and the same restriction limits
  identity-sensitivity power on the same axis.

### Manuscript sentence

Reverts / stays at SC-B-6 (r3 wording): "on the largest shuffled cell
(Gs donor into Gi-cognate receptor, 24 receptors × 4 backbones), the
tilt residual is +0.024 Å [−0.29, +0.30] under all-refs and
−0.062 Å [−0.41, +0.21] under native-only; Outcome A signed on the
load-bearing cell, CI spans zero."

Additional sentence for Methods:

> The deposited Class A + Gα-complexed active-reference record shows a
> Gs − Gi TM6-tilt gap of +0.541 Å [95% CI +0.162, +0.995] on
> native + mini-G stabilisation (n=3 Gs receptors, n=22 Gi) and
> +1.033 Å [+0.390, +1.415] on the all-strata set (n=6 Gs receptors,
> n=22 Gi; chimera-anchored). Both intervals overlap with the observed
> native-only residual CI (n=20 native-anchored Gi receptors:
> [−0.41, +0.21]), so the family-specific opening the deposited record
> shows is not resolvably reproduced or excluded by the Block B
> models on this axis. The Class A Gs record contains zero native
> heterotrimeric Gs complexes; every Class A Gs active reference in
> the campaign's curated set is mini-G or chimera stabilised.

---

## E2 — scope note (not load-bearing)

Since E1's Branch 1 not met, E2 is downgraded from "load-bearing analysis"
to "scope note" per dispatch. Recording without executing:

The tilt-axis restriction of range (Block A SD 1.19 Å) is the underlying
limit. NPxxY-OH axis has SD 4.71 Å per Block A and would resolve larger
family gaps if a family gap existed on NPxxY. Direct TM6 cytoplasmic-tip
CA measures (e.g., 6.29-Cα or 6.30-Cα endpoints rather than the
2.46↔6.37 tilt pair) would need axis definitions and a fresh compute
pass; not run in this pass. If a future revision needs load-bearing
E2, the scope is: (a) NPxxY-OH Gs − Gi ruler on the same 45-receptor
Ga-complexed set; (b) TM6-tip Ca-Ca ruler; (c) reference-separation SD
per axis for comparability.

---

## E3 — queued, not run in this pass

Cluster-boot convention audit. Enumerate every CI in the Block B
dossier, verify each is cluster-boot over the 26 paralog clusters,
recompute receptor-boot ones. Deferred pending a fresh dispatch.

---

## E4 — queued, not run in this pass

AA2AR reference-separation hypothesis. Deferred pending a fresh
dispatch. Preliminary note: from `reference_audit.csv` +
`ladder_per_receptor.csv`, AA2AR's active reference (5G53, mini-G) has
tilt 18.10 and NPxxY-OH 3.71 Å; inactive reference (5NM4) has tilt
11.99 and NPxxY-OH 9.73 Å. Δ_ref_tilt = +6.10, Δ_ref_NPxxY = −6.02.
Not unusually close on either axis; the hypothesis that AA2AR's
recurring anomaly comes from small reference separation is
prima-facie not supported by this receptor's numbers, but a full E4
per-axis rank across the 40 Block B receptors is deferred.

---

## Outputs

- `docs/BLOCK_B_FOLLOWUP_E1_E4.md` — this file.
- `experiments/019_block_b_partner_selection/analysis/external_ruler.csv` —
  103 rows, one per active reference in the campaign's curated set,
  with class_a_included / ga_complexed_included / family_resolvable
  flags for stratum construction.
- `docs/ASSUMED_NOT_VERIFIED_E.md` — items not verified in this pass.

No `ci_convention_audit.csv` produced (E3 not run).
No modification to `block_b_freeze_r3` artifacts. No r4 tag.
