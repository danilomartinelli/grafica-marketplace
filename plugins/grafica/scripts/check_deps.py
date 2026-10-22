#!/usr/bin/env python3
"""Confere as dependências do kit e diz como instalar o que faltar. Rode uma vez por sessão.

  python3 check_deps.py
"""
import importlib
import shutil
import sys

PY = [("reportlab", "reportlab"), ("PIL", "Pillow"), ("fontTools", "fonttools"), ("numpy", "numpy"), ("pypdf", "pypdf")]
BIN = ["pdftoppm", "pdftocairo", "pdfimages", "pdffonts", "pdfinfo"]

faltam_py = []
for mod, pkg in PY:
    try:
        importlib.import_module(mod)
    except ImportError:
        faltam_py.append(pkg)
faltam_bin = [b for b in BIN if not shutil.which(b)]

if not faltam_py and not faltam_bin:
    print("dependências ok")
    sys.exit(0)
if faltam_py:
    print("Faltam pacotes Python:", ", ".join(faltam_py))
    print("  instale: pip install " + " ".join(faltam_py) + "   (em alguns sistemas: pip install --break-system-packages ...)")
if faltam_bin:
    print("Faltam ferramentas do poppler:", ", ".join(faltam_bin))
    print("  Debian/Ubuntu: sudo apt-get install poppler-utils · macOS: brew install poppler · Windows: instale o poppler e ponha no PATH")
sys.exit(1)
