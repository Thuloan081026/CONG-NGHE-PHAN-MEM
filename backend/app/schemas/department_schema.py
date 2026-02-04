"""Department schemas"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class DepartmentBase(BaseModel):
    code: str
    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    head_of_department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    office_location: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    description: Optional[str] = None
    head_of_department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    office_location: Optional[str] = None
    is_active: Optional[bool] = None


class DepartmentOut(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DepartmentListOut(BaseModel):
    id: int
    code: str
    name: str
    head_of_department: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
