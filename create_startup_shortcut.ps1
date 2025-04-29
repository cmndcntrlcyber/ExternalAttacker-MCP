# PowerShell script to create a startup folder shortcut for ExternalAttacker-MCP
Write-Host "Creating Startup Folder Shortcut for ExternalAttacker-MCP..." -ForegroundColor Cyan

# Get the current script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$appPath = Join-Path $scriptPath "ExternalAttacker-App.py"

# Get the startup folder path
$startupFolder = [System.Environment]::GetFolderPath('Startup')
$shortcutPath = Join-Path $startupFolder "ExternalAttacker-MCP.lnk"

# Create a Windows Script Host object
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)

# Configure the shortcut
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-WindowStyle Hidden -Command `"cd '$scriptPath'; py ExternalAttacker-App.py`""
$Shortcut.WorkingDirectory = $scriptPath
$Shortcut.Description = "Start ExternalAttacker-MCP Security Scanner Service"
$Shortcut.IconLocation = "C:\Windows\System32\SHELL32.dll,76"  # Security shield icon
$Shortcut.WindowStyle = 7  # Minimized window

# Save the shortcut
$Shortcut.Save()

Write-Host ""
Write-Host "Shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $shortcutPath" -ForegroundColor White
Write-Host ""
Write-Host "This shortcut will start the ExternalAttacker-MCP service when you log in." -ForegroundColor Yellow
Write-Host "To disable automatic startup, simply delete the shortcut from the Startup folder." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
