@echo off
title Revenue Advisor - Application Launcher

echo ============================================================
echo               REVENUE ADVISOR - AI ANALYTICS
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] Creating Demo Users...
cd backend
python create_demo_user.py
cd ..
echo.

echo [2/3] Starting Backend Server...
start cmd /k "cd backend && title Backend Server && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul
echo.

echo [3/3] Starting Frontend Server...
start cmd /k "cd frontend && title Frontend Server && npm run dev"
timeout /t 3 /nobreak >nul
echo.

echo ============================================================
echo                   SERVERS RUNNING!
echo ============================================================
echo.
echo   Backend API:  http://localhost:8000
echo   Frontend:     http://localhost:5173
echo   API Docs:     http://localhost:8000/api/docs
echo.
echo   DEMO CREDENTIALS:
echo   ---------------------------------------------------------
echo   ADMIN      - admin@revenue.com     / admin123
echo   MANAGER    - manager@revenue.com   / manager123
echo   ANALYST    - analyst@revenue.com   / analyst123
echo.
echo   Press any key to close this window
echo   (Servers will continue running in separate windows)
echo ============================================================

pause >nul
