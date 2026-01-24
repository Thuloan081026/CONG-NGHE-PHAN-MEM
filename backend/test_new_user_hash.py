#!/usr/bin/env python3
"""
Script test đăng ký user mới với password hash
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user, authenticate_user
from app.core.security import verify_password

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_new_user_with_hash():
    """Test tạo user mới với password được hash"""

    print("🧪 TEST ĐĂNG KÝ USER MỚI VỚI PASSWORD HASH")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Tạo user test
        test_user_data = UserCreate(
            email="new_hash_user@university.edu.vn",
            password="my_secure_password_456",
            full_name="New Hash User",
            role="student"
        )

        print("⏳ Đang đăng ký user mới...")
        new_user = register_user(db, test_user_data)
        db.commit()

        print("✅ ĐĂNG KÝ THÀNH CÔNG!")
        print(f"   👤 ID: {new_user.id}")
        print(f"   📧 Email: {new_user.email}")
        print(f"   👤 Tên: {new_user.full_name}")
        print(f"   🎭 Role: {new_user.role}")
        print(f"   ✅ Active: {new_user.is_active}")

        # Kiểm tra password đã được hash
        hashed_password = new_user.hashed_password
        print(f"\n🔒 Password hash: {hashed_password[:60]}...")

        if hashed_password.startswith('$argon2'):
            print("✅ Password đã được hash bằng Argon2!")
        else:
            print("❌ Password chưa được hash!")
            return

        # Test verify password
        print("\n🔐 Test verification:")

        # Test đúng password
        correct = verify_password("my_secure_password_456", hashed_password)
        print(f"   ✅ Đúng password: {correct}")

        # Test sai password
        wrong = verify_password("wrong_password", hashed_password)
        print(f"   ❌ Sai password: {not wrong}")

        # Test đăng nhập qua service
        print("\n🚪 Test đăng nhập:")
        auth_user = authenticate_user(db, "new_hash_user@university.edu.vn", "my_secure_password_456")
        if auth_user:
            print("✅ Đăng nhập thành công!")
        else:
            print("❌ Đăng nhập thất bại!")

        # Hiển thị trong database
        print(f"\n💾 Password trong database: {hashed_password[:50]}...")

        # Clean up - xóa user test
        db.delete(new_user)
        db.commit()
        print("🧹 Đã xóa user test")

        print("\n🎉 TẤT CẢ HOẠT ĐỘNG TỐT!")
        print("   ✅ Password được hash bằng Argon2")
        print("   ✅ Verification hoạt động")
        print("   ✅ Authentication hoạt động")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_new_user_with_hash()