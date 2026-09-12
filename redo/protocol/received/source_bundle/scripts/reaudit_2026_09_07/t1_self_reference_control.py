#!/usr/bin/env python3
"""T1 (BLOCKING) — self-reference control on the Block C 2×2.

The Stage 3a interaction on ``pocket_ca_rmsd_active`` / ``_inactive`` compares
each row against two structural references:

  * ``pocket_ca_rmsd_active`` — always the receptor's role="active" reference.
  * ``pocket_ca_rmsd_inactive`` — for antagonist rows, the ``role_specific =
    inactive_neutral_antagonist`` reference when curated; otherwise the
    generic ``role="inactive"`` reference. See ``scorer/pocket_metrics.py``
    lines 1210-1244.

Prior audit rounds flagged (in ``task_E_v3_scoped_finding.json``) that
``role_specific`` selection sets ``ref_pdb == input_bound_pdb`` on ~68 % of
neutral_antagonist rows for ``ligand_rmsd_to_ref``. This test asks the
same question for ``pocket_ca_rmsd_active/_inactive``, and — if the
asymmetry exists — reruns the 2×2 restricted to rows where neither
reference matches the input crystal.

If |restricted Δ| < 0.05 Å or the restricted CI now straddles zero on
a backbone, the rescue collapses on that backbone.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]

# Make ``scorer`` and ``scripts.stage3_post_audit_analysis`` importable so we
# reuse the exact 2×2 math from the campaign. Adversarial re-audit only needs
# to change the input row set — not the estimator.
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

# NOTE: stage3_post_audit_analysis.stage3a_2x2 accepts a list of dicts and an
# ``excluded_receptors`` set — no CLI wrapper needed for the recompute.
from stage3_post_audit_analysis import stage3a_2x2  # type: ignore  # noqa: E402


ROWS_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
MANIFEST_CSV = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
REF_SET_CSV = REPO / "refs/reference_set.csv"

OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/reaudit_2026_09_07"
OUT_JSON = OUT_DIR / "t1_self_reference_control.json"

PUBLISHED_INTERACTION = {
    "boltz":    {"estimate": -0.306, "ci_lo": -0.431, "ci_hi": -0.192},
    "chai":     {"estimate": -0.137, "ci_lo": -0.223, "ci_hi": -0.055},
    "of3":      {"estimate": -0.252, "ci_lo": -0.384, "ci_hi": -0.129},
    "protenix": {"estimate": -0.184, "ci_lo": -0.271, "ci_hi": -0.101},
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---- Regex to extract cell metadata from the manifest ``prediction_path`` ----
#
# Manifest prediction paths follow the pattern:
#   .../tier3/pool/<receptor>/<ligand_role>/<arm>/<backbone>/seed_<N>/...
# We use it as an independent second source of (receptor, role, arm, backbone,
# seed) alongside the pre-parsed CSV columns, per the audit's ground rule.
PRED_PATH_RE = re.compile(
    r"/tier3/pool/(?P<receptor>[^/]+)/(?P<ligand_role>[^/]+)/(?P<arm>[^/]+)/"
    r"(?P<backbone>[a-z0-9]+)/seed_(?P<seed>\d+)/"
)


def parse_prediction_path(p: str) -> dict[str, str] | None:
    m = PRED_PATH_RE.search(p)
    if not m:
        return None
    return m.groupdict()


def build_ref_lookup(ref_set: pd.DataFrame) -> dict[tuple[str, str, str], str]:
    """(receptor, role, role_specific) -> pdb_id.

    For the ``inactive`` role, we key on ``role_specific`` (empty string
    denotes the generic inactive reference). For ``active``, ``role_specific``
    is always empty.
    """
    d: dict[tuple[str, str, str], str] = {}
    for _, r in ref_set.iterrows():
        recep = str(r.get("receptor_slug") or "").upper().strip()
        role = str(r.get("role") or "").lower().strip()
        role_specific = str(r.get("role_specific") or "").strip()
        pdb = str(r.get("pdb_id") or "").upper().strip()
        if not recep or not role or not pdb:
            continue
        d[(recep, role, role_specific)] = pdb
    return d


def resolve_ref_pdb(
    lookup: dict[tuple[str, str, str], str],
    receptor: str,
    role: str,
    role_specific: str = "",
) -> str:
    """Match ``scorer/pocket_metrics.py:1067-1091`` selection semantics.

    - active: (receptor, "active", "")
    - inactive with role_specific: try (receptor, "inactive", role_specific),
      fall back to (receptor, "inactive", "")
    """
    receptor = receptor.upper()
    role = role.lower()
    if role == "active":
        return lookup.get((receptor, "active", ""), "")
    if role == "inactive":
        if role_specific:
            hit = lookup.get((receptor, "inactive", role_specific))
            if hit:
                return hit
        return lookup.get((receptor, "inactive", ""), "")
    return ""


def role_pair_for_ligand(ligand_role: str) -> tuple[str, str]:
    """Return (primary_role, primary_role_specific) for the row's active-arm
    lookup, matching ``_role_for_state_claim(Ga-coupled-active, ligand_role)``.

    Only used to compute the *inactive* companion reference for agonist /
    decoy / none rows, which fall through to the generic inactive per
    ``pocket_metrics.py:1221-1233``.
    """
    if ligand_role == "neutral_antagonist":
        return ("inactive", "inactive_neutral_antagonist")
    if ligand_role == "inverse_agonist":
        return ("inactive", "inactive_inverse_agonist")
    return ("active", "")


def compute_row_ref_pdbs(
    row: dict, manifest_bound_pdb: str, ref_lookup: dict
) -> tuple[str, str, str, str, str]:
    """(receptor, ligand_role, arm, ref_pdb_active, ref_pdb_inactive).

    Uses the manifest's ``ligand_bound_pdb`` for input_bound_pdb (that's the
    crystal the ligand was extracted from).
    """
    receptor = str(row.get("receptor_slug") or "").upper().strip()
    ligand_role = str(row.get("ligand_role") or "").strip()

    # Active companion — always vs role="active".
    ref_active = resolve_ref_pdb(ref_lookup, receptor, "active", "")

    # Inactive companion selection matches pocket_metrics.py:1210-1244.
    primary_role, primary_role_specific = role_pair_for_ligand(ligand_role)
    if primary_role == "inactive":
        ref_inactive = resolve_ref_pdb(
            ref_lookup, receptor, "inactive", primary_role_specific,
        )
    else:
        # Primary is active — inactive companion uses expected_specific,
        # else falls back to generic inactive (line 1231-1233).
        # For agonist / apo / decoy rows expected_specific is "" so we go
        # straight to generic.
        ref_inactive = resolve_ref_pdb(ref_lookup, receptor, "inactive", "")
    return receptor, ligand_role, ref_active, ref_inactive, manifest_bound_pdb.upper().strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", default=str(ROWS_CSV))
    parser.add_argument("--manifest", default=str(MANIFEST_CSV))
    parser.add_argument("--ref-set", default=str(REF_SET_CSV))
    parser.add_argument("--out", default=str(OUT_JSON))
    args = parser.parse_args()

    print(f"[T1] loading rows: {args.rows}")
    rows = pd.read_csv(args.rows, low_memory=False)
    print(f"[T1] loaded rows: n={len(rows)}")

    print(f"[T1] loading manifest: {args.manifest}")
    manifest = pd.read_csv(args.manifest, low_memory=False)
    print(f"[T1] loaded manifest: n={len(manifest)}")

    print(f"[T1] loading ref_set: {args.ref_set}")
    ref_set = pd.read_csv(args.ref_set, low_memory=False)
    print(f"[T1] loaded ref_set: n={len(ref_set)}")
    ref_lookup = build_ref_lookup(ref_set)

    # ---------------------------------------------------------------
    # Manifest -> ligand_bound_pdb by (receptor, ligand_role, arm, backbone, seed).
    # The manifest is keyed on prediction_path; rows are keyed on
    # input_path — same path in the layout used since Block C dispatch.
    # ---------------------------------------------------------------
    manifest["prediction_path"] = manifest["prediction_path"].astype(str)
    manifest_by_pred = manifest.set_index("prediction_path")

    # Rows have an ``input_path`` that equals the manifest prediction_path
    # verbatim per the campaign rule "RMSD driver reads input_path verbatim
    # from rows.csv" (CLAUDE.md).
    if "input_path" not in rows.columns:
        print("[T1] FATAL: rows.tier3.v2.csv missing input_path column", file=sys.stderr)
        return 1

    # Join ligand_bound_pdb + backbone + partner_type onto rows. Match
    # stage3_post_audit_analysis._load_rows behaviour so downstream
    # stage3a_2x2 sees rows with the expected keys.
    print("[T1] joining manifest.{ligand_bound_pdb,backbone,partner_type} onto rows via input_path...")
    m_idx = manifest.set_index("prediction_path")
    lookup_bound = m_idx["ligand_bound_pdb"].to_dict()
    lookup_backbone = m_idx["backbone"].to_dict()
    lookup_partner_type = m_idx["partner_type"].to_dict()
    rows["input_bound_pdb"] = rows["input_path"].map(lookup_bound).fillna("")
    rows["backbone"] = rows["input_path"].map(lookup_backbone).fillna("")
    rows["partner_type"] = rows["input_path"].map(lookup_partner_type).fillna("")

    # Also join the manifest's own (receptor, ligand_role, arm, backbone) as
    # an independent check on the rows' pre-parsed columns.
    lookup_pathmeta = {}
    for pp in manifest["prediction_path"]:
        parsed = parse_prediction_path(pp)
        if parsed:
            lookup_pathmeta[pp] = parsed
    rows["_path_receptor"] = rows["input_path"].map(
        lambda p: (lookup_pathmeta.get(p, {}) or {}).get("receptor", "")
    )
    rows["_path_ligand_role"] = rows["input_path"].map(
        lambda p: (lookup_pathmeta.get(p, {}) or {}).get("ligand_role", "")
    )
    rows["_path_arm"] = rows["input_path"].map(
        lambda p: (lookup_pathmeta.get(p, {}) or {}).get("arm", "")
    )
    rows["_path_backbone"] = rows["input_path"].map(
        lambda p: (lookup_pathmeta.get(p, {}) or {}).get("backbone", "")
    )

    # ---------------------------------------------------------------
    # For each row, resolve the active + inactive reference PDBs.
    # ---------------------------------------------------------------
    print("[T1] resolving reference PDBs per row...")
    receptors = rows["receptor_slug"].fillna("").astype(str).str.upper()
    ligand_roles = rows["ligand_role"].fillna("").astype(str)

    def _resolve_active(r):
        return resolve_ref_pdb(ref_lookup, r, "active", "")

    def _resolve_inactive(r, lr):
        primary_role, primary_specific = role_pair_for_ligand(lr)
        if primary_role == "inactive":
            return resolve_ref_pdb(ref_lookup, r, "inactive", primary_specific)
        return resolve_ref_pdb(ref_lookup, r, "inactive", "")

    rows["ref_pdb_active_recomputed"] = [
        _resolve_active(r) for r in receptors
    ]
    rows["ref_pdb_inactive_recomputed"] = [
        _resolve_inactive(r, lr) for r, lr in zip(receptors, ligand_roles)
    ]

    # ---------------------------------------------------------------
    # T1b — self-reference fraction per cell (backbone × ligand_role × arm).
    # ---------------------------------------------------------------
    print("[T1b] tabulating self-reference fractions...")

    # Only Class A pocket rows (scorer restriction).
    rows_class_a = rows[
        rows["receptor_class"].fillna("").astype(str).str.upper() == "A"
    ].copy()
    passed = rows_class_a["passed"].astype(str).str.lower() == "true"
    rows_class_a = rows_class_a[passed]

    rows_class_a["ligand_role_clean"] = (
        rows_class_a["ligand_role"].fillna("").astype(str).str.strip()
    )
    rows_class_a["input_bound_pdb_u"] = (
        rows_class_a["input_bound_pdb"].fillna("").astype(str).str.upper().str.strip()
    )
    rows_class_a["backbone_clean"] = (
        rows_class_a["backbone"].fillna("").astype(str).str.lower().str.strip()
    )

    rows_class_a["ref_matches_active"] = (
        rows_class_a["ref_pdb_active_recomputed"] == rows_class_a["input_bound_pdb_u"]
    ) & (rows_class_a["input_bound_pdb_u"] != "")
    rows_class_a["ref_matches_inactive"] = (
        rows_class_a["ref_pdb_inactive_recomputed"] == rows_class_a["input_bound_pdb_u"]
    ) & (rows_class_a["input_bound_pdb_u"] != "")

    per_cell = []
    for bb in sorted(rows_class_a["backbone_clean"].unique()):
        for lr in sorted(rows_class_a["ligand_role_clean"].unique()):
            sub = rows_class_a[
                (rows_class_a["backbone_clean"] == bb)
                & (rows_class_a["ligand_role_clean"] == lr)
            ]
            if len(sub) == 0:
                continue
            n = len(sub)
            for ref_side, matches_col in (
                ("active", "ref_matches_active"),
                ("inactive", "ref_matches_inactive"),
            ):
                n_match = int(sub[matches_col].sum())
                per_cell.append({
                    "backbone": bb,
                    "ligand_role": lr,
                    "reference": ref_side,
                    "n_rows": int(n),
                    "n_self_reference": n_match,
                    "fraction_self_reference": n_match / n if n else float("nan"),
                })

    # ---------------------------------------------------------------
    # T1c — 2×2 restricted to rows where NEITHER reference matches input_bound_pdb.
    # We keep only rows where both ref_matches_active AND ref_matches_inactive
    # are False. Then feed the subset back into stage3a_2x2().
    # ---------------------------------------------------------------
    print("[T1c] re-running 2×2 with self-reference rows dropped...")
    restricted = rows_class_a[
        (~rows_class_a["ref_matches_active"])
        & (~rows_class_a["ref_matches_inactive"])
    ].copy()

    # Baseline (no restriction) — recompute to confirm we can reproduce the
    # published value locally before doing the restricted variant.
    full = rows_class_a.copy()

    def _to_records(df: pd.DataFrame) -> list[dict]:
        # stage3a_2x2 reads dict keys from rows; pass strings.
        return df.astype(str).to_dict("records")

    full_result = stage3a_2x2(_to_records(full))
    restricted_result = stage3a_2x2(_to_records(restricted))

    # ---------------------------------------------------------------
    # T1d — surviving n per backbone × cell.
    # ---------------------------------------------------------------
    surviving_summary = {}
    for bb in sorted(restricted["backbone_clean"].unique()):
        sub = restricted[restricted["backbone_clean"] == bb]
        surviving_summary[bb] = {
            "n_rows": int(len(sub)),
            "n_receptors": int(sub["receptor_slug"].nunique()),
            "n_agonist_rows": int((sub["ligand_role_clean"] == "full_agonist").sum()),
            "n_antag_rows": int(
                sub["ligand_role_clean"].isin(
                    ["neutral_antagonist", "inverse_agonist"]
                ).sum()
            ),
        }

    # ---------------------------------------------------------------
    # Per-backbone verdicts.
    # ---------------------------------------------------------------
    def _verdict(bb: str) -> str:
        r_bb = restricted_result.get("per_backbone", {}).get(bb, {})
        interaction = r_bb.get("interaction", {})
        est = interaction.get("estimate", float("nan"))
        lo = interaction.get("ci_lo", float("nan"))
        hi = interaction.get("ci_hi", float("nan"))
        n_common = interaction.get("n_receptors_in_common", 0)
        if n_common < 15:
            return f"UNDERPOWERED (n_common={n_common})"
        import math
        if math.isnan(est) or math.isnan(lo) or math.isnan(hi):
            return f"UNDERPOWERED (NaN interaction, n_common={n_common})"
        if abs(est) < 0.05:
            return f"RESCUE_COLLAPSES (|Δ|={abs(est):.3f} < 0.05)"
        if (lo < 0 < hi) or (hi < 0 < lo):
            return f"RESCUE_COLLAPSES (CI [{lo:.3f}, {hi:.3f}] straddles zero)"
        # Sign-consistent and non-trivial magnitude.
        return "RESCUE_SURVIVES_SELF_REFERENCE_CONTROL"

    verdicts = {bb: _verdict(bb) for bb in sorted(PUBLISHED_INTERACTION.keys())}

    # ---------------------------------------------------------------
    # Assemble the report.
    # ---------------------------------------------------------------
    report = {
        "task": "T1_self_reference_control",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "rows": {
                "path": str(Path(args.rows).relative_to(REPO)),
                "sha256": sha256_file(Path(args.rows)),
                "n_rows": int(len(rows)),
            },
            "manifest": {
                "path": str(Path(args.manifest).relative_to(REPO)),
                "sha256": sha256_file(Path(args.manifest)),
                "n_rows": int(len(manifest)),
            },
            "ref_set": {
                "path": str(Path(args.ref_set).relative_to(REPO)),
                "sha256": sha256_file(Path(args.ref_set)),
                "n_rows": int(len(ref_set)),
            },
        },
        "t1a_selector_trace": {
            "pocket_ca_rmsd_active": (
                "always vs receptor's role='active' reference "
                "(scorer/pocket_metrics.py:1194-1205); receptor-level, "
                "not ligand-role-conditional."
            ),
            "pocket_ca_rmsd_inactive": (
                "for antagonist rows (ligand_role in "
                "{neutral_antagonist, inverse_agonist}): role_specific "
                "inactive reference (inactive_neutral_antagonist or "
                "inactive_inverse_agonist) when curated, else generic "
                "inactive fallback (scorer/pocket_metrics.py:1210-1233). "
                "For agonist / apo / decoy rows: always generic inactive "
                "(scorer/pocket_metrics.py:1220-1233 with expected_specific="
                "''). The selector is the same _role_for_state_claim() "
                "used by ligand_rmsd_to_ref."
            ),
            "consequence": (
                "For antagonist rows, the inactive reference is the "
                "role_specific inactive PDB. If that PDB is the same "
                "crystal the antagonist ligand was extracted from "
                "(input_bound_pdb), the 2×2 antag_inactive cell is a "
                "self-comparison. The magnitude of the effect on the "
                "interaction (agonist_active - antag_active) - "
                "(agonist_inactive - antag_inactive) depends on how often "
                "ref_pdb_inactive == input_bound_pdb holds on antagonist "
                "rows only."
            ),
        },
        "t1b_self_reference_fractions": per_cell,
        "t1c_2x2_recomputed": {
            "baseline_full": full_result,
            "restricted_no_self_reference": restricted_result,
            "published_reference": PUBLISHED_INTERACTION,
        },
        "t1d_surviving_n": surviving_summary,
        "verdicts_by_backbone": verdicts,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(f"[T1] wrote {Path(args.out).relative_to(REPO)}")

    # Human-readable table to stdout.
    print()
    print("=" * 78)
    print("T1c — 2×2 interaction: published vs recomputed (full) vs restricted")
    print("=" * 78)
    print(f"{'backbone':<10} {'pub Δ':>8} {'pub CI':>18}  "
          f"{'full Δ':>8} {'full CI':>18}  "
          f"{'restr Δ':>8} {'restr CI':>18}  n_common")
    for bb in sorted(PUBLISHED_INTERACTION.keys()):
        pub = PUBLISHED_INTERACTION[bb]
        full_r = full_result.get("per_backbone", {}).get(bb, {}).get("interaction", {})
        restr_r = restricted_result.get("per_backbone", {}).get(bb, {}).get("interaction", {})
        print(
            f"{bb:<10} "
            f"{pub['estimate']:>+8.3f} [{pub['ci_lo']:+.3f}, {pub['ci_hi']:+.3f}]  "
            f"{full_r.get('estimate', float('nan')):>+8.3f} "
            f"[{full_r.get('ci_lo', float('nan')):+.3f}, {full_r.get('ci_hi', float('nan')):+.3f}]  "
            f"{restr_r.get('estimate', float('nan')):>+8.3f} "
            f"[{restr_r.get('ci_lo', float('nan')):+.3f}, {restr_r.get('ci_hi', float('nan')):+.3f}]  "
            f"n={restr_r.get('n_receptors_in_common', 0)}"
        )
    print()
    print("Verdicts (per backbone):")
    for bb, v in verdicts.items():
        print(f"  {bb:<10} {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
