#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-all}"   # all|db|backend|frontend
BUILD="${2:-}"        # --build (optional)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"
ENV_EXAMPLE="$ROOT_DIR/deployment/.env.example"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created deployment/.env from .env.example"
fi

ARGS=(--env-file "$ENV_FILE" -f "$COMPOSE" up -d)
if [[ "$BUILD" == "--build" ]]; then
  ARGS+=(--build)
fi
if [[ "$SERVICE" != "all" ]]; then
  ARGS+=("$SERVICE")
fi

docker compose "${ARGS[@]}"
