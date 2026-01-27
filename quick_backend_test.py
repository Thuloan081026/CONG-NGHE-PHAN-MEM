import requests

try:
    r = requests.post('http://localhost:8000/auth/login', 
        json={'email': 'principal@edu.vn', 'password': 'principal123'},
        timeout=3)
    print(f'Status: {r.status_code}')
    data = r.json()
    role = data.get('user', {}).get('role')
    print(f'Role: {role}')
    if role == 'principal':
        print('✅ Backend OK - Principal role confirmed')
    else:
        print(f'❌ Unexpected role: {role}')
except Exception as e:
    print(f'❌ Error: {e}')
