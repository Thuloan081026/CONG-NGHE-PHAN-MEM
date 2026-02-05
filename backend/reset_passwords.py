"""
Script to reset passwords for test users
"""
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def reset_passwords():
    db = SessionLocal()
    try:
        # Password mapping
        password_map = {
            "admin@ut.edu.vn": "admin123",
            "lecturer@ut.edu.vn": "lecturer123",
            "hod@ut.edu.vn": "hod123",
            "aa@ut.edu.vn": "aa123",
            "student@ut.edu.vn": "student123",
            "principal@ut.edu.vn": "principal123"
        }
        
        for email, password in password_map.items():
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.hashed_password = get_password_hash(password)
                user.is_active = True
                print(f"✅ Reset password for: {email}")
            else:
                print(f"❌ User not found: {email}")
        
        db.commit()
        print("\n✅ Successfully reset all passwords!")
        print("\nTest accounts:")
        print("- Admin: admin@ut.edu.vn / admin123")
        print("- Lecturer: lecturer@ut.edu.vn / lecturer123")
        print("- HOD: hod@ut.edu.vn / hod123")
        print("- Academic Affairs: aa@ut.edu.vn / aa123")
        print("- Student: student@ut.edu.vn / student123")
        print("- Principal: principal@ut.edu.vn / principal123")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Resetting passwords for test users...")
    reset_passwords()
