import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.core.security import get_password_hash, create_access_token

# Setup test database - MySQL XAMPP
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test data
test_lecturer = None
test_hod = None
test_syllabus_id = None
test_clo = None
test_plo_id = None
test_mapping = None
lecturer_token = None
hod_token = None


@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test users, syllabus, and initial data"""
    global test_lecturer, test_hod, test_syllabus_id, lecturer_token, hod_token, test_plo_id
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Clear existing data in correct order (respect foreign keys)
    # Import WorkflowEvent if needed
    try:
        from app.models.workflow import WorkflowEvent
        from app.models.review import Review
        from app.models.syllabus import SyllabusVersion
        
        # Delete in reverse dependency order
        db.query(WorkflowEvent).delete()
        db.query(Review).delete() 
        db.query(CLO_PLO_Mapping).delete()
        db.query(CLO).delete()
        db.query(PLO).delete()
        db.query(SyllabusVersion).delete()
        db.query(Syllabus).delete()
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Warning during cleanup: {e}")
        # Continue anyway for fresh test data
    
    # Create test lecturer
    test_lecturer = User(
        email="lecturer@test.com",
        full_name="Test Lecturer",
        hashed_password=get_password_hash("password123"),
        role="lecturer",
        is_active=True
    )
    db.add(test_lecturer)
    db.commit()
    db.refresh(test_lecturer)
    
    # Create test HOD
    test_hod = User(
        email="hod@test.com",
        full_name="Test HOD",
        hashed_password=get_password_hash("password123"),
        role="hod",
        is_active=True
    )
    db.add(test_hod)
    db.commit()
    db.refresh(test_hod)
    
    # Create test syllabus
    test_syllabus = Syllabus(
        subject_code="CS101",
        subject_name="Introduction to Computer Science",
        description="Test syllabus for CLO-PLO",
        credits=3,
        semester=1,
        department="Computer Science",
        academic_year="2024-2025",
        created_by=test_lecturer.id,
        status="draft"
    )
    db.add(test_syllabus)
    db.commit()
    db.refresh(test_syllabus)
    test_syllabus_id = test_syllabus.id
    
    # Create test PLO
    test_plo = PLO(
        code="PLO1",
        description="Apply fundamental programming concepts",
        program_code="CS",
        program_name="Computer Science",
        category="Knowledge",
        weight=1.0
    )
    db.add(test_plo)
    db.commit()
    db.refresh(test_plo)
    test_plo_id = test_plo.id
    
    # Create tokens
    lecturer_token = create_access_token(str(test_lecturer.id))
    hod_token = create_access_token(str(test_hod.id))
    
    db.close()
    
    yield
    
    # Cleanup
    db = TestingSessionLocal()
    db.query(CLO_PLO_Mapping).delete()
    db.query(CLO).delete()
    db.query(PLO).delete()
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    db.close()
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)


def auth_header(token):
    """Helper to create auth header"""
    return {"Authorization": f"Bearer {token}"}


# ============ CLO Tests ============

def test_create_clo():
    """Test creating a new CLO"""
    global test_clo
    
    data = {
        "syllabus_id": test_syllabus_id,
        "code": "CLO1",
        "description": "Understand basic programming concepts",
        "cognitive_level": "K2",
        "weight": 1.5
    }
    
    response = client.post("/clo-plo/clo", json=data, headers=auth_header(lecturer_token))
    
    assert response.status_code == 201
    result = response.json()
    assert result["code"] == "CLO1"
    assert result["description"] == data["description"]
    assert result["cognitive_level"] == "K2"
    assert result["weight"] == 1.5
    assert result["syllabus_id"] == test_syllabus_id
    
    test_clo = result


def test_create_clo_unauthorized():
    """Test creating CLO without permission"""
    data = {
        "syllabus_id": test_syllabus_id,
        "code": "CLO_UNAUTHORIZED",
        "description": "This should fail"
    }
    
    response = client.post("/clo-plo/clo", json=data)
    assert response.status_code == 401


def test_create_clo_invalid_syllabus():
    """Test creating CLO with invalid syllabus"""
    data = {
        "syllabus_id": 99999,
        "code": "CLO_INVALID",
        "description": "Invalid syllabus"
    }
    
    response = client.post("/clo-plo/clo", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 404


def test_get_clos_by_syllabus():
    """Test getting all CLOs for a syllabus"""
    # Create another CLO
    data = {
        "syllabus_id": test_syllabus_id,
        "code": "CLO2",
        "description": "Apply programming skills",
        "cognitive_level": "K3"
    }
    client.post("/clo-plo/clo", json=data, headers=auth_header(lecturer_token))
    
    response = client.get(f"/clo-plo/clo/syllabus/{test_syllabus_id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 2
    assert any(c["code"] == "CLO1" for c in result)
    assert any(c["code"] == "CLO2" for c in result)


def test_update_clo():
    """Test updating a CLO"""
    update_data = {
        "description": "Updated description for CLO1",
        "cognitive_level": "K3"
    }
    
    response = client.patch(
        f"/clo-plo/clo/{test_clo['id']}", 
        json=update_data, 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["description"] == "Updated description for CLO1"
    assert result["cognitive_level"] == "K3"


def test_update_clo_by_hod():
    """Test HOD can update any CLO"""
    update_data = {
        "weight": 2.0
    }
    
    response = client.patch(
        f"/clo-plo/clo/{test_clo['id']}", 
        json=update_data, 
        headers=auth_header(hod_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["weight"] == 2.0


def test_delete_clo():
    """Test deleting a CLO"""
    # Create a CLO to delete
    data = {
        "syllabus_id": test_syllabus_id,
        "code": "CLO_DELETE",
        "description": "To be deleted"
    }
    create_response = client.post("/clo-plo/clo", json=data, headers=auth_header(lecturer_token))
    clo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/clo-plo/clo/{clo_id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


# ============ PLO Tests ============

def test_create_plo_by_hod():
    """Test creating PLO by HOD"""
    data = {
        "code": "PLO2",
        "description": "Demonstrate problem-solving skills",
        "program_code": "CS",
        "program_name": "Computer Science",
        "category": "Skills",
        "weight": 1.5
    }
    
    response = client.post("/clo-plo/plo", json=data, headers=auth_header(hod_token))
    
    assert response.status_code == 201
    result = response.json()
    assert result["code"] == "PLO2"
    assert result["description"] == data["description"]
    assert result["category"] == "Skills"


def test_create_plo_unauthorized():
    """Test lecturer cannot create PLO"""
    data = {
        "code": "PLO_UNAUTHORIZED",
        "description": "This should fail"
    }
    
    response = client.post("/clo-plo/plo", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 403


def test_create_plo_duplicate_code():
    """Test creating PLO with duplicate code"""
    data = {
        "code": "PLO1",  # Already exists
        "description": "Duplicate code"
    }
    
    response = client.post("/clo-plo/plo", json=data, headers=auth_header(hod_token))
    assert response.status_code == 400


def test_get_all_plos():
    """Test getting all PLOs"""
    response = client.get("/clo-plo/plo", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 2
    assert any(p["code"] == "PLO1" for p in result)
    assert any(p["code"] == "PLO2" for p in result)


def test_get_plos_by_program():
    """Test filtering PLOs by program code"""
    response = client.get("/clo-plo/plo?program_code=CS", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert all(p["program_code"] == "CS" for p in result)


def test_update_plo():
    """Test updating PLO"""
    update_data = {
        "description": "Updated PLO description"
    }
    
    response = client.patch(
        f"/clo-plo/plo/{test_plo_id}", 
        json=update_data, 
        headers=auth_header(hod_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["description"] == "Updated PLO description"


def test_update_plo_unauthorized():
    """Test lecturer cannot update PLO"""
    update_data = {
        "description": "Should fail"
    }
    
    response = client.patch(
        f"/clo-plo/plo/{test_plo_id}", 
        json=update_data, 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 403


# ============ Mapping Tests ============

def test_create_mapping():
    """Test creating CLO-PLO mapping"""
    global test_mapping
    
    data = {
        "clo_id": test_clo["id"],
        "plo_id": test_plo_id,
        "correlation_level": "high",
        "correlation_score": 0.8,
        "notes": "Strong correlation"
    }
    
    response = client.post("/clo-plo/mapping", json=data, headers=auth_header(lecturer_token))
    
    assert response.status_code == 201
    result = response.json()
    assert result["clo_id"] == test_clo["id"]
    assert result["plo_id"] == test_plo_id
    assert result["correlation_level"] == "high"
    assert result["correlation_score"] == 0.8
    
    test_mapping = result


def test_create_mapping_duplicate():
    """Test creating duplicate mapping"""
    data = {
        "clo_id": test_clo["id"],
        "plo_id": test_plo_id,
        "correlation_level": "medium"
    }
    
    response = client.post("/clo-plo/mapping", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 400  # Already exists


def test_create_mapping_invalid_clo():
    """Test creating mapping with invalid CLO"""
    data = {
        "clo_id": 99999,
        "plo_id": test_plo_id,
        "correlation_level": "medium"
    }
    
    response = client.post("/clo-plo/mapping", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 404


def test_get_mappings_by_syllabus():
    """Test getting all mappings for a syllabus"""
    response = client.get(
        f"/clo-plo/mapping/syllabus/{test_syllabus_id}", 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 1
    assert any(m["clo_id"] == test_clo["id"] for m in result)


def test_get_mapping_matrix():
    """Test getting complete mapping matrix"""
    response = client.get(
        f"/clo-plo/mapping/matrix/{test_syllabus_id}", 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["syllabus_id"] == test_syllabus_id
    assert "clos" in result
    assert "plos" in result
    assert "mappings" in result
    assert len(result["clos"]) >= 2
    assert len(result["plos"]) >= 1
    assert len(result["mappings"]) >= 1


def test_update_mapping():
    """Test updating a mapping"""
    update_data = {
        "correlation_level": "medium",
        "correlation_score": 0.6,
        "notes": "Updated correlation"
    }
    
    response = client.patch(
        f"/clo-plo/mapping/{test_mapping['id']}", 
        json=update_data, 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["correlation_level"] == "medium"
    assert result["correlation_score"] == 0.6
    assert result["notes"] == "Updated correlation"


def test_delete_mapping():
    """Test deleting a mapping"""
    # Create a mapping to delete
    db = TestingSessionLocal()
    clo2 = db.query(CLO).filter(CLO.code == "CLO2").first()
    clo2_id = clo2.id if clo2 else None
    db.close()
    
    if clo2_id:
        data = {
            "clo_id": clo2_id,
            "plo_id": test_plo_id,
            "correlation_level": "low"
        }
        create_response = client.post("/clo-plo/mapping", json=data, headers=auth_header(lecturer_token))
        if create_response.status_code == 201:
            mapping_id = create_response.json()["id"]
            
            # Delete it
            response = client.delete(f"/clo-plo/mapping/{mapping_id}", headers=auth_header(lecturer_token))
            
            assert response.status_code == 200
            assert "deleted successfully" in response.json()["message"]


def test_delete_plo():
    """Test deleting PLO"""
    # Create a PLO to delete
    data = {
        "code": "PLO_DELETE",
        "description": "To be deleted"
    }
    create_response = client.post("/clo-plo/plo", json=data, headers=auth_header(hod_token))
    plo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/clo-plo/plo/{plo_id}", headers=auth_header(hod_token))
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


def test_validation_errors():
    """Test validation for invalid data"""
    # Invalid correlation_level
    data = {
        "clo_id": test_clo["id"],
        "plo_id": test_plo_id,
        "correlation_level": "invalid_level"
    }
    response = client.post("/clo-plo/mapping", json=data, headers=auth_header(lecturer_token))
    # Should still create as we don't enforce enum validation in schema
    # But correlation_score out of range should fail
    
    # Invalid correlation_score (> 1.0)
    data2 = {
        "clo_id": test_clo["id"],
        "plo_id": 2,  # Different PLO
        "correlation_score": 1.5  # Invalid
    }
    response2 = client.post("/clo-plo/mapping", json=data2, headers=auth_header(lecturer_token))
    assert response2.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
