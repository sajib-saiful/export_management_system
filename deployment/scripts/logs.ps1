param(
  [ValidateSet("all", "db", "backend", "frontend")]
  [string]$Service = "all",
  [switch]$Follow
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

$args = @("--env-file", $envFile, "-f", $compose, "logs")
if ($Follow) { $args += "-f" }
if ($Service -ne "all") { $args += $Service }

docker compose @args
