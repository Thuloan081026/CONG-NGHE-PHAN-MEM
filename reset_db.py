#!/usr/bin/env python
"""Reset database and create demo users with @edu.vn emails"""

import sys
sys.path.insert(0, 'backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings
from app.core.security import get_password_hash
from app.models.user import User
from app.core.database import Base

settings = Settings()
print(f"🔧 Working with: {settings.DATABASE_URL}")

# Drop and recreate database
db_name = settings.DATABASE_URL.split('/')[-1]
base_url = settings.DATABASE_URL.rsplit('/', 1)[0]

print(f"⚠️  Dropping database '{db_name}'...")
engine_base = create_engine(base_url)
try:
    with engine_base.begin() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS `{db_name}`"))
    print(f"✓ Database dropped")
except Exception as e:
    print(f"  Error: {e}")

engine_base.dispose()

# Recreate database
print(f"✓ Creating database '{db_name}'...")
engine_base = create_engine(base_url)
try:
    with engine_base.begin() as conn:
        conn.execute(text(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    print(f"✓ Database created")
except Exception as e:
    print(f"  Error: {e}")

engine_base.dispose()

# Create new connection to the database
engine = create_engine(settings.DATABASE_URL)

# Create all tables
print("📋 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created")

# Create session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Create demo users
    print("\n👥 Creating demo users with @edu.vn emails...")
    
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
        print(f"  ✓ {user_data['email']} (password: {user_data['password']})")
    
    db.commit()
    print("\n✨ All demo users created!")
    
    # Verify
    print("\n✅ Verification:")
    users = db.query(User).all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"  - {u.email} ({u.role})")

finally:
    db.close()
