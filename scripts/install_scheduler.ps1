param(
    [double]$IntervalHours = 24,
    [int]$MaxRunMinutes = 20,
    [string]$ConfigPath = "config.json",
    [string]$TaskName = "AutonomousWikiAgent"
)
$ErrorActionPreference = "Stop"
if ($IntervalHours -le 0) { throw "IntervalHours must be positive" }
$script = (Resolve-Path (Join-Path $PSScriptRoot "run_scheduled.ps1")).Path
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$config = (Resolve-Path (Join-Path $repo $ConfigPath)).Path
$uv = (Get-Command uv -ErrorAction Stop).Source
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`" -Config `"$config`" -UvPath `"$uv`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval ([TimeSpan]::FromHours($IntervalHours)) -RepetitionDuration ([TimeSpan]::FromDays(3650))
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::FromMinutes($MaxRunMinutes)) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Runs the autonomous wiki agent periodically." -Force | Out-Null
Write-Output "Registered $TaskName every $IntervalHours hour(s)."
