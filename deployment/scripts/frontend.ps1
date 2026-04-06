param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("status", "shell", "logs", "npm-install", "npm-build")]
  [string]$Action
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

switch ($Action) {
  "status" {
    docker compose --env-file $envFile -f $compose ps frontend
  }
  "shell" {
    docker compose --env-file $envFile -f $compose exec frontend sh
  }
  "logs" {
    docker compose --env-file $envFile -f $compose logs -f frontend
  }
  "npm-install" {
    docker compose --env-file $envFile -f $compose exec frontend npm install
  }
  "npm-build" {
    docker compose --env-file $envFile -f $compose exec frontend npm run build
  }
}
