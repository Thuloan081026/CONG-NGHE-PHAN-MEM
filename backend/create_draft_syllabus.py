"""Create a draft syllabus for testing Modules 3, 4, 5"""
from app.core.database import SessionLocal
from app.models.syllabus import Syllabus, SyllabusVersion
from app.models.user import User

db = SessionLocal()
try:
    # Get lecturer user
    lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
    if not lecturer:
        print("❌ Lecturer not found")
        exit(1)
    
    print(f"Using lecturer ID: {lecturer.id}")
    
    # Create draft syllabus
    syllabus = Syllabus(
        subject_code="DRAFT001",
        subject_name="Draft Test Syllabus",
        created_by=lecturer.id,
        status="draft",
        is_published=False,
        credits=3,
        semester=1,
        department="Computer Science",
        description="Draft syllabus for workflow testing",
        content="This is a draft syllabus for testing workflow approval"
    )
    db.add(syllabus)
    db.flush()
    
    # Create initial version
    version = SyllabusVersion(
        syllabus_id=syllabus.id,
        version_number=1,
        change_summary="Initial creation",
        change_description="Draft syllabus created for testing",
        subject_code=syllabus.subject_code,
        subject_name=syllabus.subject_name,
        content=syllabus.content,
        changed_fields=[],
        version_status="saved",
        created_by=lecturer.id
    )
    db.add(version)
    db.commit()
    db.refresh(syllabus)
    
    print(f"\n✅ Draft syllabus created!")
    print(f"  ID: {syllabus.id}")
    print(f"  Code: {syllabus.subject_code}")
    print(f"  Status: {syllabus.status}")
    print(f"\nUse this ID for Module 3, 4, 5 testing")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
