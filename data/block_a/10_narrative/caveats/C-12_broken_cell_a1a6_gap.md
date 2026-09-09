# C-12 — ACM1-cognate-Protenix broken cell + A1–A6 assertions cannot detect prediction failure

## Caveat

**One cell in the Block A corpus is a prediction failure**: ACM1 / cognate
arm / Protenix backbone. All 25 rows in this cell are:

- `plddt_mean` ≈ 38.66 (typical Block A: 70–90)
- `anchor_mean` ≈ 40.11 (typical: 80–90)
- Median TM6 tilt distance > 30 Å (typical: 12–18 Å)
- Median NPxxY-OH > 20 Å (typical: 4–10 Å active, 10–14 Å inactive)
- Median kink < 60° (only 2 rows; kink is Class B axis so not primary here,
  but the extreme value is diagnostic)

**Every row passes `passed=True`** because the A1–A6 assertion suite does
NOT include a pLDDT floor. The scorer's assertions catch schema violations,
missing files, and structural gate failures, but do not catch
"the model produced garbage at this scale". T6 Part 2 flagged this cell as
DIRTY; T7b confirmed no other cell falls below the mean-pLDDT-of-50 floor.

## The E1 exclusion set

E1 is the pre-specified exclusion of any cell with mean `plddt_mean` < 50.
As of T7b: exactly one cell (ACM1-cognate-Protenix). 25 rows / 9,490 =
**0.263%** of the corpus.

E1 + E2 (model-side atom clashes, 4 rows) removes 29 rows total = 0.31%.

**Per E1–E5 exclusion sweep**: removing E1+E2 shifts every headline number
by ≤ 0.5%. The cell does not shift the campaign-wide story; it does
compromise any per-receptor claim involving ACM1-cognate-Protenix.

## Methods sentence — mandatory

> The scorer's A1–A6 assertion suite catches schema violations, missing
> input files, and structural gate failures. It does NOT include a mean-
> pLDDT floor. One (receptor, backbone, arm) cell in the Block A corpus —
> ACM1 cognate arm on Protenix — falls to mean pLDDT ≈ 39 (versus typical
> 70–90 elsewhere in the campaign), with unfolded TM6 (tilt > 30 Å) and
> displaced TM7 (NPxxY-OH > 20 Å), yet all 25 rows are `passed=True`
> because the assertion suite does not floor confidence. This cell (25 rows
> / 0.263% of the corpus) is excluded from per-cell analyses via
> pre-specified exclusion set E1 (mean `plddt_mean` < 50). Aggregate
> headline numbers are invariant to E1's application (≤ 0.5% shift under
> the E1–E5 exclusion sweep) and are reported both with and without the
> exclusion.

## Related

- MANUSCRIPT_FLAGS.md Flag 24 (ACM1 protenix residual +8.77 Å, from P1b — now confirmed the cell is broken)
- MANUSCRIPT_FLAGS.md Flag 46 (broken cell + A1–A6 gap)
- T6 Part 2 (dirty); T7b (confirmed one cell only)
- E1 exclusion set applied in E1–E5 exclusion sweep fork
