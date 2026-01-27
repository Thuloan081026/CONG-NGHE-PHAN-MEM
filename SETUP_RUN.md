# 🚀 SMD System - Hướng Dẫn Chạy

## Cấu Hình Backend + Frontend

### 1. **Backend (FastAPI - Port 8000)**

Backend đã được cấu hình tự động. Để chạy:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Hoặc sử dụng task có sẵn trong VS Code:
- Chạy lệnh `Backend: Run FastAPI Server`

✅ **Trạng Thái**: Backend đang chạy trên http://localhost:8000

### 2. **Frontend (HTTP Server - Port 3000)**

Frontend phục vụ toàn bộ web application. Để chạy:

```bash
cd frontend
python -m http.server 3000
```

✅ **Trạng Thái**: Frontend đang chạy trên http://localhost:3000

## 📍 Các URL Chính

| Role | URL | Tài khoản | Mật khẩu |
|------|-----|----------|---------|
| **Login** | http://localhost:3000 | student@edu.vn | student123 |
| Admin | http://localhost:3000/admin-web/html/dashboard.html | admin@edu.vn | admin123 |
| Lecturer | http://localhost:3000/lecturer-web/dashboard.html | lecturer@edu.vn | lecturer123 |
| HOD | http://localhost:3000/hod-web/dashboard.html | hod@edu.vn | hod123 |
| Academic Affairs | http://localhost:3000/academic-affairs-web/dashboard.html | aa@edu.vn | aa123 |
| Student | http://localhost:3000/student-web/dashboard.html | student@edu.vn | student123 |

## 🔧 Quá Trình Login

1. **Người dùng truy cập**: http://localhost:3000
2. **Nhập thông tin đăng nhập** (email + password)
3. **Backend xác thực** (POST /auth/login)
4. **Nhận access token** từ backend
5. **Lấy user data** từ /users/me endpoint
6. **Chuyển hướng** đến dashboard tương ứng với role

## ✅ Các Tài Khoản Test

Tất cả tài khoản đều có cấu trúc:
- **Email**: `{role}@edu.vn`
- **Mật khẩu**: `{role}123`

Ví dụ:
```
admin@edu.vn: admin123
lecturer@edu.vn: lecturer123
hod@edu.vn: hod123
aa@edu.vn: aa123 (academic_affairs)
student@edu.vn: student123
```

## 🐛 Xử Lý Sự Cố

### Backend không chạy?
- Kiểm tra port 8000: `netstat -ano | findstr 8000`
- Kiểm tra database MySQL
- Xem logs: `uvicorn app.main:app --reload --port 8000`

### Frontend không load?
- Kiểm tra port 3000: `netstat -ano | findstr 3000`
- Xác nhận đang chạy từ thư mục `frontend/`
- Xóa browser cache

### Login thất bại?
- Kiểm tra backend API: `http://localhost:8000/docs`
- Verify tài khoản tồn tại trong database
- Kiểm tra CORS settings trong backend

## 📚 API Endpoints Chính

```
POST   http://localhost:8000/auth/login        # Đăng nhập
GET    http://localhost:8000/users/me          # Lấy thông tin user hiện tại
GET    http://localhost:8000/docs              # API documentation (Swagger)
```

## 🔐 Kiến Trúc Security

- **Backend**: Sử dụng JWT tokens cho authentication
- **Frontend**: Lưu trữ access_token trong localStorage
- **CORS**: Được cấu hình cho http://localhost:3000

---

**Tạo bởi**: SMD System Team  
**Cập nhật**: 27/01/2026
