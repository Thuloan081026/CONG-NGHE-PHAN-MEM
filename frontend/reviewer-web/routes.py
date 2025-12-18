from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.syllabus import Syllabus

router = APIRouter(prefix="/reviewer", tags=["Reviewer"])
templates = Jinja2Templates(directory="frontend/reviewer-web/templates")

@router.get("/review/{sid}")
def review_detail(
    request: Request,
    sid: int,
    db: Session = Depends(get_db)
):
    syllabus = db.query(Syllabus)\
                 .filter(Syllabus.id == sid)\
                 .first()

    return templates.TemplateResponse(
        "review_detail.html",
        {
            "request": request,
            "s": syllabus
        }
    )

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    syllabuses = db.query(Syllabus)\
                   .filter(Syllabus.status == "PENDING_REVIEW")\
                   .all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "syllabuses": syllabuses
        }
    )

@router.post("/approve/{sid}")
def approve_syllabus(
    sid: int,
    db: Session = Depends(get_db)
):
    syllabus = db.query(Syllabus)\
                 .filter(Syllabus.id == sid)\
                 .first()

    syllabus.status = "APPROVED"
    syllabus.reject_reason = None
    db.commit()

    return RedirectResponse(
        "/reviewer/dashboard",
        status_code=303
    )

@router.post("/reject/{sid}")
def reject_syllabus(
    sid: int,
    reason: str = Form(...),
    db: Session = Depends(get_db)
):
    syllabus = db.query(Syllabus)\
                 .filter(Syllabus.id == sid)\
                 .first()

    syllabus.status = "REJECTED"
    syllabus.reject_reason = reason
    db.commit()

    return RedirectResponse(
        "/reviewer/dashboard",
        status_code=303
    )

@router.get("/compare/{sid1}/{sid2}")
def compare_version(
    request: Request,
    sid1: int,
    sid2: int,
    db: Session = Depends(get_db)
):
    s1 = db.query(Syllabus).filter(Syllabus.id == sid1).first()
    s2 = db.query(Syllabus).filter(Syllabus.id == sid2).first()

    return templates.TemplateResponse(
        "compare.html",
        {
            "request": request,
            "s1": s1,
            "s2": s2
        }
    )
