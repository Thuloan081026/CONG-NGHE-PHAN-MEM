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
from app.models.review import Review
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
test_syllabus = None
test_comment_id = None
lecturer_token = None
hod_token = None


@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test users and syllabus"""
    global test_lecturer, test_hod, test_syllabus, lecturer_token, hod_token
    
    db = TestingSessionLocal()
    
    # Clear existing data
    db.query(Review).delete()
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    
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
        description="Test syllabus for review",
        credits=3,
        semester=1,
        department="Computer Science",
        academic_year="2024-2025",
        created_by=test_lecturer.id,
        status="under_review"
    )
    db.add(test_syllabus)
    db.commit()
    db.refresh(test_syllabus)
    
    # Create tokens
    lecturer_token = create_access_token(str(test_lecturer.id))
    hod_token = create_access_token(str(test_hod.id))
    
    db.close()
    
    yield
    
    # Cleanup
    db = TestingSessionLocal()
    db.query(Review).delete()
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    db.close()
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)


def auth_header(token):
    """Helper to create auth header"""
    return {"Authorization": f"Bearer {token}"}


def test_create_review_comment():
    """Test creating a new review comment"""
    global test_comment_id
    
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "This is a test comment from lecturer",
        "section": "objectives"
    }
    
    response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    
    assert response.status_code == 201
    result = response.json()
    assert result["content"] == data["content"]
    assert result["syllabus_id"] == test_syllabus.id
    assert result["section"] == "objectives"
    assert result["is_resolved"] == 0
    assert "id" in result
    assert "created_at" in result
    assert result["author_email"] == "lecturer@test.com"
    
    test_comment_id = result["id"]


def test_create_comment_invalid_syllabus():
    """Test creating comment for non-existent syllabus"""
    data = {
        "syllabus_id": 99999,
        "content": "This should fail"
    }
    
    response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 404


def test_create_comment_without_auth():
    """Test creating comment without authentication"""
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "This should fail"
    }
    
    response = client.post("/review/comment", json=data)
    assert response.status_code == 401


def test_get_syllabus_reviews():
    """Test getting all reviews for a syllabus"""
    # Create another comment
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "Second comment from HOD",
        "section": "content"
    }
    client.post("/review/comment", json=data, headers=auth_header(hod_token))
    
    # Get all comments
    response = client.get(f"/review/syllabus/{test_syllabus.id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 2
    
    # Check comments are ordered by creation date (newest first)
    assert any(c["content"] == "This is a test comment from lecturer" for c in result)
    assert any(c["content"] == "Second comment from HOD" for c in result)


def test_get_reviews_invalid_syllabus():
    """Test getting reviews for non-existent syllabus"""
    response = client.get("/review/syllabus/99999", headers=auth_header(lecturer_token))
    assert response.status_code == 404


def test_get_single_review():
    """Test getting a single review comment"""
    response = client.get(f"/review/comment/{test_comment_id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == test_comment_id
    assert result["content"] == "This is a test comment from lecturer"


def test_update_comment_content():
    """Test updating comment content by author"""
    update_data = {
        "content": "Updated comment content",
        "section": "assessment"
    }
    
    response = client.patch(
        f"/review/comment/{test_comment_id}", 
        json=update_data, 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["content"] == "Updated comment content"
    assert result["section"] == "assessment"


def test_update_comment_unauthorized():
    """Test updating comment by non-author"""
    update_data = {
        "content": "This should fail"
    }
    
    response = client.patch(
        f"/review/comment/{test_comment_id}", 
        json=update_data, 
        headers=auth_header(hod_token)
    )
    
    assert response.status_code == 403


def test_resolve_comment_by_hod():
    """Test marking comment as resolved by HOD"""
    update_data = {
        "is_resolved": 1
    }
    
    response = client.patch(
        f"/review/comment/{test_comment_id}", 
        json=update_data, 
        headers=auth_header(hod_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["is_resolved"] == 1
    assert result["resolved_by"] == test_hod.id
    assert result["resolved_at"] is not None


def test_resolve_comment_unauthorized():
    """Test marking comment as resolved by non-HOD"""
    update_data = {
        "is_resolved": 1
    }
    
    response = client.patch(
        f"/review/comment/{test_comment_id}", 
        json=update_data, 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 403


def test_get_unresolved_comments():
    """Test getting unresolved comments (HOD only)"""
    # Create an unresolved comment
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "Unresolved comment"
    }
    client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    
    response = client.get(
        f"/review/syllabus/{test_syllabus.id}/unresolved", 
        headers=auth_header(hod_token)
    )
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert any(c["content"] == "Unresolved comment" for c in result)


def test_get_unresolved_comments_unauthorized():
    """Test getting unresolved comments as non-HOD"""
    response = client.get(
        f"/review/syllabus/{test_syllabus.id}/unresolved", 
        headers=auth_header(lecturer_token)
    )
    
    assert response.status_code == 403


def test_delete_comment_by_author():
    """Test deleting comment by author"""
    # Create a comment to delete
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "Comment to be deleted"
    }
    create_response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    comment_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/review/comment/{comment_id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Comment deleted successfully"
    assert result["deleted_id"] == comment_id
    
    # Verify it's deleted
    get_response = client.get(f"/review/comment/{comment_id}", headers=auth_header(lecturer_token))
    assert get_response.status_code == 404


def test_delete_comment_by_hod():
    """Test deleting comment by HOD"""
    # Create a comment by lecturer
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "Comment to be deleted by HOD"
    }
    create_response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    comment_id = create_response.json()["id"]
    
    # HOD deletes it
    response = client.delete(f"/review/comment/{comment_id}", headers=auth_header(hod_token))
    
    assert response.status_code == 200


def test_delete_comment_unauthorized():
    """Test deleting comment by unauthorized user"""
    # Create a comment by HOD
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "HOD's comment"
    }
    create_response = client.post("/review/comment", json=data, headers=auth_header(hod_token))
    comment_id = create_response.json()["id"]
    
    # Lecturer tries to delete it
    response = client.delete(f"/review/comment/{comment_id}", headers=auth_header(lecturer_token))
    
    assert response.status_code == 403


def test_delete_nonexistent_comment():
    """Test deleting non-existent comment"""
    response = client.delete("/review/comment/99999", headers=auth_header(lecturer_token))
    assert response.status_code == 404


def test_comment_validation():
    """Test comment content validation"""
    # Empty content
    data = {
        "syllabus_id": test_syllabus.id,
        "content": ""
    }
    response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 422
    
    # Content too long (over 5000 characters)
    data = {
        "syllabus_id": test_syllabus.id,
        "content": "x" * 5001
    }
    response = client.post("/review/comment", json=data, headers=auth_header(lecturer_token))
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

