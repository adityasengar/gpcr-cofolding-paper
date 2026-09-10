# BC-4 — where the ligands actually are

**Claim**: SC-C-1's numerator is clean; the ligand-class contrast is not built on
mis-docked ligands. Also carries the dispatch's §4(a) retraction and §4(i)
peptide adjudication.

**Buildable today.** `12_g4_off_site_census/g4_full_census_v2.csv`, 40,000 rows,
columns `arm`, `role`, `ligand_source`, `distance_A`, `backbone`, `receptor`.

## Encoding

Distribution of `distance_A` — ligand centroid to pocket centroid — with the
three adjudicated bands drawn as background regions, **not** as a binary
split: in-pocket ≤ 8 Å, entrance-bound 8–15 Å, off-site > 15 Å.

**Entrance-bound must be shaded as valid, not as failure.** It is 7,349 of
40,000 rows and adjudicating it as error would roughly double the apparent
off-site rate.

Facet or split by `ligand_source`, which is the load-bearing variable and the one
a reader will not expect:

| stratum | n | off-site (> 15 Å) |
|---|---:|---:|
| apo × {agonist, antagonist} × **hetatm** | 9,800 | **1.52 %** |
| apo × {agonist, antagonist} × **peptide_chain** | 3,000 | **66.53 %** |
| apo arm, all | — | 15.1 % |
| cognate arm, all | — | 20.3 % |
| pooled, all 40,000 | 40,000 | 17.73 % |

Band counts pooled: 25,559 in-pocket, 7,349 entrance-bound, 7,092 off-site.

## What the panel has to say in its own caption

1. The stratum SC-C-1 is computed on is **1.52 %** off-site. That is the number
   the contrast depends on.
2. Peptide ligands in the *same* cells are 66.53 % off-site, at a median of
   17.5 Å, because peptide receptors bind at the extracellular vestibule.
   **Pooling the two strata manufactures a failure rate.**
3. The previously circulated pooled figure of **25.6 % is retracted** — it came
   from a receptor-chain picker that selected Gα rather than the receptor on any
   receptor shorter than ~394 aa. The corrected pooled value is 17.73 %.

## What not to do

Do not draw a single pooled off-site rate. Do not colour entrance-bound as a
failure state. Do not show the 176-row far tail without saying 175 of them are
one backbone (Chai-1) — it is a per-backbone pathology, not a block-wide one.
