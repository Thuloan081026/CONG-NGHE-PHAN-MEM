"""Quick test to debug syllabus create endpoint"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Login as lecturer
print("=== Login as Lecturer ===")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "lecturer@test.com",
        "password": "lecturer123"
    }
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
print(f"✓ Login successful")

headers = {"Authorization": f"Bearer {token}"}

# Create new syllabus
print("\n=== Create New Syllabus ===")
new_syllabus = {
    "subject_code": f"TEST{int(datetime.now().timestamp()) % 10000}",
    "subject_name": "Test Subject",
    "credits": 3,
    "semester": 1,
    "department": "Test Department",
    "description": "Test syllabus for debugging",
    "content": "Test content for syllabus"
}

print(f"Sending: {json.dumps(new_syllabus, indent=2)}")

response = requests.post(
    f"{BASE_URL}/syllabus/",
    json=new_syllabus,
    headers=headers
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print(f"\n✓ Syllabus created successfully!")
    created = response.json()
    print(f"  ID: {created['id']}")
    print(f"  Code: {created['subject_code']}")
    print(f"  Name: {created['subject_name']}")
else:
    print(f"\n✗ Failed to create syllabus")
