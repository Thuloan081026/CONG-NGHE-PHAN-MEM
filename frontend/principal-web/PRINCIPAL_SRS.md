# PHÂN TÍCH YÊMARY CẦU CHỨC NĂNG - VAI TRÒ PRINCIPAL

## 1. Mục tiêu vai trò

Principal là người ra quyết định cuối cùng ở cấp chiến lược, đảm bảo:
- Syllabus phù hợp với định hướng đào tạo của nhà trường
- Các thay đổi học thuật không làm lệch chuẩn PLO & chương trình đào tạo
- Hệ thống vận hành minh bạch, có kiểm soát

## 2. Chức năng chính (Functional Requirements)

### 2.1 Final Strategic Approval (✅ IMPLEMENTED)

**Mục đích:** Principal thực hiện phê duyệt cuối cùng Syllabus / Curriculum Proposal

**Yêu cầu:**
- [x] Phê duyệt cuối cùng Syllabus / Curriculum Proposal sau khi đã qua:
  - Lecturer
  - Head of Department (HOD)
  - Academic Affairs
- [x] Quyết định: Approve / Reject / Request Revision
- [x] Phê duyệt các thay đổi mang tính:
  - Liên khoa / liên ngành
  - Ảnh hưởng đến chuẩn đầu ra (PLO)
  - Điều chỉnh lớn về nội dung, tín chỉ, mục tiêu môn học

**Đã triển khai:**
- ✅ ApprovalModal component với 3 actions: Approve, Request Revision, Reject
- ✅ ApprovalList hiển thị danh sách đề cương chờ phê duyệt
- ✅ ApprovalsPage để manage approval workflow
- ✅ API Service methods: approveSyllabus(), requestRevision(), rejectSyllabus()

**Chi tiết:**
```
ApprovalsPage
├── ApprovalList (danh sách đề cương)
│   └── SyllabusCard (từng đề cương)
├── ApprovalModal (phê duyệt/từ chối/request revision)
└── SyllabusDetailPanel (xem chi tiết)
```

---

### 2.2 Strategic Overview & Monitoring (✅ IMPLEMENTED)

**Mục đích:** Principal có quyền xem – không chỉnh sửa các dữ liệu chiến lược

**Yêu cầu:**
- [x] Dashboard tổng quan:
  - Trạng thái duyệt syllabus toàn trường
  - Tỷ lệ phê duyệt / bị trả về
- [x] Báo cáo chiến lược:
  - CLO–PLO Mapping Report
  - Impact Analysis Report
  - Curriculum Coverage Report
- [x] Audit & KPI:
  - Thời gian xử lý trung bình
  - Hiệu suất hệ thống
  - Log hoạt động duyệt

**Đã triển khai:**
- ✅ OverviewPage - hiển thị dashboard tổng quan
- ✅ ReportsPage với tabs:
  - CLOPLOMappingReport
  - ImpactAnalysisReport
  - CurriculumCoverageReport
  - AuditKPIReport
- ✅ API Service methods: getCLOPLOMappingReport(), getImpactAnalysisReport(), getCurriculumCoverageReport(), getAuditKPIReport()

**Chi tiết các Report:**

#### 2.2.1 CLO-PLO Mapping Report
- Hiển thị tỷ lệ CLO-PLO mapping hoàn thành theo từng khoa
- Liệt kê các học phần chưa được mapping hoàn chỉnh
- Status indicators (Complete, Warning, Danger)

#### 2.2.2 Impact Analysis Report
- Phân tích ảnh hưởng của các thay đổi syllabus
- Mức độ ảnh hưởng (Low, Medium, High)
- Số lượng sinh viên bị ảnh hưởng
- Danh sách rủi ro tiềm ẩn
- Khuyến nghị xử lý

#### 2.2.3 Curriculum Coverage Report
- Cho từng chương trình (Program)
- Hiển thị % coverage của mỗi PLO
- Xác định PLO nào cần cải thiện
- Liệt kê các học phần contribute vào mỗi PLO

#### 2.2.4 Audit & KPI Report
- KPI Metrics:
  - Thời gian xử lý trung bình (ngày)
  - Tỷ lệ phê duyệt (%)
  - Tỷ lệ yêu cầu chỉnh sửa (%)
  - Tổng đề cương xử lý
- Audit Log với filters theo thời gian
- Trend chart cho thấy xu hướng

---

### 2.3 AI Decision Support (✅ IMPLEMENTED)

**Mục đích:** Hỗ trợ Principal quyết định dựa trên phân tích AI

**Yêu cầu:**
- [x] AI Summary nội dung syllabus
  - Chất lượng nội dung
  - Ảnh hưởng học thuật
  - Khuyến nghị
- [x] Semantic Diff (AI so sánh phiên bản cũ – mới)
  - Thêm mới
  - Sửa đổi
  - Xóa
- [x] CLO–PLO logic checking
  - Tất cả CLO được map với PLO
  - Không có CLO orphan
  - Coverage phù hợp
- [x] Subject Relationship Tree

**Đã triển khai:**
- ✅ ApprovalModal với tabs:
  - AI Summary (nội dung, highlight, risks, recommendations)
  - Semantic Diff (Added, Modified, Removed)
  - CLO-PLO Mapping (visualization)
  - Chi tiết (Course Info, Assessment, Prerequisites)
- ✅ SyllabusDetailPanel component
- ✅ Integrated AI data display

**Chi tiết AI Features:**

#### Tab: AI Summary
```
Nội dung:
- Quality Assessment (Excellent/Good/Fair/Poor)
- Highlights (Tối đa 5 điểm)
- Risks (Tối đa 3 rủi ro)
- Recommendations (Tối đa 3 khuyến nghị)
```

#### Tab: Semantic Diff
```
So sánh giữa:
- Phiên bản hiện tại
- Phiên bản mới
Hiển thị:
- ➕ Nội dung thêm mới
- 🔄 Nội dung được sửa
- ➖ Nội dung bị xóa
```

#### Tab: CLO-PLO Mapping
```
Hiển thị:
- Danh sách CLO
- Mapping tương ứng với PLO
- Tỷ lệ coverage (%)
- Status validation (✓ Complete, ⚠ Partial, ✗ Missing)
```

---

## 3. Use Case Diagram

### Use Case: Final Approval of Syllabus

**Actor:** Principal

**Pre-condition:**
- Syllabus đã được Lecturer, HOD & Academic Affairs phê duyệt
- Principal đã đăng nhập vào hệ thống

**Main Flow:**
1. Principal đăng nhập hệ thống
2. Xem danh sách syllabus chờ phê duyệt cuối (ApprovalsPage)
3. Chọn một syllabus để xem chi tiết (click "Chi tiết" → SyllabusDetailPanel)
4. Xem AI Summary, Semantic Diff, CLO-PLO Mapping
5. Click nút "Xem xét" → ApprovalModal mở ra
6. Lựa chọn một trong 3 quyết định:
   - **Approve:** Ghi comment (tùy chọn) → Submit
   - **Request Revision:** Ghi lý do chỉnh sửa → Submit
   - **Reject:** Xem như Request Revision
7. Hệ thống gửi thông báo đến Reviewer/Lecturer
8. Cập nhật status syllabus trong database
9. Log audit tự động được ghi

**Alternative Flow:**
- Nếu Principal muốn hủy: Click "Hủy" → Quay về danh sách

**Post-condition:**
- Syllabus được công bố (nếu Approve)
- Syllabus trả về cho người duyệt (nếu Request Revision/Reject)
- Status được cập nhật trong database

---

## 4. Cấu trúc File đã triển khai

```
frontend/principal-web/
├── src/
│   ├── pages/
│   │   ├── ApprovalsPage.jsx ✅ Final Approval & Management
│   │   ├── OverviewPage.jsx ✅ Dashboard
│   │   └── ReportsPage.jsx ✅ Strategic Reports
│   │
│   ├── components/
│   │   ├── approvals/
│   │   │   ├── ApprovalModal.jsx ✅ (Approve/Reject/Request Revision)
│   │   │   ├── ApprovalList.jsx ✅
│   │   │   ├── SyllabusCard.jsx ✅
│   │   │   └── SyllabusDetailPanel.jsx ✅ (AI Summary, Diff, Mapping)
│   │   │
│   │   ├── reports/
│   │   │   ├── CLOPLOMappingReport.jsx ✅
│   │   │   ├── ImpactAnalysisReport.jsx ✅
│   │   │   ├── CurriculumCoverageReport.jsx ✅
│   │   │   ├── AuditKPIReport.jsx ✅
│   │   │   ├── MonthlyReport.jsx (existing)
│   │   │   └── FacultyStats.jsx (existing)
│   │   │
│   │   ├── dashboard/
│   │   │   ├── StatsGrid.jsx
│   │   │   ├── SystemStatus.jsx
│   │   │   └── RecentActivities.jsx
│   │   │
│   │   └── common/
│   │       ├── Header.jsx
│   │       ├── NavigationTabs.jsx
│   │       └── StatCard.jsx
│   │
│   ├── services/
│   │   └── api.service.js ✅ (Tất cả API methods)
│   │
│   └── constants/
│       └── config.js
```

---

## 5. Chức năng đã hoàn thành

### ✅ Functional Requirements Checklist

| # | Tính năng | Status | Component | API |
|---|----------|--------|-----------|-----|
| 1 | Phê duyệt (Approve) | ✅ | ApprovalModal | approveSyllabus() |
| 2 | Yêu cầu chỉnh sửa (Request Revision) | ✅ | ApprovalModal | requestRevision() |
| 3 | Từ chối (Reject) | ✅ | ApprovalModal | rejectSyllabus() |
| 4 | Xem danh sách chờ duyệt | ✅ | ApprovalList | getPendingApprovals() |
| 5 | Xem chi tiết đề cương | ✅ | SyllabusDetailPanel | getSyllabusDetail() |
| 6 | AI Summary | ✅ | ApprovalModal (Tab) | - |
| 7 | Semantic Diff | ✅ | ApprovalModal (Tab) | - |
| 8 | CLO-PLO Mapping | ✅ | SyllabusDetailPanel (Tab) | - |
| 9 | Xem tổng quan (Dashboard) | ✅ | OverviewPage | getSystemOverview() |
| 10 | CLO-PLO Mapping Report | ✅ | CLOPLOMappingReport | getCLOPLOMappingReport() |
| 11 | Impact Analysis Report | ✅ | ImpactAnalysisReport | getImpactAnalysisReport() |
| 12 | Curriculum Coverage Report | ✅ | CurriculumCoverageReport | getCurriculumCoverageReport() |
| 13 | Audit & KPI Report | ✅ | AuditKPIReport | getAuditKPIReport() |
| 14 | Log hoạt động (Audit Log) | ✅ | AuditKPIReport | - |
| 15 | Xuất báo cáo PDF | ✅ | Various | exportReport() |

---

## 6. Luồng làm việc (Workflow)

```
┌─────────────────────────────────────────────────────┐
│            PRINCIPAL APPROVAL WORKFLOW              │
└─────────────────────────────────────────────────────┘

STEP 1: Dashboard View
┌───────────────────────────────────┐
│   OverviewPage (Dashboard)        │
│   - Total syllabi                 │
│   - Pending approvals             │
│   - Recent activities             │
│   - KPIs                          │
└───────────────────────────────────┘
         ↓
STEP 2: View Pending List
┌───────────────────────────────────┐
│   ApprovalsPage / ApprovalList   │
│   - 3 pending syllabi            │
│   - Priority badges              │
│   - Quick info                   │
└───────────────────────────────────┘
         ↓
STEP 3: View Detail (Optional)
┌───────────────────────────────────┐
│   SyllabusDetailPanel            │
│   - AI Summary                   │
│   - Semantic Diff                │
│   - CLO-PLO Mapping             │
│   - Course Details               │
└───────────────────────────────────┘
         ↓
STEP 4: Make Decision
┌───────────────────────────────────┐
│   ApprovalModal                  │
│   ├─ AI Summary Tab             │
│   ├─ Semantic Diff Tab          │
│   ├─ CLO-PLO Mapping Tab       │
│   ├─ Details Tab                │
│   └─ Action Buttons:            │
│      - Approve                  │
│      - Request Revision         │
│      - Cancel                   │
└───────────────────────────────────┘
         ↓
STEP 5: View Reports
┌───────────────────────────────────┐
│   ReportsPage (Multi-tab)        │
│   ├─ Overview                    │
│   ├─ CLO-PLO Mapping Report     │
│   ├─ Impact Analysis Report     │
│   ├─ Curriculum Coverage        │
│   └─ Audit & KPI Report         │
└───────────────────────────────────┘
```

---

## 7. API Service Methods

```javascript
// Approval Actions
approveSyllabus(syllabusId, comment) → { success, message }
requestRevision(syllabusId, reason) → { success, message }
rejectSyllabus(syllabusId, reason) → { success, message }

// Data Retrieval
getPendingApprovals() → [syllabi]
getSystemOverview() → { overview data }
getRecentActivities() → [activities]
getSyllabusDetail(syllabusId) → { detail data }

// Reports
getCLOPLOMappingReport() → { mapping data }
getImpactAnalysisReport() → { impact data }
getCurriculumCoverageReport(programId) → { coverage data }
getAuditKPIReport(timeRange) → { kpi data }
exportReport(type, params) → { downloadUrl }
```

---

## 8. Mock Data (Tạm thời - cần kết nối Backend)

Hiện tại, tất cả API methods trong `api.service.js` sử dụng mock data với `await Promise.setTimeout()`.

**Để kết nối Backend thực:**
1. Bỏ comment phần `// Real API` trong mỗi method
2. Cấu hình `baseURL` trong APIService
3. Triển khai các endpoint tương ứng trên Backend

---

## 9. Thông tin bổ sung

### UI/UX Components sử dụng
- Lucide Icons (Eye, CheckCircle, XCircle, AlertCircle, Zap, GitCompare, BookOpen, Download, etc.)
- Tailwind CSS cho styling
- React Hooks (useState, useEffect) cho state management

### Responsive Design
- Mobile: 1 cột
- Tablet: 2-3 cột
- Desktop: Full multi-column layout

### Accessibility
- ARIA labels (tương đối)
- Keyboard navigation support
- Color contrast thoả mãn WCAG

---

## 10. Trang tiếp theo / Future Enhancements

- [ ] Integration với Backend APIs
- [ ] Real-time notifications
- [ ] Advanced filtering & search
- [ ] Bulk actions
- [ ] Custom report generation
- [ ] Email notifications
- [ ] Calendar view for deadlines
- [ ] Comparison view (side-by-side syllabi)
- [ ] History tracking & versioning

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-28  
**Status:** ✅ IMPLEMENTATION COMPLETE (Frontend)
