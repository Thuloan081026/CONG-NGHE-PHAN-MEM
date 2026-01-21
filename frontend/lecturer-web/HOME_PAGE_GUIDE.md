# 🎯 Hướng dẫn sử dụng Trang chủ thông minh

## ✨ Tính năng mới

Bây giờ bạn chỉ cần truy cập **http://localhost:3000/home.html** và hệ thống sẽ tự động:

✅ Kiểm tra đăng nhập  
✅ Xác thực quyền (role)  
✅ Hiển thị menu phù hợp với vai trò  
✅ Chuyển đến trang phù hợp khi click  

**KHÔNG CẦN NHỚ LINK GÌ HẾT!**

---

## 🚀 Cách sử dụng

### Bước 1: Mở trình duyệt
```
http://localhost:3000/home.html
```

### Bước 2: Đăng nhập nhanh
Click vào một trong các nút:
- 👨‍💼 **Admin** 
- 👨‍🏫 **Giảng viên**
- 👔 **Trưởng khoa**
- 🎓 **Sinh viên**

### Bước 3: Xem Dashboard
Hệ thống tự động hiển thị các tính năng phù hợp với vai trò của bạn!

---

## 📱 Menu theo vai trò

### 👨‍💼 Admin thấy:
- 📊 Dashboard Admin
- 👥 Quản lý Users
- 📚 Tất cả Syllabus
- ⚙️ Cài đặt
- 🧪 Test Features

### 👨‍🏫 Giảng viên thấy:
- 📊 Dashboard
- ➕ Tạo Syllabus
- 📝 Đề cương của tôi
- 🤝 Cộng tác Review
- 👤 Hồ sơ

### 👔 Trưởng khoa thấy:
- 📊 Dashboard
- ✅ Duyệt Syllabus
- 👥 Giảng viên
- 📈 Báo cáo

### 🎓 Sinh viên thấy:
- 📚 Xem Syllabus
- 🔍 Tìm kiếm
- 👤 Thông tin cá nhân

---

## 🔐 Tài khoản Demo

| Vai trò | Email | Password |
|---------|-------|----------|
| Admin | admin@smd.edu.vn | admin123 |
| Giảng viên | lecturer@test.com | lecturer123 |
| Trưởng khoa | hod@test.com | hod123 |
| Sinh viên | student@test.com | student123 |

---

## 💡 Tính năng thông minh

### 1. Tự động kiểm tra đăng nhập
- Nếu đã login → Hiển thị Dashboard ngay
- Nếu chưa login → Hiển thị form đăng nhập

### 2. Nhớ phiên làm việc
- Token được lưu trong localStorage
- Không cần đăng nhập lại khi refresh trang
- Tự động logout khi token hết hạn

### 3. Phân quyền tự động
- Mỗi role thấy menu khác nhau
- Tự động điều hướng đến trang phù hợp
- Bảo mật: Backend sẽ verify lại quyền

### 4. Quick Login
- 1 click để login với tài khoản demo
- Tiết kiệm thời gian test
- Không cần nhớ email/password

---

## 🎨 Giao diện

### Màn hình Loading
- Hiển thị khi kiểm tra authentication
- Spinner animation đẹp mắt

### Màn hình Login
- Form đăng nhập
- Quick login buttons (4 roles)
- Thông báo lỗi/thành công rõ ràng

### Màn hình Dashboard
- Banner chào mừng với tên user
- Grid menu với icon
- Thông tin user + nút logout

---

## 🔄 Workflow sử dụng

```
1. Truy cập: http://localhost:3000/home.html
   ↓
2. Hệ thống check token trong localStorage
   ↓
3a. Nếu có token hợp lệ:
    → Gọi API /users/me
    → Lấy thông tin user
    → Hiển thị Dashboard với menu theo role
   
3b. Nếu không có token:
    → Hiển thị form login
    → User chọn Quick Login hoặc nhập thủ công
    → Login thành công → Lưu token → Hiển thị Dashboard
   ↓
4. User click vào menu item
   → Chuyển đến trang tương ứng
   ↓
5. Khi xong, click "Đăng xuất"
   → Xóa token
   → Quay về màn hình login
```

---

## 🛠️ Kỹ thuật

### LocalStorage
```javascript
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', refresh);
localStorage.getItem('access_token');
localStorage.clear(); // Logout
```

### API Calls
```javascript
// Check auth
GET /users/me
Headers: { Authorization: 'Bearer <token>' }

// Login
POST /auth/login
Body: { email, password }
Response: { access_token, refresh_token }
```

### Role-based Menu
```javascript
const ROLE_MENUS = {
  admin: [...],
  lecturer: [...],
  hod: [...],
  student: [...]
}
```

---

## 🐛 Troubleshooting

### Lỗi "Không thể kết nối server"
**Nguyên nhân:** Backend chưa chạy  
**Giải pháp:** 
```powershell
cd d:\smd\backend
uvicorn app.main:app --reload --port 8000
```

### Lỗi "Đăng nhập thất bại"
**Nguyên nhân:** Sai email/password hoặc user không tồn tại  
**Giải pháp:** 
- Dùng Quick Login
- Hoặc tạo user: `python create_test_users.py`

### Token hết hạn
**Hiện tượng:** Bị logout tự động  
**Nguyên nhân:** Token expired (mặc định 60 phút)  
**Giải pháp:** Đăng nhập lại

### Menu không hiển thị đúng
**Nguyên nhân:** Role trong database không khớp  
**Giải pháp:** Check API response trong F12 Console

---

## 📂 Files liên quan

```
frontend/lecturer-web/
├── home.html                    ← Trang chủ mới (QUAN TRỌNG)
├── index-redirect.html          ← Redirect helper
├── dashboard.html               ← Dashboard cũ
├── syllabus-create.html         ← Tạo syllabus
├── syllabus-list.html           ← Danh sách syllabus
├── collaborative-review.html    ← Review
└── test-all-features.html       ← Test features
```

---

## 🎯 So sánh trước và sau

### ❌ Trước đây:
```
1. Phải nhớ: http://localhost:3000/test-login.html
2. Login thủ công
3. Nhớ link từng trang:
   - /syllabus-create.html
   - /syllabus-list.html
   - /dashboard.html
4. Không có menu điều hướng
5. Mỗi lần refresh phải login lại
```

### ✅ Bây giờ:
```
1. Chỉ cần: http://localhost:3000/home.html
2. Quick login 1 click
3. Menu tự động hiển thị tất cả trang
4. Click vào menu để chuyển trang
5. Không cần login lại (nhớ phiên)
```

---

## 🚀 Lợi ích

✅ **Dễ dùng hơn:** 1 URL duy nhất  
✅ **Nhanh hơn:** Quick login buttons  
✅ **Thông minh hơn:** Tự động phân quyền  
✅ **Chuyên nghiệp hơn:** Giao diện đẹp, UX tốt  
✅ **Bảo mật hơn:** Token-based auth  

---

## 📖 Hướng dẫn cho Developer

### Thêm menu item mới
```javascript
// Trong home.html, tìm ROLE_MENUS
const ROLE_MENUS = {
  lecturer: [
    { 
      icon: '🆕', 
      title: 'Tính năng mới', 
      desc: 'Mô tả ngắn', 
      url: 'new-feature.html' 
    },
    // ... các item khác
  ]
}
```

### Thêm role mới
```javascript
const ROLE_MENUS = {
  // ... existing roles
  new_role: [
    { icon: '📋', title: 'Menu 1', desc: 'Desc', url: 'page1.html' }
  ]
};

const roleNames = {
  // ... existing
  new_role: 'Tên Role Mới'
};
```

### Thay đổi API URL
```javascript
// Đầu file home.html
const API_URL = 'http://127.0.0.1:8000'; // Đổi URL này
```

---

## ✨ Demo Video (Mô tả)

```
1. Mở browser → http://localhost:3000/home.html
2. Thấy màn hình loading (2 giây)
3. Hiển thị form login với 4 quick buttons
4. Click "👨‍🏫 Giảng viên"
5. Loading... → Đăng nhập thành công!
6. Thấy Dashboard với:
   - Banner "Chào mừng, Lecturer Test!"
   - 5 menu cards: Dashboard, Tạo Syllabus, ...
7. Click "➕ Tạo Syllabus" → Chuyển đến trang tạo
8. Click "🚪 Đăng xuất" → Quay về login
```

---

## 🎓 Kết luận

Bây giờ hệ thống đã **HOÀN TOÀN TỰ ĐỘNG**:
- ✅ Không cần nhớ link
- ✅ Tự động login/logout
- ✅ Tự động phân quyền
- ✅ Menu điều hướng thông minh

**Chỉ cần nhớ 1 URL:** `http://localhost:3000/home.html`

**Thời gian sử dụng:** < 5 giây từ mở browser đến vào dashboard!

---

**Happy Coding! 🎉**
