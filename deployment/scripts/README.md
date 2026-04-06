# Scripts Reference (PowerShell)

Run scripts from project root:

```powershell
powershell -ExecutionPolicy Bypass -File deployment\scripts\<script>.ps1 ...
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

## Linux (bash) scripts

Make scripts executable (from project root):

```bash
chmod +x deployment/scripts/*.sh
```

Examples:
- Start all: `deployment/scripts/up.sh all` (build: `BUILD=1 deployment/scripts/up.sh all`)
- Start DB only: `deployment/scripts/up.sh db`
- Logs: `deployment/scripts/logs.sh all` (non-follow: `FOLLOW=0 deployment/scripts/logs.sh all`)
- Restart backend: `deployment/scripts/task.sh restart-backend`
- Stop: `deployment/scripts/down.sh 0`
- Stop + remove volumes: `deployment/scripts/down.sh 1`

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

## Utility tasks

- Health:
  - `deployment\scripts\task.ps1 -Action health`
- Rebuild all:
  - `deployment\scripts\task.ps1 -Action rebuild`
- Restart backend:
  - `deployment\scripts\task.ps1 -Action restart-backend`
- Restart frontend:
  - `deployment\scripts\task.ps1 -Action restart-frontend`
