"""
Test thủ công 6 modules bằng cách gọi API trực tiếp
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("="*70)
print("🧪 MANUAL API TEST - 6 MODULES BACKEND")
print("="*70)

# Module 1: Authentication + User Management
print("\n📌 MODULE 1: Authentication + User Management")
print("-"*70)

# Test login
print("\n1. Test POST /auth/login...")
response = client.post("/auth/login", json={
    "email": "admin@hcmute.edu.vn",
    "password": "admin123"
})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    admin_token = data["access_token"]
    print(f"   ✅ Login successful")
    print(f"   User: {data.get('user', {}).get('email')}")
    print(f"   Role: {data.get('user', {}).get('role')}")
else:
    print(f"   ❌ Login failed: {response.text}")
    admin_token = None

# Test get users
if admin_token:
    print("\n2. Test GET /users (admin only)...")
    response = client.get("/users", headers={"Authorization": f"Bearer {admin_token}"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"   ✅ Found {len(users)} users")
        for u in users[:3]:
            print(f"      - {u.get('email')} ({u.get('role')})")
    else:
        print(f"   ❌ Failed: {response.text}")

# Module 2: Syllabus Management
print("\n\n📌 MODULE 2: Syllabus Management")
print("-"*70)

# Login as lecturer
print("\n1. Login as lecturer...")
response = client.post("/auth/login", json={
    "email": "lecturer1@hcmute.edu.vn",
    "password": "lecturer123"
})
if response.status_code == 200:
    lecturer_token = response.json()["access_token"]
    print("   ✅ Lecturer login successful")
else:
    print(f"   ❌ Failed: {response.text}")
    lecturer_token = None

# Test get syllabuses
if lecturer_token:
    print("\n2. Test GET /syllabus...")
    response = client.get("/syllabus", headers={"Authorization": f"Bearer {lecturer_token}"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found syllabuses")
        syllabuses = data.get('items', data) if isinstance(data, dict) else data
        for s in (syllabuses[:3] if isinstance(syllabuses, list) else []):
            print(f"      - [{s.get('course_code')}] {s.get('course_name')}")
    else:
        print(f"   ❌ Failed: {response.text}")

# Module 3: Workflow
print("\n\n📌 MODULE 3: Workflow (Submit → Approve → Publish)")
print("-"*70)
print("   ℹ️  Workflow APIs available:")
print("      POST /workflow/submit")
print("      POST /workflow/hod-approve")
print("      POST /workflow/aa-approve")
print("      POST /workflow/final-approve")

# Module 4: Collaborative Review
print("\n\n📌 MODULE 4: Collaborative Review")
print("-"*70)

if lecturer_token:
    print("\n1. Test GET /review/syllabus/{id}...")
    # Get first syllabus
    response = client.get("/syllabus", headers={"Authorization": f"Bearer {lecturer_token}"})
    if response.status_code == 200:
        data = response.json()
        syllabuses = data.get('items', data) if isinstance(data, dict) else data
        if syllabuses and len(syllabuses) > 0:
            syllabus_id = syllabuses[0].get('id')
            
            response = client.get(f"/review/syllabus/{syllabus_id}", 
                                headers={"Authorization": f"Bearer {lecturer_token}"})
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                reviews = response.json()
                print(f"   ✅ Found {len(reviews)} reviews")
            else:
                print(f"   ℹ️  No reviews yet or error: {response.text[:100]}")

# Module 5: CLO-PLO Mapping
print("\n\n📌 MODULE 5: CLO-PLO Mapping")
print("-"*70)

if lecturer_token:
    print("\n1. Test GET /clo-plo/clo...")
    response = client.get("/clo-plo/clo", headers={"Authorization": f"Bearer {lecturer_token}"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        clos = response.json()
        print(f"   ✅ Found {len(clos)} CLOs")
        for clo in clos[:3]:
            print(f"      - {clo.get('code')}: {clo.get('description', '')[:50]}...")
    else:
        print(f"   ❌ Failed: {response.text[:100]}")
    
    print("\n2. Test GET /clo-plo/plo...")
    response = client.get("/clo-plo/plo", headers={"Authorization": f"Bearer {lecturer_token}"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        plos = response.json()
        print(f"   ✅ Found {len(plos)} PLOs")
        for plo in plos[:3]:
            print(f"      - {plo.get('code')}: {plo.get('description', '')[:50]}...")
    else:
        print(f"   ❌ Failed: {response.text[:100]}")

# Module 6: Search
print("\n\n📌 MODULE 6: Search")
print("-"*70)

if lecturer_token:
    print("\n1. Test GET /search?q=programming...")
    response = client.get("/search?q=programming", 
                        headers={"Authorization": f"Bearer {lecturer_token}"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"   ✅ Search working, found {len(results)} results")
    else:
        print(f"   ❌ Failed: {response.text[:100]}")

print("\n" + "="*70)
print("✅ MANUAL API TEST COMPLETED")
print("="*70)
