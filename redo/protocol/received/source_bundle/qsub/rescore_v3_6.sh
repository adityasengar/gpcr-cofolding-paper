#!/bin/bash
#
# qsub/rescore_v3_6.sh — batch-rescore the frozen manuscript-critical
# corpus against the CURATE-Phase-2-augmented reference_set.csv + the
# A3 flank-consistency scorer patch.
#
# Inputs:
#   refs/reference_set.csv       (post-refs_build: 202 rows target)
#   docs/EXPERIMENT_CATALOG/data/predictions.csv  → derived manifest of
#                                                    17,568 predictions
#
# Outputs:
#   /hpc/scratch/sengaad1/paper_af3/rescore_frozen/2026-08-27/gpcr_v36/
#     rows.csv                   (one row per prediction)
#     failure_census.json        (assertion-class census)
#     <prediction_basename>.scorer.json (per-prediction sidecar)
#
# Expected wall time: ~30-60 min on a single node (v3.5 baseline was ~45
# min per rescore_v35_wrapper.log). CPU-bound (no GPU inference — just
# axis measurement + reference lookups). Overhead is GPCRdb fetches for
# receptor anchors, which are cached from prior runs.
#
# Amendment 3 safeguard: gpcr-score-batch never aborts on raise. Each
# failing prediction gets its assertion recorded in failure_census;
# execution continues.
#
# Finding #7 tripwire is armed on the batch side too (scorer/cli.py:
# _check_batch_nan_tripwire). Raises if any measurement column is >95%
# NaN across the batch — signals a silent-drop bug rather than a data
# gap.
#
#$ -N rescore_v3_6
#$ -cwd
#$ -o /hpc/scratch/sengaad1/paper_af3/logs/rescore_v3_6.$JOB_ID.log
#$ -j y
#$ -l h_rt=03:00:00
#$ -l m_mem_free=4G
#$ -l gpu_card=1               # mandatory on default.q per hpc-basel gotcha
#$ -pe smp 8

set -eo pipefail
source /etc/profile
module purge
module load proxy/GLOBAL       # RCSB / GPCRdb outbound network for any un-cached anchor fetches

# CUDA_VISIBLE_DEVICES per hpc-basel gotcha (no CUDA use here but the
# scorer imports torch elsewhere; explicit is safer than implicit).
if [ -n "${SGE_HGR_gpu_card:-}" ]; then
    export CUDA_VISIBLE_DEVICES=$(echo "$SGE_HGR_gpu_card" | grep -oE '[0-9]+' | paste -sd,)
fi
unset OMP_NUM_THREADS
set -u

REPO=${REPO:-/home/sengaad1/paper_af3}
SCRATCH=/hpc/scratch/sengaad1/paper_af3
export OUT_DIR=$SCRATCH/rescore_frozen/2026-08-27/gpcr_v36
mkdir -p "$OUT_DIR" "$SCRATCH/logs"

cd "$REPO"

# openfold3 first: it carries gemmi 0.7.5, which parses OF3-emitted mmCIF
# correctly. boltz has gemmi 0.6.5 which silently returns models=0 on those
# files (~1,940 rows regressed to A3 wrong-chain on v3.6 attempt 1). See
# regression diagnosis 2026-08-27.
source /home/sengaad1/software/venvs/openfold3/bin/activate 2>/dev/null || \
    source /home/sengaad1/software/venvs/boltz/bin/activate 2>/dev/null || \
    { echo "no venv found — install requirements and rerun"; exit 1; }

python3 --version
echo "REPO=$REPO"
echo "OUT_DIR=$OUT_DIR"

# ---------- Derive the batch manifest from EXPERIMENT_CATALOG ----------
#
# gpcr-score-batch expects: prediction_path, receptor_slug, state_claim,
# input_species. predictions.csv has: prediction_path, receptor,
# experiment_slug, ..., partner_type, partner_identity, seed, ...
#
# Every prediction in the frozen corpus is treated as an active-state
# claim (Ga_COUPLED_ACTIVE) by default. Species = human throughout
# (mouse/rat exceptions are handled inside the scorer via
# scorer/receptors.py::KNOWN_RECEPTORS).

export MANIFEST=$OUT_DIR/manifest.csv
echo "=== deriving manifest from EXPERIMENT_CATALOG ==="

python3 <<'PYEOF'
import csv, sys, os
src = "docs/EXPERIMENT_CATALOG/data/predictions.csv"
dst = os.environ["MANIFEST"]
n_written = 0
with open(src) as fi, open(dst, "w", newline="") as fo:
    reader = csv.DictReader(fi)
    fields = ["prediction_path", "receptor_slug", "state_claim", "input_species"]
    writer = csv.DictWriter(fo, fieldnames=fields)
    writer.writeheader()
    for r in reader:
        if not r.get("prediction_path"):
            continue
        # Strip species suffix (predictions.csv uses XCR1_HUMAN / TAAR1_MOUSE
        # etc.; KNOWN_RECEPTORS keys are unsuffixed). Species column is set
        # per row below; the scorer's A5 gate handles species mismatch.
        slug = (r.get("receptor") or "").strip()
        for sfx in ("_HUMAN", "_MOUSE", "_RAT", "_BOVIN"):
            if slug.upper().endswith(sfx):
                slug = slug[: -len(sfx)]
                break
        writer.writerow({
            "prediction_path": r["prediction_path"],
            "receptor_slug":   slug,
            "state_claim":     "Ga-coupled-active",
            "input_species":   "human",
        })
        n_written += 1
print(f"wrote {n_written} manifest rows to {dst}", file=sys.stderr)
PYEOF

wc -l "$MANIFEST"

# ---------- Run the batch scorer ----------
echo "=== running gpcr-score-batch (M2.5 v3.6) ==="

# scorer.cli exposes gpcr-score-batch via [project.scripts], but the venv
# doesn't have paper_af3 pip-installed — invoke batch_main directly.
python3 -c "from scorer.cli import batch_main; import sys; sys.exit(batch_main())" \
    --manifest "$MANIFEST" \
    --out "$OUT_DIR" \
    --ref-set refs/reference_set.csv \
    --cache-dir "$SCRATCH/refs/cache" \
    2>&1 | tee "$OUT_DIR/batch.stderr"

echo ""
echo "=== v3.6 output shape ==="
wc -l "$OUT_DIR/rows.csv"
cat "$OUT_DIR/failure_census.json"
echo ""
echo "=== NaN state on the 35 CURATE Phase 2 receptors ==="
python3 <<'PYEOF'
import csv, os, math
p = os.path.join(os.environ["OUT_DIR"], "rows.csv")
target = set("HRH4 ACM3 5HT1A MCHR2 KISSR CALCR BRS3 NMBR PRLHR QRFPR "
             "PE2R1 PF2R PI2R SSR1 SSR3 SSR5 CXCR1 XCR1 MC5R OPSR "
             "CML2 GP101 GPR3 GPR12 GPR15 GPR34 GPR84 GPER1 DRD5 SUCR1 "
             "GPR55 GP132 P2Y10 FFAR2 HCAR3".split())
n_by_rec = {}
n_active_ref_numeric = {}
with open(p) as f:
    for r in csv.DictReader(f):
        rec = r.get("receptor_slug", "").upper()
        if rec not in target:
            continue
        n_by_rec[rec] = n_by_rec.get(rec, 0) + 1
        v = r.get("receptor_d_active_ref", "").strip().lower()
        try:
            x = float(v) if v else float("nan")
            if not math.isnan(x):
                n_active_ref_numeric[rec] = n_active_ref_numeric.get(rec, 0) + 1
        except ValueError:
            pass
for rec in sorted(target):
    n = n_by_rec.get(rec, 0)
    n_num = n_active_ref_numeric.get(rec, 0)
    print(f"  {rec:8s} rows={n:>4d}  d_active_ref_numeric={n_num:>4d}  "
          f"pct={(100*n_num/n if n else 0):5.1f}")
PYEOF

echo ""
echo "=== v3.6 complete — inspect $OUT_DIR/rows.csv ==="
