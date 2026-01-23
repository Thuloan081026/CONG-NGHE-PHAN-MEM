# 🚀 Hướng dẫn chạy Frontend và Backend Local

## 📋 Yêu cầu hệ thống
- Python 3.8 trở lên
- Trình duyệt web hiện đại (Chrome, Firefox, Edge)
- PowerShell hoặc Command Prompt

## ⚡ BƯỚC 1: Chạy Backend

### 1.1 Cài đặt Python dependencies
```powershell
# Mở PowerShell tại thư mục backend
cd d:\smd\backend

# Cài đặt các thư viện cần thiết
python -m pip install -r requirements.txt
```

### 1.2 Khởi động Backend Server
```powershell
# Vẫn ở thư mục backend
cd d:\smd\backend

# Chạy server FastAPI
uvicorn app.main:app --reload --port 8000
```

✅ Backend sẽ chạy tại: **http://localhost:8000**
✅ API Documentation: **http://localhost:8000/docs**

### 1.3 (Optional) Tạo dữ liệu mẫu
Mở terminal mới (PowerShell thứ 2):
```powershell
cd d:\smd\backend
python create_test_users.py
```

---

## 🎨 BƯỚC 2: Chạy Frontend

Frontend của bạn là **static HTML files**, không cần build hoặc npm install.

### Cách 1: Sử dụng Python HTTP Server (Khuyến nghị)
```powershell
# Mở PowerShell mới (thứ 2 hoặc 3)
cd d:\smd\frontend\lecturer-web

# Chạy simple HTTP server
python -m http.server 3000
```

✅ Frontend sẽ chạy tại: **http://localhost:3000**

### Cách 2: Mở trực tiếp file HTML
```powershell
# Chỉ cần double-click file HTML
# Ví dụ: 
# d:\smd\frontend\lecturer-web\test-login.html
# d:\smd\frontend\lecturer-web\dashboard.html
```

⚠️ **Lưu ý:** Cách 2 có thể gặp vấn đề CORS, nên dùng Cách 1.

---

## 🔗 Kết nối Frontend với Backend

Frontend đã được cấu hình kết nối tới Backend qua API URL:
```javascript
const API_URL = 'http://127.0.0.1:8000';
```

File có sẵn kết nối API:
- `frontend/lecturer-web/test-login.html` - Test đăng nhập
- `frontend/lecturer-web/test-all-features.html` - Test tất cả tính năng
- `frontend/lecturer-web/syllabus-create.html` - Tạo syllabus
- `frontend/lecturer-web/syllabus-list.html` - Xem danh sách syllabus

---

## 🧪 BƯỚC 3: Test Kết nối

### 3.1 Kiểm tra Backend hoạt động
Mở trình duyệt, truy cập:
```
http://localhost:8000/docs
```
Bạn sẽ thấy Swagger UI với danh sách API.

### 3.2 Test Login
1. Mở: `http://localhost:3000/test-login.html`
2. Sử dụng tài khoản mặc định:
   - Email: `lecturer@test.com`
   - Password: `lecturer123`
3. Click "Test Login"
4. Nếu thành công, bạn sẽ thấy access_token

### 3.3 Test Dashboard
Sau khi login thành công:
```
http://localhost:3000/dashboard.html
```

---

## 📝 Tài khoản test mặc định

Nếu bạn đã chạy `create_test_users.py`:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@smd.edu.vn` | `admin123` |
| Lecturer | `lecturer@test.com` | `lecturer123` |
| HOD | `hod@test.com` | `hod123` |
| Student | `student@test.com` | `student123` |

---

## 🐛 Xử lý lỗi thường gặp

### Lỗi 1: "ModuleNotFoundError"
```powershell
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi 2: "Port 8000 already in use"
```powershell
# Dùng port khác
uvicorn app.main:app --reload --port 8001
```
**Lưu ý:** Nếu đổi port, phải cập nhật API_URL trong file HTML.

### Lỗi 3: CORS Error
- Đảm bảo backend đang chạy
- Dùng `python -m http.server` thay vì mở trực tiếp file HTML

### Lỗi 4: "Cannot connect to API"
- Kiểm tra backend có đang chạy: `http://localhost:8000/docs`
- Kiểm tra firewall không chặn port 8000

---

## 📦 Tóm tắt các bước nhanh

```powershell
# Terminal 1 - Backend
cd d:\smd\backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend (Lecturer Web)
cd d:\smd\frontend\lecturer-web
python -m http.server 3000

# Terminal 3 - Frontend (Admin Web)
cd d:\smd\frontend\admin-web
python -m http.server 3001
```

**Truy cập:**
- Backend API: http://localhost:8000/docs
- Lecturer Web: http://localhost:3000
- Admin Web: http://localhost:3001

---

## 🎯 Next Steps

Sau khi test thành công:
1. Xem API documentation: http://localhost:8000/docs
2. Test các tính năng trong `test-all-features.html`
3. Tạo syllabus mới trong `syllabus-create.html`
4. Xem README.md trong từng module để biết thêm chi tiết

---

## 📞 Hỗ trợ

- Backend API Reference: `backend/API_REFERENCE.md`
- Quick Start Guide: `backend/QUICK_START.md`
- Frontend Structure: `frontend/README.md`
