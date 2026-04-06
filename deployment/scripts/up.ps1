param(
  [ValidateSet("all", "db", "backend", "frontend")]
  [string]$Service = "all",
  [switch]$Build
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"
$envExample = Join-Path $root "deployment\.env.example"

if (!(Test-Path $envFile)) {
  Copy-Item $envExample $envFile
  Write-Host "Created deployment/.env from .env.example"
}

$args = @("--env-file", $envFile, "-f", $compose, "up", "-d")
if ($Build) { $args += "--build" }
if ($Service -ne "all") { $args += $Service }

docker compose @args
