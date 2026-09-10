# withdrawals/ (Block B)

One file per retracted Block B claim. Reason, evidence, dossier reference,
and the sentence the manuscript would have used if the claim survived.

**Format**: `W-B-<N>_<slug>.md`. Content: (a) the claim as stated, (b) the
reason for retraction, (c) evidence citations (dossier phase + script +
input SHA), (d) the corrected sentence if one exists.

Retractions are load-bearing for credibility. Reviewers who see a paper
that never withdraws anything have a different reaction than reviewers
who see a paper with a transparent retraction ledger.

## Distinction from Block A withdrawals

Block A's withdrawals (paper_af3_release/withdrawals/W-*.md) are numbered
W-1..W-9 without a block prefix. Block B's withdrawals use the W-B-N
prefix. W-B-3 is a Block-B-internal inversion between Phase 5 (as run)
and Phase 6b (native-only power); the other four active entries (W-B-1,
W-B-2, W-B-5, W-B-6) retire dispatch-era misattributions or figures
that do not reproduce on the delivered 32,000-row corpus.

**W-B-4 was moved to SC-B-14** on 2026-09-10 (post-freeze reclassification).
Pre-registered Outcome B did not sign; that is a signed test result on a
pre-registered alternative, not a retracted claim. See
`docs/BLOCK_B_POSTFREEZE_CHECKS.md` Check 4. The W-B-4 file remains as a
pointer stub so the numbering series stays auditable.

## Block B retractions

- `W-B-1_family_term_11pct_bare_number.md` — "Family term is ~11% of the ladder" as a single scale-neutral number
- `W-B-2_midpoint_ladder_28_receptor.md` — Per-receptor midpoint ladder 0.130 / 0.500 / 0.801 / 0.887
- `W-B-3_gs_to_gq_third_finding_manuscript_line.md` — Phase 5 Gs→Gq third finding (−0.47 Å tilt) as manuscript line
- `W-B-4_outcome_b_reads_partner_identity.md` — **MOVED to `BLOCK_B_CLAIM_SHEET.md` SC-B-14** (2026-09-10 post-freeze; pre-registered non-signature is a result, not a retraction)
- `W-B-5_dispatch_plan_block_a_shuffled_94pct.md` — "Shuffled at 94% active in Block A" — dispatch-plan misattribution (Block A had no shuffled arm)
- `W-B-6_1263_of_1935_non_inserted_decoy.md` — "1,263 of 1,935 non-inserted decoy rows make > 20 contacts" as an exact reproducible pair
