#!/usr/bin/env python3
"""
Script test nhanh đăng ký tài khoản
Tạo user mới với thông tin ngẫu nhiên
"""

import sys
import os
import random
import string
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user, authenticate_user

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_random_user():
    """Tạo thông tin user ngẫu nhiên"""

    # Tạo email ngẫu nhiên
    random_suffix = ''.join(random.choices(string.digits, k=3))
    email = f"test_user_{random_suffix}@university.edu.vn"

    # Password ngẫu nhiên
    password = "test" + ''.join(random.choices(string.digits, k=3))

    # Tên ngẫu nhiên
    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng"]
    middle_names = ["Văn", "Thị", "Đức", "Minh", "Hoàng", "Hữu", "Thành", "Ngọc"]
    last_names = ["An", "Bình", "Cường", "Dung", "Em", "Giang", "Hùng", "Lan"]

    full_name = f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"

    # Role ngẫu nhiên
    roles = ["student", "lecturer", "reviewer"]
    role = random.choice(roles)

    return {
        "email": email,
        "password": password,
        "full_name": full_name,
        "role": role
    }

def quick_test_registration():
    """Test nhanh đăng ký tài khoản"""

    print("⚡ TEST NHANH ĐĂNG KÝ TÀI KHOẢN")
    print("=" * 50)

    # Tạo user ngẫu nhiên
    user_info = generate_random_user()

    print("🎲 Thông tin user ngẫu nhiên:")
    print(f"   📧 Email: {user_info['email']}")
    print(f"   🔒 Password: {user_info['password']}")
    print(f"   👤 Tên: {user_info['full_name']}")
    print(f"   🎭 Role: {user_info['role']}")
    print()

    # Xác nhận
    confirm = input("🚀 Tạo user này? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', 'đúng', 'ok']:
        print("❌ Đã hủy")
        return

    db = SessionLocal()

    try:
        print("⏳ Đang tạo tài khoản...")

        user_data = UserCreate(**user_info)
        new_user = register_user(db, user_data)
        db.commit()

        print("✅ TẠO TÀI KHOẢN THÀNH CÔNG!")
        print(f"   👤 ID: {new_user.id}")
        print(f"   📧 Email: {new_user.email}")
        print(f"   👤 Tên: {new_user.full_name}")
        print(f"   🎭 Role: {new_user.role}")
        print(f"   ✅ Active: {new_user.is_active}")

        # Test đăng nhập
        print("\n🔐 Test đăng nhập...")
        auth_user = authenticate_user(db, user_info['email'], user_info['password'])
        if auth_user:
            print("✅ Đăng nhập thành công!")
        else:
            print("❌ Đăng nhập thất bại!")

        # Thống kê
        total_users = db.query(db.query().count()).scalar()
        print(f"\n📊 Tổng users hiện tại: {db.query(db.query().count()).scalar()}")

        print("\n💡 Lưu ý thông tin đăng nhập:")
        print(f"   📧 Email: {user_info['email']}")
        print(f"   🔒 Password: {user_info['password']}")

    except ValueError as e:
        print(f"❌ Lỗi: {e}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def batch_create_users():
    """Tạo nhiều users cùng lúc"""

    print("📦 TẠO NHIỀU USERS CÙNG LÚC")
    print("=" * 50)

    try:
        num_users = int(input("Nhập số lượng users muốn tạo (1-10): ").strip())
        if num_users < 1 or num_users > 10:
            print("❌ Số lượng phải từ 1-10")
            return
    except ValueError:
        print("❌ Vui lòng nhập số")
        return

    confirm = input(f"🚀 Tạo {num_users} users? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', 'đúng', 'ok']:
        print("❌ Đã hủy")
        return

    db = SessionLocal()
    created_users = []

    try:
        print(f"⏳ Đang tạo {num_users} users...")

        for i in range(num_users):
            user_info = generate_random_user()
            user_data = UserCreate(**user_info)

            try:
                new_user = register_user(db, user_data)
                db.commit()
                created_users.append(new_user)
                print(f"✅ {i+1:2d}. {new_user.email} ({new_user.role})")
            except ValueError as e:
                print(f"⚠️  {i+1:2d}. Bỏ qua: {user_info['email']} - {e}")
                db.rollback()
            except Exception as e:
                print(f"❌ {i+1:2d}. Lỗi: {user_info['email']} - {e}")
                db.rollback()

        print(f"\n📊 KẾT QUẢ: Tạo thành công {len(created_users)}/{num_users} users")

        if created_users:
            print("\n👥 Users đã tạo:")
            for user in created_users:
                print(f"   📧 {user.email} | 🔒 [password ngẫu nhiên] | 🎭 {user.role}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

def show_menu():
    """Menu lựa chọn"""

    print("🎯 TEST NHANH ĐĂNG KÝ TÀI KHOẢN")
    print("=" * 50)
    print("1. Tạo 1 user ngẫu nhiên")
    print("2. Tạo nhiều users cùng lúc")
    print("3. Thoát")
    print()

    choice = input("Chọn (1-3): ").strip()

    if choice == "1":
        quick_test_registration()
    elif choice == "2":
        batch_create_users()
    elif choice == "3":
        print("👋 Tạm biệt!")
        return
    else:
        print("❌ Lựa chọn không hợp lệ!")
        show_menu()

if __name__ == "__main__":
    print("🚀 SCRIPT TEST NHANH ĐĂNG KÝ TÀI KHOẢN")
    print("Tạo users với thông tin ngẫu nhiên")
    print("=" * 50)

    while True:
        show_menu()
        print()
        continue_test = input("Test tiếp? (y/n): ").strip().lower()
        if continue_test not in ['y', 'yes', 'đúng', 'ok']:
            break
        print()