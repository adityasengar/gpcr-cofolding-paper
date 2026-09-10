# Block C — open questions

Things the bundle could not settle. Per the dispatch's §8: an honest entry here
is a good outcome; an invented number is not.

## Q1 — Two source corpora were not delivered, so most of the block is unverifiable

`rows.tier3.v2.csv` (SHA `5ccf58ac…`) and the pose sibling `rows.csv` (scorer
`d9c646af…`) are named as inputs and not shipped. Consequence: of our 53 checks,
23 are recomputed from the off-site census and **30 compare shipped summaries to
one another**. SC-C-1 and SC-C-4 — the block's two surviving positives — fall in
the second group. See `DISCREPANCY_REPORT.md` D-C-1.

## Q2 — 66 named data files are absent, and the bundle does not say which absences are deliberate

Full list and triage in `DISCREPANCY_REPORT.md` D-C-2. Four matter most:
`s4_bw_decomposition.json` (the only residue-level analysis named in any block),
`task6_p0_correlation.json` (the only quantitative cross-block link, n=35 common
receptors), `task_D_species_match_root_cause.json`, and the s7/s8 nulls-and-
ceilings set. "Tidy data only" is a reasonable policy; we cannot tell which of
the 66 it covers.

## Q3 — Flag C-12 contradicts C-C-3, in the shipped files

Flag C-12 reads "Cluster-boot CI on the 2×2 interaction NOT recomputed."
C-C-3 is marked RESOLVED and `g_scc1_cluster_boot.json` is present. The dispatch
§4(m) says C-C-3 wins and the flag is stale. Confirmed by inspection; logged for
upstream correction of the flag file.

## Q4 — W-C-5's 14.5\% coincidence, left unreconciled on instruction

W-C-5 notes that Block A's 14.5\% is a Protenix-alone panel mean and shares a
value with a Block C figure coincidentally. The dispatch §4(k) instructs us not
to attempt a reconciliation. Not attempted. Recorded so a later reader does not
mistake the coincidence for a relationship.

## Q5 — An unannounced second zip

`block_c_structures.zip` appears nowhere in the dispatch and is byte-identical
to `13_structures/` in the main bundle, rooted differently. Harmless, but worth
confirming a *different* structure set was not intended.

## Q6 — The bundle README's index undercounts `13_structures/`

Says 2 files; 16 present. The dispatch §4(n) already flags this. Confirmed: the
index is stale, the data is correct. Every other directory in the index matches
exactly.

## Q7 — Not connected to two-state generation, per instruction

The dispatch forbids linking Block C to the paper's two-state generation claim,
on the grounds that Block C's arms were not designed to test it. No sentence in
the Results or Methods does. Flagged here because the temptation is real: the
2$\times$2 result reads as though it bears on state generation and it does not.
