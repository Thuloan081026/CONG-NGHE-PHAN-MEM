from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class CLO_PLO_Mapping(Base):
    """Mapping between CLO and PLO"""
    __tablename__ = "clo_plo_mappings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    clo_id = Column(Integer, ForeignKey("clos.id"), nullable=False, index=True)
    plo_id = Column(Integer, ForeignKey("plos.id"), nullable=False, index=True)
    
    # Mapping details
    correlation_level = Column(String(50), nullable=True)  # Low, Medium, High
    correlation_score = Column(Float, nullable=True)  # 0.0 - 1.0
    
    # AI suggestions
    ai_suggested = Column(Integer, default=0, nullable=True)  # 0 = manual, 1 = AI suggested
    ai_confidence = Column(Float, nullable=True)  # AI confidence score
    
    # Optional notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    clo = relationship("CLO", back_populates="mappings")
    plo = relationship("PLO", back_populates="mappings")
