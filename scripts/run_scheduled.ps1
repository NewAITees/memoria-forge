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
$log = Join-Path $logDir "scheduled-$stamp.log"
Push-Location $repo
try {
    $configFile = (Resolve-Path $Config).Path
    $configData = Get-Content -LiteralPath $configFile -Raw | ConvertFrom-Json
    $vaultValue = [string]$configData.vault_path
    if ([IO.Path]::IsPathRooted($vaultValue)) {
        $vault = (Resolve-Path $vaultValue).Path
    } else {
        $vault = (Resolve-Path (Join-Path $repo $vaultValue)).Path
    }

    function Get-MarkdownSnapshot([string]$Root) {
        @(Get-ChildItem -LiteralPath $Root -Recurse -File -Filter *.md | ForEach-Object {
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
            $relative = $_.FullName.Substring($Root.Length).TrimStart('\', '/')
            "$relative|$hash"
        } | Sort-Object)
    }

    $before = Get-MarkdownSnapshot $vault
    $output = @(& $UvPath run python run_agent.py --config $Config --once --scheduled *>&1 | Tee-Object -FilePath $log)
    $text = ($output | ForEach-Object { $_.ToString() }) -join "`n"
    $jsonStart = $text.IndexOf('{')
    if ($jsonStart -lt 0) {
        Add-Content -LiteralPath $log -Value "scheduler: no JSON result returned"
        exit 20
    }
    try {
        $result = $text.Substring($jsonStart) | ConvertFrom-Json
    } catch {
        Add-Content -LiteralPath $log -Value "scheduler: invalid JSON result: $($_.Exception.Message)"
        exit 21
    }
    $after = Get-MarkdownSnapshot $vault
    $changed = Compare-Object -ReferenceObject $before -DifferenceObject $after
    $successfulResults = @('success', 'expanded', 'expanded_and_improved')
    if ($result.result -notin $successfulResults) {
        Add-Content -LiteralPath $log -Value "scheduler: agent result '$($result.result)' is not a successful Wiki generation"
        exit 22
    }
    if ($null -eq $changed -or $changed.Count -eq 0) {
        Add-Content -LiteralPath $log -Value "scheduler: result was successful but no Markdown file was created or updated"
        exit 23
    }
    Add-Content -LiteralPath $log -Value "scheduler: verified $($changed.Count) Markdown file change(s)"
} finally {
    Pop-Location
}
