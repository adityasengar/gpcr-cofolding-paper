#!/usr/bin/env python3
"""Group 0 build step — measure the two activation axes on a deposited structure.

WHAT THIS IS.  `redo/spec/PANEL.md` §9.1 found that the NPxxY axis has never
been computed for a single off-panel structure: in
`data/block_b/09_references/reference_set.blockb_pinned.csv` the tilt axis is
populated on all 162 rows and the NPxxY axis on 64, and all 69 off-panel rows
carry tilt and zero carry NPxxY.  E0.1 therefore cannot be run — the off-panel
measurements have to be MADE from coordinates first.  This file is that build
step, and `GROUP0_SYSTEMS.md` §3 is its specification.

WHAT IT MEASURES, and nothing else:

  d_npxxy_oh   = |Y5.58:OH - Y7.53:OH|    Ballesteros-Weinstein labels, OH atoms
  d_tilt       = |2x46:CA  - 6x37:CA|     GPCRdb generic numbers, CA atoms

WHY TWO DIFFERENT NUMBERING SYSTEMS, and why that is not a detail.  The shipped
column names say it: `d_npxxy_y558_y753_oh` uses dotted BW labels,
`d_gpcrdb_tm6_tilt_246_637_ca` says `gpcrdb` and uses `x` notation.  GPCRdb's
`display_generic_number` carries both -- "6.37x37" splits into BW "6.37" and
generic "6x37" -- and in helices with a bulge THE TWO DIVERGE.  Matching the
tilt anchors on the BW field would silently land on a different residue in
exactly the receptors where TM6 geometry is most unusual.  So:

  NPxxY anchors are looked up on the `bw` field   (5.58, 7.53)
  tilt anchors are looked up on the `generic` field (2x46, 6x37)

`~/.ntfy-bridge/inbox/bw_numbering.d9c646af.py` ships `lookup_bw` and no generic
equivalent; `lookup_generic` below is the missing sibling and is the only line of
convention this file adds to the pipeline's.

NUMBERING SOURCE.  GPCRdb `residues/extended/<entry>` is the only sanctioned BW
source (`bw_numbering.py` docstring, "THIS IS THE ONLY SANCTIONED BW SOURCE").
It returns UniProt sequence positions.  Deposited structures number by
`auth_seq_id`, which need not equal the UniProt position, so SIFTS
`uniprot_segments` supplies the per-chain offset.  No hardcoded anchor table, no
canonical offset, no sequence realignment shortcut -- those are audit findings
#1 and #5 in the pipeline's own trail and they are not re-introduced here.

IDENTITY CHECK, always.  Every anchor is verified against the residue name the
numbering source expects before its coordinate is used:  5.58 and 7.53 must be
TYR with a modelled OH.  A position that is not what it claims returns a refusal,
never a number.  This is `analysis/block_d/cifmeasure.py`'s rule and the reason
that file was trusted; a construct offset that slipped would land on some other
residue and be caught on the spot.

TOOLING.  gemmi is NOT installed on this laptop (checked 2026-09-11) and
Biopython's MMCIFParser refuses some of our files (see
`figures/block_a/cifread.py:4`).  The mmCIF reader here is the same hand-rolled
one those two files use: column order is read from each file's own `_atom_site`
loop header, because it is not the same in every file and assuming a fixed order
has already crashed this project once.

SELF-TEST.  `--selftest` measures the deposited Class A entries this repo already
holds under `data/block_a/11_structures/` and `data/block_b_structures/` and
compares them against the values shipped in `reference_set.blockb_pinned.csv`.
A build step that cannot reproduce the numbers we already have is not allowed to
produce the ones we do not.

USAGE
    python3 redo/build/g0_measure_axes.py --selftest
    python3 redo/build/g0_measure_axes.py --pdb 4LDE --entry adrb2_human
    python3 redo/build/g0_measure_axes.py --from-csv redo/inputs/g0_calibration_structures.csv \\
            --out redo/g0_axis_measurements.csv --limit 25

Network: GPCRdb, EBI SIFTS and files.rcsb.org.  Everything is cached under
CACHE (default `redo/cache/structures/`), which is regenerable and belongs in
.gitignore -- the orchestrator owns that edit; this file does not make it.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
ROOT = os.path.dirname(os.path.dirname(INPUTS))
CACHE = STRUCTURES          # redo/cache/structures -- 297 mmCIF, gitignored

GPCRDB = "https://gpcrdb.org"
SIFTS_URL = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot_segments/{pdb}"
CIF_URL = "https://files.rcsb.org/download/{pdb}.cif"

# The two axes.  Declared here, once, and not passed in as parameters -- a
# measurement whose residue pair is a caller argument is a measurement that can
# be quietly changed between runs.
NPXXY_BW = ("5.58", "7.53")          # BW labels, OH atoms
TILT_GENERIC = ("2x46", "6x37")      # GPCRdb generic numbers, CA atoms
NPXXY_EXPECT_AA = "Y"                # both anchors must be tyrosine

AA3 = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q",
       "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
       "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
       "TYR": "Y", "VAL": "V"}


# ---------------------------------------------------------------------------
# HTTP with an on-disk cache, keyed on the natural key of the resource.
# Ported from bw_numbering.d9c646af.py:Api (itself a verbatim port of
# gpcr_pipeline.py:70-125).  Same throttle, same retry ladder.
# ---------------------------------------------------------------------------

class Api:
    def __init__(self, cache_dir: str = CACHE, delay: float = 0.15):
        self.cache = cache_dir
        os.makedirs(self.cache, exist_ok=True)
        self.delay = delay
        if requests is None:
            raise SystemExit("requests is not importable; the build step needs it")
        self.sess = requests.Session()
        self.sess.headers["User-Agent"] = "gpcr-state-scorer/0.1 (paper_af3 g0)"

    def _get(self, url: str, ok404: bool = False) -> bytes | None:
        for attempt in range(4):
            try:
                time.sleep(self.delay)
                r = self.sess.get(url, timeout=300, headers={"Accept": "application/json"})
                if r.status_code == 404 or (ok404 and r.status_code >= 400):
                    return None
                r.raise_for_status()
                return r.content
            except Exception:
                if attempt == 3:
                    if ok404:
                        return None
                    raise
                time.sleep(2 ** attempt)
        return None

    def get_json(self, url: str, key: str, ok404: bool = False):
        f = os.path.join(self.cache, key + ".json")
        if os.path.exists(f):
            return json.loads(open(f).read())
        data = self._get(url, ok404=ok404)
        try:
            parsed = json.loads(data) if data is not None else None
        except json.JSONDecodeError:
            parsed = None
        open(f, "w").write(json.dumps(parsed))
        return parsed

    def get_text(self, url: str, key: str, ok404: bool = False) -> str | None:
        f = os.path.join(self.cache, key)
        if os.path.exists(f):
            return open(f).read()
        data = self._get(url, ok404=ok404)
        if data is None:
            return None
        open(f, "wb").write(data)
        return data.decode("utf-8", "replace")


def get_generic_numbers(api: Api, entry: str) -> dict[int, dict]:
    """UniProt position -> {aa, segment, generic ('3x50'), bw ('3.50')}.

    Verbatim behaviour of bw_numbering.get_generic_numbers.
    """
    data = api.get_json(f"{GPCRDB}/services/residues/extended/{entry}/",
                        key=f"residues_ext_{entry}", ok404=True)
    out: dict[int, dict] = {}
    for r in data or []:
        dgn = r.get("display_generic_number") or ""
        bw = gn = ""
        if "x" in dgn:
            pre, suf = dgn.split("x", 1)
            bw = pre
            gn = pre.split(".")[0] + "x" + suf
        out[r["sequence_number"]] = {
            "aa": r.get("amino_acid"), "segment": r.get("protein_segment"),
            "generic": gn, "bw": bw,
        }
    return out


def lookup_bw(bw_map: dict[int, dict], label: str):
    """(uniprot_pos, expected_aa) for a BW label such as '5.58'."""
    for pos, info in bw_map.items():
        if info.get("bw") == label:
            return int(pos), (info.get("aa") or "")
    return None


def lookup_generic(bw_map: dict[int, dict], label: str):
    """(uniprot_pos, expected_aa) for a GPCRdb generic number such as '6x37'.

    The sibling `bw_numbering.py` does not ship.  BW and GPCRdb generic numbers
    diverge wherever a helix carries a bulge, and the tilt column is named
    `d_gpcrdb_tm6_tilt_246_637_ca` -- gpcrdb, not BW -- so this is the lookup it
    requires.
    """
    for pos, info in bw_map.items():
        if info.get("generic") == label:
            return int(pos), (info.get("aa") or "")
    return None


def accession_for_entry(api: Api, entry: str) -> str | None:
    """GPCRdb entry_name -> UniProt accession.

    Needed because SIFTS is keyed by accession and a GPCR construct routinely
    carries a SECOND accession in the same auth chain -- the fusion partner.
    See `sifts_offsets`.
    """
    data = api.get_json(f"{GPCRDB}/services/protein/{entry}/",
                        key=f"protein_entry_{entry}", ok404=True)
    return (data or {}).get("accession")


def load_sifts(api: Api, pdb: str) -> dict:
    data = api.get_json(SIFTS_URL.format(pdb=pdb.lower()),
                        key=f"sifts_{pdb.lower()}", ok404=True)
    if not data:
        return {}
    return data.get(pdb.lower(), {}).get("UniProt", {})


def sifts_offsets(sifts: dict, acc: str | None = None) -> list[dict]:
    """Flatten SIFTS to [{chain, unp_start, unp_end, auth_start, offset}].

    `offset` is auth_seq_id - uniprot_position within a segment.  It is per
    SEGMENT, not per chain: a construct with an excised ICL3 has two segments
    with different offsets and taking the first silently mis-numbers everything
    after the excision.

    THE ACCESSION FILTER IS LOAD-BEARING, and this is not a hypothetical.  A
    fusion construct puts the fusion partner and the receptor in the SAME auth
    chain, each with its own accession and its own offset.  4LDE chain A carries
    T4 lysozyme P00720 over UniProt 2-161 at offset +865 and ADRB2 P07550 over
    29-348 at offset +1000.  BW position 2x46 is UniProt 75, which falls inside
    BOTH ranges; taking the first covering segment lands on T4 lysozyme and
    returns d(2x46, 6x37) = 62.3 A against a shipped 17.6 A.  5ZTY does the same
    thing with its own fusion over 2-161.  Without `acc` this function is wrong
    on precisely the constructs that make up 40 of 64 inactive references
    (`redo/spec/PANEL.md` §9), i.e. it would corrupt the small side of the
    calibration split and nowhere else.
    """
    out = []
    for accession, rec in sifts.items():
        if acc and accession != acc:
            continue
        for m in rec.get("mappings", []):
            try:
                u0 = int(m["unp_start"]); u1 = int(m["unp_end"])
                a0 = int(m["start"]["residue_number"])
                auth0 = m["start"].get("author_residue_number")
                auth0 = int(auth0) if auth0 is not None else a0
            except (KeyError, TypeError, ValueError):
                continue
            out.append({
                "accession": accession,
                "chain": m.get("struct_asym_id"),
                "auth_chain": m.get("chain_id"),
                "unp_start": u0, "unp_end": u1,
                "auth_start": auth0,
                "offset": auth0 - u0,
            })
    return out


def unp_to_auth(segments: list[dict], pos: int, auth_chain: str | None = None):
    """UniProt position -> (auth_chain, auth_seq_id) using the covering segment."""
    for s in segments:
        if auth_chain and s["auth_chain"] != auth_chain:
            continue
        if s["unp_start"] <= pos <= s["unp_end"]:
            return s["auth_chain"], pos + s["offset"]
    return None, None


# ---------------------------------------------------------------------------
# mmCIF
# ---------------------------------------------------------------------------

def parse_cif(text: str) -> list[dict]:
    """Atoms, with column order taken from THIS file's own loop header.

    Same rule as analysis/block_d/cifmeasure.py:parse_cif -- the order is not the
    same in every file and assuming one crashed that script on its second input.
    """
    cols, atoms, in_loop = [], [], False
    for line in text.splitlines():
        if line.startswith("_atom_site."):
            cols.append(line.strip().split(".", 1)[1])
            in_loop = True
            continue
        if in_loop and line.startswith(("ATOM", "HETATM")):
            f = line.split()
            if len(f) != len(cols):
                continue
            r = dict(zip(cols, f))
            try:
                atoms.append({
                    "atom": r.get("label_atom_id"),
                    "comp": r.get("label_comp_id"),
                    "auth_chain": r.get("auth_asym_id") or r.get("label_asym_id"),
                    "label_chain": r.get("label_asym_id"),
                    "auth": r.get("auth_seq_id"),
                    "alt": r.get("label_alt_id", "."),
                    "occ": float(r.get("occupancy", 1.0) or 1.0),
                    "x": float(r["Cartn_x"]), "y": float(r["Cartn_y"]),
                    "z": float(r["Cartn_z"]),
                })
            except (TypeError, ValueError, KeyError):
                continue
        elif in_loop and line.strip() in ("#", ""):
            if atoms:
                in_loop = False
    return atoms


def pick_atom(atoms, chain, auth_seq, atom_name, expect_aa=None):
    """One atom, or a refusal string.

    Alternate conformers: the highest-occupancy altloc is taken and the choice is
    reported, because on a 2.0 A X-ray structure a Tyr OH with two conformers
    can differ by more than 2 A between them -- larger than the gap between the
    active and inactive NPxxY populations.
    """
    cands = [a for a in atoms
             if a["auth_chain"] == chain and str(a["auth"]) == str(auth_seq)]
    if not cands:
        return None, f"residue {chain}/{auth_seq} not modelled"
    comp = cands[0]["comp"]
    if expect_aa and AA3.get(comp) != expect_aa:
        return None, f"identity check failed at {chain}/{auth_seq}: {comp} is not {expect_aa}"
    named = [a for a in cands if a["atom"] == atom_name]
    if not named:
        return None, f"atom {atom_name} absent at {chain}/{auth_seq} ({comp})"
    named.sort(key=lambda a: -a["occ"])
    note = ""
    if len({a["alt"] for a in named}) > 1:
        note = f"altloc {named[0]['alt']} occ {named[0]['occ']:.2f}"
    return named[0], note


def dist(a, b) -> float:
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2
                     + (a["z"] - b["z"]) ** 2)


# ---------------------------------------------------------------------------
# The measurement
# ---------------------------------------------------------------------------

def measure(api: Api, pdb: str, entry: str, preferred_chain: str | None = None,
            cif_text: str | None = None) -> dict:
    """Both axes for one deposited structure.  Refusals, never guesses."""
    row = {
        "pdb_id": pdb.upper(), "gpcrdb_entry": entry,
        "chain_used": "", "numbering_strategy": "", "d_npxxy_oh": "", "d_tilt": "",
        "uniprot_acc": "",
        "pos_5_58": "", "pos_7_53": "", "pos_2x46": "", "pos_6x37": "",
        "auth_5_58": "", "auth_7_53": "", "auth_2x46": "", "auth_6x37": "",
        "npxxy_note": "", "tilt_note": "", "status": "ok",
    }
    bw_map = get_generic_numbers(api, entry)
    if not bw_map:
        row["status"] = f"no GPCRdb residue map for entry {entry}"
        return row

    anchors = {}
    for label in NPXXY_BW:
        hit = lookup_bw(bw_map, label)
        if hit is None:
            row["status"] = f"BW label {label} absent from {entry}"
            return row
        anchors[label] = hit
    for label in TILT_GENERIC:
        hit = lookup_generic(bw_map, label)
        if hit is None:
            row["status"] = f"generic number {label} absent from {entry}"
            return row
        anchors[label] = hit

    row["pos_5_58"], row["pos_7_53"] = anchors["5.58"][0], anchors["7.53"][0]
    row["pos_2x46"], row["pos_6x37"] = anchors["2x46"][0], anchors["6x37"][0]

    if cif_text is None:
        cif_text = api.get_text(CIF_URL.format(pdb=pdb.upper()),
                                key=f"{pdb.upper()}.cif", ok404=True)
    if cif_text is None:
        row["status"] = "mmCIF not retrievable"
        return row
    atoms = parse_cif(cif_text)
    if not atoms:
        row["status"] = "mmCIF parsed to zero atoms"
        return row

    acc = accession_for_entry(api, entry)
    row["uniprot_acc"] = acc or ""
    sifts = load_sifts(api, pdb)
    segs = sifts_offsets(sifts, acc=acc)
    if acc and not segs and sifts:
        row["status"] = (f"SIFTS has no segment for {acc} in {pdb} "
                         f"(present: {sorted(sifts)})")
        return row
    chains = [preferred_chain] if preferred_chain and any(
        s["auth_chain"] == preferred_chain for s in segs) else []
    chains += sorted({s["auth_chain"] for s in segs} - set(chains))
    if chains:
        # STRATEGY LADDER.  SIFTS is the primary numbering bridge but its
        # segment records are not uniformly reliable: for 7JVR it reports a
        # single segment unp 1-443 at offset +145 when chain R plainly runs
        # 34-441 in UniProt numbering, and for 7F83 it splits GHSR into four
        # segments whose last one maps UniProt 252-342 onto auth 1111-1201 when
        # the chain ends at 1111.  Both produce a refusal rather than a wrong
        # number -- the identity check catches them -- but both are recoverable,
        # because in each case the deposited auth numbering IS the UniProt
        # numbering.  So identity numbering is tried as a SECOND strategy and is
        # accepted only when all four anchors pass the same residue-identity
        # check.  A number is never produced by a strategy that could not prove
        # it landed on the right residue.
        strategies = [("sifts", segs)]
        strategies.append(("identity", [
            {"auth_chain": c, "unp_start": 1, "unp_end": 10 ** 6, "offset": 0,
             "accession": acc or "?"} for c in chains]))
    if not chains:
        # No SIFTS record: fall back to identity numbering on the longest
        # polymer chain, and SAY SO -- this path is a declared degradation, not
        # a silent one.
        n = {}
        for a in atoms:
            if a["comp"] in AA3:
                n.setdefault(a["auth_chain"], set()).add(a["auth"])
        chains = [max(n, key=lambda c: len(n[c]))] if n else []
        strategies = [("no-sifts-identity", [
            {"auth_chain": c, "unp_start": 1, "unp_end": 10 ** 6, "offset": 0,
             "accession": "?"} for c in chains])]

    fails = []
    for strat_name, strat_segs in strategies:
        for chain in chains:
            got = {}
            fail = ""
            for label, atom_name, expect in (
                    ("5.58", "OH", NPXXY_EXPECT_AA), ("7.53", "OH", NPXXY_EXPECT_AA),
                    ("2x46", "CA", None), ("6x37", "CA", None)):
                pos = anchors[label][0]
                ach, auth = unp_to_auth(strat_segs, pos, auth_chain=chain)
                if auth is None:
                    fail = (f"{label}: UniProt {pos} outside every {strat_name} "
                            f"segment of chain {chain}")
                    break
                atom, note = pick_atom(atoms, ach, auth, atom_name, expect_aa=expect)
                if atom is None:
                    fail = f"{label}: {note}"
                    break
                got[label] = (atom, auth, note)
            if len(got) == 4:
                row["chain_used"] = chain
                row["numbering_strategy"] = strat_name
                row["auth_5_58"], row["auth_7_53"] = got["5.58"][1], got["7.53"][1]
                row["auth_2x46"], row["auth_6x37"] = got["2x46"][1], got["6x37"][1]
                row["d_npxxy_oh"] = round(dist(got["5.58"][0], got["7.53"][0]), 6)
                row["d_tilt"] = round(dist(got["2x46"][0], got["6x37"][0]), 6)
                for k in ("5.58", "7.53"):
                    if got[k][2]:
                        row["npxxy_note"] = (row["npxxy_note"] + f" {k}:{got[k][2]}").strip()
                for k in ("2x46", "6x37"):
                    if got[k][2]:
                        row["tilt_note"] = (row["tilt_note"] + f" {k}:{got[k][2]}").strip()
                if strat_name != "sifts":
                    row["npxxy_note"] = (row["npxxy_note"]
                                         + f" [{strat_name}; SIFTS unusable: {fails[0] if fails else 'n/a'}]").strip()
                return row
            fails.append(f"{strat_name}/{chain}: {fail}")
    row["status"] = " | ".join(fails[:4])
    return row


# ---------------------------------------------------------------------------
# Self-test against the values this repo already ships
# ---------------------------------------------------------------------------

SELFTEST = [
    # (pdb, gpcrdb entry, path relative to ROOT)
    ("4LDE", "adrb2_human", "data/block_a/11_structures/connector_orthogonality/4LDE.cif"),
    ("5G53", "aa2ar_human", "data/block_a/11_structures/confidently_wrong/5G53.cif"),
    ("6PT2", "oprd_human",  "data/block_a/11_structures/agonist_only_vs_ternary/6PT2.cif"),
    ("5ZTY", "cnr2_human",  "data/block_a/11_structures/janus_cnr2/5ZTY.cif"),
    ("8GUR", "cnr2_human",  "data/block_a/11_structures/janus_cnr2/8GUR.cif"),
    ("7JVR", "drd2_human",  "data/block_a/11_structures/success_case/7JVR.cif"),
    ("7NA7", "ghsr_human",  "data/block_b_structures/01_instrument_references/GHSR_active_7NA7.cif"),
    ("7F83", "ghsr_human",  "data/block_b_structures/01_instrument_references/GHSR_inactive_7F83.cif"),
]
PINNED = os.path.join(ROOT, "data", "block_b", "09_references",
                      "reference_set.blockb_pinned.csv")
TOL = 0.01  # A.  A build step that cannot reproduce a shipped number to 0.01 A
            # is not measuring the same thing the campaign measured.


def selftest(api: Api) -> int:
    ref = {}
    for r in csv.DictReader(open(PINNED)):
        ref[r["pdb_id"].upper()] = r
    print(f"{'pdb':<6} {'entry':<12} {'axis':<10} {'measured':>12} {'shipped':>12} {'delta':>9}  verdict")
    bad = 0
    for pdb, entry, rel in SELFTEST:
        path = os.path.join(ROOT, rel)
        text = open(path).read() if os.path.exists(path) else None
        got = measure(api, pdb, entry, cif_text=text)
        want = ref.get(pdb.upper(), {})
        if got["status"] != "ok":
            print(f"{pdb:<6} {entry:<12} {'-':<10} {'REFUSED':>12} {'':>12} {'':>9}  {got['status']}")
            bad += 1
            continue
        for axis, mine, col in (("npxxy_oh", got["d_npxxy_oh"], "d_npxxy_oh_ref"),
                                ("tm6_tilt", got["d_tilt"], "d_gpcrdb_tm6_tilt_ref")):
            w = (want.get(col) or "").strip()
            if not w:
                print(f"{pdb:<6} {entry:<12} {axis:<10} {mine:>12.4f} {'(none)':>12} {'':>9}  new measurement")
                continue
            d = float(mine) - float(w)
            ok = abs(d) <= TOL
            bad += 0 if ok else 1
            print(f"{pdb:<6} {entry:<12} {axis:<10} {mine:>12.4f} {float(w):>12.4f} "
                  f"{d:>+9.4f}  {'MATCH' if ok else 'MISMATCH'}")
        if got["npxxy_note"] or got["tilt_note"]:
            print(f"{'':<6} {'':<12} note: {got['npxxy_note']} {got['tilt_note']}")
    print()
    print(f"anchor positions used (UniProt numbering), for comparison against "
          f"`anchor_positions` in {os.path.relpath(PINNED, ROOT)}:")
    for pdb, entry, rel in SELFTEST:
        path = os.path.join(ROOT, rel)
        text = open(path).read() if os.path.exists(path) else None
        g = measure(api, pdb, entry, cif_text=text)
        w = ref.get(pdb.upper(), {})
        ap = json.loads(w.get("anchor_positions") or "{}")
        agree = (str(ap.get("5.58", "")) == str(g["pos_5_58"])
                 and str(ap.get("7.53", "")) == str(g["pos_7_53"]))
        print(f"  {pdb:<6} 5.58={g['pos_5_58']} 7.53={g['pos_7_53']} "
              f"2x46={g['pos_2x46']} 6x37={g['pos_6x37']}   "
              f"pinned 5.58={ap.get('5.58', '-')} 7.53={ap.get('7.53', '-')}   "
              f"{'AGREE' if agree else 'DISAGREE'}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pdb")
    ap.add_argument("--entry")
    ap.add_argument("--from-csv")
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cache", default=CACHE)
    a = ap.parse_args()
    api = Api(a.cache)

    if a.selftest:
        return selftest(api)

    if a.pdb and a.entry:
        print(json.dumps(measure(api, a.pdb, a.entry), indent=2))
        return 0

    if a.from_csv:
        rows = list(csv.DictReader(open(a.from_csv)))
        if a.limit:
            rows = rows[:a.limit]
        out = []
        for i, r in enumerate(rows, 1):
            got = measure(api, r["pdb_id"], r["gpcrdb_entry"],
                          preferred_chain=r.get("preferred_chain") or None)
            got.update({k: r.get(k, "") for k in
                        ("receptor_slug", "state", "gpcr_class", "resolution",
                         "method", "role", "on_panel48")})
            out.append(got)
            print(f"[{i}/{len(rows)}] {got['pdb_id']:<6} {got['status']:<48} "
                  f"npxxy={got['d_npxxy_oh']} tilt={got['d_tilt']}", flush=True)
        if a.out:
            with open(a.out, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
                w.writeheader()
                w.writerows(out)
            print(f"wrote {a.out} ({len(out)} rows)")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
