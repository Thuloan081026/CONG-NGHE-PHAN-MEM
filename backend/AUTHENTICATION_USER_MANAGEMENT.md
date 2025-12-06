# BACKEND MODULE 1 – Authentication + User Management
## Xác thực & Quản lý người dùng

### 📌 Tính năng chính (Requirements)
- ✅ Đăng ký / Đăng nhập (Register / Login)
- ✅ JWT access + refresh token
- ✅ RBAC: Admin, Lecturer, HOD, AA, Student
- ✅ Thay đổi mật khẩu (Change Password)
- ✅ Import tài khoản từ CSV (CSV Import)
- ✅ System Admin quản lý user (Lock/Unlock)

---

## 📁 Cấu trúc code

### Core (Cốt lõi bảo mật)
| File | Chức năng |
|------|----------|
| `core/config.py` | Cấu hình SECRET_KEY, JWT, DB URL |
| `core/security.py` | Hash mật khẩu (bcrypt), tạo/giải mã JWT |
| `core/database.py` | SQLAlchemy setup, connection pool |
| `core/deps.py` | Dependencies: `get_current_user`, `require_roles` |

### Models (Database)
| File | Chức năng |
|------|----------|
| `models/user.py` | SQLAlchemy User model |

### Schemas (Request/Response)
| File | Chức năng |
|------|----------|
| `schemas/user_schema.py` | Pydantic schemas: UserCreate, UserOut, UserUpdate, Token, PasswordChange |

### Repositories (Data Access)
| File | Chức năng |
|------|----------|
| `repositories/user_repo.py` | CRUD operations: get, create, update, lock/unlock |

### Services (Business Logic)
| File | Chức năng |
|------|----------|
| `services/user_service.py` | Register, authenticate, change password, lock/unlock, import |

### API Routes
| File | Endpoints |
|------|-----------|
| `api/v1/auth.py` | `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/change-password` |
| `api/v1/user.py` | `/users` (CRUD), `/users/{id}/lock`, `/users/{id}/unlock` |

---

## 🔐 Luồng xác thực (Authentication Flow)

### 1️⃣ Đăng ký tài khoản (Register)

**Endpoint:** `POST /auth/register`

**Request:**
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

**Validation:**
- Email phải là duy nhất (không trùng)
- Mật khẩu sẽ được hash bằng bcrypt
- Role mặc định là `"student"` nếu không chỉ định

---

### 2️⃣ Đăng nhập (Login)

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "alice@smd.edu.vn",
  "password": "SecurePass123!"
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

**Token Payload (Access Token):**
```json
{
  "sub": "1",           // user_id
  "exp": 1702000000,    // expiration time (60 phút)
  "type": "access"
}
```

**Token Payload (Refresh Token):**
```json
{
  "sub": "1",           // user_id
  "exp": 1702604800,    // expiration time (7 ngày)
  "type": "refresh"
}
```

---

### 3️⃣ Làm mới token (Refresh Token)

**Endpoint:** `POST /auth/refresh`

**Request:**
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

---

### 4️⃣ Thay đổi mật khẩu (Change Password)

**Endpoint:** `POST /auth/change-password` hoặc `POST /users/change-password`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
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

**Validation:**
- Phải có access token hợp lệ
- `old_password` phải khớp với mật khẩu hiện tại
- `new_password` sẽ được hash rồi lưu

---

## 👥 Quản lý người dùng (User Management - Admin only)

### 5️⃣ Tạo người dùng (Create User)

**Endpoint:** `POST /users` (Admin only)

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request:**
```json
{
  "email": "bob@smd.edu.vn",
  "full_name": "Bob Trần",
  "password": "TempPass123!",
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

---

### 6️⃣ Xem danh sách người dùng (List Users)

**Endpoint:** `GET /users?skip=0&limit=10` (Admin only)

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

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

### 7️⃣ Xem thông tin người dùng (Get User)

**Endpoint:** `GET /users/{user_id}` (Admin or self)

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

### 8️⃣ Cập nhật thông tin người dùng (Update User)

**Endpoint:** `PATCH /users/{user_id}` (Admin only)

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request:**
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

---

### 9️⃣ Khóa tài khoản (Lock User)

**Endpoint:** `PATCH /users/{user_id}/lock` (Admin only)

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

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

**Tác dụng:**
- User không thể đăng nhập
- Token cũ sẽ không hoạt động
- Admin có thể mở khóa sau

---

### 🔟 Mở khóa tài khoản (Unlock User)

**Endpoint:** `PATCH /users/{user_id}/unlock` (Admin only)

**Headers:**
```
Authorization: Bearer <admin_access_token>
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
  "updated_at": "2025-12-06T11:10:00"
}
```

---

## 📤 Import người dùng từ CSV

### Cách 1️⃣: CLI Script

**File CSV:** `data/users_example.csv`

**Định dạng CSV:**
```
email,full_name,password,role
admin@smd.edu.vn,Admin User,Admin@123,admin
lecturer1@smd.edu.vn,Nguyen Van A,Pass123!,lecturer
hod@smd.edu.vn,Hoang Van C,Pass123!,hod
aa@smd.edu.vn,Le Thi D,Pass123!,aa
student1@smd.edu.vn,Pham Van E,Pass123!,student
```

**Command:**
```powershell
cd d:\project cnpm\backend
python .\scripts\import_users.py .\data\users_example.csv
```

**Output:**
```
Created 5 users
```

---

### Cách 2️⃣: HTTP API (Admin only)

**Endpoint:** `POST /users/import-csv?file_path=<path>`

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request:**
```
POST /users/import-csv?file_path=C:\project cnpm\backend\data\users_example.csv
```

**Response (200 OK):**
```json
{
  "created": 5
}
```

---

## 🔒 RBAC (Role-Based Access Control)

### Các role khả dụng:
| Role | Chức năng | Quyền |
|------|----------|-------|
| `admin` | System Admin | Quản lý user, cấu hình hệ thống, lock/unlock |
| `lecturer` | Giáo viên | Tạo/cập nhật giáo trình, duyệt cộng tác |
| `hod` | Trưởng bộ môn | Duyệt giáo trình cấp 1, quản lý giáo trình bộ môn |
| `aa` | Phòng học vụ | Duyệt giáo trình cấp 2, kiểm tra PLO mapping |
| `student` | Sinh viên | Tìm kiếm, xem giáo trình, nhận thông báo |

### Ví dụ RBAC trong code:
```python
# Chỉ admin có thể tạo user
@router.post("/users/", response_model=UserOut)
def create_user(user_in: UserCreate, _=Depends(require_roles("admin"))):
    ...

# Admin hoặc self (người dùng chính) có thể xem thông tin
@router.get("/users/{user_id}")
def get_user(user_id: int, current_user=Depends(get_current_user)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    ...
```

---

## 🚀 Hướng dẫn cài đặt & chạy

### 1. Cài dependencies
```powershell
cd d:\project cnpm\backend
python -m pip install -r requirements.txt
```

### 2. Khởi chạy server
```powershell
cd d:\project cnpm\backend
uvicorn app.main:app --reload --port 8000
```

### 3. Truy cập Swagger docs
```
http://localhost:8000/docs
```

### 4. Import dữ liệu mẫu
```powershell
cd d:\project cnpm\backend
python .\scripts\import_users.py .\data\users_example.csv
```

### 5. Đăng nhập với admin
```json
POST /auth/login
{
  "email": "admin@smd.edu.vn",
  "password": "Admin@123"
}
```

---

## 🔍 Cách sử dụng access token

### Với curl:
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/users/
```

### Với Python requests:
```python
import requests

headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(
    "http://localhost:8000/users/",
    headers=headers
)
print(response.json())
```

### Với JavaScript/Fetch:
```javascript
const response = await fetch('http://localhost:8000/users/', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});
const data = await response.json();
console.log(data);
```

---

## ⚠️ Lưu ý bảo mật (Production)

1. **Thay SECRET_KEY:**
   - Tạo chuỗi ngẫu nhiên dài (ví dụ: `openssl rand -hex 32`)
   - Lưu trong environment variable: `SECRET_KEY=...`

2. **Kích hoạt HTTPS:**
   - Tất cả token phải được gửi qua HTTPS
   - Sử dụng TLS certificate từ Let's Encrypt

3. **Rate Limiting:**
   - Hạn chế số lần login thất bại
   - Chặn brute-force attack

4. **Token Revocation:**
   - Lưu refresh tokens trong Redis
   - Hỗ trợ logout (delete token từ Redis)

5. **Logging & Monitoring:**
   - Ghi log tất cả login, lock/unlock
   - Giám sát failed login attempts

6. **Database:**
   - Thay SQLite bằng MySQL/PostgreSQL
   - Backup định kỳ
   - Encrypt sensitive fields

---

## 📋 Checklist hoàn chỉnh

- ✅ Authentication (Register, Login, Refresh)
- ✅ Password hashing (bcrypt)
- ✅ JWT tokens (access + refresh)
- ✅ RBAC (5 roles)
- ✅ Change password
- ✅ User management (CRUD)
- ✅ Lock/Unlock user
- ✅ CSV import (CLI + HTTP)
- ✅ Swagger documentation
- ⏳ Unit tests (to-do)
- ⏳ MySQL/PostgreSQL (to-do)
- ⏳ Token blacklist/revocation (to-do)

---

## 📞 Liên hệ hỗ trợ

Nếu có vấn đề, hãy check:
1. Logs server (`uvicorn` output)
2. Database `database.db` (SQLite)
3. Swagger docs (`/docs`)
4. Error messages trong response

