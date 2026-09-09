"""Shared LaTeX-safety helpers, used by sync_bib.py and md2tex.py.

Kept in one place so the bibliography and the prose cannot disagree about how a
character is rendered.
"""
import re

# Characters pdfLaTeX cannot typeset directly, or that mean something else to it.
# Accented Latin (ö, é, Š ...) is NOT here: \usepackage[T1]{fontenc} handles it.
UNICODE_MAP = {
    "α": r"$\alpha$", "β": r"$\beta$", "γ": r"$\gamma$",
    "δ": r"$\delta$", "κ": r"$\kappa$", "μ": r"$\mu$",
    "µ": r"$\mu$",    "Δ": r"$\Delta$",
    "Å": r"\AA{}",    "×": r"$\times$", "≤": r"$\leq$",
    "≥": r"$\geq$",   "≈": r"$\approx$", "→": r"$\rightarrow$",
    "‐": "-", "‑": "-", "–": "--", "—": "---",
    "‘": "`", "’": "'", "“": "``", "”": "''",
    " ": " ", " ": " ", " ": " ", "…": r"\ldots{}",
}

def unicode_to_tex(s: str) -> str:
    for a, b in UNICODE_MAP.items():
        s = s.replace(a, b)
    return s

def remaining_non_ascii(s: str):
    """Anything left that T1 fontenc may not cover — report, do not guess."""
    return sorted({c for c in s if ord(c) > 0x24F})
