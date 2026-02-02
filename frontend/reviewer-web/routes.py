from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Import các module từ project của bạn
from database import get_db
from models.syllabus import Syllabus

router = APIRouter(prefix="/reviewer", tags=["Reviewer"])
templates = Jinja2Templates(directory="frontend/reviewer-web/templates")

# --- MOCK DATA (GIẢ LẬP USER) ---
MOCK_USER = {
    "id": 1,
    "full_name": "Nguyen Van Chien",
    "email": "chien.nv@university.edu.vn",
    "role": "Head of Department (HoD)",
    "department": "Software Engineering",
    "phone": "0901234567"
}

# =========================================================
# 1. PROFILE
# =========================================================

@router.get("/profile")
def view_profile(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": MOCK_USER
        }
    )

@router.post("/profile/update")
def update_profile(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(None)
):
    MOCK_USER["full_name"] = full_name
    MOCK_USER["phone"] = phone

    if password:
        print(f"Password change requested for {MOCK_USER['email']}")

    return RedirectResponse(
        url="/reviewer/profile",
        status_code=303
    )

# =========================================================
# 2. SYLLABUS WORKFLOW
# =========================================================

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    syllabuses = (
        db.query(Syllabus)
        .filter(Syllabus.status == "PENDING_REVIEW")
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "syllabuses": syllabuses
        }
    )

@router.get("/review/{sid}")
def review_detail(
    request: Request,
    sid: int,
    db: Session = Depends(get_db)
):
    syllabus = (
        db.query(Syllabus)
        .filter(Syllabus.id == sid)
        .first()
    )

    return templates.TemplateResponse(
        "review_detail.html",
        {
            "request": request,
            "syllabus": syllabus
        }
    )

@router.post("/approve/{sid}")
def approve_syllabus(
    sid: int,
    db: Session = Depends(get_db)
):
    syllabus = db.query(Syllabus).filter(Syllabus.id == sid).first()

    if syllabus:
        syllabus.status = "APPROVED"
        syllabus.reject_reason = None
        db.commit()

    return RedirectResponse(
        url="/reviewer/dashboard",
        status_code=303
    )

@router.post("/reject/{sid}")
def reject_syllabus(
    sid: int,
    reason: str = Form(...),
    db: Session = Depends(get_db)
):
    syllabus = db.query(Syllabus).filter(Syllabus.id == sid).first()

    if syllabus:
        syllabus.status = "REJECTED"
        syllabus.reject_reason = reason
        db.commit()

    return RedirectResponse(
        url="/reviewer/dashboard",
        status_code=303
    )

@router.get("/compare/{sid1}/{sid2}")
def compare_version(
    request: Request,
    sid1: int,
    sid2: int,
    db: Session = Depends(get_db)
):
    old_syllabus = db.query(Syllabus).filter(Syllabus.id == sid1).first()
    new_syllabus = db.query(Syllabus).filter(Syllabus.id == sid2).first()

    ai_detected_changes = [
        "Description: Changed focus from 'Basic Java' to 'Advanced OOP'",
        "CLO 3: Updated verb from 'Understand' to 'Analyze' (Bloom Level increased)"
    ]

    return templates.TemplateResponse(
        "compare.html",
        {
            "request": request,
            "old_syllabus": old_syllabus,
            "new_syllabus": new_syllabus,
            "changes": ai_detected_changes
        }
    )
