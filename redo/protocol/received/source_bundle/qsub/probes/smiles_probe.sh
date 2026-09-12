#!/bin/bash
#
# qsub/probes/smiles_probe.sh - Gate 0.2 SMILES-probe driver.
#
# Iterates experiments/020_block_c_ligand_pharmacology/manifest/
# smiles_probe_manifest.csv and submits one qsub per (backbone, cell)
# against the existing qsub/rerun_${BACKBONE}.sh launchers. Existing
# launchers are UNMODIFIED - the probe uses only their public env
# contract (PRED_INPUT, PRED_OUT_DIR, PRED_SEED, PRED_SIDECAR).
#
# This driver runs on a login node OR a laptop with `ssh basel-hpc`
# capability. It is NOT itself qsub-submitted.
#
# Env contract:
#   BACKBONE            (optional) if set, only submit that backbone's rows
#   CELL_ID             (optional) if set, only submit that cell_id
#   PROBE_ROOT          (default: paper_af3/experiments/020_block_c_ligand_pharmacology)
#   PROBE_SCRATCH       (default: /hpc/scratch/sengaad1/paper_af3/experiments/
#                                 020_block_c_ligand_pharmacology/probes/smiles)
#   DRY_RUN             (default: 0) if 1, print qsub commands but do not submit
#   HOLD_JID            (optional) chain the job after this SGE job id
#   REMOTE_HOST         (default: basel-hpc) hostname to ssh to for qsub

set -euo pipefail

PROBE_ROOT="${PROBE_ROOT:-$HOME/Documents/claude/paper_af3/experiments/020_block_c_ligand_pharmacology}"
PROBE_SCRATCH="${PROBE_SCRATCH:-/hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/probes/smiles}"
REMOTE_HOST="${REMOTE_HOST:-basel-hpc}"
DRY_RUN="${DRY_RUN:-0}"
MANIFEST="${PROBE_ROOT}/manifest/smiles_probe_manifest.csv"

[ -f "$MANIFEST" ] || { echo "FATAL: manifest missing: $MANIFEST" >&2; exit 1; }

# Local paths on HPC (rsync-ed). The rerun_*.sh launchers read PRED_INPUT
# as an absolute path on the compute node.
HPC_MANIFEST_ROOT="$PROBE_SCRATCH/manifest"

echo "=== Gate 0.2 SMILES probe driver ==="
echo "PROBE_ROOT     : $PROBE_ROOT"
echo "PROBE_SCRATCH  : $PROBE_SCRATCH"
echo "MANIFEST       : $MANIFEST"
echo "BACKBONE filter: ${BACKBONE:-<none>}"
echo "CELL_ID filter : ${CELL_ID:-<none>}"
echo "DRY_RUN        : $DRY_RUN"
echo ""

# Ensure remote directory tree exists AND rsync inputs across.
if [ "$DRY_RUN" != "1" ]; then
    ssh "$REMOTE_HOST" "mkdir -p $HPC_MANIFEST_ROOT/inputs/{boltz,chai,of3,protenix} $PROBE_SCRATCH/out $PROBE_SCRATCH/sidecars $PROBE_SCRATCH/logs"
    echo "-- rsync-ing manifest + inputs to $REMOTE_HOST:$HPC_MANIFEST_ROOT --"
    rsync -a --delete "$PROBE_ROOT/manifest/" "$REMOTE_HOST:$HPC_MANIFEST_ROOT/"
    echo "-- done --"
    echo ""
fi

# Locate the four backbone launchers on HPC. Standing convention: they
# live at /home/sengaad1/paper_af3/qsub/rerun_*.sh (HPC checkout of the
# `qsub/` folder maintained via rsync from laptop).
RERUN_ROOT_HPC="/home/sengaad1/paper_af3/qsub"

# Track submitted job ids for the follow-up analysis pass.
JOBIDS_FILE="$PROBE_ROOT/analysis/_dispatched_jobids.txt"
: > "$JOBIDS_FILE"

# Skip header. CSV columns:
#   cell_id, backbone, receptor, receptor_seq_sha, ligand_name, ligand_type,
#   ligand_smiles_or_seq, ligand_inchi, tautomer_notes, protonation_notes,
#   approx_ligand_heavy_atoms, input_relpath, input_sha256, seed, notes
tail -n +2 "$MANIFEST" | python3 -c "
import csv,sys
for row in csv.reader(sys.stdin):
    if not row: continue
    cell_id, backbone, receptor, rsha, lname, ltype, lsmi, linchi, taut, prot, natoms, relpath, isha, seed, notes = row
    print('\t'.join([cell_id, backbone, receptor, ltype, relpath, isha, seed]))
" | while IFS=$'\t' read -r cell_id backbone receptor ltype relpath isha seed; do
    if [ -n "${BACKBONE:-}" ] && [ "$BACKBONE" != "$backbone" ]; then continue; fi
    if [ -n "${CELL_ID:-}" ] && [ "$CELL_ID" != "$cell_id" ]; then continue; fi

    # Backbone-specific extension is already in relpath (e.g. .yaml, .fasta, .json).
    ext="${relpath##*.}"
    pred_input="$HPC_MANIFEST_ROOT/${relpath#manifest/}"
    pred_out_dir="$PROBE_SCRATCH/out/${backbone}/${cell_id}"
    pred_sidecar="$PROBE_SCRATCH/sidecars/${backbone}_${cell_id}.json"

    # Sidecar is a rerun-plan-shaped JSON so downstream code that walks
    # up to find provenance doesn't crash. Minimal contents that satisfy
    # the schema; provenance for this probe traces back to the manifest.
    sidecar_json=$(python3 -c "
import json
print(json.dumps({
    'probe_id': 'gate02_smiles',
    'cell_id': '$cell_id',
    'backbone': '$backbone',
    'receptor': '$receptor',
    'ligand_type': '$ltype',
    'input_relpath': '$relpath',
    'input_sha256': '$isha',
    'seed': $seed,
    'partner_type': 'apo',
    'partner_identity': '',
    'partner_perturbation': '',
    'species': 'human',
    'request_id': 'gate02_${cell_id}_${backbone}',
}))")

    job_name="pa3_g02_${backbone}_${cell_id}"
    launcher="$RERUN_ROOT_HPC/rerun_${backbone}.sh"

    # PRED_SAMPLES=1, PRED_N_SEEDS=1 (parser probe, not a diversity study).
    qsub_env_vars="PRED_INPUT=$pred_input,PRED_OUT_DIR=$pred_out_dir,PRED_SEED=$seed,PRED_SIDECAR=$pred_sidecar,PRED_SAMPLES=1,PRED_N_SEEDS=1"

    # Prefer H100 opportunistic. Cap wall-time at 4h - a parser probe on
    # a small ligand should finish in <30 min but MSA fetch can drag.
    qsub_cmd="qsub -N $job_name -o $PROBE_SCRATCH/logs/${backbone}_${cell_id}.log -j y -l gpu_card=1 -l m_mem_free=16G -l h_rt=04:00:00 -v $qsub_env_vars"
    if [ -n "${HOLD_JID:-}" ]; then
        qsub_cmd="$qsub_cmd -hold_jid $HOLD_JID"
    fi
    qsub_cmd="$qsub_cmd $launcher"

    if [ "$DRY_RUN" = "1" ]; then
        echo "DRY_RUN: $qsub_cmd"
        continue
    fi

    # Write the sidecar into PRED_OUT_DIR ahead of the launcher.
    # Chai's launcher moves it aside for the duration of the fold and
    # restores it after, so it must exist at PRED_OUT_DIR/_rerun_plan.json
    # BEFORE the launcher runs.
    ssh "$REMOTE_HOST" "mkdir -p $pred_out_dir $(dirname "$pred_sidecar"); printf %s '$sidecar_json' > $pred_sidecar; cp $pred_sidecar $pred_out_dir/_rerun_plan.json"

    # Actually submit.
    jid=$(ssh "$REMOTE_HOST" "$qsub_cmd" | grep -oE 'Your job [0-9]+' | awk '{print $3}')
    if [ -z "$jid" ]; then
        echo "WARN: no jobid returned for $job_name" >&2
        continue
    fi
    echo "submitted $job_name -> jid=$jid  $pred_out_dir"
    echo -e "$jid\t$backbone\t$cell_id\t$pred_out_dir" >> "$JOBIDS_FILE"
done

echo ""
echo "=== dispatched. Job ids written to $JOBIDS_FILE ==="
