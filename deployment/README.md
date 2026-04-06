# Deployment Guide

All container deployment assets are centralized in this `deployment/` directory.

## Files

- `docker-compose.yml` -> full stack deployment (PostgreSQL + backend + frontend)
- `.env.example` -> deployment environment template
- `.dockerignore` -> build context exclusions
- `docker/backend.Dockerfile` -> backend container image
- `docker/frontend.Dockerfile` -> frontend container image
- `scripts/` -> operational scripts for DB/backend/frontend tasks

## Quick Start

From repository root:

```bash
copy deployment\.env.example deployment\.env
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build
```

Services:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## DB Deployment Best Practices Used

- Official `postgres:16` image
- Named volume (`ems_pg_data`) for persistent data
- Healthcheck with `pg_isready`
- Environment-based configuration
- `restart: unless-stopped` for resilience

## Notes

- Keep strong values for `POSTGRES_PASSWORD` and `SECRET_KEY` in `deployment/.env`.
- For production, do not expose `5432` publicly unless needed.
- Script usage reference: `deployment/scripts/README.md`

## Create Image from Running Container

Use this when you need a quick snapshot image from a live container:

```bash
docker ps
docker commit ems_backend ems/backend:snapshot-v1
docker commit ems_frontend ems/frontend:snapshot-v1
docker commit ems_db ems/postgres:snapshot-v1
docker images
```

Optional archive:

```bash
docker save -o ems-backend-snapshot.tar ems/backend:snapshot-v1
docker load -i ems-backend-snapshot.tar
```

Best practice:
- Prefer reproducible image builds via `Dockerfile` and `docker compose build`.
- Keep `docker commit` for emergency snapshots, debugging, or temporary handoff.
