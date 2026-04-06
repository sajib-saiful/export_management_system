 # EMS Deployment Instructions (Linux)

This guide covers local deployment on Linux:

1. PostgreSQL setup
2. Docker deployment
3. Create Docker images from running containers
4. Troubleshooting

---

## 1) PostgreSQL Setup

You can run PostgreSQL in two ways:

### Option A: Native PostgreSQL (local install)

1. Install PostgreSQL using your distro package manager.
2. Create database:

```bash
createdb ems_db
```

3. Backend connection string (native mode):

```text
postgresql+psycopg2://postgres:<password>@localhost:5432/ems_db
```

### Option B: PostgreSQL via Docker (recommended)

Use full Docker stack in section 2. Database is auto-created by compose using:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

---

## 2) Docker Deployment

All deployment assets are in `deployment/`.

### 2.1 Prepare environment

From project root:

```bash
cp deployment/.env.example deployment/.env
```

Update secure values in `deployment/.env`:
- `POSTGRES_PASSWORD`
- `SECRET_KEY`

### 2.2 Start full stack

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build
```

Detached:

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build -d
```

### 2.3 Access services

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

### 2.4 Useful direct commands

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml logs -f
docker compose --env-file deployment/.env -f deployment/docker-compose.yml down
docker compose --env-file deployment/.env -f deployment/docker-compose.yml down -v
```

### 2.5 Optional Linux helper scripts

From project root:

```bash
chmod +x deployment/scripts/*.sh
deployment/scripts/up.sh all
deployment/scripts/logs.sh all
deployment/scripts/task.sh restart-backend
deployment/scripts/down.sh 0
```

---

## 3) Create Docker Images from Running Containers

Use this for snapshots/debugging (not primary build workflow).

### 3.1 List running containers

```bash
docker ps
```

### 3.2 Commit containers to images

```bash
docker commit ems_backend ems/backend:snapshot-v1
docker commit ems_frontend ems/frontend:snapshot-v1
docker commit ems_db ems/postgres:snapshot-v1
```

### 3.3 Verify

```bash
docker images
```

### 3.4 Optional export/import

```bash
docker save -o ems-backend-snapshot.tar ems/backend:snapshot-v1
docker load -i ems-backend-snapshot.tar
```

Best practice:
- Prefer `Dockerfile` + `docker compose build` for reproducible images.
- Use `docker commit` for temporary snapshot purposes.

---

## 4) Troubleshooting

### Docker commands fail

- Ensure Docker Engine is running.
- Check:

```bash
docker --version
docker compose version
```

### Permission denied with Docker

Run with `sudo` or add current user to docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Port conflicts (`5432`, `8000`, `5173`)

- Stop conflicting services or update `ports` in `deployment/docker-compose.yml`.

### Backend cannot connect to DB

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml ps db
docker compose --env-file deployment/.env -f deployment/docker-compose.yml logs -f db
```

- Verify `POSTGRES_*` values in `deployment/.env`.
- Backend DB host in Docker should be `db`, not `localhost`.

### Migrations not running

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml exec backend alembic upgrade head
docker compose --env-file deployment/.env -f deployment/docker-compose.yml logs -f backend
```

### Frontend loads but API fails

- Ensure `VITE_API_BASE_URL=http://localhost:8000` in `deployment/.env`.
- Check browser network calls and backend logs.

### Reset full stack

```bash
docker compose --env-file deployment/.env -f deployment/docker-compose.yml down -v
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build -d
```
