# 🚀 Hướng dẫn Setup Nhanh cho Người Dùng Mới

## ✅ Yêu cầu trước khi bắt đầu

1. **Python 3.10+** đã cài đặt
2. **XAMPP** đã cài đặt và **MySQL Server** đang chạy (port 3306)
3. **VS Code** (khuyến nghị) hoặc terminal/PowerShell

---

## 🎯 Setup Chỉ Với 5 Bước (Không cần tạo database thủ công!)

### Bước 1: Kích hoạt Virtual Environment

```powershell
# Mở PowerShell tại thư mục dự án
cd D:\CONG-NGHE-PHAN-MEM

# Kích hoạt virtual environment
.\.venv\Scripts\Activate.ps1
```

**Lưu ý:** Nếu gặp lỗi ExecutionPolicy, chạy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bước 2: Cài đặt Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### Bước 3: Kiểm tra MySQL đang chạy

- Mở **XAMPP Control Panel**
- Bấm **Start** cho **MySQL**
- Đảm bảo MySQL đang chạy trên port **3306**

### Bước 4: Chạy Backend (Tự động tạo database & users!)

```powershell
# Từ thư mục backend
cd D:\CONG-NGHE-PHAN-MEM\backend

# Chạy FastAPI server
D:\CONG-NGHE-PHAN-MEM\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**Backend sẽ TỰ ĐỘNG:**
- ✅ Tạo database `smd_db` nếu chưa có
- ✅ Tạo tất cả các tables cần thiết
- ✅ Khởi tạo 6 tài khoản test mặc định

### Bước 5: Chạy Frontend

**Terminal mới (không tắt backend):**

```powershell
# Login Page (port 3000)
cd D:\CONG-NGHE-PHAN-MEM\frontend\lecturer-web
python -m http.server 3000
```

**Terminal khác (nếu cần admin dashboard):**

```powershell
# Admin Dashboard (port 3001)
cd D:\CONG-NGHE-PHAN-MEM\frontend\admin-web\html
python -m http.server 3001
```

---

## 🎉 Hoàn tất! Truy cập hệ thống

Mở trình duyệt và truy cập:

- **🔐 Login Page:** http://localhost:3000
- **📚 API Documentation:** http://localhost:8000/docs
- **🎛️ Admin Dashboard:** http://localhost:3001
- **👨‍🏫 Lecturer Dashboard:** http://localhost:3000/dashboard.html

---

## 👤 Tài khoản Test (Tự động được tạo)

| Vai trò | Email | Mật khẩu |
|---------|-------|----------|
| **Admin** | admin@ut.edu.vn | admin123 |
| **Giảng viên** | lecturer@ut.edu.vn | lecturer123 |
| **Trưởng khoa** | hod@ut.edu.vn | hod123 |
| **Phòng Đào tạo** | aa@ut.edu.vn | aa123 |
| **Sinh viên** | student@ut.edu.vn | student123 |
| **Hiệu trưởng** | principal@ut.edu.vn | principal123 |

---

## 🔄 Nếu gặp vấn đề

### Lỗi: "Can't connect to MySQL"
```powershell
# Kiểm tra MySQL đang chạy
netstat -ano | findstr :3306
```
- Nếu không có output → Khởi động MySQL trong XAMPP

### Lỗi: "Database creation failed"
- Kiểm tra MySQL user/password trong `backend/app/core/config.py`
- Mặc định: `root` / không có password

### Lỗi: "Port already in use"
```powershell
# Tìm process đang dùng port
netstat -ano | findstr :8000

# Kill process (thay PID)
taskkill /PID <PID> /F
```

### Reset tài khoản nếu quên mật khẩu
```powershell
cd D:\CONG-NGHE-PHAN-MEM\backend
..\\.venv\Scripts\python.exe reset_passwords.py
```

---

## 📝 Tóm tắt

**KHÔNG CẦN:**
- ❌ Tạo database thủ công trong phpMyAdmin
- ❌ Chạy SQL scripts riêng
- ❌ Import users từ CSV
- ❌ Cấu hình phức tạp

**CHỈ CẦN:**
- ✅ Bật MySQL trong XAMPP
- ✅ Chạy backend → Tự động setup hết
- ✅ Chạy frontend → Login ngay

---

## 🆘 Hỗ trợ thêm

Xem chi tiết trong: [README.md](README.md)
