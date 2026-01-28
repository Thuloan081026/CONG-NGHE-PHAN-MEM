#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Complete Development Environment Launcher
    Starts Backend + Frontend + Seeds Data
    
.DESCRIPTION
    One-command setup and start for the entire development environment:
    - Backend API (FastAPI) on port 8000
    - Frontend (Lecturer Web) on port 3000
    - Sample data populated
    - Ready for login and testing
#>

param(
    [switch]$Full = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host ""
    Write-Host "📋 COMPLETE ENVIRONMENT LAUNCHER" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\start-complete.ps1              - Menu mode (select what to do)" -ForegroundColor White
    Write-Host "  .\start-complete.ps1 -Full        - Start everything (Backend + Frontend)" -ForegroundColor White
    Write-Host "  .\start-complete.ps1 -Help        - Show this help" -ForegroundColor White
    Write-Host ""
    exit 0
}

# Setup
$workspaceRoot = Split-Path -Parent $PSCommandPath
$env:PYTHONIOENCODING = "utf-8"

# Colors
$colors = @{
    Green  = [System.ConsoleColor]::Green
    Yellow = [System.ConsoleColor]::Yellow
    Red    = [System.ConsoleColor]::Red
    Cyan   = [System.ConsoleColor]::Cyan
}

function Write-ColorLine {
    param([string]$Text, [string]$Color)
    Write-Host $Text -ForegroundColor $Color
}

# Header
Write-Host ""
Write-ColorLine "╔═══════════════════════════════════════════════════════════════════════╗" $colors.Cyan
Write-ColorLine "║                                                                       ║" $colors.Cyan
Write-ColorLine "║     🚀 COMPLETE DEVELOPMENT ENVIRONMENT LAUNCHER                      ║" $colors.Cyan
Write-ColorLine "║        SMD - Syllabus Management System                               ║" $colors.Cyan
Write-ColorLine "║                                                                       ║" $colors.Cyan
Write-ColorLine "╚═══════════════════════════════════════════════════════════════════════╝" $colors.Cyan
Write-Host ""

# Activate venv
Write-ColorLine "[STEP 0] Activating Virtual Environment..." $colors.Yellow
$venvActivate = Join-Path $workspaceRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
    Write-ColorLine "  ✓ Virtual environment activated" $colors.Green
} else {
    Write-ColorLine "  ✗ Virtual environment not found" $colors.Red
    exit 1
}

Write-Host ""

if (-not $Full) {
    # Menu mode
    Write-ColorLine "Select what to do:" $colors.Yellow
    Write-Host ""
    Write-Host "  1 | Setup Database + Seed Data" -ForegroundColor White
    Write-Host "  2 | Start Backend API only (port 8000)" -ForegroundColor White
    Write-Host "  3 | Start Frontend only (port 3000)" -ForegroundColor White
    Write-Host "  4 | Setup + Start Backend + Frontend (RECOMMENDED)" -ForegroundColor Green
    Write-Host "  5 | Setup Database Only" -ForegroundColor White
    Write-Host "  0 | Exit" -ForegroundColor White
    Write-Host ""
    $choice = Read-Host "Enter your choice [0-5]"
} else {
    $choice = "4"
}

switch ($choice) {
    "1" {
        Write-Host ""
        Write-ColorLine "[SETUP] Running database setup and seed data..." $colors.Yellow
        Set-Location $workspaceRoot
        & python setup-complete.py
    }
    
    "2" {
        Write-Host ""
        Write-ColorLine "[BACKEND] Starting FastAPI Server..." $colors.Yellow
        Set-Location (Join-Path $workspaceRoot "backend")
        Write-Host ""
        Write-ColorLine "🌐 Backend will be available at: http://localhost:8000/docs" $colors.Cyan
        Write-Host ""
        & python -m uvicorn app.main:app --reload --port 8000
    }
    
    "3" {
        Write-Host ""
        Write-ColorLine "[FRONTEND] Starting Frontend Server..." $colors.Yellow
        Set-Location (Join-Path $workspaceRoot "frontend\lecturer-web")
        Write-Host ""
        Write-ColorLine "🌐 Frontend will be available at: http://localhost:3000/home.html" $colors.Cyan
        Write-Host ""
        & python -m http.server 3000
    }
    
    "4" {
        Write-Host ""
        Write-ColorLine "[FULL SETUP] Setting up complete environment..." $colors.Yellow
        Write-Host ""
        
        # Step 1: Setup database
        Write-ColorLine "  [1/3] Setting up database..." $colors.Yellow
        Set-Location $workspaceRoot
        & python setup-complete.py | Out-String | ForEach-Object { Write-Host $_ }
        
        Write-Host ""
        Write-ColorLine "  [2/3] Starting Backend API..." $colors.Yellow
        Write-Host ""
        
        # Start backend in new window
        $backendCmd = "cd '$((Join-Path $workspaceRoot 'backend').Replace("'", "''"))'; python -m uvicorn app.main:app --reload --port 8000"
        Start-Process pwsh -ArgumentList "-NoExit -Command `"$backendCmd`""
        
        Start-Sleep -Seconds 3
        
        Write-ColorLine "  [3/3] Starting Frontend Server..." $colors.Yellow
        Write-Host ""
        
        # Start frontend in new window
        $frontendCmd = "cd '$((Join-Path $workspaceRoot 'frontend\lecturer-web').Replace("'", "''"))'; python -m http.server 3000"
        Start-Process pwsh -ArgumentList "-NoExit -Command `"$frontendCmd`""
        
        Write-Host ""
        Write-ColorLine "╔═══════════════════════════════════════════════════════════════════════╗" $colors.Green
        Write-ColorLine "║                     ✅ EVERYTHING STARTED!                             ║" $colors.Green
        Write-ColorLine "╚═══════════════════════════════════════════════════════════════════════╝" $colors.Green
        Write-Host ""
        
        Write-Host "📍 Access Points:" -ForegroundColor Cyan
        Write-Host "  • Backend API:   http://localhost:8000/docs" -ForegroundColor White
        Write-Host "  • Frontend Home: http://localhost:3000/home.html" -ForegroundColor White
        Write-Host ""
        
        Write-Host "🔐 Test Credentials:" -ForegroundColor Cyan
        Write-Host "  Email:    lecturer@test.com" -ForegroundColor White
        Write-Host "  Password: lecturer123" -ForegroundColor White
        Write-Host ""
        
        Write-Host "📋 Other Accounts:" -ForegroundColor Cyan
        Write-Host "  • Admin:    admin@smd.edu.vn / admin123" -ForegroundColor White
        Write-Host "  • HOD:      hod@test.com / hod123" -ForegroundColor White
        Write-Host "  • Student:  student@test.com / student123" -ForegroundColor White
        Write-Host ""
        
        Write-Host "💡 Tips:" -ForegroundColor Yellow
        Write-Host "  1. Check browser console (F12) if page doesn't load" -ForegroundColor White
        Write-Host "  2. Make sure no other services on ports 8000, 3000" -ForegroundColor White
        Write-Host "  3. Backend auto-reloads on code changes" -ForegroundColor White
        Write-Host "  4. Refresh browser (Ctrl+R) to see updates" -ForegroundColor White
        Write-Host ""
        
        Write-Host "Windows Info:" -ForegroundColor Cyan
        Write-Host "  • Backend running in first PowerShell window" -ForegroundColor White
        Write-Host "  • Frontend running in second PowerShell window" -ForegroundColor White
        Write-Host "  • This window can be closed (servers stay running)" -ForegroundColor White
        Write-Host ""
    }
    
    "5" {
        Write-Host ""
        Write-ColorLine "[SETUP] Running database setup only..." $colors.Yellow
        Set-Location $workspaceRoot
        & python setup-complete.py
    }
    
    "0" {
        Write-ColorLine "Exiting..." $colors.Yellow
        exit 0
    }
    
    default {
        Write-ColorLine "Invalid choice" $colors.Red
        exit 1
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
