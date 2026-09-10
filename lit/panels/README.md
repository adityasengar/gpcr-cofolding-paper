# panels/ — who benchmarked on which receptors, and which PDB entries

Built 2026-09-10 by the lit session. Answers one question: **when a paper picks a set of
GPCRs, which receptors and which PDB entries does it actually contain?**

`panels.csv` holds **613 verified rows across 4 panels, 175 distinct receptors**, each
row a (paper, subset, PDB entry) with receptor, class, family, state, resolution, partner Gα
and ligand. `panel_unit` says whether a paper enumerates its panel at **structure** level
(chiesa, zhang) or only at **receptor** level (heo's Table S2 gives per-state counts, not
PDB ids) — do not count rows across panels without it.

```
python3 build_panels.py            # rebuild panels.csv
python3 build_panels.py --refresh  # re-fetch GPCRdb first
```

| paper | panel | source | status |
|---|---|---|---|
| `chiesa2025templatebias` | 145 structures / 55 receptors / 31 families / 63 pairs | ACS SI Table S1 | **all four counts exact** |
| `zhang2026generalization` | 253 complexes / 68 receptors | npj SI Table S2 | **count exact** |
| `lee2026confornets` | 51 pairs / 102 structures | authors' repo, `assets/gpcr/references.csv` | **count exact** |
| `heo2022multistate` | 68 receptors + 45 docking complexes | bioRxiv v2 SI Tables S2, S3 | **all four counts exact** |

## The methodological finding, which outranks the lists

Panels are not published in the papers we hold — the lists are in SI, and `si_in_scope`
reads `SI NOT HELD` for every key paper. So the first approach was to re-run each
paper's stated selection rule against the GPCRdb structure API and validate by comparing
the resulting **counts** against the published ones.

**That validation is not sound, and the corpus now has the counterexample.** zhang's rule
reconstructed 250 complexes against a published 253 — a 1.2% count error, comfortably
inside any sane tolerance. When Table S2 was obtained, the reconstruction shared only
**222 of its 253 entries: 31 missed and 28 invented**, ~12% wrong in each direction.

> A matching count is not a matching membership. A count check can only ever *falsify* a
> reconstruction, never confirm one. Only an SI join proves membership.

Reconstructions are therefore labelled `count-only` regardless of how well the count
agrees, and `build_panels.py` **emits no rows for them** — a count-only rule is not a
receptor list, and leaving its rows in the same file invites exactly the misuse this
finding is about.

**Second finding: a stated rule can under-determine its own panel.** Chiesa's Table S1
reproduces all four published counts exactly, yet the rule as written ("class A GPCRs
bound to G protein released after 01 Jan 2023, human receptor and human Gα") admits 152
*further* structures in the same window, spanning 23 receptors the panel omits entirely
— with no difference in experimental method and none in resolution (both sets are 100%
cryo-EM, medians 3.00 vs 3.21 Å). No date bound separates them: at ≤2023-12-31 the rule
still misses 12 real entries while inventing 37. Something excludes whole receptors and
the paper does not say what — most likely GProteinDB membership, which they name but do
not define as a filter. **The rule cannot be repaired from the text; the panel is only
knowable from Table S1.**

## What the SI settled that the notes could not

**"Human Gαs" in chiesa means Gα subunits, plural — not Gα-s the stimulatory subtype.**
The note recorded the ambiguity and it could not be resolved from the main text. The
panel's 145 structures carry **nine** Gα subtypes and are dominated by **Gαi1 (77)**,
with Gαs second at 44. This is why their 63 pairs exceed their 55 receptors. Any sentence
implying chiesa is a Gs-coupled benchmark is wrong.

**Chiesa's benchmark is 100% active-state and 100% G-protein-bound** — 145 of 145 on
both counts. There is no inactive arm in the target set at all.

**Zhang's is 225 active / 28 inactive (89% active) and 203 of 253 G-protein-bound
(80%)**, with 215 of 253 ligands agonists. A benchmark built to test generalisation to
families unseen in training is therefore overwhelmingly agonist-bound, active-state,
transducer-coupled structures.

**The four panels barely overlap, and this is the headline.** Union 175 receptors. **No
receptor appears in all four.** 115 appear in exactly one, 51 in two, 9 in three.

| | chiesa | heo | lee | zhang |
|---|---|---|---|---|
| **chiesa** (55) | — | 10 | 13 | 20 |
| **heo** (68) | 10 | — | 15 | 7 |
| **lee** (53) | 13 | 15 | — | 13 |
| **zhang** (68) | 20 | 7 | 13 | — |

The nine receptors in three of four panels are `cckar ccr6 ccr8 cxcr3 fshr nk1r npy2r
ntr1 ssr2`. Four benchmarks that all claim to measure GPCR conformational-state
prediction are, at receptor level, four different experiments. No cross-paper claim of
the form "method X beats method Y on GPCRs" is currently supported by a shared panel.

## Still blocked, and why

`lee2026confornets` — **solved 2026-09-10 from the authors' repo**,
`github.com/aqlaboratory/confornets`, file `assets/gpcr/references.csv`: 51 pairs, 102
structures, none reused across pairs. Column `pdbidchain_i` is the **active** member and
`pdbidchain_j` the **inactive** member in all 51 rows, cross-checked against GPCRdb.

The reconstruction was never going to work — its binding constraint is *"pairs with the
fewest engineered mutations … where both structures contained at most one mutation"*
[p.15], the both-states rule alone returns 86 receptors and is flat across every snapshot
date, and no public API carries engineered-mutation counts. The lesson is not about the
rule: **an unauthenticated GitHub search API returns nothing useful. Query the repo path
directly.** A search for `confornets` reported no hits while
`api.github.com/repos/aqlaboratory/confornets` resolves instantly.

**Two of its 51 same-receptor pairs are cross-species**, which the paper does not say:
ACM3 pairs human `8E9Z` (active) with rat `4U15` (inactive), and NTR1 pairs rat `8FN1`
(active) with human `7UL2` (inactive). A within-receptor conformational contrast that is
in fact a cross-species one. This is why 51 pairs give 53 distinct GPCRdb proteins.

`heo2022multistate` — **solved 2026-09-10 via the bioRxiv preprint, not Wiley.** DOI
`10.1101/2021.11.26.470086` **version 2** (2022-04-08) is the revision that became Proteins
90:1873–1885 and is CC-BY. Its Table S2 reproduces all four published numbers exactly. **v1
is the wrong file** — its set has 55 receptors, and its Table S3 is a different table
altogether. This is the general lesson: when a journal SI is paywalled, check whether a
CC-BY preprint exists *and match its version to the published paper*.

## receptors.csv — the analysis table

One row per receptor, 175 rows, 18 columns:

`receptor` (GPCRdb entry name) · `name` · `species` · `gpcr_class` · `gpcrdb_family` ·
`n_panels` · `in_chiesa` `in_heo` `in_lee` `in_zhang` (0/1) · `n_pdb_in_panels` ·
`n_pdb_in_gpcrdb` · `has_active` `has_inactive` `both_states` (0/1) · `first_release` ·
`last_release` · `pdb_ids` (semicolon-separated).

Sorted by `n_panels` descending, so the shared core is at the top. Filter on
`both_states==1` for the 75 receptors that can support a within-receptor state contrast.

## Files

```
receptors.csv                 175 rows, ONE PER RECEPTOR - start here for analysis
panels.csv                    613 verified rows, one per (paper, subset, PDB entry)
build_panels.py               rebuilds both; carries the count-vs-membership lesson
si_tables/                    extracted tables, small, in git
  chiesa2025templatebias_tableS1.csv     145 rows: receptor, family, PDB ID
  zhang2026generalization_tableS2.csv    253 rows: PDB, resolution, class, state,
                                         ligand CCD, pharmacology, max lig/seq similarity
  zhang2026generalization_fep_series.csv 15 congeneric series with PDB and ChEMBL ids
cache/gpcrdb_structures.json  GPCRdb structure API, 1716 entries
cache/rcsb_release_dates.json RCSB cross-check (see below)
```

Raw SI lives in `../source/si/` with the other large sources, and is **not in git**.

## Mapping a panel's slugs onto GPCRdb: do not assume human

Panels are written as slugs (`OPSD`, `OPRM`, `B1B1U5`). Resolving them by appending
`_human` is wrong often enough to change an answer, and it produced a false finding in this
session: `OPSD` resolved to `opsd_human`, which GPCRdb holds only in the **Active** state,
so an audit of our own 48-receptor panel reported 39/40 with both states and raised a
cross-species alarm. The orchestrator checked the actual references — `4X1H` and `7ZBC` are
both `opsd_bovin`, the pair is same-organism, and the panel is 40/40. The alarm was an
artifact of the resolver, not a property of the panel.

Known non-human entries to resolve explicitly:

| slug | GPCRdb | note |
|---|---|---|
| `OPSD` | `opsd_bovin` | human rhodopsin has **no** inactive structure; every dark-state entry (1F88, 2I37, 3C9M, 6OFJ) is bovine |
| `B1B1U5` | `b1b1u5_9arac` | opsin from *Hasarius adansoni*, a jumping spider (active 9EPP / inactive 6I9K) |
| `OPRM` | `oprm_mouse` | in lee2026confornets' benchmark, mouse on both sides |

Resolve by checking which species GPCRdb actually holds, or collapse to the stem
(`opsd`) when only receptor identity matters. Never let `_human` be a silent default.

## Two traps recorded so they are not re-hit

**GPCRdb grows.** A rule with only a lower date bound is evaluated against today's
database, not the one the authors used, and over-counts. Every rule carries the paper's
own snapshot date as an upper bound.

**GPCRdb's `publication_date` already IS the PDB initial release date.** The first
version fetched `initial_release_date` from RCSB for all 1,716 entries on the assumption
it was the journal date. They agree on all 1,713 matched entries. The cross-check is kept
in `cache/` and is re-runnable, but no rule depends on it — do not "correct" this field.

## Next

1. `matic2023gpcrome`'s 125 non-redundant receptor–Gα pairs — the coupling-interface
   panel, and the closest thing in the corpus to our co-input. Its SI is not held.
2. Once Block B's receptor list exists, join it against `panels.csv` — the union of 175
   verified receptors is the denominator for "how much of this panel is new", and the
   nine-receptor three-panel core is the natural overlap set to include deliberately.
