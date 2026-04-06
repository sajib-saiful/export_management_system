#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
MESSAGE="${2:-new migration}"

if [[ -z "$ACTION" ]]; then
  echo "Usage: ./backend.sh <status|shell|logs|migrate|revision> [message]"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

case "$ACTION" in
  status) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps backend ;;
  shell) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec backend sh ;;
  logs) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs -f backend ;;
  migrate) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec backend alembic upgrade head ;;
  revision) docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec backend alembic revision --autogenerate -m "$MESSAGE" ;;
  *) echo "Unknown action: $ACTION"; exit 1 ;;
esac
