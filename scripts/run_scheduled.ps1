param(
    [string]$Config = "config.json",
    [string]$UvPath = "uv"
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$logDir = Join-Path $repo "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $logDir "scheduled-$stamp.log"
Push-Location $repo
try {
    & $UvPath run python run_agent.py --config $Config --once --scheduled *>&1 | Tee-Object -FilePath $log
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
