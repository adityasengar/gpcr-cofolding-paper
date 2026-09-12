"""Build the Block A switch-test manifest across 48 GPCRs × 2 arms × 4 backbones.

Block A tests whether an AF3-family co-folding model can flip a receptor
between "on" (Gα-coupled active) and "off" (apo inactive) purely by
changing the input partner. Success per (receptor, backbone) requires the
receptor + primary-Gα prediction to have TM6 outward AND the apo
prediction to have TM6 inward.

Panel (48 receptors, locked 2026-09-01):
  - Class A: 40 receptors from refs/gpcr_coupling.csv (PREREG §1).
    * JSR1 (B1B1U5) stays in manifest but reports as non-mammalian
      singleton (PREREG §5) — out of Class A primary result.
    * CNR1, OPRD kept in but reported-secondary (agonist-only active refs).
  - Class B: 4 receptors (GLP1R, GCGR, PTH1R, CRHR1) — paired active+inactive
    with G-protein-coupled active reference.
  - Class F: 4 receptors (SMO, FZD4, FZD6, FZD7) — reported as individual
    case studies, no pooled Class F number (PREREG §2c-revised).
  - Class C: excluded (dimer activation mechanism uninterpretable).

Total predictions: 48 receptors × 2 arms × 4 backbones × 25
                 − 1 (FZD4 cognate skipped, DVL2 transducer not Gα) × 4 × 25
                 = 9,500 predictions across 1,900 manifest rows.

Per-backbone (seeds, samples) is uniform (5, 5) across all four backbones
per PREREG §9 (user decision, 2026-09-01). Defaults below reflect this
uniform lock. OF3's seed variance is ~0.006 Å (effectively deterministic
across seeds); uniform (5,5) was chosen over the study's (1,5) OF3
recommendation for cross-backbone comparability, at the cost of a near-zero
per-cell CI for OF3 — expected, not false precision.

Usage:

  # Dry-run locally: build rows, run pre-checks, skip file materialisation.
  scripts/build_block_a_manifest.py \\
      --output-root /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test \\
      --manifest-out experiments/018_block_a_switch_test/manifest/manifest.csv \\
      --dry-run

  # Real run: materialise input files under output-root (on HPC login node).
  scripts/build_block_a_manifest.py \\
      --output-root /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test \\
      --manifest-out experiments/018_block_a_switch_test/manifest/manifest.csv

The `block_a` preset uses arms `cognate` + `apo` only. Shuffled and decoy
arms return in Block B on a pre-registered 12-receptor subset (PREREG §12).

The `cognate` arm resolves the partner identity per-receptor from
refs/gpcr_coupling.csv (Gs → alphas, Gi → alphai1, Gq → alphaq, Gt →
alphat). FZD4 is **apo-only** (DVL2 transducer, not Gα — substituting
alphas as a proxy would be the W54 taxonomy failure at n=1). A blanket
alphas would recreate the W54 taxonomy failure.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

# Sentinel: in a condition preset, this value in the identity slot means
# "look up primary_ga_identity per-receptor from refs/gpcr_coupling.csv".
# Prevents the W54 taxonomy failure (blanket alphas for all 40 receptors)
# and materialises the correct primary Gα family per row.
COGNATE_LOOKUP_SENTINEL = "__PRIMARY_GA_PER_COUPLING__"

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

COUPLING_CSV = REPO / "refs" / "gpcr_coupling.csv"

from scorer.bw_numbering import Api
from scorer.pre_check import load_ref_species_map
from scorer.propose import (
    DEFAULT_CACHE_DIR,
    REF_SET_CSV,
    SpecError,
    _canonicalise_receptor,
    _expand_rows,
    _parse_fasta,
    format_summary,
    materialise_inputs,
    run_pre_checks,
)
from scorer.receptors import KNOWN_RECEPTORS
from scorer.schema import PROPOSE_MANIFEST_COLUMNS


# Runtime aliases for Class B/F receptors NOT already in scorer/receptors.py's
# KNOWN_RECEPTORS table. Frozen scorer code (e54a7f8) knows GLR/CRFR1/FZD4/
# FZD7 but not the GCGR/CRHR1/FZD6 slugs used in refs/reference_set_class_bf.csv.
# Extend the in-memory table so `_canonicalise_receptor` resolves cleanly on
# these three; leaves scorer/receptors.py file untouched (frozen at e54a7f8).
KNOWN_RECEPTORS.setdefault("GCGR",  "glr_human")
KNOWN_RECEPTORS.setdefault("CRHR1", "crfr1_human")
KNOWN_RECEPTORS.setdefault("FZD6",  "fzd6_human")


# 40 Class A receptors (PREREG §1) — all with paired active+inactive tier-1
# references per refs/reference_set.csv (Step 1 audit).
BLOCK_A_CLASS_A: list[str] = [
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR",
    "ACM1", "ACM2", "ACM4", "ADA2A", "ADRB1",
    "ADRB2", "AGTR1", "APJ", "B1B1U5", "CCKAR",
    "CCR5", "CNR1", "CNR2", "CXCR2", "CXCR4",
    "DRD2", "DRD3", "EDNRA", "EDNRB", "FSHR",
    "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1",
    "LSHR", "LT4R1", "MCHR1", "NPY1R", "NPY2R",
    "OPRD", "OPRK", "OPRX", "OPSD", "OX2R",
]

# 4 Class B receptors (secretin family) — paired active+inactive with
# G-protein-coupled active reference per refs/reference_set_class_bf.csv.
BLOCK_A_CLASS_B: list[str] = ["GLP1R", "GCGR", "PTH1R", "CRHR1"]

# 4 Class F receptors — reported as individual case studies (PREREG §2c-revised).
# FZD4: **apo-only** in Block A. FZD4's actual transducer is
# Dishevelled-DEP (DVL2, UniProt O14641), NOT a Gα. Substituting `alphas`
# as a "cognate proxy" was the W54 taxonomy failure at n=1 — a caveat
# does not rescue it. FZD4 cognate arm is SKIPPED in build_all_rows
# (see FZD4_APO_ONLY set + emission-skip branch).
# TODO: DVL2 (O14641) is one MSA pre-warm + Chai `.aligned.pqt` cache
# away from a proper Block-A-post follow-up; not on the Block A path.
# FZD6 uses canonical alphas — α5-CT is identical to alphas_XLas isoform.
BLOCK_A_CLASS_F: list[str] = ["SMO", "FZD4", "FZD6", "FZD7"]

# Receptors that emit apo-only under the block_a preset (no cognate arm).
# See FZD4 rationale above. Guards against the DVL2-should-be-cognate
# taxonomy failure that a blanket alphas would recreate.
FZD4_APO_ONLY: set[str] = {"FZD4"}

# Consolidated 48-receptor panel.
BLOCK_A_RECEPTORS: list[str] = BLOCK_A_CLASS_A + BLOCK_A_CLASS_B + BLOCK_A_CLASS_F

# Block B Wide panel — same 40 Class A receptors as Block A, no additions
# (BLOCK_B_PRE_DISPATCH_DECISIONS_2026_09_02.md Decision 2, option 1).
BLOCK_B_CLASS_A: list[str] = BLOCK_A_CLASS_A[:]

# Sentinels for the Block B shuffled/decoy arms: like COGNATE_LOOKUP_SENTINEL,
# these mark "resolve per-receptor at build time," but from
# refs/constructs_block_b/<slug>_<arm>.fasta rather than from
# refs/gpcr_coupling.csv + partners.fasta. Shuffled = full non-cognate Gα
# (fold + recognition, wrong family). Decoy = full cognate Gα scaffold with
# the alpha5-CT scrambled (occupancy + fold, no recognition). See
# experiments/019_block_b_partner_selection/analysis/construct_build_report.md.
SHUFFLED_LOOKUP_SENTINEL = "__BLOCK_B_SHUFFLED_FASTA__"
DECOY_LOOKUP_SENTINEL = "__BLOCK_B_DECOY_FASTA__"

CONSTRUCTS_BLOCK_B_DIR = REPO / "refs" / "constructs_block_b"

# Species per receptor — mostly human, a couple non-human.
NON_HUMAN_SPECIES: dict[str, str] = {
    "B1B1U5": "9arac",   # Australian arachnid per refs/reference_pdbs.csv
    "OPSD":   "bovin",   # bovine rhodopsin
}

# Per-backbone (seeds, samples_per_seed) — uniform (5, 5) across all four
# backbones per PREREG §9 (locked 2026-09-01). OF3's per-seed std is 0.006 Å
# so its per-cell CI will be near zero; that's low seed variance, not false
# precision. Kept uniform for cross-backbone comparability.
DEFAULT_MN: dict[str, tuple[int, int]] = {
    "boltz":    (5, 5),
    "of3":      (5, 5),
    "protenix": (5, 5),
    "chai":     (5, 5),
}


# Condition presets:
#   Each preset = ordered dict of {condition_name: (partner_type, partner_identity, state_claim)}.
#   Extended-partners is Phase 6 material.
CONDITION_PRESETS: dict[str, dict[str, tuple[str, str, str]]] = {
    "block_a": {
        # cognate = per-receptor primary Gα from refs/gpcr_coupling.csv
        # (Gs → alphas, Gi → alphai1, Gq → alphaq, Gt → alphat). The
        # sentinel is resolved per-receptor in build_all_rows; a blanket
        # "alphas" here would re-introduce the founding W54 bug.
        "cognate": ("g_alpha", COGNATE_LOOKUP_SENTINEL, "Ga-coupled-active"),
        "apo":     ("apo", "", "apo"),
    },
    "block_b": {
        # Block B Wide, four arms (docs/BLOCK_B_DISPATCH_PLAN_2026_09_02.md).
        # cognate + apo reuse the block_a sentinel/apo tuples verbatim.
        # shuffled/decoy resolve per-receptor from
        # refs/constructs_block_b/<slug>_{shuffled,decoy}.fasta via
        # load_block_b_construct — see SHUFFLED_LOOKUP_SENTINEL /
        # DECOY_LOOKUP_SENTINEL above.
        "cognate":  ("g_alpha", COGNATE_LOOKUP_SENTINEL, "Ga-coupled-active"),
        "apo":      ("apo", "", "apo"),
        "shuffled": ("g_alpha", SHUFFLED_LOOKUP_SENTINEL, "Ga-coupled-noncognate"),
        "decoy":    ("g_alpha", DECOY_LOOKUP_SENTINEL, "Ga-decoy-scrambled-a5ct"),
    },
    "extended_partners": {
        "gs":       ("g_alpha", "alphas", "Ga-coupled-active"),
        "gi":       ("g_alpha", "alphai1", "Ga-coupled-active"),
        "gq":       ("g_alpha", "alphaq", "Ga-coupled-active"),
        "arrestin": ("arrestin", "arrestin_FL", "arrestin-coupled"),
        "apo":      ("apo", "", "apo"),
    },
}


def load_cognate_identities(coupling_csv: Path) -> dict[str, str]:
    """Return {receptor_slug_upper: primary_ga_identity} from the coupling CSV.

    Backs the cognate arm so each receptor pairs with its documented
    primary Gα family (Gs → alphas, Gi → alphai1, Gq → alphaq, Gt →
    alphat) rather than a blanket alphas. Refs the same CSV pre-registered
    as "panel of record" in refs/PREREG.md.
    """
    out: dict[str, str] = {}
    with coupling_csv.open() as fh:
        for r in csv.DictReader(fh):
            slug = (r.get("receptor_slug") or "").strip().upper()
            ident = (r.get("primary_ga_identity") or "").strip()
            if slug and ident:
                out[slug] = ident
    return out


def load_block_b_construct(receptor_slug: str, arm: str) -> tuple[str, str]:
    """Resolve a Block B shuffled/decoy partner sequence from its per-receptor FASTA.

    Reads refs/constructs_block_b/<slug>_<arm>.fasta — one single-record
    FASTA per (receptor, arm) produced by build_shuffled_decoy_constructs.py
    (see construct_build_report.md). Reuses the same ``_parse_fasta`` helper
    scorer/propose.py already uses for partners.fasta, so this is read-only
    against refs/ and requires no change to scorer/propose.py or
    partners.fasta — the resolved sequence is passed straight into the spec
    as ``partner.sequence_fasta``, which materialise_inputs already prefers
    over an identity lookup (scorer/propose.py:817-821).

    Returns (identity_slug, sequence). Sequence is "" if the file is
    missing or unparseable — caller reports FAIL and skips the row, same
    pattern as a missing cognate identity in build_all_rows.
    """
    slug = f"{receptor_slug.lower()}_{arm}"
    path = CONSTRUCTS_BLOCK_B_DIR / f"{slug}.fasta"
    seq = _parse_fasta(path).get(slug, "")
    return (slug, seq)


def build_condition_spec(
    receptor: str,
    condition: str,
    partner_type: str,
    partner_identity: str,
    state_claim: str,
    backbone: str,
    seeds: int,
    samples_per_seed: int,
    experiment_slug: str,
    partner_sequence_fasta: str = "",
) -> dict:
    """Build one in-memory spec dict for one (receptor, condition, backbone).

    ``partner_sequence_fasta``, when non-empty, is threaded through as
    ``partner.sequence_fasta`` — the inline-sequence override that
    materialise_inputs already checks before falling back to a
    partners.fasta identity lookup (scorer/propose.py:817-821). This is
    how the Block B shuffled/decoy arms supply a per-receptor sequence
    that isn't a static partners.fasta entry, without touching
    scorer/propose.py or partners.fasta.
    """
    if partner_type == "apo":
        partner = {"type": "apo", "identity": ""}
    else:
        partner = {"type": partner_type, "identity": partner_identity}
        if partner_sequence_fasta:
            partner["sequence_fasta"] = partner_sequence_fasta

    species = NON_HUMAN_SPECIES.get(receptor.upper(), "human")

    return {
        "request_id": f"{experiment_slug}_{receptor.lower()}_{condition}_{backbone}",
        "biological_question": (
            f"{experiment_slug} — {receptor} with {condition} on {backbone}."
        ),
        "receptor": receptor,
        "partner": partner,
        "state_claim": state_claim,
        "backbones": [backbone],
        "seeds": seeds,
        "samples_per_seed": samples_per_seed,
        "species": species,
        "partner_perturbation": "wt",
    }


def build_all_rows(
    receptors: list[str],
    conditions: dict[str, tuple[str, str, str]],   # condition_name → (partner_type, identity, state_claim)
    mn_per_backbone: dict[str, tuple[int, int]],
    api: Api,
    ref_species_map: dict,
    output_root: Path,
    dry_run: bool,
    experiment_slug: str,
    cognate_map: dict[str, str] | None = None,
) -> tuple[list[dict[str, str]], list[str]]:
    """Loop receptors × conditions × backbones; return (all_rows, warnings)."""
    all_rows: list[dict[str, str]] = []
    warnings: list[str] = []
    cognate_map = cognate_map or {}

    for rec in receptors:
        canonical = _canonicalise_receptor(rec)
        if canonical not in KNOWN_RECEPTORS:
            warnings.append(f"SKIP {rec}: not in KNOWN_RECEPTORS")
            continue

        for cond, (partner_type, partner_identity, state_claim) in conditions.items():
            # Skip cognate emission for FZD4 (and any receptor in
            # FZD4_APO_ONLY): FZD4's actual transducer is DVL2-DEP, not a
            # Gα. Substituting alphas as a proxy would recreate the W54
            # taxonomy failure at n=1. FZD4 apo arm is still emitted below.
            # TODO: DVL2 (UniProt O14641) — one MSA pre-warm + Chai
            # `.aligned.pqt` away from a Block-A-post follow-up.
            if rec.upper() in FZD4_APO_ONLY and cond == "cognate":
                # Prefix INFO (not SKIP) — this is a deliberate manifest
                # decision, not a receptor cleanup issue. The trailing
                # hard-fail scan below flags SKIP/FAIL; INFO is expected.
                warnings.append(
                    f"INFO {rec} {cond}: apo-only per FZD4_APO_ONLY "
                    f"(DVL2 transducer, not Gα; deferred as Block-A-post follow-up)"
                )
                continue

            # Resolve the per-receptor primary Gα identity for the cognate
            # arm. A blanket identity here would re-introduce the W54 bug.
            partner_sequence_fasta = ""
            if partner_identity == COGNATE_LOOKUP_SENTINEL:
                resolved_identity = cognate_map.get(canonical.upper())
                if not resolved_identity:
                    warnings.append(
                        f"FAIL {rec} {cond}: no primary_ga_identity in "
                        f"refs/gpcr_coupling.csv for slug {canonical}"
                    )
                    continue
            elif partner_identity in (SHUFFLED_LOOKUP_SENTINEL, DECOY_LOOKUP_SENTINEL):
                # Block B shuffled/decoy: resolve the per-receptor construct
                # FASTA under refs/constructs_block_b/ instead of a static
                # partners.fasta identity. See load_block_b_construct.
                arm = "shuffled" if partner_identity == SHUFFLED_LOOKUP_SENTINEL else "decoy"
                resolved_identity, partner_sequence_fasta = load_block_b_construct(canonical, arm)
                if not partner_sequence_fasta:
                    warnings.append(
                        f"FAIL {rec} {cond}: no Block B {arm} construct FASTA found for "
                        f"slug {canonical} at "
                        f"{CONSTRUCTS_BLOCK_B_DIR}/{canonical.lower()}_{arm}.fasta"
                    )
                    continue
            else:
                resolved_identity = partner_identity

            for bb, (seeds, samples) in mn_per_backbone.items():
                spec = build_condition_spec(
                    receptor=rec,
                    condition=cond,
                    partner_type=partner_type,
                    partner_identity=resolved_identity,
                    state_claim=state_claim,
                    backbone=bb,
                    seeds=seeds,
                    samples_per_seed=samples,
                    experiment_slug=experiment_slug,
                    partner_sequence_fasta=partner_sequence_fasta,
                )
                try:
                    rows = _expand_rows(spec)
                    run_pre_checks(spec, rows, api, ref_species_map)
                    # Step 6 (PREREG §Step 6) hard-gate: `warn_A1` on a panel
                    # receptor is a HARD FAIL — the FASTA doesn't match the
                    # receptor's own crystal-derived canonical AA at an
                    # identity-anchor. All 40 panel receptors are tier-1 per
                    # the Step 1 audit, so no soft-fail for them.
                    a1_failures = [
                        r for r in rows
                        if r.get("pre_check_status", "").startswith("warn_A1")
                    ]
                    if a1_failures:
                        warnings.append(
                            f"FAIL {rec} {cond} {bb}: A1 hard_fail on {len(a1_failures)}"
                            f"/{len(rows)} rows — identity-anchor AA mismatch on a "
                            f"panel receptor. Fix FASTA / slug before dispatch. "
                            f"Details: {a1_failures[0].get('pre_check_reason', '')[:200]}"
                        )
                        continue    # skip materialisation on hard-fail
                    if not dry_run:
                        materialise_inputs(spec, rows, output_root, api)
                    all_rows.extend(rows)
                    n_pass = sum(1 for r in rows if r["pre_check_status"] == "pass")
                    if n_pass < len(rows):
                        warnings.append(
                            f"WARN {rec} {cond} {bb}: {len(rows) - n_pass}/{len(rows)} "
                            f"pre-check warnings — {format_summary(rows)}"
                        )
                except SpecError as e:
                    warnings.append(f"FAIL {rec} {cond} {bb}: {e}")
                except Exception as e:  # noqa: BLE001
                    warnings.append(
                        f"FAIL {rec} {cond} {bb}: unexpected {type(e).__name__}: {e}"
                    )
    return all_rows, warnings


def write_manifest(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(PROPOSE_MANIFEST_COLUMNS))
        w.writeheader()
        w.writerows(rows)


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head_of(path: Path) -> str:
    """Return the git SHA of the most recent commit that touched ``path``.

    Empty string on any git failure (e.g. path never committed yet).
    """
    try:
        r = subprocess.run(
            ["git", "log", "-n", "1", "--pretty=%H", "--", str(path.resolve())],
            capture_output=True, text=True, check=True, cwd=str(REPO),
        )
        return r.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def write_manifest_provenance(manifest_path: Path, args: argparse.Namespace) -> Path:
    """Emit manifest.provenance.json alongside manifest.csv.

    Records SHA256 of every input the manifest depended on plus git SHAs
    for the code that built it. Downstream tools (rescore, block-B
    registration, primary-result unblinding) verify against this file.
    """
    prov_path = manifest_path.parent / "manifest.provenance.json"
    partners_fasta = REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"
    panel_receptor_fasta = REPO / "refs/panel_receptor_sequences.fasta"
    sealed_csv = REPO / "refs/sealed_active_refs_2026_09_01.csv"
    provenance = {
        "propose_py_git_sha": _git_head_of(REPO / "scorer" / "propose.py"),
        "build_manifest_py_git_sha": _git_head_of(REPO / "scripts" / "build_block_a_manifest.py"),
        "panel_csv_sha256": _sha256(COUPLING_CSV),
        "panel_class_bf_csv_sha256": _sha256(REPO / "refs" / "gpcr_coupling_class_bf.csv"),
        "reference_set_csv_sha256": _sha256(args.ref_set),
        "eligible_pool_csv_sha256": _sha256(REPO / "refs" / "eligible_pool.csv"),
        "sealed_active_refs_csv_sha256": _sha256(sealed_csv),
        "partners_fasta_sha256": _sha256(partners_fasta),
        "panel_receptor_sequences_fasta_sha256": _sha256(panel_receptor_fasta),
        "manifest_csv_sha256": _sha256(manifest_path),
        "materialised_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "preset": args.preset,
        "experiment_slug": args.experiment_slug,
    }
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
    return prov_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="build_block_a_manifest")
    p.add_argument("--output-root", type=Path, required=True,
                   help="Root directory for materialised inputs and prediction outputs. "
                        "Typically /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test")
    p.add_argument("--manifest-out", type=Path, required=True,
                   help="Path to write the merged manifest.csv")
    p.add_argument("--receptors", nargs="+", default=None,
                   help=f"Receptor slugs to include (default: {len(BLOCK_A_RECEPTORS)} Block A canonical)")
    p.add_argument("--boltz-mn", nargs=2, type=int, default=list(DEFAULT_MN["boltz"]),
                   metavar=("SEEDS", "SAMPLES"))
    p.add_argument("--of3-mn", nargs=2, type=int, default=list(DEFAULT_MN["of3"]),
                   metavar=("SEEDS", "SAMPLES"))
    p.add_argument("--protenix-mn", nargs=2, type=int, default=list(DEFAULT_MN["protenix"]),
                   metavar=("SEEDS", "SAMPLES"))
    p.add_argument("--chai-mn", nargs=2, type=int, default=list(DEFAULT_MN["chai"]),
                   metavar=("SEEDS", "SAMPLES"))
    p.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR,
                   help=f"GPCRdb cache (default: {DEFAULT_CACHE_DIR})")
    p.add_argument("--ref-set", type=Path, default=REF_SET_CSV,
                   help=f"reference_set.csv path (default: {REF_SET_CSV})")
    p.add_argument("--preset", choices=sorted(CONDITION_PRESETS.keys()),
                   default="block_a",
                   help="Condition preset. 'block_a' = cognate + apo (default). "
                        "'block_b' = cognate + apo + shuffled + decoy, 40 Class A "
                        "panel (default receptors) — Block B Wide. "
                        "'extended_partners' = Gs / Gi / Gq / arrestin / apo — for Phase 6.")
    p.add_argument("--experiment-slug", default=None,
                   help="Experiment folder slug (used in request_id prefix). "
                        "Default: '018_block_a_switch_test' for preset=block_a, "
                        "'019_block_a_extended_partners' for preset=extended_partners.")
    p.add_argument("--dry-run", action="store_true",
                   help="Build rows + run pre-checks, but SKIP materialise_inputs "
                        "(no on-disk file writes; input_path/prediction_path stay empty). "
                        "Use locally to validate; then re-run without --dry-run on HPC.")

    args = p.parse_args(argv)

    # Default receptor list is preset-specific: block_b's default MUST be
    # the 40 Class A panel (BLOCK_B_CLASS_A), not the full 48-receptor
    # BLOCK_A_RECEPTORS — the Class B/F receptors in that list have no
    # shuffled/decoy construct FASTAs under refs/constructs_block_b/ and
    # would hard-fail. block_a and extended_partners keep their original
    # default (BLOCK_A_RECEPTORS) unchanged.
    default_receptors_by_preset: dict[str, list[str]] = {
        "block_b": BLOCK_B_CLASS_A,
    }
    receptors = args.receptors or default_receptors_by_preset.get(args.preset, BLOCK_A_RECEPTORS)
    conditions = CONDITION_PRESETS[args.preset]
    default_slug = {
        "block_a": "018_block_a_switch_test",
        "block_b": "019_block_b_partner_selection",
        "extended_partners": "019_block_a_extended_partners",
    }[args.preset]
    experiment_slug = args.experiment_slug or default_slug
    args.experiment_slug = experiment_slug   # store back for provenance emit

    mn = {
        "boltz":    tuple(args.boltz_mn),
        "of3":      tuple(args.of3_mn),
        "protenix": tuple(args.protenix_mn),
        "chai":     tuple(args.chai_mn),
    }

    # NB: manifest rows = seeds × backbones × conditions × receptors.
    # samples_per_seed is a per-row metadata column consumed by the qsub
    # template — it multiplies OUTPUT CIFs on disk, not manifest rows.
    n_cond = len(conditions)
    print(f"Manifest — preset={args.preset} slug={experiment_slug}")
    print(f"          {len(receptors)} receptors × {n_cond} conditions × 4 backbones")
    print(f"Conditions:")
    for cname, (ptype, pid, sc) in conditions.items():
        pid_display = pid or "-"
        print(f"  {cname:<12} type={ptype:<10} identity={pid_display:<20} state_claim={sc}")
    print(f"Per-backbone (seeds, samples_per_seed) → prediction structures per cell:")
    for bb, (s, n) in mn.items():
        print(f"  {bb:<10} ({s}, {n}) → {s} manifest rows × {n} samples = {s*n} CIFs/cell")
    total_manifest_rows = sum(s for (s, _) in mn.values()) * len(receptors) * n_cond
    total_output_cifs = sum(s * n for (s, n) in mn.values()) * len(receptors) * n_cond
    print(f"Expected manifest rows: {total_manifest_rows}")
    print(f"Expected output CIFs on disk (= rows.csv scale): {total_output_cifs}")
    print(f"Dry-run: {args.dry_run}")
    print()

    api = Api(cache_dir=args.cache_dir)
    ref_species_map = load_ref_species_map(args.ref_set)
    cognate_map = load_cognate_identities(COUPLING_CSV)
    print(f"Loaded {len(cognate_map)} cognate primary_ga_identity entries "
          f"from {COUPLING_CSV.relative_to(REPO)}")
    # Summary of the coupling classes present in the panel receptors.
    class_counts: dict[str, int] = {}
    for rec in receptors:
        ident = cognate_map.get(_canonicalise_receptor(rec).upper(), "?")
        class_counts[ident] = class_counts.get(ident, 0) + 1
    print("Per-identity panel counts:")
    for ident, n in sorted(class_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {ident:<12} {n}")
    print()

    rows, warnings = build_all_rows(
        receptors=receptors,
        conditions=conditions,
        mn_per_backbone=mn,
        api=api,
        ref_species_map=ref_species_map,
        output_root=args.output_root,
        dry_run=args.dry_run,
        experiment_slug=experiment_slug,
        cognate_map=cognate_map,
    )

    print(f"Built {len(rows)} manifest rows.")
    print(f"Warnings: {len(warnings)}")
    for w in warnings:
        print(f"  {w}")

    write_manifest(rows, args.manifest_out)
    print(f"Wrote {args.manifest_out}")

    prov_path = write_manifest_provenance(args.manifest_out, args)
    print(f"Wrote {prov_path}")

    # Non-zero return if any hard failures (FAIL/SKIP) — pre-check warns are OK
    hard_fails = [w for w in warnings if w.startswith(("SKIP ", "FAIL "))]
    if hard_fails:
        print(f"\n{len(hard_fails)} hard failures — receptor list needs cleanup.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
