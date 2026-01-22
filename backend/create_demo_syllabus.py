"""
Create demo syllabus data for testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.syllabus import Syllabus, SyllabusVersion
from app.models.clo import CLO
from app.models.user import User
from datetime import datetime

def create_demo_data():
    """Create demo syllabus and CLOs"""
    db = SessionLocal()
    
    try:
        # Get admin user
        admin = db.query(User).filter(User.email == "admin@test.com").first()
        if not admin:
            print("✗ Admin user not found. Run create_test_users.py first!")
            return
        
        # Check if syllabus exists
        existing = db.query(Syllabus).filter(Syllabus.subject_code == "CS101").first()
        if existing:
            print("✓ Demo syllabus already exists")
            print(f"  ID: {existing.id}")
            print(f"  Code: {existing.subject_code}")
            print(f"  Name: {existing.subject_name}")
            return
        
        # Create demo syllabus
        print("Creating demo syllabus...")
        syllabus = Syllabus(
            subject_code="CS101",
            subject_name="Nhập môn Lập trình",
            credits=3,
            semester="Fall 2024",
            department="Khoa Công nghệ Thông tin",
            created_by=admin.id,
            status="approved",
            description="""
Môn học cung cấp kiến thức cơ bản về lập trình máy tính, giới thiệu ngôn ngữ Python.
Sinh viên sẽ học cách tư duy lập trình, thiết kế thuật toán và giải quyết vấn đề.
            """.strip(),
            objectives="""
- Hiểu các khái niệm cơ bản về lập trình
- Nắm vững cú pháp Python
- Áp dụng thuật toán để giải quyết vấn đề
- Phát triển kỹ năng debugging
            """.strip(),
            content="""
1. Giới thiệu về lập trình
2. Biến và kiểu dữ liệu
3. Cấu trúc điều khiển
4. Hàm và module
5. Cấu trúc dữ liệu
6. File và Exception
7. Lập trình hướng đối tượng
8. Project cuối kỳ
            """.strip(),
            teaching_methods="Giảng lý thuyết, thực hành trên máy, project nhóm",
            assessment_methods="Giữa kỳ 30%, Cuối kỳ 40%, Project 20%, Bài tập 10%"
        )
        db.add(syllabus)
        db.flush()
        
        print(f"✓ Syllabus created: {syllabus.subject_code} - {syllabus.subject_name}")
        
        # Create version
        version = SyllabusVersion(
            syllabus_id=syllabus.id,
            version_number="1.0",
            subject_name=syllabus.subject_name,
            content=syllabus.content,
            created_by=admin.id,
            change_description="Initial version"
        )
        db.add(version)
        
        # Create another version for diff testing
        version2 = SyllabusVersion(
            syllabus_id=syllabus.id,
            version_number="1.1",
            subject_name=syllabus.subject_name,
            content=syllabus.content + "\n9. Bonus: Web scraping",
            created_by=admin.id,
            change_description="Added web scraping topic"
        )
        db.add(version2)
        
        print(f"✓ Created 2 versions for diff testing")
        
        # Create CLOs
        clos = [
            {
                "code": "CLO1",
                "description": "Sinh viên có khả năng viết chương trình Python cơ bản để giải quyết vấn đề đơn giản",
                "plo_mapping": "PLO1, PLO2"
            },
            {
                "code": "CLO2",
                "description": "Sinh viên hiểu và áp dụng các cấu trúc dữ liệu phổ biến như list, dict, tuple",
                "plo_mapping": "PLO2, PLO3"
            },
            {
                "code": "CLO3",
                "description": "Sinh viên có kỹ năng debug và xử lý lỗi trong chương trình Python",
                "plo_mapping": "PLO3, PLO4"
            }
        ]
        
        for clo_data in clos:
            clo = CLO(
                syllabus_id=syllabus.id,
                code=clo_data["code"],
                description=clo_data["description"],
                plo_mapping=clo_data["plo_mapping"],
                created_by=admin.id
            )
            db.add(clo)
        
        print(f"✓ Created {len(clos)} CLOs")
        
        db.commit()
        print("\n✅ Demo data created successfully!")
        print(f"\nSyllabus ID: {syllabus.id}")
        print(f"Subject Code: {syllabus.subject_code}")
        print(f"Subject Name: {syllabus.subject_name}")
        print(f"Versions: 2 (for diff testing)")
        print(f"CLOs: 3 (for similarity testing)")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating demo data...\n")
    create_demo_data()
