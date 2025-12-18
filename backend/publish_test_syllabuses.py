"""Publish the test syllabuses"""
from app.core.database import SessionLocal
from app.models.syllabus import Syllabus

db = SessionLocal()
try:
    # Get syllabuses 160, 161, 162
    syllabuses = db.query(Syllabus).filter(Syllabus.id.in_([160, 161, 162])).all()
    
    for syl in syllabuses:
        syl.status = "published"
        syl.is_published = True
        print(f"Published syllabus {syl.id}: {syl.subject_code}")
    
    db.commit()
    print("\n✅ All syllabuses published!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
