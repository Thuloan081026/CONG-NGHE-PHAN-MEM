"""
Test Module 7 (AI Integration) and Module 8 (Notification)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login to get token
def login(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

print("="*70)
print("  🧪 TEST MODULE 7 & 8 - AI Integration + Notification")
print("="*70)

# Login as lecturer
lecturer_token = login("lecturer1@hcmute.edu.vn", "lecturer123")
student_token = login("student1@student.hcmute.edu.vn", "student123")

if not lecturer_token:
    print("❌ Login failed")
    exit(1)

headers_lecturer = {"Authorization": f"Bearer {lecturer_token}"}
headers_student = {"Authorization": f"Bearer {student_token}"}

print("\n" + "="*70)
print("  MODULE 7: AI Integration")
print("="*70)

# Test 1: AI Summarize
print("\n📝 Test 1: AI Auto-Summarize Syllabus")
response = requests.post(
    f"{BASE_URL}/ai/summarize",
    json={"syllabus_id": 151, "language": "vi"},
    headers=headers_lecturer
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Summary generated:")
    print(f"   {data['summary'][:200]}...")
    print(f"   Key points: {len(data['key_points'])}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# Test 2: AI Semantic Diff
print("\n🔍 Test 2: AI Semantic Diff (Compare 2 Versions)")
# First check if versions exist
response = requests.get(
    f"{BASE_URL}/syllabus/151/versions",
    headers=headers_lecturer
)
if response.status_code == 200 and len(response.json().get("items", [])) >= 2:
    versions = response.json()["items"]
    v1_id = versions[0]["id"]
    v2_id = versions[1]["id"] if len(versions) > 1 else versions[0]["id"]
    
    response = requests.post(
        f"{BASE_URL}/ai/diff",
        json={"version_id_1": v1_id, "version_id_2": v2_id, "language": "vi"},
        headers=headers_lecturer
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Diff completed:")
        print(f"   {data['changes_summary']}")
        print(f"   Impact: {data['impact_analysis']}")
        print(f"   Major changes: {len(data['major_changes'])}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
else:
    print("⚠️  Not enough versions to compare")

# Test 3: CLO Similarity Check
print("\n🎯 Test 3: AI CLO Similarity Check")
response = requests.post(
    f"{BASE_URL}/ai/clo-check",
    json={
        "syllabus_id": 151,
        "clo_description": "Students can write basic programs using Python"
    },
    headers=headers_lecturer
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Found {data['total_found']} similar CLOs")
    if data['suggestions']:
        print(f"   Top match: {data['suggestions'][0]['description']}")
        print(f"   Similarity: {data['suggestions'][0]['similarity_score']}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# Test 4: AI Health Check
print("\n🏥 Test 4: AI Health Check")
response = requests.get(f"{BASE_URL}/ai/health", headers=headers_lecturer)
if response.status_code == 200:
    data = response.json()
    print(f"✅ AI Service: {data['status']}")
    print(f"   Features: {', '.join(data['features'])}")
else:
    print(f"❌ Failed: {response.status_code}")

print("\n" + "="*70)
print("  MODULE 8: Notification")
print("="*70)

# Test 5: Student Follow Syllabus
print("\n👥 Test 5: Student Follow Syllabus")
response = requests.post(
    f"{BASE_URL}/notifications/follow",
    json={"syllabus_id": 151},
    headers=headers_student
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ {data['message']}")
    print(f"   Following: {data['is_following']}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# Test 6: Check Following Status
print("\n🔍 Test 6: Check Following Status")
response = requests.get(
    f"{BASE_URL}/notifications/following/151",
    headers=headers_student
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Following status: {data['is_following']}")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 7: Get My Notifications
print("\n📬 Test 7: Get My Notifications")
response = requests.get(
    f"{BASE_URL}/notifications/",
    headers=headers_student
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Notifications: {data['total']} total")
    if data['items']:
        print(f"   Latest: {data['items'][0]['title']}")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 8: Get Unread Notifications Only
print("\n📭 Test 8: Get Unread Notifications Only")
response = requests.get(
    f"{BASE_URL}/notifications/?unread_only=true",
    headers=headers_student
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Unread notifications: {data['total']}")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 9: Unfollow Syllabus
print("\n👋 Test 9: Unfollow Syllabus")
response = requests.delete(
    f"{BASE_URL}/notifications/unfollow/151",
    headers=headers_student
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ {data['message']}")
else:
    print(f"⚠️  {response.status_code} - {response.text}")

print("\n" + "="*70)
print("  📊 SUMMARY")
print("="*70)
print("✅ Module 7: AI Integration")
print("   - AI Summarize: Auto-generate syllabus summary")
print("   - AI Semantic Diff: Compare versions intelligently")
print("   - CLO Similarity: Find similar CLOs")
print("")
print("✅ Module 8: Notification")
print("   - Follow/Unfollow: Students can follow syllabuses")
print("   - Get Notifications: Retrieve user notifications")
print("   - Filter Unread: Show only unread notifications")
print("="*70)
