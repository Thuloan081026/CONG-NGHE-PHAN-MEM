"""Reset lecturer test user password"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# Find lecturer
user = db.query(User).filter(User.email == "lecturer@test.com").first()
if user:
    new_password = "lecturer123"
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    print(f"✅ Password updated for {user.email}")
    print(f"   New password: {new_password}")
    print(f"   Role: {user.role}")
    print(f"   Active: {user.is_active}")
else:
    print("❌ User not found")

db.close()
