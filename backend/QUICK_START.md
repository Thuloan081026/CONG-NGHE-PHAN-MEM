# 🎯 QUICK START - Authentication & User Management

## 📝 Tóm tắt chức năng (Summary)

Hệ thống quản lý xác thực và người dùng hoàn chỉnh cho ứng dụng SMD (Syllabus Management & Digitalization).

**Tính năng:**
- ✅ Đăng ký / Đăng nhập với JWT tokens
- ✅ Refresh tokens (tự động cập nhật access token)
- ✅ 5 roles: Admin, Lecturer, HOD, AA, Student
- ✅ Thay đổi mật khẩu (xác thực)
- ✅ Quản lý user: tạo, sửa, xem, khóa/mở
- ✅ Import hàng loạt từ CSV (Admin)

---

## ⚡ Cài đặt nhanh (Quick Setup)

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

### 3. Import dữ liệu mẫu (tuỳ chọn)
```powershell
cd d:\project cnpm\backend
python .\scripts\import_users.py .\data\users_example.csv
```

### 4. Truy cập API docs
```
http://localhost:8000/docs  (Swagger)
http://localhost:8000/redoc (ReDoc)
```

---

## 🔑 Các endpoint chính (Main Endpoints)

### Authentication (/auth)
| Method | Endpoint | Mô tả | Yêu cầu |
|--------|----------|-------|---------|
| POST | `/auth/register` | Đăng ký tài khoản mới | Không |
| POST | `/auth/login` | Đăng nhập, nhận JWT | Không |
| POST | `/auth/refresh` | Làm mới access token | refresh_token |
| POST | `/auth/change-password` | Thay đổi mật khẩu | access_token |

### User Management (/users)
| Method | Endpoint | Mô tả | Quyền |
|--------|----------|-------|--------|
| POST | `/users` | Tạo user mới | Admin |
| GET | `/users` | Xem danh sách user | Admin |
| GET | `/users/me` | Xem thông tin bản thân | Authenticated |
| GET | `/users/{id}` | Xem thông tin user | Admin / Self |
| PATCH | `/users/{id}` | Cập nhật thông tin user | Admin |
| PATCH | `/users/{id}/lock` | Khóa user | Admin |
| PATCH | `/users/{id}/unlock` | Mở khóa user | Admin |
| POST | `/users/import-csv` | Import từ CSV | Admin |

---

## 📌 Ví dụ sử dụng (Usage Examples)

### 1️⃣ Đăng ký

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@smd.edu.vn",
    "full_name": "Alice Nguyễn",
    "password": "SecurePass123!",
    "role": "lecturer"
  }'
```

### 2️⃣ Đăng nhập

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@smd.edu.vn",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3️⃣ Sử dụng access token

```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

### 4️⃣ Thay đổi mật khẩu

```bash
curl -X POST http://localhost:8000/auth/change-password \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewPass456!"
  }'
```

### 5️⃣ Tạo user (Admin)

```bash
curl -X POST http://localhost:8000/users \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob@smd.edu.vn",
    "full_name": "Bob Trần",
    "password": "TempPass123!",
    "role": "hod"
  }'
```

### 6️⃣ Khóa user (Admin)

```bash
curl -X PATCH http://localhost:8000/users/1/lock \
  -H "Authorization: Bearer <admin_token>"
```

### 7️⃣ Import CSV (Admin)

```bash
curl -X POST "http://localhost:8000/users/import-csv?file_path=C:\\project cnpm\\backend\\data\\users_example.csv" \
  -H "Authorization: Bearer <admin_token>"
```

---

## 📊 CSV Format

**File:** `data/users_example.csv`

```csv
email,full_name,password,role
admin@smd.edu.vn,Admin User,Admin@123,admin
lecturer1@smd.edu.vn,Nguyen Van A,Pass123!,lecturer
hod@smd.edu.vn,Hoang Van C,Pass123!,hod
aa@smd.edu.vn,Le Thi D,Pass123!,aa
student1@smd.edu.vn,Pham Van E,Pass123!,student
```

**Tạo file CSV của riêng bạn:**
1. Tạo file `.csv` với các cột: `email`, `full_name`, `password`, `role`
2. Chạy script: `python .\scripts\import_users.py <path_to_csv>`

---

## 🔐 Quản lý JWT Tokens

### Access Token
- **TTL (Time to Live):** 60 phút (cấu hình trong `core/config.py`)
- **Dùng để:** Xác thực request API
- **Header:** `Authorization: Bearer <access_token>`

### Refresh Token
- **TTL:** 7 ngày
- **Dùng để:** Lấy access token mới khi hết hạn
- **Không được dùng để:** Gọi API endpoint

### Cách refresh token
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

---

## 🛡️ Bảo mật (Security)

### Password Hashing
- Sử dụng **bcrypt** (one-way)
- Mật khẩu không bao giờ lưu dưới dạng plain text
- Thay đổi mật khẩu cũng hash lại từ đầu

### JWT Security
- Secret key được lưu trong `core/config.py`
- **Sản xuất:** Thay `SECRET_KEY` bằng chuỗi ngẫu nhiên dài, lưu trong `.env`
- Token bao gồm signature để phát hiện tampering

### RBAC (Role-Based Access Control)
```python
# Ví dụ: Chỉ admin có quyền tạo user
@router.post("/users/", response_model=UserOut)
def create_user(user_in: UserCreate, _=Depends(require_roles("admin"))):
    ...
```

### Lock/Unlock
- Admin có thể khóa user khi phát hiện hoạt động bất thường
- User bị khóa không thể đăng nhập
- Admin có thể mở khóa bất kỳ lúc nào

---

## 📂 Cấu trúc file quan trọng

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          ← Cấu hình JWT, DB
│   │   ├── security.py        ← Hash, token
│   │   ├── database.py        ← SQLAlchemy setup
│   │   └── deps.py            ← Dependencies (auth, RBAC)
│   ├── models/
│   │   └── user.py            ← User database model
│   ├── schemas/
│   │   └── user_schema.py     ← Pydantic request/response
│   ├── repositories/
│   │   └── user_repo.py       ← Database CRUD
│   ├── services/
│   │   └── user_service.py    ← Business logic
│   ├── api/v1/
│   │   ├── auth.py            ← Login, register, refresh
│   │   └── user.py            ← User CRUD, lock/unlock
│   └── main.py                ← FastAPI app entry
├── scripts/
│   └── import_users.py        ← CSV import script
├── data/
│   └── users_example.csv      ← Sample data
├── requirements.txt           ← Dependencies
└── AUTHENTICATION_USER_MANAGEMENT.md ← Full docs
```

---

## 🧪 Test bằng Swagger

1. Mở http://localhost:8000/docs
2. Click "Authorize" (khoá icon ở góc phải)
3. Nhập access_token từ login
4. Thực hiện các request từ giao diện

---

## ⚠️ Vấn đề thường gặp (Common Issues)

| Vấn đề | Giải pháp |
|--------|----------|
| "Import could not be resolved" | Cài dependencies: `pip install -r requirements.txt` |
| "Database is locked" | Xóa `database.db`, chạy lại server |
| "Token expired" | Sử dụng refresh token để lấy access token mới |
| "Not authorized (403)" | Kiểm tra role user, admin chỉ có thể tạo user |
| "Email already registered" | Email đã tồn tại, dùng email khác |

---

## 📖 Tài liệu chi tiết

Xem file `AUTHENTICATION_USER_MANAGEMENT.md` để có thông tin đầy đủ:
- Mô tả chi tiết từng endpoint
- Ví dụ request/response
- Cấu trúc RBAC
- Hướng dẫn sản xuất (Production setup)

---

## ✨ Tính năng sắp có (Upcoming)

- [ ] Unit tests
- [ ] Integration tests
- [ ] MySQL/PostgreSQL support
- [ ] Token blacklist (logout)
- [ ] 2FA (Two-factor authentication)
- [ ] OAuth2 social login
- [ ] Activity logging

