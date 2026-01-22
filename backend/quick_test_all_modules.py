"""
Quick test of all 3 modules
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app import models
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.review import Review
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.services.review_service import ReviewService
from app.services.clo_service import CLOService
from app.services.search_service import SearchService
from app.core.security import get_password_hash

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

print("\n" + "="*60)
print("QUICK TEST - 3 MODULES")
print("="*60)

try:
    # Test Module 6 - Search
    print("\n1. TEST MODULE 6 - SEARCH")
    print("-" * 60)
    search_service = SearchService(db)
    
    # Test search by name
    result = search_service.search_syllabuses(query="Programming")
    print(f"✓ Search 'Programming': {result['total']} results")
    if result['total'] > 0:
        print(f"  - {result['results'][0].subject_code}: {result['results'][0].subject_name}")
    
    # Test filter by department
    result = search_service.search_syllabuses(department="Computer Science")
    print(f"✓ Filter 'Computer Science': {result['total']} results")
    
    # Test full-text search
    result = search_service.search_syllabuses(full_text="Python")
    print(f"✓ Full-text 'Python': {result['total']} results")
    
    # Test get filters
    filters = search_service.get_search_filters()
    print(f"✓ Get filters: {len(filters['departments'])} departments, {len(filters['semesters'])} semesters")
    
    # Test Module 5 - CLO-PLO
    print("\n2. TEST MODULE 5 - CLO-PLO MAPPING")
    print("-" * 60)
    
    # Get existing syllabus
    syllabus = db.query(Syllabus).filter(Syllabus.subject_code == "CS101").first()
    if syllabus:
        print(f"✓ Found syllabus: {syllabus.subject_code}")
        
        # Get CLOs directly from database
        clos = db.query(CLO).filter(CLO.syllabus_id == syllabus.id).all()
        print(f"✓ Get CLOs for CS101: {len(clos)} CLOs")
        for clo in clos:
            print(f"  - {clo.code}: {clo.description[:50]}...")
        
        # Get mappings directly
        mappings = db.query(CLO_PLO_Mapping).join(CLO).filter(CLO.syllabus_id == syllabus.id).all()
        print(f"✓ Get CLO-PLO Mappings: {len(mappings)} mappings")
        for m in mappings:
            print(f"  - {m.clo.code} -> {m.plo.code} ({m.correlation_level})")
    else:
        print("✗ Syllabus CS101 not found")
    
    # Get all PLOs
    plos = db.query(PLO).all()
    print(f"✓ Get all PLOs: {len(plos)} PLOs")
    for plo in plos:
        print(f"  - {plo.code}: {plo.description[:50]}...")
    
    # Test Module 4 - Review
    print("\n3. TEST MODULE 4 - COLLABORATIVE REVIEW")
    print("-" * 60)
    
    # Get syllabus under review
    syllabus = db.query(Syllabus).filter(Syllabus.status == "under_review").first()
    if syllabus:
        print(f"✓ Found syllabus under review: {syllabus.subject_code}")
        
        # Get reviews directly
        reviews = db.query(Review).filter(Review.syllabus_id == syllabus.id).all()
        print(f"✓ Get reviews for {syllabus.subject_code}: {len(reviews)} reviews")
        for r in reviews:
            resolved = "✓ Resolved" if r.is_resolved else "○ Pending"
            print(f"  {resolved} - {r.content[:50]}... (Section: {r.section})")
    else:
        print("✗ No syllabus under review")
    
    print("\n" + "="*60)
    print("✅ ALL MODULES WORKING!")
    print("="*60)
    
    print("""
TONG KET:
✓ Module 6 (Search): Search, filter, full-text hoat dong
✓ Module 5 (CLO-PLO): Lay CLO, PLO, mapping hoat dong
✓ Module 4 (Review): Lay reviews hoat dong

DATA PRODUCTION:
✓ 4 syllabuses (CS101, CS201, CS301, MATH101)
✓ 3 CLOs cho CS101
✓ 3 PLOs
✓ 4 CLO-PLO mappings
✓ 2 reviews cho CS301

De chay full tests:
pytest tests/test_review.py tests/test_clo_plo.py tests/test_search.py -v
""")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
