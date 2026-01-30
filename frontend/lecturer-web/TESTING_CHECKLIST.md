# ✅ Testing Checklist - Lecturer Web v2.0

## 🔐 01. AUTHENTICATION (Đăng nhập/Đăng xuất)

### Login Tests:
- [ ] Trang login hiển thị đúng (`http://localhost:3000`)
- [ ] Nhập email/password đúng → login thành công → redirect dashboard
- [ ] Nhập password sai → hiển thị error message
- [ ] Nhập email không tồn tại → hiển thị error message
- [ ] Token được lưu trong localStorage
- [ ] User data được lưu trong localStorage

### Logout Tests:
- [ ] Click dropdown user → Logout option hiển thị
- [ ] Click Logout → confirm dialog xuất hiện
- [ ] Click Yes → logout thành công, redirect login page
- [ ] localStorage được xóa (token, user_data)
- [ ] Truy cập protected page → redirect login

### Session Tests:
- [ ] Refresh page sau login → vẫn giữ logged in
- [ ] Đóng tab → Mở lại → vẫn logged in (nếu token còn hạn)
- [ ] Token hết hạn → auto redirect login
- [ ] Multiple tabs → logout 1 tab → các tab khác cập nhật

---

## 📚 02. CREATE SYLLABUS (Tạo Đề Cương)

### Basic Info Tab:
- [ ] Subject Code input → Nhập được dữ liệu
- [ ] Subject Name input → Nhập được dữ liệu
- [ ] Credits input → Nhập số → hiển thị đúng
- [ ] Semester dropdown → Có tất cả các option
- [ ] Description textarea → Nhập được text dài

### CLO Tab:
- [ ] Nhấn "+ Add CLO" → Form xuất hiện
- [ ] Nhập CLO text → Lưu được
- [ ] Xóa CLO → Bị xóa khỏi list
- [ ] Có ít nhất 1 CLO mới cho phép submit

### PLO Tab:
- [ ] Nhấn "+ Add PLO" → Form xuất hiện
- [ ] Nhập PLO text → Lưu được
- [ ] Xóa PLO → Bị xóa khỏi list

### CLO-PLO Mapping:
- [ ] Checkbox mapping → Click để chọn/bỏ chọn
- [ ] Hiển thị matrix đúng
- [ ] Lưu được mapping

### Content Tab:
- [ ] Nhấn "+ Add Chapter" → Form xuất hiện
- [ ] Nhập Chapter Name → Lưu được
- [ ] Nhập Topics → Lưu được
- [ ] Nhập Hours → Lưu được
- [ ] Chọn CLOs covered → Lưu được

### Assessment Tab:
- [ ] Nhập weights cho từng category
- [ ] Total weight = 100% → alert/success
- [ ] Total weight ≠ 100% → alert/warning
- [ ] Weights từ 0-100 → Valid

### Prerequisites Tab:
- [ ] Nhấn "+ Add Prerequisite" → Form xuất hiện
- [ ] Chọn môn học từ dropdown → Lưu được
- [ ] Xóa prerequisite → Bị xóa
- [ ] Tương tự cho Corequisites, Related Subjects

### Resources Tab:
- [ ] Nhấn "+ Add Textbook" → Form xuất hiện
- [ ] Nhập textbook info → Lưu được
- [ ] Nhấn "+ Add Reference" → Form xuất hiện
- [ ] Nhập reference info → Lưu được
- [ ] Nhấn "+ Add Learning Material" → Form xuất hiện

### Auto-save & Submit:
- [ ] Draft auto-saves mỗi 2 phút (check console)
- [ ] Reload page → dữ liệu vẫn có (không mất)
- [ ] Nhấn "Submit for Review" → POST API call
- [ ] Success → Status chuyển "Submitted"
- [ ] Fail → Error message hiển thị

---

## ✏️ 03. EDIT & VERSION CONTROL (Quản lý Phiên bản)

### Version List:
- [ ] Trang `/syllabus-versions.html` load đúng
- [ ] Dropdown "Chọn Đề cương" hiển thị tất cả
- [ ] Click một đề cương → Load versions
- [ ] Version list hiển thị đúng (v1, v2, v3...)
- [ ] Click version → highlight active

### Version Details:
- [ ] Hiển thị tên version đúng
- [ ] Hiển thị trạng thái (Draft, Submitted...)
- [ ] Hiển thị ngày tạo
- [ ] Hiển thị change summary

### Compare Versions (Semantic Diff):
- [ ] Dropdown "Phiên bản cũ" → Chọn được
- [ ] Dropdown "Phiên bản mới" → Chọn được
- [ ] Chọn 2 versions khác nhau → Auto compare
- [ ] Diff view hiển thị:
  - [ ] Removed (Red) - phần xóa
  - [ ] Added (Green) - phần thêm
  - [ ] Unchanged - phần giữ nguyên
- [ ] So sánh từng field: CLO, PLO, Content, Assessment, Textbooks

### Edit Version:
- [ ] Nhấn "Edit" trên version cũ → Load form
- [ ] Chỉnh sửa fields → Lưu được
- [ ] Save → Tạo version mới (v_new)
- [ ] Auto-save draft hoạt động

### Submit to HoD:
- [ ] Chọn version → Nhấn "Gửi lên HoD để phê duyệt"
- [ ] Confirm dialog xuất hiện
- [ ] Click Yes → POST API call
- [ ] Success → Status chuyển "Submitted"
- [ ] Notification gửi cho HoD

### Restore Version:
- [ ] Chọn version cũ → Nhấn "Khôi phục phiên bản"
- [ ] Confirm dialog xuất hiện
- [ ] Click Yes → Tạo version mới với dữ liệu cũ
- [ ] Version list update

---

## 💬 04. COLLABORATIVE REVIEW (Xem Xét Cộng Tác)

### Tab 1: Yêu cầu xem xét cho tôi

#### Review Requests Display:
- [ ] List của review requests hiển thị
- [ ] Mỗi card hiển thị:
  - [ ] Avatar reviewer (initials)
  - [ ] Subject code & name
  - [ ] Reviewer info
  - [ ] Request note
  - [ ] Request date
  - [ ] Status badge

#### Filters:
- [ ] Filter by search → Tìm kiếm đúng
- [ ] Filter by priority (High/Medium/Low) → Hiển thị đúng
- [ ] Filter by status (Pending/Reviewed) → Hiển thị đúng

#### Review Modal:
- [ ] Nhấn "Xem xét" → Modal pop up
- [ ] Modal hiển thị:
  - [ ] Subject info
  - [ ] CLOs
  - [ ] PLOs
  - [ ] Content
- [ ] Nhập comment → Text lưu được
- [ ] Chọn review type (Góp ý/Vấn đề/Phê duyệt) → Lưu được
- [ ] Nhấn "Gửi nhận xét" → POST API call
- [ ] Success → Modal close, list update

### Tab 2: Đề cương của tôi đang review

#### My Syllabuses Display:
- [ ] List hiển thị đúng
- [ ] Mỗi card hiển thị:
  - [ ] Subject code & name
  - [ ] Status badge
  - [ ] Reviewers list
  - [ ] Comments section

#### Comments & Feedback:
- [ ] Hiển thị các bình luận từ reviewers
- [ ] Mỗi comment có:
  - [ ] Tên reviewer
  - [ ] Nội dung bình luận
  - [ ] Timestamp
  - [ ] Comment type badge (Suggestion/Concern/Approved)

#### Reply to Comments:
- [ ] Textarea "Trả lời bình luận" có sẵn
- [ ] Nhập text → Text lưu được
- [ ] Nhấn "Trả lời" → POST API call
- [ ] Success → Comment thêm vào thread

#### Auto-notify:
- [ ] Khi có bình luận mới → Email notification (nếu config)
- [ ] Thông báo hiển thị trong dashboard

---

## 📖 05. MANAGE SYLLABUS (Quản lý Đề Cương)

### List View:
- [ ] Trang `/syllabus-list.html` load đúng
- [ ] Table hiển thị tất cả fields:
  - [ ] Subject Code
  - [ ] Subject Name
  - [ ] Credits
  - [ ] Semester
  - [ ] Status
  - [ ] Updated
  - [ ] Actions

### Search:
- [ ] Nhập mã môn → Filter đúng
- [ ] Nhập tên môn → Filter đúng
- [ ] Search realtime (khi stop typing)

### Filters:
- [ ] Status filter → All/Draft/Submitted/Under Review/Approved/Published
- [ ] Semester filter → Chọn semester
- [ ] Nhấn "Apply Filters" → Filter đúng

### Actions (Per Syllabus):
- [ ] "View" button → Mở chi tiết page
- [ ] "Edit" button → Chuyển đến edit/create form
- [ ] "Delete" button (Draft only) → Delete confirm → Xóa thành công

### Pagination:
- [ ] Page numbers hiển thị đúng
- [ ] Click page number → Load correct data
- [ ] Showing X of Y syllabuses → Display đúng

### Version Comparison:
- [ ] Click version history icon → Chuyển đến versions page
- [ ] Có thể compare 2 versions
- [ ] Xem diff đúng

---

## 🔔 06. NOTIFICATIONS (Nhận Thông Báo)

### Notifications Page:
- [ ] Trang `/notifications.html` load đúng
- [ ] Hiển thị danh sách thông báo

### Stats Cards:
- [ ] "Thông báo mới" → Show unread count
- [ ] "Đã xử lý" → Show read count
- [ ] "Cần hành động" → Show action-required count
- [ ] "Tổng cộng" → Show total count

### Notification List:
- [ ] Mỗi notification hiển thị:
  - [ ] Icon (theo type)
  - [ ] Title
  - [ ] Message
  - [ ] Time (giờ trước, ngày trước)
  - [ ] Type badge
  - [ ] Unread indicator (nếu chưa đọc)

### Filters:
- [ ] "Tất cả" → Show all
- [ ] "Chưa đọc" → Show only unread
- [ ] "Đơn gửi" (Submission) → Show submission notifications
- [ ] "Review" → Show review notifications
- [ ] "Phê duyệt" (Approval) → Show approval notifications

### Actions:
- [ ] Click notification → Mark as read + show details
- [ ] Unread indicator disappear
- [ ] "Đánh dấu tất cả đã đọc" → Mark all as read
- [ ] All notifications lose unread indicator

### Notification Types:
- [ ] 📤 Submission → Orange badge
- [ ] ✏️ Review → Yellow badge
- [ ] ✅ Approval → Green badge
- [ ] ℹ️ System → Gray badge

### Action Links:
- [ ] Some notifications have "Xem chi tiết" button
- [ ] Click → Navigate to relevant page

---

## 📊 DASHBOARD (Dashboard Chính)

### 5 Stats Cards:
- [ ] "Đề tài đề xuất" → Display correct number + icon
- [ ] "Lịch Review sắp tới" → Display correct number + icon
- [ ] "Tin nhắn mới" → Display correct number + icon
- [ ] "Đề tài hoàn thành" → Display correct number + icon
- [ ] "Bản nháp" → Display correct number + icon
- [ ] Cards responsive (5-column desktop, 2-column tablet, 1 mobile)
- [ ] Cards have hover effect

### Welcome Message:
- [ ] "Welcome back, [User Name]!" → Shows user name correctly
- [ ] Message updates when user changes

### Recent Syllabuses:
- [ ] List hiển thị 5 syllabuses mới nhất
- [ ] Mỗi item hiển thị:
  - [ ] Code & Name
  - [ ] Credits, Date
  - [ ] Status badge
  - [ ] View & Edit buttons

### Quick Actions (5 Buttons):
- [ ] "Create New Syllabus" → Navigate to create page
- [ ] "View All Syllabuses" → Navigate to list
- [ ] "Version History" → Navigate to versions page
- [ ] "Collaborative Review" → Navigate to review page
- [ ] "View Notifications" → Navigate to notifications

### Responsive Design:
- [ ] Desktop (1200px+) → 5-column stats cards
- [ ] Tablet (768px-1199px) → 2-3 columns
- [ ] Mobile (<768px) → 1 column

---

## 🎨 UI/UX CHECKS

### Colors:
- [ ] Primary color (Blue-Purple #667eea) used correctly
- [ ] Success color (Green #11998e) on approved items
- [ ] Warning color (Pink #f093fb) on pending items
- [ ] Info color (Cyan #4facfe) on info items

### Fonts:
- [ ] Headings (h1-h6) display correctly
- [ ] Body text readable (font-size ≥ 14px)
- [ ] Links underlined/styled correctly

### Icons:
- [ ] Themify icons load correctly
- [ ] Icons align properly
- [ ] Icons have appropriate colors

### Spacing:
- [ ] Padding/margins look good
- [ ] No overlapping elements
- [ ] Cards have breathing room

### Buttons:
- [ ] Primary buttons (Blue-purple) = main action
- [ ] Outline buttons = secondary action
- [ ] Buttons have hover/active states
- [ ] Button text clear & readable

---

## 🔒 SECURITY CHECKS

### Authentication:
- [ ] Routes require valid token
- [ ] Expired token → auto redirect login
- [ ] Role check: lecturer role required
- [ ] Unauthorized access → 401 error

### Data Protection:
- [ ] No sensitive data in localStorage (except token)
- [ ] API calls use HTTPS (production)
- [ ] CORS headers correct

### XSS Prevention:
- [ ] User input sanitized
- [ ] No eval() or innerHTML misuse
- [ ] Form validation on client & server

---

## ⚡ PERFORMANCE CHECKS

### Load Time:
- [ ] Dashboard loads in < 2 seconds
- [ ] List page loads in < 2 seconds
- [ ] API calls optimized (pagination, limits)

### Memory:
- [ ] No memory leaks (check DevTools)
- [ ] Proper event listener cleanup
- [ ] Modals close properly

### Network:
- [ ] API calls use correct HTTP methods
- [ ] No unnecessary requests
- [ ] Error handling for network failures

---

## 📱 RESPONSIVE DESIGN CHECKS

### Desktop (1200px+):
- [ ] 5-column layout for stats cards
- [ ] Sidebar visible (not collapsed)
- [ ] Full width content

### Tablet (768px-1199px):
- [ ] 2-3 column layout (flexible)
- [ ] Sidebar toggle works
- [ ] Content readable

### Mobile (<768px):
- [ ] 1 column layout
- [ ] Sidebar collapsed by default
- [ ] Hamburger menu works
- [ ] Buttons large enough to tap
- [ ] Forms don't have tiny inputs

---

## 🐛 BUG FIXES & EDGE CASES

### Edge Cases:
- [ ] Empty syllabus list → Show "No syllabuses" message
- [ ] No notifications → Show "No notifications" message
- [ ] API timeout → Show error message + retry button
- [ ] Network error → Graceful error handling
- [ ] Invalid data from API → Proper fallback

### Input Validation:
- [ ] Required fields cannot be empty
- [ ] Email format validated
- [ ] Numbers only in numeric fields
- [ ] Max length enforced

---

## 📋 FINAL SIGN-OFF

### Before Going Live:
- [ ] All tests above passed
- [ ] No console errors (F12)
- [ ] No network errors
- [ ] All features working
- [ ] UI looks good on all devices
- [ ] Security checks passed
- [ ] Performance acceptable

### Documentation:
- [ ] README.md complete
- [ ] FEATURES_GUIDE_VI.md complete
- [ ] UPDATES_README.md complete
- [ ] API endpoints documented
- [ ] Setup instructions clear

### Deployment:
- [ ] Built minified CSS/JS
- [ ] Environment variables set
- [ ] Database migrations run
- [ ] Backend API running
- [ ] CORS configured
- [ ] SSL/HTTPS enabled (production)

---

## 🎉 Sign-Off

- **Tester**: ___________________
- **Date**: ___________________
- **Status**: ☐ PASS ☐ FAIL

**Notes**: _________________________________________________________________

---

**Test Date**: 06/01/2026
**Version**: 2.0.0
**Environment**: Development
