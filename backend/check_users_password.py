"""
Check database and fix test data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

def check_users():
    db = SessionLocal()
    
    print("\n" + "="*60)
    print("  CHECKING TEST USERS")
    print("="*60 + "\n")
    
    # Check all users
    users = db.query(User).all()
    print(f"📊 Total users: {len(users)}\n")
    
    for user in users:
        print(f"✓ {user.role:10} | {user.email:30} | Active: {user.is_active}")
    
    # Check specific test users
    print("\n" + "="*60)
    print("  TEST USER CREDENTIALS")
    print("="*60 + "\n")
    
    test_emails = ["admin@test.com", "lecturer@test.com", "student@test.com"]
    
    for email in test_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"✓ {email}")
            print(f"  Role: {user.role}")
            print(f"  Active: {user.is_active}")
            print(f"  ID: {user.id}")
            
            # Test password
            if verify_password("lecturer123", user.hashed_password) if "lecturer" in email else \
               verify_password("student123", user.hashed_password) if "student" in email else \
               verify_password("admin123", user.hashed_password):
                print(f"  Password: ✓ Valid")
            else:
                print(f"  Password: ✗ Invalid - Need to reset")
                # Reset password
                if "lecturer" in email:
                    user.hashed_password = get_password_hash("lecturer123")
                elif "student" in email:
                    user.hashed_password = get_password_hash("student123")
                elif "admin" in email:
                    user.hashed_password = get_password_hash("admin123")
                db.commit()
                print(f"  Password: ✓ Reset completed")
        else:
            print(f"✗ {email} - NOT FOUND")
    
    print()
    db.close()

if __name__ == "__main__":
    check_users()
