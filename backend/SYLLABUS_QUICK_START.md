# QUICK START - MODULE 2 SYLLABUS MANAGEMENT

## ⚡ 5 Phút Khởi Động

### 1️⃣ Khởi động Server
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2️⃣ Truy cập Swagger UI
```
http://localhost:8000/docs
```

### 3️⃣ Đăng nhập & Tạo Giáo trình

**Đăng nhập:**
```bash
POST /api/v1/auth/login
{
  "email": "lecturer1@example.com",
  "password": "securepass123"
}
```

**Tạo Giáo trình:**
```bash
POST /api/v1/syllabus
Authorization: Bearer <token_from_login>

{
  "subject_code": "CS101",
  "subject_name": "Lập trình Python",
  "credits": 3,
  "semester": 1,
  "department": "Khoa CNTT",
  "academic_year": "2025-2026",
  "objectives": "Dạy lập trình Python cơ bản",
  "content": "Variables, Functions, Classes"
}
```

---

## 🎯 Common Use Cases

### Trường hợp 1: Tạo & Chỉnh sửa Giáo trình

```
1. POST /syllabus
   → Status: "draft"
   → Version: 1 (tự động tạo)

2. PUT /syllabus/{id}
   → Cập nhật nội dung
   → Tự động tạo Version 2
   → Ghi lại changelog

3. PUT /syllabus/{id}
   → Cập nhật CLO/PLO
   → Tự động tạo Version 3
   → ...

4. PATCH /syllabus/{id}/status
   → Đổi status: "submitted"
   → Gửi duyệt

5. PATCH /syllabus/{id}/status (HOD)
   → Đổi status: "approved"

6. POST /syllabus/{id}/publish (HOD)
   → Đổi status: "published"
   → Công khai cho tất cả
```

---

### Trường hợp 2: Xem Lịch sử & Rollback

```
# Xem tất cả phiên bản
GET /syllabus/{id}/versions

# Xem chi tiết version 2
GET /syllabus/{id}/versions/2

# So sánh version 2 vs 3
GET /syllabus/{id}/versions/2/compare/3

# Khôi phục về version 2
POST /syllabus/{id}/versions/2/rollback
→ Tự động tạo version N (rollback record)
```

---

### Trường hợp 3: Cập nhật CLO-PLO

```
PUT /syllabus/{id}
{
  "clos": [
    {"id": "CLO1", "description": "Understand Python", "level": "K2"},
    {"id": "CLO2", "description": "Write programs", "level": "K3"}
  ],
  "plos": [
    {"id": "PLO1", "description": "Programming skills", "alignment": 0.9},
    {"id": "PLO2", "description": "Problem solving", "alignment": 0.8}
  ]
}

# Hoặc cập nhật mapping riêng
PATCH /syllabus/{id}/clo-plo-mapping
{
  "clo_plo_mapping": {
    "CLO1": ["PLO1"],
    "CLO2": ["PLO1", "PLO2"]
  }
}
```

---

### Trường hợp 4: Tìm kiếm Giáo trình

```
# Danh sách của tôi (có status filter)
GET /syllabus?skip=0&limit=10&semester=1&status=draft

# Tìm kiếm
GET /syllabus/search?q=python

# Lấy danh sách công khai
GET /syllabus/published?semester=1
```

---

## 🔑 API Authentication

### Lấy Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "lecturer1@example.com",
    "password": "securepass123"
  }'

# Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Sử dụng Token
```bash
curl -X GET http://localhost:8000/api/v1/syllabus \
  -H "Authorization: Bearer <access_token>"
```

---

## 👥 Test Accounts

### Lecturer (Tạo & chỉnh sửa riêng)
```
Email: lecturer1@example.com
Password: securepass123
Role: lecturer
```

### Admin (Quản lý tất cả)
```
Email: admin@example.com
Password: admin123
Role: admin
```

### HOD (Head of Department - Phê duyệt & xuất bản)
```
Email: hod@example.com
Password: hod123
Role: hod
```

---

## 📊 API Endpoints Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/syllabus` | Tạo giáo trình |
| GET | `/syllabus` | Danh sách của tôi |
| GET | `/syllabus/{id}` | Chi tiết |
| PUT | `/syllabus/{id}` | Cập nhật |
| DELETE | `/syllabus/{id}` | Xóa |
| GET | `/syllabus/search?q=...` | Tìm kiếm |
| GET | `/syllabus/published` | Công khai |
| GET | `/syllabus/{id}/versions` | Danh sách version |
| GET | `/syllabus/{id}/versions/latest` | Version mới nhất |
| GET | `/syllabus/{id}/versions/{vid}` | Chi tiết version |
| GET | `/syllabus/{id}/versions/{v1}/compare/{v2}` | So sánh |
| POST | `/syllabus/{id}/versions/{vid}/rollback` | Rollback |
| PATCH | `/syllabus/{id}/status` | Cập nhật trạng thái |
| POST | `/syllabus/{id}/publish` | Xuất bản |
| PATCH | `/syllabus/{id}/clo-plo-mapping` | Cập nhật mapping |

---

## 🧪 Test với PowerShell

```powershell
# Chạy test script
.\test_syllabus_api.ps1

# Hoặc chạy từng lệnh

# 1. Login
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{
    "email": "lecturer1@example.com",
    "password": "securepass123"
  }'

$token = $response.access_token

# 2. Tạo giáo trình
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/syllabus" `
  -Method POST `
  -Headers @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
  } `
  -Body '{
    "subject_code": "CS101",
    "subject_name": "Python",
    "credits": 3,
    "semester": 1,
    "objectives": "Learn Python",
    "content": "Variables, Functions"
  }'
```

---

## 📁 Key Files

```
Models:        app/models/syllabus.py
Schemas:       app/schemas/syllabus_schema.py
Repository:    app/repositories/syllabus_repo.py
Service:       app/services/syllabus_service.py
API:           app/api/v1/syllabus.py
Tests:         test_syllabus_api.ps1
Documentation: SYLLABUS_MANAGEMENT_MODULE.md
```

---

## 🐛 Troubleshooting

**❌ Error: "token_type must be bearer"**
- ✅ Kiểm tra token format: `Bearer <token>`

**❌ Error: "Syllabus not found"**
- ✅ Kiểm tra syllabus_id đúng

**❌ Error: "You can only update your own syllabuses"**
- ✅ Lecturer chỉ sửa được riêng của mình, dùng Admin để sửa của người khác

**❌ Error: "Database locked"**
- ✅ Kill process hiện tại: Ctrl+C, rồi chạy lại

**❌ Error: "Module not found"**
- ✅ Cài đặt dependencies: `pip install -r requirements.txt`

---

## ✨ Key Features

### 🔄 Automatic Version Control
- Mỗi `PUT` = 1 version mới
- Tự động ghi lại thay đổi
- Có thể rollback bất kỳ lúc nào

### 📍 CLO-PLO Mapping
- Liên kết Course Learning Outcomes (CLO)
- Với Program Learning Outcomes (PLO)
- Theo dõi alignment score

### ✅ Workflow Status
```
draft → submitted → under_review → approved → published
```

### 🔐 Role-Based Access
- Lecturer: Tạo & sửa riêng
- HOD/Admin: Quản lý tất cả & phê duyệt
- Student: Xem công khai

### 🔎 Search & Filter
- Tìm theo mã, tên, mô tả
- Lọc theo semester, department
- Lọc theo status

---

## 📞 Need Help?

1. **Check Documentation**: `SYLLABUS_MANAGEMENT_MODULE.md`
2. **Check Examples**: `test_syllabus_api.ps1`
3. **Check Swagger UI**: `http://localhost:8000/docs`
4. **Check ReDoc**: `http://localhost:8000/redoc`

---

**Status**: ✅ Ready to use!  
**Last Updated**: 2025-01-10  
**Version**: 1.0  
