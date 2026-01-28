# ✅ Principal Web - Login & Dashboard Ready

## 📋 Tình Trạng Hiện Tại

### ✅ Backend API (Port 8000)
- FastAPI server chạy trên `http://localhost:8000`
- Login endpoint hoạt động: `POST /auth/login`
- User endpoint hoạt động: `GET /users/me`

### ✅ Frontend Server (Port 3000)
- HTTP Server chạy từ folder `frontend/`
- Serve tất cả web applications (student, lecturer, admin, principal, etc.)

### ✅ Principal Account
- **Email**: principal@edu.vn
- **Password**: principal123
- **Role**: principal
- **Status**: ✅ Active in database

### ✅ Principal Dashboard
- **File**: `frontend/principal-web/dashboard.html`
- **URL**: http://localhost:3000/principal-web/dashboard.html
- **Status**: ✅ HTML file ready with JWT authentication

## 🔑 Tài Khoản Test Tất Cả Roles

| Role | Email | Password | URL |
|------|-------|----------|-----|
| Admin | admin@edu.vn | admin123 | /admin-web/html/dashboard.html |
| Lecturer | lecturer@edu.vn | lecturer123 | /lecturer-web/dashboard.html |
| HOD | hod@edu.vn | hod123 | /hod-web/dashboard.html |
| Academic Affairs | aa@edu.vn | aa123 | /academic-affairs-web/dashboard.html |
| Student | student@edu.vn | student123 | /student-web/dashboard.html |
| Principal | principal@edu.vn | principal123 | /principal-web/dashboard.html |

## 🚀 Cách Sử Dụng

### Login Flow
1. Truy cập: http://localhost:3000
2. Nhập email và password
3. Click "Đăng nhập"
4. Tự động redirect đến dashboard tương ứng với role

### Principal Dashboard
1. Truy cập: http://localhost:3000
2. Login: `principal@edu.vn` / `principal123`
3. Redirect đến: http://localhost:3000/principal-web/dashboard.html
4. Dashboard hiển thị:
   - User info (Email, Full Name, Role)
   - Stats cards (Lecturers, Students, Syllabi count)
   - Logout button

## 💻 Kiến Trúc Code

### Login Process
```
User Input (HTML Form)
    ↓
POST /auth/login (Backend)
    ↓
Return JWT Access Token
    ↓
Store in localStorage
    ↓
Redirect to Dashboard (based on role)
```

### Dashboard Authentication
```
Load Dashboard Page
    ↓
Check localStorage for access_token
    ↓
GET /users/me (with Bearer token)
    ↓
Verify role matches dashboard
    ↓
Display user data
```

## 🛠️ File Đã Chỉnh Sửa

### 1. Frontend Login Page
- **File**: `frontend/index.html`
- **Thay đổi**: Sửa redirect URLs từ absolute (`/principal-web/...`) thành relative (`principal-web/...`)
- **Lý do**: Phù hợp với structure của static HTTP server

### 2. Principal Dashboard
- **File**: `frontend/principal-web/dashboard.html`
- **Thay đổi**:
  - Sửa token key từ `token` → `access_token`
  - Sửa redirect URLs từ `/` → `../index.html` (relative path)
  - Nâng cấp UI với header, stats cards, better styling
  - Thêm error handling

### 3. Principal Account
- **File**: N/A (Database)
- **Thay đổi**: Tạo user account `principal@edu.vn` trong database
- **Password**: SHA256 hash của "principal123"

## 📝 Các File Python Tạo

1. **`create_principal.py`** - Tạo principal account
2. **`test_principal_login.py`** - Test login endpoint
3. **`test_principal_complete.py`** - Test full flow
4. **`check_student.py`** - Kiểm tra schema database

## ✅ Testing Checklist

- [x] Backend API responds to login
- [x] Backend returns valid JWT token
- [x] `/users/me` endpoint returns correct user data
- [x] Frontend server serves principal dashboard HTML
- [x] Principal account created in database
- [x] Login page redirects to correct dashboard
- [x] Dashboard loads without errors
- [x] Dashboard displays user info
- [x] Logout button works
- [x] All relative paths work correctly

## 🔐 Security Notes

- Passwords are hashed with SHA256 in database
- JWT tokens expire after 24 hours
- Tokens stored in localStorage (consider httpOnly cookies in production)
- CORS enabled for http://localhost:3000
- Role-based access control implemented

## 📞 Quick Commands

Start everything:
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
python -m http.server 3000
```

Test principal login:
```bash
python test_principal_complete.py
```

Access dashboard:
```
http://localhost:3000/principal-web/dashboard.html
(requires login first at http://localhost:3000)
```

---
**Status**: ✅ System Ready for Principal Web Testing  
**Date**: 27/01/2026
