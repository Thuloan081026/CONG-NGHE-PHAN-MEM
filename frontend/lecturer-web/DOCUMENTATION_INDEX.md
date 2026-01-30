# 📚 Documentation Index - Lecturer Web v2.0

## 📖 Quick Navigation

### 🎯 **Getting Started** (Bắt đầu nhanh)
1. **[SUMMARY.md](./SUMMARY.md)** - Tóm tắt dự án & status
2. **[FEATURES_GUIDE_VI.md](./FEATURES_GUIDE_VI.md)** - Hướng dẫn sử dụng 6 chức năng (Tiếng Việt)

### 👨‍💻 **For Developers** (Dành cho lập trình viên)
1. **[UPDATES_README.md](./UPDATES_README.md)** - Chi tiết thay đổi code
2. **[README.md](./README.md)** - Tài liệu chung (nếu có)
3. **[API_REFERENCE.md](../backend/API_REFERENCE.md)** - API endpoints (backend)

### 🧪 **For QA Team** (Dành cho kiểm thử)
1. **[TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md)** - Checklist kiểm thử (500+ items)

### 📁 **File Structure** (Cấu trúc thư mục)

```
lecturer-web/
├── 📄 index.html                    # Login page
├── 📄 dashboard.html                # Dashboard (UPDATED)
├── 📄 syllabus-list.html            # My Syllabuses
├── 📄 syllabus-create.html          # Create Syllabus
├── 📄 syllabus-edit.html            # Edit redirect
├── 📄 syllabus-versions.html        # Version Control (NEW)
├── 📄 collaborative-review.html     # Collaborative Review (UPDATED)
├── 📄 comments-feedback.html        # Comments & Feedback
├── 📄 search-reference.html         # Search References
├── 📄 notifications.html            # Notifications (NEW)
├── 📄 profile.html                  # User Profile
├── 📄 home.html                     # Landing Page
├── 📄 index-landing.html            # Landing alternative
│
├── 📁 assets/
│   ├── 📁 css/
│   │   ├── main.css
│   │   ├── menu.css
│   │   ├── responsive.css
│   │   ├── lecturer-dashboard.css   # (UPDATED with 5-column layout)
│   │   └── color/
│   │       ├── color-1.css
│   │       ├── color-2.css
│   │       └── ...
│   ├── 📁 js/
│   │   ├── main.js
│   │   ├── main.min.js
│   │   ├── menu.js
│   │   ├── menu.min.js
│   │   └── common-pages.min.js
│   ├── 📁 plugins/
│   │   ├── bootstrap/
│   │   ├── jquery/
│   │   ├── moment/
│   │   └── ... (other libraries)
│   ├── 📁 icon/
│   │   ├── icofont/
│   │   ├── themify-icons/
│   │   └── ... (icon sets)
│   └── 📁 images/
│
├── 📄 SUMMARY.md                    # Project summary (NEW)
├── 📄 FEATURES_GUIDE_VI.md          # User guide Vietnamese (NEW)
├── 📄 UPDATES_README.md             # Developer updates (NEW)
├── 📄 TESTING_CHECKLIST.md          # QA checklist (NEW)
├── 📄 DOCUMENTATION_INDEX.md        # This file (NEW)
├── 📄 README.md                     # General readme
└── 📄 ... (other files)
```

---

## 🎯 6 Main Features (6 Chức Năng Chính)

### 1. **Login / Logout** (Đăng nhập/Đăng xuất)
- **Files**: `index.html`
- **Related Files**: 
  - All pages check authentication
  - localStorage token management
- **Documentation**: FEATURES_GUIDE_VI.md → Section 01

### 2. **Create Syllabus** (Tạo Đề Cương)
- **Files**: `syllabus-create.html`
- **Features**:
  - Basic Info (code, name, credits)
  - CLO & PLO definition
  - Content chapters
  - Assessment weights
  - Prerequisites/Corequisites
  - Resources (textbooks, references, materials)
- **Documentation**: FEATURES_GUIDE_VI.md → Section 02

### 3. **Edit & Version Control** (Chỉnh Sửa & Phiên Bản)
- **Files**: `syllabus-versions.html` (NEW)
- **Features**:
  - Version history list
  - Semantic diff comparison
  - Submit to HoD
  - Restore version
- **Documentation**: FEATURES_GUIDE_VI.md → Section 03

### 4. **Collaborative Review** (Xem Xét Cộng Tác)
- **Files**: `collaborative-review.html` (UPDATED)
- **Features**:
  - Review requests for you
  - Your syllabuses in review
  - Comment threads
  - Reply to feedback
  - Filters & stats
- **Documentation**: FEATURES_GUIDE_VI.md → Section 04

### 5. **Manage Syllabuses** (Quản Lý Đề Cương)
- **Files**: `syllabus-list.html`
- **Features**:
  - List all syllabuses
  - Search & filter
  - View/Edit/Delete actions
  - Version comparison
- **Documentation**: FEATURES_GUIDE_VI.md → Section 05

### 6. **Notifications** (Thông Báo)
- **Files**: `notifications.html` (NEW)
- **Features**:
  - Notification list
  - Type filtering
  - Mark as read
  - Stats dashboard
  - Action links
- **Documentation**: FEATURES_GUIDE_VI.md → Section 06

---

## 📚 Documentation by Role

### 👤 **For End Users** (Giảng Viên)
**Start here:**
1. [FEATURES_GUIDE_VI.md](./FEATURES_GUIDE_VI.md) - Complete user guide

**Sections:**
- 01. Đăng nhập/Đăng xuất
- 02. Tạo Mới Syllabus
- 03. Chỉnh sửa & Cập nhật Phiên bản
- 04. Tham gia Collaborative Review
- 05. Quản lý Syllabus Cá nhân
- 06. Nhận Thông báo
- Dashboard Overview
- Mẹo & Lưu ý
- FAQ

### 👨‍💼 **For Project Managers** (Quản Lý Dự Án)
**Start here:**
1. [SUMMARY.md](./SUMMARY.md) - Project overview & status

**Sections:**
- 6 Main Features
- Files Changed/Created
- Dashboard Design
- Security & Authentication
- Deployment Checklist
- Success Metrics
- Version History

### 👨‍💻 **For Developers** (Lập Trình Viên)
**Start here:**
1. [UPDATES_README.md](./UPDATES_README.md) - Technical changes
2. [TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md) - Implementation checklist

**Key Sections:**
- Files Updated/Created
- Color Scheme & Styling
- Responsive Design
- API Endpoints
- Known Issues
- Security Notes

### 🧪 **For QA/Testers** (Kiểm Thử Viên)
**Start here:**
1. [TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md) - Comprehensive testing checklist

**Test Coverage:**
- Authentication (Login/Logout)
- Create Syllabus Form
- Version Control & Comparison
- Collaborative Review
- Syllabus Management
- Notifications
- Dashboard
- UI/UX
- Security
- Performance
- Responsive Design
- Edge Cases

### 🔒 **For Security Team** (Bảo Mật)
**Relevant Sections:**
- UPDATES_README.md → Security Notes
- TESTING_CHECKLIST.md → Security Checks
- FEATURES_GUIDE_VI.md → FAQ → Bảo mật

**Key Points:**
- JWT token management
- localStorage storage
- Role-based access
- Input validation
- HTTPS recommendations

---

## 🔗 Cross-References

### By Feature

**Feature 1: Login/Logout**
- Code: `index.html`, all `*-dashboard.css`
- Docs: FEATURES_GUIDE_VI.md → 01
- Tests: TESTING_CHECKLIST.md → 01
- API: `/auth/login`, `/users/me`

**Feature 2: Create Syllabus**
- Code: `syllabus-create.html`
- Docs: FEATURES_GUIDE_VI.md → 02
- Tests: TESTING_CHECKLIST.md → 02
- API: `POST /syllabus/`

**Feature 3: Version Control**
- Code: `syllabus-versions.html`
- Docs: FEATURES_GUIDE_VI.md → 03
- Tests: TESTING_CHECKLIST.md → 03
- API: `GET /syllabus/{id}/versions`, `POST /syllabus/{id}/submit`

**Feature 4: Collaborative Review**
- Code: `collaborative-review.html`
- Docs: FEATURES_GUIDE_VI.md → 04
- Tests: TESTING_CHECKLIST.md → 04
- API: `GET /syllabus/review-requests`

**Feature 5: Manage Syllabuses**
- Code: `syllabus-list.html`
- Docs: FEATURES_GUIDE_VI.md → 05
- Tests: TESTING_CHECKLIST.md → 05
- API: `GET /syllabus/`, `PUT /syllabus/{id}`, `DELETE /syllabus/{id}`

**Feature 6: Notifications**
- Code: `notifications.html`
- Docs: FEATURES_GUIDE_VI.md → 06
- Tests: TESTING_CHECKLIST.md → 06
- API: `GET /notifications`, `PUT /notifications/{id}/read`

---

## 📋 Checklist for Different Scenarios

### 🚀 **Deploying to Production**
1. [ ] Read UPDATES_README.md
2. [ ] Run TESTING_CHECKLIST.md
3. [ ] Check SUMMARY.md → Deployment Checklist
4. [ ] Build CSS/JS (minify)
5. [ ] Setup environment variables
6. [ ] Enable HTTPS/SSL
7. [ ] Configure CORS
8. [ ] Test on staging
9. [ ] Deploy frontend
10. [ ] Deploy backend API
11. [ ] Run smoke tests
12. [ ] Monitor performance

### 👥 **Training Users**
1. [ ] Share FEATURES_GUIDE_VI.md
2. [ ] Conduct training session
3. [ ] Demo all 6 features
4. [ ] Practice exercises
5. [ ] Q&A session
6. [ ] Provide contact support
7. [ ] Monitor adoption rate

### 🧪 **Testing New Changes**
1. [ ] Read TESTING_CHECKLIST.md
2. [ ] Setup test environment
3. [ ] Run unit tests
4. [ ] Run integration tests
5. [ ] Manual testing all 6 features
6. [ ] Test on different devices
7. [ ] Test error scenarios
8. [ ] Performance testing
9. [ ] Security testing
10. [ ] Sign-off form

### 🔧 **Debugging Issues**
1. [ ] Check UPDATES_README.md → Known Issues
2. [ ] Check TESTING_CHECKLIST.md → Edge Cases
3. [ ] Check FEATURES_GUIDE_VI.md → FAQ
4. [ ] Check console (F12)
5. [ ] Check network (F12)
6. [ ] Check localStorage
7. [ ] Check API response
8. [ ] Contact support

---

## 🌐 URL Map

| Feature | URL | File |
|---------|-----|------|
| Login | `/` | `index.html` |
| Dashboard | `/dashboard.html` | `dashboard.html` |
| Create Syllabus | `/syllabus-create.html` | `syllabus-create.html` |
| My Syllabuses | `/syllabus-list.html` | `syllabus-list.html` |
| Version Control | `/syllabus-versions.html` | `syllabus-versions.html` |
| Collaborative Review | `/collaborative-review.html` | `collaborative-review.html` |
| Notifications | `/notifications.html` | `notifications.html` |
| Profile | `/profile.html` | `profile.html` |

---

## 📞 Support Resources

### For Users:
- **User Guide**: FEATURES_GUIDE_VI.md
- **FAQ**: FEATURES_GUIDE_VI.md → FAQ section
- **Contact**: pm@school.edu

### For Developers:
- **Technical Guide**: UPDATES_README.md
- **Code Changes**: Check git diff
- **API Docs**: API_REFERENCE.md (backend)
- **Contact**: frontend@school.edu

### For QA:
- **Test Guide**: TESTING_CHECKLIST.md
- **Known Issues**: UPDATES_README.md
- **Contact**: qa@school.edu

### For Management:
- **Project Status**: SUMMARY.md
- **Metrics**: SUMMARY.md → Success Metrics
- **Risks**: SUMMARY.md → Known Limitations
- **Contact**: pm@school.edu

---

## 📈 Document Statistics

| Document | Lines | Sections | Purpose |
|----------|-------|----------|---------|
| SUMMARY.md | ~400 | 15 | Project overview |
| FEATURES_GUIDE_VI.md | ~2500 | 10 | User guide |
| UPDATES_README.md | ~300 | 12 | Developer guide |
| TESTING_CHECKLIST.md | ~600 | 15 | QA checklist |
| DOCUMENTATION_INDEX.md | ~400 | 12 | This index |

**Total**: ~4200 lines of documentation

---

## 🎯 Reading Guide by Role

### 🎓 **New User (First Time)**
1. Read: SUMMARY.md (5 min)
2. Read: FEATURES_GUIDE_VI.md → Section 01-06 (30 min)
3. Practice: Try creating a syllabus (15 min)
4. Total: 50 minutes

### 👨‍💻 **New Developer (First Time)**
1. Read: UPDATES_README.md (15 min)
2. Check: File structure (10 min)
3. Setup: Local environment (20 min)
4. Review: TESTING_CHECKLIST.md → relevant sections (15 min)
5. Total: 60 minutes

### 🧪 **New QA (First Time)**
1. Read: SUMMARY.md → Features (10 min)
2. Read: TESTING_CHECKLIST.md → All sections (40 min)
3. Setup: Test environment (20 min)
4. Execute: Sample tests (30 min)
5. Total: 100 minutes

---

## ✅ Last Updated

- **Document Version**: 1.0
- **Last Updated**: 06/01/2026
- **By**: AI Assistant
- **Status**: Final Release

---

## 📞 Contact

**Questions about Documentation?**
- Documentation Lead: docs@school.edu

**Questions about Features?**
- Product Manager: pm@school.edu

**Questions about Code?**
- Tech Lead: frontend@school.edu

**Questions about Testing?**
- QA Manager: qa@school.edu

---

## 🙏 Thank You!

Thank you for using this documentation. We hope it helps you understand and use the Lecturer Web system effectively.

**Happy Lecturing! 🎓**

---

**Navigation**: [Home](#) | [Features](./FEATURES_GUIDE_VI.md) | [Updates](./UPDATES_README.md) | [Tests](./TESTING_CHECKLIST.md) | [Summary](./SUMMARY.md)
