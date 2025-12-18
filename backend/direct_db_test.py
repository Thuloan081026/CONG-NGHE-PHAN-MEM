"""Direct database test to debug syllabus creation"""
from app.core.database import engine, SessionLocal
from app.models.syllabus import Syllabus
from sqlalchemy.orm import Session

def test_create_syllabus():
    db = SessionLocal()
    try:
        print("=== Testing Direct Syllabus Creation ===")
        
        # Get a valid user ID
        from app.models.user import User
        lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
        if not lecturer:
            print("❌ Lecturer user not found")
            return
        
        print(f"Using lecturer ID: {lecturer.id}")
        
        # Test 1: Minimal syllabus
        print("\nTest 1: Minimal syllabus (only required fields)")
        syllabus1 = Syllabus(
            subject_code="DIRECT001",
            subject_name="Direct Test",
            created_by=lecturer.id,  # Use actual user ID
            status="draft",
            is_published=False
        )
        db.add(syllabus1)
        db.commit()
        db.refresh(syllabus1)
        print(f"✓ Created syllabus ID: {syllabus1.id}")
        
        # Test 2: With optional fields
        print("\nTest 2: With some optional fields")
        syllabus2 = Syllabus(
            subject_code="DIRECT002",
            subject_name="Direct Test 2",
            created_by=lecturer.id,
            status="draft",
            is_published=False,
            credits=3,
            semester=1,
            department="Test",
            description="Test description",
            content="Test content"
        )
        db.add(syllabus2)
        db.commit()
        db.refresh(syllabus2)
        print(f"✓ Created syllabus ID: {syllabus2.id}")
        
        # Test 3: With JSON fields set to empty list
        print("\nTest 3: With JSON fields as empty lists")
        syllabus3 = Syllabus(
            subject_code="DIRECT003",
            subject_name="Direct Test 3",
            created_by=lecturer.id,
            status="draft",
            is_published=False,
            prerequisites=[],
            corequisites=[],
            textbooks=[]
        )
        db.add(syllabus3)
        db.commit()
        db.refresh(syllabus3)
        print(f"✓ Created syllabus ID: {syllabus3.id}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_create_syllabus()
