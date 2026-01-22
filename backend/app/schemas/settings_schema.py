"""
Settings Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SettingCreate(BaseModel):
    """Create setting"""
    key: str
    value: str
    description: Optional[str] = None
    encrypt: bool = False


class SettingUpdate(BaseModel):
    """Update setting"""
    value: str
    description: Optional[str] = None


class SettingOut(BaseModel):
    """Setting response"""
    id: int
    key: str
    value: str  # Will show ***ENCRYPTED*** if encrypted
    description: Optional[str]
    is_encrypted: bool
    is_active: bool
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class GeminiKeyUpdate(BaseModel):
    """Update Gemini API key"""
    api_key: str
