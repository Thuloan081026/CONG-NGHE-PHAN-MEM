#!/usr/bin/env python3
"""
Script to add a student account to the system
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash


def add_student_account(email: str, password: str, full_name: str = None):
    """
    Add a new student account to the database
    
    Args:
        email: Student email address
        password: Student password (plaintext, will be hashed)
        full_name: Student full name (optional)
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ Error: User with email '{email}' already exists!")
            return False
        
        # Create new student user
        hashed_password = get_password_hash(password)
        new_student = User(
            email=email,
            full_name=full_name or email.split('@')[0],
            hashed_password=hashed_password,
            role="student",
            is_active=True
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        
        print(f"✅ Success! Student account created:")
        print(f"   Email: {new_student.email}")
        print(f"   Full Name: {new_student.full_name}")
        print(f"   Role: {new_student.role}")
        print(f"   ID: {new_student.id}")
        print(f"   Active: {new_student.is_active}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating student account: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Add student account with the provided credentials
    email = "student@ut.edu.vn"
    password = "Student@123"
    
    print(f"Adding student account...")
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    success = add_student_account(email=email, password=password)
    
    sys.exit(0 if success else 1)
