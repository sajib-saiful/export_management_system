#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

if [[ -z "$ACTION" ]]; then
  echo "Usage: frontend.sh <status|shell|logs|npm-install|npm-build>"
  exit 1
fi

case "$ACTION" in
  status)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" ps frontend
    ;;
  shell)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec frontend sh
    ;;
  logs)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" logs -f frontend
    ;;
  npm-install)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec frontend npm install
    ;;
  npm-build)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec frontend npm run build
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
