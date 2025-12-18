"""
Notification Service
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime

from ..models.notification import Notification, SyllabusFollow
from ..models.syllabus import Syllabus
from ..models.user import User
from ..schemas.notification_schema import NotificationCreate, NotificationOut
from fastapi import HTTPException


class NotificationService:
    """Service for notifications and follows"""
    
    def create_notification(
        self, 
        db: Session, 
        notification_data: NotificationCreate
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(**notification_data.dict())
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    def get_user_notifications(
        self, 
        db: Session, 
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        unread_only: bool = False
    ) -> Tuple[List[Notification], int]:
        """Get notifications for a user"""
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        total = query.count()
        items = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return items, total
    
    def mark_as_read(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Mark notification as read"""
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.commit()
            return True
        return False
    
    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        """Mark all notifications as read"""
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True, "read_at": datetime.utcnow()})
        db.commit()
        return count
    
    def follow_syllabus(self, db: Session, user_id: int, syllabus_id: int) -> bool:
        """Student follows a syllabus"""
        # Check if already following
        existing = db.query(SyllabusFollow).filter(
            SyllabusFollow.user_id == user_id,
            SyllabusFollow.syllabus_id == syllabus_id
        ).first()
        
        if existing:
            return False  # Already following
        
        follow = SyllabusFollow(user_id=user_id, syllabus_id=syllabus_id)
        db.add(follow)
        db.commit()
        return True
    
    def unfollow_syllabus(self, db: Session, user_id: int, syllabus_id: int) -> bool:
        """Student unfollows a syllabus"""
        follow = db.query(SyllabusFollow).filter(
            SyllabusFollow.user_id == user_id,
            SyllabusFollow.syllabus_id == syllabus_id
        ).first()
        
        if follow:
            db.delete(follow)
            db.commit()
            return True
        return False
    
    def is_following(self, db: Session, user_id: int, syllabus_id: int) -> bool:
        """Check if user is following syllabus"""
        follow = db.query(SyllabusFollow).filter(
            SyllabusFollow.user_id == user_id,
            SyllabusFollow.syllabus_id == syllabus_id
        ).first()
        return follow is not None
    
    def get_syllabus_followers(self, db: Session, syllabus_id: int) -> List[int]:
        """Get all users following a syllabus"""
        follows = db.query(SyllabusFollow).filter(
            SyllabusFollow.syllabus_id == syllabus_id
        ).all()
        return [f.user_id for f in follows]
    
    def notify_syllabus_update(
        self, 
        db: Session, 
        syllabus_id: int,
        update_type: str,
        message: str
    ):
        """Notify all followers when syllabus is updated"""
        followers = self.get_syllabus_followers(db, syllabus_id)
        
        syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
        title = f"Cập nhật giáo trình: {syllabus.subject_code}" if syllabus else "Cập nhật giáo trình"
        
        for user_id in followers:
            notification_data = NotificationCreate(
                user_id=user_id,
                syllabus_id=syllabus_id,
                title=title,
                message=message,
                notification_type=update_type
            )
            self.create_notification(db, notification_data)
    
    def notify_lecturer(
        self,
        db: Session,
        lecturer_id: int,
        syllabus_id: int,
        action: str,  # approve or reject
        message: str
    ):
        """Notify lecturer when syllabus is approved/rejected"""
        title_map = {
            "approve": "✅ Giáo trình được duyệt",
            "reject": "❌ Giáo trình bị từ chối"
        }
        
        notification_data = NotificationCreate(
            user_id=lecturer_id,
            syllabus_id=syllabus_id,
            title=title_map.get(action, "Thông báo"),
            message=message,
            notification_type=action
        )
        self.create_notification(db, notification_data)
