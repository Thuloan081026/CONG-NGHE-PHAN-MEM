"""
Create test users for testing Module 7 & 8
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_users():
    """Create test users if they don't exist"""
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@test.com").first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                email="admin@test.com",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            print("✓ Admin user created")
        else:
            print("✓ Admin user already exists")
        
        # Check if lecturer exists
        lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
        if not lecturer:
            print("Creating lecturer user...")
            lecturer = User(
                email="lecturer@test.com",
                full_name="Lecturer User",
                hashed_password=get_password_hash("lecturer123"),
                role="lecturer",
                is_active=True
            )
            db.add(lecturer)
            print("✓ Lecturer user created")
        else:
            print("✓ Lecturer user already exists")
        
        # Check if student exists
        student = db.query(User).filter(User.email == "student@test.com").first()
        if not student:
            print("Creating student user...")
            student = User(
                email="student@test.com",
                full_name="Student User",
                hashed_password=get_password_hash("student123"),
                role="student",
                is_active=True
            )
            db.add(student)
            print("✓ Student user created")
        else:
            print("✓ Student user already exists")
        
        db.commit()
        print("\n✅ All test users ready!")
        print("\nLogin credentials:")
        print("  Admin:    admin@test.com / admin123")
        print("  Lecturer: lecturer@test.com / lecturer123")
        print("  Student:  student@test.com / student123")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test users...\n")
    create_test_users()
