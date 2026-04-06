#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

if [[ -z "$ACTION" ]]; then
  echo "Usage: task.sh <health|rebuild|restart-backend|restart-frontend>"
  exit 1
fi

case "$ACTION" in
  health)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" ps
    ;;
  rebuild)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" up -d --build
    ;;
  restart-backend)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" restart backend
    ;;
  restart-frontend)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE" restart frontend
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
