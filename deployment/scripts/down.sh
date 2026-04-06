#!/usr/bin/env bash
set -euo pipefail

REMOVE_VOLUMES="${1:-}"  # -v optional

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE" down)
if [[ "$REMOVE_VOLUMES" == "-v" ]]; then
  ARGS+=(-v)
fi

docker compose "${ARGS[@]}"
