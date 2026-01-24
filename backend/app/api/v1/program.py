from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/programs", tags=["Programs"])

# ---- Models ----
class Course(BaseModel):
    id: int
    code: str
    name: str
    credits: int
    prereq: Optional[List[int]] = []
    coreq: Optional[List[int]] = []

class Program(BaseModel):
    id: int
    name: str
    courses: List[Course] = []

# Fake in-memory store (sau có thể thay bằng DB)
PROGRAMS: List[Program] = []

# ---- APIs ----

@router.post("/")
def create_program(program: Program):
    PROGRAMS.append(program)
    return {"message": "Program created", "data": program}

@router.get("/")
def list_programs():
    return PROGRAMS

@router.get("/{program_id}")
def get_program(program_id: int):
    for p in PROGRAMS:
        if p.id == program_id:
            return p
    raise HTTPException(status_code=404, detail="Program not found")

@router.post("/{program_id}/courses")
def add_course(program_id: int, course: Course):
    for p in PROGRAMS:
        if p.id == program_id:
            p.courses.append(course)
            return {"message": "Course added", "data": course}
    raise HTTPException(status_code=404, detail="Program not found")
