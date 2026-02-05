# 🎓 SMD System - Syllabus Management & Digitalization

Hệ thống Quản lý Đề cương Môn học và Số hóa cho Trường Đại học

---

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt môi trường](#cài-đặt-môi-trường)
- [Khởi chạy dự án](#khởi-chạy-dự-án)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Tài khoản test](#tài-khoản-test)
- [API Documentation](#api-documentation)

---

## 🎯 Giới thiệu

**SMD System** là hệ thống quản lý đề cương môn học toàn diện, hỗ trợ quy trình:
- ✅ Tạo và quản lý syllabus
- ✅ Quy trình phê duyệt đa cấp (Lecturer → HoD → Academic Affairs → Principal)
- ✅ AI hỗ trợ phân tích và đánh giá
- ✅ CLO-PLO mapping và validation
- ✅ Tìm kiếm và tra cứu nâng cao

---

## 💻 Yêu cầu hệ thống

### Phần mềm cần thiết:
- **Python:** 3.10 hoặc cao hơn
- **XAMPP:** MySQL Server (port 3306)
- **Git:** (tùy chọn)

### Hệ điều hành:
- Windows 10/11
- Linux/Mac (có thể cần điều chỉnh lệnh)

---

## 🔧 Cài đặt môi trường

### Bước 1: Clone hoặc download dự án

```bash
cd D:\
git clone <repository-url> CONG-NGHE-PHAN-MEM
# Hoặc giải nén file ZIP vào D:\CONG-NGHE-PHAN-MEM
```

### Bước 2: Tạo Virtual Environment

```powershell
# Mở PowerShell tại thư mục dự án
cd D:\CONG-NGHE-PHAN-MEM

# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1

# Nếu gặp lỗi ExecutionPolicy, chạy lệnh:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bước 3: Cài đặt Python dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### Bước 4: Cấu hình MySQL Database

#### 4.1. Khởi động XAMPP MySQL
- Mở XAMPP Control Panel
- Start **Apache** và **MySQL**

#### 4.2. ✨ Tự động khởi tạo (Khuyến nghị)

**Backend sẽ TỰ ĐỘNG:**
- ✅ Tạo database `smd_db` nếu chưa có
- ✅ Tạo tất cả tables cần thiết
- ✅ Khởi tạo 6 tài khoản test

Chỉ cần chạy backend, mọi thứ sẽ được setup tự động!

#### 4.3. Hoặc khởi tạo thủ công (Tùy chọn)

```powershell
# Nếu muốn khởi tạo trước khi chạy backend
cd D:\CONG-NGHE-PHAN-MEM\backend
python init_users.py
```

---

## 🚀 Khởi chạy dự án

### Cần mở 5 Terminal/PowerShell riêng biệt

#### Terminal 1: Backend API (Port 8000)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\backend
D:\CONG-NGHE-PHAN-MEM\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2: Login Page (Port 3000)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\lecturer-web
python -m http.server 3000
```

#### Terminal 3: Admin Dashboard (Port 3001)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\admin-web\html
python -m http.server 3001
```

#### Terminal 4: Principal Dashboard (Port 3003)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\principal-web
python -m http.server 3003
```

#### Terminal 5: Student Portal (Port 3004) - Tùy chọn
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\student-web
python -m http.server 3004
```

### ✅ Kiểm tra hệ thống

Mở trình duyệt và truy cập:
- **Login Page:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/docs
- **Admin Dashboard:** http://localhost:3001
- **Principal Dashboard:** http://localhost:3003
- **Lecturer Dashboard:** http://localhost:3000/dashboard.html

---

## 👤 Tài khoản test

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@ut.edu.vn | admin123 |
| **Lecturer** | lecturer@ut.edu.vn | lecturer123 |
| **HOD** | hod@ut.edu.vn | hod123 |
| **Academic Affairs** | aa@ut.edu.vn | aa123 |
| **Student** | student@ut.edu.vn | student123 |
| **Principal** | principal@ut.edu.vn | principal123 |

---

## 📁 Cấu trúc dự án

```
CONG-NGHE-PHAN-MEM/
├── .venv/                          # Python virtual environment
├── backend/
│   ├── app/
│   │   ├── api/                    # API endpoints
│   │   ├── models/                 # Database models
│   │   ├── services/               # Business logic
│   │   ├── core/                   # Config, security, database
│   │   └── main.py                 # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── init_users.py              # Script khởi tạo users
│   └── reset_passwords.py         # Script reset passwords
├── frontend/
│   ├── index.html                 # Login page (port 3000)
│   ├── admin-web/                 # Admin Portal (port 3001)
│   ├── lecturer-web/              # Lecturer Portal (port 3002)
│   ├── hod-web/                   # HoD Review Portal
│   ├── academic-affairs-web/      # AA Portal
│   ├── principal-web/             # Principal Portal
│   ├── student-web/               # Student Portal
│   └── shared/                    # Shared components
└── README.md                      # File này
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive API Docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Authentication
```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ut.edu.vn", "password": "admin123"}'

# Response
{
  "access_token": "eyJ0eXAiOiJKV1...",
  "token_type": "bearer",
  "user": {...}
}
```

### Main Endpoints
- `POST /auth/login` - Đăng nhập
- `GET /users/me` - Thông tin user hiện tại
- `GET /syllabuses` - Danh sách syllabus
- `POST /syllabuses` - Tạo syllabus mới
- `PUT /syllabuses/{id}` - Cập nhật syllabus
- `POST /syllabuses/{id}/review` - Review syllabus

---

## 🛠️ Troubleshooting

### Lỗi: "Invalid credentials"
**Giải pháp:** Reset passwords
```powershell
cd D:\CONG-NGHE-PHAN-MEM\backend
python reset_passwords.py
```

### Lỗi: "Can't connect to MySQL"
**Giải pháp:**
1. Kiểm tra XAMPP MySQL đang chạy
2. Kiểm tra port 3306 không bị chiếm
3. Kiểm tra config trong `backend/app/core/config.py`

### Lỗi: "Port already in use"
**Giải pháp:** Tìm và kill process đang dùng port
```powershell
# Tìm process dùng port 8000
netstat -ano | findstr :8000

# Kill process (thay PID bằng số tìm được)
taskkill /PID <PID> /F
```

### Frontend không load được
**Giải pháp:** Hard refresh trình duyệt
- **Chrome/Edge:** Ctrl + Shift + R hoặc Ctrl + F5
- **Firefox:** Ctrl + Shift + R

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần [Troubleshooting](#troubleshooting)
2. Xem logs trong terminal
3. Kiểm tra MySQL có đang chạy không
4. Đảm bảo đã kích hoạt virtual environment

---

## 📝 License

© 2026 SMD System. All rights reserved.
