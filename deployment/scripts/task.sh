#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
if [[ -z "$ACTION" ]]; then
  echo "Usage: ./task.sh <health|rebuild|restart-backend|restart-frontend>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

case "$ACTION" in
  health)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
    ;;
  rebuild)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --build
    ;;
  restart-backend)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" restart backend
    ;;
  restart-frontend)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" restart frontend
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
