@echo off
echo ================================
echo Smart Revenue Leakage Advisor
echo ================================
echo.

echo Starting Backend Server...
cd backend
start cmd /k "python main.py"
cd ..

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo ================================
echo System Starting...
echo ================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Press any key to exit...
pause > nul
