# One-time setup: register the daily 01:00 pipeline task in Windows Task Scheduler.
# Run: powershell -NoProfile -ExecutionPolicy Bypass -File "src\register_task.ps1"
# NOTE: no non-ASCII literals in this file — PowerShell 5.1 may read .ps1 as ANSI
# and corrupt them. Paths are derived from this script's location at runtime.

$nightly = Join-Path $PSScriptRoot "nightly.ps1"
if (-not (Test-Path $nightly)) { throw "nightly.ps1 not found next to this script." }

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$nightly`""
$trigger = New-ScheduledTaskTrigger -Daily -At 1:00AM
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask -TaskName "FinanceAINote-Nightly" `
    -Action $action -Trigger $trigger -Settings $settings `
    -Description "Finance AI Note blog - daily 01:00 auto-publish pipeline (Claude Code headless, scoped permissions)" `
    -Force

Write-Host ""
Write-Host "Registered action path:"
(Get-ScheduledTask -TaskName "FinanceAINote-Nightly").Actions[0].Arguments
Write-Host "Next run:"
(Get-ScheduledTaskInfo -TaskName "FinanceAINote-Nightly").NextRunTime
