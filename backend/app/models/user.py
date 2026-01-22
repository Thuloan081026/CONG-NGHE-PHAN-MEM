from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    employee_id = Column(String(50), unique=True, nullable=True)  # Mã số giảng viên
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="student")
    is_active = Column(Boolean, default=True)
    
    # Academic information
    degree = Column(String(100), nullable=True)  # Học vị
    title = Column(String(100), nullable=True)  # Chức danh
    department = Column(String(255), nullable=True)  # Khoa/Bộ môn
    specialization = Column(String(255), nullable=True)  # Chuyên ngành
    
    # Contact information
    phone = Column(String(20), nullable=True)
    office_location = Column(String(255), nullable=True)  # Phòng làm việc
    
    # Research & Teaching information
    research_interests = Column(Text, nullable=True)  # Lĩnh vực nghiên cứu
    teaching_subjects = Column(Text, nullable=True)  # Các môn học giảng dạy
    years_experience = Column(Integer, nullable=True)  # Số năm kinh nghiệm
    syllabus_count = Column(Integer, default=0)  # Số đề cương đã tạo
    qualifications = Column(Text, nullable=True)  # Học vấn & Chứng chỉ
    publications = Column(Text, nullable=True)  # Bài báo & Công trình nghiên cứu
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    notifications = relationship("Notification", back_populates="user")
