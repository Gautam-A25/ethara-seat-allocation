from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.enums import (
    AllocationStatus,
    SeatStatus,
)
from app.models.project import Project
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation

def get_dashboard_summary(db: Session):
    total_employees = db.query(Employee).count()

    total_seats = db.query(Seat).count()

    occupied_seats = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.OCCUPIED)
        .count()
    )

    available_seats = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.AVAILABLE)
        .count()
    )

    reserved_seats = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.RESERVED)
        .count()
    )

    active_allocations = (
        db.query(SeatAllocation.employee_id)
        .filter(
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE
        )
        .subquery()
    )

    pending_allocation = (
        db.query(Employee)
        .filter(~Employee.id.in_(active_allocations))
        .count()
    )

    return {
        "total_employees": total_employees,
        "total_seats": total_seats,
        "occupied_seats": occupied_seats,
        "available_seats": available_seats,
        "reserved_seats": reserved_seats,
        "pending_allocation": pending_allocation,
    }

def get_project_utilization(db: Session):
    results = (
        db.query(
            Project.name.label("project_name"),
            func.count(SeatAllocation.id).label("allocated_seats"),
        )
        .outerjoin(
            SeatAllocation,
            (Project.id == SeatAllocation.project_id)
            & (
                SeatAllocation.allocation_status
                == AllocationStatus.ACTIVE
            ),
        )
        .group_by(Project.id, Project.name)
        .order_by(Project.name)
        .all()
    )

    return [
        {
            "project_name": row.project_name,
            "allocated_seats": row.allocated_seats,
        }
        for row in results
    ]

def get_floor_utilization(db: Session):
    floors = (
        db.query(Seat.floor)
        .distinct()
        .order_by(Seat.floor)
        .all()
    )

    result = []

    for (floor,) in floors:
        occupied = (
            db.query(Seat)
            .filter(
                Seat.floor == floor,
                Seat.status == SeatStatus.OCCUPIED,
            )
            .count()
        )

        available = (
            db.query(Seat)
            .filter(
                Seat.floor == floor,
                Seat.status == SeatStatus.AVAILABLE,
            )
            .count()
        )

        result.append(
            {
                "floor": floor,
                "occupied_seats": occupied,
                "available_seats": available,
            }
        )

    return result