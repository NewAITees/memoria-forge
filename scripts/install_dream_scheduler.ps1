param(
    [int]$IntervalMinutes = 60,
    [int]$MaxRunMinutes = 30,
    [string]$ConfigPath = "config.json",
    [string]$TaskName = "MemoriaForgeDreaming"
)
$ErrorActionPreference = "Stop"
if ($IntervalMinutes -lt 1) { throw "IntervalMinutes must be at least 1" }
if ($MaxRunMinutes -lt 1) { throw "MaxRunMinutes must be at least 1" }
$script = (Resolve-Path (Join-Path $PSScriptRoot "run_dream_scheduled.ps1")).Path
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$config = (Resolve-Path (Join-Path $repo $ConfigPath)).Path
$uv = (Get-Command uv -ErrorAction Stop).Source
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`" -Config `"$config`" -UvPath `"$uv`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval ([TimeSpan]::FromMinutes($IntervalMinutes)) -RepetitionDuration ([TimeSpan]::FromDays(3650))
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::FromMinutes($MaxRunMinutes)) -MultipleInstances IgnoreNew -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Processes one local memory Dreaming job without running the Wiki agent." -Force | Out-Null
Write-Output "Registered $TaskName every $IntervalMinutes minute(s)."
