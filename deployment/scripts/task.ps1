param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("health", "rebuild", "restart-backend", "restart-frontend")]
  [string]$Action
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

switch ($Action) {
  "health" {
    docker compose --env-file $envFile -f $compose ps
  }
  "rebuild" {
    docker compose --env-file $envFile -f $compose up -d --build
  }
  "restart-backend" {
    docker compose --env-file $envFile -f $compose restart backend
  }
  "restart-frontend" {
    docker compose --env-file $envFile -f $compose restart frontend
  }
}
