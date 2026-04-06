param(
  [switch]$RemoveVolumes
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $root "deployment\docker-compose.yml"
$envFile = Join-Path $root "deployment\.env"

$args = @("--env-file", $envFile, "-f", $compose, "down")
if ($RemoveVolumes) { $args += "-v" }

docker compose @args
