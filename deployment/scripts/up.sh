#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-all}" # all|db|backend|frontend
BUILD="${BUILD:-0}" # set BUILD=1 to build

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"
ENV_EXAMPLE="$ROOT_DIR/deployment/.env.example"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created deployment/.env from .env.example"
fi

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d)
if [[ "$BUILD" == "1" ]]; then
  ARGS+=(--build)
fi
if [[ "$SERVICE" != "all" ]]; then
  ARGS+=("$SERVICE")
fi

docker compose "${ARGS[@]}"
