@echo off
REM ==========================================================
REM    Complete Development Environment Launcher
REM    For SMD Syllabus Management System
REM ==========================================================

cd /d "%~dp0"
cls

echo.
echo ============================================================
echo.  SMD - SYLLABUS MANAGEMENT DEVELOPMENT ENVIRONMENT
echo.  Complete Setup & Run Script
echo.
echo ============================================================
echo.
echo Select what you want to do:
echo.
echo   1 ^| Run BACKEND only (FastAPI @ http://localhost:8000)
echo   2 ^| Run FRONTEND only (Lecturer Web @ http://localhost:3000)
echo   3 ^| Run FRONTEND ADMIN (Admin Web @ http://localhost:3001)
echo   4 ^| Run Backend + Lecturer Frontend
echo   5 ^| Run ALL (Backend + Lecturer + Admin)
echo   6 ^| Install/Update Python Dependencies
echo   7 ^| Check System Health
echo   8 ^| Kill all running servers (ports 8000, 3000, 3001)
echo   0 ^| Exit
echo.

set /p choice="Enter your choice [0-8]: "

if "%choice%"=="1" (
    echo.
    echo [INFO] Starting Backend Server on port 8000...
    echo.
    cd backend
    call ..\venv\Scripts\activate.bat 2>nul || python -m venv ..\venv && call ..\venv\Scripts\activate.bat
    python -m uvicorn app.main:app --reload --port 8000
) else if "%choice%"=="2" (
    echo.
    echo [INFO] Starting Lecturer Web on port 3000...
    echo.
    cd frontend\lecturer-web
    python -m http.server 3000
) else if "%choice%"=="3" (
    echo.
    echo [INFO] Starting Admin Web on port 3001...
    echo.
    cd frontend\admin-web
    python -m http.server 3001
) else if "%choice%"=="4" (
    echo.
    echo [INFO] Starting Backend + Lecturer Web in 2 windows...
    echo.
    start cmd /k "cd /d %cd%\backend && python -m uvicorn app.main:app --reload --port 8000"
    timeout /t 2 /nobreak
    start cmd /k "cd /d %cd%\frontend\lecturer-web && python -m http.server 3000"
    echo.
    echo [READY] 
    echo   - Backend: http://localhost:8000/docs
    echo   - Frontend: http://localhost:3000/home.html
    echo.
) else if "%choice%"=="5" (
    echo.
    echo [INFO] Starting ALL services (Backend + Lecturer + Admin)...
    echo.
    start cmd /k "cd /d %cd%\backend && python -m uvicorn app.main:app --reload --port 8000"
    timeout /t 2 /nobreak
    start cmd /k "cd /d %cd%\frontend\lecturer-web && python -m http.server 3000"
    timeout /t 1 /nobreak
    start cmd /k "cd /d %cd%\frontend\admin-web && python -m http.server 3001"
    echo.
    echo [READY]
    echo   - Backend: http://localhost:8000/docs
    echo   - Lecturer Web: http://localhost:3000/home.html
    echo   - Admin Web: http://localhost:3001
    echo.
) else if "%choice%"=="6" (
    echo.
    echo [INFO] Installing Python dependencies...
    echo.
    cd backend
    pip install -r requirements.txt
    echo.
    echo [DONE] Dependencies installed!
    echo.
) else if "%choice%"=="7" (
    echo.
    echo [INFO] Running system health check...
    echo.
    python check_health.py
    echo.
) else if "%choice%"=="8" (
    echo.
    echo [INFO] Killing all servers on ports 8000, 3000, 3001...
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /pid %%a /f 2>nul
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /pid %%a /f 2>nul
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do taskkill /pid %%a /f 2>nul
    echo.
    echo [DONE] All servers stopped!
    echo.
) else if "%choice%"=="0" (
    echo.
    echo [INFO] Exiting...
    echo.
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice. Please try again.
    echo.
    timeout /t 2 /nobreak
    goto start
)

pause
