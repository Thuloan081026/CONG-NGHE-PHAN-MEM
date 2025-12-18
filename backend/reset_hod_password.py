"""Reset HOD password"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
try:
    # Get HOD user
    hod = db.query(User).filter(User.email == "hod@test.com").first()
    if not hod:
        print("❌ HOD user not found!")
        exit(1)
    
    print(f"Found HOD: {hod.email} (role: {hod.role})")
    
    # Reset password
    new_password = "hod123"
    hod.hashed_password = get_password_hash(new_password)
    db.commit()
    
    print(f"✅ HOD password reset to: {new_password}")
    print(f"Hash: {hod.hashed_password[:50]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
