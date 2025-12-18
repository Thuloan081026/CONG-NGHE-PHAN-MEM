# 🎯 HƯỚNG DẪN TEST ĐĂNG KÝ TÀI KHOẢN THỦ CÔNG

## 📋 **Bước 1: Chuẩn bị**

1. **Mở Terminal/Command Prompt**
2. **Di chuyển đến thư mục backend:**
   ```bash
   cd D:\project cnpm\backend
   ```

3. **Chạy script test thủ công:**
   ```bash
   & "D:/project cnpm/.venv/Scripts/python.exe" manual_test_registration.py
   ```

## 🎮 **Bước 2: Các tùy chọn test**

### **Tùy chọn 1: Test đăng ký thủ công**
- Chọn `1` trong menu
- Nhập thông tin tài khoản:
  - **Email**: Địa chỉ email (vd: `test@university.edu.vn`)
  - **Password**: Mật khẩu (tối thiểu 6 ký tự)
  - **Họ tên**: Tên đầy đủ
  - **Role**: student, lecturer, hod, aa, principal, reviewer

### **Tùy chọn 2: Test với data mẫu**
- Chọn `2` trong menu
- Script sẽ tự động tạo 3 users mẫu:
  - Sinh Viên Mẫu (student)
  - Giảng Viên Mẫu (lecturer)
  - Reviewer Mẫu (reviewer)

### **Tùy chọn 3: Xem danh sách users**
- Chọn `3` trong menu
- Hiển thị tất cả users hiện tại trong hệ thống

## 📊 **Bước 3: Kiểm tra kết quả**

### **Cách 1: Qua script**
- Script sẽ hiển thị kết quả trực tiếp:
  ```
  ✅ ĐĂNG KÝ THÀNH CÔNG!
     👤 ID: 15
     📧 Email: test@university.edu.vn
     👤 Tên: Nguyễn Văn Test
     🎭 Role: student
     ✅ Active: True
  ```

### **Cách 2: Qua phpMyAdmin**
1. Mở trình duyệt: http://localhost/phpmyadmin
2. Chọn database: `syllabus_db`
3. Click vào table: `users`
4. Xem data mới được thêm

## 🔍 **Bước 4: Test đăng nhập**

Sau khi đăng ký thành công, script sẽ tự động test đăng nhập:

```
🔐 Test đăng nhập...
✅ Đăng nhập thành công!
   👤 Xin chào: Nguyễn Văn Test
```

## ⚠️ **Lưu ý quan trọng**

### **Validation Rules:**
- ✅ Email phải chưa tồn tại trong hệ thống
- ✅ Password được hash tự động (không lưu plain text)
- ✅ Role phải là một trong: student, lecturer, hod, aa, principal, reviewer

### **Xử lý lỗi:**
- **"Email already registered"**: Email đã được sử dụng
- **Connection Error**: Kiểm tra XAMPP MySQL có chạy không
- **Validation Error**: Kiểm tra định dạng dữ liệu

## 🎯 **Ví dụ test hoàn chỉnh**

```
🎯 CHỌN CÁCH TEST:
1. Test đăng ký thủ công (nhập thông tin)
2. Test với data mẫu có sẵn
3. Xem danh sách users hiện tại
4. Thoát

Chọn (1-4): 1

📧 Email (mặc định: manual_test@university.edu.vn): test_student@university.edu.vn
🔒 Password (mặc định: test123): password123
👤 Họ tên đầy đủ (mặc định: Người Dùng Test): Nguyễn Văn Test
🎭 Role: student, lecturer, hod, aa, principal, reviewer
   Chọn role (mặc định: student): student

📋 THÔNG TIN ĐĂNG KÝ:
   📧 Email: test_student@university.edu.vn
   👤 Tên: Nguyễn Văn Test
   🎭 Role: student
   🔒 Password: **********

🚀 Tiến hành đăng ký? (y/n): y

⏳ Đang đăng ký tài khoản...
✅ ĐĂNG KÝ THÀNH CÔNG!
   👤 ID: 15
   📧 Email: test_student@university.edu.vn
   👤 Tên: Nguyễn Văn Test
   🎭 Role: student
   ✅ Active: True

🔐 Test đăng nhập...
✅ Đăng nhập thành công!
   👤 Xin chào: Nguyễn Văn Test
```

## 🚀 **Bắt đầu test ngay!**

Chạy lệnh sau trong terminal:

```bash
cd "D:\project cnpm\backend"
& "D:/project cnpm/.venv/Scripts/python.exe" manual_test_registration.py
```

**Chọn tùy chọn 1 để nhập thông tin thủ công và test!** 🎉