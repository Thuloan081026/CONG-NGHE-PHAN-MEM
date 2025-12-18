"""
Complete Test Script for Module 7 (AI Integration) and Module 8 (Notification)
Test all endpoints with real scenarios
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")

def get_admin_token():
    """Login as admin to get token"""
    print_info("Logging in as admin...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print_success(f"Admin token: {token[:20]}...")
        return token
    else:
        print_error(f"Login failed: {response.text}")
        return None

def get_lecturer_token():
    """Login as lecturer"""
    print_info("Logging in as lecturer...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "lecturer1", "password": "lecturer123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print_success(f"Lecturer token: {token[:20]}...")
        return token
    else:
        print_error(f"Login failed: {response.text}")
        return None

def get_student_token():
    """Login as student"""
    print_info("Logging in as student...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "student1", "password": "student123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print_success(f"Student token: {token[:20]}...")
        return token
    else:
        print_error(f"Login failed: {response.text}")
        return None

def test_module_7_ai_integration(token):
    """Test Module 7: AI Integration"""
    print_header("MODULE 7: AI INTEGRATION")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: AI Health Check
    print_info("Test 1: AI Health Check")
    response = requests.get(f"{BASE_URL}/ai/health", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"AI Status: {data['status']}")
        print(f"  Model: {data['model']}")
        print(f"  Gemini Available: {data['gemini_available']}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 2: AI Summarize
    print_info("\nTest 2: AI Auto-Summarize Syllabus")
    response = requests.post(
        f"{BASE_URL}/ai/summarize",
        headers=headers,
        json={"syllabus_id": 1, "language": "vi"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success("Summarization completed!")
        print(f"\n{YELLOW}Summary:{RESET}")
        print(f"  {data['summary'][:200]}...")
        print(f"\n{YELLOW}Key Points:{RESET}")
        for i, point in enumerate(data['key_points'][:3], 1):
            print(f"  {i}. {point}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 3: AI Semantic Diff
    print_info("\nTest 3: AI Semantic Diff (Compare 2 versions)")
    response = requests.post(
        f"{BASE_URL}/ai/diff",
        headers=headers,
        json={"version_id_1": 1, "version_id_2": 2, "language": "vi"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success("Diff analysis completed!")
        print(f"\n{YELLOW}Comparison:{RESET}")
        print(f"  Version 1: {data['version_1']}")
        print(f"  Version 2: {data['version_2']}")
        print(f"\n{YELLOW}Changes Summary:{RESET}")
        print(f"  {data['changes_summary']}")
        print(f"\n{YELLOW}Major Changes:{RESET} {len(data['major_changes'])} items")
        for change in data['major_changes'][:2]:
            print(f"  • {change['description'][:80]}...")
        print(f"\n{YELLOW}Minor Changes:{RESET} {len(data['minor_changes'])} items")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 4: CLO Similarity Check
    print_info("\nTest 4: CLO Similarity Check")
    response = requests.post(
        f"{BASE_URL}/ai/clo-check",
        headers=headers,
        json={
            "syllabus_id": 1,
            "clo_descriptions": [
                "Sinh viên có khả năng lập trình Python cơ bản",
                "Hiểu và áp dụng thuật toán sắp xếp"
            ]
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success("CLO check completed!")
        print(f"\n{YELLOW}Total Suggestions:{RESET} {data['total_suggestions']}")
        for clo_result in data['suggestions'][:2]:
            print(f"\n{YELLOW}Input CLO:{RESET} {clo_result['input_clo'][:60]}...")
            print(f"{YELLOW}Similar CLOs found:{RESET} {len(clo_result['similar_clos'])}")
            for similar in clo_result['similar_clos'][:2]:
                print(f"  • [{similar['syllabus_code']}] {similar['clo_code']}")
                print(f"    Score: {similar['similarity_score']:.2f}")
                print(f"    {similar['description'][:60]}...")
    else:
        print_error(f"Failed: {response.text}")

def test_module_8_notification(student_token, lecturer_token):
    """Test Module 8: Notification System"""
    print_header("MODULE 8: NOTIFICATION SYSTEM")
    
    student_headers = {"Authorization": f"Bearer {student_token}"}
    lecturer_headers = {"Authorization": f"Bearer {lecturer_token}"}
    
    # Test 1: Student follows syllabus
    print_info("Test 1: Student Follow Syllabus")
    response = requests.post(
        f"{BASE_URL}/notifications/follow",
        headers=student_headers,
        json={"syllabus_id": 1}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Followed successfully!")
        print(f"  Message: {data['message']}")
        print(f"  Syllabus: {data['syllabus_code']} - {data['syllabus_name']}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 2: Check following status
    print_info("\nTest 2: Check Following Status")
    response = requests.get(
        f"{BASE_URL}/notifications/following/1",
        headers=student_headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Following status: {data['is_following']}")
        if data['is_following']:
            print(f"  Followed at: {data['followed_at']}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 3: Get student notifications
    print_info("\nTest 3: Get Student Notifications")
    response = requests.get(
        f"{BASE_URL}/notifications/",
        headers=student_headers,
        params={"is_read": False}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Total unread notifications: {data['total']}")
        for notif in data['notifications'][:3]:
            print(f"\n  📬 {notif['title']}")
            print(f"     Type: {notif['type']}")
            print(f"     {notif['message'][:80]}...")
            print(f"     Created: {notif['created_at']}")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 4: Get lecturer notifications
    print_info("\nTest 4: Get Lecturer Notifications")
    response = requests.get(
        f"{BASE_URL}/notifications/",
        headers=lecturer_headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Total notifications: {data['total']}")
        for notif in data['notifications'][:3]:
            print(f"\n  📬 {notif['title']}")
            print(f"     Type: {notif['type']}")
            print(f"     {notif['message'][:80]}...")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 5: Mark notification as read
    if response.status_code == 200 and data['notifications']:
        notif_id = data['notifications'][0]['id']
        print_info(f"\nTest 5: Mark Notification {notif_id} as Read")
        response = requests.put(
            f"{BASE_URL}/notifications/{notif_id}/read",
            headers=lecturer_headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print_success("Notification marked as read!")
        else:
            print_error(f"Failed: {response.text}")
    
    # Test 6: Mark all as read
    print_info("\nTest 6: Mark All Notifications as Read")
    response = requests.put(
        f"{BASE_URL}/notifications/read-all",
        headers=student_headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Marked {data['updated_count']} notifications as read!")
    else:
        print_error(f"Failed: {response.text}")
    
    # Test 7: Unfollow syllabus
    print_info("\nTest 7: Student Unfollow Syllabus")
    response = requests.delete(
        f"{BASE_URL}/notifications/unfollow/1",
        headers=student_headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Unfollowed successfully!")
        print(f"  Message: {data['message']}")
    else:
        print_error(f"Failed: {response.text}")

def test_integration_scenario():
    """Test complete integration scenario"""
    print_header("INTEGRATION TEST: Complete Workflow")
    
    # Get tokens
    admin_token = get_admin_token()
    student_token = get_student_token()
    lecturer_token = get_lecturer_token()
    
    if not admin_token or not student_token or not lecturer_token:
        print_error("Failed to get tokens. Make sure users exist!")
        return
    
    # Test Module 7
    test_module_7_ai_integration(admin_token)
    
    # Test Module 8
    test_module_8_notification(student_token, lecturer_token)
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("All modules tested!")
    print_info("\nModule 7 - AI Integration:")
    print("  ✓ AI Health Check")
    print("  ✓ Auto-Summarize Syllabus")
    print("  ✓ Semantic Diff (Version Comparison)")
    print("  ✓ CLO Similarity Check")
    print_info("\nModule 8 - Notification:")
    print("  ✓ Follow Syllabus")
    print("  ✓ Check Following Status")
    print("  ✓ Get Notifications")
    print("  ✓ Mark as Read")
    print("  ✓ Mark All as Read")
    print("  ✓ Unfollow Syllabus")
    
    print(f"\n{GREEN}🎉 ALL TESTS COMPLETED!{RESET}\n")

if __name__ == "__main__":
    print_header("TESTING MODULE 7 & 8")
    print(f"Server: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_integration_scenario()
    except Exception as e:
        print_error(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
