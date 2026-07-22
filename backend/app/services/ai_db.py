from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.employee import Employee
from app.models.project import Project
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation
from app.models.enums import AllocationStatus, SeatStatus

from app.services.dashboard_service import get_dashboard_summary


def get_employee_seat(db: Session, employee_code: str):
    allocation = (
        db.query(SeatAllocation)
        .join(Employee, SeatAllocation.employee_id == Employee.id)
        .join(Seat, SeatAllocation.seat_id == Seat.id)
        .join(Project, SeatAllocation.project_id == Project.id)
        .filter(
            Employee.employee_code == employee_code,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if allocation is None:
        return None

    return {
        "employee": allocation.employee.name,
        "employee_code": allocation.employee.employee_code,
        "project": allocation.project.name,
        "floor": allocation.seat.floor,
        "zone": allocation.seat.zone,
        "bay": allocation.seat.bay,
        "seat": allocation.seat.seat_number,
    }


def get_available_seats(db: Session, floor: int | None = None):
    query = db.query(Seat).filter(
        Seat.status == SeatStatus.AVAILABLE
    )

    if floor is not None:
        query = query.filter(Seat.floor == floor)

    seats = query.limit(20).all()

    return [
        {
            "floor": s.floor,
            "zone": s.zone,
            "bay": s.bay,
            "seat": s.seat_number,
        }
        for s in seats
    ]

def get_employee_project(db: Session, employee_code: str):
    employee = (
        db.query(Employee)
        .join(Project, Employee.project_id == Project.id)
        .filter(Employee.employee_code == employee_code)
        .first()
    )

    if employee is None:
        return None

    return {
        "employee": employee.name,
        "employee_code": employee.employee_code,
        "project": employee.project.name,
    }

def get_dashboard_data(db: Session):
    return get_dashboard_summary(db)

def get_project_seating(db: Session, project_name: str):
    allocations = (
        db.query(SeatAllocation)
        .join(Employee, SeatAllocation.employee_id == Employee.id)
        .join(Project, SeatAllocation.project_id == Project.id)
        .join(Seat, SeatAllocation.seat_id == Seat.id)
        .filter(
            func.lower(Project.name) == project_name.lower(),
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .order_by(Employee.employee_code)
        .all()
    )

    if not allocations:
        return None

    return [
        {
            "employee": a.employee.name,
            "employee_code": a.employee.employee_code,
            "seat": a.seat.seat_number,
            "floor": a.seat.floor,
            "zone": a.seat.zone,
            "bay": a.seat.bay,
        }
        for a in allocations
    ]


def get_project_manager(db: Session, project_name: str):
    project = (
        db.query(Project)
        .filter(func.lower(Project.name) == project_name.lower())
        .first()
    )

    if not project:
        return None

    return {
        "project": project.name,
        "manager": project.manager_name,
    }


def get_floor_employees(db: Session, floor: int):
    allocations = (
        db.query(SeatAllocation)
        .join(Employee, SeatAllocation.employee_id == Employee.id)
        .join(Seat, SeatAllocation.seat_id == Seat.id)
        .join(Project, SeatAllocation.project_id == Project.id)
        .filter(
            Seat.floor == floor,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .order_by(Seat.seat_number)
        .all()
    )

    return [
        {
            "employee": a.employee.name,
            "employee_code": a.employee.employee_code,
            "project": a.project.name,
            "seat": a.seat.seat_number,
        }
        for a in allocations
    ]

def get_all_project_names(db: Session):
    return [project.name for project in db.query(Project).all()]