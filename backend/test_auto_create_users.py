"""
Script test: Xóa users và kiểm tra tự động tạo lại
"""
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

try:
    # Đếm users hiện tại
    count_before = db.query(User).count()
    print(f"📊 Số users hiện tại: {count_before}")
    
    # Xóa tất cả users để test auto-create
    if count_before > 0:
        print("\n🗑️ Đang xóa tất cả users để test auto-create...")
        db.query(User).delete()
        db.commit()
        print("✅ Đã xóa tất cả users")
    
    count_after = db.query(User).count()
    print(f"📊 Số users sau khi xóa: {count_after}")
    print("\n💡 Bây giờ hãy restart backend server để xem tự động tạo users!")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
    db.rollback()
finally:
    db.close()
