from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ...core.database import get_db
from ...core.deps import get_current_user
from ...models.user import User
from ...services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/syllabuses")
def search_syllabuses(
    query: Optional[str] = Query(None, description="Search by subject name or code"),
    department: Optional[str] = Query(None, description="Filter by department"),
    semester: Optional[int] = Query(None, description="Filter by semester"),
    academic_year: Optional[str] = Query(None, description="Filter by academic year"),
    full_text: Optional[str] = Query(None, description="Full-text search across content"),
    status: str = Query("published", description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search syllabuses with filters
    - Query: search by name or code
    - Department: filter by major
    - Semester: filter by semester (1-8)
    - Full-text: search content
    """
    search_service = SearchService(db)
    return search_service.search_syllabuses(
        query=query,
        department=department,
        semester=semester,
        academic_year=academic_year,
        full_text=full_text,
        status=status,
        skip=skip,
        limit=limit
    )


@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of unique departments"""
    search_service = SearchService(db)
    return search_service.get_departments()


@router.get("/academic-years")
def get_academic_years(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of unique academic years"""
    search_service = SearchService(db)
    return search_service.get_academic_years()
