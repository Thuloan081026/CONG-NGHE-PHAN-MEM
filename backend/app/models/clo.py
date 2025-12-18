from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class CLO(Base):
    """Course Learning Outcome - Chuẩn đầu ra môn học"""
    __tablename__ = "clos"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False, index=True)
    
    # CLO info
    code = Column(String(50), nullable=False)  # e.g., "CLO1", "CLO2"
    description = Column(Text, nullable=False)  # Mô tả chuẩn đầu ra
    
    # Bloom's Taxonomy Level
    cognitive_level = Column(String(50), nullable=True)  # K1, K2, K3, K4, K5, K6
    
    # Weight/Priority
    weight = Column(Float, nullable=True, default=1.0)  # Trọng số
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="clos")
    mappings = relationship("CLO_PLO_Mapping", back_populates="clo", cascade="all, delete-orphan")
