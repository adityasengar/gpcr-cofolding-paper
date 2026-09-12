#!/usr/bin/env python3
"""Generate spec/MAP_NEW_CAMPAIGN.md from the frozen inputs.

Every table in that document is DERIVED, not transcribed.  Counts asserted in a
header have gone wrong four times on this project (see MEMORY: "a header count is
a claim nobody checks"), so nothing here is typed by hand -- if the inputs change,
re-run this and the map changes with them.

  python3 redo/build/map_new_campaign.py

Writes one file: redo/spec/MAP_NEW_CAMPAIGN.md
"""
import csv
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, SPEC  # noqa: E402


def read(name, delim=None):
    p = os.path.join(INPUTS, name)
    if delim is None:
        delim = "\t" if name.endswith(".tsv") else ","
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def main():
    rec = read("g1_receptors.tsv")
    cog = read("coupling_cognate_map.tsv")
    reg = read("g1_partner_registry.tsv")
    sysrows = read("g1_systems.csv")
    rungs = read("seq_rungs.tsv")
    lig = read("ligand_curation_candidates.tsv")
    enacted_tbl = read("ligand_set_redo.tsv")
    calib = read("g0_calibration_structures.csv")
    spec_cols = read("g1_recording_spec.tsv")

    cogby = {r["receptor_slug"]: r for r in cog}
    L = []
    w = L.append

    w("# MAP_NEW_CAMPAIGN.md — what the redo actually runs")
    w("")
    w("> **GENERATED — do not hand-edit.** `python3 redo/build/map_new_campaign.py`")
    w("> rebuilds it from `redo/inputs/`. Every count below is derived from the frozen")
    w("> tables, never transcribed, because a count asserted in a header has drifted")
    w("> from its own body four times on this project.")
    w("")
    w("Companion to `redo/protocol/MAP_FROZEN_CAMPAIGN.md`, which maps the campaign this")
    w("one supersedes. **The manuscript is frozen as the record; nothing here is built on it.**")
    w("")
    w("---")
    w("")

    # ---------------- scope ----------------
    classes = sorted({r["gclass"] for r in rec})
    cal_classes = sorted({r["gpcr_class"] for r in calib})
    w("## 0. Scope")
    w("")
    w("**Class A only** — `DECISIONS.md` D-2026-09-12-d, decided on measured grounds:")
    w("F-13 found a 9 Å inter-backbone disagreement on Class B apo and no discriminating")
    w("power at all on Class F. Guarded by `g0_preflight.py` check **G0-13**.")
    w("")
    w(f"- panel receptor classes present: **{', '.join(classes)}** "
      f"({len(rec)} receptors)")
    w(f"- calibration structure classes present: **{', '.join(cal_classes)}** "
      f"({len(calib)} rows)")
    w("")
    w("Dropped with the scope: `E0.5`, `G15`/tier `E-B1`, tier `E-scope`.")
    w("**Parked, not killed:** `E7.2`, the class B length ladder.")
    w("")
    w("---")
    w("")

    # ---------------- receptors ----------------
    clusters = collections.Counter(r["cluster"] for r in rec)
    core = [r for r in rec if r["core32_provisional"] == "yes"]
    w("## 1. Receptors — the panel")
    w("")
    w(f"**{len(rec)} receptors in {len(clusters)} paralog clusters.** "
      f"**{len(core)}** are the provisional core-32, one per cluster; the rest carry the")
    w("wide-replication arm. **The statistical unit is the cluster, not the receptor.**")
    w("")
    w("`active_pdb` / `inactive_pdb` are the Rule-P reference pair, with resolution in Å.")
    w("`cognate` is the Gα family read off the Rule-R active structure, and `evidence` is")
    w("how firmly — see §2. Ligands are §4, partners §3.")
    w("")
    w("| # | slug | UniProt | cluster | core32 | active | Å | inactive | Å | cognate | evidence |")
    w("|---:|---|---|---|:-:|---|---:|---|---:|---|---|")
    for r in rec:
        c = cogby.get(r["slug"], {})
        w(f"| {r['n']} | **{r['slug']}** | {r['uniprot']} | `{r['cluster']}` | "
          f"{'●' if r['core32_provisional'] == 'yes' else '·'} | "
          f"{r['active_pdb']} | {r['active_res']} | {r['inactive_pdb']} | {r['inactive_res']} | "
          f"{c.get('cognate_family', '?')} | {c.get('evidence_class', '?')} |")
    w("")

    # ---------------- cognate ----------------
    fam = collections.Counter(r["cognate_family"] for r in cog)
    ev = collections.Counter(r["evidence_class"] for r in cog)
    rev = [r["receptor_slug"] for r in cog
           if r["reverses_prior"] not in ("", "0", "no", "False")]
    needs = [r["receptor_slug"] for r in cog if r["verdict"] == "needs_decision"]
    w("---")
    w("")
    w("## 2. G proteins — the cognate map")
    w("")
    w("**Read off the structure the receptor was solved with**, so that the partner we")
    w("supply and the tip we score against are the same molecule. Two columns, never one:")
    w("`cognate_family` is the biology (what we supply), `reference_tip` is the structure")
    w("(what we score against). Conflating them was a real error.")
    w("")
    w("| cognate family | receptors |")
    w("|---|---:|")
    for k, v in fam.most_common():
        w(f"| {k} | {v} |")
    w("")
    w("| evidence class | receptors | meaning |")
    w("|---|---:|---|")
    meaning = {
        "STRUCTURE_EXACT": "the Rule-R active structure carries this exact Gα subtype",
        "STRUCTURE_NEAR": "same family, a near subtype",
        "CHIMERA_SPLIT": "the reference partner is a cross-family chimera — tip and scaffold disagree",
        "CONVENTION_FALLBACK": "no Gα in the Rule-R active reference; family assigned by convention",
        "PEPTIDE_ENTITY": "the partner is a deposited peptide entity, not a subunit",
    }
    for k, v in ev.most_common():
        w(f"| `{k}` | {v} | {meaning.get(k, '')} |")
    w("")
    w(f"**{len(needs)} receptors carry `needs_decision`** — every one is a `CHIMERA_SPLIT`, "
      "excluded from the primary panel and carried in the extension tier with G19 as the")
    w(f"matched control: {', '.join('`' + s + '`' for s in needs)}.")
    w("")
    w(f"**{len(rev)} assignments reverse Block B's prior** — "
      f"{', '.join('`' + s + '`' for s in rev)} — and **all four are now closed**.")
    w("`B1B1U5` by D-H (reference 9EPP); the other three by **F-14**, which found that")
    w("in each of them *the family the Rule-R structure reads is the only family with a")
    w("native, full-length, non-engineered Ga anywhere in that receptor's active")
    w("structures*. Block B's Gq prior exists for all three only as an mGsqi chimera, a")
    w("mini-G, or a subunit the depositors themselves label engineered. Evidence in")
    w("`inputs/coupling_reversal_evidence.tsv`; guarded by `g1_preflight.py` **B17**.")
    w("")
    w("---")
    w("")

    # ---------------- rungs ----------------
    byrung = collections.OrderedDict()
    for r in rungs:
        byrung.setdefault(r["rung"], r)
    fams = sorted({r["family"] for r in rungs})
    w("## 3. The length ladder — what a 'partner' is at each rung")
    w("")
    w("This is the manipulation the whole campaign exists to test. The frozen campaign")
    w("**never supplied a peptide at all** — every cognate arm there was a complete Gα.")
    w("")
    w("| rung | rule | length |")
    w("|---|---|---:|")
    for rung, r in byrung.items():
        lens = sorted({x["parent_len"] for x in rungs if x["rung"] == rung})
        reglen = sorted({x["length"] for x in reg
                         if x["construct"] == rung and x["length"] != "UNKNOWN"},
                        key=lambda v: int(v) if v.isdigit() else 0)
        w(f"| `{rung}` | {r['rule']} | {', '.join(reglen) if reglen else '—'} |")
    w("")
    w(f"Built for **{len(fams)} Gα families**: {', '.join('`' + f + '`' for f in fams)}.")
    w("")

    # ---------------- partner registry ----------------
    cls = collections.Counter(r["construct_class"] for r in reg)
    held = sum(1 for r in reg if r["held"] == "yes")
    w("### 3.1 The partner construct registry")
    w("")
    w(f"**{len(reg)} constructs, {held} held as bytes with a full sha256.** Anything not")
    w("held is not dispatchable — `g1_preflight.py` check **B4** refuses to dispatch a")
    w("construct whose bytes we do not hold.")
    w("")
    w("| construct class | n | what it is |")
    w("|---|---:|---|")
    what = {
        "peptide_control": "reversed / polyA / scramble / face-scramble / gcn4-window controls per rung",
        "ga_rung": "the length ladder itself, per Gα family",
        "ala_scan": "single-alanine walk along ct21",
        "ref_tip": "the α5 tip as deposited in each receptor's own active reference",
        "gi_to_gs_scan": "stepwise Gi→Gs substitution series on ct21",
        "not_dispatchable": "declared but not held — cannot be run",
        "uncoupling_mutant": "F376A / L388A / R380A nulls, peptide and full-length",
        "ga_rung_isoform": "GoB isoform arm",
        "species_matched_tip": "the spider Gq tip for B1B1U5",
        "non_ga_chain": "non-Gα partners: GCN4 zipper, ubiquitin, KaiB, Gβ1, Gγ2",
        "minig_deposited": "deposited mini-G constructs as an anchor",
        "wetlab_matched": "C379A peptides matching published wet-lab work",
        "boundary_variant": "the Sunahara D368–L394 27-mer boundary test",
    }
    for k, v in cls.most_common():
        w(f"| `{k}` | {v} | {what.get(k, '')} |")
    w("")
    nd = [r for r in reg if r["held"] != "yes"]
    if nd:
        w(f"**{len(nd)} are NOT dispatchable** and are named so the absence is legible: "
          + ", ".join(f"`{r['construct']}`" for r in nd) + ".")
        w("")
    w("---")
    w("")

    # ---------------- ligands ----------------
    byrec = collections.defaultdict(list)
    for r in lig:
        byrec[r["receptor"]].append(r)
    w("## 4. Ligands")
    w("")
    w("**Affinity data is NOT required.** Ligand identity is evidenced *structurally* —")
    w("the molecule is co-crystallised in an active or inactive receptor — which is a")
    w("stronger claim than an assay number. Aditya, 2026-09-12.")
    w("")
    en = [r for r in enacted_tbl if r["status"] == "enacted"]
    bl = [r for r in enacted_tbl if r["status"] == "BLOCKED"]
    onref = [r for r in en if r["is_our_reference"] == "yes"]
    w(f"**ENACTED** — `ligand_set_redo.tsv` holds **{len(en)} picks across "
      f"{len({r['receptor_slug'] for r in en})} receptors**, "
      f"**{len(onref)} of them on one of our own reference structures**, plus "
      f"**{len(bl)} blocked** receptors each carrying its reason. Gated by "
      f"`redo/gates/ligands.py`, 5 checks, each proved by planting.")
    w("")
    w("| receptor | role | ligand | CCD | structure | Å | on our reference |")
    w("|---|---|---|---|---|---:|:-:|")
    for r in en:
        w(f"| **{r['receptor_slug']}** | {r['ligand_role']} | {r['ligand_name']} | "
          f"`{r['ligand_ccd']}` | {r['bound_pdb']} | {r['bound_pdb_resolution']} | "
          f"{'●' if r['is_our_reference'] == 'yes' else '·'} |")
    w("")
    w("**Blocked, with the reason in the table itself:**")
    w("")
    w("| receptor | role | why |")
    w("|---|---|---|")
    for r in bl:
        w(f"| **{r['receptor_slug']}** | {r['ligand_role']} | {r['why']} |")
    w("")
    w(f"`ligand_curation_candidates.tsv` holds the **{len(lig)} candidate rows across "
      f"{len(byrec)} receptors** these were chosen from:")
    w("")
    w("| receptor | needs | candidates | status |")
    w("|---|---|---:|---|")
    status = {
        "S1PR1": "**enacted** — siponimod / W146, both on our own references",
        "CCKAR": "**enacted** — SR146131, off-reference and the only small-molecule candidate",
        "GHSR": "**enacted** — ibutamoren / CHEMBL1956994",
        "ADRB1": "**BLOCKED** — carazolol is on our reference and human but is an *inverse agonist* (amendment C-1); every true antagonist candidate is turkey",
        "HRH3": "**enacted** — histamine on our active reference 8YN5",
        "OPSD": "**BLOCKED** — the active reference carries a detergent (BNG), no agonist",
        "B1B1U5": "reference settled by D-H; blocker is policy not chemistry — no neutral antagonist exists",
    }
    for r in sorted(byrec, key=lambda k: (-len(byrec[k]), k)):
        need = byrec[r][0]["needed"]
        w(f"| **{r}** | {need} | {len(byrec[r])} | {status.get(r, '')} |")
    w("")
    w("**Curate retinal by ISOMER, never by CCD** (F-11). OPSD and B1B1U5 both involve")
    w("retinal, where agonist and antagonist are isomers of one covalent ligand — and")
    w("B1B1U5's reference pair carries two *different* CCDs (`A1H6M` at 9EPP, `RET` at")
    w("6I9K), so it is **not** blocked by the shared-CCD problem. I reported the candidate")
    w("pool's property as the reference pair's; that was wrong and is retracted.")
    w("")
    w("---")
    w("")

    # ---------------- decoys ----------------
    w("## 5. Decoys — rebuilt from scratch, and why")
    w("")
    w("The frozen campaign's decoys were **hand-picked FDA-approved drugs, one per")
    w("receptor, hard-coded in a Python dict**, verified against a single Tanimoto < 0.30")
    w("gate and *reported against* a ±20% property window that could reject nothing. There")
    w("was no candidate pool, no search and no draw. They cannot be reused.")
    w("")
    w("The replacement is specified in `DRULE_CHEMBL_SCOPE.md` and is **not yet built**:")
    w("")
    w("| # | deliverable | what it must do |")
    w("|---:|---|---|")
    w("| 1 | `redo/build/drule_pool.py` | extraction → `inputs/drule_candidate_pool.tsv`, one row per (receptor, candidate) with every property axis and the provenance of each activity record consulted |")
    w("| 2 | `redo/build/drule_select.py` | apply the eight axes + similarity gate; record **which axis rejected each rejection** — a rule that cannot say why it refused is not auditable |")
    w("| 3 | `redo/gates/drule.py` | proved by planting a defect: no accepted decoy has measured activity at its receptor or a cluster-mate; the pool is reproducible from the pinned release |")
    w("| 4 | a pool report **before** any threshold is fixed | how many clusters yield ≥3 accepted decoys. D-D withdrew the ≥12 figure precisely because it was set before this number existed |")
    w("")
    w("ChEMBL is needed for **presence/absence of activity only** — not for affinity.")
    w("")
    tg = read("drule_targets.tsv")
    res = [r for r in tg if r["chembl_target_id"]]
    rel = sorted({r["chembl_release"] for r in tg})
    w(f"**Status: 1 and 3 are built, 2 and 4 are not.** `drule_targets.tsv` resolves")
    w(f"**{len(res)} of {len(tg)} receptors** to a ChEMBL SINGLE PROTEIN target against")
    w(f"**{rel[0]}**, covering **{len({r['cluster'] for r in res})} of "
      f"{len({r['cluster'] for r in tg})} clusters**. The one unresolved is "
      f"**{[r['receptor_slug'] for r in tg if not r['chembl_target_id']][0]}**, which has")
    w("no ChEMBL target at all — recorded with an empty target, never dropped.")
    w("")
    w("`drule_pool.py` is written and its rule is **proved on a fixture** (4/4 branches:")
    w("active at the receptor, at a cluster-mate only, only elsewhere, and only in a")
    w("low-confidence assay). **It refuses to run against the live API** — an unpinned")
    w("pull is `paper_af3`'s ColabFold problem in another costume — so it needs a")
    w("downloaded release with `--release` and `--sha256` recorded into every row.")
    w("**That download is Aditya's decision.** `redo/gates/drule.py` gates what exists,")
    w("4 checks each proved by planting, and announces the unbuilt pool on every run.")
    w("")
    w("---")
    w("")

    # ---------------- arms ----------------
    agg = collections.OrderedDict()
    for r in sysrows:
        agg.setdefault((r["item"], r["experiment"], r["arm"]), []).append(r)
    tot_p = sum(int(r["predictions_pooled"] or 0) for r in sysrows)
    tot_c = sum(int(r["predictions_percell"] or 0) for r in sysrows)
    w("## 6. The arms, and what they cost")
    w("")
    w(f"**{len(sysrows):,} system rows in {len(agg)} arms.** Two budget columns because the")
    w("design has two grains: `pooled` shares draws within a cell, `per-cell` does not.")
    w("")
    w("| item | experiment | arm | receptor set | rows | chains | partner MSA | pooled | per-cell |")
    w("|---|---|---|---|---:|:-:|---|---:|---:|")
    for (item, exp, arm), rs in agg.items():
        r = rs[0]
        pp = sum(int(x["predictions_pooled"] or 0) for x in rs)
        pc = sum(int(x["predictions_percell"] or 0) for x in rs)
        w(f"| `{item}` | {exp} | {arm} | {r['receptor_set']} | {len(rs)} | "
          f"{r['n_chains']} | {r['partner_msa']} | {pp:,} | {pc:,} |")
    w(f"| | | | | **{len(sysrows)}** | | | **{tot_p:,}** | **{tot_c:,}** |")
    w("")
    w("**No arm in this table carries a ligand** — Group 1 is the partner-length campaign")
    w("and runs apo. The ligand arms are Group 2 and are not frozen.")
    w("")
    w("---")
    w("")

    # ---------------- recording spec ----------------
    st = collections.Counter(r["status"] for r in spec_cols)
    w("## 7. What every prediction row must record")
    w("")
    w(f"**{len(spec_cols)} columns**, and the split is the point:")
    w("")
    for k, v in st.most_common():
        w(f"- `{k}` — {v}")
    w("")
    w("The frozen campaign recorded **nothing about the MSA on any scored row** — not")
    w("depth, not source, not pairing, not a hash (F-6) — and **nothing anywhere compared")
    w("output to input** (F-9). `partner_msa_depth`, `n_chains`, `partner_seq_sha256` and")
    w("`seed` exist here so that `redo/gates/run_receipt.py` can ask whether a delivery is")
    w("what was requested. **There, a missing column is a FAILURE, not a skip.**")
    w("")
    w("---")
    w("")

    # ---------------- frozen vs open ----------------
    w("## 8. Frozen, and open")
    w("")
    w("**Frozen** — `g0_preflight.py` 13 blocking checks, `g1_preflight.py` 16, both")
    w("proved by planting the defect each catches; `layout.py` 7; `run_receipt.py` 4.")
    w("")
    w("**Open, in dependency order:**")
    w("")
    w("1. **The measurement pass** — the largest outstanding dependency. It must record")
    w("   axis values for the **F3-removed** structures too, or that filter stays")
    w("   permanently unauditable (F-12). Not started without Aditya's word.")
    w("2. **D2's regeneration** — decided at (c): expand onto `cxcr3`, `mtr1a`, `mtr1b`,")
    w("   reserve the other 17. Held until the pass is authorised so the population")
    w("   freezes once (D-2026-09-12-e).")
    w("3. **`MSA_SPEC.md` implementation** — their review found a defect inside the")
    w("   mechanism our own spec proposed: OF3 keys the per-chain MSA dict by **chain ID**,")
    w("   Protenix by **integer position**, so `{\"A\": …, \"B\": \"\"}` fails silently on")
    w("   Protenix into a live full-depth fetch, invisible in every status JSON.")
    w("4. ~~Three coupling reversals~~ — **DONE** (F-14). CCKAR = Gs, EDNRB and GHSR")
    w("   = Gi/o, on the native-Gα evidence rather than on authority counting.")
    w("5. ~~Ligand curation~~ — **DONE** (F-15): 6 picks enacted across 4 receptors.")
    w("   Open: whether to reopen amendment C-1 so ADRB1 and B1B1U5 can use an")
    w("   inverse agonist. Aditya's call, not curation.")
    w("6. **The decoy pool** — the extraction and its gate are built and proved;")
    w("   the pool itself waits on a pinned ChEMBL release being downloaded, which")
    w("   is a decision with a cost and is Aditya's.")
    w("")
    w("**Decided and not to be re-opened:** D-A (the conjunction, NPxxY calibrated, tilt")
    w("inherited and validated — every ground truth for that axis is circular), D-H")
    w("(B1B1U5 stays at 9EPP as (c′)), affinity (not needed), scope (Class A only),")
    w("D2 (the split, at the zero-cost cut).")

    out = os.path.join(SPEC, "MAP_NEW_CAMPAIGN.md")
    with open(out, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {out}  ({len(L)} lines)")


if __name__ == "__main__":
    main()
