#!/usr/bin/env python
"""Test login and create demo users if needed"""

import sys
sys.path.insert(0, 'backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.core.database import Base

settings = Settings()
print(f"✓ Connecting to: {settings.DATABASE_URL}")

# Create engine
engine = create_engine(settings.DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)
print("✓ Tables created/verified")

# Create session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Check if users exist
    existing_users = db.query(User).all()
    print(f"\n📊 Current users in database: {len(existing_users)}")
    for u in existing_users:
        print(f"  - {u.email} (role: {u.role})")
    
    if len(existing_users) == 0:
        print("\n⚠️  No users found. Creating demo users...")
        
        demo_users = [
            {"email": "admin@edu.vn", "full_name": "Quản trị viên hệ thống", "password": "admin123", "role": "admin"},
            {"email": "lecturer@edu.vn", "full_name": "Giảng viên Demo", "password": "lecturer123", "role": "lecturer"},
            {"email": "hod@edu.vn", "full_name": "Trưởng khoa CNTT", "password": "hod123", "role": "hod"},
            {"email": "aa@edu.vn", "full_name": "Phòng Đào tạo", "password": "aa123", "role": "academic_affairs"},
            {"email": "student@edu.vn", "full_name": "Sinh viên Demo", "password": "student123", "role": "student"},
        ]
        
        for user_data in demo_users:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_active=True
            )
            db.add(user)
            print(f"  ✓ {user_data['email']} / {user_data['password']}")
        
        db.commit()
        print("\n✨ Demo users created successfully!")
    
    # Test password verification
    print("\n🔐 Testing password verification...")
    admin = db.query(User).filter(User.email == "admin@edu.vn").first()
    if admin:
        print(f"  Found admin: {admin.email}")
        test_pwd = "admin123"
        is_valid = verify_password(test_pwd, admin.hashed_password)
        print(f"  Password '{test_pwd}' valid: {is_valid}")
        if not is_valid:
            print(f"  ⚠️  Hashed password mismatch. Updating...")
            admin.hashed_password = get_password_hash(test_pwd)
            db.commit()
            print(f"  ✓ Password updated")
    
    print("\n✅ Setup complete! You can now login with:")
    for user_data in [
        {"email": "admin@edu.vn", "password": "admin123"},
        {"email": "lecturer@edu.vn", "password": "lecturer123"},
        {"email": "student@edu.vn", "password": "student123"},
    ]:
        print(f"  Email: {user_data['email']} | Password: {user_data['password']}")

finally:
    db.close()
