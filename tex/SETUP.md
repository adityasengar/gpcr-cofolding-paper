# TeX setup — must be identical on both laptops

The failure this prevents: a document that compiles on one machine and not the other,
with no warning until it happens. BasicTeX ships few packages and pulls more on
demand, so drift is likely unless the environment is pinned.

**Pinned environment:** BasicTeX / TeX Live **2026**, 375 packages, listed in
`tex/tex-packages.txt`. Verify any machine with `./tex/check_tex.sh`.

## Installing on a new Mac

1. **Install BasicTeX 2026.**
   ```
   brew install --cask basictex
   ```
   ~100 MB; full MacTeX is ~5 GB and unnecessary here. Install via **brew**, not the
   `.pkg` — a `.pkg` install strands you on whatever release you picked, and `tlmgr`
   refuses to update across releases ("Local TeX Live is older than remote repository").

2. **Open a new terminal** so `/Library/TeX/texbin` lands on your PATH, then confirm:
   ```
   pdflatex --version
   ```

3. **Update the package manager itself first.** Skipping this makes step 4 fail with
   confusing version errors:
   ```
   sudo tlmgr update --self
   ```

4. **Install the packages this project needs beyond BasicTeX's defaults:**
   ```
   sudo tlmgr install latexmk siunitx orcidlink todonotes
   ```
   `siunitx` (units: Å, µM, kcal/mol), `orcidlink` (author ORCIDs at submission),
   `todonotes` (margin notes while drafting). Everything else a Nature-style
   submission needs — geometry, setspace, lineno, booktabs, caption, subcaption,
   authblk, microtype — ships with BasicTeX already.

5. **Verify the match:**
   ```
   ./tex/check_tex.sh
   ```
   It must report `latexmk present` and all pinned packages present. Anything listed
   as missing, install with the command it prints.

## When the manuscript needs a new package

Install it, then **re-pin and commit**, or the other laptop breaks silently:

```
sudo tlmgr install <package>
tlmgr list --only-installed | sed 's/^i //;s/:.*//' | sort > tex/tex-packages.txt
git add tex/tex-packages.txt && git commit -m "tex: add <package>"
```

The other machine picks it up on its next `./session_start.sh`, which runs this check.
