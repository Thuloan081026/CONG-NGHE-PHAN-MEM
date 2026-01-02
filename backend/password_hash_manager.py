#!/usr/bin/env python3
"""
Script verify và fix password hashing trong database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.core.security import get_password_hash, verify_password

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_password_hashing():
    """Kiểm tra password hashing trong database"""

    print("🔍 KIỂM TRA PASSWORD HASHING")
    print("=" * 50)

    db = SessionLocal()

    try:
        users = db.query(User).all()

        if not users:
            print("❌ Không có user nào trong database")
            return

        print(f"📊 Tổng users: {len(users)}")
        print()

        hashed_count = 0
        plain_count = 0

        for user in users:
            password = user.hashed_password

            # Check if password looks like a hash (argon2 format)
            if password.startswith('$argon2'):
                hashed_count += 1
                status = "✅ HASHED"
            else:
                plain_count += 1
                status = "❌ PLAIN TEXT"

            print(f"👤 {user.id:2d}. {user.email:30s} | {status}")
            if len(password) > 50:  # Likely a hash
                print(f"       Hash: {password[:50]}...")
            else:
                print(f"       Password: {password}")

        print()
        print("📈 THỐNG KÊ:")
        print(f"   ✅ Hashed passwords: {hashed_count}")
        print(f"   ❌ Plain text passwords: {plain_count}")

        if plain_count > 0:
            print("\n⚠️  CẢNH BÁO: Có password chưa được hash!")
            return False
        else:
            print("\n🎉 TẤT CẢ PASSWORD ĐÃ ĐƯỢC HASH!")
            return True

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False
    finally:
        db.close()

def fix_plain_passwords():
    """Fix các password plain text thành hash"""

    print("🔧 FIX PASSWORD PLAIN TEXT")
    print("=" * 50)

    confirm = input("⚠️  Script sẽ hash lại tất cả password plain text. Tiếp tục? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', 'đúng', 'ok']:
        print("❌ Đã hủy")
        return

    db = SessionLocal()

    try:
        users = db.query(User).all()
        fixed_count = 0

        print("⏳ Đang hash password...")

        for user in users:
            password = user.hashed_password

            # Nếu chưa phải hash (không bắt đầu bằng $argon2)
            if not password.startswith('$argon2'):
                # Giả sử password hiện tại là plain text
                plain_password = password

                # Hash lại
                hashed_password = get_password_hash(plain_password)
                user.hashed_password = hashed_password

                # Verify hash hoạt động
                if verify_password(plain_password, hashed_password):
                    fixed_count += 1
                    print(f"✅ Fixed: {user.email}")
                else:
                    print(f"❌ Failed to verify: {user.email}")

        db.commit()
        print(f"\n🎉 Đã fix {fixed_count} password(s)!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

def test_password_verification():
    """Test chức năng verify password"""

    print("🧪 TEST PASSWORD VERIFICATION")
    print("=" * 50)

    db = SessionLocal()

    try:
        # Tạo user test mới với password được hash
        from app.schemas.user_schema import UserCreate
        from app.services.user_service import register_user

        test_user_data = UserCreate(
            email="password_test@university.edu.vn",
            password="test_password_123",
            full_name="Password Test User",
            role="student"
        )

        print("⏳ Tạo user test...")
        test_user = register_user(db, test_user_data)
        db.commit()

        print(f"✅ Tạo user: {test_user.email}")
        print(f"   Password hash: {test_user.hashed_password[:50]}...")

        # Test verify password
        test_cases = [
            ("test_password_123", True, "Correct password"),
            ("wrong_password", False, "Wrong password"),
            ("Test_Password_123", False, "Case sensitive"),
            ("test_password_123 ", False, "Trailing space"),
        ]

        print("\n🔐 Test verification:")
        for password, expected, description in test_cases:
            result = verify_password(password, test_user.hashed_password)
            status = "✅" if result == expected else "❌"
            print(f"   {status} {description}: '{password}' -> {result}")

        # Clean up - xóa user test
        db.delete(test_user)
        db.commit()
        print("\n🧹 Đã xóa user test")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

def show_menu():
    """Menu lựa chọn"""

    print("🔐 PASSWORD HASHING MANAGEMENT")
    print("=" * 50)
    print("1. Kiểm tra password hashing trong database")
    print("2. Fix password plain text (hash lại)")
    print("3. Test password verification")
    print("4. Thoát")

    choice = input("\nChọn (1-4): ").strip()

    if choice == "1":
        check_password_hashing()
    elif choice == "2":
        fix_plain_passwords()
    elif choice == "3":
        test_password_verification()
    elif choice == "4":
        print("👋 Tạm biệt!")
        return
    else:
        print("❌ Lựa chọn không hợp lệ!")
        show_menu()

if __name__ == "__main__":
    print("🔐 QUẢN LÝ PASSWORD HASHING")
    print("Kiểm tra và fix password trong database")
    print("=" * 50)

    while True:
        show_menu()
        print()
        continue_test = input("Tiếp tục? (y/n): ").strip().lower()
        if continue_test not in ['y', 'yes', 'đúng', 'ok']:
            break
        print()