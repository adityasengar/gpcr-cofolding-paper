#!/bin/bash
#
# qsub/rerun_chai.sh — M2.3 fresh Chai-1 co-fold for one row.
#
# Env contract (identical to rerun_boltz.sh):
#   PRED_INPUT     absolute path to a Chai FASTA input
#   PRED_OUT_DIR   absolute path where Chai output should land
#   PRED_SEED      integer seed (deterministic from fresh_seed_for)
#   PRED_SIDECAR   absolute path to the rerun-plan JSON
#
# Notes:
#   - Chai-1 accepts a `--seed` via the `chai-lab fold` CLI. Output goes
#     to `<out>/pred.model_idx_N.cif` at depth 2 (confirmed by manifest
#     forensics — task3b_chai emitted this layout).
#   - Chai's install is fragile (W5-B pilot install failed in the frozen
#     branches — see plan). Kept in the panel only for the task3b
#     four-backbone attributability plot.
#
# Not yet HPC-verified — smoke-test 5 rows before scaling per plan.

#$ -N pa3_chai_rerun
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rerun_chai.$JOB_ID.log
#$ -j y
#$ -l h_rt=06:00:00
#$ -l m_mem_free=8G
#$ -l gpu_card=1
#$ -pe smp 4
#
# 2026-09-01: MSA source — CHAI_MSA_DIRECTORY (pre-built .aligned.pqt cache)
# is the ONLY supported mode. Validated 2026-09-01 (mechanism + DRD2 5x5
# scientific comparison, Delta mean d_tm6 = 0.023 A inside pilot 1sigma).
# Server-mode dropped to prevent live-fetch storms. One-off server-mode
# ablations must use a separate wrapper (qsub/verify_drd2_msa_cache.sh).
#
# 2026-09-01 (audit trail #10): CHAI_MSA_DIRECTORY did not propagate
# through `qsub -v` in the wave-1 dispatch — chai jobs ran silently
# single-sequence while _chai_status.json reported ok=true. This launcher
# now hardcodes the default cache path AND does a per-job pre-flight
# check that every protein-chain .aligned.pqt is present. Missing file
# or missing env => hard exit. A misconfigured chai job dies with a
# clear message; it does not produce contaminated CIFs.

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL

if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS
set -u

: "${PRED_INPUT:?PRED_INPUT is required (path to Chai FASTA)}"
: "${PRED_OUT_DIR:?PRED_OUT_DIR is required}"
: "${PRED_SEED:?PRED_SEED is required}"
: "${PRED_SIDECAR:?PRED_SIDECAR is required}"

[ -f "$PRED_INPUT" ] || { echo "FATAL: PRED_INPUT missing: $PRED_INPUT" >&2; exit 1; }

mkdir -p "$PRED_OUT_DIR" "$(dirname "$PRED_SIDECAR")"

# Default to chai1 venv (chai-lab 0.6.1 — post-2026-09-01 install).
# `chai` (unsuffixed) is a stale earlier install kept only for A/B ablations.
CHAI_VENV=${CHAI_VENV:-/home/sengaad1/software/venvs/chai1}
if [ ! -d "$CHAI_VENV" ]; then
    echo "FATAL: chai venv not found at $CHAI_VENV" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$CHAI_VENV/bin/activate"

python3 --version
which chai-lab 2>/dev/null || which chai 2>/dev/null || echo "warn: chai binary not on PATH"
nvidia-smi -L || true

echo "=== M2.3 rerun_chai ==="
echo "JOB_ID     : ${JOB_ID:-<no-JOB_ID>}"
echo "HOST       : $(hostname)"
echo "DATE       : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "PRED_INPUT : $PRED_INPUT"
echo "PRED_OUT   : $PRED_OUT_DIR"
echo "PRED_SEED  : $PRED_SEED"
echo "GPU        : ${CUDA_VISIBLE_DEVICES:-<none>}"
echo ""

# chai-lab fold asserts `not any(output_dir.iterdir())` on PRED_OUT_DIR
# and aborts if ANY entry — including a subdirectory — sits there.
# TWO items need to sit outside PRED_OUT_DIR before `chai-lab fold` runs:
#
#   1. The input-used marker (this script's own convention).
#   2. `_rerun_plan.json` — the supervisor writes it INSIDE PRED_OUT_DIR
#      before qsub (see scorer/supervisor.py::_submit lines 471-473 and
#      scorer/rerun_dispatch.py::ReRunPlan.sidecar). Every other backbone
#      tolerates it because they don't assert output_dir is empty. Chai
#      does. Move it up one level for the duration of the fold; restore
#      after chai completes so downstream rescore + provenance still find
#      it via the orchestrator's bounded walk-up
#      (_lift_provenance_from_sidecar with max_up=8).
#
# The 2026-08-27 validation batch's first attempt (`mkdir -p
# PRED_OUT_DIR/_meta`) failed because _meta counted as an entry;
# the second attempt (this one) puts BOTH files outside PRED_OUT_DIR.
META_DIR="$(dirname "$PRED_OUT_DIR")/_meta"
mkdir -p "$META_DIR"
cp -f "$PRED_INPUT" "$META_DIR/_input_used.$(basename "$PRED_INPUT")"
# Move the supervisor-written sidecar out of PRED_OUT_DIR for the
# duration of the fold; restore afterwards so downstream rescore's
# `_lift_provenance_from_sidecar` walk finds it at the expected leaf.
# Per-seed stash filename so concurrent Chai jobs sharing a parent dir
# don't collide.
STASH_NAME="_rerun_plan.$(basename "$PRED_OUT_DIR").json"
STASHED_SIDECAR="$(dirname "$PRED_OUT_DIR")/$STASH_NAME"
if [ -f "$PRED_OUT_DIR/_rerun_plan.json" ]; then
    mv "$PRED_OUT_DIR/_rerun_plan.json" "$STASHED_SIDECAR"
fi

set +e
# Diversity-study samples-per-seed multiplier (default 1).
N_SAMPLES="${PRED_SAMPLES:-1}"
echo "PRED_SAMPLES=$N_SAMPLES"

# MSA source — cache mode is the ONLY supported mode. Silent single-
# sequence fallback is the exact regression class audit trail #10
# exists to close (2026-09-01: env didn't propagate through qsub -v,
# jobs ran single-seq while status reported ok=true). Hardcode the
# default and refuse to launch on any config drift.
: "${CHAI_MSA_DIRECTORY:=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"
if [ ! -d "$CHAI_MSA_DIRECTORY" ]; then
    echo "FATAL: CHAI_MSA_DIRECTORY is not a directory: $CHAI_MSA_DIRECTORY" >&2
    exit 1
fi
MSA_FLAG=(--msa-directory "$CHAI_MSA_DIRECTORY")
echo "MSA         : --msa-directory $CHAI_MSA_DIRECTORY"

# Per-job pre-flight: assert every protein chain's .aligned.pqt is
# present in CHAI_MSA_DIRECTORY. Chai's silent single-sequence fallback
# on missing files was the wave-1 contamination mechanism; a
# misconfigured job must die with a clear message, not produce
# `_chai_status.json:ok=true` alongside undocumented single-seq CIFs.
python3 - "$PRED_INPUT" "$CHAI_MSA_DIRECTORY" <<'PYEOF'
import hashlib, sys
from pathlib import Path

pred_input, msa_dir = Path(sys.argv[1]), Path(sys.argv[2])
seqs, header, buf = [], None, []
for line in pred_input.read_text().splitlines():
    line = line.strip()
    if line.startswith(">"):
        if header is not None:
            seqs.append((header, "".join(buf)))
        header, buf = line[1:], []
    elif line:
        buf.append(line)
if header is not None:
    seqs.append((header, "".join(buf)))

missing, n_protein = [], 0
for hdr, seq in seqs:
    # Chai FASTA: `>protein|name=...`, `>ligand|...`, `>rna|...`, etc.
    # Only protein chains need .aligned.pqt.
    if not hdr.lower().startswith("protein"):
        continue
    n_protein += 1
    sha = hashlib.sha256(seq.upper().encode()).hexdigest()
    pqt = msa_dir / f"{sha}.aligned.pqt"
    if not pqt.exists():
        missing.append((hdr, sha, str(pqt)))

if missing:
    sys.stderr.write(
        f"FATAL: chai pre-flight — .aligned.pqt missing for "
        f"{len(missing)}/{n_protein} protein chains:\n"
    )
    for hdr, sha, pqt in missing:
        sys.stderr.write(f"  chain={hdr!r}  sha={sha[:12]}...  expected={pqt}\n")
    sys.stderr.write(
        "Refusing to launch chai — this would silently fall back to "
        "single-sequence. See docs/AUDIT_TRAIL.md #10.\n"
    )
    sys.exit(1)

print(f"[chai-preflight] {n_protein}/{n_protein} protein chain "
      f".aligned.pqt files present in {msa_dir}")
PYEOF
PREFLIGHT_EXIT=$?
if [ $PREFLIGHT_EXIT -ne 0 ]; then
    echo "FATAL: chai pre-flight failed (exit $PREFLIGHT_EXIT). "\
         "Aborting before chai-lab fold to avoid contaminated CIFs." >&2
    exit $PREFLIGHT_EXIT
fi

CHAI_CMD=(chai-lab fold)

"${CHAI_CMD[@]}" \
    "$PRED_INPUT" \
    "$PRED_OUT_DIR" \
    "${MSA_FLAG[@]}" \
    --seed "$PRED_SEED" \
    --num-trunk-recycles 3 \
    --num-diffn-timesteps 50 \
    --num-diffn-samples "$N_SAMPLES"
EXIT=$?
set -e

echo ""
echo "=== chai exit=$EXIT ==="

# Restore the stashed sidecar so `_lift_provenance_from_sidecar` finds
# it during rescore. Uses mkdir -p in case chai created no output_dir
# at all on failure — the sidecar always lands, even if fold crashed.
if [ -f "$STASHED_SIDECAR" ]; then
    mkdir -p "$PRED_OUT_DIR"
    mv "$STASHED_SIDECAR" "$PRED_OUT_DIR/_rerun_plan.json"
fi

STATUS_JSON="$PRED_OUT_DIR/_chai_status.json"
python3 - "$EXIT" "$PRED_OUT_DIR" "$PRED_SEED" "$STATUS_JSON" <<'PY'
import json, sys
from pathlib import Path
exit_code = int(sys.argv[1]); out_dir = Path(sys.argv[2])
seed = int(sys.argv[3]); status_path = Path(sys.argv[4])
# Chai emits pred.model_idx_N.cif — accept both cif and pdb to be safe
produced = sorted(str(p) for p in list(out_dir.rglob("*.cif")) + list(out_dir.rglob("*.pdb")))
status = {"backbone": "chai", "exit_code": exit_code, "seed": seed,
          "produced_files": produced, "n_produced": len(produced),
          "ok": exit_code == 0 and len(produced) > 0}
status_path.write_text(json.dumps(status, indent=2))
print(json.dumps(status, indent=2))
PY

find "$PRED_OUT_DIR" -maxdepth 6 \( -name '*.cif' -o -name '*.pdb' -o -name '_chai_status.json' \) \
    -printf '%p  %s bytes\n' 2>/dev/null || true

exit "$EXIT"
