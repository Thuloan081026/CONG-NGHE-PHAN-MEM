"""
System Settings Model - For storing API keys and configurations
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from ..core.database import Base


class SystemSetting(Base):
    """System configuration settings"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_encrypted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, nullable=True)  # User ID who updated
    
    def __repr__(self):
        return f"<SystemSetting {self.key}>"
