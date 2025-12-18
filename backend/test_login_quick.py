from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
r = client.post('/auth/login', json={'email': 'admin@hcmute.edu.vn', 'password': 'admin123'})
print(f'Status: {r.status_code}')
data = r.json()
print(f'Has user: {data.get("user") is not None}')
print(f'User email: {data.get("user", {}).get("email")}')
print(f'User role: {data.get("user", {}).get("role")}')
