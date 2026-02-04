# Frontend Structure Overview

## 📁 Cấu trúc tổng quan

```
frontend/
├── admin-web/              # System Admin Portal (12 trang)
├── lecturer-web/           # Lecturer Portal (10 trang)
├── hod-web/               # Head of Department (9 trang)
├── academic-affairs-web/  # Academic Affairs (11 trang)
├── principal-web/         # Principal/Rector (6 trang)
├── student-web/           # Student Web Portal (8 trang)
├── student-mobile/        # Student Mobile App (6 screens)
└── shared/                # Common components & utilities
```

## 📊 Tổng kết

- **Tổng Web Apps:** 7 modules (56 trang)
- **Mobile App:** 1 app (6 screens)
- **Shared Components:** 1 library

## 🚀 Thứ tự phát triển đề xuất

### Phase 1 (Core - 3 tháng)
1. **shared/** - Common components trước
2. **admin-web/** - System admin cơ bản
3. **lecturer-web/** - Tạo/quản lý syllabus
4. **student-web/** - Xem/tìm kiếm syllabus

### Phase 2 (Review Workflow - 2 tháng)
5. **hod-web/** - Review level 1
6. **academic-affairs-web/** - Review level 2

### Phase 3 (Advanced - 2 tháng)
7. **principal-web/** - Strategic approval
8. **student-mobile/** - Mobile app

## 🔧 Tech Stack

### Web Apps
- **Framework:** React 18 / NextJS 14
- **UI Library:** Material-UI / Ant Design
- **State:** Redux Toolkit
- **Forms:** React Hook Form
- **HTTP:** Axios
- **Build:** Vite / Webpack

### Mobile App
- **Framework:** React Native 0.72+
- **Navigation:** React Navigation 6
- **UI:** React Native Paper
- **State:** Redux Toolkit

## 📦 Package Scripts

Mỗi module sẽ có:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "test": "jest"
  }
}
```

## 🌐 API Integration

Tất cả modules sử dụng:
- Base API URL: `http://127.0.0.1:8000`
- Authentication: JWT Bearer token
- Error handling: Global interceptors
- Loading states: Global state management

## 📱 Responsive Design

- **Desktop:** 1366x768+ (primary)
- **Tablet:** 768x1024
- **Mobile:** 360x640+
