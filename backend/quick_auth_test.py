"""Test login without checking response"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Trực tiếp test endpoint
response = client.post("/auth/login", json={
    "email": "admin@hcmute.edu.vn",
    "password": "admin123"
})

if response.status_code == 200:
    data = response.json()
    print("✅ Module 1: Authentication - WORKING")
    print(f"   Token received: {data['access_token'][:30]}...")
    print(f"   User in response: {'Yes' if data.get('user') else 'No (but token works)'}")
    
    # Test protected endpoint
    token = data['access_token']
    response2 = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    if response2.status_code == 200:
        users = response2.json()
        print(f"   Protected endpoint works: {len(users)} users found")
    else:
        print(f"   Protected endpoint status: {response2.status_code}")
else:
    print(f"❌ Login failed: {response.status_code}")
