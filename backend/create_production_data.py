"""
Create production data for all 6 backend modules in XAMPP database
"""
import sys
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.models.review import Review
from app.core.security import get_password_hash
from app.core.database import Base

def create_all_tables():
    """Create all tables"""
    print("🔨 Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created!")

def create_users(db: Session):
    """Module 1: Authentication + User Management"""
    print("\n📦 MODULE 1: Creating Users (Authentication + User Management)...")
    
    users_data = [
        {"email": "admin@hcmute.edu.vn", "full_name": "System Admin", "role": "admin", "password": "admin123"},
        {"email": "hod.cs@hcmute.edu.vn", "full_name": "Dr. Nguyen Van A", "role": "hod", "password": "hod123"},
        {"email": "lecturer1@hcmute.edu.vn", "full_name": "TS. Tran Thi B", "role": "lecturer", "password": "lecturer123"},
        {"email": "lecturer2@hcmute.edu.vn", "full_name": "ThS. Le Van C", "role": "lecturer", "password": "lecturer123"},
        {"email": "aa@hcmute.edu.vn", "full_name": "Academic Affairs Officer", "role": "academic_affairs", "password": "aa123"},
        {"email": "student1@student.hcmute.edu.vn", "full_name": "Nguyen Van D", "role": "student", "password": "student123"},
        {"email": "student2@student.hcmute.edu.vn", "full_name": "Tran Thi E", "role": "student", "password": "student123"},
    ]
    
    created_users = {}
    for user_data in users_data:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                role=user_data["role"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=1
            )
            db.add(user)
            db.flush()
            created_users[user_data["role"]] = user
            print(f"  ✓ Created {user_data['role']}: {user_data['email']}")
        else:
            created_users[user_data["role"]] = existing
            print(f"  ⚠ User exists: {user_data['email']}")
    
    db.commit()
    return created_users

def create_syllabuses(db: Session, users: dict):
    """Module 2: Syllabus Management"""
    print("\n📦 MODULE 2: Creating Syllabuses (Syllabus Management)...")
    
    syllabuses_data = [
        {
            "subject_code": "IT001",
            "subject_name": "Nhập môn Lập trình",
            "description": "Môn học cung cấp kiến thức nền tảng về lập trình với Python",
            "credits": 4,
            "semester": 1,
            "department": "Công nghệ Thông tin",
            "academic_year": "2024-2025",
            "objectives": "Học sinh nắm được các khái niệm cơ bản về lập trình, cấu trúc dữ liệu và giải thuật",
            "content": "Python basics, Data structures, Algorithms"
        },
        {
            "subject_code": "IT002",
            "subject_name": "Cấu trúc Dữ liệu và Giải thuật",
            "description": "Môn học về các cấu trúc dữ liệu như Array, List, Tree, Graph",
            "credits": 4,
            "semester": 2,
            "department": "Công nghệ Thông tin",
            "academic_year": "2024-2025",
            "objectives": "Hiểu và áp dụng các cấu trúc dữ liệu và giải thuật cơ bản",
            "content": "Array, Linked List, Stack, Queue, Tree, Graph, Sorting, Searching"
        },
        {
            "subject_code": "IT003",
            "subject_name": "Cơ sở Dữ liệu",
            "description": "SQL, ER diagram, normalization, transaction",
            "credits": 3,
            "semester": 1,
            "department": "Công nghệ Thông tin",
            "academic_year": "2024-2025",
            "objectives": "Thiết kế và quản lý cơ sở dữ liệu quan hệ",
            "content": "SQL, Database design, Normalization, Transactions"
        }
    ]
    
    created_syllabuses = []
    for i, syl_data in enumerate(syllabuses_data):
        existing = db.query(Syllabus).filter(Syllabus.subject_code == syl_data["subject_code"]).first()
        if not existing:
            syllabus = Syllabus(
                **syl_data,
                created_by=users["lecturer"].id,
                status="draft"
            )
            db.add(syllabus)
            db.flush()
            created_syllabuses.append(syllabus)
            print(f"  ✓ Created syllabus: {syl_data['subject_code']} - {syl_data['subject_name']}")
        else:
            created_syllabuses.append(existing)
            print(f"  ⚠ Syllabus exists: {syl_data['subject_code']}")
    
    db.commit()
    return created_syllabuses

def create_clos(db: Session, syllabuses: list):
    """Module 5: CLO Management"""
    print("\n📦 MODULE 5a: Creating CLOs (Course Learning Outcomes)...")
    
    created_clos = []
    for i, syllabus in enumerate(syllabuses[:2]):  # First 2 syllabuses
        clo_count = 3 if i == 0 else 4
        for j in range(clo_count):
            existing = db.query(CLO).filter(
                CLO.syllabus_id == syllabus.id,
                CLO.code == f"CLO{j+1}"
            ).first()
            
            if not existing:
                clo = CLO(
                    syllabus_id=syllabus.id,
                    code=f"CLO{j+1}",
                    description=f"Sinh viên có khả năng {['phân tích', 'thiết kế', 'triển khai', 'đánh giá'][j]} các vấn đề trong {syllabus.subject_name}",
                    cognitive_level=["K2", "K3", "K4", "K5"][j],
                    weight=1.0
                )
                db.add(clo)
                db.flush()
                created_clos.append(clo)
                print(f"  ✓ Created CLO{j+1} for {syllabus.subject_code}")
            else:
                created_clos.append(existing)
    
    db.commit()
    return created_clos

def create_plos(db: Session):
    """Module 5: PLO Management"""
    print("\n📦 MODULE 5b: Creating PLOs (Program Learning Outcomes)...")
    
    plos_data = [
        {"code": "PLO1", "description": "Kiến thức nền tảng về Khoa học máy tính", "category": "Knowledge", "program_code": "IT", "program_name": "Information Technology"},
        {"code": "PLO2", "description": "Kỹ năng lập trình và phát triển phần mềm", "category": "Skills", "program_code": "IT", "program_name": "Information Technology"},
        {"code": "PLO3", "description": "Kỹ năng làm việc nhóm và giao tiếp", "category": "Soft Skills", "program_code": "IT", "program_name": "Information Technology"},
        {"code": "PLO4", "description": "Tư duy phản biện và giải quyết vấn đề", "category": "Competence", "program_code": "IT", "program_name": "Information Technology"},
    ]
    
    created_plos = []
    for plo_data in plos_data:
        existing = db.query(PLO).filter(PLO.code == plo_data["code"]).first()
        if not existing:
            plo = PLO(**plo_data, weight=1.0)
            db.add(plo)
            db.flush()
            created_plos.append(plo)
            print(f"  ✓ Created {plo_data['code']}: {plo_data['description'][:50]}...")
        else:
            created_plos.append(existing)
    
    db.commit()
    return created_plos

def create_mappings(db: Session, clos: list, plos: list):
    """Module 5: CLO-PLO Mapping"""
    print("\n📦 MODULE 5c: Creating CLO-PLO Mappings...")
    
    mappings_data = [
        {"clo_idx": 0, "plo_idx": 0, "level": "high", "score": 0.9},
        {"clo_idx": 0, "plo_idx": 1, "level": "medium", "score": 0.6},
        {"clo_idx": 1, "plo_idx": 1, "level": "high", "score": 0.85},
        {"clo_idx": 1, "plo_idx": 3, "level": "medium", "score": 0.7},
        {"clo_idx": 2, "plo_idx": 2, "level": "high", "score": 0.8},
        {"clo_idx": 2, "plo_idx": 3, "level": "high", "score": 0.9},
    ]
    
    count = 0
    for mapping_data in mappings_data:
        if mapping_data["clo_idx"] < len(clos) and mapping_data["plo_idx"] < len(plos):
            clo = clos[mapping_data["clo_idx"]]
            plo = plos[mapping_data["plo_idx"]]
            
            existing = db.query(CLO_PLO_Mapping).filter(
                CLO_PLO_Mapping.clo_id == clo.id,
                CLO_PLO_Mapping.plo_id == plo.id
            ).first()
            
            if not existing:
                mapping = CLO_PLO_Mapping(
                    clo_id=clo.id,
                    plo_id=plo.id,
                    correlation_level=mapping_data["level"],
                    correlation_score=mapping_data["score"],
                    ai_suggested=0,
                    notes=f"Manual mapping between {clo.code} and {plo.code}"
                )
                db.add(mapping)
                count += 1
                print(f"  ✓ Mapped {clo.code} → {plo.code} (level: {mapping_data['level']})")
    
    db.commit()
    print(f"  📊 Total mappings created: {count}")

def create_reviews(db: Session, syllabuses: list, users: dict):
    """Module 4: Collaborative Review"""
    print("\n📦 MODULE 4: Creating Review Comments (Collaborative Review)...")
    
    reviews_data = [
        {
            "syllabus": syllabuses[0],
            "content": "Phần mục tiêu môn học cần bổ sung thêm về kỹ năng thực hành",
            "section": "objectives",
            "user": "hod"
        },
        {
            "syllabus": syllabuses[0],
            "content": "Nội dung môn học rất chi tiết và phù hợp với chuẩn đầu ra",
            "section": "content",
            "user": "lecturer"
        },
        {
            "syllabus": syllabuses[1],
            "content": "Cần thêm ví dụ thực tế về các giải thuật",
            "section": "content",
            "user": "hod"
        },
    ]
    
    count = 0
    for review_data in reviews_data:
        review = Review(
            syllabus_id=review_data["syllabus"].id,
            content=review_data["content"],
            section=review_data["section"],
            created_by=users[review_data["user"]].id,
            is_resolved=0
        )
        db.add(review)
        count += 1
        print(f"  ✓ Created review for {review_data['syllabus'].subject_code}: {review_data['content'][:50]}...")
    
    db.commit()
    print(f"  📊 Total reviews created: {count}")

def main():
    """Main execution"""
    print("=" * 70)
    print("🚀 CREATING PRODUCTION DATA FOR ALL 6 BACKEND MODULES")
    print("=" * 70)
    
    # Create tables
    create_all_tables()
    
    # Create data
    db = SessionLocal()
    try:
        # Module 1: Users
        users = create_users(db)
        
        # Module 2: Syllabuses
        syllabuses = create_syllabuses(db, users)
        
        # Module 5: CLO-PLO
        clos = create_clos(db, syllabuses)
        plos = create_plos(db)
        create_mappings(db, clos, plos)
        
        # Module 4: Reviews
        create_reviews(db, syllabuses, users)
        
        # Module 3: Workflow (data created via API later)
        print("\n📦 MODULE 3: Workflow (submit/approve) - Use API endpoints")
        
        # Module 6: Search (uses existing syllabus data)
        print("📦 MODULE 6: Search - Data ready (uses syllabuses)")
        
        print("\n" + "=" * 70)
        print("✅ ALL PRODUCTION DATA CREATED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📊 SUMMARY:")
        print(f"  • Users: {len(users)} roles")
        print(f"  • Syllabuses: {len(syllabuses)} courses")
        print(f"  • CLOs: {len(clos)} learning outcomes")
        print(f"  • PLOs: {len(plos)} program outcomes")
        print(f"  • Reviews: Created for collaboration")
        print("\n🔐 LOGIN CREDENTIALS:")
        print("  Admin: admin@hcmute.edu.vn / admin123")
        print("  HOD: hod.cs@hcmute.edu.vn / hod123")
        print("  Lecturer: lecturer1@hcmute.edu.vn / lecturer123")
        print("  Student: student1@student.hcmute.edu.vn / student123")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
