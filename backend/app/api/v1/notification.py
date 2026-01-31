"""
Notification API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...models.notification import SyllabusFollow
from ...services.notification_service import NotificationService
from ...schemas.notification_schema import (
    NotificationOut, NotificationListOut,
    FollowRequest, FollowResponse
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])
notification_service = NotificationService()


@router.get("/", response_model=NotificationListOut)
def get_my_notifications(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's notifications
    
    **Lấy danh sách thông báo của user**
    - Filter: unread_only=true để chỉ lấy chưa đọc
    - Pagination: skip, limit
    """
    items, total = notification_service.get_user_notifications(
        db, current_user.id, skip, limit, unread_only
    )
    
    # Convert items to NotificationOut schema
    notification_items = [NotificationOut.from_orm(item) for item in items]
    
    return NotificationListOut(
        items=notification_items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark notification as read"""
    success = notification_service.mark_as_read(db, notification_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Marked as read", "notification_id": notification_id}


@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    count = notification_service.mark_all_as_read(db, current_user.id)
    return {"message": f"Marked {count} notifications as read"}


@router.post("/follow", response_model=FollowResponse)
def follow_syllabus(
    request: FollowRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Follow a syllabus to receive updates
    
    **Student follow giáo trình để nhận thông báo khi cập nhật**
    """
    success = notification_service.follow_syllabus(
        db, current_user.id, request.syllabus_id
    )
    
    if success:
        return FollowResponse(
            syllabus_id=request.syllabus_id,
            is_following=True,
            message="Đã follow giáo trình thành công"
        )
    else:
        return FollowResponse(
            syllabus_id=request.syllabus_id,
            is_following=True,
            message="Bạn đã follow giáo trình này rồi"
        )


@router.delete("/unfollow/{syllabus_id}")
def unfollow_syllabus(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unfollow a syllabus"""
    success = notification_service.unfollow_syllabus(
        db, current_user.id, syllabus_id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Not following this syllabus")
    
    return {"message": "Unfollow thành công", "syllabus_id": syllabus_id}


@router.get("/following/{syllabus_id}")
def check_following(
    syllabus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if user is following syllabus"""
    follow = db.query(SyllabusFollow).filter(
        SyllabusFollow.user_id == current_user.id,
        SyllabusFollow.syllabus_id == syllabus_id
    ).first()
    
    if follow:
        return {
            "syllabus_id": syllabus_id,
            "is_following": True,
            "followed_at": follow.followed_at
        }
    else:
        return {
            "syllabus_id": syllabus_id,
            "is_following": False
        }
