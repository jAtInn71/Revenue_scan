@echo off
echo ================================================
echo   Starting Revenue Analysis System
echo ================================================
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo [WARNING] No .env file found in backend directory
    echo Creating .env from .env.example...
    copy backend\.env.example backend\.env
    echo.
    echo [ACTION REQUIRED] Please edit backend\.env and add your OpenAI API key
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

REM Check if OpenAI key is configured
findstr /C:"OPENAI_API_KEY=sk-" backend\.env >nul
if errorlevel 1 (
    echo [WARNING] OpenAI API key not configured
    echo.
    echo Please edit backend\.env and add your OpenAI API key:
    echo OPENAI_API_KEY=sk-your-actual-key-here
    echo.
    echo Get your key from: https://platform.openai.com/api-keys
    echo.
    pause
)

echo Starting Backend Server...
echo.
start "Revenue Analysis - Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 >nul

echo Starting Frontend Development Server...
echo.
start "Revenue Analysis - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo   Both servers are starting...
echo ================================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/api/docs
echo Frontend:     http://localhost:5173
echo.
echo Press any key to open the application in browser...
pause >nul

start http://localhost:5173

echo.
echo Servers are running. Close this window when done.
echo To stop servers, close their respective command windows.
pause
