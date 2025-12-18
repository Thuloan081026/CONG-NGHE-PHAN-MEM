"""
Simple test to check search functionality
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import all models
from app.core.database import Base
from app.models.user import User
from app.models.syllabus import Syllabus, SyllabusVersion
from app.models.workflow import WorkflowEvent
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.models.review import Review
from app.services.search_service import SearchService

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Clean up - delete in proper order to respect foreign keys
    db.query(Review).delete()
    db.query(CLO_PLO_Mapping).delete()
    db.query(CLO).delete()
    db.query(PLO).delete()
    db.query(WorkflowEvent).delete()
    db.query(SyllabusVersion).delete()
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Database cleaned")
    
    # Create test user
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="test_hash",
        role="lecturer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✓ User created: {user.email}")
    
    # Create test syllabuses
    syllabuses = [
        Syllabus(
            subject_code="CS101",
            subject_name="Introduction to Programming",
            description="Basic programming",
            department="Computer Science",
            semester=1,
            credits=3,
            academic_year="2024-2025",
            objectives="Learn programming",
            content="Python, Java",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        Syllabus(
            subject_code="MATH101",
            subject_name="Calculus I",
            description="Differential calculus",
            department="Mathematics",
            semester=1,
            credits=4,
            academic_year="2024-2025",
            objectives="Master calculus",
            content="Derivatives, limits",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        )
    ]
    
    for s in syllabuses:
        db.add(s)
    db.commit()
    print(f"✓ Created {len(syllabuses)} syllabuses")
    
    # Test search service
    service = SearchService(db)
    
    # Test 1: Search by name
    print("\n=== Test 1: Search by 'Programming' ===")
    result = service.search_syllabuses(query="Programming")
    print(f"Found: {result['total']} results")
    for s in result['results']:
        print(f"  - {s.subject_code}: {s.subject_name}")
    
    # Test 2: Filter by department
    print("\n=== Test 2: Filter by Computer Science ===")
    result = service.search_syllabuses(department="Computer Science")
    print(f"Found: {result['total']} results")
    for s in result['results']:
        print(f"  - {s.subject_code}: {s.subject_name}")
    
    # Test 3: Filter by semester
    print("\n=== Test 3: Filter by semester 1 ===")
    result = service.search_syllabuses(semester=1)
    print(f"Found: {result['total']} results")
    for s in result['results']:
        print(f"  - {s.subject_code}: {s.subject_name}")
    
    # Test 4: Full-text search
    print("\n=== Test 4: Full-text search for 'Python' ===")
    result = service.search_syllabuses(full_text="Python")
    print(f"Found: {result['total']} results")
    for s in result['results']:
        print(f"  - {s.subject_code}: {s.subject_name}")
    
    # Test 5: Get filters
    print("\n=== Test 5: Get available filters ===")
    filters = service.get_search_filters()
    print(f"Departments: {filters['departments']}")
    print(f"Semesters: {filters['semesters']}")
    print(f"Academic years: {filters['academic_years']}")
    
    # Test 6: Search by code
    print("\n=== Test 6: Search by code 'CS101' ===")
    syllabus = service.search_by_code("CS101")
    if syllabus:
        print(f"Found: {syllabus.subject_code} - {syllabus.subject_name}")
    else:
        print("Not found")
    
    print("\n✅ ALL TESTS PASSED!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
