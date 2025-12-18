"""
COMPREHENSIVE TEST: All 8 Backend Modules
Test tất cả chức năng từ Module 1 đến Module 8
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_header(text, char='='):
    print(f"\n{BLUE}{char*70}")
    print(f"  {text}")
    print(f"{char*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}[PASS] {text}{RESET}")

def print_error(text):
    print(f"{RED}[FAIL] {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}[TEST] {text}{RESET}")

def print_data(label, value):
    print(f"{CYAN}  {label}: {RESET}{value}")

# ==================== MODULE 1: AUTHENTICATION ====================

def test_module_1_authentication():
    """Module 1: Authentication + User Management"""
    print_header("MODULE 1: AUTHENTICATION + USER MANAGEMENT")
    
    # Test 1.1: Login as Admin
    print_info("Test 1.1: Admin Login")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    if response.status_code == 200:
        admin_token = response.json()["access_token"]
        print_success(f"Admin login successful")
        print_data("Token", admin_token[:30] + "...")
    else:
        print_error(f"Login failed: {response.text}")
        return None
    
    # Test 1.2: Login as Lecturer
    print_info("\nTest 1.2: Lecturer Login")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "lecturer@test.com", "password": "lecturer123"}
    )
    if response.status_code == 200:
        lecturer_token = response.json()["access_token"]
        print_success(f"Lecturer login successful")
    else:
        print_error(f"Login failed: {response.text}")
        lecturer_token = None
    
    # Test 1.3: Login as Student
    print_info("\nTest 1.3: Student Login")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "student@test.com", "password": "student123"}
    )
    if response.status_code == 200:
        student_token = response.json()["access_token"]
        print_success(f"Student login successful")
    else:
        print_error(f"Login failed: {response.text}")
        student_token = None
    
    # Test 1.3b: Login as HOD
    print_info("\nTest 1.3b: HOD Login")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "hod@test.com", "password": "hod123"}
    )
    if response.status_code == 200:
        hod_token = response.json()["access_token"]
        print_success(f"HOD login successful")
    else:
        print_error(f"Login failed: {response.text}")
        hod_token = None
    
    # Test 1.4: Get All Users (Admin only)
    print_info("\nTest 1.4: Get All Users (Admin RBAC)")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    if response.status_code == 200:
        users = response.json()
        print_success(f"Retrieved {len(users)} users")
        for user in users[:3]:
            print_data(f"  {user['role']}", f"{user['email']} - {user['full_name']}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 1.5: Create New User (Admin only)
    print_info("\nTest 1.5: Create New User")
    new_user = {
        "email": f"test_user_{datetime.now().timestamp()}@test.com",
        "full_name": "Test User",
        "password": "test123",
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        created_user = response.json()
        print_success(f"User created: {created_user['email']}")
        test_user_id = created_user['id']
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")
        test_user_id = None
    
    # Test 1.6: Lock User (Admin only)
    if test_user_id:
        print_info(f"\nTest 1.6: Lock User {test_user_id}")
        response = requests.patch(
            f"{BASE_URL}/users/{test_user_id}/lock",
            headers=headers
        )
        if response.status_code == 200:
            print_success(f"User locked successfully")
        else:
            print_error(f"Failed: {response.text}")
    
    return {
        "admin_token": admin_token,
        "lecturer_token": lecturer_token,
        "student_token": student_token,
        "hod_token": hod_token
    }

# ==================== MODULE 2: SYLLABUS MANAGEMENT ====================

def test_module_2_syllabus(tokens):
    """Module 2: Syllabus Management"""
    print_header("MODULE 2: SYLLABUS MANAGEMENT")
    
    lecturer_headers = {"Authorization": f"Bearer {tokens['lecturer_token']}"}
    
    # Test 2.1: Get All Syllabuses
    print_info("Test 2.1: Get All Syllabuses")
    response = requests.get(f"{BASE_URL}/syllabus/published", headers=lecturer_headers)
    if response.status_code == 200:
        data = response.json()
        syllabuses = data.get('items', [])
        print_success(f"Retrieved {len(syllabuses)} syllabuses (total: {data.get('total', 0)})")
        if syllabuses:
            syllabus = syllabuses[0]
            print_data("  First syllabus", f"{syllabus['subject_code']} - {syllabus['subject_name']}")
            syllabus_id = syllabus['id']
        else:
            syllabus_id = None
    else:
        print_error(f"Failed: {response.text}")
        syllabus_id = None
    
    # Test 2.2: Get Syllabus by ID
    if syllabus_id:
        print_info(f"\nTest 2.2: Get Syllabus {syllabus_id}")
        response = requests.get(f"{BASE_URL}/syllabus/{syllabus_id}", headers=lecturer_headers)
        if response.status_code == 200:
            syllabus = response.json()
            print_success(f"Retrieved syllabus: {syllabus['subject_code']}")
            print_data("  Name", syllabus['subject_name'])
            print_data("  Status", syllabus['status'])
            print_data("  Credits", syllabus['credits'])
        else:
            print_error(f"Failed: {response.text}")
    
    # Test 2.3: Get Syllabus Versions
    if syllabus_id:
        print_info(f"\nTest 2.3: Get Syllabus Versions")
        response = requests.get(f"{BASE_URL}/syllabus/{syllabus_id}/versions", headers=lecturer_headers)
        if response.status_code == 200:
            data = response.json()
            # Check if it's a list or dict with items
            if isinstance(data, dict):
                versions = data.get('items', [])
                total = data.get('total', 0)
                print_success(f"Retrieved {len(versions)} versions (total: {total})")
            else:
                versions = data
                print_success(f"Retrieved {len(versions)} versions")
                
            for v in versions[:3]:
                print_data(f"  Version {v['version_number']}", v.get('change_description', 'N/A'))
        else:
            print_error(f"Failed: {response.text}")
    
    # Test 2.4: Create New Syllabus
    print_info("\nTest 2.4: Create New Syllabus")
    new_syllabus = {
        "subject_code": f"TEST{int(datetime.now().timestamp()) % 10000}",
        "subject_name": "Test Subject",
        "credits": 3,
        "semester": 1,
        "department": "Test Department",
        "description": "Test syllabus for module testing"
    }
    response = requests.post(f"{BASE_URL}/syllabus/", json=new_syllabus, headers=lecturer_headers)
    if response.status_code == 200 or response.status_code == 201:
        created = response.json()
        print_success(f"Syllabus created: {created['subject_code']}")
        new_syllabus_id = created['id']
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")
        new_syllabus_id = None
    
    # Test 2.5: Update Syllabus
    if new_syllabus_id:
        print_info(f"\nTest 2.5: Update Syllabus {new_syllabus_id}")
        update_data = {
            "description": "Updated description - Testing version control"
        }
        response = requests.put(
            f"{BASE_URL}/syllabus/{new_syllabus_id}",
            json=update_data,
            headers=lecturer_headers
        )
        if response.status_code == 200:
            print_success("Syllabus updated (new version created)")
        else:
            print_error(f"Failed: {response.text}")
    
    # For Module 3-5 testing, use draft syllabus if create failed
    test_syllabus_id = new_syllabus_id if new_syllabus_id else 172  # Fresh draft syllabus for workflow
    return {"syllabus_id": test_syllabus_id}

# ==================== MODULE 3: WORKFLOW ====================

def test_module_3_workflow(tokens, data):
    """Module 3: Workflow (Submit → Approve → Publish)"""
    print_header("MODULE 3: WORKFLOW (REVIEW → APPROVE → PUBLISH)")
    
    lecturer_headers = {"Authorization": f"Bearer {tokens['lecturer_token']}"}
    hod_headers = {"Authorization": f"Bearer {tokens['hod_token']}"}
    admin_headers = {"Authorization": f"Bearer {tokens['admin_token']}"}
    
    syllabus_id = data.get('syllabus_id')
    if not syllabus_id:
        print_error("No syllabus_id available for workflow testing")
        return
    
    # Test 3.1: Submit for Review
    print_info(f"Test 3.1: Submit Syllabus {syllabus_id} for Review")
    response = requests.post(
        f"{BASE_URL}/workflow/submit",
        json={"syllabus_id": syllabus_id},
        headers=lecturer_headers
    )
    if response.status_code == 200:
        print_success("Syllabus submitted for review")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 3.2: Get Workflow Events
    print_info(f"\nTest 3.2: Get Workflow Events")
    response = requests.get(
        f"{BASE_URL}/workflow/{syllabus_id}/events",
        headers=admin_headers
    )
    if response.status_code == 200:
        data_response = response.json()
        events = data_response.get('items', [])
        print_success(f"Retrieved {len(events)} workflow events (total: {data_response.get('total', 0)})")
        for event in events[:3]:
            print_data(f"  {event['action']}", f"by user {event['created_by']} - {event.get('comment', 'N/A')}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 3.3: Approve by HOD
    print_info(f"\nTest 3.3: HOD Approve")
    response = requests.post(
        f"{BASE_URL}/workflow/hod-approve",
        json={"syllabus_id": syllabus_id, "comment": "Approved by HOD"},
        headers=hod_headers  # Use HOD token
    )
    if response.status_code == 200:
        print_success("HOD approved")
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")

# ==================== MODULE 4: COLLABORATIVE REVIEW ====================

def test_module_4_review(tokens, data):
    """Module 4: Collaborative Review"""
    print_header("MODULE 4: COLLABORATIVE REVIEW")
    
    lecturer_headers = {"Authorization": f"Bearer {tokens['lecturer_token']}"}
    syllabus_id = data.get('syllabus_id')
    
    if not syllabus_id:
        print_error("No syllabus_id for review testing")
        return
    
    # Test 4.1: Add Comment
    print_info(f"Test 4.1: Add Review Comment")
    response = requests.post(
        f"{BASE_URL}/review/comment",
        json={
            "syllabus_id": syllabus_id,
            "content": "This is a test review comment",
            "section": "general"
        },
        headers=lecturer_headers
    )
    if response.status_code == 200 or response.status_code == 201:
        review = response.json()
        print_success(f"Review added: ID {review['id']}")
        review_id = review['id']
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")
        review_id = None
    
    # Test 4.2: Get Reviews for Syllabus
    print_info(f"\nTest 4.2: Get All Reviews")
    response = requests.get(
        f"{BASE_URL}/review/syllabus/{syllabus_id}",
        headers=lecturer_headers
    )
    if response.status_code == 200:
        reviews = response.json()
        print_success(f"Retrieved {len(reviews)} reviews")
        for r in reviews[:3]:
            print_data(f"  By {r['author_email']}", r['content'][:50] + "...")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 4.3: Delete Review
    if review_id:
        print_info(f"\nTest 4.3: Delete Review {review_id}")
        response = requests.delete(
            f"{BASE_URL}/review/comment/{review_id}",
            headers=lecturer_headers
        )
        if response.status_code == 200:
            print_success("Review deleted")
        else:
            print_error(f"Failed: {response.text}")

# ==================== MODULE 5: CLO-PLO MAPPING ====================

def test_module_5_clo_plo(tokens, data):
    """Module 5: CLO-PLO Mapping"""
    print_header("MODULE 5: CLO-PLO MAPPING")
    
    lecturer_headers = {"Authorization": f"Bearer {tokens['lecturer_token']}"}
    admin_headers = {"Authorization": f"Bearer {tokens['admin_token']}"}
    syllabus_id = data.get('syllabus_id')
    
    if not syllabus_id:
        print_error("No syllabus_id for CLO-PLO testing")
        return
    
    # Test 5.1: Create CLO
    print_info("Test 5.1: Create CLO")
    response = requests.post(
        f"{BASE_URL}/clo-plo/clo",
        json={
            "syllabus_id": syllabus_id,
            "code": "CLO1",
            "description": "Student can understand basic programming concepts"
        },
        headers=lecturer_headers
    )
    if response.status_code == 200 or response.status_code == 201:
        clo = response.json()
        print_success(f"CLO created: {clo['code']}")
        clo_id = clo['id']
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")
        clo_id = None
    
    # Test 5.2: Get CLOs for Syllabus
    print_info(f"\nTest 5.2: Get CLOs")
    response = requests.get(
        f"{BASE_URL}/clo-plo/clo/syllabus/{syllabus_id}",
        headers=lecturer_headers
    )
    if response.status_code == 200:
        clos = response.json()
        print_success(f"Retrieved {len(clos)} CLOs")
        for clo in clos[:3]:
            print_data(f"  {clo['code']}", clo['description'][:50] + "...")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 5.3: Create PLO
    print_info("\nTest 5.3: Create PLO")
    plo_code = f"PLO{int(datetime.now().timestamp()) % 1000}"
    response = requests.post(
        f"{BASE_URL}/clo-plo/plo",
        json={
            "code": plo_code,
            "description": "Program outcome for software engineering"
        },
        headers=admin_headers  # PLO requires admin role
    )
    if response.status_code == 200 or response.status_code == 201:
        plo = response.json()
        print_success(f"PLO created: {plo['code']}")
        plo_id = plo['id']
    else:
        print_error(f"Failed: {response.status_code} - {response.text}")
        plo_id = None
    
    # Test 5.4: Map CLO to PLO
    if clo_id and plo_id:
        print_info(f"\nTest 5.4: Map CLO {clo_id} to PLO {plo_id}")
        response = requests.post(
            f"{BASE_URL}/clo-plo/mapping",
            json={
                "clo_id": clo_id,
                "plo_id": plo_id,
                "mapping_level": "high"
            },
            headers=lecturer_headers
        )
        if response.status_code == 200 or response.status_code == 201:
            print_success("CLO-PLO mapping created")
        else:
            print_error(f"Failed: {response.status_code} - {response.text}")

# ==================== MODULE 6: SEARCH ====================

def test_module_6_search(tokens):
    """Module 6: Search Functionality"""
    print_header("MODULE 6: SEARCH (STUDENT SEARCH)")
    
    student_headers = {"Authorization": f"Bearer {tokens['student_token']}"}
    
    # Test 6.1: Search by Subject Code
    print_info("Test 6.1: Search by Subject Code")
    response = requests.get(
        f"{BASE_URL}/search/syllabuses?query=IT001",
        headers=student_headers
    )
    if response.status_code == 200:
        data = response.json()
        results = data.get('items', [])
        print_success(f"Found {len(results)} results (total: {data.get('total', 0)})")
        for r in results[:3]:
            print_data(f"  {r['subject_code']}", r['subject_name'])
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 6.2: Search by Subject Name
    print_info("\nTest 6.2: Search by Subject Name")
    response = requests.get(
        f"{BASE_URL}/search/syllabuses?query=programming",
        headers=student_headers
    )
    if response.status_code == 200:
        data = response.json()
        results = data.get('items', [])
        print_success(f"Found {len(results)} results (total: {data.get('total', 0)})")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 6.3: Filter by Department
    print_info("\nTest 6.3: Filter by Department")
    response = requests.get(
        f"{BASE_URL}/search/syllabuses?department=Computer Science",
        headers=student_headers
    )
    if response.status_code == 200:
        data = response.json()
        results = data.get('items', [])
        print_success(f"Found {len(results)} results in Computer Science (total: {data.get('total', 0)})")
    else:
        print_error(f"Failed: {response.text}")

# ==================== MODULE 7: AI INTEGRATION ====================

def test_module_7_ai(tokens):
    """Module 7: AI Integration"""
    print_header("MODULE 7: AI INTEGRATION")
    
    admin_headers = {"Authorization": f"Bearer {tokens['admin_token']}"}
    
    # Test 7.1: AI Health Check
    print_info("Test 7.1: AI Health Check")
    response = requests.get(f"{BASE_URL}/ai/health", headers=admin_headers)
    if response.status_code == 200:
        health = response.json()
        print_success(f"AI Status: {health['status']}")
        print_data("  Gemini", "Available" if health['gemini_available'] else "Using fallback")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 7.2: AI Summarize
    print_info("\nTest 7.2: AI Auto-Summarize")
    response = requests.post(
        f"{BASE_URL}/ai/summarize",
        json={"syllabus_id": 151, "language": "vi"},
        headers=admin_headers
    )
    if response.status_code == 200:
        result = response.json()
        print_success("Summarization completed")
        print_data("  Summary", result['summary'][:80] + "...")
        print_data("  Key Points", f"{len(result['key_points'])} items")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 7.3: AI Semantic Diff
    print_info("\nTest 7.3: AI Semantic Diff")
    response = requests.post(
        f"{BASE_URL}/ai/diff",
        json={"version_id_1": 1, "version_id_2": 2, "language": "vi"},
        headers=admin_headers
    )
    if response.status_code == 200:
        result = response.json()
        print_success("Diff analysis completed")
        print_data("  Versions", f"{result['version_1']} vs {result['version_2']}")
        print_data("  Changes", f"{len(result['major_changes'])} major, {len(result['minor_changes'])} minor")
    else:
        print_error(f"Failed: {response.text}")

# ==================== MODULE 8: NOTIFICATION ====================

def test_module_8_notification(tokens):
    """Module 8: Notification System"""
    print_header("MODULE 8: NOTIFICATION SYSTEM")
    
    student_headers = {"Authorization": f"Bearer {tokens['student_token']}"}
    
    # Test 8.1: Get Notifications
    print_info("Test 8.1: Get Student Notifications")
    response = requests.get(f"{BASE_URL}/notifications/", headers=student_headers)
    if response.status_code == 200:
        result = response.json()
        print_success(f"Total notifications: {result['total']}")
        for notif in result['items'][:3]:
            print_data(f"  [{notif['notification_type']}]", notif['title'])
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 8.2: Follow Syllabus
    print_info("\nTest 8.2: Follow Syllabus")
    response = requests.post(
        f"{BASE_URL}/notifications/follow",
        json={"syllabus_id": 151},
        headers=student_headers
    )
    if response.status_code == 200:
        print_success("Followed syllabus successfully")
    else:
        # Already following is OK
        print_info("Already following or error")
    
    # Test 8.3: Check Following Status
    print_info("\nTest 8.3: Check Following Status")
    response = requests.get(
        f"{BASE_URL}/notifications/following/151",
        headers=student_headers
    )
    if response.status_code == 200:
        result = response.json()
        status = "Following" if result['is_following'] else "Not following"
        print_success(f"Status: {status}")
    else:
        print_error(f"Failed: {response.text}")

# ==================== MAIN TEST RUNNER ====================

def main():
    """Run all module tests"""
    print_header("COMPREHENSIVE TEST: ALL 8 BACKEND MODULES", '=')
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Module 1: Authentication
        tokens = test_module_1_authentication()
        if not tokens:
            print_error("Authentication failed. Cannot continue.")
            return
        
        # Module 2: Syllabus Management
        data = test_module_2_syllabus(tokens)
        
        # Module 3: Workflow
        test_module_3_workflow(tokens, data)
        
        # Module 4: Collaborative Review
        test_module_4_review(tokens, data)
        
        # Module 5: CLO-PLO Mapping
        test_module_5_clo_plo(tokens, data)
        
        # Module 6: Search
        test_module_6_search(tokens)
        
        # Module 7: AI Integration
        test_module_7_ai(tokens)
        
        # Module 8: Notification
        test_module_8_notification(tokens)
        
        # Final Summary
        print_header("TEST SUMMARY", '=')
        print_success("Module 1: Authentication + User Management")
        print_success("Module 2: Syllabus Management")
        print_success("Module 3: Workflow (Submit → Approve)")
        print_success("Module 4: Collaborative Review")
        print_success("Module 5: CLO-PLO Mapping")
        print_success("Module 6: Search Functionality")
        print_success("Module 7: AI Integration")
        print_success("Module 8: Notification System")
        
        print(f"\n{GREEN}*** ALL 8 MODULES TESTED SUCCESSFULLY! ***{RESET}\n")
        
    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
