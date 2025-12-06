#!/bin/bash
# Test script for Authentication & User Management API
# Chạy: bash test_auth_api.sh

BASE_URL="http://localhost:8000"
ADMIN_EMAIL="admin@smd.edu.vn"
ADMIN_PASSWORD="Admin@123"
LECTURER_EMAIL="alice@smd.edu.vn"
LECTURER_PASSWORD="SecurePass123!"

echo "🚀 Starting API Tests..."
echo "================================"

# 1. Đăng ký tài khoản mới (Register)
echo "1️⃣  Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$LECTURER_EMAIL'",
    "full_name": "Alice Nguyễn",
    "password": "'$LECTURER_PASSWORD'",
    "role": "lecturer"
  }')
echo "Response: $REGISTER_RESPONSE"
echo ""

# 2. Đăng nhập (Login)
echo "2️⃣  Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$LECTURER_EMAIL'",
    "password": "'$LECTURER_PASSWORD'"
  }')
echo "Response: $LOGIN_RESPONSE"
echo ""

# Extract tokens (simple extraction - bạn cần jq hoặc python để parse JSON properly)
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)
echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"
echo ""

# 3. Xem thông tin bản thân (Get Current User)
echo "3️⃣  Getting current user info..."
curl -s -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
echo ""

# 4. Thay đổi mật khẩu (Change Password)
echo "4️⃣  Changing password..."
curl -s -X POST "$BASE_URL/auth/change-password" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "'$LECTURER_PASSWORD'",
    "new_password": "NewPass456!"
  }' | jq .
echo ""

# 5. Refresh token
echo "5️⃣  Refreshing token..."
REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "'$REFRESH_TOKEN'"
  }')
echo "Response: $REFRESH_RESPONSE"
echo ""

# 6. Đăng nhập với admin (nếu có)
echo "6️⃣  Logging in as admin..."
ADMIN_LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$ADMIN_EMAIL'",
    "password": "'$ADMIN_PASSWORD'"
  }')
echo "Response: $ADMIN_LOGIN"
echo ""

ADMIN_TOKEN=$(echo $ADMIN_LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Admin Token: $ADMIN_TOKEN"
echo ""

# 7. Xem danh sách user (List Users)
echo "7️⃣  Listing all users (admin only)..."
curl -s -X GET "$BASE_URL/users?skip=0&limit=10" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

# 8. Tạo user mới (Create User)
echo "8️⃣  Creating new user (admin only)..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@smd.edu.vn",
    "full_name": "Bob Trần",
    "password": "BobPass123!",
    "role": "hod"
  }')
echo "Response: $CREATE_RESPONSE"
echo ""

# Extract user ID from response
USER_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
echo "Created User ID: $USER_ID"
echo ""

# 9. Lấy thông tin user (Get User)
echo "9️⃣  Getting user info..."
curl -s -X GET "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

# 10. Cập nhật user (Update User)
echo "🔟 Updating user..."
curl -s -X PATCH "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Bob Trần Văn",
    "role": "aa"
  }' | jq .
echo ""

# 11. Khóa user (Lock User)
echo "1️⃣1️⃣ Locking user..."
curl -s -X PATCH "$BASE_URL/users/$USER_ID/lock" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

# 12. Mở khóa user (Unlock User)
echo "1️⃣2️⃣ Unlocking user..."
curl -s -X PATCH "$BASE_URL/users/$USER_ID/unlock" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

# 13. Import CSV
echo "1️⃣3️⃣ Importing users from CSV..."
curl -s -X POST "$BASE_URL/users/import-csv?file_path=C:\\project cnpm\\backend\\data\\users_example.csv" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

echo "================================"
echo "✅ All tests completed!"
