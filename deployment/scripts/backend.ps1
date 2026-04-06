param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("status", "shell", "logs", "migrate", "revision")]
  [string]$Action,
  [string]$Message = "new migration"
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

switch ($Action) {
  "status" {
    docker compose --env-file $envFile -f $compose ps backend
  }
  "shell" {
    docker compose --env-file $envFile -f $compose exec backend sh
  }
  "logs" {
    docker compose --env-file $envFile -f $compose logs -f backend
  }
  "migrate" {
    docker compose --env-file $envFile -f $compose exec backend alembic upgrade head
  }
  "revision" {
    docker compose --env-file $envFile -f $compose exec backend alembic revision --autogenerate -m "$Message"
  }
}
