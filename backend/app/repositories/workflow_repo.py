from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from ..models.workflow import WorkflowEvent


class WorkflowRepository:
    """Repository để truy vấn workflow events"""

    def create(self, db: Session, obj_in: dict) -> WorkflowEvent:
        ev = WorkflowEvent(**obj_in)
        db.add(ev)
        db.commit()
        db.refresh(ev)
        return ev

    def get_by_id(self, db: Session, event_id: int) -> Optional[WorkflowEvent]:
        return db.query(WorkflowEvent).filter(WorkflowEvent.id == event_id).first()

    def list_by_syllabus(self, db: Session, syllabus_id: int, skip: int = 0, limit: int = 100) -> (List[WorkflowEvent], int):
        q = db.query(WorkflowEvent).filter(WorkflowEvent.syllabus_id == syllabus_id).order_by(desc(WorkflowEvent.created_at))
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> (List[WorkflowEvent], int):
        q = db.query(WorkflowEvent).order_by(desc(WorkflowEvent.created_at))
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
