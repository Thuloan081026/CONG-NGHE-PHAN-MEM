"""Debug TokenUser validation"""
from app.core.database import SessionLocal
from app.services import user_service
from app.schemas.user_schema import TokenUser

db = SessionLocal()

user = user_service.authenticate_user(db, "admin@hcmute.edu.vn", "admin123")
if user:
    print(f"User found: {user.id}")
    
    # Try validate
    try:
        token_user = TokenUser.model_validate(user)
        print(f"✅ TokenUser validated successfully")
        print(f"Type: {type(token_user)}")
        print(f"Data: {token_user}")
        print(f"Dict: {token_user.model_dump()}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

db.close()
