from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/student", tags=["Student"])
templates = Jinja2Templates(directory="student-web/templates")

@router.get("/roadmap")
def roadmap(request: Request):
    roadmap_data = [
        {"id": 1, "semester": 1, "subject_code": "CS101", "subject_name": "Intro to IT"},
        {"id": 2, "semester": 2, "subject_code": "CS102", "subject_name": "Programming"},
        {"id": 3, "semester": 3, "subject_code": "CS201", "subject_name": "Data Structures"},
    ]

    return templates.TemplateResponse(
        "roadmap.html",
        {
            "request": request,
            "roadmap": roadmap_data
        }
    )

@router.get("/search")
def search(request: Request, q: str = ""):
    all_syllabuses = [
        {"id": 1, "subject_code": "CS101", "subject_name": "Intro to IT"},
        {"id": 2, "subject_code": "CS102", "subject_name": "Programming"},
        {"id": 3, "subject_code": "CS201", "subject_name": "Data Structures"},
    ]

    if q:
        syllabuses = [
            s for s in all_syllabuses
            if q.lower() in s["subject_code"].lower()
            or q.lower() in s["subject_name"].lower()
        ]
    else:
        syllabuses = all_syllabuses

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "syllabuses": syllabuses
        }
    )

@router.get("/syllabus/{sid}")
def syllabus_detail(request: Request, sid: int):
    syllabus = {
        "id": sid,
        "subject_code": "CS101",
        "subject_name": "Intro to IT",
        "credits": 3,
        "description": "Giới thiệu ngành Công nghệ thông tin.",
        "clos": "CLO1, CLO2, CLO3",
        "assessment": "Midterm 30%, Final 50%, Assignment 20%",
        "materials": "Slide, Textbook, Online resources"
    }

    ai_summary = "Môn học cung cấp kiến thức nền tảng về CNTT và lập trình cơ bản."

    return templates.TemplateResponse(
        "syllabus.html",
        {
            "request": request,
            "s": syllabus,
            "ai_summary": ai_summary
        }
    )

@router.post("/follow/{sid}")
def follow_syllabus(sid: int):
    # Sau này lưu DB
    return RedirectResponse(
        url="/student/syllabus/" + str(sid),
        status_code=303
    )
2