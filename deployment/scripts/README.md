# Scripts Reference (PowerShell + Linux shell)

Run scripts from project root:

```powershell
powershell -ExecutionPolicy Bypass -File deployment\scripts\<script>.ps1 ...
```

Linux/macOS (bash):

```bash
chmod +x deployment/scripts/*.sh
./deployment/scripts/up.sh all --build
```

## Stack lifecycle

- Start all services:
  - `deployment\scripts\up.ps1 -Build`
- Start one service:
  - `deployment\scripts\up.ps1 -Service db`
- Stop services:
  - `deployment\scripts\down.ps1`
- Stop and remove data volume:
  - `deployment\scripts\down.ps1 -RemoveVolumes`
- View logs:
  - `deployment\scripts\logs.ps1 -Service all -Follow`

Linux equivalents:
- Start all services:
  - `./deployment/scripts/up.sh all --build`
- Start one service:
  - `./deployment/scripts/up.sh db`
- Stop services:
  - `./deployment/scripts/down.sh`
- Stop and remove data volume:
  - `./deployment/scripts/down.sh -v`
- View logs:
  - `./deployment/scripts/logs.sh all -f`

## Database tasks

- Status:
  - `deployment\scripts\db.ps1 -Action status`
- Open psql:
  - `deployment\scripts\db.ps1 -Action psql`
- Backup:
  - `deployment\scripts\db.ps1 -Action backup -Path .\ems_backup.sql`
- Restore:
  - `deployment\scripts\db.ps1 -Action restore -Path .\ems_backup.sql`
- Reset DB:
  - `deployment\scripts\db.ps1 -Action reset`

Linux equivalents:
- Status: `./deployment/scripts/db.sh status`
- Open psql: `./deployment/scripts/db.sh psql`
- Backup: `./deployment/scripts/db.sh backup ./ems_backup.sql`
- Restore: `./deployment/scripts/db.sh restore ./ems_backup.sql`
- Reset: `./deployment/scripts/db.sh reset`

## Backend tasks

- Status:
  - `deployment\scripts\backend.ps1 -Action status`
- Shell:
  - `deployment\scripts\backend.ps1 -Action shell`
- Logs:
  - `deployment\scripts\backend.ps1 -Action logs`
- Run migrations:
  - `deployment\scripts\backend.ps1 -Action migrate`
- New Alembic revision:
  - `deployment\scripts\backend.ps1 -Action revision -Message "add field"`

Linux equivalents:
- Status: `./deployment/scripts/backend.sh status`
- Shell: `./deployment/scripts/backend.sh shell`
- Logs: `./deployment/scripts/backend.sh logs`
- Migrate: `./deployment/scripts/backend.sh migrate`
- Revision: `./deployment/scripts/backend.sh revision "add field"`

## Frontend tasks

- Status:
  - `deployment\scripts\frontend.ps1 -Action status`
- Shell:
  - `deployment\scripts\frontend.ps1 -Action shell`
- Logs:
  - `deployment\scripts\frontend.ps1 -Action logs`
- Install packages:
  - `deployment\scripts\frontend.ps1 -Action npm-install`
- Build:
  - `deployment\scripts\frontend.ps1 -Action npm-build`

Linux equivalents:
- Status: `./deployment/scripts/frontend.sh status`
- Shell: `./deployment/scripts/frontend.sh shell`
- Logs: `./deployment/scripts/frontend.sh logs`
- Install: `./deployment/scripts/frontend.sh npm-install`
- Build: `./deployment/scripts/frontend.sh npm-build`

## Utility tasks

- Health:
  - `deployment\scripts\task.ps1 -Action health`
- Rebuild all:
  - `deployment\scripts\task.ps1 -Action rebuild`
- Restart backend:
  - `deployment\scripts\task.ps1 -Action restart-backend`
- Restart frontend:
  - `deployment\scripts\task.ps1 -Action restart-frontend`

Linux equivalents:
- Health: `./deployment/scripts/task.sh health`
- Rebuild all: `./deployment/scripts/task.sh rebuild`
- Restart backend: `./deployment/scripts/task.sh restart-backend`
- Restart frontend: `./deployment/scripts/task.sh restart-frontend`
