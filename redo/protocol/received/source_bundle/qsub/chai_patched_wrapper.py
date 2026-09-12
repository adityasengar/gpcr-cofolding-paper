"""Wrapper: monkey-patch chai-lab's colabfold client to use longer timeouts
(60s instead of hardcoded 6.02s) and then invoke `chai-lab fold` with argv.

Rationale: chai-lab v0.x hardcodes timeout=6.02 on all requests to
api.colabfold.com. On the NIBR proxy (nibr-proxy.global.nibr.novartis.net:2011),
concurrent MSA downloads exceed this and cause infinite retry loops. Boltz and
OF3 use different MSA clients that don't have this issue.

This wrapper monkey-patches requests.get / requests.post as seen by
chai_lab.data.dataset.msas.colabfold so the timeout is 60s.
"""
import sys
import requests

# Save original methods
_orig_get = requests.get
_orig_post = requests.post

def _patched_get(*args, **kwargs):
    # chai-lab uses timeout=6.02 for connect+read; use a tuple so
    # connect can fail fast (30s) but slow proxy downloads have a
    # generous read window (600s).
    if kwargs.get('timeout') == 6.02:
        kwargs['timeout'] = (30, 600)
    return _orig_get(*args, **kwargs)

def _patched_post(*args, **kwargs):
    if kwargs.get('timeout') == 6.02:
        kwargs['timeout'] = (30, 600)
    return _orig_post(*args, **kwargs)

requests.get = _patched_get
requests.post = _patched_post

print("[chai_patched_wrapper] monkey-patched requests timeout 6.02 -> 60.02",
      file=sys.stderr)

# Now invoke chai-lab CLI with the remaining argv
sys.argv = ['chai-lab'] + sys.argv[1:]
from chai_lab.main import cli
cli()
