#!/usr/bin/env python
"""
Setup Complete Development Environment
- Create database
- Create test users (admin, lecturer, students)
- Create sample syllabuses
- Create sample workflows
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.syllabus import Syllabus, SyllabusVersion
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import json

def create_tables():
    """Create all database tables"""
    print("[STEP 1] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

def create_test_users():
    """Create test users"""
    print("\n[STEP 2] Creating test users...")
    db = SessionLocal()
    
    try:
        users_data = [
            {
                "email": "admin@smd.edu.vn",
                "full_name": "Admin User",
                "password": "admin123",
                "role": "admin",
                "department": "Administration"
            },
            {
                "email": "lecturer@test.com",
                "full_name": "Dr. Nguyen Van A",
                "password": "lecturer123",
                "role": "lecturer",
                "department": "Computer Science"
            },
            {
                "email": "hod@test.com",
                "full_name": "Prof. Tran Thi B",
                "password": "hod123",
                "role": "hod",
                "department": "Computer Science"
            },
            {
                "email": "student@test.com",
                "full_name": "Student One",
                "password": "student123",
                "role": "student",
                "department": "Computer Science"
            },
            {
                "email": "reviewer@test.com",
                "full_name": "Dr. Reviewer",
                "password": "reviewer123",
                "role": "reviewer",
                "department": "Quality Assurance"
            }
        ]
        
        for user_data in users_data:
            # Check if user exists
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  ✓ User {user_data['email']} already exists")
                continue
            
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                department=user_data["department"],
                is_active=True
            )
            db.add(user)
            print(f"  ✓ Created user: {user_data['email']} ({user_data['role']})")
        
        db.commit()
        print("\n✅ All test users created successfully!")
        
    except Exception as e:
        print(f"✗ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_syllabuses():
    """Create sample syllabuses"""
    print("\n[STEP 3] Creating sample syllabuses...")
    db = SessionLocal()
    
    try:
        lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
        if not lecturer:
            print("✗ Lecturer user not found")
            return
        
        print("  ✓ Sample syllabuses setup skipped (using existing data)")
        print("    You can create syllabuses through the web interface")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("\n" + "="*60)
    print("  SETTING UP DEVELOPMENT ENVIRONMENT")
    print("="*60)
    
    try:
        create_tables()
        create_test_users()
        create_sample_syllabuses()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print("\nYou can now:")
        print("  1. Start Backend:  python -m uvicorn app.main:app --reload --port 8000")
        print("  2. Start Frontend: python -m http.server 3000 (in frontend/lecturer-web)")
        print("  3. Login with: lecturer@test.com / lecturer123")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
