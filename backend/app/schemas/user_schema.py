from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    employee_id: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = Field(default="student")
    
    # Academic information
    degree: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    specialization: Optional[str] = None
    
    # Contact information
    phone: Optional[str] = None
    office_location: Optional[str] = None
    
    # Research & Teaching information
    research_interests: Optional[str] = None
    teaching_subjects: Optional[str] = None
    years_experience: Optional[int] = None
    qualifications: Optional[str] = None
    publications: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    employee_id: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    
    # Academic information
    degree: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    specialization: Optional[str] = None
    
    # Contact information
    phone: Optional[str] = None
    office_location: Optional[str] = None
    
    # Research & Teaching information
    research_interests: Optional[str] = None
    teaching_subjects: Optional[str] = None
    years_experience: Optional[int] = None
    qualifications: Optional[str] = None
    publications: Optional[str] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    syllabus_count: Optional[int] = 0
    created_at: datetime
    updated_at: Optional[datetime] = None  # Can be None on first create

    class Config:
        from_attributes = True


class UserListOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenUser(BaseModel):
    """User info trong Token response"""
    id: int
    email: str
    role: str
    full_name: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional[TokenUser] = None  # User info


class TokenData(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class LockStatus(BaseModel):
    is_locked: bool
