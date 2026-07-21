from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import SeatStatus


class SeatBase(BaseModel):
    floor: int
    zone: str
    bay: str
    seat_number: str
    status: SeatStatus


class SeatCreate(SeatBase):
    pass


class SeatUpdate(BaseModel):
    floor: Optional[int] = None
    zone: Optional[str] = None
    bay: Optional[str] = None
    seat_number: Optional[str] = None
    status: Optional[SeatStatus] = None


class SeatResponse(SeatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SeatSuggestionResponse(BaseModel):
    floor: int
    zone: str
    bay: str
    seat_number: str

    model_config = ConfigDict(from_attributes=True)