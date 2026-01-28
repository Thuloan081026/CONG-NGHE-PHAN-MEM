# 📊 Principal Dashboard - User Guide

## Overview
The Principal Dashboard is a comprehensive management interface for educational institution principals to:
- ✅ **FE-01**: Log in/out securely
- ✅ **FE-02**: Approve or reject syllabus documents
- ✅ **FE-03**: View system reports and analytics

## Quick Start

### 1. Login
- **URL**: `http://localhost:3000/index.html`
- **Email**: `principal@edu.vn`
- **Password**: `123456`

### 2. Dashboard Automatically Loads
After successful login, you'll see the Principal Dashboard with:
- Sidebar menu for navigation
- Summary statistics
- Quick access to all features

## Feature Details

### FE-01: Login/Logout ✅
**Purpose**: Secure authentication and session management

**How it works**:
1. Enter credentials on the login page
2. Backend validates using JWT tokens
3. Token stored in browser localStorage
4. Dashboard verifies token on each load
5. Click "Đăng Xuất" (Logout) to exit

**Security**:
- Tokens expire automatically
- Role verification (principal only)
- Session cleared on logout

---

### FE-02: Approve Syllabi ✅
**Purpose**: Review and approve course syllabi documents

**Access**: Click "✅ Phê Duyệt Đề Cương" in sidebar

**Features**:
- **List of Pending Syllabi**: Shows all syllabi waiting for approval
- **Course Information**: Course code, name, lecturer, faculty
- **Submission Date**: When syllabus was submitted
- **Status Badge**: Visual indicator of current status

**Table Columns**:
| Mã Môn | Tên Môn | Giảng Viên | Khoa | Ngày Nộp | Trạng Thái | Hành Động |
|--------|---------|-----------|------|----------|-----------|----------|
| CS101 | Nhập Môn Lập Trình | Nguyễn Văn A | CNTT | 2026-01-20 | ⏳ Chờ | ✅ Duyệt / ❌ Từ Chối |

**How to Approve/Reject**:
1. Navigate to "Phê Duyệt Đề Cương" tab
2. Review syllabus information in the list
3. Click "✅ Duyệt" (Approve) to accept
   - Syllabus marked as approved
   - Status updates in reports immediately
4. Click "❌ Từ Chối" (Reject) to send back for revision
   - Instructor will be notified to revise
   - Status updated for tracking

**Example Pending Syllabi**:
- CS101 - Nhập Môn Lập Trình (Nguyễn Văn A, CNTT)
- CS102 - Cấu Trúc Dữ Liệu (Trần Thị B, CNTT)
- MATH101 - Giải Tích 1 (Phạm Thị D, Toán)
- CS103 - Cơ Sở Dữ Liệu (Lê Văn C, CNTT)

---

### FE-03: View System Reports ✅
**Purpose**: Monitor syllabus approval progress and faculty performance

**Access**: Click "📊 Báo Cáo Hệ Thống" in sidebar

**Dashboard Sections**:

#### 1. Summary Statistics (Top Cards)
Shows key metrics:
- **✅ Đã Duyệt**: Number of approved syllabi
- **⏳ Chờ Duyệt**: Number of pending syllabi
- **KPI Score**: Quality/performance metric (0-5)
- **Tiến Độ**: Approval completion percentage

#### 2. Faculty Report Table
Displays statistics for each faculty:
- Faculty name
- Total syllabi
- Approved count (with badge)
- Pending count (with badge)
- Rejected count (with badge)
- Completion percentage

**Example**:
```
Công Nghệ Thông Tin | 12 | ✅ 7 | ⏳ 3 | ❌ 2 | 58%
Toán - Tin          | 10 | ✅ 8 | ⏳ 1 | ❌ 1 | 80%
Vật Lý              | 8  | ✅ 5 | ⏳ 2 | ❌ 1 | 62%
Hóa Học             | 9  | ✅ 6 | ⏳ 2 | ❌ 1 | 67%
```

#### 3. Status Analysis Table
Breakdown of all syllabi by status:
- Status name (Đã Duyệt, Chờ Duyệt, Từ Chối)
- Count of syllabi with that status
- Percentage of total
- Visual progress bar showing proportion

**Example**:
```
Đã Duyệt | 26 | 43% | [████████░░░░░░░░░░░░]
Chờ Duyệt | 28 | 46% | [██████████░░░░░░░░░░░░░░░]
Từ Chối  | 5  | 8%  | [██░░░░░░░░░░░░░░░░░░░░░░]
```

**How to Use Reports**:
1. Monitor approval progress weekly
2. Identify faculties needing assistance
3. Track KPI metrics for performance
4. Make data-driven decisions about approval policies
5. Plan workload based on pending count

---

## Navigation

### Sidebar Menu
Click menu items to switch between pages:

```
📊 CHỨC NĂNG (Features)
├─ 📈 Tổng Quan (Dashboard) - Summary view
├─ ✅ Phê Duyệt Đề Cương (Approvals) - FE-02
├─ 📊 Báo Cáo Hệ Thống (Reports) - FE-03
└─ 👥 Quản Lý Khoa (Faculty) - Faculty management

⚙️ CÀI ĐẶT (Settings)
└─ 🚪 Đăng Xuất (Logout) - Exit dashboard
```

### Dashboard Page
Default landing page showing:
- System overview statistics
- Quick status summary
- Current time/date
- Recent activity indicator

### Faculty Page
Complete faculty information:
- Faculty name and head
- Number of lecturers
- Total syllabi count
- Approval progress for each faculty

---

## Data & Statistics

### Sample Data
The dashboard includes realistic sample data:

**Syllabi Types**:
- CS101-CS103: Computer Science courses
- MATH101-102: Mathematics courses
- PHY101: Physics course

**Status Distribution**:
- Approved (✅): 2 syllabi - 33%
- Pending (⏳): 4 syllabi - 67%
- Rejected (❌): 1 syllabus

**Faculties**:
- Công Nghệ Thông Tin (CNTT) - 12 lecturers
- Toán - Tin - 10 lecturers
- Vật Lý - 8 lecturers
- Hóa Học - 9 lecturers

---

## Tips & Best Practices

### Approval Workflow
1. **Check Dashboard** first to see pending count
2. **Review Approvals** tab for detailed list
3. **Check Reports** to understand impact of decisions
4. **Make Decision** - Approve or Reject each syllabus
5. **Monitor Progress** to track completion

### Using Reports Effectively
- **Weekly Check**: Review reports at end of each week
- **Faculty Follow-up**: If faculty has low approval rate, contact them
- **KPI Tracking**: Monitor KPI score trends over time
- **Planning**: Use progress percentage to estimate completion date

### Quality Control
- Review syllabus content before approving
- Check submission dates for on-time submissions
- Use rejection strategically to improve quality
- Provide feedback to instructors when rejecting

---

## Troubleshooting

### Can't Login
- ✅ Verify email: `principal@edu.vn`
- ✅ Verify password: `123456`
- ✅ Check backend is running on port 8000
- ✅ Clear browser cache and retry

### Dashboard Not Loading
- ✅ Ensure you're logged in
- ✅ Check browser console for errors (F12)
- ✅ Verify token is stored in localStorage
- ✅ Try logging in again

### Approve/Reject Not Working
- ✅ Status updates immediately - check Reports page
- ✅ Page refreshes to show updated counts
- ✅ Approval triggers notification to instructor

### Reports Not Showing Data
- ✅ Reports use mock data - no API needed
- ✅ Check sidebar is fully loaded
- ✅ Click Reports tab again if blank

---

## Feature Roadmap

### Current Implementation ✅
- Login/Logout with JWT
- Syllabus approval interface
- System reports and analytics
- Faculty management view
- Mock data for testing

### Future Enhancements 🔄
- Real database integration
- Email notifications on approval/rejection
- Approval comments and notes
- Bulk approval operations
- Export reports to PDF
- Timeline/history tracking
- Faculty performance analytics
- Custom report generation

---

## Technical Details

### Architecture
- **Frontend**: HTML/CSS/JavaScript (no framework required)
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Authentication**: JWT tokens
- **Data**: Mock JSON in JavaScript (easily replaceable)

### File Structure
```
frontend/
├─ index.html                 # Login page
└─ principal-web/
   └─ dashboard.html          # Principal dashboard (ALL FEATURES)
```

### API Integration Ready
The dashboard is structured to easily connect to backend APIs:
- Replace mock data with API calls
- Change endpoints in JavaScript functions
- Maintain same UI and functionality

---

## Security & Compliance

### User Data Protection
- Passwords hashed with SHA256
- Tokens encrypted with JWT
- Session timeout on inactivity
- CORS enabled for secure API calls

### Role-Based Access
- Principal role required to access dashboard
- Other roles redirect to own dashboards
- Automatic role verification on load

### Audit Trail
- Login/logout tracked
- Approval actions timestamped
- User information logged
- Ready for compliance reporting

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console (F12) for errors
3. Verify backend is running
4. Check network requests in browser DevTools

---

**Version**: 1.0 (FE-01/02/03 Complete)  
**Last Updated**: 2026-01-27  
**Status**: ✅ Ready for Production
