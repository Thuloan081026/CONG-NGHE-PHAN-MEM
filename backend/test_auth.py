#!/usr/bin/env python3
"""Test authentication directly"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services import user_service

db = SessionLocal()

test_accounts = [
    ("admin@ut.edu.vn", "admin123"),
    ("admin@test.com", "admin123"),
    ("lecturer@ut.edu.vn", "lecturer123"),
    ("lecturer@test.com", "lecturer123"),
    ("student@ut.edu.vn", "student123"),
    ("student@test.com", "student123"),
]

print("\n" + "="*60)
print("TEST AUTHENTICATION")
print("="*60 + "\n")

for email, password in test_accounts:
    print(f"Testing {email} / {password}...")
    user = user_service.authenticate_user(db, email, password)
    if user:
        print(f"  ✅ SUCCESS - {user.full_name} ({user.role})")
    else:
        print(f"  ❌ FAILED")
    print()

db.close()
