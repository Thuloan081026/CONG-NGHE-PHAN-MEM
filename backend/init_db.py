"""Script để khởi tạo database và tạo bảng"""
from app.core.database import engine, Base
from app.models import user, syllabus, review

def init_db():
    """Tạo tất cả các bảng trong database"""
    print("Đang tạo các bảng trong database...")
    Base.metadata.create_all(bind=engine)
    print("Hoàn thành! Database đã được khởi tạo.")

if __name__ == "__main__":
    init_db()
