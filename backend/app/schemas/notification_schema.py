"""
Notification Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationCreate(BaseModel):
    """Create notification"""
    user_id: int
    syllabus_id: Optional[int] = None
    title: str
    message: str
    notification_type: str  # update, approve, reject, follow


class NotificationOut(BaseModel):
    """Notification response"""
    id: int
    user_id: int
    syllabus_id: Optional[int] = None
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        orm_mode = True


class NotificationListOut(BaseModel):
    """List of notifications with pagination"""
    items: list[NotificationOut]
    total: int
    skip: int
    limit: int


class FollowRequest(BaseModel):
    """Follow/Unfollow syllabus"""
    syllabus_id: int


class FollowResponse(BaseModel):
    """Follow response"""
    syllabus_id: int
    is_following: bool
    message: str
