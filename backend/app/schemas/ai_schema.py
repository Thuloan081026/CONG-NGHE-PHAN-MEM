from pydantic import BaseModel
from typing import Optional, List

class SummaryRequest(BaseModel):
    syllabus_id: int
    content: str

class SummaryResponse(BaseModel):
    task_id: str

class DiffRequest(BaseModel):
    syllabus_id: int
    old_content: str
    new_content: str

class DiffResponse(BaseModel):
    task_id: str

class CLOCheckRequest(BaseModel):
    syllabus_id: int
    clos: List[str]
    plos: List[str]

class CLOCheckResponse(BaseModel):
    task_id: str
