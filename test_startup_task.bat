@echo off
echo Testing ExternalAttacker-MCP Startup Task...
echo.

:: Check if the task exists
schtasks /query /tn "ExternalAttacker-MCP" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: The ExternalAttacker-MCP task does not exist.
    echo Please run create_startup_task.bat or create_startup_task.ps1 first.
    echo.
    pause
    exit /b 1
)

echo Starting the ExternalAttacker-MCP service...
echo.
echo NOTE: This will open a new PowerShell window running the service.
echo Press CTRL+C in that window to stop the service when testing is complete.
echo.

:: Run the task immediately
powershell.exe -Command "cd '%~dp0' && py ExternalAttacker-App.py"

echo.
echo If the service didn't start, check the README_STARTUP.md file for troubleshooting.
pause
