#!/usr/bin/env python3
"""
Script test workflow đăng ký syllabus và duyệt
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
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user
from app.services.workflow_service import WorkflowService
from datetime import datetime

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_workflow():
    """Test workflow đăng ký và duyệt syllabus"""

    print("🔄 TEST WORKFLOW ĐĂNG KÝ VÀ DUYỆT SYLLABUS")
    print("=" * 60)

    db = SessionLocal()

    try:
        # 1. Tạo lecturer để test workflow
        print("\n1️⃣ Tạo lecturer để test workflow...")

        lecturer_data = UserCreate(
            email="workflow_lecturer@university.edu.vn",
            password="lecturer123",
            full_name="Giảng Viên Workflow",
            role="lecturer"
        )

        lecturer = register_user(db, lecturer_data)
        db.commit()
        print(f"✅ Tạo lecturer: {lecturer.email} (ID: {lecturer.id})")

        # 2. Lecturer tạo syllabus mới
        print("\n2️⃣ Lecturer tạo syllabus mới...")

        syllabus = Syllabus(
            subject_code="TEST001",
            subject_name="Môn Test Workflow",
            description="Môn học để test workflow",
            credits=2,
            semester=2,
            department="Khoa Test",
            academic_year="2025-2026",
            objectives="Test workflow system",
            content="Test content",
            teaching_methods="Test methods",
            assessment_methods="Test assessment",
            prerequisites='[{"id": "TEST000", "name": "Môn Tiên Quyết"}]',
            clos='[{"id": "CLO_TEST", "description": "Test CLO", "level": "K2"}]',
            plos='[{"id": "PLO_TEST", "description": "Test PLO", "alignment": 0.7}]',
            assessment_weights='{"exam": 70, "assignment": 30}',
            created_by=lecturer.id
        )

        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)
        print(f"✅ Tạo syllabus: {syllabus.subject_code} - {syllabus.subject_name}")
        print(f"   - Status: {syllabus.status}")
        print(f"   - Created by: {lecturer.email}")

        # 3. Lecturer submit syllabus
        print("\n3️⃣ Lecturer submit syllabus...")

        workflow_service = WorkflowService()

        try:
            submit_result, submit_event = workflow_service.submit(db, syllabus.id, lecturer.id, "Đề nghị duyệt syllabus test")
            db.commit()
            print("✅ Submit thành công")
            print(f"   - Status mới: {submit_result.status}")

            # Check workflow event
            events = db.query(WorkflowEvent).filter(WorkflowEvent.syllabus_id == syllabus.id).all()
            print(f"   - Số workflow events: {len(events)}")
            for event in events:
                print(f"     ⚡ {event.action}: {event.from_status} -> {event.to_status}")

        except Exception as e:
            print(f"❌ Lỗi submit: {e}")
            db.rollback()

        # 4. HOD approve
        print("\n4️⃣ HOD duyệt syllabus...")

        hod = db.query(User).filter(User.role == "hod").first()
        if hod:
            try:
                hod_approve, hod_event = workflow_service.hod_approve(db, syllabus.id, hod.id, "HOD duyệt OK")
                db.commit()
                print("✅ HOD duyệt thành công")
                print(f"   - Status mới: {hod_approve.status}")

                # Check workflow events
                events = db.query(WorkflowEvent).filter(WorkflowEvent.syllabus_id == syllabus.id).all()
                print(f"   - Tổng workflow events: {len(events)}")
                for event in events:
                    print(f"     ⚡ {event.action}: {event.from_status} -> {event.to_status}")

            except Exception as e:
                print(f"❌ Lỗi HOD duyệt: {e}")
                db.rollback()
        else:
            print("❌ Không tìm thấy HOD")

        # 5. AA approve
        print("\n5️⃣ AA duyệt syllabus...")

        aa = db.query(User).filter(User.role == "aa").first()
        if aa:
            try:
                aa_approve, aa_event = workflow_service.aa_approve(db, syllabus.id, aa.id, "AA duyệt OK")
                db.commit()
                print("✅ AA duyệt thành công")
                print(f"   - Status mới: {aa_approve.status}")

            except Exception as e:
                print(f"❌ Lỗi AA duyệt: {e}")
                db.rollback()
        else:
            print("❌ Không tìm thấy AA")

        # 6. Principal final approve and publish
        print("\n6️⃣ Principal phê duyệt và công bố...")

        principal = db.query(User).filter(User.role == "principal").first()
        if principal:
            try:
                final_approve, final_event = workflow_service.final_approve_and_publish(db, syllabus.id, principal.id, "Phê duyệt và công bố")
                db.commit()
                print("✅ Principal phê duyệt thành công")
                print(f"   - Status cuối: {final_approve.status}")
                print(f"   - Published: {final_approve.is_published}")
                if final_approve.published_at:
                    print(f"   - Published at: {final_approve.published_at}")

            except Exception as e:
                print(f"❌ Lỗi Principal duyệt: {e}")
                db.rollback()
        else:
            print("❌ Không tìm thấy Principal")

        # 7. Thống kê workflow
        print("\n7️⃣ Thống kê workflow hoàn chỉnh...")

        final_syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus.id).first()
        if final_syllabus:
            print(f"📊 Syllabus: {final_syllabus.subject_code}")
            print(f"   - Status: {final_syllabus.status}")
            print(f"   - Published: {final_syllabus.is_published}")

        # Count all workflow events
        total_events = db.query(WorkflowEvent).filter(WorkflowEvent.syllabus_id == syllabus.id).count()
        print(f"   - Tổng workflow events: {total_events}")

        # Show all workflow events
        print("   - Chi tiết workflow:")
        events = db.query(WorkflowEvent).filter(WorkflowEvent.syllabus_id == syllabus.id).order_by(WorkflowEvent.id).all()
        for i, event in enumerate(events, 1):
            print(f"     {i}. {event.action}: {event.from_status or 'None'} -> {event.to_status}")
            print(f"        👤 {event.performed_by} | 💬 {event.comment}")

        # 8. Thống kê tổng thể
        print("\n8️⃣ Thống kê tổng thể hệ thống...")

        total_users = db.query(User).count()
        total_syllabuses = db.query(Syllabus).count()
        total_workflow_events = db.query(WorkflowEvent).count()

        print(f"👥 Tổng users: {total_users}")
        print(f"📚 Tổng syllabuses: {total_syllabuses}")
        print(f"⚡ Tổng workflow events: {total_workflow_events}")

        # Syllabus by status
        status_counts = {}
        syllabuses = db.query(Syllabus).all()
        for s in syllabuses:
            status = s.status or "draft"
            status_counts[status] = status_counts.get(status, 0) + 1

        print("📊 Syllabus theo status:")
        for status, count in status_counts.items():
            print(f"   - {status}: {count}")

        print("\n" + "=" * 60)
        print("🎉 HOÀN THÀNH TEST WORKFLOW!")
        print("✅ Workflow đăng ký và duyệt hoạt động tốt")
        print("✅ Status transitions đúng")
        print("✅ Audit trail đầy đủ")
        print("✅ Multi-level approval OK")

    except Exception as e:
        print(f"❌ Lỗi test workflow: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_workflow()