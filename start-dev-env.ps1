#!/usr/bin/env pwsh
# ==========================================================
#    Complete Development Environment Launcher (PowerShell)
#    For SMD Syllabus Management System
# ==========================================================

$ErrorActionPreference = "Continue"

Clear-Host

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  SMD - SYLLABUS MANAGEMENT DEVELOPMENT ENVIRONMENT" -ForegroundColor Cyan
Write-Host "  Complete Setup & Run Script (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Select what you want to do:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1 | Run BACKEND only (FastAPI @ http://localhost:8000)" -ForegroundColor White
Write-Host "  2 | Run FRONTEND only (Lecturer Web @ http://localhost:3000)" -ForegroundColor White
Write-Host "  3 | Run FRONTEND ADMIN (Admin Web @ http://localhost:3001)" -ForegroundColor White
Write-Host "  4 | Run Backend + Lecturer Frontend (in separate windows)" -ForegroundColor White
Write-Host "  5 | Run ALL (Backend + Lecturer + Admin in separate windows)" -ForegroundColor White
Write-Host "  6 | Install/Update Python Dependencies" -ForegroundColor White
Write-Host "  7 | Check System Health" -ForegroundColor White
Write-Host "  8 | Kill all running servers (ports 8000, 3000, 3001)" -ForegroundColor White
Write-Host "  0 | Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice [0-8]"

$scriptPath = $PSScriptRoot

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "[INFO] Starting Backend Server on port 8000..." -ForegroundColor Green
        Write-Host ""
        Set-Location "$scriptPath\backend"
        & python -m uvicorn app.main:app --reload --port 8000
    }
    "2" {
        Write-Host ""
        Write-Host "[INFO] Starting Lecturer Web on port 3000..." -ForegroundColor Green
        Write-Host ""
        Set-Location "$scriptPath\frontend\lecturer-web"
        & python -m http.server 3000
    }
    "3" {
        Write-Host ""
        Write-Host "[INFO] Starting Admin Web on port 3001..." -ForegroundColor Green
        Write-Host ""
        Set-Location "$scriptPath\frontend\admin-web"
        & python -m http.server 3001
    }
    "4" {
        Write-Host ""
        Write-Host "[INFO] Starting Backend + Lecturer Web in separate windows..." -ForegroundColor Green
        Write-Host ""
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$scriptPath\backend'; python -m uvicorn app.main:app --reload --port 8000`""
        Start-Sleep -Seconds 2
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$scriptPath\frontend\lecturer-web'; python -m http.server 3000`""
        Write-Host ""
        Write-Host "[READY]" -ForegroundColor Green
        Write-Host "  - Backend: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "  - Frontend: http://localhost:3000/home.html" -ForegroundColor Cyan
        Write-Host ""
    }
    "5" {
        Write-Host ""
        Write-Host "[INFO] Starting ALL services (Backend + Lecturer + Admin)..." -ForegroundColor Green
        Write-Host ""
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$scriptPath\backend'; python -m uvicorn app.main:app --reload --port 8000`""
        Start-Sleep -Seconds 2
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$scriptPath\frontend\lecturer-web'; python -m http.server 3000`""
        Start-Sleep -Seconds 1
        Start-Process pwsh -ArgumentList "-NoExit -Command `"cd '$scriptPath\frontend\admin-web'; python -m http.server 3001`""
        Write-Host ""
        Write-Host "[READY]" -ForegroundColor Green
        Write-Host "  - Backend: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "  - Lecturer Web: http://localhost:3000/home.html" -ForegroundColor Cyan
        Write-Host "  - Admin Web: http://localhost:3001" -ForegroundColor Cyan
        Write-Host ""
    }
    "6" {
        Write-Host ""
        Write-Host "[INFO] Installing Python dependencies..." -ForegroundColor Green
        Write-Host ""
        Set-Location "$scriptPath\backend"
        & pip install -r requirements.txt
        Write-Host ""
        Write-Host "[DONE] Dependencies installed!" -ForegroundColor Green
        Write-Host ""
    }
    "7" {
        Write-Host ""
        Write-Host "[INFO] Running system health check..." -ForegroundColor Green
        Write-Host ""
        Set-Location "$scriptPath"
        & python check_health.py
        Write-Host ""
    }
    "8" {
        Write-Host ""
        Write-Host "[INFO] Killing all servers on ports 8000, 3000, 3001..." -ForegroundColor Green
        Write-Host ""
        $processes = @(
            (netstat -ano | Select-String ":8000.*LISTENING" | ForEach-Object { $_ -replace '.*LISTENING\s+(\d+).*', '$1' }),
            (netstat -ano | Select-String ":3000.*LISTENING" | ForEach-Object { $_ -replace '.*LISTENING\s+(\d+).*', '$1' }),
            (netstat -ano | Select-String ":3001.*LISTENING" | ForEach-Object { $_ -replace '.*LISTENING\s+(\d+).*', '$1' })
        )
        
        foreach ($pid in $processes) {
            if ($pid) {
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                Write-Host "  ✓ Killed process $pid" -ForegroundColor Yellow
            }
        }
        Write-Host ""
        Write-Host "[DONE] All servers stopped!" -ForegroundColor Green
        Write-Host ""
    }
    "0" {
        Write-Host ""
        Write-Host "[INFO] Exiting..." -ForegroundColor Yellow
        Write-Host ""
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "[ERROR] Invalid choice. Please try again." -ForegroundColor Red
        Write-Host ""
        Start-Sleep -Seconds 2
    }
}

Read-Host "Press Enter to continue"
