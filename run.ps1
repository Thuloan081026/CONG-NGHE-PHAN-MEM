#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Python Runner with UTF-8 Encoding Support
    Chạy Python files với UTF-8 encoding để hỗ trợ Vietnamese characters
#>

param(
    [string]$FilePath = "",
    [string[]]$Arguments = @()
)

# Set UTF-8 encoding for Python output
$env:PYTHONIOENCODING = "utf-8"

# Show Python version
Write-Host "Python Runtime:" -ForegroundColor Cyan
python --version
Write-Host ""

if ($FilePath) {
    Write-Host "Running: python $FilePath $Arguments" -ForegroundColor Yellow
    Write-Host ""
    python $FilePath @Arguments
} else {
    Write-Host "Usage: .\run.ps1 -FilePath 'backend/create_test_users.py'" -ForegroundColor Yellow
    Write-Host "   or: .\run.ps1 -FilePath 'check_health.py'" -ForegroundColor Yellow
}
