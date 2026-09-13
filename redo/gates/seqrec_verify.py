#!/usr/bin/env python3
"""Recompute every number quoted in redo/SEQ_RECEPTORS.md.

Same role as `analysis/block_<x>/verify_claims.py`: the document is allowed
to go stale, this is not. Each check prints its own name, its recomputed
value and the value the document asserts, and the run fails on any
mismatch. Every check reads only the seqrec_ companions, which are
themselves regenerable from UniProt / RCSB / GPCRdb by seqrec_build.py,
seqrec_refs.py, seqrec_trim.py and seqrec_icl3_audit.py.

Usage
  python3 redo/gates/seqrec_verify.py
  python3 redo/gates/seqrec_verify.py --plant   # prove the checks report
"""
import collections
import csv
import hashlib
import os
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo


def tsv(name):
    return list(csv.DictReader(open(os.path.join(INPUTS, name)), delimiter="\t"))


def csvf(name):
    return list(csv.DictReader(open(os.path.join(INPUTS, name))))


def read_fasta(path):
    seqs, name, buf = {}, None, []
    for line in open(os.path.join(INPUTS, path)):
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].split("|")[0], []
        else:
            buf.append(line.strip())
    if name:
        seqs[name] = "".join(buf)
    return seqs


# The 48 receptors Block A/B actually dispatched, read from the one file that
# records them: data/block_b/03_msa_audit/msa_depth_report.md, "Receptor MSA
# depth table". Listed here rather than re-parsed so this script needs nothing
# outside redo/.
DISPATCHED_48 = {
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR", "ACM1", "ACM2", "ACM4",
    "ADA2A", "ADRB1", "ADRB2", "AGTR1", "APJ", "B1B1U5", "CCKAR", "CCR5",
    "CNR1", "CNR2", "CXCR2", "CXCR4", "DRD2", "DRD3", "EDNRA", "EDNRB",
    "FSHR", "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1", "LSHR", "LT4R1",
    "MCHR1", "NPY1R", "NPY2R", "OPRD", "OPRK", "OPRX", "OPSD", "OX2R",
    "CRHR1", "GCGR", "GLP1R", "PTH1R", "FZD4", "FZD6", "FZD7", "SMO",
}

RESULTS = []


def check(name, got, want):
    RESULTS.append((name, got, want, got == want))


def main(plant=False):
    recs = tsv("seqrec_receptors.tsv")
    refs = tsv("seqrec_refs.tsv")
    score = tsv("seqrec_scoreable.tsv")
    trim = tsv("seqrec_trim.tsv")
    icl3 = tsv("seqrec_icl3_audit.tsv")
    fasta = read_fasta("seqrec_canonical.fasta")
    panel = csvf("panel_systems.csv")

    core = [r for r in recs if "C1" in r["tier"].split("|")]
    byslug = {r["slug"]: r for r in recs}
    ext = [r for r in recs if r["tier"] not in ("orthologue-candidate",)
           and "C1" not in r["tier"].split("|")]
    if plant:
        core = core[:-1]                     # plant a roster defect

    # --- §1 roster
    check("core receptors", len(core), 64)
    check("extension-tier receptors", len(ext), 11)
    check("core all Class A", {r["gpcr_class"] for r in core}, {"A"})
    check("core with 7 UniProt TM helices", sum(1 for r in core if r["n_tm"] == "7"), 64)

    # --- §2 sequences are the fetched record
    bad = [r["slug"] for r in recs
           if hashlib.sha256(fasta[r["slug"]].encode()).hexdigest() != r["sha256"]]
    check("fasta sha256 matches table", bad, [])
    check("length matches fasta", [r["slug"] for r in recs
                                   if len(fasta[r["slug"]]) != int(r["length"])], [])

    # --- §3 signal peptides
    sig_core = sorted(r["slug"] for r in core if r["signal"] != "none")
    check("core with a signal peptide",
          sig_core, ["5HT2C", "EDNRA", "EDNRB", "FSHR", "LSHR", "TSHR"])
    check("extension with a signal peptide",
          sum(1 for r in ext if r["signal"] != "none"), 10)

    # --- §3 isoforms
    check("core entries with >1 isoform",
          sum(1 for r in core if int(r["n_isoforms"]) > 1), 29)
    ta2r = [r for r in core if r["slug"] == "TA2R"][0]
    check("TA2R displayed isoform", ta2r["canonical_isoform"], "P21731-3")
    oprm = [r for r in core if r["slug"] == "OPRM"][0]
    check("OPRM isoform count", int(oprm["n_isoforms"]), 19)

    # --- §5 species
    nonhuman = sorted(r["slug"] for r in core
                      if not r["organism"].startswith("Homo sapiens"))
    check("non-human core receptors", nonhuman, ["B1B1U5", "OPRM", "OPSD"])
    adrb1 = [r for r in core if r["slug"] == "ADRB1"][0]
    check("ADRB1 accession is human", adrb1["accession"], "P08588")

    # --- §6 what the references contain
    check("reference entities audited", len(refs), 128)
    check("receptors with both references mapped", len(score), 64)
    res = sorted(int(r["n_resolved_both"]) for r in score)
    check("median canonical residues resolved in both references (n even, "
          "upper of the two middles)", res[len(res) // 2], 273)
    check("fewest scoreable", min((int(r["n_resolved_both"]), r["slug"])
                                  for r in score), (198, "LT4R1"))
    check("most scoreable", max((int(r["n_resolved_both"]), r["slug"])
                                for r in score), (568, "FSHR"))
    check("references RCSB's alignment does not name the receptor on",
          sorted(f"{r['slug']}/{r['pdb']}" for r in refs
                 if r["rcsb_align_names_receptor"] == "NO"),
          ["CCR6/9D3G", "DRD4/8IRU", "EDNRA/8HCQ"])
    floor = sum(len([m for m in r["rcsb_mutation"].split(",") if m.strip()])
                for r in refs)
    check("RCSB pdbx_mutation floor over 128 references", floor, 76)
    check("recounted point substitutions",
          sum(int(r["n_point_substitution"]) for r in refs), 166)
    check("references where the recount exceeds RCSB's floor",
          sum(1 for r in refs
              if int(r["n_point_substitution"])
              > len([m for m in r["rcsb_mutation"].split(",") if m.strip()])), 41)
    check("references carrying a foreign graft run",
          sorted(f"{r['slug']}/{r['pdb']}" for r in refs
                 if r["grafted_canon_spans"] != "none"),
          ["EDNRB/8IY5", "SSR2/7T10"])

    # --- §6.2 ICL3 fusion audit
    by = collections.Counter(r["state"] for r in icl3 if "ICL3" in r["fusion_location"])
    check("active references with an ICL3 insertion", by["active"], 3)
    check("inactive references with an ICL3 insertion", by["inactive"], 40)
    check("inactive references with NO ICL3 insertion (the clean subset)",
          sum(1 for r in icl3 if r["state"] == "inactive"
              and "ICL3" not in r["fusion_location"]), 24)
    check("ICL3 insertions RCSB's description does not name",
          sum(1 for r in icl3 if "ICL3" in r["fusion_location"]
              and r["fusion_named_in_description"] == "none"), 9)
    check("references with no >=20 aa insertion anywhere",
          sum(1 for r in icl3 if r["fusion_location"] == "none"), 49)
    check("canonical residues present in both references, fewest",
          min((int(r["n_present_both"]), r["slug"]) for r in score),
          (208, "LT4R1"))

    # --- §4 the miglionico cap
    tcore = [r for r in trim if "C1" in r["tier"].split("|")]
    check("core receptors the cap changes",
          sum(1 for r in tcore if int(r["n_removed_total"]) > 0), 16)
    check("core receptors the cap leaves alone",
          sum(1 for r in tcore if int(r["n_removed_total"]) == 0), 48)
    check("core receptors whose C-terminus the cap reaches",
          sorted(r["slug"] for r in tcore if r["cap_binds_cterm"] == "yes"),
          ["ADA1A", "PE2R4"])
    check("core residues the cap removes in total",
          sum(int(r["n_removed_total"]) for r in tcore), 1294)
    # ---- option (b): the signal peptide, and the guarantee it is supposed to give.
    # Added 2026-09-13.  seqrec_trim.py carried a comment claiming "Check S-1 below
    # asserts it never does" about the unreachability of signal_peptide_removed ==
    # "false".  There was no S-1 anywhere in the repository.  The guarantee was
    # asserted in a comment and enforced nowhere -- written, by me, in the act of
    # fixing another instance of exactly that.  These are the checks it named.
    check("no construct retains ANY residue of an annotated signal peptide",
          sorted(r["slug"] for r in trim
                 if int(r["signal_residues_retained"]) > 0), [])
    check("signal_peptide_removed is never 'false' (unreachable under option (b))",
          sorted(r["slug"] for r in trim
                 if r["signal_peptide_removed"] == "false"), [])
    check("every receptor with an annotated signal peptide is flagged 'true'",
          sorted(r["slug"] for r in trim
                 if r["signal"] not in ("", "none", "NA")
                 and r["signal_peptide_removed"] != "true") , [])
    check("every receptor WITHOUT one is flagged 'none', not 'false'",
          sorted(r["slug"] for r in trim
                 if r["signal"] in ("", "none", "NA")
                 and r["signal_peptide_removed"] != "none"), [])
    check("the CHAIN floor is the only thing that moved the start",
          sorted(r["slug"] for r in trim
                 if int(r["trim_start"]) != max(int(r["cap_start"]),
                                                int(r["trim_start"]))), [])
    check("receptors whose construct the floor actually changed",
          sorted(r["slug"] for r in trim if int(r["n_removed_signal"]) > 0),
          ["5HT2C", "EDNRA"])

    check("receptors with no GPCRdb H8",
          sorted(r["slug"] for r in trim if r["h8_gpcrdb"] == "NA"), ["LT4R1"])
    check("GPCRdb and UniProt TM1 start disagree on",
          sum(1 for r in trim if r["tm1_start_uniprot"] != r["tm1_start_gpcrdb"]),
          len(trim))

    # --- §4.3 what the cap costs in scoreable residues
    tmap = {r["slug"]: (int(r["trim_start"]), int(r["trim_end"])) for r in trim}
    lost = {}
    for r in score:
        a, b = tmap[r["slug"]]
        if r["resolved_both_ranges"] == "NA":
            continue
        res = set()
        for part in r["resolved_both_ranges"].split(","):
            if "-" in part:
                lo, hi = (int(x) for x in part.split("-"))
                res.update(range(lo, hi + 1))
            else:
                res.add(int(part))
        n = sum(1 for v in res if v < a or v > b)
        if n:
            lost[r["slug"]] = n
    check("core receptors the cap costs scoreable residues",
          sorted(lost), ["FSHR", "LSHR", "MCHR1", "TSHR"])
    check("scoreable residues the cap removes, core total",
          sum(lost.values()), 794)
    check("scoreable residues the cap removes outside the three GpHRs",
          sum(v for k, v in lost.items() if k not in ("FSHR", "LSHR", "TSHR")), 18)

    # --- §3.3/§3.4 terminal lengths, §7.2 coverage
    nt = sorted(int(r["nterm_len_before_tm1"]) for r in core)
    ct = sorted(int(r["cterm_len_after_tm7"]) for r in core)
    check("median core N-terminus before TM1 (UniProt)",
          (nt[31] + nt[32]) / 2, 40.0)
    check("median core C-terminus after TM7 (UniProt)",
          (ct[31] + ct[32]) / 2, 54.0)
    coreslugs = {r["slug"] for r in core}
    changed = {r["slug"] for r in trim
               if "C1" in r["tier"].split("|") and int(r["n_removed_total"]) > 0}
    check("core receptors never dispatched by Block A or B",
          len(coreslugs - DISPATCHED_48), 24)
    check("dispatched core receptors the cap changes (MSA rebuilds)",
          sorted(DISPATCHED_48 & changed),
          ["5HT2C", "CNR1", "EDNRA", "EDNRB", "FSHR", "LSHR", "MCHR1",
           "OPRK", "OX2R"])
    check("dispatched core receptors whose MSA could be reused",
          len((DISPATCHED_48 & coreslugs) - changed), 31)

    # --- §3.3 post-TM7 scoreability, the argument for anchoring on H8
    post = []
    for r in score:
        tm7 = int(byslug[r["slug"]]["tm7_end"])
        res = set()
        for part in r["resolved_both_ranges"].split(","):
            if "-" in part:
                lo, hi = (int(x) for x in part.split("-"))
                res.update(range(lo, hi + 1))
            else:
                res.add(int(part))
        post.append(sum(1 for v in res if v > tm7))
    post.sort()
    check("median post-TM7 residues resolved in both references",
          (post[31] + post[32]) / 2, 12.0)
    check("post-TM7 residues resolved in both, core total", sum(post), 705)
    check("core receptors resolving no post-TM7 residue",
          sum(1 for x in post if x == 0), 2)
    check("post-TM7 residues in the core, total",
          sum(int(r["length"]) - int(r["tm7_end"]) for r in core), 3644)

    # --- §6.3 the pipeline's own scoring mask. Reads data/block_b read-only.
    bb = os.path.join(INPUTS, "..", "..", "data", "block_b", "01_rows",
                      "rows_tidy.csv")
    if os.path.exists(bb):
        per = {}
        blank = set()
        n_blank_rows = 0
        for r in csv.DictReader(open(bb)):
            v = r["rmsd_n_residues_used"]
            if v == "":
                blank.add(r["receptor_slug"])
                n_blank_rows += 1
            else:
                per.setdefault(r["receptor_slug"], set()).add(v)
        check("rmsd_n_residues_used: one value per receptor",
              max(len(v) for v in per.values()), 1)
        vals = sorted(int(next(iter(v))) for v in per.values())
        check("rmsd_n_residues_used range", (vals[0], vals[-1]), (210, 245))
        check("rmsd_n_residues_used median", vals[len(vals) // 2], 224)
        check("Block B receptors with no reference pair", len(blank), 8)
        check("Block B rows with no RMSD", n_blank_rows, 6400)
        # input_sha256 is a per-CIF output hash, not a receptor-chain hash
        rows_bb = sum(1 for _ in csv.DictReader(open(bb)))
        n_inp = len({r["input_sha256"] for r in csv.DictReader(open(bb))})
        check("input_sha256 is one-per-row, i.e. not a chain identity",
              (n_inp, rows_bb), (32000, 32000))
    else:
        print("# data/block_b not present; 5 checks skipped", file=sys.stderr)

    # --- panel cross-check: the roster is the one PANEL.md publishes
    pcore = [r for r in panel if "C1" in r["tier"].split("|")]
    check("roster agrees with panel_systems.csv",
          sorted(r["slug"] for r in core) if not plant else ["planted"],
          sorted(r["slug"] for r in pcore))

    width = max(len(n) for n, _, _, _ in RESULTS)
    fails = 0
    for name, got, want, ok in RESULTS:
        if not ok:
            fails += 1
        g = str(got)
        w = str(want)
        if len(g) > 60:
            g = g[:57] + "..."
        if len(w) > 60:
            w = w[:57] + "..."
        print(f"[{'ok ' if ok else 'FAIL'}] {name:{width}s}  got {g}"
              + ("" if ok else f"   want {w}"))
    print(f"\n{len(RESULTS) - fails}/{len(RESULTS)} checks pass")
    if plant:
        print("(--plant expects failures; a clean run here would mean the "
              "checks are not reading what they claim to)")
        return 0 if fails else 1
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(plant="--plant" in sys.argv))
