# Academic Affairs Web - Phòng Đào Tạo Portal

## 📂 Cấu trúc folder

```
academic-affairs-web/
├── src/
│   ├── pages/
│   │   ├── approval/          # Level 2 approval (3 pages)
│   │   ├── program/           # Program management (4 pages)
│   │   └── analytics/         # Analytics (2 pages)
│   ├── components/
│   └── services/
└── public/
```

## 📄 Pages cần phát triển (11 trang)

### Dashboard
1. `pages/Dashboard.jsx` - Tổng quan toàn trường
2. `pages/auth/Login.jsx` - Đăng nhập

### Academic Approval (3 trang)
3. `pages/approval/Level2Queue.jsx` - Queue level 2
4. `pages/approval/PLOMappingReview.jsx` - Review PLO mapping
5. `pages/approval/ApprovalDecision.jsx` - Approve/Reject

### Program Management (4 trang)
6. `pages/program/ProgramManagement.jsx` - Quản lý chương trình
7. `pages/program/PLOStandards.jsx` - Thư viện PLO
8. `pages/program/ModuleRelationships.jsx` - Môn tiên quyết
9. `pages/program/CreditRubrics.jsx` - Tín chỉ & rubrics

### Analytics (2 trang)
10. `pages/analytics/UniversitySearch.jsx` - Tìm kiếm toàn trường
11. `pages/analytics/Reports.jsx` - Báo cáo phân tích
