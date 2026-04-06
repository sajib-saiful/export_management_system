#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-all}" # all|db|backend|frontend
FOLLOW="${FOLLOW:-1}" # set FOLLOW=0 for non-follow

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs)
if [[ "$FOLLOW" == "1" ]]; then
  ARGS+=(-f)
fi
if [[ "$SERVICE" != "all" ]]; then
  ARGS+=("$SERVICE")
fi

docker compose "${ARGS[@]}"
