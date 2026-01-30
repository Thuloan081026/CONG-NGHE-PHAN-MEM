"""
Admin Dashboard API
Provides statistics and dashboard data for admin panel
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict

from ...core.database import get_db
from ...core.deps import require_roles

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin"))
) -> Dict:
    """
    Get dashboard statistics for admin panel
    Returns counts of users, syllabuses, reviews, etc.
    """
    
    # Count total users
    total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    
    # Count users by role
    admin_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'")).scalar()
    lecturer_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'lecturer'")).scalar()
    hod_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'hod'")).scalar()
    aa_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'academic_affairs'")).scalar()
    
    # Count syllabuses by status
    total_syllabuses = db.execute(text("SELECT COUNT(*) FROM syllabuses")).scalar()
    published = db.execute(text("SELECT COUNT(*) FROM syllabuses WHERE status = 'published'")).scalar()
    draft = db.execute(text("SELECT COUNT(*) FROM syllabuses WHERE status = 'draft'")).scalar()
    
    # Count pending review (submitted + hod_approved)
    pending_review = db.execute(text(
        "SELECT COUNT(*) FROM syllabuses WHERE status IN ('submitted', 'hod_approved')"
    )).scalar()
    
    # Count reviews
    total_reviews = db.execute(text("SELECT COUNT(*) FROM reviews")).scalar()
    
    return {
        "total_users": total_users or 0,
        "admin_count": admin_count or 0,
        "lecturer_count": lecturer_count or 0,
        "hod_count": hod_count or 0,
        "aa_count": aa_count or 0,
        "total_syllabuses": total_syllabuses or 0,
        "published": published or 0,
        "draft": draft or 0,
        "pending_review": pending_review or 0,
        "total_reviews": total_reviews or 0
    }


@router.get("/dashboard/recent-users")
def get_recent_users(
    limit: int = 5,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin"))
):
    """Get recent users from database (latest created)"""
    result = db.execute(text(
        "SELECT id, email, full_name, role, created_at "
        "FROM users ORDER BY created_at DESC LIMIT :limit"
    ), {"limit": limit})
    
    users = []
    for row in result:
        users.append({
            "id": row[0],
            "email": row[1],
            "full_name": row[2],
            "role": row[3],
            "created_at": str(row[4]) if row[4] else None
        })
    
    return users


@router.get("/dashboard/recent-syllabuses")
def get_recent_syllabuses(
    limit: int = 5,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin"))
):
    """Get recent syllabuses from database (latest created)"""
    try:
        result = db.execute(text(
            "SELECT s.id, s.subject_code, s.subject_name, s.status, s.created_at, "
            "u.full_name as creator_name "
            "FROM syllabuses s "
            "LEFT JOIN users u ON s.created_by = u.id "
            "ORDER BY s.created_at DESC LIMIT :limit"
        ), {"limit": limit})
        
        syllabuses = []
        for row in result:
            syllabuses.append({
                "id": row[0],
                "subject_code": row[1],
                "subject_name": row[2],
                "status": row[3],
                "created_at": str(row[4]) if row[4] else None,
                "creator_name": row[5]
            })
        
        return syllabuses
    except Exception as e:
        # If table doesn't exist or any error, return empty array
        print(f"Error fetching syllabuses: {e}")
        return []
