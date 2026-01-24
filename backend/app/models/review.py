from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class Review(Base):
    """Model for Collaborative Review Comments"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Comment content
    content = Column(Text, nullable=False)
    
    # Optional: section reference (which section of syllabus is being commented on)
    section = Column(String(100), nullable=True)  # e.g., "objectives", "content", "assessment"
    
    # Status tracking
    is_resolved = Column(Integer, default=0)  # 0 = not resolved, 1 = resolved
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    syllabus = relationship("Syllabus", foreign_keys=[syllabus_id])
    author = relationship("User", foreign_keys=[created_by])
    resolver = relationship("User", foreign_keys=[resolved_by])
