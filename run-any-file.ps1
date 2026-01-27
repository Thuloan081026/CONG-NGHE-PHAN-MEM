#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Universal Python File Runner - Chạy bất kỳ file Python nào mà không cần fix
    
.DESCRIPTION
    Script này cho phép chạy bất kỳ file Python nào trong workspace
    với PYTHONPATH được cấu hình tự động.
    
.PARAMETER openFile
    Chạy file hiện tại đang mở trong VS Code
    
.PARAMETER filePath
    Đường dẫn đến file cần chạy (tương đối từ workspace root)
    
.PARAMETER args
    Arguments truyền vào file Python
    
.EXAMPLE
    # Chạy file đang mở
    .\run-any-file.ps1 -openFile
    
    # Chạy file cụ thể
    .\run-any-file.ps1 -filePath "check_health.py"
    .\run-any-file.ps1 -filePath "backend/create_test_users.py"
    
    # Chạy với arguments
    .\run-any-file.ps1 -filePath "backend/check_db_data.py" -args "--verbose", "--output"
#>

param(
    [switch]$openFile,
    [string]$filePath,
    [string[]]$args
)

$ErrorActionPreference = "Continue"

# ===== COLOR SETUP =====
$colors = @{
    Green  = [System.ConsoleColor]::Green
    Yellow = [System.ConsoleColor]::Yellow
    Red    = [System.ConsoleColor]::Red
    Cyan   = [System.ConsoleColor]::Cyan
    White  = [System.ConsoleColor]::White
}

function Write-ColorOutput {
    param([string]$Message, [System.ConsoleColor]$Color = $colors.White)
    Write-Host $Message -ForegroundColor $Color
}

# ===== WORKSPACE SETUP =====
$workspaceRoot = Split-Path $PSScriptRoot -Parent
$pythonExe = Join-Path $workspaceRoot ".venv\Scripts\python.exe"
$pythonPath = @(
    "$workspaceRoot\backend"
    "$workspaceRoot"
) -join ";"

# ===== HEADER =====
Write-Host ""
Write-ColorOutput "╔═════════════════════════════════════════════════════════╗" -Color $colors.Cyan
Write-ColorOutput "║  🐍 Universal Python File Runner - Run Any File ✨      ║" -Color $colors.Cyan
Write-ColorOutput "╚═════════════════════════════════════════════════════════╝" -Color $colors.Cyan
Write-Host ""

# ===== VALIDATE PYTHON =====
if (-not (Test-Path $pythonExe)) {
    Write-ColorOutput "[ERROR] Python executable not found: $pythonExe" -Color $colors.Red
    Write-ColorOutput "        Trying system python..." -Color $colors.Yellow
    $pythonExe = "python"
}

# ===== GET FILE PATH =====
if ($openFile) {
    Write-ColorOutput "[INFO] Chế độ: Chạy file đang mở" -Color $colors.Yellow
    
    # Lấy file từ VS Code active editor
    $activeFile = $PROFILE -replace 'Microsoft.PowerShell_profile.ps1', '' | Get-Item -ErrorAction SilentlyContinue
    
    # Fallback: Hiển thị menu chọn file
    Write-ColorOutput "[?] Không thể detect file đang mở. Chọn file:" -Color $colors.Yellow
    
    $pyFiles = Get-ChildItem -Path $workspaceRoot -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | 
               Where-Object { $_.DirectoryName -notmatch '\.venv|__pycache__|\.git' } |
               Select-Object -First 20
    
    for ($i = 0; $i -lt $pyFiles.Count; $i++) {
        $relativePath = $pyFiles[$i].FullName -replace [regex]::Escape($workspaceRoot), '.' -replace '\\', '/'
        Write-Host "  $($i+1)) $relativePath" -ForegroundColor $colors.White
    }
    
    Write-Host ""
    $choice = Read-Host "Chọn số [1-$($pyFiles.Count)]"
    
    if ($choice -match '^\d+$' -and $choice -ge 1 -and $choice -le $pyFiles.Count) {
        $filePath = $pyFiles[$choice - 1].FullName -replace [regex]::Escape($workspaceRoot), '.' -replace '^\.\\', '' -replace '\\', '/'
    } else {
        Write-ColorOutput "[ERROR] Lựa chọn không hợp lệ!" -Color $colors.Red
        exit 1
    }
} elseif (-not $filePath) {
    Write-ColorOutput "[ERROR] Cần cung cấp -filePath hoặc -openFile" -Color $colors.Red
    Write-Host ""
    Write-Host "Cách dùng:" -ForegroundColor $colors.Cyan
    Write-Host "  .\run-any-file.ps1 -filePath 'check_health.py'" -ForegroundColor $colors.White
    Write-Host "  .\run-any-file.ps1 -filePath 'backend/create_test_users.py'" -ForegroundColor $colors.White
    Write-Host "  .\run-any-file.ps1 -openFile" -ForegroundColor $colors.White
    Write-Host ""
    exit 1
}

# ===== RESOLVE FILE PATH =====
$fullPath = $filePath
if (-not (Test-Path $fullPath -IsValid)) {
    # Try to find relative to workspace
    $fullPath = Join-Path $workspaceRoot $filePath
}

if (-not (Test-Path $fullPath)) {
    Write-ColorOutput "[ERROR] File không tìm thấy: $filePath" -Color $colors.Red
    Write-ColorOutput "        Tìm kiếm tại: $fullPath" -Color $colors.Red
    exit 1
}

# ===== DISPLAY INFO =====
Write-ColorOutput "[FILE] " -Color $colors.Green -NoNewline
Write-Host "$filePath"

Write-ColorOutput "[PYTHON] " -Color $colors.Green -NoNewline
Write-Host "$pythonExe"

Write-ColorOutput "[PYTHONPATH] " -Color $colors.Green -NoNewline
Write-Host "$pythonPath"

if ($args.Count -gt 0) {
    Write-ColorOutput "[ARGS] " -Color $colors.Green -NoNewline
    Write-Host ($args -join " ")
}

Write-Host ""
Write-ColorOutput "════════════════════════════════════════════════════════════" -Color $colors.Cyan
Write-Host ""

# ===== RUN PYTHON FILE =====
$env:PYTHONPATH = $pythonPath
$env:PYTHONUNBUFFERED = "1"

try {
    if ($args.Count -gt 0) {
        & $pythonExe $fullPath @args
    } else {
        & $pythonExe $fullPath
    }
    
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-ColorOutput "════════════════════════════════════════════════════════════" -Color $colors.Cyan
    
    if ($exitCode -eq 0) {
        Write-ColorOutput "[✓ SUCCESS] File chạy thành công! (Exit code: 0)" -Color $colors.Green
    } else {
        Write-ColorOutput "[✗ ERROR] File kết thúc với lỗi (Exit code: $exitCode)" -Color $colors.Red
    }
    
} catch {
    Write-ColorOutput "[✗ EXCEPTION] Lỗi khi chạy file: $_" -Color $colors.Red
    exit 1
}

Write-Host ""
