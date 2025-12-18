"""
AI Integration Schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class SummarizeRequest(BaseModel):
    """Request to summarize syllabus content"""
    syllabus_id: int
    language: Optional[str] = "vi"  # vi or en


class SummarizeResponse(BaseModel):
    """AI Summary response"""
    syllabus_id: int
    summary: str
    key_points: List[str]
    generated_at: datetime
    
    class Config:
        from_attributes = True


class DiffRequest(BaseModel):
    """Request to compare two syllabus versions"""
    version_id_1: int
    version_id_2: int
    language: Optional[str] = "vi"


class DiffResponse(BaseModel):
    """Semantic diff between two versions"""
    version_1: int
    version_2: int
    changes_summary: str
    major_changes: List[Dict[str, Any]]
    minor_changes: List[Dict[str, Any]]
    impact_analysis: str
    
    class Config:
        from_attributes = True


class CLOCheckRequest(BaseModel):
    """Request to check CLO mapping suggestions"""
    syllabus_id: int
    clo_description: str


class CLOSuggestion(BaseModel):
    """Similar CLO suggestion"""
    clo_id: int
    clo_code: str
    description: str
    similarity_score: float
    syllabus_code: str
    syllabus_name: str


class CLOCheckResponse(BaseModel):
    """CLO similarity check response"""
    input_clo: str
    suggestions: List[CLOSuggestion]
    total_found: int
    
    class Config:
        from_attributes = True
