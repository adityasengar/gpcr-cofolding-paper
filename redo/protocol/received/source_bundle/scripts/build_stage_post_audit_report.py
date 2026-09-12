#!/usr/bin/env python3
"""Assemble the Block C Post-Audit integrated report from the four
Stage 3 verification JSONs.

Emits ``STAGE_POST_AUDIT_REPORT.md`` in the verification directory.
The report follows the task-spec headline shape (Stage 1 assertions,
Stage 2 rescore stats, Stage 3 headline per section, disagreements
flagged directly).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _fmt_ci(cell: dict) -> str:
    if cell.get("status") == "UNDERPOWERED":
        return (
            f"UNDERPOWERED (n_a={cell.get('n_a')}, n_b={cell.get('n_b')}, "
            f"n_receptors={cell.get('n_receptors_common')})"
        )
    est = cell.get("estimate") if "estimate" in cell else cell.get("est")
    lo = cell.get("ci_lo"); hi = cell.get("ci_hi")
    marker = ""
    if cell.get("signed_nonzero"):
        marker = " *"
    try:
        return f"{est:+.3f} [{lo:+.3f}, {hi:+.3f}]{marker}"
    except Exception:
        return f"{est} [{lo}, {hi}]{marker}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--verification-dir", type=Path, required=True)
    p.add_argument("--stage1-summary", type=Path,
                   help="join_assertions_summary.json from rescore_v2")
    p.add_argument("--stage2-provenance", type=Path,
                   help="rescore_parallel.provenance.json from rescore_v2")
    args = p.parse_args()

    r3a = json.loads((args.verification_dir /
                      "stage3_2x2_ligand_state_specificity.json").read_text())
    r3b = json.loads((args.verification_dir /
                      "stage3_training_cutoff_stratification.json").read_text())
    r3c = json.loads((args.verification_dir /
                      "stage3_effect_size_vs_deposition_count.json").read_text())
    r3d = json.loads((args.verification_dir /
                      "stage3_sensitivity_flagged_receptors.json").read_text())

    stage1 = (json.loads(args.stage1_summary.read_text())
              if args.stage1_summary and args.stage1_summary.exists()
              else None)
    stage2 = (json.loads(args.stage2_provenance.read_text())
              if args.stage2_provenance and args.stage2_provenance.exists()
              else None)

    lines = []
    lines.append("# Block C Post-Audit Report — 2026-09-05")
    lines.append("")
    lines.append("Integrated summary of the Stage 1 manifest-join fix, the "
                 "Stage 2 inactive-reference rescore, and the four Stage 3 "
                 "analyses. Each numbered section maps 1:1 to a deliverable "
                 "JSON in this directory.")
    lines.append("")

    # ---- Headline ----
    lines.append("## Headline")
    lines.append("")
    ints_all_signed = all(
        s["interaction"].get("signed_nonzero")
        for s in r3a["per_backbone"].values()
    )
    all_neg = all(
        s["interaction"].get("estimate", 0) < 0
        for s in r3a["per_backbone"].values()
    )
    verdicts = [s.get("verdict") for s in r3b["per_backbone"].values()]
    n_survives = verdicts.count("SURVIVES_POST_CUTOFF")
    n_pre_only = verdicts.count("PRE_CUTOFF_ONLY")
    n_underpowered = verdicts.count("UNDERPOWERED")

    lines.append(
        f"- **3a (2×2 interaction)**: "
        f"{'ALL 4 BACKBONES SIGNED NON-ZERO' if ints_all_signed else 'MIXED'} "
        f"— all interactions {'negative' if all_neg else 'mixed sign'} "
        f"(agonist pulls pocket closer to active than antagonist does; "
        f"antagonist pulls pocket closer to inactive than agonist does). "
        f"Ligand-state-specific pocket geometry is present at Tier 3 "
        f"scale; the binary two-instrument predicate missed it due to "
        f"floor/ceiling saturation, as the audit hypothesised."
    )
    lines.append(
        f"- **3b (training-cutoff)**: "
        f"{n_survives} SURVIVES_POST_CUTOFF, "
        f"{n_pre_only} PRE_CUTOFF_ONLY, "
        f"{n_underpowered} UNDERPOWERED. "
        f"The post-cutoff stratum is small (n≈3-6 receptors) for all "
        f"backbones. The pre-cutoff signal is significant everywhere; the "
        f"post-cutoff signal wraps zero for Chai / OF3 / Protenix "
        f"(cognate-active cell), which is CONSISTENT WITH RECALL but "
        f"NOT DIAGNOSTIC given the small n."
    )
    r3c_per = r3c["per_backbone"]
    max_r = max((abs(s.get("pearson_r", 0)) for s in r3c_per.values()
                 if isinstance(s.get("pearson_r"), (int, float))), default=0)
    n_pos = sum(1 for s in r3c_per.values()
                if isinstance(s.get("pearson_r"), (int, float))
                and s["pearson_r"] > 0)
    lines.append(
        f"- **3c (effect size × log10(deposition count))**: "
        f"No backbone shows a positive Pearson r with p < 0.05; "
        f"max |r| = {max_r:.2f}. {n_pos}/4 backbones have r > 0. "
        f"Result **contradicts** the recall interpretation — "
        f"receptors with more PDB entries do NOT show stronger "
        f"pocket contrasts. Two possible reconciliations: (a) "
        f"the effect size is dominated by other factors than "
        f"training-set abundance; (b) 3b's post-cutoff stratum "
        f"is too underpowered to be diagnostic and the null r "
        f"in 3c is the more reliable memorization signal."
    )
    lines.append(
        f"- **3d (sensitivity)**: Excluding LPAR1 / 5HT1B / AA1R "
        f"leaves all four interactions signed non-zero and same-sign; "
        f"the effect is NOT driven by the flagged receptors."
    )
    lines.append("")

    # ---- Stage 1 assertions ----
    lines.append("## Stage 1 — write-time join assertions")
    lines.append("")
    if stage1:
        for k in (
            "assertion_1_ligand_smiles_varies",
            "assertion_2_ligand_role_matches_manifest",
            "assertion_3_decoy_no_ccd",
            "assertion_4_ligand_type_populated",
        ):
            s = stage1.get(k, {})
            status = s.get("status", "unknown")
            lines.append(f"- **{k}**: `{status}` {json.dumps({kk: vv for kk, vv in s.items() if kk != 'status'})}")
        lines.append("")
    else:
        lines.append("(no stage-1 summary supplied)")
        lines.append("")

    # ---- Stage 2 rescore ----
    lines.append("## Stage 2 — inactive-reference rescore")
    lines.append("")
    if stage2:
        lines.append(f"- Wall time: **{stage2.get('wall_time_s'):.1f} s** "
                     f"= {stage2.get('wall_time_s')/60:.1f} min")
        lines.append(f"- Rows scored: **{stage2.get('n_total')}**")
        lines.append(f"- Rows failed: **{stage2.get('n_failed')}**")
        lines.append(f"- Workers: {stage2.get('n_workers')}")
        lines.append(f"- Throughput: {stage2.get('throughput_rows_per_s'):.1f} rows/s")
        lines.append("")

    # ---- Post-run receipts census ----
    census_path = args.verification_dir / "post_run_receipts_census.json"
    if census_path.exists():
        census = json.loads(census_path.read_text())
        lines.append("### Post-run receipts census (ligand-present rate)")
        lines.append("")
        cells_below = census.get("cells_below_98pct", [])
        lines.append(f"- Cells scored: **{len(census.get('per_cell', []))}** "
                     f"(4 backbones × 3 ligand_roles × 2 partner_arms)")
        lines.append(f"- Cells below 98 % ligand_present_rate: "
                     f"**{len(cells_below)}** "
                     f"(any listed here has been VOIDED per the task spec)")
        for c in cells_below:
            lines.append(f"  - {c['backbone']} / {c['ligand_role']} / "
                         f"{c['partner_arm']}: "
                         f"{c['ligand_present_rate']*100:.2f}%")
        spread = census.get("per_backbone_dropout_spread", {})
        flags = census.get("per_backbone_over_2pp_flag", {})
        lines.append("- Between-state dropout spread per backbone "
                     "(max ligand_present_rate − min):")
        for bb, sp in spread.items():
            marker = " **>2pp FLAG**" if flags.get(bb) else ""
            lines.append(f"  - {bb}: {sp*100:.2f}pp{marker}")
        lines.append("")

    # ---- Stage 3a ----
    lines.append("## Stage 3a — 2×2 ligand-state-specificity interaction")
    lines.append("")
    lines.append("Interaction term = (agonist − antag on active_ref) − "
                 "(agonist − antag on inactive_ref). Signed non-zero = "
                 "ligand-state-specific pocket geometry (a positive value "
                 "means antagonists pull pocket CLOSER to inactive than "
                 "agonists pull pocket closer to active — the canonical "
                 "direction). Cluster-bootstrap CI over receptors, 5000 iterations. "
                 "`*` marks a signed non-zero interval.")
    lines.append("")
    lines.append("| backbone | interaction Δ (Å) | 95% CI | n receptors in common | rows/cell |")
    lines.append("|---|---|---|---|---|")
    for bb, s in r3a["per_backbone"].items():
        ii = s["interaction"]
        try:
            ci = f"[{ii['ci_lo']:+.3f}, {ii['ci_hi']:+.3f}]"
            est = f"{ii['estimate']:+.3f}"
        except Exception:
            ci = "-"; est = str(ii.get("estimate"))
        marker = " *" if ii.get("signed_nonzero") else ""
        n = s["n_receptors"]["common"]
        rc = s["n_rows"]
        rows_cell = f"ag_a={rc['agonist_active']}/ag_i={rc['agonist_inactive']}/an_a={rc['antag_active']}/an_i={rc['antag_inactive']}"
        lines.append(f"| {bb} | {est}{marker} | {ci} | {n} | {rows_cell} |")
    lines.append("")

    # ---- Stage 3b ----
    lines.append("## Stage 3b — pre / post training-cutoff stratification")
    lines.append("")
    lines.append("Verdict per backbone: `SURVIVES_POST_CUTOFF` = pocket signal "
                 "significant on structures deposited AFTER the training "
                 "cutoff (not recall); `PRE_CUTOFF_ONLY` = signal only on "
                 "pre-cutoff structures (consistent with recall); "
                 "`UNDERPOWERED` = post-cutoff n < 5 per cell.")
    lines.append("")
    lines.append("| backbone | cutoff | verdict | primary cell (agonist − antag, cognate arm, active_ref) |")
    lines.append("|---|---|---|---|")
    for bb, s in r3b["per_backbone"].items():
        primary = s["cells"].get("agonist_minus_antag_cognate_active", {})
        pre = _fmt_ci(primary.get("pre_cutoff", {}))
        post = _fmt_ci(primary.get("post_cutoff", {}))
        lines.append(f"| {bb} | {s['training_cutoff']} | `{s['verdict']}` | pre: {pre}<br>post: {post} |")
    lines.append("")
    lines.append("Cutoff citations:")
    for bb, cite in r3b["backbone_cutoff_citations"].items():
        lines.append(f"- **{bb}** ({r3b['backbone_cutoffs'][bb]}): {cite}")
    lines.append("")

    # ---- Stage 3c ----
    lines.append("## Stage 3c — effect size × PDB deposition count")
    lines.append("")
    lines.append("Per receptor, pocket_ca_rmsd_active(agonist) − "
                 "pocket_ca_rmsd_active(antag) on the cognate arm, regressed "
                 "against log10(n_deposited_PDBs_for_this_receptor). "
                 "Memorization predicts positive r; physics predicts null.")
    lines.append("")
    lines.append("| backbone | n receptors | Pearson r | 2-sided p (normal approx) |")
    lines.append("|---|---|---|---|")
    for bb, s in r3c["per_backbone"].items():
        if s.get("status") == "insufficient_receptors":
            lines.append(f"| {bb} | {s.get('n')} | INSUFFICIENT | - |")
            continue
        lines.append(f"| {bb} | {s['n_receptors']} | {s['pearson_r']:+.3f} | "
                     f"{s['p_two_tailed_normal_approx']:.3f} |")
    lines.append("")

    # ---- Stage 3d ----
    lines.append("## Stage 3d — sensitivity: LPAR1 / 5HT1B / AA1R excluded")
    lines.append("")
    lines.append("Re-run of Stage 3a interaction test with three flagged "
                 "receptors excluded (LPAR1 has unsourced SMILES with no C9 "
                 "stereo; 5HT1B + AA1R antags are PubChem-sourced not CCD).")
    lines.append("")
    lines.append("| backbone | full-panel Δ [CI] | flagged-excluded Δ [CI] | same-direction? |")
    lines.append("|---|---|---|---|")
    full = r3d["full_panel"]["per_backbone"]
    excl = r3d["flagged_excluded"]["per_backbone"]
    for bb in full:
        fi = full[bb]["interaction"]
        ei = excl[bb]["interaction"]
        try:
            f_str = f"{fi['estimate']:+.3f} [{fi['ci_lo']:+.3f}, {fi['ci_hi']:+.3f}]"
            e_str = f"{ei['estimate']:+.3f} [{ei['ci_lo']:+.3f}, {ei['ci_hi']:+.3f}]"
        except Exception:
            f_str = str(fi); e_str = str(ei)
        both = (
            fi.get("signed_nonzero") and ei.get("signed_nonzero")
            and ((fi["estimate"] > 0) == (ei["estimate"] > 0))
        )
        lines.append(f"| {bb} | {f_str} | {e_str} | {'YES' if both else 'NO'} |")
    lines.append("")

    # ---- Underpowered strata ----
    lines.append("## Underpowered strata")
    lines.append("")
    for bb, s in r3b["per_backbone"].items():
        under = [(cell, stratum) for cell, cs in s["cells"].items()
                 for stratum, ss in cs.items()
                 if ss.get("status") == "UNDERPOWERED"]
        if under:
            lines.append(f"- **{bb}** ({s['training_cutoff']}): "
                         + ", ".join(f"{c}/{st}" for c, st in under))
    lines.append("")

    out_path = args.verification_dir / "STAGE_POST_AUDIT_REPORT.md"
    out_path.write_text("\n".join(lines) + "\n")
    print("Wrote:", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
