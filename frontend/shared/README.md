# Shared - Common Components & Utilities

## 📂 Cấu trúc folder

```
shared/
├── components/                # Reusable UI components
│   ├── layout/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Footer.jsx
│   │   └── MainLayout.jsx
│   ├── forms/
│   │   ├── Input.jsx
│   │   ├── Select.jsx
│   │   ├── DatePicker.jsx
│   │   └── FormBuilder.jsx
│   ├── tables/
│   │   ├── DataTable.jsx
│   │   └── SortableTable.jsx
│   └── ui/
│       ├── Button.jsx
│       ├── Modal.jsx
│       ├── Notification.jsx
│       └── Loading.jsx
├── services/                  # API services
│   ├── apiClient.js           # Axios config
│   ├── authService.js
│   ├── syllabusService.js
│   └── notificationService.js
├── hooks/                     # Custom React hooks
│   ├── useAuth.js
│   ├── useNotification.js
│   └── useSyllabus.js
├── utils/                     # Helper functions
│   ├── formatters.js
│   ├── validators.js
│   └── storage.js
├── constants/                 # App constants
│   ├── api.js
│   ├── roles.js
│   └── statuses.js
└── types/                     # TypeScript types
    ├── user.ts
    ├── syllabus.ts
    └── workflow.ts
```

## 🔧 Common Components

### Layout Components
- Header (navigation, user menu)
- Sidebar (navigation menu)
- Footer
- MainLayout (wrapper)

### Form Components
- Input, Select, DatePicker
- FormBuilder (dynamic forms)
- Validation helpers

### Table Components
- DataTable (pagination, filtering)
- SortableTable

### UI Components
- Button (variants)
- Modal
- Notification/Toast
- Loading spinner

## 🌐 API Services

### authService.js
- login(), logout()
- refreshToken()
- getCurrentUser()

### syllabusService.js
- getSyllabusList()
- getSyllabusDetail()
- createSyllabus()
- updateSyllabus()

### notificationService.js
- getNotifications()
- markAsRead()
- subscribe()

## 🪝 Custom Hooks

### useAuth
- User authentication state
- Login/logout functions
- Role checking

### useNotification
- Show notifications
- Toast messages

### useSyllabus
- Syllabus CRUD operations
- Caching logic

## 🔧 Utilities

### formatters.js
- formatDate()
- formatCurrency()
- formatStatus()

### validators.js
- validateEmail()
- validatePhone()
- validateCLO()

### storage.js
- localStorage wrapper
- sessionStorage wrapper
