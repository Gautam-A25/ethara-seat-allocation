from enum import Enum


class EmployeeStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING = "Pending"


class ProjectStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class SeatStatus(str, Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"


class AllocationStatus(str, Enum):
    ACTIVE = "Active"
    RELEASED = "Released"