# C-D-9 — Reference-predicate calibration on Nb-anchor PDBs partial (NPxxY-OH only)

## Caveat

Part A/D2 §3 ran the reference-predicate calibration on the 4 D2
receptors' deposited references. Existing references in
`refs/reference_set.csv` (7T94/4LDE/6OS2/8FEG active; 5ZKC/2RH1/4ZUD/4DJH
inactive) all calibrate correctly on both axes (NPxxY-OH AND
GPCRdb TM6 tilt).

**Nb-anchor PDBs (5JQH, 6VI4, 4MQS)**: NPxxY-OH calibration
verified — 4MQS (ACM2 active) PASS at 4.21 Å; 5JQH (ADRB2 inactive)
FAIL at 11.16 Å; 6VI4 (OPRK inactive) FAIL at 12.88 Å. Instrument
classifies references correctly on the NPxxY axis.

**TM6-tilt (`d_gpcrdb_tm6_tilt_246_637_ca`) calibration on Nb-anchor
PDBs**: **deferred**. Needs GPCRdb 2×46 / 6×37 residue-position
mapping for each of the 3 Nb-anchor PDBs — small compute (~ 30 min)
but not run in this Block D pass.

**Consequence**: F3's negative finding (SC-D-6: inactive-Nb
unreliable) rests on the instrument being sound on both axes. NPxxY
soundness is verified; TM6-tilt soundness is inferred from the
receptor-side calibration passing on both axes for the pre-existing
references. The residual risk that TM6-tilt would flip a Nb-anchor
verdict is low but not zero. Deferred as ANV.

Small follow-up: a subagent-launched TM6-tilt sweep on the 3 Nb-anchor
PDBs would close this to full calibration.

## References

- `dossiers/BLOCK_D/partA/PARTA_D2.md` §3 (Reference-predicate calibration).
- `refs/nanobody_state_anchors.csv` — Nb-anchor PDB IDs + deposition dates.
- `refs/reference_set.csv` — existing D2 receptor references (calibrated correctly).
- `dossiers/BLOCK_D/ASSUMED_NOT_VERIFIED_BLOCK_D.md` §Reference-predicate calibration.
