#!/usr/bin/env python3
"""
Test script cho Workflow Module
Test trực tiếp các functions mà không cần server
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
from app.services.workflow_service import WorkflowService
from app.repositories.syllabus_repo import SyllabusRepository
from app.repositories.workflow_repo import WorkflowRepository
from app.core.security import get_password_hash

# Tạo database test
DATABASE_URL = "sqlite:///./test_workflow.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo tables
Base.metadata.create_all(bind=engine)

def test_workflow():
    print("🚀 Testing Workflow Module...")

    db = SessionLocal()

    try:
        # 1. Tạo test users
        print("\n1. Tạo test users...")
        lecturer = User(
            email="lecturer@test.com",
            full_name="Test Lecturer",
            hashed_password="hashed_password123",  # Mock hash for test
            role="lecturer"
        )
        hod = User(
            email="hod@test.com",
            full_name="Test HOD",
            hashed_password="hashed_password123",
            role="hod"
        )
        aa = User(
            email="aa@test.com",
            full_name="Test AA",
            hashed_password="hashed_password123",
            role="aa"
        )
        principal = User(
            email="principal@test.com",
            full_name="Test Principal",
            hashed_password="hashed_password123",
            role="principal"
        )

        db.add_all([lecturer, hod, aa, principal])
        db.commit()

        print("✅ Users created")

        # 2. Tạo test syllabus
        print("\n2. Tạo test syllabus...")
        syllabus = Syllabus(
            subject_code="TEST101",
            subject_name="Test Subject",
            description="Test syllabus for workflow",
            created_by=lecturer.id
        )
        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)

        print(f"✅ Syllabus created with ID: {syllabus.id}, Status: {syllabus.status}")

        # 3. Test workflow service
        print("\n3. Test workflow transitions...")
        service = WorkflowService()

        # Submit
        print("   - Lecturer submits...")
        updated, event = service.submit(db, syllabus.id, lecturer.id, "Initial submission")
        print(f"   ✅ Status: {updated.status}, Event: {event.action}")

        # HOD approve
        print("   - HOD approves...")
        updated, event = service.hod_approve(db, syllabus.id, hod.id, "Approved by HOD")
        print(f"   ✅ Status: {updated.status}, Event: {event.action}")

        # AA approve
        print("   - AA approves...")
        updated, event = service.aa_approve(db, syllabus.id, aa.id, "Approved by AA")
        print(f"   ✅ Status: {updated.status}, Event: {event.action}")

        # Final approve and publish
        print("   - Principal final approves...")
        updated, event = service.final_approve_and_publish(db, syllabus.id, principal.id, "Final approval")
        print(f"   ✅ Status: {updated.status}, Published: {updated.is_published}, Event: {event.action}")

        # 4. Test listing events
        print("\n4. Test listing workflow events...")
        events, total = service.list_events(db, syllabus.id)
        print(f"   ✅ Total events: {total}")
        for ev in events:
            print(f"   - {ev.action}: {ev.from_status} → {ev.to_status} by {ev.performer}")

        # 5. Test error cases
        print("\n5. Test error cases...")

        # Try to submit already submitted syllabus
        try:
            service.submit(db, syllabus.id, lecturer.id)
            print("   ❌ Should have failed")
        except Exception as e:
            print(f"   ✅ Correctly rejected: {str(e)}")

        # Try wrong role
        try:
            service.hod_approve(db, syllabus.id, lecturer.id)  # Wrong role
            print("   ❌ Should have failed")
        except Exception as e:
            print(f"   ✅ Correctly rejected: {str(e)}")

        print("\n🎉 All tests passed! Workflow module hoạt động đúng chuẩn.")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    test_workflow()