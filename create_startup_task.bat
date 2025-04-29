@echo off
echo Creating Windows startup task for ExternalAttacker-MCP...

:: Create scheduled task that runs on startup
schtasks /create /tn "ExternalAttacker-MCP" /tr "powershell.exe -Command \"cd '%~dp0'; py ExternalAttacker-App.py\"" /sc onstart /ru "%USERNAME%" /f

echo.
echo Task created successfully!
echo Name: ExternalAttacker-MCP
echo Trigger: At system startup
echo Action: Run the ExternalAttacker-App.py Python script
echo.
echo You can manage this task in the Windows Task Scheduler
pause
