#!/usr/bin/env python3
"""
Script to verify student account in database
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import User


def verify_student_account(email: str):
    """Verify if student account exists"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"✅ Tài khoản sinh viên tồn tại:")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Họ tên: {user.full_name}")
            print(f"   Vai trò: {user.role}")
            print(f"   Trạng thái: {'Kích hoạt' if user.is_active else 'Vô hiệu hóa'}")
            print(f"   Ngày tạo: {user.created_at}")
            return True
        else:
            print(f"❌ Tài khoản không tồn tại: {email}")
            return False
    finally:
        db.close()


if __name__ == "__main__":
    email = "student@ut.edu.vn"
    print(f"Kiểm tra tài khoản: {email}\n")
    verify_student_account(email)
