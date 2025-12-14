from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import json

from ..models.syllabus import Syllabus, SyllabusVersion
from ..models.user import User
from ..schemas.syllabus_schema import SyllabusCreate, SyllabusUpdate
from ..repositories.syllabus_repo import SyllabusRepository, SyllabusVersionRepository
<<<<<<< HEAD
from fastapi import HTTPException
=======
from ..core.exceptions import HTTPException
>>>>>>> origin/HoangLong


class SyllabusService:
    """Service for Syllabus operations"""

    def __init__(self):
        self.repo = SyllabusRepository()
        self.version_repo = SyllabusVersionRepository()

    def create_syllabus(
        self,
        db: Session,
        syllabus_in: SyllabusCreate,
        user_id: int
    ) -> Syllabus:
        """
        Create new syllabus with initial version tracking
        
        Quy trình:
        1. Kiểm tra xem subject_code đã tồn tại chưa
        2. Tạo syllabus mới với status = "draft"
        3. Tự động tạo version 1 cho syllabus
        """
        # Check if subject_code already exists
        existing = self.repo.get_by_code(db, syllabus_in.subject_code)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Subject code '{syllabus_in.subject_code}' already exists"
            )

        # Prepare syllabus data
        syllabus_data = syllabus_in.dict()
        syllabus_data["created_by"] = user_id
        syllabus_data["status"] = "draft"
        syllabus_data["is_published"] = False

        # Create syllabus
        syllabus = self.repo.create(db, syllabus_data)

        # Create initial version
        self.version_repo.create(
            db,
            {
                "syllabus_id": syllabus.id,
                "version_number": 1,
                "change_summary": "Initial creation",
                "change_description": f"Giáo trình '{syllabus.subject_name}' được tạo lần đầu",
                "subject_code": syllabus.subject_code,
                "subject_name": syllabus.subject_name,
                "content": syllabus.content,
                "changed_fields": [],
                "version_status": "saved",
                "created_by": user_id
            }
        )

        return syllabus

    def update_syllabus(
        self,
        db: Session,
        syllabus_id: int,
        update_data: SyllabusUpdate,
        user_id: int
    ) -> Syllabus:
        """
        Update syllabus and automatically create new version
        
        Quy trình:
        1. Lấy syllabus hiện tại
        2. Phát hiện các trường đã thay đổi
        3. Cập nhật syllabus
        4. Tạo version mới với changelog
        """
        syllabus = self.repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        # Detect changed fields
        changed_fields = []
        previous_values = {}
        new_values = {}

        update_dict = update_data.dict(exclude_unset=True)
        change_summary = update_dict.pop("change_summary", "Manual update")

        for field, new_value in update_dict.items():
            old_value = getattr(syllabus, field, None)
            if old_value != new_value:
                changed_fields.append(field)
                previous_values[field] = old_value
                new_values[field] = new_value

        # Update syllabus
        updated_syllabus = self.repo.update(db, syllabus, update_dict)

        # Create version record if there are changes
        if changed_fields:
            next_version_number = self.version_repo.get_version_number(db, syllabus_id)
            self.version_repo.create(
                db,
                {
                    "syllabus_id": syllabus_id,
                    "version_number": next_version_number,
                    "change_summary": change_summary,
                    "change_description": f"Updated: {', '.join(changed_fields)}",
                    "subject_code": updated_syllabus.subject_code,
                    "subject_name": updated_syllabus.subject_name,
                    "content": updated_syllabus.content,
                    "changed_fields": changed_fields,
                    "previous_values": previous_values,
                    "new_values": new_values,
                    "version_status": "saved",
                    "created_by": user_id
                }
            )

        return updated_syllabus

    def get_syllabus(self, db: Session, syllabus_id: int) -> Optional[Syllabus]:
        """Get syllabus by ID"""
        return self.repo.get_by_id(db, syllabus_id)

    def get_syllabus_by_code(self, db: Session, subject_code: str) -> Optional[Syllabus]:
        """Get syllabus by subject code"""
        return self.repo.get_by_code(db, subject_code)

    def list_my_syllabuses(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        semester: Optional[int] = None,
        department: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Syllabus], int]:
        """List syllabuses created by current user"""
        return self.repo.list_by_lecturer(
            db, user_id, skip, limit, semester, department, status
        )

    def list_published_syllabuses(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        semester: Optional[int] = None,
        department: Optional[str] = None
    ) -> Tuple[List[Syllabus], int]:
        """List published syllabuses"""
        return self.repo.list_published(db, skip, limit, semester, department)

    def search_syllabuses(
        self,
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Syllabus], int]:
        """Search syllabuses by keyword"""
        return self.repo.search(db, keyword, skip, limit)

    def delete_syllabus(self, db: Session, syllabus_id: int) -> bool:
        """Delete syllabus and all its versions"""
        return self.repo.delete(db, syllabus_id)

    def publish_syllabus(self, db: Session, syllabus_id: int) -> Optional[Syllabus]:
        """
        Publish syllabus (change status to published)
        Chỉ có thể publish khi ở trạng thái "approved"
        """
        syllabus = self.repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        if syllabus.status != "approved":
            raise HTTPException(
                status_code=400,
                detail="Syllabus must be 'approved' before publishing"
            )

        return self.repo.update_status(
            db, syllabus_id, "published", True, datetime.utcnow()
        )

    def update_syllabus_status(
        self,
        db: Session,
        syllabus_id: int,
        new_status: str
    ) -> Optional[Syllabus]:
        """Update syllabus workflow status"""
        valid_statuses = ["draft", "submitted", "under_review", "approved", "published"]
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        syllabus = self.repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        return self.repo.update_status(db, syllabus_id, new_status)


class SyllabusVersionService:
    """Service for Syllabus Version operations"""

    def __init__(self):
        self.version_repo = SyllabusVersionRepository()
        self.repo = SyllabusRepository()

    def get_version(self, db: Session, version_id: int) -> Optional[SyllabusVersion]:
        """Get specific version"""
        return self.version_repo.get_by_id(db, version_id)

    def get_latest_version(self, db: Session, syllabus_id: int) -> Optional[SyllabusVersion]:
        """Get latest version of a syllabus"""
        return self.version_repo.get_latest_version(db, syllabus_id)

    def list_versions(
        self,
        db: Session,
        syllabus_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[SyllabusVersion], int]:
        """
        List all versions of a syllabus
        Sắp xếp theo mới nhất trước
        """
        return self.version_repo.list_versions(db, syllabus_id, skip, limit)

    def get_version_history(
        self,
        db: Session,
        syllabus_id: int,
        limit: int = 50
    ) -> List[SyllabusVersion]:
        """Get version history timeline"""
        return self.version_repo.get_version_history(db, syllabus_id, limit)

    def rollback_to_version(
        self,
        db: Session,
        syllabus_id: int,
        version_id: int,
        user_id: int
    ) -> Optional[Syllabus]:
        """
        Rollback syllabus to a specific version
        
        Quy trình:
        1. Lấy version được chỉ định
        2. Kiểm tra xem nó có thuộc syllabus này không
        3. Restore nội dung từ version đó
        4. Tạo version mới với ghi chú rollback
        """
        version = self.version_repo.get_by_id(db, version_id)
        if not version or version.syllabus_id != syllabus_id:
            raise HTTPException(status_code=404, detail="Version not found")

        syllabus = self.repo.get_by_id(db, syllabus_id)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")

        # Get current state before rollback
        old_content = syllabus.content

        # Restore from version
        update_data = {
            "content": version.content,
            "subject_name": version.subject_name
        }

        updated = self.repo.update(db, syllabus, update_data)

        # Create rollback version record
        next_version = self.version_repo.get_version_number(db, syllabus_id)
        self.version_repo.create(
            db,
            {
                "syllabus_id": syllabus_id,
                "version_number": next_version,
                "change_summary": f"Rollback to version {version.version_number}",
                "change_description": f"Reverted to version {version.version_number}",
                "subject_code": updated.subject_code,
                "subject_name": updated.subject_name,
                "content": updated.content,
                "changed_fields": ["content"],
                "previous_values": {"content": old_content},
                "new_values": {"content": version.content},
                "version_status": "saved",
                "created_by": user_id
            }
        )

        return updated

    def compare_versions(
        self,
        db: Session,
        version_id_1: int,
        version_id_2: int
    ) -> Dict[str, Any]:
        """Compare two versions and show differences"""
        return self.version_repo.compare_versions(db, version_id_1, version_id_2)

    def export_version(
        self,
        db: Session,
        version_id: int
    ) -> Optional[Dict[str, Any]]:
        """Export version as JSON"""
        version = self.version_repo.get_by_id(db, version_id)
        if not version:
            return None

        return {
            "version_number": version.version_number,
            "subject_code": version.subject_code,
            "subject_name": version.subject_name,
            "content": version.content,
            "created_at": version.created_at,
            "created_by": version.created_by,
            "change_summary": version.change_summary,
            "change_description": version.change_description
        }
