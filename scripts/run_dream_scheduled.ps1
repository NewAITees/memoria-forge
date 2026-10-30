param(
    [string]$Config = "config.json",
    [string]$UvPath = "uv"
)
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$logDir = Join-Path $repo "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $logDir "dream-$stamp.log"
$exitCode = 0
Push-Location $repo
try {
    $configFile = (Resolve-Path $Config).Path
    try {
        # Windows PowerShell 5.1 turns redirected native stderr into terminating ErrorRecords under Stop.
        $ErrorActionPreference = "Continue"
        $output = @(& $UvPath run python run_agent.py --config $configFile --dream-batch --dream-limit 10 *>&1 | Tee-Object -FilePath $log)
        $processExitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = "Stop"
    }
    if ($processExitCode -ne 0) {
        Add-Content -LiteralPath $log -Value "dream scheduler: worker process exited with code $processExitCode"
        $exitCode = $processExitCode
    } else {
        $text = ($output | ForEach-Object { $_.ToString() }) -join "`n"
        $jsonStart = $text.IndexOf('{')
        if ($jsonStart -lt 0) {
            Add-Content -LiteralPath $log -Value "dream scheduler: no JSON result returned"
            $exitCode = 30
        } else {
            try {
                $result = $text.Substring($jsonStart) | ConvertFrom-Json
                if ($result.result -notin @("completed", "idle")) {
                    Add-Content -LiteralPath $log -Value "dream scheduler: worker result '$($result.result)' (processed=$($result.processed_count), errors=$($result.error_count))"
                    $exitCode = 31
                } else {
                    Add-Content -LiteralPath $log -Value "dream scheduler: verified result '$($result.result)'"
                }
            } catch {
                Add-Content -LiteralPath $log -Value "dream scheduler: invalid JSON result: $($_.Exception.Message)"
                $exitCode = 32
            }
        }
    }
} catch {
    Add-Content -LiteralPath $log -Value "dream scheduler: $($_.Exception.Message)"
    $exitCode = 33
} finally {
    Pop-Location
}
exit $exitCode
