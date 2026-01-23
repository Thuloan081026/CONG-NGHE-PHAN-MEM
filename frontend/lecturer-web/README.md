# Lecturer Web - Lecturer Portal

## 📂 Cấu trúc folder

```
lecturer-web/
├── src/
│   ├── pages/
│   │   ├── auth/              # Login
│   │   ├── syllabus/          # Syllabus management (5 pages)
│   │   └── collaboration/     # Collaborative review (2 pages)
│   ├── components/            # Reusable components
│   ├── services/              # API services
│   └── styles/
├── public/
└── package.json
```

## 📄 Pages cần phát triển (10 trang)

### Authentication & Dashboard
1. `pages/auth/Login.jsx` - Đăng nhập giảng viên
2. `pages/Dashboard.jsx` - Tổng quan syllabus

### Syllabus Management (5 trang)
3. `pages/syllabus/CreateSyllabus.jsx` - Tạo syllabus (multi-step)
4. `pages/syllabus/EditSyllabus.jsx` - Chỉnh sửa
5. `pages/syllabus/MySyllabusList.jsx` - Danh sách của tôi
6. `pages/syllabus/VersionHistory.jsx` - Lịch sử version
7. `pages/syllabus/SyllabusDetail.jsx` - Xem chi tiết

### Collaboration (2 trang)
8. `pages/collaboration/CollaborativeReview.jsx` - Review
9. `pages/collaboration/CommentsManager.jsx` - Quản lý feedback

### Search
10. `pages/SearchReference.jsx` - Tìm kiếm tham khảo
