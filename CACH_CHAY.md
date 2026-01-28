# Hướng dẫn chạy SMD System

## Bước 1: Mở 4 Terminal/PowerShell riêng biệt

### Terminal 1 - Backend API (Port 8000)
```bash
cd c:\smd\backend
c:\smd\smd\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2 - Frontend Login Page (Port 3000)
```bash
cd c:\smd\smd\frontend
python -m http.server 3000
```

### Terminal 3 - Admin Dashboard (Port 3001)
```bash
cd c:\smd\smd\frontend\admin-web\html
python -m http.server 3001
```

### Terminal 4 - Lecturer Dashboard (Port 3002)
```bash
cd c:\smd\smd\frontend\lecturer-web
python -m http.server 3002
```

## Bước 2: Truy cập hệ thống

Mở trình duyệt và truy cập: **http://localhost:3000**

## Tài khoản test

- **Admin:** admin@test.com / admin123
- **Lecturer:** lecturer@test.com / lecturer123
- **Student:** student@test.com / student123

## Luồng hoạt động

1. Truy cập http://localhost:3000 → Hiển thị trang login
2. Nhập email và password → Click "Đăng nhập"
3. Hệ thống tự động chuyển hướng:
   - Admin → http://localhost:3001 (Admin Dashboard)
   - Lecturer → http://localhost:3002 (Lecturer Dashboard)

## Dừng hệ thống

Nhấn **Ctrl + C** ở mỗi terminal để dừng từng server
