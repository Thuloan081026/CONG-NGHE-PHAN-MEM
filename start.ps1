#!/usr/bin/env pwsh
# Complete Development Environment Launcher

param(
    [switch]$Full = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host ""
    Write-Host "COMPLETE ENVIRONMENT LAUNCHER" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\start-complete.ps1              - Menu mode" -ForegroundColor White
    Write-Host "  .\start-complete.ps1 -Full        - Start everything" -ForegroundColor White
    Write-Host "  .\start-complete.ps1 -Help        - Show help" -ForegroundColor White
    Write-Host ""
    exit 0
}

$workspaceRoot = Split-Path -Parent $PSCommandPath
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  COMPLETE DEVELOPMENT ENVIRONMENT LAUNCHER" -ForegroundColor Cyan
Write-Host "  SMD - Syllabus Management System" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activate venv
Write-Host "[STEP 0] Activating Virtual Environment..." -ForegroundColor Yellow
$venvActivate = Join-Path $workspaceRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
    Write-Host "  OK - Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "  ERROR - Virtual environment not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

if (-not $Full) {
    Write-Host "Select what to do:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1 | Setup Database + Seed Data" -ForegroundColor White
    Write-Host "  2 | Start Backend API only (port 8000)" -ForegroundColor White
    Write-Host "  3 | Start Frontend only (port 3000)" -ForegroundColor White
    Write-Host "  4 | Setup + Start Backend + Frontend (RECOMMENDED)" -ForegroundColor Green
    Write-Host "  5 | Setup Database Only" -ForegroundColor White
    Write-Host "  0 | Exit" -ForegroundColor White
    Write-Host ""
    $choice = Read-Host "Enter your choice"
} else {
    $choice = "4"
}

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "[SETUP] Running setup..." -ForegroundColor Yellow
        Set-Location $workspaceRoot
        python setup-complete.py
    }
    
    "2" {
        Write-Host ""
        Write-Host "[BACKEND] Starting FastAPI Server..." -ForegroundColor Yellow
        Set-Location (Join-Path $workspaceRoot "backend")
        Write-Host ""
        Write-Host "Backend: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
        python -m uvicorn app.main:app --reload --port 8000
    }
    
    "3" {
        Write-Host ""
        Write-Host "[FRONTEND] Starting Frontend Server..." -ForegroundColor Yellow
        Set-Location (Join-Path $workspaceRoot "frontend\lecturer-web")
        Write-Host ""
        Write-Host "Frontend: http://localhost:3000/home.html" -ForegroundColor Cyan
        Write-Host ""
        python -m http.server 3000
    }
    
    "4" {
        Write-Host ""
        Write-Host "[FULL SETUP] Setting up complete environment..." -ForegroundColor Yellow
        Write-Host ""
        
        Write-Host "  [1/3] Setting up database..." -ForegroundColor Yellow
        Write-Host ""
        Set-Location $workspaceRoot
        python setup-complete.py
        
        Write-Host ""
        Write-Host "  [2/3] Starting Backend API..." -ForegroundColor Yellow
        Write-Host ""
        
        $backendPath = Join-Path $workspaceRoot "backend"
        $backendCmd = "cd '$backendPath'; python -m uvicorn app.main:app --reload --port 8000"
        Start-Process pwsh -ArgumentList "-NoExit -Command `"$backendCmd`""
        
        Start-Sleep -Seconds 3
        
        Write-Host "  [3/3] Starting Frontend Server..." -ForegroundColor Yellow
        Write-Host ""
        
        $frontendPath = Join-Path $workspaceRoot "frontend\lecturer-web"
        $frontendCmd = "cd '$frontendPath'; python -m http.server 3000"
        Start-Process pwsh -ArgumentList "-NoExit -Command `"$frontendCmd`""
        
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  OK - EVERYTHING STARTED!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Access Points:" -ForegroundColor Cyan
        Write-Host "  Backend API:   http://localhost:8000/docs" -ForegroundColor White
        Write-Host "  Frontend Home: http://localhost:3000/home.html" -ForegroundColor White
        Write-Host ""
        
        Write-Host "Test Credentials:" -ForegroundColor Cyan
        Write-Host "  Email:    lecturer@test.com" -ForegroundColor White
        Write-Host "  Password: lecturer123" -ForegroundColor White
        Write-Host ""
        
        Write-Host "Other Accounts:" -ForegroundColor Cyan
        Write-Host "  Admin:    admin@smd.edu.vn / admin123" -ForegroundColor White
        Write-Host "  HOD:      hod@test.com / hod123" -ForegroundColor White
        Write-Host "  Student:  student@test.com / student123" -ForegroundColor White
        Write-Host ""
    }
    
    "5" {
        Write-Host ""
        Write-Host "[SETUP] Running setup only..." -ForegroundColor Yellow
        Set-Location $workspaceRoot
        python setup-complete.py
    }
    
    "0" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
