# Cập Nhật Lecturer Web - SMD System v2.0

## 🎯 Tóm Tắt Thay Đổi

Đã cập nhật toàn bộ giao diện và chức năng của **lecturer-web** theo yêu cầu, với 6 chức năng chính cho giảng viên.

---

## ✨ Các Chức Năng Chính

### ✅ 01. Đăng nhập / Đăng xuất
- Giao diện hiện đại với gradient background
- Xác thực qua API backend
- Quản lý session với JWT token
- Đăng xuất an toàn

### ✅ 02. Tạo Mới Syllabus
- Form toàn diện với các tab:
  - **Basic Info**: Mã môn, tên, tín chỉ, mô tả
  - **CLO & PLO**: Định nghĩa và ánh xạ CLO-PLO
  - **Content**: Nội dung chương trình (chương, chủ đề, giờ)
  - **Assessment**: Trọng số đánh giá (tự động kiểm tra tổng = 100%)
  - **Prerequisites**: Môn tiên quyết, song hành, tương đương
  - **Resources**: Giáo trình, tài liệu tham khảo, tài liệu hỗ trợ
- **Auto-save Draft**: Tự động lưu mỗi 2 phút
- **Validation**: Kiểm tra dữ liệu nhập vào

### ✅ 03. Chỉnh Sửa & Cập Nhật Phiên Bản Syllabus
- **Trang mới**: `syllabus-versions.html`
- **Version History**: Hiển thị tất cả phiên bản (v1, v2, v3...)
- **AI Semantic Diff**: So sánh sự khác biệt giữa 2 phiên bản:
  - Hiển thị **Green** (thêm mới)
  - Hiển thị **Red** (xóa)
  - Phát hiện thay đổi từng trường: CLO, PLO, Content, Assessment Methods, Textbooks
- **Submit to HoD**: Gửi phiên bản mới lên HoD để phê duyệt
- **Restore Version**: Khôi phục phiên bản cũ (tạo bản copy mới)

### ✅ 04. Tham Gia Collaborative Review
- **Trang nâng cấp**: `collaborative-review.html`
- **2 Tab chính**:
  1. **"Yêu cầu xem xét cho tôi"**: Các đề cương từ đồng nghiệp chờ feedback
  2. **"Đề cương của tôi đang review"**: Đề cương của bạn đang được xem xét
  
- **Chức năng**:
  - Xem chi tiết đề cương
  - Đưa ra nhận xét (Góp ý / Vấn đề / Phê duyệt)
  - Xem feedback từ HoD
  - Trả lời bình luận
  - Filters: Ưu tiên, Trạng thái
  
- **Stats Cards**: Hiển thị số thống kê
  - Chờ xem xét
  - Đã xem xét
  - Bình luận
  - Đang review

### ✅ 05. Quản Lý Syllabus Cá Nhân
- **Trang**: `syllabus-list.html`
- **Danh sách bảng**: Tất cả đề cương của giảng viên
- **Cột hiển thị**: Code, Name, Credits, Semester, Status, Updated, Actions
- **Filters nâng cao**:
  - Search: Tìm kiếm theo mã hoặc tên
  - Status: Draft, Submitted, Under Review, Approved, Published
  - Semester: Học kỳ 1, 2, 3...
  
- **So sánh phiên bản qua AI**:
  - Vào Version History
  - Chọn 2 phiên bản để so sánh
  - Xem tất cả thay đổi

- **Actions per Syllabus**:
  - 👁 View (Xem chi tiết)
  - ✏️ Edit (Chỉnh sửa)
  - 🔄 History (Lịch sử phiên bản)
  - 📊 Compare (So sánh)
  - 🗑 Delete (Xóa - chỉ Draft)

### ✅ 06. Nhận Thông Báo
- **Trang mới**: `notifications.html`
- **Stats Cards**: 
  - Chưa đọc
  - Đã đọc
  - Cần hành động
  - Tổng cộng
  
- **Loại thông báo**:
  - 📤 **Submission** (Đơn gửi)
  - ✏️ **Review** (Xem xét)
  - ✅ **Approval** (Phê duyệt)
  - ℹ️ **System** (Hệ thống)
  
- **Filters**: Tất cả, Chưa đọc, Đơn gửi, Review, Phê duyệt
- **Actions**:
  - Đánh dấu đã đọc
  - Đánh dấu tất cả đã đọc
  - Click vào thông báo để xem chi tiết
  - Link đến tài nguyên liên quan

---

## 📊 Dashboard - Giao Diện Mới

### 5 Stats Card (Giống ảnh):
1. **Đề tài đề xuất** (5) - Đang chờ duyệt
2. **Lịch Review sắp tới** (2) - Trong tuần này
3. **Tin nhắn mới** (12) - Từ nhóm G3-SEP
4. **Đề tài hoàn thành** (18) - Đã phê duyệt
5. **Bản nháp** (3) - Chưa hoàn thành

### Quick Actions (5 nút):
- ➕ Create New Syllabus
- 📄 View All Syllabuses
- 🔄 Version History
- 💬 Collaborative Review
- 🔔 View Notifications

### Recent Syllabuses:
- Danh sách 5 đề cương mới nhất
- Hiển thị: Code, Name, Credits, Status, Updated date
- Nút: View, Edit

---

## 🗂️ Danh Sách File Được Cập Nhật/Tạo

### Cập Nhật:
1. **dashboard.html** - Dashboard mới với 5 cards stats
2. **collaborative-review.html** - Nâng cấp với 2 tabs, review workflow
3. **assets/css/lecturer-dashboard.css** - Thêm styles cho 5-column layout, responsive

### Tạo Mới:
1. **syllabus-versions.html** - Quản lý phiên bản & compare
2. **notifications.html** - Hệ thống thông báo toàn diện
3. **FEATURES_GUIDE_VI.md** - Hướng dẫn sử dụng chi tiết (tiếng Việt)

### Giữ Nguyên (Có sẵn):
- **index.html** - Login page
- **syllabus-list.html** - Danh sách (có filters sẵn)
- **syllabus-create.html** - Tạo đề cương (đầy đủ fields)
- **syllabus-edit.html** - Redirect đến create với ?id=
- **comments-feedback.html** - Phản hồi & bình luận
- **search-reference.html** - Tìm kiếm tài liệu
- **profile.html** - Hồ sơ giảng viên

---

## 🎨 Giao Diện Cải Tiến

### Sidebar Menu:
```
📊 Dashboard
📚 Syllabus Management
   └─ View All
   └─ Create New
   └─ Version History
💬 Collaboration
   └─ Collaborative Review
   └─ Comments & Feedback
⚙️ Settings
   └─ My Profile
   └─ Notifications
🔐 Account
   └─ Logout
```

### Color Scheme:
- **Primary**: #667eea (Xanh tím)
- **Success**: #11998e → #38ef7d (Xanh lá)
- **Warning**: #f093fb → #f5576c (Hồng)
- **Info**: #4facfe → #00f2fe (Xanh dương)
- **Neutral**: #f5f7fa (Xám nhạt)

### Responsive:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

---

## 🚀 Cách Sử Dụng

### Đăng Nhập:
```
URL: http://localhost:3000
Email: lecturer@email.com
Password: your_password
```

### Truy Cập Các Trang:
- Dashboard: `/`
- Create Syllabus: `/syllabus-create.html`
- My Syllabuses: `/syllabus-list.html`
- Version History: `/syllabus-versions.html`
- Collaborative Review: `/collaborative-review.html`
- Notifications: `/notifications.html`
- Profile: `/profile.html`

---

## 🔧 API Endpoints Được Sử Dụng

```
POST /auth/login                    - Đăng nhập
GET  /users/me                      - Lấy thông tin người dùng
GET  /syllabus/                     - Danh sách đề cương
POST /syllabus/                     - Tạo đề cương
GET  /syllabus/{id}                 - Chi tiết đề cương
PUT  /syllabus/{id}                 - Cập nhật đề cương
GET  /syllabus/{id}/versions        - Lịch sử phiên bản
POST /syllabus/{id}/submit          - Gửi cho HoD
GET  /syllabus/review-requests      - Yêu cầu review
GET  /notifications                 - Danh sách thông báo
PUT  /notifications/{id}/read       - Đánh dấu đã đọc
PUT  /notifications/mark-all-read   - Đánh dấu tất cả đã đọc
```

---

## ✅ Kiểm Tra Login

### Đảm bảo:
- ✅ Login không bị ảnh hưởng (sử dụng localStorage token)
- ✅ Authentication check trên mỗi trang
- ✅ Tự động redirect nếu token hết hạn
- ✅ Logout xóa toàn bộ localStorage

### Cách Test:
1. Đăng nhập thành công
2. Kiểm tra **Developer Tools** → Storage → localStorage
   - `access_token` phải tồn tại
   - `user_data` phải có thông tin
3. Refresh page → vẫn giữ login
4. Logout → xóa token, redirect về login

---

## 📝 Thay Đổi Chi Tiết

### Dashboard.html
- **Thay**: 4 stats cards → **5 stats cards**
- **Thêm**: Links đến Version History, Notifications
- **Cập nhật**: Menu sidebar có "Version History"

### Collaborative-review.html
- **Thay**: Bố cục cũ → **2 tabs structure**
- **Thêm**: Filter, comment threads, reply functionality
- **Thêm**: Stats cards (chờ xem, đã xem, bình luận)

### lecturer-dashboard.css
- **Thêm**: Styles cho `.dashboard-header` (flex, gap)
- **Cập nhật**: `.stat-card` sizes cho responsive 5-column
- **Thêm**: `.filter-btn.active` styling
- **Thêm**: Media queries cho mobile

### Notifications.html (NEW)
- Trang hoàn chỉnh quản lý thông báo
- Real-time notification loading
- Filter by type
- Mark as read functionality

### Syllabus-versions.html (NEW)
- Version history list
- Semantic diff comparison
- Submit to HoD button
- Restore version functionality

---

## 🐛 Known Issues & Workarounds

### Nếu gặp vấn đề:

1. **API không kết nối được?**
   - Kiểm tra backend có running: `http://localhost:8000`
   - Kiểm tra CORS headers

2. **Login không hoạt động?**
   - Xóa localStorage: `localStorage.clear()`
   - Refresh page: `F5`

3. **Trang trắng sau login?**
   - Kiểm tra Network tab (F12) có lỗi gì không
   - Kiểm tra console (F12) có error không

4. **Phiên bản không hiển thị?**
   - Kiểm tra API endpoint: `/syllabus/{id}/versions`
   - Kiểm tra status code từ API

---

## 📚 Tài Liệu Hỗ Trợ

1. **FEATURES_GUIDE_VI.md** - Hướng dẫn sử dụng chi tiết cho người dùng cuối
2. **README.md** (file này) - Tổng quan cho developers
3. **API_REFERENCE.md** - Tham khảo API endpoints (nếu có)

---

## 🔐 Security Notes

- ✅ Token được lưu trong **localStorage** (cần HTTPS trong production)
- ✅ API calls có **Authorization header**
- ✅ Role check: `lecturer` role required
- ✅ Auto-redirect nếu không authenticated

**Recommendation**: Sử dụng **sessionStorage** thay **localStorage** cho bảo mật cao hơn.

---

## 📞 Support

Nếu gặp bất kỳ vấn đề nào:
1. Kiểm tra **Browser Console** (F12) xem error
2. Kiểm tra **Network tab** xem API response
3. Kiểm tra **localStorage** có token không
4. Liên hệ Admin / IT Support

---

**Cập nhật**: 06/01/2026
**Phiên bản**: 2.0.0
**Status**: ✅ Ready for Testing
