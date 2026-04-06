#!/usr/bin/env bash
set -euo pipefail

REMOVE_VOLUMES="${1:-0}" # pass 1 to remove volumes

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE_FILE" down)
if [[ "$REMOVE_VOLUMES" == "1" ]]; then
  ARGS+=(-v)
fi

docker compose "${ARGS[@]}"
