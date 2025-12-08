@echo off
echo ========================================
echo  Revenue Leakage System - Backend
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Starting backend server...
echo.
echo ========================================
echo  Backend running at:
echo  - http://localhost:8000
echo  - API Docs: http://localhost:8000/api/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
