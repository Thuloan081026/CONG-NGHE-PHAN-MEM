#!/usr/bin/env python
"""Test lecturer API response"""
import requests
import json

API_URL = "http://localhost:8000"

# Login
login_data = {
    "email": "lecturer1@hcmute.edu.vn",
    "password": "lecturer123"
}

print("🔐 Logging in...")
login_resp = requests.post(f"{API_URL}/auth/login", json=login_data)
print(f"Login status: {login_resp.status_code}")

if login_resp.status_code != 200:
    print(f"Login failed: {login_resp.text}")
    exit(1)

login_data = login_resp.json()
token = login_data.get('access_token')
print(f"✅ Token obtained: {token[:20]}...")

# Get syllabuses
print("\n📚 Getting syllabuses...")
headers = {"Authorization": f"Bearer {token}"}
syllabus_resp = requests.get(f"{API_URL}/syllabus/?skip=0&limit=10", headers=headers)
print(f"Syllabus status: {syllabus_resp.status_code}")

if syllabus_resp.status_code != 200:
    print(f"Failed: {syllabus_resp.text}")
    exit(1)

syllabus_data = syllabus_resp.json()
print(f"\n✅ Response structure:")
print(f"  Keys: {list(syllabus_data.keys())}")
print(f"  Total: {syllabus_data.get('total')}")
print(f"  Count: {syllabus_data.get('count')}")
print(f"  Items: {len(syllabus_data.get('items', []))}")

if syllabus_data.get('items'):
    print(f"\n✅ First 3 syllabuses:")
    for s in syllabus_data['items'][:3]:
        print(f"  - {s.get('subject_code')}: {s.get('subject_name')} (Status: {s.get('status')})")
else:
    print("\n❌ No items in response!")
    print(f"Full response: {json.dumps(syllabus_data, indent=2)}")
