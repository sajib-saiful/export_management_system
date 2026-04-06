#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
if [[ -z "$ACTION" ]]; then
  echo "Usage: ./frontend.sh <status|shell|logs|npm-install|npm-build>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

case "$ACTION" in
  status) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps frontend ;;
  shell) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec frontend sh ;;
  logs) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs -f frontend ;;
  npm-install) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec frontend npm install ;;
  npm-build) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec frontend npm run build ;;
  *) echo "Unknown action: $ACTION"; exit 1 ;;
esac
