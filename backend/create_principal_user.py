"""
Tạo tài khoản Principal (Hiệu trưởng)
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

try:
    # Kiểm tra xem principal đã tồn tại chưa
    existing = db.query(User).filter(User.email == "principal@ut.edu.vn").first()
    
    if existing:
        print(f"✓ Tài khoản principal@ut.edu.vn đã tồn tại")
    else:
        print("📝 Đang tạo tài khoản Principal...")
        principal = User(
            email="principal@ut.edu.vn",
            full_name="Hiệu trưởng",
            hashed_password=get_password_hash("principal123"),
            role="principal",
            is_active=True
        )
        db.add(principal)
        db.commit()
        print("✅ Đã tạo tài khoản: principal@ut.edu.vn / principal123")
    
    # Hiển thị tất cả users
    print("\n👥 Danh sách tất cả tài khoản:")
    users = db.query(User).all()
    for user in users:
        print(f"  • {user.email} - {user.full_name} ({user.role})")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()
