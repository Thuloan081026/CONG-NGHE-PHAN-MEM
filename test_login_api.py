import requests
import json

# Test login
url = "http://localhost:8000/auth/login"
payload = {
    "email": "student@edu.vn",
    "password": "student123"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        if token:
            print(f"\n✅ Login successful! Token: {token[:50]}...")
            
            # Test /users/me
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get("http://localhost:8000/users/me", headers=headers)
            print(f"\n/users/me Status: {user_response.status_code}")
            print(f"/users/me Response: {json.dumps(user_response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
