from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...models.syllabus import Syllabus
from ...models.subscription import Subscription

router = APIRouter(prefix="/student", tags=["student"])


@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy dữ liệu dashboard cho student"""
    
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied. Student role required.")
    
    # Đếm tổng số syllabuses published
    total_syllabuses = db.query(func.count(Syllabus.id)).filter(
        Syllabus.status == "published"
    ).scalar() or 0
    
    # Đếm số syllabuses đang theo dõi
    subscriptions_count = db.query(func.count(Subscription.id)).filter(
        Subscription.user_id == current_user.id
    ).scalar() or 0
    
    # Lấy thông tin chương trình (mock data - có thể expand sau)
    program_info = {
        "name": "Công nghệ Phần mềm",
        "code": "7480103",
        "total_credits": 150
    }
    
    # Lấy danh sách syllabuses mới nhất (5 items)
    recent_syllabuses = db.query(Syllabus).filter(
        Syllabus.status == "published"
    ).order_by(desc(Syllabus.updated_at)).limit(5).all()
    
    syllabuses_data = []
    for syl in recent_syllabuses:
        syllabuses_data.append({
            "id": syl.id,
            "subject_code": syl.subject_code,
            "subject_name": syl.subject_name,
            "credits": syl.credits,
            "version": syl.version,
            "updated_at": syl.updated_at.isoformat() if syl.updated_at else None,
            "semester": syl.semester or "N/A"
        })
    
    return {
        "stats": {
            "total_syllabuses": total_syllabuses,
            "subscriptions": subscriptions_count,
            "program": program_info["name"],
            "total_credits": program_info["total_credits"]
        },
        "recent_syllabuses": syllabuses_data
    }


@router.get("/syllabuses")
async def search_syllabuses(
    keyword: str = None,
    major: str = None,
    semester: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tìm kiếm syllabuses cho student"""
    
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied")
    
    query = db.query(Syllabus).filter(Syllabus.status == "published")
    
    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            (Syllabus.subject_name.like(search)) |
            (Syllabus.subject_code.like(search))
        )
    
    if semester:
        query = query.filter(Syllabus.semester == semester)
    
    syllabuses = query.order_by(desc(Syllabus.updated_at)).all()
    
    result = []
    for syl in syllabuses:
        result.append({
            "id": syl.id,
            "subject_code": syl.subject_code,
            "subject_name": syl.subject_name,
            "credits": syl.credits,
            "version": syl.version,
            "semester": syl.semester or "N/A",
            "updated_at": syl.updated_at.isoformat() if syl.updated_at else None
        })
    
    return {"syllabuses": result, "total": len(result)}


@router.get("/subscriptions")
async def get_my_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy danh sách syllabuses đang theo dõi"""
    
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied")
    
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).all()
    
    result = []
    for sub in subscriptions:
        syllabus = db.query(Syllabus).filter(Syllabus.id == sub.syllabus_id).first()
        if syllabus:
            result.append({
                "id": sub.id,
                "syllabus_id": syllabus.id,
                "subject_code": syllabus.subject_code,
                "subject_name": syllabus.subject_name,
                "credits": syllabus.credits,
                "version": syllabus.version,
                "semester": syllabus.semester or "N/A",
                "subscribed_at": sub.created_at.isoformat() if sub.created_at else None,
                "has_updates": False  # TODO: Implement update tracking
            })
    
    return {"subscriptions": result, "total": len(result)}


@router.post("/subscribe/{syllabus_id}")
async def subscribe_to_syllabus(
    syllabus_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Theo dõi một syllabus"""
    
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Kiểm tra syllabus có tồn tại không
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    
    # Kiểm tra đã subscribe chưa
    existing = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.syllabus_id == syllabus_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed")
    
    # Tạo subscription mới
    new_sub = Subscription(
        user_id=current_user.id,
        syllabus_id=syllabus_id
    )
    db.add(new_sub)
    db.commit()
    
    return {"message": "Subscribed successfully", "subscription_id": new_sub.id}


@router.delete("/unsubscribe/{subscription_id}")
async def unsubscribe_from_syllabus(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Hủy theo dõi syllabus"""
    
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied")
    
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    
    return {"message": "Unsubscribed successfully"}
