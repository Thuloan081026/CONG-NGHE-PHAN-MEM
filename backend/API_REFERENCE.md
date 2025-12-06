# 📚 AUTHENTICATION & USER MANAGEMENT - API REFERENCE

## 📖 Tài liệu endpoints chi tiết

---

## 🔐 Authentication Endpoints (`/auth`)

### 1. Register (Đăng ký)

**Endpoint:** `POST /auth/register`  
**Quyền:** Không yêu cầu  
**Rate limit:** Không

**Request Body:**
```json
{
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "password": "SecurePass123!",
  "role": "lecturer"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "role": "lecturer",
  "is_active": true,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T10:30:00"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

**Validation:**
- `email`: Phải là email hợp lệ, duy nhất
- `password`: Tối thiểu 8 ký tự (tuỳ chọn)
- `role`: admin, lecturer, hod, aa, student (mặc định: student)
- `full_name`: Tuỳ chọn

---

### 2. Login (Đăng nhập)

**Endpoint:** `POST /auth/login`  
**Quyền:** Không yêu cầu  
**Rate limit:** Nên có (chống brute-force)

**Request Body:**
```json
{
  "email": "alice@smd.edu.vn",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzAyMDAwMDAwLCJ0eXBlIjoiYWNjZXNzIn0.signature",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzAyNjA0ODAwLCJ0eXBlIjoicmVmcmVzaCJ9.signature",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

**Notes:**
- Token phải được gửi trong header: `Authorization: Bearer <access_token>`
- Access token hết hạn sau 60 phút
- Refresh token hết hạn sau 7 ngày

---

### 3. Refresh Token (Làm mới)

**Endpoint:** `POST /auth/refresh`  
**Quyền:** Không yêu cầu  
**Rate limit:** Không

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Invalid token" | "Not a refresh token"
}
```

**Notes:**
- Sử dụng khi access token sắp hết hạn
- Refresh token hợp lệ được trả về token mới

---

### 4. Change Password (Thay đổi mật khẩu)

**Endpoint:** `POST /auth/change-password`  
**Quyền:** Authenticated  
**Rate limit:** 5 requests/hour

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "old_password": "SecurePass123!",
  "new_password": "NewPass456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Old password incorrect"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Validation:**
- `old_password` phải khớp với mật khẩu hiện tại
- `new_password` tối thiểu 8 ký tự (tuỳ chọn)
- `new_password` không được giống `old_password`

---

## 👥 User Management Endpoints (`/users`)

### 5. Create User (Tạo người dùng)

**Endpoint:** `POST /users`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "bob@smd.edu.vn",
  "full_name": "Bob Trần",
  "password": "BobPass123!",
  "role": "hod"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "email": "bob@smd.edu.vn",
  "full_name": "Bob Trần",
  "role": "hod",
  "is_active": true,
  "created_at": "2025-12-06T10:35:00",
  "updated_at": "2025-12-06T10:35:00"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Insufficient privileges"
}
```

---

### 6. List Users (Danh sách người dùng)

**Endpoint:** `GET /users?skip=0&limit=10`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `skip`: Số record bỏ qua (mặc định: 0)
- `limit`: Số record trả về (mặc định: 100, max: 1000)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "alice@smd.edu.vn",
    "full_name": "Alice Nguyễn",
    "role": "lecturer",
    "is_active": true,
    "created_at": "2025-12-06T10:30:00"
  },
  {
    "id": 2,
    "email": "bob@smd.edu.vn",
    "full_name": "Bob Trần",
    "role": "hod",
    "is_active": true,
    "created_at": "2025-12-06T10:35:00"
  }
]
```

---

### 7. Get Current User (Xem thông tin bản thân)

**Endpoint:** `GET /users/me`  
**Quyền:** Authenticated  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "role": "lecturer",
  "is_active": true,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T10:30:00"
}
```

---

### 8. Get User by ID (Xem thông tin user)

**Endpoint:** `GET /users/{user_id}`  
**Quyền:** Admin or Self  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `user_id`: ID của user cần xem

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "role": "lecturer",
  "is_active": true,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T10:30:00"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "Not authorized"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "User not found"
}
```

---

### 9. Update User (Cập nhật thông tin)

**Endpoint:** `PATCH /users/{user_id}`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Path Parameters:**
- `user_id`: ID của user cần cập nhật

**Request Body:**
```json
{
  "full_name": "Alice Nguyễn Thị",
  "role": "hod"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn Thị",
  "role": "hod",
  "is_active": true,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T11:00:00"
}
```

**Notes:**
- Chỉ có thể cập nhật `full_name` và `role`
- Không thể cập nhật `email` hay `password` (dùng endpoint riêng)

---

### 10. Lock User (Khóa tài khoản)

**Endpoint:** `PATCH /users/{user_id}/lock`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Path Parameters:**
- `user_id`: ID của user cần khóa

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "role": "lecturer",
  "is_active": false,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T11:05:00"
}
```

**Effect:**
- User không thể đăng nhập
- Token cũ sẽ bị từ chối
- Thông báo sẽ được gửi cho user (nếu có hệ thống notification)

---

### 11. Unlock User (Mở khóa tài khoản)

**Endpoint:** `PATCH /users/{user_id}/unlock`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Path Parameters:**
- `user_id`: ID của user cần mở khóa

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "alice@smd.edu.vn",
  "full_name": "Alice Nguyễn",
  "role": "lecturer",
  "is_active": true,
  "created_at": "2025-12-06T10:30:00",
  "updated_at": "2025-12-06T11:10:00"
}
```

**Effect:**
- User có thể đăng nhập lại
- Token mới sẽ hoạt động bình thường

---

### 12. Import Users from CSV (Import từ CSV)

**Endpoint:** `POST /users/import-csv?file_path=<path>`  
**Quyền:** Admin only  
**Rate limit:** Không

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `file_path`: Đường dẫn tuyệt đối đến file CSV (Windows: `C:\path\to\file.csv`)

**CSV Format:**
```
email,full_name,password,role
admin@smd.edu.vn,Admin User,Admin@123,admin
lecturer1@smd.edu.vn,Nguyen Van A,Pass123!,lecturer
student1@smd.edu.vn,Pham Van E,Pass123!,student
```

**Response (200 OK):**
```json
{
  "created": 3
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "[Errno 2] No such file or directory: '...'"
}
```

**Notes:**
- File CSV phải có header: `email,full_name,password,role`
- Nếu email đã tồn tại, sẽ bị bỏ qua
- Mật khẩu sẽ được hash bằng bcrypt
- Không có callback khi import thất bại (sẽ cải thiện sau)

---

## 🔒 RBAC Matrix (Bảng quyền)

| Endpoint | Admin | Lecturer | HOD | AA | Student |
|----------|-------|----------|-----|----|---------| 
| POST /auth/register | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /auth/login | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /auth/refresh | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /auth/change-password | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /users | ✅ | ❌ | ❌ | ❌ | ❌ |
| GET /users | ✅ | ❌ | ❌ | ❌ | ❌ |
| GET /users/me | ✅ | ✅ | ✅ | ✅ | ✅ |
| GET /users/{id} | ✅ | ✅* | ✅* | ✅* | ✅* |
| PATCH /users/{id} | ✅ | ❌ | ❌ | ❌ | ❌ |
| PATCH /users/{id}/lock | ✅ | ❌ | ❌ | ❌ | ❌ |
| PATCH /users/{id}/unlock | ✅ | ❌ | ❌ | ❌ | ❌ |
| POST /users/import-csv | ✅ | ❌ | ❌ | ❌ | ❌ |

*Chỉ xem được thông tin của chính mình hoặc nếu là admin

---

## 📊 HTTP Status Codes

| Code | Meaning | Ngữ cảnh |
|------|---------|----------|
| 200 | OK | Request thành công |
| 201 | Created | Resource được tạo thành công |
| 400 | Bad Request | Input không hợp lệ |
| 401 | Unauthorized | Chưa xác thực hoặc token hết hạn |
| 403 | Forbidden | Không có quyền thực hiện |
| 404 | Not Found | Resource không tồn tại |
| 409 | Conflict | Email đã tồn tại |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Lỗi server |

---

## 🔑 Token Structure

### Access Token Payload
```json
{
  "sub": "1",           // User ID (string)
  "exp": 1702000000,    // Expiration timestamp (Unix)
  "type": "access"      // Token type
}
```

### Refresh Token Payload
```json
{
  "sub": "1",           // User ID (string)
  "exp": 1702604800,    // Expiration timestamp (Unix)
  "type": "refresh"     // Token type
}
```

### Cách decode (Python):
```python
import jwt
from app.core.config import settings

token = "eyJhbGciOiJIUzI1NiIs..."
payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
print(payload)
# {'sub': '1', 'exp': 1702000000, 'type': 'access'}
```

---

## 💾 Data Models

### User Model
```
{
  id: int (primary key)
  email: str (unique, 255 chars max)
  full_name: str (nullable, 255 chars max)
  hashed_password: str (bcrypt hash)
  role: str (admin | lecturer | hod | aa | student)
  is_active: bool (default: true)
  created_at: datetime (auto)
  updated_at: datetime (auto)
}
```

---

## 🛠️ Caching Strategy (Sắp tới)

- Access token: Không cache (JWT tự contain thông tin)
- User info: Cache 5 phút (Redis)
- User list: Cache 10 phút (chỉ admin)
- Invalidate cache khi update

---

## 📞 Support & FAQ

**Q: Token hết hạn, làm sao?**  
A: Dùng refresh token: `POST /auth/refresh` với refresh_token

**Q: Quên mật khẩu?**  
A: Hiện tại chưa hỗ trợ. Admin có thể reset bằng cách update user

**Q: Có thể revoke token?**  
A: Hiện tại không. Cải tiến: sử dụng token blacklist (Redis)

**Q: Mất password cũ, sửa sao?**  
A: Admin gọi API cập nhật user, sau đó user reset

