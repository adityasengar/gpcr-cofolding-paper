# GATE-4 — Scorer SHA discrepancy: D1 vs D2/D3

**Verdict**: **SAFE for cross-tier comparability.** **Bug #4 NOT MATERIAL** to any D-tier headline. **Documentation drift confirmed on both D2 and D3 headline docs** — same pattern as Block C's T7C headline.

**Executed**: 2026-09-10 (GATE-4 fork, Block D autonomous closeout dispatch).

---

## §1 Row-level scorer SHA — what actually landed

Direct read from the row-level `scorer_git_sha` column in each corpus:

| Tier | Corpus | Unique `scorer_git_sha` value | Rows |
|---|---|---|---:|
| D1 | `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` | `d9c646af5f89861c16062bf256de96a8389d9915` | 14,000 |
| D2 | `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` | `d9c646af5f89861c16062bf256de96a8389d9915` | 2,370 |
| D3 | `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` | `d9c646af5f89861c16062bf256de96a8389d9915` | 25,810 |

**All three D-tier corpora were scored by the SAME scorer version.** Row-level column is authoritative (matches HPC-stamped `~/paper_af3/scorer/_version_sha.py` and laptop `scorer/_version_sha.py`, both = `d9c646af…`).

## §2 The "891041e858f3" phantom SHA

The prior handoff and the D2/D3 headline docs cite scorer `891041e858f3747b…`. That SHA **does not exist in git** — any form:

```
$ git rev-parse 891041e858f3
fatal: ambiguous argument '891041e858f3': unknown revision or path not in the working tree.
$ git cat-file -e 891041e858f3
fatal: Not a valid object name 891041e858f3
$ git log --all --pretty='%H' | grep -c '^891041e858f3'
0
```

Not a ref, not an orphan object, not in reflog. **This is the same documentation-drift pattern as Block C's `T7C_POST_FIX_HEADLINE.md`** which also cited `891041e858f3` while the actual row-level column said `d9c646af`. Neither prose figure is a real commit — most likely artifact of a venv install from a dirty/rebased tree, or manual typo propagated across headlines.

**Row-level `d9c646af` is authoritative.** All headline-doc prose citing `891041e858f3` must be corrected.

## §3 What changed between `d9c646af` and HEAD (scorer/)

Full commit chain (49 commits `d9c646af..HEAD`): D-tier + Block C closeout landed as source-tree changes AFTER the scoring venv was installed. Only two files touched:

```
$ git diff --stat d9c646af..HEAD -- scorer/
 scorer/pocket_metrics.py | 206 ++++++++++++++++++++++++++++++++++++++---------
 scorer/propose.py        | 162 ++++++++++++++++++++++++++++++++++---
 2 files changed, 321 insertions(+), 47 deletions(-)
```

**`scorer/pocket_metrics.py` — 4 function-level hunks:**

| Function | Line (post) | Purpose of change | Affects D-tier? |
|---|---:|---|---|
| `w648_chi1` | 458 | Add W6.48 χ1 dihedral emitter | No (D-tier headlines don't consume χ1) |
| `_mcs_ligand_rmsd` | 583 | Bug #3 — automorphism-safe MCS | No (D-tier has no small-molecule ligand) |
| `ligand_rmsd_to_ref` | 714 | Bug #4 — `MCS_FALLBACK_MIN_COVERAGE=0.8` fast-path guard | See §4 |
| `build_pocket_reference_cache` | 1347 | Bug #2 — 8 Å pocket-proximity tripwire on HETATM picker | See §5 |

**`pocket_ca_rmsd` (line 292): UNCHANGED between `d9c646af` and HEAD.** Confirmed by empty diff hunk in that line range.

**`compute_pocket_axes_bundle` (line 1069) and `_pocket_rmsds_against_ref` (line 997): UNCHANGED.** These are the functions that emit `pocket_ca_rmsd_active` / `pocket_ca_rmsd_inactive` — the columns D1's F5 (CNR2 saturation) rests on. **No functional change; D1 F5 is directly comparable across the whole scorer-`d9c646af` family (D1, D2, D3, Block C `rescore_t7c_full`).**

**`scorer/axes.py` — UNCHANGED** (not in the diff scope). This is where the two-instrument predicate columns (`d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`) are defined. D-tier NPxxY-OH and TM6-tilt numbers are byte-identical to Block C's two-instrument predicate.

**`scorer/propose.py` — 162 line diff, all MSA-plumbing + Nb-arm helpers.** Functions changed: `_boltz_msa_field`, `_boltz_yaml_monomer`, `_boltz_yaml_two_chain`, `_of3_apply_msa_paths`, `_of3_query_dict`, `_of3_json_monomer`, `_protenix_apply_msa_paths`, `_protenix_ligand_entry`, `_row_input_content`, `_receptor_nb_content`. These are all **input-generation code**, run at dispatch/prediction time; scoring is unaffected.

## §4 Bug #4 (`ligand_rmsd_to_ref` fast-path coverage guard) — placement + relevance

**Placement**: commit `9e640d508c0781e32669de874334cdbba767dc17`, 2026-09-08 08:36 CEST. **NOT an ancestor of `d9c646af`** (`git merge-base --is-ancestor 9e640d5 d9c646af` exits 1). So Bug #4 was NOT in the scoring venv for any D-tier run.

**Relevance check — how many rows would be affected**:

| Tier | Rows | `ligand_rmsd_to_ref` populated | Cells affected |
|---|---:|---:|---|
| D1 | 14,000 | 0 (0.0%) | None — apo-only, no small-molecule ligand |
| D2 | 2,370 | 0 (0.0%) | None — nanobody + peptide chains only, no small-molecule ligand |
| D3 | 25,810 | 990 (3.8%) | **All 990 rows are MCHR1** — apo-only tier but scorer's ligand path fired on MCHR1's reference (see §7 caveat) |

**Verdict**: Bug #4 does **NOT** affect any D-tier headline number. The D3 headline (MSA-depth active fraction) is computed from the two-instrument predicate columns in `axes.py` (UNCHANGED), not from `ligand_rmsd_to_ref`. The 990 MCHR1 rows carry spurious `ligand_rmsd_to_ref` values that (a) should not have been emitted on an apo-only tier and (b) were computed under the pre-Bug-#4 fast-path — but they don't feed the headline.

**D3 headline F7 is misleading**: `tier_d3_full_headline_2026_09_08.md` line 106-109 states *"Bug #4 fix landed alongside D3."* This is technically true in git ancestor order (`9e640d5` came right after `c307a82`, which lists the D3 result), but is **misleading** because Bug #4 was NOT in the venv that scored D3 rows. The row-level `scorer_git_sha` proves this.

## §5 Bug #2 (pocket-proximity HETATM tripwire) — placement + relevance

**Placement**: part of `48ddfc1` ("Docking-measurement bug hunt 2026-09-07"). **NOT an ancestor of `d9c646af`** — landed AFTER. So D-tier scoring used the LEGACY largest-HETATM picker to pick reference ligand for `ligand_rmsd_to_ref`.

**Relevance**: same as Bug #4 — affects reference-ligand definition, not receptor-side pocket-Cα. D-tier headlines are on receptor-side metrics (two-instrument predicate + pocket-Cα-RMSD-to-active/inactive), so Bug #2 does not affect them.

**Read-through to Block C**: Block C's `rescore_t7c_full/rows.csv` was also scored on `d9c646af` (same as D-tier). Bug #2 was applied at the ANALYSIS stage in Block C, not the SCORING stage. Consistent with the Block C wrap posture — the scorer venv was fixed at `d9c646af` and analytic layers on top handled the corrections.

## §6 D1 F5 reproducibility check — CNR2 pocket-Cα-RMSD saturation

D1 F5 states: CNR2 apo × all 4 backbones × 500 samples per bb — 100% of predictions sub-Å to BOTH active and inactive references. Reproduces cleanly on the scored corpus:

```
$ awk -F, 'BEGIN{OFS=","}NR==1{for(i=1;i<=NF;i++){if($i=="receptor_slug")r=i;if($i=="pocket_ca_rmsd_active")a=i;if($i=="pocket_ca_rmsd_inactive")n=i;if($i=="input_path")p=i};next}
  $r=="CNR2"{split($p,x,"/");for(i in x)if(x[i]~/boltz|chai|of3|protenix/)bb=x[i];
  if($a!=""&&$a<1.0)ha[bb]++;if($n!=""&&$n<1.0)hi[bb]++;n_bb[bb]++}
  END{for(bb in n_bb)print bb,n_bb[bb],ha[bb]/n_bb[bb],hi[bb]/n_bb[bb]}' D1/rows.csv | sort
```

Numbers reproduce headline table (100% sub-Å-to-active AND sub-Å-to-inactive for CNR2 on all 4 backbones). Since `pocket_ca_rmsd` and `compute_pocket_axes_bundle` are UNCHANGED across the scorer diff, this is not a re-derivation of a possibly-different quantity — it's the same code path evaluated against the same corpus.

**Cross-scorer re-score not required**: the code path is provably identical. No new evidence needed to establish comparability.

## §7 D3 MCHR1 `ligand_rmsd_to_ref` — flagged but not in scope

D3 is apo-only per PREREG §D-3. All 990 D3 rows with populated `ligand_rmsd_to_ref` are for MCHR1. Suggests the scorer's reference-cache fired for MCHR1 in a way it didn't for the other 25 D3 receptors. Likely cause: MCHR1's reference structures contain a ligand HETATM the scorer picked; the scored row has no query ligand so the value is either NaN-adjacent or a phantom RMSD.

**Not in this gate's scope to resolve** — flag for the D3 Part A analysis. If MCHR1's `ligand_rmsd_to_ref` values are consumed anywhere downstream, they need re-inspection under Bug #4 rules (rows might have pushed through the pre-Bug-#4 fast-path). If not consumed, ignore.

## §8 Deliverable summary

- **Cross-tier scorer comparability**: **SAFE.** All three D-tier corpora scored on `d9c646af`; `pocket_ca_rmsd` code path unchanged from `d9c646af` to HEAD; `scorer/axes.py` (two-instrument predicate columns) unchanged. D1 F5 is directly comparable to Block C G2.
- **Bug #4 relevance to D-tier headlines**: **NOT MATERIAL.** D1 + D2 have zero `ligand_rmsd_to_ref` rows; D3 has 990 (all MCHR1) but these don't feed the depth-lever headline.
- **Documentation drift**: **TWO occurrences** — D2 headline doc and D3 headline doc both cite the phantom SHA `891041e858f3`. Corrections needed at dossier-authoring time (§Part B / Part C). Same pattern as Block C's T7C headline drift; suggests a systemic issue in how the venv-stamped SHA is being propagated to prose.

**No STOP conditions.** GATE-4 clears the way for §3 STATE_CHECK through §6 to proceed. GATE-1/2/3 findings should be checked against §8 verdicts before any cross-tier claim lands in the dossier of record.

---

## Feed-forward to §6 open-for-adjudication

- **6.1 GATE-4 verdict line**: *"Scorer SHA drift is documentation-only; row-level scorer=`d9c646af` is uniform across D1/D2/D3 and identical to Block C's `rescore_t7c_full` scorer. Cross-tier comparability guaranteed by construction. Bug #4 not material — no D-tier headline consumes `ligand_rmsd_to_ref`."*
- **6.6 (judgment call, not resolved here)**: whether the D2/D3 headline docs get retroactively corrected in-place, or the correction lives only in the release-repo dossier and the working-repo headlines are archived-as-is. Same question came up for Block C's T7C headline; consistent handling preferred.
