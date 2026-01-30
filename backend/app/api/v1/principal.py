"""
Principal Dashboard API
Provides statistics and dashboard data for principal
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict

from ...core.database import get_db
from ...core.deps import require_roles

router = APIRouter(prefix="/api/principal", tags=["principal"])


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _=Depends(require_roles("principal", "admin"))
) -> Dict:
    """
    Get dashboard statistics for principal panel
    Returns counts of users, syllabuses, pending approvals, etc.
    """
    
    # Count total users
    total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    
    # Count users by role
    admin_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'")).scalar()
    lecturer_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'lecturer'")).scalar()
    student_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'student'")).scalar()
    hod_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'hod'")).scalar()
    aa_count = db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'academic_affairs'")).scalar()
    
    # Count syllabuses
    total_syllabuses = db.execute(text("SELECT COUNT(*) FROM syllabuses")).scalar()
    
    # Count syllabuses by workflow status
    published = db.execute(text(
        "SELECT COUNT(*) FROM syllabuses WHERE workflow_status IN ('approved', 'published')"
    )).scalar()
    
    draft = db.execute(text("SELECT COUNT(*) FROM syllabuses WHERE workflow_status = 'draft'")).scalar()
    
    # Count pending approvals (all pending states)
    pending_approval = db.execute(text(
        "SELECT COUNT(*) FROM syllabuses WHERE workflow_status IN ('pending_hod_approval', 'pending_principal_approval', 'pending_aa_approval')"
    )).scalar()
    
    # Count rejected
    rejected = db.execute(text("SELECT COUNT(*) FROM syllabuses WHERE workflow_status = 'rejected'")).scalar()
    
    return {
        "total_users": total_users or 0,
        "admin_count": admin_count or 0,
        "lecturer_count": lecturer_count or 0,
        "student_count": student_count or 0,
        "hod_count": hod_count or 0,
        "aa_count": aa_count or 0,
        "total_syllabuses": total_syllabuses or 0,
        "published": published or 0,
        "draft": draft or 0,
        "pending_approval": pending_approval or 0,
        "rejected": rejected or 0
    }


@router.get("/dashboard/pending-syllabuses")
def get_pending_syllabuses(
    limit: int = 10,
    db: Session = Depends(get_db),
    _=Depends(require_roles("principal", "admin"))
):
    """Get syllabuses pending approval"""
    result = db.execute(text(
        """
        SELECT s.id, s.subject_code, s.subject_name, s.workflow_status, s.created_at,
               u.full_name as creator_name, u.email as creator_email
        FROM syllabuses s
        LEFT JOIN users u ON s.created_by = u.id
        WHERE s.workflow_status IN ('pending_hod_approval', 'pending_principal_approval', 'pending_aa_approval')
        ORDER BY s.created_at DESC
        LIMIT :limit
        """
    ), {"limit": limit})
    
    syllabuses = []
    for row in result:
        syllabuses.append({
            "id": row[0],
            "code": row[1],
            "title": row[2],
            "workflow_status": row[3],
            "created_at": row[4].isoformat() if row[4] else None,
            "creator_name": row[5],
            "creator_email": row[6]
        })
    
    return syllabuses
