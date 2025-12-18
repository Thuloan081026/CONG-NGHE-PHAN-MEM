from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkflowActionRequest(BaseModel):
    syllabus_id: int
    comment: Optional[str] = None


class WorkflowEventOut(BaseModel):
    id: int
    syllabus_id: int
    action: str
    from_status: Optional[str] = None
    to_status: str
    comment: Optional[str] = None
    performed_by: int
    created_at: datetime

    class Config:
        from_attributes = True


# Kết quả trả về: event + trạng thái syllabus (tối giản)
class WorkflowResultOut(BaseModel):
    event: WorkflowEventOut
    syllabus_id: int
    new_status: str
    is_published: Optional[bool] = False

    class Config:
        from_attributes = True
