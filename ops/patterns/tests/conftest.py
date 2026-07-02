# conftest.py — setup central de sys.path para toda a suite (debate O6, item 4)
# Torna os shims individuais dos testes redundantes (e inofensivos) apos a
# unificacao dos test_*.py da raiz de ops/patterns dentro de tests/.
import os
import sys

_PATTERNS = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_MECHA = os.path.abspath(os.path.join(_PATTERNS, "..", ".."))
_KERNEL_VALIDATORS = os.path.join(_MECHA, "kernel", "validators")

for _p in (_PATTERNS, _MECHA, _KERNEL_VALIDATORS):
    if _p not in sys.path:
        sys.path.insert(0, _p)
