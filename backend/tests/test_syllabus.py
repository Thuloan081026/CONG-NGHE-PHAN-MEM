"""
Test Module 2: Syllabus Management
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db

# Test database
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Global variables
lecturer_token = None
hod_token = None
test_syllabus_id = None

@pytest.fixture(scope="module", autouse=True)
def setup_tokens():
    """Setup authentication tokens"""
    global lecturer_token, hod_token
    
    # Login as lecturer
    response = client.post("/auth/login", json={
        "email": "lecturer1@hcmute.edu.vn",
        "password": "lecturer123"
    })
    assert response.status_code == 200
    lecturer_token = response.json()["access_token"]
    
    # Login as HOD
    response = client.post("/auth/login", json={
        "email": "hod.cs@hcmute.edu.vn",
        "password": "hod123"
    })
    assert response.status_code == 200
    hod_token = response.json()["access_token"]
    
    yield

# ============= SYLLABUS CRUD TESTS =============

def test_create_syllabus():
    """Test: Lecturer tạo syllabus mới"""
    global test_syllabus_id
    
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT999",
            "course_name": "Test Course",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "Information Technology",
            "description": "Test syllabus for automated testing",
            "objectives": "Learn testing",
            "content": "Unit 1: Introduction\nUnit 2: Testing",
            "assessment_methods": "Midterm 30%, Final 70%"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["course_code"] == "IT999"
    assert data["status"] == "draft"
    assert data["version"] == 1
    test_syllabus_id = data["id"]

def test_create_syllabus_duplicate_code():
    """Test: Không cho tạo syllabus trùng course_code trong cùng semester"""
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT001",  # Đã tồn tại
            "course_name": "Duplicate",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "Information Technology"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_create_syllabus_unauthorized():
    """Test: Student không thể tạo syllabus"""
    # Login as student
    response = client.post("/auth/login", json={
        "email": "student1@student.hcmute.edu.vn",
        "password": "student123"
    })
    student_token = response.json()["access_token"]
    
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT888",
            "course_name": "Unauthorized Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403

def test_get_all_syllabuses():
    """Test: Lấy danh sách tất cả syllabuses"""
    response = client.get(
        "/syllabus",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_syllabus_by_id():
    """Test: Lấy chi tiết syllabus"""
    response = client.get(
        f"/syllabus/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_syllabus_id
    assert data["course_code"] == "IT999"

def test_update_syllabus():
    """Test: Lecturer cập nhật syllabus (tạo version mới)"""
    response = client.put(
        f"/syllabus/{test_syllabus_id}",
        json={
            "course_name": "Updated Test Course",
            "description": "Updated description",
            "content": "Updated content"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["course_name"] == "Updated Test Course"
    assert data["version"] == 2  # Version tăng lên

def test_update_syllabus_unauthorized():
    """Test: Lecturer khác không thể update"""
    # Login as lecturer2
    response = client.post("/auth/login", json={
        "email": "lecturer2@hcmute.edu.vn",
        "password": "lecturer123"
    })
    other_token = response.json()["access_token"]
    
    response = client.put(
        f"/syllabus/{test_syllabus_id}",
        json={"course_name": "Hacked"},
        headers={"Authorization": f"Bearer {other_token}"}
    )
    assert response.status_code == 403

def test_get_syllabus_versions():
    """Test: Xem lịch sử versions của syllabus"""
    response = client.get(
        f"/syllabus/{test_syllabus_id}/versions",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Có ít nhất 2 versions (create + update)
    assert data[0]["version_number"] == 1
    assert data[1]["version_number"] == 2

def test_get_specific_version():
    """Test: Xem nội dung của 1 version cụ thể"""
    response = client.get(
        f"/syllabus/{test_syllabus_id}/versions/1",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["version_number"] == 1
    assert "content_snapshot" in data

def test_delete_syllabus():
    """Test: Xóa syllabus (chỉ draft)"""
    response = client.delete(
        f"/syllabus/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()

# ============= FILTER & SEARCH TESTS =============

def test_filter_by_status():
    """Test: Filter syllabuses theo status"""
    response = client.get(
        "/syllabus?status=draft",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["status"] == "draft"

def test_filter_by_program():
    """Test: Filter theo program"""
    response = client.get(
        "/syllabus?program=Information Technology",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["program"] == "Information Technology"

def test_filter_by_semester():
    """Test: Filter theo semester"""
    response = client.get(
        "/syllabus?semester=1/2024-2025",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["semester"] == "1/2024-2025"

# ============= METADATA TESTS =============

def test_syllabus_with_prerequisites():
    """Test: Tạo syllabus với prerequisites"""
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT998",
            "course_name": "Advanced Course",
            "credits": 4,
            "theory_hours": 45,
            "practice_hours": 45,
            "semester": "2/2024-2025",
            "program": "Information Technology",
            "prerequisites": "IT001, IT002"  # Yêu cầu học trước
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["prerequisites"] == "IT001, IT002"

def test_syllabus_with_corequisites():
    """Test: Tạo syllabus với corequisites"""
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT997",
            "course_name": "Parallel Course",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "2/2024-2025",
            "program": "Information Technology",
            "corequisites": "IT998"  # Học song song
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["corequisites"] == "IT998"

# ============= VERSION CONTROL TESTS =============

def test_version_increment():
    """Test: Mỗi lần update phải tăng version"""
    # Tạo syllabus mới
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT996",
            "course_name": "Version Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "2/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    syllabus_id = response.json()["id"]
    initial_version = response.json()["version"]
    
    # Update lần 1
    response = client.put(
        f"/syllabus/{syllabus_id}",
        json={"course_name": "Version Test v2"},
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.json()["version"] == initial_version + 1
    
    # Update lần 2
    response = client.put(
        f"/syllabus/{syllabus_id}",
        json={"course_name": "Version Test v3"},
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.json()["version"] == initial_version + 2

def test_version_history_integrity():
    """Test: Lịch sử versions phải đầy đủ"""
    # Tạo syllabus
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT995",
            "course_name": "History Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "2/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    syllabus_id = response.json()["id"]
    
    # Update 3 lần
    for i in range(3):
        client.put(
            f"/syllabus/{syllabus_id}",
            json={"course_name": f"History Test v{i+2}"},
            headers={"Authorization": f"Bearer {lecturer_token}"}
        )
    
    # Kiểm tra history
    response = client.get(
        f"/syllabus/{syllabus_id}/versions",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    versions = response.json()
    assert len(versions) == 4  # 1 create + 3 updates
    
    # Versions phải liên tục
    version_numbers = [v["version_number"] for v in versions]
    assert version_numbers == [1, 2, 3, 4]
