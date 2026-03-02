@echo off
REM ============================================
REM Windows Task Scheduler Setup
REM AI Employee - Silver Tier
REM ============================================

echo.
echo ========================================
echo   AI EMPLOYEE SCHEDULER SETUP
echo   Silver Tier - Windows Task Scheduler
echo ========================================
echo.

REM Get current directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%scripts\run_ai_employee.py"

REM Check if script exists
if not exist "%SCRIPT_PATH%" (
    echo [ERROR] Script not found: %SCRIPT_PATH%
    echo Please run this batch file from the project root directory.
    pause
    exit /b 1
)

echo [INFO] Script found: %SCRIPT_PATH%
echo.

REM Find Python executable
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

REM Get Python path
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"
echo [INFO] Python found: %PYTHON_PATH%
echo.

REM Task configuration
set "TASK_NAME=AI_Employee_Scheduler"
set "TASK_DESCRIPTION=Runs AI Employee orchestrator every 5 minutes"
set "SCHEDULE_INTERVAL=5"

echo ========================================
echo   TASK CONFIGURATION
echo ========================================
echo Task Name: %TASK_NAME%
echo Description: %TASK_DESCRIPTION%
echo Schedule: Every %SCHEDULE_INTERVAL% minutes
echo Script: %SCRIPT_PATH%
echo Python: %PYTHON_PATH%
echo.

echo [WARNING] This will create a scheduled task that runs every %SCHEDULE_INTERVAL% minutes.
echo [WARNING] The task will start automatically and run in the background.
echo.
set /p CONFIRM="Do you want to continue? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo [INFO] Setup cancelled by user
    pause
    exit /b 0
)

echo.
echo [INFO] Creating scheduled task...
echo.

REM Delete existing task if it exists
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Removing existing task...
    schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
)

REM Create the scheduled task
REM Run every 5 minutes, starting now
schtasks /Create ^
    /TN "%TASK_NAME%" ^
    /TR "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /SC MINUTE ^
    /MO %SCHEDULE_INTERVAL% ^
    /F ^
    /RL HIGHEST

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo [SUCCESS] Scheduled task created successfully!
    echo.
    echo Task Details:
    echo   Name: %TASK_NAME%
    echo   Schedule: Every %SCHEDULE_INTERVAL% minutes
    echo   Status: Enabled
    echo.
    echo The AI Employee will now run automatically every %SCHEDULE_INTERVAL% minutes.
    echo.
    echo To verify: schtasks /Query /TN "%TASK_NAME%"
    echo To disable: schtasks /Change /TN "%TASK_NAME%" /DISABLE
    echo To delete: schtasks /Delete /TN "%TASK_NAME%" /F
    echo.
    echo Check logs at: logs\actions.log
    echo.
) else (
    echo.
    echo [ERROR] Failed to create scheduled task
    echo.
    echo This might be due to:
    echo   1. Insufficient permissions (try running as Administrator)
    echo   2. Task Scheduler service not running
    echo   3. Invalid paths or configuration
    echo.
    echo Please check SCHEDULER_SETUP.md for manual setup instructions.
    echo.
)

pause
