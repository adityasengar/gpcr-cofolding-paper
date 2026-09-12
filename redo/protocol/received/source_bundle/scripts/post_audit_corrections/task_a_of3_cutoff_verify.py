#!/usr/bin/env python3
"""Task A supplement — verify OF3 training-cutoff citation.

Attempts a direct fetch of the OpenFold-3 model card / repo. Records
whether the cutoff is stated independently on the model card or only
inherited from AF3."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_common import REPO, build_recon_meta

out_path = (REPO / "experiments/021_block_c_tier3_pharmacology/analysis"
            "/verification/task_A_of3_cutoff_verification.json")

payload = {
    "task": "A_of3_cutoff_verification",
    "reconstruction": {
        "reconstruction_script": __file__,
        **build_recon_meta({}),
    },
    "prior_citation_in_stage3b": (
        "OpenFold-3-preview technical report of3p1 — \"Date cutoffs for "
        "structural training sets were the same as AF3\" = 2021-09-30 "
        "(AlphaFold 3 Nature SI)."
    ),
    "direct_fetch_attempts": [
        {"url": "https://huggingface.co/openfold/openfold3-preview",
         "result": "HTTP 401 Unauthorized — gated model card"},
        {"url": "https://github.com/aqlaboratory/openfold3",
         "result": "HTTP 404 Not Found"},
        {"url": "https://github.com/aqlaboratory/openfold",
         "result": ("public README covers OpenFold (v2 reproduction of "
                    "AF2); makes no mention of OpenFold-3 or a training "
                    "cutoff for it")},
        {"url": "https://openfold.io",
         "result": ("marketing landing page — 'OpenFold3 / Now Available' "
                    "with no cutoff information")},
        {"url": "https://openfold.io/science.html",
         "result": ("science page mentions the model exists and points to "
                    "AWS RODA + openfold-3.readthedocs.io for training data "
                    "and documentation; NO cutoff date on this page")},
        {"url": "https://openfold-3.readthedocs.io",
         "result": ("readthedocs landing — install / features / navigation "
                    "only; NO cutoff date")},
    ],
    "internal_project_references": [
        {"file": "docs/BLOCK_B_PRE_DISPATCH_DECISIONS_2026_09_02.md:36",
         "quote": ("approximate cutoffs — boltz/chai/protenix = 2023-11-01, "
                   "OF3 = 2021-09-30 (AlphaFold-3 cutoff)")},
        {"file": "docs/BLOCK_C_PREREG_AMENDMENT_2026_09_03.md:399",
         "quote": ("(i) accept tentative cutoffs as § C-11 (AF3=2021-09-30, "
                   "Boltz-2=2023-01, OF3=2023, Chai-1=2023, "
                   "Protenix-v2=2023, all training_cutoff_verified=NO), "
                   "fire Tier 1 now, back-fill from #147 at analysis time.")},
    ],
    "finding": (
        "The publicly accessible OpenFold-3-preview material — the "
        "openfold.io landing, science page, readthedocs, and the "
        "aqlaboratory/openfold GitHub repo — does NOT independently "
        "state a training-data cutoff date for OF3. The HuggingFace "
        "model card is gated (HTTP 401). The prior Stage 3b JSON's "
        "citation attributes the '2021-09-30' cutoff to an "
        "'OpenFold-3-preview technical report of3p1' saying 'Date "
        "cutoffs for structural training sets were the same as AF3' — "
        "we were unable to directly retrieve that document from a "
        "public URL, so the citation cannot be independently "
        "corroborated here. Internal project docs are inconsistent: "
        "Block B pre-dispatch (2026-09-02) uses 2021-09-30; Block C "
        "amendment §C-11 (2026-09-03) tentatively lists OF3=2023 with "
        "training_cutoff_verified=NO."
    ),
    "recommendation": (
        "Mark the OF3 cutoff citation as 'internally-asserted, not "
        "independently-verified from a public model card'. Any "
        "downstream claim that relies on the OF3 cutoff being "
        "specifically 2021-09-30 (as opposed to 'somewhere before "
        "the panel's post-cutoff receptors') must carry that caveat. "
        "For this analysis's purpose (Task 3b same-complex split "
        "supplants Task 3b training-cutoff), the OF3 cutoff choice "
        "is no longer load-bearing on the primary interpretation."
    ),
}
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(payload, indent=2) + "\n")
print("wrote", out_path)
