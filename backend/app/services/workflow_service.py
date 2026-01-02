from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..models.workflow import WorkflowEvent
from ..models.syllabus import Syllabus
from ..repositories.syllabus_repo import SyllabusRepository
from ..repositories.workflow_repo import WorkflowRepository
from fastapi import HTTPException


class WorkflowService:
    """Service xử lý quy trình review → approve → publish cho Syllabus.

    Quy định trạng thái:
    - draft -> submitted (lecturer submits)
    - submitted -> hod_approved (HOD approves)
    - hod_approved -> aa_approved (Academic Affairs approves)
    - aa_approved -> published (Principal final approves -> publish)

    Mỗi lần chuyển trạng thái sẽ tạo một WorkflowEvent để lưu audit trail.
    """

    def __init__(self):
        self.syllabus_repo = SyllabusRepository()
        self.workflow_repo = WorkflowRepository()

    def _create_event(
        self,
        db: Session,
        syllabus_id: int,
        action: str,
        from_status: Optional[str],
        to_status: str,
        performed_by: int,
        comment: Optional[str] = None
    ) -> WorkflowEvent:
        event = WorkflowEvent(
            syllabus_id=syllabus_id,
            action=action,
            from_status=from_status,
            to_status=to_status,
            comment=comment,
            performed_by=performed_by
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def submit(self, db: Session, syllabus_id: int, user_id: int, comment: Optional[str] = None):
        syllabus = self.syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        if syllabus.status != "draft":
            raise HTTPException(status_code=400, detail="Only draft syllabus can be submitted")

        from_status = syllabus.status
        to_status = "submitted"

        # Update syllabus status
        updated = self.syllabus_repo.update_status(db, syllabus_id, to_status)

        # Create event
        event = self._create_event(db, syllabus_id, "submit", from_status, to_status, user_id, comment)
        return updated, event

    def hod_approve(self, db: Session, syllabus_id: int, user_id: int, comment: Optional[str] = None):
        syllabus = self.syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        if syllabus.status != "submitted":
            raise HTTPException(status_code=400, detail="Only submitted syllabus can be HOD approved")

        from_status = syllabus.status
        to_status = "hod_approved"

        updated = self.syllabus_repo.update_status(db, syllabus_id, to_status)
        event = self._create_event(db, syllabus_id, "hod_approve", from_status, to_status, user_id, comment)
        return updated, event

    def aa_approve(self, db: Session, syllabus_id: int, user_id: int, comment: Optional[str] = None):
        syllabus = self.syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        if syllabus.status != "hod_approved":
            raise HTTPException(status_code=400, detail="Only HOD approved syllabus can be AA approved")

        from_status = syllabus.status
        to_status = "aa_approved"

        updated = self.syllabus_repo.update_status(db, syllabus_id, to_status)
        event = self._create_event(db, syllabus_id, "aa_approve", from_status, to_status, user_id, comment)
        return updated, event

    def final_approve_and_publish(self, db: Session, syllabus_id: int, user_id: int, comment: Optional[str] = None):
        syllabus = self.syllabus_repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        if syllabus.status != "aa_approved":
            raise HTTPException(status_code=400, detail="Only AA approved syllabus can be final approved and published")

        from_status = syllabus.status
        to_status = "published"

        # Update syllabus status to published and set published flag
        updated = self.syllabus_repo.update_status(db, syllabus_id, to_status, is_published=True)

        event = self._create_event(db, syllabus_id, "final_approve_and_publish", from_status, to_status, user_id, comment)
        return updated, event

    # ----- Listing / getting events -----
    def list_events(self, db: Session, syllabus_id: int, skip: int = 0, limit: int = 100):
        """Liệt kê lịch sử workflow cho một syllabus"""
        return self.workflow_repo.list_by_syllabus(db, syllabus_id, skip, limit)

    def get_event(self, db: Session, event_id: int):
        """Lấy chi tiết một workflow event"""
        ev = self.workflow_repo.get_by_id(db, event_id)
        if not ev:
            raise HTTPException(status_code=404, detail="Workflow event not found")
        return ev
