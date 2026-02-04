#!/usr/bin/env python
"""Create demo syllabuses for lecturer@edu.vn"""
from app.core.database import SessionLocal
from app.models.user import User
from app.models.syllabus import Syllabus
from datetime import datetime

db = SessionLocal()

# Get lecturer@edu.vn user
lecturer = db.query(User).filter(User.email == 'lecturer@edu.vn').first()
if not lecturer:
    print("❌ lecturer@edu.vn not found!")
    exit(1)

print(f"✅ Found lecturer: {lecturer.full_name} (ID: {lecturer.id})")

# Create syllabuses
syllabuses_data = [
    {
        "subject_code": "SE101",
        "subject_name": "Nhập môn Kỹ thuật Phần mềm",
        "description": "Giới thiệu cơ bản về kỹ thuật phần mềm",
        "credits": 3,
        "semester": 1,
        "department": "Bộ môn Hệ thống Thông tin",
        "academic_year": "2025-2026",
        "status": "published",
        "is_published": True
    },
    {
        "subject_code": "SE102",
        "subject_name": "Thiết kế Phần mềm",
        "description": "Các mô hình và kiến trúc thiết kế phần mềm",
        "credits": 3,
        "semester": 2,
        "department": "Bộ môn Hệ thống Thông tin",
        "academic_year": "2025-2026",
        "status": "published",
        "is_published": True
    },
    {
        "subject_code": "SE103",
        "subject_name": "Testing và Đảm bảo Chất lượng",
        "description": "Kiểm thử và QA trong phát triển phần mềm",
        "credits": 4,
        "semester": 3,
        "department": "Bộ môn Hệ thống Thông tin",
        "academic_year": "2025-2026",
        "status": "published",
        "is_published": True
    },
    {
        "subject_code": "SE104",
        "subject_name": "Phát triển Ứng dụng Web",
        "description": "Xây dựng ứng dụng web hiện đại",
        "credits": 4,
        "semester": 4,
        "department": "Bộ môn Hệ thống Thông tin",
        "academic_year": "2025-2026",
        "status": "submitted",
        "is_published": False
    },
    {
        "subject_code": "SE105",
        "subject_name": "DevOps và Deployment",
        "description": "Triển khai và quản lý hạ tầng",
        "credits": 3,
        "semester": 5,
        "department": "Bộ môn Hệ thống Thông tin",
        "academic_year": "2025-2026",
        "status": "draft",
        "is_published": False
    }
]

created_count = 0
for data in syllabuses_data:
    # Check if already exists
    existing = db.query(Syllabus).filter(Syllabus.subject_code == data["subject_code"]).first()
    if existing:
        print(f"⏭️  {data['subject_code']} - Đã tồn tại, bỏ qua")
        continue
    
    syllabus = Syllabus(
        subject_code=data["subject_code"],
        subject_name=data["subject_name"],
        description=data.get("description"),
        credits=data.get("credits"),
        semester=data.get("semester"),
        department=data.get("department"),
        academic_year=data.get("academic_year"),
        created_by=lecturer.id,
        status=data.get("status", "draft"),
        is_published=data.get("is_published", False),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(syllabus)
    created_count += 1
    print(f"✅ Created: {data['subject_code']} - {data['subject_name']} (Status: {data['status']})")

db.commit()
db.close()

print(f"\n🎉 Created {created_count} syllabuses for lecturer@edu.vn")
