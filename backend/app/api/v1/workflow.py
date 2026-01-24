from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.deps import get_current_user, require_roles
from ...models.user import User
from ...schemas.workflow_schema import WorkflowActionRequest, WorkflowResultOut
from ...services.workflow_service import WorkflowService
from ...schemas.workflow_schema import WorkflowEventOut

router = APIRouter(prefix="/workflow", tags=["workflow"])
service = WorkflowService()


@router.post("/submit", response_model=WorkflowResultOut)
def submit_workflow(
    payload: WorkflowActionRequest,
    current_user: User = Depends(require_roles("lecturer")),
    db: Session = Depends(get_db)
):
    """Lecturer nộp giáo trình (draft -> submitted)"""
    updated, event = service.submit(db, payload.syllabus_id, current_user.id, payload.comment)
    return {"event": event, "syllabus_id": updated.id, "new_status": updated.status, "is_published": updated.is_published}


@router.post("/hod-approve", response_model=WorkflowResultOut)
def hod_approve(
    payload: WorkflowActionRequest,
    current_user: User = Depends(require_roles("hod")),
    db: Session = Depends(get_db)
):
    """HOD duyệt cấp 1 (submitted -> hod_approved)"""
    updated, event = service.hod_approve(db, payload.syllabus_id, current_user.id, payload.comment)
    return {"event": event, "syllabus_id": updated.id, "new_status": updated.status, "is_published": updated.is_published}


@router.post("/aa-approve", response_model=WorkflowResultOut)
def aa_approve(
    payload: WorkflowActionRequest,
    current_user: User = Depends(require_roles("aa")),
    db: Session = Depends(get_db)
):
    """Academic Affairs duyệt cấp 2 (hod_approved -> aa_approved)"""
    updated, event = service.aa_approve(db, payload.syllabus_id, current_user.id, payload.comment)
    return {"event": event, "syllabus_id": updated.id, "new_status": updated.status, "is_published": updated.is_published}


@router.post("/final-approve", response_model=WorkflowResultOut)
def final_approve(
    payload: WorkflowActionRequest,
    current_user: User = Depends(require_roles("principal")),
    db: Session = Depends(get_db)
):
    """Principal duyệt cuối cùng và publish (aa_approved -> published)"""
    updated, event = service.final_approve_and_publish(db, payload.syllabus_id, current_user.id, payload.comment)
    return {"event": event, "syllabus_id": updated.id, "new_status": updated.status, "is_published": updated.is_published}


@router.get("/{syllabus_id}/events")
def list_workflow_events(
    syllabus_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liệt kê lịch sử workflow của một syllabus (pagination)"""
    items, total = service.list_events(db, syllabus_id, skip, limit)
    # Convert SQLAlchemy objects to dicts for JSON serialization
    items_dict = [
        {
            "id": item.id,
            "syllabus_id": item.syllabus_id,
            "action": item.action,
            "from_status": item.from_status,
            "to_status": item.to_status,
            "comment": item.comment,
            "created_by": item.performed_by,
            "created_at": item.created_at.isoformat() if item.created_at else None
        }
        for item in items
    ]
    return {"total": total, "count": len(items), "items": items_dict}


@router.get("/events/{event_id}", response_model=WorkflowEventOut)
def get_workflow_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy chi tiết một workflow event theo id"""
    ev = service.get_event(db, event_id)
    return ev
