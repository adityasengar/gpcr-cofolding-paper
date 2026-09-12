# ROWS_SPEC_DERIVED.md — reconstructed header for `paper_af3`'s D-tier `rows.csv`

**What this is.** `paper_af3` sent one real `rows.csv` line with no header
(`redo/protocol/received/rows_csv_line.txt`, 2,238 B, from
`experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` — OPSD × boltz × apo × D1,
seed 1800878580, sample 16). This document reconstructs what each of its fields is, so
we can read their row files and, eventually, emit our own in the same shape.

**This is reproduction, not audit.** Where the row and the code disagree, the most likely
explanation is that we are holding six files out of a repository and reading them wrong.
Every item in §3 is phrased as a question for that reason.

**Field count.** The line parses to **102** RFC-4180 fields (101 top-level commas; one
quoted field, #44, containing 19 more). Their covering note says "All 92 columns present"
— see **C5**.

---

## 0. How confidence was graded

The scale is deliberately harsh, because the point of the document is to say what we still
have to ask.

| grade | rule |
|---|---|
| **CERTAIN** | the **received code** names the column, **and** the sample value pins index→name independently — an exact arithmetic reproduction, an exact string-format reproduction, or a literal the code writes unconditionally |
| **INFERRED** | the received code names and computes the quantity, but index→name rests on block order, adjacency or elimination |
| **GUESSED** | the name does **not** appear in the received code. It comes from a header or dossier we already hold (`data/block_a/01_rows/block_a_rows.csv`, `data/block_b/01_rows/rows_tidy.csv`, `data/block_d/05_state_check/`) or from the peer's recovered prose, which per `RECEIVED_LOG.md`'s own caveat is a lead and not authority |
| **UNKNOWN** | nothing we hold explains it |

A consequence worth stating plainly: several **GUESSED** fields are ones we are in practice
very sure of — field 83's digest is byte-identical across all 64 hex characters to the
value on 32,000 Block B rows — but the name lives in a shipped header, not in code, so it
stays GUESSED. §3's ask list separates those from the fields we genuinely cannot name.

**Tally: 33 CERTAIN, 28 INFERRED, 31 GUESSED, 10 UNKNOWN.**

### The three recomputations that carry most of the CERTAIN grades

1. **A100.** Applying the code's own coefficients (`axes.d9c646af.py:355-356`) to fields
   74–78 gives `−14.43·12.280546983770716 − 7.62·10.058053750756157 + 9.11·10.74397310176268
   − 6.32·10.550516069036624 − 5.22·9.522488715929256 + 278.88 = 6.520279747022485` —
   bit-identical to field 79. That single check pins six fields at once and, by adjacency,
   fixes the whole 69–83 block.
2. **Reference deltas.** `(45+46)/2 = 47`, `37−45 = 48`, `37−46 = 49`, all exact to the last
   digit, reproducing `references.d9c646af.py::compute_deltas` and its documented sign
   convention. Pins five fields and, with them, field 37 as the primary axis.
3. **Pocket routing.** For `state_claim="apo"`, `_role_for_state_claim` returns `role=None`,
   so `compute_pocket_axes_bundle` takes `ref = ref_active` (line 1090) and writes
   `ref=fallback:` into the notes (line 1247). Fields 84 and 93 are then the same number by
   construction — and they are, exactly; so are 85 and 95. Pins the entire 84–100 tail.

---

## 1. The 102 fields

Long values are truncated with `…`; nothing else is altered. *(empty)* means a
zero-length field, which is not the same as the literal string `nan` — that distinction
does real work at fields 70–72.

| # | proposed column name | value in the sample row | writer | meaning | confidence |
|---:|---|---|---|---|---|
| 0 | `input_path` | `/hpc/scratch/sengaad1/paper_af3/experiments/02…` | not in received code; name verbatim in the Block A + Block B headers we hold | absolute path of the scored model CIF on their scratch | **GUESSED** |
| 1 | `input_sha256` | `e5ceec00c1d89192111ce8bebba535957a4c5740128687…` | not in received code; name verbatim in the Block A + Block B headers we hold | sha256 of the CIF bytes. Verified NOT the input-YAML sha (9d3090c3…) we hold | **GUESSED** |
| 2 | `receptor_slug` | `OPSD` | not in received code; name verbatim in the Block B header we hold; `receptor_slug` is also the parameter name throughout `references.py`/`pocket_metrics.py`, upper-cased there as here | receptor identifier | **GUESSED** |
| 3 | **?** | `hint` | nothing we hold | value `hint`. Reads like a provenance token — how the receptor was resolved (cf. `receptor_from_path_substring` vs a manifest hint in `propose.py::_expand_rows`) — but nothing we hold names a column or a vocabulary containing `hint` | **UNKNOWN** |
| 4 | `input_state_claim` | `apo` | not in received code; name verbatim in the Block A + Block B headers we hold; the value is `StateClaim.APO.value`, used at `pocket_metrics.d9c646af.py:739` and `:889-903` | the state the input claims. Independently confirmed by field 89: `ref=fallback:` is only reachable when `_role_for_state_claim` returns role=None, i.e. apo/design/class_bc | **GUESSED** |
| 5 | `receptor_seq_len` | `348` | nothing we hold | 348 = exactly the residue count of the dispatched YAML sequence we hold | **GUESSED** |
| 6 | `receptor_chain` | `A` | `receptor_chain_name` is a parameter of `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle`; `receptor_chain` is a column in the Block C census (BLUEPRINT §E4a) | chain id of the receptor in the CIF; `A` matches the YAML `protein: id A` | **GUESSED** |
| 7 | `chain_selection_method` | `identity_match_to_wt` | not in received code; name AND value verbatim in `data/block_d/05_state_check/BLOCK_D_STATE_CHECK.md:69` — "`chain_selection_method = identity_match_to_wt` uniformly across … 42,180 rows" | v2 chain picker (anchor-hit + SIFTS/struct_ref_seq) | **GUESSED** |
| 8 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 9 | **?** | `7a500695564d413831da6eab3ec9abe417714850b504f4…` | nothing we hold | a 64-hex digest. Tested against every artefact we hold (input YAML, CIF path, receptor sequence in several encodings, status JSON) — no match | **UNKNOWN** |
| 10 | **?** | `59f34272ca1bb461de2d4048e1975609b7c755761de985…` | nothing we hold | a second 64-hex digest, same story | **UNKNOWN** |
| 11 | `scorer_git_sha` | `d9c646af5f89861c16062bf256de96a8389d9915` | not in received code; name verbatim in the Block A + Block B headers we hold; the value is the commit label on the source they sent | scorer commit. `data/block_d/08_dossier` records `d9c646af` uniform across all three D tiers | **GUESSED** |
| 12 | `scorer_version` | `0.1.0+d9c646af5f89861c16062bf256de96a8389d9915` | not in received code; name verbatim in the Block A + Block B headers we hold | `0.1.0+<40-hex>` — identical format to Block B's `0.1.0+04243c45…` | **GUESSED** |
| 13 | `bw_source` | `gpcrdb:services/residues/extended` | `bw_numbering.d9c646af.py:118-135` builds `{GPCRDB}/services/residues/extended/{entry}/`; its docstring calls this "THE ONLY SANCTIONED BW SOURCE" | tag naming where BW numbering came from | **GUESSED** |
| 14 | `entry_name` | `opsd_bovin` | `anchors.d9c646af.py::resolve_anchors` → `AnchorSet.entry_name` | GPCRdb entry name. Pinned: field 15 is this string interpolated into the code's URL f-string | **CERTAIN** |
| 15 | `entry_url` | `https://gpcrdb.org/services/residues/extended/…` | `anchors.d9c646af.py:86` — `f"https://gpcrdb.org/services/residues/extended/{entry_name}/"` | GPCRdb residues/extended URL. Byte-exact reproduction of that f-string | **CERTAIN** |
| 16 | `residues_ext_payload_sha256` | `b3a320351982c749d1ffcfdc019b56ca4ad59c0dc7380b…` | `anchors.d9c646af.py:85` — `sha256_json(bw_map)` → `AnchorSet.residues_ext_payload_sha256` | sha of the exact GPCRdb JSON used. Name is the dataclass field; the digest itself is not checkable from what we hold | **INFERRED** |
| 17 | `anchor_3.50_uniprot_pos` | `135` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 3.50. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 18 | `anchor_3.50_aa_expected` | `R` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 3.50. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 19 | `anchor_3.50_aa_observed` | `R` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 20 | `anchor_3.51_uniprot_pos` | `136` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 3.51. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 21 | `anchor_3.51_aa_expected` | `Y` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 3.51. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 22 | `anchor_3.51_aa_observed` | `Y` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 23 | `anchor_5.58_uniprot_pos` | `223` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 5.58. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 24 | `anchor_5.58_aa_expected` | `Y` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 5.58. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 25 | `anchor_5.58_aa_observed` | `Y` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 26 | `anchor_6.30_uniprot_pos` | `247` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 6.30. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 27 | `anchor_6.30_aa_expected` | `E` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 6.30. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 28 | `anchor_6.30_aa_observed` | `E` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 29 | `anchor_6.34_uniprot_pos` | `251` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 6.34. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 30 | `anchor_6.34_aa_expected` | `T` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 6.34. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 31 | `anchor_6.34_aa_observed` | `T` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 32 | `anchor_7.53_uniprot_pos` | `306` | `anchors.d9c646af.py::resolve_anchors` → `Anchor.uniprot_pos` | UniProt position of BW 7.53. Pinned: matches OPSD_BOVIN and `redo/inputs/g0_reference_axis_gap.csv` (anchor_5_58=223, anchor_7_53=306, anchors `3.50|3.51|5.58|6.30|6.34|7.53`) | **CERTAIN** |
| 33 | `anchor_7.53_aa_expected` | `Y` | `anchors.d9c646af.py::AnchorSet.expected_aas` | GPCRdb-expected residue at 7.53. **Which of this cell and the next is expected vs observed cannot be decided** — they are identical on this row | **INFERRED** |
| 34 | `anchor_7.53_aa_observed` | `Y` | `axes.d9c646af.py::observed_aas_at_anchors` | residue actually seen in the model at that position (see caveat on the previous cell) | **INFERRED** |
| 35 | `numbering_method` | `aligned-to-uniprot` | nothing we hold | value `aligned-to-uniprot` — self-describing residue-numbering provenance; the token appears nowhere else in this repo or in the received code | **GUESSED** |
| 36 | `identity_to_wt` | `1.0` | `anchors.d9c646af.py::verify_aa_identity` consumes `model_identity` (= `UnverifiedUniProtModel.identity`) against `anchor_mapping_threshold=0.90` | whole-chain sequence identity to WT. 1.0 ≥ 0.90, consistent with A1 passing (field 52 empty) | **INFERRED** |
| 37 | `d_tm6_r350_r630_ca` | `9.59855080355363` | `axes.d9c646af.py::compute_all_axes` | R3.50 CA – 6.30 CA, Å. Position from block order; the Block B header carries the same five axes in the same relative order | **INFERRED** |
| 38 | `d_npxxy_y558_y753_ca` | `16.86633544130141` | `axes.d9c646af.py::compute_all_axes` | Y5.58 CA – Y7.53 CA, Å (the CA-CA variant, not OH-OH) | **INFERRED** |
| 39 | `d_tm5_outward_r350_r558_ca` | `7.893282058649621` | `axes.d9c646af.py::compute_all_axes` | R3.50 CA – 5.58 CA, Å | **INFERRED** |
| 40 | `d_y558_pack_min_heavy` | `3.139109034710328` | `axes.d9c646af.py::compute_all_axes` | Y5.58 OH → nearest TM3/TM6 heavy atom, Å | **INFERRED** |
| 41 | `d_dry_sidechain_r350cz_e630oe1` | `3.5785226291725474` | `axes.d9c646af.py::compute_all_axes` | R3.50 CZ – 6.30 carboxyl O, Å. 3.58 Å = ionic lock intact, consistent with d_tm6 = 9.60 Å ≈ the inactive reference 8.73 Å | **INFERRED** |
| 42 | `icl2_helical_frac` | `0.21428571428571427` | `axes.d9c646af.py::icl2_helical_frac` | ICL2 helicity over the 14-residue window C-terminal to R3.50. **Pinned**: 0.21428571428571427 = 3/14 exactly, i.e. total=14 = the default `window`, 3 hits | **CERTAIN** |
| 43 | `plddt_mean` | `82.97846549680864` | `axes.d9c646af.py::plddt_mean` | mean pLDDT over the whole receptor chain. **Pinned**: 82.978 ≠ 84.621 = mean of field 44, which rules out the anchor-mean reading (Block A ships that separately) | **CERTAIN** |
| 44 | `plddt_at_anchors` | `[82.12100219726562, 86.98899841308594, 85.0699…` | `axes.d9c646af.py::plddt_at_anchors` | per-anchor pLDDT. 20 values — see contradiction **C2**. Block B's column of this name also holds a 20-element list; Block A calls it `plddt_at_anchors_list` | **INFERRED** |
| 45 | `receptor_d_active_ref` | `14.7211668355467` | `references.d9c646af.py::compute_deltas` (return slot 1); named as a column in its docstring and in `references.d9c646af.py:193-196` | active-reference value of the primary axis. **Pinned** by (45+46)/2 = 47 exactly | **CERTAIN** |
| 46 | `receptor_d_inactive_ref` | `8.725237074143028` | `references.d9c646af.py::compute_deltas` (return slot 2) | inactive-reference value of the primary axis. Same pin | **CERTAIN** |
| 47 | `receptor_midpoint` | `11.723201954844864` | `references.d9c646af.py::compute_deltas` (return slot 3) | (active+inactive)/2. **Pinned**: (14.7211668355467 + 8.725237074143028)/2 = 11.723201954844864 exactly | **CERTAIN** |
| 48 | `delta_to_active` | `-5.12261603199307` | `references.d9c646af.py::compute_deltas` (return slot 4) | current − d_active_ref. **Pinned**: 9.59855080355363 − 14.7211668355467 = −5.12261603199307 exactly | **CERTAIN** |
| 49 | `delta_to_inactive` | `0.8733137294106026` | `references.d9c646af.py::compute_deltas` (return slot 5) | current − d_inactive_ref. **Pinned**: 9.59855080355363 − 8.725237074143028 = 0.8733137294106026 exactly | **CERTAIN** |
| 50 | `confidence_flag` | `borderline` | not in received code; name verbatim in the Block B header we hold | pLDDT confidence bin, **not** a state call. Verified on all 32,000 Block B rows: low <50, borderline 50–70, high ≥70 of `min_plddt_at_anchor`; 64.169 → `borderline` exactly | **GUESSED** |
| 51 | `min_plddt_at_anchor` | `64.16899871826172` | not in received code; name verbatim in the Block A + Block B headers we hold | minimum of field 44. **Value pinned**: min(field 44) = 64.16899871826172 exactly; the same identity holds on all 9,490 Block A rows | **GUESSED** |
| 52 | `A1_amino_acid_identity` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold; the assertion class `A1AminoAcidIdentity` is imported in `anchors.d9c646af.py:16-21` | A1 failure detail, empty on pass | **GUESSED** |
| 53 | `A2_fasta_completeness` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold; `A2FASTATrunc` imported in `anchors.d9c646af.py` | A2 failure detail, empty on pass | **GUESSED** |
| 54 | `A3_wrong_chain` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold | A3 failure detail, empty on pass | **GUESSED** |
| 55 | `A4_reference_class_match` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold; `A4ReferenceClassMismatch` raised in `references.d9c646af.py:269` | A4 failure detail, empty on pass | **GUESSED** |
| 56 | `A5_species_match` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold; `A5SpeciesMismatch` raised in `references.d9c646af.py:301` | A5 failure detail, empty on pass | **GUESSED** |
| 57 | `A6_receptor_identity` | *(empty)* | not in received code; name verbatim in the Block A + Block B headers we hold | A6 failure detail, empty on pass | **GUESSED** |
| 58 | `ref_set_csv_sha256` | `7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a8…` | not in received code; name verbatim in the Block B header we hold | sha of `refs/reference_set.csv`. `data/block_d/05_state_check` records `7a261988` uniform on all D-tier rows; Block B's value is the different `6ee2cad8…`, as expected | **GUESSED** |
| 59 | `run_ts_utc` | `2026-09-06T20:09:33Z` | not in received code; name verbatim in the Block B header we hold | scoring timestamp. Same `…Z` format as Block B, and it falls inside the rescore window in `rescore_parallel.provenance.json` (finished 20:09:52Z) | **GUESSED** |
| 60 | `cache_key` | `3500b88e75b638f3d2390be1bd0202c97161a6bc71c3ff…` | not in received code; name verbatim in the Block B header we hold | 64-hex, same shape as Block B's. The peer's prose names this column for this row | **GUESSED** |
| 61 | `passed` | `True` | not in received code; name verbatim in the Block A + Block B headers we hold | all assertions passed | **GUESSED** |
| 62 | `receptor_class` | `A` | not in received code; name verbatim in the Block B header we hold; `receptor_class` is the parameter name in `axes.py`, `anchors.py`, `pocket_metrics.py`, `references.py` | GPCR class. `A` is correct for OPSD and is what makes field 63 empty | **GUESSED** |
| 63 | `not_applicable_axes` | *(empty)* | `axes.d9c646af.py:112-133`, whose docstring says verbatim: "Used to populate the `not_applicable_axes` annotation column on ScorerRow" | axes not calibrated for this class. Empty is exactly `not_applicable_axes_for('A')` — every axis in `AXIS_APPLICABILITY` includes `A` | **INFERRED** |
| 64 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 65 | `seed_used` | `1800878580` | `propose.d9c646af.py:707` — `row["seed_used"] = str(seed)` | the seed. **Pinned**: matches the `seed_1800878580` path segment and `_boltz_status.json` `seed` / `seed_passed` | **CERTAIN** |
| 66 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 67 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 68 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 69 | `d_npxxy_y558_y753_oh` | `12.470604390750273` | `axes.d9c646af.py::d_npxxy_y558_y753_oh` | Y5.58 OH – Y7.53 OH, Å — predicate axis 1. Position rests on elimination plus the peer's prose, which quotes this exact 17-digit value for this column name | **INFERRED** |
| 70 | `d_ga_alpha5_r350_ca` | `nan` | not in received code; name verbatim in the Block A + Block B headers we hold | Gα α5 tip depth. **Discriminated**: on all 8,000 Block B apo rows this trio is the literal `nan` while the RMSD family is `''` or numeric and never `nan`. Order within 70–72 assumed from the Block B header | **GUESSED** |
| 71 | `n_interface_contacts_ga_receptor` | `nan` | not in received code; name verbatim in the Block A + Block B headers we hold | receptor–Gα contact count; `nan` with no partner (same discrimination) | **GUESSED** |
| 72 | `plddt_ga_alpha5` | `nan` | not in received code; name verbatim in the Block A + Block B headers we hold | pLDDT over the Gα α5 helix; `nan` with no partner | **GUESSED** |
| 73 | `d_gpcrdb_tm6_tilt_246_637_ca` | `14.014953229750716` | `axes.d9c646af.py::compute_all_axes` | 2.46 CA – 6.37 CA, Å — predicate axis 2. Position by adjacency to the pinned A100 block | **INFERRED** |
| 74 | `a100_component_1_ca` | `12.280546983770716` | `axes.d9c646af.py::compute_all_axes` | 1.53 CA – 7.55 CA. **Pinned by recomputation** — see the A100 check below | **CERTAIN** |
| 75 | `a100_component_2_ca` | `10.058053750756157` | `axes.d9c646af.py::compute_all_axes` | 2.50 CA – 3.37 CA | **CERTAIN** |
| 76 | `a100_component_3_ca` | `10.74397310176268` | `axes.d9c646af.py::compute_all_axes` | 3.42 CA – 4.42 CA | **CERTAIN** |
| 77 | `a100_component_4_ca` | `10.550516069036624` | `axes.d9c646af.py::compute_all_axes` | 5.66 CA – 6.34 CA | **CERTAIN** |
| 78 | `a100_component_5_ca` | `9.522488715929256` | `axes.d9c646af.py::compute_all_axes` | 6.58 CA – 7.35 CA | **CERTAIN** |
| 79 | `a100_index` | `6.520279747022485` | `axes.d9c646af.py::compute_all_axes` | **Pinned**: −14.43·(74) −7.62·(75) +9.11·(76) −6.32·(77) −5.22·(78) + 278.88 = 6.520279747022485, bit-identical to the field | **CERTAIN** |
| 80 | `angle_class_b_tm6_kink_639_650_654_deg` | `158.81597700147006` | `axes.d9c646af.py::compute_all_axes` | Cα-Cα-Cα angle at 6.39/6.50/6.54, degrees | **INFERRED** |
| 81 | `threshold_npxxy_oh_active_lt` | `9.08` | not in received code; name verbatim in the Block B header we hold | active iff axis 1 < this. **Byte-identical** to the value on all 32,000 Block B rows (`9.08`) | **GUESSED** |
| 82 | `threshold_gpcrdb_tm6_tilt_active_gt` | `14.932` | not in received code; name verbatim in the Block B header we hold | active iff axis 2 > this. Byte-identical to Block B (`14.932`) | **GUESSED** |
| 83 | `thresholds_panel_csv_sha256` | `242b509f7b7af56669d72cd71906d91edd18ef43706c21…` | not in received code; name verbatim in the Block B header we hold | sha of the thresholds panel. **Byte-identical across all 64 hex chars** to Block B's value — the strongest non-code attestation in the row | **GUESSED** |
| 84 | `pocket_ca_rmsd` | `1.187699237032282` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` (dict key; its docstring calls these "the six pocket-metric columns") | pocket CA RMSD to the role-matched reference. **Pinned**: equals field 93 exactly, which is what the code produces when `role=None` → `ref = ref_active` | **CERTAIN** |
| 85 | `pocket_sidechain_rmsd` | `2.220162820414681` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` | pocket side-chain RMSD. **Pinned**: equals field 95 exactly, same argument | **CERTAIN** |
| 86 | `w648_chi1` | `75.10539480760785` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` → `pocket_metrics.d9c646af.py::w648_chi1` | toggle-switch W6.48 χ1, degrees. Position by adjacency | **INFERRED** |
| 87 | `ligand_rmsd_to_ref` | `nan` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` → `ligand_rmsd_to_ref` | `nan` because `input_state_claim == "apo"` returns `(NaN, "apo_no_ligand", "")` at line 739-740 — the note half of that same return is visible in field 89 | **INFERRED** |
| 88 | `pocket_ca_rmsd_missing_residues *or* pocket_ligand_atom_map_method` | *(empty)* | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` | **The two are not separable on this row** — both are `""` here. One of them is field 88 and the other is field 90 | **INFERRED** |
| 89 | `pocket_notes` | `lig:apo_no_ligand;ref=fallback:4X1H;7tm_n=227` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` | **Pinned**: `lig:apo_no_ligand` is line 1181 + line 740; `ref=fallback:` is line 1247 with `role or 'fallback'`; `7tm_n=` is line 1248. Block B's `pocket_notes` has the identical shape (`lig:apo_no_ligand;ref=fallback:6G79;7tm_n=223`) | **CERTAIN** |
| 90 | `the other of the field-88 pair` | *(empty)* | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` | see field 88 | **INFERRED** |
| 91 | **?** | *(empty)* | nothing we hold | empty | **UNKNOWN** |
| 92 | `ligand_slug` | `apo_no_ligand` | nothing we hold | `apo_no_ligand` — the same token as the `input_path` segment and as the note in field 89. No held file names a column for it | **GUESSED** |
| 93 | `pocket_ca_rmsd_active` | `1.187699237032282` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1200 | pocket CA RMSD against the ACTIVE reference, own Kabsch. Block pinned at both ends by fields 97/98 and the literals in 99/100; dict order then forces 93–96 | **CERTAIN** |
| 94 | `pocket_ca_rmsd_inactive` | `1.1628521312930702` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1239 | same against the inactive reference | **CERTAIN** |
| 95 | `pocket_sidechain_rmsd_active` | `2.220162820414681` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1201 | side-chain variant, active | **CERTAIN** |
| 96 | `pocket_sidechain_rmsd_inactive` | `1.0393045709856719` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1240 | side-chain variant, inactive | **CERTAIN** |
| 97 | `pocket_ref_pdb_sha_active` | `02b285a2ed63ff0d1de5e86938a45383b8453ea4d2f984…` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1202-1204; named as a column at `pocket_metrics.d9c646af.py:173-175` | provenance sha of the active reference PDB | **CERTAIN** |
| 98 | `pocket_ref_pdb_sha_inactive` | `b69af7a9eade63d8a1df9d3c4c4d322a613903887cd7ab…` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1241-1243 | provenance sha of the inactive reference PDB | **CERTAIN** |
| 99 | `pocket_ref_role_active` | `active` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1205 — `out["pocket_ref_role_active"] = "active"` | **Pinned**: the code writes this literal unconditionally when `ref_active` exists | **CERTAIN** |
| 100 | `pocket_ref_role_inactive` | `generic_inactive_fallback` | `pocket_metrics.d9c646af.py::compute_pocket_axes_bundle` line 1233 — `inactive_role_tag = "generic_inactive_fallback"` | **Pinned**: that literal is reachable only via `role != "inactive"` and empty `ligand_role` — exactly this row | **CERTAIN** |
| 101 | **?** | *(empty)* | nothing we hold | empty; the line ends with a comma, so this may be a real 102nd column or a trailing-separator artefact | **UNKNOWN** |
---

## 2. Blocks — do the 102 fields group into identity / inputs / geometry / confidence?

**Mostly, with five clean seams and three genuine violations.**

| fields | block | seam quality |
|---:|---|---|
| 0–16 | **identity + provenance** — path, two content hashes, two unexplained hashes, scorer stamp, GPCRdb source/entry/URL/payload hash | clean |
| 17–36 | **anchors** — six `(uniprot_pos, aa, aa)` triples, then numbering method and identity-to-WT | clean at 17 and 37 |
| 37–51 | **legacy six-axis geometry, reference deltas, confidence** | clean at 37; **internally mixed** |
| 52–68 | **gates + run provenance** — A1–A6, ref-set hash, timestamp, cache key, `passed`, class, seed | clean at 52 |
| 69–83 | **predicate axes, literature metrics, thresholds** | clean at 69 and 84 |
| 84–101 | **pocket metrics**, ending in the eight dual-reference columns | clean; ends the row |

The seams at **17, 37, 52, 69 and 84** are sharp — each is the first field of a coherent
group and the field before it is the last of the previous one.

Three things break the tidy picture, and they matter when reading the file:

- **Confidence is not one block.** `plddt_mean` (43) and `plddt_at_anchors` (44) sit
  *before* the reference-delta run 45–49, and `confidence_flag` (50) and
  `min_plddt_at_anchor` (51) sit *after* it. The four confidence fields are split around
  five geometry fields. Block B's `rows_tidy.csv` keeps all four adjacent and in the order
  `plddt_mean, plddt_at_anchors, min_plddt_at_anchor, confidence_flag` — so D has both
  split them and swapped the last two.
- **Provenance appears four separate times**: 0–1, 9–16, 58–62, and again at 83.
- **The partner-engagement trio (70–72) sits inside the predicate block**, between the two
  thresholded axes. In Block B those three live together after `confidence_flag`.

So: identity / inputs / geometry / confidence is the right mental model for 5 of the 6
blocks, but "confidence" is not contiguous and "provenance" is scattered. Any reader of
these files must go by name, never by position.

---

## 3. What we still have to ask

### 3.0 The ask that makes every other one redundant

**A-0. Send `head -1 experiments/022_tier_d1_deep_apo/analysis/full/rows.csv`.** One line.
It closes §3.1, §3.2 and §3.3 completely and turns this whole document into a check on our
own reading. Everything below is what to ask *if* that line is awkward to extract.

### 3.1 Fields nothing we hold explains — 10 (UNKNOWN)

| ask | field | value | what we need |
|---|---:|---|---|
| A-1 | 3 | `hint` | The column name and its full vocabulary. `hint` is not an `arm` value (`apo/cognate/decoy/shuffled`), not a `cluster_id`, not an `active_stabilization_source`. Our guess is a receptor-resolution provenance token, but it is only a guess. |
| A-2 | 9 | `7a500695…` | What is hashed? Not the input YAML (`9d3090c3…`), not the CIF (field 1), not the receptor sequence in any encoding we tried. |
| A-3 | 10 | `59f34272…` | Same question. Two adjacent unexplained digests is the largest single gap in the row. |
| A-4 | 8 | *(empty)* | Name, and what a populated value looks like. |
| A-5 | 64, 66, 67, 68 | *(empty)* | Four empty fields interleaved with `seed_used` (65) in the run-provenance block. Names, and one example row where each is populated. |
| A-6 | 91 | *(empty)* | Sits between the pocket-notes group and the ligand slug. |
| A-7 | 101 | *(empty)* | The line ends with a comma. Is there a real 102nd column, or is this a trailing separator — i.e. is the header 101 names or 102? |

### 3.2 Fields we can name from files we already hold, but cannot place — 31 (GUESSED)

These need confirmation, not explanation. We have the name verbatim in a Block A, Block B
or Block D artefact; what we cannot prove is that the name belongs at that index.

- **Identity / provenance (11):** 0 `input_path`, 1 `input_sha256`, 2 `receptor_slug`,
  4 `input_state_claim`, 5 `receptor_seq_len`, 6 `receptor_chain`,
  7 `chain_selection_method`, 11 `scorer_git_sha`, 12 `scorer_version`, 13 `bw_source`,
  92 `ligand_slug`.
  *(5, 13 and 92 are the weak ones here — no held file names a column for them; 5 is
  "348 = the exact residue count of the YAML you sent", 13 is the BW endpoint string, 92 is
  the `input_path` ligand segment.)*
- **Gates + run provenance (11):** 52–57 `A1_amino_acid_identity` … `A6_receptor_identity`,
  58 `ref_set_csv_sha256`, 59 `run_ts_utc`, 60 `cache_key`, 61 `passed`, 62 `receptor_class`.
- **Confidence (2):** 50 `confidence_flag`, 51 `min_plddt_at_anchor`.
- **Partner engagement (3):** 70 `d_ga_alpha5_r350_ca`,
  71 `n_interface_contacts_ga_receptor`, 72 `plddt_ga_alpha5` — and please confirm the
  order, which we took from the Block B header.
- **Thresholds (3):** 81, 82, 83.
- **Numbering (1):** 35 `numbering_method`, value `aligned-to-uniprot` — this token appears
  nowhere in the received code or in any Block A–D artefact we hold. What are its other
  possible values?

### 3.3 Ordering ambiguities inside otherwise-solid blocks — 4

| ask | where | the ambiguity |
|---|---|---|
| A-8 | 18/19, 21/22, 24/25, 27/28, 30/31, 33/34 | Each anchor carries two amino-acid cells. `expected_aas()` and `observed_aas_at_anchors()` both exist in the code and **both values are identical on this row**, so we cannot tell which comes first. A single row with an A1 mismatch would settle it forever. |
| A-9 | 44 | The 20 pLDDT values are unlabelled. What is the BW-label order? Without it the list is unusable per-anchor. |
| A-10 | 88 / 90 | `pocket_ca_rmsd_missing_residues` and `pocket_ligand_atom_map_method` are both `""` here. Which index is which? |
| A-11 | 70–72 | Order of the partner trio (see 3.2). |

---

## 4. Where the sample row and the code do not agree

Five items. **C1 and C2 are the ones worth their time.**

### C1 — The row is scored by a two-instrument predicate; the code at the stamped commit says the predicate is single-metric

The row's `scorer_git_sha` is `d9c646af…`. In `axes.d9c646af.py`, the header comment over
the literature metrics (lines 288–296) reads:

> These are ADDITIVE geometry columns — the current single-metric NPxxY-OH predicate does
> NOT depend on them (see scorer/switch_signal.py::MotifThresholds, user-locked).

`d_gpcrdb_tm6_tilt_246_637_ca` is defined immediately under that comment (line 318). Yet
the same row carries **two** threshold columns — field 81 `9.08` for the NPxxY-OH axis and
field 82 `14.932` for exactly that tilt axis — and the peer's own trace derives the verdict
from both ("`d_npxxy_oh > 9.08` … AND `d_tm6_tilt < 14.932` … → this row is INACTIVE by the
two-instrument predicate"). The same threshold pair is byte-identical on all 32,000 Block B
rows we hold, which were stamped `04243c45` — where the identical comment is present.

`references.d9c646af.py:30-34` makes it a three-way disagreement: it says classification
"uses the full 6-axis vector (TM6, NPxxY, TM5-out, Y5.58-pack, DRY, ICL2)". Neither
thresholded axis is in that list — the NPxxY there is the CA-CA variant (field 38); the
thresholded one is OH-OH (field 69).

**Ask:** `scorer/switch_signal.py` (`MotifThresholds`) and whatever module actually applies
the thresholds. We hold neither, and the comment in the module we do hold points away from
the thing that produced the row.

### C2 — The row's own anchor block says six anchors; the row's pLDDT list says twenty

`anchors.d9c646af.py`'s docstring: *"Every scored row identifies exactly six anchors … 3.50,
3.51, 5.58, 6.30, 6.34, 7.53."* Fields 17–34 are exactly those six, in that order.

But:

- Field 44 holds **20** values, and `axes.plddt_at_anchors` iterates
  `model.anchor_set.anchors` — so the anchor set has 20 entries, not 6.
- This is not one-off: across all **9,490** Block A rows, `plddt_at_anchors_list` is 20 long
  on 8,595 and 19 long on 895.
- It has to be 20, because the populated literature axes dereference fifteen further BW
  labels through the same `model.anchor_set.anchors` — 2.46, 6.37 (field 73); 1.53, 7.55,
  2.50, 3.37, 3.42, 4.42, 5.66, 6.58, 7.35 (fields 74–78); 6.39, 6.50, 6.54 (field 80).
  Union with the six documented anchors = **exactly 20 labels.** If the anchor set were six,
  fields 73–80 would all be NaN. They are not.

**Ask:** `scorer/schema.py::ANCHOR_KEYS`, plus the ordering of field 44 (see A-9). The
docstring is stale in a way that would have sent our reconstruction down the wrong path.

### C3 — `icl2_helical_frac`: the docstrings say [3.8, 4.5] Å, the code tests [3.8, 6.4] Å

`axes.d9c646af.py:26-28` (module docstring) and `:449-450` (function docstring) both give
the α-helix window as `3.8..4.5 Å`. Line 464 is `if 3.8 <= d <= 6.4:`. The sample value
0.21428571428571427 = 3/14 is produced by the code as written. The code looks right —
Cα(i)–Cα(i+4) in an α-helix is ≈6.2 Å, so a 4.5 Å ceiling would score almost nothing — but
anyone reimplementing from the docstring gets a different column. **Ask:** confirm 6.4 Å is
intended and the docstrings are the stale half.

### C4 — Two different threshold files are named

`axes.d9c646af.py:4-7` says thresholds "live in `refs/state_thresholds.csv` and are
consulted only at classification time in `scorer/references.py`". The `references.py` we
hold contains no threshold read and no classification function at all — only
`compute_deltas`. And the row provenances its thresholds to a *thresholds panel* CSV
(field 83), not to `state_thresholds.csv`. **Ask:** which file is of record, and which
module reads it. Same underlying gap as C1.

### C5 — "All 92 columns present"; the line has 102 fields

Their covering note for `rows_csv_line.txt` says 92. We count 102 (101 top-level commas;
field 44 is quoted and contributes 19 internal commas that are not separators). Cheapest
possible resolution: A-0.

### C6 — Absences, stated rather than inferred (not contradictions — confirmations)

- **No state/verdict column.** The row carries both predicate axes and both thresholds and
  nothing holding the resulting call. No field has the value `inactive`; the only boolean
  is field 61 `passed`. Block A ships `active` / `npxxy_active` / `tilt_active`; Block B
  ships none; D appears to ship none. This confirms our own §E4b reading rather than
  contradicting it, but it should be recorded: **the state call is not in the row file.**
- **No `backbone` column.** No field equals `boltz`. This answers our blueprint question
  **I4** for D-tier: backbone is recoverable only from `input_path`. (Confirm via A-0.)

---

## 5. Checked, and NOT a finding

Recorded because it is what makes §4 believable. Every one of these looked like a defect
first.

1. **Field 50 `borderline` vs their "non-borderline in both axes".** Looked like the row
   contradicting their own trace. It does not: field 50 is `confidence_flag`, not a state
   call. On all 32,000 Block B rows `confidence_flag` is a pure function of
   `min_plddt_at_anchor` — `low` below 50, `borderline` 50–70, `high` at or above 70. This
   row's `min_plddt_at_anchor` is 64.169, so `borderline` is exactly right and says nothing
   about active/inactive.
2. **`ref=fallback:4X1H` paired with `pocket_ref_role_active = active`.** 4X1H reads like
   dark-state rhodopsin, so this looked like an active/inactive swap. It is not a new
   finding: `redo/inputs/g0_reference_axis_gap.csv` and `redo/spec/PANEL.md` both record
   OPSD active = 4X1H / inactive = 7ZBC, and PANEL.md *already* flags 4X1H's annotation as
   a known, separately-recorded defect ("the one core receptor whose active reference is
   known to be mis-annotated"). The row is internally consistent with that reference set:
   84 = 93 and 85 = 95 exactly, which is only true if the primary reference *is* the active
   one.
3. **Field 43 (82.978) is not the mean of field 44 (84.621).** Not an error. 43 is
   `plddt_mean` over the whole chain; 44 is the anchor list. Block A ships both quantities
   as separate columns (`plddt_mean`, and `plddt_at_anchors` which there holds the anchor
   *mean*). The mismatch is what proves field 43 is the chain mean.
4. **Fields 9 and 10 might have been the input-YAML hash.** They are not — we hold that
   file and its sha is `9d3090c3…`, which appears nowhere in the row. Nor are they the CIF
   hash (field 1). Genuinely unexplained, so they are in the ask list rather than assigned.
5. **Fields 70–72 might have been the RMSD family** (`rmsd_to_active_ref`,
   `rmsd_to_inactive_ref`, `rmsd_pos`). Checked against Block B: on all 8,000 apo rows the
   RMSD family is `''` or a number and **never** the literal `nan`, while
   `d_ga_alpha5_r350_ca` / `n_interface_contacts_ga_receptor` / `plddt_ga_alpha5` are the
   literal `nan` on all 8,000. The empty-vs-`nan` distinction settles it.
6. **Our own drift, not theirs.** `data/block_d/08_dossier/EXPERIMENT_DOSSIER_BLOCK_D.md`
   states the predicate as "NPxxY-OH < **9.082** Å". The row carries `9.08`, and so do all
   32,000 Block B rows. Worth one line in the ask ("is the stored threshold 9.08 exactly, or
   a rounded print of 9.082?") and a correction on our side either way.
7. **The two commits we hold do not explain any of the above.** `diff axes.04243c45.py
   axes.d9c646af.py` is imports only — the axis functions, the A100 coefficients and the
   "single-metric predicate" comment are identical at both commits.
   `diff references.04243c45.py references.d9c646af.py` is the Block C `role_specific`
   addition only. So C1 and C2 are not artefacts of comparing across commits.
