"""
Script to initialize test users in the database
Run this after creating the database and tables
"""
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_users():
    db = SessionLocal()
    try:
        # Check if users already exist
        existing_user = db.query(User).filter(User.email == "admin@ut.edu.vn").first()
        if existing_user:
            print("Users already exist. Skipping initialization.")
            return
        
        # Create test users
        users_data = [
            {
                "email": "admin@ut.edu.vn",
                "password": "admin123",
                "full_name": "Administrator",
                "role": "admin",
                "department": "Administration"
            },
            {
                "email": "lecturer@ut.edu.vn",
                "password": "lecturer123",
                "full_name": "Lecturer User",
                "role": "lecturer",
                "department": "Computer Science"
            },
            {
                "email": "hod@ut.edu.vn",
                "password": "hod123",
                "full_name": "Head of Department",
                "role": "hod",
                "department": "Computer Science"
            },
            {
                "email": "aa@ut.edu.vn",
                "password": "aa123",
                "full_name": "Academic Affairs",
                "role": "academic_affairs",
                "department": "Academic Affairs Office"
            },
            {
                "email": "student@ut.edu.vn",
                "password": "student123",
                "full_name": "Student User",
                "role": "student",
                "department": "Computer Science",
                "student_id": "2021001"
            },
            {
                "email": "principal@ut.edu.vn",
                "password": "principal123",
                "full_name": "Principal",
                "role": "principal",
                "department": "Administration"
            }
        ]
        
        for user_data in users_data:
            password = user_data.pop("password")
            user = User(
                **user_data,
                hashed_password=get_password_hash(password),
                is_active=True
            )
            db.add(user)
            print(f"Created user: {user.email} (Role: {user.role})")
        
        db.commit()
        print("\n✅ Successfully initialized all test users!")
        print("\nTest accounts:")
        print("- Admin: admin@ut.edu.vn / admin123")
        print("- Lecturer: lecturer@ut.edu.vn / lecturer123")
        print("- HOD: hod@ut.edu.vn / hod123")
        print("- Academic Affairs: aa@ut.edu.vn / aa123")
        print("- Student: student@ut.edu.vn / student123")
        print("- Principal: principal@ut.edu.vn / principal123")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing test users...")
    init_users()
