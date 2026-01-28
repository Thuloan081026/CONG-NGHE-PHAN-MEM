#!/usr/bin/env pwsh
# Setup PowerShell to automatically activate venv and set PYTHONPATH

$workspaceRoot = Split-Path -Parent $PSCommandPath

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Activating Virtual Environment..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$venvActivate = Join-Path $workspaceRoot ".venv" "Scripts" "Activate.ps1"

if (Test-Path $venvActivate) {
    . $venvActivate
    Write-Host "[✓] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[✗] Virtual environment not found at .venv" -ForegroundColor Red
    exit 1
}

# Set PYTHONPATH
$pythonPath = "$workspaceRoot\backend;$workspaceRoot"
$env:PYTHONPATH = $pythonPath

Write-Host "[OK] PYTHONPATH configured: $pythonPath" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Environment Ready!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now you can run Python files from anywhere:" -ForegroundColor Yellow
Write-Host "  python check_health.py" -ForegroundColor White
Write-Host "  python backend/create_test_users.py" -ForegroundColor White
Write-Host ""
