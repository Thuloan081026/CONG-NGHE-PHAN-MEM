# 🚀 Quick Start Guide - Lecturer Web v2.0

## ⚡ 5 Phút Bắt Đầu

### Step 1: Đăng Nhập (1 phút)
1. Truy cập: `http://localhost:3000`
2. Nhập email và password
3. Nhấn **"Đăng nhập"**
4. → Vào Dashboard

### Step 2: Xem Dashboard (1 phút)
- 5 Stats cards ở trên
- Recent syllabuses ở giữa
- Quick actions ở bên phải
- Sidebar menu bên trái

### Step 3: Tạo Đề Cương Đầu Tiên (2 phút)
1. Nhấn **"Create New Syllabus"** (nút xanh)
2. Điền thông tin:
   - Subject Code: `CS101`
   - Subject Name: `Introduction to Programming`
   - Credits: `3`
   - Semester: `1`
3. Nhấn **"Next"** hoặc tab khác
4. Nhấn **"Submit"** (cuối cùng)
5. → Success! ✓

### Step 4: Quản Lý Đề Cương (1 phút)
1. Nhấn **"View All Syllabuses"**
2. Bạn sẽ thấy đề cương vừa tạo
3. Nhấn **"Edit"** hoặc **"View"** để xem chi tiết

---

## 🎯 6 Chức Năng Chính - Quick Access

### 1️⃣ Đăng Nhập
- **Trang**: `http://localhost:3000`
- **Time**: 1 phút
- **Task**: Nhập email/password → Đăng nhập

### 2️⃣ Tạo Đề Cương
- **Trang**: Dashboard → **"Create New Syllabus"**
- **Time**: 5-10 phút
- **Task**: Fill 6 tabs (Basic, CLO, Content, Assessment, Prerequisites, Resources)

### 3️⃣ Chỉnh Sửa & Phiên Bản
- **Trang**: Dashboard → **"Version History"**
- **Time**: 3-5 phút
- **Task**: 
  1. Chọn đề cương
  2. Chọn 2 phiên bản
  3. So sánh (Diff)

### 4️⃣ Collaborative Review
- **Trang**: Dashboard → **"Collaborative Review"**
- **Time**: 5-10 phút
- **Task**:
  1. Tab "Yêu cầu xem xét" → Review đề cương
  2. Tab "Đề cương của tôi" → Xem feedback

### 5️⃣ Quản Lý Đề Cương
- **Trang**: Dashboard → **"View All Syllabuses"**
- **Time**: 2-3 phút
- **Task**: Search, filter, view/edit/delete

### 6️⃣ Thông Báo
- **Trang**: Dashboard → **"View Notifications"**
- **Time**: 1-2 phút
- **Task**: Xem thông báo, mark as read, filter

---

## 💡 Tips & Tricks

### ⏱️ Auto-save Works!
- Khi tạo đề cương, tự động lưu **mỗi 2 phút**
- Bạn có thể **tắt tab** mà **không mất dữ liệu**
- Dữ liệu lưu dưới status: **"Draft"**

### 🔒 Login Stays
- Refresh page → Vẫn logged in
- Token lưu trong localStorage
- Logout → Xóa token + redirect login

### 🎨 Responsive Design
- **Desktop**: Full layout, sidebar visible
- **Tablet**: Collapsible sidebar, 2-3 columns
- **Mobile**: 1 column, hamburger menu

### 🔍 Quick Search
- Trang **Syllabuses**: Search by code/name
- Trang **Notifications**: Filter by type
- Trang **Collaborative Review**: Filter by priority/status

### ⌨️ Keyboard Shortcuts (if implemented)
- `Ctrl+S` - Save (in form)
- `Esc` - Close modal
- `Enter` - Submit form

---

## ❌ Common Issues & Solutions

### ❌ "Can't login"
**Solution:**
1. Check email is correct
2. Check password is correct
3. Check backend API is running (`http://localhost:8000`)
4. Clear browser cache: `Ctrl+Shift+Delete`
5. Try again

### ❌ "Page looks broken"
**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` Mac)
2. Clear localStorage: `localStorage.clear()` in console
3. Close & reopen browser
4. Check JavaScript errors: Press `F12`

### ❌ "Lost my data"
**Solution:**
1. If Draft: Check localStorage
2. If Submitted: Check Version History
3. If Deleted: Can't recover (only Draft can delete)
4. Contact admin for backup restore

### ❌ "API not responding"
**Solution:**
1. Check backend is running: `http://localhost:8000`
2. Check internet connection
3. Check CORS headers
4. Wait 30 seconds and retry

---

## 🎓 Step-by-Step: Create Your First Syllabus

### **Step 1: Go to Create Page** (30 seconds)
```
Dashboard → "Create New Syllabus" button
```

### **Step 2: Fill Basic Info** (2 minutes)
| Field | Example |
|-------|---------|
| Subject Code | CS201 |
| Subject Name | Data Structures |
| Credits | 3 |
| Semester | 2 |
| Description | Study of fundamental data structures... |

### **Step 3: Add CLOs** (2 minutes)
Click **"+ Add CLO"** 3-4 times:
- CLO 1: Understand fundamental data structures
- CLO 2: Implement and analyze algorithms
- CLO 3: Design efficient solutions
- CLO 4: Apply DS to real-world problems

### **Step 4: Define PLOs** (1 minute)
Click **"+ Add PLO"**:
- PLO 1: Generic skill
- PLO 2: Subject-specific skill
- ...

### **Step 5: Map CLO-PLO** (1 minute)
Check which CLOs support which PLOs using checkboxes

### **Step 6: Add Content** (3 minutes)
Click **"+ Add Chapter"** for each:
- Chapter 1: Introduction (2 hours)
- Chapter 2: Arrays & Lists (4 hours)
- Chapter 3: Stacks & Queues (3 hours)
- ...

### **Step 7: Set Assessment Weights** (1 minute)
| Component | Weight |
|-----------|--------|
| Attendance | 10% |
| Assignment | 20% |
| Midterm | 20% |
| Final | 30% |
| Project | 20% |
| **TOTAL** | **100%** ✓ |

### **Step 8: Add Prerequisites** (1 minute)
- CS101 (Prerequisite)
- EN101 (Corequisite)

### **Step 9: Add Resources** (1 minute)
- Textbook: "Algorithm Design Manual" (2nd edition)
- Reference: Stack Overflow, GeeksforGeeks
- Materials: PowerPoint slides, practice problems

### **Step 10: Submit** (30 seconds)
1. Review all information
2. Click **"Submit for Review"** (at top)
3. Confirm dialog
4. Success! ✓

**Total Time: ~15 minutes** ⏱️

---

## 🔄 Workflow: From Create to Approval

```
1️⃣ Create & Save (Draft)
   ↓ (Auto-save every 2 minutes)
2️⃣ Submit for Review (Submitted)
   ↓ (Notify HoD)
3️⃣ HoD Reviews & Provides Feedback
   ↓ (You receive notification)
4️⃣ You See Feedback in Collaborative Review
   ↓ (You make changes)
5️⃣ Create New Version
   ↓ (Auto-save new version)
6️⃣ Re-submit with Changes (Submitted v2)
   ↓ (Notify HoD again)
7️⃣ HoD Approves
   ↓
8️⃣ Status: Approved/Published ✓
```

---

## 📊 Feature Overview Table

| # | Feature | Where | Time | Difficulty |
|---|---------|-------|------|------------|
| 1️⃣ | Login | `http://localhost:3000` | 1 min | Easy |
| 2️⃣ | Create Syllabus | Dashboard → Create | 15 min | Medium |
| 3️⃣ | Version Control | Dashboard → Version History | 5 min | Medium |
| 4️⃣ | Collaborative Review | Dashboard → Collaborative Review | 5 min | Medium |
| 5️⃣ | Manage Syllabuses | Dashboard → View All | 3 min | Easy |
| 6️⃣ | Notifications | Dashboard → Notifications | 2 min | Easy |

---

## 🎯 Today's Agenda (First Day)

| Time | Task | Duration |
|------|------|----------|
| 09:00 | Login to system | 2 min |
| 09:05 | Read Quick Start guide | 5 min |
| 09:10 | Explore Dashboard | 3 min |
| 09:15 | Create first syllabus | 15 min |
| 09:30 | View in list | 2 min |
| 09:35 | Edit syllabus | 5 min |
| 09:45 | Submit for review | 2 min |
| 09:50 | Check notifications | 2 min |
| 10:00 | **DONE! ✓** | 1 hour |

---

## 📖 Need More Help?

### Quick Questions?
→ Check **[FEATURES_GUIDE_VI.md](./FEATURES_GUIDE_VI.md)** → **FAQ section**

### Detailed Guide?
→ Read **[FEATURES_GUIDE_VI.md](./FEATURES_GUIDE_VI.md)** (Vietnamese, 2500+ lines)

### Technical Issues?
→ Check **[UPDATES_README.md](./UPDATES_README.md)** → **Known Issues**

### Need to Test?
→ Use **[TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md)**

### Project Overview?
→ Read **[SUMMARY.md](./SUMMARY.md)**

---

## 🚨 Emergency

**Something broken?**

1. **Restart browser**: Close all tabs and reopen
2. **Clear cache**: `Ctrl+Shift+Delete` → Clear all
3. **Clear localStorage**: Open F12 → Console → `localStorage.clear()`
4. **Try incognito**: `Ctrl+Shift+N` → Test there
5. **Contact support**: pm@school.edu

---

## ✅ Checklist: Ready to Use?

Before you start, make sure:

- [ ] Backend API running: `http://localhost:8000` ✓
- [ ] Frontend running: `http://localhost:3000` ✓
- [ ] Browser supports: Chrome/Firefox/Safari ✓
- [ ] JavaScript enabled ✓
- [ ] Cookie & localStorage enabled ✓
- [ ] You have login credentials ✓

All checked? → **Let's go! 🚀**

---

## 🎉 You're Ready!

You now know:
- ✅ How to login
- ✅ How to create a syllabus
- ✅ How to manage versions
- ✅ How to collaborate with colleagues
- ✅ How to get notifications
- ✅ Where to find help

### Next Steps:
1. Try creating your first syllabus
2. Experiment with all features
3. Read FEATURES_GUIDE_VI.md for details
4. Ask questions (no question too small!)
5. Provide feedback to improve system

---

## 📞 Support

**Questions?**
- User Support: support@school.edu
- Training: training@school.edu
- Technical: backend@school.edu

**Hours**: Monday-Friday, 09:00-17:00

---

**Version**: 2.0.0
**Last Updated**: 06/01/2026
**Status**: Ready to Use ✓

🎓 **Happy Lecturing!**
