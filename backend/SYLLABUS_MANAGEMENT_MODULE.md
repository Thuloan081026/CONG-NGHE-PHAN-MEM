# MODULE 2: QUẢN LÝ GIÁO TRÌNH (SYLLABUS MANAGEMENT)

## 📋 Tổng Quan

Module 2 cung cấp hệ thống quản lý giáo trình toàn diện với các tính năng:

- ✅ **CRUD Giáo trình**: Tạo, đọc, cập nhật, xóa giáo trình
- ✅ **Phiên bản & Lịch sử**: Tự động theo dõi mỗi thay đổi, có thể rollback
- ✅ **Metadata Giáo trình**: CLO, PLO, tiên quyệt, yêu cầu song song
- ✅ **Quy trình Phê duyệt**: Draft → Submitted → Under Review → Approved → Published
- ✅ **So sánh Phiên bản**: Xem các khác biệt giữa hai phiên bản
- ✅ **Phân quyền Người dùng**: Lecturer (chỉnh sửa riêng), HOD/Admin (quản lý tất cả)

---

## 🗄️ CẤU TRÚC CỞ SỞ DỮ LIỆU

### Bảng `syllabuses` (Giáo trình)

Lưu trữ thông tin cơ bản của giáo trình.

```
┌─────────────────────────────────────┐
│          syllabuses                 │
├─────────────────────────────────────┤
│ id (PRIMARY KEY)                    │
│ subject_code (UNIQUE)               │ Mã môn (ví dụ: CS101, CS102)
│ subject_name                        │ Tên môn học
│ description                         │ Mô tả ngắn
│ credits                             │ Số tín chỉ
│ semester                            │ Kỳ học (1, 2, 3...)
│ department                          │ Bộ môn
│ academic_year                       │ Năm học (2025-2026)
│                                     │
│ objectives (TEXT)                   │ Mục tiêu học tập
│ content (TEXT)                      │ Nội dung giáo trình
│ teaching_methods (TEXT)             │ Phương pháp giảng dạy
│ assessment_methods (TEXT)           │ Phương pháp đánh giá
│                                     │
│ prerequisites (JSON)                │ Các môn tiên quyệt
│ corequisites (JSON)                 │ Các môn học song song
│ related_subjects (JSON)             │ Các môn liên quan
│                                     │
│ clos (JSON)                         │ Course Learning Outcomes
│ plos (JSON)                         │ Program Learning Outcomes
│ clo_plo_mapping (JSON)              │ Ánh xạ CLO → PLO
│                                     │
│ assessment_weights (JSON)           │ Trọng số đánh giá
│ textbooks (JSON)                    │ Sách giáo khoa
│ references (JSON)                   │ Tài liệu tham khảo
│ learning_materials (JSON)           │ Tài liệu học tập
│                                     │
│ created_by (FK → users.id)          │ Người tạo (Lecturer)
│ status                              │ draft|submitted|under_review|...
│ is_published                        │ Đã xuất bản?
│ created_at (TIMESTAMP)              │
│ updated_at (TIMESTAMP)              │
│ published_at (TIMESTAMP)            │
└─────────────────────────────────────┘
```

### Bảng `syllabus_versions` (Phiên bản Giáo trình)

Theo dõi từng thay đổi, cho phép rollback và xem lịch sử.

```
┌──────────────────────────────────────┐
│      syllabus_versions               │
├──────────────────────────────────────┤
│ id (PRIMARY KEY)                     │
│ syllabus_id (FK → syllabuses.id)     │
│ version_number                       │ 1, 2, 3, ...
│ change_summary                       │ "Updated CLO mappings"
│ change_description (TEXT)            │ Chi tiết thay đổi
│                                      │
│ subject_code                         │ Snapshot của mã môn
│ subject_name                         │ Snapshot của tên môn
│ content (TEXT)                       │ Snapshot của nội dung
│                                      │
│ changed_fields (JSON)                │ ["content", "clos"]
│ previous_values (JSON)               │ {"content": "old value"}
│ new_values (JSON)                    │ {"content": "new value"}
│                                      │
│ version_status                       │ saved|submitted|review|approved
│ created_by (FK → users.id)           │ Ai tạo phiên bản này?
│ created_at (TIMESTAMP)               │
└──────────────────────────────────────┘
```

---

## 📡 API ENDPOINTS

### 1️⃣ CRUD GIÁO TRÌNH

#### **POST /api/v1/syllabus** - Tạo giáo trình mới
```bash
curl -X POST "http://localhost:8000/api/v1/syllabus" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_code": "CS101",
    "subject_name": "Lập trình Python",
    "credits": 3,
    "semester": 1,
    "department": "Khoa CNTT",
    "academic_year": "2025-2026",
    "objectives": "Dạy học lập trình Python cơ bản",
    "content": "Variables, Functions, Classes, ...",
    "teaching_methods": "Lectures and Labs",
    "assessment_methods": "Exams and Projects"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "subject_name": "Lập trình Python",
  "credits": 3,
  "semester": 1,
  "department": "Khoa CNTT",
  "academic_year": "2025-2026",
  "status": "draft",
  "is_published": false,
  "created_by": 2,
  "created_at": "2025-01-10T10:30:00",
  "updated_at": "2025-01-10T10:30:00",
  "published_at": null
}
```

---

#### **GET /api/v1/syllabus** - Lấy danh sách giáo trình của tôi
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus?skip=0&limit=10&semester=1&status=draft" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:**
```json
{
  "total": 5,
  "count": 5,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "subject_code": "CS101",
      "subject_name": "Lập trình Python",
      "credits": 3,
      "status": "draft",
      "is_published": false,
      "created_at": "2025-01-10T10:30:00",
      ...
    }
  ]
}
```

---

#### **GET /api/v1/syllabus/{syllabus_id}** - Lấy chi tiết giáo trình
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/1" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "subject_name": "Lập trình Python",
  "objectives": "...",
  "content": "...",
  "clos": [
    {"id": "CLO1", "description": "Understand basics of Python", "level": "K2"},
    {"id": "CLO2", "description": "Write simple programs", "level": "K3"}
  ],
  "plos": [
    {"id": "PLO1", "description": "Programming skills"},
    {"id": "PLO2", "description": "Problem solving"}
  ],
  "clo_plo_mapping": {
    "CLO1": ["PLO1"],
    "CLO2": ["PLO1", "PLO2"]
  },
  "versions": [
    {
      "id": 1,
      "version_number": 1,
      "change_summary": "Initial creation",
      "created_at": "2025-01-10T10:30:00"
    }
  ],
  ...
}
```

---

#### **PUT /api/v1/syllabus/{syllabus_id}** - Cập nhật giáo trình
```bash
curl -X PUT "http://localhost:8000/api/v1/syllabus/1" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "objectives": "Updated objectives",
    "change_summary": "Fixed typos in objectives"
  }'
```

**Tính năng:**
- Tự động phát hiện các trường thay đổi
- Tạo version mới với lịch sử thay đổi
- Lưu giá trị cũ để có thể rollback sau

**Response:**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "subject_name": "Lập trình Python",
  "objectives": "Updated objectives",
  "status": "draft",
  ...
}
```

---

#### **DELETE /api/v1/syllabus/{syllabus_id}** - Xóa giáo trình
```bash
curl -X DELETE "http://localhost:8000/api/v1/syllabus/1" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:** `204 No Content`

---

### 2️⃣ QUẢN LÝ PHIÊN BẢN

#### **GET /api/v1/syllabus/{syllabus_id}/versions** - Lịch sử phiên bản
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/1/versions?skip=0&limit=50" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:**
```json
{
  "total": 5,
  "versions": [
    {
      "id": 5,
      "version_number": 5,
      "change_summary": "Updated CLO mappings",
      "changed_fields": ["clo_plo_mapping"],
      "created_at": "2025-01-12T14:20:00",
      "created_by": 2
    },
    {
      "id": 4,
      "version_number": 4,
      "change_summary": "Fixed assessment methods",
      "changed_fields": ["assessment_methods", "assessment_weights"],
      "created_at": "2025-01-11T09:15:00",
      "created_by": 2
    },
    ...
  ]
}
```

---

#### **GET /api/v1/syllabus/{syllabus_id}/versions/latest** - Phiên bản mới nhất
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/1/versions/latest" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 5,
  "version_number": 5,
  "change_summary": "Updated CLO mappings",
  "changed_fields": ["clo_plo_mapping"],
  "previous_values": {"clo_plo_mapping": {...old mapping...}},
  "new_values": {"clo_plo_mapping": {...new mapping...}},
  "created_at": "2025-01-12T14:20:00",
  "created_by": 2
}
```

---

#### **GET /api/v1/syllabus/{syllabus_id}/versions/{version_id}/compare/{version_id_2}** - So sánh 2 phiên bản
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/1/versions/3/compare/5" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Response:**
```json
{
  "version_1": 3,
  "version_2": 5,
  "differences": {
    "changed_fields": ["clos", "clo_plo_mapping", "assessment_weights"],
    "previous_values": {
      "clos": [...old CLOs...],
      "clo_plo_mapping": {...old mapping...},
      "assessment_weights": {...old weights...}
    },
    "new_values": {
      "clos": [...new CLOs...],
      "clo_plo_mapping": {...new mapping...},
      "assessment_weights": {...new weights...}
    }
  }
}
```

---

#### **POST /api/v1/syllabus/{syllabus_id}/versions/{version_id}/rollback** - Khôi phục giáo trình
```bash
curl -X POST "http://localhost:8000/api/v1/syllabus/1/versions/3/rollback" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Tính năng:**
- Khôi phục nội dung từ phiên bản cũ (ví dụ v3)
- Tự động tạo phiên bản mới (ví dụ v6) để ghi lại rollback
- Có thể hoàn tác những thay đổi không mong muốn

**Response:**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "subject_name": "Lập trình Python",
  "status": "draft",
  ...
}
```

---

### 3️⃣ QUY TRÌNH PHÊ DUYỆT

#### **PATCH /api/v1/syllabus/{syllabus_id}/status** - Cập nhật trạng thái
```bash
curl -X PATCH "http://localhost:8000/api/v1/syllabus/1/status" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "submitted"
  }'
```

**Trạng thái hợp lệ:**
- `draft`: Bản nháp (mới tạo)
- `submitted`: Đã nộp để phê duyệt
- `under_review`: Đang được phê duyệt
- `approved`: Đã được phê duyệt
- `published`: Đã xuất bản

**Response:**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "status": "submitted",
  ...
}
```

---

#### **POST /api/v1/syllabus/{syllabus_id}/publish** - Xuất bản giáo trình
```bash
curl -X POST "http://localhost:8000/api/v1/syllabus/1/publish" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Điều kiện:**
- Giáo trình phải có status = "approved"
- Chỉ HOD/Admin có thể publish

**Response:**
```json
{
  "id": 1,
  "subject_code": "CS101",
  "status": "published",
  "is_published": true,
  "published_at": "2025-01-12T15:00:00",
  ...
}
```

---

### 4️⃣ CLO/PLO MAPPING

#### **PATCH /api/v1/syllabus/{syllabus_id}/clo-plo-mapping** - Cập nhật ánh xạ
```bash
curl -X PATCH "http://localhost:8000/api/v1/syllabus/1/clo-plo-mapping" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "clo_plo_mapping": {
      "CLO1": ["PLO1", "PLO3"],
      "CLO2": ["PLO2"],
      "CLO3": ["PLO1", "PLO2", "PLO3"]
    }
  }'
```

**Response:**
```json
{
  "id": 1,
  "clo_plo_mapping": {
    "CLO1": ["PLO1", "PLO3"],
    "CLO2": ["PLO2"],
    "CLO3": ["PLO1", "PLO2", "PLO3"]
  },
  ...
}
```

---

### 5️⃣ TÌM KIẾM VÀ CÔNG KHAI

#### **GET /api/v1/syllabus/search?q=keyword** - Tìm kiếm
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/search?q=python&skip=0&limit=10" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Tìm kiếm theo:**
- Mã môn (subject_code)
- Tên môn (subject_name)
- Mô tả (description)

**Response:**
```json
{
  "total": 2,
  "count": 2,
  "items": [
    {
      "id": 1,
      "subject_code": "CS101",
      "subject_name": "Lập trình Python",
      ...
    },
    {
      "id": 2,
      "subject_code": "CS102",
      "subject_name": "Python nâng cao",
      ...
    }
  ]
}
```

---

#### **GET /api/v1/syllabus/published** - Giáo trình công khai
```bash
curl -X GET "http://localhost:8000/api/v1/syllabus/published?semester=1&skip=0&limit=10" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

**Giáo trình:**
- Có status = "published"
- Có is_published = true
- Ai cũng có thể xem

---

## 🔐 PHÂN QUYỀN

| Role | Create | Read Own | Read All | Update Own | Update All | Delete | Approve | Publish |
|------|--------|----------|----------|-----------|-----------|--------|---------|---------|
| **Lecturer** | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **HOD** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **AA** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Student** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 💾 WORKFLOW QUY TRÌNH

```
┌─────────────────────────────────────────────────────────────┐
│                    Lecturer tạo Syllabus                    │
│                                                             │
│  POST /syllabus → status: "draft"                           │
│  (Tự động tạo version 1)                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Lecturer chỉnh sửa (PUT)       │
        │ - Cập nhật nội dung            │
        │ - Thêm CLO/PLO                 │
        │ - Tự động tạo version mới      │
        │ (version 2, 3, ...)            │
        └────────────┬───────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │ Lecturer nộp để phê duyệt              │
    │ PATCH /status → status: "submitted"    │
    └────────────┬───────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│           HOD/Admin phê duyệt                    │
│                                                  │
│  Xem lại:                                        │
│  - Nội dung giáo trình                           │
│  - Lịch sử thay đổi (versions)                   │
│  - So sánh với phiên bản trước                   │
│                                                  │
│  Chọn:                                           │
│  ✅ Phê duyệt: PATCH /status → "approved"       │
│  ❌ Từ chối: Yêu cầu chỉnh sửa                   │
└──────────────┬───────────────────────────────────┘
               │
               ▼
    ┌───────────────────────────────┐
    │ Approved: Xuất bản            │
    │ POST /publish                 │
    │ → status: "published"         │
    │ → is_published: true          │
    └───────────────────────────────┘
```

---

## 📝 JSON SCHEMA - CHI TIẾT CÁC TRƯỜNG

### CLO (Course Learning Outcome)
```json
"clos": [
  {
    "id": "CLO1",
    "description": "Hiểu biết cơ bản về lập trình Python",
    "level": "K2"  // K1, K2, K3, K4, K5, K6 (Bloom's taxonomy)
  },
  {
    "id": "CLO2",
    "description": "Viết chương trình Python đơn giản",
    "level": "K3"
  }
]
```

### PLO (Program Learning Outcome)
```json
"plos": [
  {
    "id": "PLO1",
    "description": "Kỹ năng lập trình",
    "alignment": 0.8  // 0-1 (mức độ liên quan)
  },
  {
    "id": "PLO2",
    "description": "Giải quyết vấn đề",
    "alignment": 0.6
  }
]
```

### CLO-PLO Mapping
```json
"clo_plo_mapping": {
  "CLO1": ["PLO1"],           // CLO1 liên kết với PLO1
  "CLO2": ["PLO1", "PLO2"],   // CLO2 liên kết với PLO1 và PLO2
  "CLO3": ["PLO2"]            // CLO3 liên kết với PLO2
}
```

### Assessment Weights
```json
"assessment_weights": {
  "attendance": 10,      // Điểm danh 10%
  "assignment": 30,      // Bài tập 30%
  "midterm": 20,         // Kiểm tra giữa kỳ 20%
  "final_exam": 40,      // Thi cuối kỳ 40%
  "project": 0,          // Đồ án 0%
  "other": 0             // Khác 0%
}
// Tổng: 100%
```

### Prerequisites (Tiên quyệt)
```json
"prerequisites": [
  {"id": 1, "code": "CS100", "name": "Lập trình C cơ bản"},
  {"id": 2, "code": "MATH101", "name": "Toán rời rạc"}
]
```

### Textbooks
```json
"textbooks": [
  {
    "title": "Learning Python",
    "author": "Mark Lutz",
    "year": 2024,
    "isbn": "978-1098159855",
    "publisher": "O'Reilly"
  }
]
```

---

## 🧪 KIỂM THỬ

### Test Script PowerShell

```powershell
# 1. Đăng nhập lấy token
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{
    "email": "lecturer1@example.com",
    "password": "securepass123"
  }'

$token = $loginResponse.access_token

# 2. Tạo giáo trình mới
$createResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syllabus" `
  -Method POST `
  -Headers @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
  } `
  -Body '{
    "subject_code": "CS101",
    "subject_name": "Lập trình Python",
    "credits": 3,
    "semester": 1,
    "department": "Khoa CNTT",
    "academic_year": "2025-2026",
    "objectives": "Dạy học lập trình Python cơ bản",
    "content": "Variables, Functions, Classes"
  }'

$syllabusId = $createResponse.id
Write-Host "Created syllabus ID: $syllabusId"

# 3. Cập nhật giáo trình
$updateResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syllabus/$syllabusId" `
  -Method PUT `
  -Headers @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
  } `
  -Body '{
    "objectives": "Updated objectives",
    "clos": [
      {"id": "CLO1", "description": "Understand basics", "level": "K2"},
      {"id": "CLO2", "description": "Write programs", "level": "K3"}
    ],
    "change_summary": "Added CLOs"
  }'

# 4. Lấy lịch sử phiên bản
$versions = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syllabus/$syllabusId/versions" `
  -Method GET `
  -Headers @{"Authorization" = "Bearer $token"}

Write-Host "Versions: $($versions.total)"

# 5. Nộp để phê duyệt
$submitResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syllabus/$syllabusId/status" `
  -Method PATCH `
  -Headers @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
  } `
  -Body '{"status": "submitted"}'

Write-Host "Status: $($submitResponse.status)"
```

---

## 📊 FLOW DỮ LIỆU

```
┌──────────────┐
│   Frontend   │ (Admin Web, Lecturer Web)
└──────┬───────┘
       │
       ▼ HTTP Request
┌──────────────────────┐
│   API Routes         │  app/api/v1/syllabus.py
│   (Endpoints)        │  - POST/GET/PUT/DELETE /syllabus
└──────┬───────────────┘  - Version control endpoints
       │
       ▼ Dependency Injection
┌──────────────────────┐
│   Services           │  app/services/syllabus_service.py
│   (Business Logic)   │  - SyllabusService
└──────┬───────────────┘  - SyllabusVersionService
       │
       ▼ Method calls
┌──────────────────────┐
│   Repositories       │  app/repositories/syllabus_repo.py
│   (Data Access)      │  - SyllabusRepository.create()
└──────┬───────────────┘  - SyllabusVersionRepository.list_versions()
       │
       ▼ SQLAlchemy ORM
┌──────────────────────┐
│   Models             │  app/models/syllabus.py
│   (Schemas)          │  - Syllabus
└──────┬───────────────┘  - SyllabusVersion
       │
       ▼ SQL Queries
┌──────────────────────┐
│   Database           │  SQLite (dev) / MySQL (prod)
│   (SQLAlchemy)       │  - syllabuses table
└──────────────────────┘  - syllabus_versions table
```

---

## 🚀 CHẠY HỆ THỐNG

### 1. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 2. Khởi động Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Truy cập API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Test API
Sử dụng Swagger UI hoặc test script PowerShell/Bash.

---

## 📌 TÓMO TẮT ĐIỀU KIỆN CÓ SẴN

### Quyền Hạn (Authorization)
- ✅ `require_roles("lecturer", "hod", "admin")`: Tạo, cập nhật giáo trình
- ✅ `require_roles("hod", "admin")`: Xóa, phê duyệt, xuất bản
- ✅ `get_current_user`: Ai cũng xem được công khai

### Workflow Status
```
draft → submitted → under_review → approved → published
   ↓
[Lecturer chỉnh sửa]
   ↓
[Gửi lại để review]
```

### Version Control
- Mỗi thay đổi = 1 version mới
- Có thể rollback đến version cũ
- Có thể so sánh 2 version
- Xem changelog của từng thay đổi

---

## 🎯 Các Tính Năng Chính

| Tính Năng | Mô Tả |
|-----------|-------|
| 📝 CRUD | Tạo, đọc, cập nhật, xóa giáo trình |
| 📚 Version Control | Tự động theo dõi, rollback, so sánh |
| 🎯 CLO/PLO | Course & Program Learning Outcomes |
| ✅ Workflow | Draft → Submitted → Approved → Published |
| 🔍 Search | Tìm kiếm theo mã, tên, mô tả |
| 👥 Multi-role | Lecturer, HOD, Admin, AA, Student |
| 📊 Metadata | Tiên quyệt, song song, tài liệu tham khảo |
| 🔐 Authorization | Phân quyền dựa trên role |

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. Access token hợp lệ?
2. Role của user có đủ quyền không?
3. Syllabus ID có tồn tại?
4. Dữ liệu JSON định dạng đúng?

---

**Status**: ✅ Module 2 hoàn thành và sẵn sàng sử dụng
