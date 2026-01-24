#!/usr/bin/env python3
"""Initialize database with demo users"""
from app.core.database import engine, Base, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

# Create all tables
print("📋 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

# Create session
db = SessionLocal()

try:
    # Demo users với email @ut.edu.vn
    demo_users = [
        {"email": "admin@ut.edu.vn", "full_name": "Quản trị viên hệ thống", "password": "admin123", "role": "admin"},
        {"email": "lecturer@ut.edu.vn", "full_name": "Giảng viên Demo", "password": "lecturer123", "role": "lecturer"},
        {"email": "hod@ut.edu.vn", "full_name": "Trưởng khoa CNTT", "password": "hod123", "role": "hod"},
        {"email": "aa@ut.edu.vn", "full_name": "Phòng Đào tạo", "password": "aa123", "role": "academic_affairs"},
        {"email": "student@ut.edu.vn", "full_name": "Sinh viên Demo", "password": "student123", "role": "student"},
    ]
    
    print("\n👥 Creating demo users...")
    for user_data in demo_users:
        # Check if user exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"  ✓ {user_data['email']} already exists")
        else:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_active=True
            )
            db.add(user)
            print(f"  ✅ Created {user_data['email']}")
    
    db.commit()
    
    print("\n✨ Database initialized successfully!")
    print("\n📝 Login credentials:")
    for user_data in demo_users:
        print(f"  • {user_data['email']} / {user_data['password']} ({user_data['role']})")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()
