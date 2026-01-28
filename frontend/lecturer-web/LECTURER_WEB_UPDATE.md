# Hướng dẫn Đẩy Dữ liệu và Cải thiện Giao diện Lecturer Web

## 📋 Những gì đã được thực hiện

### 1. ✅ Cập nhật CSS Dashboard (lecturer-dashboard.css)
- **Màu xanh dương hài hòa**: Tất cả các card stats giờ sử dụng gradient xanh dương từ `#2563eb` → `#3b82f6` → `#60a5fa`
- **Thêm bóng (Shadow)**: Các card có bóng đôi (drop shadow + inner glow) với `box-shadow` tăng cường
- **Navigation đậm hơn**: 
  - `.nav-level` từ `font-weight: 700` → `font-weight: 900`
  - `.sidebar-menu > li > a` thêm `font-weight: 600`
  
#### Thay đổi Màu Card:
| Card Type | Màu cũ | Màu mới |
|-----------|--------|---------|
| Primary (Total) | Purple | Blue: `#2563eb` → `#60a5fa` |
| Success (Published) | Green | Green: `#059669` → `#34d399` |
| Warning (In Review) | Pink | Red: `#dc2626` → `#f87171` |
| Info (Draft) | Cyan | Cyan: `#0891b2` → `#22d3ee` |

### 2. ✅ Tạo Script Python Tạo Dữ liệu Demo
**File**: `backend/create_lecturer_web_data.py`

Tạo dữ liệu toàn diện cho 3 giảng viên:
- **12 Giáo trình** (Syllabuses)
  - 4 cho lecturer 1 (AI/ML focus): 3 published, 1 in_review
  - 4 cho lecturer 2 (Database/Systems): 2 published, 1 submitted, 1 draft
  - 4 cho lecturer 3 (Web/Frontend): 3 published, 1 in_review

- **36 CLO** (Course Learning Outcomes) - 3 CLO mỗi giáo trình
- **5 Review** với rating từ 4-5 sao
- **7 Thông báo** (Notifications) - lẫn đã đọc và chưa đọc
- **3 Hồ sơ Giảng viên** với thông tin chi tiết:
  - Full name, Employee ID, Degree, Title
  - Department, Phone, Office Location
  - Research Interests, Teaching Subjects
  - Qualifications, Publications

### 3. ✅ Cập nhật Profile.html (profile.html)
- Đã có logic lấy dữ liệu từ API: `GET /users/me`
- Hiển thị thông tin giảng viên: tên, email, khoa, chức danh
- Cho phép chỉnh sửa và lưu hồ sơ: `PUT /users/me`

### 4. ✅ Cập nhật Notifications.html (notifications.html)
- **Lấy dữ liệu API**: `GET /notifications?skip=0&limit=50`
- **Hiển thị danh sách thông báo** động từ backend
- **Thống kê**: Cập nhật số thông báo chưa đọc, đã đọc, tổng số
- **Lọc thông báo**: All, Unread, Phê duyệt (approve), Yêu cầu sửa (reject)
- **Đánh dấu đã đọc**: Click vào thông báo hoặc "Đánh dấu tất cả đã đọc"
- **Hiệu ứng**: Hover animation, border indicator cho chưa đọc

---

## 🚀 Hướng dẫn Chạy Script Tạo Dữ liệu

### Bước 1: Đảm bảo Backend Đang Chạy
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Bước 2: Chạy Script Tạo Dữ liệu
Từ thư mục `backend`, chạy:

```bash
python create_lecturer_web_data.py
```

**Output mong đợi:**
```
============================================================
🚀 Creating Comprehensive Lecturer Web Demo Data
============================================================

📚 Creating Lecturer Profiles...
  ✓ Created lecturer: Ts. Trần Thị Bích
  ✓ Created lecturer: ThS. Lê Văn Chính
  ✓ Created lecturer: Ks. Phạm Thị Linh

📖 Creating Comprehensive Syllabuses...
  ✓ Created: IT101 - Nhập môn Lập trình Python... (Status: published)
  [... 11 more syllabuses ...]

🎯 Creating Course Learning Outcomes (CLOs)...
  ✓ Created 36 CLOs

💬 Creating Reviews & Feedback...
  ✓ Created review for syllabus 1
  [... more reviews ...]

🔔 Creating Notifications...
  ✓ Created notification: 'Giáo trình mới được duyệt'
  [... more notifications ...]

============================================================
✅ Data Creation Summary:
   • Lecturers: 3
   • Syllabuses: 12
   • CLOs: 36
   • Reviews: 5
   • Notifications: 7
============================================================

✨ Demo data created successfully!

📝 Lecturer Accounts:
   • Email: lecturer1@hcmute.edu.vn
     Name: Ts. Trần Thị Bích
     Password: lecturer123

   • Email: lecturer2@hcmute.edu.vn
     Name: ThS. Lê Văn Chính
     Password: lecturer123

   • Email: lecturer3@hcmute.edu.vn
     Name: Ks. Phạm Thị Linh
     Password: lecturer123
```

### Bước 3: Đăng nhập và Kiểm tra
1. Truy cập: `http://localhost:3000/lecturer-web/dashboard.html`
2. Đăng nhập với một trong các tài khoản:
   - Email: `lecturer1@hcmute.edu.vn`
   - Password: `lecturer123`

3. Kiểm tra các page:
   - **Dashboard** (`/dashboard.html`): Hiển thị 12 giáo trình
   - **Syllabus List** (`/syllabus-list.html`): Danh sách với filter
   - **Profile** (`/profile.html`): Thông tin giảng viên từ API
   - **Notifications** (`/notifications.html`): 7 thông báo demo

---

## 🎨 Thay đổi Giao diện

### CSS Gradient Màu Xanh Dương Hài Hòa

**Tất cả stat cards hiện sử dụng:**
```css
/* Primary card (Total) */
background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #60a5fa 100%);
box-shadow: 0 8px 25px rgba(37, 99, 235, 0.35), 
            0 0 20px rgba(37, 99, 235, 0.15);

/* On hover */
box-shadow: 0 12px 35px rgba(37, 99, 235, 0.45),
            0 0 30px rgba(37, 99, 235, 0.25);
```

### Navigation Font Weight
- **Nav Levels** (NAVIGATION, SYLLABUS MANAGEMENT, etc.): `font-weight: 900` (rất đậm)
- **Menu Items**: `font-weight: 600` (đậm)
- **Active/Hover**: Thêm scale effect và color change

### Other Cards
- **Welcome Box**: Gradient xanh dương, shadow tương tự
- **Regular Cards**: Shadow tăng từ `rgba(0,0,0,0.08)` → `rgba(37, 99, 235, 0.15)`

---

## 📊 Dữ liệu Demo Chi Tiết

### Giảng viên (3 người)

#### 1. Ts. Trần Thị Bích (lecturer1@hcmute.edu.vn)
- **Chuyên môn**: AI, Machine Learning
- **Môn dạy**: 4 giáo trình (IT101-IT104)
- **Kinh nghiệm**: 8 năm
- **Trình độ**: Tiến sĩ Khoa học Máy tính

#### 2. ThS. Lê Văn Chính (lecturer2@hcmute.edu.vn)
- **Chuyên môn**: Phát triển phần mềm, Database
- **Môn dạy**: 4 giáo trình (IT201-IT204)
- **Kinh nghiệm**: 5 năm
- **Trình độ**: Thạc sĩ Kỹ thuật Phần mềm

#### 3. Ks. Phạm Thị Linh (lecturer3@hcmute.edu.vn)
- **Chuyên môn**: Web Development, UI/UX
- **Môn dạy**: 4 giáo trình (IT301-IT304)
- **Kinh nghiệm**: 6 năm
- **Trình độ**: Thạc sĩ Công nghệ Thông tin

### Giáo trình (12 cái)
Mỗi giáo trình có:
- Subject Code + Name
- Credits, Semester, Department
- Objectives, Content, Teaching Methods
- Assessment Methods + Weights
- 3-4 Textbooks tham khảo
- 3 CLOs (Course Learning Outcomes)
- Status: draft, submitted, in_review, hoặc published

### Trạng thái Giáo trình
| Status | Count | Description |
|--------|-------|-------------|
| Published | 6 | Giáo trình đã duyệt, có thể xem công khai |
| In Review | 2 | Đang chờ duyệt từ HoD |
| Submitted | 1 | Giảng viên gửi xét duyệt |
| Draft | 3 | Chưa gửi, dạng nháp |

### Thông báo (7 cái)
- 4 thông báo đã đọc
- 3 thông báo chưa đọc
- Loại: approve (2), reject (1), update (3), follow (1)

---

## ✨ Tính năng Đã Thêm/Cải Thiện

### Dashboard
✅ Màu xanh dương hài hòa trên tất cả card  
✅ Bóng (shadow) tăng cường trên card  
✅ Navigation text bolder (nổi bật hơn)  
✅ Dữ liệu thực từ 3 giảng viên  

### Syllabuses
✅ 12 giáo trình với chi tiết đầy đủ  
✅ Trạng thái khác nhau (draft, submitted, in_review, published)  
✅ Hiển thị đầy đủ trên syllabus-list.html  

### Profile
✅ Lấy dữ liệu từ API `/users/me`  
✅ Hiển thị tất cả thông tin giảng viên  
✅ Cho phép chỉnh sửa hồ sơ  

### Notifications
✅ Lấy dữ liệu từ API `/notifications`  
✅ Hiển thị đầy đủ 7 thông báo  
✅ Filter: All, Unread, Approve, Reject  
✅ Đánh dấu đã đọc  
✅ Thống kê tự động cập nhật  

---

## 🔧 Điều chỉnh Nếu Cần

### Thay đổi Số lượng Dữ liệu
Trong `create_lecturer_web_data.py`, chỉnh sửa:
```python
# Tăng số giáo trình
base_syllabuses_data = [...]  # Thêm các mục mới

# Tăng số thông báo
notifications_data = [...]  # Thêm các item mới
```

### Thay đổi Màu Gradient
Trong `lecturer-dashboard.css`:
```css
.stat-card {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 50%, #YOUR_COLOR3 100%);
}
```

### Thay đổi Font Weight Navigation
```css
.sidebar-menu .nav-level {
    font-weight: 900;  /* Có thể điều chỉnh: 700, 800, 900, bold */
}
```

---

## 📝 Ghi chú Quan trọng

1. **Không xóa file code**: Tất cả chỉnh sửa chỉ thêm hoặc chỉnh sửa, không xóa file
2. **Không dùng JavaScript**: HTML + Python/FastAPI API, CSS được tối ưu
3. **Dữ liệu Demo**: Hoàn toàn có thể xóa và tạo lại bất kỳ lúc nào
4. **API Endpoint**: `POST /notifications/{notif_id}/read` để đánh dấu đã đọc

---

## ✅ Checklist Hoàn tất

- [x] Cập nhật CSS dashboard (màu xanh dương, bóng, font đậm)
- [x] Tạo script Python demo data
- [x] 3 Giảng viên + Chi tiết hồ sơ
- [x] 12 Giáo trình + 36 CLOs
- [x] 5 Reviews
- [x] 7 Notifications
- [x] Profile.html lấy data từ API
- [x] Notifications.html lấy data từ API + filter
- [x] Tất cả page hiển thị đầy đủ dữ liệu

---

## 📞 Hỗ Trợ

Nếu gặp lỗi:
1. Kiểm tra backend đang chạy: `http://localhost:8000/docs`
2. Kiểm tra token trong localStorage
3. Mở F12 (DevTools) xem Network/Console logs
4. Chạy lại script: `python create_lecturer_web_data.py`

---

**Hoàn tất vào**: 23/01/2026  
**Thay đổi chính**: CSS (blue harmony + shadow + bold nav) + Demo Data (3 lecturers, 12 syllabuses, 36 CLOs, 7 notifications) + API integration (profile, notifications)
