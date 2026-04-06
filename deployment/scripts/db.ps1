param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("status", "psql", "backup", "restore", "reset")]
  [string]$Action,
  [string]$Path
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

switch ($Action) {
  "status" {
    docker compose --env-file $envFile -f $compose ps db
  }
  "psql" {
    docker compose --env-file $envFile -f $compose exec db psql -U postgres -d ems_db
  }
  "backup" {
    if (-not $Path) { throw "Provide -Path for backup file, e.g. .\ems_backup.sql" }
    docker compose --env-file $envFile -f $compose exec -T db pg_dump -U postgres -d ems_db > $Path
  }
  "restore" {
    if (-not $Path) { throw "Provide -Path for restore file, e.g. .\ems_backup.sql" }
    Get-Content $Path | docker compose --env-file $envFile -f $compose exec -T db psql -U postgres -d ems_db
  }
  "reset" {
    docker compose --env-file $envFile -f $compose down -v
    docker compose --env-file $envFile -f $compose up -d db
  }
}
