from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.seat_allocation import SeatAllocation
from app.models.seat import Seat
from app.schemas.seat import SeatCreate, SeatUpdate
from app.models.enums import SeatStatus, AllocationStatus


def create_seat(db: Session, seat_data: SeatCreate) -> Seat:
    existing = (
        db.query(Seat)
        .filter(
            Seat.floor == seat_data.floor,
            Seat.zone == seat_data.zone,
            Seat.seat_number == seat_data.seat_number,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat already exists.",
        )

    seat = Seat(**seat_data.model_dump())

    db.add(seat)
    db.commit()
    db.refresh(seat)

    return seat


def get_seat(db: Session, seat_id: int) -> Seat:
    seat = db.query(Seat).filter(Seat.id == seat_id).first()

    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found.",
        )

    return seat


def get_all_seats(db: Session):
    return db.query(Seat).all()

def get_available_seats(db: Session):
    return (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.AVAILABLE)
        .all()
    )

def update_seat(
    db: Session,
    seat_id: int,
    seat_data: SeatUpdate,
) -> Seat:

    seat = get_seat(db, seat_id)

    update_data = seat_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(seat, key, value)

    db.commit()
    db.refresh(seat)

    return seat


def delete_seat(
    db: Session,
    seat_id: int,
) -> None:

    seat = get_seat(db, seat_id)

    db.delete(seat)
    db.commit()

def get_seat_suggestions(
    db: Session,
    employee_id: int,
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    # Find active allocations for teammates
    teammate_allocations = (
        db.query(SeatAllocation)
        .join(Employee, SeatAllocation.employee_id == Employee.id)
        .join(Seat, SeatAllocation.seat_id == Seat.id)
        .filter(
            Employee.project_id == employee.project_id,
            SeatAllocation.allocation_status == AllocationStatus.ACTIVE,
        )
        .all()
    )

    preferred_floors = {allocation.seat.floor for allocation in teammate_allocations}
    preferred_zones = {allocation.seat.zone for allocation in teammate_allocations}

    suggestions = (
        db.query(Seat)
        .filter(Seat.status == SeatStatus.AVAILABLE)
        .all()
    )

    if preferred_floors or preferred_zones:
        preferred = [
            seat
            for seat in suggestions
            if seat.floor in preferred_floors
            and seat.zone in preferred_zones
        ]

        if preferred:
            return preferred

    return suggestions 