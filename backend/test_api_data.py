"""
Test API to verify data is being returned
"""
import requests
import json
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import create_access_token
from app.models.syllabus import Syllabus

# Get a lecturer user for auth - use lecturer1
db = SessionLocal()
lecturer = db.query(User).filter(User.email == "lecturer1@hcmute.edu.vn").first()
if not lecturer:
    # Fallback to first lecturer
    lecturer = db.query(User).filter(User.role == "lecturer").first()
db.close()

if not lecturer:
    print("❌ No lecturer found in database!")
    exit(1)

print(f"✓ Found lecturer: {lecturer.full_name} ({lecturer.email})")

# Create a token for this user
token = create_access_token(subject=str(lecturer.id))
print(f"✓ Token created: {token[:20]}...")

# Test API endpoints
API_URL = "http://localhost:8000"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test 1: GET /users/me
print("\n[TEST 1] GET /users/me")
res = requests.get(f"{API_URL}/users/me", headers=headers)
print(f"Status: {res.status_code}")
if res.ok:
    user_data = res.json()
    print(f"✓ User: {user_data.get('full_name')} ({user_data.get('email')})")
else:
    print(f"❌ Error: {res.text}")

# Test 2: GET /syllabus/
print("\n[TEST 2] GET /syllabus/")
res = requests.get(f"{API_URL}/syllabus/", headers=headers)
print(f"Status: {res.status_code}")
if res.ok:
    data = res.json()
    print(f"Response keys: {data.keys() if isinstance(data, dict) else 'list'}")
    if isinstance(data, dict):
        print(f"Total syllabuses: {data.get('total')}")
        print(f"Items count: {len(data.get('items', []))}")
        if data.get('items'):
            first = data['items'][0]
            print(f"First syllabus: {first.get('subject_code')} - {first.get('subject_name')}")
    elif isinstance(data, list):
        print(f"Syllabuses list length: {len(data)}")
        if data:
            print(f"First: {data[0]}")
else:
    print(f"❌ Error: {res.text}")

# Test 3: GET /notifications
print("\n[TEST 3] GET /notifications")
res = requests.get(f"{API_URL}/notifications", headers=headers)
print(f"Status: {res.status_code}")
if res.ok:
    data = res.json()
    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'list'}")
    if isinstance(data, dict):
        print(f"Total notifications: {data.get('total')}")
        print(f"Items count: {len(data.get('items', []))}")
        if data.get('items'):
            first = data['items'][0]
            print(f"First notification: {first.get('title')}")
    else:
        print(f"Notifications list: {len(data)}")
else:
    print(f"❌ Error: {res.text}")

# Test 4: Check database directly
print("\n[TEST 4] Database check")
db = SessionLocal()
try:
    lec_count = db.query(User).filter(User.role == "lecturer").count()
    syl_count = db.query(Syllabus).count()
    print(f"✓ Lecturers in DB: {lec_count}")
    print(f"✓ Syllabuses in DB: {syl_count}")
finally:
    db.close()

print("\n✨ Tests completed!")
