from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class PLO(Base):
    """Program Learning Outcome - Chuẩn đầu ra chương trình"""
    __tablename__ = "plos"

    id = Column(Integer, primary_key=True, index=True)
    
    # PLO info
    code = Column(String(50), unique=True, nullable=False, index=True)  # e.g., "PLO1", "PLO2"
    description = Column(Text, nullable=False)  # Mô tả chuẩn đầu ra chương trình
    
    # Program info
    program_code = Column(String(100), nullable=True)  # Mã chương trình đào tạo
    program_name = Column(String(255), nullable=True)  # Tên chương trình
    
    # Category
    category = Column(String(100), nullable=True)  # Knowledge, Skills, Attitudes
    
    # Weight/Priority
    weight = Column(Float, nullable=True, default=1.0)  # Trọng số
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mappings = relationship("CLO_PLO_Mapping", back_populates="plo", cascade="all, delete-orphan")
