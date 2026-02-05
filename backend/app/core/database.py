from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .config import settings
import pymysql


def create_database_if_not_exists():
    """Tự động tạo database nếu chưa tồn tại"""
    if "mysql" in settings.DATABASE_URL:
        # Parse database name from URL
        # Format: mysql+pymysql://user:password@host:port/database_name
        db_name = settings.DATABASE_URL.split('/')[-1]
        
        # Tạo connection string không có database name
        base_url = settings.DATABASE_URL.rsplit('/', 1)[0]
        
        try:
            # Connect to MySQL server (không chỉ định database)
            temp_engine = create_engine(base_url)
            with temp_engine.begin() as conn:
                # Kiểm tra và tạo database nếu chưa có
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                print(f"✅ Database '{db_name}' đã sẵn sàng!")
            temp_engine.dispose()
        except Exception as e:
            print(f"⚠️ Lỗi khi tạo database: {e}")
            print(f"Vui lòng kiểm tra MySQL đã chạy chưa và thông tin kết nối")


# Tự động tạo database trước khi khởi tạo engine
create_database_if_not_exists()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=False,
    pool_recycle=300,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def initialize_demo_users():
    """Tự động tạo các tài khoản demo khi khởi động"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có user nào chưa
        user_count = db.query(User).count()
        if user_count > 0:
            return  # Đã có users, không tạo nữa
        
        # Danh sách tài khoản demo với email @ut.edu.vn
        demo_users = [
            {"email": "admin@ut.edu.vn", "full_name": "Quản trị viên hệ thống", "password": "admin123", "role": "admin"},
            {"email": "lecturer@ut.edu.vn", "full_name": "Giảng viên Demo", "password": "lecturer123", "role": "lecturer"},
            {"email": "hod@ut.edu.vn", "full_name": "Trưởng khoa CNTT", "password": "hod123", "role": "hod"},
            {"email": "principal@ut.edu.vn", "full_name": "Hiệu trưởng", "password": "principal123", "role": "principal"},
            {"email": "aa@ut.edu.vn", "full_name": "Phòng Đào tạo", "password": "aa123", "role": "academic_affairs"},
            {"email": "student@ut.edu.vn", "full_name": "Sinh viên Demo", "password": "student123", "role": "student"},
        ]
        
        print("\n👥 Đang tạo tài khoản demo...")
        for user_data in demo_users:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_active=True
            )
            db.add(user)
            print(f"  ✅ {user_data['email']} / {user_data['password']}")
        
        db.commit()
        print("✨ Tài khoản demo đã được tạo!\n")
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo tài khoản demo: {e}")
        db.rollback()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Close session properly
