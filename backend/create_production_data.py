"""
Create Production Sample Data
Tao du lieu mau cho production (khong bi xoa sau khi test)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from app.core.database import Base
from app import models  # Import all models
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.models.review import Review
from app.core.security import get_password_hash

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    print("\n" + "="*60)
    print("TAO DU LIEU MAU CHO PRODUCTION")
    print("="*60)
    
    # Cleanup existing data first
    print("\n0. Xoa du lieu cu...")
    try:
        from app.models.workflow import WorkflowEvent
        db.query(WorkflowEvent).delete()
        db.query(Review).delete()
        db.query(CLO_PLO_Mapping).delete()
        db.query(CLO).delete()
        db.query(PLO).delete()
        db.query(Syllabus).delete()
        db.query(User).delete()
        db.commit()
        print("   ✓ Da xoa du lieu cu!")
    except Exception as e:
        print(f"   ⚠ Khong co du lieu cu hoac loi: {e}")
        db.rollback()
    
    # 1. Create Users
    print("\n1. Tao Users...")
    
    users_data = [
        {
            "email": "lecturer1@university.edu",
            "full_name": "Dr. Nguyen Van A",
            "password": "lecturer123",
            "role": "lecturer"
        },
        {
            "email": "lecturer2@university.edu",
            "full_name": "Dr. Tran Thi B",
            "password": "lecturer123",
            "role": "lecturer"
        },
        {
            "email": "hod@university.edu",
            "full_name": "Prof. Le Van C",
            "password": "hod123",
            "role": "hod"
        },
        {
            "email": "student@university.edu",
            "full_name": "Nguyen Van Student",
            "password": "student123",
            "role": "student"
        }
    ]
    
    users = []
    for data in users_data:
        user = User(
            email=data["email"],
            full_name=data["full_name"],
            hashed_password=get_password_hash(data["password"]),
            role=data["role"],
            is_active=True
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    for u in users:
        db.refresh(u)
    print(f"   ✓ Tao {len(users)} users thanh cong!")
    
    # 2. Create Syllabuses
    print("\n2. Tao Syllabuses...")
    
    syllabuses_data = [
        {
            "subject_code": "CS101",
            "subject_name": "Introduction to Programming",
            "description": "Learn fundamental programming concepts using Python",
            "department": "Computer Science",
            "semester": 1,
            "credits": 3,
            "academic_year": "2024-2025",
            "objectives": "Master basic programming, understand algorithms, develop problem-solving skills",
            "content": "Variables, data types, control structures, functions, OOP basics",
            "teaching_methods": "Lectures, lab sessions, practical projects",
            "assessment_methods": "Assignments (30%), Midterm (30%), Final exam (40%)",
            "status": "published",
            "is_published": True
        },
        {
            "subject_code": "CS201",
            "subject_name": "Data Structures and Algorithms",
            "description": "Advanced data structures and algorithm design",
            "department": "Computer Science",
            "semester": 3,
            "credits": 4,
            "academic_year": "2024-2025",
            "objectives": "Master data structures, analyze algorithms, implement efficient solutions",
            "content": "Arrays, linked lists, stacks, queues, trees, graphs, sorting, searching",
            "teaching_methods": "Theory lectures, coding exercises, algorithm analysis",
            "assessment_methods": "Labs (20%), Assignments (30%), Exams (50%)",
            "status": "published",
            "is_published": True
        },
        {
            "subject_code": "CS301",
            "subject_name": "Database Systems",
            "description": "Database design, SQL, and database management",
            "department": "Computer Science",
            "semester": 5,
            "credits": 3,
            "academic_year": "2025-2026",
            "objectives": "Understand database concepts, master SQL, design normalized databases",
            "content": "ER modeling, normalization, SQL queries, transactions, indexing",
            "teaching_methods": "Lectures, SQL labs, database design projects",
            "assessment_methods": "Labs (25%), Project (35%), Final exam (40%)",
            "status": "under_review",
            "is_published": False
        },
        {
            "subject_code": "MATH101",
            "subject_name": "Calculus I",
            "description": "Differential calculus and applications",
            "department": "Mathematics",
            "semester": 1,
            "credits": 4,
            "academic_year": "2024-2025",
            "objectives": "Master derivatives, limits, and applications",
            "content": "Limits, continuity, derivatives, applications of derivatives",
            "teaching_methods": "Lectures, problem-solving sessions",
            "assessment_methods": "Quizzes (20%), Midterm (30%), Final (50%)",
            "status": "published",
            "is_published": True
        }
    ]
    
    syllabuses = []
    for i, data in enumerate(syllabuses_data):
        syllabus = Syllabus(
            **{k: v for k, v in data.items()},
            created_by=users[i % 2].id,  # Alternate between lecturers
            published_at=datetime.now(UTC) if data["is_published"] else None
        )
        db.add(syllabus)
        syllabuses.append(syllabus)
    
    db.commit()
    for s in syllabuses:
        db.refresh(s)
    print(f"   ✓ Tao {len(syllabuses)} syllabuses thanh cong!")
    
    # 3. Create CLOs for CS101
    print("\n3. Tao CLOs cho CS101...")
    
    clos_data = [
        {
            "code": "CLO1",
            "description": "Understand basic programming concepts and syntax",
            "cognitive_level": "K2"
        },
        {
            "code": "CLO2",
            "description": "Apply programming concepts to solve simple problems",
            "cognitive_level": "K3"
        },
        {
            "code": "CLO3",
            "description": "Design and implement object-oriented programs",
            "cognitive_level": "K4"
        }
    ]
    
    clos = []
    for data in clos_data:
        clo = CLO(
            syllabus_id=syllabuses[0].id,  # CS101
            **data
        )
        db.add(clo)
        clos.append(clo)
    
    db.commit()
    for c in clos:
        db.refresh(c)
    print(f"   ✓ Tao {len(clos)} CLOs thanh cong!")
    
    # 4. Create PLOs
    print("\n4. Tao PLOs...")
    
    plos_data = [
        {
            "code": "PLO1",
            "description": "Apply knowledge of computing fundamentals",
            "program_name": "Computer Science"
        },
        {
            "code": "PLO2",
            "description": "Design and implement software solutions",
            "program_name": "Computer Science"
        },
        {
            "code": "PLO3",
            "description": "Analyze and solve complex problems",
            "program_name": "Computer Science"
        }
    ]
    
    plos = []
    for data in plos_data:
        plo = PLO(**data)
        db.add(plo)
        plos.append(plo)
    
    db.commit()
    for p in plos:
        db.refresh(p)
    print(f"   ✓ Tao {len(plos)} PLOs thanh cong!")
    
    # 5. Create CLO-PLO Mappings
    print("\n5. Tao CLO-PLO Mappings...")
    
    mappings_data = [
        {"clo_id": clos[0].id, "plo_id": plos[0].id, "correlation_level": "High", "correlation_score": 0.9},
        {"clo_id": clos[1].id, "plo_id": plos[0].id, "correlation_level": "Medium", "correlation_score": 0.7},
        {"clo_id": clos[1].id, "plo_id": plos[2].id, "correlation_level": "High", "correlation_score": 0.8},
        {"clo_id": clos[2].id, "plo_id": plos[1].id, "correlation_level": "High", "correlation_score": 0.9},
    ]
    
    mappings = []
    for data in mappings_data:
        mapping = CLO_PLO_Mapping(**data)
        db.add(mapping)
        mappings.append(mapping)
    
    db.commit()
    print(f"   ✓ Tao {len(mappings)} mappings thanh cong!")
    
    # 6. Create Reviews
    print("\n6. Tao Reviews...")
    
    reviews_data = [
        {
            "syllabus_id": syllabuses[2].id,  # CS301 (under_review)
            "created_by": users[1].id,  # Lecturer 2
            "content": "Great content! Suggest adding more practical examples in Section 3.",
            "section": "Content",
            "is_resolved": 0
        },
        {
            "syllabus_id": syllabuses[2].id,
            "created_by": users[2].id,  # HOD
            "content": "Please update the assessment weights to match department standards.",
            "section": "Assessment",
            "is_resolved": 0
        }
    ]
    
    reviews = []
    for data in reviews_data:
        review = Review(**data)
        db.add(review)
        reviews.append(review)
    
    db.commit()
    print(f"   ✓ Tao {len(reviews)} reviews thanh cong!")
    
    print("\n" + "="*60)
    print("HOAN THANH TAO DU LIEU MAU!")
    print("="*60)
    
    print(f"""
✓ {len(users)} users
✓ {len(syllabuses)} syllabuses ({sum(1 for s in syllabuses if s.is_published)} published)
✓ {len(clos)} CLOs
✓ {len(plos)} PLOs
✓ {len(mappings)} CLO-PLO mappings
✓ {len(reviews)} reviews

THONG TIN DANG NHAP:
- Lecturer 1: lecturer1@university.edu / lecturer123
- Lecturer 2: lecturer2@university.edu / lecturer123
- HOD: hod@university.edu / hod123
- Student: student@university.edu / student123

XEM DU LIEU:
- phpMyAdmin: http://localhost/phpmyadmin
- Database: syllabus_db
""")
    
except Exception as e:
    print(f"\n❌ LOI: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
