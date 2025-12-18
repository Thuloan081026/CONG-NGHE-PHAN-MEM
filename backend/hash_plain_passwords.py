#!/usr/bin/env python3
"""
Script hash lại tất cả password plain text trong database
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

def hash_all_plain_passwords():
    """Hash lại tất cả password plain text"""

    print("🔧 HASH LẠI TẤT CẢ PASSWORD PLAIN TEXT")
    print("=" * 60)
    print("⚠️  Script sẽ chuyển đổi password plain text thành hash")
    print("   Việc này không thể hoàn tác!")
    print()

    # Xác nhận
    confirm = input("🚀 Tiếp tục? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y', 'đúng', 'ok']:
        print("❌ Đã hủy")
        return

    db = SessionLocal()

    try:
        users = db.query(User).all()
        fixed_count = 0
        error_count = 0

        print(f"⏳ Đang hash password cho {len(users)} users...")
        print()

        for user in users:
            old_password = user.hashed_password

            # Nếu chưa phải hash (không bắt đầu bằng $argon2)
            if not old_password.startswith('$argon2'):
                try:
                    # Hash password
                    new_hashed_password = get_password_hash(old_password)

                    # Verify hash hoạt động
                    if verify_password(old_password, new_hashed_password):
                        user.hashed_password = new_hashed_password
                        fixed_count += 1

                        print(f"✅ {user.email}")
                        print(f"   Old: '{old_password}'")
                        print(f"   New: {new_hashed_password[:50]}...")
                        print()
                    else:
                        print(f"❌ Verify failed: {user.email}")
                        error_count += 1

                except Exception as e:
                    print(f"❌ Error hashing {user.email}: {e}")
                    error_count += 1
            else:
                print(f"⚠️  Already hashed: {user.email}")

        # Commit changes
        if fixed_count > 0:
            db.commit()
            print("💾 Đã lưu thay đổi vào database")
        else:
            print("ℹ️  Không có password nào cần hash")

        print()
        print("📊 KẾT QUẢ:")
        print(f"   ✅ Đã hash thành công: {fixed_count}")
        print(f"   ❌ Lỗi: {error_count}")

        if fixed_count > 0:
            print("\n🎉 HOÀN THÀNH! Password đã được bảo mật bằng Argon2")

    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
        db.rollback()
    finally:
        db.close()

def test_new_user_hashing():
    """Test tạo user mới với password được hash"""

    print("🧪 TEST TẠO USER MỚI VỚI PASSWORD HASH")
    print("=" * 60)

    from app.schemas.user_schema import UserCreate
    from app.services.user_service import register_user

    db = SessionLocal()

    try:
        # Tạo user test
        test_user_data = UserCreate(
            email="hash_test@university.edu.vn",
            password="secure_password_123",
            full_name="Hash Test User",
            role="student"
        )

        print("⏳ Tạo user test...")
        test_user = register_user(db, test_user_data)
        db.commit()

        print("✅ Tạo user thành công!")
        print(f"   👤 Email: {test_user.email}")
        print(f"   🔒 Password hash: {test_user.hashed_password[:60]}...")

        # Verify password
        is_valid = verify_password("secure_password_123", test_user.hashed_password)
        print(f"   ✅ Password verification: {is_valid}")

        # Test wrong password
        is_invalid = verify_password("wrong_password", test_user.hashed_password)
        print(f"   ❌ Wrong password test: {not is_invalid}")

        # Clean up
        db.delete(test_user)
        db.commit()
        print("🧹 Đã xóa user test")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔐 HASH PASSWORD PLAIN TEXT")
    print("Chuyển đổi tất cả password trong database thành hash")
    print("=" * 60)

    # Hiển thị thống kê trước
    print("📊 TÌNH TRẠNG HIỆN TẠI:")
    from check_passwords import check_passwords
    check_passwords()

    print()
    hash_all_plain_passwords()

    print()
    print("🧪 TEST PASSWORD HASHING MỚI:")
    test_new_user_hashing()

    print()
    print("🔍 KIỂM TRA LẠI SAU KHI HASH:")
    check_passwords()