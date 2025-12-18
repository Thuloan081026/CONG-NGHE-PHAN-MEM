#!/usr/bin/env python3
"""
Script test kết nối MySQL và verify data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    """Test kết nối MySQL"""

    print("🔍 Test kết nối MySQL...")

    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Kết nối MySQL thành công!")

        # Test query data
        db = SessionLocal()

        # Count users
        users_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        print(f"👥 Users: {users_count}")

        # Count syllabuses
        syllabuses_count = db.execute(text("SELECT COUNT(*) FROM syllabuses")).scalar()
        print(f"📚 Syllabuses: {syllabuses_count}")

        # Count workflow events
        events_count = db.execute(text("SELECT COUNT(*) FROM workflow_events")).scalar()
        print(f"⚡ Workflow Events: {events_count}")

        # Show sample data
        print("\n📋 Sample data:")

        # Users
        users = db.execute(text("SELECT email, full_name, role FROM users")).fetchall()
        for user in users:
            print(f"   👤 {user[0]} - {user[1]} ({user[2]})")

        # Syllabus
        syllabus = db.execute(text("SELECT subject_code, subject_name, status FROM syllabuses")).fetchone()
        if syllabus:
            print(f"   📖 {syllabus[0]} - {syllabus[1]} (Status: {syllabus[2]})")

        # Workflow events
        events = db.execute(text("SELECT action, to_status, comment FROM workflow_events ORDER BY id")).fetchall()
        for event in events:
            print(f"   ⚡ {event[0]} -> {event[1]}: {event[2]}")

        db.close()

        print("\n🎉 TẤT CẢ HOẠT ĐỘNG TỐT!")
        print("📊 Kiểm tra phpMyAdmin để xem data: http://localhost/phpmyadmin")

    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()