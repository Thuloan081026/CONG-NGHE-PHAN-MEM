#!/usr/bin/env python3
"""
Script test thủ công đăng ký tài khoản
Người dùng nhập thông tin và xem kết quả trực tiếp
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user, authenticate_user

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def manual_test_registration():
    """Test thủ công đăng ký tài khoản"""

    print("🧪 TEST THỦ CÔNG ĐĂNG KÝ TÀI KHOẢN")
    print("=" * 50)
    print("Nhập thông tin để test đăng ký tài khoản")
    print("Nhấn Enter để bỏ qua và dùng giá trị mặc định")
    print()

    # Nhập thông tin từ user
    email = input("📧 Email (mặc định: manual_test@university.edu.vn): ").strip()
    if not email:
        email = "manual_test@university.edu.vn"

    password = input("🔒 Password (mặc định: test123): ").strip()
    if not password:
        password = "test123"

    full_name = input("👤 Họ tên đầy đủ (mặc định: Người Dùng Test): ").strip()
    if not full_name:
        full_name = "Người Dùng Test"

    role_options = ["student", "lecturer", "hod", "aa", "principal", "reviewer"]
    print(f"🎭 Role: {', '.join(role_options)}")
    role = input("   Chọn role (mặc định: student): ").strip().lower()
    if not role or role not in role_options:
        role = "student"

    print("\n" + "=" * 50)
    print("📋 THÔNG TIN ĐĂNG KÝ:")
    print(f"   📧 Email: {email}")
    print(f"   👤 Tên: {full_name}")
    print(f"   🎭 Role: {role}")
    print(f"   🔒 Password: {'*' * len(password)}")
    print("=" * 50)

    # Xác nhận
    confirm = input("\n🚀 Tiến hành đăng ký? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', 'đúng', 'ok']:
        print("❌ Đã hủy test")
        return

    db = SessionLocal()

    try:
        # Tạo user
        print("\n⏳ Đang đăng ký tài khoản...")

        user_data = UserCreate(
            email=email,
            password=password,
            full_name=full_name,
            role=role
        )

        new_user = register_user(db, user_data)
        db.commit()

        print("✅ ĐĂNG KÝ THÀNH CÔNG!")
        print(f"   👤 ID: {new_user.id}")
        print(f"   📧 Email: {new_user.email}")
        print(f"   👤 Tên: {new_user.full_name}")
        print(f"   🎭 Role: {new_user.role}")
        print(f"   ✅ Active: {new_user.is_active}")

        # Test đăng nhập
        print("\n🔐 Test đăng nhập...")
        auth_user = authenticate_user(db, email, password)
        if auth_user:
            print("✅ Đăng nhập thành công!")
            print(f"   👤 Xin chào: {auth_user.full_name}")
        else:
            print("❌ Đăng nhập thất bại!")

        # Hiển thị tất cả users
        print("\n📊 DANH SÁCH TẤT CẢ USERS:")
        all_users = db.query(User).order_by(User.id).all()
        for user in all_users:
            print(f"   {user.id:2d}. {user.email:30s} | {user.full_name:20s} | {user.role:10s}")

        print("\n" + "=" * 50)
        print("🎉 TEST HOÀN THÀNH!")
        print("💡 Kiểm tra phpMyAdmin: http://localhost/phpmyadmin")
        print("   - Database: syllabus_db")
        print("   - Table: users")

    except ValueError as e:
        print(f"❌ LỖI: {e}")
        if "Email already registered" in str(e):
            print("💡 Email này đã được đăng ký rồi!")
    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def show_menu():
    """Hiển thị menu lựa chọn"""

    print("🎯 CHỌN CÁCH TEST:")
    print("1. Test đăng ký thủ công (nhập thông tin)")
    print("2. Test với data mẫu có sẵn")
    print("3. Xem danh sách users hiện tại")
    print("4. Thoát")

    choice = input("\nChọn (1-4): ").strip()

    if choice == "1":
        manual_test_registration()
    elif choice == "2":
        test_with_sample_data()
    elif choice == "3":
        show_current_users()
    elif choice == "4":
        print("👋 Tạm biệt!")
        return
    else:
        print("❌ Lựa chọn không hợp lệ!")
        show_menu()

def test_with_sample_data():
    """Test với data mẫu"""

    print("🧪 TEST VỚI DATA MẪU")
    print("=" * 50)

    sample_users = [
        {"email": "sample_student@university.edu.vn", "password": "student123", "full_name": "Sinh Viên Mẫu", "role": "student"},
        {"email": "sample_lecturer@university.edu.vn", "password": "lecturer123", "full_name": "Giảng Viên Mẫu", "role": "lecturer"},
        {"email": "sample_reviewer@university.edu.vn", "password": "reviewer123", "full_name": "Reviewer Mẫu", "role": "reviewer"}
    ]

    db = SessionLocal()

    try:
        print("⏳ Đang tạo users mẫu...")

        for user_info in sample_users:
            user_data = UserCreate(**user_info)
            try:
                new_user = register_user(db, user_data)
                db.commit()
                print(f"✅ Tạo: {new_user.email} ({new_user.role})")
            except ValueError as e:
                print(f"⚠️  Bỏ qua: {user_info['email']} - {e}")
                db.rollback()
            except Exception as e:
                print(f"❌ Lỗi: {user_info['email']} - {e}")
                db.rollback()

        print("\n📊 KẾT QUẢ:")
        total_users = db.query(User).count()
        print(f"   👥 Tổng users: {total_users}")

        # Thống kê theo role
        roles = ["student", "lecturer", "hod", "aa", "principal", "reviewer"]
        for role in roles:
            count = db.query(User).filter(User.role == role).count()
            if count > 0:
                print(f"   - {role}: {count}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

def show_current_users():
    """Hiển thị danh sách users hiện tại"""

    print("📋 DANH SÁCH USERS HIỆN TẠI")
    print("=" * 70)

    db = SessionLocal()

    try:
        users = db.query(User).order_by(User.id).all()

        if not users:
            print("❌ Chưa có user nào trong hệ thống")
            return

        print(f"{'ID':<3} {'Email':<35} {'Tên':<20} {'Role':<12} {'Active':<6}")
        print("-" * 70)

        for user in users:
            active = "✅" if user.is_active else "❌"
            print(f"{user.id:<3} {user.email:<35} {user.full_name:<20} {user.role:<12} {active:<6}")

        print("-" * 70)
        print(f"📊 Tổng cộng: {len(users)} users")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🎯 HƯỚNG DẪN TEST ĐĂNG KÝ TÀI KHOẢN THỦ CÔNG")
    print("=" * 50)
    print("Script này giúp bạn test chức năng đăng ký tài khoản")
    print("bằng cách tương tác trực tiếp với database MySQL")
    print()

    while True:
        show_menu()
        print()
        continue_test = input("Test tiếp? (y/n): ").strip().lower()
        if continue_test not in ['y', 'yes', 'đúng', 'ok']:
            break
        print()