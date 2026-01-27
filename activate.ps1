Write-Host ""
Write-Host "Activating Virtual Environment..." -ForegroundColor Cyan
Write-Host ""

$venvActivate = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvActivate) {
    . $venvActivate
    Write-Host "OK - Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR - Virtual environment not found at .venv" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Environment Ready!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now you can run Python files from anywhere:" -ForegroundColor Yellow
Write-Host "  python check_health.py" -ForegroundColor White
Write-Host "  python backend/create_test_users.py" -ForegroundColor White
Write-Host ""
