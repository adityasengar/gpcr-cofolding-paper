#!/usr/bin/env python3
"""g1_recording_spec.py -- the per-prediction recording contract, as CODE.

**CURRENT SIZE: 79 columns** (47 inherited + 2 pocket-RMSD on 2026-09-12 + 30
dispatch-readiness on 2026-09-14).  Do not transcribe that number anywhere; run
`--check`, which prints it.  It has been quoted as 47 in nine documents while the
file held 49, which is the header-count failure class this project keeps hitting.

**Why this file exists, 2026-09-12.** `g1_recording_spec.tsv` is the 47-column
contract every delivered run must satisfy, and it was a HAND-MADE file sitting in
`inputs/`, which is declared code-only.  Three scripts read it and none wrote it.
`DECISIONS.md` F-22 records the general form: `layout.py` L3 compares a file to its
OWN recorded hash, so it catches an edit made after stamping and is blind to a file
created by hand and then stamped.  The campaign's most load-bearing input was the
clearest instance.

This generator reproduces the existing 47 rows EXACTLY -- `--check` asserts it
byte-for-byte against the file as it stood -- and then adds the two columns
`PLAN.md` Pillar 0 calls blocking.

**What the two new columns are for.**  `SC-C-6` records that the binary predicate is
floor-pinned on apo and ceiling-pinned on cognate for ~65% of cells, and says to
prefer the continuous pocket readout.  Measured on Block C's own rows, the choice of
instrument changes the ligand effect 5.5-7.9x while leaving the partner effect's sign,
direction and significance intact, and it inflates the apparent spread BETWEEN
backbones about fivefold.  Without these two columns a depth sweep has no
reference-free readout at all, because `kalakoti2025afsample2` [p.6] states confidences
across masking levels are "not directly comparable".

Run:    python3 redo/build/g1_recording_spec.py
Check:  python3 redo/build/g1_recording_spec.py --check   (regenerate and diff)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS                                     # noqa: E402

OUT = os.path.join(INPUTS, "g1_recording_spec.tsv")
HEADER = ["column", "grain", "dtype", "status", "required_for", "why"]

# The 47 columns exactly as delivered, moved from a hand-made TSV into code on
# 2026-09-12 (DECISIONS.md F-22).  Content is unchanged except that 10 rows
# carried only 5 fields -- four tabs where there should be five, the trailing `why`
# omitted rather than left empty -- and are padded to 6 here.  Nothing parsed the
# file strictly enough to notice, which is the same story as the file having had no
# generator at all.
INHERITED = [
    ['prediction_id', 'row', 'str', 'new', 'everything', "one row per prediction, not per cell. Block B's helicity and register columns live only in a 640-row cell-level file; a ladder cannot be argued from cell medians."],
    ['item', 'row', 'str', 'new', 'everything', 'G1a, P1b, G3a ... the RUN_MATRIX item that dispatched the row'],
    ['arm', 'row', 'str', 'new', 'everything', 'ladder, intermediate_nested, a5null, composition_controls ...'],
    ['receptor_slug', 'row', 'str', 'exists', 'everything', ''],
    ['receptor_uniprot_acc', 'row', 'str', 'new', 'chain identity', "which record; Block A's panel FASTA carries two sequences each for ADRB1, FSHR and MCHR1"],
    ['receptor_seq_sha256', 'row', 'str', 'new', 'chain identity', 'settles which of two variant sequences a row consumed. SEQ_RECEPTORS.md owns the bytes'],
    ['receptor_species', 'row', 'str', 'new', 'cross-species audit', "SEQUENCES.md 3.3; three of C1's 64 are non-human and two of them are in the provisional CORE-32"],
    ['partner_species', 'row', 'str', 'new', 'cross-species audit', ''],
    ['cross_species_partner', 'row', 'bool', 'new', 'cross-species audit', 'true wherever receptor_species != partner_species. No block has ever carried this column and the three mismatches were invisible as a result'],
    ['partner_construct_id', 'row', 'str', 'new', 'everything', 'the g1_partner_registry.tsv key, e.g. R3_ct21 / ct21@scramble#2'],
    ['partner_seq_sha256', 'row', 'str', 'new', 'everything', 'SEQUENCES.md 0.1. Block B hashed the FASTA; Block D hashed only the nanobody chains, which is why its three non-Gs cognate arms cannot be resolved from the drop'],
    ['n_partner_aa', 'row', 'int', 'exists (cell)', 'every rung verifiable from data', 'promote to row. Makes every rung checkable against the dispatch note rather than trusting it'],
    ['partner_ga_family', 'row', 'str', 'new', 'family contrasts', 'Gs/Gi1/Gq/G13/Gt1...; resolved from COUPLING.md at dispatch, recorded per row'],
    ['partner_ga_accession', 'row', 'str', 'new', 'family contrasts', 'the UniProt record the rung was sliced from'],
    ['chain_role_json', 'row', 'str', 'new', 'multi-peptide cells', "{chain_id: receptor|partner|peptide_ligand|gbeta|ggamma} with a sha256 each. A model handed two unlabelled 21-mers can place either in the intracellular crevice; endothelin1 is 21 aa, exactly ct21's length"],
    ['n_chains', 'row', 'int', 'new', 'R8_hetero', ''],
    ['partner_chain_order', 'row', 'str', 'new', 'R8_hetero', 'nothing in any block establishes that the backbones are order-invariant on three chains'],
    ['partner_msa_mode', 'row', 'str', 'new', 'the whole ladder', 'off (primary) / on (E1.9 contrast). SEQUENCES.md 6.1'],
    ['partner_msa_depth', 'row', 'int', 'new', 'the whole ladder', "the ladder is uninterpretable without it: a 21-aa conserved query pulled 732 homologs in this project's own cache while a designed 40-mer pulled 1"],
    ['partner_msa_depth_uniref90', 'row', 'int', 'new', 'the whole ladder', ''],
    ['receptor_msa_depth', 'row', 'int', 'new', 'joins to Group 8', "on in Group 1 everywhere; varying it is Group 8. STATUS CORRECTED 2026-09-14: this read `exists`, and `exists` is what tells us NOT to ask for a column. A whole-header sweep of every delivered block table finds no MSA-depth column of any kind anywhere -- 0 occurrences. F-6 says the same: the frozen campaign recorded NOTHING about the MSA on any scored row."],
    ['partner_chain_helicity_frac', 'row', 'float', 'new', 'reach vs recognition', 'DSSP H/G/I over the WHOLE supplied chain. Generalises partner_tail11_helicity_frac, which is meaningless at the 11-mer rung where the tail is the chain. tran2026nanogs: an unstapled linear alpha5 peptide is a random coil and does nothing'],
    ['partner_helix_span_len', 'row', 'int', 'new', 'the length hypothesis', 'number of residues in the LONGEST contiguous helical run on the supplied chain. A fraction cannot express the hypothesis: the 11-mer and the 21-mer are both reported helical, differing in helix LENGTH (a short helix near the C terminus vs a long one spanning most of the 21-mer). The predicted covariate is continuous and monotone in length, not a switch'],
    ['partner_helix_span_start', 'row', 'int', 'new', 'the length hypothesis', "first residue of that run, numbered from the supplied chain's N terminus"],
    ['partner_helix_span_end', 'row', 'int', 'new', 'the length hypothesis', "last residue of that run. Start and end together say WHERE the helix sits, which is what distinguishes 'a short helix at the tip' from 'a long helix along the chain'"],
    ['partner_helix_span_uniprot_range', 'row', 'str', 'new', 'the length hypothesis', 'the same span mapped onto the parent Galpha numbering, so a predicted helix can be set against a reported one without re-deriving the offset'],
    ['partner_tail11_helicity_frac', 'row', 'float', 'exists (cell)', 'continuity with Block B', 'promote to row'],
    ['plddt_partner_chain_mean', 'row', 'float', 'new', 'reach vs recognition', "the closest in-silico analogue of tran's CD measurement. Block B has plddt_ga_alpha5 only"],
    ['plddt_ga_alpha5', 'row', 'float', 'exists', 'per-rung comparability', ''],
    ['n_interface_contacts_ga_receptor', 'row', 'int', 'exists', 'engagement, not presence', ''],
    ['d_ga_alpha5_r350_ca', 'row', 'float', 'exists', 'engagement depth', ''],
    ['interface_score_dockq_like', 'row', 'float', 'new', 'the intermediate rungs', 'junker2026peptidedesign p16: comparing an interface score across peptides of different lengths is unsound, and p5 reports PAE OVER-estimates exactly where a GPCR peptide is misplaced. A confidence metric will not catch the failure mode; a DockQ-like score will. Defined identically from 11 to 805 residues, or reported within-rung only'],
    ['contact_register_last5_json', 'row', 'str', 'exists (cell)', 'the register question', 'which receptor positions the last five partner residues touch. 3SN6 puts Y391 on R131(3.50); 6E67 puts E392 there'],
    ['ras_domain_ca_rmsd_to_R7', 'row', 'float', 'new', 'R6a/R6b/R6c and M5_dHD', 'a bulk control that arrives as a molten globule is not mass-matched to anything. Gate before G3b dispatches'],
    ['axis_npxxy', 'row', 'float', 'exists', 'the predicate', 'shipped continuously, never only as a call'],
    ['axis_tm6', 'row', 'float', 'exists', 'the predicate', 'shipped continuously, never only as a call'],
    ['state_call', 'row', 'str', 'derived', 'the predicate', 'a derived call, recomputable from the two axes and a stated threshold'],
    ['active_frac_deposited', 'row', 'float', 'new', 'E1.2 exposure stratification', "yu2026domainmotion's decisive covariate is training composition (40.3 points) not the co-input (11.9/9.1). A bulk control not stratified by deposited exposure is uninterpretable on their design. Median split declared BEFORE dispatch"],
    ['n_deposited_active', 'row', 'int', 'new', 'E1.2 exposure stratification', ''],
    ['n_deposited_inactive', 'row', 'int', 'new', 'E1.2 exposure stratification', ''],
    ['worse_reference_res', 'row', 'float', 'new', 'covariate, not filter', 'RUN_MATRIX 10.1: keep the resolution rule as a covariate and report the headline with and without a 3.00 A restriction'],
    ['backbone', 'row', 'str', 'exists', 'everything', ''],
    ['seed', 'row', 'int', 'exists', 'seed pairing', "seeds are unpaired everywhere in A-D: 1,898 distinct seed_outer across Block A's 380 cells. Pair seeds across arms within a cell or no within-seed contrast is readable"],
    ['sample_index', 'row', 'int', 'new', 'sample vs seed grain', 'Block D\'s "256 of 319 unanimous" is a sample-grain number read as a seed-grain one. STATUS CORRECTED 2026-09-14: this read `exists` and the column appears in NO delivered block header -- 0 occurrences across every block table. The distinction it carries is the one that number was misread on, so marking it `exists` meant never asking for the column that settles it.'],
    ['ref_alpha5_tip_identity', 'row', 'float', 'new', 'the alpha5 rungs', "fraction identity between the alpha5 tip of THIS receptor's active reference and the canonical tip of the family we supplied, at the rung's own length. 0.82 at ct11 and 0.62 at ct21 for the nine mini-Gs/q receptors; 0.64 at ct11 for OPSD"],
    ['ref_alpha5_is_canonical', 'row', 'bool', 'new', 'the alpha5 rungs', "false wherever the active reference's alpha5 tip matches no canonical human Galpha. 12 of the 64 census receptors, 6 of the provisional CORE-32. Without this column the mismatch is invisible at exactly the residues the paper is about"],
    ['ref_alpha5_pdb', 'row', 'str', 'new', 'the alpha5 rungs', 'which deposited entry the two columns above were read from'],
]


# The two columns PLAN.md Pillar 0 makes blocking.  Named to match the columns
# rows.tier3.v2.csv already carries, so the redo and the frozen campaign can be read
# with one vocabulary rather than two.
ADDED = [
    ["pocket_ca_rmsd_active", "row", "float", "new", "every arm",
     "Ca RMSD of the orthosteric pocket to the ACTIVE reference. SC-C-6 prefers this "
     "over the binary predicate, which is floor-pinned on apo and ceiling-pinned on "
     "cognate for ~65% of cells. Measured on Block C's rows the instrument choice "
     "moves the ligand effect 5.5-7.9x and inflates the apparent spread BETWEEN "
     "backbones ~5x, while leaving the partner effect's sign, direction and "
     "significance intact. Absent from the first 47 columns; PLAN.md Pillar 0 blocking."],
    ["pocket_ca_rmsd_inactive", "row", "float", "new", "every arm",
     "The same, to the INACTIVE reference. Both are required, not one: the readout "
     "that behaves is the DIFFERENCE (inactive - active), and a single distance "
     "cannot say whether a structure moved toward active or merely away from its "
     "reference. rows.tier3.v2.csv carries both under these names."],
]


# ---------------------------------------------------------------------------
# 2026-09-14.  Thirty columns, added in one edit because the window closes at
# dispatch and every one of them is free today.
#
# Grouped by WHAT THEY COST THE PIPELINE TEAM, because an ask that does not
# distinguish "echo the value we handed you" from "write new measurement code"
# spends credibility it will need later:
#
#   ECHO (15)   dispatch metadata we supply; they write it back unchanged
#   EXISTS (6)  already computed and shipped in Blocks B and/or D; spec edit only
#   NEW (9)     genuinely new measurement, and the nine that make the campaign
#               auditable at all
# ---------------------------------------------------------------------------
ADDED_2026_09_14 = [

    # -- A. The run receipt.  Without these eight, gates/run_receipt.py cannot
    # run: it reads seven columns and this contract declared none of them, so a
    # delivery conforming exactly to the contract we were about to ship is
    # REFUSED on run 1 by the gate that exists to protect run 1.  Proved by
    # building two fixture runs to each contract and calling check_run(): both
    # returned four FAILs and zero PASSes.  Each pair is requested-vs-returned,
    # which is the whole point -- F-9 found that nothing in the frozen pipeline
    # compared output to input anywhere, so a monomer returned where a dimer was
    # asked for passed every check.
    ['n_chains_requested', 'row', 'int', 'new', 'run receipt R1',
     'ECHO. What we dispatched. R1 compares this against n_chains_returned.'],
    ['n_chains_returned', 'row', 'int', 'new', 'run receipt R1',
     'NEW. Counted from the delivered structure, not from the request. This is the '
     'column that catches a monomer returned where a dimer was asked for.'],
    ['partner_requested', 'row', 'str', 'new', 'run receipt R2',
     'ECHO. The g1_partner_registry.tsv construct id as dispatched.'],
    ['partner_returned_sha256', 'row', 'str', 'new', 'run receipt R2',
     'NEW. sha256 of the partner chain sequence AS RETURNED, read off the delivered '
     'structure. R2 compares it against the dispatched partner_seq_sha256.'],
    ['seed_requested', 'row', 'int', 'new', 'run receipt R3',
     'ECHO. The seed we allocated. Pairing across arms is only checkable if the '
     'REQUESTED seed is on the row; Blocks A and B both lost the within-seed '
     'contrast because only the used seed was ever recorded (1,898 distinct '
     'seed_outer across 380 Block A cells).'],
    ['seed_used', 'row', 'int', 'new', 'run receipt R3',
     'NEW. The seed the backbone actually ran. The frozen OF3 status file names '
     'resolved_seeds [945550830] while the output directories are 108204258, '
     '2344327426, 2650761416 and 4017696312 -- so requested != used has already '
     'happened once, undetected.'],
    ['partner_msa_depth_expected', 'row', 'int', 'new', 'run receipt R4',
     'ECHO. 1 at every ladder rung under the query-only regime. Stating the target '
     'on the row is what makes "off" checkable without trusting the word.'],
    ['partner_msa_depth_observed', 'row', 'int', 'new', 'run receipt R4',
     'NEW. Rows counted in the alignment actually consumed. A missing value here is '
     'a FAILURE, not a skip -- a check that quietly does nothing when its input is '
     'absent is the defect it exists to catch.'],

    # -- B. Confidence.  Title clause 3 IS a confidence claim and this contract
    # carried two partner-side pLDDT columns and nothing else.  Blocks B and D
    # each ship all four already, so this is a spec edit, not new code.
    ['plddt_mean', 'row', 'float', 'exists', 'title clause 3',
     'EXISTS in Block B (rows_tidy.csv col 30) and Block D (col 44).'],
    ['plddt_at_anchors', 'row', 'float', 'exists', 'title clause 3',
     'EXISTS in Block B (col 31) and Block D (col 45).'],
    ['min_plddt_at_anchor', 'row', 'float', 'exists', 'title clause 3',
     'EXISTS in Block B (col 32) and Block D (col 52). Also the input the X1 '
     'anchor-admissibility census needs, which is a free experiment.'],
    ['confidence_flag', 'row', 'str', 'exists', 'title clause 3',
     'EXISTS in Block B (col 33) and Block D (col 51).'],

    # -- C. Ligand identity.  Without these three the decoy arm dispatches,
    # costs 396 predictions, and returns data that cannot be analysed: each
    # receptor draws THREE decoy molecules and nothing on the row says which one
    # produced the prediction.
    ['ligand_id', 'row', 'str', 'new', 'the decoy arm',
     'ECHO. ChEMBL id for a decoy, CCD for a curated ligand, "none" when ligand-free.'],
    ['ligand_inchikey', 'row', 'str', 'new', 'the decoy arm',
     'ECHO. drule_selected.tsv sets ligand_must_key_by=inchikey on every accepted '
     'decoy, so the InChIKey is the identity, not the name.'],
    ['ligand_draw_index', 'row', 'int', 'new', 'the decoy arm',
     'ECHO. 1..k within the receptor draw. THE column that makes the decoy arm '
     'analysable; without it the three molecules are indistinguishable in the output.'],

    # -- D. Templates.  The redo specifies no template setting for any backbone,
    # so whichever launcher the receiving team writes will govern and each
    # library default is inherited silently.  Worse than a gap: our own documents
    # contradict each other on OpenFold-3's default (BLOCK_B_CLAIM_SHEET.md:303
    # says off-is-also-default; six frozen-bundle locations say default-on).  The
    # requested/used pair settles it from the data instead of from the prose.
    ['templates_requested', 'row', 'bool', 'new', 'no-oracle guarantee',
     'ECHO. false on every row of this campaign (D-2026-09-14-b).'],
    ['templates_used', 'row', 'bool', 'new', 'no-oracle guarantee',
     'NEW, and a RUNTIME echo, not a re-read of the input file. The frozen status '
     "JSONs' template fields are input-file probes -- status_writer.py re-reads the "
     'yaml it just wrote -- so they cannot catch a library default applied after the '
     'input is parsed. If a template of the very receptor being predicted reaches '
     'the model, the paper is showing it the answer.'],

    # -- E. MSA realised-vs-target.  E8.3 is Blocking in six places.  `full` is a
    # real condition (cached a3m, no subsample) and `default` is a live fetch --
    # different conditions wearing the same name -- while every slope was fitted
    # with full imputed as 4096 against a real span of ~2K-11K rows, and one
    # ADRB1 cell consumed 13,678.
    ['receptor_msa_depth_target', 'row', 'int', 'new', 'E8.3, the depth anchor',
     'ECHO. What was asked for.'],
    ['receptor_msa_depth_realised', 'row', 'int', 'new', 'E8.3, the depth anchor',
     'NEW. Rows actually consumed. subsample_msa.py returns the input UNCHANGED when '
     'len(entries) <= depth while the manifest still records the nominal depth, so '
     'target and realised diverge silently at the shallow rungs too.'],
    ['msa_target_unreached', 'row', 'bool', 'new', 'E8.3, the depth anchor',
     'NEW. true wherever realised < target. Makes the silent no-op above visible '
     'per row instead of per campaign.'],
    ['msa_mode_label', 'row', 'str', 'new', 'E8.3, the depth anchor',
     'ECHO, with `default` and `full` as DISTINCT values. Collapsing them is the '
     'defect: OPSD x Boltz-2 apo reads 38.8% under D1 `default` and 10.0% under D3 '
     '`full`, 28.8 points apart at ~3 sigma, both arms apo.'],
    ['msa_depth_by_chain_json', 'row', 'str', 'new', 'the undeclared chains',
     'NEW. {chain_id: realised_depth}, keyed the same way as chain_role_json. The '
     'contract governs the receptor and partner chains and says nothing about any '
     'other: 22 G2 rows supply a peptide ligand as a polymer chain and 30 G1 '
     'heterotrimer rows supply Gbeta1 + Ggamma2 -- 52 rows whose alignment regime is '
     'undeclared. Ggamma2 measures at depth 3,191 in our own cache. One column '
     'covers partner, ligand and Gbetagamma rather than three.'],

    # -- F. The instrument.  Extracting the predicate into a table, and naming it
    # on every row, is what makes a second receptor class or a different protein
    # family cheap later -- and it makes today's thresholds auditable from the
    # data rather than from twelve copy-pasted module constants.
    ['instrument_id', 'row', 'str', 'new', 'the state call',
     'ECHO. Key into g0_instrument.tsv. 9.082 and 14.932 are currently copy-pasted '
     'as module constants into at least twelve files instead of read from one table.'],
    ['system_family', 'row', 'str', 'new', 'the state call',
     'ECHO. "gpcr" today. The seam that makes a different protein family additive '
     'rather than a rewrite.'],
    ['system_class', 'row', 'str', 'new', 'the state call',
     'ECHO. "A" today, and Class A only by D-2026-09-12-d on measured grounds (F-13). '
     'Recorded so a pooled cross-class rate is visible in the data if anyone ever '
     'computes one, which F-13 forbids.'],
    ['threshold_applied', 'row', 'str', 'new', 'the state call',
     'ECHO. The actual cut used for THIS row, so state_call stays recomputable when '
     'the threshold is later refitted. 9.08 is applied and 9.082 is derived -- a '
     'truncation that already changes the call for one borderline row and fails '
     "Block B's check B20."],

    # -- G. Cost.  One column retires ask P1 permanently.
    ['wall_seconds', 'row', 'float', 'new', 'the cost model',
     'NEW. End-to-end wall time per prediction. matrix_cost.py prices every '
     'prediction off ONE measured apo rate and chain-B length enters the model '
     'nowhere, so all three scenarios are derived for a 394-residue full Galpha: a '
     '21-residue chain B is 401 tokens, 1.06-1.11x, BELOW the model own floor of '
     '2.0x. With this column the cost-versus-length curve falls out of the campaign '
     'across all seven rungs at zero extra GPU time.'],

    # -- H. The amendment protocol.
    ['tranche', 'row', 'str', 'new', 'append-only amendment',
     'ECHO. "t1" for everything registered today. A later addition enumerates as t2 '
     'with its own registration date and never rewrites t1, so "decided before '
     'seeing data" stays checkable. Also makes cross-tranche pooling visible in the '
     'delivered rows, which is the one thing no gate can otherwise see.'],

    # -- I. Structural QC.  Already shipped in Block B; the free X3 experiment
    # needs exactly these two.
    ['chain_breaks', 'row', 'int', 'exists', 'fold integrity',
     'EXISTS in Block B (rows_tidy.csv col 51).'],
    ['ramachandran_outlier_frac', 'row', 'float', 'exists', 'fold integrity',
     'EXISTS in Block B (col 52). With chain_breaks this is the free fold-integrity '
     'control: a bulk control that arrives as a molten globule is mass-matched to '
     'nothing.'],
]


def build():
    rows = [list(r) for r in INHERITED]
    if len(rows) != 47:
        sys.exit(f"FAIL: expected the 47 inherited columns, have {len(rows)}")
    out = rows + ADDED + ADDED_2026_09_14
    names = [r[0] for r in out]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        sys.exit(f"FAIL: duplicate column name(s) {dupes} -- a later block "
                 f"re-declares a column an earlier one already has.")
    bad = [r[0] for r in out if r[3] not in ("new", "exists", "exists (cell)", "derived")]
    if bad:
        sys.exit(f"FAIL: unknown status on {bad}. The vocabulary is fixed at "
                 f"new / exists / exists (cell) / derived -- `exists` means DO NOT "
                 f"ASK FOR IT, so a wrong value here silently drops a real ask.")
    if len(r := out) != 79:
        sys.exit(f"FAIL: expected 79 columns, built {len(r)}")
    return out


def main(argv):
    rows = build()
    body = "\t".join(HEADER) + "\n" + "\n".join("\t".join(r) for r in rows) + "\n"
    if "--check" in argv:
        have = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if have != body:
            sys.exit("FAIL: g1_recording_spec.tsv does not match this generator. "
                     "Re-run without --check, then restamp the manifest.")
        print(f"OK  {len(rows)} columns, file matches the generator")
        return 0
    open(OUT, "w", encoding="utf-8").write(body)
    print(f"wrote {OUT}  ({len(rows)} columns: {len(INHERITED)} inherited "
          f"+ {len(ADDED)} pocket (2026-09-12) "
          f"+ {len(ADDED_2026_09_14)} dispatch-readiness (2026-09-14))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
