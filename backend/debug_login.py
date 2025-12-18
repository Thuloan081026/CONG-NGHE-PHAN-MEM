"""Debug login response"""
from app.core.database import SessionLocal
from app.services import user_service
from app.schemas.user_schema import UserOut

db = SessionLocal()

# Test authenticate
user = user_service.authenticate_user(db, "admin@hcmute.edu.vn", "admin123")
if user:
    print(f"User found: {user.id}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Active: {user.is_active}")
    print(f"Created: {user.created_at}")
    print(f"Updated: {user.updated_at}")
    
    # Try validate
    try:
        user_out = UserOut.model_validate(user)
        print(f"\n✅ Validation successful")
        print(f"UserOut: {user_out}")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
else:
    print("User not found or wrong password")

db.close()
