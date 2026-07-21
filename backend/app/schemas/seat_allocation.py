from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import AllocationStatus


class SeatAllocationRequest(BaseModel):
    employee_id: int
    seat_id: int


class SeatReleaseRequest(BaseModel):
    employee_id: int


class SeatAllocationResponse(BaseModel):
    id: int
    employee_id: int
    seat_id: int
    project_id: int
    allocation_status: AllocationStatus
    allocation_date: datetime
    released_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)