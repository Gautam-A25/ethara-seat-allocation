from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_employees: int
    total_seats: int
    occupied_seats: int
    available_seats: int
    reserved_seats: int
    pending_allocation: int


class ProjectUtilizationResponse(BaseModel):
    project_name: str
    allocated_seats: int


class FloorUtilizationResponse(BaseModel):
    floor: int
    occupied_seats: int
    available_seats: int