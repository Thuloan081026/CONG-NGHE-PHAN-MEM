# 📊 DASHBOARDS WITH LIVE DATA - QUICK REFERENCE

All dashboards now display real mock data on page load!

## ✅ Testing Each Dashboard

### 1. **Student Dashboard** 
🔗 **Direct Link**: [http://localhost:3000/student-web/dashboard.html](http://localhost:3000/student-web/dashboard.html)

**What You'll See:**
- ✅ 5 Enrolled Courses (CS301, CS401, CS201, CS102, CS303)
- ✅ Course details table with lecturer names
- ✅ Faculty information
- ✅ Update dates
- ✅ View and Subscribe buttons

**Mock Data:**
```
CS301 - Cơ sở dữ liệu | Lecturer: TS. Nguyễn Văn A | 28/12/2025
CS401 - Trí tuệ nhân tạo | Lecturer: TS. Trần Thị B | 27/12/2025
CS201 - Cấu trúc dữ liệu | Lecturer: TS. Lê Văn C | 26/12/2025
CS102 - Lập trình hướng đối tượng | Lecturer: ThS. Phạm Văn D | 25/12/2025
CS303 - Mạng máy tính | Lecturer: TS. Hoàng Thị E | 24/12/2025
```

---

### 2. **Lecturer Dashboard** 
🔗 **Direct Link**: [http://localhost:3000/lecturer-web/dashboard.html](http://localhost:3000/lecturer-web/dashboard.html)

**What You'll See:**
- ✅ Welcome message with lecturer name
- ✅ 4 Stat Cards:
  - Total Syllabuses: 5
  - Published: 2
  - In Review: 1
  - Draft: 1
- ✅ Recent syllabuses table with all details
- ✅ Status badges (Published, In Review, Draft)
- ✅ Quick action buttons

**Mock Data Loaded:**
- CS301 - Cơ sở dữ liệu nâng cao (Published)
- CS401 - Trí tuệ nhân tạo (In Review)
- CS201 - Cấu trúc dữ liệu (Published)
- CS102 - Lập trình hướng đối tượng (Draft)
- CS303 - Mạng máy tính (Published)

---

### 3. **Admin Dashboard** 
🔗 **Direct Link**: [http://localhost:3000/admin-web/dashboard-interactive.html](http://localhost:3000/admin-web/dashboard-interactive.html)

**What You'll See:**
- ✅ Interactive sidebar with 4 pages
- ✅ Dashboard page with key metrics
- ✅ Users management page
- ✅ System settings page
- ✅ Reports page

**Key Metrics Displayed:**
- Total Users: 2,850
- Active Syllabi: 487
- System Errors: 3
- Uptime: 99.8%

**Pages:**
1. **Dashboard** - Overview with stat cards and recent activities
2. **Users** - User management table (6 sample users)
3. **System** - Database & SMTP configuration
4. **Reports** - Role statistics and system reports

---

### 4. **Academic Affairs Dashboard** 
🔗 **Direct Link**: [http://localhost:3000/academic-affairs-web/dashboard-interactive.html](http://localhost:3000/academic-affairs-web/dashboard-interactive.html)

**What You'll See:**
- ✅ Interactive sidebar with 5 pages
- ✅ Dashboard with pending approvals
- ✅ Syllabi management
- ✅ PLO (Program Learning Outcomes) management
- ✅ Reports with faculty progress
- ✅ Course management

**Key Metrics Displayed:**
- Pending Syllabi: 8
- Approved Syllabi: 287
- Active Courses: 54
- Completion Rate: 87%

**Pages:**
1. **Dashboard** - Pending syllabi with Approve/Reject buttons
2. **Syllabi** - Complete syllabus list with filters
3. **PLO** - Program Learning Outcomes management
4. **Reports** - Faculty progress with progress bars
5. **Courses** - Course management by year/cohort

---

### 5. **Principal Dashboard** 
🔗 **Direct Link**: [http://localhost:3000/principal-web/dashboard.html](http://localhost:3000/principal-web/dashboard.html)

**What You'll See:**
- ✅ Interactive sidebar with multiple pages
- ✅ Approval interface for syllabi (FE-02)
- ✅ System reports and analytics (FE-03)
- ✅ Key metrics and statistics
- ✅ Faculty breakdown table

**Features:**
- Approve/Reject buttons for pending syllabi
- Real-time status updates
- Faculty performance metrics
- Progress bars and analytics

---

## 🔄 How to Test with Login

### Option 1: Direct Links (Mock Data Only)
Simply click any dashboard link above to see immediate data display.

### Option 2: Login & Navigate
1. Open [http://localhost:3000/index.html](http://localhost:3000/index.html)
2. Login with credentials:

**Test Credentials:**
```
Student:         student@edu.vn / 123456
Lecturer:        lecturer@edu.vn / 123456
Admin:           admin@edu.vn / 123456
Academic Affairs: aa@edu.vn / 123456
Principal:       principal@edu.vn / 123456
```

3. You'll be redirected to the corresponding dashboard
4. All mock data will load automatically

---

## 📈 Data Loading Flow

```
Page Load
    ↓
Check for Mock Data Object
    ↓
Calculate Statistics (counts, totals)
    ↓
Animate Stat Cards
    ↓
Populate Tables with Data
    ↓
Display Result
```

---

## ✨ Features in All Dashboards

✅ **Instant Data Display**
- Mock data loads immediately on page open
- No waiting for API calls
- Fallback to demo data if offline

✅ **Animated Numbers**
- Stat cards count up smoothly
- Creates engaging visual effect
- Takes ~1 second to complete

✅ **Interactive Tables**
- View details button
- Status badges with colors
- Responsive design
- Hover effects

✅ **Multi-Page Navigation**
- Sidebar menu for navigation
- Active page highlighting
- Smooth page transitions
- No reload required

✅ **Professional Styling**
- Gradient backgrounds
- Color-coded status badges
- Responsive layout
- Modern typography

---

## 🔧 How to Verify Data is Displaying

### In Browser Console (F12):
```javascript
// Should show mock data object
console.log(mockStudentData)      // Student
console.log(mockLecturerData)     // Lecturer
console.log(mockAdminData)        // Admin
console.log(mockAAData)           // Academic Affairs
```

### Check Network Tab:
- Look for HTML requests to dashboard files
- Should NOT see API calls to /syllabus/ or other APIs
- Mock data is embedded in the page

### Check Elements:
- Open Developer Tools → Elements tab
- Find tables with data populated
- Find stat cards with numbers displayed
- All should contain real mock data values

---

## 🚀 Quick Test Checklist

- [ ] Open student dashboard → See 5 courses
- [ ] Open lecturer dashboard → See stat cards with numbers
- [ ] Open admin dashboard → See key metrics
- [ ] Open AA dashboard → See syllabi list
- [ ] Open principal dashboard → See approve buttons
- [ ] Click sidebar items → Pages switch
- [ ] Check stat cards → Numbers animated
- [ ] Refresh page → Data reloads instantly
- [ ] Open in new tab → Data displays again

---

## 📊 Sample Data Overview

### Student Data (5 items)
- Course codes, names, lecturers
- Faculty assignments
- Approval status

### Lecturer Data (5 items)
- Syllabus codes, names
- Status (published/in_review/draft)
- Faculty assignments
- Last update dates

### Admin Data
- 6 user records
- 5 activity logs
- 6 role statistics
- System metrics

### Academic Affairs Data
- 5 syllabi with statuses
- 3 PLO records
- 4 faculty progress records
- 4 course records

### Principal Data
- 7 syllabi (mixed statuses)
- 4 faculty breakdown
- Real-time statistics

---

## 💡 Troubleshooting

**Q: Dashboard shows "Loading..."?**
A: This means the page is still trying to fetch from API. Check:
1. Backend server must be running (port 8000)
2. Check browser console for errors (F12 → Console)
3. Mock data function should be called automatically

**Q: No data displayed?**
A: Check:
1. Open browser console (F12)
2. Look for JavaScript errors
3. Verify mock data objects exist in page source
4. Check HTML structure matches expected element IDs

**Q: Stats show 0?**
A: This means:
1. Mock data isn't being loaded
2. Try refreshing page (Ctrl+F5)
3. Check that loadDashboardData() is being called
4. Look for console errors

**Q: Buttons don't work?**
A: This is normal - demo buttons show alerts:
1. Approve button → Shows alert "Approved!"
2. Reject button → Shows alert "Rejected!"
3. These are for demo purposes

---

## 📝 Notes

- All data is **mock/demo data** for testing
- No real data is being modified
- Perfect for testing UI before API integration
- Easy to replace mock data with real API calls
- All dashboards are **fully responsive**
- Works on **all modern browsers**

---

**Status**: ✅ **ALL DASHBOARDS HAVE LIVE MOCK DATA**

Ready to test! Open any dashboard link above and see the data immediately! 🎉
