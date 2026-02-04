# 🎨 Frontend Structure Overview

## 📁 Cấu trúc các module

```
frontend/
├── index.html                 # Login page (Port 3000)
├── admin-web/                 # Admin Portal (Port 3001)
│   └── html/                  # Static HTML files
├── lecturer-web/              # Lecturer Portal (Port 3002)
│   ├── dashboard.html
│   ├── syllabus-create.html
│   ├── syllabus-list.html
│   └── ...
├── hod-web/                   # Head of Department Portal
│   ├── dashboard.html
│   ├── syllabus-review.html
│   └── ...
├── academic-affairs-web/      # Academic Affairs Portal
├── principal-web/             # Principal Portal
├── student-web/               # Student Portal
└── shared/                    # Shared resources
    ├── css/
    ├── js/
    └── components/
```

## 🚀 Khởi chạy Frontend

### Yêu cầu:
- Python 3.x đã cài đặt
- Backend API đang chạy trên port 8000

### Các lệnh khởi chạy:

#### 1. Login Page (Port 3000)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend
python -m http.server 3000
```

#### 2. Admin Dashboard (Port 3001)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\admin-web\html
python -m http.server 3001
```

#### 3. Lecturer Dashboard (Port 3002)
```powershell
cd D:\CONG-NGHE-PHAN-MEM\frontend\lecturer-web
python -m http.server 3002
```

## 🔗 Access URLs

- **Login:** http://localhost:3000
- **Admin:** http://localhost:3001
- **Lecturer:** http://localhost:3002
- **HoD:** http://localhost:3002/hod-web/
- **Student:** http://localhost:3000/student-web/

## 📊 Tổng quan các Portal

| Portal | Pages | Main Features |
|--------|-------|---------------|
| **Admin** | 12 | User management, System settings, Reports |
| **Lecturer** | 10 | Create/Edit syllabus, View status |
| **HoD** | 9 | Review queue, Approval workflow |
| **Academic Affairs** | 11 | Final review, CLO-PLO validation |
| **Principal** | 6 | Strategic approval, Reports |
| **Student** | 8 | Search/View syllabus, Feedback |

## 🌐 API Integration

Tất cả frontend modules kết nối với Backend API:

```javascript
const API_BASE_URL = 'http://localhost:8000';
const token = localStorage.getItem('access_token');

// Example API call
fetch(`${API_BASE_URL}/syllabuses`, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

## 📱 Tech Stack

### Current (Simple deployment):
- **HTML5** - Static pages
- **CSS3** - Styling
- **Vanilla JavaScript** - Interactivity
- **Python HTTP Server** - Development server

### Future (Production ready):
- React/Next.js
- TypeScript
- Material-UI/Ant Design
- Redux Toolkit

## 🎯 Development Guidelines

1. **File Organization:** Mỗi portal có cấu trúc riêng
2. **Naming Convention:** kebab-case cho files HTML
3. **CSS:** Shared styles trong `/shared/css/`
4. **JavaScript:** Shared functions trong `/shared/js/`
5. **Assets:** Images, icons trong `/assets/`

## 🔐 Authentication Flow

```
1. User đăng nhập tại http://localhost:3000
2. Backend trả về access_token
3. Token được lưu vào localStorage
4. Frontend redirect đến dashboard tương ứng
5. Mỗi request API gửi kèm Bearer token
```

## 🛠️ Common Issues

### Lỗi CORS
- Đảm bảo Backend đã enable CORS
- Check `app/main.py` có `CORSMiddleware`

### Không load được static files
- Kiểm tra đường dẫn relative
- Đảm bảo đang chạy từ đúng thư mục

### Token expired
- Login lại để lấy token mới
- Token có thời hạn 60 phút

---

Xem README.md chính ở root directory để biết hướng dẫn chi tiết về cài đặt và khởi chạy toàn bộ hệ thống.

