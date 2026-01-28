#!/usr/bin/env python3
"""
Full integration test for Principal login to dashboard
"""
import requests
import time

print("=" * 70)
print("FULL PRINCIPAL LOGIN FLOW TEST")
print("=" * 70)

# Step 1: Test login API
print("\n[STEP 1] Test Login API")
print("-" * 70)

try:
    response = requests.post('http://localhost:8000/auth/login', 
        json={'email': 'principal@edu.vn', 'password': 'principal123'},
        timeout=5
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed with status {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
    data = response.json()
    token = data.get('access_token')
    user = data.get('user', {})
    role = user.get('role')
    
    print(f"✅ Login successful")
    print(f"   Email: {user.get('email')}")
    print(f"   Role: {role}")
    print(f"   Full Name: {user.get('full_name')}")
    print(f"   Token: {token[:40]}...")
    
    if role != 'principal':
        print(f"❌ Wrong role! Expected 'principal', got '{role}'")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 2: Test /users/me
print("\n[STEP 2] Test /users/me Endpoint")
print("-" * 70)

try:
    response = requests.get('http://localhost:8000/users/me',
        headers={'Authorization': f'Bearer {token}'},
        timeout=5
    )
    
    if response.status_code != 200:
        print(f"❌ /users/me failed with status {response.status_code}")
        exit(1)
    
    user_data = response.json()
    print(f"✅ /users/me successful")
    print(f"   Role: {user_data.get('role')}")
    print(f"   Email: {user_data.get('email')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 3: Test frontend assets
print("\n[STEP 3] Test Frontend Assets")
print("-" * 70)

try:
    # Test index.html
    response = requests.get('http://localhost:3000/index.html', timeout=5)
    if response.status_code != 200:
        print(f"❌ index.html returned {response.status_code}")
        exit(1)
    
    content = response.text
    if "'principal': 'principal-web/dashboard.html'" not in content:
        print("❌ index.html missing principal mapping")
        exit(1)
    
    if "console.log('User role type':" not in content:
        print("❌ index.html missing debug logging")
        exit(1)
    
    print(f"✅ index.html OK ({len(content)} bytes)")
    
    # Test principal dashboard
    response = requests.get('http://localhost:3000/principal-web/dashboard.html', timeout=5)
    if response.status_code != 200:
        print(f"❌ principal-web/dashboard.html returned {response.status_code}")
        exit(1)
    
    print(f"✅ principal-web/dashboard.html OK ({len(response.content)} bytes)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 4: Test redirect logic
print("\n[STEP 4] Test Redirect Logic")
print("-" * 70)

dashboardMap = {
    'admin': 'admin-web/html/dashboard.html',
    'lecturer': 'lecturer-web/dashboard.html',
    'hod': 'hod-web/dashboard.html',
    'academic_affairs': 'academic-affairs-web/dashboard.html',
    'student': 'student-web/dashboard.html',
    'principal': 'principal-web/dashboard.html',
    'reviewer': 'reviewer-web/dashboard.html',
    'user': 'user-web/dashboard.html'
}

role = user.get('role')
redirectUrl = dashboardMap.get(role)

if not redirectUrl:
    print(f"❌ Role '{role}' not found in dashboard map!")
    exit(1)

print(f"✅ Role '{role}' maps to: {redirectUrl}")

# Verify the dashboard URL exists
response = requests.get(f'http://localhost:3000/{redirectUrl}', timeout=5)
if response.status_code != 200:
    print(f"❌ Dashboard URL returned {response.status_code}")
    exit(1)

print(f"✅ Dashboard URL is accessible")

# Final summary
print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\n📌 Login Flow Summary:")
print(f"   1. User: {user.get('email')}")
print(f"   2. Password: principal123")
print(f"   3. Role: {role}")
print(f"   4. Dashboard: {redirectUrl}")
print(f"   5. Full URL: http://localhost:3000/{redirectUrl}")
print("\n✨ System is ready for principal login!")
