param([string]$TaskName = "AutonomousWikiAgent")
$ErrorActionPreference = "Stop"
Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo | Select-Object TaskName,LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns
