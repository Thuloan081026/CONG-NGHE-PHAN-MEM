# 🎓 Lecturer Web - SMD System

## Hệ Thống Quản lý & Số hóa Giáo trình (SMD) - Giao diện Giảng viên

Giao diện web chuyên biệt cho giảng viên quản lý, tạo, và xuất bản giáo trình môn học.

---

## ✨ Tính Năng Chính

### 📊 Dashboard
- **Thống kê giáo trình**: Total, Published, In Review, Draft
- **Giáo trình gần đây**: Hiển thị 5 giáo trình cập nhật gần nhất
- **Quick Actions**: Nút tạo mới, xem tất cả, reviews & feedback
- **Chào mừng cá nhân hóa**: Hiển thị tên giảng viên

### 📚 Syllabus Management
- **Tạo giáo trình mới**: Form chi tiết với tất cả thông tin
- **Danh sách giáo trình**: Hiển thị tất cả với filter
- **Chỉnh sửa giáo trình**: Cập nhật nội dung
- **Quản lý phiên bản**: Lịch sử thay đổi
- **Xem chi tiết**: Toàn bộ thông tin giáo trình

### 👤 Hồ Sơ Giảng Viên
- **Thông tin cá nhân**: Tên, Email, Khoa, Chức danh
- **Thông tin học vấn**: Bằng cấp, Chuyên ngành, Kinh nghiệm
- **Liên hệ**: Điện thoại, Địa chỉ phòng làm việc
- **Lĩnh vực nghiên cứu**: Các chủ đề quan tâm
- **Chỉnh sửa**: Cập nhật hồ sơ trực tiếp

### 🔔 Thông Báo
- **Danh sách thông báo**: Tất cả cập nhật từ hệ thống
- **Filter**: All, Unread, Approved, Rejected
- **Đánh dấu đã đọc**: Một hoặc tất cả
- **Thống kê**: Chưa đọc, đã đọc, tổng số
- **Chi tiết**: Thời gian, loại, nội dung

### 💬 Reviews & Feedback
- **Phản hồi**: Nhận và trả lời bình luận
- **Đánh giá**: Rating từ các reviewer
- **Lịch sử**: Theo dõi tất cả phản hồi

### 🔍 Tìm Kiếm
- **Tìm giáo trình**: Theo mã, tên, từ khóa
- **Xem tài liệu tham khảo**: Danh sách học phần liên quan
- **Lọc nâng cao**: Theo trạng thái, kỳ, bộ môn

---

## 🚀 Bắt Đầu Nhanh

### 1. Chạy Script Tạo Dữ Liệu Demo
```bash
cd backend
python create_lecturer_web_data.py
```

### 2. Khởi động Backend
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Mở Frontend
```
http://localhost:3000/lecturer-web/dashboard.html
```

### 4. Đăng nhập
```
Email: lecturer1@hcmute.edu.vn
Password: lecturer123
```

---

## 👥 Tài Khoản Demo

| Email | Tên | Chuyên Môn | Giáo Trình |
|-------|-----|-----------|-----------|
| `lecturer1@hcmute.edu.vn` | Ts. Trần Thị Bích | AI/ML | 4 (3 pub, 1 review) |
| `lecturer2@hcmute.edu.vn` | ThS. Lê Văn Chính | Database | 4 (2 pub, 1 sub, 1 draft) |
| `lecturer3@hcmute.edu.vn` | Ks. Phạm Thị Linh | Web Dev | 4 (3 pub, 1 review) |

**Mật khẩu mặc định**: `lecturer123`

---

## 📁 Cấu Trúc Thư Mục

```
lecturer-web/
├── assets/
│   ├── css/
│   │   ├── lecturer-dashboard.css    ← Main stylesheet (cải thiện)
│   │   ├── main.css
│   │   ├── menu.css
│   │   └── responsive.css
│   ├── js/
│   ├── images/
│   └── plugins/
├── dashboard.html                    ← Dashboard chính
├── profile.html                      ← Hồ sơ giảng viên
├── notifications.html                ← Thông báo
├── syllabus-list.html               ← Danh sách giáo trình
├── syllabus-view.html               ← Xem giáo trình
├── syllabus-edit.html               ← Chỉnh sửa giáo trình
├── syllabus-create.html             ← Tạo giáo trình mới
├── syllabus-versions.html           ← Quản lý phiên bản
├── comments-feedback.html            ← Reviews & Feedback
├── search-reference.html             ← Tìm kiếm
├── home.html                         ← Trang chủ
├── index.html                        ← Index
└── README.md                         ← File này
```

---

## 🎨 Giao Diện Được Cải Thiện

### Màu Sắc Xanh Dương Hài Hòa
- **Primary Card**: Gradient xanh dương (`#2563eb → #60a5fa`)
- **Success Card**: Gradient xanh lá (`#059669 → #34d399`)
- **Warning Card**: Gradient đỏ (`#dc2626 → #f87171`)
- **Info Card**: Gradient xanh lam (`#0891b2 → #22d3ee`)

### Bóng (Shadow) Nâng Cao
- **Drop Shadow**: `0 8px 25px` - Đổ bóng xuống
- **Glow Effect**: `0 0 20px` - Hiệu ứng sáng
- **Hover Effect**: Shadow tăng cường khi hover

### Navigation Đậm Hơn
- **Nav Labels**: Font-weight 900 (rất đậm)
- **Menu Items**: Font-weight 600 (đậm)
- **Active State**: Highlight + scale effect

---

## 🔌 API Integration

### Endpoints Sử Dụng

#### Authentication
```
POST /auth/login
POST /auth/logout
GET /auth/me
```

#### Users
```
GET /users/me                    ← Lấy thông tin giảng viên
PUT /users/me                    ← Cập nhật hồ sơ
GET /users/{id}
```

#### Syllabuses
```
GET /syllabus/                   ← Danh sách giáo trình
GET /syllabus/{id}               ← Chi tiết giáo trình
POST /syllabus/                  ← Tạo giáo trình
PUT /syllabus/{id}               ← Cập nhật giáo trình
DELETE /syllabus/{id}            ← Xóa giáo trình
```

#### Notifications
```
GET /notifications               ← Danh sách thông báo
PUT /notifications/{id}/read     ← Đánh dấu đã đọc
```

#### Reviews
```
GET /reviews/                    ← Danh sách review
POST /review/                    ← Tạo review mới
GET /review/{id}                 ← Chi tiết review
```

---

## 💻 Công Nghệ Sử Dụng

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Gradients, animations, flexbox
- **Bootstrap 5**: Grid system, components
- **Vanilla JavaScript**: Minimal, API calls only

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **MySQL**: Database
- **Python**: Language

### Tools
- **Font Awesome 6**: Icons
- **Themify Icons**: Additional icons
- **jQuery**: DOM manipulation (optional)

---

## 📊 Demo Data Statistics

### Giảng Viên: 3
- Profile chi tiết (degree, title, department, phone, office)
- Research interests & teaching subjects
- Qualifications & publications

### Giáo Trình: 12
- **Published**: 6
- **In Review**: 2
- **Submitted**: 1
- **Draft**: 3

### CLO: 36
- 3 CLOs per syllabus
- Cognitive levels: K2, K3, K4, K5

### Reviews: 5
- Rating: 4-5 stars
- Types: content, structure, learning outcomes

### Notifications: 7
- Types: approve, reject, update, follow
- Status: read/unread

---

## 🔄 Workflow Giáo Trình

```
Draft
  ↓
Submit for Review
  ↓
HoD Review
  ├─→ Approved → Published
  └─→ Rejected → Needs Revision
```

---

## 🛠️ Troubleshooting

### Không thấy dữ liệu
1. ✅ Kiểm tra backend chạy: `http://localhost:8000/docs`
2. ✅ Chạy script demo: `python create_lecturer_web_data.py`
3. ✅ Kiểm tra token trong localStorage
4. ✅ Mở DevTools (F12) xem error

### Không đăng nhập được
1. ✅ Kiểm tra email chính xác (ví dụ: `lecturer1@hcmute.edu.vn`)
2. ✅ Mật khẩu: `lecturer123`
3. ✅ Backend phải chạy trên port 8000
4. ✅ Kiểm tra CORS configuration

### Lỗi API
1. ✅ Kiểm tra backend log
2. ✅ Mở Network tab trong DevTools
3. ✅ Kiểm tra request/response headers
4. ✅ Xác nhận token valid

---

## 📚 Tài Liệu Thêm

- [LECTURER_WEB_UPDATE.md](./LECTURER_WEB_UPDATE.md) - Hướng dẫn chi tiết
- [CSS_CHANGES_REFERENCE.md](./CSS_CHANGES_REFERENCE.md) - Tham chiếu CSS
- [API_REFERENCE.md](../API_REFERENCE.md) - Tài liệu API

---

## 🔐 Bảo Mật

- ✅ Mật khẩu mã hóa (hashed)
- ✅ Token-based authentication (JWT)
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection

---

## 📱 Responsive Design

- ✅ Desktop (1920px+)
- ✅ Laptop (1366px - 1920px)
- ✅ Tablet (768px - 1365px)
- ✅ Mobile (320px - 767px)

---

## 🎯 Tính Năng Sắp Tới

- [ ] Export syllabus to PDF
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Collaboration tools
- [ ] AI-powered content suggestions
- [ ] Analytics & reports
- [ ] Mobile app

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra documentation
2. Mở DevTools (F12) xem error
3. Kiểm tra backend logs
4. Liên hệ team support

---

## 📄 Giấy Phép

© 2025 SMD System - Hệ Thống Quản lý & Số hóa Giáo trình  
Tất cả quyền được bảo lưu.

---

## 🎉 Công Nhân

**Hoàn thành**: 23/01/2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

**Happy Teaching! 🚀**
