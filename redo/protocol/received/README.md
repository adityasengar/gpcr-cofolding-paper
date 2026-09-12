# Files received from paper_af3 over the encrypted bridge, 2026-09-11

Not a data drop. These are the pipeline side's own reference files, sent in
response to the blueprint request so we could cross-check our reconstruction
against their ground truth.

| file | sha256 (verified on receipt) | what |
|---|---|---|
| `gpcr_coupling.csv` | `6f497124841a76f4…` | receptor -> cognate Ga. `primary_ga_identity` is the string `scorer/propose.py::_partner_fasta` looks up at manifest-build time |
| `partners.fasta` | `1322501173417deb…` | the partner sequence catalogue as dispatched, 28 entries (was written 29 here; that count came from our own blueprint, not from the file) |
| `panel_receptor_sequences.fasta` | `12176740d7a61732…` | receptor chain-A sequences as dispatched |

Every hash was verified against the sender's stated value on arrival.
