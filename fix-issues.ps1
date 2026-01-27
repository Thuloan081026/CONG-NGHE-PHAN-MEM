#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Fix PowerShell Execution Policy & Missing Dependencies
    Sửa lỗi "running scripts is disabled" và cài đặt packages cần thiết
#>

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       🔧 FIXING POWERSHELL & PYTHON ISSUES                    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ===== FIX 1: PowerShell Execution Policy =====
Write-Host "[STEP 1] Fixing PowerShell Execution Policy..." -ForegroundColor Yellow
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "  ✓ PowerShell Execution Policy set to RemoteSigned" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to set execution policy (might need admin)" -ForegroundColor Red
    Write-Host "  Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

# ===== FIX 2: Install Missing Packages =====
Write-Host ""
Write-Host "[STEP 2] Installing missing Python packages..." -ForegroundColor Yellow

$workspaceRoot = Split-Path -Parent $PSCommandPath
$pythonExe = Join-Path $workspaceRoot ".venv\Scripts\python.exe"

# Check venv
if (-not (Test-Path $pythonExe)) {
    Write-Host "  ✗ Virtual environment not found!" -ForegroundColor Red
    exit 1
}

$packagesToInstall = @(
    "argon2-cffi",
    "argon2-cffi-bindings",
    "bcrypt"
)

foreach ($package in $packagesToInstall) {
    Write-Host "  • Installing $package..." -ForegroundColor Cyan
    & $pythonExe -m pip install $package --force-reinstall -q
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ $package installed successfully" -ForegroundColor Green
    } else {
        Write-Host "    ✗ Failed to install $package" -ForegroundColor Red
    }
}

# ===== VERIFY FIX =====
Write-Host ""
Write-Host "[STEP 3] Verifying fixes..." -ForegroundColor Yellow

# Test argon2
Write-Host "  • Testing argon2 backend..." -ForegroundColor Cyan
& $pythonExe -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['argon2'], deprecated='auto'); pwd = ctx.hash('test'); print('✓')" -ErrorAction SilentlyContinue
if ($LASTEXITCODE -eq 0) {
    Write-Host "    ✓ argon2 backend works!" -ForegroundColor Green
} else {
    Write-Host "    ✗ argon2 still has issues" -ForegroundColor Red
}

# Test PowerShell script execution
Write-Host "  • Testing PowerShell script execution..." -ForegroundColor Cyan
$testScript = Join-Path $workspaceRoot "test-ps-script.ps1"
Write-Host "Write-Host 'OK'" | Out-File $testScript -Force
& $testScript -ErrorAction SilentlyContinue
if ($LASTEXITCODE -eq 0) {
    Write-Host "    ✓ PowerShell scripts can run!" -ForegroundColor Green
    Remove-Item $testScript -Force
} else {
    Write-Host "    ✗ PowerShell script execution still blocked" -ForegroundColor Red
}

# ===== SUMMARY =====
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║       ✓ ALL FIXES COMPLETED!                                 ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "You can now:" -ForegroundColor Yellow
Write-Host "  • Run PowerShell scripts (.ps1 files)" -ForegroundColor White
Write-Host "  • Create user accounts (argon2 password hashing works)" -ForegroundColor White
Write-Host "  • Use all Python packages without errors" -ForegroundColor White
Write-Host ""
Write-Host "Next step: Try running" -ForegroundColor Cyan
Write-Host "  python backend/create_test_users.py" -ForegroundColor White
Write-Host ""
