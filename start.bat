@echo off
REM HealTrack AI - Quick Start Script for Windows

echo.
echo ================================================
echo   HealTrack AI - Startup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [1/3] Starting Backend API Server...
echo        Port: 5000
start "HealTrack Backend" cmd /k "cd /d %cd%\backend && python app.py"
timeout /t 3 /nobreak

echo [2/3] Starting Frontend Dev Server...
echo        Port: 5173
start "HealTrack Frontend" cmd /k "cd /d %cd%\frontend && npm run dev"
timeout /t 2 /nobreak

echo.
echo ================================================
echo   All services started!
echo ================================================
echo.
echo   Frontend:  http://localhost:5173
echo   Backend:   http://localhost:5000
echo.
echo   ✓ Backend running
echo   ✓ Frontend running
echo.
echo   Open browser to http://localhost:5173
echo.
echo   Note: Close these windows to stop services
pause
