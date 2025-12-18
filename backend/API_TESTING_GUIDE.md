# 📋 Hướng dẫn Test API Syllabus Management với Postman

## 🚀 Chuẩn bị

### 1. **Khởi động API Server**
```bash
cd D:\project cnpm\backend
& "D:/project cnpm/.venv/Scripts/python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**API Base URL:** `http://127.0.0.1:8000`

### 2. **Import Collection vào Postman**

1. Mở **Postman**
2. Click **Import** (top left)
3. Chọn **File**
4. Import file: `D:\project cnpm\backend\syllabus_api_postman_collection.json`
5. Collection sẽ xuất hiện: **"Syllabus Management API - Test Collection"**

### 3. **Cài đặt Environment Variables**

1. Trong Postman, tạo **Environment** mới
2. Thêm variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (sẽ được set sau khi login)

---

## 🧪 Test Scenarios

### **Phase 1: Health Check**

1. **API Health Check**
   - Method: `GET`
   - URL: `{{base_url}}/`
   - Expected: `200 OK` với FastAPI docs

### **Phase 2: User Authentication**

#### **2.1 Register User**
```json
POST {{base_url}}/api/v1/auth/register
Content-Type: application/json

{
  "email": "ngohuynhthuloan@gmail.com",
  "password": "password123",
  "full_name": "Ngô Huỳnh Thu Loan",
  "role": "lecturer"
}
```
- **Expected:** `201 Created` với user info
- **Check:** Password được hash bằng Argon2

#### **2.2 Login**
```json
POST {{base_url}}/api/v1/auth/login
Content-Type: application/json

{
  "email": "ngohuynhthuloan@gmail.com",
  "password": "password123"
}
```
- **Expected:** `200 OK` với JWT token
- **Save token:** Copy `access_token` vào environment variable

#### **2.3 Get Current User**
```json
GET {{base_url}}/api/v1/auth/me
Authorization: Bearer {{access_token}}
```
- **Expected:** `200 OK` với user info

### **Phase 3: Syllabus Management**

#### **3.1 Create Syllabus**
```json
POST {{base_url}}/api/v1/syllabus/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Introduction to Computer Science",
  "course_code": "CS101",
  "description": "Basic computer science concepts",
  "credits": 3,
  "prerequisites": "None",
  "objectives": "Learn basic programming",
  "course_content": "Variables, loops, functions",
  "teaching_methods": "Lectures, labs",
  "assessment_methods": "Exams, assignments",
  "resources": "Textbook, online resources"
}
```
- **Expected:** `201 Created` với syllabus info

#### **3.2 Get All Syllabuses**
```json
GET {{base_url}}/api/v1/syllabus/
Authorization: Bearer {{access_token}}
```
- **Expected:** `200 OK` với array of syllabuses

#### **3.3 Get Syllabus by ID**
```json
GET {{base_url}}/api/v1/syllabus/1
Authorization: Bearer {{access_token}}
```
- **Expected:** `200 OK` với syllabus details

#### **3.4 Update Syllabus**
```json
PUT {{base_url}}/api/v1/syllabus/1
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Advanced Computer Science",
  "description": "Advanced programming concepts"
}
```
- **Expected:** `200 OK` với updated syllabus

### **Phase 4: Search & Filter**

#### **4.1 Search Syllabuses**
```json
GET {{base_url}}/api/v1/search/?q=computer
Authorization: Bearer {{access_token}}
```
- **Expected:** `200 OK` với search results

### **Phase 5: Workflow Management**

#### **5.1 Get Workflow Events**
```json
GET {{base_url}}/api/v1/workflow/
Authorization: Bearer {{access_token}}
```
- **Expected:** `200 OK` với workflow events

#### **5.2 Create Workflow Event**
```json
POST {{base_url}}/api/v1/workflow/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "syllabus_id": 1,
  "action": "submitted",
  "from_status": "draft",
  "to_status": "pending_review",
  "comments": "Submitted for review"
}
```
- **Expected:** `201 Created` với workflow event

### **Phase 6: AI Features**

#### **6.1 Generate Syllabus Content**
```json
POST {{base_url}}/api/v1/ai/generate-syllabus
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "topic": "Machine Learning",
  "level": "intermediate",
  "duration": "12 weeks"
}
```
- **Expected:** `200 OK` với AI-generated content

### **Phase 7: CLO/PLO Management**

#### **7.1 Create CLO**
```json
POST {{base_url}}/api/v1/clo/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "syllabus_id": 1,
  "code": "CLO1",
  "description": "Understand basic programming concepts",
  "level": "understanding"
}
```
- **Expected:** `201 Created` với CLO info

#### **7.2 Create PLO**
```json
POST {{base_url}}/api/v1/plo/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "program_id": 1,
  "code": "PLO1",
  "description": "Apply programming skills",
  "level": "application"
}
```
- **Expected:** `201 Created` với PLO info

---

## 🔍 Test Cases Quan trọng

### **Authentication Tests**
- ✅ Register user thành công
- ✅ Login với credentials đúng
- ✅ Login với credentials sai → 401 Unauthorized
- ✅ Access protected endpoint without token → 401 Unauthorized
- ✅ Access protected endpoint with invalid token → 401 Unauthorized

### **CRUD Tests**
- ✅ Create syllabus
- ✅ Read syllabus (all & by ID)
- ✅ Update syllabus
- ✅ Delete syllabus (nếu có endpoint)

### **Business Logic Tests**
- ✅ Password hashing (Argon2)
- ✅ JWT token generation/validation
- ✅ Role-based access control
- ✅ Workflow state transitions

### **Error Handling Tests**
- ✅ Invalid JSON → 422 Unprocessable Entity
- ✅ Missing required fields → 422 Unprocessable Entity
- ✅ Resource not found → 404 Not Found
- ✅ Unauthorized access → 401 Unauthorized
- ✅ Forbidden access → 403 Forbidden

---

## 🐛 Troubleshooting

### **Common Issues:**

1. **"Connection refused"**
   - Check if API server is running on port 8000
   - Verify URL: `http://127.0.0.1:8000`

2. **"401 Unauthorized"**
   - Check if JWT token is set in environment variables
   - Verify token format: `Bearer <token>`

3. **"422 Unprocessable Entity"**
   - Check JSON format and required fields
   - Validate data types (string, number, etc.)

4. **"500 Internal Server Error"**
   - Check server logs in terminal
   - Verify database connection
   - Check for missing dependencies

### **Debug Tips:**

1. **Check API Documentation:**
   - Visit: `http://127.0.0.1:8000/docs`
   - Interactive Swagger UI

2. **Monitor Server Logs:**
   - Watch terminal output for errors
   - Check database connection status

3. **Test Individual Components:**
   - Test database connection separately
   - Test authentication flow step-by-step

---

## 📊 Expected Response Codes

| Method | Endpoint | Success | Error Cases |
|--------|----------|---------|-------------|
| GET | `/` | 200 | - |
| POST | `/api/v1/auth/register` | 201 | 422, 400 |
| POST | `/api/v1/auth/login` | 200 | 401, 422 |
| GET | `/api/v1/auth/me` | 200 | 401 |
| GET | `/api/v1/syllabus/` | 200 | 401 |
| POST | `/api/v1/syllabus/` | 201 | 401, 422 |
| GET | `/api/v1/syllabus/{id}` | 200 | 401, 404 |
| PUT | `/api/v1/syllabus/{id}` | 200 | 401, 404, 422 |

---

## 🎯 Quick Test Checklist

- [ ] API server running
- [ ] Postman collection imported
- [ ] Environment variables set
- [ ] Health check passes
- [ ] User registration works
- [ ] Login returns JWT token
- [ ] Protected endpoints accessible
- [ ] CRUD operations work
- [ ] Search functionality works
- [ ] Error handling proper

**Happy Testing! 🚀**