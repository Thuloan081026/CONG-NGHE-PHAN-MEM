"""Department model"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

from ..core.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)  # Mã khoa
    name = Column(String(255), nullable=False)  # Tên khoa
    name_en = Column(String(255), nullable=True)  # Tên tiếng Anh
    description = Column(Text, nullable=True)  # Mô tả
    head_of_department = Column(String(255), nullable=True)  # Trưởng khoa
    email = Column(String(255), nullable=True)  # Email liên hệ
    phone = Column(String(20), nullable=True)  # Số điện thoại
    office_location = Column(String(255), nullable=True)  # Vị trí văn phòng
    is_active = Column(Boolean, default=True)  # Trạng thái hoạt động
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
