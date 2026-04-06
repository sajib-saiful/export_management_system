#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-all}"   # all|db|backend|frontend
FOLLOW="${2:-}"       # -f optional

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE" logs)
if [[ "$FOLLOW" == "-f" ]]; then
  ARGS+=(-f)
fi
if [[ "$SERVICE" != "all" ]]; then
  ARGS+=("$SERVICE")
fi

docker compose "${ARGS[@]}"
