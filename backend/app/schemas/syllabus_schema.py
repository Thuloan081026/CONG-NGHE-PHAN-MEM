from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Base CLO (Course Learning Outcome) Schema
class CLOBase(BaseModel):
    id: str  # CLO1, CLO2, ...
    description: str
    level: Optional[str] = "K3"  # Bloom's taxonomy level
    
    class Config:
        from_attributes = True


# Base PLO (Program Learning Outcome) Schema
class PLOBase(BaseModel):
    id: str  # PLO1, PLO2, ...
    description: str
    alignment: Optional[float] = Field(None, ge=0, le=1)  # 0-1 score
    
    class Config:
        from_attributes = True


# Textbook/Reference Schema
class TextbookSchema(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    
    class Config:
        from_attributes = True


# Assessment weights Schema
class AssessmentWeightsSchema(BaseModel):
    attendance: Optional[float] = 0
    assignment: Optional[float] = 0
    midterm: Optional[float] = 0
    final_exam: Optional[float] = 0
    project: Optional[float] = 0
    other: Optional[float] = 0
    
    class Config:
        from_attributes = True


# Base Syllabus Schema (common fields)
class SyllabusBase(BaseModel):
    subject_code: str
    subject_name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    semester: Optional[int] = None
    department: Optional[str] = None
    academic_year: Optional[str] = None
    
    objectives: Optional[str] = None
    content: Optional[str] = None
    teaching_methods: Optional[str] = None
    assessment_methods: Optional[str] = None
    
    prerequisites: Optional[List[Dict[str, Any]]] = None
    corequisites: Optional[List[Dict[str, Any]]] = None
    related_subjects: Optional[List[Dict[str, Any]]] = None
    
    clos: Optional[List[Dict[str, Any]]] = None
    plos: Optional[List[Dict[str, Any]]] = None
    clo_plo_mapping: Optional[Dict[str, List[str]]] = None
    
    assessment_weights: Optional[Dict[str, float]] = None
    textbooks: Optional[List[Dict[str, Any]]] = None
    references: Optional[List[Dict[str, Any]]] = None
    learning_materials: Optional[List[Dict[str, Any]]] = None


# Create new Syllabus (request)
class SyllabusCreate(SyllabusBase):
    pass


# Update existing Syllabus
class SyllabusUpdate(BaseModel):
    subject_name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    semester: Optional[int] = None
    department: Optional[str] = None
    academic_year: Optional[str] = None
    
    objectives: Optional[str] = None
    content: Optional[str] = None
    teaching_methods: Optional[str] = None
    assessment_methods: Optional[str] = None
    
    prerequisites: Optional[List[Dict[str, Any]]] = None
    corequisites: Optional[List[Dict[str, Any]]] = None
    related_subjects: Optional[List[Dict[str, Any]]] = None
    
    clos: Optional[List[Dict[str, Any]]] = None
    plos: Optional[List[Dict[str, Any]]] = None
    clo_plo_mapping: Optional[Dict[str, List[str]]] = None
    
    assessment_weights: Optional[Dict[str, float]] = None
    textbooks: Optional[List[Dict[str, Any]]] = None
    references: Optional[List[Dict[str, Any]]] = None
    learning_materials: Optional[List[Dict[str, Any]]] = None
    
    change_summary: Optional[str] = None  # For version tracking


# Response Syllabus (with metadata)
class SyllabusOut(SyllabusBase):
    id: int
    created_by: int
    status: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# List of Syllabuses (pagination)
class SyllabusListOut(BaseModel):
    total: int
    count: int
    page: int
    page_size: int
    items: List[SyllabusOut]
    
    class Config:
        from_attributes = True


# Version related schemas
class SyllabusVersionBase(BaseModel):
    version_number: int
    change_summary: Optional[str] = None
    change_description: Optional[str] = None
    subject_code: str
    subject_name: str
    content: Optional[str] = None
    changed_fields: Optional[List[str]] = None
    previous_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    version_status: str = "saved"


class SyllabusVersionOut(SyllabusVersionBase):
    id: int
    syllabus_id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SyllabusVersionListOut(BaseModel):
    total: int
    versions: List[SyllabusVersionOut]
    
    class Config:
        from_attributes = True


# Full Syllabus with versions
class SyllabusDetailOut(SyllabusOut):
    versions: Optional[List[SyllabusVersionOut]] = None
    
    class Config:
        from_attributes = True


# Status update request
class SyllabusStatusUpdate(BaseModel):
    status: str  # draft, submitted, under_review, approved, published
    is_published: Optional[bool] = None
    change_summary: Optional[str] = None


# CLO-PLO Mapping request
class CLOPLOMappingUpdate(BaseModel):
    clo_plo_mapping: Dict[str, List[str]]  # {"CLO1": ["PLO1", "PLO2"], ...}


# Bulk operations
class SyllabusBulkCreate(BaseModel):
    syllabuses: List[SyllabusCreate]
