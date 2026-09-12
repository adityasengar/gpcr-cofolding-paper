#!/usr/bin/env python3
"""The run registry — one row per experiment, whether it can run, and what the
plan of record does with it.

`CATALOGUE.md` says what COULD be run. `g1_systems.csv` / `g2_systems.csv` say
what IS enumerated. `RUN_MATRIX.md` says what it would cost and at which stage.
`CAMPAIGN.md` §2 says whether each one survives the nine findings. `DECISIONS.md`
says what has been ruled in or out. `PLAN.md` sequences the campaign into five
pillars. **Nothing joined those six**, so "what are we running?" had no answer you
could read off a file — which is how 36 of 45 experiments came to have no
enumerated systems without anyone noticing, and how 30 came to sit at
`NEEDS_TRIAGE` while `CAMPAIGN.md` §2 was already carrying a verdict and a reason
for every one of them.

This joins them. It DERIVES what is derivable and refuses to invent the rest: an
experiment whose status cannot be established from the files is marked
`NEEDS_TRIAGE`, never given a plausible status. A registry that guesses is worse
than no registry, because it reads as authoritative.

**The one thing that is authored rather than parsed, and how it is kept honest.**
`PLAN.md` names ZERO experiment ids — grep it, there are none — so the pillar
assignment cannot be parsed out of it. It is authored below in `PILLAR_MAP` and
`DECIDED`, and **every authored row carries a verbatim anchor that must be present
in the document it cites.** A basis that cites text the document does not contain
is a FAILURE, not a skip: `derive()` raises and the registry is not written. So
the crosswalk cannot rot silently when a spec is rewritten — it breaks loudly and
names the experiment.

Proved by planting, not asserted:

    python3 redo/build/run_registry.py --selftest

    python3 redo/build/run_registry.py
    python3 redo/build/manifest.py

Writes: inputs/run_registry.tsv
"""

import collections
import csv
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, SPEC  # noqa: E402

OUT = os.path.join(INPUTS, "run_registry.tsv")

EID = r"E\d+\.\d+"


class SpecError(RuntimeError):
    """A spec the registry depends on is missing, empty, or no longer says what
    a basis claims it says. Never downgraded to a warning: a check that quietly
    does nothing when its input is absent is the defect it exists to catch."""


def _read(spec, name):
    p = os.path.join(spec, name)
    if not os.path.exists(p):
        raise SpecError(f"{name} is absent from {spec} — cannot derive triage")
    return open(p).read()


# --------------------------------------------------------------------------
# The authored half: PLAN.md's pillars, and decisions that settle an item.
#
# Both tables map an experiment to (value, document, verbatim anchor). The
# anchor is checked against the document at run time. Keep anchors SHORT and
# distinctive -- they are a tripwire on the spec's wording, not a quotation.
# --------------------------------------------------------------------------

# eid -> (pillar, document, anchor, why this pillar discharges it)
PILLAR_MAP = {
    "E0.1": ("1", "PLAN.md", "726 calibration + 610 application + 98 pinned reference",
             "Pillar 1 IS the measurement pass E0.1 needs"),
    "E0.2": ("1", "PLAN.md", "726 calibration + 610 application + 98 pinned reference",
             "rides on E0.1's measurement pass, which is Pillar 1"),
    # E0.3 is deliberately NOT here either. Pillar 1's pass is 726 + 610 + 98,
    # and 726 + 610 = 1,336 is exactly the Active/Inactive split -- the 21 Class
    # A Intermediates E0.3 exists to measure are the rows that split EXCLUDES.
    # See PI_ANCHOR.
    # E0.4 is deliberately NOT here. It is the one Group 0 item that is free on
    # A and B today, staged at RUN_MATRIX 7.3 S0.7, and carries an empty
    # "Depends on" in the catalogue -- so the registry's blanket
    # `eid.startswith("E0.")` BLOCKED rule is wrong about it. See FREE_ANCHOR.

    "E1.1": ("3", "PLAN.md", "Length ladder: 11, 13, 15, 17, 19, 21, 26, full",
             "Pillar 3 IS the ladder"),
    "E1.2": ("3", "PLAN.md", "The matched nulls that answer",
             "R6a_da5 / R6b_a5perm / R6c_a5polyA / ubiquitin are Pillar 3's matched nulls"),
    "E1.3": ("3", "PLAN.md", "The matched nulls that answer",
             "composition- and order-matched controls are Pillar 3's matched nulls"),
    "E1.4": ("3", "PLAN.md", "Specificity**: family swap",
             "Pillar 3's specificity block names the family swap"),
    "E1.5": ("3", "PLAN.md", "the 21-position\n  alanine scan",
             "Pillar 3's specificity block names the alanine scan"),
    "E1.6": ("3", "PLAN.md", "the Gi/Gt single-residue natural pair",
             "Pillar 3's specificity block names the Gi/Gt pair"),
    "E1.7": ("3", "PLAN.md", "inputs/g1_systems.csv` (2,039 rows, 23 arms)",
             "R8_hetero is one of Pillar 3's 23 enumerated arms"),
    "E1.8": ("3", "PLAN.md", "known uncoupling point mutants",
             "Pillar 3's specificity block names the uncoupling mutants"),
    "E1.9": ("3", "PLAN.md", "G17 — partner MSA on vs off — is BLOCKING and belongs here",
             "Pillar 3 promotes G17/E1.9 from optional to blocking"),

    "E2.1": ("0", "PLAN.md", "Mine `rows.tier3.v2.csv`, steps 3–5",
             "Pillar 0 mines the file E2.1 asked for; its step 1 is already done"),
    "E2.2": ("4", "PLAN.md", "T1 small-molecule agonist vs antagonist at a fixed partner condition",
             "Pillar 4 IS the ligand crossing"),
    "E2.4": ("4", "PLAN.md", "decoy arm rides along as EXPLORATORY at k = 11",
             "Pillar 4 carries the decoy arm as an exploratory rider"),

    "E4.1": ("5", "PLAN.md", "A date-stratified holdout",
             "Pillar 5 names the date-stratified holdout"),

    "E6.1": ("0", "PLAN.md", "to `g1_recording_spec.tsv`",
             "Pillar 0 amends the recording spec, which is E6.1's contract enacted as an input"),

    "E8.3": ("0", "PLAN.md", "Measure the real MSA depths along the ladder",
             "Pillar 0's depth measurement is E8.3's realised-depth half"),
}

# eid -> (decision id, document, anchor, what it settled)
DECIDED = {
    "E0.5": ("D-2026-09-12-d", "DECISIONS.md",
             'This closes `E0.5` at option (a)',
             "closed at option (a) — drop B and F, the work is Class A"),
    "E2.4": ("D-2026-09-12-h", "DECISIONS.md",
             "The decoy arm RUNS at k = 11, as an EXPLORATORY arm",
             "runs at k=11 EXPLORATORY, frozen; the pre-registered bar stays at 12"),
    "E3.1": ("F-10", "DECISIONS.md",
             "P7 IS COMPUTED. The null holds: pLDDT does not separate.",
             "the receptor-conditional restatement is computed: 7,486 rows, every "
             "interval spans 0.5; HANDOVER's pooled 0.60-0.96 does not reproduce"),
    "E3.2": ("CATALOGUE E3.2", "CATALOGUE.md",
             "**Design.** Already computed",
             "already computed; both grains derived in redo/build/matrix_power.py"),
    "E5.2": ("CAMPAIGN 2.6", "CAMPAIGN.md",
             "**DIES** as an ask, **SURVIVES** as our own analysis",
             "dies as an upstream ask (F-7 makes the file describe an unusable arm); "
             "survives as our own analysis on our own rows"),
    "E7.2": ("D-2026-09-12-d", "DECISIONS.md",
             "**`E7.2` is parked, not killed.**",
             "parked behind the Class A scope decision; needs a class B instrument"),
    "E7.5": ("D-2026-09-12-e", "DECISIONS.md",
             "(c) buys three panel receptors, not a tier",
             "the panel expansion is priced: three receptors (cxcr3, mtr1a, mtr1b), "
             "held until the measurement pass is authorised"),
}

# Free/cheap items whose input is in hand and which NO pillar carries. The
# anchor is the catalogue's own cost line, so the claim "this is free" is the
# spec's, not ours.
FREE_ANCHOR = {
    "E0.4": ("CATALOGUE.md", "- **Cost.** `free` on A and B today."),
    "E3.3": ("CATALOGUE.md", "`free` on Block A; a required column on any new peptide arm"),
    "E4.2": ("CATALOGUE.md", "`free` — Block B rows plus the GPCRdb snapshot, both in hand"),
    "E4.3": ("CATALOGUE.md", "`free` to establish (a search over the deposited set)"),
    "E5.3": ("CATALOGUE.md", "**Question.** Does the partner *shift* the ensemble or *narrow* it?"),
    "E5.4": ("CATALOGUE.md", "Replace a threshold argument with a dose–response one"),
    "E5.5": ("CATALOGUE.md", "`free` on A and B; needs Block D's rows for D"),
    "E7.1": ("CATALOGUE.md", "free to write; `real` to test"),
    "E7.4": ("CATALOGUE.md", "`free` once one row-level ligand table exists"),
    "E9.1": ("CATALOGUE.md", "**Cost.** `free`, and most of it is done above"),
    "E9.3": ("CATALOGUE.md", "Report every rung against its own backbone's floor"),
}

# Items whose only remaining blocker is a choice Aditya has to make (authorise
# compute, send an ask upstream, or resolve a disagreement between two specs).
PI_ANCHOR = {
    "E0.3": ("DECISIONS.md", "the 21 excluded rows are the Class A Intermediates"),
    "E2.3": ("CAMPAIGN.md", "**E2.3** efficacy ladder | **DIES** for this campaign"),
    "E5.1": ("RUN_MATRIX.md", "steric exclusion at panel scale (E5.1)"),
    "E6.2": ("CAMPAIGN.md", "**CHANGES — demoted from rank 1**"),
    "E6.4": ("CAMPAIGN.md", "**SURVIVES**, blocking | Free before dispatch, impossible after"),
    "E7.3": ("CAMPAIGN.md", "**SURVIVES**, corrected to 8 receptors"),
    "E7.6": ("CAMPAIGN.md", "**CHANGES — its reagent is mislabelled**"),
    "E8.1": ("PLAN.md", "do not spend predictions pretending to close it"),
    "E8.2": ("MSA_SUBSAMPLING_REGIMES.md", "Stage 3 — regime (c), add the ligand"),
    "E9.2": ("CAMPAIGN.md", "**CHANGES — shrinks to the bistability bound**"),
}

# One line of prose per experiment, saying what the cited documents establish.
# Every one of these is backed by an anchor above; this is the human-readable
# half, never the evidence.
TRIAGE_WHY = {
    "E0.1": "PLAN.md Pillar 1 is the measurement pass; it does not start without Aditya's word",
    "E0.2": "rides on E0.1's pass (Pillar 1); CAMPAIGN.md 2.1 SURVIVES. TWO SCOPE LIMITS: PLAN.md Pillar 1 measures TWO axes and neither g1_recording_spec.tsv nor any pillar carries the PIF connector option (b) needs; and paajanen2026activation excluded arrestins, so option (c) cannot check E7.6's arrestin arm",
    "E0.3": "PILLAR 1 AS WRITTEN DOES NOT COVER IT, and the arithmetic is the argument: PLAN.md Pillar 1's pass is 726 + 610 + 98, and 726 + 610 = 1,336 is exactly the Class A Active/Inactive population — D-2026-09-12-d records that 'the 21 excluded rows are the Class A Intermediates', i.e. the very structures E0.3 exists to measure are the ones the pass excludes. Adding 21 rows is one decision. CAMPAIGN.md 2.1 SURVIVES, reading rule pre-committed (>=15 of 21 strictly between the cuts, or report the scatter)",
    "E0.4": "STATUS DISAGREES WITH THE SPECS: the registry marks every E0.* BLOCKED on the measurement pass, but CATALOGUE.md E0.4 costs it `free` on A and B today with an EMPTY 'Depends on', and RUN_MATRIX.md 7.3 S0.7 stages it among the free re-analyses. CAMPAIGN.md 2.1 promotes it — F-1 makes the continuous axes the SUBSTITUTE for the second instrument rather than a robustness extra. It is free now and no pillar carries it",
    "E0.5": "DECISIONS.md D-2026-09-12-d closes it at option (a); CAMPAIGN.md 2.1 DIES as an experiment, survives as one Methods sentence",
    "E1.1": "Pillar 3's ladder; CAMPAIGN.md 2.2 CHANGES (F-5: baseline, alignment regime and reading all move)",
    "E1.2": "Pillar 3's matched nulls; CAMPAIGN.md 2.2 CHANGES — R6b_a5perm is the true bulk control, non-Ga chains are the second",
    "E1.3": "Pillar 3's matched nulls; CAMPAIGN.md 2.2 CHANGES — its stated rationale was backwards, decisive only MSA-free",
    "E1.4": "Pillar 3's specificity block; CAMPAIGN.md 2.2 CHANGES — Gq is n=2 on the frozen panel, report as a bound",
    "E1.5": "Pillar 3's specificity block; CAMPAIGN.md 2.2 CHANGES — must run at ct21, MSA-free",
    "E1.6": "Pillar 3's specificity block; CAMPAIGN.md 2.2 SURVIVES and gains a GoA/GoB sibling from COUPLING.md",
    "E1.7": "one of Pillar 3's 23 enumerated arms; CAMPAIGN.md 2.2 SURVIVES, stays last (three-chain schema)",
    "E1.8": "Pillar 3's specificity block; CAMPAIGN.md 2.2 CHANGES — the mutants fit inside ct21, so it is a ladder arm now",
    "E1.9": "PLAN.md Pillar 3 promotes G17 from optional to BLOCKING; REGIMES 5 stages it as Stage 2b, 3,600 predictions, in no budget tier",
    "E2.1": "COMPUTED 2026-09-12 on the landed rows.tier3.v2.csv (analysis/block_c/received_2026_09_12/FIRST_LOOK.md): arm parse cross-validated against the g4 census on 800 of 800 cells, zero mismatches. CAMPAIGN.md 2.3 devalues it to the apo x ligand half (F-7: cognate is blanket alphas on 35 of 40)",
    "E2.2": "Pillar 4; 296 cells in g2_systems.csv. CAMPAIGN.md 2.3 rescopes it: F-7 kills the cheap re-export path, re-running clean is now the only option, panel 16 receptors / 15 clusters",
    "E2.3": "SPEC CONFLICT: CAMPAIGN.md 2.3 says DIES for this campaign (curation that does not exist), but D-2026-09-12-f relaxed C-1 and g2_systems.csv now carries 6 cells as G21(proposed). inputs/ wins over a narrative; Aditya must say which stands",
    "E2.4": "DECISIONS.md D-2026-09-12-h: runs at k=11 EXPLORATORY, frozen, gated by drule.py. 48 cells in g2_systems.csv. The bar stays at 12 and the arm is not claimed to have met it",
    "E3.1": "DECISIONS.md F-10 computes it: 7,486 primary rows, 38 receptors, 24 clusters, every interval spans 0.5 at both scopes. RESIDUAL: the ARM-conditional half and the whole-complex-vs-anchor re-aggregation finding are not done",
    "E3.2": "CATALOGUE.md E3.2 'Already computed' — +1.1 pp, 300 of 319 cells unanimous at seed grain; both grains derived in redo/build/matrix_power.py, recorded at RUN_MATRIX.md:547-548",
    "E3.3": "free on Block A's plddt_ga_alpha5; plddt_partner_chain_mean is already required by g1_recording_spec.tsv. CAMPAIGN.md 2.4 promotes it (F-5 gives it a second job at a depth-1 rung). NO PILLAR carries it",
    "E4.1": "PLAN.md Pillar 5 names the holdout. CAMPAIGN.md 2.5: it BECAME FREE — Protenix splits 16/14 and Chai 21/9 on the frozen 30, so three of four backbones stratify for zero predictions. RUN_MATRIX.md G8 still costs it at 7,200",
    "E4.2": "free (Block B rows + GPCRdb snapshot in hand). CAMPAIGN.md 2.5 promotes it to a HARD PREDECESSOR of the bulk control; PF-9 says the median split must be declared BEFORE dispatch. PLAN.md Pillar 3 dispatches the nulls and never mentions it",
    "E4.3": "free. CAMPAIGN.md 2.5 corrects the claim to 'no WILD-TYPE a5-CT of any length appears with a receptor' (OPSD's 4X1H holds an engineered 11-mer). PLAN.md Pillar 3 runs the 21-mer and does not make the argument",
    "E4.4": "NOTHING SETTLES IT. CAMPAIGN.md 2.5 says SURVIVES, still blocked on a candidate, and CATALOGUE.md records the blocker as 'Finding a candidate. The search was closed rather than answered.' That is a search nobody has re-run, not a decision anyone can take. RUN_MATRIX.md G13 costs it at 600 and no pillar carries it. Left at NEEDS_TRIAGE deliberately",
    "E5.1": "RUN_MATRIX.md 7.3 S0.6, cost `cheap`: needs one cognate structure per receptor (analysis/block_a/DATA_REQUESTS.md item 7), an ask that has never been sent. CAMPAIGN.md 2.6 gives it a second job — the fragment-restricted interface reference the ladder needs from 11 to 394 residues. PLAN.md has no mechanism pillar",
    "E5.2": "CAMPAIGN.md 2.6: DIES as an ask (F-7 makes s4_bw_decomposition.json describe an arm we cannot use), SURVIVES as our own analysis on our own rows. RESIDUAL: that analysis is free and unscheduled",
    "E5.3": "free on Block B's 50 samples per cell. CAMPAIGN.md 2.6 SURVIVES, unaffected. Staged at RUN_MATRIX.md 7.3 S0.7; no pillar",
    "E5.4": "free; the distance is continuous on every row. CAMPAIGN.md 2.6 PROMOTES it — engagement depth is the placement covariate the ladder needs, and junker2026peptidedesign shows a confidence metric will not catch a misplaced GPCR peptide. PLAN.md Pillar 3 does not require it",
    "E5.5": "free on A and B; the D half needs Block D's rows, which have not shipped. CAMPAIGN.md 2.6 SURVIVES at low priority, post-hoc unless pre-registered afresh",
    "E6.1": "PLAN.md Pillar 0 amends g1_recording_spec.tsv (47 columns), which is E6.1's contract enacted as an input. RESIDUAL: CAMPAIGN.md 2.7 says it GROWS (per-chain alignment sha + row count, n_chains, checkpoint_sha, wall_time_s, gpu_model, output_sha, attempt), and PF-14 records runs/README.md as drafted and unsent",
    "E6.2": "HALF DISCHARGED: rows.tier3.v2.csv landed 2026-09-12 (analysis/block_c/received_2026_09_12/, 40,801 rows x 101 columns) and NO DECISIONS.md entry records the landing. Block D's three rows.csv have NOT shipped. CAMPAIGN.md 2.7 demotes the pair from rank 1 (F-7)",
    "E6.4": "CAMPAIGN.md 2.7 SURVIVES, BLOCKING: free before dispatch, impossible after; Blocks A and B both failed it (1,898 distinct seed_outer across 380 Block A cells). g1_recording_spec.tsv carries `seed` for exactly this. PLAN.md names no pillar and Pillar 3 dispatches 2,039 systems",
    "E7.1": "free to write. CAMPAIGN.md 2.8 SURVIVES as Discussion. Being unable to name a good inactive-directing co-input is itself the result",
    "E7.2": "DECISIONS.md D-2026-09-12-d parks it as the acknowledged cost of the Class A scope: it needs a calibrated class B instrument, which is a second paper's work. CAMPAIGN.md 2.8 CHANGES — deferred, kept as an option, 'the sharpest venue biologically' (hilger2020gcgr: in class B the agonist alone produces no TM6 opening). RUN_MATRIX.md G15 is struck through",
    "E7.3": "CAMPAIGN.md 2.8 SURVIVES, corrected to 8 receptors (PANEL.md: q9wtk1_cavpo is lt4r1_human). RUN_MATRIX.md G14 costs it at 4,800. Ungradeable by construction, so it is a demonstration not evidence. No pillar",
    "E7.4": "free once one row-level ligand table exists — and one now does. CAMPAIGN.md 2.8 SURVIVES and CHANGES METHOD (run the injection on the pilot's own rows, not Block C's). PF-13 and RUN_MATRIX.md 4.3 both say it must precede the ligand arm. PLAN.md Pillar 4 says 'a null here is a finding' and does not schedule the injection that makes a null bounded",
    "E7.5": "DECISIONS.md D-2026-09-12-e prices it: (c) buys three panel receptors (cxcr3, mtr1a, mtr1b), not a tier, held until the measurement pass is authorised. CAMPAIGN.md 2.8: DIES as a uniform multiplier, SURVIVES as one Tier-4 replication arm at 2,880 predictions",
    "E7.6": "CAMPAIGN.md 2.8: the reagent is MISLABELLED — partners.fasta's arrestin_FL is beta-arrestin-1 P49407 residues 22-36, an N-domain beta-strand, not the finger loop (45-86), and arrestin_Ctail's bytes are not held. Sequences must be built from scratch and the circularity check must pass first. Costed inside RUN_MATRIX.md G3a/b; NOT enumerated in g1_systems.csv",
    "E8.1": "SPEC CONFLICT: MSA_SUBSAMPLING_REGIMES.md 5 schedules it as Stage 2 (5,440 marginal, gated on Stage 0's mapping test) and CAMPAIGN.md 2.9 says it SURVIVES and gains urgency — but PLAN.md Pillar 2 is apo and partnerless BY CONSTRUCTION and declines to bound the complex case in those words. Aditya's call",
    "E8.2": "MSA_SUBSAMPLING_REGIMES.md 5 Stage 3, 8,160 (+8,160 marginal over Stage 2), 'not premature... but it is third'. PLAN.md Pillar 2 is apo/monomer and Pillar 4 holds depth at default, so neither covers depth x ligand — and Pillar 2's own rationale (a monomer never touches per-chain MSA mapping) does not exclude a small-molecule ligand arm",
    "E8.3": "PLAN.md Pillar 0's Option Z depth measurement covers the realised-depth half, and g1_recording_spec.tsv already requires partner_msa_depth / receptor_msa_depth. RESIDUAL, and it is blocking: CAMPAIGN.md 2.9 says it GOT WORSE — subsample_msa.py:106-107 returns the input unchanged when len(entries) <= depth while the manifest records the nominal depth, so a '512' arm on a 300-row alignment is a 300-row arm labelled 512. PF-11's passthrough control and the OPSD x Boltz n=500 rerun are in no pillar",
    "E9.1": "free, and CATALOGUE.md E9.1 already recomputes it (91 of 160 Block B apo cells pinned at 0, 9 at 1, 24 informative). CAMPAIGN.md 2.10 adds a free re-read: under F-2 a cell pinned at 0 may be pinned by the pLDDT gate, not by geometry. Group 9 appears in NO spec except CATALOGUE.md and CAMPAIGN.md — not in RUN_MATRIX 7.1, not in PLAN.md",
    "E9.2": "CAMPAIGN.md 2.10 CHANGES — shrinks to the bistability bound; RUN_MATRIX.md 6.2 recommends 8,000 over 48,000 and costs it as G7, which carries NO E-id. Depends on E0.1 (Pillar 1, unauthorised) and on E9.1's free re-read. No pillar",
    "E9.3": "free, and an analysis convention rather than an experiment: never pool a rate across backbones. CAMPAIGN.md 2.10 SURVIVES, adopt as a convention. DECISIONS.md F-13 already enforces it for Class B. PLAN.md states no such convention",
}


# --------------------------------------------------------------------------
# The parsed half. Every parser FAILS on an empty result.
# --------------------------------------------------------------------------

def catalogue_entries(spec=None):
    """id -> {title, cost, depends, banner} parsed from the BODY, not a header."""
    text = _read(spec or SPEC, "CATALOGUE.md")
    parts = re.split(r"\n### (E\d+\.\d+)", text)
    out = {}
    for i in range(1, len(parts), 2):
        eid, body = parts[i], parts[i + 1]
        title = body.split("\n", 1)[0].strip(" —-")

        def field(name):
            m = re.search(r"\*\*%s\.\*\*\s*(.+?)(?:\n- \*\*|\n\n|\Z)" % name,
                          body, flags=re.S)
            return " ".join(m.group(1).split())[:300] if m else ""
        # The banner may sit anywhere in the entry, not only at its head --
        # matching only the start missed E0.5's CLOSED and E7.2's PARKED, which
        # are the two entries whose status is already decided.
        banner = ""
        m = re.search(r"^> \*\*(.+?)\*\*", body, flags=re.S | re.M)
        if m:
            banner = " ".join(m.group(1).split())[:160]
        out[eid] = {"title": title, "cost": field("Cost"),
                    "depends": field("Depends on"), "banner": banner}
    if len(out) < 40:
        raise SpecError(f"CATALOGUE.md yielded {len(out)} experiments, expected >=40")
    return out


def enumerated(inputs=None):
    """experiment id -> (file, n_systems, n_receptors, n_clusters)."""
    inputs = inputs or INPUTS
    out = {}
    for fn in ("g1_systems.csv", "g2_systems.csv"):
        p = os.path.join(inputs, fn)
        if not os.path.exists(p):
            raise SpecError(f"inputs/{fn} is absent — a missing systems file is a "
                            f"FAILURE, not a skip; it would silently zero a count")
        with open(p) as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            for eid in re.findall(EID, r.get("experiment", "")):
                d = out.setdefault(eid, {"file": fn, "n": 0, "rec": set(), "cl": set()})
                d["n"] += 1
                if r.get("receptor_slug"):
                    d["rec"].add(r["receptor_slug"])
                if r.get("receptor_cluster"):
                    d["cl"].add(r["receptor_cluster"])
    return out


def campaign_verdicts(spec=None):
    """eid -> (SURVIVES|CHANGES|DIES, the verdict line verbatim).

    CAMPAIGN.md section 2 is the only document that triages all 46 experiments,
    one table per group. The registry never read it, which is the whole reason
    30 rows sat at NEEDS_TRIAGE.
    """
    text = _read(spec or SPEC, "CAMPAIGN.md")
    sec = text.split("\n# 2. Every catalogued experiment", 1)
    if len(sec) < 2:
        raise SpecError("CAMPAIGN.md has no section 2 experiment triage")
    body = sec[1].split("\n# 3.", 1)[0]
    out = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        eids = re.findall(EID, cells[0])
        if not eids:
            continue
        verdict = cells[1]
        head = re.search(r"(SURVIVES|CHANGES|DIES)", verdict)
        for eid in eids:
            out[eid] = (head.group(1) if head else "",
                        " ".join(verdict.split())[:200])
    if len(out) < 40:
        raise SpecError(f"CAMPAIGN.md section 2 yielded {len(out)} verdicts, expected >=40")
    return out


def run_matrix_items(spec=None):
    """eid -> ['G8 (7,200)', ...] from RUN_MATRIX.md section 7.1's item table."""
    text = _read(spec or SPEC, "RUN_MATRIX.md")
    sec = text.split("\n## 7.1 Items", 1)
    if len(sec) < 2:
        raise SpecError("RUN_MATRIX.md has no section 7.1 item table")
    body = sec[1].split("\n## 7.2", 1)[0]
    out = collections.defaultdict(list)
    seen = 0
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7 or cells[0] in ("id", "---"):
            continue
        seen += 1
        item = re.sub(r"[*~`]", "", cells[0]).strip()
        preds = re.sub(r"[*~`]", "", cells[-1]).strip()
        for eid in sorted(set(re.findall(EID, cells[1]))):
            out[eid].append(f"{item} ({preds})")
    if seen < 20:
        raise SpecError(f"RUN_MATRIX.md 7.1 yielded {seen} item rows, expected >=20")
    return dict(out)


def stage0_items(spec=None):
    """eid -> 'S0.3 [free (them)]' from RUN_MATRIX.md section 7.3."""
    text = _read(spec or SPEC, "RUN_MATRIX.md")
    sec = text.split("\n## 7.3 Stage 0", 1)
    if len(sec) < 2:
        raise SpecError("RUN_MATRIX.md has no section 7.3 Stage 0 table")
    body = sec[1].split("\n## 7.4", 1)[0]
    out = {}
    rows = 0
    for line in body.splitlines():
        if not line.startswith("| S0."):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        rows += 1
        for eid in sorted(set(re.findall(EID, cells[1]))):
            out[eid] = f"{cells[0]} [{cells[2]}]"
    if rows < 5:
        raise SpecError(f"RUN_MATRIX.md 7.3 yielded {rows} stage-0 rows, expected >=5")
    return out


def preflights(spec=None):
    """eid -> 'PF-11' from CAMPAIGN.md section 8's pre-flight table."""
    text = _read(spec or SPEC, "CAMPAIGN.md")
    sec = text.split("\n# 8. The pre-flights", 1)
    if len(sec) < 2:
        raise SpecError("CAMPAIGN.md has no section 8 pre-flight table")
    body = sec[1].split("\n# 9.", 1)[0]
    out = {}
    rows = 0
    for line in body.splitlines():
        if not line.startswith("| **PF-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows += 1
        pf = re.sub(r"[*]", "", cells[0]).strip()
        for eid in sorted(set(re.findall(EID, cells[1]))):
            out[eid] = pf
    if rows < 10:
        raise SpecError(f"CAMPAIGN.md 8 yielded {rows} pre-flight rows, expected >=10")
    return out


def regime_stages(spec=None):
    """eid -> 'REGIMES Stage 2' from MSA_SUBSAMPLING_REGIMES.md's stage headings.

    Group 8 is the only group whose staging lives nowhere else: it carries no
    RUN_MATRIX 7.1 line item (the depth cube is costed as G5a/b with no E-id)
    and MSA_SUBSAMPLING.md never writes E8.1/E8.2/E8.3 at all.
    """
    text = _read(spec or SPEC, "MSA_SUBSAMPLING_REGIMES.md")
    out = {}
    for m in re.finditer(r"^### (Stage [0-9a-z]+)[^\n]*$", text, flags=re.M):
        for eid in sorted(set(re.findall(EID, m.group(0)))):
            out[eid] = f"REGIMES {m.group(1)}"
    if not out:
        raise SpecError("MSA_SUBSAMPLING_REGIMES.md yielded no staged experiments")
    return out


def _check_anchor(spec, eid, doc, anchor, table):
    """A basis that cites text a document does not contain is a FAILURE.

    This is the check that keeps the authored crosswalk honest. Proved by
    planting: --selftest deletes an anchor from a copy of spec/ and asserts the
    derivation refuses to run.
    """
    if anchor not in _read(spec, doc):
        raise SpecError(
            f"{table}[{eid}] cites {doc} for text that document does not contain: "
            f"{anchor!r}. Either the spec was rewritten and the basis is now false, "
            f"or the basis was wrong when written. Fix the crosswalk, do not relax "
            f"this check.")


# --------------------------------------------------------------------------

def derive(spec=None, inputs=None):
    spec = spec or SPEC
    cat = catalogue_entries(spec)
    enum = enumerated(inputs)
    matrix = run_matrix_items(spec)
    stage0 = stage0_items(spec)
    verdicts = campaign_verdicts(spec)
    pfs = preflights(spec)
    regimes = regime_stages(spec)

    for tbl, name in ((PILLAR_MAP, "PILLAR_MAP"), (DECIDED, "DECIDED")):
        for eid, row in tbl.items():
            _check_anchor(spec, eid, row[1], row[2], name)
    for tbl, name in ((FREE_ANCHOR, "FREE_ANCHOR"), (PI_ANCHOR, "PI_ANCHOR")):
        for eid, (doc, anchor) in tbl.items():
            _check_anchor(spec, eid, doc, anchor, name)

    missing = sorted(set(TRIAGE_WHY) - set(cat)) + sorted(set(cat) - set(TRIAGE_WHY))
    if missing:
        raise SpecError(f"TRIAGE_WHY and CATALOGUE.md disagree on which experiments "
                        f"exist: {missing}")

    rows = []
    for eid in sorted(cat, key=lambda e: (int(e[1:].split(".")[0]),
                                          int(e.split(".")[1]))):
        c = cat[eid]
        e = enum.get(eid)
        banner = c["banner"]

        # ---- status: can it run at all? Unchanged from the first registry.
        if banner.startswith("CLOSED"):
            status, why = "DROPPED", f"catalogue banner: {banner[:110]}"
        elif banner.startswith("PARKED"):
            status, why = "PARKED", f"catalogue banner: {banner[:110]}"
        elif e:
            status, why = "ENUMERATED", f"{e['n']} systems in {e['file']}"
        elif eid.startswith("E0."):
            status, why = ("BLOCKED",
                           "Group 0 is the instrument calibration and depends on "
                           "the MEASUREMENT PASS, which has never run and does not "
                           "start without Aditya's word")
        else:
            # Renamed from NEEDS_TRIAGE 2026-09-12. This column answers "is
            # there a systems row for it", and that is all it ever answered;
            # calling the answer NEEDS_TRIAGE made 30 rows read as undecided
            # while CAMPAIGN.md section 2 already carried a verdict for every
            # one. The triage now lives in its own column and means something.
            status, why = ("NOT_ENUMERATED",
                           "in the catalogue; no row in g1_systems.csv or "
                           "g2_systems.csv — see the triage column")

        # ---- pillar: which of PLAN.md's five discharges it, or none.
        pillar = PILLAR_MAP[eid][0] if eid in PILLAR_MAP else "none"

        # ---- triage: what the plan and the decisions do with it.
        # Order matters and is the argument: a decision already taken outranks
        # a pillar, a pillar outranks a stage, and nothing outranks silence.
        if eid in DECIDED:
            triage = "SUPERSEDED"
        elif eid in PI_ANCHOR:
            triage = "NEEDS_PI_DECISION"
        elif eid in PILLAR_MAP:
            triage = "COVERED_BY_PILLAR"
        elif eid in FREE_ANCHOR:
            triage = "FREE_UNSCHEDULED"
        else:
            triage = "NEEDS_TRIAGE"

        # ---- where it is staged, if anywhere. Parsed, never authored.
        staged = []
        if eid in matrix:
            staged += matrix[eid]
        if eid in stage0:
            staged.append(stage0[eid])
        if eid in pfs:
            staged.append(pfs[eid])
        if eid in regimes:
            staged.append(regimes[eid])

        verdict, verdict_line = verdicts.get(eid, ("", ""))

        basis = TRIAGE_WHY[eid]
        if eid in DECIDED:
            d = DECIDED[eid]
            basis = f"{d[0]} ({d[1]}): {d[3]}. {basis}"
        elif eid in PILLAR_MAP:
            basis = f"PLAN.md Pillar {pillar} — {PILLAR_MAP[eid][3]}. {basis}"

        rows.append({
            "experiment": eid,
            "group": eid.split(".")[0],
            "title": c["title"],
            "status": status,
            "status_basis": why,
            "pillar": pillar,
            "triage": triage,
            "triage_basis": basis[:700],
            "campaign_verdict": verdict,
            "campaign_verdict_line": verdict_line,
            "staged_as": "; ".join(staged),
            "systems_enumerated": "yes" if e else "no",
            "systems_file": e["file"] if e else "",
            "n_systems": e["n"] if e else 0,
            "n_receptors": len(e["rec"]) if e else 0,
            "n_clusters": len(e["cl"]) if e else 0,
            "named_in_run_matrix": "yes" if eid in matrix or eid in stage0 else "no",
            "cost_class": c["cost"][:120],
            "depends_on": c["depends"][:160],
        })
    return rows


def main():
    rows = derive()

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    st = collections.Counter(r["status"] for r in rows)
    tr = collections.Counter(r["triage"] for r in rows)
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} experiments)\n")
    print("  status — can it run?")
    for k, v in st.most_common():
        print(f"    {k:<18} {v}")
    print("\n  triage — what does the plan do with it?")
    for k, v in tr.most_common():
        print(f"    {k:<18} {v}")
    print("\n  pillar")
    for k, v in sorted(collections.Counter(r["pillar"] for r in rows).items()):
        print(f"    {k:<18} {v}")
    print()
    for g in sorted({r["group"] for r in rows}, key=lambda x: int(x[1:])):
        gr = [r for r in rows if r["group"] == g]
        s = collections.Counter(r["triage"] for r in gr)
        # a row serving "E1.8+E1.1" belongs to BOTH experiments, so summing
        # n_systems across a group double-counts it. Report the file's own size.
        files = {r["systems_file"] for r in gr if r["systems_file"]}
        n = 0
        for fn in files:
            with open(os.path.join(INPUTS, fn)) as fh:
                n += sum(1 for _ in fh) - 1
        print(f"  {g}: {len(gr):>2} experiments  {dict(s)}"
              + (f"  {n:,} systems" if n else ""))
    tri = [r["experiment"] for r in rows if r["triage"] == "NEEDS_TRIAGE"]
    print(f"\n  still NEEDS_TRIAGE ({len(tri)}): {', '.join(tri) or 'none'}")
    free = [r["experiment"] for r in rows if r["triage"] == "FREE_UNSCHEDULED"]
    print(f"  FREE and no pillar ({len(free)}): {', '.join(free)}")
    pi = [r["experiment"] for r in rows if r["triage"] == "NEEDS_PI_DECISION"]
    print(f"  needs Aditya ({len(pi)}): {', '.join(pi)}")
    return 0


# --------------------------------------------------------------------------
# Self-test. Every check below is proved by PLANTING the defect it catches and
# watching the derivation refuse. The harness copies the WHOLE spec tree, not
# its top level -- g0_preflight's harness copied only top-level files and every
# plant silently failed to apply for a day while the tally still printed clean.
# So each plant asserts the bytes actually changed before it asserts anything
# about the check.
# --------------------------------------------------------------------------

def _plant(tmp, doc, find, replace):
    p = os.path.join(tmp, doc)
    before = open(p).read()
    after = before.replace(find, replace, 1)
    if after == before:
        raise AssertionError(f"PLANT DID NOT APPLY in {doc}: {find!r} not found. "
                             f"The plant proves nothing and the harness must say so.")
    open(p, "w").write(after)
    return len(before) - len(after)


def _expect_fail(tmp, label, inputs=None):
    try:
        derive(spec=tmp, inputs=inputs)
    except SpecError as exc:
        print(f"  PASS  {label}\n          caught: {str(exc)[:150]}")
        return True
    print(f"  FAIL  {label} — derivation succeeded with the defect planted")
    return False


def selftest():
    src = SPEC
    plants = [
        ("PILLAR_MAP anchor deleted (E1.9's G17 promotion)",
         "PLAN.md", "G17 — partner MSA on vs off — is BLOCKING and belongs here", "xx"),
        ("DECIDED anchor deleted (D-2026-09-12-h runs the decoy arm)",
         "DECISIONS.md", "The decoy arm RUNS at k = 11, as an EXPLORATORY arm", "xx"),
        ("FREE_ANCHOR deleted (E7.4's free cost line)",
         "CATALOGUE.md", "`free` once one row-level ligand table exists", "xx"),
        ("PI_ANCHOR deleted (PLAN.md's Pillar 2 decline)",
         "PLAN.md", "do not spend predictions pretending to close it", "xx"),
        ("CAMPAIGN.md section 2 triage tables removed",
         "CAMPAIGN.md", "\n# 2. Every catalogued experiment", "\n# 2. REMOVED"),
        ("RUN_MATRIX.md section 7.1 item table removed",
         "RUN_MATRIX.md", "\n## 7.1 Items", "\n## 7.1 REMOVED"),
        ("RUN_MATRIX.md section 7.3 Stage 0 table removed",
         "RUN_MATRIX.md", "\n## 7.3 Stage 0", "\n## 7.3 REMOVED"),
        ("CAMPAIGN.md section 8 pre-flight table removed",
         "CAMPAIGN.md", "\n# 8. The pre-flights", "\n# 8. REMOVED"),
        ("MSA_SUBSAMPLING_REGIMES.md deleted entirely",
         "MSA_SUBSAMPLING_REGIMES.md", None, None),
        ("CATALOGUE.md loses an experiment heading (E9.3)",
         "CATALOGUE.md", "\n### E9.3 —", "\n#### E9.3 —"),
    ]

    print("run_registry self-test — each check proved by planting its defect\n")
    ok = 0
    # control: an unmodified copy must succeed, or every PASS below is vacuous
    with tempfile.TemporaryDirectory() as tmp:
        dst = os.path.join(tmp, "spec")
        shutil.copytree(src, dst)
        n_copied = sum(len(f) for _, _, f in os.walk(dst))
        if n_copied < 15:
            print(f"  FAIL  control — harness copied only {n_copied} files")
            return 1
        try:
            derive(spec=dst)
            print(f"  PASS  control: clean copy of spec/ ({n_copied} files) derives cleanly")
            ok += 1
        except SpecError as exc:
            print(f"  FAIL  control: clean copy raised {exc}")
            return 1

    for label, doc, find, repl in plants:
        with tempfile.TemporaryDirectory() as tmp:
            dst = os.path.join(tmp, "spec")
            shutil.copytree(src, dst)
            if find is None:
                os.remove(os.path.join(dst, doc))
            else:
                _plant(dst, doc, find, repl)
            ok += _expect_fail(dst, label)

    # A missing systems file must FAIL, not silently zero a count -- the
    # defect that let the registry ship 30 rows reading "0 systems" while
    # g2_systems.csv held 350. Planted by copying only one of the two.
    with tempfile.TemporaryDirectory() as tmp:
        half = os.path.join(tmp, "inputs")
        os.makedirs(half)
        shutil.copy(os.path.join(INPUTS, "g1_systems.csv"), half)
        if not os.path.exists(os.path.join(half, "g1_systems.csv")):
            raise AssertionError("PLANT DID NOT APPLY: g1_systems.csv was not copied")
        ok += _expect_fail(SPEC, "g2_systems.csv absent from inputs/", inputs=half)

    total = len(plants) + 2
    print(f"\n  {ok}/{total} checks proved")
    return 0 if ok == total else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
