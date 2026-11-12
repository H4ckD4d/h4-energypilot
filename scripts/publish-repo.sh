#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OWNER="H4ckD4d"
REPO="h4-energypilot"
gh auth status >/dev/null
LOGIN="$(gh api user --jq .login)"
if [ "$(printf '%s' "$LOGIN" | tr '[:upper:]' '[:lower:]')" != "$(printf '%s' "$OWNER" | tr '[:upper:]' '[:lower:]')" ]; then
  echo "Authenticated as $LOGIN; expected $OWNER. Refusing to publish." >&2
  exit 1
fi
cd "$ROOT"
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "Existing repository: https://github.com/$OWNER/$REPO — skipping to avoid overwriting."
  exit 0
fi
if [ ! -d .git ]; then
  git init -b main
fi
git add .
if ! git diff --cached --quiet; then
  git -c commit.gpgsign=false -c user.name='Chris Cruz' \
      -c user.email='65521295+H4ckD4d@users.noreply.github.com' \
      commit -m 'feat: launch trilingual H4 MVP with SEO and tenant-scoped API'
fi
gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push \
  --description='EnergyPilot open source MVP — Chris Cruz @h4ckd4d'
echo "Published: https://github.com/$OWNER/$REPO"
