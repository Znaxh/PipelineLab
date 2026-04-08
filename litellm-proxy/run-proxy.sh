#!/usr/bin/env bash
# Run LiteLLM in "config file only" mode. Unsets DB env vars so the proxy
# does not require Prisma (avoids conflicts with PipelineLab's DATABASE_URL).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

if [[ ! -d .venv ]]; then
  echo "Run: uv venv && uv sync" >&2
  exit 1
fi

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

unset DATABASE_URL DIRECT_URL DATABASE_HOST DATABASE_USERNAME DATABASE_PASSWORD DATABASE_NAME DATABASE_SCHEMA || true

: "${LITELLM_MASTER_KEY:?Set LITELLM_MASTER_KEY in litellm-proxy/.env}"

PORT="${PORT:-4000}"
exec .venv/bin/litellm --config config.yaml --port "$PORT" "$@"
