# EMS Deployment Instructions (Windows)

This guide covers local deployment on Windows:

1. PostgreSQL setup
2. Docker deployment
3. Create Docker images from running containers
4. Troubleshooting

---

## 1) PostgreSQL Setup

You can run PostgreSQL in two ways:

### Option A: Native PostgreSQL (local install)

1. Install PostgreSQL for Windows.
2. Create database:

```powershell
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

```powershell
copy deployment\.env.example deployment\.env
```

Update secure values in `deployment\.env`:
- `POSTGRES_PASSWORD`
- `SECRET_KEY`

### 2.2 Start full stack

```powershell
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build
```

Detached:

```powershell
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build -d
```

### 2.3 Access services

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

### 2.4 Optional PowerShell helper scripts

```powershell
deployment\scripts\up.ps1 -Build
deployment\scripts\logs.ps1 -Service all -Follow
deployment\scripts\down.ps1
deployment\scripts\down.ps1 -RemoveVolumes
```

---

## 3) Create Docker Images from Running Containers

Use this for snapshots/debugging (not primary build workflow).

### 3.1 List running containers

```powershell
docker ps
```

### 3.2 Commit containers to images

```powershell
docker commit ems_backend ems/backend:snapshot-v1
docker commit ems_frontend ems/frontend:snapshot-v1
docker commit ems_db ems/postgres:snapshot-v1
```

### 3.3 Verify

```powershell
docker images
```

### 3.4 Optional export/import

```powershell
docker save -o ems-backend-snapshot.tar ems/backend:snapshot-v1
docker load -i ems-backend-snapshot.tar
```

Best practice:
- Prefer `Dockerfile` + `docker compose build` for reproducible images.
- Use `docker commit` for temporary snapshot purposes.

---

## 4) Troubleshooting

### Docker commands fail

- Start Docker Desktop.
- Check:

```powershell
docker --version
docker compose version
```

### Port conflicts (`5432`, `8000`, `5173`)

- Stop conflicting apps or update `ports` in `deployment/docker-compose.yml`.

### Backend cannot connect to DB

```powershell
deployment\scripts\db.ps1 -Action status
deployment\scripts\logs.ps1 -Service db -Follow
```

- Confirm `POSTGRES_*` values in `deployment\.env`.
- Backend DB host in Docker should be `db`, not `localhost`.

### Migrations not running

```powershell
deployment\scripts\backend.ps1 -Action migrate
deployment\scripts\backend.ps1 -Action logs
```

### Frontend loads but API fails

- Ensure `VITE_API_BASE_URL=http://localhost:8000` in `deployment\.env`.
- Check backend logs and browser network tab.

### Reset full stack

```powershell
deployment\scripts\down.ps1 -RemoveVolumes
deployment\scripts\up.ps1 -Build
```
