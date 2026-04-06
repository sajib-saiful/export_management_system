# Export Management System (EMS)

Production-ready local SaaS starter for export management with:
- Multi-tenant isolation by `company_id`
- JWT auth + bcrypt password hashing
- RBAC permission checks for module CRUD
- Per-role permission profiles (Admin vs Staff)
- Dynamic FOB/CFR/CPT calculation engine
- Product/Supplier/Buyer/Cost Head CRUD + price history
- Reports API + frontend PDF export

## Project Structure

```text
backend/
  app/
    main.py
    core/
    models/
    schemas/
    api/
    services/
    db/
    utils/
  alembic/
  requirements.txt
  .env
frontend/
  src/
    pages/
    components/
    services/
  package.json
```

## PostgreSQL Setup

1. Install PostgreSQL.
2. Create DB:
   - `createdb ems_db`

## Backend Setup

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Database Schema

Implemented with Alembic migration:
- `companies`, `users`, `roles`, `permissions`, `role_permissions`
- `products`, `product_prices`, `suppliers`, `buyers`
- `cost_heads`, `calculations`, `cost_entries`

Migration file:
- `backend/alembic/versions/0001_initial.py`
- `backend/alembic/versions/0002_rbac_per_role_permissions.py`

## Seed Data

- Roles: `Admin`, `Staff`
- Permissions: role-specific permission profiles for each module
- Default company cost heads auto-created on register:
  - Packing (FOB)
  - Transport (FOB)
  - Shipping (CFR)
  - Air Freight (CPT)

## Deployment

All Docker and deployment configuration is now centralized in `deployment/`.

Deployment docs:
- `deployment/README.md`
- `deployment/scripts/README.md`
- `DEPLOYMENT_WINDOWS.md`
- `DEPLOYMENT_LINUX.md`

### Quick Docker Run (Recommended)

From project root (Windows PowerShell):

```bash
copy deployment\.env.example deployment\.env
docker compose --env-file deployment/.env -f deployment/docker-compose.yml up --build
```

Endpoints:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

### Run with Deployment Scripts

Use PowerShell helper scripts from project root:

```powershell
deployment\scripts\up.ps1 -Build
```

Common commands:
- Start all services: `deployment\scripts\up.ps1 -Build`
- Start DB only: `deployment\scripts\up.ps1 -Service db`
- View logs: `deployment\scripts\logs.ps1 -Service all -Follow`
- Stop services: `deployment\scripts\down.ps1`
- Stop + remove DB volume: `deployment\scripts\down.ps1 -RemoveVolumes`

Service-specific tasks:
- DB backup: `deployment\scripts\db.ps1 -Action backup -Path .\ems_backup.sql`
- DB restore: `deployment\scripts\db.ps1 -Action restore -Path .\ems_backup.sql`
- Backend migration: `deployment\scripts\backend.ps1 -Action migrate`
- Frontend build: `deployment\scripts\frontend.ps1 -Action npm-build`

### Create Docker Image from Running Container

After deployment is running, you can create a reusable image snapshot from a live container using `docker commit`.

1. Check running containers:

```bash
docker ps
```

2. Commit container to a new image:

```bash
docker commit ems_backend ems/backend:snapshot-v1
docker commit ems_frontend ems/frontend:snapshot-v1
docker commit ems_db ems/postgres:snapshot-v1
```

3. Verify images:

```bash
docker images
```

4. Optional export/import:

```bash
docker save -o ems-backend-snapshot.tar ems/backend:snapshot-v1
docker load -i ems-backend-snapshot.tar
```

Best practice note:
- Prefer `Dockerfile` + `docker compose build` for reproducible builds.
- Use `docker commit` mainly for debugging snapshots or quick backups.

## Core API Endpoints

Auth:
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/auth/permissions`

Products:
- `GET/POST /api/v1/products`
- `PUT/DELETE /api/v1/products/{id}`
- `POST /api/v1/products/price-history`

Suppliers:
- `GET/POST /api/v1/suppliers`
- `PUT/DELETE /api/v1/suppliers/{id}`

Buyers:
- `GET/POST /api/v1/buyers`
- `PUT/DELETE /api/v1/buyers/{id}`

Cost Heads:
- `GET/POST /api/v1/cost-heads`
- `PUT/DELETE /api/v1/cost-heads/{id}`

Calculations:
- `POST /api/v1/calculations`
- `GET /api/v1/calculations`
- `GET /api/v1/calculations/{id}`

Reports:
- `GET /api/v1/reports/price-history`

## Sample API Calls

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"company_name\":\"Acme Export\",\"full_name\":\"Admin User\",\"email\":\"admin@acme.com\",\"password\":\"StrongPass123\"}"
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@acme.com\",\"password\":\"StrongPass123\"}"
```

Create Product:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/products \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Rice\",\"category\":\"Food\",\"grade\":\"A\",\"unit\":\"kg\"}"
```

Create Calculation:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/calculations \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"product_id\":1,\"entries\":[{\"cost_head_id\":1,\"amount\":10},{\"cost_head_id\":2,\"amount\":20},{\"cost_head_id\":3,\"amount\":15},{\"cost_head_id\":4,\"amount\":25}]}"
```

## Security Notes

- Passwords are hashed with bcrypt.
- JWT token required for protected endpoints.
- SQLAlchemy ORM protects against SQL injection in query construction.
- Every business query is filtered by authenticated user `company_id` for tenant isolation.
