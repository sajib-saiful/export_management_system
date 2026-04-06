# EMS Deployment Instructions

This guide covers end-to-end local deployment for the Export Management System:

1. PostgreSQL setup
2. Docker deployment
3. Create Docker images from running containers
4. Troubleshooting

---

## 1) PostgreSQL Setup

You can run PostgreSQL in two ways:

### Option A: Native PostgreSQL (local install)

1. Install PostgreSQL.
2. Create database:

```bash
createdb ems_db
```

3. Use connection string for backend:

```text
postgresql+psycopg2://postgres:<password>@localhost:5432/ems_db
```

### Option B: PostgreSQL via Docker (recommended with full stack)

Use the Docker deployment below; DB is created automatically from:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

---

## 2) Docker Deployment

All deployment files are under `deployment/`.

### 2.1 Prepare environment

From project root:

```powershell
copy deployment\.env.example deployment\.env
```

Edit `deployment/.env` and set secure values:
- `POSTGRES_PASSWORD`
- `SECRET_KEY`

### 2.2 Start full stack

```powershell
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build
```

Or detached mode:

```powershell
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build -d
```

### 2.3 Access services

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

### 2.4 Useful script-based deployment commands

```powershell
deployment\scripts\up.ps1 -Build
deployment\scripts\logs.ps1 -Service all -Follow
deployment\scripts\down.ps1
deployment\scripts\down.ps1 -RemoveVolumes
```

---

## 3) Create Docker Images from Running Containers

Use this for quick snapshots (debugging or handoff), not as your primary build strategy.

### 3.1 Check running containers

```bash
docker ps
```

### 3.2 Commit containers into images

```bash
docker commit ems_backend ems/backend:snapshot-v1
docker commit ems_frontend ems/frontend:snapshot-v1
docker commit ems_db ems/postgres:snapshot-v1
```

### 3.3 Verify images

```bash
docker images
```

### 3.4 Export and import image (optional)

```bash
docker save -o ems-backend-snapshot.tar ems/backend:snapshot-v1
docker load -i ems-backend-snapshot.tar
```

### Best Practice

- Preferred: `Dockerfile` + `docker compose build` (reproducible).
- Use `docker commit` only for snapshots/emergency backup/debugging.

---

## 4) Troubleshooting

### Problem: `docker compose` command fails

- Ensure Docker Desktop is running.
- Check version:

```bash
docker --version
docker compose version
```

### Problem: Port already in use (`5432`, `8000`, `5173`)

- Identify process and stop it, or change port mappings in `deployment/docker-compose.yml`.

### Problem: Backend cannot connect to DB

- Check DB health:

```powershell
deployment\scripts\db.ps1 -Action status
deployment\scripts\logs.ps1 -Service db -Follow
```

- Verify `POSTGRES_*` values in `deployment/.env`.
- Confirm backend uses host `db` (inside compose network), not `localhost`.

### Problem: Migrations not applied

- Run migration task:

```powershell
deployment\scripts\backend.ps1 -Action migrate
```

- Recheck backend logs:

```powershell
deployment\scripts\backend.ps1 -Action logs
```

### Problem: Frontend opens but API calls fail

- Confirm backend URL in deployment env:
  - `VITE_API_BASE_URL=http://localhost:8000`
- Check browser network tab and backend logs.

### Problem: Need clean restart from scratch

```powershell
deployment\scripts\down.ps1 -RemoveVolumes
deployment\scripts\up.ps1 -Build
```

This removes PostgreSQL data volume and recreates everything.
