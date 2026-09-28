# Registers a Windows Task Scheduler task that runs the Django backup_db
# management command every 8 hours, even if the machine was asleep or the
# user wasn't logged in at the scheduled time.
#
# Run this ONCE (as Administrator) from the project root to install the task:
#   powershell -ExecutionPolicy Bypass -File scripts\windows\setup_backup_task.ps1
#
# To remove it later:
#   Unregister-ScheduledTask -TaskName "StaffixDBBackup" -Confirm:$false

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path "$PSScriptRoot\..\..").Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ManagePy = Join-Path $ProjectRoot "manage.py"

if (-not (Test-Path $Python)) {
    throw "Could not find virtual environment Python at $Python. Update this script if your venv path differs."
}

$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$ManagePy`" backup_db --include-media" -WorkingDirectory $ProjectRoot

# Runs immediately, then repeats every 8 hours indefinitely.
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 8) -RepetitionDuration ([TimeSpan]::MaxValue)

$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName "StaffixDBBackup" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Backs up the Staffix Django database and media files every 8 hours." -Force

Write-Host "Scheduled task 'StaffixDBBackup' installed. It will run every 8 hours, starting now."
