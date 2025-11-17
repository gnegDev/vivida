@echo off
REM GBM Treatment Optimization API v3.0 - Windows Startup Script

echo ================================================================================
echo GBM TREATMENT OPTIMIZATION API v3.0
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Starting API server...
echo.
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

python app.py

pause
