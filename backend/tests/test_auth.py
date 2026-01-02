"""
Test Module 1: Authentication + User Management
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash

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

# Global test data
admin_token = None
lecturer_token = None
test_user_id = None

@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test data before all tests"""
    global admin_token, lecturer_token
    
    # Login as admin
    response = client.post("/auth/login", json={
        "email": "admin@hcmute.edu.vn",
        "password": "admin123"
    })
    assert response.status_code == 200
    admin_token = response.json()["access_token"]
    
    # Login as lecturer
    response = client.post("/auth/login", json={
        "email": "lecturer1@hcmute.edu.vn",
        "password": "lecturer123"
    })
    assert response.status_code == 200
    lecturer_token = response.json()["access_token"]
    
    yield
    
    # Cleanup if needed

# ============= AUTH TESTS =============

def test_login_success():
    """Test: Login thành công"""
    response = client.post("/auth/login", json={
        "email": "lecturer1@hcmute.edu.vn",
        "password": "lecturer123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "lecturer1@hcmute.edu.vn"
    assert data["user"]["role"] == "lecturer"

def test_login_invalid_email():
    """Test: Login với email không tồn tại"""
    response = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "password123"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_login_wrong_password():
    """Test: Login với password sai"""
    response = client.post("/auth/login", json={
        "email": "lecturer1@hcmute.edu.vn",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_missing_fields():
    """Test: Login thiếu fields"""
    response = client.post("/auth/login", json={
        "email": "lecturer1@hcmute.edu.vn"
    })
    assert response.status_code == 422

# ============= USER MANAGEMENT TESTS =============

def test_create_user_by_admin():
    """Test: Admin tạo user mới"""
    global test_user_id
    
    response = client.post(
        "/users",
        json={
            "email": "newtest@hcmute.edu.vn",
            "password": "newtest123",
            "full_name": "New Test User",
            "role": "lecturer"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newtest@hcmute.edu.vn"
    assert data["role"] == "lecturer"
    assert data["is_active"] == True
    test_user_id = data["id"]

def test_create_user_duplicate_email():
    """Test: Tạo user với email đã tồn tại"""
    response = client.post(
        "/users",
        json={
            "email": "lecturer1@hcmute.edu.vn",
            "password": "test123",
            "full_name": "Duplicate",
            "role": "lecturer"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_create_user_unauthorized():
    """Test: Lecturer không thể tạo user"""
    response = client.post(
        "/users",
        json={
            "email": "test@test.com",
            "password": "test123",
            "full_name": "Test",
            "role": "student"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 403

def test_get_all_users():
    """Test: Admin xem danh sách users"""
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "email" in data[0]
    assert "role" in data[0]

def test_get_user_by_id():
    """Test: Xem chi tiết 1 user"""
    response = client.get(
        f"/users/{test_user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user_id
    assert data["email"] == "newtest@hcmute.edu.vn"

def test_update_user():
    """Test: Admin cập nhật thông tin user"""
    response = client.patch(
        f"/users/{test_user_id}",
        json={"full_name": "Updated Name"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

def test_lock_user():
    """Test: Admin khóa user"""
    response = client.patch(
        f"/users/{test_user_id}/lock",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["is_active"] == False

def test_unlock_user():
    """Test: Admin mở khóa user"""
    response = client.patch(
        f"/users/{test_user_id}/unlock",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["is_active"] == True

def test_delete_user():
    """Test: Admin xóa user"""
    response = client.delete(
        f"/users/{test_user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()

def test_get_current_user():
    """Test: Lấy thông tin user hiện tại"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "lecturer1@hcmute.edu.vn"
    assert data["role"] == "lecturer"

# ============= AUTHORIZATION TESTS =============

def test_access_without_token():
    """Test: Truy cập endpoint cần auth mà không có token"""
    response = client.get("/users")
    assert response.status_code == 401

def test_access_with_invalid_token():
    """Test: Truy cập với token không hợp lệ"""
    response = client.get(
        "/users",
        headers={"Authorization": "Bearer invalid_token_xyz"}
    )
    assert response.status_code == 401

def test_role_based_access():
    """Test: Lecturer không thể truy cập admin endpoints"""
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    # Lecturer có thể xem danh sách nhưng không tạo/xóa
    # Kiểm tra qua create endpoint
    response = client.post(
        "/users",
        json={"email": "test@test.com", "password": "test123", "full_name": "Test", "role": "student"},
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 403
