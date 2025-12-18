from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from ..core.database import Base


class Syllabus(Base):
    """Model for Syllabus (Giáo trình)"""
    __tablename__ = "syllabuses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    subject_code = Column(String(50), unique=True, nullable=False, index=True)
    subject_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metadata
    credits = Column(Integer, nullable=True)  # Số tín chỉ
    semester = Column(Integer, nullable=True)  # Kỳ học
    department = Column(String(100), nullable=True)  # Bộ môn
    academic_year = Column(String(20), nullable=True)  # Năm học (2025-2026)
    
    # Content sections
    objectives = Column(Text, nullable=True)  # Mục tiêu học tập
    content = Column(Text, nullable=True)  # Nội dung giáo trình
    teaching_methods = Column(Text, nullable=True)  # Phương pháp giảng dạy
    assessment_methods = Column(Text, nullable=True)  # Phương pháp đánh giá
    
    # Prerequisites & relationships
    prerequisites = Column(JSON, nullable=True)  # [{id, name}, ...] of prerequisite subjects
    corequisites = Column(JSON, nullable=True)  # Học song song
    related_subjects = Column(JSON, nullable=True)  # Các môn liên quan
    
    # CLO/PLO (Competency & Program Learning Outcomes)
    clos = Column(JSON, nullable=True)  # [{"id": "CLO1", "description": "...", "level": "K3"}, ...]
    plos = Column(JSON, nullable=True)  # [{"id": "PLO1", "description": "...", "alignment": 0.8}, ...]
    clo_plo_mapping = Column(JSON, nullable=True)  # {"CLO1": ["PLO1", "PLO2"], ...}
    
    # Assessment weights
    assessment_weights = Column(JSON, nullable=True)  # {"attendance": 10, "assignment": 30, "exam": 60}
    
    # Learning materials & resources
    textbooks = Column(JSON, nullable=True)  # [{"title": "...", "author": "...", "year": 2024}, ...]
    references = Column(JSON, nullable=True)  # [{"title": "...", "url": "...", "type": "website"}, ...]
    learning_materials = Column(JSON, nullable=True)  # Slides, videos, etc.
    
    # Status & ownership
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Lecturer ID
    status = Column(String(50), default="draft")  # draft, submitted, under_review, approved, published
    is_published = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    versions = relationship("SyllabusVersion", back_populates="syllabus", cascade="all, delete-orphan")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    workflow_events = relationship("WorkflowEvent", back_populates="syllabus")
=======
>>>>>>> origin/HoangLong
=======
>>>>>>> origin/NgoUyen
=======
>>>>>>> origin/ThuMinh
    creator = relationship("User", foreign_keys=[created_by])


class SyllabusVersion(Base):
    """Model for Syllabus Version (Version control)"""
    __tablename__ = "syllabus_versions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    syllabus_id = Column(Integer, ForeignKey("syllabuses.id"), nullable=False, index=True)
    
    # Version info
    version_number = Column(Integer, nullable=False)  # 1, 2, 3, ...
    change_summary = Column(String(255), nullable=True)  # "Updated CLO mappings", "Fixed typos"
    change_description = Column(Text, nullable=True)  # Detailed changelog
    
    # Snapshot of content at this version
    subject_code = Column(String(50), nullable=False)
    subject_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    
    # Changed fields (for diff detection)
    changed_fields = Column(JSON, nullable=True)  # ["content", "clos", "assessment_weights"]
    previous_values = Column(JSON, nullable=True)  # {"content": "old value", ...}
    new_values = Column(JSON, nullable=True)  # {"content": "new value", ...}
    
    # Version status in workflow
    version_status = Column(String(50), default="saved")  # saved, submitted, review, approved
    
    # Who made the change
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    syllabus = relationship("Syllabus", back_populates="versions")
    creator = relationship("User", foreign_keys=[created_by])


# For backward compatibility, also import User
from .user import User
