"""Test login response direct"""
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

response = client.post("/auth/login", json={
    "email": "admin@hcmute.edu.vn",
    "password": "admin123"
})

print(f"Status: {response.status_code}")
print(f"Response text: {response.text}")
print(f"\nParsed JSON:")
data = response.json()
for key, value in data.items():
    print(f"  {key}: {value}")
