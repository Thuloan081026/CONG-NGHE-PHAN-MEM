from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    content: str = Field(..., min_length=10, max_length=5000)
    section: Optional[str] = None


class ReviewCreate(ReviewBase):
    syllabus_id: int


class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    section: Optional[str] = None
    is_resolved: Optional[int] = None


class ReviewResponse(ReviewBase):
    id: int
    syllabus_id: int
    created_by: int
    author_email: str
    is_resolved: int
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
