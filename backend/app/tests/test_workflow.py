"""
Test Module 3: Workflow (Review → Approve → Publish)
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
aa_token = None
admin_token = None
test_syllabus_id = None

@pytest.fixture(scope="module", autouse=True)
def setup_tokens():
    """Setup authentication tokens"""
    global lecturer_token, hod_token, aa_token, admin_token
    
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
    
    # Login as AA (Academic Affairs)
    response = client.post("/auth/login", json={
        "email": "aa@hcmute.edu.vn",
        "password": "aa123"
    })
    assert response.status_code == 200
    aa_token = response.json()["access_token"]
    
    # Login as Admin (Principal)
    response = client.post("/auth/login", json={
        "email": "admin@hcmute.edu.vn",
        "password": "admin123"
    })
    assert response.status_code == 200
    admin_token = response.json()["access_token"]
    
    yield

# ============= WORKFLOW SUBMIT TESTS =============

def test_submit_syllabus_for_review():
    """Test: Lecturer submit syllabus để review"""
    global test_syllabus_id
    
    # Tạo syllabus mới
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT900",
            "course_name": "Workflow Test Course",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "Information Technology"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    test_syllabus_id = response.json()["id"]
    
    # Submit for review
    response = client.post(
        f"/workflow/submit/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_hod"
    assert "submitted" in data["message"].lower()

def test_submit_already_submitted():
    """Test: Không thể submit syllabus đã submit"""
    response = client.post(
        f"/workflow/submit/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()

def test_submit_unauthorized():
    """Test: Lecturer khác không thể submit"""
    # Login as another lecturer
    response = client.post("/auth/login", json={
        "email": "lecturer2@hcmute.edu.vn",
        "password": "lecturer123"
    })
    other_token = response.json()["access_token"]
    
    response = client.post(
        f"/workflow/submit/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {other_token}"}
    )
    assert response.status_code == 403

# ============= HOD APPROVAL TESTS =============

def test_hod_approve():
    """Test: HOD approve syllabus"""
    response = client.post(
        f"/workflow/hod-approve/{test_syllabus_id}",
        json={"comments": "Approved by HOD"},
        headers={"Authorization": f"Bearer {hod_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_aa"
    assert "approved" in data["message"].lower()

def test_hod_reject():
    """Test: HOD reject syllabus"""
    # Tạo syllabus mới để test reject
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT901",
            "course_name": "Reject Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    reject_id = response.json()["id"]
    
    # Submit
    client.post(
        f"/workflow/submit/{reject_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    
    # HOD reject
    response = client.post(
        f"/workflow/hod-reject/{reject_id}",
        json={"comments": "Needs revision"},
        headers={"Authorization": f"Bearer {hod_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    assert "rejected" in data["message"].lower()

def test_hod_approve_unauthorized():
    """Test: Lecturer không thể approve như HOD"""
    response = client.post(
        f"/workflow/hod-approve/{test_syllabus_id}",
        json={"comments": "Fake approval"},
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 403

# ============= AA APPROVAL TESTS =============

def test_aa_approve():
    """Test: Academic Affairs approve"""
    response = client.post(
        f"/workflow/aa-approve/{test_syllabus_id}",
        json={"comments": "Approved by AA"},
        headers={"Authorization": f"Bearer {aa_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_principal"
    assert "approved" in data["message"].lower()

def test_aa_reject():
    """Test: AA reject syllabus"""
    # Tạo syllabus mới
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT902",
            "course_name": "AA Reject Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    aa_reject_id = response.json()["id"]
    
    # Submit và HOD approve
    client.post(f"/workflow/submit/{aa_reject_id}", headers={"Authorization": f"Bearer {lecturer_token}"})
    client.post(f"/workflow/hod-approve/{aa_reject_id}", json={"comments": "OK"}, headers={"Authorization": f"Bearer {hod_token}"})
    
    # AA reject
    response = client.post(
        f"/workflow/aa-reject/{aa_reject_id}",
        json={"comments": "Not aligned with curriculum"},
        headers={"Authorization": f"Bearer {aa_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

def test_aa_approve_wrong_status():
    """Test: AA không thể approve syllabus chưa qua HOD"""
    # Tạo syllabus mới (status = draft)
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT903",
            "course_name": "Wrong Status Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    wrong_id = response.json()["id"]
    
    response = client.post(
        f"/workflow/aa-approve/{wrong_id}",
        json={"comments": "Wrong"},
        headers={"Authorization": f"Bearer {aa_token}"}
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"].lower()

# ============= FINAL APPROVAL TESTS =============

def test_principal_approve_publish():
    """Test: Principal approve và publish"""
    response = client.post(
        f"/workflow/final-approve/{test_syllabus_id}",
        json={"comments": "Final approval granted"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"
    assert "published" in data["message"].lower()

def test_principal_reject():
    """Test: Principal reject (back to lecturer)"""
    # Tạo workflow hoàn chỉnh để test
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT904",
            "course_name": "Principal Reject Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    principal_reject_id = response.json()["id"]
    
    # Submit → HOD approve → AA approve
    client.post(f"/workflow/submit/{principal_reject_id}", headers={"Authorization": f"Bearer {lecturer_token}"})
    client.post(f"/workflow/hod-approve/{principal_reject_id}", json={"comments": "OK"}, headers={"Authorization": f"Bearer {hod_token}"})
    client.post(f"/workflow/aa-approve/{principal_reject_id}", json={"comments": "OK"}, headers={"Authorization": f"Bearer {aa_token}"})
    
    # Principal reject
    response = client.post(
        f"/workflow/final-reject/{principal_reject_id}",
        json={"comments": "Strategic concerns"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

# ============= WORKFLOW HISTORY TESTS =============

def test_get_workflow_history():
    """Test: Xem lịch sử workflow của syllabus"""
    response = client.get(
        f"/workflow/history/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4  # submit, hod_approve, aa_approve, final_approve
    
    # Kiểm tra workflow events
    events = [event["action"] for event in data]
    assert "submit" in events
    assert "hod_approve" in events
    assert "aa_approve" in events
    assert "final_approve" in events

def test_workflow_event_details():
    """Test: Chi tiết workflow event"""
    response = client.get(
        f"/workflow/history/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    events = response.json()
    
    # Mỗi event phải có đầy đủ thông tin
    for event in events:
        assert "action" in event
        assert "performed_by" in event
        assert "created_at" in event
        assert "comments" in event or event["comments"] is None

# ============= WORKFLOW STATUS TESTS =============

def test_get_pending_syllabuses_hod():
    """Test: HOD xem danh sách pending syllabuses"""
    response = client.get(
        "/workflow/pending/hod",
        headers={"Authorization": f"Bearer {hod_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_pending_syllabuses_aa():
    """Test: AA xem danh sách pending syllabuses"""
    response = client.get(
        "/workflow/pending/aa",
        headers={"Authorization": f"Bearer {aa_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_pending_syllabuses_principal():
    """Test: Principal xem danh sách pending syllabuses"""
    response = client.get(
        "/workflow/pending/principal",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# ============= WORKFLOW VALIDATION TESTS =============

def test_cannot_edit_published_syllabus():
    """Test: Không thể edit syllabus đã published"""
    response = client.put(
        f"/syllabus/{test_syllabus_id}",
        json={"course_name": "Hacked Published"},
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 400
    assert "published" in response.json()["detail"].lower()

def test_cannot_delete_published_syllabus():
    """Test: Không thể xóa syllabus đã published"""
    response = client.delete(
        f"/syllabus/{test_syllabus_id}",
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    assert response.status_code == 400
    assert "published" in response.json()["detail"].lower()

def test_workflow_sequence_enforcement():
    """Test: Phải đi đúng thứ tự workflow"""
    # Tạo syllabus mới
    response = client.post(
        "/syllabus",
        json={
            "course_code": "IT905",
            "course_name": "Sequence Test",
            "credits": 3,
            "theory_hours": 30,
            "practice_hours": 30,
            "semester": "1/2024-2025",
            "program": "IT"
        },
        headers={"Authorization": f"Bearer {lecturer_token}"}
    )
    sequence_id = response.json()["id"]
    
    # Thử approve trước khi submit
    response = client.post(
        f"/workflow/hod-approve/{sequence_id}",
        json={"comments": "Skip submit"},
        headers={"Authorization": f"Bearer {hod_token}"}
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"].lower()
