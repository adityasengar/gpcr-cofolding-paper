#!/usr/bin/env python3
"""Does any panel draw developer text onto a figure?

WHY THIS EXISTS. On 2026-09-10 the corpus session rasterised the panels rather
than trusting their ledger status, and found BB-1 -- MAIN-TEXT FIGURE 4 --
carrying a red annotation on its face:

    "The superseded 0.552 / 0.810 / 0.892 reference dashes named in the BB-1
     spec are deliberately not drawn: 0.552 is a pre-consolidation snapshot..."

That is a build note. It documents a real and correct decision, the ledger
already records it, and it must not reach a submission. Its ledger entry said
`ready`, and reading the script did not catch it; looking at the rendered PNG
did.

It was reported as the only instance. It was not. `bc1_pocket_2x2.py` was
drawing a second red block, and the last sentence of that one -- "Add the
per-receptor points when the rows arrive" -- was an instruction to us, on a
figure that is in the SI today. A grep found the first and missed the second,
which is the argument for a check that runs rather than a search someone
remembers to do.

THE RULE, and why it is drawn where it is:

    Text placed with fig.text() is CAPTION-AREA FURNITURE -- provenance, the
    filter, the n. It must be neutral in colour: grey, or ink.

    Text placed with ax.text() is IN THE DATA. It may be any colour, because
    there it means something: a threshold in red, a backbone in its own hue, a
    verdict coloured by the verdict.

So a red fig.text is the signature of a note to ourselves, and this file fails
on one. A red ax.text is fine and is not looked at.

WHAT IT CANNOT CATCH, stated so nobody trusts it too far: a build note written
in grey. Colour is a proxy for intent and a good one, but the real check is
still to render the panel and look at it, which is why `draw the number to check
it` is a standing rule on this project and not a one-off.

Usage:  python3 figures/audit_panels.py
Exit 1 if any panel draws warning-coloured text at figure level.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# colour tokens that read as a warning rather than as content
WARN = re.compile(r"color\s*=\s*(fs\.VERM|VERM|['\"]red['\"]|['\"]#[cCdDeEfF][0-9a-fA-F]{1,2}"
                  r"[0-3][0-9a-fA-F]{3}['\"]|['\"]crimson['\"]|['\"]firebrick['\"])")

# a fig.text( call and everything up to its closing paren, across line breaks
FIGTEXT = re.compile(r"fig\.text\s*\((?:[^()]|\([^()]*\))*\)", re.S)


def main():
    bad, checked = [], 0
    for path in sorted(glob.glob(os.path.join(HERE, "block_*", "panels", "*.py"))
                       + glob.glob(os.path.join(HERE, "panels", "*.py"))):
        src = open(path).read()
        checked += 1
        for m in FIGTEXT.finditer(src):
            hit = WARN.search(m.group(0))
            if hit:
                line = src.count("\n", 0, m.start()) + 1
                bad.append((os.path.relpath(path, os.path.dirname(HERE)),
                            line, hit.group(1)))

    print("=" * 78)
    print("PANEL AUDIT -- developer text drawn at figure level")
    print("=" * 78)
    print("\n%d panel scripts checked" % checked)
    print("%d draw warning-coloured text with fig.text()" % len(bad))
    for rel, line, tok in bad:
        print("   %s:%d  color=%s" % (rel, line, tok))

    print("\n" + "=" * 78)
    if bad:
        print("A red annotation at figure level is a note to ourselves. Move it to")
        print("the console, or to FIGURE_PROVENANCE.md, or to the ledger entry --")
        print("all three are read by the people who can act on it, and none of them")
        print("ships. If the text is genuinely for a READER, keep it and make it")
        print("neutral: it is content, and content is not red.")
    else:
        print("No panel draws warning-coloured text at figure level.")
        print("This does NOT mean no panel carries a build note -- one written in")
        print("grey passes here. Render the panel and look at it.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
