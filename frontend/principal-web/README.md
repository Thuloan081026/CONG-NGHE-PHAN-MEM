# 🎓 Principal Dashboard - SMD System

## Tổng quan

Đây là giao diện Quản lý cho vai trò **Principal (Rector)** trong hệ thống **Syllabus Management & Development (SMD)**.

Principal có quyền:
- ✅ Phê duyệt cuối cùng (Final Approval) các đề cương
- ✅ Yêu cầu chỉnh sửa (Request Revision)
- ✅ Xem báo cáo chiến lược (Strategic Reports)
- ✅ Theo dõi KPI và Audit Log

---

## 📂 Cấu trúc thư mục

```
principal-web/
├── public/
│   └── index.html          # Entry point
├── src/
│   ├── pages/              # Trang chính
│   │   ├── ApprovalsPage.jsx      # Phê duyệt đề cương
│   │   ├── OverviewPage.jsx       # Dashboard tổng quan
│   │   └── ReportsPage.jsx        # Báo cáo chiến lược
│   │
│   ├── components/         # React components
│   │   ├── approvals/      # Phê duyệt
│   │   ├── reports/        # Báo cáo
│   │   ├── dashboard/      # Dashboard
│   │   └── common/         # Chung
│   │
│   ├── services/
│   │   └── api.service.js  # API calls
│   │
│   ├── constants/
│   │   └── config.js       # Cấu hình
│   │
│   ├── App.jsx             # Main app
│   └── index.js            # Bootstrap
│
├── package.json
├── vite.config.js
├── tailwind.config.js
└── PRINCIPAL_SRS.md        # Requirements Spec
```

---

## 🚀 Các tính năng chính

### 1️⃣ Final Strategic Approval (Phê duyệt cuối cùng)

**Luồng công việc:**
1. Principal xem danh sách đề cương chờ duyệt
2. Click "Chi tiết" để xem AI Summary, Semantic Diff, CLO-PLO Mapping
3. Click "Xem xét" để mở ApprovalModal
4. Chọn một trong 3 quyết định:
   - **✅ Phê duyệt (Approve)** - Đề cương công bố
   - **📝 Yêu cầu chỉnh sửa (Request Revision)** - Trả về HOD
   - **❌ Từ chối (Reject)** - Từ chối toàn bộ

**Thành phần:**
- `ApprovalsPage` - Quản lý trang phê duyệt
- `ApprovalList` - Danh sách đề cương
- `SyllabusCard` - Thẻ từng đề cương
- `ApprovalModal` - Modal phê duyệt
- `SyllabusDetailPanel` - Chi tiết đề cương

### 2️⃣ Strategic Overview (Tổng quan chiến lược)

**Dashboard:**
- 📊 Tổng số đề cương
- ⏳ Đề cương chờ duyệt
- ✅ Đề cương phê duyệt tháng này
- 📈 Hoạt động gần đây
- 🏥 Trạng thái hệ thống

**Thành phần:**
- `OverviewPage` - Trang tổng quan
- `StatsGrid` - Thống kê
- `SystemStatus` - Trạng thái hệ thống
- `RecentActivities` - Hoạt động gần đây

### 3️⃣ Strategic Reports (Báo cáo chiến lược)

Có 5 loại báo cáo:

#### 📚 CLO-PLO Mapping Report
- Tỷ lệ mapping hoàn thành theo khoa
- Danh sách học phần chưa mapping
- Status: Complete ✅ / Warning ⚠️ / Danger ❌

#### ⚡ Impact Analysis Report
- Phân tích ảnh hưởng của thay đổi
- Mức độ: Low 🟢 / Medium 🟡 / High 🔴
- Sinh viên bị ảnh hưởng
- Rủi ro & khuyến nghị

#### 📋 Curriculum Coverage Report
- Coverage % của mỗi PLO
- Số lượng PLO theo chương trình
- Xác định PLO cần cải thiện

#### 📈 Audit & KPI Report
- Thời gian xử lý trung bình
- Tỷ lệ phê duyệt / yêu cầu chỉnh sửa
- Audit log (ngày, hành động, người)
- Trend chart

#### 🎯 Overview Report
- Báo cáo hàng tháng
- Thống kê theo khoa

### 4️⃣ AI Decision Support (Hỗ trợ quyết định bằng AI)

Trong ApprovalModal, Principal có quyền xem:

#### 🤖 AI Summary Tab
```
- Chất lượng nội dung (Excellent/Good/Fair/Poor)
- Điểm nổi bật (5 items)
- Rủi ro tiềm ẩn (3 items)
- Khuyến nghị (3 items)
```

#### 🔀 Semantic Diff Tab
```
- Nội dung thêm mới (➕)
- Nội dung sửa đổi (🔄)
- Nội dung bị xóa (➖)
```

#### 🎯 CLO-PLO Mapping Tab
```
- Danh sách CLO
- Mapping tương ứng PLO
- Tỷ lệ coverage (%)
- Status validation (✓/⚠/✗)
```

#### 📋 Chi tiết Tab
```
- Mục tiêu môn học
- Nội dung chính
- Phương pháp đánh giá
- Tiên quyết
```

---

## 🔌 API Service Methods

### Approval Actions
```javascript
approveSyllabus(syllabusId, comment)
requestRevision(syllabusId, reason)
rejectSyllabus(syllabusId, reason)
```

### Data Retrieval
```javascript
getPendingApprovals()          // Danh sách chờ duyệt
getSystemOverview()            // Tổng quan dashboard
getRecentActivities()          // Hoạt động gần đây
getSyllabusDetail(syllabusId)  // Chi tiết đề cương
```

### Reports
```javascript
getCLOPLOMappingReport()       // Báo cáo CLO-PLO
getImpactAnalysisReport()      // Báo cáo ảnh hưởng
getCurriculumCoverageReport()  // Báo cáo coverage
getAuditKPIReport(timeRange)   // Báo cáo KPI & Audit
exportReport(type, params)     // Xuất báo cáo
```

---

## 📖 Hướng dẫn sử dụng

### Bước 1: Xem Dashboard
```
OverviewPage
├── Stats (Total, Pending, Approved, etc.)
├── System Status
└── Recent Activities
```

### Bước 2: Phê duyệt Đề cương
```
ApprovalsPage
└── Chọn Syllabus
    ├── Click "Chi tiết" → View SyllabusDetailPanel
    └── Click "Xem xét" → Open ApprovalModal
        ├── View AI Summary, Diff, Mapping, Details
        └── Make Decision: Approve / Request Revision / Cancel
```

### Bước 3: Xem Báo cáo
```
ReportsPage
├── Overview Tab (Monthly + Faculty Stats)
├── CLO-PLO Mapping Tab
├── Impact Analysis Tab
├── Curriculum Coverage Tab
└── Audit & KPI Tab
```

---

## 🛠️ Cài đặt & Chạy

### Cài đặt dependencies
```bash
cd principal-web
npm install
```

### Chạy development server
```bash
npm run dev
```

### Build production
```bash
npm run build
```

---

## 📝 Mock Data

Hiện tại, hệ thống sử dụng **mock data** từ `api.service.js`.

### Để kết nối Backend thực:

1. **Cấu hình BaseURL** trong `src/services/api.service.js`:
```javascript
baseURL: 'http://localhost:8000/api' // Thay đổi theo backend
```

2. **Bỏ comment phần "Real API"** trong mỗi method

3. **Triển khai endpoints** trên Backend:
```
POST /api/approvals/{id}/approve
POST /api/approvals/{id}/request-revision
POST /api/approvals/{id}/reject
GET /api/approvals/pending
GET /api/system/overview
GET /api/activities/recent
GET /api/syllabus/{id}
GET /api/reports/clo-plo-mapping
GET /api/reports/impact-analysis
GET /api/reports/curriculum-coverage
GET /api/reports/audit-kpi
POST /api/reports/export
```

---

## 🎨 Styling

Sử dụng **Tailwind CSS** cho styling.

### Màu sắc chính:
- Primary: Indigo (`from-indigo-600 to-purple-600`)
- Success: Green (`text-green-600`)
- Warning: Yellow (`text-yellow-600`)
- Danger: Red (`text-red-600`)
- Info: Blue (`text-blue-600`)

### Responsive Breakpoints:
- Mobile: `max-w-full`
- Tablet: `md:` (768px)
- Desktop: `lg:` (1024px)

---

## 📊 Component Hierarchy

```
App
├── Header
├── NavigationTabs
└── Page Content
    ├── OverviewPage
    │   ├── StatsGrid
    │   ├── SystemStatus
    │   └── RecentActivities
    │
    ├── ApprovalsPage
    │   ├── ApprovalList
    │   │   └── SyllabusCard (×3)
    │   ├── SyllabusDetailPanel (conditional)
    │   └── ApprovalModal (conditional)
    │
    └── ReportsPage
        ├── Report Tabs
        ├── CLOPLOMappingReport
        ├── ImpactAnalysisReport
        ├── CurriculumCoverageReport
        └── AuditKPIReport
```

---

## ⚙️ Configuration

### `src/constants/config.js`
```javascript
export const PRIORITY_LABELS = {
  high: 'Cao',
  medium: 'Trung bình',
  low: 'Thấp'
};

export const PRIORITY_COLORS = {
  high: 'bg-red-100 text-red-800',
  medium: 'bg-yellow-100 text-yellow-800',
  low: 'bg-green-100 text-green-800'
};
```

---

## 🐛 Troubleshooting

### API errors
- Kiểm tra `baseURL` trong `api.service.js`
- Đảm bảo backend đang chạy
- Kiểm tra network tab trong DevTools

### Component không load
- Clear browser cache
- Restart development server
- Kiểm tra console errors

### Styling issues
- Rebuild Tailwind CSS: `npm run build:css`
- Kiểm tra `tailwind.config.js`

---

## 📚 Tài liệu tham khảo

- [PRINCIPAL_SRS.md](./PRINCIPAL_SRS.md) - Yêu cầu chi tiết
- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Lucide Icons](https://lucide.dev)

---

## ✅ Checklist triển khai

- [x] Frontend components
- [x] UI/UX design
- [x] Mock API service
- [x] Routing & Navigation
- [ ] Backend integration
- [ ] Authentication
- [ ] Error handling
- [ ] Loading states
- [ ] Testing

---

**Phiên bản:** 1.0  
**Cập nhật lần cuối:** 2025-01-28  
**Trạng thái:** ✅ Ready for Backend Integration
