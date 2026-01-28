#!/usr/bin/env python3
import requests
import json
import webbrowser
import time

print("=" * 60)
print("SMD SYSTEM - PRINCIPAL LOGIN FLOW TEST")
print("=" * 60)

# Step 1: Test login
print("\n[Step 1] Testing Principal Login...")
login_url = "http://localhost:8000/auth/login"
login_payload = {
    "email": "principal@edu.vn",
    "password": "principal123"
}

try:
    response = requests.post(login_url, json=login_payload)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.json()}")
        exit(1)
    
    data = response.json()
    token = data.get('access_token')
    user = data.get('user', {})
    
    print(f"✅ Login successful!")
    print(f"   Email: {user.get('email')}")
    print(f"   Role: {user.get('role')}")
    print(f"   Name: {user.get('full_name')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 2: Test /users/me
print("\n[Step 2] Testing /users/me endpoint...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    me_response = requests.get("http://localhost:8000/users/me", headers=headers)
    
    if me_response.status_code != 200:
        print(f"❌ /users/me failed: {me_response.status_code}")
        exit(1)
    
    user_data = me_response.json()
    print(f"✅ /users/me successful!")
    print(f"   Role: {user_data.get('role')}")
    print(f"   Email: {user_data.get('email')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 3: Test dashboard HTML
print("\n[Step 3] Testing Principal Dashboard URL...")
try:
    dashboard_response = requests.get("http://localhost:3000/principal-web/dashboard.html")
    
    if dashboard_response.status_code != 200:
        print(f"❌ Dashboard request failed: {dashboard_response.status_code}")
        exit(1)
    
    print(f"✅ Dashboard HTML loaded successfully!")
    print(f"   Content size: {len(dashboard_response.content)} bytes")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 4: Provide localStorage setup code
print("\n[Step 4] Setup instructions for browser test...")
print(f"✅ Token ready: {token[:50]}...")
print("\n📌 To test in browser:")
print("   1. Open: http://localhost:3000")
print("   2. Login with:")
print("      - Email: principal@edu.vn")
print("      - Password: principal123")
print("   3. You will be redirected to: http://localhost:3000/principal-web/dashboard.html")

# Test localStorage setup script
localStorage_setup = f"""
// Paste this in browser console to test manually:
localStorage.setItem('access_token', '{token}');
localStorage.setItem('user_data', JSON.stringify({json.dumps(user_data)}));
window.location.href = 'http://localhost:3000/principal-web/dashboard.html';
"""

print("\n📌 Or paste this in browser console (F12 -> Console):")
print(localStorage_setup)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - SYSTEM IS READY!")
print("=" * 60)
