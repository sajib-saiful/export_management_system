#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
PATH_ARG="${2:-}"

if [[ -z "$ACTION" ]]; then
  echo "Usage: ./db.sh <status|psql|backup|restore|reset> [path]"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deployment/docker-compose.yml"
ENV_FILE="$ROOT_DIR/deployment/.env"

case "$ACTION" in
  status)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps db
    ;;
  psql)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec db psql -U postgres -d ems_db
    ;;
  backup)
    if [[ -z "$PATH_ARG" ]]; then echo "Provide path, e.g. ./ems_backup.sql"; exit 1; fi
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T db pg_dump -U postgres -d ems_db > "$PATH_ARG"
    ;;
  restore)
    if [[ -z "$PATH_ARG" ]]; then echo "Provide path, e.g. ./ems_backup.sql"; exit 1; fi
    cat "$PATH_ARG" | docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T db psql -U postgres -d ems_db
    ;;
  reset)
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" down -v
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d db
    ;;
  *)
    echo "Unknown action: $ACTION"
    exit 1
    ;;
esac
