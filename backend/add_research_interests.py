import sys
sys.path.insert(0, 'app')

from app.core.database import SessionLocal
from sqlalchemy import text
from app.models.user import User

def add_research_interests():
    """Thêm dữ liệu mẫu research interests cho giảng viên"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("🎯 THÊM LĨNH VỰC NGHIÊN CỨU")
        print("=" * 60)
        
        # Tìm user giảng viên
        email = "nguyen.dat@university.edu.vn"
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ Không tìm thấy user: {email}")
            print("💡 Chạy script create_lecturer_profile_data.py trước!")
            return False
        
        print(f"\n👤 Tìm thấy giảng viên: {user.full_name}")
        print(f"   User ID: {user.id}")
        
        # Xóa research interests cũ nếu có
        delete_old = text("DELETE FROM research_interests WHERE user_id = :user_id")
        db.execute(delete_old, {"user_id": user.id})
        db.commit()
        
        # Danh sách lĩnh vực nghiên cứu
        interests = [
            "Machine Learning",
            "Deep Learning",
            "Natural Language Processing",
            "Computer Vision",
            "Data Science",
            "Artificial Intelligence",
            "Big Data",
            "Cloud Computing"
        ]
        
        print(f"\n📝 Thêm {len(interests)} lĩnh vực nghiên cứu:")
        
        # Thêm từng interest
        for interest in interests:
            insert_query = text("""
                INSERT INTO research_interests (user_id, interest_name)
                VALUES (:user_id, :interest_name)
            """)
            db.execute(insert_query, {
                "user_id": user.id,
                "interest_name": interest
            })
            print(f"   ✓ {interest}")
        
        db.commit()
        
        print("\n✅ Thêm thành công!")
        
        # Kiểm tra dữ liệu
        check_query = text("""
            SELECT COUNT(*) as count 
            FROM research_interests 
            WHERE user_id = :user_id
        """)
        result = db.execute(check_query, {"user_id": user.id}).fetchone()
        print(f"\n📊 Tổng số lĩnh vực: {result[0]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\n💡 Đảm bảo bạn đã chạy:")
    print("   1. create_research_interests_table.py")
    print("   2. create_lecturer_profile_data.py")
    print()
    
    success = add_research_interests()
    print("\n" + "=" * 60)
    if success:
        print("✨ Hoàn thành!")
    else:
        print("❌ Thất bại!")
    print("=" * 60)
