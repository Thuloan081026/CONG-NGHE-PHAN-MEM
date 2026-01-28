#!/usr/bin/env python3
"""Check users in database"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

db = SessionLocal()

try:
    users = db.query(User).all()
    
    print("\n" + "="*60)
    print("DANH SÁCH TÀI KHOẢN TRONG DATABASE")
    print("="*60)
    
    if not users:
        print("\n❌ Không có user nào trong database!")
    else:
        for user in users:
            print(f"\n📧 Email: {user.email}")
            print(f"   Tên: {user.full_name}")
            print(f"   Role: {user.role}")
            print(f"   Active: {user.is_active}")
            print(f"   Password hash: {user.hashed_password[:50]}...")
            
            # Test password
            test_passwords = ["admin123", "lecturer123", "student123", "Admin@123", "Lecturer@123"]
            for pwd in test_passwords:
                if verify_password(pwd, user.hashed_password):
                    print(f"   ✅ Password: {pwd}")
                    break
    
    print("\n" + "="*60)
    print("THÔNG TIN ĐĂNG NHẬP:")
    print("="*60)
    print("\nĐể đăng nhập, sử dụng:")
    print("  Email: <email từ danh sách trên>")
    print("  Password: <password tương ứng>")
    print("\nVí dụ:")
    print("  Email: admin@test.com")
    print("  Password: admin123")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
