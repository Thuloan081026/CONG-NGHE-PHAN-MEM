#!/usr/bin/env python
"""Test syllabuses for lecturer@edu.vn"""
import requests

API_URL = "http://localhost:8000"

# Login
print("🔐 Logging in as lecturer@edu.vn...")
login_data = {
    "email": "lecturer@edu.vn",
    "password": "lecturer123"
}

login_resp = requests.post(f"{API_URL}/auth/login", json=login_data)
if login_resp.status_code != 200:
    print(f"❌ Login failed: {login_resp.text}")
    exit(1)

login_result = login_resp.json()
token = login_result.get('access_token')
user = login_result.get('user', {})

print(f"✅ Login OK: {user.get('full_name')} ({user.get('email')})")

# Get syllabuses
print("\n📚 Fetching syllabuses...")
headers = {"Authorization": f"Bearer {token}"}
syllabus_resp = requests.get(f"{API_URL}/syllabus/?skip=0&limit=10", headers=headers)

if syllabus_resp.status_code != 200:
    print(f"❌ Failed: {syllabus_resp.text}")
    exit(1)

data = syllabus_resp.json()
print(f"✅ Total: {data['total']} syllabuses")
print(f"\nSyllabuses for {user.get('full_name')}:\n")

print(f"{'Code':<10} {'Subject Name':<35} {'Credits':<8} {'Status':<12}")
print("-" * 70)

for syl in data['items']:
    print(f"{syl['subject_code']:<10} {syl['subject_name']:<35} {syl['credits']:<8} {syl['status']:<12}")

print(f"\n✨ Tất cả dữ liệu sẵn sàng! Hãy refresh trang trong browser.")
