from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# CLO Schemas
class CLOBase(BaseModel):
    code: str
    description: str
    cognitive_level: Optional[str] = None
    weight: Optional[float] = 1.0


class CLOCreate(CLOBase):
    syllabus_id: int


class CLOUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    cognitive_level: Optional[str] = None
    weight: Optional[float] = None


class CLOResponse(CLOBase):
    id: int
    syllabus_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# PLO Schemas
class PLOBase(BaseModel):
    code: str
    description: str
    program_code: Optional[str] = None
    program_name: Optional[str] = None
    category: Optional[str] = None
    weight: Optional[float] = 1.0


class PLOCreate(PLOBase):
    pass


class PLOUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    program_code: Optional[str] = None
    program_name: Optional[str] = None
    category: Optional[str] = None
    weight: Optional[float] = None


class PLOResponse(PLOBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# CLO-PLO Mapping Schemas
class MappingBase(BaseModel):
    clo_id: int
    plo_id: int
    correlation_level: Optional[str] = None
    correlation_score: Optional[float] = None
    ai_suggested: Optional[int] = 0
    ai_confidence: Optional[float] = None
    notes: Optional[str] = None


class MappingCreate(MappingBase):
    @validator('correlation_score')
    def validate_score(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('correlation_score must be between 0 and 1')
        return v


class MappingUpdate(BaseModel):
    correlation_level: Optional[str] = None
    correlation_score: Optional[float] = None
    notes: Optional[str] = None


class MappingResponse(MappingBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class BulkCLOCreate(BaseModel):
    syllabus_id: int
    clos: List[CLOBase]


class BulkMappingCreate(BaseModel):
    mappings: List[MappingCreate]


class SyllabusMappingMatrix(BaseModel):
    syllabus_id: int
    clos: List[CLOResponse]
    plos: List[PLOResponse]
    mappings: List[MappingResponse]
