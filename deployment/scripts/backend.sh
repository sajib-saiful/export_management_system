#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
MESSAGE="${2:-new migration}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

if [[ -z "$ACTION" ]]; then
  echo "Usage: backend.sh <status|shell|logs|migrate|revision> [message]"
  exit 1
fi

case "$ACTION" in
  status)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" ps backend
    ;;
  shell)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec backend sh
    ;;
  logs)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" logs -f backend
    ;;
  migrate)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec backend alembic upgrade head
    ;;
  revision)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" exec backend alembic revision --autogenerate -m "$MESSAGE"
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
