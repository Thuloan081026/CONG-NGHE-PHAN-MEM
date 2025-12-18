"""
Search Service for Syllabus Search
Provides search and filtering capabilities for students
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from ..models.syllabus import Syllabus
from ..models.user import User


class SearchService:
    """Service for searching syllabuses with filters"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def search_syllabuses(
        self,
        query: Optional[str] = None,
        department: Optional[str] = None,
        semester: Optional[int] = None,
        academic_year: Optional[str] = None,
        full_text: Optional[str] = None,
        status: str = "published",
        skip: int = 0,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search syllabuses with multiple filters
        
        Args:
            query: Search by subject name or code (basic search)
            department: Filter by department/major
            semester: Filter by semester
            academic_year: Filter by academic year
            full_text: Full-text search across content fields
            status: Filter by status (default: published)
            skip: Pagination offset
            limit: Pagination limit
            
        Returns:
            Dictionary with results and total count
        """
        # Build base query
        db_query = self.db.query(Syllabus)
        
        # Apply status filter (default: only published syllabuses for students)
        if status:
            db_query = db_query.filter(Syllabus.status == status)
            if status == "published":
                db_query = db_query.filter(Syllabus.is_published == True)
        
        # Basic search: subject name or code
        if query:
            search_pattern = f"%{query}%"
            db_query = db_query.filter(
                or_(
                    Syllabus.subject_name.ilike(search_pattern),
                    Syllabus.subject_code.ilike(search_pattern)
                )
            )
        
        # Filter by department
        if department:
            db_query = db_query.filter(Syllabus.department == department)
        
        # Filter by semester
        if semester is not None:
            db_query = db_query.filter(Syllabus.semester == semester)
        
        # Filter by academic year
        if academic_year:
            db_query = db_query.filter(Syllabus.academic_year == academic_year)
        
        # Full-text search across content fields
        if full_text:
            text_pattern = f"%{full_text}%"
            db_query = db_query.filter(
                or_(
                    Syllabus.subject_name.ilike(text_pattern),
                    Syllabus.subject_code.ilike(text_pattern),
                    Syllabus.description.ilike(text_pattern),
                    Syllabus.objectives.ilike(text_pattern),
                    Syllabus.content.ilike(text_pattern),
                    Syllabus.teaching_methods.ilike(text_pattern),
                    Syllabus.assessment_methods.ilike(text_pattern)
                )
            )
        
        # Get total count before pagination
        total = db_query.count()
        
        # Apply ordering and pagination
        results = db_query.order_by(
            Syllabus.subject_code.asc()
        ).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "results": results
        }
    
    def get_search_filters(self) -> Dict[str, List[Any]]:
        """
        Get available filter options for search UI
        
        Returns:
            Dictionary with available departments, semesters, and academic years
        """
        # Get distinct departments
        departments = self.db.query(Syllabus.department).filter(
            Syllabus.department.isnot(None),
            Syllabus.is_published == True
        ).distinct().order_by(Syllabus.department).all()
        
        # Get distinct semesters
        semesters = self.db.query(Syllabus.semester).filter(
            Syllabus.semester.isnot(None),
            Syllabus.is_published == True
        ).distinct().order_by(Syllabus.semester).all()
        
        # Get distinct academic years
        academic_years = self.db.query(Syllabus.academic_year).filter(
            Syllabus.academic_year.isnot(None),
            Syllabus.is_published == True
        ).distinct().order_by(Syllabus.academic_year.desc()).all()
        
        return {
            "departments": [d[0] for d in departments],
            "semesters": [s[0] for s in semesters],
            "academic_years": [y[0] for y in academic_years]
        }
    
    def search_by_code(self, subject_code: str) -> Optional[Syllabus]:
        """
        Get a specific syllabus by subject code
        
        Args:
            subject_code: Subject code to search for
            
        Returns:
            Syllabus object or None
        """
        return self.db.query(Syllabus).filter(
            Syllabus.subject_code == subject_code,
            Syllabus.is_published == True
        ).first()
    
    def get_related_syllabuses(self, syllabus_id: int, limit: int = 5) -> List[Syllabus]:
        """
        Get related syllabuses based on department and semester
        
        Args:
            syllabus_id: ID of the source syllabus
            limit: Maximum number of results
            
        Returns:
            List of related syllabuses
        """
        # Get source syllabus
        source = self.db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
        if not source:
            return []
        
        # Find related syllabuses in same department or semester
        query = self.db.query(Syllabus).filter(
            Syllabus.id != syllabus_id,
            Syllabus.is_published == True,
            or_(
                Syllabus.department == source.department,
                Syllabus.semester == source.semester
            )
        )
        
        return query.order_by(Syllabus.created_at.desc()).limit(limit).all()
    
    def get_popular_syllabuses(self, limit: int = 10) -> List[Syllabus]:
        """
        Get most recently published syllabuses
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of popular syllabuses
        """
        return self.db.query(Syllabus).filter(
            Syllabus.is_published == True
        ).order_by(
            Syllabus.published_at.desc()
        ).limit(limit).all()
