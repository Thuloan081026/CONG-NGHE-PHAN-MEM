# PowerShell Test Script for Authentication & User Management API
# Usage: powershell -ExecutionPolicy Bypass -File test_auth_api.ps1

$BaseUrl = "http://localhost:8000"
$AdminEmail = "admin@smd.edu.vn"
$AdminPassword = "Admin@123"
$LecturerEmail = "alice@smd.edu.vn"
$LecturerPassword = "SecurePass123!"

Write-Host "🚀 Starting API Tests..." -ForegroundColor Green
Write-Host "================================"

# Helper function to make requests
function Invoke-ApiRequest {
    param (
        [string]$Method,
        [string]$Endpoint,
        [hashtable]$Body = $null,
        [string]$Token = $null
    )

    $Headers = @{
        "Content-Type" = "application/json"
    }

    if ($Token) {
        $Headers["Authorization"] = "Bearer $Token"
    }

    $Url = "$BaseUrl$Endpoint"
    
    if ($Body) {
        $BodyJson = ConvertTo-Json $Body
        $Response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $Headers -Body $BodyJson
    } else {
        $Response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $Headers
    }

    return $Response
}

# 1. Đăng ký tài khoản mới (Register)
Write-Host "1️⃣  Registering new user..." -ForegroundColor Cyan
$RegisterBody = @{
    email = $LecturerEmail
    full_name = "Alice Nguyễn"
    password = $LecturerPassword
    role = "lecturer"
}
$RegisterResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/register" -Body $RegisterBody
Write-Host "Response:" (ConvertTo-Json $RegisterResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 2. Đăng nhập (Login)
Write-Host "2️⃣  Logging in..." -ForegroundColor Cyan
$LoginBody = @{
    email = $LecturerEmail
    password = $LecturerPassword
}
$LoginResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/login" -Body $LoginBody
Write-Host "Response:" (ConvertTo-Json $LoginResponse -Depth 3) -ForegroundColor White
$AccessToken = $LoginResponse.access_token
$RefreshToken = $LoginResponse.refresh_token
Write-Host "Access Token: $AccessToken" -ForegroundColor Yellow
Write-Host "Refresh Token: $RefreshToken" -ForegroundColor Yellow
Write-Host ""

# 3. Xem thông tin bản thân (Get Current User)
Write-Host "3️⃣  Getting current user info..." -ForegroundColor Cyan
$UserResponse = Invoke-ApiRequest -Method GET -Endpoint "/users/me" -Token $AccessToken
Write-Host "Response:" (ConvertTo-Json $UserResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 4. Thay đổi mật khẩu (Change Password)
Write-Host "4️⃣  Changing password..." -ForegroundColor Cyan
$ChangePassBody = @{
    old_password = $LecturerPassword
    new_password = "NewPass456!"
}
$ChangePassResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/change-password" -Body $ChangePassBody -Token $AccessToken
Write-Host "Response:" (ConvertTo-Json $ChangePassResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 5. Refresh token
Write-Host "5️⃣  Refreshing token..." -ForegroundColor Cyan
$RefreshBody = @{
    refresh_token = $RefreshToken
}
$RefreshResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/refresh" -Body $RefreshBody
Write-Host "Response:" (ConvertTo-Json $RefreshResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 6. Đăng nhập với admin
Write-Host "6️⃣  Logging in as admin..." -ForegroundColor Cyan
$AdminLoginBody = @{
    email = $AdminEmail
    password = $AdminPassword
}
$AdminLoginResponse = Invoke-ApiRequest -Method POST -Endpoint "/auth/login" -Body $AdminLoginBody
Write-Host "Response:" (ConvertTo-Json $AdminLoginResponse -Depth 3) -ForegroundColor White
$AdminToken = $AdminLoginResponse.access_token
Write-Host "Admin Token: $AdminToken" -ForegroundColor Yellow
Write-Host ""

# 7. Xem danh sách user (List Users)
Write-Host "7️⃣  Listing all users (admin only)..." -ForegroundColor Cyan
$ListResponse = Invoke-ApiRequest -Method GET -Endpoint "/users?skip=0&limit=10" -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $ListResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 8. Tạo user mới (Create User)
Write-Host "8️⃣  Creating new user (admin only)..." -ForegroundColor Cyan
$CreateBody = @{
    email = "bob@smd.edu.vn"
    full_name = "Bob Trần"
    password = "BobPass123!"
    role = "hod"
}
$CreateResponse = Invoke-ApiRequest -Method POST -Endpoint "/users" -Body $CreateBody -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $CreateResponse -Depth 3) -ForegroundColor White
$UserId = $CreateResponse.id
Write-Host "Created User ID: $UserId" -ForegroundColor Yellow
Write-Host ""

# 9. Lấy thông tin user (Get User)
Write-Host "9️⃣  Getting user info..." -ForegroundColor Cyan
$GetUserResponse = Invoke-ApiRequest -Method GET -Endpoint "/users/$UserId" -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $GetUserResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 10. Cập nhật user (Update User)
Write-Host "🔟 Updating user..." -ForegroundColor Cyan
$UpdateBody = @{
    full_name = "Bob Trần Văn"
    role = "aa"
}
$UpdateResponse = Invoke-ApiRequest -Method PATCH -Endpoint "/users/$UserId" -Body $UpdateBody -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $UpdateResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 11. Khóa user (Lock User)
Write-Host "1️⃣1️⃣ Locking user..." -ForegroundColor Cyan
$LockResponse = Invoke-ApiRequest -Method PATCH -Endpoint "/users/$UserId/lock" -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $LockResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 12. Mở khóa user (Unlock User)
Write-Host "1️⃣2️⃣ Unlocking user..." -ForegroundColor Cyan
$UnlockResponse = Invoke-ApiRequest -Method PATCH -Endpoint "/users/$UserId/unlock" -Token $AdminToken
Write-Host "Response:" (ConvertTo-Json $UnlockResponse -Depth 3) -ForegroundColor White
Write-Host ""

# 13. Import CSV
Write-Host "1️⃣3️⃣ Importing users from CSV..." -ForegroundColor Cyan
try {
    $ImportUrl = "$BaseUrl/users/import-csv?file_path=d:\project cnpm\backend\data\users_example.csv"
    $Headers = @{
        "Authorization" = "Bearer $AdminToken"
    }
    $ImportResponse = Invoke-RestMethod -Uri $ImportUrl -Method POST -Headers $Headers
    Write-Host "Response:" (ConvertTo-Json $ImportResponse -Depth 3) -ForegroundColor White
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "================================"
Write-Host "✅ All tests completed!" -ForegroundColor Green
