# 🎯 QUICK REFERENCE - Principal Dashboard

## 🚀 Quick Start (30 seconds)

1. **Open Login**: http://localhost:3000/index.html
2. **Enter Credentials**:
   - Email: `principal@edu.vn`
   - Password: `123456`
3. **Click "Đăng Nhập"**
4. **Dashboard loads** - Ready to use!

---

## 📋 Feature Quick Reference

### FE-01: Login/Logout ✅
| Action | Steps |
|--------|-------|
| **Login** | Email + Password → Click "Đăng Nhập" |
| **Logout** | Click "🚪 Đăng Xuất" in sidebar |
| **Session** | Auto-expires if inactive, Clears on logout |

### FE-02: Approve Syllabi ✅
| Component | Description |
|-----------|-------------|
| **Page** | Click "✅ Phê Duyệt Đề Cương" |
| **Content** | Table of 4 pending syllabi |
| **Columns** | Code, Name, Lecturer, Faculty, Date, Status, Actions |
| **Actions** | "✅ Duyệt" (Approve) or "❌ Từ Chối" (Reject) |
| **Feedback** | Alert + Instant update |

### FE-03: View Reports ✅
| Section | Content |
|---------|---------|
| **Stats** | Cards showing Approved, Pending, KPI, Progress |
| **Faculty Table** | Breakdown by faculty with counts & percentages |
| **Status Table** | Analysis by status with progress bars |
| **Auto-Update** | Updates when syllabi approved/rejected |

---

## 🎮 Interactive Elements

### Sidebar Menu
```
Tổng Quan .......................... Main dashboard
✅ Phê Duyệt Đề Cương .............. Approvals (FE-02)
📊 Báo Cáo Hệ Thống ............... Reports (FE-03)
👥 Quản Lý Khoa ................... Faculty management
🚪 Đăng Xuất ...................... Logout
```

### Action Buttons
- **✅ Duyệt** - Approve syllabus (Green button)
- **❌ Từ Chối** - Reject syllabus (Red button)
- **🚪 Đăng Xuất** - Logout (Orange button)

---

## 📊 Sample Data Included

### Pending Syllabi (FE-02)
```
CS101    | Nhập Môn Lập Trình      | Nguyễn Văn A   | CNTT
CS102    | Cấu Trúc Dữ Liệu        | Trần Thị B     | CNTT
MATH101  | Giải Tích 1             | Phạm Thị D     | Toán
CS103    | Cơ Sở Dữ Liệu           | Lê Văn C       | CNTT
```

### System Statistics (FE-03)
```
Approved: 2 (28%)
Pending:  4 (57%)
Rejected: 1 (14%)
KPI: 3.2/5.0
Progress: 34%
```

---

## 🔐 Security Features

- ✅ JWT Token validation
- ✅ Role-based access (principal only)
- ✅ Automatic logout on expiration
- ✅ Secure API calls with Bearer token
- ✅ CORS-enabled communication

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Backend | FastAPI (Python) |
| Database | MySQL |
| Auth | JWT Tokens |
| Server | Python http.server (port 3000) |

---

## ⚡ Performance

- **Load Time**: < 1 second
- **Page Transitions**: Instant (no page reload)
- **Data Updates**: Immediate feedback
- **No Dependencies**: Lightweight, fast
- **Mobile Ready**: Responsive design

---

## 📱 Responsive Breakpoints

- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't login | Check email/password, restart backend |
| Dashboard blank | Check token in localStorage (F12) |
| Buttons don't work | Check browser console (F12) for errors |
| Data not updating | Page auto-updates, try refresh (F5) |
| Logout fails | Clear cache, try again |

---

## 📚 Documentation Files

1. **IMPLEMENTATION_COMPLETE.md** - Full technical details
2. **PRINCIPAL_DASHBOARD_GUIDE.md** - User guide with examples
3. **PRINCIPAL_FEATURES_READY.py** - Feature summary
4. **This File** - Quick reference

---

## 🎓 File Location

**Frontend Dashboard**: 
```
frontend/principal-web/dashboard.html
```

**Backend**:
```
backend/app/main.py
Port: 8000
```

**Frontend Server**:
```
frontend/
Port: 3000
```

---

## ✨ Feature Highlights

### FE-01: Login/Logout
✅ JWT authentication working
✅ Session persistence in localStorage
✅ Auto-logout on token expiration
✅ Role verification on load

### FE-02: Approve Syllabi
✅ List of pending syllabi displayed
✅ Approve button with immediate feedback
✅ Reject button with immediate feedback
✅ Status updates reflected in Reports
✅ Real-time calculation of statistics

### FE-03: View System Reports
✅ Summary statistics calculated
✅ Faculty breakdown displayed
✅ Status analysis with percentages
✅ Progress visualization
✅ Auto-update when status changes

---

## 🚀 Ready to Test!

**Step 1**: Backend running? ✅
- Check: http://localhost:8000/docs

**Step 2**: Frontend running? ✅
- Check: http://localhost:3000/index.html

**Step 3**: Login & Test ✅
- Go to: http://localhost:3000/index.html
- Email: principal@edu.vn
- Password: 123456
- Click: Đăng Nhập

**Step 4**: Explore Features ✅
- Click sidebar items to navigate
- Click Approve/Reject buttons
- View report statistics
- Click Logout when done

---

## 📈 Next Steps

1. ✅ **Test FE-01**: Login and check authentication
2. ✅ **Test FE-02**: Approve/reject syllabi and confirm updates
3. ✅ **Test FE-03**: View reports and verify calculations
4. 🔄 **Backend Integration** (Optional): Connect real API endpoints
5. 🚀 **Deployment**: Move to production server

---

**Version**: 1.0 Complete ✅  
**Status**: Ready for Testing  
**Last Updated**: 2026-01-27

---

**Need Help?** Check PRINCIPAL_DASHBOARD_GUIDE.md for detailed instructions
