# HoD Web - Head of Department Portal

## 📂 Cấu trúc folder

```
hod-web/
├── src/
│   ├── pages/
│   │   ├── review/            # Review & approval (4 pages)
│   │   ├── collaboration/     # Collaboration management (2 pages)
│   │   └── analysis/          # Lookup & analysis (1 page)
│   ├── components/
│   ├── services/
│   └── styles/
└── public/
```

## 📄 Pages cần phát triển (9 trang)

### Dashboard
1. `pages/Dashboard.jsx` - Tổng quan công việc
2. `pages/auth/Login.jsx` - Đăng nhập

### Review & Approval (4 trang)
3. `pages/review/ReviewQueue.jsx` - Queue chờ duyệt
4. `pages/review/ReviewDetail.jsx` - Review chi tiết (AI tools)
5. `pages/review/ApprovalDecision.jsx` - Approve/Reject
6. `pages/review/ApprovedHistory.jsx` - Lịch sử đã duyệt

### Collaboration Management (2 trang)
7. `pages/collaboration/Dashboard.jsx` - Quản lý collaborative review
8. `pages/collaboration/FeedbackCompilation.jsx` - Tổng hợp feedback

### Analysis
9. `pages/analysis/DepartmentSearch.jsx` - Tìm kiếm & so sánh
