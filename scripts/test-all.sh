#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ "${H4_USE_CURRENT_ENV:-0}" = "1" ]; then
  PYTHON="$(command -v python3)"
else
  if [ ! -x "$ROOT/.venv/bin/python" ]; then
    python3 -m venv "$ROOT/.venv"
  fi
  PYTHON="$ROOT/.venv/bin/python"
  "$PYTHON" -m pip install -e "$ROOT/apps/api[test]"
fi
cd "$ROOT"
PYTHONPATH="$ROOT/apps/api/src${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON" -m pytest apps/api/tests -q
"$PYTHON" -m unittest discover -s tests -v
"$PYTHON" scripts/build_site.py --preview
"$PYTHON" scripts/check_seo.py site/dist
