"""Test HOD login"""
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test HOD login
print("Testing HOD login...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "hod@test.com", "password": "hod123"}
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"✓ HOD login successful")
    token = response.json()["access_token"]
    print(f"Token: {token[:50]}...")
else:
    print(f"✗ Failed: {response.text}")
    
    # Try different password
    print("\nTrying default password...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "hod@test.com", "password": "password"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ HOD login successful with 'password'")
    else:
        print(f"✗ Failed: {response.text}")
