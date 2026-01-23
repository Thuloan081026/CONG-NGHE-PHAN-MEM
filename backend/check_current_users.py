"""
Kiểm tra users hiện có trong database
"""
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

try:
    users = db.query(User).all()
    print(f"\n📊 Tổng số users: {len(users)}\n")
    
    if users:
        print("👥 Danh sách users:")
        for user in users:
            print(f"  • {user.email} - {user.full_name} ({user.role})")
    else:
        print("⚠️ Không có users nào trong database!")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
finally:
    db.close()
