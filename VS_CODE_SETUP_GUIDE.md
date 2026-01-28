# 🚀 HƯỚNG DẪN CẤU HÌNH VS CODE - COMPLETE SETUP GUIDE

## ✅ Những gì đã được cấu hình

Tôi đã tạo sẵn toàn bộ file cấu hình VS Code cho bạn:

### 📁 File được tạo
- `.vscode/settings.json` - Cấu hình chung VS Code
- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Automation tasks
- `.vscode/extensions.json` - Khuyến nghị extensions

### 🔧 Cấu hình Python Environment
- ✅ Virtual Environment (.venv) đã được phát hiện
- ✅ Python 3.11.10 
- ✅ Tất cả dependencies đã cài đặt (FastAPI, SQLAlchemy, MySQL, etc.)

---

## 🎯 CÁCH CHẠY HỆ THỐNG

### **Cách 1: Chạy từ VS Code (Khuyến nghị)**

#### **Option 1: Chạy chỉ Backend**
1. **Mở Terminal trong VS Code** (Ctrl + `)
2. Chọn **Run → Run Without Debugging** hoặc nhấn `Ctrl+F5`
3. Chọn "Python: Backend FastAPI" từ dropdown

Backend sẽ chạy tại: **http://localhost:8000/docs**

#### **Option 2: Chạy Full Stack (Backend + Lecturer Web)**
1. **Mở Terminal trong VS Code** (Ctrl + `)
2. Chọn **Run → Run Without Debugging** hoặc nhấn `Ctrl+F5`
3. Chọn "Full Stack (Backend + Lecturer Web)" từ dropdown

Truy cập:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000/home.html

#### **Option 3: Dùng Tasks**
1. **Nhấn Ctrl+Shift+P** để mở Command Palette
2. Gõ `Run Task` → chọn task bạn muốn chạy:
   - "Backend: Run FastAPI Server"
   - "Frontend: Lecturer Web (port 3000)"
   - "Frontend: Admin Web (port 3001)"

### **Cách 2: Chạy từ Terminal (PowerShell)**

```powershell
# Mở Terminal tại thư mục workspace
cd "c:\Users\ngouy\OneDrive\Documents\CONG-NGHE-PHAN-MEM"

# Chạy Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Mở terminal mới (Shift+Alt++) - Chạy Frontend
cd frontend\lecturer-web
python -m http.server 3000
```

---

## 📋 TEST CHECKLIST

Sau khi chạy, kiểm tra danh sách sau:

- [ ] **Backend API**: http://localhost:8000/docs (nên thấy Swagger UI)
- [ ] **Frontend**: http://localhost:3000/home.html (nên thấy trang chủ)
- [ ] **Login test**: Sử dụng tài khoản `lecturer@test.com` / `lecturer123`
- [ ] **Dashboard**: Xem danh sách syllabus

---

## 🔐 Tài khoản Test Mặc định

| Vai trò | Email | Password |
|---------|-------|----------|
| **Admin** | admin@smd.edu.vn | admin123 |
| **Lecturer** | lecturer@test.com | lecturer123 |
| **HOD** | hod@test.com | hod123 |
| **Student** | student@test.com | student123 |

---

## 🆘 FIX LỖI THƯỜNG GẶP

### **Lỗi 1: "Module not found" - ModuleNotFoundError**
```powershell
# Cách fix
cd backend
pip install -r requirements.txt
```

### **Lỗi 2: "Port 8000 already in use"**
```powershell
# Tìm process đang sử dụng port 8000
netstat -ano | findstr :8000

# Kill process (thay PID_NUMBER bằng số từ kết quả trên)
taskkill /PID <PID_NUMBER> /F
```

### **Lỗi 3: "Cannot connect to MySQL"**
```
✅ Kiểm tra MySQL đã khởi động chưa
✅ Database URL trong app/core/config.py: 
   DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
✅ Thay user/password theo setup của bạn
```

### **Lỗi 4: Python không được nhận dạng**
```powershell
# Dùng lệnh này trong terminal
& ".venv/Scripts/Activate.ps1"

# Hoặc sử dụng Python executable đầy đủ
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

### **Lỗi 5: VS Code không tìm thấy Python**
1. **Ctrl+Shift+P** → `Python: Select Interpreter`
2. Chọn `.venv/Scripts/python.exe`

---

## 🎨 VS CODE EXTENSIONS (Tự động cài đặt được)

**Các extension được khuyến nghị:**
- `ms-python.python` - Python support
- `ms-python.vscode-pylance` - Python Language Server
- `ms-python.black-formatter` - Code formatter
- `charliermarsh.ruff` - Python linter
- `ms-vscode.rest-client` - REST API testing
- `eamodio.gitlens` - Git integration
- `ritwickdey.liveserver` - Live server (cho frontend)

**Cách cài:**
```powershell
# Hoặc cài lần lượt từ Extensions sidebar (Ctrl+Shift+X)
```

---

## 🔍 KIỂM TRA HEALTH SYSTEM

Chạy health check:
```powershell
cd "c:\Users\ngouy\OneDrive\Documents\CONG-NGHE-PHAN-MEM"
python check_health.py
```

---

## 📊 STRUCTURE DỰ ÁN

```
CONG-NGHE-PHAN-MEM/
├── .vscode/              ← VS Code config (đã tạo!)
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
├── backend/              ← FastAPI Server
│   ├── app/
│   │   ├── main.py      ← Entry point
│   │   ├── api/         ← API routes
│   │   └── core/        ← Config, database
│   └── requirements.txt
├── frontend/            ← Static HTML Files
│   ├── lecturer-web/    ← Port 3000
│   ├── admin-web/       ← Port 3001
│   └── ...
└── .venv/              ← Virtual environment
```

---

## 💡 TIPS & TRICKS

### **1. Auto-reload Backend**
Backend sẽ tự động reload khi bạn sửa code (đã cấu hình `--reload`)

### **2. Debug Mode**
Đặt breakpoint và nhấn **F5** để chạy debug mode

### **3. View Python Version**
```powershell
python --version
.venv/Scripts/python.exe --version
```

### **4. Check Active Dependencies**
```powershell
pip list
```

### **5. Run Specific Python File**
```powershell
# Trong VS Code: Click file → Run (Ctrl+F5)
# Hoặc trong terminal:
python filename.py
```

---

## 🎓 NEXT STEPS

1. ✅ **Đã setup VS Code** - Bạn có thể chạy lệnh ngay bây giờ!
2. 📌 **Chạy Backend**: Ctrl+Shift+P → "Run Task" → "Backend: Run FastAPI Server"
3. 📌 **Chạy Frontend**: Ctrl+Shift+P → "Run Task" → "Frontend: Lecturer Web (port 3000)"
4. 🌐 **Mở browser**: http://localhost:3000/home.html
5. 🧪 **Test**: Login với `lecturer@test.com` / `lecturer123`

---

## 📞 CẦN GỌI LẠI?

Nếu gặp vấn đề:
1. Kiểm tra terminal output (Panel dưới VS Code)
2. Chạy `check_health.py` để diagnose
3. Xem file lỗi chi tiết trong `.vscode/` logs

**Happy coding! 🚀**
