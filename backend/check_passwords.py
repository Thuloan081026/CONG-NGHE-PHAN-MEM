#!/usr/bin/env python3
"""
Script kiểm tra nhanh password hashing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_passwords():
    """Kiểm tra password trong database"""

    print("🔍 KIỂM TRA PASSWORD TRONG DATABASE")
    print("=" * 60)

    db = SessionLocal()

    try:
        users = db.query(User).order_by(User.id).all()

        if not users:
            print("❌ Không có user nào")
            return

        print(f"📊 Tổng users: {len(users)}")
        print()

        hashed_count = 0
        plain_count = 0

        print("👥 CHI TIẾT USERS:")
        print("-" * 60)

        for user in users:
            password = user.hashed_password

            if password.startswith('$argon2'):
                status = "✅ HASHED"
                hashed_count += 1
            else:
                status = "❌ PLAIN TEXT"
                plain_count += 1

            print(f"{user.id:2d}. {user.email:35s} | {status}")
            if len(password) > 50:
                print(f"    Hash: {password[:50]}...")
            else:
                print(f"    Password: '{password}'")

        print("-" * 60)
        print("📈 THỐNG KÊ:")
        print(f"   ✅ Password đã hash: {hashed_count}")
        print(f"   ❌ Password plain text: {plain_count}")

        if plain_count > 0:
            print("\n⚠️  CẦN FIX: Có password chưa được hash!")
            print("   Chạy: python password_hash_manager.py -> option 2")
        else:
            print("\n🎉 TỔT: Tất cả password đã được hash!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_passwords()