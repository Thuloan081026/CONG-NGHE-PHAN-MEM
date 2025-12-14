from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class WorkflowEvent(Base):
    """Ghi lại sự kiện của workflow cho mỗi syllabus

    - action: submit, hod_approve, aa_approve, final_approve, publish
    - from_status / to_status: trạng thái trước và sau khi thay đổi
    - performed_by: user id
    - comment: ghi chú (nếu có)
    """
    __tablename__ = "workflow_events"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    syllabus = relationship("Syllabus", back_populates="workflow_events", foreign_keys=[syllabus_id])
    performer = relationship("User", foreign_keys=[performed_by])
