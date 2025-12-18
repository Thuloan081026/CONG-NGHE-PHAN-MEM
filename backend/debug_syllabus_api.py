"""Debug syllabus creation API"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Login as lecturer
print("=== Login as Lecturer ===")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "lecturer@test.com", "password": "lecturer123"}
)

if response.status_code != 200:
    print(f"Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"✓ Login successful")

headers = {"Authorization": f"Bearer {token}"}

# Generate unique code
timestamp = int(datetime.now().timestamp())

# Test: Create syllabus
print("\n=== Test: Create Syllabus ===")
syllabus_data = {
    "subject_code": f"TEST{timestamp % 10000}",
    "subject_name": "Test Subject",
    "credits": 3,
    "semester": 1,
    "department": "CS",
    "description": "Test description"
}
print(f"Payload: {json.dumps(syllabus_data, indent=2)}")
response = requests.post(f"{BASE_URL}/syllabus/", json=syllabus_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 201 or response.status_code == 200:
    print("\n✅ SUCCESS! Syllabus created successfully!")
    created = response.json()
    print(f"  ID: {created['id']}")
    print(f"  Code: {created['subject_code']}")
    print(f"  Status: {created['status']}")
else:
    print("\n❌ FAILED!")
