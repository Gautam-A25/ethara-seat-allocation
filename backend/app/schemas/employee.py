from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import EmployeeStatus


class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    email: EmailStr
    department: str
    role: str
    joining_date: date
    status: EmployeeStatus
    project_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None
    joining_date: Optional[date] = None
    status: Optional[EmployeeStatus] = None
    project_id: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)