# A3 chain-picker diagnostic report — 2026-08-26

## Symptom

M2.2 v3.1 rescore: every `w40_ADRB2_alpha5_*aa` row and every `w47_adrb2_*` row (100% within each experiment) fails A3 `wrong_chain`. Together ~340 rows blocked.

## Root cause

`scorer/structure.py::align_numbering` has an off-by-N corruption when the chain sequence contains a mid-sequence insert (TEV cleavage site, linker, tag) longer than a point mutation but shorter than the `max_gap_fill=30` threshold.

### Reproduction (real w40 row)

Sample input: `/hpc/scratch/sengaad1/subsampling/outputs/w40_ADRB2_alpha5_15aa/predictions/boltz_results_input/predictions/input/input_model_0.pdb`

Chain A: 460 residues. First 60:
```
    MKTIIALSYIFCLVFA DYKDDDDA MGQPGNGSAFLLAPN R SHAPDHDV ENLYFQGT QQRDEVWVV...
    [signal 16aa   ][FLAG 8aa][ADRB2 N-ter    ][mut][ADRB2 ][TEV site]        [ADRB2 continues]
```

WT ADRB2 (413aa): `MGQPGNGSAFLLAPN G SHAPDHDV T QERDEVWVVGMGIVMS...`

Expected alignment:
```
    chain[24..38] → WT[1..15]   (block A, 15 residues match)
    chain[39]     → WT[16]      (1-aa mutation R vs G)
    chain[40..47] → WT[17..24]  (SHAPDHDV, matches)
    chain[48..55] → TEV insert  (unmatched, correctly gapped)
    chain[56..end] → WT[25..end] (QQRDEVWVVGMGIVMS..., matches)
```

### What the aligner produces

```
    mapping = align_numbering(residues, wt_seq)
    mapping[24..38] = 1..15         # block A, correct
    mapping[39..57] = 16..34        # WRONG — extrapolated from LEFT flank only
    mapping[58..end] = 35..end      # SHIFTED +7 by "strictly increasing" enforcer
```

The mapping walks `chain[58] → WT[35]` when the correct answer is `chain[58] → WT[28]`. Every residue past index 58 is compared to WT+7, so `_score_aligned` reports identity=49/430=12% and A3 fires.

## Code trace

Lines 155-175 of `scorer/structure.py::align_numbering`:

```python
    # Short-gap extrapolation only. Long gaps (fusion inserts) stay
    # unmapped — their residues do not get UniProt numbers.
    for i in range(len(obs)):
        if i in mapping:
            continue
        left = i - 1
        while left >= 0 and left not in mapping:
            left -= 1
        right = i + 1
        while right < len(obs) and right not in mapping:
            right += 1
        gap_left = i - left if left >= 0 else float("inf")
        gap_right = right - i if right < len(obs) else float("inf")
        gap_span = (right - left - 1) if (left >= 0 and right < len(obs)) else max(gap_left, gap_right)
        if gap_span > max_gap_fill:
            continue  # fusion insert — leave unmapped
        if left >= 0:
            mapping[i] = mapping[left] + (i - left)   # extrapolates from LEFT only
        elif right < len(obs):
            mapping[i] = mapping[right] - (right - i)

    # enforce strictly increasing numbers over the mapped subset
    last = None
    for i in sorted(mapping):
        if last is not None and mapping[i] <= last:
            mapping[i] = last + 1                     # rotates 58->28 to 58->35
        last = mapping[i]
```

**The bug:** the extrapolation naively fills from LEFT without checking that the RIGHT flank position is compatible. Then the strictly-increasing enforcer treats the fake extrapolation as authoritative and shifts every downstream real match to accommodate.

## Fix (minimal diff)

Two-line change in `align_numbering`: before extrapolating over a gap, verify the flanks are position-consistent — i.e. `mapping[right] == mapping[left] + (right - left)`. If they are NOT (indicating the gap contains an insert or deletion), leave the gap unmapped rather than fabricating positions.

```python
        # Consistency check: if BOTH flanks are known, only extrapolate
        # linearly when the flank positions are exactly (right - left)
        # apart. If they differ, the gap contains an insert or deletion
        # and extrapolation would fabricate false positions that later
        # get amplified by the strictly-increasing enforcer.
        if left >= 0 and right < len(obs):
            flank_delta = mapping[right] - mapping[left]
            if flank_delta != (right - left):
                continue  # insert/deletion in this gap — leave unmapped
```

Plus one safety line in the enforcer: only bump a mapping value if the collision was NOT caused by an insert (i.e. only when the previous position is truly consecutive in the observed sequence). This is a defensive belt-and-braces guard.

## Impact

Row recovery: ~340 rows currently 100% A3-failing (w40 + w47 + w7a adrb2 mutants).

Wave 40 sanity gate: currently BLOCKED (0 rows pass A3 → no active-rate computable). Fix unblocks the paper's built-in Boltz 90 / OF3 80 / Ptx 29 validation.

No design-principle change: 70% identity + 200 matched residues thresholds stay unchanged. Fix corrects a genuine bookkeeping error in the alignment function, not a policy relaxation.

## Test coverage

Add `tests/test_structure_align.py::test_tev_insert_alignment` with a synthetic construct sequence `signal_peptide + FLAG + WT[1:30] + TEV_site + WT[30:end]` and assert that `_score_aligned` reports identity > 70% against the WT.

## Alternative approach (coordinator suggestion)

Swap `difflib.SequenceMatcher` to `gemmi.align_string_sequences` (Needleman-Wunsch, handles inserts natively via proper gap penalties). Cleaner but bigger diff. The minimal-diff flank-consistency fix above is preferred because it's ~4 lines and easy to review; NW swap would be ~20 lines and requires re-validating F1-F6 fixture behavior.
