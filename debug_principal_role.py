import requests
import json

# Test principal login
response = requests.post('http://localhost:8000/auth/login', json={
    'email': 'principal@edu.vn',
    'password': 'principal123'
})

print(f"Status: {response.status_code}")
data = response.json()
print(f"Full Response:")
print(json.dumps(data, indent=2))

# Check role in login response
if 'user' in data:
    role = data['user'].get('role')
    print(f"\n--- Role from Login Response ---")
    print(f"Role: '{role}'")
    print(f"Role type: {type(role)}")
    print(f"Role length: {len(role) if role else 'None'}")
    print(f"Role repr: {repr(role)}")
    print(f"Role bytes: {role.encode() if role else 'None'}")

# Also test /users/me
if 'access_token' in data:
    token = data['access_token']
    me_response = requests.get('http://localhost:8000/users/me', 
        headers={'Authorization': f'Bearer {token}'})
    print(f"\n--- Role from /users/me ---")
    user_data = me_response.json()
    role2 = user_data.get('role')
    print(f"Role: '{role2}'")
    print(f"Role repr: {repr(role2)}")
