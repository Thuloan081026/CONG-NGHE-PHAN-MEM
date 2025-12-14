from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.syllabus import Syllabus, SyllabusVersion
from .base import BaseRepository


class SyllabusRepository(BaseRepository[Syllabus]):
    """Repository for Syllabus CRUD operations"""

    def get_by_code(self, db: Session, subject_code: str) -> Optional[Syllabus]:
        """Get syllabus by subject code"""
        return db.query(Syllabus).filter(Syllabus.subject_code == subject_code).first()

    def get_by_id(self, db: Session, syllabus_id: int) -> Optional[Syllabus]:
        """Get syllabus by ID"""
        return db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()

    def list_by_lecturer(
        self,
        db: Session,
        lecturer_id: int,
        skip: int = 0,
        limit: int = 100,
        semester: Optional[int] = None,
        department: Optional[str] = None,
        status: Optional[str] = None
    ) -> tuple[List[Syllabus], int]:
        """List syllabuses by lecturer with optional filters"""
        query = db.query(Syllabus).filter(Syllabus.created_by == lecturer_id)

        if semester:
            query = query.filter(Syllabus.semester == semester)
        if department:
            query = query.filter(Syllabus.department == department)
        if status:
            query = query.filter(Syllabus.status == status)

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def list_published(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        semester: Optional[int] = None,
        department: Optional[str] = None
    ) -> tuple[List[Syllabus], int]:
        """List published syllabuses"""
        query = db.query(Syllabus).filter(
            and_(Syllabus.is_published == True, Syllabus.status == "published")
        )

        if semester:
            query = query.filter(Syllabus.semester == semester)
        if department:
            query = query.filter(Syllabus.department == department)

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def list_by_department(
        self,
        db: Session,
        department: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Syllabus], int]:
        """List syllabuses by department"""
        query = db.query(Syllabus).filter(Syllabus.department == department)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def search(
        self,
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Syllabus], int]:
        """Search syllabuses by code or name"""
        query = db.query(Syllabus).filter(
            or_(
                Syllabus.subject_code.ilike(f"%{keyword}%"),
                Syllabus.subject_name.ilike(f"%{keyword}%"),
                Syllabus.description.ilike(f"%{keyword}%")
            )
        )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, obj_in: Dict[str, Any]) -> Syllabus:
        """Create new syllabus"""
        db_obj = Syllabus(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Syllabus, obj_in: Dict[str, Any]) -> Syllabus:
        """Update syllabus"""
        for field, value in obj_in.items():
            if value is not None and hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, syllabus_id: int) -> bool:
        """Delete syllabus"""
        syllabus = self.get_by_id(db, syllabus_id)
        if syllabus:
            db.delete(syllabus)
            db.commit()
            return True
        return False

    def update_status(
        self,
        db: Session,
        syllabus_id: int,
        status: str,
        is_published: bool = False,
        published_at: Optional[datetime] = None
    ) -> Optional[Syllabus]:
        """Update syllabus status"""
        syllabus = self.get_by_id(db, syllabus_id)
        if syllabus:
            syllabus.status = status
            syllabus.is_published = is_published
            if is_published:
                syllabus.published_at = published_at or datetime.utcnow()
            db.add(syllabus)
            db.commit()
            db.refresh(syllabus)
        return syllabus


class SyllabusVersionRepository(BaseRepository[SyllabusVersion]):
    """Repository for Syllabus Version (version control)"""

    def get_by_id(self, db: Session, version_id: int) -> Optional[SyllabusVersion]:
        """Get version by ID"""
        return db.query(SyllabusVersion).filter(SyllabusVersion.id == version_id).first()

    def get_latest_version(self, db: Session, syllabus_id: int) -> Optional[SyllabusVersion]:
        """Get latest version of a syllabus"""
        return db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus_id
        ).order_by(desc(SyllabusVersion.version_number)).first()

    def list_versions(
        self,
        db: Session,
        syllabus_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[SyllabusVersion], int]:
        """List all versions of a syllabus"""
        query = db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus_id
        ).order_by(desc(SyllabusVersion.version_number))

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def get_version_number(self, db: Session, syllabus_id: int) -> int:
        """Get next version number for a syllabus"""
        latest = self.get_latest_version(db, syllabus_id)
        return (latest.version_number + 1) if latest else 1

    def create(self, db: Session, obj_in: Dict[str, Any]) -> SyllabusVersion:
        """Create new version record"""
        db_obj = SyllabusVersion(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_version_history(
        self,
        db: Session,
        syllabus_id: int,
        limit: int = 50
    ) -> List[SyllabusVersion]:
        """Get version history with pagination"""
        return db.query(SyllabusVersion).filter(
            SyllabusVersion.syllabus_id == syllabus_id
        ).order_by(desc(SyllabusVersion.created_at)).limit(limit).all()

    def compare_versions(
        self,
        db: Session,
        version_id_1: int,
        version_id_2: int
    ) -> Optional[Dict[str, Any]]:
        """Compare two versions and return differences"""
        v1 = self.get_by_id(db, version_id_1)
        v2 = self.get_by_id(db, version_id_2)

        if not v1 or not v2:
            return None

        return {
            "version_1": v1.version_number,
            "version_2": v2.version_number,
            "differences": {
                "changed_fields": v2.changed_fields,
                "previous_values": v2.previous_values,
                "new_values": v2.new_values
            }
        }
