#!/usr/bin/env python3
'''Strip nulls from an a3m, verify uniform column widths after lowercase-strip.'''
import string, sys
from pathlib import Path
if len(sys.argv) != 3:
    print("usage: clean_a3m.py <input.a3m> <output.a3m>", file=sys.stderr); sys.exit(2)
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
tbl = str.maketrans("", "", string.ascii_lowercase)
with open(src, "rb") as f:
    raw = f.read()
text = raw.replace(b"\x00", b"").decode("utf-8", errors="replace")
lines = [ln.rstrip() if ln.startswith(">") else ln.rstrip() for ln in text.splitlines() if ln.strip()]
q_len = len(lines[1].translate(tbl))
kept = [lines[0], lines[1]]
skipped = 0
for i in range(2, len(lines), 2):
    if i+1 >= len(lines): break
    hdr, seq = lines[i], lines[i+1]
    if len(seq.translate(tbl)) == q_len:
        kept.append(hdr); kept.append(seq)
    else:
        skipped += 1
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text("\n".join(kept) + "\n")
print(f"wrote {dst}: {len(kept)//2} seqs (q_len={q_len}), skipped {skipped}")
