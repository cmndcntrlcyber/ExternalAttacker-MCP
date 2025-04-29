# PowerShell script to create a Windows startup task for ExternalAttacker-MCP
Write-Host "Creating Windows startup task for ExternalAttacker-MCP..." -ForegroundColor Cyan

# Get the current script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$appPath = Join-Path $scriptPath "ExternalAttacker-App.py"

# Create the action and trigger for the task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Command `"cd '$scriptPath'; py ExternalAttacker-App.py`""
$trigger = New-ScheduledTaskTrigger -AtStartup

# Register the scheduled task
Register-ScheduledTask -TaskName "ExternalAttacker-MCP" -Action $action -Trigger $trigger -RunLevel Highest -Force

Write-Host ""
Write-Host "Task created successfully!" -ForegroundColor Green
Write-Host "Name: ExternalAttacker-MCP" -ForegroundColor White
Write-Host "Trigger: At system startup" -ForegroundColor White
Write-Host "Action: Run the ExternalAttacker-App.py Python script" -ForegroundColor White
Write-Host ""
Write-Host "You can manage this task in the Windows Task Scheduler" -ForegroundColor Yellow
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
