# 🚀 Hướng Dẫn Khởi Chạy Dự Án SMD

## ✅ Trạng thái hiện tại
- **Backend**: ✅ Đang chạy trên `http://localhost:8000`
- **Frontend**: ✅ Đang chạy trên `http://localhost:3000`

## 📋 Các bước đã thực hiện

### 1. Backend Setup
- Python environment: `Python 3.13.2` (Virtual Environment)
- Đã cài đặt tất cả dependencies từ `requirements.txt`
- FastAPI server đang chạy với uvicorn
- CORS đã được cấu hình cho phép tất cả origins (development mode)

### 2. Frontend Setup
- Static HTML files được serve qua Python HTTP server
- Port 3000 đang hoạt động

## 🌐 Truy cập ứng dụng

### Trang đăng nhập:
```
http://localhost:3000/index.html
```

### Tài khoản test:
- **Admin**: 
  - Email: `admin@hcmute.edu.vn`
  - Password: `admin123`
  
- **Lecturer**: 
  - Email: `lecturer1@hcmute.edu.vn`
  - Password: `lecturer123`

### Backend API:
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

## 🔄 Khởi động lại servers

### Backend (Terminal 1):
```powershell
cd D:\smd\backend
D:/smd/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend (Terminal 2):
```powershell
cd D:\smd\frontend
D:/smd/.venv/Scripts/python.exe -m http.server 3000
```

## 🔍 Kiểm tra kết nối

Test backend API:
```powershell
D:/smd/.venv/Scripts/python.exe -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

Kết quả mong đợi:
```json
{"status": "healthy", "message": "Backend API is running"}
```

## 📁 Cấu trúc Dashboard theo Role

Sau khi login, hệ thống sẽ redirect đến dashboard tương ứng:

- **Admin**: `http://localhost:3000/admin-web/html/dashboard.html`
- **Lecturer**: `http://localhost:3000/lecturer-web/dashboard.html`
- **HOD**: `http://localhost:3000/lecturer-web/dashboard.html`

## ⚙️ Cấu hình CORS

Backend đã được cấu hình CORS cho phép:
- Allow all origins: `["*"]`
- Allow all methods: `["*"]`
- Allow all headers: `["*"]`

File cấu hình: `backend/app/main.py` (line 34-41)

## 📝 Lưu ý

1. **Backend** phải chạy trước khi frontend có thể kết nối
2. **Port conflicts**: Đảm bảo port 8000 và 3000 không bị chiếm dụng
3. **Database**: Backend sử dụng SQLite hoặc MySQL (kiểm tra `backend/app/core/database.py`)
4. **Auto-reload**: Backend có tính năng auto-reload khi code thay đổi

## 🛠️ Troubleshooting

### Backend không khởi động được:
```powershell
# Kiểm tra port 8000 có bị chiếm không
netstat -ano | findstr :8000

# Kill process nếu cần
taskkill /PID <PID> /F
```

### Frontend không load được:
```powershell
# Kiểm tra port 3000
netstat -ano | findstr :3000

# Hoặc dùng port khác
python -m http.server 3001
```

### CORS errors:
- Kiểm tra backend đã chạy chưa
- Xem console browser để biết chi tiết lỗi
- Đảm bảo `API_URL` trong `index.html` đúng là `http://localhost:8000`

## 📦 Dependencies

Backend đã cài đặt:
- fastapi (0.128.0)
- uvicorn (0.40.0)
- SQLAlchemy (2.0.45)
- PyJWT (2.10.1)
- passlib (1.7.4)
- pymysql (1.1.2)
- và nhiều packages khác...

Xem đầy đủ trong `backend/requirements.txt`
