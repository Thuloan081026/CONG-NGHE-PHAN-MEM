# Admin Web - System Administration Portal

## 📂 Cấu trúc folder

```
admin-web/
├── src/
│   ├── pages/
│   │   ├── auth/              # Login, forgot password
│   │   ├── users/             # User management (3 pages)
│   │   ├── settings/          # System configuration (4 pages)
│   │   ├── publishing/        # Publishing management (2 pages)
│   │   └── monitoring/        # Audit log & reports (1 page)
│   ├── components/            # Reusable components
│   ├── services/              # API services
│   ├── utils/                 # Helper functions
│   └── styles/                # CSS/SCSS files
├── public/                    # Static assets
└── package.json
```

## 📄 Pages cần phát triển (12 trang)

### Authentication
1. `pages/auth/Login.jsx` - Đăng nhập admin
2. `pages/Dashboard.jsx` - Tổng quan hệ thống

### User Management (3 trang)
3. `pages/users/UserList.jsx` - Danh sách users
4. `pages/users/UserForm.jsx` - Tạo/sửa user
5. `pages/users/RolesPermissions.jsx` - Phân quyền

### System Settings (4 trang)
6. `pages/settings/GeneralSettings.jsx` - Cấu hình chung
7. `pages/settings/CLOPLOTemplates.jsx` - Mẫu CLO/PLO
8. `pages/settings/GradingScale.jsx` - Thang điểm
9. `pages/settings/WorkflowRules.jsx` - Quy trình duyệt

### Publishing (2 trang)
10. `pages/publishing/PublishingQueue.jsx` - Queue chờ publish
11. `pages/publishing/PublishedManagement.jsx` - Quản lý đã publish

### Monitoring
12. `pages/monitoring/AuditLog.jsx` - Lịch sử & báo cáo

## 🔧 Tech Stack
- React 18 / NextJS 14
- Material-UI / Ant Design
- Redux Toolkit
- React Hook Form
- Axios
