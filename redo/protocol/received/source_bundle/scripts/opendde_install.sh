#!/bin/bash
# OpenDDE install (Aureka Research, AF3-family all-atom co-folding, 2026-07)
# Package: opendde (PyPI 1.1.1)   License: Apache-2.0 code + weights   Commercial: OK
# Weights: aurekaresearch/OpenDDE on HuggingFace (ungated); auto-download on first `opendde pred`
# See https://github.com/aurekaresearch/OpenDDE for current licence terms.
set -eo pipefail
module purge
module load proxy/GLOBAL Python/3.13.5-GCCcore-14.3.0
mkdir -p "$HOME/software/venvs"
rm -rf "$HOME/software/venvs/opendde"
python -m venv "$HOME/software/venvs/opendde"
source "$HOME/software/venvs/opendde/bin/activate"
python -m pip install --upgrade pip
echo "=== pip install opendde[gpu]   $(date) ==="
# torch==2.7.1 on Linux x86_64 default PyPI wheel is CUDA 12.6; opendde pins triton, cuequivariance
pip install --progress-bar off "opendde[gpu]==1.1.1"
echo "=== Done   $(date) ==="
pip list | grep -iE 'opendde|torch|numpy|scipy|rdkit|cuequivariance|triton' || true
python -c "import opendde; print('opendde OK:', opendde.__file__)"
opendde --help | head -30 || true
