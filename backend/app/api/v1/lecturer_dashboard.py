from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.syllabus import Syllabus
from app.models.user import User
from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/lecturer",
    tags=["Lecturer Dashboard"]
)

@router.get("/dashboard")
def lecturer_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Chỉ lecturer được vào
    if current_user.role != "lecturer":
        raise HTTPException(status_code=403, detail="Access denied")

    lecturer_id = current_user.id

    pending = db.query(func.count(Syllabus.id)).filter(
        Syllabus.lecturer_id == lecturer_id,
        Syllabus.status.in_(["submitted", "hod_pending"])
    ).scalar()

    review = db.query(func.count(Syllabus.id)).filter(
        Syllabus.lecturer_id == lecturer_id,
        Syllabus.status == "in_review"
    ).scalar()

    approved = db.query(func.count(Syllabus.id)).filter(
        Syllabus.lecturer_id == lecturer_id,
        Syllabus.status.in_(["approved", "published"])
    ).scalar()

    recent = (
        db.query(Syllabus)
        .filter(Syllabus.lecturer_id == lecturer_id)
        .order_by(Syllabus.updated_at.desc())
        .limit(5)
        .all()
    )

    return {
        "pending": pending,
        "review": review,
        "approved": approved,
        "recent": [
            {
                "id": s.id,
                "subject_code": s.subject_code,
                "subject_name": s.subject_name,
                "status": s.status,
                "updated_at": s.updated_at
            }
            for s in recent
        ]
    }
