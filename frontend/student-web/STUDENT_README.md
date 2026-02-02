# Student Web Portal - SMD System

## 📖 Giới thiệu

Student Web Portal là giao diện dành cho Sinh viên trong Hệ thống Quản lý và Số hóa Giáo trình (SMD). Được xây dựng dựa trên **Ruang Admin** theme.

## ✨ Tính năng chính

### 1. Dashboard
- Thống kê tổng quan (Giáo trình công khai, Đang theo dõi, Chương trình đào tạo, Cập nhật gần đây)
- Danh sách giáo trình mới cập nhật
- Giáo trình đang theo dõi
- Nút theo dõi/bỏ theo dõi nhanh

### 2. Tìm kiếm Giáo trình
- Tìm kiếm theo Mã môn học / Tên môn học
- Lọc theo Chuyên ngành
- Lọc theo Học kỳ
- Hiển thị kết quả dạng bảng với DataTables
- Xem chi tiết và theo dõi giáo trình

### 3. Chi tiết Giáo trình
- **AI Summary**: Tóm tắt thông minh nội dung môn học
- **Subject Tree**: Cây môn học liên quan (Tiên quyết, Hiện tại, Tiếp theo)
- **PLO Mapping**: Ma trận chuẩn đầu ra chương trình
- Nội dung giáo trình chi tiết (Accordion)
- Tải xuống PDF
- Báo lỗi giáo trình

### 4. Giáo trình theo dõi
- Hiển thị tất cả giáo trình đang theo dõi
- Thống kê: Tổng số, Có cập nhật mới, Chưa cập nhật
- Thông báo cập nhật mới
- Bỏ theo dõi giáo trình

### 5. Thông tin cá nhân
- Xem và chỉnh sửa thông tin cá nhân
- Đổi mật khẩu
- Cài đặt thông báo (Email, Cập nhật giáo trình, Tin tức)
- Tiến độ học tập (Tín chỉ hoàn thành, GPA, Môn đã hoàn thành, Học kỳ hiện tại)

## 🎨 Theme & UI

- **Theme**: Ruang Admin (Bootstrap 4)
- **Icons**: Font Awesome 5
- **Charts**: Chart.js (trong dashboard)
- **Tables**: DataTables
- **Colors**: 
  - Primary: Blue (#4e73df)
  - Success: Green (#1cc88a)
  - Warning: Yellow (#f6c23e)
  - Danger: Red (#e74a3b)

## 📁 Cấu trúc trang

```
student-web/
├── dashboard.html              # Trang chủ Dashboard
├── syllabus-search.html       # Tìm kiếm giáo trình
├── syllabus-detail.html       # Chi tiết giáo trình (AI Summary, Subject Tree, PLO Map)
├── my-subscriptions.html      # Giáo trình đang theo dõi
├── profile.html               # Thông tin cá nhân
├── css/                       # Stylesheet files
├── js/                        # JavaScript files
├── vendor/                    # Third-party libraries
└── img/                       # Images and logos
```

## 🔐 Tài khoản test

- **Email**: student@hcmute.edu.vn
- **Password**: st123
- **Role**: student

## 🚀 Hướng dẫn sử dụng

### 1. Đăng nhập
- Truy cập: `http://localhost:3000/`
- Nhập email: `student@hcmute.edu.vn` và password: `st123`
- Hệ thống tự động redirect đến Student Dashboard

### 2. Xem Dashboard
- Xem thống kê tổng quan
- Danh sách giáo trình mới cập nhật
- Giáo trình đang theo dõi

### 3. Tìm kiếm giáo trình
- Click "Tìm kiếm Giáo trình" trong menu
- Nhập từ khóa hoặc chọn bộ lọc
- Xem kết quả và click "Xem" để xem chi tiết

### 4. Xem chi tiết giáo trình
- **AI Summary**: Đọc tóm tắt nội dung môn học
- **Subject Tree**: Xem môn tiên quyết và môn tiếp theo
- **PLO Mapping**: Kiểm tra chuẩn đầu ra chương trình
- Đọc nội dung chi tiết từng phần (Accordion)
- Click "Theo dõi" để nhận thông báo cập nhật
- Click "Tải PDF" để tải giáo trình
- Click "Báo lỗi" nếu phát hiện sai sót

### 5. Quản lý giáo trình theo dõi
- Click "Giáo trình theo dõi" trong menu
- Xem danh sách tất cả môn đang theo dõi
- Các môn có cập nhật mới sẽ hiển thị badge màu vàng
- Click "Bỏ theo dõi" để ngừng nhận thông báo

### 6. Cập nhật thông tin cá nhân
- Click "Thông tin cá nhân" trong menu
- Click "Chỉnh sửa" để cập nhật thông tin
- Đổi mật khẩu trong phần "Đổi mật khẩu"
- Bật/tắt thông báo trong "Cài đặt thông báo"

## 🔧 Kết nối Backend API

Các trang đã có placeholder cho API calls:

```javascript
const API_BASE_URL = 'http://localhost:8000';

// Authentication check
GET /users/me

// Dashboard data
GET /api/student/dashboard

// Syllabus search
GET /syllabuses?keyword=...&major=...&semester=...

// Syllabus detail
GET /syllabuses/{id}
GET /syllabuses/{id}/ai-summary
GET /syllabuses/{id}/subject-tree
GET /syllabuses/{id}/plo-mapping

// Subscriptions
POST /syllabuses/{id}/subscribe
DELETE /syllabuses/{id}/unsubscribe
GET /students/subscriptions

// Profile
GET /students/profile
PUT /students/profile
PUT /students/change-password

// Report error
POST /syllabuses/{id}/report-error
```

## 📊 Các tính năng đặc biệt

### AI Summary
- Tóm tắt tự động nội dung môn học
- Hiển thị kiến thức chính và kỹ năng đạt được
- Giúp sinh viên hiểu nhanh nội dung môn học

### Subject Tree
- Hiển thị môn tiên quyết (Prerequisite)
- Hiển thị môn đang xem (Current)
- Hiển thị môn tiếp theo (Next Courses)
- Giúp sinh viên lập kế hoạch học tập

### PLO Mapping
- Ma trận chuẩn đầu ra chương trình
- Hiển thị mức độ đạt từng PLO
- Giúp sinh viên hiểu mục tiêu học tập

## 🎯 Workflow Student

```
1. Login → Student Dashboard
2. Xem giáo trình mới cập nhật
3. Tìm kiếm giáo trình quan tâm
4. Xem chi tiết + AI Summary + Subject Tree
5. Theo dõi giáo trình
6. Nhận thông báo khi có cập nhật
7. Báo lỗi nếu phát hiện sai sót
```

## 📝 TODO - Backend Integration

- [ ] Kết nối API authentication
- [ ] Fetch real syllabus data from backend
- [ ] Implement AI Summary API
- [ ] Implement Subject Tree API
- [ ] Implement PLO Mapping API
- [ ] Subscription management API
- [ ] Profile update API
- [ ] Error reporting API
- [ ] Real-time notifications (WebSocket)

## 🎨 Customization

Để tùy chỉnh theme:
- Màu sắc: Sửa trong `css/ruang-admin.min.css`
- Logo: Thay thế `img/logo/logo.png`
- Sidebar: Cập nhật trong mỗi file HTML (phần `<ul class="navbar-nav sidebar">`)

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng liên hệ:
- Email: support@smd.edu.vn
- Báo lỗi: Sử dụng chức năng "Báo lỗi" trong trang chi tiết giáo trình

---

**Developed with ❤️ for HCMUTE Students**
