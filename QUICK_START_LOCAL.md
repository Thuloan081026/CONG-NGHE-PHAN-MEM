# 🚀 QUICK START - Chạy Local trong 3 phút!

## ⚡ Cách nhanh nhất

### Bước 1: Double-click file này
```
start-local.bat
```

### Bước 2: Chọn option 4 hoặc 5
- **Option 4**: Backend + Lecturer (Khuyến nghị để test)
- **Option 5**: Tất cả (Backend + Lecturer + Admin)

### Bước 3: Đợi servers khởi động (5-10 giây)

### Bước 4: Mở trình duyệt
- **Test Login**: http://localhost:3000/test-login.html
- **Dashboard**: http://localhost:3000/dashboard.html
- **API Docs**: http://localhost:8000/docs

---

## 📋 URLs quan trọng

| Service | URL | Mô tả |
|---------|-----|-------|
| **🏠 TRANG CHỦ** | **http://localhost:3000/home.html** | **Trang chủ thông minh - Chỉ cần nhớ URL này!** |
| **Backend API** | http://localhost:8000/docs | API documentation (Swagger) |
| **Lecturer Web** | http://localhost:3000 | Giao diện giảng viên |
| **Admin Web** | http://localhost:3001 | Giao diện admin |
| **Test Login** | http://localhost:3000/test-login.html | Test đăng nhập (cũ) |

---

## 🔐 Tài khoản test

| Vai trò | Email | Password |
|---------|-------|----------|
| **Admin** | admin@smd.edu.vn | admin123 |
| **Lecturer** | lecturer@test.com | lecturer123 |
| **HOD** | hod@test.com | hod123 |

---

## 🎯 Test Checklist

- [ ] Backend chạy: http://localhost:8000/docs
- [ ] Frontend chạy: http://localhost:3000
- [ ] Login thành công với `lecturer@test.com`
- [ ] Dashboard hiển thị đúng
- [ ] Xem danh sách syllabus

---

## 🐛 Lỗi thường gặp

### "Port 8000 already in use"
```powershell
# Tìm và kill process
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### "Module not found"
```powershell
cd d:\smd\backend
pip install -r requirements.txt
```

### "Cannot connect to API"
- Kiểm tra Backend có chạy không: http://localhost:8000/docs
- Restart backend server

---

## 📁 File paths

```
d:\smd\
├── start-local.bat          ← Double-click để chạy
├── LOCAL_SETUP_GUIDE.md     ← Hướng dẫn chi tiết
├── backend\                 ← Backend API
│   └── app\main.py
└── frontend\
    ├── lecturer-web\        ← Giao diện giảng viên
    └── admin-web\           ← Giao diện admin
```

---

## 💡 Tips

1. **Khuyến nghị**: Dùng `start-local.bat` option 4 để test nhanh
2. **Debug**: Xem console của browser (F12) để check lỗi
3. **API Test**: Dùng Swagger UI tại http://localhost:8000/docs
4. **Reload**: Sau khi sửa code backend, server tự reload
5. **Stop**: Ctrl+C trong terminal để dừng server

---

## 🎓 Học thêm

- **API Reference**: `backend/API_REFERENCE.md`
- **Quick Start**: `backend/QUICK_START.md`
- **Frontend Guide**: `frontend/README.md`
- **Full Setup Guide**: `LOCAL_SETUP_GUIDE.md`

---

## ✅ Checklist cài đặt lần đầu

- [ ] Python 3.8+ đã cài
- [ ] Đã chạy `pip install -r requirements.txt`
- [ ] Database file `database.db` đã có
- [ ] Đã tạo test users (optional)

---

## 🔄 Workflow hàng ngày

```powershell
# 1. Mở PowerShell
# 2. Chạy file bat
start-local.bat

# 3. Chọn option 4
# 4. Mở browser: http://localhost:3000
# 5. Login: lecturer@test.com / lecturer123
# 6. Bắt đầu làm việc!
```

---

## 📞 Quick Commands

```powershell
# Backend only
cd d:\smd\backend
uvicorn app.main:app --reload --port 8000

# Frontend only  
cd d:\smd\frontend\lecturer-web
python -m http.server 3000

# Check ports
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

---

**Thời gian setup**: ~3 phút (nếu đã cài Python)  
**Difficulty**: ⭐ Rất dễ

**Chúc bạn code vui vẻ! 🎉**
