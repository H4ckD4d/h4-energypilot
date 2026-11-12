#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../site/dist"
python3 -m http.server 8080 --bind 127.0.0.1
