"""Rerun manifest generator + fresh-rerun bookkeeping.

Two entry points:

  build_manifest(outputs_root, out_csv, ...)
      Walks ``outputs_root`` (the shared branch scratch root
      /hpc/scratch/sengaad1/subsampling/) and emits refs/rerun_manifest.csv
      with one row per co-folding prediction found in the M2 wave-spec.

  fresh_seed_for(prediction_sha)
      Deterministic new seed from the frozen prediction file SHA.

Both feed M2 Phase A' — see ~/.claude/plans/hey-claude-i-have-fluffy-brook.md.

**Amendment 3 (user):** batch driver NEVER aborts on raise. Manifest
distinguishes:
  - receptor_disambig_conflict — old substring rule disagrees with new
                                  word-boundary resolver
  - receptor_unresolved_in_original — frozen rule returned '?' or empty
                                       (~522 cap-exp + ~689 steering rows)
"""
from __future__ import annotations

import csv
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from scorer.cache import content_sha256
from scorer.receptors import (
    AmbiguousReceptorError,
    UnresolvedReceptorError,
    resolve_receptor,
)


# ---------------------------------------------------------------------------
# WaveGroup — an experiment cluster + its on-disk globs
# ---------------------------------------------------------------------------


@dataclass
class WaveGroup:
    slug: str
    branch: str                             # "cap-exp" | "steering"
    tier: str                               # "A_headline" | "B_support"
    path_globs: list[str] = field(default_factory=list)  # relative to outputs_root
    expected_control: dict[str, float] | None = None
    receptor_from_path: str = ""            # regex on the matched path


def default_wave_spec() -> list[WaveGroup]:
    """The 24 manuscript-critical experiment groups from the M2 plan.

    All paths are RELATIVE to ``/hpc/scratch/sengaad1/subsampling/`` (both
    branches share scratch — only which sibling dirs are used differs).

    Frozen on-disk layouts discovered via HPC forensics:
      - outputs/task3b_arm{1,2}_{multimer,control}/<uniprot_slug>/boltz_results_input/predictions/**/*.pdb
      - outputs/w40_<REC>_alpha5_<N>aa/predictions/boltz_results_input/predictions/**/*.pdb
      - outputs/w45_aa2ar_<CCD>_seed<N>/predictions/boltz_results_input/predictions/**/*.pdb
      - outputs/{of3,protenix}_multimer_*/<uniprot_slug>/**/*.cif
      - outputs/w14b_chai_task3b/<uniprot_slug>/**/*.pdb
      - outputs/w46_<REC>_{withGA,noGA}_af2m/**/*.pdb
      - weekend_2026_08_22/{w4,w5,w6,w6b,w6c,w6d,w6e,w2,w3,w7a}/<W-experiment>/out/boltz_results_inputs/predictions/**/*.pdb
      - round4/{phase|part|xcheck}*/out/boltz_results_inputs/predictions/**/*.pdb
      - alascan/p<N>/out/boltz_results_input/predictions/**/*.pdb
      - mech_ideas/M<N>_*/out/boltz_results_input/predictions/**/*.pdb
      - round2/{lenB,panelA}_*/out/boltz_results_input/predictions/**/*.pdb
      - proteome_extended/out/boltz_results_inputs/predictions/**/*.pdb
      - track_b_closure/pilot1/{of3,ptx}/out/**/*.cif

    Since Boltz consistently emits predictions deep under
    ``boltz_results_input(s)/predictions/**/*.pdb``, we use plain ``**``
    from the experiment root. Path.glob() in Python treats ``**`` as
    zero-or-more directories.
    """
    return [
        # ---- Cap-exp headlines --------------------------------------------
        WaveGroup(
            slug="task3b_boltz",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/task3b_arm1_multimer/**/*.pdb",
                "outputs/task3b_arm2_control/**/*.pdb",
            ],
            receptor_from_path=r"task3b_arm[12](?:_multimer|_control)/([^/]+)/",
        ),
        WaveGroup(
            slug="task3b_of3",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/of3_multimer_full46/**/*.cif",
                "outputs/of3_multimer_noga_full46/**/*.cif",
                "outputs/of3_multimer_shuffled_full46/**/*.cif",
                "outputs/of3_multimer_task3b/**/*.cif",
                "outputs/w12b_of3_task3b_arm2/**/*.cif",
            ],
            receptor_from_path=r"outputs/(?:of3_multimer_[a-z_46]+|w12b_of3_task3b_arm2)/([^/]+)/",
        ),
        WaveGroup(
            slug="task3b_protenix",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/protenix_multimer_full46/**/*.cif",
                "outputs/protenix_multimer_noga_full46/**/*.cif",
                "outputs/protenix_multimer_shuffled_full46/**/*.cif",
                "outputs/protenix_multimer_task3b/**/*.cif",
                "outputs/w12b_protenix_task3b_arm2/**/*.cif",
            ],
            receptor_from_path=r"outputs/(?:protenix_multimer_[a-z_46]+|w12b_protenix_task3b_arm2)/([^/]+)/",
        ),
        WaveGroup(
            slug="task3b_chai",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/w14b_chai_task3b/*/*.cif",
                "outputs/w15b_chai_task3b_arm2/*/*.cif",
            ],
            receptor_from_path=r"w1[45]b_chai_task3b(?:_arm2)?/([^/]+)/",
        ),
        WaveGroup(
            slug="w46_af2m",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/w46_*_af2m*/**/*.pdb",
                "outputs/w46b_*/**/*.pdb",
                "outputs/w46c_*/**/*.pdb",
                # 2026-08-25 audit: w46b + w46c af2m arms also landed on
                # the steering scratch root — extend so both branches
                # are picked up.
                "weekend_2026_08_22/**/w46[bc]_*/**/*.pdb",
                "weekend_2026_08_22/**/W46[bc]_*/**/*.pdb",
            ],
            receptor_from_path=r"outputs/w46[a-z]?_([A-Z0-9]+)_",
        ),
        WaveGroup(
            slug="w40_alpha5_ladder",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/w40_*_alpha5_*aa/**/*.pdb",
                # 2026-08-25 fresh-angle audit: OF3+Ptx multimer_alpha5
                # were missed by Boltz-only glob. Sanity-control spread
                # Boltz 90 / OF3 80 / Ptx 29 needs all three.
                "outputs/of3_multimer_alpha5/**/*.cif",
                "outputs/protenix_multimer_alpha5/**/*.cif",
            ],
            receptor_from_path=r"outputs/w40_([A-Z0-9]+)_alpha5_",
            expected_control={"boltz": 90.0, "of3": 80.0, "protenix": 29.0},
        ),
        WaveGroup(
            slug="w45_aa2ar_n140",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/w45_aa2ar_*_seed*/**/*.pdb",
                # 2026-08-25 fresh-angle audit: extends AA2AR bimodality
                # to OF3+Ptx backbones (n=50 each).
                "outputs/of3_multimer_aa2ar_n50/**/*.cif",
                "outputs/protenix_multimer_aa2ar_n50/**/*.cif",
            ],
            receptor_from_path=r"w45_(aa2ar)_|(?:of3_|protenix_)multimer_(aa2ar)_n50",
        ),
        WaveGroup(
            # 2026-08-25 audit: w43 AA2AR sampling-budget ablation
            # (Amendment 10e, 20 tasks × n=20). Supports Task-3b headline
            # defensibility — sensitivity of active-rate to sampling_steps.
            slug="w43_aa2ar_sampling_budget",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/w43_*/**/*.pdb",
                "weekend_2026_08_22/**/w43_*/**/*.pdb",
            ],
            receptor_from_path=r"w43_(aa2ar|[A-Z0-9]+)_",
        ),
        WaveGroup(
            # 2026-08-25 audit: w49 20-seed variance envelope on AA2AR
            # (Amendment 10l, 10 tasks × n=20). Variance baseline for
            # the AA2AR bimodality headline (paired with w45).
            slug="w49_aa2ar_seed_variance",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/w49_*/**/*.pdb",
                "weekend_2026_08_22/**/w49_*/**/*.pdb",
            ],
            receptor_from_path=r"w49_(aa2ar|[A-Z0-9]+)_",
        ),
        WaveGroup(
            slug="w39_adversarial_ga",
            branch="cap-exp", tier="A_headline",
            path_globs=[
                "outputs/w39a_boltz_scr40mer_n20/**/*.pdb",
                "outputs/w39b_boltz_gcn4_n20/**/*.pdb",
            ],
            receptor_from_path=r"predictions/([a-z0-9]+_human|[a-z0-9]+_mouse)/",
        ),
        WaveGroup(
            slug="aa2ar_confidence_vs_correctness",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/multimer_n50_hi/**/*.pdb",
                "outputs/multimer_aa2ar_replicate/**/*.pdb",
            ],
            receptor_from_path=r"multimer_(?:n50_hi|aa2ar_replicate)/([^/]+)?",
        ),
        # ---- Steering headlines (weekend, round4, proteome) ---------------
        WaveGroup(
            slug="w6d_beta2ar_chemistry_code",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w6d/W6d_boltz_l15_ladder_n20/**/*.pdb",
                "weekend_2026_08_22/w6d/W6d_boltz_e19_ladder_n20/**/*.pdb",
                "weekend_2026_08_22/w6b/W6b_boltz_l21_ladder_n20/**/*.pdb",
                "weekend_2026_08_22/w6/W6_verify_y18m/**/*.pdb",
                "weekend_2026_08_22/w6/W6_verify_l21i_e19d/**/*.pdb",
                "weekend_2026_08_22/w6e/W6E_boltz_adrb2_gs_n100/**/*.pdb",
                "weekend_2026_08_22/w6e/W6E_ptx_adrb2_gs_n100/**/*.cif",
            ],
            receptor_from_path=r"predictions/(adrb2[a-z0-9_]*)/",
        ),
        WaveGroup(
            slug="cam_two_lever",
            branch="steering", tier="A_headline",
            path_globs=[
                "proteome_extended/out/**/*.pdb",
                "proteome_exploration_2/out/**/*.pdb",
                "proteome_exploration_r3/out/**/*.pdb",
                "weekend_2026_08_22/w4/W4G_cam_prospective_boltz/**/*.pdb",
                "weekend_2026_08_22/w4/W4E_cam_n50_boltz/**/*.pdb",
                "weekend_2026_08_22/w4/W4E_cam_n50_of3/**/*.cif",
                "weekend_2026_08_22/w4/W4E_cam_n50_ptx/**/*.cif",
                "weekend_2026_08_22/w5/W5K_cam_*/**/*.pdb",
                "weekend_2026_08_22/w5/W5K_cam_*/**/*.cif",
                "weekend_2026_08_22/w2/W2_cam_chem_boltz/**/*.pdb",
                "weekend_2026_08_22/w2/W2_highn_cam_boltz/**/*.pdb",
                # 2026-08-25 fresh-angle audit: cross-backbone CaM chem
                "weekend_2026_08_22/w3/W3_cam_chem_of3/**/*.cif",
            ],
            receptor_from_path=r"predictions/(cam[a-z0-9_]*|calm[a-z0-9_]*)/",
        ),
        WaveGroup(
            slug="round4_mechanism",
            branch="steering", tier="A_headline",
            path_globs=[
                "round4/phase1_bundle/out/**/*.pdb",
                "round4/phase2_bundle/out/**/*.pdb",
                "round4/phase3alt_bundle/out/**/*.pdb",
                "round4/phase4_bundle/out/**/*.pdb",
                "round4/part3_killshot/out/**/*.pdb",
                "round4/part4_ood/out/**/*.pdb",
                "round4/xcheck_A_gai1_chem/out/**/*.pdb",
                "round4/xcheck_B_ood/out/**/*.pdb",
            ],
            receptor_from_path=r"predictions/([a-z0-9]+)_[a-z0-9_]+/",
        ),
        WaveGroup(
            slug="w5f_prospective_peptide_design",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w5f/W5F_prospective_boltz/**/*.pdb",
                "weekend_2026_08_22/w5f/W5F_prospective_of3/**/*.cif",
                "weekend_2026_08_22/w5f/W5F_prospective_ptx/**/*.cif",
            ],
            receptor_from_path=r"W5F_prospective_(boltz|of3|ptx)",
        ),
        WaveGroup(
            slug="class_b_asymmetry",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w6b/W6b_glp1r_boltz_n50/**/*.pdb",
                "weekend_2026_08_22/w6b/W6b_calcr_ptx_n50/**/*.cif",
                "weekend_2026_08_22/w6c/W6c_calcr_boltz_n50/**/*.pdb",
                "weekend_2026_08_22/w6c/W6c_glp1r_ptx_n50/**/*.cif",
                # 2026-08-25 audit: extends to Class B natives across
                # 5 receptors (GCGR/PTHR1/CRHR1/VIPR1/SCTR) — MASTER §5b
                # Wave 44 breadth.
                "weekend_2026_08_22/w6c/W6c_classb_boltz_native_test/**/*.pdb",
                "weekend_2026_08_22/w6c/W6c_classb_of3_native_test/**/*.cif",
                "weekend_2026_08_22/w6c/W6c_classb_ptx_native_test/**/*.cif",
            ],
            receptor_from_path=r"W6[bc]_(?:classb_(?:boltz|of3|ptx)_native_test|(glp1r|calcr))_",
        ),
        # ---- Support tier -------------------------------------------------
        WaveGroup(
            slug="w8_holo_factorial",
            branch="cap-exp", tier="B_support",
            path_globs=[
                "outputs/multimer_holo_ga_full/**/*.pdb",
                "outputs/multimer_holo_noga_full/**/*.pdb",
                "outputs/of3_multimer_holo_ga_full/**/*.cif",
                "outputs/of3_multimer_holo_noga_full/**/*.cif",
                "outputs/protenix_multimer_holo_ga_full/**/*.cif",
                "outputs/protenix_multimer_holo_noga_full/**/*.cif",
            ],
            receptor_from_path=r"(?:multimer|of3_multimer|protenix_multimer)_holo_[a-z]+_full/([^/]+)/",
        ),
        WaveGroup(
            slug="w47_adrb2_negative",
            branch="cap-exp", tier="B_support",
            path_globs=["outputs/w47_adrb2_*_seed*/**/*.pdb"],
            receptor_from_path=r"w47_(adrb2)_",
        ),
        WaveGroup(
            slug="w42_a5_tip_mutant",
            branch="cap-exp", tier="B_support",
            path_globs=["outputs/w42_*_gas_F376A_L388A/**/*.pdb"],
            receptor_from_path=r"w42_([A-Z0-9]+)_gas_",
        ),
        WaveGroup(
            slug="w41_adenosine_paralogs",
            branch="cap-exp", tier="B_support",
            path_globs=["outputs/w41_*_seed42/**/*.pdb"],
            receptor_from_path=r"w41_([A-Z0-9]+)_",
        ),
        WaveGroup(
            slug="w50_2_apo_gapfill",
            branch="cap-exp", tier="B_support",
            path_globs=[
                "outputs/w50_2_*_apo_*/**/*.pdb",
                "outputs/w50_2_*_apo_*/**/*.cif",
            ],
            receptor_from_path=r"w50_2_([A-Z0-9]+)_apo_",
        ),
        WaveGroup(
            slug="w54b_apo_topup",
            branch="cap-exp", tier="B_support",
            path_globs=[
                "outputs/w54b_*_apo*/**/*.pdb",
                "outputs/w54b_*_apo*/**/*.cif",
            ],
            receptor_from_path=r"w54b_[a-z0-9]+_([A-Z0-9]+)_apo",
        ),
        WaveGroup(
            slug="alanine_scan_p01_p21",
            branch="steering", tier="B_support",
            path_globs=["alascan/p*/out/**/*.pdb"],
            receptor_from_path=r"alascan/p(\d+)/",
        ),
        WaveGroup(
            slug="mechanism_panel_m1_m6",
            branch="steering", tier="B_support",
            path_globs=["mech_ideas/M*_*/out/**/*.pdb"],
            receptor_from_path=r"mech_ideas/M(\d+)_[a-z0-9_]+/",
        ),
        WaveGroup(
            slug="r2_lenb_r2_panela",
            branch="steering", tier="B_support",
            path_globs=[
                "round2/lenB_*/out/**/*.pdb",
                "round2/panelA_*/out/**/*.pdb",
            ],
            receptor_from_path=r"round2/(lenB|panelA)_[a-z0-9_]+/",
        ),
        WaveGroup(
            slug="track_b_pilot",
            branch="steering", tier="B_support",
            path_globs=[
                "track_b_closure/pilot1/of3/out/**/*.cif",
                "track_b_closure/pilot1/ptx/out/**/*.cif",
            ],
            receptor_from_path=r"track_b_closure/pilot1/(of3|ptx)/",
        ),

        # ================================================================
        # 2026-08-25 4-audit consolidation — 26 new WaveGroups + 4 glob
        # extensions confirmed on basel-hpc scratch. All 20 recovered
        # from load-bearing manuscript claims (`docs/DRAFT_ABSTRACT_v22.md`,
        # `session_final_2026_08_23.md`, `MASTER_STATUS.md` §5b/c evidence
        # pyramid) AND verified empirically via `find *.pdb|*.cif | wc -l`
        # on `/hpc/scratch/sengaad1/subsampling/` (steering root — where
        # cap-exp jobs also land except for `outputs/w54*/` on the
        # cap-exp-owned root).
        # ================================================================

        # ---- Headline (A) ---------------------------------------------
        WaveGroup(
            # v22 §Nature-framing 4 — killshot mitigated for
            # ADRB1/CCR8/PD2R2 (three receptors accept any α-helical
            # peptide). This is the LOAD-BEARING data — the LATE
            # `w39_adversarial_ga` resubmit is empty.
            slug="w39_early_adversarial",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/multimer_decoy_scrambled/**/*.pdb",
                "outputs/multimer_decoy_alpha5/**/*.pdb",
                "outputs/multimer_decoy_nonga/**/*.pdb",
            ],
            receptor_from_path=r"outputs/multimer_decoy_[a-z]+/([^/]+)/",
        ),
        WaveGroup(
            # v22 abstract — ZMA row of AA2AR ligand-response gradient.
            # 6-slug antag factorial across Boltz + OF3 + Protenix on
            # BOTH branches' roots (cap-exp originally, but landed on
            # steering scratch too per the fresh-angle steering audit).
            slug="w3_antag_factorial",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/multimer_antag_ga_full/**/*.pdb",
                "outputs/multimer_antag_noga_full/**/*.pdb",
                "outputs/of3_multimer_antag_ga_full/**/*.cif",
                "outputs/of3_multimer_antag_noga_full/**/*.cif",
                "outputs/protenix_multimer_antag_ga_full/**/*.cif",
                "outputs/protenix_multimer_antag_noga_full/**/*.cif",
            ],
            receptor_from_path=r"outputs/(?:multimer|of3_multimer|protenix_multimer)_antag_[a-z]+_full/([^/]+)/",
        ),
        WaveGroup(
            # MASTER §7 axis 21 — β-arrestin1 finger-loop peptide drives
            # INactive-state on all four AF3-family backbones.
            slug="arrestin_bidirectional",
            branch="steering", tier="A_headline",
            path_globs=[
                "outputs/multimer_bidirectional_arrestin/**/*.pdb",
                "outputs/boltz_bidirectional_arrestin/**/*.pdb",
                "outputs/of3_bidirectional_arrestin/**/*.cif",
                "outputs/of3_multimer_bidirectional_arrestin/**/*.cif",
                "outputs/protenix_bidirectional_arrestin/**/*.cif",
                "outputs/w23a_boltz_arr2_panel/**/*.pdb",
            ],
            receptor_from_path=r"outputs/(?:multimer|boltz|of3|of3_multimer|protenix)_bidirectional_arrestin/([^/]+)/",
        ),
        WaveGroup(
            # v22 §11.6 + MASTER Wave 12c — training-density falsification;
            # μOR chemistry-blind despite more Gi complexes than β2AR.
            # Union of cap-exp bz/of3/ptx_w8a-e/w9b-c AND steering
            # W8x/W8y/W8z/W9a-d + multimer_w8c_wrongagonist/w8d_neutral.
            slug="w8_reviewer_hardening",
            branch="steering", tier="A_headline",
            path_globs=[
                # cap-exp naming
                "outputs/boltz_w8a_*/**/*.pdb",
                "outputs/boltz_w8b_*/**/*.pdb",
                "outputs/boltz_w8c_*/**/*.pdb",
                "outputs/boltz_w8d_*/**/*.pdb",
                "outputs/boltz_w8e_*/**/*.pdb",
                "outputs/of3_w8[abcde]_*/**/*.cif",
                "outputs/protenix_w8[abcde]_*/**/*.cif",
                "outputs/ptx_w8[abcde]_*/**/*.cif",
                "outputs/boltz_w9b_*/**/*.pdb",
                "outputs/boltz_w9c_*/**/*.pdb",
                "outputs/of3_w9[bc]_*/**/*.cif",
                "outputs/protenix_w9[bc]_*/**/*.cif",
                # steering-root variants + neutral/wrongagonist
                "outputs/multimer_w8c_wrongagonist/**/*.pdb",
                "outputs/multimer_w8d_neutral/**/*.pdb",
                "outputs/of3_multimer_w8c_wrongagonist/**/*.cif",
                "outputs/of3_multimer_w8d_neutral/**/*.cif",
                # steering weekend W8x/y/z + W9a-d (LEL crossreceptor,
                # scaffold scan, optcode ×3bb, scrambled)
                "weekend_2026_08_22/w8x/**/*.pdb",
                "weekend_2026_08_22/w8x/**/*.cif",
                "weekend_2026_08_22/w8y/**/*.pdb",
                "weekend_2026_08_22/w8y/**/*.cif",
                "weekend_2026_08_22/w8z/**/*.pdb",
                "weekend_2026_08_22/w8z/**/*.cif",
                "weekend_2026_08_22/w9a/**/*.pdb",
                "weekend_2026_08_22/w9a/**/*.cif",
                "weekend_2026_08_22/w9b/**/*.pdb",
                "weekend_2026_08_22/w9b/**/*.cif",
                "weekend_2026_08_22/w9c/**/*.pdb",
                "weekend_2026_08_22/w9c/**/*.cif",
                "weekend_2026_08_22/w9d/**/*.pdb",
                "weekend_2026_08_22/w9d/**/*.cif",
            ],
            receptor_from_path=r"w[89][a-z0-9]?_(?:[a-z]+_)?([A-Z0-9]+)_",
        ),
        WaveGroup(
            # Table 1 Wave 48 — Chai-1 arrestin-parity row (~82.3%).
            slug="w48_chai_arrestin",
            branch="steering", tier="A_headline",
            path_globs=["outputs/w48_*_chai_arrestin/**/*.cif"],
            receptor_from_path=r"w48_([^_]+)_chai_arrestin",
        ),
        WaveGroup(
            # session_final §Reviewer objections: OF3-defaults-active
            # defense. W5-A stress: `weekend/w5a/W5A_{of3,ptx}_stress`.
            slug="w5a_of3_stress",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w5a/W5A_of3_stress/**/*.cif",
                "weekend_2026_08_22/w5a/W5A_ptx_stress/**/*.cif",
            ],
            receptor_from_path=r"W5A_(?:of3|ptx)_stress/([^/]+)/",
        ),
        WaveGroup(
            # session_final §Reviewer: β2AR mouse/rat/cow memorization
            # test.
            slug="w5e_beta2ar_species",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w5e/W5E_species_boltz/**/*.pdb",
                "weekend_2026_08_22/w5e/W5E_species_ptx/**/*.cif",
            ],
            receptor_from_path=r"W5E_species_(?:boltz|ptx)/([^/]+)/",
        ),
        WaveGroup(
            # session_final §Reviewer: "rules-are-post-hoc" defense —
            # 80% correct on reverse-fail library.
            slug="w5i_failure_library",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w5i/W5I_cam_revfail_boltz/**/*.pdb",
                "weekend_2026_08_22/w5i/W5I_revfail_boltz/**/*.pdb",
                "weekend_2026_08_22/w5i/W5I_revfail_of3/**/*.cif",
                "weekend_2026_08_22/w5i/W5I_revfail_ptx/**/*.cif",
            ],
            receptor_from_path=r"W5I_(?:cam_)?revfail_(?:boltz|of3|ptx)/([^/]+)/",
        ),
        WaveGroup(
            # Extends chemistry code to Gαq/Gαo — session_final §Dimension.
            slug="w5j_gaq_gao_ladders",
            branch="steering", tier="A_headline",
            path_globs=["weekend_2026_08_22/w5j/W5J_gq_go_ladder_boltz/**/*.pdb"],
            receptor_from_path=r"W5J_gq_go_ladder_boltz/([^/]+)/",
        ),
        WaveGroup(
            # session_final §Dimension 2 — "Only Class A" objection;
            # mGluRs / CaSR / GABBR2 null on all 3bb.
            slug="w5n_class_c_mgluR",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w5n/W5N_classc_boltz/**/*.pdb",
                "weekend_2026_08_22/w5n/W5N_classc_of3/**/*.cif",
                "weekend_2026_08_22/w5n/W5N_classc_ptx/**/*.cif",
            ],
            receptor_from_path=r"W5N_classc_(?:boltz|of3|ptx)/([^/]+)/",
        ),
        WaveGroup(
            # Wave 7a — orthologs (close/distant/GLP1R) + r16/y18 ladders
            # + null polyD/E/G/K/R cross-family robustness.
            slug="w7a_orthologs_ladders",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w7a/W7a_boltz_close_orthologs/**/*.pdb",
                "weekend_2026_08_22/w7a/W7a_boltz_distant_orthologs/**/*.pdb",
                "weekend_2026_08_22/w7a/W7a_boltz_glp1r_orthologs/**/*.pdb",
                "weekend_2026_08_22/w7a/W7a_boltz_r16_ladder_n20/**/*.pdb",
                "weekend_2026_08_22/w7a/W7a_boltz_y18_ladder_n20/**/*.pdb",
                "weekend_2026_08_22/w7a/W7a_ptx_close_orthologs/**/*.cif",
            ],
            receptor_from_path=r"W7a_(?:boltz|ptx)_(?:close|distant|glp1r|r16|y18)_[a-z_0-9]+/([^/]+)/",
        ),
        WaveGroup(
            # W7b + W7bx + W7d density-scan cluster. Training density is
            # a nuisance parameter of the ORIGINAL job (baked into the
            # checkpoint), NOT the fresh seed — for M2.4 fresh rerun,
            # this group is optional (density-scan analysis doesn't
            # gain from re-folding). Kept in the manifest for M2.2
            # rescore. Tag scope carefully at submission time.
            slug="w7bd_density_scan",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w7b/**/*.pdb",
                "weekend_2026_08_22/w7bx/**/*.pdb",
                "weekend_2026_08_22/w7d/**/*.pdb",
                "weekend_2026_08_22/w7d/**/*.cif",
            ],
            receptor_from_path=r"W7b[x]?_boltz_([a-z0-9]+)_d\d+|W7d_[a-z0-9]+_([a-z0-9]+)_",
        ),
        WaveGroup(
            # Session_final §next-priorities — 3bb OOD test on new
            # receptors.
            slug="w4f_ood_test",
            branch="steering", tier="A_headline",
            path_globs=[
                "weekend_2026_08_22/w4f/W4F_ood_boltz/**/*.pdb",
                "weekend_2026_08_22/w4f/W4F_ood_of3/**/*.cif",
                "weekend_2026_08_22/w4f/W4F_ood_ptx/**/*.cif",
            ],
            receptor_from_path=r"W4F_ood_(?:boltz|of3|ptx)/([^/]+)/",
        ),
        WaveGroup(
            # W7b AA2AR n=50 — outside weekend tree; feeds AA2AR
            # bimodality density-scaling subclaim.
            slug="w7b_aa2ar_n50",
            branch="steering", tier="A_headline",
            path_globs=["outputs/w7b_boltz_aa2ar_n50/**/*.pdb"],
            receptor_from_path=r"w7b_boltz_(aa2ar)_n50",
        ),

        # ---- Support (B) ----------------------------------------------
        WaveGroup(
            # session_final §Reviewer: polyA/polyK/polyE nulls across
            # Boltz + Ptx (OF3 arms empty per reality check).
            slug="w5d_null_ligand_controls",
            branch="steering", tier="B_support",
            path_globs=[
                "weekend_2026_08_22/w5d/W5D_boltz_polyA_n100/**/*.pdb",
                "weekend_2026_08_22/w5d/W5D_ptx_polyA_n100/**/*.cif",
                "weekend_2026_08_22/w3/W3_polyA_LELL_boltz/**/*.pdb",
                "weekend_2026_08_22/w3/W3_polyA_LELL_of3/**/*.cif",
                "weekend_2026_08_22/w3/W3_polyA_LELL_ptx/**/*.cif",
            ],
            receptor_from_path=r"W(?:5D|3)_[a-zA-Z_]+/([^/]+)/",
        ),
        WaveGroup(
            slug="w4a_permissive",
            branch="steering", tier="B_support",
            path_globs=[
                "weekend_2026_08_22/w4a/W4A_permissive_of3/**/*.cif",
                "weekend_2026_08_22/w4a/W4A_permissive_ptx/**/*.cif",
            ],
            receptor_from_path=r"W4A_permissive_(?:of3|ptx)/([^/]+)/",
        ),
        WaveGroup(
            slug="w4c_crossbb_validation",
            branch="steering", tier="B_support",
            path_globs=[
                "weekend_2026_08_22/w4c/W4C_crossbb_of3_n20/**/*.cif",
                "weekend_2026_08_22/w4c/W4C_crossbb_ptx_n20/**/*.cif",
            ],
            receptor_from_path=r"W4C_crossbb_(?:of3|ptx)_n20/([^/]+)/",
        ),
        WaveGroup(
            slug="w4d_third_template",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w4d/W4D_third_template_boltz/**/*.pdb"],
            receptor_from_path=r"W4D_third_template_boltz/([^/]+)/",
        ),
        WaveGroup(
            slug="w2_gao_alanine",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w2/W2_gao_alanine_boltz/**/*.pdb"],
            receptor_from_path=r"W2_gao_alanine_boltz/([^/]+)/",
        ),
        WaveGroup(
            slug="w2_gaq_alanine",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w2/W2_gaq_alanine_boltz/**/*.pdb"],
            receptor_from_path=r"W2_gaq_alanine_boltz/([^/]+)/",
        ),
        WaveGroup(
            slug="w2_highn_beta2ar",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w2/W2_highn_beta2ar_boltz/**/*.pdb"],
            receptor_from_path=r"W2_highn_beta2ar_boltz/([^/]+)/",
        ),
        WaveGroup(
            # Distinct from w40_alpha5_ladder — W2 coarse length ladder,
            # ×3bb, smaller n. Both are load-bearing (coarse-then-fine).
            slug="w2_length",
            branch="steering", tier="B_support",
            path_globs=[
                "weekend_2026_08_22/w2/W2_length_boltz/**/*.pdb",
                "weekend_2026_08_22/w2/W2_length_of3/**/*.cif",
                "weekend_2026_08_22/w2/W2_length_ptx/**/*.cif",
            ],
            receptor_from_path=r"W2_length_(?:boltz|of3|ptx)/([^/]+)/",
        ),
        WaveGroup(
            # W7c double + triple-failure mechanism controls (~60 preds).
            slug="w7c_mechanism_controls",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w7c/**/*.pdb"],
            receptor_from_path=r"W7c_[a-z_]+/([^/]+)/",
        ),
        WaveGroup(
            # W7e R131 DRY-anchor mutation ladder (~20 preds).
            slug="w7e_r131_ladder",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w7e/W7e_boltz_r131_ladder_n10/**/*.pdb"],
            receptor_from_path=r"W7e_boltz_r131_ladder_n10/([^/]+)/",
        ),
        WaveGroup(
            # W7f double-break control (~20 preds).
            slug="w7f_double_break",
            branch="steering", tier="B_support",
            path_globs=["weekend_2026_08_22/w7f/W7f_boltz_double_break_n20/**/*.pdb"],
            receptor_from_path=r"W7f_boltz_double_break_n20/([^/]+)/",
        ),
        WaveGroup(
            # Expands the (now-dropped) wc4_bz 3-pred marginal into the
            # 3-embed AA2AR pair-rep null set (CLR/NEC/ZMA).
            slug="wc4_aa2ar_embed",
            branch="steering", tier="B_support",
            path_globs=["outputs/wc4_aa2ar_*_embed/**/*.pdb"],
            receptor_from_path=r"wc4_aa2ar_[A-Z]+_embed/([^/]+)/",
        ),
    ]


# ---------------------------------------------------------------------------
# Backbone inference (file ext + parent-dir hints)
# ---------------------------------------------------------------------------


BACKBONE_DIR_HINTS = [
    (re.compile(r"/of3_multimer[_/]|/W\d+[a-zA-Z_]*_of3_|/of3/|/W5F_prospective_of3"), "of3"),
    (re.compile(r"/protenix_multimer[_/]|/W\d+[a-zA-Z_]*_ptx_|/ptx/|/W6[bc]?_[a-z]+_ptx_"), "protenix"),
    (re.compile(r"/w1[24-79][a-z]?_chai|_chai(_|/|$)|/chai_|/chai1"), "chai"),
    (re.compile(r"_af2m(_|/|$)|/af2_|_af2mm_"), "af2mm"),
    (re.compile(r"/afcluster"), "afcluster"),
]


def infer_backbone(path: str) -> str:
    for pat, name in BACKBONE_DIR_HINTS:
        if pat.search(path):
            return name
    if path.endswith(".pdb"):
        return "boltz"
    if path.endswith(".cif"):
        return "of3"
    return "unknown"


# ---------------------------------------------------------------------------
# Frozen substring rule — reproduces audit_a1v3_register.py:53-58 verbatim
# ---------------------------------------------------------------------------


FROZEN_RECEPTOR_LIST = [
    "AA1R", "AA2AR", "AA2BR", "AA3R", "ADA1A", "ADA2A",
    "ADRB1", "ADRB2", "ADRB3",
    "ACM1", "ACM2", "ACM3", "ACM4", "ACM5",
    "5HT1A", "5HT1B", "5HT2A", "5HT2B", "5HT2C", "5HT5A", "5HT6R", "5HT7R",
    "DRD1", "DRD2", "DRD3", "DRD4", "DRD5",
    "OPRD", "OPRK", "OPRM", "OPRX", "OPSD",
    "HRH1", "HRH2", "HRH3", "HRH4",
    "NK1R", "NK2R", "NK3R",
    "GHSR", "MC4R", "CNR1", "CNR2", "GLP1R", "CALCR",
    "CXCR1", "CXCR2", "CXCR3", "CXCR4", "CCR2", "CCR5", "CCR6", "CCR8",
    "MTR1A", "MTR1B", "EDNRA", "EDNRB",
    "SSR2", "TRHR", "V2R", "FSHR", "LSHR", "TSHR",
    "AGTR1", "APJ", "C5AR1", "CASR", "CCKAR", "CRFR1",
    "GRM2", "GRM3", "GRM4", "GRM5", "GRPR",
    "LPAR1", "LT4R1", "MCHR1", "NPY1R", "NPY2R",
    "NTR1", "OX2R", "OXYR", "PD2R2", "PE2R4",
    "S1PR1", "S1PR5", "SMO", "TA2R",
    "CAM", "CALM",  # for the CaM two-lever positive-control path
]


def frozen_substring_receptor(path: str) -> str:
    p = path.upper()
    for r in FROZEN_RECEPTOR_LIST:
        if r in p:
            return r
    return "?"


# ---------------------------------------------------------------------------
# Fresh-seed derivation
# ---------------------------------------------------------------------------


def fresh_seed_for(prediction_sha256_hex: str) -> int:
    """Deterministic new seed from the frozen prediction's file SHA."""
    return int(prediction_sha256_hex[:8], 16) & 0x7fffffff


# ---------------------------------------------------------------------------
# Manifest builder
# ---------------------------------------------------------------------------


def _extract_receptor_from_path(path: str, pattern: str) -> str:
    if not pattern:
        return ""
    m = re.search(pattern, path)
    if not m:
        return ""
    for g in m.groups():
        if g:
            return g.upper()
    return ""


def _iter_prediction_files(outputs_root: Path, group: WaveGroup) -> Iterable[Path]:
    seen: set[Path] = set()
    for g in group.path_globs:
        for p in outputs_root.glob(g):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def build_manifest(
    outputs_root: os.PathLike[str] | str,
    out_csv: os.PathLike[str] | str,
    *,
    wave_spec: list[WaveGroup] | None = None,
    steering_outputs_root: os.PathLike[str] | str | None = None,
    extra_outputs_roots: list[os.PathLike[str] | str] | None = None,
    max_per_group: int | None = None,
    compute_sha: bool = True,
) -> dict[str, Any]:
    outputs_root = Path(outputs_root).resolve()
    if steering_outputs_root is None:
        steering_outputs_root = outputs_root
    steering_outputs_root = Path(steering_outputs_root).resolve()
    # Extra roots (e.g. subsampling-cap-exp/ for w54b) are walked in
    # addition to the primary roots. Every group's globs try each root.
    extra_roots = [Path(r).resolve() for r in (extra_outputs_roots or [])]
    wave_spec = wave_spec or default_wave_spec()

    counts: dict[str, int] = {}
    disambig_conflicts = 0
    unresolved_in_original = 0
    total_rows = 0
    seen_paths: set[str] = set()  # dedup across roots

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        cols = [
            "prediction_path", "prediction_sha", "experiment_slug", "wave_group",
            "branch", "tier", "backbone",
            "receptor_from_path_substring", "receptor_resolved",
            "disambig_conflict", "receptor_unresolved_in_original",
            "expected_control_json", "new_seed",
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()

        for group in wave_spec:
            branch_root = (steering_outputs_root
                           if group.branch == "steering"
                           else outputs_root)
            group_roots = [branch_root, *extra_roots]
            group_count = 0
            for root in group_roots:
                for p in _iter_prediction_files(root, group):
                    if max_per_group is not None and group_count >= max_per_group:
                        break
                    ps = str(p)
                    if ps in seen_paths:
                        continue
                    seen_paths.add(ps)

                    sha = content_sha256(p) if compute_sha else ""
                    bb = infer_backbone(ps)
                    sub_rec = frozen_substring_receptor(ps)
                    try:
                        new_rec, _ = resolve_receptor(ps)
                    except (AmbiguousReceptorError, UnresolvedReceptorError):
                        new_rec = ""
                    group_hint = _extract_receptor_from_path(
                        ps, group.receptor_from_path
                    )
                    if not new_rec and group_hint:
                        new_rec = group_hint

                    disambig = (
                        sub_rec not in ("", "?") and new_rec and sub_rec != new_rec
                    )
                    unresolved_orig = sub_rec in ("", "?")
                    if disambig:
                        disambig_conflicts += 1
                    if unresolved_orig:
                        unresolved_in_original += 1

                    w.writerow({
                        "prediction_path": ps,
                        "prediction_sha": sha,
                        "experiment_slug": group.slug,
                        "wave_group": group.slug,
                        "branch": group.branch,
                        "tier": group.tier,
                        "backbone": bb,
                        "receptor_from_path_substring": sub_rec,
                        "receptor_resolved": new_rec,
                        "disambig_conflict": str(bool(disambig)).lower(),
                        "receptor_unresolved_in_original":
                            str(bool(unresolved_orig)).lower(),
                        "expected_control_json":
                            json.dumps(group.expected_control) if group.expected_control else "",
                        "new_seed": (fresh_seed_for(sha) if sha else ""),
                    })
                    total_rows += 1
                    group_count += 1
            counts[group.slug] = group_count

    return {
        "total_rows": total_rows,
        "per_group_counts": counts,
        "disambig_conflicts": disambig_conflicts,
        "unresolved_in_original": unresolved_in_original,
        "out_csv": str(out_csv),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="gpcr-manifest",
        description="Build refs/rerun_manifest.csv from HPC outputs tree.")
    p.add_argument("--outputs-root",
                   default="/hpc/scratch/sengaad1/subsampling/",
                   help="Branch scratch root (outputs/ + weekend_/ + round4/ + ... are siblings).")
    p.add_argument("--steering-outputs-root", default=None)
    p.add_argument("--extra-root", action="append", default=None,
                   help="Additional roots to walk (each group's globs try every root). "
                        "Use to pull in cap-exp scratch: --extra-root /hpc/scratch/sengaad1/subsampling-cap-exp/")
    p.add_argument("--out", default="refs/rerun_manifest.csv")
    p.add_argument("--max-per-group", type=int, default=None)
    p.add_argument("--no-sha", action="store_true")
    args = p.parse_args(argv)

    summary = build_manifest(
        outputs_root=args.outputs_root,
        out_csv=args.out,
        steering_outputs_root=args.steering_outputs_root,
        extra_outputs_roots=args.extra_root,
        max_per_group=args.max_per_group,
        compute_sha=not args.no_sha,
    )
    import sys
    print(json.dumps(summary, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
