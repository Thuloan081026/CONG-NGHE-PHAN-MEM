"""
Create demo data for Module 7 & 8 testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.notification import Notification, SyllabusFollow
from app.models.user import User
from app.models.syllabus import Syllabus, SyllabusVersion
from datetime import datetime

def create_demo_data():
    """Create demo notifications and follows"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("  CREATING DEMO DATA FOR MODULE 7 & 8")
        print("="*60 + "\n")
        
        # Get users
        admin = db.query(User).filter(User.email == "admin@test.com").first()
        student = db.query(User).filter(User.email == "student@test.com").first()
        lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
        
        if not admin or not student or not lecturer:
            print("❌ Users not found. Run create_test_users.py first")
            return
        
        print(f"✓ Found users:")
        print(f"  Admin: {admin.email} (ID: {admin.id})")
        print(f"  Student: {student.email} (ID: {student.id})")
        print(f"  Lecturer: {lecturer.email} (ID: {lecturer.id})")
        
        # Get syllabus
        syllabus = db.query(Syllabus).first()
        if not syllabus:
            print("\n❌ No syllabus found. Creating demo syllabus...")
            syllabus = Syllabus(
                subject_code="CS101",
                subject_name="Introduction to Computer Science",
                credits=3,
                semester="1",
                department="Computer Science",
                description="Basic programming concepts",
                status="approved"
            )
            db.add(syllabus)
            db.commit()
            db.refresh(syllabus)
            print(f"✓ Created syllabus: {syllabus.subject_code}")
        else:
            print(f"\n✓ Found syllabus: {syllabus.subject_code} - {syllabus.subject_name}")
        
        # Create syllabus versions for diff testing
        print("\n📦 Creating syllabus versions for AI Diff testing...")
        version1 = db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus.id,
            SyllabusVersion.version_number == 1
        ).first()
        
        if not version1:
            version1 = SyllabusVersion(
                syllabus_id=syllabus.id,
                version_number=1,
                subject_code=syllabus.subject_code,
                subject_name=syllabus.subject_name,
                content="Version 1: Basic programming, variables, loops, functions",
                created_by=lecturer.id,
                change_description="Initial version"
            )
            db.add(version1)
            print("  ✓ Created Version 1")
        else:
            print("  ✓ Version 1 already exists")
        
        version2 = db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus.id,
            SyllabusVersion.version_number == 2
        ).first()
        
        if not version2:
            version2 = SyllabusVersion(
                syllabus_id=syllabus.id,
                version_number=2,
                subject_code=syllabus.subject_code,
                subject_name=syllabus.subject_name + " - Updated",
                content="Version 2: Advanced topics, OOP, data structures, algorithms",
                created_by=lecturer.id,
                change_description="Added advanced topics and OOP"
            )
            db.add(version2)
            print("  ✓ Created Version 2")
        else:
            print("  ✓ Version 2 already exists")
        
        db.commit()
        
        # Create student follow
        print("\n👥 Creating student follow...")
        follow = db.query(SyllabusFollow).filter(
            SyllabusFollow.user_id == student.id,
            SyllabusFollow.syllabus_id == syllabus.id
        ).first()
        
        if not follow:
            follow = SyllabusFollow(
                user_id=student.id,
                syllabus_id=syllabus.id
            )
            db.add(follow)
            print(f"  ✓ Student {student.email} now follows {syllabus.subject_code}")
        else:
            print(f"  ✓ Student already follows syllabus")
        
        # Create notifications
        print("\n📬 Creating demo notifications...")
        
        # Notification 1: Welcome
        notif1 = db.query(Notification).filter(
            Notification.user_id == student.id,
            Notification.title == "Welcome to Syllabus Management System"
        ).first()
        
        if not notif1:
            notif1 = Notification(
                user_id=student.id,
                title="Welcome to Syllabus Management System",
                message="Thank you for joining! You can now follow syllabuses and receive updates.",
                notification_type="system",
                is_read=False
            )
            db.add(notif1)
            print("  ✓ Created welcome notification for student")
        
        # Notification 2: Syllabus update
        notif2 = db.query(Notification).filter(
            Notification.user_id == student.id,
            Notification.syllabus_id == syllabus.id,
            Notification.notification_type == "update"
        ).first()
        
        if not notif2:
            notif2 = Notification(
                user_id=student.id,
                syllabus_id=syllabus.id,
                title=f"Syllabus Updated: {syllabus.subject_code}",
                message=f"The syllabus '{syllabus.subject_name}' has been updated. Check the latest version.",
                notification_type="update",
                is_read=False
            )
            db.add(notif2)
            print("  ✓ Created update notification for student")
        
        # Notification 3: Lecturer approval
        notif3 = db.query(Notification).filter(
            Notification.user_id == lecturer.id,
            Notification.notification_type == "approve"
        ).first()
        
        if not notif3:
            notif3 = Notification(
                user_id=lecturer.id,
                syllabus_id=syllabus.id,
                title="Syllabus Approved",
                message=f"Your syllabus '{syllabus.subject_code}' has been approved by admin.",
                notification_type="approve",
                is_read=False
            )
            db.add(notif3)
            print("  ✓ Created approval notification for lecturer")
        
        db.commit()
        
        # Summary
        print("\n" + "="*60)
        print("  DEMO DATA CREATED SUCCESSFULLY")
        print("="*60 + "\n")
        
        notif_count = db.query(Notification).count()
        follow_count = db.query(SyllabusFollow).count()
        version_count = db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus.id
        ).count()
        
        print(f"📊 Database Status:")
        print(f"   Notifications: {notif_count} records")
        print(f"   Follows: {follow_count} records")
        print(f"   Syllabus Versions: {version_count} records")
        
        print(f"\n🎯 Test Data Ready:")
        print(f"   Syllabus ID: {syllabus.id}")
        print(f"   Version 1 ID: {version1.id if version1 else 'N/A'}")
        print(f"   Version 2 ID: {version2.id if version2 else 'N/A'}")
        print(f"   Student ID: {student.id}")
        print(f"   Lecturer ID: {lecturer.id}")
        
        print(f"\n✅ Ready to test:")
        print(f"   1. AI Summarize: syllabus_id={syllabus.id}")
        print(f"   2. AI Diff: version_id_1={version1.id if version1 else 'N/A'}, version_id_2={version2.id if version2 else 'N/A'}")
        print(f"   3. Notifications: Login as student@test.com")
        print(f"   4. Follow: Student already follows syllabus {syllabus.id}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data()
