import requests
import json

# Test login principal
url = "http://localhost:8000/auth/login"
payload = {
    "email": "principal@edu.vn",
    "password": "principal123"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Login successful!")
        print(f"Token: {token[:50]}...")
        print(f"Role: {data['user']['role']}")
        
        # Test /users/me
        headers = {"Authorization": f"Bearer {token}"}
        user_response = requests.get("http://localhost:8000/users/me", headers=headers)
        print(f"\n✅ /users/me Status: {user_response.status_code}")
        user_data = user_response.json()
        print(f"User role: {user_data['role']}")
        print(f"User email: {user_data['email']}")
        print(f"\nNow go to: http://localhost:3000/principal-web/dashboard.html")
    else:
        print(f"❌ Login failed: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")
