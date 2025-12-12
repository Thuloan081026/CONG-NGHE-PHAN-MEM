# Backend - Syllabus Management & Digitalization (SMD)

## 📚 Mô tả dự án

**SMD (Syllabus Management & Digitalization System)** là hệ thống quản lý và số hóa giáo trình cho các trường đại học.

### 🎯 Tính năng chính
- ✅ Quản lý giáo trình tập trung (Centralized syllabus management)
- ✅ Xác thực & quản lý người dùng (Authentication & user management)
- ✅ **Version control với Rollback** (NEW - Module 2)
- ✅ CLO/PLO mapping & metadata (NEW - Module 2)
- ✅ Quy trình duyệt giáo trình (Syllabus review workflow)
- ✅ AI-powered features (Diff detection, summarization, CLO-PLO mapping)
- ✅ Tìm kiếm nâng cao & phân tích
- ✅ Thông báo real-time & theo dõi
- ✅ Phân quyền dựa trên role (RBAC)

---

## 📦 Công nghệ sử dụng

### Backend
- **Framework:** FastAPI (Python 3.8+)
- **Database:** SQLite (dev) / MySQL/PostgreSQL (production)
- **Authentication:** JWT (access + refresh tokens)
- **Password:** bcrypt hashing
- **Validation:** Pydantic
- **ORM:** SQLAlchemy

### Frontend (Tương lai)
- **Web:** ReactJS / Next.js
- **Mobile:** React Native

### AI/ML (Tương lai)
- **Orchestration:** LangChain
- **Models:** PhoBERT, ViCLIP, Llama 3
- **Processing:** Celery + Redis

---

## 📚 MODULES

### ✅ Module 1: Authentication & User Management
**Status**: COMPLETED - 13 endpoints, 40+ files, 300+ pages documentation

Features:
- User registration & login
- JWT token management (access + refresh)
- Password hashing with bcrypt
- Role-based access control (5 roles)
- User lock/unlock for admin
- CSV bulk import

📖 **Documentation**: See `AUTHENTICATION_USER_MANAGEMENT.md`

---

### ✅ Module 2: Syllabus Management (NEW!)
**Status**: COMPLETED - 20 endpoints, version control, CLO-PLO mapping

Features:
- CRUD operations for syllabuses
- **Automatic version control** - Each update creates a new version
- **Rollback capability** - Restore to previous versions
- **Version comparison** - See what changed between versions
- **CLO-PLO mapping** - Link course & program learning outcomes
- **Workflow approval** - Draft → Submitted → Approved → Published
- **Metadata management** - Prerequisites, textbooks, assessment weights
- **Search & filtering** - By code, name, semester, department

📖 **Documentation**: See `SYLLABUS_MANAGEMENT_MODULE.md` & `MODULE_2_IMPLEMENTATION_SUMMARY.md`

---

## 🏗️ Kiến trúc (Architecture)

```
backend/
├── app/
│   ├── core/                    # Configuration & security
│   │   ├── config.py           # Settings
│   │   ├── security.py         # JWT, password hashing
│   │   ├── database.py         # DB connection
│   │   └── deps.py             # Dependencies (auth, RBAC)
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── syllabus.py         # NEW - Module 2
│   │   ├── review.py
│   │   └── ...
│   │
│   ├── schemas/                 # Pydantic request/response
│   │   ├── user_schema.py
│   │   ├── syllabus_schema.py  # NEW - Module 2
│   │   └── ...
│   │
│   ├── repositories/            # Data access layer (CRUD)
│   │   ├── user_repo.py
│   │   ├── syllabus_repo.py    # NEW - Module 2
│   │   └── ...
│   │
│   ├── services/                # Business logic layer
│   │   ├── user_service.py
│   │   ├── syllabus_service.py # NEW - Module 2
│   │   ├── ai_service.py
│   │   └── ...
│   │
│   ├── api/v1/                  # API routes
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── user.py              # User management endpoints
│   │   ├── syllabus.py          # NEW - Module 2 (20 endpoints)
│   │   ├── review.py            # Review workflow endpoints
│   │   └── ...
│   │
│   └── main.py                  # FastAPI app entry point
│
├── scripts/                      # Utility scripts
│   └── import_users.py          # CSV user import
│
├── data/                         # Sample data
│   └── users_example.csv
│
├── migrations/                   # Alembic (future)
├── tests/                        # Unit tests
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python 3.8 hoặc cao hơn
- pip / conda
- PowerShell (Windows) hoặc Bash (Linux/Mac)

### Bước 1: Clone & Setup

```powershell
cd d:\project cnpm\backend
```

### Bước 2: Cài dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Bước 3: Khởi chạy server

```powershell
uvicorn app.main:app --reload --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

### Bước 4: Truy cập API docs

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

## 📖 Tài liệu

### Module 1: Authentication & User Management ✅
- **File:** `AUTHENTICATION_USER_MANAGEMENT.md` (đầy đủ)
- **Quick Start:** `QUICK_START.md`
- **Endpoints:** 13 endpoints (register, login, refresh, change password, CRUD, lock/unlock, import CSV)

### Modules khác (Sắp tới)
- Module 2: Syllabus Management
- Module 3: Review & Approval Workflow
- Module 4: Search & Analytics
- Module 5: AI Services
- Module 6: Notifications

---

## 🧪 Testing

### Option 1: Swagger UI (Dễ nhất)
1. Mở http://localhost:8000/docs
2. Click "Authorize" (khoá icon)
3. Nhập access token từ login
4. Click endpoint để test

### Option 2: PowerShell Script (Toàn bộ flow)

```powershell
powershell -ExecutionPolicy Bypass -File test_auth_api.ps1
```

### Option 3: Bash Script (Linux/Mac)

```bash
bash test_auth_api.sh
```

### Option 4: cURL (Manual)

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@smd.edu.vn","password":"Pass123!","role":"lecturer"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@smd.edu.vn","password":"Pass123!"}'

# Get current user (with token)
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔑 Roles & Permissions

| Role | Mô tả | Quyền |
|------|-------|-------|
| **admin** | System Admin | Quản lý user, khóa/mở, cấu hình hệ thống, cuối cùng duyệt |
| **lecturer** | Giáo viên | Tạo/sửa giáo trình, duyệt cộng tác |
| **hod** | Trưởng bộ môn | Duyệt giáo trình cấp 1, quản lý bộ môn |
| **aa** | Phòng học vụ | Duyệt giáo trình cấp 2, kiểm tra PLO |
| **student** | Sinh viên | Xem giáo trình, theo dõi, phản hồi |

---

## 📝 CSV Import Format

**File:** `data/users_example.csv`

```csv
email,full_name,password,role
admin@smd.edu.vn,Admin User,Admin@123,admin
lecturer1@smd.edu.vn,Nguyen Van A,Pass123!,lecturer
hod@smd.edu.vn,Hoang Van C,Pass123!,hod
aa@smd.edu.vn,Le Thi D,Pass123!,aa
student1@smd.edu.vn,Pham Van E,Pass123!,student
```

**Import:**
```powershell
python .\scripts\import_users.py .\data\users_example.csv
```

---

## 🔐 Bảo mật (Security)

### Development
- SQLite database (`database.db`)
- Secret key: mặc định (không an toàn)
- HTTP (không HTTPS)

### Production
1. **Thay SECRET_KEY:**
   - Sinh chuỗi ngẫu nhiên: `openssl rand -hex 32`
   - Lưu trong environment: `export SECRET_KEY=...`

2. **Database:**
   - Thay SQLite bằng MySQL/PostgreSQL
   - Cập nhật `DATABASE_URL` trong `.env`

3. **HTTPS:**
   - Sử dụng Nginx reverse proxy
   - SSL certificate từ Let's Encrypt

4. **Rate Limiting:**
   - Thêm `slowapi` để chống brute-force

5. **Logging & Monitoring:**
   - Ghi log tất cả login, lock/unlock
   - Giám sát failed attempts

6. **Token Management:**
   - Lưu refresh tokens trong Redis
   - Hỗ trợ logout (token blacklist)

---

## 📊 Database Schema

### User Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📋 Checklist triển khai

### Phase 1: Authentication ✅
- [x] User model & schema
- [x] Password hashing (bcrypt)
- [x] JWT tokens (access + refresh)
- [x] Login endpoint
- [x] RBAC dependencies
- [x] Change password
- [x] CSV import

### Phase 2: Syllabus (Upcoming)
- [ ] Syllabus model
- [ ] CRUD endpoints
- [ ] Version control
- [ ] Diff detection

### Phase 3: Workflow (Upcoming)
- [ ] Review status machine
- [ ] Approval endpoints
- [ ] Notification system
- [ ] Activity logging

### Phase 4: AI/Search (Upcoming)
- [ ] AI service integration
- [ ] Elasticsearch integration
- [ ] Celery task queue
- [ ] Content summarization

---

## 🐛 Troubleshooting

| Vấn đề | Giải pháp |
|--------|----------|
| "ModuleNotFoundError" | Cài dependencies: `pip install -r requirements.txt` |
| "Port 8000 already in use" | Thay port: `uvicorn app.main:app --port 8001` |
| "Database is locked" | Xóa `database.db`, khởi động lại |
| "Invalid token" | Refresh token hoặc login lại |
| "Permission denied" | Kiểm tra role, admin có quyền cao nhất |
| "Email already registered" | Dùng email khác |

---

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Tạo Pull Request

---

## 📞 Support & Contact

Nếu có câu hỏi hoặc vấn đề:

1. Kiểm tra tài liệu: `AUTHENTICATION_USER_MANAGEMENT.md`
2. Xem log server (uvicorn output)
3. Truy cập http://localhost:8000/docs để test endpoint
4. Liên hệ team development

---

## 📜 License

[MIT License](LICENSE) - Tự do sử dụng cho mục đích học tập & thương mại

---

## ✨ Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-06 | Initial release - Authentication & User Management |
| 0.2.0 (TBD) | - | Syllabus Management |
| 0.3.0 (TBD) | - | Review Workflow |
| 0.4.0 (TBD) | - | AI Services |

---

**Happy Coding! 🚀**
