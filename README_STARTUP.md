# ExternalAttacker-MCP Startup Configuration

This document provides instructions for setting up the ExternalAttacker-MCP to run automatically at system startup on Windows.

## Available Startup Methods

Three scripts are provided to help you configure the automatic startup:

1. **BAT Script** - Traditional Windows batch file (scheduled task)
2. **PowerShell Script** - Modern PowerShell approach (scheduled task, recommended)
3. **Startup Shortcut** - Simple startup folder shortcut (user login only)

The first two methods create a Windows scheduled task that runs when your computer starts, while the shortcut method runs the service when you log in.

## Method 1: Using the Batch File

1. **Right-click** on `create_startup_task.bat` and select **Run as administrator**
2. A command prompt window will open and create the scheduled task
3. Press any key to close when finished

## Method 2: Using PowerShell (Recommended)

1. **Right-click** on `create_startup_task.ps1` and select **Run with PowerShell**
2. If prompted about execution policy, choose **Yes** to continue
3. The script will create a scheduled task with elevated privileges
4. Press any key to close when finished

## Method 3: Using Startup Folder Shortcut

This method is simpler but only runs when a user logs in:

1. **Right-click** on `create_startup_shortcut.ps1` and select **Run with PowerShell**
2. The script will create a shortcut in your Windows Startup folder
3. To remove this startup item, simply delete the shortcut from your Startup folder

## Manual Method

If you prefer to set up the task manually:

1. Open **Task Scheduler** (search for it in the Start menu)
2. Click **Create Basic Task**
3. Name it "ExternalAttacker-MCP" and click Next
4. Select **When the computer starts** and click Next
5. Select **Start a program** and click Next
6. Browse to find PowerShell.exe (typically in C:\Windows\System32\WindowsPowerShell\v1.0)
7. In the **Add arguments** field, enter:
   ```
   -Command "cd 'C:\Users\cmndcntrl\.code\ai-test\vercel-app\app\ExternalAttacker-MCP'; py ExternalAttacker-App.py"
   ```
8. Click Next and then Finish

## Verifying the Task

To verify the task was created:

1. Open **Task Scheduler**
2. Look for "ExternalAttacker-MCP" in the task list
3. Right-click and select **Properties** to view or modify settings

## Removing the Task

If you need to remove the automatic startup:

1. Open **Task Scheduler**
2. Find "ExternalAttacker-MCP" in the task list
3. Right-click and select **Delete**

## Testing Your Configuration

To test that your startup configuration works correctly without rebooting:

1. **Using BAT script**: Run `test_startup_task.bat`
2. **Using PowerShell**: Run `test_startup_task.ps1`

These test scripts will verify that the scheduled task exists and then run the service directly. Press CTRL+C to stop the service after testing.

## Troubleshooting

If the service doesn't start automatically:

1. Check if Python is in your system PATH
2. Make sure the script path is correct in the task properties
3. Examine the Windows Event Logs for any errors
4. Try running the script manually to check for issues
5. Check task security settings if running with administrator privileges
