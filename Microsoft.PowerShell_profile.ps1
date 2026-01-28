# Profile for PowerShell in VS Code
# Tự động activate virtual environment khi mở terminal

# Get workspace root
$workspaceRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

# Virtual environment path
$venvPath = Join-Path $workspaceRoot ".venv"
$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"

# Auto-activate if venv exists
if ((Test-Path $activateScript) -and $env:VIRTUAL_ENV -eq $null) {
    . $activateScript
    Write-Host "✓ Virtual Environment activated: $venvPath" -ForegroundColor Green
    Write-Host ""
}

# Set PYTHONPATH for global import support
$env:PYTHONPATH = "$venvPath\..\backend;$venvPath\.."

# Customize prompt
function prompt {
    $venvName = if ($env:VIRTUAL_ENV) { 
        "(.venv) " 
    } else { 
        "" 
    }
    
    "$venvName$($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
}

# Useful aliases
Set-Alias -Name runpy -Value Invoke-PythonFile -ErrorAction SilentlyContinue
Set-Alias -Name backend -Value { Set-Location (Join-Path $workspaceRoot "backend") }
Set-Alias -Name frontend -Value { Set-Location (Join-Path $workspaceRoot "frontend") }

Write-Host "=== Development Environment Ready ===" -ForegroundColor Cyan
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  • python <file>          - Chạy file Python bất kỳ" -ForegroundColor White
Write-Host "  • .\run-any-file.ps1 -filePath 'file.py'  - Helper script" -ForegroundColor White
Write-Host "  • backend               - Jump to backend folder" -ForegroundColor White
Write-Host "  • frontend              - Jump to frontend folder" -ForegroundColor White
Write-Host ""
