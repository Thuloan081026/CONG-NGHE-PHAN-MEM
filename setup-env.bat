@echo off
REM Auto-activate virtual environment and set PYTHONPATH
REM Chạy file này để setup environment

cd /d "%~dp0"

echo.
echo ========================================
echo  Activating Virtual Environment...
echo ========================================
echo.

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found at .venv
    exit /b 1
)

REM Set PYTHONPATH globally
setx PYTHONPATH "%CD%\backend;%CD%"
echo [OK] PYTHONPATH set: %CD%\backend;%CD%

echo.
echo ========================================
echo  Environment Ready!
echo ========================================
echo.
echo Now you can run Python files from anywhere:
echo   python check_health.py
echo   python backend/create_test_users.py
echo.
pause
