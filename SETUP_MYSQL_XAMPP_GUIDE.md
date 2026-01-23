# 🎓 HƯỚNG DẪN SETUP DATABASE MYSQL VỚI XAMPP

## 📋 YÊU CẦU

1. ✅ XAMPP đã cài đặt
2. ✅ Python 3.8+ đã cài đặt
3. ✅ Backend dependencies đã cài đặt

---

## 🚀 BƯỚC 1: KHỞI ĐỘNG XAMPP

### Windows:
1. Mở XAMPP Control Panel
2. Click **Start** cho **Apache**
3. Click **Start** cho **MySQL**
4. Đợi đến khi cả 2 service chuyển sang màu xanh

### Kiểm tra MySQL:
- Mở browser: `http://localhost/phpmyadmin`
- Nếu hiển thị phpMyAdmin -> MySQL đã chạy thành công ✅

---

## 🚀 BƯỚC 2: CÀI ĐẶT PYMYSQL

Mở terminal trong thư mục backend:

```bash
cd d:\smd\backend
D:/smd/.venv/Scripts/python.exe -m pip install pymysql
```

Hoặc nếu dùng pip bình thường:
```bash
pip install pymysql
```

---

## 🚀 BƯỚC 3: TẠO DATABASE

Chạy script setup database:

```bash
cd d:\smd\backend
D:/smd/.venv/Scripts/python.exe setup_mysql_database.py
```

**Script này sẽ:**
- ✅ Tạo database `smd_db`
- ✅ Tạo tất cả tables cần thiết
- ✅ Verify setup

**Output mong đợi:**
```
✅ Database 'smd_db' created successfully!
✅ Successfully created tables
✅ Database verification successful!
```

---

## 🚀 BƯỚC 4: TẠO TEST USERS

Chạy script tạo users:

```bash
cd d:\smd\backend
D:/smd/.venv/Scripts/python.exe create_test_users_mysql.py
```

**Script này sẽ tạo 6 tài khoản test:**

1. **Admin**
   - Email: `admin@hcmute.edu.vn`
   - Password: `admin123`
   - Role: `admin`
   - Dashboard: `/admin-web/html/dashboard.html`

2. **HoD (Head of Department)** ⭐
   - Email: `hod@hcmute.edu.vn`
   - Password: `hod123`
   - Role: `hod`
   - Dashboard: `/hod-web/dashboard.html`

3. **Lecturer 1**
   - Email: `lecturer1@hcmute.edu.vn`
   - Password: `lecturer123`
   - Role: `lecturer`
   - Dashboard: `/lecturer-web/dashboard.html`

4. **Lecturer 2**
   - Email: `lecturer2@hcmute.edu.vn`
   - Password: `lecturer123`
   - Role: `lecturer`

5. **Academic Affairs**
   - Email: `aa@hcmute.edu.vn`
   - Password: `aa123`
   - Role: `academic_affairs`

6. **Student**
   - Email: `student@hcmute.edu.vn`
   - Password: `student123`
   - Role: `student`

---

## 🚀 BƯỚC 5: CẬP NHẬT BACKEND CONFIG

### Option 1: Sử dụng Environment Variable (Khuyến nghị)

Tạo file `.env` trong thư mục `backend`:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/smd_db
SECRET_KEY=your-secret-key-here-change-in-production
```

### Option 2: Sửa trực tiếp file config.py

Mở file `d:\smd\backend\app\core\config.py` và sửa:

```python
DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/smd_db"
```

---

## 🚀 BƯỚC 6: KHỞI ĐỘNG HỆ THỐNG

### Terminal 1 - Backend:
```bash
cd d:\smd\backend
D:/smd/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2 - Frontend:
```bash
cd d:\smd\frontend
D:/smd/.venv/Scripts/python.exe -m http.server 3000
```

---

## 🚀 BƯỚC 7: TEST ĐĂNG NHẬP

1. Mở browser: `http://localhost:3000/index.html`

2. **Test HoD Login:**
   - Email: `hod@hcmute.edu.vn`
   - Password: `hod123`
   - Expected: Tự động chuyển đến `http://localhost:3000/hod-web/dashboard.html`

3. **Test Admin Login:**
   - Email: `admin@hcmute.edu.vn`
   - Password: `admin123`
   - Expected: Tự động chuyển đến `http://localhost:3000/admin-web/html/dashboard.html`

4. **Test Lecturer Login:**
   - Email: `lecturer1@hcmute.edu.vn`
   - Password: `lecturer123`
   - Expected: Tự động chuyển đến `http://localhost:3000/lecturer-web/dashboard.html`

---

## 🔍 KIỂM TRA DATABASE

### Qua phpMyAdmin:
1. Mở: `http://localhost/phpmyadmin`
2. Click vào database `smd_db`
3. Click vào table `users`
4. Tab `Browse` để xem tất cả users

### Qua SQL Query:
```sql
SELECT id, email, full_name, role, is_active 
FROM users 
ORDER BY role;
```

Expected result: 6 users với các role khác nhau

---

## ✅ WORKFLOW TỰ ĐỘNG NHẬN DIỆN ROLE

Hệ thống đã được config để tự động nhận diện role:

```
1. User nhập email + password
        ↓
2. Backend kiểm tra credentials
        ↓
3. Backend trả về user info + role
        ↓
4. Frontend nhận role và tự động redirect:
   - admin → /admin-web/html/dashboard.html
   - hod → /hod-web/dashboard.html
   - lecturer → /lecturer-web/dashboard.html
   - academic_affairs → /admin-web/html/dashboard.html
   - student → /student-web/index.html
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: "Can't connect to MySQL server"
**Giải pháp:**
- Kiểm tra XAMPP MySQL đã start chưa
- Kiểm tra port 3306 có bị chiếm chưa
- Restart XAMPP MySQL service

### Lỗi: "Access denied for user 'root'@'localhost'"
**Giải pháp:**
- XAMPP mặc định root không có password
- Nếu đã set password, update trong script:
  ```python
  MYSQL_PASSWORD = "your_password"
  ```

### Lỗi: "No module named 'pymysql'"
**Giải pháp:**
```bash
pip install pymysql
```

### Lỗi: "Database 'smd_db' doesn't exist"
**Giải pháp:**
- Chạy lại: `python setup_mysql_database.py`

### Login thành công nhưng không redirect
**Kiểm tra:**
1. Console browser (F12) có lỗi gì không
2. Backend có trả về đúng role không
3. Check file `index.html` dòng 174-179 có đúng URL không

---

## 📊 CẤU TRÚC DATABASE

### Table: users
```sql
- id (PRIMARY KEY, AUTO_INCREMENT)
- email (UNIQUE, VARCHAR)
- hashed_password (VARCHAR)
- full_name (VARCHAR)
- role (ENUM: admin, hod, lecturer, academic_affairs, student)
- department (VARCHAR, NULLABLE)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## 🎯 KIỂM TRA HOÀN TẤT

Checklist sau khi setup:

- [ ] XAMPP MySQL đã running
- [ ] Database `smd_db` đã tạo
- [ ] 6 test users đã tạo trong table `users`
- [ ] Backend đang chạy trên port 8000
- [ ] Frontend đang chạy trên port 3000
- [ ] Login HoD redirect đúng sang `/hod-web/dashboard.html`
- [ ] Login Admin redirect đúng sang `/admin-web/html/dashboard.html`
- [ ] Login Lecturer redirect đúng sang `/lecturer-web/dashboard.html`

---

## 📝 NOTES

### Về Security:
- ⚠️ Passwords đang là plain text trong script (chỉ dùng cho development)
- ⚠️ Production cần hash passwords và dùng environment variables
- ⚠️ SECRET_KEY cần thay đổi trong production

### Về Database:
- MySQL charset: `utf8mb4_unicode_ci` (support Vietnamese)
- Connection pool: Tự động quản lý bởi SQLAlchemy
- Sessions: Tự động đóng sau mỗi request

### Về Authentication:
- JWT tokens được lưu trong localStorage
- Access token expire: 60 phút
- Refresh token expire: 7 ngày

---

## 🎉 SUCCESS!

Nếu tất cả steps trên đã hoàn thành:

✅ **Database đã setup xong!**
✅ **Users đã được tạo!**
✅ **Hệ thống sẵn sàng sử dụng!**

**Login ngay tại:** `http://localhost:3000/index.html`

**Test với HoD account:**
- Email: `hod@hcmute.edu.vn`
- Password: `hod123`

Sau khi login thành công, bạn sẽ được tự động chuyển đến HoD Dashboard! 🎊

---

## 📞 SUPPORT

Nếu gặp vấn đề, kiểm tra:
1. XAMPP Control Panel - MySQL running
2. Terminal backend - Có lỗi gì không
3. Terminal frontend - Có lỗi gì không
4. Browser Console (F12) - Có lỗi JavaScript không
5. Network tab - API calls có thành công không

---

© 2026 SMD System - HCMUTE
