#!/usr/bin/env python3
"""
Script tạo data mẫu trực tiếp vào MySQL
Không cần server, ghi thẳng vào database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.workflow import WorkflowEvent
from app.core.security import get_password_hash
from datetime import datetime

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_data():
    """Tạo data mẫu trong MySQL"""

    print("🚀 Tạo data mẫu trong MySQL database...")

    # Tạo tables
    print("📋 Tạo tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

    db = SessionLocal()

    try:
        # 1. Tạo users
        print("\n👥 Tạo users...")
        users_data = [
            {"email": "lecturer@university.edu.vn", "full_name": "Nguyễn Văn An", "role": "lecturer"},
            {"email": "hod@university.edu.vn", "full_name": "Trần Thị Bình", "role": "hod"},
            {"email": "aa@university.edu.vn", "full_name": "Lê Văn Cường", "role": "aa"},
            {"email": "principal@university.edu.vn", "full_name": "Phạm Thị Dung", "role": "principal"}
        ]

        users = []
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=user_data["email"],  # Plain text for simplicity
                role=user_data["role"]
            )
            db.add(user)
            users.append(user)

        db.commit()
        print(f"✅ Đã tạo {len(users)} users")

        # 2. Tạo syllabus
        print("\n📚 Tạo syllabus...")
        syllabus = Syllabus(
            subject_code="CNPM001",
            subject_name="Công nghệ Phần mềm",
            description="Môn học về phát triển phần mềm hiện đại",
            credits=3,
            semester=1,
            department="Công nghệ Thông tin",
            academic_year="2025-2026",
            objectives="Hiểu và áp dụng quy trình phát triển phần mềm",
            content="Agile, Scrum, CI/CD, Testing, DevOps",
            teaching_methods="Bài giảng, Thực hành, Project",
            assessment_methods="Thi viết (40%), Bài tập (30%), Project (30%)",
            prerequisites='[{"id": "PROG101", "name": "Lập trình Cơ bản"}]',
            clos='[{"id": "CLO1", "description": "Hiểu quy trình Agile", "level": "K3"}, {"id": "CLO2", "description": "Áp dụng Scrum", "level": "K4"}]',
            plos='[{"id": "PLO1", "description": "Kỹ năng mềm", "alignment": 0.8}, {"id": "PLO2", "description": "Kỹ năng chuyên môn", "alignment": 0.9}]',
            assessment_weights='{"attendance": 10, "assignment": 30, "exam": 60}',
            created_by=users[0].id  # Lecturer
        )

        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)
        print(f"✅ Đã tạo syllabus: {syllabus.subject_code}")

        # 3. Tạo workflow events
        print("\n⚡ Tạo workflow events...")

        # Submit
        event1 = WorkflowEvent(
            syllabus_id=syllabus.id,
            action="submit",
            from_status=None,
            to_status="submitted",
            comment="Đề nghị duyệt giáo trình",
            performed_by=users[0].id  # Lecturer
        )
        db.add(event1)

        # HOD approve
        event2 = WorkflowEvent(
            syllabus_id=syllabus.id,
            action="hod_approve",
            from_status="submitted",
            to_status="hod_approved",
            comment="Đã duyệt cấp khoa",
            performed_by=users[1].id  # HOD
        )
        db.add(event2)

        # AA approve
        event3 = WorkflowEvent(
            syllabus_id=syllabus.id,
            action="aa_approve",
            from_status="hod_approved",
            to_status="aa_approved",
            comment="Đã duyệt phòng Đào tạo",
            performed_by=users[2].id  # AA
        )
        db.add(event3)

        # Final approve
        event4 = WorkflowEvent(
            syllabus_id=syllabus.id,
            action="final_approve_and_publish",
            from_status="aa_approved",
            to_status="published",
            comment="Phê duyệt và công bố",
            performed_by=users[3].id  # Principal
        )
        db.add(event4)

        # Update syllabus status
        syllabus.status = "published"
        syllabus.is_published = True
        syllabus.published_at = datetime.utcnow()

        db.commit()
        print("✅ Đã tạo 4 workflow events và cập nhật syllabus status")

        # 4. Summary
        print("\n🎉 HOÀN THÀNH! Data đã được ghi vào MySQL")
        print("📊 Kiểm tra phpMyAdmin: http://localhost/phpmyadmin")
        print("   - Database: syllabus_db")
        print("   - Tables: users, syllabuses, workflow_events")

        # Show created data
        print("\n📋 Data đã tạo:")
        print(f"   👥 Users: {len(users)}")
        for user in users:
            print(f"      - {user.email} ({user.role})")

        print(f"   📚 Syllabus: {syllabus.subject_code} - {syllabus.subject_name}")
        print(f"   ⚡ Workflow: {syllabus.status} (published)")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()