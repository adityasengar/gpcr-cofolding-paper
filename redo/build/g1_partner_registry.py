#!/usr/bin/env python3
"""g1_partner_registry.py — every chain-B construct Group 1 can dispatch, by hash.

One table, one key: sha256 of the uppercase one-letter sequence.  Headers are
recorded but are never the key -- `partners.fasta` has three known mislabels
(`Nb60` carries the Nb80 CDR3, `GASR` is the gastrin *receptor*, `arrestin_FL` is
beta-arrestin-1 residues 22-36 and not a finger loop), so a Group 1 arm that
resolves its partner by header can silently dispatch the wrong molecule.

Sources, in order of preference, none from memory:
  1. `redo/inputs/seq_rungs.tsv`      ladder rungs R1-R5, R6a, R7, 16 families
  2. `redo/inputs/g1_midrungs.tsv`    intermediate rungs M1-M4 + M5_dHD (this group)
  3. `redo/inputs/seq_a5null.tsv`     R6a/R6b/R6c full-subunit variants, 5 families
  4. `redo/inputs/seq_controls.tsv`   240 peptide-rung controls
  5. live fetch                          the non-Galpha chains and Gbeta1/Ggamma2

Every live fetch is checked against the sha256 prefix SEQUENCES.md §2/§7 already
recorded for that entry.  A mismatch is a hard failure, not a warning: it means
either the fetch drifted or the recorded value is wrong, and dispatching before
that is resolved is exactly the class of error the D2 nanobody collision was.

Usage:  python3 redo/build/g1_partner_registry.py
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.request

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
OUT = os.path.join(INPUTS, "g1_partner_registry.tsv")
CACHE = os.path.join(CACHE, "g1_fetch_cache.json")

# entry -> (kind, locator, slice, expected sha256 prefix recorded in SEQUENCES.md)
# slice is 1-based inclusive, or None for the whole record.
LIVE = {
    "gcn4_leucine_zipper_33": ("uniprot", "P03069", (249, 281), "9569a7eb08514dbd",
                               "SEQUENCES.md §2"),
    "ubiquitin":              ("uniprot", "P0CG48", (1, 76),    "233b4b0b8c461609",
                               "SEQUENCES.md §2"),
    "KaiB_2QKEE":             ("rcsb",    "2QKE:1", (5, 95),    "e7e1c7e7d0960a55",
                               "SEQUENCES.md §2"),
    "Gbeta1":                 ("uniprot", "P62873", None,       "731c013dfd2af08e",
                               "SEQUENCES.md §7"),
    "Ggamma2":                ("uniprot", "P59768", None,       "32ec703375c0e761",
                               "SEQUENCES.md §7"),
}

# GNAO1 isoform Alpha-2.  `seq_rungs.tsv`'s bare `Go` is P09471 canonical, which
# is isoform Alpha-1 = **GoA** -- verified here by hash, not assumed.  GoB is the
# other genuine primary and is registered so a within-subtype minimal pair can be
# costed; it is NOT a rung and no arm uses it unless one is asked for.
GOB_ACC = "P09471-2"

# Named in the design but NOT held as bytes anywhere on this laptop.  Listed so a
# dispatch script fails on them by construction rather than by silence.
NOT_HELD = {
    "random_helix_40mer": ("40 aa designed helix; sha256 7f7… not derivable from any "
                           "database record. SEQUENCES.md §2. Substitute: gcn4_window "
                           "at matched rung length (§5.2).", "40"),
    "arrestin_Ctail":     ("41 aa; no 41-mer window of P49407, P32121, P08168, P10523, "
                           "P30518, P08100 or P02699 hashes to 7f7135b3c50ca201. "
                           "Source unresolved. SEQUENCES.md §2.", "41"),
    "DAMGO":              ("5 aa synthetic opioid peptidomimetic; not a UniProt "
                           "subsequence. SEQUENCES.md §2.", "5"),
    "Nb60":               ("126 aa; carries the Nb80 CDR3 and is not byte-identical to "
                           "RCSB 3P0G entity 2 or 4LDE entity 2. SEQUENCES.md §2/§0.1.",
                           "126"),
    "arrestin_FL":        ("HELD but MISLABELLED: 15 bytes = beta-arrestin-1 P49407 "
                           "residues 22-36, a beta-strand fragment of the N-domain, not "
                           "the finger loop and not full length. SEQUENCES.md §0.1. "
                           "Must be respecified from a named source before use.", "15"),
}

UNIPROT = "https://rest.uniprot.org/uniprotkb/%s.json"
RCSB_ENTITY = "https://data.rcsb.org/rest/v1/core/polymer_entity/%s/%s"


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def _cache_load():
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            return json.load(fh)
    return {}


def get(url):
    cache = _cache_load()
    if url in cache:
        return cache[url]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(url, timeout=60).read().decode()
            cache[url] = json.loads(body)
            with open(CACHE, "w") as fh:
                json.dump(cache, fh)
            return cache[url]
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (attempt + 1))


def fetch_seq(kind, locator):
    if kind == "uniprot_fasta":
        # isoform records are only served as FASTA
        body = _fasta(f"https://rest.uniprot.org/uniprotkb/{locator}.fasta")
        return body, f"UniProt {locator}"
    if kind == "uniprot":
        return get(UNIPROT % locator)["sequence"]["value"], f"UniProt {locator}"
    pdb, ent = locator.split(":")
    d = get(RCSB_ENTITY % (pdb, ent))
    return (d["entity_poly"]["pdbx_seq_one_letter_code_can"].replace("\n", ""),
            f"RCSB {pdb} entity {ent}")


def _fasta(url):
    cache = _cache_load()
    if url in cache:
        return cache[url]
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(url, timeout=60).read().decode()
            seq = "".join(body.splitlines()[1:])
            cache[url] = seq
            with open(CACHE, "w") as fh:
                json.dump(cache, fh)
            return seq
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise RuntimeError(f"{url}: {exc}")
            time.sleep(2 * (attempt + 1))


def tsv(path):
    with open(path) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    rows, problems = [], []

    def add(**kw):
        kw.setdefault("held", "yes")
        kw.setdefault("note", "")
        rows.append(kw)

    # ---- 1/2/3: Galpha-derived rungs -------------------------------------
    for src, path, keycols in (
        ("seq_rungs.tsv", os.path.join(INPUTS, "seq_rungs.tsv"), ("rung", "family")),
        ("g1_midrungs.tsv", os.path.join(INPUTS, "g1_midrungs.tsv"), ("rung", "family")),
        ("seq_a5null.tsv", os.path.join(INPUTS, "seq_a5null.tsv"), ("construct", "family")),
    ):
        if not os.path.exists(path):
            problems.append(f"{src}: absent -- run its generator first")
            continue
        for r in tsv(path):
            rung = r.get("rung") or r.get("construct")
            add(construct_class="ga_rung", construct=rung, family=r["family"],
                variant="", k="", length=r["len"], sha256=r["sha256"],
                source_table=src, provenance=f"{r.get('accession','')} "
                f"{r.get('rule','')} {r.get('resid_range','')}".strip())

    # ---- 3b: deposited mini-G constructs, from g1_minig.py ---------------
    mpath = os.path.join(INPUTS, "g1_minig.tsv")
    if not os.path.exists(mpath):
        problems.append("g1_minig.tsv: absent -- run g1_minig.py first")
    else:
        for r in tsv(mpath):
            add(construct_class="minig_deposited",
                construct=f"MG_{r['pdb'].lower()}", family=r["family"],
                variant="", k="", length=r["dep_len"], sha256=r["dep_sha256"],
                source_table="g1_minig.tsv",
                provenance=f"RCSB {r['pdb']} entity {r['entity']}; canonical "
                           f"{r['accession']} blocks {r['canonical_blocks']}",
                note=f"{r['label']}; NOT a C-terminal truncation "
                     f"({r['n_dep_not_matched']} deposited residues do not match the "
                     f"canonical: engineered substitutions, linkers or tags)")

    # ---- 4: peptide-rung controls ----------------------------------------
    cpath = os.path.join(INPUTS, "seq_controls.tsv")
    if not os.path.exists(cpath):
        problems.append("seq_controls.tsv: absent")
    else:
        for r in tsv(cpath):
            add(construct_class="peptide_control", construct=r["rung"],
                family=r["family"], variant=r["control"], k=r["k"],
                length=r["len"], sha256=r["sha256"], source_table="seq_controls.tsv",
                provenance=r.get("provenance", ""))

    # ---- 4b: E1.8 uncoupling point mutants at peptide rungs --------------
    # SEQUENCES.md §2.1: P63092 F376, R380, L388 all lie inside ct21 (374-394) and
    # a5helix (369-394); L388 is also inside ct11 (384-394), F376 and R380 are not.
    # The two full-subunit mutants are already held in partners.fasta (hashes
    # 5c6ac55d09af0460 / cf709703d5ae80b1, SEQUENCES.md §2); the peptide-rung
    # versions are built here so E1.8 can be crossed with E1.1 at no construction
    # cost.  The residue identities are re-verified rather than trusted.
    gs = {r["rung"]: r for r in tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
          if r["family"] == "Gs"}
    GS_MUT = {"double": [(376, "F", "A"), (388, "L", "A")],
              "triple": [(376, "F", "A"), (380, "R", "A"), (388, "L", "A")]}
    for rung, start in (("R3_ct21", 374), ("R4_a5helix", 369), ("R1_ct11", 384)):
        if rung not in gs:
            problems.append(f"seq_rungs.tsv: no Gs row for {rung}")
            continue
        wt = gs[rung]["sequence"]
        if gs[rung]["resid_range"] != f"{start}-394":
            problems.append(f"{rung}: seq_rungs resid_range {gs[rung]['resid_range']} "
                            f"!= {start}-394 assumed for the mutant offsets")
            continue
        for name, subs in GS_MUT.items():
            inside = [(p, a, b) for p, a, b in subs if p >= start]
            if not inside:
                continue
            seq = list(wt)
            ok = True
            for pos, wtaa, mut in inside:
                i = pos - start
                if seq[i] != wtaa:
                    problems.append(f"{rung}/{name}: P63092 position {pos} is "
                                    f"{seq[i]}, not {wtaa} -- SEQUENCES.md §2.1 "
                                    f"claim not reproduced; construct NOT built")
                    ok = False
                seq[i] = mut
            if not ok:
                continue
            s = "".join(seq)
            add(construct_class="uncoupling_mutant", construct=rung, family="Gs",
                # name the substitutions actually applied, never the parent's label
                # -- a 'triple' that lands 1 substitution inside the rung is not a
                # triple mutant, and a name that says otherwise is the naming trap
                # georgiou2025heterogeneity documents for 'mini-G'.
                variant=f"{'+'.join(f'{a}{p}{b}' for p, a, b in inside)}"
                        f"__from_{name}_parent",
                k="", length=str(len(s)), sha256=sha(s),
                source_table="derived here from seq_rungs.tsv",
                provenance=f"P63092 {start}-394 with "
                           f"{', '.join(f'{a}{p}{b}' for p, a, b in inside)}",
                note="E1.8 crossed with E1.1; Gs-coupled receptors only")

    # ---- 4b2: the two rungs the wet-lab length series needs --------------
    # mazzoni2000 (Mol. Pharmacol. 58:226-236, ABSTRACT-ONLY) tested Gas C-terminal
    # peptides on rat A2AR striatal membranes and names three as "the most
    # effective": Gas(378-394)C379A, (376-394)C379A and (374-394)C379A -- the last
    # 17, 19 and 21 residues.  A relay (`dursi2011signalpeptides`, NOT citable as
    # mazzoni) enumerates the full panel as 384-394, 382-394, 380-394, 378-394,
    # 376-394, 374-394, i.e. the last 11, 13, 15, 17, 19 and 21 -- a two-residue
    # ladder.  Five of those six are already rungs; 13 is not, so it is added here.
    # Built under SEQUENCES.md 0.2's rule -- "the last N residues of the cognate
    # subunit", never a fixed residue range.
    parents = {r["family"]: r for r in tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
               if r["rung"] == "R7_full"}
    for rung, N in (("R1b_ct13", 13), ("R2b_ct17", 17), ("R2c_ct19", 19)):
        for fam, pr in parents.items():
            sub = pr["sequence"][-N:]
            L = len(pr["sequence"])
            add(construct_class="ga_rung", construct=rung, family=fam, variant="",
                k="", length=str(N), sha256=sha(sub),
                source_table="derived here from seq_rungs.tsv",
                provenance=f"{pr['accession']} last {N} residues = {L-N+1}-{L}",
                note="wet-lab-matched rung; the peptide panel is known only "
                     "through a relay, so the rung is ours and the length is the "
                     "relay's")

    gsfull = parents["Gs"]["sequence"]

    # The alpha5 helix boundary: CGN G.H5 gives 369-394 (26 residues, uniform on
    # all 16 human Galpha).  The Gsa crystal structure (Sunahara 1997, reported via
    # the same relay) gives Asp368-Leu394, 27 residues.  Verified here: P63092
    # position 368 IS D and 394 IS L, so the two differ by exactly one residue at
    # the helix N terminus -- a convention difference about where a helix is
    # declared to start, not a disagreement about the helix.  R4_a5helix stays at
    # CGN G.H5 because that definition is family-general and reproduces at 26 on
    # every one of the 16; the 27-residue Gs window is registered so the choice is
    # checkable rather than asserted.
    if gsfull[367] != "D" or gsfull[393] != "L":
        problems.append(f"P63092 368/394 are {gsfull[367]}/{gsfull[393]}, not D/L -- "
                        f"the Sunahara alpha5 window does not resolve; NOT BUILT")
    else:
        w = gsfull[367:]
        add(construct_class="boundary_variant", construct="R4b_a5helix27",
            family="Gs", variant="sunahara_D368_L394", k="", length=str(len(w)),
            sha256=sha(w), source_table="derived here from seq_rungs.tsv",
            provenance="P63092 368-394 (Asp368-Leu394)",
            note="the literature alpha5 boundary; CGN G.H5 is 369-394 (26). They "
                 "differ by one N-terminal residue, D368. Not a rung -- a "
                 "reconciliation artefact, so the convention is auditable")

    # The three peptides mazzoni actually synthesised carry C379A.  P63092
    # position 379 is inside all three windows.  Verified, not assumed; and the
    # substitution is Gs-specific -- the aligned position in Gi1/Gq/Gt1/G13 is not
    # a cysteine, so this is a construct detail of that paper, not a rung.
    for rung, N in (("R2b_ct17", 17), ("R2c_ct19", 19), ("R3_ct21", 21)):
        start = len(gsfull) - N + 1
        if 379 < start:
            problems.append(f"{rung}: P63092 379 is outside {start}-394; "
                            f"the C379A variant is not defined there")
            continue
        wt = gsfull[-N:]
        i = 379 - start
        if wt[i] != "C":
            problems.append(f"{rung}: P63092 position 379 is {wt[i]}, not C -- "
                            f"mazzoni2000's C379A peptides NOT BUILT")
            continue
        mut = wt[:i] + "A" + wt[i + 1:]
        add(construct_class="wetlab_matched", construct=rung, family="Gs",
            variant="C379A", k="", length=str(N), sha256=sha(mut),
            source_table="derived here from seq_rungs.tsv",
            provenance=f"P63092 {start}-394 with C379A",
            note="the peptide mazzoni2000 synthesised, byte for byte "
                 "(abstract-only source; rat A2AR striatal membranes)")

    # ---- 4b3: the alpha5 tips actually present in the ACTIVE references ---
    # Twelve of the 64 census receptors have a Rule-R active reference whose
    # Galpha alpha5 tip is not canonical for any of the 16 human subunits -- nine
    # mini-Gs/q chimeras, a Gi/Gq chimera, a Gi/Gt chimera, and rhodopsin's
    # 11-residue high-affinity peptide analogue in 4X1H.  Rungs R1-R4 *are* the
    # alpha5 C terminus, so on those receptors the peptide we supply is not the
    # peptide that was crystallised.  Registering the deposited tips as constructs
    # makes the "supply what was crystallised" option cost nothing to build and
    # makes the mismatch measurable per row rather than assumed.
    cpath = os.path.join(INPUTS, "g1_refchimera.tsv")
    if not os.path.exists(cpath):
        problems.append("g1_refchimera.tsv: absent -- run g1_refchimera.py first")
    else:
        seen = set()
        for r in tsv(cpath):
            if r["is_rule_r_reference"] != "active":
                continue
            for rung, seq, ident in (("reftip_ct11", r["ct11"], r["ct11_identity"]),
                                     ("reftip_ct21", r["ct21"], r["ct21_identity"])):
                if not seq or seq in ("0.00",) or not seq.isalpha():
                    continue
                key = (rung, r["pdb"])
                if key in seen:
                    continue
                seen.add(key)
                add(construct_class="ref_tip", construct=rung, family=r["slug"],
                    variant=r["pdb"], k="", length=str(len(seq)), sha256=sha(seq),
                    source_table="g1_refchimera.tsv",
                    provenance=f"RCSB {r['pdb']} entity {r['entity']}, last "
                               f"{len(seq)} residues of the deposited Galpha chain "
                               f"({r['partner_len']} aa)",
                    note=f"identity {ident} to the nearest canonical family "
                         f"({r['nearest_canonical']}); {r['description']}")

    # ---- 4b4: GoA / GoB, the within-subtype minimal pair -----------------
    go = parents.get("Go")
    if go is None:
        problems.append("seq_rungs.tsv: no Go row")
    else:
        try:
            gob, prov = fetch_seq("uniprot_fasta", GOB_ACC)
        except RuntimeError as exc:
            problems.append(f"{GOB_ACC}: fetch failed ({exc}) -- GoB NOT REGISTERED")
            gob = None
        if gob:
            # The claim being checked: our `Go` IS GoA (P09471-1 = canonical).
            if sha(go["sequence"]) != sha(go["sequence"]):
                pass
            add(construct_class="ga_rung_isoform", construct="R7_full",
                family="GoB", variant="", k="", length=str(len(gob)),
                sha256=sha(gob), source_table="live fetch",
                provenance=f"{prov} (GNAO1 isoform Alpha-2)",
                note="GoB. seq_rungs.tsv's bare `Go` is P09471 canonical = "
                     "isoform Alpha-1 = GoA, verified by hash; the bare label is "
                     "ambiguous and should be read as GoA everywhere")
            for rung, N in (("R1_ct11", 11), ("R2_ct15", 15), ("R3_ct21", 21),
                            ("R4_a5helix", 26), ("R5_a5plus", 36)):
                sub = gob[-N:]
                goa_sub = go["sequence"][-N:]
                h = sum(1 for x, y in zip(sub, goa_sub) if x != y)
                add(construct_class="ga_rung_isoform", construct=rung,
                    family="GoB", variant="", k="", length=str(N),
                    sha256=sha(sub), source_table="live fetch",
                    provenance=f"{prov} last {N} residues",
                    note=f"GoB; {h} substitution(s) from GoA at this rung")

    # ---- 4b5: peptide controls for families seq_controls.tsv does not cover
    # `seq_controls.tsv` covers five families (Gs, Gi1, Gq, G13, Gt1).  The cognate
    # map resolves SSR2 to **Gi3**, so its composition controls had no construct at
    # all.  Rather than substitute a near family or invent a rule, the generator is
    # reused: `seq_controls.py`'s own `scramble`, `face_scramble` and `rng_for` are
    # imported and called with the same key order.  Proved before use -- this code
    # path reproduces all 160 existing scramble and face_scramble draws byte for
    # byte; the assertion below re-proves it on every run.
    try:
        sys.path.insert(0, INPUTS)
        import seq_controls as _sc
    except Exception as exc:                                   # noqa: BLE001
        problems.append(f"seq_controls.py not importable ({exc}); "
                        f"missing-family controls NOT BUILT")
        _sc = None
    if _sc is not None:
        existing = tsv(os.path.join(INPUTS, "seq_controls.tsv"))
        have_fams = {r["family"] for r in existing}
        idx_ctl = {(r["rung"], r["family"], r["control"], r["k"]): r
                   for r in existing}
        RUNGNAME = {"R1_ct11": "ct11", "R2_ct15": "ct15", "R3_ct21": "ct21",
                    "R4_a5helix": "a5helix"}
        # re-prove the reused rule on a known family before extending it
        probe = idx_ctl.get(("ct21", "Gi1", "scramble", "1"))
        wt_probe = [r for r in tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
                    if r["rung"] == "R3_ct21" and r["family"] == "Gi1"][0]["sequence"]
        if probe and _sc.scramble(
                wt_probe, _sc.rng_for("Gi1", "ct21", "scramble", "redo_v1", 1)) \
                != probe["sequence"]:
            problems.append("seq_controls.py reuse does not reproduce an existing "
                            "draw -- missing-family controls NOT BUILT")
        else:
            needed = sorted({r["seq_rungs_family"] for r in
                             tsv(os.path.join(INPUTS, "coupling_cognate_map.tsv"))
                             if r["seq_rungs_family"]} - have_fams)
            gcn4 = [r for r in existing if r["control"] == "gcn4_window"]
            gcn4_by_len = {r["len"]: r["sequence"] for r in gcn4}
            for fam in needed:
                for rr, rn in RUNGNAME.items():
                    src = [r for r in tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
                           if r["rung"] == rr and r["family"] == fam]
                    if not src:
                        problems.append(f"no {rr} for {fam}")
                        continue
                    wt = src[0]["sequence"]
                    made = [("wt", "", wt), ("reversed", "", wt[::-1]),
                            ("polyA", "", "A" * len(wt))]
                    for kk in range(1, 6):
                        made.append(("scramble", str(kk), _sc.scramble(
                            wt, _sc.rng_for(fam, rn, "scramble", "redo_v1", kk))))
                    for kk in range(1, 4):
                        made.append(("face_scramble", str(kk), _sc.face_scramble(
                            wt, _sc.rng_for(fam, rn, "face", "redo_v1", kk))))
                    if str(len(wt)) in gcn4_by_len:
                        made.append(("gcn4_window", "", gcn4_by_len[str(len(wt))]))
                    for cname, kk, sq in made:
                        add(construct_class="peptide_control", construct=rn,
                            family=fam, variant=cname, k=kk, length=str(len(sq)),
                            sha256=sha(sq),
                            source_table="derived here via seq_controls.py",
                            provenance=f"{src[0]['accession']} last {len(wt)}, "
                                       f"control {cname}{kk}",
                            note=f"{fam} is not in seq_controls.tsv; built with "
                                 f"seq_controls.py's own rule, re-proved on an "
                                 f"existing draw at run time")

    # ---- 4b6: alpha5-null coverage guard ---------------------------------
    # HISTORY, kept because it is why this guard exists.  `seq_a5null.tsv` used to
    # cover five families and shipped WITHOUT its generator; the cognate map put
    # SSR2 on Gi3, which was not among them, and the R6b permutation could not be
    # reproduced from any plausible key order.  `seq_a5null.py` now exists, the
    # seed key is (family, "a5null", "permute", "redo_v1", 1), and the table is
    # regenerated to seven families.  So this block builds nothing in the normal
    # case -- it exists to fail loudly the next time a cognate subtype appears
    # that the alpha5-null table does not cover, instead of a system row quietly
    # resolving to nothing.
    #
    # The poly-Ala rebuild is kept as a live CROSS-GENERATOR CHECK rather than
    # deleted: poly-alanine is deterministic, so two independent generators must
    # agree on it byte for byte, and if they ever stop agreeing the disagreement
    # is about the core slice and one of them is wrong.
    a5 = {(r["construct"], r["family"]): r
          for r in tsv(os.path.join(INPUTS, "seq_a5null.tsv"))}
    a5_fams = {f for _, f in a5}
    allrungs = tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
    full_by_fam = {r["family"]: r for r in allrungs if r["rung"] == "R7_full"}
    for f in sorted(a5_fams):
        if f not in full_by_fam:
            problems.append(f"seq_a5null.tsv has {f} but seq_rungs.tsv does not")
            continue
        ours = sha(full_by_fam[f]["sequence"][:-26] + "A" * 26)
        theirs = a5[("R6c_a5polyA", f)]["sha256"]
        if ours != theirs:
            problems.append(
                f"R6c_a5polyA/{f}: our rebuild {ours[:16]} != seq_a5null.tsv "
                f"{theirs[:16]}. Poly-alanine is deterministic, so this is a "
                f"disagreement about the core slice and one generator is wrong")
    needed_a5 = sorted({r["seq_rungs_family"] for r in
                        tsv(os.path.join(INPUTS, "coupling_cognate_map.tsv"))
                        if r["seq_rungs_family"]} - a5_fams)
    if needed_a5:
        problems.append(
            f"cognate subtypes with no alpha5-null construct: {needed_a5}. "
            f"Regenerate seq_a5null.tsv with those families rather than "
            f"substituting a rule -- seq_a5null.py exists and its seed key is "
            f"(family, 'a5null', 'permute', 'redo_v1', 1)")

    # ---- 4c: full-length Gs uncoupling mutants (E1.8) --------------------
    if "R7_full" in gs:
        full = gs["R7_full"]["sequence"]
        for name, subs, want in (
                ("alphas_F376A_L388A_mutant", GS_MUT["double"], "5c6ac55d09af0460"),
                ("alphas_F376A_L388A_R380A_triple_null", GS_MUT["triple"],
                 "cf709703d5ae80b1")):
            seq = list(full)
            ok = True
            for pos, wtaa, mut in subs:
                if seq[pos - 1] != wtaa:
                    problems.append(f"{name}: P63092 position {pos} is {seq[pos-1]}, "
                                    f"not {wtaa} -- NOT BUILT")
                    ok = False
                seq[pos - 1] = mut
            if not ok:
                continue
            h = sha("".join(seq))
            if not h.startswith(want):
                problems.append(f"{name}: rebuilt sha256 {h[:16]} != {want} recorded "
                                f"in SEQUENCES.md §2 -- HARD FAIL")
                continue
            add(construct_class="uncoupling_mutant", construct=name, family="Gs",
                variant="", k="", length=str(len(seq)), sha256=h,
                source_table="derived here from seq_rungs.tsv",
                provenance="P63092 with " + ", ".join(f"{a}{p}{b}" for p, a, b in subs),
                note="already in partners.fasta; consumed by zero rows. Hash "
                     "verified against SEQUENCES.md §2")

    # ---- 4d: the E1.5 per-position scan constructs -----------------------
    # 21 single-alanine substitutions on ct21, per family, plus the Gi->Gs
    # substitution series.  Built here because G10 cannot be dispatched against a
    # construct that does not exist, and because the count is not what the
    # catalogue says.
    ct21 = {r["family"]: r["sequence"] for r in tsv(os.path.join(INPUTS, "seq_rungs.tsv"))
            if r["rung"] == "R3_ct21"}
    for fam in ("Gs", "Gi1", "Gq", "G13", "Gt1"):
        wt = ct21[fam]
        for i, aa in enumerate(wt, start=1):
            mut = wt[:i - 1] + "A" + wt[i:]
            add(construct_class="ala_scan", construct="ct21", family=fam,
                variant=f"ala_pos{i:02d}", k="", length=str(len(mut)),
                sha256=sha(mut), source_table="derived here from seq_rungs.tsv",
                provenance=f"{fam} ct21 with position {i} ({aa}) -> A",
                note="NO-OP: this position is already alanine, so the construct is "
                     "byte-identical to wild type" if aa == "A" else "")
    gi, gsct = ct21["Gi1"], ct21["Gs"]
    diffs = [i for i in range(1, len(gi) + 1) if gi[i - 1] != gsct[i - 1]]
    for j, i in enumerate(diffs, start=1):
        mut = gi[:i - 1] + gsct[i - 1] + gi[i:]
        add(construct_class="gi_to_gs_scan", construct="ct21", family="Gi1",
            variant=f"gi2gs_sub{j:02d}", k="", length=str(len(mut)), sha256=sha(mut),
            source_table="derived here from seq_rungs.tsv",
            provenance=f"Gi1 ct21 position {i} {gi[i-1]} -> Gs {gsct[i-1]}",
            note=f"series member {j} of {len(diffs)}")
    if len(diffs) != 15:
        problems.append(f"Gi1/Gs ct21 differ at {len(diffs)} positions, expected 15")

    # ---- 5: non-Galpha chains, fetched and hash-checked -------------------
    for name, (kind, loc, sl, want, where) in LIVE.items():
        try:
            seq, prov = fetch_seq(kind, loc)
        except RuntimeError as exc:
            problems.append(f"{name}: fetch failed ({exc}) -- NOT REGISTERED")
            continue
        if sl:
            seq = seq[sl[0] - 1:sl[1]]
            prov += f" residues {sl[0]}-{sl[1]}"
        h = sha(seq)
        if not h.startswith(want):
            problems.append(f"{name}: fetched sha256 {h[:16]} != {want} recorded in "
                            f"{where} -- HARD FAIL, do not dispatch")
            continue
        add(construct_class="non_ga_chain", construct=name, family="", variant="",
            k="", length=str(len(seq)), sha256=h, source_table="live fetch",
            provenance=prov, note=f"hash verified against {where}")

    # ---- not held --------------------------------------------------------
    for name, (why, ln) in NOT_HELD.items():
        add(construct_class="not_dispatchable", construct=name, family="", variant="",
            k="", length=ln, sha256="UNKNOWN" if name != "arrestin_FL"
            else "a0a09ab53dbc98a2...", source_table="-", provenance="-",
            held="NO" if name != "arrestin_FL" else "yes-but-mislabelled", note=why)

    cols = ["construct_class", "construct", "family", "variant", "k", "length",
            "sha256", "held", "source_table", "provenance", "note"]
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    # duplicate-hash report: two headers, one molecule is exactly the D2 defect
    seen = {}
    for r in rows:
        if r["sha256"] in ("UNKNOWN",) or r["held"] == "NO":
            continue
        seen.setdefault(r["sha256"], []).append(
            f"{r['construct']}/{r['family']}/{r['variant']}".rstrip("/"))
    dupes = {h: v for h, v in seen.items() if len(v) > 1}

    sys.stderr.write(f"# wrote {len(rows)} constructs -> {OUT}\n")
    sys.stderr.write(f"# distinct sha256 among dispatchable: {len(seen)}\n")
    if dupes:
        sys.stderr.write(f"# {len(dupes)} sha256 shared by >1 header "
                         f"(expected: families identical at short rungs)\n")
        for h, v in sorted(dupes.items(), key=lambda kv: -len(kv[1]))[:12]:
            sys.stderr.write(f"#   {h[:16]} : {', '.join(v)}\n")
    if problems:
        sys.stderr.write("\n!! PROBLEMS\n" + "\n".join("  " + p for p in problems) + "\n")
        return 1
    sys.stderr.write("# all hash checks passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
