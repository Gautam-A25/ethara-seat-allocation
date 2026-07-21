from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.enums import AllocationStatus, SeatStatus
from app.models.seat import Seat
from app.models.seat_allocation import SeatAllocation
from app.schemas.seat_allocation import (
    SeatAllocationRequest,
    SeatReleaseRequest,
)

def allocate_seat(
    db: Session,
    allocation_data: SeatAllocationRequest,
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == allocation_data.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    seat = (
        db.query(Seat)
        .filter(Seat.id == allocation_data.seat_id)
        .first()
    )

    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found.",
        )

    if seat.status != SeatStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat is not available.",
        )

    existing_employee_allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id == employee.id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if existing_employee_allocation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee already has an active seat allocation.",
        )

    existing_seat_allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.seat_id == seat.id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if existing_seat_allocation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat is already occupied.",
        )

    allocation = SeatAllocation(
        employee_id=employee.id,
        seat_id=seat.id,
        project_id=employee.project_id,
        allocation_status=AllocationStatus.ACTIVE,
    )

    db.add(allocation)

    seat.status = SeatStatus.OCCUPIED

    db.commit()

    db.refresh(allocation)

    return allocation

def release_seat(
    db: Session,
    release_data: SeatReleaseRequest,
):
    allocation = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.employee_id == release_data.employee_id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .first()
    )

    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active seat allocation not found.",
        )

    seat = (
        db.query(Seat)
        .filter(Seat.id == allocation.seat_id)
        .first()
    )

    allocation.allocation_status = AllocationStatus.RELEASED
    allocation.released_date = datetime.now()

    seat.status = SeatStatus.AVAILABLE

    db.commit()
    db.refresh(allocation)

    return allocation