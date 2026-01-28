"""
Kiểm tra password hash của admin
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

db = SessionLocal()

try:
    admin = db.query(User).filter(User.email == "admin@ut.edu.vn").first()
    
    if admin:
        print(f"📧 Email: {admin.email}")
        print(f"🔐 Password hash: {admin.hashed_password[:50]}...")
        print(f"📏 Hash length: {len(admin.hashed_password)}")
        
        # Test verify password
        print(f"\n🧪 Testing password verification:")
        test_password = "admin123"
        result = verify_password(test_password, admin.hashed_password)
        print(f"   verify_password('admin123', hash) = {result}")
        
        # Show what hash should be
        print(f"\n🔨 Current hash function:")
        new_hash = get_password_hash("admin123")
        print(f"   get_password_hash('admin123') = {new_hash[:50]}...")
        print(f"   Length: {len(new_hash)}")
        
    else:
        print("❌ Admin user not found!")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
