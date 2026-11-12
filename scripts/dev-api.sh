#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../apps/api"
python3 -m pip install -e '.[test]'
export H4_CREATE_TABLES=1
if [ -z "${H4_TENANTS:-}" ]; then
  echo 'Set H4_TENANTS with hashes from scripts/bootstrap_keys.py before starting.' >&2
  exit 1
fi
exec python3 -m uvicorn energypilot.app:app --host 127.0.0.1 --port 8000 --reload
