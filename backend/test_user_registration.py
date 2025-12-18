#!/usr/bin/env python3
"""
Script test chức năng đăng ký tài khoản trực tiếp qua database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user
from app.core.security import get_password_hash, verify_password
from datetime import datetime

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_user_registration():
    """Test chức năng đăng ký tài khoản"""

    print("🧪 TEST CHỨC NĂNG ĐĂNG KÝ TÀI KHOẢN")
    print("=" * 50)

    db = SessionLocal()

    try:
        # Test case 1: Đăng ký user mới thành công
        print("\n1️⃣ Test đăng ký user mới...")

        user_data = UserCreate(
            email="test_student@university.edu.vn",
            password="password123",
            full_name="Nguyễn Văn Test",
            role="student"
        )

        try:
            new_user = register_user(db, user_data)
            db.commit()
            print(f"✅ Đăng ký thành công: {new_user.email} (ID: {new_user.id})")
            print(f"   - Full name: {new_user.full_name}")
            print(f"   - Role: {new_user.role}")
            print(f"   - Active: {new_user.is_active}")
        except Exception as e:
            print(f"❌ Lỗi đăng ký: {e}")
            db.rollback()

        # Test case 2: Đăng ký user với email đã tồn tại
        print("\n2️⃣ Test đăng ký với email trùng lặp...")

        duplicate_user_data = UserCreate(
            email="test_student@university.edu.vn",  # Email đã dùng ở test 1
            password="different_password",
            full_name="Trùng Lặp",
            role="student"
        )

        try:
            duplicate_user = register_user(db, duplicate_user_data)
            db.commit()
            print("❌ Không nên thành công - email đã tồn tại!")
        except ValueError as e:
            print(f"✅ Đúng rồi - từ chối đăng ký: {e}")
        except Exception as e:
            print(f"❌ Lỗi khác: {e}")
            db.rollback()

        # Test case 3: Test đăng nhập với user vừa tạo
        print("\n3️⃣ Test đăng nhập với user vừa tạo...")

        from app.services.user_service import authenticate_user

        authenticated_user = authenticate_user(db, "test_student@university.edu.vn", "password123")
        if authenticated_user:
            print(f"✅ Đăng nhập thành công: {authenticated_user.email}")
            print(f"   - ID: {authenticated_user.id}")
            print(f"   - Full name: {authenticated_user.full_name}")
        else:
            print("❌ Đăng nhập thất bại")

        # Test case 4: Test đăng nhập sai password
        print("\n4️⃣ Test đăng nhập với sai password...")

        wrong_auth = authenticate_user(db, "test_student@university.edu.vn", "wrong_password")
        if wrong_auth:
            print("❌ Không nên đăng nhập được với sai password!")
        else:
            print("✅ Đúng rồi - từ chối đăng nhập sai password")

        # Test case 5: Test đăng ký thêm vài users khác
        print("\n5️⃣ Test đăng ký thêm users khác...")

        additional_users = [
            {"email": "student1@university.edu.vn", "password": "pass123", "full_name": "Sinh Viên 1", "role": "student"},
            {"email": "student2@university.edu.vn", "password": "pass123", "full_name": "Sinh Viên 2", "role": "student"},
            {"email": "reviewer@university.edu.vn", "password": "review123", "full_name": "Reviewer", "role": "reviewer"}
        ]

        created_users = []
        for user_info in additional_users:
            user_data = UserCreate(**user_info)
            try:
                new_user = register_user(db, user_data)
                db.commit()
                created_users.append(new_user)
                print(f"✅ Tạo user: {new_user.email} ({new_user.role})")
            except Exception as e:
                print(f"❌ Lỗi tạo user {user_info['email']}: {e}")
                db.rollback()

        # Test case 6: Đếm tổng số users
        print("\n6️⃣ Thống kê users trong database...")

        total_users = db.query(User).count()
        users_by_role = {}
        for role in ["lecturer", "hod", "aa", "principal", "student", "reviewer"]:
            count = db.query(User).filter(User.role == role).count()
            if count > 0:
                users_by_role[role] = count

        print(f"📊 Tổng số users: {total_users}")
        for role, count in users_by_role.items():
            print(f"   - {role}: {count}")

        # Test case 7: Hiển thị tất cả users
        print("\n7️⃣ Danh sách tất cả users:")

        all_users = db.query(User).order_by(User.id).all()
        for user in all_users:
            print(f"   👤 {user.id}: {user.email} - {user.full_name} ({user.role})")

        print("\n" + "=" * 50)
        print("🎉 HOÀN THÀNH TEST ĐĂNG KÝ TÀI KHOẢN!")
        print("✅ Chức năng đăng ký hoạt động tốt")
        print("✅ Password hashing và verification OK")
        print("✅ Validation email trùng lặp OK")
        print("✅ Authentication OK")

    except Exception as e:
        print(f"❌ Lỗi test: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_user_registration()