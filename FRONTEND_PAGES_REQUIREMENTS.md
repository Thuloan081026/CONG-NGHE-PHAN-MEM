# 📊 SMD Frontend Pages Requirements

## Tổng Quan Hệ Thống
**Hệ thống quản lý và số hóa Giáo trình (SMD)** - SP26SE001

---

## 1️⃣ SYSTEM ADMIN - Web App (12 trang)

### Authentication & Dashboard
1. **Login Page** - Đăng nhập admin
2. **Dashboard** - Tổng quan hệ thống (statistics, KPIs, recent activities)

### User Management (3 trang)
3. **User List Page** - Danh sách tất cả users
4. **Create/Edit User Page** - Form tạo/sửa user (single/bulk import)
5. **User Roles & Permissions** - Phân quyền chi tiết theo role

### System Configuration (4 trang)
6. **General Settings** - Cấu hình chung (semester, academic year)
7. **CLO/PLO Templates** - Quản lý mẫu chuẩn đầu ra
8. **Grading Scale Config** - Cấu hình thang điểm
9. **Workflow Rules** - Cấu hình quy trình duyệt

### Publishing Management (2 trang)
10. **Publishing Queue** - Danh sách syllabus chờ publish
11. **Published Syllabus Management** - Quản lý syllabus đã xuất bản

### System Monitoring
12. **Audit Log & Reports** - Lịch sử hoạt động, báo cáo hệ thống

---

## 2️⃣ LECTURER - Web App (10 trang)

### Authentication & Dashboard
1. **Login Page** - Đăng nhập giảng viên
2. **Dashboard** - Tổng quan syllabus của giảng viên (drafts, pending, approved)

### Syllabus Creation & Management (5 trang)
3. **Create Syllabus** - Form tạo syllabus mới (multi-step wizard)
   - Step 1: Basic Info (subject code, name, credits, semester)
   - Step 2: Learning Outcomes (CLO definition)
   - Step 3: Course Content (detailed curriculum)
   - Step 4: Assessment & Materials
   - Step 5: Review & Submit
4. **Edit Syllabus** - Chỉnh sửa syllabus draft
5. **My Syllabus List** - Danh sách syllabus của giảng viên
6. **Syllabus Version History** - Lịch sử version và changes
7. **Syllabus Preview/Detail** - Xem chi tiết syllabus

### Collaboration & Review (2 trang)
8. **Collaborative Review** - Trang review nội dung từ đồng nghiệp
9. **Comments & Feedback** - Quản lý comments/feedback nhận được

### Resources & Search
10. **Search & Reference** - Tìm kiếm syllabus tham khảo

---

## 3️⃣ HEAD OF DEPARTMENT (HoD) - Web App (9 trang)

### Authentication & Dashboard
1. **Login Page** - Đăng nhập trưởng khoa
2. **Dashboard** - Tổng quan công việc (pending approvals, statistics)

### Review & Approval (4 trang)
3. **Review Queue** - Danh sách syllabus chờ duyệt level 1
4. **Syllabus Review Detail** - Trang review chi tiết với AI tools
   - AI Change Detection
   - CLO-PLO validation
   - Side-by-side comparison
5. **Approval Decision** - Form approve/reject với lý do
6. **Approved History** - Lịch sử syllabus đã duyệt

### Collaborative Review Management (2 trang)
7. **Collaborative Review Dashboard** - Quản lý collaborative review
8. **Feedback Compilation** - Tổng hợp feedback từ giảng viên

### Lookup & Analysis
9. **Department Syllabus Search** - Tìm kiếm và so sánh syllabus khoa

---

## 4️⃣ ACADEMIC AFFAIRS (AA) - Web App (11 trang)

### Authentication & Dashboard
1. **Login Page** - Đăng nhập phòng đào tạo
2. **Dashboard** - Tổng quan toàn trường

### Academic Approval (3 trang)
3. **Level 2 Review Queue** - Syllabus chờ duyệt level 2
4. **PLO Mapping Review** - Kiểm tra mapping CLO-PLO với Program standards
5. **Approval Decision** - Approve/reject level 2

### Course/Program Management (4 trang)
6. **Program Management** - Quản lý chương trình đào tạo
7. **PLO Standards Library** - Thư viện chuẩn đầu ra chương trình
8. **Module Relationships** - Quản lý môn tiên quyết/song hành
9. **Credit & Rubrics Config** - Cấu hình tín chỉ và rubrics

### Lookup & Analysis (2 trang)
10. **University-wide Search** - Tìm kiếm syllabus toàn trường
11. **Analytics & Reports** - Báo cáo phân tích (CLO coverage, version trends)

---

## 5️⃣ PRINCIPAL (Rector) - Web App (6 trang)

### Authentication & Dashboard
1. **Login Page** - Đăng nhập hiệu trưởng
2. **Executive Dashboard** - Dashboard chiến lược (KPIs, high-level metrics)

### Strategic Approval (2 trang)
3. **Strategic Review Queue** - Các quyết định quan trọng cần phê duyệt
4. **Final Approval** - Phê duyệt cuối cùng

### System Oversight (2 trang)
5. **Impact Analysis** - Phân tích tác động của thay đổi
6. **System Reports & Audit** - Báo cáo toàn hệ thống

---

## 6️⃣ STUDENT / PUBLIC USER - Web App (8 trang) + Mobile App (6 screens)

### Web App (8 trang)
1. **Landing Page** - Trang chủ public (introduce system)
2. **Search Page** - Tìm kiếm syllabus
   - Filter: Subject Name, Code, Major, Semester
3. **Syllabus Detail View** - Xem chi tiết syllabus
   - Full content display
   - AI Summary section
   - Download PDF option
4. **Subject Relationship Tree** - Roadmap môn học (visual tree/graph)
5. **CLO-PLO Mapping View** - Xem ma trận CLO-PLO
6. **Compare Syllabus** - So sánh 2 syllabus versions
7. **My Subscriptions** - Quản lý theo dõi môn học
8. **Feedback/Report Error** - Form báo lỗi/góp ý

### Mobile App (6 screens)
1. **Splash Screen** - Màn hình khởi động
2. **Home/Search Screen** - Tìm kiếm nhanh
3. **Syllabus List Screen** - Danh sách kết quả
4. **Syllabus Detail Screen** - Chi tiết syllabus (optimized for mobile)
5. **Subject Roadmap Screen** - Roadmap visual
6. **Notifications Screen** - Thông báo cập nhật

---

## 7️⃣ COMMON PAGES (Shared Components) - 5 trang

1. **Profile Settings** - Cài đặt tài khoản cá nhân (all roles)
2. **Notifications Center** - Trung tâm thông báo
3. **Help & Documentation** - Hướng dẫn sử dụng
4. **Change Password** - Đổi mật khẩu
5. **Error Pages** - 404, 500, 403, etc.

---

## 📊 TỔNG KẾT SỐ LƯỢNG TRANG

| Module | Số trang/screens | Độ ưu tiên |
|--------|------------------|------------|
| **System Admin** | 12 trang | Cao |
| **Lecturer** | 10 trang | Cao |
| **Head of Department** | 9 trang | Cao |
| **Academic Affairs** | 11 trang | Trung bình |
| **Principal** | 6 trang | Thấp |
| **Student Web** | 8 trang | Cao |
| **Student Mobile** | 6 screens | Trung bình |
| **Common Pages** | 5 trang | Cao |
| **TỔNG WEB** | **61 trang** | |
| **TỔNG MOBILE** | **6 screens** | |

---

## 🎯 PHÂN BỔ CÔNG VIỆC THEO TASK PACKAGE

### Task Package 1: System Admin (12 trang)
- User Management: 3 trang
- System Config: 4 trang
- Publishing: 2 trang
- Monitoring: 1 trang
- Dashboard: 2 trang

### Task Package 2: Lecturer (10 trang)
- Syllabus CRUD: 5 trang
- Collaboration: 2 trang
- Dashboard: 2 trang
- Search: 1 trang

### Task Package 3: Reviewers & Approvers (26 trang)
- HoD: 9 trang
- Academic Affairs: 11 trang
- Principal: 6 trang

### Task Package 4: Internal Tools (Integrated vào các module trên)
- Version Comparison
- CLO-PLO Analysis
- Reports

### Task Package 5: Student (14 trang/screens)
- Web: 8 trang
- Mobile: 6 screens

---

## 🔧 CÔNG NGHỆ FRONTEND

### Web App
- **Framework**: ReactJS/NextJS
- **UI Library**: Material-UI / Ant Design
- **State Management**: Redux / Zustand
- **Form Handling**: React Hook Form
- **Charts**: Recharts / Chart.js
- **Rich Text Editor**: TipTap / Quill

### Mobile App
- **Framework**: React Native
- **Navigation**: React Navigation
- **UI Kit**: React Native Paper / NativeBase
- **State**: Redux Toolkit

---

## 📱 RESPONSIVE REQUIREMENTS

### Desktop (Primary)
- Resolution: 1366x768 trở lên
- All features available

### Tablet
- Resolution: 768x1024
- Optimized layout cho HoD/AA review

### Mobile (Student focused)
- Resolution: 360x640 trở lên
- Priority: Search, View, Subscribe

---

## 🎨 UI/UX CONSIDERATIONS

### Design System
- **Color Palette**: University branding colors
- **Typography**: Clear hierarchy (Roboto/Inter)
- **Icons**: Material Icons / Feather Icons
- **Spacing**: 8px grid system

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode

### Performance
- Initial load < 3s
- Lazy loading for heavy components
- Image optimization
- Code splitting by route

---

## 🚀 DEVELOPMENT ROADMAP

### Phase 1 (3 months) - Core Modules
- ✅ System Admin basic
- ✅ Lecturer CRUD
- ✅ Student search & view

### Phase 2 (2 months) - Review Workflow
- HoD review interface
- Academic Affairs approval
- Notification system

### Phase 3 (2 months) - Advanced Features
- AI integration UI
- Analytics dashboards
- Mobile app

### Phase 4 (1 month) - Polish & Testing
- UI/UX refinement
- Performance optimization
- Security testing

---

## 📝 NOTES

1. **Reusable Components**: Nhiều trang share components (form inputs, tables, modals)
2. **Progressive Enhancement**: Phát triển từ core features → advanced features
3. **API Integration**: Tất cả trang đều cần integrate với Web API (Task Package 7)
4. **Real-time Updates**: WebSocket cho notifications và collaborative features
5. **Offline Support**: Mobile app cần cache data cho offline viewing

---

**Prepared by:** Development Team  
**Last Updated:** December 19, 2025  
**Status:** Planning Phase
