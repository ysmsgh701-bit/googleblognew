# Nightly blog pipeline runner — invoked by Windows Task Scheduler at 01:00 daily.
# Runs Claude Code headless with the pipeline prompt and logs the output.
# NOTE: no non-ASCII literals in this file — PowerShell 5.1 may read .ps1 as ANSI
# and corrupt them. The project root is derived from this script's location.

$ErrorActionPreference = "Continue"
# Keep Korean output from the headless run readable in the log file.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$root = Split-Path -Parent $PSScriptRoot   # src/ -> project root
Set-Location $root

$logDir = Join-Path $root "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir ("nightly-" + (Get-Date -Format "yyyy-MM-dd") + ".log")

"[START] $(Get-Date -Format o)" | Out-File $log -Encoding utf8

$prompt = Get-Content (Join-Path $root "src\nightly_prompt.md") -Raw -Encoding UTF8

# claude.ps1 shim lives in %APPDATA%\npm — resolve full path for the scheduler context.
# Permissions: acceptEdits + the scoped allowlist in .claude/settings.json.
# Anything outside the allowlist is denied and logged, not silently executed.
$claude = Join-Path $env:APPDATA "npm\claude.ps1"

# Pipe the prompt via stdin instead of an argument: embedded double quotes in the
# prompt can truncate argument passing to the native exe (caused the 07-18 failure).
# Retry once after 5 minutes on failure (covers transient API errors like 07-15).
$maxAttempts = 2
for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    "[ATTEMPT $attempt] $(Get-Date -Format o)" | Out-File $log -Append -Encoding utf8
    $prompt | & $claude -p --permission-mode acceptEdits 2>&1 |
        Out-File $log -Append -Encoding utf8
    if ($LASTEXITCODE -eq 0) { break }
    if ($attempt -lt $maxAttempts) { Start-Sleep -Seconds 300 }
}

"[END] $(Get-Date -Format o) exit=$LASTEXITCODE" | Out-File $log -Append -Encoding utf8
