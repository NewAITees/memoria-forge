param([string]$TaskName = "AutonomousWikiAgent")
$ErrorActionPreference = "Stop"
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
Write-Output "Unregistered $TaskName."
