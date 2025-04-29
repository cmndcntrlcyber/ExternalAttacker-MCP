# PowerShell script to test the ExternalAttacker-MCP startup task
Write-Host "Testing ExternalAttacker-MCP Startup Task..." -ForegroundColor Cyan
Write-Host ""

# Get the current script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if the task exists
try {
    $task = Get-ScheduledTask -TaskName "ExternalAttacker-MCP" -ErrorAction Stop
    Write-Host "Task found. Status: $($task.State)" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: The ExternalAttacker-MCP task does not exist." -ForegroundColor Red
    Write-Host "Please run create_startup_task.bat or create_startup_task.ps1 first." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "Starting the ExternalAttacker-MCP service..." -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: This will run the service in the current window." -ForegroundColor Yellow
Write-Host "Press CTRL+C to stop the service when testing is complete." -ForegroundColor Yellow
Write-Host ""

# Run the python script directly
try {
    Set-Location $scriptPath
    py ExternalAttacker-App.py
}
catch {
    Write-Host "Error running the service: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "If the service didn't start, check the README_STARTUP.md file for troubleshooting." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
