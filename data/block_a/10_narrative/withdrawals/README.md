# withdrawals/

One file per retracted claim. Reason, evidence, dossier reference, and the
sentence the manuscript would have used if the claim survived.

**Format**: `W-<N>_<slug>.md`. Content: (a) the claim as stated, (b) the
reason for retraction, (c) evidence citations (dossier phase + script +
input SHA), (d) the corrected sentence if one exists.

Retractions are load-bearing for credibility. Reviewers who see a paper
that never withdraws anything have a different reaction than reviewers who
see a paper with a transparent retraction ledger.

## Block A retractions

- `W-1_apo_bistability_panel_mean.md` — "14.5% apo-active panel mean" as a cross-backbone signal
- `W-2_plddt_tracks_correctness_campaign_wide.md` — pLDDT tracks correctness as a campaign-wide claim
- `W-3_bimodal_cells_29_25.md` — "29 bimodal cells, 25 in apo (86%)"
- `W-4_opsd_apo_boltz_04A.md` — "OPSD/apo/Boltz reaches 0.40 Å from active crystal" as cell-median
- `W-5_lpar1_of3_918_04.md` — "LPAR1-OF3 91.8% predicate-active with 0.4% sub-Å" as Block A
- `W-6_of3_rerun_silently_merged.md` — "OF3 rerun 2,375 rows silently merged into Block A with `no-git`"
- `W-7_merged_via_driver.md` — "Merged via `merge_of3_rerun_rows.py`" claim in two docs
- `W-8_14pt5_pc_cross_backbone.md` — "14.5% panel mean as a cross-backbone signal"

## Added post-scientific-review

- `W-2_plddt_tracks_correctness_campaign_wide.md` — **RESTATED**: the Protenix-overconfident-across-panel framing was a `plddt_mean` artifact of non-anchor residues; collapses to null at anchor-restricted grain. Pre-review version preserved in the `pre-scientific-review` tag.
- `W-9_permutation_null_was_vacuous.md` — Phase 4h's within-receptor arm-permutation null tests "does adding a G protein change structure" (trivially yes); the load-bearing wrong-partner null lives in Block B.
